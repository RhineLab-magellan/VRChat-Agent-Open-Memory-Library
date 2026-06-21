---
title: VRChat OSC 协议完整数据库
category: hybrid

knowledge_level: applied
status: active

tags:
  - hybrid
  - osc
  - avatar

aliases:
  - "OSC Protocol"
  - "OSC 协议"
  - "Open Sound Control"
  - OSC

source: docs.vrchat.com + changelog + vrchat-community/osc
source_type: community
version: 1.0
last_review: 2026-06-05
confidence: High
---
# VRChat OSC 协议完整数据库

> 版本: 1.0 | 更新: 2026-06-05 | 来源: docs.vrchat.com + changelog + vrchat-community/osc

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

### 端口配置

| 用途 | 端口 | 说明 |
|------|------|------|
| 接收 (VRChat 监听) | 9000 | 外部应用发送到 VRChat |
| 发送 (VRChat 输出) | 9001 | VRChat 发送到外部应用 |

### 命令行参数

```
--osc=<Port>:<senderIP>:<outPort>
```

### 消息格式

- 地址格式: `/category/endpoint` (必须以 `/` 开头)
- 支持类型: `int`, `float`, `bool` (Avatar Parameters)

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

### 按钮值 (0/1)

| 地址 | 功能 | 平台 |
|------|------|------|
| `/input/Jump` | 跳跃 | Desktop/VR |
| `/input/Run` | 跑步 | Desktop/VR |
| `/input/Voice` | 语音/静音 | Desktop/VR |
| `/input/Use` | 使用 | Desktop/VR |
| `/input/Grab` | 抓取 | VR |
| `/input/Drop` | 放下 | VR |
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

### ⚠️ 官方 OSC 不暴露原始 VR 硬件按键(2026-06-15 补充)

> **🔴 关键约束**: VRChat 官方 OSC Input Control API **只支持语义化输入**(`/input/Jump`、`/input/Use`、`/input/Grab` 等),**不暴露 X/Y/A/B 等原始 VR 硬件按键**。

**【FACT,来源:github.com/vrchat-community/osc/docs/Input.md】**

| 类别 | 地址 | 数量 |
|------|------|------|
| 语义化输入 | Jump/Run/Voice/Use/Grab/Drop/ComfortLeft/ComfortRight/QuickMenuToggleLeft/Right/PanicButton | ~15 个 |
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

> 人体追踪数据输入

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

### 头部对齐

```
/tracking/trackers/head/position  (Vector3)
/tracking/trackers/head/rotation  (Euler)
```

- position 用于空间对齐（无插值）
- rotation 用于偏航对齐（缓慢插值）
- 可单独发送 position 或 rotation

### 限制

- 仅 VR 模式有效
- Desktop 模式不支持

---

## 6. Eye Tracking API

> 眼部追踪数据输入

### 眼睑

| 地址 | 类型 | 说明 |
|------|------|------|
| `/tracking/eye/EyesClosedAmount` | float | 眼睛闭合程度 (0-1) |

### 眼球追踪 (选择一种)

| 地址 | 类型 | 说明 |
|------|------|------|
| `/tracking/eye/CenterPitchYaw` | float[2] | 中心俯仰角+偏航角 |
| `/tracking/eye/CenterPitchYawDist` | float[3] | +距离 |
| `/tracking/eye/CenterVec` | float[3] | 中心方向向量 |
| `/tracking/eye/CenterVecFull` | float[3] | 完整中心向量 |
| `/tracking/eye/LeftRightPitchYaw` | float[4] | 左右分开 |
| `/tracking/eye/LeftRightVec` | float[6] | 左右分开向量 |

### 说明

- 目前仅支持同时控制双眼眨眼
- 未来可能支持单眼眨眼

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

| 地址 | 类型 | 说明 |
|------|------|------|
| `/chatbox/input` | string | 发送聊天消息 |
| `/chatbox/typing` | bool | 打字状态 |

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

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1 | 2026-06-10 | 补充 OSC 库推荐、线程安全、Debug Interface、Input 重置要求、TouchOSC 布局文件 |
| 1.0 | 2026-06-05 | 初始整理 |

## 来源

- docs.vrchat.com（官方文档）
- docs.vrchat.com 更新日志（2025.3.3, 2026.2.1）
- vrchat-community/osc GitHub Wiki
- wiki.vrchat.com
- deepwiki.com/vrchat-community/osc (2026-06-10)

## 备注

- Camera OSC 端点在 creators.vrchat.com 官方文档中**缺失**，仅在 changelog 中出现
- 部分 Camera 端点的值变更通知存在问题（已反馈）
- `/chatbox/input` 参数以知识库为准（单参数 string），DeepWiki 双参数描述待验证

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

### 访问方式

```
Action Menu → OSC → Debug
```

### 功能特性

| 功能 | 说明 |
|------|------|
| **自动激活** | 打开 Debug 界面时自动启用 OSC |
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

### 连续值 (Axes)

| 地址 | 说明 | 重置要求 |
|------|------|----------|
| `/input/Vertical` | 前进(1) / 后退(-1) | **必须重置为 0** |
| `/input/Horizontal` | 右移(1) / 左移(-1) | **必须重置为 0** |
| `/input/LookHorizontal` | 视角左右 / VR快转 | **必须重置为 0** |
| `/input/MoveHoldFB` | 移动持有物体前后 | **必须重置为 0** |
| `/input/SpinHoldCwCcw` | 旋转持有物体 | **必须重置为 0** |

### 按钮值 (Buttons)

| 地址 | 说明 | 重置要求 |
|------|------|----------|
| `/input/Jump` | 跳跃 | **必须重置为 0** |
| `/input/Run` | 跑步 | **必须重置为 0** |
| `/input/Voice` | 语音/静音 | **必须重置为 0** |
| 所有其他按钮 | — | **必须重置为 0** |

### 原因

持续的非零值会导致连续输入（如持续前进、持续旋转）。每次操作后必须重置为 0。

---

## 附录 E: TouchOSC 布局文件

> 来源: vrchat-community/osc Example Files and Configurations

### 布局文件列表

| 文件 | 用途 | 目标 API |
|------|------|----------|
| `vrc-emote.tosc` | Avatar 表情和手势控制 | Avatar Parameters API |
| `vrc-input.tosc` | 游戏输入模拟 | Input Control API |

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

---

## 附录 F: 社区资源管理

> 来源: vrchat-community/osc Community Resources and Tools

### 提交要求

| 要求 | 说明 |
|------|------|
| **文档** | 必须包含清晰的使用说明 |
| **开源** | 源代码必须公开可审查 |
| **许可证** | 必须包含适当的开源许可证 |
| **TOS 合规** | 不得违反 VRChat 服务条款 |

### 提交流程

1. 在 GitHub Discussions 的 "Show and Tell" 分类发布
2. 通过审查标准后纳入官方资源列表

### 安全建议

- 下载应用程序仅来自可信来源
- 使用前验证应用完整性
- 尽可能从源码编译而非使用预编译二进制
- 审查源代码（如果可用）