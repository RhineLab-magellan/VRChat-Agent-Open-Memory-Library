---
title: 排行榜实现(Pattern)
category: world
subcategory: udon/persistence/patterns
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - patterns
  - leaderboard
  - playerdata
  - score
aliases:
  - 排行榜实现
  - Leaderboard Pattern
  - 高分榜
related:
  - ../../../../api/persistence.md
  - ../../index.md
  - ../player-data.md
  - ../serialization.md
  - ../limits-and-quirks.md
  - ../../../examples/persistence/leaderboard.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/examples/persistence/leaderboard/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# 排行榜实现(Pattern)

> 数据层:**PlayerData**(跨设备同步 + 所有人可见)
> 关键 API:`PlayerData.SetFloat/TryGetFloat` + `OnPlayerDataUpdated`
> 官方示例:https://creators.vrchat.com/worlds/examples/persistence/leaderboard/
> 适用 SDK:3.7+ / UdonSharp C#

---

## 概述

排行榜(Leaderboard)是 PlayerData 的经典应用:
- **数据小**:每个玩家 1 个 float
- **跨设备**:PC 跳跃加分 → Quest rejoin 数据保留
- **所有人可见**:每位玩家的最新分数会同步给所有其他玩家
- **Late Joiner**:自动恢复所有玩家分数

**架构**:
- 1 个 `LeaderboardManager` 脚本(场景级)
- 1 个 `LeaderboardSlot` Prefab(每个玩家的 PlayerObject,RectTransform)
- Scroll View 容器(自动排序)

---

## 完整实现(简化版,生产可用)

### 文件 1:LeaderboardManager.cs

```csharp
using System;
using UdonSharp;
using UnityEngine;
using UnityEngine.UI;
using VRC.SDKBase;
using VRC.SDK3.Persistence;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class LeaderboardManager : UdonSharpBehaviour {
    [Header("Configuration")]
    [Tooltip("PlayerData key for the high score")]
    [SerializeField] private string scoreKey = "Leaderboard-Score";
    
    [Tooltip("Maximum number of leaderboard slots")]
    [SerializeField] private int maxSlots = 20;
    
    [Header("UI References")]
    [SerializeField] private RectTransform slotContainer;  // Scroll View content
    [SerializeField] private GameObject slotPrefab;        // LeaderboardSlot prefab
    [SerializeField] private Text titleText;
    
    // Local data
    private VRCPlayerApi[] _cachedPlayers = new VRCPlayerApi[20];
    private float[] _cachedScores = new float[20];
    private int _playerCount = 0;
    private bool _initialized = false;
    
    public override void OnPlayerRestored(VRCPlayerApi player) {
        if (player != Networking.LocalPlayer) return;
        _initialized = true;
        RefreshAllSlots();
    }
    
    public override void OnPlayerDataUpdated(VRCPlayerApi player, PlayerData.Info[] infos) {
        // 检查是否变更了 score key
        bool scoreChanged = false;
        foreach (var info in infos) {
            if (info.Key == scoreKey) {
                scoreChanged = true;
                break;
            }
        }
        if (scoreChanged) {
            RefreshAllSlots();
        }
    }
    
    public override void OnPlayerJoined(VRCPlayerApi player) {
        RefreshAllSlots();
    }
    
    public override void OnPlayerLeft(VRCPlayerApi player) {
        RefreshAllSlots();
    }
    
    public void RefreshAllSlots() {
        if (!_initialized) return;
        
        // 1. 收集所有玩家 + 分数
        VRCPlayerApi[] players = VRCPlayerApi.GetPlayers(new VRCPlayerApi[VRCPlayerApi.GetPlayerCount()]);
        _playerCount = players.Length;
        
        for (int i = 0; i < _playerCount; i++) {
            _cachedPlayers[i] = players[i];
            if (PlayerData.TryGetFloat(players[i], scoreKey, out float score)) {
                _cachedScores[i] = score;
            } else {
                _cachedScores[i] = 0f;
            }
        }
        
        // 2. 排序(降序)
        SortPlayersByScore();
        
        // 3. 重建 Scroll View slots
        RebuildSlots();
    }
    
    private void SortPlayersByScore() {
        // 简单冒泡排序(玩家数量通常 < 20)
        for (int i = 0; i < _playerCount - 1; i++) {
            for (int j = 0; j < _playerCount - i - 1; j++) {
                if (_cachedScores[j] < _cachedScores[j + 1]) {
                    // Swap scores
                    float tempScore = _cachedScores[j];
                    _cachedScores[j] = _cachedScores[j + 1];
                    _cachedScores[j + 1] = tempScore;
                    // Swap players
                    VRCPlayerApi tempPlayer = _cachedPlayers[j];
                    _cachedPlayers[j] = _cachedPlayers[j + 1];
                    _cachedPlayers[j + 1] = tempPlayer;
                }
            }
        }
    }
    
    private void RebuildSlots() {
        // 清理现有 slots
        for (int i = slotContainer.childCount - 1; i >= 0; i--) {
            DestroyImmediate(slotContainer.GetChild(i).gameObject);
        }
        
        // 创建新 slots(按排序顺序)
        for (int i = 0; i < _playerCount && i < maxSlots; i++) {
            GameObject slotObj = Instantiate(slotPrefab, slotContainer);
            LeaderboardSlot slot = slotObj.GetComponent<LeaderboardSlot>();
            if (slot != null) {
                slot.SetData(i + 1, _cachedPlayers[i], _cachedScores[i]);
            }
        }
    }
}
```

### 文件 2:LeaderboardSlot.cs(PlayerObject)

```csharp
using UdonSharp;
using UnityEngine;
using UnityEngine.UI;
using VRC.SDKBase;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class LeaderboardSlot : UdonSharpBehaviour {
    [SerializeField] private Text rankText;
    [SerializeField] private Text nameText;
    [SerializeField] private Text scoreText;
    
    [UdonSynced] private int _rank = 0;
    [UdonSynced] private string _playerName = "";
    [UdonSynced] private float _score = 0f;
    
    // 防止重复创建
    public override void OnPlayerRestored(VRCPlayerApi player) {
        if (!Networking.IsOwner(gameObject)) return;
        // 数据已加载,可以渲染
        UpdateUI();
    }
    
    public void SetData(int rank, VRCPlayerApi player, float score) {
        if (!Networking.IsOwner(gameObject)) return;
        
        _rank = rank;
        _playerName = player.displayName;
        _score = score;
        RequestSerialization();
        UpdateUI();
    }
    
    public override void OnDeserialization() {
        UpdateUI();
    }
    
    private void UpdateUI() {
        if (rankText != null) rankText.text = $"#{_rank}";
        if (nameText != null) nameText.text = _playerName;
        if (scoreText != null) scoreText.text = $"{_score:F0}";
    }
}
```

### 文件 3:ScoreSubmitter.cs(玩家本地加分)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.SDK3.Persistence;

public class ScoreSubmitter : UdonSharpBehaviour {
    [SerializeField] private string scoreKey = "Leaderboard-Score";
    [SerializeField] private int pointsPerJump = 1;
    
    private bool _dataReady = false;
    private float _currentScore = 0f;
    
    public override void OnPlayerRestored(VRCPlayerApi player) {
        if (player != Networking.LocalPlayer) return;
        _dataReady = true;
        
        if (PlayerData.TryGetFloat(Networking.LocalPlayer, scoreKey, out float saved)) {
            _currentScore = saved;
        } else {
            _currentScore = 0f;
        }
    }
    
    // 玩家跳跃时调用
    public void OnPlayerJumped() {
        if (!_dataReady) return;
        _currentScore += pointsPerJump;
        PlayerData.SetFloat(Networking.LocalPlayer, scoreKey, _currentScore);
    }
}
```

---

## 关键设计点

### 1. PlayerObject 作为 Slot

**为什么用 PlayerObject 作为 LeaderboardSlot?**
- 每个玩家自动生成一个 slot
- 玩家离开 → slot 自动销毁
- 玩家重新加入 → 自动重建

**Prefab 结构**:
```
LeaderboardSlot (GameObject - RectTransform)
├── VRCPlayerObject          (组件)
├── VRCEnablePersistence    (组件 - 持久化 _rank, _playerName, _score)
└── UdonBehaviour            (组件 - LeaderboardSlot.cs)
    ├── [UdonSynced] int _rank
    ├── [UdonSynced] string _playerName
    └── [UdonSynced] float _score
```

### 2. 排序在场景中

- 每个 slot 是 Scroll View 的子节点
- Vertical Layout Group + Content Size Fitter 让子节点按层级顺序排序
- 改变 slot 在层级中的位置 = 改变显示顺序

### 3. 数据流

```
玩家跳跃 (本地)
    ↓
ScoreSubmitter.OnPlayerJumped()
    ↓
PlayerData.SetFloat(localPlayer, "score", newScore)
    ↓
VRChat 同步(帧末)
    ↓
所有玩家的 OnPlayerDataUpdated() 触发
    ↓
LeaderboardManager.RefreshAllSlots()
    ↓
重排 slots(在层级中的位置)
    ↓
UI 自动更新(Vertical Layout Group)
```

---

## 性能优化

### 避免频繁排序

```csharp
// ❌ 错误:每次 Set 都排序
public void OnPlayerDataUpdated(...) {
    SortPlayersByScore();  // 即使只有 1 个玩家分数变化
    RebuildSlots();
}

// ✅ 优化:阈值触发
private float _lastRefresh = 0;
public void OnPlayerDataUpdated(...) {
    if (Time.time - _lastRefresh < 1f) return;  // 1 秒内不重复刷新
    _lastRefresh = Time.time;
    RefreshAllSlots();
}
```

### 复用 Slot 对象(避免 Instantiate/Destroy)

```csharp
// 用对象池替代 Instantiate/Destroy
[SerializeField] private LeaderboardSlot[] _slotPool = new LeaderboardSlot[20];

private void RebuildSlots() {
    for (int i = 0; i < _playerCount; i++) {
        if (i < _slotPool.Length && _slotPool[i] != null) {
            _slotPool[i].SetData(i + 1, _cachedPlayers[i], _cachedScores[i]);
            _slotPool[i].gameObject.SetActive(true);
        }
    }
    for (int i = _playerCount; i < _slotPool.Length; i++) {
        if (_slotPool[i] != null) {
            _slotPool[i].gameObject.SetActive(false);
        }
    }
}
```

---

## 跨设备同步(核心特性)

> 玩家在 PC 上跳跃 100 次,关闭 VRChat → 在 Quest 上重新加入 → 排行榜仍有 100 分

**实现**:
1. `OnPlayerRestored` 触发 → `PlayerData.TryGetFloat` 读取
2. 数据从 VRChat 服务器自动下载
3. UI 自动更新

**无需任何额外代码** - 这是 PlayerData 的内置功能。

---

## 完整数据流(从开始到结束)

```
[初始状态] 玩家 A 跳了 10 次 → score=10
                          ↓
              PlayerData.SetFloat("score", 10) [本地]
                          ↓
              [VRChat 服务器] <--- 同步
                          ↓
       ┌──────────────────┼──────────────────┐
       ↓                  ↓                  ↓
  玩家 A 本地         玩家 B 客户端      玩家 C 客户端
  (立即可见)         OnPlayerData       OnPlayerData
                     Updated            Updated
                          ↓                  ↓
                  RefreshAllSlots()  RefreshAllSlots()
                          ↓                  ↓
                  UI 更新(从 #X     UI 更新(从 #X
                          ↓
[玩家 A 离开]
       ↓
PlayerObject 自动销毁
       ↓
[玩家 A 在 Quest 重新加入]
       ↓
OnPlayerRestored 触发
       ↓
PlayerData.TryGetFloat("score") → 10
       ↓
ScoreSubmitter._currentScore = 10
       ↓
LeaderboardManager.RefreshAllSlots() → 重建 UI,显示 score=10
       ↓
[Quest 上,玩家 A 看到自己的 10 分]
```

---

## 关键限制与坑

| 限制/坑 | 说明 | 缓解 |
|--------|------|------|
| Slot 是 PlayerObject | 每个玩家只能看到自己的"占位"slot,score 来自同步 | 排序在 Manager(场景级),不是 slot |
| 字符串限制 | 玩家名字 String 值 ~50 字符 | 实际显示名通常 < 30,无问题 |
| 100KB 配额 | 1 个 float 远未触及 | 不担心 |
| 排序算法 | 简单冒泡在 N<20 时 OK | 玩家 > 20 时改归并排序 |
| Late Joiner 看到旧分数 | 这是 **特性** 不是 bug | 玩家期望 "我之前多少分" |

---

## 测试方法

### ClientSim 测试
1. 打开 ClientSim 窗口
2. 进入 Play Mode
3. 跳几次,观察 PlayerData 窗口中的 "Leaderboard-Score" 值
4. 退出 Play Mode
5. 重新进入 → 分数应保留

### Build & Test 测试
1. Build & Test 启动 2 个测试客户端
2. 客户端 1 跳跃 → 客户端 2 看到分数变化
3. 关闭客户端 1 → 客户端 2 的 slot 自动移除
4. 重新 Build & Test → 客户端 1 分数保留

### 已发布 World 测试
1. 上传 World
2. PC + Quest 登录同一账号
3. PC 跳跃 → Quest 退出 → 重新加入 → Quest 看到分数

---

## 完整文件清单(创建此 Pattern 需)

```
Assets/
└── Leaderboard/
    ├── LeaderboardManager.cs        ← 场景级,挂在 Leaderboard GameObject
    ├── ScoreSubmitter.cs            ← 挂在玩家身上(或 Interact 触发)
    ├── LeaderboardSlot.cs           ← 挂在 LeaderboardSlot Prefab
    ├── LeaderboardSlot.prefab       ← PlayerObject Prefab
    │   ├── VRCPlayerObject
    │   ├── VRCEnablePersistence
    │   ├── UdonBehaviour (LeaderboardSlot.cs)
    │   └── Text × 3 (rank/name/score)
    └── LeaderboardCanvas.prefab     ← Scroll View
```

---

## 相关知识库

- `memory/api/persistence.md` - API 速查
- `memory/world/udon/persistence/player-data.md` - PlayerData 详细 API
- `memory/world/udon/persistence/limits-and-quirks.md` - 100KB 限制
- `memory/world/examples/persistence/leaderboard.md` - 官方 Example Central 笔记
- `memory/patterns/late-joiner-state-restore.md` - Late Joiner 模式
- `memory/patterns/master-follower-syncer.md` - Master-Follower 同步模式
