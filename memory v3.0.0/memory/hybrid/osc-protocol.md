---
title: "VRChat OSC 协议完整数据库"
category: hybrid
knowledge_level: applied
status: active
source: "docs.vrchat.com + changelog + vrchat-community/osc + VRChat 2025.4.2p1 Release Notes"
source_type: community
version: 1.3
last_review: 2026-06-30
confidence: High
tags:
  - hybrid
  - osc
  - avatar
aliases:
  - "OSC Protocol"
  - "OSC 协议"
  - "Open Sound Control"
  - OSC
related:
  - audio-link.md
  - alcom.md
  - udon-world-plugins.md
  - vcc.md
  - "../avatar/full-body-tracking.md"
---
# VRChat OSC 协议完整数据库

> 版本: 1.2 | 更新: 2026-06-30 | 来源: docs.vrchat.com + changelog + vrchat-community/osc

---

## 目录

1. [OSC 基础](#1-osc-基础)
2. [Avatar Parameters API](#2-avatar-parameters-api)
3. [Avatar Scaling API](#3-avatar-scaling-api)
4. [Input Control API](#4-input-control-api)
5. [Tracking API](#5-tracking-api)
6. [Eye Tracking API](#6-eye-tracking-api)
7. [Camera API](#7-camera-api-202533-新增)
8. [Chatbox API](#8-chatbox-api)
9. [OSCQuery 自动发现](#9-oscquery-自动发现)

---

## 1. OSC 基础

> **OSC 定义**: Open Sound Control 是设备/应用间通信协议，源于 Stanford CNMAT。
> 出处: https://opensoundcontrol.stanford.edu/index.html

### 端口配置

| 用途 | 端口 | 说明 |
|------|------|------|
| 接收 (VRChat 监听) | 9000 | 外部应用发送到 VRChat |
| 发送 (VRChat 输出) | 9001 | VRChat 发送到外部应用 |

### 命令行参数

```
--osc=<inPort>:<senderIP>:<outPort>
```

| 完整命令示例 | 用途 |
|-------------|------|
| `--osc=9000:127.0.0.1:9001` | 默认配置（与无参数等价） |
| `--osc=9000:localhost:9001` | `localhost` 与 `127.0.0.1` 等价 |
| `--osc=9000:192.168.1.42:9001` | 跨设备（VRChat 推送到 192.168.1.42） |

### 消息格式 (2026-06-30 新增)

- **结构**: 一个 OSC 消息 = 地址 (address) + 值 (value)
- **地址**: `/category/endpoint` 形式，**必须以 `/` 开头**，用 `/` 分隔层级
  - 例: `/avatar/parameters/VRCEmote`
- **值类型**: Avatar Parameters 仅支持 `int` / `float` / `bool`
- **传输**: 单连接单向（Sender → Receiver），**UDP 无握手**
  - 启动顺序无关（Sender/Receiver 谁先启动都行）
  - 没有连接建立/断开过程

### 启用方法 (2026-06-30 新增)

```
Action Menu → OSC → Enabled
```

开启后 OSC 默认监听 9000 端口接收外部消息。

---

## 2. Avatar Parameters API

> 控制 Avatar 参数，支持输入和输出

### 地址格式

```
/avatar/parameters/{ParameterName}
/avatar/change  (Avatar 切换通知)
```

### Avatar 切换

| 地址 | 类型 | 说明 |
|------|------|------|
| `/avatar/change` | string | 当本地玩家加载新 Avatar 时发送，包含 Avatar ID |

### 内置只读参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `VRCEmote` | int | 默认动画 (1-16) |
| `VRCFaceBlendV` | float | 面部混合 V |
| `VRCFaceBlendH` | float | 面部混合 H |
| `PreviewMode` | int | 菜单预览中=1，否则=0 |
| `IsOnFriendsList` | bool | 观看者是否是穿着者好友 |
| `IsAnimatorEnabled` | bool | Animator 是否启用 |
| `AvatarVersion` | int | SDK3=3，否则=0 |

### 手势参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `GestureRight` | int | 右手手势 (0-7) |
| `GestureLeft` | int | 左手手势 (0-7) |
| `GestureRightWeight` | float | 右手手势权重 (0.0-1.0) |
| `GestureLeftWeight` | float | 左手手势权重 (0.0-1.0) |

### 缩放参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `ScaleModified` | bool | 是否修改过缩放 |
| `ScaleFactor` | float | 当前高度/默认高度 |
| `ScaleFactorInverse` | float | 1/ScaleFactor |
| `EyeHeightAsMeters` | float | 眼睛高度（米） |
| `EyeHeightAsPercent` | float | 眼睛高度百分比 |

### 声音参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `Viseme` | int | 嘴型 (0-14) |
| `Voice` | float | 麦克风音量 (0.0-1.0) |
| `Earmuffs` | bool | 耳塞模式 |
| `MuteSelf` | bool | 自我静音 |

### 玩家状态参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `AFK` | bool | 离开 |
| `InStation` | bool | 在载具中 |
| `Seated` | bool | 坐着 |
| `VRMode` | int | VR模式=1 |
| `TrackingType` | int | 追踪点数 |

### 位置参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `Grounded` | bool | 触地 |
| `Upright` | float | 直立程度 (0-1) |
| `AngularY` | float | Y轴角速度 |
| `VelocityX` | float | 右向速度 (m/s) |
| `VelocityY` | float | 向上速度 (m/s) |
| `VelocityZ` | float | 前进速度 (m/s) |
| `VelocityMagnitude` | float | 总速度 |

### TrackingType 值

| 值 | 说明 |
|----|------|
| 0 | 未初始化 |
| 1 | Generic 骨骼 |
| 2 | 仅手部追踪（过渡状态） |
| 3 | 3点追踪（头+手）/ Desktop 人形 |
| 4 | 4点追踪（+臀部） |
| 5 | 5点追踪（+脚） |
| 6 | 6点全身追踪 |

### 手势值 (GestureLeft/Right)

| 值 | 手势 |
|----|------|
| 0 | 空 |
| 1 | 张开 |
| 2 | 拳头 |
| 3 | 手掌 |
| 4 | 指向 |
| 5 | 耶 |
| 6 | 好 |
| 7 | 停 |

### 嘴型值 (Viseme)

| 值 | 嘴型 |
|----|------|
| 0 | sil |
| 1 | PP |
| 2 | FF |
| 3 | TH |
| 4 | DD |
| 5 | kk |
| 6 | CH |
| 7 | SS |
| 8 | nn |
| 9 | RR |
| 10 | aa |
| 11 | E |
| 12 | I |
| 13 | O |
| 14 | U |

### 配置文件

路径: `~\AppData\LocalLow\VRChat\VRChat\OSC\{userId}\Avatars\{avatarId}.json`

```json
{
    "id": "avtr_xxx",
    "name": "AvatarName",
    "parameters": [
        {
            "name": "Face",
            "input": { "address": "/avatar/parameters/Face", "type": "Int" },
            "output": { "address": "/custom/app/trackselect", "type": "Float" }
        }
    ]
}
```

### 📦 字段类型与大小写敏感性 (2026-06-30 修正)

| 端点 | 合法 type 值 | 大小写 |
|------|-------------|--------|
| `input.type` | `"Int"` / `"Bool"` / `"Float"` | **大写** |
| `output.type` | `"Int"` / `"bool"` / `"Float"` | **注意**：`"bool"` 是**小写**！ |

> 旧版文档未明确大小写敏感性，**这是常见错误源**。

### ⚠️ Build & Test 行为 (2026-06-30 新增)

- **Build & Test 模式不会保存配置文件**到磁盘
- 可以使用 OSC，但 `~\AppData\LocalLow\...` 路径下看不到配置文件
- 配置文件仅在 **Published Avatar**（发布后的 Avatar）加载时才会读取/生成

### ⚠️ Stop-gap 临时方案 (2026-06-30 新增)

> 配置文件系统是 VRChat 的**临时方案**，目的是在客户端内 OSC UI 集成完成前允许部分定制。
>
> **未来可能移除**。长期依赖此功能的用户应关注 VRChat 公告并准备迁移。

---

## 3. Avatar Scaling API

> Avatar 缩放控制

### 眼睛高度端点

| 地址 | 类型 | 权限 | 说明 |
|------|------|------|------|
| `/avatar/eyeheight` | float | 读/写 | 当前眼睛高度（米） |
| `/avatar/eyeheightmin` | float | 只读 | 最小可选高度（默认0.2） |
| `/avatar/eyeheightmax` | float | 只读 | 最大可选高度（默认5.0） |
| `/avatar/eyeheightscalingallowed` | bool | 只读 | 是否允许 OSC 缩放 |

### 眼睛高度范围

- 最小值: 0.01m (1cm)
- 最大值: 10000m (10km)
- 官方支持范围: 0.1m - 100m
- 超出官方范围会显示警告

### 🎮 Udon 强制覆盖 (2026-06-30 新增)

> 关键：世界脚本（Udon）**可强制覆盖**用户或 OSC 设置的 eye height，绕过 `eyeheightmin`/`eyeheightmax` UI 限制。

**回环机制**（事件流）：
1. 收到用户/OSC 设置的 eye height（作为事件）
2. 收到 Udon 强制覆盖的实际值（作为事件）
3. 监听端可观察两个事件以区分意图

### ⚠️ 越界警告与免责声明 (2026-06-30 新增)

| 行为 | 说明 |
|------|------|
| 越界显示 | eye height < 0.1m 或 > 100m 时，HUD 会显示警告 |
| **官方支持** | 仅 0.1m - 100m |
| **免责** | 越界时出现的问题**不支持**联系 VRChat 客服或提交 bug 报告 |

### /avatar/scale (2026.2.1 新增)

支持超出默认 UI 限制的更大缩放。

---

## 4. Input Control API

> 模拟用户输入

### 连续值 (-1 到 1)

| 地址 | 功能 |
|------|------|
| `/input/Vertical` | 前进(1) / 后退(-1) |
| `/input/Horizontal` | 右移(1) / 左移(-1) |
| `/input/LookHorizontal` | 视角左右 / VR快转 |
| `/input/MoveHoldFB` | 移动持有物体前后 |
| `/input/MoveHoldLR` | 移动持有物体左右 |
| `/input/SpinHoldCwCcw` | 旋转持有物体 |
| `/input/SpinHoldUD` | 旋转持有物体 上下 |
| `/input/SpinHoldLR` | 旋转持有物体 左右 |
| `/input/UseAxisRight` | 右手使用轴 **[UNKNOWN]** 源文档标注 "not sure if this works"，待官方确认 |
| `/input/GrabAxisRight` | 右手抓取轴 **[UNKNOWN]** 源文档标注 "not sure if this works"，待官方确认 |

### 保持式移动按钮 (2026-06-30 新增)

| 地址 | 功能 |
|------|------|
| `/input/MoveForward` | 保持前进（区别于 Vertical axis） |
| `/input/MoveBackward` | 保持后退 |
| `/input/MoveLeft` | 保持左移 |
| `/input/MoveRight` | 保持右移 |
| `/input/LookLeft` | 保持视角左转（Desktop 平滑，VR 在 Comfort Turning 开启时为快转） |
| `/input/LookRight` | 保持视角右转（同上） |

### 按钮值 (0/1)

> **🔴 2026-06-30 修正**: 源文档 **不提供通用名** `Use`/`Grab`/`Drop`，仅保留 VR 专用分支 `UseRight`/`UseLeft`/`GrabRight`/`GrabLeft`/`DropRight`/`DropLeft`。

| 地址 | 功能 | 平台 |
|------|------|------|
| `/input/Jump` | 跳跃 | Desktop/VR |
| `/input/Run` | 跑步 | Desktop/VR |
| `/input/Voice` | 语音/静音（双模式行为见下） | Desktop/VR |
| `/input/ComfortLeft` | 快转左 | VR |
| `/input/ComfortRight` | 快转右 | VR |
| `/input/GrabRight` | 右手抓取 | VR |
| `/input/GrabLeft` | 左手抓取 | VR |
| `/input/DropRight` | 右手放下 | VR |
| `/input/DropLeft` | 左手放下 | VR |
| `/input/UseRight` | 右手使用 | VR |
| `/input/UseLeft` | 左手使用 | VR |
| `/input/QuickMenuToggleLeft` | 左手快捷菜单 | VR |
| `/input/QuickMenuToggleRight` | 右手快捷菜单 | VR |
| `/input/PanicButton` | 安全模式 | Desktop/VR |

### Voice 双模式行为 (2026-06-30 新增)

| 模式 | 行为 |
|------|------|
| **Toggle Voice 开启**（Settings） | `/input/Voice` 从 0→1 切换静音状态，之后必须重置为 0。**按住 1 时不能用控制器/键盘切换** |
| **Toggle Voice 关闭**（默认） | Push-To-Mute 模式：0 = 静音，1 = 解除静音 |

### 🔔 Voice 音量滑块范围提醒 (2025.4.2+ Steam Audio)

> **FACT** (2025.4.2 Steam Audio 替换 ONSP):Voice 音量滑块的**等效范围发生变化**。
> - 旧音频系统:Voice 滑块 100% ≈ 100% 实际输出
> - 新音频系统:Voice 滑块 100% ≈ 150% 实际输出
> - **等效值**:**新 65% ≈ 旧 100%**

#### 影响范围

| 对象 | 影响 |
|------|------|
| **教程/教学用户** | 提醒"调回 100% 会非常响" |
| **OSC 应用** | 如果通过 OSC 设置用户 Voice 音量,**需考虑新等效值** |
| **第三方工具** | 旧值映射需更新 |

#### 文档引用

> 完整内容详见 `memory/world/audio-steam.md` §"Voice 音量滑块范围变更"

### ⚠️ 官方 OSC 不暴露原始 VR 硬件按键(2026-06-15 补充 / 2026-06-30 修正)

> **🔴 关键约束**: VRChat 官方 OSC Input Control API **只支持语义化输入**(`/input/Jump`、`/input/UseRight`、`/input/GrabRight` 等),**不暴露 X/Y/A/B 等原始 VR 硬件按键**。

**【FACT,来源:github.com/vrchat-community/osc/docs/Input.md】**

| 类别 | 地址 | 数量 |
|------|------|------|
| 语义化输入 | Jump/Run/Voice/UseRight/UseLeft/GrabRight/GrabLeft/DropRight/DropLeft/ComfortLeft/ComfortRight/QuickMenuToggleLeft/Right/PanicButton | ~17 个 |
| 原始 VR 硬件按键 | X/Y/A/B/Trigger Touch/Grip Touch 等 | **0 个(不支持)** |

### 监听 X 键的 OSC 方案(必须用第三方)

VRChat 官方未提供 `/input/Oculus_Cross_Left` 之类的地址。**要让外部应用监听 X 键的 OSC,必须用第三方桥接程序**:

| 方案 | 机制 | 备注 |
|------|------|------|
| **I5UCC/VRCThumbParamsOSC** | 读取 SteamVR Controller Actions,转 OSC | 开源、活跃,推荐 |
| **VRChat Inputs Spreadsheet** | 仅文档参考,非 OSC | 社区维护的轴名清单 |

#### I5UCC/VRCThumbParamsOSC 命名约定

注意该项目的 A/B 命名约定是 **Oculus Touch 命名**(对应物理按键 X/Y):

| OSC 参数(Avatar) | 物理按键 | 说明 |
|------------------|---------|------|
| `/avatar/parameters/LeftAButton` | **左手 X** 键 | Bool |
| `/avatar/parameters/LeftBButton` | **左手 Y** 键 | Bool |
| `/avatar/parameters/RightAButton` | **右手 A** 键 | Bool |
| `/avatar/parameters/RightBButton` | **右手 B** 键 | Bool |
| `/avatar/parameters/LeftThumb` | 左手拇指位置 | Int 0-4 (0=无,1=A/X,2=B/Y,3=Trackpad,4=Thumbstick) |
| `/avatar/parameters/RightThumb` | 右手拇指位置 | Int 0-4 |
| `/avatar/parameters/ControllerType` | 控制器类型 | Int 0/1/2/10/11/12 |

支持设备:**Valve Index / Meta Touch / SteamVR Trackers / XInput Controllers**。

**使用方式**:
1. 安装并运行 VRCThumbParamsOSC 作为后台进程
2. 它读取 SteamVR Controller Actions
3. 通过 OSC 发送为 Avatar Parameters(给本地 Avatar)
4. Avatar 的 Expression Parameters 资产中添加对应参数(`LeftAButton` 等)
5. 外部应用监听 `/avatar/parameters/LeftAButton` 即可

**延迟**:本地 Avatar 端 OSC 入站约 50-200ms,适合非实时场景(直播控台、统计),不适合精确计时。

### 替代方案:Udon 内直接读取

如果不需要外部应用,直接在 Udon 中用 Unity Input API 读取 X 键(详见 `memory/world/udon/input-events.md` "精确按键识别限制"章节):

```csharp
bool xHeld = Input.GetButton("Oculus_CrossPlatform_Button2");
```

---

## 5. Tracking API

> 人体追踪数据输入（Full Body IK）

### 追踪器地址 (8个追踪器)

```
/tracking/trackers/{1-8}/position  (Vector3: X,Y,Z)
/tracking/trackers/{1-8}/rotation  (Vector3: Euler角度)
```

### 追踪器映射

| 编号 | 位置 |
|------|------|
| 1 | 臀部 (Hip) |
| 2 | 胸部 (Chest) |
| 3 | 脚1 (Foot 1) |
| 4 | 脚2 (Foot 2) |
| 5 | 膝盖1 (Knee 1) |
| 6 | 膝盖2 (Knee 2) |
| 7 | 手肘1 (Elbow 1) |
| 8 | 手肘2 (Elbow 2) |

### 追踪空间假设 (2026-06-30 新增)

| 项 | 值 | 说明 |
|----|----|------|
| 坐标系 | Unity 左手坐标系 | +y up, +x right, +z forward |
| 单位 | 1.0f = 1m | 发送端需用户输入真实身高做缩放 |
| Euler 顺序 | Z, X, Y | 内部分别应用生成四元数 |
| 方向约定 | 与 SteamVR 追踪器一致 | 复用 VRChat 现有实现 |

### ⚠️ 发送数量建议 (2026-06-30 新增)

> 📘 **少而准优于多而差**
>
> - 追踪数据越少（高准确度），VRChat IK 补偿效果越好
> - 初始阶段建议**仅发送脚+臀**（3-4 个追踪器）
> - 追踪数据绝对位置/旋转无漂移时，才逐步增加追踪点
> - 8 个全开不一定带来更好效果，可能引入更多抖动

### 头部对齐

```
/tracking/trackers/head/position  (Vector3)
/tracking/trackers/head/rotation  (Euler)
```

- position 用于空间对齐（**无插值**，每帧完全对齐）
- rotation 用于偏航对齐（**缓慢 lerp**）
- 可单独发送 position / rotation / 两者 / 都不发

### 🕐 Head Rotation 300ms 阈值 (2026-06-30 新增)

| 行为 | 触发条件 | VRChat 反应 |
|------|---------|-------------|
| **单次消息** | 仅一条 head rotation 消息，300ms 内无后续 | 一次性即时对齐 yaw（不 lerp） |
| **持续流** | 300ms 内收到第二条 head rotation | 进入正常 lerp 模式 + 10 秒数据超时 |
| **位置/旋转分离** | position 单独发 | 仅做位置对齐，**不会触发 yaw 对齐** |
| **仅旋转无位置** | rotation 单独发 | 仅做 yaw 对齐 |

> **使用场景**: 单次模式适合发送端没有稳定头戴传感器时（例如校准过程中用户被假定面朝前方）。

### Auto-center OSC Trackers 按钮 (2026-06-30 新增)

> 🚧 **该按钮部分文档可能已过时**

- **位置**: Quick Menu → Tracking & IK → 齿轮图标
- **功能**: 自动找 Y 轴最低的 2 个追踪器，其中点对齐到用户头部位置正下方
- **前向推断**: 假设最低的 2 个追踪器是左右脚，由此推断前向
- **方向切换**: 反复点击按钮会在两个前向方向间切换（因为仅靠 Y 高度无法判断前后）

### Tracker Models 调试模式 (2026-06-30 新增)

- **位置**: Quick Menu → Tracking & IK → 齿轮图标 → Tracker display model
- **设置 "Tracker: System"**: 模型**校准后仍保持显示**，便于调试 OSC 追踪数据流

### 头部对齐细节

- `position` 与 avatar 头部骨骼（**不是眼位**）位置对齐
- 整个 OSC 追踪空间平移以使 `head/position` 对齐到头骨根
- `rotation` 假定 Euler(0,0,0) = 中性面朝前

### 限制

- 仅 VR 模式有效
- Desktop 模式不支持

---

## 6. Eye Tracking API

> 眼部追踪数据输入（VR 模式）

### 眼睑

| 地址 | 类型 | 说明 |
|------|------|------|
| `/tracking/eye/EyesClosedAmount` | float | 眼睛闭合程度 (0-1)，同时控制双眼 |

### 眼球追踪 (选择一种)

> 🚧 **同时仅支持一个 eye-look 地址**
>
> 发送多个不同格式的 eye-look 地址可能产生未定义行为。建议仅实现其中 1-2 种格式。

| 地址 | 类型 | 说明 |
|------|------|------|
| `/tracking/eye/CenterPitchYaw` | float[2] | 中心俯仰角+偏航角 (°) |
| `/tracking/eye/CenterPitchYawDist` | float[3] | +距离 (m) |
| `/tracking/eye/CenterVec` | float[3] | 中心方向向量（归一化，raycast 找距离） |
| `/tracking/eye/CenterVecFull` | float[3] | 完整中心向量（**长度有意义**，单位 m 决定 raycast 距离） |
| `/tracking/eye/LeftRightPitchYaw` | float[4] | 左右分开 pitch+yaw |
| `/tracking/eye/LeftRightVec` | float[6] | 左右分开方向向量 |

### 🕐 10 秒超时 (2026-06-30 新增)

> **关键行为**: 10 秒未收到数据后，眼动行为恢复默认值（自动看 / 自动眨眼）。

| 数据类型 | 独立超时 |
|---------|---------|
| 眼睑 (`EyesClosedAmount`) | ✅ 独立计时 |
| 眼球追踪 (eye-look) | ✅ 独立计时 |

### Unity 坐标约定 (2026-06-30 新增)

| 项 | 值 |
|----|---|
| 坐标系 | 左手（与 HMD 局部一致） |
| 方向约定 | +x right, +y up, +z forward |
| pitch 正值 | **朝下** |
| yaw 正值 | **朝右** |

### 案例参考数据 (2026-06-30 新增)

> 用户 IPD = 64mm，眼目标：头部上方 15°，右方 20°，距离 50cm

| 端点 | 案例数据 |
|------|---------|
| `CenterPitchYaw` | `-15.252, 20.128` |
| `CenterPitchYawDist` | `-15.252, 20.128, 0.503` |
| `CenterVec` | `0.332, 0.263, 0.905` |
| `CenterVecFull` | `0.167, 0.132, 0.456` |
| `LeftRightPitchYaw` | `-14.903, 23.592, -15.560, 16.503` |
| `LeftRightVec` | `0.387, 0.257, 0.886, 0.274, 0.268, 0.923` |

### 实现参考

- **官方 Gist 示例**: https://gist.github.com/vrchat-developer/bc07d3dba46206f6ee42d36323c034eb
- 假设项目有 "eye root" + "eye target" Transform，需设置用户 IPD
- **不要直接复制**——是教学参考，需根据实际情况调整

### 说明

- 目前仅支持同时控制双眼眨眼
- 未来可能支持单眼眨眼
- 地址**大小写敏感**

---

## 7. Camera API (2025.3.3 新增)

> 相机控制端点，约30+个，全部支持读写

### 模式

| 地址 | 类型 | 值 |
|------|------|-----|
| `/usercamera/Mode` | int | 0:关闭 1:照片 2:直播 3:Emoji 4:多层 5:打印 6:无人机 |

### 姿态

| 地址 | 类型 | 说明 |
|------|------|------|
| `/usercamera/Pose` | Vector3+Quaternion | 位置和旋转 |

### 动作

| 地址 | 类型 | 说明 |
|------|------|------|
| `/usercamera/Close` | - | 关闭相机 |
| `/usercamera/Capture` | - | 拍照 |
| `/usercamera/CaptureDelayed` | - | 定时拍照 |

### 切换 (bool)

| 地址 | 说明 |
|------|------|
| `/usercamera/ShowUIInCamera` | UI 遮罩 |
| `/usercamera/Lock` | 锁定 |
| `/usercamera/LocalPlayer` | 本地玩家遮罩 |
| `/usercamera/RemotePlayer` | 远程玩家遮罩 |
| `/usercamera/Environment` | 环境遮罩 |
| `/usercamera/GreenScreen` | 绿幕 |
| `/usercamera/SmoothMovement` | 平滑移动 |
| `/usercamera/LookAtMe` | 看我行为 |
| `/usercamera/AutoLevelRoll` | 自动水平翻滚 |
| `/usercamera/AutoLevelPitch` | 自动水平俯仰 |
| `/usercamera/Flying` | 飞行模式 |
| `/usercamera/TriggerTakesPhotos` | 触发拍照 |
| `/usercamera/DollyPathsStayVisible` | 路径可见 |
| `/usercamera/CameraEars` | 相机音频 |
| `/usercamera/ShowFocus` | 对焦叠加 |
| `/usercamera/Streaming` | Spout 推流 |
| `/usercamera/RollWhileFlying` | 飞行时翻滚 |
| `/usercamera/OrientationIsLandscape` | 横屏方向 |

### 滑块 (float)

| 地址 | 默认 | 范围 | 说明 |
|------|------|------|------|
| `/usercamera/Zoom` | 45 | 20-150 | 缩放 |
| `/usercamera/Exposure` | 0 | -10~10 | 曝光 |
| `/usercamera/FocalDistance` | - | - | 焦距 |
| `/usercamera/Aperture` | - | - | 光圈 |
| `/usercamera/Hue` | - | - | 绿幕色调 |
| `/usercamera/Saturation` | - | - | 绿幕饱和度 |
| `/usercamera/Lightness` | - | - | 绿幕亮度 |
| `/usercamera/LookAtMeXOffset` | - | - | LAM X偏移 |
| `/usercamera/LookAtMeYOffset` | - | - | LAM Y偏移 |
| `/usercamera/FlySpeed` | - | - | 飞行速度 |
| `/usercamera/TurnSpeed` | - | - | 转向速度 |
| `/usercamera/SmoothingStrength` | - | - | 平滑强度 |
| `/usercamera/PhotoRate` | - | - | 路径拍照速率 |
| `/usercamera/Duration` | - | - | 路径持续时间 |

---

## 8. Chatbox API

> 聊天输入和状态

### 地址

| 地址 | 签名 | 说明 |
|------|------|------|
| `/chatbox/input` | `(string text, bool send, bool notify)` | 发送聊天消息（**3 参数**，见下） |
| `/chatbox/typing` | `(bool)` | 打字状态 |

### 📦 `/chatbox/input` 3 参数签名 (2026-06-30 修正)

> **🔴 关键修正**: 旧版"单参数 string"是**错误**的。官方明确为 3 参数 `s b n`。

| 位置 | 参数 | 类型 | 默认 | 含义 |
|------|------|------|------|------|
| `s` | text | string | — | 聊天框文本 |
| `b` | send | bool | — | `True` 立即发送（绕过键盘）；`False` 打开键盘预填充 |
| `n` | notify | bool | `True` | `False` 静音通知音效；省略时默认触发音效 |

### 📏 Chatbox 显示限制 (2026-06-30 新增)

| 限制 | 值 |
|------|---|
| 字符数上限 | **144 字符** |
| 显示行数上限 | **9 行**（含换行与折行） |

超出限制的内容会被截断/省略。

---

## 9. OSCQuery 自动发现

> VRChat 2023.3.1+ 支持

### 功能

- mDNS/Bonjour 服务发现
- TCP 查询地址空间和值
- 自动配置 IP 和端口

### VRChat 接收的 OSCQuery 路径

| 路径 | 说明 |
|------|------|
| `/avatar` | /avatar/change + /avatar/parameters/* |
| `/tracking/vrsystem` | /tracking/vrsystem/head, /leftwrist, /rightwrist, /pose |

### 参考资源 (2026-06-30 新增)

| 资源 | 链接 | 用途 |
|------|------|------|
| **OSCQuery 规范** | https://github.com/Vidvox/OSCQueryProposal | 协议规范 |
| **VRChat Wiki** | https://github.com/vrchat-community/osc/wiki/OSCQuery | VRChat 集成指南 |
| **官方 C# 库** | https://github.com/vrchat-community/vrc-oscquery-lib | 开源 OSCQuery 库 |
| **VRChat 起始版本** | 2023.3.1 | OSCQuery 支持起点 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **1.2** | **2026-06-30** | **重大修正**: 1) Chatbox `/chatbox/input` 3 参数签名 2) 删除 Input 通用名 (Use/Grab/Drop) 3) 修正 Debug 路径 4) 补充 Eye Tracking 10s 超时 + 互斥规则 + 案例数据 5) 补充 Tracker 300ms 阈值 + 坐标约定 + 数量建议 + Auto-center 6) 补充 Avatar Scaling Udon 强制覆盖 + 越界免责 7) 补充 Build & Test 行为 + stop-gap 警告 + type 大小写 8) 补充 TouchOSC 直链 + OSCQuery 链接 + 实现 Gist 链接 9) 新增附录 G(实现参考) + 附录 H(资源分类索引) |
| 1.1 | 2026-06-10 | 补充 OSC 库推荐、线程安全、Debug Interface、Input 重置要求、TouchOSC 布局文件 |
| 1.0 | 2026-06-05 | 初始整理 |

## 来源

- docs.vrchat.com（官方文档）— 2026-06-30 抓取 (本次审计主源)
- docs.vrchat.com 更新日志（2025.3.3, 2026.2.1）
- vrchat-community/osc GitHub Wiki
- wiki.vrchat.com
- deepwiki.com/vrchat-community/osc (2026-06-10)
- 参考文献/SP/osc/*.md (2026-06-30 抓取自 docs.vrchat.com/llms.txt)

## 备注

- Camera OSC 端点在 creators.vrchat.com 官方文档中**缺失**，仅在 changelog 中出现
- 部分 Camera 端点的值变更通知存在问题（已反馈）
- ~~`/chatbox/input` 参数以知识库为准（单参数 string）~~ **已修正 2026-06-30**：`/chatbox/input` 官方为 3 参数签名 `s b n`（text + send-bool + notify-bool），源见 `osc-as-input-controller.md §Chatbox`

---

## 附录 A: 推荐 OSC 库

> 来源: vrchat-community/osc DIY Integration Guide

### 官方推荐库

| 语言 | 库 | 仓库 | 说明 |
|------|-----|------|-----|
| C# | OscCore | vrchat/osccore (all-in-one branch) | VRChat 客户端内部使用，性能最佳 |
| Python | python-osc | attwad/python-osc | VRChat 团队内部测试使用 |
| 多种 | CNMAT OSC | cnmat.org/OpenSoundControl | 社区参考，全面语言支持 |

### OscCore 特点

- 性能优化：最小内存分配
- 高吞吐量消息处理
- 减少垃圾回收开销

---

## 附录 B: 线程安全注意事项

> 来源: vrchat-community/osc DIY Integration Guide

### 关键要求

| 阶段 | 说明 |
|------|------|
| **接收** | OSC 数据接收发生在后台线程 |
| **传输** | Unity 应用必须将数据转到主线程 |
| **处理** | 使用线程安全的数据结构进行线程间通信 |

### 推荐实现模式

```
1. OSC Receiver 在后台线程捕获数据
2. 将数据存储在线程安全的 buffer 中
3. 主应用线程在 Update/帧循环中处理 buffer 中的数据
```

### 错误处理建议

- 消息验证
- 超时处理（针对期望的响应）
- 网络中断的优雅处理

---

## 附录 C: Debug Interface 完整说明

> 来源: vrchat-community/osc Debugging OSC

### 访问方式 (2026-06-30 修正)

```
Action Menu → OSC → OSC Debug
```

> **修正**: 正确路径是 **OSC → OSC Debug**（不是 OSC → Debug）。

### 功能特性

| 功能 | 说明 |
|------|------|
| **自动激活** | 打开 Debug 界面时**自动启用 OSC**（即使之前在 Action Menu 中禁用了 OSC） |
| **实时监控** | 显示传入 OSC 消息 |
| **参数验证** | 显示地址、值范围、当前值 |

### 显示内容

- OSC 地址 (e.g., `/avatar/parameters/parameterName`)
- 值范围 (预期范围)
- 当前值 (实时数据)

### 限制

| 限制项 | 说明 |
|--------|------|
| 仅传入消息 | 不显示 VRChat 发出的消息 |
| 内部变化不显示 | 不显示 VRChat 内部参数变化 |
| 网络问题不可见 | 防火墙/端口配置问题不会在界面体现 |
| 性能影响 | 高频消息可能影响性能 |

---

## 附录 D: Input 值重置要求

> 来源: vrchat-community/osc Avatar Parameters and Input Control

### 🔴 通用规则 (2026-06-30 强化)

> **所有 axes 和 buttons 在每次操作后都必须重置为 0**。
> 持续的非零值会导致连续输入（如持续前进、持续旋转）。
> 下列表格仅列示例，**未列出的端点同样适用此规则**。

### 连续值 (Axes)

| 地址 | 说明 | 重置要求 |
|------|------|----------|
| `/input/Vertical` | 前进(1) / 后退(-1) | **必须重置为 0** |
| `/input/Horizontal` | 右移(1) / 左移(-1) | **必须重置为 0** |
| `/input/LookHorizontal` | 视角左右 / VR快转 | **必须重置为 0** |
| `/input/MoveHoldFB` | 移动持有物体前后 | **必须重置为 0** |
| `/input/SpinHoldCwCcw` | 旋转持有物体 | **必须重置为 0** |
| `/input/SpinHoldUD` | 旋转持有物体 上下 | **必须重置为 0** |
| `/input/SpinHoldLR` | 旋转持有物体 左右 | **必须重置为 0** |
| 所有其他 axes | — | **必须重置为 0** |

### 按钮值 (Buttons)

| 地址 | 说明 | 重置要求 |
|------|------|----------|
| `/input/Jump` | 跳跃 | **必须重置为 0** |
| `/input/Run` | 跑步 | **必须重置为 0** |
| `/input/Voice` | 语音/静音 | **必须重置为 0** |
| `/input/MoveForward` | 保持前进 | **必须重置为 0** |
| `/input/MoveBackward` | 保持后退 | **必须重置为 0** |
| `/input/MoveLeft` | 保持左移 | **必须重置为 0** |
| `/input/MoveRight` | 保持右移 | **必须重置为 0** |
| `/input/LookLeft` | 保持视角左转 | **必须重置为 0** |
| `/input/LookRight` | 保持视角右转 | **必须重置为 0** |
| 所有其他按钮 | — | **必须重置为 0** |

### 原因

持续的非零值会导致连续输入（如持续前进、持续旋转）。每次操作后必须重置为 0。

> ⚠️ **特别注意 `send=True` 误用**: Chatbox `/chatbox/input` 第二个参数 `send` 也需要重置回 `False`，否则会持续发送。

---

## 附录 E: TouchOSC 布局文件

> 来源: vrchat-community/osc Example Files and Configurations

### 布局文件列表 (2026-06-30 补充直链)

| 文件 | 用途 | 目标 API | 直链 |
|------|------|----------|------|
| `vrc-emote.tosc` | Avatar 表情和手势控制 | Avatar Parameters API | https://github.com/vrchat-community/osc/raw/main/files/touch-osc/vrc-emote.tosc |
| `vrc-input.tosc` | 游戏输入模拟（含 Vertical/Horizontal/Jump） | Input Control API | https://github.com/vrchat-community/osc/raw/main/files/touch-osc/vrc-input.tosc |

### 使用方法

1. 将 `.tosc` 文件传输到移动设备
2. 在 TouchOSC 中导入布局
3. 配置 OSC 连接指向 VRChat（通常是 `localhost:9000`）
4. 使用界面控制 Avatar 参数或游戏输入

### 布局文件格式

- 文件扩展名: `.tosc`
- 内容: 编码的 UI 布局定义、控制映射、OSC 路由
- 兼容性: TouchOSC 1.x 和 2.x
- 平台: iOS、Android、桌面跨平台

### 配置文件示例

- **Avatar Config**: https://github.com/vrchat-community/osc/raw/main/files/avatar-parameters/configs/example-avatar-config.json

---

## 附录 F: 社区资源管理

> 来源: vrchat-community/osc Community Resources and Tools

### ⚠️ 整体安全警告 (2026-06-30 强化)

> **🔴 USE THESE AT YOUR OWN RISK!**
>
> 运行他人编写的代码**本质上就有风险**。下列大多数项目都是开源的，可自行审查安全性。
> **强烈建议**:
> - 阅读源代码而非使用预编译二进制
> - 仅从可信来源下载
> - 使用前验证应用完整性

### 提交要求

| 要求 | 说明 |
|------|------|
| **文档** | 必须包含清晰的使用说明 |
| **开源** | 源代码必须公开可审查 |
| **许可证** | 必须包含适当的开源许可证 |
| **TOS 合规** | 不得违反 VRChat 服务条款 |

### 提交流程

1. 在 GitHub Discussions 的 "Show and Tell" 分类发布
2. 通过审查标准后纳入官方资源列表（官方每周更新）

---

## 附录 G: OSC 实现参考 (2026-06-30 新增)

> 来源: 官方 Developer Gist 仓库

| 主题 | 链接 | 说明 |
|------|------|------|
| **Eye Tracking** | https://gist.github.com/vrchat-developer/bc07d3dba46206f6ee42d36323c034eb | 假设有 eye root + eye target Transform，需设置 IPD，**不要直接复制** |
| **Full Body Trackers** | https://gist.github.com/vrchat-developer/129c1647667945158b14709f8d65d471 | 假设有用于位姿追踪的 avatar 骨骼，需根据实际身高调整 |

### Gist 使用约定

- 均为**教学参考**，不是即用方案
- 需根据实际项目结构调整
- 阅读代码理解原理，不要盲目复制

---

## 附录 H: 社区资源分类索引 (2026-06-30 新增)

> ⚠️ **不收录完整链接列表**（维护成本高、链接易失效），仅保留分类索引。
> 完整列表见源文档 `参考文献/SP/osc/osc-resources.md`

| 类别 | 典型项目（标杆） | 用途 |
|------|----------------|------|
| **Controllers** | BrainFlowsIntoVRChat, VRChat Hotkeys OSC | 脑电、键盘热键 → Avatar |
| **Face Tracking** | VSeeFace, VRCFaceTracking | 面部/唇动 → Avatar |
| **Hand Tracking** | leapmotion-osc | Leap Motion 手指追踪 |
| **Haptics** | bHaptics VRChat-OSC | bHaptics 触觉反馈 |
| **Heart Rate** | HRPresence, OyasumiVR, Pulsoid | 心率 → Avatar (睡眠检测等) |
| **IRL Control** | vrc-osc-audio-controls, vrcwatch | 系统音频、时间、CPU/RAM |
| **Library** | OscCore (官方), phorcys, VRC_OSCLib | OSC 库 (C#/Rust) |
| **Text** | TTS-Voice-Wizard | TTS → Avatar 显示 |
| **Twitch** | Spooder, EZTwitchOSCBot | Twitch 直播联动 |
| **Utilities** | VRCOSC, Protokol, TouchOSC | 综合 OSC 工具 |

> 维护建议：仅在调研具体功能时按类别查找项目，**不要逐个跟踪更新状态**。