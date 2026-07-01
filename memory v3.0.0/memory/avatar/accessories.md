---
title: VRChat Avatar Accessories 系统 (2026.2.1+)
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - accessories
  - vrc-native
  - googly-eyes
  - 2026

aliases:
  - Accessories
  - "Avatar Accessories"
  - "Avatar 配饰系统"
  - "Googly Eyes"

related:
  - modular-avatar.md
  - vrcfury-reference.md
  - performance-rank.md
  - thry-avatar-evaluator-metrics.md
  - vrcraycast.md
  - index.md

source: VRChat 2026.2.1 / 2026.2.1p1 / 2026.2.1 open-beta Release Notes
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Avatar Accessories 系统 (2026.2.1+)

> **来源**:VRChat 2026.2.1 正式上线,2026.1.3p1 Open Beta 与 2026.2.1 Open Beta 阶段测试
> **域**:Avatar(原生 VRChat 系统,**非** Modular Avatar 组件)
> **定位**:与 MA 的 "Visible Head Accessory" 是完全不同的概念(后者是 MA 的局部功能,前者是 VRChat 原生 Avatar 配饰系统)

---

## 1. 概述

**Avatar Accessories**(Avatar 配饰)允许玩家为自己的 Avatar 添加**可穿戴的虚拟物品**,如:

- 帽子
- 太阳镜
- 光环
- 尾巴
- 猫耳 / Googly Eyes
- 其他装饰性附件

### 核心特征

| 特性 | 说明 |
|------|------|
| **持久性** | 一旦装备,**永久附属于 Avatar**(不像 Items 离开世界就消失) |
| **跨世界** | 在所有世界中保持穿戴状态 |
| **客户端加载** | 在 Looks 或 Accessories 标签页显示加载指示器 |
| **跨平台** | PC / Quest / Android / iOS 全平台支持 |
| **Look 集成** | 可在 Look(Avatar 外观预设)中保存 Accessories 配置 |

---

## 2. 数量限制

### 2.1 单 Avatar 数量限制

| 限制类型 | 数量 | 备注 |
|----------|------|------|
| **每 Avatar 最大** | **5** 个 Accessories | 硬性上限 |

### 2.2 全局渲染限制(远端玩家)

| 平台 | 总渲染上限 | 备注 |
|------|-----------|------|
| **PC** | **240** | 按距离排序,最近的先渲染 |
| **Quest / Android / iOS** | **80** | 移动端严格上限 |

> **优先级规则**:**距离玩家近的优先渲染**。超过上限时,远处的 Avatar 上的 Accessories 不渲染(而非减少单 Avatar 数量)。
>
> **重要**:此限制与单 Avatar 5 个上限**独立**(per-avatar 限制不受全局限制影响)。

---

## 3. Look Editor 行为变更 (2026.1.3p1)

2026.1.3p1 Open Beta 引入的 Look Editor 改进**特别针对 Accessories**:

| 变更点 | 行为 |
|--------|------|
| **"All" 可见性选项** | ❌ **已移除** |
| **保留选项** | 仅 "Human" / "Extra" |
| **进入骨骼重定向模式** | 可见性模式自动匹配当前附着对象的模式 |
| **Gizmo 高亮** | 鼠标悬停时对应 slider 高亮 |
| **Gizmo 悬停距离** | 增大,便于 VR 选择 |
| **旋转 slider 速度** | 减半至 90 度 (FACT:vrchat-202613p1-open-beta.md:28) |
| **颜色选择面板** | 修复选择颜色时的闪烁 |
| **attachable skeleton 计算起点** | Humanoid 从 **Hip 骨**开始(之前的骨骼被跳过) |
| **Root 骨** | 仍包含,现在显示在 "Humanoid" 可见性模式下 |

---

## 4. 已知修复 (2026.2.1p1)

| 问题 | 修复 |
|------|------|
| Accessories 通知每次都出现 | 修复为仅首次出现 |
| Fallback shaders 在带 Accessories 的 Avatar 上崩溃 | 已修复 |
| Accessories 商店 listing 归因文字 | 已修复 |
| 缩放限制外的远程用户警告 | 仅本地显示(不再推送) |
| 本地 nameplate 显示 Muted/Volume 指示器 | 已移除(本端不需要) |
| Animated Emoji 通过 in-game camera 流程创建 | 修复 |
| 移动平台低 RAM 时玩家不可见 | 已修复 |

---

## 5. 性能与最佳实践

### 5.1 对 Avatar Performance Rank 的影响

> **⚠️ 重要**:Accessories 的渲染开销**会计入穿戴它们的 Avatar 的 Performance Rank**。
> 远端玩家的 Accessories **不计入**该玩家的 Performance Rank(因为它们由本地渲染)。

### 5.2 兼容性建议

1. **优先测试 Quest**:Quest 的 80 个全局上限可能更早触发
2. **使用距离排序**:在拥挤实例中,远处的 Accessories 可能不渲染
3. **Look 预设**:为不同场景(日常/活动/演出)保存不同 Accessories 组合
4. **避免 Accessories 循环依赖**:不要让一个 Accessory 引用同一 Avatar 的其他 Attachments

---

## 6. 与 Modular Avatar 集成状态

> **⚠️ [Missing Information / 未确认]**:截至 2026-06-30,Modular Avatar 是否提供 Accessories 的 NDMF 工具支持?**未在知识库内确认**。
>
> 建议:查 MA GitHub 仓库 issue / changelog 确认。

### 与 "Visible Head Accessory" 的区别

| 维度 | Avatar Accessories (VRChat 原生) | Visible Head Accessory (MA 组件) |
|------|----------------------------------|-----------------------------------|
| 性质 | VRChat 运行时系统 | Modular Avatar 编译时组件 |
| 用途 | 装备可穿戴物品 | 让头部子对象在第一人称可见 |
| 数量限制 | 单 Avatar 5 个,全局 80/240 | 无(由子对象数量决定) |
| 跨世界 | ✅ 永久装备 | ✅ 编译进 Avatar |
| 依赖 | VRChat 客户端原生 | MA NDMF 编译流程 |

---

## 7. 故障排查

| 症状 | 可能原因 | 修复 |
|------|---------|------|
| 装备的 Accessory 不显示 | 超过全局渲染限制(80/240) | 检查实例内 Accessories 数量,移动靠近玩家 |
| Accessories 通知反复出现 | 2026.2.1 之前的客户端 bug | 升级到 2026.2.1p1+ |
| Fallback 错误显示 | 客户端版本 < 2026.2.1p1 | 升级客户端 |
| Look 中 Accessories 加载卡住 | Avatar 切换 + Accessories 加载竞争 | 等待加载完成,或在 Look Editor 切到 Accessories 标签查看进度 |
| Accessories 在 3P 模式不显示(头部) | 2026.2.1 Open Beta 已知问题,已修复 | 升级到 2026.2.1+ |

---

## 8. 参考资料

- **VRChat 2026.2.1 Release Notes**(Build 1835) - Accessories 正式上线
- **VRChat 2026.2.1 Open Beta Notes** - Beta 阶段细节 + Build 1832/1833 修复
- **VRChat 2026.1.3p1 Open Beta Notes** - Look Editor 行为变更
- **VRChat 2026.2.1p1 Release Notes** - 后续补丁
- **VRChat Developer Update**(2026-04) - 详细 API 解释
- 相关:`memory/avatar/vrcraycast.md` (Avatar 端 raycast 性能优化与 Accessories 兼容性)
- 相关:`memory/avatar/performance-rank.md` (Accessories 计入 Performance Rank)

---

**最后更新**:2026-06-30 | **状态**:✅ 知识库收录 | **来源**:VRChat 官方 Release Notes
