---
title: "Simple RPG(简单 RPG)"
category: world
subcategory: examples
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/examples/persistence/simple-rpg/"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - persistence
  - udonsharp
aliases:
  - "Simple RPG(简单 RPG)"
  - simple-rpg
related:
  - health-bar.md
  - leaderboard.md
  - persistent-pen.md
  - position-sync.md
  - post-processing-settings.md
---
# Simple RPG(简单 RPG)

> SDK Version: 3.4.x+
> 关联底层: `memory/api/persistence.md`

## 数据层选择

| 类型 | **PlayerObject** |
|------|------------------|
| 关键组件 | `VRCPlayerObject` + `UdonBehaviour` + `VRCEnablePersistence` + `[UdonSynced]` |

## 概述

一个简单 RPG 体验的示例,可以升级、改变职业和击败敌人。
使用 **`persistence-beta` branch** 进行测试。

## 使用方法

1. 打开 `Assets/Examples/RPG` 文件夹下的场景 `RPGExample`
2. 播放场景
3. 选择职业:走过相应的底座
4. 通过击败敌人获得经验值
5. 经验值足够时升级(头顶的钻石数量指示等级)
6. 重新加入 World
7. 加载时,你应该被传送到之前的位置,并保留上次选择的职业、相同等级和经验值

## 技术分解

### RPGPlayer 脚本
附加到 GameObject 上,该 GameObject 上有 PlayerObject 脚本,意味着 **RPGPlayer 脚本为每个玩家实例化一次**。
RPGPlayer 控制头顶钻石的显示(指示职业和等级),也用于显示其他玩家的武器。

### 3 个职业底座
3 个不同的底座,走过时会触发,告诉你的 RPGPlayer 实例更改职业。

### 数据持久化机制

⚠️ **关键设计**:
> **职业、上次位置、经验和等级** 都是通过是 `UdonSynced` 且在 `VRCPlayerObject` 上而持久化的。
> 任何在属于 PlayerObject 的 GameObject 上的脚本中的 `UdonSynced` 变量都会自动持久化。

```csharp
public class RPGPlayer : UdonSharpBehaviour
{
    [UdonSynced] public int playerClass;       // 职业 (0=Warrior, 1=Mage, 2=Rogue)
    [UdonSynced] public int playerLevel;       // 等级
    [UdonSynced] public int playerExperience;  // 经验值
    [UdonSynced] public Vector3 lastPosition;  // 上次位置
    [UdonSynced] public Quaternion lastRotation; // 上次旋转
}
```

### 战斗系统
战斗使用 **粒子碰撞** 完成,每个职业有不同的粒子效果作为攻击,带有 collider。
敌人死亡时给 1 exp,需要 4 exp 才能升级。
敌人在被击败后 10-15 秒重新生成。

## 数据流

```text
玩家走近底座 → trigger 触发
    ↓
调用本地玩家的 RPGPlayer.ChangeClass(newClass)
    ↓
playerClass = newClass
RequestSerialization()
    ↓
[UdonSynced] 字段同步给所有玩家
VRCEnablePersistence 自动持久化
    ↓
玩家离开 World → 重新加入 → OnPlayerRestored
    ↓
所有 [UdonSynced] 字段自动从服务器恢复
```

## 限制

- **100 KB/player/world**(PlayerObject 配额)
- RPGPlayer 数据小(class + level + exp + position + rotation < 100 bytes)
- 远未触及上限
- ⚠️ **测试需要 `persistence-beta` branch**

## Key 命名空间建议

由于数据存储在 PlayerObject 的 `[UdonSynced]` 字段中,Key 命名空间概念不直接适用。
但如果混用 PlayerData(例如保存职业偏好),应使用前缀:

```text
推荐前缀: RPG-
示例:
- RPG-FavoriteClass     (Int,0=Warrior, 1=Mage, 2=Rogue)
- RPG-TotalKills        (Int)
- RPG-TotalPlayTime     (Float,秒)
```

## Changelog

- **0.0.3**: Added Instructions Canvas
- **0.0.2**: Script tweaks: RPG Example uses VRCEnablePersistence components on player objects so that they persist again

## 验证清单

✅ 数据层:PlayerObject
✅ 关键组件:VRCPlayerObject + UdonBehaviour + VRCEnablePersistence
✅ [UdonSynced] 自动持久化机制说明
✅ 引用 100 KB 限制
✅ Key 命名空间前缀建议(扩展场景)
✅ 引用 OnPlayerRestored 时机
