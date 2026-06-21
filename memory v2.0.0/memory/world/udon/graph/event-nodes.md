---
title: Udon Event Nodes | 事件节点
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - networking
  - pickup
  - event

aliases:
  - "事件"

related:
  - index.md
  - graph-elements.md
  - special-nodes.md
  - api/events-reference.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Udon Event Nodes | 事件节点

> 来源: https://creators.vrchat.com/worlds/udon/graph/event-nodes/
> 更新日期: 2025-11-25
> 索引日期: 2026-06-15
> Domain: World / Udon

Udon 中所有"Event" 类别节点的清单。脚本通过 Event 监听行为并触发逻辑链。

> **Input Events** 有专门页面(本文件不覆盖)。要跳转到 Graph 中的 Event:在 **Graph Sidebar** 中点击它。
> 列表中所有节点在需要 Flow 的位置都有 Flow 端口。
>
> 📌 与 Networking 直接相关的事件在 **Network Components 页面**单独列出(本文件不重复)。

> **注意**: 所有节点的返回类型均为 `System.Void`(Advanced Notes 中明确说明)

---

## Interact(本地玩家交互)

> **本地玩家**与此 GameObject 交互时触发。

**条件**:
- GameObject 必须有 `Collider` 组件
- GameObject 必须有 `UdonBehaviour` 组件

> 如果要玩家与 2D UI 交互,使用 **VRC Ui Shape + Button** 组件。

---

## Pickup 相关(本地玩家)

| Event | 触发时机 |
|-------|---------|
| `OnDrop` | 本地玩家**持有后放下**此对象 |
| `OnPickup` | 本地玩家**拾起**此对象 |
| `OnPickupUseDown` | 本地玩家**持有并按下 "Use" 按钮**(按下瞬间),需要 Desktop 的 `'Auto Hold'` |
| `OnPickupUseUp` | 本地玩家**持有并松开 "Use" 按钮**(松开瞬间),需要 Desktop 的 `'Auto Hold'` |

---

## Player Join / Leave / Restore

| Event | 输出 | 触发时机 |
|-------|------|---------|
| `OnPlayerJoined` | `player` : `VRC.SDKBase.VRCPlayerApi` | 任何玩家**加入实例**时触发。`player` 为加入者 |
| `OnPlayerLeft` | `player` : `VRC.SDKBase.VRCPlayerApi` | 任何玩家**离开实例**时触发。`player` 为离开者 |
| `OnPlayerRestored` | `player` : `VRC.SDKBase.VRCPlayerApi` | 玩家的**所有持久化数据**完成加载后触发(包括 PlayerData 和 PlayerObjects) |

### Join/Restore 行为说明

> **当你加入一个实例时**:
> - 你会执行**实例内所有玩家**(包括你自己)的 `OnPlayerJoined`
> - 你会执行**实例内所有玩家**(包括你自己)的 `OnPlayerRestored`
>
> **当其他玩家加入你的实例时**:
> - 你只执行**该加入玩家**的 `OnPlayerJoined` 和 `OnPlayerRestored`

> **【推断】** 这意味着 `OnPlayerJoined` 不仅用于"迎接新玩家",也常用于**初始化本地数据**(比如为每个在线玩家创建 UI 列表)

---

## Station(本地玩家)

| Event | 触发时机 |
|-------|---------|
| `OnStationEntered` | 本地玩家**进入**此对象上的 Station |
| `OnStationExited` | 本地玩家**离开**此对象上的 Station |

---

## Video(本地 VideoPlayer)

| Event | 触发时机 |
|-------|---------|
| `OnVideoEnd` | 视频播放**结束**(自然结束或玩家交互) |
| `OnVideoError` | 视频加载**出错**。输出 `videoError` : `VRC.SDK3.Components.Video.VideoError` |
| `OnVideoLoop` | 视频**完成一次循环**(仅当循环启用) |
| `OnVideoPause` | 视频**暂停** |
| `OnVideoPlay` | 视频**开始播放**(新视频开始/取消暂停/玩家交互) |
| `OnVideoStart` | 视频**从停止状态开始播放** |
| `OnVideoReady` | VideoPlayer **加载新视频就绪** |

### Video Events 区分

| Event | 与 OnVideoPlay 的区别 |
|-------|---------------------|
| `OnVideoStart` | 仅在**从停止状态**开始播放时触发 |
| `OnVideoPlay` | **任何开始播放**(包括取消暂停) |
| `OnVideoReady` | 仅在**新视频加载就绪**时触发(未必开始播放) |

---

## Player Events(玩家事件)

> 所有 Player Events 共享: **输出 `player` : `VRC.SDKBase.VRCPlayerApi`**

### Trigger / Collision 系列(玩家碰撞体相关)

| Event | 触发时机 | 频率 |
|-------|---------|------|
| `OnPlayerTriggerEnter` | 任何玩家的 Capsule Collider **进入** Trigger Collider | 单次 |
| `OnPlayerTriggerStay` | 任何玩家的 Capsule Collider **停留**在 Trigger Collider 内 | **每帧** |
| `OnPlayerTriggerExit` | 任何玩家的 Capsule Collider **离开** Trigger Collider | 单次 |
| `OnPlayerCollisionEnter` | 任何玩家的 Capsule Collider **进入** Collider | 单次 |
| `OnPlayerCollisionStay` | 任何玩家的 Capsule Collider **停留**在 Collider 内 | **每帧** |
| `OnPlayerCollisionExit` | 任何玩家的 Capsule Collider **离开** Collider | 单次 |
| `OnPlayerParticleCollision` | **粒子系统**与玩家 Capsule Collider 碰撞(需 Particle "Collision"+"Send Collision Messages") | 单次 |

> **【风险】** `OnPlayerTriggerStay` / `OnPlayerCollisionStay` 每帧触发,在大量玩家时是**性能热点**。建议改用 Enter/Exit + 计时器模式。

---

### 其他 Player Events

| Event | 触发时机 |
|-------|---------|
| `OnPlayerRespawn` | 本地玩家在菜单中点击 "Respawn" 重生 |
| `OnPersistenceUsageUpdated` | 玩家的**持久化用量**更新 |
| `OnPlayerDataStorageExceeded` | 玩家**超过** Player Data Storage 配额 |
| `OnPlayerDataStorageWarning` | 玩家**接近** Player Data Storage 上限 |
| `OnPlayerObjectStorageExceeded` | 玩家**超过** Player Object Storage 配额 |
| `OnPlayerObjectStorageWarning` | 玩家**接近** Player Object Storage 上限 |

---

## 设备 / 输入 / 平台 Events

| Event | 输出 | 触发时机 |
|-------|------|---------|
| `OnScreenUpdate` | `data` : `VRC.SDK3.Platform.ScreenUpdateData` | 本地玩家**首次在移动设备进入世界**时,以及设备方向变化时 |
| `OnInputMethodChanged` | `inputMethod` : `VRC.SDKBase.VRCInputMethod` | 本地玩家**切换输入方式**(Keyboard/Mouse/Controller 等) |
| `OnLanguageChanged` | `language` : `string` | 本地玩家**更新显示语言** |
| `OnPlayerSuspendChanged` | `player` : `VRC.SDKBase.VRCPlayerApi` | 任何玩家的**设备进入挂起状态** |
| `OnVRCPlusMassGift` | `gifter` : `VRCPlayerApi`, `numGifts` : `int` | 任何玩家在实例内**投下礼物炸弹** |
| `OnVRCCameraSettingsChanged` | `camera` : `VRC.SDK3.Rendering.VRCCameraSettings` | 用户**修改相机设置**(Near Clip / FOV 等) |
| `OnVRCQualitySettingsChanged` | - | 用户**调整图形质量设置** |

### OnScreenUpdate 输出结构

`ScreenUpdateData` struct 字段:

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `ScreenUpdateType` | 目前只有 `OrientationChanged`,未来可扩展 |
| `orientation` | `VRCOrientation` | `Landscape` / `Portrait` |
| `resolution` | `Vector2` | 设备分辨率 |

### OnPlayerSuspendChanged 详细

- **挂起** = 设备进入**睡眠模式**或**切换到其他 App**
- 对于**被挂起的玩家**,此 Event 会在**唤醒时**触发
- 通过 `VRCPlayerApi.isSuspended` 判断是**唤醒**还是**挂起**

> **挂起期间**: 设备**不运行 Udon 代码**且**不响应网络事件**,直到玩家重新打开 VRChat。
>
> **多玩家交互最佳实践**:
> - 对挂起玩家做出反应
> - 例如将重要对象的所有权**转移给未挂起的玩家**
> - **不要假设 PC 玩家不会挂起**(目前不会,但不应假设)

### OnVRCCameraSettingsChanged 注意事项

| 行为 | 是否触发 |
|------|---------|
| 手动通过 `VRCCameraSettings` 修改值 | ❌ **不**触发 |
| 相机 `Position` / `Rotation` 变化 | ❌ **不**触发(几乎每帧变化) |
| PhotoCamera **Zoom 滑块**拖动 | ✅ **每帧**触发(影响 FOV) |
| Dolly 路径调整 Zoom | ✅ **每帧**触发 |
| 改变**屏幕分辨率**(包括调整 VRChat 窗口) | ✅ **每帧**触发 |

> ⚠️ 此 Event 可能**每帧触发多次**,**建议保持处理逻辑轻量**以避免性能影响。
> `OnVRCQualitySettingsChanged` 同样可能频繁触发。

---

## Advanced Notes(高级说明)

> 所有上述节点返回类型均为 **`System.Void`**(无返回值)。

---

## 任务提示词列表对照(未在文档中验证)

任务原始要求中列出的以下事件,在本次抓取的官方文档中**未明确出现**:

| 任务要求 Event | 文档中是否存在 | 状态 |
|----------------|---------------|------|
| `OnPlayerPickup` | ✅ 在 "Pickup 相关" 列表 | 已收录 |
| `OnPlayerDrop` | ✅ 在 "Pickup 相关" 列表(以 `OnDrop` 命名) | 已收录 |
| `OnPlayerUseDown` | ✅ 在 "Pickup 相关" 列表(以 `OnPickupUseDown` 命名) | 已收录 |
| `OnPlayerUseUp` | ✅ 在 "Pickup 相关" 列表(以 `OnPickupUseUp` 命名) | 已收录 |
| `OnPlayerTriggerEnter` | ✅ 在 "Player Events" | 已收录 |
| `OnPlayerTriggerExit` | ✅ 在 "Player Events" | 已收录 |
| `OnPlayerCollisionEnter` | ✅ 在 "Player Events" | 已收录 |
| `OnPlayerCollisionExit` | ✅ 在 "Player Events" | 已收录 |
| `OnPlayerRespawn` | ✅ 在 "其他 Player Events" | 已收录 |
| `OnPlayerRestored` | ✅ 在 "Player Join/Leave/Restore" | 已收录 |
| `OnPlayerSuspensionChanged` | ✅ 命名为 `OnPlayerSuspendChanged` | 已收录 |
| `OnPlayerAvatarChanged` | ❌ **未在文档中出现** | 【未确认】 |
| `OnOwnershipRequest` | ❌ **未在文档中出现** | 【未确认】 |
| `OnOwnershipTransferred` | ❌ **未在文档中出现** | 【未确认】 |
| `OnVideoReady` | ✅ 在 "Video" 列表 | 已收录 |
| `OnVideoStart` | ✅ 在 "Video" 列表 | 已收录 |
| `OnVideoEnd` | ✅ 在 "Video" 列表 | 已收录 |
| `OnVideoError` | ✅ 在 "Video" 列表 | 已收录 |
| `MidiNoteOn` | ✅ 在独立 MIDI 页面 | 已收录(注意: **无 `On` 前缀**) |
| `MidiNoteOff` | ✅ 在独立 MIDI 页面 | 已收录(注意: **无 `On` 前缀**) |
| `MidiControlChange` | ✅ 在独立 MIDI 页面 | 已收录(注意: **无 `On` 前缀**) |

> ✅ **2026-06-15 修正**: MIDI 事件在 **Event Nodes 列表中未单独列出**,但在独立的 [MIDI 子分类文档](https://creators.vrchat.com/worlds/udon/midi/) 中有完整记录。
>
> **签名修正**: 官方签名为 `MidiNoteOn/MidiNoteOff/MidiControlChange`(**无 `On` 前缀,无 `VRCPlayerApi player` 参数**),签名形如 `MidiNoteOn(int channel, int number, int velocity)`。
>
> 详细参考: `memory/world/udon/midi/index.md`、`memory/world/udon/midi/realtime-midi.md`

---

## 相关知识库

- [`index.md`](./index.md) — Udon Node Graph 主页
- [`graph-elements.md`](./graph-elements.md) — Graph 元素
- [`special-nodes.md`](./special-nodes.md) — 特殊节点(含 OnVariableChanged)
- `../../api/events-reference.md` — Udon 事件完整参考
- `../udonsharp/` — UdonSharp C# 入口
