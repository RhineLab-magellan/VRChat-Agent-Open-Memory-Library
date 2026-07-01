---
title: "lilToon 着色器变体"
category: avatar
subcategory: shader
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: official
version: 1.0
upstream_version: "v2.3.2 (2025-10-29)"
last_review: 2026-06-21
confidence: Medium
tags:
  - avatar
  - shader
  - liltoon
aliases:
  - lilToon
  - "lilToon 着色器变体"
related:
  - overview.md
  - render-modes.md
  - fur.md
  - outline.md
  - optimization.md
---
# lilToon 着色器变体

---

## 变体一览

| 着色器 | 说明 | 用途 |
|--------|------|------|
| **lilToon** | 主着色器 | 一般用途 |
| **lilToonLite** | 轻量版 | 降低负荷 |
| **lilToonMulti** | 多关键词版 | 大量材质 |
| **lilToonOverlay** | 叠加版 | 覆盖效果 |
| **lilToonOutlineOnly** | 仅轮廓 | 轮廓线专用 |
| **lilToonFurOnly** | 仅毛发 | 毛发专用 |
| **lilToonFadeOnly** | 仅淡出 | 淡出效果 |

---

## 主着色器 (lilToon)

### 说明
通用主着色器，适合大多数场景。

### 特点
```
✓ 功能完整
✓ 性能平衡
✓ 兼容性最佳
```

### 使用建议
**首选着色器**，除非有特殊需求。

---

## 轻量版 (lilToonLite)

### 说明
在保持视觉效果的同时大幅降低负荷。

### 特点
```
✓ 显著降低负荷
✓ 视觉效果接近主版
✗ 部分高级功能缺失
```

### 使用建议
```
- Quest 兼容
- 性能受限设备
- 简单 Avatar
```

### 转换方法
```
优化菜单 > lilToonLiteに変換
```

---

## 多关键词版 (lilToonMulti)

### 说明
使用 Shader Keyword 的版本。

### 特点
```
✓ 材质数量多时更高效
✗ Build 尺寸可能增大
```

### 使用建议
```
- 大量使用相同材质时
- 需要减少 Draw Call 时
```

> ⚠️ 可能增加 Build 尺寸，谨慎使用

---

## 叠加版 (lilToonOverlay)

### 说明
覆盖在材质上的透明着色器。

### 特点
```
✓ 比普通透明更轻量
✓ 无多余 Pass
```

### 使用建议
```
- 叠加效果层
- 贴花效果
- 覆盖纹理
```

---

## 仅轮廓版 (lilToonOutlineOnly)

### 说明
仅渲染轮廓线。

### 典型用途

**硬边模型平滑轮廓**：
```
1. 准备光滑法线模型
2. 使用此着色器渲染轮廓
3. 获得比硬边更平滑的轮廓线
```

### 使用建议
```
- 硬边模型
- 需要平滑轮廓时
- 与主着色器配合
```

---

## 仅毛发版 (lilToonFurOnly)

### 说明
仅渲染毛发部分。

### 典型用途

**混合毛发渲染**：
```
- 透明毛发 + Cutout 毛发组合
- 获得更自然的毛发效果
```

### 使用建议
```
毛发着色器组合使用
```

---

## 文件命名规则

### Pass 后缀

```
_o     → 轮廓线
_cutout → 镂空
_trans  → 透明
_fur    → 毛发
_ref    → 折射
_gem    → 宝石
_tess   → 细分
_overlay → 叠加
_fakeshadow → 假阴影
_one    → 单 Pass
_two    → 双 Pass
```

---

## 变体选择指南

```
需要什么效果?
├── 仅轮廓线 → lilToonOutlineOnly
├── 毛发 → lilToonFurOnly / 主着色器毛发模式
├── 覆盖效果 → lilToonOverlay
└── 普通渲染
    ├── 负荷优先 → lilToonLite
    ├── 大量材质 → lilToonMulti
    └── 一般用途 → lilToon (主着色器)
```

---

## 相关文档

- [概述与特性](overview.md) — 完整特性
- [渲染模式](render-modes.md) — 各模式详解
- [毛发设置](fur.md) — 毛发配置
- [轮廓线设置](outline.md) — 描边配置
- [优化指南](optimization.md) — 性能优化
