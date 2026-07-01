---
title: "SDK Prefabs"
category: world
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - sync
  - video
  - mirror
  - portal
  - avatar
aliases:
  - "SDK Prefabs"
  - sdk-prefabs
related:
  - layers.md
  - vvmw.md
  - creator-economy.md
  - items.md
  - performance-guide.md
---
# SDK Prefabs

> 来源: VRChat 官方文档 (https://creators.vrchat.com/worlds/sdk-prefabs/)
> 源 URL Last Updated: **Aug 29, 2023**
> 抓取日期: 2026-06-15
> 置信度: High

---

## Domain

**World → SDK Prefab 资源** — VRChat Worlds SDK 自带的 8 个 Udon 示例 Prefab，作为最佳实践参考实现。

## Subdomain

- Avatar Pedestal（Avatar 切换）
- Chair（座椅）
- Mirror（镜像）
- Portal Marker（实例传送）
- World（场景描述符）
- Video Sync（视频播放）
- Pen System（3D 绘画）
- Variable Sync（同步示例）

## Conclusion

VRChat Worlds SDK 在 `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs/` 下提供 **8 个 Udon 示例 Prefab**，覆盖 World 开发的核心场景。**VRCPortalMarker 必须在场景根**才能正确同步目标实例。所有 Prefab 都是开源 Udon 实现，**推荐作为生产环境起点或参考实现**。

---

## FACT — 8 个 SDK Prefab 完整列表

| Prefab | 路径 | 用途 | 强制位置 |
|---|---|---|---|
| **VRCAvatarPedestal** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > AvatarPedestal` | 点击切换 Avatar 示例 | 无 |
| **VRCChair** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > VRCChair > VRCChair3` | 点击就坐椅子示例 | 无 |
| **VRCMirror** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > VRCMirror` | 镜面渲染示例 | 无 |
| **VRCPortalMarker** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > VRCPortalMarker` | 跨实例传送门示例 | ⚠ **必须场景根** |
| **VRCWorld** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > World` | VRC_SceneDescriptor 场景定义示例 | 场景根 |
| **VRCVideoSync** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > VideoPlayers` | Udon 视频播放器示例 | 无 |
| **Simple Pen System** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > SimplePenSystem` | 3D 绘画笔示例 | 无 |
| **Udon Variable Sync** | `Packages > VRChat SDK - Worlds > Samples > UdonExampleScene > Prefabs > Udon Variable Sync` | 同步机制自文档示例 | 无 |

---

## Evidence — Prefab 详细说明

### 1. VRCAvatarPedestal

> "An example of how to create an avatar pedestal that you click on to wear a new avatar using Udon."

- **功能**: 点击 pedestal 切换玩家 Avatar
- **依赖**: `VRC_AvatarPedestal` 组件
- **使用场景**: Avatar 展示厅、试穿点、角色扮演主题世界
- **相关知识**: `memory/api/pickups.md`（Pickup 触发模式）

### 2. VRCChair

> "An example of how to create a chair that you click on to sit in using Udon."

- **路径注意**: 实际是 `VRCChair3`（推测 `VRCChair` 和 `VRCChair2` 已被取代）
- **功能**: 点击就坐
- **依赖**: `VRC_Station` 组件
- **使用场景**: 任何需要"就坐"的世界（咖啡馆、电影院、教室）

### 3. VRCMirror

> "An example of how to create the ever-popular Mirror using Udon."

- **功能**: 实时镜面反射
- **依赖**: `VRC_MirrorReflection` 组件
- **重要**: 最新版 prefab 已正确配置 **Item Layer (3)** 用于反射 Items
- **修复历史**: 老 SDK / 自定义 mirror 不反射 Items（详见 `items.md`）
- **使用场景**: 化妆间、试衣镜、自我观察

### 4. VRCPortalMarker ⚠ 必须场景根

> "An example of how to use [VRC_PortalMarker](/worlds/components/vrc_portalmarker)."

> "This prefab **must** be at the root of your scene hierarchy for the portal's destination instance to be synced with other players."

- **功能**: 跨实例传送门
- **依赖**: `VRC_PortalMarker` 组件
- **关键约束**: ⚠ **必须在场景根（hierarchy root）** 才能正确同步目标实例
- **失败后果**: 嵌套在其他对象下会导致 Portal 实例不同步
- **使用场景**: 多房间世界、世界间跳转、活动入口

### 5. VRCWorld

> "An example of how to use [VRC_SceneDescriptor](/worlds/components/vrc_scenedescriptor) to define a VRChat World."

- **功能**: 场景描述符示例
- **依赖**: `VRC_SceneDescriptor` 组件
- **位置**: 必须场景根
- **使用场景**: 任何 World 的"必备"起点

### 6. VRCVideoSync

> "An example of how to create an Udon-powered [Video Player](/worlds/udon/video-players/)."

**两个变体**:

| 变体 | 后端 | 优势 |
|---|---|---|
| `UdonSyncPlayer (AVPro).prefab` | AVPro | ✅ **支持直播流** |
| `UdonSyncPlayer (Unity).prefab` | Unity VideoPlayer | ✅ **某些场景更稳定** |

- **使用场景**: 电影院、直播活动、视频背景
- **选型决策**:
  - 需要直播 → AVPro
  - 优先稳定性 / 简单 VOD → Unity

### 7. Simple Pen System

> "An example of how to create an Udon-powered pen for drawing in 3D space!"

- **文档**: [Simple Pen System](https://creators.vrchat.com/worlds/examples/udon-example-scene/simple-pen-system/)
- **功能**: 3D 空间绘画
- **使用场景**: 涂鸦世界、白板、签名板、教学标注

### 8. Udon Variable Sync

> "A self-documenting example on how Udon Variable Sync works! Drop it into your world and test it out to see how it works."

- **功能**: 自文档同步机制示例
- **使用场景**: 学习、调试、参考

---

## Analysis — 与现有知识库交叉引用

| 现有知识 | 关联 Prefab |
|---|---|
| `memory/sources/example-central.md` | Example Central 提供更多高级示例 |
| `memory/world/items.md` | VRCMirror 反射 Item 的修复 |
| `memory/world/udon/data-containers/index.md` | VideoSync 可能使用 DataToken 存储 URL |
| `memory/world/creator-economy.md` | Store API 可在 Pedestal 中集成 |
| `memory/api/networking.md` | Udon Variable Sync 演示同步机制 |
| `memory/api/pickups.md` | Pedestal / Chair 都是基于 Pickup/Interactable 模式 |

### Prefab 与 VRC 组件映射

| Prefab | 主要 VRC 组件 | Udon 复杂度 |
|---|---|---|
| VRCAvatarPedestal | VRC_AvatarPedestal | 中 |
| VRCChair | VRC_Station | 低 |
| VRCMirror | VRC_MirrorReflection | 低（无 Udon 逻辑） |
| VRCPortalMarker | VRC_PortalMarker | 中 |
| VRCWorld | VRC_SceneDescriptor | 无（配置型） |
| VRCVideoSync | VRC_SpatialAudioSource + Unity VideoPlayer/AVPro | 高（同步 + 控制） |
| Simple Pen System | 自实现（TrailRenderer / LineRenderer） | 高 |
| Udon Variable Sync | 自实现（演示用） | 中 |

---

## Inference 【推断】

【推断 1】**VRCChair3 是当前版本**——命名为 `3` 表明有 `VRCChair` 和 `VRCChair2` 历史版本，已被取代。

【推断 2】**VRCPortalMarker 必须场景根是网络同步约束**——`VRC_PortalMarker` 内部可能依赖 `NetworkID` 与场景根对象的稳定标识，嵌套在其他 Transform 下可能破坏 Identity 计算。

【推断 3】**VRCMirror 无 Udon 逻辑**——Mirror 反射是 VRChat 客户端原生功能，Udon 主要用于配置 Layer Mask / 距离 / Quality 等参数。

【推断 4】**Simple Pen System 的"高级"体现在轨迹同步**——3D 绘画需要将玩家笔触通过网络同步给其他玩家，涉及多点同步、LineRenderer 重建、对象池等。

【推断 5】**VRCVideoSync 是 Udon 视频同步标准**——尽管有视频播放器(参考工程)等第三方实现更强大，SDK 自带 prefab 是最简起点。

---

## Risks

| 风险 | 严重度 | 说明 |
|---|---|---|
| **VRCPortalMarker 嵌套** | 🔴 高 | 嵌套场景对象下 → Portal 不同步 → 玩家卡在传送门 |
| **老 Mirror 反射失败** | 🟡 中 | 老 SDK mirror 不反射 Item（见 `items.md`） |
| **AVPro 平台兼容** | 🟡 中 | AVPro 在某些 Android 设备可能不稳定 |
| **示例代码即生产** | 🟡 中 | 示例 prefab 是教学用，直接用于生产可能功能不足 |
| **Udon 编译警告** | 🟢 低 | UdonSharp 升级时示例可能产生警告 |

---

## Unknowns & Open Questions

| 编号 | 问题 |
|---|---|
| U-1 | VRCChair3 之前的 VRCChair / VRCChair2 是否仍可在 SDK 中找到？ |
| U-2 | VRCMirror 是否支持 Android (Quest)？ |
| U-3 | Udon Variable Sync 示例是否覆盖 Manual / Continuous / Smooth 三种模式？ |
| U-4 | 是否存在 Simple Pen System 的进阶版本（支持多人协作）？ |
| U-5 | VideoSync 的 Udon 同步带宽占用情况？ |

---

## Recommendations

### 起步阶段

1. **首次开发** 复制 SDK Prefab 到自己的项目目录修改——避免直接修改 SDK Package
2. **Portal Marker** 永远放在场景根——使用 `VRCWorld` Prefab 作为参考结构
3. **Mirror** 使用最新版 prefab——确保 Item 反射支持
4. **Video Player** 根据需求选择 AVPro（直播）或 Unity（VOD）

### 进阶阶段

1. **学习 Example Central**——SDK Prefab 是基础，Example Central 提供更复杂场景
2. **参考视频播放器(参考工程)**——视频播放生产环境应使用视频播放器(`FACT.md` 中已记录架构)
3. **Pen System 升级**——考虑商业插件如 Crayon / Marker Tools
4. **Pedestal 扩展**——集成 Creator Economy 商业 Avatar 展示

### 部署阶段

1. **验证 VRCPortalMarker 在 hierarchy 根**——发布前必检
2. **Mirror 性能**——大场景中 Mirror 数量限制为 2-3 个
3. **Video Player 音频**——使用 VRC_SpatialAudioSource 优化 3D 音频

---

## 引用

- **源页面**: https://creators.vrchat.com/worlds/sdk-prefabs/
- **相关页面**: https://creators.vrchat.com/worlds/components/vrc_portalmarker/
- **相关页面**: https://creators.vrchat.com/worlds/components/vrc_scenedescriptor/
- **相关页面**: https://creators.vrchat.com/worlds/components/vrc_mirrorreflection/
- **相关页面**: https://creators.vrchat.com/worlds/udon/video-players/
- **相关页面**: https://creators.vrchat.com/worlds/examples/udon-example-scene/simple-pen-system/
- **相关知识**: `memory/sources/example-central.md` (更高级示例)
- **相关知识**: `memory/world/creator-economy.md` (Store API 集成)
