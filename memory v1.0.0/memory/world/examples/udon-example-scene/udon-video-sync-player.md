# Udon Video Sync Player

> Udon Example Scene · 视频同步子页面
> 源文档:https://creators.vrchat.com/worlds/examples/udon-example-scene/udon-video-sync-player
> 最后更新:2026-06-15

---

## 概述

UdonSyncPlayer 演示如何使用 **Unity / AVPro 视频播放器**加载并同步视频播放,让所有人(及迟加入者)同步观看。

> 同步两个核心要素:
> 1. **视频 URL**:所有人观看相同视频
> 2. **播放时间**:所有人同步到相同时间点

---

## 同步流程(整体时序)

### 发起者流程

```
Become Owner of UdonSyncPlayer Object
    ↓
Send new URL
    ↓
Try to Load & Play URL
    ↓
When Video Starts → Send Sync info out
    ↓
Send new Sync info every syncFrequency seconds
```

### 其他用户流程

```
Receive new URL value
    ↓
Try to Load & Play URL
    ↓
Receive Sync Info → Jump to synced time
```

---

## 1. 某人加载 URL(Someone Loads a URL)

**场景**:有 2 人在房间,某人粘贴新 URL 到 Input Field,触发 `OnURLChanged` 事件。

```csharp
public void OnURLChanged() {
    // 1. 将 LocalPlayer 设为 Owner(以便控制变量)
    if (!Networking.IsOwner(gameObject)) {
        Networking.SetOwner(Networking.LocalPlayer, gameObject);
    }
    
    // 2. 从 InputField 获取 URL
    string newUrl = inputField.text;
    
    // 3. 用 SetProgramVariable 设置 url 变量(等效于 "sendChange" = ON)
    this.SetProgramVariable("url", newUrl);
    
    // 4. 通知 Udon 更新 url 给所有人
    RequestSerialization();
}
```

> **小贴士**:`SetProgramVariable` 等价于"sendChange" 开关开启的 `set url`——如果想在另一个 UdonBehaviour 上修改变量,这是常用方式。
>
> **小贴士**:代码中有 `IsValid` 检查防止对象已销毁/未正确设置。后续说明中省略以保持简洁。

---

## 2. 用户获取新 URL(Users Get New URL)

由于 graph 中有 url 的 **Variable Change 事件**,URL 更新时**自动触发**该事件,直接尝试播放 URL。

```csharp
public void OnUrlChanged() {  // Variable Change 事件
    // 加载并播放新 URL
    LoadAndPlayUrl(url);
}
```

---

## 3. 视频开始(The Video Starts)

视频实际开始播放时**本地触发**该事件。**Owner 和其他人都调用同一事件**,差异在 `UpdateTimeAndOffset` 内部分支处理。

```csharp
public void OnVideoStart() {
    UpdateTimeAndOffset();  // Owner 同步时间,Non-Owner 走 Resync 分支
}
```

---

## 4. 更新时间与偏移(Update Time and Offset)

### 关键判断

```csharp
public void UpdateTimeAndOffset() {
    if (!Networking.IsOwner(gameObject)) {
        Resync();  // 非 Owner 走 Resync
        return;
    }
    
    // Owner:同步两个数(视频时间 + 服务器时间锚点)
    float currentVideoTime = videoPlayer.time;
    double serverTime = Networking.GetServerTimeInSeconds();
    
    // 合并为单个 Vector2 变量(简化同步逻辑)
    timeAndOffset = new Vector2(currentVideoTime, (float)serverTime);
    
    RequestSerialization();
    
    // 周期性更新(可选,用于处理快进/暂停/重播)
    SendCustomEventDelayedSeconds(nameof(UpdateTimeAndOffset), syncFrequency);
}
```

### 关键设计:**Vector2 合并同步**

| 分量 | 含义 |
|------|------|
| `timeAndOffset.x` | 视频当前时间 |
| `timeAndOffset.y` | Owner 处于该视频时间时的服务器时间 |

**优势**:把两个相关数值合并到单个变量,简化同步逻辑,减少请求次数。

### 简化选项

> 如果 Owner 永不暂停/快退/快进,可设 `syncFrequency = 0`,所有人从视频**开始时间**同步,而非周期性更新时间。

---

## 5. 重新同步(Resync)

非 Owner 收到 `timeAndOffset` 后,根据服务器时间差**跳转视频**。

**示例**:
```
1. Owner 在 video-time=0 时设置 timeAndOffset = (0, 1000)
2. 你在 45 秒后加入,收到该值
3. 你的 server-time = 1045
4. 计算差值:1045 - 1000 = 45 秒
5. 跳到视频 00:45
```

```csharp
public void Resync() {
    float videoTimeAtSync = timeAndOffset.x;
    double serverTimeAtSync = timeAndOffset.y;
    double currentServerTime = Networking.GetServerTimeInSeconds();
    
    double serverDelta = currentServerTime - serverTimeAtSync;
    float targetVideoTime = videoTimeAtSync + (float)serverDelta;
    
    videoPlayer.time = targetVideoTime;
    videoPlayer.Play();
}
```

---

## 改进方向(Improvements and Augmentations)

官方列出的可改进点:

| 改进 | 说明 |
|------|------|
| **延迟播放等待** | 非 Owner 等待接收 Owner 信息后再播放 |
| **流媒体检测** | 检测流媒体 URL vs 视频,关闭流媒体的同步 |
| **错误处理** | 处理 Video Error 事件,给用户友好提示 |
| **权限控制** | 仅允许特定玩家更改视频 |
| **播放列表** | 创建视频播放列表 |
| **视频队列** | 创建视频 Queueing 系统 |

---

## 关键设计模式

### 模式 1:URL 同步 + 时间同步解耦

- **URL 同步**:Variable Change 触发(单次)
- **时间同步**:周期性 Vector2 同步(可选)

### 模式 2:Vector2 复合同步变量

将两个相关数值打包到一个 Vector2,减少序列化次数和复杂度。

### 模式 3:服务器时间作为全局基准

`Networking.GetServerTimeInSeconds()` 是同步计算的"真理源"——所有人对同一时刻有共识。

### 模式 4:周期性 + 事件驱动混合同步

- URL 变化 → Variable Change 立即同步
- 视频时间 → 周期性 SendCustomEventDelayedSeconds 同步

---

## 与相关知识库关联

- **Manual Sync 模式**:`memory/api/networking.md`
- **时间同步算法**:参考 `memory/FACT.md` 中 **视频播放器时间同步算法(参考工程)**(更复杂的生产实现)
- **Video Player API**:`memory/api/video-player.md`(参见 task-17)

---

## 参见

- **视频播放器时间同步算法模式(参考工程)**:本地知识库,生产级视频同步参考(更完善的 VRCUrl + 时间同步实现)
- **Manual Sync 完整规范**:`memory/api/networking.md`
