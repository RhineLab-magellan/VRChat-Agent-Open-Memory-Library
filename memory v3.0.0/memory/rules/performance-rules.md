---
title: "Rule Set: Performance Rules"
category: rules
knowledge_level: applied
status: active
source: "VRChat 官方文档 + Udon VM 解释执行特性 + Udon VM 逆向研究 (vrcd.org.cn)"
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
tags:
  - rules
  - rules
  - animator
  - performance
  - pickup
  - serialization
aliases:
  - 性能
  - "Rule Set: Performance Rules"
related:
  - vrchat-api-exposure.md
  - networking-rules.md
  - multi-vm-rules.md
  - udon-vm-architecture.md
  - udonsharp-deep-pitfalls.md
---
# Rule Set: Performance Rules


---

## 性能分析三轴

所有性能判断必须从三个维度分析：

1. **代码执行步骤** — Udon VM 是**纯解释器**（9 条指令，无 JIT），每条指令都有装箱/拆箱成本
2. **网络带宽 / 同步方式** — 同步频率、字段数量、同步模式选择
3. **多 Udon VM 协作损耗** — 跨 Behaviour 调用、跨 VM 通信成本

### 性能基准 (来自官方文档)
> **Udon 比标准 C# 慢 200x ~ 1000x。**
> - 40+ 迭代的逻辑建议用 Animation 替代（不是 Animator Script，是 Unity Animation 组件）
> - 优先使用 Unity/VRC 内置组件而非 Udon 实现

### VM 级根本原因 (详见 `udon-vm-architecture.md`)

| 现象 | 根因 |
|---|---|
| 变量访问慢 | 每个变量是独立装箱的 StrongBox<T>，读=拆箱，写=装箱 |
| 外部调用慢 | EXTERN 指令走完整的签名解析→委托查找→委托调用链 |
| 整体慢 | 纯解释执行，无 JIT、无循环展开、无热点编译 |
| 10 秒超时 | `CheckExecutionTimeLimit` 硬限制，触发后 Behaviour 永久停止 |

---


## RULE-PF-01: Event-Driven Over Update()

### Rule
能由事件触发的逻辑，不应放入无条件的 `Update()`。

### Reason
`Update()` 每帧执行。即使早期 return，仍然消耗一次方法调用和条件检查。事件驱动代码只在需要时执行。

### Prefer
- `Interact()` — 玩家点击
- `OnPlayerTriggerEnter/Exit/Stay` — 触发区域
- `OnPickup/OnDrop/OnPickupUseDown/Up` — 拾取交互
- `OnDeserialization()` — 收到网络更新
- `OnOwnershipTransferred()` — ownership 变化
- `FieldChangeCallback` — 特定字段变化
- `SendCustomEvent` / `SendCustomEventDelayedSeconds` — 自定义事件

---


## RULE-PF-02: Cache References At Start

### Rule
在 `Start()` 中缓存所有外部引用，热路径中不做组件查找。

### Reason
`GetComponent()`, `GameObject.Find()`, `Transform.Find()` 等查找操作在 Udon VM 中执行步骤多。每帧执行会造成显著性能压力。

### Code
```csharp
// ✅ 正确 — Start 中缓存
[SerializeField] private Transform _target;  // 优先 SerializeField
private UdonBehaviour _otherBehaviour;
void Start() {
    _otherBehaviour = otherObject.GetComponent<UdonBehaviour>();
}

// ❌ 错误 — Update 中查找
void Update() {
    var t = GameObject.Find("Player").transform;
}
```

---


## RULE-PF-02b: Prefab Instantiation Cost

### Rule
运行时 `Instantiate()` 带 UdonBehaviour 的 prefab 有两段成本：
1. GameObject / Component 创建: ~1ms
2. Udon VM 实例创建: ~1ms
**合计每个 Udon prefab 约 2ms**。

### Fix
- 对象池预分配（VRCObjectPool 或动态数组池）
- 通过 `SetActive(true/false)` 控制可用性
- `SetProgramVariable` + `SendCustomEvent` 重新初始化已存在实例而非新建
- 在不需要时 `Destroy` 冗余 VM 释放资源

### Pattern
参见 `patterns/unorthodox-patterns.md` Pattern 3

---


## RULE-PF-03: Throttle Update

### Rule
高频 `Update()` 逻辑需要节流。

### Reason
`Update()` 在 Udon VM 中每帧执行。90fps = 每秒 90 次完整解释执行。

### Pattern
```csharp
private float _nextUpdateTime;
private const float UPDATE_INTERVAL = 0.1f; // 10Hz

void Update() {
    float t = Time.time;
    if (t < _nextUpdateTime) return;
    _nextUpdateTime = t + UPDATE_INTERVAL;
    // 实际逻辑
}
```

---


## RULE-PF-04: Avoid String Operations In Hot Path

### Rule
高频路径中避免字符串拼接、比较和格式化。

### Reason
Udon VM 中字符串操作成本高。每次拼接都可能创建新字符串对象。

### Prefer
- 用 `int`/`enum` 状态代替字符串状态
- 用 `int` switch/if 代替字符串比较
- 预缓存常用字符串

---


## RULE-PF-05: Minimize Array Operations

### Rule
避免不必要的数组遍历、重排、复制。

### Reason
Udon VM 对数组操作的解释执行成本随数组大小线性增长。

### Tips
- 用 `break` 提前退出循环
- 在状态变化时更新数组，不在 Update 中持续遍历
- 考虑用 `DataList`/`DataDictionary` 替代大数组查找（但需注意其自身成本）

---


## RULE-PF-06: Use Bit Packing For Multiple Booleans

### Rule
多个 bool 字段应压缩为单个 int 的 bit flags。

### Reason
减少同步变量数量和带宽。

### Pattern
参见 `patterns/bit-packed-flags.md`

---


## RULE-PF-07: Prefer int/Enum State Over String State

### Rule
状态字段使用 `int` 或 `enum`（底层为 int），不使用字符串。

### Reason
- int 比较比字符串比较快
- int 同步占用固定 4 字节，字符串可能很大
- int 可以直接用 switch

---


## RULE-PF-08: Defer Non-Critical Work

### Rule
非关键逻辑使用 `SendCustomEventDelayedSeconds` 延迟执行。

### Reason
将执行步骤分散到不同帧，避免单帧峰值。

### Pattern
```csharp
void OnStateChanged() {
    // 关键：立即更新
    UpdateCriticalVisuals();
    // 非关键：延迟执行
    SendCustomEventDelayedSeconds(nameof(_UpdateNonCriticalVisuals), 0.05f);
}
```

---


## RULE-PF-09: Minimize EXTERN Calls In Hot Path

### Rule
热路径（Update、FixedUpdate、LateUpdate、PostLateUpdate）中极力减少任何 EXTERN 调用。

### Reason (VM 级根因)
EXTERN 是 Udon VM 最昂贵的单指令。每次调用走完整的外部调用链：堆签名查找 → UdonWrapper 解析 → 委托获取 → 委托 invoke → 返回。在 Update 中每帧调用 `Debug.Log()`、`GetComponent()`、`Animator.SetFloat()` 等都会累积巨额成本。

### Fix
- **缓存引用**: Start 中缓存 VRCPlayerApi、组件引用，不在 Update 中查找
- **批量操作**: 将多个 Animator 参数在一次调用中设置
- **移除 Update 中的 Debug.Log**: 用条件编译或 `if (_debugMode && Time.frameCount % 60 == 0)` 限制
- **根本原则**: Update 中只做纯计算（变量读写、if/for），不调任何外部 API
- **Animation Event 替代 Update 轮询**: 用 Animator 的 Animation Event 触发 Udon 回调代替 Update 轮询
- **参考**: `rules/udon-vm-architecture.md` 第 3 节 EXTERN 完整调用链

---


## RULE-PF-10: Understand Boxing/Unboxing Cost of Every Variable Access

### Rule
在 Udon VM 中，每一个变量的每次读写都涉及 `StrongBox<T>` 的装箱/拆箱。`int a = b;` 在 Udon VM 中是 3-4 条 VM 指令 + 堆查找 + 类型匹配 + 拆箱 + 装箱，不是一条 CPU 指令。

### Impact
- 频繁的变量读写有明显成本
- 合并频繁一起访问的变量到数组，减少独立变量数量
- 避免不必要的变量拷贝

### Reference
`rules/udon-vm-architecture.md` 第 2.1 节 UdonHeap 装箱机制
