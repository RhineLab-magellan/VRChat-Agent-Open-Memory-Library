---
title: String Loading - 远程字符串加载
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - json

aliases:
  - "String Loading - 远程字符串加载"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# String Loading - 远程字符串加载

> 来源: https://creators.vrchat.com/worlds/udon/string-loading/
> 抓取日期: 2026-06-15
> SDK: 3.2.3+ (VRCStringDownloader)
> 状态: ✅ FACT (官方文档)

---

## 概述

**String Loading** 允许从互联网**下载文本文件**并用于 VRChat 世界。

- **支持格式**: 任意文本格式(`.txt`、`.json` 等)
- **两种方式**:
  1. SDK 内置 `DownloadString` 脚本
  2. 用 `VRCStringDownloader.LoadUrl` 自己写

> **典型用例**: 动态加载配置(JSON)、文本内容、远端指令表等

---

## 关键限制(必读!)

### 1. Rate Limiting(限流)

> **5 秒/字符串** 的下载限制

- 超过限制 → 进入**队列**,**随机顺序**下载
- 全场景共享

### 2. 单文件最大 **100MB**

### 3. 队列上限 **1000 元素**

---

## Trusted URLs(白名单)

> **白名单外** 需用户在 VRChat 设置中开启 **"Allow Untrusted URLs"**

### 完整白名单

| 域名 | 用途 |
|---|---|
| `*.disbridge.com` | Disbridge |
| `*.github.io` | GitHub Pages |
| `gist.githubusercontent.com` | GitHub Gist |
| `pastebin.com` | Pastebin |
| `*.vrcdn.cloud` | VRCDN |

> **共享白名单**: `*.github.io` 和 `*.vrcdn.cloud` 同时在 **Image Loading** 白名单中
> 详细: `memory/world/udon/external-urls.md`

---

## 3 种使用方式

### 方式 1: SDK 内置 `DownloadString` 脚本(最简单)

1. 创建新 GameObject
2. 添加 `UdonBehaviour` 组件
3. 选择 **`DownloadString`** 作为 Program Source
4. 输入 URL
5. 选择要在哪个 Text 组件显示下载的文本

### 方式 2: 自定义 `VRCStringDownloader.LoadUrl`(灵活)

```csharp
using VRC.SDK3.StringLoading;
using VRC.Udon.Common.Interfaces;

VRCStringDownloader.LoadUrl(VRCUrl url, IUdonEventReceiver udonBehaviour);
```

**步骤**:
1. 调用 `LoadUrl` 传入 URL 和 UdonBehaviour
2. 等待 `OnStringLoadSuccess` 或 `OnStringLoadError` 事件
3. 通过 `IVRCStringDownload` 访问结果

### 方式 3: 自定义字节编码(高级)

> 通过 `ResultBytes` 访问原始字节 + 自定义 `System.Text.Encoding`

详见下方完整示例。

---

## 事件

### OnStringLoadSuccess

```csharp
public override void OnStringLoadSuccess(IVRCStringDownload result);
```

- **返回**: `IVRCStringDownload`
- **触发**: `LoadUrl` 成功从互联网下载字符串

### OnStringLoadError

```csharp
public override void OnStringLoadError(IVRCStringDownload result);
```

- **返回**: `IVRCStringDownload`
- **触发**: `LoadUrl` 下载失败

---

## 完整 API

### VRCStringDownloader(静态类)

```csharp
namespace VRC.SDK3.StringLoading
public static class VRCStringDownloader
```

#### LoadUrl

```csharp
public static void LoadUrl(
    VRCUrl Url,                       // 必需:URL
    IUdonEventReceiver UdonBehaviour  // 必需:接收事件的 UdonBehaviour
)
```

**关键提示**:
- **Udon Graph**: 默认为**当前 UdonBehaviour**
- **UdonSharp**: 必须使用 **`(IUdonEventReceiver)this`**

---

### IVRCStringDownload(结果)

| 方法 | 返回 | 说明 |
|---|---|---|
| `GetError()` | `string` | `OnStringLoadError` 的错误消息 |
| `GetErrorCode()` | `int` | HTTP 错误码 |
| `GetResultBytes()` | `byte[]` | **原始字节数组**(UTF-8 标准解码前)。**访问会返回数据副本** |
| `GetResult()` | `string` | UTF-8 解码后的字符串 |
| `GetUdonBehaviour()` | `UdonBehaviour` | 接收事件的 UdonBehaviour |
| `GetUrl()` | `VRCUrl` | 下载尝试的 URL |

---

## 完整示例

### 基础示例(UTF-8 + ASCII)

```csharp
using System.Text;
using UdonSharp;
using UnityEngine;
using VRC.SDK3.StringLoading;
using VRC.SDKBase;
using VRC.Udon.Common.Interfaces;

public class ResultBytesExample : UdonSharpBehaviour
{
    [SerializeField]
    private VRCUrl url;

    void Start()
    {
        VRCStringDownloader.LoadUrl(url, (IUdonEventReceiver)this);
    }

    public override void OnStringLoadSuccess(IVRCStringDownload result)
    {
        string resultAsUTF8 = result.Result;
        byte[] resultAsBytes = result.ResultBytes;
        string resultAsASCII = Encoding.ASCII.GetString(resultAsBytes);
        Debug.Log($"UTF8: {resultAsUTF8}");
        Debug.Log($"ASCII: {resultAsASCII}");
    }

    public override void OnStringLoadError(IVRCStringDownload result)
    {
        Debug.LogError($"Error loading string: {result.ErrorCode} - {result.Error}");
    }
}
```

### JSON 配置加载示例(高级)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.StringLoading;
using VRC.Udon.Common.Interfaces;
using VRC.SDK3.Data;  // VRCJson

public class ConfigLoader : UdonSharpBehaviour
{
    [SerializeField] private VRCUrl configUrl;
    [SerializeField] private UdonBehaviour targetSystem;  // 接收配置的 Udon 脚本

    void Start()
    {
        VRCStringDownloader.LoadUrl(configUrl, (IUdonEventReceiver)this);
    }

    public override void OnStringLoadSuccess(IVRCStringDownload result)
    {
        // 1. 解析为 DataToken
        DataToken json = VRCJson.TryParseFromString(result.Result);

        if (json.TokenType == TokenType.DataDictionary)
        {
            DataDictionary config = json.DataDictionary;

            // 2. 提取配置
            string worldName = config["name"].String;
            float maxPlayers = (float)config["maxPlayers"].Number;

            // 3. 通过 SetProgramVariable 传递给目标系统
            targetSystem.SetProgramVariable("worldName", worldName);
            targetSystem.SetProgramVariable("maxPlayers", maxPlayers);
            targetSystem.SendCustomEvent("OnConfigLoaded");
        }
    }

    public override void OnStringLoadError(IVRCStringDownload result)
    {
        Debug.LogError($"Config load failed: {result.Error}");
        // 使用缓存或硬编码默认配置
    }
}
```

> VRCJson + Data Containers 详细: `memory/world/data-containers.md` ⭐

---

## 关键设计模式

### 1. 链式下载(避免阻塞)

```csharp
private string[] _urlsToDownload;
private int _currentIndex = 0;

void Start()
{
    DownloadNext();
}

private void DownloadNext()
{
    if (_currentIndex >= _urlsToDownload.Length) return;
    var url = new VRCUrl(_urlsToDownload[_currentIndex]);
    VRCStringDownloader.LoadUrl(url, (IUdonEventReceiver)this);
}

public override void OnStringLoadSuccess(IVRCStringDownload result)
{
    ProcessString(result.Result);
    _currentIndex++;
    DownloadNext();  // 串行下载
}
```

### 2. 预上传默认配置 + 远端覆盖

```csharp
[SerializeField] private string _defaultConfig = "{\"name\":\"Default\"}";
[SerializeField] private VRCUrl _remoteConfigUrl;

void Start()
{
    // 1. 先用默认配置启动
    ApplyConfig(_defaultConfig);

    // 2. 尝试加载远端配置覆盖
    if (_remoteConfigUrl != null)
    {
        VRCStringDownloader.LoadUrl(_remoteConfigUrl, (IUdonEventReceiver)this);
    }
}

public override void OnStringLoadSuccess(IVRCStringDownload result)
{
    ApplyConfig(result.Result);  // 覆盖
}
```

### 3. 缓存 + TTL(避免重复下载)

```csharp
[SerializeField] private string _cachedConfig;
[SerializeField] private float _cacheTtlSeconds = 300f;  // 5 分钟
private float _lastLoadTime = -9999f;

void Start()
{
    if (Time.time - _lastLoadTime > _cacheTtlSeconds)
    {
        VRCStringDownloader.LoadUrl(_configUrl, (IUdonEventReceiver)this);
    }
    else
    {
        ApplyConfig(_cachedConfig);
    }
}
```

---

## 风险与陷阱

| 风险 | 等级 | 说明 |
|---|---|---|
| URL 白名单外 | 🔴 严重 | 用户需开启 "Allow Untrusted URLs" |
| 超过 5s/字符串 限流 | 🟡 中等 | 进入队列,顺序随机 |
| 100MB 单文件 | 🟡 中等 | 超出失败 |
| 1000 元素队列 | 🟡 中等 | 超出失败 |
| 错误处理缺失 | 🟡 中等 | 必须实现 `OnStringLoadError` |
| 同步假设 | 🟡 中等 | `OnStringLoadSuccess` 是**异步**的,不能假设立即可读 |
| `ResultBytes` 返回副本 | 🟡 中等 | 每次访问都复制,大量访问有性能成本 |
| VRChat 菜单打开时 | 🟢 低 | 输入/下载不受影响(只影响 Input) |

---

## 与知识库互补

- **External URLs + 白名单**: `memory/world/udon/external-urls.md` ⭐
- **Image Loading**: `memory/world/udon/image-loading.md` ⭐ 类似机制
- **Data Containers + VRCJson**: `memory/world/data-containers.md` ⭐ JSON 解析
- **Udon 事件**: `memory/api/events-reference.md` ⭐ OnStringLoad* 签名
- **Persistence**: `memory/api/persistence.md` ⭐ 与 String Loading 的取舍

---

## String Loading vs Persistence

| 维度 | String Loading | Persistence (PlayerData) |
|---|---|---|
| **数据来源** | 远端 URL(开发者控制) | 玩家本机(VRChat 平台) |
| **典型用途** | 配置、公告、远端指令 | 玩家进度、设置、所有权 |
| **可修改** | 仅开发者(更新 URL) | 玩家可修改 |
| **跨世界** | ✅ 同一 URL 跨世界生效 | ❌ 玩家数据 per-玩家 |
| **大小** | 100MB/字符串 | 100KB/玩家/世界(压缩后) |
| **速度** | 异步(可能数秒) | 同步(几乎瞬时) |
| **离线** | ❌ 需网络 | ✅ 始终可用 |

> 选哪个? 静态配置 → **String Loading**;玩家数据 → **Persistence**

---

## 相关 VRChat 官方文档

- [String Loading](/worlds/udon/string-loading) - 本页官方原版
- [External URLs](/worlds/udon/external-urls) - URL 白名单
- [Image Loading](/worlds/udon/image-loading) - 图片下载
- [Data Containers](/worlds/udon/data-containers/) - JSON 处理
