---
title: VRChat Safety System — 玩家安全系统
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - safety
  - shield-level
  - shader-blocking
  - moderation
  - content-control

aliases:
  - Safety System
  - 安全系统
  - Shield Level
  - 盾牌等级
  - Shader Blocking
  - Custom Animations

related:
  - avatar/trust-rank.md
  - avatar/performance-rank.md
  - world/udon/udon-moderation-tool-guidelines.md
  - avatar/shader/orl/shader-list.md
  - platform/mobile-ui-optimization.md

source: docs.vrchat.com/docs/vrchat-safety-and-trust-system
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Safety System — 玩家安全系统

> 来源: https://docs.vrchat.com/docs/vrchat-safety-and-trust-system
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方玩家系统)
> 关联: `avatar/trust-rank.md` (Trust Rank 决定 Safety 默认行为)

---

## 概述

**Safety System** 是 Trust and Safety 系统的两大组件之一。它让玩家**控制如何处理**其他 Trust Rank 用户的 Avatar 特性。

> **🔴 关键事实**: Safety 系统是**玩家级**控制（不是创建者级），但**创建者必须知道**：
> - 自己的 Avatar 特性可能被屏蔽
> - 哪些 Shader 会被替换为 Standard
> - 哪些动画/粒子/灯光会被禁用

---

## 1. 4 种 Shield Level

> [FACT] Safety 菜单顶部有 4 个预设 "Shield Levels"，覆盖大部分用户需求。

| Shield Level | 行为 | 适用场景 |
|--------------|------|----------|
| **Maximum** | 最严 | 想要最安静环境的用户 |
| **Normal** | 默认 | 推荐（大多数用户）|
| **None** | 几乎全开 | 完全信任房间内所有人 |
| **Custom** | 自定义 | 精细控制每个特性 |

> [FACT] **Custom 模式是特殊模式** — 你可以完全自定义每个特性的开/关状态。

### 1.1 Normal 默认设置

> [FACT] 系统设计为:**Normal 模式对大多数用户即可正常工作**，无需自定义。
>
> 大多数用户**应该**保留 Normal 模式。

### 1.2 行为详解

#### Maximum
- 默认隐藏所有非好友的 Avatar 特性

#### None
- 几乎所有特性对**所有 Trust Rank 开放**
- **创作者注意**: 大多数玩家**不会**用此设置（除非完全信任房间）

#### Custom
- 玩家可针对**每个 Trust Rank 单独配置**每个特性

> [FACT] 即使 Shield Level 设为 None，**Nuisance 用户仍会被屏蔽**（除非玩家显式解除）。

---

## 2. 8 大 Safety 元素

> [FACT] Safety 系统控制 8 大 Avatar 特性类型。每种特性可以独立开关。

| # | 元素 | 描述 | 创作者影响 |
|---|------|------|------------|
| 1 | **Voice** | 麦克风语音 | 无关 |
| 2 | **Avatar** | 隐藏整个 Avatar（显示 "muted" 头像）| ⚠️ 高 |
| 3 | **User Icon and Emoji** | 用户头像和自定义 Emoji | ⚠️ 中（隐藏时马赛克） |
| 4 | **Audio** | Avatar 音效（非麦克风）| ⚠️ 高 |
| 5 | **Lights and Particles** | 光源 + 粒子 + **Line/Trail Renderer** | ⚠️ 高 |
| 6 | **Shaders** | **所有 Shader 替换为 Standard** | ⚠️ **极高** ⭐ |
| 7 | **Custom Animations** | 自定义动画 | ⚠️ 高 |
| 8 | **Animated Emoji** | 动画表情 | ⚠️ 中 |

### 2.1 Shader 替换行为 ⭐

> [FACT] **当 Shaders 被禁用时，用户 Avatar 上的所有 Shader 都被替换为 Standard Shader。**
>
> 详细技术规范见 [Shader Fallback System](https://creators.vrchat.com/avatars/shader-fallback-system/) 创作者文档。

**创作者影响**:
- lilToon / SCSS / UnlitWF / ORL 等高级 Shader 都会**回退到 Standard**
- 视觉效果**大幅下降**（无 PBR、无 Toon 阴影、无 Fur、无 Matcap）
- 玩家**仍能看到 Avatar**，但**不会**看到精心设计的视觉效果

**应对策略**:
- 在 Standard Shader 上**保持 Avatar 基础外观**（基础颜色、简单阴影）
- 不要依赖**任何非 Standard Shader 特性**作为 Avatar 识别标志
- 测试: 自己在 Safety 设置中关闭 Shaders 看 Avatar 表现

### 2.2 Line/Trail Renderer 被禁用

> [FACT] **Lights and Particles 禁用时，Line Renderer 和 Trail Renderer 也会被禁用。**
>
> 创作者使用 Trail Renderer 做武器特效/魔法光环时需要注意。

### 2.3 Avatar 元素被禁用

> [FACT] **Avatar 元素被禁用时，Avatar 整个被隐藏**（替换为 "muted" 占位），**所有 Avatar 特性同时被禁用**。

---

## 3. Shield Level 切换行为

### 3.1 顶部按钮（Shield Levels Bar）

> [FACT] 4 个按钮从左到右: **Maximum / Normal / None / Custom**

### 3.2 中间设置区

> [FACT] 选中 Shield Level 后，中间区域显示**当前 Shield Level 的设置**。
>
> 在 Custom 模式下，可以**切换每个特性**的开/关。

### 3.3 底部 Trust Ranks 列表

> [FACT] 底部是**每个 Trust Rank 的列表**。
>
> 选中 Rank 后，中间设置区显示**该 Rank 的当前设置**。

### 3.4 Tooltip 区域

> [FACT] UI 元素有 tooltip 功能：
> - **蓝色区域文字**：随选择的 Mode 变化
> - **底部文字**：指向 UI 元素时显示帮助

---

## 4. 单用户覆盖（Hiding/Showing Specific Users）

> [FACT] 玩家可以**对特定用户**覆盖 Safety 设置。
>
> 覆盖方法:
> 1. 在 Social Quick Menu 中选择该用户
> 2. 点击 "Hide Avatar" / "Show Avatar" / "Use Safety Settings"

| 操作 | 效果 |
|------|------|
| **Hide Avatar** | 该用户 Avatar 立即隐藏，**所有特性同时禁用**（除语音）|
| **Show Avatar** | 该用户 Avatar 立即显示，**所有特性同时启用** |
| **Use Safety Settings** | 恢复 Safety System 控制 |

> [FACT] **Hide Avatar 不影响语音** — 玩家仍能听到该用户说话。

> [FACT] **Friends 在 Normal 模式下不会被任何特性隐藏**。
>
> 如果想屏蔽好友的 Avatar 特性，可以**显式**使用 Hide Avatar。

---

## 5. Safe Mode（紧急屏蔽）

> [FACT] **Safe Mode** 是**紧急快捷键**，立即**禁用所有用户的所有特性**。

| 平台 | 快捷键 |
|------|--------|
| **桌面** | `Shift + Esc` |
| **VR** | 双 Trigger + 双 Menu 按钮 |

> [FACT] **Safe Mode 启用时**:
> 1. Safety 切换到 **Custom** 模式
> 2. **所有 Rank 的所有特性被关闭**
> 3. 屏幕中央显示说明文字
> 4. ⚠️ **会覆盖你之前的 Custom 设置**

> [FACT] **Safe Mode 不会自动撤销** — 需要手动恢复 Safety 到原模式。
>
> 如果之前用 Custom 模式，需要**手动重新配置**。

---

## 6. Instance Moderator Actions（实例版主操作）

> [FACT] 当你是 **Instance Owner** 或 **Group Instance** 的 Owner/Moderator/Admin 时，Quick Menu 出现 "Instance Moderator Actions"。

| 操作 | 效果 |
|------|------|
| **Warn User** | 向用户发送警告消息 |
| **Kick User** | 将用户踢出实例，**1 小时内不能加入** |
| **Force Mic Off** | 静音玩家麦克风（玩家可自由解除）|
| **Ban From Group** | 群组实例中**封禁**该用户（不能加入该群组的实例或该群组）|

> [FACT] **这些操作通过 VRChat 平台执行**，不是 Udon 自定义实现。

> 创作者角度：Udon 工具必须**不绕过**这些平台行为。详见 `world/udon/udon-moderation-tool-guidelines.md`

---

## 7. Quick Menu "Scanning Mode"（扫描模式）

> [FACT] 打开 Quick Menu 时，Nameplate 显示**更多信息**（Trust Rank 等）。
>
> - 指向用户 → 显示**快速信息**
> - 点击用户 → **Social Quick Menu**（完整信息）

### 7.1 Interacting with a User

> [FACT] 在 Social Quick Menu 中可执行:
> - 发送好友请求
> - 静音/取消静音用户语音
> - Hide/Show/Use Safety Settings
> - 查看 Avatar 详情
> - 屏蔽/取消屏蔽用户

### 7.2 翻页

> [FACT] **"<" / ">"** 按钮：滚动浏览**实例中所有用户**。
>
> 用途: 检查你屏蔽/静音/加好友的所有用户。

### 7.3 Nameplate 显示

> [FACT] **Nameplate 文字位置**:
> - **左上方**: **Trust Rank**（如 "Trusted User"）
> - **右上方**: **Avatar Performance Rank**（如 "Excellent"）
>
> **关键行为**:
> - Trust Rank 文字**仅在 Quick Menu 打开时**显示
> - 玩家可在 Settings → User Interface → Nameplate 中调整显示
> - 也可在 Radial Menu → Options → Nameplates 中调整
>
> **设计意图**: Trust Rank **默认隐藏**避免干扰体验；Performance Rank **持续显示**（"out of the way during normal play"）

---

## 8. 创作者适配指南

### 8.1 必须考虑 Safety 的场景

| 场景 | 创建者必须考虑 |
|------|---------------|
| **Avatar Shader 选择** | Shader 被屏蔽时降级到 Standard |
| **Avatar 灯光/粒子** | 数量受 Lights and Particles 控制 |
| **Avatar Trail/Line Renderer** | 受 Lights and Particles 控制 |
| **Avatar 音效** | 受 Audio 控制 |
| **Avatar 动画** | 受 Custom Animations 控制 |

### 8.2 屏蔽测试方法（自己测试）

> 创作者可以**自己测试** Avatar 在 Safety 屏蔽下的表现:
> 1. 让自己成为**另一个客户端**（Profile）
> 2. 设置 Safety → Custom → Shaders OFF
> 3. 进入世界看自己的 Avatar 表现

### 8.3 Fallback Avatar 策略

> [FACT] **Fallback Avatar**（备用 Avatar）是当用户的 Avatar 被屏蔽时**显示的替代 Avatar**。
>
> - 用户必须**显式设置** Fallback Avatar
> - Fallback 通常是**轻量、简单**的 Avatar
> - **Impostor** 是另一种替代: 由 VRChat 自动生成的**低精度静态模型**

详细 Impostor/Fallback 区别见 `avatar/impostor-fallback.md`

---

## 9. Safety 系统与其他文档的关系

| 文档 | 关系 |
|------|------|
| `avatar/trust-rank.md` | Trust Rank 决定 Safety 默认行为 |
| `avatar/performance-rank.md` | Avatar 性能等级（Nameplate 右） |
| `world/udon/udon-moderation-tool-guidelines.md` | Udon 工具不绕过 Safety 平台规则 |
| `avatar/shader/orl/shader-list.md` | Shader Fallback 选项影响 Safety 行为 |
| `platform/mobile-ui-optimization.md` | 移动端 UI 设计受 Safety 影响 |

---

## 10. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **Maximum Shield Level 的具体默认设置**（与 Normal 差异）
2. ❓ **Safe Mode 关闭后如何恢复**（Custom 设置是否会保留备份）
3. ❓ **Instance Moderator Actions** 的 API 限制（同一实例可踢出多少用户）
4. ❓ **Ban From Group** 的具体范围（仅限 Group Instance 还是所有该群组内容）
5. ❓ **Animated Emoji** 与普通 Emoji 的精确区分
6. ❓ Shader 替换为 Standard 时**是否包括 Particles 使用的 Shader**
7. ❓ **Nuisance 标签**与 Safety None 模式的交互

---

## 来源

- [VRChat Safety and Trust System](https://docs.vrchat.com/docs/vrchat-safety-and-trust-system)
- [Shader Fallback System (创作者)](https://creators.vrchat.com/avatars/shader-fallback-system/)
- [VRChat Avatar Performance Ranking](https://creators.vrchat.com/avatars/avatar-performance-ranking-system/)
- 本地化版本: `参考文献/SP/user-guide/vrchat-safety-and-trust-system.md`
