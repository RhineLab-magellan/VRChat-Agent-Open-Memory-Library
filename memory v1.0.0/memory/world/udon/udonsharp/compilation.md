# UdonSharp 编译管线

> Type: TECHNICAL REFERENCE
> Source: vrchat-community/UdonSharp (DeepWiki, commit 5d1a2b3d) + creators.vrchat.com/worlds/udon/udonsharp/
> Confidence: High
> SDK Version: VRChat SDK 3.x | UdonSharp 1.x
> Last Updated: 2026-06-15
> **迁移说明**: 本文档为 `world/udonsharp-compilation.md` 的权威位置

---

## 概述

UdonSharp 编译管线将 C# 源码转换为可执行 Udon Assembly 程序。该管线通过四阶段处理，将高级 C# 语法逐步转换为低级别 Udon 虚拟机指令。

---

## 四阶段编译流程

```
┌─────────────┐    ┌──────────────┐    ┌────────────┐    ┌───────────┐    ┌─────────────────┐
│   Setup     │ →  │    Roslyn    │ →  │    Bind    │ →  │    Emit   │ →  │ Udon Interface  │
│   Phase     │    │  Compilation │    │   Phase    │    │   Phase   │    │     Bridge      │
└─────────────┘    └──────────────┘    └────────────┘    └───────────┘    └─────────────────┘
```

---

## 1. Setup Phase（准备阶段）

### 核心任务
初始化编译上下文，加载 C# 源文件到 Roslyn 语法树。

### 关键数据结构

| 组件 | 用途 |
|------|------|
| `ModuleBinding` | 追踪每个源文件的编译产物 |
| `CSharpSyntaxTree` | Roslyn 解析的语法树（含预处理器符号） |
| `UdonSharpCompileOptions` | 编译配置和设置 |

### 源码
```csharp
CompilationContext.LoadSyntaxTreesAndCreateModules();
```

**特点**：源文件并行处理，提高大型项目编译速度。

---

## 2. Roslyn Compilation Phase（Roslyn 编译阶段）

### 核心任务
创建 `CSharpCompilation` 对象，执行标准 C# 编译流程。

### 处理内容
- 语义分析
- 类型检查
- 符号解析

### 关键映射

| 映射 | 方法 |
|------|------|
| ISymbol → UdonSharp Symbol | `CompilationContext.GetSymbol` |
| ITypeSymbol → TypeSymbol | `CompilationContext.GetTypeSymbol` |
| 外部程序集加载 | `GetMetadataReferences` |

---

## 3. Bind Phase（绑定阶段）

### 核心任务
遍历 Roslyn 语法树，创建语义验证后的 BoundNode 树。

### 核心组件
`BinderSyntaxVisitor` — 将语法节点转换为 BoundNode 对象。

### 关键操作

| 操作 | 输入 | 输出 |
|------|------|------|
| `VisitAccessExpression` | 成员访问语法 | `BoundAccessExpression` |
| `VisitInvocationExpression` | 方法调用语法 | `BoundInvocationExpression` |
| `VisitLiteralExpression` | 字面量 | `BoundConstantExpression` |
| `VisitAssignmentExpression` | 赋值语法 | Assignment bound nodes |

### 处理内容
- 符号引用解析
- 类型检查
- 语法树 → 抽象语法树转换

---

## 4. Emit Phase（发射阶段）

### 核心任务
从 BoundNode 树生成 Udon Assembly 代码。

### 核心组件：EmitContext

| 组件 | 用途 | 关键方法 |
|------|------|---------|
| `ValueTable` | 变量分配和生命周期管理 | `CreateInternalValue`, `GetUserValue` |
| `AssemblyModule` | 指令发射和方法链接 | `AddCopy`, `AddPush`, `AddJump` |
| `MethodLinkage` | 方法调用解析和参数传递 | `GetMethodLinkage` |
| `AssemblyDebugInfo` | 调试信息生成 | `UpdateSyntaxNode` |

### 方法发射流程

```
1. Root Method Emission     → 基类到派生类顺序处理所有虚方法
2. Dependency Resolution    → 发射已发射方法引用的方法
3. Recursive Processing     → 循环直到所有依赖解决
4. Export Generation        → 为 public 和 event 方法创建导出
```

---

## 5. Udon Interface Bridge（Udon 接口桥接）

### 核心任务
将 UASM 代码组装为 `IUdonProgram` 对象。

### 核心组件：CompilerUdonInterface

| 组件 | 用途 | 策略 |
|------|------|------|
| `IUAssemblyAssembler` | UASM → IUdonProgram | 池化实例复用 |
| `HeapFactory` | Udon 堆分配管理 | 每个程序可配置堆大小 |
| `UdonEditorInterface` | Udon API 定义 | 节点定义缓存 |

---

## 错误处理与诊断

### CompilationContext.Diagnostics 系统

编译管线在所有阶段收集错误：

| 阶段 | 常见错误类型 | 示例 |
|------|-------------|------|
| Setup | 文件 I/O、语法错误 | 源文件缺失 |
| Roslyn | C# 编译错误 | 类型解析失败 |
| Bind | UdonSharp 特定限制 | 泛型方法不支持 |
| Emit | Udon 兼容性 | 不支持的 API 调用 |

---

## 对开发者的意义

### 编译时间优化
- 源文件并行处理
- 方法按依赖顺序发射
- 增量编译支持

### 调试编译问题
- 查看具体阶段的诊断信息
- 定位绑定期的类型问题
- 识别不支持的 C# 特性

### 性能考量
- 复杂泛型 → Bind 阶段报错
- 不支持的方法调用 → Emit 阶段报错
- 预处理器符号影响语法树

---

## 相关文档

- `memory/world/udon/udonsharp/index.md` — UdonSharp 总览
- `memory/world/udon/udonsharp/configuration.md` — UdonSharp 配置
- `memory/world/udon/udonsharp/attributes.md` — UdonSharp Attributes
- `memory/world/udon/udonsharp/performance-tips.md` — 性能优化
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制
- `memory/rules/udon-vm-architecture.md` — Udon VM 架构
- `memory/api/udonsharp-runtime.md` — UdonSharpBehaviour 运行时系统
- `memory/world/udon/vm-and-assembly.md` — Udon 字节码规范

---

## 迁移历史

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-06-15 | 迁移 | 从 `world/udonsharp-compilation.md` 整合到本文件 |
| 2026-06-10 | 创建 | 原始 `world/udonsharp-compilation.md` 文档 |
