---
title: SCSS (Silent's Cel Shading Shader) 分析报告
category: avatar
subcategory: shader

knowledge_level: applied
status: active

tags:
  - avatar
  - shader
  - scss
  - light

aliases:
  - "着色器"
  - "SCSS"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-21
maintenance_status: "4 年无重大更新,2026-06-21 复核确认"
confidence: Medium
---
# SCSS (Silent's Cel Shading Shader) 分析报告

**来源**: Silent 创作
**创建时间**: 项目最初托管于 GitLab，后同步至 GitHub
**语言**: HLSL (36.1%), C# (35.5%), ShaderLab (28.4%)

---

## 概述

SCSS (Silent's Cel Shading Shaders) 是一款专为 Unity 设计的 Cel Shading 着色器，支持 Forward Rendering。该项目最初托管于 GitLab，后同步至 GitHub。提供详细的 Wiki 文档和手动设置指南。

**设计哲学**: 提供类似工具箱的模块化功能，用户可以选择性使用，而非强制全部启用。

---

## 核心特性分析

### 1. 渲染模式系统

| 模式 | 说明 | VRChat 适用性 |
|------|------|---------------|
| **Opaque** | 实体材质，无透明 | ✅ 最快，推荐 |
| **Cutout** | Alpha to coverage，支持锐利/抖动边缘 | ✅ 常用 |
| **Fade** | Alpha 混合，透明区域完全透明 | ⚠️ 排序问题 |
| **Transparent** | 预乘 alpha，matcap/specular 仍可见 | ✅ 透明物体 |
| **Additive** | 叠加模式，无深度写入 | ⚠️ 特效 |
| **Custom** | 自定义混合参数 | 🔽 高级 |

### 2. 双阴影系统: Lightramp vs Crosstone

#### Lightramp（纹理渐变方式）
- **Lighting Ramp**: 纹理定义光影过渡（lightwarp/ramp）
- 支持自定义渐变曲线
- 与 Unity 照明系统集成
- 适合有特定风格需求的用户

#### Crosstone（参数化方式）
- **Tone Blending Mode**: Combined（乘法）/ Separate（分离）
- **Shading Breakpoint/Width**: 控制阴影转折点
- **Shading Tone**: RGB 控制色调，Alpha 控制转折点
- 适合不需要额外纹理资源的场景

**对比**: Crosstone 比 Lightramp 更灵活，无需准备 ramp 纹理，但 Lightramp 可实现更细腻的渐变效果。

### 3. PBR 集成

| 功能 | 说明 |
|------|------|
| **金属度/光滑度** | 与 Unity Standard 一致 |
| **高光类型** | Standard / Cloth / Anisotropic / Cel / Cel Strand |
| **Detail Maps** | 叠加细节纹理（不同缩放） |
| **Secondary UV** | 独立 UV 通道用于贴花 |

### 4. NPR 特性

#### Matcap 系统
- 4 个 Matcap 槽位
- **Blend Modes**: Additive / Median / Multiply
- **Space**: World / Tangent（解决 VR 头部转动问题）
- 支持遮罩控制区域

#### Rim Lighting
- **Lit**: 光照前应用
- **Ambient**: 光照后应用（阴影中也可见）
- **AmbientAlt**: 仅影响光照计算
- **Light Direction Mask**: 双向分割

### 5. 轮廓线系统

| 特性 | 说明 |
|------|------|
| **VR 优化** | 距离自适应缩小（防止近处穿帮） |
| **顶点色控制** | R=宽度, G=Y位置, B=深度偏移 |
| **轮廓遮罩** | 纹理控制轮廓宽度 |
| **深度偏移** | 避免复杂物体穿帮 |

### 6. 高级功能

#### Subsurface Scattering (SSS)
- Thickness Map 控制散射强度
- Scattering Color/Intensity/Power/Distortion
- 适用于皮肤和布料

#### Detail Maps
- 细节贴图叠加（不同平铺）
- Secondary UV 支持
- 细节法线（可用于毛绒布料）

#### Animation System
- 纹理动画（帧动画）
- 支持图集行列配置
- 可通过 Unity Animation 驱动

#### Vanishing
- 相机距离渐隐
- Start/End 双边界控制

---

## VRChat 特有功能

### 1. Simple Inventory System（衣物切换）

**核心原理**: 基于 UV 位置识别物品，通过顶点位移实现无缝裁剪

**优势对比**:
| 方法 | Draw Calls | 性能 | 限制 |
|------|-----------|------|------|
| **SCSS UV 切换** | 1 | 最低 | 需要 UV 编辑 |
| 分离网格 | N+1 | 较高 | 合并后更优 |
| ShapeKeys | - | 最高 | 每激活都昂贵 |
| 骨骼缩放 | - | 中 | 约束延迟问题 |
| 材质槽+隐形 | N+1 | 较高 | 每槽=1 drawcall |
| Clipping Mask | 1 | 中 | 需 Cutout 模式 |
| ID Mask | 1 | 中 | 额外纹理 |

**设计建议**:
- 避免与 ShapeKey 合并网格
- stride 建议 1（无平铺图案时）
- 推荐布局: Face / Body / Clothes(combined)

### 2. AudioLink 集成

**功能**:
- 4 个频段独立控制
- **Mode**: Soft Pulse / VU-meter
- **Time Range**: 历史采样范围
- Fallback BPM（无 AudioLink 时）
- Light Sensitivity（光敏发射）

**对比 lilToon**: 功能类似，但 SCSS 提供了更详细的每频段配置。

### 3. Shader Baking

**功能**:
- 生成优化变体（移除未使用特性）
- 锁定所有设置
- 减小 Build Size
- 轻微性能提升

---

## 高级选项

| 选项 | 说明 |
|------|------|
| **Albedo Alpha Mode** | Transparency / Smoothness / Clipping Mask |
| **Vertex Colour Mode** | Colour / Outline / Additional Data |
| **Light Ramp Type** | Horizontal / Vertical / None |
| **Pixel Art Mode** | 像素风格渲染（不失真） |
| **Lighting Calculation** | Unbiased / Cubed / Standard / Directional / Biased |
| **Indirect Shading Type** | Dynamic / Directional / Flatten |
| **Light Skew** | 灯光方向权重调整 |

---

## 优点分析

### ✅ 优势

1. **模块化设计**
   - Simple/Normal/Advanced 模式分层显示
   - 新手友好，可逐步探索
   - 不启用不会破坏效果

2. **双阴影系统**
   - Lightramp 适合细腻风格
   - Crosstone 适合快速配置
   - 两者互补

3. **强大的 Matcap 系统**
   - World/Tangent 空间切换（VR 关键）
   - 多槽位+多混合模式
   - 比多数着色器更灵活

4. **Inventory System**
   - 零额外 draw call
   - 不依赖 Cutout 模式
   - 比 ShapeKey 性能更好

5. **VR 优化的 Outline**
   - 距离自适应
   - 顶点色精细控制
   - 深度偏移防止穿帮

6. **详细的文档**
   - Wiki 手动设置指南
   - 传输指南（UTS2 迁移）
   - 其他教程（Post-Processing, Standard Shader 等）

7. **开源透明**
   - 源码可审计
   - 社区可贡献

---

## 缺点分析

### ❌ 劣势

1. **BRP Only**
   - 仅支持 Forward Rendering
   - 不支持 URP/HDRP（相比 lilToon 的全管线支持）

2. **文档分散**
   - 主要文档在 GitLab Wiki
   - GitHub README 信息较少
   - 可能导致用户困惑

3. **学习曲线**
   - 设置项繁多
   - Simple/Normal/Advanced 分层可能仍然复杂
   - 高级功能需要理解 PBR/NPR 概念

4. **活跃度**
   - 2 位贡献者
   - 相比 lilToon 社区较小

5. **缺少内置预设**
   - 没有一键预设系统
   - 需要手动配置
   - 不如 lilToon 友好

6. **AudioLink 文档不完整**
   - Wiki 中 AudioLink 页面无法访问
   - 需参考其他资源

7. **不支持 GPU Instancing 优化**
   - 相比某些现代着色器

8. **Outline 性能**
   - 距离自适应虽好，但可能有性能开销
   - 高多边形模型影响更大

---

## 与 lilToon 对比

| 维度 | SCSS | lilToon |
|------|------|---------|
| **渲染管线** | BRP Only | BRP/URP/HDRP 全支持 |
| **学习难度** | 中高 | 低 |
| **预设系统** | ❌ 无 | ✅ 完善 |
| **文档质量** | ✅ 详细 Wiki | ✅ 官方文档 |
| **社区资源** | 较少 | 丰富 |
| **Inventory System** | ✅ UV 方式 | ⚠️ 需第三方 |
| **Matcap 灵活性** | ✅ 多槽位+多模式 | 中等 |
| **Outline VR 优化** | ✅ 距离自适应 | ✅ 类似 |
| **AudioLink** | ✅ 每频段配置 | ✅ 完善 |
| **Shader Baking** | ✅ 有 | ✅ 有 |
| **活跃维护** | 一般 | 活跃 |

---

## 使用场景推荐

### 推荐使用 SCSS 的场景

1. **需要精细 Matcap 控制的 Avatar**
   - 多层 Matcap 效果
   - World/Tangent 空间切换

2. **服装切换（Inventory）需求**
   - 零额外 draw call
   - 不需要 ShapeKey

3. **复杂 Outline 控制**
   - 顶点色精细调节
   - VR 近距离穿帮防止

4. **双色调系统（Crosstone）**
   - 快速配置，无需 ramp 纹理
   - 精确阴影配色

### 推荐使用 lilToon 的场景

1. **新手用户** — 一键预设，简单上手
2. **URP/HDRP 项目** — SCSS 不支持
3. **需要大量社区资源** — 教程/预设丰富
4. **快速迭代** — 内置优化和容量削减

---

## 性能评估

| 指标 | SCSS | lilToon |
|------|------|---------|
| **基础消耗** | 中 | 低 |
| **功能复杂度** | 高 | 中 |
| **Baking 效果** | ✅ 有效 | ✅ 有效 |
| **VR 优化** | ✅ 优秀 | ✅ 良好 |
| **Inventory 效率** | ✅ 极高 | N/A |

---

## 总结

**SCSS 是一款功能全面、VR 优化的 Cel Shading 着色器**，适合需要精细控制的进阶用户。其 Inventory System 和 Matcap 系统是其独特优势，但相比 lilToon 的易用性和社区资源，仍有一定差距。

**定位**: 中高级用户的 Cel Shading 工具箱，而非新手友好的一站式解决方案。

---

## 相关资源

| 资源 | 链接 |
|------|------|
| **GitHub** | https://github.com/s-ilent/scss |
| **GitLab** | https://gitlab.com/s-ilent/SCSS |
| **文档** | https://gitlab.com/s-ilent/SCSS/-/wikis/Manual/Setting-Overview |
| **下载** | https://gitlab.com/s-ilent/SCSS/-/archive/master/SCSS-master.zip |

---