---
title: API: Data Containers
category: api
knowledge_level: applied
status: active
tags:
  - api
  - data-containers
  - data-token
  - data-list
  - data-dictionary
  - vrcjson
  - serialization
aliases:
  - Data Containers API
  - "DataToken API"
  - "DataList API"
  - "DataDictionary API"
  - "VRCJson API"
related:
  - world/udon/data-containers/index.md
  - world/udon/data-containers/data-tokens.md
  - world/udon/data-containers/data-lists.md
  - world/udon/data-containers/data-dictionaries.md
  - world/udon/data-containers/vrcjson.md
  - world/udon/data-containers/byte-and-bit-operations.md
  - api/networking.md
  - patterns/bit-packed-flags.md
  - rules/udonsharp-language-limits.md
source: 本地知识库整理(基于 VRChat 官方文档)
source_type: community
version: 1.0
last_review: 2026-06-21
confidence: High
---

# API: Data Containers

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/udon/data-containers/)
> 状态: ✅ API 索引页(指向 4 个详细子页面)
> 命名空间: `VRC.SDK3.Data`
> SDK: 3.5.0+

---

## Overview

Udon Data Containers 提供 4 个核心 API 类,用于存储、查询、序列化数据:

| API 类 | 用途 | 详细文档 |
|--------|------|---------|
| **`DataToken`** | 类型系统底层(异构值 + 类型擦除) | [`world/udon/data-containers/data-tokens.md`](../world/udon/data-containers/data-tokens.md) |
| **`DataList`** | 动态数组(类似 C# `List<T>`) | [`world/udon/data-containers/data-lists.md`](../world/udon/data-containers/data-lists.md) |
| **`DataDictionary`** | 键值对(类似 C# `Dictionary<K,V>`) | [`world/udon/data-containers/data-dictionaries.md`](../world/udon/data-containers/data-dictionaries.md) |
| **`VRCJson`** | JSON 序列化/反序列化 | [`world/udon/data-containers/vrcjson.md`](../world/udon/data-containers/vrcjson.md) |

> **使用前提**(UdonSharp):`using VRC.SDK3.Data;`

---

## 1. DataToken API 速查

**位置**: `VRC.SDK3.Data.DataToken`(struct)

**TokenType 枚举**(部分):

| TokenType | 用途 |
|-----------|------|
| `Null` | 空值 |
| `Boolean` | 布尔 |
| `Byte` / `SByte` / `Short` / `UShort` / `Int` / `UInt` / `Long` / `ULong` | 整数 |
| `Float` / `Double` | 浮点 |
| `String` | 字符串 |
| `DataList` | 嵌套列表 |
| `DataDictionary` | 嵌套字典 |
| `Reference` | 任意 C# 对象(**不可序列化**) |
| `DataError` | 错误信息 |

**关键方法**:

| 方法 | 用途 |
|------|------|
| `TokenType` 属性 | 查询类型 |
| `IsNumber` / `IsNull` 属性 | 类型安全检查 |
| `.Int` / `.Float` / `.String` / `.DataList` / `.DataDictionary` | 提取值(类型不匹配抛异常) |
| `.Error` | 提取错误(永不抛异常) |
| `Bitcast(TokenType)` | 值保留型类型转换(同字节宽度) |
| `ToString()` | 安全字符串化(永不抛异常) |

**详细文档**: [`data-tokens.md`](../world/udon/data-containers/data-tokens.md)

---

## 2. DataList API 速查

**位置**: `VRC.SDK3.Data.DataList`

**Properties**:

| 属性 | 类型 | 说明 |
|------|------|------|
| `Count` | `int` | 元素数 |
| `Capacity` | `int` | 容量(可读写) |

**核心方法**:

| 方法 | 用途 |
|------|------|
| `Add(DataToken)` | 末尾追加 |
| `Insert(int, DataToken)` | 指定位置插入 |
| `Remove(DataToken)` / `RemoveAt(int)` | 删除 |
| `Contains(DataToken)` | 查询 |
| `IndexOf(DataToken)` | 找索引 |
| `Sort()` | 排序 |
| `TryGetValue(int[, TokenType], out DataToken)` | 安全取值 |
| `ShallowClone()` / `DeepClone()` | 克隆 |
| `ToArray()` | 转 DataToken[] |

**详细文档**: [`data-lists.md`](../world/udon/data-containers/data-lists.md)

---

## 3. DataDictionary API 速查

**位置**: `VRC.SDK3.Data.DataDictionary`

**Properties**:

| 属性 | 类型 | 说明 |
|------|------|------|
| `Count` | `int` | 键值对数 |

**核心方法**:

| 方法 | 用途 |
|------|------|
| `SetValue(DataToken key, DataToken value)` | 设置值(覆盖/添加) |
| `Add(DataToken key, DataToken value)` | 仅当 key 不存在时添加 |
| `Remove(DataToken key)` | 删除 |
| `ContainsKey(DataToken key)` / `ContainsValue(DataToken value)` | 查询 |
| `GetKeys()` / `GetValues()` | 枚举(返回 DataList) |
| `TryGetValue(DataToken key[, TokenType], out DataToken)` | 安全取值 |
| `ShallowClone()` / `DeepClone()` | 克隆 |

**关键限制**: **键可以是任意 DataToken**,但 **JSON 序列化仅支持字符串键**。

**详细文档**: [`data-dictionaries.md`](../world/udon/data-containers/data-dictionaries.md)

---

## 4. VRCJson API 速查

**位置**: `VRC.SDK3.Data.VRCJson`(静态类)

**核心方法**:

```csharp
// JSON → DataList/DataDictionary
bool VRCJson.TryDeserializeFromJson(string input, out DataToken result);

// DataList/DataDictionary → JSON
bool VRCJson.TrySerializeToJson(DataToken input, JsonExportType exportType, out DataToken result);
```

**JsonExportType**:

| 值 | 用途 |
|----|------|
| `Minify` | 压缩格式(**网络传输**) |
| `Beautify` | 格式化(**调试/UI**) |

**关键限制**:

- ❌ 不支持 Object Reference
- ❌ DataDictionary 仅字符串键
- ❌ 不支持 NaN / Infinity
- ❌ 根必须是 List 或 Dict
- ⚠️ 数字统一为 Double(反序列化后)

**详细文档**: [`vrcjson.md`](../world/udon/data-containers/vrcjson.md)

---

## 5. DataError 枚举

当容器操作失败,返回的 DataToken 含 DataError:

| DataError | 触发 |
|-----------|------|
| `None` | 成功 |
| `KeyDoesNotExist` | DataDictionary key 不存在 |
| `IndexOutOfRange` | DataList 越界 |
| `TypeMismatch` | 类型不匹配(`TryGetValue` + TokenType) |
| `TypeUnsupported` | Reference 序列化 / 非字符串键序列化 / 根非容器 |
| `ValueUnsupported` | NaN / Infinity 序列化 |
| `UnableToParse` | JSON 无效 |

**最佳实践**:用 `result.ToString()` 而非 `result.String`(后者可能抛异常)。

---

## 6. 与 C# 对应类型的限制

> 🔴 **关键事实**:Udon **不允许**自定义 `List<T>` / `Dictionary<K, V>` 派生类。**必须**用 DataList / DataDictionary。

| 需求 | C# 替代 | Udon 替代 |
|------|---------|----------|
| 动态数组 | `List<T>` | `DataList` |
| 键值对 | `Dictionary<K, V>` | `DataDictionary` |
| JSON 序列化 | `JsonUtility`(**未暴露**) | `VRCJson` |
| 装箱对象 | `object` | `DataToken.Reference`(**不可序列化**) |

**性能含义**(【推断】):DataList/DataDictionary 比原生数组慢 **5-10 倍**——VM EXTERN + 类型检查 + DataToken 装箱的开销。

详见 `memory/rules/udonsharp-language-limits.md` 和 `memory/api/not-exposed.md`。

---

## 7. 典型使用模式

### 7.1 JSON 网络同步(官方推荐)

```csharp
[UdonSynced] private string _json;
private DataDictionary _data = new DataDictionary();

public override void OnPreSerialization()
{
    if (VRCJson.TrySerializeToJson(_data, JsonExportType.Minify, out DataToken result))
        _json = result.String;
}

public override void OnDeserialization()
{
    if (VRCJson.TryDeserializeFromJson(_json, out DataToken result)
        && result.TokenType == TokenType.DataDictionary)
        _data = result.DataDictionary;
}
```

### 7.2 安全外部数据访问

```csharp
// 外部 JSON → 类型安全访问
if (VRCJson.TryDeserializeFromJson(json, out DataToken t)
    && t.TokenType == TokenType.DataDictionary)
{
    DataDictionary dict = t.DataDictionary;
    if (dict.TryGetValue("name", TokenType.String, out DataToken nameToken))
    {
        Debug.Log(nameToken.String);
    }
}
```

### 7.3 嵌套数据(任意深度)

```csharp
DataDictionary config = new DataDictionary();
DataDictionary user = new DataDictionary();
user.SetValue("name", "Alice");
user.SetValue("score", 1000);
config.SetValue("user", user);

// 访问 config["user"]["score"]
if (config.TryGetValue("user", out DataToken userToken)
    && userToken.TokenType == TokenType.DataDictionary)
{
    DataDictionary userDict = userToken.DataDictionary;
    if (userDict.TryGetValue("score", TokenType.Int, out DataToken scoreToken))
    {
        Debug.Log(scoreToken.Int);
    }
}
```

---

## 8. 性能与陷阱

| 陷阱 | 说明 | 缓解 |
|------|------|------|
| **方括号不安全** | `dict["key"]` 在 key 不存在时会 halt | 用 `TryGetValue` |
| **类型不匹配抛异常** | `.String` 访问 float token 会 halt | 用 `TokenType` 检查 |
| **JSON 数字变 Double** | 反序列化后所有数字变 Double | 关键 ID 用 String |
| **Reference 不可序列化** | 含 GameObject/Player 的容器无法 JSON 同步 | 仅同步纯数据 |
| **DeepClone 不克隆 Reference** | 数组、GameObject 保持原引用 | 浅层复制后修改小心 |
| **嵌套过深** | JSON 解析性能急剧下降 | 嵌套深度 ≤ 5 |

---

## 9. 相关知识

- **详细子页面**:
  - [`../world/udon/data-containers/data-tokens.md`](../world/udon/data-containers/data-tokens.md) — DataToken 完整 API
  - [`../world/udon/data-containers/data-lists.md`](../world/udon/data-containers/data-lists.md) — DataList 完整 API
  - [`../world/udon/data-containers/data-dictionaries.md`](../world/udon/data-containers/data-dictionaries.md) — DataDictionary 完整 API
  - [`../world/udon/data-containers/vrcjson.md`](../world/udon/data-containers/vrcjson.md) — VRCJson 完整 API
  - [`../world/udon/data-containers/byte-and-bit-operations.md`](../world/udon/data-containers/byte-and-bit-operations.md) — 位/字节底层
  - [`../world/udon/data-containers/index.md`](../world/udon/data-containers/index.md) — 父索引
- **网络同步**: [`networking.md`](networking.md) — 容器同步模式
- **位域压缩**: `memory/patterns/bit-packed-flags.md` — 字节级压缩
- **Udon 限制**: `memory/rules/udonsharp-language-limits.md` — C# List/Dictionary 不可用
- **未暴露 API**: `memory/api/not-exposed.md` — JsonUtility 不可用原因
- **官方源**: https://creators.vrchat.com/worlds/udon/data-containers/
