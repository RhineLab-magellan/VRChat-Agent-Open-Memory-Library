---
title: Android/Quest Development
category: platform

knowledge_level: applied
status: active

tags:
  - platform
  - shader
  - light
  - avatar

aliases:
  - "Android/Quest Development"

related:
  - avatar/performance-rank.md
  - avatar/optimization-guide.md
  - world/performance-guide.md
  - platform/mobile-ui-optimization.md
  - platform/cross-platform-content.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-10
confidence: Medium
---
# Android/Quest Development

> 来源: VRChat 官方文档 (creators.vrchat.com/platforms/android/)
> 置信度: High
---

## Overview

VRChat 支持 Android 平台（Quest + 移动设备）。开发跨平台内容需要特殊考虑。

---

## 平台设置

### Unity Build Settings
```
Edit → Build Settings → Android → Switch Platform
```

### VRChat SDK Control Panel
```
Select Platform: Android
```

---

## 内容限制

### Avatar 着色器限制 ⚠️
Avatar **只能**使用 VRChat Mobile Shaders（SDK 内置）：
- Mobile/VRChat/Lit
- Mobile/VRChat/Lightmapped
- Mobile/VRChat/Unlit

**禁止**: 自定义着色器（会导致上传失败）

### World 着色器
World 不受着色器限制，但：
- 必须高度优化
- 推荐使用 `Mobile/VRChat/Lightmapped`
- 必须烘焙光照

---

## 跨平台 Avatar 要求

### Armature 匹配 ⚠️
PC 和 Android 版本的 **骨架路径必须完全相同**：
```
Armature (root)
└── Hips (root bone) ← 必须一致
    └── Spine
        └── ...
```

### Root Bone 要求
- **Hips** 是 root bone
- PC 和 Android 的 **scale 和 rotation 必须相同**
- 可以移除非必要骨骼（裙子、头发等）
- **禁止**改变基础骨架结构

### 常见问题
骨架不匹配会导致：
- 奇怪的身体扭曲
- 跨平台查看异常
- 动画错位

---

## 性能优化

### Geometry
| 指标 | Quest 标准 |
|------|-----------|
| **三角形** | ≤70,000 (Excellent: 32,000) |
| **材质数** | ≤16 (Excellent: 2) |
| **Draw Calls** | 尽量减少 |

### Textures
- 最大分辨率: 1024x1024 (1K)
- 使用纹理图集
- 降低 "Max Size" 在导入设置中

### Lighting
- **必须烘焙**光照
- 避免实时灯光
- 使用 Light Probes
- 低 lightmap 分辨率

### Occlusion Culling
- **必须烘焙**遮挡剔除
- 减少 GPU 负载
- 设置简单但有效

---

## Content Optimization Checklist

### Worlds
- [ ] 烘焙光照（不是可选，是必须）
- [ ] 降低几何复杂度
- [ ] 避免透明度
- [ ] 降低纹理分辨率
- [ ] 烘焙遮挡剔除
- [ ] 使用优化的着色器

### Avatars
- [ ] 移除多余组件
- [ ] 减少骨骼数量
- [ ] 降低多边形数量
- [ ] 避免透明度
- [ ] 减小纹理大小
- [ ] 仅使用 Mobile Shaders

---

## 工具推荐

### EasyQuestSwitch
VCC 包，可自动调整跨平台内容：
```
VCC → Manage Packages → EasyQuestSwitch
```

### SDK 示例
SDK 包含 Quest 优化示例。

---

## 发布流程

1. 在 Android 平台开发和测试
2. 优化所有性能指标
3. Build & Publish
4. 世界自动在 Quest 和 Android 移动设备上可用

---

## 移动设备差异

| 设备 | 屏幕分辨率 | 性能 |
|------|-----------|------|
| Quest 2/3 | 高 | 中 |
| Android 手机 | 中-低 | 低 |
| Android 平板 | 中 | 中 |

> 好的 Quest 世界在手机上也会有良好表现

---

## 相关文档

- `memory/avatar/performance-rank.md` - 性能排名标准
- `memory/avatar/optimization-guide.md` - Avatar 优化
- `memory/world/performance-guide.md` - World 优化
- `memory/platform/mobile-ui-optimization.md` - 移动端 UI
- `memory/platform/cross-platform-content.md` - 跨平台内容