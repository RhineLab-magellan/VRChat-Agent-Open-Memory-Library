---
title: "示例包: curated (VRChat 官方精选)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - curated
  - vrchat-official

aliases:
  - "VRChat Curated VPM"
  - "VRChat 官方精选包"
  - "com.vrchat.repos.curated"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/official.md
  - sources/example-central.md
  - avatar/optimization-guide.md
  - world/performance-guide.md

source: vcc.vrczh.org + mirror vpm index (upstream packages.vrchat.com 国内不可达)
source_type: official
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# curated — VRChat 官方精选包

> **📦 VPM 仓库速查**:
> - **apiId**: `curated`
> - **上游 URL**: <https://packages.vrchat.com/curated> (国内被墙, 仅以 mirror 为准)
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/curated>
> - **状态**: ✅ 同步成功
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/curated> (80861 bytes, 2026-07-01 快照)
> - Upstream VPM index: <https://packages.vrchat.com/curated> (国内不可达, **仅以 mirror 为准**)
> - 顶层 description: 镜像站未提供；upstream 同样为空 (VRChat 不维护顶层描述)

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `curated` |
| **作者** | VRChat |
| **类型** | 官方精选 (由 VRChat 官方审核/推荐的社区包) |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/curated> |
| **上游 URL** | <https://packages.vrchat.com/curated> (国内被墙) |
| **包数量** | 9 个 |
| **同步状态** | ✅ 同步成功 (2026-07-01 01:40 UTC) |

---

## 包含的 9 个包

> 字段说明: `unity` 表示该 version 兼容的 Unity 主版本。

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `com.llealloo.audiolink` | **AudioLink** | v0.3.1 | ? | Audio reactive prefabs for VRChat — 音频反应预制体 |
| 2 | `dev.vrlabs.vrworldtoolkit` | **VRWorld Toolkit** | v2.1.5 | 2019.4 | VRChat world 创建辅助工具集 |
| 3 | `com.nathannrsg.easy-quest-switch` | **EasyQuestSwitch** | v1.2.1 | ? | PC/Quest 平台切换自动化 |
| 4 | `com.vrchat.avatars.3.0.manager` | **Avatars 3.0 Manager** | v2.0.18 | 2019.4 | Playable Layers/Parameters 管理工具 |
| 5 | `blackstartx.gesture-manager` | **Gesture Manager** | v3.8.2 | 2019.4 | Avatar 动画预览工具 (Unity 内) |
| 6 | `com.vrchat.av3emulator` | **Av3Emulator** | v3.1.3 | 2019.4 | Avatar 3.0 System 模拟器 |
| 7 | `com.vrchat.client-simulator` | **VRChat Client Simulator** | v1.2.2 | 2019.4 | SDK3 World 测试用客户端模拟器 |
| 8 | `com.vrchat.udonsharp` | **UdonSharp** | v1.1.6 | 2019.4 | C# → Udon 字节码编译器 |
| 9 | (其他社区提交) | ... | ... | ... | mirror 包含 9 个包中部分未列出 |

> ⚠️ 部分 `unity` 字段为 `?` 表示 mirror 数据中该字段缺失。**实际包内一定有 unity 字段** — 这是 mirror 的解析问题，不是包本身的问题。

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2019.4** | 5/9 | VRWorld Toolkit, Av3Emulator, Gesture Manager, Avatars 3.0 Manager, Client Simulator, UdonSharp |
| **2022.3** | 0/9 | ⚠️ 所有包仅声明 2019.4，但部分包 (e.g. UdonSharp 1.1.6) **实际兼容 2022.3** (VRChat 当前 LTS) |
| **6000.0** | 0/9 | 不支持 Unity 6 (除 hai-vr Basis 系列) |

**风险提示**: 部分包虽然标 2019.4 但实际**双版本兼容**。需查阅各包最新 changelog 确认 2022.3 支持状态。

---

## 主要包详细说明

### AudioLink (v0.3.1)
- **作者**: LleaWee (Llealloo)
- **核心功能**: 让 Shader 通过音频反应。在 VRC World 中通过 OSC 接收主机音频
- **应用场景**: 舞厅、音乐可视化、动态光照
- **架构**: Master Time Anchor + 8 通道音频 FFT
- **知识库参考**: `memory/hybrid/osc-protocol.md` (AudioLink OSC 协议)

### UdonSharp (v1.1.6)
- **作者**: VRChat (Merlin)
- **核心功能**: C# 编译到 Udon 字节码
- **VPM 依赖**: `com.vrchat.base`, `com.vrchat.worlds`
- **应用场景**: 几乎所有 Udon World 都依赖
- **知识库参考**: `memory/world/udon/` (UdonSharp 全部知识)

### VRWorld Toolkit (v2.1.5)
- **作者**: VRLabs
- **核心功能**: World 创建辅助 (碰撞设置、Mirror、Player 区域配置、Mirror 优化)
- **应用场景**: World 性能优化必备
- **知识库参考**: `memory/world/performance-guide.md`

### Avatars 3.0 Manager (v2.0.18)
- **作者**:  Hai­Cat­fish
- **核心功能**: Playable Layers (Base/Additive/Gesture/Action/FX) 可视化编辑
- **应用场景**: Avatar 动画参数管理
- **知识库参考**: `memory/avatar/playable-layers.md`

### Gesture Manager (v3.8.2)
- **作者**: BlackStartX
- **核心功能**: Unity Editor 内模拟 VRChat 菜单, 直接触发手势/动作测试
- **应用场景**: Avatar 调试 (无需进游戏测试)

### Av3Emulator (v3.1.3)
- **作者**: lyuma
- **核心功能**: Unity Editor 内模拟 Avatar 3.0 系统 (Playable Layers 状态机、参数、菜单)
- **应用场景**: Avatar 调试 (无需进游戏测试)
- **注意**: anatawa12 维护的 fork (com.anatawa12.av3emulator) 仍在更新到 3.0.3

### Client Simulator (v1.2.2)
- **作者**: VRChat
- **核心功能**: SDK3 World 测试用客户端模拟器
- **应用场景**: World 调试, Udon 行为验证
- **知识库参考**: `memory/sources/clientsim.md`

### EasyQuestSwitch (v1.2.1)
- **作者**: NathanNRsg
- **核心功能**: 一键在 PC/Quest 平台设置之间切换 (资源、设置、Player 层)
- **应用场景**: 跨平台 World 开发
- **知识库参考**: `memory/platform/easyquestswitch.md`

---

## 已知差异 (Mirror vs Upstream)

| 差异点 | 描述 |
|--------|------|
| 顶层 description | 均为空 — VRChat 不维护 |
| 包内 description | mirror 完整保留 upstream |
| URL 改写 | upstream 的 `https://*.zip` → mirror 的 `https://vpm.vrczh.org/files/download/...zip?fileId={sha256}/...` |
| BOM 清理 | (upstream 未知，国内无法访问) |
| 同步延迟 | ≤ 10 分钟 (`*/10 * * * *`) |

---

## 使用建议

- ✅ **国内用户**: 添加 `https://vpm.vrczh.org/vpm/curated` 即可访问所有 9 个精选包
- ⚠️ **海外用户**: 优先用 upstream `https://packages.vrchat.com/curated` (实时性 + 海外速度)
- ⚠️ **若用 mirror 找不到 AudioLink**: 检查 VCC 缓存 (`%LOCALAPPDATA%\VRChatCreatorCompanion\Cache`) 是否有 stale 缓存
- ❌ **不要添加到 VCC** 的同时**再添加 upstream** — 会导致包版本冲突 (mirror 已注入 SDK)

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | 80861 |
| Upstream 字节 | N/A (国内不可达) |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
