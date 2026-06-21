---
title: Screen Canvas
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - udonsharp
  - reference

aliases:
  - "Screen Canvas"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Screen Canvas

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/screen-canvas)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/screen-canvas/
> 文档版本: Last updated Oct 30, 2024
> SDK: 3.0+ (VRC_UIShape, IsUserInVR, TeleportTo)

## Example Central Package

> ✅ **需要 Example Central Package**
> 通过 `VRChat SDK → 🏠 Example Central` 导入
> 包含 ScreenCanvas Prefab、HideInVR Graph、TeleportToTarget Graph

### Example World
- **World ID**: `wrld_1448021c-b126-4cb9-ac92-1ab660884b02`
- **URL**: https://vrchat.com/home/world/wrld_1448021c-b126-4cb9-ac92-1ab660884b02

---

## 概述

演示如何为 **2D 屏幕用户**(Mobile、Desktop)创建 **Screen-Space UI Canvas**。
- 屏幕用户看到 UI 边框 + 按钮
- VR 用户看不到(避免"贴脸"问题)
- 按钮触发玩家传送到新位置

**典型场景**: 移动端用户的菜单、操作提示、传送点。

---

## 关键 Udon API

| API | 角色 | 说明 |
|-----|------|------|
| `VRCPlayerApi.IsUserInVR()` | 检测用户是否在 VR | 屏幕用户返回 false |
| `VRCPlayerApi.TeleportTo(Vector3, Quaternion)` | 传送玩家 | 每个玩家独立 |
| `Transform.GetPositionAndRotation()` | 获取目标位置和旋转 | 用于 TeleportTo |
| `GameObject.SetActive(bool)` | 启用/禁用对象 | 用于 HideInVR |
| `VRC_UIShape` (SDK Prefab) | Screen-Space UI 组件 | 屏幕用户专属 UI 容器 |

---

## 核心架构

### 两个 Graph 程序

| 程序 | 角色 | 触发 |
|------|------|------|
| `HideInVR` | 屏幕用户专属 UI 显隐控制 | `Start()` |
| `TeleportToTarget` | 玩家点击按钮 → 传送到目标 | UI Button `_Trigger` |

### 屏幕用户行为

```
进入世界 (Mobile / Desktop)
  ↓
显示屏幕 UI(屏幕边缘粗白边 + "Teleport" 按钮)
  ↓
点击按钮 → TeleportTo
  ↓
到达新位置,显示 "Second Location / Here you are!"
```

### VR 用户行为

```
进入世界 (VR)
  ↓
ScreenCanvas 整体 SetActive(false)
  ↓
不显示屏幕 UI(避免贴脸遮挡)
```

---

## HideInVR 程序详解

```csharp
public class HideInVR : UdonSharpBehaviour
{
    private void Start()
    {
        VRCPlayerApi localPlayer = Networking.LocalPlayer;
        if (localPlayer.IsUserInVR())
        {
            // VR 用户:禁用 ScreenCanvas
            gameObject.SetActive(false);
        }
        // 屏幕用户:保持激活
    }
}
```

### 关键设计

| 决策 | 原因 |
|------|------|
| 在 `Start()` 检查 | 每玩家进入时独立判断 |
| **不是** `[NetworkCallable]` | 不需要同步,本地决策 |
| `IsUserInVR()` 在客户端 | 平台检测,网络无意义 |

---

## TeleportToTarget 程序详解

```csharp
public class TeleportToTarget : UdonSharpBehaviour
{
    public Transform target;  // 公开 Inspector 字段

    public void _Trigger()
    {
        Vector3 pos = target.position;
        Quaternion rot = target.rotation;
        Networking.LocalPlayer.TeleportTo(pos, rot);
    }
}
```

### UI Button 接线

```
Button (UI)
  ↓
OnClick() → UdonBehaviour.SendCustomEvent("_Trigger")
```

或通过 Udon Graph 直接连接。

### Transform 子物体细节

> 文档原话: "Note that the transform has a child Sprite to show the spot on the ground where the player will be teleported, as a convenience."

- `TeleportTarget` 有子 Sprite 显示目标点
- Sprite 需要**独立旋转**(可能是地面标记)
- 通过父子结构分离旋转: Sprite 旋转 vs 玩家传送旋转

---

## VRC_UIShape 与 Screen 模式

> 💡 **VRC_UIShape 是 SDK Prefab**,在 `SDK > Prefabs` 中可找到
> 它是为 2D 屏幕用户设计的 UI 系统
> 与 World Space Canvas 不同: 自动跟随屏幕而非固定在世界空间

### 详细使用方式
- 在场景中放置 VRC_UIShape Prefab
- 添加子 UI(Button, Text, Image 等)
- 这些 UI **只对 2D 屏幕用户可见**
- 配合 `HideInVR` 程序避免 VR 误显

---

## 关键设计模式

### 1. 平台检测 (IsUserInVR)

```csharp
if (Networking.LocalPlayer.IsUserInVR()) { ... }
```

- **常见误区**: 在 `Update` 中调用 — 浪费
- **正确做法**: `Start()` 调用一次即可(平台不会在运行中切换)
- **缓存**: 必要时缓存到本地变量(本例不需要)

### 2. 传送点的 Sprite 子物体
- Transform 提供位置 + 旋转给玩家
- 子 Sprite 独立旋转(可能是水平躺平的标记)
- 这种"父子结构"是 Unity 常用模式

### 3. EditorOnly 工具: VRCButtonLayout

> 文档原话: "The `VRCButtonLayout` object is a helpful tool for showing where different buttons in the VRChat Mobile UI will appear so you can try to work around them. It is tagged `EditorOnly` and will not be uploaded with your world."

- 标记为 `EditorOnly` → 不会上传到 VRChat
- 仅在 Unity Editor 中显示 VRChat 移动端 UI 按钮的位置
- 便于设计时避免 UI 被系统按钮遮挡

---

## 已知问题(文档原话)

> ⚠️ "In ClientSim, the collider generated for the ScreenCanvas is always placed at (0,0,0) and covers the whole size of the canvas. In the VRChat Client, the existing collider is used and appears in the proper position."

**说明**:
- **ClientSim**: 模拟器的 Collider 总是 (0,0,0),尺寸覆盖整个 Canvas
- **VRChat Client**: 使用实际 Collider,在正确位置
- **对策**: 在 ClientSim 场景中调整初始 Spawn 位置,让用户在 Collider 前

这是模拟器与真实客户端的差异,属于 ClientSim 已知限制。

---

## 二次开发建议

- **多个 Screen UI**: 为不同平台(Android vs iOS vs Desktop)准备不同 UI
- **多按钮组**: 用 Trigger 区域动态启用不同 Screen UI
- **VRC_UIShape 组合**: 菜单 + 提示 + 操作 UI 组合

---

## 与知识库互补

- **VRCPlayerApi 完整 API**: `memory/api/player-api.md`(待建)
- **IsUserInVR 详细行为**: `memory/api/player-api.md`(待建)
- **VRC_UIShape 详细使用**: `memory/platform/mobile-ui-optimization.md` ⭐
- **TeleportTo API**: `memory/api/events-reference.md` 中 Player Positions 章节
- **ClientSim 已知限制**: `memory/sources/clientsim.md` ⭐
- **EditorOnly Tag**: `memory/unity/editor-tags.md`(待建)

## 相关 Udon 文档链接

- [VRCPlayerApi.IsUserInVR](https://udonsharp.docs.vrchat.com/vrchat-api/#vrcplayerapi)
- [TeleportTo API](/worlds/udon/players/player-positions/#teleportto)
- [VRC_UIShape 完整文档](/worlds/components/vrc-ui-shape) (待链接验证)
- [ClientSim 模拟器](/worlds/clientsim)
