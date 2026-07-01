---
title: "VRChat Shader Globals | `_VRChat*` 全局变量"
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
  - world
  - udon
  - shader
  - culling
aliases:
  - 着色器
  - "VRChat Shader Globals | `_VRChat*` 全局变量"
related:
  - "world/udon/vrc-graphics/index.md"
  - "avatar/shader/scss.md"
  - "api/udon-type-exposure.md"
---
# VRChat Shader Globals | `_VRChat*` 全局变量

> 来源: VRChat 官方文档 — https://creators.vrchat.com/worlds/udon/vrc-graphics/vrchat-shader-globals/
> 索引日期: 2026-06-15
> Last Published: 2026-02-23
> 父文档: `memory/world/udon/vrc-graphics/index.md` (本文件即父文档内 VRC Graphics 体系一部分,原 `memory/world/vrc-graphics.md` 占位页已删除)

---

## 概述

VRChat 提供多个**全局 Shader 参数**,Shader 创建者可以使用这些参数实现 VRChat 特定功能(如检测手持相机模式、获取网络时间、检测镜面渲染等)。

> ⚠️ **🔴 警告**: 不要在自定义 Shader 中使用 `_VRChat` 前缀(除了本页文档化的变量)。该前缀是**受保护命名空间**,VRChat 可能随时新增未文档化的变量。

---

## 相机相关全局变量

### `_VRChatCameraMode` (float)

当前相机模式:

| 值 | 含义 |
|---|------|
| `0` | 正常渲染 |
| `1` | VR 手持相机中渲染 |
| `2` | Desktop 手持相机中渲染 |
| `3` | 截图中渲染 |

**典型用途**:
- 在手持相机视角中隐藏特定 UI
- 截图模式下禁用某些动画
- 优化不同模式下的渲染质量

```hlsl
float cameraMode = _VRChatCameraMode;
if (cameraMode == 3.0) {
    // 截图模式: 提高抗锯齿质量
    quality = HIGH;
}
```

### `_VRChatCameraMask` (uint)

当前相机的 `cullingMask` 属性。**仅在 `_VRChatCameraMode != 0` 时可用**。

```hlsl
uint cameraMask = _VRChatCameraMask;
// 可用于检查是否包含特定 layer
bool showUI = (cameraMask & (1 << UI_LAYER)) != 0;
```

### `_VRChatMirrorMode` (float)

当前是否在镜面渲染中:

| 值 | 含义 |
|---|------|
| `0` | 正常渲染,不在镜中 |
| `1` | VR 中查看的镜面 |
| `2` | Desktop 模式下查看的镜面 |

### `_VRChatFaceMirrorMode` (float)

| 值 | 含义 |
|---|------|
| `0` | 不是面部镜面 |
| `1` | 面部镜面渲染(VR 和 Desktop 使用不同相机类型!) |

### 相机位置/旋转变量

| 变量 | 类型 | 内容 |
|------|------|------|
| `_VRChatMirrorCameraPos` | `float3` | 镜相机世界坐标(非 VR 眼相关,"居中")。不在镜中时为 `(0,0,0)` |
| `_VRChatScreenCameraPos` | `float3` | 主屏幕相机世界坐标。相机未激活时为 `(0,0,0)` |
| `_VRChatPhotoCameraPos` | `float3` | 手持拍照相机世界坐标。相机未激活时为 `(0,0,0)` |
| `_VRChatScreenCameraRot` | `float4` | 主屏幕相机旋转(四元数)。相机未激活时为 `(0,0,0,0)` |
| `_VRChatPhotoCameraRot` | `float4` | 手持相机旋转(四元数)。相机未激活时为 `(0,0,0,0)` |

**典型用途**:
- 屏幕空间反射(SSR)使用相机位置重建视图矩阵
- 自定义天空盒根据相机位置切换
- 计算世界 UI 与相机的相对距离

```hlsl
// 自定义天空盒: 根据相机模式切换
float3 cameraPos = _VRChatScreenCameraPos;
if (_VRChatCameraMode > 0.5) {
    cameraPos = _VRChatPhotoCameraPos;
}
// 用 cameraPos 重建视图矩阵
```

---

## VRChat 时间全局变量

`_VRChatTime*` 全局变量提供各种时间信息,可用于时钟、动画同步等。

> **重要**: 所有下列全局变量都是**无符号整数位模式**,在 Shader 中应定义为 `uint`。

### 基础时间变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `_VRChatTimeUTCUnixSeconds` | `uint` | 当前 UTC 时间(秒)的低 32 位 Unix 时间戳。按无符号数处理,**2038 年前不会溢出**。若系统时间设置为 1970 年之前,该值未定义 |
| `_VRChatTimeNetworkMs` | `uint` | 网络同步时间(毫秒)。**等价于** Udon 的 `Networking.GetServerTimeInMilliseconds()`。技术上是有符号数,但可按无符号处理。**仅用于同步和偏移**,绝对值无意义;可能回绕 |

### 编码时间变量 (位域)

> 这些变量将多个时间字段编码为单个 `uint`,使用位范围(从 0 开始)。

#### `_VRChatTimeEncoded1` (32 bits)

| 位范围 | 内容 |
|--------|------|
| `[0-4]` | 当前小时(UTC, 0-23) |
| `[5-10]` | 当前分钟(UTC, 0-59) |
| `[11-16]` | 当前秒(UTC & Local 共用) |
| `[17-21]` | 当前小时(Local, 0-23) |
| `[22-27]` | 当前分钟(Local, 0-59) |
| `[28-31]` | **保留** |

#### `_VRChatTimeEncoded2` (32 bits)

| 位范围 | 内容 |
|--------|------|
| `[0-9]` | 毫秒(UTC & Local 共用) |
| `[10]` | 时区偏移符号位(1 = 负偏移) |
| `[11-26]` | UTC 到 Local 时区偏移(秒) |
| `[27-31]` | **保留** |

> 所有 UTC 到 Local 的时区偏移受 VRChat 菜单中"首选时区"设置影响。
> "当前时间"始终指**观察者的本地时间**,而非 Avatar 穿戴者的本地时间。

### 时间变量可用性

时间值在 VRChat 客户端及所有 VRChat SDK 中**Play Mode 期间**可用。

---

## SDK HLSL 辅助函数

VRChat SDK 提供头文件含解码时间格式的辅助函数。

### Include 路径

```hlsl
#include "Packages/com.vrchat.base/ShaderLibrary/VRCTime.cginc"
```

### 可用函数

| 函数 | 返回值 | 用途 |
|------|--------|------|
| `VRC_GetUTCUnixTimeInSeconds()` | `uint` | 获取 UTC Unix 时间(秒) |
| `VRC_GetNetworkTimeInMilliseconds()` | `uint` | 获取网络同步时间(毫秒) |
| `VRC_GetUTCTime(out uint h, out uint m, out uint s, out uint ms)` | void | 解码 UTC 时间 |
| `VRC_GetLocalTime(out uint h, out uint m, out uint s, out uint ms)` | void | 解码 Local 时间 |
| `VRC_GetTimezoneOffsetSeconds()` | `int` | 获取时区偏移(秒) |

### 完整 Shader 示例

```hlsl
Shader "Custom/VRCTimeClock"
{
    Properties { }

    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            #include "Packages/com.vrchat.base/ShaderLibrary/VRCTime.cginc"

            struct appdata { float4 vertex : POSITION; };
            struct v2f { float4 vertex : SV_POSITION; float2 uv : TEXCOORD0; };

            v2f vert(appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.vertex.xy * 0.5 + 0.5;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                // 提取本地时间
                uint h, m, s, ms;
                VRC_GetLocalTime(h, m, s, ms);

                // 时钟显示: 小时角度
                float hourAngle = (h % 12) / 12.0 * 6.28318;
                float2 center = float2(0.5, 0.5);
                float2 toCenter = i.uv - center;
                float angle = atan2(toCenter.y, toCenter.x);

                // 时针
                float hourHand = smoothstep(0.05, 0.0, abs(angle - hourAngle));
                hourHand *= smoothstep(0.4, 0.3, length(toCenter));

                return fixed4(hourHand, hourHand, hourHand, 1.0);
            }
            ENDCG
        }
    }
}
```

---

## U# 端使用示例

虽然 `_VRChat*` 是 Shader 端变量,但 U# 可以读取对应的 Udon API:

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class VRCTimeReader : UdonSharpBehaviour
{
    void Update()
    {
        // 等价于 _VRChatTimeNetworkMs (Udon 端)
        uint networkMs = (uint)Networking.GetServerTimeInMilliseconds();

        // UTC Unix 时间(秒)
        uint unixSeconds = (uint)(System.DateTime.UtcNow.Subtract(
            new System.DateTime(1970, 1, 1)).TotalSeconds);

        Debug.Log($"Network: {networkMs}ms, UTC: {unixSeconds}s");
    }
}
```

---

## 性能考量

| 操作 | 开销 |
|------|------|
| 读取 `_VRChat*` 全局变量 | **零成本**(Shader 端 uniform) |
| 多次读取相同变量 | 编译器会优化为单次 |
| `VRCTime.cginc` 辅助函数 | 一次解码(位运算,几乎免费) |

**建议**:
- 在 `vert` / `frag` 中**直接读取**全局变量,无需 Udon 端转发
- 避免在 Udon 中通过 `SetGlobal` 设置这些变量(无效)
- 时间变量在每帧自动更新

---

## `_VRChat` vs `_Udon` 前缀对比

| 前缀 | 类型 | 用途 | 数量 |
|------|------|------|------|
| **`_VRChat*`** | VRChat 引擎注入 | 相机模式、镜子、时间等**只读**全局信息 | 受保护命名空间,VRChat 维护 |
| **`_Udon*`** | Udon 用户注入 | 通过 `VRCShader.SetGlobal*` 自定义**可写**全局参数 | 用户控制 |

**关键区别**:
- `_VRChat*` 由 VRChat 引擎**自动设置**,Udon 不能修改
- `_Udon*` 由 Udon **手动设置**,世界和 Avatar 都可以读取
- 两者互不冲突,可同时使用

```hlsl
// Avatar Shader 同时使用两种全局变量
float4 frag() : SV_Target {
    // 读取 VRChat 引擎变量
    if (_VRChatCameraMode > 0.5) return float4(0,0,0,1);  // 手持相机中隐藏

    // 读取 Udon 自定义变量
    float3 tintColor = _UdonTint;  // 由 World 的 Udon 脚本设置
    return float4(tintColor, 1.0);
}
```

---

## 相关知识

- `memory/world/udon/vrc-graphics/index.md` — VRC Graphics 总览
- `memory/avatar/shader/liltoon/` — lilToon 中对 `_VRChat` 变量的使用
- `memory/avatar/shader/scss.md` — SCSS 时间同步
- `memory/api/udon-type-exposure.md` — `Rendering` 命名空间
- 官方文档: https://creators.vrchat.com/worlds/udon/vrc-graphics/vrchat-shader-globals/
