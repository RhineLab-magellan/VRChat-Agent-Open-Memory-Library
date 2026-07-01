---
title: "Persistence Examples - 索引"
category: world
subcategory: examples
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/examples/persistence/"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - misc
  - index
  - navigation
aliases:
  - 持久化
  - "Persistence Examples - 索引"
related:
  - health-bar.md
  - leaderboard.md
  - persistent-idle-game.md
  - persistent-pen.md
  - playerdata-types.md
  - position-sync.md
  - post-processing-settings.md
  - simple-rpg.md
  - unlock-items.md
  - "api/persistence.md"
  - "api/networking.md"
  - "sources/example-central.md"
  - "sources/clientsim.md"
---
# Persistence Examples - 索引


## 概述

VRChat 官方提供 **9 个 Persistence 示例 Prefab**,覆盖跨实例数据保留的典型应用场景。
所有示例通过 **Example Central**(`VRChat SDK > 🏠 Example Central`)导入。

## 9 个示例分类

| # | 示例 | 数据层 | 核心 API | 文档 |
|---|------|--------|----------|------|
| 1 | **Health Bar** | PlayerObject | `VRCPlayerObject` + 血量同步 | [health-bar.md](./health-bar.md) |
| 2 | **Leaderboard** | PlayerData | `PlayerData.SetFloat/TryGetFloat` | [leaderboard.md](./leaderboard.md) |
| 3 | **Persistent Idle Game** | PlayerData | `PlayerData` + `OnPlayerRestored` | [persistent-idle-game.md](./persistent-idle-game.md) |
| 4 | **Persistent Pen** | PlayerObject | `VRCPlayerObject` + `VRCEnablePersistence` | [persistent-pen.md](./persistent-pen.md) |
| 5 | **Player Data Types** | PlayerData | 18 种支持数据类型演示 | [playerdata-types.md](./playerdata-types.md) |
| 6 | **Position Sync** | PlayerObject | 0.5s 周期 + `OnPlayerRestored` | [position-sync.md](./position-sync.md) |
| 7 | **Post-Processing Settings** | PlayerData | `OnPlayerDataUpdated` + Slider | [post-processing-settings.md](./post-processing-settings.md) |
| 8 | **Simple RPG** | PlayerObject | `UdonSynced` 变量自动持久化 | [simple-rpg.md](./simple-rpg.md) |
| 9 | **Unlock Items** | PlayerData | `OnPlayerRestored` + 成就系统 | [unlock-items.md](./unlock-items.md) |

## PlayerData vs PlayerObject 决策矩阵

| 场景特征 | 推荐数据层 | 示例 |
|----------|------------|------|
| **大量数据** + **频繁变化** | PlayerObject | Persistent Pen (笔触数据) |
| **少量数据** + **偶尔变化** | PlayerData | Health Bar、Settings、Unlocks |
| **跨设备同步** + **所有人可见** | PlayerData | Leaderboard |
| **需要场景中 synced GameObject** | PlayerObject | RPG Player、Position Sync |
| **简单 key-value** | PlayerData | Idle Game 分数 |
| **复杂 UdonBehaviour 状态** | PlayerObject | Pen System、RPG Player |

⚠️ **重要警告**: 任何 PlayerData 修改会发送 **全部** PlayerData。跨 Prefab 引用时易膨胀。

## 关键工程约束(全部示例通用)

### 限制

| 类型 | 限制 | 说明 |
|------|------|------|
| PlayerData | 100 KB/player/world | 已压缩配额 |
| PlayerObject | 100 KB/player/world | 独立配额(不共享) |
| 原始数据上限 | ~300 KB | 高度可压缩时可达 |
| String max | ~50 chars | 建议值 |
| Key max | 128 chars | 建议值 |

### 行为约束

- ❌ **OnPlayerLeft 中无法保存数据** —— 玩家离开时无法触发持久化写入
- ❌ **不能跨 World 共享** —— 数据绑定到具体 World
- ❌ **无内置 save slots** —— 只有单一持久化存储
- ✅ **OnPlayerRestored 前写入会静默忽略** —— 必须用 `_dataReady` flag 守卫

### Key 命名空间建议(避免冲突)

由于 PlayerData 跨整个 World 的所有 Prefab 共享,**官方建议使用 Prefab 名作为前缀**:

```text
推荐格式: <Prefab名>-<功能描述>
示例:
- Momo-PPP-BloomAmount        # 来自 Momo Post Processing
- IdleGame-POINTS_KEY         # 来自 Persistent Idle Game
- PenSystem-Line-Color-0      # 来自 Persistent Pen
- RPG-Player-Level            # 来自 Simple RPG
```

❌ 错误:直接使用 `score` / `level` / `health`(易冲突)

## OnPlayerRestored 时机(所有示例的核心)

```csharp
// 在 OnPlayerRestored 之前写入会静默忽略
// 必须用 _dataReady flag 守卫

private bool _dataReady = false;

public override void OnPlayerRestored(VRCPlayerApi player)
{
    if (player != Networking.LocalPlayer) return;  // 只处理本地玩家
    _dataReady = true;
    LoadData();
}
```

## 关联知识库

- `memory/api/persistence.md` - 底层 API 参考(PlayerData / PlayerObject 完整方法签名)
- `memory/api/networking.md` - `[UdonSynced]` 网络同步机制(与 PlayerObject 互链)
- `memory/sources/example-central.md` - Example Central 使用指南
- `memory/sources/clientsim.md` - ClientSim 编辑器模拟(支持 PlayerData 调试窗口)

## 验收标准

✅ 10 个 .md 文件全部创建
✅ 每个示例标注 PlayerData/PlayerObject 用法
✅ 全部引用 100 KB 限制
✅ 全部强调 Key 命名空间前缀方案
✅ 全部引用底层 persistence.md
