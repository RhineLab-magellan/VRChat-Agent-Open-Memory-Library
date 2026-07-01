---
title: "Player Forces — 玩家移动力 / 速度 / 重力"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/udon/players/player-forces/ (Last updated: 2024-05-08)"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - udonsharp
aliases:
  - "Player Forces — 玩家移动力 / 速度 / 重力"
  - player-forces
related:
  - player-positions.md
  - player-collisions.md
  - getting-players.md
  - player-audio.md
  - player-avatar-scaling.md
---
# Player Forces — 玩家移动力 / 速度 / 重力

> Subtype: API 详解
> 底层引用: `memory/api/player-api.md`
> 抓取日期: 2026-06-15

---

## 概述

本文档涵盖**作用于玩家的力/速度相关**的 API,包括移动速度、跳跃、重力、Immobilize。

> ⚠️ **Local player only**: 以下函数**仅对本地玩家**有效,不能在其他玩家的 `VRCPlayerApi` 上调用。

与位置相关的 API 见 [player-positions.md](./player-positions.md)。

---

## 移动速度 API

### GetWalkSpeed / SetWalkSpeed

- **类型**: `float`
- **工作范围**: `0 - 5`
- **默认**: 2
- **说明**: 玩家**行走**速度
- **建议**: 设置**低于** Run Speed

### GetRunSpeed / SetRunSpeed

- **类型**: `float`
- **工作范围**: `0 - 10`
- **默认**: 4
- **说明**: 玩家**奔跑**速度
- **建议**: 设置**高于** Walk Speed

### GetStrafeSpeed / SetStrafeSpeed

- **类型**: `float`
- **工作范围**: `0 - 5`
- **默认**: 2
- **说明**: 玩家**横向移动**速度
- **建议**: 与 Walk Speed 设置**相同**
- **关键**: ⚠️ **不受奔跑加速影响**

---

## 跳跃与重力 API

### GetJumpImpulse / SetJumpImpulse

- **类型**: `float`
- **工作范围**: `0 - 10`
- **默认**: 0
- **说明**: 玩家**跳跃时施加的力**
- **关键**: 默认是 0,意味着默认无跳跃能力
- **VRCWorld Prefab 默认**: 设置为 3
- **使用**: 如果世界需要跳跃,**必须**显式设置此值

### GetGravityStrength / SetGravityStrength

- **类型**: `float`
- **工作范围**: `0 - 10`
- **默认**: 1
- **说明**: 世界**重力**倍率(1 = 地球重力)
- **关键** ⚠️:
  - **不要**直接修改 Unity 的 `Physics.Gravity` (会污染项目设置)
  - **使用** 此 Udon API 调整世界内重力
  - 这是一个**倍数**,值越大重力越强
- **应用场景**: 低重力太空世界、高重力行星世界、月球 (0.166)

---

## Immobilize API

### Immobilize

- **类型**: `Boolean` 属性
- **设置**: `true` 让玩家**钉在原地**
- **效果**:
  - 关闭玩家的 Locomotion (移动系统)
  - Avatar 保持在原位
  - ⚠️ **VR 玩家仍可能小范围转动视角** (head rotation),但 Avatar 不会移动

#### 与 `velocity` 的关系

任务提示中提到的 `velocity` (即 `SetVelocity`) 在当前文档中归类在 [player-positions.md](./player-positions.md) 中,详见该文件。

#### 与 `immobile` 的命名差异

任务提示中的 `immobile` → 当前官方 API 名称为 **`Immobilize`** (动词形式),见下方代码。

```csharp
// 钉住本地玩家
localPlayer.Immobilize = true;

// 解除
localPlayer.Immobilize = false;
```

---

## 典型场景配方

### 1. 进入战斗区域提升移动

```csharp
public override void OnPlayerTriggerEnter(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        player.SetRunSpeed(8f);    // 8 米/秒
        player.SetWalkSpeed(4f);   // 4 米/秒
        player.SetJumpImpulse(5f); // 强跳跃
    }
}

public override void OnPlayerTriggerExit(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        // 恢复默认
        player.SetRunSpeed(4f);
        player.SetWalkSpeed(2f);
        player.SetJumpImpulse(3f);
    }
}
```

### 2. 月球世界 — 低重力

```csharp
public override void OnPlayerJoined(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        player.SetGravityStrength(0.166f); // 月球重力
        player.SetJumpImpulse(8f);          // 跳跃力增大
    }
}
```

### 3. 监狱牢房 — Immobilize

```csharp
public void LockInCell(VRCPlayerApi player)
{
    player.Immobilize = true;
}

public void ReleaseFromCell(VRCPlayerApi player)
{
    player.Immobilize = false;
}
```

### 4. 商店对话 — 锁定移动但允许视角

```csharp
public void StartShopDialog(VRCPlayerApi player)
{
    // 钉住玩家,但 VR 玩家仍可转动头部看店主
    player.Immobilize = true;
    // 玩家仍可通过 `OnPlayerTriggerStay` 等事件接收数据
}
```

---

## 与任务规格的差异说明

> ⚠️ **任务提示与当前官方 API 存在以下差异**:
>
> | 任务提示 | 当前官方 API | 说明 |
> |---|---|---|
> | `ApplyPlayerForce(Vector3)` | **已移除/不可用** | 当前 Creator Docs **不再列出**此 API |
> | `velocity` (设置速度) | `SetVelocity(Vector3)` | 归类在 player-positions.md |
> | `immobile` | `Immobilize` (属性) | 命名差异(动词化) |
> | `UseAttachedStation` | (在 index.md) | 不属于本文件 |
> | `IsPlayerGrounded()` | (在 player-positions.md) | 归类在 player-positions.md |
>
> **结论**: `ApplyPlayerForce` 在当前 SDK 已被移除,取而代之的是更细粒度的 `SetWalkSpeed` / `SetRunSpeed` / `SetJumpImpulse` / `SetGravityStrength` / `Immobilize` 组合。如需一次性施加力,可用 `SetVelocity`(见 player-positions.md)。

---

## 与底层 API 的对照

| 本文件 API | 底层 `player-api.md` 摘要 |
|---|---|
| `SetWalkSpeed` / `SetRunSpeed` | ❌ 底层未列出(本文件为主要权威来源) |
| `SetJumpImpulse` | ❌ 底层未列出(本文件为主要权威来源) |
| `SetGravityStrength` | ❌ 底层未列出(本文件为主要权威来源) |
| `Immobilize` | ❌ 底层未列出(本文件为主要权威来源) |
| `SetVelocity` | (在 player-positions.md) |
| `IsPlayerGrounded` | (在 player-positions.md) |
| `UseAttachedStation` | (在 index.md) |

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **Local Player Only** | 所有 Set* 函数仅本地玩家有效,远程玩家调用无效 |
| **Immobilize 持续性** | 设置后持续到玩家离开或被重置,**不会**自动恢复 |
| **VR 视角限制** | Immobilize 不能阻止 VR 玩家转动头部 |
| **物理修改禁忌** | ⚠️ 不要改 `Physics.Gravity`,用 `SetGravityStrength` |
| **极端值警告** | 速度 0 可能让玩家无法移动,负值/极大值行为未定义 |
| **Quest 性能** | 频繁 SetSpeed 调用无性能问题,但避免每帧无意义调用 |
| **跳跃不重力** | 设置 `JumpImpulse = 0` 不代表无重力,玩家仍会下落 |

---

## 与其他知识库的关系

| 知识库 | 关系 |
|---|---|
| `memory/api/player-api.md` | 底层 API 简略版 |
| `memory/world/udon/players/player-positions.md` | 位置、速度、传送 API |
| `memory/world/udon/players/index.md` | `UseAttachedStation` |
| `memory/world/udon/networking/` | 移动参数变化是否需要同步 |
