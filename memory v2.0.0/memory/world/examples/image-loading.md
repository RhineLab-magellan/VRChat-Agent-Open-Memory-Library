---
title: Image Loading Example
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - event
  - udonsharp

aliases:
  - "Image Loading Example"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Image Loading Example

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/image-loading)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/image-loading/
> 文档版本: Last updated Oct 29, 2024
> SDK: 3.2.3+ (VRCImageDownloader / VRCStringDownloader)

## Example Central Package

> ⚠️ **独立 GitHub 仓库**(非 Example Central 内置)
> 通过 GitHub 仓库单独下载
> 包含完整 Gallery 场景、SlideshowFrame Prefab、Web 资源模板

### GitHub 仓库
- **仓库**: https://github.com/vrchat-community/examples-image-loading
- **Zip 下载**: https://codeload.github.com/vrchat-community/examples-image-loading/zip/refs/heads/main
- **Prefab Unitypackage (v0.2.0)**: https://github.com/vrchat-community/examples-image-loading/releases/download/0.2.0/SlideshowFrame.unitypackage
- **场景路径**: `Assets/_Project/Gallery`

### 资源托管
- 演示用 GitHub Pages 托管(免费)
- 推荐方案: GitHub Pages(免费 + 与仓库同源)
- 自定义: 任何可公开访问的 HTTP/HTTPS URL

---

## 概述

演示 Udon 从互联网**下载图片**并作为**世界物体的纹理**或**UI 元素**显示。
- 演示如何用 GitHub Pages 免费托管图片资源
- 提供完整的 SlideshowFrame Prefab,可直接拖入场景使用

---

## 关键 Udon API

| API | 用途 | 触发事件 |
|-----|------|----------|
| `new VRCImageDownloader()` | 构造下载器(必须**保存为变量**防 GC) | - |
| `VRCStringDownloader.LoadUrl(VRCUrl, IUdonEventReceiver)` | 加载字符串(标题) | `OnStringLoadSuccess/Error` |
| `downloadImage.DownloadImage(VRCUrl, IUdonEventReceiver, TextureInfo)` | 下载图片 | `OnImageLoadSuccess/Error` |

### 重要注意事项
> ⚠️ **VRCImageDownloader 必须保存为字段**
> 否则会被 GC 回收,Texture 也将丢失引用
> 文档原话: "It's important to store the VRCImageDownloader as a variable, to stop it from being garbage collected!"

---

## 重要 GameObject 结构

### TheFrame

```
TheFrame (GameObject)
├── SlideshowFrame (UdonBehaviour - 下载逻辑)
├── Mesh (黑色相框)
├── Picture (Mesh - 渲染下载的纹理)
└── UI (World-Space Canvas - 显示标题)
```

### SlideshowFrame 公共变量

| 名称 | 类型 | 说明 |
|------|------|------|
| `Image Urls` | `VRCUrl[]` | 要下载的图片 URL 数组 |
| `String Url` | `VRCUrl` | 标题字符串 URL(单数) |
| `Renderer` | `Renderer` | 目标 Renderer,`sharedMaterial` 的 texture 被设置 |
| `Field` | `UI Element` | 标题显示 UI |
| `Slide Duration Seconds` | `float` | 每张图片显示时长 |

---

## 核心逻辑流程

### 1. Start 阶段

```csharp
private void Start()
{
    // 关键: this 必须 cast 为 IUdonEventReceiver
    _udonEventReceiver = (IUdonEventReceiver)this;

    // 标题(字符串)下载一次,成功后回调 OnStringLoadSuccess
    VRCStringDownloader.LoadUrl(stringUrl, _udonEventReceiver);
}
```

### 2. 字符串下载成功

```csharp
public override void OnStringLoadSuccess(IVRCStringDownload result)
{
    _captions = result.Result.Split('\n');
    UpdateCaptionText();
}

public override void OnStringLoadError(IVRCStringDownload result)
{
    Debug.LogError($"Could not load string {result.Error}");
}
```

### 3. 图片下载

```csharp
// 下载时把 downloader 保存到字段
_imageDownloader = new VRCImageDownloader();
_imageDownloader.DownloadImage(imageUrl, _udonEventReceiver, _textureInfo);

// 成功回调
public override void OnImageLoadSuccess(IVRCImageDownload result)
{
    // 设置 Renderer 的 texture
    renderer.sharedMaterial.SetTexture("_MainTex", result.Texture);
    // 延迟后加载下一张
    SendCustomEventDelayedSeconds(nameof(LoadNext), SlideDurationSeconds);
}
```

### 4. 循环

- 每次访问同一张图(2nd+ time)会从缓存引用加载,不会重新下载
- 如果首次下载失败,该位置永远为空(无重试)

---

## URL 模式

### GitHub Pages 格式
```
https://<your-github-username>.github.io/<your-repo-name>/1.jpg
https://<your-github-username>.github.io/<your-repo-name>/captions.csv
```

### 关键提示
> 💡 **只要文件名保持不变(1.jpg, 2.jpg...)**,更新 GitHub 仓库后 URL 仍然指向新文件
> 仓库自带 GitHub Action(`.github/workflows/static.yml`)自动发布到 Pages

### VRCUrl 设置要求
- 用户需在 VRChat 客户端启用 **"Untrusted URLs"** 设置
- 这是 VRChat 默认的安全策略,需用户主动启用

---

## VRChat SDK 自带 `ImageDownload` 脚本

如果不想自己写代码,可以直接使用 SDK 自带的封装:
1. 创建 GameObject
2. 添加 UdonBehaviour
3. Program Source 选择 `ImageDownload`
4. 选择要应用纹理的 Material
5. (可选) 自定义 `TextureInfo` 设置

---

## 已知问题(文档原话)

- ⚠️ **第一张图的标题加载不够快**,首次循环时不会显示,到第二圈才显示
- 这是 GitHub Issue 中跟踪的常见问题

---

## 与知识库互补

- **VRCImageDownloader 完整 API**: `memory/world/image-loading.md`(待建)
- **VRCStringDownloader**: 同上
- **Untrusted URLs 客户端设置**: `memory/world/supported-assets.md`(待建)
- **VRCUrl**: `memory/api/vrc-url.md`(待建)
- **Example Central**: `memory/sources/example-central.md`

## 相关 Udon 文档链接

- [主 Image Loading 文档页](/worlds/udon/image-loading) - 完整 API、域名与文件限制
- [GitHub: examples-image-loading](https://github.com/vrchat-community/examples-image-loading)
- [GitHub Pages](https://pages.github.com/)
- [SlideshowFrame.cs 源码](https://github.com/vrchat-community/examples-image-loading/blob/main/Assets/_Project/Frame/SlideshowFrame.cs)
