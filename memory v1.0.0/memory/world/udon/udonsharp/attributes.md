# UdonSharp Attributes

> Type: API REFERENCE
> Domain: World
> Source: creators.vrchat.com/worlds/udon/udonsharp/attributes
> SDK Version: 3.10.x
> Last Updated (官方): 2025-04-28
> Last Updated (本地化): 2026-06-15
> Confidence: High（UdonSynced 系列）/ Medium（NetworkCallable）

---

## Domain Detection

- **领域**: World
- **子领域**: Udon VM / 同步系统
- **核心服务对象**: U# 工程师

---

## 概述

**【FACT】** Attributes 用于扩展 UdonSharp 类、字段、方法的功能。UdonSharp **新增**了若干专用 Attribute，**同时支持** 大量 C# 和 Unity 已有的 Attribute。

**推荐资源**：[Varneon's UdonSharp Development Practices — Attributes](https://vrclibrary.com/wiki/books/varneons-udonsharp-development-practices/page/attributes)

---

## 1. UdonSharp 专用 Attributes

**【FACT - 官方 attributes 页面】** 仅以下 4 个属性由 U# / VRChat SDK 提供：

| Attribute | 命名空间 | 用途 |
|-----------|---------|------|
| `UdonSynced` | `UdonSharp` | 同步字段到所有玩家 |
| `UdonSyncMode` | `UdonSharp` | 同步模式枚举（None/Linear/Smooth） |
| `UdonBehaviourSyncMode` | `UdonSharp` | 设置整个 Behaviour 的同步模式 |
| `BehaviourSyncMode` | `UdonSharp` | 同步模式枚举（Any/Continuous/Manual/None/NoVariableSync） |

> **【未确认】** 官方 attributes 页面未单独列出 `NetworkCallable` 和 `RecursiveMethod`，但这两者在实践中确实存在。详见 §3。

---

## 2. UdonSynced 详解

### 2.1 签名

```csharp
[UdonSynced]
[UdonSynced(UdonSyncMode mode)]
```

**用途**：标记字段在网络上**为所有玩家同步**。

**【FACT】** 详细同步机制见 [memory/api/networking.md](../../../api/networking.md)。

### 2.2 示例

```csharp
using UdonSharp;
using VRC.SDKBase;

public class Example : UdonSharpBehaviour
{
    [UdonSynced]
    public bool synchronizedBoolean;          // 默认模式: None（瞬时切换）

    [UdonSynced(UdonSyncMode.Linear)]
    public float synchronizedFloat;           // 线性插值同步
}
```

### 2.3 同步模式（UdonSyncMode 枚举）

**【FACT - 官方】** 4 种模式：

| 模式 | 说明 |
|------|------|
| `None` | **默认**，不插值，值变化时立即生效 |
| `Linear` | 线性插值（在旧值和新值之间平滑过渡） |
| `Smooth` | 平滑插值（更柔和的过渡曲线） |
| `_NotSynced_` | **默认值**（未使用 `[UdonSynced]` 时） |

### 2.4 同步模式选择

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 布尔开关、状态标志 | `None` | 离散值无需插值 |
| 浮点位置/缩放/音量 | `Linear` | 线性最直观 |
| 相机/动画参数 | `Smooth` | 平滑曲线更自然 |
| 调试用临时值 | 不加 `[UdonSynced]` | `_NotSynced_` 避免意外同步 |

> **【推断】** `Smooth` 模式的具体插值算法未在官方文档中明确，与 Unity 的 SmoothDamp 类似但行为可能有差异。

---

## 3. UdonBehaviourSyncMode 详解

### 3.1 签名

```csharp
[UdonBehaviourSyncMode]
[UdonBehaviourSyncMode(BehaviourSyncMode mode)]
```

**用途**：对**整个 UdonBehaviour** 选择同步模式，影响该类所有同步字段。

**【FACT】** 添加此 Attribute 后，UdonSharp 会在 Unity Inspector 中**隐藏**同步模式下拉菜单。

**【FACT】** 同时启用**额外验证**，确保同步变量与所选模式兼容。

### 3.2 示例

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Example : UdonSharpBehaviour
{
    // 此类的所有 [UdonSynced] 字段都按 Manual 模式处理
}
```

### 3.3 BehaviourSyncMode 枚举（5 种模式）

**【FACT - 官方】**

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| `Any` | **默认**，不强制，可在 Unity 中自由选择 | 通用脚本 |
| `Continuous` | 自动高频更新，但可能因节省带宽而**不总是可靠** | 持续状态（位置/旋转） |
| `Manual` | 由用户**手动**调用 `RequestSerialization()` 触发，更低频但**可靠** | 离散事件、状态切换 |
| `None` | **强制**该 Behaviour 无同步变量，UI 隐藏选择下拉；**`SendCustomNetworkEvent` / `NetworkCalling` 在此模式下不工作** | 纯本地逻辑、UI |
| `NoVariableSync` | **强制**无同步变量，但可在 Manual 或 Continuous 的 GameObject 上使用 | 本地控制、UI 转发(见 [多机位导演系统模式(参考工程)](../../../../FACT.md#12-novariablesync-ui-转发模式参考工程)) |

### 3.4 模式选择决策树

```
需要网络同步变量？
├─ 否 → [UdonBehaviourSyncMode(None)]
│  └─ 仍需发送 NetworkEvent？→ 必须改为 Manual（None 不支持 NetworkEvent）
├─ 是
│  ├─ 高频更新（位置/旋转）→ [UdonBehaviourSyncMode(Continuous)]
│  └─ 低频、事件驱动 → [UdonBehaviourSyncMode(Manual)] + 主动 RequestSerialization
└─ 不确定 → 用 Any（默认），后期收紧
```

> **【R-HIGH】** `None` 模式**无法**使用 `SendCustomNetworkEvent` 或 `NetworkCallable`，是常见踩坑点。详见 [memory/api/networking.md](../../../api/networking.md)。

---

## 4. 与已有知识库的关系

| 现有知识库 | 应补充/引用 |
|-----------|----------|
| `memory/api/networking.md` | **核心** — 详细的 UdonSynced、RequestSerialization、NetworkEvent、NetworkCallable 机制 |
| `memory/patterns/manual-sync-state.md` | 引用本文 §3.3 `Manual` 模式 |
| `memory/patterns/owner-authoritative-interaction.md` | 引用本文 §3.3 `Manual` 模式 |
| `memory/rules/udonsharp-language-limits.md` | 引用本文 §2.3 同步模式 |
| `memory/api/udonsharp-runtime.md` | FieldChangeCallback 配合 [UdonSynced] 使用 |
| `memory/journal/` | 待积累实际使用案例 |

---

## 5. 未在官方 attributes 页面列出但实践中使用的 Attribute

### 5.1 `[RecursiveMethod]`

**【FACT - index.md 提及】** 用于允许**递归方法调用**。

```csharp
using UdonSharp;

public class RecursiveExample : UdonSharpBehaviour
{
    [RecursiveMethod]
    public int Factorial(int n)
    {
        if (n <= 1) return 1;
        return n * Factorial(n - 1);
    }
}
```

> **【未确认】** 官方 attributes 页面未列出此 Attribute，但 index.md 明确提及"Recursive method calls are supported via the `[RecursiveMethod]` attribute"。

### 5.2 `[NetworkCallable]` (SDK 3.8.1+)

**【FACT - memory/api/networking.md 已记录】** 用于声明方法可**远程调用并传递参数**。

```csharp
using UdonSharp;
using VRC.SDK3.UdonNetworkCalling;

public class PlayerStats : UdonSharpBehaviour
{
    [NetworkCallable]
    public void SetHealth(float newHealth)
    {
        // 接收远程调用，参数被序列化
    }
}

// 调用方
NetworkCalling.SendCustomNetworkEvent(
    (IUdonEventReceiver)target, 
    NetworkEventTarget.All, 
    "SetHealth", 
    100f
);
```

> **【未确认】** 官方 attributes 页面未列出此 Attribute，详细信息见 `memory/api/networking.md`。

### 5.3 `[FieldChangeCallback]`

**【FACT - memory/api/udonsharp-runtime.md 已记录】** 字段变化时**自动触发回调**。

```csharp
[UdonSynced, FieldChangeCallback(nameof(OnToggleChanged))]
private bool _syncedToggle;

public bool SyncedToggle
{
    set { _syncedToggle = value; toggleObject.SetActive(value); }
    get => _syncedToggle;
}

private void OnToggleChanged() { /* 自动调用 */ }
```

> **【未确认】** 官方 attributes 页面未列出此 Attribute，属于 U# 运行时扩展。

---

## 6. 标准 C# / Unity Attributes（U# 支持）

**【FACT - 通用知识】** U# 同时支持大量 C# / Unity 标准 Attribute，常用：

| Attribute | 用途 | 示例 |
|-----------|------|------|
| `[Header("...")]` | Inspector 分组标题 | `[Header("Settings")]` |
| `[SerializeField]` | 强制序列化私有字段 | `[SerializeField] private int _count;` |
| `[Tooltip("...")]` | 字段悬停提示 | `[Tooltip("Max players")] public int maxPlayers;` |
| `[Range(min, max)]` | 数值范围滑块 | `[Range(0, 100)] public int percent;` |
| `[HideInInspector]` | Inspector 隐藏字段 | `[HideInInspector] public int _cache;` |
| `[Space]` | Inspector 间距 | `[Space(10)]` |
| `[DefaultExecutionOrder]` | 控制 Update 顺序 | `[DefaultExecutionOrder(100)]` |

> **【推断】** 以上 Attribute 由 Unity 序列化系统处理，U# 透传给 Unity。完整 Unity Attribute 列表不在 U# 文档范围内。

---

## 7. 风险与未知

### 风险

- **【R-HIGH】** `[UdonBehaviourSyncMode(None)]` 静默**禁用**所有 NetworkEvent 调用
- **【R-MED】** `[UdonSynced(UdonSyncMode.Linear)]` 在 Master 端表现为瞬时切换（无插值目标）
- **【R-LOW】** 字段未标 `[UdonSynced]` 时为 `_NotSynced_`，容易在重构时遗漏

### 未知

- **【未确认】** `NetworkCallable`、`RecursiveMethod`、`FieldChangeCallback` 官方 attributes 页面未列出，需通过源码/UdonSharp 文档间接确认
- **【未确认】** UdonSyncMode 枚举的 `Smooth` 实现细节（插值系数、是否可配置）
- **【未确认】** 多个 `[UdonSynced]` 字段在同一次 `RequestSerialization` 调用中的**带宽聚合**行为（需配合 `memory/api/networking.md` 带宽限制理解）
