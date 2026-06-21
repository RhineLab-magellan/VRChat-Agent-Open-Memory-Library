---
title: UnlitWF Shader Suite 知识库
category: avatar
subcategory: shader

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "着色器"
  - "UnlitWF"

related:
  - avatar/shader/index.md

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: UnlitWF_Shader_20260208 (2026-02-08)
last_review: 2026-06-21
confidence: Medium
---
# UnlitWF Shader Suite 知识库

> UnlitWF（UnToon）— 基于 Unlit 的专业效果 Shader 套件
> 
> 来源：https://github.com/whiteflare/Unlit_WF_ShaderSuite

---

## 目录

1. [项目概述](#1-项目概述)
2. [Shader 家族分类](#2-shader-家族分类)
3. [核心架构](#3-核心架构)
4. [效果系统](#4-效果系统)
5. [专业效果系统](#5-专业效果系统)
6. [平台支持](#6-平台支持)
7. [优缺点分析](#7-优缺点分析)
8. [与 lilToon/SCSS 对比](#8-与-liltoonscss-对比)
9. [VRChat 适用性](#9-vrchat-适用性)

---

## 1. 项目概述

### 1.1 设计理念

UnlitWF 的核心理念：

> *"将纹理 그대로描画하는 Unlit シェーダ에 다양한 효과를 추가"*  
> *"在直接渲染纹理的 Unlit Shader 基础上添加各种效果"*

**定位**：基于 Unlit 的 Toon Shader 扩展包，而非从头编写的 PBR 替代方案。

### 1.2 核心特点

| 特性 | 描述 |
|------|------|
| **渲染管线** | Built-in RP + URP 双支持 |
| **Shader 语言** | ShaderLab (65.7%) + HLSL (11.0%) + C# (23.3%) |
| **模块化设计** | 共享 `cginc` 包含文件 + 变体组合 |
| **平台支持** | Desktop / Mobile / VRChat / Quest |
| **Editor 工具** | 自定义 Inspector、材质转换、构建优化 |

### 1.3 安装方式

```text
VPM 安装：https://whiteflare.github.io/vpm-repos/docs/unlitwf

unitypackage（VRChat 直接导入）：
  - _01_Core.unitypackage      ← 核心 Shader
  - _02_Texture.unitypackage   ← Matcap/CubeMap 素材
  - _03_Examples.unitypackage  ← 示例场景

URP 其他版本：
  - Unity2019.4: head_unity2019URP 分支
  - Unity2021.3+: head_unity2021URP 分支
```

---

## 2. Shader 家族分类

### 2.1 主 Shader 树

```
UnlitWF/
├── WF_UnToon_                    ← Base UnToon 基础系列
│   ├── Opaque                    ← 不透明
│   ├── TransCutout               ← Alpha Cutout（叶子/头发）
│   ├── Transparent               ← Alpha Blend 标准透明
│   ├── Transparent3Pass          ← 3-Pass 高质量透明
│   ├── Transparent_Mask          ← Stencil Mask 输入
│   └── Transparent_MaskOut       ← Stencil Mask 输出
│
├── UnToon_PowerCap/              ← PowerCap 增强系列
│   └── (相同的透明度变体)
│
├── UnToon_TriShade/              ← TriShade 三层阴影系列
│   └── (相同的透明度变体)
│
├── UnToon_Tessellation/          ← Tessellation 细分系列
│   └── (相同的透明度变体)
│
├── UnToon_Outline/               ← Outline 轮廓系列
│   └── (相同的透明度变体)
│
└── Custom_*                      ← 自定义组合变体
    ├── Custom_PowerCap_Outline_Opaque
    ├── Custom_Tess_PowerCap_Opaque
    └── ...
```

### 2.2 透明度模式矩阵

| 模式 | Queue | Alpha 处理 | 适用场景 |
|------|-------|-----------|---------|
| **Opaque** | Geometry | 无 | 实体对象 |
| **TransCutout** | AlphaTest | 二值 Cutoff | 硬边透明（叶子、头发） |
| **Transparent** | Transparent | Alpha Blending | 标准透明 |
| **Transparent3Pass** | Transparent | 多 Pass 渲染 | 高质量透明（玻璃、水） |

### 2.3 Shader 家族说明

| 家族 | 特点 | 使用场景 |
|------|------|---------|
| **Base UnToon** | 基础 Toon 着色，完整效果链 | 通用 Avatar |
| **PowerCap** | 增强 Matcap，多个 Matcap 槽位 | 高级视觉效果 |
| **TriShade** | 三层阴影渐变 | 细腻阴影控制 |
| **Tessellation** | 硬件细分，平滑模型 | 高精度模型 |
| **Outline** | 内置轮廓线渲染 | 需要描边的模型 |

---

## 3. 核心架构

### 3.1 Central Data Structure 模式

UnlitWF 的核心架构围绕 **三个数据结构** 展开：

```hlsl
// appdata - Vertex 输入
struct appdata {
    float4 vertex;    // 顶点位置
    float2 uv;        // UV 坐标
    float3 normal;    // 法线
    float4 tangent;   // 切线
};

// v2f - Vertex to Fragment 插值
struct v2f {
    float4 vs_vertex;     // 屏幕空间顶点
    float3 ws_vertex;     // 世界空间顶点
    float3 ws_normal;     // 世界空间法线
    float3 light_color;   // 光源颜色
};

// drawing - Central Effect Processing Data ⭐核心
struct drawing {
    float4 color;         // 主颜色
    float3 ws_vertex;     // 世界空间位置
    float3 ws_normal;     // 世界空间法线
    float3 light_color;   // 光照颜色
};
```

**设计模式**：效果函数接收 `drawing` struct，修改后返回，实现效果链式调用。

### 3.2 顺序效果管线

Fragment shader 按顺序应用效果，每个 `draw*()` 函数修改 `drawing` struct：

| 阶段 | 函数 | 功能 |
|------|------|------|
| **纹理采样** | `drawMainTex()`, `drawMainTex2nd()` | 基础纹理 + 第二纹理 |
| **颜色处理** | `drawGradientMap()`, `drawColorChange()` | 渐变映射、HSV 调整 |
| **表面效果** | `drawMetallic()`, `drawMatcapColor()` | 金属感、Matcap |
| **光照效果** | `drawToonShade()`, `drawRimLight()` | 卡通阴影、边缘光 |
| **后处理** | `drawEmissiveScroll()`, `drawDissolve()` | 自发光滚动、溶解 |

### 3.3 属性命名规范

统一的属性前缀系统：

| 前缀 | 效果类别 | 示例属性 |
|------|---------|---------|
| `\_TX2_` | 第二纹理 | `\_TX2_Enable`, `\_TX2_MainTex`, `\_TX2_Color` |
| `\_MT_` | 金属效果 | `\_MT_Enable`, `\_MT_Metallic`, `\_MT_ReflSmooth` |
| `\_TS_` | Toon 阴影 | `\_TS_Enable`, `\_TS_BaseColor`, `\_TS_Steps` |
| `\_TR_` | Rim Light | `\_TR_Enable`, `\_TR_Color`, `\_TR_Width` |
| `\_NM_` | Normal Map | `\_NM_Enable`, `\_BumpScale`, `\_NM_Power` |
| `\_HL_` | Matcap | `\_HL_Enable`, `\_HL_MatcapTex`, `\_HL_Power` |
| `\_ES_` | Emission Scroll | `\_ES_ScrollEnable`, `\_ES_SC_Speed` |
| `\_DFD_` | Distance Fade | 距离渐变 |
| `\_DSV_` | Dissolve | 溶解效果 |

---

## 4. 效果系统

### 4.1 Toon Shading（卡通阴影）

| 属性 | 说明 |
|------|------|
| `\_TS_Enable` | 启用开关 |
| `\_TS_Steps` | 阴影步数 |
| `\_TS_BaseColor` | 基础色 |
| `\_TS_1st_ShadeColor` | 第一阴影色 |
| `\_TS_2nd_ShadeColor` | 第二阴影色 |

### 4.2 Rim Light（边缘光）

| 属性 | 说明 |
|------|------|
| `\_TR_Enable` | 启用开关 |
| `\_TR_Color` | 边缘光颜色 |
| `\_TR_Width` | 边缘宽度 |
| `\_TR_Feather` | 边缘柔化 |

### 4.3 Matcap（材质捕获）

支持多个 Matcap 槽位（PowerCap 变体）：

| 属性 | 说明 |
|------|------|
| `\_HL_Enable` | 启用开关 |
| `\_HL_MatcapTex` | Matcap 纹理 |
| `\_HL_Power` | 强度 |
| `\_HL_Blend` | 混合模式 |

### 4.4 Metallic（金属效果）

自定义金属系统（非标准 PBR）：

| 属性 | 说明 |
|------|------|
| `\_MT_Enable` | 启用开关 |
| `\_MT_Metallic` | 金属度 |
| `\_MT_ReflSmooth` | 反射平滑度 |

### 4.5 Dissolve（溶解效果）

| 属性 | 说明 |
|------|------|
| `\_DSV_Enable` | 启用开关 |
| `\_DSV_MaskTex` | 溶解遮罩 |
| `\_DSV_BaseOffset` | 基础偏移 |
| `\_DSV_Color` | 溶解边缘色 |

---

## 5. 专业效果系统

### 5.1 FakeFur System（毛发系统）

| 特性 | 说明 |
|------|------|
| **实现方式** | Geometry Shader 生成多层毛发 |
| **毛发层数** | 1-6 层可配置 |
| **染色方式** | Base→Tip 渐变染色 |
| **遮罩支持** | 长度遮罩 + Alpha 遮罩 |
| **平台限制** | ❌ 不支持移动端（需要 SM5.0） |

**Shader 变体**：
- `WF_FakeFur_TransCutout` — 标准毛发
- `WF_FakeFur_Transparent` — 透明毛发
- `WF_FakeFur_Mix` — 双层毛发
- `WF_FakeFur_FurOnly_*` — 仅毛发（无基础表面）

**核心属性**：
```
_FUR_Height     — 毛发长度 (0-0.2)
_FUR_Repeat     — 毛发层数 (1-6)
_FUR_Vector     — 生长方向
_FUR_TintColorBase/Tip — 基部/尖端颜色
```

### 5.2 Water System（水面系统）

| 特性 | 说明 |
|------|------|
| **波浪层数** | 支持 3 层独立波浪 |
| **法线贴图** | 多层法线混合 |
| **焦散效果** | 焦散纹理投影 |
| **反射** | Cubemap 反射 |
| **折射** | TransparentRefracted 变体 |

**Shader 变体**：
- `WF_Water_Surface_Transparent` — 标准水面
- `WF_Water_Surface_TransparentRefracted` — 带折射
- `WF_Water_Surface_Opaque` — 不透明水面
- `WF_Water_Caustics_Addition` — 焦散投影

### 5.3 Grass System（草地系统）

| 特性 | 说明 |
|------|------|
| **高度计算** | World Y / UV / Vertex Color / Mask |
| **波动动画** | 风力模拟 |
| **高度染色** | 基于高度的着色 |

**高度类型**：
| 类型 | 来源 |
|------|------|
| `WORLD_Y` | 世界 Y 坐标 |
| `UV` | UV 坐标 |
| `VERTEX_COLOR` | 顶点颜色通道 |
| `MASK_TEX` | 纹理遮罩 |

### 5.4 Gem System（宝石系统）

| 特性 | 说明 |
|------|------|
| **Flake 效果** | 内部闪光模拟 |
| **双面渲染** | Front + Back 独立渲染 |
| **反射控制** | Cubemap 反射 + 单色模式 |
| **透明变体** | Transparent / Opaque |

**Shader 变体**：
- `WF_Gem_Transparent` — 双 Pass 透明宝石
- `WF_Gem_Opaque` — 单 Pass 不透明宝石

### 5.5 Particle System（粒子系统）

| 特性 | 说明 |
|------|------|
| **混合模式** | Multiple blend modes |
| **Flip-Book** | 帧动画支持 |
| **Vertex Color** | MUL/ADD/SUB 混合 |

---

## 6. 平台支持

### 6.1 渲染管线抽象

```hlsl
// 纹理采样抽象
#if defined(URP)
    TEXTURE2D(_MainTex);
    SAMPLER(sampler_MainTex);
    #define PICK_MAIN_TEX2D(tex, uv) SAMPLE_TEXTURE2D(tex, sampler##tex, uv)
#else
    UNITY_DECLARE_TEX2D(_MainTex);
    #define PICK_MAIN_TEX2D(tex, uv) UNITY_SAMPLE_TEX2D(tex, uv)
#endif
```

### 6.2 Mobile 优化策略

| 功能 | Desktop | Mobile |
|------|---------|--------|
| Shadow Variants | 完整支持 | 跳过 |
| Lighting Model | 完整 Toon | 简化光照 |
| Effect Chains | 完整效果 | 减少效果 |
| 变体数量 | 大量 | 精简 |

### 6.3 VRChat 集成

| 集成点 | 支持情况 |
|--------|---------|
| VRC LightVolumes | ✅ v2.0.1+ 支持 |
| Quest 兼容 | ✅ Mobile 变体 |
| 阴影投射/接受 | ✅ Shadow Caster/Meta Pass |
| Stencil Mask | ✅ VRChat 常用技术 |

---

## 7. 优缺点分析

### 7.1 优点

| 优点 | 分析 |
|------|------|
| **模块化效果系统** | `drawing` struct 模式使效果可组合、可复用 |
| **统一命名规范** | 前缀系统使属性组织清晰，易于维护 |
| **多透明度模式** | 4 种透明度模式覆盖所有使用场景 |
| **跨平台抽象** | 内置 URP/BRP 兼容层，减少重复代码 |
| **丰富的专业效果** | Fur/Water/Grass/Gem/Particle 五大专业系统 |
| **Editor 工具完善** | 自定义 Inspector、材质转换、构建优化 |
| **持续维护** | 持续更新 |

### 7.2 缺点

| 缺点 | 影响 | 严重度 |
|------|------|--------|
| **基于 Unlit** | 不是真正的 PBR，金属/粗糙度系统非标准 | ⚠️ 中 |
| **Geometry Shader 依赖** | FakeFur 不支持 Quest/移动端 | ⚠️ 中 |
| **文档语言** | 主要为日语，英文文档有限 | ⚠️ 低 |
| **社区规模** | 相对较小众 | ⚠️ 低 |

---

## 8. 与 lilToon/SCSS 对比

### 8.1 功能对比矩阵

| 特性 | UnlitWF | lilToon | SCSS |
|------|---------|--------|------|
| **定位** | Unlit 扩展 | 全功能 PBR | Cel Shader |
| **Toon 阴影** | ✅ 阶梯阴影 | ✅ 阶梯/平滑 | ✅ 双阴影系统 |
| **Outline** | ✅ 多种模式 | ✅ 内置 | ✅ 多种 |
| **Fur 毛发** | ✅ Geometry | ✅ 噪声采样 | ❌ |
| **Water 水面** | ✅ 波浪+焦散 | ⚠️ 基础 | ❌ |
| **Gem 宝石** | ✅ Flake 效果 | ⚠️ 折射 | ❌ |
| **PBR 支持** | ⚠️ 有限 | ✅ 完整 | ❌ |
| **Matcap** | ✅ 多种模式 | ✅ | ✅ |
| **Dissolve** | ✅ | ✅ | ✅ |
| **Quest 支持** | ✅ Mobile 变体 | ✅ | ✅ |
| **文档语言** | 日语为主 | 中文/日文 | 日语 |

### 8.2 适用场景分析

| 场景 | 推荐 Shader | 原因 |
|------|------------|------|
| **Avatar 通用** | lilToon | 全功能、文档完善、社区大 |
| **Cel Shader 优先** | SCSS | 双阴影系统、UV 服装切换 |
| **独特效果需求** | UnlitWF | Fur/Water/Grass/Gem 专业系统 |
| **日系动漫风格** | SCSS / lilToon | 专用 Cel Shader |
| **水/宝石特效** | UnlitWF | 专用效果系统 |

### 8.3 核心差异总结

| 维度 | UnlitWF | lilToon |
|------|---------|---------|
| **设计理念** | Unlit 基础上添加效果 | 完整 PBR + Toon 扩展 |
| **渲染基础** | Unlit（无光照计算基础） | Standard/PBR |
| **效果深度** | Fur/Water/Grass/Gem 深入 | 通用功能全面 |
| **社区生态** | 较小众 | 全球最大 VRChat Shader |

---

## 9. VRChat 适用性

### 9.1 平台适用性

| 平台 | 适用性 | 推荐变体 |
|------|--------|---------|
| **PC Avatar** | ✅ 非常适合 | Base UnToon / PowerCap / TriShade |
| **PC World** | ✅ 适合 | Water / Grass / Gem 系统 |
| **Quest Avatar** | ⚠️ 有限支持 | Mobile 变体，功能减少 |
| **Quest World** | ⚠️ 有限支持 | 避免 FakeFur / Tessellation |

### 9.2 整体评价

| 维度 | 评分 | 说明 |
|------|------|------|
| **功能完整性** | ★★★★☆ | 专业效果系统丰富 |
| **代码质量** | ★★★★☆ | 模块化、命名规范 |
| **文档完整性** | ★★★☆☆ | 日语为主，DeepWiki 完整 |
| **VRChat 集成** | ★★★★☆ | Quest 支持、LightVolumes |
| **社区生态** | ★★★☆☆ | 较小众，主要日本用户 |
| **维护活跃度** | ★★★★★ | 持续更新 |

### 9.3 定位总结

**UnlitWF 是一套专注于 Unlit 扩展的专业效果 Shader 套件**，而非通用的 PBR 替代方案。

- **优势场景**：需要 Fur/Water/Grass/Gem 等专业效果的 Avatar/World 创作
- **不适合**：追求标准 PBR 工作流、金属/粗糙度精确控制的场景
- **定位差异**：与 lilToon（全能型）形成互补，而非直接竞争

---

## 相关文档

- `memory/avatar/shader/index.md` — Shader 知识库索引
- `memory/avatar/shader/liltoon/` — lilToon 详细文档
- `memory/avatar/shader/scss/` — SCSS 详细文档