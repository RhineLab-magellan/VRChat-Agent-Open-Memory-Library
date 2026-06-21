---
title: World Examples — SDK 与官方示例索引
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - udonsharp
  - reference

aliases:
  - "World Examples — SDK 与官方示例索引"

related:
  - obstacle-course/index.md
  - obstacle-course/build-from-demo-parts.md
  - obstacle-course/build-from-custom-parts.md
  - obstacle-course/uoc-flythrough.md
  - obstacle-course/uoc-how-stuff-works.md
  - obstacle-course/uoc-window.md
  - udon-example-scene/index.md
  - world/examples/ai-navigation.md
  - world/examples/detect-controller-collide.md
  - world/examples/image-loading.md
  - world/examples/minimap.md
  - world/examples/mute-others.md
  - world/examples/player-join-zones.md
  - world/examples/screen-canvas.md
  - world/examples/udon.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# World Examples — SDK 与官方示例索引

> **Domain**: World
> **本地化日期**: 2026-06-15
> **覆盖**:VRChat 官方 Creator Docs / SDK Prefabs / Example Central / World Jam 项目

---

## 概述

本目录集中本地化 **VRChat 官方 World 示例项目** 的文档。每个子分类对应一个完整的官方示例,内容包含:

- 官方 GitHub 仓库 / Release zip 链接
- 快速开始步骤
- 核心程序设计
- 关键工程参数

---

## 子分类索引

### ⭐ Obstacle Course(World Jam 2 官方套件)

> **Time Trial 模式完整参考实现**

- **GitHub**: https://github.com/vrchat/VRChat-Obstacle-Jam
- **Release**: v1.0.3(最后验证:2026-06-15)
- **Demo Scene**:`Assets/_WorldJam2/Scenes/DemoScene`
- **完整路径**:`world/examples/obstacle-course/`

| 文档 | 内容 |
|------|------|
| [index.md](./obstacle-course/index.md) | Overview + Quick Start + Move/Jump/Players/PowerUp 配置 |
| [build-from-demo-parts.md](./obstacle-course/build-from-demo-parts.md) | 使用 Demo 预制件 + Toolkit 窗口拼装赛道 |
| [build-from-custom-parts.md](./obstacle-course/build-from-custom-parts.md) | 自定义 Checkpoint/PowerUp/Hazard 预制件 |
| [uoc-flythrough.md](./obstacle-course/uoc-flythrough.md) | Cinemachine 飞行通过相机(预览视频) |
| [uoc-how-stuff-works.md](./obstacle-course/uoc-how-stuff-works.md) | 内部机制详解(13+ 程序,OnPlayerDataEnter 桥接) |
| [uoc-window.md](./obstacle-course/uoc-window.md) | Toolkit Editor 窗口完整用法 |

**核心模块**:PlayerDataManager / PlayerData / Course / Checkpoint / OnPlayerDataEnter / PowerUp / PlayerModsManager / Hazard / Score / HighScore / Toolkit

**关键工程参数**:
- **Number of Players** = N → SDK Publish Capacity = **N / 2**
- 玩家 Walk/Run/Strafe 三轴同速(简化设计)
- PowerUp 同类相消(Speed 与 Jump 独立队列)

---

### Udon Example Scene(SDK 内置标准示例)

- **完整路径**:`world/examples/udon-example-scene/`
- **来源**:VRChat SDK 内置(无需单独下载)
- **内容**:13+ Prefab,5 种同步模式详解

| 文档 | 内容 |
|------|------|
| [index.md](./udon-example-scene/index.md) | 13+ Prefab 详解 + 5 种同步模式 |

---

## 涉及的核心设计模式

| 模式 | 出现于 | 关键优势 |
|------|--------|----------|
| **VRCObjectPool + 动态重建** | Obstacle Course (PlayerDataManager) | 玩家数量可配置 |
| **OnPlayerDataEnter 桥接** | Obstacle Course | 统一 Trigger 处理,避免重复 OnTriggerEnter |
| **同名查找 + 引用注入** | Obstacle Course (Toolkit) | Prefab 完全可序列化 |
| **分数同步用 synced 变量** | Obstacle Course (ScoreField) | 简单可靠,带宽较高 |
| **Effect Queue + 同类相消** | Obstacle Course (PlayerModsManager) | Buff/Debuff 系统的"刷新计时"语义 |

---

## 与其他知识库的关系

- **`sources/example-central.md`**:VRChat 官方 Example Central 一站式获取工具,与本目录互为补充
- **`world/clientsim/`**:Editor 内模拟 VRChat 客户端(World 测试工具)
- **`platform/easyquestswitch.md`**:PC/Quest 平台切换自动化
- **`world/udon/udonsharp/compilation.md`**:UdonSharp 编译管线(原 `world/udonsharp-compilation.md` 已迁移并删除)

---

**最后验证日期**:2026-06-15
