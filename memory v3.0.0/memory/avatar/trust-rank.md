---
title: VRChat Trust Rank — 玩家信任等级系统
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - trust
  - moderation
  - upload-permission
  - content-gating

aliases:
  - Trust Rank
  - 信任等级
  - 信任系统
  - "Trust System"
  - Visitor
  - New User
  - Known User
  - Trusted User
  - Nuisance
  - "Content Gating"

related:
  - avatar/safety-system.md
  - world/udon/udon-moderation-tool-guidelines.md
  - avatar/performance-rank.md
  - avatar/modular-avatar.md

source: docs.vrchat.com/docs/vrchat-safety-and-trust-system
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Trust Rank — 玩家信任等级系统

> 来源: https://docs.vrchat.com/docs/vrchat-safety-and-trust-system
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方玩家系统)
> 关联: `avatar/safety-system.md` (Safety 系统) + `world/udon/udon-moderation-tool-guidelines.md` (Udon 版主工具)

---

## 概述

VRChat **Trust and Safety 系统**是 VRChat 信任机制的扩展。它用于保护用户免受**滋扰行为**（屏幕空间 Shader、响亮声音、麦克风、视觉噪声、恶意粒子）的影响。

该系统包含**两个核心组件**:
- **Trust System**（信任系统）— 决定用户是否被允许上传内容
- **Safety System**（安全系统）— 让用户决定如何处理其他人的 Avatar 特性

> **🔴 关键事实**: Trust 和 Safety 系统**相互独立但联动**。即使 Safety 设为 None，Nuisance 用户的 Avatar 仍会被隐藏。

---

## 1. Trust Rank 完整层级

### 1.1 7 个 Trust Rank

> [FACT] 用户 Trust 决定 Trust Rank，是"用户在 VRChat 中度过的时间、贡献的内容、结交的朋友"等多个变量的**综合指标**。

| Rank | 名称 | 关键权限 | 备注 |
|------|------|----------|------|
| **Visitor** | 访客 | ❌ 无法上传 | 全新账号 |
| **New User** | 新用户 | ✅ **可上传 Avatar/World** | 升级节点 ⭐ |
| **User** | 普通用户 | 标准 | 隐藏 Trust 标志后的显示 |
| **Known User** | 已知用户 | 可隐藏 Trust 标志 | |
| **Trusted User** | 信任用户 | 可隐藏 Trust 标志 | |
| **Nuisance** | 滋扰用户 | ❌ 大多数 Avatar 被屏蔽 | 被举报标记 |
| **VRChat Team** | VRChat 团队 | 不可伪装 | 内部账号 |
| **Friends** | 好友（特殊）| Normal 模式下全特性开放 | 不显示在 Nameplate |

> [FACT] **Friends 是一种特殊 Trust Rank**。在 Normal Shield Level 下，好友的所有 Avatar 特性都开放显示。可以通过 Nameplate 上的 Trust 标志区分。
>
> 玩家可以**像配置其他 Trust Rank 一样**自定义 Friends 的 Safety 设置（不只是 Normal 默认行为）。

### 1.2 关键节点：Visitor → New User

> [FACT] 当 Visitor 升级为 **New User** 时，**获得上传内容的权限**。前提是使用 VRChat 账号（不能是 Steam/Oculus/Viveport 账号）。
>
> 用户升级后会**收到通知**，并被引导至 VRChat 文档以开始创建内容。

**升级行为说明**:
- 简单通过**玩 VRChat**（探索世界、加好友、创建内容）即可增加 Trust
- 当 Trust 达到阈值时自动升级
- 用户**会收到通知**关于 Trust Rank 转换

### 1.3 不会增加 Trust 的行为

> [FACT] 以下行为**不会**增加 Trust:
> - 在世界中**挂机 / 闲置**（AFK）
> - 上传大量**低质量内容**
> - **大量加好友**

### 1.4 隐藏 Trust 标志

> [FACT] **Known User** 及以上等级的 Trust Rank 都可以选择**关闭 Trust 标志**显示。
>
> 关闭后显示为 **"User"**，**同时 Safety 系统对其也按 User 等级处理**（不是按实际等级）。
>
> 这是给不希望显示高 Trust 等级的用户使用的功能。
>
> 默认:
> - **Known** 和 **Trusted** 用户**显示** Trust 标志
> - 切换后显示为 **User**

### 1.5 Nuisance 标签

> [FACT] **Nuisance** 是特殊的 Trust Rank。被标记的用户在打开 Quick Menu 时会在 Nameplate 顶部有**指示符**。
>
> 大多数情况下，这些用户的 **Avatar 会被完全屏蔽**。
>
> **创作者角度**: Nuisance 用户的 Avatar 几乎不会对你的 World 流量产生贡献。

### 1.6 VRChat Team

> [FACT] **VRChat Team** Rank 仅供 VRChat 团队成员使用。
>
> 当 VRChat 团队成员开启 "DEV" 标签时，**在 Quick Menu 中选择该用户**可以看到 "VRChat Team" 标志。
>
> 如果怀疑 "DEV" 标签的用户不是 VRChat 团队成员：
> 1. 打开 Quick Menu
> 2. 选择该用户
> 3. 检查 Trust Rank（Avatar 缩略图下方应显示 "VRChat Team"）
>
> 如果不是，则可能是恶意用户，**建议截图并举报给 Moderation 团队**。

### 1.7 Trust 系统的内部逻辑

> [FACT] **Trust 系统的内部计算方法是有意隐藏的**，以防止被利用。
>
> VRChat 团队表示:
> - 提升 Trust 的**最好方法就是玩 VRChat**
> - 他们可以**根据需要调整**计算方式
> - 详细计算方式**不公开**

---

## 2. 创作者注意：上传权限

### 2.1 上传 Avatar/World 的前提

> [INFERENCE-FROM-setup-2fa] **来源**: `user-guide/setup-2fa.md` + 平台通用知识
>
> 必须满足以下所有条件才能上传内容:
> 1. **Trust Rank ≥ New User**（已升级）
> 2. **使用 VRChat 账号**（不是 Steam/Oculus/Viveport 账号）
> 3. **已完成 SDK 2FA 设置**（开发者账号）

### 2.2 Steam/Oculus/Viveport 账号转换

> [INFERENCE-FROM-setup-2fa] **来源**: `user-guide/setup-2fa.md`（非本节主源 `vrchat-safety-and-trust-system.md`）。此节描述的是 VRChat 平台广为人知的转换流程，但需从 setup-2fa.md 验证。
>
> 如果使用 Steam/Oculus/Viveport 账号登录 VRChat，**无法直接上传内容**。
>
> 转换方法:
> 1. 在 VRChat 内打开 Settings
> 2. 右下角找到**转换按钮**开始流程
> 3. **必须使用空白的新 VRChat 账号**作为转换目标
> 4. ⚠️ **转换后 Steam/Oculus 账号信息不会转移**

> **🔴 重要提示**: 转换前确保**新的 VRChat 账号是空白的**，没有任何收藏或内容。

### 2.3 SDK 2FA

> [FACT] **VRChat 2FA**仅对使用 VRChat 账号登录的用户可用（不适用于 Steam/Oculus/Viveport 账号）。
>
> 设置方法:
> 1. 登录 VRChat 网站
> 2. "Edit Profile" → "Two-Factor Authentication"
> 3. 启用并绑定验证器（推荐 Authy，可云备份）

详细流程见 `user-guide/setup-2fa.md`（未入库 - 玩家层内容）

---

## 3. Trust Rank 升级策略（创作者友好）

### 3.1 快速升级路径

> [FACT] 官方推荐的 Trust 提升方式:
>
> 1. **在新用户阶段积极玩 VRChat**（几天内可达 New User）
> 2. **加真实好友**（不是大量加陌生人）
> 3. **创建高质量 Avatar 和 World**（一旦有权限）
> 4. **避免 AFK 挂机**

### 3.2 创作者路径时间线

| 阶段 | 时间 | 动作 |
|------|------|------|
| **Visitor → New User** | 几小时到几天 | 玩 + 加好友 |
| **New User → Known User** | 几周到几个月 | 创建内容 |
| **Known User → Trusted User** | 持续活跃 | 长期高质量贡献 |

---

## 4. Nameplate 显示规则

> [FACT] **Trust Rank 通常在 Nameplate 上不可见**。
>
> - 默认仅在**打开 Quick Menu** 时显示
> - 可以在 Settings → User Interface → Nameplate 中调整
> - 右上角显示 **Avatar 性能等级**（Performance Rank）

---

## 5. Trust 系统与其他文档的关系

| 文档 | 关系 |
|------|------|
| `avatar/safety-system.md` | Trust Rank 决定 Safety 系统的默认行为 |
| `world/udon/udon-moderation-tool-guidelines.md` | Udon 版主工具基于 Trust 概念 |
| `avatar/performance-rank.md` | Nameplate 同时显示 Trust 和 Performance |
| `vrchatsdk/faq.md` | 简略 FAQ 涵盖 Trust |

---

## 6. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ Trust Rank 升级的**精确阈值**（官方明确说"intentionally hidden"）
2. ❓ **New User 升级需要的具体时间**（几小时到几天，个体差异大）
3. ❓ **Known User → Trusted User** 的具体条件
4. ❓ **Nuisance** 的具体判定标准（官方明确说"intentionally hidden"）
5. ❓ Trust 系统的**反作弊机制**（防止恶意刷 Trust）
6. ❓ **VRChat Team 标志**是否可由用户举报伪造
7. ❓ 多账号 Trust 是否独立计算

---

## 7. 创作者 FAQ

### Q1: 何时可以上传 Avatar/World？
> A: Trust Rank 达到 **New User** 后，使用 VRChat 账号（不是 Steam/Oculus/Viveport）登录，并完成 2FA 设置。

### Q2: Trust Rank 显示在哪里？
> A: 默认仅在打开 Quick Menu 时显示。可在 Settings → Nameplate 调整。

### Q3: 如何让 Trust Rank 快速提升？
> A: 玩 VRChat + 加真实好友 + 创建高质量内容。**不要**挂机或大量加好友。

### Q4: Nuisance 标签会撤销吗？
> A: 官方未明确说明撤销机制。建议保持良好的社交行为。

### Q5: Steam 账号如何上传内容？
> A: 必须先**转换为 VRChat 账号**（在 Settings 找到转换按钮）。⚠️ 转换后不可逆。

---

## 来源

- [VRChat Safety and Trust System](https://docs.vrchat.com/docs/vrchat-safety-and-trust-system)
- [VRChat 2FA Setup](https://docs.vrchat.com/docs/setup-2fa)
- [VRChat User FAQ](https://docs.vrchat.com/docs/frequently-asked-questions)
- 本地化版本: `参考文献/SP/user-guide/vrchat-safety-and-trust-system.md`
