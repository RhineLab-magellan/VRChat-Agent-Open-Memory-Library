---
title: "UdonSharp - VRChat SDK C# 编程前端"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "creators.vrchat.com/worlds/udon/udonsharp/"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - misc
  - index
  - navigation
aliases:
  - "UdonSharp - VRChat SDK C# 编程前端"
  - index
related:
  - attributes.md
  - configuration.md
  - editorscripting.md
  - performance-tips.md
---
# UdonSharp - VRChat SDK C# 编程前端

> Domain: World
> SDK Version: 3.10.x (持续更新)
> Last Updated (官方): 2026-02-26
> Last Updated (本地化): 2026-06-15
---

## 概述

**UdonSharp**（简称 U#）是 VRChat Worlds SDK 内置的 C# 编程前端，允许开发者使用 C# 编写 Udon 脚本，编译时自动转译为 Udon Assembly / Udon Bytecode，运行在 Udon VM 中。

**核心定位**：
- C# 语法作为前端表达 → Udon Assembly 作为后端产物
- 与 Udon Graph（节点编辑器）功能等价但更适合复杂逻辑
- 包含在 VRChat Worlds SDK 中，无需独立安装

**子页面导航**：
- [`attributes.md`](./attributes.md) — U# 专用 Attribute（UdonSynced、UdonBehaviourSyncMode、UdonSyncMode、BehaviourSyncMode）
- [`configuration.md`](./configuration.md) — Project Settings > Udon Sharp 配置
- [`editorscripting.md`](./editorscripting.md) — 自定义 Inspector、Proxies、Editor 工具
- [`performance-tips.md`](./performance-tips.md) — 性能优化关键提示

> **注**：`class-exposure-tree`（类暴露树）已本地化到 `memory/api/udon-type-exposure.md`，本目录不重复创建。

---

## Domain Detection

- **领域**: World
- **子领域**: Udon VM / 脚本层
- **身份**: World Technical Director
- **核心服务对象**: U# 工程师

---

## 1. 如何创建 UdonSharp 脚本

### 1.1 通过 Project 窗口

1. 在项目资源浏览器中右键
2. 导航到 `Create` → `U# script`
3. 点击 `U# script`，打开文件创建对话框
4. 输入脚本名并保存
5. 完成后在同目录生成两个文件：
   - **UdonSharp Program Asset**（一般无需手动编辑）
   - **`.cs` 文件**（类继承自 `UdonSharpBehaviour`）

### 1.2 通过 Hierarchy 窗口

1. 在场景中创建新 GameObject
2. 添加 `Udon Behaviour` 组件
3. 点击 `New Program` 按钮旁的下拉菜单，选择 `Udon C# Program Asset`
4. 点击 `New Program` 创建 Program Asset
5. 点击 `Create Script` 选择保存位置和脚本名

### 1.3 默认脚本模板

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class YourScriptName : UdonSharpBehaviour
{
    void Start()
    {
        
    }
}
```

> **【FACT】** 模板可自定义（见 `configuration.md` 的 Script template override）。

---

## 2. 支持的 C# 特性（Supported C# Features）

**【FACT - 官方文档】** UdonSharp 支持 C# 的绝大多数基础语法：

| 特性类别 | 支持项 |
|---------|--------|
| **流程控制** | `if`、`else`、`while`、`for`、`do`、`foreach`、`switch`、`return`、`break`、`continue`、三元运算符 `(condition ? true : false)`、`??`（null 合并） |
| **类型转换** | 隐式和显式类型转换 |
| **数组** | 数组、数组索引器、Jagged Arrays（锯齿数组） |
| **运算符** | 全部内置算术运算符 |
| **短路求值** | Conditional short circuit — `(true \|\| CheckIfTrue())` 不会执行 `CheckIfTrue()` |
| **typeof** | `typeof()` — 返回 U# 抽象类型 |
| **方法参数** | `out`、`ref`、extension methods、`params` |
| **用户方法** | 参数、返回值（out/ref/extension/params） |
| **静态方法** | 静态用户方法 |
| **继承** | UdonSharpBehaviour 继承、虚方法等 |
| **事件回调** | Unity/Udon 事件回调（带参），如 `OnPlayerJoined(VRCPlayerApi)` |
| **字符串插值** | `$"Player {name} joined"` 形式 |
| **字段初始化** | 字段初始化器（**编译时**执行，非运行时） |
| **跨类访问** | 跨 UdonSharpBehaviour 类访问字段、调用方法 |
| **递归** | 通过 `[RecursiveMethod]` attribute 启用 |

### 2.1 递归方法示例

```csharp
using UdonSharp;

public class RecursiveExample : UdonSharpBehaviour
{
    [RecursiveMethod]
    public int Factorial(int n)
    {
        if (n <= 1) return 1;
        return n * Factorial(n - 1);  // 递归调用需 [RecursiveMethod]
    }
}
```

> **【FACT】** 不标注 `[RecursiveMethod]` 的递归调用会编译失败。

---

## 3. 与 Unity/C# 的差异（Differences）

UdonSharp **不符合任何版本的 C# 语言规范**，部分 C# 特性未实现或无法工作。

### 3.1 关键差异列表

| 差异 | 说明 | 解决方案 |
|------|------|---------|
| **基类** | 最佳实践：继承 `UdonSharpBehaviour` 而非 `MonoBehaviour` | `public class X : UdonSharpBehaviour` |
| **`enabled` 状态** | 修改 `Behaviour` 类型字段的 `enabled` 对 `UdonSharpBehaviour` 无效 | 用具体 U# 脚本类型作为序列化字段 |
| **集合类** | 只支持数组 `[]` 和 [Data Containers](../data-containers/) | 用 `DataList` / `DataDictionary` 代替 `List<T>` / `Dictionary<K,V>` |
| **字段初始化** | 在**编译时**执行，不依赖场景中其他对象 | 依赖场景对象的初始化逻辑放在 `Start()` 中 |
| **网络同步** | 需要 `[UdonSynced]` attribute 标记字段 | 见 [`attributes.md`](./attributes.md) |
| **数值转换** | **有溢出检查**（UdonVM 限制） | 注意 `byte`/`short` 范围，使用显式转换时考虑溢出 |
| **GetType 抽象** | 返回 U# 抽象类型，不一定符合预期 | 例如 `int[][]` 的 `GetType()` 返回 `object[]` 而非 `int[][]` |

### 3.2 Jagged Array 类型抽象（关键细节）

```csharp
int[][] jagged = new int[3][];
Debug.Log(jagged.GetType().ToString());
// C# 期望输出: "int[][]"
// UdonSharp 实际输出: "object[]"  ← 抽象后的类型
```

**【FACT】** 这是 Udon VM 抽象化的结果，可能影响依赖类型比较的代码（罕见场景）。

### 3.3 数值溢出检查

```csharp
byte b = 200;
b = (byte)(b + 100);  // C# 中: 44 (静默环绕)
// UdonSharp 中: 抛出异常 (Overflow check)
```

**【推断】** 字段累加、颜色通道计算等场景需注意 byte 范围。

---

## 4. 不支持的 C# 特性（FAQ 关键）

**【FACT - 官方 FAQ】** 学习 C# 教程时可能遇到但 U# 中**不可用**的常见特性：

| ❌ 不支持 | 说明 | 替代方案 |
|---------|------|---------|
| **Generic Classes** (`Class<T>`) | 泛型类 | 用具体类型或 `object` 数组 |
| **Generic Non-Static Methods** | 泛型非静态方法 | 同上 |
| **Interfaces** | 接口 | 抽象基类 |
| **Method Overloads** | 方法重载 | 不同方法名 |
| **Properties** | C# 属性 | 公共字段 + 显式 getter/setter 方法 |

> **【FACT】** 以上特性在 Udon VM 中**未实现**。强行使用会导致编译错误。

---

## 5. 示例脚本

### 5.1 旋转立方体示例（官方）

```csharp
using UnityEngine;
using UdonSharp;

public class RotatingCubeBehaviour : UdonSharpBehaviour
{
    private void Update()
    {
        transform.Rotate(Vector3.up, 90f * Time.deltaTime);
    }
}
```

### 5.2 其他示例来源

- **SDK 内置**: `Assets/UdonSharp/UtilityScripts`（可安全删除不用时）
- **GitHub Wiki**: https://github.com/vrchat-community/UdonSharp/wiki/examples
- **VRChat Creator Hub**: https://ask.vrchat.com/c/creator-hub/63/none

---

## 6. 常见问题（FAQ）

### Q1: UdonSharp 支持所有 Udon 特性吗？

**【FACT】** 是的。Udon 支持的所有功能 U# 都能访问。可通过 [Class Exposure Tree](https://github.com/MerlinVR/UdonSharp/wiki/class-exposure-tree) 验证（已本地化到 `memory/api/udon-type-exposure.md`）。

### Q2: 一个 GameObject 上能有多个 UdonSharp UdonBehavior 吗？

**【FACT】** 可以。

### Q3: C# 教程中哪些常见方面在 U# 中不工作？

见上文 §4 表格（Generic、Interface、Method Overload、Properties）。

---

## 7. 与已有知识库的关系

| 现有知识库 | 应补充/引用 |
|-----------|----------|
| `memory/api/udonsharp-runtime.md` | 引用 [`attributes.md`](./attributes.md)、[`performance-tips.md`](./performance-tips.md) |
| `memory/api/udon-type-exposure.md` | **互链** — 类暴露树的本地化位置 |
| `memory/api/exposed-types.md` | 引用本文 §2 Supported C# Features |
| `memory/api/not-exposed.md` | 引用本文 §3、§4 |
| `memory/rules/udonsharp-language-limits.md` | 引用 [`attributes.md`](./attributes.md)、[`performance-tips.md`](./performance-tips.md) |
| `memory/world/udon/vm-and-assembly.md` | 配合阅读（U# 是 C# 前端，VM 是运行时） |

---

## 8. 风险与未知

### 风险

- **【R-MED】** 字段初始化在编译时执行，若依赖场景对象，会导致 NullReferenceException
- **【R-MED】** 数值溢出检查可能让原本在 C# 中静默环绕的代码抛出异常
- **【R-LOW】** Jagged Array 的 `GetType()` 抽象可能影响反射逻辑

### 未知

- **【未确认】** `class-exposure-tree` 官方 URL 内容已迁移至 `memory/api/udon-type-exposure.md`，两者同步状态需定期验证
- **【未确认】** 官方文档未明确列出所有不支持的 C# 特性（如 `async/await`、`yield return`、`LINQ`），需通过实际编译验证
