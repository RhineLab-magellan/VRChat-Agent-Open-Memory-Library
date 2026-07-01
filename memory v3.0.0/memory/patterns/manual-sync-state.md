---
title: Pattern: Manual Sync State
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
  - "Manual Sync State"
  - "同步"

related:
  - world/udon/networking/performance.md
  - world/udon/networking/network-details.md
  - world/udon/networking/variables.md
  - world/udon/networking/late-joiners.md
  - world/udon/networking/ownership.md
  - world/udon/networking/compatibility.md
  - world/udon/networking/index.md
  - patterns/bit-packed-flags.md
  - patterns/late-joiner-state-restore.md
  - patterns/owner-authoritative-interaction.md
  - api/networking.md
  - world/scene-components/vrc-objectsync.md
  - world/scene-components/vrc-enablepersistence.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Pattern: Manual Sync State


---

## Problem
需要将对象的离散状态同步给房间内所有玩家，但状态变化频率低、不连续。需要在节带网络宽的同时保持状态正确。

## Context
- 门、灯、开关等离散状态对象
- 游戏中的回合/阶段/得分等状态
- 任何不连续变化但需要全局一致的状态

## Udon Constraints
- Continuous Sync 每帧序列化所有 synced variable，对离散状态浪费带宽
- NoVariableSync 不能自动同步状态，只能手动用 Network Event
- Network Event 无法恢复 late joiner 状态

## Networking Model

| 维度 | 决策 |
|---|---|
| State Owner | 对象的 owner |
| Source of Truth | `[UdonSynced]` int/byte 字段 |
| Sync Type | Manual Sync |
| Synced Variables | 最小状态字段，如 `_stateIndex` (int) |
| Mutation Path | 仅在 owner 侧发生状态变化时修改 |
| Ownership Path | 通过 Interact 或显式 SetOwner 转移 |
| Serialization Path | 每个状态变化后立即 `RequestSerialization()` |
| Receive Path | `FieldChangeCallback` 或 `OnDeserialization()` 触发远端更新 |
| Late Joiner | 加入时自动接收最新 synced variables，`OnDeserialization()` 触发 |
| Conflict Strategy | Owner 独占写入；快速连续修改时，最后的值胜出 |
| Bandwidth Budget | ~4 bytes/change + serialization header。变化频率由逻辑控制，通常 < 1Hz |
| Failure Mode | 如果 `RequestSerialization()` 被忘记调用，状态不同步 — 这是最常见 bug |

## Performance Notes

- **Code Execution**: 状态变化是离散事件，无 Update 成本
- **Network Bandwidth**: 仅变化时同步，远优于 Continuous Sync
- **Multi-VM**: 单 Behaviour 管理状态，其他 Behaviour 可通过 SerializeField 引用读取

## Implementation Sketch

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class DoorController : UdonSharpBehaviour {
    [UdonSynced, FieldChangeCallback(nameof(StateIndex))]
    private int _stateIndex = 0;
    // 0 = Closed, 1 = Open, 2 = Animating

    public int StateIndex {
        get => _stateIndex;
        set {
            _stateIndex = value;
            ApplyState();
        }
    }

    public override void Interact() {
        if (_stateIndex == 2) return; // debounce: 动画中
        _stateIndex = (_stateIndex == 0) ? 2 : 2; // 进入动画
        RequestSerialization();
        ApplyState();
    }

    private void ApplyState() {
        // 根据 _stateIndex 更新 Animator / Transform
    }

    // 动画完成回调 (通过 Animation Event → SendCustomEvent)
    public void OnAnimationComplete() {
        _stateIndex = (_stateIndex == 2 && _wasOpen) ? 0 : 1;
        RequestSerialization();
    }
}
```

## When To Use
- 离散状态：门开/关、灯亮/灭、回合阶段
- 低频变化：玩家手动触发，非自动连续变化
- 需要 late joiner 正确恢复状态

## When Not To Use
- 连续运动（用 Continuous Sync + VRCObjectSync）
- 一次性效果（用 Network Event）
- 单人场景（不需要同步）

---

## 相关知识库(性能优化)


关键交叉引用:

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/performance.md` | **10 条带宽优化规则、合并序列化、位域压缩** |
| `memory/world/udon/networking/network-details.md` | 内部字节细节、Manual 280KB vs Continuous 200B 差异 |
| `memory/world/udon/networking/variables.md` | `[UdonSynced]` 字段类型与序列化大小 |
| `memory/world/udon/networking/late-joiners.md` | Manual Sync 的 Late Joiner 自动同步保证 |
| `memory/world/udon/networking/ownership.md` | Manual 写入的 Owner 权限 |
| `memory/world/udon/networking/compatibility.md` | 字段增删与跨版本兼容 |
| `memory/world/udon/networking/index.md` | Manual vs Continuous 决策树 |
| `memory/patterns/bit-packed-flags.md` | 8 bool → 1 byte 的位域压缩模式 |
| `memory/patterns/late-joiner-state-restore.md` | Late Joiner 状态恢复模式 |
| `memory/patterns/owner-authoritative-interaction.md` | Owner 模式 |
| `memory/api/networking.md` | API 速查 |

## 相关 Scene Components

- `memory/world/scene-components/vrc-objectsync.md` - **与本模式的关键区别**: `VRCObjectSync` 是**自动物理同步**模式(每帧同步 Transform),本模式是**手动状态同步**模式(按需同步变量)。决策见 `vrc-objectsync.md#与-manual-sync-区别` 决策树
- `memory/world/scene-components/vrc-enablepersistence.md` - **本模式 + 持久化**: 在 PlayerObject 上使用本模式,数据会**跨实例持久化**(100KB/玩家/World),适合"玩家解锁进度、关卡状态"等场景
