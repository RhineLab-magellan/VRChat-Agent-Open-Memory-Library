---
title: "示例包: hai-vr (Haï~ World/Avatar 工具集)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - world
  - avatar
  - hai-vr
  - combo-gesture-expressions

aliases:
  - "Haï~"
  - "Animator As Code"
  - "CGE"
  - "ComboGestureExpressions"
  - "Prefabulous"
  - "dev.hai-vr.vpm"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - world/clientsim/index.md
  - avatar/playable-layers.md
  - avatar/optimization-guide.md
  - hybrid/osc-protocol.md

source: vcc.vrczh.org + upstream hai-vr.github.io/vpm-listing/index.json
source_type: official
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# hai-vr — Haï~ World/Avatar 工具集

> **📦 VPM 仓库速查**:
> - **apiId**: `hai-vr`
> - **上游 URL**: <https://hai-vr.github.io/vpm-listing/index.json>
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/hai-vr>
> - **状态**: ✅ 同步成功 (但 mirror 比 upstream 多 7 个包, 详见 §已知差异)
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/hai-vr> (454967 bytes, 2026-07-01) — **包数 34**
> - Upstream VPM index: <https://hai-vr.github.io/vpm-listing/index.json> (220117 bytes, 2026-07-01) — **包数 27**
> - **包数差异**: mirror 多 7 个包 (注入 VRChat 官方 SDK + hai-vr 子包)
> - **重要**: upstream 有 **UTF-8 BOM** (`0xFEFF`), **mirror 已清理**
> - 顶层 description: 镜像站未提供；upstream 同样为空 (Haï~ 不写顶层描述)

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `hai-vr` |
| **作者** | Haï~ |
| **类型** | Avatar + World 工具集 (跨域) |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/hai-vr> |
| **上游 URL** | <https://hai-vr.github.io/vpm-listing/index.json> |
| **包数量** | **Mirror=34, Upstream=27** (mirror 多 7 个, 详见 §已知差异) |
| **同步状态** | ✅ 同步成功 |
| **文档** | <https://docs.hai-vr.dev> |

---

## 包含的 27 个原生包 (Upstream)

> 来源: upstream index 解析

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `dev.hai-vr.animator-as-code.v1` | Animator As Code (Alpha) | v1.0.9920 | 2019.4 | Base Animator As Code library. This library only requires Unity. |
| 2 | `dev.hai-vr.animator-as-code.v1.vrchat` | Animator As Code - VRChat (Alpha) | v1.0.9920 | 2019.4 | VRChat Avatars extension functions. |
| 3 | `dev.hai-vr.animator-as-code.v1.vrchat-destructive-workflow` | Animator As Code - VRChat (Destructive Workflow) | v1.0.9920 | 2019.4 | Animator As Code - VRChat (Destructive Workflow) |
| 4 | `dev.hai-vr.animator-as-code.v1.ndmf-processor` | Animator As Code - NDMF Processor (Alpha) | v1.0.9920 | 2019.4 | Execute Animator As Code scripts when NDM Framework. |
| 5 | `dev.hai-vr.animator-as-code.v1.modular-avatar` | Animator As Code - Modular Avatar (Alpha) | v1.0.9920 | 2019.4 | Companion library to create Modular Avatar components. |
| 6 | `dev.hai-vr.vcc-dependencies-for-vixen` | Haï~ - VCC Dependencies for Vixen | v0.0.1 | 2019.4 | This package does not contain Vixen, only instructions on which dependencies to pull in VCC. |
| 7 | `dev.hai-vr.view-large-blendtrees` | View large BlendTrees | v1.0.0 | 2019.4 | View large BlendTrees. |
| 8 | `dev.hai-vr.resilience.toolkit` | Haï~ Resilience Toolkit | v1.0.0 | 2019.4 | Resilience Toolkit |
| 9 | `dev.hai-vr.visual-expressions-editor` | Haï~ Visual Expressions Editor | v2.0.0 | 2019.4 | Visual Expressions Editor |
| 10 | `dev.hai-vr.animation-viewer` | Haï~ Animation Viewer | v2.0.0 | 2019.4 | Animation Viewer |
| 11 | `dev.hai-vr.blendshape-viewer` | Haï~ Blendshape Viewer | v2.0.0 | 2019.4 | Blendshape Viewer |
| 12 | `dev.hai-vr.property-finder` | Haï~ Property Finder | v2.0.0 | 2019.4 | Property Finder |
| 13 | `dev.hai-vr.lightbox-viewer` | Haï~ Lightbox Viewer | v2.0.0 | 2019.4 | Lightbox Viewer |
| 14 | `dev.hai-vr.auto-reset-osc-config` | Haï~ Auto-reset OSC config file | v1.1.2 | 2019.4 | Deletes the OSC config file after every avatar upload |
| 15 | `dev.hai-vr.resilience.prefabulous.universal` | Haï~ Prefabulous Universal | v2.0.0 | 2019.4 | Prefabulous Universal |
| 16 | `dev.hai-vr.prefabulous-avatar` | Haï~ Prefabulous Avatar (Alpha) | v1.0.9900 | 2019.4 | Prefabulous Avatar |
| 17 | `dev.hai-vr.prefabulous-vrm-vtubing` | Haï~ Prefabulous for VRM and VTubing | v2.0.0 | 2019.4 | Prefabulous for VRM |
| 18 | `dev.hai-vr.prefabulous-platform-conversions` | Haï~ Prefabulous for Platform Conversions | v2.0.0 | 2019.4 | Prefabulous for Platform Conversions |
| 19 | `dev.hai-vr.cge` | Haï~ ComboGestureExpressions (Beta) | v3.1.5101 | 2019.4 | ComboGestureExpressions |
| 20 | `dev.hai-vr.cge-to-faceemo-converter` | Haï~ Convert ComboGesture to FaceEmo | v0.0.9900 | 2019.4 | Convert ComboGesture to FaceEmo |
| 21 | `dev.hai-vr.denormalized-avatar-exporter` | Haï~ Denormalized Avatar Exporter (Beta) | v1.0.0 | 2019.4 | Denormalized Avatar Exporter |
| 22 | `dev.hai-vr.chillaxins` | Haï~ Chillaxins | v1.0.0 | 2019.4 | Chillaxins |
| 23 | `dev.hai-vr.let-me-see` | Haï~ LetMeSee | v1.0.1 | 2022.3 | Lets you see in VR without entering Play mode. |
| 24 | `dev.hai-vr.external-expressions-menu` | Haï~ External Expressions Menu | v1.0.0-beta.1 | 2019.4 | (description 占位: CHANGEME) |
| 25 | `dev.hai-vr.h-view` | Haï~ App - H-View | v1.0.0 | 2019.4 | (Contains .exe) H-View |
| 26 | `dev.hai-vr.skinned-mesh-constraint` | Haï~ Skinned Mesh Constraint | v1.0.1 | 2019.4 | Constraint a GameObject onto a mesh polygon |
| 27 | `dev.hai-vr.new-avatar-blueprint-ids-in-older-sdks` | Haï~ Generate new Avatar blueprint IDs in older SDKs | v1.0.0 | 2019.4 | (no description) |

---

## 包含的 7 个额外包 (Mirror Only)

> ⚠️ **这些包在 upstream 中不存在**, 是 mirror 同步器注入的:

| # | Package ID | Display Name | 类型 |
|---|------------|--------------|------|
| 1 | `com.vrchat.avatars` | VRChat SDK - Avatars | 注入: VRChat 官方 SDK |
| 2 | `com.vrchat.base` | VRChat SDK - Base | 注入: VRChat 官方 SDK |
| 3 | `com.vrchat.core.vpm-resolver` | VRChat Package Resolver Tool | 注入: VRChat 官方工具 |
| 4 | `com.vrchat.worlds` | VRChat SDK - Worlds | 注入: VRChat 官方 SDK |
| 5 | `dev.hai-vr.basis.avataroptimizer` | HVR Basis AvatarOptimizer | haï-vr 子包 (Unity 6 专用) |
| 6 | `dev.hai-vr.basis.optimizable` | HVR Basis Optimizable | haï-vr 子包 (Unity 6 专用) |
| 7 | `dev.hai-vr.no-thanks` | (推测) | haï-vr 子包 |

**注意**: 4 个 `com.vrchat.*` 注入包**与 curated/official 仓库重复**, VCC 会自动选择最高版本。**2 个 `dev.hai-vr.basis.*` 包仅支持 Unity 6** (2025+ 新包, mirror 已同步)。

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2019.4** | 23/27 | 绝大多数 (兼容老 SDK 3.0) |
| **2022.3** | 1/27 | LetMeSee (其他包未标 2022.3 但实际兼容) |
| **6000.0** | 2/27 (basis.*) | HVR Basis 系列 (Unity 6 专用) |

> **实际兼容情况**: 多数标 2019.4 的包**实际双版本兼容** (2019.4 + 2022.3), 反映 Hai~ 团队的"开发测试版本"标注风格。

---

## 主要包详细说明

### Animator As Code (AAC) - v1.0.9920
- **核心功能**: 编程式生成 Animator Controller + VRChat Avatars 3.0 集成
- **架构**:
  - 基础库 (`animator-as-code.v1`)
  - VRChat 扩展 (`animator-as-code.v1.vrchat`)
  - Destructive Workflow 变体 (`animator-as-code.v1.vrchat-destructive-workflow`)
  - NDMF Processor (`animator-as-code.v1.ndmf-processor`)
  - Modular Avatar 适配器 (`animator-as-code.v1.modular-avatar`)
- **应用场景**: 替代 Animator Controller 拖拽配置, 用 C# 代码生成复杂动画
- **知识库参考**: `memory/avatar/playable-layers.md`

### ComboGestureExpressions (CGE) - v3.1.5101
- **核心功能**: 复杂手势/动作组合菜单系统
- **依赖**: `dev.hai-vr.resilience.toolkit` + 多个 AAC 子包 + `com.vrchat.avatars ^3.3.0`
- **应用场景**: 复杂 Avatar 菜单 (表情/动作组合)
- **知识库参考**: `memory/avatar/playable-layers.md`

### Prefabulous 系列
- **核心功能**: 跨 Avatar Prefab 共享/转换系统
- **子包**:
  - `prefabulous.universal` - 通用 Prefab 共享
  - `prefabulous-avatar` - Avatar 专用 (Alpha)
  - `prefabulous-vrm-vtubing` - VRM/VTuber 平台
  - `prefabulous-platform-conversions` - 平台转换 (VRChat → Resonite)
- **应用场景**: 大型 Avatar 项目 Prefab 复用

### LetMeSee - v1.0.1
- **核心功能**: 在 Unity Editor 中模拟 VR (无需进入 Play mode)
- **应用场景**: Avatar 调试 (大幅提升效率)
- **限制**: 仅 2022.3 支持

### Auto-reset OSC config file - v1.1.2
- **核心功能**: 每次 Avatar 上传后自动删除 OSC 配置文件
- **应用场景**: 防止 OSC 配置漂移
- **知识库参考**: `memory/hybrid/osc-protocol.md`

### HVR Basis 系列 (Unity 6 专用) - v0.0.1
- **核心功能**: Unity 6 平台 Avatar 优化 (Basis Framework)
- **依赖**: `dev.hai-vr.lightbox-viewer >=2.4.1-alpha.2`
- **应用场景**: **未来 Unity 6 项目** (2025+)

---

## 已知差异 (Mirror vs Upstream)

| 维度 | Mirror | Upstream | 说明 |
|------|--------|----------|------|
| 包数量 | **34** | 27 | ⚠️ mirror 多 7 个 (4 VRChat SDK + 3 hai-vr 子包) |
| 顶层 description | 空 | 空 | Haï~ 不写 |
| 包内 description | 完整 | 完整 | ✅ 一致 |
| **BOM 字符** | ✅ **已清理** | ⚠️ **含 UTF-8 BOM** | mirror 自动清理 |
| 字节数 | 454967 | 220117 | ⚠️ **Mirror 比 Upstream 大 2.1 倍** (主要来自注入 SDK 包) |
| 同步状态 | ✅ | ✅ | |

**注入包识别方法**:
- `com.vrchat.*` 4 个包 → 任何 mirror 注入
- `dev.hai-vr.basis.*` 2 个包 → haï-vr 新发布, mirror 已同步
- 任何 `name` 为 `xxx@VPM Repos Synchronizer` 的 repo 顶层 (如 `hai-vr@VPM Repos Synchronizer`) → mirror 元数据覆盖

---

## 必装建议

**Avatar 创作者 (推荐)**:
- `dev.hai-vr.animator-as-code.v1.vrchat` (动画生成)
- `dev.hai-vr.cge` (复杂菜单)
- `dev.hai-vr.prefabulous.universal` (Prefab 共享)

**调试 (推荐)**:
- `dev.hai-vr.let-me-see` (Editor 内 VR 模拟) — **2022.3 专用**

**不要装**:
- `dev.hai-vr.animator-as-code.v1.vrchat-destructive-workflow` (除非明确需要破坏性 workflow)
- `dev.hai-vr.basis.*` (Unity 6 专用, 2022.3 用户无效)

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | 454967 |
| Upstream 字节 | 220117 |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
