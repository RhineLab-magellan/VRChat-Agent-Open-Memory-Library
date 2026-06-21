---
title: lilToon Stencil 设置详解
category: avatar
subcategory: shader

knowledge_level: applied
status: active

tags:
  - avatar
  - shader
  - liltoon

aliases:
  - "lilToon"

related:
  - basic-settings.md
  - render-modes.md
  - outline.md
  - fur.md

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: v2.3.2 (2025-10-29)
last_review: 2026-06-21
confidence: Medium
---
# lilToon Stencil 设置详解

---

## 概述

Stencil 是 3D 空间中的遮罩处理，可在材质间控制绘制顺序和可见性。

---

## 核心概念

### Stencil 工作原理

```
1. Writer 材质写入 Stencil ID
2. Reader 材质检查 Stencil ID
3. 根据条件决定是否绘制
```

### 关键参数

| 参数 | 说明 |
|------|------|
| **Ref** | Stencil ID (0-255) |
| **ReadMask** | 读取掩码 |
| **WriteMask** | 写入掩码 |
| **Comp** | 比较方法 |
| **Pass** | 绘制时行为 |
| **Fail** | 不绘制时行为 |
| **ZFail** | 深度失败时行为 |

---

## 比较方法 (Comp)

| 值 | 说明 |
|----|------|
| **Never** | 永不通过 |
| **Always** | 始终通过（默认） |
| **Equal** | 相等时通过 |
| **NotEqual** | 不等时通过 |
| **Less** | 小于时通过 |
| **LessEqual** | 小于等于时通过 |
| **Greater** | 大于时通过 |
| **GreaterEqual** | 大于等于时通过 |

---

## 通道行为 (Pass/Fail/ZFail)

| 值 | 说明 |
|----|------|
| **Keep** | 保持当前值 |
| **Zero** | 设为 0 |
| **Replace** | 替换为 Ref |
| **IncrementSaturate** | +1 (上限 255) |
| **DecrementSaturate** | -1 (下限 0) |
| **Invert** | 按位取反 |
| **IncrementWrap** | +1 (溢出归 0) |
| **DecrementWrap** | -1 (溢出归 255) |

---

## 常用设置

### 快捷按钮

| 按钮 | 说明 |
|------|------|
| **Set Writer** | 设为写入侧 |
| **Set Reader** | 设为读取侧 |
| **Reset** | 恢复初始状态 |

---

## 实际应用示例

### 眉毛绘制在头发上

```
眉毛材质: Set Writer, Ref=1, Pass=Replace
头发材质: Set Reader, Ref=1, Comp=NotEqual
```

### 流程

```
1. 皮肤先绘制（Ref=0）
2. 眉毛绘制，写入 Ref=1
3. 头发检查，非 Ref=1 区域绘制
```

---

## 完整设置示例

### 1. 面部零件在头发上

| 属性 | 皮肤 | 面部零件 | 头发 |
|------|------|----------|------|
| Ref | 0 | 1 | 1 |
| Comp | Always | Always | NotEqual |
| Pass | Keep | Replace | Keep |
| Render Queue | 2450 | 2451 | 2452 |

### 2. 面部零件在头发上（半透明）

| 属性 | 皮肤 | 面部零件 | 头发 | 头发(透明) |
|------|------|----------|------|-----------|
| Ref | 0 | 1 | 1 | 1 |
| Comp | Always | Always | NotEqual | Equal |
| Pass | Keep | Replace | Keep | Keep |
| Render Queue | 2450 | 2451 | 2452 | 2460 |

### 3. 仅皮肤部分透明的头发

| 属性 | 皮肤 | 头发(不透明) | 头发(透明) |
|------|------|--------------|-----------|
| Ref | 1 | 1 | 1 |
| Comp | Always | NotEqual | Equal |
| Pass | Replace | Keep | Keep |
| Render Queue | 2450 | 2451 | 2460 |

### 4. 仅皮肤上透明的头发（半透明面部零件）

| 属性 | 皮肤 | 头发(不透明) | 面部零件 | 头发(透明) | 头发(透明2) |
|------|------|--------------|----------|------------|-------------|
| Ref | 1 | 1 | 2 | 1 | 2 |
| Comp | Always | NotEqual | Always | Equal | Equal |
| Pass | Replace | Keep | Replace | Keep | Keep |
| Render Queue | 2450 | 2451 | 2452 | 2460 | 2461 |

### 5. 仅皮肤上显示的腮红/发影

| 属性 | 皮肤 | 腮红/发影 |
|------|------|-----------|
| Ref | 1 | 1 |
| Comp | Always | Equal |
| Pass | Replace | Keep |
| Render Queue | 2450 | 2460 |

### 6. 对象边缘的轮廓线

| 属性 | 本体 | 轮廓线 |
|------|------|--------|
| Ref | 1 | 1 |
| Comp | Always | NotEqual |
| Pass | Replace | Keep |

### 7. 仅透过镜片可见的对象

| 属性 | 镜片 | 对象 |
|------|------|------|
| Ref | 1 | 1 |
| Comp | Always | Equal |
| Pass | Replace | Keep |
| Render Queue | 2450 | 2451 |
| ZWrite | Off | On |

---

## FakeShadow 设置

### 概述
FakeShadow 通过偏移网格模拟阴影。

### 参数

| 参数 | 说明 |
|------|------|
| **向き** | 偏移方向（叠加到灯光） |
| **Offset** | 偏移量 |

### FakeShadow Stencil 配置

| 属性 | 皮肤 | 头发 | FakeShadow |
|------|------|------|------------|
| Ref | 51 | 0 | 51 |
| ReadMask | 255 | 255 | 255 |
| WriteMask | 255 | 255 | 255 |
| Comp | Always | Always | Equal |
| Pass | Replace | Replace | Keep |
| Fail | Keep | Keep | Keep |
| ZFail | Keep | Keep | Keep |

> ℹ️ Ref 值可使用 0 以外的任意值。

---

## 注意事项

### Render Queue 重要性

```
描画处理 ≠ 画面可见性
```

- 隐藏部分也可能写入 Stencil
- 绘制顺序影响 Stencil 结果

### 数值选择

> ⚠️ 建议使用随机数值（如 82、143）避免冲突

简单值（1、2）易与其他资源冲突。

---

## 相关文档

- [基本设置](basic-settings.md) — Render Queue 等
- [渲染模式](render-modes.md) — 透明模式
- [轮廓线](outline.md) — 描边配置
- [毛发设置](fur.md) — 毛发效果
