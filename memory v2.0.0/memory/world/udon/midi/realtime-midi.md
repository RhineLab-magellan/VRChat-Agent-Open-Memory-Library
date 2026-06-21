---
title: Realtime MIDI(实时 MIDI 输入)
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - event

aliases:
  - "Realtime MIDI(实时 MIDI 输入)"

related:
  - midi-playback.md
  - index.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Realtime MIDI(实时 MIDI 输入)

> 来源: https://creators.vrchat.com/worlds/udon/midi/realtime-midi/
> 抓取日期: 2026-06-15
> 最后更新: 2025-04-07 (官方) / 2026-06-15 (本地化)
> Domain: World / Udon / MIDI
> 状态: ✅ FACT (官方文档)

---

## 概述

使用 **MIDI 设备** 实时控制 Udon 世界,响应 MIDI 音符和控制器变化。
与 [`./midi-playback.md`](./midi-playback.md) 的文件回放不同,本节聚焦**真实硬件设备**的实时输入。

### 典型场景
- 真实钢琴键盘演奏 → 控制世界事件
- MIDI 控制器(Launchpad / APC) → 灯光 / 音视频控制
- DJ/VJ 实时表演
- 音乐教学(教师钢琴 → 学生端可视化)

---

## 🔌 Components 组件

### 1. VRC Midi Listener(必加,手动)

**作用**: 告知 VRChat "我想要接收 MIDI 事件",按需启动 MIDI 系统。

添加到场景中**任意 GameObject** 上(可以是空 GameObject,或与其他组件同对象)。

| 字段 | 类型 | 说明 |
|------|------|------|
| **Active Events** | enum flags | **必须**勾选要接收的事件类型(**默认全不勾选**) |
| **Behaviour** | `UdonBehaviour` | 接收 MIDI 事件的 UdonBehaviour(**可以是同 GameObject 或其他对象**) |

> 🔴 **【FACT】** 默认所有 MIDI 事件都是**未启用**状态。开始测试前必须先勾选 `Active Events`,否则不会收到任何事件。

### 2. VRCMidiHandler(自动,禁止手动添加)

**作用**: VRChat 在场景启动时**自动添加**的 GameObject,处理 MIDI 设备驱动并向所有 Listener 分发事件。

> 🔴 **【FACT】** **绝不要手动添加 `VRCMidiHandler` 组件**!它是 VRChat 运行时自动添加/移除的,目的是:
> - **每个 MIDI 设备只连接一次**(多个 Listener 共享同一设备)
> - 玩家离开世界时自动断开设备连接
> - 避免多个实例竞争设备访问

---

## 🎛️ Device Selection 设备选择

### Editor(编辑器测试)

通过 **VRChat SDK 菜单** 选择 MIDI 设备:
- 位置: `VRChat SDK → Midi Utility Window`(具体菜单名以 SDK 实际为准)
- **保存位置**: Editor Preferences(跨项目记住设备选择)

![image](https://creators.vrchat.com/assets/images/realtime-midi-215557576-5414eb63-a857-4334-8a8c-05f3b6436773-3294993bdeb24537f638b9dfa41278a9.png/)

### Runtime(运行时)

进入世界时,VRChat **自动打开第一个找到的 MIDI 设备**。

#### 指定特定设备(多设备情况)

如果电脑上有多个 MIDI 设备,可以用**启动参数** `--midi=<devicename>` 指定:

**示例**: 设备在 Windows 上显示为 `SchneebleCo MidiKeySmasher 89`
```bash
# VRChat 启动参数(Steam / 快捷方式)
--midi=midikeysmasher
```

> **匹配规则**:
> - **部分匹配**(不需要完整设备名)
> - **忽略大小写**(`MidiKeySmasher` = `midikeysmasher`)
> - 完整启动参数列表: [Launch Options](https://docs.vrchat.com/docs/launch-options)

---

## 🎹 事件签名

```csharp
public override void MidiNoteOn(int channel, int number, int velocity)
public override void MidiNoteOff(int channel, int number, int velocity)
public override void MidiControlChange(int channel, int number, int value)
```

> 完整签名、参数范围、技术细节见 [`./index.md`](./index.md#-midi-events3-个核心事件)

### 实时 vs 回放的事件差异

| 维度 | Realtime | Playback |
|------|---------|---------|
| 事件源 | USB/Bluetooth MIDI 设备 | MIDI 文件 |
| 触发时机 | 玩家按下/松开琴键 | 文件播放进度 |
| 设备依赖 | 必须有 MIDI 设备 | 不需要(本地 Asset) |
| `channel` 来源 | 设备配置的发送通道 | MIDI 文件中编码的通道 |
| `velocity` | 真实按键力度(0-127,设备支持) | MIDI 文件中编码的力度 |

> **关键观察**: **事件签名完全相同**,所以你可以用同一份 Udon 脚本同时处理实时输入和文件回放!

---

## 🌍 Example Scene 示例世界

**Udon Midi Test** —— 官方测试世界,展示**所有 3 种事件类型**的读取和显示。

- **World ID**: `wrld_f8bc6485-dcdf-4646-89d8-14e4772561ee`
- **URL**: https://vrchat.com/home/world/wrld_f8bc6485-dcdf-4646-89d8-14e4772561ee

直接访问该世界可看到:
- 每个通道的 Note On/Off 实时显示
- 控制器变化的数值显示
- 设备连接状态指示

---

## 💡 完整 UdonSharp 示例(实时设备监听)

> **简化示例**: 监听所有通道的 Note On,在控制台输出 note 信息。

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

[UdonBehaviourSyncMode(BehaviourSyncMode.None)]
public class RealtimeMidiLogger : UdonSharpBehaviour
{
    [SerializeField] private bool logNoteOn = true;
    [SerializeField] private bool logNoteOff = false;
    [SerializeField] private bool logControlChange = false;

    public override void MidiNoteOn(int channel, int number, int velocity)
    {
        if (!logNoteOn) return;
        Debug.Log($"[MIDI Note On] ch={channel} note={number} vel={velocity}");
    }

    public override void MidiNoteOff(int channel, int number, int velocity)
    {
        if (!logNoteOff) return;
        Debug.Log($"[MIDI Note Off] ch={channel} note={number} vel={velocity}");
    }

    public override void MidiControlChange(int channel, int number, int value)
    {
        if (!logControlChange) return;
        Debug.Log($"[MIDI CC] ch={channel} cc={number} val={value}");
    }
}
```

**Inspector 配置**:
1. 在任意 GameObject 上添加 `VRC Midi Listener` 组件
2. **勾选 Active Events** 的 3 个事件(Note On / Off / Control Change)
3. **将本 UdonBehaviour 拖到 `Behaviour` 字段**
4. 进入 Play Mode(或 Build & Test)测试

---

## 🔧 关键设计模式

### 1. Listener + Behaviour 分离

`VRC Midi Listener` 组件与 `UdonBehaviour` 可以**不在同一 GameObject** 上:

```
[GameObject A] VRC Midi Listener
                └─ Behaviour 引用 → [GameObject B] UdonBehaviour
```

**优势**:
- 多个 Listener 共享一个设备 → 节省设备连接
- 多个 Behaviour 接收同一设备 → 解耦输入与逻辑

### 2. Active Events 标志位

`Active Events` 字段是 **flags enum**:
- `MidiNoteOn`
- `MidiNoteOff`
- `MidiControlChange`

**最佳实践**:
- **只勾选你需要的事件类型** → 减少事件分发开销
- 实时性要求高时,关闭不需要的事件类型

### 3. 无限旋转旋钮的处理

`MidiControlChange` 的 `value` 范围通常 0-127,但**无限旋转的旋钮**(无起止位置的旋钮)可能只输出:
- `0` 和 `1`(或正负方向)
- 其他自定义双值

> **处理方案**: 在 Udon 中维护自己的状态,根据 0/1 切换来增减内部计数器。

```csharp
private int[] _knobValues = new int[128];

public override void MidiControlChange(int channel, int number, int value)
{
    if (number != 16) return; // 只关心 CC#16
    if (value == 1) _knobValues[number]++;
    else if (value == 0) _knobValues[number]--;
    Debug.Log($"Knob 16: {_knobValues[number]}");
}
```

### 4. 设备特定的行为(Launchpad 模式)

Launchpad / APC 等 MIDI 控制器有**特殊模式**(Session Mode / User Mode):
- 不同模式下,按钮发送的 **note 编号不同**
- 应在 Udon 中**先判断设备模式**再响应

---

## ⚠️ 限制与陷阱

| 陷阱 | 说明 | 解决方案 |
|------|------|---------|
| **Quest 不支持** | Quest 端无法接收 MIDI | 提供非 MIDI 的回退方案 |
| **默认不启用事件** | Listener 的 `Active Events` 默认全不勾选 | 测试前必须勾选,文档化提醒 |
| **多设备冲突** | 多 MIDI 设备时,默认连接"第一个找到的" | 启动参数 `--midi=<devicename>` 指定 |
| **蓝牙 MIDI 兼容性差** | 部分蓝牙 MIDI 设备在 Windows 上需要额外驱动 | 推荐 USB MIDI;或使用 [Tobias Erichsen's rtpMIDI](https://www.tobias-erichsen.de/software/rtpmidi.html) |
| **Listener 必须存在** | 没有 `VRC Midi Listener` 组件,VRChat 不会启动 MIDI 系统 | 至少添加 1 个 Listener(可放在空 GameObject) |
| **VRCMidiHandler 禁止手动添加** | 自动管理的设备连接,手动添加会冲突 | **永远不要**给场景手动加 `VRCMidiHandler` |
| **启动参数大小写** | 设备名匹配忽略大小写,但要包含关键子串 | 使用唯一子串(如 `midikeysmasher` 而非 `smasher`) |

---

## 🔬 MIDI 设备兼容性参考

| 设备类型 | 兼容性 | 备注 |
|---------|-------|------|
| **USB MIDI 键盘** | ✅ 优秀 | 即插即用,推荐 |
| **USB MIDI 控制器**(Launchpad, APC) | ✅ 优秀 | CC 和 Note 都支持 |
| **蓝牙 MIDI** | ⚠️ 视情况 | Windows 需额外驱动,macOS 内置支持 |
| **虚拟 MIDI 端口**(rtpMIDI / loopMIDI) | ✅ 优秀 | 用于软件间 MIDI 桥接 |
| **老式 MIDI 接口**(5-pin DIN) | ✅ 良好 | 需 USB-MIDI 接口适配器 |

---

## 🎯 实时 MIDI vs 文件回放 决策表

| 场景 | 推荐方式 | 理由 |
|------|---------|------|
| 节奏游戏 | Playback | 精确时序,无需玩家有 MIDI 设备 |
| 钢琴演奏 | Realtime | 需要真实乐器反馈 |
| 灯光秀 | Playback | 预录时序,精准同步 |
| DJ 表演 | Realtime | 需要即时响应 |
| 音乐教学 | Realtime | 双向互动 |
| 音乐可视化 | Playback | 大规模同步,确定性输出 |
| VJ 控制 | Realtime | 实时混音控制 |
| 派对互动 | Realtime | 玩家可即兴参与 |

> **关键决策点**: 玩家**需要控制时序**吗?
> - **是** → Realtime
> - **否,要确定性输出** → Playback

---

## 与知识库互补

| 关联知识库 | 路径 | 说明 |
|----------|------|------|
| **MIDI 总览** | [`./index.md`](./index.md) | 3 个事件签名 + 技术参数速查 |
| **MIDI 文件回放** | [`./midi-playback.md`](./midi-playback.md) | VRCMidiPlayer 组件 |
| **MIDI Playback 示例** | `memory/world/examples/midi-playback.md` | 4-Grid LogoButton 实现 |
| **Udon 事件完整参考** | `memory/api/events-reference.md` | 事件方法 + 调用约束 |
| **VRChat 启动参数** | https://docs.vrchat.com/docs/launch-options | `--midi=` 等启动参数完整列表 |
| **rtpMIDI** | https://www.tobias-erichsen.de/software/rtpmidi.html | Windows 蓝牙 MIDI / 虚拟端口工具 |

---

## 二次开发建议

| 扩展方向 | 实现思路 |
|---------|---------|
| **设备多路复用** | 多个 Listener 指向同一 UdonBehaviour,实现输入聚合 |
| **力度可视化** | 用 `velocity` 控制灯光亮度/粒子数量/物体缩放 |
| **控制器到动作映射** | 用 `Dictionary<int, System.Action<float>>` 将 CC 编号映射到自定义动作 |
| **设备状态缓存** | 维护 `int[] lastNoteVelocities = new int[128]`,记录每个 note 的最新力度,用于恢复显示 |
| **模式切换** | 监听特定 CC(如 CC#16)切换世界功能模式 |
| **MIDI 录制** | 缓存 `MidiNoteOn/Off` 事件为时间序列,允许回放玩家的演奏 |
