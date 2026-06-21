---
title: Pattern: Advanced Sync Patterns
category: patterns

knowledge_level: applied
status: active

tags:
  - patterns
  - patterns
  - constraint
  - sync
  - serialization
  - event

aliases:
  - "同步"
  - "Advanced Sync Patterns"

source: VRChat Agent Skills 模板(参考工程)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Pattern: Advanced Sync Patterns


---

## 1. Packed Sync Data

### Problem
每个 `[UdonSynced]` 变量有独立开销。多个小值浪费 budget。

### Solution
用 Vector3 的 3 个 float 组件存储 3 个独立 int 值，或用 int 的 32 bit 存储多个 flag。

### Constraints
- float 有 24-bit mantissa 精度 → int 最大 16,777,216 精确 round-trip
- 解包时用 `Mathf.RoundToInt` 吸收浮点噪声
- 不能用于需要插值的值

### Template
`PackedStateSync.cs` — `OnPreSerialization` 调用 `PackState()` 写入 Vector3 组件；`OnDeserialization` 调用 `UnpackState()` 恢复。

---

## 2. Rate-Limited Serialization

### Problem
快速操作（slider 拖动）每秒触发数十次变化事件，每次都 `RequestSerialization()` 会淹没 11KB/s 预算。

### Solution
`_syncLocked` flag + `SendCustomEventDelayedSeconds` 强制序列化间隔（如 0.15s）。cooldown 窗口内只保存最新值，窗口结束时一次性发送。

### Template
`RateLimitedSync.cs` — SyncCooldown (0.15s)、_syncLocked、_changeCounter。首变设置 lock 并调度 _OnSyncUnlock，后续变化更新 _localValue。解锁时若 counter 有变化则多一次窗口确保最终值发出。

---

## 3. Dual-Copy Sync Variables

### Problem
直接读写 `[UdonSynced]` 字段容易出错——非 owner 写入被静默丢弃。

### Solution
维护本地工作副本 + synced 传输副本，严格分离：
- `OnPreSerialization`: local → synced（仅在 dirty flag 时）
- `OnDeserialization`: synced → local
- 所有游戏逻辑只读 local 副本

### Template
`DualCopySync.cs` — `volume` (public local) / `_syncedVolume` (private UdonSynced)。`_dirty` flag 防止不必要的序列化。

---

## 4. Delayed Serialization Batching

### Problem
多个快速事件各自调用 `RequestSerialization()`，产生重复包。

### Solution
设置 pending flag，调度单次延迟序列化。所有在延迟触发前到达的变化批量到一个包。

### Template
`BatchedSync.cs` — `_syncPending` 使 `ScheduleBatchedSync` 幂等。BatchDelay 0.2s。所有字段在一个包中序列化。建议 100-300ms 延迟。

---

## 5. IsClogged Retry Pattern

### Problem
网络拥塞时 `RequestSerialization()` 可能静默丢弃。没有内置重试/确认。

### Solution
`TrySerialize` 检查 `Networking.IsClogged`。拥堵时跳过调用，用 `SendCustomEventDelayedSeconds` 调度重试，线性退避。

### Template
`CloggedRetrySync.cs` — MaxRetries=5、线性退避 `RetryDelay * retryCount`。`_retryPending` 防止重试链叠加。放弃后下次调用重置计数器。

---

## When To Use Each Pattern

| 场景 | 模式 |
|---|---|
| 需要将多个小值压缩为一个 synced var | 1. Packed Sync |
| Slider/快速交互需节流 | 2. Rate-Limited |
| 复杂系统需要干净的本地/synced 分离 | 3. Dual-Copy |
| 多个事件几乎同时发生 | 4. Batched Sync |
| 需要可靠的网络传输 | 5. IsClogged Retry |
