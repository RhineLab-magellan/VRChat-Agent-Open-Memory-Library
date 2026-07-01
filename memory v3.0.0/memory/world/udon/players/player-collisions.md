---
title: "Player Collisions — 玩家碰撞检测"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/udon/players/player-collisions/ (Last updated: 2025-04-09)"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - udonsharp
aliases:
  - "Player Collisions — 玩家碰撞检测"
  - player-collisions
related:
  - player-forces.md
  - getting-players.md
  - player-audio.md
  - player-avatar-scaling.md
  - player-positions.md
---
# Player Collisions — 玩家碰撞检测

> Subtype: API 详解
> 底层引用: `memory/api/player-api.md`
> 抓取日期: 2026-06-15

---

## 概述

Udon 提供**三种方式**检测 Player 与 Object 的碰撞:
1. **Triggers** — 区域进入/离开/停留检测
2. **Physics** — 物理对象碰撞
3. **Particles** — 粒子与玩家碰撞

> 📚 **官方推荐**: 完整示例见 [Udon Example Scene](https://creators.vrchat.com/worlds/examples/udon-example-scene/)。

---

## 1. Triggers (触发器)

适用场景: 检测玩家**进入/离开某个区域**。

### 三个事件

| 事件 | 触发时机 |
|---|---|
| `OnPlayerTriggerEnter(VRCPlayerApi player)` | 玩家胶囊体**进入** Trigger Collider |
| `OnPlayerTriggerStay(VRCPlayerApi player)` | 玩家胶囊体**停留**在 Trigger Collider 内(每帧) |
| `OnPlayerTriggerExit(VRCPlayerApi player)` | 玩家胶囊体**离开** Trigger Collider |

### 配置方法

在 GameObject 上添加 Collider 组件 → 勾选 **`Is Trigger`** 复选框 → 同一 GameObject 添加 UdonBehaviour。

> 📚 **Unity 参考**: [Collision](https://docs.unity3d.com/2022.3/Documentation/Manual/CollidersOverview.html) | [Collider Shapes](https://docs.unity3d.com/Manual/collider-shapes-introduction.html)

### ⚠️ 边缘情况 (Edge Cases)

以下情况可能导致事件被跳过:
- 玩家**传送**进出 collider
- 玩家移动**极快**

设计逻辑时需考虑这些场景,避免依赖"必然会触发 TriggerEnter"。

---

## 2. Physics (物理碰撞)

适用场景: **移动的物理对象**(弹球、子弹等)与玩家碰撞。这些对象 Collider 的 `IsTrigger = false`。

### 三个事件 + 一个特殊事件

| 事件 | 触发时机 |
|---|---|
| `OnPlayerCollisionEnter(VRCPlayerApi player)` | 玩家胶囊体**进入** Collider |
| `OnPlayerCollisionStay(VRCPlayerApi player)` | 玩家胶囊体**停留**在 Collider 内(每帧) |
| `OnPlayerCollisionExit(VRCPlayerApi player)` | 玩家胶囊体**离开** Collider |
| `OnControllerColliderHitPlayer()` | **CharacterController** 击中玩家 |

### ⚠️ 关键约束: 物理碰撞事件仅对移动对象触发

> **`OnPlayerCollision*` 事件在玩家"走入"静止物体时**不会**触发**。
>
> 如果需要处理"玩家撞静止物体"的场景,**使用 Trigger Collider**,不要用物理碰撞。

```csharp
// 错误: 玩家走入静止物体不会触发
public override void OnPlayerCollisionEnter(VRCPlayerApi player)
{
    // 玩家走入一面墙 → 这个事件**不会**被调用
}

// 正确: 用 Trigger 检测静止区域
public override void OnPlayerTriggerEnter(VRCPlayerApi player)
{
    // 玩家走入一个 Trigger 区域 → 这个事件**会**被调用
}
```

---

## 3. Particles (粒子碰撞)

### OnPlayerParticleCollision

- **事件**: `OnPlayerParticleCollision(VRCPlayerApi player)`
- **触发**: 玩家与 Particle 碰撞
- **前置条件** (在 Particle System 上):
  - ✅ Collision 模块**开启**
  - ✅ `Send Collision Messages` **开启**
  - ✅ Collision 模式: `World` + `3D`

---

## 性能敏感度对比

| 事件 | 性能开销 | 触发频率 |
|---|---|---|
| `OnPlayerTriggerEnter/Exit` | 🟢 低 | 离散事件(每玩家一次) |
| `OnPlayerCollisionEnter/Exit` | 🟢 低 | 离散事件(每玩家一次) |
| `OnPlayerTriggerStay` | 🔴 **高** | **每帧**每玩家触发 |
| `OnPlayerCollisionStay` | 🔴 **高** | **每帧**每玩家触发 |
| `OnPlayerParticleCollision` | 🟡 中 | 视粒子密度 |

> ⚠️ **Stay 事件是性能热点**:
> - 10 个玩家在 1 个 Trigger 区域内 → 10 次/帧 Stay 调用
> - 多区域 + 多玩家 → 指数级增长
> - 替代方案: 用 `OnPlayerTriggerEnter` 设置状态标志,避免在 `Stay` 中重复处理

---

## 典型场景配方

### 1. 进入区域播放音效

```csharp
public override void OnPlayerTriggerEnter(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        audioSource.Play();
        triggerLight.color = Color.green;
    }
}
```

### 2. 物理弹球击中玩家

```csharp
public override void OnPlayerCollisionEnter(VRCPlayerApi player)
{
    if (player == Networking.LocalPlayer)
    {
        // 玩家被弹球击中
        Debug.Log($"Hit by {gameObject.name}");
        player.SetVelocity(Vector3.up * 5f); // 弹起
    }
}
```

### 3. 粒子爆炸伤害检测

```csharp
public override void OnPlayerParticleCollision(VRCPlayerApi player)
{
    // 每个被粒子击中的玩家都触发
    DealDamage(player, 10);
}
```

### 4. 高效区域检测(避免 Stay 性能问题)

```csharp
private bool _isPlayerInZone;

public override void OnPlayerTriggerEnter(VRCPlayerApi player)
{
    if (player.isLocal) _isPlayerInZone = true;
}

public override void OnPlayerTriggerExit(VRCPlayerApi player)
{
    if (player.isLocal) _isPlayerInZone = false;
}

private void Update()
{
    // 使用 _isPlayerInZone 标志,避免 Stay 每帧触发开销
    if (_isPlayerInZone)
    {
        ApplySlowEffect();
    }
}
```

---

## 与底层 API 的对照

| 本文件 API | 底层 `player-api.md` 摘要 |
|---|---|
| `OnPlayerCollisionEnter/Exit/Stay` | 已列出 |
| `OnPlayerTriggerEnter/Exit/Stay` | (本文件为主要权威来源) |
| `OnPlayerParticleCollision` | (本文件为主要权威来源) |
| `OnControllerColliderHitPlayer` | (本文件为主要权威来源) |

> ⚠️ **底层文档错误案例**: "Player Collision 仅对移动物体有效" — 本文件已确认**仅对移动的物理对象**触发,静止物理对象需用 Trigger。

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **Stay 事件性能** | Stay 每帧每玩家触发,避免在其中做重活,用 Enter/Exit 设标志 |
| **物理碰撞误用** | 期望"玩家走入静止物体"却用 `OnPlayerCollision*` 是常见错误,改用 Trigger |
| **边缘情况** | 玩家传送/极快速移动可能跳过 Trigger 事件,设计时考虑重传逻辑 |
| **Collider 形状** | 复杂 Collider 性能更差,简单 Box/Sphere 优先 |
| **多 Trigger 嵌套** | 嵌套 Trigger 会产生额外 Enter/Exit 对,避免复杂嵌套 |
| **Particle 性能** | 大量粒子 + `Send Collision Messages` 在 Quest 上是性能灾难 |

---

## 调试与测试

```csharp
// 调试: 记录所有碰撞事件
public override void OnPlayerTriggerEnter(VRCPlayerApi player)
{
    Debug.Log($"[Trigger Enter] {player.displayName} (id={player.playerId})");
}

public override void OnPlayerTriggerExit(VRCPlayerApi player)
{
    Debug.Log($"[Trigger Exit] {player.displayName} (id={player.playerId})");
}
```

> 📚 **示例场景**: [Udon Example Scene](https://creators.vrchat.com/worlds/examples/udon-example-scene/) 演示了所有三种碰撞检测方式。

---

## 与其他知识库的关系

| 知识库 | 关系 |
|---|---|
| `memory/api/player-api.md` | 底层 API 简略版 |
| `memory/world/examples/udon-example-scene/` | 官方碰撞示例 |
| `memory/world/udon/networking/` | 碰撞 + 网络同步的相关注意事项 |
| `memory/world/performance-guide.md` | Trigger 性能优化 |
