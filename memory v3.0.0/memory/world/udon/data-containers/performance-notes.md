---
title: DataList/DataDictionary 性能基准说明
category: world
subcategory: udon/data-containers

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - data-containers
  - data-list
  - data-dictionary
  - performance
  - benchmark
  - unverified

aliases:
  - DataList Performance
  - DataDictionary Performance
  - 性能基准
  - DataList 性能
  - DataDictionary 性能

related:
  - ./index.md
  - ./data-lists.md
  - ./data-dictionaries.md
  - ./data-tokens.md
  - ./vrcjson.md
  - ./byte-and-bit-operations.md
  - ../../../api/data-containers.md
  - ../../../patterns/bit-packed-flags.md
  - ../../../world/performance-guide.md

source: Udon VM 字节码分析 + VRChat 官方文档 + 第三方基准(社区)
source_type: community
version: 1.0
last_review: 2026-06-21
confidence: Medium
---

# DataList / DataDictionary 性能基准说明

> 🔴 **【未实测】** 本文档中所有数字均基于 **Udon VM 字节码分析 + 官方文档 + 第三方社区基准** 推断,**未经本环境 Unity 运行时实测验证**。
>
> 📋 **【需 Unity 实测验证】** 任何最终性能优化决策需在以下环境中实测:
> - Unity 2022.3.22f1
> - VRChat SDK 3.10.x(Worlds)
> - ClientSim(本地模拟)
> - 真实 VRChat Client(可选)
>
> 文档目的:为创作者和未来 Agent 提供**性能瓶颈方向**和**优化策略**,而非精确数字。

---

## 1. 为什么需要性能基准文档?

Udon VM 是受限的字节码沙箱,DataList / DataDictionary 这类"通用容器"在 Udon 中**有显著的性能开销**。但**本环境无 Unity**,无法实测,因此只能基于以下方法给出**推断**性能:

1. **Udon VM 字节码分析**:每个方法调用展开为多个 EXTERN 指令
2. **VRChat 官方文档**:API 复杂度标注(O(1) / O(n) / O(n²))
3. **第三方社区基准**:XANA 等社区的性能报告(需验证)
4. **DataToken 类型系统分析**:17 个 TokenType 引入 boxing / unboxing

**诚实声明**:本文档所有具体数字(如 5-10x 慢)都是**方向性估计**,**不应**作为最终优化决策的唯一依据。

---

## 2. 性能开销来源分析(VM 字节码层)

### 2.1 DataList 17 个 TokenType → 装箱/拆箱开销

**DataToken 的设计**:Udon 用 `DataToken`(类似 `object`)表示任意类型,内部是一个 8 字节结构体:

```
struct DataToken {
    TokenType type;   // 1 byte (类型标签:Int / Float / String / DataList / DataDictionary / ...)
    DataTokenStorage storage;  // 7 bytes (实际数据,小值内联,大值引用)
}
```

**TokenType 枚举**(17 个):

| 类别 | TokenType | 装箱/拆箱? |
|------|-----------|-----------|
| 数值 | `Int`, `Long`, `Float`, `Double` | 小值内联,**无装箱** |
| 文本 | `String` | 引用,无装箱 |
| 布尔 | `Boolean` | 1 字节内联 |
| 容器 | `DataList`, `DataDictionary` | 引用,无装箱 |
| 字节 | `Byte` | 1 字节内联 |
| 二进制 | `ByteArray` | 引用 |
| 特殊 | `Null`, `Error`, `None`, `Reference`, `Color`, `Vector*`, `Quaternion` | 引用 / 内联 |

**装箱开销场景**:
- `dict.SetValue("player", Networking.LocalPlayer)` → `VRCPlayerApi` 装箱为 `Reference` token
- `dict.GetValue<DataList>(...)` → 拆箱为 `DataList` 引用
- `dict.GetValue<int>(...)` → 拆箱为 `int` 值类型

### 2.2 EXTERN 调用开销

Udon 的 DataList / DataDictionary 方法**全部展开为 EXTERN 指令**,每个 EXTERN 包含:

```
EXTERN call:
  1. 参数推送(C# 端 stack)
  2. 跨 Udon→C# 边界调用(每次 ~5-10ns)
  3. 类型检查(TokenType 验证)
  4. 实际逻辑(动态分发)
  5. 返回值包装(DataToken 重建)
  6. 跨 C#→Udon 边界返回
```

**vs C# `List<T>`**:
- C# `List<int>.Add(int)` → JIT 编译为内联汇编,直接 push 数组,**1-2 ns**
- Udon `DataList.Add(int)` → EXTERN + TokenType 包装,**~50-100 ns**(推断)

### 2.3 强类型检测

每个方法内部需做 `TokenType` 验证:
- `Add(DataToken)` → 检查 token 类型(可选),写入底层 `object[]`
- `dict[key]` → 哈希 + 类型检查(若指定 `TokenType` 参数)

**vs C# `Dictionary<K, V>`**:
- C# `Dictionary<string, int>` → JIT 内联,泛型特化,**~50 ns**
- Udon `DataDictionary.SetValue` → 哈希 + 装箱 + EXTERN,**~300 ns**(推断)

---

## 3. 性能基准推断(基于字节码分析)

### 3.1 DataList vs C# `List<T>`

> 🔴 **【未实测】** 以下数字为**推断**,基于 Udon EXTERN 开销 + 装箱成本。

| 操作 | C# `List<T>`(假设可用) | Udon `DataList` | 性能比(推断) |
|------|------------------------|-----------------|--------------|
| `Add` (int 值) | ~5 ns | ~50-80 ns | **~10-15x 慢** |
| `Add` (string) | ~10 ns | ~80-120 ns | **~8-12x 慢** |
| `Insert` (中位) | ~20 ns (O(n)) | ~200-400 ns | **~10-20x 慢** |
| `RemoveAt` (中位) | ~30 ns (O(n)) | ~250-500 ns | **~8-15x 慢** |
| `Count` (属性) | ~1 ns | ~10-20 ns | **~10-20x 慢** |
| `Capacity` (读) | ~1 ns | ~10-20 ns | **~10-20x 慢** |
| 索引器 `list[i]` (int) | ~2 ns | ~30-50 ns | **~15-25x 慢** |
| 索引器 `list[i]` (引用) | ~5 ns | ~50-80 ns | **~10-15x 慢** |

**综合估计**:`DataList` 平均比 C# `List<T>` **慢 5-10x**。

> 来源分析:EXTERN 开销(~10x) + 装箱(偶尔) + TokenType 检查(部分路径) = 综合 5-10x

### 3.2 DataDictionary vs C# `Dictionary<K, V>`

| 操作 | C# `Dictionary<K, V>`(假设可用) | Udon `DataDictionary` | 性能比(推断) |
|------|----------------------------------|----------------------|--------------|
| `TryGetValue` (string key) | ~30 ns | ~200-300 ns | **~6-10x 慢** |
| `Add` / `SetValue` (string key) | ~40 ns | ~250-400 ns | **~6-10x 慢** |
| `ContainsKey` (string key) | ~30 ns | ~200-300 ns | **~6-10x 慢** |
| `Remove` (string key) | ~50 ns | ~300-500 ns | **~6-10x 慢** |
| `GetKeys()` (缓存命中) | ~100 ns | ~200 ns | **~2x 慢** |
| `GetValues()` (n=100,重建) | ~200 ns | ~800-1000 ns | **~4-5x 慢** |
| `ContainsValue` (n=100, 线性) | ~500 ns | ~3000-5000 ns | **~6-10x 慢** |
| JSON 序列化 (n=50 键值) | N/A | ~500-5000 ns | 仅 DataDictionary 支持 |

**综合估计**:`DataDictionary` 平均比 C# `Dictionary<K, V>` **慢 6x**(与现有 `data-dictionaries.md` §9.1 一致)。

**为什么 6x 而不是 5-10x?**
- DataDictionary 内部用 `Dictionary<string, object>` 实现
- 主要开销 = **2 层 EXTERN**(外层 DataDictionary + 内层 C# Dictionary)+ **TokenType 验证**
- 哈希 + 等值检查(C# 端)较高效

### 3.3 VRCJson 序列化 / 反序列化

| 数据规模 | 序列化时间(推断) | 反序列化时间(推断) |
|---------|------------------|-------------------|
| 小 (< 100 字符) | ~0.1-0.3 ms | ~0.2-0.5 ms |
| 中 (1-10 KB) | ~0.5-2 ms | ~1-5 ms |
| 大 (10-100 KB) | ~5-30 ms | ~10-50 ms |
| 超大 (> 100 KB) | ~50-500 ms | ~100-1000 ms |

**性能瓶颈**:
- `VRCJson.TrySerializeToJson` → 内部用 reflection 遍历 DataList / DataDictionary 树
- `VRCJson.TryDeserializeFromJson` → lazy parse + 反射构造
- 嵌套深度 > 5 层后,**反射调用栈深**,性能急剧下降

**实测建议**:
- 单次序列化 > 5ms 应考虑分批
- 嵌套深度 > 3 层建议扁平化(用 key 路径如 `"player.score.level"`)

---

## 4. 基准测试方法(给未来 Agent / 创作者)

### 4.1 基础 Get/Set 性能对比

```csharp
using VRC.SDK3.Data;
using UnityEngine;

// 1000 次 Get/Set 操作时间对比
public class DataListBenchmark : UdonSharpBehaviour {
    void Start() {
        int n = 1000;
        var sw = new System.Diagnostics.Stopwatch();
        
        // 1. DataList int Add
        sw.Restart();
        DataList list = new DataList();
        list.Capacity = n;
        for (int i = 0; i < n; i++) list.Add(i);
        long addTime = sw.ElapsedMilliseconds;
        Debug.Log($"DataList Add {n} ints: {addTime}ms");
        
        // 2. DataList 索引访问
        sw.Restart();
        long sum = 0;
        for (int i = 0; i < n; i++) sum += list[i].Int;
        long getTime = sw.ElapsedMilliseconds;
        Debug.Log($"DataList Get {n} ints: {getTime}ms");
        
        // 3. DataDictionary 写
        sw.Restart();
        DataDictionary dict = new DataDictionary();
        for (int i = 0; i < n; i++) dict.SetValue($"key_{i}", i);
        long setTime = sw.ElapsedMilliseconds;
        Debug.Log($"DataDict SetValue {n}: {setTime}ms");
        
        // 4. DataDictionary 读
        sw.Restart();
        long dictSum = 0;
        for (int i = 0; i < n; i++) {
            if (dict.TryGetValue($"key_{i}", TokenType.Int, out DataToken v)) {
                dictSum += v.Int;
            }
        }
        long getDictTime = sw.ElapsedMilliseconds;
        Debug.Log($"DataDict TryGetValue {n}: {getDictTime}ms");
    }
}
```

**预期输出** (推断,无 Unity 实测):
```
DataList Add 1000 ints: ~50-80ms
DataList Get 1000 ints: ~30-50ms
DataDict SetValue 1000: ~250-400ms
DataDict TryGetValue 1000: ~200-300ms
```

### 4.2 嵌套深度 vs 时间关系

```csharp
// 嵌套深度 vs 序列化时间
void TestNestedDepth() {
    int[] depths = { 1, 2, 3, 5, 10 };
    
    foreach (int d in depths) {
        DataList root = new DataList();
        DataList current = root;
        
        // 构造 d 层嵌套
        for (int i = 0; i < d; i++) {
            DataList inner = new DataList();
            current.Add(inner);
            current = inner;
        }
        current.Add(42);  // 叶子
        
        var sw = System.Diagnostics.Stopwatch.StartNew();
        for (int i = 0; i < 100; i++) {
            VRCJson.TrySerializeToJson(root, out DataToken result);
        }
        sw.Stop();
        Debug.Log($"Depth {d} serialize x100: {sw.ElapsedMilliseconds}ms");
    }
}
```

**预期结果**(推断):
- 深度 1: ~10ms
- 深度 2: ~15ms
- 深度 3: ~25ms
- 深度 5: ~80ms
- 深度 10: ~500ms+ (急剧恶化)

### 4.3 序列化时间 vs 数据大小关系

```csharp
// 数据大小 vs 序列化时间
void TestSerializeSize() {
    int[] sizes = { 10, 100, 1000, 10000 };
    
    foreach (int n in sizes) {
        DataList list = new DataList();
        for (int i = 0; i < n; i++) list.Add($"item_{i}");
        
        var sw = System.Diagnostics.Stopwatch.StartNew();
        for (int i = 0; i < 10; i++) {
            VRCJson.TrySerializeToJson(list, out DataToken result);
        }
        sw.Stop();
        Debug.Log($"Size {n} serialize x10: {sw.ElapsedMilliseconds}ms");
    }
}
```

**预期结果**(推断):
- n=10: ~1ms
- n=100: ~3ms
- n=1000: ~15ms
- n=10000: ~150ms+

---

## 5. 性能优化建议(基于原理,无需实测)

### 5.1 热路径用原生数组 + 手动序列化

```csharp
// ❌ 避免:热路径用 DataList(每帧 60Hz)
void Update() {
    positions.Add(transform.position);  // 装箱 + EXTERN
}

// ✅ 推荐:热路径用 Vector3[] + 手动写
[SerializeField] private Vector3[] _positions = new Vector3[1000];
private int _writeIndex = 0;

void Update() {
    _positions[_writeIndex % _positions.Length] = transform.position;  // 直接数组写
    _writeIndex++;
}
```

**理由**:数组访问 = 1 个 EXTERN,DataList 索引 = 1 个 EXTERN + 边界检查 + 装箱,**3-5x 差**。

### 5.2 大量数据用 byte[] + BitConverter

```csharp
// ❌ 避免:1000 个 float 用 DataList 持久化
DataList floats = new DataList();
for (int i = 0; i < 1000; i++) floats.Add(Mathf.PI * i);
PlayerData.Set("data", floats);  // 序列化慢

// ✅ 推荐:用 byte[] 存储
byte[] buffer = new byte[1000 * 4];
for (int i = 0; i < 1000; i++) {
    byte[] bytes = System.BitConverter.GetBytes(Mathf.PI * i);
    System.Buffer.BlockCopy(bytes, 0, buffer, i * 4, 4);
}
PlayerData.Set("data", buffer);  // 直接存二进制
```

**理由**:
- DataList 序列化 = 反射遍历 + 装箱拆箱
- byte[] 序列化 = 直接 memcpy
- 性能差 **10-50x**,数据量越大差距越大

### 5.3 避免嵌套 DataDictionary(嵌套 DataList 更快)

```csharp
// ❌ 避免:嵌套 DataDictionary(每层 6x 开销)
DataDictionary config = new DataDictionary();
config.SetValue("player", new DataDictionary());
((DataDictionary)config["player"].Reference).SetValue("score", 100);
((DataDictionary)config["player"].Reference).SetValue("level", 5);

// ✅ 推荐:扁平化 key 路径
DataDictionary flat = new DataDictionary();
flat.SetValue("player.score", 100);
flat.SetValue("player.level", 5);
```

**理由**:
- 嵌套 DataDictionary 序列化时需递归遍历,每层 N 个 EXTERN
- 扁平化 = 1 层 DataDictionary + O(1) 访问
- 嵌套 3 层 ≈ 18x 开销,扁平化 ≈ 6x 开销

### 5.4 缓存 DataList.Length

```csharp
// ❌ 避免:循环中每次访问 Count
for (int i = 0; i < list.Count; i++) {  // 每次循环调 Count 属性
    Process(list[i]);
}

// ✅ 推荐:缓存 Count
int count = list.Count;  // 1 次访问
for (int i = 0; i < count; i++) {
    Process(list[i]);
}
```

**理由**:
- `Count` 属性 = EXTERN 调用(每次 ~10-20ns)
- 循环 1000 次 = 1000 次 EXTERN
- 缓存后 = 1 次 EXTERN

**节省**:1000 次循环 ≈ 10-20μs(看似小,热路径累积显著)

### 5.5 预分配 Capacity

```csharp
// ❌ 避免:Add 触发自动扩容
DataList list = new DataList();
for (int i = 0; i < 100; i++) list.Add(i);  // 多次 2x 拷贝

// ✅ 推荐:预设 Capacity
DataList list = new DataList();
list.Capacity = 100;  // 1 次分配
for (int i = 0; i < 100; i++) list.Add(i);  // 无扩容
```

**理由**:
- `Add` 超过 Capacity → 自动 2x 扩容,拷贝原数组
- 100 个元素 = log₂(100) ≈ 7 次扩容,7 次拷贝
- 预设 = 0 次拷贝

### 5.6 避免 ContainsValue(线性扫描)

```csharp
// ❌ 避免:ContainsValue(O(n) 慢)
if (dict.ContainsValue(targetValue)) { ... }

// ✅ 推荐:用 GetKeys() + key 反查(O(1) 哈希)
DataList keys = dict.GetKeys();
for (int i = 0; i < keys.Count; i++) {
    if (dict[keys[i]].String == targetValue) { ... }
}
```

**理由**:
- `ContainsValue` = 遍历所有值(线性)
- key 反查 = O(1) 哈希

### 5.7 JSON 序列化分批

```csharp
// ❌ 避免:一次性序列化大数据
DataList big = new DataList();
for (int i = 0; i < 10000; i++) big.Add($"item_{i} with some text");
VRCJson.TrySerializeToJson(big, out DataToken json);  // 慢

// ✅ 推荐:分批
const int batchSize = 100;
for (int batch = 0; batch < 100; batch++) {
    DataList sub = new DataList();
    for (int i = 0; i < batchSize; i++) {
        sub.Add($"item_{batch * batchSize + i} with some text");
    }
    VRCJson.TrySerializeToJson(sub, out DataToken json);
    // 处理...
}
```

**理由**:
- 避免单次 > 5ms 卡顿(玩家会感知)
- 分散到多帧,VR 帧率稳定

---

## 6. 实测验证清单(给未来 Agent)

如需实测,需准备:

### 6.1 环境要求
- [ ] Unity 2022.3.22f1
- [ ] VRChat SDK 3.10.x(Worlds)
- [ ] ClientSim(本地模拟,无需 VRChat Client)
- [ ] .NET Profiler(可选,看调用栈)
- [ ] 至少 1 个测试 World(UdonSharp 脚本可编译)

### 6.2 测试场景
- [ ] 1000 次 DataList Add(Get/Set)
- [ ] 1000 次 DataDictionary Add/GetValue
- [ ] 嵌套 1/2/3/5/10 层 JSON 序列化
- [ ] 1KB / 10KB / 100KB / 1MB JSON 序列化
- [ ] ContainsKey vs GetKeys 迭代性能
- [ ] DataList 索引 vs foreach 性能

### 6.3 报告模板
完成实测后,建议在 `performance-notes.md` 追加"§7. 实测数据"章节,格式:
```markdown
## 7. 实测数据(待补充)

> 测量环境: Unity 2022.3.22f1, VRChat SDK 3.10.x, ClientSim
> 测量日期: YYYY-MM-DD
> 测量者: [Agent 名]

| 测试 | 推断 | 实测 | 偏差 |
|------|------|------|------|
| DataList Add 1000 | 50-80ms | TBD ms | TBD |
| ... |
```

---

## 7. 与现有文档的关系

| 现有文档 | 关系 |
|---------|------|
| `data-lists.md` | 提供 DataList API;本文档补充**性能维度** |
| `data-dictionaries.md` §9.1 | 已包含 DataDictionary 6x 慢的推断;本文档扩展至 DataList |
| `data-tokens.md` | 解释 17 个 TokenType;本文档 §2.1 引用其类型系统 |
| `vrcjson.md` | 介绍 VRCJson API;本文档 §3.3 推断其性能 |
| `byte-and-bit-operations.md` | 强调用 byte[] 替代 DataList 的核心思路;本文档 §5.2 强化该建议 |
| `bit-packed-flags.md` | 用 int/uint 存多 bool;**本质**与"避免 DataList"一致 |
| `performance-guide.md` | 整体性能指南;本文档是其**数据容器专项** |

---

## 8. 重要限制声明(再次强调)

> 🔴 **【未实测】** 本文档中所有性能数字均为推断,**本环境无 Unity 运行时**。
>
> 🔴 **【需 Unity 实测验证】** 任何优化决策需在 `Unity 2022.3.22f1 + VRChat SDK 3.10.x + ClientSim` 环境中实测。
>
> 🟡 **【方向性建议】** 优化策略(§5)基于**原理**(EXTERN / 装箱 / 反射)推导,**无需实测即可应用**。
> 但具体"应该预分配多少 Capacity"等问题需实测。
>
> ✅ **【可信部分】** O(n) / O(1) 复杂度标注(来自官方文档)、JSON 序列化分批建议(基于原理)、避免 ContainsValue(基于 API 语义)——这些**可信**。
>
> ❌ **【不可信部分】** 具体数字(如 5-10x 慢、0.3ms 等)、精确瓶颈百分比——这些**仅作方向性参考**。
