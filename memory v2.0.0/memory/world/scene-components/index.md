---
title: Scene Components 总览
category: world
subcategory: scene-components

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "Scene Components 总览"

related:
  - ../whitelisted-world-components.md
  - textmeshpro.md
  - vrc-avatarpedestal.md
  - vrc-cameradolly.md
  - vrc-mirrorreflection.md
  - vrc-objectsync.md
  - vrc-portalmarker.md
  - vrc-scenedescriptor.md
  - vrc-station.md
  - vrc-enablepersistence.md
  - api/pickups.md
  - api/audio.md
  - api/ui.md
  - api/events-reference.md
  - api/persistence.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Scene Components 总览

> VRChat Worlds 专用组件索引
>
> 来源: https://creators.vrchat.com/worlds/components/
> 最后更新: 2026-06-15
> 本任务版本: 覆盖 9 个核心组件 (达到单任务 URL 上限)

---

## 概述

每个想导入 VRChat 的 Unity 场景都需要 `VRC_SceneDescriptor` 组件。VRChat Worlds SDK 提供了多种专用组件,允许用户与世界进行交互(拾取物体、在镜面中看到自己、坐下、使用 UI 等)。

完整组件白名单请参考 [Allowlisted World Components](../whitelisted-world-components.md)。

> **FACT**: 每个 World 必须有 **1 个且仅有 1 个** `VRC_SceneDescriptor`,缺失会导致 World 完全无法加载。

---

## 组件索引

| 组件 | 类名 | 文档 | 用途 |
|------|------|------|------|
| **TextMesh Pro** | `TMP_Text` (TextMeshProUGUI / TextMeshPro) | [textmeshpro.md](./textmeshpro.md) | 高质量 2D/3D 文本 |
| **VRC Avatar Pedestal** | `VRC_AvatarPedestal` | [vrc-avatarpedestal.md](./vrc-avatarpedestal.md) | 展示和切换 Avatar |
| **VRC Camera Dolly** | `VRC_CameraDollyAnimation` / `Path` / `Point` | [vrc-cameradolly.md](./vrc-cameradolly.md) | 相机轨道动画 |
| **VRC Mirror Reflection** | `VRC_MirrorReflection` | [vrc-mirrorreflection.md](./vrc-mirrorreflection.md) | 实时反射镜面 |
| **VRC Object Sync** | `VRCObjectSync` | [vrc-objectsync.md](./vrc-objectsync.md) | 物理对象位置/旋转同步(核心) |
| **VRC Portal Marker** | `VRC_PortalMarker` | [vrc-portalmarker.md](./vrc-portalmarker.md) | 传送门 |
| **VRC Scene Descriptor** | `VRCSceneDescriptor` | [vrc-scenedescriptor.md](./vrc-scenedescriptor.md) | 场景描述符(World 必含) |
| **VRC Station** | `VRCStation` | [vrc-station.md](./vrc-station.md) | 玩家固定座位 |
| **VRC Enable Persistence** | `VRCEnablePersistence` | [vrc-enablepersistence.md](./vrc-enablepersistence.md) | 启用持久化 |

### 本任务未覆盖的组件(后续任务处理)

- `VRC_Pickup` (详见 [../../api/pickups.md](../../api/pickups.md))
- `VRC_SpatialAudioSource` (详见 [../../api/audio.md](../../api/audio.md))
- `VRC_UIShape` (详见 [../../api/ui.md](../../api/ui.md))
- `VRC_PhysBone` / `VRC_PhysBoneCollider` / `VRC_PhysBoneRoot` (Avatar 域,详见 [../../avatar/](../../avatar/))
- `VRC_ContactSender` / `VRC_ContactReceiver` (Avatar 域)
- `VRC_Constraints` (Avatar 域)

---

## World PhysBone 与 Contact 限制

> **FACT** (来自官方文档,验证于 2025-03-07): 当前加载的 World 中:
> - **PhysBone 限制**: 1024 个 active 的 PhysBone + PhysBone Collider
> - **Contact 限制**: 1024 个 active 的 Contact Sender + Contact Receiver
>
> 超过上限的组件将被禁用,直到现有组件被禁用或销毁。
> SDK 会显示警告,但只要在运行时不超过 1024 个,警告可忽略。

---

## Inspector 通用提示

- 所有 Scene Component 都通过 Unity Inspector 暴露配置
- UdonSharp 中通过 `GetComponent<T>()` 引用,例如:
  ```csharp
  [SerializeField] private VRCStation station;
  [SerializeField] private VRCObjectSync objectSync;
  [SerializeField] private VRC_PortalMarker portal;
  ```
- 多数组件提供 Udon 事件回调(Networked/本地),可在 `UdonSharpBehaviour` 子类中重写

---

## 跨页引用

- [VRCSceneDescriptor 与 VRCObjectSync 协作](./vrc-scenedescriptor.md#object-prefabs)
- [VRCObjectSync 与 Manual Sync 区别](./vrc-objectsync.md#与-manual-sync-区别)
- [VRCStation 事件回调](../../api/events-reference.md#station-事件)
- [VRCEnablePersistence 持久化 API](../../api/persistence.md)
- [VRC_Pickup 与 VRCObjectSync](../../api/pickups.md)
- [VRC_SpatialAudioSource 3D 音频](../../api/audio.md)

---

## 相关模式(在 `patterns/` 中)

- 物理对象所有权自动转移 → 见 `patterns/collision-ownership-transfer.md` (引用 vrc-objectsync)
- 座位事件驱动逻辑 → 见 `patterns/station-event-driven-logic.md` (引用 vrc-station)
- 自定义传送门 → 见 `patterns/dynamic-portal-marker.md` (引用 vrc-portalmarker)
