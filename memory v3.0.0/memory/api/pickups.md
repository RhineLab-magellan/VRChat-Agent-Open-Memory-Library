---
title: "API: Pickups (VRCObjectPickup)"
category: api
knowledge_level: core
status: active
source: "VRChat 官方文档 + 项目实测 + VRChat 2026.1.2 Release Notes"
source_type: official
version: 1.1
last_review: 2026-06-30
confidence: High
tags:
  - api
  - sync
  - pickup
  - ownership
aliases:
  - Pickups
  - "拾取 API"
  - VRCPickup
  - 拾取系统
related:
  - events-reference.md
  - networking.md
  - official-doc-clarifications.md
  - player-api.md
  - animator.md
---

---
# API: Pickups (VRCObjectPickup)


---

## VRCObjectPickup

VRCObjectPickup 是 VRChat 的内置拾取组件，挂载在 GameObject 上与 UdonBehaviour 配合。

### OnPickup()
- **暴露**: ✅
- **说明**: 玩家拾取对象时调用。此时 ownership 自动转移给拾取玩家。

### OnDrop()
- **暴露**: ✅
- **说明**: 玩家放下对象时调用。ownership 保留在放下玩家。

### OnPickupUseDown()
- **暴露**: ✅
- **说明**: 手持时按下 Use 键（Trigger）。

### OnPickupUseUp()
- **暴露**: ✅
- **说明**: 手持时松开 Use 键。

## VRCObjectSync

### 自动同步
- 位置、旋转由 VRCObjectSync 自动处理
- 不需要手动同步 Transform

### Respawn
- **暴露**: ⚠️ 需要验证
- **说明**: 重置对象到初始位置。

## 与 UdonBehaviour 配合

### 典型结构
```text
GameObject
  ├── VRCObjectPickup
  ├── VRCObjectSync
  └── UdonBehaviour (你的脚本)
```

### Sync Mode 建议
拾取对象使用 `BehaviourSyncMode.Continuous` 如果需要 synced variable 配合位置同步，或 `Manual` 仅用于状态同步。

### Ownership 转移
- Pickup 时 ownership 自动转移给拾取者
- Drop 时 ownership 保留
- 其他玩家 Pickup 时 ownership 自动转移

## 常见错误
- 拾取对象上使用 Manual Sync 但需要连续位置同步（位置由 VRCObjectSync 处理，独立于 UdonBehaviour SyncMode）
- OnDrop 中没有处理状态清理
- 多人争抢拾取时的竞态（通常由 VRChat 内置处理）

## 🔄 VRChat 修复历史 (2026.1.2+)

> **FACT** (2026.1.2):"Fixed an issue where Auto Hold could leave a pickup stuck in a 'grabbed' state for a remote user."

### 问题场景

| 场景 | 表现 | 修复状态 |
|------|------|----------|
| **AutoHold 启用** | 远端用户可能看到 Pickup **卡在"被抓住"状态** | ✅ 2026.1.2 修复 |
| **所有权转移异常** | Owner 已放下,但远端仍显示 grabbed | ✅ 2026.1.2 修复 |

### 创作者影响

| 影响项 | 说明 |
|--------|------|
| **无需代码改动** | 纯引擎层修复 |
| **AutoHold 行为恢复** | 2026.1.2+ 远端状态正确同步 |
| **旧版客户端** | 2026.1.1 及之前可能仍触发此问题 |

### 缓解措施(在旧版客户端仍有效)

```csharp
// 在 OnDrop 中显式重置 AutoHold 状态
public override void OnDrop()
{
    if (!Networking.IsOwner(gameObject)) return;
    // 显式重置内部状态以避免卡住
    // 注意:这只是缓解措施,2026.1.2+ 修复后不需要
}
```

### 关联文档

- `memory/world/scene-components/vrc-objectsync.md` - 物理同步与所有权
- `memory/api/events-reference.md` - OnPickup / OnDrop 事件签名
