---
title: "lilToon 基本设置"
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
  - "lilToon 基本设置"
related:
  - render-modes.md
  - color-settings.md
  - troubleshooting.md
---
# lilToon 基本设置

---

## 基本设定面板

控制基础渲染行为，首先需要设置的项目。

---

## 描画模式 (Rendering Mode)

详见 [渲染模式详解](render-modes.md)

---

## Cutoff (阈值)

| 参数 | 说明 |
|------|------|
| **Cutoff** | 透明度低于此值时完全透明（カットアウト模式） |

---

## Cull Mode (描画面)

| 模式 | 说明 | 性能 |
|------|------|------|
| **Back** | 仅渲染前面（默认） | ✅ 最优 |
| **Front** | 仅渲染背面 | 🟢 优 |
| **Off** | 两面都渲染 | 🟡 中 |

### 典型设置

| 部位 | 推荐 |
|------|------|
| 皮肤 | Back |
| 头发 | Back / Off |
| 服装 | Back |
| 透明物体 | Off |

### 两面描画的注意事项

| 参数 | 说明 |
|------|------|
| **裏面の法線を反転** | 背面时反转法线（用于双面纹理） |
| **裏面を影にする** | 强制使背面变暗的程度 |

---

## 非表示 (Invisible)

| 参数 | 说明 |
|------|------|
| **非表示** | 开启时材质不可见 |

---

## ZWrite (深度写入)

| 选项 | 说明 |
|------|------|
| **On** | 写入深度信息（默认，推荐） |
| **Off** | 不写入深度信息 |

### 典型用途

- 半透明材质：`Off` 可解决渲染问题
- 透明叠加：`Off` 让后面的物体正确显示

---

## Render Queue (渲染队列)

| 说明 | 示例 |
|------|------|
| 决定材质绘制顺序的数值 | 2450 (默认), 3000 等 |
| 较大值 = 之后绘制 = 显示在上层 | |

### 常见问题解决

⚠️ **半透明物体重叠时后方消失**：
```
解决方案：提高前景物体的 Render Queue 值
```

### 常用 Render Queue 值

| 用途 | 值 |
|------|-----|
| 不透明 | 2000 |
| 半透明（默认） | 2450 |
| 半透明（前景） | 2500+ |

---

## キーワード (Keywords)

### 着色器变体关键词

| 关键词 | 说明 |
|--------|------|
| `LILTOON` | 主着色器 |
| `LILTOON_LITE` | 轻量版 |
| `LILTOON_MULTI` | 多关键词版 |
| `LILTOON_FUR` | 毛发着色器 |
| `LILTOON_OUTLINE` | 轮廓线着色器 |
| `LILTOON_OVERLAY` | 叠加着色器 |

---

## 基本设定参数一览

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 描画モード | enum | 不透明/透明/折射等 |
| Cutoff | float | 透明度阈值 |
| Cull Mode | enum | Back/Front/Off |
| 裏面の法線を反転 | bool | 背面法线反转 |
| 裏面を影にする | float | 背面阴影强度 |
| 色 | color | 背面填充色 |
| 非表示 | bool | 隐藏材质 |
| ZWrite | bool | 深度写入 |
| Render Queue | int | 渲染队列值 |

---

## 相关文档

- [渲染模式](render-modes.md) — 各模式详解
- [颜色设置](color-settings.md) — 主色/透明度
- [阴影设置](color-settings.md#阴影) — 阴影配置
- [故障排除](troubleshooting.md) — 常见问题
