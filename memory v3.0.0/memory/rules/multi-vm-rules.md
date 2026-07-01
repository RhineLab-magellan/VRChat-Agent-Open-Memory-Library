---
title: "Rule Set: Multi-VM Collaboration Rules"
category: rules
knowledge_level: applied
status: active
source: "Udon VM 架构理解 + 项目实测"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - rules
  - rules
  - udonsharp
aliases:
  - "Rule Set： Multi-VM Collaboration Rules"
  - "Rule Set: Multi-VM Collaboration Rules"
related:
  - udon-vm-architecture.md
  - udonsharp-deep-pitfalls.md
  - udonsharp-language-limits.md
  - networking-rules.md
  - performance-rules.md
---
# Rule Set: Multi-VM Collaboration Rules


---

## 核心认知

每个挂载在 GameObject 上的 UdonBehaviour 是一个独立的 Udon 程序实例。每个 UdonBehaviour 有自己的：

- 事件入口
- 变量存储
- 同步上下文
- 执行环境

**多个 UdonBehaviour 之间的通信不是免费的函数调用，而是跨 VM 边界操作。**

---

## RULE-MV-01: Hot Path Logic In One Behaviour

### Rule
高频逻辑应集中在一个 UdonBehaviour 中。低频或冷路径逻辑才适合拆分为独立 Behaviour。

### Reason
跨 UdonBehaviour 调用涉及：
- UdonBehaviour 引用查找
- 跨 VM 方法派发
- 可能的序列化/反序列化
- 调试困难

### Decision Tree
```text
这段逻辑的执行频率？
├── 每帧 → 必须在同一个 Behaviour
├── 高频事件（每秒多次）→ 尽量在同一 Behaviour
├── 中频事件（每秒一次到几次）→ 可以拆分，需评估
└── 低频事件（偶尔触发）→ 可以拆分
```

---

## RULE-MV-02: Minimize Cross-Behaviour Calls

### Rule
减少热路径中的跨 UdonBehaviour 调用次数。

### How
- 用 `[SerializeField]` 预绑定引用，避免运行时查找
- 批量数据传递（一次传数组），避免多次单值调用
- 将需要频繁协作的逻辑合并进同一 Behaviour

---

## RULE-MV-03: SerializeField Over Runtime Find

### Rule
跨 Behaviour 引用优先使用 `[SerializeField]` 在编辑器中绑定，避免 `GetComponent()` 查找。

### Reason
`[SerializeField]` 在编译时/场景加载时解析，没有运行时成本。
`GetComponent()` 在 Udon VM 中是逐步执行的组件查找。

---

## RULE-MV-04: Centralize Networking

### Rule
网络同步逻辑应集中管理，避免分散在多个 Behaviour 中各做各的同步。

### Reason
- 减少 `RequestSerialization()` 的调用次数
- 减少同步变量的总数
- 便于 NetLog 和调试
- 避免多个 Behaviour 对同一逻辑状态的竞争写入

---

## RULE-MV-05: Avoid Chained Event Dispatching

### Rule
避免 A.SendCustomEvent → B.Method → B.SendCustomEvent → C.Method 的链式事件派发。

### Reason
- 每次 SendCustomEvent 跨 VM 派发
- 链式派发延误会累积
- 难以跟踪执行顺序
- 可能导致意外的递归

### Prefer
- 使用一个中心 Behaviour 接收事件，直接调用已绑定的其他 Behaviour
- 使用 int 状态机统一管理事件响应

---

## RULE-MV-06: Understand State Sharing Cost

### Rule
多个 Behaviour 共享同一高频状态时，需要评估合并的可能性。

### Analysis
```text
场景: 3 个 Behaviour 都需要读取玩家分数

Bad: 每个 Behaviour 各维护一份分数，通过 SendCustomEvent 同步
Good: 1 个 Behaviour 持有分数，其他 Behaviour 通过 SerializeField 直接引用读取
Better: 分数相关的 UI、音效、动画逻辑全部合并进 1 个 Behaviour
```

---

## RULE-MV-07: Minimize Runtime UdonBehaviour Instantiation

### Rule
减少运行时 Instantiate 带 UdonBehaviour 的 prefab。每次 Instantiate 不仅创建 GameObject，还需要创建新的 Udon VM 实例。

### Cost Data (社区实测)
- Instantiate prefab: ~1ms
- Udon VM 创建: ~1ms
- **合计每个 Udon prefab 实例: ~2ms**

### Fix
- 使用对象池模式（VRCObjectPool 或简易动态数组池）
- 预分配最大化数量，通过 SetActive 控制可见性
- 通过 `SetProgramVariable` + `SendCustomEvent` 重新初始化已存在的实例
- 用完回收而非 Destroy

### Pattern
参见 `patterns/unorthodox-patterns.md` Pattern 3: 动态数组简易对象池

---

## RULE-MV-08: Toggle 数组减少按钮 VM 数量

### Rule
批量相同功能的 UI 按钮使用 Toggle 数组代替每个按钮独立挂载 UdonBehaviour。

### Pattern
一个 UdonBehaviour 管理一个 Toggle 数组。Toggle 触发时遍历找到 isOn=true 的索引，索引即为参数。

### Benefit
N 个按钮从 N 个 UdonBehaviour 减少到 1 个，节省 N-1 个 Udon VM。

---

## RULE-MV-09: 并行线程卸载计算（高风险技术）

### Rule
Udon VM 是单线程的，但 Unity 的其他子系统（音频线程、GPU）在独立上下文中运行。理论上可将计算卸载到这些并行上下文。**但这些技术均属高风险/未验证范畴，需极度谨慎。**

### Three Approaches

| 技术 | 验证状态 | 并行上下文 | 主要风险 |
|---|---|---|---|
| Animator BlendTree | ❌ 未验证 Idea | 未知 | 可能仍在主线程，完全未实测 |
| OnAudioFilterRead | ✅ 特性确认 | 音频线程 | 与主线程数据竞争，可能导致并行事故 |
| GPU Callback | ✅ 社区使用 | GPU | 延迟 + 仅适合批量数据 |

### 核心原则
- 所有并行卸载都**提高了 Udon 运行时整体代价**——只是从主线程转移到并行线程
- 总 CPU 预算不变，仅在主线程是明确瓶颈时才有意义
- 必须保证并行线程与 Udon 主线程操作的数据完全隔离

### Pattern
参见 `patterns/unorthodox-patterns.md` Pattern 4
