---
title: "lilToon AudioLink 集成"
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
  - audio
aliases:
  - 音频
  - lilToon
related:
  - color-settings.md
  - reflection-settings.md
  - advanced-settings.md
---
# lilToon AudioLink 集成

---

## 概述

AudioLink 是 VRChat 的音频数据分析系统，lilToon 支持与其同步动画。

### 依赖

- VRChat 的 Udon AudioLink 系统
- 支持 AudioLink 的世界

---

## AudioLink 原理

```
音乐 → 频谱分析 → 频段数据 → 着色器采样 → 动画效果
```

---

## 参数详解

### UV 控制

| 参数 | 说明 |
|------|------|
| **UV Mode** | 采样 UV 类型 (UV0-3) |
| **サイズ** | UV 尺寸（影响时序偏移） |
| **Offset** | 时序偏移量 |
| **角度** | UV 旋转角度 |

### 频段采样

| 参数 | 说明 |
|------|------|
| **帯域** | 采样频段（音高） |
| **マスク** | 效果遮罩 (RGB) |

### 遮罩说明

**通常模式**：
- R = 延迟
- G = 频段
- B = 强度

**Spectrum 模式**：
- R = 音量
- G = 频段
- B = 强度

### 应用控制

| 参数 | 说明 |
|------|------|
| **AudioLink無効時の初期値** | 非対応世界的行为 |
| **適用先** | 效果应用目标 |
| **ローカル化** | 使用本地纹理而非 AudioLink |
| **ローカルマップ** | 本地纹理 (R通道) |
| **BPM** | 音乐节奏 |
| **拍数** | BPM 乘数 |
| **Offset** | 同步偏移 |

---

## 应用目标

| 目标 | 说明 |
|------|------|
| **発光** | 发光强度 |
| **色** | 发光颜色 |
| **ラメ** | 闪光效果 |
| **その他** | 其他效果 |

---

## 使用建议

### 本地纹理替代

在不支持 AudioLink 的世界：

```
1. 启用 ローカル化
2. 设置 ローカルマップ
3. 使用预录制的音频动画纹理
```

### 纹理制作

1. 在支持的世界录制
2. 导出动画纹理
3. 在其他世界使用本地模式

---

## 典型应用

### 音乐反应发光

```
适用: 服装边缘、配件
效果: 随音乐闪烁/变色
```

### 频谱可视化

```
适用: 身体装饰
效果: 频段对应颜色变化
```

### 节奏同步动画

```
适用: 头发、尾巴
效果: BPM 同步摆动
```

---

## 注意事项

> ⚠️ AudioLink 依赖于 VRChat 世界实现
> 非対応世界需要使用本地纹理

### 性能考虑

- 多个 AudioLink 材质可能增加负荷
- 合理使用遮罩减少计算

---

## 相关文档

- [发光设置](./color-settings.md#発光設定) — 发光参数
- [闪光设置](./reflection-settings.md#ラメ設定) — 闪光参数
- [距离渐变](./advanced-settings.md#距離フェード) — 距离效果
