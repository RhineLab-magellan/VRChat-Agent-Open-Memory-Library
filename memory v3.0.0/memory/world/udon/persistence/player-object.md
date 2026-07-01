---
title: PlayerObject 实战
category: world
subcategory: udon/persistence
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - storage
  - player-object
  - gameplay-object
aliases:
  - PlayerObject 教程
  - PlayerObject API
  - 玩家对象
  - 持久化游戏对象
related:
  - ../../../api/persistence.md
  - ../index.md
  - player-data.md
  - serialization.md
  - limits-and-quirks.md
  - patterns/persistent-pen.md
  - ../networking/ownership.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/persistence/player-object/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# PlayerObject 实战

> SDK Version: 3.7+(核心) / 3.10+(Storage Information API)
> 官方文档:https://creators.vrchat.com/worlds/udon/persistence/player-object/
> 命名空间:`VRC.SDKBase` + `UnityEngine`

---

## 概述

**PlayerObject** 是 VRChat **自动为每个玩家实例化** 的 GameObject。可挂载 Udon 脚本,可通过 `[UdonSynced]` 同步数据,可加 `VRCEnablePersistence` 让数据 **跨会话持久化**。

> **核心特性**:
> - 加入玩家 → 自动 spawn 一份
> - 离开玩家 → 自动 despawn
> - 玩家 **永远拥有** 该对象(不能转移)
> - 可作为 per-player 对象池、健康条、武器、笔触等

### PlayerObject 三大用途

1. **持久化数据存储**(加 `VRCEnablePersistence`)
2. **per-player 对象池**(血条、伤害计算区域、UI 容器)
3. **不可偷取的玩家物品**(工具、武器 - 所有权不可转移)

---

## 设置(Setup)

### 5 步创建 PlayerObject

1. **创建 GameObject** Prefab(场景中放一个即可,VRChat 会自动 disable 模板)
2. **添加 `VRCPlayerObject` 组件** - 标识为 PlayerObject 模板
3. **(可选)添加 `UdonBehaviour`** - 挂 Udon 脚本逻辑
4. **(可选)添加 `VRCEnablePersistence`** - 启用持久化
5. **添加 `[UdonSynced]` 字段** - 同步的数据字段

### 完整 Prefab 结构示例

```
SimplePenSystem (GameObject)
├── VRCPlayerObject          (组件)
├── VRCEnablePersistence    (组件)
└── UdonBehaviour            (组件 - 你的脚本)
    ├── [UdonSynced] int _lineCount
    ├── [UdonSynced] Vector3[] _linePoints
    └── [UdonSynced] Color[] _lineColors
```

### 关键组件职责

| 组件 | 作用 |
|------|------|
| `VRCPlayerObject` | 标识该 GameObject 为 PlayerObject 模板 |
| `VRCEnablePersistence` | 启用 UdonSynced 字段的持久化(跨会话保存) |
| `UdonBehaviour` | Udon 脚本 + `[UdonSynced]` 字段定义 |

> **没有 `VRCEnablePersistence`** → 仍然自动实例化,但 `[UdonSynced]` 字段 **不会跨会话保留**(只在本实例有效)

---

## Ownership(所有权模型)

> 🔑 **PlayerObject 的所有权是绑定性的,玩家永远拥有自己的 PlayerObject**

### 关键规则

| 规则 | 含义 |
|------|------|
| 玩家拥有 PlayerObject | 自动 owner,**不能转移** |
| 同一 PlayerObject 内所有子物体 | 全部属于该玩家 |
| `Networking.SetOwner()` 不可用 | 调用会静默失败 |
| 玩家离开 → PlayerObject 销毁 | 数据保留在服务器 |
| 玩家重新加入 → PlayerObject 重新 spawn | 数据从服务器恢复 |

### 设计意义

```text
✅ 适合:工具、武器、玩家专属 UI
   - 玩家永远拥有自己的笔,不被偷
   - 血条永远跟随玩家
   
❌ 不适合:需要转移所有权的对象(球、卡片)
   - 用 VRCObjectSync 替代
```

---

## 模板(Template)与实例(Instance)

> **模板**:场景中那个原始的 GameObject(VRC 自动 disable 但保留)
> **实例**:VRChat 为每个玩家生成的副本

### 模板规则

| 规则 | 含义 |
|------|------|
| 模板自动 disabled | 不要启用它 |
| 不要销毁/修改模板 | 会导致错误或异常行为 |
| 场景其他对象不能引用模板 | 必须引用实例 |
| 模板可以引用场景对象 | 跨玩家共享引用 OK |

### 查找 PlayerObject 实例(关键 API)

```csharp
using VRC.SDKBase;
using UnityEngine;

// 方法 1:获取玩家的所有 PlayerObject
GameObject[] objects = Networking.GetPlayerObjects(player);

// 方法 2:从模板引用翻译到玩家实例
public Transform referenceChildTransform;  // 在 Inspector 拖入模板的子物体
public void FindReference(VRCPlayerApi targetPlayer) {
    Component foundComponent = Networking.FindComponentInPlayerObjects(targetPlayer, referenceChildTransform);
    // foundComponent 就是 targetPlayer 那个 PlayerObject 对应子物体的引用
}

// 完整实战:查找特定脚本
public MyPenScript FindMyPen(VRCPlayerApi player) {
    GameObject[] objects = Networking.GetPlayerObjects(player);
    for (int i = 0; i < objects.Length; i++) {
        if (!Utilities.IsValid(objects[i])) continue;
        MyPenScript found = objects[i].GetComponentInChildren<MyPenScript>();
        if (Utilities.IsValid(found)) return found;
    }
    return null;
}
```

> **为什么需要 `FindComponentInPlayerObjects`**:VRChat 不会自动同步模板到实例的引用。你在 Inspector 拖入的是模板引用,必须翻译到具体玩家的实例。

---

## 持久化(Loading Persistent User Data)

### 3 个持久化条件(全部满足才持久化)

1. GameObject(模板或子物体)有 `UdonBehaviour`
2. `UdonBehaviour` 有 `[UdonSynced]` 变量
3. 该 `UdonBehaviour` 的 GameObject 也有 `VRCEnablePersistence` 组件

> 任何一条不满足 → 数据不会跨会话保留

### 时序警告(必读)

> 🔴 **不要在 `Start` 或 `OnDeserialization` 中读取 PlayerObject 的持久化数据**

```csharp
// ❌ 错误:数据可能未加载完
public override void Start() {
    Debug.Log(_lineCount);  // 可能是默认值 0,不是持久化值
}

// ✅ 正确:等待 OnPlayerRestored
private bool _dataReady = false;

public override void OnPlayerRestored(VRCPlayerApi player) {
    // OnPlayerRestored 在每个玩家(不只是本地)的 PlayerObject 上触发
    // 必须用 if (!Networking.IsOwner(...)) return; 守卫
    
    if (!Networking.IsOwner(gameObject)) return;
    _dataReady = true;
    // 此时可以安全读取 _lineCount(已经是持久化值)
    RenderAllLines();
}
```

> **OnPlayerRestored 触发条件**:VRChat 玩家的 **全部** 持久化数据加载完成。在每个相关 PlayerObject 上都会触发(不只本地玩家的)。

---

## 4 个 PlayerObject 事件

| 事件 | 触发时机 | 用途 |
|------|---------|------|
| `OnPlayerRestored(VRCPlayerApi player)` | 玩家数据加载完成 | **核心** - 初始化/恢复数据 |
| `OnPersistenceUsageUpdated(VRCPlayerApi)` | `RequestStorageUsageUpdate` 后 | 查询存储用量 |
| `OnPlayerObjectStorageWarning(VRCPlayerApi)` | PlayerObject 接近上限 | 提示用户清理 |
| `OnPlayerObjectStorageExceeded(VRCPlayerApi)` | PlayerObject 超出限制 | 数据未保存 |

---

## 6 个方法(SDK 3.10+)

```csharp
using VRC.SDKBase;

// 查询 API
GameObject[] objects = Networking.GetPlayerObjects(VRCPlayerApi player);
Component comp = Networking.FindComponentInPlayerObjects(VRCPlayerApi player, Component templateRef);

// Storage Information API(SDK 3.10+)
int limit = Networking.GetPlayerObjectStorageLimit();      // 100 * 1024
int used = Networking.GetPlayerObjectStorageUsage(player); // 当前用量(可能过期)
Networking.RequestStorageUsageUpdate();                    // 异步刷新

// VRCPlayerApi 上的快捷方法
GameObject[] objs = player.GetPlayerObjects();
```

---

## 完整实战模板(持久画笔骨架)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class SimplePenSystem : UdonSharpBehaviour {
    [UdonSynced] public int _lineCount = 0;
    [UdonSynced] public Vector3[] _linePoints = new Vector3[100];
    [UdonSynced] public Color[] _lineColors = new Color[100];
    [UdonSynced] public int[] _linePointCount = new int[20];
    
    private bool _dataReady = false;
    
    public override void OnPlayerRestored(VRCPlayerApi player) {
        // 关键:OnPlayerRestored 在每个玩家(不只本地)的 PlayerObject 上触发
        if (!Networking.IsOwner(gameObject)) return;
        _dataReady = true;
        RenderAllLines();
    }
    
    // 本地玩家添加一条线
    public void AddLine(Vector3[] points, Color color) {
        if (!_dataReady) return;
        // 修改 [UdonSynced] 字段
        // ...
        RequestSerialization();  // Manual 同步
    }
    
    public override void OnDeserialization() {
        if (!_dataReady) return;
        RenderAllLines();  // 同步后重建可视化
    }
    
    private void RenderAllLines() {
        // 重建 LineRenderer 等
    }
}
```

---

## PlayerObject 跨设备同步(不可保存的"会话内"数据)

> **关键理解**:PlayerObject 数据分两层

| 层级 | 生命周期 | 是否跨设备 |
|------|---------|-----------|
| `[UdonSynced]` 字段 | 实例内 + 跨会话(需 VRCEnablePersistence) | ✅ |
| 实例本身 | 实例内(玩家离开销毁) | ❌ |

> **含义**:如果你的 PlayerObject 是"画笔"这种 per-player 工具,数据保存在服务器的 [UdonSynced] 字段里。玩家在 PC 上画线 → Quest 上 rejoin → 重新 spawn PlayerObject → [UdonSynced] 字段自动从服务器加载 → 渲染相同线条。

---

## 4 个常见陷阱

| 陷阱 | 症状 | 修复 |
|------|------|------|
| 没加 `VRCEnablePersistence` | 字段跨会话丢失 | 同步字段必须加该组件 |
| `Start` 读取字段 | 读到默认值(数据未加载) | 改用 `OnPlayerRestored` 守卫 |
| 多个玩家共享一个 PlayerObject 引用 | 找到错的玩家实例 | 用 `Networking.FindComponentInPlayerObjects` 翻译 |
| 修改 disabled 模板 | 玩家实例异常 | 不要动模板(VRChat 已自动 disable) |

---

## 关键 API vs 限制速查

| 维度 | 限制 |
|------|------|
| 配额 | 100 KB / 玩家 / World(**独立于** PlayerData) |
| 原始数据 | ~300 KB(高度可压缩时) |
| 所有权 | 玩家拥有,**不能转移** |
| 实例化时机 | 加入实例时 |
| 销毁时机 | 离开实例时 |
| 模板修改 | ❌ 不要修改 disabled 模板 |
| Late Joiner | 自动获取最新 [UdonSynced] 值 |

---

## 实战示例(本目录内)

- [patterns/persistent-pen.md](./patterns/persistent-pen.md) - 持久画笔(经典 PlayerObject 案例)

---

## 相关知识库

- `memory/api/persistence.md` - 完整 API 速查
- `memory/world/udon/networking/ownership.md` - 所有权机制详解
- `memory/world/udon/networking/variables.md` - UdonSynced 字段类型
- `memory/world/examples/persistence/health-bar.md` - 血条 Example
- `memory/world/examples/persistence/position-sync.md` - 位置同步 Example
- `memory/world/examples/persistence/simple-rpg.md` - RPG Example
- `memory/patterns/owner-authoritative-interaction.md` - Owner Authority 模式
