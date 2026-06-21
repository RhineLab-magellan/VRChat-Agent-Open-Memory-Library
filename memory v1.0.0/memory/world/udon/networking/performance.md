# Performance Considerations 性能优化

> Type: WORLD / Udon Reference
> Confidence: High
> Source: VRChat 官方 Creator Docs (Performance Considerations)
> SDK Version: 3.x
> Last Updated: 2026-06-15

---

## 简介

高效的 Networking 是流畅多人体验的基础。设计不当的网络同步会导致 **带宽飙升、卡顿、状态不一致**。本文档汇总官方推荐的 **10 条带宽优化规则** 和 **对象池 / 合并序列化** 等关键策略。

> **核心原则**:**Networking 不是免费的**——每字节、每同步、每事件都消耗配额。

---

## 带宽限制(再次强调)

> ⚠️ 这些数字是 **所有 Udon 行为共享的硬上限**。

| 限制类型 | 数值 | 超出后果 |
|---------|------|---------|
| **总带宽** | **~11 KB/s** | `IsClogged = true`,全局拥塞 |
| **Manual Sync** | **280,496 bytes/serialization** | 事件缓存、延迟发送 |
| **Continuous Sync** | **~200 bytes/serialization** | 序列化 **直接失败** |
| **Network Event 参数** | 16 KB/event | 内部拆分 |
| **总吞吐(Events)** | ~18 KB/s | 实际可用 8-10 KB/s |

---

## Variables vs Events:何时用哪个

### Variables(同步数据)适用场景

| 场景 | 示例 |
|------|------|
| Late Joiner 需要的状态 | 门开/关、玩家分数 |
| 离散状态 | 回合阶段、玩家等级 |
| 关键数据 | 排行榜、游戏结果 |
| 需要 Owner 写入的 | 玩家私人数据 |

### Events(瞬时动作)适用场景

| 场景 | 示例 |
|------|------|
| 临时视觉 | 粒子、音效、震动 |
| 触发动画 | 一次性 Play() |
| 发射子弹 | 子弹事件 |
| UI 提示 | 浮动伤害数字 |

### 反模式:用 Event 同步状态

```csharp
// ❌ 致命错误
public class Door : UdonSharpBehaviour {
    public void Interact() {
        SendCustomNetworkEvent(NetworkEventTarget.All, nameof(OpenDoor));
    }
    
    public void OpenDoor() {
        animator.SetBool("IsOpen", true);
    }
}
// Late Joiner:门是关的(Event 不会重放)

// ✅ 正确
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Door : UdonSharpBehaviour {
    [UdonSynced] private bool _isOpen;
    
    public void Interact() {
        if (Networking.IsOwner(gameObject)) {
            _isOpen = !_isOpen;
            RequestSerialization();
        }
    }
}
```

---

## 10 条带宽优化规则

### 规则 1:避免不必要的同步

| 操作 | 影响 |
|------|------|
| ❌ 每帧同步位置 | 浪费 200B/帧 × 30fps = 6KB/s |
| ✅ 插值/外推 | 减少同步频率,客户端平滑 |
| ❌ 同步物理 Rigidbody | 除非必要,不用网络同步物理 |
| ✅ 用 VRCObjectSync | VRChat 内部优化通道 |
| ❌ 频繁小幅更新 | 占用配额 |
| ✅ 阈值变化才同步 | 减少 90%+ 序列化次数 |

**代码示例**:
```csharp
// ❌ 每帧同步
void Update() {
    if (Networking.IsOwner(gameObject)) {
        _position = transform.position;
        RequestSerialization();
    }
}

// ✅ 阈值同步
private const float THRESHOLD = 0.1f;
private Vector3 _lastSynced;

void Update() {
    if (Networking.IsOwner(gameObject)) {
        if (Vector3.Distance(transform.position, _lastSynced) > THRESHOLD) {
            _position = transform.position;
            _lastSynced = _position;
            RequestSerialization();
        }
    }
}
```

### 规则 2:使用正确的 Sync Mode

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 门开/关 | **Manual** | 离散状态,变化稀疏 |
| 玩家位置 | **Continuous**(或 VRCObjectSync) | 高频变化 |
| 积分板 | **Manual** | 关键数据 |
| 进度条 | **Continuous** | 平滑过渡 |
| 临时分数 | **Manual** | 偶发更新 |

### 规则 3:用位域压缩多个 bool

```csharp
// ❌ 8 个 bool = 8 bytes
[UdonSynced] private bool _active;
[UdonSynced] private bool _hidden;
[UdonSynced] private bool _locked;
[UdonSynced] private bool _marked;
// ... 5 个更多

// ✅ 1 个 byte = 8 个 bool
[UdonSynced] private byte _flags;
// bit0 = active
// bit1 = hidden
// bit2 = locked
// ...
```

> 节省 7 bytes/同步 × 频率 = **巨大带宽节省**。

### 规则 4:避免同步不必要的精度

```csharp
// ❌ 同步完整 Vector3(12 bytes)
[UdonSynced] private Vector3 _position;

// ✅ 同步压缩的 short(2-6 bytes)
[UdonSynced] private int _posX;  // 4 bytes
[UdonSynced] private int _posY;
[UdonSynced] private int _posZ;
```

> 对于网格位置,**`int` 比 `Vector3` 节省 0%**,但对于小范围坐标(0-100),用 `byte`(0-255)更省。

### 规则 5:分组合并变量

```csharp
// ❌ 5 个独立 byte
[UdonSynced] private byte _health;
[UdonSynced] private byte _mana;
[UdonSynced] private byte _stamina;
[UdonSynced] private byte _armor;
[UdonSynced] private byte _level;

// ✅ 用结构体 / 数组
[UdonSynced] private byte[] _stats = new byte[5];
// _stats[0] = health, _stats[1] = mana, ...
// 一次序列化 = 1 长度前缀 + 5 bytes = 9 bytes
// vs 5 个独立 byte = 5 * (1 + 1) = 10 bytes
```

> 当 `OnPreSerialization` 触发一次时,合并同步可以减少 5 个独立序列化的开销。

### 规则 6:用 VRCObjectSync 同步物理

```csharp
// ❌ 手写位置同步(占用配额)
[UdonSynced(UdonSyncMode.Smooth)] private Vector3 _position;
[UdonSynced(UdonSyncMode.Smooth)] private Quaternion _rotation;
void Update() {
    if (Networking.IsOwner(gameObject)) {
        _position = transform.position;
        _rotation = transform.rotation;
    }
}

// ✅ 用 VRCObjectSync(VRChat 内部优化)
public class PhysicsObject : UdonSharpBehaviour {
    // VRCObjectSync 自动处理,无需 synced 变量
}
```

> VRCObjectSync 使用 **专用网络通道**(不走 synced 变量配额)。

### 规则 7:Network Event 节流

```csharp
// ❌ 无限制事件
public void Fire() {
    SendCustomNetworkEvent(NetworkEventTarget.All, nameof(PlayEffect));
}

// ✅ 显式速率限制
[NetworkCallable(maxEventsPerSecond: 5)]
public void PlayEffect() { /* ... */ }
```

> 默认 5/s,推荐 **尽可能低**(防滥用)。

### 规则 8:本地优先的视觉效果

```csharp
// ❌ 网络事件触发本地效果
public void OnLocalHit() {
    SendCustomNetworkEvent(NetworkEventTarget.All, nameof(PlayHitEffect));
}

public void PlayHitEffect() {
    particleSystem.Emit(50);
}

// ✅ 本地 + 远端分离
public void OnLocalHit() {
    // 本地立即播放(零延迟)
    PlayHitEffect();
    // 远端稍后播放
    SendCustomNetworkEvent(NetworkEventTarget.Others, nameof(PlayHitEffect));
}
```

> 关键:本地效果 **不需要走网络**,Owners 永远本地立即触发,只给远端发 Event。

### 规则 9:合并连续修改

```csharp
// ❌ 多次小修改 + 多次序列化
public void SetState(int a, int b, int c) {
    _a = a;
    RequestSerialization();
    _b = b;
    RequestSerialization();
    _c = c;
    RequestSerialization();
}

// ✅ 一次性修改 + 一次序列化
public void SetState(int a, int b, int c) {
    _a = a;
    _b = b;
    _c = c;
    RequestSerialization();  // 只触发一次
}
```

> **多次 `RequestSerialization()` 不会** 合并——每次都立即尝试发送。

### 规则 10:监控 + 降级

```csharp
void Update() {
    if (Networking.IsClogged) {
        // 降级
        particleSystem.Stop();
        highQualitySync.enabled = false;
    } else {
        // 恢复
        if (!particleSystem.isPlaying) particleSystem.Play();
        highQualitySync.enabled = true;
    }
}
```

> `IsClogged` 是网络健康的 **实时指示器**,应作为降级开关。

---

## 对象池(Object Pool)同步

> 详见 `network-components.md`。这里补充性能相关。

### 为什么用对象池?

| 优势 | 说明 |
|------|------|
| 避免运行时 instantiate | 实例化消耗大 |
| 减少同步对象数 | 池内对象状态由 Pool 管理 |
| 自动 Late Joiner 同步 | Pool 内部处理 |
| 性能可预测 | 池大小固定,带宽稳定 |

### 实现模式

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class BulletManager : UdonSharpBehaviour {
    [SerializeField] private VRCObjectPool bulletPool;
    [SerializeField] private int poolSize = 32;
    [UdonSynced] private int _activeCount;  // 仅统计,不存对象引用
    
    [NetworkCallable(maxEventsPerSecond: 30)]
    public void FireBullet(Vector3 origin, Vector3 direction) {
        if (!Networking.IsOwner(gameObject)) return;
        
        GameObject bullet = bulletPool.TryToSpawn();
        if (bullet == null) return;  // 池耗尽
        
        bullet.transform.position = origin;
        bullet.transform.forward = direction;
        bullet.SetActive(true);
        
        _activeCount++;
        // 不需要 RequestSerialization(对象状态由 Pool 自动同步)
    }
    
    [NetworkCallable(maxEventsPerSecond: 30)]
    public void ReturnBullet(GameObject bullet) {
        if (!Networking.IsOwner(gameObject)) return;
        bulletPool.Return(bullet);
        _activeCount--;
    }
}
```

---

## 合并序列化(Batch Serialization)

> 在 `OnPreSerialization` 中一次性打包所有需要同步的数据。

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class BatchedData : UdonSharpBehaviour {
    [UdonSynced] private byte[] _batchData = new byte[64];
    
    // 各种状态
    private bool _isActive;
    private byte _health;
    private byte _mana;
    
    public override void OnPreSerialization() {
        // 一次性打包所有状态
        _batchData[0] = (byte)(_isActive ? 1 : 0);
        _batchData[1] = _health;
        _batchData[2] = _mana;
        // 剩余 61 bytes 备用
    }
    
    public override void OnDeserialization() {
        // 一次性解包
        _isActive = _batchData[0] == 1;
        _health = _batchData[1];
        _mana = _batchData[2];
    }
}
```

> **单次序列化** 发送 64 bytes,vs 3 个独立变量可能 3-5 次序列化 = 3-15 bytes + 多次开销。

---

## Ownership & Object Sync 性能

### 最小化所有权转移

```csharp
// ❌ 频繁转移
public override void Interact() {
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
    _state = !_state;
    RequestSerialization();
}

// ✅ Owner 模式
public override void Interact() {
    SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(RequestToggle));
}

[NetworkCallable]
public void RequestToggle() {
    if (!Networking.IsOwner(gameObject)) return;
    _state = !_state;
    RequestSerialization();
}
```

> 所有权转移涉及 **网络消息**(延迟 + 带宽),应最小化。

---

## 测试 & 调试性能

### 监控方式

| 工具 | 用法 |
|------|------|
| **World Debug Views** | 实时显示每对象字节数 |
| **Network Stats API** | 程序化访问详细指标 |
| **Debug.Log** | 记录 `OnPostSerialization.byteCount` |
| **ClientSim** | Editor 模拟多个玩家 |

### 关键指标

| 指标 | 健康值 | 警告 | 危险 |
|------|-------|------|------|
| `BytesOutAverage` | < 2 KB/s | 2-8 KB/s | > 11 KB/s |
| `IsClogged` 时间占比 | < 1% | 1-10% | > 10% |
| 单对象 `TotalBytes` | < 1 KB/s | 1-5 KB/s | > 10 KB/s |
| `ReliableEventsInOutboundQueue` | 0-5 | 5-20 | > 20 |

### 性能测试模式

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PerformanceTestObject : UdonSharpBehaviour {
    [UdonSynced] private Vector3 _position;
    [UdonSynced] private Quaternion _rotation;
    [UdonSynced] private int _counter;
    
    private int _localUpdateCount = 0;
    private float _lastReportTime = 0;
    
    void Update() {
        if (Networking.IsOwner(gameObject)) {
            transform.Rotate(Vector3.up, 1f);
            _position = transform.position;
            _rotation = transform.rotation;
            _counter++;
            
            if (Time.time - _lastReportTime > 1.0f) {
                Debug.Log($"[Perf] Updates/sec: {_localUpdateCount}");
                _localUpdateCount = 0;
                _lastReportTime = Time.time;
            }
            _localUpdateCount++;
            
            RequestSerialization();
        }
    }
}
```

---

## 性能优化清单(发布前)

```
□ 所有 synced 数组已初始化
□ 用 [UdonSynced] 替代 Network Event 同步状态
□ 高频变化用 Continuous(200B 上限)或 VRCObjectSync
□ 离散状态用 Manual(280KB 上限)+ RequestSerialization
□ 多 bool 用 byte 位域压缩
□ 物理对象用 VRCObjectSync
□ Network Event 设速率限制(尽可能低)
□ 监控 IsClogged,有降级方案
□ 检查所有 OnPreSerialization 不做重计算
□ 玩家列表等动态数据用 synced 数组
□ 跨平台字段保持一致
□ Build & Test 测试 2+ 玩家
□ 监控 Debug Menu 6 数据
```

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| 超出带宽上限 | 🔴 Critical | 数据丢失、玩家看到不同步 |
| 用 Event 同步状态 | 🔴 Critical | Late Joiner 看不到 |
| 频繁 SetOwner | 🟠 High | 引入延迟,带宽浪费 |
| 数组未初始化 | 🔴 Critical | 静默失败 |
| Debug.Log 过多 | 🟠 High | 消耗带宽配额 |
| 高频 Manual 序列化 | 🟠 High | 占用带宽 |
| 未做跨平台测试 | 🟠 High | PC/Quest 字段不匹配 |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/variables.md` | 同步变量类型 |
| `memory/world/udon/networking/events.md` | Network Event 速率限制 |
| `memory/world/udon/networking/ownership.md` | 所有权与性能 |
| `memory/world/udon/networking/network-components.md` | VRCObjectSync/ObjectPool |
| `memory/world/udon/networking/network-details.md` | 内部字节细节 |
| `memory/patterns/bit-packed-flags.md` | 位域压缩模式 |
| `memory/patterns/advanced-sync-patterns.md` | 高级同步模式 |
| `memory/api/networking.md` | API 速查 |
