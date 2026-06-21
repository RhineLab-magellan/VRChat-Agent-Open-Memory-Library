# Pattern: IID Object Identity (整数身份映射)

> Type: PATTERN
> Source: ULocalization(参考工程)
> Confidence: High
> SDK Version: 3.10.x
> Last Verified: 2026-06-20
> Reference: `memory/sources/ulocalization.md`

---

## Problem / Context

Udon 沙箱的多个限制同时出现：
1. Udon 不能把普通 `C# Object`（如 `LocalizeStringEvent`）作为 Dictionary key
2. Udon 端不能跨过 Editor-Runtime 边界持久化对象引用
3. Udon 端不能做 `object.ReferenceEquals`
4. 编辑器配置的引用（"LocalizeStringEvent A"）必须在运行时能找到对应实例

传统方案：
- ❌ `Dictionary<T, U>` 在 Udon 端不可靠（暴露受限）
- ❌ 直接序列化对象引用到 Udon 字段 → 引用失效（克隆后）

ULocalization 场景：场景可能有 100+ LocalizeEvent + 50+ LocalizedString + 30+ Variable，需要在运行时索引访问。

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| `Dictionary<TKey, TValue>` 暴露受限 | 不能用 `Dictionary<LocalizeEvent, int>` |
| 不能 `GetHashCode()` 用于业务 | Udon 的 GetHashCode 不保证稳定 |
| 跨 Build 引用失效 | Editor 引用 → 运行时不是同一对象 |
| VRCPlayerObject 克隆 | 克隆后的对象是"新对象"，原引用失效 |

---

## Solution

**核心思想**：Editor 端用 `List<object>` + 顺序索引分配 int ID。运行时用 `int` 作为 universal handle。克隆后用 `RenewPrefab` 重建映射。

### 关键机制

#### 1. ID 分配（Editor 端）

```csharp
// IID.cs
public static int GenerateId(object key) {
    if (key == null) return -1;
    if (!objects.Contains(key)) {
        objects.Add(key);
    }
    return objects.IndexOf(key);  // 0, 1, 2, ...
}
```

#### 2. 引用缓存（按类型分组）

```csharp
// LocalizeEventCache.cs
static List<LocalizedMonoBehaviour> localizeEvents = new();

public static int AddOrGet(LocalizedMonoBehaviour localizeEvent) {
    if (localizeEvent == null) return -1;
    if (!localizeEvents.Contains(localizeEvent)) {
        localizeEvents.Add(localizeEvent);
    }
    return localizeEvents.IndexOf(localizeEvent);
}

// LocalizedCache.cs (按 LocalizedReference 类型)
static Dictionary<LocalizedReference, HashSet<LocalizedMonoBehaviour>> localizeds = new();

// VariableCache.cs (按 IVariable 类型)
static Dictionary<IVariable, HashSet<IVariable>> variables = new();
```

#### 3. Udon 端通过 int 访问

```csharp
// LocalizationShim.cs
public int GetLocalized(int localizeEvent) {
    if (localizeEvent < 0) return -1;
    return _8[localizeEvent];  // _8 是 int[] 数组
}

public object GetValue(int variable) {
    return _19[variable];
}
```

#### 4. 引用更新（克隆场景）

```csharp
// CloneDetector.cs → LocalizationShim.RenewPrefab
public void RenewPrefab(GameObject go, int prefab, object[] refs) {
    _r_cache0 = new DataDictionary();
    _r_cache1 = new DataDictionary();
    _r_refs0 = _20[prefab];  // 原始 ref 数组
    _r_refs1 = refs;          // 克隆 ref 数组

    var udons = go.GetComponentsInChildren<UdonBehaviour>(true);
    for (var i = 0; i < udons.Length; i++) {
        var value = instance.GetProgramVariable(CompilerConstants.UsbTypeNameHeapKey);
        if (value == null) continue;

        var id = (string)value;
        var idx = Array.IndexOf(_23, id);  // 在字段类型表中查找
        if (idx < 0) continue;

        // 根据类型 ID 调用对应的 Clone* 方法
        switch (__26[j]) {
            case "__34e35fe8fc0d5c82f904f6ad75d8a5f6":  // LocalizeStringEvent
                if (Array.IndexOf(__22, (int)_v[1]) < 0) continue;
                _v[1] = CloneLocalizeEvent((int)_v[1]);
                break;
            // ... 16 个 case
        }
    }
}
```

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | 单一 Shim |
| Source of Truth | Editor 端 `List<object>` (int 索引 = 引用) |
| Sync Type | N/A |
| Synced Variables | `int[]` 数组存 ID |
| Mutation Path | Editor 端 `AddOrGet` |
| Ownership Path | 无 |
| Serialization Path | Editor 注入 int[] 到 Shim |
| Receive Path | Udon 端用 int[] 索引访问 |
| Late Joiner | 自动（int 是 universal handle） |
| Conflict Strategy | 无（本地） |
| Bandwidth Budget | 0 |
| Failure Mode | ID 越界（数组长度检查可解决） |

---

## Implementation Sketch

```csharp
// === Editor 端：通用 ID 分配器 ===
public static class IID {
    static List<object> _all = new();
    static Dictionary<Type, List<object>> _byType = new();

    public static int GenerateId<T>(T key) where T : class {
        if (key == null) return -1;
        if (!_byType.TryGetValue(typeof(T), out var list)) {
            list = new List<object>();
            _byType[typeof(T)] = list;
        }
        if (!list.Contains(key)) list.Add(key);
        _all.Add(key);
        return list.IndexOf(key);
    }

    public static IEnumerable<T> GetAll<T>() where T : class {
        return _byType.TryGetValue(typeof(T), out var list)
            ? list.Cast<T>()
            : Enumerable.Empty<T>();
    }
}

// === 运行时：用 int 引用 object ===
public class RefInt {
    public int Id;
}

public T ResolveRef<T>(int id) where T : class {
    if (id < 0) return null;
    return (T)_objects[id];
}
```

---

## When To Use

✅ **适用**：
- 场景中需要索引访问大量同类对象
- 需要跨 Editor-Runtime 边界引用
- 涉及 VRCPlayerObject 克隆重建引用

❌ **不适用**：
- 对象数量极少（< 10）→ 直接用字段引用
- 运行时频繁增删对象 → 数组重建成本高
- 需要 Dictionary key 语义 → 应转用 Hash 模式

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **ULocalization** | 100+ LocalizeEvent/Localized/Variable ID 映射 | 完整三缓存分离 |
| Persistence 系统 | PlayerObject 槽位索引 | 简化版（单 List） |
| VRCObjectPool | 对象池索引 | 简化为 List |

---

## 关联文档

- `memory/sources/ulocalization.md` — 项目溯源
- `memory/patterns/slot-parameter-passing.md` — 配套的 slot 传参
- `memory/patterns/build-time-vs-runtime-separation.md` — 配套的 Build-Runtime 分离
- `memory/FACT.md` § ULocalization
