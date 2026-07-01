---
title: "示例包: lilxyzw (lilToon + 工具集)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - avatar
  - shader
  - liltoon

aliases:
  - "lilToon"
  - "lilxyzw"
  - "io.github.lilxyzw.vpm"
  - "lilAvatarUtils"
  - "lilycalInventory"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/poiyomi.md
  - avatar/shader/index.md
  - avatar/shader/liltoon/index.md
  - avatar/optimization-guide.md

source: vcc.vrczh.org + upstream lilxyzw.github.io/vpm-repos/vpm.json
source_type: official
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# lilxyzw — lilToon + Avatar 工具集

> **📦 VPM 仓库速查**:
> - **apiId**: `lilxyzw`
> - **上游 URL**: <https://lilxyzw.github.io/vpm-repos/vpm.json> (GitHub Pages, 国内偶尔抽风)
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/lilxyzw>
> - **状态**: ✅ 同步成功
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/lilxyzw> (75732 bytes, 2026-07-01)
> - Upstream VPM index: <https://lilxyzw.github.io/vpm-repos/vpm.json> (77930 bytes, 2026-07-01)
> - **重要**: upstream 有 **UTF-8 BOM** (`0xFEFF`), **mirror 已清理** — 程序读取时需注意

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `lilxyzw` |
| **作者** | lilxyzw |
| **类型** | Avatar Shader (lilToon) + Avatar 工具集 |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/lilxyzw> |
| **上游 URL** | <https://lilxyzw.github.io/vpm-repos/vpm.json> (GitHub Pages, 国内偶尔抽风) |
| **包数量** | 9 个 (Mirror=9, Upstream=9, **✅ 一致**) |
| **同步状态** | ✅ 同步成功 |

---

## 包含的 9 个包

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `jp.lilxyzw.liltoon` | **lilToon** | v1.3.7 | 2018.1 | Feature-rich toon shader. |
| 2 | `jp.lilxyzw.lilavatarutils` | lilAvatarUtils | v1.0.0 | 2019.4 | Utilities for avatar modification. |
| 3 | `jp.lilxyzw.lilycalinventory` | lilycalInventory | v1.0.0 | 2019.4 | Modify avatar at build time. |
| 4 | `jp.lilxyzw.lileditortoolbox` | lilEditorToolbox | v0.1.0 | 2022.3 | Extensions for Unity Editor. |
| 5 | `jp.lilxyzw.lilndmfmeshsimplifier` | lilNDMFMeshSimplifier | v0.2.0 | 2022.3 | Simplify meshes at build time. (VPM 依赖 `nadena.dev.ndmf ^1.5.0`) |
| 6 | `jp.lilxyzw.liloutlinesmoother` | lilOutlineSmoother | v1.0.0 | 2022.3 | Smooth outline normals. (VPM 依赖 `nadena.dev.ndmf ^1.5.0`) |
| 7 | `jp.lilxyzw.lilanythingreplacer` | lilAnythingReplacer | v1.0.0 | 2022.3 | Replace references at build time. (VPM 依赖 `nadena.dev.ndmf ^1.5.0`) |
| 8 | `jp.lilxyzw.lilpbr` | lilPBR | v1.0.0 | 2022.3 | PBR Shaders |
| 9 | `jp.lilxyzw.lilemo` | lilEmo | v1.0.0 | 2022.3 | A non-destructive plugin for creating avatar facial expressions. (VPM 依赖 `nadena.dev.modular-avatar ^1.14`) |

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2018.1** | 1/9 | lilToon 主包 (最广兼容, 支持 2018 LTS 起) |
| **2019.4** | 2/9 | lilAvatarUtils, lilycalInventory |
| **2022.3** | 6/9 | 大部分 2022 LTS 工具包 |
| **6000.0** | 0/9 | 不支持 Unity 6 |

**注**: lilToon 标 2018.1 但**实际支持 2019.4/2022.3** (向下兼容设计)。但 Unity 6 需等 2.x 系列。

---

## 主要包详细说明

### lilToon (jp.lilxyzw.liltoon, v1.3.7)
- **核心功能**: 业内主流卡通渲染 Shader
- **特性**: PBR 兼容, Outline, MatCap, 颜色混合, 阴影模式, 8 灯光支持, VRChat Light Volumes 兼容
- **应用场景**: 几乎所有日式 VRChat Avatar 头部/服装
- **知识库参考**: `memory/avatar/shader/liltoon/index.md` (16 个详细文档)
- **文档**: <https://lilxyzw.github.io/lilToon/>

### lilAvatarUtils (v1.0.0)
- **核心功能**: Avatar 修改工具集 (菜单生成, 骨骼映射, Mesh 合并等)
- **应用场景**: Avatar 制作辅助

### lilycalInventory (v1.0.0)
- **核心功能**: Avatar 物品切换 (衣服/配饰), 网格化菜单配置
- **应用场景**: 复杂 Avatar 物品管理
- **关联**: 与 MA 的 Merge Armature 配合使用

### lilNDMFMeshSimplifier (v0.2.0)
- **核心功能**: NDMF 阶段简化 Mesh (LOD 生成, 顶点合并)
- **VPM 依赖**: `nadena.dev.ndmf ^1.5.0` (强制)
- **应用场景**: Quest 平台 Avatar 性能优化

### lilEmo (v1.0.0)
- **核心功能**: 非破坏性 Avatar 表情系统
- **VPM 依赖**: `nadena.dev.modular-avatar ^1.14` (强制)
- **应用场景**: Avatar 表情菜单配置

---

## 已知差异 (Mirror vs Upstream)

| 维度 | Mirror | Upstream | 说明 |
|------|--------|----------|------|
| 包数量 | 9 | 9 | ✅ 一致 |
| 顶层 description | 空 | 空 | lilxyzw 不写 |
| 包内 description | 完整 | 完整 | ✅ 一致 |
| **BOM 字符** | ✅ **已清理** | ⚠️ **含 UTF-8 BOM** | 程序读取需 strip, 否则 JSON.parse 失败 |
| 字节数 | 75732 | 77930 | mirror 小 ~2.8% (BOM 移除贡献) |
| URL 改写 | ✅ | 原 URL | |

---

## Shader 选型建议 (lilToon vs Poiyomi)

| 维度 | lilToon | Poiyomi Toon |
|------|---------|--------------|
| 主流度 | ⭐⭐⭐⭐⭐ (日式主流) | ⭐⭐⭐⭐ (欧美主流) |
| 性能 | ⭐⭐⭐⭐ (Quest 兼容较好) | ⭐⭐ (Pro 版 Quest 较慢) |
| 渲染特性 | 卡通优先, PBR 兼容 | 全功能 (Toon/Pro 切换) |
| 学习曲线 | 中等 | 中等偏高 |
| 国内访问 | ✅ (mirror) | ⚠️ (mirror 同步失败, 需用 upstream) |
| 文档 | ✅ 完整官方文档 (日/英) | ✅ 完整官方文档 |
| 兼容 | URP/HDRP/BRP | URP/HDRP/BRP |

**国内用户建议**:
- ✅ 优先 lilToon (mirror 稳定)
- ⚠️ Poiyomi mirror 同步失败, 需用 upstream `https://poiyomi.github.io/vpm/index.json`

---

## 必装建议

**Avatar 创作者 (必备)**:
- `jp.lilxyzw.liltoon` (必备)

**Avatar 性能优化**:
- `jp.lilxyzw.lilndmfmeshsimplifier` + `nadena.dev.ndmf` (Quest 优化)

**Avatar 物品管理**:
- `jp.lilxyzw.lilycalinventory` + `nadena.dev.modular-avatar` (复杂 Avatar)

**不需要**:
- `jp.lilxyzw.liloutlinesmoother` (效果与 lilToon 自带 Outline 重叠)

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | 75732 |
| Upstream 字节 | 77930 |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
