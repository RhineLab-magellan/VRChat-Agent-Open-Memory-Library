---
title: VRCRaycast (Avatar 组件,SDK 3.10.3+)
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - raycast
  - vrc-component
  - performance
  - sdk-3-10

aliases:
  - VRCRaycast
  - "Avatar Raycast"
  - "Avatar 光线投射"

related:
  - ../api/dynamics.md
  - vrc-constraints.md
  - performance-rank.md
  - accessories.md
  - thry-avatar-evaluator-metrics.md

source: VRChat 2026.2.1 / 2026.2.1 Open Beta Release Notes + VRChat Creator Docs
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRCRaycast (Avatar 组件,SDK 3.10.3+)

> **SDK 版本**:3.10.3(2025 末)
> **类型**:Avatar 端组件
> **官方文档**:https://creators.vrchat.com/avatars/avatar-components/raycast
> **作用**:将 Avatar 骨骼上的 raycast 投射到世界中,并写入 Animator 参数

---

## 1. 概述

`VRCRaycast` 是 VRChat 官方 Avatar 组件,允许 Avatar 设计师将**光线投射**绑定到特定骨骼上,并通过 **Animator 参数**反馈结果。典型应用:

- 探测脚下是否有地面(用于踩水效果)
- 检测 Avatar 是否被物体遮挡
- 实现 Avatar 端的世界交互
- 行走状态检测(用于特殊动画过渡)

> **关键设计**:Raycast 结果通过 Animator 参数传递,设计师可在 Animator Controller 中基于参数实现响应式动画。

---

## 2. 核心机制

### 2.1 投射方向

- Raycast 从**指定骨骼位置**出发
- 沿骨骼的**局部方向**(通常是 -Y,即向下)投射
- 长度由 Inspector 配置
- 默认:头骨向下投射

### 2.2 Animator 参数

- Raycast 结果以 **Float 参数** 形式暴露
- 默认参数名:`IsRaycastHit`(可在 Inspector 修改)
- 命中时 = 1.0,未命中 = 0.0
- 在 Animator 中可作为 1D Blend Tree 输入

### 2.3 骨骼配置

支持任意 Avatar 骨骼作为 raycast 源:

| 常用骨骼 | 用途 |
|----------|------|
| `Head` | 头部碰撞/被遮挡检测 |
| `Hips` | 全身位置检测 |
| `LeftFoot` / `RightFoot` | 踩地/踩水检测 |
| `LeftHand` / `RightHand` | 抓握检测 |

---

## 3. 性能与限制 (2026.2.1 重要更新)

### 3.1 自动剥离(2026.2.1+)

> **🔴 关键性能特性**:**当玩家本地屏蔽 Poor / Very Poor 头像,且 VRCRaycast 组件数超过性能阈值时,VRCRaycast 会自动从其他玩家的 Avatar 上剥离**(2026.2.1 引入)。

| 触发条件 | 行为 |
|----------|------|
| 玩家本地设置 = 屏蔽 Poor | 自动剥离 Poor Avatar 上的 VRCRaycast |
| 玩家本地设置 = 屏蔽 Very Poor | 自动剥离 Very Poor Avatar 上的 VRCRaycast |
| 组件数 > 性能阈值 | 即使评级 OK 也可能剥离 |

**效果**:
- 远端玩家看到的 Avatar 不再执行 VRCRaycast
- 远端玩家不会看到基于 raycast 的反应式动画
- 显著降低远端渲染和物理开销

### 3.2 Animator 参数修复(2026.2.1)

> **修复前 bug**:Animator 移动 raycast 时,无实时光照世界中的 Animator 参数错误(可能返回 0 或错值)。

**修复内容**:
- 在无实时光照世界中,Animator 控制的 VRCRaycast 现在返回**正确结果**
- 修复前:`IsRaycastHit` 参数在某些帧返回错误值,导致动画抖动
- 修复后:结果稳定

### 3.3 第一人称头骨处理(2026.2.1)

> **修复前 bug**:头部 VRCRaycast 在头部对第一人称视角隐藏**之后**应用。

**修复内容**:
- 现在 VRCRaycast 在头部隐藏**之前**应用
- 与"其他玩家视角"行为一致(对称)
- 玩家自己戴的 Avatar 与他人看到的 Avatar 行为现在一致

---

## 4. 最佳实践

### 4.1 控制组件数量

- 每个 Avatar **不要超过 3-4 个** VRCRaycast
- 优先使用 `Hips` 单点 + Animator 计算,而不是多个骨骼
- 移除未使用的 VRCRaycast 组件(即使未连线)

### 4.2 阈值设置

- Raycast 长度不要过长(默认 1-2 米足够)
- 远距离检测用 `SphereCast` 类似机制(VRCRaycast 本身是 raycast)
- 避免在远端玩家身上启用大量 raycast(会被自动剥离)

### 4.3 与 Accessories 协同

- Accessories 添加的 mesh **不影响** VRCRaycast
- VRCRaycast 始终基于 Avatar 骨骼,不管 Accessories 是否存在
- 头部的 VRCRaycast 在 Accessories 加载前后行为一致

---

## 5. 与同类方案对比

| 方案 | 类型 | 平台 | 性能 | 数据可见性 |
|------|------|------|------|-----------|
| **VRCRaycast** | Avatar 组件 | 全部 | 自动剥离(2026.2.1+) | Animator 参数(本地玩家) |
| World Udon Raycast | World 脚本 | World | N/A(World 端) | Udon 变量 |
| Avatar PhysBone Collider | 物理碰撞 | 全部 | 计入性能等级 | Collision Event |
| 第三方 Raycast 包(如 VRCFury) | 自定义 | 取决于实现 | 通常无自动剥离 | 自定义 |

> **推荐**:能用 VRCRaycast 解决的,优先用 VRCRaycast(自动剥离是核心优势)。

---

## 6. 已知问题

| 问题 | 版本 | 状态 |
|------|------|------|
| Animator 移动 raycast 时无实时光照世界参数错误 | < 2026.2.1 | ✅ 已修复(2026.2.1 Build 1833) |
| 头部 raycast 第一人称对称性问题 | < 2026.2.1 | ✅ 已修复(2026.2.1 Build 1833) |
| Poor/Very Poor Avatar 远端 raycast 性能 | < 2026.2.1 | ✅ 已修复(2026.2.1 自动剥离) |

---

## 7. 参考资料

- **VRChat Creator Docs**:https://creators.vrchat.com/avatars/avatar-components/raycast
- **VRChat 2026.2.1 Release Notes**(Build 1835)
- **VRChat 2026.2.1 Open Beta Notes**(Build 1833)
- **SDK 3.10.3 Changelog** - 引入 VRCRaycast
- 相关:`memory/api/dynamics.md` (SDK 时间线)
- 相关:`memory/avatar/accessories.md` (与 Accessories 协同)
- 相关:`memory/avatar/performance-rank.md` (性能等级与剥离阈值)

---

**最后更新**:2026-06-30 | **状态**:✅ 知识库收录 | **来源**:VRChat 官方 Release Notes + Creator Docs
