---
title: "Rule Set: UdonSharp Deep Pitfalls"
category: rules
knowledge_level: applied
status: active
source: "VRChat 社区 UdonSharp 深度指南 (vrcd.org.cn) + VRChat Feedback"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - rules
  - rules
  - udonsharp
  - avatar
aliases:
  - "Rule Set： UdonSharp Deep Pitfalls"
  - "Rule Set: UdonSharp Deep Pitfalls"
related:
  - multi-vm-rules.md
  - udon-vm-architecture.md
  - udonsharp-language-limits.md
  - networking-rules.md
  - performance-rules.md
---
# Rule Set: UdonSharp Deep Pitfalls


---

## RULE-DP-01: 工程路径不能有非 ASCII 字符

### Rule
Unity 工程目录名及完整路径不得包含任何非 ASCII 字符（中文、日文、特殊符号等）。

### Reason
Mono 对非 ASCII 字符串编码支持有历史 bug（如 mono/mono#20968, mono/mono#7117）。Mono 维护已停止，这些问题不会修复。可能导致：
- Unity 打包脚本出错（非你的脚本错误，而是 Unity 内部）
- `Illegal byte sequence encountered in the input`
- 字符串转换异常

### Fix
确保路径只含 ASCII 字符，如 `C:\Projects\MyVRCAvatarWorld\`。

---

## RULE-DP-02: 禁止使用 `internal` 关键字在 UdonSharp 脚本中

### Rule
UdonSharp 脚本中的类方法、类属性访问器不应使用 `internal` 修饰符。截止 SDK 3.8.2 未修复。

### Reason
U# 编译器从未考虑 `internal` 修饰符。取决于 U# 程序集的编译顺序，`internal` 方法会**随机被导出或不被导出**——没有任何错误提示。

### Workaround
使用条件编译：
```csharp
#if COMPILER_UDONSHARP
    public
#else
    internal protected
#endif
```
注意：两个不同命名空间有同名类型且同时 using 时可能冲突。

---

## RULE-DP-03: Enum 的 5 个陷阱

### 3.1 Enum.ToString() 不会输出名称
```csharp
enum UserEnum { One, Two }
UserEnum v = UserEnum.One;
Debug.Log(v.ToString()); // Output: "0" 而非 "One"
```
**Fix**: 用 `switch` + 手动字符串映射。

### 3.2 不能将 Enum cast 与其他操作写在一起
```csharp
// ❌ 错误
dataList.Add((int)anEnum);    // "Cannot retrieve heap variable of type 'Int32' as type 'DataToken'"
bar += (byte)enumValue;      // "Cannot retrieve heap variable of type 'Int32' as type 'byte'"

// ✅ 正确: 必须先转到独立 int 变量
int enumAsInt = (int)enumType;
dataList.Add(enumAsInt);
byte enumAsByte = (byte)enumAsInt;
```

### 3.3 可选方法参数不要用 Enum 做默认值
```csharp
// ❌ 编译错误
void OptionalEnum(AnEnum e = AnEnum.Option) { }
```

### 3.4 非用户定义 Enum 的 == 比较必须 cast 到 int
```csharp
// ❌ 可能出错
if (inputMethod == VRCInputMethod.Touch) { }

// ✅ 正确
if ((int)inputMethod == (int)VRCInputMethod.Touch) { }
```

### 3.5 用户定义 Enum 的特定比较场景会出错
```csharp
enum TestEnum { ONE, TWO }
var max = TestEnum.TWO;
Debug.Log(max >= TestEnum.TWO);           // false (????!)
Debug.Log((int)max >= (int)TestEnum.TWO); // true
Debug.Log(TestEnum.TWO >= TestEnum.TWO);  // true (但这个却正确!)
```
**Fix**: 始终将 Enum 值 cast 到 int 后再做比较操作。

---

## RULE-DP-04: 避免使用 `partial` 关键字

### Rule
在 UdonSharp 中避免使用 `partial` 关键字拆分类定义。

### Reason
`partial` 类在版本管理（Git）中容易造成冲突和追踪困难。多个文件定义同一个类会让代码审查和合并变得复杂。

---

## RULE-DP-05: 禁止在 Update 中分配内存

### Rule
不要在 `Update()`/`LateUpdate()`/`FixedUpdate()` 中创建新对象或将 struct 赋给新变量。

### Reason
- Udon 中每次分配新对象/装箱会导致内存分配
- 大量一次性对象迫使 GC 执行**全面的非增量收集**（冻结所有代码），导致游戏频繁卡顿
- 这在 VR 中尤其糟糕（可能导致晕动症）

### Avoid
- `new` 操作符在热路径
- struct → object 装箱
- 向数组频繁添加新元素（导致重新分配）
- `Debug.Log()` 内部的隐式字符串分配

### Pattern
- 在 `Start()` 中预分配所有数组和对象
- 使用固定容量 + 手动计数
- 用 `StringBuilder`（3.7.1+）代替 `+` 拼接

---

## RULE-DP-06: Manual Sync 的 OnDeserialization 分帧问题

### Rule
当有多个 `[UdonSynced]` 变量时，`OnDeserialization()` 触发时**不一定所有变量都已完成同步**。VRCSDK 可能将同步拆分到 2 帧或更多帧。

### Impact
- 不能在 `OnDeserialization()` 中假设所有 synced variables 都已更新
- 这在 Manual Sync 中尤其是大同步负载时容易出问题

### Fix
- 压缩每个 UdonBehaviour 的同步变量数量和大小，确保能在一帧内完成同步
- 为关键变量使用 `[FieldChangeCallback]` 做独立监控
- 不要依赖 `OnDeserialization()` 处理"所有变量一起更新"的逻辑

---

## RULE-DP-07: Continuous Sync 丢包不重传

### Rule
Continuous Sync 不保证变量最终同步。中途丢包后**不会重新同步**，远端可能永久看到旧值。

### Reason
Continuous Sync 是 fire-and-forget 式持续推送。没有确认机制，没有重传。

### Fix
- 重要状态不要依赖 Continuous Sync
- 离散关键状态用 Manual Sync（Manual Sync 丢包概率更低且有确认）
- Continuous Sync 仅用于容错性高的连续数据（位置/旋转）

---

## RULE-DP-08: 禁止使用 NoVariableSync

### Rule
不要使用 `BehaviourSyncMode.NoVariableSync`。只使用 Manual、Continuous、None 三种。

### Reason
`NoVariableSync` 有各种奇怪的 Bug。事件可能不可达，行为不可预测。

---

## RULE-DP-09: 不要同步 String 类型

### Rule
尽可能避免将 `string` 作为 `[UdonSynced]` 变量。

### Reason
String 大小不确定，编码开销大（UTF-16 每字符 2 字节），极易超出 Continuous Sync 的 200B 预算导致静默截断。

### Prefer
- 同步 int ID，本地查表解析为 string
- 使用 `SendCustomNetworkEvent` 触发一次性消息
- 如果必须同步长 string，用 Manual Sync（上限 ~280KB）

---

## RULE-DP-10: 不要同步 DisplayName，用 playerId

### Rule
不要通过同步 `displayName` 字符串来传递玩家标识。使用 `playerId` (int)。

### Reason
- `displayName` 是变长字符串，浪费同步带宽
- `displayName` 可能被用户随时更改
- `playerId` 是固定的 4 字节 int，稳定唯一

### Pattern
```csharp
// ✅ 正确: 同步 playerId
[UdonSynced] private int _lastInteractorId;
VRCPlayerApi player = VRCPlayerApi.GetPlayerById(_lastInteractorId);

// ❌ 错误: 同步 displayName
[UdonSynced] private string _lastInteractorName;
```

---

## RULE-DP-11: 手动调用 OnDeserialization 保持主客一致

### Rule
Owner 在执行 `RequestSerialization()` 后，应手动调用 `OnDeserialization()` 以保证本地表现与远端一致。

### Pattern
```csharp
[UdonSynced] public int Variable;

public void SetSyncedVariable() {
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
    Variable = newValue;
    RequestSerialization();
    OnDeserialization();  // 手动触发，统一表现逻辑
}

public override void OnDeserialization() {
    // 所有表现更新逻辑集中在这里
    UpdateVisuals();
}
```

### Reason
`OnDeserialization()` 只在远端自动触发。Owner 侧不自动触发。把所有表现逻辑集中在 `OnDeserialization()` 中并手动触发，可保证所有客户端的表现一致。

---

## RULE-DP-12: 避免 `public` 内部实现方法

### Rule
不要将内部实现方法标记为 `public`。如果不得不 `public`（如给其他脚本用的 API），方法名加 `_` 前缀。

### Reason
1. `public` 方法被导出到 Udon 符号表，有微小的性能影响
2. `public` 方法默认可被 `SendCustomEvent()` 或网络 RPC 调用——存在安全隐患
3. `_` 前缀是一种约定，暗示"不应被外部调用"

### Pattern
```csharp
// ✅ 内部实现 - private
private void UpdateScoreDisplay() { }

// ✅ 公开 API - _ 前缀
public void _IncrementScore(int points) { }
```

---

## RULE-DP-13: 将 SyncMode 写死在脚本中

### Rule
始终使用 `[UdonBehaviourSyncMode()]` 属性在代码中声明同步模式，不要依赖 Inspector 设置。

### Pattern
```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class MyScript : UdonSharpBehaviour { }
```

### Reason
Inspector 中的 SyncMode 设置容易在 prefab 迭代中丢失或被错误覆盖。代码中显式声明是唯一可靠方式。

---

## RULE-DP-14: UdonSharp Assembly Definition 名称必须一致

### Rule
UdonSharp Assembly Definition (.asmdef) 的文件名必须与其中定义的名称完全一致。

---

## RULE-DP-15: U# 编译器不尊重程序集定义的符号

### Rule
条件编译符号必须定义到 Project Global（Project Settings → Player → Scripting Define Symbols），U# 编译器不读取 .asmdef 中的符号定义。

---

## RULE-DP-16: U# Proxy Object 代理对象失同步

### Rule
假设运行时实例化的 UdonBehaviour 的 C# 代理对象可能与实际 UdonBehaviour 失去同步。

### Context
- U# 脚本在 Unity Editor 中同时存在于两个层：C# MonoBehaviour 代理对象 + 底层 UdonBehaviour
- 代理对象上的操作不是 100% 转发到 UdonBehaviour
- 部分情况下调用代理对象会触发原始 C# 逻辑而非转发到 Udon

### Impact
运行时 Instantiate 带 UdonSharpBehaviour 的 prefab 时，代理对象的状态可能与 UdonBehaviour 不一致。

---

## RULE-DP-17: Profiling UdonBehaviour

### Technique
在 Unity Profiler 中追踪 UdonBehaviour 的执行耗时：

通过修改 `UdonBehaviour.LoadProgram()` 插入 ProfilerMarker：
```csharp
_managedUpdateProfilerMarker = new ProfilerMarker($"{gameObject.name}.Update()");
_managedLateUpdateProfilerMarker = new ProfilerMarker($"{gameObject.name}.LateUpdate()");
_managedFixedUpdateProfilerMarker = new ProfilerMarker($"{gameObject.name}.FixedUpdate()");
```
之后在 Profiler 中会以 `{GameObject名称}.(Late/Fixed)Update()` 形式显示耗时。

---

---

## RULE-DP-18b: OnAudioFilterRead 的并行陷阱

### Rule
`OnAudioFilterRead` 在 Unity 音频线程中执行，**与 Udon 主线程并行**。虽然在同一 UdonBehaviour 中，但两个线程可能同时访问成员变量，导致**数据竞争**。

### Impact
- 音频线程和主线程同时读写同一个 UdonBehaviour 变量 → 结果不可预期
- 虽然可以利用这个并行特性卸载计算，但必须确保数据隔离

### Fix
- 如果不需要音频处理，不要在 UdonBehaviour 中实现 `OnAudioFilterRead`
- 如果利用音频线程做计算卸载，必须保证音频线程操作的数据集与主线程完全隔离
- 注意 U# Proxy Object 在 Editor 中的行为可能与实际 UdonBehaviour 不一致

### 相关的并行卸载技术
参见 `patterns/unorthodox-patterns.md` Pattern 4（含三种并行卸载技术对比与风险评级）。

---

## RULE-DP-18: 不要问 LLM 关于 U# 的任何事情

### Rule
不要依赖 LLM（包括本 Agent 在不确定时）对 U# 的判断，始终验证。U# 资料极少，LLM 会大量胡言乱语（幻觉）。

### 本文档本身的免责
本文档来自 VRChat 社区（vrcd.org.cn），作者明确声明：**不论证所有事实完全正确。部分内容基于对 UdonVM 的逆向工程推断，需要验证。**
