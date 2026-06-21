# API: AudioSource

> Type: API
> Confidence: Medium-High
> Source: 社区经验 + 项目实测
> Last Updated: 2026-06-04

---

## AudioSource 在 Udon 中的暴露

### AudioSource.Play()
- **暴露**: ✅
- **热路径**: ✅
- **说明**: 播放 AudioClip。适合一次性触发。

### AudioSource.Stop()
- **暴露**: ✅
- **热路径**: ✅

### AudioSource.Pause()
- **暴露**: ⚠️ 需要验证

### AudioSource.PlayOneShot(AudioClip clip)
- **暴露**: ⚠️ 需要验证
- **说明**: 不确定是否暴露。建议使用多个 AudioSource 组件作为替代。

### AudioSource.volume
- **暴露**: ✅

### AudioSource.pitch
- **暴露**: ✅

### AudioSource.loop
- **暴露**: ✅

### AudioSource.isPlaying
- **暴露**: ⚠️ 需要验证

### AudioSource.clip
- **暴露**: ✅

## 网络同步模式

### 音效 = Network Event
```csharp
// Owner 触发音效
public override void Interact() {
    SendCustomNetworkEvent(NetworkEventTarget.All, nameof(PlayClickSound));
}

public void PlayClickSound() {
    _audioSource.Play();
}
```

### 持续背景音 = 本地派生
```csharp
// 根据 synced state 本地控制
// 不需要同步 AudioSource 状态本身

public int State {
    set {
        _state = value;
        if (_state == STATE_ALARM) {
            _alarmSource.Play();
        } else {
            _alarmSource.Stop();
        }
    }
}
```

## 常见错误
- 同步 AudioSource 的 play/stop 状态（应本地派生）
- 在热路径中频繁 Play()（创建新的音频通道）
- 多个 Behaviour 同时控制同一个 AudioSource
