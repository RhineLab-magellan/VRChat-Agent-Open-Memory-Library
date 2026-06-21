---
title: VizVid (VVMW) — 案例研究型参考工程
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - source
  - sync
  - audio
  - video
  - pickup

aliases:
  - "VizVid (VVMW) — 案例研究型参考工程"

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: 1.7.5 (2026-05-02)
last_review: 2026-06-21
confidence: Medium
---
# VizVid (VVMW) — 案例研究型参考工程

> Tier: B（高质量开源项目，VRChat 生态最流行的视频播放器）
> 双重身份: **A2 案例研究型** + **C16 工具使用指南型**（互补）
> 项目官方名: **VizVid** (仓库名 VVMW)
> 项目类型: VRChat World 多人视频同步播放器
> 项目形态: Unity Prefab + UdonSharpBehaviour 套件（多模块）
> SDK 目标: VRChat SDK 3.x
> 仓库: https://github.com/JLChnToZ/VVMW
> 作者: JLChnToZ (https://xtl.booth.pm/)
> 许可: VRChat 生态通用开源许可（参见仓库 LICENSE）
> 当前版本: **1.7.5 稳定版** (2026-05-02)
> Stars: 169
> VPM 仓库: `https://xtlcdn.github.io/vpm/`
> 最后查看: 2026-06-20

> **🔄 双重身份说明**：
> - **A2 案例研究型**（本文件）：分析项目架构与时间同步算法 → 沉淀"Manual Sync + Owner Authority + 时间同步算法"到 `memory/FACT.md`
> - **C16 工具使用指南型**（`memory/world/vvmw.md`）：作为可推荐工具，含 VPM 仓库 / 模块清单 / 安装教程 / 9 大功能
> - 两者互补：模式层给创作者"理解原理"，工具层给创作者"直接拿来用"

---

## 项目概述

**VizVid (VVMW)** 是 VRChat 创作者生态中**最受欢迎的多人同步视频播放器**之一，由 JLChnToZ 维护。从 1.0.x 持续迭代到 1.7.5，覆盖：

- 🎬 VOD 视频（YouTube / Vimeo / Twitch / 自有 CDN）
- 📡 直播流（RTSP / RTMP / YouTube Live / Twitch Live）
- 🖼️ PNG/JPEG 图片查看
- 🎵 AudioLink 集成
- 💡 LTCGI 集成
- 🌟 VRC Light Volumes 集成
- 🔒 Udon Auth 锁定 UI
- 🌍 12+ 语言本地化

**双重价值**：
- **作为工具**：5 大模块、4 种显示模式、PC/Quest 跨平台，World 视频/直播/活动现场"开箱即用"
- **作为案例**：时间同步算法（服务器时间锚点 + 阈值触发 + 延迟补偿 + Performer 模式）是 VRChat 生态最完善的多人音视频同步实现

**核心设计哲学**：
- 三层职责分离: 主控制器 / 前端处理器 / 播放后端抽象
- 多种播放器后端可插拔: Unity VideoPlayer / AVPro / Image Viewer
- 完整 Manifest 同步: 视频 URL + 状态 + 时间 + 速度 + 循环范围
- 完整事件体系: Interact / Region / Pickup / Stream Key

## 项目结构（公开 Releases 推断 + README 关键组件）

```
VVMW/ (Packages/idv.jlchntoz.vvmw/)
├── VVMW (Game Object)                  ← 主控制器
│   ├── VideoCore (UdonSharpBehaviour)  ← 状态机 + 同步核心
│   ├── FrontendHandler                 ← 播放列表 / 队列 / 历史
│   └── Handler (Builtin/AVPro/Image)   ← 播放后端抽象
│
├── Builtin Module                      ← Unity VideoPlayer 后端
│   └── VRCUnityVideoPlayer 包装
│
├── AVPro Module                        ← AVPro 商业插件后端
│   └── VRCAVProVideoPlayer 包装
│
├── Image Module                        ← PNG/JPEG 图片查看
│
├── Playlist Queue Handler              ← 预设播放列表 + 队列
│
├── Locale                              ← 12+ 语言自动检测
│
├── Rate Limit Resolver                 ← VRChat 5s/URL 限流智能调度
│
├── Default Screen / Screen             ← 内置屏幕 Prefab
│
├── Default Audio Source                ← 音频源配置（多通道支持）
│
├── Default UI / Screen with Overlay    ← 内置 UI Prefab
│
├── Topaz Chat / CDN                    ← 直播流服务集成
│
└── Udon Auth 锁定 UI                   ← 第三方 Udon Auth 集成
```

**关键事实**：
- 1.3.0+ 拆出 `vrcw-foundation`（基础模块独立仓库）
- 模块化设计：屏幕 / 音频 / UI 三者**解耦**，支持多实例

## 三大同步模式（核心创新点）

| 模式 | 适用场景 | 同步主体 | 持久化 |
|------|---------|---------|--------|
| **Local Mode** | 单玩家本地预览 | 不同步 | 否 |
| **Global Sync** | 全员同步（默认） | Manual + Owner Authority | 否（可选 PlayerData） |
| **Local Mode + Upload** | 上传 URL 前本地预览 | 临时不同步 | 否 |

**主控制器 (VideoCore) 状态机**:
```
Idle → Loading → Playing → Paused
                  ↑
                  └── Abort
```

## 核心设计模式（已沉淀到 patterns/ + FACT.md）

| # | 模式 | 出处 | 沉淀 |
|---|------|------|------|
| 1 | **Manual Sync + Owner Authority** | `VideoCore.cs` | `memory/FACT.md` §视频播放器 + `patterns/manual-sync-state.md` |
| 2 | **服务器时间锚点** | `CalcSyncTime()` | `memory/FACT.md` §视频播放器 |
| 3 | **阈值同步** | `timeDriftDetectThreshold = 0.9F` | `memory/FACT.md` §视频播放器 |
| 4 | **冷却期防同步风暴** | `OWNER_SYNC_COOLDOWN_TICKS = 3s` | `memory/FACT.md` §视频播放器 |
| 5 | **双缓冲状态分离** | `localXxx` + `[UdonSynced] xxx` | `memory/FACT.md` §视频播放器 + `patterns/dual-copy-variables.md` |
| 6 | **Performer 模式延迟补偿** | `PerformerLatency` | `memory/FACT.md` §视频播放器 |
| 7 | **播放后端抽象（Strategy 模式）** | `Handler` 接口 | `memory/patterns/strategy-pattern-udon.md` |
| 8 | **字符串拼接避冲突** | `\u2029` Paragraph Separator | `memory/patterns/data-encoding-tricks.md` |

## 9 大功能特性

| # | 特性 | 实现版本 | 价值 |
|---|------|----------|------|
| 1 | 基础播放/快进/暂停 | 1.0+ | 标配 |
| 2 | 预设播放列表 + 用户队列 | 1.0+ | Watch-together 核心 |
| 3 | 玩家输入 URL 历史记录 | 1.0.32+ | 玩家体验 |
| 4 | Quest 跨平台 URL | 1.0+ | PC/Quest 双兼容 |
| 5 | PNG/JPEG 图片查看 | 1.0.37+ | 通用场景 |
| 6 | 低延迟模式（RTSP/RTMP） | 1.0+ | 直播表演 |
| 7 | 播放速度调节 | 1.1.0+ | 教学/演示 |
| 8 | 智能请求调度防 5s 限流 | 1.1.0+ | 关键稳定性 |
| 9 | 本地模式（脱机预览） | 1.0+ | 单人模式 |

## 9 大集成生态

| 集成 | 用途 | 价值 |
|------|------|------|
| **AudioLink** | 视频音频自动切换到 AudioLink 源 | 音频可视化 |
| **LTCGI** | 提供 CustomRenderTexture 视频输出 | 屏幕反射/折射 |
| **VRC Light Volumes** | 视频播放联动动态光照 | 沉浸感 |
| **Topaz Chat** | 直播流服务 | 现场表演 |
| **Udon Auth** | 锁定 UI 防止误操作 | 权限控制 |
| **YTTL** | 显示视频标题 | 视频来源追踪 |
| **AVPro** | 商业视频插件后端 | 直播流 + 7.1 音频 |
| **Udon Auth** | UI 权限锁定 | 主持人/观众分级 |
| **PlayerData** | 持久化（可选） | 跨实例恢复 |

## 4 种显示模式（自定义 Shader）

| 模式 | 用途 |
|------|------|
| **Stretch** | 拉伸填满屏幕（默认） |
| **Contain** | 保持比例黑边 |
| **Cover** | 保持比例裁剪 |
| **Stereographic Video Source** | 立体 VR 视频（左右/上下） |

## 13+ 个 Releases 演进

| 版本 | 日期 | 关键更新 |
|------|------|----------|
| 1.0+ | — | 基础播放 + AVPro + 直播 + 本地模式 |
| 1.0.32 | — | 播放历史 + TMP 支持 |
| 1.0.37 | — | PNG/JPEG 图片查看 |
| 1.1.0 | — | 播放速度 + 智能请求调度 |
| 1.3.0 | — | 跨平台双输入框 + Stream Key 分配器 |
| 1.4.x | 2025-12 ~ 2026-01 | YT-DLP 优化 + Fallback 流程 + 多语言 |
| 1.5.0 ~ 1.5.3 | 2026-02 | 12 种语言 + AB loop 准备 + Fullscreen 解锁 |
| **1.6.0** | **2026-04-08** | **AB loop + Fullscreen 解锁模式** |
| **1.7.0-beta.1** | **2026-04-13** | **Active region 支持 auto mute / auto play / AudioLink 注册 / broadcast texture** |
| **1.7.1 ~ 1.7.4** | **2026-04 ~ 2026-05** | **bug 修复 + overlay UI 持续打磨** |
| **1.7.5** | **2026-05-02** | **当前稳定版 — 1.7 系列最终稳定 + 1.7.0-beta 引入特性 GA** |

## 工程评价

| 维度 | 评分 | 说明 |
|------|------|------|
| **设计质量** | ⭐⭐⭐⭐⭐ | 三层职责分离 + 多后端抽象 + 模块化解耦 |
| **工程深度** | ⭐⭐⭐⭐⭐ | 时间同步算法是 VRChat 生态最完善实现 |
| **可复用性** | ⭐⭐⭐⭐⭐ | 拖 Prefab 即用，5 大模块可独立配置 |
| **可维护性** | ⭐⭐⭐⭐☆ | 模块化清晰，但 PlayerData 持久化路径较复杂 |
| **Creator 友好** | ⭐⭐⭐⭐⭐ | Screen Configurator 组件 + 双 Inspector |
| **Quest 适配** | ⭐⭐⭐⭐⭐ | 双输入框 + Quest 独立 URL 字段 + 硬件限制兼容 |
| **文档/注释** | ⭐⭐⭐⭐☆ | README 完整 + 详细 Bundle 说明 |
| **测试覆盖** | ⭐⭐⭐☆☆ | Editor 集成较好，但缺单元测试 |
| **生态集成** | ⭐⭐⭐⭐⭐ | 9 大集成（AudioLink/LTCGI/VRCLightVolumes/Topaz/UdonAuth/YTTL）|
| **更新频率** | ⭐⭐⭐⭐⭐ | 2-4 周一个版本，长期活跃维护 |

## 对创作者的建议

✅ **直接使用**：
- 拖 Prefab 即可，5 大模块按需启用
- 适合 1-2 年 Udon 经验创作者

✅ **作为学习模板**：
- Manual Sync + Owner Authority 正确用法
- 时间同步算法（服务器时间锚点 + 阈值触发 + 延迟补偿）
- 多后端抽象（Strategy 模式在 Udon 中的实现）
- 5s URL 限流的智能调度
- 模块化解耦（屏幕/音频/UI 独立）

⚠️ **谨慎魔改**：
- 不要改 VideoCore 主控制器（同步逻辑复杂）
- 不要改 Handler 接口（影响多后端兼容）
- 建议做"周边扩展"或"独立 Prefab"而非"核心改造"

## 沉淀记录

### 已沉淀到知识库
- `memory/FACT.md` §视频播放器时间同步算法模式（2026-06-06）
- `memory/patterns/manual-sync-state.md` Manual Sync 规范
- `memory/world/udon/video-players/index.md` 视频播放器总览（已引用 VVMW）
- `memory/sources/open-source-projects.md` A2 案例研究

### 知识优先级
L3 社区标准（VRChat 生态最流行的视频播放器之一）

## 知识溯源

- 源码: https://github.com/JLChnToZ/VVMW
- Releases: https://github.com/JLChnToZ/VVMW/releases
- README: https://github.com/JLChnToZ/VVMW/blob/develop/README.md
- Bundle 详细说明: https://github.com/JLChnToZ/VVMW/blob/main/Packages/idv.jlchntoz.vvmw/README.md
- 提取日期: 2026-06-20
- 提取方式: README + CHANGELOG + 13 个 Releases 分析
- 分析者: VRChat Technical Architect Agent (CherryClaw)
