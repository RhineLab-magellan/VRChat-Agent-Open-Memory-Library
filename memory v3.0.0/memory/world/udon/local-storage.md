---
title: VRChat Local Storage — 本地文件系统与注册表
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - local-storage
  - appdata
  - registry
  - local-player-moderations

aliases:
  - Local VRChat Storage
  - 本地存储
  - AppData LocalLow
  - LocalPlayerModerations
  - 本地玩家管理
  - 日志文件
  - VRChat Cache
  - "AppData"

related:
  - world/udon/debugging-udon-projects.md
  - world/udon/launch-options.md
  - world/udon/persistence/index.md
  - world/udon/persistence/player-data.md
  - api/persistence.md
  - avatar/safety-system.md

source: docs.vrchat.com/docs/local-vrchat-storage
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Local Storage — 本地文件系统与注册表

> 来源: https://docs.vrchat.com/docs/local-vrchat-storage
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方本地存储文档)
> 关联: `world/udon/debugging-udon-projects.md` (日志文件位置) + `world/udon/persistence/index.md` (PlayerData)

---

## 概述

> [FACT] VRChat 在本地存储**多种**数据。
>
> 本文档列出**非穷尽**的存储位置和**用途**。
>
> **创作者需要知道**这些位置，因为:
> - **调试**需要查看日志 (`output_log`)
> - **Udon 持久化** 写入 `LocalAvatarData` / `PlayerData`
> - **玩家屏蔽** 数据存储在 `LocalPlayerModerations`
> - **Asset 缓存** 在 `Cache-WindowsPlayer`

> **🔴 关键事实**: 主存储位置是 `%UserProfile%\AppData\LocalLow\VRChat\VRChat\`（Windows）。

---

## 1. AppData LocalLow 完整目录表

> [FACT] 主存储位置: `%UserProfile%\AppData\LocalLow\VRChat\VRChat\`

### 1.1 完整文件/文件夹清单

| 文件/文件夹 | 用途 | 备注 |
|------|------|------|
| `output_log_yyyy-MM-dd_HH-mm-ss.txt` | **应用程序日志**（含 Udon 调试输出）| 时间戳表示**客户端启动时间**<br>**24 小时**后自动删除 |
| `config.json` | **配置文件**（应用设置）| 详见 [Configuration File](https://docs.vrchat.com/docs/configuration-file) |
| `Cache-WindowsPlayer\` | **资源下载缓存**（Avatar / World / 图像等）| 可在 `config.json` 中重新配置到**其他盘** |
| `Avatars\` | **本地测试 Avatar**（Build & Test 输出）| - |
| `OSC\` | **OSC 设置存储**（即使不用 OSC 也可能存在）| - |
| `LocalAvatarData\` | **Avatar 参数存储**（已穿戴 Avatar 的参数）| - |
| `Tools\` | **额外应用程序**（目前仅含 video URL parser）| - |
| `LocalPlayerModerations` | **本地玩家管理**（用户间操作）| 目前仅 **Show/Hide Avatar**<br>详见 §2 |

### 1.2 日志文件命名

> [FACT] `output_log_yyyy-MM-dd_HH-mm-ss.txt` 命名规则:
> - **每次启动** VRChat 生成**新文件**
> - 时间戳表示**客户端启动时间**（HH-mm-ss）
> - **24 小时后**自动删除

> **调试相关性**: 创作者调试时需用 `--enable-udon-debug-logging` 启动才会输出 Udon 详细信息
> （详见 `world/udon/debugging-udon-projects.md`）

### 1.3 配置缓存位置

> [FACT] `Cache-WindowsPlayer` 位置**可重新配置**:
> - 在 `config.json` 中设置
> - **目的**: 移动到**容量更大**的盘
>
> 详见 `world/udon/configuration-file.md` (待建)

### 1.4 Avatars 目录

> [FACT] `Avatars\` 用于**本地测试 Avatar**:
> - "Build and Test" 功能输出的 **测试 Avatar** 文件
> - **不进** VRChat 上传系统
> - 本地调试用

### 1.5 OSC 目录

> [FACT] `OSC\` 存储:
> - 使用 OSC **所需数据**
> - **可能存在**即使玩家**不用 OSC**
> - 详见 `hybrid/osc-protocol.md`

### 1.6 LocalAvatarData 目录

> [FACT] `LocalAvatarData\` 存储:
> - **已穿戴 Avatar 的参数**
> - 与 **PlayerData** 不同
> - 详见 `world/udon/persistence/index.md`

### 1.7 Tools 目录

> [FACT] `Tools\` 存储**额外应用程序**:
> - 目前**仅**含 **video URL parser**
> - VRChat 用于解析视频 URL 的工具

### 1.8 LocalPlayerModerations 文件

> [FACT] `LocalPlayerModerations` 存储:
> - 玩家对其他用户的**"player moderations"**（已保存的操作）
> - 目前**仅** **"Show Avatar"** 和 **"Hide Avatar"** 操作
> - 详见 §2 文件格式

---

## 2. LocalPlayerModerations 文件格式 ⭐

> [FACT] **CRITICAL: 创作者可理解的二进制/文本混合格式**

### 2.1 文件格式定义

> [FACT] **存储行格式** (Storage line format):
> ```
> <key><padding><value><newline>
>  |    |        |      |
>  |    |        |      +-> "\r\n" (CRLF)
>  |    |        +--------> 3 bytes, human-readable decimal, 0-prefixed (e.g. 127, 004, 012)
>  |    +-----------------> ' ' (padded by spaces up to 64)
>  +----------------------> UTF-8 encoded key
> ```

### 2.2 字段详解

| 字段 | 类型 | 描述 |
|------|------|------|
| `key` | UTF-8 字符串 | 用户标识（VRChat 用户 ID） |
| `padding` | 空格 | 补足到 **64 字符** |
| `value` | 3 字节十进制 | 0-prefixed 数字（如 `127`, `004`, `012`）|
| `newline` | `\r\n` | CRLF |

### 2.3 当前值定义

> [FACT] 目前**只有 2 个可能的 value**:
>
> | Value | 含义 |
> |-------|------|
> | `004` | **Hide Avatar**（隐藏该用户的 Avatar）|
> | `005` | **Show Avatar**（显示该用户的 Avatar）|

### 2.4 创作者影响

> [FACT] **创作者角度**:
> - **不能直接访问/修改** `LocalPlayerModerations`
> - 玩家**隐藏你的 Avatar** 时 = `004` 记录
> - **此文件是本地存储** — VRChat 平台**不强制**该设置
> - **重新安装** VRChat = 清空此文件

> **社区/调试角度**:
> - 此格式**公开**，第三方工具可读写
> - 理论上可制作 **Avatar 黑名单管理工具**

---

## 3. 临时文件

> [FACT] VRChat 和其依赖可能在**各种临时文件夹**存储数据。
> 列表**非穷尽**。

### 3.1 临时分析文件

> [FACT] 位置: `%TEMP%\VRChat\VRChat`
>
> 用途: **Analytics 文件**（分析数据）临时存储
>
> 详情:
> - VRChat 为开发目的**收集分析数据**
> - 详见 [Privacy Policy](https://hello.vrchat.com/privacy)
> - **用户可拒绝**（在 VRChat 设置中）

---

## 4. Windows 注册表

> [FACT] VRChat 在 `HKCU\Software\VRChat\vrchat` 存储**玩家偏好设置**。
>
> 方式: 通过 [Unity PlayerPrefs API](https://docs.unity3d.com/2019.4/Documentation/ScriptReference/PlayerPrefs.html)
>
> 影响:
> - 注册表项**可在 Editor 调试**
> - 玩家可通过 **regedit** 查看/修改
> - **创作者无法** 在 Udon 中直接读写

### 4.1 常见 PlayerPrefs 项

> [FACT] 常见项包括（基于 Unity PlayerPrefs 惯例）:
> - **音视频设置**（音量、麦克风等）
> - **UI 偏好**（菜单位置、显示选项）
> - **性能选项**（分辨率、FPS 限制）
> - **键位绑定**（在 Settings 菜单中改）

> **注意**: 注册表项**与 `config.json` 不同**。
> - `config.json` = 应用主配置
> - 注册表 = Unity PlayerPrefs 偏好

---

## 5. 平台特定存储

> [FACT] **当前文档仅涵盖 Windows**。
>
> 推测其他平台:
> - **Android (Quest)**: `/sdcard/Android/data/com.vrchat.vrchat/files/`
> - **macOS**: `~/Library/Application Support/VRChat/VRChat/`
> - **Linux/Wine**: 兼容性**不官方支持**（见 `world/development/vm-setup.md`）

> **🔴 验证状态**: macOS / Quest / Linux 路径**未在官方文档中明确**，需通过实践或第三方资料验证。

---

## 6. 创作者调试速查

### 6.1 日志查看流程

> [FACT] **调试 Udon**:
> 1. **启动 VRChat** 时带 `--enable-udon-debug-logging` flag
> 2. **实时查看**: `Debug GUI` 覆盖层（`Right Shift + Backtick + 3`）
> 3. **历史查看**: 打开 `%UserProfile%\AppData\LocalLow\VRChat\VRChat\output_log_*.txt`
> 4. **看持久化**: 检查 `LocalAvatarData\` 目录

### 6.2 缓存清理

> [FACT] 何时**清理**本地存储:
> - **Avatar 显示异常** → 清理 `Cache-WindowsPlayer\Avatars\`
> - **World 加载异常** → 清理 `Cache-WindowsPlayer\Worlds\`
> - **OSC 不工作** → 检查 `OSC\` 目录
> - **持久化数据异常** → 谨慎清理 `LocalAvatarData\`

> **⚠️ 警告**: 清理 `LocalAvatarData\` = **丢失所有已穿戴 Avatar 的 PlayerData**！

### 6.3 性能优化

> [FACT] **性能优化建议**:
> - 移动 `Cache-WindowsPlayer` 到 **SSD**（在 `config.json` 配置）
> - 定期清理**旧日志**（24h 自动清理 + 手动清理）
> - 关闭 VRChat 时**确保正常退出**（避免临时文件残留）

---

## 7. 隐私与安全

> [FACT] **隐私考虑**:
> - VRChat 收集**分析数据**（在 `%TEMP%\VRChat\VRChat`）
> - 用户**可拒绝**（在 VRChat 设置中）
> - 详见 [Privacy Policy](https://hello.vrchat.com/privacy)

> **创作者角度**:
> - Udon Debug Log **可能**包含**玩家数据**（注意日志清理）
> - **不要**在 `Debug.Log` 中输出**敏感信息**（密码、token 等）

---

## 8. 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 找不到 `output_log` | 没启用 `--enable-udon-debug-logging` | 启动时加 flag |
| 找不到 `Cache-WindowsPlayer` | VRChat 未启动过 / 路径被改 | 检查 `config.json` |
| 持久化数据丢失 | 误删 `LocalAvatarData\` | **永远不要**手动删除 |
| 玩家 Avatar 仍显示（已 hide） | 浏览器/注册表缓存 | 重启 VRChat |
| `%TEMP%` 临时文件巨大 | 多次崩溃未清理 | 手动清理 `%TEMP%\VRChat\VRChat` |

---

## 9. 玩家常见问题

### Q1: 我的日志在哪里?

> `%UserProfile%\AppData\LocalLow\VRChat\VRChat\output_log_*.txt`

### Q2: 我想清理 VRChat 缓存但不丢数据?

> **安全清理**:
> - `Cache-WindowsPlayer\Avatars\` ✅
> - `Cache-WindowsPlayer\Worlds\` ✅
> - `OSC\` ✅
> - 临时文件 ✅
>
> **危险清理**:
> - `LocalAvatarData\` ❌（丢持久化）
> - `LocalPlayerModerations` ❌（丢黑名单）
> - `config.json` ❌（恢复默认设置）

### Q3: 我隐藏了某玩家的 Avatar，但重新登录后又看到?

> - **检查** `LocalPlayerModerations` 是否存在
> - **不要** 移动/重命名 `AppData\LocalLow\VRChat\`
> - 检查 VRChat **重新安装**（会清空）

### Q4: macOS/Quest 的路径是?

> **未在官方文档明确**。需通过实践验证。

---

## 10. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `world/udon/debugging-udon-projects.md` | 日志文件位置、Debug GUI 启动 |
| `world/udon/launch-options.md` | `--enable-udon-debug-logging` 等调试 flag |
| `world/udon/persistence/index.md` | `LocalAvatarData` 详解 |
| `world/udon/persistence/player-data.md` | PlayerData 写入 `LocalAvatarData` |
| `api/persistence.md` | 持久化 API |
| `avatar/safety-system.md` | LocalPlayerModerations 来源 |
| `world/development/vm-setup.md` | Linux/Wine 兼容性 |

---

## 11. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **macOS** 的本地存储路径
2. ❓ **Quest (Android)** 的本地存储路径
3. ❓ **Linux/Wine** 的本地存储路径
4. ❓ `LocalPlayerModerations` 是否有**未公开的 value**（除 004/005）
5. ❓ `Tools\` 目录未来会增加什么应用
6. ❓ `config.json` 完整字段列表
7. ❓ **Quest** 上 `LocalAvatarData` 是否存在（Quest 没有 PlayerData API）
8. ❓ **磁盘配额** 限制（每个文件夹大小）
9. ❓ **多用户** Windows 账号的存储隔离
10. ❓ **加密** 状态（哪些数据加密存储）

---

## 来源

- [VRChat Local VRChat Storage](https://docs.vrchat.com/docs/local-vrchat-storage)
- [VRChat Configuration File](https://docs.vrchat.com/docs/configuration-file)
- [Unity PlayerPrefs API](https://docs.unity3d.com/2019.4/Documentation/ScriptReference/PlayerPrefs.html)
- 本地化版本: `参考文献/SP/user-guide/local-vrchat-storage.md`
