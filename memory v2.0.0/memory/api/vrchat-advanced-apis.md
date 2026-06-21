---
title: API: VRChat Advanced APIs
category: api

knowledge_level: core
status: active

tags:
  - api
  - shader
  - light
  - avatar

aliases:
  - "VRChat Advanced APIs"

source: VRChat 官方文档 (creators.vrchat.com/worlds/udon/)
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High
---
# API: VRChat Advanced APIs

> SDK Version: VRChat SDK 3.x
> Last Verified: 2026-06-04

---

## 1. VRCGraphics（图形 API）

### 暴露的函数

| 函数 | 说明 | 热路径 |
|---|---|---|
| `VRCGraphics.Blit(src, dst, mat)` | 使用着色器将源纹理复制到目标 RenderTexture | ❌ |
| `VRCGraphics.DrawMeshInstanced()` | GPU instancing 多次绘制相同网格 | ❌ |
| `VRCShader.PropertyToID(name)` | 获取着色器属性名的 ID（初始化时调用一次，可复用） | ✅ (缓存后) |
| `VRCShader.SetGlobal(propId, value)` | 使用 ID 设置全局着色器值，**在所有着色器可用，包括 Avatar** | ⚠️ |

### 重要说明
- `VRCShader.SetGlobal` 设置的值在 Avatar 着色器中也可见
- `Blit` 不能传 null 目标
- `PropertyToID` 应缓存，避免重复调用

---

## 2. VRCQualitySettings（画质设置）

### 可访问属性

| 属性 | 类型 |
|---|---|
| `AntiAliasing` | int |
| `PixelLightCount` | int |
| `LODBias` | float |
| `MaximumLODLevel` | int |
| `ShadowResolution` | ShadowResolution |
| `ShadowDistance` | float (钳制 0.1-10000) |
| `ShadowCascades` | int |
| `vSyncCount` | int |

### 阴影设置

```csharp
// 按质量等级设置
VRCQualitySettings.SetShadowDistance(float low, float medium, float high, float mobile);
// 所有等级相同
VRCQualitySettings.SetShadowDistance(float allSame);
// 恢复用户配置
VRCQualitySettings.ResetShadowDistance();
```

> ⚠️ 设置阴影距离后用户的 "Shadow Quality" 设置会被覆盖，用户会在菜单中看到警告

### 级联阴影

```csharp
VRCQualitySettings.shadowCascade2Split = float;
VRCQualitySettings.shadowCascade4Split = Vector3;
```

### 事件

`OnVRCQualitySettingsChanged` — 用户更改暴露属性的图形设置时触发

---

## 3. 语音/化身音频控制

### 语音设置 (VRCPlayerApi)

| 方法 | 参数范围 | 说明 |
|---|---|---|
| `SetVoiceGain(int)` | 0-24 dB | 语音增益，默认 15 |
| `SetVoiceDistanceNear(float)` | 0-1,000,000 米 | 音量开始衰减的近距离阈值，建议 0 |
| `SetVoiceDistanceFar(float)` | 0-1,000,000 米 | 能听到语音的最远距离，默认 25 |
| `SetVoiceVolumetricRadius(float)` | 0-1000 米 | 语音源体积半径，默认 0 |
| `SetVoiceLowpass(bool)` | on/off | 远程语音低通滤波（DJ 场景建议关闭） |

### Avatar 音频设置

| 方法 | 参数 | 说明 |
|---|---|---|
| `SetAvatarAudioGain(int)` | 0-10 dB | Avatar 音频最大增益，默认 10 |
| `SetAvatarAudioFarRadius(float)` | 米 | Avatar 音频最远距离，默认 40 |
| `SetAvatarAudioNearRadius(float)` | 米 | 起始距离，默认 0 |
| `SetAvatarAudioVolumetricRadius(float)` | 米 | 体积半径，默认 0 |
| `SetAvatarAudioForceSpatial(bool)` | | 强制空间化 |
| `SetAvatarAudioCustomCurve(bool)` | | 使用自定义曲线 |

---

## 4. Drones（无人机 API）

| 方法/事件 | 说明 |
|---|---|
| `VRCPlayerApi.GetDrone()` | 获取目标玩家的无人机 API |
| `VRCDroneApi.GetPlayer()` | 获取无人机所属玩家 |
| `OnDroneTriggerEnter/Exit/Stay` | 无人机触发事件 |

---

## 5. MIDI 支持

### MIDI 事件

| 事件 | 参数 | 说明 |
|---|---|---|
| `MidiNoteOn` | channel, noteNumber, velocity | Note On 消息 |
| `MidiNoteOff` | channel, noteNumber, velocity | Note Off 消息 |
| `MidiControlChange` | channel, controlNumber, value | 控制改变（旋钮/滑杆） |

支持实时乐器输入和 MIDI 文件回放。

---

## 6. AI Navigation（AI 导航）

### 能力
- 从场景几何体自动生成 NavMesh
- 支持动态障碍物和 OffMesh Links
- **Runtime 生成**：可在 VRChat 客户端运行时创建和更新导航网格

### VRChat 限制
- **自定义 Agent 类型**：不支持
- `NavMeshSurface.UpdateNavMesh()`：返回不可用的 AsyncOperation
- `NavMeshSurface.CollectObjects`：Enum 数组在 Udon 中不可用

---

## 7. 语言 API

| 方法 | 返回 | 说明 |
|---|---|---|
| `GetCurrentLanguage()` | string (RFC 5646) | 本地用户选择的语言 |
| `GetAvailableLanguages()` | string[] | 玩家可选择的所有语言 |
| `OnLanguageChanged` | string | 本地玩家更新显示语言时触发 |

---

## 8. VRC+ 事件

| 事件 | 参数 | 说明 |
|---|---|---|
| `OnVRCPlusMassGift` | gifter, numGifts (int) | 玩家投放礼物炸弹 |
| `OnVRCCameraSettingsChanged` | VRCCameraSettings | 用户更改图形设置 |
| `OnVRCQualitySettingsChanged` | — | 用户调整影响 Quality Settings 的图形设置 |

---

## 9. VRCObjectSync 完整 API

| 方法/属性 | 说明 |
|---|---|
| `FlagDiscontinuity()` | 传送物体时触发，跳过本帧的平滑处理 |
| `SetGravity(bool)` / `GetGravity()` | 设置/获取重力 |
| `SetKinematic(bool)` / `GetKinematic()` | 设置/获取运动学 |
| `Respawn()` | 重生物体到初始位置和旋转，清除速度 |
