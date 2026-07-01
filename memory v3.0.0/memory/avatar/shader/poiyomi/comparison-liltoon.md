---
title: "Poiyomi vs lilToon - 全面对比"
category: avatar
subcategory: shader
poiyomi_subdir: true
knowledge_level: applied
status: active
source: "本地知识库整理(2026-07-01) + 双 Shader 官方文档"
source_type: official
version: 1.0
upstream_version: "Poiyomi 10.0 / lilToon 2.3.2"
last_review: 2026-07-01
confidence: High
tags:
  - avatar
  - shader
  - poiyomi
  - liltoon
  - comparison
  - selection-guide
aliases:
  - "Poiyomi vs lilToon"
  - "Poiyomi 对比 lilToon"
  - "Shader 选择"
related:
  - "./installation.md"
  - "./pro-vs-toon.md"
  - "./shader-variants.md"
  - "./quest-optimization.md"
  - "../liltoon/index.md"
  - "../scss.md"
  - "../../../sources/vpm-mirrors/samples/poiyomi.md"
  - "../../../sources/vpm-mirrors/samples/lilxyzw.md"
---

# Poiyomi vs lilToon — 全面对比

> **Domain**: Avatar → Shader → Poiyomi vs lilToon
> **目的**: 帮你选择适合自己的 Avatar Shader
> **状态**: 活跃(Active)

---

## 1. 概述

Poiyomi 和 lilToon 是 **VRChat Avatar Toon Shader 两大主流**,各占半壁江山。本档基于双 Shader 官方文档对比,帮你根据**需求、风格、预算**选择。

> ⚠️ **客观声明**: 对比基于**官方文档功能**,实际效果需根据具体 Avatar 测试。

---

## 2. 一句话总结

| Shader | 一句话 |
|--------|--------|
| **Poiyomi** | "功能最丰富的 Toon Shader,9 种 Lighting Type + Modular System" |
| **lilToon** | "社区最成熟的 Toon Shader,30%+ VRChat Avatar 使用" |

---

## 3. 核心维度对比

### 3.1 市场与社区

| 维度 | Poiyomi | lilToon |
|------|---------|---------|
| **市场占有率** | 主流(欧美为主) | 30%+ VRChat Avatar(最大) |
| **主流地区** | 欧美、幻想风格 | 日系、亚洲风格 |
| **社区活跃度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Discord 用户** | 庞大 | 庞大 |
| **教程资源** | 丰富(Discord + YouTube) | 极丰富(日语为主) |
| **预设数量** | 较多 | 非常多(社区) |
| **国内访问** | ⚠️ VPM mirror 失败 | ✅ lilxyzw 镜像稳定 |

### 3.2 商业模式

| 维度 | Poiyomi | lilToon |
|------|---------|---------|
| **许可证** | Patreon 订阅 | MIT(免费开源) |
| **价格** | 免费 Toon + $10/月 Pro | 完全免费 |
| **商业模式** | SaaS 订阅 | 开源 + 自愿赞助 |
| **代码可读** | ❌ 闭源 | ✅ 完整开源 |
| **二次修改** | ❌ 不允许 | ✅ 允许(遵守 MIT) |

### 3.3 架构

| 维度 | Poiyomi 10.0 | lilToon 2.3.2 |
|------|--------------|----------------|
| **架构** | Shader Graph 9.x+ Pro | Shader Lab |
| **代码开源** | ❌ | ✅ MIT |
| **变体** | 5 个分级(Nano→Tera) | 1 通用 + 多个独立 Shader |
| **Thry Editor** | ✅ 官方集成 | ✅ 第三方集成 |
| **Material 池** | ✅ Modular Shader(Pro) | ❌ 需手动 |
| **Quest 优化** | ✅ Micro 变体 | ✅ Quest 详细指南 |

### 3.4 功能对比

| 功能 | Poiyomi | lilToon |
|------|---------|---------|
| **基础 Toon 阴影** | ✅ | ✅ |
| **Outline** | ✅ | ✅ |
| **AudioLink** | ✅ 完整(5 频段 + AL Spectrum) | ✅ 需手动配置 |
| **Light Volumes** | ✅ | ✅ |
| **LTCGI** | ✅ | ❌ |
| **Fur 毛发** | ✅ Pro 1-31 层 + Lil Fur | ✅ 噪声采样(跨平台) |
| **Dissolve** | ✅ 4 类型 + Geometric(Pro) | ✅ |
| **Stencil** | ✅ | ✅ |
| **Modular Shader** | ✅ Pro | ❌ |
| **5 变体分级** | ✅ | ❌ |
| **9 种 Lighting Type** | ✅ | ❌(1-2 种) |
| **Constellation(星空)** | ✅ Pro | ❌ |
| **ShatterWave** | ✅ Pro | ❌ |
| **Voronoi 3D** | ✅ Pro | ❌ |
| **Internal Parallax** | ✅ Pro | ❌ |
| **Geometric Dissolve** | ✅ Pro | ❌ |
| **Global Themes** | ✅ Pro 4 主题 | ❌ |
| **Global Mask** | ✅ Pro 16 通道 | ❌ |

### 3.5 性能

| 维度 | Poiyomi | lilToon |
|------|---------|---------|
| **PC 性能** | 中等(Pro 较重) | 良好 |
| **Quest 性能** | ✅ Micro 变体优化 | ✅ 详细 Quest 指南 |
| **Poiyomi Pro Tera** | 重型 | - |
| **lilToon 默认** | - | 轻量 |
| **文档数据 benchmark** | 较少 | 较多 |

> **实际数据**: 需在具体 Avatar 上测试。两者在 PC 上差距不大,lilToon 略轻;Quest 上两者都需配置。

### 3.6 跨平台

| 维度 | Poiyomi | lilToon |
|------|---------|---------|
| **BRP** | ✅ | ✅ |
| **URP** | ✅ Beta(6000.0+) | ✅ |
| **HDRP** | ❌ | ✅ |
| **PC 跨平台** | ✅ | ✅ |
| **Quest** | ✅ Micro 变体 | ✅ |
| **Warudo VTubing** | ✅(需手动锁定) | ✅ |

---

## 4. 风格适用

### 4.1 Poiyomi 擅长的风格

| 风格 | 原因 |
|------|------|
| **欧美幻想 Toon** | 5 变体 + 9 Lighting Type 适合复杂风格 |
| **风格化 VFX(星空/几何)** | Pro Constellation / Geometric Dissolve |
| **音乐驱动 Avatar** | 完整 AudioLink 集成 |
| **多人协作项目** | Modular Shader System 共享材质池 |
| **复杂视觉(史诗 Avatar)** | Tera 变体 + Pro 全部效果 |

### 4.2 lilToon 擅长的风格

| 风格 | 原因 |
|------|------|
| **日式动漫 Toon** | 默认风格贴近日系 |
| **简单 Avatar** | 开箱即用 + 大量预设 |
| **开源定制** | MIT 许可,可改源码 |
| **预算 $0** | 完全免费 |
| **新教程/示例多** | 社区庞大,日英教程都有 |

---

## 5. 选择决策树

### 5.1 快速决策

```
你的核心需求?
│
├─ 想要开源 + 免费 + 大量预设
│   └─ ✅ lilToon
│
├─ 想要 Modular Shader System + 9 种 Lighting Type
│   └─ ✅ Poiyomi Pro
│
├─ 想要 VFX 风格(星空/几何溶解)
│   └─ ✅ Poiyomi Pro
│
├─ 国内访问稳定
│   └─ ✅ lilToon(VPM 镜像 OK)
│
├─ 想要 Pro 简化版本(免费 Pro 基础)
│   └─ ✅ Poiyomi Toon
│
└─ 不确定 / 想要两者都尝试
    └─ Poiyomi Toon + lilToon 都很容易上手,试错成本低
```

### 5.2 详细决策矩阵

| 优先级 | 选 Poiyomi | 选 lilToon |
|--------|------------|-----------|
| **价格敏感** | ⚠️ Pro $10/月 | ✅ 完全免费 |
| **功能丰富** | ✅ Pro 完整 | ❌ 基础够用 |
| **预设数量** | ⚠️ 中等 | ✅ 极多 |
| **开源透明** | ❌ 闭源 | ✅ MIT |
| **国内访问** | ⚠️ mirror 失败 | ✅ 稳定 |
| **Quest 优化** | ✅ Micro 变体 | ✅ 详细指南 |
| **VFX 风格** | ✅ Constellation / ShatterWave | ❌ |
| **音乐 Avatar** | ✅ AudioLink 完整 | ⚠️ 需手动 |
| **Modular 系统** | ✅ Pro | ❌ |
| **5 变体分级** | ✅ | ❌ |
| **9 Lighting Type** | ✅ | ❌ |

---

## 6. 共存策略

**重要**: 同一 Avatar 可以**同时用 Poiyomi 和 lilToon**,因为 Shader 是 Material 级别,不是 Avatar 级别。

### 6.1 混用示例

```text
Avatar
├── Body        → Poiyomi Toon Mega(身体用 Poiyomi)
├── Hair        → lilToon(头发用 lilToon)
├── Clothing    → Poiyomi Pro(服装用 Pro 的 Modular)
├── Accessories → lilToon(配件用 lilToon 预设)
└── Effects     → Poiyomi Pro Tera(特效用 Poiyomi Tera)
```

**优势**:
- 各取所长
- 减小单个 Shader 学习成本
- 灵活组合

**注意**:
- 风格需统一(避免视觉割裂)
- 性能累加计算

### 6.2 迁移策略

**Poiyomi → lilToon**:
1. 复制 Material,Shader 改为 lilToon
2. 手动重新配置(参数名不完全对应)
3. 验证视觉效果

**lilToon → Poiyomi**:
1. 复制 Material,Shader 改为 Poiyomi
2. 手动重新配置
3. 注意 Poiyomi 默认是 Toon(不是 PBR)

---

## 7. 与 SCSS 三方对比

| 维度 | Poiyomi | lilToon | SCSS |
|------|---------|---------|------|
| **市场** | 主流 | 30%+ | 较小 |
| **价格** | 免费+$10 Pro | 免费 | 免费 |
| **Toon 风格** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **预设** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **开源** | ❌ | ✅ | ✅ |
| **UV 服装切换** | ❌ | ❌ | ✅ 零 Draw Call |
| **Matcap** | ✅ | ✅ | ✅ 多槽位 |
| **双阴影** | ✅ Pro | ❌ | ✅ Crosstone |
| **学习曲线** | 高 | 中 | 高 |

**结论**:
- **Poiyomi** = 风格化 + Pro 高级功能
- **lilToon** = 通用 + 社区丰富
- **SCSS** = 极致 Toon + 服装切换

---

## 8. 实战推荐

### 8.1 第一次做 Avatar

```
推荐: lilToon
理由: 免费 + 大量预设 + 详细教程
```

### 8.2 有经验,想升级

```
推荐: Poiyomi Toon → Poiyomi Pro
理由: 探索更多风格 + 团队 Modular
```

### 8.3 团队/工作室

```
推荐: Poiyomi Pro
理由: Modular Shader System 共享材质池
```

### 8.4 风格化定制(星空/幻想)

```
推荐: Poiyomi Pro Tera
理由: 风格化效果无人能及
```

### 8.5 国内独立开发者

```
推荐: lilToon(主要) + Poiyomi Toon(辅助)
理由: 国内访问稳定 + 风格互补
```

---

## 9. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Poiyomi Installation** | `./installation.md` |
| **Poiyomi Pro vs Toon** | `./pro-vs-toon.md` |
| **Poiyomi Shader Variants** | `./shader-variants.md` |
| **Poiyomi Quest 优化** | `./quest-optimization.md` |
| **lilToon 知识库** | `../liltoon/index.md` |
| **SCSS 知识库** | `../scss.md` |
| **Poiyomi VPM 数据** | `memory/sources/vpm-mirrors/samples/poiyomi.md` |
| **lilToon VPM 数据** | `memory/sources/vpm-mirrors/samples/lilxyzw.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **对比基准** | Poiyomi 10.0 / lilToon 2.3.2 |
| **客观性** | 基于官方文档,实战需测试 |
| **评审状态** | Stage 2.8 完成 |
| **下一步** | Stage 3 路由 + Stage 4 缺口修复 |
