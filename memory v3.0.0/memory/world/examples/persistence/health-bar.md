---
title: "Health Bar(血条)"
category: world
subcategory: examples
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/examples/persistence/health-bar/"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - persistence
  - udonsharp
aliases:
  - "Health Bar(血条)"
  - health-bar
related:
  - leaderboard.md
  - persistent-pen.md
  - position-sync.md
  - post-processing-settings.md
  - simple-rpg.md
---
# Health Bar(血条)


## 数据层选择

| 类型 | PlayerObject |
|------|--------------|
| 关键组件 | `VRCPlayerObject` + `UdonBehaviour` + `VRCEnablePersistence` |

## 概述

一个简单的血条系统,使用 **PlayerObject** 同步和持久化玩家的血量。
在示例世界中,玩家站在"熔岩"区域会受到伤害,血量归零后会复活并恢复满血。

## 使用方法

### 客户端测试
1. 运行场景或 Build & Test
2. 打开 `HealthBar_ExampleScene`
3. 走到红色"熔岩"区域
4. 抬头查看血条,会看到血量因持续掉血而减少
5. 离开熔岩并重新加入 World
6. 血量会恢复到之前的值(注意:完全归零后会复活并恢复满血)

### 导入方法
通过 **Example Central**(`VRChat SDK > 🏠 Example Central`)导入。

## 技术分解

熔岩存储对本地玩家血条的引用。玩家进入触发器时,会通过血条的 `TakeDamage` 函数开始造成伤害。

⚠️ **关键约束**:`TakeDamage` 只能由本地客户端调用。

### Inspector 参数

#### HealthBar
- `Slider` Health Bar Slider - 显示玩家血量的 UI Slider
- `Vector3` Offset Above Head - 血条距离玩家头顶的偏移
- `float` MaxHealth - 玩家最大血量

#### Lava
- `float` Damage per second - 熔岩每秒造成的伤害

## PlayerObject 模式要点

```csharp
// PlayerObject 中的 [UdonSynced] 变量自动持久化
public class HealthBar : UdonSharpBehaviour
{
    [UdonSynced] private float currentHealth;
    
    public void TakeDamage(float amount)
    {
        if (!Networking.IsOwner(Networking.LocalPlayer, gameObject)) return;
        currentHealth = Mathf.Max(0, currentHealth - amount);
        RequestSerialization();  // 同步 + 自动持久化
    }
}
```

## Key 命名空间建议

```text
推荐前缀: HealthBar-
示例:
- HealthBar-MaxHealth
- HealthBar-CurrentHealth(自动持久化)
```

## 限制

- **100 KB/player/world**(PlayerObject 配额,独立于 PlayerData)
- 血量数据小,远未触及上限

## Changelog

- **0.0.2** - Added in-world UI, thumbnail, published world
- **0.0.1** - Initial Version

## 验证清单

✅ 数据层:PlayerObject
✅ 关键组件:VRCPlayerObject + UdonBehaviour + VRCEnablePersistence
✅ 引用 100 KB 限制
✅ 引用 OnPlayerRestored 时机
✅ Key 命名空间前缀建议
