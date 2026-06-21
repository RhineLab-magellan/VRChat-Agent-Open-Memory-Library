# Pattern: Fade-Then-Snap（淡入淡出移动）

> Type: PATTERN
> Source: QuickBrown LuraSwitch2(参考工程) — `SwitchBoard.cs`
> Confidence: High
> SDK Version: VRChat SDK 3.x
> Last Verified: 2026-06-20

---

## Problem

物体需要**瞬时**位置更新（Pickup 重置、关卡切换、传送）：
- 直接 `transform.position = newPos` → 玩家看到"瞬移"，破坏沉浸感
- 插值移动 → 玩家看到"滑动"，但**有时**业务需要瞬时定位（重置/重置点）
- 完全淡出再淡入 → 玩家看不到移动，无违和感

## Context

- 平台重置到起点（玩家死亡/重置）
- 关卡切换时物体归位
- 拾取物在玩家放下后回到 Holder
- 任何"必须瞬时定位但又要视觉平滑"的场景

## Udon Constraints

- 协程不可用（无 StartCoroutine）
- `SendCustomEventDelayedSeconds` 用于时间间隔
- Fade 用 `MaterialPropertyBlock` 改 alpha 或 `CanvasGroup.alpha`
- Token 模式防止重入

## Solution: 3-Stage 隐藏移动

```csharp
[SerializeField] private Renderer _renderer;
[SerializeField] private CanvasGroup _canvasGroup;
[SerializeField] private float _moveFadeInSeconds = 0.3f;

// 1. 立即变透明
// 2. 瞬时移动(玩家看不到)
// 3. 淡入回来
public void TeleportWithFadeOut(Vector3 newPos, Quaternion newRot) {
    if (_fadeInStep != 0) return;  // 防止重入
    _fadeInStep = 1;
    ApplyAlphaImmediate(0f);  // 阶段 1:透明
    transform.SetPositionAndRotation(newPos, newRot);  // 阶段 2:移动
    StartFadeIn(_moveFadeInSeconds);  // 阶段 3:淡入
}
```

## Implementation Sketch

```csharp
public class FadeSnapMover : UdonSharpBehaviour {
    [SerializeField] private Renderer[] _renderers;
    [SerializeField] private CanvasGroup _canvasGroup;
    [SerializeField] private float _fadeInSeconds = 0.3f;

    private MaterialPropertyBlock _mpb;
    private float _alpha = 1f;
    private int _fadeInStep = 0;  // 0=idle, 1=fading in

    private void Start() {
        _mpb = new MaterialPropertyBlock();
    }

    public void TeleportWithFadeOut(Vector3 newPos, Quaternion newRot) {
        if (_fadeInStep != 0) return;  // 重入保护
        _fadeInStep = 1;

        // 阶段 1:瞬间透明
        ApplyAlpha(0f);

        // 阶段 2:移动(玩家看不到)
        transform.SetPositionAndRotation(newPos, newRot);

        // 阶段 3:启动淡入
        SendCustomEventDelayedFrames(nameof(TickFadeIn), 1);
    }

    public void TickFadeIn() {
        if (_fadeInStep != 1) return;
        _alpha += Time.deltaTime / _fadeInSeconds;
        if (_alpha >= 1f) {
            _alpha = 1f;
            _fadeInStep = 0;  // 退出淡入
        } else {
            SendCustomEventDelayedFrames(nameof(TickFadeIn), 1);
        }
        ApplyAlpha(_alpha);
    }

    private void ApplyAlpha(float alpha) {
        if (_canvasGroup != null) {
            _canvasGroup.alpha = alpha;
        }
        for (int i = 0; i < _renderers.Length; i++) {
            _renderers[i].GetPropertyBlock(_mpb);
            _mpb.SetFloat("_Alpha", alpha);
            // 或:_mpb.SetColor("_BaseColor", new Color(1,1,1,alpha));
            _renderers[i].SetPropertyBlock(_mpb);
        }
    }
}
```

## Networking Model

| 维度 | 决策 |
|------|------|
| State Owner | 物体 owner(若需同步) |
| Source of Truth | `[UdonSynced] Vector3 _targetPos` + `Quaternion _targetRot` |
| Sync Type | Manual Sync |
| Synced Variables | 2-3 个(位置/旋转/淡入状态) |
| Mutation Path | 玩家交互 → 修改 synced → 远端各自执行本地 fade |
| Ownership Path | Pickup / Interact 时 SetOwner |
| Serialization Path | 移动前 RequestSerialization |
| Receive Path | OnDeserialization → 本地触发 TeleportWithFadeOut |
| Late Joiner | 立即 snap 到 synced 位置 + alpha=1 |
| Conflict Strategy | 单一权威(无并发) |
| Bandwidth Budget | ~28B(3 vec3 + 1 quat) |
| Failure Mode | 玩家在 fade-in 中再次触发 → 重入保护(已实现) |

## Key Design Points

### 1. 重入保护 (FadeInStep Token)

```csharp
if (_fadeInStep != 0) return;  // 已在淡入中,忽略
_fadeInStep = 1;  // 标记"正在淡入"
```

**问题场景**:玩家在淡入过程中(0.3s 内)再次触发移动。
- 无保护:alpha 在 0 → 0.3 → 0(再次透明)→ 0.3 → 0.6(累加错误)
- 有保护:第 2 次调用直接 return(等当前淡入完成)

### 2. MaterialPropertyBlock 而非 sharedMaterial

```csharp
_renderer.GetPropertyBlock(_mpb);
_mpb.SetFloat("_Alpha", alpha);
_renderer.SetPropertyBlock(_mpb);
```

**为什么不用** `material.SetFloat(...)`:
- sharedMaterial 改动会污染 Asset(其他用同一材质的物体都变)
- MaterialPropertyBlock 是实例级,不影响其他人

### 3. 帧延迟 vs 时间延迟

| 方式 | 适用 |
|------|------|
| `SendCustomEventDelayedFrames(1)` | 短间隔(< 0.1s),帧率敏感 |
| `SendCustomEventDelayedSeconds(0.016)` | 跨平台,精确时间 |

**推荐**:用帧延迟(TickFadeIn 每帧调一次),简单且 60fps 下 = 0.016s/帧,精度足够。

### 4. Late Joiner 路径

```csharp
public override void OnDeserialization() {
    if (isFirstJoin) {
        // Late joiner:直接 snap 到 synced 位置
        transform.SetPositionAndRotation(_syncedPos, _syncedRot);
        ApplyAlpha(1f);  // 满 alpha,不淡入
    } else {
        // 状态变化:淡入淡出
        TeleportWithFadeOut(_syncedPos, _syncedRot);
    }
}
```

## When To Use

✅ **适合**:
- 玩家可见的"瞬时"位置更新(死亡重置、关卡切换)
- 物体**不能**用插值(如要严格定位到网格点)
- 玩家对位置变化敏感(VR 头显用户更敏感)
- 移动距离 > 0.5m(距离小则淡入淡出反而怪)

❌ **不适合**:
- 移动距离极小(< 0.1m,玩家察觉不到)
- 玩家需要看到移动过程(教学/演示)
- 移动中物体仍有功能(如抓握中的物体不能用 fade)
- 移动频率极高(> 5Hz,淡入淡出叠加混乱)

## When Not To Use

- 物理对象(应让物理引擎自然处理)
- 玩家持有中的物体(直接设位置即可)
- 隐身/透明的物体(无需 fade)

## Parameter Tuning

| 参数 | 范围 | 影响 |
|------|------|------|
| `_fadeInSeconds` | 0.1-0.5s | 淡入时长,值大=平滑但延迟 |
| 透明度下限 | 0 (完全透明) | 0.05+ 可能仍可见 |

**推荐配置**:
- VR 用户:`_fadeInSeconds = 0.4-0.5s`（VR 头显对突变更敏感）
- 桌面端:`_fadeInSeconds = 0.2-0.3s`
- 远距离移动:`_fadeInSeconds = 0.5s+`(让 fade 覆盖移动时间)

## Common Pitfalls

| 坑 | 后果 | 修复 |
|---|---|---|
| 无重入保护 | alpha 累加混乱 | `_fadeInStep` token |
| 直接改 `material.alpha` | 污染共享材质 | MaterialPropertyBlock |
| Update 中持续调淡入 | 浪费 CPU | 用 delayed frames 触发 |
| Late joiner 走 fade 路径 | 看到诡异淡入 | 区分首次 / 后续 |

## Cross-Reference

- `material-propertyblock-safe-update.md` - 共享材质安全更新
- `master-follower-syncer.md` - 同步位置/旋转
- `late-joiner-state-restore.md` - Late joiner 立即 snap

## Reference Implementation

`C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\01_Switch\SCRIPT\SwitchBoard.cs` (581 行)
