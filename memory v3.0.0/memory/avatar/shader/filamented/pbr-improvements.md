---
title: "Filamented PBR 改进详解"
category: avatar
subcategory: shader
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: "v1.4.0 (2024-03)"
last_review: 2026-06-21
confidence: Medium
tags:
  - avatar
  - shader
  - filamented
  - light
  - occlusion
aliases:
  - "Filamented PBR 改进详解"
  - pbr-improvements
related:
  - comparison.md
  - overview.md
  - "../orl/comparison.md"
  - "../liltoon/reflection-settings.md"
  - "../orl/overview.md"
---
# Filamented PBR 改进详解

## 一、Fresnel 计算修复（核心改进）

### Standard 的问题

Unity Standard Shader 对非金属材质使用了一个不精确的 Fresnel 近似公式，导致：

| 问题 | 表现 |
|------|------|
| Fresnel 过强 | 非金属表面的镜面反射比预期更强 |
| 光泽不自然 | 光滑表面（如塑料、玻璃）的光泽看起来假 |
| 能量不守恒 | 在某些角度下高光过亮 |

### Filamented 的解决方案

```
标准 Fresnel (Schlick):  F = F0 + (1 - F0) * (1 - cosθ)^5

Filament 改进方案：
- 使用更精确的 Fresnel 计算
- 非金属 F0 基于 reflectance 参数
- 结果：更柔和、更自然的镜面光泽
```

### 对比示意

```
角度变化时：

Standard:  [黑暗] → [突然变亮] → [高光过强]
           ↑                            ↑
           └──── Fresnel 跳变 ──────────┘

Filamented: [柔和过渡] → [自然衰减]
            ↑                    ↑
            └──── 平滑过渡 ─────┘
```

## 二、Exposure Occlusion（Specular 遮挡）

### 解决的问题

传统 PBR 流程中，烘焙到 Lightmap 的阴影只影响漫反射，不影响镜面反射：

```
传统流程：
Lightmap 烘焙阴影
    ↓
漫反射：正确衰减 ❌镜面反射：不受影响 → 黑暗区域出现不合理的高光
```

### Filamented 流程

```
Lightmap 烘焙阴影
    ↓
Exposure Occlusion 计算
    ↓
漫反射：正确衰减 ✅ 镜面反射：同步衰减 ✅
```

### 实现方式

Exposure Occlusion 使用 Lightmap 的强度信息来遮挡 Specular：

```
occlusion = lightmap_sample
specular *= occlusion
diffuse *= occlusion
```

## 三、改进的 Parallax（视差映射）

### Standard 的问题

Standard 使用较低质量的视差采样，在极端角度下容易出现穿帮。

### Filamented 的改进

- 提升视差采样精度
- 在大角度下更稳定
- 减少"漂浮感"

## 四、VRC Light Volumes 支持

### 集成方式

Filamented 完整支持 VRCLightVolumes 系统：

```csharp
// VRC Light Volumes 自动检测并应用
// 无需额外配置，Shader 内置支持
```

### 支持的功能

- ✅ 体素化光照探针替代
- ✅ Point/Spot/Area 光源
- ✅ 动态颜色修改
- ✅ 烘焙阴影继承

## 五、光照贴图增强

### Bicubic Lightmap Filtering

更平滑的光照贴图采样方式：

```
Standard:     [块状] → [双线性插值] → 边缘过渡不平滑
Filamented:   [块状] → [双立方插值] → 边缘过渡平滑
```

### Lightmap-derived Specular

光照贴图强度用于遮挡反射探针，减少黑暗区域的不自然反射。

## 六、技术总结

| 改进项 | 技术级别 | 视觉影响 |
|--------|----------|----------|
| Fresnel 修复 | 核心 | ⭐⭐⭐⭐⭐ |
| Specular Occlusion | 重要 | ⭐⭐⭐⭐ |
| Parallax 改进 | 中等 | ⭐⭐⭐ |
| Light Volumes | 重要 | ⭐⭐⭐⭐ |
| Bicubic Filtering | 次要 | ⭐⭐⭐ |

### 性能影响

轻微增加计算复杂度，但：
- 不影响运行时性能
- 主要影响光照烘焙质量
- 整体开销可控