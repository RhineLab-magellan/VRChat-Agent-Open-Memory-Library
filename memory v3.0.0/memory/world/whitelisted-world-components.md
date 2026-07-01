---
title: "Allowlisted World Components"
category: world
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - constraint
  - event
aliases:
  - "Allowlisted World Components"
  - whitelisted-world-components
related:
  - community-labs.md
  - companions.md
  - creator-economy.md
  - world/udon/data-containers/index.md
  - items.md
---
# Allowlisted World Components

> 来源: VRChat 官方文档 (https://creators.vrchat.com/worlds/whitelisted-world-components/)
> 源 URL Last Updated: **Nov 25, 2025**
> 抓取日期: 2026-06-15
> 置信度: High

---

## Domain

**World → API 白名单** — VRChat World 中**所有**可用的 Script 组件完整清单。**不在此清单中的组件将无法工作**。

## Subdomain

- Unity 内置组件
- VRChat 自定义组件
- TextMeshPro
- 后期处理
- 第三方 Asset（Dynamic Bone / Final IK / AVPro / Oculus Spatializer）
- Unity UI / Event System

## Conclusion

VRChat World 维护一个**封闭的 Script 白名单**，分为 **10 个组件集合**，总计约 **200+ 个可用组件**。**任何不在白名单中的 Script 在 World 中将静默失败**。Quest 平台有额外限制（见脚注）。白名单的**核心动机是安全 + 性能**——禁止 I/O、网络、反射、动态加载等危险 API。

---

## FACT — 10 个组件集合完整清单

| # | 组件集合 | 数量 | 类别 |
|---|---|---|---|
| 1 | Unity Components | 76 | Unity 内置 |
| 2 | VRChat Components | 15 | VRChat SDK |
| 3 | Dynamic Bone | 2 | 第三方（已弃用） |
| 4 | Text Mesh Pro | 11 | Unity 内置 |
| 5 | Unity Event System | 10 | Unity UI 输入 |
| 6 | Unity UI | 30 | Unity uGUI |
| 7 | Post Processing Stack V2 | 3 | 后期处理 |
| 8 | AVPro | 7 | 视频播放 |
| 9 | Oculus Spatializer Unity | 4 | 空间音频 |
| 10 | Final IK | 62 | 反向运动学 |

---

## Evidence — 完整组件清单

### 1. Unity Components (76 个)

**Animation / Constraints**:
- AimConstraint
- Animator
- LookAtConstraint
- ParentConstraint
- PositionConstraint
- RotationConstraint
- ScaleConstraint

**Audio Filters** (8 个):
- AudioChorusFilter
- AudioDistortionFilter
- AudioEchoFilter
- AudioHighPassFilter
- AudioLowPassFilter
- AudioReverbFilter
- AudioReverbZone
- AudioSource

**Rendering**:
- BillboardRenderer
- Canvas, CanvasGroup, CanvasRenderer
- FlareLayer
- Halo
- LensFlare
- Light
- LightProbeGroup
- LightProbeProxyVolume
- LineRenderer
- MeshFilter
- MeshRenderer
- OcclusionArea
- OcclusionPortal
- ParticleAnimator
- ParticleEmitter
- ParticleRenderer
- ParticleSystem
- ParticleSystemForceField
- ParticleSystemRenderer
- Projector
- RectTransform
- ReflectionProbe
- Rendering.SortingGroup
- SkinnedMeshRenderer
- Skybox
- SpriteMask
- SpriteRenderer
- Terrain
- TerrainCollider
- TextMesh
- Tilemap
- TilemapRenderer
- TrailRenderer
- Tree
- VideoPlayer
- WindZone

**Physics / Colliders**:
- BoxCollider
- CapsuleCollider
- CharacterJoint
- Cloth
- ConfigurableJoint
- ConstantForce
- FixedJoint
- HingeJoint
- MeshCollider
- Rigidbody
- SphereCollider
- SpringJoint
- WheelCollider
- WorldParticleCollider

**Navigation**:
- Grid
- NavMeshAgent
- NavMeshObstacle
- OffMeshLink

**Transform / Core**:
- Camera
- Transform

**EllipsoidParticleEmitter / MeshParticleEmitter** (旧粒子系统):
- EllipsoidParticleEmitter
- MeshParticleEmitter

**PlayableDirector**:
- PlayableDirector

**注意**:
- `WorldParticleCollider` 是 Unity 旧粒子系统专用，Unity 5.4+ 已弃用
- `Camera` 允许，但受 `memory/world/vrc-camera-settings.md` 限制
- `Light` 允许但需注意阴影/烘焙

### 2. VRChat Components (15 个)

| 组件 | 状态 | 文档 |
|---|---|---|
| VRC_AvatarPedestal | ✅ Active | `/worlds/components/vrc_avatarpedestal` |
| VRCContactReceiver¹ | ✅ Active | `/common-components/contacts#vrccontactreceiver` |
| VRCContactSender¹ | ✅ Active | `/common-components/contacts#vrccontactsender` |
| VRC_IKFollower | ⚠ **已弃用** | 用 VRChat Constraints 或 Unity Constraints 代替 |
| VRC_MidiListener | ✅ Active | `/worlds/udon/midi/realtime-midi/` |
| VRC_MirrorReflection | ✅ Active | `/worlds/components/vrc_mirrorreflection` |
| VRCPhysBone¹ | ✅ Active | `/common-components/physbones#vrcphysbone` |
| VRCPhysBoneCollider¹ | ✅ Active | `/common-components/physbones#vrcphysbonecollider` |
| VRCPhysBoneRoot | ✅ Active | `/common-components/physbones#vrcphysboneroot` |
| VRCPipelineManager | ✅ Active | `/sdk/vrcpipelinemanager` |
| VRC_PortalMarker | ✅ Active | `/worlds/components/vrc_portalmarker` |
| VRC_SceneDescriptor | ✅ Active | `/worlds/components/vrc_scenedescriptor` |
| VRC_SpatialAudioSource | ✅ Active | `/worlds/components/vrc_spatialaudiosource` |
| VRC_Station | ✅ Active | `/worlds/components/vrc_station` |
| VRC_UiShape | ✅ Active | `/worlds/components/vrc_uishape` |

¹ **有 shape limits**——见 `/worlds/components#world-shape-limits`

### 3. Dynamic Bone (2 个，**已弃用**)

| 组件 | 状态 | 替代 |
|---|---|---|
| DynamicBone | ⚠ **已弃用** | VRCPhysBone |
| DynamicBoneCollider | ⚠ **已弃用** | VRCPhysBoneCollider |

### 4. Text Mesh Pro (11 个)

- TMP_Dropdown
- TMP_InputField
- TMP_ScrollbarEventHandler
- TMP_SelectionCaret
- TMP_SpriteAnimator
- TMP_SubMesh
- TMP_SubMeshUI
- TMP_Text
- TextContainer
- TextMeshPro
- TextMeshProUGUI

### 5. Unity Event System (10 个)

- BaseInput
- BaseInputModule
- BaseRaycaster
- EventSystem
- EventTrigger
- PhysicsRaycaster
- PointerInputModule
- StandaloneInputModule
- TouchInputModule
- UIBehaviour

### 6. Unity UI (30 个)

**Layout**:
- AspectRatioFitter
- CanvasScaler
- ContentSizeFitter
- GridLayoutGroup
- HorizontalLayoutGroup
- HorizontalOrVerticalLayoutGroup
- LayoutElement
- LayoutGroup
- VerticalLayoutGroup

**Rendering / Mask**:
- BaseMeshEffect
- Graphic
- GraphicRaycaster
- Image
- Mask
- MaskableGraphic
- Outline
- PositionAsUV1
- RawImage
- RectMask2D
- Shadow

**Input**:
- Button
- Dropdown (注: 原文出现两次)
- InputField
- ScrollRect
- Scrollbar
- Selectable
- Slider
- Text
- Toggle
- ToggleGroup

### 7. Post Processing Stack V2 (3 个)

- PostProcessDebug
- PostProcessLayer
- PostProcessVolume

**PPSv1 状态**:
> "PPSv1 is not supported in either VRCSDK2 or VRCSDK3. It has been deprecated by Unity."

### 8. AVPro (7 个)

- ApplyToMaterial
- ApplyToMesh
- AudioOutput
- DisplayIMGUI
- DisplayUGUI
- **MediaPlayer** ⭐
- SubtitlesUGUI

**使用场景**: 视频播放（替代 Unity VideoPlayer，支持直播流）

### 9. Oculus Spatializer Unity (4 个)

- ONSPAmbisonicsNative
- ONSPAudioSource
- ONSPReflectionZone
- OculusSpatializerUnity

**使用场景**: 高级 3D 空间音频（HRTF）

### 10. Final IK (62 个)

> "VRChat has highly modified its implementation of FinalIK. As such, these components may not work as documented."

**IK Solver**:
- AimIK, CCDIK, FABRIK, FABRIKRoot
- FullBodyBipedIK, BipedIK
- LimbIK, LegIK
- LookAtIK, TrigonometricIK
- VRIK (VR IK)
- IK (基类), IKExecutionOrder

**Behaviour**:
- BehaviourBase, BehaviourFall, BehaviourPuppet
- Amplifier, AnimationBlocker
- BodyTilt, Inertia, Recoil
- HitReaction, HitReactionVRIK

**Grounder** (5 个):
- Grounder, GrounderBipedIK, GrounderFBBIK
- GrounderIK, GrounderQuadruped, GrounderVRIK

**Interaction**:
- InteractionObject, InteractionSystem, InteractionTarget, InteractionTrigger
- InteractionTrigger 触发器
- TriggerEventBroadcaster
- MuscleCollisionBroadcaster, JointBreakBroadcaster
- PressureSensor

**Puppet / Ragdoll**:
- PuppetMaster, PuppetMasterSettings
- Prop, PropRoot
- RagdollCreator, RagdollEditor, RagdollUtility
- BipedRagdollCreator

**Poser**:
- AimPoser, GenericPoser, HandPoser, Poser
- OffsetModifier, OffsetModifierVRIK, OffsetPose

**Rotation Limits**:
- RotationLimit (基类)
- RotationLimitAngle, RotationLimitHinge
- RotationLimitPolygonal, RotationLimitSpline

**Other**:
- FingerRig, FBBIKArmBending, FBBIKHeadEffector
- ShoulderRotator, SolverManager, TwistRelaxer

---

## Analysis — 与现有知识库交叉引用

| 现有知识 | 关联 |
|---|---|
| `memory/api/not-exposed.md` | **未暴露 API 黑名单**——非白名单 Script 直接失败 |
| `memory/api/udon-type-exposure.md` | Udon Type Exposure Tree 索引 |
| `memory/api/exposed-types.md` | 详细暴露类型清单 |
| `memory/rules/vrchat-api-exposure.md` | API 暴露判断 |
| `memory/avatar/vrc-constraints.md` | VRC Constraints（与 Unity Constraints 对比） |
| `memory/world/items.md` | Layer / Mirror / Physics |
| `memory/world/sdk-prefabs.md` | SDK Prefab 使用的具体组件 |
| `memory/world/supported-assets.md` | 第三方 Scripted Asset（Final IK / Dynamic Bone / PPSv2 / AVPro） |
| `memory/world/creator-economy.md` | Store API 相关 |
| `memory/world/udon/data-containers/index.md` | Udon 数据容器 |

### Quest 平台限制

> "The Android version of VRChat has some exceptions to this list. Check [here](/platforms/android/quest-content-limitations#components) for more info."

详细限制见 `memory/platform/android-development.md`。**关键差异**:
- TextMeshPro ✅ 保留
- PPSv2 ❌ 不可用
- Final IK ❌ 不可用
- Dynamic Bone ❌ 不可用
- AVPro ⚠ 可能受限

### Shape Limits（重要约束）

> "Maximum shape limits apply to these components. For more information, check the advice [here](/worlds/components#world-shape-limits)."

**受 Shape Limit 影响的组件**:
- VRCContactReceiver
- VRCContactSender
- VRCPhysBone
- VRCPhysBoneCollider

**含义**: 复杂 Avatar/World 中这些组件的数量、嵌套深度、参数规模有上限，超过会导致警告或上传失败。

---

## Inference 【推断】

【推断 1】**白名单是封闭的且服务端校验**——World 上传时 VRChat 服务器会扫描所有 Component 引用，不在白名单中的 Script 会被剔除或导致上传失败。

【推断 2】**白名单设计原则是"显式拒绝"而非"白名单 + 黑名单"**——这种策略保证安全（不会意外引入危险 API），但灵活度低（新库需官方支持）。

【推断 3】**Final IK 有 60+ 组件白名单**——表明 VRChat 对 Final IK 进行了**完整的 Unity 集成**，而非简单 hack。这意味着 Final IK 在 World 中的功能是**受支持的**，但**实现被修改过**（"may not work as documented"）。

【推断 4】**AVPro + Oculus Spatializer 暗示 VRChat 视频/音频标准**——AVPro 处理视频，Oculus Spatializer 处理 3D 音频，两者都是商业 Asset。

【推断 5】**UI 组件数量最多（30 个）**——说明 Unity uGUI 在 VRChat 中是**完整支持**的，UI 开发不需要特殊方案。

【推断 6】**Final IK VRIK 是 VR 关键**——VRIK 是支持 VR 头手追踪的 IK 方案，在 World 中用于复杂 NPC 互动。

---

## Risks

| 风险 | 严重度 | 说明 |
|---|---|---|
| **使用非白名单 Script** | 🔴 高 | World 上传失败或运行时静默失败 |
| **Shape Limit 超限** | 🟡 中 | Contact/PhysBone 组件超规模导致警告 |
| **Final IK 文档不一致** | 🟡 中 | "may not work as documented"——升级需测试 |
| **Quest 平台组件缺失** | 🟡 中 | PPSv2 / Final IK / Dynamic Bone 在 Quest 不可用 |
| **AVPro 兼容性** | 🟡 中 | 第三方视频库可能与新 Unity 版本冲突 |
| **Dynamic Bone 迁移** | 🟢 低 | 旧 World 升级时需迁移到 PhysBones |

---

## Unknowns & Open Questions

| 编号 | 问题 |
|---|---|
| U-1 | 哪些 Script 是 Quest 端**额外**不可用的？完整列表在哪？ |
| U-2 | "shape limits" 具体数值？每个组件 / 总数？ |
| U-3 | 是否存在 Script 在某些 SDK 版本被加入/移除白名单？ |
| U-4 | Oculus Spatializer 在 Quest 上的实际行为？ |
| U-5 | 是否支持其他空间音频方案（如 Steam Audio、Meta XR Audio）？ |

---

## Recommendations

### 起步检查

1. **World 上传前**——检查每个 GameObject 上的 Component 是否在白名单
2. **跨平台发布前**——使用 `EasyQuestSwitch` 自动处理 PC/Quest 差异（`memory/platform/easyquestswitch.md`）
3. **升级 SDK 时**——重新检查白名单变更

### 选型决策

| 需求 | 推荐 | 备选 |
|---|---|---|
| **UI** | Unity uGUI（30 组件完整支持） | TextMeshPro（文本） |
| **约束** | Unity Constraints | VRC Constraints（已弃用）/ Final IK（仅 PC） |
| **物理骨骼** | VRCPhysBone | Dynamic Bone（已弃用） |
| **视频** | AVPro（直播） | Unity VideoPlayer（VOD） |
| **空间音频** | Oculus Spatializer | Unity AudioSource（基础） |
| **后期处理** | PPSv2（仅 PC） | 无（Quest 不支持） |
| **IK** | Final IK（仅 PC） | Unity Constraints（Quest 兼容） |

### 跨平台模式

```csharp
// 平台条件编译
#if UNITY_ANDROID && !UNITY_EDITOR
    // Quest 端禁用 PC 专用组件
    GetComponent<PostProcessLayer>().enabled = false;
    GetComponent<DynamicBone>().enabled = false;
    // ... 其他平台特定逻辑
#endif
```

或者使用 **EasyQuestSwitch** 自动化（推荐）。

### 性能优化

1. **优先 Unity 内置组件**——白名单中数量最多（76 个）
2. **避免 Final IK 在性能敏感场景**——IK 求解开销大
3. **UI 避免使用 Mask**——Mask 在移动端性能差；用 RectMask2D 代替

---

## 引用

- **源页面**: https://creators.vrchat.com/worlds/whitelisted-world-components/
- **Quest 限制**: https://creators.vrchat.com/platforms/android/quest-content-limitations#components
- **Shape Limits**: https://creators.vrchat.com/worlds/components#world-shape-limits
- **Unity Constraints**: https://docs.unity3d.com/2022.3/Documentation/Manual/Constraints.html
- **VRChat Constraints**: https://creators.vrchat.com/common-components/constraints/
- **VRChat PhysBones**: https://creators.vrchat.com/common-components/physbones/
- **VRChat Contacts**: https://creators.vrchat.com/common-components/contacts/
- **相关知识**: `memory/api/not-exposed.md` (反向参考：黑名单)
- **相关知识**: `memory/api/udon-type-exposure.md` (类型暴露树)
- **相关知识**: `memory/platform/android-development.md` (Quest 限制)
- **相关知识**: `memory/platform/easyquestswitch.md` (平台切换工具)
