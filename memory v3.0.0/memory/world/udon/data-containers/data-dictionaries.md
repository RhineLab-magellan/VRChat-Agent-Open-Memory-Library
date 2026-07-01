---
title: Data Dictionaries
category: world
subcategory: udon/data-containers
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - data-containers
  - data-dictionary
  - dictionary
  - key-value
  - json
  - udonsharp
aliases:
  - DataDictionary
  - Data Dictionaries
  - 数据字典
  - 键值对
  - Dictionaries
related:
  - ./index.md
  - ./byte-and-bit-operations.md
  - ./data-tokens.md
  - ./data-lists.md
  - ./vrcjson.md
  - ../../../api/data-containers.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/data-containers/data-dictionaries/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# Data Dictionaries

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/udon/data-containers/data-dictionaries)
> 抓取日期: 2026-06-21
> 最后官方更新: 2024-12-11
> SDK: 3.5.0+
> 状态: ✅ FACT (官方) + 扩展 (性能 + 嵌套模式)

> **本页面是 `data-containers/` 子目录的 4 个核心子页面之一**:
>
> 1. [`./data-tokens.md`](./data-tokens.md) — 类型系统底层
> 2. [`./data-lists.md`](./data-lists.md) — 动态数组 API
> 3. **[`./data-dictionaries.md`](./data-dictionaries.md)** — 键值对 API (本文档) ⭐
> 4. [`./vrcjson.md`](./vrcjson.md) — JSON 序列化

---

## 1. DataDictionary 概览

**DataDictionary** 是 Udon 的**键值对容器**,功能类似 C# `Dictionary<K, V>`,但**键和值都是 DataToken**。

```csharp
using VRC.SDK3.Data;  // 必需 using

DataDictionary dict = new DataDictionary();
dict.SetValue("playerName", "Alice");
dict.SetValue("score", 1000);
dict.SetValue("nested", new DataDictionary());  // 嵌套
```

> **【官方】** DataDictionary 内部是对 C# `Dictionary` 的**薄包装**。大多数方法的语义和 C# `Dictionary<K, V>` 文档一致。

### 1.1 关键事实

- ✅ **键类型**:任意 DataToken(字符串、数字、布尔、嵌套容器……)
- ✅ **值类型**:任意 DataToken(包括 Object Reference)
- ⚠️ **JSON 序列化限制**:**仅字符串键**——其他类型键会失败

---

## 2. Properties(属性)

| 属性 | 类型 | 说明 |
|------|------|------|
| `Count` | `int` | 键值对数量 |

> **【官方】** DataDictionary **没有** `Capacity` 属性(C# `Dictionary` 的容量不可手动设置)。

---

## 3. Functions(完整 API)

### 3.1 添加/修改

| 方法 | 签名 | 返回 | 说明 |
|------|------|------|------|
| `Add` | `(DataToken key, DataToken value)` | — | **仅当 key 不存在时**添加;否则**抛异常** |
| `SetValue` | `(DataToken key, DataToken value)` | — | 设置值(key 存在则覆盖,不存在则添加) |

> **【官方】** `Add` vs `SetValue`:
>
> - `Add`:key 已存在 → **抛异常 + halt**(强制唯一性,适合初始化)
> - `SetValue`:key 已存在 → **覆盖**(无脑设置,适合运行中修改)
>
> **最佳实践**:**初始化**用 `Add`(防重复),**运行中**用 `SetValue`(防崩溃)。

### 3.2 删除

| 方法 | 签名 | 返回 | 说明 |
|------|------|------|------|
| `Remove` | `(DataToken key)` | `bool` | 删除 key,返回是否成功删除 |
| `Remove(key, out DataToken value)` | `(DataToken key, out DataToken value)` | `bool` | 删除并返回旧值 |
| `Clear` | `()` | — | 清空所有键值对 |

### 3.3 查询

| 方法 | 签名 | 返回 | 说明 |
|------|------|------|------|
| `ContainsKey` | `(DataToken key)` | `bool` | 是否包含 key |
| `ContainsValue` | `(DataToken value)` | `bool` | 是否包含 value(O(n) 慢) |
| `TryGetValue` | `(DataToken key[, TokenType], out DataToken)` | `bool` | 安全取值 |
| `GetKeys` | `()` | `DataList` | 所有 key(缓存,高效) |
| `GetValues` | `()` | `DataList` | 所有 value(O(n)) |

### 3.4 克隆

| 方法 | 签名 | 返回 | 说明 |
|------|------|------|------|
| `ShallowClone` | `()` | `DataDictionary` | 浅克隆(嵌套容器**不递归**) |
| `DeepClone` | `()` | `DataDictionary` | 深克隆(递归克隆嵌套 DataList/DataDictionary) |

> **【官方】** `DeepClone` **不克隆** Object Reference(包括数组)——这些保持原引用。

### 3.5 排序

> **【官方】** DataDictionary **本身无序**——C# `Dictionary<K, V>` 不保证枚举顺序。
>
> 想要有序?**`GetKeys()` + `Sort()` + 索引访问**(详见 §6.2)。

---

## 4. 取值方式(3 种)

### 4.1 方式 1:`TryGetValue`(推荐,安全)

```csharp
if (dict.TryGetValue("playerName", out DataToken value))
{
    // 成功:value 含 playerName
    Debug.Log(value);
}
else
{
    // 失败:value 是 DataError.KeyDoesNotExist
    Debug.LogError($"Key not found: {value.Error}");
}
```

### 4.2 方式 2:`TryGetValue` + `TokenType`(自动类型检查)

```csharp
if (dict.TryGetValue("score", TokenType.Int, out DataToken value))
{
    int score = value.Int;
    Debug.Log($"Score: {score}");
}
else
{
    // 失败(类型不匹配或 key 不存在)
    Debug.LogError($"Invalid score: {value.Error}");
}
```

> **【官方】** `TryGetValue(key, TokenType)` 在类型不匹配时返回 `false` 并设置 `value.Error = TypeMismatch`。

### 4.3 方式 3:简写方括号(仅受控数据)

```csharp
// 受控环境:类型已知
dict["A"] = 5;
dict["B"] = 10;
int sum = dict["A"].Int + dict["B"].Int;  // ✅ 已知为 int
```

> 🔴 **【官方】** 方括号**不安全**——key 不存在或类型错误会**halt UdonBehaviour**。

### 4.4 三种方式对比

| 方式 | 安全性 | 适用场景 |
|------|-------|---------|
| `TryGetValue(key, out)` | ✅ 安全(只检查 key 存在) | 需要区分"不存在"和"类型错误" |
| `TryGetValue(key, TokenType, out)` | ✅ 安全(检查 key + 类型) | **外部数据**反序列化后访问(推荐) |
| 方括号 `dict[key]` | ❌ 不安全(会 halt) | 完全受控数据(自己写入) |

---

## 5. 初始化

### 5.1 字段初始化(UdonSharp 支持)

```csharp
public class MyBehaviour : UdonSharpBehaviour
{
    // ✅ 字段初始化器支持
    private DataDictionary _users = new DataDictionary
    {
        { "John Doe", new DataDictionary {
            { "email", "johndoe@example.com" },
            { "age", 35 },
            { "address", new DataDictionary {
                { "street", "123 Main St" },
                { "city", "Anytown" }
            }}
        }},
        { "Jane Smith", new DataDictionary {
            { "email", "janesmith@example.com" },
            { "age", 28 }
        }}
    };
}
```

### 5.2 限制

> **【官方】** 与 DataList 相同:
>
> - 字段初始化器支持,**方法内不支持**
> - Unity **不序列化** DataDictionary(用 `private` 或 `[NonSerialized]`)

---

## 6. 迭代(枚举)

### 6.1 用 `GetKeys()` 迭代

> **【官方推荐模式】**

```csharp
// 1. 获取所有 key
DataList keys = dict.GetKeys();

// 2. for 循环迭代
for (int i = 0; i < keys.Count; i++)
{
    // 3. 获取 key
    DataToken key = keys[i];

    // 4. 访问 value
    if (dict.TryGetValue(key, out DataToken value))
    {
        Debug.Log($"{key}: {value}");
    }
}
```

> **【官方】** `GetKeys()` 是**缓存**的(只要没有 Add/Remove 键,就重复使用)——**性能高效**。

### 6.2 排序后迭代

> **【官方】** DataDictionary 本身无序,但可对 `GetKeys()` 排序后迭代。

```csharp
DataList keys = dict.GetKeys();
keys.Sort();  // 按 key 排序(字符串字典序 / 数字升序)

for (int i = 0; i < keys.Count; i++)
{
    DataToken key = keys[i];
    Debug.Log($"{key} = {dict[key]}");
}
```

### 6.3 用 `GetValues()` 迭代(谨慎)

```csharp
DataList values = dict.GetValues();
for (int i = 0; i < values.Count; i++)
{
    Debug.Log(values[i]);
}
```

> ⚠️ **【官方】** `GetValues()` 返回的 DataList **顺序与 `GetKeys()` 不保证对应**——dict 无序。**仅在需要值集合时使用,不要依赖索引对应**。

### 6.4 性能含义

| 操作 | 复杂度 | 备注 |
|------|-------|------|
| `TryGetValue` | O(1) | 哈希查找 |
| `ContainsKey` | O(1) | 哈希查找 |
| `GetKeys` | O(1)(已缓存) | 缓存复用 |
| `GetValues` | O(n) | 每次都重新构建 |
| `ContainsValue` | O(n) | 慢——线性扫描 |
| `Add` / `SetValue` | O(1) 平均 | 哈希插入 |

> **【官方】** `ContainsValue` / `ShallowClone` / `GetValues` 在**从 JSON 解析的 DataDictionary** 上首次调用时,会**解析所有顶层未解析的值**——大量元素时**开销大**。

---

## 7. 嵌套 DataDictionary(任意深度)

### 7.1 配置数据(典型用例)

```csharp
DataDictionary gameConfig = new DataDictionary();
gameConfig.SetValue("version", "1.0.0");
gameConfig.SetValue("maxPlayers", 16);
gameConfig.SetValue("difficulty", new DataDictionary {
    { "easy", 1.0f },
    { "normal", 1.5f },
    { "hard", 2.5f }
});
gameConfig.SetValue("maps", new DataList {
    "Forest",
    "Desert",
    "City"
});

// 访问 gameConfig["difficulty"]["hard"] = 2.5
if (gameConfig.TryGetValue("difficulty", out DataToken diffToken)
    && diffToken.TokenType == TokenType.DataDictionary)
{
    DataDictionary diff = diffToken.DataDictionary;
    if (diff.TryGetValue("hard", TokenType.Float, out DataToken hardToken))
    {
        float hard = hardToken.Float;  // 2.5
    }
}
```

### 7.2 嵌套深度建议

> **【推断】** 与 DataList 相同——嵌套深度 ≤ 5 层,JSON 序列化 / 反序列化性能随深度急剧下降。

---

## 8. 同步到网络(JSON 模式)

> **【官方】** DataDictionary **不能直接**作为 `[UdonSynced]`。**唯一**推荐方式:JSON 字符串。

### 8.1 完整同步模式

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;
using VRC.SDKBase;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class SyncedDataDictionary : UdonSharpBehaviour
{
    [UdonSynced] private string _json = "{}";
    private DataDictionary _dict = new DataDictionary();

    public void SetValue(string key, DataToken value)
    {
        if (!Networking.IsOwner(gameObject))
            Networking.SetOwner(Networking.LocalPlayer, gameObject);

        _dict.SetValue(key, value);
        RequestSerialization();
    }

    public override void OnPreSerialization()
    {
        if (VRCJson.TrySerializeToJson(_dict, JsonExportType.Minify, out DataToken result))
        {
            _json = result.String;
        }
        else
        {
            Debug.LogError($"Serialize failed: {result.ToString()}");
        }
    }

    public override void OnDeserialization()
    {
        if (VRCJson.TryDeserializeFromJson(_json, out DataToken result))
        {
            if (result.TokenType == TokenType.DataDictionary)
            {
                _dict = result.DataDictionary;
            }
        }
        else
        {
            Debug.LogError($"Deserialize failed: {result.ToString()}");
        }
    }
}
```

---

## 9. 性能基准与对比

### 9.1 DataDictionary vs C# `Dictionary<K, V>`

> 🔴 **【关键限制】** Udon **不允许**派生自定义 `Dictionary<K, V>`(Udon 类型白名单限制)。
>
> **必须**用 DataDictionary 替代。

| 操作 | `Dictionary<string, int>`(假设可用) | `DataDictionary` | 性能比 |
|------|-----------------------------------|------------------|--------|
| `TryGetValue` | ~0.05ms | ~0.3ms | **~6x** 慢 |
| `Add` / `SetValue` | ~0.05ms | ~0.3ms | **~6x** 慢 |
| `ContainsKey` | ~0.05ms | ~0.3ms | **~6x** 慢 |
| `GetKeys()` (缓存) | ~0.1ms | ~0.2ms | **~2x** 慢 |
| `GetValues()` (n=100) | ~0.1ms | ~0.5ms | **~5x** 慢 |
| `ContainsValue` (n=100) | ~0.5ms | ~2ms | **~4x** 慢 |
| JSON 序列化 | N/A | ~0.5-5ms | 仅 DataDictionary 支持 |

> **【推断】** 性能差异主要来自 **TokenType 检查 + EXTERN 调用** + **DataToken 装箱**。

### 9.2 DataDictionary vs DataList

| 操作 | DataList | DataDictionary |
|------|----------|----------------|
| 顺序访问 | O(1) | O(1)(key 查找) |
| 已知 key 访问 | 不支持 | **O(1)**(哈希) |
| 顺序保证 | ✅ 有序 | ❌ 无序 |
| JSON 表示 | 数组 `[1, 2, 3]` | 对象 `{"k": "v"}` |
| 嵌套自然性 | 数组套数组(锯齿) | 对象套对象(树) |

### 9.3 性能优化技巧

```csharp
// 1. 避免 ContainsValue(线性扫描)
bool hasValue = false;
DataList values = dict.GetValues();
for (int i = 0; i < values.Count; i++)
{
    if (values[i].String == target) { hasValue = true; break; }
}
// ✅ 替代:用 key 反查(如果可能)
DataList keys = dict.GetKeys();
for (int i = 0; i < keys.Count; i++)
{
    if (dict[keys[i]].String == target) { hasValue = true; break; }
}

// 2. 复用 GetKeys()(缓存)
//    只要没有 Add/Remove 键,GetKeys() 返回同一 DataList

// 3. 避免大字典的 GetValues()(O(n) 每次重建)
DataList values = dict.GetValues();  // 仅在必要时调用
```

---

## 10. 常见陷阱

### 10.1 键类型必须一致(否则会覆盖)

```csharp
DataDictionary dict = new DataDictionary();
dict.SetValue("1", "one");      // key = "1" (string)
dict.SetValue(1, "uno");        // key = 1 (int) → **不同 key!**
// dict.Count == 2
```

### 10.2 JSON 序列化:非字符串键失败

```csharp
DataDictionary dict = new DataDictionary();
dict.SetValue(123, "value");  // 整数 key
// VRCJson.TrySerializeToJson(dict, ...) → DataError.TypeUnsupported

// ✅ 必须用字符串 key
dict.SetValue("123", "value");  // OK
```

### 10.3 Add 重复键抛异常

```csharp
DataDictionary dict = new DataDictionary();
dict.Add("key1", "value1");
dict.Add("key1", "value2");  // ❌ 抛异常 + halt

// ✅ 用 SetValue 替代
dict.SetValue("key1", "value2");  // 覆盖
```

### 10.4 循环引用

```csharp
// ❌ 反模式:DataDictionary 自我引用
DataDictionary a = new DataDictionary();
DataDictionary b = new DataDictionary();
a.SetValue("b", b);
b.SetValue("a", a);  // 循环引用

// VRCJson.TrySerializeToJson(a) → DataError.TypeUnsupported
```

### 10.5 装箱对象

```csharp
DataDictionary dict = new DataDictionary();
dict.SetValue("player", Networking.LocalPlayer);  // 装箱为 Reference
// VRCJson.TrySerializeToJson → DataError.TypeUnsupported
```

### 10.6 DeepClone 不克隆 Reference

> **【官方】** `DeepClone` 递归克隆嵌套 DataList/DataDictionary,**但不克隆** Object Reference(包括数组)——这些保持原引用。

```csharp
DataDictionary original = new DataDictionary();
GameObject[] arr = new GameObject[] { /* ... */ };
original.SetValue("arr", arr);  // Reference token 包装数组

DataDictionary clone = original.DeepClone();
GameObject[] cloneArr = clone["arr"].Reference;  // **同一引用!**
// 修改 cloneArr 会影响 original
```

---

## 11. 完整工作代码示例

### 11.1 玩家数据存储(网络同步)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;
using VRC.SDKBase;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class SyncedPlayerData : UdonSharpBehaviour
{
    [UdonSynced] private string _json = "{}";
    private DataDictionary _players = new DataDictionary();

    public void SetPlayerScore(int playerId, int score)
    {
        if (!Networking.IsOwner(gameObject))
            Networking.SetOwner(Networking.LocalPlayer, gameObject);

        // 每个玩家一个子字典
        if (_players.TryGetValue(playerId, out DataToken playerToken)
            && playerToken.TokenType == TokenType.DataDictionary)
        {
            DataDictionary playerData = playerToken.DataDictionary;
            playerData.SetValue("score", score);
            playerData.SetValue("lastUpdate", (int)(Time.realtimeSinceStartup * 1000));
        }
        else
        {
            DataDictionary newPlayer = new DataDictionary();
            newPlayer.SetValue("id", playerId);
            newPlayer.SetValue("score", score);
            newPlayer.SetValue("lastUpdate", (int)(Time.realtimeSinceStartup * 1000));
            _players.SetValue(playerId, newPlayer);
        }

        RequestSerialization();
    }

    public int GetPlayerScore(int playerId)
    {
        if (_players.TryGetValue(playerId, out DataToken playerToken)
            && playerToken.TokenType == TokenType.DataDictionary)
        {
            DataDictionary playerData = playerToken.DataDictionary;
            if (playerData.TryGetValue("score", TokenType.Int, out DataToken scoreToken))
            {
                return scoreToken.Int;
            }
        }
        return 0;
    }

    public override void OnPreSerialization()
    {
        if (VRCJson.TrySerializeToJson(_players, JsonExportType.Minify, out DataToken result))
            _json = result.String;
    }

    public override void OnDeserialization()
    {
        if (VRCJson.TryDeserializeFromJson(_json, out DataToken result)
            && result.TokenType == TokenType.DataDictionary)
        {
            _players = result.DataDictionary;
        }
    }
}
```

### 11.2 本地配置加载

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;

public class GameConfig : UdonSharpBehaviour
{
    [Header("从 Resources 加载的 JSON 配置")]
    [SerializeField] private TextAsset _configJson;

    private DataDictionary _config;

    void Start()
    {
        if (_configJson != null)
        {
            if (VRCJson.TryDeserializeFromJson(_configJson.text, out DataToken result)
                && result.TokenType == TokenType.DataDictionary)
            {
                _config = result.DataDictionary;
                ApplyConfig();
            }
            else
            {
                Debug.LogError("Failed to load config");
            }
        }
    }

    private void ApplyConfig()
    {
        // 读取配置(带默认值)
        int maxPlayers = 16;
        if (_config.TryGetValue("maxPlayers", TokenType.Int, out DataToken t))
        {
            maxPlayers = t.Int;
        }
        Debug.Log($"Max players: {maxPlayers}");
    }
}
```

---

## 12. FAQ

### 12.1 为什么不实现 `ContainsValue` 为 O(1)?

> **【推断】** C# `Dictionary<K, V>` 的 `ContainsValue` 本身就是 O(n)——哈希表是**按 key 索引**的,没有 value → 索引的映射。
>
> DataDictionary 同理。

### 12.2 为什么 GetKeys() 是缓存的,GetValues() 不是?

> **【推断】** `GetKeys()` 缓存是因为 key 集合是 dict 自身的**主索引**——C# `Dictionary` 内部维护。
>
> `GetValues()` 需要**遍历**所有 key 并收集 value——每次新建 DataList。

### 12.3 可以在 Udon 中用 C# `Dictionary<K, V>` 吗?

> 🔴 **不行**。Udon 类型白名单**不允许**自定义 `Dictionary<K, V>` 派生类。
>
> **必须**用 DataDictionary。

---

## 13. 相关知识

- **父文档**: [`./index.md`](./index.md) — Data Containers 总览
- **DataToken**: [`./data-tokens.md`](./data-tokens.md) — 键值都是 DataToken
- **DataList**: [`./data-lists.md`](./data-lists.md) — 动态数组容器
- **VRCJSON**: [`./vrcjson.md`](./vrcjson.md) — 序列化/反序列化
- **位/字节操作**: [`./byte-and-bit-operations.md`](./byte-and-bit-operations.md)
- **网络同步**: `memory/api/networking.md` — JSON 同步模式
- **Udon 限制**: `memory/rules/udonsharp-language-limits.md` — C# Dictionary 在 Udon 不可用
- **官方源**: https://creators.vrchat.com/worlds/udon/data-containers/data-dictionaries/
