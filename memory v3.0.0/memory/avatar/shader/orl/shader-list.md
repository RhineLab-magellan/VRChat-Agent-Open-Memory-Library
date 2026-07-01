---
title: "ORL Shaders 详细列表"
category: avatar
subcategory: shader
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: official
version: 1.0
upstream_version: "v7.2.0 (2026-01-24)"
last_review: 2026-06-21
confidence: Medium
tags:
  - avatar
  - shader
  - orl
  - occlusion
aliases:
  - 着色器
  - "ORL Shaders 详细列表"
related:
  - overview.md
  - configurable.md
  - comparison.md
---
# ORL Shaders 详细列表

> Standard/Toon/VFX/UI/Special 全分类详解

---

## Standard Shaders (PBR) - 22个

### Base Shader - PBR核心

**Shader 名称**: `orels1/Standard` 系列

#### Main Settings

| 参数 | 说明 |
|------|------|
| **Main Color** | 主色调 |
| **Albedo** | 主纹理，支持 UV/Local Space/World Space/Triplanar |
| **Mapping Space** | 纹理映射空间选择 |
| **Masks** | Mask 纹理（R=Metallic, G=AO, B=Detail, A=Smoothness） |
| **Metal/AO/Detail/Smooth** | 自定义 Mask 通道映射 |
| **Roughness Mode** | 切换 Smoothness/Roughness 模式 |
| **Normal Map** | 法线贴图，支持 Flip Y (UE Mode) |
| **Emission** | 自发光控制 |

#### Parallax

| 参数 | 说明 |
|------|------|
| **Enable Parallax** | 启用 Parallax Occlusion Mapping |
| **Height** | 高度图（必须线性） |
| **Height Strength** | 视差强度 |
| **Height Ref Plane** | 参考平面偏移 |
| **Steps** | 质量步数 |
| **Scaled Based On Angle** | 掠射角时降低强度 |

#### Details

支持 Packed HDRP 模式和 Separated BIRP 模式：

| 参数 | 说明 |
|------|------|
| **Detail Map Mode** | Packed/Separated |
| **Detail Map** | 细节贴图 |
| **Details Normal Map** | 细节法线（仅 Separated） |
| **Albedo Scale** | 亮度调整 |
| **Normal Scale** | 法线强度 |
| **Smooth Scale** | 光滑度偏移 |

#### VRChat Features

| 参数 | 说明 |
|------|------|
| **VRC Fallback** | Shader Fallback（Standard/Toon/Hidden/Transparent/Cutout/ToonCutout） |
| **Hide from Main View** | 主视角隐藏（VR/Desktop） |
| **Hide from Handheld Camera** | 手持相机隐藏 |
| **Hide from Mirror** | 镜子隐藏 |

#### VRCLightVolumes

| 参数 | 说明 |
|------|------|
| **Enable VRC Light Volumes** | 启用 VRCLightVolumes v2.0.0+ 支持 |

#### Shading Mode

| 模式 | 说明 |
|------|------|
| **Default** | 标准 PBR |
| **Cloth** | 布料风格（含 Sheen + Wraparound） |

##### Clear Coat（Default 模式）

| 参数 | 说明 |
|------|------|
| **Add Clear Coat** | 启用清漆层 |
| **Clear Coat Strength** | 清漆强度 |
| **Use Clear Coat Mask** | 使用 Mask |
| **Clear Coat Smoothness** | 清漆光滑度 |

##### Cloth Settings

| 参数 | 说明 |
|------|------|
| **Custom Sheen Color** | 自定义 sheen 色 |
| **Add Subsurface Color** | 简易 SSS 效果 |
| **Subsurface Color** | SSS 色调 |

#### Advanced Settings

| 参数 | 说明 |
|------|------|
| **Culling Mode** | Back/Front/Off |
| **Render Type** | Opaque/Cutout/Transparent/Fade/Custom |
| **Cutoff** | Cutout 阈值 |
| **Depth Write** | 深度写入控制 |
| **GSAA** | Geometric Specular Anti Aliasing |
| **Mobile Tweaks** | 移动端优化 |

---

### AudioLink Shader

**Shader 名称**: `orels1/Standard AudioLink` / `orels1/Standard AudioLink Cutout`

#### Global Settings

| 参数 | 说明 |
|------|------|
| **Mask** | 音频效果遮罩 |
| **UV Channel** | UV 通道选择（1-4） |
| **Tint** | 全局色调 |
| **Kill Effects** | 禁用所有效果（Udon 控制） |
| **Effect Type** | 效果类型选择 |

#### Effect Types

| 效果 | 参数 |
|------|------|
| **Band Selection** | 频率带选择（Bass/LowMid/HighMid/High）、历史范围、滚动轴 |
| **UV Based** | UV 布局自定义频率分布、主题色支持 |
| **Waveform** | 波形显示、渐变色、中线、翻转、偏移、缩放 |
| **Bar** | 音量条、平滑度、渐变、缩放 |
| **Pulse** | Emission/Texture 双模式、强度、方向、速度 |

---

### Dissolve Shader

**Shader 名称**: `orels1/Standard Dissolve` 等

| 参数 | 说明 |
|------|------|
| **Cutoff** | Alpha 裁剪阈值 |
| **Cutoff Range Min/Max** | 范围控制 |
| **Fade Based On** | Local Position/UV/Texture/Vertex Colors |
| **Fade Direction** | X/Y/Z 及负向 |
| **Debug Fade Gradient** | 调试渐变可视化 |
| **Use Baked Noise** | 预烘焙噪声 |
| **Noise Scale/Texture/Strength** | 噪声参数 |
| **Scroll Speed** | 噪声滚动速度 |
| **Overlay Texture** | 叠加纹理（图案） |
| **Add Glowing Border** | 发光边缘 |
| **Border Width/Color** | 边缘宽度/颜色 |

---

### 其他 Standard Shader

| Shader | 核心功能 |
|--------|----------|
| **Decals** | 贴花系统 |
| **Dither Fade** | 抖动淡入淡出 |
| **Foliage** | 植被 SSS 近似 |
| **Glass** | 玻璃材质 |
| **Hotspotting** | 热区效果 |
| **Layered Material** | 多层材质混合 |
| **Layered Parallax** | 多层视差 |
| **LTCGI** | LTCGI 光照集成 |
| **AreaLit** | 区域光照 |
| **Neon Light** | 霓虹灯光效果 |
| **Puddles** | 水坑/积水效果 |
| **Pulse** | 脉冲效果 |
| **Tessellated Displacement** | 细分位移 |
| **Triplanar Effects** | 三平面映射效果 |
| **Vertex Animation** | 顶点动画（GPU） |
| **Vertical Fog** | 垂直雾效 |
| **Video Screen** | 视频纹理 |
| **VRSL GI** | VRSL 全局光照 |

---

## Toon Shaders - 3个

| Shader | 说明 |
|--------|------|
| **Base Shader (v2)** | 卡通着色器核心 |
| **UV Discard** | UV 丢弃效果 |
| **Legacy Shader (v1)** | 旧版卡通着色器 |

---

## Special Shaders - 1个

### Snow Coverage (v7.2.0 新增)

积雪覆盖效果，适用于 World 环境。

---

## VFX Shaders - 9个

| Shader | 功能 | 关键参数 |
|--------|------|----------|
| **Clouds** | 云效果 | - |
| **Ghost Lines** | 幽灵线 | - |
| **Glitch Screen** | 故障屏幕 | - |
| **Patterns** | 图案效果 | - |
| **Shield** | 能量护盾 | 双层噪声、深度融合 |
| **Laser** | 激光效果 | - |
| **Holographic Parallax** | 全息视差 | - |
| **Cubemap Screen** | 立方体屏幕 | - |
| **Block Fader** | 块状淡入 | - |

### Shield Shader 详解

| 参数 | 说明 |
|------|------|
| **Global Tint** | 全局色调 |
| **Noise Texture** | 预烘焙噪声纹理 |
| **Layer 1/2 Color** | 各层颜色 |
| **Layer 1/2 Smoothing** | 各层平滑度 |
| **Layer 1/2 Width** | 各层宽度 |
| **Layer 1/2 Movement** | 各层运动方向 |
| **Depth Blend Enabled** | 深度融合开关 |
| **Blend Distance** | 融合距离 |
| **Blend Tint** | 边缘高亮颜色 |

> ⚠️ 深度融合需要 Depth Pass（可通过配置低强度点光源实现）

---

## UI Shaders - 5个

| Shader | 功能 |
|--------|------|
| **Base Shader** | UI 基础 |
| **AudioLink** | UI 音频响应 |
| **Layered Parallax** | UI 分层视差 |
| **Scrolling Texture** | 滚动纹理 |
| **Sheen** | 光泽效果 |

---

## Configurable Modules

| 模块 | 功能 |
|------|------|
| **Custom GI Diffuse Ramp** | 自定义 GI 漫反射渐变 |
| **Depth Fade** | 深度淡入 |
| **Dither Fade** | 抖动淡入 |
| **Masked Tweaks** | 遮罩调整 |
| **SSR** | 屏幕空间反射 |
| **Vertex Colors** | 顶点颜色支持 |

---

## 相关文档

- [Overview](./overview.md) - 项目概览
- [Configurable Shader](./configurable.md) - 模块化系统
- [Comparison](./comparison.md) - Shader 对比