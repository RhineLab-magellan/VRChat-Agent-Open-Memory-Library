---
title: 序列化类型清单
category: world
subcategory: udon/persistence
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - serialization
  - data-types
  - byte-array
aliases:
  - 序列化类型
  - 数据类型
  - 18 种类型
  - byte[] 编码
related:
  - ../../../api/persistence.md
  - ../index.md
  - player-data.md
  - player-object.md
  - limits-and-quirks.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/persistence/player-data/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# 序列化类型清单

> SDK Version: 3.7+
> 官方文档:https://creators.vrchat.com/worlds/udon/persistence/player-data/
> 主题:PlayerData 支持的 18 种原生类型 + byte[] 自定义序列化模式

---

## 概述

PlayerData 原生支持 **18 种数据类型**。如果你需要更复杂的数据结构(数组、嵌套对象、字典),**有两种方案**:
1. **多 key 拆分**(推荐简单场景)
2. **byte[] 自定义序列化**(推荐复杂场景,使用 `VRCJson` / `DataList` / `DataDictionary`)

> **警告**:PlayerData 不支持原生 `int[]` / `string[]` / `DataList` 等容器类型。**必须用 byte[] + VRCJson 自行序列化**。

---

## 18 种原生类型完整清单

### 整数家族(8 种)

| 类型 | C# 类型 | 字节数 | 范围 | 适用场景 |
|------|--------|-------|------|---------|
| sbyte | `System.SByte` | 1 | -128 ~ 127 | 小负数、字节状态 |
| byte | `System.Byte` | 1 | 0 ~ 255 | 位标志、ASCII 字符 |
| short | `System.Int16` | 2 | -32,768 ~ 32,767 | 中等范围 |
| ushort | `System.UInt16` | 2 | 0 ~ 65,535 | 中等无符号 |
| **int** | `System.Int32` | **4** | -2.1B ~ 2.1B | **最常用**(分数、数量) |
| uint | `System.UInt32` | 4 | 0 ~ 4.3B | 大无符号 |
| long | `System.Int64` | 8 | -9.2Q ~ 9.2Q | 超大整数、时间戳(ms) |
| ulong | `System.UInt64` | 8 | 0 ~ 18.4Q | 超大无符号 |

### 浮点(2 种)

| 类型 | C# 类型 | 字节数 | 精度 | 适用场景 |
|------|--------|-------|------|---------|
| **float** | `System.Single` | **4** | 7 位 | **最常用**(位置、速度) |
| double | `System.Double` | 8 | 15 位 | 高精度物理 |

### 向量 / 旋转 / 颜色(7 种)

| 类型 | 字节数 | 适用场景 |
|------|-------|---------|
| **Vector3** | 12 | 位置、速度、加速度 |
| Vector2 | 8 | 2D 坐标、UV |
| Vector4 | 16 | 切线、四元数分量 |
| **Quaternion** | 16 | 旋转 |
| Color | 16 | 颜色(RGBA float) |
| Color32 | 4 | 颜色(RGBA byte,适合 UI) |

### 基础类型(1 种)

| 类型 | 字节数 | 适用场景 |
|------|-------|---------|
| **bool** | 1 | 标志位 |
| **string** | 2N+overhead | 文本(50 字符建议上限) |

### 自定义(1 种)

| 类型 | 字节数 | 适用场景 |
|------|-------|---------|
| **byte[]** | N+overhead | 自定义序列化(JSON / 二进制) |

> **总计**:8 + 2 + 7 + 2 + 1 = **20 种**(含 string + byte[])。官方文档列出的 18 种不包含 string 和 byte[] 作为"原生类型"。

---

## 类型选择决策

```
需要存储什么?
├─ 单值 ── int(4B) / float(4B) / Vector3(12B) / Color32(4B) / bool(1B)
├─ 多值同质 ── 用 byte[] 存数组(JSON 或二进制)
├─ 多值异质 ── 用 byte[] 存 DataDictionary(JSON)
├─ 复杂对象 ── 用 byte[] 存 JSON 字符串
└─ 大量记录 ── 多 key 拆分 + 前缀命名
```

---

## 关键事实:Key 计数与配额

> 🔴 **每条 Set 操作都计入 100KB 配额**

| 操作 | 配额影响 |
|------|---------|
| `SetInt(player, "key", 0)` | ~4 bytes(值)+ key 名长度 |
| `SetString(player, "key", "hello")` | ~5 bytes(值)+ key 名长度 |
| `SetVector3(player, "key", Vector3.zero)` | ~12 bytes(值)+ key 名长度 |
| **整体** | **key 名 + 值的序列化字节数总和 ≤ 100KB** |

### 命名空间策略(必读)

```text
推荐:  <Prefab名>-<功能>-<子项>
避免:  短通用名(score/level/health)

示例:
- IdleGame-Points              (主分数)
- IdleGame-Autoclicker-Count   (子项)
- PenSystem-Line-0-Color       (第 0 条线颜色)
- PenSystem-Line-0-Points      (第 0 条线点集 → byte[])

❌ 错误:score、level、color、x、y(易冲突)
```

---

## byte[] 自定义序列化模式

> **场景**:需要存数组、列表、字典、复杂对象

### 模式 1:VRCJson 存 DataDictionary(推荐)

```csharp
using VRC.SDK3.Persistence;
using VRC.SDK3.Data;

// 1. 构造复杂结构
DataDictionary dict = new DataDictionary();
dict["playerName"] = "Alice";
dict["level"] = 42;
dict["achievements"] = new DataList();
((DataList)dict["achievements"]).Add("first_kill");
((DataList)dict["achievements"]).Add("level_10");

// 2. 序列化为 JSON
string json = VRCJson.Serialize(dict);  // {"playerName":"Alice","level":42,...}

// 3. 转为 byte[]
byte[] bytes = System.Text.Encoding.UTF8.GetBytes(json);

// 4. 存入 PlayerData
PlayerData.SetBytes(Networking.LocalPlayer, "RPG-Save-Data", bytes);

// 5. 读取
PlayerData.TryGetBytes(Networking.LocalPlayer, "RPG-Save-Data", out byte[] saved);
if (saved != null) {
    string loadedJson = System.Text.Encoding.UTF8.GetString(saved);
    VRCJson.TryDeserialize(loadedJson, out DataToken result);
    if (result.Type == DataToken.DataType.Dictionary) {
        DataDictionary loaded = (DataDictionary)result.Data;
        // 重新构造对象
    }
}
```

### 模式 2:二进制自定义编码(更紧凑)

```csharp
// 1. 编码多个 int 为 byte[](4 字节/个,小端序)
public static byte[] EncodeInts(int[] values) {
    byte[] result = new byte[values.Length * 4];
    for (int i = 0; i < values.Length; i++) {
        byte[] intBytes = System.BitConverter.GetBytes(values[i]);
        System.Array.Copy(intBytes, 0, result, i * 4, 4);
    }
    return result;
}

// 2. 解码
public static int[] DecodeInts(byte[] bytes) {
    int count = bytes.Length / 4;
    int[] result = new int[count];
    for (int i = 0; i < count; i++) {
        result[i] = System.BitConverter.ToInt32(bytes, i * 4);
    }
    return result;
}

// 3. 配合 PlayerData 存
int[] scores = new int[] { 100, 200, 300 };
byte[] encoded = EncodeInts(scores);
PlayerData.SetBytes(Networking.LocalPlayer, "HighScores", encoded);
```

### 模式 3:多 key 拆分(简单场景)

```csharp
// 10 个成就 → 10 个 bool key(易读、易调试)
for (int i = 0; i < 10; i++) {
    string key = $"Unlocks-Achievement-{i}";
    bool unlocked = ComputeAchievement(i);
    PlayerData.SetBool(Networking.LocalPlayer, key, unlocked);
}

// 读取所有成就
bool[] achievements = new bool[10];
for (int i = 0; i < 10; i++) {
    if (PlayerData.TryGetBool(Networking.LocalPlayer, $"Unlocks-Achievement-{i}", out bool val)) {
        achievements[i] = val;
    } else {
        achievements[i] = false;
    }
}
```

---

## String 长度限制详解

| 限制 | 数值 | 来源 |
|------|------|------|
| **建议 String 值** | ~50 字符 | 官方建议 |
| 实际硬限制 | 由 100KB 配额决定 | 大量短字符串会迅速耗尽配额 |
| 编码 | UTF-8 | 标准 |
| Key 名长度 | 128 字符(建议) | 官方建议 |

### String 容量估算

```
100KB 配额 / 平均 50 字符/字符串(UTF-8 = 50 bytes)
= 100,000 / 50 = 2,000 个字符串(理论上限)

实际:留 50% 余量,推荐 < 1,000 个字符串
```

---

## 跨玩家类型变化

> 🔴 **同 key 可以从 int 改为 string**,但旧值 **不会** 自动转换

```csharp
// 第一次写
PlayerData.SetInt(player, "score", 42);  // 存为 int

// 第二次写(同 key)
PlayerData.SetString(player, "score", "forty-two");  // 覆盖为 string

// 读取用 GetInt 会怎样? → 返回 0(default),不报错
// 读取用 GetString → 正常返回 "forty-two"
```

**最佳实践**:每个 key 的类型在整个 World 生命周期内 **保持一致**。

---

## 嵌套 DataToken 模式(高级)

```csharp
// 嵌套对象 + 数组
DataDictionary saveData = new DataDictionary();
saveData["playerInfo"] = new DataDictionary();
((DataDictionary)saveData["playerInfo"])["name"] = "Alice";
((DataDictionary)saveData["playerInfo"])["level"] = 99;

saveData["inventory"] = new DataList();
((DataList)saveData["inventory"]).Add("sword");
((DataList)saveData["inventory"]).Add("shield");
((DataList)saveData["inventory"]).Add("potion");

// 整个序列化为 1 个 byte[]
string json = VRCJson.Serialize(saveData);
byte[] bytes = System.Text.Encoding.UTF8.GetBytes(json);
PlayerData.SetBytes(player, "Game-Save", bytes);
```

> **数据大小**:JSON 字符串约 1.2-1.5x 原始数据大小,压缩后接近原大小。

---

## 类型大小对比表(优化参考)

| 类型 | 字节 | 100KB 可存数量 | 适用场景 |
|------|------|--------------|---------|
| bool | 1 | ~100,000 | 标志位集合 |
| byte | 1 | ~100,000 | 状态枚举 |
| int | 4 | ~25,000 | 计数 |
| float | 4 | ~25,000 | 测量值 |
| Color32 | 4 | ~25,000 | 颜色 |
| Vector3 | 12 | ~8,300 | 3D 位置 |
| Quaternion | 16 | ~6,250 | 旋转 |
| string(50字符) | ~50 | ~2,000 | 玩家名字 |
| byte[] | N+overhead | - | 自定义数据 |

---

## 4 个常见陷阱

| 陷阱 | 症状 | 修复 |
|------|------|------|
| 用 `int[]` 存数组 | 编译失败/静默失败 | 用 byte[] + VRCJson |
| `Get*` 在 key 不存在时返回默认值 | 0 误判为"已解锁" | 用 `TryGet*` 区分 |
| 大量短字符串 | 字符串头开销大,快速耗尽配额 | 合并为 byte[] + JSON |
| 类型中途变更(int → string) | 旧数据无法访问 | 类型保持一致 |

---

## 与 PlayerObject 序列化对比

| 维度 | PlayerData | PlayerObject `[UdonSynced]` |
|------|-----------|----------------------------|
| 原生支持类型 | 18 种(含 byte[]) | Udon 暴露类型(更多) |
| 数组 | ❌(需 byte[] 包装) | ✅(int[]/string[]/Vector3[]) |
| DataList/DataDictionary | ❌(需 byte[] 包装) | ✅(直接 UdonSynced) |
| 序列化开销 | 写一次 = 发全部 | 单独同步 |
| Late Joiner | 自动恢复 | 自动恢复 |

> **结论**:如果你需要存数组或 DataList,PlayerObject 天然更省事;PlayerData 需用 byte[] + VRCJson。

---

## 相关知识库

- `memory/api/persistence.md` - API 速查
- `memory/world/udon/data-containers/` - VRCJson / DataList / DataDictionary 详解
- `memory/world/udon/networking/variables.md` - UdonSynced 字段类型
- `memory/world/examples/persistence/playerdata-types.md` - 18 种类型演示示例
