---
title: VRCTween 补间类型全表
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
  - tween-types

aliases:
  - "补间类型"
  - "VRCTween Tween Types"
  - "Built-in Tween Types"

related:
  - ../index.md
  - basics.md
  - control.md
  - patterns.md
  - ../animation-events.md

source: VRChat Creator Docs (https://creators.vrchat.com/worlds/udon/vrctween/tween-types/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---

# VRCTween 补间类型全表

> 来源: https://creators.vrchat.com/worlds/udon/vrctween/tween-types/
> 抓取日期: 2026-06-21
> 状态: ✅ FACT (官方文档本地化)

---

## 概述

VRCTween 内置 **7 大类补间**,覆盖最常用的 Unity 组件和 VRChat 场景需求。所有方法都是**扩展方法**,可调用在 `GameObject` 或具体组件上(部分类型仅组件上可用)。

| 类别 | 数量 | 适用对象 |
|---|---|---|
| Transform | 5 | GameObject / Transform |
| Path | 2 | GameObject / Transform |
| UI | 5 | Image / Text / CanvasGroup / Slider / RectTransform |
| Sprite | 2 | SpriteRenderer |
| Renderer | 2 | Renderer(用 MaterialPropertyBlock) |
| Light | 2 | Light |
| Audio | 2 | AudioSource |

> 加上 **4 个虚拟补间**(`TweenFloat / TweenInt / TweenColor / TweenVector3`)+ `DelayedCall` + `DelayedSetActive`,总计 ~25 个 API。

---

## 1. Transform 补间(最常用)

> 可调用在 `GameObject` 或 `Transform` 上,两者等价。

### TweenPosition / TweenLocalPosition

```csharp
public GameObject door;

public void OpenDoor()
{
    // 世界位置
    door.TweenPosition(new Vector3(0, 3, 0), 1f, VRCTweenEase.OutQuad);
}

public void CloseDoor()
{
    // 本地位置(相对父对象)
    door.TweenLocalPosition(Vector3.zero, 1f, VRCTweenEase.InOutQuad);
}
```

| 特性 | TweenPosition | TweenLocalPosition |
|---|---|---|
| 坐标系 | 世界 | 本地(相对父对象) |
| 适用 | 门/独立物体 | 子物体跟随父级移动 |
| 起点 | 当前位置 | 当前位置 |

### TweenRotation / TweenLocalRotation

> 用 **Euler 角**(`Vector3`)而不是 Quaternion,直接传角度。

```csharp
public GameObject lever;

public void PullLever()
{
    lever.TweenRotation(new Vector3(-45, 0, 0), 0.5f, VRCTweenEase.OutBack);
}

public void ResetLever()
{
    lever.TweenLocalRotation(Vector3.zero, 0.5f, VRCTweenEase.InOutQuad);
}
```

> **Euler 大角度合法**: 旋转补间只要求**有限值**,允许大角度(不像位置/缩放有 ~520,000 限制)。

### TweenScale

> 🔴 **TweenScale 是本地缩放**。Unity 的 `lossyScale`(世界缩放)只读,所以**没有 TweenGlobalScale**。

```csharp
public GameObject pickup;

public void OnPickedUp()
{
    pickup.TweenScale(Vector3.zero, 0.3f, VRCTweenEase.InBack);  // 缩到 0
}

public void OnDropped()
{
    pickup.TweenScale(Vector3.one, 0.3f, VRCTweenEase.OutBack);  // 弹回
}
```

---

## 2. Path 补间(多点路径)

> 沿一系列 `Vector3` waypoint 移动物体。**最少 2 个点**。

### TweenPath / TweenLocalPath

```csharp
public GameObject platform;

public void StartPatrol()
{
    Vector3[] route = new Vector3[]
    {
        new Vector3(0, 0, 0),
        new Vector3(10, 0, 0),
        new Vector3(10, 0, 10),
        new Vector3(0, 0, 10)
    };

    // 线性巡逻 + 无限循环
    platform.TweenPath(
        route,                          // waypoints
        8f,                             // duration(秒)
        VRCTweenPathType.Linear,        // 类型
        true,                           // closePath: 最后一个点自动连回第一个
        10,                             // resolution(CatmullRom 时有效,1-50)
        VRCTweenEase.Linear             // 缓动
    ).SetLoops(-1, VRCTweenLoopType.Restart);
}
```

### 平滑曲线模式

```csharp
public void StartCameraFlythrough()
{
    Vector3[] cameraPath = new Vector3[]
    {
        new Vector3(0, 2, 0),
        new Vector3(5, 4, 3),
        new Vector3(10, 2, 8),
        new Vector3(15, 3, 5)
    };

    // CatmullRom 平滑曲线
    camera.TweenPath(
        cameraPath,
        6f,
        VRCTweenPathType.CatmullRom,   // 平滑插值
        false,                          // 不闭合
        10,                             // resolution
        VRCTweenEase.InOutSine
    ).OnComplete(this, nameof(OnFlythroughDone));
}
```

### Path 参数表

| 参数 | 类型 | 说明 |
|---|---|---|
| `waypoints` | `Vector3[]` | 最少 2 个点; 含 NaN/Inf/极值会被**拒绝** |
| `pathType` | `VRCTweenPathType` | `Linear` / `CatmullRom` |
| `closePath` | `bool` | `true` = 最后一个点自动连回第一个(适合巡逻回路) |
| `resolution` | `int` | CatmullRom 曲线细分(默认 10),**静默 clamp 到 1-50** |
| `ease` | `VRCTweenEase` | 沿路径的速度曲线 |

> **最佳实践**: 巡逻回路用 `closePath=true` + `SetLoops(-1, Restart)` 做无缝循环。

---

## 3. UI 补间

### TweenColor / TweenFade (Graphic)

> `Graphic` 是 `Image` / `Text` / `RawImage` 的基类,这些方法**通用**于所有 UI 元素。

```csharp
public Image myImage;
public Text myText;

void Start()
{
    myImage.TweenColor(Color.red, 1f, VRCTweenEase.OutQuad);
    myText.TweenFade(0f, 1f, VRCTweenEase.OutQuad);  // 淡出
}
```

### TweenFade (CanvasGroup)

> 整个 UI 面板淡入淡出(可同时影响所有子元素)。

```csharp
public CanvasGroup menuPanel;

public void ShowMenu()
{
    menuPanel.gameObject.SetActive(true);
    menuPanel.TweenFade(1f, 0.5f, VRCTweenEase.OutQuad);
}

public void HideMenu()
{
    menuPanel.TweenFade(0f, 0.5f, VRCTweenEase.OutQuad)
        .OnComplete(this, nameof(OnMenuHidden));
}

public void OnMenuHidden()
{
    menuPanel.gameObject.SetActive(false);
}
```

### TweenValue (Slider)

> 生命条/进度条平滑变化。

```csharp
public Slider healthBar;

public void TakeDamage(float damage)
{
    float newHealth = Mathf.Max(0, healthBar.value - damage);
    healthBar.TweenValue(newHealth, 0.3f, VRCTweenEase.OutQuad);
}
```

### TweenAnchorPos

> **移动 UI 元素的正确方式**(在 Canvas 布局中)。

```csharp
public RectTransform notificationPanel;

public void SlideIn()
{
    notificationPanel.anchoredPosition = new Vector2(-500, 0);  // 初始在屏幕外
    notificationPanel.TweenAnchorPos(Vector2.zero, 0.5f, VRCTweenEase.OutQuad);
}

public void SlideOut()
{
    notificationPanel.TweenAnchorPos(new Vector2(500, 0), 0.5f, VRCTweenEase.InQuad);
}
```

> ⚠️ **不要用 `TweenPosition` 移动 UI** — Canvas 内部用 `RectTransform`,改 `position` 会被 Canvas 覆盖。必须用 `TweenAnchorPos` 或 `TweenSizeDelta`。

### TweenSizeDelta

> 调整 UI 元素的宽高(用于展开/折叠面板、tooltip 弹出)。

```csharp
public RectTransform tooltip;

public void ExpandTooltip()
{
    tooltip.TweenSizeDelta(new Vector2(400, 200), 0.3f, VRCTweenEase.OutQuad);
}

public void CollapseTooltip()
{
    tooltip.TweenSizeDelta(Vector2.zero, 0.3f, VRCTweenEase.InQuad);
}
```

---

## 4. Sprite 补间(2D 游戏)

> `SpriteRenderer`(不是 UI Graphic)。

```csharp
public SpriteRenderer mySprite;

void Start()
{
    mySprite.TweenColor(Color.blue, 1f, VRCTweenEase.OutQuad);
    mySprite.TweenFade(0f, 1f, VRCTweenEase.OutQuad);
}
```

---

## 5. Renderer 补间(MaterialPropertyBlock)

> 🔴 **推荐方式**: 用 MaterialPropertyBlock **不创建材质实例**,**支持 GPU Instancing**。

### TweenColor (Renderer)

```csharp
public Renderer myRenderer;

void Start()
{
    myRenderer.TweenColor(Color.red, 1f, VRCTweenEase.OutQuad);
    // 默认动 _Color
}
```

自定义 shader 属性:

```csharp
public void GlowUp()
{
    myRenderer.TweenColor("_EmissionColor", Color.yellow, 1f, VRCTweenEase.OutQuad);
}
```

### TweenFloat (Renderer)

```csharp
public Renderer myRenderer;

void Start()
{
    // 溶解效果
    myRenderer.TweenFloat("_DissolveAmount", 1f, 2f, VRCTweenEase.InQuad);

    // 金属度
    myRenderer.TweenFloat("_Metallic", 0.8f, 1f, VRCTweenEase.OutQuad);
}
```

> **常见属性名**: `_Color`(主色), `_EmissionColor`(自发光), `_Metallic`, `_Glossiness`, `_Cutoff`。
> **找不到属性?** 检查 shader 的 Property 名字是否匹配(大小写敏感)。

---

## 6. Light 补间

```csharp
public Light myLight;

public void FadeOutLight()
{
    myLight.TweenIntensity(0f, 2f, VRCTweenEase.OutQuad);
}

public void FlashLight()
{
    myLight.TweenIntensity(5f, 0.1f, VRCTweenEase.OutQuad);
}

public void Sunset()
{
    myLight.TweenColor(new Color(1f, 0.5f, 0.2f), 3f, VRCTweenEase.InOutSine);
}
```

---

## 7. Audio 补间

```csharp
public AudioSource musicSource;

public void FadeOutMusic()
{
    musicSource.TweenVolume(0f, 2f, VRCTweenEase.OutQuad);
}

public void FadeInMusic()
{
    musicSource.Play();
    musicSource.TweenVolume(1f, 2f, VRCTweenEase.InQuad);
}

public void AccelerateEngine()
{
    engineSource.TweenPitch(2f, 1f, VRCTweenEase.OutQuad);
}
```

> **音高范围**: 典型 -3 到 3,任何有限值都接受。

---

## 8. 虚拟补间(Virtual Tweens)速查

> 详见 `basics.md` 的"虚拟补间"章节,这里列签名:

| 方法 | 签名 |
|---|---|
| `TweenFloat` | `(start, end, dur, this, varName, onUpdateName, ease)` |
| `TweenInt` | `(start, end, dur, this, varName, onUpdateName, ease)` |
| `TweenColor` | `(start, end, dur, this, varName, onUpdateName, ease)` |
| `TweenVector3` | `(start, end, dur, this, varName, onUpdateName, ease)` |
| `DelayedCall` | `(this, callbackName, delay)` |
| `DelayedSetActive` | `(gameObject, active, delay)` |

**使用条件**: 变量必须 `public` + `[System.NonSerialized]`,回调方法必须 `public`。

---

## 选择指南: 该用哪个?

| 需求 | 推荐 API |
|---|---|
| 移动物体(门/平台) | `TweenPosition` / `TweenLocalPosition` |
| 旋转物体(把手/摇杆) | `TweenRotation`(Euler 角度) |
| 改变大小(拾取物/UI 反馈) | `TweenScale` |
| 沿路径移动(巡逻/相机) | `TweenPath`(Linear / CatmullRom) |
| UI 颜色/透明度 | `TweenColor` / `TweenFade` |
| UI 移动/缩放 | `TweenAnchorPos` / `TweenSizeDelta` |
| 整组 UI 淡入淡出 | `CanvasGroup.TweenFade` |
| 进度条 | `Slider.TweenValue` |
| 物体材质变色 | `Renderer.TweenColor`(避免材质实例化) |
| 灯光强度/颜色 | `Light.TweenIntensity` / `TweenColor` |
| 音乐/音效淡入淡出 | `AudioSource.TweenVolume` |
| 分数计数/相机 FOV/Animator 参数 | 虚拟补间 `TweenFloat` / `TweenInt` |
| 延时回调(可取消) | `VRCTween.DelayedCall` |
| 延时启用/禁用对象 | `VRCTween.DelayedSetActive` |

---

## 不支持/【待官方文档确认】

- ⚠️ **`TweenQuaternion`** — **未在官方文档出现**。需要 Quaternion 插值请用虚拟补间(`TweenVector3` 作用于整向量)或自己包装 Slerp。**【待官方文档确认是否有意省略】**
- ⚠️ **TrailRenderer / LineRenderer** — **未列出**,如有需求请用虚拟补间控制 `position`/`widthMultiplier`。
- ⚠️ **ParticleSystem 数值参数**(`startSize` / `startSpeed` 等) — 未列出,可用 `TweenFloat` 间接控制(如通过 Animator 参数或 MaterialPropertyBlock)。
- ⚠️ **Camera 字段**(FOV / orthographicSize) — **未列为内置**,但虚拟补间 `TweenFloat` 可控制 FOV(官方示例)。

---

## 官方文档子页面对应

| 本文件章节 | 官方页面 |
|---|---|
| Transform / Path / UI / Renderer / Light / Audio / Sprite | `https://creators.vrchat.com/worlds/udon/vrctween/tween-types`/ |
