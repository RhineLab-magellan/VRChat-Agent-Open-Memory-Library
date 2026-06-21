# MIDI Playback(MIDI 文件回放)

> 来源: https://creators.vrchat.com/worlds/udon/midi/midi-playback
> 抓取日期: 2026-06-15
> 最后更新: 2024-11-15 (官方) / 2026-06-15 (本地化)
> Domain: World / Udon / MIDI
> 状态: ✅ FACT (官方文档)

---

## 概述

通过 **`VRCMidiPlayer` 组件** 播放 MIDI 文件,同步播放对应的音频文件,并向所有目标 UdonBehaviour 发送 **MIDI Note On / Note Off 事件**。

> ⚠️ **【FACT 修正】** 任务描述中提到"使用 `VRC MIDI Player` 静态方法"——**这与官方文档不一致**。当前 SDK 中 **没有静态方法** 的 MIDI 播放器,实际 API 是 **`VRCMidiPlayer` 组件**(MonoBehaviour),通过 Inspector 字段配置 + 实例方法 `Play()` / `Stop()` 调用。

### 典型场景
- 节奏游戏
- 音乐可视化
- 灯光秀同步
- 预录 MIDI 演奏的精确回放

### 快速开始
可直接加载 **MidiPlaybackScene 示例** 起步: 详见 [`memory/world/examples/midi-playback.md`](../../examples/midi-playback.md)

---

## 📁 Assets: MidiFile 和 AudioClip

### 文件准备

1. **拖入文件** 到 Unity 的 `Assets` 文件夹
   - MIDI 文件必须以 **`.mid`** 扩展名结尾
   - 音频文件可以是 Unity 支持的任意格式: `.aif` / `.wav` / `.mp3` / `.ogg`

2. **关联 AudioClip**:
   - 选中 MIDI 文件
   - 在 Inspector 中将对应的音频文件拖到 `Audio Clip` 字段

![image](https://creators.vrchat.com/assets/images/midi-playback-214464414-32af9c18-c003-49ed-bd12-dd431367db56-eced7f443e31cf8c6a4a1f3b8322dc79.png)

3. **【FACT】** **BPM 必须正确设置**
   - 如果数据看起来不匹配音频,90% 的情况是 BPM 问题
   - 可在 Inspector 中勾选 **"Override Bpm"** 覆盖
   - **更好的做法**: 直接编辑 MIDI 文件,写入正确的 BPM

---

## 🔌 Component: VRCMidiPlayer

> **核心组件**: `VRCMidiPlayer`(命名空间 `VRC.SDK3.Midi`)
> 类似 `AudioSource`,但使用 **MIDI Asset** 而非 AudioClip
> 它向所有 **Target Behaviours** 发送 MIDI Note On / Note Off 事件

### Inspector 字段

| 名称 | 类型 | 说明 |
|------|------|------|
| **Midi File** | `MidiFile`(Asset) | SMF 格式的 MIDI 文件,触发其事件数据 |
| **Audio Source** | `AudioSource` | 与 MIDI 数据对应的音频组件(在同 GameObject 上) |
| **Target Behaviours** | `UdonBehaviour[]` | 接收 MIDI Note On / Note Off 事件的 UdonBehaviour 列表 |
| **Display Debug Blocks** | `bool` | 启用后,在 Scene View 中显示当前 MIDI 文件的所有音符(辅助调试) |

### 方法(Methods)

| 方法 | 说明 |
|------|------|
| `Play()` | 启动 MIDI 事件和 Audio Source 的同步播放 |
| `Stop()` | 停止 MIDI 事件和 Audio Source 的播放 |

### 属性(Properties)

| 属性 | 类型 | 说明 |
|------|------|------|
| `time` | `float` | 设置 / 获取 MIDI 和 Audio 源的当前时间(秒) |
| `midiData` | `MidiData` | 获取包含当前 MIDI 轨道所有数据的对象(可在播放前用于预配置) |

---

## 📊 数据类层级

```
MidiData
  ├── Tracks: MidiTrack[]
  │     ├── Blocks: MidiBlock[]
  │     │     ├── Note (byte) 0-127
  │     │     ├── Velocity (byte) 0-127
  │     │     ├── Channel (byte) 1-16
  │     │     ├── StartTimeMs / EndTimeMs
  │     │     ├── StartTimeSec / EndTimeSec
  │     │     └── LengthSec
  │     ├── minNote / maxNote (byte)
  │     └── minVelocity / maxVelocity (byte)
  └── Bpm (byte)
```

### Class: MidiData

返回的 MIDI 顶层数据,包含所有轨道和 BPM。

| 字段 | 类型 | 说明 |
|------|------|------|
| `Tracks` | `MidiTrack[]` | 文件中的 MidiTrack 数组 |
| `Bpm` | `byte` | 曲目的 BPM |

### Class: MidiTrack

封装一个 `MidiBlock` 数组,提供音符和力度范围的便捷引用。

| 字段 | 类型 | 说明 |
|------|------|------|
| `Blocks` | `MidiBlock[]` | 轨道中的 MidiBlock 数组 |
| `minNote` | `byte` | 该轨道中最低的音符 |
| `maxNote` | `byte` | 该轨道中最高的音符 |
| `minVelocity` | `byte` | 该轨道中最低的力度(**不包括 0**) |
| `maxVelocity` | `byte` | 该轨道中最高的力度 |

### Class: MidiBlock

表示一个完整的 MIDI 音符事件(从 Note On 到 Note Off),附带元数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| `Note` | `byte` | 0-127 范围的音符编号 |
| `Velocity` | `byte` | 0-127 范围的力度 |
| `Channel` | `byte` | **1-16** 范围的通道(⚠️ 与事件的 0-15 索引**不同**) |
| `StartTimeMs` | `float` | Note On 开始的时刻(毫秒) |
| `EndTimeMs` | `float` | Note Off 触发的时刻(毫秒) |
| `StartTimeSec` | `float` | Note On 开始的时刻(秒) |
| `EndTimeSec` | `float` | Note Off 触发的时刻(秒) |
| `LengthSec` | `float` | 整个事件的时长(从 Note On 到 Note Off,秒) |

> ⚠️ **重要差异**: `MidiBlock.Channel` 是 **1-16**,而 `MidiNoteOn/Off` 事件的 `channel` 参数是 **0-15**(0-indexed)。**索引时需要 -1 转换**!

---

## 🎯 事件签名

```csharp
public override void MidiNoteOn(int channel, int number, int velocity)
public override void MidiNoteOff(int channel, int number, int velocity)
```

> 完整签名与参数说明见 [`./index.md`](./index.md#-midi-events3-个核心事件)。

---

## 💡 完整 UdonSharp 示例

> **【FACT 验证】** 来自 Example Central 4-Grid LogoButton,完整代码见 [`memory/world/examples/midi-playback.md`](../../examples/midi-playback.md#完整-udonsharp-代码logobuttoncs)

核心逻辑:
```csharp
using UdonSharp;
using VRC.SDK3.Midi;
using UnityEngine.UI;

[UdonBehaviourSyncMode(BehaviourSyncMode.None)]
public class LogoButton : UdonSharpBehaviour
{
    [SerializeField] private Transform[] grids;
    [SerializeField] private VRCMidiPlayer player;
    [SerializeField] private int[] channels;  // 通道到 Grid 的映射

    public override void MidiNoteOn(int channel, int number, int velocity)
    {
        UpdateGridState(channel, number, true);
    }

    public override void MidiNoteOff(int channel, int number, int velocity)
    {
        UpdateGridState(channel, number, false);
    }

    private void UpdateGridState(int midiChannel, int noteNumber, bool isEnabled)
    {
        for (var gridIndex = 0; gridIndex < grids.Length; gridIndex++)
        {
            if (midiChannel != channels[gridIndex]) continue;
            // 12 音位量化
            var image = grids[gridIndex].GetChild(noteNumber % 12).GetComponent<Image>();
            image.enabled = isEnabled;
        }
    }
}
```

---

## 🔧 关键设计模式

### 1. `BehaviourSyncMode.None` — MIDI 回放是本地播放

MIDI 播放由 VRChat 客户端**自动保证一致性**:
- 每玩家都从自己的 MIDI Asset 听到**同步的音轨**
- **不需要跨玩家同步** MIDI 状态
- 避免不必要的网络带宽浪费

### 2. Note On/Off 配对

Note On 启用 → Note Off 禁用,严格配对避免图像卡在 enabled 状态。

### 3. 12 平均律量化

```csharp
var child = grids[gridIndex].GetChild(noteNumber % 12);
```

`noteNumber % 12` 落在 `[0, 11]`,对应 12 半音(C=0, C#=1, ..., B=11)。
- **简单可视化**: 12 个图标
- **高级映射**: 查表(`Dictionary<int, Color>`)将 MIDI 编号映射到颜色/图像

### 4. channels 数组作为映射表

```csharp
[SerializeField] private int[] channels = new int[] { 3, 4, 1, 2 };
```

将 MIDI 通道与显示 Grid 解耦,**同一段 MIDI 可呈现不同视觉效果**。

### 5. velocity 参数的实际应用

虽然 `velocity` 在示例中未使用,但可用于:
- 力度相关的**视觉强度**(透明度/缩放)
- 力度相关的**颜色亮度**
- 力度相关的**粒子数量**

---

## ⚠️ 限制与陷阱

| 陷阱 | 说明 | 解决方案 |
|------|------|---------|
| **本地 Asset 限制** | MIDI 文件**必须是 Unity Asset**,不能用 `VRCUrl` 网络加载 | 跟随 world 上传,大小计入 world 体积预算 |
| **BPM 不匹配** | MIDI 文件 BPM 设置错误,音符时序与音频错位 | 勾选 "Override Bpm" 或编辑 MIDI 文件 |
| **Channel 索引差异** | `MidiBlock.Channel` 是 1-16,事件 `channel` 是 0-15 | 数据查询时 `block.Channel - 1 == event.channel` |
| **桌面端独占** | Quest 完全不支持 MIDI | 提供 UI 触发的回退方案 |
| **MIDIBPM 精度** | 实际播放使用 MIDI 文件的微秒级时序,Inspector BPM 仅作显示 | 不要在 `Update` 中读取 `time` 用于精确同步(改用 `midiData` 预计算) |

---

## 🆚 任务描述 vs 官方文档对照

| 项 | 任务描述 | 官方文档 | 实际 |
|---|---------|---------|------|
| 类名 | `VRC MIDI Player`(静态方法) | `VRCMidiPlayer` 组件 | ✅ 组件(无静态方法) |
| Play 方法 | `PlayMidiFile(VRCUrl url)` | `player.Play()` 实例方法 | ✅ 实例方法 |
| Stop 方法 | `StopMidiFile()` | `player.Stop()` 实例方法 | ✅ 实例方法 |
| Pause/Resume | `PauseMidiFile() / ResumeMidiFile()` | ❌ 不存在 | ❌ 仅 `Stop()`,需手动用 `time` 暂停 |
| 事件前缀 | `OnMidiNoteOn` | `MidiNoteOn` | ✅ 无 `On` 前缀 |
| 事件 player 参数 | `VRCPlayerApi player` | 无 | ✅ 无 player 参数 |

> 任务表中推测的"VRC MIDI Player 静态方法"API **是错误信息**,可能是参考了已弃用的旧版 MIDI Player。当前 SDK **只支持组件方式**。

---

## 与知识库互补

| 关联知识库 | 路径 | 说明 |
|----------|------|------|
| **MIDI 总览** | [`./index.md`](./index.md) | 3 个事件签名 + 技术参数速查 |
| **实时 MIDI** | [`./realtime-midi.md`](./realtime-midi.md) | 真实设备输入 |
| **MIDI Playback 示例** | `memory/world/examples/midi-playback.md` | 4-Grid LogoButton 完整实现 |
| **Udon 事件完整参考** | `memory/api/events-reference.md` | 事件方法 + 调用约束 |
| **AudioLink** | `memory/hybrid/audiolink-system.md` | 音频驱动视觉的另一种方式 |
| **MIDI 节点(图)** | `memory/world/udon/graph/event-nodes.md` | Node Graph 中的 MIDI 事件 |
| **MIDI Standard Files** | https://midi.org/standard-midi-files | SMF 规范 |

---

## 二次开发建议

| 扩展方向 | 实现思路 |
|---------|---------|
| **添加更多 Grid** | 复制 Grid Prefab,加入 `grids` 数组,同步扩展 `channels` 数组 |
| **自定义映射** | 把 `int % 12` 换成查表(`Dictionary<int, Color>` MIDI → 颜色) |
| **力度相关动画** | 监听 `velocity` 参数,实现力度相关的视觉强度(透明度/缩放) |
| **MIDI 数据预处理** | 启动时读取 `player.midiData`,缓存音符时间表,避免在 `MidiNoteOn` 中遍历整个 track |
| **多音轨混合** | 每个音轨用一个 `VRCMidiPlayer`,不同 Target Behaviours 接收不同通道 |
