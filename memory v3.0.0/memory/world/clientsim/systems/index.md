---
title: "ClientSim Systems"
category: world
subcategory: clientsim
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - misc
  - index
  - navigation
aliases:
  - "ClientSim Systems"
  - index
related:
  - architecture.md
  - editor.md
  - runtime.md
  - script-execution-order.md
  - index.md
---
# ClientSim Systems

> 来源: [VRChat Creator Docs - Systems](https://creators.vrchat.com/worlds/clientsim/systems/)
> 索引日期: 2026-06-15

---

## 概述

本节介绍 ClientSim **内部系统**的工作原理,适用于:

- 深入理解 ClientSim 行为
- 排查 ClientSim 相关问题
- 贡献 ClientSim 项目本身

---

## 子分类

| 子系统 | 职责 | 文档 |
|--------|------|------|
| **Architecture** | 整体架构(Observer Pattern + Dependency Injection) | [architecture.md](architecture.md) |
| **Editor** | Unity Editor 内的辅助系统(场景设置、Inspector) | [editor.md](editor.md) |
| **Runtime** | Play Mode 中模拟 VRChat 行为的系统 | [runtime.md](runtime.md) |
| **Script Execution Order** | 11 个核心系统的 Unity 脚本执行顺序 | [script-execution-order.md](script-execution-order.md) |

---

## 子分类(详细内容索引)

### Editor 子系统(3 个子页面)

| 页面 | 说明 |
|------|------|
| `editor-runtime-linker` | 在 Editor 与 Runtime 之间桥接 ClientSim 系统的链接器 |
| `helper-editors` | ClientSim 自定义 Inspector / Editor 辅助类 |
| `settings-window` | ClientSim Settings Window(本地玩家名称、身高、开关) |

### Runtime 子系统(18 个子页面)

| 页面 | 说明 |
|------|------|
| `blacklist-manager` | 黑名单管理,防止某些系统在测试中触发 |
| `event-dispatcher` | 事件分发器,Observer Pattern 的核心实现 |
| `helpers` | VRCSDK Helper 类(ClientSim 中复刻的 VRCPlayerApi 等) |
| `highlight-manager` | 高亮管理,模拟 VRChat 的物体高亮 |
| `input` | 键鼠 / Gamepad 输入处理 |
| `interactive-layer-provider` | 交互层 Provider,管理 UI / Pickup 等交互层级 |
| `main` | ClientSim Main 入口,生命周期管理 |
| `menu` | ClientSim 菜单(模拟 VRChat 快捷菜单) |
| `player-manager` | 玩家管理,管理本地与远程玩家 |
| `player-spawner` | 玩家生成器,模拟玩家进出 |
| `player` | Player 类,代表单个玩家实例 |
| `runtime-loader` | Runtime Loader,Play Mode 启动时初始化所有系统 |
| `scene-manager` | 场景管理,模拟 VRChat 场景加载与切换 |
| `settings` | Runtime Settings(读取 ClientSimSettings 资源) |
| `synced-object-manager` | Synced Object 管理,处理 PlayerObject 的同步数据 |
| `tooltip-manager` | Tooltip 管理,显示玩家交互提示 |
| `udon-manager` | Udon 管理,桥接 UdonBehaviour 与 ClientSim 事件 |
| `unity-event-system` | Unity Event System 集成,UI 事件分发 |

> **任务范围说明**:本次任务仅本地化至 Systems 父级 4 个文件(`architecture.md`、`editor.md`、`runtime.md`、`script-execution-order.md`)。
> 上述子页面(`editor-runtime-linker`、`event-dispatcher` 等)为**二级子页面**,不在本任务范围,可在后续任务中单独处理。

---

## 关联阅读顺序

| 读者 | 推荐顺序 |
|------|----------|
| **使用者**(只想用 ClientSim) | [index.md](../index.md) → [playerdata-editor.md](../playerdata-editor.md) |
| **深度用户**(想理解行为差异) | [index.md](../index.md) → [script-execution-order.md](script-execution-order.md) → [architecture.md](architecture.md) |
| **贡献者**(想参与开发) | [architecture.md](architecture.md) → [editor.md](editor.md) → [runtime.md](runtime.md) → 子页面 |
