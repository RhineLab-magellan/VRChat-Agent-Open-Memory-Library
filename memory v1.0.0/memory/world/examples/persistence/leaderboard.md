# Leaderboard(排行榜)

> Domain: World / Examples / Persistence
> Source: https://creators.vrchat.com/worlds/examples/persistence/leaderboard
> 索引日期: 2026-06-15
> SDK Version: 3.4.x+
> 关联底层: `memory/api/persistence.md`

## 数据层选择

| 类型 | PlayerData |
|------|------------|
| 关键 API | `PlayerData.SetFloat/TryGetFloat` + `OnPlayerDataUpdated` |

## 概述

使用 **PlayerData** 持久化和显示玩家高分。
支持跨设备同步 —— 玩家在 PC 上的分数在 Quest 上重新加入时仍能恢复。

## 使用方法

### 客户端测试
1. 打开 Leaderboard 场景
2. 进入 Play Mode
3. 你的名字以 0 分出现在排行榜上
4. 跳跃,分数增加
5. 退出并重新进入 Play Mode
6. 排行榜仍保留你的名字,分数被记住

## 技术分解

### Leaderboard 脚本
可以添加任何希望玩家按其排序的 key。支持 **Float 和 Int**。

### LeaderboardSlot 脚本
这是一个 **PlayerObject**(`RectTransform`),意味着每个加入的玩家都会创建一个实例。
对象创建时,会自动添加到 Leaderboard 定义的 Scroll View 中。

### Scroll View 排序机制
Scroll View 的 content transform 带有 **Vertical Layout Group**,使所有子项按层级顺序自动排序。
`Leaderboard` 脚本会在玩家持久化分数变化时更新 `LeaderboardSlot` 在层级中的位置。

## 数据流

```text
玩家跳跃 → 分数 +1
    ↓
PlayerData.SetFloat(player, "LeaderBoard_Score", score)
    ↓
OnPlayerDataUpdated 触发
    ↓
所有玩家看到该玩家的 LeaderboardSlot 位置更新
    ↓
玩家重新加入 → OnPlayerRestored → 从 PlayerData 读取分数
```

## Key 命名空间建议

```text
推荐前缀: Leaderboard-
示例:
- Leaderboard-Score       (Float,自动持久化)
- Leaderboard-PlayerName  (String,~50 chars)
```

## 限制

- **100 KB/player/world**(PlayerData 配额)
- 排行榜数据小,远未触及上限
- ⚠️ String max ~50 chars(玩家名字)

## Changelog

- **0.0.2**: Script tweaks: Use VRCEnablePersistence components on player objects

## 验证清单

✅ 数据层:PlayerData
✅ 关键 API:PlayerData.SetFloat/TryGetFloat
✅ 引用 100 KB 限制
✅ 跨设备同步场景明确
✅ Key 命名空间前缀建议
