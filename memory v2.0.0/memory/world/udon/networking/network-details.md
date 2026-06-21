---
title: Networking Specs & Tricks 内部细节
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - networking
  - udon
  - sync
  - serialization

aliases:
  - "网络"

related:
  - world/udon/networking/index.md
  - world/udon/networking/variables.md
  - world/udon/networking/performance.md
  - world/udon/networking/debugging.md
  - world/udon/networking/network-components.md
  - api/networking.md

source: VRChat 官方 Creator Docs (Networking Specs & Tricks)
source_type: official
version: 1.0
last_review: 2026-06-15
confidence: High
---
# Networking Specs & Tricks 内部细节

> SDK Version: 3.x
---

## 简介

> **作者提示**:"Networking in Udon can be challenging! Try to keep things simple until you're more experienced."

本文档深入 **字节级** 网络细节,涵盖:
- 带宽硬限制(权威数据)
- Manual vs Continuous 内部差异
- 完整字段类型序列化表
- 多个 UdonBehaviour 行为
- 数组初始化陷阱
- 可见性优先级

---

## 一、带宽限制(权威数据)

> ⚠️ **所有规格可能在未来调整**。具体每对象数据见 **Debug Menu 6**。

### 硬限制

| 限制类型 | 数值 |
|---------|------|
| **总带宽** | **~11 KB/s** |
| **Manual Sync** | **280,496 bytes/serialization** |
| **Continuous Sync** | **~200 bytes/serialization** |

### 超出限制的行为

```
数据量超限
  → IsClogged = true
    │
    ├─ Continuous: 序列化失败,日志错误
    └─ Manual: 事件缓存,延后重试
      │
      └─ 业务逻辑继续执行
         但数据未发送/接收
```

| Sync Mode | 超出限制行为 | 业务逻辑 |
|-----------|------------|---------|
| **Continuous** | 序列化失败,日志记录错误 | ✅ 继续执行 |
| **Manual** | 事件缓存,稍后重试 | ✅ 继续执行 |

> ⚠️ **关键风险**:数据未发送,但本地逻辑继续执行——玩家看到的状态 **不一致**。

---

## 二、Continuous Synchronization(持续同步)

### 设计目的

> 用于 **频繁变化且中间值不重要** 的数据(如随机移动的 Transform 位置)。

| 维度 | 说明 |
|------|------|
| 更新时机 | 每帧自动 |
| 中间值 | VRChat **内部差值优化** |
| 带宽限制 | ~200 bytes/serialization |
| Late Joiner | 自动同步最新值 |
| 适合 | Transform、进度条 |

### 内部优化

> **VRChat 自动差值压缩**——连续帧之间不发送所有数据,丢失的中间值在接收端补间。

```
Owner 帧序列:
  F1: pos=(0, 0, 0)
  F2: pos=(0.1, 0, 0)
  F3: pos=(0.2, 0, 0)
  ...

实际发送:
  F1: pos=(0, 0, 0)         ← 完整
  F5: pos=(0.4, 0, 0)       ← 跳帧,差值更新
  F10: pos=(0.8, 0, 0)      ← 继续跳帧
```

> **应用**:让高频变化对象走 Continuous,带宽可接受。

### 适合的场景

| 场景 | 原因 |
|------|------|
| 玩家位置(连续移动) | 中间值不重要 |
| 进度条 | 平滑过渡 |
| 旋转动画 | 中间帧可插值 |
| 音量条 | 连续变化 |

### 不适合的场景

| 场景 | 原因 |
|------|------|
| 门开/关(离散) | 中间值(半开半关)无意义 |
| 分数变化 | 离散整数,中间值无意义 |
| 棋盘位置 | 离散状态 |

---

## 三、Manual Synchronization(手动同步)

### 设计目的

> 用于 **不频繁但快速变化** 的数据,且 **中间值必须正确**(如棋盘棋子位置)。

| 维度 | 说明 |
|------|------|
| 更新时机 | `RequestSerialization()` 显式调用 |
| 频率控制 | 开发者决定(可节流) |
| 带宽限制 | 280,496 bytes/serialization |
| 适合 | 离散状态、关键数据 |

### 内部节流机制

> **关键**:**多次 `RequestSerialization()` 不会合并**——每次都尝试立即发送。

```csharp
// 实际行为
RequestSerialization();  // → 立即尝试发送
RequestSerialization();  // → 立即尝试发送
RequestSerialization();  // → 立即尝试发送
// 3 次独立的序列化尝试,可能被 VRChat 内部节流
```

### 内部行为

> **"Scripts can call RequestSerialization as often as they want, but Udon will wait until enough time has passed before calling OnPreSerialization, sending the data, and calling OnPostSerialization with the result."**

```
RequestSerialization()
  → VRChat 内部判断是否到了发送时间
    → 太频繁? → 缓存,延后
    → 时间到? → 调用 OnPreSerialization
              → 发送数据
              → 调用 OnPostSerialization(SerializationResult)
```

### 适合的场景

| 场景 | 原因 |
|------|------|
| 门开/关 | 离散,中间值不重要 |
| 棋盘棋子 | 关键位置,中间值有误 |
| 玩家分数 | 整数,不能插值 |
| 回合阶段 | 离散状态 |
| 玩家列表 | 关键数据 |

### 减少序列化的技巧

```csharp
// 技巧 1:节流
private float _lastSyncTime = 0;
private const float MIN_INTERVAL = 0.1f;

public void TrySync() {
    if (Time.time - _lastSyncTime < MIN_INTERVAL) return;
    _lastSyncTime = Time.time;
    RequestSerialization();
}

// 技巧 2:变化阈值
private Vector3 _lastPos;
private const float THRESHOLD = 0.1f;

public void TrySync(Vector3 newPos) {
    if (Vector3.Distance(newPos, _lastPos) < THRESHOLD) return;
    _lastPos = newPos;
    _position = newPos;
    RequestSerialization();
}
```

---

## 四、Synced Variables(完整类型表)

> 来源:VRChat 官方 `network-details.md` Specs

> **关于"size"**:**size 是内存占用**,序列化时 **可能传输更多**。例如 `bool` 在内存中 1 bit,网络传输至少 1 byte(8 倍膨胀)。

### Boolean 类型

| 类型 | Size |
|------|------|
| `bool` | 1 byte |

### 整数类型(完整)

| 类型 | 范围 | Size |
|------|------|------|
| `sbyte` | -128 to 127 | 1 byte |
| `byte` | 0 to 255 | 1 byte |
| `short` | -32,768 to 32,767 | 2 bytes |
| `ushort` | 0 to 65,535 | 2 bytes |
| `int` | ±2.15 × 10^9 | 4 bytes |
| `uint` | 0 to 4.29 × 10^9 | 4 bytes |
| `long` | ±9.22 × 10^18 | 8 bytes |
| `ulong` | 0 to 1.84 × 10^19 | 8 bytes |

### 浮点类型

| 类型 | 范围 | 精度 | Size |
|------|------|------|------|
| `float` | ±3.4 × 10^38 | ~6-9 位 | 4 bytes |
| `double` | ±1.7 × 10^308 | ~15-17 位 | 8 bytes |

### Unity 几何类型

| 类型 | 大小 | 等价 |
|------|------|------|
| `Vector2` | 8 bytes | float × 2 |
| `Vector3` | 12 bytes | float × 3 |
| `Vector4` | 16 bytes | float × 4 |
| `Quaternion` | 16 bytes | float × 4 |

### 颜色类型

| 类型 | 大小 | 等价 |
|------|------|------|
| `Color` | 16 bytes | float RGBA |
| `Color32` | 4 bytes | byte RGBA |

### 文本类型

| 类型 | 范围 | 大小 |
|------|------|------|
| `char` | U+0000 to U+FFFF | 2 bytes |
| `string` | same as char | 2 bytes / char |
| `VRCUrl` | U+0000 to U+FFFF | 2 bytes / char |

---

## 五、序列化字节监控

> **"To find out how many bytes of serialized data were, use `byteCount` in the OnPostSerialization event."**

```csharp
public override void OnPostSerialization(SerializationResult result) {
    if (result.success) {
        Debug.Log($"Serialized {result.byteCount} bytes");
    } else {
        Debug.LogError("Serialization failed");
    }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | `bool` | 序列化是否成功 |
| `byteCount` | `int` | 实际发送的字节数 |

> **监控建议**:在生产 World 中记录 `byteCount` 分布,识别带宽热点。

---

## 六、Manual vs Continuous 字节差异

| 维度 | Manual | Continuous |
|------|--------|-----------|
| **每 serialization 上限** | 280,496 bytes | ~200 bytes |
| **序列化频率** | 显式 `RequestSerialization` | 每帧 |
| **总带宽贡献** | 取决于调用频率 | 取决于 200B × 帧数 |
| **优化机制** | 无内部差值 | VRChat 自动差值压缩 |
| **Late Joiner** | 最近一次序列化值 | 最新值 |

### 实际带宽计算

```
场景:100 个 networked 对象,全部用 Manual Sync,每秒 1 次序列化,每次 50 bytes

总带宽:100 × 50 × 1 = 5000 bytes/s = 4.88 KB/s
占 11 KB/s 上限:44%
```

```
场景:100 个 networked 对象,全部用 Continuous,200 bytes/serialization,30fps

总带宽:100 × 200 × 30 = 600,000 bytes/s = 585 KB/s
远超 11 KB/s 上限!→ 严重拥塞
```

> **结论**:**Continuous 只能用于少量对象**(< 10 个,200B 内)。**Manual 适合多数场景**。

---

## 七、多个 UdonBehaviour 行为

> 当一个 GameObject 上有 **多个 UdonBehaviour** 时,行为取 **最严格的设置**。

### 严格性排序

```
NoVariableSync(最严格) > Manual > Continuous(最宽松)
```

### 行为示例

```
┌──────────────────────────────────────┐
│ GameObject:                          │
│  ├─ UdonBehaviour A (Manual)         │
│  └─ UdonBehaviour B (Continuous)     │
└──────────────────────────────────────┘
→ 整体行为:Manual
   (B 的 Continuous 行为被 A 的 Manual 覆盖)
```

### 实际影响

```csharp
// UdonBehaviour A
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class A : UdonSharpBehaviour {
    [UdonSynced] public int _valueA;
}

// UdonBehaviour B
[UdonBehaviourSyncMode(BehaviourSyncMode.Continuous)]
public class B : UdonSharpBehaviour {
    [UdonSynced] public int _valueB;
    
    public void Update() {
        if (Networking.IsOwner(gameObject)) {
            _valueB = Time.frameCount;  // 期望每帧同步
        }
    }
}
// 实际行为:_valueB 也是 Manual(由 A 决定)
// 必须在 B 的某处调用 RequestSerialization() 才能同步
```

> **设计原则**:**为每个 UdonBehaviour 选择合适模式**,避免一个 Manual 把其他 Continuous 降级。

---

## 八、数组同步陷阱

### 核心规则

> **未初始化的 synced 数组 = 不同步(静默失败)**

```csharp
// ❌ 静默失败
[UdonSynced] private int[] _data;  // null!不同步!

// ✅ 正确:初始化
[UdonSynced] private int[] _data = new int[10];

// ✅ 正确:空数组
[UdonSynced] private string[] _items = new string[0];
```

### 诊断方法

```csharp
public override void OnPostSerialization(SerializationResult result) {
    if (!result.success) {
        Debug.LogError("Serialization failed - check synced array initialization!");
    }
}
```

### 数组内容修改 vs 引用替换

```csharp
// ❌ 不会触发 OnVariableChanged(数组引用未变)
public void ModifyItem(int index, int value) {
    _data[index] = value;
}

// ✅ 重新赋值引用
public void ModifyItem(int index, int value) {
    _data[index] = value;
    _data = _data;  // 触发引用"变化"(实际无变化,但 OnVariableChanged 仍可能不触发)
    // 更可靠:用 FieldChangeCallback setter
}
```

> **最可靠**:用 `FieldChangeCallback` 包装数组操作。

---

## 九、可见性优先级(Visibility Prioritization)

> **VRChat 内部优化**:**当前对本地用户可见的同步对象优先同步**。

### 机制

- VRChat 周期性检查所有 `Mesh Renderer` 子物体的可见性
- 用于质量服务(QoS)和网络负载均衡
- 不可见对象可能减少同步频率(VRChat 内部决策)

### 实际应用

| 优化策略 | 效果 |
|---------|------|
| 把远处对象的同步频率降低 | 视锥外对象不浪费带宽 |
| 临时隐藏的对象 | 同步频率自动降低 |
| 不必要的 Mesh Renderer | 移除以避免被检查 |

### 注意

> **不可见对象的同步频率降低是 VRChat 内部决策,不可控**。开发者应自行设计节流逻辑。

---

## 十、Manual Sync 内部时间线

### 完整流程

```
RequestSerialization() 调用
  ↓
VRChat 内部判断:时间到?
  ├─ 否 → 缓存调用,延后
  └─ 是 → 继续
        ↓
      调用 OnPreSerialization()
        ↓
      序列化 [UdonSynced] 变量
        ↓
      发送数据到服务器
        ↓
      调用 OnPostSerialization(SerializationResult)
        ↓
      服务器转发给所有玩家
        ↓
      远端调用 OnDeserialization()
        ↓
      远端更新 [UdonSynced] 变量
        ↓
      触发 FieldChangeCallback(如果配置)
```

### 实际间隔

> **VRChat 内部决定**最小发送间隔——基于数据大小、当前负载、玩家数等。

**经验值**(非官方):
- 极小数据(几个 bytes):约 50ms
- 中等数据(100 bytes):约 100-200ms
- 大数据(1KB+):约 500ms+
- 极小间隔(> 10 Hz)可能被节流

---

## 十一、Continuous 同步的内部时间线

### 简化流程

```
每帧:
  1. VRChat 检查 Owner 的 [UdonSynced] 变量
  2. 与上一帧对比
  3. 变化? → 序列化并发送
  4. 未变化? → 跳过
  5. 内部差值压缩(连续帧合并)
```

> **与 Manual 不同**:**Continuous 的"每帧"是逻辑概念,实际发送可能是多次合并**。

---

## 十二、调试技巧汇总

### 字节数监控

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class ByteMonitor : UdonSharpBehaviour {
    [UdonSynced] private int _a;
    [UdonSynced] private int _b;
    [UdonSynced] private int _c;
    
    private int _serializationCount = 0;
    private int _totalBytes = 0;
    
    public override void OnPostSerialization(SerializationResult result) {
        if (result.success) {
            _serializationCount++;
            _totalBytes += result.byteCount;
            if (_serializationCount % 10 == 0) {
                Debug.Log($"[Monitor] 10 serializations, avg {_totalBytes / 10} bytes");
                _totalBytes = 0;
            }
        }
    }
}
```

### 同步频率监控

```csharp
public class SyncRateMonitor : UdonSharpBehaviour {
    private int _syncCount = 0;
    private float _lastReport = 0;
    
    public override void OnDeserialization() {
        _syncCount++;
    }
    
    void Update() {
        if (Time.time - _lastReport > 1.0f) {
            Debug.Log($"[Rate] {(_syncCount / (Time.time - _lastReport)):F1} syncs/sec");
            _syncCount = 0;
            _lastReport = Time.time;
        }
    }
}
```

---

## 关键公式汇总

### 单对象带宽

```
Manual:  bytes_per_sync × syncs_per_second = bytes/sec
Continuous: bytes_per_serialization × 30 (fps) = bytes/sec
```

### 总体带宽

```
total_bandwidth = Σ all_objects
```

**警告阈值**:
- 接近 11 KB/s → 需要优化
- 超过 11 KB/s → 拥塞

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| 误用 Continuous 同步大对象 | 🔴 Critical | 超出 200B 上限,失败 |
| 数组未初始化 | 🔴 Critical | 静默失败 |
| 多个 UdonBehaviour 互相降级 | 🟠 High | 一个 Manual 影响所有 |
| 假设 Manual 不限频率 | 🟠 High | 内部节流存在 |
| Continuous 内部差值假设 | 🟡 Medium | 中间值可能被合并 |
| `byteCount` 误读 | 🟡 Medium | 不含网络头开销 |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/variables.md` | synced 变量类型 |
| `memory/world/udon/networking/performance.md` | 性能优化 |
| `memory/world/udon/networking/debugging.md` | 调试方法 |
| `memory/world/udon/networking/network-components.md` | VRCObjectSync 等 |
| `memory/api/networking.md` | API 速查 |
