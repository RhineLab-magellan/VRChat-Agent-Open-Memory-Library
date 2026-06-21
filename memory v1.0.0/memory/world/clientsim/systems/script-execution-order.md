# Script Execution Order

> 来源: [VRChat Creator Docs - Script Execution Order](https://creators.vrchat.com/worlds/clientsim/systems/script-execution-order)
> 索引日期: 2026-06-15

---

## 概述

ClientSim 在 Unity 中预设了**严格的 Script Execution Order**,确保 11 个核心系统在 Play Mode 中以正确顺序执行。

> ⚠️ **修改 ClientSim 的 Script Execution Order 可能导致交互、输入、Udon 事件触发时序异常,除非完全理解每个系统职责,否则不建议调整。**

---

## Script Execution Order 完整表

| Execution Order | System Name | Description |
|-----------------|-------------|-------------|
| **-Infinity** | **UnityInputSystem** | Unity InputSystem 在所有 MonoBehaviour 之前更新。用户按钮输入被发送到 `ClientSimInput` 并分发事件。 |
| **-3000** | **TrackingProvider** | 检查输入以更新 TrackingProvider。例如:Desktop 头部 X 旋转。 |
| **-3000** | **PlayerController** | 在射线检测前更新 Player 位置。 |
| **-2000** | **PlayerRaycaster** | 将 PlayerHands 位置更新到 TrackingProvider 的手部数据。射线检测以查找世界中的可交互对象。**必须在 EventSystems 更新前完成**。 |
| **-1000** | **Unity Event System** | 发送鼠标事件以与 UI 交互。**顺序不可更改**。 |
| **0** | **ClientSimBehaviours** | (ClientSim 自定义 MonoBehaviour 的默认执行点) |
| **0** | **UdonBehaviour** | 向 Udon Programs 发送 Update 事件。 |
| **1** | **UdonInput** | **必须在 `UdonBehaviour.Update` 之后**,以确保正确的事件顺序。 |
| **10000** | **ClientSimBaseInput** | 更新 Input 事件的当前帧 tick。仅需确保测试与 Play Mode 在 Input 处理时机上行为一致。 |
| **30000** | **PlayerStationManager** | **尽可能晚**地更新 Station 上玩家的位置,以便所有其他脚本先完成评估。 |
| **30001** | **TooltipManager** | 在最终确定玩家位置后,更新 Tooltip 的视觉位置。 |
| **31000** | **PostLateUpdater** | VRChat 的 `PostLateUpdate` 事件被发送到 UdonBehaviours。 |

---

## 执行阶段分析

### 阶段 1:输入采集 (-Infinity ~ -3000)

```
UnityInputSystem (-Infinity)
    │ 读取硬件输入
    ▼
ClientSimInput (派发)
    │
    ├──► TrackingProvider (-3000)    // 头部 / 手部姿态
    │
    └──► PlayerController (-3000)    // 玩家位移(WASD)
```

**关键点**:
- `UnityInputSystem` 必须在所有 MonoBehaviour 之前
- `TrackingProvider` 与 `PlayerController` 并列,均早于 -2000

### 阶段 2:交互检测 (-2000 ~ -1000)

```
PlayerRaycaster (-2000)
    │ 发射射线,查找 Pickup / Interact
    │
    ▼
Unity Event System (-1000)
    │ UI 鼠标事件分发
```

**关键点**:
- `PlayerRaycaster` **必须早于** `Unity Event System`,否则交互检测的 GameObject 未及时更新
- `Unity Event System` 顺序**不可更改**(Unity 内置约束)

### 阶段 3:Udon 执行 (0 ~ 1)

```
ClientSimBehaviours (0)   // ClientSim 内部组件
UdonBehaviour (0)          // Udon Update 事件
    │
    ▼
UdonInput (1)              // Udon Input 事件
```

**关键点**:
- `UdonInput` 必须在 `UdonBehaviour.Update` 之后,确保 Input 事件响应 Udon 状态变化
- 顺序差 1 是**有意为之**,用于保证 Udon 事件正确分发

### 阶段 4:后置处理 (10000 ~ 31000)

```
ClientSimBaseInput (10000)    // Input 帧 tick
    │
    ▼
PlayerStationManager (30000)  // Station 玩家位置(尽可能晚)
    │
    ▼
TooltipManager (30001)        // Tooltip 视觉(玩家位置确定后)
    │
    ▼
PostLateUpdater (31000)       // VRChat PostLateUpdate
```

**关键点**:
- `PlayerStationManager` 与 `TooltipManager` 顺序差 1,确保 Tooltip 在玩家位置确定后更新
- `PostLateUpdater` 触发 VRChat 的 `PostLateUpdate` 事件给 UdonBehaviours

---

## 工程意义

### 1. 输入链路延迟

| 现象 | 原因 |
|------|------|
| 按下交互键,Udon 下一帧才收到事件 | `UdonInput` 排在 `UdonBehaviour.Update` 之后 1 个单位 |
| UI 点击与 GameObject 拾取冲突 | `PlayerRaycaster` 早于 `Unity Event System`,Unity 先分发 UI 事件 |

### 2. 性能与确定性

| 维度 | 设计 |
|------|------|
| **测试可重现** | `ClientSimBaseInput` 单独在 10000 更新,统一 Input tick 时机 |
| **位置稳定** | `PlayerStationManager` 在 30000 晚于所有常规逻辑,Station 上位置不会被其他系统覆盖 |
| **VRChat 兼容** | `PostLateUpdater` 31000 模仿 VRChat 客户端的 PostLateUpdate 时机 |

### 3. 自定义脚本介入点

| 想做的事 | 推荐 Order |
|----------|-----------|
| 比 Udon 更早读取 Input | `-3000 ~ -1` |
| 比 ClientSim 组件更早 | `< 0`(负值) |
| 在 Udon Update 之前执行 | `-1 ~ 0` |
| 在 Udon Update 之后执行 | `2 ~ 9999` |
| 比 Station 更新更晚 | `30000 ~ 30000`(很窄) |
| 比 PostLateUpdater 更晚 | `> 31000` |

> ⚠️ **不建议**将自己的脚本插入 `UnityInputSystem`/`Unity Event System` 之间,可能破坏输入链路。

---

## 关键数字速查

| Order | 含义 |
|-------|------|
| `-Infinity` | 早于所有 MonoBehaviour |
| `-3000` | 输入与玩家更新阶段 |
| `-2000` | 交互检测阶段 |
| `-1000` | UI 事件阶段(不可更改) |
| `0` | 默认阶段 |
| `1` | Udon 紧随后置 |
| `10000` | Input tick 收尾 |
| `30000` | Station / Tooltip 阶段 |
| `31000` | PostLateUpdate 阶段 |

---

## 相关页面

- [Systems Index](index.md) - 回到 Systems 父目录
- [Architecture](architecture.md) - 整体架构
- [Editor](editor.md) - Editor 子系统
- [Runtime](runtime.md) - Runtime 子系统
