---
title: "VRChat Creator Companion (VCC)"
category: hybrid
knowledge_level: applied
status: active
source: "https://vcc.docs.vrchat.com/ (2026-07-01 全站下载)"
source_type: official
version: "2.6.x (2025-12)"
last_review: 2026-07-01
confidence: High
tags:
  - hybrid
  - vcc
  - vpm
  - toolchain
  - project-management
aliases:
  - VCC
  - "Creator Companion"
  - "VRChat Creator Companion"
related:
  - alcom.md
  - "../sources/vpm-package-template.md"
  - audio-link.md
  - osc-protocol.md
  - udon-world-plugins.md
---

# VRChat Creator Companion (VCC)

> **Domain**: Hybrid（Avatar + World 共享 Base 基础设施）
> **定位**: VRChat 官方项目与依赖管理器
> **官方文档**: https://vcc.docs.vrchat.com/
> **本地副本**: `参考文献/VCC官方文档/`

---

## 1. 概述

**[FACT]** VCC 是 VRChat 官方推出的桌面应用，负责：

| 功能域 | 职责 |
|--------|------|
| **项目管理** | 创建 / 打开 / 备份 Unity 项目 |
| **VPM 集成** | VRChat Package Manager — 统一包管理 |
| **模板系统** | Avatar / World / UdonSharp 三种项目模板 |
| **SDK 分发** | 2023 年起，SDK 更新仅通过 VCC 推送 |
| **迁移工具** | Legacy `.unitypackage` → VPM 格式自动迁移 |
| **社区仓库** | 第三方 VPM Repo 的添加/管理 |

**平台**: Windows 10/11 (64-bit) — CLI 可运行于 macOS/Linux  
**UI 技术栈**: WebView2（Edge 内核）  
**安装路径**: `%LOCALAPPDATA%\Programs`（可自定义）  
**配置文件**: `%LocalAppData%\VRChatCreatorCompanion\settings.json`

---

## 2. 架构概念

```
┌──────────────────────────────────────────────┐
│              VCC Desktop App                  │
│  ┌────────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Project Mgr│  │ VPM Core │  │ Settings │ │
│  │ (创建/备份) │  │ (依赖解析)│  │ (配置)   │ │
│  └────────────┘  └──────────┘  └──────────┘ │
│         │              │              │       │
│         ▼              ▼              ▼       │
│  ┌──────────────────────────────────────┐    │
│  │         VPM Library (SemVer)         │    │
│  │   依赖解析 · 版本范围 · 包安装/删除    │    │
│  └──────────────────────────────────────┘    │
│         │              │                     │
│         ▼              ▼                     │
│  ┌──────────┐  ┌──────────────┐             │
│  │ Official │  │  Community   │             │
│  │  Repos   │  │   Repos      │             │
│  │(Base/    │  │  (vpm.json)  │             │
│  │ Worlds/  │  │              │             │
│  │ Avatars) │  │              │             │
│  └──────────┘  └──────────────┘             │
└──────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│         Unity Project                 │
│  ┌──────────────────────────────┐    │
│  │ Packages/vpm-manifest.json   │    │
│  │ Packages/com.vrchat.core.    │    │
│  │   vpm-resolver/  ← 自动恢复  │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

---

## 3. 核心工作流

### 3.1 创建新项目

```
VCC → New → 选择模板 (Avatar / World / UdonSharp) → 命名 → Create Project
```

**内部过程**:
1. 创建目录 `{location}/{projectName}`
2. 复制选中模板到目标目录
3. 更新 `ProjectSettings` 中的 `productName`
4. 若失败则删除目录并报错
5. 将项目加入 `userProjects[]` 列表

### 3.2 管理已有项目

```
VCC → Add Existing Project → 选择文件夹 → Manage Project → 勾选/升级包
```

- "Installed Version" = 已安装
- "Not Installed" = 未安装
- 点击 `+` 自动安装最新版
- 版本下拉可查看所有历史版本

### 3.3 迁移 Legacy 项目

```
VCC → Add Existing Project → 检测到 Assets/VRCSDK → 显示 Migrate Project 按钮
```

**两种模式**:
- **Migrate a copy**: 创建 `{ProjectName}-Migrated` 副本（安全）
- **Migrate in place**: 直接原地修改（需有备份）

**迁移排除的文件夹**:
`Library`, `Logs`, `Assets\VRCSDK`, `Assets\Udon`, `Assets\UdonSharp`,
`Assets\VRChat Examples`, `Packages\com.vrchat.vrcsdk3`, `ProjectSettings\ProjectVersion.txt`

**特殊包迁移**: UdonSharp、AudioLink、GestureManager 等 Curated Packages 自动从 `/Assets/` 中替换为新版。

### 3.4 添加社区仓库

```
VCC → Settings → Packages → Add Repository → 输入 URL → Add → 确认
```

- 仓库信息存储在 `settings.json` → `userRepos` 数组
- 可通过 cogwheel 按钮添加自定义 Headers（如私有仓库 Token）
- 每个仓库左侧有勾选框控制启用/禁用

---

## 4. VPM 格式速览

### 4.1 三种官方包

| 包名 | 说明 |
|------|------|
| `com.vrchat.base` | Base SDK（World + Avatar 公用） |
| `com.vrchat.worlds` | Worlds SDK（Udon 支持） |
| `com.vrchat.avatars` | Avatars SDK（Avatars 3.0） |

### 4.2 VPM Manifest 关键字段

```json
{
  "name": "com.author.packagename",
  "displayName": "My Package",
  "version": "1.0.0",
  "vpmDependencies": {
    "com.vrchat.worlds": "3.5.x"
  },
  "legacyFolders": {
    "Assets\\OldFolder": "guid..."
  },
  "legacyFiles": {},
  "legacyPackages": []
}
```

- `vpmDependencies` 使用 SemVer 范围（如 `3.5.x` = `>=3.5.0 <3.6.0`）
- `legacyFolders` 自动检测并移除旧版 `.unitypackage` 目录

### 4.3 版本策略: Branding.Breaking.Bumps

VRChat 官方包的准语义化版本：`{Branding}.{Breaking}.{Bumps}`

| 位 | 含义 | 触发条件 |
|----|------|---------|
| Branding | 重大系统变更 | SDK2→SDK3 (2.x→3.x) |
| Breaking | API 不兼容变更 | 需更新依赖包 |
| Bumps | 常规更新 | Bug 修复 + 新功能 |

> **[FACT]** SDK 3.3.0 首次声明 Public SDK API。该 API 内的接口不会因 Bumps 升级而破坏。

---

## 5. Package Resolver

**[FACT]** `com.vrchat.core.vpm-resolver` 是唯一**不可移除**的 VPM 包。

**工作原理**:
1. Unity 打开项目时，对比 `Packages/vpm-manifest.json` 与实际 `Packages/` 目录
2. 发现缺失 → 弹出对话框提示
3. 自动下载并安装缺失的包（无需 VCC 客户端）

**Git 集成**:
- `.gitignore` 排除所有 `com.vrchat.*` 包，但**保留** `com.vrchat.core.*` (Resolver)
- 克隆后首次打开 Unity → Resolver 自动恢复依赖

---

## 6. 已知问题

| 问题 | 严重度 | 来源 | 状态 |
|------|--------|------|------|
| **"Failed to add Repo" 误报** | 🟡 中等 | `modular-avatar.md §8.2` | VCC 已知 bug，99% 情况仓库已成功添加，点 Cancel 即可 |
| **Pre-release 依赖解析 bug** | 🟡 中等 | `modular-avatar.md` | MA 预发布版在 VCC 中依赖解析失败，建议用 ALCOM |
| **WebView2 白屏** | 🔴 严重 | FAQ | 重装 WebView2 或用 `http://localhost:5476/` 浏览器访问 |
| **长路径导致包丢失** | 🟡 中等 | FAQ | Windows 路径过长，建议 `C:\Projects\` 短路径或启用 Win32 长路径 |
| **settings.json 损坏** | 🔴 严重 | FAQ | 删除 `%LocalAppData%\VRChatCreatorCompanion\settings.json` 后重启 VCC |

---

## 7. CLI (`vpm`)

**[FACT]** VCC 提供独立的 CLI 工具，通过 .NET 8 安装：

```bash
dotnet tool install --global vrchat.vpm.cli
```

**常用命令**:
```bash
vpm new MyProject World              # 创建 World 项目
vpm add package com.vrchat.udonsharp # 安装包
vpm list projects                    # 列出项目
vpm migrate legacy ./MyProject       # 迁移 Legacy 项目
vpm add repo https://example.com/vpm.json  # 添加仓库
vpm install templates                # 安装最新模板
vpm install unity                    # 安装兼容的 Unity 版本
```

> 完整 CLI 参考见 `参考文献/VCC官方文档/15-vpm-cli.md`，包含 `migrate 2022`、`--headers`、`--inplace` 等高级用法。

---

## 8. 定位总结

> VCC = 项目创建器 + 包管理器 + SDK 分发器 + 迁移工具

- **对于 World 创作者**: 创建 World/UdonSharp 项目，管理 UdonSharp/ClientSim/AudioLink 等包
- **对于 Avatar 创作者**: 创建 Avatar 项目，管理 MA/AAO/VRCFury 等 VPM 包
- **对于工具开发者**: 使用 Package Template + Package Listing 模板分发自己的工具

> **与 ALCOM 的关系**: ALCOM 是社区开发的开源替代品，共享配置文件，可共存。详见 `alcom.md`。
