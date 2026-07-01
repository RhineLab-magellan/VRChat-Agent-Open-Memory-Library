---
title: Companions & Props (Items 分离,2026.2.3+)
category: world

knowledge_level: applied
status: active

tags:
  - world
  - items
  - companions
  - props
  - creator-granularity
  - 2026

aliases:
  - Companions
  - "Avatar Companions"
  - Props
  - "Props 移动修改"
  - "Items 分离"

related:
  - items.md
  - layers.md
  - performance-guide.md
  - ../avatar/accessories.md
  - index.md

source: VRChat 2026.2.3 / 2026.2.3p1 / 2026.2.3 Open Beta Release Notes
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Companions & Props (Items 分离,2026.2.3+)

> **重要变更**:2026.2.3 起,Inventory 中的 "Items" **拆分为两个独立类别**:
> - **Props**(传统 Item,可丢出/收起)
> - **Companions**(跟随玩家的"伙伴")
>
> **来源**:VRChat 2026.2.3 正式上线(2026.2.3 Open Beta Build 1863 起 Companion 系统启用)

---

## 1. 概念对比

| 维度 | Props(传统 Item) | Companions |
|------|------------------|------------|
| **行为** | 玩家丢出、收回、可重新放置 | **永久 spawned**,跟随玩家 |
| **生成方式** | 玩家在世界中手动丢出 | 进入新实例自动存在 |
| **位置控制** | 完全由玩家控制 | 新重定位系统(不完全固定) |
| **跟随玩家** | ❌ 不会 | ✅ 跟随更紧密 |
| **Spawn/Despawn 动画** | 通用 | 各自有自定义动画 |
| **同时数量** | 多个(具体上限待查) | **仅 1 个** |
| **世界能否隐藏/禁用** | ✅ 可以 | ❌ **不能**(World Creator 角度) |
| **首版应用** | 已有所有 Item | Reference Cube Companion(2026.2.3 Open Beta) |
| **已升级老 Companion** | — | Kath、Treats(2026.2.3p1 完成) |

---

## 2. World Creator 角度(创作者须知)

### 2.1 Companions 无法被 World 隐藏

> **🔴 关键约束**:`World 不能隐藏或禁用 Companions`(2026.2.3 起)。
>
> 与 Props 不同,即使 World 作者通过 VRC_ContentSettings 或类似机制禁用 Props,Companions **仍然显示**。
>
> **设计影响**:World 设计需要考虑玩家会自带 Companion,不能假设"干净场景"。

### 2.2 Props 颗粒度控制(2026.2.3 新增)

VRChat 网站的 **World Details 页面**新增 Props 能力分类禁用功能:

| 能力分类 | 说明 | 状态 |
|----------|------|------|
| **"Props that Modify Player Movement"** | 永久禁用可改变玩家移动速度、传送等能力的 Props | ✅ **2026.2.3 上线** |
| 未来更多类别 | 官方表示"会添加更多" | ⌛ 待定 |

#### 启用方式

1. 访问 https://vrchat.com/home/content/worlds
2. 点击 World 缩略图打开 "Edit"
3. 在 **Default Content Settings** 找到新分类
4. 按需禁用,并在文本框说明原因
5. 滚到顶部按 "Save"

> **影响范围**:此设置对**所有玩家**生效(World 级别),不针对单个玩家。

### 2.3 与 Items 的关系

| 项目 | Items(旧) | Items(新拆分后) |
|------|-----------|-----------------|
| Props 类别 | 一部分 | ✅ 全部非 Companion Item |
| Companions 类别 | 一部分 | ✅ 跟随玩家型 Item |
| Layer 归属 | Layer 3 (`Item`) | **同 Layer 3 (`Item`)**(未变更) |

> **⚠️ [Missing Information / 未确认]**:Companions 是否在物理上使用与 Props 相同的 Layer 3?**未在 release notes 中明确**。
> **建议**:查 VRChat Creator Docs 或社区测试。

---

## 3. 用户角度(快速参考)

### 3.1 装备 Companion

- 进入新 World → Companion 自动跟随
- 通过 Quick Menu "Here" tab 或 Companion 详情页定制
- 旧的 Inventory 方式仍可用

### 3.2 切换 Companion

- 一次只能有 1 个 Companion
- 切换前需要收起当前 Companion

### 3.3 与 Props 共存

- Companions 与 Props **可以同时存在**
- Companions 独立于 Props 隐藏机制
- Props 可被 World 禁用,Companions 不能

---

## 4. Udon 行为变更建议

### 4.1 现有 World 影响

> **World Author 应重新测试**:
> - 之前假设"玩家无 Companion 干扰"的设计可能不再成立
> - 2026.2.3 后任何 World 都可能有玩家携带 Companion

### 4.2 LayerMask 调整

```csharp
// 推荐:Physics 方法显式排除 Companion/Prop 区域
// Layer 3 (Item) 同时包含 Props 和 Companions
int layerMask = LayerMask.GetMask("Default", "Environment", "Pickup", "Interactive");
// 故意排除 "Item" (Layer 3) - 包含 Props 和 Companions

RaycastHit hit;
if (Physics.Raycast(origin, direction, out hit, maxDistance, layerMask))
{
    if (Utilities.IsValid(hit.gameObject))  // 防御 null/Item
    {
        return hit.gameObject;
    }
}
```

### 4.3 监测 API

> **⚠️ [Missing Information / 未确认]**:
> - Udon 端是否有 `OnCompanionAttached` / `OnCompanionDetached` 事件?**未确认**
> - Udon 端能否判断玩家是否携带 Companion?**未确认**
> - 建议查 VRChat Creator Docs 更新日志

---

## 5. 已知问题与时间线

| 版本 | 变更 |
|------|------|
| 2026.2.3 Open Beta Build 1863 | Companion 系统启用(仅 Reference Cube Companion) |
| 2026.2.3 正式版 | Companion 系统 + Props 移动修改禁用 |
| 2026.2.3p1 | Kath、Treats 升级为新系统 |
| 未来 | 更多 Companion 类别,可能更多 Props 能力分类禁用 |

---

## 6. 故障排查

| 症状 | 可能原因 | 修复 |
|------|---------|------|
| Companion 不显示 | 旧版 Companion(未升级) | 等待官方升级(Kath/Treats 已升级) |
| World 尝试隐藏 Companion 失败 | Companion 不能被 World 隐藏 | 接受此限制,设计兼容场景 |
| 多个 Companion 同时存在 | 当前规则仅允许 1 个 | 收起前一个后再装备 |
| Companion 穿模 | 重定位系统边界 | 调整 World 几何或等待官方修复 |
| Props 移动修改未禁用 | World 设置未更新 | 在 VRChat Website 启用对应禁用 |

---

## 7. 参考资料

- **VRChat 2026.2.3 Release Notes**(Build 1864)
- **VRChat 2026.2.3 Open Beta Notes**(Build 1863)
- **VRChat 2026.2.3p1 Release Notes**(Build 1865) - Kath/Treats 升级
- 相关:`memory/world/items.md` (旧版 Items 概念)
- 相关:`memory/world/layers.md` (Layer 3 Item 定义)
- 相关:`memory/avatar/accessories.md` (Avatar 端配饰,完全独立)

---

**最后更新**:2026-06-30 | **状态**:✅ 知识库收录 | **来源**:VRChat 官方 Release Notes
