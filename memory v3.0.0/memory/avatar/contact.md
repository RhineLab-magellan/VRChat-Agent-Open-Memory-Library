---
title: "Avatar Contact System (VRC Contact, 2026.2.1+)"
category: avatar
subcategory: contact
knowledge_level: applied
status: active
source: "VRChat 官方文档 creators.vrchat.com/avatars/contact + 2026.2.1 Release Notes"
source_type: official
version: 1.0
last_review: 2026-07-01
confidence: High
tags:
  - avatar
  - contact
  - vrc-contact
  - dynamics
  - sdk-3-10
aliases:
  - "VRC Contact"
  - "Avatar Contact"
  - "Contact System"
  - 接触系统
  - "VRC Contact Receiver"
  - "VRC Contact Sender"
related:
  - api/dynamics.md
  - avatar-dynamic-bone-limits.md
  - avatar/optimization-guide.md
  - avatar/performance-benchmarks.md
  - world/scene-components/index.md
  - world/udon/world-debug-views.md
---

# Avatar Contact System (VRC Contact, 2026.2.1+)

> 2026.2.1 Release Notes 引入 Avatar-side 公开 Contact API。
> 本文档汇总 Avatar ↔ World / Avatar ↔ Avatar 的接触检测机制与限制。

---

## 概述

VRC Contact 是 VRChat 内置的接触检测系统,与 PhysBone 同属 Dynamics 框架。2026.2.1 起 Avatar 可通过 `VRCContactReceiver` 组件公开接触行为,World 端通过 Udon 事件 `OnContactEnter` / `OnContactExit` / `OnContactStay` 接收通知。

| 维度 | World Contact (SDK 3.10.0+) | Avatar Contact (2026.2.1+) |
|------|------------------------------|------------------------------|
| 发送方 | World 对象 (`VRCContactSender`) | Avatar 骨骼 (`VRCContactReceiver` 上配对 Sender) |
| 接收方 | World 对象 (`VRCContactReceiver`) | Avatar 公开参数 / 动画 / FX Layer |
| 触发 | Udon `OnContactEnter` 等 | Animator 参数 / PhysBone 状态 |
| 限制 | 1024 房间上限 | 见 §性能基准 |

---

## 核心组件

### VRCContactSender(接触发射器)

挂载到 GameObject 上,定义接触源的位置、形状、碰撞标签。

| 字段 | 说明 |
|------|------|
| `shape` | Sphere / Capsule / Cube / Plane,定义接触体积 |
| `collisionTags` | 字符串标签列表,用于 Sender ↔ Receiver 匹配 |
| `radius` / `size` | 接触体积大小 |
| `allowSelfContact` | 是否允许自身 Avatar 的其他 Sender 触发 |

### VRCContactReceiver(接触接收器)

挂载到 GameObject 上,定义接收接触的目标。

| 字段 | 说明 |
|------|------|
| `shape` | 同 Sender |
| `collisionTags` | 至少 1 个与 Sender 匹配才触发 |
| `onEnter` | 进入时触发的事件 |
| `onExit` | 离开时触发的事件 |
| `onStay` | 持续接触时每帧触发 |
| `allowSelfContact` | 同 Sender |

---

## World 端 Udon 事件

### 三个核心事件

```csharp
using VRC.Dynamics;

public override void OnContactEnter(ContactReceiverInfo info) {
    // info.isAvatar - bool,是否来自 Avatar
    // info.player - VRCPlayerApi(可能为 null)
    // info.contactPoint - Vector3 接触点
    // info.collisionTags - 触发接触的标签数组
    if (info.isAvatar && info.player != null) {
        Debug.Log($"Touched by {info.player.displayName}");
    }
}

public override void OnContactExit(ContactReceiverInfo info) {
    // 离开事件
}

public override void OnContactStay(ContactReceiverInfo info) {
    // 持续接触(每帧)
}
```

### ContactReceiverInfo 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `isAvatar` | bool | 是否来自 Avatar(World Sender 也可为 true) |
| `isLocal` | bool | 是否本地玩家触发 |
| `player` | VRCPlayerApi | 触发玩家(可能为 null) |
| `contactPoint` | Vector3 | 接触点世界坐标 |
| `collisionTags` | string[] | 触发标签 |

---

## Avatar ↔ World 通信

### 场景:Avatar 进入 World 触发区

```
Avatar(挂载 VRCContactReceiver collisionTags=["WorldTrigger"])
  ↓ 进入
World Object(挂载 VRCContactSender collisionTags=["WorldTrigger"])
  ↓ 触发
World UdonBehaviour.OnContactEnter(info)
  → 业务逻辑:开门/给积分/触发剧情
```

### 场景:World 物体接触 Avatar 身体部位

```
World Object(VRCContactSender collisionTags=["Head","Hand"])
  ↓ 接触
Avatar(VRCContactReceiver collisionTags=["Head","Hand"])
  ↓ 触发
Avatar Animator Parameter("IsTouched", true)
  → FX Layer 播放触碰反应动画
```

---

## 性能基准(来自 `avatar/performance-benchmarks.md`)

| 配置 | 每 1000 个 Contacts 的帧时间 |
|------|------------------------------|
| 关闭状态 | **0.5 ms** |
| 开启 Receivers | **0.75 ms**(+50%) |
| 本地 Avatar 参数 | **+1.5 ms** 每 1000 个 |

**房间最大上限**: 4096 个 Contacts(超出部分停止工作)。

### 优化建议

- **形状选小**: Sphere > Capsule > Cube(碰撞检测成本递增)
- **类型选少**: 同 Receiver 的多 Sender 共享 type,减少配对计算
- **碰撞标签精确**: 避免"接受所有标签"的 Receiver(性能 + 行为双损)
- **本地 Avatar 参数**: 仅在需要本地反应时启用

---

## 房间限制(World 端)

来自 `world/scene-components/index.md`:

> **FACT** (验证于 2025-03-07): 当前加载的 World 中:
> - **PhysBone 限制**: 1024 个 active 的 PhysBone + PhysBone Collider
> - **Contact 限制**: 1024 个 active 的 Contact Sender + Contact Receiver
>
> 超过上限的组件将被禁用,直到现有组件被禁用或销毁。
> SDK 会显示警告,但只要在运行时不超过 1024 个,警告可忽略。

> ⚠️ **1024 限制是世界运行时**,而 4096 是 SDK 编译/统计上限,二者不冲突。

---

## Debug View 7: PhysBone & Contact Overlay

来自 `world/udon/world-debug-views.md`:

> Debug View 7 高亮世界中**附近的 PhysBones 和 Contacts**。
> 用途:调试 PhysBone / Contact 组件行为不符合预期时。

启用方式: 在 World 中按 `F1` → 选 Debug View 7(需 ClientSim / World 已加载)。

---

## SDK 版本要求

| API | 最低 SDK |
|-----|----------|
| World `OnContactEnter` | **3.10.0+** |
| World `VRCContactSender` / `VRCContactReceiver` | **3.10.0+** |
| Avatar 公开 Contact API | **2026.2.1 build+** |

> ⚠️ 旧 SDK(< 3.10.0)编译通过但**运行时静默忽略** Contact 事件。始终检查 `#if UDONSHARP` 或 SDK 版本条件。

---

## 实战模式

### 模式 1:门控触发(Avatar 进区域开门)

```csharp
// 挂在门附近空 GameObject 上的 Udon
public override void OnContactEnter(ContactReceiverInfo info) {
    if (info.isAvatar && info.player != null && info.player.isLocal) {
        // 只对本地玩家开门
        SendCustomNetworkEvent(NetworkEventTarget.All, nameof(OpenDoor));
    }
}
```

### 模式 2:Avatar 端反应(被 World 物体触碰时)

```
Avatar 上 VRCContactReceiver(collisionTags=["Fire"], onEnter=SetBool "IsOnFire"=true)
  → FX Layer: Transition "OnFire" → "Burn" 状态
  → 播放火焰动画 + Particle System
```

### 模式 3:多玩家协同(碰撞点 + 玩家归属)

```csharp
public override void OnContactEnter(ContactReceiverInfo info) {
    if (!info.isAvatar || info.player == null) return;

    // 记录被谁触碰
    _lastTouchedPlayerId = info.player.playerId;
    _lastTouchedPosition = info.contactPoint;

    // 同步给所有人(Manual Sync 模式)
    RequestSerialization();
}
```

---

## 与 PhysBone 的关系

| 维度 | Contact | PhysBone |
|------|---------|----------|
| 用途 | 接触检测(瞬时/持续) | 骨骼模拟(链式摆动) |
| 数据类型 | 触发事件 + 玩家信息 | 骨骼 transform + grab/release 事件 |
| 性能特征 | O(n) 形状检测 | O(链长) 弹簧模拟 |
| 配合使用 | 常见:Avatar 触发的 PhysBone 拉拽 | — |

> **最佳实践**: Avatar 全身 PhysBone + 关键部位 Contact(头/手/脚),配合 FX Layer 反馈。

---

## 已知坑

1. **onStay 每帧触发** — 不要在里面做重活(网络同步、复杂逻辑),仅做轻量更新
2. **collisionTags 区分大小写** — `"Head"` ≠ `"head"`
3. **isAvatar 不等于 isLocal** — World 物体碰撞也会 isAvatar=false;需双重判断
4. **player 可能为 null** — Sender 在某些边界情况(null Sender / delayed join)下 player 为 null,需做空检查
5. **脱离范围不立即触发 onExit** — 物理引擎有脱节延迟,关键状态用 polling 而非事件

---

## 相关文档

- **World Dynamics API**:`memory/api/dynamics.md`(SDK 3.10.0+ 完整说明)
- **PhysBone 限制**:`memory/avatar/avatar-dynamic-bone-limits.md`
- **Avatar 性能基准**:`memory/avatar/performance-benchmarks.md`
- **Quest 兼容性**:`memory/rules/quest-constraints.md`
- **lilToon 接触功能(Shader 端)**:`memory/avatar/shader/liltoon/fur.md`
