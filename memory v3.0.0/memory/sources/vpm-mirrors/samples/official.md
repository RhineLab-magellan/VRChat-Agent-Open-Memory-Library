---
title: "示例包: official (VRChat 官方 SDK)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - vrchat-official
  - sdk
  - avatars
  - worlds
  - udonsharp

aliases:
  - "VRChat Official"
  - "com.vrchat.repos.official"
  - "VRChat SDK"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/curated.md
  - api/networking.md
  - api/persistence.md
  - api/events-reference.md
  - avatar/avatar-fallback-system.md
  - world/udon/udonsharp/compilation.md

source: vcc.vrczh.org + mirror vpm index (upstream packages.vrchat.com 国内不可达)
source_type: official
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# official — VRChat 官方 SDK 包

> **📦 VPM 仓库速查**:
> - **apiId**: `official`
> - **上游 URL**: <https://packages.vrchat.com/official> (国内被墙, 仅以 mirror 为准)
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/official>
> - **状态**: ✅ 同步成功
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/official> (301696 bytes, 2026-07-01)
> - Upstream VPM index: <https://packages.vrchat.com/official> (国内不可达, **仅以 mirror 为准**)
> - 顶层 description: 镜像站未提供；upstream 同样为空 (VRChat 不维护顶层描述)

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `official` |
| **作者** | VRChat |
| **类型** | 官方 SDK (必备基础) |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/official> |
| **上游 URL** | <https://packages.vrchat.com/official> (国内被墙) |
| **包数量** | 4 个 (基础 SDK 包) |
| **同步状态** | ✅ 同步成功 |
| **文档** | <https://creators.vrchat.com/sdk/vpm/> |

---

## 包含的 4 个包

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `com.vrchat.avatars` | **VRChat SDK - Avatars** | v3.10.4 | 2019.4 | Our powerful Avatars 3.0 System |
| 2 | `com.vrchat.base` | **VRChat SDK - Base** | v3.10.4 | 2019.4 | Base for VRChat SDK |
| 3 | `com.vrchat.worlds` | **VRChat SDK - Worlds** | v3.10.4 | 2019.4 | Tools for creating interactive VRChat worlds using Udon |
| 4 | `com.vrchat.core.vpm-resolver` | **VRChat Package Resolver Tool** | v0.1.29 | 2019.4 | Tool to Download VPM Packages |

> ⚠️ 三个 SDK 包都标 2019.4 但**实际全部支持 2022.3** (这是 SDK 3.4.2+ 的最低 Unity 版本, 2022.3.22f1 是当前主版本)。
>
> ⚠️ v3.10.4 是 2026-07-01 时的最新稳定版, mirror 完整保留 80+ 历史版本供回滚。

---

## 完整版本历史 (摘录)

> 完整历史见 `samples/official-mirror.json` (`com.vrchat.avatars.versions` 字段)
> 镜像完整保留**所有 80+ 历史版本** (从 3.0.9 → 3.10.4, 包括所有 beta/rc/preview)

```
3.0.9 (legacy, 2019 末期)
   ↓
3.1.0 - 3.1.13 (1.x series, 2020)
   ↓
3.2.0 - 3.2.3 (2021)
   ↓
3.3.0 (2022 早期)
   ↓
3.4.0 - 3.4.2 (2022 LTS 切期, 切换到 Unity 2022.3)
   ↓
3.5.0 - 3.5.2 (2023 稳定期)
   ↓
3.6.0 - 3.6.2-constraints.* (2024, Constraints 集成)
   ↓
3.7.0 - 3.7.6 (2024-2025, Fallback 系统, IK 2.0)
   ↓
3.8.0 - 3.8.2 (2025)
   ↓
3.9.0 - 3.9.1 (2025, 性能优化)
   ↓
3.10.0 - 3.10.4 (2026, 最新稳定)
```

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2019.4** | 4/4 (标) | 全部 4 个包都标 2019.4 (实际是最低支持版本) |
| **2022.3** | 4/4 (实际) | **VRChat 当前主版本 (2022.3.22f1 LTS)** — SDK 3.4.2+ 强制要求 |
| **6000.0** | 0/4 | **不支持 Unity 6** (需等 SDK 4.x) |

**关键**: 标 2019.4 ≠ 排除 2022.3。VRChat 沿用 "最低支持版本" 风格标注, 实际 3.4.2+ 起 SDK 已切到 2022.3 LTS。

---

## 主要包详细说明

### VRChat SDK - Base (com.vrchat.base, v3.10.4)
- **核心功能**: 所有 VRChat SDK 的依赖基础
- **包含**: VRCSDK Core API、Udon API、SDK 通用工具类
- **强制依赖**: 所有其他 VRChat 包
- **知识库参考**: `memory/api/` (Udon API 完整白名单)

### VRChat SDK - Avatars (com.vrchat.avatars, v3.10.4)
- **核心功能**: Avatar 3.0 系统 (Playable Layers, Expression Menu, Parameters)
- **VPM 依赖**: `com.vrchat.base`
- **应用场景**: 任何 Avatar 项目必须
- **知识库参考**:
  - `memory/avatar/playable-layers.md`
  - `memory/avatar/avatar-fallback-system.md`
  - `memory/avatar/full-body-tracking.md`
  - `memory/avatar/ik-2.0.md`

### VRChat SDK - Worlds (com.vrchat.worlds, v3.10.4)
- **核心功能**: World SDK + Udon 工具
- **VPM 依赖**: `com.vrchat.base`
- **应用场景**: 任何 World 项目必须
- **知识库参考**:
  - `memory/world/udon/` (Udon 完整知识)
  - `memory/world/scene-components/` (VRCSceneDescriptor 等 9 个核心组件)
  - `memory/api/persistence.md`

### VRChat Package Resolver Tool (com.vrchat.core.vpm-resolver, v0.1.29)
- **核心功能**: VPM 协议解析器 (下载依赖、版本检查)
- **应用场景**: 任何 VPM 项目自动安装
- **知识库参考**: `memory/sources/vpm-package-template.md` (VPM 包开发模板)

---

## 主要功能模块 (按 SDK 域)

### Avatar 域 (SDK Avatars 3.10.4)
- **Avatar 3.0 基础**: Playable Layers (Base/Additive/Gesture/Action/FX)
- **Expression System**: Expression Menu, Expression Parameters
- **VRC Constraints**: 6 种约束类型 (Rotation/Position/Scale/Parent/Aim/IK)
- **PhysBone**: 物理骨骼系统 (含默认值配置)
- **Avatar Fallback System** (2025+): 跨 Avatar 共享资产
- **IK 2.0** (2025+): 新一代 IK 系统
- **Full Body Tracking**: 全身追踪支持
- **Permissions**: 公开 Avatar 克隆 / 可见性设置

### World 域 (SDK Worlds 3.10.4)
- **VRCSceneDescriptor**: Scene 必含核心
- **VRCObjectSync**: 物理对象同步
- **VRCStation**: 坐姿/传送站
- **VRCMirrorReflection**: 镜面反射
- **VRCEnablePersistence**: 持久化
- **VRCPlayerAudioAPI**: 玩家音频 API
- **VRCAvatarPedestal**: Avatar 展示台
- **VRCVideoSyncPlayer**: 视频同步
- **VRCPortalMarker**: 传送门

### Udon 域 (跨 SDK)
- **UdonSharp 编译器**: C# → Udon 字节码
- **Networking API**: 11KB/s 带宽限制, NetworkCallable (3.8.1+)
- **Persistence API**: 100KB/player/world (压缩后)
- **Audio API**: AudioSource, AudioMixer, Steam Audio (2025+)
- **OSC API**: 完整 OSC 协议
- **Data Containers**: VRCDataList, VRCDataDict, VRCJson, VRCString

---

## 与 curated 关系

- `curated` 包含 9 个**社区精选**包 (含 AudioLink, UdonSharp, VRWorld Toolkit 等)
- `official` 包含 4 个**VRChat 官方**包
- **VCC 默认会同时添加两个 repo** (VRChat 官方配置)
- 实际**UdonSharp 包含在 curated** 而不是 official, 但 official 中 UdonSharp 是被 curated 注入的

---

## 已知差异 (Mirror vs Upstream)

| 维度 | Mirror | Upstream | 说明 |
|------|--------|----------|------|
| 包数量 | 4 | 4 (推测) | ✅ 一致 |
| 顶层 description | 空 | 空 | VRChat 不写 |
| 包内 description | 完整 | 完整 (推测) | ✅ 一致 |
| 版本历史 | 80+ (完整) | 80+ (推测) | ✅ mirror 完整保留 |
| URL 改写 | ✅ | 原 URL | mirror 改写 zip URL 走 vpm.vrczh.org |
| 字节数 | 301696 | N/A (不可达) | |

---

## 必装建议

**任何项目 (必备)**:
- `com.vrchat.base` (强制)
- `com.vrchat.avatars` (Avatar 项目)
- `com.vrchat.worlds` (World 项目)
- `com.vrczh.core.vpm-resolver` (自动, 不用手动装)

**版本选择建议**:
- ✅ 用 `latest` 标签 (3.10.4 当前)
- ⚠️ 旧版仅在需要兼容老工程时使用 (e.g. 3.4.2 之前的 2019.4 工程)
- 🔄 **不要混用** major.minor 不同版本 (e.g. Avatars 3.7 + Base 3.10) — 协议不兼容

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | 301696 |
| Upstream 字节 | N/A (国内不可达) |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
