---
title: "Network Components 网络组件"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "VRChat 官方 Creator Docs (Network Components)"
source_type: official
version: 1.0
last_review: 2026-06-15
confidence: High
tags:
  - world
  - networking
  - udon
aliases:
  - "Network Components 网络组件"
  - network-components
related:
  - "world/udon/networking/index.md"
  - "world/udon/networking/events.md"
  - "world/udon/networking/ownership.md"
  - "world/udon/networking/variables.md"
  - "world/udon/networking/late-joiners.md"
  - "world/udon/networking/debugging.md"
  - "api/networking.md"
  - "api/persistence.md"
---
# Network Components 网络组件

> SDK Version: 3.x
---

## 简介

VRChat 提供了多个 **核心网络组件**,封装了常用的同步逻辑。理解这些组件的能力边界,是构建稳定 World 的基础。

> 涵盖:Networking 属性 + 事件 + VRCObjectSync + VRCObjectPool

---

## 一、Networking 属性(Networking Static Class)

通过 `Networking.XXX` 访问,**所有静态属性**,不依赖 GameObject。

| 属性 | 类型 | 说明 | 热路径 |
|------|------|------|--------|
| `LocalPlayer` | `VRCPlayerApi` | 本地玩家 API 对象 | ✅ |
| `IsInstanceOwner` | `bool` | 本地玩家是否是实例创建者 | ✅ |
| `InstanceOwner` | `VRCPlayerApi` | 实例创建者(可能 null) | ✅ |
| `IsMaster` | `bool` | 本地玩家是否是 Master | ✅ |
| `Master` | `VRCPlayerApi` | 当前 Master(保证非 null) | ✅ |
| `IsNetworkSettled` | `bool` | 所有数据已 deserialized 并应用 | ✅ |
| `IsClogged` | `bool` | 网络是否拥塞 | ✅ |
| `SimulationTime` | `float` | 当前玩家/对象的模拟时间戳 | ✅ |

### 详细说明

#### `LocalPlayer`

```csharp
// 在 Start 中缓存
private VRCPlayerApi _localPlayer;

public override void Start() {
    _localPlayer = Networking.LocalPlayer;
}
```

> 永远缓存,不要每帧访问。

#### `IsInstanceOwner`

| 场景 | 返回值 |
|------|-------|
| Invite/Invite+/Friends/Friends+ 实例 | 实例创建者返回 `true` |
| **Group 实例** | **永远 `false`** |
| **Public 实例** | **永远 `false`** |
| **Build & Test(SDK 测试模式)** | **永远 `false`** |

> ⚠️ 不要用 `IsInstanceOwner` 判断"是否是管理员",因为 Group/Public 永远 false。

#### `InstanceOwner`

| 场景 | 返回值 |
|------|-------|
| Owner 在实例中 | `VRCPlayerApi` 对象 |
| Owner 离开实例 | **`null`**(Owner 重新加入后恢复) |

> **关键**:`InstanceOwner` 永不变(创建者永远是创建者),但对象引用可能为 null。

#### `IsMaster`

> ⚠️ **Master 不可靠**——VRChat 可能在任何时候转移 Master。

| 触发变化 | 事件 |
|---------|------|
| Master 离开实例 | `OnMasterTransferred` 触发 |
| Master 是 Android 设备且挂起太久 | 可能被转移 |

> 不要用 `IsMaster` 做权限判断,改用 `IsInstanceOwner` 或自定义 Moderation。

#### `IsNetworkSettled`

```csharp
private bool _isReady = false;

public override void Update() {
    if (!_isReady && Networking.IsNetworkSettled) {
        _isReady = true;
        // 所有 synced 数据已加载完成,可以安全使用
        OnNetworkReady();
    }
}
```

> **重要**:在 Late Joiner 加入时,等 `IsNetworkSettled` 后再访问 synced 变量。

#### `IsClogged`

```csharp
void Update() {
    if (Networking.IsClogged) {
        // 降级表现
        particleSystem.Stop();
    }
}
```

> 用于自适应降级,避免持续同步触发拥塞。

---

## Simulation Time(模拟时间)

> VRChat 内部使用的时间戳,用于对象同步和延迟补偿。

### 概念

- `SimulationTime(player)`:玩家/对象的"模拟时间",表示 VRChat 认为该对象 **在多久之前** 处于当前位置
- **目的**:让接收方知道 **需要多少延迟** 才能平滑复现

### 用法

```csharp
// 玩家当前网络延迟
float latency = Time.realtimeSinceStartup - Networking.SimulationTime(Networking.LocalPlayer);

// 判断对象是否需要追赶
float objectLag = Time.realtimeSinceStartup - objectSync.SimulationTime;
```

### 调整机制

Simulation Time 根据多种因素动态调整:
- 网络延迟
- 可靠性
- 数据包接收频率
- 目标:实时但防止 hitching

> 用于构建自定义的 VRCObjectSync-like 系统。

---

## 二、Networking Events(网络事件)

> 已在 `events.md` 中详述,此处补充在 Network Components 上下文中的用法。

### 完整列表

| # | 事件 | 签名 | 触发时机 | 替代方式 |
|---|------|------|---------|---------|
| 1 | `OnPreSerialization` | `()` | 即将发送数据 | - |
| 2 | `OnDeserialization` | `()` | 收到网络数据(无时间信息) | - |
| 3 | `OnDeserialization(DeserializationResult)` | `(DeserializationResult)` | 收到网络数据(带 send/receive time) | - |
| 4 | `OnPostSerialization` | `(SerializationResult)` | 数据已发送(含字节数) | - |
| 5 | `OnSpawn` | `()` | **(已弃用)** | 用 `OnEnable` 替代 |
| 6 | `OnOwnershipRequest` | `(VRCPlayerApi req, VRCPlayerApi newOwner)` → `bool` | 收到所有权请求 | - |
| 7 | `OnOwnershipTransferred` | `(VRCPlayerApi newOwner)` | 所有权已转移 | - |
| 8 | `OnMasterTransferred` | `(VRCPlayerApi newMaster)` | Master 转移 | - |
| 9 | `OnVariableChanged` | `(variable)` | 变量值变化(可自动生成) | - |

### `OnDeserialization(DeserializationResult)` 详解

> 比基础 `OnDeserialization` 提供 **时间信息**。

```csharp
public override void OnDeserialization(DeserializationResult result) {
    // 三个属性
    float sendTime = result.sendTime;
    float receiveTime = result.receiveTime;
    bool isFromStorage = result.isFromStorage;
}
```

| 属性 | 类型 | 说明 |
|------|------|------|
| `sendTime` | `float` | 消息发送时间(基于 VRChat 启动后秒数) |
| `receiveTime` | `float` | 消息接收时间(基于 VRChat 启动后秒数) |
| `isFromStorage` | `bool` | 数据是否从 Persistence 存储恢复 |

### 时间换算(关键!)

> ⚠️ **每个玩家的 `Time.realtimeSinceStartup` 不同**!

```csharp
// 错误:直接比较 sendTime
float ago = Time.realtimeSinceStartup - result.sendTime;  // 不准!

// 正确:用 receiveTime 作为基准
float ago = result.receiveTime - result.sendTime;

// 同步 sendTime 到其他玩家
float offset = Time.realtimeSinceStartup - result.sendTime;
// 其他玩家:用 offset + 自己的 Time.realtimeSinceStartup = 绝对时间
```

> `sendTime` 可能是 **负数**(发送方在 VRChat 启动前发送)。

### `OnVariableChanged` 关键规则

```csharp
[UdonSynced, FieldChangeCallback(nameof(Health))]
private float _health;

public float Health {
    get => _health;
    set { _health = value; OnHealthChanged(); }
}
```

| 规则 | 说明 |
|------|------|
| **数组内容变化不触发** | 数组引用未变,内容修改不会触发 |
| **触发时机早于 OnDeserialization** | OnVariableChanged 在所有 synced 变量写完前触发 |
| **跨变量不一致** | 触发时其他变量可能未更新 |
| **Owner/Non-Owner 都触发** | 包括网络同步接收 |

---

## 三、VRCObjectSync(物理对象同步)

> **自动同步 Transform(位置/旋转/缩放)和 Rigidbody(物理)状态** 的内置组件。

### 核心功能

| 功能 | 同步范围 | 备注 |
|------|---------|------|
| **Transform** | Position / Rotation / Scale | - |
| **Rigidbody** | 物理状态 | - |
| **Interpolation** | 自动 | VRChat 内部处理 |
| **Discontinuity** | FlagDiscontinuity 触发时无插值 | 用于 teleport |

### 配置

```
1. GameObject 上添加 Rigidbody
2. 添加 VRCObjectSync
3. (可选)VRCPickup(支持拾取)
```

### FlagDiscontinuity

```csharp
public void Teleport() {
    transform.position = newPosition;  // 目标位置
    objectSync.FlagDiscontinuity();    // 标记:无插值
}
```

> 用于 teleport、重置位置等"瞬时"移动,避免插值动画。

### Gravity 控制

```csharp
// 启用/禁用 gravity(VRChat 推荐方式)
objectSync.SetGravity(true);
bool isGravityOn = objectSync.GetGravity();
```

> ⚠️ **有 VRCObjectSync 时,gravity 必须用 VRCObjectSync 控制,不能直接用 Rigidbody**。

### Kinematic 控制

```csharp
objectSync.SetKinematic(true);
bool isKinematic = objectSync.GetKinematic();
```

### Respawn(回到初始位置)

```csharp
objectSync.Respawn();
```

**自动执行**:
1. 设置 `DiscontinuityHint = true`
2. `transform.position` = 初始位置
3. `transform.rotation` = 初始旋转
4. 如果有 Rigidbody:
   - `velocity` = `Vector3.zero`
   - `angularVelocity` = `Vector3.zero`
   - `position` = 初始位置
   - `rotation` = 初始旋转

### Ownership 行为

| 行为 | 说明 |
|------|------|
| 默认 Owner | 第一个加入的玩家(实例 Master) |
| 修改限制 | 只有 Owner 能改 position/rotation |
| 玩家拾取时 | 拾取者自动成为 Owner(VRCPickup) |
| Owner 离开 | VRChat 自动转移给新玩家 |

> VRCObjectSync **不是** 通过 `[UdonSynced]` 变量工作,而是通过 VRChat 内部优化通道。

---

## 四、VRCObjectPool(对象池同步)

> **轻量管理一组 GameObject 的激活状态**,自动同步池中对象状态。

### 核心特性

| 特性 | 说明 |
|------|------|
| 轻量管理 | 管理一组对象数组 |
| 自动同步 | 池内对象激活状态自动同步 |
| Late Joiner | 新玩家自动看到正确激活状态 |
| Owner 控制 | 只有 Owner 能 spawn/return |

### 配置

```
1. GameObject 上添加 VRCObjectPool
2. 在 Inspector 中指定 Pool(对象数组)
3. 添加 UdonBehaviour 调用 TryToSpawn / Return
```

### API

#### TryToSpawn

```csharp
GameObject spawned = pool.TryToSpawn();
if (spawned != null) {
    // 成功 spawn
} else {
    // 池中无可用对象
}
```

> 返回 `null` 表示池耗尽(没有可用对象)。

#### Return(Owner 调用)

```csharp
pool.Return(gameObject);  // 对象回到池中,自动 disabled
```

> 只有 **Pool Owner** 能调用 `Return`,非 Owner 调用无效。

### Late Joiner 自动同步

```
时间线:
T+0: Pool 创建,所有对象 inactive
T+10s: Player A spawns Object1 → Object1 激活
T+20s: Player B 加入 → 自动看到 Object1 激活(Object2 仍 inactive)
```

> **不需要写 OnPlayerJoined 同步逻辑**,VRChat 内部处理。

### 典型应用场景

| 场景 | 用法 |
|------|------|
| 弹道(子弹/飞镖) | 从池中 spawn,命中后 Return |
| 临时道具 | spawn → 使用 → Return |
| 资源点 | spawn 树苗/矿石 |
| NPC/敌人 | spawn 敌人,死亡 Return |

---

## 五、其他网络相关组件

### VRCPickup(自动所有权)

| 行为 | 自动处理 |
|------|---------|
| 玩家拾取 | **所有权自动转移** 给该玩家 |
| 玩家放下 | 所有权保留给该玩家 |
| 玩家丢出 | 物理抛物,所有权保留 |
| 玩家离开 | VRChat 重新分配 |

> 详见 `world/components/vrcpickup.md`(如已入库)。

### VRCStation(座位同步)

> 玩家使用 Station 时,自身 Transform 跟随 Station。

| 行为 | 说明 |
|------|------|
| 玩家坐下 | Transform 锁定到 Station |
| 玩家离开 | 自动解除 |
| 多人同步 | 坐在 Station 上的玩家对其他玩家可见 |

### PlayerObject(玩家专属对象)

> 每个玩家都有自己的一份实例化对象。详见 Persistence 文档。

| 特性 | 说明 |
|------|------|
| 唯一性 | 每个玩家独立实例 |
| 跨实例持久 | 可选持久化(VRCEnablePersistence) |
| 替代方案 | 可作为 Per-Player Object Pool |

### PlayerData(玩家数据持久化)

> 跨实例、跨平台、跨设备的玩家数据。

| 限制 | 数值 |
|------|------|
| PlayerData 配额 | 100 KB/玩家 |
| PlayerObject 配额 | 100 KB/玩家 |
| 压缩后容量 | 最多 300 KB 原始数据(可压缩时) |

> 详见 `memory/api/persistence.md` 和 `memory/world/persistence/`。

---

## 完整示例:物理交互世界

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PhysicsCrate : UdonSharpBehaviour {
    [SerializeField] private VRCObjectSync objectSync;
    [SerializeField] private VRCObjectPool pool;
    [SerializeField] private GameObject visual;
    [UdonSynced] private int _state;  // 0=in pool, 1=active
    
    public override void OnPlayerJoined(VRCPlayerApi player) {
        // Late Joiner:自动通过 synced 看到状态
        if (_state == 0) {
            visual.SetActive(false);
        }
    }
    
    [NetworkCallable]
    public void Spawn() {
        if (!Networking.IsOwner(gameObject)) return;
        GameObject obj = pool.TryToSpawn();
        if (obj != null) {
            _state = 1;
            RequestSerialization();
        }
    }
    
    [NetworkCallable]
    public void Despawn() {
        if (!Networking.IsOwner(gameObject)) return;
        pool.Return(gameObject);
        _state = 0;
        RequestSerialization();
    }
    
    public void TeleportCrate() {
        if (Networking.IsOwner(gameObject)) {
            transform.position = newPosition;
            objectSync.FlagDiscontinuity();  // 无插值
        }
    }
}
```

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| 用 `IsMaster` 做权限 | 🔴 Critical | Master 不可预测 |
| VRCObjectSync 直接改 Rigidbody.gravity | 🟠 High | 改用 objectSync.SetGravity |
| ObjectPool 非 Owner Return | 🟠 High | 无效,只有 Owner 能操作 |
| ObjectPool 同步结构不匹配 | 🟠 High | Pool 数量变化需兼容考虑 |
| `IsInstanceOwner` 在 Group/Public 永远 false | 🟡 Medium | 不适用于这些实例类型 |
| `Time.realtimeSinceStartup` 跨玩家不同 | 🟠 High | 同步时间需用 offset |
| `OnVariableChanged` 数组内容不触发 | 🟡 Medium | 用 Setter 包装 |
| `OnSpawn` 已弃用 | 🟢 Low | 改用 OnEnable |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/events.md` | 完整事件列表 |
| `memory/world/udon/networking/ownership.md` | 所有权 API 详解 |
| `memory/world/udon/networking/variables.md` | synced 变量 |
| `memory/world/udon/networking/late-joiners.md` | Late Joiner 同步 |
| `memory/world/udon/networking/debugging.md` | Network 调试 |
| `memory/api/networking.md` | API 速查 |
| `memory/api/persistence.md` | PlayerData/PlayerObject 配额 |
