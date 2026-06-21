# Pattern: Slot-Based Parameter Passing (槽位参数传递)

> Type: PATTERN
> Source: ULocalization(参考工程)
> Confidence: High
> SDK Version: 3.10.x
> Last Verified: 2026-06-20
> Reference: `memory/sources/ulocalization.md`

---

## Problem / Context

Udon 的 `SendCustomEvent(methodName)` **不接受参数**。当 UnityEvent listener 需要传入 string / Sprite / int / bool 等参数时，无法直接传递。

传统方案：
- ❌ `SendCustomEvent` 无参数重载
- ❌ 序列化到 synced 变量 → 不必要的网络开销
- ❌ 用全局 Dictionary → 暴露受限

ULocalization 场景：UnityEvent listener 可能要：
- 调 `AudioSource.PlayOneShot(clip)` 传 AudioClip
- 调 `TMP_Text.text = text` 传 string
- 调 `Animator.SetTrigger(name)` 传 string
- 调 `Slider.Select()` 无参
- 调 `VRCPickup.InteractionText = text` 传 string

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| `SendCustomEvent(string)` 无参数 | 无法直接传 string/int/Object |
| 无 `Func<T, R>` | 无法做"传参 + 调用"组合 |
| 无 `params object[]` | 无法做变长参数 |
| 无 Lambda | 无法做延迟绑定 |

---

## Solution

**核心思想**：Shim 预定义固定数量的 `object` 字段作为参数槽位。调用前手动填入，生成的方法从槽位读取。

### 关键机制

#### 1. 三槽位定义

```csharp
// LocalizationShim.cs
public partial class LocalizationShim {
    object _l_t;  // Target: 要操作的对象
    object _l_p;  // Prefab value: 默认/原值
    object _l_a;  // Active value: 运行时新值
}
```

#### 2. 每次分派前填槽

```csharp
// 运行时: 分派一个 LocalizeEvent 的所有 listeners
public void RefreshLocalizeEvent(int localizeEvent) {
    if (localizeEvent < 0) return;
    var localized = _8[localizeEvent];
    if (localized < 0) return;

    // 准备值
    _l_p = GetLocalizedValue(localized);

    // 分派所有 listeners
    var __9 = _9[localizeEvent];    // listener 数量
    var __10 = _10[localizeEvent]; // listener method hash 数组
    var __11 = _11[localizeEvent]; // listener target 对象数组
    var __12 = _12[localizeEvent]; // listener argument 对象数组

    for (var i = 0; i < __9; i++) {
        _l_t = __11[i];   // 填 target
        _l_a = __12[i];   // 填 argument
        SendCustomEvent(__10[i]);  // 调 hash 方法
    }
}
```

#### 3. 生成的方法读槽

```csharp
// LocalizationShim_Generated.cs
public void __0bf0b1b18ad0f865ed8825d48c851014() =>
    ((global::UnityEngine.AI.NavMeshAgent)_l_t).CompleteOffMeshLink();

public void __f1547e55a5c9dd22ff36ce8ac1135bde() =>
    ((global::UnityEngine.AudioSource)_l_t).clip = (global::UnityEngine.AudioClip)_l_p;

public void __f462db2d71719101c7aa431ac56d1195() =>
    ((global::TMPro.TextMeshPro)_l_t).text = (global::System.String)_l_p;

public void __ac7c94b676f0cfeab3122aa5857bed10() =>
    ((global::UnityEngine.Animator)_l_t).SetTrigger((global::System.String)_l_a);
```

#### 4. 类型化包装（运行时无 cast 风险）

- `_l_t` 用 `((ConcreteType)_l_t)` 强制转型 → 生成时已确定类型
- `_l_p` / `_l_a` 用 `((ConcreteType)_l_p)` 强制转型 → 同样

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | 单一 Shim |
| Source of Truth | Editor 端 listener 列表 + 类型表 |
| Sync Type | N/A |
| Synced Variables | 无（纯本地） |
| Mutation Path | Editor 配置 + 运行时调用 |
| Ownership Path | 无 |
| Serialization Path | 无 |
| Receive Path | `SendCustomEvent(hash)` 内部调 |
| Late Joiner | 自动 |
| Conflict Strategy | 无 |
| Bandwidth Budget | 0 |
| Failure Mode | 类型 cast 失败（Udon VM 抛 InvalidCastException） |

---

## Implementation Sketch

```csharp
// === 简化版：3 槽位 ===
public partial class MyDispatcher : UdonSharpBehaviour {
    object _l_t;  // target
    object _l_p;  // prefab value
    object _l_a;  // active value

    // 代码生成的 2 个方法
    public void __hash_set_text() => ((TMP_Text)_l_t).text = (string)_l_p;
    public void __hash_set_clip() => ((AudioSource)_l_t).clip = (AudioClip)_l_p;

    // 分派入口
    public void Dispatch(int listenerIndex) {
        _l_t = _targets[listenerIndex];
        _l_p = _values[listenerIndex];
        _l_a = _arguments[listenerIndex];
        SendCustomEvent(_methodHashes[listenerIndex]);
    }
}
```

---

## When To Use

✅ **适用**：
- UnityEvent listener 需要传参
- 参数数量 ≤ 3（`target` + `value` + 可选 `arg`）
- 参数类型固定（编译期可知）

❌ **不适用**：
- 0 参数 → 直接 `SendCustomEvent`
- > 3 个参数 → 扩展性差，考虑用 Sync 替代
- 参数类型运行时决定 → 无法预生成 wrapper

---

## 槽位数量选择

| 槽数 | 适用 |
|------|------|
| 1 (`_l_t`) | 仅传 target |
| 2 (`_l_t`, `_l_p`) | target + 单 value（90% 场景） |
| 3 (`_l_t`, `_l_p`, `_l_a`) | target + prefab + active（多状态） |
| 4+ | 考虑改成同步变量或序列化 |

ULocalization 用 3 槽位是为了同时支持 `set_text(value)` 和 `set_name(value)` 两种语义。

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **ULocalization** | 3 槽位（target + prefab + active） | 完整 |
| 简化版 Udon 工具 | 1-2 槽位 | 缩小型 |
| 数据采集器 | 2 槽位（source + timestamp） | 通用 |

---

## 关联文档

- `memory/sources/ulocalization.md` — 项目溯源
- `memory/patterns/hash-based-dispatch.md` — 配套的 hash 分派
- `memory/patterns/code-generation-type-erasure.md` — 配套的代码生成
- `memory/FACT.md` § ULocalization
