# API: VRChat Dynamics for Worlds (SDK 3.10.0+)

> Type: API
> Source: VRChat 官方文档 + VRChat Agent Skills 模板(参考工程)
> Confidence: High
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

### OnPhysBoneGrab / OnPhysBoneRelease
```csharp
public override void OnPhysBoneGrab(PhysBoneGrabInfo info) {
    Debug.Log($"PhysBone grabbed by: {info.player?.displayName}");
}
```

### PhysBoneGrabInfo
- `info.player` — VRCPlayerApi（可能为 null）

---

## VRC Constraints

World-side constraints 类似 Unity Joint 系统，但在 VRChat 的约束框架下运行。

---

## SDK Version Requirement

- ⚠️ `OnPhysBoneGrab`、`OnContactEnter` 等在 SDK < 3.10.0 **编译通过但运行时静默忽略**
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
