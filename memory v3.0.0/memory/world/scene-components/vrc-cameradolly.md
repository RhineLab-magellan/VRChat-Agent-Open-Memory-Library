---
title: "VRC Camera Dolly"
category: world
subcategory: scene-components
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - video
  - udonsharp
aliases:
  - "VRC Camera Dolly"
  - vrc-cameradolly
related:
  - vrc-scenedescriptor.md
  - textmeshpro.md
  - vrc-avatarpedestal.md
  - vrc-enablepersistence.md
  - vrc-portalmarker.md
---
# VRC Camera Dolly

> 相机轨道动画系统(用于 VRChat 截图/视频)
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_cameradolly/
> 官方类名: `VRC_CameraDollyAnimation`, `VRC_CameraDollyPath`, `VRC_CameraDollyPathPoint`
> 最后更新: 2026-06-15
> 最新更新日期: 2025-12-12

---

## 概述

VRC Camera Dolly 允许将相机轨道动画应用于 VRChat 用户的相机系统(用于截图、视频录制等)。

> **FACT** (来自官方文档): 系统由 3 个组件组成:
> - `VRC Camera Dolly Animation`: 顶层组件,代表整个动画
> - `VRC Camera Dolly Path`: 单条动画路径
> - `VRC Camera Dolly Path Point`: 路径上的一个关键帧

---

## 层级结构(必须严格嵌套)

```
Animation (VRC_CameraDollyAnimation)
├── Path 1 (VRC_CameraDollyPath)
│   ├── Point 1 (VRC_CameraDollyPathPoint)
│   └── Point 2 (VRC_CameraDollyPathPoint)
└── Path 2 (VRC_CameraDollyPath)
    ├── Point 1 (VRC_CameraDollyPathPoint)
    ├── Point 2 (VRC_CameraDollyPathPoint)
    ├── Point 3 (VRC_CameraDollyPathPoint)
    └── Point 4 (VRC_CameraDollyPathPoint)
```

---

## VRC Camera Dolly Animation 参数

| 参数 | 说明 |
|------|------|
| **Is Relative To Player** | 动画基于世界原点还是玩家位置 |
| **Is Speed Based** | 时间驱动(用 Duration)还是速度驱动(用飞行速度值) |
| **Is Using Look At Me** | 是否使用 Look-At-Me 偏移 |
| **Is Using Greenscreen** | 是否使用绿屏 HSL 值 |
| **Is Using Multi Stream** | 是否为多流动画(直播用) |
| **Path Type** | 所有动画路径的插值方式 |
| **Loop Type** | 动画循环方式(None / Loop / PingPong) |
| **Capture Type** | 动画捕获方式(Screenshot / Video / Photo Booth) |
| **Focus Mode** | 对焦模式(Auto / Manual / Semi-Auto) |
| **Anchor Mode** | 锚点模式(World / Player / Custom) |
| **Paths** | 此动画包含的路径列表 |

---

## VRC Camera Dolly Path 参数

| 参数 | 说明 |
|------|------|
| **Points** | 此路径包含的关键帧列表 |

---

## VRC Camera Dolly Path Point 参数

| 参数 | 说明 |
|------|------|
| **Zoom** | 关键帧的缩放值 |
| **Duration** | 关键帧的持续时间(时间驱动模式) |
| **Speed** | 关键帧的速度值(速度驱动模式) |
| **Focal Distance** | 关键帧的对焦距离(手动对焦) |
| **Aperture** | 关键帧的光圈(手动/半自动对焦) |
| **Hue** | 关键帧的绿屏色相(绿屏模式) |
| **Saturation** | 关键帧的绿屏饱和度(绿屏模式) |
| **Lightness** | 关键帧的绿屏明度(绿屏模式) |
| **Look At Me X Offset** | 关键帧的 Look-At-Me 水平偏移 |
| **Look At Me Y Offset** | 关键帧的 Look-At-Me 垂直偏移 |

---

## 使用步骤

> **FACT** (来自官方文档): 正确使用 Camera Dolly 必须遵循 5 步:

1. **创建 Animation 节点**: 给任意 GameObject 添加 `VRC_CameraDollyAnimation` 组件并配置参数
2. **添加 Path**: 在上述 GameObject 的子节点添加 `VRC_CameraDollyPath`
3. **添加 Point**: 给一组 GameObject 各添加 `VRC_CameraDollyPathPoint` 组件,定义关键帧参数
4. **收集路径**: 选中顶层对象,点击 **`Collect Paths & Points`** 按钮
   > ⚠️ **必须** 每次层级结构更新后都重新点击
5. **应用动画**: 调用 `VRCCameraDollyAnimation.Import()` 将动画应用到本地玩家的 VRChat 相机

> **FACT**: Editor Gizmos 会可视化动画路径。但 **ClientSim 不支持 Camera Dolly 预览**,需要使用 `Build and Test` 真实测试。

---

## U# 引用方式

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class CameraDollyController : UdonSharpBehaviour
{
    [SerializeField] private VRC_CameraDollyAnimation dollyAnimation;
    
    public override void Interact()
    {
        // 将动画应用到本地玩家的 VRChat 用户相机
        dollyAnimation.Import();
    }
    
    public void StartRecording()
    {
        // 触发 Import 后,玩家可使用 VRChat 内置截图/录像
        dollyAnimation.Import();
    }
}
```

---

## Path Type 插值方式

`Path Type` 控制所有路径的插值方式(参考 Unity AnimationCurve 概念):
- **Linear**: 线性插值
- **Catmull-Rom**: 平滑曲线
- **Bezier**: 贝塞尔曲线(需手动控制点)

---

## Anchor Mode 锚点模式

| 模式 | 说明 |
|------|------|
| **World** | 动画基于世界坐标(0,0,0) |
| **Player** | 动画基于玩家当前位置(适用于跟随相机) |
| **Custom** | 自定义锚点(自定义 Transform) |

---

## 典型应用场景

### 1. 商业片头 / 宣传动画

World 加载时自动播放一段相机轨道动画,展示 World 全景。

### 2. 电影感环绕

为某物体添加 360° 环绕的相机动画,玩家可以触发播放。

### 3. 玩家动作重放

记录玩家动作,然后用 Camera Dolly 重新展示(配合 Timeline)。

### 4. 绿屏直播间

设置 `Is Using Greenscreen`,制作直播用的虚拟背景。

---

## 性能考虑

- **多个 Camera Dolly**: 每个动画独立,不会互相影响
- **Path Point 数量**: 大量 Point 会增加 Inspector 配置复杂度,但运行时性能影响小
- **Loop Type**: PingPong 比 Loop 复杂,但 VRChat 已优化
- **路径插值**: Bezier 最昂贵,Linear 最便宜

---

## 平台兼容性

- **PC**: 完全支持
- **Quest**: 完全支持(因 Camera Dolly 是 VRChat 客户端层面处理)
- **Mobile**: 不适用(World 仅支持 PC/Quest)

---

## 常见陷阱

1. **忘记点击 `Collect Paths & Points`**: 修改层级后未重新收集,动画不更新
2. **Path 与 Animation 层级错乱**: 必须 Animation > Path > Point,否则 SDK 报错
3. **Duration 与 Speed 模式混淆**: 时间驱动用 Duration,速度驱动用 Speed
4. **绿屏 HSL 配置错误**: Hue 是 0-360 度,不是 0-255
5. **Loop Type 误用**: 设置 Loop 但希望单向播放

---

## 与其他组件的依赖

- **VRChat 相机系统**: 强依赖,无 VRChat 相机时无意义
- **VRC_UIShape**: 可与 UI 按钮配合,提供 "播放动画" 按钮
- **VRCStation**: 可在玩家坐下时自动播放相机动画
- **VRC_SceneDescriptor**: 加载 World 时可在 OnSceneWasLoaded 触发

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_cameradolly/
- 关联组件: [VRC_SceneDescriptor](./vrc-scenedescriptor.md)
- 关联模式: `patterns/dolly-import-event.md` (后续任务)
