---
title: "示例包: nadena (Modular Avatar)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - avatar
  - modular-avatar
  - ndmf

aliases:
  - "Modular Avatar"
  - "nadena.dev.modular-avatar"
  - "MA"
  - "NDMF"
  - "Non-Destructive Modular Framework"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/anatawa12.md
  - avatar/playable-layers.md
  - avatar/optimization-guide.md
  - avatar/vrcfury-reference.md

source: vcc.vrczh.org + upstream vpm.nadena.dev/vpm.json
source_type: official
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# nadena — Modular Avatar + NDMF

> **📦 VPM 仓库速查**:
> - **apiId**: `nadena`
> - **上游 URL**: <https://vpm.nadena.dev/vpm.json>
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/nadena>
> - **状态**: ✅ 同步成功
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/nadena> (326412 bytes, 2026-07-01)
> - Upstream VPM index: <https://vpm.nadena.dev/vpm.json> (369587 bytes, 2026-07-01)
> - 顶层 description: 镜像站未提供；upstream 同样为空 (bd_ 不写顶层描述)

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `nadena` |
| **作者** | bd_ (bd_@nadena.dev) |
| **类型** | 核心 Avatar 框架 (必备) |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/nadena> |
| **上游 URL** | <https://vpm.nadena.dev/vpm.json> |
| **包数量** | 4 个 |
| **同步状态** | ✅ 同步成功 |

---

## 包含的 4 个包

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `nadena.dev.modular-avatar` | **Modular Avatar** | v1.17.1 | 2022.3 | A suite of tools for assembling your avatar out of reusable components |
| 2 | `nadena.dev.ndmf` | **Non-Destructive Modular Framework** | v1.14.0 | 2022.3 | A framework for building non-destructive plugins for VRChat Avatar 3.0 |
| 3 | `nadena.dev.misc-vrc-tools` | **bd_'s misc tools** | v0.0.8 | 2022.3 | bd_'s random tools for VRChat |
| 4 | `nadena.dev.modular-avatar.resonite` | **Modular Avatar - Resonite support** | v0.0.47 | 2022.3 | (description 缺失) — Resonite 平台兼容层 |

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2019.4** | 0/4 | ⚠️ **无 2019.4 支持** (但 mirror 解析出 2019.4 是数据问题，见下文) |
| **2022.3** | 4/4 | 全部包都支持 2022.3 — **VRChat 当前主版本 (SDK 3.4.2+)** |
| **6000.0** | 0/4 | 不支持 Unity 6 |

> ⚠️ 注: 我之前用 `getAllRepos` 解析时 Modular Avatar 0.8.0 标的是 2019.4 — 这是 **历史版本** 的 unity 字段。新版本 (1.x) 全部切到 2022.3。

---

## 主要包详细说明

### Modular Avatar (nadena.dev.modular-avatar, v1.17.1)
- **作者**: bd_
- **核心功能**: Avatar 组件化系统, 提供 MA Menu Installer / Merge Armature / Object Toggle / World Constraint / Replace Bone 等组件
- **应用场景**: 几乎所有非平凡 Avatar 都依赖 MA 进行组件化
- **VPM 依赖**: `nadena.dev.ndmf >=1.11.0 <2.0.0-a` (强制)
- **知识库参考**: `memory/avatar/` (Modular Avatar 完整使用)
- **GitHub**: <https://github.com/bdunderscore/modular-avatar>

### Non-Destructive Modular Framework (nadena.dev.ndmf, v1.14.0)
- **作者**: bd_
- **核心功能**: 非破坏性 Avatar 构建框架 — 多个 NDMF 插件按顺序处理 Avatar 而不修改原始 prefab
- **应用场景**: AAO (Avatar Optimizer), HhotateA AvatarPoseLibrary, lilEmo 等数十个包都依赖 NDMF
- **VPM 依赖**: 无 (被依赖方)
- **知识库参考**: `memory/api/udonsharp-runtime.md` (NDMF 执行顺序机制)
- **GitHub**: <https://github.com/bdunderscore/ndmf>

### bd_'s misc tools (nadena.dev.misc-vrc-tools, v0.0.8)
- **作者**: bd_
- **核心功能**: bd_ 的杂项小工具集
- **应用场景**: 调试工具, MA 高级用户

### Modular Avatar - Resonite support (nadena.dev.modular-avatar.resonite, v0.0.47)
- **作者**: bd_
- **核心功能**: 跨平台支持 — 把 MA 生成的 Avatar 导出到 Resonite 平台
- **应用场景**: Resonite 用户 (极少, 主要给跨平台创作者)

---

## 与 VRCFury 关系

nadena Modular Avatar 与 VRCFury **功能有部分重叠** (都是为了简化 Avatar 装配):
- **MA**: 组件化, NDMF 非破坏性, 强制 NDMF 依赖
- **VRCFury**: GUI 工具 + 编程 API, 允许破坏性 workflow
- **选择建议**:
  - 简单 Avatar 装配 → MA (业内主流, 生态更广)
  - 复杂/特殊需求 → VRCFury (灵活度更高)
  - 两者**可共存**, 但同一 Avatar 建议只用一种以避免冲突
- **知识库参考**: `memory/avatar/vrcfury-reference.md` §3 (MA vs VRCFury 决策树)

---

## 已知差异 (Mirror vs Upstream)

| 维度 | Mirror | Upstream | 说明 |
|------|--------|----------|------|
| 包数量 | 4 | 4 | ✅ 一致 |
| 顶层 description | 空 | 空 | bd_ 不写 |
| 包内 description | 完整 | 完整 | ✅ 一致 |
| URL 改写 | ✅ (zip → vpm.vrczh.org) | upstream 原 .zip URL | mirror 改写但 zipSHA256 相同 |
| BOM | 无 | 无 | ✅ 干净 |
| 同步延迟 | ≤ 10 分钟 | 实时 | mirror 滞后 |

---

## 必装建议

**任何 Avatar 项目都建议安装**:
- `nadena.dev.modular-avatar` (必备)
- `nadena.dev.ndmf` (作为依赖自动装)

**扩展 (按需)**:
- `com.anatawa12.avatar-optimizer` (优化, 强推荐)
- `dev.hai-vr.animator-as-code.v1.vrchat` (动画生成)

**Quest 兼容**:
- MA 全部包只支持 2022.3, **Quest 端完全兼容** (但注意 Quest 平台 Avatar 性能约束)

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | 326412 |
| Upstream 字节 | 369587 |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
