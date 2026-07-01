---
title: "Poiyomi Shaders - Quest 优化策略"
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
  - quest
  - optimization
  - mobile
  - micro
aliases:
  - "Poiyomi Quest 优化"
  - "Poiyomi Mobile"
  - "Poiyomi Micro 变体"
  - "Quest Avatar"
related:
  - "./shader-variants.md"
  - "./pro-vs-toon.md"
  - "./audiolink-integration.md"
  - "../../../../参考文献/Poiyomi/01-download-install.md"
  - "../../performance-rank.md"
  - "../../optimization-guide.md"
---

# Poiyomi Shaders — Quest 优化策略

> **Domain**: Avatar → Shader → Poiyomi → Quest 优化
> **原始参考**: `参考文献/Poiyomi/01-download-install.md` + 相关变体说明
> **状态**: 活跃(Active)

---

## 1. 概述

Quest 是 Android 移动 GPU(Adreno 650 / XR2 Gen 2),与 PC 桌面 GPU 性能差距 5-10 倍。Poiyomi 提供 **Micro 变体**专为 Quest 优化,但**仅选变体不够**,还需要**手动关闭/调低**多项重效果。

本文档总结 Quest Avatar 的 **Material 配置 + Avatar 整体优化**最佳实践。

---

## 2. 变体选择(必读)

> 详见 `./shader-variants.md`

| 变体 | Quest 性能 | 推荐度 |
|------|-----------|--------|
| **Micro** | ⭐⭐⭐⭐ | ✅ **首选** |
| **Mega** | ⭐⭐ | ⚠️ 边缘可用 |
| **Giga** | ⭐ | ❌ 不推荐 |
| **Tera** | ⭐ | ❌ 不推荐 |
| **Nano** | ⭐⭐⭐⭐⭐ | ✅ 性能极致 |

**硬性规则**: Quest Avatar **必须用 Micro 或 Nano 变体**。

---

## 3. Material 配置禁用清单

### 3.1 必须禁用的功能

| 功能 | Quest 影响 | 禁用方法 |
|------|-----------|----------|
| **Grab Pass** | 严重卡顿(每帧截图) | 不用 `.poiyomi/Poiyomi Toon Grab Pass` 变体 |
| **Poiyomi Fur 1-31 层** | 几何激增 | Micro 变体默认禁用 |
| **ShatterWave** | 顶点计算密集 | 关闭 Toggle |
| **Geometric Dissolve** | 几何重建 | 关闭 Toggle |
| **Voronoi 3D** | 计算密集 | 用 2D 替代 |
| **Constellation** | 多 Pass | 关闭或限制数量 |
| **Internal Parallax** | 多次纹理采样 | 关闭 |
| **AL Spectrum** | 频谱计算 | 改用基础 AudioLink |

### 3.2 调低参数(非完全禁用)

| 参数 | PC 默认 | Quest 推荐 |
|------|---------|-----------|
| **Outline Width** | 0.005 | 0.003 |
| **Shadow Layers** | 3 | 1 |
| **AudioLink Band** | 5 | 4 (Micro 限制) |
| **Light Volumes Sample Count** | 16 | 8 |
| **Texture Quality** | 完整 | 512px 上限 |
| **Material Count** | 10+ | ≤ 5 |
| **Material 共享率** | 50% | ≥ 80% |

### 3.3 保留的功能(对 Quest 安全)

| 功能 | 备注 |
|------|------|
| **基础 Toon 阴影** | Texture Ramp |
| **Outline** | 简化模式 |
| **AudioLink 基础** | 4 频段 |
| **Decals(贴花)** | 1-2 槽 |
| **Color Adjust** | OKLab/HSV |
| **Vertex Options 基础** | Translation/Scale/Rotation |
| **Rim Lighting** | 单层 |

---

## 4. Avatar 整体优化

### 4.1 材质数量控制

| 等级 | Quest 上限 | PC 上限 |
|------|-----------|---------|
| **Excellent** | 5 | 10 |
| **Good** | 8 | 15 |
| **Medium** | 10 | 20 |
| **Poor** | 15+ | 30+ |

**策略**: 用 Poiyomi Pro 的 Modular Shader System / Global Mask 减少 Material 数量(详见 `./modular-system.md`)。

### 4.2 纹理预算

| 等级 | 纹理总大小 | 单张上限 |
|------|-----------|----------|
| **Quest Good** | < 10 MB | 1 MB |
| **Quest Excellent** | < 5 MB | 512 KB |

**优化工具**:
- **Avatar Compressor (LAC)**: 自动压缩 → `memory/avatar/lac-avatar-compressor.md`
- **Avatar Optimizer (AAO)**: 通用优化 → `memory/avatar/avatar-optimizer.md`

### 4.3 多边形预算

| Avatar 等级 | 三角形 | 网格数 |
|-------------|--------|--------|
| **Quest Good** | < 32,000 | ≤ 5 |
| **Quest Excellent** | < 20,000 | ≤ 3 |

详见 `memory/avatar/performance-rank.md` §Quest 等级。

### 4.4 物理骨骼预算

| 项 | Quest 上限 |
|----|-----------|
| **PhysBone 数量** | 8 (官方默认上限) |
| **PhysBone Transform** | 64 (官方) |
| **Particle System** | 极有限 |

详见 `memory/avatar/avatar-dynamic-bone-limits.md` + `memory/avatar/avatar-particle-system-limits.md`。

---

## 5. PC/Quest 跨平台发布

### 5.1 双 Material 策略

```text
Avatar
├── PC Materials/        ← Mega/Giga/Tera 变体
│   ├── Body.mat
│   ├── Hair.mat
│   └── ...
└── Quest Materials/    ← Micro/Nano 变体(同结构)
    ├── Body.mat
    ├── Hair.mat
    └── ...
```

**切换方法**:
1. 手动复制 Material
2. 切换 Shader 为目标变体
3. 调整参数(同名属性保留)

### 5.2 EasyQuestSwitch 自动化

**EasyQuestSwitch** 是 VRChat 官方工具,可一键切换 PC/Quest 变体。

详见 `memory/platform/easyquestswitch.md`。

```text
安装 EasyQuestSwitch VPM:
https://packages.vrchat.com/

用法:
1. Tools → EasyQuestSwitch
2. 添加 PC Material 和 Quest Material 映射
3. 触发切换 → 自动替换
```

### 5.3 Poiyomi 与 EasyQuestSwitch 集成

Poiyomi 变体本身与 EasyQuestSwitch **直接兼容**,因为变体名都是合法的 Shader 名。

---

## 6. VRC Light Volumes 集成

Quest 也支持 **VRC Light Volumes**(2026.1+),但需要调低参数:

| 参数 | PC 默认 | Quest 推荐 |
|------|---------|-----------|
| **Sample Count** | 16 | 8 |
| **Volume Size** | 1.0 | 0.5 |
| **Volume Light Count** | 4 | 2 |

详见 `memory/world/vrc-light-volumes.md` §Quest 章节。

---

## 7. 常见 Quest 性能问题

| 问题 | 原因 | 解决 |
|------|------|------|
| **整体卡顿** | Material 过多 | 合并 Material / 用 Modular |
| **特定 Mesh 卡顿** | 复杂 Shader 效果 | 简化变体 + 关效果 |
| **粒子卡顿** | Particle System 过多 | 减少 Particle + 简化 |
| **阴影卡顿** | 实时光照过多 | 烘焙光照 + 减少实时光 |
| **Outline 卡顿** | 描边过粗 | 调低 Width |
| **AudioLink 卡顿** | AL Spectrum | 改基础 AudioLink |
| **First Frame 黑屏** | Shader 编译 | 用 Shader Variant 预编译 |

---

## 8. 测试方法

### 8.1 性能测试

```text
1. 打包 Avatar 到 Quest
2. 进入任意 World
3. 打开 VRChat 内置 Performance Rank
4. 检查指标:
   - Shader Complexity
   - Material Slot Count
   - Particle System Count
   - PhysBone Count
5. 目标: Excellent 或 Good
```

### 8.2 视觉测试

```text
1. 验证基础 Toon 效果正常
2. 验证 Outline 正常
3. 验证 AudioLink 响应(需 World 有 Controller)
4. 验证 Light Volumes(如有)
5. 验证无明显闪烁/穿模
```

---

## 9. 实战陷阱

| 错误 | 症状 | 修复 |
|------|------|------|
| **PC Avatar 直接用 Mega 变体上 Quest** | 严重卡顿 | 改用 Micro + 关闭 Pro 效果 |
| **Quest 启用 Grab Pass** | 帧率 1-5 | 切回非 Grab Pass 变体 |
| **AudioLink 5 频段** | Micro 自动降到 4 频段 | OK,无需修复 |
| **Quest 用了 Geometric Dissolve** | 编译警告 + 卡顿 | 关闭 Toggle |
| **多 Material 切换变体** | 性能提升但参数错位 | 用 EasyQuestSwitch 自动化 |
| **忘了调低 Light Volumes** | Quest 边缘卡顿 | 调低 Sample Count |

---

## 10. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Poiyomi Shader Variants** | `./shader-variants.md` |
| **Poiyomi Pro vs Toon** | `./pro-vs-toon.md` |
| **Poiyomi AudioLink 集成** | `./audiolink-integration.md` |
| **Poiyomi Modular System** | `./modular-system.md` |
| **VRChat Performance Rank** | `memory/avatar/performance-rank.md` |
| **Avatar 优化指南** | `memory/avatar/optimization-guide.md` |
| **EasyQuestSwitch** | `memory/platform/easyquestswitch.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **上游版本** | Poiyomi 10.0 |
| **目标平台** | Quest 2/3/Pro (Android) |
| **评审状态** | Stage 2.6 完成 |
| **下一步** | Stage 2.7 Poiyomi vs LilToon |
