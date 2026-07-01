---
title: "AudioLink 音频同步系统 API 与使用指南"
category: hybrid
knowledge_level: applied
status: active
source: "github.com/llealloo/audiolink"
source_type: community
version: 1.0
upstream_version: "v3.1.2 (2026-02-15)"
last_review: 2026-06-21
confidence: Medium
tags:
  - hybrid
  - shader
  - audio
  - avatar
aliases:
  - 音频
  - "AudioLink 音频同步系统 API 与使用指南"
related:
  - osc-protocol.md
  - alcom.md
  - udon-world-plugins.md
  - vcc.md
  - "../world/vrc-light-volumes.md"
---
# AudioLink 音频同步系统 API 与使用指南

> **本文定位**:VRChat 音频同步系统(AudioLink)的 API 参考 + 组件使用指南
> **本文性质**:工具使用文档(Group C — 实用工具使用指南),保留项目名和 API 命名
> **学习方式**:作为工具学习 — 创作者通过本文档学习如何在自己的 Avatar/World 中使用音频同步系统
> **仓库**: https://github.com/llealloo/audiolink (原 vrchat-community/audiolink 已 404,2026 年迁移至 llealloo 个人仓库)
> **当前版本**: **v3.1.2** (2026-02-15)

---

## 系统概述

| 属性 | 值 |
|------|-----|
| 纹理尺寸 | 128×64 (8192 像素) |
| 采样率 | 48000 Hz |
| 频率范围 | 13.75 Hz - 14080 Hz |
| 频段划分 | 10 octaves × 24 bins = 240 DFT bins |
| 4-band 频率 | Bass / LowMid / HighMid / Treble |

---

## ALPass 向量定义(Shader 索引)

### 核心通道

| Pass 名称 | UV 坐标 | 说明 |
|-----------|---------|------|
| `ALPASS_AUDIOLINK` | (0, 0) | 主音频数据 |
| `ALPASS_AUDIOBASS` | (0, 0) | 低频 (Band 0) |
| `ALPASS_AUDIOLOWMIDS` | (0, 1) | 中低频 (Band 1) |
| `ALPASS_AUDIOHIGHMIDS` | (0, 2) | 中高频 (Band 2) |
| `ALPASS_AUDIOTREBLE` | (0, 3) | 高频 (Band 3) |
| `ALPASS_DFT` | (0, 4) | 离散傅里叶变换数据 |
| `ALPASS_WAVEFORM` | (0, 6) | 波形数据 |
| `ALPASS_AUDIOLINKHISTORY` | (1, 0) | 历史音频数据 |

### VU 与时间

| Pass 名称 | UV 坐标 | 说明 |
|-----------|---------|------|
| `ALPASS_GENERALVU` | (0, 22) | 通用 VU 表 |
| `ALPASS_GENERALVU_INSTANCE_TIME` | (2, 22) | 实例时间 |
| `ALPASS_GENERALVU_LOCAL_TIME` | (3, 22) | 本地时间 |
| `ALPASS_GENERALVU_NETWORK_TIME` | (4, 22) | 网络时间 |
| `ALPASS_GENERALVU_PLAYERINFO` | (6, 22) | 玩家信息 |
| `ALPASS_MEDIASTATE` | (5, 22) | 媒体状态 |

### 主题颜色

| Pass 名称 | UV 坐标 | 说明 |
|-----------|---------|------|
| `ALPASS_THEME_COLOR0` | (0, 23) | 主题色 0 |
| `ALPASS_THEME_COLOR1` | (1, 23) | 主题色 1 |
| `ALPASS_THEME_COLOR2` | (2, 23) | 主题色 2 |
| `ALPASS_THEME_COLOR3` | (3, 23) | 主题色 3 |

### 其他通道

| Pass 名称 | UV 坐标 | 说明 |
|-----------|---------|------|
| `ALPASS_CCINTERNAL` | (12, 22) | CC 内部数据 |
| `ALPASS_CCCOLORS` | (25, 22) | CC 颜色 |
| `ALPASS_CCSTRIP` | (0, 24) | CC 条带 |
| `ALPASS_CCLIGHTS` | (0, 25) | CC 灯光 |
| `ALPASS_AUTOCORRELATOR` | (0, 27) | 自相关器 |
| `ALPASS_FILTEREDAUDIOLINK` | (0, 28) | 滤波音频 |
| `ALPASS_CHRONOTENSITY` | (16, 28) | 时间性 |
| `ALPASS_FILTEREDVU` | (24, 28) | 滤波 VU |
| `ALPASS_GLOBAL_STRINGS` | (40, 28) | 全局字符串 |

---

## 核心常量

```csharp
AudioLinkWidth = 128
AudioLinkHeight = 64
AudioLinkSps = 48000
AudioLinkExpBins = 24
AudioLinkExpOct = 10
AudioLinkETotalBins = 240
AudioLinkBottomFrequency = 13.75f
AudioLinkBaseAmplitude = 2.5f
AudioLinkDftQ = 4.0f
AudioLinkTrebleCorrection = 5.0f
AudioLink4BandTargetRate = 90.0f
```

---

## 数据编码格式

### 字符串编码(Unicode → Float)

```csharp
// UpdateGlobalString() - 每 4 个字符编码为 1 个 Vector4
Vector4[] vecs = new Vector4[8];  // 32 字符最大
for (int i = 0; i < vecs.Length; i++)
{
    vecs[i].x = IntToFloatBits24Bit(codePoints[j++]);
    vecs[i].y = IntToFloatBits24Bit(codePoints[j++]);
    vecs[i].z = IntToFloatBits24Bit(codePoints[j++]);
    vecs[i].w = IntToFloatBits24Bit(codePoints[j++]);
}
audioMaterial.SetVectorArray(nameID, vecs);
```

### 时间编码

```csharp
// DecodeDataAsSeconds() - 27 位整数编码秒
int time = (int)DecodeDataAsUInt(position) & 0x7ffffff;
return (float)(time / 1000) + (float)(time % 1000) / 1000.0f;
```

---

## UdonSharp API

### 纹理数据访问

```csharp
// 检查数据可用性(需要 audioDataToggle = true)
audioLink.AudioDataIsAvailable()

// 读取像素
audioLink.GetDataAtPixel(x, y)           // 直接读取
audioLink.LerpAudioDataAtPixel(x, y)     // 线性插值
audioLink.GetDataAtPixelMultiline(x, y)  // 多行包裹

// 频率采样
audioLink.GetAmplitudeAtFrequency(440f)   // 指定 Hz
audioLink.GetAmplitudeAtQuarterNote(3, 12) // 3 octave, 12 quarter
audioLink.GetAmplitudeAtNote(4, 0)       // 4 octave, C note
```

### 时间系统

```csharp
audioLink.GetChronoTime(index: 0, band: 0)           // 原始时间
audioLink.GetChronoTimeNormalized(index, band, speed) // 归一化 [0,1]
audioLink.GetChronoTimeInterval(index, band, speed, interval) // 带区间
```

### 字符串同步

```csharp
audioLink.GetCustomString1()  // 获取同步字符串 1
audioLink.GetCustomString2()  // 获取同步字符串 2
```

---

## 同步架构

### Manual Sync + Owner Transfer

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class AudioLink : UdonSharpBehaviour
{
    [UdonSynced] public string customString1;

    public void UpdateCustomStrings()
    {
        if (!Networking.IsOwner(gameObject))
            Networking.SetOwner(_localPlayer, gameObject);

        // ... 更新逻辑

        RequestSerialization();
    }
}
```

### 位域压缩模式

```csharp
[UdonSynced] byte _flags = 0b10;  // bit0=playing, bit1=locked

void CopyIntoFlags()
{
    _flags = 0;
    if (_syncOwnerPlaying) _flags |= 1;
    if (_syncLocked) _flags |= 2;
}
```

---

## 性能特征

### 已知热点

| 操作 | 频率 | 开销 | 备注 |
|------|------|------|------|
| `SendAudioOutputData` | 每帧 | ~2ms | 8 次 SetFloatArray |
| `FPSUpdate` | 每秒 | 低 | 时间同步计算 |
| `UpdateGlobalString` | 按需 | 中 | 字符串编码 |

### 实验性功能

| 功能 | 默认 | 风险 |
|------|------|------|
| `audioDataToggle` | false | VRCAsyncGPUReadback 成本高 |

### WebGL 路径

```csharp
#if UNITY_WEBGL && !UNITY_EDITOR
    FetchAnalyzerLeft(WebALID, audioLinkWebPeer.WaveformSamplesLeft, 4096);
    FetchAnalyzerRight(WebALID, audioLinkWebPeer.WaveformSamplesRight, 4096);
#endif
```

---

## 组件列表

### 核心组件

| 组件 | 说明 |
|------|------|
| `AudioLink` | 主控制器，音频处理核心 |
| `AudioLink.DataAPI` | 数据访问 API |
| `AudioLinkController` | UI 控制面板 |
| `AudioLinkControllerHandle` | 控制句柄 |
| `AudioLinkMiniPlayer` | 视频播放器 |
| `AudioLinkZone` | 区域检测 |

### 响应组件

| 组件 | 说明 |
|------|------|
| `AudioReactiveLight` | 灯光响应 |
| `AudioReactiveObject` | 物体变换响应 |
| `AudioReactiveBlendshapes` | 表情同步 |
| `AudioReactiveSurface` | 表面发光 |
| `AudioReactiveSurfaceArray` | 表面数组 |

### 辅助组件

| 组件 | 说明 |
|------|------|
| `ThemeColorController` | 主题色同步 |
| `GlobalSlider` | 全局滑块同步 |
| `GlobalToggle` | 全局开关同步 |

---

## 📚 相关设计模式(参考工程提炼)

本文档是 AudioLink 系统**使用指南**(API、组件、UV 坐标)。如需了解从 AudioLink 提炼的**通用设计模式**(纹理编码、Master 时间锚点、漂移校正等),请参阅:

- `memory/FACT.md` §核心设计模式 — 模式 1-5
- `memory/world/udon/data-containers/byte-and-bit-operations.md` — 位域压缩底层原理
- `memory/patterns/bit-packed-flags.md` — 位域压缩同步模式应用

> **设计模式 → 实际应用**:AudioLink 是这些设计模式的"代表实现",创作者可以参考其 API 用法,将这些模式应用到自己的项目中

---

## 📚 参考实现

本节描述的开源 VRChat 音频同步系统(AudioLink)项目,见:

- `memory/sources/open-source-projects.md` §音频同步类目

如需了解项目安装、VPM 配置、源码版本,参阅 `memory/sources/` 目录
