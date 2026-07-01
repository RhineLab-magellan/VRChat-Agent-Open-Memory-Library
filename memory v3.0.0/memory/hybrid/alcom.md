---
title: "ALCOM (Alternative Creator Companion)"
category: hybrid
knowledge_level: applied
status: active
source: "https://vrc-get.anatawa12.com/en/alcom/ + https://wiki.vrchat.com/wiki/Community:Alternative_Creator_Companion (Tier B 社区来源)"
source_type: community
version: "1.1.x (2025-11)"
last_review: 2026-07-01
confidence: High
tags:
  - hybrid
  - alcom
  - vrc-get
  - toolchain
  - vpm
  - open-source
aliases:
  - ALCOM
  - "Alternative Creator Companion"
  - "vrc-get GUI"
related:
  - vcc.md
  - "../sources/vpm-package-template.md"
  - audio-link.md
  - osc-protocol.md
  - udon-world-plugins.md
---

# ALCOM — Alternative Creator Companion

> **Domain**: Hybrid（Avatar + World 共享 Base 基础设施）
> **定位**: VCC 的开源高性能替代品
> **作者**: anatawa12 + 40 contributors
> **仓库**: https://github.com/vrc-get/vrc-get
> **许可证**: MIT

---

## 1. 概述

**[FACT]** ALCOM 是社区开发的 VRChat Creator Companion (VCC) 替代方案，基于以下技术栈：

| 组件 | 技术 |
|------|------|
| 底层 CLI | `vrc-get`（Rust 编写） |
| GUI 框架 | Tauri + Next.js |
| Web 渲染 | WebView2 (Win) / WKWebView (macOS) / webkit2gtk (Linux) |

**核心定位**:
- 提供 VCC **全部功能** + 额外增强
- **跨平台**: Windows / macOS / Linux
- 与 VCC **共享配置文件**（`settings.json`），无需迁移即可切换

---

## 2. 相比 VCC 的增强特性

| 特性 | ALCOM | VCC |
|------|-------|-----|
| **跨平台** | ✅ Windows / macOS / Linux | ❌ 仅 Windows GUI |
| **并行下载** | ✅ 多包同时安装 | ❌ 串行安装 |
| **本地缓存** | ✅ 已下载包本地缓存复用 | ❌ 每次重新下载 |
| **安装速度** | **显著更快**（秒级完成） | 标准速度 |
| **多语言** | ✅ 中/英/日/法/德/繁中 | ❌ 仅英文 |
| **Changelog 直达** | ✅ 更新时直接显示 | ❌ 需手动查找 |
| **开源** | ✅ MIT License | ❌ 闭源 |
| **包管理器安装** | ✅ winget / Homebrew / Scoop / AUR | ❌ 仅手动安装 |

---

## 3. 安装方式

### Windows
```bash
winget install anatawa12.ALCOM
# 或下载 .exe / .zip: https://github.com/vrc-get/vrc-get/releases
```

### macOS
```bash
brew install --cask alcom
# 或下载 .dmg
```

### Linux
- AppImage / DEB / RPM
- Arch AUR: `yay -S alcom`

---

## 4. 与 VCC 的关系

**[FACT]** ALCOM 设计为与 VCC **无缝共存**：

- 使用相同的 `settings.json`（项目列表、仓库列表共享）
- **无需迁移** — 安装 ALCOM 后自动识别 VCC 管理的项目
- 可以随时在两个工具之间切换

```
VCC settings.json  ←── 共享 ──→  ALCOM settings.json
        │                                │
        ▼                                ▼
    VCC 管理项目                    ALCOM 管理项目
   (相同项目列表)                  (相同项目列表)
```

---

## 5. vrc-get CLI（底层引擎）

ALCOM 的底层是 `vrc-get` — 一个用 Rust 编写的 VPM CLI 实现。

**相比官方 `vpm` CLI 的优势**:
- Rust 原生性能（vs .NET 8 运行时）
- 支持并行包解析/下载
- 跨平台原生支持

```bash
# 基本用法（与 vpm 类似）
vrc-get repo add https://vpm.anatawa12.com/vpm.json
vrc-get install com.anatawa12.avatar-optimizer
```

---

## 6. 已知问题 / 限制

| 问题 | 严重度 | 说明 | 状态 |
|------|--------|------|------|
| **ALCOM 创建 World 项目 InputManager 不完整** | 🔴 严重 | ALCOM 创建的项目只有 18 个默认轴（无 VR 预设），直接使用 Input 系统会失败 (vrc-get/vrc-get#1899) | ✅ 2025-02 已修复 |
| **Linux 支持非官方** | 🟡 中等 | Linux 版为社区尽力维护，无主要维护者使用 Linux | 持续中 |
| **部分 VCC 功能可能滞后** | 🟡 中等 | VCC 新功能可能在 ALCOM 中延迟支持 | 跟随中 |

> **[FACT]** 对于 World 项目创建，即使 InputManager 问题已修复，仍建议优先用 VCC 创建项目，然后用 ALCOM 管理包。

---

## 7. 推荐使用场景

| 场景 | 推荐 | 原因 |
|------|------|------|
| **批量安装/更新包** | ALCOM | 并行下载 + 缓存，速度优势明显 |
| **macOS / Linux 用户** | ALCOM | VCC 无 GUI 可用 |
| **MA 预发布版安装** | ALCOM | VCC 依赖解析有 bug |
| **中文用户** | ALCOM | 原生简体中文界面 |
| **创建 World 项目** | VCC | 确保 InputManager 完整（历史原因） |
| **首次安装 Unity + SDK** | VCC | 官方引导流程更完整 |

---

## 8. 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.1.5 | 2025-11-16 | 最新 GUI 版本 |
| v1.1.0-beta.1 | 2025-05-25 | 最新 Beta |
| v1.0.1 | 2025-02-23 | 当前稳定版 |
| v1.0.0 | 2025-01-15 | 首个正式版 |
| v0.1.0 | 2024-04-18 | 初始预览版 |

---

## 9. 生态关联

- **AAO (Avatar Optimizer)**: 作者同为 anatawa12，VPM 仓库 `https://vpm.anatawa12.com/vpm.json`
- **vrc-get CLI**: 被部分 CI/CD pipeline 用作 `anatawa12/sh-actions/resolve-vpm-packages`
- **VCC 官方**: VCC 若出现依赖解析问题，官方文档有时建议 "用 ALCOM 代替 VCC"
