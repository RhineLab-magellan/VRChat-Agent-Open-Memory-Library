# Video Players - VRChat 视频播放器

> 来源: https://creators.vrchat.com/worlds/udon/video-players/
> 抓取日期: 2026-06-15
> 最后更新: 2024-08-06
> Domain: World / Udon / Video
> 状态: ✅ FACT (官方文档)
> 任务: task-17

---

## 概述

VRChat 允许在世界(Udon World)中通过 SDK 提供的 **视频播放器组件** 播放视频。SDK 提供两个核心组件:

| 组件 | 命名空间 | 后端 |
|------|---------|------|
| `VRCUnityVideoPlayer` | `VRC.SDK3.Video.Components` | Unity VideoPlayer (原生) |
| `VRCAVProVideoPlayer` | `VRC.SDK3.Video.Components.AVPro` | AVPro 插件(商业) |

> **重要约束**:两个组件的运行时行为、平台兼容性和功能支持**不同**,选型时必须明确后端类型。

---

## 社区 Prefab 推荐

VRChat 官方不维护视频播放器 Prefab,但社区有三个主流实现:

| Prefab | 后端 | 说明 |
|--------|------|------|
| **VideoTXL** | 自实现 | 轻量级视频播放器 |
| **ProTV** | AVPro | 完整电视系统(含频道切换、画质调节) |
| **USharpVideo** | Unity | U# 实现,适合简单场景 |

> 推荐起点:从 SDK 自带的 `UdonSyncPlayer (AVPro).prefab` / `UdonSyncPlayer (Unity).prefab` 学起,再根据需求选择社区方案。

---

## SDK 自带 Prefab

> 路径: `Packages/VRChat SDK - Worlds/Samples/UdonExampleScene/Prefabs/VideoPlayers/`

包含两个 Prefab:

| Prefab | 后端 | 特点 |
|--------|------|------|
| `UdonSyncPlayer (AVPro).prefab` | AVPro | 支持**直播流** |
| `UdonSyncPlayer (Unity).prefab` | Unity | 编辑器内可播放 |

### 关键限制

> **示例 Prefab 默认关闭循环**(`loop = false`),以保证同步正确性。
> 若需循环播放: 启用 `Loop` 字段 → **移除 UdonBehaviour** → 失去同步功能。

### UdonSyncPlayer 是"同步示例",非强制

- 不需要"同步所有人看同一视频" → 可**仅用 VRC Video Player 组件**(不挂 UdonBehaviour)
- 需要同步 → 使用 `UdonSyncPlayer` 提供的同步图,**或基于其实现自己的同步**

详见: `memory/world/examples/udon-example-scene/udon-video-sync-player.md`

---

## 选型决策:AVPro vs Unity VideoPlayer

| 维度 | VRCUnityVideoPlayer | VRCAVProVideoPlayer |
|------|---------------------|---------------------|
| **PC 支持** | ✅ | ✅ |
| **Quest 支持** | ✅ | ❌ |
| **直播流(YouTube Live / Twitch)** | ❌ | ✅ |
| **编辑器内可播放** | ✅ Play Mode 即可 | ❌ 必须 Build & Test |
| **.mp4 / .webm 直链** | ✅ | ✅ |
| **YouTube/Vimeo 嵌入** | 仅客户端(Editor 不行) | 仅客户端(Editor 不行) |
| **音频通道数** | 2 (Stereo) | 6 (5.1,声称 8 但实际仅 6) |
| **PCVR 7.1 音频 (EAC3)** | ❌ | ✅ 仅 PCVR |
| **价格** | 免费 (Unity 内置) | 商业插件,需购买 |

### 选型建议

```
仅 PC + 需要直播流(YouTube Live / Twitch)  → AVPro
PC + Quest + 简单 VOD 视频                  → Unity VideoPlayer
需要 5.1 / 7.1 音频                         → AVPro (PC) / Unity (Quest,仅 Stereo)
优先编辑器内调试                            → Unity VideoPlayer
```

---

## Android / Quest 兼容性

> **过去**:Quest 没有 URL 解析器(URL resolver),需要高级用户手写 workaround。
> **现在**:VRChat 客户端在 Android/Quest 上**也内置了 URL 解析器**,无需 workaround。

**重要事实**:

- 同一个世界可以在 PC 和 Quest 上同时运行
- 视频 URL 通过 `VRCUrl` 字段传递给组件
- **Quest 上的视频白名单独立维护**(见 `www-whitelist.md`)

---

## ⚠️ Rate Limiting(频率限制)

> **同一用户** 全局每 5 秒**只能发起 1 个新的视频 URL 请求**(跨所有视频播放器)。

| 场景 | 行为 |
|------|------|
| 单一视频播放器 | 5s 限制通常不构成问题 |
| 多个视频播放器 | 必须保证请求间隔 ≥ 5s |
| **迟加入者** | 加入时若有 N 个视频正在播放,需在 ≥ 5s 间隔内发送 N 个 URL 请求 |
| **默认 URL** | 也受 5s 限制约束 |

### 实践建议

```csharp
// ❌ 错误:连续触发多个视频请求
public void PlayVideo1() { player1.PlayURL(url1); }
public void PlayVideo2() { player2.PlayURL(url2); }  // 失败!

// ✅ 正确:错开 5 秒以上
public void PlayMultiple() {
    player1.PlayURL(url1);
    SendCustomEventDelayedSeconds(nameof(PlaySecondVideo), 6f);
}
public void PlaySecondVideo() { player2.PlayURL(url2); }
```

---

## Unity VideoPlayer 集成(UdonSharp)

### 最小可运行示例

```csharp
using UnityEngine;
using UdonSharp;
using VRC.SDKBase;
using VRC.SDK3.Video.Components;
using VRC.SDK3.Components;

public class VideoController : UdonSharpBehaviour
{
    [SerializeField] private VRCUnityVideoPlayer unityVideo;
    [SerializeField] private VRCUrl videoUrl;  // Editor 预定义,运行时不可 new VRCUrl()

    public void Interact()  // 玩家交互触发
    {
        unityVideo.PlayURL(videoUrl);
    }

    public void StopVideo()
    {
        unityVideo.Stop();
    }
}
```

### Udon Type Exposure 注意

> **VRCUnityVideoPlayer 暴露的 API 必须在白名单中**,详细清单见 `memory/api/exposed-types.md` 和 `memory/api/udon-type-exposure.md`。

主要暴露方法(以 SDK 3.10.3 为例):

| 方法 | 用途 |
|------|------|
| `PlayURL(VRCUrl)` | 加载并播放 URL |
| `LoadURL(VRCUrl)` | 仅加载,不播放 |
| `Play()` | 播放(已加载) |
| `Pause()` | 暂停 |
| `Stop()` | 停止 |
| `SetTime(float)` | 跳转到指定时间(秒) |
| `GetTime()` | 获取当前播放时间 |
| `GetDuration()` | 获取视频总时长 |

---

## AVPro 集成(UdonSharp)

```csharp
using UnityEngine;
using UdonSharp;
using VRC.SDKBase;
using VRC.SDK3.Video.Components.AVPro;

public class AVProVideoController : UdonSharpBehaviour
{
    [SerializeField] private VRCAVProVideoPlayer avproVideo;
    [SerializeField] private VRCUrl streamUrl;  // YouTube Live / Twitch 流

    public void PlayStream()
    {
        // AVPro 支持 YouTube Live / Twitch 直播流
        avproVideo.PlayURL(streamUrl);
    }
}
```

### 音频通道说明

> **⚠️ AVPro speaker 组件错误地声称支持 8 通道音频**。
> 实际**只支持 6 通道 (5.1)**。
> **[AVPro 在 PCVR 上支持 EAC3 7.1 音频]**

---

## 视频源类型对比

| 视频源 | PC | Quest | 同步 | 备注 |
|--------|----|----|------|------|
| **Unity VideoPlayer** | ✅ | ✅ | 需自实现 | 原生,简单场景 |
| **AVPro 插件** | ✅ | ❌ | 需自实现 | 商业插件,需单独购买 |
| **YouTube URL** | ✅ | ❌ | URL 同步 + 时间同步 | 域名白名单 |
| **Vimeo URL** | ✅ | ❌ | URL 同步 + 时间同步 | 域名白名单 |
| **Twitch URL** | ✅ | ❌ | URL 同步 + 时间同步 | 域名白名单 |
| **本地 VideoClip** | ✅ | ✅ | 需自实现 | 推荐方案,无需网络 |
| **自有 CDN (HTTPS)** | ✅ | ✅ | URL 同步 + 时间同步 | 需 CORS 配置 |

---

## 视频源平台差异

| 维度 | PC | Quest |
|------|----|----|
| 视频解码器 | 硬件 + 软件 | **仅硬件(受限)** |
| 最大分辨率 | 4K | 1080p (推荐 720p) |
| 视频格式 | MP4 / WebM / MOV | MP4 (H.264) |
| 流媒体 | 支持 | 受限(部分域名不可用) |
| 视频后端 | AVPro / Unity VideoPlayer | **仅 Unity VideoPlayer** |
| 协议 | HTTP / HTTPS | **必须 HTTPS** |

> **Quest 强制 HTTPS**:VRChat Android 客户端**拒绝播放非 HTTPS 协议的 URL**。

---

## 视频 URL 与 VRCUrl

```csharp
using VRC.SDKBase;

// ✅ Editor 预定义 VRCUrl(运行时唯一可用方式)
[SerializeField] private VRCUrl myVideoUrl;  // Inspector 设置

// ✅ 运行时使用
public void Play() {
    videoPlayer.PlayURL(myVideoUrl);  // 传入 VRCUrl
}

// ❌ 错误! VRCUrl 构造函数仅在 Editor 可用
public void Start() {
    var url = new VRCUrl("https://...");  // Runtime 失败!
}
```

> 完整 `VRCUrl` API 详见 `memory/world/udon/external-urls.md`。

---

## 视频同步模式

`UdonSyncPlayer` 使用 **Manual Sync + Vector2 时间戳**(详见 `udon-video-sync-player.md`):

```
URL 同步:Variable Change 事件触发(单次)
时间同步:周期性 Vector2 同步(可选,频率可调)
服务器时间锚点:Networking.GetServerTimeInSeconds()
```

**生产级参考**: `memory/FACT.md` 中**视频播放器时间同步算法模式(参考工程)** —— VRChat 社区最完善的音视频同步实现。

| 模式 | 来源 | 特点 |
|------|------|------|
| **简单同步** | `UdonSyncPlayer` Prefab | URL + Vector2 时间戳 |
| **生产级同步** | 视频播放器(参考工程) | 服务器时间锚点 + 阈值触发 + 延迟补偿 + Performer 模式 |
| **多机位同步** | 多机位导演系统(参考工程) | NetworkCallable RPC + 双缓冲 |

---

## 视频优化(Encoding Best Practices)

> **强烈建议** 上传 web 优化版视频。

### MP4 Fast Start

| 工具 | 操作 |
|------|------|
| **FFMPEG** | 添加参数 `-movflags +faststart` |
| **HandBrake** | 勾选 'Web Optimized' 复选框 |
| **其他编码器** | 查找 "fast start" / "web optimized" 选项 |

### 原理

- **未启用 fast start**:客户端必须下载**整个**视频文件后才能开始播放
- **启用 fast start**:视频可**分块流式传输**,首屏加载后立即开始播放

```bash
# FFMPEG 示例
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

---

## 风险与版权

> ⚠️ **视频内容涉及版权问题**。VRChat 视频播放器**不规避版权保护**。

| 风险 | 说明 |
|------|------|
| **版权侵权** | 播放未授权视频可能导致世界被举报/下架 |
| **YouTube 政策** | Google 可能随时更改 YouTube 嵌入策略 |
| **Vimeo 政策** | Vimeo Pro/Business 账户政策可能变化 |
| **域名白名单** | 平台可能随时调整白名单 |
| **Quest 硬件限制** | 老旧 Quest 设备可能无法硬解 1080p |

### 合规建议

- **自制内容** 或获得明确授权
- 使用自有 CDN 存放**已授权**视频
- 避免在公开世界使用未授权影视内容

---

## 与已有知识库关联

| 知识库 | 关系 |
|--------|------|
| `memory/world/udon/external-urls.md` | VRCUrl + 白名单基础 |
| `memory/world/examples/udon-example-scene/udon-video-sync-player.md` | UdonSyncPlayer 完整实现 |
| `memory/world/sdk-prefabs.md` | 8 个 SDK Prefab 总览 |
| `memory/api/exposed-types.md` | U# 类型暴露完整清单(查 VRCUnityVideoPlayer / VRCAVProVideoPlayer) |
| `memory/api/udon-type-exposure.md` | Type Exposure 索引 |
| `memory/api/networking.md` | Manual Sync 规范 |
| **`memory/FACT.md` → 视频播放器时间同步算法模式(参考工程)** | **生产级视频同步参考** |
| `memory/FACT.md` → 音频同步系统(参考工程) | 音频同步(无网络)参考 |
| `memory/world/udon/networking/` | 网络同步基础 |
| `memory/patterns/manual-sync-state.md` | Manual Sync 模式 |

---

## 参见

- **Video Player Allowlist**: `memory/world/udon/video-players/www-whitelist.md`
- **Udon Video Sync Player 示例**: `memory/world/examples/udon-example-scene/udon-video-sync-player.md`
- **VRCUrl & External URLs**: `memory/world/udon/external-urls.md`
- **视频播放器时间同步算法模式(参考工程)**: `memory/FACT.md` (6. Manual Sync + Owner Authority)
- **社区 Prefab**:
  - VideoTXL: <https://github.com/Superbstom/VideoTXL>
  - ProTV: <https://github.com/Polar-Pumpkin/ProTV>
  - USharpVideo: <https://github.com/MerlinVR/USharpVideo>
