# VRChat-Agent-Open-Memory-Library

> 🧠 **VRChat 专属 AI Agent 开放记忆库 v3.0.0** — Agent 身份驱动 · 结构化 · 可验证 · 多领域的 VRChat 创作者知识体系

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version: v3.0.0](https://img.shields.io/badge/Version-v3.0.0-blue.svg)](CHANGELOG.md)
[![Files: ~351](https://img.shields.io/badge/Files-~351-blue.svg)]()
[![Language: 中文](https://img.shields.io/badge/Language-中文-red.svg)]()
[![Architecture: SOUL+Memory](https://img.shields.io/badge/Architecture-SOUL+Memory-purple.svg)]()
[![Quality: 100% YAML Coverage](https://img.shields.io/badge/Quality-100%25_YAML_Coverage-brightgreen.svg)]()
[![Search: 99.6% Reachable](https://img.shields.io/badge/Search-99.6%25_Reachable-brightgreen.svg)]()

---

## 📖 简介

**VRChat-Agent-Open-Memory-Library v3.0.0** 是继 v2.0.0 架构性升级后的**内容规模化扩张与质量治理里程碑**。在 SOUL + Memory 双层架构基础上，完成了：

- **SOUL.md** — 定义 Agent 是谁、如何思考、如何工作（身份 · 人格 · 领域路由 · 6 工作模式 · 证据系统）
- **memory/** — 结构化知识库本体（**351 个** Markdown 文件，3.26 MB，覆盖 12 个域目录）
- **100% YAML frontmatter 覆盖** — 所有文档含标准化机器可解析元数据
- **99.6% 搜索可达率** — A20 实测 981 个问题跨 12 域可检索
- **0 死链** — A19 治理周期完成全库链接修复

在V1.0版本中SOUL没有承担导航功能所以并未纳入到体系中，V2.0版本为了进一步减少优化系统提示词占用，将SOUL纳入了设计流程中。V3.0 在成熟架构上大规模填充内容并建立完整治理闭环。

在实际使用时可以考虑将Soul文件加上自己的Agent身份做整合，在保留原有文件导航框架的基础上做升级

---

## 🏗️ v3.0.0 核心架构：Memory 

```
VRChat-Agent-Open-Memory-Library/
│
├── SOUL.md                   # 🧬 Agent 身份系统 (v3.0)
│   ├── Identity              #   Agent 角色定义与核心原则
│   ├── Personality           #   工程人格：客观克制 · 精确不迎合 · 教学适应性
│   ├── Domain Router         #   6 领域自动路由（Avatar/World/Hybrid/External/Research/Meta）
│   ├── Working Modes ×6      #   Architect / Engineer / Reviewer / Teacher / Researcher / Curator
│   ├── Evidence System       #   证据体系：[FACT] / [INFERENCE] / [UNKNOWN] / [CONFLICT]
│   ├── Failure Policy        #   知识不足时的安全降级策略
│   └── Retrieval Protocol    #   6 步知识检索协议
│
├── memory/                   # 📚 结构化知识库本体 (351 篇 / 3.26 MB)
│   ├── _always-load.md       #   🔴 运行资料：领域识别 + 30s 核心约束 + 回答前自检
│   ├── FACT.md               #   📋 基础引导：KB 架构 + 核心约束 + 修正记录
│   ├── index.md              #   🧭 文件索引：按需求快速定位
│   ├── JOURNAL.jsonl         #   📓 操作日志 (36+ 条记录)
│   │
│   ├── world/      (154 篇)  #   🌍 World 领域 — Udon/光照/烘焙/网络/持久化/示例
│   ├── avatar/     (75 篇)   #   👤 Avatar 领域 — 改模/优化/Shader(Poiyomi+lilToon+5种)
│   ├── api/        (18 篇)   #   📚 API 参考 — 网络/动画/音频/UI/持久化/类型暴露树
│   ├── rules/      (8 篇)    #   ⚖️ 规则系统 — 硬约束与强制要求
│   ├── patterns/   (22 篇)   #   🎯 设计模式 — 同步/状态机/位域/决策树
│   ├── hybrid/     (6 篇)    #   🔗 Hybrid 领域 — OSC/AudioLink/VCC/ALCOM
│   ├── platform/   (6 篇)    #   📱 Platform 领域 — Quest/跨平台/移动UI/Player Config
│   ├── vrchatsdk/  (19 篇)   #   🌐 VRChatSDK — HTTP API 完整参考
│   ├── sources/    (25 篇)   #   🔖 来源追踪 — 开源项目/VPM镜像站/ClientSim
│   ├── reviews/    (5 篇)    #   ✅ 审查系统 — 15 项清单 + 32+ 失败案例 + 严重性模型
│   ├── references/ (2 篇)    #   📎 参考资料 — 元数据与对比
│   ├── misc/       (4 篇)    #   📌 杂项 — 后处理/无障碍
│   │
│   ├── meta/       (3 篇)    #   🛠️ 知识库治理体系
│   │   ├── kb-protocol.md    #   知识写入流程 + 维护协议 + 审计标准
│   │   ├── working-modes.md  #   6 工作模式完整定义
│   │   └── auxiliary-scripts.md # 5 个维护脚本清单
│   │
│   └── _curator_tools/       #   🔮 策展工具预留目录 (A19 治理脚本)
│
├── memory v1.0.0/            # 📦 v1.0.0 归档
├── memory v3.0.0/            # ⭐ v3.0.0 主工作目录 (SOUL.md + memory/)
├── CHANGELOG.md              # 📝 版本更新日志
├── LICENSE                   # 📜 MIT License
└── README.md                 # 📖 本文件
```

---

## 📋 核心文件角色速查

| 文件 | 角色 | 谁读取 | 何时读取 |
|------|------|--------|---------|
| **`SOUL.md`** | Agent 身份与行为准则 | Agent 系统 | 会话初始化时加载为 System Prompt |
| **`memory/_always-load.md`** | 跨域核心约束 + 自检清单 | Agent | **每次回答前必读**（30s 速查） |
| **`memory/FACT.md`** | KB 架构、长期事实、修正记录 | Agent + 维护者 | 会话初始化 + 知识库维护 |
| **`memory/index.md`** | 多领域路由地图 + 完整文件清单 | Agent | 领域识别后，定位具体知识文件 |
| **`memory/JOURNAL.jsonl`** | 结构化操作日志 | Curator 模式 | 知识写入 / 审计回溯 |
| **`memory/meta/kb-protocol.md`** | 知识写入流程与维护协议 | Curator 模式 | 知识库维护操作 |
| **`memory/meta/working-modes.md`** | 6 工作模式完整定义 | 全部模式 | 模式触发时加载 |
| **`memory/meta/auxiliary-scripts.md`** | 维护脚本清单与运行顺序 | Curator 模式 | 定期维护 |

---

## 🔌 不同 Agent 系统加载方式

本库设计为 **平台无关**，可适配多种 AI Agent 系统。以下是各平台的推荐加载方案：

### 1. GitHub Copilot (VS Code)

```
直接在 VS Code 中打开本仓库作为 workspace。
Copilot 自动将 SOUL.md 和 memory/ 作为上下文加载。
```

**配置方式**：无需额外配置，workspace 内的 `.md` 文件自动纳入上下文。可通过 `.github/copilot-instructions.md` 显式指定 `SOUL.md` 为 System Prompt。

### 2. Cursor / Claude Code

```yaml
# .cursorrules 或 CLAUDE.md
# 将 SOUL.md 作为 Project Instructions
instructions: SOUL.md
memory_root: memory/
```

或在项目根目录放置 `AGENTS.md` / `CLAUDE.md`，内容指向 `SOUL.md`。

### 3. Cherry Studio / 自定义 Agent

```markdown
# Agent 配置
System Prompt = 读取 SOUL.md 全文
Memory Root = memory/
启动文件 = _always-load.md, FACT.md, index.md
```

直接将 `SOUL.md` 内容复制到 Agent 的 System Prompt 字段，`memory/` 目录作为知识库附加文件。

### 4. 通用 LLM Chat (ChatGPT / Claude Web / DeepSeek) <- 不推荐

```markdown
# 手动加载流程
1. 复制 SOUL.md 全文 → 粘贴到对话开头作为 System Prompt
2. 附加 _always-load.md（核心约束）
3. 按需附加 index.md（路由地图）或具体域文件
```

> ⚠️ 通用 Chat 上下文窗口有限，建议按需加载具体域文件，不要一次加载全部 313 个文件。

### 5. OpenAI Custom GPT / Claude Project

```
将 SOUL.md 设为 Instructions
将 memory/ 目录上传为 Knowledge files
在 Instructions 中引用 memory/index.md 作为路由入口
```

---

## 🗂️ 知识库结构

---

## 🏷️ 知识分类体系

本库采用 **三维分类**，每份知识同时具备以下标签：

### 1. 领域分类（Domain）

| 域 | 图标 | 内容范围 | 文件数 |
|---|------|---------|--------|
| **World** | 🌍 | Udon 编程、网络同步、场景组件、性能优化、光照烘焙、VRCTween、Persistence、示例场景 | 154 |
| **Avatar** | 👤 | Animator、PhysBone、Shader (Poiyomi/lilToon/SCSS/ORL/Filamented/UnlitWF)、MA/VRCFury 工具链、优化、信任与安全 | 75 |
| **Sources** | 🔖 | 信息源分级、开源项目、VPM 镜像站完整数据 (57 仓库)、ClientSim | 25 |
| **Patterns** | 🎯 | 可复用设计模式（同步/状态机/位域/决策树）| 22 |
| **VRChatSDK** | 🌐 | HTTP API、WebSocket、TypeScript SDK、数据模型 | 19 |
| **API** | 📚 | 网络/玩家/动画/音频/UI/持久化 API 签名 + 类型暴露树 | 18 |
| **Rules** | ⚖️ | 硬约束（语言限制/网络/性能/VM 架构/深度陷阱）| 8 |
| **Misc** | 📌 | 后处理、无障碍指南 | 4 |
| **Hybrid** | 🔗 | OSC 协议 (32KB 完整版)、AudioLink、VCC/ALCOM 项目管理 | 6 |
| **Platform** | 📱 | Quest/Android 开发、跨平台策略、移动 UI、Player Config | 6 |
| **Reviews** | ✅ | 审查清单、32+ 失败案例、严重性模型、整合计划 | 5 |
| **Meta** | 🛠️ | 知识库治理（写入协议/工作模式/维护脚本）| 3 |
| **References** | 📎 | 官方文档对比、知识源对照 | 2 |

### 2. 可信度分级（Credibility Tier）

| Tier | 级别 | 来源 | 处理方式 |
|------|------|------|---------|
| **A** | 官方规范 | VRChat 官方文档、官方源码、直接实验验证 | 直接采纳为 FACT |
| **B** | 官方发布 | SDK 内置示例、官方博客、Staff 发言 | 采纳但标注渠道 |
| **C** | 社区标准 | 高质量开源项目（如 lilToon, MA）、跨源验证一致的结论 | 采纳但标注项目来源 |
| **D** | 优秀案例 | 知名 World/Avatar 的实现分析 | 标注【参考案例】|
| **E** | 工程推理 | 基于 Tier A/B 知识 + 工程经验的逻辑推导 | 标注【推断】|

### 3. YAML 元数据标准化（v2.0.0 新增）

每个核心文件头部包含标准化 YAML frontmatter：

```yaml
---
title: 文档标题
category: world | avatar | api | rules | patterns | ...
knowledge_level: applied | theoretical | reference
status: active | draft | deprecated
tags: [tag1, tag2, ...]
aliases: [别名1, 别名2]
related: [关联文件路径]
source: 知识来源
source_type: official | community | inference
version: 1.0
last_review: 2026-06-21
confidence: High | Medium | Low
---
```

> 此元数据层使知识库可被机器解析，支持自动化审计（`validation_script.py`）、链接健康检查（`url_health_check.py`）等维护操作。v3.0.0 已实现 **100% 文件含完整 YAML frontmatter**，为向量化/RAG 摄入提供标准化元数据层。

---

## 🧬 SOUL.md — Agent 身份系统详解

`SOUL.md` 是 v2.0.0 的核心创新。它定义了 Agent 的 **完整行为框架**：

### 6 工作模式（Auto-Select）

| Mode | 职责 | 触发场景 |
|------|------|---------|
| **Architect** | 项目架构、系统设计、网络拓扑、技术选型 | 新项目启动、大规模重构 |
| **Engineer** | UdonSharp 实现、Avatar 构建、功能开发、Bug 修复 | 具体功能实现 |
| **Reviewer** | 代码审查、性能审计、资源审查、安全评估 | 代码审查、性能分析 |
| **Teacher** | 改模教学、工具使用引导、问题诊断 | 新手引导、改模问题 |
| **Researcher** | 案例研究匹配、模式检索、插件评估 | 技术调研、方案对比 |
| **Curator** | 知识库审计、修复、补全（内部触发） | 知识库维护 |

### 证据系统（Evidence System）

```
[FACT]      知识库明确存在 → 标注来源文件 + 章节
[INFERENCE] 基于 FACT 推导 → 必须标注【推断】
[UNKNOWN]   证据不足 → 必须标注【未确认】+ Missing Information
[CONFLICT]  多来源矛盾 → 标注冲突双方 + 采用较新版本 + 建议验证
```

### 6 步知识检索协议

```
1. Domain Detection → 匹配 Domain Router
2. 读 memory/{domain}/index.md → 获取子目录和文件清单
3. 定位候选文档（最多 3 个）
4. 读取核心文档（每个 ≤ 200 行，优先读 §概述/§约束/§速查）
5. 知识充分性检查 → 不足则 Grep 扩展搜索（最多 1 轮）
6. 仍不充分 → 标注 [UNKNOWN] + Missing Information
```

---

## 🔑 核心特性

### 🧭 路由系统动态搜索

`index.md` 作为**路由地图**，Agent 在回答前先识别领域（World/Avatar/Hybrid/Platform/VRChatSDK），再定位到对应目录检索——避免跨域混淆。

### ⚡ 30 秒启动协议 - 本质与Skill类似

`_always-load.md` 定义了 Agent **每次回答前必须执行的检查**：
- 领域识别（Avatar? World? Hybrid?）
- 知识优先级（L1 官方规范 > L5 工程推理）
- World 代码生成的 10 项硬约束（禁止 List/Dict/LINQ/async/coroutine…）
- 回答完整性自检（FACT/INFERENCE 区分、风险标记、未知项标记）

### 🎯 UdonSharp 专项审查系统 

`reviews/` 目录提供完整的代码质量保障：
- **15 项检查清单**：继承、SyncMode、语言合规、网络同步、性能、安全
- **32+ 失败案例**：真实项目中的常见错误模式
- **4 级严重性模型**：致命/严重/警告/建议

### 🌐 设计模式决策树

`patterns/index.md` 包含**交互式决策树**，根据同步需求（连续/离散、Late Joiner、多人并发）自动路由到正确的设计模式。

### 📊 API 暴露状态追踪

`api/udon-type-exposure.md` + `api/exposed-types.md` + `api/not-exposed.md` 构成完整的 **Udon 类型暴露知识**：
- ✅ 1387 个类型暴露树（9579 个可用 API）
- ❌ 未暴露 API 黑名单（List/Dictionary/反射/线程/异常…）
- 🔧 API 检查器代码模式（静态分析用）

### 🛠️ 知识库治理体系 <- 当模型需要更新memory时的标准流程 - auxiliary-scripts指向Python脚本部分暂时缺失。

`memory/meta/` 目录定义了知识库的自我维护机制：

| 文件 | 内容 |
|------|------|
| `kb-protocol.md` | 知识写入流程（新发现→journal→具体文件→索引→核心约束→FACT）、维护协议（审计→分析→修复→验证→记录）、审计得分标准（A:90+ / B:78 / C/D） |
| `working-modes.md` | 6 种工作模式的完整定义，含触发场景、输出格式、核心知识、审查重点 |
| `auxiliary-scripts.md` | 5 个 Python 维护脚本（validation/governance/version_audit/url_health/pure_knowledge_audit）的用途与运行顺序 |

---

## 🚀 快速开始

### 用于 AI Agent

```yaml
# Agent 配置示例
system_prompt: "SOUL.md"                # Agent 身份与行为准则
memory_root: "memory/"
boot_files:
  - memory/_always-load.md              # 启动协议（每次回答前必读）
  - memory/FACT.md                      # 长期事实（会话初始化）
  - memory/index.md                     # 路由地图（领域识别后）
workflow:
  1. 加载 SOUL.md 作为 System Prompt
  2. 领域识别 → 读 memory/index.md
  3. 核心约束 → 读 memory/_always-load.md
  4. 领域知识 → 按 index.md 路由到具体目录
  5. 规则检查 → 读 memory/rules/
  6. 模式选择 → 读 memory/patterns/
  7. API 速查 → 读 memory/api/
  8. 代码审查 → 读 memory/reviews/
```

### 用于人类创作者

| 我想做什么 | 从哪里开始 |
|-----------|-----------|
| 学习 Udon 编程 | `memory/world/udon/index.md` → `memory/world/udon/udonsharp/` |
| 解决网络同步问题 | `memory/rules/networking-rules.md` → `memory/patterns/manual-sync-state.md` |
| 优化 World 性能 | `memory/rules/performance-rules.md` → `memory/world/performance-guide.md` |
| Avatar 改模入门 | `memory/avatar/modular-avatar.md` → `memory/avatar/teaching-methodology.md` |
| 选择 Avatar Shader | `memory/avatar/shader/index.md`（Poiyomi/lilToon/SCSS/ORL/Filamented/UnlitWF 对比矩阵） |
| Poiyomi Shader 学习 | `memory/avatar/shader/poiyomi/index.md`（8 主题知识文档） |
| 审查 UdonSharp 代码 | `memory/reviews/review-checklist.md` → `memory/reviews/common-failures.md` |
| 开发外部应用 | `memory/vrchatsdk/index.md` → 按需查阅 API 文档 |
| Quest 适配 | `memory/platform/android-development.md` → `memory/platform/easyquestswitch.md` |
| 管理 VCC/ALCOM 项目 | `memory/hybrid/vcc.md` → `memory/hybrid/alcom.md` |
| 查阅 API 签名 | `memory/api/` 目录 grep 关键词 |
| 了解 OSC 协议 | `memory/hybrid/osc-protocol.md`（32KB 完整版，含 8 附录） |

---

## ⚠️ 核心约束速查 --该部分主要来自工程实践总结

> 以下为 VRChat World/Avatar 开发的**绝对红线**，Agent 和创作者在使用本库时必须遵守：

| # | 约束 | 后果 |
|---|------|------|
| 1 | **只支持 BRP 渲染管线**（禁止 URP/HDRP） | 项目完全无法工作 |
| 2 | Editor 脚本必须放在 `Editor` 文件夹内 | 跨平台构建失败 |
| 3 | Unity 版本锁定 2022.3.22f1 LTS | 版本不兼容 |
| 4 | 禁止 List/Dictionary/LINQ/lambda | Udon VM 不支持 |
| 5 | 禁止 async/await/try-catch/coroutine | Udon VM 不支持 |
| 6 | 非 Owner 禁止写入 UdonSynced 变量 | 同步数据被覆盖 |
| 7 | Manual Sync 必须调 RequestSerialization() | 数据永不发送 |
| 8 | Update 中禁止 GetComponent/Find | 严重性能问题 |
| 9 | 同步 String/DisplayName 需特殊处理 | 带宽浪费 |
| 10 | Enum 比较必须 cast 到 int | 装箱导致 GC |

> 完整约束列表见 `memory/_always-load.md` 和 `memory/rules/` 目录。

---

## 🆕 v3.0.0 核心新增

v3.0.0 在 v2.0.0 成熟架构基础上进行了大规模内容扩张和质量治理：

| 新增内容 | 规模 | 说明 |
|----------|------|------|
| 🎨 **Poiyomi Shaders** | 8 主题 + 65 原始文档 | 五大变体、AudioLink 集成、Modular System、9 种 Lighting Type、Quest 优化 |
| 👤 **玩家操作知识库** | 6 新建 + 2 修改 | Trust Rank、Safety System、Skeletal Input、标准手姿、Expression Menu、Launch Options |
| 🔧 **VCC / ALCOM** | 2 篇系统化文档 | VCC 架构/工作流/VPM 格式 + ALCOM 开源替代 (Rust+Tauri, MIT) |
| 📡 **OSC 协议重大更新** | 23→32KB (+40%) | Chatbox 3 参数修正、10+ 核心补充、6 行为细节、资源分类索引 |
| 📦 **VPM 镜像站数据** | 12 篇 + 57 仓库 JSON | vcc.vrczh.org 全量数据，含 8 大核心包详细分析 |
| 🌍 **Community Labs / Companions / Steam Audio** | 3 篇新建 | World 发布流程、Items 分裂、2025.4.2+ 音频迁移 |
| 📹 **VRCCameraSettings / VRCQualitySettings** | 2 篇新建 | 屏幕/手持相机 + VR 双眼、阴影距离覆盖 |
| 🛡️ **A18/A19 治理闭环** | 0 死链 / 100% YAML | 351 篇全部通过验证，26 死链清零，搜索可达率 99.6% |

---

## 📊 知识库数据来源

| 来源类别 | 具体来源 | 对应目录 |
|---------|---------|---------|
| 🏛️ **VRChat 官方** | Creator Docs、SDK 源码、Udon VM 规范、Release Notes (171 篇) | `world/udon/` `api/` `rules/` |
| 🏛️ **VRChat API** | HTTP API 官方文档、WebSocket 规范 | `vrchatsdk/` |
| 🔧 **核心工具** | Modular Avatar、VRCFury、lilToon (17 篇)、Poiyomi (9 篇)、AAO、ClientSim、VCC/ALCOM | `avatar/` `world/clientsim/` `hybrid/` |
| 📦 **开源项目** | Sardinal、ULocalization、UdonVoiceUtils、LuraSwitch2、VizVid、VPM 镜像站 (57 仓库) | `sources/` `patterns/` |
| 👥 **社区智慧** | VRCD 文档库、DeepWiki、Discord 讨论、创作者笔记、Booth 数据库 | `misc/` `references/` |
| ✍️ **开发实践** | 个人笔记、项目经验、代码审查记录、A18/A19/A20 治理报告 | `reviews/` `journal/` |

---

## 📈 项目状态

| 指标 | v3.0.0 | v2.0.0 | v1.0.0 |
|------|--------|--------|--------|
| 📁 总文件数 | **351** | 313 | 295 |
| 📂 总大小 | **~3.26 MB** | ~2.8 MB | ~2.5 MB |
| 🌍 最大领域 | World（154 篇，44%） | World（149 篇，48%） | World（~130 篇） |
| 🆕 新增目录 | VPM 镜像站数据、Shader 子域扩展 | `meta/` `_curator_tools/` | — |
| 🆕 新增系统 | A18/A19 治理闭环、99.6% 搜索可达 | SOUL.md + YAML 标准化 | — |
| ✅ YAML 覆盖率 | **100%** (351/351) | ~95% | 0% |
| 🔗 死链数 | **0** | ~26 | 未知 |
| 📅 更新日期 | 2026-07-01 | 2026-06-21 | 2026-06-20 |
| 🔄 更新频率 | 持续建设中（A19 治理完成） | 持续建设中 | — |
| 🌐 语言 | 中文为主，保留英文技术术语 | 同 | 同 |
| 📜 许可证 | MIT | MIT | MIT |

---

## 📝 版本历史

| 版本 | 日期 | 核心变化 |
|------|------|---------|
| **v3.0.0** | 2026-07-01 | 内容规模化扩张：Poiyomi Shaders 8 主题入库 + 玩家知识库导入 + VCC/ALCOM 系统化 + OSC 协议 40% 扩充 + VPM 镜像站 57 仓库数据。A18/A19 治理闭环：100% YAML 覆盖、0 死链、99.6% 搜索可达率。351 篇文档，3.26 MB。 |
| **v2.0.0** | 2026-06-21 | SOUL.md Agent 身份系统 + YAML 元数据标准化 + meta/ 治理体系 + VRCTween/Persistence 新增 |
| **v1.0.0** | 2026-06-20 | 初始版本，295 文件，6 大领域知识库 |

> 详细变更见 [CHANGELOG.md](CHANGELOG.md)

---

## 🤝 贡献指南

本库设计为 **AI Agent 优先**的知识系统。如果您希望对本仓库贡献，请在Training data文件夹中 打包上传以下资料:

1. **原始知识文件**：如官方文档/个人笔记/QA文档/工程 等资料
2. **可信度标注**：按 Tier A~E 分级，区分 FACT 和 INFERENCE
3. **YAML 元数据**：遵循 `meta/kb-protocol.md` 中的 frontmatter 规范
4. **交叉引用**：在相关文件间建立双向链接
5. **格式规范**：遵循现有文件的 Markdown 结构和元数据格式
6. **审查验证**：资料类文档确认内容的正确性，工程类需要确定在最新版SDK是否能够运行。

或者 请加入QQ群聊：

```
902222352
```

打包提供 上述文件 并且详细叙述知识来源的可靠性以及您的人工审查结论。


如果采用则会由Master进行二次审查与模型自审，确定置信度后再决定是否纳入知识库体系中。

---

## 📝 许可

本项目采用 [MIT License](LICENSE) 开源。

**知识共享声明**：本库中的知识来源于 VRChat 官方文档、开源项目文档、社区公开讨论，以及作者的个人实践笔记。所有第三方知识均标注原始来源。如果您发现任何版权问题，请提交 Issue。

---
