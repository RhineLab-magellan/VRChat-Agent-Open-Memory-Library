---
title: UI Events - Unity UI 事件白名单
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - animator
  - audio
  - event
  - udonsharp

aliases:
  - "事件"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# UI Events - Unity UI 事件白名单

> 来源:https://creators.vrchat.com/worlds/udon/ui-events/
> 本地化日期:2026-06-15
> 状态:FACT(VRChat 官方白名单)
> 关联:`memory/api/udonsharp-runtime.md` - UdonSharp 运行时类型暴露

---

## 一、核心概念

> **FACT**:Unity UI 事件可**直接调用方法**,**不需要编写 UdonBehaviour** 用于简单交互。

VRChat 对 Unity UI 事件可调用的目标做了**白名单限制**——只有特定组件的**特定方法/属性**可被 UI 事件触发。

```text
UI 元素(Button/Slider/Toggle/InputField)
   ↓ UnityEvent
目标组件上的方法或属性
   ↓
白名单内 → ✅ 可调用
白名单外 → ❌ 静默忽略或编译错误
```

### 核心价值

- **零代码**:不需要 UdonBehaviour,直接连 UI 事件即可
- **类型安全**:VRChat 在编译时校验白名单
- **性能最优**:无 Udon VM 调度开销

---

## 二、完整白名单

### 2.1 Animator

| 成员 |
|------|
| `Play` |
| `PlayInFixedTime` |
| `Rebind` |
| `SetBool` |
| `SetFloat` |
| `SetInteger` |
| `SetTrigger` |
| `ResetTrigger` |
| `speed` |

### 2.2 AudioSource

| 成员 |
|------|
| `Pause` / `Play` / `PlayDelayed` / `PlayOneShot` / `Stop` / `UnPause` |
| `bypassEffects` / `bypassListenerEffects` / `bypassReverbZones` |
| `dopplerLevel` / `enabled` / `loop` |
| `maxDistance` / `rolloffMode` / `minDistance` / `mute` / `pitch` / `playOnAwake` |
| `priority` / `spatialize` / `spread` / `time` / `volume` |

### 2.3 Audio Filters(8 种)

**AudioDistortionFilter**:`decayRatio` / `delay` / `dryMix` / `enabled` / `wetMix`

**AudioEchoFilter**:`decayRatio` / `delay` / `dryMix` / `enabled` / `wetMix`

**AudioHighPassFilter**:`cutoffFrequency` / `enabled` / `highpassResonanceQ`

**AudioLowPassFilter**:`cutoffFrequency` / `enabled` / `lowpassResonanceQ`

**AudioReverbFilter**:`decayHFRatio` / `decayTime` / `density` / `diffusion` / `dryLevel` / `enabled` / `hfReference` / `reflectionsDelay` / `reflectionsLevel` / `reverbDelay` / `reverbLevel` / `room` / `roomHF` / `roomLF`

**AudioReverbZone**:`decayHFRatio` / `decayTime` / `density` / `diffusion` / `enabled` / `HFReference` / `LFReference` / `maxDistance` / `minDistance` / `reflections` / `reflectionsDelay` / `room` / `roomHF` / `roomLF`

### 2.4 Button

| 成员 |
|------|
| `enabled` / `interactable` / `targetGraphic` |

### 2.5 Collider

| 成员 |
|------|
| `enabled` / `isTrigger` |

### 2.6 Dropdown

| 成员 |
|------|
| `captionText` / `enabled` / `interactable` / `itemText` / `targetGraphic` / `template` / `value` |

### 2.7 Image

| 成员 |
|------|
| `alphaHitTestMinimumThreshold` / `enabled` / `fillAmount` / `fillCenter` / `fillClockwise` / `fillOrigin` / `maskable` / `preserveAspect` / `raycastTarget` / `useSpriteMesh` |

### 2.8 GameObject

| 成员 |
|------|
| `SetActive` |

### 2.9 InputField

> **FACT**:InputField 字符上限为 **16,000 字符**(Text 组件渲染上限)。

| 成员 |
|------|
| `ForceLabelUpdate` |
| `caretBlinkRate` / `caretPosition` / `caretWidth` / `characterLimit` |
| `customCaretColor` / `enabled` / `interactable` / `readOnly` |
| `selectionAnchorPosition` / `text` / `textComponent` / `selectionFocusPosition` |

### 2.10 Light

| 成员 |
|------|
| `Reset` |
| `bounceIntensity` / `colorTemperature` / `cookie` / `enabled` / `intensity` / `range` |
| `shadowBias` / `shadowNearPlane` / `shadowNormalBias` / `shadowStrength` / `spotAngle` |

### 2.11 LineRenderer

| 成员 |
|------|
| `allowOcclusionWhenDynamic` / `shadowCastingMode` / `enabled` |
| `endWidth` / `loop` / `motionVectorGenerationMode` / `numCapVertices` / `numCornerVertices` |
| `probeAnchor` / `receiveShadows` / `shadowBias` / `startWidth` / `lightProbeUsage` / `useWorldSpace` / `widthMultiplier` |

### 2.12 Mask

| 成员 |
|------|
| `enabled` / `showMaskGraphic` |

### 2.13 MeshRenderer

| 成员 |
|------|
| `shadowCastingMode` / `enabled` / `probeAnchor` / `probeAnchor` / `receiveShadows` / `lightProbeUsage` |

### 2.14 ParticleSystem

| 成员 |
|------|
| `Clear` / `Emit` / `Pause` / `Play` / `Simulate` / `Stop` / `TriggerSubEmitter` |
| `time` / `useAutoRandomSeed` |

### 2.15 ParticleSystemForceField

| 成员 |
|------|
| `endRange` / `gravityFocus` / `length` / `multiplyDragByParticleSize` / `multiplyDragByParticleVelocity` / `startRange` |

### 2.16 Projector

| 成员 |
|------|
| `aspectRatio` / `enabled` / `nearClipPlane` / `farClipPlane` / `fieldOfView` / `orthographic` / `orthographicSize` |

### 2.17 RawImage

| 成员 |
|------|
| `enabled` / `maskable` / `raycastTarget` |

### 2.18 RectMask2D

| 成员 |
|------|
| `enabled` |

### 2.19 Scrollbar

| 成员 |
|------|
| `enabled` / `handleRect` / `interactable` / `numberOfSteps` / `size` / `targetGraphic` / `value` |

### 2.20 ScrollRect

| 成员 |
|------|
| `content` / `decelerationRate` / `elasticity` / `enabled` / `horizontal` / `horizontalNormalizedPosition` |
| `horizontalScrollbar` / `horizontalScrollbarSpacing` / `inertia` / `scrollSensitivity` |
| `vertical` / `verticalNormalizedPosition` / `verticalScrollbar` / `verticalScrollbarSpacing` / `viewport` |

### 2.21 Selectable

| 成员 |
|------|
| `enabled` / `interactable` / `targetGraphic` |

### 2.22 SkinnedMeshRenderer

| 成员 |
|------|
| `allowOcclusionWhenDynamic` / `shadowCastingMode` / `enabled` |
| `lightProbeProxyVolumeOverride` / `motionVectorGenerationMode` / `probeAnchor` / `receiveShadows` |
| `rootBone` / `skinnedMotionVectors` / `updateWhenOffscreen` / `lightProbeUsage` |

### 2.23 Slider

| 成员 |
|------|
| `enabled` / `fillRect` / `handleRect` / `interactable` |
| `maxValue` / `minValue` / `normalizedValue` / `targetGraphic` / `value` / `wholeNumbers` |

### 2.24 Text

| 成员 |
|------|
| `alignByGeometry` / `enabled` / `fontSize` / `lineSpacing` / `maskable` / `raycastTarget` |
| `resizeTextForBestFit` / `resizeTextMaxSize` / `resizeTextMinSize` / `supportRichText` / `text` |

### 2.25 Toggle

| 成员 |
|------|
| `enabled` / `group` / `interactable` / `isOn` / `targetGraphic` |

### 2.26 ToggleGroup

| 成员 |
|------|
| `allowSwitchOff` / `enabled` |

### 2.27 TrailRenderer

| 成员 |
|------|
| `Clear` / `allowOcclusionWhenDynamic` / `autodestruct` / `shadowCastingMode` / `enabled` |
| `emitting` / `endWidth` / `motionVectorGenerationMode` / `numCapVertices` / `numCornerVertices` |
| `probeAnchor` / `receiveShadows` / `shadowBias` / `startWidth` / `lightProbeUsage` / `widthMultiplier` |

### 2.28 UdonBehaviour

| 成员 |
|------|
| `RunProgram` / `SendCustomEvent` / `Interact` |

---

## 三、可作为 UI Event Target 的完整组件列表

```
Animator
AudioSource
AudioDistortionFilter
AudioEchoFilter
AudioHighPassFilter
AudioLowPassFilter
AudioReverbFilter
AudioReverbZone
Button
Collider
Dropdown
Image
GameObject
InputField
Light
LineRenderer
Mask
MeshRenderer
ParticleSystem
ParticleSystemForceField
Projector
RawImage
RectMask2D
Scrollbar
ScrollRect
Selectable
SkinnedMeshRenderer
Slider
Text
Toggle
ToggleGroup
TrailRenderer
UdonBehaviour
```

> **FACT**:任何不在此列表中的组件,均**不能**被 UI Event 直接调用。

---

## 四、典型用法

### 4.1 Button → Animator.Play

```yaml
# Unity Inspector 配置
Button → OnClick() → Animator.Play("StateName")
```

### 4.2 Slider → AudioSource.volume

```yaml
# Unity Inspector 配置
Slider → OnValueChanged(float) → AudioSource.volume
```

### 4.3 Toggle → GameObject.SetActive

```yaml
# Unity Inspector 配置
Toggle → OnValueChanged(bool) → GameObject.SetActive(bool)
```

### 4.4 InputField → UdonBehaviour.SendCustomEvent

```yaml
# Unity Inspector 配置
InputField → OnValueChanged(string) → UdonBehaviour.SendCustomEvent("OnInputChanged")
```

### 4.5 Button → UdonBehaviour.RunProgram

> **FACT**:`RunProgram` 可用于**强制重启 Udon 程序**,等价于"重新执行 _start"。

```yaml
Button → OnClick() → UdonBehaviour.RunProgram
```

---

## 五、底层机制(【推断】)

### 5.1 UI Event 调用栈

```
Unity UI Event
  ↓ UnityEvent.Invoke
目标组件的 Method/Property
  ↓
VRChat 编译时校验白名单
  ↓
运行时通过 Reflection 缓存查找
  ↓
直接 C# 调用(无 Udon VM)
```

### 5.2 性能特征

| 方式 | 性能 | 灵活性 |
|------|------|--------|
| UI Event(白名单) | ⭐⭐⭐⭐⭐(直接 C# 调用) | ⭐⭐(仅白名单) |
| UdonBehaviour + SendCustomEvent | ⭐⭐(经 Udon VM 调度) | ⭐⭐⭐⭐⭐(任意逻辑) |
| SendCustomNetworkEvent | ⭐(网络序列化) | ⭐⭐⭐⭐⭐(跨玩家) |

**最佳实践**:能用 UI Event 就用 UI Event,只在需要复杂逻辑时退到 UdonBehaviour。

---

## 六、与 UdonBehaviour 的协作

### 6.1 简单 UI 控制

| 场景 | 推荐 |
|------|------|
| 按钮控制音视频 | UI Event → AudioSource |
| 滑块控制音量 | UI Event → AudioSource.volume |
| Toggle 开关 UI | UI Event → GameObject.SetActive |
| 简单计数 | UI Event → UdonBehaviour.SendCustomEvent |

### 6.2 复杂逻辑控制

```csharp
// 复杂逻辑必须用 UdonBehaviour
public class ComplexButtonHandler : UdonSharpBehaviour
{
    public void OnButtonClick()  // UI Event 调用此方法
    {
        // 复杂逻辑
        UpdateScore();
        SyncToNetwork();
        PlayEffects();
    }
}
```

---

## 七、缺失的方法(常见需求)

> **FACT**:以下方法**不在白名单内**,**不能**被 UI Event 直接调用。

| 不支持 | 解决方案 |
|--------|----------|
| 访问 Transform 字段 | 使用 UdonBehaviour + 内部逻辑 |
| 访问 Rigidbody 字段 | 同上 |
| 自定义方法(无白名单) | 同上 |
| 跨玩家调用 | `SendCustomNetworkEvent` |
| 数据持久化 | UdonBehaviour + PlayerData |

---

## 八、风险与限制

### 8.1 编译时静默忽略

> **【推断】** 如果配置了白名单外的方法,可能在编译时**静默忽略**而非报错。建议测试时使用 Build & Test 验证。

### 8.2 运行时限制

- UI Event 不可携带 Udon 复杂类型
- 不可作为 `SendCustomNetworkEvent` 的目标
- 不可调用 `UdonBehaviour.RunProgram` 进行**条件性**重启(只能全重启)

### 8.3 性能陷阱

- **N 个按钮 + N 个 AudioSource** = N 次 UI Event 监听,**无显著开销**
- 但若每个按钮都触发 UdonBehaviour.SendCustomEvent,**Udon VM 调度成本累积**

---

## 九、与其他文档的关系

| 相关文档 | 用途 |
|----------|------|
| `memory/api/udonsharp-runtime.md` | UdonSharp 完整运行时 |
| `memory/api/udon-type-exposure.md` | 类型暴露规则 |
| `memory/api/events-reference.md` | Udon 事件完整 API |
| `memory/world/udon/using-build-test.md` | 测试 UI 事件 |

---

## 十、检查清单(工程交付前)

- [ ] 所有 UI Event 目标组件在白名单内
- [ ] InputField 字符限制在 16,000 以内
- [ ] 复杂逻辑(>=3 个操作)回退至 UdonBehaviour
- [ ] 测试 Build & Test 确认 UI 事件触发
- [ ] 没有滥用 `UdonBehaviour.RunProgram`(仅在需要重启时使用)
