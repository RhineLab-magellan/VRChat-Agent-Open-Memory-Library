---
title: UdonSharp Configuration
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udonsharp
  - udon

aliases:
  - "UdonSharp Configuration"

source: creators.vrchat.com/worlds/udon/udonsharp/configuration
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# UdonSharp Configuration

> Domain: World
> SDK Version: 3.10.x
> Last Updated (官方): 2024-08-06
> Last Updated (本地化): 2026-06-15
---

## Domain Detection

- **领域**: World
- **子领域**: UdonSharp 编辑器配置
- **核心服务对象**: U# 工程师 / 工具链维护者

---

## 概述

**【FACT】** UdonSharp 的所有设置位于：

```
Edit > Project Settings > Udon Sharp
```

> **【未确认】** 官方文档中提到的"Debug build / Inline Code / Listen for client exceptions"配置项可能因 SDK 版本不同而有所变化。

---

## 1. Udon Sharp 编译设置

### 1.1 Auto compile on modify（修改时自动编译）

**【FACT】** 启用后，脚本被修改并保存时**自动编译**。

| 推荐 | 场景 |
|------|------|
| ✅ 启用 | 日常开发，迭代速度快 |
| ❌ 关闭 | 大型项目、CI/批处理场景 |

### 1.2 Compile all script（编译所有脚本）

**【FACT】** 检测到 U# 脚本变更时，**编译所有脚本**（而非仅修改的脚本）。

**【推断】** 启用会增加编译时间但保证脚本间引用一致性。建议**保持启用**。

### 1.3 Compile on focus（聚焦时编译）

**【FACT】** 仅在编辑器**获得焦点**且脚本有变更时编译。

| 推荐 | 场景 |
|------|------|
| ✅ 启用 | 避免后台编译占用 CPU；外部编辑器（VSCode/Rider）保存时自动触发 |
| ❌ 关闭 | 仅在 Unity 内部编辑脚本 |

### 1.4 Script template override（脚本模板覆盖）

**【FACT】** 可定义**自定义模板**，创建 U# 脚本时使用该模板。

**使用方式**：
1. 创建模板脚本（包含 `<TemplateClassName>` 占位符）
2. 拖入 `Script template override` 字段

**默认模板**：

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class <TemplateClassName> : UdonSharpBehaviour
{
    void Start()
    {
        
    }
}
```

**【FACT】** `<TemplateClassName>` 会被替换为**文件名的类名**。

#### 推荐自定义模板

```csharp
// 团队模板示例：强制带 Header、namespace、Header 标记
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

namespace MyTeam.Worlds
{
    /// <summary>
    /// TODO: Add description
    /// </summary>
    [AddComponentMenu("MyTeam/<TemplateClassName>")]
    public class <TemplateClassName> : UdonSharpBehaviour
    {
        [Header("Settings")]
        
        private void Start()
        {
            
        }
    }
}
```

---

## 2. 调试设置（Debugging）

### 2.1 Debug build（调试构建）

**【FACT】** 启用/禁用 `Inline Code` 和 `Listen for client exceptions`。

**【推断】** 通常仅在**排查运行时问题**时启用，发布构建前关闭。

### 2.2 Inline Code（内联代码）

**【FACT】** 在生成的 Udon Assembly 中**包含 C# 内联代码**。

| 用途 | 说明 |
|------|------|
| 调试 | 错误堆栈可定位到 C# 源码行 |
| 反编译 | Udon Graph 视图可看到 C# 源码 |

**【R-LOW】** 启用会**增加程序集大小**，但不影响运行时性能（仅影响查看体验）。

### 2.3 Listen for client exceptions（监听客户端异常）

**【FACT】** 监听 VRChat 客户端输出日志中的**异常**，并尝试**匹配到项目中的脚本**。

**【FACT】** 设置方法见 [class-exposure-tree 文档](https://github.com/vrchat-community/UdonSharp/wiki/class-exposure-tree)。

> **【未确认】** 官方文档链接指向 GitHub Wiki 的 class-exposure-tree 页面（已迁移），实际可能是另一个调试配置文档。

**典型使用场景**：
- 玩家报告 World 崩溃
- 通过客户端日志反向定位 U# 脚本异常行
- 开发期 Debug 工具

---

## 3. 配置实践建议

### 3.1 个人开发

| 设置 | 推荐值 |
|------|--------|
| Auto compile on modify | ✅ 启用 |
| Compile all script | ✅ 启用 |
| Compile on focus | ✅ 启用（如使用外部 IDE）|
| Debug build | ❌ 关闭（除非调试）|
| Inline Code | ❌ 关闭（除非需要反编译）|
| Listen for client exceptions | ✅ 启用（开发期）|

### 3.2 团队 / 大型项目

| 设置 | 推荐值 |
|------|--------|
| Auto compile on modify | ⚠️ 部分启用（仅修改脚本后）|
| Compile all script | ✅ 启用（保证引用一致）|
| Compile on focus | ✅ 启用 |
| Script template override | ✅ 配置团队统一模板（namespace、Header 等）|

### 3.3 CI / 自动化构建

| 设置 | 推荐值 |
|------|--------|
| Auto compile on modify | ❌ 禁用 |
| Compile all script | ⚠️ 通过命令行/Editor 脚本手动触发 |

> **【推断】** CI 环境下应使用 `UdonSharpProgramAsset` 的**显式重编译**（Editor 脚本），避免依赖编辑器焦点。

---

## 4. 配置对工程的影响

### 4.1 编译产物

- **Program Asset**: UdonSharp 编译后的 Udon Assembly 容器
- **依赖关系**: Compile all script 确保所有引用都正确编译

### 4.2 编辑器性能

**【推断】** 大型项目（>50 U# 脚本）启用所有自动编译可能导致：
- 编辑器卡顿（编译期间）
- 频繁磁盘 IO
- 焦点切换时短暂卡顿

**优化方案**：
- 分模块开发
- 关闭 Compile on focus（仅在 Unity 内编辑时）
- 使用 VCC Package 拆分 ScriptableObject 配置

### 4.3 调试周期

| 场景 | 推荐配置组合 |
|------|------------|
| **快速迭代** | Auto + Compile all + Compile on focus ✅✅✅ |
| **稳定性优先** | Auto + Compile all ✅✅ |
| **详细调试** | + Debug build + Inline Code + Listen for exceptions |

---

## 5. 与已有知识库的关系

| 现有知识库 | 应补充/引用 |
|-----------|----------|
| `memory/api/udonsharp-runtime.md` | 编译管线与编辑器集成相关 |
| `memory/sources/vpm-package-template.md` | VPM Package 开发的 CI 配置参考 |
| `memory/rules/udonsharp-language-limits.md` | 编译错误处理与限制 |

---

## 6. 风险与未知

### 风险

- **【R-LOW】** Debug build / Inline Code 启用会**增加 Program Asset 体积**
- **【R-MED】** Listen for client exceptions 可能产生**大量日志噪音**（频繁匹配失败）
- **【R-MED】** 大型项目开启全部自动编译可能导致**编辑器卡顿**

### 未知

- **【未确认】** `Debug build` 在不同 SDK 版本下的具体行为
- **【未确认】** 是否有更细粒度的 per-script 编译控制（基于路径或命名空间）
- **【未确认】** Listen for client exceptions 的日志匹配机制（正则？精确匹配？）
