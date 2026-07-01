---
title: VRCTween 常用模式
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
  - patterns
  - best-practices

aliases:
  - "补间模式"
  - "VRCTween Patterns"
  - "常见用法"
  - "Best Practices"
  - "UI 淡入淡出"
  - "按钮回弹"
  - "相机跟随"

related:
  - ../index.md
  - basics.md
  - tween-types.md
  - control.md
  - sequence.md
  - custom-tween.md
  - ../animation-events.md
  - ../ui-events.md

source: VRChat Creator Docs (https://creators.vrchat.com/worlds/udon/vrctween/)
source_type: community
version: 1.0
last_review: 2026-06-21
confidence: High
---

# VRCTween 常用模式

> 来源: VRChat Creator Docs + 社区最佳实践
> 抓取日期: 2026-06-21
> 状态: ✅ FACT + PATTERN(官方文档 + 实战模式)

---

## 概述

本文档汇总**创作者最常写**的 VRCTween 模式,每个模式都给出**完整可编译**的 UdonSharp 代码,以及**已知陷阱**与**性能注意事项**。

> **核心原则**:
> 1. **创建前先 Kill 旧 tween**(防止快速点击重叠)
> 2. **OnDestroy 必须 KillAllTweens**(无限循环必须清理)
> 3. **热路径用复用模式**(每帧或每事件)
> 4. **检查 IsValid**(输入验证失败不报错)
> 5. **同步动画用 Goto + Synced 时间戳**

---

## 模式 1: 按钮按下回弹

> 最常见的 UI 反馈:点击 → 弹大 → 弹回

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class BouncyButton : UdonSharpBehaviour
{
    public GameObject button;
    private VRCTweenHandle _tween;

    public override void Interact()
    {
        // 1. Kill 旧 tween(快速点击时)
        if (_tween.IsValid) _tween.Kill();

        // 2. 弹大 → 弹回
        _tween = button.TweenScale(Vector3.one * 1.3f, 0.1f, VRCTweenEase.OutQuad)
            .OnComplete(this, nameof(ResetScale));
    }

    public void ResetScale()
    {
        _tween = button.TweenScale(Vector3.one, 0.25f, VRCTweenEase.OutElastic);
    }

    public override void OnDestroy()
    {
        button.KillAllTweens();
    }
}
```

**关键细节**:
- `_tween.IsValid` 检查(默认值无效)
- `OutElastic` 弹回(过冲感)
- 两个阶段用不同 `duration`(弹大快、弹回慢)

---

## 模式 2: UI 淡入淡出(整组面板)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class UIPanelController : UdonSharpBehaviour
{
    public CanvasGroup panel;

    public void ShowPanel()
    {
        panel.gameObject.SetActive(true);
        panel.TweenFade(1f, 0.5f, VRCTweenEase.OutQuad)
            .OnComplete(this, nameof(OnShown));
    }

    public void HidePanel()
    {
        panel.TweenFade(0f, 0.4f, VRCTweenEase.InQuad)
            .OnComplete(this, nameof(OnHidden));
    }

    public void OnShown()
    {
        panel.interactable = true;  // 淡入后可交互
    }

    public void OnHidden()
    {
        panel.interactable = false;
        panel.gameObject.SetActive(false);
    }
}
```

**关键细节**:
- `CanvasGroup.TweenFade` 同时影响所有子元素
- 完全淡出后 `SetActive(false)` 节省渲染
- 用 `interactable` 控制可交互窗口期

---

## 模式 3: 通知横幅滑入滑出

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class NotificationBanner : UdonSharpBehaviour
{
    public RectTransform banner;

    public void ShowNotification(string message)
    {
        // 从屏幕左侧滑入
        banner.anchoredPosition = new Vector2(-500, 0);
        banner.TweenAnchorPos(Vector2.zero, 0.5f, VRCTweenEase.OutBack)
            .OnComplete(this, nameof(AutoHide));
    }

    public void AutoHide()
    {
        // 3 秒后自动滑出
        VRCTween.DelayedCall(this, nameof(HideAfterDelay), 3f);
    }

    public void HideAfterDelay()
    {
        banner.TweenAnchorPos(new Vector2(-500, 0), 0.4f, VRCTweenEase.InQuad);
    }
}
```

**关键细节**:
- `TweenAnchorPos` 移动 UI(不是 `TweenPosition`)
- `OutBack` 滑入有过冲感
- `DelayedCall` 替代 `SendCustomEventDelayedSeconds`(可取消)

---

## 模式 4: 相机平滑跟随(热路径复用)

> **必须用复用模式**,否则每帧创建+销毁 tween 性能爆炸。

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class SmoothCameraFollow : UdonSharpBehaviour
{
    public Transform target;
    public float defaultDuration = 0.3f;
    private VRCTweenHandle _moveHandle;
    private bool _initialized = false;

    void Start()
    {
        // 一次创建,无限循环,初始暂停
        _moveHandle = gameObject.TweenPosition(
            target.position, defaultDuration, VRCTweenEase.OutQuad
        )
        .SetLoops(-1, VRCTweenLoopType.Restart)
        .Pause();
        _initialized = true;
    }

    public void FollowTarget()
    {
        if (!_initialized) return;
        // 重新配置 + 重启
        _moveHandle.ChangeEndValue(target.position, true)
            .SetDuration(defaultDuration)
            .SetEase(VRCTweenEase.OutQuad);
        _moveHandle.Restart();
    }

    public override void OnDestroy()
    {
        if (_initialized && _moveHandle.IsValid) _moveHandle.Kill();
    }
}
```

**关键细节**:
- `ChangeEndValue(target, true)` → 起点=当前位置(避免跳回原点)
- `SetLoops(-1, Restart)` → 完成后保持 alive(以便 Restart)
- 必须在 `Start` 创建,不能延迟(否则 OnDestroy 时 `_moveHandle` 是 `default`)

**性能事实**(官方基准):
- 500 tween × 300 帧
- 复用模式 vs kill-and-recreate:
  - 内存少 **46 倍**
  - 速度快 **10 倍**

---

## 模式 5: Late joiner 同步动画

> 🔴 **VRCTween 不自动同步**。Late joiner 需要用 `Goto()` 跳到正确时间。

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.SDK3.Components;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class SyncedPatrol : UdonSharpBehaviour
{
    public GameObject platform;
    public Vector3[] waypoints;
    [UdonSynced] public float startTime;
    private VRCTweenHandle _handle;
    private float _totalDuration = 8f;

    void Start()
    {
        _handle = platform.TweenPath(
            waypoints,
            _totalDuration,
            VRCTweenPathType.CatmullRom,
            true,   // closePath
            10,
            VRCTweenEase.Linear
        ).SetLoops(-1, VRCTweenLoopType.Restart);
    }

    public override void OnDeserialization()
    {
        // Late joiner 跳到正确时间
        float elapsed = (float)(Networking.GetServerTimeInSeconds() - startTime);
        _handle.Goto(elapsed % _totalDuration, true);  // 模 duration(因为循环)
    }

    public void Interact()
    {
        // 仅 owner 启动同步
        if (!Networking.IsOwner(gameObject))
        {
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        }
        startTime = (float)Networking.GetServerTimeInSeconds();
        RequestSerialization();
    }
}
```

**关键细节**:
- 用 `Networking.GetServerTimeInSeconds()` 算出 elapsed
- 循环 tween 需要 `% duration`
- `OnDeserialization` 在 Late joiner 触发时同步状态

---

## 模式 6: 大量物体交错动画(性能关键)

> 🔴 **不要同帧创建几十个 tween** — 错开,做"波浪"效果。

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class TileWave : UdonSharpBehaviour
{
    public GameObject[] tiles;
    public float delayBetween = 0.05f;
    public float duration = 0.3f;
    private int _nextIndex = 0;

    public void AnimateAll()
    {
        _nextIndex = 0;
        AnimateNext();
    }

    public void AnimateNext()
    {
        if (_nextIndex >= tiles.Length) return;
        tiles[_nextIndex].TweenScale(Vector3.one * 0.8f, duration, VRCTweenEase.OutBack);
        _nextIndex++;
        // 用 DelayedCall 替代 SendCustomEventDelayedSeconds(可取消)
        VRCTween.DelayedCall(this, nameof(AnimateNext), delayBetween);
    }
}
```

**关键细节**:
- 错开避免同帧 GC / EXTERN 峰值
- 视觉上反而更好看(波浪感)
- `DelayedCall` 可取消(可加 `_waveHandle.Kill()`)

---

## 模式 7: 开关按钮(状态机)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class ToggleButton : UdonSharpBehaviour
{
    public GameObject indicator;
    public bool isOn = false;
    private VRCTweenHandle _tween;

    public override void Interact()
    {
        if (_tween.IsValid) _tween.Kill();
        isOn = !isOn;

        if (isOn)
        {
            _tween = indicator.TweenPosition(new Vector3(1, 0, 0), 0.2f, VRCTweenEase.OutBack)
                .OnComplete(this, nameof(OnToggledOn));
        }
        else
        {
            _tween = indicator.TweenPosition(new Vector3(0, 0, 0), 0.2f, VRCTweenEase.OutBack)
                .OnComplete(this, nameof(OnToggledOff));
        }
    }

    public void OnToggledOn() { /* 音效/粒子 */ }
    public void OnToggledOff() { /* 音效/粒子 */ }

    public override void OnDestroy()
    {
        indicator.KillAllTweens();
    }
}
```

---

## 模式 8: 拾取物飞向玩家(简化版)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.SDK3.Components;

public class PickupAttractor : UdonSharpBehaviour
{
    public GameObject pickup;
    public float attractSpeed = 0.3f;
    public VRCPlayerApi targetPlayer;
    private VRCTweenHandle _tween;

    public void AttractToPlayer()
    {
        if (!Utilities.IsValid(targetPlayer)) return;

        if (_tween.IsValid) _tween.Kill();

        _tween = pickup.TweenPosition(targetPlayer.GetPosition(), attractSpeed, VRCTweenEase.InQuad)
            .OnComplete(this, nameof(OnArrived));
    }

    public void OnArrived()
    {
        // 拾取音效
        // 销毁对象
        Destroy(pickup);
    }
}
```

---

## 模式 9: 灯光脉冲(呼吸效果)

```csharp
public class BreathingLight : UdonSharpBehaviour
{
    public Light targetLight;
    public float minIntensity = 1f;
    public float maxIntensity = 3f;
    public float pulseDuration = 2f;

    void Start()
    {
        targetLight.TweenIntensity(maxIntensity, pulseDuration, VRCTweenEase.InOutSine)
            .SetLoops(-1, VRCTweenLoopType.Yoyo);  // 来回脉冲
    }

    public override void OnDestroy()
    {
        targetLight.KillAllTweens();
    }
}
```

---

## 模式 10: 摄像机推拉(电影感)

```csharp
public class CinematicCamera : UdonSharpBehaviour
{
    public Camera mainCamera;
    [System.NonSerialized] public float currentFOV;
    public float defaultFOV = 60f;
    public float closeUpFOV = 35f;

    public void ZoomIn()
    {
        VRCTween.TweenFloat(currentFOV, closeUpFOV, 2f, this, nameof(currentFOV), nameof(ApplyFOV), VRCTweenEase.OutQuad);
    }

    public void ZoomOut()
    {
        VRCTween.TweenFloat(currentFOV, defaultFOV, 1.5f, this, nameof(currentFOV), nameof(ApplyFOV), VRCTweenEase.InOutQuad);
    }

    public void ApplyFOV()
    {
        mainCamera.fieldOfView = currentFOV;
    }
}
```

---

## 模式 11: 链式开关门(用 state 模式)

```csharp
public class FancyDoor : UdonSharpBehaviour
{
    public GameObject door;
    public AudioSource sound;
    public int currentStep = 0;
    public bool cancelled = false;

    public void Interact()
    {
        cancelled = false;
        currentStep = 0;
        Step1_Lift();
    }

    public void Step1_Lift()
    {
        currentStep = 1;
        door.TweenPosition(new Vector3(0, 3, 0), 1f, VRCTweenEase.OutQuad)
            .OnComplete(this, nameof(StepDone));
        sound.Play();
    }

    public void StepDone()
    {
        if (cancelled) return;
        switch (currentStep)
        {
            case 1: Step2_Rotate(); break;
            case 2: Step3_Glow(); break;
            case 3: break; // done
        }
    }

    public void Step2_Rotate()
    {
        currentStep = 2;
        door.TweenRotation(new Vector3(0, 90, 0), 0.8f, VRCTweenEase.InOutQuad)
            .OnComplete(this, nameof(StepDone));
    }

    public void Step3_Glow()
    {
        currentStep = 3;
        // ... 灯光/粒子效果
    }

    public void Cancel()
    {
        cancelled = true;
        door.KillAllTweens();
    }
}
```

---

## 模式 12: 音频淡入淡出(带 BGM 切换)

```csharp
public class BGMCrossfade : UdonSharpBehaviour
{
    public AudioSource sourceA;
    public AudioSource sourceB;
    public AudioClip newClip;
    public float fadeDuration = 2f;

    public void CrossfadeToNewTrack()
    {
        // 1. 准备 B 轨道
        sourceB.clip = newClip;
        sourceB.volume = 0f;
        sourceB.Play();

        // 2. 并行淡入 + 淡出
        sourceA.TweenVolume(0f, fadeDuration, VRCTweenEase.Linear)
            .OnComplete(this, nameof(OnFadeOutDone));
        sourceB.TweenVolume(1f, fadeDuration, VRCTweenEase.Linear);
    }

    public void OnFadeOutDone()
    {
        sourceA.Stop();
    }
}
```

---

## 反模式(不要做)

### ❌ 1. 同帧创建 50+ tween

```csharp
// ❌ 错
public void AnimateAll()
{
    for (int i = 0; i < 100; i++)
    {
        tiles[i].TweenScale(...);  // 100 个 EXTERN 同帧触发!
    }
}

// ✅ 错开(模式 6)
```

### ❌ 2. 不 Kill 旧 tween 就创建新的

```csharp
// ❌ 错(快速点击时多个 tween 跑)
public override void Interact()
{
    button.TweenScale(...);  // 第二次点击时第一个 tween 还在跑
}

// ✅ 检查 + Kill(模式 1)
```

### ❌ 3. 无限循环 tween 不清理

```csharp
// ❌ 错(GameObject 销毁后 tween 还在跑 → null ref)
void Start() { light.TweenIntensity(5f, 1f, VRCTweenEase.Linear).SetLoops(-1, Yoyo); }
// 没有 OnDestroy 清理

// ✅
public override void OnDestroy() { light.KillAllTweens(); }
```

### ❌ 4. 用 TweenPosition 移动 UI

```csharp
// ❌ Canvas 会覆盖
uiImage.TweenPosition(new Vector2(100, 0), 1f, ...);

// ✅ 用 TweenAnchorPos
rectTransform.TweenAnchorPos(new Vector2(100, 0), 1f, ...);
```

### ❌ 5. 试图用 VRCTween 做物理运动

```csharp
// ❌ VRCTween 不参与物理模拟
// ✅ 用 Rigidbody + PhysBone
```

### ❌ 6. ChangeEndValue 改 Color/Vector3 虚拟补间

```csharp
// ❌ 官方不支持
VRCTween.TweenColor(...);
h.ChangeEndValue(Color.red, true);  // 不生效

// ✅ Kill + 重建
if (h.IsValid) h.Kill();
h = VRCTween.TweenColor(current, Color.red, 1f, ...);
```

### ❌ 7. 同步动画不用 Goto

```csharp
// ❌ 错(每个玩家看到的不同步)
public void Interact()
{
    obj.TweenPosition(target, 5f, ...);
    // 没有 [UdonSynced] 时间戳,Late joiner 看到从 0 开始
}

// ✅ 用 Goto + Synced(模式 5)
```

---

## 性能清单(创作前自查)

- [ ] 所有 tween 创建后检查 `IsValid`?(输入验证)
- [ ] 重复触发的 tween 在创建前 Kill 旧 handle?
- [ ] 无限循环 tween 在 OnDestroy 清理?
- [ ] 热路径(每帧)用 `ChangeEndValue` 复用而非 kill-recreate?
- [ ] 大量物体(20+)的同步动画用 `DelayedCall` 错开?
- [ ] UI 移动用 `TweenAnchorPos` 而非 `TweenPosition`?
- [ ] 同步动画用 `[UdonSynced]` + `Goto` 而非裸调?
- [ ] 复杂序列考虑用 state 字段模式(`currentStep`)?

---

## 速查表: 缓动 → 场景

| 场景 | 推荐 Ease |
|---|---|
| 按钮回弹 | `OutBack` / `OutElastic` |
| UI 淡入淡出 | `OutQuad` / `InQuad` |
| 通知滑入 | `OutBack` |
| 物理掉落 | `InQuad` / `InCubic` |
| 弹跳落地 | `OutBounce` |
| 相机平滑 | `InOutSine` / `InOutCubic` |
| 旋转/旋转物体 | `OutCubic` / `InOutQuad` |
| 灯光脉冲 | `InOutSine` + Yoyo |
| 匀速轮播 | `Linear` |
| 弹跳金币 | `OutBounce` |

---

## 官方文档相关章节

| 模式 | 官方文档 |
|---|---|
| 1-3 (UI 模式) | 主页面"Basic Usage" |
| 4 (相机跟随) | 主页面"Tween Reuse" |
| 5 (Late joiner) | `settings` 页面"Seeking With Goto" |
| 6 (大量物体) | 主页面"Staggering Many Tweens" |
| 7-12 | 各种组合(基于 `tween-types` 和 `settings`) |
