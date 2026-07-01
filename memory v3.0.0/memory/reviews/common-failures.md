---
title: "Common Failures"
category: reviews
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - reviews
  - review
  - networking
  - sync
  - serialization
  - ownership
aliases:
  - "Common Failures"
  - common-failures
related:
  - review-checklist.md
  - severity-model.md
  - "../api/events-reference.md"
  - "../api/networking.md"
  - "../rules/networking-rules.md"
---
# Common Failures


---

## FAIL-01: 忘记 RequestSerialization

### 症状
修改了 `[UdonSynced]` 变量，但远端看不到变化。

### 原因
Manual Sync 模式下，修改 synced variable 后没有调用 `RequestSerialization()`。

### 修复
在每个修改 synced variable 的路径末尾加 `RequestSerialization()`。

### 规则
参见 RULE-NW-02

---

## FAIL-02: Late Joiner 看到默认状态

### 症状
Host 触发了状态变化，新加入玩家看到的是初始默认状态而不是当前状态。

### 原因
状态只通过 Network Event 同步，没有 `[UdonSynced]` 变量保存持久状态。

### 修复
将状态用 `[UdonSynced]` 变量存储，在 `OnDeserialization()` 中重建表现。

### 规则
参见 RULE-NW-03

---

## FAIL-03: 非 Owner 修改 Synced Variable

### 症状
多个玩家同时操作对象，状态混乱。

### 原因
没有检查 ownership 就修改 synced variable。

### 修复
在修改 `[UdonSynced]` 变量前检查 `Networking.IsOwner(gameObject)`。

### 规则
参见 RULE-NW-01

---

## FAIL-04: Continuous Sync 滥用

### 症状
网络卡顿、延迟大、房间内玩家互相影响性能。

### 原因
离散状态使用 Continuous Sync，每帧序列化所有 synced variable。

### 修复
离散状态改用 Manual Sync + RequestSerialization。

### 规则
参见 RULE-NW-06

---

## FAIL-05: 频繁 Debug.Log 导致卡顿

### 症状
Udon VM 执行卡顿，帧率下降。

### 原因
`Debug.Log()` 在 Udon VM 中执行成本远高于 native Unity。每帧打印会导致显著的性能问题。

### 修复
- 移除热路径中的 Debug.Log
- 使用条件编译 `#if UNITY_EDITOR` 包裹调试日志
- 用 int 计数器限制日志频率

---

## FAIL-06: 跨 Behaviour 链式调用

### 症状
事件响应延迟大、行为不可预测。

### 原因
A.SendCustomEvent → B.Method → B.SendCustomEvent → C.Method 的链式派发，每跳有帧延迟。

### 修复
集中逻辑到同一个 Behaviour，用直接方法调用替代链式事件。

### 规则
参见 RULE-MV-05

---

## FAIL-07: Update 中 GetComponent

### 症状
明显的帧率下降，尤其是在多名玩家在房间时。

### 原因
每帧执行 `GetComponent<T>()` 在 Udon VM 中是非常昂贵的逐步查找操作。

### 修复
在 `Start()` 中缓存引用，或使用 `[SerializeField]` 预绑定。

### 规则
参见 RULE-PF-02

---

## FAIL-08: 大数组频繁重分配

### 症状
内存压力、Udon VM 执行骤停。

### 原因
在热路径中创建或重分配大数组。

### 修复
使用固定大小数组 + 手动追踪有效元素数量。

---

## FAIL-09: Network Event 传播延迟错觉

### 症状
远端玩家看到"跳跃"或"瞬移"，而非平滑过渡。

### 原因
Animation 触发用 Network Event，但动画的中间帧没有被同步。远端直接跳到最终状态。

### 修复
- 将状态变化用 `[UdonSynced]` 同步
- 远端根据状态值本地播放动画
- Network Event 仅用于触发 AudioSource/ ParticleSystem

---

## FAIL-10: Owner 离开后状态丢弃

### 症状
owner 玩家离开房间后，对象看起来"重置"了。

### 原因
ownership 转移到新玩家，但新 owner 没有收到完整状态同步。

### 修复
- 确保所有状态通过 `[UdonSynced]` 持久化
- ownership 转移时 Udon 自动传输 synced variables
- 在 `OnOwnershipTransferred()` 中不需要额外操作（除非有本地缓存需要重建）

---

## FAIL-11: uGUI Button Owner Check 使非 Owner 按钮无响应

### 症状
非 owner 玩家点击 UI 按钮无任何反应。

### 原因
uGUI OnClick 在所有客户端本地触发。用 `IsOwner` return 阻止了非 owner 的执行。

### 修复
方案 A: `SendCustomNetworkEvent(NetworkEventTarget.Owner, ...)` 委托给 owner
方案 B: 先 `Networking.SetOwner()` 再执行本地操作

---

## FAIL-12: Continuous Sync String 静默截断

### 症状
远端玩家看到的字符串不完整或损坏。

### 原因
Continuous Sync 约 200 字节共享预算。UTF-16 每字符 2 字节，超过约 100 字符被静默截断——无错误无警告。

### 修复
- 赋值前检查长度并截断
- 长字符串改用 Manual Sync
- 在 Continuous Sync 中保持字符串极短

---

## FAIL-13: Manual Sync 大数组溢出静默丢弃

### 症状
Manual Sync 的大数组数据从未到达远端，接收方看到旧数据。

### 原因
序列化 payload 超过约 280KB (280,496 bytes) 时，整个包被静默丢弃——无部分投递、无错误。

### 修复
- 序列化前估算字节数
- 大数组用 `byte[]` 替代 `int[]`（节省 75% 空间）
- 超大数据考虑分块同步或 delta sync

---

## FAIL-14: Continuous 和 Manual Sync 混用

### 症状
既想要自动同步又想手动控制，结果行为不符合预期。

### 原因
`BehaviourSyncMode` 是单一 enum。Continuous mode 中 `RequestSerialization()` 冗余；Manual mode 中没有自动同步。两者不能叠加。

### 修复
分离到不同 Behaviour：Continuous 用于位置/旋转，Manual 用于离散状态。

---

## FAIL-15: PlayerData 在 OnPlayerRestored 前写入

### 症状
数据保存似乎成功但下次 session 读取不到。

### 原因
在 `OnPlayerRestored` 触发前调用 `PlayerData.Set*` 会被静默忽略。

### 修复
用 `_dataReady` flag 守卫所有写入，flag 在 `OnPlayerRestored` 中设为 true。

---

## FAIL-16: [NetworkCallable] 在 SDK < 3.8.1

### 症状
代码编译通过但网络方法从未被远端调用。

### 原因
`[NetworkCallable]` 属性在 SDK < 3.8.1 编译通过但运行时静默忽略。

### 修复
验证 SDK >= 3.8.1。旧版本用 synced variables + `SendCustomNetworkEvent`。

---

## FAIL-17: Dynamics API 在 SDK < 3.10.0

### 症状
`OnPhysBoneGrab`、`OnContactEnter` 等回调从未触发。

### 原因
World-side Dynamics 在 SDK 3.10.0 才引入。旧 SDK 编译通过但运行时静默忽略。

### 修复
验证 SDK >= 3.10.0。

---

## FAIL-18: 所有客户端在 Update 中运行游戏逻辑

### 症状
多人同时修改状态，owner 频繁切换，数据混乱。

### 原因
条件在所有客户端同时为 true，每个人都调用 SetOwner + 修改值。

### 修复
在 Update 开头检查 `if (!Networking.IsOwner(gameObject)) return;`。只有 owner 运行游戏逻辑，其他客户端在 `OnDeserialization` 中更新显示。

---

## FAIL-19: Enum.ToString() 输出数字而非名称

### 症状
`Debug.Log(enumValue.ToString())` 输出 `"0"` 而非枚举名称。

### 修复
使用 `switch` + 手动字符串映射。

---

## FAIL-20: Enum 类型转换与操作符写在一起导致运行时异常

### 症状
`dataList.Add((int)anEnum)` 抛出 `"Cannot retrieve heap variable of type 'Int32' as type 'DataToken'"`。

### 修复
先将 Enum cast 到单独的 `int` 变量，再使用该变量。

---

## FAIL-21: Manual Sync 多变量分帧同步导致 OnDeserialization 不可靠

### 症状
`OnDeserialization()` 触发时某些 synced variable 仍是旧值。

### 修复
- 压缩每个 Behaviour 的 synced 变量数量
- 关键变量用 `[FieldChangeCallback]` 独立监控
- 不要假设所有变量同时到达

---

## FAIL-22: Continuous Sync 丢包导致远端永久不同步

### 症状
远端玩家偶尔看不到最新的位置/旋转，状态"卡住"。

### 修复
关键状态用 Manual Sync（有确认机制）。

---

## FAIL-23: `internal` 关键字导致方法随机不可用

### 症状
方法有时有效有时无效，无任何错误提示。

### 修复
使用条件编译 `#if COMPILER_UDONSHARP public #else internal protected #endif`。

---

## FAIL-24: Update 中分配内存导致 GC 冻结

### 症状
VR 中周期性卡顿/黑屏，帧时间突增。

### 修复
- Start 中预分配所有数组
- 用 `StringBuilder` 替代字符串拼接
- 避免 Update 中的隐式装箱（如 `Debug.Log` 内部格式化）
- 使用固定大小 buffer + 手动索引

---

## FAIL-25: 10 秒超时导致 Behaviour 永久停止

### 症状
World 运行一段时间后某个 UdonBehaviour 完全停止工作，无报错、无恢复。

### 原因
Udon VM 的 `CheckExecutionTimeLimit` 在单次 `Interpret()` 调用超过 10 秒时强制 `_halted = true`，且 `_hasError = true` → `enabled = false`。**Behaviour 永久禁用，不会恢复。**

### 触发场景
- 无限循环/递归
- `Update()` 中过度计算 + 大量 EXTERN 调用 → 单帧解释执行超过 10 秒
- 大数组的嵌套循环在纯解释器下比预期慢得多

### 修复
- 对循环添加边界检查和计数器保护
- 确保递归有明确的终止条件 + `[RecursiveMethod]`
- 大计算拆分为多帧（`SendCustomEventDelayedFrames`）
- 参见 `rules/udon-vm-architecture.md` 第 5.2 节

---

## FAIL-26: Collision Ownership Transfer 导致所有权转移风暴

### 症状
大量玩家同时碰撞，所有人卡顿、网络拥堵。

### 原因
在 Collision 事件中调用 `Networking.SetOwner()`。历史上存在 bug，多人同时碰撞会导致所有权反复转移。

### 修复
VRC_Object Sync 自动处理。不要在 Collision 中手动 SetOwner。Pickup 事件中 ownership 也自动转移。

---

## FAIL-27: 网络事件过多 → Death Runs

### 症状
数据丢失、远端行为不一致。

### 原因
网络事件过多导致 "Death Runs"——数据在传输中被丢弃。

### 修复
用 synced variable + RequestSerialization 替代大量频繁的网络事件。

---

## FAIL-28: 同步变量设置后立即发网络事件 → 乱序

### 症状
远端收到网络事件时 synced variable 还是旧值。

### 原因
同步变量更新比网络事件慢，两者到达顺序不保证。

### 修复
不要依赖"先 RequestSerialization 再 SendCustomNetworkEvent"的顺序。用 OnDeserialization/FieldChangeCallback 在远端触发后续逻辑。

---

## FAIL-29: 父 Selector 强制覆盖子 syncMode 导致初始化时序错乱


### 症状
互斥选择器(SwitchSelector)启动后,子开关无法正确响应同步状态,或 OnDeserialization 中出现 IsGlobal 标志错误。

### 原因
SwitchSelector 的 `Start()` 与 SwitchBase 的 `Start()` 执行顺序**不被 Udon 保证**:
- 若 Selector 立即调 `ForceSyncModeToSwitches()`,子开关的 syncMode 已被改为 None
- 但子开关的 `OnDeserialization` 可能在更早的 syncMode(Local)状态下被触发
- 子开关走错分支,IsGlobal 标志与实际状态不一致

### 修复
**强制延迟 1 帧初始化**:
```csharp
private void Start() {
    SendCustomEventDelayedFrames(nameof(DeferredInitialize), 1);
}

public void DeferredInitialize() {
    ForceSyncModeToSwitches();  // 此时所有子 Start() 已完成
    EnsureGlobalOwnership();
}
```

更优做法:在子开关的 `OnDeserialization` 中**不判断 IsGlobal**,统一信任 synced 值:
```csharp
// SwitchBase.cs
// NOTE: IsGlobal チェックをここでは行わない。
// SwitchSelector (Global) 使用時、SwitchBase の syncMode は Start() 時点ではまだ Local...
public override void OnDeserialization() {
    _toggleIsOn = _syncedToggleIsOn;  // 不判断 IsGlobal
    ApplyValueFromExternal(...);
}
```

### 规则
参见 `memory/patterns/exclusive-control-selector.md` + `memory/rules/multi-vm-rules.md` §初始化时序

---

## FAIL-30: 滑块插值自我回声导致抖动


### 症状
Master 拖动滑块,本地值在"自己改的"和"网络回声"之间反复跳动,出现明显抖动。

### 原因
Master 写入 synced 值 → 触发自己的 OnDeserialization → 插值器"覆盖回中间值" → 滑块抖动。

**触发链路**:
1. Master: `sliderValue = X; RequestSerialization();`
2. Master OnDeserialization: `InterpolateTo(_syncedSliderValue, 0.3f);` ← **回声被当远端数据**
3. 0.3s 内插值器在 `sliderValue` 写入新值 → 再次序列化...
4. 死循环

### 修复
**双标志分离发送方/接收方**:
```csharp
// 插值器输出时(本地写入中)
public bool IsInterpolating { get; private set; }       // 是否在插值
public bool IsInterpolationApplyingOutput { get; private set; }  // 插值器是否正在输出

// OnDeserialization 中
if (s.IsInterpolating && !s.IsInterpolationApplyingOutput) {
    // 接收方:从远端拉数据,本地应用
    s.ApplyValueFromExternal(v, ...);
} else {
    // 发送方 / 输出中:忽略,避免回声
    return;
}
```

### 规则
参见 `memory/patterns/master-follower-syncer.md` §回声排除

---

## FAIL-31: Editor 反射访问私有字段导致重命名后静默崩


### 症状
Editor 自定义 Inspector 工作正常,但运行时某次重构后,Editor 中调用的字段值无法正确显示,运行时取值正常。

### 原因
Editor 工具用 `Reflection` 访问 UdonSharpBehaviour 的私有字段:
```csharp
var valueField = typeof(MirrorController).GetField(
    "_value", BindingFlags.NonPublic | BindingFlags.Instance);
valueField.SetValue(controller, newValue);
```

**隐患**:
- 字段重命名/删除 → 编译通过,**运行时崩**或读到 null
- 无编译期检查
- 维护者可能不知道 Editor 依赖某个私有字段

### 修复
**方案 A: 用 `[SerializeField] internal`** 替代 private
```csharp
[SerializeField] internal float _value;  // Editor 可见,无需反射
```

**方案 B: 用 `EditorOnly` API**
```csharp
#if UNITY_EDITOR
var so = new SerializedObject(controller);
so.FindProperty("_value").floatValue = newValue;
so.ApplyModifiedProperties();
#endif
```

**方案 C: 提取公共属性**
```csharp
public float Value {
    get => _value;
    set { _value = value; }
}
```

### 规则
参见 `memory/rules/udonsharp-deep-pitfalls.md` (Editor-Only 反射陷阱)

---

## FAIL-32: `SendCustomEventDelayedFrames(1)` 初始化在低帧率设备不可靠


### 症状
Quest 等低帧率设备(20-30fps)上,延迟初始化的脚本有时工作,有时不工作。

### 原因
`SendCustomEventDelayedFrames(1)` = "1 帧后执行" = 33ms(30fps) ~ 50ms(20fps)。
- 1 帧延迟 = **不可预测的时长**
- 假设 60fps: 1 帧 = 16.67ms,后续 Start 100% 已完成
- 假设 20fps: 1 帧 = 50ms,但部分 Start 可能仍在其他 Behaviour 队列中
- **1 帧延迟本质是"魔法数字",无保证**

### 修复
**方案 A: 用 2-3 帧延迟**(容错更好):
```csharp
SendCustomEventDelayedFrames(nameof(DeferredInitialize), 3);  // 3 帧 ≈ 50-100ms
```

**方案 B: 显式初始化链**(更可靠):
```csharp
// 父级 Init() 显式调用子级 Init()
public void Init() {
    _childA.Init();
    _childB.Init();
    ForceSyncModeToSwitches();
}
```

**方案 C: 用 bool flag 守门 + 多次尝试**:
```csharp
private int _initAttempts = 0;

public void DeferredInitialize() {
    if (AreChildrenReady()) {
        DoInitialize();
    } else if (_initAttempts++ < 5) {
        SendCustomEventDelayedFrames(nameof(DeferredInitialize), 2);
    } else {
        Debug.LogError("Init timeout");
    }
}
```

### 规则
参见 `memory/rules/multi-vm-rules.md` §初始化时序 + `memory/rules/performance-rules.md` §Update 成本
