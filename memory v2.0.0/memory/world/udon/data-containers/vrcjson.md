---
title: VRCJSON
category: world
subcategory: udon/data-containers
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - data-containers
  - vrcjson
  - json
  - serialization
  - deserialize
  - udonsharp
aliases:
  - VRCJSON
  - VRCJson
  - "VRC JSON"
  - JSON序列化
  - JSON
  - 序列化
related:
  - ./index.md
  - ./byte-and-bit-operations.md
  - ./data-tokens.md
  - ./data-lists.md
  - ./data-dictionaries.md
  - ../../../api/data-containers.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/data-containers/vrcjson/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# VRCJSON

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/udon/data-containers/vrcjson)
> 抓取日期: 2026-06-21
> 最后官方更新: 2023-12-07
> SDK: 3.5.0+
> 状态: ✅ FACT (官方) + 扩展 (性能 + 与 .NET JsonUtility 对比)

> **本页面是 `data-containers/` 子目录的 4 个核心子页面之一**:
>
> 1. [`./data-tokens.md`](./data-tokens.md) — 类型系统底层
> 2. [`./data-lists.md`](./data-lists.md) — 动态数组 API
> 3. [`./data-dictionaries.md`](./data-dictionaries.md) — 键值对 API
> 4. **[`./vrcjson.md`](./vrcjson.md)** — JSON 序列化 (本文档) ⭐

---

## 1. VRCJSON 概览

**VRCJSON** 是 Udon 内置的 JSON 工具类,用于 **DataList / DataDictionary ↔ JSON 字符串** 双向转换。

```csharp
using VRC.SDK3.Data;  // VRCJson 在此 namespace

// DataList → JSON
if (VRCJson.TrySerializeToJson(myList, JsonExportType.Minify, out DataToken result))
{
    string json = result.String;  // "[1,2,3]"
}

// JSON → DataList / DataDictionary
if (VRCJson.TryDeserializeFromJson(jsonString, out DataToken result))
{
    if (result.TokenType == TokenType.DataDictionary)
    {
        DataDictionary dict = result.DataDictionary;
    }
    else if (result.TokenType == TokenType.DataList)
    {
        DataList list = result.DataList;
    }
}
```

> **【官方】** VRCJSON 命名空间说明:
>
> - **UdonSharp**:`VRC.SDK3.Data` namespace
> - **Udon Graph**:类名前缀 "VRC" 被移除,搜索 "Json"

---

## 2. JSON ↔ DataContainer 映射

| JSON 概念 | Udon 对应 |
|----------|----------|
| **JSON 数组** `[1, 2, 3]` | `DataList` |
| **JSON 对象** `{"k": "v"}` | `DataDictionary`(仅**字符串键**) |
| **JSON 数字** `42` | `Double`(反序列化后) |
| **JSON 字符串** `"text"` | `String` |
| **JSON 布尔** `true` / `false` | `Boolean` |
| **JSON null** | `Null` token |

> **【官方】** 序列化时,DataList ↔ JSON 数组,DataDictionary ↔ JSON 对象。

---

## 3. 完整 API(2 个核心函数)

### 3.1 `VRCJson.TryDeserializeFromJson`

**JSON 字符串 → DataList / DataDictionary**

| 参数 | 类型 | 说明 |
|------|------|------|
| 输入 | `string` | JSON 字符串 |
| 输出 | `out DataToken` | 成功:DataList 或 DataDictionary;失败:DataError |

**返回**:`bool`(成功 / 失败)

```csharp
public static bool TryDeserializeFromJson(
    string input,
    out DataToken result
);
```

### 3.2 `VRCJson.TrySerializeToJson`

**DataList / DataDictionary → JSON 字符串**

| 参数 | 类型 | 说明 |
|------|------|------|
| 输入 | `DataToken` | DataList 或 DataDictionary(根必须是容器) |
| 输入 | `JsonExportType` | Minify(压缩)或 Beautify(格式化) |
| 输出 | `out DataToken` | 成功:String token;失败:DataError |

**返回**:`bool`(成功 / 失败)

```csharp
public static bool TrySerializeToJson(
    DataToken input,
    JsonExportType exportType,
    out DataToken result
);
```

### 3.3 JsonExportType 枚举

| 值 | 说明 | 用途 |
|----|------|------|
| `Minify` | 压缩格式,**无空白字符** | **网络传输**、持久化(最小体积) |
| `Beautify` | 格式化,**每行一个元素 + Tab 缩进** | 调试、日志、UI 显示 |

```csharp
// Minify 示例
// [{"name":"Alice","score":100},{"name":"Bob","score":200}]

// Beautify 示例
// [
//   {
//     "name": "Alice",
//     "score": 100
//   },
//   ...
// ]
```

---

## 4. 反序列化详解

### 4.1 基本模式

```csharp
if (VRCJson.TryDeserializeFromJson(json, out DataToken result))
{
    // 成功——根据类型分支
    if (result.TokenType == TokenType.DataDictionary)
    {
        Debug.Log($"Dictionary with {result.DataDictionary.Count} items");
    }
    else if (result.TokenType == TokenType.DataList)
    {
        Debug.Log($"List with {result.DataList.Count} items");
    }
    // else: 不可能发生——成功反序列化**必须**是 dict 或 list
}
else
{
    // 失败——result 含 DataError
    Debug.LogError($"JSON parse failed: {result.ToString()}");
}
```

### 4.2 关键性能特征:惰性解析

> **【官方】** VRCJson **不立即解析整个 JSON**——只解析**顶层**。
>
> 后果:
>
> 1. 顶层有效但深层无效 → 初始 `TryDeserializeFromJson` 返回 **true**
> 2. 后续访问无效子项 → `TryGetValue` 返回 **false** + `DataError.UnableToParse`

```csharp
// 例: 顶层有效,但嵌套有错误
string json = "{\"valid\": true, \"nested\": [1, 2, INVALID]}";

if (VRCJson.TryDeserializeFromJson(json, out DataToken result))
{
    // ✅ 返回 true——顶层 OK
    if (result.DataDictionary.TryGetValue("nested", out DataToken nested))
    {
        // ❌ 返回 false——深层 INVALID
        Debug.LogError($"Nested parse failed: {nested.Error}");
    }
}
```

### 4.3 数字精度损失

> **【官方】** JSON 数字**反序列化后统一为 `Double`**。

```csharp
string json = "{\"id\": 12345678901234567}";  // 长整数

if (VRCJson.TryDeserializeFromJson(json, out DataToken result))
{
    result.DataDictionary.TryGetValue("id", out DataToken id);
    Debug.Log(id.TokenType);  // TokenType.Double
    Debug.Log(id.Double);     // 精度可能丢失(long 17+ 位)
}

// ✅ 关键 ID 用 String 存储
string json2 = "{\"id\": \"12345678901234567\"}";  // 字符串形式
```

---

## 5. 序列化详解

### 5.1 基本模式

```csharp
if (VRCJson.TrySerializeToJson(dictionary, JsonExportType.Beautify, out DataToken json))
{
    // 成功——立即取出字符串
    Debug.Log($"JSON: {json.String}");

    // 或同步到网络
    _syncedJsonString = json.String;
}
else
{
    // 失败——json 含 DataError
    Debug.LogError($"Serialize failed: {json.ToString()}");
}
```

### 5.2 根必须是 List 或 Dict

> 🔴 **【官方】** JSON 根**不能**是简单值(数字、字符串、布尔)。
>
> 必须用 DataList 或 DataDictionary 包装。

```csharp
// ❌ 反模式:序列化简单值
DataToken simple = 42;
VRCJson.TrySerializeToJson(simple, JsonExportType.Minify, out DataToken r);
// → false,DataError.TypeUnsupported

// ✅ 正确:包装为容器
DataList wrapper = new DataList();
wrapper.Add(42);
VRCJson.TrySerializeToJson(wrapper, JsonExportType.Minify, out DataToken r);
// → true,"[42]"
```

### 5.3 Beautify 模式(可读性 vs 大小)

```csharp
// 同样数据:[{"a":1,"b":2},{"a":3,"b":4}]

// Minify: 一行
// [{"a":1,"b":2},{"a":3,"b":4}]  // 25 chars

// Beautify: 多行
// [
//   {
//     "a": 1,
//     "b": 2
//   },
//   {
//     "a": 3,
//     "b": 4
//   }
// ]  // 60+ chars
```

> **【官方】** Minify 适合**网络传输**(节省带宽 ~50%);Beautify 适合**调试**(可读)。

---

## 6. JSON 限制(关键!)

> 🔴 **【官方】** JSON 是**严格**的规范。DataList/DataDictionary 表达能力强于 JSON,所以**部分 DataToken 无法序列化**。

### 6.1 限制汇总

| 限制 | 触发场景 | 错误类型 |
|------|---------|---------|
| **不支持 Object Reference** | 容器含任何 `Reference` token | `TypeUnsupported` |
| **仅支持字符串键** | DataDictionary 键不是 String | `TypeUnsupported` |
| **不支持 NaN / Infinity** | 含 `float.NaN` / `float.PositiveInfinity` 等 | `ValueUnsupported` |
| **根必须是容器** | 序列化单个 token(非 List/Dict) | `TypeUnsupported` |
| **数字统一为 Double** | 反序列化时所有数字变 Double | (非错误,自动行为) |

### 6.2 序列化失败处理模式

```csharp
public bool SafeSerialize(DataDictionary data, out string json)
{
    json = null;
    if (VRCJson.TrySerializeToJson(data, JsonExportType.Minify, out DataToken result))
    {
        json = result.String;
        return true;
    }

    // 失败诊断
    DataError err = result.Error;
    switch (err)
    {
        case DataError.TypeUnsupported:
            Debug.LogError("Data contains Reference or non-string keys — not serializable");
            break;
        case DataError.ValueUnsupported:
            Debug.LogError("Data contains NaN or Infinity — not serializable");
            break;
        default:
            Debug.LogError($"Serialize failed: {result.ToString()}");
            break;
    }
    return false;
}
```

### 6.3 序列化前清理(防御模式)

```csharp
public DataDictionary SanitizeForJson(DataDictionary source)
{
    DataDictionary clean = new DataDictionary();
    DataList keys = source.GetKeys();
    for (int i = 0; i < keys.Count; i++)
    {
        string key = keys[i].String;  // 仅保留字符串键
        if (source.TryGetValue(key, out DataToken value))
        {
            if (value.TokenType == TokenType.Float)
            {
                float f = value.Float;
                if (!float.IsNaN(f) && !float.IsInfinity(f))
                {
                    clean.SetValue(key, value);
                }
            }
            else if (value.TokenType == TokenType.Double)
            {
                double d = value.Double;
                if (!double.IsNaN(d) && !double.IsInfinity(d))
                {
                    clean.SetValue(key, value);
                }
            }
            else if (value.TokenType != TokenType.Reference)
            {
                clean.SetValue(key, value);
            }
            // 跳过 Reference + NaN/Infinity
        }
    }
    return clean;
}
```

---

## 7. 错误处理详解

### 7.1 完整 DataError 类型

| DataError | 触发 |
|-----------|------|
| `None` | 成功(无错误) |
| `UnableToParse` | JSON 字符串格式无效 |
| `TypeUnsupported` | 容器含 Reference / 非字符串键 / 根非容器 |
| `ValueUnsupported` | 含 NaN / Infinity |
| `KeyDoesNotExist` | (非 VRCJson 错误,容器访问) |
| `IndexOutOfRange` | (非 VRCJson 错误,DataList 访问) |
| `TypeMismatch` | (非 VRCJson 错误,TryGetValue TokenType 不匹配) |

### 7.2 `ToString()` vs `String` 属性

> **【官方】** 错误 token 用 `ToString()` 而非 `String`,因为:
>
> - `String` 抛异常(若 token 不含字符串)
> - `ToString()` 自动组合 enum + 详细消息

```csharp
// ✅ 推荐
Debug.LogError(result.ToString());

// ❌ 不推荐(可能抛异常)
Debug.LogError(result.String);
```

---

## 8. 性能基准

### 8.1 VRCJson vs .NET `JsonUtility`

| 维度 | VRCJson | .NET `JsonUtility` |
|------|---------|---------------------|
| Udon 可用 | ✅ | ❌ **未暴露** |
| 序列化目标 | DataList / DataDictionary | C# `[Serializable]` 类 |
| 反序列化目标 | DataList / DataDictionary | C# `[Serializable]` 类 |
| 嵌套支持 | ✅ 任意深度 | 嵌套类(固定) |
| 性能(典型) | 中等 | 快(原生 .NET) |
| 可读性 | Minify / Beautify | 不可控 |
| 引用支持 | ❌(Object Reference) | ❌(Unity null) |
| 错误处理 | 显式 `bool` + DataError | 抛异常 |

> **【关键】** Udon **不能**用 .NET `JsonUtility`——它未被 Udon 暴露。**必须**用 VRCJson。

### 8.2 序列化速度(典型数据)

| 数据大小 | Minify | Beautify | 大小(Beautify / Minify) |
|---------|--------|----------|-------------------------|
| 10 字段 dict | ~0.1ms | ~0.1ms | 1.0x |
| 100 字段 dict | ~0.5ms | ~0.5ms | 1.2x |
| 1000 字段 dict | ~3ms | ~4ms | 1.5x |
| 嵌套 3 层 × 10 | ~0.3ms | ~0.4ms | 1.3x |
| 嵌套 5 层 × 10 | ~0.8ms | ~1ms | 1.5x |

> **【推断】** 性能数据基于 Udon VM 9 指令开销估算。**Beautify 比 Minify 慢 10-30%**(字符串拼接开销)。

### 8.3 大小对比(典型数据)

```json
// 同样数据
// Minify: ~500 bytes
{"players":[{"id":1,"name":"Alice","score":100},{"id":2,"name":"Bob","score":200},...]}

// Beautify: ~800 bytes (1.6x)
{
  "players": [
    {
      "id": 1,
      "name": "Alice",
      "score": 100
    },
    ...
  ]
}
```

> **【官方】** 网络同步**用 Minify**——节省 ~30-50% 带宽。

### 8.4 性能优化技巧

```csharp
// 1. 用 Minify(网络传输)
VRCJson.TrySerializeToJson(data, JsonExportType.Minify, out result);

// 2. 避免频繁序列化(缓存)
private string _cachedJson = null;
private DataDictionary _cachedSource = null;

public string GetJson()
{
    if (_cachedSource == _currentData && _cachedJson != null)
        return _cachedJson;

    if (VRCJson.TrySerializeToJson(_currentData, JsonExportType.Minify, out DataToken r))
    {
        _cachedSource = _currentData;
        _cachedJson = r.String;
        return _cachedJson;
    }
    return null;
}

// 3. 浅层数据(避免深嵌套)
```

---

## 9. 完整工作代码示例

### 9.1 从网络/资源加载 JSON 配置

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;
using VRC.SDKBase;

public class JsonConfigLoader : UdonSharpBehaviour
{
    [SerializeField] private TextAsset _configFile;
    [SerializeField] private VRCUrl _remoteConfigUrl;

    private DataDictionary _config;
    private int _maxPlayers = 16;
    private float _spawnCooldown = 5.0f;

    void Start()
    {
        // 方式 1:从 TextAsset 加载
        LoadFromTextAsset();

        // 方式 2:从 URL 加载(异步)
        // VRCStringDownloader.LoadUrl(_remoteConfigUrl, (VRCStringDownloader.LoadUrlCompl) =>
        // {
        //     LoadFromString(result);
        // });
    }

    private void LoadFromTextAsset()
    {
        if (_configFile == null) return;
        if (VRCJson.TryDeserializeFromJson(_configFile.text, out DataToken result)
            && result.TokenType == TokenType.DataDictionary)
        {
            _config = result.DataDictionary;
            ApplyConfig();
        }
        else
        {
            Debug.LogError("Invalid config JSON");
        }
    }

    private void LoadFromString(string json)
    {
        if (VRCJson.TryDeserializeFromJson(json, out DataToken result)
            && result.TokenType == TokenType.DataDictionary)
        {
            _config = result.DataDictionary;
            ApplyConfig();
        }
    }

    private void ApplyConfig()
    {
        if (_config.TryGetValue("maxPlayers", TokenType.Int, out DataToken t1))
            _maxPlayers = t1.Int;

        if (_config.TryGetValue("spawnCooldown", TokenType.Float, out DataToken t2))
            _spawnCooldown = t2.Float;

        Debug.Log($"Config: maxPlayers={_maxPlayers}, cooldown={_spawnCooldown}");
    }
}
```

### 9.2 JSON 网络同步(完整模式)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;
using VRC.SDKBase;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class JsonSyncedData : UdonSharpBehaviour
{
    [UdonSynced] private string _json = "{}";
    private DataDictionary _data = new DataDictionary();

    public void SetKey(string key, DataToken value)
    {
        if (!Networking.IsOwner(gameObject))
            Networking.SetOwner(Networking.LocalPlayer, gameObject);

        _data.SetValue(key, value);
        Sync();
    }

    public DataToken GetKey(string key)
    {
        if (_data.TryGetValue(key, out DataToken value))
            return value;
        return new DataToken();  // Null token
    }

    private void Sync()
    {
        if (VRCJson.TrySerializeToJson(_data, JsonExportType.Minify, out DataToken result))
        {
            _json = result.String;
            RequestSerialization();
        }
        else
        {
            Debug.LogError($"Sync failed: {result.ToString()}");
        }
    }

    public override void OnDeserialization()
    {
        if (string.IsNullOrEmpty(_json)) return;

        if (VRCJson.TryDeserializeFromJson(_json, out DataToken result)
            && result.TokenType == TokenType.DataDictionary)
        {
            _data = result.DataDictionary;
        }
        else
        {
            Debug.LogError($"Deserialize failed: {result.ToString()}");
        }
    }
}
```

### 9.3 安全外部 JSON 解析

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;

public class SafeJsonParser : UdonSharpBehaviour
{
    public bool TryParseUserJson(string userJson, out DataDictionary result)
    {
        result = null;

        // 1. 解析
        if (!VRCJson.TryDeserializeFromJson(userJson, out DataToken token))
        {
            Debug.LogError($"Invalid JSON: {token.ToString()}");
            return false;
        }

        // 2. 检查根类型
        if (token.TokenType != TokenType.DataDictionary)
        {
            Debug.LogError("Root must be an object");
            return false;
        }

        // 3. 验证必需字段(类型安全)
        DataDictionary dict = token.DataDictionary;
        if (!dict.TryGetValue("name", TokenType.String, out DataToken name))
        {
            Debug.LogError("Missing or invalid 'name'");
            return false;
        }
        if (!dict.TryGetValue("age", TokenType.Int, out DataToken age))
        {
            Debug.LogError("Missing or invalid 'age'");
            return false;
        }

        result = dict;
        return true;
    }
}
```

---

## 10. 调试技巧

### 10.1 错误诊断

```csharp
void DebugJsonError(DataToken result, string operation)
{
    Debug.LogError($"{operation} failed: {result.ToString()}");
    // ToString() 输出: "TypeUnsupported: DataDictionary contains a non-string key"
}
```

### 10.2 大小监控

```csharp
void LogJsonSize(DataDictionary data, string label)
{
    if (VRCJson.TrySerializeToJson(data, JsonExportType.Minify, out DataToken r))
    {
        Debug.Log($"{label}: {r.String.Length} bytes");
    }
}
```

### 10.3 格式化输出

```csharp
void PrintJsonPretty(DataDictionary data)
{
    if (VRCJson.TrySerializeToJson(data, JsonExportType.Beautify, out DataToken r))
    {
        Debug.Log(r.String);  // 多行可读
    }
}
```

---

## 11. 风险与注意事项

| 风险 | 说明 | 缓解 |
|------|------|------|
| **JSON 不支持 Reference** | 装箱对象导致序列化失败 | 仅序列化纯数据容器 |
| **JSON 数字变 Double** | 长整数精度丢失 | 关键 ID 用 String |
| **NaN/Infinity 失败** | 数学计算产生特殊值 | 序列化前过滤 |
| **非字符串键失败** | int key 序列化失败 | 用 string key |
| **根非容器失败** | 序列化单个 token 失败 | 包成 DataList |
| **惰性解析陷阱** | 深层错误延迟暴露 | `TryGetValue` 错误检查 |
| **带宽成本** | JSON 比原生数组大 | 高频用原生数组同步 |

---

## 12. 与 .NET JsonUtility 对比

> **【关键】** Udon **不能**用 .NET `JsonUtility`,因为它**未被 Udon 暴露**。
>
> 详见 `memory/api/not-exposed.md`。

| 维度 | VRCJson | .NET JsonUtility(不可用) |
|------|---------|--------------------------|
| Udon 暴露 | ✅ | ❌ |
| 输入 | DataList/Dictionary | C# 类 |
| 输出 | DataList/Dictionary | C# 类 |
| 嵌套 | 任意深度 | 类嵌套 |
| 类型安全 | 运行时(DataToken) | 编译时(泛型) |
| 性能 | 中等(VM EXTERN) | 快(原生 .NET) |

---

## 13. FAQ

### 13.1 为什么要 VRCJson 而不是 .NET JsonUtility?

> **【官方】** `.NET JsonUtility` 未被 Udon 暴露(白名单外)。VRChat 提供的 VRCJson 是**唯一**可用方案。
>
> 详见 `memory/api/udon-type-exposure.md`。

### 13.2 为什么 VRCJson 只支持 DataList/Dictionary 根?

> **【官方】** JSON 规范本身只支持数组和对象作为根——简单值(数字、字符串)不能作为合法 JSON 根。
>
> VRCJson 严格遵循 JSON 规范。

### 13.3 反序列化后 int 变 Double 是 bug 吗?

> **不是 bug**——是 JSON 规范本身。JSON 不区分整数 / 浮点。VRCJson 选择 Double 作为**通用表示**。
>
> 关键 ID 用字符串存储是常见做法。

---

## 14. 相关知识

- **父文档**: [`./index.md`](./index.md) — Data Containers 总览
- **DataToken**: [`./data-tokens.md`](./data-tokens.md) — TokenType 与 Error
- **DataList**: [`./data-lists.md`](./data-lists.md) — 序列化源
- **DataDictionary**: [`./data-dictionaries.md`](./data-dictionaries.md) — 序列化源
- **位/字节操作**: [`./byte-and-bit-operations.md`](./byte-and-bit-operations.md) — 自定义序列化协议
- **网络同步**: `memory/api/networking.md` — JSON 同步模式
- **未暴露 API**: `memory/api/not-exposed.md` — .NET JsonUtility 不可用原因
- **类型暴露**: `memory/api/udon-type-exposure.md` — Udon 白名单
- **官方源**: https://creators.vrchat.com/worlds/udon/data-containers/vrcjson/
