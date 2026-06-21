---
title: ClientSim 知识库(项目仓库元数据)
category: sources

knowledge_level: applied
status: archived

tags:
  - sources
  - migrated

aliases:
  - "ClientSim 知识库(项目仓库元数据)"

related:
  - world/clientsim/index.md
  - world/clientsim/playerobject-editor.md
  - world/clientsim/playerdata-editor.md
  - world/clientsim/systems/index.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# ClientSim 知识库(项目仓库元数据)

> 来源: vrchat-community/ClientSim (DeepWiki 文档)
> 索引日期: 2026-06-10
> 原始仓库: github.com/vrchat-community/ClientSim
> Last indexed: 26 May 2025 (commit 2fc16f)

> ⚠️ **本文档定位**:ClientSim **项目仓库**元数据(发展历史、双向同步、贡献流程)。
> 配套的**用户使用文档**已迁移至 `memory/world/clientsim/`(2026-06-15):
> - [ClientSim 使用文档(用户视角)](../world/clientsim/index.md) - 5 大特性、4 个调试窗口、Networking 差异
> - [PlayerObject Editor](../world/clientsim/playerobject-editor.md) - 调试 PlayerObject
> - [PlayerData Editor](../world/clientsim/playerdata-editor.md) - 调试 PlayerData
> - [Systems(架构与子系统)](../world/clientsim/systems/index.md) - Observer + DI 架构、Script Execution Order

---

## 概述

ClientSim 是 VRChat 官方维护的 Unity 编辑器模拟工具，让开发者可以在不发布到 VRChat 的情况下测试 SDK3 世界。

### 核心定位

| 功能 | 说明 |
|------|------|
| 对象状态检查 | 实时查看对象属性和状态，直接调试 |
| 行为验证 | 测试 Udon 脚本和世界逻辑 |
| 事件模拟 | 模拟玩家交互和触发器 |
| 性能测试 | 发布前识别潜在问题 |

### 与 VRChat 关系

- **2025 年前**: 独立 Unity 包，Community 维护
- **2025 年后**: 集成到 VRChat SDK，官方维护
- **仓库**: `vrchat-community/ClientSim` (公仓) + VRChat 私有仓库 (内研)
- **双向同步**: 公仓与私有仓库保持同步

---

## 发展历史

### CyanEmu 时代

ClientSim 起源于社区项目 **CyanEmu**（CyanLaser 创建），提供：
- Unity Editor 集成模式
- VRChat 行为模拟算法
- 世界状态检查机制
- 玩家交互模拟框架

### ClientSim 诞生

CyanLaser 同时是 CyanEmu 和 ClientSim 的开发者，确保：
- 设计理念连续性
- 技术架构延续性
- 核心模拟原理增强

### VRChat 官方接管

- 获得官方支持
- 与 VRChat SDK3 深度集成
- 长期维护保障

---

## 仓库结构演变 (2025)

### 重构原因

ClientSim 被合并到 VRChat SDK，原有独立 Unity 项目结构变得过时。

### 主要变更

| 项目 | 重构前 | 重构后 |
|------|--------|--------|
| 结构 | 独立 Unity 项目 + 内嵌包 | 源码仓库 (Source/) |
| 文档 | 本地 `Documentation/` | 迁移至 Creator Docs |
| 测试 | Tests/ 文件夹 | 已移除 (功能异常) |
| 历史 | - | legacy 分支保留 |

### 文档迁移表

| 组件 | 旧位置 | 新位置 | 访问方式 |
|------|--------|--------|----------|
| API 文档 | Documentation/ | Creator Docs | Web |
| 使用示例 | 本地 md | Creator Docs | Web |
| 贡献指南 | 本地文件 | creator-docs 仓库 | PR |

### Legacy 分支

`legacy` 分支保留重构前的完整状态：
- 原始文档结构
- 测试套件实现
- Unity 项目配置
- 开发工具和实用程序

---

## 双向同步架构

### 同步组件

| 组件 | 公仓 | 私有仓 | 同步方向 |
|------|------|--------|----------|
| 源码 | Source/ | 内部源码树 | 双向 |
| 文档 | 已移除 | 内部文档 | 单向至 creator-docs |
| 测试 | 已移除 | 内部测试 | 私有 |
| 构建配置 | 存在 | 内部构建系统 | 双向 |
| Legacy | legacy 分支 | 不同步 | 仅公仓 |

### 同步触发器

- 合并到公仓 `main` 分支
- 私有仓库内部开发里程碑
- 冲突解决的手动同步
- 计划维护同步

### 贡献者可见性限制

| 方面 | 公仓可见性 | 私有仓 |
|------|------------|--------|
| 源码 | ✅ 完全可见 | 内部开发 |
| 测试套件 | ❌ 已移除 | 内部测试 |
| 文档 | ➡️ 迁移至 creator-docs | 内部文档 |
| 构建流程 | 🔧 部分 (仅配置) | 内部构建系统 |

---

## 开发环境要求

### 当前要求

| 组件 | 要求 | 说明 |
|------|------|------|
| Unity Editor | VRChat SDK 兼容版本 | 测试 ClientSim 功能 |
| VRChat SDK3 | 最新版本 | ClientSim 作为 SDK 的一部分 |
| 源码 | Source/ 目录内容 | 所有开发工作焦点 |
| 文档 | creator-docs 仓库 | 文档贡献 |

### 贡献流程

1. 所有代码更改必须在 `Source/` 目录
2. 通过 Pull Request 提交
3. VRChat 团队审查 PR
4. 批准后合并并同步到内部系统
5. 最终集成可能包含公仓不可见的修改

### 审查标准

- **代码质量**: 符合项目标准和可维护性
- **功能性**: 与 VRChat SDK3 和 Unity Editor 正确集成
- **兼容性**: 确保与内部 VRChat 系统兼容
- **文档**: 清晰说明更改及其影响

---

## ClientSim 已知限制

### 测试套件状态

| 问题 | 影响 | 状态 |
|------|------|------|
| 测试已移除 | 自动化测试能力下降 | 计划恢复任务 |
| Legacy 测试可用 | 参考实现保留 | legacy 分支中 |
| 需手动测试 | 贡献者必须手动验证更改 | 当前要求 |

### 文档工作流

- ClientSim 文档贡献通过 `creator-docs` 仓库
- 代码贡献留在 ClientSim 仓库
- 代码和文档系统之间保持交叉引用

---

## 同步监控

同步系统包括：
- 同步操作自动验证
- 冲突检测和告警
- 失败同步回滚能力
- 所有同步活动审计日志

---

## 与知识库现有内容的关联

### 已有记载

1. **Persistence 测试**: 知识库提到 ClientSim 作为本地测试工具
2. **Testing Guide**: 记录了 ClientSim 限制

### 新增知识

以下内容是知识库的**新增条目**：
- ClientSim 完整发展历史
- CyanEmu 起源
- 2025 年仓库重构详情
- 双向同步架构
- 贡献流程
- legacy 分支用途

---

## 参考链接

- GitHub: https://github.com/vrchat-community/ClientSim
- DeepWiki: https://deepwiki.com/vrchat-community/ClientSim
- Creator Docs: https://creators.vrchat.com/