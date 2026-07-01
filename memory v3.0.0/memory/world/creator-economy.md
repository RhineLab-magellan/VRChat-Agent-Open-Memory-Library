---
title: "Creator Economy SDK"
category: world
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - avatar
  - udonsharp
aliases:
  - "Creator Economy SDK"
  - creator-economy
related:
  - "sources/example-central.md"
  - "api/networking.md"
  - items.md
  - luraswitch2.md
  - performance-guide.md
---
# Creator Economy SDK

---

## Overview

VRChat Creator Economy 允许创作者通过销售虚拟产品（Udon Products）来获利。产品可以是一次性购买或订阅类型。

---

## 核心概念

### UdonProduct
- Unity ScriptableObject，代表商店中的产品
- 通过 UdonProductManager 创建：`VRChat SDK → UdonProduct Manager`
- 或手动创建：`Assets → Create → VRChat → UdonProduct`

---

## Store API

### 打开商店页面
```csharp
// 打开世界商店
Store.OpenWorldStorePage();

// 打开群组页面
Store.OpenGroupPage(groupId);

// 打开群组商店
Store.OpenGroupStorePage(groupId);

// 打开指定 Listing
Store.OpenListing(listingId, storeSection, contextId);
// storeSection: "vrchat" | "avatar" | "world" | "group"
// contextId: group ID 或 world ID（用于群组/世界商店）

// 打开市场商店
Store.OpenMarketplaceStore(section, listingId);
```

### 产品查询
```csharp
// 检查玩家是否拥有产品
bool owns = Store.DoesPlayerOwnProduct(player, productId);

// 检查是否有任何玩家拥有产品
bool anyOwns = Store.DoesAnyPlayerOwnProduct(productId);

// 获取拥有产品的玩家列表
var players = Store.GetPlayersWhoOwnProduct(productId);
```

### 事件
```csharp
// 产品事件
Store.SendProductEvent(productId, eventName);

// 查询购买
Store.ListPurchases();
Store.ListAvailableProducts();
Store.ListProductOwners(productId);

// 回调事件
OnPurchaseConfirmed(player, productId)
OnPurchaseConfirmedMultiple(player, productIds[])
OnPurchaseExpired(player, productId)
OnPurchasesLoaded(player, purchases[])
OnProductEvent(player, productId, eventName)
OnListPurchases(player, purchases[])
OnListAvailableProducts(products[])
OnListProductOwners(players[])
```

---

## 示例 Prefabs

通过 Example Central 导入：
```
Unity Menu → VRChat SDK → 🏠 Example Central
Settings → Enable "Show Creator Economy Examples"
```

### 可用 Prefabs

| Prefab | 功能 |
|--------|------|
| **OpenListing** | 打开单个 Listing 页面 |
| **OpenWorldStore** | 打开世界商店 |
| **OpenGroupPage** | 打开群组页面 |
| **FloatingOverheadBuyIndicator** | 浮动购买指示器 |
| **ProductOwnersInInstance** | 列出实例中的产品所有者 |
| **ProductOwnersOnlyArea** | 仅所有者可进入区域 |
| **UdonProductToggle** | 基于所有权切换 GameObject |
| **SupporterList** | 支持者列表 |
| **ProductEventTimed** | 定时产品事件 |

---

## 配置步骤

### 1. 创建产品
1. 在 Unity 中创建 UdonProduct
2. 配置产品 ID 和属性
3. 在 VRChat Creator Dashboard 发布

### 2. 集成到世界
```csharp
// 打开 Listing
Store.OpenListing("prod_xxxx-xxxx", "group", "grp_xxxx-xxxx");

// 检查所有权
if (Store.DoesPlayerOwnProduct(player, productId))
{
    // 给予访问权限
}
```

### 3. 测试
- 必须 "Build & Publish" 才能测试商店功能
- "Build & Test" 不支持打开商店

---

## 产品类型

| 类型 | 说明 |
|------|------|
| **Consumable** | 消耗品，可重复购买 |
| **Instant** | 即时交付，一次性购买 |
| **Subscription** | 订阅，定期收费 |

---

## 限制

1. 需要 VRChat Trust Rank "New User" 或更高
2. Creator Economy Examples 需要 Beta 权限
3. 商店功能仅在发布版本可用

---

## 相关文档

- `memory/sources/example-central.md` - Example Central 使用
- `memory/api/networking.md` - 网络同步