---
title: API: Networking
category: api

knowledge_level: core
status: active

tags:
  - api
  - networking
  - sync
  - serialization
  - ownership

aliases:
  - Networking
  - "网络 API"
  - 网络同步
  - "Networking API"

related:
  - world/udon/networking/index.md
  - world/udon/networking/compatibility.md
  - world/udon/networking/events.md
  - world/udon/networking/variables.md
  - world/udon/networking/ownership.md
  - world/udon/networking/late-joiners.md
  - world/udon/networking/network-components.md
  - world/udon/networking/debugging.md
  - world/udon/networking/performance.md
  - world/udon/networking/network-details.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-04
confidence: High
---
# API: Networking

---

## Networking (UdonBehaviour 成员)

### Networking.SetOwner(VRCPlayerApi player, GameObject obj)
- **暴露**: ✅
- **热路径**: ❌ (涉及 ownership transfer network message)
- **说明**: 将 obj 的 ownership 转移给 player。只有当前 owner 可以转移。非 owner 调用无效果。
- **注意**: Transfer 不是即时的，有网络延迟。transfer 完成后触发 `OnOwnershipTransferred()`。

### Networking.LocalPlayer
- **暴露**: ✅
- **热路径**: ✅
- **说明**: 返回本地玩家的 VRCPlayerApi。在 Start 中缓存引用。

### Networking.GetOwner(GameObject obj)
- **暴露**: ✅
- **热路径**: ✅ (轻量查询)
- **说明**: 返回 obj 的当前 owner。

### Networking.IsOwner(GameObject obj)
- **暴露**: ✅
- **热路径**: ✅
- **说明**: 检查本地玩家是否是 obj 的 owner。常用于 guard clause。

## UdonBehaviour 同步成员

### RequestSerialization()
- **暴露**: ✅
- **热路径**: ⚠️ (会触发序列化，不适合每帧调用)
- **说明**: Manual Sync 模式下，显式请求序列化 synced variable。修改后必须调用。

### OnDeserialization()
- **暴露**: ✅
- **热路径**: ✅ (网络事件驱动)
- **说明**: 收到远端 synced variable 更新时调用。Late joiner 加入时也会调用。

### OnPreSerialization()
- **暴露**: ✅
- **热路径**: ⚠️ (每次序列化前调用)
- **说明**: 序列化前准备数据。可以在这里更新 synced variable 为最新值再序列化。

### OnPostSerialization()
- **暴露**: ✅
- **热路径**: ⚠️
- **说明**: 序列化完成后调用。少见使用场景。

### SendCustomNetworkEvent(NetworkEventTarget target, string eventName)
- **暴露**: ✅
- **热路径**: ⚠️ (产生网络消息)
- **说明**: 向指定目标发送网络事件。eventName 必须是无参方法名。
- **Target 选项**: `NetworkEventTarget.All`, `NetworkEventTarget.Owner`

### BehaviourSyncMode
- `NoVariableSync` — 不同步任何变量
- `Manual` — 手动调用 RequestSerialization 同步
- `Continuous` — 自动持续同步

### UdonSyncMode（同步变量插值模式）
用于 `[UdonSynced]` 属性的可选参数，控制网络同步时的插值行为：

| Mode | 说明 | 适用场景 |
|------|------|---------|
| `None` | 无插值（默认） | 离散状态、开关、枚举值 |
| `Linear` | 线性插值 (lerp) | 连续位置、速度 |
| `Smooth` | 平滑插值 | 需要更自然过渡的值 |
| `NotSynced` | 显式不同步 | 本地计算或手动同步 |

```csharp
[UdonSynced] public bool toggle;                    // 默认 None
[UdonSynced(UdonSyncMode.Linear)] public float progress;  // 线性插值
[UdonSynced(UdonSyncMode.NotSynced)] public int localOnly; // 不同步
```

**注意**: `NotSynced` 用于需要本地计算后手动同步的场景，与 `BehaviourSyncMode.None` 不同。

---

## Bandwidth Limits ⚠️

| 限制类型 | 数值 | 说明 |
|---------|------|------|
| **总带宽** | ~11 KB/s | Udon scripts 可发送的总带宽 |
| **Manual Sync** | 280,496 bytes/serialization | 每次序列化最大数据量 |
| **Continuous Sync** | ~200 bytes/serialization | 每次序列化最大数据量 |

### 超出限制后果
- 网络拥塞
- `IsClogged` 返回 true
- 数据丢失或延迟

### 优化建议
- Manual Sync 用于离散状态（棋盘位置、游戏状态）
- Continuous Sync 用于高频变化（位置、进度条）
- 避免频繁序列化

---

## Network Events Rate Limiting

### [NetworkCallable] (SDK 3.8.1+)
```csharp
[NetworkCallable(maxEventsPerSecond: 50)]
public void MyNetworkedMethod() { }
```

- 限制方法每秒可被调用的次数
- 范围: 1-100
- 默认: 无限制（但有隐含限制）

### NetworkCalling API
```csharp
// 获取指定事件排队数
int queued = NetworkCalling.GetQueuedEvents(target, eventName);

// 获取所有排队事件
int allQueued = NetworkCalling.GetAllQueuedEvents();
```

### 安全建议
- 私有方法或以下划线 `_` 开头的方法不会被网络调用
- `[NetworkCallable]` 显式标记网络可调用方法

---

## 常见错误
- Manual Sync 忘记 RequestSerialization（最常见 bug）
- 非 owner 调用 SetOwner（无效果但不报错）
- Continuous Sync 用于离散状态
- SendCustomNetworkEvent 用于 late joiner 需要的状态
- 超出带宽限制导致网络拥塞

---

## 深入阅读(应用层详解)

> 本文档为 **API 速查表**。完整的应用层详解、模式、案例、风险分析见 `memory/world/udon/networking/` 子分类。

| 子页面 | 主题 |
|--------|------|
| `memory/world/udon/networking/index.md` | Networking 概述、带宽限制速查、Manual vs Continuous 决策树 |
| `memory/world/udon/networking/compatibility.md` | 跨版本兼容、降级策略、Serialization 限制 |
| `memory/world/udon/networking/events.md` | 完整 Network Events 列表、`[NetworkCallable]`、速率限制(5-100/s) |
| `memory/world/udon/networking/variables.md` | 完整 `[UdonSynced]` 字段类型表、序列化大小、FieldChangeCallback |
| `memory/world/udon/networking/ownership.md` | 完整所有权转移流程、Master vs InstanceOwner、SetOwner 安全 |
| `memory/world/udon/networking/late-joiners.md` | Late Joiner 同步策略、Buffer Events、OnPlayerJoined 模式 |
| `memory/world/udon/networking/network-components.md` | VRCObjectSync、VRCPickup、VRCObjectPool、Networking 属性/事件 |
| `memory/world/udon/networking/debugging.md` | World Debug Views、ClientSim 调试、Stats API |
| `memory/world/udon/networking/performance.md` | 10 条带宽优化规则、对象池、合并序列化 |
| `memory/world/udon/networking/network-details.md` | 内部字节细节、Manual vs Continuous 字节差异、数组陷阱 |

> 数据来源:VRChat 官方 Creator Docs(2025-11-13 更新版本),本地化日期 2026-06-15。
