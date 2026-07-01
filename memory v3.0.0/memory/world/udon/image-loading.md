---
title: "Image Loading - 远程图片加载"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "本地知识库整理 + VRChat 2026.2.3p1 Release Notes"
source_type: community
version: 1.1
last_review: 2026-06-30
confidence: Medium
tags:
  - world
  - udon
  - udonsharp
aliases:
  - "Image Loading - 远程图片加载"
  - image-loading
related:
  - ai-navigation.md
  - debugging-udon-projects.md
  - external-urls.md
  - ui-events.md
  - vm-and-assembly.md
---
# Image Loading - 远程图片加载

> 来源: https://creators.vrchat.com/worlds/udon/image-loading/
> 抓取日期: 2026-06-15
> SDK: 3.2.3+ (VRCImageDownloader)
> 状态: ✅ FACT (官方文档)

---

## 概述

**Image Loading** 允许从互联网下载图片,在 VRChat 世界中显示为**纹理**。

### 典型用例

- **更新世界纹理** 而无需重新上传
- 创建**季节性海报** / 活动宣传
- 跨世界**重用同一纹理**,一次更新全部生效

SDK 包含易用的 `ImageDownload` 脚本,或用 `VRCImageDownloader` 对象**自己写**。

> **官方推荐**: 查看 [Image Loader Example](/worlds/examples/image-loading) 快速开始
> **本地化示例**: `memory/world/examples/image-loading.md` ⭐ 完整 Prefab + GitHub Pages

---

## 关键限制与参数(必读!)

### 1. 最大分辨率: **2048 × 2048 像素**

> 超过 2048x2048 的图片**下载会失败**

### 2. Rate Limiting(限流)

> **5 秒/张** 的下载限制(全场景共享)

- 超过限制 → 进入**队列**,**随机顺序**下载
- 限制**应用于整个场景**,与 `VRCImageDownload` 组件数量无关

### 3. URL 直接指向图片文件

> **禁止 URL 重定向**!URL 必须直接指向图片,否则失败

### 4. 纹理格式自动识别

下载的图片自动解释为:

| 图片类型 | 格式 |
|---|---|
| 带 alpha 通道 | RGBA32 / RGB64 等 |
| 不带 alpha 通道 | RGB24 / RGB48 等 |
| 灰度图 | R8 / R16 等 |

### 5. 队列上限: **1000 元素**

### 6. 缓冲区限制: **32MB / Input + Output**

- 超过 32MB 会**错误**

### 7. 域白名单(见 `external-urls.md`)

---

## 内存管理(关键!)

> **🔴 关键警告**: 已下载的图片**占用大量内存**!用完后**必须**通过 Udon 释放。

```csharp
// ❌ 错误 - 下载新图但没释放旧图,玩家最终崩溃
void DownloadNewImage()
{
    _imageDownloader.DownloadImage(newUrl, this, _textureInfo);
    // 旧图还在内存中!
}

// ✅ 正确 - 释放旧图
void DownloadNewImage()
{
    if (_currentDownload != null)
    {
        _currentDownload.Dispose();  // 释放旧图
    }
    _currentDownload = _imageDownloader.DownloadImage(newUrl, this, _textureInfo);
}
```

> **严重后果**: 不释放图片,玩家在世界停留足够长时间后**会内存溢出崩溃**!

---

## VRCImageDownloader API

### 构造

```csharp
new VRCImageDownloader()
```

> **🔴 必读**: 必须**保存为字段**!否则会被 GC 回收,Texture 也会丢失引用
> 官方原话: "It's important to store the VRCImageDownloader as a variable, to stop it from being garbage collected!"

```csharp
// ❌ 错误 - 局部变量会被 GC
public void Download()
{
    var downloader = new VRCImageDownloader();
    downloader.DownloadImage(...);  // 危险
}

// ✅ 正确
[SerializeField] private VRCImageDownloader _imageDownloader;
```

### DownloadImage 方法

```csharp
IVRCImageDownload DownloadImage(
    VRCImageDownloader Instance,      // 必需:ImageDownloader 组件
    VRCUrl Url,                        // 必需:图片 URL
    Material Material = null,         // 可选:自动应用为主纹理
    UdonBehaviour UdonBehavior = null, // 可选:接收事件的 UdonBehaviour
    TextureInfo TextureInfo = null     // 可选:纹理参数
)
```

**返回** `IVRCImageDownload` - 可用于跟踪下载进度。

> **UdonSharp 重要提示**: UdonSharp **不会自动**接收事件,**必须**显式指定 `UdonBehavior` 参数(通常用 `(IUdonEventReceiver)this`)。

### Dispose 方法

```csharp
void Dispose()
```

- 清理 `VRCImageDownloader`
- **释放**已下载的纹理
- Dispose 后 `VRCImageDownloader` **不可再用**下载新图

> **Dispose 行为**:
> - Dispose 整个 `VRCImageDownloader` 会使**所有**相关 `IVRCImageDownload` 和纹理失效
> - 只想释放**单个**下载 → Dispose 单个 `IVRCImageDownload`

---

## TextureInfo(纹理参数)

```csharp
public class TextureInfo
{
    bool GenerateMipmaps = false;       // 默认 false
    FilterMode FilterMode = Trilinear;  // 默认 Trilinear
    TextureWrapMode WrapModeU = Repeat; // 默认 Repeat
    TextureWrapMode WrapModeV = Repeat; // 默认 Repeat
    TextureWrapMode WrapModeW = Repeat; // 默认 Repeat(仅 Texture3D 有关)
    int AnisoLevel = 9;                 // 默认 9
    string MaterialProperty = "_MainTex"; // 默认 _MainTex
}
```

### AnisoLevel 强制规则

> **VRChat 使用强制各向异性过滤**

- `1 ≤ value ≤ 9` → Unity 强制设为 **9**
- `value > 9` → Unity 钳制在 **[9, 16]**
- `0` → 禁用过滤

---

## IVRCImageDownload(下载结果)

通过 `VRCImageDownloader.DownloadImage`、`OnImageLoadSuccess`、`OnImageLoadError` 返回。

> **注意**: 多数字段在**下载完成或失败前**是无效的。

| 方法 | 返回 | 说明 |
|---|---|---|
| `GetError()` | `VRCImageDownloadError` | 关联的错误(失败时) |
| `GetErrormessage()` | `string` | 错误消息 |
| `GetMaterial()` | `Material` | 传给 `DownloadImage` 的 Material |
| `GetProgress()` | `float` | 下载进度 [0, 1](用于自定义加载条) |
| `GetResult()` | `Texture2D` | 下载的图片纹理 |
| `GetSizeInMemoryBytes()` | `int` | 纹理占用字节数 |
| `GetState()` | `VRCImageDownloadState` | 下载状态 |
| `GetTextureInfo()` | `TextureInfo` | 传入的纹理信息 |
| `GetUdonbehavior()` | `UdonBehaviour` | 接收事件的 UdonBehaviour |
| `GetURL()` | `VRCURL` | 下载的 URL |

### Dispose 单个 IVRCImageDownload

```csharp
// 释放单个下载,不影响其他下载
currentDownload.Dispose();
```

Dispose 后 State 变为 `Unloaded`。

---

## VRCImageDownloadState 枚举

| 状态 | 说明 |
|---|---|
| `Pending` | 未开始或进行中 |
| `Error` | 下载失败(见 `VRCImageDownloadError`) |
| `Complete` | 下载完成,纹理可用 |
| `Unloaded` | Dispose 后的待 GC 状态 |
| `Unknown` | 未知状态 |

---

## VRCImageDownloadError 枚举

| 错误 | 触发条件 |
|---|---|
| `InvalidURL` | URL 无效 |
| `AccessDenied` | URL 访问被拒 |
| `InvalidImage` | 下载的不是有效图片 |
| `DownloadError` | Web 请求错误 |
| `Unknown` | 未知错误 |

---

## 事件签名

```csharp
public override void OnImageLoadSuccess(IVRCImageDownload result);
public override void OnImageLoadError(IVRCImageDownload result);
```

---

## 典型用法(完整示例)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon.Common.Interfaces;

public class ImageDownloaderExample : UdonSharpBehaviour
{
    [SerializeField] private VRCUrl imageUrl;
    [SerializeField] private Material targetMaterial;  // 可选

    // 🔴 必须保存为字段
    private VRCImageDownloader _downloader;
    private IVRCImageDownload _download;
    private TextureInfo _textureInfo;

    void Start()
    {
        _downloader = new VRCImageDownloader();  // 必须在 Start 中创建
        _textureInfo = new TextureInfo();
        _textureInfo.GenerateMipmaps = true;
        _textureInfo.FilterMode = FilterMode.Trilinear;
        _textureInfo.AnisoLevel = 9;
    }

    public void DownloadImage()
    {
        // 释放旧下载
        if (_download != null)
        {
            _download.Dispose();
        }
        // 启动新下载
        _download = _downloader.DownloadImage(
            imageUrl,
            (IUdonEventReceiver)this,  // UdonSharp 必须显式指定
            targetMaterial,             // 可选
            _textureInfo                // 可选
        );
    }

    public override void OnImageLoadSuccess(IVRCImageDownload result)
    {
        Texture2D tex = result.GetResult();
        Debug.Log($"Image downloaded: {tex.width}x{tex.height}, " +
                  $"size: {result.GetSizeInMemoryBytes()} bytes");
        // 应用到目标 material(若未在 DownloadImage 指定)
    }

    public override void OnImageLoadError(IVRCImageDownload result)
    {
        Debug.LogError($"Image load failed: {result.GetErrormessage()}");
        _download = null;  // 清理
    }

    void OnDestroy()
    {
        if (_download != null) _download.Dispose();
        if (_downloader != null) _downloader.Dispose();
    }
}
```

---

## 风险与陷阱

| 风险 | 等级 | 说明 |
|---|---|---|
| 不释放旧图片 | 🔴 严重 | 玩家长时间停留会**内存溢出崩溃** |
| `VRCImageDownloader` 未保存为字段 | 🔴 严重 | 被 GC 回收,Texture 引用丢失 |
| 超过 2048x2048 分辨率 | 🟡 中等 | 下载失败 |
| 超过 5s/张 限流 | 🟡 中等 | 进入队列,顺序随机 |
| 超过 32MB 缓冲区 | 🟡 中等 | 失败 |
| 队列超过 1000 元素 | 🟡 中等 | 失败 |
| UdonSharp 未指定 UdonBehavior | 🟡 中等 | 收不到回调 |
| URL 重定向 | 🟡 中等 | 失败 |
| 灰度图 + alpha | 🟢 低 | 解释为 RG(不是 RGBA) |

## 🔄 VRChat 修复历史 (2026.2.3p1+)

> **FACT** (2026.2.3p1):"Fixed textures not being accessible from the CPU when loaded via `VRCImageDownloader`."

### 问题描述

| 项目 | 详情 |
|------|------|
| **受影响操作** | `VRCImageDownloader` 加载的纹理在 CPU 端访问(如 `GetPixels()`, `EncodeToPNG()`) |
| **原行为** | 访问返回**空数据**或**异常** |
| **修复行为** | CPU 端访问现在**正常返回像素数据** |
| **修复版本** | 2026.2.3p1+ |

### 创作者影响

| 影响项 | 说明 |
|--------|------|
| **CPU 纹理操作** | `GetPixels`, `GetPixel`, `EncodeToPNG` 等现在可用 |
| **动态生成纹理** | 可读取下载图片后处理(滤镜、合成) |
| **无需代码改动** | 纯引擎层修复 |
| **旧版客户端** | 2026.2.3 之前可能仍触发此问题 |

### 典型用例

```csharp
// 修复后:可以从下载的图片读取像素
public override void OnImageLoadSuccess(IVRCImageDownload result)
{
    Texture2D tex = (Texture2D)result.Material.mainTexture;
    
    // 2026.2.3p1+ 之前:返回空数据
    // 2026.2.3p1+:正常返回像素数据
    Color[] pixels = tex.GetPixels();
    
    // 可以做后续处理
    // 例如:模糊滤镜
    for (int i = 0; i < pixels.Length; i++)
    {
        pixels[i].r *= 0.5f;  // 红色减半
    }
    tex.SetPixels(pixels);
    tex.Apply();
}
```

### 关联文档

- `memory/world/examples/image-loading.md` - 完整图片加载示例
- `memory/api/events-reference.md` - OnImageLoadSuccess 事件签名

---

## 与知识库互补

- **完整 Image Loading 示例**: `memory/world/examples/image-loading.md` ⭐ SlideshowFrame Prefab
- **External URLs + 白名单**: `memory/world/udon/external-urls.md` ⭐
- **String Loading**: `memory/world/udon/string-loading.md` ⭐ 类似机制
- **Udon 事件**: `memory/api/events-reference.md` ⭐ OnImageLoad* 事件

---

## 相关 VRChat 官方文档

- [Image Loading](/worlds/udon/image-loading) - 本页官方原版
- [Image Loader Example](/worlds/examples/image-loading) - 官方示例
