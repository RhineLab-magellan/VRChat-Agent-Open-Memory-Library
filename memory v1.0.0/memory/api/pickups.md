# API: Pickups (VRCObjectPickup)

> Type: API
> Confidence: High
> Source: VRChat 官方文档 + 项目实测
> Last Updated: 2026-06-04

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
