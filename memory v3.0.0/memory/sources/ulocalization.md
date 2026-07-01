---
title: "ULocalization — 知识库溯源"
category: sources
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - sources
  - audio
  - event
  - udonsharp
aliases:
  - "ULocalization — 知识库溯源"
  - ulocalization
related:
  - sardinal.md
  - udonvoiceutils.md
  - community-notes.md
  - example-central.md
  - official-docs.md
---
# ULocalization — 知识库溯源

> **类型**: World 工具 / 适配层 (UdonSharp 包装 Unity Localization)
> **Tier**: A (作者活跃维护 + VPM 官方分发 + 高质量源码)
> **仓库**: https://github.com/ikuko/ULocalization
> **作者**: [@ikuko](https://x.com/magi_ikuko) (HoshinoLabs)
> **License**: MIT
> **最后查看**: 2026-06-20
> **SDK 版本**: VRChat SDK 3.10.x / UdonSharp 1.x / Unity 2022.3+
> **依赖**: `com.unity.localization`, `com.hoshinolabs.sardinal`, `com.hoshinolabs.sardinject`

---

## 项目概述

ULocalization 是 VRChat UdonSharp 的本地化系统，**不是从零构建的本地化系统**，而是**Unity 官方 Localization 系统的 UdonSharp 适配层**。

通过 **Sardinal（Signal/事件）+ Sardinject（DI 容器）+ 大量代码生成 + 哈希分派** 的组合，把 Unity Localization 的完整功能（StringTable / AssetTable / SmartFormat / PersistentVariables / Locale 切换）适配到 Udon VM 沙箱中执行。

**核心创新**：在 Udon 端实现了对 UnityEvent 的完整支持，绕过 Udon 沙箱的多个主要限制（无委托、无泛型方法、无反射、SendCustomEvent 无参数）。

---

## 核心功能

1. **Locale 管理**: 启动时可选 Locale（`IStartupLocaleSelector` 接口），运行时可切换
2. **本地化字符串**: `LocalizedString` + `LocalizeStringEvent`（支持 SmartFormat）
3. **本地化资产**: `LocalizedAudioClip` / `LocalizedTexture` / `LocalizedSprite` / `LocalizedOptionData` / `LocalizedOptionDataList`
4. **持久化变量**: 16 种 IVariable 类型（Bool/SByte/Byte/Short/UShort/Int/UInt/Long/ULong/String/Float/Double/Object + NestedVariablesGroup/VariablesGroupAsset）
5. **UnityEvent 集成**: 把 UnityEvent listener 在 Udon 端完整保留并分派
6. **Culture 感知格式化**: `.ToString(f, culture)` 支持地区格式
7. **VRCPlayerObject 克隆支持**: `CloneDetector` + `RenewPrefab` 重建引用

---

## 项目规模

| 指标 | 数值 |
|------|------|
| 总 .cs 文件 | 145 |
| Runtime 文件 | 107 |
| Runtime/Udon 文件 | 73 |
| Editor 文件 | 33 |
| Editor/Udon 文件 | 27 |
| Shim 字段数 | 27 (`_0` ~ `_26`) |
| 生成的 hash 方法数 | 500+ |
| 支持的 UnityEvent 目标类型 | 100+ |
| 支持的 IVariable 类型 | 16 + 4 扩展 |
| 支持的 LocalizeEvent 类型 | 5 |
| 支持的 LocalizedReference 类型 | 6 |
| `[RecursiveMethod]` 标注 | 6 处 |
| 同步模式 | `BehaviourSyncMode.None` |

---

## 关键学习点

### 1. Hash-Based Method Dispatch (哈希方法分派)

Udon 没有委托/函数指针，ULocalization 用 MD5(Type+Method) hash + 自动生成 wrapper 方法 + `SendCustomEvent(hash)` 间接分派。**完美绕过 Udon 限制，零反射开销**。

→ 沉淀到 `memory/patterns/hash-based-dispatch.md`

### 2. IID Object Identity (整数身份映射)

Udon 不能用 Dictionary 索引普通 C# 对象，ULocalization 用 Editor 端 `IID.GenerateId` 顺序分配 int，运行时所有引用通过 int 索引。跨 Build 引用稳定。

→ 沉淀到 `memory/patterns/iid-object-identity.md`

### 3. Slot-Based Parameter Passing (槽位参数传递)

`SendCustomEvent` 不接受参数，ULocalization 用 3 个 object 字段（`_l_t` / `_l_p` / `_l_a`）作为参数槽位，调用前手动填入，生成方法从槽位读取。

→ 沉淀到 `memory/patterns/slot-parameter-passing.md`

### 4. Code Generation with Type Erasure (代码生成 + 类型擦除)

Udon 没有泛型方法，ULocalization 用 Type.FullName MD5 hash 作为 type ID，每个具体类型生成 switch case + 元组模式（`object[2]` = `(shim, int id)`）实现类型安全。

→ 沉淀到 `memory/patterns/code-generation-type-erasure.md`

### 5. Build-Time vs Runtime Separation (构建时与运行时分离)

Unity Editor API 在 Udon 不可用，ULocalization 把所有反射/LINQ/缓存放到 Editor 端，注入 27 个字段到 Udon，运行时仅做 O(1) 查表。Build 阶段禁用并清理原始 LocalizeEvent。

→ 沉淀到 `memory/patterns/build-time-vs-runtime-separation.md`

### 6. God Shim 模式

单一 `LocalizationShim` 处理所有 LocalizeEvent / LocalizedString / Variable。Udon 限制下的不可避免选择。

### 7. SmartLiteFormatter (SmartFormat 子集)

Udon 不能直接调用 SmartFormat 库，重写最小子集（正则解析 + 16 个类型 case + Culture 感知）。

### 8. CloneDetector + RenewPrefab 机制

`VRCPlayerObject` 克隆后，原始 LocalizeEvent / Localized 引用失效。`CloneDetector` 在每个 PlayerObject 上自动 `RenewPrefab` 重建 int 索引。

---

## 知识提取记录（反向索引）

| 沉淀位置 | 提取内容 |
|----------|----------|
| `memory/FACT.md` § ULocalization(参考工程) | 5 大核心模式摘要 + 工程参数 |
| `memory/patterns/hash-based-dispatch.md` | 哈希分派完整模式 + 代码骨架 |
| `memory/patterns/iid-object-identity.md` | 整数身份映射完整模式 + 代码骨架 |
| `memory/patterns/slot-parameter-passing.md` | 槽位传参完整模式 + 代码骨架 |
| `memory/patterns/code-generation-type-erasure.md` | 代码生成 + 类型擦除完整模式 + 代码骨架 |
| `memory/patterns/build-time-vs-runtime-separation.md` | Build-Runtime 分离完整模式 + 代码骨架 |
| `memory/sources/open-source-projects.md` | A7 案例研究型参考工程条目 |
| `memory/sources/index.md` | 新来源登记 |
| `memory/patterns/index.md` | 14-18 号新模式 + 决策树更新 |
| *(Session 分析报告 V3.0 起写入 `特殊Agent提示词/`)* | 工作过程记录 |

---

## 元数据

| 字段 | 值 |
|------|-----|
| **Stars** | 100+ (在 sources/ 中保留，不外流) |
| **License** | MIT |
| **依赖** | com.unity.localization, com.hoshinolabs.sardinal, com.hoshinolabs.sardinject |
| **维护状态** | 活跃（VPM 分发 + GitHub Releases） |
| **首次分析** | 2026-06-20 |
| **最后更新** | 2026-06-20 |
| **分析覆盖** | 35+ 关键 .cs 文件深度阅读（Runtime/Editor 各 15+） |

---

## 相关项目

| 项目 | 关系 |
|------|------|
| `HoshinoLabs.Sardinal` | Signal 事件系统，被 Localization 用作 locale 变化通知 |
| `HoshinoLabs.Sardinject` | DI 容器，被 Localization 用作依赖注入和 Scene 容器 |
| `Unity Localization` | 底层本地化引擎，被 ULocalization 包装 |
| VRChat SDK | VRCPlayerObject / VRCObjectPool / VRCObjectSync 被 CloneDetector 引用 |

---

## 借鉴点总览

| 借鉴点 | 如何借鉴到自己的项目 |
|--------|---------------------|
| **Hash 命名方法** | 任何需要"动态分派"的 Udon 场景 |
| **IID 身份映射** | 需要持久化对象引用的所有场景 |
| **Slot 参数传递** | UnityEvent + Udon 的所有场景 |
| **Type-Erasure 元组** | Sardinject `ISerializable` 模式 |
| **Build 时清理** | 任何"接管原生组件"的 Udon 工具 |
| **代码生成工具** | Roslyn Source Generator / T4 模板 |
| **DI 容器选择** | 复杂 Udon 项目应引入 Sardinject |
| **依赖 Sardinal + Sardinject** | 高内聚的依赖组合 |
