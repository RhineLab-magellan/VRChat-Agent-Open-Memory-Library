---
title: "VRCAsyncGPUReadback | 异步 GPU 读回"
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
  - osc
  - event
  - udonsharp
aliases:
  - "VRCAsyncGPUReadback | 异步 GPU 读回"
  - asyncgpureadback
related:
  - "world/udon/vrc-graphics/index.md"
  - "hybrid/audio-link.md"
  - "api/udon-type-exposure.md"
---
# VRCAsyncGPUReadback | 异步 GPU 读回

> 来源: VRChat 官方文档 — https://creators.vrchat.com/worlds/udon/vrc-graphics/asyncgpureadback/
> 索引日期: 2026-06-15
> SDK: 3.5.0+
> 父文档: `memory/world/udon/vrc-graphics/index.md` (本文件即父文档内 VRC Graphics 体系一部分,原 `memory/world/vrc-graphics.md` 占位页已删除)

---

## 概述

**AsyncGPUReadback** 是 Unity 的特性,允许开发者将 GPU 上的纹理数据(如特定像素颜色)异步复制到 CPU 代码。与 `Texture2D.GetPixels` 类似,但**不会阻塞主线程**。

通过异步传输,Unity 确保该过程不会影响应用帧率和整体性能。AsyncGPUReadback 帮助开发者避免停滞渲染管线,因为数据传输发生在主线程的并行后台。

**常见用例**:
- 根据渲染输出生成 CPU 端数据
- 创建纹理 mipmap 链
- 实现自定义后处理效果
- 分析渲染帧(AI、Computer Vision)
- **将 RenderTexture 数据传递给 OSC**(VRChat 外发)

---

## VRCAsyncGPUReadback vs Unity AsyncGPUReadback

VRChat 的实现是 Unity 函数的**包装器**(wrapper),使用了**不同的接口**。

| 维度 | Unity `AsyncGPUReadback` | VRChat `VRCAsyncGPUReadback` |
|------|-------------------------|------------------------------|
| **入口** | `AsyncGPUReadback` | `VRCAsyncGPUReadback` |
| **回调方式** | `Action<AsyncGPUReadbackRequest>` | `IUdonEventReceiver` (UdonBehaviour) |
| **接收事件** | 回调直接执行 | 接收 `OnAsyncGpuReadbackComplete` |
| **取数据** | `request.GetData<T>()` | `request.TryGetData(array)` |
| **请求类型** | `AsyncGPUReadbackRequest` | `VRCAsyncGPUReadbackRequest` |

---

## 使用步骤 (4 步)

1. **准备数据数组**(用于接收读回数据)
2. **发起 AsyncGPUReadback 请求**
3. **在 `OnAsyncGpuReadbackComplete` 接收完成消息**
4. **使用 `TryGetData` 从 request 取出数据**

---

## 完整 UdonSharp 示例

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Rendering;
using VRC.Udon.Common.Interfaces;

public class AGPURB : UdonSharpBehaviour
{
    public Texture texture;

    void Start()
    {
        // 步骤 1+2: 发起请求,传入 IUdonEventReceiver(this)
        VRCAsyncGPUReadback.Request(texture, 0, (IUdonEventReceiver)this);
    }

    // 步骤 3: 接收完成消息
    public void OnAsyncGpuReadbackComplete(VRCAsyncGPUReadbackRequest request)
    {
        if (request.hasError)
        {
            Debug.LogError("GPU readback error!");
            return;
        }

        // 步骤 4: 使用 TryGetData 取出数据
        var px = new Color32[texture.width * texture.height];
        Debug.Log("GPU readback success: " + request.TryGetData(px));
        Debug.Log("GPU readback data: " + px[0]);
    }
}
```

---

## 关键 API 详解

### VRCAsyncGPUReadbackRequest 结构

继承自 Unity `AsyncGPUReadbackRequest`,主要属性:

| 属性 | 类型 | 说明 |
|------|------|------|
| `hasError` | bool | 是否发生错误(纹理不可读、格式不支持等) |
| `done` | bool | 读回是否完成 |
| `layerDataSize` | int | 每层数据字节数 |
| `layerCount` | int | 纹理层数 |

**主要方法**:
- `bool TryGetData<T>(T[] data)` — 尝试取出数据到数组,返回成功/失败

### VRCAsyncGPUReadback.Request() 签名族

| 签名 | 用途 |
|------|------|
| `Request(Texture src, int mipIndex, Action<...> callback)` | 异步读回 Texture |
| `Request(RenderTexture src, int mipIndex, Action<...> callback)` | 异步读回 RenderTexture |
| `Request(Texture src, int mipIndex, TextureFormat dstFormat, Action<...> callback)` | 转换格式后读回 |
| `RequestIntoNativeArray(...)` | 读回到 NativeArray(零拷贝) |

> 注: VRChat 包装层将 `Action<...>` 替换为 `IUdonEventReceiver`,但底层调用的仍是 Unity 的同名函数族。

---

## 典型应用场景

### 场景 1: RenderTexture → Texture2D (用于 OSC 发送)

```csharp
public RenderTexture sourceRT;
public Texture2D snapshotTexture;

public void CaptureSnapshot()
{
    // 异步读回 RenderTexture
    VRCAsyncGPUReadback.Request(sourceRT, 0, (IUdonEventReceiver)this);
}

public void OnAsyncGpuReadbackComplete(VRCAsyncGPUReadbackRequest request)
{
    if (request.hasError) return;

    // 转换为 Texture2D 像素数据
    var data = request.GetData<byte>();
    snapshotTexture.LoadRawTextureData(data);
    snapshotTexture.Apply();

    // 可进一步通过 OSC 发送
    SendOSCMessage(snapshotTexture);
}
```

### 场景 2: 音频同步系统的核心机制 (✅ 已验证,参考工程)

音频同步系统使用 `VRCAsyncGPUReadback` 从 GPU 音频纹理读回频谱数据,然后传递给 Shader。

**简化模式**:
```csharp
// 音频同步风格: 每 N 帧请求一次
private int _frameCounter = 0;

void Update()
{
    if (++_frameCounter >= 4)  // 不要每帧调用
    {
        _frameCounter = 0;
        VRCAsyncGPUReadback.Request(audioTexture, 0, (IUdonEventReceiver)this);
    }
}

public void OnAsyncGpuReadbackComplete(VRCAsyncGPUReadbackRequest request)
{
    if (request.hasError) return;
    var spectrumData = request.GetData<float>();
    ProcessSpectrum(spectrumData);
}
```

### 场景 3: ComputeBuffer 读回

```csharp
public ComputeBuffer computeBuffer;

public void ReadComputeResult()
{
    // ComputeBuffer 也支持 readback(需先 UnmarkWritable)
    VRCAsyncGPUReadback.Request(computeBuffer, (IUdonEventReceiver)this);
}

public void OnAsyncGpuReadbackComplete(VRCAsyncGPUReadbackRequest request)
{
    if (request.hasError) return;
    var result = new float[computeBuffer.count];
    request.TryGetData(result);
    // 处理 result...
}
```

---

## 关键限制

| 限制 | 说明 | 应对 |
|------|------|------|
| **回调不在主线程** | GPU 读回完成后回调可能在子线程 | 使用 `SendCustomEvent` 跳转到主线程处理数据 |
| **每次请求有成本** | GPU 同步 + 数据传输 | 避免每帧调用,使用帧间隔(如每 4~10 帧) |
| **Texture 必须可读** | `isReadable = true` | 创建时勾选 Read/Write Enabled |
| **格式兼容性** | 某些压缩格式不支持 readback | 使用 `dstFormat` 参数转换 |
| **Quest 兼容性** | 某些 Quest 配置不可用(老 GPU) | 提供 fallback 路径 |
| **数据大小限制** | 单次 readback 数据过大可能失败 | 分块多次 readback |

### 回调线程问题解决方案

```csharp
// ❌ 错误: 直接在回调中访问 Udon API 可能异常
public void OnAsyncGpuReadbackComplete(VRCAsyncGPUReadbackRequest request)
{
    if (request.hasError) return;
    var data = request.GetData<byte>();
    // 这里 data 仍在 GPU 内存中...
    someUdonVariable = data[0];  // 可能在非主线程
}

// ✅ 正确: SendCustomEvent 跳转到主线程
private byte[] _readbackData;

public void OnAsyncGpuReadbackComplete(VRCAsyncGPUReadbackRequest request)
{
    if (request.hasError) return;
    _readbackData = new byte[request.layerDataSize];
    request.TryGetData(_readbackData);
    SendCustomEvent(nameof(ProcessDataOnMainThread));
}

public void ProcessDataOnMainThread()
{
    // 现在安全地在主线程
    someUdonVariable = _readbackData[0];
}
```

---

## 音频同步系统实战参考 (✅ 已验证,参考工程)

> **FACT**: 音频同步系统是 VRCAsyncGPUReadback 在 VRChat 中最成功的应用

**关键模式**:
1. 音频数据通过 `OnAudioFilterRead` 写入 `CustomRenderTexture`
2. Shader 计算频谱并写入 `_AudioTexture` (作为全局纹理)
3. Avatar/World Shader 采样 `_AudioTexture` 实现音频反应
4. Udon 端用 `VRCAsyncGPUReadback` **可选地**读回 CPU 端做额外处理(但**不是必须**)

**关键优势**:
- 音频驱动 Shader → **零网络同步开销**
- GPU 端直接计算 → CPU 端几乎无开销
- 完整参考实现见 `memory/world/audiolink-architecture.md`

---

## 性能基准

| 操作 | 开销 |
|------|------|
| 一次 256×256 RGBA32 readback | ~0.5-1ms (PC) / 1-3ms (Quest) |
| 一次 1920×1080 RGBA32 readback | ~5-15ms (PC) / 15-30ms (Quest) |
| 回调函数本身 | <0.1ms |

**建议**:
- 1Hz 采样足够大多数用途
- 4Hz 适合实时可视化
- >30Hz 几乎一定引起性能问题

---

## 相关知识

- `memory/world/udon/vrc-graphics/index.md` — VRC Graphics 总览
- `memory/hybrid/audio-link.md` — 音频同步系统 API 完整架构(深度使用 readback)
- `memory/api/udon-type-exposure.md` — `Rendering` 命名空间 7 个类型(VRCAsyncGPUReadback 等)
- Unity 官方文档: [AsyncGPUReadback](https://docs.unity3d.com/ScriptReference/Rendering.AsyncGPUReadback.html)
