---
title: Data Tokens
category: world
subcategory: udon/data-containers
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - data-containers
  - data-token
  - token-type
  - type-system
  - udonsharp
aliases:
  - DataToken
  - 数据令牌
  - "Data Token"
  - 数据 Token
  - Tokens
related:
  - ./index.md
  - ./byte-and-bit-operations.md
  - ./data-lists.md
  - ./data-dictionaries.md
  - ./vrcjson.md
  - ../../../api/data-containers.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/data-containers/data-tokens/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# Data Tokens

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/udon/data-containers/data-tokens)
> 抓取日期: 2026-06-21
> 最后官方更新: 2024-07-30
> SDK: 3.5.0+
> 状态: ✅ FACT (官方) + 扩展 (性能 + 与 C# object 对比)

> **本页面是 `data-containers/` 子目录的 4 个核心子页面之一**:
>
> 1. **[`./data-tokens.md`](./data-tokens.md)** — 类型系统底层 (本文档) ⭐
> 2. [`./data-lists.md`](./data-lists.md) — 动态数组 API
> 3. [`./data-dictionaries.md`](./data-dictionaries.md) — 键值对 API
> 4. [`./vrcjson.md`](./vrcjson.md) — JSON 序列化

---

## 1. DataToken 类型系统总览

**DataToken** 是 Udon 容器(DataList / DataDictionary)存储的**基本单元**。每个 token **只能存一个变量**,但这个变量可以是另一个 DataList / DataDictionary(实现任意深度嵌套)。

### 1.1 支持的 TokenType(完整列表)

| TokenType | C# 类型 | 说明 | 序列化 |
|-----------|---------|------|--------|
| `Null` | `null` | 空值 | ✅ |
| `Boolean` | `bool` | 布尔值 | ✅ |
| `SByte` | `sbyte` | 8 位有符号 | ✅ |
| `Byte` | `byte` | 8 位无符号 | ✅ |
| `Short` | `short` | 16 位有符号 | ✅ |
| `UShort` | `ushort` | 16 位无符号 | ✅ |
| `Int` | `int` | 32 位有符号 | ✅ |
| `UInt` | `uint` | 32 位无符号 | ✅ |
| `Long` | `long` | 64 位有符号 | ✅ |
| `ULong` | `ulong` | 64 位无符号 | ✅ |
| `Float` | `float` | 32 位浮点 | ✅ (但 JSON 限制 NaN/Infinity) |
| `Double` | `double` | 64 位浮点 | ✅ (但 JSON 限制 NaN/Infinity) |
| `String` | `string` | 字符串 | ✅ |
| `DataList` | `DataList` | 动态数组(可嵌套) | ✅ |
| `DataDictionary` | `DataDictionary` | 键值对(可嵌套) | ✅ |
| `Object Reference` | `object` | **任意** C# 对象(通过装箱) | ❌ **不可序列化** |
| `DataError` | `DataError` enum | 错误信息 | ❌ (仅作为返回值) |

> **【官方】** JSON 序列化时,数字会被规范化为 `Double`。反序列化后所有数字都是 `Double`,即使原来是 `int`/`byte`/`float`。

### 1.2 TokenType 枚举顺序(用于比较与排序)

```csharp
Null < Number < String < DataList < DataDictionary < Reference
```

> **【官方】** `DataList.Sort()` 在混合类型场景下,按 TokenType 枚举顺序排序。`CompareTo()` 也遵循相同规则。

---

## 2. DataToken Properties(属性)

> **【官方】** 以下属性用于从 DataToken 中**提取**值。访问错误的类型会**抛异常并 halt UdonBehaviour**。

### 2.1 类型查询属性(安全,无异常)

| 属性 | 返回 | 说明 |
|------|------|------|
| `TokenType` | `TokenType` | **精确**类型(用于 switch/if) |
| `IsNumber` | `bool` | 任何数字类型都返回 `true` |
| `IsNull` | `bool` | Null/已销毁对象/为空字符串/`Utilities.IsValid == false` 都视为 null |

### 2.2 值提取属性(类型不匹配会抛异常)

| 属性 | 返回类型 | 自动提升规则 |
|------|---------|-------------|
| `Boolean` | `bool` | 仅 bool |
| `Number` | `double` | **任何**数字类型(double upcast) |
| `SByte` | `sbyte` | 仅 sbyte |
| `Byte` | `byte` | 仅 byte |
| `Short` | `short` | `short` / `sbyte` / `byte` |
| `UShort` | `ushort` | `ushort` / `byte` |
| `Int` | `int` | `int` / `sbyte` / `byte` / `short` / `ushort` |
| `UInt` | `uint` | `uint` / `byte` / `ushort` |
| `Long` | `long` | `long` / `sbyte` / `byte` / `short` / `ushort` / `uint` |
| `ULong` | `ulong` | `ulong` / `byte` / `ushort` / `uint` |
| `Float` | `float` | 任何数字类型 |
| `Double` | `double` | **任何**数字类型(同上) |
| `String` | `string` | 仅 string |
| `DataDictionary` | `DataDictionary` | 仅 DataDictionary |
| `DataList` | `DataList` | 仅 DataList |
| `Reference` | `object` | 仅 Reference(任意装箱对象) |
| `Error` | `DataError` | **永不抛异常**;非 Error token 返回 `DataError.None` |

> ⚠️ **【官方】** `Error` 属性是**唯一**永不抛异常的提取属性。这是错误处理的关键。

---

## 3. DataToken Functions(方法)

| 方法 | 用途 | 关键点 |
|------|------|--------|
| `Bitcast(TokenType)` | 值保留型类型转换 | 同字节宽度,位模式不变,返回**副本** |
| `ToString()` | 通用字符串化 | **永不抛异常**;适合 Debug.Log |
| `GetHashCode()` | 哈希(用于字典键) | 容器内部使用 |
| `CompareTo(DataToken)` | 大小比较 | -1 / 0 / 1;混合类型按 TokenType 顺序 |

> **【官方】** `Bitcast` 是值保留型,类似 C++ `reinterpret_cast` 或 C# `BitConverter`。**详见 [`./byte-and-bit-operations.md`](./byte-and-bit-operations.md) §1**。

---

## 4. 创建 DataToken

### 4.1 UdonSharp:隐式创建(推荐)

```csharp
using UdonSharp;
using VRC.SDK3.Data;
using UnityEngine;

public class DataTokenCreation : UdonSharpBehaviour
{
    void Start()
    {
        // ❌ 显式 new 较繁琐
        DataToken _explicitFloat = new DataToken(5.3f);
        DataToken _explicitInt = new DataToken(5);
        DataToken _explicitString = new DataToken("value");
        DataToken _explicitBool = new DataToken(true);

        // ✅ 隐式装箱(推荐):UdonSharp 自动创建 DataToken
        DataToken _float = 5.3f;
        DataToken _int = 5;
        DataToken _string = "value";
        DataToken _bool = true;

        // 数组 → DataList(隐式)
        DataList list = new int[] { 1, 2, 3 };  // 【待官方文档确认】隐式行为

        // 字典 → DataDictionary(隐式)
        DataDictionary dict = new DataDictionary { { "key", "value" } };
    }
}
```

> 🔴 **【官方】** **不要**使用 `nameof()` 隐式创建 DataToken,会导致错误。

### 4.2 Udon Graph

- 使用 **DataToken Implicit** 节点(隐式装箱)
- 或使用 **DataToken Constructor** 节点(显式)

### 4.3 隐式 vs 显式 选择

| 场景 | 推荐方式 |
|------|---------|
| 容器赋值 (`dict["k"] = 5;`) | 隐式自动 |
| 局部变量声明 | 隐式 `DataToken t = 5;` |
| 显式强调类型 | 显式 `new DataToken(value)` |
| 复杂表达式 | 隐式(更简洁) |

---

## 5. 从 DataToken 提取值(3 种方式)

### 5.1 方式 1:`TokenType` 检查 + 直接取值(最灵活)

```csharp
DataToken unknownToken = /* 来自外部源 */;

if (unknownToken.TokenType == TokenType.String)
{
    Debug.Log(unknownToken.String);  // ✅ 安全
}
else if (unknownToken.IsNumber)
{
    Debug.Log(unknownToken.Number);  // ✅ double,可能丢精度(long/ulong)
}
```

### 5.2 方式 2:`IsNumber` 检查(数字通用)

```csharp
// 不知道具体是 int/float/double?用 IsNumber + Number
if (unknownToken.IsNumber)
{
    double d = unknownToken.Number;  // 任何数字类型都拿到 double
    Debug.Log(d);
}
```

> ⚠️ **【官方】** `Number` 拿到的是 `double`。如果原 token 是 `long` 或 `ulong`,可能**丢失精度**。

### 5.3 方式 3:`TryGetValue(key, TokenType, out)`(容器访问)

容器(DataList/DataDictionary)内置类型检查版取值:

```csharp
DataDictionary dict = /* ... */;
if (dict.TryGetValue("playerName", TokenType.String, out DataToken value))
{
    Debug.Log(value.String);
}
// else 时,value 是 DataError
```

> **【官方】** 类型不匹配时返回 `false`,且 `value` token 包含 `DataError.TypeMismatch`。

### 5.4 方式 4:简写方括号(仅在**完全受控**时使用)

```csharp
// 受控环境:类型已知且保证存在
DataDictionary dict = new DataDictionary();
dict["A"] = 5;
dict["B"] = 10;

// 直接访问——不安全!若 key 不存在或类型不对,会 halt
int sum = dict["A"].Int + dict["B"].Int;
```

> 🔴 **【官方】** 简写方括号**不安全**。仅在你**完全控制**数据(自己写入且类型已知)时使用。**外部数据必须用 `TryGetValue`**。

---

## 6. 嵌套 DataToken(任意深度)

DataToken **可以包含** DataList/DataDictionary,后者又包含 DataToken——形成**任意深度**的嵌套树:

```csharp
DataList outer = new DataList();
DataList inner = new DataList();
inner.Add(1);
inner.Add(2);
inner.Add(3);

outer.Add(inner);  // DataList 嵌套 DataList → 二维数组效果

// 三维嵌套
DataList depth3 = new DataList();
DataDictionary dict2d = new DataDictionary();
dict2d.Set("inner", inner);
depth3.Add(dict2d);
outer.Add(depth3);
```

### 6.1 访问嵌套值

```csharp
// 用 TryGetValue 逐层访问
if (outer.TryGetValue(0, out DataToken t1))
{
    if (t1.TokenType == TokenType.DataList)
    {
        DataList innerList = t1.DataList;
        if (innerList.TryGetValue(0, TokenType.Int, out DataToken t2))
        {
            int value = t2.Int;  // = 1
            Debug.Log(value);
        }
    }
}
```

### 6.2 嵌套深度建议

> **【推断】** Udon VM 没有递归调用栈大小限制,但**嵌套过深**会显著影响性能(每次访问需多次 EXTERN 调用 + 类型检查)。
>
> **最佳实践**:嵌套深度 ≤ 5 层,UI/配置数据 ≤ 3 层。

---

## 7. DataError 详解

当容器操作失败,会返回**包含 DataError 的 token**,而非抛异常。

### 7.1 DataError 枚举(完整)

| DataError | 触发场景 |
|-----------|---------|
| `None` | 无错误(成功) |
| `KeyDoesNotExist` | DataDictionary 中 key 不存在 |
| `IndexOutOfRange` | DataList 索引越界(`< 0` 或 `>= Count`) |
| `TypeMismatch` | 类型不匹配(仅 `TryGetValue` 显式指定 TokenType 时) |
| `TypeUnsupported` | 容器含 Reference Token,无法序列化 |
| `ValueUnsupported` | 含 NaN/Infinity,无法 JSON 序列化 |
| `UnableToParse` | JSON 格式无效 |

### 7.2 检查错误

```csharp
DataToken result = /* TryGetValue/Serialize 失败时的 token */;

if (result.Error != DataError.None)
{
    Debug.LogError(result.ToString());
    // ToString() 会自动组合 enum + 详细信息字符串
}
```

> **【官方】** DataError token 同时包含**枚举**和**详细字符串**。`ToString()` 会自动组合为完整消息,适合 `Debug.Log(token)`。

### 7.3 TryGetValue 错误处理模式

```csharp
if (dict.TryGetValue("key", TokenType.Float, out DataToken token))
{
    // 成功,使用 token.Float
    float value = token.Float;
}
else
{
    // 失败,token 包含 DataError
    Debug.LogError($"Failed: {token}");  // 打印 "TypeMismatch: ..."
}
```

---

## 8. `String` vs `ToString()` 关键区别

> **【官方 FAQ】** 这是初学者**最常混淆**的问题。

| 调用 | 适用场景 | 类型不匹配行为 |
|------|---------|--------------|
| `token.String` | 提取**字符串值** | **抛异常** + halt |
| `token.ToString()` | **转换任意**为字符串 | **永不抛异常** |

### 8.1 示例对比

```csharp
DataToken stringToken = "hello";
DataToken floatToken = 3.14f;

string s1 = stringToken.String;   // ✅ "hello"
string s2 = floatToken.String;    // ❌ 抛 InvalidCastException,UdonBehaviour 停止

string s3 = stringToken.ToString(); // ✅ "hello"
string s4 = floatToken.ToString();  // ✅ "3.14"(用 InvariantCulture)
```

### 8.2 实用建议

- `Debug.Log(token)` → 自动调用 `ToString()`,**安全**
- `Debug.Log(token.String)` → **危险**,先检查 `TokenType == String`
- DataError 始终用 `token.ToString()`(组合 enum + 消息)

---

## 9. 与 C# `object` 的区别

| 维度 | C# `object` | Udon `DataToken` |
|------|------------|-------------------|
| 装箱/拆箱 | 隐式(IL 层面) | **显式**(VM 层面有 EXTERN 调用) |
| 类型擦除 | 编译时类型擦除,运行时反射 | **运行时类型擦除**,无反射 |
| 性能 | 接近原生(GC 压力) | **比直接类型慢 5-10 倍**(【推断】VM EXTERN 开销) |
| 序列化 | 需自定义 | 自动支持(VRCJson) |
| 嵌套 | 任意 C# 对象 | 仅 DataList/DataDictionary/Reference |

### 9.1 性能含义

> **【推断】** DataToken 的隐式装箱每次都是**多次 VM 指令**(PUSH + EXTERN)。在 `Update()` 循环中大量装箱会显著影响性能。
>
> **最佳实践**:
> - 高频循环(每帧)用**强类型原生数组**(`int[]` / `float[]`)
> - 容器化数据用 DataToken(仅在需要时)
> - 避免在 `Update` 中反复 `DataList.Add()` → 考虑预分配

---

## 10. 典型应用场景

### 10.1 JSON 反序列化的安全访问

```csharp
if (VRCJson.TryDeserializeFromJson(jsonString, out DataToken result))
{
    // 【外部数据】必须类型检查
    if (result.IsNumber)
    {
        double d = result.Number;
        Debug.Log($"Got number: {d}");
    }
    else if (result.TokenType == TokenType.String)
    {
        Debug.Log($"Got string: {result.String}");
    }
}
```

### 10.2 配置系统的默认值

```csharp
DataDictionary config = LoadConfig();
float volume = 1.0f;  // 默认值
if (config.TryGetValue("volume", TokenType.Float, out DataToken tok))
{
    volume = tok.Float;
}
```

### 10.3 跨类型数值运算

```csharp
DataToken a = 5;       // Int
DataToken b = 5.5f;    // Float
DataToken c = 5.5;     // Double

// 混合数值:用 Number (double) 统一
double sum = a.Number + b.Number + c.Number;
```

---

## 11. 调试技巧

### 11.1 打印 token 信息

```csharp
// 安全的字符串化(不抛异常)
Debug.Log($"Token: {token}");

// 详细类型信息
Debug.Log($"Type={token.TokenType}, IsNull={token.IsNull}, IsNumber={token.IsNumber}");

// 错误 token
if (token.Error != DataError.None)
{
    Debug.LogError($"Error token: {token.ToString()}");
}
```

### 11.2 二进制表示(位调试)

```csharp
DataToken intToken = 0x12345678;
DataToken floatToken = intToken.Bitcast(TokenType.Float);
Debug.Log($"Int 0x{intToken.Int:X8} as Float = {floatToken.Float}");

DataToken doubleToken = new DataToken(0.1d);
DataToken ulongToken = doubleToken.Bitcast(TokenType.ULong);
Debug.Log($"Double 0.1 as ULong = 0x{ulongToken.ULong:X16}");
```

> **【官方】** `Bitcast` 是**值保留型**类型转换(同字节宽度),位模式不变。详见 [`./byte-and-bit-operations.md`](./byte-and-bit-operations.md)。

---

## 12. 风险与注意事项

| 风险 | 说明 | 缓解 |
|------|------|------|
| **类型不匹配抛异常** | 直接 `.String` 访问 float token 会 halt | 用 `TokenType` 检查 / `TryGetValue` |
| **外部数据不安全** | JSON 反序列化数据无类型保证 | 必须 `TryGetValue` + `TokenType` |
| **装箱性能开销** | 每次隐式装箱 = 多次 VM 指令 | 高频场景用原生数组 |
| **嵌套过深** | JSON 嵌套 > 5 层性能急剧下降 | 限制嵌套深度 |
| **JSON 数字精度** | 数字统一为 Double,长整数会丢精度 | 关键 ID 用 String 存储 |
| **Reference 不可序列化** | 装箱的对象无法 `VRCJson` 序列化 | 仅用于临时数据 |
| **NaN/Infinity 不可序列化** | Float.NaN/PositiveInfinity 无法 JSON | 序列化前检查 |

### 12.1 反射支持

> **【官方 FAQ】** 为什么不实现 `TryGetValue<T>`(直接返回 C# 值)?
>
> - Udon VM **不支持**泛型(只有 UdonSharp 静态方法支持)
> - 泛型版会**隐藏 DataError**(返回默认值)
> - 当前 token 形式让错误显式可见
>
> **替代方案**:在 UdonSharp 中写**扩展方法**模拟 `TryGetValue<T>`(利用静态方法 + 泛型支持)。

---

## 13. 内部实现简述(【推断】)

> 以下基于 Udon VM 9 指令的推断,非官方说明。

- **DataToken** 在堆上是**结构体**(TokenType + 值)
- **装箱/拆箱** = `EXTERN` 调用包装 + `COPY` 指令复制
- **类型擦除** = 实际存储就是 `object` 引用,TokenType 字段标记类型
- **性能** = 每次操作 ~ 5-10 条 VM 指令(对比原生类型 ~ 1-2 条)

---

## 相关知识

- **父文档**: [`./index.md`](./index.md) — Data Containers 总览
- **位/字节操作**: [`./byte-and-bit-operations.md`](./byte-and-bit-operations.md) — Bitcast 等
- **DataList**: [`./data-lists.md`](./data-lists.md) — 容器 API
- **DataDictionary**: [`./data-dictionaries.md`](./data-dictionaries.md) — 容器 API
- **VRCJSON**: [`./vrcjson.md`](./vrcjson.md) — JSON 序列化
- **网络同步**: `memory/api/networking.md` — 容器同步模式
- **官方源**: https://creators.vrchat.com/worlds/udon/data-containers/data-tokens/
