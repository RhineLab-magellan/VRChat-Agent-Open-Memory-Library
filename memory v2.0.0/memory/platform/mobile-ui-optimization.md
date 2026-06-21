---
title: Mobile UI Optimization
category: platform

knowledge_level: applied
status: active

tags:
  - platform
  - optimization
  - udonsharp

aliases:
  - "优化"

related:
  - platform/android-development.md
  - platform/cross-platform-content.md
  - api/ui.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-10
confidence: Medium
---
# Mobile UI Optimization

> 来源: VRChat 官方文档 (creators.vrchat.com/platforms/android/android-best-practices/)
> 置信度: High
---

## Overview

移动设备（Android/iOS）用户通过触摸屏交互，屏幕较小，性能受限。优化 UI 对移动用户体验至关重要。

---

## 平台差异

| 平台 | 控制方式 | 屏幕 | 性能 |
|------|----------|------|------|
| **VR** | VR 控制器 | N/A | 高 |
| **Desktop** | 键鼠 | 大 | 高 |
| **Mobile** | 触摸屏 | 小 | 中 |

---

## VRC_UIShape Component

### 配置 Canvas
移动设备 UI 必须正确配置 `VRC_UIShape`：

1. 在 Canvas 上添加 `VRC_UIShape` 组件
2. 设置 Shape Type（Rectangle/Ellipse）
3. 配置边界和交互区域

### Focus View
VRChat 的 "Focus View" 功能允许用户：
- 扩展 UI
- 平移 UI
- 缩放 UI

这对小屏幕上的可读性至关重要。

---

## 设计指南

### 1. 可读性 (Legibility)
- ✅ 使用大字号（至少 18pt+）
- ✅ 使用清晰易读的字体
- ✅ 高对比度颜色
- ❌ 小字体或低对比度

### 2. 简洁性 (Conciseness)
- ✅ 删除不必要的文字
- ✅ 使用图标和符号
- ❌ 大量文本阅读困难

### 3. 本地化 (Localization)
- ✅ UI 支持多语言
- ✅ 考虑文本扩展空间
- ❌ 硬编码文本

### 4. 触摸目标 (Touch Targets)
- ✅ 大按钮（至少 44x44 像素）
- ✅ 足够间距防止误触
- ❌ 小按钮或密集布局

### 5. 屏幕空间 UI (Screen-Space UI)
> **推荐**: 使用标准 Unity UGUI Canvas（Screen Space - Overlay/Camera）

屏幕空间 UI 在触摸屏上比世界空间面板更易交互：
- 不需要走过去
- 始终跟随视角
- 可使用 Focus View 放大

### 6. 方向检测
```csharp
public override void OnScreenUpdate()
{
    // 获取屏幕方向和分辨率
    // 触发时机：首次加载 + 方向改变
}
```

---

## 响应式设计

### 检测设备类型
```csharp
// 移动设备检测
bool isMobile = VRC.SDKBase.RuntimePlatform == Android;
```

### 自适应布局
```csharp
// 根据屏幕调整
if (Screen.width < 1000)
{
    // 移动设备布局
    uiCanvas.renderMode = RenderMode.ScreenSpaceOverlay;
}
else
{
    // PC/VR 布局
    uiCanvas.renderMode = RenderMode.WorldSpace;
}
```

---

## 测试方法

### Android
1. 启用设备 "Developer Mode" 和 "USB Debugging"
2. SDK → Build & Test → Android
3. 连接设备测试

### iOS
1. VRChat iOS App → 设置 → 输入 SDK 本地 IP
2. SDK → Build & Test → iOS

### 编辑器模拟
使用游戏手柄模拟移动触屏控制。

---

## 性能考虑

1. **Canvas 数量**: 减少 Canvas 数量
2. **Raycast Target**: 仅必要元素启用
3. **Graphic Raycaster**: 优化 raycast 频率
4. **静态 UI**: 静态元素使用静态批处理

---

## 最佳实践清单

- [ ] 使用大按钮（≥44px）
- [ ] 高对比度文本
- [ ] 删除冗余文本
- [ ] 支持多语言
- [ ] 使用屏幕空间 UI
- [ ] 实现 OnScreenUpdate 方向检测
- [ ] 测试 Focus View 功能
- [ ] 考虑文本扩展

---

## 相关文档

- `memory/platform/android-development.md` - Android 开发
- `memory/platform/cross-platform-content.md` - 跨平台内容
- `memory/api/ui.md` - UI API 参考