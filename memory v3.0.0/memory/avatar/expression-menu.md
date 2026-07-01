---
title: Action / Expression / Puppet Menu — Avatar 菜单三层结构
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - action-menu
  - expression-menu
  - puppet-menu
  - widget
  - ui

aliases:
  - Action Menu
  - Expression Menu
  - Puppet Menu
  - Flick Select
  - Pick Select
  - 动作菜单
  - 表情菜单
  - 控件
  - 手柄菜单

related:
  - avatar/playable-layers.md
  - avatar/modular-avatar.md
  - avatar/standard-hand-poses.md
  - avatar/skeletal-input.md
  - avatar/animator-system.md
  - platform/mobile-ui-optimization.md

source: docs.vrchat.com/docs/action-menu
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Action / Expression / Puppet Menu — Avatar 菜单三层结构

> 来源: https://docs.vrchat.com/docs/action-menu
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方 Action Menu 文档)
> 关联: `avatar/playable-layers.md` (FX Layer 接收菜单参数) + `avatar/modular-avatar.md` (Full Controller 组件)

---

## 概述

> [FACT] **Action Menu** 是访问 Avatar 控件和**快速访问**控件的**主要方式**。
>
> - 当使用 **Avatars 3.0** Avatar 时，这些控件**完全可定制**
> - 可作为**多种类型**之一（Button/Toggle/Slider/Stage/Puppet...）
> - **驱动** Animator Parameters 告知 Avatar 如何反应

> **🔴 关键事实（创作者角度）**:
> - 玩家在 Action Menu 中做的**任何操作** = 触发 **Animator Parameter 变化**
> - 创作者需在 **FX Layer** 中**监听**这些参数
> - 菜单结构是**三层**: Action Menu → Expression Menu → Puppet Menu

---

## 1. 三层菜单结构

> [FACT] **UI 有 3 个层级**:
> 1. **Action Menu**（根菜单）
> 2. **Expression Menu**（表达式菜单）
> 3. **Puppet Menu**（木偶菜单）

### 1.1 Action Menu（根菜单）

> [FACT] **Action Menu** 是**根菜单**。
>
> 当前**包含内容**:
> - **Gesture Toggle**（手势开关）
> - **Config**（UI 配置）
> - **Emojis**（表情）
> - **Expression Menu**（进入下层）
> - **Close**（关闭）

### 1.2 Expression Menu（表达式菜单）

> [FACT] **Expression Menu** 可包含各种 **Widgets**（控件），包括 **Stages**（舞台）。
>
> - 进入**包含 Puppets 的 Stage** = 进入该 Stage 的 **Puppet Mode**
> - **每个 Expression Menu** 可有**多个 Stage**
> - 可**同时在每只手上**打开菜单

#### 1.2.1 Widgets（控件）

> [FACT] Widgets 包括:
> - **Button**（按钮）
> - **Toggle**（开关）
> - 其他控件类型
>
> **创作者可配置**这些 Widgets，**它们以各种方式作用**于 Animator Parameters。

#### 1.2.2 Stages（舞台）

> [FACT] **Stage** 是一种特殊 Widget，用于**进入 Puppet Mode**。
>
> - Stage **包含 Puppets**（木偶）
> - 进入 Stage 后**进入 Puppet Mode**（驱动手柄/鼠标值）
> - 创作者可定义**多个 Stage**（如 "Emotes" / "Mood" / "Toggles"）

### 1.3 Puppet Menu（木偶菜单）

> [FACT] **Puppet Menu** 驱动 Avatar 的各种**值/参数**。
>
> - **构建 Avatars 3.0 Avatar** 时由创作者**映射**这些参数
> - 在此模式中，**移动摇杆** / **触摸 Vive 触摸板** / **使用鼠标** 即可"玩"木偶效果
>
> **使用方式**:
> - **移动摇杆** → 驱动 Animator Parameter 连续变化
> - **停止移动** → 参数回到默认
> - 可实现**混合动画**（如 "happy" + "surprised" 同时存在）

> [FACT] **从 Puppet Menu 返回 Expression Menu**:
> - **拉 Trigger**（手柄归中时）= 回到 Expression Menu
> - 再拉 Trigger = 回到 Action Menu

> **Puppet Menu 示例效果**: 不同方向摇杆 = 不同心情（happy / surprised / sad...），可**连续混合**。
> 详见 §5 示例

---

## 2. 两种选择方式：Flick vs Pick

> [FACT] 径向菜单中有**两种选择方法**。

### 2.1 Flick Select（弹选）⭐ 默认

> [FACT] **Flick** 模式:
> - **推动摇杆**指向想要的扇区方向
> - **推动一段** → 显示**指示器**（预览）
> - **完全推到底** → **触发选择**
>
> 类比: **像"弹"出**选择（flick = 弹）

### 2.2 Pick Select（点选）

> [FACT] **Pick** 模式:
> - **推动摇杆**指向想要的扇区方向
> - **再用 Trigger 确认**选择（桌面用鼠标移动 + LMB）
> - 两步选择
>
> 类比: **像"瞄准后扣扳机"**

### 2.3 默认值

> [FACT] **默认是 Flick**（Vive 除外）。
>
> 切换方法: **Action Menu > Settings > Flick enabled** 设置。

### 2.4 桌面模式

> [FACT] 桌面模式**特殊行为**:
> - **只能打开一个菜单**（不能双开）
> - **必须点击确认**选择
> - **Flick** 模式 = 鼠标移动 + 点击

---

## 3. 关闭与记忆（Closing and Saving）

> [FACT] **菜单关闭机制**:

### 3.1 Back 选项

> [FACT] 在 **Action / Expression 菜单**或任何子文件夹中:
> - 选 **Back** 选项 = 退出文件夹/菜单（breadcrumb 上移）
> - 持续选 Back = 关闭菜单

### 3.2 摇杆点击（短期关闭）

> [FACT] **单次点击摇杆**:
> - **关闭菜单**
> - **记忆**当前所在位置
> - 下次打开 = **回到上次位置**

### 3.3 应用场景

> [FACT] 这个"记忆位置"设计:
> - 玩家**常用**某个深嵌套菜单 → 不必每次都从根目录导航
> - **来回切换** 主菜单和深嵌套菜单的体验**流畅**
> - **创作者** 设计菜单时考虑玩家的"工作流路径"

---

## 4. 控制器操作详解

> [FACT] 各控制器打开 Action Menu 的方法:

### 4.1 Valve Index

> [FACT] **打开方式**: 点击对应手的 **Joystick**（默认）
> **Back / 选 Pick 模式**: 用 **Trigger**

### 4.2 Oculus Touch

> [FACT] **打开方式**: 点击对应手的 **Joystick**（默认）
> **Back / 选 Pick 模式**: 用 **Trigger**

### 4.3 Vive Wand

> [FACT] **打开方式**: **长按**控制器顶部的 **Menu 按钮**
>
> ⚠️ Vive 与 Index/Touch **不同**: Vive 必须长按

### 4.4 其他带摇杆的控制器

> [FACT] **打开方式**: **点击摇杆**（Joystick In）
> **Back / 选 Pick 模式**: 用 **Trigger**

### 4.5 通用方法

> [FACT] **所有控制器**: **长按 Quick Menu 按钮** 也能拉起 Action Menu

### 4.6 桌面模式

> [FACT] 桌面模式: **按 R 键** 拉起 Action Menu。
> - 移动鼠标选择
> - 点击确认
> - 点击 Back 选项退出

> 详细见 `avatar/standard-hand-poses.md` §5 (Action Menu 唤起方式对照表)

---

## 5. Puppet Menu 示例

> [FACT] **Puppet Menu 的典型用法**:
>
> <Image title="Puppet Menu" align="center" width="800px" src="https://media2.giphy.com/media/c63LdtLhEHe95HGbWC/giphy.gif" />
>
> 玩家移动摇杆/触摸板/鼠标到**不同方向** = 驱动**不同** Animator Parameter 值。
> 示例设置允许在**各种心情间混合**（如 "happy" 和 "surprised" 任意混合）。

> **关键事实**:
> - **任何可参数化的东西**都能从 Puppet Menu 读取
> - 包括 **Toggle on/off 按钮**和其他 UI 元素
> - **不止**示例中展示的"心情"用法
> - ⚠️ 部分 UI 元素类型（如新的 Toggle）**VRChat 仍在开发中**（源文档原文 "still working on"）

### 5.1 双菜单支持

> [FACT] **菜单可同时在两只手打开**（或单手）。
> - 默认: Flick 模式
> - 在 Action Menu UI 内的 **Settings** 中可切换为 Trigger 确认

### 5.2 退出 Puppet Menu

> [FACT] **退出 Puppet 回到 Expression 菜单**:
> - **拉 Trigger** 一次 = 回到 Expression 菜单
> - **再拉 Trigger** 一次 = 回到 Action 主菜单

---

## 6. Debug Menu（创作者/高级玩家）⭐

> [FACT] **Debug Menu** 在 Action Menu 中**可用**。
>
> - 弹出**文本显示**
> - 显示 Avatar **当前 animator state**
> - 包含: **parameter values / tracking states / current motion states** 等详情
> - **调试时非常有用**

> **创作者**应:
> - 在调试 Avatar 时**使用** Debug Menu
> - 查看参数是否按预期变化
> - 检查 motion state 是否正确触发

---

## 7. 平台限制

> [FACT] **Quest Hand Tracking Beta**:
> - **目前无法访问** Action Menu
> - **替代方法**: 使用 **Quick Menu wing** 控制 Avatar
>
> 详见 `platform/mobile-ui-optimization.md`

---

## 8. 创作者设计建议

> [FACT] **菜单设计的最佳实践**（基于官方文档）:

### 8.1 控件选择

> [FACT] **根据功能选 Widget**:
> - **瞬时动作**（如挥手）→ **Button**
> - **二值状态**（如开/关帽子）→ **Toggle**
> - **进入子菜单**（如情绪控制）→ **Stage**
> - **连续控制**（如表情强度）→ **Puppet**

### 8.2 菜单深度

> [FACT] **考虑玩家导航成本**:
> - 玩家每次"Back"操作**消耗操作**
> - **太深嵌套** = 玩家不常用该功能
> - **记忆位置**机制可缓解，但**不要**滥用嵌套

### 8.3 双手同时打开

> [FACT] 玩家可**同时在两只手打开菜单**（独立 Expression Menu）。
>
> **创作者角度**:
> - **可利用**这个特性做**双手协调**功能
> - 例如: 左手调音量 / 右手调表情
> - **不要假设**玩家只用单手

### 8.4 Puppet Menu 设计

> [FACT] Puppet Menu 适合:
> - **连续变化**参数（不限于二值）
> - **多维控制**（如 2D 摇杆 = 2 个参数）
> - **混合动画**（让玩家"摸索"有趣的中间状态）

### 8.5 Bindings 自定义

> [FACT] 玩家在 **Action Menu > Settings > Bindings** 中可**自定义**:
> - **打开 Action Menu** 的方式
> - 常见自定义示例: **"clicking in the joystick"**（设置点击摇杆打开 Action Menu）
>
> 创作者应**避免**假设默认绑定（玩家可能改过）。

---

## 9. 玩家常见问题

### Q1: Quest Hand Tracking 怎么用 Action Menu?

> 目前**不支持**。用 **Quick Menu wing** 替代控制 Avatar。

### Q2: 菜单"记住位置"怎么清掉?

> **完全关闭**菜单（Back 到顶层）即可。下次打开从**根菜单**开始。

### Q3: Flick vs Pick 怎么选?

> [FACT] **Flick 优势**:
> - **单手单步**操作（更快）
> - 适合**频繁切换**（如战斗中切换装备）
>
> **Pick 优势**:
> - **误触少**（需二次确认）
> - 适合**重要但罕见**操作（防误触）

### Q4: Puppet Menu 只能控制"心情"吗?

> **不是**。任何 Animator Parameter 都可被 Puppet 驱动。示例中的"心情"只是**最直观**的用法。

### Q5: 两手同时开菜单有什么区别?

> [FACT] 每只手**独立**打开 **Expression Menu**（可在每个手上配不同 Expression）。
> - 玩家可在**左手**开 "Emotes" + **右手**开 "Toggles"
> - **互不干扰**

---

## 10. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `avatar/playable-layers.md` | FX Layer 接收菜单驱动参数 |
| `avatar/animator-system.md` | Animator Parameter 来源之一就是菜单 |
| `avatar/modular-avatar.md` | `Full Controller` 组件合并完整 animator/expression menu/parameters |
| `avatar/standard-hand-poses.md` | 控制器按钮唤起 Action Menu 的细节 |
| `avatar/skeletal-input.md` | Hand Tracking 当前不支持 Action Menu |
| `platform/mobile-ui-optimization.md` | Quest 替代 UI 方案 |

---

## 11. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **Widgets 的完整类型列表**（除 Button/Toggle/Stage/Puppet 之外是否还有其他）
2. ❓ **Stages 嵌套 Stages** 是否支持
3. ❓ **菜单打开/关闭** 的精确事件回调（创作者能否在 Udon 中监听）
4. ❓ **Puppet Menu 持续时间**对 Performance Rank 的影响
5. ❓ **Flick 灵敏度** 是否可调
6. ❓ **菜单 Position 记忆** 的具体机制（持久化到哪个文件）
7. ❓ **多 Stage 切换** 是否消耗带宽
8. ❓ **Bindings 自定义** 能否保存到云端

---

## 来源

- [VRChat Action Menu](https://docs.vrchat.com/docs/action-menu)
- [What is Avatars 3.0?](https://docs.vrchat.com/docs/what-is-avatars-30)
- 本地化版本: `参考文献/SP/user-guide/action-menu.md`
