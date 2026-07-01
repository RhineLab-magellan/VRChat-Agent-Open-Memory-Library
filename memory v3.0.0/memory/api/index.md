---
title: "API Reference — 总览"
category: api
knowledge_level: core
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-15
confidence: Medium
tags:
  - misc
  - index
  - navigation
aliases:
  - "API Reference — 总览"
  - index
related:
  - player-api.md
  - events-reference.md
  - pickups.md
  - dynamics.md
  - networking.md
  - persistence.md
  - vrchat-advanced-apis.md
  - animator.md
  - audio.md
  - ui.md
  - udonsharp-runtime.md
  - udon-type-exposure.md
  - exposed-types.md
  - not-exposed.md
  - api-checker.md
---
# API Reference — 总览

> 状态: ✅ 16 个 API 文件已分类组织

---

## 概述

本目录提供 UdonSharp 编程时所需的 **API 速查表**。每个文件按"Udon 暴露状态"+"热路径标记"组织。

| 标记 | 含义 |
|------|------|
| ✅ 暴露 | 已确认在 Udon VM 中可用 |
| ⚠️ 需验证 | 文档未明确，需自行测试 |
| ❌ 未暴露 | 不可用（见 `not-exposed.md`） |
| 热路径 ✅ | 每帧调用成本可接受 |
| 热路径 ⚠️ | 每帧调用有显著成本 |
| 热路径 ❌ | 不能在 Update/每帧场景使用 |

---

## 按子域分类

### 🎯 核心交互 API

| 文档 | 主题 | 关键 API |
|------|------|---------|
| **[player-api.md](player-api.md)** | 玩家信息、位置、语音、追踪 | `VRCPlayerApi`, `displayName`, `GetPosition`, `TeleportTo`, `SetVoice*` |
| **[events-reference.md](events-reference.md)** | Udon 事件完整签名 | `OnPlayerJoined/Left`, `Interact`, `InputJump/Use`, `OnOwnershipRequest`, MIDI 事件 |
| **[pickups.md](pickups.md)** | 拾取物体 API | `OnPickup`, `OnDrop`, `VRCObjectSync` |
| **[dynamics.md](dynamics.md)** | World 动力学（SDK 3.10.0+） | `OnContactEnter`, `OnPhysBoneGrab` |

### 🌐 网络与同步 API

| 文档 | 主题 | 关键 API |
|------|------|---------|
| **[networking.md](networking.md)** | Networking 类 + UdonBehaviour 同步成员 | `SetOwner`, `RequestSerialization`, `SendCustomNetworkEvent`, `[UdonSynced]`, `[NetworkCallable]` |
| **[persistence.md](persistence.md)** | 持久化 PlayerData/PlayerObject | `PlayerData.SetInt/TryGetString`, `OnPlayerRestored`, `OnPersistenceUsageUpdated` |
| **[vrchat-advanced-apis.md](vrchat-advanced-apis.md)** | VRCGraphics/QualitySettings/Drones/MIDI | `VRCGraphics.Blit`, `VRCShader.SetGlobal`, `VRCQualitySettings` |

### 🎨 渲染与媒体 API

| 文档 | 主题 | 关键 API |
|------|------|---------|
| **[animator.md](animator.md)** | Animator 控制 | `SetInteger`, `SetFloat`, `SetBool`, `Play` |
| **[audio.md](audio.md)** | AudioSource 播放 | `Play`, `Stop`, `volume`, `pitch` |
| **[ui.md](ui.md)** | Unity UI 集成 | `Text.text`, `Button.onClick`, `Slider.value` |

### 🛠 底层运行时 API

| 文档 | 主题 | 关键 API |
|------|------|---------|
| **[udonsharp-runtime.md](udonsharp-runtime.md)** | UdonSharpBehaviour 反射与代理 | `GetProgramVariable/SetProgramVariable`, `FieldChangeCallback`, `GetUdonTypeID` |
| **[udon-type-exposure.md](udon-type-exposure.md)** | Udon Type 暴露树索引 | 1387 类型 / 9579 暴露 API |
| **[exposed-types.md](exposed-types.md)** | 已暴露类型详细清单 | 自动生成完整列表 |
| **[not-exposed.md](not-exposed.md)** | 未暴露 API 黑名单 | List/Dictionary/反射/线程/异常 |
| **[api-checker.md](api-checker.md)** | API 检查器代码模式 | C# 代码静态分析工具 |
| **[official-doc-clarifications.md](official-doc-clarifications.md)** | 官方文档澄清与陷阱 | Player Collision 限制、IsNetworkSettled、OnVariableChanged、EventTiming |

---

## 按使用场景速查

| 场景 | 推荐 API 文档 |
|------|--------------|
| **门/开关/离散状态** | networking.md + events-reference.md |
| **玩家位置/旋转同步** | networking.md + player-api.md |
| **拾取物体** | pickups.md + dynamics.md |
| **网络事件触发** | networking.md + events-reference.md |
| **数据持久化** | persistence.md + official-doc-clarifications.md |
| **UI 按钮响应** | ui.md + events-reference.md |
| **动画状态切换** | animator.md |
| **音效播放** | audio.md |
| **跨脚本通信** | udonsharp-runtime.md |
| **类型检查** | udonsharp-runtime.md + udon-type-exposure.md |
| **VFX 后期处理** | vrchat-advanced-apis.md + world/udon/vrc-graphics/ |
| **Quest 兼容** | rules/performance-rules.md + platform/android-development.md |

---

## API 检查工作流

```
1. 找到需要的 API
   ↓
2. 查 exposed-types.md → 确认 Udon 暴露
   ↓
3. 查 api/<topic>.md → 获取精确签名 + 热路径标记
   ↓
4. 查 not-exposed.md → 确认不在黑名单
   ↓
5. 查 official-doc-clarifications.md → 注意已知陷阱
   ↓
6. 查 rules/ → 验证使用模式合规
   ↓
7. 查 patterns/ → 获取推荐实现模式
```

---

## 与其他目录的关系

| 关系 | 目录 |
|------|------|
| **应用层详解** | `memory/world/udon/networking/` （10 个文档） |
| **语言限制** | `memory/rules/udonsharp-language-limits.md` |
| **API 暴露规则** | `memory/api/udon-type-exposure.md` |
| **设计模式** | `memory/patterns/` |
| **场景组件** | `memory/world/scene-components/` |
| **VRChat 官方文档本地化** | `memory/world/udon/` （15+ 文档） |

---

## 信任模型

| 来源 | 等级 | 文档 |
|------|------|------|
| VRChat 官方文档 | Tier A | networking.md, persistence.md, dynamics.md, udonsharp-runtime.md, vrchat-advanced-apis.md |
| UdonSharp 官方 + DeepWiki | Tier A | udon-type-exposure.md, exposed-types.md, not-exposed.md, api-checker.md |
| 官方文档修正 | Tier A | official-doc-clarifications.md, events-reference.md |
| 社区经验 | Tier B | animator.md, audio.md, ui.md, pickups.md |

> **重要**: 标记为 `⚠️ 需验证` 的 API 需自行测试；标记为 `热路径 ❌` 的 API 不能在 Update 中使用。
