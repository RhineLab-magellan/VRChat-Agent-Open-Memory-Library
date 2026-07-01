---
title: "VizVid (VVMW) — VRChat 多功能视频播放器"
category: world
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: "1.7.5 (2026-05-02)"
last_review: 2026-06-21
confidence: Medium
tags:
  - world
  - sync
  - audio
  - video
  - light
aliases:
  - "VizVid (VVMW) — VRChat 多功能视频播放器"
  - vvmw
related:
  - "sources/vvmw.md"
  - "world/udon/video-players/index.md"
  - "world/udon/video-players/www-whitelist.md"
  - "hybrid/audio-link.md"
  - "world/vrc-light-volumes.md"
  - FACT.md
  - "patterns/manual-sync-state.md"
  - "world/udon/external-urls.md"
  - "api/persistence.md"
  - "world/performance-guide.md"
  - "hybrid/udon-world-plugins.md"
---
# VizVid (VVMW) — VRChat 多功能视频播放器

> 来源: https://github.com/JLChnToZ/VVMW
> 作者: JLChnToZ (https://xtl.booth.pm/)
> 当前版本: **1.7.5 稳定版** (2026-05-02)
> Stars: 169
> 许可: VRChat 生态通用开源许可
> 沉淀日期: 2026-06-20
> 类别: 3D Props / World / VRChat / Video Player
> 双重身份: **A2 案例研究型** + **C16 工具使用指南型**

---

## 概述

**VizVid (VVMW)** 是 VRChat 创作者生态中**最受欢迎的多人同步视频播放器之一**，由 JLChnToZ 维护。从 1.0.x 持续迭代到 1.7.5，覆盖 VOD 视频、直播流、图片查看、AudioLink 集成、LTCGI 集成、VRC Light Volumes 集成等场景。

**核心优势**：
- **多后端可插拔**：Unity VideoPlayer / AVPro / Image Viewer 三种后端自由切换
- **多人同步成熟**：服务器时间锚点 + 阈值触发 + 延迟补偿，VRChat 生态最完善实现
- **PC/Quest 跨平台**：双输入框 + Quest 独立 URL 字段 + 硬件限制兼容
- **5 大模块解耦**：屏幕 / 音频 / UI 独立配置，支持多实例
- **9 大集成生态**：AudioLink / LTCGI / VRCLightVolumes / Topaz / UdonAuth / YTTL / PlayerData
- **12+ 语言本地化**：EN/ZH/JA/KO/FR/DE/IT/ES/PT/PL/RU/UK/HE/TH
- **稳定活跃维护**：2-4 周一个版本，长期活跃

> **对 Agent 的意义**：该播放器已沉淀出 8 个**通用 Udon 模式**（Manual Sync + Owner Authority + 时间同步算法 + 阈值同步 + 冷却期 + 双缓冲 + Performer + Strategy），
> 同时也是**工具使用指南型参考工程**（C16）。两层身份互补：模式层给创作者"理解原理"，工具层给创作者"直接拿来用"。

---

## 适用场景

✅ **直接推荐场景**：
- 🎬 多人观影（Watch-together）World（影院、客厅、咖啡厅）
- 📡 直播表演 World（演唱会、DJ 现场、VTuber 活动）
- 🖼️ 艺术展示 World（图片幻灯片、画展）
- 🎓 教学演示 World（视频教程、演讲）
- 🎮 游戏厅 World（视频背景 + 游戏 UI）
- 🏢 会议 World（PPT 同步播放）
- 🎵 音乐 World（AudioLink 可视化背景）
- 💡 沉浸感 World（VRC Light Volumes 联动）

❌ **不太适合**：
- 仅需最简单 1 个视频 + 不需要同步（用 SDK 自带 `UdonSyncPlayer` 即可）
- 需要深度自定义同步逻辑（应基于本项目源码二次开发）
- 仅图片查看且无同步需求（用 `VRCUnityVideoPlayer` 直接加载更轻量）

---

## 5 大模块清单

| 模块 | 作用 | 后端 |
|------|------|------|
| **Builtin Module** | Unity VideoPlayer 后端 | VRCUnityVideoPlayer |
| **AVPro Module** | 商业视频插件后端（直播流 + 7.1 音频）| VRCAVProVideoPlayer |
| **Image Module** | PNG/JPEG 图片查看 | 通用 |
| **Playlist Queue Handler** | 预设播放列表 + 用户队列 | — |
| **Locale** | 12+ 语言自动检测 | — |

**模块化优势**：屏幕（Screen）/ 音频源（Audio Source）/ UI 三者**完全解耦**，可独立配置，且支持同一 World 中**多实例**（如 3 块不同步的屏幕）。

---

## 9 大功能特性

| # | 特性 | 实现版本 | 价值 |
|---|------|----------|------|
| 1 | 基础播放 / 快进 / 暂停 / 进度条 | 1.0+ | 标配 |
| 2 | 预设播放列表 + 用户队列 | 1.0+ | Watch-together 核心 |
| 3 | 玩家输入 URL 历史记录 | 1.0.32+ | 玩家体验优化 |
| 4 | Quest 跨平台 URL | 1.0+ | PC/Quest 双兼容 |
| 5 | PNG/JPEG 图片查看 | 1.0.37+ | 通用场景 |
| 6 | 低延迟模式（RTSP/RTMP） | 1.0+ | 直播表演 |
| 7 | 播放速度调节（0.5x - 2x） | 1.1.0+ | 教学/演示 |
| 8 | **智能请求调度防 5s 限流** | 1.1.0+ | ⭐ 关键稳定性 |
| 9 | 本地模式（脱机预览） | 1.0+ | 单人模式 |

---

## 4 种显示模式（自定义 Shader）

| 模式 | 用途 | 适用场景 |
|------|------|----------|
| **Stretch** | 拉伸填满屏幕 | 背景视频（默认） |
| **Contain** | 保持比例 + 黑边 | 标准电影放映 |
| **Cover** | 保持比例 + 裁剪 | 满屏背景 |
| **Stereographic Video Source** | 立体 VR 视频 | 180°/360° 视频 |

**使用方式**：在屏幕材质的 Inspector 中选择对应的 Shader 模式。

---

## 9 大集成生态

| 集成 | 用途 | 关键能力 |
|------|------|----------|
| **AudioLink** | 视频音频自动切换到 AudioLink 源 | 音频可视化、节拍驱动特效 |
| **LTCGI** | 提供 CustomRenderTexture 视频输出 | 屏幕反射/折射、动态全局光照 |
| **VRC Light Volumes** | 视频播放联动动态光照 | 沉浸感（屏幕亮起时照亮房间） |
| **Topaz Chat** | 直播流服务 | 现场表演、演唱会 |
| **Udon Auth** | 锁定 UI 防止误操作 | 主持人/观众分级 |
| **YTTL** | 显示视频标题 | 视频来源追踪、版权溯源 |
| **AVPro** | 商业视频插件后端 | 直播流 + 7.1 音频（PCVR） |
| **PlayerData** | 持久化（可选） | 跨实例恢复玩家设置 |
| **Stream Key Assigner** | 每实例/每用户唯一 stream key | 直播流权限分配 |

---

## 安装方式

### 方式 1：通过 VCC/VPM（推荐）

1. 打开 VCC → 选 VRChat World 项目
2. VCC Settings → Add Package → 输入：
   ```
   https://xtlcdn.github.io/vpm/
   ```
3. 在项目列表中搜索 `idv.jlchntoz.vvmw` → 点击 Add
4. VCC 会自动下载并安装依赖（AVPro 需自行购买）

### 方式 2：手动导入

1. 从 [GitHub Releases](https://github.com/JLChnToZ/VVMW/releases) 下载最新 `.unitypackage` 或 `.zip`
2. ⚠️ **不推荐**（README 明确警告）：手动导入会**缺失依赖**
3. 必须手动安装依赖：
   - VRChat SDK 3.x
   - AVPro（如使用 AVPro 后端）
   - Udon Auth（如使用 UI 锁定）
   - VRC Light Volumes（如使用光照联动）
   - AudioLink（如使用音频可视化）

---

## 快速使用步骤

### 第一次使用

1. **拖入主控制器**：
   - 在 Project 面板找到 `VVMW` Prefab → 拖入场景
2. **配置屏幕**：
   - 拖入 `Default Screen` Prefab（或自定义屏幕）
   - 屏幕材质选择显示模式（Stretch/Contain/Cover/Stereographic）
3. **配置音频源**：
   - 拖入 `Default Audio Source`
   - 单声道：1 个 AudioSource
   - 立体声/环绕声：2-8 个 AudioSource（AVPro 支持 5.1/7.1）
4. **配置 UI**：
   - 拖入 `Default UI` Prefab（或自定义）
   - 传统 uGUI / TextMeshPro 双支持
5. **添加后端**：
   - Builtin Module（Unity VideoPlayer）→ PC + Quest
   - AVPro Module → 仅 PC，可播直播流
   - Image Module → 图片查看
6. **配置 Playlist Queue Handler**：
   - 预设播放列表 + 队列管理
7. **测试**：
   - 1 个 ClientSim 实例 → Editor Play Mode
   - 2 个 Build & Test 实例 → 完整多人同步验证

### 高级配置

#### 1. Quest 独立 URL

- 启用 `Quest URL` 字段
- 可设置 PC URL 与 Quest URL 不同
- **Quest 强制 HTTPS**：HTTP URL 会被 Quest 拒绝

#### 2. 玩家区域自动播放

- 启用 `Active Region` 组件
- 玩家进入区域 → 自动播放指定 URL
- 玩家离开 → 自动停止
- 1.7.0-beta.1+ 新增 auto mute / AudioLink 注册 / broadcast texture

#### 3. Stream Key 分配器

- 添加 `Stream Key Assigner` 组件
- 每实例/每用户分配独立 stream key
- 用于直播流权限控制（防止泄露）

#### 4. UI 锁定

- 集成 Udon Auth
- 仅特定用户可控制（主持人模式）
- 其他用户仅观看

#### 5. AB Loop

- 启用 AB Loop 模式
- 设置循环范围（开始/结束时间）
- 适合音乐循环 / 教学片段

---

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

---

## 平台兼容性

| 平台 | 兼容性 | 备注 |
|------|--------|------|
| **PC VR** | ✅ 完整功能 | 最佳体验（可启用 AVPro） |
| **PC Desktop** | ✅ 完整功能 | — |
| **Android (Quest)** | ✅ 自动优化 | 仅 Unity VideoPlayer 后端，HTTPS 强制 |
| **iOS** | ⚠️ 理论支持 | 未经官方测试 |

**自动平台适配**：
- **Quest**：强制使用 Builtin Module（Unity VideoPlayer）
- **PC**：可使用 AVPro Module（商业插件，付费）
- **URL 调度**：同一 World 在 PC/Quest 同时运行时，自动选择对应 URL

---

## 已知限制

来自官方说明 + Agent 分析：

| 限制 | 说明 | 影响 |
|------|------|------|
| **AVPro 需付费** | 商业插件，PC only | 直播流需购买授权 |
| **5s/URL 限流** | VRChat 全局 5s/URL 限制 | 已内置智能调度，但大量同时加载仍可能受限 |
| **Quest 强制 HTTPS** | HTTP URL 被 Quest 拒绝 | 需 HTTPS CDN |
| **Quest 视频格式限制** | 仅 MP4 (H.264) | 直播流格式需兼容性测试 |
| **复杂同步逻辑** | 时间同步算法复杂 | 不建议魔改 VideoCore |
| **依赖较多** | 9 大集成需分别安装 | 完整功能需装多个依赖 |
| **Editor 内 AVPro 无法播放** | AVPro 必须 Build & Test | Unity VideoPlayer 可在 Editor Play |
| **PlayerData 配额** | 100KB 限制 | 仅设置类可持久化 |
| **音频通道数** | Unity 后端 2 通道 / AVPro 6 通道（5.1）| 7.1 仅 PCVR EAC3 |

---

## 与官方 `UdonSyncPlayer` 的对比

| 维度 | 官方 UdonSyncPlayer | VVMW (VizVid) |
|------|---------------------|---------------|
| **维护方** | VRChat 官方 | JLChnToZ 社区 |
| **多后端** | ❌ 单后端 | ✅ Unity / AVPro / Image |
| **直播流** | 仅 AVPro | ✅ Builtin 低延迟 / AVPro 完整 |
| **跨平台 URL** | ❌ | ✅ 双输入框 |
| **同步精度** | URL + Vector2 时间戳 | ✅ 服务器时间锚点 + 阈值 + Performer |
| **同步风暴防护** | ❌ | ✅ OWNER_SYNC_COOLDOWN_TICKS |
| **播放列表** | ❌ | ✅ Playlist Queue Handler |
| **历史记录** | ❌ | ✅ 1.0.32+ |
| **播放速度** | ❌ | ✅ 1.1.0+ |
| **本地模式** | ❌ | ✅ |
| **集成生态** | ❌ | ✅ 9 大集成 |
| **本地化** | ❌ | ✅ 12+ 语言 |
| **跨实例持久化** | ❌ | ✅ PlayerData 可选 |
| **更新频率** | 随 SDK | 2-4 周一个版本 |
| **学习价值** | ⭐⭐⭐（基础） | ⭐⭐⭐⭐⭐（完整实现） |

**升级建议**：
- 简单 1 个视频 + 不需要同步 → 官方 `UdonSyncPlayer`
- 1-2 个视频 + 多人同步 → **VVMW**
- 直播表演 + 音频可视化 → **VVMW + AVPro + AudioLink**
- 教学演示 + AB Loop → **VVMW**

---

## 沉淀到知识库的内容

### 通用模式（8 个）→ `memory/FACT.md` + `memory/patterns/`

| 模式 | 文档 | 来源 |
|------|------|------|
| Manual Sync + Owner Authority | `FACT.md` §视频播放器 | `VideoCore.cs` |
| 服务器时间锚点 | `FACT.md` §视频播放器 | `CalcSyncTime()` |
| 阈值同步 | `FACT.md` §视频播放器 | `timeDriftDetectThreshold` |
| 冷却期防同步风暴 | `FACT.md` §视频播放器 | `OWNER_SYNC_COOLDOWN_TICKS` |
| 双缓冲状态分离 | `FACT.md` §视频播放器 | `localXxx` + `[UdonSynced] xxx` |
| Performer 模式延迟补偿 | `FACT.md` §视频播放器 | `PerformerLatency` |
| 播放后端抽象 | `memory/patterns/strategy-pattern-udon.md` | `Handler` 接口 |
| 字符串拼接避冲突 | `memory/patterns/data-encoding-tricks.md` | `\u2029` Paragraph Separator |

### 案例研究档案 → `memory/sources/vvmw.md`

包含完整项目档案（5 大模块 + 13 个 Releases + 9 大功能 + 9 大集成 + 4 种显示模式 + 工程评价）

---

## 引用格式

**向创作者推荐时**：
> 推荐使用 **VizVid (VVMW)** (v1.7.5)，JLChnToZ 维护，
> VRChat 创作者生态最受欢迎的多人同步视频播放器，5 大模块 + 9 大集成 + 12+ 语言本地化。
> VPM 仓库：https://xtlcdn.github.io/vpm/
> 仓库：https://github.com/JLChnToZ/VVMW

**作为知识来源时**：
> 来源：`memory/sources/vvmw.md`（案例研究 + 8 个 Pattern 来源）
> 工具使用：`memory/world/vvmw.md`（本文件）

---

## 关联知识库

| 文档 | 关系 |
|------|------|
| `memory/sources/vvmw.md` | **本项目的案例研究型源文档**（A2） |
| `memory/world/udon/video-players/index.md` | 视频播放器总览（SDK 基础） |
| `memory/world/udon/video-players/www-whitelist.md` | 视频 URL 白名单 |
| `memory/hybrid/audio-link.md` | AudioLink 集成（VVMW 集成之一） |
| `memory/world/vrc-light-volumes.md` | VRC Light Volumes（VVMW 集成之一） |
| `memory/FACT.md` §视频播放器 | **时间同步算法模式（参考工程）** |
| `memory/patterns/manual-sync-state.md` | Manual Sync 基础 |
| `memory/world/udon/external-urls.md` | VRCUrl 基础 |
| `memory/api/persistence.md` | PlayerData API（持久化用） |
| `memory/world/performance-guide.md` | World 性能优化（多实例屏幕场景） |
| `memory/world/udon/video-players/` | 视频播放器底层知识 |
| `memory/hybrid/udon-world-plugins.md` | 推荐 Udon 世界插件索引 |
