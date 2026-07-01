---
title: "The Udon VM and Udon Assembly - 字节码与汇编参考"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - udon-graph
  - udonsharp
aliases:
  - "The Udon VM and Udon Assembly - 字节码与汇编参考"
  - vm-and-assembly
related:
  - ai-navigation.md
  - debugging-udon-projects.md
  - external-urls.md
  - image-loading.md
  - ui-events.md
---
# The Udon VM and Udon Assembly - 字节码与汇编参考

> 来源:https://creators.vrchat.com/worlds/udon/vm-and-assembly/
> 本地化日期:2026-06-15
> 状态:FACT(VRChat 官方字节码规范)
> **⭐ 关键文档**:与 `memory/rules/udon-vm-architecture.md` 配套,与 `memory/api/udonsharp-runtime.md` 强相关
> **⚠️ 高级主题**:仅在性能优化或调试极端问题时参考

---

## 一、概述

### 1.1 是什么

> **FACT**:Udon VM 是一个**字节码解释器**,用于运行编译后的 Udon Graph 程序。

### 1.2 设计约束

| 有 | 没有 |
|----|------|
| .NET 环境依赖 | ❌ 反射访问函数 |
| 流程控制(`JUMP`/`JUMP_INDIRECT`/`JUMP_IF_FALSE`) | ❌ 局部变量(只有对象字段) |
| 调用 C# 函数(白名单内) | ❌ 直接实现 call/return / 子例程(可用 `JUMP_INDIRECT` 模拟) |
| 整数堆栈 | ❌ 真正的局部变量(递归需非常小心) |

> **关键洞察**:整数堆栈在多数情况下应被视为**"操作码的额外参数"**,而非通用栈。递归必须**极度谨慎**(无局部变量保护)。

### 1.3 何时需要

- 从 Udon Graph / UdonSharp 导出 **Udon Assembly** 看编译结果
- **性能分析**:理解"我写的代码如何编译"
- **寻找 extern 名**:`UnityEngineDebug.__Log__SystemObject__SystemVoid` 等
- **逆向工程**:理解 SDK 暴露的方法

---

## 二、Udon Types(Udon 类型名)

### 2.1 命名规则

> **FACT**:"Udon Types" 是 Udon 引用 C# 类型的方式。

| 规则 | 说明 | 示例 |
|------|------|------|
| **移除所有 `.` 和 `+`** | 用作分隔符 | `VRC.SDKBase.VRCPlayerApi+TrackingData` → `VRCSDKBaseVRCPlayerApiTrackingData` |
| **`[]` 追加 `Array` 后缀** | 数组类型 | `System.Int32[]` → `SystemInt32Array` |

### 2.2 完整示例

```text
.NET Type: System.Int32[]
Udon Type: SystemInt32Array

.NET Type: VRC.SDKBase.VRCPlayerApi+TrackingData
Udon Type: VRCSDKBaseVRCPlayerApiTrackingData

.NET Type: System.String
Udon Type: SystemString
```

### 2.3 关键例外

> **FACT**:`VRCUdonUdonBehaviour` 变为 `VRCUdonCommonInterfacesIUdonEventReceiver`(Array 后缀规则仍适用)。

> **FACT**:`VRCInstantiate` 是唯一"伪造"的 Udon 类型名,实际对应特殊操作。

---

## 三、Udon Assembly 程序结构

### 3.1 两个段

> **FACT**:Udon Assembly 程序由**数据段**和**代码段**组成,使用 start/end 指令标记。

```assembly
.data_start
# Variables go here
.data_end

.code_start
# Opcodes go here
.code_end
```

---

## 四、数据段(The Data Section)

### 4.1 用途

- 标记 UdonBehaviour 的变量
- 标记哪些变量公开(`.export`)

### 4.2 数据存储方式

> **FACT**:数据存储在 **Udon Heap**(Udon 堆)中。

- 名为"堆"实为**扁平的带类型值数组**
- "heap index" 指**该数组的索引**

### 4.3 变量定义语法

```assembly
symbol: %UdonType, initial_value
```

**示例**:
```assembly
message: %SystemString, "Hello, world!"
```

| 元素 | 含义 |
|------|------|
| `message` | 变量符号名 |
| `%SystemString` | 类型 |
| `"Hello, world!"` | 初始值 |

### 4.4 合法初始值

> **FACT**:合法值包括 `null` / `this` / `true` / `false` / 字符串 / 字符常量 / 整数 / 无符号整数(以 `u` 结尾)/ 浮点数。
> 汇编器对类型严格:

| 类型 | 合法值 |
|------|--------|
| `SystemSingle` / `SystemDouble` | 数字或 `null` |
| `SystemInt32` / `SystemUInt32` | 整数(有/无符号)或 `null` |
| `SystemString` | 字符串字面量或 `null` |
| 其他类型(含 `SystemObject`) | 仅 `this` 或 `null` |

### 4.5 `this` 特殊语义

> **FACT**:`this` 的含义**取决于变量类型**,不是 C# 中的传统 `this`。

| 变量类型 | `this` 指向 |
|----------|-------------|
| `GameObject` | UdonBehaviour 的 GameObject |
| `Transform` | `GameObject.transform` |
| `UdonBehaviour` / `IUdonBehaviour` / `Object` | UdonBehaviour 自身 |
| 其他类型 | ❌ 错误 |

### 4.6 已知 Udon Assembly 限制

> **FACT**:以下类型**无法在 Udon Assembly 中指定非空初始值**(可在 Udon Graph 和 UdonSharp 中指定):

- `SystemType`
- `SystemInt64`
- `SystemUInt64`
- `SystemSByte`
- `SystemByte`
- `SystemInt16`
- `SystemUInt16`
- `SystemBoolean`(**`true`/`false` 实际无法成功指定**)

> **唯一绕过方式**:**不使用 Udon Assembly**(改用 Udon Graph 或 UdonSharp)。

> **FACT**:浮点数**总是按 float 读取**,即使目标类型是 double。

### 4.7 导出与同步元数据

#### 公开变量

```assembly
.export message
```

- 等价于 UdonSharp 的 `public` 修饰符
- 在 Unity Inspector 中可见

#### 同步元数据

```assembly
.sync message, none
```

- 标记变量为网络同步
- 等价于 UdonSharp 的 `[UdonSynced]` 特性 + `synced` 复选框
- 第二个参数是**插值模式**:`none` / `linear` / `smooth`

| 模式 | 含义 |
|------|------|
| `none` | 无插值,直接同步 |
| `linear` | 线性插值 |
| `smooth` | 平滑插值 |

> **【推断】** 并非所有类型都支持所有插值模式。

---

## 五、代码段(The Code Section)

### 5.1 结构

代码段是**带标签和可能导出的操作码列表**。

```assembly
.export _start
_start:
    PUSH, message
    EXTERN, ""UnityEngineDebug.__Log__SystemObject__SystemVoid""
    JUMP, 0xFFFFFFFC
```

### 5.2 事件导出

#### 标准事件

- 以 `_` 开头(如 `_onEnable`, `_start`)
- 参数通过**变量(非公开)** 传递,需要**自行创建**
- 完整列表**很长**,最佳探索方式:**Udon Graph**

#### 启动顺序

> **FACT**:**前两个事件是 `_onEnable` 和 `_start`(按此顺序)**。它们**总是先于其他事件运行**,中间无间隔。
> 任何试图绕过这一点的调用都将被忽略。

参考 `memory/world/udon/event-execution-order.md` 获取完整执行顺序。

#### 自定义事件

- 永远**不带参数**(自定义机制除外)
- **不以 `_` 开头**

### 5.3 操作码参数

参数可以是:
- 整数
- 符号(整数值,即 heap index 或 code address)
- **字符串**(汇编器会创建**隐藏的未命名变量**存放字符串,实际值是 heap index)

### 5.4 已知陷阱

> **🔴 定义两个指向同一位置的代码符号会导致 `Address aliasing detected` 错误。**

---

## 六、9 个 Udon Opcodes 完整参考

> **FACT**:Udon VM 共有 **9 个 Opcodes**(Opcode 3 未使用)。

### 6.1 总览表

| # | 名称 | 参数数 | 简述 |
|---|------|--------|------|
| 0 | `NOP` | 0 | 无操作 |
| 1 | `PUSH, parameter` | 1 | 推入堆栈(实际是 heap index) |
| 2 | `POP` | 0 | 弹出堆栈 |
| 3 | (未使用) | - | 保留 |
| 4 | `JUMP_IF_FALSE, parameter` | 1 | 条件跳转 |
| 5 | `JUMP, parameter` | 1 | 无条件跳转(0xFFFFFFFC = 返回) |
| 6 | `EXTERN, parameter` | 1 | 调用 C# 方法 |
| 7 | `ANNOTATION, parameter` | 1 | 注释(忽略) |
| 8 | `JUMP_INDIRECT, parameter` | 1 | 间接跳转 |
| 9 | `COPY` | 0 | 复制 |

### 6.2 详细说明

#### `NOP` (Opcode 0)

- **参数数**:0
- **行为**:无操作
- **用途**:一般无理由使用;**唯一例外**:`Address aliasing detected` 错误时用 NOP 隔离

#### `PUSH, parameter` (Opcode 1)

- **参数数**:1
- **行为**:将整数推入堆栈顶部

> **⚠️ 关键理解**:Udon Assembly 看起来"推入值",**实际推入的是 heap address**。
> 除非你**极度追求体积优化**(可能以运行时速度为代价)或尝试混淆,**永远不要在条件分支中**使用 PUSH。
> **正确模式**:在 `EXTERN` / `COPY` / `JUMP_IF_FALSE` **前**立即 PUSH 所有内容。

#### `POP` (Opcode 2)

- **参数数**:0
- **行为**:移除堆栈顶部整数,无其他副作用

#### `JUMP_IF_FALSE, parameter` (Opcode 4)

- **参数数**:1
- **行为**:
  1. 弹出堆栈顶的 heap index
  2. 读取 `SystemBoolean` 值
  3. 若为 `false`,跳转到参数指定的字节码位置
  4. 否则继续下一条指令

#### `JUMP, parameter` (Opcode 5)

- **参数数**:1
- **行为**:跳转到参数指定的字节码位置

> **特殊值**:`JUMP, 0xFFFFFFFC` 用于**结束执行**(从 Udon 代码返回)。

#### `EXTERN, parameter` (Opcode 6) ⭐ 关键

- **参数数**:1
- **行为**:Udon **执行任何有用操作**都通过此指令

> **参数细节**:
> - 参数是 heap index,**初始包含 extern 名(字符串)**,**但该位置也会被写入**
> - 优化:Udon 在首次运行后**缓存** extern 信息到该 heap index
> - 这些缓存值仍是 heap 值,**可被复制**

> **参数传递**:
> - 参数按 `PUSH` 顺序给出,**第一个 PUSH 的值就是第一个参数**
> - `in` 参数:读取
> - `ref` 参数:读取并写入
> - `out` 参数:写入
> - **非静态 extern**:`this` 参数加在**最前**
> - **有返回值**(返回类型非 `SystemVoid`):返回值作 `out` 参数加在**最后**

#### `ANNOTATION, parameter` (Opcode 7)

- **参数数**:1
- **行为**:**长 NOP**,参数被忽略
- **用途**:源码级调试标记

#### `JUMP_INDIRECT, parameter` (Opcode 8)

- **参数数**:1
- **行为**:
  1. 获取参数指定的 heap index
  2. 读取 `SystemUInt32` 值
  3. 解释为**字节码位置**并跳转

**用途**:模拟 call/return 机制(无原生支持的子例程)。

#### `COPY` (Opcode 9)

- **参数数**:0
- **行为**:
  1. 弹出**两个** heap index
  2. **第二个弹出的值**(即第一个 PUSH 的)**复制到第一个弹出的位置**(即第二个 PUSH 的)

---

## 七、Externs Reference(外部方法签名)

> **🔴 警告**:依赖 extern 签名的精确格式**不可取**,除非你依赖**已知存在的特定 extern**。
> 签名格式可能很奇怪,泛型等属性无法从签名推断。若需要完整 API,需**编写 C# 代码从 Udon Graph 节点抓取**。

### 7.1 签名格式

> **FACT**:Extern 形式为 `SomeUdonTypeName.SomeSignature`。

**唯一例外**:`VRCInstantiate`(Udon 类型名是"伪造的")。

### 7.2 签名结构

**示例**:
```text
SystemDateTimeOffset.__TryParseExact__SystemString_SystemStringArray_SystemIFormatProvider_SystemGlobalizationDateTimeStyles_SystemDateTimeOffsetRef__SystemBoolean
```

**对应 C# 签名**:
```csharp
System.DateTimeOffset.TryParseExact(
    string input,
    string[] formats,
    System.IFormatProvider formatProvider,
    System.Globalization.DateTimeStyles styles,
    out System.DateTimeOffset result
)
```

### 7.3 命名规则

| 元素 | 说明 |
|------|------|
| 开头 | `__`(双下划线) |
| 函数名 | `__` 后接函数名(构造函数为 `ctor`) |
| 参数分隔 | `__` 后每个**非 this 参数**的 Udon 类型名,下划线分隔 |
| ref/out 修饰 | Udon 类型名加 `Ref` 后缀 |
| 结尾 | `__` 后接返回类型的 Udon 类型名 |

> **重要**:**非静态方法的 `this` 参数不会在签名中标记**。

### 7.4 特殊情况

| 情况 | 描述 |
|------|------|
| **泛型** | 类型参数作 "Udon types" 列出(如 `T`),有**隐式的 `SystemType` 参数** |
| **UdonBehaviour 变形** | `VRCUdonUdonBehaviour` → `VRCUdonCommonInterfacesIUdonEventReceiver`(Array 后缀规则仍适用) |

### 7.5 探索 Externs 的方法

> **FACT**:**目前没有完整的 extern 参考**。

| 资源 | 用途 |
|------|------|
| **UdonSharp API 参考** | https://udonsharp.docs.vrchat.com/vrchat-api(VRChat 方法) |
| **UdonSharp Class Exposure Tree** | https://udonsharp.docs.vrchat.com/class-exposure-tree(浏览可用类) |
| **从 Udon Graph 节点导出** | 最可靠的方法(可看到实际签名) |

> **🔴 已知问题**:UdonSharp Class Exposure Tree 的**复制成员名功能当前已损坏**。可用来快速浏览,但**实际获取 extern 名仍需 Udon Graph**。

---

## 八、完整示例程序

### 8.1 Hello World

```assembly
.data_start
    message: %SystemString, "Hello, world!"
.data_end

.code_start
.export _start
_start:
    PUSH, message
    EXTERN, "UnityEngineDebug.__Log__SystemObject__SystemVoid"
    JUMP, 0xFFFFFFFC
.code_end
```

### 8.2 条件分支

```assembly
.data_start
    counter: %SystemInt32, null
    threshold: %SystemInt32, 10
.data_end

.code_start
.export _start
_start:
    PUSH, counter
    PUSH, threshold
    EXTERN, "SystemInt32.__op_GreaterThan__SystemInt32_SystemInt32__SystemBoolean"
    JUMP_IF_FALSE, end
    
    PUSH, counter
    EXTERN, "UnityEngineDebug.__Log__SystemObject__SystemVoid"
    
end:
    JUMP, 0xFFFFFFFC
.code_end
```

### 8.3 同步变量

```assembly
.data_start
    .export score
    score: %SystemInt32, 0
    .sync score, linear
.data_end
```

---

## 九、与其他文档的关系

| 相关文档 | 用途 |
|----------|------|
| `memory/rules/udon-vm-architecture.md` | Udon VM 架构(高级规则) |
| `memory/api/udonsharp-runtime.md` | UdonSharp 运行时系统 |
| `memory/api/udon-type-exposure.md` | Udon 类型暴露规则 |
| `memory/rules/udonsharp-language-limits.md` | UdonSharp 语言限制 |
| `memory/api/events-reference.md` | 事件完整参考 |

> **关联说明**:
> - **`udon-vm-architecture.md`** 应引用本文档作为字节码参考
> - **`udonsharp-runtime.md`** 应引用本文档的 EXTERN 签名规则
> - **`udon-type-exposure.md`** 应引用本文档的"Udon Types"命名规则
> - **`udonsharp-language-limits.md`** 应引用本文档的 PUSH/COPY/EXTERN 实现限制

---

## 十、性能与设计含义

### 10.1 PUSH 的"虚假"语义

> **核心洞察**:PUSH 推入的是 **heap index**,不是值本身。

- 这意味着每个 PUSH **本身不做任何工作**,只是传递引用
- COPY 才是**真正的数据移动**
- EXTERN 才触发**实际计算**

### 10.2 EXTERN 缓存

> **FACT**:Udon **首次运行后缓存** extern 信息,后续调用直接使用缓存。

- 缓存值仍在 heap 中,可被 COPY
- 这就是为什么 Udon **执行大量重复 extern 调用**比"看起来"快

### 10.3 整数堆栈的真实用途

> **FACT**:整数堆栈 = "操作码的额外参数"通道。

- 不应作为通用计算栈
- 递归必须**极度小心**(无局部变量保护)
- 推荐模式:在 EXTERN/COPY/JUMP_IF_FALSE **前**立即 PUSH

### 10.4 与 UdonSharp 的性能对比

| 维度 | Udon Assembly(手写) | UdonSharp 编译产物 |
|------|---------------------|-------------------|
| 可读性 | ❌ 极差 | ✅ 良好 |
| 可维护性 | ❌ 差 | ✅ 良好 |
| 性能(同逻辑) | ✅ **可能略快**(避免冗余 PUSH/COPY) | ✅ 接近最优 |
| 调试难度 | 🔴 极高 | 🟢 低 |
| 适用场景 | 🔴 **极少** | ✅ **绝大多数** |

> **【推断】** 手写 Udon Assembly **仅在极端性能优化场景**下有意义。**99% 的情况应使用 UdonSharp**。

---

## 十一、风险与限制

### 11.1 不稳定的 API

> **🔴 警告**:Extern 签名**不属于稳定 API**。VRChat 可能在任何版本变更。

| 风险 | 等级 | 说明 |
|------|------|------|
| Extern 签名变更 | 🔴 严重 | SDK 更新可能破坏 Udon Assembly |
| 类型名变更 | 🟡 中等 | 极少,但 `VRCUdonUdonBehaviour` 已有先例 |
| Opcode 行为变更 | 🟢 低 | 9 个 Opcode 已稳定多年 |

### 11.2 调试困难

- 无原生调试器
- 错误信息不友好(`Address aliasing detected` 等)
- 必须通过 `Debug.Log` + Log Viewer 调试

### 11.3 维护成本

> **【推断】** Udon Assembly 代码**几乎不可维护**,应仅作为**最后手段**。

---

## 十二、检查清单(决定是否使用 Udon Assembly)

- [ ] UdonSharp / Udon Graph **无法实现**所需逻辑
- [ ] 性能**关键**路径,且 UdonSharp 已验证为瓶颈
- [ ] 准备好**接受外部签名变更风险**
- [ ] 准备好**接受高维护成本**
- [ ] 有完整单元测试覆盖

> **⚠️ 默认推荐**:**不要使用 Udon Assembly**。仅在所有其他方案都失败时考虑。

---

## 十三、Missing Information

> **【未确认】** 以下信息需要查询额外资料:
>
> - Opcode 3 的确切含义(疑似保留未用)
> - 完整 extern 列表(官方未提供)
> - `VRCInstantiate` 的真实实现细节
> - Udon VM 的执行速度基准数据
