---
title: "推荐 Udon 世界插件(Recommended Udon World Plugins)"
category: hybrid
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - hybrid
  - json
  - ownership
aliases:
  - "推荐 Udon 世界插件(Recommended Udon World Plugins)"
  - udon-world-plugins
related:
  - alcom.md
  - audio-link.md
  - osc-protocol.md
  - vcc.md
  - index.md
---
# 推荐 Udon 世界插件(Recommended Udon World Plugins)

> **Domain**: Hybrid
> **类型**: 推荐工具索引(Group C — 工具使用指南)
> **目标读者**: VRChat World 创作者(推荐安装的插件) + 玩家(识别 World 能力)
> **状态**: ✅ 已收录 2 个插件(TLP UdonVoiceUtils + VizVid VVMW)

---

## 本文定位

本文档是**推荐 World 创作者安装**的 Udon 插件索引。每个插件都满足以下条件:

| 条件 | 说明 |
|------|------|
| **公开维护** | 开源 + 持续维护 + 社区有反馈渠道 |
| **VPM 分发** | 通过 VPM 安装(不依赖 .unitypackage 手动导入) |
| **文档完整** | 有 README + 注释 + 示例 |
| **质量验证** | 经过知识库深度分析(FACT/Source 文档) |
| **设计规范** | 遵循 VRChat 最佳实践(同步、Ownership、Quest 兼容) |

**与 `memory/sources/open-source-projects.md` 的区别**:
- `sources/open-source-projects.md` = **案例研究**型参考工程(不推荐给创作者,仅分析其设计模式)
- 本文档 = **工具使用**型推荐(创作者可直接装到自己的 World 中使用)

**与 `memory/world/examples/` 的区别**:
- `world/examples/` = VRChat 官方示例(教学性质,提供完整工程参考)
- 本文档 = 第三方插件(生产性质,提供特定功能)

---

## 收录插件列表

### ⭐ TLP UdonVoiceUtils (UVU) — 玩家语音/音频动态控制库

| 属性 | 值 |
|------|-----|
| **仓库** | https://github.com/Guribo/UdonVoiceUtils |
| **作者** | Guribo (TLP) |
| **许可证** | GPL-3.0 |
| **VPM** | `https://raw.githubusercontent.com/Guribo/UdonVoiceUtils/main/package.json` |
| **最后验证** | 2026-06-20 |
| **SDK** | VRChat SDK 3.x |
| **核心规模** | 35 个 .cs 文件,1446 行主 Controller |
| **5 层次创新** | ①架构层(MVC + Strategy + ExecutionOrder 链) ②同步层(Dual-Copy) ③冲突层(优先级仲裁 + PrivacyChannel) ④稳定性层(Master 所有权三层防御) ⑤性能层(RaycastNonAlloc + 零分配) |

#### 推荐理由

| 场景 | UVU 提供的解决方案 |
|------|-------------------|
| **玩家进入"静音房间"** | `VoiceOverrideRoom` 完整示例,进入区域后自动静音所有人 |
| **关上门后听不到外面** | `VoiceOverrideDoor` 完整示例,门状态控制音频穿透 |
| **触发器区域静音** | `VoiceOverrideTriggerZone` 完整示例,3 层保险(Trigger/距离/重连) |
| **按玩家距离衰减** | `DefaultPlayerOcclusion` 完整示例,`Physics.RaycastNonAlloc` 零分配 |
| **为单个玩家调整音量** | `AdjustableGain` 完整示例,`SetVoiceGain` + Slider |
| **麦克风激活控制** | `MicActivation` 完整示例,基于区域/状态 |
| **隐私分组(多频道)** | `PlayerAudioOverride.PrivacyChannel` 内置支持 |
| **不同 Override 冲突仲裁** | `PlayerAudioOverrideList.GetMaxPriority` 自动选最高优先级 |

#### 相比 `memory/world/examples/mute-others.md` 的升级

| 维度 | 官方 MuteOthers 示例 | UVU 工业级方案 |
|------|---------------------|---------------|
| **同步机制** | 本地(每个玩家独立) | 全员同步 + Master 权威 |
| **持久化** | 无 | PlayerData 100KB 配额内可保存 |
| **优先级** | 无(全局开关) | Priority 字段(0-100)+ 仲裁算法 |
| **多区域组合** | 否(只能全局) | 是(房间/门/区域可叠加) |
| **遮挡检测** | 否 | `DefaultPlayerOcclusion` Raycast |
| **跨实例恢复** | 否 | PlayerData 持久化 |
| **Editor 调试** | 无 | Gizmos 颜色编码 + Custom Editor |
| **可扩展性** | 单脚本 | MVC + Strategy + 8 层职责 |
| **性能** | N/A(简单遍历) | `PlayerUpdateRate` 节流 + 零分配池 |
| **Quest 兼容** | ✅ | ✅(无反射/无 GC) |

#### 使用建议

**适合场景**:
- 🎭 社交类 World(密室、酒吧、会议室、教室)
- 🎵 音乐/表演 World(舞台控制、麦克风激活)
- 🔒 隐私需求场景(私人房间、多频道分组)
- 🏠 沉浸式 RPG(基于区域的音频规则)

**不太适合**:
- 大型多人世界(>40 人)— 优先级仲裁计算成本需要评估
- 简单 Mute 需求 — 用官方 `mute-others` 示例更轻量
- 纯视觉展示 World — 不需要音频控制

#### 完整资源

- **案例研究**: `memory/sources/udonvoiceutils.md` (深度分析,10 章节,10 大难题,工程评价)
- **互补示例**: `memory/world/examples/mute-others.md` (官方基础版,适合学习)
- **设计模式**: `memory/patterns/index.md` (10 个 ⭐U 模式: dual-copy-sync / execution-order-chain / strategy-pattern-udon / object-pool-udon / priority-arbitration / master-ownership-defense / gizmos-relationship / trigger-event-fallback / compile-time-debug-strip / auto-scripting-symbol)
- **API 索引**: `memory/sources/udonvoiceutils.md` §8 (PlayerAudio* API 完整列表)

#### 安装方式

```json
// 在 VCC/VPM 中添加 VPM 仓库
https://raw.githubusercontent.com/Guribo/UdonVoiceUtils/main/package.json
```

安装后在 World 中:
1. 拖入 `PlayerAudioController` Prefab 到场景
2. 拖入 `SyncedPlayerAudioConfigurationModel` 关联 Controller
3. 拖入 `PlayerAudioView` UI 面板
4. 添加需要的 `VoiceOverride*` 触发器 Prefab
5. 测试多人同步

---

### ⭐ VizVid (VVMW) — 多人同步视频播放器

| 属性 | 值 |
|------|-----|
| **仓库** | https://github.com/JLChnToZ/VVMW |
| **作者** | JLChnToZ |
| **VPM** | `https://xtlcdn.github.io/vpm/` (包名: `idv.jlchntoz.vvmw`) |
| **最后验证** | 2026-06-20 (1.6.0 稳定版 / 1.7.0-beta.1) |
| **SDK** | VRChat SDK 3.x |
| **核心规模** | 5 大模块 + 13 个 Releases + 9 大集成 + 12+ 语言本地化 |
| **8 模式沉淀** | Manual Sync + Owner Authority + 服务器时间锚点 + 阈值同步 + 冷却期防风暴 + 双缓冲状态 + Performer 延迟补偿 + Strategy 模式多后端 |

#### 推荐理由

| 场景 | VVMW 提供的解决方案 |
|------|---------------------|
| **多人观影(Watch-together)** | 预设播放列表 + 用户队列 + 同步时间戳 |
| **直播表演(演唱会/DJ)** | 低延迟模式 + AVPro 后端 + Topaz Chat 集成 |
| **图片幻灯片(艺术展)** | Image Module + 4 种显示模式 |
| **跨平台 URL** | 双输入框(PC + Quest 独立 URL)|
| **音频可视化** | AudioLink 集成(自动切换音轨 + 状态上报) |
| **动态光照** | VRC Light Volumes 集成(屏幕亮起联动光照) |
| **UI 权限锁定** | Udon Auth 集成(主持人/观众分级) |
| **视频标题溯源** | YTTL 集成(已知来源自动显示标题) |
| **多实例屏幕** | 模块化解耦(屏幕/音频/UI 独立配置) |
| **直播流权限** | Stream Key Assigner(每实例/每用户唯一) |

#### 相比官方 `UdonSyncPlayer` 的升级

| 维度 | 官方 UdonSyncPlayer | VVMW (VizVid) |
|------|---------------------|---------------|
| **多后端** | ❌ 单后端 | ✅ Unity / AVPro / Image |
| **直播流** | 仅 AVPro | ✅ Builtin 低延迟 / AVPro 完整 |
| **跨平台 URL** | ❌ | ✅ 双输入框 |
| **同步精度** | URL + Vector2 时间戳 | ✅ 服务器时间锚点 + 阈值 + Performer |
| **同步风暴防护** | ❌ | ✅ OWNER_SYNC_COOLDOWN_TICKS |
| **播放列表/队列** | ❌ | ✅ Playlist Queue Handler |
| **历史记录** | ❌ | ✅ 1.0.32+ |
| **播放速度** | ❌ | ✅ 1.1.0+ |
| **本地模式** | ❌ | ✅ |
| **集成生态** | ❌ | ✅ 9 大集成(AudioLink/LTCGI/VRCLightVolumes/Topaz/UdonAuth/YTTL) |
| **本地化** | ❌ | ✅ 12+ 语言 |
| **跨实例持久化** | ❌ | ✅ PlayerData 可选 |
| **AB Loop** | ❌ | ✅ 1.6.0+ |
| **学习价值** | ⭐⭐⭐(基础) | ⭐⭐⭐⭐⭐(完整实现) |

#### 5 大模块概览

| 模块 | 作用 | 后端 |
|------|------|------|
| **Builtin Module** | Unity VideoPlayer 后端 | VRCUnityVideoPlayer |
| **AVPro Module** | 商业视频插件(直播流 + 7.1) | VRCAVProVideoPlayer |
| **Image Module** | PNG/JPEG 图片查看 | 通用 |
| **Playlist Queue Handler** | 预设播放列表 + 用户队列 | — |
| **Locale** | 12+ 语言自动检测 | — |

#### 使用建议

**适合场景**:
- 🎬 多人观影(Watch-together)World(影院、客厅、咖啡厅)
- 📡 直播表演(演唱会、DJ 现场、VTuber 活动)
- 🖼️ 艺术展示 World(图片幻灯片、画展)
- 🎓 教学演示 World(视频教程、演讲)
- 🎮 游戏厅 World(视频背景 + 游戏 UI)
- 🎵 音乐 World(AudioLink 可视化背景)
- 💡 沉浸感 World(VRC Light Volumes 联动)

**不太适合**:
- 仅需最简单 1 个视频 + 不需要同步(用 SDK 自带 `UdonSyncPlayer` 即可)
- 需要深度自定义同步逻辑(应基于本项目源码二次开发)
- 仅图片查看且无同步需求(用 `VRCUnityVideoPlayer` 直接加载更轻量)

#### 完整资源

- **案例研究**: `memory/sources/vvmw.md` (深度分析,5 大模块 + 13 个 Releases + 9 大集成 + 工程评价)
- **工具使用**: `memory/world/vvmw.md` (本节对应的完整工具文档)
- **时间同步算法模式**: `memory/FACT.md` §视频播放器时间同步算法模式(参考工程)
- **互补官方示例**: `memory/world/udon/video-players/index.md` (SDK 基础视频播放器)
- **依赖生态**:
  - `memory/hybrid/audio-link.md` AudioLink 集成
  - `memory/world/vrc-light-volumes.md` VRC Light Volumes 集成
  - `memory/api/persistence.md` PlayerData API

#### 安装方式

```json
// 在 VCC/VPM 中添加 VPM 仓库
https://xtlcdn.github.io/vpm/
```

安装后在 World 中:
1. 拖入 `VVMW` Prefab 到场景
2. 拖入 `Default Screen` Prefab(屏幕)
3. 拖入 `Default Audio Source`(音频源,单/立体声/5.1)
4. 拖入 `Default UI` Prefab(传统 uGUI / TextMeshPro 双支持)
5. 添加后端模块(Builtin / AVPro / Image)
6. 可选:配置 Playlist Queue Handler / Active Region / Stream Key Assigner
7. 测试多人同步(2 个 Build & Test 实例)

⚠️ **Quest 强制 HTTPS**:Quest 客户端拒绝 HTTP URL,需配置 HTTPS CDN

---

## 待收录插件(评估中)

| 插件 | 领域 | 状态 |
|------|------|------|
| **AudioLink** | 音频同步/可视化 | ⏳ 待评估(已是 Hybrid 域核心文档) |
| **VRCLightVolumes** | 光照系统 | ⏳ 待评估(已有 `memory/world/vrc-light-volumes.md`) |

> **注**: 案例研究(`sources/open-source-projects.md`) ≠ 推荐插件(本文)。升级条件: 工具稳定性 + 社区反馈 + 文档完整度 + 长期维护承诺

---

## 评估标准(插件晋升)

如果一个第三方插件希望被收录到本文档,需满足:

| 维度 | 要求 |
|------|------|
| **维护状态** | 最近 6 个月内至少有 1 次 commit |
| **社区反馈** | 10+ stars 或 100+ downloads |
| **文档完整** | README + 至少 3 个示例 Prefab |
| **VPM 分发** | 有 `package.json` 可通过 VPM 安装 |
| **设计质量** | 遵循 VRChat 最佳实践(无反射黑魔法、无 GC 滥用) |
| **跨平台** | PC/Quest 兼容(不依赖 PC-only 特性) |
| **可验证** | 知识库已建立 `sources/` 深度分析文档 |

---

## 与其他知识库的关系

| 关系 | 目录 |
|------|------|
| **案例研究溯源** | `memory/sources/open-source-projects.md`(所有推荐插件都必须先入案例研究) |
| **设计模式沉淀** | `memory/patterns/index.md`(插件实现的通用模式) |
| **官方示例互补** | `memory/world/examples/`(基础教学 vs 工业级) |
| **API 参考** | `memory/api/`(VRCPlayerApi 音频相关 API) |
| **失败案例参考** | `memory/reviews/common-failures.md`(避免重蹈覆辙) |

---

## 维护记录

| 日期 | 变更 |
|------|------|
| 2026-06-20 | 创建本文档,收录 TLP UdonVoiceUtils 作为首个推荐插件 |
| 2026-06-20 | 新增 VizVid (VVMW) 作为第二个推荐插件(A2/C16 双重身份) |
