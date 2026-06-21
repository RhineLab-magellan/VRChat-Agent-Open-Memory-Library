# Udon Type Exposure Tree - VRChat SDK 3.10.3

> Type: INDEX
> Source: `参考文献/UdonTypeExposure.txt` + VRChat 官方文档
> SDK Version: 3.10.3
> Export Date: 2026-06-11
> Confidence: High
> Last Updated: 2026-06-15
> **关联参考**:`memory/world/udon/vm-and-assembly.md` - Udon Types 命名规则(`VRC.SDKBase.VRCPlayerApi+TrackingData` → `VRCSDKBaseVRCPlayerApiTrackingData`)

---

## Udon Type 命名规则(摘要)

> **FACT**:"Udon Types" 是 Udon 引用 C# 类型的方式,与 .NET 命名有两点区别:
> 1. **移除所有 `.` 和 `+`**:`VRC.SDKBase.VRCPlayerApi+TrackingData` → `VRCSDKBaseVRCPlayerApiTrackingData`
> 2. **`[]` 追加 `Array` 后缀**:`System.Int32[]` → `SystemInt32Array`
>
> **关键例外**:
> - `VRCUdonUdonBehaviour` → `VRCUdonCommonInterfacesIUdonEventReceiver`(Array 后缀规则仍适用)
> - `VRCInstantiate` 是唯一"伪造"的 Udon 类型名
>
> **完整规则与示例**:见 `memory/world/udon/vm-and-assembly.md` §"Udon Types"

---

## 概述

Udon Type Exposure Tree 描述了 VRChat Udon VM 暴露的 Unity API 类型和成员。

**统计数据**：
- 总类型数：1387
- 有暴露成员的类型：1067
- 暴露成员总数：9579
- 未暴露成员总数：6323

---

## 文件格式说明

```
[Namespace] NamespaceName <namespace>
  [Type] (XX%) TypeName <kind>
    [EXPOSED] <Type> TypeName           ← 类型本身暴露
    [EXPOSED] <Method> Signature        ← 暴露的方法
    [NOT EXPOSED] <Property> Signature  ← 未暴露的属性
```

**标记含义**：
| 标记 | 含义 |
|------|------|
| `[EXPOSED]` | 该成员在 Udon 中可用 |
| `[NOT EXPOSED]` | 该成员不可用 |
| `[Type] (XX%)` | XX% 表示该类型的暴露程度 |

---

## 命名空间索引

| 命名空间 | 暴露类型数 | 说明 |
|----------|-----------|------|
| `Playables` | 542 | UnityEngine 核心类型（GameObject, Transform, Physics 等）|
| `Diagnostics` | 62 | System 类型（String, Math, Convert, DateTime 等）|
| `UI` | 108 | UnityEngine.UI 组件 |
| `TMPro` | 34 | TextMeshPro 类型 |
| `Video` | 38 | VRC 视频系统 |
| `Platform` | 36 | VRC 平台 API（Networking, VRCPlayerApi 等）|
| `Data` | 13 | VRC 数据容器（DataList, DataDictionary, DataToken）|
| `Dynamics` | 27 | VRC 物理动力学（VRCConstraintSource, Contact 等）|
| `Components` | 18 | VRC 组件（VRCContactReceiver, VRCPhysBone 等）|
| `Animations` | 16 | Unity 约束系统（ParentConstraint, LookAtConstraint 等）|
| `Navigation` | 9 | NavMesh 导航系统 |
| `AI` | 33 | NavMeshAgent 等 AI 类型 |
| `Rendering` | 7 | VRC 渲染 API |
| `Cinemachine` | 12 | Cinemachine 虚拟相机 |
| `AVPro` | 2 | AVPro 视频播放器 |
| `Base` | 2 | VRC 视频基类 |
| `RegularExpressions` | 20 | 正则表达式 |
| `Generic` | 5 | 泛型集合接口 |
| `NetworkCalling` | 1 | `[NetworkCallable]` 支持 |
| `StringLoading` | 2 | VRC 字符串下载 |
| `Economy` | 5 | VRC 经济系统 |
| `Midi` | 7 | VRC MIDI 支持 |
| `Image` | 9 | VRC 图片下载 |

---

## 关键类型快速查表

### UnityEngine 核心

| 类型 | 暴露率 | 暴露成员 | 路径 |
|------|--------|----------|------|
| GameObject | 高 | 大部分 | `Playables.GameObject` |
| Transform | 高 | 大部分 | `Playables.Transform` |
| Component | 61.7% | 20+ | `Playables.Component` |
| Vector3 | 高 | 全部 | `Playables.Vector3` |
| Quaternion | 高 | 全部 | `Playables.Quaternion` |
| Time | 高 | 全部 | `Playables.Time` |
| Mathf | 高 | 大部分 | `Playables.Mathf` |

### 物理系统

| 类型 | 暴露率 | 暴露成员 | 路径 |
|------|--------|----------|------|
| Rigidbody | 97.3% | 71 | `Playables.Rigidbody` |
| Rigidbody2D | 98.7% | 78 | `Playables.Rigidbody2D` |
| Collider | 高 | 大部分 | `Playables.Collider` |

### 渲染系统

| 类型 | 暴露率 | 暴露成员 | 路径 |
|------|--------|----------|------|
| Material | 81.9% | 127 | `Playables.Material` |
| Renderer | 高 | 大部分 | `Playables.Renderer` |
| Camera | 85.0% | 119 | `Playables.Camera` |
| Mesh | 78.6% | 169 | `Playables.Mesh` |

### 动画系统

| 类型 | 暴露率 | 暴露成员 | 路径 |
|------|--------|----------|------|
| Animator | 95.3% | 142 | `Playables.Animator` |
| AnimationClip | 78.9% | 15 | `Playables.AnimationClip` |

### 音频系统

| 类型 | 暴露率 | 暴露成员 | 路径 |
|------|--------|----------|------|
| AudioSource | 高 | 大部分 | `Playables.AudioSource` |

### 粒子系统

| 类型 | 暴露率 | 暴露成员 | 路径 |
|------|--------|----------|------|
| ParticleSystem | 90.1% | 73 | `Playables.ParticleSystem` |

### VRC 特定类型

| 类型 | 暴露率 | 暴露成员 | 路径 |
|------|--------|----------|------|
| VRCPlayerApi | 43.2% | 89 | `Platform.VRCPlayerApi` |
| Networking | 42.2% | 30 | `Platform.Networking` |
| DataList | 92.9% | 39 | `Data.DataList` |
| DataDictionary | 76.9% | 20 | `Data.DataDictionary` |
| DataToken | 99.4% | 156 | `Data.DataToken` |

---

## 暴露树文件位置

原始文件：`参考文献/UdonTypeExposure.txt`
解析数据：`参考文献/udon_exposure_parsed.json`
详细分析：`参考文献/key_types_analysis.txt`

---

## 相关知识

- `memory/api/exposed-types.md` — 已暴露类型详细清单
- `memory/api/not-exposed.md` — 未暴露 API 黑名单
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制
- `memory/api/udonsharp-runtime.md` — UdonSharp 运行时系统
- `memory/world/udon/vm-and-assembly.md` — **官方字节码规范**(Udon Type 命名规则、EXTERN 签名、9 Opcodes)
- `memory/rules/udon-vm-architecture.md` — Udon VM 架构(逆向分析)