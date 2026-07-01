---
title: "示例包: poiyomi (Poiyomi Shader)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - avatar
  - shader
  - poiyomi

aliases:
  - "Poiyomi"
  - "Poiyomi Toon Shader"
  - "Poiyomi Pro"
  - "io.github.poiyomi.vpm"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/lilxyzw.md
  - avatar/shader/index.md
  - avatar/shader/poiyomi/index.md
  - reviews/poiyomi-integration-plan-2026-07-01.md

source: vcc.vrczh.org (mirror) + upstream poiyomi.github.io/vpm/index.json + Poiyomi 10.0 官方文档(2026-07-01)
source_type: official
version: 0.2 (示例流程 + 10.0 演进)
last_review: 2026-07-01
confidence: High
---

# poiyomi — Poiyomi Shader (同步失败的示例)

> **📦 VPM 仓库速查**:
> - **apiId**: `poiyomi`
> - **上游 URL**: <https://poiyomi.github.io/vpm/index.json> (GitHub Pages, **必须用此源**, mirror 失败)
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/poiyomi> ⚠️ **同步失败, 国内不可用**
> - **状态**: 🔴 **同步失败** — 请使用上游 URL 添加到 VCC
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/poiyomi> — ⚠️ **0 bytes, 同步失败**
> - Upstream VPM index: <https://poiyomi.github.io/vpm/index.json> (37945 bytes, 2026-07-01) — **使用此源**
> - 顶层 description: 镜像站未提供；upstream 同样为空 (Poiyomi 不写顶层描述)

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `poiyomi` |
| **作者** | Poiyomi |
| **类型** | Avatar Shader (Poiyomi Toon / Pro) |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/poiyomi> ⚠️ **同步失败, 国内不可用** |
| **上游 URL** | <https://poiyomi.github.io/vpm/index.json> (GitHub Pages, 国内偶尔抽风) |
| **包数量** | 2 个 (Upstream) |
| **同步状态** | 🔴 **同步失败** (lastError 未公开, 推测: GitHub Pages 反爬 或 非标 VPM 格式) |

---

## 包含的 2 个包 (Upstream)

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `com.poiyomi.toon` | **Poiyomi Toon Shader** | v8.1.166 | 2019.4 | Feature-rich shaders for Unity and VRChat. |
| 2 | `com.poiyomi.pro` | **Poiyomi Pro** | v9.3.66 | 2019.4 | Poiyomi Pro shaders. Downloads after authenticating with Patreon ($10+ tier). |

> ⚠️ **Poiyomi Pro 需要 Patreon $10+ 订阅认证** — 镜像站无法镜像 Pro 包的鉴权流, 即便 mirror 同步成功也**不能下载 Pro 内容**。Mirror 失败可能与此无关 (但说明镜像对 Pro 包存在天然限制)。

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2019.4** | 2/2 | 两个包都标 2019.4 (实际兼容 2022.3) |
| **2022.3** | 0/2 (标) | 实际兼容 2022.3 (Poiyomi 团队维护双版本) |
| **6000.0** | 0/2 | 不支持 Unity 6 |

---

## 主要包详细说明

### Poiyomi Toon Shader (v8.1.166)
- **核心功能**: 业内主流 Shader 之一, 8.x 系列为免费 Toon
- **特性**: Toon/PBR 切换, 视频纹理, 渐变遮罩, 大量参数, 兼容绝大部分 VRChat Avatar
- **应用场景**: 欧美主流 Avatar, 服装, 配饰
- **文档**: <https://poiyomi.com/>

### Poiyomi Pro (v9.3.66)
- **核心功能**: Pro 增强版, 包含 9.x 系列的额外效果 (Lighting、Tessellation 等)
- **获取**: Patreon $10+ 订阅 → Discord 鉴权 → 下载 Pro 版
- **应用场景**: 商业 Avatar, 高端定制
- **知识库参考**: `memory/hybrid/osc-protocol.md` (Poiyomi Pro 集成示例)

---

## ⚠️ 同步失败分析与解决

### 失败原因推测

mirror 同步任务 (cron `*/10 * * * *`) 持续失败的可能原因:
1. **GitHub Pages 反爬**: Poiyomi 的 VPM index 可能在某次更新后设置了非标准 CORS 头, Deno Deploy 的 fetch 失败
2. **JSON 格式校验**: Poiyomi 的 index 包含自定义字段, Deno 端 schema 校验失败
3. **Pro 包鉴权问题**: Poiyomi Pro 需要 token, mirror 端无 token → 整个 index 解析失败

### 解决建议

**短期方案**: 直接用 upstream
```
VCC → Add Repository → https://poiyomi.github.io/vpm/index.json
```

**长期方案**: 等待 vrczh 维护者修复 (无 ETA)

**替代源**:
- ALCOM 内置源: ALCOM 自带的 VPM 列表可能已含 Poiyomi
- 手动下载: 从 Poiyomi 官网下载 .unitypackage, 直接拖入 Unity

---

## 已知差异 (Mirror vs Upstream)

| 维度 | Mirror | Upstream | 说明 |
|------|--------|----------|------|
| 包数量 | **0** (同步失败) | 2 | 🔴 严重不同步 |
| 顶层 description | N/A | 空 | Poiyomi 不写 |
| 包内 description | N/A | 完整 | upstream 可用 |
| 字节数 | 0 | 37945 | mirror 完全空 |
| 同步状态 | 🔴 status=2 | ✅ | mirror API 报告 `syncStatus.status=2` |

---

## Shader 选型建议 (Poiyomi vs lilToon)

| 维度 | Poiyomi | lilToon |
|------|---------|---------|
| 主流地区 | 欧美 | 日式/亚洲 |
| 免费版本 | 8.x Toon | 1.x 全部 |
| 付费版本 | 9.x Pro (Patreon) | 无 |
| 国内访问 | ⚠️ (mirror 失败) | ✅ (mirror OK) |
| 性能 | 中等 (Pro Quest 较慢) | 较好 (Quest 兼容) |
| 文档完整度 | ✅ 中英 | ✅ 日英 |

**国内用户建议**:
- ❌ Poiyomi mirror 同步失败, 需配置 upstream (GitHub Pages 国内慢)
- ✅ 改用 lilToon (mirror 稳定, 国内访问快)

---

## 10.0 版本演进(NEW 2026-07-01)

> 2026-07-01 完整下载 Poiyomi 官方文档(v10.0)后,补充本节。

### 10.0 关键变化

| 维度 | 9.x | 10.0 |
|------|------|------|
| **架构** | 传统 Shader Lab | Shader Graph 9.x+ Pro 基础 |
| **变体** | 1-2 个 | 5 个分级(Nano/Micro/Mega/Giga/Tera) |
| **Modular Shader System** | ❌ | ✅ (Pro 专属) |
| **Lighting Type** | 几种 | 9 种 |
| **AudioLink 集成** | 基础 | 完整 + AL Spectrum + AL Volume Color |
| **VPM 实际包版本** | 9.3.66 (Pro) | 仍可能 9.3.x(10.0 文档先行) |

### 10.0 文档"分阶段推出"风险

> ⚠️ **重要**: Poiyomi 10.0 文档声明"正在分阶段推出"。这意味着:
> - 文档中描述的某些功能**实际可能尚未在 VPM 包中提供**
> - VPM 实际可用版本可能仍为 9.3.x
> - 建议**双轨验证**:文档查功能 + 实际安装查 VPM 包

### 知识库完整入库(2026-07-01)

| 项目 | 数量 | 位置 |
|------|------|------|
| **原始数据 .md** | 65 | `参考文献/Poiyomi/` |
| **主题知识文档** | 8 | `memory/avatar/shader/poiyomi/` |
| **整合计划** | 1 | `memory/reviews/poiyomi-integration-plan-2026-07-01.md` |

**主题文档清单**:
- `index.md` - Poiyomi 知识库总览
- `installation.md` - 安装与版本
- `shader-variants.md` - 5 变体详解
- `audiolink-integration.md` - AudioLink 集成
- `modular-system.md` - Modular Shader System (Pro)
- `shading-styles.md` - 9 种 Lighting Type
- `quest-optimization.md` - Quest 优化策略
- `pro-vs-toon.md` - Pro vs Toon 边界
- `comparison-liltoon.md` - Poiyomi vs lilToon

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | **0** (同步失败) |
| Upstream 字节 | 37945 |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
