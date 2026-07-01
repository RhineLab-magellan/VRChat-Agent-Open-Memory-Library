---
title: "lilToon 优化指南"
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
  - "lilToon 优化指南"
related:
  - basic-settings.md
  - color-settings.md
  - render-modes.md
  - troubleshooting.md
---
# lilToon 优化指南

---

## 优化概述

lilToon 提供多种优化手段：
- 自动着色器优化
- 纹理烘焙
- 版本转换
- 构建尺寸削减

---

## 纹理烘焙 (Bake)

### 烘焙选项

| 选项 | 说明 |
|------|------|
| **全て焼き込み** | 主色+校正+图层2&3 合并 |
| **色調補正を焼き込み** | 仅烘焙色调校正 |
| **レイヤー2を焼き込み** | 主色+图层2 合并 |
| **レイヤー3を焼き込み** | 主色+图层3 合并 |

### 烘焙优势

```
✓ 减少运行时计算
✓ 简化材质复杂度
✓ 跨着色器兼容性
✓ 减少纹理采样
```

### 使用建议

| 场景 | 建议 |
|------|------|
| 最终发布 | 全量烘焙 |
| 迭代开发 | 按需烘焙 |
| 跨着色器迁移 | 色调烘焙优先 |

---

## 版本转换

### lilToonLite 转换

| 源 | 目标 | 优势 |
|----|------|------|
| 通常版 | Lite 版 | 减少负荷 |

### lilToonMulti 转换

| 源 | 目标 | 说明 |
|----|------|------|
| 通常版 | Multi 版 | 使用 Shader Keyword |

> ⚠️ Multi 版可能导致 Build 尺寸增大

### MToon (VRM) 转换

| 源 | 目标 | 说明 |
|----|------|------|
| lilToon | MToon | VRM 兼容性 |

> ⚠️ 参数不完全兼容，视觉效果可能变化

---

## 构建尺寸优化

### Shader 设置优化

| 选项 | 说明 |
|------|------|
| **ForwardAddパスで影を有効化** | ForwardAdd 阴影 |
| **ForwardAddパスを使用** | ForwardAdd Pass |
| **頂点ライトを使用** | 顶点光 |
| **ライトマップを使用** | 灯光贴图（VRChat 不需要） |

### 未使用属性移除

```
Assets/lilToon/[Material] Remove unused properties
```

---

## 纹理导入设置

### 忽略的设置

以下设置可能被忽略：

| 设置 | 说明 |
|------|------|
| **Wrap Mode** | 纹理环绕模式 |
| **Filter Mode** | 采样过滤模式 |

### 固定 SamplerState

| 纹理类型 | SamplerState |
|---------|--------------|
| グラデーションマップ | sampler_linear_clamp |
| 大部分遮罩 | sampler_linear_repeat |
| 形状遮罩 | sampler_linear_clamp |

---

## 性能优化建议

### 渲染模式选择

```
不透明 > カットアウト > 半透明 > 高负荷模式
```

### 遮罩使用

| 建议 | 说明 |
|------|------|
| 合并遮罩 | 减少纹理数量 |
| 合理通道 | 充分利用 RGBA |
| 烘焙遮罩 | 减少采样 |

### 材质数量

| 建议 | 说明 |
|------|------|
| 合并相似材质 | 减少 Draw Call |
| 使用图层系统 | 减少材质数量 |

---

## 编辑器工具

### 菜单项

| 工具 | 用途 |
|------|------|
| **Refresh shaders** | 修复着色器错误 |
| **Remove unused properties** | 移除未使用属性 |
| **Run migration** | 执行版本迁移 |
| **Setup from FBX** | FBX 自动设置 |

### Fix Lighting

```
GameObject/lilToon/[GameObject] Fix lighting
```

修复多 Mesh 物体亮度不一致。

---

## 纹理命名规则 (Setup from FBX)

### 主纹理

命名规则：
- 包含材质名
- 非特殊名称

```
✓ face.png, texture_face.png
✗ face_outline_mask.png, face_smoothness.png
```

### 轮廓线遮罩

包含 `outline`：
```
✓ face_outline.png, face_outline_mask.png
✗ face_mask.png, face_ol_mask.png
```

### 阴影遮罩

包含 `shadow`/`shade` + `mask`/`strength`：
```
✓ face_shadow_mask.png, face_shadow_strength_mask.png
✗ face_shadow_color.png, face_shadow.png
```

### 排除关键词

```
mask, shadow, shade, outline, normal, bumpmap,
matcap, rimlight, emittion, reflection, specular,
roughness, smoothness, metallic, metalness,
opacity, parallax, displacement, height, ambient, occlusion
```

---

## 相关文档

- [基本设置](basic-settings.md) — 渲染参数
- [颜色设置](color-settings.md) — 图层系统
- [渲染模式](render-modes.md) — 性能对比
- [故障排除](troubleshooting.md) — 常见问题
