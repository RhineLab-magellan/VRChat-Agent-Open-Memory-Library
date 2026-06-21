# Player Positions — 玩家位置/旋转/追踪/速度/传送

> Domain: World / Udon / Players
> Subtype: API 详解
> Source: https://creators.vrchat.com/worlds/udon/players/player-positions (Last updated: 2024-12-13)
> 底层引用: `memory/api/player-api.md`
> 抓取日期: 2026-06-15

---

## 概述

玩家的**位置、旋转、速度**均可通过 Udon 访问和修改。**所有**以下节点都需要 `VRCPlayerApi` 作为输入。

与力相关的 API 见 [player-forces.md](./player-forces.md)。

---

## 位置与旋转 API

### GetPosition

- **返回**: `Vector3` (世界空间)
- **说明**: 获取玩家位置

```csharp
Vector3 pos = player.GetPosition();
```

### GetRotation

- **返回**: `Quaternion` (世界空间)
- **说明**: 获取玩家旋转

```csharp
Quaternion rot = player.GetRotation();
```

> 📝 **替代方案**: 若需要"玩家大致朝向"(尤其是全身追踪玩家),考虑用 `GetRotation` 而非 `GetTrackingData(AvatarRoot).rotation`,因为后者在全身追踪时不会随头部方向旋转。

---

## 骨骼 API

### GetBonePosition

- **输入**: `HumanBodyBones` 枚举值
- **返回**: `Vector3` (世界空间) 或 `Vector3.Zero (0,0,0)` (骨骼不存在)
- **说明**: 获取玩家 Avatar 指定骨骼的位置
- **警告** ⚠️:
  - **不同 Avatar 骨骼位置可能差异极大**
  - **不要**基于骨骼位置假设玩家身高、姿态等
  - 不同 Avatar 的"Head"骨骼不一定在预期位置

### GetBoneRotation

- **返回**: `Quaternion` (世界空间) 或 `Quaternion.Identity` (骨骼不存在)
- **说明**: 获取玩家 Avatar 指定骨骼的旋转
- **警告** ⚠️: 同 `GetBonePosition`,骨骼位置不可强假设

---

## 追踪数据 API (推荐方式)

### GetTrackingData

- **输入**: `TrackingDataType` 枚举
- **返回**: `TrackingData` 结构体(含 `position` 和 `rotation`)
- **说明**: **官方推荐**获取玩家头部和手部位置/旋转的方式

#### `TrackingDataType` 枚举值

| 值 | 说明 |
|---|---|
| `Head` | 玩家头部 |
| `LeftHand` | 玩家左手 |
| `RightHand` | 玩家右手 |
| `Origin` | **本地 VR 用户**的 playspace 中心;**本地桌面用户**的玩家位置;**所有远程用户**的玩家位置 |
| `AvatarRoot` | Avatar 根 Transform (与玩家胶囊体附着的同一 Transform) |

#### 关键差异

- **本地玩家**: 数据来自 **TrackingManager** (即直接来自头显/追踪器)
- **远程玩家**: 数据来自 Avatar 的 **RightHand / LeftHand / Head 骨骼**
- **全身追踪注意** ⚠️: `AvatarRoot` 在全身追踪(Full-Body Tracking)用户中**不会**随头部朝向旋转
  - 需要"玩家大致朝向"时,**用 `GetRotation` 替代 `GetTrackingData(AvatarRoot).rotation`**

```csharp
TrackingData headData = player.GetTrackingData(VRCPlayerApi.TrackingDataType.Head);
Vector3 headPos = headData.position;
Quaternion headRot = headData.rotation;
```

---

## 速度 API

### GetVelocity

- **返回**: `Vector3` (世界空间,速度向量)
- **说明**: 获取玩家**当前移动速度**(大小 + 方向)

```csharp
Vector3 vel = player.GetVelocity();
float speed = vel.magnitude;
```

### SetVelocity

- **输入**: `Vector3` (世界空间)
- **说明**: **设置**玩家移动速度
- **副作用** ⚠️: 在本地玩家上调用时,其 `IsPlayerGrounded` 被设为 `false` (因为他们不再"直接控制"自己的移动)

```csharp
// 弹起玩家
player.SetVelocity(new Vector3(0, 5f, 0));
```

> 📝 **与 player-forces.md 的关系**: 任务规格中 `velocity` API 在新文档中归类在本文件。

---

## 接地检测 API

### IsPlayerGrounded

- **返回**: `bool IsPlayerGrounded`
- **说明**: 获取玩家是否**接触地面**(决定是否可跳跃)
- **使用**: 与 `SetVelocity` 配合时自动变 false

```csharp
if (player.IsPlayerGrounded())
{
    // 玩家在地面上,可以跳跃
    player.SetJumpImpulse(5f);
}
```

---

## 传送 API

### TeleportTo

将**本地玩家**传送到新位置和指定旋转(除非 Station 不允许)。

- **签名**: `TeleportTo(Vector3 teleportPos, Quaternion teleportRot, ...)`
- **输入**:
  | 参数 | 类型 | 必填 | 说明 |
  |---|---|---|---|
  | `teleportPos` | `Vector3` | ✅ | 目标位置(世界空间) |
  | `teleportRot` | `Quaternion` | ✅ | 目标旋转(世界空间) |
  | `TeleportOrientation` | `SceneDescriptorSpawnOrientation` | ❌ | 玩家与目标位置/旋转的对齐方式 |
  | `lerpOnRemote` | `bool` | ❌ | 是否为远程玩家插值(默认 `false`) |

#### 关键约束

| 约束 | 说明 |
|---|---|
| **仅本地玩家** | ⚠️ Udon 只能传送本地玩家。要让其他玩家传送,使用 [Networking](../networking/) 让他们**自行**传送 |
| **Station 阻止** | Stations 可以阻止 Udon 传送玩家 |
| **高频传送** | 高频/短距离传送时,考虑设置 `lerpOnRemote = false` |

#### `lerpOnRemote` 行为对比

| 值 | 远程玩家视角 | 带宽成本 |
|---|---|---|
| `false` (默认) | 瞬移(看起来突兀) | 较高(每次传送都是一次 sync) |
| `true` | 平滑过渡(像正常移动) | 较低(被当作普通移动) |

#### ⚠️ 重要警告: 不要在网络更新中传送

> **不要在网络更新期间传送玩家**(如 [OnDeserialization](../networking/network-components/#ondeserialization))。否则玩家的 Avatar 可能在传送过程中意外与环境碰撞。
>
> 正确做法: 使用 [SendCustomEventDelayedFrames](https://creators.vrchat.com/worlds/udon/graph/special-nodes/#sendcustomeventdelayedframes) **延迟一帧**再传送。

```csharp
// 错误: 在 OnDeserialization 中直接传送
public override void OnDeserialization()
{
    player.TeleportTo(pos, rot); // ⚠️ 可能导致碰撞异常
}

// 正确: 延迟一帧
public override void OnDeserialization()
{
    SendCustomEventDelayedFrames(nameof(DelayedTeleport), 1);
}

public void DelayedTeleport()
{
    player.TeleportTo(teleportPos, teleportRot, 
        VRC_SceneDescriptor.SpawnOrientation.AlignPlayerWithSpawnPoint,
        false);
}
```

---

## 典型场景配方

### 1. 玩家接近 NPC 触发对话

```csharp
public override void OnPlayerTriggerEnter(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        // 面向 NPC
        Vector3 npcForward = npcTransform.forward;
        Quaternion lookAt = Quaternion.LookRotation(-npcForward); // 背对 NPC
        
        // 平滑传送并对齐
        player.TeleportTo(
            player.GetPosition(),
            lookAt,
            VRC_SceneDescriptor.SpawnOrientation.AlignPlayerWithSpawnPoint,
            true // 平滑过渡
        );
    }
}
```

### 2. 弹跳垫 — 物理弹起

```csharp
public override void OnPlayerTriggerEnter(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        // 弹起 8 米/秒
        player.SetVelocity(new Vector3(0, 8f, 0));
    }
}
```

### 3. HUD 跟随玩家头部

```csharp
private void Update()
{
    if (player == null || !Utilities.IsValid(player)) return;
    
    TrackingData headData = player.GetTrackingData(VRCPlayerApi.TrackingDataType.Head);
    hudTransform.position = headData.position + headData.rotation * Vector3.forward * 0.5f;
    hudTransform.rotation = headData.rotation;
}
```

### 4. 全身追踪玩家朝向

```csharp
private void Update()
{
    if (player == null || !Utilities.IsValid(player)) return;
    
    // 用 GetRotation 而非 AvatarRoot,因为 FBT 用户 AvatarRoot 不旋转
    Quaternion playerFacing = player.GetRotation();
    npcIndicator.rotation = playerFacing;
}
```

### 5. 跨实例玩家位置恢复

```csharp
// 加载持久化位置
public void RestorePosition()
{
    Vector3 savedPos = LoadPersistedPosition();
    Quaternion savedRot = LoadPersistedRotation();
    
    // 延迟一帧,避免在网络更新中传送
    SendCustomEventDelayedFrames(nameof(DelayedRestore), 1);
}

public void DelayedRestore()
{
    Networking.LocalPlayer.TeleportTo(savedPos, savedRot, 
        VRC_SceneDescriptor.SpawnOrientation.Default,
        true);
}
```

---

## 与任务规格的差异说明

> ⚠️ **任务提示与当前官方 API 存在以下差异**:
>
> | 任务提示 | 当前官方 API | 位置 |
> |---|---|---|
> | `GetPosition` | ✅ 一致 | 本文件 |
> | `GetRotation` | ✅ 一致 | 本文件 |
> | `IsPlayerGrounded` | ✅ 一致 | 本文件 |
> | `GetPlayerHeight` | ❌ 当前文档**未列出** | 旧 API,可能已弃用 |
> | `GetPlayerEyeHeightAsMeters` | ✅ 仍存在(但归类在 player-avatar-scaling.md) | player-avatar-scaling.md |
> | `GetTrackingData` | ✅ 一致 | 本文件 |
> | `GetBonePosition` | ✅ 存在(替代 `GetPlayerHeight`) | 本文件 |

---

## 与底层 API 的对照

| 本文件 API | 底层 `player-api.md` 摘要 |
|---|---|
| `GetPosition` | ✅ 有 |
| `GetRotation` | ❌ 底层未列出 |
| `GetTrackingData` | ✅ 有 |
| `TeleportTo` | ✅ 有 |
| `GetVelocity` / `SetVelocity` | ❌ 底层未列出 |
| `IsPlayerGrounded` | ❌ 底层未列出 |
| `GetBonePosition` / `GetBoneRotation` | ❌ 底层未列出 |

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **传送时机** | ⚠️ 不要在 `OnDeserialization` 中传送,延迟一帧 |
| **骨骼假设** | 不同 Avatar 骨骼位置差异极大,不能基于 Head 骨骼位置假设玩家身高 |
| **FBT 与 AvatarRoot** | 全身追踪用户的 `AvatarRoot` 不随头部旋转,需用 `GetRotation` 替代 |
| **GetBonePosition 返回 Zero** | 骨骼不存在时返回 `Vector3.Zero`,可能误判为"在原点" |
| **远程玩家追踪数据** | 来自 Avatar 骨骼,不是真实头显数据,延迟更高 |
| **高频读取** | `GetTrackingData` 在 `Update` 中调用有跨 VM 成本(底层文档已标注) |
| **SetVelocity 影响 Grounded** | 调用后 `IsPlayerGrounded` 自动变 false,可能误判 |

---

## 性能优化

| 优化 | 说明 |
|---|---|
| **缓存常用引用** | 玩家引用、Transform 在 `Start` 中缓存 |
| **避免每帧 GetTrackingData** | 非必要时改用 `Transform` 缓存(本地玩家可缓存 `Camera.main`) |
| **预分配数组** | 多玩家操作时配合 `VRCPlayerApi[]` 缓存 |
| **延迟帧** | 传送等副作用操作延迟 1 帧,避免与网络更新冲突 |

---

## 与其他知识库的关系

| 知识库 | 关系 |
|---|---|
| `memory/api/player-api.md` | 底层 API 简略版 |
| `memory/world/udon/players/player-forces.md` | 移动/速度/力相关 |
| `memory/world/udon/players/player-avatar-scaling.md` | `GetPlayerEyeHeightAsMeters` |
| `memory/world/udon/networking/` | 网络更新事件、传送同步 |
| `memory/world/udon/networking/network-components.md` | `OnDeserialization` 注意事项 |
