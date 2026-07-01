---
title: "API: VRChat Dynamics for Worlds (SDK 3.10.0+)"
category: api
knowledge_level: core
status: active
source: "VRChat 官方文档 + VRChat Agent Skills 模板(参考工程) + 2026.2.1 Release Notes"
source_type: official
version: 1.1
last_review: 2026-06-30
confidence: High
tags:
  - api
  - physbone
  - contact
  - constraint
  - event
aliases:
  - "Dynamics API"
  - 动态系统
  - "PhysBone/Contact API"
  - Dynamics
related:
  - api-checker.md
  - audio.md
  - events-reference.md
  - not-exposed.md
  - persistence.md
---
# API: VRChat Dynamics for Worlds (SDK 3.10.0+)

> SDK Version: 3.10.0+
> Last Verified: 2026-06-04

---

## Overview

SDK 3.10.0 引入了 World-side Dynamics：PhysBones、Contacts、VRC Constraints 现在可以在世界对象上使用。

## Contact Events

### OnContactEnter / OnContactExit / OnContactStay
```csharp
using VRC.Dynamics;

public override void OnContactEnter(ContactEnterInfo info) {
    if (info.isAvatar) {
        Debug.Log($"Touched by avatar: {info.player?.displayName}");
    }
}
```

### ContactEnterInfo
- `info.isAvatar` — bool，是否来自 Avatar
- `info.player` — VRCPlayerApi（可能为 null）
- 需要 `VRCContactReceiver` 组件

---

## PhysBone Events

### OnPhysBoneGrabbed / OnPhysBoneReleased
```csharp
public override void OnPhysBoneGrabbed(PhysBoneGrabbedInfo physBoneInfo) {
    // Called when the PhysBone is grabbed by a player.
    Debug.Log($"PhysBone grabbed by: {physBoneInfo.player?.displayName}");
}
```

### PhysBoneGrabbedInfo
- `physBoneInfo.player` — VRCPlayerApi（可能为 null）

---

## VRC Constraints

World-side constraints 类似 Unity Joint 系统，但在 VRChat 的约束框架下运行。

---

## SDK Version Requirement

- ⚠️ `OnPhysBoneGrabbed`、`OnContactEnter` 等在 SDK < 3.10.0 **编译通过但运行时静默忽略**
- 始终检查 `#if UDONSHARP` 或 SDK 版本条件

---

## SDK Version Feature Timeline

| SDK | Key Features |
|---|---|
| 3.7.1 | StringBuilder, Regex, System.Random |
| 3.7.4 | **Persistence API** (PlayerData / PlayerObject) |
| 3.7.6 | Multi-platform Build & Publish |
| 3.8.0 | PhysBone dependency sorting, Drone API |
| 3.8.1 | **`[NetworkCallable]`** (parameterized network events) |
| 3.9.0 | Camera Dolly API, Auto Hold pickup |
| 3.10.0 | **Dynamics for Worlds** (PhysBones, Contacts, VRC Constraints) |
| 3.10.1 | Bug fixes, stability improvements |
| 3.10.2 | EventTiming.PostLateUpdate/FixedUpdate, PhysBones fixes |
| 3.10.3 | VRCPlayerApi.isVRCPlus, VRCRaycast (avatar), Mirror fix |

> SDK < 3.9.0 已于 2025-12-02 弃用。新 world 上传需要 3.9.0+。

---

## VRCRaycast (Avatar 端)

> **🔴 注意**:VRCRaycast 是 **Avatar 组件**,**不属于 World Dynamics**。但因同属 SDK 3.10.3 引入,在此处简要说明。
>
> **完整文档**:`memory/avatar/vrcraycast.md`

### 速查

- 作用:Avatar 骨骼向下投射 raycast,结果写入 Animator 参数(默认 `IsRaycastHit`)
- 用途:踩地检测、遮挡检测、Avatar 端世界交互
- 文档:https://creators.vrchat.com/avatars/avatar-components/raycast

### 2026.2.1 关键更新

| 改进 | 详情 |
|------|------|
| **自动剥离** | 玩家本地屏蔽 Poor/Very Poor 时,从其他玩家 Avatar 上剥离 VRCRaycast |
| **无实时光照修复** | Animator 移动 raycast 时参数正确返回 |
| **第一人称对称** | 头部 raycast 在头部隐藏**之前**应用 |

详见 `memory/avatar/vrcraycast.md` 完整文档。
