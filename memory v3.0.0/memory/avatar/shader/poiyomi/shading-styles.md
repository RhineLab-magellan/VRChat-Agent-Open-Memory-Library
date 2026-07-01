---
title: "Poiyomi Shaders - 9 种 Lighting Type (Shading Styles)"
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
confidence: Medium
tags:
  - avatar
  - shader
  - poiyomi
  - shading
  - lighting
  - texture-ramp
aliases:
  - "Poiyomi 阴影"
  - "Poiyomi Shading"
  - "Poiyomi Lighting Type"
  - "Texture Ramp"
  - "Multilayer Math"
related:
  - "./installation.md"
  - "./pro-vs-toon.md"
  - "../../../../参考文献/Poiyomi/63-shadows-shading-styles.md"
  - "../../../../参考文献/Poiyomi/22-light-data.md"
  - "../../../../参考文献/Poiyomi/23-rim-lighting.md"
---

# Poiyomi Shaders — 9 种 Lighting Type (Shading Styles)

> **Domain**: Avatar → Shader → Poiyomi → Shading Styles
> **原始参考**: `参考文献/Poiyomi/63-shadows-shading-styles.md`(合并页)
> **状态**: 活跃(Active)
> **⚠️ 已知缺口**: Wrapped/Skin/ShadeMap/Flat/Realistic/Cloth/SDF 7 个子页面 404,本档基于合并页 + 公开信息

---

## 1. 概述

Poiyomi 10.0 提供 **9 种 Lighting Type**,从卡通(Texture Ramp)到 PBR(Realistic)到风格化(SDF),覆盖几乎所有视觉风格需求。

> **关键约束**: Lighting Type **不能在运行时动画化**!如需切换,使用 Material 交换。

---

## 2. 9 种 Lighting Type 速查

| # | 类型 | 风格 | 复杂度 | 适用 |
|---|------|------|--------|------|
| 1 | **Texture Ramp** | 卡通 | ⭐ | 标准 Toon、可控阴影 |
| 2 | **Multilayer Math** | 卡通 | ⭐⭐ | 复杂 Toon、3 层阴影 |
| 3 | **Wrapped** | 柔和 | ⭐ | 皮肤、柔和过渡 |
| 4 | **Skin** | 次表面 | ⭐⭐ | 皮肤专用 |
| 5 | **ShadeMap** | 风格化 | ⭐ | 风格化角色 |
| 6 | **Flat** | 平面 | ⭐ | 2D 风格 |
| 7 | **Realistic** | PBR | ⭐⭐⭐ | 写实物体 |
| 8 | **Cloth** | 织物 | ⭐⭐ | 服装、布料 |
| 9 | **SDF** | 距离场 | ⭐⭐⭐ | 实验性、几何溶解 |

---

## 3. 详细参数

### 3.1 Texture Ramp(卡通斜面)

> 详细参数已抓取(63-shadows-shading-styles.md §Texture Ramp)

**概念**: 用渐变纹理控制阴影级别,经典 Toon 效果。

**关键参数**:
- `Shadow Tint` (Color): 阴影颜色
- `Lighting Ramp` (Linear Gradient Texture, sRGB OFF): 渐变纹理
- `Ramp Offset` (Float, -1.0~1.0): 渐变偏移
- `Ramp Count` (Float): 渐变数量
- `Ramp Selector UV` (Dropdown): UV0/UV1/UV2/UV3
- `Shadow Strength` (Float, 0~1): 阴影强度
- `Ignore Indirect Shadow Color` (Float, 0~1): 忽略环境色

**工具**: Thry Gradient Editor 可可视化编辑渐变。

**适用**: 标准 Toon Avatar、可控阴影过渡。

### 3.2 Multilayer Math(多层数学)

> 详细参数已抓取(63-shadows-shading-styles.md §Multilayer Math)

**概念**: 数学定义的渐变,3 个 Shadow Layer + Border,无需外部纹理。

**3 个 Shadow Layer(1/2/3)** 每个包含:
- `Color Tex`(Color Texture, sRGB ON): 阴影色纹理
- `Color`(Color): 基础阴影色
- `Border`(Float, 0~1): 阴影边界
- `Blur`(Float, 0~1): 模糊度
- `Receive Shadow`(Float, 0~1): 受阴影影响
- `Normal Blend`(Float, 0~1): 与法线混合

**Border 共享参数**:
- `Border Color`(Color): 边界颜色

**适用**: 复杂 Toon 效果(双阴影/三阴影/边界高亮)、无需纹理资源。

### 3.3 Wrapped(柔和包裹)

> ⚠️ 详情子页面 404,基于 LilToon Wrapped 经验推断

**概念**: 半 Lambert 风格的柔和过渡,无明显阴影边界。

**适用**: 皮肤、有机生物、避免硬阴影。

### 3.4 Skin(皮肤专用)

> ⚠️ 详情子页面 404,基于 PBR SSS 经验推断

**概念**: 内置次表面散射(SSS)模拟,适合皮肤透光感。

**适用**: 皮肤、耳朵、鼻尖(光穿透效果)。

### 3.5 ShadeMap(风格化阴影)

> ⚠️ 详情子页面 404

**概念**: 用外部 ShadeMap 纹理定义阴影形状/区域。

**适用**: 风格化角色、漫画阴影、Cel 阴影自定义。

### 3.6 Flat(平面)

> ⚠️ 详情子页面 404

**概念**: 完全平面着色,无光照计算。

**适用**: 2D 风格 Avatar、NPR 渲染、UI 元素。

### 3.7 Realistic(写实 PBR)

> ⚠️ 详情子页面 404,基于 PBR 原理推断

**概念**: 完整 PBR 光照模型,接近 Standard Shader 效果。

**适用**: 写实风格 Avatar、World 物件、混合现实。

### 3.8 Cloth(织物)

> ⚠️ 详情子页面 404,基于各向异性原理推断

**概念**: 模拟织物的高光模式(各向异性),适合布料。

**适用**: 服装、丝绸、天鹅绒。

### 3.9 SDF(距离场)

> ⚠️ 详情子页面 404,基于 SDF 原理推断

**概念**: 用 Signed Distance Function 定义阴影/光照形状。

**适用**: 实验性风格、几何溶解、与 Geometric Dissolve 联动。

---

## 4. 决策矩阵

| 视觉风格 | 推荐 Lighting Type | 理由 |
|----------|---------------------|------|
| **标准日式 Toon** | Texture Ramp | 经典,纹理可控 |
| **复杂 Toon(三阴影)** | Multilayer Math | 数学定义,3 层 |
| **皮肤/有机生物** | Skin / Wrapped | SSS + 柔和过渡 |
| **风格化角色** | ShadeMap | 外部纹理控制 |
| **2D 风格** | Flat | 平面着色 |
| **写实风格** | Realistic | PBR |
| **服装/布料** | Cloth | 各向异性 |
| **实验性** | SDF | 距离场 |

---

## 5. 与其他 Shader 对比

| 维度 | Poiyomi | LilToon | SCSS |
|------|---------|---------|------|
| **Lighting Type 数量** | 9 | 1-2 | 2 (Crosstone + Lightramp) |
| **Shadow Layer 数量** | 3 (Multilayer) | 1-2 | 2 (双阴影) |
| **皮肤专用** | ✅ Skin | ⚠️ 基础 SSS | ❌ |
| **织物专用** | ✅ Cloth | ❌ | ❌ |
| **2D 平面** | ✅ Flat | ❌ | ❌ |
| **距离场** | ✅ SDF | ❌ | ❌ |

**Poiyomi 优势**: Lighting Type 选择最多,适合复杂/混合风格。

---

## 6. 性能影响

| Lighting Type | 性能影响 | 备注 |
|---------------|----------|------|
| **Texture Ramp** | ⭐ 低 | 1 张纹理查找 |
| **Multilayer Math** | ⭐⭐ 中 | 3 层数学计算 |
| **Wrapped** | ⭐ 低 | 简单数学 |
| **Skin** | ⭐⭐ 中 | SSS 计算 |
| **ShadeMap** | ⭐⭐ 中 | 1 张纹理查找 |
| **Flat** | ⭐ 极低 | 无计算 |
| **Realistic** | ⭐⭐⭐ 高 | PBR 完整计算 |
| **Cloth** | ⭐⭐ 中 | 各向异性 |
| **SDF** | ⭐⭐⭐ 高 | 距离场计算 |

**Quest 推荐**: Texture Ramp / Wrapped / Flat

---

## 7. 实战陷阱

| 错误 | 症状 | 修复 |
|------|------|------|
| **运行时换 Lighting Type** | 不生效 | 改用 Material 交换 |
| **Quest 用了 Realistic** | 卡顿 | 改用 Texture Ramp |
| **Multilayer Math 全部 Layer 都启用** | 计算过重 | 只用需要的层 |
| **Lighting Ramp 纹理带 sRGB** | 颜色错误 | 必须 sRGB OFF |
| **忘启用 Receive Shadow** | 阴影不响应灯光 | 启用对应参数 |

---

## 8. 已知缺口与待补充

| 子页面 | 状态 | 影响 |
|--------|------|------|
| Wrapped | ❌ 404 | 推断文档,影响小 |
| Skin | ❌ 404 | 推断文档,影响小 |
| ShadeMap | ❌ 404 | 推断文档,影响小 |
| Flat | ❌ 404 | 推断文档,影响小 |
| Realistic | ❌ 404 | 推断文档,影响中 |
| Cloth | ❌ 404 | 推断文档,影响小 |
| SDF | ❌ 404 | 推断文档,影响中 |

**Stage 4 重抓计划**: 见 `memory/reviews/poiyomi-integration-plan-2026-07-01.md` §3.6

---

## 9. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Poiyomi Shadows/Shading 原文(合并)** | `参考文献/Poiyomi/63-shadows-shading-styles.md` |
| **Light Data(基础)** | `参考文献/Poiyomi/22-light-data.md` |
| **Rim Lighting(边缘光)** | `参考文献/Poiyomi/23-rim-lighting.md` |
| **Poiyomi Pro vs Toon** | `./pro-vs-toon.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **上游版本** | Poiyomi 10.0 |
| **完整度** | 2/9 完整,7/9 推断(已标注) |
| **评审状态** | Stage 2.5 完成 |
| **下一步** | Stage 2.6 Quest 优化 |
