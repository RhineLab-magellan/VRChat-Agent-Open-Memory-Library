# Network Events 网络事件

> Type: WORLD / Udon API Reference
> Confidence: High
> Source: VRChat 官方 Creator Docs (Network Events)
> SDK Version: 3.8.1+ ([NetworkCallable] 引入版本)
> Last Updated: 2026-06-15

---

## 简介

**Network Events** 是 Udon 中简单的 **单向网络通信机制**。当脚本触发网络事件时,该事件会对 **目标玩家** 执行一次(当前实例内)。

### 核心特性

| 特性 | 说明 |
|------|------|
| **一次性** | 事件触发即结束,不会持久化 |
| **不可重放** | **迟到玩家不会收到** 已发生的事件 |
| **适合瞬时动作** | 粒子效果、声音、动画触发 |
| **不适合状态** | 必须用 `[UdonSynced]` 变量持久化 |

> ⚠️ **最常见错误**:用 Network Event 同步状态(门开/关)。**Late Joiner 会看到错误状态**。改用 `[UdonSynced]` 变量。

---

## 完整事件列表(8 个 Networking Events)

| # | 事件 | 签名 | 触发时机 | 适用模式 |
|---|------|------|---------|---------|
| 1 | `OnPlayerJoined` | `(VRCPlayerApi player)` | 新玩家加入实例 | Manual/Continuous |
| 2 | `OnPlayerLeft` | `(VRCPlayerApi player)` | 玩家离开实例 | Manual/Continuous |
| 3 | `OnOwnershipRequest` | `(VRCPlayerApi requester, VRCPlayerApi newOwner)` → `bool` | 收到所有权请求 | Manual/Continuous |
| 4 | `OnOwnershipTransferred` | `(VRCPlayerApi player)` | 所有权已转移 | Manual/Continuous |
| 5 | `OnDeserialization` | `()` | 收到网络数据 | Manual/Continuous |
| 6 | `OnPreSerialization` | `()` | 即将发送数据 | Manual |
| 7 | `OnPostSerialization` | `(SerializationResult result)` | 数据已发送 | Manual |
| 8 | `OnMasterTransferred` | `(VRCPlayerApi newMaster)` | Master 转移(因旧 Master 离开) | Manual/Continuous |

### 补充:其他常用网络相关事件

| 事件 | 来源 | 说明 |
|------|------|------|
| `OnVariableChanged` | UdonSynced 字段 | 变量值变化时触发(包括同步接收) |
| `OnDataStorageAdded` | PlayerData/PlayerObject | 玩家首次数据存储时触发 |
| `OnPlayerSuspendChanged` | PlayerApi | 玩家设备挂起/恢复 |

---

## 定义事件

### UdonSharp 语法

```csharp
using UdonSharp;
using VRC.SDKBase;
using VRC.Udon.Common.Interfaces;

public class BubbleGun : UdonSharpBehaviour {
    
    // 普通方法:通过 SendCustomNetworkEvent 调用
    public void Trigger() {
        // 业务逻辑
    }
    
    // 网络可调用方法 (SDK 3.8.1+)
    [NetworkCallable(maxEventsPerSecond: 10)]
    public void FireWithParams(int damage, string weaponType) {
        // 带参方法
    }
}
```

### Udon Graph 语法

```
1. 在 Udon Graph 中创建 "Event Custom" 节点
2. 输入唯一名称(不以 _ 开头)
3. 添加 "Flow" 连接
4. 节点的 "MaxEventsPerSecond" 控制速率
```

### 事件命名规则

| 规则 | 说明 |
|------|------|
| 唯一性 | 每个 UdonBehaviour 内事件名必须唯一 |
| 区分大小写 | `Fire` 和 `fire` 是不同事件 |
| UdonSharp | 使用 `nameof()` 让 IDE 静态检查 |
| 不以下划线开头 | `_Method` 是私有事件(防外部调用) |
| 接收方 Sync Mode | 不能是 `None`,否则无法接收 |

---

## 调用事件

### 方式 1:`SendCustomNetworkEvent`(无参,传统)

```csharp
// UdonSharpBehaviour
SendCustomNetworkEvent(NetworkEventTarget.All, nameof(Trigger));

// UdonBehaviour
udonBehaviour.SendCustomNetworkEvent(NetworkEventTarget.All, "Trigger");
```

### 方式 2:`NetworkCalling.SendCustomNetworkEvent`(带参,SDK 3.8.1+)

```csharp
using VRC.SDK3.UdonNetworkCalling;
using VRC.Udon.Common.Interfaces;

// 调用带参网络事件
NetworkCalling.SendCustomNetworkEvent(
    (IUdonEventReceiver)targetBehaviour,  // 目标脚本
    NetworkEventTarget.All,                // 目标
    nameof(FireWithParams),                // 事件名
    50,                                    // 参数 0: int damage
    "PlasmaRifle"                          // 参数 1: string weaponType
);
```

### 关键差异

| 方式 | 带参能力 | 调用语法 | 推荐度 |
|------|---------|---------|--------|
| `SendCustomNetworkEvent` | ❌ 无参 | `udon.SendCustomNetworkEvent(target, "Method")` | ⭐⭐ |
| `NetworkCalling.SendCustomNetworkEvent` | ✅ 带参 | `NetworkCalling.SendCustomNetworkEvent((IUdonEventReceiver)udon, target, "Method", P0, P1...)` | ⭐⭐⭐⭐⭐ |

> **建议**:新代码统一使用 `NetworkCalling.SendCustomNetworkEvent`,支持参数更灵活。

---

## 事件目标(NetworkEventTarget)

| 目标 | 说明 | 行为 |
|------|------|------|
| `All` | 实例内所有玩家 | 本地立即执行,远端网络发送 |
| `Others` | 除自己外的所有玩家 | 仅网络发送,本地不执行 |
| `Owner` | 对象当前 Owner | 请求转交或直接给 Owner |
| `Self` | 仅本地"回环" | 绕过所有速率限制,纯本地执行 |

### 目标选择策略

```csharp
// 开门:需要 Late Joiner 看到 → 不用 Event
[UdonSynced] private bool isOpen;

// 播放开门的音效:瞬时,不需要持久 → 用 Event
[NetworkCallable(maxEventsPerSecond: 5)]
public void PlayOpenSound() { /* ... */ }

// Self 用于纯本地逻辑(但本质就是普通方法调用)
public void LocalEffect() {
    SendCustomNetworkEvent(NetworkEventTarget.Self, nameof(LocalEffect));
}
```

> **Self 用途**:`Self` 绕过速率限制,在频繁触发的本地动画/粒子中很有用(等同函数调用)。

---

## 参数白名单

Network Event 最多支持 **8 个参数**,每个参数必须是 **可序列化类型**:

| 类型 | 序列化大小 | 备注 |
|------|-----------|------|
| `int` / `uint` | 4 bytes | - |
| `float` | 4 bytes | - |
| `string` | 可变 | UTF-8 编码 |
| `bool` | 1 byte | - |
| `byte` | 1 byte | - |
| `long` | 8 bytes | - |
| `Vector2` | 8 bytes | - |
| `Vector3` | 12 bytes | - |
| `Vector4` | 16 bytes | - |
| `Quaternion` | 16 bytes | - |
| `VRCUrl` | 可变 | URL 字符串 |
| `Color` / `Color32` | 16/4 bytes | - |
| `VRCPlayerApi` | 4 bytes | Player ID |
| 对应数组 | 元素 × 数量 | byte[] 走 UTF-8 编码 |

### 类型不匹配的处理

```csharp
[NetworkCallable]
public void TakeDamage(int amount) { /* ... */ }

// 调用时传入 null
NetworkCalling.SendCustomNetworkEvent(
    target, NetworkEventTarget.All, nameof(TakeDamage), 
    (int)null  // 错误:实际发送 default(int) = 0
);
```

**规则**:`null` → 接收方收到 `default(T)`(`int` = 0, `string` = null, 引用类型 = null)。

---

## 参数大小限制与事件拆分(Event Splitting)

### 硬性限制

| 限制 | 数值 |
|------|------|
| **单事件总参数大小** | 16 KB |
| **单参数大小** | 无单独限制(只受总事件限制) |
| **总吞吐** | ~18 KB/s(含网络开销) |
| **实际可用** | 8-10 KB/s |

### 1024 字节拆分规则

> **关键**:**如果事件参数 > 1024 bytes,VRChat 内部会拆分为多个事件**,接收方重新组装为一次调用。

```csharp
// 编码示例(参数 = 字节数)
int x = 0;                    // 4 bytes
Vector3 v = Vector3.zero;     // 12 bytes
new string('x', 400);         // 400 bytes UTF-8
"うどんは美味しい";          // 24 bytes UTF-8(非 ASCII)
new char[128];                // 256 bytes UTF-16(C# spec)
new byte[1024];               // 1024 bytes → 1 个事件
new byte[1025];               // 1025 bytes → 2 个事件
new byte[16 * 1024];          // 16384 bytes → 16 个事件(达到上限)
new int[512];                 // 2048 bytes → 2 个事件
new string[2] { "test", "foobar" }; 
// = 18 bytes: 4 + 6 (UTF-8) + 8 (2 * sizeof(int) 长度前缀)
```

### 拆分对速率限制的影响

```csharp
[NetworkCallable(maxEventsPerSecond: 2)]
public void BigDataEvent(byte[] data) { /* ... */ }

// 假设发送 2048 bytes
// 实际效果:1 个 SendCustomNetworkEvent = 2 个内部事件
// 速率限制按"内部事件"计数,实际只有 1 次调用/秒
```

> **风险**:大事件 + 严格速率限制 = 实际调用频率远低于配置值。

---

## 速率限制(Rate Limiting)

### 默认与最大

| 参数 | 数值 |
|------|------|
| **默认速率** | 5 events/second |
| **最大配置** | 100 events/second |
| **配置范围** | 1-100 |
| **全局上限** | ~100 events/second(不可配置) |

### 配置语法

```csharp
// UdonSharp
[NetworkCallable(maxEventsPerSecond: 20)]
public void MyEvent() { }

// Udon Graph
// 在 Event Custom 节点上设置 "MaxEventsPerSecond"
```

> **特殊值 0**:在 Udon Graph 中,`MaxEventsPerSecond = 0` 标记为 **Legacy 事件**(兼容旧 SDK)。

### 速率限制行为

| 行为 | 说明 |
|------|------|
| 客户端节流 | 超速事件进入队列,等速率允许后再发 |
| 服务端节流 | 防止恶意行为(玩家本地基本不可见) |
| 队列无限 | 没有队列长度上限,持续超速会积压 |
| 本地立即执行 | Self 目标 + 发送方自己不受限 |
| Best-Effort | 实际速率可能略低(网络负载、服务端压力) |

> ⚠️ **强烈建议**:把速率限制设得 **尽可能低**,作为防止恶意滥用的安全网。

### 拥塞监控 API

```csharp
using VRC.SDK3.UdonNetworkCalling;
using VRC.Udon.Common.Interfaces;
using TMPro;

public class EventQueueExample : UdonSharpBehaviour {
    [SerializeField] private TextMeshProUGUI queueStatus;
    
    void Update() {
        queueStatus.text = $"Queue: {NetworkCalling.GetAllQueuedEvents()}";
        queueStatus.text += $"\nSpecific Event Queue: {NetworkCalling.GetQueuedEvents((IUdonEventReceiver)this, "SomeNetworkEvent")}";
        queueStatus.text += $"\nClogged: {Networking.IsClogged}";
    }
}
```

| 函数 | 说明 |
|------|------|
| `NetworkCalling.GetQueuedEvents(udon, eventName)` | 指定事件当前队列数 |
| `NetworkCalling.GetAllQueuedEvents()` | 全局所有事件队列总数 |
| `Networking.IsClogged` | 网络是否拥塞(综合判断) |

---

## 事件顺序保证

> ✅ **重要保证**:**单玩家发送的事件按顺序到达**。

```csharp
SendCustomNetworkEvent(All, "EventA");  // 先到
SendCustomNetworkEvent(All, "EventB");  // 后到
// 远端接收顺序:A → B
```

### 速率限制破坏顺序

```csharp
// EventA 限速 3/s,EventB 不限速
[NetworkCallable(maxEventsPerSecond: 3)]
public void EventA() { }

[NetworkCallable(maxEventsPerSecond: 100)]
public void EventB() { }

// 发送顺序:A1, A2, A3, A4, B1
// 实际接收:A1, A2, A3, B1, A4  ← B1 跳过 A4 到达
```

> **多玩家并发**:不保证跨玩家的顺序(玩家 A 的事件 vs 玩家 B 的事件)。

---

## 访问发送方信息

```csharp
using VRC.SDK3.UdonNetworkCalling;

[NetworkCallable]
public void SomeEvent() {
    if (NetworkCalling.InNetworkCall) {
        VRCPlayerApi sender = NetworkCalling.CallingPlayer;
        // 业务逻辑
    }
}
```

| 属性 | 说明 |
|------|------|
| `NetworkCalling.CallingPlayer` | 发起该网络调用的玩家,`null` 表示非网络调用 |
| `NetworkCalling.InNetworkCall` | 当前是否在网络调用上下文中 |

> **注意**:`InNetworkCall` 在入口函数终止后重置。如果从入口调用其他方法,状态保留。

---

## Legacy 事件与安全(SDK 3.8.1 前)

### 历史背景

```
SDK 3.8.1 之前:
- 任何 public 方法都可被网络调用
- 唯一限制:方法名不能以 _ 开头

SDK 3.8.1+:
- 引入 [NetworkCallable] 显式标记
- 私有方法/下划线方法默认不可调用
- 兼容性保留:无参数 public 方法仍可被调用
```

### 阻止外部调用

```csharp
// ✅ 安全:下划线开头
private void _InternalMethod() { /* 不可网络调用 */ }

// ❌ 风险:public 但不应被调用
public void HelperMethod() { /* 旧 SDK 可被调用 */ }

// ✅ 推荐:显式标记
[NetworkCallable]
public void PublicMethod() { /* 明确可调用 */ }
```

### Legacy 事件(Component vs GameObject 语义)

| 方式 | 语义 | 行为 |
|------|------|------|
| `[NetworkCallable]` 调用 | **Component Index** | 仅指定 `UdonBehaviour` 接收 |
| Legacy 调用(无参,无 attribute) | **GameObject 语义** | 类似 `SendMessage`,调用对象上所有 `UdonBehaviour` |

> ⚠️ **危险**:网络化 `GameObject` 上 `Destroy` Component 会破坏 Component Index 顺序,导致 **未定义行为**。**永远不要 Destroy 网络化 UdonBehaviour**。

---

## 典型模式

### 模式 1:状态修改请求 → Owner 模式

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Door : UdonSharpBehaviour {
    [UdonSynced] private bool _isOpen;
    
    // 任何玩家交互 → 通知 Owner 改状态
    public override void Interact() {
        SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(RequestToggle));
    }
    
    [NetworkCallable(maxEventsPerSecond: 10)]
    public void RequestToggle() {
        // Owner 收到后修改
        if (!Networking.IsOwner(gameObject)) return;
        _isOpen = !_isOpen;
        RequestSerialization();
    }
}
```

### 模式 2:视觉/音效事件 → All 模式

```csharp
public override void OnPickupUseDown() {
    // 播放开火音效(瞬时,所有玩家)
    SendCustomNetworkEvent(NetworkEventTarget.All, nameof(PlayFireEffect));
}

[NetworkCallable(maxEventsPerSecond: 5)]
public void PlayFireEffect() {
    audioSource.PlayOneShot(fireSound);
    particleSystem.Emit(22);
}
```

### 模式 3:跨脚本带参调用

```csharp
public class ScoreManager : UdonSharpBehaviour {
    [NetworkCallable(maxEventsPerSecond: 50)]
    public void AddScore(VRCPlayerApi player, int amount) {
        // 更新分数
    }
}

// 调用方
public class HitDetector : UdonSharpBehaviour {
    [SerializeField] private ScoreManager scoreManager;
    
    public void OnHit(VRCPlayerApi attacker) {
        NetworkCalling.SendCustomNetworkEvent(
            (IUdonEventReceiver)scoreManager,
            NetworkEventTarget.All,
            nameof(ScoreManager.AddScore),
            attacker, 10
        );
    }
}
```

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| 用 Event 同步状态 | 🔴 Critical | Late Joiner 看不到 |
| 速率限制设太高 | 🟠 High | 防止恶意玩家滥用 |
| 大事件未考虑拆分 | 🟡 Medium | 实际速率低于配置 |
| `null` 参数误用 | 🟡 Medium | 接收方收到 `default(T)` |
| 跨版本速率不一致 | 🟡 Medium | 服务端可能丢弃事件 |
| Destroy 网络 Component | 🔴 Critical | Component Index 错乱 |
| `InNetworkCall` 误读 | 🟢 Low | 仅在入口函数有效 |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/late-joiners.md` | Late Joiner 与 Event 关系 |
| `memory/world/udon/networking/variables.md` | 变量同步(状态持久化) |
| `memory/world/udon/networking/ownership.md` | Owner 模式 + 事件 |
| `memory/api/networking.md` | API 速查 |
| `memory/api/udon-type-exposure.md` | Udon Type Exposure |
