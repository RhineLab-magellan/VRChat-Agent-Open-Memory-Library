# Pattern: Event-Driven State Machine

> Type: PATTERN
> Confidence: High
> SDK Version: VRChat SDK 3.x
> Last Verified: 2026-06-04

---

## Problem
复杂的逻辑状态管理容易变成混乱的 bool 标记 + if/else 堆叠。Update() 中每帧检查状态机条件浪费执行步骤。

## Context
- 多阶段逻辑（回合制游戏、多步骤 puzzle、关卡流程）
- 状态之间有明确的转换条件
- 需要网络同步状态
- 需要 late joiner 恢复状态

## Udon Constraints
- 无 enum.TryParse，但可以用 const int 定义状态
- 无 switch-on-string，但 switch-on-int 可用
- SendCustomEvent 是最接近"状态转换回调"的机制

## Networking Model

| 维度 | 决策 |
|---|---|
| State Owner | 状态机所在 Behaviour 的 owner |
| Source of Truth | `[UdonSynced]` int `_state` |
| Sync Type | Manual Sync |
| Synced Variables | `_state` (int) — 当前状态 ID |
| Mutation Path | 事件（Interact、Trigger、Timer）触发 `TransitionTo(newState)` |
| Serialization Path | `TransitionTo()` 内调用 `RequestSerialization()` |
| Receive Path | `FieldChangeCallback` 触发 `OnStateChanged()` |
| Late Joiner | `_state` 自动同步，`OnDeserialization()` 调用 `OnStateChanged()` |

## Implementation Sketch

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class StateMachine : UdonSharpBehaviour {
    // 状态定义
    private const int STATE_IDLE = 0;
    private const int STATE_PLAYING = 1;
    private const int STATE_PAUSED = 2;
    private const int STATE_ENDED = 3;

    [UdonSynced, FieldChangeCallback(nameof(CurrentState))]
    private int _currentState = STATE_IDLE;

    public int CurrentState {
        get => _currentState;
        set {
            _currentState = value;
            OnStateChanged();
        }
    }

    private void TransitionTo(int newState) {
        // Owner 检查（如果需要）
        if (_currentState == newState) return;
        _currentState = newState;
        RequestSerialization();
        OnStateChanged();
    }

    private void OnStateChanged() {
        // 离开旧状态的清理
        // ...

        // 进入新状态
        switch (_currentState) {
            case STATE_IDLE:
                // 初始化 idle
                break;
            case STATE_PLAYING:
                SendCustomEventDelayedSeconds(nameof(_OnTimerEnd), 60f);
                break;
            case STATE_PAUSED:
                break;
            case STATE_ENDED:
                break;
        }
    }

    // 事件驱动状态转换
    public override void Interact() {
        if (_currentState == STATE_IDLE)
            TransitionTo(STATE_PLAYING);
    }

    public void _OnTimerEnd() {
        if (_currentState == STATE_PLAYING)
            TransitionTo(STATE_ENDED);
    }

    public override void OnDeserialization() {
        OnStateChanged(); // late joiner 恢复
    }
}
```

## When To Use
- 3+ 个状态的逻辑
- 状态转换有条件依赖
- 需要网络同步状态机位置

## When Not To Use
- 只有 2 个状态且逻辑简单（直接 bool 足够）
- 纯本地逻辑不需要网络同步
- 完全无状态的瞬时交互

## Related Patterns
- `manual-sync-state.md` — 底层同步机制
- `late-joiner-state-restore.md` — late joiner 恢复

## 相关 Scene Components

- `memory/world/scene-components/vrc-station.md` - **典型事件源**:`OnStationEntered` / `OnStationExited` 是本模式的常见事件源,实现"玩家坐下 → 状态机进入 ACTIVE 阶段"的转换
- `memory/world/scene-components/vrc-portalmarker.md` - **多 World 状态机**:Portal Marker 触发的 World 跳转是大型状态转换,可用本模式管理多 World 流程
