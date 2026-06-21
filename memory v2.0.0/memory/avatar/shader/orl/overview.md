---
title: ORL Shaders 概览
category: avatar
subcategory: shader

knowledge_level: applied
status: active

tags:
  - avatar
  - shader
  - orl
  - liltoon
  - json
  - light

aliases:
  - "着色器"

related:
  - shader-list.md
  - configurable.md
  - comparison.md

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: v7.2.0 (2026-01-24)
last_review: 2026-06-21
confidence: Medium
---
# ORL Shaders 概览


## 项目信息

| 项目 | 内容 |
|------|------|
| **名称** | orels Unity Shaders (ORL Shaders) |
| **发布时间** | 2024年（持续更新） |
| **最新功能** | Snow Coverage Shader (v7.2.0) |

## 定位

orels Unity Shaders - 模块化 VRChat World 着色器套件。

> **注意**: ORL 主要面向 World 开发，Avatar 开发推荐使用 lilToon。

ORL Shaders 是 **VRChat World 开发专用** 的模块化着色器套件，核心优势在于：

1. **Configurable Shader 系统** - 可自由组合功能模块
2. **丰富的 VFX 特效库** - 护盾、激光、溶解等
3. **专业的 PBR 实现** - Parallax OM、GSAA、Mobile Tonemapping
4. **深度 VRChat 集成** - Shader Fallback、VRCLightVolumes、Camera View 控制


## 安装方式

### VCC 一键安装（推荐）

```
https://orels1.github.io/orels-Unity-Shaders/index.json
```

1. 打开 VRChat Creator Companion (VCC)
2. 进入 Project Management
3. 添加 Community Repository
4. 搜索并安装 "ORL Shaders"

### 手动安装

1. VCC → Project Management → Add Repository
2. 粘贴上述 URL
3. 在 Project Management 中添加 "ORL Shaders" 包

## Shader 分类总览

| 类别 | 数量 | 说明 |
|------|------|------|
| **Standard Shaders (PBR)** | 22 | 基础 PBR + 功能扩展 |
| **Toon Shaders** | 3 | 卡通渲染（v1/v2） |
| **Special Shaders** | 1 | 积雪覆盖 |
| **VFX Shaders** | 9 | 视觉效果特效 |
| **UI Shaders** | 5 | UI 专用着色器 |
| **Configurable** | 模块化 | 可组合的 Uber Shader |

### Standard Shaders (PBR) 列表

| Shader | 功能 |
|--------|------|
| Base Shader | PBR 核心，包含 Parallax/Details/VRChat Features |
| AudioLink | 音频响应（5种模式） |
| Color Randomisation | 颜色随机化 |
| Decals | 贴花系统 |
| Dissolve | 溶解效果 |
| Dither Fade | 抖动淡入淡出 |
| Foliage | 植被专用（SSS近似） |
| Glass | 玻璃材质 |
| Hotspotting | 热区效果 |
| Layered Material | 分层材质 |
| Layered Parallax | 分层视差 |
| LTCGI | LTCGI 光照集成 |
| AreaLit | 区域光照 |
| Neon Light | 霓虹灯光 |
| Puddles | 水坑/积水 |
| Pulse | 脉冲效果 |
| Tessellated Displacement | 细分位移 |
| Triplanar Effects | 三平面映射 |
| Vertex Animation | 顶点动画 |
| Vertical Fog | 垂直雾效 |
| Video Screen | 视频屏幕 |
| VRSL GI | VRSL 全局光照 |

### VFX Shaders 列表

| Shader | 功能 |
|--------|------|
| Clouds | 云效果 |
| Ghost Lines | 幽灵线效果 |
| Glitch Screen | 故障屏幕效果 |
| Patterns | 图案效果 |
| Shield | 能量护盾（双层噪声+深度融合） |
| Laser | 激光效果 |
| Holographic Parallax | 全息视差 |
| Cubemap Screen | 立方体贴图屏幕 |
| Block Fader | 块状淡入淡出 |

## 核心架构

### Configurable Shader 系统

ORL 的核心创新是 **Configurable Shader**，允许用户：

- 自由组合功能模块
- 基于已有 Shader 扩展（如：Vertex Animation + LTCGI）
- 减少材质变体数量，提升 Draw Call Batching

### Shader Generator

面向 Shader 开发者的代码生成系统：

- 声明式 Shader 定义 → 自动生成 HLSL
- 支持自定义模块（.orlsource）
- 支持自定义 Lighting Models

## 版本历史

| 版本 | 主要更新 |
|------|----------|
| 7.2.0 | 新增 Snow Coverage Shader |
| 7.x | 重构 Standard Shader，添加 VRCLightVolumes 支持 |
| 6.x | Configurable Shader 系统引入 |
| 5.x | Toon Shader v2 发布 |

## 迁移指南

| 迁移路径 | 说明 |
|----------|------|
| v6 → v7 | 有专门迁移文档 |
| 旧版 → v6 | 有专门迁移文档 |
| 常规更新 | 直接覆盖即可 |

## 获取帮助

- **文档站**: shaders.orels.sh
- **Discord**: discord.gg/orels1
- **GitHub Issues**: github.com/orels1/orels-Unity-Shaders/issues

## 相关文档

- [Shader List](./shader-list.md) - 详细 Shader 列表
- [Configurable Shader](./configurable.md) - 模块化系统详解
- [Comparison](./comparison.md) - 与其他 Shader 对比