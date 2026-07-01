---
title: VRCTween 序列与并行(用 OnComplete 链式回调)
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
  - sequence

aliases:
  - "补间序列"
  - "Tween Sequence"
  - "Chain Tweens"
  - "补间组合"
  - "Sequence and Parallel"

related:
  - ../index.md
  - basics.md
  - tween-types.md
  - control.md
  - patterns.md
  - ../animation-events.md

source: VRChat Creator Docs (https://creators.vrchat.com/worlds/udon/vrctween/#chain-tweens-with-callbacks)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# VRCTween 序列与并行(用 OnComplete 链式回调)

> 来源: https://creators.vrchat.com/worlds/udon/vrctween/#chain-tweens-with-callbacks
> 抓取日期: 2026-06-21
> 状态: ✅ FACT (官方文档本地化)
> 重要事实: **官方没有 `VRCTween.Sequence` 类**

---

## 关键事实

> 🔴 **VRCTween 官方没有提供 Sequence / Append / Join API**。所有"序列"必须**用 `OnComplete` 链式回调**实现。

> 这与 DOTween 原生不同(原生有 `DOTween.Sequence().Append()` 等),VRCTween 出于 Udon 限制**省略**了 Sequence。

> **【待官方文档确认】**: 是否未来版本会加入 `VRCTween.Sequence`?目前(2026-06)无此 API。

---

## 1. 基础模式: OnComplete 链

```csharp
void Start()
{
    cube.TweenPosition(Vector3.up * 5, 1f, VRCTweenEase.OutQuad)
        .OnComplete(this, nameof(OnFirstTweenComplete));
}

public void OnFirstTweenComplete()
{
    cube.TweenRotation(new Vector3(0, 180, 0), 1f, VRCTweenEase.InOutQuad)
        .OnComplete(this, nameof(OnSecondTweenComplete));
}

public void OnSecondTweenComplete()
{
    Debug.Log("Sequence complete!");
}
```

**模式**:
1. 创建 tween A
2. 在 A 上挂 `OnComplete(this, nameof(B))`
3. B 完成后挂 `OnComplete(this, nameof(C))`
4. 每个回调方法**必须 public**

---

## 2. 三步开门序列(完整示例)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class DoorOpenSequence : UdonSharpBehaviour
{
    public GameObject door;
    public AudioSource doorSound;
    public ParticleSystem sparkleEffect;

    public void Interact()
    {
        BeginOpen();
    }

    public void BeginOpen()
    {
        // 步骤 1: 门向上抬
        door.TweenPosition(new Vector3(0, 3, 0), 1f, VRCTweenEase.OutQuad)
            .OnComplete(this, nameof(OnLifted));
    }

    public void OnLifted()
    {
        // 步骤 2: 旋转打开
        door.TweenRotation(new Vector3(0, 90, 0), 0.8f, VRCTweenEase.InOutQuad)
            .OnComplete(this, nameof(OnRotated));
    }

    public void OnRotated()
    {
        // 步骤 3: 播音效 + 粒子
        doorSound.Play();
        sparkleEffect.Play();
        // 结束
    }
}
```

> **优势**: 清晰、可读、易调试(每步都是一个 public 方法)
> **代价**: 大量 public 方法(序列越长越多)

---

## 3. 并行播放(Parallel)

VRCTween **天然支持并行** — 直接**不挂 OnComplete** 创建多个 tween 即可,它们独立运行。

```csharp
public void OpenDoorWithEffects()
{
    // 并行 1: 门抬升
    door.TweenPosition(new Vector3(0, 3, 0), 1f, VRCTweenEase.OutQuad);

    // 并行 2: 灯光渐亮
    doorLight.TweenIntensity(5f, 1f, VRCTweenEase.OutQuad);

    // 并行 3: 音效淡入
    doorSound.Play();
    doorSound.TweenVolume(1f, 1f, VRCTweenEase.InQuad);
}
```

> **关键**: 并行的 tween 都从创建那一帧开始,**并行播放**。

---

## 4. 半自动并行+序列混合

> 想要"两个并行 + 完成后启动下一步"?

```csharp
public void OpenDoorSequence()
{
    // 阶段 1: 门抬升 + 灯渐亮(并行)
    door.TweenPosition(new Vector3(0, 3, 0), 1f, VRCTweenEase.OutQuad)
        .OnComplete(this, nameof(Stage1Done));
    doorLight.TweenIntensity(5f, 1f, VRCTweenEase.OutQuad);
}

public void Stage1Done()
{
    // 阶段 2: 旋转 + 音效(并行)
    door.TweenRotation(new Vector3(0, 90, 0), 0.8f, VRCTweenEase.InOutQuad)
        .OnComplete(this, nameof(Stage2Done));
    doorSound.Play();
}

public void Stage2Done()
{
    // 阶段 3: 粒子效果
    sparkleEffect.Play();
}
```

> **原理**: 在**最快完成**的那个 tween 上挂 OnComplete,触发下一阶段。

---

## 5. 大量回调的可维护模式

> 序列很长时(5+ 步骤),`public` 回调方法会爆炸。**用 state 字段切换**:

```csharp
public class LongSequence : UdonSharpBehaviour
{
    public GameObject obj;
    public int currentStep = 0;
    private VRCTweenHandle _h;

    public void BeginSequence()
    {
        currentStep = 0;
        Step0();
    }

    public void Step0()
    {
        currentStep = 1;
        obj.TweenPosition(Vector3.up, 1f, VRCTweenEase.OutQuad)
            .OnComplete(this, nameof(OnStepComplete));
    }

    public void OnStepComplete()
    {
        switch (currentStep)
        {
            case 1: Step1(); break;
            case 2: Step2(); break;
            case 3: Step3(); break;
        }
    }

    public void Step1()
    {
        currentStep = 2;
        obj.TweenRotation(new Vector3(0, 90, 0), 1f, VRCTweenEase.InOutQuad)
            .OnComplete(this, nameof(OnStepComplete));
    }

    public void Step2()
    {
        currentStep = 3;
        obj.TweenScale(Vector3.one * 1.5f, 0.5f, VRCTweenEase.OutBack)
            .OnComplete(this, nameof(OnStepComplete));
    }

    public void Step3()
    {
        Debug.Log("All steps done!");
    }
}
```

> **优势**: 单一 public 回调方法 `OnStepComplete`,用 `currentStep` 路由。
> **代价**: switch-case 不够优雅,但 Udon 不支持 delegate,这是权衡。

---

## 6. 取消序列

> 序列中途取消? **每个 OnComplete 入口处检查状态**:

```csharp
public bool _cancelled = false;
public int currentStep = 0;

public void BeginSequence()
{
    _cancelled = false;
    currentStep = 0;
    Step0();
}

public void CancelSequence()
{
    _cancelled = true;
    obj.KillAllTweens();  // 杀掉当前正在播放的 tween
}

public void OnStepComplete()
{
    if (_cancelled) return;  // 已被取消,不再继续
    // ... switch logic
}
```

> **关键**: 杀掉当前 tween **不会自动阻止** 已注册的 OnComplete 再次触发(如果 tween 已经在当前帧完成队列中),所以**双重检查** + 显式 flag。

---

## 7. 间隔(AppendInterval 替代)

> DOTween 的 `AppendInterval` 在 VRCTween 中没有。用 `DelayedCall`:

```csharp
public void OpenDoorWithDelay()
{
    door.TweenPosition(new Vector3(0, 3, 0), 1f, VRCTweenEase.OutQuad)
        .OnComplete(this, nameof(AfterDelay));
}

public void AfterDelay()
{
    // 等待 0.5 秒
    VRCTween.DelayedCall(this, nameof(AfterWait), 0.5f);
}

public void AfterWait()
{
    door.TweenRotation(new Vector3(0, 90, 0), 1f, VRCTweenEase.InOutQuad);
}
```

> 嵌套回调,够用但稍长。

---

## 8. 完整实战: 5 段飞行引导

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Components;

public class FlightGuide : UdonSharpBehaviour
{
    public GameObject arrow;
    public Transform[] waypoints;  // 5 个航点
    public GameObject[] waypointMarkers;
    public int currentStep = 0;
    public bool cancelled = false;

    public void StartGuide()
    {
        cancelled = false;
        currentStep = 0;
        FlyToNext();
    }

    public void FlyToNext()
    {
        if (cancelled) return;
        if (currentStep >= waypoints.Length)
        {
            Debug.Log("Guide complete!");
            return;
        }

        // 飞向当前 waypoint
        arrow.TweenPosition(waypoints[currentStep].position, 2f, VRCTweenEase.InOutSine)
            .OnComplete(this, nameof(OnArrived));

        // 当前 marker 闪烁
        if (currentStep < waypointMarkers.Length)
        {
            waypointMarkers[currentStep].TweenScale(Vector3.one * 1.5f, 0.5f, VRCTweenEase.OutBack)
                .OnComplete(this, nameof(ShrinkMarker));
        }
    }

    public void OnArrived()
    {
        currentStep++;
        FlyToNext();
    }

    public void ShrinkMarker()
    {
        if (currentStep < waypointMarkers.Length)
        {
            waypointMarkers[currentStep].TweenScale(Vector3.one, 0.3f, VRCTweenEase.InQuad);
        }
    }

    public void CancelGuide()
    {
        cancelled = true;
        arrow.KillAllTweens();
    }
}
```

> **亮点**: 5 步序列 + 并行 marker 闪烁,用单一 `OnArrived` 回调驱动。

---

## 9. 反模式(不要做)

### ❌ 试图在 OnComplete 中再嵌套创建 tween 又等其 OnComplete

```csharp
// ❌ 反例: 难以追踪 + 大量嵌套
public void Step1()
{
    obj.TweenPosition(target, 1f, VRCTweenEase.OutQuad)
        .OnComplete(this, nameof(Step2));
}

public void Step2()
{
    obj.TweenRotation(rot, 1f, VRCTweenEase.InOutQuad)
        .OnComplete(this, nameof(Step3));
}
// ... Step3, Step4, Step5... 嵌套地狱
```

**用 state 模式(上文)代替**。

### ❌ 试图"等待"多个 tween 都完成

```csharp
// ❌ VRCTween 没"全部完成"回调
public void OnPartADone() { _partADone = true; CheckBoth(); }
public void OnPartBDone() { _partBDone = true; CheckBoth(); }
public void CheckBoth()
{
    if (_partADone && _partBDone) DoNext();
}
```

> 这个**确实能做**(用 flag),但要小心**多次触发**问题(两个 tween 几乎同时完成时,CheckBoth 触发 2 次)。

```csharp
// ✅ 修正: 用一个 tween 作为"协调者"
public void ParallelWork()
{
    // 慢的那个挂 OnComplete
    slowTween.OnComplete(this, nameof(BothDone));
    fastTween.OnComplete(this, nameof(NoOp));  // 哑回调
}
public void BothDone() { /* 真正的下一步 */ }
public void NoOp() { }
```

---

## 10. 官方文档中的 Sequence 等价物

> 🔴 **官方文档目前没有 `VRCTween.Sequence` / `Append` / `Join` API**。
>
> 官方"Chain Tweens with Callbacks"章节**明确推荐**用 OnComplete 链实现序列。

```csharp
// 官方示例 (https://creators.vrchat.com/worlds/udon/vrctween/#chain-tweens-with-callbacks)
void Start()
{
    cube.TweenPosition(Vector3.up * 5, 1f, VRCTweenEase.OutQuad)
        .OnComplete(this, nameof(OnFirstTweenComplete));
}

public void OnFirstTweenComplete()
{
    cube.TweenRotation(new Vector3(0, 180, 0), 1f, VRCTweenEase.InOutQuad)
        .OnComplete(this, nameof(OnSecondTweenComplete));
}

public void OnSecondTweenComplete()
{
    Debug.Log("Sequence complete!");
}
```

> **结论**: OnComplete 链是 VRCTween 序列的**唯一官方方式**。如果觉得啰嗦,用 state 字段压缩。

---

## 11. 已知限制

- ❌ **没有原生 `Sequence` / `Append` / `AppendInterval` / `Join` / `Insert`**
- ❌ **没有"全部完成"事件** — 必须自己用 flag
- ❌ **没有"任意子步骤完成"事件** — 只能挂单一 OnComplete
- ❌ **没有"子 tween 失败"事件** — 失败的 tween 永远不会触发 OnComplete
- ❌ **没有 tween 优先级** — 多个 tween 修改同一属性时**后者覆盖前者**

---

## 官方文档子页面对应

| 本文件章节 | 官方页面 |
|---|---|
| 序列(OnComplete 链) | `https://creators.vrchat.com/worlds/udon/vrctween/#chain-tweens-with-callbacks` |
| 并行(直接创建多个) | `https://creators.vrchat.com/worlds/udon/vrctween/`/ (主页面) |
| DelayedCall | `https://creators.vrchat.com/worlds/udon/vrctween/virtual-tweens#delayedcall` |
