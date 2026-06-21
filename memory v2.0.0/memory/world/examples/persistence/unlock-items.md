---
title: Unlock Items(永久解锁)
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - persistence
  - networking
  - udonsharp

aliases:
  - "Unlock Items(永久解锁)"

source: https://creators.vrchat.com/worlds/examples/persistence/unlock-items/
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Unlock Items(永久解锁)


## 数据层选择

| 类型 | **PlayerData** |
|------|----------------|
| 关键 API | `OnPlayerRestored` + 成就系统 |

## 概述

如何使用 **PlayerData 永久解锁物品**,以简单的世界内成就作为演示。
⚠️ **注意**:此处的 "Items" 是通用术语,**不指** [user-spawned items](/worlds/items)。

## 使用方法

1. 进入 World
2. 执行动作以解锁成就
   - 在 World 中花费时间(10 秒,2 分钟,5 分钟)
   - 移动距离(10 单位,100 单位,300 单位)
   - Respawn
   - 找到秘密
   - 完成以上所有
3. 观察 UI 显示你解锁的成就
4. 离开并返回 —— 你的成就和统计(在 World 中花费的时间、移动距离)应持续保存

## 技术分解

### UnlockItems 主脚本

```csharp
public class UnlockItems : UdonSharpBehaviour
{
    private bool _dataReady = false;
    private const float UPDATE_STATS_TIME = 1f;
    
    public override void OnPlayerRestored(VRCPlayerApi player)
    {
        if (player != Networking.LocalPlayer) return;
        _dataReady = true;
        UpdateStats();  // 检查并恢复已解锁的成就
    }
    
    public void UpdateStats()
    {
        CheckTimeInWorld();
        CheckDistanceMoved();
        CheckHasPlayerRespawned();
        CheckHasFoundSecret();
        CheckAllAchievementsUnlocked();
        
        // 递归调用(延迟后再次运行)
        SendCustomEventDelayedSeconds(nameof(UpdateStats), UPDATE_STATS_TIME);
    }
}
```

### 5 个检查方法

| 方法 | 触发条件 | 解锁内容 |
|------|----------|----------|
| `CheckTimeInWorld()` | 在 World 中累计时间(10s/2min/5min) | 时间类成就 |
| `CheckDistanceMoved()` | 累计移动距离(10/100/300 单位) | 距离类成就 |
| `CheckHasPlayerRespawned()` | 玩家死亡后 respawn | 复活成就 |
| `CheckHasFoundSecret()` | 找到隐藏地点 | 秘密成就 |
| `CheckAllAchievementsUnlocked()` | 完成所有上述成就 | 终极成就 |

### 成就解锁机制

对于在 `UpdateStats` 检查期间解锁的每个成就,调用 `UnlockAchievement` 方法,
该方法更新目标成就的 sprite、颜色和文本。

```csharp
public void UnlockAchievement(int achievementId)
{
    if (!_dataReady) return;
    
    // 1. 写入 PlayerData(永久)
    string key = $"UnlockItems-Achievement-{achievementId}";
    PlayerData.SetBool(Networking.LocalPlayer, key, true);
    
    // 2. 更新 UI(本地)
    UpdateAchievementUI(achievementId);
}
```

## Key 命名空间分析

✅ **本示例 Key 命名规范** —— 使用 `UnlockItems-Achievement-{id}` 格式,包含 Prefab 名前缀。

## 数据流

```text
玩家进入 World → OnPlayerRestored
    ↓
UpdateStats 启动(每 1 秒运行一次)
    ↓
5 个检查方法并行运行
    ↓
新成就解锁 → UnlockAchievement(id)
    ↓
PlayerData.SetBool(localPlayer, "UnlockItems-Achievement-{id}", true)
    ↓
更新 UI 反馈
    ↓
玩家离开 World → 重新加入 → OnPlayerRestored
    ↓
遍历 PlayerData 中所有 UnlockItems-Achievement-* key → 恢复已解锁成就
```

## 限制

- **100 KB/player/world**(PlayerData 配额)
- 5 个成就 + 统计 = ~10 个 key(远未触及上限)
- ⚠️ **OnPlayerRestored 前写入会静默忽略** —— 必须用 `_dataReady` flag 守卫

## 永久解锁 vs 临时状态

| 场景 | 推荐 | 说明 |
|------|------|------|
| **永久解锁** | PlayerData | 跨 World 实例、跨玩家重新加入 |
| **本局状态** | `[UdonSynced]` on PlayerObject | 玩家离开 World 后重置 |
| **当前进度** | PlayerData + 时间戳 | 防止成就滥用 |

## Changelog

- Last updated on **Jun 12, 2025**

## 验证清单

✅ 数据层:PlayerData
✅ 关键 API:OnPlayerRestored + PlayerData.SetBool/TryGetBool
✅ 引用 100 KB 限制
✅ Key 命名空间前缀规范(本示例规范)
✅ 引用 OnPlayerRestored 时机
✅ 永久解锁 vs 临时状态区分
