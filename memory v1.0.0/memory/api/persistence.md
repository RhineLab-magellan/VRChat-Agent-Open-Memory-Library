# API: Persistence (PlayerData / PlayerObject)

> Type: API
> Source: VRChat 官方文档 + VRChat Agent Skills 模板(参考工程)
> Confidence: High
> SDK Version: 3.7.4+
> Last Verified: 2026-06-04

---

## Storage Layer Decision Tree

```text
其他玩家需要看到这个值吗？
├─ 否 ── 跨 session / rejoin 需要保留吗？
│         ├─ 否 ──→ 非同步字段 (plain private field)
│         └─ 是 ─→ PlayerData (key-value, per-player)
│
└─ 是 ── 与特定玩家绑定还是世界共享？
          │
          ├─ Per-player ── 玩家需要场景中的 synced GameObject 吗？
          │                 ├─ 否 ──→ PlayerData (其他人通过 OnPlayerDataUpdated 读取)
          │                 └─ 是 ─→ PlayerObject (synced UdonBehaviour per player)
          │
          └─ 共享 ─────── Late joiner 需要看到当前值吗？
                            ├─ 否 ──→ SendCustomNetworkEvent
                            └─ 是 ─→ [UdonSynced] (Continuous or Manual)
```

## Storage Layers Quick Reference

| Layer | Scope | Lifetime | Capacity | Use |
|---|---|---|---|---|
| Non-synced field | Self | Scene reload | Unlimited | UI state, timers |
| [UdonSynced] | All players | Instance lifetime | ~200B (Cont) / ~280KB (Manual) | Shared game state |
| SendCustomNetworkEvent | All players | Instant | Event name only | Sound, particle triggers |
| PlayerData | Per player, readable by all | Cross-session | 100 KB/player/world (压缩) | Settings, unlocks, scores |
| PlayerObject | Per player, synced behaviour | Instance + cross-session | 100 KB/player/world (压缩) | Complex per-player state |

---

## Storage Compression ⚠️

VRChat 使用压缩格式存储数据：
- **实际限制**: 100 KB per player per world（压缩后）
- **原始数据**: 可存储最多 ~300 KB 原始数据（压缩至 100 KB）
- **压缩效果**: 取决于数据可压缩性

### 存储限制详情
| 类型 | 限制 | 说明 |
|------|------|------|
| PlayerData | 100 KB/player | 独立配额 |
| PlayerObject | 100 KB/player | 独立配额 |
| String max | ~50 chars | 建议值 |
| Key max | 128 chars | 建议值 |

---

## PlayerData API

### Setup
1. `using VRC.SDK3.Persistence;`
2. Enable persistence on UdonBehaviour
3. Wait for `OnPlayerRestored` before access

### Key Methods
```csharp
// Read (returns false if key doesn't exist)
PlayerData.TryGetInt(player, "key", out int value);
PlayerData.TryGetString(player, "key", out string value);
PlayerData.TryGetFloat(player, "key", out float value);
PlayerData.TryGetBool(player, "key", out bool value);
PlayerData.TryGetBytes(player, "key", out byte[] value);
PlayerData.TryGetVector3(player, "key", out Vector3 value);

// Write (only to local player)
PlayerData.SetInt(Networking.LocalPlayer, "key", value);
PlayerData.SetString(Networking.LocalPlayer, "key", value);

// Utility
PlayerData.HasKey(player, "key");
PlayerData.DeleteKey(Networking.LocalPlayer, "key");
PlayerData.GetKeys(player); // returns string[]
```

### Critical Rules
- ⚠️ 在 `OnPlayerRestored` 触发前写入 → 静默忽略。始终用 `_dataReady` flag 守卫。
- ⚠️ String key 计入 100KB 限制，保持 key 名短小
- ⚠️ 只能写入本地玩家的数据。其他玩家只读。
- Limit: 100KB per player per world; String max ~50 chars; Key max 128 chars

---

## PlayerObject API

### Concept
每个玩家自动实例化一个 prefab 副本，own 该副本。支持 `[UdonSynced]` 变量实时同步。

### Setup
1. Create prefab with: `VRCPlayerObject` + `UdonBehaviour` + `VRCEnablePersistence`
2. Place one instance in scene
3. VRChat 自动为每个玩家实例化

### Key Behavior
- `OnPlayerRestored` 在**所有** PlayerObject 实例上触发，不只是本地玩家的
- 必须用 `if (!Networking.IsOwner(player, gameObject)) return;` 守卫
- Instances are owned by their player — `Networking.SetOwner()` not needed

### PlayerData vs PlayerObject

| | PlayerData | PlayerObject |
|---|---|---|
| Type | Key-value store | Synced UdonBehaviour on prefab |
| Storage | 100 KB/player | 100 KB/player (separate quota) |
| API | Static methods | Direct field access |
| Visibility | Not synced to others | Fully synced via [UdonSynced] |
| Best for | Settings, scores, unlocks | Real-time per-player state |

---

## Storage Information API (SDK 3.10.0+)

```csharp
// Query storage usage
int used = player.GetPlayerDataStorageUsage();
int limit = player.GetPlayerDataStorageLimit();

// Request fresh usage data (async)
player.RequestStorageUsageUpdate();

// Event: fires when updated usage data available
public override void OnPersistenceUsageUpdated() { }
```

---

## Common Mistakes

| Mistake | Why | Fix |
|---|---|---|
| Writing before OnPlayerRestored | Silently ignored | Guard with _dataReady flag |
| [UdonSynced] for local-only data | Wastes bandwidth | Use non-synced field |
| SendCustomNetworkEvent for late joiner state | Late joiners miss it | Use [UdonSynced] |
| Duplicating value in both [UdonSynced] and PlayerData | Two sources of truth | Pick one layer |
| Changing PlayerObject prefab without checking Network IDs | Breaks persistence mapping | Audit Network IDs before restructure |
