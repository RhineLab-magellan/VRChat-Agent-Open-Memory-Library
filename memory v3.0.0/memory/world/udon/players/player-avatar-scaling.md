---
title: "Player Avatar Scaling — Avatar 缩放系统"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/udon/players/player-avatar-scaling/ (Last updated: 2023-07-28)"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - event
  - avatar
aliases:
  - "Player Avatar Scaling — Avatar 缩放系统"
  - player-avatar-scaling
related:
  - player-audio.md
  - player-positions.md
  - getting-players.md
  - player-collisions.md
  - player-forces.md
---
# Player Avatar Scaling — Avatar 缩放系统

> Domain: World / Udon / Players
> Subtype: API 详解
> 底层引用: `memory/api/player-api.md`
> 抓取日期: 2026-06-15

---

## 概述

Udon 提供 Avatar 缩放能力,允许世界创作者:
- **允许/强制** Avatar 缩放功能和参数
- **响应** 玩家身高变化事件

相关事件(`OnAvatarChanged`、`OnAvatarEyeHeightChanged`)见 [Avatar Events](https://creators.vrchat.com/worlds/udon/avatar-events/)。

---

## ⚠️ 关键约束: 缩放不影响碰撞

> **缩放 Avatar 不会改变其与环境的碰撞**,就像在 Unity 中缩放一个 Avatar 再上传也不会改变碰撞一样。

---

## 两种工作模式

Avatar 缩放有**两种模式**,可在玩家级别独立调整:

### 1. Player-Controlled 模式 (玩家控制)
- 玩家可通过 Action Menu 中的**径向菜单**或 Quick Menu 中的 **"Match Eye Height" 按钮**调整自己的身高
- **当前为默认模式**

#### 1.1 玩家侧操作流程(2026-06-30 更新,源自官方 docs)

**Avatar Height 拨盘(自己)**:
- VR: 按 B → Expressions → Quick Actions → Avatar Height 拨盘
- Desktop: 按 R → Expressions → Quick Actions → Avatar Height 拨盘

**Match Eye Height(匹配对方眼高)**:
- VR: 按 B → 用 Trigger 指向并点击其他用户 → 在其 **Profile Page** 中滚动找到 "Match Eye Height"
- Desktop: 按住 Shift 用鼠标 → 左键点击其他用户 → 在其 **Profile Page** 中滚动找到 "Match Eye Height"

> ⚠️ **关键澄清**:"Match Eye Height" 按钮**不在**本地玩家的 Quick Menu 中,而在**目标玩家**的 Profile Page 中(需要先点选对方玩家)

### 2. World-Authoritative 模式 (世界权威)
- 玩家无法自行调整,只能由世界中的 Udon 程序控制
- 玩家菜单中的缩放选项被禁用

无论哪种模式,Avatar/眼高变化都会触发 `OnAvatarChanged` 和 `OnAvatarEyeHeightChanged` 事件。

---

## 模式切换方式

### 方式 A: 通过网站禁用 (彻底关闭)

登录 [VRChat Website](https://vrchat.com/home/content/worlds) → My Worlds → 选择世界 → 关闭 Avatar Scaling → 保存

**效果**:
- 系统对世界中的玩家**完全禁用**
- 玩家只能使用**默认尺寸**
- 菜单中的 Avatar 缩放组件也被禁用
- ⚠️ **以下 Udon 函数变为无效**(调用无效果):
  - `SetManualAvatarScalingAllowed`
  - `SetAvatarEyeHeightMinimumByMeters`
  - `SetAvatarEyeHeightMaximumByMeters`
  - `SetAvatarEyeHeightByMeters`
  - `SetAvatarEyeHeightByMultiplier`

### 方式 B: 保留函数能力,仅关闭玩家控制

**保留** 网站设置中的 Avatar Scaling 启用,改用 Udon 调用 `SetManualAvatarScalingAllowed(false)` 切换到世界权威模式。

---

## 玩家控制模式函数 (Player-Controlled Scaling)

> ⚠️ **Local player only**: 以下函数(除特别说明外)**仅对本地玩家**有效,不能在其他玩家的 `VRCPlayerApi` 上调用。

### GetManualAvatarScalingAllowed

- **返回**: `bool`
- **说明**: 检查本地玩家是否被允许控制自己的 Avatar 缩放
- **`true`**: Player-Controlled 模式
- **`false`**: World-Authoritative 模式

### SetManualAvatarScalingAllowed

- **输入**: `bool`
- **`true`**: 切换到 Player-Controlled 模式
- **`false`**: 切换到 World-Authoritative 模式

### GetAvatarEyeHeightMinimumAsMeters

- **返回**: `float` (米)
- **范围**: `>= 0.2` 米
- **说明**: 返回本地玩家在 Player-Controlled 模式下允许的**最小眼高**

### SetAvatarEyeHeightMinimumByMeters

- **输入**: `float` (米)
- **约束**: `>= 0.2` 米
- **说明**: 设置本地玩家在 Player-Controlled 模式下允许的**最小眼高**

### GetAvatarEyeHeightMaximumAsMeters

- **返回**: `float` (米)
- **范围**: `<= 5` 米
- **说明**: 返回本地玩家在 Player-Controlled 模式下允许的**最大眼高**

### SetAvatarEyeHeightMaximumByMeters

- **输入**: `float` (米)
- **约束**: `<= 5` 米
- **说明**: 设置本地玩家在 Player-Controlled 模式下允许的**最大眼高**

---

## 世界权威模式函数 (World-Authoritative Scaling)

> ⚠️ **Local player only**: 以下函数(除特别说明外)**仅对本地玩家**有效。

### GetAvatarEyeHeightAsMeters

- **返回**: `float` (米)
- **说明**: 返回**目标玩家** Avatar 的**当前配置眼高**
- **差异** ⭐: **该函数对本地玩家和远程玩家都有效**(其他函数通常仅对本地玩家有效)
- **用途**: 跨玩家同步缩放状态时使用

### SetAvatarEyeHeightByMeters

- **输入**: `float` (米)
- **说明**: 设置当前玩家 Avatar 的眼高(米)

### SetAvatarEyeHeightByMultiplier

- **输入**: `float` (倍率)
- **说明**: 设置眼高为**目标玩家 Avatar 在预制体尺度下的眼高**的指定倍率
- **示例**: `1.0` = 原始眼高, `0.5` = 缩小到一半, `2.0` = 放大一倍

---

## 与任务规格的差异说明

> ⚠️ **任务提示中提到的 `SetAvatarScale(0.4-1.4)` 与当前官方 API 不一致**:
>
> - **任务规格**: `SetAvatarScale(float scale)` 限制 0.4-1.4
> - **当前官方 API**: 已重构为 **EyeHeight 系统** (`SetAvatarEyeHeightByMeters` / `SetAvatarEyeHeightByMultiplier`),范围 0.2-5 米
>
> 这是 SDK 演进的结果 — 旧版 `SetAvatarScale` 已被弃用/替换,新 API 基于**眼高(米)**而非**缩放倍率**。`SetAvatarScale` 在当前 Creator Docs 已**不再列出**。
>
> 建议查阅本地 Unity 工程中实际 SDK 版本暴露的 API,可能仍存在旧版 API(向后兼容)。

---

## 典型场景配方

### 1. 进入世界时锁定为世界权威模式

```csharp
public override void OnPlayerJoined(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        // 切换到世界权威模式
        player.SetManualAvatarScalingAllowed(false);
        
        // 限制缩放范围 (虽在此模式下不直接生效,作为防御)
        player.SetAvatarEyeHeightMinimumByMeters(0.5f);
        player.SetAvatarEyeHeightMaximumByMeters(3.0f);
    }
}
```

### 2. 根据剧情设置玩家眼高

```csharp
// 设定本地玩家眼高为 1.0 米(小人国)
localPlayer.SetAvatarEyeHeightByMeters(1.0f);

// 或者用倍率 — 原始眼高的 0.5 倍
localPlayer.SetAvatarEyeHeightByMultiplier(0.5f);
```

### 3. 响应 Avatar 变化事件

```csharp
// 见 avatar-events.md
public override void OnAvatarEyeHeightChanged(VRCPlayerApi player, float eyeHeight)
{
    Debug.Log($"{player.displayName} new eye height: {eyeHeight}m");
    
    // 例如: 调整相机距离、调整 UI 大小等
    followCamera.transform.localPosition = new Vector3(0, eyeHeight + 0.2f, 0);
}
```

---

## 关键参数范围速查

| 模式 | API | 范围 |
|---|---|---|
| Player-Controlled | `SetAvatarEyeHeightMinimumByMeters` | `>= 0.2` 米 |
| Player-Controlled | `SetAvatarEyeHeightMaximumByMeters` | `<= 5` 米 |
| World-Authoritative | `SetAvatarEyeHeightByMeters` | 0.2 - 5 米 (建议) |
| World-Authoritative | `SetAvatarEyeHeightByMultiplier` | 0.1 - 2.0 (经验值) |
| (已废弃) | `SetAvatarScale` | 0.4 - 1.4 (旧版) |

---

## 与底层 API 的对照

| 本文件 API | 底层 `player-api.md` 摘要 |
|---|---|
| `GetAvatarEyeHeightAsMeters` | 有(简要说明) |
| `GetAvatarScale` | ❌ 旧 API,新文档不再列出 |
| `SetAvatarScale` | ❌ 旧 API,新文档不再列出 (范围 0.4-1.4 来自旧 SDK) |
| `SetManualAvatarScalingAllowed` | 新增于本文件 |
| `SetAvatarEyeHeightMinimumByMeters/Maximum` | 新增于本文件 |
| `SetAvatarEyeHeightByMultiplier` | 新增于本文件 |

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **缩放不影响碰撞** | ⚠️ 缩放后的 Avatar 仍以原始碰撞体与世界交互,可能导致视觉错位 |
| **网站禁用时函数无效** | 若网站彻底关闭 Avatar Scaling,所有 Set* 函数调用**无效果** |
| **范围硬限制** | `MinimumByMeters` < 0.2 或 `MaximumByMeters` > 5 米的值会被拒绝 |
| **本地玩家限制** | 大部分函数仅本地玩家可用,远程玩家调用无效 |
| **跨玩家状态查询** | 只有 `GetAvatarEyeHeightAsMeters` 对远程玩家有效 |
| **Mode 切换持久性** | `SetManualAvatarScalingAllowed(false)` 设置持续到玩家离开世界 |
| **Quest 性能** | 极大/极小的缩放可能影响 Quest 性能(尤其涉及 PhysBone/Particle 时) |

---

## 与其他知识库的关系

| 知识库 | 关系 |
|---|---|
| `memory/api/player-api.md` | 底层 API 简略版 |
| `memory/api/animator.md` | Avatar 缩放影响 Animator IK 目标(待补充) |
| `memory/avatar/playable-layers.md` | Avatar 端缩放控制(独立于本文件的世界端控制) |
| `memory/world/udon/avatar-events.md` | `OnAvatarChanged` / `OnAvatarEyeHeightChanged` 事件 |
