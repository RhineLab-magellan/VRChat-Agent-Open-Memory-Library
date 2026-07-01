---
title: VRChat Launch Options — 17 个启动选项完整参考
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - launch-options
  - debugging
  - build-test
  - command-line

aliases:
  - Launch Options
  - 启动选项
  - 命令行参数
  - "VRChat CLI"
  - "Command Line"

related:
  - world/udon/using-build-test.md
  - world/udon/debugging-udon-projects.md
  - world/udon/world-debug-views.md
  - world/udon/midi/realtime-midi.md
  - hybrid/osc-protocol.md
  - world/udon/local-storage.md

source: docs.vrchat.com/docs/launch-options
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Launch Options — 17 个启动选项完整参考

> 来源: https://docs.vrchat.com/docs/launch-options
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方启动选项)
> 关联: `world/udon/using-build-test.md` + `world/udon/debugging-udon-projects.md` (部分 flag)

---

## 概述

> [FACT] 启动选项（Launch Options）是 VRChat 启动时的**命令行参数**，**主要用于创建者调试**。
>
> **注意**: 玩家在普通使用中**通常不需要**这些选项。

> [FACT] **3 种设置启动选项的方式**:
> 1. **Steam**: Library → 右键 VRChat → Properties → Set Launch Options
> 2. **Oculus PC / Meta Rift**: 创建 VRChat.exe 快捷方式
> 3. **Oculus Quest**: **不支持**任何启动选项

> [FACT] **Oculus Quest 不支持任何启动选项**（这是平台限制）。

---

## 1. 17 个启动选项完整表

> [FACT] 17 个选项按功能分类。

### 1.1 模式控制（2 个）

| 选项 | 描述 | 用途 |
|------|------|------|
| `--no-vr` | 强制桌面模式 | 调试时不需要 VR |
| `--profile=X` | 指定用户配置（X 是数字，0 = 默认）| 多账号测试 |

> [FACT] `--profile=X` 中 X 是数字，**0 是默认 Profile**。可启动多个 VRChat 实例用不同 Profile 模拟多玩家。

### 1.2 性能控制（3 个）

| 选项 | 描述 | 用途 |
|------|------|------|
| `--fps=X` | 覆盖 FPS 上限 | 调试 FPS 问题 |
| `--enable-amd-stutter-workaround` | AMD 渲染补丁 | 解决 AMD 卡顿 |
| `--disable-hw-video-decoding` | 禁用硬件视频解码 | 调试视频问题 |
| `--enable-hw-video-decoding` | 强制硬件视频解码 | 调试视频问题 |

> [FACT] `--fps=X` 覆盖默认 FPS 限制:
> - **桌面**: 默认 90 FPS
> - **VR**: 默认是头显最大刷新率

> [FACT] 视频解码默认是**硬件**（Windows）。使用 `--disable-hw-video-decoding`（即软件）会用 CPU 解码，**影响性能**。

> [FACT] `--enable-amd-stutter-workaround` 是**渲染补丁**:
> - 解决 AMD 显卡卡顿
> - **不推荐**默认启用（可能引入新卡顿）
> - 仅供高级用户测试

### 1.3 调试（3 个）⭐

| 选项 | 描述 | 用途 |
|------|------|------|
| `--enable-debug-gui` | 启用 Debug GUI | **必备** ⭐ |
| `--enable-sdk-log-levels` | 启用 SDK 详细日志 | 调试 SDK |
| `--enable-udon-debug-logging` | 启用 Udon 详细日志 | **必备** ⭐ |

> [FACT] **3 个调试 flag 详解**:

| Flag | 日志大小 | 性能影响 | 必备 |
|------|---------|----------|------|
| `--enable-debug-gui` | - | 低 | ⭐ 创作者必备 |
| `--enable-sdk-log-levels` | **VERY LARGE** | 中 | SDK 调试时 |
| `--enable-udon-debug-logging` | **较大**（Udon 问题世界）| 中 | Udon 调试时 |

> [FACT] ⚠️ **`--enable-sdk-log-levels` 会让日志文件变得非常大**。
>
> [FACT] ⚠️ **`--enable-udon-debug-logging` 在 Udon 有问题的世界中日志会很大**。
>
> **不要在生产环境保持启用**。

### 1.4 系统（4 个）

| 选项 | 描述 | 用途 |
|------|------|------|
| `--skip-registry-install` | 跳过 `vrchat://` 注册 | 防止 Installation Helper 弹窗 |
| `--ignore-trackers=serial1,serial2` | 忽略特定 Tracker | 调试 Tracker 干扰 |
| `--affinity=<ARG>` | 线程亲和性（hex bitmask）| AMD CCX 优化 |
| `--process-priority=<ARG>` | 进程优先级 | 进程调度 |
| `--main-thread-priority=<ARG>` | 主线程优先级 | 主线程调度 |

> [FACT] `--ignore-trackers=serial1,serial2`:
> - 逗号分隔的**序列号列表**
> - Tracker 序列号含**空格**用 `%20`（如 `Serial%20Number` 对应 "Serial Number"）
> - 用于**排除干扰性 Tracker**（如镜像放置的 Tracker）

> [FACT] `--affinity=<ARG>` 是 **hex bitmask** 字符串:
> - `FFFF` = 前 16 线程
> - `FF` = 前 8 线程
> - 等等
>
> ⚠️ **除非你用有 inter-CCX latency 问题的 AMD CPU，否则不要使用！**
> 用错会导致性能问题。

> [FACT] `--process-priority=<ARG>` 数值:
> - `-2`: Idle
> - `-1`: Below Normal
> - `0`: Normal（默认）
> - `1`: Above Normal
> - `2`: High
>
> ⚠️ **不要**随意设置 — 可能影响系统响应性。

> [FACT] `--main-thread-priority=<ARG>` 数值:
> - `-2`: Lowest
> - `-1`: Below Normal
> - `0`: Normal
> - `1`: Above Normal
> - `2`: Highest
>
> ⚠️ **不要**随意设置。

### 1.5 MIDI（1 个）

| 选项 | 描述 | 用途 |
|------|------|------|
| `--midi=deviceName` | 指定 MIDI 设备 | 多设备时精确选择 |

> [FACT] `--midi=deviceName`:
> - **强制 VRChat 搜索**包含 `deviceName` 的连接设备
> - **支持部分匹配**和**大小写不敏感**
>
> 例: 设备显示为 `SchneebleCo MidiKeySmasher 89`
> ```bash
> --midi=midikeysmasher
> ```
>
> 详见 `world/udon/midi/realtime-midi.md`

### 1.6 测试（3 个）⭐

| 选项 | 描述 | 用途 |
|------|------|------|
| `--watch-worlds` | 监听 World Build & Reload | **必备** ⭐ |
| `--watch-avatars` | 监听 Avatar Build & Reload | **必备** ⭐ |
| `--enforce-world-server-checks` | 强制服务端 World 校验 | 调试服务端检查 |

> [FACT] `--watch-worlds` 详解:
> - 监听 VRChat SDK 构建世界的目录
> - **新世界构建后自动加入**（本地实例）
> - 配合 `Build & Reload` 大幅加速迭代
> - 详见 `world/udon/using-build-test.md` §5.4

> [FACT] `--watch-avatars` 详解:
> - 监听 VRChat SDK 构建测试 Avatar 的目录
> - **新 Avatar 构建后自动切换**到新版本（如果在穿测试 Avatar）
> - 与 `--watch-worlds` **对称**（World 热重载 vs Avatar 热重载）
>
> **Memory 库之前未记录 `--watch-avatars`** — 本文补全。

> [FACT] `--enforce-world-server-checks`:
> - **手动启用**服务端 World 处理
> - 加入 World 前**必须**先通过服务端检查
> - 用于**调试 World 失败服务端检查**的问题

### 1.7 OSC（1 个）⚠️ 格式修正

| 选项 | 描述 | 用途 |
|------|------|------|
| `--osc=inPort:outIP:outPort` | 自定义 OSC 网络设置 | 多 OSC 应用并存 |

> [FACT] ⚠️ **`--osc` 官方格式**（来自 `launch-options.md`）:
>
> ```
> --osc=inPort:outIP:outPort
> ```
>
> 接受 3 个参数:
> - **inPort**: VRChat 监听 OSC 输入的端口
> - **outIP**: VRChat 发送 OSC 输出的目标 IP
> - **outPort**: VRChat 发送 OSC 输出的目标端口
>
> **Memory 库 `hybrid/osc-protocol.md` 中的格式 `--osc=<Port>:<senderIP>:<outPort>` 是简略或不准确的。**
>
> **本文以 user-guide 官方格式为准** — 见 §4 修正。

### 1.8 Unity 原生（4 个）

| 选项 | 描述 | 用途 |
|------|------|------|
| `-screen-width N` | 屏幕宽度 | 调试 |
| `-screen-height N` | 屏幕高度 | 调试 |
| `-screen-fullscreen N` | 全屏（0 或 1）| 调试 |
| `-monitor N` | 显示器索引（1-based）| 调试 |

> [FACT] 这些是 **Unity 引擎原生参数**，不是 VRChat 特有。
>
> Unity 文档: https://docs.unity3d.com/Manual/CommandLineArguments.html
>
> ⚠️ **不要**使用 `force` 系列参数（会让 VRChat 不可用）。

---

## 2. 创作者推荐组合

> [FACT] 创作者调试 World 的推荐组合:

```bash
VRChat.exe \
  --no-vr \
  --enable-debug-gui \
  --enable-sdk-log-levels \
  --enable-udon-debug-logging \
  --watch-worlds \
  --profile=0 \
  -screen-width 1920 \
  -screen-height 1080
```

**详解**:
- `--no-vr`: 桌面模式（不需要 VR）
- `--enable-debug-gui`: 启用 Debug GUI
- `--enable-sdk-log-levels`: SDK 详细日志
- `--enable-udon-debug-logging`: Udon 详细日志
- `--watch-worlds`: 监听 World Build & Reload
- `--profile=0`: 默认账号
- 屏幕 1920x1080

### 2.1 多 Profile 测试

```bash
# 终端 1 (Profile 0 = Master)
VRChat.exe --no-vr --watch-worlds --profile=0

# 终端 2 (Profile 1 = 普通玩家)
VRChat.exe --no-vr --watch-worlds --profile=1
```

> [FACT] 多 Profile 用于**多客户端测试**（模拟多玩家）。

### 2.2 MIDI 设备指定

```bash
VRChat.exe --no-vr --midi=midikeysmasher --enable-debug-gui
```

> [FACT] 当多 MIDI 设备时，指定设备名可避免自动选择第一个设备。

---

## 3. AMD Inter-CCX Latency 优化

> [FACT] 来自社区贡献（"Fallen Ninja" on VRChat），**未经 VRChat 团队直接验证**。

### 3.1 何时使用

> [FACT] 如果你有**多 CCX 的 AMD CPU**（大多数 1000/2000/3000 系列和部分 5000/7000 系列），使用 `--affinity` 限制**仅用第一个 CCX** 可以**减少 inter-core communication latency**，**获得显著 FPS 提升**。

### 3.2 推荐配置

查询 CPU "Core config"（https://en.wikipedia.org/wiki/List_of_AMD_Ryzen_processors），看 `Nx` 中 `x` 前面的数字：

| 配置 | Affinity 字符串 |
|------|----------------|
| 2 | `--affinity=F` |
| 3 | `--affinity=3F` |
| 4 | `--affinity=FF` |
| 6 | `--affinity=FFF` |
| 8 | `--affinity=FFFF` |

> ⚠️ **不要**关闭 SMT（除非你知道自己做什么）。
>
> ⚠️ **不要**在 Intel CPU 上用 `--affinity`。

### 3.3 工具

> [FACT] 工具: https://bitsum.com/tools/cpu-affinity-calculator/

---

## 4. ⚠️ 已知冲突修正

### 4.1 `--osc` 格式冲突

> **Memory 库 `hybrid/osc-protocol.md` (第 1 章 OSC 基础)** 写:
> ```
> --osc=<Port>:<senderIP>:<outPort>
> ```
>
> **user-guide 官方 `launch-options.md`** 写:
> ```
> --osc=inPort:outIP:outPort
> ```
>
> **分析**:
> - `osc-protocol.md` 把 in 和 out **混在一起**为单 `<Port>`
> - 官方是 **3 段**: inPort / outIP / outPort
>
> **建议**: Memory 库 `osc-protocol.md` 应**修正**为官方格式。
>
> **本文档**采用官方格式。

### 4.2 `--watch-avatars` vs `--watch-worlds` 对称

> [FACT] **user-guide 揭示 Memory 库缺失**:
> - `--watch-worlds` 已在 `using-build-test.md` 详细记录
> - `--watch-avatars` **未记录**（对称功能）
>
> **Memory 库补全**:
> - `--watch-avatars` 监听 Avatar Build 目录
> - 自动切换到新版本（穿测试 Avatar 时）

---

## 5. 常见错误

> [FACT] **常见错误**:

| 错误 | 原因 | 解决 |
|------|------|------|
| **Oculus Quest 上设 flag 无效** | Quest 不支持 | 用 PC 调试 |
| **`--affinity` 用错导致性能下降** | 误用 | 仅 AMD 多 CCX CPU 用 |
| **生产环境保持 `--enable-sdk-log-levels`** | 日志巨大 | 调试完移除 |
| **多 Profile 启动冲突** | 配置目录问题 | 用不同 Steam 账号 / 配置路径 |
| **Unity `force` 参数让 VRChat 崩溃** | VRChat 不支持 | 不要用 |

---

## 6. 平台支持

> [FACT] 各平台支持:

| 平台 | 启动选项支持 |
|------|------------|
| **Steam (PC)** | ✅ 完整 |
| **Oculus PC / Meta Rift** | ✅ 通过快捷方式 |
| **Oculus Quest** | ❌ 不支持 |
| **Pico** | ❌ 不支持 |
| **Viveport** | ❌ 不支持 |

---

## 7. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `world/udon/using-build-test.md` | 5.4 节涵盖 `--watch-worlds` 详细用法 |
| `world/udon/debugging-udon-projects.md` | 3 个调试 flag 详细用法 |
| `world/udon/world-debug-views.md` | Debug GUI 视图 |
| `world/udon/midi/realtime-midi.md` | `--midi` flag 详细 |
| `hybrid/osc-protocol.md` | ⚠️ 需修正 `--osc` 格式 |
| `world/udon/local-storage.md` (待建) | 日志文件位置 |

---

## 8. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ `--watch-avatars` 是否需要 Build & Test 启用
2. ❓ `--enforce-world-server-checks` 的具体服务端检查内容
3. ❓ `--midi=deviceName` 多设备并存的优先级
4. ❓ `--affinity` 在 Apple Silicon Mac 上的行为（不适用）
5. ❓ Linux/Wine 下的支持（VRChat 不支持，但可能有 hack）
6. ❓ 17 个选项的**完整版本历史**（哪些是新加的）

---

## 来源

- [VRChat Launch Options](https://docs.vrchat.com/docs/launch-options)
- [Unity Standalone Player Command Line Arguments](https://docs.unity3d.com/Manual/CommandLineArguments.html)
- 本地化版本: `参考文献/SP/user-guide/launch-options.md`
- 相关: `hybrid/osc-protocol.md` (Memory 库) — `--osc` 格式需修正
