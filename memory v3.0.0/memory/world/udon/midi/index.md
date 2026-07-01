---
title: "MIDI in Udon"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - misc
  - index
  - navigation
aliases:
  - "MIDI in Udon"
  - index
related:
  - realtime-midi.md
  - midi-playback.md
  - "../graph/index.md"
  - "../networking/index.md"
  - "../players/index.md"
---
# MIDI in Udon

> 来源: https://creators.vrchat.com/worlds/udon/midi/
> 抓取日期: 2026-06-15
> 最后更新: 2024-06-04 (官方) / 2026-06-15 (本地化)
> Domain: World / Udon
> 状态: ✅ FACT (官方入口文档)

---

## 概述

MIDI(乐器数字接口,Musical Instrument Digital Interface)自 1980 年代以来一直是连接各类音乐设备的标准协议。VRChat 在 Udon 中集成了 MIDI 支持,使创作者可以构建**响应真实乐器实时输入**与**预录 MIDI 演奏**的世界。

> 背景: [MIDI on Wikipedia](https://en.wikipedia.org/wiki/MIDI)

---

## 两种 MIDI 使用方式

| 方式 | 说明 | 文档 |
|------|------|------|
| **Realtime**(实时输入) | 接收**插入电脑的 MIDI 设备**的实时事件 | [realtime-midi.md](./realtime-midi.md) |
| **Playback**(回放) | 播放 MIDI 文件 + 同步音频 | [midi-playback.md](./midi-playback.md) |

两种方式都通过 **Udon 的 MIDI 事件** 与脚本交互,事件签名详见下方。

---

## 🎹 Midi Events(3 个核心事件)

> **【FACT】** 以下签名来自 VRChat 官方文档,事件回调方法必须声明为 `public override void`。

### `MidiNoteOn` 音符按下

```csharp
public override void MidiNoteOn(int channel, int number, int velocity) { }
```

**触发时机**:
- MIDI 设备上按下琴键/按钮
- MIDI 文件播放到 Note On 消息

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `channel` | `int` | 0-15 | MIDI 通道(MIDI 标准为 1-16,VRChat 内部使用 0-indexed) |
| `number` | `int` | 0-127 | 音符编号(部分设备可能不输出完整范围) |
| `velocity` | `int` | 0-127 | 触发力度(取决于设备是否支持) |

### `MidiNoteOff` 音符松开

```csharp
public override void MidiNoteOff(int channel, int number, int velocity) { }
```

**触发时机**:
- MIDI 设备上松开琴键/按钮
- MIDI 文件播放到 Note Off 消息

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `channel` | `int` | 0-15 | MIDI 通道(0-indexed) |
| `number` | `int` | 0-127 | 音符编号 |
| `velocity` | `int` | 0-127 | 通常为 0,但因设备而异 |

### `MidiControlChange` 控制器变化

```csharp
public override void MidiControlChange(int channel, int number, int value) { }
```

**触发时机**:
- 旋钮(knob)转动
- 推子(slider)推动
- 其他控制信号变化

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `channel` | `int` | 0-15 | MIDI 通道(0-indexed) |
| `number` | `int` | 0-127 | 控制器编号(Control Number) |
| `value` | `int` | 0-127 | 控制器值(部分无限旋转的旋钮可能只输出 0/1 或其他双值) |

> ⚠️ **【未确认】** 任务描述中提到的事件签名 `OnMidiNoteOn(VRCPlayerApi player, int channel, int number, int velocity)` **与官方文档不一致**。官方文档明确参数列表为 `(int channel, int number, int velocity)`,**没有 `VRCPlayerApi player` 参数,也没有 `On` 前缀**。MIDI 事件是**设备级全局事件**,不绑定到具体玩家。

---

## 技术参数速查

| 参数 | 范围 | 来源 | 说明 |
|------|------|------|------|
| `channel` | 0-15 | MIDI 1.0 规范 | 0-indexed(VRChat 内部表示) |
| `number` | 0-127 | MIDI 1.0 规范 | Note On/Off:音高;CC:控制器号 |
| `velocity` | 0-127 | MIDI 1.0 规范 | 力度,0 在 Note On 中常被当作 Note Off |
| `value` | 0-127 | MIDI 1.0 规范 | 控制器值(连续推子 = 全范围,无限旋钮 = 0/1) |

> **设计意图**: MIDI 1.0 规范定义 channel 为 1-16,但 VRChat 内部使用 0-indexed(0-15)。在配置 MIDI 设备时,设备的"通道 1"对应 VRChat 的 `channel=0`。

---

## 平台兼容性

| 平台 | MIDI 支持 | 备注 |
|------|----------|------|
| **Windows** | ✅ 完整支持 | 桌面客户端独占 |
| **macOS** | ✅ 完整支持 | 桌面客户端独占 |
| **Android(Quest)** | ❌ **不支持** | Quest 端无 MIDI 设备接入能力 |

> 🔴 **关键风险**: MIDI 功能是**桌面端独占**,Quest 用户完全无法使用。在设计 MIDI 世界时,需考虑:
> - Quest 用户将无法触发 MIDI 事件(无论实时输入还是文件回放)
> - 应提供**非 MIDI 的回退路径**(例如 VRChat 内的 UI 触发器)
> - 文件回放在桌面端是"本地播放"(无需 MIDI 设备,使用 `VRCMidiPlayer` 组件即可)

---

## 典型应用场景

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| 节奏游戏(音乐游戏) | Playback | MIDI 文件精确驱动游戏逻辑 + 同步音频 |
| 音乐可视化 | Playback | Note On/Off 触发视觉特效 |
| 灯光秀 | Playback | 预录 MIDI 触发灯光时序 |
| 钢琴演奏交互 | Realtime | 真实钢琴键盘控制世界事件 |
| DJ/VJ 设备 | Realtime | MIDI 控制器(Launchpad / APC)控制灯光/音视频 |
| 教学应用 | Realtime | 教师 MIDI 键盘演示给学生 |

---

## 与知识库互补

| 关联知识库 | 路径 | 说明 |
|----------|------|------|
| **MIDI 文件回放** | [`./midi-playback.md`](./midi-playback.md) | `VRCMidiPlayer` 组件 + MidiData/MidiTrack/MidiBlock 类 |
| **实时 MIDI 输入** | [`./realtime-midi.md`](./realtime-midi.md) | `VRC Midi Listener` 组件 + 设备选择 |
| **MIDI Playback 示例** | `memory/world/examples/midi-playback.md` | 4-Grid LogoButton 完整实现 |
| **Udon 事件完整参考** | `memory/api/events-reference.md` | 3 个 MIDI 事件签名 + 调用约束 |
| **MIDI 节点(图)** | `memory/world/udon/graph/event-nodes.md` | Udon Node Graph 中的 MIDI 事件节点 |
| **AudioLink** | `memory/hybrid/audiolink-system.md` | 音频数据驱动的另一种方式(Shader-Centric) |

---

## 子页面索引

| 页面 | 路径 | 核心内容 |
|------|------|---------|
| Midi Playback | `memory/world/udon/midi/midi-playback.md` | MIDI 文件回放、VRCMidiPlayer 组件、4 个数据类 |
| Realtime Midi | `memory/world/udon/midi/realtime-midi.md` | 实时 MIDI 设备输入、Listener 组件、运行时设备选择 |
