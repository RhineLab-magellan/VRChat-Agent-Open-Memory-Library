# Graphlit 节点式 Shader 编辑器

> VRChat World/Object 高质量 PBR 着色器编辑器

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **项目地址** | https://github.com/z3y/Graphlit |
| **类型** | 节点式 Shader 编辑器（非预设着色器） |
| **语言/架构** | C# (68.3%) + HLSL (29.6%) |
| **许可证** | MIT License |
| **开发者** | z3y |
| **Stars** | 106 |
| **最新版本** | v2.7.2 (2026-02-24) |
| **Unity 版本** | 2022.3+ |
| **渲染管线** | Built-in + URP（URP 支持不完整） |

**VPM 安装源**：`https://z3y.github.io/vpm-package-listing/`

**VRChat 测试世界**：`wrld_6fd2e6c4-d4f2-49ea-8cf6-ce7ccb0e7111`

---

## 核心定位

Graphlit **不是**开箱即用的预设着色器（如 lilToon）。它是一个完整的**节点式 Shader 编辑器**，允许通过可视化节点图创建自定义 PBR 或 Toon 着色器。

| 对比 | lilToon | Graphlit |
|------|---------|----------|
| 使用方式 | 调整参数，预设逻辑 | 构建节点图，完全可定制 |
| 目标场景 | Avatar | World/Object |
| 学习曲线 | 低 | 高 |
| PBR 精度 | 中等 | 业界领先 |

---

## 内置 Shader

| Shader | 说明 |
|--------|------|
| `Graphlit/Lit` | 主 PBR Shader（推荐），由节点图构建 |
| `Graphlit/Standard Compatible` | 标准输入的 PBR Shader |

---

## PBR 特性（最强项）

Graphlit 基于 **CoreRP + Google Filament + OpenPBR**，提供 VRChat 可用的最高精度 PBR 实现：

### 光照与阴影

| 特性 | 说明 |
|------|------|
| **Inverse Square Falloff** | 真实的点/聚光灯衰减（v2.0+） |
| **PCF Shadow Filtering** | 点/聚光灯软阴影 |
| **Contact Hardening** | 接触硬化阴影 |
| **Micro Shadowing** | 微阴影 |

### PBR 精度增强

| 特性 | 说明 |
|------|------|
| **Specular Occlusion** | 基于 AO 的镜面光遮蔽 |
| **Horizon Occlusion** | 地平线遮蔽，减少边缘漏光 |
| **F82 Metallic Edge Tint** | 金属边缘着色 |
| **Energy Conservation** | 能量守恒 |
| **Alpha To Coverage** | 透明抗锯齿 |
| **Geometric Specular AA** | 几何镜面抗锯齿 |

### 高级材质

| 特性 | 说明 |
|------|------|
| **Coat（Clear Coat）** | 清漆层，用于车漆等效果 |
| **Thin Film Iridescence** | 薄膜虹彩（蛋白石/贝母效果） |
| **Multi Bounce AO** | 多弹跳 AO |

### 光照系统集成

| 系统 | 支持状态 |
|------|----------|
| **Bakery GPU Lightmapper** | ✅ MonoSH、Lightmapped Specular、Bicubic Lightmap |
| **LTCGI** | ✅ 官方支持 |
| **AreaLit** | ✅ 官方支持 |
| **VRC Light Volumes v2.0** | ✅ 官方支持 |
| **Clustered BIRP** | ✅ 官方支持 |
| **Ray Tracing** | ✅ via VRCTrace |

### VRChat 特定功能

| 功能 | 说明 |
|------|------|
| **Mirror Reflection Mode** | 采样 VRChat 镜面纹理（v2.0+） |
| **Improved Box Projection** | 改进的盒投影 |

---

## 节点编辑器功能

| 功能 | 说明 |
|------|------|
| **Live Preview** | 节点上直接预览着色效果 |
| **Register/Fetch 变量节点** | 无线连接，避免节点图凌乱 |
| **Varyings Packing** | 自动打包 varyings（如 uv0+uv1 → float4） |
| **Keyword Properties Pass Flags** | 减少着色器变体数量 |
| **自定义函数节点** | 支持 HLSL 代码内联或外部文件引用 |
| **节点热键** | G/B 等快捷键提升效率 |
| **分组复制** | 支持跨 Graph 复制节点组 |

### Master Node 配置

- **Shader Name**：生成的着色器名称
- **Custom Editor**：自定义编辑器
- **Fallback**：后备着色器
- **Graph Precision**：默认精度
- **Outline Pass**：创建轮廓线 Pass
- **Stencil**：模板选项

### Lit Target 选项

- Normal dropoff 设置
- Specular Highlights and Reflections 开关
- Bakery Mono SH、Lightmapped Specular、Bicubic Lightmap 特性

### Unlit Target 选项

- Custom Lighting 模式：生成完整光照 Pass 和关键词

---

## Toon Shader 实现

Graphlit 的 Toon Shader 通过 **Custom Lighting** 模式实现，区别于预设输出：

```
Custom Lighting = Unlit Graph + Main Light Node + Lightmap UVs + Blend Final Color
```

### 创建方式

`Right Click → Create → Graphlit → Custom Graph` 或 `Toon Graph`

### 核心节点

| 节点 | 说明 |
|------|------|
| **Main Light** | 光照颜色、方向、阴影衰减、距离衰减 |
| **Toon Light** | 基于 Open Lit 的 Toon 光照 |
| **Toon Shadow Layers** | 分层阴影 |
| **Stylized Specular** | 风格化高光 |
| **Blend Final Color** | 处理透明度和 Meta Pass |

### 轮廓线设置

1. Master Node 启用 Outline Pass
2. 使用 Outline Scale 节点基于顶点法线缩放
3. Outline Pass Branch 自定义轮廓线 Pass 输出
4. Sample Texture 2D LOD 采样轮廓线遮罩纹理

### 示例

- `Packages/com.z3y.graphlit/Shaders/Toon.graphlit` — Toon 示例
- `Packages/com.z3y.graphlit/Shaders/Samples/CustomPBR.graphlit` — PBR 示例

---

## 优点

1. **PBR 质量天花板**：基于 Filament 的 PBR 实现是 VRChat 可用的最高精度
2. **光照系统集成最全面**：Bakery + LTCGI + AreaLit + VRC Light Volumes 四大系统全覆盖
3. **完全可定制**：节点编辑器意味着可以做任何事情，没有预设限制
4. **纹理打包工具内置**：解决 PBR 多图问题的工具随项目提供
5. **变体优化**：Keyword Pass Flags 显著减少编译变体数量
6. **活跃开发**：78 个 Release，最近更新 2026-02-24
7. **MIT 许可证**：完全免费，无商业限制

---

## 缺点与局限性

### 核心定位问题

| 问题 | 说明 |
|------|------|
| ❌ **非 Avatar 着色器** | 主要面向 World/Object，无 fur/dissolve/stencil 面具等功能 |
| ❌ **节点图门槛高** | 需要理解 shader 编程概念，不适合非技术用户 |
| ❌ **预设数量少** | 没有一键预设系统，需要手动构建所有效果 |
| ❌ **Toon 需自行构建** | 相比 lilToon 的预设 Toon，Graphlit 的 Toon 效果完全从零开始 |

### 技术局限性

| 问题 | 说明 |
|------|------|
| ❌ **URP 支持不完整** | Dots、Decals、Rendering Layers、SSAO 尚未实现 |
| ❌ **Mirror Mode Normal 限制** | Mirror reflection 模式下法线不生效 |
| ❌ **Specular Occlusion 依赖烘焙** | 需要光照烘焙才能生效，实时模式不可用 |
| ❌ **Custom Function 解析器较弱** | 数组等复杂输入可能解析失败 |
| ❌ **文档质量一般** | 大量知识依赖 Discord 社区 |

---

## 与 lilToon 对比

| 维度 | Graphlit | lilToon |
|------|----------|---------|
| **定位** | 节点编辑器（通用） | 预设着色器（Avatar） |
| **学习曲线** | 高 | 低 |
| **PBR 精度** | ⭐⭐⭐⭐⭐ 业界领先 | ⭐⭐⭐ 中等 |
| **Toon 效果** | ⭐⭐⭐ 需自行构建 | ⭐⭐⭐⭐⭐ 预设丰富 |
| **光照集成** | ⭐⭐⭐⭐⭐ Bakery/LTCGI/AreaLit/VLCV 全部 | ⭐⭐⭐⭐ LTCGI/VRC LV 支持 |
| **Avatar 适配** | ❌ 不推荐 | ✅ 首选 |
| **World/Object 适配** | ✅ 强烈推荐 | ⚠️ 可用但非最优 |
| **Fur 毛发** | ❌ | ✅ |
| **Dissolve** | ❌ | ✅ |
| **AudioLink** | 需手动集成 | ✅ 内置 |
| **许可证** | MIT | MIT |
| **开发活跃度** | 高（78 releases） | 高 |

---

## 适用场景建议

### ✅ Graphlit 最适合的场景

1. **高质量 World 物体着色**：需要 Bakery 烘焙、LTCGI、VRCLightVolumes 集成的 World 物件
2. **专业光照效果**：Clear Coat、Thin Film Iridescence、Contact Hardening 等高级 PBR 效果
3. **自定义 Toon Shader**：需要完全控制 Toon 着色逻辑的高级用户
4. **Shader 开发者**：学习 PBR 实现原理，或创建专用着色器

### ❌ 不适合的场景

1. **Avatar 制作**：lilToon 依然是首选，有完整的 Avatar 功能套件
2. **快速原型**：预设系统缺失，不适合快速迭代
3. **非技术用户**：节点图编辑器对新手不友好

---

## 相关文档

- `memory/avatar/shader/liltoon/` — lilToon Avatar 着色器
- `memory/world/bakery/` — Bakery GPU Lightmapper
- `memory/hybrid/osc-protocol.md` — AudioLink 协议（Graphlit Toon 需手动集成）