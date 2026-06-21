---
title: Misc Domain — 跨领域杂项知识
category: misc

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "Misc Domain — 跨领域杂项知识"

related:
  - postprocessing-principles.md
  - postprocessing-usage.md
  - accessibility-guide.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Misc Domain — 跨领域杂项知识

> **Domain**: Misc(跨领域)
> **Type**: Knowledge Base
> **本地化日期**: 2026-06-15
> **文件数**: 3

---

## 概述

**Misc Domain** 存放**跨 Avatar + World 领域**的杂项知识,不适合归入单一域。

> **收录标准**:
> - 影响多个域的通用最佳实践
> - 与体验质量(非纯技术)相关的设计指南
> - 不属于 World/Udon/Avatar/Hybrid 主流分类的内容

---

## 文档分类

### 后处理(2)

| 文档 | 来源 | 内容 |
|------|------|------|
| [postprocessing-principles.md](postprocessing-principles.md) | VRCD 文档库 | 后处理原理(现实参照)|
| [postprocessing-usage.md](postprocessing-usage.md) | VRCD 文档库 | Unity 参数与最佳实践(Bloom/Vignette/Chromatic)|

### 无障碍设计(1)

| 文档 | 来源 | 内容 |
|------|------|------|
| [accessibility-guide.md](accessibility-guide.md) | VRCLibrary (Code-Floof)| VR 无障碍设计(视觉散光/晕动症)|

---

## 主题速查

### 后处理

| 后处理效果 | 关键参数 | 性能开销 |
|-----------|---------|---------|
| **Bloom** | Intensity / Threshold / Fast Mode | 🟡 中 |
| **Vignette** | 边缘暗角 | 🟢 低 |
| **Color Grading** | 色调 / 饱和度 / Gamma | 🟢 低 |
| **Chromatic Aberration** | 色差 | 🟡 中 |
| **Grain** | 颗粒 | 🟢 低 |
| **Motion Blur** | 运动模糊 | 🟡 中 |

> **核心原则**:少即是多 — 后处理效果越多,性能负担越重

### 无障碍

| 障碍 | 原因 | 缓解措施 |
|------|------|---------|
| **散光**(光源晕轮)| 视觉缺陷 | 提高 Gamma |
| **晕动症** | VR 不适 | 减少急动、降低运动模糊 |
| **色觉障碍** | 红绿色盲 | 避免仅用颜色区分 |
| **光敏感** | 癫痫 / 偏头痛 | 避免快速闪烁 |

---

## 与其他知识库的关系

- **`world/performance-guide.md`**:后处理性能影响
- **`world/creator-economy.md`**:无障碍作为质量评分因素
- **`avatar/optimization-guide.md`**:Avatar 后处理(LilToon 内置)

---

**最后更新**:2026-06-15
