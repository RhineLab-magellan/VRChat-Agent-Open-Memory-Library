---
title: Pattern: Bit-Packed Flags
category: patterns

knowledge_level: applied
status: active

tags:
  - patterns
  - patterns
  - constraint
  - networking
  - sync
  - serialization

aliases:
  - "Bit-Packed Flags"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Pattern: Bit-Packed Flags


---

## Problem
多个 bool 状态字段各自占用一个 `[UdonSynced]` 变量，浪费同步带宽和序列化步骤。需要压缩以减少网络开销。

## Context
- 3 个以上 bool 状态需要同步
- 例如：4 盏灯的开关状态、8 个按钮的按下状态
- 每个 bool 不需要独立变化检测（或可接受合并变化）

## Udon Constraints
- 每个 `[UdonSynced]` 变量在序列化时都有 header 开销
- int 在 Udon VM 中是原生类型，位运算可用
- 不支持 `BitArray` 等高级类型

## Networking Model

| 维度 | 决策 |
|---|---|
| State Owner | 对象 owner |
| Source of Truth | 单个 `[UdonSynced]` int/uint 作为 bit flags |
| Sync Type | Manual Sync |
| Synced Variables | `_flags` (int) — 所有 bool 打包为一个 int |
| Mutation Path | owner 使用位运算设置/清除/翻转 bit |
| Serialization Path | 修改后 `RequestSerialization()` |
| Receive Path | `FieldChangeCallback` 解析各个 bit 并更新表现 |
| Bandwidth Budget | 1 int (4 bytes) 代替 N 个 bool (N × ~2 bytes each) |
| Failure Mode | 位运算错误会导致多个状态同时错误 |

## Implementation Sketch

```csharp
// 位定义
private const int FLAG_LIGHT_0 = 1 << 0;  // 1
private const int FLAG_LIGHT_1 = 1 << 1;  // 2
private const int FLAG_LIGHT_2 = 1 << 2;  // 4
private const int FLAG_LIGHT_3 = 1 << 3;  // 8

[UdonSynced, FieldChangeCallback(nameof(Flags))]
private int _flags = 0;

public int Flags {
    get => _flags;
    set {
        _flags = value;
        UpdateAllLights();
    }
}

// 读取某个 flag
private bool GetFlag(int mask) => (_flags & mask) != 0;

// 设置某个 flag
private void SetFlag(int mask) {
    _flags |= mask;
    RequestSerialization();
}

// 清除某个 flag
private void ClearFlag(int mask) {
    _flags &= ~mask;
    RequestSerialization();
}

// 翻转某个 flag
private void ToggleFlag(int mask) {
    _flags ^= mask;
    RequestSerialization();
}
```

## When To Use
- 3+ 个关联 bool 状态需要同步
- 状态作为一个组一起变化
- 需要最小化 synced variable 数量

## When Not To Use
- 只有 1-2 个 bool（直接 sync 也 OK）
- 每个 bool 需要独立的 FieldChangeCallback 做不同的处理（可以用分层处理解决）
- bool 之间完全没有关联（但仍可通过位运算独立处理）

## Performance Comparison
```text
方案 A: 8 个独立的 [UdonSynced] bool
  = 8 × (serialization header + 1 byte) ≈ 16-24 bytes per change

方案 B: 1 个 [UdonSynced] int bit flags
  = 1 × (serialization header + 4 bytes) ≈ 8 bytes per change

节省: ~50-66% 带宽
```
