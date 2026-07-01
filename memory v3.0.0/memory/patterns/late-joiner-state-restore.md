---
title: "Late Joiner State Restore"
category: patterns
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - patterns
  - patterns
  - constraint
  - networking
  - sync
  - performance
aliases:
  - "Late Joiner State Restore"
  - late-joiner-state-restore
related:
  - "world/scene-components/vrc-objectsync.md"
  - "world/scene-components/vrc-enablepersistence.md"
  - "world/scene-components/vrc-scenedescriptor.md"
---
# Pattern: Late Joiner State Restore


---

## Problem
玩家在游戏/世界运行中途加入（late join），需要看到与其他玩家一致的对象状态。如果状态仅靠 Network Event 传递，late joiner 永远收不到。

## Context
- 任何状态持续的多人世界
- 门、开关、游戏分数、回合状态等
- 动态生成/销毁的对象

## Udon Constraints
- Network Event 是 fire-and-forget，不缓存
- `[UdonSynced]` 变量在玩家加入时自动同步最新值
- `OnDeserialization()` 在 late joiner 加入时会被调用
- 没有内置的"状态快照"机制 — 需要手动设计

## Networking Model

| 维度 | 决策 |
|---|---|
| State Owner | 对象 owner |
| Source of Truth | `[UdonSynced]` 变量集合 |
| Sync Type | Manual Sync（离散状态）或 Continuous Sync（连续状态） |
| Synced Variables | 所有 late joiner 需要的状态 |
| Mutation Path | owner 修改 → `RequestSerialization()` |
| Ownership Path | 按需转移 |
| Serialization Path | 每次状态变化 |
| Receive Path | `OnDeserialization()` 统一处理所有状态恢复 |
| Late Joiner Behavior | 加入时自动接收最新 synced value → `OnDeserialization()` → 本地表现重建 |
| Conflict Strategy | N/A（late joiner 被动接收） |
| Bandwidth Budget | 仅加入时一次性传输，之后按正常变化频率 |
| Failure Mode | 如果状态分散在多个 Behaviour 且未全部标记 `[UdonSynced]`，late joiner 部分状态缺失 |

## Performance Notes

- **Code Execution**: `OnDeserialization()` 在 late join 时一次性执行，之后无额外成本
- **Network Bandwidth**: 加入时一次性传输当前状态，与正常同步开销相同
- **Multi-VM**: 确保所有包含必需状态的 Behaviour 有合理的 SyncMode 和 synced variables

## Implementation Sketch

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class GameState : UdonSharpBehaviour {
    // 所有状态都在这里，集中管理
    [UdonSynced, FieldChangeCallback(nameof(RoundNumber))]
    private int _roundNumber = 1;
    [UdonSynced, FieldChangeCallback(nameof(GamePhase))]
    private int _gamePhase = 0; // 0=Waiting, 1=Playing, 2=Ended

    // 各 player 的分数（如果必须 synced）
    [UdonSynced] private int[] _scores = new int[16];

    public override void OnDeserialization() {
        // Late joiner 和远端更新都在这里处理
        // 在这里做本地表现重建，不要依赖 Network Event
        UpdateAllVisuals();
    }
}
```

## When To Use
- 任何 late joiner 需要看到一致状态的世界
- 几乎是所有多人 VRChat World 的必需模式

## When Not To Use
- 单人世界
- 纯瞬时交互世界（如简单的音效触发，状态不需要持久）
- 每个会话都完全重置的世界（但即使如此也建议保留此模式）

## Checklist: Late Joiner Readiness
- [ ] 所有 persisted 状态都有 `[UdonSynced]` 变量
- [ ] `OnDeserialization()` 能重建完整表现
- [ ] 不依赖 Network Event 恢复状态
- [ ] 动态生成的对象有对应的 synced state 指示其存在
- [ ] 测试：Host 触发状态 → 新玩家加入 → 状态一致

## 相关 Scene Components

- `memory/world/scene-components/vrc-objectsync.md` - **物理对象 Late Joiner**:`VRCObjectSync` 内置 late joiner 同步(Transform 自动同步),新加入玩家看到一致物理位置
- `memory/world/scene-components/vrc-enablepersistence.md` - **跨实例 Late Joiner**:`VRCEnablePersistence` 实现**跨实例**数据恢复(下次进入 World),与本模式"同实例内"late joiner 互补
- `memory/world/scene-components/vrc-scenedescriptor.md` - **Spawn Point Late Joiner**:`VRCSceneDescriptor` 的 Spawn Order 决定新玩家出生位置,本质是另一类 late joiner 处理
