---
title: 解锁物品实现(Pattern)
category: world
subcategory: udon/persistence/patterns
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - patterns
  - unlock
  - achievement
  - inventory
aliases:
  - 解锁物品
  - Unlock Items
  - 成就系统
  - Achievement System
related:
  - ../../../../api/persistence.md
  - ../../index.md
  - ../player-data.md
  - ../serialization.md
  - ../limits-and-quirks.md
  - ../../../examples/persistence/unlock-items.md
  - ../../../examples/persistence/persistent-idle-game.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/examples/persistence/unlock-items/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# 解锁物品实现(Pattern)

> 数据层:**PlayerData**(简单 key-value)
> 关键 API:`PlayerData.SetBool` + `OnPlayerRestored`
> 官方示例:https://creators.vrchat.com/worlds/examples/persistence/unlock-items/
> 适用 SDK:3.7+ / UdonSharp C#

---

## 概述

解锁系统(Achievement/Unlock System)是 PlayerData 的另一经典应用:
- **数据小**:每个解锁 1 个 bool
- **跨设备**:PC 解锁 → Quest 看到
- **持久化**:玩家离开后重新加入仍能看到解锁状态
- **成就触发**:基于时间、距离、事件等条件

**官方示例**:5 大成就 + 2 个统计指标(停留时间、移动距离)

| 成就 | 类型 | 条件 |
|------|------|------|
| 探索者 | 时间 | 在 World 中停留 10 秒 |
| 旅人 | 时间 | 停留 2 分钟 |
| 老兵 | 时间 | 停留 5 分钟 |
| 漫步者 | 距离 | 移动 10 单位 |
| 旅行者 | 距离 | 移动 100 单位 |
| 漫游者 | 距离 | 移动 300 单位 |
| 重生者 | 事件 | 玩家重生 |
| 秘密发现者 | 事件 | 找到隐藏触发器 |
| 完美主义 | 综合 | 全部解锁 |

---

## 完整实现

### 架构

```
UnlockItemsManager (场景级,1 个)
├── 9 个成就槽位(UI Image + Text)
├── 2 个统计指标(时间、距离)
└── UpdateStats() 循环检测

玩家操作
├── 移动 / 跳跃 / 触发
└── UnlockItemsManager 检测条件
    ↓
PlayerData.SetBool 写入
    ↓
OnPlayerDataUpdated 触发
    ↓
所有玩家的 UI 更新
```

### 文件 1:UnlockItemsManager.cs

```csharp
using UdonSharp;
using UnityEngine;
using UnityEngine.UI;
using VRC.SDKBase;
using VRC.SDK3.Persistence;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class UnlockItemsManager : UdonSharpBehaviour {
    [Header("Configuration")]
    [SerializeField] private string achievementKeyPrefix = "Unlocks-Achievement-";
    [SerializeField] private string timeKey = "Unlocks-Time-In-World";
    [SerializeField] private string distanceKey = "Unlocks-Distance-Traveled";
    [SerializeField] private string respawnKey = "Unlocks-Has-Respawned";
    [SerializeField] private string secretKey = "Unlocks-Found-Secret";
    
    [SerializeField] private float updateStatsInterval = 1f;  // 每秒检查一次
    
    [Header("Thresholds")]
    [SerializeField] private float[] timeThresholds = { 10f, 120f, 300f };
    [SerializeField] private float[] distanceThresholds = { 10f, 100f, 300f };
    
    [Header("UI References")]
    [SerializeField] private Image[] achievementIcons;
    [SerializeField] private Text[] achievementTexts;
    [SerializeField] private Text timeStatText;
    [SerializeField] private Text distanceStatText;
    [SerializeField] private Sprite lockedSprite;
    [SerializeField] private Sprite unlockedSprite;
    [SerializeField] private Color lockedColor = Color.gray;
    [SerializeField] private Color unlockedColor = Color.white;
    
    // Local state
    private bool _dataReady = false;
    private float _timeInWorld = 0f;
    private float _distanceTraveled = 0f;
    private Vector3 _lastPosition;
    private int _respawnCount = 0;
    private bool _foundSecret = false;
    
    public override void OnPlayerRestored(VRCPlayerApi player) {
        if (player != Networking.LocalPlayer) return;
        _dataReady = true;
        
        // 加载统计数据
        PlayerData.TryGetFloat(Networking.LocalPlayer, timeKey, out _timeInWorld);
        PlayerData.TryGetFloat(Networking.LocalPlayer, distanceKey, out _distanceTraveled);
        PlayerData.TryGetInt(Networking.LocalPlayer, respawnKey, out _respawnCount);
        PlayerData.TryGetBool(Networking.LocalPlayer, secretKey, out _foundSecret);
        
        // 记录当前位置(用于距离计算)
        if (Networking.LocalPlayer != null) {
            _lastPosition = Networking.LocalPlayer.GetPosition();
        }
        
        // 启动统计更新循环
        SendCustomEventDelayedSeconds(nameof(UpdateStats), updateStatsInterval);
        
        // 初始 UI 更新
        UpdateAllUI();
    }
    
    // 每秒调用一次
    public void UpdateStats() {
        if (!_dataReady) return;
        if (Networking.LocalPlayer == null) return;
        
        // 1. 时间统计
        _timeInWorld += updateStatsInterval;
        PlayerData.SetFloat(Networking.LocalPlayer, timeKey, _timeInWorld);
        CheckTimeAchievements();
        
        // 2. 距离统计
        Vector3 currentPos = Networking.LocalPlayer.GetPosition();
        float distance = Vector3.Distance(currentPos, _lastPosition);
        _distanceTraveled += distance;
        PlayerData.SetFloat(Networking.LocalPlayer, distanceKey, _distanceTraveled);
        _lastPosition = currentPos;
        CheckDistanceAchievements();
        
        // 3. 更新 UI
        UpdateAllUI();
        
        // 4. 重新调度
        SendCustomEventDelayedSeconds(nameof(UpdateStats), updateStatsInterval);
    }
    
    private void CheckTimeAchievements() {
        for (int i = 0; i < timeThresholds.Length; i++) {
            if (_timeInWorld >= timeThresholds[i]) {
                UnlockAchievement(i);
            }
        }
    }
    
    private void CheckDistanceAchievements() {
        for (int i = 0; i < distanceThresholds.Length; i++) {
            if (_distanceTraveled >= distanceThresholds[i]) {
                UnlockAchievement(timeThresholds.Length + i);  // 3-5
            }
        }
    }
    
    // 玩家重生时调用(从 Scene Descriptor 的 Respawn 事件)
    public void OnPlayerRespawned() {
        if (!_dataReady) return;
        _respawnCount++;
        PlayerData.SetInt(Networking.LocalPlayer, respawnKey, _respawnCount);
        UnlockAchievement(timeThresholds.Length + distanceThresholds.Length);  // 6
    }
    
    // 玩家找到秘密触发器时调用
    public void OnSecretFound() {
        if (!_dataReady) return;
        _foundSecret = true;
        PlayerData.SetBool(Networking.LocalPlayer, secretKey, _foundSecret);
        UnlockAchievement(timeThresholds.Length + distanceThresholds.Length + 1);  // 7
    }
    
    private void UnlockAchievement(int index) {
        if (!_dataReady) return;
        if (index < 0 || index >= achievementIcons.Length) return;
        
        string key = $"{achievementKeyPrefix}{index}";
        
        // 检查是否已解锁
        if (PlayerData.TryGetBool(Networking.LocalPlayer, key, out bool unlocked) && unlocked) {
            return;  // 已解锁
        }
        
        // 写入解锁
        PlayerData.SetBool(Networking.LocalPlayer, key, true);
        
        // 检查"完美主义"成就
        CheckAllAchievementsUnlocked();
    }
    
    private void CheckAllAchievementsUnlocked() {
        int total = achievementIcons.Length;
        int unlockedCount = 0;
        for (int i = 0; i < total; i++) {
            string key = $"{achievementKeyPrefix}{i}";
            if (PlayerData.TryGetBool(Networking.LocalPlayer, key, out bool unlocked) && unlocked) {
                unlockedCount++;
            }
        }
        if (unlockedCount >= total) {
            UnlockAchievement(total - 1);  // 最后一个 = 完美主义
        }
    }
    
    public override void OnPlayerDataUpdated(VRCPlayerApi player, PlayerData.Info[] infos) {
        if (player != Networking.LocalPlayer) return;
        UpdateAllUI();
    }
    
    private void UpdateAllUI() {
        if (!_dataReady) return;
        
        // 成就图标 + 文字
        int total = achievementIcons.Length;
        for (int i = 0; i < total; i++) {
            string key = $"{achievementKeyPrefix}{i}";
            bool unlocked = false;
            PlayerData.TryGetBool(Networking.LocalPlayer, key, out unlocked);
            
            if (achievementIcons[i] != null) {
                achievementIcons[i].sprite = unlocked ? unlockedSprite : lockedSprite;
                achievementIcons[i].color = unlocked ? unlockedColor : lockedColor;
            }
            if (achievementTexts[i] != null) {
                achievementTexts[i].color = unlocked ? unlockedColor : lockedColor;
            }
        }
        
        // 统计指标
        if (timeStatText != null) {
            timeStatText.text = FormatTime(_timeInWorld);
        }
        if (distanceStatText != null) {
            distanceStatText.text = $"{_distanceTraveled:F1} m";
        }
    }
    
    private string FormatTime(float seconds) {
        int total = (int)seconds;
        int hours = total / 3600;
        int minutes = (total % 3600) / 60;
        int secs = total % 60;
        if (hours > 0) return $"{hours}h {minutes}m {secs}s";
        if (minutes > 0) return $"{minutes}m {secs}s";
        return $"{secs}s";
    }
}
```

### 文件 2:SecretTrigger.cs(找到秘密)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class SecretTrigger : UdonSharpBehaviour {
    [SerializeField] private UnlockItemsManager manager;
    [SerializeField] private string playerTag = "SecretFound";  // 防重复
    
    public override void OnPlayerTriggerEnter(VRCPlayerApi player) {
        if (player != Networking.LocalPlayer) return;
        if (manager == null) return;
        // 简单防重
        // (实际可用 PlayerData 标记)
        manager.OnSecretFound();
    }
}
```

### 文件 3:SceneDescriptorHook.cs(重生事件)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class SceneDescriptorHook : UdonSharpBehaviour {
    [SerializeField] private UnlockItemsManager manager;
    
    public override void OnPlayerRespawn(VRCPlayerApi player) {
        if (player == Networking.LocalPlayer && manager != null) {
            manager.OnPlayerRespawned();
        }
    }
}
```

---

## 关键设计点

### 1. 数据存储策略

| 数据 | 类型 | Key | 默认值 |
|------|------|-----|--------|
| 时间统计 | float | `Unlocks-Time-In-World` | 0 |
| 距离统计 | float | `Unlocks-Distance-Traveled` | 0 |
| 重生次数 | int | `Unlocks-Has-Respawned` | 0 |
| 找到秘密 | bool | `Unlocks-Found-Secret` | false |
| 成就 0-8 | bool | `Unlocks-Achievement-0` ~ `Unlocks-Achievement-8` | false |

**总配额**:~9 bool + 2 float + 1 int + 1 bool ≈ 30 字节(远低于 100KB)

### 2. 命名空间

> ⚠️ 全部用 `Unlocks-` 前缀,**避免与其他 Prefab 冲突**

```
✅ Unlocks-Achievement-0
✅ Unlocks-Time-In-World
❌ Achievement-0       (易冲突)
❌ Time                (太通用)
```

### 3. 时间累加的实现

```csharp
// ✅ 正确:累加 + 写入(玩家离开时仍保留累加值)
_timeInWorld += updateStatsInterval;
PlayerData.SetFloat(Networking.LocalPlayer, timeKey, _timeInWorld);

// ❌ 错误:每次重置为 0(玩家重新进入时丢失)
_timeInWorld = 0;  // 错!会覆盖 PlayerData 中已保存的值
```

> **关键**:`OnPlayerRestored` 中先 `TryGetFloat` 读取旧值,再累加。否则会覆盖。

### 4. 距离计算

```csharp
// ✅ 正确:每帧记录位置,每秒计算距离
private Vector3 _lastPosition;

public override void OnPlayerRestored(VRCPlayerApi player) {
    // 记录初始位置
    _lastPosition = Networking.LocalPlayer.GetPosition();
}

public void UpdateStats() {
    Vector3 currentPos = Networking.LocalPlayer.GetPosition();
    float distance = Vector3.Distance(currentPos, _lastPosition);
    _distanceTraveled += distance;
    _lastPosition = currentPos;
}
```

### 5. 周期性更新 vs 事件驱动

| 模式 | 优点 | 缺点 |
|------|------|------|
| **周期性更新**(每秒) | 简单,统一处理 | 持续 CPU 开销 |
| **事件驱动**(跳跃/移动) | 高效 | 需要 hook 多个事件 |

> **官方示例选择周期性更新** - 简单优先。

---

## 性能优化

### 避免每帧写入

```csharp
// ✅ 官方做法:每秒一次
public void UpdateStats() {
    SendCustomEventDelayedSeconds(nameof(UpdateStats), updateStatsInterval);
}
```

### 避免遍历所有成就

```csharp
// ❌ 错误:每次 Set 都遍历所有成就
private void UnlockAchievement(int index) {
    PlayerData.SetBool(...);
    for (int i = 0; i < 9; i++) {
        if (PlayerData.TryGetBool(...)) unlockedCount++;
    }
}

// ✅ 优化:维护本地 Set
private bool[] _localUnlocked = new bool[9];

private void UnlockAchievement(int index) {
    if (_localUnlocked[index]) return;
    _localUnlocked[index] = true;
    PlayerData.SetBool(Networking.LocalPlayer, $"{keyPrefix}{index}", true);
}
```

---

## Late Joiner 处理

> **自动处理** - PlayerData 内置 Late Joiner 恢复

**新玩家进入**:
1. `OnPlayerJoined` 触发
2. VRChat 服务器发 **该玩家已有的全部 PlayerData**
3. `OnPlayerRestored` 触发 → `TryGetFloat/TryGetBool/TryGetInt` 读取
4. UI 自动更新

> 看到"刚进入就显示自己之前的成就" - 这就是 Late Joiner 体验。

---

## 跨设备同步(再次强调)

```
PC 上探索 5 分钟,解锁"老兵"成就
    ↓
关闭 VRChat
    ↓
Quest 上重新打开 VRChat,进入同一 World
    ↓
OnPlayerRestored → TryGetBool("Unlocks-Achievement-2") = true
    ↓
UI 显示已解锁"老兵"成就
    ↓
无需任何额外代码
```

---

## 完整文件清单

```
Assets/
└── UnlockItems/
    ├── UnlockItemsManager.cs        ← 场景级核心
    ├── SecretTrigger.cs             ← 触发器
    ├── SceneDescriptorHook.cs       ← 重生 hook
    ├── UnlockItemsCanvas.prefab     ← UI 画布
    │   ├── 9 个 Image + Text (成就槽)
    │   ├── 2 个 Text (时间/距离)
    │   └── 锁定/解锁 Sprite
    └── AchievementsConfig.asset     ← ScriptableObject(可选,放阈值)
```

---

## 测试清单

- [ ] 客户端本地测试(ClientSim PlayerData 窗口)
- [ ] Build & Test 多客户端
- [ ] PC → Quest 跨设备
- [ ] 玩家离开 → 重新进入,数据保留
- [ ] 玩家断网 → 重连,数据保留
- [ ] 重置数据(VRChat 菜单)后所有成就清零
- [ ] 玩家达到"完美主义"成就(全部解锁)

---

## 拓展应用

### 物品库存(Inventory)

```csharp
// 物品 ID 用 int 编码(节省空间)
public void AddItem(int itemId) {
    if (!_dataReady) return;
    string key = $"Inventory-Item-{itemId}";
    PlayerData.SetBool(Networking.LocalPlayer, key, true);
}

public bool HasItem(int itemId) {
    string key = $"Inventory-Item-{itemId}";
    PlayerData.TryGetBool(Networking.LocalPlayer, key, out bool has);
    return has;
}

// 列出所有物品
public int[] GetAllItems() {
    string[] keys = PlayerData.GetKeys(Networking.LocalPlayer);
    DataList items = new DataList();
    foreach (string key in keys) {
        if (key.StartsWith("Inventory-Item-")) {
            int itemId = int.Parse(key.Substring("Inventory-Item-".Length));
            items.Add(itemId);
        }
    }
    return items.ToArray();
}
```

### 商店(Shop)

```csharp
public bool PurchaseItem(int itemId, int price) {
    if (!_dataReady) return false;
    
    string currencyKey = "Shop-Currency";
    PlayerData.TryGetInt(Networking.LocalPlayer, currencyKey, out int currency);
    if (currency < price) return false;
    
    currency -= price;
    PlayerData.SetInt(Networking.LocalPlayer, currencyKey, currency);
    PlayerData.SetBool(Networking.LocalPlayer, $"Shop-Owns-{itemId}", true);
    return true;
}
```

---

## 相关知识库

- `memory/api/persistence.md` - API 速查
- `memory/world/udon/persistence/player-data.md` - PlayerData 详细 API
- `memory/world/udon/persistence/limits-and-quirks.md` - 100KB 限制
- `memory/world/examples/persistence/unlock-items.md` - 官方 Example Central 笔记
- `memory/world/examples/persistence/persistent-idle-game.md` - Idle Game(类似模式)
- `memory/world/udon/persistence/patterns/leaderboard.md` - 排行榜模式
