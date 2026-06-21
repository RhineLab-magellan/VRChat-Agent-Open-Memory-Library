---
title: API: Player API
category: api

knowledge_level: core
status: active

tags:
  - api
  - ownership
  - udonsharp

aliases:
  - "Player API"

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-04
confidence: High
---
# API: Player API


---

## VRCPlayerApi

### 生命周期

#### OnPlayerJoined(VRCPlayerApi player)
- **暴露**: ✅
- **说明**: 玩家加入房间时调用。用于初始化 per-player 数据。
- **注意**: 此时玩家的 VRCPlayerApi 已可用，但对象可能尚未完全加载。

#### OnPlayerLeft(VRCPlayerApi player)
- **暴露**: ✅
- **说明**: 玩家离开房间时调用。用于清理 per-player 数据。
- **注意**: 如果该玩家是某些对象的 owner，会触发 ownership transfer。

### 常用属性

#### player.displayName
- **暴露**: ✅
- **热路径**: ✅ (缓存后)
- **说明**: 返回玩家显示名称字符串。

#### player.isLocal
- **暴露**: ✅
- **说明**: 判断是否是本地玩家。

#### player.isMaster
- **暴露**: ✅
- **说明**: 判断是否是房间 Master。

#### player.playerId
- **暴露**: ✅ (需要验证具体 API 名)
- **说明**: 玩家唯一 ID（int）。

### 位置/追踪

#### player.GetTrackingData(VRCPlayerApi.TrackingDataType trackingDataType)
- **暴露**: ✅
- **说明**: 获取玩家追踪数据（头、手位置旋转等）。
- **TrackingDataType**: Head, LeftHand, RightHand, Origin 等。

#### player.GetPosition()
- **暴露**: ✅
- **说明**: 获取玩家位置。等价于 GetTrackingData(Head).position。

#### player.TeleportTo(Vector3 position, Quaternion rotation)
- **暴露**: ✅
- **说明**: 将本地玩家传送到指定位置。只能在本地玩家上调用。

---

## 语音/音频控制

### 语音设置

| 方法 | 参数 | 说明 |
|---|---|---|
| `SetVoiceGain(int)` | 0-24 dB, 默认 15 | 语音增益 |
| `SetVoiceDistanceNear(float)` | 0-1,000,000 米 | 音量开始衰减的近距离阈值，建议 0 |
| `SetVoiceDistanceFar(float)` | 0-1,000,000 米 | 能听到语音的最远距离，默认 25 |
| `SetVoiceVolumetricRadius(float)` | 0-1000 米 | 语音源体积半径，默认 0 |
| `SetVoiceLowpass(bool)` | on/off | 远程语音低通滤波（DJ 场景建议关闭） |

### Avatar 音频设置

| 方法 | 参数 | 说明 |
|---|---|---|
| `SetAvatarAudioGain(int)` | 0-10 dB, 默认 10 | Avatar 音频最大增益 |
| `SetAvatarAudioFarRadius(float)` | 米, 默认 40 | 最远距离 |
| `SetAvatarAudioNearRadius(float)` | 米, 默认 0 | 起始距离 |
| `SetAvatarAudioVolumetricRadius(float)` | 米, 默认 0 | 体积半径 |
| `SetAvatarAudioForceSpatial(bool)` | | 强制空间化 |
| `SetAvatarAudioCustomCurve(bool)` | | 使用自定义曲线 |

---

## 额外属性与方法

| 属性/方法 | 说明 |
|---|---|
| `IsInstanceOwner` | 邀请/好友+实例返回 true，公开实例始终 false |
| `InstanceOwner` | 返回实例 owner 的 VRCPlayerApi 或 null |
| `IsVRCPlus` | 是否有 VRC+ 订阅 |
| `IsSuspended` | 设备是否被暂停（睡眠/切换应用） |
| `GetPickupInHand(Hand)` | 获取手持拾取物（仅本地玩家有效） |
| `PlayHapticEventInHand(Hand, duration, amplitude, frequency)` | 手柄震动（0-1） |
| `UseAttachedStation()` | 使玩家进入同 GameObject 上的 Station |
| `SimulationTime` | 玩家的模拟时间 |
| `GetDrone()` | 获取目标玩家的无人机 API → VRCDroneApi |

## 语言 API

| 方法 | 返回 | 说明 |
|---|---|---|
| `GetCurrentLanguage()` | string (RFC 5646) | 本地用户选择的语言 |
| `GetAvailableLanguages()` | string[] | 玩家可选择的所有语言 |

## 新增事件

| 事件 | 触发时机 |
|---|---|
| `OnPlayerSuspendChanged` | 玩家设备被暂停/唤醒 |
| `OnScreenUpdate` | 移动设备进入世界或设备方向变化 |
| `OnInputMethodChanged` | 本地玩家使用不同输入方式 |
| `OnLanguageChanged` | 本地玩家更新显示语言 |

### 常见错误
- 在 OnPlayerJoined 中尝试修改其他玩家的数据（只能操作本地玩家）
- 缓存 VRCPlayerApi 引用过长（玩家离开后引用失效）
- 高频读取 GetTrackingData（每次都有跨 VM 调用成本）
- **Player Collision 仅对移动物体有效**：当玩家"走进"静止物体时不触发
