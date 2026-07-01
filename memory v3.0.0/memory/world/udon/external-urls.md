---
title: "External URLs - 外部 URL 与白名单"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - udonsharp
aliases:
  - "External URLs - 外部 URL 与白名单"
  - external-urls
related:
  - ai-navigation.md
  - debugging-udon-projects.md
  - image-loading.md
  - ui-events.md
  - vm-and-assembly.md
---
# External URLs - 外部 URL 与白名单

> 来源: https://creators.vrchat.com/worlds/udon/external-urls/
> 抓取日期: 2026-06-15
> 状态: ✅ FACT (官方文档)

---

## 概述

Udon 可使用**外部 URL** 加载远程内容。URL **必须**包装在 **`VRCUrl`** 对象中。

- **运行时输入**: 用户可通过 `VRCUrlInputField` 组件输入 URL
- **预定义**: 世界创建者可随世界一起上传预定义的 `VRCUrl`

---

## 🔒 Allowlist(白名单)机制

> **安全原因**,VRChat **限制**外部 URL 的使用方式

**默认行为**:`VRCUrl` **只能**在 **VRChat 域白名单**中访问。

**绕过方式**:用户可在 VRChat 设置中启用 **"Allow Untrusted URLs"**。

### 行为矩阵

| 场景 | 白名单内 | 白名单外 |
|---|---|---|
| 用户在 input field 输入 `VRCUrl` | ✔️ 允许 | ⚠️ 需要 "Allow Untrusted URLs" |
| Udon 在运行时**前**声明 `VRCUrl` | ✔️ 允许 | ⚠️ 需要 "Allow Untrusted URLs" |

---

## VRCUrl 类完整 API

```csharp
namespace VRC.SDKBase
public class VRCUrl
```

### 构造函数

| 名称 | 摘要 |
|---|---|
| `VRCUrl(string url)` | 接受 URL 字符串的构造函数。**仅在 Editor 时可调用!** |

### 属性

| Static | 类型 | 名称 | 摘要 |
|---|---|---|---|
| ✔️ | `VRCUrl` | `Empty` | 一个空 URL |

### 方法

| Static | 返回 | 名称 | 摘要 |
|---|---|---|---|
|  | `string` | `Get()` | 检索 URL 的当前字符串值 |
| ✔️ | `bool` | `IsNullOrEmpty(VRCUrl vrcUrl)` | 指示指定 VRCUrl 是否为 null 或引用空字符串("") |

---

## 关键约束(工程要点)

### 🔴 VRCUrl 构造函数仅在 Editor 可用!

```csharp
// ❌ 错误!  运行时构造 VRCUrl 失败
void Start()
{
    var url = new VRCUrl("https://example.com/image.png");  // Runtime 不可用
}
```

```csharp
// ✅ 正确!  在 Editor 中预定义 VRCUrl 字段
[SerializeField] private VRCUrl myImageUrl;  // 在 Inspector 中设置

void Start()
{
    var url = myImageUrl;  // 使用 Inspector 预定义的 VRCUrl
}
```

> 详细 Image Loading: `memory/world/udon/image-loading.md` ⭐ VRCImageDownloader 用法
> 详细 String Loading: `memory/world/udon/string-loading.md` ⭐ VRCStringDownloader 用法

### VRCUrlInputField: 用户运行时输入

- 是 `Unity UI` 组件,玩家可在 VRChat 中**直接输入 URL**
- 输入的 URL **不享受**白名单豁免(白名单外需用户开启 "Allow Untrusted URLs")

---

## 白名单域名(适用 Image + String Loading)

> **以下域名在白名单内**,用户**无需**开启 "Allow Untrusted URLs" 即可访问

### Image + String 通用

| 域名 | 用途 |
|---|---|
| `*.disbridge.com` | DisBridge |
| `*.github.io` | GitHub Pages |
| `*.vrcdn.cloud` | VRCDN |
| `assets.vrchat.com` | VRChat 资源 |

### Image 专用

| 域名 | 用途 |
|---|---|
| `dl.dropbox.com`, `dl.dropboxusercontent.com` | Dropbox |
| `*.github.io` | GitHub Pages |
| `images4.imagebam.com` | ImageBam |
| `i.ibb.co` | ImgBB |
| `images2.imgbox.com` | imgbox |
| `i.imgur.com` | Imgur |
| `i.postimg.cc` | Postimages |
| `i.redd.it` | Reddit |
| `pbs.twimg.com` | Twitter |
| `*.vrcdn.cloud` | VRCDN |
| `i.ytimg.com` | Ytimg |

### String 专用

| 域名 | 用途 |
|---|---|
| `*.disbridge.com` | Disbridge |
| `*.github.io` | GitHub Pages |
| `gist.githubusercontent.com` | Github Gist |
| `pastebin.com` | Pastebin |
| `*.vrcdn.cloud` | VRCDN |

---

## Rate Limiting(限流)

> **关键限制**:**每个 URL 每 5 秒只能下载一次** (Image + String 都一样)

- 超出限制 → 下载**进入队列**,**随机顺序**下载
- **每场景** 1000 个元素队列上限
- Image 限制 Input/Output 缓冲区 32MB
- String 限制 100MB 单文件

---

## 安全最佳实践

### 1. 使用白名单内域名

```csharp
// ✅ 推荐 - GitHub Pages 白名单内
[SerializeField] private VRCUrl configUrl = new VRCUrl("https://username.github.io/config.json");
```

### 2. 始终处理错误

```csharp
public override void OnStringLoadError(IVRCStringDownload result)
{
    Debug.LogError($"URL load failed: {result.Error} (code: {result.ErrorCode})");
    // 使用缓存值或默认值
    UseFallbackConfig();
}
```

### 3. 不要在运行时创建 VRCUrl

```csharp
// ❌ 错误
void OnEnable() { var url = new VRCUrl(inputField.text); }

// ✅ 正确 - 通过 VRCUrlInputField 组件获取
public void OnInputChanged()
{
    // VRCUrlInputField 内部已处理 VRCUrl 构造
    var url = vrcUrlInputField.GetUrl();
}
```

### 4. 考虑灰度发布

```csharp
// 关键内容应**预上传**到世界(不依赖运行时 URL)
[SerializeField] private VRCUrl defaultConfig;  // 默认配置随世界发布
// 运行时可选地从 URL 更新
```

---

## 风险与限制

| 风险 | 等级 | 说明 |
|---|---|---|
| `new VRCUrl(string)` 在 Runtime | 🔴 严重 | **Editor Only**!Runtime 调用失败 |
| 白名单外 URL | 🟡 中等 | 需要用户开启 "Allow Untrusted URLs" |
| 限流触发 | 🟡 中等 | 5s/URL,超出进入队列(随机顺序) |
| 域名变更 | 🟡 中等 | 白名单官方可能调整 |
| 32MB 缓冲区(Image) | 🟡 中等 | 大图会失败 |
| 100MB 单文件(String) | 🟡 中等 | 超出失败 |

---

## 与知识库互补

- **Image Loading**: `memory/world/udon/image-loading.md` ⭐ VRCImageDownloader
- **String Loading**: `memory/world/udon/string-loading.md` ⭐ VRCStringDownloader
- **UI Events**: `memory/world/udon/ui-events.md` ⭐ VRCUrlInputField 在 UI 事件白名单内
- **Udon 事件**: `memory/api/events-reference.md` ⭐ OnStringLoad* 事件

---

## 相关 VRChat 官方文档

- [External URLs](/worlds/udon/external-urls) - 本页官方原版
- [Image Loading](/worlds/udon/image-loading) - 图像下载详细
- [String Loading](/worlds/udon/string-loading) - 字符串下载详细
