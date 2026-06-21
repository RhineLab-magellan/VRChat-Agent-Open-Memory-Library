# Animation Events - Animator 事件白名单

> 来源: https://creators.vrchat.com/worlds/udon/animation-events
> 抓取日期: 2026-06-15
> 状态: ✅ FACT (官方白名单)

---

## 概述

可以从 **Animation** 中[调用事件](https://docs.unity3d.com/2022.3/Documentation/Manual/script-AnimationWindowEvent.html)。本页列出**可被 Animation Event 调用**的**白名单方法**。

> **🔴 关键**: 不在白名单中的事件,VRChat 中**不会触发**!

---

## 完整白名单

### UdonBehaviour 控制

| 事件方法 | 用途 |
|---|---|
| `RunProgram` | 重启 Udon 程序(等价于重新执行 `_start`) |
| `SendCustomEvent` | 发送自定义事件 |

### Animator 控制(白名单内)

| 事件方法 | 用途 |
|---|---|
| `Play` | 播放动画 |
| `Pause` | 暂停 |
| `Stop` | 停止 |
| `PlayInFixedTime` | 固定时间播放 |
| `Rebind` | 重新绑定 |
| `SetBool` | 设置 bool 参数 |
| `SetFloat` | 设置 float 参数 |
| `SetInteger` | 设置 int 参数 |
| `SetTrigger` | 设置 trigger 参数 |
| `ResetTrigger` | 重置 trigger |

### GameObject 控制

| 事件方法 | 用途 |
|---|---|
| `SetActive` | 启用/禁用 GameObject |

---

## 与 UI Events 白名单的关系

> **注意**: Animation Events 白名单 **与** UI Events 白名单**不同**!

| 维度 | Animation Events | UI Events |
|---|---|---|
| 触发源 | Unity Animation 关键帧 | Unity UI 事件 |
| 数量 | **12 个方法**(很窄) | **28 个组件**(很广) |
| 主要用法 | 同步动画时间 + Udon 逻辑 | UI 直接控制组件 |

> UI Events 完整白名单: `memory/world/udon/ui-events.md` ⭐ 28 个组件 100+ 成员

---

## 与 World Animator 系统的关系

> **核心概念**: World Animator = **逻辑驱动系统** (Udon Event → SetBool/SetTrigger → State Machine)

- World Animator 中的 **Animation Event** 是 Animator 时间轴到达某帧时触发的方法调用
- 本页白名单定义了**可被 Animation Event 调用的方法**

> 详细 Animator 系统: `memory/world/udonsharp-compilation.md` 和 `memory/api/animator.md`

---

## 典型用法

### 1. 动画结束时触发 Udon 逻辑

```csharp
// UdonSharpBehaviour 中
public void OnAnimationEnd()  // 动画最后帧调用 SendCustomEvent
{
    Debug.Log("Animation finished!");
    SpawnParticle();
}
```

```
AnimationClip 最后帧
  → Animation Event: SendCustomEvent("OnAnimationEnd")
  → UdonBehaviour.OnAnimationEnd()
```

### 2. 同步多个 Animator

```
Animator A 播放到第 30 帧
  → Animation Event: AnimatorB.Play("StateName")
  → Animator A 切到下一 State
```

### 3. 触发 Udon 重启

```
AnimationClip
  → Animation Event: RunProgram
  → UdonBehaviour 重新执行 _start
```

> **典型用途**: 重置 Udon 状态机(配合 Animation 作为"按钮"使用)

---

## 风险与限制

### 不在白名单的方法 ❌

- **任何** 自定义 Udon 方法(除 `SendCustomEvent` 包装外)
- **任何** Transform/Rigidbody 等组件方法(除白名单内)
- **任何** Networking/Player API 方法

### 静默失败

> **🔴 关键**: 不在白名单的方法**会被静默忽略**,不会报错

- 在 Editor 中测试时**不会发现**
- 进入 VRChat 后才发现"动画播放了但事件没触发"
- **建议**: 在 Animator 设置中,事件名称拼写**100% 准确**(大小写敏感)

---

## 与知识库互补

- **UI Events 白名单**: `memory/world/udon/ui-events.md`
- **Udon 事件完整参考**: `memory/api/events-reference.md`
- **Animator API**: `memory/api/animator.md`
- **UdonSharp 编译管线**: `memory/world/udonsharp-compilation.md`

---

## 相关 VRChat 官方文档

- [Animation Events](/worlds/udon/animation-events)
- [Unity Animation Window Events](https://docs.unity3d.com/2022.3/Documentation/Manual/script-AnimationWindowEvent.html)
- [UdonSharp Event Nodes](/worlds/udon/graph/event-nodes)
