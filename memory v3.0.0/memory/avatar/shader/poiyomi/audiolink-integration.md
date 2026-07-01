---
title: "Poiyomi Shaders - AudioLink 集成"
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
  - audiolink
  - audio-reactive
  - world-integration
aliases:
  - "Poiyomi AudioLink"
  - "Poiyomi 音频驱动"
  - "Poiyomi AL Spectrum"
  - "Poiyomi Volume Color"
related:
  - "./installation.md"
  - "./shader-variants.md"
  - "./modular-system.md"
  - "../../../../参考文献/Poiyomi/11-audio-link.md"
  - "../../../../参考文献/Poiyomi/12-al-spectrum.md"
  - "../../../../参考文献/Poiyomi/62-volume-color.md"
  - "../../../hybrid/osc-protocol.md"
---

# Poiyomi Shaders — AudioLink 集成

> **Domain**: Avatar → Shader → Poiyomi → AudioLink
> **原始参考**: `参考文献/Poiyomi/11-audio-link.md` + `12-al-spectrum.md` + `62-volume-color.md`
> **状态**: 活跃(Active)

---

## 1. 概述

Poiyomi 10.0 提供**完整的 AudioLink 集成**,覆盖从频段驱动 → 频谱可视化 → 体积颜色投射的全流程。配合 World 端 AudioLink Controller,可让 Avatar 实时响应 World 内音频。

> **AudioLink 基础**: 详见 `https://audiolink.dev/`,本知识库 `memory/hybrid/osc-protocol.md` 有 OSC 集成说明。

---

## 2. AudioLink 三件套

| 组件 | 文档 | 用途 |
|------|------|------|
| **AudioLink 基础** | `11-audio-link.md` | 5 频段驱动(全局) |
| **AL Spectrum** | `12-al-spectrum.md` | 频谱可视化(波形) |
| **AL Volume Color** | `62-volume-color.md` | UV 方向颜色波形投射 |

**速查对比**:

| 维度 | 基础 AudioLink | AL Spectrum | AL Volume Color |
|------|----------------|-------------|-----------------|
| **复杂度** | ⭐ 简单 | ⭐⭐⭐ 复杂 | ⭐⭐ 中等 |
| **输出** | 数值驱动 | 频谱图案 | 颜色波形 |
| **适用** | 缩放/发光/淡入淡出 | 装饰纹理 | 体积颜色 |
| **数据** | 5 频段数值 | 完整频谱 | 低/中/高三色 |

---

## 3. 基础 AudioLink(11-audio-link.md)

### 3.1 启用步骤

1. **World 端**: World 必须有 AudioLink Controller(World 创建者负责)
2. **Avatar 端**: 在 Poiyomi Material Inspector 找到 `Audio Link` 类别
3. **Toggle 启用**: `Audio Link` 主开关(默认关闭)
4. **Anim Toggle**: 启用后可由 Animator 动画化(运行时切换)

> **重要**: AudioLink **默认启用**。要游戏中关闭,需动画化 `Audio Link` Toggle(不是 Section Header)。

### 3.2 5 个频段

| 频段 | 频率范围 | 典型用途 |
|------|----------|----------|
| **Bass** | 0-200 Hz | 重低音脉动、放大 |
| **Low Mid** | 200-800 Hz | 中低频呼吸 |
| **High Mid** | 800-3000 Hz | 中高频细节 |
| **Treble** | 3000+ Hz | 高频闪烁、闪光 |
| **Volume** | 总体 | 整体缩放、淡入淡出 |

### 3.3 关键参数

| 参数 | 类型 | 范围 | 用途 |
|------|------|------|------|
| **Audio Link** | Toggle | - | 总开关 |
| **Anim Toggle** | Toggle | - | 是否可由 Animator 控制 |
| **Bass / Mid / Treble** | Float | 0-20 | 各频段 Emission Strength |
| **Band Override** | Dropdown | Auto/Bass/Low Mid/High Mid/Treble | 强制指定频段 |

### 3.4 典型应用

**场景 1: Bass 驱动发光**
```text
Material → AudioLink → Toggle: ON
Material → Emission → Emission 强度: 0.0 (默认)
Material → AudioLink → Bass: 5.0
效果: 低音鼓点触发 Material 发光
```

**场景 2: 整体 Volume 缩放**
```text
Material → AudioLink → Toggle: ON
Material → AudioLink → Volume: 0.1
效果: 整体音量驱动 Material 缩放(±10%)
```

---

## 4. AL Spectrum(12-al-spectrum.md)

### 4.1 概念

将音频频谱可视化为 UV 空间的颜色/亮度图案,可投到 Mesh 上形成**会跳舞的纹理**。

### 4.2 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| **Positioning Mode** | Dropdown | `UV` / `Position` / `Rotation` / `Scale` / `Mirrored UV` / `Symmetry` |
| **UV** | Dropdown | UV0/UV1/UV2/UV3 |
| **Position/Rotation/Scale** | Vector3 / Float | 网格空间定位 |
| **Mirrored UV** | Toggle | UV 镜像模式 |
| **Symmetry Mode** | Dropdown | 对称方式(左右对称等) |

### 4.3 典型应用

**场景: Avatar 背部 LED 条频谱**
```text
1. 在 Avatar 背部放 Plane(UV 沿条带方向)
2. Material: Poiyomi Pro Tera + AL Spectrum
3. Positioning Mode: Position
4. UV: UV0
5. AudioLink Toggle: ON
效果: 背部 LED 条按频谱律动
```

---

## 5. AL Volume Color(62-volume-color.md)

### 5.1 概念

将 3 个频段(低/中/高)分别映射为 3 种颜色,在 UV 方向上**投射为波形**。效果类似 Volume Rendering 的彩色雾气。

### 5.2 关键参数

| 参数 | 类型 | 范围 | 用途 |
|------|------|------|------|
| **UV** | Dropdown | UV0-UV3 | Volume Color 投射 UV 空间 |
| **UV Direction** | Dropdown | X/Y | 波形投射方向 |
| **Blend Type** | Dropdown | Replace/Multiply/Screen/Linear Dodge/Overlay/Mixed | 混合方式 |
| **Alpha** | Float | 0-1 | 整体可见性 |
| **Volume Color Low** | Color | - | 低频颜色 |
| **Low Emission** | Float | 0-20 | 低频发光强度 |
| **Volume Color Mid** | Color | - | 中频颜色 |
| **Mid Emission** | Float | 0-20 | 中频发光强度 |
| **Volume Color High** | Color | - | 高频颜色 |
| **High Emission** | Float | 0-20 | 高频发光强度 |

### 5.3 典型应用

**场景: 烟雾 Aura**
```text
1. Avatar 周围放 Sphere(低面数,内部)
2. Material: Poiyomi Pro + Volume Color
3. UV Direction: Y(从下往上)
4. Volume Color Low: 红
5. Volume Color Mid: 黄
6. Volume Color High: 蓝
7. Blend Type: Additive
效果: 烟雾从下到上由红→黄→蓝流动
```

---

## 6. 性能考虑

| 因素 | 影响 | 缓解 |
|------|------|------|
| **AudioLink 主开关** | 即使关闭, Shader 仍会查询 AudioLink 数据 | Quest 不用 AudioLink 时,Material 应不开启 |
| **AL Spectrum** | 每帧计算频谱 → 较重 | Quest 慎用;Mega+ 推荐 |
| **Volume Color** | 中等开销 | 适量使用 |
| **多 Material 联动** | 累加开销 | 共享 AudioLink 数据(自动) |

**Quest 推荐**:
- Micro 变体: AudioLink 限 4 频段
- 避免 AL Spectrum(计算密集)
- Volume Color 可用,但限制 Material 数量

---

## 7. World 端要求(关键)

> ⚠️ **Avatar 单独启用 AudioLink 不会工作**。World 必须有 AudioLink Controller。

| 条件 | 说明 |
|------|------|
| **World 有 AudioLink Controller** | World 创建者需在 World 内放置 |
| **World 有音频源** | 音乐、语音、环境音均可 |
| **玩家进入 World** | Avatar Material 自动读取 World 音频数据 |

**开发者视角**: 如果你的 World 不需要音乐驱动 Avatar,不需要装 AudioLink Controller。AudioLink 启用与否完全由 World 决定,Avatar 只是"被动响应"。

---

## 8. 实战陷阱

| 错误 | 症状 | 修复 |
|------|------|------|
| **World 没装 AudioLink** | Avatar 完全无反应 | 装 AudioLink Controller(World 端) |
| **Anim Toggle 写错** | 游戏中无法关闭 AudioLink | 动画化 Toggle 不是 Section Header |
| **Quest 用了 AL Spectrum** | 卡顿严重 | 改用基础 AudioLink |
| **Volume Color 混合选错** | 颜色被覆盖 | 改用 Mixed 或 Multiply |
| **多频段叠加过强** | 发光溢出 | 降低 Emission 值(< 5) |

---

## 9. Pro vs Toon 差异

| 功能 | Toon | Pro |
|------|------|-----|
| **基础 AudioLink 5 频段** | ✅ | ✅ |
| **AL Spectrum** | ⚠️ 基础 | ✅ 完整 |
| **AL Volume Color** | ✅ | ✅ |
| **AudioLink + Modular** | ❌ | ✅ |

**Pro 优势**: AudioLink 数据可通过 Modular Shader System 注入自定义模块,实现复杂音频驱动效果。

---

## 10. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **AudioLink 基础 原文** | `参考文献/Poiyomi/11-audio-link.md` |
| **AL Spectrum 原文** | `参考文献/Poiyomi/12-al-spectrum.md` |
| **AL Volume Color 原文** | `参考文献/Poiyomi/62-volume-color.md` |
| **Poiyomi Installation** | `./installation.md` |
| **Poiyomi Modular System** | `./modular-system.md` |
| **OSC 协议** | `memory/hybrid/osc-protocol.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **上游版本** | Poiyomi 10.0 |
| **评审状态** | Stage 2.3 完成 |
| **下一步** | Stage 2.4 Modular Shader System |
