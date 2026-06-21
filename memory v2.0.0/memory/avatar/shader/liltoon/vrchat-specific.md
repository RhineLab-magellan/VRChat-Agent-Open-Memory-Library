---
title: lilToon VRChat 特定配置
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
  - color-settings.md
  - optimization.md
  - troubleshooting.md

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: v2.3.2 (2025-10-29)
last_review: 2026-06-21
confidence: Medium
---
# lilToon VRChat 特定配置

---

## Custom Safety Fallback

### 概述
VRChat Safety 系统激活时的着色器回退配置。

### 参数

| 参数 | 说明 |
|------|------|
| **Shader Type** | 着色器类型 |
| **Rendering Mode** | 透明模式 |
| **Facing** | 描画面（单/双面） |
| **Shading** | ToonStandard 阴影类型（Custom 时可选 Ramp 纹理） |

### 输出预览

`Result` 显示基于设置生成的标签，用于确定回退目标着色器。

---

## Safety 系统说明

### 默认行为

VRChat Safety 激活时：
- 使用 ToonStandard 着色器
- 不透明化处理

### 自定义回退

可通过设置自定义回退着色器：
```
Custom Safety Fallback > Shader Type > 自定义选择
```

---

## 注意事项

> ⚠️ 文档撰写时 ToonTransparent 不存在
> 回退目标为 Unlit/Transparent

---

## VRChat 特定参数

### 距离裁剪取消

| 参数 | 说明 |
|------|------|
| **距離クリッピングキャンセラー** | 防止近裁剪导致的消失 |

> ℹ️ 仅在 Near Clip > 0.1 时生效

### VR 视差强度

多个效果包含 VR 视差控制：

| 效果 | 参数 |
|------|------|
| MatCap | VR時の視差の強さ |
| RimLight | VR時の視差の強さ |
| 闪光 | VR時の視差の強さ |
| 宝石 | VR時の視差の強さ |

---

## VRChat 亮度建议

### 亮度设置

| 参数 | 建议值 | 说明 |
|------|--------|------|
| **明るさの下限** | 0.0 - 0.2 | 防止过暗 |
| **明るさの上限** | 保持默认或略低 | 防止过曝 |
| **影色への環境光影響度** | 0.3 - 0.5 | 暗世界阴影控制 |

---

## VRChat 优化建议

### Avatar 容量

```
lilToon 自动优化着色器
Build 时移除未使用功能
```

### 纹理优化

| 优化项 | 方法 |
|--------|------|
| 未使用纹理 | 移除或 Bake |
| 纹理分辨率 | 合理尺寸（1024-2048） |
| 图层合并 | 使用 Bake 功能 |

### 渲染模式选择

| 场景 | 推荐模式 |
|------|---------|
| 皮肤 | 不透明 |
| 头发 | 半透明 |
| 服装 | 不透明/半透明 |
| 配件 | 根据需求 |

---

## 常见 VRChat 问题

### 阴影过强

**解决方案**：
- 降低 影色への環境光影響度
- 使用遮罩隔离面部阴影
- 使用 ライト方向のオーバーライド

### 亮度不一

**解决方案**：
- 对多 Mesh 对象执行 Fix lighting
- 统一材质设置
- 检查顶点灯强度

### Safety 表现异常

**解决方案**：
- 检查 Custom Safety Fallback 设置
- 测试不透明模式
- 验证纹理 alpha 通道

---

## 相关文档

- [基本设置](basic-settings.md) — 渲染参数
- [阴影设置](color-settings.md#阴影设置) — 阴影配置
- [优化指南](optimization.md) — 性能优化
- [故障排除](troubleshooting.md) — 常见问题
