---
title: "Udon Basics"
category: world
subcategory: examples
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon-graph
  - udonsharp
aliases:
  - "Udon Basics"
  - udon
related:
  - README.md
  - detect-controller-collide.md
  - image-loading.md
  - mute-others.md
  - player-join-zones.md
---
# Udon Basics

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/udon)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/udon/
> 文档版本: Last updated Oct 30, 2024
> SDK: Udon / UdonSharp 通用

## Example Central Package

> ❌ **不需要 Example Central Package**
> 本页是 4 个独立的 Udon 基础模式参考,不是完整的 UnityPackage
> 这 4 个模式可作为学习起点直接复制使用

---

## 概述

本页是 VRChat 官方提供的 **Udon 基础代码片段集合**,覆盖 4 个最常见的入门场景。每个模式都同时提供 Udon Graph 和 UdonSharp 两种实现。是学习 Udon 开发的标准起点。

---

## 模式 1: Rotating Cube(旋转立方体)

**用途**: 演示 Udon 生命周期中的 `Update()` 事件,以及最基础的 `transform` 操作。

**关键 Udon API**:
- `UdonSharpBehaviour.Update()` - 每帧调用
- `transform.Rotate(axis, angle)` - 围绕轴旋转

**UdonSharp 代码**:
```csharp
using UnityEngine;
using VRC.SDKBase;

public class RotatingCubeBehaviour : UdonSharpBehaviour
{
    private void Update()
    {
        transform.Rotate(Vector3.up, 90f * Time.deltaTime);
    }
}
```

**可复用要点**:
- `Time.deltaTime` 确保旋转速率与帧率无关
- `Vector3.up` 等同于 `Vector3(0, 1, 0)`

---

## 模式 2: Interact(玩家交互)

**用途**: 演示 `Interact()` 事件,玩家点击物体触发回调。

**关键 Udon API**:
- `public override void Interact()` - 玩家点击触发
- `gameObject.SetActive(bool)` - 启用/禁用游戏对象

**UdonSharp 代码**:
```csharp
using UnityEngine;
using VRC.SDKBase;

public class ClickMe : UdonSharpBehaviour
{
    public override void Interact()
    {
        gameObject.SetActive(false);
    }
}
```

**前置条件(必读)**:
> ⚠️ GameObject **必须** 有 Collider 组件,玩家才能与之交互

**可复用要点**:
- 适合"消息提示"、"门消失"、"按钮按下"等一次性触发场景
- Collider 是 Interact 的物理基础,缺失则完全无响应

---

## 模式 3: Teleport Player(传送玩家)

**用途**: 演示 `TeleportTo` API,玩家被传送到指定 Transform 的位置和旋转。

**关键 Udon API**:
- `Networking.LocalPlayer.TeleportTo(Vector3 pos, Quaternion rot)`
- `public Transform targetPosition` - Inspector 公开的目标 Transform

**UdonSharp 代码**:
```csharp
using UnityEngine;
using VRC.SDKBase;

public class TeleportPlayer : UdonSharpBehaviour
{
    public Transform targetPosition;

    public override void Interact()
    {
        Networking.LocalPlayer.TeleportTo(
            targetPosition.position,
            targetPosition.rotation);
    }
}
```

**关键注意**:
- `targetPosition` 必须声明为 `public` 才能在 Inspector 中赋值
- 目标 Transform **也必须** 有 Collider 组件
- 传送只影响本地玩家,不需要任何同步(每玩家独立)

**可复用要点**:
- 这是"非同步逻辑"的典型例子 — 传送是本地行为,无需 Ownership
- 适合门、检查点、过场动画切换

---

## 模式 4: Sending Events(发送自定义事件)

**用途**: 演示 UdonBehaviour 之间通过**变量访问 + 自定义事件**通信。

**关键 Udon API**:
- `SendCustomNetworkEvent(NetworkEventTarget, string methodName)` - 网络事件
- 直接访问其他 UdonBehaviour 的 public 字段/方法
- `NetworkEventTarget.All` / `NetworkEventTarget.Owner`

**UdonSharp 代码**:
```csharp
using UdonSharp;
using UnityEngine;
using VRC.Udon.Common.Interfaces;

public class SomeExample : UdonSharpBehaviour
{
    [SerializeField] private SomeOtherExample otherBehaviour;

    void Start()
    {
        if (otherBehaviour.somePublicBoolean)
        {
            otherBehaviour.SomeCustomEvent();
        }
    }

    public override void Interact()
    {
        DoStuff();
    }

    private void DoStuff()
    {
        SendCustomNetworkEvent(NetworkEventTarget.All, nameof(DoNetworkEventStuff));
    }

    public void DoNetworkEventStuff()
    {
        otherBehaviour.somePublicBoolean = false;
        otherBehaviour.SomeCustomEvent();
        otherBehaviour.SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(DoOwnerStuff));
    }
}
```

**可复用要点**:
- 变量通信: `otherBehaviour.somePublicBoolean` 直接读写
- 本地事件: `otherBehaviour.SomeCustomEvent()` 同步调用
- 网络事件: `SendCustomNetworkEvent` 跨玩家调用
- `nameof(DoNetworkEventStuff)` 避免字符串硬编码

**通信模式总结**:

| 模式 | 调用语法 | 作用范围 |
|------|----------|----------|
| 直接访问变量 | `other.field` | 本地 |
| 本地事件 | `other.Method()` | 本地同步 |
| 网络事件 | `other.SendCustomNetworkEvent(target, "Method")` | 跨玩家 |

---

## 与知识库互补

- **Udon 事件完整参考**: `memory/api/events-reference.md`
- **Udon 编译管线**: `memory/world/udon/udonsharp/compilation.md`
- **UdonSharp 运行时系统**: `memory/api/udonsharp-runtime.md`
- **带参网络同步**: `memory/api/networking.md` 中的 [NetworkCallable]

## 相关 Udon 文档链接

- [Udon Graph Event Nodes](/worlds/udon/graph/event-nodes/#interact)
- [Player Positions: TeleportTo](/worlds/udon/players/player-positions/#teleportto)
