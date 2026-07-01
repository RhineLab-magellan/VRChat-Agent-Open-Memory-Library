---
title: "Player Audio — 玩家语音与 Avatar 音频"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/udon/players/player-audio/ (Last updated: 2025-04-04)"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - audio
  - avatar
aliases:
  - 音频
  - "Player Audio — 玩家语音与 Avatar 音频"
related:
  - player-avatar-scaling.md
  - player-positions.md
  - getting-players.md
  - player-collisions.md
  - player-forces.md
---
# Player Audio — 玩家语音与 Avatar 音频

> Domain: World / Udon / Players
> Subtype: API 详解
> 底层引用: `memory/api/player-api.md`
> 抓取日期: 2026-06-15

---

## 概述

玩家有两个音频源:
1. **麦克风语音** (Voice)
2. **Avatar 附件音频** (Avatar Audio)

Udon 可以控制**其他玩家**的语音/Avatar 音频如何被**本地玩家**听到。**不能改变玩家自己听到自己的方式**(例如无法调整玩家对自己语音的增益)。

**简单示例** — 把玩家语音增益从默认 15dB 调低到 5dB:
```csharp
somePlayer.SetVoiceGain(5);
```

---

## Voice API (语音控制)

### Set Voice Gain

- **签名**: `SetVoiceGain(int dB)`
- **单位**: 分贝 (dB)
- **范围**: 0 - 24
- **默认**: 15
- **说明**: 给玩家的语音**添加增益**(可正可负,实际 API 限制 0-24)
- **典型用途**: 远距离玩家降低增益,近战玩家恢复正常

---

### Set Voice Distance Near

- **签名**: `SetVoiceDistanceNear(float meters)`
- **单位**: 米
- **范围**: 0 - 1,000,000
- **默认**: 0
- **说明**: 语音音量**开始衰减**的近距离阈值
- **强烈建议** ⚠️: 保持为 0,以获得真实的空间感

---

### Set Voice Distance Far

- **签名**: `SetVoiceDistanceFar(float meters)`
- **单位**: 米
- **范围**: 0 - 1,000,000
- **默认**: 25
- **说明**: 能听到该玩家语音的**最远距离**
- **典型用途**:
  - 调低值 → 让该玩家语音"传不远"(私密对话场景)
  - 设为 0 → **实际上让该玩家被静音**(对本地而言)

> 📌 **实现原理**: 这就是"静音别人"的官方推荐方式 — 设置 `DistanceFar = 0`

---

### Set Voice Volumetric Radius

- **签名**: `SetVoiceVolumetricRadius(float meters)`
- **单位**: 米
- **范围**: 0 - 1,000
- **默认**: 0
- **说明**: 玩家语音的**体积半径**(默认点声源,设置后呈现"区域感")
- **使用建议** ⚠️:
  - **保持为 0,除非明确知道用途**
  - 主要用于大型远距离音频源需要"听起来更大"的场景
  - **必须** `<` `VoiceDistanceFar`,否则逻辑错乱
- **替代方案**: 想让远距离玩家语音听起来近 → 增大 `VoiceDistanceNear` 而不是 VolumetricRadius

---

### Set Voice Lowpass

- **签名**: `SetVoiceLowpass(bool enabled)`
- **默认**: `true` (开启低通滤波)
- **说明**: 当语音较远时,通过低通滤波器提升嘈杂世界中的可懂度
- **关闭场景**: 当玩家用语音通道播放**高质量 DJ 混音**等高保真音频时,关闭此滤波以保留高频
- **应用**: DJ 舞台、ASMR 房间、远程表演场景

---

## Avatar Audio API (Avatar 音频)

> 控制玩家 Avatar 附件的 `AudioSource` 在世界中的表现。

### SetAvatarAudioGain

- **签名**: `SetAvatarAudioGain(int dB)`
- **单位**: 分贝
- **范围**: 0 - 10
- **默认**: 10
- **说明**: Avatar 音频的**最大允许增益**

---

### SetAvatarAudioFarRadius

- **签名**: `SetAvatarAudioFarRadius(float meters)`
- **单位**: 米
- **范围**: 无限制
- **默认**: 40
- **说明**: 听到 Avatar 音频的**最远距离**
- **静音实现**: 设为 0 等同于静音该玩家的 Avatar 音频
- **关键**: 与 `AudioSource.maxDistance` 比较,取**较小**值

---

### SetAvatarAudioNearRadius

- **签名**: `SetAvatarAudioNearRadius(float meters)`
- **单位**: 米
- **范围**: 无限制
- **默认**: 0
- **说明**: 听到 Avatar 音频**达到最大音量**的起始距离
- **关键**: 与 `AudioSource.maxDistance` 比较,取**较小**值

---

### SetAvatarAudioVolumetricRadius

- **签名**: `SetAvatarAudioVolumetricRadius(float meters)`
- **单位**: 米
- **范围**: 无限制
- **默认**: 0
- **使用建议** ⚠️:
  - **保持为 0,除非明确知道用途**
  - 必须 `<` `AvatarAudioFarRadius`

---

### SetAvatarAudioForceSpatial

- **签名**: `SetAvatarAudioForceSpatial(bool enabled)`
- **默认**: `false`
- **说明**: 强制开启空间化(`spatialBlend = 1`)
- **用途**: 覆盖 Avatar 内 AudioSource 的空间化设置

---

### SetAvatarAudioCustomCurve

- **签名**: `SetAvatarAudioCustomCurve(bool enabled)`
- **默认**: `false`
- **说明**: 是否使用预配置的自定义曲线
- **依赖**: 需 Avatar 端预设自定义曲线才有效

---

## 典型场景配方

### 1. 静默其他玩家(本地视角)

```csharp
// 让该玩家的语音无法被本地玩家听到
targetPlayer.SetVoiceDistanceFar(0);
targetPlayer.SetAvatarAudioFarRadius(0);
```

### 2. DJ 舞台 — 关闭低通滤波保真

```csharp
djPlayer.SetVoiceLowpass(false);
djPlayer.SetVoiceDistanceFar(1000000); // 远距离也清晰
```

### 3. 私密对话圈 — 限制语音距离

```csharp
// 让该玩家的语音只在 5 米内可闻
targetPlayer.SetVoiceDistanceFar(5f);
targetPlayer.SetVoiceDistanceNear(0f);
```

### 4. 大型表演者 — 体积感语音

```csharp
performerPlayer.SetVoiceVolumetricRadius(5f);   // 5米体感
performerPlayer.SetVoiceDistanceFar(50f);        // 50米最远
```

---

## 与底层 API 的对照

| 本文件 API | 底层 `player-api.md` 摘要 |
|---|---|
| `SetVoiceGain` | 0-24 dB, 默认 15 |
| `SetVoiceDistanceNear` | 0-1,000,000 米, 建议 0 |
| `SetVoiceDistanceFar` | 0-1,000,000 米, 默认 25 |
| `SetVoiceVolumetricRadius` | 0-1000 米, 默认 0 |
| `SetVoiceLowpass` | on/off |
| `SetAvatarAudioGain` | 0-10 dB, 默认 10 |
| `SetAvatarAudioFarRadius` | 默认 40 |
| `SetAvatarAudioNearRadius` | 默认 0 |
| `SetAvatarAudioVolumetricRadius` | 默认 0 |
| `SetAvatarAudioForceSpatial` | 默认 Off |
| `SetAvatarAudioCustomCurve` | 默认 Off |

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **远端玩家角度** | `SetVoice*` 控制的是**本地玩家**对该玩家语音的接收方式,不是该玩家自身的输出 |
| **默认值易被覆盖** | 玩家加入时这些设置不会自动应用,需在 `OnPlayerJoined` 中重新设置 |
| **VolumetricRadius 与 FarRadius 关系** | VolumetricRadius 必须 < FarRadius,违反会导致无声/异常行为 |
| **Lowpass 误关** | 在嘈杂场景关闭 Lowpass 会让远距离玩家完全听不清,除非明确是高保真需求 |
| **Quest 性能** | 同时设置过多玩家的音频参数对 Quest 不友好,避免在 `Update` 中批量调用 |

---

## 与其他知识库的关系

| 知识库 | 关系 |
|---|---|
| `memory/api/player-api.md` | 底层 API 简略版 |
| `memory/api/audio.md` | 一般音频 API(待补充) |
| `memory/world/examples/mute-others.md` | 静音其他玩家完整示例 (引用本文件) |
| `memory/world/udon/audio.md` | 3D 音频/世界音频设置(待补充) |
