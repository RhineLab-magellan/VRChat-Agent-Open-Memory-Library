# VRChat-Agent-Open-Memory-Library

> 🧠 **VRChat 专属 AI Agent 开放记忆库** — 结构化、可验证、多领域的 VRChat 创作者知识体系

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Files: ~291](https://img.shields.io/badge/Files-~291-blue.svg)]()
[![Language: 中文](https://img.shields.io/badge/Language-中文-red.svg)]()

---

## 📖 简介

**VRChat-Agent-Open-Memory-Library** 是一个为 VRChat 创作者 AI Agent 设计的结构化知识库。它将 VRChat 官方文档、社区智慧、开源项目源码、以及资深创作者的实践经验，整合为一个**可被 AI Agent 直接检索与推理**的记忆系统。

本库不仅是"文档的堆砌"——每一份知识都经过**可信度分级**（Tier A~E）、**事实/推断标注**（FACT/INFERENCE）、以及**领域专家交叉验证**，确保 Agent 在生成代码或给出建议时，能区分"确定的事实"和"合理的推断"。

---

## 🎯 适用场景

| 场景 | 说明 |
|------|------|
| 🤖 **AI Agent 记忆后端** | 作为 VRChat 创作专用 Agent 的知识底座，为代码生成、问题诊断、设计建议提供依据 |
| 🔍 **创作者快速查阅** | 按领域索引快速定位 API 签名、设计模式、性能约束、常见陷阱 |
| 📝 **代码审查参考** | 15 项 UdonSharp 审查清单 + 32+ 失败案例 + 严重性分级模型 |
| 🏗️ **World 开发全流程** | 从 Udon 编程、网络同步、性能优化到光照烘焙、场景组件的完整知识链 |
| 👤 **Avatar 改模与优化** | Modular Avatar、VRCFury、AAO、lilToon 等核心工具的深度技术文档 |
| 🌐 **外部应用开发** | VRChat HTTP API / WebSocket / TypeScript SDK 完整参考（18 篇） |
| 📱 **跨平台适配** | Quest/Android 限制、移动 UI 优化、PC/Quest 自动切换策略 |
| 🔗 **Hybrid 系统集成** | OSC 协议数据库、AudioLink 音频可视化、Avatar↔World 交互模式 |

---

## 🗂️ 知识库结构

```
memory/
├── _always-load.md           # 🔴 Agent 启动必读：领域识别协议 + 30s 核心约束
├── FACT.md                   # 📋 长期事实库：架构决策 + 修正记录 + 绝对规则
├── index.md                  # 🧭 多领域路由地图：按需求快速定位到正确文件
├── JOURNAL.jsonl             # 📓 操作日志（结构化 JSONL）
│
├── world/          (~130 篇) # 🌍 World 领域 — 主力建设方向
│   ├── udon/                 #   Udon 编程（可视化 + C#）+ VM + 事件 + 调试
│   ├── scene-components/     #   9 个核心场景组件（镜像/传送门/桌台/站点…）
│   ├── examples/             #   SDK 内置示例拆解（13+ Prefab + Obstacle Course）
│   ├── bakery/               #   Bakery 光照烘焙指南
│   ├── shader/               #   GraphLit 节点编辑器
│   ├── clientsim/            #   ClientSim 编辑器模拟工具
│   └── *.md                  #   性能优化/光照/遮挡剔除/反射探针/图形 API…
│
├── avatar/         (~51 篇)  # 👤 Avatar 领域 — 改模与优化
│   ├── shader/               #   5 大着色器深度文档（lilToon 17篇/ORL/SCSS…）
│   ├── modular-avatar.md     #   Modular Avatar 完整参考（25+ 组件）
│   ├── vrcfury-reference.md  #   VRCFury 全组件清单 + 优化场景对比矩阵
│   └── *.md                  #   Animator/PhysBone/Constraint/优化/教学法…
│
├── api/            (~17 篇)  # 📚 API 参考 — UdonSharp 编程速查
│   ├── networking.md         #   网络同步 API（SetOwner/Serialization/NetworkEvent）
│   ├── udon-type-exposure.md #   1387 类型 / 9579 暴露 API 完整树索引
│   ├── not-exposed.md        #   未暴露 API 黑名单（List/Dict/LINQ/反射…）
│   └── *.md                  #   玩家/动画/音频/UI/持久化/拾取/事件…
│
├── rules/          (~8 篇)   # ⚖️ 规则系统 — 硬约束与强制要求
│   ├── networking-rules.md   #   网络同步 22 条规则
│   ├── udonsharp-language-limits.md # C# 语言限制 14 条
│   ├── performance-rules.md  #   性能优化 12 条规则
│   ├── multi-vm-rules.md     #   多 VM 协作 9 条规则
│   └── *.md                  #   VM 架构/深度陷阱/API 暴露判断…
│
├── patterns/       (~22 篇)  # 🎯 设计模式 — 可复用实现方案
│   ├── manual-sync-state.md          # 手动同步离散状态
│   ├── bit-packed-flags.md           # 位域压缩标志
│   ├── owner-authoritative-interaction.md # 所有者权威交互
│   ├── late-joiner-state-restore.md  # 延迟加入者状态恢复
│   ├── event-driven-state-machine.md # 事件驱动状态机
│   └── *.md                  #   Sardinal/LuraSwitch2/ULocalization 独有 Pattern…
│
├── hybrid/         (~4 篇)   # 🔗 Hybrid 领域 — 跨系统集成
│   ├── osc-protocol.md       #   OSC 完整协议数据库
│   ├── audio-link.md         #   AudioLink 音频可视化
│   └── udon-world-plugins.md #   推荐 Udon 世界插件索引
│
├── platform/       (~5 篇)   # 📱 Platform 领域 — 跨平台开发
│   ├── android-development.md    # Quest/Android 约束
│   ├── cross-platform-content.md # 跨平台资源策略
│   ├── mobile-ui-optimization.md # 移动端 UI 优化
│   └── easyquestswitch.md        # EasyQuestSwitch PC/Quest 切换
│
├── vrchatsdk/      (~19 篇)  # 🌐 VRChatSDK — HTTP API 完整参考
│   ├── 01_首页.md ~ 18_API_群组.md  # 用户/世界/Avatar/好友/实例/文件/群组 API
│   ├── 03_Websocket_API.md          # WebSocket 实时事件
│   └── 16~17_模型_*.md              # 数据模型定义
│
├── sources/        (~14 篇)  # 🔖 来源追踪 — 信息源分级
│   ├── sardinal.md           #   HoshinoLabs Sardinal 通用消息总线
│   ├── ulocalization.md      #   HoshinoLabs ULocalization 多语言
│   ├── vpm-package-template.md # VPM 包开发模板
│   └── *.md                  #   ClientSim/UdonVoiceUtils/LuraSwitch2…
│
├── reviews/        (~4 篇)   # ✅ 审查系统 — 质量标准
│   ├── review-checklist.md   #   15 项 UdonSharp 审查清单
│   ├── common-failures.md    #   32+ 已知失败模式
│   └── severity-model.md     #   严重性分级模型
│
├── references/     (~2 篇)   # 📎 参考资料 — 元数据与对比
├── misc/           (~4 篇)   # 📌 杂项 — 后处理/无障碍设计
└── journal/        (~8 篇)   # 📝 会话记忆 — 临时记录（定期清理）
```

---

## 🏷️ 知识分类体系

本库采用**多维度分类**，每份知识同时具备以下标签：

### 1. 领域分类（Domain）

| 域 | 图标 | 内容范围 | 文件数 |
|---|------|---------|--------|
| **World** | 🌍 | Udon 编程、网络同步、场景组件、性能优化、光照烘焙 | ~130 |
| **Avatar** | 👤 | Animator、PhysBone、Shader、MA/VRCFury/AAO 工具链、优化 | ~51 |
| **Hybrid** | 🔗 | OSC 协议、AudioLink、Avatar↔World 交互、MIDI | ~4 |
| **Platform** | 📱 | Quest/Android 开发、跨平台策略、移动 UI | ~5 |
| **VRChatSDK** | 🌐 | HTTP API、WebSocket、TypeScript SDK、数据模型 | ~19 |

### 2. 内容类型（Content Type）

| 类型 | 目录 | 说明 | 示例 |
|------|------|------|------|
| **规则 (Rules)** | `rules/` | 硬约束，违反即编译失败/崩溃/严重性能问题 | `networking-rules.md`（22 条） |
| **模式 (Patterns)** | `patterns/` | 可复用实现方案，含 Problem/Context/Solution/Tradeoffs | `manual-sync-state.md` |
| **API 参考 (API Ref)** | `api/` | 接口签名、暴露状态、热路径标记 | `networking.md` |
| **领域知识 (Domain)** | `world/` `avatar/` `hybrid/` `platform/` | 专题深度文档 | `modular-avatar.md` |
| **来源追踪 (Sources)** | `sources/` | 信息源分级与交叉验证 | `sardinal.md` |
| **审查标准 (Reviews)** | `reviews/` | 检查清单、失败模式、严重性模型 | `review-checklist.md` |
| **参考资料 (References)** | `references/` | 知识库与外部来源的差异对比 | `creator-docs-comparison.md` |
| **会话记忆 (Journal)** | `journal/` | 临时记录，定期清理（7~60 天） | 会话/审查/问题/草稿 |

### 3. 可信度分级（Credibility Tier）

| Tier | 级别 | 来源 | 处理方式 |
|------|------|------|---------|
| **A** | 官方规范 | VRChat 官方文档、官方源码、直接实验验证 | 直接采纳为 FACT |
| **B** | 官方发布 | SDK 内置示例、官方博客、Staff 发言 | 采纳但标注渠道 |
| **C** | 社区标准 | 高质量开源项目（如 lilToon, MA）、跨源验证一致的结论 | 采纳但标注项目来源 |
| **D** | 优秀案例 | 知名 World/Avatar 的实现分析 | 标注【参考案例】|
| **E** | 工程推理 | 基于 Tier A/B 知识 + 工程经验的逻辑推导 | 标注【推断】|

> **核心原则**：Agent 回答时必须区分 FACT（确定事实）和 INFERENCE（推断）。证据不足时输出 "Missing Information"，绝不强行回答。

---

## 🔑 核心特性

### 🧭 多领域路由系统

`index.md` 作为**路由地图**，Agent 在回答前先识别领域（World/Avatar/Hybrid/Platform），再定位到对应目录检索——避免跨域混淆。

### ⚡ 30 秒启动协议

`_always-load.md` 定义了 Agent **每次回答前必须执行的检查**：
- 领域识别（Avatar? World? Hybrid?）
- 知识优先级（L1 官方规范 > L5 工程推理）
- World 代码生成的 10 项硬约束（禁止 List/Dict/LINQ/async/coroutine…）
- 回答完整性自检

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

---

## 🚀 快速开始

### 用于 AI Agent

```yaml
# Agent 配置示例
memory_root: "memory/"
boot_files:
  - _always-load.md      # 启动协议（必读）
  - FACT.md              # 长期事实（必读）
  - index.md             # 路由地图（必读）
workflow:
  1. 领域识别 → 读 index.md
  2. 核心约束 → 读 _always-load.md
  3. 领域知识 → 按 index.md 路由到具体目录
  4. 规则检查 → 读 rules/
  5. 模式选择 → 读 patterns/
  6. API 速查 → 读 api/
  7. 代码审查 → 读 reviews/
```

### 用于人类创作者

| 我想做什么 | 从哪里开始 |
|-----------|-----------|
| 学习 Udon 编程 | `world/udon/index.md` → `world/udon/udonsharp/` |
| 解决网络同步问题 | `rules/networking-rules.md` → `patterns/manual-sync-state.md` |
| 优化 World 性能 | `rules/performance-rules.md` → `world/performance-guide.md` |
| Avatar 改模入门 | `avatar/modular-avatar.md` → `avatar/teaching-methodology.md` |
| 选择 Avatar Shader | `avatar/shader/index.md`（完整对比矩阵） |
| 审查 UdonSharp 代码 | `reviews/review-checklist.md` → `reviews/common-failures.md` |
| 开发外部应用 | `vrchatsdk/01_首页.md` → 按需查阅 API 文档 |
| Quest 适配 | `platform/android-development.md` → `platform/easyquestswitch.md` |
| 查阅 API 签名 | `api/` 目录 grep 关键词 |

---

## 📊 知识库数据来源

| 来源类别 | 具体来源 | 对应目录 |
|---------|---------|---------|
| 🏛️ **VRChat 官方** | Creator Docs、SDK 源码、Udon VM 规范 | `world/udon/` `api/` `rules/` |
| 🏛️ **VRChat API** | HTTP API 官方文档、WebSocket 规范 | `vrchatsdk/` |
| 🔧 **核心工具** | Modular Avatar、VRCFury、lilToon、AAO、ClientSim | `avatar/` `world/clientsim/` |
| 📦 **开源项目** | Sardinal、ULocalization、UdonVoiceUtils、LuraSwitch2 | `sources/` `patterns/` |
| 👥 **社区智慧** | VRCD 文档库、DeepWiki、Discord 讨论、创作者笔记 | `misc/` `references/` |
| ✍️ **作者实践** | Kuriko 个人笔记、项目经验、代码审查记录 | `reviews/` `journal/` |

---

## ⚠️ 核心约束速查

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

> 完整约束列表见 `_always-load.md` 和 `rules/` 目录。

---

## 📈 项目状态

| 指标 | 数值 |
|------|------|
| 📁 总文件数 | ~291 篇 Markdown |
| 📂 一级目录 | 14 个 |
| 🌍 最大领域 | World（~130 篇，45%） |
| 👤 第二大领域 | Avatar（~51 篇，18%） |
| 📅 最后更新 | 2026-06-20 |
| 🔄 更新频率 | 持续建设中 |
| 🌐 语言 | 中文为主，保留英文技术术语 |
| 📜 许可证 | MIT |

---

## 🤝 贡献指南

本库设计为 **AI Agent 优先**的知识系统。如果您希望贡献：

1. **知识贡献**：确保新知识附带 Source 标注和 Last Verified 日期
2. **可信度标注**：按 Tier A~E 分级，区分 FACT 和 INFERENCE
3. **交叉引用**：在相关文件间建立双向链接
4. **格式规范**：遵循现有文件的 Markdown 结构和元数据格式
5. **审查验证**：涉及代码模式的知识需经过至少一次实际项目验证

---

## 📝 许可

本项目采用 [MIT License](LICENSE) 开源。

**知识共享声明**：本库中的知识来源于 VRChat 官方文档、开源项目文档、社区公开讨论，以及作者的个人实践笔记。所有第三方知识均标注原始来源。如果您发现任何版权问题，请提交 Issue。

---

> 🧠 *"让 AI Agent 真正理解 VRChat 创作——不仅仅是代码补全，而是基于结构化知识的专业判断。"*
