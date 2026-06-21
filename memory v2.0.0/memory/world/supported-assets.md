---
title: Supported Scripted Assets
category: world

knowledge_level: applied
status: active

tags:
  - world
  - physbone
  - udonsharp

aliases:
  - "Supported Scripted Assets"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Supported Scripted Assets

> 来源: VRChat 官方文档 (https://creators.vrchat.com/worlds/supported-assets/)
> 源 URL Last Updated: **Feb 23, 2024**
> 抓取日期: 2026-06-15
> 置信度: High
> Domain: World → External Assets / Script Compatibility

---

## Domain

**World → 外部 Scripted Asset** — VRChat World 中允许使用的第三方 Asset 列表。

## Subdomain

- 文本渲染（TextMeshPro）
- 后期处理（Post Processing Stack v2）
- 物理模拟（Dynamic Bone）
- 反向运动学（Final IK）

## Conclusion

VRChat Worlds 仅支持 **4 个外部 Scripted Asset**：**TextMeshPro**（必选文本方案）、**Post Processing Stack v2**（后期处理）、**Final IK**、**Dynamic Bone**。**除 TextMeshPro 外，其他 3 个在 Quest 上不可用**。Post Processing v1 **完全不支持**。Dynamic Bone **仅 v1.3.0 及以下可用**，已被 VRChat PhysBones 取代。

---

## FACT — 支持的 Scripted Asset 完整列表

| Asset | 类别 | 状态 | Quest 兼容 | 推荐度 |
|---|---|---|---|---|
| **TextMeshPro** | 文本渲染 | ✅ Active | ✅ 支持 | ⭐⭐⭐⭐⭐ 强烈推荐 |
| **Post Processing Stack v2** | 后期处理 | ✅ Active | ❌ **不可用** | ⭐⭐⭐⭐ 标准方案 |
| **Final IK** | 反向运动学 | ✅ Active | ❌ **不可用** | ⭐⭐⭐ 功能丰富 |
| **Dynamic Bone** | 物理模拟 | ⚠ **已弃用** | ❌ **不可用** | ❌ **改用 PhysBones** |

**不在白名单中（**不**允许）**:
- Post Processing Stack v1（已弃用）
- 任何其他第三方 Scripted Asset（unitypackage 形式）

---

## Evidence — 各 Asset 详解

### 1. TextMeshPro ✅ 强烈推荐

> "'TextMesh Pro is the ultimate text solution for Unity. It's the perfect replacement for Unity's UI Text & Text Mesh.'"

> "As of Unity 2018, TextMesh Pro is a built-in component of Unity. We strongly recommend TextMeshPro over Unity's built-in text components, as it delivers high-quality text in any font size or screen size."

**关键事实**:
- **Unity 2018+ 内置组件**——无需单独导入
- **强推荐** 替代 Unity 内置 Text / TextMesh
- **优势**: 任意字号/屏幕大小下高质量文本
- **Quest 兼容**: ✅ 唯一可用的 Scripted Asset

**相关组件清单**（来自 `whitelisted-world-components.md`）:
- TMP_Dropdown, TMP_InputField, TMP_ScrollbarEventHandler
- TMP_SelectionCaret, TMP_SpriteAnimator
- TMP_SubMesh, TMP_SubMeshUI
- TMP_Text, TextContainer, TextMeshPro, TextMeshProUGUI

**使用场景**:
- HUD / 菜单文本
- 玩家名牌（虽然 VRChat 内部也有 Nameplate）
- 任意 UI 文本需求

### 2. Post Processing Stack v2 ✅ 标准方案

> "Import from Package Manager."

> "We strongly suggest checking out [Silent's Post Processing guide](https://gitlab.com/s-ilent/SCSS/-/wikis/Other/Post-Processing) for more info and best practices."

> **caution** "Do not import the `Test` folder when importing post-processing. It will cause script errors which will prevent you from uploading the world."

**关键事实**:
- **导入方式**: Package Manager（**不是 Asset Store**）
- **致命警告**: ⚠ **不要导入 `Test` 文件夹**——会导致脚本错误，世界无法上传
- **Quest 兼容**: ❌ 不可用（Quest World 无后处理）
- **额外资源**: Silent 的 SCSS Wiki 提供最佳实践

**PPSv2 组件清单**:
- PostProcessDebug
- PostProcessLayer
- PostProcessVolume

**PPSv1 状态**:
> "PPSv1 is not supported in either VRCSDK2 or VRCSDK3. It has been deprecated by Unity."

- ❌ **PPSv1 完全不支持**（SDK2 和 SDK3 都不支持）
- ❌ 已被 Unity 弃用

**使用场景**:
- 颜色分级 / LUT
- Bloom / Vignette
- 屏幕空间特效
- ⚠ **跨平台 World 必须在 PC/Quest 上分别测试**

### 3. Final IK ✅ 功能丰富

> "'The final Inverse Kinematics solution for the game developer.'"

> "VRChat has highly modified its implementation of FinalIK. As such, these components may not work as documented."

> "We do not directly support or test custom FinalIK implementations in worlds. However, they _should_ work fine, and if we must intentionally break one or more of these, we will try our best to inform creators."

**关键事实**:
- **VRChat 高度修改**——可能不按原文档工作
- **不直接支持/测试**自定义 FinalIK 实现
- **Quest 兼容**: ❌ 不可用
- **发现问题**: 通过 VRChat Feedback 报告

**Final IK 组件清单**（60+ 个）:
- AimIK, AimPoser, Amplifier
- AnimationBlocker, BehaviourBase, BehaviourFall, BehaviourPuppet
- BipedIK, BipedRagdollCreator, BodyTilt, CCDIK, FABRIK, FABRIKRoot
- FBBIKArmBending, FBBIKHeadEffector, FingerRig, FullBodyBipedIK
- GenericPoser, Grounder*（5 种）, HandPoser, HitReaction*
- IK, IKExecutionOrder, Inertia
- InteractionObject, InteractionSystem, InteractionTarget, InteractionTrigger
- JointBreakBroadcaster, LegIK, LimbIK, LookAtIK
- MuscleCollisionBroadcaster, OffsetModifier*, OffsetPose
- Poser, PressureSensor, Prop, PropRoot
- PuppetMaster, PuppetMasterSettings
- RagdollCreator, RagdollEditor, RagdollUtility
- Recoil, RotationLimit*
- ShoulderRotator, SolverManager
- TriggerEventBroadcaster, TrigonometricIK, TwistRelaxer
- **VRIK**（VR 反向运动学）

**使用场景**:
- 复杂 IK 绑定（机械臂、触手、尾巴）
- 玩家追踪（VR 头手）
- 自定义 Avatar 交互

**风险提示**:
- VRChat 文档明确 "may not work as documented"
- 不建议用于关键玩法逻辑
- 升级 VRChat SDK 时需重新测试

### 4. Dynamic Bone ⚠ 已弃用

> "'Dynamic Bone applies physics to objects. With simple setup, your object will move realistically.'"

> "\*Works up to v1.3.0, currently supplied version on asset store may not work."

**关键事实**:
- **状态**: ⚠ **已弃用**——VRChat 推荐使用 PhysBones
- **版本限制**: ✅ **仅 v1.3.0 及以下可用**
- **Quest 兼容**: ❌ 不可用
- **替代方案**: **VRChat PhysBones**（`memory/avatar/` 中已记录）

**Dynamic Bone 组件**:
- DynamicBone（**已弃用**）→ 改用 VRCPhysBone
- DynamicBoneCollider（**已弃用**）→ 改用 VRCPhysBoneCollider

**使用建议**:
- ❌ **新 World 不应使用** Dynamic Bone
- ✅ 旧 World 升级时迁移到 PhysBones
- ✅ PhysBones 是 Avatar 域标准，但**在 World 中也可用**（通过 `VRCPhysBoneRoot`）

---

## Analysis — 与现有知识库交叉引用

| 现有知识 | 关联 |
|---|---|
| `memory/api/not-exposed.md` | 黑名单 API——其他第三方 Asset 不会暴露给 Udon |
| `memory/world/whitelisted-world-components.md` | 完整白名单组件清单 |
| `memory/avatar/` | PhysBones 在 Avatar 域的详细文档 |
| `memory/world/performance-guide.md` | 后期处理对 GPU 的影响 |
| `memory/sources/example-central.md` | Post Processing v2 实战案例 |

### Asset 选择决策

| 需求 | 推荐 | 备选 |
|---|---|---|
| **文本渲染** | TextMeshPro | （无） |
| **后期处理** | Post Processing Stack v2 | Silent 的 SCSS Wiki 方案 |
| **IK 绑定** | VRChat Constraints | Final IK（不推荐，Quest 不可用） |
| **物理模拟** | VRChat PhysBones | Dynamic Bone v1.3.0（已弃用） |
| **Quest 兼容** | 仅 TextMeshPro + PhysBones | — |

---

## Inference 【推断】

【推断 1】**白名单是封闭的**——VRChat 不会自动支持新发布的 Asset；任何新 Scripted Asset 都需要 VRChat 官方更新白名单。

【推断 2】**Quest 不支持 Post Processing / Final IK / Dynamic Bone**——是因为 Android 性能预算有限，VRChat 优先保证基础功能。

【推断 3】**TextMeshPro 是 Unity 2018+ 内置**——SDK 3.x 对应 Unity 2022.3 LTS，TMP 早已内置无需单独 Package。

【推断 4】**PPSv1 文档仍存在但功能已无**——可能是 SEO 目的保留链接，新用户应直接用 PPSv2。

【推断 5】**Final IK 的"高度修改"是技术债**——VRChat 为了支持自家 Avatar 3.0 物理系统对 FinalIK 做了侵入式修改，导致版本兼容性脆弱。

---

## Risks

| 风险 | 严重度 | 说明 |
|---|---|---|
| **导入 Test 文件夹** | 🔴 高 | Post Processing 的 Test 文件夹含**编译错误**——World **无法上传** |
| **PPSv1 误用** | 🔴 高 | PPSv1 已被 Unity 弃用且 VRChat 不支持，**直接失败** |
| **Dynamic Bone 新版本** | 🟡 中 | Asset Store 当前版本可能不兼容，**仅 v1.3.0 及以下可用** |
| **Final IK 跨版本** | 🟡 中 | VRChat 修改了实现，原文档可能误导 |
| **Quest 平台差异** | 🟡 中 | Post Processing / Final IK / Dynamic Bone **在 Quest 上完全不工作** |
| **迁移成本** | 🟢 低 | Dynamic Bone → PhysBones 需重做配置 |

---

## Unknowns & Open Questions

| 编号 | 问题 |
|---|---|
| U-1 | Final IK 是否支持新版本（购买后能否升级）？ |
| U-2 | Post Processing v2 在新版 Unity 上是否有兼容问题？ |
| U-3 | TextMeshPro 在 Quest 性能表现？ |
| U-4 | 是否还有其他 Asset 正在申请白名单？ |
| U-5 | 是否有 Avatar 域专用 Asset 可以移植到 World 域？ |

---

## Recommendations

### 文本需求

✅ **永远使用 TextMeshPro**——Unity 内置，性能优秀，Quest 兼容。
❌ **不要使用** Unity 内置 Text / TextMesh。

### 后期处理

1. ✅ **PPSv2 + Package Manager** 导入
2. ❌ **绝不要勾选 Test 文件夹**（上传前在 Unity Console 检查无错误）
3. ⚠ **Quest World 必须移除 PPSv2**（详见 `platform/android-development.md`）
4. 📚 参考 Silent's Post Processing Guide

### IK 需求

1. **首选 VRChat Constraints**（Avatar 域标准，Quest 兼容）——在 World 中通过 GameObject 父子关系实现
2. **次选 Final IK**——仅 PC 平台，Quest 不可用
3. ⚠ 任何 IK 升级需重新测试 VRChat 兼容性

### 物理模拟

1. **必须使用 PhysBones**——Dynamic Bone 已弃用
2. **World 端使用 VRCPhysBoneRoot + VRCPhysBone + VRCPhysBoneCollider**
3. ⚠ 旧 World 升级时系统化迁移

### 跨平台发布

```csharp
#if UNITY_ANDROID
    // 禁用所有非 TextMeshPro Scripted Asset
    camera.GetComponent<PostProcessLayer>().enabled = false;
    foreach (var dyn in GetComponentsInChildren<DynamicBone>())
        dyn.enabled = false;
    foreach (var fik in GetComponentsInChildren<IK>())
        fik.enabled = false;
#endif
```

或者使用 **EasyQuestSwitch** 自动平台切换（`memory/platform/easyquestswitch.md`）。

---

## 引用

- **源页面**: https://creators.vrchat.com/worlds/supported-assets/
- **相关页面**: https://creators.vrchat.com/worlds/whitelisted-world-components/ (完整组件白名单)
- **Silent's Post Processing Guide**: https://gitlab.com/s-ilent/SCSS/-/wikis/Other/Post-Processing
- **VRChat Feedback**: https://feedback.vrchat.com
- **Final IK Asset Store**: https://assetstore.unity.com/packages/tools/animation/final-ik-14290
- **Dynamic Bone Asset Store**: https://assetstore.unity.com/packages/tools/animation/dynamic-bone-16743
- **相关知识**: `memory/platform/easyquestswitch.md` (PC/Quest 自动切换)
