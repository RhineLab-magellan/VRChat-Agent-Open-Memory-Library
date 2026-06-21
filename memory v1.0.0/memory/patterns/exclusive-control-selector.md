# Pattern: Exclusive Control Selector（互斥选择器）

> Type: PATTERN
> Source: QuickBrown LuraSwitch2(参考工程) — `SwitchSelector.cs`
> Confidence: High
> SDK Version: VRChat SDK 3.x
> Last Verified: 2026-06-20

---

## Problem

需要"多选一"互斥控制：
- 4 个开关组成"四选一"组,激活一个时其他自动关闭
- 多关卡同时只能激活一个
- 多模式同时只能选一个
- 传统做法:4 个独立开关 + 4 个 Manual Sync = 4 次序列化(浪费 + 状态可能不一致)

## Context

- 关卡选择器(关卡 A/B/C/D)
- 模式切换(PvP / PvE / Casual)
- 楼层跳转(B1 / 1F / 2F / 3F)
- 主题切换(白天 / 夜晚 / 黄昏)
- 任何"互斥集合"控制

## Udon Constraints

- 多个独立 `[UdonSynced]` 字段同步互斥状态浪费带宽
- 客户端独立关闭其他开关可能导致"瞬时不一致"(其他玩家看到 2 个开关同时亮)
- 子对象的 syncMode 时序与 Selector 初始化有依赖关系

## Networking Model

| 维度 | 决策 |
|------|------|
| State Owner | Selector(单一) |
| Source of Truth | Selector 的 `_activeIndex` (int/byte) |
| Sync Type | Manual Sync(1 个变量) |
| Synced Variables | `_activeIndex` (byte) + 可选 `_allowAllOff` (bool) |
| Mutation Path | Selector 内部:子开关通过回调通知 → 改 `_activeIndex` |
| Ownership Path | 通过 `EnsureGlobalOwnership` 抢占 |
| Serialization Path | Selector 自身 `RequestSerialization` |
| Receive Path | OnDeserialization → 强制所有子开关到对应状态 |
| Late Joiner | 同上(自动) |
| Conflict Strategy | 集中权威,无并发可能 |
| Bandwidth Budget | 1 byte / change ≈ 200B 包 |
| Failure Mode | 子开关 syncMode 未被强制改写 → 双重同步 |

## Implementation Sketch

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class SwitchSelector : UdonSharpBehaviour {
    [SerializeField] private SwitchBase[] _switches;
    [SerializeField] private bool _allowAllOff = false;
    [SerializeField] private int _activeIndex = -1;  // -1 = 全部关闭

    [UdonSynced] private byte _syncedActiveIndex = 255;  // 255 = 未初始化
    [UdonSynced] private bool _syncedAllowAllOff = false;

    public override void OnSwitchStateChanged(SwitchBase changedSwitch, bool isOn) {
        if (!Networking.IsOwner(gameObject)) return;

        int changedIndex = System.Array.IndexOf(_switches, changedSwitch);
        if (isOn) {
            EnforceExclusive(changedIndex);  // 强制关闭其他
            _activeIndex = changedIndex;
            _syncedActiveIndex = (byte)changedIndex;
        } else {
            if (!_allowAllOff && _activeIndex == changedIndex) {
                // 不允许全关,强制重新打开
                changedSwitch.ForceSetOn();
                return;
            }
            _activeIndex = -1;
            _syncedActiveIndex = 255;
        }
        RequestSerialization();
    }

    private void EnforceExclusive(int keepIndex) {
        for (int i = 0; i < _switches.Length; i++) {
            if (i == keepIndex) continue;
            _switches[i].SetStateImmediate(false);  // 强制关,不走回调
        }
    }

    /// <summary>
    /// 强制覆盖子开关的 syncMode 为 NoVariableSync,
    /// 避免双重同步
    /// </summary>
    public void ForceSyncModeToSwitches() {
        for (int i = 0; i < _switches.Length; i++) {
            _switches[i].ForceSyncModeNone();
        }
    }

    public override void OnDeserialization() {
        // 把 synced 索引应用到所有子开关
        for (int i = 0; i < _switches.Length; i++) {
            _switches[i].SetStateImmediate(i == _syncedActiveIndex);
        }
    }

    /// <summary>
    /// 延迟 1 帧初始化,确保子开关 Start() 先跑完
    /// </summary>
    public void DeferredInitialize() {
        ForceSyncModeToSwitches();
        EnsureGlobalOwnership();
    }
}
```

## Key Design Points

### 1. 集中权威(Selector 唯一 `[UdonSynced]`)

| 方案 | synced 字段数 | 包大小 / 切换 |
|------|--------------|------------|
| 4 个独立开关 | 4 | ~800B |
| 1 个 Selector 集中 | 1 | ~200B |

**75% 带宽节省**。

### 2. 强制覆盖子开关 syncMode

```csharp
public void ForceSyncModeToSwitches() {
    for (int i = 0; i < _switches.Length; i++) {
        _switches[i].ForceSyncModeNone();  // 强制 NoVariableSync
    }
}
```
**为什么必需**：子开关默认 Manual Sync + `[UdonSynced]`,会与 Selector 重复同步。强制覆盖后,子开关只听 Selector 调度。

### 3. 1 帧延迟初始化(规避时序陷阱)

```csharp
private void Start() {
    SendCustomEventDelayedFrames(nameof(DeferredInitialize), 1);
}

public void DeferredInitialize() {
    ForceSyncModeToSwitches();  // 此时子开关 Start() 已完成
    EnsureGlobalOwnership();
}
```

**核心问题**:
- 子开关 `Start()` 可能在 Selector `Start()` **之前或之后**(Udon 不保证顺序)
- 如果 Selector 立即强制 `NoVariableSync`,子开关的 `OnDeserialization` 会跳过 IsGlobal 分支
- **必须延迟 1 帧**等所有子对象 Start 跑完

### 4. `_allowAllOff` 灵活性

```csharp
if (!_allowAllOff && _activeIndex == changedIndex) {
    changedSwitch.ForceSetOn();  // 必须保持一个开
    return;
}
```
支持"必须选一个"(单选) vs "可全关"(取消选择) 两种语义。

## When To Use

✅ **适合**:
- 任何"多选一"互斥场景
- N ≥ 3 时(节省带宽显著)
- 客户端可观测状态(玩家需要看到谁被选)
- 状态变化频率低(切换 < 1Hz)

❌ **不适合**:
- 多个独立开关(无互斥需求)
- 切换频率极高(> 5Hz,中央同步成为瓶颈)
- 状态不需要同步到客户端

## When Not To Use

- N = 2(2 个独立开关更简单)
- 客户端无需知道哪个被选(直接 SendCustomNetworkEvent 即可)
- 切换+选择逻辑耦合复杂(拆分后状态机爆炸)

## Common Pitfalls

| 坑 | 后果 | 修复 |
|---|---|---|
| 子开关 syncMode 未强制覆盖 | 双层同步,带宽翻倍 | `ForceSyncModeToSwitches` |
| 立即强制 syncMode(不等 1 帧) | 时序错乱,初始化失败 | `SendCustomEventDelayedFrames(1)` |
| `_allowAllOff` 未设计 | 玩家点掉最后一个后无法恢复 | 默认 false,提供 Inspector 选项 |
| Follower 端未禁用子开关输入 | 远端玩家可独立关掉子开关 | OnDeserialization 后强制 `SetStateImmediate` |

## Performance

- **带宽**: 1 byte / 切换 ≈ 200B 包
- **CPU**: Selector OnDeserialization O(N),子开关状态应用 O(1) 每个
- **内存**: 1 个 `[UdonSynced]` byte + 1 个 `[UdonSynced]` bool = 2 字节 synced 字段

## Cross-Reference

- `master-follower-syncer.md` - 主从同步的另一种拓扑
- `manual-sync-state.md` - 基础 Manual 模式
- `event-driven-state-machine.md` - Selector 内部可用事件驱动
- `owner-authoritative-interaction.md` - Master 权威模式

## Reference Implementation

`C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\03_ModeSwitch\SCRIPT\SwitchSelector.cs` (849 行)
