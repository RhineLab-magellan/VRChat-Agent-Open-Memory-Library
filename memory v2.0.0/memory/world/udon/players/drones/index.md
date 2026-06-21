---
title: Drone API 总览 (VRCDroneApi)
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "Drone API 总览 (VRCDroneApi)"

related:
  - index.md
  - getting-drones.md
  - drone-information.md

source: https://creators.vrchat.com/worlds/udon/players/drones/ (Last updated: 2026-03-07)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Drone API 总览 (VRCDroneApi)

> Domain: World / Udon / Players / Drones
> Subtype: API 总览
> 父级索引: [`memory/world/udon/players/index.md`](../index.md)
> 抓取日期: 2026-06-15

---

## 概述

VRChat 提供 **"无人机视角" 玩家模式** — 玩家可以从无人机视角观察世界。Udon 通过 `VRCDroneApi` 与正在使用无人机的玩家进行交互。

`VRCDroneApi` **不是** `VRCPlayerApi` 的子类或替代品,而是 **平行的、独立的对象**:

| 维度 | `VRCPlayerApi` | `VRCDroneApi` |
|---|---|---|
| **代表** | 玩家角色(Avatar) | 玩家部署的无人机 |
| **获取来源** | `Networking.LocalPlayer` / `VRCPlayerApi.GetPlayers()` | `player.GetDrone()` |
| **物理形态** | 玩家 Avatar(Character Controller) | 独立 Collider(无人机) |
| **Trigger 事件** | `OnPlayerTriggerEnter/Exit/Stay` | `OnDroneTriggerEnter/Exit/Stay` |
| **位置/旋转查询** | `GetPosition()` / `GetRotation()` | `GetPosition()` / `GetRotation()` |
| **速度查询** | `GetVelocity()` | `GetVelocity()` |
| **传送** | `TeleportTo()` | `TeleportTo()` (支持平滑过渡) |
| **使用模式** | 玩家存在即生效 | **仅当玩家启动 Drone 模式时存在** |

---

## 与 `VRCPlayerApi` 的关系

`VRCDroneApi` **从属**于 `VRCPlayerApi`,两者是 **持有关系**:

```text
VRCPlayerApi (玩家角色)
└── GetDrone() → VRCDroneApi (该玩家的无人机,如果已部署)
                  └── GetPlayer() → VRCPlayerApi (回到原玩家)
```

> 📌 **关键设计**:
> - 一个玩家同时 **只能拥有一个** 无人机
> - 玩家 **未启动 Drone 模式时** ,`GetDrone()` 返回 **null**
> - 玩家 **离开实例** 时,其无人机也会被销毁,引用一并失效

---

## 子页面

| 页面 | 内容 |
|---|---|
| [getting-drones.md](./getting-drones.md) | `GetDrone()` 获取方法 + 3 个 Trigger 事件 |
| [drone-information.md](./drone-information.md) | Drone 状态、位置/旋转/速度/传送 等 10 个 API |

---

## 支持的事件 (Trigger Events)

Udon Behaviour 上的 Trigger Collider 监听 **无人机** 进入时,会触发以下事件:

| 事件 | 触发时机 | 签名 |
|---|---|---|
| `OnDroneTriggerEnter` | Drone 进入 Trigger Collider | `(VRCDroneApi drone)` |
| `OnDroneTriggerExit` | Drone 离开 Trigger Collider **或** 在 Trigger 内被销毁(despawn) | `(VRCDroneApi drone)` |
| `OnDroneTriggerStay` | Drone 每帧停留在 Trigger 内 | `(VRCDroneApi drone)` |

> ⚠️ **与 Player Trigger 事件平行,不互通**:
> - 玩家以 **Avatar 形态** 进入 Trigger → 触发 `OnPlayerTriggerEnter`,**不会** 触发 `OnDroneTriggerEnter`
> - 玩家以 **Drone 形态** 进入 Trigger → 触发 `OnDroneTriggerEnter`,**不会** 触发 `OnPlayerTriggerEnter`
> - 同一玩家可 **先后** 触发两个事件(先 Player 后 Drone,或反之)
>
> 详见 [`getting-drones.md`](./getting-drones.md) 与 `memory/world/udon/players/player-collisions.md` 的对比。

---

## 模式可用性

> ⚠️ **Drone 模式仅在特定 World 启用** :
> - 取决于 **世界发布设置** 与 **平台限制** (PC / Quest 行为可能不同)
> - 玩家在 **未启用 Drone 模式的世界** 中,`GetDrone()` 始终返回 `null`
> - `OnDroneTriggerEnter/Exit/Stay` 事件 **完全不会触发**
> - **设计建议** : 任何 Drone 相关逻辑都应做 **null 检查** 和 **"未部署" 状态分支**

---

## 与已有知识库的关系

| 现有知识库 | 关系 |
|---|---|
| [`../index.md`](../index.md) | **父级** Player API 总览,Drone API 是其子分类 |
| `memory/api/player-api.md` | 底层 `VRCPlayerApi` 文档,**`GetDrone()`** 是其延伸 |
| `memory/api/events-reference.md` | 应补充 3 个 Drone Trigger 事件 |
| `memory/world/udon/players/player-collisions.md` | Player Collisions 兄弟页面,Drone 与 Player Trigger 平行 |

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **Drone API 新功能** | 2024-2025 推出,API 稳定性需关注,文档中应标注 **官方可能更新** |
| **模式可用性** | Drone 模式需世界启用,`GetDrone()` 可能始终返回 `null` |
| **Trigger 事件不互通** | Drone 与 Player Trigger 事件独立,需分别监听,详见上方表格 |
| **`GetDrone()` 需 null 检查** | 玩家未部署 Drone 时返回 `null` |
| **引用失效** | 玩家离开实例时,其 Drone 引用立即失效,`OnPlayerLeft` 中**严禁**继续访问 |
| **性能 — `OnDroneTriggerStay`** | 每帧触发,复杂逻辑会拖慢世界,需严格控制开销 |
| **多平台差异** | Quest 性能较弱,Drone 复杂交互需重点测试 |

---

## Sub-page 导航

- 📄 [getting-drones.md](./getting-drones.md) — `GetDrone()` 与 3 个 Trigger 事件
- 📄 [drone-information.md](./drone-information.md) — 位置/旋转/速度/传送等 10 个 API
