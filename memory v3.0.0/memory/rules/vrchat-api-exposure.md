---
title: "Rule Set: VRChat API Exposure"
category: rules
knowledge_level: applied
status: active
source: "VRChat 官方文档 + UdonSharp 文档"
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - rules
  - rules
  - animator
  - networking
  - audio
  - pickup
aliases:
  - "Rule Set： VRChat API Exposure"
  - "Rule Set: VRChat API Exposure"
related:
  - performance-rules.md
  - networking-rules.md
  - "../patterns/slot-parameter-passing.md"
  - multi-vm-rules.md
  - udon-vm-architecture.md
---
# Rule Set: VRChat API Exposure


---

## RULE-API-01: Verify Before Use

### Rule
任何 API 使用前必须判断：
1. 是否被 VRChat Udon 暴露
2. 是否能在 UdonSharp 中编译
3. 是否适合在 Udon VM 热路径中调用
4. 是否会带来网络或多 VM 协作成本

### Reason
Unity 提供大量 API，但只有一小部分被 VRChat 暴露给 Udon。使用未暴露 API 会导致编译错误或运行时无效果。

---

## RULE-API-02: Known Exposed API Categories

### 确认暴露
- `UdonSharpBehaviour` 基类
- `[UdonSynced]`, `[FieldChangeCallback]`
- `Networking.SetOwner()`, `Networking.LocalPlayer`, `Networking.GetOwner()`
- `RequestSerialization()`, `OnDeserialization()`
- `SendCustomEvent()`, `SendCustomNetworkEvent()`, `SendCustomEventDelayedSeconds()`
- `Interact()`, `OnPickup()`, `OnDrop()`, `OnPickupUseDown()`, `OnPickupUseUp()`
- `OnPlayerTriggerEnter/Exit/Stay`
- `OnPlayerJoined`, `OnPlayerLeft`
- `OnOwnershipTransferred`
- `OnPreSerialization`, `OnPostSerialization`
- `VRCPlayerApi`, `TrackingData`
- `VRCObjectPickup`, `VRCObjectSync`
- `GameObject`, `Transform`, `Rigidbody`（基本属性和方法）
- `Animator`（基本参数设置）
- `AudioSource`（基本播放控制）
- `ParticleSystem`（基本控制）
- `Time.time`, `Time.deltaTime`
- `Vector3`, `Quaternion`（基本运算）
- `DataList`, `DataDictionary`, `DataToken`
- `VRCPlayerApi.TeleportTo()`

### 不确定或需要验证
- `Physics.Raycast` — 需要确认，部分项目可用
- `Material.SetColor` — 需要确认在不同 VRChat SDK 版本的表现
- `Renderer.material` — 可能受安全沙箱限制
- `Shader.SetGlobalFloat` — 通常受限

### 确认不可用
- 任何 `System.IO` 文件操作
- 网络请求（HTTP、WebSocket）
- `PlayerPrefs`（跨平台表现可能不一致）
- `Camera` 操作的大部分方法

---

## RULE-API-03: API Heat Assessment

### 热路径安全 API（可在 Update/高频事件中使用）
- `Time.time`, `Time.deltaTime`
- `Vector3` 基本运算
- int/float 比较和赋值
- `Transform.position`（读）
- 数组索引读写

### 避免在热路径使用的 API
- `GameObject.Find()`
- `GetComponent<T>()`
- `Debug.Log()`
- `SendCustomEvent()` — 每次调用有帧延迟
- `RequestSerialization()` — 不应每帧调用
- 字符串操作
- 复杂的 `Transform` 链式访问

---

## RULE-API-04: When Uncertain

当 API 可用性不确定时：
1. 明确告知用户"需要验证"
2. 将 API 列入 `pending/uncertain-api.md`
3. 提供替代方案
4. 建议在 Editor 中测试编译
