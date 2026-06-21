# Editor Systems

> 来源: [VRChat Creator Docs - Editor](https://creators.vrchat.com/worlds/clientsim/systems/editor/)
> 索引日期: 2026-06-15

---

## 概述

Editor 子系统在 **Unity Editor 阶段**(非 Play Mode)辅助 ClientSim 的设置与配置。

> These systems help set things up in the Unity Editor.

---

## 子系统列表(3 个)

| 子系统 | 职责 | 文档 |
|--------|------|------|
| **Editor Runtime Linker** | 桥接 Editor 系统与 Runtime 系统,允许 Editor 工具调用 Runtime 逻辑 | 待补充(`editor-runtime-linker.md`) |
| **Helper Editors** | 自定义 Inspector / Editor 辅助类,优化 GameObject 与 Component 的编辑体验 | 待补充(`helper-editors.md`) |
| **Settings Window** | ClientSim Settings Window,配置本地玩家名称、身高、启用/禁用 ClientSim | 待补充(`settings-window.md`) |

> **任务范围说明**:本任务仅本地化 Editor 父页面,3 个子页面(`editor-runtime-linker`、`helper-editors`、`settings-window`)为**二级子页面**,不在本任务范围,可在后续任务中单独处理。

---

## 职责范围

| 维度 | Editor 系统职责 |
|------|----------------|
| **场景设置** | 注入 ClientSim 必要的 GameObject 与 Component |
| **Inspector 增强** | 自定义 ClientSimNetworkingView、ClientSimNetworkIdHolder 等组件的 Inspector |
| **Window 提供** | Settings Window、PlayerData Editor、PlayerObject Editor |
| **数据存储** | 管理 `ClientSimStorage/` 目录下的 JSON 文件 |
| **跨模式桥接** | 在 Editor 与 Runtime 之间无缝传递配置 |

---

## 与 Runtime 子系统的关系

```
┌──────────────────────────────────┐
│   Editor Systems (Editor Mode)   │
│   - Settings Window              │
│   - Helper Editors               │
│   - Editor Runtime Linker        │
└──────────┬───────────────────────┘
           │ 在 Play Mode 启动时注入配置
           ▼
┌──────────────────────────────────┐
│  Runtime Systems (Play Mode)     │
│  - RuntimeLoader (初始化入口)     │
│  - Settings (读取配置)            │
│  - Main (生命周期管理)            │
└──────────────────────────────────┘
```

---

## 相关页面

- [Systems Index](index.md) - 回到 Systems 父目录
- [Architecture](architecture.md) - 整体架构(Observer + DI)
- [Runtime](runtime.md) - Runtime 子系统
- [Script Execution Order](script-execution-order.md) - 系统执行顺序
