---
title: "Player Mod Setter"
category: world
subcategory: examples
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon-graph
  - udonsharp
aliases:
  - "Player Mod Setter"
  - player-mod-setter
related:
  - index.md
  - avatar-scaling-settings.md
  - simple-pen-system.md
  - udon-video-sync-player.md
  - world-audio-settings.md
---
# Player Mod Setter

> Udon Example Scene · VRCWorldSettings 子页面
> 源文档:https://creators.vrchat.com/worlds/examples/udon-example-scene/player-mod-setter/
> 最后更新:2026-06-15

---

## 概述

本 UdonBehaviour 示例脚本允许配置 World 中**玩家的移动参数**。

> **双版本**:
> - **UdonSharp**:`PlayerModSetter.cs`
> - **Udon Graph**:`VRCWorldSettings.asset`
>
> 两者功能相似,任选其一用于 VRChat World。

**Udon Graph 文件位置**:
```
Packages/com.vrchat.worlds/Samples/UdonExampleScene/UdonProgramSources/VRCWorldSettings.asset/
```

---

## 变量

| 名称 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `Jump Height` | float | `3` | 玩家跳跃强度,受重力影响 |
| `Run Speed` | float | `4` | **键盘输入**:前后移动且未按 Shift 键时的速度<br>**摇杆输入**:前后倾斜摇杆时的速度 |
| `Walk Speed` | float | `2` | **键盘输入**:前后移动且**按住** Shift 键时的速度<br>**摇杆输入**:始终使用 "Run Speed",不使用 "Walk Speed" |
| `Strafe Speed` | float | `2` | 左右移动速度 |
| `Gravity` | float | `1` | 重力对玩家的影响系数 |
| `Use Legacy Locomotion` | bool | `false` | 启用 VRChat 已弃用的旧版移动系统。**Udon 之后无法禁用** |

---

## 输入设备差异(关键细节)

| 设备 | Walk Speed 行为 | Run Speed 行为 |
|------|----------------|---------------|
| **键盘** | 按住 Shift 时使用 Walk Speed | 不按 Shift 时使用 Run Speed |
| **摇杆** | **不使用** Walk Speed | 始终使用 Run Speed |

> 这是 VRChat 移动系统的特殊设计,需要在 World 设计时考虑手柄用户体验。

---

## 使用注意

- `Use Legacy Locomotion = true` 后,**Udon 之后无法再设为 false**(单向设置)
- 默认值适配大多数 World,仅在需要特殊移动手感时调整

---

## 集成位置

`VRCWorldSettings` 是 `VRCWorld` Prefab 的**四大组件之一**。

**详见** [index.md#vrcworld](index.md#11-vrcworld)

---

## 与相关知识库关联

- **VRCWorld 整体架构**:[index.md](index.md)
- **Networking 模式**:`memory/api/networking.md`
