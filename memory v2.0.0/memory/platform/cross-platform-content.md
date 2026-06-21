---
title: Cross-Platform Content
category: platform

knowledge_level: applied
status: active

tags:
  - platform
  - avatar
  - udonsharp

aliases:
  - "Cross Platform"
  - 跨平台
  - "PC/Quest 兼容"
  - Cross-Platform

related:
  - "platform/easyquestswitch.md"
  - "platform/mobile-ui-optimization.md"
  - "avatar/optimization-guide.md"
  - "world/performance-guide.md"
  - "platform/android-development.md"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-10
confidence: High
---

---
# Cross-Platform Content


---

## Overview

VRChat 支持多平台（PC VR/Desktop、Android Quest、移动设备）。创建跨平台内容需要考虑平台差异。

---

## 平台支持

| 平台 | VR/Desktop | Quest | Mobile |
|------|------------|-------|--------|
| **Windows** | ✅ | - | - |
| **Quest** | - | ✅ | - |
| **Android Phone** | - | - | ✅ |
| **iOS** | - | 实验性 | ✅ |

---

## 平台切换

### Unity Build Settings
```
Edit → Build Settings
选择目标平台 → Switch Platform
```

### VRChat SDK
```
SDK Control Panel → Select Platform
```

---

## Avatar 跨平台要求

### Skeleton 一致性 ⚠️
PC 和 Android avatar 的 **armature 路径必须完全相同**：

```
✓ Correct
Armature
└── Hips ← root bone (scale/rotation must match)
    └── Spine
        └── Chest
            └── ...

✗ Incorrect  
Armature
└── Root (different name!)
    └── Hips
        └── ...
```

### Root Bone 规则
- **Hips** 是标准的 root bone
- PC 和 Android 版本的 Hips **scale 和 rotation 必须相同**
- 可以移除非必要骨骼（裙子、头发、尾巴等）
- **禁止**改变基础骨架层级结构

### 最佳实践
1. 从同一源文件创建 PC 和 Android 版本
2. 移除而非修改基础骨骼
3. 使用相同命名规范
4. 导出前验证 armature 结构

---

## World 跨平台

### 内容回退
VRChat 尝试自动加载最兼容的内容版本：
- Android 玩家加载 Android 版本
- PC 玩家加载 PC 版本

### 最佳化差异

| 方面 | PC | Android |
|------|-----|---------|
| 着色器 | 无限制 | Mobile Shaders |
| 几何 | 高复杂度 | 低复杂度 |
| 纹理 | 高分辨率 | 1K 最大 |
| 光照 | 实时可用 | 必须烘焙 |

---

## iOS 支持

VRChat 正在实验 iOS 支持系统：
- World 可自动回退到 Android 版本
- Avatar 需要上传 iOS 专用版本以获得最佳效果

---

## 工具链

### VCC Package Manager
管理跨平台项目：
```
VRChat SDK → Manage Packages
```

### EasyQuestSwitch
自动调整内容的平台适配：
```
VCC → Add Package → EasyQuestSwitch
```

功能：
- 平台特定的材质切换
- 骨骼简化
- 纹理降级

---

## 测试清单

- [ ] PC 平台正常运行
- [ ] Android/Quest 平台正常运行
- [ ] Avatar 在所有平台正确显示
- [ ] World 性能在所有平台可接受
- [ ] 跨平台查看无异常

---

## 相关文档

- `memory/platform/android-development.md` - Android 开发
- `memory/avatar/performance-rank.md` - 性能标准
- `memory/sources/example-central.md` - 示例中心