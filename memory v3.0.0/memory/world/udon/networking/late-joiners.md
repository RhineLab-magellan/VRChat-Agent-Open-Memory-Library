---
title: "Late Joiners 迟到玩家同步"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "VRChat 官方 Creator Docs (Late Joiners & Sync Issues)"
source_type: official
version: 1.0
last_review: 2026-06-15
confidence: High
tags:
  - world
  - networking
  - udon
  - sync
  - serialization
  - event
  - udonsharp
aliases:
  - "Late Joiners 迟到玩家同步"
  - late-joiners
related:
  - "world/udon/networking/index.md"
  - "world/udon/networking/events.md"
  - "world/udon/networking/variables.md"
  - "world/udon/networking/ownership.md"
  - "patterns/late-joiner-state-restore.md"
  - "api/networking.md"
---
# Late Joiners 迟到玩家同步

> SDK Version: 3.x
---

## 简介

当玩家加入一个 **已经存在一段时间的实例** 时,他们需要看到当前的 World 状态。VRChat 通过同步系统自动处理大部分场景,但开发者必须设计好 **状态恢复逻辑**,否则 Late Joiners 会看到 **错误或残缺的状态**。

> ⚠️ **这是 VRChat World 中最常见的 Bug 来源之一**——据社区统计,约 30% 的 World Bug 与 Late Joiner 同步相关。

---

## VRChat 如何处理 Late Joiners

当新玩家加入实例时,VRChat 自动执行:

| 步骤 | 说明 |
|------|------|
| **1. 同步变量值** | 通过 `OnDeserialization` 事件发送最新 `[UdonSynced]` 变量 |
| **2. 分配对象 Owner** | 根据当前所有权状态,告知新玩家每个对象的 Owner |
| **3. 不重放事件** | 已发生过的 Network Events **不会** 重发给新玩家 |

### 关键含义

```
Late Joiner 的体验:
  ✅ 看到所有 [UdonSynced] 变量的最新值
  ✅ 看到正确的对象 Owner
  ❌ 看不到已发生的 Network Event(粒子、音效、动画)
```

> **设计含义**:**任何关键状态都必须用 `[UdonSynced]` 变量,不能用 Network Event**。

---

## 三种 Late Joiner 同步策略

### 策略 1:用 Synced 变量(推荐,最常用)

> 适合:**关键状态、玩家可观察的状态**。

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Door : UdonSharpBehaviour {
    [SerializeField, UdonSynced] private bool isDoorClosed;
    
    public void OpenDoor() {
        isDoorClosed = false;
        RequestSerialization();  // 同步给所有人(包括未来加入的玩家)
    }
}
```

**Late Joiner 表现**:加入时收到 `isDoorClosed = false`,门保持打开。

### 策略 2:在 `OnDeserialization` 中应用状态

> 适合:**收到变量后需要应用表现**(开关门动画、UI 更新)。

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Continuous)]
public class DoorVisual : UdonSharpBehaviour {
    [SerializeField] private GameObject lockedDoor;
    [UdonSynced] private bool isDoorClosed;
    
    public override void OnDeserialization() {
        // Late Joiner 加入时,这里被调用一次
        // 应用门的状态
        lockedDoor.SetActive(isDoorClosed);
    }
}
```

**Late Joiner 表现**:加入时 `OnDeserialization` 触发,门立即显示正确状态。

### 策略 3:Event + Variable 组合(Owner 模式)

> 适合:**任何玩家都可交互**,但状态由 Owner 决定。

```csharp
public class Door : UdonSharpBehaviour {
    [UdonSynced] private bool isDoorClosed;
    
    public override void Interact() {
        // 任何玩家交互:通知 Owner 改状态
        SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(RequestToggle));
    }
    
    [NetworkCallable(maxEventsPerSecond: 5)]
    public void RequestToggle() {
        if (!Networking.IsOwner(gameObject)) return;
        isDoorClosed = !isDoorClosed;
        RequestSerialization();
    }
}
```

**Late Joiner 表现**:加入时收到 `isDoorClosed` 当前值,门状态正确。

---

## 关键反模式(绝对避免)

### 反模式 1:用 Event 同步状态

```csharp
// ❌ 致命错误:Late Joiner 看不到
public class Door : UdonSharpBehaviour {
    public override void Interact() {
        SendCustomNetworkEvent(NetworkEventTarget.All, nameof(OpenDoor));
    }
    
    public void OpenDoor() {
        animator.SetBool("IsOpen", true);
        audioSource.PlayOneShot(openSound);
    }
}
// Late Joiner 加入:门是关闭的(动画未触发,音效未播)
```

**正确做法**:用 `[UdonSynced] bool _isOpen` + `OnDeserialization` 应用状态。

### 反模式 2:同步变量后忘记 `RequestSerialization()`

```csharp
// ❌ Manual Sync 必须显式调用
public void ModifyValue(int newVal) {
    _myValue = newVal;          // 仅本地修改
    // 忘记 RequestSerialization → 其他玩家看不到
}
```

**正确做法**:使用 `FieldChangeCallback`,在 setter 中自动调用 `RequestSerialization`。

### 反模式 3:在 `Start` 中初始化状态(覆盖网络值)

```csharp
// ❌ 错误:Late Joiner 收到 synced 值,被 Start 覆盖
public override void Start() {
    _isOpen = false;            // 覆盖了 Late Joiner 收到的 true
}

// ✅ 正确:在 OnDeserialization 中应用,Start 只设置默认
public override void Start() {
    ApplyState();  // 使用当前 _isOpen 值(可能是 synced)
}
```

### 反模式 4:假设玩家 0 = Owner

```csharp
// ❌ 错误:假设第一个玩家是 Owner
if (Networking.LocalPlayer.playerId == 0) { /* ... */ }

// ✅ 正确:用 Networking.IsOwner
if (Networking.IsOwner(gameObject)) { /* ... */ }
```

### 反模式 5:Late Joiner 重复触发事件

```csharp
// ❌ 错误:Late Joiner 加入时,SendCustomNetworkEvent(All, "Init") 
//    会导致所有已在线玩家再次看到 Init 效果
public override void OnPlayerJoined(VRCPlayerApi player) {
    SendCustomNetworkEvent(NetworkEventTarget.All, nameof(ShowWelcome));
}

// ✅ 正确:用 synced 标志位 + 一次性应用
[UdonSynced] private bool _didInit;
public override void OnPlayerJoined(VRCPlayerApi player) {
    if (player == Networking.LocalPlayer) {
        // 只对新玩家本地播放欢迎动画
        ShowWelcome();
    }
}
```

---

## Buffer Events vs Non-Buffer Events

### 概念区分

| 类型 | 行为 | 适用场景 |
|------|------|---------|
| **Non-Buffer Event** | 只发给 **当前在线** 的玩家 | 临时动作、UI 提示 |
| **Buffer Event** | 发给 **未来加入** 的玩家(Late Joiner) | 状态恢复、初始设置 |

### UdonSharp 中的 Buffer Events

```csharp
// Buffer 事件(SendCustomNetworkEvent 的特殊目标)
SendCustomNetworkEvent(NetworkEventTarget.AllBuffered, nameof(OnPlayerReady));
```

| 目标 | 说明 |
|------|------|
| `All` | 仅当前在线 |
| `AllBuffered` | 当前在线 + 未来加入的玩家 |

> ⚠️ **谨慎使用**:`AllBuffered` 会被重发给 Late Joiner,可能触发意外的重复逻辑(音效、粒子等)。

### 实际应用

```csharp
public class GameManager : UdonSharpBehaviour {
    [UdonSynced] private int _gameState;  // 0=Lobby, 1=Playing, 2=Ended
    
    public override void OnPlayerJoined(VRCPlayerApi player) {
        if (player == Networking.LocalPlayer) {
            // 自己是新加入的 → 不要用 All 触发任何效果
            // synced 变量已自动同步
            Debug.Log("I joined, _gameState = " + _gameState);
        }
    }
}
```

> **核心规则**:**Late Joiner 通过 `[UdonSynced]` 变量自动同步,通常不需要额外的 Buffer Event**。

---

## Late Joiner 同步模式完整示例

### 示例:游戏房间

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class GameRoom : UdonSharpBehaviour {
    [UdonSynced] private int _currentRound = 0;
    [UdonSynced] private int _playerCount = 0;
    [UdonSynced] private VRCPlayerApi _currentHost;
    [UdonSynced] private bool _isGameActive = false;
    
    public override void OnPlayerJoined(VRCPlayerApi player) {
        // 玩家加入时,playerCount + 1
        if (Networking.IsOwner(gameObject)) {
            _playerCount++;
            RequestSerialization();
        }
    }
    
    public override void OnPlayerLeft(VRCPlayerApi player) {
        if (Networking.IsOwner(gameObject)) {
            _playerCount--;
            RequestSerialization();
        }
    }
    
    public override void OnDeserialization() {
        // Late Joiner 收到 _currentRound, _isGameActive 等
        // 应用 UI
        roundUI.text = $"Round {_currentRound}";
        gameActiveUI.SetActive(_isGameActive);
    }
}
```

**Late Joiner 体验**:
- 加入时立即看到 `Round 5`、`Game Active`、当前玩家数
- 不需要任何额外代码

### 示例:复杂场景(物理对象)

```csharp
public class SyncedBox : UdonSharpBehaviour {
    [SerializeField] private VRCObjectSync objectSync;
    
    public override void OnPlayerJoined(VRCPlayerApi player) {
        if (player == Networking.LocalPlayer) {
            // 自己是新加入的,VRCObjectSync 自动同步位置
            // 不需要手动处理
            Debug.Log("Box position will sync automatically");
        }
    }
}
```

> `VRCObjectSync` **自动处理 Late Joiner 状态同步**,无需手动代码。

---

## OnPlayerJoined 与 Late Joiner

### 事件触发时机

```
时间线:
T+0s: 实例创建
T+30s: Player A 加入 → OnPlayerJoined 触发(在所有玩家)
T+60s: Player B 加入 → OnPlayerJoined 触发(在所有玩家,包括 A)
T+90s: Player C(Late Joiner)加入 → OnPlayerJoined 触发(在所有玩家,包括 A/B)
       此时,C 立即收到所有 [UdonSynced] 变量
       但 C **不会** 重放已发生的事件
```

### OnPlayerJoined 中的常见任务

| 任务 | 实现 |
|------|------|
| 统计玩家数 | 在 Owner 中 `_playerCount++` + `RequestSerialization` |
| 通知其他玩家 | `SendCustomNetworkEvent(Others, "Welcomer")` (非 All) |
| 触发新玩家本地逻辑 | `if (player == Networking.LocalPlayer) { ... }` |
| 检查 `IsNetworkSettled` | 等所有数据 deserialized 后再处理 |

### IsNetworkSettled 标志

```csharp
[SerializeField] private bool _isReady = false;

public override void Update() {
    if (!_isReady && Networking.IsNetworkSettled) {
        _isReady = true;
        // 所有 synced 数据已加载完成
        OnNetworkReady();
    }
}
```

| 标志 | 说明 |
|------|------|
| `Networking.IsNetworkSettled` | 所有数据 deserialized 后返回 `true` |

---

## OnPlayerLeft 的 Late Joiner 含义

> **关键**:`OnPlayerLeft` **不会在 Late Joiner 加入时回放**(因为 Late Joiner 没经历过该事件)。

```csharp
public override void OnPlayerLeft(VRCPlayerApi player) {
    // 这只在事件发生时刻被所有在线玩家调用
    // Late Joiner 不会调用(他们没看到玩家离开)
    
    // 关键:玩家列表等状态必须用 [UdonSynced] 变量
    if (Networking.IsOwner(gameObject)) {
        _playerList = RemovePlayerFromList(_playerList, player);
        RequestSerialization();
    }
}
```

---

## Late Joiner 调试技巧

### 验证 Late Joiner 行为

```
1. Build & Test,World 启动
2. 玩家 A 加入,操作门(打开)
3. 玩家 B 加入(模拟 Late Joiner)
4. 玩家 B 是否看到"门是开的"?
   ✅ 看到 = 正确实现
   ❌ 看到门是关的 = Bug
```

### 客户端模拟

| 工具 | 用途 |
|------|------|
| **ClientSim** | Editor 内模拟多个玩家,自动测试 Late Joiner |
| **World Debug Views** | 查看每个对象的 Owner、同步状态 |
| **Debug.Log** | 在 `OnDeserialization` 中加日志,确认变量值 |

### 常见问题

| 现象 | 原因 |
|------|------|
| Late Joiner 看不到状态 | 用了 Event 同步,改用 `[UdonSynced]` |
| Late Joiner 状态被覆盖 | `Start()` 初始化覆盖了 synced 值 |
| Late Joiner 重复触发效果 | 用了 `AllBuffered` 误触 |
| 玩家列表不同步 | 用 `[UdonSynced] int[]` 或 `string[]` |

---

## 跨平台 Late Joiner(PC/Quest)

> PC 和 Quest 平台 **必须保持一致的 `[UdonSynced]` 字段**,否则跨平台时:
- 字段值可能不一致
- 序列化结构不匹配 → **不兼容**

```csharp
// ❌ 错误:Quest 版本字段少
#if UNITY_ANDROID
public class QuestVersion : UdonSharpBehaviour {
    [UdonSynced] private int _score;  // Quest 只有 1 个字段
}
#else
public class PCVersion : UdonSharpBehaviour {
    [UdonSynced] private int _score;
    [UdonSynced] private float _extra;  // PC 有 2 个字段
}
#endif
// 跨平台玩家看到的同步数据不匹配

// ✅ 正确:PC/Quest 字段一致
public class UnifiedVersion : UdonSharpBehaviour {
    [UdonSynced] private int _score;
    [UdonSynced] private float _extra;  // 所有平台都有
}
```

---

## 典型模式

### 模式 1:简单状态(Manual + RequestSerialization)

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class SimpleFlag : UdonSharpBehaviour {
    [UdonSynced, FieldChangeCallback(nameof(IsCaptured))]
    private bool _isCaptured;
    
    public bool IsCaptured {
        get => _isCaptured;
        set { _isCaptured = value; OnCaptureChanged(); }
    }
    
    [NetworkCallable]
    public void Capture() {
        if (!Networking.IsOwner(gameObject)) return;
        IsCaptured = true;
        RequestSerialization();
    }
    
    private void OnCaptureChanged() {
        flagRenderer.material = IsCaptured ? redMat : blueMat;
    }
}
```

### 模式 2:持续状态(Continuous + OnDeserialization)

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Continuous)]
public class PlayerHealth : UdonSharpBehaviour {
    [UdonSynced(UdonSyncMode.Smooth)] private float _health;
    
    public override void OnDeserialization() {
        // Late Joiner:收到 _health 当前值
        // 普通接收:_health 变化
        healthBar.value = _health;
    }
}
```

### 模式 3:玩家列表

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PlayerListManager : UdonSharpBehaviour {
    [UdonSynced] private int[] _playerIds = new int[0];
    
    public override void OnPlayerJoined(VRCPlayerApi player) {
        if (Networking.IsOwner(gameObject)) {
            AddPlayer(player.playerId);
            RequestSerialization();
        }
    }
    
    public override void OnPlayerLeft(VRCPlayerApi player) {
        if (Networking.IsOwner(gameObject)) {
            RemovePlayer(player.playerId);
            RequestSerialization();
        }
    }
    
    public override void OnDeserialization() {
        // Late Joiner 收到完整玩家列表
        UpdatePlayerListUI(_playerIds);
    }
    
    private void AddPlayer(int id) {
        var newList = new int[_playerIds.Length + 1];
        for (int i = 0; i < _playerIds.Length; i++) newList[i] = _playerIds[i];
        newList[_playerIds.Length] = id;
        _playerIds = newList;
    }
    
    private void RemovePlayer(int id) {
        // 类似实现
    }
}
```

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| 用 Event 同步状态 | 🔴 Critical | Late Joiner 丢失 |
| Start() 覆盖 synced 值 | 🔴 Critical | 状态被重置 |
| 忘记 `RequestSerialization` | 🔴 Critical | Manual 模式不同步 |
| `AllBuffered` 误用 | 🟠 High | 重复触发效果 |
| 跨平台字段不一致 | 🔴 Critical | 序列化不匹配 |
| 数组未初始化 | 🔴 Critical | 静默失败 |
| OnPlayerLeft 不更新变量 | 🟠 High | Late Joiner 看到错误玩家列表 |
| 假设 `playerId == 0` 是 Master | 🟡 Medium | 用 `Networking.IsMaster` |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/events.md` | Event 不可用于 Late Joiner |
| `memory/world/udon/networking/variables.md` | UdonSynced 变量自动同步 |
| `memory/world/udon/networking/ownership.md` | 玩家离开导致 Owner 转移 |
| `memory/patterns/late-joiner-state-restore.md` | Late Joiner 恢复模式 |
| `memory/api/networking.md` | API 速查 |
