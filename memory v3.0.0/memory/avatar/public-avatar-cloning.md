---
title: Public Avatar Cloning — 公共 Avatar 克隆
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - ux
  - public

aliases:
  - "Public Avatar Cloning"
  - "Avatar 克隆"
  - "Clone Avatar"

related:
  - avatar/safety-system.md
  - avatar/trust-rank.md
  - avatar/avatar-fallback-system.md

source: https://docs.vrchat.com/docs/public-avatar-cloning
source_type: community
version: 1.1
last_review: 2026-06-30
confidence: High
---

# Public Avatar Cloning — 公共 Avatar 克隆

> 来源: VRChat 官方文档 - Public Avatar Cloning
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **注意**: 玩家侧 UX 文档,非创作者核心。

---

## 1. 概述

**Avatar Cloning** 允许玩家复制其他玩家正在穿的 **Public Avatar** 到自己的 Avatar 列表。

**前提条件**:
- 对方 Avatar 标记为 **Public**
- 对方**启用**了 "Allow Avatar Cloning"

---

## 2. 克隆流程

```
1. 看到某玩家穿的 Avatar(你感兴趣)
2. 打开 Quick Menu
   - Desktop: ESC
   - VR: Menu 按钮
3. 点击该玩家
4. 满足前提条件 → 显示 "Clone Avatar" 按钮
5. 点击 "Clone Avatar"
6. 你自动切换到该 Avatar
```

---

## 3. 防止被克隆的两种方法

### 3.1 禁用 Allow Avatar Cloning

**路径**: VRChat Settings → Avatar 设置

**效果**:
- 防止**当前 Avatar** 被其他人克隆
- 即使你的 Avatar 是 Public 也有效

**Auto Disable Avatar Cloning**:
- 启用后,离开世界时**自动禁用** Allow Avatar Cloning
- 防止忘记禁用导致持续暴露

### 3.2 设为 Private

**路径**: VRChat 网站 → `vrchat.com/home/avatars` → My Avatars → Make Private

**限制**:
- ⚠️ **只对**自己上传的 Avatar 有效
- 别人的 Avatar 你不能设为 Private

**效果**:
- 你的 Avatar 从 Public 列表移除
- 没人能克隆你的 Avatar

---

## 4. 决策树:何时防止克隆

| 情况 | 建议 |
|------|------|
| 想让别人克隆你的 Avatar | 保持 Public + 启用 Allow Avatar Cloning |
| 仅自己使用 | 设 Private |
| 临时不让克隆 | 禁用 Allow Avatar Cloning(不取消 Public) |
| 离开世界后自动恢复 | 启用 Auto Disable Avatar Cloning |

---

## 5. 风险与提示

| 风险 | 等级 | 说明 |
|------|------|------|
| **Public + Allow Cloning → 自动克隆** | 🟡 中 | 别人可立即克隆 |
| **跨会话** | 🟢 低 | 一次克隆永久在你的 Avatar 列表 |
| **不能选择性阻止** | 🟡 中 | 不能只对某些人禁用克隆 |
| **Auto Disable 需手动启用** | 🟢 低 | 默认关闭,需用户主动启用 |

---

## 6. 创作者角度

虽然这是玩家 UX 文档,但创作者应知道:

- **Public Avatar 默认可被克隆**(除非作者禁用)
- **别人克隆你的 Avatar** 不会通知你
- 如果你**不希望**你的 Avatar 被克隆:
  - 设 Private(彻底)
  - 或禁用 Allow Avatar Cloning(临时)

---

## 7. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/public-avatar-cloning
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)
