---
title: "API: Complete Udon Event Reference"
category: api
knowledge_level: core
status: active
source: "UdonSharp 官方文档 (udonsharp.docs.vrchat.com/events/)"
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - api
  - networking
  - sync
  - serialization
  - ownership
  - event
aliases:
  - "Events Reference"
  - "Udon 事件参考"
  - 事件全集
  - "Event Reference"
related:
  - networking.md
  - api-checker.md
  - pickups.md
  - audio.md
  - data-containers.md
---
# API: Complete Udon Event Reference

> SDK Version: VRChat SDK 3.x
> Last Verified: 2026-06-04

---

## 核心规则

- **所有 Udon 事件方法必须是 `public override`**
- **`_` 前缀方法不会被网络事件调用**（VRChat 2020.4.4+）
- **Udon 比标准 C# 慢 200x ~ 1000x**
- **40+ 迭代的逻辑建议用 Animation 替代**

---

## 1. Udon Input Events（之前未完整记录）

**需要玩家拥有交互权限。**

| 方法 | 参数 | 说明 |
|---|---|---|
| `Interact()` | — | 玩家与物体交互 |
| `InputJump(bool, UdonInputEventArgs)` | value, args | 跳跃输入 |
| `InputUse(bool, UdonInputEventArgs)` | value, args | 使用输入 |
| `InputGrab(bool, UdonInputEventArgs)` | value, args | 抓取输入 |
| `InputDrop(bool, UdonInputEventArgs)` | value, args | 放下输入 |
| `InputMoveHorizontal(float, UdonInputEventArgs)` | value, args | 水平移动 |
| `InputMoveVertical(float, UdonInputEventArgs)` | value, args | 垂直移动 |
| `InputLookHorizontal(float, UdonInputEventArgs)` | value, args | 视角水平旋转 |
| `InputLookVertical(float, UdonInputEventArgs)` | value, args | 视角垂直旋转 |

---

## 2. Udon Networking Events（精确签名）

| 方法 | 返回 | 说明 |
|---|---|---|
| `OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner)` | `bool` | 所有权即将转移。`true`=接受，`false`=拒绝 |
| `OnOwnershipTransferred(VRCPlayerApi player)` | `void` | 所有权变更后触发 |
| `OnPreSerialization()` | `void` | 序列化前（仅 Owner） |
| `OnPostSerialization(SerializationResult result)` | `void` | 序列化后。`result.success` + `result.byteCount` |
| `OnDeserialization()` | `void` | 收到网络数据（非 Owner） |

> ⚠️ 旧文档警告: 设置所有权后不能立即设置同步变量，旧 Owner 需要先确认，可能需要数秒。
> ⚠️ **Collision Ownership Transfer 存在历史 bug**，会导致所有权转移风暴并卡顿所有玩家。VRC_Object Sync 应自动处理，无需手动。

---

## 3. Udon Station Events（精确签名）

| 方法 | 参数 |
|---|---|
| `OnStationEntered(VRCPlayerApi player)` | player |
| `OnStationExited(VRCPlayerApi player)` | player |

---

## 4. Udon String/Image Loading Events

| 方法 | 参数 |
|---|---|
| `OnImageLoadSuccess(IVRCImageDownload result)` | result |
| `OnImageLoadError(IVRCImageDownload result)` | result |
| `OnStringLoadSuccess(IVRCStringDownload result)` | result |
| `OnStringLoadError(IVRCStringDownload result)` | result |

---

## 5. Udon MIDI Events(2026-06-15 新增)

> **来源**: VRChat 官方 MIDI 文档 (`memory/world/udon/midi/`)
> **平台限制**: **桌面端独占**,Quest 完全不支持
> **必须组件**: 场景中需有 `VRC Midi Listener` 组件 + 勾选对应 `Active Events`
> **实时性**: Realtime(设备输入) + Playback(文件回放) 共用相同事件签名

| 方法 | 参数 | 触发条件 |
|---|---|---|
| `MidiNoteOn(int channel, int number, int velocity)` | channel(0-15) / number(0-127) / velocity(0-127) | MIDI 设备按下琴键 / MIDI 文件播放到 Note On |
| `MidiNoteOff(int channel, int number, int velocity)` | channel(0-15) / number(0-127) / velocity(0-127 通常为 0) | MIDI 设备松开琴键 / MIDI 文件播放到 Note Off |
| `MidiControlChange(int channel, int number, int value)` | channel(0-15) / number(0-127) / value(0-127) | MIDI 控制器变化(旋钮/推子) |

> ⚠️ **【FACT 修正】** 一些早期文档/社区资料中可能见到 `OnMidiNoteOn(VRCPlayerApi player, ...)` 的错误签名。**官方签名无 `On` 前缀,无 `VRCPlayerApi player` 参数**——MIDI 事件是**设备级全局事件**,不绑定到具体玩家。
>
> ⚠️ **数据类差异**: `MidiBlock.Channel` 是 **1-16**,事件 `channel` 参数是 **0-15**(0-indexed)。查询 `MidiBlock[]` 时需 `block.Channel - 1 == event.channel` 转换。

### 事件注册方式
1. 场景中任意 GameObject 添加 **`VRC Midi Listener`** 组件
2. 勾选 `Active Events`(默认全不勾选)
3. 将目标 `UdonBehaviour` 拖到 `Behaviour` 字段
4. 在 UdonBehaviour 中 `public override` 实现上述方法

详细文档:
- 总览与事件: `memory/world/udon/midi/index.md`
- 文件回放(`VRCMidiPlayer` 组件): `memory/world/udon/midi/midi-playback.md`
- 实时输入(`VRC Midi Listener` 组件): `memory/world/udon/midi/realtime-midi.md`

---

## 6. 受支持的 Unity MonoBehaviour 事件全集

### 生命周期
`Start()`, `Update()`, `FixedUpdate()`, `LateUpdate()`, `PostLateUpdate()`

### 启用/禁用
`OnEnable()`, `OnDisable()`, `OnDestroy()`

### 碰撞（3D + 2D）
`OnCollisionEnter/Exit/Stay`, `OnCollisionEnter2D/Exit2D/Stay2D`

### 触发器（3D + 2D）
`OnTriggerEnter/Exit/Stay`, `OnTriggerEnter2D/Exit2D/Stay2D`

### 控制器
`OnControllerColliderHit()`, `OnControllerColliderHitPlayer()`

### 渲染
`OnWillRenderObject()`, `OnPreRender()`, `OnPostRender()`, `OnPreCull()`, `OnRenderImage()`, `OnRenderObject()`, `OnDrawGizmos()`, `OnDrawGizmosSelected()`

### 粒子
`OnParticleCollision()`, `OnParticleTrigger()`

### 鼠标
`OnMouseDown/Up/UpAsButton/Drag/Enter/Exit/Over`

### 可见性
`OnBecameVisible()`, `OnBecameInvisible()`

### Animator
`OnAnimatorIK()`, `OnAnimatorMove()`

### 音频
`OnAudioFilterRead()`

### 其他
`OnJointBreak()`, `OnJointBreak2D()`, `OnValidate()`, `Reset()`, `OnTransformChildrenChanged()`, `OnTransformParentChanged()`

---

## 7. 方法可见性与调用方式

| 调用场景 | 可见性 | API |
|---|---|---|
| 本地直接调用 | `private` 可 | `Behaviour.Method()` |
| `SendCustomEvent` | 必须 `public` | `SendCustomEvent("Method")` |
| `SendCustomNetworkEvent` | 必须 `public`，不能 `_` 开头 | `SendCustomNetworkEvent(All, "Method")` |
| 纯本地 public（防网络调用） | `public void _Method()` | `_` 前缀阻止网络事件调用（2020.4.4+） |
| Udon 事件回调 | `public override` | 自动触发 |

---

## 8. 相关知识库(Udon 官方文档本地化)

> 10 个 Udon 核心单页已本地化到 `memory/world/udon/`,涵盖事件、输入、动画、外部资源、调试等基础系统。

| 主题 | 本地化文档 | 关联内容 |
|---|---|---|
| Udon 总览 | `memory/world/udon/index.md` | 概念、3 种创建方式、VM 细节、9 条指令 |
| **事件执行顺序** ⭐关键 | `memory/world/udon/event-execution-order.md` | `_onEnable → _start` 无间隔执行 |
| Animation Events | `memory/world/udon/animation-events.md` | Animator 事件白名单 (12 方法) |
| Avatar Events | `memory/world/udon/avatar-events.md` | OnAvatarChanged / OnAvatarEyeHeightChanged |
| Input Events | `memory/world/udon/input-events.md` | Interact/InputUse/InputJump/InputGrab + UdonInputEventArgs |
| UI Events | `memory/world/udon/ui-events.md` | Unity UI 事件白名单 (28 组件) |
| Debugging | `memory/world/udon/debugging-udon-projects.md` | Debug 模式 + 错误日志 + UdonSharp 异常监听 |
| External URLs | `memory/world/udon/external-urls.md` | VRCUrl + 域白名单 + 5s 限流 |
| Image Loading | `memory/world/udon/image-loading.md` | VRCImageDownloader + 2048x2048 + 32MB |
| String Loading | `memory/world/udon/string-loading.md` | VRCStringDownloader + 100MB |
| AI Navigation | `memory/world/udon/ai-navigation.md` | NavMeshAgent + 运行时 NavMesh + Owner 计算 |
| VM and Assembly | `memory/world/udon/vm-and-assembly.md` | 字节码逆向、9 Opcode、类型命名规则 |
| Using Build & Test | `memory/world/udon/using-build-test.md` | 本地测试流程 |
| World Debug Views | `memory/world/udon/world-debug-views.md` | 调试视图 |

---

## 8. 关键工程约束（来自官方文档）

### 性能
- Udon 比标准 C# 慢 **200x ~ 1000x**
- Update 中避免复杂循环
- 40+ 迭代的逻辑建议用 **Animation 替代**（不是 Animator）
- 热路径避免 `GetComponent<T>()`
- 优先使用 Unity/VRC 内置组件而非 Udon 实现

### 网络
- 事件过多 → "Death Runs"（数据丢失）
- 同步变量更新比网络事件慢 → **设置同步变量后立即发事件可能乱序**
- Instantiation **不支持网络同步**，必须使用对象池

### Struct
- `Vector3.Normalize()` 不修改变量本身 → 必须 `v = v.normalized`

### 编辑器脚本
- 编辑器代码放在 `Editor` 文件夹或用 `#if UNITY_EDITOR`
- 同文件内编辑器代码: `#if !COMPILER_UDONSHARP && UNITY_EDITOR`
- U# 编辑器采用 Proxy 机制: `UpdateProxy()` / `ApplyProxyModifications()`
