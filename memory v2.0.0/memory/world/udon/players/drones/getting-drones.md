---
title: Getting Drones — 获取 Drone 实例
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - udonsharp

aliases:
  - "Getting Drones — 获取 Drone 实例"

related:
  - index.md

source: https://creators.vrchat.com/worlds/udon/players/drones/getting-drones/ (Last updated: 2026-03-20)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Getting Drones — 获取 Drone 实例

> Domain: World / Udon / Players / Drones
> Subtype: API 详解 — 获取方法 + Trigger 事件
> 父级索引: [`./index.md`](./index.md)
> 抓取日期: 2026-06-15

---

## 概述

本章涵盖两件事:

1. **如何获取 `VRCDroneApi` 实例** (从 `VRCPlayerApi` 派生)
2. **3 个 Trigger 事件** (Drone 与 Collider 交互)

> 📌 **设计原则**: 与 `VRCPlayerApi` 平行,Drone **不** 通过 `GetPlayers()` 一类的方法批量获取,而是 **每个 Player 单独查询**。

---

## Methods (方法)

### VRCPlayerApi.GetDrone

- **签名**: `VRCDroneApi GetDrone()`
- **返回**: `VRCDroneApi` 或 **null**
- **说明**: 获取该玩家正在使用的 Drone
- **null 条件**:
  - 玩家 **未启动 Drone 模式**
  - Drone 模式在当前世界 **未启用**
- **风险** ⚠️: 频繁调用成本极低,但**必须做 null 检查**

```csharp
public override void OnPlayerJoined(VRCPlayerApi player)
{
    VRCDroneApi drone = player.GetDrone();
    if (drone != null)
    {
        // 玩家已部署 Drone — 立刻交互
        Debug.Log($"Player {player.displayName} has a drone at {drone.GetPosition()}");
    }
    else
    {
        // 玩家未部署 Drone
    }
}
```

---

### VRCDroneApi.GetPlayer

- **签名**: `VRCPlayerApi GetPlayer()`
- **返回**: `VRCPlayerApi` (拥有该 Drone 的玩家)
- **说明**: 从 Drone 回到原 Player
- **用途**:
  - 在 Trigger 事件中识别 **哪个玩家** 的 Drone 触发了事件
  - 查询玩家属性 (`isMaster` / `isVRCPlus` / `displayName` 等)

```csharp
public override void OnDroneTriggerEnter(VRCDroneApi drone)
{
    VRCPlayerApi owner = drone.GetPlayer();
    if (Utilities.IsValid(owner))
    {
        Debug.Log($"Drone of {owner.displayName} entered");
    }
}
```

---

## Events (事件)

> 📌 **3 个 Trigger 事件** 都接收 `VRCDroneApi drone` 参数。
> 触发条件:**Drone Collider** 进入/离开/停留在 **UdonBehaviour 同一 GameObject 上的 Trigger Collider**。
> 与 Player Collider 的 Trigger 事件 **完全独立、互不触发**。

---

### OnDroneTriggerEnter

- **签名**: `void OnDroneTriggerEnter(VRCDroneApi drone)`
- **触发时机**: Drone 进入 **本脚本所在 GameObject 的 Trigger Collider**
- **参数**:
  | 参数 | 类型 | 说明 |
  |---|---|---|
  | `drone` | `VRCDroneApi` | 触发事件的 Drone,可用于查询玩家/位置/速度 |

- **典型用途**:
  - 无人机进入区域 → 触发剧情/任务/特效
  - 无人机飞过检查点 → 计时
  - 安全区/危险区检测

```csharp
public override void OnDroneTriggerEnter(VRCDroneApi drone)
{
    VRCPlayerApi owner = drone.GetPlayer();
    if (!Utilities.IsValid(owner)) return;

    // 示例: 玩家驾驶无人机进入目标区域
    Debug.Log($"{owner.displayName}'s drone entered");

    if (drone.IsDeployed())
    {
        // 已部署 — 安全执行位置查询
        Vector3 pos = drone.GetPosition();
    }
}
```

---

### OnDroneTriggerExit

- **签名**: `void OnDroneTriggerExit(VRCDroneApi drone)`
- **触发时机**:
  1. Drone **离开** Trigger Collider,或
  2. Drone **在 Trigger 内部被销毁 (despawn)** — 例如玩家主动退出 Drone 模式
- **重要** ⚠️: **despawn 也会触发此事件** ,但此时 `drone.GetPlayer()` 可能返回 **null**(引用已失效),需 `Utilities.IsValid` 保护

```csharp
public override void OnDroneTriggerExit(VRCDroneApi drone)
{
    // ⚠️ 必须 IsValid — despawn 场景下 player 引用可能失效
    VRCPlayerApi owner = drone.GetPlayer();
    if (!Utilities.IsValid(owner))
    {
        // Drone 已被销毁,玩家可能已离开或退出 Drone 模式
        return;
    }

    Debug.Log($"{owner.displayName}'s drone exited");
}
```

---

### OnDroneTriggerStay

- **签名**: `void OnDroneTriggerStay(VRCDroneApi drone)`
- **触发时机**: Drone **每帧** 停留在 Trigger 内
- **性能警告** ⚠️:
  - **每帧调用** ,类似 `Update`
  - 逻辑成本必须 **极低** (O(1) 简单判断)
  - **严禁** 在其中执行 `GetPlayers()` 数组分配、复杂计算、网络序列化
- **典型用途**:
  - 持续伤害(DoT)
  - 持续 buff/debuff
  - 推力(Drone 飞过气流区域)

```csharp
public override void OnDroneTriggerStay(VRCDroneApi drone)
{
    // 保持轻量 — 此函数每帧调用
    if (!drone.IsDeployed()) return;

    Vector3 pos = drone.GetPosition();
    if (pos.y < -50f)
    {
        // Drone 掉出世界,自动传送回起点
        drone.TeleportTo(Vector3.zero, Quaternion.identity, false);
    }
}
```

---

## 与 Player Trigger 事件的对比

| 维度 | Player Trigger (`OnPlayerTriggerEnter/Exit/Stay`) | Drone Trigger (`OnDroneTriggerEnter/Exit/Stay`) |
|---|---|---|
| **触发对象** | 玩家 Avatar(Character Controller) | 玩家 Drone(独立 Collider) |
| **触发场景** | 玩家以 Avatar 行走/飞行进入 | 玩家从 Drone 视角飞入 |
| **参数** | `VRCPlayerApi player` | `VRCDroneApi drone` |
| **事件互通** | ❌ **不会** 触发 Drone 事件 | ❌ **不会** 触发 Player 事件 |
| **多形态玩家** | 一个玩家可同时触发 Player + Drone 事件(取决于其形态) | 同上 |
| **来源 Collider** | Avatar 物理 Collider | Drone 物理 Collider |

> 📌 **关键设计**:
> - 想同时支持两种形态,必须 **同时实现两套事件** (`OnPlayerTriggerEnter` + `OnDroneTriggerEnter`)
> - 两个事件的 `GetPlayer()` 返回 **同一个** `VRCPlayerApi`(若该玩家两种形态都进过 Trigger)
> - 详细 Collider 配置见 `memory/world/udon/players/player-collisions.md`

---

## 完整示例: 无人机检查点系统

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class DroneCheckpoint : UdonSharpBehaviour
{
    [Header("Checkpoint 设置")]
    [SerializeField] private Transform _respawnPoint;
    [SerializeField] private float _fallThreshold = -50f;

    [Header("触发器")]
    [SerializeField] private Collider _trigger;  // 必须勾选 isTrigger

    // 用于在 Player 形态 + Drone 形态都支持
    public override void OnPlayerTriggerEnter(VRCPlayerApi player)
    {
        // Player 形态 — 略
    }

    public override void OnDroneTriggerEnter(VRCDroneApi drone)
    {
        VRCPlayerApi owner = drone.GetPlayer();
        if (!Utilities.IsValid(owner)) return;
        if (!drone.IsDeployed()) return;

        // 检查点逻辑(简化)
        Debug.Log($"[Checkpoint] Drone of {owner.displayName} entered");
    }

    public override void OnDroneTriggerStay(VRCDroneApi drone)
    {
        if (!drone.IsDeployed()) return;

        // 每帧 — 必须轻量
        if (drone.GetPosition().y < _fallThreshold)
        {
            drone.TeleportTo(
                _respawnPoint.position,
                _respawnPoint.rotation,
                false  // false = 立即传送(非平滑)
            );
        }
    }

    public override void OnDroneTriggerExit(VRCDroneApi drone)
    {
        VRCPlayerApi owner = drone.GetPlayer();
        if (!Utilities.IsValid(owner)) return;
        Debug.Log($"[Checkpoint] Drone of {owner.displayName} exited");
    }
}
```

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **`GetDrone()` 返回 null** | 玩家未部署 Drone / 世界未启用 Drone 模式,**必须** null 检查 |
| **`OnDroneTriggerStay` 性能** | 每帧触发,严禁复杂逻辑 |
| **Despawn 场景** | `OnDroneTriggerExit` 在 Drone 被销毁时也会触发,`GetPlayer()` 可能为 null |
| **事件不互通** | Player 与 Drone Trigger 事件独立,需分别监听 |
| **多平台** | Quest 上 Drone 模式行为/性能可能与 PC 不同 |
| **模式可用性** | 部分世界/平台可能未启用 Drone 模式,代码必须能优雅降级 |

---

## 与底层 API 的对照

| 本文件 API | 底层 `player-api.md` |
|---|---|
| `VRCPlayerApi.GetDrone()` | `GetDrone()` (本文件首次详细出现) |
| `VRCDroneApi.GetPlayer()` | 本文件首次详细出现 |
| `OnDroneTriggerEnter/Exit/Stay` | `memory/api/events-reference.md` 应补充这 3 个事件 |

---

## 最佳实践

1. **永远 null 检查**: `GetDrone()` 之后用 `if (drone == null) return;` 守护
2. **用 `Utilities.IsValid` 守护 owner**: Despawn 场景下 player 引用可能失效
3. **`OnDroneTriggerStay` 保持轻量**: 只做简单判断,不要分配、不要序列化
4. **同时实现两套事件**: 若需支持玩家在 Avatar 与 Drone 形态下都响应,必须同时实现 Player + Drone Trigger 事件
5. **Drone 模式可用性**: 在世界发布前,**必须** 实际测试 Drone 模式是否启用,避免无声失效
