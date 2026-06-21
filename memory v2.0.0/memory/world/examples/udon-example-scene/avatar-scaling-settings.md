---
title: Avatar Scaling Settings
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - avatar
  - udonsharp

aliases:
  - "Avatar Scaling Settings"

related:
  - index.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Avatar Scaling Settings

> Udon Example Scene · Avatar Scaling 子页面
> 源文档:https://creators.vrchat.com/worlds/examples/udon-example-scene/avatar-scaling-settings/
> 最后更新:2026-06-15

---

## 概述

本示例 UdonBehaviour 脚本允许**轻松覆盖 World 的 Avatar Scaling 设置**。

> 编写自定义 Avatar Scaling Udon 脚本:参考 [Avatar Scaling 文档](https://creators.vrchat.com/worlds/avatars#avatar-scaling)

**程序位置**:`VRCWorld.prefab` 内的 `Avatar Scaling Settings` 组件

---

## 变量

| 名称 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `disableAvatarScaling` | bool | `false` | 禁用 Avatar 缩放 |
| `minimumHeight` | float | `0.2` | 玩家可选的最小 Avatar 眼睛高度(米) |
| `maximumHeight` | float | `5` | 玩家可选的最大 Avatar 眼睛高度(米) |
| `alwaysEnforceHeight` | bool | `false` | 启用后,玩家切换到过高/过矮 Avatar 时自动设为 minimumHeight / maximumHeight |

> **任务提示词中提到的 0.5x-1.5x 范围**:**实际默认值**为 0.2m(最小眼睛高度)~ 5m(最大眼睛高度),并非字面意义的缩放倍数。

---

## 配置示例

### 场景 1:允许玩家自由缩放 Avatar

**不需要修改任何设置**(使用默认 0.2m ~ 5m 范围)。

### 场景 2:禁止玩家缩放 Avatar

- 启用 `disableAvatarScaling`

### 场景 3:限制玩家使用特定 Avatar 高度

- 按需设置 `minimumHeight` 和 `maximumHeight`
- 如果要防止过高/过矮 Avatar,启用 `alwaysEnforceHeight`

---

## 集成位置

`Avatar Scaling Settings` 是 `VRCWorld` Prefab 的**四大组件之一**,与 VRC Scene Descriptor、VRC Pipeline Manager、VRCWorldSettings 并列。

**详见** [index.md](index.md#11-vrcworld)

---

## 与相关知识库关联

- **VRCWorld 整体架构**:[index.md#vrcworld](index.md)
- **Avatar 系统**:`memory/avatar/` 域
- **VRCPipelineManager**:`memory/avatar/vrcpipeline-manager.md`
