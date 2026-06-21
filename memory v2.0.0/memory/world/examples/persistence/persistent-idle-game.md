---
title: Persistent Idle Game(放置类游戏)
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - persistence
  - networking

aliases:
  - "Persistent Idle Game(放置类游戏)"

source: https://creators.vrchat.com/worlds/examples/persistence/persistent-idle-game/
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Persistent Idle Game(放置类游戏)


## 数据层选择

| 类型 | **混合(主要是 PlayerData)** |
|------|------------------------------|
| 关键 API | `PlayerData.SetInt/TryGetInt` + `OnPlayerRestored` |

## 概述

一个简单的放置类游戏,使用 **PlayerData** 保存每个玩家的分数和自动点击器数量。

## 使用方法

### 客户端测试
1. 加载场景,根据需要调整 "IdleGame" 对象上的 Udon 值
2. Play Mode
3. 点击按钮收集 cheese
4. 购买自动点击器(auto-clicker)
5. 离开 Play Mode
6. 在 ClientSim PlayerData 窗口观察数据是否保存在各自 key 下

## 技术分解

### 主要脚本:`IdleGame.cs`
处理游戏玩法、保存和加载。唯一的其他脚本 `IdleGameButton.cs` 与主脚本通信玩家的点击事件。

### 数据持久化 Key

| 常量名 | 用途 | 数据类型 |
|--------|------|----------|
| `POINTS_KEY` | 玩家点击获得的分数 | int |
| `AUTOCLICKERS_KEY` | 自动点击器数量 | int |

### 核心逻辑

```csharp
// 玩家点击按钮时
public void OnButtonClicked()
{
    if (!_dataReady) return;  // 守卫
    points += 1;
    PlayerData.SetInt(Networking.LocalPlayer, POINTS_KEY, points);
}

// 购买自动点击器时
public void BuyAutoClicker()
{
    int cost = CalculateCost(autoClickers);
    if (points < cost) return;
    
    points -= cost;
    autoClickers += 1;
    
    PlayerData.SetInt(Networking.LocalPlayer, POINTS_KEY, points);
    PlayerData.SetInt(Networking.LocalPlayer, AUTOCLICKERS_KEY, autoClickers);
}

// 每秒为每个 auto-clicker 增加 1 个分数
// 重新加载场景时,使用 POINTS_KEY 和 AUTOCLICKERS_KEY 加载分数和自动点击器值
```

## Key 命名空间建议

```text
推荐前缀: IdleGame-
示例:
- IdleGame-POINTS        (Int)
- IdleGame-AUTOCLICKERS  (Int)
```

## 限制

- **100 KB/player/world**(PlayerData 配额)
- 分数和点击器数量小,远未触及上限
- ⚠️ **OnPlayerRestored 前写入会静默忽略**

## Changelog

- **0.0.2**: Script tweaks: The code uses OnPlayerRestored to load player data

## 验证清单

✅ 数据层:PlayerData(混合模式)
✅ 关键 API:PlayerData.SetInt/TryGetInt
✅ 引用 100 KB 限制
✅ 引用 OnPlayerRestored 时机
✅ Key 命名空间前缀建议
