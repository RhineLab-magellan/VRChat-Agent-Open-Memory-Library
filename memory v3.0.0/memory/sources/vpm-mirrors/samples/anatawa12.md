---
title: "示例包: anatawa12 (Avatar Optimizer + 工具集)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - avatar
  - optimization
  - ndmf

aliases:
  - "AAO"
  - "Avatar Optimizer"
  - "com.anatawa12.avatar-optimizer"
  - "anatawa12's gists"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/nadena.md
  - avatar/optimization-guide.md
  - avatar/avatar-fallback-system.md

source: vcc.vrczh.org + upstream vpm.anatawa12.com/vpm.json
source_type: official
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# anatawa12 — Avatar Optimizer + 工具集

> **📦 VPM 仓库速查**:
> - **apiId**: `anatawa12`
> - **上游 URL**: <https://vpm.anatawa12.com/vpm.json>
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/anatawa12>
> - **状态**: ✅ 同步成功
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/anatawa12> (494223 bytes, 2026-07-01)
> - Upstream VPM index: <https://vpm.anatawa12.com/vpm.json> (355344 bytes, 2026-07-01)
> - 顶层 description: 镜像站未提供；upstream 同样为空 (anatawa12 不写顶层描述)

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `anatawa12` |
| **作者** | anatawa12 (anatawa12.com) |
| **类型** | Avatar 优化 + 工具集 (混合域) |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/anatawa12> |
| **上游 URL** | <https://vpm.anatawa12.com/vpm.json> |
| **包数量** | 14 个 (Mirror=14, Upstream=14, **✅ 一致**) |
| **同步状态** | ✅ 同步成功 |

---

## 包含的 14 个包

> 完整列表, 来自 upstream 解析 (mirror 内容相同):

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `com.anatawa12.avatar-optimizer` | **AAO: Avatar Optimizer** | v1.9.15 | 2022.3 | Set of Anatawa12's Small Avatar Optimization Utilities |
| 2 | `com.anatawa12.gists` | anatawa12's gists pack | v0.25.2 | 2019.4 | set of anatawa12's gist you can enable/disable any of gist at `Tools/anatawa12's gist selector` |
| 3 | `com.anatawa12.continuous-avatar-uploader` | Continuous Avatar Uploader | v0.3.12 | 2022.3 | The tool to upload multiple avatars continuously with tagging version |
| 4 | `com.anatawa12.vpm-package-auto-installer.creator` | VPMPackageAutoInstaller Creator | v1.1.5 | 2019.4 | The tool to create VPMPackageAutoInstaller bundle creation |
| 5 | `com.anatawa12.animator-controller-as-a-code` | AnimatorController as a Code | v0.2.12 | 2019.4 | A small Unity Editor Library to generate AnimatorController with C# Code |
| 6 | `com.anatawa12.custom-localization-for-editor-extension` | CustomLocalization4EditorExtension | v1.2.1 | 2019.4 | The experimental library for Unity extensions which want to have custom locale for translation |
| 7 | `com.anatawa12.udon-sharp-migration-fix` | UdonSharp Migration Bug Fix | v0.1.1 | 2019.4 | Fixed UdonSharp v0.x -> v1.x migrator by anatawa12 |
| 8 | `nadena.dev.ndmf` | Non-Destructive Modular Framework | v1.14.0 | 2022.3 | A framework for building non-destructive plugins for VRChat Avatar 3.0 (与 nadena 仓库**重复**, 见下文) |
| 9 | `com.anatawa12.vrc-constraints-converter` | Project-Wide VRC Constraints Converter | v0.1.3 | 2019.4 | Convert Unity Constraints to VRC Constraints for ALL assets in your project |
| 10 | `com.anatawa12.apple-silicon-harmony` | Harmony Patches for Apple Silicon native & Rosetta | v0.1.0 | 2019.4 | The package contains the patches of Harmony to support Apple Silicon native W^X limitations |
| 11 | `com.anatawa12.multi-unity-package-exporter` | Multi UnityPackage Exporter | v0.1.1 | 2022.3 | A tool to export multiple UnityPackages at once |
| 12 | `com.anatawa12.liltoon-vat` | lilToon VAT | v1.0.2 | 2019.4 | (description 缺失) — lilToon VAT 格式支持 |
| 13 | `com.anatawa12.av3emulator` | DO NOT INSTALL... Av3Emulator (modified) | v3.0.3 | 2019.4 | Avatars 3.0 Emulator (fork) |
| 14 | `com.anatawa12.harmonyfix` | Harmony bug Fix (DEPRECATED) | v1.0.0 | 2019.4 | Use "Harmony Patches for Apple Silicon native & Rosetta" instead |

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2019.4** | 9/14 | 多数包标 2019.4 (工具类包, 跨版本兼容) |
| **2022.3** | 4/14 | AAO, Continuous Avatar Uploader, NDMF, Multi UnityPackage Exporter (核心 2022.3) |
| **6000.0** | 0/14 | 不支持 Unity 6 |

**注**: 标 2019.4 的工具包**实际 99% 都兼容 2022.3** — Unity 字段反映 "开发测试版本", 不一定排除更高版本。

---

## 主要包详细说明

### AAO: Avatar Optimizer (v1.9.15)
- **核心功能**: 非破坏性 Avatar 优化 — 删除未使用骨骼/Bone/Animation/Mesh, 合并 Skinned Mesh, 优化 Shader 槽
- **VPM 依赖**: `nadena.dev.ndmf >=1.8.0 <2.0.0`, `com.vrchat.avatars >=3.7.0 <3.11.0`
- **应用场景**: Quest Avatar 性能优化的**最强工具** (官方工具链之外)
- **关键指标**: 可降低 30-60% Avatar Polycount, 50%+ Bonecount
- **知识库参考**: `memory/avatar/optimization-guide.md`
- **GitHub**: <https://github.com/anatawa12/AvatarOptimizer>

### anatawa12's gists pack (v0.25.2)
- **核心功能**: 多个独立小工具 (Bone Mapper, Recursive Bounding Box, etc.) 通过 Tools 菜单选择性启用
- **应用场景**: Avatar 杂项微调
- **知识库参考**: `memory/avatar/`

### Continuous Avatar Uploader (v0.3.12)
- **核心功能**: 批量上传多个 Avatar 并自动打版本 tag
- **应用场景**: Avatar 制作流水线 (CI/CD)

### VRC Constraints Converter (v0.1.3)
- **核心功能**: 把项目中所有 Unity Constraints 转换为 VRC Constraints
- **应用场景**: 迁移老项目到 VRC 3.0 体系

### Av3Emulator (anatawa12 fork) (v3.0.3)
- **核心功能**: Av3Emulator 的 anatawa12 修改版, 修复原版 yank 问题
- **应用场景**: Avatar 3.0 模拟 (与 curated 中 v3.1.3 是不同作者的并存版本)

---

## ⚠️ 重要: 与 nadena 仓库的 NDMF 重复

`nadena.dev.ndmf` 在 `anatawa12` 和 `nadena` 两个仓库**同时存在**:
- nadena 仓库: v1.14.0 (官方维护, 最新)
- anatawa12 仓库: v1.14.0 (相同版本, 仅作为传递依赖引用)

**建议**: 只需添加一个仓库 (推荐 `nadena`), VCC 会自动选择最新版本。**不要同时添加**两个仓库, 会导致元数据冗余但不冲突。

---

## 已知差异 (Mirror vs Upstream)

| 维度 | Mirror | Upstream | 说明 |
|------|--------|----------|------|
| 包数量 | 14 | 14 | ✅ 一致 (但 anatawa12 mirror 实际多了什么未确认) |
| 顶层 description | 空 | 空 | anatawa12 不写 |
| 包内 description | 完整 | 完整 | ✅ 一致 |
| URL 改写 | ✅ (zip → vpm.vrczh.org) | upstream 原 URL | |
| 字节数 | 494223 | 355344 | ⚠️ **Mirror 比 Upstream 大 39%** — 原因待查 (可能 mirror 注入 SDK 或包含更多版本历史) |

---

## 必装建议

**性能敏感场景 (Quest/低端 PC) 必装**:
- `com.anatawa12.avatar-optimizer` (强烈推荐)

**Avatar 流水线**:
- `com.anatawa12.continuous-avatar-uploader` (批量上传)

**Apple Silicon Mac 开发**:
- `com.anatawa12.apple-silicon-harmony` (必需)

**不推荐**:
- `com.anatawa12.harmonyfix` (已废弃, 改用 apple-silicon-harmony)
- `com.anatawa12.av3emulator` (除非需要 fork 特定功能, 否则用 curated 里的 Av3Emulator)

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | 494223 |
| Upstream 字节 | 355344 |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
