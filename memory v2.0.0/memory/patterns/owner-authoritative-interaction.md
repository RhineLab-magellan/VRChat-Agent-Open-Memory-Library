---
title: Pattern: Owner Authoritative Interaction
category: patterns

knowledge_level: applied
status: active

tags:
  - patterns
  - patterns
  - constraint
  - networking
  - sync
  - performance

aliases:
  - "Owner Authoritative Interaction"

related:
  - world/udon/networking/ownership.md
  - world/udon/networking/events.md
  - world/udon/networking/variables.md
  - world/udon/networking/late-joiners.md
  - world/udon/networking/network-components.md
  - world/udon/networking/compatibility.md
  - world/udon/networking/performance.md
  - world/udon/networking/debugging.md
  - world/udon/networking/index.md
  - api/networking.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Pattern: Owner Authoritative Interaction

本文档为基础模式。详细 Networking 文档、所有权 API 流程、风险分析见 `memory/world/udon/networking/` 子分类。

---

## Problem
在 VRChat 多人世界中，多个玩家可能同时与同一对象交互（点击、拾取、触发）。需要确保只有一个人能够执行状态变更，且所有玩家看到一致结果。

## Context
- 多人交互对象（开关、按钮、门、控制器）
- 任何多个玩家可能同时 Interact 的对象
- 需要 late joiner 看到正确状态的对象

## Udon Constraints
- 每个 UdonBehaviour 同一时间只有一个 owner
- 只有 owner 可以写入 `[UdonSynced]` 变量
- Network Event 无法被 late joiner 收到

## Networking Model

| 维度 | 决策 |
|---|---|
| State Owner | 交互对象的 owner（默认为 Master，可转移给交互玩家） |
| Source of Truth | `[UdonSynced]` 变量（如 `_state`） |
| Sync Type | Manual Sync |
| Synced Variables | `_state` (int) — 对象状态索引 |
| Mutation Path | owner 在 `Interact()` 中修改 `_state` |
| Ownership Path | 可选的 `Networking.SetOwner()` 转移 ownership 给交互者 |
| Serialization Path | 修改 `_state` 后立即 `RequestSerialization()` |
| Receive Path | 远端在 `OnDeserialization()` 或 `FieldChangeCallback` 中更新表现 |
| Late Joiner | `[UdonSynced]` 变量自动同步最新值，`OnDeserialization()` 触发表现更新 |
| Conflict Strategy | Owner 锁定：只有当前 owner 可以修改。如需频繁切换 owner，在 `Interact()` 开头检查 `isOwner` |
| Bandwidth Budget | 4 bytes per state change (int)，变化频率通常 < 1Hz |
| Failure Mode | Network Event 丢失不会影响状态（状态靠变量同步）；owner 离开后 ownership 转移给 Master |

## Performance Notes

- **Code Execution**: `Interact()` → 检查 owner → 修改 int → `RequestSerialization()`，步骤极少
- **Network Bandwidth**: 变化时才同步，手动控制频率
- **Multi-VM**: 单 Behaviour 处理，无跨 VM 调用

## Implementation Sketch

```
Interact():
  1. [可选] 如果不是 owner，Networking.SetOwner(...) 或 return
  2. 修改 _state
  3. RequestSerialization()
  4. 触发本地表现更新

FieldChangeCallback:
  1. 接收新 state 值
  2. 更新本地 Animator / Material / AudioSource

OnDeserialization:
  1. 处理 late joiner 表现恢复
```

## When To Use
- 任何多人可交互的离散状态对象
- 需要 owner 保护的状态变更

## When Not To Use
- 不需要网络同步的单人对象
- 纯粹的连续运动（用 Continuous Sync + VRCObjectSync）
- 需要多个玩家同时操作的对象（需要更复杂的状态合并）

---

## 相关知识库(应用层详解)


| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/ownership.md` | **所有权 API 详解、SetOwner 流程、Master vs InstanceOwner、OnOwnershipRequest 业务规则** |
| `memory/world/udon/networking/events.md` | Network Event 速率限制、`[NetworkCallable]`、`SendCustomNetworkEvent(Owner)` 模式 |
| `memory/world/udon/networking/variables.md` | `[UdonSynced]` 字段写入权限、FieldChangeCallback 自动触发 |
| `memory/world/udon/networking/late-joiners.md` | Owner 离开时的转移与 Late Joiner 同步保证 |
| `memory/world/udon/networking/network-components.md` | VRCPickup 自动所有权机制、VRCObjectPool Owner 控制 |
| `memory/world/udon/networking/compatibility.md` | 跨平台所有权兼容性、PC/Quest 字段一致性 |
| `memory/world/udon/networking/performance.md` | 所有权转移的带宽成本、最小化转移策略 |
| `memory/world/udon/networking/debugging.md` | 所有权冲突诊断、`OnOwnershipRequest` 调试 |
| `memory/world/udon/networking/index.md` | Networking 概述、决策树 |
| `memory/api/networking.md` | API 速查(Networking 类成员) |

## Related Patterns
- `manual-sync-state.md` - Manual Sync 模式(本模式的基础)

## 相关 Scene Components

- `memory/world/scene-components/vrc-objectsync.md` - **物理对象所有权**:`VRCObjectSync` 自动处理碰撞所有权转移(Allow Collision Ownership Transfer),适合物理交互;与本模式互补,本模式适合离散状态,ObjectSync 适合物理 Transform
- `memory/world/scene-components/vrc-station.md` - **Station 事件驱动**:`OnStationEntered` / `OnStationExited` 是典型的"事件触发所有权变更"模式,可结合本模式实现多人载具
