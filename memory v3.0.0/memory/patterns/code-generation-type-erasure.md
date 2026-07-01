---
title: "Code Generation with Type Erasure (代码生成 + 类型擦除)"
category: patterns
knowledge_level: applied
status: active
source: ULocalization(参考工程)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - patterns
  - patterns
  - constraint
  - audio
  - event
aliases:
  - "Code Generation with Type Erasure (代码生成 + 类型擦除)"
  - code-generation-type-erasure
related:
  - "sources/ulocalization.md"
  - "patterns/hash-based-dispatch.md"
  - "patterns/build-time-vs-runtime-separation.md"
  - FACT.md
---
# Pattern: Code Generation with Type Erasure (代码生成 + 类型擦除)

> SDK Version: 3.10.x
> Last Verified: 2026-06-20
> Reference: `memory/sources/ulocalization.md`

---

## Problem / Context

Udon VM **不支持泛型方法、类型擦除不彻底、switch 类型有限**。当业务需要"对多个具体类型做相同操作"时，无法用 C# 泛型 + 反射。

具体场景：
- ❌ `T Deserialize<T>(IDataReader reader)` → Udon 不可用
- ❌ `switch (obj) { case BoolVariable v: ... }` → 部分 Udon 不支持 pattern matching
- ❌ 16 种 `IVariable` 类型的 GetValue/SetValue → 不能写泛型方法
- ❌ 100+ 组件类型的方法分派 → 不能写泛型约束

ULocalization 场景：
- 16 种 `IVariable` 类型（Bool / Int / String / Float / ...）需要统一 GetValue/SetValue
- 5 种 `LocalizeEvent` 类型（String / AudioClip / Texture / Sprite / Dropdown）需要统一序列化
- 6 种 `LocalizedReference` 类型需要统一 ID 缓存

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| 无泛型方法 | `T Foo<T>()` 不可用 |
| 无类型 switch | `switch (v) { case X x: }` 有限制 |
| 暴露 API 受限 | 部分类型不能作为方法参数 |
| 性能差异大 | boxing 慢，object cast 慢 |

---

## Solution

**核心思想**：用 Type.FullName 计算 MD5 hash 作为 type ID。生成 switch case 显式处理每个类型。运行时按 type ID 索引到具体实现。

### 关键机制

#### 1. Type ID 生成

```csharp
// Editor 端
static string BuildVariableId(IVariable variable) {
    if (variable == null) return null;
    return $"__{variable.GetType().FullName.Replace(".", "").ComputeHashMD5()}";
}

// 例: "UnityEngineLocalizationSmartFormatPersistentVariablesBoolVariable" → "__f8cfba77af0119c086592e79c73223e5"
```

#### 2. Type ID 集合（共享）

```csharp
// Shim 持有 type ID 数组
[Inject, SerializeField, HideInInspector]
string[] _17;  // 变量 type ID 数组

[Inject, SerializeField, HideInInspector]
object[] _19;  // 变量值数组
```

#### 3. Switch 分派

```csharp
// SmartLiteFormat.cs (格式化器)
[RecursiveMethod]
string SmartLiteFormat(string format, DataDictionary args) {
    // ... 解析 placeholder
    for (var j = 0; j < kl; j++) {
        // ... 解析 key path
        switch (_17[v]) {  // ← 按 type ID switch
            case "__f8cfba77af0119c086592e79c73223e5":  // BoolVariable
                d = null;
                s = ((bool)_19[v]).ToString(culture);
                break;
            case "__6bac394d6972c8d339cc1ce54df77912":  // SByteVariable
                d = null;
                s = ((sbyte)_19[v]).ToString(f, culture);
                break;
            // ... 16 个 case
        }
    }
}
```

#### 4. 类型擦除序列化器

```csharp
// 每个具体类型一个薄包装类
public sealed class IntVariable : Variable<UnityEngine.Localization.SmartFormat.PersistentVariables.IntVariable> { }
public sealed class StringVariable : Variable<UnityEngine.Localization.SmartFormat.PersistentVariables.StringVariable> { }
public sealed class BoolVariable : Variable<UnityEngine.Localization.SmartFormat.PersistentVariables.BoolVariable> { }
// ... 16 个类

// Variable<T> 泛型类（仅 Editor 端用）
public class Variable<T> : IVariable, ISerializable where T : IVariable {
    [Inject, SerializeField] T variable;

    public void Serialize(IDataWriter writer) {
        writer.WriteReference("", LocalizationResolver.Resolve());
        writer.WriteInt32("", VariableCache.AddOrGet(variable));
    }
}
```

#### 5. 类型擦除扩展方法

```csharp
// 16 个具体类型的 GetValue/SetValue
public static class IntVariableExtensions {
    public static int GetValue(this IntVariable self) {
        var _self = (object[])(object)self;
        var _localization = (LocalizationShim)_self[0];
        var _variable = (int)_self[1];
        return (int)_localization.GetValue(_variable);
    }
    public static void SetValue(this IntVariable self, int value) {
        var _self = (object[])(object)self;
        var _localization = (LocalizationShim)_self[0];
        var _variable = (int)_self[1];
        _localization.SetValue(_variable, value);
    }
}
// 15 个类似文件
```

#### 6. 元组模式（重要）

所有"伪装"的 Udon 引用实际上是 `object[2]`：

```csharp
// 结构: [LocalizationShim ref, int id]
public static LocalizedString GetLocalized(this LocalizeStringEvent self) {
    var _self = (object[])(object)self;          // 强转 object[]
    var _localization = (LocalizationShim)_self[0];
    var _localizeEvent = (int)_self[1];
    var _localized = _localization.GetLocalized(_localizeEvent);
    if (_localized < 0) return default;
    var localized = new object[2];
    localized[0] = _localization;
    localized[1] = _localized;
    return (LocalizedString)(object)localized;  // 再强转回
}
```

> **Udon 神奇之处**：`LocalizedString` 实际上是 `object[2]`，但编译期类型仍是 `LocalizedString`。Udon VM 不做类型检查，可直接强转。这是**零开销**的"伪类型"。

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | N/A（类型擦除 + 本地） |
| Source of Truth | Editor 端类型表 |
| Sync Type | N/A |
| Synced Variables | 无 |
| Mutation Path | 编译期 switch case |
| Ownership Path | 无 |
| Serialization Path | 无 |
| Receive Path | Udon 端 int → type ID 索引 |
| Late Joiner | 自动 |
| Conflict Strategy | 无 |
| Bandwidth Budget | 0 |
| Failure Mode | 新增类型未注册 → 静默失败（switch 落到 default） |

---

## Implementation Sketch

```csharp
// === 简化版：类型擦除 dispatch ===
public abstract class MyValue { }  // 标记接口

public sealed class IntValue : MyValue { public int V; }
public sealed class StringValue : MyValue { public string V; }

public partial class Dispatcher : UdonSharpBehaviour {
    string[] _typeIds;
    object[] _values;

    // 运行时: 按 type ID 分派
    public void DoSomething(int idx) {
        switch (_typeIds[idx]) {
            case "__int__hash__":
                IntValue v = (IntValue)_values[idx];
                DoInt(v);
                break;
            case "__string__hash__":
                StringValue s = (StringValue)_values[idx];
                DoString(s);
                break;
        }
    }

    void DoInt(IntValue v) { /* ... */ }
    void DoString(StringValue v) { /* ... */ }
}
```

---

## When To Use

✅ **适用**：
- 类型集合有限（< 20）但需要类型安全
- 类型在编译期完全确定
- 性能要求高（避免反射）

❌ **不适用**：
- 类型集合开放（用户可扩展）→ 不可枚举
- 数量 < 3 → 直接写 switch 更简单
- 动态类型（运行时新增）→ 不可用

---

## 与泛型对比

| 维度 | 泛型 (C#) | 类型擦除 (Udon) |
|------|-----------|------------------|
| 代码量 | 1 个泛型方法 | N 个具体类 + 1 个 switch |
| 编译期 | 类型检查 | 无 |
| 运行期 | 0 开销 | 1 次 switch 跳转 |
| 反射需求 | 无 | 无 |
| 内存 | 单实例 | N 个 wrapper 类（每个 ~50 字节） |
| 可扩展性 | 任意类型 | 必须改代码生成器 |

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **ULocalization** | 16 IVariable + 5 LocalizeEvent + 6 LocalizedReference | 完整三组 |
| Modular Avatar | NDMF 组件分类 | 缩小型 |
| ORL Shader | 模块化配置类型 | 简化 |

---

## 关联文档

- `memory/sources/ulocalization.md` — 项目溯源
- `memory/patterns/hash-based-dispatch.md` — 配套 hash 分派
- `memory/patterns/build-time-vs-runtime-separation.md` — 配套 Build-Runtime 分离
- `memory/FACT.md` § ULocalization
