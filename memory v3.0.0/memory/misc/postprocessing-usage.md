---
title: "后处理使用方式 — Unity 参数与最佳实践"
category: misc
knowledge_level: applied
status: active
source: "VRCD 文档库（docs.vrcd.org.cn）"
source_type: community
version: 1.0
last_review: 2026-06-05
confidence: Medium
tags:
  - misc
  - udonsharp
  - reference
aliases:
  - "后处理使用方式 — Unity 参数与最佳实践"
  - postprocessing-usage
related:
  - postprocessing-principles.md
  - "../rules/performance-rules.md"
  - accessibility-guide.md
  - index.md
  - "../api/not-exposed.md"
---
# 后处理使用方式 — Unity 参数与最佳实践

> 来源: VRCD 文档库（docs.vrcd.org.cn）| 更新: 2026-06-05

---

## 核心原则

> ⚠️ **少即是多**：后处理效果越多，性能负担越重。打的勾越多，激活的选项越多。

---

## Bloom（炫光）

### 参数说明

| 参数 | 说明 | 备注 |
|------|------|------|
| **Intensity** | 炫光效果强度 | — |
| **Threshold** | 过滤低于此亮度的像素 | — |
| **Soft Knee** | 阈值过渡方式 | 0=硬阈值，1=软阈值 |
| **Clamp** | 限制像素量（Gamma 空间） | — |
| **Diffusion** | 遮罩效果范围 | 建议整数，性能优化 |
| **Anamorphic Ratio** | 变形比例 | 负值垂直，正值水平 |
| **Color** | 炫光颜色 | — |
| **Fast Mode** | 降低质量换性能 | **推荐开启** |
| **Texture** | 污迹/灰尘纹理蒙版 | 建议低分辨率 |

### 推荐设置

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| Intensity | 0~1 | 超 1 仅用于特殊强炫光场景 |
| Threshold | 0~2 | — |
| Clamp | 3~4 | 确保炫光强度不超出承受范围 |
| Anamorphic Ratio | 按需配置 | — |
| **Fast Mode** | **开启** | 性能优化 |

---

## Vignette（晕影）

### 模式

| 模式 | 说明 |
|------|------|
| **Classic** | 经典模式，参数控制位置/形状/强度 |
| **Masked** | 使用自定义纹理蒙版创建晕影 |

### Classic 模式参数

| 参数 | 说明 |
|------|------|
| **Color** | 晕影颜色（Alpha 通道实现透明度） |
| **Center** | 晕影中心点，默认 0.5, 0.5（屏幕中心） |
| **Intensity** | 渐晕量 |
| **Smoothness** | 晕影边框平滑度 |
| **Roundness** | 方形程度（低=方形，高=圆形） |
| **Rounded** | 完美圆形 vs 跟随屏幕纵横比 |

### Masked 模式参数

| 参数 | 说明 |
|------|------|
| **Color** | 晕影颜色 |
| **Mask** | 单通道 8 位灰度纹理蒙版 |
| **Opacity** | 蒙版不透明度 |

### 最佳实践

根据三种晕影模式，建议模拟**自然晕影**和**光学晕影**：

- **自然晕影**：逐渐变暗，光线以不同角度到达传感器
- **光学晕影**：渐进式，由镜头特性和镜筒阴影引起
- **机械晕影**：通常突然发生，只在角落

**操作**：打开强度（Intensity）并调整为看着舒适的值即可。

---

## Grain（颗粒）

### 参数说明

| 参数 | 说明 |
|------|------|
| **Colored** | 彩色 vs 灰度颗粒 |
| **Intensity** | 对底层图像的影响程度 |
| **Size** | 颗粒大小 |
| **Luminance Contribution** | 与场景明暗的互动关系 |

### 两类实践方向

#### 胶片颗粒

| 参数 | 设置 | 说明 |
|------|------|------|
| Colored | **关** | 无颜色 |
| Intensity | 0~1 | 根据喜好 |
| Size | 0.4~2 | — |
| Luminance Contribution | **0** | — |

#### 数码噪点

| 参数 | 设置 | 说明 |
|------|------|------|
| Colored | **开** | 有颜色 |
| Intensity | 0~1 | 强光→0，弱光→1 |
| Size | 0.4~2 | 推荐 **0.6** |
| Luminance Contribution | **1** | — |

### ⚠️ VR 注意事项

> **请慎用此功能，VR 端的噪点会导致玩家产生眩晕的感觉。**

---

## Ambient Occlusion（环境光遮蔽）

### 效果

描绘物体和物体相交或靠近时遮挡周围漫反射光线的效果。

**解决的问题**：
- 漏光、飘、阴影不实
- 缝隙、褶皱、墙角、角线表现不清晰
- 细小物体细节不清晰

**直观感受**：画面的明暗度，开启后暗部阴影更明显。

### 模式

| 模式 | 说明 |
|------|------|
| **MSVO（多比例体积遮挡）** | 桌面和控制台硬件上质量更高、速度更快，但需要着色器支持 |
| **SAO（可扩展环境遮挡）** | 兼容性更好 |

---

## 性能优化建议

| 平台 | 建议 |
|------|------|
| **PC** | 适度使用，优先开启 Fast Mode |
| **Quest/VR** | **极谨慎**，Grain 可能导致眩晕，其他效果也尽量简化 |

### 具体建议

- Bloom 的 Diffusion 值建议为整数（影响内部迭代计数）
- 不要对 Diffusion 进行动画处理（可能导致感知问题）
- Grain 的 Texture 建议使用低分辨率

---

## 相关文档

- `postprocessing-principles.md` — 后处理原理与现实参照
- `performance-rules.md` — World 性能约束