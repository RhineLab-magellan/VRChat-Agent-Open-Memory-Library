---
title: "Poiyomi Shaders - Pro vs Toon 功能边界"
category: avatar
subcategory: shader
poiyomi_subdir: true
knowledge_level: applied
status: active
source: "本地知识库整理(2026-07-01) + Poiyomi 官方文档 v10.0"
source_type: official
version: 1.0
upstream_version: 10.0
last_review: 2026-07-01
confidence: High
tags:
  - avatar
  - shader
  - poiyomi
  - pro
  - toon
  - patreon
  - feature-comparison
aliases:
  - "Poiyomi Pro"
  - "Poiyomi Toon"
  - "Pro vs Toon"
  - "Poiyomi Patreon"
related:
  - "./installation.md"
  - "./shader-variants.md"
  - "./modular-system.md"
  - "./shading-styles.md"
  - "../../../../参考文献/Poiyomi/00-introduction.md"
  - "../../../sources/vpm-mirrors/samples/poiyomi.md"
---

# Poiyomi Shaders — Pro vs Toon 功能边界

> **Domain**: Avatar → Shader → Poiyomi → Pro vs Toon
> **原始参考**: `参考文献/Poiyomi/00-introduction.md` + 知识库比对
> **状态**: 活跃(Active)

---

## 1. 概述

Poiyomi 有**两套独立包**:
- **Poiyomi Toon**: 免费,基础 Toon/PBR
- **Poiyomi Pro**: 订阅,完整功能 + 高级效果

本档明确**哪些功能 Toon 有 / 哪些必须 Pro**,帮助你判断是否需要订阅。

---

## 2. 决策树

```
你需要这些功能吗?
│
├─ Modular Shader System         → 必须 Pro
├─ Poiyomi Fur(1-31 层)         → 必须 Pro
├─ ShatterWave                   → 必须 Pro
├─ Geometric Dissolve            → 必须 Pro
├─ Constellation(星空)           → 必须 Pro
├─ Voronoi 3D                    → 必须 Pro
├─ Internal Parallax             → 必须 Pro
├─ BlackLight Masking            → 必须 Pro
├─ 第三方模块                    → 必须 Pro
│
├─ 基础 Toon/PBR/Outline/AudioLink → Toon 即可
├─ 9 种 Lighting Type             → Toon 有大部分,Pro 更完整
├─ AL Spectrum/Volume Color       → Toon 有基础
├─ Thry Editor                    → 两者都有
└─ Lil Fur(基于 LilToon)          → 两者都有
```

---

## 3. 完整功能对比表

### 3.1 基础与编辑器(两者都有)

| 功能 | Toon | Pro |
|------|------|-----|
| **5 个变体 (Nano→Tera)** | ✅ | ✅ |
| **Thry Editor UI** | ✅ | ✅ |
| **Cross Shader Editor** | ✅ | ✅ |
| **Presets** | ✅ | ✅ |
| **9 种 Lighting Type** | ✅ 基础 | ✅ 完整 |
| **9 种 Rendering Preset** | ✅ | ✅ |
| **AudioLink 基础** | ✅ | ✅ |
| **AL Spectrum** | ✅ 基础 | ✅ 完整 |
| **AL Volume Color** | ✅ | ✅ |
| **Lil Fur(基于 LilToon)** | ✅ | ✅ |
| **Light Volumes** | ✅ | ✅ |
| **LTCGI** | ✅ | ✅ |
| **Global Masks** | ❌ | ✅ |
| **Global Themes** | ❌ | ✅ |
| **RGBA Color Masking** | 基础 | ✅ 完整 |
| **BlackLight Masking** | ❌ | ✅ |

### 3.2 Pro 专属功能(Poiyomi Pro 必须)

| 功能 | Toon | Pro | 重要性 |
|------|------|-----|--------|
| **Modular Shader System** | ❌ | ✅ | ⭐⭐⭐⭐⭐ |
| **Poiyomi Fur(1-31 层)** | ❌ | ✅ | ⭐⭐⭐⭐⭐ |
| **ShatterWave** | ❌ | ✅ | ⭐⭐⭐⭐ |
| **Geometric Dissolve** | ❌ | ✅ | ⭐⭐⭐⭐ |
| **Constellation(星空)** | ❌ | ✅ | ⭐⭐⭐ |
| **Voronoi 3D** | ❌ | ✅ | ⭐⭐⭐ |
| **Internal Parallax** | ❌ | ✅ | ⭐⭐⭐ |
| **BlackLight Masking** | ❌ | ✅ | ⭐⭐ |
| **第三方模块支持** | ❌ | ✅ | ⭐⭐⭐⭐ |
| **完整 Modular 主题** | ❌ | ✅ | ⭐⭐⭐ |

### 3.3 Toon 也有但 Pro 更强(部分功能)

| 功能 | Toon 实现 | Pro 实现 |
|------|----------|----------|
| **AudioLink 频段** | 4 (Micro) / 5 | 5 完整 + 自定义模块 |
| **Lighting Type 参数** | 基础参数 | 完整参数 + 高级控制 |
| **Voronoi** | 2D | 2D + 3D + Random Cell Color |
| **Masking** | 基础 RGBA | 完整 Channel Module + Scale/Offset |

---

## 4. 订阅决策

### 4.1 必须订阅 Pro 的场景

| 场景 | 原因 |
|------|------|
| **需要 Modular Shader System** | 团队/复杂 Avatar 必备 |
| **需要 Poiyomi Fur 1-31 层** | 风格化毛发效果 |
| **需要星空/几何溶解** | 风格化视觉 |
| **需要第三方模块** | 扩展性 |
| **需要 BlackLight** | 夜光效果 |
| **预算 $10+/月可承受** | 性价比高 |

### 4.2 不需要 Pro 的场景

| 场景 | 原因 |
|------|------|
| **基础 Toon 风格 Avatar** | Toon 已够用 |
| **预算 $0** | 免费 Toon 即可 |
| **只用基础效果** | 9 种 Lighting Type 基础够用 |
| **不需高级 VFX** | Geometric Dissolve/ShatterWave 不用 |

### 4.3 Patreon 等级选择

| 等级 | 价格 | 解锁内容 |
|------|------|----------|
| **免费** | $0 | Toon 完整 + 部分 Pro 基础 |
| **$2/月** | $2 | 早期访问测试功能 |
| **$5/月** | $5 | 额外测试包 |
| **$10/月** ⭐ | $10 | **Pro 完整** + 全部 Shader 变体 |
| **$20/月** | $20 | 更早访问 + 优先支持 |
| **$50/月** | $50 | 全部内容 + 最高优先支持 |

**推荐**: 大多数用户 **$10/月** 即可获得完整 Pro。

---

## 5. 鉴权流程

> 详见 `./installation.md` §5

```
Patreon $10+/月订阅
    ↓
Discord 绑定 Patreon 账户
    ↓
#pro-downloads 频道下载 .unitypackage
    ↓
手动 Import 到 Unity
    ↓
Unity Inspector 出现 Pro Shader 选项
```

---

## 6. 商业使用合规

| 维度 | 规则 |
|------|------|
| **商业 Avatar 销售** | ✅ Patreon ToS 允许 |
| **二次分发 Pro .unitypackage** | ❌ 禁止 |
| **用 Pro 制作 Avatar 出售** | ✅ 允许 |
| **公开镜像 Pro 下载链接** | ❌ 禁止 |
| **取消订阅后** | 订阅期内仍可用,期满停用 |

---

## 7. 实战陷阱

| 错误 | 后果 | 修复 |
|------|------|------|
| **未订阅用 Pro 变体** | Shader 不可见/编译失败 | 订阅 $10+ 或改 Toon |
| **用免费变体想要 Pro 效果** | 看不到 Toggle | 升级 Pro |
| **Pro 鉴权过期** | Pro Shader 失效 | 续订 Patreon |
| **混用 Toon 和 Pro Material** | 风格不统一 | 决定好风格再选择 |
| **Quest 上用 Pro 完整功能** | 性能问题 | Pro 也有 Micro 变体,可用但需关重效果 |

---

## 8. Pro vs Toon 与变体的关系

**变体(Nano/Micro/Mega/Giga/Tera)是独立于 Pro/Toon 的维度**:

```
Poiyomi Toon × 5 变体 = 5 个 Toon Shader
Poiyomi Pro × 5 变体 = 5 个 Pro Shader
```

| 变体 | Toon | Pro |
|------|------|-----|
| Nano | `.poiyomi/Poiyomi Toon Nano` | `.poiyomi/Poiyomi Pro Nano` |
| Micro | `.poiyomi/Poiyomi Toon Micro` | `.poiyomi/Poiyomi Pro Micro` |
| Mega | `.poiyomi/Poiyomi Toon Mega` | `.poiyomi/Poiyomi Pro Mega` |
| Giga | (合并到 Mega) | `.poiyomi/Poiyomi Pro Giga` |
| Tera | (合并到 Mega) | `.poiyomi/Poiyomi Pro Tera` |

> 注: Giga/Tera 主要在 Pro 端区分(因为 Pro 才需要这些变体)

---

## 9. 实战推荐组合

### 9.1 新手入门

```
Poiyomi Toon Mega (免费)
+ 基础 9 种 Lighting Type
+ AudioLink 5 频段
+ Outline
```

### 9.2 中级玩家

```
Poiyomi Pro Mega ($10/月)
+ 9 种 Lighting Type 完整
+ AL Spectrum
+ Poiyomi Fur 5 层(Pro 限制)
+ Voronoi 2D
+ Modular(基础)
```

### 9.3 高级玩家

```
Poiyomi Pro Tera ($10/月)
+ 全部 Pro 功能
+ 完整 Modular
+ Poiyomi Fur 31 层
+ ShatterWave / Geometric Dissolve
+ Voronoi 3D / Constellation
+ 内部 Parallax
```

### 9.4 Quest 优化

```
Poiyomi Toon Micro (免费) ← Quest 首选
+ 基础 Toon
+ AudioLink 4 频段
+ 简化 Outline
- 不开任何 Pro 效果
```

---

## 10. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Poiyomi Introduction 原文** | `参考文献/Poiyomi/00-introduction.md` |
| **Poiyomi Download & Install** | `参考文献/Poiyomi/01-download-install.md` |
| **Poiyomi Modular System** | `./modular-system.md` |
| **Poiyomi Shader Variants** | `./shader-variants.md` |
| **VPM 包元数据(含 Patreon 鉴权)** | `memory/sources/vpm-mirrors/samples/poiyomi.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **上游版本** | Poiyomi 10.0 |
| **Pro 价格** | Patreon $10/月起 |
| **评审状态** | Stage 2.7 完成 |
| **下一步** | Stage 2.8 LilToon 对比 + Stage 3 路由 |
