---
title: "VRC Graphics | VRCGraphics / VRCShader / VRCCameraSettings / VRCQualitySettings"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - misc
  - index
  - navigation
aliases:
  - 着色器
  - "VRC Graphics | VRCGraphics / VRCShader / VRCCameraSettings / VRCQualitySettings"
related:
  - vrchat-shader-globals.md
  - asyncgpureadback.md
  - "world/udon/vrc-graphics/asyncgpureadback.md"
  - "world/udon/vrc-graphics/vrchat-shader-globals.md"
  - asyncgpureadback.md
  - "world/performance-guide.md"
  - "rules/udonsharp-language-limits.md"
  - "api/udon-type-exposure.md"
---
# VRC Graphics | VRCGraphics / VRCShader / VRCCameraSettings / VRCQualitySettings

> 来源: VRChat 官方文档 — https://creators.vrchat.com/worlds/udon/vrc-graphics/
> 索引日期: 2026-06-15
> SDK: 3.5.0+
> 父文档: `memory/world/udon/vrc-graphics/index.md` 自身(原 `memory/world/vrc-graphics.md` 已删除,内容已整合至本文件及子页面)
> 子页面: `asyncgpureadback.md`、`vrchat-shader-globals.md`
> 互链文档: `memory/world/vrc-camera-settings.md`、`memory/world/vrc-quality-settings.md`

---

## 概述

Udon 提供对 Unity Graphics 功能子集的访问,通过 4 个 VRC 命名空间下的类型暴露:

| 类型 | 命名空间 | 作用 | 详细文档 |
|------|----------|------|----------|
| **VRCShader** | `VRC.SDK3.Rendering` (推断) | 全局 Shader 参数设置器 | 本文件 + `vrchat-shader-globals.md` |
| **VRCGraphics** | `VRC.SDK3.Rendering` (推断) | Unity `Graphics` 类子集(Blit/DrawMeshInstanced) | 本文件 |
| **VRCCameraSettings** | `VRC.SDK3.Rendering` (推断) | 屏幕/手持相机访问、VR 双眼位置 | `memory/world/vrc-camera-settings.md` |
| **VRCQualitySettings** | `VRC.SDK3.Rendering` (推断) | 质量设置只读访问 + 阴影距离覆盖 | `memory/world/vrc-quality-settings.md` |

**与 Unity Graphics 的关系**:
- `VRCGraphics` **不是** `UnityEngine.Graphics` 的完全替代,而是其**白名单子集**
- 所有方法都经过 Udon VM 校验,跨平台兼容性由 VRChat SDK 维护
- 性能敏感(每帧调用会触发 GPU 同步)

---

## VRCGraphics API

### VRCGraphics.Blit()

将源纹理复制到目标 RenderTexture,使用指定 shader。

#### 签名
```csharp
// 标准 Blit
VRCGraphics.Blit(Texture source, RenderTexture dest);

// 带缩放/偏移
VRCGraphics.Blit(Texture source, RenderTexture dest, Vector2 scale, Vector2 offset);

// 使用自定义 Material
VRCGraphics.Blit(Texture source, Material mat, int pass);
```

**注意**:
- **不允许** 传 `null` 作为 destination
- Material 版本隐式写入当前激活 RenderTexture

#### 典型用途

- 屏幕后处理 (Post-processing)
- 实时模糊 (Blur)、色阶 (Color Grading)
- 小地图 (Minimap) 渲染
- 自定义 UI 蒙版

#### Meta Quest 限制 ⚠️🔴

**VRCGraphics.Blit 在 Quest GPU 上不会工作**,除非满足以下条件之一:

| 方案 | 实现 |
|------|------|
| **1. Shader 加 ZTest Always** | 在 Shader 的 Pass 中添加 `ZTest Always` |
| **2. 关闭 RenderTexture Depth** | 设置 `renderTexture.depth = 0` |

**未做此处理会导致操作静默失败**(不报错但不渲染)。

```hlsl
// Shader Pass 修复示例
Pass
{
    ZTest Always  // ← Quest 必需
    ZWrite Off
    Cull Off
    // ...
}
```

参考实现: SDK Samples → Minimap (提供 Udon Graph + UdonSharp 两个版本)。

---

### VRCGraphics.DrawMeshInstanced()

使用 GPU 实例化绘制同一网格多次。

```csharp
VRCGraphics.DrawMeshInstanced(Mesh mesh, int submeshIndex, Material material, Matrix4x4[] matrices);
```

**适用场景**:
- 大量相同几何体(草丛、粒子、装饰物)
- 替代 `Instantiate` + `Renderer` 数组,显著降低 Draw Call

**性能优势**:
- 单次 Draw Call 渲染 N 个实例
- 适合 10~1000+ 同质对象批量渲染
- 不适合每个实例材质不同的场景

---

## VRCShader API

### VRCShader.PropertyToID()

获取基于 shader 属性名的 ID。**强烈建议在初始化时调用一次**,ID 可重复使用且不会改变(跨材质、跨 Shader 保持稳定)。

```csharp
int id = VRCShader.PropertyToID("_UdonMyProperty");
```

#### 🔴 关键限制:`_Udon` 前缀

属性名必须以 **`_Udon`** 为前缀,或使用字面量 **`_AudioTexture`**。否则:

| 情况 | 行为 |
|------|------|
| 属性名有 `_Udon` 前缀 | ✅ 可用于 `SetGlobal`,全局生效 |
| 属性名是 `_AudioTexture` | ✅ 可用于 `SetGlobal`(AudioLink 专用) |
| 属性名**无** `_Udon` 前缀 | ⚠️ `PropertyToID` 仍返回 ID,但 `SetGlobal` **静默失败** |

**示例**:
```csharp
// ✅ 正确
int id1 = VRCShader.PropertyToID("_UdonTintColor");    // 全局生效
int id2 = VRCShader.PropertyToID("_AudioTexture");      // AudioLink 专用通道

// ❌ 错误 - PropertyToID 不报错,但 SetGlobal 不会生效
int id3 = VRCShader.PropertyToID("TintColor");
VRCShader.SetGlobalColor(id3, Color.red);  // 静默失败
```

### VRCShader.SetGlobal() 全套方法

使用 `PropertyToID` 获取的 ID 作为 key,设置值将在**世界中所有 Shader**(包括 Avatar Shader!)中以该名称可用。

| 方法 | 说明 |
|------|------|
| `VRCShader.SetGlobalFloat(int id, float value)` | 全局 Float |
| `VRCShader.SetGlobalInt(int id, int value)` | 全局 Int(注:Unity bug 仍按 float 存) |
| `VRCShader.SetGlobalVector(int id, Vector4 value)` | 全局 Vector4 |
| `VRCShader.SetGlobalColor(int id, Color value)` | 全局 Color |
| `VRCShader.SetGlobalMatrix(int id, Matrix4x4 value)` | 全局 4x4 矩阵 |
| `VRCShader.SetGlobalTexture(int id, Texture value)` | 全局 Texture(替代材质实例化) |
| `VRCShader.SetGlobalBuffer(int id, ComputeBuffer value)` | 全局 ComputeBuffer |
| `VRCShader.SetGlobalFloatArray(int id, float[] values)` | 全局 Float 数组 |
| `VRCShader.SetGlobalVectorArray(int id, Vector4[] values)` | 全局 Vector 数组 |
| `VRCShader.SetGlobalMatrixArray(int id, Matrix4x4[] values)` | 全局 Matrix 数组 |
| `VRCShader.SetGlobalInteger(int id, int value)` | ⚠️ 由于 Unity bug,内部仍以 float 存储 |

**作用范围**:
- 同一 **World 实例** 内全部 Shader(包括玩家 Avatar 上的 Shader)
- **不影响** 其他 World 实例
- 不会持久化(World 重载后值重置)

**U# 完整示例**:
```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Rendering;

[UdonBehaviourSyncMode(BehaviourSyncMode.NoVariableSync)]
public class GlobalShaderController : UdonSharpBehaviour
{
    [SerializeField] private Color tintColor = Color.white;
    private int _tintColorID;
    private int _glowIntensityID;

    void Start()
    {
        // 初始化时获取 ID(可重用)
        _tintColorID = VRCShader.PropertyToID("_UdonTintColor");
        _glowIntensityID = VRCShader.PropertyToID("_UdonGlowIntensity");

        // 初始化时设置默认值,避免每帧调用
        VRCShader.SetGlobalColor(_tintColorID, tintColor);
        VRCShader.SetGlobalFloat(_glowIntensityID, 1.0f);
    }

    public void SetTint(Color newColor)
    {
        VRCShader.SetGlobalColor(_tintColorID, newColor);
    }

    public void SetGlow(float intensity)
    {
        VRCShader.SetGlobalFloat(_glowIntensityID, Mathf.Clamp01(intensity));
    }
}
```

---

## VRChat 提供的内置 Shader Globals

> ⚠️ 不要在自定义 Shader 中使用 `_VRChat` 前缀(受保护命名空间,新变量可能随时新增)

### 相机相关(详见 [vrchat-shader-globals.md](./vrchat-shader-globals.md))

| 变量 | 类型 | 说明 |
|------|------|------|
| `_VRChatCameraMode` | float | 0=正常 / 1=VR 手持 / 2=Desktop 手持 / 3=截图 |
| `_VRChatCameraMask` | uint | 相机 cullingMask(modal!=0 时可用) |
| `_VRChatMirrorMode` | float | 0=不在镜中 / 1=VR 镜 / 2=Desktop 镜 |
| `_VRChatFaceMirrorMode` | float | 1=面部镜子 / 0=其他 |
| `_VRChatMirrorCameraPos` | float3 | 镜相机世界坐标 |
| `_VRChatScreenCameraPos` | float3 | 主屏相机位置 |
| `_VRChatPhotoCameraPos` | float3 | 手持相机位置 |
| `_VRChatScreenCameraRot` | float4 | 主屏相机旋转(四元数) |
| `_VRChatPhotoCameraRot` | float4 | 手持相机旋转(四元数) |

### 时间相关(详见 [vrchat-shader-globals.md](./vrchat-shader-globals.md))

| 变量 | 类型 | 说明 |
|------|------|------|
| `_VRChatTimeUTCUnixSeconds` | uint | UTC Unix 时间(秒,32 位无符号) |
| `_VRChatTimeNetworkMs` | int/uint | 网络同步时间(等价 `Networking.GetServerTimeInMilliseconds`) |
| `_VRChatTimeEncoded1` | uint | 时/分/秒(UTC+Local 编码) |
| `_VRChatTimeEncoded2` | uint | 毫秒 + 时区偏移 |

**SDK 辅助**:
```hlsl
#include "Packages/com.vrchat.base/ShaderLibrary/VRCTime.cginc"

uint VRC_GetUTCUnixTimeInSeconds();
uint VRC_GetNetworkTimeInMilliseconds();
void VRC_GetUTCTime(out uint hours, out uint minutes, out uint seconds, out uint ms);
void VRC_GetLocalTime(out uint hours, out uint minutes, out uint seconds, out uint ms);
int VRC_GetTimezoneOffsetSeconds();
```

---

## 子页面

| 子页面 | 内容 |
|--------|------|
| [asyncgpureadback.md](./asyncgpureadback.md) | VRCAsyncGPUReadback 异步 GPU 读回 API、回调机制、AudioLink 应用 |
| [vrchat-shader-globals.md](./vrchat-shader-globals.md) | `_VRChat*` 全局变量详细说明(相机/镜子/时间)、HLSL 辅助 |

---

## 性能考量

| 操作 | 建议 |
|------|------|
| `SetGlobalFloat/Vector/...` | **避免每帧调用**,在状态变化时设置 |
| `SetGlobalTexture` | 替代材质实例化,适合大纹理共享 |
| `DrawMeshInstanced` | 适合 ≥10 个同质对象批量渲染 |
| `Blit` | 单帧不要多次(每次触发 GPU 同步) |
| `VRCAsyncGPUReadback.Request` | 避免每帧调用,有 GPU/CPU 同步成本 |

---

## 相关知识库

- `memory/world/udon/vrc-graphics/asyncgpureadback.md` — AsyncGPUReadback 详细
- `memory/world/udon/vrc-graphics/vrchat-shader-globals.md` — `_VRChat*` 全局变量详细
- `memory/world/udon/async-gpu-readback.md` (旧版,如有) — 历史参考
- `memory/world/performance-guide.md` — 渲染性能优化
- `memory/avatar/shader/` — Avatar Shader 全局变量集成
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制(末尾已补充 VRC Graphics 限制)
- `memory/api/udon-type-exposure.md` — 暴露类型清单(VRCGraphics/VRCShader 已确认在 `Rendering` 命名空间)
