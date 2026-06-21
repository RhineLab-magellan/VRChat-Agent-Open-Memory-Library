---
title: VRChat Playable Layers 知识库
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - animator
  - playable-layer

aliases:
  - "Playable Layers"
  - 播放层
  - "Avatar 播放层"
  - "FX Layer"

source: creators.vrchat.com/avatars/playable-layers/
source_type: community
version: 1.0
last_review: 2026-06-05
confidence: High
---

---
# VRChat Playable Layers 知识库


---

## 目录

1. [概述](#1-概述)
2. [Humanoid vs Generic](#2-humanoid-vs-generic)
3. [层级顺序](#3-层级顺序)
4. [各层详解](#4-各层详解)
5. [附加姿势](#5-附加姿势)
6. [Avatar Mask 规则](#6-avatar-mask-规则)
7. [VRCFury 集成](#7-vrcfury-集成)

---

## 1. 概述

Playable Layers 允许将 Avatar 功能分离到独立的动画层中，如跑步、跳跃、点赞、微笑、摇尾巴等。

### 需要的基础知识

- Unity Animator Controller
- Avatar Mask
- Blend Trees

---

## 2. Humanoid vs Generic

### Humanoid Avatar（人形Avatar）

5个 Playable Layers:
| 层级 | 说明 |
|------|------|
| **Base** | 基础运动层 |
| **Additive** | 叠加层 |
| **Gesture** | 手势层 |
| **Action** | 动作层 |
| **FX** | 特效层 |

### Generic Avatar（通用Avatar）

3个 Playable Layers:
| 层级 | 说明 |
|------|------|
| **Base** | 基础运动层 |
| **Action** | 动作层 |
| **FX** | 特效层 |

---

## 3. 层级顺序

层级按顺序应用：

```
Base → Additive → Gesture → Action → FX
```

**优先级**: FX 最高，Base 最低

**示例**: 如果 Additive 动画骨骼（权重1.0），然后 Action 也动画同一骨骼（权重1.0），**Action 优先**。

---

## 4. 各层详解

### 4.1 Base Layer

**用途**: 始终播放的功能，响应移动（locomotion），如行走、跑步、跳跃、跌落、蹲下等。

**要求**:
- ✅ 只影响 Transform
- ✅ 使用 Avatar Mask 确保只影响适当的 Transform

**注意**: 在此层添加内容需要重新定义 locomotion 动画状态，非常复杂。

### 4.2 Additive Layer

**用途**: 在 Base 层已有的基础上"添加"动画，如呼吸动画。

**重要**:
- ⚠️ **仅用于人形骨骼**
- ❌ 非人形骨骼（尾巴、耳朵等）应使用 **Gesture** 层

**特点**:
- 始终设置为 "Additive" 混合模式
- 如果骨骼在 locomotion 期间移动，Additive 动画会叠加在上面

**注意**: 第一个 Additive 层的 Avatar Mask 会被忽略（内部屏蔽用途）。

### 4.3 Gesture Layer

**用途**: 需要在播放底层动画的同时作用于特定身体部位的动画。

**功能**:
- 手势触发（Hand OR Expression Menu）
- 闲置动画（尾巴摇摆、翅膀拍动、耳朵移动等）
- 非人形骨骼动画

**要求**:
- ✅ 只影响 Transform
- ✅ 使用 Avatar Mask 确保只影响目标部位

### 4.4 Action Layer

**用途**: 完全覆盖其他层的骨骼动画，类似 AV2 Emotes。

**重要**:
- ⚠️ **默认混合到零**
- ⚠️ 在 Action 层做任何事之前，必须使用 **Playable Layer Control** 状态行为将层混合上来
- ⚠️ 完成时必须混合回零

### 4.5 FX Layer

**用途**: 处理所有**非 Transform** 的动画。

**特点**:
- ✅ 全部复制到镜像克隆（与其他层不同）
- ✅ 可以启用/禁用 GameObject
- ✅ 可以修改组件、材质、Shader 属性
- ✅ 可以动画粒子系统

**包含**:
- 启用/禁用 GameObject
- 组件修改
- 材质切换
- Shader 动画
- 粒子系统动画
- Blend Shape 动画

**注意**:
- ⚠️ 不建议在 FX 层动画 Transform
- 第一层 FX 默认 mask 会禁用所有人形肌肉但启用所有 GameObject 动画

---

## 5. 附加姿势

### 5.1 T-Pose

自定义 T-Pose 用于：
- 确定 Avatar 测量（尤其是视点位置）
- 手腕对齐/扭曲
- 翼展（影响 IPD）

**注意**:
- T-Pose 中的关节弯曲会影响 Avatar 比例
- 肘部弯曲可能影响多个功能

### 5.2 IK Pose

IK Pose 用于确定主要关节弯曲方向。

**膝盖弯曲规则**:
- 脚向外旋转 → 膝盖向内弯曲
- 脚向内旋转 → 膝盖向外弯曲

### 5.3 Sitting Pose

Sitting Pose 用于：
- 坐姿时视点校准
- 坐姿动画和闲置动画

**注意**: 自定义可能需要大量调整，建议使用过渡状态。

---

## 6. Avatar Mask 规则

### 6.1 冲突规则

如果 Gesture 中有非肌肉动画（如 Transform），这些 Transform **必须**在 FX mask 中禁用。

### 6.2 示例

**场景**:
- Avatar 有尾巴（非人形骨骼链）
- Gesture 动画层有尾巴的特殊 mask
- 另一个 Gesture 动画层有"所有部位"mask

**解决方案**:
1. 在第一层 FX 创建自定义 mask
2. 禁用所有肌肉（人形图全部红色）
3. 禁用尾巴中的所有骨骼
4. 启用任何 FX 动画的 Transform（如用于 blend shape 或材质的蒙皮网格）

### 6.3 常见问题

**问题**: GameObject 同时有 Gesture 中的动画 Transform 和 FX 中的效果组件

**解决方案**:
- 创建子 GameObject 放置静态网格或效果
- 不动画子对象的 Transform，只动画父对象

---

## 7. VRCFury 集成

### VRCFury Components（Avatar 自动化）

| 组件 | 用途 |
|------|------|
| Armature Link | 服装/道具附加到骨骼 |
| Full Controller | 合并完整 animator/expression menu/parameters |
| Gestures | 基于手势创建动画 |
| Global Collider | 全局 PhysBone collider 和 Contact sender |
| Toggle | 菜单切换、按钮、滑块 |
| Other | 高级功能 |

### VRCFury 中的 Constraint 使用

**Cross-Eye Fix**:
- 使用 rotation constraints 消除眼睛滚动
- 自动修复 VRChat 引入的眼睛骨骼滚动问题

### 重要提示

⚠️ **不要在多个 Playable Layers 中使用相同的 controller**

这可能导致某些设置正常工作，但随着 Avatar 功能扩展会造成重大问题。

---

## 8. Avatar Animator = 参数驱动系统

### 核心定义

```
Avatar Animator = VRChat 对 Unity Animator 的特殊封装
驱动方式 = VRChat Parameters 驱动状态机
```

### 工作流

```
Expression Menu
        ↓
Expression Parameter（参数）
        ↓
Playable Layer（Animator Controller）
        ↓
State Machine
        ↓
Animation Clip
        ↓
Avatar
```

**关键特点**：
- 控制来源：VRChat Parameters（手势、表情、菜单项）
- 无需 Udon 脚本，参数自动驱动
- VRChat 自动同步部分参数
- 核心用途：表情、菜单、手势、Toggle

### 内置驱动参数

```csharp
VelocityMagnitude  → 速度
GestureLeft       → 左手势
GestureRight      → 右手势
IsLocal           → 本地/远程
// 以及用户定义的 Expression Parameters
```

### Playable Layers 中的驱动方式

| Layer | 驱动源 | 说明 |
|-------|--------|------|
| Base | 移动输入 | Locomotion 状态机 |
| Additive | 持续 | 呼吸等叠加动画 |
| Gesture | 手势触发 | 手势 + Expression Menu |
| Action | 动作触发 | Emotes 完全覆盖 |
| FX | 菜单参数 | Toggle、Button、Slider |

### Avatar vs World 核心区别

| 方面 | Avatar Animator | World Animator |
|------|-----------------|----------------|
| 运行主体 | 玩家 Avatar | 场景物体 |
| 控制来源 | VRChat Parameters | Udon / Script |
| 脚本控制 | ❌ 不支持 | ✅ 支持 |
| 网络同步 | VRChat 自动同步 | 开发者自行同步 |
| 开发模式 | **参数驱动** | **逻辑驱动** |

## SDK 示例文件

位置: `Packages/com.vrchat.avatars/Samples/AV3 Demo Assets/Animation/Controllers`

| Playable Layer | 文件名 |
|----------------|--------|
| Base | `vrc_AvatarV3LocomotionLayer` |
| Additive | `vrc_AvatarV3IdleLayer` |
| FX | `vrc_AvatarV3FaceLayer` |
| Action | `vrc_AvatarV3ActionLayer` |
| Gesture | `vrc_AvatarV3HandsLayer` |

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-06-05 | 初始创建 |

## 来源

- creators.vrchat.com/avatars/playable-layers/
- vrcfury.com/components/