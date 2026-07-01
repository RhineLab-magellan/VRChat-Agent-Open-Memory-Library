---
title: Avatar Interaction Permissions — Avatar 交互权限设置
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - ux
  - safety
  - permission

aliases:
  - "Avatar Interaction Permissions"
  - "交互权限"
  - "Avatar 互动设置"
  - "PANIC 按钮"

related:
  - "world/scene-components/vrc-scenedescriptor.md"
  - avatar/safety-system.md
  - avatar/trust-rank.md

source: https://docs.vrchat.com/docs/permissions-and-settings
source_type: community
version: 1.1
last_review: 2026-06-30
confidence: High
---

# Avatar Interaction Permissions — Avatar 交互权限设置

> 来源: VRChat 官方文档 - Avatar Interaction Permissions and Settings
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **注意**: 玩家侧 UX 文档,非创作者核心。

---

## 1. 概述

在 Quick Menu 的 **Settings tab**(齿轮图标 tab) 中,可以调整谁能与你的 Avatar 交互。

**核心规则**:
> **双方必须显式允许交互,才能进行交互。**

---

## 2. 三个核心设置

| 设置 | 默认 | 选项/含义 |
|------|------|----------|
| **Mode** | Friends | Friends / Everyone / Nobody |
| **Allow/Pause Interactions** | - | 全局开关,忽略 Mode |
| **Self Interact** | - | 切换与**自己** Avatar 的交互 |

### 2.1 Mode(模式)

定义**谁能**与你交互:

| 选项 | 含义 |
|------|------|
| **Friends** | 仅好友可交互(默认) |
| **Everyone** | 所有人可交互 |
| **Nobody** | 没人可交互 |

### 2.2 Allow/Pause Interactions(全局开关)

- 忽略 Mode 设置
- **全局开启/关闭**所有交互
- 紧急时使用

### 2.3 Self Interact(自我交互)

- 切换与你**自己** Avatar 的交互
- 调试/自拍时使用

---

## 3. 玩家级覆盖

### 3.1 Per-User Override

- 点击 Quick Menu 中的用户
- 可为该用户**单独覆盖**权限设置
- 覆盖**跨会话保存**

### 3.2 Nameplate 图标识别

- **手图标灰色** = 该用户不允许与你交互
- **手图标亮起** = 允许交互

---

## 4. 紧急控制

### 4.1 Pause 按钮

- 立即暂停**所有交互**全局
- 不改变 Safety 设置

### 4.2 PANIC 按钮

- 暂停**所有交互**
- 同时将 Safety Shield 设为 **Maximum** 等级

**使用场景**:
- 恶意骚扰
- 突发不适
- 快速远离骚扰

---

## 5. 玩家 UX 流程

### 5.1 启用某用户交互

```
1. Quick Menu → Settings tab(齿轮)
2. 找到该用户(或点击用户 → Per-User Override)
3. 切换权限为允许
4. 设置自动保存
```

### 5.2 紧急停止

```
1. Quick Menu → Settings tab
2. 按 PANIC 按钮(红色突出按钮)
3. 立即生效:
   - 所有交互停止
   - Safety Shield → Maximum
```

---

## 6. 与 Safety / Trust 系统的关系

| 系统 | 范围 | 文档 |
|------|------|------|
| **Interaction Permissions(本文档)** | 控制 Avatar 交互(手柄互动,Who can interact) | `memory/avatar/avatar-interaction-permissions.md` |
| **Safety System** | 控制看到其他玩家 Avatar 的特性(What you see) | `memory/avatar/safety-system.md` |
| **Trust Rank** | 决定用户上传/可见性 | `memory/avatar/trust-rank.md` |
| **Safe Mode** | 紧急屏蔽**所有**用户所有特性(Shift+Esc) | `memory/avatar/safety-system.md` §5 |
| **PANIC 按钮(本文档)** | 紧急停止交互 + Safety Shield → Maximum | (Quick Menu 中) |

### 关键区别

- **Safety System** 控制 **你看到什么**(是否显示 Shader、Audio 等)
- **Interaction Permissions** 控制 **谁能与你互动**(握手、PhysBone 抓取等)
- 两者**正交**:
  - Safety High + Interaction Everyone: 看到基本 Avatar,任何人都能互动
  - Safety Low + Interaction Nobody: 看到完整 Avatar,但没人能互动

---

## 7. 风险与提示

| 风险 | 等级 | 说明 |
|------|------|------|
| **默认 Friends** | 🟡 中 | 公共场合可能限制交互 |
| **PANIC 不可逆(无确认)** | 🟡 中 | 按下立即生效,需手动恢复 |
| **跨会话保存** | 🟢 低 | 一次设置长期生效,可能遗忘 |
| **Nobody 模式** | 🟢 低 | 极端设置,可能影响正常使用 |

---

## 8. 创作者角度

虽然这是玩家 UX 文档,但创作者应知道:

- Avatar 交互相关**菜单**(Radial Menu)在 Friends 模式下仅对好友可见
- 交互内容(PhysBone 等)受全局 Pause 影响
- 设计 Avatar 时考虑"No Body"模式下的体验

---

## 9. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/permissions-and-settings
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)
