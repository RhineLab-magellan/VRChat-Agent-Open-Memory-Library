---
title: VRC Enable Persistence
category: world
subcategory: scene-components

knowledge_level: applied
status: active

tags:
  - world
  - persistence
  - udonsharp

aliases:
  - "持久化"

related:
  - api/persistence.md
  - world/udon/data-containers/byte-and-bit-operations.md
  - api/networking.md
  - world/data-containers.md
  - api/pickups.md
  - vrc-scenedescriptor.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# VRC Enable Persistence

> 启用 PlayerObject 持久化组件
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_enablepersistence/
> 官方类名: `VRCEnablePersistence`
> 最后更新: 2026-06-15
> 最新更新日期: 2024-11-19

---

## 概述

`VRCEnablePersistence` 用于启用 **PlayerObject 持久化**。将该组件添加到 PlayerObject 后,**该 GameObject 及其子 UdonBehaviour 的所有 `[UdonSynced]` 变量会被持久化**。

> **FACT** (来自官方文档): 必须与 `VRCPlayerObject` 组件**在同 GameObject** 上才能工作。

---

## 核心概念

### 什么是 PlayerObject

> **FACT** (来自 VRChat 官方文档): **PlayerObject** 是为每个玩家实例化的 GameObject,包含玩家在该 World 中的私有数据。

**关键特征**:
- **每个玩家独立**: A 玩家的 PlayerObject 与 B 玩家**完全隔离**
- **跨实例持久化**: 玩家下次进入同一 World,PlayerObject 数据**自动恢复**
- **玩家离开时不销毁**: 数据保留到世界 / 玩家被清理

### 持久化 vs 同步

| 维度 | `[UdonSynced]` 同步 | `VRCEnablePersistence` 持久化 |
|------|----------------------|------------------------------|
| **作用** | 网络同步(本实例内) | 跨实例存储(玩家数据) |
| **数据保留** | 玩家离开即清除 | 玩家离开仍保留 |
| **数据共享** | 实例内所有玩家可见 | 仅该玩家可见 |
| **存储位置** | VRChat 服务器(内存) | VRChat 服务器(磁盘) |
| **数据容量** | 取决于 UdonSynced 字段 | **100 KB / 玩家 / World**(压缩后) |

---

## 必备依赖

> **FACT** (来自官方文档): 必须在同一 GameObject 上有 `VRCPlayerObject` 组件。

**完整组件列表** (同一 GameObject):
1. **`VRCPlayerObject`** - 标记此 GameObject 为 PlayerObject
2. **`VRCEnablePersistence`** - 启用持久化
3. **`UdonBehaviour` / `UdonSharpBehaviour`** - 包含要持久化的数据
4. **`[UdonSynced]` 字段** - 要持久化的具体数据

---

## Inspector 参数

`VRCEnablePersistence` 组件本身**没有 Inspector 字段**,其行为是隐式的:
- 启用后,该 GameObject 及子 GameObject 的所有 `[UdonSynced]` 字段自动持久化
- 数据在玩家**离开**实例时保存
- 玩家**重新加入**时恢复

---

## U# 完整示例

### 基础配置

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PlayerInventory : UdonSharpBehaviour
{
    // 这些字段会自动持久化(因为该 Behaviour 在 PlayerObject + EnablePersistence 子层级)
    [UdonSynced] private int coinCount = 0;
    [UdonSynced] private string playerLevel = "Level 1";
    [UdonSynced] private bool hasCompletedTutorial = false;
    
    public void AddCoin()
    {
        if (!Networking.IsOwner(gameObject)) return;
        
        coinCount++;
        RequestSerialization();
    }
}
```

### GameObject 层级

```
PlayerObject (GameObject)
├── VRCPlayerObject
├── VRCEnablePersistence
├── UdonBehaviour (PlayerInventory.cs)
│   └── [UdonSynced] 字段(coinCount, playerLevel 等)
├── Child Behaviour 1
│   └── [UdonSynced] 字段(其他数据)
└── Child Behaviour 2
    └── [UdonSynced] 字段(其他数据)
```

> **FACT**: `VRCEnablePersistence` 持久化**该 GameObject 及所有子 GameObject** 的 UdonBehaviour 同步字段。

---

## 完整数据流

### 1. 玩家首次加入

```
1. VRChat 创建该玩家的 PlayerObject 实例
2. 加载 VRCEnablePersistence + VRCPlayerObject
3. 初始化 UdonBehaviour 的 [UdonSynced] 字段为默认值
4. 调用 OnPlayerJoined 事件
```

### 2. 玩家游戏中

```
1. 玩家执行操作修改 [UdonSynced] 字段
2. Owner 端调用 RequestSerialization()
3. 数据同步到所有玩家(常规同步)
4. 数据**同时**保存到 VRChat 服务器(持久化)
```

### 3. 玩家离开

```
1. VRChat 检测玩家离开
2. VRCEnablePersistence 触发数据保存
3. PlayerObject 标记为"已保存状态"
4. 玩家退出实例
```

### 4. 玩家下次加入同一 World

```
1. VRChat 查找该玩家的持久化数据
2. 创建 PlayerObject 实例
3. 加载持久化的 [UdonSynced] 字段值
4. 调用 OnPlayerJoined 事件
5. UdonBehaviour 恢复数据
```

---

## 存储限制

> **FACT** (来自 [../../../api/persistence.md](../../../api/persistence.md)):
> - **单玩家 / 单 World**: ~300 KB 原始数据,压缩后 **~100 KB** 实际存储
> - **压缩**: VRChat 自动压缩(透明)
> - **超过限制**: 持久化失败,数据丢失
> - **错误反馈**: VRChat 客户端会显示警告

### 优化建议

1. **精简字段**: 只持久化必要数据
2. **使用位域压缩**: 多个 bool 用一个 byte(参见 [../../../world/udon/data-containers/byte-and-bit-operations.md](../../../world/udon/data-containers/byte-and-bit-operations.md))
3. **避免大字符串**: 字符串压缩率低
4. **使用 VRCJson**: 复杂数据序列化为 JSON 字符串

---

## U# 引用方式

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class PersistenceController : UdonSharpBehaviour
{
    [SerializeField] private VRCEnablePersistence persistence;
    
    public override void OnPlayerJoined(VRCPlayerApi player)
    {
        if (player.isLocal)
        {
            // 本地玩家 PlayerObject 已创建并恢复持久化数据
            Debug.Log("Persistent data loaded");
        }
    }
}
```

> ⚠️ **注意**: `VRCEnablePersistence` 引用本身通常**不需要**在 U# 中使用,其行为是隐式的。
> 重点是配置**正确层级结构**和**同步字段**。

---

## 与其他组件的依赖

| 关联组件 | 关系 |
|----------|------|
| **VRCPlayerObject** | **强依赖**,必须在同一 GameObject |
| **UdonBehaviour** | **强依赖**,要持久化数据必须有 UdonBehaviour |
| **VRC_SceneDescriptor** | 无直接依赖 |
| **VRCObjectSync** | 互斥(对象同步 vs 数据持久化,语义不同) |
| **VRCPickup** | 可同时使用(Pickup 状态本身不持久化) |

---

## PlayerData vs PlayerObject

> **FACT**: VRChat 提供两种持久化机制:

| 维度 | VRCEnablePersistence (PlayerObject) | PlayerData API |
|------|------------------------------------|---------------|
| **存储单位** | GameObject 状态 | 字符串键值对 |
| **使用方式** | 组件 + `[UdonSynced]` 字段 | `PlayerData.Set(key, value)` |
| **数据量** | 100 KB / 玩家 / World | 100 KB / 玩家 / World(共享) |
| **灵活性** | 适合结构化数据 | 适合简单数据 |
| **推荐场景** | 复杂游戏状态 | 简单标记 / 计数 |

### PlayerData API 示例

```csharp
// PlayerData API(更灵活)
using VRC.SDK3.Persistence;

public void SaveSetting(string key, string value)
{
    PlayerData.Set(Networking.LocalPlayer, key, value);
}

public string LoadSetting(string key)
{
    return PlayerData.GetString(Networking.LocalPlayer, key);
}
```

**PlayerData 完整 API**: [../../../api/persistence.md](../../../api/persistence.md)

---

## 最佳实践

1. **明确数据归属**: 决定用 PlayerObject 还是 PlayerData,不要混用
2. **分层组织**: 复杂数据按模块分多个 UdonBehaviour,每个负责一个子系统
3. **Owner 验证**: 持久化只对 Owner 端有效,非 Owner 写入被忽略
4. **避免频繁序列化**: 每次 RequestSerialization 都消耗带宽
5. **错误处理**: VRChat 客户端会显示持久化失败警告,需测试

---

## 常见陷阱

1. **缺少 VRCPlayerObject**: VRCEnablePersistence 失效
2. **非 Owner 端写入**: 数据被忽略,无错误提示
3. **超过 100 KB**: 持久化失败,数据丢失
4. **同步模式错误**: 必须有 `[UdonSynced]` 字段,普通字段不持久化
5. **多次添加 VRCEnablePersistence**: 行为未定义
6. **未触发 RequestSerialization**: 修改字段不保存

---

## 跨页引用

- **持久化完整 API**: [../../../api/persistence.md](../../../api/persistence.md)
- **Networking 完整 API**: [../../../api/networking.md](../../../api/networking.md)
- **数据容器 (VRCJson / VRCDataList)**: [../../../world/data-containers.md](../../../world/data-containers.md)
- **字节位运算**: [../../../world/udon/data-containers/byte-and-bit-operations.md](../../../world/udon/data-containers/byte-and-bit-operations.md)
- **VRCPickup**: [../../../api/pickups.md](../../../api/pickups.md)
- **VRC_SceneDescriptor**: [./vrc-scenedescriptor.md](./vrc-scenedescriptor.md)

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_enablepersistence/
- 完整持久化 API: [../../../api/persistence.md](../../../api/persistence.md)
- 数据容器参考: [../../../world/data-containers.md](../../../world/data-containers.md)
