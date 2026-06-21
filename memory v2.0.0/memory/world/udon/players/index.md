---
title: Player API 总览 (VRCPlayerApi)
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "Player API 总览 (VRCPlayerApi)"

related:
  - drones/index.md
  - drones/getting-drones.md
  - getting-players.md
  - player-audio.md
  - player-avatar-scaling.md
  - player-collisions.md
  - player-forces.md
  - player-positions.md
  - drones/drone-information.md

source: https://creators.vrchat.com/worlds/udon/players/ (Last updated: 2026-03-04)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Player API 总览 (VRCPlayerApi)

> Domain: World / Udon / Players
> Subtype: API 总览
> 底层引用: `memory/api/player-api.md`
> 抓取日期: 2026-06-15

---

## 概述

Udon 通过 `VRCPlayerApi` 与玩家交互。玩家进入/离开实例时,任何监听 `OnPlayerJoined` / `OnPlayerLeft` 事件的 UdonBehaviour 都会被触发。

由于 `VRCPlayerApi` 涵盖内容极广,VRChat 官方按用途将其拆分为多个子页面:

| 子页面 | 涵盖内容 |
|---|---|
| **Getting Players** | 获取玩家对象/列表/Tag 系统 |
| **Player Positions** | 位置、旋转、骨骼、追踪、速度、传送 |
| **Player Forces** | 移动速度、重力、跳跃、Immobilize |
| **Player Collisions** | Trigger、Physics、Particle 碰撞 |
| **Player Audio** | 语音增益/距离 + Avatar 音频 |
| **Player Avatar Scaling** | 玩家控制的缩放 vs 世界权威缩放 |
| **Drone API** | 无人机玩家 (单独在 `drones/` 目录,见 task-12) |
| **Player Events** | 玩家事件(Graph 节点) |

> 📌 **Drone API 详见 [`./drones/`](./drones/index.md) 目录** (task-12 独立子分类)
>
> ⚠️ **关键差异 — `OnPlayerTriggerEnter` vs `OnDroneTriggerEnter`** :
>
> | 维度 | Player Trigger | Drone Trigger |
> |---|---|---|
> | **参数** | `VRCPlayerApi player` | `VRCDroneApi drone` |
> | **触发对象** | 玩家 Avatar(Character Controller) | 玩家 Drone(独立 Collider) |
> | **事件互通** | ❌ **不会** 触发 Drone 事件 | ❌ **不会** 触发 Player 事件 |
> | **并行监听** | 若需同时响应两种形态,**必须分别实现两套事件** | 同左 |
> | **来源 GameObject** | UdonBehaviour 同一 GameObject 上的 Collider(isTrigger) | 同左 |
>
> → **链向** [`./drones/index.md`](./drones/index.md) 与 [`./drones/getting-drones.md`](./drones/getting-drones.md)

---

## 通用属性与方法 (Generally Useful)

### IsValid

- **类型**: `Boolean` (静态方法 `Utilities.IsValid(player)` 或实例属性)
- **说明**: 检查 Player 引用是否仍有效
- **关键**: 玩家离开后引用会失效,**使用前必须检查**
- **Udon Graph**: 通用 IsValid 节点提供 True/False 双流输出

```csharp
public override void OnPlayerLeft(VRCPlayerApi player)
{
    if (Utilities.IsValid(player))
    {
        // Player is valid
    }
    else
    {
        // Player is not valid
    }
}
```

> 📌 **底层引用**: `memory/api/player-api.md` 错误案例 — "缓存 VRCPlayerApi 引用过长(玩家离开后引用失效)"

---

### EnablePickups

- **类型**: `Boolean`
- **说明**: 启用/禁用玩家的 `VRCPickup` 拾取能力
- **默认**: `true` (开),仅在需要关闭时使用

---

### get displayName

- **类型**: `string`
- **说明**: 玩家显示名称
- **关键差异**: `displayName` ≠ Username
  - `displayName`: VRChat 内显示的昵称(公开)
  - `Username`: 登录用户名(**不公开,不可在 Udon 中获取**)

---

### Get isLocal

- **输入**: `VRCPlayerApi`
- **输出**: `Boolean`
- **说明**: 该 Player 是否是本地玩家(你)

---

### Get isMaster

- **输入**: `VRCPlayerApi`
- **输出**: `Boolean`
- **说明**: 该 Player 是否是**实例 Master**
- **参考**: [Instance Master](https://creators.vrchat.com/worlds/udon/networking#the-instance-master)

---

### Get isInstanceOwner

- **输入**: `VRCPlayerApi`
- **输出**: `Boolean`
- **说明**: 该 Player 是否是**当前实例 Owner**(邀请/好友+实例)
- **关键**: 公开实例始终返回 `false`

---

### Get isVRCPlus

- **输入**: `VRCPlayerApi`
- **输出**: `Boolean`
- **说明**: 该 Player 是否有活跃的 VRC+ 订阅

---

### Get isSuspended

- **输入**: `VRCPlayerApi`
- **输出**: `Boolean`
- **说明**: 玩家设备是否**被暂停**
- **触发条件**:
  - 设备进入睡眠模式
  - 切换到其他应用
- **平台差异** ⚠️:
  - **PC 玩家永远不会被暂停**
  - **Quest/Android 设备** 在挂起/切换应用时会暂停
- **关键约束**:
  - `isSuspended` 对**本地玩家**始终返回 `false` (因为 Udon 在本地玩家暂停时根本不运行)
  - 代码应假设**任何平台任何时候都可能有设备被暂停**,不能依赖当前行为

---

### GetPickupInHand

- **输入**: `VRCPlayerApi, Hand (None / Left / Right)`
- **输出**: `VRCPickup` (可能为 `null`)
- **限制**: **仅本地玩家有效**
- **说明**: 获取玩家指定手中持有的 `VRCPickup`,未持有时返回 `null`

---

### IsOwner

- **输入**: `VRCPlayerApi, GameObject`
- **输出**: `Boolean`
- **说明**: 该 Player 是否是给定 GameObject 的 Owner
- **重要**: 与 Sync 强相关,详见 `memory/api/networking.md`

---

### IsUserInVR

- **输入**: `VRCPlayerApi`
- **输出**: `Boolean`
- **说明**: 该 Player 是否正在使用 VR 头显

---

### PlayHapticEventInHand

- **签名**: `_VRCPlayerApi, Hand, float, float, float_`
- **参数**:
  | 参数 | 范围 | 说明 |
  |---|---|---|
  | `Hand` | None/Left/Right | 目标手柄 |
  | `duration` | 秒 | 震动持续时间 |
  | `amplitude` | 0.0 - 1.0 | 震动强度 |
  | `frequency` | 0.0 - 1.0 | 震动频率(速度) |
- **说明**: 触发玩家手柄震动,**仅当玩家有 Haptic 控制器时有效**
- **风险** ⚠️: 不同控制器上的感受差异极大

---

### UseAttachedStation

- **签名**: `_VRCPlayerApi_`
- **说明**: 使玩家**进入**与该 UdonBehaviour **同一 GameObject 上的 Station**
- **应用场景**: 椅子、载具、座位等 Station 同步进入

---

### SimulationTime

- **类型**: `float`
- **说明**: 玩家的模拟时间
- **参考**: [Network Components](https://creators.vrchat.com/worlds/udon/networking/network-components/)

---

### UseLegacyLocomotion

- **签名**: `_VRCPlayerApi_`
- **状态**: ⚠️ **NOT RECOMMENDED** (官方明确不推荐)
- **说明**: 开启旧版移动系统,模拟已废弃的 SDK2 移动方式
- **副作用**: 启用后会**持续生效**直到玩家离开世界
- **使用场景**: 仅在需要兼容极旧世界行为时使用

---

## 语言 API (Language)

> 完整的多语言能力参考。所有语言代码均为 **RFC 5646** 格式。

### GetCurrentLanguage

- **返回**: `string` (RFC 5646 格式)
- **示例**: `en`、`ja`、`es`、`zh-CN`、`zh-TW`
- **说明**: 获取**本地用户**当前选择的语言
- **限制**: 仅本地玩家有效

### GetAvailableLanguages

- **返回**: `string[]` (RFC 5646 格式数组)
- **说明**: 获取 VRChat 设置中玩家**可选择的所有语言**
- **限制**: 仅本地玩家有效

#### 已知 RFC 5646 语言代码参考

| 代码 | 语言 |
|---|---|
| `en` | English (默认) |
| `ja` | 日本語 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `ko` | 한국어 |
| `zh-CN` | 简体中文 |
| `zh-TW` | 繁體中文(台灣) |
| `ru` | Русский |
| `pt-BR` | Português (Brasil) |
| `th` | ภาษาไทย |
| `vi` | Tiếng Việt |

> 📝 **注意**:VRChat 实际支持的语言集合可能随 SDK 版本更新,代码中应做空值/长度检查,而非硬编码。

---

## 与已有知识库的关系

| 现有知识库 | 关系 |
|---|---|
| `memory/api/player-api.md` | **底层 API 总览**(简略版),本文件为**应用层详解** |
| `memory/api/events-reference.md` | 玩家事件回调 (`OnPlayerJoined`/`OnPlayerLeft`/`OnPlayerSuspendChanged` 等),应补充 3 个 Drone Trigger 事件 |
| `memory/world/udon/players/*.md` | 本目录其他 6 个子页面 |
| `memory/world/udon/players/drones/` | **Drone API 子分类** (task-12 已完成,3 个 .md) |

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **Drone API 分离** | 必须在文档/代码中明确分隔 `VRCPlayerApi` 与 `VRCDroneApi`,避免混淆 |
| **`isSuspended` 跨平台差异** | PC 永远为 `false`,**不可假设** 跨平台行为一致 |
| **`isMaster` / `isInstanceOwner` 变化** | Master 转移时会变化,需在 `OnPlayerTriggerEnter` 等事件中**重新检查**,不能依赖缓存 |
| **`PlayHapticEventInHand` 感受差异** | `amplitude`/`frequency` 在不同控制器上感受差异大,需实测 |
| **`UseLegacyLocomotion` 持续生效** | 启用后会持续到玩家离开,**不能反向关闭** |
| **引用失效** | 玩家离开后 `VRCPlayerApi` 引用立即失效,`OnPlayerLeft` 中**严禁**继续操作该 player 的属性(但事件本身仍触发) |

---

## Sub-page 导航

- 📄 [getting-players.md](./getting-players.md) — 获取玩家对象
- 📄 [player-audio.md](./player-audio.md) — 语音与 Avatar 音频
- 📄 [player-avatar-scaling.md](./player-avatar-scaling.md) — Avatar 缩放
- 📄 [player-collisions.md](./player-collisions.md) — 玩家碰撞 (Player Trigger 事件)
- 📄 [player-forces.md](./player-forces.md) — 移动/力/重置
- 📄 [player-positions.md](./player-positions.md) — 位置/旋转/追踪
- 📁 [drones/](./drones/index.md) — **Drone API** (子分类)
  - 📄 [drones/getting-drones.md](./drones/getting-drones.md) — `GetDrone()` + 3 个 Drone Trigger 事件
  - 📄 [drones/drone-information.md](./drones/drone-information.md) — 位置/旋转/速度/传送 等 10 个 API
