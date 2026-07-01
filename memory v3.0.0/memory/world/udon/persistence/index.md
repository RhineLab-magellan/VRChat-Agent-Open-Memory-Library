---
title: Persistence 实战教程 - 索引
category: world
subcategory: udon/persistence
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - storage
  - index
  - navigation
aliases:
  - 持久化教程
  - Persistence Tutorial
  - PlayerData 教程
  - PlayerObject 教程
related:
  - ../../../api/persistence.md
  - player-data.md
  - player-object.md
  - serialization.md
  - limits-and-quirks.md
  - patterns/leaderboard.md
  - patterns/unlock-items.md
  - patterns/persistent-pen.md
  - ../index.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/persistence/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# Persistence 实战教程 - 索引

> SDK Version: 3.10+(Storage Information API) / 3.7+(核心 PlayerData/PlayerObject)
> 官方文档:https://creators.vrchat.com/worlds/udon/persistence/
> 定位:**实战教程**(非 API 参考,API 速查见 `memory/api/persistence.md`)

---

## 什么是 Persistence?

Persistence(持久化)允许 World 保存玩家的高分、物品栏、最后位置、货币、解锁内容、偏好设置等。**当玩家离开 World 后再回来,Udon 仍能访问他们保存的数据**。

- **存储位置**:VRChat 服务器(与玩家账号绑定)
- **跨平台**:PC ↔ Quest ↔ Android 同一账号共享
- **跨实例**:同一 World 的所有实例共享数据
- **跨设备**:玩家在 PC 上解锁的物品,Quest 重新加入时仍能恢复

> **关键事实**:数据与 **World ID + 玩家账号** 绑定。不同 World 互不干扰。

---

## 两种持久化方案

VRChat 提供 **2 种** 持久化方案,覆盖绝大多数需求场景:

| 方案 | 类型 | 适合场景 |
|------|------|----------|
| **PlayerData** | 键值数据库(Key-Value Store) | 设置、分数、解锁、库存、玩家偏好 |
| **PlayerObject** | 自动实例化的 GameObject(可挂 Udon + 同步变量) | 工具、武器、血条、复杂 per-player 状态 |

> **核心区别**:PlayerData 是 **数据**,PlayerObject 是 **带数据的 GameObject**。

---

## PlayerData vs PlayerObject 完整对比

| 维度 | PlayerData | PlayerObject |
|------|-----------|--------------|
| **本质** | 键值数据库(扁平) | GameObject 模板,VRChat 自动为每个玩家实例化 |
| **存储配额** | 100 KB / 玩家 / World(压缩后) | 100 KB / 玩家 / World(压缩后,**独立配额**) |
| **原始数据上限** | ~300 KB(高度可压缩时) | ~300 KB(高度可压缩时) |
| **API 风格** | 静态方法 `PlayerData.SetXxx(player, key, value)` | 直接字段访问 `[UdonSynced] public int x;` |
| **数据可见性** | 任何 Udon 脚本可读写(写仅本地) | 通过 `[UdonSynced]` 同步给所有人 |
| **持久化机制** | 自动,无需标记 | 必须加 `VRCEnablePersistence` 组件 |
| **Owner 机制** | 无(纯数据) | 玩家拥有该 GameObject,**无法转移** |
| **同步开销** | 写一次 = 发全部 PlayerData(manual sync 模式) | 单独同步,不影响其他数据 |
| **Late Joiner** | 自动获取最新值 | 自动获取最新值(走 UdonSynced) |
| **写入限制** | 只能写本地玩家的数据 | 只能写自己 PlayerObject 的数据 |
| **删除 Key** | ❌ **不支持** 删除(只能覆盖值) | 走 UdonSynced 字段重置 |
| **Key 名长度** | 128 字符(建议值) | N/A(用字段名) |
| **String 值长度** | ~50 字符(建议值) | N/A |
| **最适合** | 简单 key-value(分数、设置) | 复杂 UdonBehaviour 状态(笔触、RPG) |

---

## 何时使用哪种?决策矩阵

```
你的数据是 key-value 形式吗?
├─ 是 ── 数据量大(>20 字段) 或 频繁变化(>1Hz)?
│         ├─ 是 ──→ PlayerObject(避免整体发送)
│         └─ 否 ──→ PlayerData(简单直接)
│
└─ 否 ── 你是数据还是带数据的物体?
          ├─ 纯数据(分数、设置) ──→ PlayerData
          └─ 带行为/可视化的物体(笔、武器、血条) ──→ PlayerObject
```

### 经验法则

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 玩家音量/亮度设置 | PlayerData | 简单 key-value,变化稀疏 |
| 高分排行榜 | PlayerData | 1 个 float 字段,所有人可见 |
| 成就解锁 | PlayerData | bool 列表,简单 |
| 自动点击器数量 | PlayerData | 简单 int |
| **画笔笔触数据**(>1KB,频繁变) | PlayerObject | 大量数据 + 高频变化,不应走 PlayerData |
| 玩家血条 | PlayerObject | 需要同步给所有人 + 持久化 |
| 玩家位置记忆 | PlayerObject | 复杂 per-player 状态 |
| RPG 角色等级/经验 | PlayerObject | 多个 UdonSynced 字段 |
| 工具/武器(不可被偷) | PlayerObject | PlayerObject 所有权**不能转移**,天然防偷 |

---

## 关键工程约束(必读)

### 数据存储位置

| 环境 | 存储位置 | 测试注意 |
|------|---------|---------|
| **已发布 World** | VRChat 服务器(跨平台/跨实例) | 同账号同 World 多开 → 数据冲突 |
| **Build & Test** | 本地(测试客户端) | 关闭测试客户端 → 数据删除 |
| **ClientSim** | 项目内 JSON 文件 | 见 ClientSim 文档 |

### 100 KB 限制详解

> ⚠️ **核心限制**:每个玩家在每个 World 可使用 **100 KB PlayerData + 100 KB PlayerObject**(独立配额)。

- 实际存储的是 **压缩后** 的大小
- 原始数据可达 ~300 KB(高度可压缩时)
- 超出 → VRChat 写错误日志,数据 **未保存**
- **String max** ~50 字符(建议值),**Key max** 128 字符(建议值)

### 时序约束(90% 玩家踩坑)

> 🔴 **必须等待 `OnPlayerRestored` 触发后再读写 PlayerData/PlayerObject 数据**

- `OnPlayerJoined` 触发时,数据可能还没从服务器拉取
- 太早读写 → 你的写入 **会** 被服务器拉来的旧数据覆盖
- **必须** 用 `_dataReady` flag 守卫

### 网络同步开销(高频写场景)

- PlayerData 每次写 = 发 **全部** PlayerData(类似 Manual Sync)
- PlayerObject = 单独同步(开销分摊)
- 高频写 PlayerData → 触发 `IsClogged = true`
- **建议**:高频 + 大量数据走 PlayerObject,稀疏 + 小数据走 PlayerData

---

## Key 命名空间(避免冲突)

> PlayerData 跨整个 World 的所有脚本共享,**必须用 Prefab 名作为前缀**:

```text
推荐格式: <Prefab名>-<功能描述>
示例:
- Momo-PPP-BloomAmount        # 来自 Momo Post Processing
- IdleGame-POINTS_KEY         # 来自 Persistent Idle Game
- PenSystem-Line-Color-0      # 来自 Persistent Pen
- RPG-Player-Level            # 来自 Simple RPG
- UnlockItems-Achievement-1   # 来自 Unlock Items
```

❌ 错误:`score`、`level`、`health`(易冲突,多个 Prefab 共用时数据互相覆盖)

---

## 子目录导航

| 文档 | 主题 | 推荐阅读 |
|------|------|---------|
| [player-data.md](./player-data.md) | PlayerData 完整 API(20+ 方法) | 第一次用 PlayerData |
| [player-object.md](./player-object.md) | PlayerObject + VRCEnablePersistence 设置 | 第一次用 PlayerObject |
| [serialization.md](./serialization.md) | 支持的 18 种数据类型 + byte[] 编码 | 需要存复杂结构 |
| [limits-and-quirks.md](./limits-and-quirks.md) | 100KB 限制 + 压缩策略 + 写入时机优化 | 优化阶段 |
| [patterns/leaderboard.md](./patterns/leaderboard.md) | 排行榜完整实现(浮动积分) | 实战 |
| [patterns/unlock-items.md](./patterns/unlock-items.md) | 成就/物品解锁系统 | 实战 |
| [patterns/persistent-pen.md](./patterns/persistent-pen.md) | 持久画笔(复杂 PlayerObject) | 实战 |

---

## 5 个 Persistence 事件速查

| 事件 | 触发时机 | 用途 |
|------|---------|------|
| `OnPlayerRestored(VRCPlayerApi player)` | 玩家持久化数据加载完成后 | **核心** - 加载/初始化数据 |
| `OnPlayerDataUpdated(VRCPlayerApi player, PlayerData.Info[] infos)` | 帧末,PlayerData 变更时 | 监听其他玩家数据变化 |
| `OnPlayerDataStorageWarning(VRCPlayerApi player)` | PlayerData 接近上限 | 提示玩家清理 |
| `OnPlayerDataStorageExceeded(VRCPlayerApi player)` | PlayerData 超出限制 | 数据未保存,需提示 |
| `OnPersistenceUsageUpdated(VRCPlayerApi player)` | 调用 `RequestStorageUsageUpdate` 后 | 获取实时存储用量 |

> **PlayerObject 事件**: `OnPlayerObjectStorageWarning` / `OnPlayerObjectStorageExceeded`(独立配额)

---

## 4 种存储信息查询方法(SDK 3.10+)

```csharp
using VRC.SDKBase;

// 1. 配额限制(常量)
int dataLimit = player.GetPlayerDataStorageLimit();   // 100 * 1024
int objLimit = player.GetPlayerObjectStorageLimit();  // 100 * 1024

// 2. 当前用量(可能过期)
int dataUsed = player.GetPlayerDataStorageUsage();
int objUsed = player.GetPlayerObjectStorageUsage();

// 3. 触发异步更新
player.RequestStorageUsageUpdate();

// 4. 事件回调
public override void OnPersistenceUsageUpdated(VRCPlayerApi player) {
    if (player == Networking.LocalPlayer) {
        Debug.Log($"PlayerData: {player.GetPlayerDataStorageUsage()}/{player.GetPlayerDataStorageLimit()}");
    }
}
```

⚠️ **警告**:不要频繁调用 `RequestStorageUsageUpdate`,存储信息可能随时间过期。

---

## 与其他子目录的关系

| 知识库文件 | 关系 |
|-----------|------|
| `memory/api/persistence.md` | **API 速查表**(本文是实战教程) |
| `memory/world/examples/persistence/` | 9 个 Example Central 官方示例笔记 |
| `memory/world/udon/index.md` | Udon 总览(VM 关系 + 3 种创建方式) |
| `memory/world/udon/networking/` | 网络同步(与 PlayerObject 强相关) |
| `memory/rules/networking-rules.md` | 网络同步规则 |
| `memory/patterns/manual-sync-state.md` | Manual Sync 模式 |
| `memory/patterns/late-joiner-state-restore.md` | Late Joiner 状态恢复 |
| `memory/sources/clientsim.md` | ClientSim 编辑器模拟(含 PlayerData 调试窗口) |

---

## 验收标准

✅ 8 个 .md 文件全部创建(1 索引 + 4 基础 + 3 实战)
✅ 所有 API 经官方文档验证(2025-08-01 / 2025-09-17 / 2025-11-25)
✅ PlayerData vs PlayerObject 完整对比
✅ 100KB 限制 + 压缩策略完整覆盖
✅ Key 命名空间前缀建议
✅ 时序约束(OnPlayerRestored 等待)强调
✅ 3 个实战 Pattern 完整实现(含代码)
✅ 不与 `api/persistence.md` 重复
