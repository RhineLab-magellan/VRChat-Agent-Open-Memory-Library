---
title: "Network Variables 网络变量"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "VRChat 官方 Creator Docs (Network Variables) + Specs"
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
  - "Network Variables 网络变量"
  - variables
related:
  - "world/udon/networking/index.md"
  - "world/udon/networking/compatibility.md"
  - "world/udon/networking/network-details.md"
  - "world/udon/networking/performance.md"
  - "api/networking.md"
  - "patterns/bit-packed-flags.md"
  - "patterns/manual-sync-state.md"
---
# Network Variables 网络变量

> SDK Version: 3.x
---

## 简介

**Network Variables**(又名 Synced Variables)是 Udon 中跨玩家共享数据的核心机制。与 Network Event 不同,**变量是持久的**——任何新加入实例的玩家都会自动收到最新值。

> ✅ **核心承诺**:**Late Joiners 一定能看到最新状态**(无论 Manual/Continuous,无需手动 `RequestSerialization` on join)。

---

## 核心机制

### 如何同步

| 方式 | 行为 |
|------|------|
| **Inspector 勾选 "synced"** | VRChat 自动同步该字段 |
| **UdonSharp `[UdonSynced]`** | 编译时自动识别同步字段 |
| **Owner 修改** | 只有 Owner 能改,非 Owner 修改会被忽略或警告 |

### 不同步模式的行为

| Sync Mode | 修改方式 | 序列化时机 | Late Joiner 表现 |
|-----------|---------|-----------|-----------------|
| **NoVariableSync** | 任意 | 永不 | ❌ 看不到(默认值) |
| **Manual** | `RequestSerialization()` | 显式调用时 | ✅ 看到最近一次成功序列化的值 |
| **Continuous** | 任意 | 每帧自动 | ✅ 看到最新值 |

### 设置同步模式

#### Inspector

```
在 UdonBehaviour Inspector 中:
"Synchronization" 下拉菜单
  ├─ None (NoVariableSync)
  ├─ Manual
  └─ Continuous
```

#### UdonSharp Attribute

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PlayerData : UdonSharpBehaviour {
    [UdonSynced] private int _score;
}

[UdonBehaviourSyncMode(BehaviourSyncMode.Continuous)]
public class PlayerPosition : UdonSharpBehaviour {
    [UdonSynced] private Vector3 _position;
}

[UdonBehaviourSyncMode(BehaviourSyncMode.NoVariableSync)]
public class LocalLogic : UdonSharpBehaviour {
    // 仅本地逻辑,纯事件
}
```

---

## 完整字段类型表(序列化大小)

> 来源:VRChat 官方 `network-details.md` Specs

### Boolean 类型

| 类型 | 大小 | 备注 |
|------|------|------|
| `bool` | 1 byte | 序列化为 1 byte(非 1 bit) |

### 整数类型

| 类型 | 范围 | 大小 |
|------|------|------|
| `sbyte` | -128 to 127 | 1 byte |
| `byte` | 0 to 255 | 1 byte |
| `short` | -32,768 to 32,767 | 2 bytes |
| `ushort` | 0 to 65,535 | 2 bytes |
| `int` | -2,147,483,648 to 2,147,483,647 | 4 bytes |
| `uint` | 0 to 4,294,967,295 | 4 bytes |
| `long` | ±9.22 × 10^18 | 8 bytes |
| `ulong` | 0 to 1.84 × 10^19 | 8 bytes |

### 浮点类型

| 类型 | 范围 | 精度 | 大小 |
|------|------|------|------|
| `float` | ±3.4 × 10^38 | ~6-9 位 | 4 bytes |
| `double` | ±1.7 × 10^308 | ~15-17 位 | 8 bytes |

### Unity 几何类型

| 类型 | 大小 | 备注 |
|------|------|------|
| `Vector2` | 8 bytes | float × 2 |
| `Vector3` | 12 bytes | float × 3 |
| `Vector4` | 16 bytes | float × 4 |
| `Quaternion` | 16 bytes | float × 4 |

### 颜色类型

| 类型 | 大小 | 备注 |
|------|------|------|
| `Color` | 16 bytes | float RGBA |
| `Color32` | 4 bytes | byte RGBA |

### 文本类型

| 类型 | 范围 | 大小 |
|------|------|------|
| `char` | U+0000 to U+FFFF | 2 bytes |
| `string` | same as char | 2 bytes / char(UTF-8/16 视实现) |
| `VRCUrl` | U+0000 to U+FFFF | 2 bytes / char |

### 其他

| 类型 | 大小 | 备注 |
|------|------|------|
| `VRCPlayerApi` | 4 bytes | Player ID(非对象引用) |
| 数组 | 元素 × 数量 | 数组需初始化! |

> **关于 VRCPlayerApi**:不能同步对象引用,只同步 Player ID。接收方需要用 ID 查询 API。

---

## 序列化的实际字节数

> ⚠️ **重要**:`size` 表是 **内存占用**,序列化时 **可能更大**(因为网络开销)。

| 变量类型 | 内存大小 | 实际网络字节(含开销) |
|---------|---------|-------------------|
| `bool` | 1 byte | ≥ 1 byte + header |
| `int` | 4 bytes | ≥ 4 bytes + header |
| `Vector3` | 12 bytes | ≥ 12 bytes + header |
| `string "hello"` | 10 bytes | 10 + 长度前缀 + header |
| `byte[100]` | 100 bytes | 100 + 4 长度前缀 + header |

**监控方法**:在 `OnPostSerialization` 中检查 `result.byteCount`:

```csharp
public override void OnPostSerialization(SerializationResult result) {
    if (result.success) {
        Debug.Log($"Serialized {result.byteCount} bytes");
    }
}
```

---

## 同步模式详解

### Continuous Sync

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Continuous)]
public class HealthBar : UdonSharpBehaviour {
    [UdonSynced] private float _healthPercent;
    
    public void TakeDamage(float amount) {
        _healthPercent -= amount;
        // 无需 RequestSerialization,自动每帧同步
    }
}
```

| 维度 | 说明 |
|------|------|
| **更新时机** | 每帧自动(可插值) |
| **带宽** | ~200 bytes/serialization 上限 |
| **中间值** | VRChat 内部差值优化(中间帧不全部发) |
| **适合** | 高频变化(进度条、Transform 跟随) |
| **不适合** | 离散状态(浪费带宽) |

> **VRChat 优化**:Continuous 自动压缩连续帧,丢失的中间值会在接收端补间。

### Manual Sync

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Score : UdonSharpBehaviour {
    [UdonSynced] private int _value;
    
    public void AddPoint() {
        _value++;
        RequestSerialization();  // 必须显式调用
    }
}
```

| 维度 | 说明 |
|------|------|
| **更新时机** | `RequestSerialization()` 调用时 |
| **带宽** | 280,496 bytes/serialization 上限 |
| **频率控制** | 由开发者决定(可节流) |
| **适合** | 离散状态、关键数据 |
| **不适合** | 高频变化(需要每次手动调用) |

> **常见 Bug**:**忘记 `RequestSerialization()`**——这是 VRChat Networking 第一大错误。

### NoVariableSync(默认)

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.NoVariableSync)]
public class LocalOnly : UdonSharpBehaviour {
    // [UdonSynced] 字段不会被同步
    // 只能通过 NetworkEvent 通信
}
```

| 维度 | 说明 |
|------|------|
| **同步字段** | ❌ 全部忽略 |
| **事件** | ✅ 仍可发送/接收 |
| **适合** | 纯 UI、纯本地计算 |

---

## UdonSyncMode 插值模式(SDK 3.8.1+)

控制 `[UdonSynced]` 字段在网络同步时的插值行为:

```csharp
[UdonSynced] public bool toggle;                    // 默认 None
[UdonSynced(UdonSyncMode.Linear)] public float progress;  // 线性插值
[UdonSynced(UdonSyncMode.Smooth)] public Vector3 pos;     // 平滑插值
[UdonSynced(UdonSyncMode.NotSynced)] public int localOnly; // 不同步
```

| Mode | 说明 | 适用场景 |
|------|------|---------|
| `None` | 无插值(默认) | 离散状态、开关、枚举值 |
| `Linear` | 线性插值 (lerp) | 连续位置、速度 |
| `Smooth` | 平滑插值 | 需要更自然过渡的值 |
| `NotSynced` | 显式不同步 | 本地计算或手动同步 |

> **注意**:`NotSynced` 用于需要本地计算后手动同步的场景,与 `BehaviourSyncMode.None` 不同。

---

## FieldChangeCallback 机制

**自动监听变量变化的回调**(SDK 1.0+):

```csharp
[UdonSynced, FieldChangeCallback(nameof(Score))]
private int _score = 0;

public int Score {
    get => _score;
    set {
        _score = value;
        // 任何地方修改 _score 都会触发这个 setter
        OnScoreChanged();
    }
}

private void OnScoreChanged() {
    // 更新 UI、音效等
}
```

### 关键规则

| 规则 | 说明 |
|------|------|
| **数组内容变化不触发** | 数组引用未变,内容修改不会触发 |
| **触发时机** | 变量写入时立即触发,先于 `OnDeserialization` |
| **跨字段不一致** | 触发时其他变量可能未更新完 |
| **Owner/Non-Owner 都会触发** | 包括网络同步接收 |

---

## 数组同步的陷阱

```csharp
// ❌ 错误:未初始化的数组
[UdonSynced] private int[] _data;  // null!不同步!

// ✅ 正确:初始化数组
[UdonSynced] private int[] _data = new int[10];

// ✅ 正确:空数组
[UdonSynced] private string[] _items = new string[0];
```

> ⚠️ **最关键规则**:**未初始化的同步数组 = 不同步**(行为静默失败!)。必须用 `OnPostSerialization` 验证。

---

## 多个 UdonBehaviour 行为

> 当一个 GameObject 上有 **多个 UdonBehaviour** 时,同步行为取 **最严格的设置**。

```
┌──────────────────────────────────────┐
│ GameObject:                          │
│  ├─ UdonBehaviour A (Manual)         │ → 整体:Manual
│  └─ UdonBehaviour B (Continuous)     │   (A 比 B 严格)
└──────────────────────────────────────┘
```

**规则**:`NoVariableSync` > `Manual` > `Continuous`

> **设计建议**:为每个 UdonBehaviour 选择合适的模式,避免一个 Continuous 把所有变量降级为 Manual。

---

## 可见性优先级(Visibility Prioritization)

> **VRChat 内部优化**:**当前对本地用户可见的同步对象优先同步**。

- VRChat 周期性检查所有 `Mesh Renderer` 子物体的可见性
- 用于质量服务(QoS)和网络负载均衡
- 不可见对象可能减少同步频率(VRChat 内部决策)

**应用**:性能优化时,可以利用摄像机视锥外对象同步较慢的特性。

---

## Late Joiner 同步保证

| 同步模式 | Late Joiner 收到值 | 时机 |
|---------|------------------|------|
| Manual | 最近一次成功序列化的值 | 加入实例时 |
| Continuous | 最新值 | 加入实例时 |
| NoVariableSync | 默认值(变量未发送) | N/A |

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Door : UdonSharpBehaviour {
    [UdonSynced] private bool _isOpen = false;  // Late Joiner 默认 false
    
    public override void OnDeserialization() {
        // Late Joiner 收到后,这里被调用
        // 应用 _isOpen 状态
        animator.SetBool("IsOpen", _isOpen);
    }
}
```

---

## 典型模式

### 模式 1:同步简单状态

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class LightSwitch : UdonSharpBehaviour {
    [UdonSynced, FieldChangeCallback(nameof(IsOn))]
    private bool _isOn = false;
    
    public bool IsOn {
        get => _isOn;
        set { _isOn = value; ApplyState(); }
    }
    
    public override void Interact() {
        // 不需要 owner 检查,因为只改 _isOn(RequestSerialization 需要 owner)
        SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(ToggleLight));
    }
    
    [NetworkCallable(maxEventsPerSecond: 5)]
    public void ToggleLight() {
        if (!Networking.IsOwner(gameObject)) return;
        IsOn = !IsOn;
        RequestSerialization();
    }
    
    private void ApplyState() {
        light.enabled = IsOn;
    }
}
```

### 模式 2:同步连续 Transform(用插值)

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Continuous)]
public class SyncedTransform : UdonSharpBehaviour {
    [UdonSynced(UdonSyncMode.Linear)] private Vector3 _position;
    [UdonSynced(UdonSyncMode.Smooth)] private Quaternion _rotation;
    
    void Update() {
        // Owner:更新 synced 变量
        if (Networking.IsOwner(gameObject)) {
            _position = transform.position;
            _rotation = transform.rotation;
        } else {
            // Non-Owner:使用 sync 插值(无需手动处理)
            // Unity 会通过 UdonSyncMode 自动应用
        }
    }
}
```

### 模式 3:位域压缩

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class FlagController : UdonSharpBehaviour {
    [UdonSynced] private byte _flags;  // 8 个 bool 占 1 byte
    
    public const byte FLAG_ACTIVE  = 1 << 0;  // 0b00000001
    public const byte FLAG_HIDDEN  = 1 << 1;  // 0b00000010
    public const byte FLAG_LOCKED  = 1 << 2;  // 0b00000100
    // 节省 7 bytes vs 8 个 bool
}
```

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| 数组未初始化 | 🔴 Critical | 静默失败,不同步 |
| 忘记 RequestSerialization | 🔴 Critical | Manual 模式最常见 bug |
| 同步引用类型 | 🔴 Critical | 引用同步只同步 ID |
| 同步超大 string | 🟠 High | 占用大量带宽配额 |
| 跨版本字段顺序变化 | 🔴 Critical | 见 compatibility.md |
| 同步频率超限 | 🟠 High | 触发拥塞,IsClogged = true |
| 同步多 UdonBehaviour 互相干扰 | 🟡 Medium | 取最严格模式 |
| FieldChangeCallback 误用 | 🟡 Medium | 数组内容变化不触发 |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/compatibility.md` | 字段增删与兼容性 |
| `memory/world/udon/networking/network-details.md` | 序列化字节数详解 |
| `memory/world/udon/networking/performance.md` | 带宽优化 |
| `memory/api/networking.md` | API 速查 |
| `memory/patterns/bit-packed-flags.md` | 位域压缩模式 |
| `memory/patterns/manual-sync-state.md` | Manual Sync 模式 |
