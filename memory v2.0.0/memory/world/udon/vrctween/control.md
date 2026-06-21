---
title: VRCTween 播放控制 + 设置 API
category: world
subcategory: udon/vrctween

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - vrctween
  - animation
  - tween
  - control

aliases:
  - "补间控制"
  - "VRCTween Control"
  - "Settings and Control"
  - "Play/Pause/Stop"

related:
  - ../index.md
  - basics.md
  - tween-types.md
  - sequence.md
  - patterns.md
  - ../animation-events.md

source: VRChat Creator Docs (https://creators.vrchat.com/worlds/udon/vrctween/settings/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# VRCTween 播放控制 + 设置 API

> 来源: https://creators.vrchat.com/worlds/udon/vrctween/settings/
> 抓取日期: 2026-06-21
> 状态: ✅ FACT (官方文档本地化)

---

## 概述

`VRCTweenHandle` 提供完整的**播放控制**、**状态查询**、**运行时配置**能力。控制方法立即生效;配置方法大多**返回 handle 用于链式调用**。

> 🔴 **关键约束**: 部分设置(`OnComplete` / `SetLoops` / `SetDelay` / `SetUpdate` / `From` / `SetSpeedBased`)必须**在 tween 启动前**(同帧)调用,否则可能不生效。
> 但 `SetDuration` / `SetEase` / `ChangeEndValue` **可在 tween 运行中调用**。

---

## 1. 控制方法(Control)

| 方法 | 描述 |
|---|---|
| `tweenHandle.Play()` | 恢复播放(从暂停 → 播放) |
| `tweenHandle.Pause()` | 暂停当前播放(返回 handle 可链) |
| `tweenHandle.Kill()` | 停止并销毁 tween |
| `tweenHandle.Complete()` | 立即跳到终点(并触发 OnComplete) |
| `tweenHandle.Restart()` | 从头重新开始 |
| `tweenHandle.Flip()` | 翻转播放方向(不启动,如果暂停) |
| `tweenHandle.PlayBackwards()` | 设置方向为倒放 + 播放 |
| `tweenHandle.PlayForwards()` | 设置方向为正放 + 播放 |
| `tweenHandle.Goto(time, andPlay)` | 跳转到指定时间(秒) |
| `VRCTween.KillAll()` | 销毁场景中所有 tween |
| `gameObject.KillAllTweens()` | 销毁该 GameObject 上所有 tween |

### 控制方法使用示例

```csharp
VRCTweenHandle _fade;

void Start()
{
    _fade = audioSource.TweenVolume(1f, 2f, VRCTweenEase.InSine)
        .OnRewind(this, nameof(OnFadeOut))
        .Pause();  // 创建后立刻暂停,等待事件触发
}

public void OnZoneEnter()
{
    _fade.PlayForwards();  // 正放: 音量 0 → 1
}

public void OnZoneExit()
{
    _fade.PlayBackwards(); // 倒放: 音量 1 → 0
}

public void OnFadeOut()
{
    // 倒放回到 0 触发(由 OnRewind 设置)
}
```

### Goto 用法 — Late joiner 同步

```csharp
[UdonSynced] float _tweenStartTime;
VRCTweenHandle _syncedTween;

void Start()
{
    _syncedTween = gameObject.TweenPosition(targetPos, 10f, VRCTweenEase.Linear)
        .SetLoops(-1, VRCTweenLoopType.Restart);
}

public override void OnDeserialization()
{
    // 晚加入的玩家: 用服务器时间算出"已经过了多久",跳到对应位置
    float elapsed = (float)(Networking.GetServerTimeInSeconds() - _tweenStartTime);
    _syncedTween.Goto(elapsed, true);  // 跳转 + 继续播放
}
```

> **`andPlay`**:
> - `true` → 跳转后继续播放
> - `false` → 跳转后暂停(用于编辑器预览对齐)

### 方向控制细节

- `Flip()` 只**切换方向**,不自动播放。如果当前是暂停,需要再 `Play()`
- `PlayBackwards()` 和 `PlayForwards()` **同时**设置方向 + 启动
- **倒放回 0 的 tween 不会自动 Kill**,保留以便再次反向。需要手动 Kill

---

## 2. 状态查询属性(Query)

| 属性 | 类型 | 描述 |
|---|---|---|
| `tweenHandle.IsValid` | `bool` | **关键**: handle 有效(对应一个真实 tween)时为 `true`,`default(VRCTweenHandle)` 为 `false` |
| `tweenHandle.IsPlaying` | `bool` | 正在播放中 |
| `tweenHandle.IsActive` | `bool` | tween 存在且未被 Kill |
| `tweenHandle.Elapsed` | `float` | 已播放时间(秒) |
| `tweenHandle.Duration` | `float` | 总时长(秒) |
| `tweenHandle.IsBackwards` | `bool` | 当前是否倒放 |

> 🔴 **`IsValid` vs `IsActive`**:
> - `IsValid` → "这个 handle 是不是有效的"(从未创建的 handle 是 `default`,IsValid=false)
> - `IsActive` → "这个 tween 还在不在"(被 Kill 后 IsActive=false)

```csharp
// 推荐模式: 检查 handle 是否有效
VRCTweenHandle h = cube.TweenPosition(badValue, 2f, VRCTweenEase.OutQuad);
if (h.IsValid)
{
    h.OnComplete(this, nameof(OnDone));
}
else
{
    Debug.LogWarning("Tween creation failed (invalid input)");
}
```

---

## 3. 设置方法(Settings)

### OnComplete(完成回调)

```csharp
door.TweenPosition(openPosition, 1f, VRCTweenEase.OutQuad)
    .OnComplete(this, nameof(OnDoorOpened));

public void OnDoorOpened() { /* 必须 public! */ }
```

| 参数 | 说明 |
|---|---|
| `callback` | 接收回调的 UdonBehaviour(传 `this`) |
| `eventName` | 自定义事件名(**必须 public 方法**) |

### OnRewind(倒放回到 0)

```csharp
audioSource.TweenVolume(1f, 2f, VRCTweenEase.InSine)
    .OnRewind(this, nameof(OnFadeComplete));
```

> **重要**: `OnRewind` **只在倒放回到 0 触发**,`Restart()` **不会**触发它。

### SetLoops(循环)

```csharp
tweenHandle.SetLoops(5, VRCTweenLoopType.Restart);
```

| `VRCTweenLoopType` | 行为 |
|---|---|
| `Restart` (0) | 每次循环重新从起点开始 |
| `Yoyo` (1) | 来回(正放 + 倒放) |
| `Incremental` (2) | 每次循环的终点累加(适合"持续旋转") |

```csharp
// 无限循环巡逻
.SetLoops(-1, VRCTweenLoopType.Restart);

// 来回 5 次
.SetLoops(5, VRCTweenLoopType.Yoyo);

// 持续匀速旋转
.SetLoops(-1, VRCTweenLoopType.Incremental);
```

### SetDelay(延迟)

```csharp
tweenHandle.SetDelay(1.5f);  // 1.5 秒后才开始
```

> **负数/NaN/Inf 静默忽略**。仅 0 和正数有效。

### SetUpdate(更新阶段)

```csharp
tweenHandle.SetUpdate(VRCTweenUpdateType.LateUpdate);
```

| `VRCTweenUpdateType` | 何时更新 |
|---|---|
| `Update` (0) | MonoBehaviour Update(默认) |
| `LateUpdate` (1) | 所有 Update 之后 |
| `FixedUpdate` (2) | 物理帧 |
| `PostLateUpdate` (3) | **关键**: 所有 LateUpdate 之后 → **覆盖相机/IK** |

> **PostLateUpdate 用例**: 让 VRCTween 驱动的相机移动在所有 IK、Camera 系统之后执行,避免抖动。

### From(翻转起点终点)

```csharp
public GameObject notification;  // 已经在场景中的目标位置

void Start()
{
    // 从 (0, 10, 0) 飞到当前场景中的位置
    notification.TweenPosition(new Vector3(0, 10, 0), 1f, VRCTweenEase.OutBounce)
        .From();  // 起点=目标值(0,10,0), 终点=当前位置
}
```

> 适用场景:"出现动画" — 物体已经在最终位置,从一个偏离点飞过来。
> **仅对非虚拟补间有效**。必须**创建后立即**调用。

### SetSpeedBased(速度模式)

```csharp
// duration = 5 含义: 5 单位/秒(而不是 5 秒)
gameObject.TweenPosition(targetPos, 5f, VRCTweenEase.Linear)
    .SetSpeedBased();
```

> 适用: 相机匀速运动、跨不同距离都保持**视觉速度一致**。
> **必须创建后立即调用**。

### SetEase(覆盖缓动)

```csharp
// 预设
tweenHandle.SetEase(VRCTweenEase.OutBounce);

// 自定义 AnimationCurve
public AnimationCurve customEase;
tweenHandle.SetEase(customEase);
```

> 接受 `VRCTweenEase` 预设 **或** `AnimationCurve`。
> 可在 tween 运行中调用,过渡更平滑。

### SetDuration(运行时修改时长)

```csharp
tweenHandle.SetDuration(3f);  // 改成 3 秒
```

> **负数/NaN/Inf 静默忽略**。
> 可在 tween 运行中调用。

### ChangeEndValue(运行时改终点)

```csharp
tweenHandle.ChangeEndValue(new Vector3(10, 0, 0), true);
```

| 参数 | 说明 |
|---|---|
| `newEndValue` | 新终点(类型必须匹配:Vector3/float/Color/Vector2) |
| `snapStartValue` | `true` → 把起点改为当前值(避免跳回原点) |

> **使用场景**: 热路径复用(相机跟随)。
> **不可用**: 虚拟 Color/Vector3 补间、Renderer 补间、Light 补间、Path 补间。

```csharp
VRCTweenHandle _moveHandle;

void Start()
{
    _moveHandle = gameObject.TweenPosition(Vector3.zero, 1f, VRCTweenEase.OutQuad)
        .SetLoops(-1, VRCTweenLoopType.Restart)
        .Pause();
}

public void MoveTo(Vector3 target, float duration)
{
    _moveHandle.ChangeEndValue(target, true)   // 起点 = 当前位置
        .SetDuration(duration)
        .SetEase(VRCTweenEase.OutCubic);
    _moveHandle.Restart();
}
```

---

## 4. Tween 复用(热路径优化)

> **何时使用**: 相机跟随、UI 跟随移动目标、每帧重定向。
> **何时不用**: 一次性动画(按钮按下、门开关) — 杀+重建更清晰。

```csharp
public class CameraFollower : UdonSharpBehaviour
{
    public Transform target;
    public float defaultDuration = 0.5f;
    private VRCTweenHandle _moveHandle;

    void Start()
    {
        // 一次创建,无限循环(保持存活),初始暂停
        _moveHandle = gameObject.TweenPosition(
            target.position, 1f, VRCTweenEase.OutQuad
        )
        .SetLoops(-1, VRCTweenLoopType.Restart)
        .Pause();
    }

    public void MoveTo(Vector3 targetPos, float duration)
    {
        _moveHandle.ChangeEndValue(targetPos, true)  // 起点=当前位置
            .SetDuration(duration)
            .SetEase(VRCTweenEase.OutCubic);
        _moveHandle.Restart();
    }
}
```

> **性能基准(官方内部)**: 500 tween × 300 帧,复用模式比 kill-and-recreate:
> - 内存分配 **少 46 倍**
> - 速度 **快 10 倍**

---

## 5. 路径类型

| `VRCTweenPathType` | 描述 |
|---|---|
| `Linear` | 直线段连接 waypoint |
| `CatmullRom` | 平滑曲线(默认 resolution 10,可 clamp 1-50) |

---

## 6. 缓动类型完整列表(31 种)

> 详细描述见 `basics.md` 的"缓动速查"章节,这里列所有可用值:

```
Linear
InSine / OutSine / InOutSine
InQuad / OutQuad / InOutQuad
InCubic / OutCubic / InOutCubic
InQuart / OutQuart / InOutQuart
InQuint / OutQuint / InOutQuint
InExpo / OutExpo / InOutExpo
InCirc / OutCirc / InOutCirc
InElastic / OutElastic / InOutElastic
InBack / OutBack / InOutBack
InBounce / OutBounce / InOutBounce
```

**实用选择**:
- `OutQuad` → UI 默认(自然减速)
- `InOutSine` → 相机平滑
- `OutBack` → 按钮回弹(过冲感)
- `OutElastic` → 玩具/角色弹性
- `OutBounce` → 物理落地
- `Linear` → 匀速轮播/转盘

---

## 7. 输入验证规则(静默)

| API | 无效输入 | 行为 |
|---|---|---|
| 创建方法 | `target=null` | 返回 invalid handle |
| 创建方法 | `duration < 0` / NaN / Inf | 返回 invalid handle(0 允许) |
| 创建方法 | 位置/缩放/路径点含 NaN/Inf 或 \|值\|>~520,000 | 返回 invalid handle |
| 创建方法 | path `resolution` 超出 1-50 | 静默 clamp,tween 仍创建 |
| `SetDuration` | 负数/NaN/Inf | 静默忽略(0 允许) |
| `SetDelay` | 负数/NaN/Inf | 静默忽略 |
| `Goto` | NaN/Inf | 静默忽略;否则 clamp 到 [0, duration] |
| `ChangeEndValue` | 无效 float/vector | 静默忽略 |

> **最佳实践**: 创建后 `if (handle.IsValid)` 分支处理。

---

## 8. 生命周期管理

| 场景 | 推荐做法 |
|---|---|
| 一次性 tween | 不用管(完成自动清理) |
| 有限次循环(5 次) | 不用管(完成自动清理) |
| 无限循环(`-1`) | `OnDestroy` 调 `KillAllTweens` |
| GameObject 频繁创建/销毁 | 在 `OnDestroy` 调 `KillAllTweens` |
| 玩家退出实例 | VRCTween 自动清理(系统级) |

```csharp
public override void OnDestroy()
{
    gameObject.KillAllTweens();  // 清当前 GameObject 上所有 tween
}

public void OnWorldCleanup()
{
    VRCTween.KillAll();  // 清场景所有 tween(慎用)
}
```

---

## 9. 限制与陷阱

### 不会自动同步

> 🔴 **每个玩家看到的 tween 是本地独立播放的**。需要同步必须用 `[UdonSynced]` 时间戳 + `Goto()`。

### Tween 句柄唯一性

> 句柄**每个场景实例独立**。`VRCTweenHandle` 是**结构体**,不持有引用,失效后变 `default`。

### 短时长不稳定

> `duration < 0.01` 可能不平滑。最小推荐 `0.05+`。

### Udon Graph 集成

> 1. 搜节点 "VRCTween TweenPosition" 或其他创建方法
> 2. 连接 GameObject + 参数
> 3. 节点输出 `VRCTweenHandle`
> 4. 用 `VRCTweenHandle` 节点(Kill/Pause/SetDelay/OnComplete)控制

---

## 官方文档子页面对应

| 本文件章节 | 官方页面 |
|---|---|
| 全部内容 | `https://creators.vrchat.com/worlds/udon/vrctween/settings`/ |
