---
title: Object Ownership 对象所有权
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - networking
  - udon
  - ownership

aliases:
  - "所有权"

related:
  - world/udon/networking/index.md
  - world/udon/networking/events.md
  - world/udon/networking/variables.md
  - world/udon/networking/network-components.md
  - api/networking.md
  - patterns/owner-authoritative-interaction.md

source: VRChat 官方 Creator Docs (Object Ownership)
source_type: official
version: 1.0
last_review: 2026-06-15
confidence: High
---
# Object Ownership 对象所有权

> SDK Version: 3.x
---

## 简介

在 VRChat 中,**每个网络化的 GameObject 都有一个 Owner**。所有权决定 **哪个玩家可以修改该对象的网络同步数据**。理解并管理好所有权,是构建多人世界的基础。

---

## 所有权核心规则

| 规则 | 说明 |
|------|------|
| **默认 Owner** | **第一个加入实例的玩家** 拥有所有网络化对象 |
| **可转移** | 通过 `Networking.SetOwner()` 在玩家间动态转移 |
| **修改权限** | **只有 Owner 可以修改** `[UdonSynced]` 变量 |
| **自动转移** | Owner 离开实例时,VRChat 自动分配新 Owner |
| **Master 与 Owner** | Master 是 **所有未分配 Owner 对象** 的默认持有者 |

---

## 转移所有权 API

```csharp
Networking.SetOwner(VRCPlayerApi player, GameObject obj);
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `player` | `VRCPlayerApi` | 新 Owner(必须是当前在实例中的玩家) |
| `obj` | `GameObject` | 目标对象 |

### 关键约束

| 约束 | 说明 |
|------|------|
| **当前 Owner 才能转移** | 非 Owner 调用 `SetOwner` **无效果**(不报错) |
| **同步是异步的** | Transfer 不是即时的,需网络确认 |
| **新 Owner 收到事件** | `OnOwnershipTransferred` 在新 Owner 侧触发 |
| **旧 Owner 也收到事件** | 所有玩家都收到 `OnOwnershipTransferred` |
| **请求者收到 `OnOwnershipRequest`** | 在转移前收到(可拒绝) |

### 典型代码

```csharp
public override void Interact() {
    // 把当前 GameObject 所有权转给本地玩家
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
}
```

---

## 所有权事件(2 个核心)

### 1. `OnOwnershipRequest`

> 在所有权转移 **前** 触发,可决定 **批准或拒绝** 请求。

```csharp
public override bool OnOwnershipRequest(VRCPlayerApi requestingPlayer, VRCPlayerApi newOwner) {
    // 业务规则:只允许特定条件下的转移
    if (CanTransferTo(requestingPlayer)) {
        return true;  // 批准
    }
    return false;    // 拒绝
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `requestingPlayer` | `VRCPlayerApi` | 发起请求的玩家 |
| `newOwner` | `VRCPlayerApi` | 期望成为新 Owner 的玩家 |
| 返回值 | `bool` | `true` = 批准,`false` = 拒绝 |

### 2. `OnOwnershipTransferred`

> 所有权 **转移完成后** 触发,所有玩家都收到。

```csharp
public override void OnOwnershipTransferred(VRCPlayerApi newOwner) {
    Debug.Log($"New owner: {newOwner.displayName}");
    // 更新 UI、特效、权限逻辑
    UpdateOwnerUI(newOwner);
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `newOwner` | `VRCPlayerApi` | 新的 Owner |

---

## 完整所有权转移流程

```
Requester 玩家                   Owner 玩家                 Server
    │                              │                        │
    ├─ Interact()                  │                        │
    │   └─ SetOwner(Self, obj) ────┼───► 请求转移 ────────►│
    │                              │                        │
    │                              │                        │
    │                              │◄── 转发请求 ───────────┤
    │                              │                        │
    │                              ├─ OnOwnershipRequest()  │
    │                              │  ├─ 检查业务规则       │
    │                              │  └─ return true/false  │
    │                              │                        │
    │                              │── 批准/拒绝 ──────────►│
    │                              │                        │
    │◄─── 转移结果通知 ────────────┼────────────────────────┤
    │                              │                        │
    ├─ OnOwnershipTransferred()    ├─ OnOwnershipTransferred()
    │   (新 Owner 也是 Requester)  │  (旧 Owner 也收到)
    │                              │                        │
    │  Requester 成为新 Owner      │  旧 Owner 失去权限     │
```

---

## Instance Master 与 Instance Owner

### 两个不同概念

| 概念 | 说明 | API |
|------|------|-----|
| **Instance Master** | 实例中拥有未分配网络对象的玩家(可变化) | `Networking.IsMaster`、`Networking.Master` |
| **Instance Owner** | 创建实例的玩家(有审核权限,永不变) | `Networking.IsInstanceOwner`、`Networking.InstanceOwner` |

### Instance Master 规则

> **关键**:**Master 可能在任何时候改变**,不能依赖 Master 做权限判断。

| 规则 | 说明 |
|------|------|
| 第一个加入的玩家 | 初始 Master |
| Master 离开 | 自动转移给另一个玩家(VRChat 内部决策) |
| Master 是 Android 设备且挂起太久 | 可能被转移 |
| Master 选择标准 | 平台、网络条件等(VRChat 服务端决定) |

> ⚠️ **唯一保证**:Master 离开时会转移。除此之外,任何其他观察到的行为 **都可能在未来改变**。

### Instance Owner 规则

| 规则 | 说明 |
|------|------|
| **永不变化** | 创建实例的玩家永远是 Instance Owner |
| **跨平台有效** | Invite/Invite+/Friends/Friends+ 实例 |
| **Group 实例** | `IsInstanceOwner` **始终返回 `false`** |
| **Build & Test 模式** | SDK 测试模式下 `IsInstanceOwner` 始终 `false` |
| **Owner 离开** | `InstanceOwner` 返回 `null`(再次加入恢复) |
| **特殊权限** | Instance Owner 有 **审核权限**(kick/ban) |

### 权限判断选择

```csharp
// ❌ 错误:用 Master 做权限
if (Networking.IsMaster) {
    // 让 Master 拥有管理员权限
}

// ✅ 正确:用 Instance Owner 或自定义权限系统
if (Networking.IsInstanceOwner) {
    // 拥有真正审核权限
}

// ✅ 更好:实现自己的 Moderation 系统
if (isPlayerInAdminList(player)) {
    // 管理员权限
}
```

---

## Best Practices 最佳实践

| 实践 | 说明 |
|------|------|
| **不要依赖特定玩家成为 Master** | 选择标准是 VRChat 内部的 |
| **修改 synced 变量前检查/请求 owner** | 避免失败写入 |
| **处理玩家断线和 Late Joiner** | Owner 离开会转移,Late Joiner 看到的是当前 Owner |
| **避免依赖 Instance Master** | 用 ownership 检查或 `IsInstanceOwner` |
| **最小化所有权转移** | 频繁转移引入延迟和潜在 desync |
| **`OnOwnershipRequest` 双方执行** | 请求者和当前 Owner 都运行该逻辑,可能 desync |

---

## 所有权与同步变量

### 写入权限

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class ScoreBoard : UdonSharpBehaviour {
    [UdonSynced] private int _score;
    
    public void AddScore() {
        if (!Networking.IsOwner(gameObject)) {
            // 非 Owner:要么 return,要么请求所有权
            return;
        }
        _score++;
        RequestSerialization();
    }
}
```

### 修改顺序(关键!)

```csharp
// ❌ 错误顺序
public void OnPickup() {
    Networking.SetOwner(player, gameObject);
    _value = newValue;              // 这一行可能仍由旧 Owner 执行
    RequestSerialization();
}

// ✅ 正确顺序
public void OnPickup() {
    _value = newValue;              // 先修改本地
    Networking.SetOwner(player, gameObject);
    RequestSerialization();          // 然后请求序列化
}
```

> **解释**:Ownership Transfer 是异步的。即使先调用 `SetOwner`,后续的同步操作可能仍由旧 Owner 执行。最佳实践是 **先完成本地修改,再触发 Transfer**。

---

## 所有权与 Object Pool

`VRC Object Pool` 的 Owner 拥有 spawn/return 权限:

```csharp
// Pool 内的对象由 Pool Owner 控制
// 非 Owner 不能 spawn,只能观察
```

> 详见 `network-components.md` 中的 VRCObjectPool。

---

## 所有权与 VRCPickup

`VRCPickup` 内部自动处理所有权:

| 行为 | 机制 |
|------|------|
| 玩家拾取物体 | 所有权自动转移给该玩家 |
| 玩家放下/掉落 | 所有权保留给该玩家(直到离开) |
| 玩家离开 | VRChat 重新分配 |

> 详见 `network-components.md` 中的 VRCPickup。

---

## 常见所有权反模式

### 反模式 1:每个交互都转移所有权

```csharp
// ❌ 不好:频繁转移
public override void Interact() {
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
    _state = !_state;
    RequestSerialization();
}

// ✅ 更好:使用 Owner 模式,所有交互都由 Owner 处理
public override void Interact() {
    SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(RequestToggle));
}
```

### 反模式 2:用 Master 做权限

```csharp
// ❌ Master 不可靠
if (Networking.IsMaster) {
    BanPlayer(target);
}

// ✅ 用 InstanceOwner 或自定义权限
if (Networking.IsInstanceOwner || IsAdmin(player)) {
    BanPlayer(target);
}
```

### 反模式 3:同步变量写入前未检查 Owner

```csharp
// ❌ 非 Owner 写入被静默忽略
public void ModifyState(int newValue) {
    _state = newValue;          // 非 Owner 写入无效
    RequestSerialization();     // Request 也会失败
}

// ✅ 加上 Owner 检查
public void ModifyState(int newValue) {
    if (!Networking.IsOwner(gameObject)) {
        Debug.LogWarning("Not owner, cannot modify");
        return;
    }
    _state = newValue;
    RequestSerialization();
}
```

---

## 实例 Master 转移事件

> `OnMasterTransferred` 在 Master 变化时触发(因旧 Master 离开):

```csharp
public override void OnMasterTransferred(VRCPlayerApi newMaster) {
    // 第一个加入的玩家:OnPlayerJoined 之后会触发
    // 旧 Master 离开:所有玩家都收到
    Debug.Log($"New master: {newMaster.displayName}");
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `newMaster` | `VRCPlayerApi` | 新 Master,保证非 null |

> **触发顺序**:Master 转移 → `OnPlayerLeft` (旧 Master) → `OnMasterTransferred`

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| 频繁转移所有权 | 🟠 High | 引入延迟,可能 desync |
| 用 Master 做权限 | 🔴 Critical | Master 不可预测变化 |
| 同步变量写入未检查 Owner | 🟠 High | 静默失败 |
| 顺序错(SetOwner 后再写) | 🟡 Medium | 可能由旧 Owner 写入 |
| `OnOwnershipRequest` 双方执行 | 🟡 Medium | 请求者侧与 Owner 侧逻辑分歧导致 desync |
| Owner 离开时未处理 | 🟠 High | 需要在 `OnPlayerLeft` 中处理 |
| 依赖 Master 不会变 | 🔴 Critical | 不可靠 |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/events.md` | SendCustomNetworkEvent(Owner 模式) |
| `memory/world/udon/networking/variables.md` | synced 变量写入权限 |
| `memory/world/udon/networking/network-components.md` | VRCPickup 自动所有权 |
| `memory/api/networking.md` | API 速查 |
| `memory/patterns/owner-authoritative-interaction.md` | Owner 模式实现 |
