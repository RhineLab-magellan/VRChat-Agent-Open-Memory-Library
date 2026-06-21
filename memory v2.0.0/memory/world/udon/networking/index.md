---
title: Networking 概述
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "网络"

related:
  - tools/network-id-utility.md
  - tools/network-stats.md
  - api/networking.md
  - patterns/manual-sync-state.md
  - patterns/owner-authoritative-interaction.md
  - patterns/late-joiner-state-restore.md
  - patterns/bit-packed-flags.md
  - patterns/advanced-sync-patterns.md
  - world/udon/networking/variables.md

source: VRChat 官方 Creator Docs (Networking Index)
source_type: official
version: 1.0
last_review: 2026-06-15
confidence: High
---
# Networking 概述

> SDK Version: 3.x (Continuous 维护)
---

## 简介

VRChat Networking 是 **Udon 多玩家同步的核心系统**,让 World 中的对象、数据、事件能在实例内所有玩家之间保持一致。

Networking 围绕 **三大核心概念** 设计:

| 概念 | 定义 | 生命周期 | 典型用途 |
|------|------|---------|---------|
| **Variables(网络变量)** | 跨玩家共享的持久数据 | 持续,迟到玩家可获取最新值 | 分数、门状态、位置 |
| **Events(网络事件)** | 一次性触发的动作 | 触发即结束,不可重放 | 发射子弹、播放动画 |
| **Ownership(所有权)** | 决定哪名玩家可修改对象 | 玩家离开时自动转移 | 交互对象、Physics 物体 |

> **关键区别**:Variables 是状态(长期),Events 是动作(瞬时)。把状态写进事件是 **世界最常见 Networking Bug**。

---

## 带宽限制(权威数据)

> ⚠️ 这是 **Udon 整体发送能力** 的硬上限,所有 UdonBehaviour 共享此配额。

| 限制类型 | 数值 | 触发机制 | 超出后果 |
|---------|------|---------|---------|
| **总带宽** | **~11 KB/s** | 所有 Udon 同步总和 | `Networking.IsClogged = true`,全局拥塞 |
| **Manual Sync** | **280,496 bytes/serialization** | `RequestSerialization()` | 事件被缓存、延迟发送 |
| **Continuous Sync** | **~200 bytes/serialization** | 每帧自动 | 事件 **直接失败**,日志报错 |
| **Network Event 参数** | 16 KB/event | `SendCustomNetworkEvent` | 内部拆分为多个事件 |
| **Network Event 总吞吐** | ~18 KB/s(含网络开销) | 同上 | 实际可用 8-10 KB/s |

### 超过带宽的连锁反应

```
数据量超限
  → IsClogged = true
    → Continuous: 序列化失败,日志错误
    → Manual: 事件排队,延后重试
      → 业务逻辑继续执行,但数据未发送
        → 玩家看到的状态不一致
```

> **设计建议**:在所有 Networking 入口处检查 `IsClogged`,发现拥塞时降级表现(关闭粒子、减少同步频率)。

---

## 同步模式选择决策树

```
是否需要 Late Joiner 看到正确状态?
├── 是 → 必须使用 [UdonSynced] 变量 (Manual/Continuous)
│   │
│   变量是否高频变化 (≥ 10Hz)?
│   ├── 是 → Continuous Sync (200B 上限,适合 transform/进度条)
│   └── 否 → Manual Sync + RequestSerialization() (280KB 上限)
│
└── 否 → 可选 Network Event (瞬时动作)
    │
    是否需要参数?
    ├── 否 → SendCustomNetworkEvent(target, "EventName")
    └── 是 → [NetworkCallable] + NetworkCalling.SendCustomNetworkEvent (SDK 3.8.1+)
```

### 模式速查

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 门开/关 | Manual Sync + `bool` | 离散状态,变化稀疏 |
| 玩家位置 | Continuous + `Vector3` | 高频变化,中间值有意义 |
| 子弹发射 | Network Event | 瞬时动作,不需要持久化 |
| 积分板 | Manual Sync + `int[]` | 关键状态,Late Joiner 必须看到 |
| 物理物体 Transform | `VRCObjectSync` | VRChat 内置优化(插值、压缩) |
| 拾取物体 | `VRCPickup` + 事件 | 自动处理所有权转移 |

---

## 三个核心概念的协作关系

```
┌─────────────────────────────────────────────────────────┐
│  Player A (Owner)                                       │
│    │                                                    │
│    ├─ 修改 [UdonSynced] 变量                            │
│    │   └─ Manual: RequestSerialization() ──┐            │
│    │                                       │            │
│    └─ SendCustomNetworkEvent(All, "X")  ──┤            │
│                                            ▼            │
│                                    VRChat Server        │
│                                            │            │
│      ┌─────────────────────────────────────┼─────────┐  │
│      ▼                                     ▼         ▼  │
│  Player A(本地)                   Player B      Player C│
│  ├─ 变量: 立即应用                ├─ 变量: 收到  ├─ ... │
│  └─ 事件: 立即触发                │  更新        │       │
│                                   └─ 事件: 触发  │       │
│                                                   │       │
│  ┌─── Late Joiner Player D 加入 ─────────────────┘       │
│  │                                                       │
│  ├─ 变量: 收到最新值,触发 OnDeserialization()           │
│  └─ 事件: 不会收到(已发生)                              │
└─────────────────────────────────────────────────────────┘
```

---

## 网络事件 vs 变量(决策矩阵)

| 维度 | Variables | Events |
|------|-----------|--------|
| 持久性 | ✅ 持续,新玩家可见 | ❌ 一次性,新玩家不可见 |
| 带宽效率 | 高(单次发送,所有人共享) | 中(每次触发都发送) |
| 调用频率 | 受 Manual/Continuous 限制 | 受 `[NetworkCallable]` 速率限制 |
| 触发一致性 | 最终一致(Last-Write-Wins) | 即时(有序保证) |
| 适合的状态 | 离散、关键、可恢复 | 瞬时、装饰、不影响游戏逻辑 |
| Owner 依赖 | 必须 Owner 修改 | 不依赖 Owner(Any → Any) |

---

## 关键性能指标(KPI)

| 指标 | 健康值 | 警告 | 危险 |
|------|-------|------|------|
| `BytesOutAverage` | < 2 KB/s | 2-8 KB/s | > 11 KB/s |
| `IsClogged` 持续 true | < 1% 时间 | 1-10% 时间 | > 10% 时间 |
| 序列化失败(OnPostSerialization) | 0 次/分钟 | 1-5 次/分钟 | 持续失败 |
| `ReliableEventsInOutboundQueue` | 0-5 | 5-20 | > 20 |

> **监控方式**:World Debug Views 菜单(Debug Menu 6)实时显示每对象的字节数。

---

## 子页面索引

| 文档 | 主题 |
|------|------|
| `compatibility.md` | 跨版本兼容、降级策略、Serialization 限制 |
| `events.md` | 8 个 Networking Events 完整列表 |
| `variables.md` | UdonSynced 字段类型、序列化大小计算 |
| `ownership.md` | Owner 转移流程、SetOwner 安全检查 |
| `late-joiners.md` | OnPlayerJoined 状态同步、Buffer Events |
| `network-components.md` | VRCObjectSync、VRCPickup、Object Pool |
| `debugging.md` | Network 图表、Stats 窗口、ClientSim 模拟 |
| `performance.md` | 带宽优化 10 条规则、对象池、合并序列化 |
| `network-details.md` | 内部实现细节、Manual vs Continuous 字节差异 |
| `tools/` | **开发/调试工具子分类** |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/api/networking.md` | API 速查(Networking 类、UdonBehaviour 同步成员) |
| `memory/patterns/manual-sync-state.md` | Manual Sync 模式实现范式 |
| `memory/patterns/owner-authoritative-interaction.md` | Owner Authority 模式 |
| `memory/patterns/late-joiner-state-restore.md` | Late Joiner 状态恢复 |
| `memory/patterns/bit-packed-flags.md` | 位域压缩同步(节省带宽) |
| `memory/patterns/advanced-sync-patterns.md` | 高级同步模式 |
| `memory/world/udon/networking/variables.md` | UdonSynced 字段类型详解 |
| `memory/world/udon/networking/tools/` | **开发/调试工具**(Network ID Utility + Network Stats API) |

---

## 风险与陷阱

| 风险 | 说明 | 缓解措施 |
|------|------|---------|
| 带宽超限 | Continuous 200B、Manual 280KB 是硬上限 | 监控 `IsClogged`、使用位域压缩 |
| Master 抢占 | Master 离开时自动获得所有权 | 使用 `IsInstanceOwner` 而非 `IsMaster` 做权限 |
| Late Joiner 错位 | 用 Event 同步状态,新玩家丢失 | 状态必须用 `[UdonSynced]` 变量 |
| RequestSerialization 遗漏 | Manual Sync 最常见 bug | 用 `[UdonSynced]` + `FieldChangeCallback` 自动序列化提示 |
| 连续每帧 Serialize | 性能杀手 | Manual + 阈值变化才触发 |

---

## 开发/调试工具

> **Tools**:see [tools/](tools/)

Networking 配套提供了两个开发/调试工具,用于解决开发期的常见问题:

| 工具 | 类别 | 解决问题 |
|------|------|---------|
| [`tools/network-id-utility.md`](tools/network-id-utility.md) | **Editor 工具** | 跨平台 World(PC/Quest)的 Network ID 对齐、冲突解决 |
| [`tools/network-stats.md`](tools/network-stats.md) | **运行时 API**(`VRC.SDK3.Network.Stats`) | 实时监控带宽、序列化次数、对象级网络开销 |

### 与现有调试工具的区分

| 工具 | 类别 | 详见 |
|------|------|------|
| `tools/network-id-utility.md` | Editor 工具(分配/导入/导出 Network ID) | 本页 |
| `tools/network-stats.md` | 运行时 API(程序化访问网络指标) | 本页 |
| `debugging.md` | 调试方法论 + ClientSim 模拟 + VRChat 客户端 Stats 窗口 | `debugging.md` |
| `memory/sources/clientsim.md` + `memory/world/clientsim/` | ClientSim 项目仓库元数据 + 4 个调试窗口 | `clientsim.md` |

> ⚠️ **重要区分**:ClientSim **没有** 专门的 "Network 图表" 工具,它的 4 个窗口是 Settings / PlayerObject / PlayerData / Main。ClientSim 的核心价值是 **模拟网络行为**,而 Network Stats API 是 **可视化/程序化访问真实网络数据**。
