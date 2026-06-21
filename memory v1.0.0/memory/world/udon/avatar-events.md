# Avatar Events - 玩家 Avatar 变更事件

> 来源: https://creators.vrchat.com/worlds/udon/avatar-events
> 抓取日期: 2026-06-15
> 状态: ✅ FACT (官方文档)
> 关联: `memory/api/events-reference.md`

---

## 概述

**Avatar Events** 允许 Udon **响应玩家 Avatar 相关的变化**。这是处理 "玩家换 Avatar" 场景的**唯一官方机制**。

---

## 事件 1: `OnAvatarChanged`

### 签名

```csharp
public override void OnAvatarChanged(VRCPlayerApi player)
```

### 触发时机

> **官方定义**: "Called when a player's avatar has finished loading."
> 玩家 Avatar **加载完成**时触发。

### 参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `player` | `VRCPlayerApi` | 触发事件的玩家 |

### 关键行为

| 玩家 | 行为 |
|---|---|
| **本地玩家** | `player.GetEyeHeightAsMeters()` 返回 **Prefab 高度**(非 Eye Height 缩放后) |
| **远程玩家** | 远程玩家可能**还未同步新的 Eye Height**,**不可依赖返回的 Eye Height 值** |

### 使用场景

```csharp
public override void OnAvatarChanged(VRCPlayerApi player)
{
    if (player == Networking.LocalPlayer)
    {
        // 本地 Avatar 加载完成,执行初始化
        AdjustCameraPosition();
    }
    // 注意: 远程玩家时不要依赖 eye height
}
```

---

## 事件 2: `OnAvatarEyeHeightChanged`

### 签名

```csharp
public override void OnAvatarEyeHeightChanged(VRCPlayerApi player, float previousEyeHeight)
```

### 触发时机

> **官方定义**: "Called when a player has their eye height change via switching to another avatar or via the avatar scaling system."
> 玩家切换 Avatar 或使用 [Avatar Scaling](/worlds/udon/players/player-avatar-scaling) 系统导致 **Eye Height 变化**时触发。

### 参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `player` | `VRCPlayerApi` | 触发事件的玩家 |
| `previousEyeHeight` | `float` | **先前**的 Eye Height(米) |

### 🔴 关键时序约束

> **首次 Avatar 加载**:本地或远程玩家**首次加入世界**时,`previousEyeHeight` 可能是 **0**。这表示"无先前的 Eye Height"。

#### 本地玩家(LOCAL)

- 玩家**更换 Avatar** 并应用了 **persisted eye height**(保存的 Eye Height 与 Prefab 不同)
- **此事件仅会为 persisted height 触发一次**

#### 远程玩家(REMOTE) — ⚠️ 多次触发!

- 远程玩家更换 Avatar 并应用 persisted eye height
- **此事件可能触发多次**(每次新 Eye Height 同步给你时)

> **重要时序**:
> - 对于**远程玩家**,你可能**先**收到 `OnAvatarEyeHeightChanged`,**后**收到 `OnAvatarChanged`
> - 但**不会**收到**乱序**的 `OnAvatarEyeHeightChanged`

### 使用场景

```csharp
public override void OnAvatarEyeHeightChanged(VRCPlayerApi player, float previousEyeHeight)
{
    // 玩家 Eye Height 变化,可能需要:
    // 1. 调整相机位置
    // 2. 更新 UI 锚点
    // 3. 重新计算 NPC 互动距离

    if (previousEyeHeight == 0f)
    {
        // 首次加入,previousEyeHeight = 0 是正常情况
        return;
    }

    if (player == Networking.LocalPlayer)
    {
        // 本地玩家持久化 Eye Height 变化
    }
    else
    {
        // 远程玩家 - 每次收到新 Eye Height 都会触发
    }
}
```

---

## 事件执行时序总结

### 玩家加入世界

```
玩家加入
  → 首次 Avatar 加载
  → OnAvatarChanged(本地/远程均触发)
  → OnAvatarEyeHeightChanged(previousEyeHeight = 0)
```

### 本地玩家更换 Avatar(有 Persisted Eye Height)

```
玩家换 Avatar
  → OnAvatarChanged(本地)
  → OnAvatarEyeHeightChanged(localPlayer, previousHeight)
    (仅触发一次,使用 persisted height)
```

### 远程玩家更换 Avatar(有 Persisted Eye Height)

```
远程玩家换 Avatar
  → 可能触发多次:
    OnAvatarEyeHeightChanged(remotePlayer, height1)  // 第 1 次同步
    OnAvatarEyeHeightChanged(remotePlayer, height2)  // 第 2 次同步(若同步多次)
  → 最终: OnAvatarChanged(remotePlayer)
```

---

## 与其他事件的关系

| 事件 | 时机 | 关系 |
|---|---|---|
| `OnPlayerJoined` | 玩家进入实例 | **早于** OnAvatarChanged |
| `OnAvatarChanged` | Avatar 加载完成 | **晚于** OnPlayerJoined |
| `OnAvatarEyeHeightChanged` | Eye Height 变化 | 顺序**不固定**于 OnAvatarChanged |
| `OnPlayerLeft` | 玩家离开 | **不影响** Avatar 事件 |

> 详细事件执行顺序: `memory/world/udon/event-execution-order.md` ⭐ **关键文档**

---

## 持久化 Eye Height 行为

> **机制**: VRChat 会同步玩家 **Eye Height 相对 Prefab 高度的偏差**

```
Avatar Prefab Height = 1.5m
玩家 Persisted Eye Height = 1.7m  (向上缩放 0.2m)
  → 同步到所有客户端: variance = +0.2m
  → 其他客户端 OnAvatarEyeHeightChanged 收到 +0.2m
```

> 详细 Avatar Scaling 系统: `memory/world/udon/players/player-avatar-scaling.md`

---

## 风险与陷阱

| 风险 | 等级 | 说明 |
|---|---|---|
| 远程玩家 Eye Height 依赖 | 🔴 严重 | **绝对不要** 在 `OnAvatarChanged` 中读远程玩家的 Eye Height |
| 多次 OnAvatarEyeHeightChanged | 🟡 中等 | 远程玩家可能**多次**触发,需幂等处理 |
| `previousEyeHeight = 0` 误判 | 🟡 中等 | 首次加入时=0,不是错误 |
| 事件时序假设 | 🟡 中等 | 不要假设 OnAvatarChanged 一定先于 OnAvatarEyeHeightChanged |
| `OnAvatarChanged` 中的同步变量访问 | 🟢 低 | 同步变量可能还未对所有玩家同步 |

---

## 工程最佳实践

### 1. 防御性读取 Eye Height

```csharp
public override void OnAvatarChanged(VRCPlayerApi player)
{
    if (player == Networking.LocalPlayer)
    {
        // 本地: 安全
        float eyeHeight = player.GetEyeHeightAsMeters();
        AdjustCamera(eyeHeight);
    }
    // 远程: 不要读 eye height
}
```

### 2. 使用 SetProgramVariable 而非公共变量

```csharp
public override void OnAvatarChanged(VRCPlayerApi player)
{
    // 用 SetProgramVariable 避免暴露公开字段
    targetSystem.SetProgramVariable("playerAvatarReady", true);
}
```

### 3. 幂等处理多次触发

```csharp
private VRCPlayerApi[] _processedPlayers = new VRCPlayerApi[80];

public override void OnAvatarEyeHeightChanged(VRCPlayerApi player, float previousEyeHeight)
{
    // 检查是否已处理过
    if (WasProcessed(player)) return;
    MarkProcessed(player);
    // ... 业务逻辑
}
```

---

## 与知识库互补

- **Udon 事件完整参考**: `memory/api/events-reference.md` ⭐
- **事件执行顺序**: `memory/world/udon/event-execution-order.md` ⭐ 关键时序
- **Player API**: `memory/api/player-api.md` ⭐
- **Player Avatar Scaling**: `memory/world/udon/players/player-avatar-scaling.md` ⭐

---

## 相关 VRChat 官方文档

- [Avatar Events](/worlds/udon/avatar-events)
- [Player Avatar Scaling](/worlds/udon/players/player-avatar-scaling)
