---
title: "Drone Information — Drone 信息查询"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/udon/players/drones/drone-information/ (Last updated: 2026-03-20)"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - udonsharp
aliases:
  - "Drone Information — Drone 信息查询"
  - drone-information
related:
  - index.md
  - getting-drones.md
  - "../../ai-navigation.md"
  - "../../data-containers/byte-and-bit-operations.md"
  - "../../data-containers/data-dictionaries.md"
---
# Drone Information — Drone 信息查询

> Domain: World / Udon / Players / Drones
> Subtype: API 详解 — 状态/位置/旋转/速度/传送
> 父级索引: [`./index.md`](./index.md)
> 抓取日期: 2026-06-15

---

## 概述

`VRCDroneApi` 提供 10 个成员方法/属性,用于查询和操控 Drone 的状态、位置、旋转、速度,以及执行传送。

> 📌 **与 `VRCPlayerApi` 平行**: `VRCDroneApi` 的 API **命名约定与 `VRCPlayerApi` 几乎一致** (`GetPosition` / `GetRotation` / `GetVelocity` / `TeleportTo`),但 Drone 版本额外提供 `IsDeployed` 状态查询与 `Try*` 失败安全版本。

---

## API 总览

| 类别 | 方法 | 用途 |
|---|---|---|
| **Owner 查询** | `GetPlayer()` | 获取拥有此 Drone 的玩家 |
| **状态查询** | `IsDeployed()` | Drone 是否已部署到世界 |
| **位置** | `GetPosition()` | 当前位置(可能为零点) |
| **位置(安全)** | `TryGetPosition(out Vector3)` | 失败时返回 `false`,不修改参数 |
| **旋转** | `GetRotation()` | 当前旋转(可能为单位四元数) |
| **旋转(安全)** | `TryGetRotation(out Quaternion)` | 失败时返回 `false` |
| **速度** | `GetVelocity()` | 当前速度向量 |
| **速度(安全)** | `TryGetVelocity(out Vector3)` | 失败时返回 `false` |
| **传送** | `TeleportTo(position, rotation, smooth)` | 设置位置+旋转,可选平滑过渡 |
| **设速度** | `SetVelocity(velocity)` | 设置速度向量 |

---

## Owner 查询

### GetPlayer

- **签名**: `VRCPlayerApi GetPlayer()`
- **返回**: `VRCPlayerApi` (拥有此 Drone 的玩家)
- **说明**: 与 `VRCPlayerApi.GetDrone()` 互为反向
- **失效场景**: Player 离开实例 / Drone 被销毁 → 返回值失效,**必须** `Utilities.IsValid` 检查
- **见**: [`getting-drones.md`](./getting-drones.md) 章节,本节不再展开

---

## 状态查询

### IsDeployed

- **签名**: `bool IsDeployed()`
- **返回**:
  - `true` — Drone 已部署,`GetPosition/GetRotation/GetVelocity` 返回有效值
  - `false` — Drone **未部署**(玩家未启动 Drone 模式,或 Drone 模式在世界未启用)
- **典型用法** ⭐: 任何查询前先 `IsDeployed` 守护,避免拿到零值/单位值

```csharp
public override void OnDroneTriggerStay(VRCDroneApi drone)
{
    if (!drone.IsDeployed()) return;  // ⭐ 必须先检查

    Vector3 pos = drone.GetPosition();  // 现在一定是有效位置
    // ...
}
```

> 📌 **设计意图**: `IsDeployed` 是 Drone 专有,**`VRCPlayerApi` 没有对应方法**(玩家总在世界中)。

---

## 位置 (Position)

### GetPosition

- **签名**: `Vector3 GetPosition()`
- **返回**: Drone 的世界坐标位置
- **未部署时**: 行为未明确定义,**可能** 返回 `Vector3.zero` 或上次缓存值
- **推荐** ⭐: 配合 `IsDeployed()` 使用,或改用 `TryGetPosition` 拿明确成功标志

```csharp
if (drone.IsDeployed())
{
    Vector3 pos = drone.GetPosition();
    // 使用 pos
}
```

---

### TryGetPosition

- **签名**: `bool TryGetPosition(out Vector3 position)`
- **输入**: `out Vector3 position` (接收位置)
- **返回**:
  - `true` — 成功获取,`position` 是有效值
  - `false` — 失败(未部署/已销毁等),`position` 保持原值(不保证重置)
- **优势**: 比 `IsDeployed` + `GetPosition` 更安全、更显式

```csharp
Vector3 pos;
if (drone.TryGetPosition(out pos))
{
    // 成功
    Debug.Log($"Drone at {pos}");
}
else
{
    // 失败 — 安全降级
}
```

> 📌 **设计模式**: `Try*` 系列是 **.NET 标准模式** ,VRChat 在 Drone API 中引入,用于避免无效值的歧义。

---

## 旋转 (Rotation)

### GetRotation

- **签名**: `Quaternion GetRotation()`
- **返回**: Drone 的世界旋转
- **未部署时**: 可能返回 `Quaternion.identity`,需配合 `IsDeployed`

---

### TryGetRotation

- **签名**: `bool TryGetRotation(out Quaternion rotation)`
- **输入**: `out Quaternion rotation`
- **返回**: `bool` — 是否成功
- **用法**: 与 `TryGetPosition` 相同模式

```csharp
Quaternion rot;
if (drone.TryGetRotation(out rot))
{
    Vector3 forward = rot * Vector3.forward;
    // ...
}
```

---

## 速度 (Velocity)

### GetVelocity

- **签名**: `Vector3 GetVelocity()`
- **返回**: Drone 当前的 **速度向量**(含方向和大小,单位 m/s)
- **未部署时**: 行为未明确定义,可能返回 `Vector3.zero`

```csharp
if (drone.IsDeployed())
{
    Vector3 vel = drone.GetVelocity();
    float speed = vel.magnitude;  // 速率
    if (speed > 5f)
    {
        // 高速无人机
    }
}
```

---

### TryGetVelocity

- **签名**: `bool TryGetVelocity(out Vector3 velocity)`
- **输入**: `out Vector3 velocity`
- **返回**: `bool` — 是否成功
- **用法**: 与 `TryGetPosition` 相同模式

---

## 操控 (Mutation)

### TeleportTo

- **签名**: `void TeleportTo(Vector3 position, Quaternion rotation, bool lerp)`
- **参数**:
  | 参数 | 类型 | 说明 |
  |---|---|---|
  | `position` | `Vector3` | 目标世界坐标位置 |
  | `rotation` | `Quaternion` | 目标世界旋转 |
  | `lerp` | `bool` | **可选** — `true` = 远程玩家看到平滑插值,`false`/默认 = 立即 snap |
- **说明**: 同时设置 Drone 的位置和旋转
- **网络行为**:
  - `lerp = false`(默认): 远程玩家看到 **瞬移**,无插值
  - `lerp = true`: 远程玩家看到 **平滑过渡**(具体时长由 VRChat 决定)
- **典型用途**:
  - 飞出世界边界 → 强制回中心
  - 检查点重置
  - 剧情位置强制引导
- **风险** ⚠️:
  - **不检查碰撞** — 传送到墙里可能导致不可预测行为
  - 频繁调用会 **触发大量网络同步**

```csharp
// 立即传送(远程玩家也立即看到)
drone.TeleportTo(respawnPos, respawnRot, false);

// 平滑传送(远程玩家看到缓动)
drone.TeleportTo(cinematicPos, cinematicRot, true);
```

> 📌 **与 `VRCPlayerApi.TeleportTo` 对比**:
> - Player 版本的 `TeleportTo` **不支持 lerp 参数** ,只有 Drone 版本支持平滑过渡
> - 这是 Drone 特有的能力

---

### SetVelocity

- **签名**: `void SetVelocity(Vector3 velocity)`
- **参数**:
  | 参数 | 类型 | 说明 |
  |---|---|---|
  | `velocity` | `Vector3` | 目标速度向量(m/s) |
- **说明**: 强制设置 Drone 的当前速度
- **典型用途**:
  - 弹射/击飞
  - 推力场(气流区)
  - 强制减速
- **风险** ⚠️:
  - **不保证持久** — 物理系统会持续应用推力/重力/玩家输入,此值会被快速覆盖
  - **不检查碰撞** — 高速度撞墙可能导致不可预测行为
  - 频繁调用会产生 **网络同步开销**

```csharp
// 弹射 — 向上 10 m/s
drone.SetVelocity(Vector3.up * 10f);

// 反向推力
drone.SetVelocity(-drone.GetVelocity() * 0.5f);
```

> 📌 **与 `VRCPlayerApi.SetVelocity` 关系**:
> - `VRCPlayerApi` **没有** `SetVelocity` 方法(只能通过 `Player Forces` 间接控制)
> - Drone 特有 `SetVelocity` 是因为 Drone 是 "自由飞行" 模式,需要更直接的物理控制

---

## 完整 API 对照表

| API | 签名 | 返回/输入 | 失败安全? | 备注 |
|---|---|---|---|---|
| `GetPlayer` | `VRCPlayerApi GetPlayer()` | 拥有者 Player | ❌ | 失效时引用无效,需 `IsValid` |
| `IsDeployed` | `bool IsDeployed()` | bool | — | **推荐先调用** |
| `GetPosition` | `Vector3 GetPosition()` | 位置 | ⚠️ 可能返零 | 配合 `IsDeployed` |
| `TryGetPosition` | `bool TryGetPosition(out Vector3)` | 位置 + bool | ✅ | **推荐使用** |
| `GetRotation` | `Quaternion GetRotation()` | 旋转 | ⚠️ 可能返单位 | 配合 `IsDeployed` |
| `TryGetRotation` | `bool TryGetRotation(out Quaternion)` | 旋转 + bool | ✅ | **推荐使用** |
| `GetVelocity` | `Vector3 GetVelocity()` | 速度 | ⚠️ 可能返零 | 配合 `IsDeployed` |
| `TryGetVelocity` | `bool TryGetVelocity(out Vector3)` | 速度 + bool | ✅ | **推荐使用** |
| `TeleportTo` | `void TeleportTo(Vector3, Quaternion, bool lerp)` | 操控 | — | `lerp=true` 支持平滑 |
| `SetVelocity` | `void SetVelocity(Vector3)` | 操控 | — | 瞬时覆盖,非持久 |

---

## 完整示例: 弹射与重置系统

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class DroneLauncher : UdonSharpBehaviour
{
    [Header("弹射器")]
    [SerializeField] private float _launchForce = 10f;

    [Header("重置区")]
    [SerializeField] private Transform _respawnPoint;
    [SerializeField] private float _voidY = -50f;

    [Header("气流区")]
    [SerializeField] private Vector3 _windDirection = new Vector3(0, 0, 5f);
    [SerializeField] private float _windStrength = 0.5f;

    // 弹射器 — 玩家触发
    public void LaunchDrone()
    {
        VRCDroneApi localDrone = Networking.LocalPlayer.GetDrone();
        if (localDrone == null) return;
        if (!localDrone.IsDeployed()) return;

        // 向上弹射
        localDrone.SetVelocity(Vector3.up * _launchForce);
    }

    // 重置区 — Drone 掉出世界
    public override void OnDroneTriggerStay(VRCDroneApi drone)
    {
        if (!drone.IsDeployed()) return;

        Vector3 pos;
        if (!drone.TryGetPosition(out pos)) return;  // 优雅失败

        if (pos.y < _voidY)
        {
            // 立即传送到重置点
            drone.TeleportTo(_respawnPoint.position, _respawnPoint.rotation, false);
        }
    }

    // 气流区 — 给 Drone 持续推力
    public override void OnDroneTriggerStay2(VRCDroneApi drone) { } // 仅示意
}
```

> ⚠️ **示例注意**: 上面的 `OnDroneTriggerStay2` 是 **示意错误代码** — 同名事件会冲突,实际项目需用多个 UdonBehaviour 或状态机区分。

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **未部署时零值** | `GetPosition/GetRotation/GetVelocity` 在未部署时**可能**返回零值/单位值,需 `IsDeployed` 守护 |
| **`TeleportTo` 不检查碰撞** | 传送到墙内/几何体外可能导致不可预测行为 |
| **`SetVelocity` 不持久** | 物理系统会持续推力/重力,设值会被快速覆盖 |
| **频繁调用同步** | `TeleportTo` / `SetVelocity` 频繁调用会产生网络同步开销 |
| **Drone 模式可用性** | 需先确认世界启用 Drone 模式,否则所有 API 行为未定义 |
| **Despawn 失效** | Drone 被销毁后,所有方法返回值未定义,需 `IsDeployed` 守护 |

---

## 与底层 API 的对照

| 本文件 API | `VRCPlayerApi` 对应 API | 差异 |
|---|---|---|
| `GetPlayer()` | `GetDrone()` | 互为反向 |
| `GetPosition()` | `GetPosition()` | **同名同语义** |
| `GetRotation()` | `GetRotation()` | **同名同语义** |
| `GetVelocity()` | `GetVelocity()` | **同名同语义** |
| `TeleportTo(pos, rot, lerp)` | `TeleportTo(pos, rot)` | **Drone 版本多 lerp 参数** |
| `IsDeployed()` | ❌ 无 | **Drone 专有** |
| `SetVelocity(vel)` | ❌ 无 | **Drone 专有** |
| `TryGet*` 系列 | ❌ 无 | **Drone 专有** (`.NET Try 模式`) |

---

## 最佳实践

1. **优先 `TryGet*` 系列**: 比 `IsDeployed` + `Get*` 组合更显式、更安全
2. **`IsDeployed` 必查**: 在 Trigger 事件中处理前先 `IsDeployed()` 守护
3. **`TeleportTo` 避免穿墙**: 传送前检查目标位置是否在合法区域
4. **`SetVelocity` 用于瞬时效果**: 持续推力应改用 `Player Forces` 思路(Drone 无对应 API,需用 `SetVelocity` 配合 Timer)
5. **`lerp=true` 仅用于剧情**: 平滑传送会产生网络同步开销,日常重置用 `false`
6. **多平台测试**: Quest 上 Drone 物理/性能可能与 PC 不同,需实测
