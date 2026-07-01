---
title: "Poiyomi Shaders - 5 个变体详解"
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
  - variants
  - micro
  - quest
aliases:
  - "Poiyomi 变体"
  - "Poiyomi Nano/Micro/Mega/Giga/Tera"
  - "Poiyomi Quest 优化"
related:
  - "./installation.md"
  - "./pro-vs-toon.md"
  - "./quest-optimization.md"
  - "../../../../参考文献/Poiyomi/01-download-install.md"
  - "../../../../参考文献/Poiyomi/02-render-preset.md"
---

# Poiyomi Shaders — 5 个变体详解

> **Domain**: Avatar → Shader → Poiyomi → 变体选择
> **原始参考**: `参考文献/Poiyomi/01-download-install.md` + `02-render-preset.md`
> **状态**: 活跃(Active)

---

## 1. 概述

Poiyomi 10.0 引入 **5 个分级变体**,按 Shader 复杂度和性能分级,覆盖 PC 顶级机 → Quest 移动端的全部场景。本文档帮你**选择最合适的变体**,避免 Quest Avatar 卡顿或 PC 高端机效果平平。

---

## 2. 5 个变体速查表

| 变体 | 性能评级 | 目标平台 | 适用场景 | 关键限制 |
|------|----------|----------|----------|----------|
| **Nano** | ⭐⭐⭐⭐⭐ | PC + Quest | 极简 Avatar、纯 Toon、性能优先 | 功能最少,基础效果 |
| **Micro** | ⭐⭐⭐⭐ | **Quest 首选** | Quest Avatar、移动端 | 禁用 Fur/Geometric Dissolve 等重型效果 |
| **Mega** | ⭐⭐⭐ | PC 通用 | 标准 PC Avatar、通用 | 平衡功能与性能 |
| **Giga** | ⭐⭐ | PC 高端 | 复杂 PC Avatar | 重型效果可用 |
| **Tera** | ⭐ | 顶级 PC | 顶级视觉效果 | 全部效果解锁,需要高端 GPU |

---

## 3. 变体详细对比

### 3.1 Nano(最轻量)

```hlsl
Shader: .poiyomi/Poiyomi Toon Nano
```

**特性**:
- ✅ 基础 Toon 阴影 + 颜色
- ✅ AudioLink 基础支持
- ✅ 简化 Outline
- ❌ 无 Fur / Geometric Dissolve / ShatterWave
- ❌ 无 Voronoi 3D / Constellation
- ❌ 简化后处理

**适用**:
- 性能敏感型 Avatar(低端 PC/Quest)
- 大场景、多 Avatar 同屏
- 纯 Toon 风格(无特效需求)

### 3.2 Micro(Quest 首选)

```hlsl
Shader: .poiyomi/Poiyomi Toon Micro
```

**特性**:
- ✅ Nano 全部功能
- ✅ Quest 兼容性优化
- ✅ 移动 GPU 适配(降低精度)
- ❌ 无 Poiyomi Fur 1-31 层
- ❌ 无 ShatterWave
- ❌ 无 Geometric Dissolve
- ⚠️ AudioLink 限制到 4 频段

**适用**:
- **Quest Avatar 首选**
- 移动端
- 想要在 Quest 上保留大部分 Toon 效果

**Quest 优化要点**:
- 避免使用 Grab Pass
- 避免多层 Alpha Blend
- 简化后处理效果
- 详见 `quest-optimization.md`

### 3.3 Mega(PC 通用)

```hlsl
Shader: .poiyomi/Poiyomi Toon Mega
```

**特性**:
- ✅ Micro 全部功能
- ✅ 完整 Fur 基础层
- ✅ 标准 AudioLink 5 频段
- ✅ Panosphere UV / Polar UV
- ✅ Voronoi 2D
- ⚠️ Fur 最多 5 层(非 Pro 31 层)

**适用**:
- **PC 通用 Avatar 默认选择**
- 想要效果 + 性能平衡

### 3.4 Giga(PC 高端)

```hlsl
Shader: .poiyomi/Poiyomi Pro Giga
```

**特性**:
- ✅ Mega 全部功能
- ✅ 完整 9 种 Lighting Type
- ✅ Distortion UV
- ✅ Internal Parallax
- ✅ Constellation(星空)
- ✅ Voronoi 3D
- ⚠️ 部分效果仍需 Pro 鉴权

**适用**:
- PC 中高端 Avatar
- 想要风格化视觉效果(星空、几何溶解等)

### 3.5 Tera(顶级 PC)

```hlsl
Shader: .poiyomi/Poiyomi Pro Tera
```

**特性**:
- ✅ Giga 全部功能
- ✅ 全部 Pro 效果解锁
- ✅ 完整 Modular Shader System
- ✅ Poiyomi Fur 1-31 层
- ✅ ShatterWave
- ✅ Geometric Dissolve
- ✅ 全部 9 种 Lighting Type 完整参数

**适用**:
- **顶级 PC Avatar**
- 不在意性能(高端 GPU)
- 想要 Poiyomi 全部能力

---

## 4. 决策矩阵

### 4.1 按平台

| 平台 | 推荐变体 | 备选 |
|------|----------|------|
| **Quest 2/3/Pro** | **Micro** | Nano(性能极致) |
| **低端 PC(GTX 1060 / RX 580)** | Nano | Micro |
| **中端 PC(GTX 1660 / RTX 3060)** | **Mega** | Giga |
| **高端 PC(RTX 3080+)** | **Giga** | Tera |
| **顶级 PC(RTX 4080+/RX 7900 XT+)** | **Tera** | - |

### 4.2 按 Avatar 复杂度

| Avatar 类型 | 推荐变体 |
|-------------|----------|
| **简化 Avatar(无 Fur/特效)** | Nano |
| **标准 Avatar(Toon + 基础 Outline)** | **Micro** |
| **服装切换 Avatar(SCSS 风格)** | Mega |
| **音乐 Avatar(AudioLink 重度)** | Giga |
| **幻想 Avatar(星空/几何/粒子)** | **Tera** |

### 4.3 按预算

| 预算 | 推荐 | 说明 |
|------|------|------|
| **免费** | Nano / Micro | Toon 版即可 |
| **Patreon $10/月** | **Mega** + 部分 Pro 效果 | Pro Giga 也可 |
| **Patreon $20/月** | **Giga** | 完整 Pro 效果 |
| **Patreon $50/月** | **Tera** | 全部功能 + 优先支持 |

---

## 5. 变体切换策略

### 5.1 同一 Avatar 跨平台发布

```text
PC 默认 → Mega 变体
Quest 版本 → 复制 Material,切换到 Micro 变体
```

**实现方法**:
1. 在 Material Inspector 的 Shader 下拉中选择目标变体
2. Unity 会**保留**同名属性,但部分参数可能丢失
3. 建议先在 PC 调好,再复制到 Quest 版

### 5.2 EasyQuestSwitch 集成

Poiyomi 与 **EasyQuestSwitch** 兼容(VRChat 官方工具),可一键切换 PC/Quest 变体。

详见 `memory/platform/easyquestswitch.md`(知识库已有)。

---

## 6. 性能对比(预估)

> ⚠️ **重要**: 以下为**估算值**,实际性能取决于 Avatar 复杂度、Material 数量、灯光数等。

| 变体 | Draw Call 基准 | 同屏 Avatar 推荐数 | 备注 |
|------|----------------|--------------------|------|
| **Nano** | 0.5x | 50+ | 极轻量 |
| **Micro** | 0.7x | 30-40 | Quest 推荐 |
| **Mega** | 1.0x(基线) | 15-20 | PC 通用 |
| **Giga** | 1.5x | 10-15 | PC 高端 |
| **Tera** | 2.5x+ | 5-10 | 性能密集 |

**测试建议**:
1. 在目标平台实际测试(VRChat 客户端 + Performance Rank)
2. 使用 `memory/avatar/performance-rank.md` 校验等级
3. 配合 `memory/avatar/optimization-guide.md` 优化

---

## 7. 实战陷阱

### 7.1 常见错误

| 错误 | 症状 | 修复 |
|------|------|------|
| **Quest 上用 Tera** | 严重卡顿 + 帧率< 30 | 切换到 Micro |
| **PC 用了 Nano 觉得效果差** | 没发挥 Poiyomi 优势 | 至少用 Mega |
| **变体切换后参数丢失** | 部分 Material 异常 | 手动重新配置(同名属性保留) |
| **Toon 用了 Pro 变体** | Inspector 无 Pro 效果选项 | 订阅 Patreon + 鉴权 |
| **Micro 上启用 Poiyomi Fur** | 编译警告 + 性能差 | Micro 禁用 Fur,改用 Mega |

### 7.2 变体选择的 3 个问题

问自己:
1. **目标平台是什么?** (Quest → Micro, PC → Mega+)
2. **需要的视觉效果?** (基础 Toon → Nano/Micro, 风格化 → Giga/Tera)
3. **预算?** (免费 → Toon, $10+ → Pro)

---

## 8. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Poiyomi Download & Install** | `参考文献/Poiyomi/01-download-install.md` |
| **Poiyomi Render Preset** | `参考文献/Poiyomi/02-render-preset.md` |
| **Poiyomi Installation 知识** | `./installation.md` |
| **Poiyomi Quest 优化** | `./quest-optimization.md` |
| **Poiyomi Pro vs Toon** | `./pro-vs-toon.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **上游版本** | Poiyomi 10.0 |
| **评审状态** | Stage 2.2 完成 |
| **下一步** | Stage 2.3 AudioLink 集成 |
