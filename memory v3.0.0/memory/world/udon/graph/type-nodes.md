---
title: "Type Nodes | 类型引用节点"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - mirror
  - reflection
  - avatar
aliases:
  - "Type Nodes | 类型引用节点"
  - type-nodes
related:
  - index.md
  - event-nodes.md
  - graph-elements.md
  - searching-for-nodes.md
  - special-nodes.md
  - "api/exposed-types.md"
  - "api/not-exposed.md"
---
# Type Nodes | 类型引用节点

> 来源: https://creators.vrchat.com/worlds/udon/graph/type-nodes/

> ⚠️ **重定向说明**: `https://creators.vrchat.com/worlds/udon/graph/type-nodes`/ 返回 **301 Moved Permanently**。
> 实际位置: `https://creators.vrchat.com/worlds/udon/graph/type-nodes/`(带尾部斜杠/)。

这些节点用于**获取特定类型的引用**。每个节点都有**一个对应类型的输出**。

> 📌 官方文档**只列出 VRChat 类型**。Unity 类型请参考 Unity 官方文档。

---

## 类型引用模式

对于每种支持的类型,通常提供 3 种节点变体:

| 节点后缀 | 含义 | 用途 |
|---------|------|------|
| `<TypeName>` | 类型实例 | 直接引用一个对象 |
| `<TypeName>[]` | 数组类型 | 处理对象集合 |
| `<TypeName>Ref` | 引用类型 | 用于输入端口的"引用"位置(可替换) |

> **【推断】** `Ref` 变体用于**需要"对象引用占位符"的场景** — 当一个端口期望某种类型但允许通过 Inspector 注入不同实例时使用。具体行为以 SDK 实际生成为准。

---

## VRChat SDK 组件类型

### 1. VRCAvatarPedestal

| 节点 | 类型定义 |
|------|---------|
| `VRCSDK3ComponentsVRCAvatarPedestal` | `VRC.SDK3.Components.VRCAvatarPedestal` |
| `VRCSDK3ComponentsVRCAvatarPedestal[]` | `VRC.SDK3.Components.VRCAvatarPedestal[]` |
| `VRCSDK3ComponentsVRCAvatarPedestalRef` | `VRC.SDK3.Components.VRCAvatarPedestal` |

**用途**: Avatar 切换台(可触发 Avatar 切换的实体)

---

### 2. VRCMirrorReflection

| 节点 | 类型定义 |
|------|---------|
| `VRCSDK3ComponentsVRCMirrorReflection` | `VRC.SDK3.Components.VRCMirrorReflection` |
| `VRCSDK3ComponentsVRCMirrorReflection[]` | `VRC.SDK3.Components.VRCMirrorReflection[]` |
| `VRCSDK3ComponentsVRCMirrorReflectionRef` | `VRC.SDK3.Components.VRCMirrorReflection` |

**用途**: 镜面反射组件

---

### 3. VRCPickup

| 节点 | 类型定义 |
|------|---------|
| `VRCSDK3ComponentsVRCPickup` | `VRC.SDK3.Components.VRCPickup` |
| `VRCSDK3ComponentsVRCPickup[]` | `VRC.SDK3.Components.VRCPickup[]` |
| `VRCSDK3ComponentsVRCPickupRef` | `VRC.SDK3.Components.VRCPickup` |

**用途**: V3 拾取组件(Sync Pickup)

---

### 4. VRCPortalMarker

| 节点 | 类型定义 |
|------|---------|
| `VRCSDK3ComponentsVRCPortalMarker` | `VRC.SDK3.Components.VRCPortalMarker` |
| `VRCSDK3ComponentsVRCPortalMarker[]` | `VRC.SDK3.Components.VRCPortalMarker[]` |
| `VRCSDK3ComponentsVRCPortalMarkerRef` | `VRC.SDK3.Components.VRCPortalMarker` |

**用途**: Portal 标记(跨世界传送)

---

### 5. VRCStation

| 节点 | 类型定义 |
|------|---------|
| `VRCSDK3ComponentsVRCStation` | `VRC.SDK3.Components.VRCStation` |
| `VRCSDK3ComponentsVRCStation[]` | `VRC.SDK3.Components.VRCStation[]` |
| `VRCSDK3ComponentsVRCStationRef` | `VRC.SDK3.Components.VRCStation` |

**用途**: Station(玩家可以"坐"上去的固定位置)

---

## VRChat SDK Base 类型

### 6. InputManager

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseInputManager` | `VRC.SDKBase.InputManager` |
| `VRCSDKBaseInputManager[]` | `VRC.SDKBase.InputManager[]` |
| `VRCSDKBaseInputManagerRef` | `VRC.SDKBase.InputManager` |

---

### 7. IVRC_Destructible

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseIVRCDestructible` | `VRC.SDKBase.IVRC_Destructible` |

---

### 8. RPC.Destination

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseRPCDestination` | `VRC.SDKBase.RPC+Destination` |

---

### 9. VRC_EventDispatcher

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseVRCEventDispatcher` | `VRC.SDKBase.VRC_EventDispatcher` |

---

### 10. VRC_EventHandler

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseVRCEventHandler` | `VRC.SDKBase.VRC_EventHandler` |
| `VRCSDKBaseVRCEventHandlerVrcBroadcastType` | `VRC.SDKBase.VRC_EventHandler+VrcBroadcastType` |

---

### 11. VRC_Pickup(旧版)

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseVRCPickup` | `VRC.SDKBase.VRC_Pickup` |
| `VRCSDKBaseVRCPickupPickupHand` | `VRC.SDKBase.VRC_Pickup+PickupHand` |

**用途**: 旧版拾取组件(建议新项目使用 `VRCPickup`)

---

### 12. VRC_SceneDescriptor.SpawnOrientation

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseVRCSceneDescriptorSpawnOrientation` | `VRC.SDKBase.VRC_SceneDescriptor+SpawnOrientation` |

---

### 13. VRCInputMethod ⭐

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseVRCInputMethod` | `VRC.SDKBase.VRCInputMethod`(枚举) |

**枚举值**:

| Index | Name | 说明 |
|-------|------|------|
| 0 | `Keyboard` | 键盘 |
| 1 | `Mouse` | 鼠标 |
| 2 | `Controller` | 通用手柄 |
| 3 | `Gaze` | 注视(老旧) |
| 5 | `Vive` | **Vive 控制器(通过 SteamVR)** |
| 6 | `Oculus` | Oculus |
| 7 | `ViveXR` | **Vive XR Elite Controller(通过 OpenXR)** |
| 10 | `Index` | Valve Index |
| 11 | `HPMotionController` | HP Motion Controller |
| 12 | `Osc` | OSC(外部输入) |
| 13 | `QuestHands` | Quest 手部追踪 |
| 14 | `Generic` | 通用 |
| 15 | `Touch` | Touch |
| 16 | `OpenXRGeneric` | OpenXR 通用 |
| 17 | `Pico` | Pico |
| 18 | `SteamVR2` | SteamVR 2.0 |

> ⚠️ **Vive 命名歧义**:
> - `VRCInputMethod.ViveXr` = Vive XR Elite Controller(**OpenXR** 模式)
> - `VRCInputMethod.Vive` = Vive 控制器(**SteamVR** 模式)
>
> 两者**不是同一设备**,识别时务必明确。

---

### 14. VRCInputSetting

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseVRCInputSetting` | `VRC.SDKBase.VRCInputSetting` |

---

### 15. VRCPlayerApi ⭐(核心)

| 节点 | 类型定义 |
|------|---------|
| `VRCSDKBaseVRCPlayerApi` | `VRC.SDKBase.VRCPlayerApi` |
| `VRCSDKBaseVRCPlayerApi[]` | `VRC.SDKBase.VRCPlayerApi[]` |
| `VRCSDKBaseVRCPlayerApiRef` | `VRC.SDKBase.VRCPlayerApi` |
| `VRCSDKBaseVRCPlayerApiTrackingData` | `VRC.SDKBase.VRCPlayerApi+TrackingData` |
| `VRCSDKBaseVRCPlayerApiTrackingData[]` | `VRC.SDKBase.VRCPlayerApi+TrackingData[]` |
| `VRCSDKBaseVRCPlayerApiTrackingDataRef` | `VRC.SDKBase.VRCPlayerApi+TrackingData` |
| `VRCSDKBaseVRCPlayerApiTrackingDataType` | `VRC.SDKBase.VRCPlayerApi+TrackingDataType` |

**用途**: 玩家 API,几乎是所有 Player 事件的**核心输出类型**。
- `VRCPlayerApi` 包含 `isSuspended` 等状态属性
- `TrackingData` 包含追踪数据(Head/RightHand/LeftHand 等)
- `TrackingDataType` 枚举选择追踪点

> 详细 API 见 `../../../api/exposed-types.md`(知识库)

---

## 与已有知识库关系

| 主题 | 相关文档 |
|------|---------|
| **VRCPlayerApi 完整 API** | `../../api/exposed-types.md` |
| **未暴露 API 黑名单** | `../../api/not-exposed.md` |
| **Networking 完整规范** | `../../api/networking.md` |
| **MIDI 事件** | 本知识库未收录,【未确认】是否在 MIDI 组件页 |
| **Ownership 事件** | 本知识库未收录,【未确认】是否在 Ownership 组件页 |

> **【风险】** 本文件仅整理了**官方文档当前列出**的 Type 节点。**Node Graph 中实际可见的类型可能更多**(尤其是 Unity 基础类型),需要 Graph 内搜索补充。

---

## 任务提示词对照

| 任务要求内容 | 实际文档状态 |
|------------|------------|
| **Type 转换节点** | ❌ 官方文档**未单独列出**显式 Cast 节点 — 类型转换在 Udon Graph 中通过**端口连接自动完成**(Noodle 颜色渐变表示隐式转换) |
| **Cast 节点(隐式/显式)** | ❌ 同上,**无独立 Cast 节点** — 转换由 Graph 系统处理 |
| **数组类型** | ✅ 已收录 — `<TypeName>[]` 变体 |
| **Type 引用节点** | ✅ 已收录 — 完整列表 |

> **【推断】** Udon Graph 设计理念是"节点类型化" — 端口类型不匹配时**无法连接**,所以不需要显式 Cast 节点。**Unity 类型**(int/float/string/Vector3/...)的 Cast 由 Noodle 系统隐式处理。

---

## 相关知识库

- [`index.md`](./index.md) — Udon Node Graph 主页
- [`event-nodes.md`](./event-nodes.md) — Event 节点
- [`graph-elements.md`](./graph-elements.md) — Graph 元素
- [`searching-for-nodes.md`](./searching-for-nodes.md) — 节点搜索
- [`special-nodes.md`](./special-nodes.md) — 特殊节点
- `../../api/exposed-types.md` — 已暴露类型详细清单
- `../../api/not-exposed.md` — 未暴露 API 黑名单
