---
title: VRC Object Sync ⭐
category: world
subcategory: scene-components

knowledge_level: applied
status: active

tags:
  - world
  - sync
  - ownership

aliases:
  - "同步"

related:
  - api/networking.md
  - api/pickups.md
  - patterns/manual-sync-state.md
  - patterns/owner-authoritative-interaction.md
  - api/events-reference.md
  - vrc-scenedescriptor.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# VRC Object Sync ⭐

> 物理对象位置/旋转同步组件(**核心组件**)
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_objectsync/
> 官方类名: `VRCObjectSync`
> 最后更新: 2026-06-15
> 最新更新日期: 2025-03-07

---

## 概述

`VRCObjectSync` 同步 GameObject 的 Transform 到实例内的所有玩家。它同步:
- **position** (位置)
- **rotation** (旋转)
- **kinematic state** (运动学状态)
- **gravity state** (重力状态)

> ⭐ **核心组件**: VRChat 中最常用的网络同步组件之一,用于物理交互对象(球、箱子、可拾取物等)。

---

## Inspector 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| **Allow Collision Ownership Transfer** | Bool | true | 如果勾选,与另一玩家拥有的物体碰撞时自动转移所有权 |
| **Force Kinematic On Remote** | Bool | true | 如果勾选,非拥有者的 Rigidbody 强制为 kinematic 模式 |

> **FACT**: 当 kinematic 状态为 ON 时,Rigidbody 忽略力、碰撞和关节(由 VRCObjectSync 远程控制以避免物理冲突)。

---

## 运行时方法 (Methods)

| 方法 | 签名 | 说明 |
|------|------|------|
| `SetKinematic` | `void SetKinematic(bool value)` | 修改运动学状态(同步到所有玩家) |
| `SetGravity` | `void SetGravity(bool value)` | 修改重力状态(同步到所有玩家) |
| `FlagDiscontinuity` | `void FlagDiscontinuity()` | 触发时**传送物体** - 本帧的修改将应用无平滑过渡 |
| `TeleportTo` | `void TeleportTo(Transform targetLocation)` | 将物体移动到指定位置(自动调用 FlagDiscontinuity) |
| `Respawn` | `void Respawn()` | 将物体移回初始生成位置 |

> **FACT** (来自官方文档): `SetKinematic` 和 `SetGravity` 通常由 Rigidbody 自身处理,但在此处显式控制用于同步目的。

---

## 完整 U# 示例

### 基础引用与所有权获取

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(VRCObjectSync))]
public class PhysicsObject : UdonSharpBehaviour
{
    [SerializeField] private VRCObjectSync objectSync;
    [SerializeField] private float interactCooldown = 1f;
    
    private bool canInteract = true;
    
    public override void Interact()
    {
        if (!canInteract) return;
        
        // 1. 获取所有权
        if (!Networking.IsOwner(objectSync.gameObject))
        {
            Networking.SetOwner(Networking.LocalPlayer, objectSync.gameObject);
        }
        
        // 2. 执行操作(仅 Owner 端有意义)
        // ... 业务逻辑 ...
        
        canInteract = false;
        SendCustomEventDelayedSeconds(nameof(ResetCooldown), interactCooldown);
    }
    
    public void ResetCooldown() => canInteract = true;
}
```

### 传送物体

```csharp
public override void Interact()
{
    if (!Networking.IsOwner(objectSync.gameObject)) return;
    
    // 方式 1: 使用 TeleportTo
    Transform target = teleportTargets[currentIndex];
    objectSync.TeleportTo(target);
    
    // 方式 2: 手动传送 + FlagDiscontinuity
    transform.position = teleportTargets[currentIndex].position;
    objectSync.FlagDiscontinuity();  // 关键:告诉远程玩家不平滑
}
```

### 状态切换

```csharp
// 拾起时变为 kinematic(忽略物理)
public void OnPickup()
{
    if (!Networking.IsOwner(gameObject))
    {
        Networking.SetOwner(Networking.LocalPlayer, gameObject);
    }
    objectSync.SetKinematic(true);
    objectSync.SetGravity(false);
}

// 放下时恢复物理
public void OnDrop()
{
    if (!Networking.IsOwner(gameObject)) return;
    objectSync.SetKinematic(false);
    objectSync.SetGravity(true);
}
```

### 完整模式:基于生命周期的所有权管理

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

[RequireComponent(typeof(VRCObjectSync))]
public class SharedPhysicsBall : UdonSharpBehaviour
{
    [SerializeField] private VRCObjectSync objectSync;
    [SerializeField] private float force = 10f;
    
    public override void OnPlayerCollisionEnter(VRCPlayerApi player)
    {
        // 1. 自动获取所有权(如果开启了 Allow Collision Ownership Transfer)
        //    引擎层面已处理,这里只需执行业务
        if (!Networking.IsOwner(gameObject)) return;
        
        // 2. 给球一个远离玩家的力
        Vector3 direction = (transform.position - player.GetPosition()).normalized;
        GetComponent<Rigidbody>().AddForce(direction * force, ForceMode.Impulse);
    }
}
```

---

## ⭐ 与 Manual Sync 的核心区别

> **核心原则**:
> - **VRCObjectSync**: 物理对象(位置/旋转)**实时同步**,适合 Rigidbody 物体
> - **Manual Sync**: 业务逻辑同步(状态/数据),适合游戏状态机

| 维度 | VRCObjectSync | Manual Sync (UdonSynced) |
|------|--------------|--------------------------|
| **同步内容** | Transform + Kinematic + Gravity | 自定义 `[UdonSynced]` 字段 |
| **同步频率** | 物理引擎驱动(每帧) | 显式 `RequestSerialization()` 触发 |
| **带宽占用** | 较高(实时物理) | 较低(按需) |
| **适用场景** | 球、箱子、推车 | 门状态机、计分板、配置 |
| **Owner 决定** | 物理交互者(碰撞) | 业务逻辑决定 |
| **值类型** | 仅 Vector3/Quaternion | 任意白名单类型 |
| **插值** | 平滑插值(可 FlagDiscontinuity 关闭) | 无插值(由代码决定) |
| **创建方式** | 添加组件(零代码) | 写代码手动同步 |

### 选型决策树

```
需要同步什么?
├─ 物理 Transform (位置/旋转)
│  └─ 用 VRCObjectSync
│
└─ 业务状态 (boolean/int/枚举)
   └─ 用 Manual Sync (`[UdonSynced]`)
   
但业务状态需要"实时平滑"?
├─ 是 → Continuous Sync `[UdonSynced]` + 客户端插值(详见 [api/networking.md](../../../api/networking.md))
└─ 否 → Manual Sync
```

---

## 所有权转移的三种方式

### 1. 碰撞自动转移

启用 `Allow Collision Ownership Transfer`,VRCObjectSync 在 **物理碰撞** 时自动转移所有权给碰撞对方。

> **典型场景**: 玩家推球时,球自动属于该玩家,推的力作用于该玩家端

### 2. Trigger 转移

> ⚠️ 注意: VRCObjectSync **没有** Trigger 转移选项(这是 VRCPickup 的特性)
> Trigger 转移需要用 `VRCPickup` 组件(详见 [../../../api/pickups.md](../../../api/pickups.md))

### 3. 手动转移

```csharp
public void TakeOwnership()
{
    if (!Networking.IsOwner(gameObject))
    {
        Networking.SetOwner(Networking.LocalPlayer, gameObject);
    }
}
```

> **FACT**: 所有权变更时,所有玩家都会收到 `OnOwnershipTransferred` 事件:

```csharp
public override void OnOwnershipTransferred(VRCPlayerApi player)
{
    if (player.isLocal)
    {
        // 本地玩家刚获得所有权,可以开始操作
    }
    else
    {
        // 其他玩家获得所有权,本端变为只读
    }
}
```

---

## OnPlayerCollision* 事件

VRCObjectSync 默认会接收其他玩家的碰撞事件(前提是其他玩家有 Rigidbody 或 Collider):

```csharp
public override void OnPlayerCollisionEnter(VRCPlayerApi player) { }
public override void OnPlayerCollisionStay(VRCPlayerApi player) { }
public override void OnPlayerCollisionExit(VRCPlayerApi player) { }
```

> ⚠️ **重要**: 玩家自己的 Rigidbody/Collider 必须配置正确的 `Collision Detection Mode` (推荐 `Continuous Dynamic`)。否则碰撞事件不会触发。

---

## 性能考虑

### 带宽占用

- VRCObjectSync 持续同步,每个 ObjectSync 每秒消耗部分带宽
- **带宽预算**: 参见 [../../../api/networking.md](../../../api/networking.md) (~11KB/s 总带宽)
- 大量 ObjectSync(>20 个)会显著影响帧率

### 优化建议

1. **远距离禁用同步**: 玩家远离时禁用 VRCObjectSync(`objectSync.enabled = false`)
2. **减少 ObjectSync 数量**: 静态物体不要加 VRCObjectSync
3. **Kinematic 优化**: 不需要物理的物体保持 kinematic
4. **合理使用 Respawn**: 物体丢失后自动重生,避免永久消失

### 平台性能分级

| 平台 | 推荐 ObjectSync 数 |
|------|-------------------|
| **Quest 2/3** | < 10 个 |
| **PC (低端)** | < 30 个 |
| **PC (高端)** | < 50 个(仍需测试) |

---

## 错误模式与陷阱

### ❌ 错误 1: 在 Non-Owner 端修改 Transform

```csharp
// ❌ 错误:Non-Owner 端修改会被 VRCObjectSync 覆盖
public void MoveObject()
{
    transform.position += Vector3.up;  // 错误!
}
```

**修复**: 始终先获取所有权。

### ❌ 错误 2: 忘记 FlagDiscontinuity

```csharp
// ❌ 错误:传送后远端会有平滑过渡,看起来很怪
public void TeleportBadly()
{
    if (!Networking.IsOwner(gameObject)) return;
    transform.position = newPos;  // 远端会平滑插值,出现"追赶"效果
}

// ✅ 正确:使用 TeleportTo 或 FlagDiscontinuity
public void TeleportCorrectly()
{
    if (!Networking.IsOwner(gameObject)) return;
    objectSync.TeleportTo(targetTransform);
}
```

### ❌ 错误 3: Owner 在物理 Tick 中频繁切换

```csharp
// ❌ 错误:每帧都 SetOwner 会导致网络风暴
private void Update()
{
    if (someCondition)
    {
        Networking.SetOwner(Networking.LocalPlayer, gameObject);  // 网络爆炸!
    }
}
```

**修复**: 一次性获取所有权,持久持有直到主动放弃。

### ❌ 错误 4: 忽视 Force Kinematic On Remote

- **开启**: 非 Owner 端 Rigidbody 是 kinematic,不会发生物理冲突
- **关闭**: 非 Owner 端也会模拟物理,导致状态冲突和抖动
- **推荐**: 始终开启(默认值)

### ❌ 错误 5: 与 VRCPickup 同时使用造成所有权死锁

VRCObjectSync 适用于"被推的球",VRCPickup 适用于"被拿的物"。不要在同物体上同时使用。

---

## 跨页引用

- **Manual Sync 模式**: [../../../patterns/manual-sync-state.md](../../../patterns/manual-sync-state.md)
- **Owner 权威交互**: [../../../patterns/owner-authoritative-interaction.md](../../../patterns/owner-authoritative-interaction.md)
- **物理对象生命周期**: [../../../patterns/physics-object-lifecycle.md](../../../patterns/physics-object-lifecycle.md)
- **VRCPickup**: [../../../api/pickups.md](../../../api/pickups.md) (与 VRCObjectSync 互补)
- **Networking 完整 API**: [../../../api/networking.md](../../../api/networking.md)
- **事件参考**: [../../../api/events-reference.md](../../../api/events-reference.md)

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_objectsync/
- 关联组件: [VRC_SceneDescriptor](./vrc-scenedescriptor.md)
- 完整 Networking 文档: [../../../api/networking.md](../../../api/networking.md)
