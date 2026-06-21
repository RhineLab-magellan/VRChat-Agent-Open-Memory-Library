# VRC Scene Descriptor ⭐

> 场景描述符(**World 必含核心组件**)
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_scenedescriptor
> 官方类名: `VRCSceneDescriptor`
> 最后更新: 2026-06-15
> 最新更新日期: 2025-12-11

---

## 概述

`VRCSceneDescriptor` 描述 VRChat World。每个想用作 VRChat World 的 Unity 场景**必须有且仅有一个** `VRCSceneDescriptor` 组件。

> ⭐ **核心组件 - World 必备**:
> - **缺失**: World **完全无法加载**
> - **多个**: SDK 报错,无法发布
> - **位置**: 通常放在场景根 GameObject,命名为 "Scene Descriptor" 或 "VRCWorld"

---

## Inspector 参数(完整)

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **Spawns** | Transform[] | ✅ | 玩家出生点的 Transform 数组 |
| **Spawn Radius** | float | ✅ | 玩家在出生点附近随机生成的范围(0=精确位置) |
| **Spawn Order** | enum | ✅ | 出生点使用顺序(First / Sequential / Random / Demo) |
| **Spawn Orientation** | enum | ✅ | 玩家初始朝向(Default / AlignPlayer / AlignRoom) |
| **Reference Camera** | Camera | ✅ | 该相机的设置被应用于房间内用户 |
| **Respawn Height -Y** | float | ✅ | 玩家掉落到此 Y 高度以下时重生(同时 Pickup 物体也会重生或销毁) |
| **Object Behaviour At Respawn** | enum | ✅ | Pickup 物体掉出世界时的处理(Destroy / Respawn) |
| **Forbid Free Modification** | bool | ❌ | 如果开启,非 Master 玩家不能操作非 Sync 物体 |
| **Forbid User Portals** | bool | ❌ | 禁止用户从 World 菜单打开 Portal |
| **User Custom Voice Falloff Range** | bool | ❌ | 启用自定义语音衰减范围 |
| **Unity Version** | string | 自动 | Unity 版本,通常不需要手动修改 |
| **Dynamic Prefabs** | GameObject[] | ❌ | **已弃用**,SDK3 不再使用 |
| **Dynamic Materials** | Material[] | ❌ | **已弃用**,SDK3 不再使用 |
| **Interact Passthrough** | LayerMask | ❌ | 允许交互穿透的 User Layers |

> **FACT** (来自官方文档,验证于 2025-12-11): `Dynamic Prefabs` 和 `Dynamic Materials` 字段**已弃用**,在 SDK3 中不再使用,保留仅为向后兼容。

---

## Spawn Order 详解

| 选项 | 行为 |
|------|------|
| **First** | 总是使用第一个 Spawn(简单场景推荐) |
| **Sequential** | 按顺序使用 Spawns 列表(玩家按时间顺序) |
| **Random** | 随机选择 Spawn(社交 World 常用) |
| **Demo** | Spawn 是房间中心位置,玩家根据 Room Scale 位置保持相对偏移 |

---

## Spawn Orientation 详解

| 选项 | 行为 |
|------|------|
| **Default** | VRChat 默认(目前为 "Align Player With Spawn Point") |
| **Align Player With Spawn Point** | 玩家朝向与 Spawn Transform 一致 |
| **Align Room With Spawn Point** | 玩家 Room Scale 中心与 Spawn Point 对齐 |

> **FACT**: Default 当前等同 AlignPlayer,但未来可能变化。建议显式选择以避免行为变化。

---

## Respawn Height 详解

- **作用**: 玩家(或 Pickup)Y 坐标低于此值时自动重生
- **推荐值**: 地图最低点 Y - 5 到 - 10
- **过小**: 玩家可能掉出世界后才触发重生
- **过大**: 误判玩家正常位置为掉出世界

> **FACT**: 此字段同时影响 Pickup 物体,Object Behaviour At Respawn 决定 Pickup 是 Destroy 还是 Respawn 到初始位置。

---

## Object Behaviour At Respawn

| 选项 | 行为 |
|------|------|
| **Destroy** | 删除掉出世界的 Pickup |
| **Respawn** | 将 Pickup 重生到其初始位置 |

---

## Forbid Free Modification

> **FACT**: 启用后,非 Master 玩家无法操作非同步物体(无法移动、旋转、改 Transform)。

**典型用法**:
- 防止玩家破坏 World 布局
- 减少作弊可能性
- 保护关键游戏逻辑物体

**注意**:
- **Master 玩家仍可修改**所有物体
- VRCObjectSync / VRCPickup 等同步物体不受影响(它们有 Owner 概念)

---

## Forbid User Portals

启用后,玩家无法从 VRChat 菜单创建 Portal。

**典型用法**:
- 防止玩家逃出限定区域
- 防止"World hopping"行为
- 强制游戏流程

---

## Interact Passthrough

**LayerMask**: 定义哪些 User Layers 上的 Collider **允许交互穿透**。

**典型用法**:
- 让玩家可以"穿过"某些 UI 元素触发下层 UI
- 解决多层 UI 重叠时的优先级问题

详见 [../../layers.md](../../layers.md)

---

## U# 引用方式

### 基础引用

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class WorldInitializer : UdonSharpBehaviour
{
    [SerializeField] private VRCSceneDescriptor sceneDescriptor;
    [SerializeField] private Transform[] customSpawnPoints;
    
    public override void OnPlayerJoined(VRCPlayerApi player)
    {
        if (player.isLocal)
        {
            // 本地玩家刚加入,初始化场景逻辑
            Debug.Log($"World: {sceneDescriptor.gameObject.name}");
        }
    }
}
```

### 动态修改 Spawn Points(不推荐)

> ⚠️ **警告**: VRCSceneDescriptor 的大部分字段在运行时是 **只读** 的。建议在 Inspector 中预先配置。

```csharp
// 通常不修改 VRCSceneDescriptor
// 而是用 VRCStation / VRC_AvatarPedestal 等组件处理玩家位置
```

---

## 必备关联组件

| 组件 | 关系 |
|------|------|
| **VRC_SceneDescriptor** | **自身** - World 必备 |
| **VRCObjectSync** | 用于 World 内可交互物理对象 |
| **VRCPickup** | 用于 World 内可拾取物体 |
| **VRCStation** | 用于 World 内可坐下位置 |
| **Audio Source** | 配合 VRC_SpatialAudioSource 处理 3D 音频 |
| **Lighting** | World 必须有合适的光照(详见 [../../performance-guide.md](../../performance-guide.md)) |

---

## Reference Camera

> **FACT** (来自官方文档): 该相机的设置被应用于房间内所有用户。

**典型配置**:
- **位置**: 出生点附近的相机,展示 World 入口
- **Field of View**: 标准 60-70 度
- **Clipping Planes**: Near 0.1, Far 1000+
- **Clear Flags**: Skybox 或 Solid Color

**注意**:
- Reference Camera 不会渲染到屏幕,只用于配置
- 玩家实际看到的是 VRChat 内部相机(由其控制)
- 修改 Reference Camera 会影响所有用户的初始视角

---

## Audio 设置关联

VRCSceneDescriptor 与 VRC_SpatialAudioSource 配合实现 3D 音频:

```csharp
[SerializeField] private VRC_SpatialAudioSource[] audioSources;

// 玩家位置变化时,音频自动调整(VRChat 客户端处理)
```

**音频设置详情**: 参见 [../../../api/audio.md](../../../api/audio.md)

---

## 性能考虑

- VRCSceneDescriptor 本身**不消耗性能**(只是配置)
- **Spawn 数组大小**: 太多 Spawn 略微增加初始化时间(通常 < 20)
- **Reference Camera 复杂度**: 复杂的相机设置可能在初始化时短暂影响帧率

---

## 平台兼容性

- **PC / Quest**: 完全相同
- **不同平台 Spawn 行为**: 完全相同(VRChat 抽象层)

---

## 最佳实践

1. **统一命名 Scene Descriptor 对象**: `Scene Descriptor` 或 `VRCWorld`
2. **Spawn Points 放在出生点上方 0.5-1.0 单位**: 避免卡在地面
3. **Respawn Height 留出缓冲**: 比地图最低点低 5-10 单位
4. **配置多个 Spawn Points**: 大 World 至少 2-3 个,Random 模式需要 3+
5. **Reference Camera 优化**: 不要放太多光源
6. **Forbid User Portals 按需**: 社交 World 通常允许,游戏 World 视情况禁止

---

## 常见陷阱

1. **忘记添加 VRCSceneDescriptor**: World 无法发布
2. **添加多个 VRCSceneDescriptor**: SDK 报错
3. **Spawn Points 留空**: 玩家无法出生
4. **Respawn Height 过高**: 玩家误判重生
5. **Forbid Free Modification 与游戏逻辑冲突**: 玩家无法操作应操作物体
6. **Dynamic Prefabs 误用**: 字段已弃用,使用 Pool 模式(详见 [../../patterns/](../../patterns/))

---

## 完整场景结构示例

```
World (GameObject)
├── VRCSceneDescriptor
│   ├── Spawns: [SpawnPoint_1, SpawnPoint_2, SpawnPoint_3]
│   ├── Reference Camera: SpawnCamera
│   ├── Respawn Height: -50
│   └── ...
├── SpawnPoint_1 (Transform)
├── SpawnPoint_2 (Transform)
├── SpawnCamera (Camera)
├── Environment (GameObject)
│   ├── Terrain
│   ├── Lighting
│   └── ...
├── Interactive (GameObject)
│   ├── VRCObjectSync_1
│   ├── VRCObjectSync_2
│   └── ...
├── Stations (GameObject)
│   ├── VRCStation_Chair1
│   ├── VRCStation_Chair2
│   └── ...
└── UI (GameObject)
    └── VRC_UIShape + Canvas
```

---

## 跨页引用

- **VRCObjectSync**: [./vrc-objectsync.md](./vrc-objectsync.md)
- **VRCStation**: [./vrc-station.md](./vrc-station.md)
- **VRCEnablePersistence**: [./vrc-enablepersistence.md](./vrc-enablepersistence.md)
- **VRCPickup**: [../../../api/pickups.md](../../../api/pickups.md)
- **VRC_SpatialAudioSource**: [../../../api/audio.md](../../../api/audio.md)
- **VRC_UIShape**: [../../../api/ui.md](../../../api/ui.md)
- **Layers**: [../../layers.md](../../layers.md)
- **性能指南**: [../../performance-guide.md](../../performance-guide.md)

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_scenedescriptor
- Audio 集成: [../../../api/audio.md](../../../api/audio.md)
- World 性能: [../../performance-guide.md](../../performance-guide.md)
