---
title: "Network Stats | VRChat Creation"
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
  - world
  - networking
  - udon
aliases:
  - "Network Stats | VRChat Creation"
  - network-stats
related:
  - network-id-utility.md
  - "../../avatar-events.md"
  - "../../graph/event-nodes.md"
  - "../compatibility.md"
  - "../debugging.md"
---
# Network Stats | VRChat Creation

> 来源:https://creators.vrchat.com/worlds/udon/networking/network-stats/
> SDK 版本:VRChat SDK 3.x(2025-08-01)
> 分类:Networking 工具 → 运行时统计 API
> **核心类**:`VRC.SDK3.Network.Stats`(静态类)

---

## 概述

VRChat 通过 **`VRC.SDK3.Network.Stats`** 静态类暴露 Udon 可访问的网络统计指标。

**两类统计**:
- **Global Network Statistics**:整个实例级别的网络状态
- **Per GameObject / Per Player Statistics**:单个对象/玩家的网络开销

**典型用途**:
- 实时监控带宽使用,避免触发 VRChat 网络限制(~11 KB/s)
- 定位高开销对象(序列化频率、字节数)
- 调试"卡顿"问题(延迟、抖动)
- 动态调整同步策略(过载时降频)

---

## 全局网络统计(Global Network Statistics)

| 名称 | 类型 | 描述 |
|------|------|------|
| `ThroughputPercentage` | `float` | **当前已用输出吞吐占允许上限的百分比**(运行平均值) |
| `RoundTripVariance` | `float` | 与服务器往返时间的 **统计方差** |
| `BytesInMax` | `float` | **单秒接收字节数的峰值** |
| `BytesOutMax` | `float` | **单秒发送字节数的峰值** |
| `BytesOutAverage` | `float` | **每秒发送字节数的运行平均值** |
| `BytesInAverage` | `float` | **每秒接收字节数的运行平均值** |
| `HitchesPerNetworkTick` | `float` | **每个网络 tick 缺失样本数的运行平均值** |
| `Suffering` | `float` | **队列中待发送消息数**(拥塞指标) |
| `TimeInRoom` | `float` | **当前实例停留时长**(秒) |

### 关键指标解读

| 指标 | 警戒线 | 解读 |
|------|--------|------|
| `ThroughputPercentage` | > 80% | 接近带宽上限,可能触发丢包/限流 |
| `Suffering` | > 50 | 队列堆积,网络过载 |
| `BytesOutMax` | 接近 11 KB/s | 触发 VRChat 限流(总带宽上限) |
| `HitchesPerNetworkTick` | > 阈值 | 客户端帧率问题,非网络问题 |
| `RoundTripVariance` | 高 | 延迟抖动大,Continuous 同步不平滑 |

---

## 单对象 / 单玩家统计(Per GameObject and Per Player Statistics)

> **默认行为**:如果对象 **未通过网络同步** 或 **不在网络拓扑中**,所有统计返回默认值(0 / false)。

| 名称 | 类型 | 描述 |
|------|------|------|
| `UpdateInterval` | `float` | **该对象发送网络消息的时间间隔**(运行平均值,秒) |
| `ReceiveInterval` | `float` | **该对象接收网络消息的时间间隔**(运行平均值,秒) |
| `FinalDelay` | `float` | **对象的同步时间调整量**(秒) |
| `Group` | `int` | VRChat 将相近对象分组同步,这是对象所属的组号 |
| `GroupDelay` | `float` | **该组所有对象的同步调整平均值**(秒) |
| `Sleeping` | `bool` | **`true` 表示对象空闲,无网络收发** |
| `Size` | `int` | **最近一次网络消息的字节数** |
| `BytesPerSecondAverage` | `float` | **该对象的网络吞吐运行平均值**(字节/秒) |
| `TotalBytes` | `int` | **该对象的累计网络数据量**(字节) |
| `ReliableEventsInOutboundQueue` | `int` | **该对象待发送的可靠事件数**(Manual sync 等) |
| `LastSendTime` | `float` | **该对象最后一次发送消息的时间** |
| `LastReceiveTime` | `float` | **该对象最后一次接收消息的时间** |

---

## 典型使用模式

### 模式 1:带宽监控 UI

```csharp
using UdonSharp;
using VRC.SDK3.Network;
using UnityEngine.UI;

public class NetworkStatsHUD : UdonSharpBehaviour
{
    public Text statsText;

    void Update()
    {
        float throughput = Stats.ThroughputPercentage;
        float bytesOut = Stats.BytesOutAverage;
        float bytesIn = Stats.BytesInAverage;
        float suffering = Stats.Suffering;

        statsText.text = $"Throughput: {throughput:F1}%\n" +
                        $"Out: {bytesOut:F0} B/s\n" +
                        $"In: {bytesIn:F0} B/s\n" +
                        $"Suffering: {suffering:F0}";
    }
}
```

**应用**:World 中提供开发者 HUD 监控网络状态。

### 模式 2:动态限流

```csharp
void Update()
{
    // 当吞吐超过 80% 时,停止发送非关键同步
    if (Stats.ThroughputPercentage > 80f)
    {
        StopNonCriticalSync();
    }
}
```

### 模式 3:对象级调试

```csharp
public void LogObjectStats(GameObject obj)
{
    float bps = Stats.GetBytesPerSecondAverage(obj);
    int size = Stats.GetSize(obj);
    bool sleeping = Stats.GetSleeping(obj);

    Debug.Log($"[NetStats] {obj.name}: " +
              $"BPS={bps:F0}, Size={size}, Sleeping={sleeping}");
}
```

**应用**:定位 "哪些对象消耗了最多带宽"。

### 模式 4:死对象检测

```csharp
void Update()
{
    // 如果对象空闲超过 10 秒且不在 Group 0,可能是僵尸对象
    float timeSinceReceive = Time.time - Stats.GetLastReceiveTime(gameObject);
    if (timeSinceReceive > 10f && Stats.GetSleeping(gameObject))
    {
        // 对象已停止同步
    }
}
```

---

## API 使用注意

### 静态类访问

```csharp
using VRC.SDK3.Network;

// 全局统计(直接通过类名访问)
float throughput = Stats.ThroughputPercentage;

// 对象级统计(通过 GameObject 参数)
float bps = Stats.GetBytesPerSecondAverage(myGameObject);
int size = Stats.GetSize(myGameObject);
bool sleeping = Stats.GetSleeping(myGameObject);
```

### ⚠️ 默认值陷阱

> **未同步对象返回默认值**(0 / false),不会抛错!

```csharp
// 这是常见错误:以为对象没同步就是有问题
if (Stats.GetSleeping(unrelatedObject))
{
    // 实际上 unrelatedObject 从未同步,永远返回 true(默认)
}
```

**正确做法**:
```csharp
if (IsNetworkedObject(obj) && Stats.GetSleeping(obj))
{
    // 对象确实在同步,且当前空闲
}
```

---

## 与其他工具的区分

| 工具/特性 | 范围 | 运行时/Editor | 用途 |
|----------|------|--------------|------|
| **`VRC.SDK3.Network.Stats` API**(本文) | 程序化访问 | **Runtime** | 集成到 World 逻辑中 |
| **VRChat 客户端 Stats 窗口** | 客户端 UI | **Runtime** | 用户/开发者可视化(见 task-08 world-debug-views) |
| **Network ID Utility**(见 `network-id-utility.md`) | ID 管理 | **Editor Only** | 分配/导入/导出 Network ID |
| **ClientSim**(见 `memory/sources/clientsim.md` 和 `memory/world/clientsim/index.md`) | Editor 内模拟网络环境 | **Editor Only** | 4 个调试窗口(Settings / PlayerObject / PlayerData / 主窗口) |

### ClientSim vs Network Stats API

> ⚠️ **重要区分**:ClientSim **没有** 专门的 "Network 图表" 工具。它的 4 个窗口是:
> - **Settings Window** - ClientSim 配置
> - **PlayerObject Editor** - 调试 PlayerObject
> - **PlayerData Editor** - 调试 PlayerData
> - **Main Window** - 控制 ClientSim 启停
>
> ClientSim 的核心价值是 **模拟网络行为**(触发 `OnDeserialization` 等事件),而不是 **可视化网络流量**。

| 维度 | ClientSim | `VRC.SDK3.Network.Stats` API |
|------|-----------|------------------------------|
| **运行位置** | Unity Editor(ClientSim 模式) | VRChat 客户端(Runtime) |
| **数据来源** | 模拟数据(伪网络) | 真实网络数据 |
| **访问方式** | Editor 窗口 GUI | Udon 脚本 API |
| **适用场景** | 开发期快速测试网络事件流 | 实际部署后的运行时监控 |
| **指标** | 无可视化(4 个调试窗口不含网络图表) | 数值(可编程) |
| **远程玩家** | **不模拟** | 真实存在 |
| **`byteCount` 语义** | 属性数量 | 实际字节数 |

详细 ClientSim Networking 差异:见 `memory/world/clientsim/index.md` 的 "Networking Differences in ClientSim" 章节。

---

## 关键要点

| 要点 | 说明 |
|------|------|
| **核心类** | `VRC.SDK3.Network.Stats`(静态类) |
| **两类统计** | Global(实例级)+ Per Object(对象级) |
| **核心指标** | `ThroughputPercentage` / `BytesOutMax` / `Suffering` |
| **带宽上限** | VRChat 限制 ~11 KB/s,`ThroughputPercentage` 接近 100% 即触顶 |
| **默认值陷阱** | 未同步对象返回 0/false,需主动判断 |
| **典型用途** | 带宽监控 UI、动态限流、对象级调试 |
| **跨工具** | 与 ClientSim Network 图表、客户端 Stats 窗口、Network ID Utility 互补 |
| **SDK 版本** | SDK 3.x 通用(可能随版本更新) |

---

## 与带宽限制的关系

> 📌 来自 `memory/api/networking.md` 的事实:
> **VRChat 总带宽: ~11 KB/s**(所有玩家/对象总和)
> **Manual sync: 280,496 bytes/serialization**
> **Continuous sync: ~200 bytes/serialization**

**Network Stats 的应用**:
- `ThroughputPercentage` 接近 100% → 触发限流
- `BytesOutMax` 接近 11,000 B/s → 接近上限
- `Suffering` > 50 → 队列堆积,网络饱和

**实践**:
- World 中加入 Network Stats HUD,让开发者实时看到带宽压力
- 触发限流时主动降级(降低序列化频率、合并小数据)
- 配合 `OnDeserialization` 频率统计,定位热点

---

## Missing Information

- `Stats` 类的 **完整方法签名**(Getter 方法命名规则,文档未明示)
- 是否支持 **Player 级别统计**(文档提到 "Per Player" 但未给出示例)
- `Group` 分组的具体算法(VRChat 如何决定分组?)
- `HitchesPerNetworkTick` 的正常值范围
- 指标是否在 **Editor / Build / Client** 模式下都可用

> 以上信息文档未明确说明,需要进一步实验或查阅 SDK 源码。
