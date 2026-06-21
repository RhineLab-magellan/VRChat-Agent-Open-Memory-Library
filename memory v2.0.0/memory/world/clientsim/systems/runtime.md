---
title: Runtime Systems
category: world
subcategory: clientsim

knowledge_level: applied
status: active

tags:
  - world
  - pickup
  - event
  - light

aliases:
  - "Runtime Systems"

related:
  - script-execution-order.md
  - index.md
  - architecture.md
  - editor.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Runtime Systems

These systems help simulate things that happen at Runtime in VRChat worlds.

---

## 概述

Runtime 子系统在 **Play Mode** 中模拟 VRChat 客户端的运行行为。


---

## 子系统列表(18 个)

| 子系统 | 职责 | 文档 |
|--------|------|------|
| **Blacklist Manager** | 黑名单管理,防止某些系统在测试中触发 | 待补充(`blacklist-manager.md`) |
| **Event Dispatcher and Events** | 事件分发器,Observer Pattern 的核心实现 | 待补充(`event-dispatcher.md`) |
| **VRCSDK Helpers** | VRCSDK Helper 类,ClientSim 中复刻 VRCPlayerApi 等 | 待补充(`helpers.md`) |
| **HighlightManager** | 高亮管理,模拟 VRChat 物体高亮反馈 | 待补充(`highlight-manager.md`) |
| **Input** | 键鼠 / Gamepad 输入处理 | 待补充(`input.md`) |
| **InteractiveLayerProvider** | 交互层 Provider,管理 UI / Pickup 等交互层级 | 待补充(`interactive-layer-provider.md`) |
| **Client Sim Main** | ClientSim Main 入口,生命周期管理 | 待补充(`main.md`) |
| **Client Sim Menu** | 模拟 VRChat 快捷菜单 | 待补充(`menu.md`) |
| **Player Manager** | 玩家管理,管理本地与远程玩家 | 待补充(`player-manager.md`) |
| **Player Spawner** | 玩家生成器,模拟玩家进出实例 | 待补充(`player-spawner.md`) |
| **Player** | Player 类,代表单个玩家实例 | 待补充(`player.md`) |
| **RuntimeLoader** | Runtime Loader,Play Mode 启动时初始化所有系统 | 待补充(`runtime-loader.md`) |
| **Scene Manager** | 场景管理,模拟 VRChat 场景加载与切换 | 待补充(`scene-manager.md`) |
| **Settings** | Runtime Settings,读取 ClientSimSettings 资源 | 待补充(`settings.md`) |
| **SyncedObjectManager** | Synced Object 管理,处理 PlayerObject 的同步数据 | 待补充(`synced-object-manager.md`) |
| **TooltipManager** | Tooltip 管理,显示玩家交互提示 | 待补充(`tooltip-manager.md`) |
| **UdonManager** | Udon 管理,桥接 UdonBehaviour 与 ClientSim 事件 | 待补充(`udon-manager.md`) |
| **Unity Event System** | Unity Event System 集成,UI 事件分发 | 待补充(`unity-event-system.md`) |


---

## 职责范围

| 维度 | Runtime 系统职责 |
|------|------------------|
| **Player 模拟** | 本地玩家输入、远程玩家占位、PlayerObject 同步 |
| **输入处理** | 键鼠 / Gamepad → TrackingProvider → PlayerController |
| **事件分发** | EventDispatcher + Unity Event System 协调 UI / Interact 事件 |
| **Udon 桥接** | UdonManager 将 UdonBehaviour 与 ClientSim 事件系统对接 |
| **场景与生命周期** | RuntimeLoader 启动、SceneManager 切场景、Main 周期管理 |
| **持久化** | SyncedObjectManager 处理 PlayerObject,Settings 读取 ClientSimSettings |
| **UI 反馈** | TooltipManager 提示、HighlightManager 高亮、Menu 模拟 |

---

## 系统执行时序

详细执行顺序见 [Script Execution Order](script-execution-order.md)。

简化时序:

```
Play Mode 启动
    │
    ▼
RuntimeLoader 初始化所有系统
    │
    ▼
每帧:
  1. UnityInputSystem (-Infinity)        // 输入读取
  2. TrackingProvider (-3000)            // 头部 / 手部姿态
  3. PlayerController (-3000)            // 玩家位移
  4. PlayerRaycaster (-2000)             // 拾取 / 交互射线
  5. Unity Event System (-1000)          // UI 事件
  6. ClientSimBehaviours (0)             // ClientSim 组件
  7. UdonBehaviour (0)                   // Udon Update
  8. UdonInput (1)                       // Udon 输入事件
  9. ClientSimBaseInput (10000)          // Input 帧 tick
  10. PlayerStationManager (30000)       // Station 玩家位置
  11. TooltipManager (30001)             // Tooltip 位置
  12. PostLateUpdater (31000)            // VRChat PostLateUpdate
```

---

## 相关页面

- [Systems Index](index.md) - 回到 Systems 父目录
- [Architecture](architecture.md) - 整体架构(Observer + DI)
- [Editor](editor.md) - Editor 子系统
- [Script Execution Order](script-execution-order.md) - 详细执行顺序表
