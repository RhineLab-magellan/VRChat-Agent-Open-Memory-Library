---
title: Avatar Fallback System — Avatar 降级显示系统
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - performance
  - platform

aliases:
  - "Avatar Fallback System"
  - "Fallback Avatar"
  - "Avatar 降级系统"
  - "Fallback 角色"

related:
  - "avatar/performance-rank.md"
  - "avatar/thry-avatar-evaluator-metrics.md"
  - "avatar/optimization-guide.md"
  - "platform/cross-platform-content.md"
  - "platform/android-development.md"

source: https://docs.vrchat.com/docs/avatar-fallback-system
source_type: community
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Avatar Fallback System — Avatar 降级显示系统

> 来源: VRChat 官方文档 - Avatar Fallback System
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **关键 Insight**: Fallback 是**用户视角**的降级机制 — 当看到其他玩家显示为"灰色机器人"占位时,实际看到的可能是其 Fallback Avatar。

---

## 1. 概述

**Fallback Avatar** 是 VRChat 在以下情况下替代其他玩家 Avatar 显示的简单、高性能 Avatar:
- 平台不兼容（PC vs Quest）
- 性能等级超出用户设置
- Avatar 文件大小超限
- 加载错误

Fallback 必须是**全平台构建**的简单 Avatar,Good 性能等级起步。

---

## 2. Fallback 触发原因（5 种 + 1 变体）

打开 Quick Menu 看其他玩家的 **nameplate**(铭牌),根据图标判断 Fallback 原因:

| # | 原因 | 图标 | 触发条件 |
|---|------|------|---------|
| 1 | **Performance Blocked** | 🔵 蓝色 feather-light + 内嵌性能等级 | 对方 Avatar 超过你设置的 Minimum Performance Rank |
| 2 | **File Size Blocked** | 🔵 蓝色 feather | 对方 Avatar 超过 Maximum Allowed Avatar Filesize |
| 3 | **Missing Asset** | 🔵 蓝色 feather | 对方 Avatar 没有你平台的版本(Windows vs Android) |
| 4 | **Error** | 🔵 蓝色 feather | 加载/初始化错误(尝试 hide+show 重试) |
| 5 | **Safety Blocked / Manually Hidden / Loading** | ⚪ **无**蓝色 feather(特殊图标) | Safety 屏蔽 / 你手动隐藏 / 仍在加载 |

### 关键判断点

- **有**蓝色 feather 图标 → Fallback Avatar 显示中
- **无**蓝色 feather → 仍可能是灰色机器人,但原因不是 Fallback

---

## 3. 各原因详解

### 3.1 Performance Blocked

- **原因**: 对方 Avatar 性能等级超过你设置的 Minimum Displayed Performance Rank
- **可解决**:
  - 你可以点 **"Show Avatar"** 强制显示(代价:帧数下降)
  - 对方创作者:优化 Avatar
- **参考**: `memory/avatar/performance-rank.md`

### 3.2 File Size Blocked

- **原因**: 对方 Avatar 文件大小超过你设置的 Maximum Allowed Avatar Filesize
- **关键概念区分** ⚠️:
  > **文件大小 ≠ 内存使用**(文件大小是下载体积,内存使用是运行时 VRAM)
  > 两者可能相关但不是同一件事

### 3.3 Missing Asset

- **原因**: 平台不兼容(最常见场景)
  - Jim(Windows PC)穿了只有 PC 版本的 Avatar
  - Naomi(Quest)看不到这个 Avatar → 显示 Fallback
- **可解决**:
  - Jim 可以在菜单选择 Fallback Avatar(给 Quest 用户看的)
  - Jim 创作者应该上传 PC + Android 双版本

### 3.4 Error

- **原因**: 加载或初始化错误
- **可解决**: 在 Quick Menu 中 hide + show 重试

### 3.5 Blocked via Safety / Manually Hidden / Loading

- **无蓝色 feather 图标**(特殊情形)
- **Safety Blocked**: VRChat Safety and Trust System 屏蔽(你配置不显示某 Trust Rank 的 Avatar)
- **Manually Hidden**: 你点过 Quick Menu 的 "Hide Avatar" 按钮
- **Loading**: Avatar 正在下载或初始化(下载条满 + 初始化慢 = 复杂 Avatar)

---

## 4. 自定义 Fallback 上传流程

### 4.1 硬性要求清单

你的 Fallback Avatar 必须:

- ✅ **所有平台都已构建**(目前 Windows + Android/Quest)
- ✅ **各平台 Performance Rank ≥ Good**(Quest 端更严格)
- ✅ **Fallback 标志从 Android 上传中设置**
- ⚠️ 上传不合规的 PC 版本会**清除** Fallback 标志

### 4.2 上传步骤

```
1. 创建 Fallback Avatar
   - PC + Android 都需 Good 或 Excellent
   - 推荐:先做 Android 版本(更严格)

2. 用 Android/Quest 平台 Unity 项目
   - 设置好 VRCSDK
   - 上传 → 注意上传对话框中 "Define as Fallback" 复选框
   - 勾选

3. 立即切换到 Windows 平台
   - 同一 Unity 项目
   - 可选:用更宽松的 PC 版本(Good 即可)
   - 上传到同一 Blueprint ID

4. 完成!该 Avatar 即可作为你的 Fallback 选择
```

### 4.3 Grandfathered Fallback(2021-09-01 之前)

- 不强制要求 PC + Android 双版本
- 缺 Windows asset → 显示为随机色机器人 + 缩略图
- 缺 PC asset → Windows 用户看到 "Perf Blocked" 机器人

---

## 5. 选择与管理 Fallback

### 5.1 默认 Fallback

- VRChat **随机**从 Featured Public 选一个作为你的初始 Fallback

### 5.2 切换 Fallback

- Avatar 菜单 → 右上角按钮 → "Choose Fallback"
- 切换选项:
  - 多数 Featured Public Avatar 都可用
  - 你自己的 Avatar(满足要求)
- 操作:
  - "Switch PC" → 切换回 PC 视图
  - "Change into Avatars" → 确认选择

### 5.3 Picture-in-Picture 预览

- Avatar 菜单中显示所选 Avatar 的画中画预览

### 5.4 隐藏 Fallback UI

- 点 "Hide Fallback" 按钮(左上角)→ UI 收起

---

## 6. 重要 FAQ

### Q: 能把 Fallback 设为 Public 让别人用吗?

**❌ 不能。** Fallback 只能你自己用。

### Q: 能用喜欢的 Avatar 作 Fallback 吗?

**❌ 不能。** 必须自己上传并设置标志。

### Q: 我 Avatar 上传时 Good,Perf Filter 后变 Excellent,为什么不能用?

- Fallback 必须以 **SDK 上传时的等级**为准
- Perf Filter 的事后优化**不算**

### Q: PC 端不达标,但 Quest 端达标,我勾选了 Fallback 标志,能骗过系统吗?

**❌ 不能。** PC 端会显示为 Perf Blocked 机器人(作弊失败)。

### Q: 我穿非人形 Avatar,但 Fallback 是人形,会怎样?

- Fallback **没有 IK**
- 你的手臂腿不会动
- 没有姿势信息可显示

### Q: Fallback 与当前 Avatar 比例差异大(2m vs 1m),会怎样?

- VRChat **会做缩放**让尺寸合理匹配
- 限制宽松但有上限

### Q: 双方都是人形但比例差异大,会怎样?

- 系统尽力匹配动作
- 极端比例可能产生不良结果
- 建议 Fallback 与当前 Avatar 比例相近

### Q: 点 "Show Avatar" 后 Fallback 仍然显示,为什么?

- **如果对方没有你平台的版本** → 仍然只能看到 Fallback(无内容可显示)
- **如果对方超过 Minimum Performance Rank** → 点 "Show Avatar" 后会显示原 Avatar(你接受帧数代价)

---

## 7. 工程实践要点(创作者)

### 7.1 Fallback 设计原则

| 原则 | 说明 |
|------|------|
| **简洁优先** | Fallback 性能门槛最低,别加无意义功能 |
| **比例匹配** | Fallback 比例接近主 Avatar,缩放体验好 |
| **IK 友好** | 选 Humanoid Fallback(对方用 Generic 时你的 IK 才正常) |
| **风格中立** | 通用 Fallback 比角色特定 Fallback 更实用 |

### 7.2 与平台要求配合

- **Quest 端**: 必须达到 Good 或 Excellent(更严)
- **PC 端**: Good 即可(较宽松)
- **跨平台**: 利用 PC 更宽松做 PC-only 增强,然后 Quest Fallback 提供基础

### 7.3 常见失败模式

| 失败 | 原因 | 修复 |
|------|------|------|
| 标志消失 | 上传不达标 PC 版本 | 重新上传合规版本并勾选 |
| 对方看不到我的 Fallback | 没设标志 | 上传时勾选 "Define as Fallback" |
| 仍显示 "Perf Blocked" 机器人 | Fallback 不满足等级 | 优化至 Good/Excellent |

---

## 8. 相关文档

- `memory/avatar/performance-rank.md` — Performance Rank 标准
- `memory/avatar/thry-avatar-evaluator-metrics.md` — 7 项检测指标
- `memory/avatar/optimization-guide.md` — 优化实操
- `memory/platform/cross-platform-content.md` — 跨平台开发
- `memory/platform/android-development.md` — Quest 端要求
- `memory/platform/easyquestswitch.md` — PC/Quest 切换工具

---

## 9. 风险与陷阱

| 风险 | 等级 | 说明 |
|------|------|------|
| **标志被清** | 🔴 高 | 上传不合规 PC 版本会清掉 Fallback 标志 |
| **Quest 端不达标** | 🔴 高 | Android/Quest Fallback 必须 Good+,比 PC 严格 |
| **非人形 + 人形 Fallback** | 🟡 中 | 失去 IK,动作不自然 |
| **比例差异** | 🟢 低 | 系统会缩放但极端情况效果差 |
| **文件大小 ≠ VRAM** | 🟡 中 | 创作者需理解两者区别,不要混淆 |
| **公开 Fallback 不可能** | 🟢 低 | 设计限制,无解 |

---

## 10. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/avatar-fallback-system
- **官方版本更新**: 2021-09-01(Grandfathered 截止)
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)
