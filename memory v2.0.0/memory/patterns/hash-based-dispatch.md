---
title: Pattern: Hash-Based Method Dispatch (哈希方法分派)
category: patterns

knowledge_level: applied
status: active

tags:
  - patterns
  - patterns
  - constraint
  - audio
  - event
  - udonsharp

aliases:
  - "Hash-Based Method Dispatch (哈希方法分派)"

related:
  - sources/ulocalization.md
  - patterns/slot-parameter-passing.md
  - patterns/code-generation-type-erasure.md
  - FACT.md
  - reviews/common-failures.md

source: ULocalization(参考工程)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Pattern: Hash-Based Method Dispatch (哈希方法分派)


---

## Problem / Context

Udon VM **不支持委托 / 函数指针**。当需要"动态选择方法"（如 UnityEvent listener 分发、字符串到方法映射）时，C# 的 `Action<T>` / `Func<T, TResult>` / `Delegate` 都不可用。

传统方案：
- ❌ `SendCustomEvent(string)` 只能传方法名，调用者必须硬编码
- ❌ 运行时无法"动态选择"目标方法
- ❌ UnityEvent 持久 listener 在 Udon 端无法被 Udon 行为直接调用

ULocalization 场景：100+ 不同 (Component, Method) 组合需要被 LocalizeEvent 触发。

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| 无 `Delegate` 类型 | 不可写 `Action<X> x = someMethod` |
| 无 `MethodInfo` | 不可 `GetMethod().Invoke()` |
| `SendCustomEvent(string)` | 仅字符串方法名，编译期必须存在 |
| 无 Lambda | 不可 `x => x.DoSomething()` |

---

## Solution

**核心思想**：在 Editor 端为每个允许的 (Type, Method) 组合预生成一个 hash 命名的 wrapper 方法。Udon 端调用时用 hash 字符串间接分派。

### 关键机制

#### 1. Hash 命名约定

```csharp
// Editor: 计算 (TypeName + MethodName) 的 MD5 hash
public static string ComputeHashMD5(this string self) {
    var buff = md5provider.ComputeHash(Encoding.UTF8.GetBytes(self));
    return BitConverter.ToString(buff).ToLower().Replace("-", string.Empty);
}

// 生成签名: "UnityEngineAudioSource.__Play__SystemVoid"
var signature = $"UnityEngine{targetType.FullName.Replace(".", "")}.{methodName}__{retType}";

// 转 hash: "__35a8e04bf600a5223ffbd8f024a1a7ef"
var methodId = $"__{signature.ComputeHashMD5()}";
```

#### 2. 代码生成 (LocalizatiionShim_Generated.cs)

```csharp
internal sealed partial class LocalizationShim {
    public void __0bf0b1b18ad0f865ed8825d48c851014() =>
        ((global::UnityEngine.AI.NavMeshAgent)_l_t).CompleteOffMeshLink();
    public void __f1547e55a5c9dd22ff36ce8ac1135bde() =>
        ((global::UnityEngine.AudioSource)_l_t).clip = (global::UnityEngine.AudioClip)_l_p;
    public void __0756f083fc35bc876f6a3e78aa5659eb() =>
        ((global::TMPro.TextMeshPro)_l_t).text = (global::System.String)_l_p;
    // ... 500+ 个 hash 命名方法
}
```

#### 3. 运行时分派

```csharp
// LocalizationShim.cs (运行时分派)
for (var i = 0; i < __9; i++) {
    _l_t = __11[i];      // target object
    _l_a = __12[i];      // argument
    SendCustomEvent(__10[i]);  // __10[i] 是 hash 字符串
}
```

#### 4. 白名单（编辑器侧约束）

```csharp
// UnityEventFilter.cs — 只允许特定 (Type, Method) 组合
static Dictionary<Type, Dictionary<string, string>> allowedUnityEventTargetTypes = new() {
    [typeof(UnityEngine.AudioSource)] = new() {
        ["Play"] = "UnityEngineAudioSource.__Play__SystemVoid",
        ["set_clip"] = "UnityEngineAudioSource.__set_clip__UnityEngineAudioClip__SystemVoid",
        // ...
    },
    // 100+ 个类型
};
```

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | 单一 Shim (Singleton) |
| Source of Truth | Editor 端预生成的 hash 表 |
| Sync Type | N/A（本地分派，不需要网络） |
| Synced Variables | 无 |
| Mutation Path | Editor 端代码生成 |
| Ownership Path | 无 |
| Serialization Path | 无 |
| Receive Path | `SendCustomEvent(hashString)` |
| Late Joiner | 自动（hash 是字符串）|
| Conflict Strategy | 无 |
| Bandwidth Budget | 0（无网络） |
| Failure Mode | hash 冲突（极低概率，但需保证 MD5 唯一性） |

---

## Implementation Sketch

```csharp
// === Editor 端 (代码生成器) ===

// 1. 白名单定义
var allowedMethods = new Dictionary<Type, List<string>> {
    [typeof(AudioSource)] = new() { "Play", "Pause", "Stop" },
    [typeof(TMP_Text)] = new() { "set_text" },
    [typeof(Button)] = new() { "Select" },
};

// 2. 生成所有 hash 方法
foreach (var (type, methods) in allowedMethods) {
    foreach (var method in methods) {
        var signature = $"{type.FullName.Replace(".", "")}.{method}";
        var hash = signature.ComputeHashMD5();
        var wrapper = $@"
            public void __{hash}() => (({type.FullName})_l_t).{method}((ArgType)_l_a);
        ";
        generatedCode.AppendLine(wrapper);
    }
}

// 3. 运行时: 用户配置 listener
var eventTarget = audioSource;
var eventMethod = "Play";
var signature = $"{eventTarget.GetType().FullName.Replace(".", "")}.{eventMethod}";
var hash = $"__{signature.ComputeHashMD5()}";  // "__xxx..."
// 存储到 shim 的 listener 数组
```

---

## When To Use

✅ **适用**：
- 需要 UnityEvent 持久 listener 在 Udon 端被触发
- 动态目标类型 + 固定方法集合（如 100+ Component 类型）
- 静态可枚举的 API 表面

❌ **不适用**：
- 只需 1-3 个方法 → 直接 `SendCustomEvent` 硬编码
- 动态方法名（用户输入）→ 不可枚举
- 需要返回值 → 不可用

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **ULocalization** | 100+ UnityEvent 目标分派 | 完整实现 |
| 自定义 UI 事件系统 | UI Button → Udon 行为 | 缩小型 |
| OSC 消息 → 行为调用 | OSC 路径 → method | 字符串→hash |

---

## 关联文档

- `memory/sources/ulocalization.md` — ULocalization 项目溯源
- `memory/patterns/slot-parameter-passing.md` — 配套的 slot 传参模式
- `memory/patterns/code-generation-type-erasure.md` — 代码生成策略
- `memory/FACT.md` § ULocalization(参考工程) — 案例研究摘要
- `memory/reviews/common-failures.md` — FAIL-23: `internal` 关键字导致方法随机不可用
