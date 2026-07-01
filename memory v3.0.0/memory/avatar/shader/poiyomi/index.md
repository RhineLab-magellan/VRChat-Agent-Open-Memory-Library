---
title: "Poiyomi Shaders 知识库索引"
category: avatar
subcategory: shader
poiyomi_subdir: true
knowledge_level: applied
status: active
source: "本地知识库整理(2026-07-01) + Poiyomi 官方文档 v10.0 完整入库"
source_type: official
version: 1.0
upstream_version: 10.0
last_review: 2026-07-01
confidence: High
tags:
  - avatar
  - shader
  - poiyomi
  - index
  - navigation
  - knowledge-base
aliases:
  - "Poiyomi KB"
  - "Poiyomi Knowledge Base"
  - "Poiyomi 索引"
related:
  - "./installation.md"
  - "./shader-variants.md"
  - "./audiolink-integration.md"
  - "./modular-system.md"
  - "./shading-styles.md"
  - "./quest-optimization.md"
  - "./pro-vs-toon.md"
  - "./comparison-liltoon.md"
  - "../../../../参考文献/Poiyomi/INDEX.md"
  - "../../../../参考文献/Poiyomi/00-introduction.md"
  - "../index.md"
---

# Poiyomi Shaders 知识库索引

> **Domain**: Avatar → Shader → Poiyomi
> **完整入库时间**: 2026-07-01
> **状态**: 活跃(Active)
> **总文档数**: 8 个主题知识 + 65 个原始参考(链接)

---

## 1. 概述

本知识库收录 Poiyomi Shaders 的**结构化知识**,由 65 个官方原始文档提炼而来。原始数据保留在 `参考文献/Poiyomi/`,本目录提供**主题化、可决策的知识**。

**Poiyomi 是什么**: VRChat Avatar 主流 Toon Shader,与 lilToon 并列第一梯队。5 个变体(Nano→Tera)覆盖 PC→Quest 全部场景。

---

## 2. 快速导航

| 文档 | 主题 | 何时阅读 |
|------|------|----------|
| **[installation.md](./installation.md)** | 安装与版本 | 第一次安装 / 版本升级时 |
| **[shader-variants.md](./shader-variants.md)** | 5 变体详解 | 选择变体时 |
| **[audiolink-integration.md](./audiolink-integration.md)** | AudioLink 集成 | 制作音乐 Avatar |
| **[modular-system.md](./modular-system.md)** | Modular Shader System(Pro) | 团队/复杂 Avatar |
| **[shading-styles.md](./shading-styles.md)** | 9 种 Lighting Type | 选择阴影风格 |
| **[quest-optimization.md](./quest-optimization.md)** | Quest 优化策略 | 制作 Quest Avatar |
| **[pro-vs-toon.md](./pro-vs-toon.md)** | Pro vs Toon 边界 | 决定是否订阅 |
| **[comparison-liltoon.md](./comparison-liltoon.md)** | Poiyomi vs lilToon | 选择 Shader 时 |

---

## 3. 决策树(快速入口)

### 3.1 我应该用 Poiyomi 吗?

```
你的 Avatar 需求?
│
├─ 想要风格化 Toon + 高级 VFX(星空/几何)
│   └─ ✅ Poiyomi Pro
│
├─ 想要 Modular Shader System(团队协作)
│   └─ ✅ Poiyomi Pro
│
├─ 想要 9 种 Lighting Type
│   └─ ✅ Poiyomi
│
├─ 想要 5 个变体分级(Quest 优化)
│   └─ ✅ Poiyomi
│
├─ 想要开源 + 免费 + 大量预设
│   └─ ❌ 改用 lilToon
│
└─ 想要 UV 服装切换零 Draw Call
    └─ ❌ 改用 SCSS
```

### 3.2 第一次安装 Poiyomi

1. 读 **[installation.md](./installation.md)** - 安装与版本
2. 读 **[pro-vs-toon.md](./pro-vs-toon.md)** - 决定 Toon 还是 Pro
3. 读 **[shader-variants.md](./shader-variants.md)** - 选择变体
4. 如做 Quest,读 **[quest-optimization.md](./quest-optimization.md)**

### 3.3 制作音乐 Avatar

1. 读 **[audiolink-integration.md](./audiolink-integration.md)**
2. 确认 World 端有 AudioLink Controller
3. 启用 Material 的 AudioLink Toggle
4. 调 5 频段参数

### 3.4 团队/工作室

1. 读 **[modular-system.md](./modular-system.md)**
2. 规划共享材质池
3. 创建自定义模块(Pro)
4. 用 Global Themes 做主题切换

---

## 4. 知识库结构

```
memory/avatar/shader/poiyomi/         ← 本知识库(提炼知识)
├── index.md                          ← 本文件
├── installation.md                   ← 安装与版本
├── shader-variants.md                ← 5 变体详解
├── audiolink-integration.md          ← AudioLink 集成
├── modular-system.md                 ← Modular Shader System (Pro)
├── shading-styles.md                 ← 9 种 Lighting Type
├── quest-optimization.md             ← Quest 优化
├── pro-vs-toon.md                    ← Pro vs Toon 边界
└── comparison-liltoon.md             ← Poiyomi vs lilToon

参考文献/Poiyomi/                     ← 原始数据(65 个 .md)
├── INDEX.md                          ← 原始数据主索引
├── 00-introduction.md
├── 01-download-install.md
├── 02-render-preset.md
├── ... (共 65 个文档)
└── 64-tps-wizard.md
```

---

## 5. 关键概念速查

### 5.1 5 个变体

| 变体 | 平台 | 推荐度 |
|------|------|--------|
| **Nano** | PC + Quest | 性能极致 |
| **Micro** | Quest 首选 | ⭐⭐⭐⭐ |
| **Mega** | PC 通用 | ⭐⭐⭐⭐⭐ |
| **Giga** | PC 高端 | ⭐⭐⭐ |
| **Tera** | 顶级 PC | ⭐⭐ |

详见 **[shader-variants.md](./shader-variants.md)**

### 5.2 Pro vs Toon 关键差异

| 功能 | Toon | Pro |
|------|------|-----|
| Modular Shader System | ❌ | ✅ |
| Poiyomi Fur 1-31 层 | ❌ | ✅ |
| ShatterWave / Geometric Dissolve | ❌ | ✅ |
| Constellation / Voronoi 3D | ❌ | ✅ |
| Global Themes (4 主题) | ❌ | ✅ |
| 完整 9 Lighting Type | ⚠️ 基础 | ✅ 完整 |

详见 **[pro-vs-toon.md](./pro-vs-toon.md)**

### 5.3 AudioLink 三件套

| 组件 | 复杂度 | 适用 |
|------|--------|------|
| 基础 AudioLink (5 频段) | ⭐ | 缩放/发光 |
| AL Spectrum | ⭐⭐⭐ | 频谱图案 |
| AL Volume Color | ⭐⭐ | 颜色波形 |

详见 **[audiolink-integration.md](./audiolink-integration.md)**

---

## 6. Quest Avatar 速查

详见 **[quest-optimization.md](./quest-optimization.md)**

**硬性规则**:
- ✅ 必须用 **Micro 或 Nano** 变体
- ❌ 禁用 Grab Pass / ShatterWave / Geometric Dissolve
- ❌ 禁用 Voronoi 3D / Constellation / Internal Parallax
- ⚠️ AudioLink 限 4 频段
- ⚠️ Material 数量 ≤ 5

**推荐工具**:
- EasyQuestSwitch(自动 PC/Quest 切换)
- Avatar Compressor (LAC)(纹理压缩)
- Avatar Optimizer (AAO)(通用优化)

---

## 7. 9 种 Lighting Type

详见 **[shading-styles.md](./shading-styles.md)**

| # | 类型 | 风格 |
|---|------|------|
| 1 | Texture Ramp | 卡通 |
| 2 | Multilayer Math | 复杂卡通 |
| 3 | Wrapped | 柔和 |
| 4 | Skin | 皮肤 |
| 5 | ShadeMap | 风格化 |
| 6 | Flat | 2D |
| 7 | Realistic | PBR |
| 8 | Cloth | 织物 |
| 9 | SDF | 距离场 |

**注意**: 2/9 完整(Texture Ramp + Multilayer Math),7/9 推断(详情子页面 404)

---

## 8. Pro 鉴权流程

详见 **[installation.md §5](./installation.md#5-pro-鉴权流程patreon-10)**

```
Patreon $10+/月 → Discord 绑定 → #pro-downloads 下载 → Import 到 Unity
```

---

## 9. 与其他 Shader 对比

详见 **[comparison-liltoon.md](./comparison-liltoon.md)**

| 维度 | Poiyomi | lilToon | SCSS |
|------|---------|---------|------|
| 风格化 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 预设数量 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 开源 | ❌ | ✅ MIT | ✅ MIT |
| 国内访问 | ⚠️ | ✅ | ✅ |
| Quest 优化 | ✅ | ✅ | ✅ |

---

## 10. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Poiyomi 原始数据主索引** | `参考文献/Poiyomi/INDEX.md` |
| **Poiyomi Introduction 原文** | `参考文献/Poiyomi/00-introduction.md` |
| **Poiyomi 全部 65 文档** | `参考文献/Poiyomi/*.md` |
| **VPM 包元数据** | `memory/sources/vpm-mirrors/samples/poiyomi.md` |
| **Avatar Shader 主索引** | `../index.md` |
| **lilToon 知识库** | `../liltoon/index.md` |
| **SCSS 知识库** | `../scss.md` |
| **Avatar 性能等级** | `memory/avatar/performance-rank.md` |
| **Avatar 优化指南** | `memory/avatar/optimization-guide.md` |

---

## 11. 知识库维护

| 维度 | 状态 |
|------|------|
| **主题知识文档** | 8/8 完成 (Stage 2) |
| **原始数据入库** | 65/65 (2026-07-01) |
| **路由补全** | ✅ (Stage 3) |
| **缺口修复** | ⚠️ shading-styles 7 子页面 + matcaps + TPS 子页面待重抓 (Stage 4) |
| **下次评审** | Stage 4 完成后 (2026-07-15) |

### 11.1 入库历史

| 日期 | 事件 |
|------|------|
| 2026-07-01 | 65 原始文档入库 |
| 2026-07-01 | Stage 1 完成(索引 + 引用) |
| 2026-07-01 | Stage 2 完成(8 主题知识) |
| 2026-07-01 | Stage 3 完成(路由补全) |
| 待办 | Stage 4 缺口修复 |

### 11.2 待补充

- 实战案例(从社区搜集)
- 性能 benchmark(实际测试)
- Poiyomi + MA/AAO/VRCFury 集成示例

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **主题文档** | 8 个 |
| **原始参考** | 65 个(链接) |
| **上游版本** | Poiyomi 10.0(分阶段推出) |
| **完整度** | 90%(7 个 shading-styles 子页面缺细节) |
| **评审状态** | Stage 2 + 3 完成 |
