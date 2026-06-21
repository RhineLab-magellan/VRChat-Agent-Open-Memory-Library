---
title: Architecture
category: world
subcategory: clientsim

knowledge_level: applied
status: active

tags:
  - world
  - event
  - udonsharp

aliases:
  - "Architecture"

related:
  - runtime.md
  - index.md
  - editor.md
  - script-execution-order.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Architecture


---

## 概述

ClientSim 的架构以**小型组件**为核心,采用**事件驱动的 Observer Pattern**,结合**手动 Dependency Injection** —— 每个类只通过构造函数或初始化方法接收其所需的依赖。

### 设计目标

| 目标 | 实现手段 |
|------|----------|
| **解耦** | Observer Pattern(事件系统) |
| **可测试** | Dependency Injection(易于 Mock) |
| **可扩展到 VR** | Player Controller 基于 generic dependency providers,可平滑迁移到 VR 而无需重写核心系统 |

---

## Observer Pattern 观察者模式

ClientSim 使用 Observer Pattern 在系统间传递事件。任何系统都可以监听事件,无需知道谁处理它。

### 优势

| 优势 | 说明 |
|------|------|
| **解耦** | 发送事件的系统不直接依赖接收系统,提升模块独立性 |
| **可测试性** | 一个系统发送事件时,不需要为了测试而直接依赖另一个系统 |
| **可扩展性** | 新增功能只需添加新的 Listener,无需修改 Sender |

### 核心实现

具体实现见 [Event Dispatcher](runtime.md#event-dispatcher)(待二级子页面补充)。

---

## Dependency Injection 依赖注入

ClientSim 采用**手动管理**的依赖注入:

| 步骤 | 说明 |
|------|------|
| **1. 系统创建** | 创建时通过构造函数或 `Initialize` 方法接收所有依赖 |
| **2. Provider 模式** | 依赖被结构化为 Provider,必须实现特定接口 |
| **3. 接口依赖** | 依赖类时,依赖其**接口**而非实现类 |
| **4. 可替换性** | 可注入不同 Provider 实现,无需修改使用方代码 |
| **5. 可测试** | 依赖可被 Mock,便于单元测试 |

### 模式示意

```text
┌─────────────────────┐
│  ClassA (依赖接口)   │
└─────────┬───────────┘
          │ 依赖 IProvider (接口)
          ▼
┌─────────────────────┐
│  IProvider (接口)   │
└─────────┬───────────┘
          │ 实现
          ▼
┌─────────────────────┐         ┌──────────────────┐
│ MockProvider (测试) │   OR    │ RealProvider     │
└─────────────────────┘         └──────────────────┘
```

### 设计意义

| 场景 | 优势体现 |
|------|----------|
| **单元测试** | 注入 Mock Provider,无需启动完整 ClientSim |
| **多平台扩展** | 未来支持 VR 输入时,只需注入新的 `ITrackingProvider` 实现 |
| **配置驱动** | 通过替换 Provider 实现,可在不同场景使用不同输入设备 |

---

## 架构总览

```
            ┌─────────────────────────────────────────┐
            │         EventDispatcher (Observer)        │
            │  send / subscribe / unsubscribe          │
            └──────────┬───────────────────┬────────────┘
                       │                   │
        ┌──────────────▼──────┐  ┌─────────▼────────────┐
        │  TrackingProvider    │  │  InputSystem         │
        │  (位置/旋转数据)      │  │  (键鼠/手柄输入)       │
        └──────────┬──────────┘  └─────────┬────────────┘
                   │                       │
                   └───────────┬───────────┘
                               ▼
                   ┌───────────────────────────┐
                   │  PlayerController          │
                   │  (基于 IDependencyProvider)│
                   └───────────┬───────────────┘
                               ▼
                   ┌───────────────────────────┐
                   │  UdonManager / SyncedMgr   │
                   │  (桥接 UdonBehaviour)      │
                   └───────────────────────────┘
```

---

## 相关页面

- [Systems Index](index.md) - 回到 Systems 父目录
- [Editor](editor.md) - Editor 子系统
- [Runtime](runtime.md) - Runtime 子系统(含 EventDispatcher)
- [Script Execution Order](script-execution-order.md) - 系统执行顺序
