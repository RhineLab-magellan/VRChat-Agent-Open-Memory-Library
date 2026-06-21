---
title: PlayerData 实战
category: world
subcategory: udon/persistence
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - storage
  - player-data
  - key-value
aliases:
  - PlayerData 教程
  - PlayerData API
  - 玩家数据
related:
  - ../../../api/persistence.md
  - ../index.md
  - player-object.md
  - serialization.md
  - limits-and-quirks.md
  - patterns/leaderboard.md
  - patterns/unlock-items.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/persistence/player-data/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# PlayerData 实战

> SDK Version: 3.7+(核心 API) / 3.10+(Storage Information API)
> 官方文档:https://creators.vrchat.com/worlds/udon/persistence/player-data/
> 命名空间:`VRC.SDK3.Persistence`(核心) + `VRC.SDKBase`(查询)

---

## 概述

PlayerData 是 **键值数据库(Key-Value Store)**,与每个玩家关联。**任何 Udon 脚本** 可访问它,无需 Prefab 设置。**任何 UdonBehaviour 的同步设置不影响** PlayerData(设为 None 也能用)。

支持的类型:
- 整数家族(sbyte/byte/short/ushort/int/uint/long/ulong)
- 浮点(float/double)
- 向量(Vector2/Vector3/Vector4)
- 颜色(Color/Color32)
- Quaternion
- String
- bool
- **byte[]**(原始字节,用于自定义序列化)

---

## 设置(Setup)

> 极其简单:用就完事了。无需在 Inspector 勾选任何东西,无需 Prefab。

```csharp
using VRC.SDK3.Persistence;  // 核心 API
using VRC.SDKBase;          // VRCPlayerApi + Storage Info API

public class MyPlayerData : UdonSharpBehaviour {
    public override void OnPlayerRestored(VRCPlayerApi player) {
        // 等到 OnPlayerRestored 才能安全读写
    }
}
```

### 时序警告(必读)

> 🔴 **不要在 `OnPlayerJoined` 中读写 PlayerData**

```csharp
// ❌ 错误:可能读到空数据,或被服务器拉来的数据覆盖
public override void OnPlayerJoined(VRCPlayerApi player) {
    PlayerData.SetInt(player, "score", 0);  // 静默失败 / 被覆盖
}

// ✅ 正确:OnPlayerRestored 触发后读写
private bool _dataReady = false;

public override void OnPlayerRestored(VRCPlayerApi player) {
    if (player != Networking.LocalPlayer) return;  // 只处理本地玩家
    _dataReady = true;
    LoadData();
}
```

> **为什么**:`OnPlayerJoined` 触发时,数据可能还在从 VRChat 服务器下载。`OnPlayerRestored` 表示该玩家的全部持久化数据已就绪。

---

## 写入(Mutators)完整列表

> 17 种 Set 方法。**只能写本地玩家**。写入是即时生效(走 Manual Sync 模式)。

```csharp
using VRC.SDK3.Persistence;

// 整数家族
PlayerData.SetSByte(player, "key", (sbyte)-1);
PlayerData.SetByte(player, "key", (byte)255);
PlayerData.SetShort(player, "key", (short)-1000);
PlayerData.SetUShort(player, "key", (ushort)1000);
PlayerData.SetInt(player, "key", 42);
PlayerData.SetUInt(player, "key", 42u);
PlayerData.SetLong(player, "key", 42L);
PlayerData.SetULong(player, "key", 42ul);

// 浮点
PlayerData.SetFloat(player, "key", 3.14f);
PlayerData.SetDouble(player, "key", 3.14159);

// 向量 / 颜色 / 旋转
PlayerData.SetVector2(player, "key", new Vector2(1, 2));
PlayerData.SetVector3(player, "key", new Vector3(1, 2, 3));
PlayerData.SetVector4(player, "key", new Vector4(1, 2, 3, 4));
PlayerData.SetQuaternion(player, "key", Quaternion.identity);
PlayerData.SetColor(player, "key", Color.red);
PlayerData.SetColor32(player, "key", new Color32(255, 0, 0, 255));

// 字符串 / 布尔
PlayerData.SetString(player, "key", "hello");
PlayerData.SetBool(player, "key", true);

// 字节数组(自定义序列化)
PlayerData.SetBytes(player, "key", new byte[] { 0x01, 0x02 });
```

### 写入的 5 个关键事实

1. **类型可变**:同 key 可以从 int 改为 string(覆盖即可)
2. **不能删除 key**:只能 Set 一个新值(可为空字符串或 0)
3. **只能写本地玩家**:`player` 参数必须是 `Networking.LocalPlayer`
4. **批量写入合并**:一帧内多次 Set → 一起发送(类似 Manual Sync)
5. **写入即同步**:远程玩家会通过 `OnPlayerDataUpdated` 收到通知

---

## 读取(Accessors)完整列表

> 17 对 `Get*` / `TryGet*`。`Get*` 返回默认值,`TryGet*` 返回是否存在的 bool。

```csharp
// 读取:使用 TryGet 区分"默认值"和"key 不存在"
bool exists = PlayerData.TryGetInt(Networking.LocalPlayer, "score", out int score);
if (!exists) {
    score = 0;  // key 不存在
}

// ❌ Get* 在 key 不存在时返回默认值(无法区分"未设置"和"显式设为 0")
int value = PlayerData.GetInt(player, "score");  // key 不存在 → 返回 0
```

### 跨玩家读取

```csharp
// 任何 Udon 脚本可读任何玩家的 PlayerData(只要该玩家已 OnPlayerRestored)
public override void OnPlayerDataUpdated(VRCPlayerApi player, PlayerData.Info[] infos) {
    if (player == Networking.LocalPlayer) {
        // 本地玩家的数据变化 - 处理 UI 更新
        UpdateLocalUI();
    } else {
        // 远程玩家数据变化 - 排行榜/成就系统
        UpdateLeaderboardSlot(player);
    }
}
```

---

## 查询(Queries)

```csharp
// HasKey - 检查 key 是否存在
if (PlayerData.HasKey(player, "score")) {
    // ...
}

// GetType - 获取 key 的类型(Type 对象)
System.Type t = PlayerData.GetType(player, "score");
if (t == typeof(int)) { /* ... */ }

// TryGetType - 安全的类型查询
if (PlayerData.TryGetType(player, "score", out System.Type t, out bool success)) {
    Debug.Log($"score 类型: {t}");
}
```

---

## 18 个事件

> 完整事件列表见 `../index.md#5-个-persistence-事件速查`。最常用 3 个:

| 事件 | 用途 | 重要参数 |
|------|------|---------|
| `OnPlayerRestored(VRCPlayerApi player)` | 数据加载完成 | 必须在所有读写前等待 |
| `OnPlayerDataUpdated(VRCPlayerApi, PlayerData.Info[])` | 帧末数据更新 | `infos[i].State` 描述变更类型 |
| `OnPlayerDataStorageExceeded(VRCPlayerApi)` | 超出配额 | 数据未保存,提示用户 |

### `OnPlayerDataUpdated` 的 `Info.State` 5 状态

```csharp
public override void OnPlayerDataUpdated(VRCPlayerApi player, PlayerData.Info[] infos) {
    foreach (var info in infos) {
        switch ((int)info.State) {
            case 0:  // Unchanged - 未变化
                break;
            case 1:  // Added - 新增 key
                break;
            case 2:  // Removed - key 被删除(当前 API 不支持删除,预留)
                break;
            case 3:  // Changed - 值变化
                HandleChange(player, info.Key);
                break;
            case 4:  // Restored - 从服务器恢复(玩家重新加入)
                HandleRestore(player, info.Key);
                break;
        }
    }
}
```

> **Iterating 慢**:如果超过 10 个 key,直接用 `TryGet*` 检查目标 key(避免遍历)

---

## 存储信息(SDK 3.10+)

```csharp
using VRC.SDKBase;

// 常量查询
int dataLimit = player.GetPlayerDataStorageLimit();  // 100 * 1024 = 102400

// 当前用量(可能过期)
int used = player.GetPlayerDataStorageUsage();

// 异步更新
player.RequestStorageUsageUpdate();
// 结果在 OnPersistenceUsageUpdated 中获取
public override void OnPersistenceUsageUpdated(VRCPlayerApi player) {
    int newUsed = player.GetPlayerDataStorageUsage();
    int limit = player.GetPlayerDataStorageLimit();
    if (newUsed > limit * 0.9f) {
        Debug.LogWarning("PlayerData 用量超过 90%");
    }
}
```

---

## 完整实战模板(Master 写入 + 所有人读取)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.SDK3.Persistence;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PlayerDataManager : UdonSharpBehaviour {
    [UdonSynced] private bool _dataReady = false;
    [UdonSynced] private int _score = 0;
    
    // 1. 本地玩家数据加载完成后
    public override void OnPlayerRestored(VRCPlayerApi player) {
        if (player != Networking.LocalPlayer) return;
        // 读本地数据
        if (PlayerData.TryGetInt(Networking.LocalPlayer, "score", out int saved)) {
            _score = saved;
        } else {
            _score = 0;
        }
        _dataReady = true;
    }
    
    // 2. 写本地数据(本地玩家触发,例如跳跃加分)
    public void AddScore(int amount) {
        if (!_dataReady) return;  // 守卫
        _score += amount;
        PlayerData.SetInt(Networking.LocalPlayer, "score", _score);
    }
    
    // 3. 所有人接收 OnPlayerDataUpdated(框架末尾统一触发)
    public override void OnPlayerDataUpdated(VRCPlayerApi player, PlayerData.Info[] infos) {
        // 更新 UI
        if (player == Networking.LocalPlayer) {
            // 本地 UI
            UpdateLocalScoreUI();
        } else {
            // 排行榜槽位
            UpdateLeaderboardSlot(player);
        }
    }
}
```

---

## PlayerData.Info 完整结构

```csharp
public class PlayerData.Info {
    public string Key { get; }   // key 名
    public State State { get; }  // 状态枚举(Unchanged/Added/Removed/Changed/Restored)
}
```

---

## 4 个常见陷阱

| 陷阱 | 症状 | 修复 |
|------|------|------|
| `OnPlayerJoined` 写数据 | 写入"成功"但被服务器拉来的数据覆盖 | 改用 `OnPlayerRestored` 守卫 |
| 用 `Get*` 读取稀疏 key | 无法区分"未设置"和"显式设为默认值" | 改用 `TryGet*` |
| 高频 Set(每帧 60 次) | `IsClogged = true`,全局网络拥塞 | 走 PlayerObject 或降频 |
| 多个 Prefab 共享 key 名 | 数据互相覆盖 | 用 `<Prefab名>-<功能>` 前缀 |

---

## 关键 API vs 限制速查

| 维度 | 限制 |
|------|------|
| 配额 | 100 KB / 玩家 / World(压缩后) |
| 原始数据 | ~300 KB(高度可压缩时) |
| Key 长度 | 128 字符(建议值) |
| String 值 | ~50 字符(建议值) |
| Key 删除 | ❌ 不支持(只能 Set 覆盖) |
| 写入目标 | 只能写本地玩家 |
| 同步开销 | 写一次 = 发全部 PlayerData(类似 Manual Sync) |
| Late Joiner | 自动获取最新值 |

---

## 实战示例(本目录内)

- [patterns/leaderboard.md](./patterns/leaderboard.md) - 排行榜
- [patterns/unlock-items.md](./patterns/unlock-items.md) - 解锁物品/成就
- [patterns/persistent-pen.md](./patterns/persistent-pen.md) - 持久画笔(用 PlayerObject)

---

## 相关知识库

- `memory/api/persistence.md` - 完整 API 速查
- `memory/world/examples/persistence/leaderboard.md` - 排行榜 Example Central 笔记
- `memory/world/examples/persistence/persistent-idle-game.md` - Idle Game 笔记
- `memory/world/examples/persistence/unlock-items.md` - 解锁物品笔记
- `memory/patterns/late-joiner-state-restore.md` - Late Joiner 状态恢复模式
- `memory/rules/networking-rules.md` - 网络同步规则
