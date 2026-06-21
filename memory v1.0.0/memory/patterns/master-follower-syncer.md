# Pattern: Master-Follower Syncer（主从同步器）

> Type: PATTERN
> Source: QuickBrown LuraSwitch2(参考工程) — `SwitchSyncer.cs`
> Confidence: High
> SDK Version: VRChat SDK 3.x
> Last Verified: 2026-06-20

---

## Problem

多个同类型对象（Toggle / Slider / Selector）需要在 Master 端集中控制：
- 玩家操作任一对象 → 触发所有其他对象更新
- 多 Master 抢占 → 单一权威源
- Late joiner 需要拿到当前权威值
- 频次高（每帧或每 0.1s）但不能打爆带宽

## Context

- 多通道开关控制（如 8 个灯的 1 个总开关）
- 滑块/推子集中同步（如多通道音量）
- 多关卡选择器联动
- 任何"1 Master + N Followers" 拓扑

## Udon Constraints

- Manual Sync 每次序列化有 header 开销（~10 bytes）
- 大量独立 `[UdonSynced]` 字段拖慢 OnDeserialization
- 直接 SendCustomNetworkEvent 不能恢复 Late joiner
- 单一 Behaviour 同步所有值可压缩到 1 次序列化

## Networking Model

| 维度 | 决策 |
|------|------|
| State Owner | Master（由 `EnsureGlobalOwnership` 抢占） |
| Source of Truth | Syncer 内部 `[UdonSynced]` 字段 |
| Sync Type | Manual Sync + 节流（默认 0.1s） |
| Synced Variables | 集中的 state array（如 `byte[] _states`） |
| Mutation Path | Master 端通过 `QueueSync` 累积到节流窗口结束 |
| Ownership Path | OnPlayerJoined / OnDeserialization 主动抢 owner |
| Serialization Path | `RequestSerialization` 在节流 tick 触发 |
| Receive Path | `OnDeserialization` → 写入 `_syncedXXX` → 通知 Followers |
| Late Joiner | Master 端主动重新广播（`RequestSerialization`） |
| Conflict Strategy | Master 权威；多玩家抢时 Instance Master 兜底 |
| Bandwidth Budget | 1 个包 / 0.1s = ~10 KB/s 内可承受 |
| Failure Mode | 丢包 → 下个 tick 重传（容忍少量丢包） |

## Implementation Sketch

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class SwitchSyncer : UdonSharpBehaviour {
    [SerializeField] private SwitchBase[] _switches;
    [SerializeField] private float _syncIntervalSeconds = 0.1f;

    private bool _serializationPending = false;
    private bool _initialized = false;

    public override void OnPlayerJoined(VRCPlayerApi player) {
        if (!Networking.IsOwner(gameObject)) return;
        // 新玩家加入时主动同步,避免 Late joiner 状态缺失
        RequestSerialization();
    }

    /// <summary>
    /// 由 SwitchBase 在状态变化时调用（同一 Frame 内多次调用合并为 1 次）
    /// </summary>
    public void QueueSync() {
        if (_serializationPending) return;
        _serializationPending = true;
        SendCustomEventDelayedSeconds(nameof(ProcessSync), _syncIntervalSeconds);
    }

    public void ProcessSync() {
        _serializationPending = false;
        if (!Networking.IsOwner(gameObject)) return;
        RequestSerialization();
    }

    public override void OnDeserialization() {
        // 把 _syncedXXX 推给各 Follower
        for (int i = 0; i < _switches.Length; i++) {
            var s = _switches[i];
            if (s.IsInterpolating && !s.IsInterpolationApplyingOutput) continue; // 排除自身回声
            s.ApplyValueFromExternalWithTimeVisualOnly(
                _syncedValues[i], ..., ...);
        }
    }

    private void EnsureGlobalOwnership() {
        if (!Networking.IsOwner(gameObject)) {
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        }
    }
}
```

## Key Design Points

### 1. Master 抢占 (`EnsureGlobalOwnership`)

```csharp
// 每次 OnPlayerJoined / OnDeserialization 主动检查
if (!Networking.IsOwner(gameObject)) {
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
}
```
**关键**：不在 OnPlayerJoined 抢（时序不可靠），统一在 OnDeserialization 抢。

### 2. 节流窗口 (`QueueSync`)

```csharp
if (_serializationPending) return;  // 已在排队,忽略
_serializationPending = true;
SendCustomEventDelayedSeconds(nameof(ProcessSync), 0.1f);
```
**关键**：0.1s 窗口内的多次修改合并为 1 次序列化。窗口结束后检查 `_dirty` 标志,确认有变化再 `RequestSerialization`。

### 3. 回声排除 (`IsInterpolating` + `IsInterpolationApplyingOutput`)

```csharp
// 双标志:IsInterpolating 期间,排除"自己刚发的回声"
if (s.IsInterpolating && !s.IsInterpolationApplyingOutput) continue;
```
- `IsInterpolating = true`：正在向目标值插值
- `IsInterpolationApplyingOutput = true`：插值器**正在输出**到 synced 值（说明是 Master 自己刚改的）
- 只有"非输出"状态才是远端推送,需要本地应用

### 4. Follower 视觉同步 (`ApplyValueFromExternalWithTimeVisualOnly`)

```csharp
// Follower 端:不写回 synced 字段,只更新表现
s.ApplyValueFromExternalWithTimeVisualOnly(v, ..., sliderSyncInterpolationTime);
```
- Follower 端**不调用** `RequestSerialization`
- 只更新本地视觉表示(Transform / Material / Animation)

## When To Use

✅ **适合**:
- 1 个 Master 集中控制 N 个同类型对象
- N > 4 时(节省带宽)
- 玩家可能切换 Master(如第一个玩家退出后第二个接管)
- 需要节流避免序列化风暴

❌ **不适合**:
- 每个对象独立运作(直接 Manual Sync 即可)
- N ≤ 2(节省效益不显著)
- 对象类型不同(无统一 state schema)

## When Not To Use

- 子对象已独立 Manual Sync 状态(双层同步浪费)
- 实时性要求极高(< 0.1s 窗口过大)
- 对象间无联动需求

## Performance

- **带宽**: 1 包 / 0.1s ≈ 10 包/s × 200B = 2KB/s(单 Master)
- **CPU**: Follower 端 OnDeserialization 遍历 N 个子对象(O(N),N ≤ 32 通常无压力)
- **内存**: 1 个 `[UdonSynced]` 数组 + 1 个本地缓存数组 = 2N 字节(N=8 时 = 16 字节)

## Common Pitfalls

| 坑 | 后果 | 修复 |
|---|---|---|
| 忘记 `EnsureGlobalOwnership` | Master 退场后无权威 | OnDeserialization 主动检查 |
| 节流窗口太长(>0.5s) | 玩家操作反馈迟钝 | 默认 0.1s,操作密集时 0.05s |
| Follower 误调 `RequestSerialization` | 同步风暴 | Follower 端用 `IsOwner` return 守卫 |
| 新玩家加入未重新广播 | Late joiner 状态缺失 | OnPlayerJoined 主动 RequestSerialization |

## Cross-Reference

- `manual-sync-state.md` - 基础 Manual 模式
- `advanced-sync-patterns.md` - Rate-Limited Serialization（节流窗口思想来源）
- `owner-authoritative-interaction.md` - Owner 抢占模式
- `late-joiner-state-restore.md` - Late joiner 恢复

## Reference Implementation

`C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\01_Switch\SCRIPT\SwitchSyncer.cs` (736 行)
