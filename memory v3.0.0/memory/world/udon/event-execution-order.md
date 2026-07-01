---
title: "Event Execution Order - 事件执行顺序"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "本地知识库整理 + VRChat 2026.1.2p2 Release Notes"
source_type: community
version: 1.1
last_review: 2026-06-30
confidence: Medium
tags:
  - world
  - udon
  - event
aliases:
  - 事件
  - "Event Execution Order - 事件执行顺序"
related:
  - animation-events.md
  - avatar-events.md
  - input-events.md
  - ui-events.md
  - ai-navigation.md
---
# Event Execution Order - 事件执行顺序

> 来源: https://creators.vrchat.com/worlds/udon/event-execution-order/
> 抓取日期: 2026-06-15
> 状态: ✅ FACT (官方文档,**关键文档**)
> 关联: `memory/api/events-reference.md` ⭐ 事件方法签名

---

## 🔴 这是 Udon 开发中**最重要的文档之一**!

> **关键警告**: Unity 和 VRChat 更新**可能改变**以下事件执行顺序。
> 不是所有事件都列出,有些事件的执行顺序**取决于场景**(是否是 Object Owner、是否是 Late Joiner 等)。

---

## 概述

Udon 和 Unity 有**内置事件**,在脚本中包含它们时会**自动调用**。

- `Start()` - 每个脚本调用**一次**
- `Update()` - 每帧调用**一次**

写 Udon 脚本时,**了解事件发生顺序**至关重要。

> **官方提示**: Unity 提供(不完整的)[内置事件列表](https://docs.unity3d.com/2022.3/Documentation/Manual/ExecutionOrder.html),其中许多在 VRChat 中也可用。

---

## ⭐ 关键约束:`_onEnable` → `_start` 无间隔执行

> **🔴 关键设计约束(必须记忆)**

```
_onEnable()  ──┐
              │  ← 中间没有空隙!同一帧内连续执行
_start()     ──┘
              ↓
         其他事件按顺序触发
```

### 含义

1. **`_onEnable` 紧接 `_start` 执行**,**中间没有任何空隙**
2. 在 `_onEnable` 中**绝对不能**假设其他 UdonBehaviour 已 `_start`
3. 需要"其他系统就绪"的初始化**必须**放在 `_start` 中

### 详细机制(来自 Udon VM 逆向)

> 来自 `memory/rules/udon-vm-architecture.md` 的事件执行流程:

```csharp
RunEventAdvanced("_onEnable", canRunBeforeStart: true)  // ✅ 允许 Start 前
RunEventAdvanced("_start",    canRunBeforeStart: true)  // ✅ 允许 Start 前
RunEventAdvanced("_interact", canRunBeforeStart: false) // ❌ Start 后才可
```

- VM 内部 `_isReady? _hasDoneStart? _hasError?` 状态检查
- `canRunBeforeStart = true` 的事件可在 Start 前触发
- `canRunBeforeStart = false` 的事件需要 Start 后才可触发

---

## 事件执行顺序图

> **官方原图**: 来自 creators.vrchat.com,显示 Udon + Unity 重要事件执行顺序

### Unity MonoBehaviour 生命周期事件顺序

```
[Awake] (单次,脚本实例化时)
   ↓
[OnEnable] (每次 GameObject 激活)
   ↓
[Start] (单次,首次 Update 前)
   ↓
[FixedUpdate] (固定时间步,默认 50Hz)
   ↓   (0~N 次物理帧)
[Update] (每帧,渲染前)
   ↓
[LateUpdate] (每帧,渲染后)
   ↓
[OnPreCull] / [OnBecameVisible] / [OnWillRenderObject]
   ↓
[OnPostRender] / [OnRenderObject]
   ↓
[OnDisable] (GameObject 失活)
   ↓
[OnDestroy] (GameObject 销毁)
```

### Udon 特有事件(VRChat 上下文)

```
[Start] (同 Unity)
   ↓
[OnPlayerJoined] (其他玩家加入)
   ↓
[OnAvatarChanged] (玩家 Avatar 加载完成) - 可能多次
[OnAvatarEyeHeightChanged] (玩家 Eye Height 变化) - 时序不固定
   ↓
[OnPlayerLeft] (玩家离开)
   ↓
[OnOwnershipRequest] → [OnOwnershipTransferred]
   ↓
[OnPreSerialization] → [OnDeserialization]
```

### 物理事件顺序

```
[OnTriggerEnter] / [OnCollisionEnter]    ← 进入
[OnTriggerStay]   / [OnCollisionStay]    ← 持续(每物理帧)
[OnTriggerExit]   / [OnCollisionExit]    ← 离开
```

### 输入事件

```
[OnMouseDown] → [OnMouseDrag] → [OnMouseUp]
[InputJump] / [InputUse] / [InputGrab] / [InputDrop]  (状态变化时)
[InputMoveHorizontal/Vertical] / [InputLookHorizontal/Vertical]  (轴值变化时)
```

---

## 关键事件对的关键时序

### `OnPlayerJoined` 和 `OnPlayerLeft`

> **🔴 Late Joiner 关键**: 新玩家加入时,已存在的 UdonBehaviour 的 `OnPlayerJoined` **会收到新玩家**

```
玩家 A 加入
  → A 的 OnEnable → Start
  → (其他玩家可能在世界中)

玩家 B 加入(后于 A)
  → B 的 OnEnable → Start
  → 所有 UdonBehaviour.OnPlayerJoined(B)  ← 包括 A 的脚本!

玩家 A 离开
  → 所有 UdonBehaviour.OnPlayerLeft(A)
```

### `OnAvatarChanged` 和 `OnAvatarEyeHeightChanged`

- **本地玩家**: `OnAvatarChanged` 先于 `OnAvatarEyeHeightChanged`
- **远程玩家**: 时序**不固定**(`OnAvatarEyeHeightChanged` 可能先于 `OnAvatarChanged`)

> 详细: `memory/world/udon/avatar-events.md`

### Network 序列化

```
Owner 端: 业务代码 → OnPreSerialization → [网络传输] → OnPostSerialization
Non-Owner:  [网络接收] → OnDeserialization → 业务代码
```

> 详细: `memory/api/networking.md`

---

## 常见错误(踩坑)

### ❌ 在 `_onEnable` 中访问其他 UdonBehaviour

```csharp
// ❌ 错误!  _onEnable 时其他脚本可能还没 _start
public override void _onEnable()
{
    otherBehaviour.someValue = 5;  // otherBehaviour 可能未初始化
}
```

**修复**: 把跨脚本访问移到 `_start`:

```csharp
// ✅ 正确
public override void _start()
{
    otherBehaviour.someValue = 5;  // 此时所有 _onEnable 已完成
}
```

### ❌ 在 `_start` 中假设 Network 已同步

```csharp
// ❌ 错误! Late Joiner 触发 _start 时,可能没有网络数据
public override void _start()
{
    Debug.Log(_syncedValue);  // 可能是初始值,不是同步值
}
```

**修复**: 在 `OnDeserialization` 中使用同步数据。

### ❌ 在 `Update` 中无脑检查

```csharp
// ❌ 错误!  即使数据没变也每帧检查
void Update() { CheckForChange(); }
```

**修复**: 用事件驱动而非 Update 轮询。

---

## Udon VM 内部执行流程(逆向工程)

> 来自 `memory/rules/udon-vm-architecture.md`

### 事件检测(ProcessEntryPoints)

UdonBehaviour 通过**符号表**检测程序员定义的事件:

| 导出符号 | 触发的事件 | 代理类型 |
|---|---|---|
| `_interact` | Interact | — |
| `_update` | Update | RegisterUpdate |
| `_lateUpdate` | LateUpdate | RegisterUpdate |
| `_fixedUpdate` | FixedUpdate | RegisterUpdate |
| `_postLateUpdate` | PostLateUpdate | RegisterUpdate |
| `_onRenderObject` | OnRenderObject | OnRenderObjectProxy |
| `_onWillRenderObject` | OnWillRenderObject | OnWillRenderObjectProxy |
| `_onTriggerStay` | OnTriggerStay | OnTriggerStayProxy |
| `_onCollisionStay` | OnCollisionStay | OnCollisionStayProxy |
| `_onAnimatorMove` | OnAnimatorMove | OnAnimatorMoveProxy |
| `_onAudioFilterRead` | OnAudioFilterRead | OnAudioFilterReadProxy |

### 事件执行流程(RunEventAdvanced)

```
RunEventAdvanced("eventName", canRunBeforeStart)
  → _isReady? _hasDoneStart? _hasError? _udonVM null?  // 状态检查
  → _eventTable.TryGetValue("eventName", out entryPoints)
  → foreach entryPoint: RunProgram(entryPoint)
    → SetProgramCounter(entryPoint)
    → _udonVM.Interpret()  // VM 解释执行
    → 错误则 _hasError = true, enabled = false  // 🔴 永久停止
    → 恢复 program counter
```

### VariableChangeEvent(FieldChangeCallback 底层)

```
"_var_changed__variableName" 前缀匹配
  → 解析变量名
  → 建立 variableAddress → (eventAddress, oldValueAddress) 映射
  → 变量变化时自动触发
```

> 详细: `memory/api/udonsharp-runtime.md`

---

## 与知识库互补

- **Udon 事件完整参考**: `memory/api/events-reference.md` ⭐ 事件方法签名
- **Udon VM 架构**: `memory/rules/udon-vm-architecture.md` ⭐ RunEventAdvanced 机制
- **UdonSharp 运行时**: `memory/api/udonsharp-runtime.md` ⭐ FieldChangeCallback
- **Networking 序列化**: `memory/api/networking.md` ⭐ OnPre/Post/Deserialization
- **Avatar 事件**: `memory/world/udon/avatar-events.md` ⭐ Avatar 加载时序
- **Animation 事件**: `memory/world/udon/animation-events.md` ⭐ Animator 时序

---

## 相关 VRChat 官方文档

- [Event Execution Order](/worlds/udon/event-execution-order) - 本页官方原版
- [Unity Execution Order](https://docs.unity3d.com/2022.3/Documentation/Manual/ExecutionOrder.html) - 完整 Unity 事件表

## 🔄 VRChat 修复历史 (2026.1.2p2+)

> **FACT** (2026.1.2p2):"Fixed an issue causing `PostLateUpdate` events to be called one frame too late."

### 问题描述

| 项目 | 详情 |
|------|------|
| **受影响事件** | 使用 `EventTiming.PostLateUpdate` 的自定义 Udon 事件 |
| **原行为** | 比预期**晚一帧**触发,导致基于 `PostLateUpdate` 的逻辑与渲染时序错位 |
| **修复行为** | `PostLateUpdate` 事件现在**在正确的帧**触发 |
| **修复版本** | 2026.1.2p2+ |

### 创作者影响

| 影响项 | 说明 |
|--------|------|
| **时序修复** | `PostLateUpdate` 相关逻辑现在准时执行 |
| **无需代码改动** | 纯引擎层修复 |
| **配合 SDK 3.10.2** | `EventTiming.PostLateUpdate/FixedUpdate` 引入后逐步稳定 |

### 历史背景

> SDK 3.10.2 引入了 `EventTiming.PostLateUpdate` 和 `EventTiming.FixedUpdate`,允许自定义事件绑定到 Unity 的特定更新阶段。
> 2026.1.2p2 修复了时序偏差,这是该 API 引入后的**第一个重大修正**。

### 验证建议

```csharp
// 在 Update 中检查 PostLateUpdate 时序
public void Update()
{
    Debug.Log($"[Frame {Time.frameCount}] Update at {Time.time}");
}

public override void PostLateUpdate()  // 自定义事件
{
    Debug.Log($"[Frame {Time.frameCount}] PostLateUpdate at {Time.time}");
}
// 2026.1.2p2+:两个日志的 frameCount 应相同
// 2026.1.2p1 及之前:PostLateUpdate 的 frameCount 比 Update 大 1
```

### 关联文档

- `memory/api/events-reference.md` - 自定义事件绑定
- SDK 3.10.2 Release Notes - EventTiming.PostLateUpdate/FixedUpdate 引入
