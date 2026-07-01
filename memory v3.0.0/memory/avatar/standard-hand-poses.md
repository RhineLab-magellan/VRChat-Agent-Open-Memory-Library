---
title: VRChat Standard Hand Poses — 7 种标准手姿定义
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - hand-pose
  - gesture
  - valve-index
  - oculus-touch
  - controller-bindings

aliases:
  - Standard Hand Poses
  - 标准手姿
  - 手势定义
  - Hand Pose
  - Fist
  - Open Hand
  - Point
  - Thumbs Up
  - Victory
  - Hand Gun
  - Rock N Roll

related:
  - avatar/skeletal-input.md
  - avatar/animator-system.md
  - avatar/playable-layers.md
  - avatar/modular-avatar.md
  - platform/mobile-ui-optimization.md

source: docs.vrchat.com/docs/valve-index + docs.vrchat.com/docs/touch
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Standard Hand Poses — 7 种标准手姿定义

> 来源:
> - https://docs.vrchat.com/docs/valve-index
> - https://docs.vrchat.com/docs/touch
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方手势定义)
> 关联: `avatar/skeletal-input.md` (手指追踪) + `avatar/animator-system.md` (手势参数)

---

## 概述

> [FACT] VRChat 定义了 **7 种标准手姿**，用于触发 **Gesture Animator Parameters**。
>
> - **手姿是玩家必须做的物理手势**
> - 创作者在 **Avatar Animator** 中**监听这些手势**并响应
> - **不同控制器的传感器数量不同**，导致手姿定义**有差异**

> **🔴 关键事实**:
> - **Valve Index** 控制器有 **5 指 capacitive sensors**（5 指都可独立追踪）
> - **Oculus Touch** 控制器只有 **3 指被定义**（中/食指/拇指），其他指根据食指/中指推断
> - 两种控制器**手势定义不同**（见下表）

---

## 1. 7 种标准手姿（共同定义）

> [FACT] VRChat 标准手姿包括以下 7 种。

| 手姿 | 中文 | 描述 |
|------|------|------|
| **Fist** | 拳 | 4 指全下 + 拇指下 |
| **Open Hand** | 张开 | 4 指全上 + 拇指上 |
| **Point** | 指点 | 中/无名/小指下 + 食指未按 + 拇指下 |
| **Thumbs Up** | 点赞 | 中/无名/小指下 + 食指按 + 拇指上 |
| **Victory** | 胜利 (V) | 小/无名指下 + 中指上 + 食指未按 + 拇指下 |
| **Hand Gun** | 手枪 | 中/无名/小指下 + 食指未按 + 拇指上 |
| **Rock N Roll** | 摇滚 | 小指上 + 无名/中指下 + 食指未按 + 拇指下 |

> **手势数值**: 在 Animator 中，Gesture 数值 **0 = Neutral, 1 = Fist, 2 = Open Hand, 3 = Point, 4 = Victory, 5 = Rock N Roll, 6 = Hand Gun, 7 = Thumbs Up**。
>
> 详见 `avatar/animator-system.md`

---

## 2. Valve Index 手姿（5 指精确定义）

> [FACT] **Valve Index Controllers** 包含以下 capacitive sensors:
> - **pinky** (小指)
> - **ring** (无名指)
> - **middle** (中指)
> - **trigger** (食指, 通过 trigger 按压)
> - **thumbpad/touchpad/buttons** (拇指)
> - **squeeze** sensor (握力)

> [FACT] **Index 控制器有 5 指独立追踪**，手势定义**精确**。

### 2.1 Index 7 种手姿完整表

| 手姿 | 小指 | 无名指 | 中指 | 食指 | 拇指 |
|------|------|--------|------|------|------|
| **Fist** | Down | Down | Down | Trigger | Down |
| **Open Hand** | Up | Up | Up | No trigger | Up |
| **Point** | Down | Down | Down | No trigger | Down |
| **Thumbs Up** | Down | Down | Down | Trigger | Up |
| **Victory** | Down | Down | **Up** | No trigger | Down |
| **Hand Gun** | Down | Down | Down | No trigger | Up |
| **Rock N Roll** | **Up** | Down | Down | No trigger | Down |

### 2.2 Index Finger Posing 原理

> [FACT] **在 Index 控制器上**:
> - 手指**始终**追踪控制器上传感器的状态
> - 追踪**不完全精确**（开/合状态足够）
> - 这种持续追踪**改善沉浸感**

### 2.3 创作者影响

> [FACT] **Index 用户做手势时，Avatar 手指立即响应**（无需 Gesture Toggle）。
>
> 创作者可以**精确控制**每种手势的 Avatar 表现。

---

## 3. Oculus Touch 手姿（3 指简略定义）

> [FACT] **Oculus Touch Controllers** 只有 **3 个明确的手指**:
> - **Middle** (中指, 通过 grip pull 推断)
> - **Index** (食指, 通过 trigger pull 推断)
> - **Thumb** (拇指, 通过 thumbstick/button 推断)
>
> **小指 (pinky) 和无名指 (ring) 的状态通过算法推断**，不是独立追踪。

### 3.1 Touch 7 种手姿完整表

| 手姿 | 中指 | 食指 | 拇指 |
|------|------|------|------|
| **Fist** | Down | Trigger | Down |
| **Open Hand** | Up | No trigger | Up |
| **Point** | Down | No trigger | Down |
| **Thumbs Up** | Down | Trigger | Up |
| **Victory** | Up | No trigger | Down |
| **Hand Gun** | Down | No trigger | Up |
| **Rock N Roll** | Up | Trigger | Down |

### 3.2 Touch 与 Index 关键差异

> [FACT] **重要差异**:
> 1. Touch **没有** independent pinky/ring 追踪
> 2. **Rock N Roll** 在 Touch 上是"中指上 + 食指按"
> 3. **Victory** 在 Touch 上是"中指上 + 食指未按"
> 4. Index 区分 Rock N Roll 与 Victory 通过**小指**位置

### 3.3 创作者适配

> [FACT] **为 Touch 设计 Avatar 时**:
> - **不要假设** 5 指独立追踪
> - 测试时**两种控制器**都试
> - **手势检测**应基于 Animator Parameters（0-7 数值），不是物理手指

---

## 4. 触发表（Quick Reference）

> [FACT] 玩家需要做这些手势来触发 Animator 中的 Gesture 参数。

### 4.1 Index 用户手势提示

> [FACT] Valve Index 提示:
> - 用 **5 指传感器** 准确做手势
> - 闭手时**注意 pinky/ring 弯曲**（可能在 4 指都弯下时不明显）

### 4.2 Touch 用户手势提示

> [FACT] Oculus Touch 提示:
> - **用 grip pull 中指** (不像 Index 那样直接)
> - **Thumb 状态**通过 thumbstick 推断

---

## 5. Action Menu 交互与手姿

> [FACT] **Action Menu 打开方式**:
>
> | 控制器 | Action Menu 唤起方式 |
> |--------|---------------------|
> | **Valve Index** | 点击 Joystick In（默认）|
> | **Oculus Touch** | 点击 Joystick In（默认）|
> | **Vive Wand** | 长按 Menu 按钮 |
> | **其他带 Joystick** | 点击 Joystick In |
> | **桌面** | 按 **R** 键 |

> 详细见 `avatar/expression-menu.md` (待入库)

---

## 6. 按钮分配（与手姿无关）

> [FACT] **Valve Index 按钮分配**:

| 按钮 | 分配 |
|------|------|
| **Right A** (底部右侧按钮) | Jump |
| **Left A** (底部左侧按钮) | Toggle Mute |
| **B** (顶部按钮) | Quick Menu |
| **Touchpad Touch/Press/Scroll** | Reserved for future features |
| **Grip** (squeeze) | Grab / Equip |
| **Trigger** (index finger pull) | Use / Interact |
| **Right Thumbstick** | Turn |
| **Left Thumbstick** | Locomote |
| **Right Thumbstick In** | Action Menu Right |
| **Left Thumbstick In** | Action Menu Left |

> [FACT] **Oculus Touch 按钮分配**:

| 按钮 | 分配 |
|------|------|
| **A** (右手底) | Jump |
| **X** (左手底) | Mute |
| **B / Y** (顶) | Quick Menu |
| **Grip** (中指 pull) | Pick Up |
| **Trigger** (食指 pull) | Select / Interact |
| **Right Thumbstick** | Turn |
| **Left Thumbstick** | Locomote |
| **Right Thumbstick In** | Action Menu Right |
| **Left Thumbstick In** | Action Menu Left |
| **Both Triggers + Both Menu** | **Safe Mode** ⭐ |

> ⚠️ **Touch 的 "Both Triggers + Both Menu"** 是 Safe Mode 触发键（不同于桌面 Shift+Esc）。
> 详见 `avatar/safety-system.md` §5

---

## 7. Index 自定义绑定注意事项

> [FACT] **Index 创作者侧重要提示**:

### 7.1 thumb-touchable 按钮约束

> [FACT] VRChat **检查每个 thumb 可触及按钮的 touch 事件**来判断拇指是否弯曲。
>
> ⚠️ **如果 thumb-touchable 按钮没有为相同 touch 事件分配，VRChat 无法判断拇指弯曲，手部追踪不正确**。

### 7.2 Hard Input Bindings

> [FACT] 以下 binding 是 **hard input**（不可重新分配）:
> - `Jump`
> - `Mic Toggle`
> - `Gesture Toggle`
> - `Action Menu Left / Right`

---

## 8. 创作者 Avatar Rigging 指南

> [FACT] **VRChat 创作者使用 Unity 的 Mechanim + Mixamo "YBot" 角色**作为标准 rigging 设置。

### 8.1 测试方法

> [FACT] **用 Unity Avatar Muscles & Settings tab 测试**:
> - 切换 **Hand open/closed state**
> - 检查手姿是否**正确显示**
> - 如异常，**调整 weight-painting 和 rigging**

### 8.2 创作者目标

> [FACT] **创作者希望**:
> - Index 用户做手势时，Avatar **手部立即响应**
> - Touch 用户做手势时，Avatar **手部立即响应**
> - **两种控制器的 Avatar 表现一致**

### 8.3 配置建议

> [FACT] 创作者应:
> 1. **调整 finger muscle ranges** 以适应多控制器
> 2. **测试两种控制器**
> 3. 必要时启用 **Legacy Fingers** 兼容性
> 4. 考虑 **Avatar Performance**（更多手指骨骼 = 更高 Performance Rank）

---

## 9. 玩家常见问题

### Q1: 为什么我的 Avatar 手指不响应 Skeletal Input?

> 可能原因:
> 1. 控制器**未正确连接**
> 2. 驱动**版本过旧**（特别是 Virtual Desktop < 1.32.13）
> 3. Avatar 肌肉范围**配置不当**
> 4. 启用了 **Legacy Fingers**（per-avatar 关闭）
> 5. 启用了 **Safe Mode**

### Q2: 7 种手姿我可以自己定义吗?

> **不能**。7 种手姿是 VRChat 平台固定定义。玩家必须**做出相应手姿**才能触发。

### Q3: Index 和 Touch 哪个更精确?

> [FACT] **Index 更精确**（5 指独立追踪）。Touch 通过算法推断无名指和小指。

### Q4: Action Menu 怎么开?

> [FACT] 默认方式:
> - **Index/Touch**: 点击 Joystick In
> - **Vive**: 长按 Menu 按钮
> - **桌面**: 按 R 键

---

## 10. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `avatar/skeletal-input.md` | Skeletal Input 与手指追踪的来源 |
| `avatar/animator-system.md` | Gesture Animator Parameters 接收手姿输入 |
| `avatar/playable-layers.md` | Gesture Layer 处理手姿 |
| `avatar/modular-avatar.md` | MA Gestures 组件基于手姿 |
| `avatar/safety-system.md` | Safe Mode 快捷键 |
| `platform/mobile-ui-optimization.md` | 移动端手部 UI |

---

## 11. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **7 种手姿的 Animator 数值映射**（0-7）的官方映射表
2. ❓ **混合手势**（例如 Point + Thumbs Up）如何处理
3. ❓ **手姿转换阈值**（传感器值如何映射到手势分类）
4. ❓ **混合现实** (Mixed Reality) 控制器的手势定义
5. ❓ **VRChat 内部**对手势检测的算法细节
6. ❓ **5 指 vs 3 指** 的精确算法差异
7. ❓ **Hand Tracking 模式**下的手姿定义

---

## 来源

- [Valve Index Controllers](https://docs.vrchat.com/docs/valve-index)
- [Oculus Touch](https://docs.vrchat.com/docs/touch)
- [SteamVR Input 2.0](https://docs.vrchat.com/docs/steamvr-input-20)
- [VRChat Hand Poses](https://docs.vrchat.com/docs/valve-index#section-vrchat-standard-hand-poses)
- 本地化版本: `参考文献/SP/user-guide/valve-index.md` + `touch.md`
