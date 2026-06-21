---
title: Pattern: Soft Detent Interpolation（软吸附插值）
category: patterns

knowledge_level: applied
status: active

tags:
  - patterns
  - patterns
  - udonsharp

aliases:
  - "Soft Detent Interpolation（软吸附插值）"
  - "软吸附插值"

source: QuickBrown LuraSwitch2(参考工程) — `SliderSwitch.cs` (段への吸着 / SoftDetent)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Pattern: Soft Detent Interpolation（软吸附插值）

> ⚠️ **历史版本标注** — 本 Pattern 基于 LuraSwitch2 v3.00 (2023) 提炼
> 当前 LuraSwitch2 已重写为 v1.06 (2026-03-06, VN3 License)
> Pattern 核心思想(SmoothStep 软磁力 + 完全吸附阈值)在 Udon 沙箱中仍是通用解法
> 详见 `world/luraswitch2.md` v1.06 工具使用指南

---

## Problem

滑块需要在"段位"附近自动吸附（如 0%, 25%, 50%, 75%, 100%），但**完全硬 snap 会跳变，完全不 snap 又难以精确定位**。需要中间最优解：
- 段位附近：增加"磁力"，玩家松手后自动吸附
- 段位之间：自由滑动
- 完全吸附：值严格等于段位
- 平滑过渡：吸附过程不能突兀

## Context

- 多段位开关（OFF / LOW / MID / HIGH）
- 音量/亮度/温度调节
- 速度/功率档位
- 任何"段位+连续值"混合滑块

## Mathematical Foundation

### 核心公式：磁力系数计算

```csharp
float rawValue = /* 玩家拖到的位置 */;
float nearestSnap = /* 最近的段位值 */;
float distance = Mathf.Abs(rawValue - nearestSnap);
float snapRange = /* 吸附作用半径,默认 0.1 */;

// 核心:基于 SmoothStep 的非线性磁力
float magnetism = 1f - Mathf.SmoothStep(0f, snapRange, distance);
//  distance = 0      → magnetism = 1 (完全吸附)
//  distance = snapRange → magnetism = 0 (无影响)
//  distance = snapRange/2 → magnetism = 0.5 (中等)

float snappedValue = Mathf.Lerp(rawValue, nearestSnap, magnetism);
```

### 完整算法(基于 QuickBrown 实现)

```csharp
[SerializeField] private int _stepCount = 4;  // 4 段
[SerializeField] private float _softDetentRange = 0.12f;  // 吸附半径
[SerializeField] private float _snapRange = 0.02f;  // 完全吸附阈值

public float ApplySoftDetent(float rawValue) {
    if (_stepCount <= 1) return rawValue;  // 无段位,直接返回

    float stepSize = 1f / (_stepCount - 1);  // 0, 0.333, 0.667, 1.0

    // 1. 找最近段位
    int nearestStep = Mathf.RoundToInt(rawValue / stepSize);
    nearestStep = Mathf.Clamp(nearestStep, 0, _stepCount - 1);
    float nearestSnap = nearestStep * stepSize;

    // 2. 计算磁力(基于 SmoothStep)
    float distance = Mathf.Abs(rawValue - nearestSnap);
    float magnetism = 1f - Mathf.SmoothStep(0f, _softDetentRange, distance);

    // 3. 插值
    float result = Mathf.Lerp(rawValue, nearestSnap, magnetism);

    // 4. 完全吸附阈值内:硬 snap
    if (distance < _snapRange) {
        result = nearestSnap;
    }

    return result;
}
```

## Networking Model

| 维度 | 决策 |
|------|------|
| State Owner | Slider 的 owner |
| Source of Truth | `[UdonSynced] float _syncedSliderValue` |
| Sync Type | Manual Sync + 节流 |
| Synced Variables | 1 个 float（精度可接受） |
| Mutation Path | Master 在 Update 中应用 SoftDetent 后写回 synced |
| Ownership Path | Interact 时 SetOwner |
| Serialization Path | 节流后 RequestSerialization |
| Receive Path | OnDeserialization → 插值到目标值 |
| Late Joiner | Snap 到 synced 值(不插值) |
| Conflict Strategy | 玩家松手后值才同步,避免拖动中频繁序列化 |
| Bandwidth Budget | 1 float / 切换 ≈ 4-8B 包 |
| Failure Mode | SoftDetent 范围过大 → 滑块难拖到非段位位置 |

## Implementation Sketch

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class SoftDetentSlider : UdonSharpBehaviour {
    [SerializeField] private int _stepCount = 4;
    [SerializeField] private float _softDetentRange = 0.12f;
    [SerializeField] private float _snapRange = 0.02f;
    [SerializeField] private float _interpolationTime = 0.3f;

    [UdonSynced] private float _syncedValue;
    private float _displayedValue;
    private bool _isDragging = false;

    public override void OnPickup() {
        _isDragging = true;
        Networking.SetOwner(Networking.LocalPlayer, gameObject);
    }

    public override void OnDrop() {
        _isDragging = false;
        // 玩家松手:应用最终 SoftDetent,再同步
        _syncedValue = ApplySoftDetent(_displayedValue);
        RequestSerialization();
    }

    private void Update() {
        if (!_isDragging) return;
        if (!Networking.IsOwner(gameObject)) return;

        // 拖动中:本地应用 SoftDetent(实时反馈)
        float rawValue = /* 从 controller 读取 */;
        _displayedValue = ApplySoftDetent(rawValue);
        ApplyToHandle(_displayedValue);
    }

    private float ApplySoftDetent(float rawValue) {
        if (_stepCount <= 1) return rawValue;
        float stepSize = 1f / (_stepCount - 1);
        int nearestStep = Mathf.RoundToInt(rawValue / stepSize);
        nearestStep = Mathf.Clamp(nearestStep, 0, _stepCount - 1);
        float nearestSnap = nearestStep * stepSize;
        float distance = Mathf.Abs(rawValue - nearestSnap);
        float magnetism = 1f - Mathf.SmoothStep(0f, _softDetentRange, distance);
        float result = Mathf.Lerp(rawValue, nearestSnap, magnetism);
        if (distance < _snapRange) result = nearestSnap;
        return result;
    }
}
```

## Visual Curve

SmoothStep 曲线在 `distance / snapRange` 上的表现：

```
magnetism
1.0 |**                                       (完全吸附)
    |  ***
0.5 |     *****                              (中等磁力)
    |          *******
0.0 |________________ ********_____           (无影响)
    0   0.25  0.5  0.75  1.0+
    distance / snapRange
```

**特征**:
- 距离 0：完全吸附(1.0)
- 距离 50% snapRange：中等磁力(0.5)
- 距离 ≥ snapRange：无影响(0.0)
- 曲线平滑(SmoothStep 的二阶连续)

## When To Use

✅ **适合**:
- 滑块有"标准档位"（如音量 0/25/50/75/100）
- 玩家期望"自然吸附"而非"卡顿定位"
- 段位数 ≤ 10（太多段位计算成本上升）
- 视觉/物理对象（Handle 位置、灯光亮度）

❌ **不适合**:
- 段位数 > 20（计算成本高，玩家难以区分）
- 玩家需要**严格连续值**（如角度微调）
- 实时绘制（拖动过程中不能有吸附感）

## When Not To Use

- 0% ~ 100% 自由值（如 RGB 调色）
- 多维控制（如 XYZ 位置，3 个轴各自 SoftDetent 会卡顿）
- 数学公式驱动的值（如 sin(t)、物理模拟）

## Parameter Tuning

| 参数 | 范围 | 影响 |
|------|------|------|
| `_stepCount` | 2-10 | 段位数,过密反而难用 |
| `_softDetentRange` | 0.05-0.2 | 吸附半径,值大=难拖离段位 |
| `_snapRange` | 0.01-0.05 | 完全吸附阈值,值大=明显跳变 |
| `_interpolationTime` | 0.1-0.5s | 远端插值时间,值大=平滑但延迟 |

**推荐配置**:
- 4 段 OFF/LOW/MID/HIGH:`_stepCount=4, _softDetentRange=0.12, _snapRange=0.02`
- 5 段音量:`_stepCount=5, _softDetentRange=0.1, _snapRange=0.015`

## Common Pitfalls

| 坑 | 后果 | 修复 |
|---|---|---|
| 拖动中也调 `RequestSerialization` | 序列化风暴 | 只在 OnDrop 时同步 |
| `snapRange > softDetentRange` | 永远到不了非段位 | snapRange 应远小于 softDetentRange |
| stepCount 太大(>10) | 玩家卡顿,难用 | 限制在 2-10 |
| 未区分拖动/松手 | 玩家松手后值"漂移" | OnDrop 时强制重新 ApplySoftDetent |
| Float 同步精度不足 | 远端值微小偏差累积 | LocalSave 模式 ×100 整数化 |

## Performance

- **CPU**: 每次 ApplySoftDetent = 1 Round + 1 Abs + 1 SmoothStep + 1 Lerp = ~5 指令
- **拖动中**: Update 每帧调用 = ~5 指令(可接受)
- **松手时**: 1 次 Apply + 1 次同步 = ~10 指令
- **远端**: 1 个 float 反序列化 + SmoothDamp 插值 = ~3 指令/帧

## Cross-Reference

- `master-follower-syncer.md` - 滑块值通常由 Syncer 节流
- `manual-sync-state.md` - 基础 Manual 模式
- `late-joiner-state-restore.md` - 远端 snap 不插值

## Reference Implementation

`C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\01_Switch\SCRIPT\SliderSwitch.cs` (2218 行,含 SoftDetent 实现)
