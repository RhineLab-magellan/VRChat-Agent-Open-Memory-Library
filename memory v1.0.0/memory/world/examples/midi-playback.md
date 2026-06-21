# MIDI Playback

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/midi-playback)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/midi-playback
> 文档版本: Last updated Nov 15, 2024
> SDK: 3.4+ (VRCMidiPlayer / MidiNoteOn / MidiNoteOff)

## Example Central Package

> ✅ **需要 Example Central Package** (含 MIDI 资产)
> 通过 `VRChat SDK → 🏠 Example Central` 导入
> 包含 MIDI 资产文件、音频文件、4 个 Grid Prefab

### Example World
- **World ID**: `wrld_57799f09-406a-4c8c-9c42-e593cae6305a`
- **URL**: https://vrchat.com/home/world/wrld_57799f09-406a-4c8c-9c42-e593cae6305a

### 资源说明
- ⚠️ **需要 MIDI 资产文件**(非 VRCUrl 网络加载)
- MIDI 是 **Unity Editor 内的 Asset**,不是 VRChat URL
- 任务表中"VRCUrl"标注为 **不准确**,实际是本地 MIDI Asset

---

## 概述

演示如何播放 **MIDI 文件** 并将其与音频文件同步。
- **MIDI 驱动视觉**: Note On/Off 事件触发图像变化
- **音频驱动听觉**: 同步播放对应的音频
- **典型场景**: 节奏游戏、音乐可视化、灯光秀同步

---

## 关键 Udon API

| API | 命名空间 | 说明 |
|-----|----------|------|
| `VRCMidiPlayer` | `VRC.SDK3.Midi` | 类似 AudioSource,但使用 MIDI Asset |
| `MidiNoteOn` | Udon Event | 收到 Note On 时触发 |
| `MidiNoteOff` | Udon Event | 收到 Note Off 时触发 |
| `MidiNote(int channel, int number, int velocity)` | 事件签名 | 三参数 |

### 事件签名

```csharp
public override void MidiNoteOn(int channel, int number, int velocity) { }
public override void MidiNoteOff(int channel, int number, int velocity) { }
```

---

## MidiGrid UdonBehaviour

### 公共变量(Inspector 暴露)

| 名称 | 类型 | 说明 |
|------|------|------|
| `grids` | `Transform[]` | 4 个 RectTransform(每个有 GridLayoutGroup + 12 个 Image 子物体) |
| `channels` | `int[]` | MIDI 通道到 Grid 的映射,默认 `[3, 4, 1, 2]` |
| `player` | `VRCMidiPlayer` | 发送事件给 MidiGrid 的播放组件 |

### 视觉化逻辑

```
Note On(channel=3, number=75)
  ↓
查找 channels 数组 → gridIndex=0 (因为 channels[0]=3)
  ↓
计算 noteNumber % 12 → 75 % 12 = 3 → 第 4 个子图像(C#=0, D=1, D#=2, E=3)
  ↓
启用 gridIndex=0 的 child[3] 的 Image
  ↓
控制台输出 "3 : 75"
```

**Note Off 行为相同,但 `enabled = false`。**

---

## Inspector 字段详解

### `channels` 数组
- **默认**: `[3, 4, 1, 2]`
- **意义**: MIDI 通道 3 → Grid 0,通道 4 → Grid 1,以此类推
- **自定义**: 修改顺序改变视觉映射关系

### 控制台输出格式
- 每个 Note On 输出 `"channel:noteNumber"`
- 例如 `"3:75"` 表示通道 3 播放了 note 75
- **调试技巧**: 加载自定义 MIDI 时,先观察控制台输出确定通道分布

---

## 完整 UdonSharp 代码(LogoButton.cs)

```csharp
using UdonSharp;
using UnityEngine;
using UnityEngine.UI;
using VRC.SDK3.Midi;

[UdonBehaviourSyncMode(BehaviourSyncMode.None)]
public class LogoButton : UdonSharpBehaviour
{
    [SerializeField] private Transform[] grids;
    [SerializeField] private VRCMidiPlayer player;
    [SerializeField] private int[] channels;

    private void Start()
    {
        // 启动时禁用所有 Grid 子图像
        foreach (var grid in grids)
        {
            for (var i = 0; i < grid.childCount; i++)
            {
                var child = grid.GetChild(i);
                var image = child.GetComponent<Image>();
                image.enabled = false;
            }
        }

        // 延迟 1 秒开始播放
        SendCustomEventDelayedSeconds(nameof(_PlayAudio), 1);
    }

    public void _PlayAudio()
    {
        player.Play();
    }

    public override void MidiNoteOn(int channel, int number, int velocity)
    {
        UpdateGridState(channel, number, true);
        Debug.Log($"{channel} : {number}");
    }

    public override void MidiNoteOff(int channel, int number, int velocity)
    {
        UpdateGridState(channel, number, false);
    }

    private void UpdateGridState(int midiEventChannel, int midiEventNoteNumber, bool isEnabled)
    {
        for (var gridIndex = 0; gridIndex < grids.Length; gridIndex++)
        {
            var gridChannel = channels[gridIndex];
            if (midiEventChannel != gridChannel) continue;

            // 12 音位量化(C=0, C#=1, ..., B=11)
            var child = grids[gridIndex].GetChild(midiEventNoteNumber % 12);
            var image = child.GetComponent<Image>();
            image.enabled = isEnabled;
        }
    }
}
```

---

## 关键设计模式

### 1. BehaviourSyncMode.None
> MIDI 播放是**本地播放**,不需要跨玩家同步
> 每玩家都从自己的 MIDI Asset 听到同步的音轨
> 这是 VRC 内置"内容一致性"的体现

### 2. Note On/Off 配对模式
- Note On 启用 → Note Off 禁用
- 严格配对,避免图像卡在 enabled 状态

### 3. 模 12 量化(MIDI Octave)
- 12 平均律,note number % 12 落在 [0, 11]
- 适合简单的可视化(每个音位一个图标)
- 复杂可视化可用查表(MIDI → 颜色/图像)

### 4. channels 数组作为映射表
- 解耦 MIDI 通道与显示 Grid
- 同一段 MIDI 可呈现不同视觉效果
- 易于扩展(>4 通道)

---

## 二次开发建议

- **添加更多 Grid**: 复制 Grid Prefab,加入 `grids` 数组,同时扩展 `channels` 数组
- **自定义映射**: 把 `int % 12` 换成查表(MIDI number → 颜色)
- **同步动画**: 监听 `velocity` 参数,实现力度相关的视觉强度

---

## 与知识库互补

- **Udon 事件完整参考**: `memory/api/events-reference.md`
- **VRC SDK3 MIDI 命名空间**: `memory/api/vrchat-sdk3.md`(待建)
- **AudioLink 系统**: `memory/hybrid/audiolink-system.md`(参考音频驱动视觉的另一种方式)

## 相关 Udon 文档链接

- [VRCMidiPlayer Component](/worlds/udon/midi/midi-playback/#component-vrcmidiplayer)
- [MIDI Note On Event](/worlds/udon/midi#midinoteon)
- [MIDI Note Off Event](/worlds/udon/midi#midinoteoff)
- [MIDI Standard Files](https://midi.org/standard-midi-files)
- [Unity GridLayoutGroup](https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/script-GridLayoutGroup.html)
