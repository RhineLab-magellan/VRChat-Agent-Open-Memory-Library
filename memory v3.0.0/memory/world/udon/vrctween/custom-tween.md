---
title: VRCTween 自定义补间(虚拟补间 + AnimationCurve)
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
  - virtual-tween
  - animationcurve

aliases:
  - "自定义补间"
  - "Custom Tween"
  - "虚拟补间"
  - "Virtual Tween"
  - "Custom Easing"
  - "AnimationCurve"

related:
  - ../index.md
  - basics.md
  - tween-types.md
  - control.md
  - patterns.md
  - ../animation-events.md

source: VRChat Creator Docs (https://creators.vrchat.com/worlds/udon/vrctween/virtual-tweens/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# VRCTween 自定义补间(虚拟补间 + AnimationCurve)

> 来源: https://creators.vrchat.com/worlds/udon/vrctween/virtual-tweens/
> 抓取日期: 2026-06-21
> 状态: ✅ FACT (官方文档本地化)

---

## 关键事实

> 🔴 **VRCTween 没有"自定义 VRCTweenBase 子类"机制**(不像 Unity 的 `Tween<T>` 抽象类)。
>
> 官方"自定义"补间实际有两种:
> 1. **虚拟补间(Virtual Tweens)** — 写入任意 `float / int / Color / Vector3` 变量,每帧回调应用
> 2. **自定义 AnimationCurve** — 在 `SetEase(curve)` 中覆盖预设缓动

---

## 1. 虚拟补间 4 大方法

> 用于"内置补间类型不适用"的场景:相机 FOV、Animator 参数、分数计数、Shader 字段等。

| 方法 | 目标类型 | 典型用途 |
|---|---|---|
| `VRCTween.TweenFloat` | `float` | FOV、音量、Shader 强度、Animator Float 参数 |
| `VRCTween.TweenInt` | `int` | 分数计数、玩家血量整数 |
| `VRCTween.TweenColor` | `Color` | 自定义 LUT 颜色、滤镜色 |
| `VRCTween.TweenVector3` | `Vector3` | 自定义坐标、目标点 |

### 通用签名

```csharp
VRCTween.TweenXxx(
    startValue,        // 起点
    endValue,          // 终点
    duration,          // 秒
    this,              // 接收回调的 UdonBehaviour
    nameof(variable),  // 接收插值的 public 变量
    nameof(onUpdate),  // 每帧调用的 public 方法
    ease               // 缓动
);
```

### 必备条件

1. **变量**必须 `public` + `[System.NonSerialized]`
2. **回调方法**必须 `public`
3. 用 `nameof()` 传变量名和方法名(避免拼写错误)

```csharp
[System.NonSerialized] public float fovValue;  // public + NonSerialized

VRCTweenHandle tweenHandle = VRCTween.TweenFloat(
    60f, 90f, 2f, this, nameof(fovValue), nameof(OnFovUpdate), VRCTweenEase.OutQuad
);

public void OnFovUpdate()
{
    myCamera.fieldOfView = fovValue;
}
```

### 多个并行虚拟补间

> 用**不同的变量名**可以同时跑多个 TweenFloat。

```csharp
[System.NonSerialized] public float fovValue;
[System.NonSerialized] public float bloomValue;

void Start()
{
    VRCTween.TweenFloat(60f, 90f, 2f, this, nameof(fovValue), nameof(UpdateFov), VRCTweenEase.OutQuad);
    VRCTween.TweenFloat(0f, 1f, 2f, this, nameof(bloomValue), nameof(UpdateBloom), VRCTweenEase.OutQuad);
}

public void UpdateFov() { myCamera.fieldOfView = fovValue; }
public void UpdateBloom() { bloomMaterial.SetFloat("_Bloom", bloomValue); }
```

---

## 2. TweenVector3 vs TweenPosition 区别

> ⚠️ **关键陷阱**:`TweenVector3` 的缓动作用于**整向量**(作为整体插值),**不是逐轴**。

| 方法 | 缓动应用方式 |
|---|---|
| `TweenPosition(target, dur, ease)` | X/Y/Z **共享**一个 ease 曲线 |
| `TweenVector3(start, end, dur, ease)` | 整向量作为整体(类似四元数)插值 |

> **如果想要"逐轴分别缓动"** — 用三次 `TweenFloat` 或在 Update 里自己算。

---

## 3. DelayedCall — 可取消的延时

```csharp
VRCTweenHandle timerHandle = VRCTween.DelayedCall(this, nameof(OnTimerFinished), 5.0f);

public void CancelTimer() { timerHandle.Kill(); }

public void OnTimerFinished()
{
    Debug.Log("5 seconds elapsed!");
}
```

> **vs `SendCustomEventDelayedSeconds`**:
> - 优势:**可取消**(`Kill()`)
> - 优势:不依赖 Update 帧数,按真实时间
> - 劣势:必须持有 `VRCTweenHandle`

---

## 4. DelayedSetActive — 延时启用/禁用

```csharp
// 3 秒后禁用
VRCTweenHandle handle = VRCTween.DelayedSetActive(myObject, false, 3f);
```

> 等价于 `DelayedCall` + 回调里 `SetActive(false)`,但更简洁。
> **目标对象在 delay 期间被销毁则静默跳过**(不抛异常)。

---

## 5. 自定义 AnimationCurve 缓动

> `SetEase(AnimationCurve)` 在创建后任何时刻调用,可覆盖预设。

### Inspector 编辑

```csharp
public AnimationCurve customEase;  // Inspector 拖入
```

### 在 Inspector 中:
- X 轴(0 到 1) = tween 进度
- Y 轴(0 到 1) = 插值因子

### 代码使用

```csharp
public AnimationCurve bounceEase;

void Start()
{
    gameObject.TweenPosition(new Vector3(0, 5, 0), 2f, VRCTweenEase.Linear)
        .SetEase(bounceEase);  // 用自定义曲线
}
```

### 实用自定义曲线

**颠簸落地**(线性下落 + 末端反弹):
```
曲线形状: 斜线 → 在 0.95 拉到 1.1 → 回到 1
X: 0 ─── 0.7 ── 0.85 ── 0.95 ── 1
Y: 0 ─── 0.7 ── 0.95 ── 1.1 ── 1
```

**蓄力释放**(0~0.3 缓 → 0.3~0.7 急 → 0.7~1 缓):
```
X: 0 ── 0.3 ──── 0.7 ── 1
Y: 0 ── 0.05 ─── 0.95 ── 1
```

**心跳脉冲**(0 → 1 → 0 → 1 → 1):
```
X: 0 ── 0.1 ── 0.2 ── 0.3 ── 1
Y: 0 ── 1 ── 0 ── 1 ── 1
```

---

## 6. 复合补间: 缓动 + 虚拟补间

> 想要"自定义缓动 + 写入任意变量"?
>
> 用虚拟补间 + 自定义 AnimationCurve:

```csharp
[System.NonSerialized] public float pulseValue;
public AnimationCurve heartbeatCurve;

public void Heartbeat()
{
    VRCTween.TweenFloat(0f, 1f, 2f, this, nameof(pulseValue), nameof(ApplyHeartbeat), VRCTweenEase.Linear)
        .SetEase(heartbeatCurve);
}

public void ApplyHeartbeat()
{
    glowMaterial.SetFloat("_Emission", pulseValue);
}
```

> **关键**: 第一参数 `ease=VRCTweenEase.Linear`(作为占位),然后 `.SetEase(curve)` 覆盖。

---

## 7. ChangeEndValue 的适用范围

> `ChangeEndValue` 在运行时改终点,适用于"热路径复用"。

| 支持 | 不支持 |
|---|---|
| Transform (Position/Rotation/Scale) | 虚拟 TweenColor |
| UI (Color/Fade/Value/Anchor/Size) | 虚拟 TweenVector3 |
| Sprite (Color/Fade) | Renderer 补间(MaterialPropertyBlock) |
| Audio (Volume/Pitch) | Light 补间 |
| 虚拟 TweenFloat / TweenInt | Path 补间 |

---

## 8. 实战案例

### 案例 1: 相机 FOV 渐变(场景电影感)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class CinematicFOV : UdonSharpBehaviour
{
    public Camera targetCamera;
    [System.NonSerialized] public float currentFOV;
    public AnimationCurve dollyEase;

    public void ZoomIn()
    {
        VRCTween.TweenFloat(60f, 30f, 3f, this, nameof(currentFOV), nameof(ApplyFOV), VRCTweenEase.Linear)
            .SetEase(dollyEase);
    }

    public void ApplyFOV()
    {
        targetCamera.fieldOfView = currentFOV;
    }

    public void ResetFOV()
    {
        VRCTween.TweenFloat(currentFOV, 60f, 1f, this, nameof(currentFOV), nameof(ApplyFOV), VRCTweenEase.OutQuad);
    }
}
```

### 案例 2: 分数滚动

```csharp
public class ScoreCounter : UdonSharpBehaviour
{
    public Text scoreText;
    [System.NonSerialized] public int displayedScore;
    private int _targetScore;

    public void SetScore(int target)
    {
        _targetScore = target;
        VRCTween.TweenInt(displayedScore, target, 2f, this, nameof(displayedScore), nameof(UpdateText), VRCTweenEase.OutCubic);
    }

    public void UpdateText()
    {
        scoreText.text = displayedScore.ToString();
    }
}
```

### 案例 3: 自定义 LUT 颜色(后期处理)

```csharp
public class ColorFilter : UdonSharpBehaviour
{
    public Material postProcessMaterial;
    [System.NonSerialized] public Color currentTint;

    public void SetTint(Color target)
    {
        VRCTween.TweenColor(Color.white, target, 1.5f, this, nameof(currentTint), nameof(ApplyTint), VRCTweenEase.InOutSine);
    }

    public void ApplyTint()
    {
        postProcessMaterial.SetColor("_Tint", currentTint);
    }
}
```

### 案例 4: 多个虚拟补间 + AnimationCurve

```csharp
public class UIPulseGlow : UdonSharpBehaviour
{
    public Image glowImage;
    [System.NonSerialized] public float alphaValue;
    [System.NonSerialized] public float scaleValue;
    public AnimationCurve pulseCurve;

    public void StartPulse()
    {
        VRCTween.TweenFloat(0f, 1f, 1.5f, this, nameof(alphaValue), nameof(ApplyAlpha), VRCTweenEase.Linear)
            .SetEase(pulseCurve)
            .SetLoops(-1, VRCTweenLoopType.Yoyo);
        VRCTween.TweenFloat(1f, 1.3f, 1.5f, this, nameof(scaleValue), nameof(ApplyScale), VRCTweenEase.Linear)
            .SetEase(pulseCurve)
            .SetLoops(-1, VRCTweenLoopType.Yoyo);
    }

    public void ApplyAlpha()
    {
        Color c = glowImage.color;
        c.a = alphaValue;
        glowImage.color = c;
    }

    public void ApplyScale()
    {
        glowImage.transform.localScale = Vector3.one * scaleValue;
    }
}
```

---

## 9. 限制与陷阱

### ChangeEndValue 不支持的虚拟补间

> **不要在 Color/Vector3 虚拟补间上用 `ChangeEndValue`**,官方明确说"not supported"。

```csharp
// ❌ 不可用
[System.NonSerialized] public Color currentTint;
VRCTweenHandle h = VRCTween.TweenColor(...);
h.ChangeEndValue(Color.red, true);  // 不支持!

// ✅ 改用: Kill + 重建
if (h.IsValid) h.Kill();
h = VRCTween.TweenColor(currentTint, Color.red, 1f, this, nameof(currentTint), nameof(ApplyTint), VRCTweenEase.OutQuad);
```

### 虚拟补间变量被序列化

> 如果**忘记加 `[System.NonSerialized]`**,场景保存时插值的中间值会被序列化,下次加载可能"卡"在中间值。

### 回调方法名拼写错误

> 用 `nameof()` 而不是字符串字面量,让编译器验证。

### Update 频率

> 虚拟补间的 `OnUpdate` 在 `Update` / `LateUpdate` / `FixedUpdate` 中触发,取决于创建时的 `SetUpdate`。**默认 Update**。

---

## 10. 常见问题

### Q: 能用虚拟补间动 Quaternion 吗?

> **官方文档没有 `TweenQuaternion`**。需要 Quaternion 插值,自己写:
>
> ```csharp
> [System.NonSerialized] public Quaternion currentRot;
> public Vector3 eulerStart, eulerEnd;
> public float t;  // 虚拟补间驱动的进度因子
>
> VRCTween.TweenFloat(0f, 1f, 1f, this, nameof(t), nameof(UpdateRot), VRCTweenEase.InOutQuad);
>
> public void UpdateRot()
> {
>     currentRot = Quaternion.Slerp(Quaternion.Euler(eulerStart), Quaternion.Euler(eulerEnd), t);
>     transform.rotation = currentRot;
> }
> ```

### Q: 虚拟补间支持 OnComplete 吗?

> **支持**。所有 VRCTweenHandle 方法(`.OnComplete` / `.SetLoops` / `.SetDelay` 等)都通用。

```csharp
VRCTween.TweenFloat(0f, 100f, 2f, this, nameof(value), nameof(OnUpdate), VRCTweenEase.OutQuad)
    .OnComplete(this, nameof(OnFinished))
    .SetLoops(3, VRCTweenLoopType.Yoyo);
```

### Q: 多个虚拟补间动同一个变量?

> 会**互相覆盖**。用一个变量只跑一个虚拟补间。

```csharp
// ❌ 反例
[System.NonSerialized] public float x;
VRCTween.TweenFloat(0f, 1f, 1f, this, nameof(x), ...);
VRCTween.TweenFloat(0f, 5f, 2f, this, nameof(x), ...);  // 后启动的覆盖前一个!

// ✅ 用不同变量
[System.NonSerialized] public float x1;
[System.NonSerialized] public float x2;
VRCTween.TweenFloat(0f, 1f, 1f, this, nameof(x1), ...);
VRCTween.TweenFloat(0f, 5f, 2f, this, nameof(x2), ...);
```

---

## 官方文档子页面对应

| 本文件章节 | 官方页面 |
|---|---|
| 虚拟补间全部 | `https://creators.vrchat.com/worlds/udon/vrctween/virtual-tweens`/ |
| SetEase(curve) | `https://creators.vrchat.com/worlds/udon/vrctween/settings#setease` |
| ChangeEndValue 支持范围 | `https://creators.vrchat.com/worlds/udon/vrctween/settings#changeendvalue` |
