---
title: "VRChat Avatar 改模基础知识"
category: avatar
knowledge_level: applied
status: active
source: "VRCD 文档库"
source_type: community
version: 1.0
last_review: 2026-06-21
confidence: Medium
tags:
  - avatar
  - animator
  - modular-avatar
aliases:
  - "VRChat Avatar 改模基础知识"
  - avatar-modding-guide
related:
  - "avatar/ndmf-tools.md"
  - "avatar/animator-system.md"
  - ma-component-cards.md
  - ma2bt.md
  - modular-avatar-tutorials-detailed.md
---
# VRChat Avatar 改模基础知识

> 来源: VRCD 文档库 | 更新: 2026-06-21

---

## 开发环境

- **Unity 版本**: 2022.3.22f1
- **MA 当前版本**: 1.17.1+（2026-05-14 stable） | 1.18.0-alpha.0（2026-05-31 alpha）

---

## Bike Pose 问题

### 问题描述

这是 Unity（不是 Modular Avatar 或 VRCFury）的 Bug。

录制动画时，预览姿势可能被错误写入到场景中。如果**模型本身被完全解压缩**，将无法简单恢复成原始的 T-Pose 或 A-Pose。

**表现**：模型呈现扭曲的"自行车姿势"。

### 解决方案

使用 [Avatar Pose Matcher](https://github.com/ColorlessColor/Avatar_Pose_Matcher) 工具：

1. 下载 `.unitypackage` 并导入 Unity
2. 菜单栏 `Tools > Avatar Pose Matcher`
3. Bugged Avatar：拖入需要修复的模型
4. Target Avatar：拖入原版模型
5. 点击 **Match** 按钮

> ⚠️ Avatar Pose Matcher 会复制坐标和旋转数据，但**不会修改缩放（Scale）数据**

> 💡 不推荐使用旧的 Avatar_Matcher 脚本，Avatar Pose Matcher 是重写版，有更多错误检查。

---

## MA Merge Animator 的 WD 兼容问题

MA Merge Animator 有"匹配 Avatar WD"设置，上传模型时 SDK 会检查是否使用了未定义的参数。

> ⚠️ VRChat SDK 默认动画控制器都是 **WD OFF**

---

## 工程管理最佳实践

### 预制体（Prefab）与预制体变体（Prefab Variant）

- 使用 Prefab 和 Prefab Variant 管理组件，模块化工程
- 使用 git 进行版本控制
- 使用 VCC/ALCOM 进行包管理

### 导出注意事项

- 导出 unitypackage 时不要导出公共依赖
- 导入时注意导入列表

---

## 相关工具

| 工具 | 用途 |
|------|------|
| [Avatar Pose Matcher](https://github.com/ColorlessColor/Avatar_Pose_Matcher) | 修复 Bike Pose |
| [VRC Head Chop](https://creators.vrchat.com/avatars/avatar-components/vrc-headchop/) | 隐藏头上装饰品/光环/眼镜 |

---

## 相关文档

- `avatar/ndmf-tools.md` — NDMF 工具生态
- `avatar/animator-system.md` — Animator 系统