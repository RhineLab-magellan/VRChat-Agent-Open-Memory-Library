# Byte and Bit Operations

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/udon/data-containers/byte-and-bit-operations)
> 最后官方更新: 2024-07-31
> 本地化日期: 2026-06-15
> Type: REFERENCE + PATTERN
> Confidence: High
> SDK: 3.5.0+
> 状态: ✅ FACT (官方) + 扩展 (位运算/位域压缩)

> **重要提示**: 本页面讲解的是**底层二进制数据操作**概念,面向**高级创作者**。
>
> 三个核心工具:
> 1. **`DataToken.Bitcast()`** —— DataToken 上的"不安全转型" / 值保留型类型转换
> 2. **`System.BitConverter`** —— C# 标准类,基本类型 ↔ `byte[]`
> 3. **`System.Buffer`** —— C# 标准类,数组间高速内存块复制
>
> 配套必读:位域压缩同步模式 → `memory/patterns/bit-packed-flags.md`

---

## 1. DataToken.Bitcast (值保留转型)

`Bitcast` 是 DataToken 上的**值保留转型** ("unsafe cast"),允许把一个基本类型的位重新解释为另一个类型,**不改变位模式**。**在 Udon 中这是进行位级访问的关键方法**。

### 1.1 典型用途

| 转换 | 场景 | 大小 |
|------|------|------|
| `Double` → `ULong` | 把浮点数的位当 8 字节整数访问 | 8 字节 |
| `Float` → `UInt` | 把单精度浮点的位当 4 字节无符号整数访问 | 4 字节 |
| `Int` → `Float` | (注意)位模式会变,值不保留(不推荐) | 4 字节 |
| `ULong` → `Double` | 反向转换,恢复原浮点数 | 8 字节 |

### 1.2 基本用法

```csharp
using UdonSharp;
using VRC.SDK3.Data;
using UnityEngine;

public class BitcastExample : UdonSharpBehaviour
{
    void Start()
    {
        double doubleValue = 123.456d;
        DataToken doubleToken = new DataToken(doubleValue);

        // Double → ULong(同 8 字节,值保留)
        DataToken ulongToken = doubleToken.Bitcast(TokenType.ULong);

        // ULong → Double(恢复原值)
        DataToken resultDoubleToken = ulongToken.Bitcast(TokenType.Double);

        Debug.Log($"{doubleToken} - 0x{ulongToken:02X} - {resultDoubleToken}");
    }
}
```

### 1.3 关键规则

| 规则 | 说明 |
|------|------|
| **同字节宽度** | 必须使用**相同字节宽度**的类型对(如 Double↔ULong=8 字节,Float↔UInt=4 字节) |
| **位模式保留** | 不改变位,只重新解释为新类型 |
| **支持类型** | `Boolean/Byte/SByte/Short/UShort/Int/UInt/Long/ULong/Float/Double` |
| **不支持数组/字符串** | 只能对标量基本类型 Bitcast |

> **【推断】** 在 Udon VM 层面,Bitcast 是零成本操作(仅重新标记堆中数据的 TokenType),适合用于调试、压缩编码、位运算等场景。

---

## 2. System.BitConverter (基本类型 ↔ byte[])

`BitConverter` 是 C# 标准类,**在 Udon 中已暴露**,用于把基本类型转换为 `byte[]` 或反向解码。**主要用于持久化数据压缩、自定义序列化协议**。

### 2.1 支持的方法 (Udon 已暴露)

| 方法 | 用途 | 输出大小 |
|------|------|----------|
| `BitConverter.GetBytes(int)` | int → byte[] | 4 字节 |
| `BitConverter.GetBytes(float)` | float → byte[] | 4 字节 |
| `BitConverter.GetBytes(double)` | double → byte[] | 8 字节 |
| `BitConverter.GetBytes(long)` | long → byte[] | 8 字节 |
| `BitConverter.GetBytes(short)` | short → byte[] | 2 字节 |
| `BitConverter.GetBytes(bool)` | bool → byte[] | 1 字节 |
| `BitConverter.ToInt32(byte[], int)` | byte[] → int | 4 字节 |
| `BitConverter.ToSingle(byte[], int)` | byte[] → float | 4 字节 |
| `BitConverter.ToDouble(byte[], int)` | byte[] → double | 8 字节 |
| `BitConverter.ToInt64(byte[], int)` | byte[] → long | 8 字节 |
| `BitConverter.ToInt16(byte[], int)` | byte[] → short | 2 字节 |
| `BitConverter.ToBoolean(byte[], int)` | byte[] → bool | 1 字节 |

### 2.2 平台字节序警告

> ⚠️ **【官方】** BitConverter 的字节序**取决于运行平台**。在 VRChat Client(Unity Mono/.NET)上**是小端序 (Little-Endian)**,但跨平台持久化时**不保证一致性**。
>
> **最佳实践**:持久化前手动指定字节序,或使用 `IsLittleEndian` 检测。

```csharp
// 字节序检测
if (BitConverter.IsLittleEndian)
{
    // 当前平台是小端序
}
```

### 2.3 完整示例 (官方 Basic Serializer)

```csharp
using System;
using System.Text;
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;

public class BitConverterExample : UdonSharpBehaviour
{
    void Start()
    {
        // 测试数据
        int originalInt = 63;
        double originalDouble = 734531.433d;
        string originalString = "Test string";
        float[] originalFloatArray = new float[] { 543, 12.6f, 63.1231f };

        // 序列化 → 反序列化
        byte[] serialized = Serialize(originalInt, originalDouble, originalString, originalFloatArray);
        Deserialize(serialized, out int newInt, out double newDouble, out string newString, out float[] newFloatArray);

        // 验证
        Debug.Log($"{originalInt} - {newInt}");
        Debug.Log($"{originalDouble} - {newDouble}");
        Debug.Log($"{originalString} - {newString}");
        Debug.Log($"{originalFloatArray.Length} - {newFloatArray.Length}");
        for (int i = 0; i < originalFloatArray.Length && i < newFloatArray.Length; i++)
        {
            Debug.Log($"{originalFloatArray[i]} - {newFloatArray[i]}");
        }
    }

    byte[] Serialize(int intValue, double doubleValue, string stringValue, float[] floatArrayValues)
    {
        int size = 0;
        byte[] intBytes = BitConverter.GetBytes(intValue);
        size += intBytes.Length;  // 4 bytes

        byte[] doubleBytes = BitConverter.GetBytes(doubleValue);
        size += doubleBytes.Length;  // 8 bytes

        byte[] stringBytes = Encoding.UTF8.GetBytes(stringValue);
        size += stringBytes.Length;  // variable

        byte[] stringLengthBytes = BitConverter.GetBytes(stringBytes.Length);
        size += stringLengthBytes.Length;  // 4 bytes

        byte[] floatArrayLengthBytes = BitConverter.GetBytes(Buffer.ByteLength(floatArrayValues));
        size += floatArrayLengthBytes.Length;  // 4 bytes

        size += Buffer.ByteLength(floatArrayValues);  // floatArray.Length * 4

        byte[] output = new byte[size];
        int offset = 0;

        // 写入 int
        Buffer.BlockCopy(intBytes, 0, output, offset, intBytes.Length);
        offset += intBytes.Length;

        // 写入 double
        Buffer.BlockCopy(doubleBytes, 0, output, offset, doubleBytes.Length);
        offset += doubleBytes.Length;

        // 写入 string length
        Buffer.BlockCopy(stringLengthBytes, 0, output, offset, stringLengthBytes.Length);
        offset += stringLengthBytes.Length;

        // 写入 string bytes
        Buffer.BlockCopy(stringBytes, 0, output, offset, stringBytes.Length);
        offset += stringBytes.Length;

        // 写入 float[] length
        Buffer.BlockCopy(floatArrayLengthBytes, 0, output, offset, floatArrayLengthBytes.Length);
        offset += floatArrayLengthBytes.Length;

        // 写入 float[] (直接 BlockCopy,无需 GetBytes 转换)
        Buffer.BlockCopy(floatArrayValues, 0, output, offset, Buffer.ByteLength(floatArrayValues));
        offset += Buffer.ByteLength(floatArrayValues);

        Debug.Log($"Encoded data in {output.Length} bytes");
        return output;
    }

    bool Deserialize(byte[] input, out int intValue, out double doubleValue, out string stringValue, out float[] floatArrayValues)
    {
        int offset = 0;

        intValue = BitConverter.ToInt32(input, offset);
        offset += 4;

        doubleValue = BitConverter.ToDouble(input, offset);
        offset += 8;

        int stringLength = BitConverter.ToInt32(input, offset);
        offset += 4;

        stringValue = Encoding.UTF8.GetString(input, offset, stringLength);
        offset += stringLength;

        int floatArrayByteLength = BitConverter.ToInt32(input, offset);
        offset += 4;

        floatArrayValues = new float[floatArrayByteLength / 4];
        Buffer.BlockCopy(input, offset, floatArrayValues, 0, floatArrayByteLength);

        return true;
    }
}
```

---

## 3. System.Buffer (高速数组块复制)

`Buffer.BlockCopy` 在 Udon 中已暴露,用于在数组间**高速复制内存块**,**比逐元素循环快数倍**。特别适合将 `float[]` / `int[]` 直接复制到 `byte[]`(无需类型转换)。

### 3.1 关键 API

| 方法 | 用途 | 备注 |
|------|------|------|
| `Buffer.BlockCopy(src, srcOffset, dst, dstOffset, count)` | 内存块复制 | **count 以字节为单位** |
| `Buffer.ByteLength(array)` | 获取数组字节长度 | `int[].Length * 4`,`float[].Length * 4` |

### 3.2 数组 ↔ 字节对应关系

| 数组类型 | 单元素字节数 | 示例 |
|----------|-------------|------|
| `byte[]` | 1 | `new byte[10]` → 10 字节 |
| `short[]` / `ushort[]` | 2 | `new short[10]` → 20 字节 |
| `int[]` / `uint[]` / `float[]` | 4 | `new int[10]` → 40 字节 |
| `long[]` / `ulong[]` / `double[]` | 8 | `new double[10]` → 80 字节 |
| `bool[]` | 1 | `new bool[10]` → 10 字节 |

### 3.3 典型用法

```csharp
// float[] → byte[] (零成本内存块复制)
byte[] output = new byte[Buffer.ByteLength(floatArray)];
Buffer.BlockCopy(floatArray, 0, output, 0, Buffer.ByteLength(floatArray));

// byte[] → float[] (零成本内存块恢复)
float[] restored = new float[byteArray.Length / 4];
Buffer.BlockCopy(byteArray, 0, restored, 0, byteArray.Length);
```

> **【推断】** Buffer.BlockCopy 在 Udon VM 层面映射为单条 EXTERN 调用 + 底层 memcpy,比 C# 逐元素循环快 5-10 倍。

---

## 4. 位运算 (Bitwise Operations) 【扩展内容】

> ⚠️ **【扩展】** 官方文档未明确列出位运算符,以下基于 C# 标准 + UdonSharp 编译验证。

UdonSharp **完整支持 C# 位运算符**,这是位域压缩同步模式 (`memory/patterns/bit-packed-flags.md`) 的基础。

### 4.1 支持的位运算符

| 运算符 | 名称 | 示例 | 说明 |
|--------|------|------|------|
| `&` | 按位与 | `a & b` | 同时为 1 才为 1 (掩码提取) |
| `\|` | 按位或 | `a \| b` | 任一为 1 即为 1 (置位) |
| `^` | 按位异或 | `a ^ b` | 不同为 1,相同为 0 (翻转) |
| `~` | 按位取反 | `~a` | 0↔1 互换 (清除位) |
| `<<` | 左移 | `a << n` | 乘以 2^n (创建位标志) |
| `>>` | 右移 | `a >> n` | 除以 2^n (提取位) |

### 4.2 完整位运算模式

```csharp
// 1. 定义位标志常量
const byte FLAG_RUNNING  = 1 << 0;  // 0b00000001 = 1
const byte FLAG_CROUCHED = 1 << 1;  // 0b00000010 = 2
const byte FLAG_FLYING   = 1 << 2;  // 0b00000100 = 4
const byte FLAG_INVIS    = 1 << 3;  // 0b00001000 = 8
const byte FLAG_MUTED    = 1 << 4;  // 0b00010000 = 16
const byte FLAG_FROZEN   = 1 << 5;  // 0b00100000 = 32
const byte FLAG_GODMODE  = 1 << 6;  // 0b01000000 = 64
const byte FLAG_AFK      = 1 << 7;  // 0b10000000 = 128

[UdonSynced] private byte _playerFlags = 0;

// 2. 设置位 (Set / OR)
_playerFlags |= FLAG_RUNNING;
// 等价于: _playerFlags = _playerFlags | FLAG_RUNNING;

// 3. 清除位 (Clear / AND NOT)
_playerFlags &= ~FLAG_CROUCHED;
// 等价于: _playerFlags = _playerFlags & ~FLAG_CROUCHED;

// 4. 检查位 (Check)
if ((_playerFlags & FLAG_FLYING) == FLAG_FLYING) {
    // 玩家正在飞行
}
bool isRunning = (_playerFlags & FLAG_RUNNING) != 0;  // 简化写法

// 5. 翻转位 (Toggle / XOR)
_playerFlags ^= FLAG_MUTED;
// 当前是 1 → 变 0;当前是 0 → 变 1

// 6. 提取位 (Extract)
int bitValue = (_playerFlags >> 3) & 1;  // 提取第 3 位(0 或 1)
```

### 4.3 注释规范 (强制建议)

> **【规范】** 位运算**可读性差**,**必须**在每个常量定义处写明二进制布局:

```csharp
// ❌ 不推荐:无注释
const byte FLAG_A = 1 << 0;
const byte FLAG_B = 1 << 1;

// ✅ 推荐:标注位号 + 二进制
const byte FLAG_A = 1 << 0;  // bit 0: 玩家是否激活
const byte FLAG_B = 1 << 1;  // bit 1: 玩家是否无敌
const byte FLAG_C = 1 << 2;  // bit 2: 玩家是否静音
const byte FLAG_D = 1 << 3;  // bit 3: 玩家是否冻结
```

---

## 5. U# 类型转换规则 (int ↔ byte)

### 5.1 数值转换表

| 转换 | 是否支持 | 备注 |
|------|---------|------|
| `int` → `byte` | ✅ | **有溢出检查**,超出 0-255 抛 `OverflowException` |
| `byte` → `int` | ✅ | 安全,隐式扩展 |
| `int` → `sbyte` | ✅ | 有溢出检查 (-128~127) |
| `float` → `int` | ✅ | `(int)3.7f = 3`,**截断** (不四舍五入) |
| `int` → `float` | ✅ | 精度损失(> 2^24 时) |
| `int[]` → `byte[]` | ❌ | **需逐元素转换** |
| `byte` → `byte` (装箱) | ✅ | DataToken 隐式装箱 |

### 5.2 显式转换示例

```csharp
int value = 200;
byte b = (byte)value;  // ✅ OK (0-255 范围内)

int large = 300;
byte overflow = (byte)large;  // ❌ 抛 OverflowException

// 安全做法:先 mask 再转换
int safeInt = 300;
byte safeByte = (byte)(safeInt & 0xFF);  // = 44 (300 mod 256)

// 截断
float f = 3.7f;
int i = (int)f;  // = 3 (非四舍五入)

// 浮点转整型:有符号/无符号显式转换
float pi = 3.14f;
int truncated = (int)pi;          // 3
uint unsignedVal = (uint)pi;      // 3
```

### 5.3 checked / unchecked 上下文

```csharp
// checked: 显式溢出检查
byte result1 = checked((byte)300);  // ❌ 抛 OverflowException

// unchecked: 截断模式(位运算常见)
byte result2 = unchecked((byte)300);  // = 44 (300 mod 256)
```

> **【推断】** Udon VM 在 UdonSharp 编译时,默认行为等同于 `unchecked` 上下文(类似 IL 的 `overflow` 标志关闭),但**建议显式标注**以提高可读性。

---

## 6. 压缩效果对比

### 6.1 序列化空间对比

| 方案 | 字段数 | 序列化大小 | 节省 |
|------|--------|------------|------|
| 8 个独立 `[UdonSynced] bool` | 8 | ~8-24 bytes (含 header) | 基准 |
| 1 个 `[UdonSynced] byte` (位标志) | 1 | 1 byte (+ header) | **~87.5%** |
| 1 个 `[UdonSynced] int` (位标志) | 1 | 4 bytes (+ header) | ~50% |
| 1 个 `[UdonSynced] short` (位标志) | 1 | 2 bytes (+ header) | ~75% |

> **【官方】** Manual sync 限制 ~280KB/serialization,Continuous sync ~200 bytes/serialization。
> 来源: `memory/api/networking.md`

### 6.2 何时用 byte vs int

| 标志数量 | 推荐类型 | 容量 |
|----------|---------|------|
| 1-8 | `byte` (8 位) | 8 个 bool |
| 9-16 | `short` (16 位) | 16 个 bool |
| 17-32 | `int` (32 位) | 32 个 bool |
| 33-64 | `long` 或 `int[2]` | 64 个 bool |
| >64 | `byte[]` + DataList | 不限 |

---

## 7. 典型应用场景

### 7.1 玩家状态

```csharp
[UdonSynced] private byte _playerFlags = 0;

// 状态组合:[飞行] + [隐身] + [管理员]
void SetPlayerMode(VRCPlayerApi player)
{
    _playerFlags |= FLAG_FLYING;
    _playerFlags |= FLAG_INVIS;
    RequestSerialization();
}

void ClearAdmin()
{
    _playerFlags &= ~FLAG_GODMODE;
    RequestSerialization();
}
```

### 7.2 物品槽位 (Inventory)

```csharp
[UdonSynced] private int _inventorySlots = 0;  // 32 个槽位

void ToggleSlot(int slotIndex)
{
    if (slotIndex < 0 || slotIndex >= 32) return;
    int mask = 1 << slotIndex;
    _inventorySlots ^= mask;  // 翻转槽位
    RequestSerialization();
}

bool IsSlotActive(int slotIndex)
{
    int mask = 1 << slotIndex;
    return (_inventorySlots & mask) != 0;
}
```

### 7.3 特性开关 (Feature Flags)

```csharp
[UdonSynced] private byte _featureFlags = 0;

void EnablePvP()
{
    _featureFlags |= 0b00000001;  // bit 0: PvP
    RequestSerialization();
}

void EnableVoiceChat()
{
    _featureFlags |= 0b00000010;  // bit 1: 语音
    RequestSerialization();
}
```

### 7.4 配合 FieldChangeCallback 自动刷新 UI

```csharp
[UdonSynced, FieldChangeCallback(nameof(Flags))]
private byte _flags = 0;

public byte Flags
{
    get => _flags;
    set
    {
        _flags = value;
        UpdateUI();  // 位变化时自动刷新
    }
}
```

---

## 8. 与音频同步系统的 _flags 案例对比

> **来源**: `memory/hybrid/audio-link.md` 位域压缩模式(参考工程)

```csharp
// 音频同步系统 _flags 案例
[UdonSynced] byte _flags = 0b10;  // bit0=playing, bit1=locked

private void CopyIntoFlags()
{
    _flags = 0;
    if (_syncOwnerPlaying) _flags |= 1;  // 设置 bit 0
    if (_syncLocked) _flags |= 2;        // 设置 bit 1
}
```

**对比表**:

| 维度 | 音频同步系统 _flags | 本文档模式 |
|------|---------------------|-----------|
| **类型** | `byte` (1 字节) | `byte` / `int` (按需) |
| **标志数** | 2 个 (playing + locked) | 任意 8/16/32 个 |
| **写入方式** | 全量重写 (`_flags = 0; ... \|=`) | 增量修改 (`\|=` / `&=~` / `^=`) |
| **读取方式** | 单 bit 检查 | 任意位提取 |
| **FieldChangeCallback** | 未使用 | 推荐使用 |
| **典型带宽** | 1 byte/serialization | 1-4 bytes/serialization |

**两种风格选择**:
- **全量重写** (音频同步系统风格): 适合"多个 bool 状态需要原子快照"的场景
- **增量修改** (bit-packed-flags 风格): 适合"独立 bool 可独立变化"的场景

---

## 9. 风险与注意事项

| 风险 | 说明 | 缓解 |
|------|------|------|
| **可读性差** | 位运算 `&`、`\|`、`~` 难以一眼看懂 | **强制注释** (位号 + 含义) |
| **溢出检查** | `int → byte` 大值会抛异常 | 用 `& 0xFF` 截断或 `unchecked` |
| **不必要压缩** | 位域压缩仅对 **`[UdonSynced]`** 有意义 | 本地变量**不需**压缩 |
| **同步粒度** | 修改任一位 = 重发整字段 | 高频独立变化场景考虑拆分 |
| **bool 数量上限** | 超过 32 个用 `int` 浪费 | 用 `int[]` 数组或多个 int |
| **【推断】VM 性能** | 位运算本身快速,但 32 bit + AND + OR 仍需多步 VM 指令 | 高频场景考虑 Native Plugin |

### 9.1 同步粒度权衡

**反模式**: 用 1 个 `int` 装 32 个 bool,但客户端**只关心 1 个** bit 的变化 —— 仍要等整个 int 同步。

**正确做法**:
- 关联 bool(总是一起变) → 打包为 1 个 int
- 独立 bool(可能 5s 变 1 个) → 各自独立 `[UdonSynced]`

### 9.2 与 bool[] 数组的对比

| 维度 | 位标志 (1 个 int) | bool[] 数组 |
|------|-------------------|-------------|
| 同步方式 | 单字段同步 | **不能** 整体同步 |
| 写入粒度 | 1 bit | 1 元素 |
| 访问速度 | 极快 (单条 VM 指令) | 需数组索引 (多步) |
| 适用场景 | 1-32 个状态 | > 32 个状态 |

---

## 10. 与已有知识库关系

| 现有知识库 | 关联 |
|-----------|------|
| `memory/world/data-containers.md` | **父文档**:Data Containers 概述 |
| `memory/patterns/bit-packed-flags.md` | **核心模式**:位域压缩同步 (本任务是其底层原理) |
| `memory/hybrid/audio-link.md` | **案例**:音频同步系统 _flags 字段(参考工程) |
| `memory/api/networking.md` | **带宽限制** (~11KB/s, Manual 280KB) |
| `memory/api/not-exposed.md` | **白名单确认**:BitConverter/Buffer 已暴露 |

### 推荐阅读路径

```
位域压缩需求?
  ↓
看 memory/patterns/bit-packed-flags.md (使用模式)
  ↓
看本文档 (字节/位操作底层原理)
  ↓
看 memory/hybrid/audio-link.md (实际案例)
  ↓
看 memory/api/networking.md (带宽预算)
```

---

## 11. 完整工作代码示例

### 11.1 位标志工具类

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PlayerFlagManager : UdonSharpBehaviour
{
    // 位标志定义(bit 0-7)
    private const byte FLAG_ACTIVE   = 1 << 0;  // 玩家激活
    private const byte FLAG_FLYING   = 1 << 1;  // 飞行模式
    private const byte FLAG_INVIS    = 1 << 2;  // 隐身
    private const byte FLAG_MUTED    = 1 << 3;  // 静音
    private const byte FLAG_FROZEN   = 1 << 4;  // 冻结
    private const byte FLAG_GODMODE  = 1 << 5;  // 无敌
    private const byte FLAG_AFK      = 1 << 6;  // 离开
    private const byte FLAG_READY    = 1 << 7;  // 就绪

    [UdonSynced, FieldChangeCallback(nameof(Flags))]
    private byte _flags = 0;

    public byte Flags
    {
        get => _flags;
        set
        {
            _flags = value;
            OnFlagsChanged();
        }
    }

    // 公共 API:设置标志
    public void SetFlag(byte mask)
    {
        if (!Networking.IsOwner(gameObject))
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        _flags |= mask;
        RequestSerialization();
    }

    // 公共 API:清除标志
    public void ClearFlag(byte mask)
    {
        if (!Networking.IsOwner(gameObject))
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        _flags &= (byte)~mask;  // 显式 unchecked
        RequestSerialization();
    }

    // 公共 API:翻转标志
    public void ToggleFlag(byte mask)
    {
        if (!Networking.IsOwner(gameObject))
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        _flags ^= mask;
        RequestSerialization();
    }

    // 公共 API:检查标志
    public bool HasFlag(byte mask)
    {
        return (_flags & mask) == mask;
    }

    // 公共 API:计数(统计设置了几个标志)
    public int CountFlags()
    {
        byte v = _flags;
        int count = 0;
        while (v != 0)
        {
            count += v & 1;
            v >>= 1;
        }
        return count;
    }

    // 标志变化时自动刷新 UI
    private void OnFlagsChanged()
    {
        Debug.Log($"[Flags] Active={HasFlag(FLAG_ACTIVE)}, Flying={HasFlag(FLAG_FLYING)}");
        // TODO: 触发 UI 更新
    }

    // Interact 触发:切换飞行
    public override void Interact()
    {
        ToggleFlag(FLAG_FLYING);
    }
}
```

### 11.2 BitConverter + Buffer 序列化 (持久化示例)

```csharp
using System;
using System.Text;
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class CompactPlayerData : UdonSharpBehaviour
{
    // 32 个 bool 状态 → 4 个 byte
    [UdonSynced] private byte _flagsA = 0;  // bit 0-7
    [UdonSynced] private byte _flagsB = 0;  // bit 8-15
    [UdonSynced] private byte _flagsC = 0;  // bit 16-23
    [UdonSynced] private byte _flagsD = 0;  // bit 24-31

    // 把所有状态打包为 byte[] 用于持久化
    public byte[] PackToBytes()
    {
        return new byte[] { _flagsA, _flagsB, _flagsC, _flagsD };
    }

    // 从 byte[] 恢复
    public bool UnpackFromBytes(byte[] data)
    {
        if (data == null || data.Length < 4) return false;
        _flagsA = data[0];
        _flagsB = data[1];
        _flagsC = data[2];
        _flagsD = data[3];
        RequestSerialization();
        return true;
    }
}
```

### 11.3 DataToken.Bitcast 用法示例

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Data;

public class DataTokenBitcastExample : UdonSharpBehaviour
{
    void Start()
    {
        // 例 1:浮点数位模式调试
        float pi = 3.14159f;
        DataToken floatToken = new DataToken(pi);
        DataToken intToken = floatToken.Bitcast(TokenType.Int);
        Debug.Log($"Float {pi} 的位模式 = 0x{intToken.Int:X8}");

        // 例 2:用 ULong 存储 Double 进行精确位操作
        double d = 0.1d + 0.2d;  // = 0.30000000000000004
        DataToken dToken = new DataToken(d);
        DataToken lToken = dToken.Bitcast(TokenType.ULong);
        Debug.Log($"Double {d} 的位模式 = 0x{lToken.ULong:X16}");

        // 例 3:把 int 当 byte 数组访问
        int value = 0x12345678;
        DataToken vToken = new DataToken(value);
        DataToken floatToken2 = vToken.Bitcast(TokenType.Float);
        Debug.Log($"Int 0x{value:X8} 作为 float = {floatToken2.Float}");
    }
}
```

---

## 12. 调试技巧

### 12.1 位标志可视化

```csharp
// 打印 8 位二进制
void PrintFlags(byte flags)
{
    string binary = System.Convert.ToString(flags, 2).PadLeft(8, '0');
    Debug.Log($"Flags: 0b{binary}");
}

// 打印每个 bit 的状态
void PrintFlagDetails(byte flags)
{
    for (int i = 0; i < 8; i++)
    {
        bool isSet = (flags & (1 << i)) != 0;
        Debug.Log($"  bit {i}: {(isSet ? "1" : "0")}");
    }
}
```

### 12.2 序列化大小验证

```csharp
void CheckSerializationSize()
{
    int sizeBefore = 8;  // 假设 8 个独立 bool
    int sizeAfter = 1;   // 1 个 byte
    float saving = (1f - (float)sizeAfter / sizeBefore) * 100f;
    Debug.Log($"带宽节省: {saving:F1}%");
}
```

---

## 相关知识

- `memory/world/data-containers.md` — Data Containers 父文档
- `memory/patterns/bit-packed-flags.md` — 位域压缩同步模式 ⭐
- `memory/hybrid/audio-link.md` — 音频同步系统位域压缩案例(参考工程)
- `memory/api/networking.md` — 带宽限制 (~11KB/s, Manual 280KB)
- `memory/api/not-exposed.md` — 白名单黑名单
- `memory/api/udon-type-exposure.md` — Udon Type Exposure 索引
- 官方源: https://creators.vrchat.com/worlds/udon/data-containers/byte-and-bit-operations
