---
title: "Poiyomi Shaders - Modular Shader System (Pro)"
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
  - modular-shader
  - module-definition
  - template-collection
  - pro
  - shader-development
aliases:
  - "Poiyomi 模块化"
  - "Poiyomi Modular"
  - "VRLM VRLT VRLTC"
  - "Module Definition"
related:
  - "./installation.md"
  - "./pro-vs-toon.md"
  - "../../../../参考文献/Poiyomi/32-modular-shader-system.md"
  - "../../../../参考文献/Poiyomi/33-global-masks.md"
  - "../../../../参考文献/Poiyomi/34-global-themes.md"
  - "../../../../参考文献/Poiyomi/35-rgba-color-masking.md"
  - "../../../../参考文献/Poiyomi/36-blacklight-masking.md"
---

# Poiyomi Shaders — Modular Shader System (Pro)

> **Domain**: Avatar → Shader → Poiyomi → Modular System
> **原始参考**: `参考文献/Poiyomi/32-modular-shader-system.md` + 33-36
> **状态**: 活跃(Active)
> **🔒 Pro 专属**: 此功能需 Poiyomi Pro 订阅

---

## 1. 概述

Poiyomi 10.0 引入 **Modular Shader System**,允许**第三方 Shader 开发者**创建可被 Poiyomi Pro 调用的功能模块。核心思想:**共享材质池**(避免重复 Material)、**模块化架构**(每个功能独立)、**主题化**(全局换色)。

**适用对象**:
- 🔧 Shader 开发者(创建自定义模块)
- 🎨 Avatar 创作者(使用 Global Themes/Masks)
- 🏢 团队 Avatar 项目(共享材质)

---

## 2. 核心概念

### 2.1 模块化架构

Poiyomi 整体由**模块**组装:

```
Poiyomi Pro Shader
    ├── Poi_Emission (发光)
    ├── Poi_Dissolve (溶解)
    ├── Poi_AudioLink (音频驱动)
    ├── Poi_Fur (毛发)
    ├── ... (数十个模块)
    └── [用户模块] (通过 Modular System 注入)
```

每个模块由**两个文件**组成:

| 文件类型 | 扩展名 | 用途 |
|----------|--------|------|
| **Module Definition** | `.asset` | YAML,定义模块元数据 + 模板引用 |
| **Template Collection** | `.poiTemplateCollection` | 实际 Shader 代码模板 |

### 2.2 命名约定

| 前缀 | 含义 | 示例 |
|------|------|------|
| `VRLM_` | Module Definition | `VRLM_PoiYourModule.asset` |
| `VRLT_` | Template Collection 单个 | `VRLT_PoiYourModule.poi` |
| `VRLTC_` | Template Collection 完整 | `VRLTC_PoiYourModule.poiTemplateCollection` |

### 2.3 注入点(Injection Points)

Poiyomi Pro 在编译时将模块插入到预设的注入点:

| 注入点 | 位置 | 用途 |
|--------|------|------|
| `BASE_PASS` | 主渲染 Pass | 基础颜色、阴影 |
| `ADD_PASS` | 额外 Pass | 透明、混合 |
| `OUTLINE_PASS` | 描边 Pass | 轮廓线 |

---

## 3. 文件结构

```text
Poi_FeatureModules/
└── Poi_YourModule/
    ├── VRLM_PoiYourModule.asset                    # 模块定义
    ├── VRLM_PoiYourModule.asset.meta
    ├── VRLTC_PoiYourModule.poiTemplateCollection   # Shader 代码集合
    └── VRLTC_PoiYourModule.poiTemplateCollection.meta
```

### 3.1 Module Definition 示例(YAML)

```yaml
# VRLM_PoiYourModule.asset
name: PoiYourModule
author: Your Name
description: 模块功能描述
version: 1.0.0
templates:
  - VRLT_PoiYourModule
injectionPoints:
  - BASE_PASS
dependencies: []
```

### 3.2 Template Collection 结构

```text
VRLTC_PoiYourModule.poiTemplateCollection
├── VRLT_PoiYourModule_VERTEX.hlsl
├── VRLT_PoiYourModule_FRAGMENT.hlsl
└── VRLT_PoiYourModule_PROPERTIES.hlsl
```

---

## 4. Global Masks(33-global-masks.md)

### 4.1 概念

**全局遮罩**允许一个 Mask 纹理同时影响**多个 Material**。Poiyomi Pro 提供 **16 通道**遮罩系统。

### 4.2 容量

| 维度 | 数量 | 说明 |
|------|------|------|
| **Mask 槽位数** | 4 | 4 张 Mask 纹理 |
| **通道/Mask** | 4 | RGBA |
| **总通道数** | 4 × 4 = 16 | 16 通道遮罩 |

### 4.3 应用方式

| 应用 | 说明 |
|------|------|
| **跨 Material 共享** | 一个 Mask 驱动多个 Material 的不同区域 |
| **性能优化** | 避免每个 Material 单独 Mask 纹理 |
| **动画驱动** | Mask 纹理可被 Animator 动画化 |

### 4.4 典型应用

**服装切换的零 Draw Call 方案**(对比 SCSS UV 切换):
```text
1. 创建 1 张 Global Mask 纹理(各区域用不同通道标记)
2. 所有 Material 都引用这同一个 Global Mask
3. 用 Animator 改变 Mask 的可见性 → 所有 Material 同步响应
```

---

## 5. Global Themes(34-global-themes.md)

### 5.1 概念

**全局主题**允许运行时切换整套 Material 的颜色方案。最多 4 个主题。

### 5.2 关键参数

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| **Theme Count** | Int | 1-4 | 主题数量 |
| **Color Space** | Dropdown | OKLab / HSV | 颜色空间 |
| **Saturation Style** | Toggle | - | 饱和度处理方式 |

### 5.3 OKLab vs HSV 色空间

| 色空间 | 优势 | 劣势 |
|--------|------|------|
| **OKLab** | 感知线性、过渡自然 | 较新,设计师不熟悉 |
| **HSV** | 直观、设计师熟悉 | 过渡不线性 |

**推荐**: 团队用 OKLab(科学),个人/爱好者用 HSV(直观)。

### 5.4 典型应用

**多主题 Avatar**(白天/夜晚/特殊活动):
```text
1. 主题 1: 正常白
2. 主题 2: 暗夜黑
3. 主题 3: 节日红
4. 主题 4: 霓虹彩
→ Animator 驱动 Theme 切换 → 整套 Avatar 瞬间换色
```

---

## 6. RGBA Color Masking(35-rgba-color-masking.md)

### 6.1 概念

通过 RGBA 通道分别控制**颜色、Normal、Color Blend、Normal Blend** 的蒙版影响。

### 6.2 关键参数

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| **Mode** | Dropdown | Texture / Vertex Colors | 数据源 |
| **Channel Module** | Dropdown | - | 通道选择 |
| **Scale** | Float | - | 强度缩放 |
| **Offset** | Float | - | 强度偏移 |
| **Color Blend** | Float | 0-1 | 颜色混合度 |
| **Normal Blend** | Float | 0-1 | 法线混合度 |

### 6.3 典型应用

**身体彩绘**(用 Vertex Color 通道区分):
- R 通道: 区域 1
- G 通道: 区域 2
- B 通道: 区域 3
- A 通道: 区域 4
→ 每个区域用不同 Material 属性

---

## 7. BlackLight Masking(36-blacklight-masking.md)

### 7.1 概念

通过 **Black Point Light** 让某些区域在"黑光"下发光(类似 UV 灯/夜光)。

### 7.2 必要组件

| 组件 | 设置 | 说明 |
|------|------|------|
| **Point Light** | Color = Black(0,0,0) | 黑色但有光照计算 |
| **Point Light** | Mode = Realtime | 实时模式 |
| **Point Light** | Render Mode = Not Important | 不投射阴影 |
| **BlackLight Mask** | 4 槽位 | Poiyomi Pro 提供 |

### 7.3 典型应用

**夜光服装**:
```text
1. 在 Avatar 区域放 Point Light(Color=Black, Mode=Realtime, RenderMode=Not Important)
2. Material 启用 BlackLight Masking
3. 选 Mask 槽位 1,设置发光色
效果: 走近该 Point Light 时,服装区域发光
```

---

## 8. 实战陷阱

| 错误 | 症状 | 修复 |
|------|------|------|
| **模块未导入** | Shader 编译错误 | 确认 .asset 和 .poiTemplateCollection 都在 Plugins |
| **Toon 用户尝试用 Pro 模块** | 模块不可见 | 订阅 Patreon Pro |
| **Global Mask 通道重叠** | 多个区域相互干扰 | 通道分配要正交 |
| **Theme 切换跳变** | 颜色突变 | 用 OKLab 色空间或加过渡动画 |
| **BlackLight 用错光源类型** | 无效果 | 必须 Point Light + 黑色 + Realtime + Not Important |

---

## 9. 性能 vs 功能矩阵

| 维度 | Toon | Pro(无 Modular) | Pro + Modular |
|------|------|----------------|----------------|
| **基础功能** | ✅ | ✅ | ✅ |
| **Global Mask** | ❌ | ❌ | ✅ 16 通道 |
| **Global Theme** | ❌ | ❌ | ✅ 4 主题 |
| **RGBA Color Masking** | 基础 | 基础 | ✅ 完整 |
| **BlackLight Masking** | ❌ | ❌ | ✅ 4 槽位 |
| **第三方模块** | ❌ | ❌ | ✅(可扩展) |
| **团队共享** | ❌ | ❌ | ✅ 共享池 |

---

## 10. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Modular Shader System** | `参考文献/Poiyomi/32-modular-shader-system.md` |
| **Global Masks** | `参考文献/Poiyomi/33-global-masks.md` |
| **Global Themes** | `参考文献/Poiyomi/34-global-themes.md` |
| **RGBA Color Masking** | `参考文献/Poiyomi/35-rgba-color-masking.md` |
| **BlackLight Masking** | `参考文献/Poiyomi/36-blacklight-masking.md` |
| **Poiyomi Pro vs Toon** | `./pro-vs-toon.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **上游版本** | Poiyomi 10.0 |
| **功能级别** | 🔒 Poiyomi Pro 专属 |
| **评审状态** | Stage 2.4 完成 |
| **下一步** | Stage 2.5 Shading Styles |
