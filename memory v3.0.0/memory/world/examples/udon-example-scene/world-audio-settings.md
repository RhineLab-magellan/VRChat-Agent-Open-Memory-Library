---
title: "World Audio Settings"
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
  - audio
  - avatar
aliases:
  - 音频
  - "World Audio Settings"
related:
  - index.md
  - avatar-scaling-settings.md
  - player-mod-setter.md
  - simple-pen-system.md
  - udon-video-sync-player.md
---
# World Audio Settings

> Udon Example Scene · 世界音频设置子页面
> 源文档:https://creators.vrchat.com/worlds/examples/udon-example-scene/world-audio-settings/
> 最后更新:2026-06-15

---

## ⚠️ 重要提示

> **This script is currently not present in the Udon example scene.**
>
> **本脚本当前不在 Udon 示例场景中。**

本页面记录的是**预期/规划中的脚本**,而非当前 SDK 内置示例。如需使用,请自行实现或参考 [Player Audio 文档](https://creators.vrchat.com/worlds/audio/)。

---

## 概述

本 UdonBehaviour 示例脚本允许配置 VRChat World 中的**玩家语音**和**Avatar 音频**。

**关键行为**:
- 脚本在**玩家加入 World 时**设置一次
- 之后可使用其他脚本**修改这些值**

---

## 涉及的音频设置(预期)

| 类别 | 预期配置项 | 说明 |
|------|----------|------|
| **Voice(玩家语音)** | Voice Priority | 玩家语音的优先级(0~100) |
| **Voice(玩家语音)** | Voice Gain | 玩家语音的音量增益(dB) |
| **Voice(玩家语音)** | Voice Distance Near/Far | 玩家语音的近/远距离(米) |
| **BGM(背景音乐)** | BGM Priority | BGM 音频源的优先级 |
| **BGM(背景音乐)** | BGM Volume | BGM 音量 |
| **Avatar Audio(Avatar 音频)** | Avatar Audio Priority | Avatar 音频源的优先级 |
| **Avatar Audio(Avatar 音频)** | Avatar Audio Gain | Avatar 音频音量增益 |

> **注**:具体配置项以 [Player Audio 文档](https://creators.vrchat.com/worlds/audio/) 为准。

---

## API 参考

相关 API:

- `VRCPlayerApi.SetVoiceGain(float)` — 设置玩家语音增益
- `VRCPlayerApi.SetVoiceDistanceNear(float)` — 设置语音近距离
- `VRCPlayerApi.SetVoiceDistanceFar(float)` — 设置语音远距离
- `AudioSource.priority` — 音频源优先级(0 = 最高,256 = 最低)
- `AudioSource.volume` — 音频源音量

**参见**:`memory/api/audio.md`(如存在)、`memory/world/audio.md`

---

## 典型实现模式

```csharp
public class WorldAudioSettings : UdonSharpBehaviour {
    [Header("Voice Settings")]
    public float voiceGain = 15f;
    public float voiceDistanceNear = 0f;
    public float voiceDistanceFar = 25f;
    
    [Header("BGM Settings")]
    public AudioSource bgmSource;
    public int bgmPriority = 128;
    public float bgmVolume = 0.5f;
    
    public override void OnPlayerJoined(VRCPlayerApi player) {
        if (player == Networking.LocalPlayer) {
            // 配置玩家语音
            player.SetVoiceGain(voiceGain);
            player.SetVoiceDistanceNear(voiceDistanceNear);
            player.SetVoiceDistanceFar(voiceDistanceFar);
            
            // 配置 BGM
            if (bgmSource != null) {
                bgmSource.priority = bgmPriority;
                bgmSource.volume = bgmVolume;
            }
        }
    }
}
```

> **警告**:以上为参考实现,**未在 SDK 中提供现成 Prefab**。请基于最新 VRChat Creator Docs 验证 API 签名。

---

## 触发时机

| 事件 | 用途 |
|------|------|
| `OnPlayerJoined` | 玩家加入时应用音频设置(本脚本的典型使用点) |
| 手动调用 | 之后可由其他脚本主动调用修改 |

---

## 已知限制

- **不在 SDK 内置示例中**:本脚本在 [VRChat Creator Docs](https://creators.vrchat.com/worlds/examples/udon-example-scene/world-audio-settings/) 中有说明但**当前未包含在 Udon Example Scene Prefab 中**
- **仅设置一次**:OnPlayerJoined 中只触发一次,动态修改需其他脚本配合
- **每个玩家独立配置**:语音设置是基于玩家的,需要在 `OnPlayerJoined` 中按玩家配置

---

## 与相关知识库关联

- **VRCPlayerApi 完整 API**:`memory/api/player.md`
- **Audio Source Unity API**:`memory/api/audio.md`
- **VRCWorld 整体架构**:[index.md](index.md)
