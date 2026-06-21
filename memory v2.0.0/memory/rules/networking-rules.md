---
title: Rule Set: Networking Rules
category: rules

knowledge_level: applied
status: active

tags:
  - rules
  - rules
  - networking
  - sync
  - serialization
  - ownership

aliases:
  - "网络"

source: VRChat 官方文档 + UdonSharp 官方文档 + 项目实测
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Rule Set: Networking Rules


---

## RULE-NW-01: Owner Writes Synced State

### Rule
`[UdonSynced]` 变量应由 owner 写入。非 owner 修改同步变量会导致不可预期的行为。

### Reason
VRChat 网络模型是 owner-authoritative。只有 owner 的 synced variable 写入会被序列化并发送给远端。

### Exceptions
- 如果通过 `Networking.SetOwner()` 转移 ownership 后，新 owner 可以写入
- 某些"无 owner"对象（如 Scene 层对象）的规则不同

---

## RULE-NW-02: Manual Sync Requires RequestSerialization

### Rule
使用 `BehaviourSyncMode.Manual` 时，修改 `[UdonSynced]` 变量后必须显式调用 `RequestSerialization()`。

### Reason
Manual Sync 模式下，运行时不会自动序列化。不调用 `RequestSerialization()` 的修改永远不会发送给远端。

### Code
```csharp
[UdonSynced] private int _state;
private void ChangeState(int newState) {
    _state = newState;
    RequestSerialization();  // ← 必须
}
```

---

## RULE-NW-03: Late Joiner State Requires Synced Variables

### Rule
晚加入玩家需要恢复的状态必须使用 `[UdonSynced]` 变量持久同步，不能仅靠 Network Event。

### Reason
- `[UdonSynced]` 变量会在玩家加入时自动被最新值初始化
- Network Event 只发送给当前在房间的玩家，late joiner 收不到
- `OnDeserialization()` 在 late joiner 加入时会被调用，可用于恢复本地表现

### Pattern
参见 `patterns/late-joiner-state-restore.md`

---

## RULE-NW-04: Network Event Is For Transient Effects

### Rule
Network Event 适合一次性声音、粒子、动画触发，不适合作为持久状态来源。

### Reason
- Network Event 是 fire-and-forget
- Late joiner 收不到已经发送过的 Network Event
- 无法从 Network Event 恢复状态

### 适用
- 音效播放
- 粒子爆发
- 一次性动画（如开门动画触发）
- 网络聊天消息（不需要 late joiner 看到历史）

### 不适用
- 门的开/关状态
- 灯光状态
- 游戏分数
- 任何 late joiner 需要看到的状态

---

## RULE-NW-05: Only Sync Necessary State

### Rule
只同步必要状态。可本地计算的表现数据不要同步。

### Reason
每字节同步数据都消耗网络带宽和序列化时间。

### Examples

同步（必要）:
- 门的状态 (0=关, 1=开, 2=动画中)
- 游戏分数
- 对象的 owner ID

不同步（可本地派生）:
- 门的位置（根据状态 ID 本地插值）
- UI 颜色（根据状态选择本地素材）
- 音效播放（Network Event 触发，本地 AudioSource 播放）

---

## RULE-NW-06: Continuous Sync Is For Truly Continuous Data

### Rule
`BehaviourSyncMode.Continuous` 只用于真正需要连续变化的数据（如玩家位置、旋转）。离散状态用 Manual Sync。

### Reason
Continuous Sync 每次序列化都会发送所有 synced variables，即使没有变化。对离散状态是巨大的带宽浪费。

---

## RULE-NW-07: Sync Type Decision Tree

```text
状态是 late joiner 需要的吗？
├── 否 → Network Event
│   例: 一次性音效、粒子、聊天消息
│
└── 是 → 状态是连续变化的吗？
    ├── 是 → Continuous Sync
    │   例: 玩家位置、抓取物体位姿
    │
    └── 否 → 状态变化频率如何？
        ├── 低频（<1Hz）→ Manual Sync + RequestSerialization
        │   例: 门状态、开关、UI 状态
        │
        └── 中频（1-10Hz）→ 评估是否需要降频
            例: 需要节流的分数更新
```

---

## RULE-NW-08: Ownership Transfer Is Explicit

### Rule
Ownership transfer 需要显式调用 `Networking.SetOwner(Networking.LocalPlayer, targetObject)`。

### Reason
Udon 不会自动转移 ownership。非 owner 要写入 synced variable 必须先通过 ownership transfer 或请求 owner 代为写入。

---

## RULE-NW-09: OnDeserialization For Remote State Update

### Rule
远端玩家应通过 `OnDeserialization()` 接收 synced variable 更新，并在其中更新本地表现。

### Reason
`OnDeserialization()` 在收到远端 synced variable 更新时被调用。配合 `FieldChangeCallback` 可以只响应实际变化的字段。

### Pattern
```csharp
[UdonSynced, FieldChangeCallback(nameof(State))]
private int _state;
public int State {
    get => _state;
    set {
        _state = value;
        UpdateVisuals();  // 本地和远端都会执行
    }
}
```

---

## RULE-NW-10: SetOwner Is Locally Immediate (SDK 3.7.1+)

### Rule
`Networking.SetOwner()` 在调用客户端上**本地立即生效**。调用返回后 `Networking.IsOwner(gameObject)` 立即返回 `true`，`OnOwnershipTransferred` 在 `SetOwner` 调用栈内同步触发。

### Reason
SDK 3.7.1+ 中 ownership transfer 是本地同步的。两个客户端同时调用 `SetOwner` 时，双方都"本地成功"，但网络按到达顺序裁决 durable owner。失败方的写入会被胜方的序列化覆盖。

### Impact
- 在 `SetOwner` 后可以立即写入 `[UdonSynced]` 并调用 `RequestSerialization()`
- 不需要等待 callback 确认 ownership
- 并发 SetOwner 的"失败方覆盖"是网络属性，不应在客户端做仲裁

---

## RULE-NW-11: Separate Continuous and Manual Sync

### Rule
Continuous Sync 和 Manual Sync 的关切必须在**不同的 UdonBehaviour** 中处理。不要在一个 Behaviour 上混用。

### Reason
`BehaviourSyncMode` 是单一 enum 值。Continuous mode 中 `RequestSerialization()` 是冗余调用；Manual mode 中没有自动同步。混用导致带宽浪费或功能缺失。

### Pattern
```text
GameObject
├── Behaviour A: Continuous Sync (位置/旋转)
└── Behaviour B: Manual Sync (分数/状态)
```

---

## RULE-NW-12: Non-Owner Write Is Silently Reverted

### Rule
非 owner 对 `[UdonSynced]` 变量的写入是**纯本地**的。下一次从真正的 owner 反序列化时，写入会被静默覆盖。没有错误、没有警告。

### Fix
所有 synced variable 写入前必须：
```csharp
if (!Networking.IsOwner(gameObject))
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
// 此时 IsOwner = true（本地立即），安全写入
_value = newValue;
RequestSerialization();
```

---

## RULE-NW-13: String Budget In Continuous Sync

### Rule
Continuous Sync 的 synced `string` 受约 200 字节共享预算限制。UTF-16 编码每字符 2 字节，超过约 100 字符会被静默截断。

### Fix
- Continuous Sync 中保持 synced string 极短（< 40 字符安全余量）
- 长字符串用 Manual Sync（上限约 280KB）
- 在赋值前检查长度并截断

---

## RULE-NW-14: Networking.IsClogged Check

### Rule
调用 `RequestSerialization()` 前检查 `Networking.IsClogged`，尤其是在中高频同步场景。

### Reason
VRChat Udon 网络预算约 11KB/s。网络拥塞时 `RequestSerialization()` 可能静默丢弃。`IsClogged` 允许检测拥塞并延迟重试。

### Pattern
```csharp
if (Networking.IsClogged) {
    SendCustomEventDelayedSeconds(nameof(_RetrySync), 1.0f);
    return;
}
RequestSerialization();
```

---

## RULE-NW-15: NetworkCallable (SDK 3.8.1+)

### Rule
SDK 3.8.1+ 支持 `[NetworkCallable]` 属性的参数化网络事件，最多 8 个参数。低于 3.8.1 编译通过但运行时静默忽略。

### Constraints
- 方法必须 `public`，不能是 `static`/`virtual`/`override`
- 参数必须是 syncable 类型
- 默认速率限制 5 calls/sec/event（可配置到 100）
- 不替代 `[UdonSynced]` 的持久状态

### Pattern
```csharp
[NetworkCallable]
public void TakeDamage(int damage, int attackerId) {
    health -= damage;
}
SendCustomNetworkEvent(NetworkEventTarget.All, nameof(TakeDamage), dmg, atkId);
```

---

## RULE-NW-16: Sync Data Budget

### Rule
目标是每个 UdonBehaviour < 50 bytes synced data。整个 world 总共 < 100 bytes。

### Reference
- Voting system: `int + int + bool` = 9 bytes
- Shooting manager: `bool + bool + string + int` = ~38 bytes
- Global counter: 0 synced variables (Network Event only)

### Sync Minimization 6 Principles
1. 不同步可派生值（elapsed time = current time - syncedStartTime）
2. 使用最小类型（0-255 → `byte`, 0-65535 → `ushort`）
3. Bit-pack bool 组（8 flags = 1 int 4B vs 8 bool 8B）
4. 一次性效果用 SendCustomNetworkEvent（无需 synced variable）
5. 同步状态，不同步动作（sync gamePhase, event for startGame）
6. 单一 source of truth（只有 owner 修改 → 所有客户端 OnDeserialization 更新显示）

---

## RULE-NW-17: uGUI Callback Anti-Pattern

### Rule
uGUI button OnClick **在所有客户端本地触发**。用 `IsOwner` 守卫会阻止非 owner 的按钮响应。

### Fix
```csharp
// ❌ 错误: 非 owner 点击无反应
public void OnButtonClicked() {
    if (!Networking.IsOwner(gameObject)) return; // 按钮对非 owner 无响应!
}

// ✅ 方案 A: 委托给 owner（低频操作）
public void OnButtonClicked() {
    SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(OwnerAction));
}

// ✅ 方案 B: 获取 ownership 后执行（即时响应）
public void OnButtonClicked() {
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
    // 写入 synced variable + RequestSerialization
}
```

---

## RULE-NW-18: `_` 前缀方法防止网络事件调用

### Rule
以 `_` 开头的 public 方法不会被 `SendCustomNetworkEvent` 调用（VRChat 2020.4.4+）。用于标记仅限本地使用的 public API。

### Pattern
```csharp
// 可被网络事件调用
public void SyncMethod() { }

// 不会被网络事件调用（仅本地 public API）
public void _LocalAPI() { }
```

---

## RULE-NW-19: 禁止 Collision Ownership Transfer

### Rule
不要在 Collision 事件中执行 `Networking.SetOwner()`。历史上存在 bug，会导致所有权转移风暴并卡顿所有玩家。

### Fix
VRC_Object Sync 脚本自动处理所有权转移，无需手动在 Collision 中实现。Pickup 事件中 ownership 也自动转移（如果是网络化的 Pickup）。

---

## RULE-NW-20: 同步变量与网络事件的顺序问题

### Rule
同步变量更新比网络事件慢。**设置同步变量后立即 `SendCustomNetworkEvent` 可能导致远端收到事件时变量尚未同步**。

### Fix
- 不要在 `RequestSerialization()` 后立即发 Network Event
- 如果需要远端在变量更新后执行逻辑，使用 `OnDeserialization()` 或 `FieldChangeCallback` 触发
- 或者在 Network Event 中不依赖于刚更新的 synced variable 值

---

## RULE-NW-21: OnOwnershipRequest 可拒绝所有权转移

### Rule
`OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner)` 返回 `bool`。返回 `true` 接受，`false` 拒绝。用于在关键操作期间（turn-based 逻辑、事务中）保护状态。

---

## RULE-NW-22: Network Event 过多导致 Death Runs

### Rule
网络事件过多会导致 "Death Runs"——数据丢失。使用 synced variable + RequestSerialization 替代大量频繁的网络事件。
