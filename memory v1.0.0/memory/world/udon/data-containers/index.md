# Data Containers & VRCJson

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/udon/data-containers/)
> 置信度: High
> SDK: 3.5.0+
> Last Updated: 2026-06-15
> **迁移说明**: 本文档为 `world/data-containers.md` 的权威位置

---

## Overview

Data Containers 提供类似 C# List 和 Dictionary 的数据结构，用于存储和操作数据。VRCJson 允许与标准 JSON 格式互相转换。

---

## Data Token Types

每个 DataToken 存储一个变量，支持以下类型：

| 类型 | 说明 |
|------|------|
| Null | 空值 |
| Boolean | 布尔值 |
| SByte, Byte | 有/无符号字节 |
| Short, UShort | 有/无符号短整型 |
| Int, UInt | 整型 |
| Long, ULong | 长整型 |
| Float, Double | 浮点数 |
| String | 字符串 |
| DataList | 存储其他 DataToken（可嵌套） |
| DataDictionary | 存储其他 DataToken（可嵌套） |
| Object Reference | 可存储任何对象，但**不能序列化** |
| DataError | 错误信息枚举 |

---

## Data Lists

### 基本操作
```csharp
DataList list = new DataList();
list.Add(42);
list.Add("hello");
list.Insert(0, 3.14f);
list.RemoveAt(1);
int count = list.Count;
object value = list[0];
```

### 排序
```csharp
list.Sort();  // 数字优先，然后 Null < Number < String < List < Dict < Reference
```

### 克隆
```csharp
DataList shallow = list.ShallowClone();
DataList deep = list.DeepClone();  // 递归克隆所有嵌套容器
```

### 同步方法 ⚠️
Data Lists **不能直接同步**。推荐通过 JSON 序列化：
```csharp
[UdonSynced] private string _json = "";

public override void OnPreSerialization()
{
    if (VRCJson.TrySerializeToJson(_list, JsonExportType.Minify, out DataToken result))
        _json = result.String;
}

public override void OnDeserialization()
{
    if (VRCJson.TryDeserializeFromJson(_json, out DataToken result))
        _list = result.DataList;
}
```

---

## Data Dictionaries

### 基本操作
```csharp
DataDictionary dict = new DataDictionary();
dict.Set("key1", 42);
dict.Set("key2", "value");
dict.Set("nested", new DataList());

object value = dict["key1"];
bool exists = dict.ContainsKey("key1");
dict.Remove("key1");

DataList keys = dict.GetKeys();
DataList values = dict.GetValues();
```

### 克隆
```csharp
DataDictionary shallow = dict.ShallowClone();
DataDictionary deep = dict.DeepClone();
```

### JSON 同步
与 DataList 相同，通过字符串序列化。

---

## VRCJson API

### 反序列化 (JSON → Data)
```csharp
if (VRCJson.TryDeserializeFromJson(jsonString, out DataToken result))
{
    if (result.TokenType == DataTokenType.DataList)
        _list = result.DataList;
    else if (result.TokenType == DataTokenType.DataDictionary)
        _dict = result.DataDictionary;
}
```

### 序列化 (Data → JSON)
```csharp
if (VRCJson.TrySerializeToJson(data, JsonExportType.Minify, out DataToken result))
{
    string json = result.String;
}
```

### JsonExportType
| 类型 | 说明 |
|------|------|
| Minify | 压缩格式（无缩进） |
| Pretty | 格式化（带缩进） |

---

## JSON 限制 ⚠️

JSON 有严格限制，序列化时需注意：

1. **仅支持字符串键**: DataDictionary 中的非字符串键会被拒绝
2. **根只能是 List 或 Dict**: 不能序列化单独的 Token
3. **不支持 Reference**: 包含对象引用的容器无法序列化
4. **不支持 NaN/Infinity**: 浮点数值必须是有效数字

### 错误类型
| 错误 | 含义 |
|------|------|
| DoesNotExist | 访问不存在的键或索引 |
| TypeMismatch | 类型不匹配 |
| TypeUnsupported | 数据类型不支持序列化格式 |
| ValueUnsupported | 值不被支持（如 NaN/Infinity） |
| MalformedJson | JSON 格式无效 |

---

## 性能考虑

1. **嵌套深度**: 避免过深嵌套，性能会下降
2. **JSON 序列化开销**: 每次序列化/反序列化都有性能成本
3. **数组 vs DataList**: 如果不需要动态大小，使用普通数组更高效
4. **DataToken 装箱**: 频繁的类型检查和装箱会影响性能

---

## Byte and Bit Operations

> 详细文档: [`./byte-and-bit-operations.md`](./byte-and-bit-operations.md)
> 参考: creators.vrchat.com/worlds/udon/data-containers/byte-and-bit-operations

Data Containers 还支持底层二进制操作，用于高级用例（如位域压缩、自定义序列化协议）。

### 三大核心工具

| 工具 | 用途 | 关键方法 |
|------|------|----------|
| **`DataToken.Bitcast()`** | 值保留型类型转换（同字节宽度） | `doubleToken.Bitcast(TokenType.ULong)` |
| **`System.BitConverter`** | 基本类型 ↔ `byte[]` | `BitConverter.GetBytes(int)`、`ToInt32(byte[], int)` |
| **`System.Buffer`** | 数组间高速内存块复制 | `Buffer.BlockCopy(src, srcOff, dst, dstOff, count)` |

### 位域压缩 (Bitset)

8 个独立 `[UdonSynced] bool` → 1 个 `[UdonSynced] byte`,**节省 87.5% 序列化空间**。详见 `memory/patterns/bit-packed-flags.md`。

### 快速跳转

- **位运算符 ( `&`、`|`、`^`、`~`、`<<`、`>>` )**: 详见 `byte-and-bit-operations.md` §4
- **位标志模板代码**: 详见 `byte-and-bit-operations.md` §11
- **与 AudioLinkMiniPlayer._flags 对比**: 详见 `byte-and-bit-operations.md` §8

---

## 相关文档

- `memory/world/udon/data-containers/byte-and-bit-operations.md` — **位/字节操作**
- `memory/api/networking.md` — 网络同步模式
- `memory/patterns/bit-packed-flags.md` — 位域压缩模式
- `memory/rules/udonsharp-language-limits.md` — 集合类型限制（List/Dictionary 禁用）

---

## 迁移历史

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-06-15 | 迁移 | 从 `world/data-containers.md` 整合到本文件 |
| 2026-06-10 | 创建 | 原始 `world/data-containers.md` 文档 |
