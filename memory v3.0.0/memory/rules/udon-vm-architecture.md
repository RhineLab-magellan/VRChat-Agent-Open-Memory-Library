---
title: "Udon VM Architecture Reference"
category: rules
knowledge_level: applied
status: active
source: "VRChat SDK DLL 逆向工程 (vrcd.org.cn Udon VM 研究笔记) + 官方文档 (creators.vrchat.com)"
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - rules
  - udonsharp
  - light
aliases:
  - "Udon VM Architecture Reference"
  - udon-vm-architecture
related:
  - "world/udon/vm-and-assembly.md"
  - multi-vm-rules.md
  - udonsharp-deep-pitfalls.md
  - udonsharp-language-limits.md
  - networking-rules.md
---
# Udon VM Architecture Reference

> SDK Version: VRChat SDK 3.x (核心 VM 变化极小)
> Last Verified: 2026-06-15
> **关联参考**:`memory/world/udon/vm-and-assembly.md` - 官方字节码规范(汇编语法 + Extern 签名格式)

---

## 1. Opcode Set — 只有 9 条指令

Udon VM 的指令集极其精简。所有 UdonSharp 代码最终编译为这 9 条指令的组合。**完整规范(Udon Assembly 语法、9 Opcodes 详解、Extern 签名格式)见 [`memory/world/udon/vm-and-assembly.md`](../world/udon/vm-and-assembly.md)**。

| Opcode | 值 | 操作数 | 含义 |
|---|---|---|---|
| NOP | 0x0 | 无 (4 bytes) | No operation，仅步进 PC |
| PUSH | 0x1 | 单操作数 (8 bytes) | 将堆地址推入栈 |
| POP | 0x2 | 无 (4 bytes) | 栈顶弹出。栈空 → 程序停止 |
| JUMP_IF_FALSE | 0x4 | 单操作数 (8 bytes) | 出栈读取 bool，false 时跳转 |
| JUMP | 0x5 | 单操作数 (8 bytes) | 无条件跳转（含耗时检查） |
| EXTERN | 0x6 | 单操作数 (8 bytes) | 外部函数调用（最昂贵指令） |
| ANNOTATION | 0x7 | 单操作数 (8 bytes) | 注解（仅步进 PC，可能是调试信息） |
| JUMP_INDIRECT | 0x8 | 单操作数 (8 bytes) | 从堆读取目标地址后跳转 |
| COPY | 0x9 | 无 (4 bytes) | 出栈两次，源→目标堆复制 |

**每条指令 4-8 字节。条件分支/循环 = JUMP_IF_FALSE。函数调用 = EXTERN。变量赋值 = COPY。**

---

## 2. 核心数据结构

### 2.1 UdonHeap — 装箱地狱

```text
_heap: IStrongBox[]  (默认 512，最大 1,048,576)
```

- 每个变量都是**独立装箱**的 `StrongBox<T>` 对象
- `GetHeapVariable<T>`: 先从 StrongBox 获取 object，再类型检查/拆箱
- `CopyHeapVariable`: 有完整的类型匹配链（float/int/bool/enum/array/...），每次 copy 都要走一遍
- `TryGetHeapVariable`: 同样的拆箱路径

**性能影响**: UdonSharp 中的 `int a = b;` 在 Udon VM 中 = PUSH + PUSH + COPY + POP = 至少 3-4 条指令 + 堆拆箱/装箱。不是一条 CPU 指令！

### 2.2 LightweightStack — 栈

```text
_stack: LightweightStack<uint> (初始容量 1024)
```

- 存储的是**堆地址** (uint)，不是值本身
- 栈扩容: 容量不足时 `new T[2 * capacity]` + `Array.Copy`
- PopSlice: EXTERN 调用时一次弹出所有参数的堆地址

### 2.3 程序计数器与字节码

```text
_processedByteCode: uint[]  (从 byte[] 转换而来)
_programCounter: uint       (字节偏移量，必须 4 字节对齐)
```

- `byte[] → uint[]`: 验证指令合法性 + 4 字节对齐
- 零操作数指令占 1 个 uint slot，单操作数占 2 个
- `CheckJumpTarget`: 跳转目标必须 4 字节对齐，否则抛异常

---

## 3. EXTERN — 最昂贵的指令

### 调用链

```
EXTERN 指令
  → 从堆读取外部调用签名 (string 或 CachedUdonExternDelegate)
  → [首次调用] 解析签名字符串 "模块名.__方法名__参数类型__返回类型"
  → UdonWrapper.GetExternFunctionDelegate() + GetExternFunctionParameterCount()
  → 创建 CachedUdonExternDelegate 并写回堆（缓存）
  → [后续调用] 直接从缓存读取委托
  → _stack.PopSlice(parameterCount) 获取参数堆地址
  → delegate.Invoke(_heap, parameterAddresses)
```

### 签名格式
```
外部模块名称.__外部调用名称__参数类型__返回类型

例: "SystemMath.__Abs__SystemDecimal__SystemDecimal"
```

### 安全白名单
- `IUdonSecurityBlacklist._blacklist` 过滤禁用类型
- 两个程序集: `VRC.Udon.Wrapper.Modules` (Unity/.Net) + `VRC.Udon.VRCWrapperModules` (VRChat)
- 在 delegate invoke 之前/之中进行白名单检查

### 性能代价
每一步都有成本：堆查找 → 签名解析 → 委托获取 → 参数出栈 → 委托调用 → 参数入栈 → 下一指令。**每次 `Debug.Log()`、`Animator.SetInteger()`、`Networking.SetOwner()` 都走这条完整路径。**

---

## 4. 执行循环 (Interpret)

```
while (_programCounter < uint.MaxValue && _programCounter + 3 < length):
    switch (opcode):
        NOP:          _programCounter += 4
        PUSH:         读操作数 → _stack.Push() → _programCounter += 8
        POP:          _stack.TryPop() → 空则 halted → _programCounter += 4
        JUMP_IF_FALSE: CheckExecutionTimeLimit() → _stack.Pop() → 
                       读取 bool → true=+8, false=跳转
        JUMP:         CheckExecutionTimeLimit() → CheckJumpTarget → 跳转
        JUMP_INDIRECT: CheckExecutionTimeLimit() → 从堆读地址 → 跳转
        EXTERN:       CheckExecutionTimeLimit() → 委托调用链 → +8
        ANNOTATION:   _programCounter += 8
        COPY:         _stack.Pop()×2 → CopyHeapVariable → +4
```

**解读**:
- **纯解释执行** — 没有任何 JIT，没有热点编译
- **没有优化** — 没有循环展开、没有死代码消除、没有指令合并
- **JUMP_IF_FALSE/JUMP/JUMP_INDIRECT/EXTERN** 四条指令触发了 `CheckExecutionTimeLimit`
- EXTERN 是整个 VM 中最昂贵的路径

---

## 5. 安全检查

### 5.1 跳转目标验证 (CheckJumpTarget)
- 目标必须是 4 的整数倍
- 不允许 `uint.MaxValue`
- 不满足 → `UdonVMException`

### 5.2 执行时间限制 (CheckExecutionTimeLimit)
- 单次 `Interpret()` 调用执行 > **10 秒** → `_halted = true` + 抛异常
- 仅在无 Debugger 附加时生效
- **JUMP_IF_FALSE / JUMP / JUMP_INDIRECT / EXTERN 都触发检查**
- 设计用途: 防止无限循环/无限递归

### 5.3 字节码验证 (ProcessByteCode)
- 未知 opcode → 拒绝加载
- 每条指令的格式必须合法

---

## 6. 事件系统

### 事件检测 (ProcessEntryPoints)
UdonBehaviour 通过符号表检测程序员定义的事件：

| 导出符号 | 触发的事件 | 代理类型 |
|---|---|---|
| `_interact` | Interact | — |
| `_update` | Update | RegisterUpdate |
| `_lateUpdate` | LateUpdate | RegisterUpdate |
| `_fixedUpdate` | FixedUpdate | RegisterUpdate |
| `_postLateUpdate` | PostLateUpdate | RegisterUpdate |
| `_onRenderObject` | OnRenderObject | OnRenderObjectProxy |
| `_onWillRenderObject` | OnWillRenderObject | OnWillRenderObjectProxy |
| `_onTriggerStay` | OnTriggerStay | OnTriggerStayProxy |
| `_onCollisionStay` | OnCollisionStay | OnCollisionStayProxy |
| `_onAnimatorMove` | OnAnimatorMove | OnAnimatorMoveProxy |
| `_onAudioFilterRead` | OnAudioFilterRead | OnAudioFilterReadProxy |

### 事件执行流程 (RunEventAdvanced)
```
RunEventAdvanced("_interact", canRunBeforeStart)
  → _isReady? _hasDoneStart? _hasError? _udonVM null?
  → _eventTable.TryGetValue("_interact", out entryPoints)
  → foreach entryPoint: RunProgram(entryPoint)
    → SetProgramCounter(entryPoint)
    → _udonVM.Interpret()
    → 错误则 _hasError = true, enabled = false
    → 恢复 program counter
```

### VariableChangeEvent (FieldChangeCallback 底层实现)
```
"_var_changed__variableName" 前缀匹配
  → 解析变量名
  → 建立 variableAddress → (eventAddress, oldValueAddress) 映射
  → 变量变化时自动触发
```

---

## 7. Udon 为什么慢 — 基于 VM 架构的根本原因

### 7.1 纯解释器 (No JIT)
无任何编译优化。每条指令独立执行，无热点检测，无方法内联。

### 7.2 每变量每次访问都是装箱/拆箱
```
int a = 5;         // StrongBox<int> 分配在堆上
int b = a;         // COPY: 类型检查 → 拆箱 → 装箱 → 写堆
                   // 不是一条 CPU 指令！
```

### 7.3 EXTERN 是最昂贵的单指令
每次调用 Debug.Log、Animator.SetInteger、Networking.SetOwner 都要走完整的外部调用链。**热路径中应极度减少 EXTERN 调用频率。**

### 7.4 无寄存器、全栈式
所有操作通过栈传递堆地址，不能直接在寄存器中操作值。

### 7.5 10 秒硬限制
任何单次 Interpret 调用超过 10 秒 → Behaviour **永久停止** (`_hasError = true, enabled = false`)。

---

## 8. 对 UdonSharp 开发的工程启示

### 8.1 减少变量访问
每个变量的每次读/写都涉及 StrongBox 拆箱/装箱。合并频繁一起使用的变量到数组，批量操作。

### 8.2 减少 EXTERN 调用 (最重要!)
- 减少 `Debug.Log` 频率（每次都是完整 EXTERN）
- 缓存 `VRCPlayerApi` 引用（避免重复 GetComponent/GetPlayerById EXTERN）
- 批量 Animator 参数设置（而非分散调用）
- Update 中力避任何 EXTERN 调用

### 8.3 避免深层调用栈
每次方法调用 = 多次 PUSH/POP/COPY + EXTERN 或 JUMP。减少递归深度，避免长调用链。

### 8.4 事件驱动 > Update
Update 每帧执行解释循环。事件驱动只在需要时执行。从 VM 层面看，每个 `_update` 符号都会注册代理 + 每帧触发完整的 Interpret 流程。

### 8.5 单一 Interpret 调用的总指令数应 << 限值
虽然 10 秒看起来很宽裕，但解释执行 + 装箱拆箱 + EXTERN 让每指令的实际成本很高。复杂循环 + 大量 EXTERN 可以轻易逼近限值。

### 8.6 OPCode 计数估算
```
if (a > 0)        ≈ PUSH + EXTERN(>? ) + JUMP_IF_FALSE  ≈ 24 bytes
a = b + c;        ≈ PUSH×2 + EXTERN(+?) + COPY           ≈ ~40 bytes
数组访问 a[i]      ≈ PUSH + EXTERN(数组索引)               ≈ EXTERN 成本
```

**一个简单方法可能编译为 50-200 条 VM 指令。**

---

## 9. 相关知识

- `memory/api/events-reference.md` — Udon 事件完整参考
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制(本 VM 架构的直接结果)
- `memory/world/udon/vm-and-assembly.md` — **官方 Udon 字节码规范**(Udon Assembly 语法、9 Opcodes 完整说明、Extern 签名格式、Udon Types 命名规则)
- `memory/api/udon-type-exposure.md` — Udon 类型暴露规则
- `memory/world/udon/ui-events.md` — UI 事件白名单(EXEC 不经 Udon VM)
- `memory/world/udon/world-debug-views.md` — Debug 视图(含 Suffering 字段、Net Objects 统计)

### 双向对照表(本逆向分析 ↔ 官方字节码规范)

| 逆向分析(`udon-vm-architecture.md`) | 官方规范(`vm-and-assembly.md`) |
|--------------------------------------|--------------------------------|
| §1 9 Opcodes 表格 | §6 9 Opcodes 详细说明(含参数/堆栈语义) |
| §2 UdonHeap / LightweightStack | §4.2 数据段 / §5 代码段 |
| §3 EXTERN 调用链 | §6.2 EXTERN opcode 完整说明 |
| §4 Interpret 主循环 | §5.3 操作码参数规则 |
| §5 安全检查 | §11 风险与限制 |
| §6 事件系统 | §5.2 事件导出(`_onEnable`, `_start` 顺序) |

---

## 10. Udon 官方文档本地化索引(2026-06-15)

> 10 个 Udon 核心单页已本地化到 `memory/world/udon/`,跨引用如下:

| 主题 | 本地化文档 | VM 架构关联 |
|---|---|---|
| Udon 总览 | `memory/world/udon/index.md` | 9 Opcodes 概述、类型命名规则、this 含义 |
| **事件执行顺序** ⭐ | `memory/world/udon/event-execution-order.md` | `_onEnable → _start` 无间隔,RunEventAdvanced 时序 |
| Animation Events | `memory/world/udon/animation-events.md` | 12 个 EXTERN 入口(RunProgram/SendCustomEvent/Animator) |
| Avatar Events | `memory/world/udon/avatar-events.md` | OnAvatarChanged/OnAvatarEyeHeightChanged 时序 |
| Input Events | `memory/world/udon/input-events.md` | Button/Axis 事件签名,UdonInputEventArgs |
| External URLs | `memory/world/udon/external-urls.md` | VRCUrl 白名单 + 5s 限流 |
| Image Loading | `memory/world/udon/image-loading.md` | VRCImageDownloader EXTERN 链 |
| String Loading | `memory/world/udon/string-loading.md` | VRCStringDownloader EXTERN 链 |
| AI Navigation | `memory/world/udon/ai-navigation.md` | NavMeshAgent 集成 + Owner 计算 |
| Debugging Udon | `memory/world/udon/debugging-udon-projects.md` | 错误日志 + Halt 行为 + EXTERN Debug.Log 成本 |
