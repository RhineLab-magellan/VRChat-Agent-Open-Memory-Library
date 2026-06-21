# Unity Layers in VRChat

> 来源: VRChat 官方文档 (https://creators.vrchat.com/worlds/layers)
> 源 URL Last Updated: **Mar 26, 2026**
> 抓取日期: 2026-06-15
> 置信度: High
> Domain: World → Layer / Physics / Sticker / Interaction

---

## Domain

**World → Layer 系统** — VRChat 对 Unity Layer 的预定义约定、限制、与 Physics/UI/Mirror 的交互。

## Subdomain

- Unity Layer 0-31 分配
- Sticker 系统（VRChat+）
- Physics 操作的 Layer Mask 实践
- Interaction Block / Passthrough
- 渲染 Culling

## Conclusion

VRChat SDK 在创建 Unity 项目时**自动配置 32 个 Layer 中的 22 个**（0-21），**Layer 22-30 是 User 自由层**，**Layer 31 被 Unity Editor Preview 占用**。World 上传时 VRChat 会**强制重置已使用 Layer 的名称和碰撞矩阵**。Physics 操作必须配合 `LayerMask` + `Utilities.IsValid` 避免命中 Items/Stickers 等"被保护"对象。

---

## FACT — Unity 32 个 Layer 完整分配表

| Layer | Name | 描述 | 允许 Sticker |
|---|---|---|---|
| 0 | **Default** | Unity 默认；VRChat Avatar Pedestals 使用 | ✔ |
| 1 | **TransparentFX** | Unity Flare Assets | ❌ |
| 2 | **IgnoreRaycast** | Unity Physics Raycast 不命中（无 mask 时）；**VRChat Physics 仍命中** | ❌ |
| 3 | **Item** | VRChat Items 玩家生成物；上传时被移到 Layer 0 | ❌ |
| 4 | **Water** | Unity Standard Assets；VRChat **Portals**、**Mirrors** 使用；常用于 Post Processing | ✔ |
| 5 | **UI** | ⚠ Unity UI 默认；VRChat UI pointer **仅在菜单打开时**命中；VRChat Camera 仅当 UI 启用时渲染 | ❌ |
| 6 | **reserved6** | ⚠ VRChat 保留；上传时 GameObject 被移到 Layer 0 | ❌ |
| 7 | **reserved7** | ⚠ VRChat 保留；上传时 GameObject 被移到 Layer 0 | ❌ |
| 8 | **Interactive** | Unity/VRChat 都不用；**推荐用于"禁止 Sticker"的 collider** | ❌ |
| 9 | **Player** | VRChat 其他玩家（**非本地玩家**） | ❌ |
| 10 | **PlayerLocal** | VRChat **本地玩家**；Humanoid Avatar **不渲染 head 骨骼** | ❌ |
| 11 | **Environment** | Unity/VRChat 都不用 | ✔ |
| 12 | **UiMenu** | ⚠ VRChat UI pointer **仅在菜单打开时**命中 | ❌ |
| 13 | **Pickup** | VRChat Pickups 默认 Layer；**不与玩家碰撞** | ❌ |
| 14 | **PickupNoEnvironment** | **仅与 Pickup (Layer 13) 碰撞** | ❌ |
| 15 | **StereoLeft** | Unity/VRChat 都不用 | ❌ |
| 16 | **StereoRight** | Unity/VRChat 都不用 | ❌ |
| 17 | **Walkthrough** | **不与玩家碰撞** | ✔ |
| 18 | **MirrorReflection** | VRChat **镜像渲染本地玩家**；**仅在镜中显示**；**不进主相机**；**不阻挡 Raycast** | ❌ |
| 19 | **InternalUI** | ⚠ VRChat 内部 UI（菜单、Nameplate、Debug） | ❌ |
| 20 | **HardwareObjects** | ⚠ VRChat 物理硬件虚拟表示（**控制器、Tracker**） | ❌ |
| 21 | **reserved4** | ⚠ VRChat 保留；上传时 GameObject 被移到 Layer 0 | ❌ |
| **22-30** | **Unused (User)** | **User 自由层**；上传时 VRChat **不覆盖** | (✔)¹ |
| 31 | **Editor Preview** | ⚠ Unity Editor Preview Window 占用 | (✔)¹ |

¹ Layers 22-31 默认允许 Sticker；可通过 Interaction Passthrough 禁用

---

## Evidence — 章节详解

### 1. Layer 上传覆盖规则

> "If you change the collision matrix, rename, or remove built-in layers, your changes will be overridden when you upload your world to VRChat."

> "Layers 22-31 are unused 'User' Unity layers. You can edit them freely, and changes to these layers will not be discarded when you build & upload your world."

**推论**:
- **User 自由层**（22-30）允许自定义名称和碰撞矩阵
- **Layer 31** 虽不强制覆盖但被 Unity Editor 占用，**不建议用于游戏内容**
- 上传行为是**自动且不可关闭**的——World 作者无法保留对 Layer 0-21 的修改

### 2. Sticker 系统

> "Stickers allow VRChat+ users to place images on `Collider` components in your world."

**关键规则**:
- Sticker 仅能放置在 **Collider** 组件上
- 允许 Layer（表内 ✔ 标记）: Default, Water, Environment, Walkthrough, 22-30, 31
- **禁止 Layer**: Interactive (8)、Player (9)、PlayerLocal (10)、MirrorReflection (18)、InternalUI (19)、HardwareObjects (20)、Pickup 系列
- **World 级别禁用**: VRChat Website → Edit → 关闭 Stickers

**推荐实践**（原文）:
> "We recommend using layer 8 ('Interactive') because it is unused by VRChat and Unity."

### 3. Physics 和 Layer — 需要 `Utilities.IsValid` 校验的方法

> "When using Physics operations, it's best to limit which layers you're testing against to avoid items on Reserved layers. It's also a good idea to use `Utilities.IsValid` on any object passed back to a Physics call to make sure you didn't accidentally pick up a 'protected' object, which will be `null`, possibly shutting down your UdonBehaviour."

**完整方法清单**（23 个）:

| # | 方法 | 说明 |
|---|---|---|
| 1 | `Physics.Raycast` | 射线，返回首个命中 |
| 2 | `Physics.RaycastAll` | 射线，返回所有命中 |
| 3 | `Physics.RaycastNonAlloc` | 射线，预分配数组（**减 GC**） |
| 4 | `Physics.SphereCast` | 球体投射 |
| 5 | `Physics.SphereCastAll` | 球体投射所有 |
| 6 | `Physics.SphereCastNonAlloc` | 球体投射优化版 |
| 7 | `Physics.OverlapSphere` | 球体内所有 collider |
| 8 | `Physics.OverlapBox` | Box 内所有 collider |
| 9 | `Physics.OverlapCapsule` | Capsule 内所有 collider |
| 10 | `Physics.OverlapSphereNonAlloc` | 球体重叠优化版 |
| 11 | `Physics.OverlapBoxNonAlloc` | Box 重叠优化版 |
| 12 | `Physics.OverlapCapsuleNonAlloc` | Capsule 重叠优化版 |
| 13 | `Rigidbody.SweepTest` | Rigidbody 单向碰撞测试 |
| 14 | `Rigidbody.SweepTestAll` | Rigidbody 路径所有命中 |
| 15 | `Physics.CapsuleCast` | Capsule 投射首个 |
| 16 | `Physics.CapsuleCastAll` | Capsule 投射所有 |
| 17 | `Physics.CapsuleCastNonAlloc` | Capsule 投射优化版 |
| 18 | `Physics.BoxCast` | Box 投射首个 |
| 19 | `Physics.BoxCastAll` | Box 投射所有 |
| 20 | `Physics.BoxCastNonAlloc` | Box 投射优化版 |
| 21 | `Collider.Raycast` | 对单个 collider 投射 |
| 22 | `Physics.CheckSphere` | 球体是否重叠任意 collider |
| 23 | `Physics.CheckBox` | Box 是否重叠任意 collider |
| 24 | `Physics.CheckCapsule` | Capsule 是否重叠任意 collider |

### 4. Interaction Block / Passthrough

**Interaction 行为**:
- Interaction（远距离抓取、UI 激光）**被大多数 VRChat Layer 阻挡**
- **以下 Layer 对 Interaction 透明**（可穿透交互）:
  - `UiMenu` (12)
  - `UI` (5)
  - `PlayerLocal` (10)
  - `MirrorReflection` (18)

**User Layer (22-31) 的 Interaction Passthrough**:
> "Interaction through User layers is blocked by default. Use the 'Interact Passthrough' mask to define layers that will be transparent to interaction (allow interactions to pass through)."

> "Note that collision test rays originate differently from Desktop/Mobile players (inside the player capsule) versus VR players (from the user's tracked hand). This means that VR players can penetrate colliders with their hand even when the player collider is blocked. Those same colliders will therefore not block interaction from the VR player, since the hand has penetrated."

**重要警告（VR vs Desktop 差异）**:
- **Desktop/Mobile**: 碰撞射线从 player capsule 内部出发
- **VR**: 碰撞射线从用户追踪的手部出发
- VR 用户的手可能**穿透 collider**，导致这些 collider **无法阻挡 VR 用户的 Interaction**

---

## Analysis — 与现有知识库交叉引用

| 现有知识 | 关联 |
|---|---|
| `memory/world/items.md` | Layer 3 (`Item`) 详述、Items 与 Udon 不可交互 |
| `memory/api/udon-type-exposure.md` | `Utilities.IsValid` 暴露状态 |
| `memory/rules/networking-rules.md` | Networked Object Layer 选择 |
| `memory/sources/example-central.md` | Pickup / Mirror 示例参考实现 |
| `memory/api/pickups.md` | Layer 13/14 (`Pickup`, `PickupNoEnvironment`) 行为 |

### Layer 选择决策树

```
需要 Sticker 支持吗？
├─ 是 → Default/Water/Environment/Walkthrough/User(22-30)
└─ 否 → 业务 Layer 选择
       ├─ 仅与 Pickup 碰撞 → PickupNoEnvironment (14)
       ├─ 不与玩家碰撞 → Walkthrough (17)
       ├─ 远距离交互可穿透 → UI (5) / UiMenu (12) / PlayerLocal (10) / MirrorReflection (18)
       └─ 标准碰撞 → Default (0) / Environment (11) / User (22-30)
```

---

## Inference 【推断】

【推断 1】**VRChat 上传时强制重置 Layer 配置是为了一致性**——避免 World 作者误改 Unity 内置 Layer 导致 VRChat 内部系统（玩家渲染、镜像、UI pointer）失效。

【推断 2】**`Interactive` (Layer 8) 是 Sticker 防御的标准答案**——文档明确推荐此用法，意味着它已成为社区惯例，可放心使用。

【推断 3】**`PlayerLocal` (Layer 10) 不渲染 head 骨骼**——是为 VR 头显用户避免"看到自己头内部"——第一人称 Avatar 渲染的常见需求。

【推断 4】**Layer 14 (`PickupNoEnvironment`) 解决 Pickup 与环境碰撞的经典痛点**——文档中未给具体用例，但从命名推断是为"可被拾取但不与场景静态碰撞"的对象设计。

【推断 5】**VR 玩家的手部射线与 Desktop capsule 射线的差异是隐藏陷阱**——可能让 World 作者在 Desktop 测试时通过的 collider 在 VR 上失效。

---

## Risks

| 风险 | 严重度 | 说明 |
|---|---|---|
| **修改 Layer 0-21** | 🔴 高 | 上传时强制重置，所有修改丢失 |
| **Physics 命中 Item** | 🔴 高 | 触发 UdonBehaviour 自禁用（见 `items.md`） |
| **未指定 LayerMask** | 🟡 中 | Physics 默认命中所有 Layer，可能误命中 Player/Item |
| **VR 玩家手部穿透** | 🟡 中 | Desktop 测试通过，VR 失效 |
| **Mirror 反射老 Layer** | 🟡 中 | 见 `items.md` 中关于 VRCMirror 的 Layer 修复 |
| **Sticker 污染 collider** | 🟢 低 | 使用 Layer 8 解决 |

---

## Unknowns & Open Questions

| 编号 | 问题 |
|---|---|
| U-1 | 哪些 Layer 在 Desktop 与 Android (Quest) 上行为有差异？ |
| U-2 | Layer 22-31 中是否存在某些 Layer 被 VRChat 未来功能占用？ |
| U-3 | Sticker 在 MirrorReflection Layer 上的行为？ |
| U-4 | "collision matrix" 具体哪些 Layer 对组合被默认禁用？ |
| U-5 | Unity 6 / 新 BRP 是否有 Layer 系统变更？ |

---

## Recommendations

### 实现层

```csharp
// 标准 Physics 安全模式
int hitLayerMask = LayerMask.GetMask(
    "Default", "Environment", "Interactive", "Pickup"
);  // 故意排除: Item, Player*, MirrorReflection, UI, InternalUI, reserved*

RaycastHit hit;
if (Physics.Raycast(origin, direction, out hit, maxDist, hitLayerMask))
{
    if (Utilities.IsValid(hit.gameObject))
    {
        // 进一步业务校验
    }
}
```

### 协作层

1. **设计阶段**确定 Layer 用途，文档化到 World README
2. **避免使用** Layer 6/7/21（reserved）和 Layer 19/20（VRChat 内部）
3. **Sticker 防御** 默认使用 Layer 8 (`Interactive`)
4. **Pickup 专用** Layer 13/14 处理拾取物品碰撞
5. **VR 测试** 必做——Desktop 通过不代表 VR 通过

### 文档层

- 任何 Layer 用途变更需同步到 World Design Spec
- Layer 22-30 自定义时建议命名包含 `User_` 前缀避免混淆

---

## 引用

- **源页面**: https://creators.vrchat.com/worlds/layers
- **Unity 官方 Layer 文档**: https://docs.unity3d.com/2022.3/Documentation/Manual/Layers.html
- **Unity 官方 Layer 碰撞**: https://docs.unity3d.com/2022.3/Documentation/Manual/LayerBasedCollision.html
- **Unity 官方 Raycast**: https://docs.unity3d.com/2022.3/Documentation/ScriptReference/Physics.Raycast.html
- **VRChat+**: https://hello.vrchat.com/vrchatplus
- **相关页面**: https://creators.vrchat.com/worlds/items (Layer 3 Item 行为)
- **相关页面**: https://creators.vrchat.com/worlds/components#world-shape-limits (Physics 形状限制)
