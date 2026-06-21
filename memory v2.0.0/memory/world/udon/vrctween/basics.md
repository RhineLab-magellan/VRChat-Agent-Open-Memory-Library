---
title: VRCTween 基础 API
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
  - basics
  - api

aliases:
  - "VRCTween 基础"
  - "VRCTween Basic Usage"
  - "补间基础"
  - "TweenHandle"

related:
  - ../index.md
  - tween-types.md
  - control.md
  - sequence.md
  - ../animation-events.md

source: VRChat Creator Docs (https://creators.vrchat.com/worlds/udon/vrctween/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# VRCTween 基础 API

> 来源: https://creators.vrchat.com/worlds/udon/vrctween/
> 抓取日期: 2026-06-21
> 状态: ✅ FACT (官方文档本地化)

---

## 概述

VRCTween 提供了**两类调用入口**:

1. **扩展方法** — 在目标类型(Transform / GameObject / UI 组件等)上调用
2. **静态方法** — `VRCTween.TweenXxx(...)` 形式(主要用于虚拟补间)

所有方法都返回 `VRCTweenHandle`,用于**控制 / 配置** 这个补间。

```csharp
// 扩展方法风格(最常用)
VRCTweenHandle h1 = cube.TweenPosition(target, 2f, VRCTweenEase.OutQuad);

// 静态方法风格(虚拟补间)
VRCTweenHandle h2 = VRCTween.TweenFloat(0f, 100f, 2f, this, nameof(myValue), nameof(OnUpdate), VRCTweenEase.Linear);
```

---

## 基础流程: 创建 → 配置 → 控制

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class TweenBasics : UdonSharpBehaviour
{
    public GameObject cube;
    private VRCTweenHandle _tweenHandle;

    public override void Start()
    {
        // 1. 创建补间 — 移动到 (0, 5, 0),持续 2 秒,OutQuad 缓动
        _tweenHandle = cube.TweenPosition(
            new Vector3(0, 5, 0),  // 目标值(终点)
            2f,                     // duration
            VRCTweenEase.OutQuad    // 缓动函数
        );

        // 2. 链式配置
        _tweenHandle
            .SetDelay(0.5f)                       // 延迟 0.5s 才开始
            .SetLoops(2, VRCTweenLoopType.Yoyo)   // 来回 2 次(共 4 个单向)
            .OnComplete(this, nameof(OnDone));    // 完成回调
    }

    public void OnDone()
    {
        Debug.Log("Tween finished!");
    }

    public override void OnDestroy()
    {
        // 3. 清理(无限循环或长 tween 必须)
        cube.KillAllTweens();
    }
}
```

---

## 关键 API 索引

### 创建(扩展方法) — 详见 `tween-types.md`

| 调用形式 | 用途 |
|---|---|
| `gameObject.TweenPosition(target, dur, ease)` | 世界位置 |
| `gameObject.TweenLocalPosition(target, dur, ease)` | 本地位置 |
| `gameObject.TweenRotation(target, dur, ease)` | 世界旋转(Euler) |
| `gameObject.TweenLocalRotation(target, dur, ease)` | 本地旋转(Euler) |
| `gameObject.TweenScale(target, dur, ease)` | 缩放(本地) |
| `gameObject.TweenPath(points, dur, type, close, res, ease)` | 多点路径 |
| `image.TweenColor(color, dur, ease)` | UI / Sprite / Renderer 颜色 |
| `image.TweenFade(alpha, dur, ease)` | UI / Sprite 透明度 |
| `canvasGroup.TweenFade(alpha, dur, ease)` | CanvasGroup 透明度 |
| `slider.TweenValue(val, dur, ease)` | Slider 值 |
| `rectTransform.TweenAnchorPos(pos, dur, ease)` | UI 锚点位置 |
| `rectTransform.TweenSizeDelta(size, dur, ease)` | UI 尺寸 |
| `renderer.TweenFloat(propName, val, dur, ease)` | Shader float 属性 |
| `light.TweenIntensity(val, dur, ease)` | Light 强度 |
| `light.TweenColor(color, dur, ease)` | Light 颜色 |
| `audioSource.TweenVolume(vol, dur, ease)` | Audio 音量 |
| `audioSource.TweenPitch(pitch, dur, ease)` | Audio 音高 |

### 创建(静态方法) — 虚拟补间

```csharp
VRCTween.TweenFloat(start, end, dur, this, nameof(variable), nameof(OnUpdate), ease);
VRCTween.TweenInt(start, end, dur, this, nameof(variable), nameof(OnUpdate), ease);
VRCTween.TweenColor(start, end, dur, this, nameof(variable), nameof(OnUpdate), ease);
VRCTween.TweenVector3(start, end, dur, this, nameof(variable), nameof(OnUpdate), ease);
VRCTween.DelayedCall(this, nameof(OnTimer), delay);
VRCTween.DelayedSetActive(gameObject, active, delay);
```

> **虚拟补间要求**: 变量必须 `public`, 加 `[System.NonSerialized]` 防止 Unity 序列化。

### 关键参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `target` / `end` | 各种类型 | 终点值(起点 = 对象的当前值) |
| `duration` | `float` | 秒数; 0 是允许的(用于复用模式); < 0/NaN/Inf 被拒绝 |
| `ease` | `VRCTweenEase` 或 `AnimationCurve` | 缓动函数(默认 OutQuad 类) |

### 链式配置方法(返回 handle)

| 方法 | 用途 | 调用时机 |
|---|---|---|
| `.From()` | 翻转起点终点(从 target 动到当前值) | **创建后立即** |
| `.SetDelay(seconds)` | 延迟开始 | **创建后立即** |
| `.SetLoops(n, type)` | 循环次数 + 类型(Restart/Yoyo/Incremental) | **创建后立即** |
| `.SetSpeedBased()` | duration 改为"单位/秒" | **创建后立即** |
| `.SetUpdate(type)` | Update 阶段(Update/LateUpdate/FixedUpdate/PostLateUpdate) | **创建后立即** |
| `.OnComplete(this, name)` | 完成回调 | **创建后立即** |
| `.OnRewind(this, name)` | 倒放回到 0 回调 | **创建后立即** |
| `.SetEase(ease)` | 修改缓动 | **任意时刻** |
| `.SetDuration(seconds)` | 修改 duration | **任意时刻** |
| `.ChangeEndValue(val, snap)` | 修改终点值 | **任意时刻**(Color/Vector3 虚拟/Renderer/Light/Path 不可用) |

> 🔴 **关键**:`From / SetLoops / SetDelay / SetSpeedBased / SetUpdate / OnComplete / OnRewind` 必须在 tween **开始播放前**(同帧内)调用,否则可能不生效。
> `SetEase / SetDuration / ChangeEndValue` 可在 tween 运行中调用。

---

## 虚拟补间(Virtual Tweens)

> 用于"内置补间类型都不适用"的场景(分数计数、相机 FOV、Animator 参数等)

### TweenFloat

```csharp
[System.NonSerialized] public float fovValue;

VRCTweenHandle tweenHandle = VRCTween.TweenFloat(
    60f, 90f, 2f, this, nameof(fovValue), nameof(OnFovUpdate), VRCTweenEase.OutQuad
);

public void OnFovUpdate()
{
    myCamera.fieldOfView = fovValue;  // 每帧把插值结果应用到 FOV
}
```

### TweenInt(整数计数)

```csharp
[System.NonSerialized] public int scoreValue;

VRCTween.TweenInt(0, 100, 5f, this, nameof(scoreValue), nameof(OnCountUpdate), VRCTweenEase.Linear);

public void OnCountUpdate()
{
    scoreText.text = scoreValue.ToString();
}
```

### TweenColor

```csharp
[System.NonSerialized] public Color lightColor;

VRCTween.TweenColor(Color.red, Color.blue, 2f, this, nameof(lightColor), nameof(OnColorUpdate), VRCTweenEase.Linear);

public void OnColorUpdate()
{
    myLight.color = lightColor;
}
```

### TweenVector3(整向量插值,不是逐轴)

```csharp
[System.NonSerialized] public Vector3 targetPosition;

VRCTween.TweenVector3(Vector3.zero, new Vector3(5, 10, 0), 2f, this, nameof(targetPosition), nameof(OnPositionUpdate), VRCTweenEase.OutQuad);

public void OnPositionUpdate()
{
    myParticleSystem.transform.position = targetPosition;
}
```

> **注意**:TweenVector3 的缓动**作用于整向量**(作为 4 元数差值处理),**不是逐轴**插值。如需逐轴请用 `TweenPosition`。

### DelayedCall(可取消的延时回调)

```csharp
VRCTweenHandle timerHandle = VRCTween.DelayedCall(this, nameof(OnTimerFinished), 5.0f);

// 取消
public void CancelTimer() { timerHandle.Kill(); }

public void OnTimerFinished() { Debug.Log("5 seconds elapsed!"); }
```

> 比 `SendCustomEventDelayedSeconds` 优势:**可取消**。

### DelayedSetActive(延时启停)

```csharp
// 3 秒后禁用
VRCTweenHandle handle = VRCTween.DelayedSetActive(myObject, false, 3f);

// 等价于 DelayedCall + 在回调里 SetActive(false),但更简洁
// 目标对象在 delay 期间被销毁则静默跳过
```

---

## 回调方法命名规范

> **关键约束**: `OnComplete` / `OnRewind` 指向的方法必须 `public`, 且使用 `nameof()` 传名字符串。

```csharp
// ✅ 正确 — public + nameof
public void OnDoorOpened() { /* ... */ }
.OnComplete(this, nameof(OnDoorOpened));

// ❌ 错误 — private 方法
private void OnDoorOpened() { /* ... */ }
.OnComplete(this, nameof(OnDoorOpened));  // 静默失败,不报错!

// ❌ 错误 — 硬编码字符串(拼写错误会静默失败)
.OnComplete(this, "OnDoorOpned");
```

> **建议**: 严格用 `nameof()`,让编译器帮你检查名字拼写。

---

## 缓动(Ease)速查

完整 31 种预设 + 自定义 `AnimationCurve`:

| 类别 | 预设 |
|---|---|
| **基础** | `Linear` |
| **Sine** | `InSine` / `OutSine` / `InOutSine`(自然感) |
| **Quad** | `InQuad` / `OutQuad`(UI 首选) / `InOutQuad` |
| **Cubic** | `InCubic` / `OutCubic` / `InOutCubic` |
| **Quart / Quint** | 4 种 × 3(In/Out/InOut) |
| **Expo** | 爆炸性加减速,3 种 |
| **Circ** | 圆滑加减速,3 种 |
| **Elastic** | 弹性(回弹),3 种 |
| **Back** | 起始/结束微微过冲,3 种 |
| **Bounce** | 弹跳(落地),3 种 |

**实用选择**:
- UI 弹出 → `OutBack`(过冲感) 或 `OutQuad`
- 平滑相机 → `InOutSine` / `InOutCubic`
- 物理掉落 → `InQuad`
- 弹跳金币 → `OutBounce`
- 持续匀速(轮播) → `Linear`

**自定义 AnimationCurve**:
```csharp
public AnimationCurve customEase;  // Inspector 编辑

void Start()
{
    gameObject.TweenPosition(Vector3.up, 2f, VRCTweenEase.Linear)
        .SetEase(customEase);  // 覆盖预设
}
```

---

## 完整示例: 按钮按下回弹

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
        // 先 Kill 旧 tween(防止快速点击)
        if (_tween.IsValid) _tween.Kill();

        // 弹大 → 弹回
        _tween = button.TweenScale(Vector3.one * 1.3f, 0.1f, VRCTweenEase.OutQuad)
            .OnComplete(this, nameof(OnPopDone));
    }

    public void OnPopDone()
    {
        _tween = button.TweenScale(Vector3.one, 0.2f, VRCTweenEase.OutElastic);
    }

    public override void OnDestroy()
    {
        button.KillAllTweens();
    }
}
```

---

## 输入验证陷阱

```csharp
// ❌ 反例: 不检查 handle 是否有效
cube.TweenPosition(new Vector3(0, float.NaN, 0), 2f, VRCTweenEase.OutQuad)
    .OnComplete(this, nameof(OnDone));  // tween 根本没创建,OnDone 永远不会触发!

// ✅ 正例
VRCTweenHandle h = cube.TweenPosition(new Vector3(0, float.NaN, 0), 2f, VRCTweenEase.OutQuad);
if (h.IsValid)
{
    h.OnComplete(this, nameof(OnDone));
}
```

---

## 官方文档子页面对应

| 本文件章节 | 官方页面 |
|---|---|
| 创建补间 | `https://creators.vrchat.com/worlds/udon/vrctween/#create-a-tween` |
| 接收回调 | `https://creators.vrchat.com/worlds/udon/vrctween/#receive-callbacks` |
| 虚拟补间 | `https://creators.vrchat.com/worlds/udon/vrctween/virtual-tweens`/ |
| 缓动类型 | `https://creators.vrchat.com/worlds/udon/vrctween/settings#ease-types` |
