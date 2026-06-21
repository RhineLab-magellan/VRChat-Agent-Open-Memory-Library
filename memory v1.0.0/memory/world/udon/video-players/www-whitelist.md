# Video Player Allowlist - 视频白名单

> 来源: https://creators.vrchat.com/worlds/udon/video-players/www-whitelist
> 抓取日期: 2026-06-15
> 最后更新: 2024-12-11
> Domain: World / Udon / Video / Whitelist
> 状态: ✅ FACT (官方文档)
> 任务: task-17

---

## 概述

VRChat 视频播放器**默认只允许访问白名单内服务**的 URL。

> 🔴 **如果 URL 所在服务不在白名单内,视频不会播放,除非用户在 VRChat 设置中勾选 "Allow Untrusted URLs"。**

### ⚠️ Master 实例 "Allow Untrusted URLs" 问题

> **SDK 自带的示例视频播放器无法处理 Master 关闭 "Untrusted URLs" 的情况**——这会导致视频无法播放。
> **用户自建视频播放器**应修改 Udon 代码,将同步所有权**转移给请求视频的用户**,以绕过 Master 设置的影响。

---

## Allowlisted Services(白名单内服务)

> 以下服务**默认被信任**,白名单 URL 无需用户额外设置。

| Service | Domain | 备注 |
|---------|--------|------|
| **Akamai CDN** | `vod-progressive.akamaized.net` | 商业 CDN |
| **Facebook Video** | `*.facebook.com`,`*.fbcdn.net` | - |
| **Google Video** | `*.googlevideo.com` | - |
| **Hyperbeam** | `*.hyperbeam.com`,`*.hyperbeam.dev` | - |
| **Mixcloud** | `*.mixcloud.com` | 音频流媒体 |
| **NicoNico** | `*.nicovideo.jp` | 日本视频站 |
| **Soundcloud** | `soundcloud.com`,`*.sndcdn.com` | 音频流媒体 |
| **Topaz Chat** | `*.topaz.chat` | - |
| **Twitch.TV** | `*.twitch.tv`,`*.ttvnw.net`,`*.twitchcdn.net` | **直播流** |
| **VRCDN** | `*.vrcdn.live`,`*.vrcdn.video`,`*.vrcdn.cloud` | VRChat 自有 CDN |
| **Vimeo** | `*.vimeo.com` | 视频站 |
| **Youku** | `*.youku.com` | 优酷(中国) |
| **YouTube** | `*.youtube.com`,`youtu.be` | 视频站 |

### 重要限制

> 🔴 **资源必须位于服务的白名单域名中** —— 这意味着**短链接(redirect)不工作**!

例如:
- ✅ `https://www.youtube.com/watch?v=...` 直接播放
- ❌ `https://youtu.be/...` 是合法短链,但**仍属白名单范围**(`youtu.be` 已在表中)
- ❌ 任何非 `*.youtube.com` / `youtu.be` 域名的 YouTube 链接(第三方下载站等)→ 不工作

---

## 平台差异

### Android / Quest 强制 HTTPS

> **VRChat on Android will not play video if the host is not using HTTPS protocol.**

| 平台 | HTTP | HTTPS |
|------|------|-------|
| **PC** | ✅ (部分域名支持) | ✅ |
| **Quest (Android)** | ❌ **拒绝播放** | ✅ **必须** |

**实践建议**:**始终使用 HTTPS**,不要依赖 HTTP。

### YouTube URL 限制

| URL 形式 | 是否支持 | 备注 |
|---------|---------|------|
| `https://www.youtube.com/watch?v=XXX` | ✅ 推荐 | "watch" 形式 |
| `https://youtu.be/XXX` | ✅ | 短链形式(已在白名单) |
| YouTube Live 流 | ✅ (AVPro) | 仅 AVPro 后端,Quest 不支持 |
| YouTube Music | ❌ | 不支持 |
| 已删除 / 私有 / 受限视频 | ❌ | 取决于视频本身的访问权限 |
| **未公开** 视频 | ❌ | **必须公开** |
| **公开** 视频 | ✅ | **YouTube URL 必须为公开视频** |

### Vimeo 限制

| 账户类型 | URL 形式 | 是否支持 |
|---------|---------|---------|
| **Vimeo Basic** | 基础视频 URL | ✅ 免费 |
| **Vimeo Pro / Business** | 直链 | ✅ 付费 |

### 自有 Host / CDN

| 维度 | 说明 |
|------|------|
| **成本** | 付费,取决于 Provider |
| **链接形式** | 直链 `.mp4` / `.webm` 文件 |
| **限制** | 默认**不在白名单内**,用户必须启用 "Allow Untrusted URLs" |
| **推荐** | 使用 CDN(Amazon CloudFront、BunnyCDN)分发 |

> **CDN 提示**:CDN 服务通常**不在白名单中**(因其开放性),需用户启用 "Allow Untrusted URLs"。

---

## Twitch.TV 白名单特别说明

> ✅ **Twitch 在白名单内**(`*.twitch.tv`,`*.ttvnw.net`,`*.twitchcdn.net`)

- 直播流(`.m3u8`)→ 需使用 **AVPro 后端**(Unity VideoPlayer 不支持直播)
- Quest **不支持** Twitch 直播

---

## 完整域名白名单速查

| 域名 | PC | Quest | 备注 |
|------|----|----|------|
| `*.akamaized.net` (`vod-progressive.akamaized.net`) | ✅ | ⚠️ | Akamai CDN |
| `*.facebook.com`, `*.fbcdn.net` | ✅ | ⚠️ | Facebook Video |
| `*.googlevideo.com` | ✅ | ⚠️ | Google Video |
| `*.hyperbeam.com`, `*.hyperbeam.dev` | ✅ | ⚠️ | Hyperbeam |
| `*.mixcloud.com` | ✅ | ⚠️ | Mixcloud |
| `*.nicovideo.jp` | ✅ | ⚠️ | NicoNico |
| `*.topaz.chat` | ✅ | ⚠️ | Topaz Chat |
| `*.twitch.tv`, `*.ttvnw.net`, `*.twitchcdn.net` | ✅ | ❌ | Twitch (Quest 不支持直播) |
| `*.vrcdn.live`, `*.vrcdn.video`, `*.vrcdn.cloud` | ✅ | ✅ | VRCDN |
| `*.vimeo.com` | ✅ | ⚠️ | Vimeo |
| `*.youku.com` | ✅ | ⚠️ | 优酷 |
| `*.youtube.com`, `youtu.be` | ✅ | ❌ | YouTube |
| `soundcloud.com`, `*.sndcdn.com` | ✅ | ⚠️ | SoundCloud |
| **`twitch.tv`** (主域名直播) | ✅ | ❌ | 需 AVPro |
| **`bilibili.com`** | ⚠️ | ❌ | **不在白名单**!需 B 站特定格式 + Untrusted URLs |
| 自有 CDN (HTTPS) | ✅ | ✅ | 需 "Allow Untrusted URLs" |
| 自有 CDN (HTTP) | ✅ | ❌ | Quest 拒绝 |

> ⚠️ = "具体兼容性需测试,官方未明确"

---

## 不支持的服务(明确)

| 域名/服务 | 是否支持 | 备注 |
|----------|---------|------|
| `bilibili.com` | ❌ 默认 | B 站 API 需 `bilibili.com/video/BVxxxx` 形式,且**默认不在白名单** |
| `*.mp4` / `*.webm` 直链(白名单外) | ❌ 默认 | 需 "Allow Untrusted URLs" |
| HTTP 协议(非 HTTPS) | ❌ | Quest 完全拒绝 |
| 流媒体 RTMP | ❌ | VRChat 不支持 RTMP 协议 |
| HLS / DASH 自有源 | ⚠️ | 取决于域名是否在白名单 |

---

## VRCUrl 类与白名单关系

> **VRCUrl 是 Udon 访问外部 URL 的唯一方式**。详细 API 见 `memory/world/udon/external-urls.md`。

### 行为矩阵

| 场景 | URL 在白名单 | URL 不在白名单 |
|------|-------------|---------------|
| 用户在 input field 输入 `VRCUrl` | ✅ 允许 | ⚠️ 需 "Allow Untrusted URLs" |
| Udon 在运行时**前**声明 `VRCUrl`(Editor 预设) | ✅ 允许 | ⚠️ 需 "Allow Untrusted URLs" |

> 即:**白名单外的 URL,必须有用户在 VRChat 客户端设置中启用 "Allow Untrusted URLs"**。

### VRCUrl API 速查

| 方法 | 签名 | 说明 |
|------|------|------|
| `VRCUrl.Get()` | `string` | 获取 URL 字符串 |
| `VRCUrl.IsNullOrEmpty(VRCUrl)` | `static bool` | 判断是否为空 |
| `VRCUrl.Empty` | `static VRCUrl` | 空 URL 常量 |
| `VRCUrl(string)` | 构造函数 | **仅 Editor 可用** |

> Udon Type Exposure 状态: `VRCUrl` 暴露率 61.54% (8 个暴露成员),完整清单见 `memory/api/exposed-types.md`。

---

## 实践模式:Master Untrusted URLs 兼容

> **SDK 示例 Prefab 不处理此场景**。生产环境应实现 fallback。

### 推荐方案:所有权转移

```csharp
using UdonSharp;
using VRC.SDKBase;
using VRC.SDK3.Video.Components;

public class RobustVideoPlayer : UdonSharpBehaviour
{
    [SerializeField] private VRCUnityVideoPlayer video;
    [SerializeField] private VRCUrl defaultUrl;

    // 玩家请求播放时,先获取所有权
    public void OnPlayerRequestPlayURL(VRCUrl url)
    {
        VRCPlayerApi requestingPlayer = Networking.LocalPlayer;
        
        // 转移所有权给请求者
        if (!Networking.IsOwner(gameObject))
        {
            Networking.SetOwner(requestingPlayer, gameObject);
        }
        
        // 请求者播放
        video.PlayURL(url);
    }
    
    // 初始化时播放默认 URL
    public void Start()
    {
        video.PlayURL(defaultUrl);
    }
}
```

### 关键设计意图

- **Master 关 Untrusted URLs** → Master 自己无法加载非白名单 URL
- **所有权转移给请求者** → 请求者自己处理 Untrusted URLs 设置
- **请求者关 Untrusted URLs** → 视频不播放,但不影响其他玩家
- **请求者开 Untrusted URLs** → 该玩家正常观看

---

## 风险与时效

| 风险 | 说明 |
|------|------|
| **白名单可能变化** | 官方明确说明白名单**可能随时变更,不再另行通知** |
| **YouTube 政策** | Google 可能修改 YouTube 嵌入条件 |
| **Vimeo 政策** | Vimeo Pro/Business 政策可能变化 |
| **Twitch 嵌入** | Twitch 可能要求额外认证 |
| **Quest 硬件** | 老旧 Quest 设备硬解能力有限,可能播放失败 |
| **CDN 域名变更** | 自有 CDN 域名需长期维护 |
| **CORS 配置** | 自有 CDN 需正确配置 CORS,否则 Quest 拒绝 |

> **文档时效性警告**:本白名单**截至 2024-12-11 官方公布内容**。生产环境使用前应**检查最新白名单**(https://creators.vrchat.com/worlds/udon/video-players/www-whitelist)。

---

## 视频优化(白名单内服务的共通建议)

> **Web 优化(fast start)** 是提升加载速度的关键。

| 工具 | 操作 |
|------|------|
| **FFMPEG** | `-movflags +faststart` |
| **HandBrake** | 勾选 'Web Optimized' |

**原理**:
- 无 fast start:需下载**完整**视频后才能播放
- 有 fast start:可**分块流式传输**,立即开始播放

---

## 与已有知识库关联

| 知识库 | 关系 |
|--------|------|
| `memory/world/udon/video-players/index.md` | 父页面(Video Players 总览) |
| `memory/world/udon/external-urls.md` | VRCUrl 类 + 白名单基础 |
| `memory/world/udon/image-loading.md` | 4KB 图像白名单(参考) |
| `memory/world/udon/string-loading.md` | VRCStringDownloader 白名单(参考) |
| `memory/api/exposed-types.md` | VRCUrl 完整暴露 API |
| `memory/world/examples/udon-example-scene/udon-video-sync-player.md` | UdonSyncPlayer 实现 |
| `memory/FACT.md` → VVMW | 视频同步生产参考 |
| `memory/FACT.md` → AudioLink | 音频零网络同步参考 |

---

## 参见

- **Video Players 总览**: `memory/world/udon/video-players/index.md`
- **VRCUrl & External URLs**: `memory/world/udon/external-urls.md`
- **Udon Type Exposure Tree**: `memory/api/udon-type-exposure.md`
- **官方白名单原文**: <https://creators.vrchat.com/worlds/udon/video-players/www-whitelist>
