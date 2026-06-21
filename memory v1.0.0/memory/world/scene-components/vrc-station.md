# VRC Station

> 玩家固定座位组件
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_station
> 官方类名: `VRCStation`
> 最后更新: 2026-06-15
> 最新更新日期: 2024-12-10

---

## 概述

`VRCStation` 允许玩家通过 Interact 坐下。SDK 中提供 `VRCChair3` Prefab 作为示例。

> **FACT** (来自官方文档): 此组件**也可以在 Avatar 上使用**,用于在 Avatar 上创建座位(可承载其他玩家)。

---

## Inspector 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **Player Mobility** | enum | ✅ | 玩家坐下时能否移动(Mobile / Immobilize / Immobilize For Vehicle) |
| **Can Use Station From Station** | bool | ❌ | 玩家坐在 Station 中时是否可切换到其他 Station |
| **Animation Controller** (可选) | RuntimeAnimatorController | ❌ | 自定义坐下动画(覆盖 Avatar 默认 "Sitting" playable layer) |
| **Disable Station Exit** | bool | ❌ | 玩家是否无法通过常规方式退出 Station(需用 trigger 强制退座) |
| **Seated** | bool | ❌ | 该 Station 是否代表玩家坐下(影响 Avatar Seated IK) |
| **Station Enter Player Location** | Transform | ✅ | 玩家坐下时传送到的 Transform 位置 |
| **Station Exit Player Location** | Transform | ✅ | 玩家退座时传送到的 Transform 位置 |
| **Controls Object** | GameObject | ❌ | 该 Station 控制一个物体(如车辆) |

---

## Player Mobility 详解

| 选项 | 行为 | 适用场景 |
|------|------|----------|
| **Mobile** | 坐下时仍可移动 | 沙发、轮椅、漂浮平台 |
| **Immobilize** | 不可移动,移动到 "Station Enter Location" | 椅子、观景台 |
| **Immobilize For Vehicle** | 同 Immobilize,但针对移动 Station 优化 | 车辆、飞船、过山车 |

---

## Animation Controller

可选参数,用于覆盖 Avatar 默认的 "Sitting" 可播放层动画:
- **不指定**: 使用 Avatar 默认的 Sitting 动画
- **指定**: 使用自定义 Animator Controller

> **FACT**: Animation Controller 作用于 Avatar 的 Sitting playable layer,允许完全自定义坐下动画(飞机驾驶、汽车方向盘等)。

---

## Seated 参数详解

> **FACT** (来自官方文档): `Seated` 字段决定是否启用 **Seated-IK**(Avatar 的 Sitting playable layer 切换)。
> - **Seated=true**: 启用 Seated-IK,Avatar 应用"坐下"姿态
> - **Seated=false**: 不启用 Seated-IK,玩家可以在车辆上站立

**SDK2 与 SDK3 差异**:
- **SDK2 Avatar**: Station 会自动应用 Seated 动画(由 State Behaviors 处理)
- **SDK3 Avatar**: Station 不自动应用动画,需自行实现

---

## U# 引用与事件

### 引用方式

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

[RequireComponent(typeof(VRCStation))]
public class ChairController : UdonSharpBehaviour
{
    [SerializeField] private VRCStation station;
    
    public override void Interact()
    {
        // 注意:VRCStation 的 Interact 行为是进入 Station,
        // 通常不需要在 U# 中处理 Interact,直接交给 VRCStation
    }
    
    public override void OnStationEntered(VRCPlayerApi player)
    {
        // 玩家进入 Station
        Debug.Log($"{player.displayName} sat in {gameObject.name}");
        
        // 例如:启动车辆控制
        if (station.Seated && player.isLocal)
        {
            // 本地玩家坐下,启动控制
        }
    }
    
    public override void OnStationExited(VRCPlayerApi player)
    {
        // 玩家退出 Station
        Debug.Log($"{player.displayName} left {gameObject.name}");
    }
}
```

> **FACT** (来自官方文档): `OnStationEntered` 和 `OnStationExited` 在 **VRCStation 组件所在 GameObject** 的 Udon Behaviour 上触发(不是玩家自己的)。

### 强制退座

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class ChairController : UdonSharpBehaviour
{
    [SerializeField] private VRCStation station;
    
    public void ForceExitLocalPlayer()
    {
        // 让本地玩家离开 Station
        if (Networking.LocalPlayer != null)
        {
            // VRCStation 内部提供 ExitStation 节点(Udon Graph)
            // U# 中调用方式:
            station.gameObject.SetActive(false);
            station.gameObject.SetActive(true);
        }
    }
}
```

> ⚠️ **注意**: 在 U# 中强制退座的直接 API 不公开,常用方法:
> 1. 临时禁用/启用 VRCStation
> 2. 移动 Station 到很远位置
> 3. 使用 Udon Graph 的 `ExitStation` 节点(详见 [../../../world/udon/](../../../world/udon/))

---

## 事件触发位置

> **FACT** (来自官方文档,验证于 2024-12-10):
> - `OnStationEntered` / `OnStationExited` 事件在 **VRCStation 组件所在 GameObject** 上的 Udon Behaviour 中触发
> - 同一 GameObject 必须有 `UdonBehaviour` 或 UdonSharpBehaviour 接收事件

### 错误示例

```csharp
// ❌ 错误:事件在 UdonBehaviour 上,但 VRCStation 在另一个 GameObject
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class WrongScript : UdonSharpBehaviour
{
    public override void OnStationEntered(VRCPlayerApi player)
    {
        // 这个方法**不会**被调用,因为 VRCStation 不在此 GameObject 上
    }
}
```

### 正确示例

```csharp
// ✅ 正确:VRCStation 与 UdonBehaviour 在同一 GameObject
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class ChairScript : UdonSharpBehaviour
{
    [SerializeField] private VRCStation station;  // 引用同 GameObject 的 Station
    
    public override void OnStationEntered(VRCPlayerApi player)
    {
        // 正确触发
    }
}
```

---

## 创建 Station 的步骤

> **FACT** (来自官方文档): 创建一个基本 Station 需要 4 个步骤:

1. **VRCStation 组件**: 在 GameObject 上添加 VRCStation,设置 Enter 和 Exit Point(可为自己或另一个 Transform)
2. **Collider**: 添加 Collider(通常 `Is Trigger` 启用)
3. **UdonBehaviour**: 添加 Udon 程序处理坐下逻辑(SDK 中提供 `StationGraph` 示例)
4. **(可选) Mesh**: 椅子/座位的视觉外观

### 完整场景结构

```
Chair (GameObject)
├── VRCStation
│   ├── Station Enter Player Location: EnterPoint
│   ├── Station Exit Player Location: ExitPoint
│   ├── Player Mobility: Immobilize
│   └── Seated: true
├── UdonBehaviour (StationGraph 或自定义 U#)
├── Collider (Is Trigger = true)
└── Mesh (视觉)

EnterPoint (Transform, child of Chair)
ExitPoint (Transform, child of Chair, 通常在椅子外)
```

---

## 用于 World 的 Station

### Animator 访问 Avatar 参数

> **FACT** (来自官方文档): 你的 Animator 可以访问 Avatar 参数来响应 Avatar 进入 Station。
> - **`Seated` 参数**: 检测 Avatar 的 Seated-IK 是否启用
> - **`AvatarVersion` 参数**: 检测 Avatar 是 SDK2 还是 SDK3
> - **`InStation` 参数**: 检测 Avatar 是否在 Station 中

### SDK2 vs SDK3 Avatar

> **FACT** (来自官方文档,验证于 2024-12-10):

**SDK2 Avatar**:
- Station 自动应用 Seated 动画(State Behaviors)
- 检查 `Seated` 决定 Fixed Seated Pose 或 Full-body 动画
- 检查 `AvatarVersion < 3`

**SDK3 Avatar**:
- Station **不自动应用** Seated 动画
- 开发者可完全控制 Tracking Control / Pose Space 变化
- 决定权在 Creator,不在 SDK

> ⚠️ **重要**: SDK3 Avatar 的 `Seated` 参数**不一定**表示该 Avatar 的 Tracking Type。
> Creator 必须自己实现 Tracking Control 行为。

### 检测 SDK2 Avatar

```csharp
// 在 Animator 状态机中
// 如果 AvatarVersion < 3,应用旧版 Seated 行为
// 如果 AvatarVersion == 3,应用新版行为
```

### Animator 状态机示例

```
Idle
  ↓
[检测 InStation = true] → SeatedState
  ├── [AvatarVersion = 3] → ModernSeatedAnimation
  └── [AvatarVersion < 3] → LegacySeatedAnimation
```

---

## 用于 Avatar 的 Station

> **FACT** (来自官方文档): 默认的 `VRCChair` Prefab 可用于 Avatar,让其他玩家"坐在"你身上。

### Avatar Station 限制

- **最多 6 个 Stations**: 每个 Avatar 最多 6 个 Station,超过会被禁用
- **Entry 与 Exit 距离**: Entry 和 Exit Transform 之间不能超过 2 米
- **红色框必须启用**: 上传时必须启用,禁用则 Station 失效

### 上传前配置

> **FACT** (来自官方文档): 红色框(包含 Station 组件的 GameObject)必须在**上传时启用**,否则 Station 不工作。

- 切换红色框会移除当前坐在该 Station 的玩家
- 切换绿色框(子组件)只阻止新玩家坐下
- **必须**在 FX Layer 中实现切换逻辑

### Avatar Station 与 Safety

> **FACT** (来自官方文档): 用户可以用 Safety 系统禁用动画。
> - 如果 Avatar Station 默认开启(开关默认 on),即使穿戴者用动画关闭,Station 仍激活
> - 这是 VRChat 设计,Creator 无法覆盖

### Animator 行为差异

```csharp
// U# 中(用于 World Station)
public override void OnStationEntered(VRCPlayerApi player) { }

// U# 中(用于 Avatar Station)
// Avatar 上的 Udon 可以处理自己作为 Station 的逻辑
public override void OnStationEntered(VRCPlayerApi player)
{
    // 玩家坐到本 Avatar 上
}
```

---

## 典型应用场景

### 1. World 椅子

最基础应用。椅子 + VRCStation + Collider,玩家坐下聊天。

### 2. 车辆

VRCStation + 移动逻辑,玩家坐下后可驾驶车辆。配合 `Immobilize For Vehicle` 优化移动 Station 性能。

### 3. Avatar 装备

用 Avatar 上的 VRCStation 让其他玩家"坐在"自己身上,如摩托车后座、宠物、食物等。

### 4. 观景台 / 拍照点

VRCStation + Camera Dolly,玩家坐下后自动播放相机动画。

### 5. 多人载具

VRCStation + 多座位 + 主控 Station,实现"驾驶员"控制所有座位。

---

## 性能考虑

- **多个 Station**: 性能影响小,Station 本身轻量
- **移动 Station**: 性能影响大,频繁移动 Station 会触发大量网络同步
- **Seated-IK**: 启用 Seated 后,Avatar 计算成本略增(可忽略)
- **Anim 切换**: 频繁进出 Station 会触发 Animator 状态切换,稍耗性能

---

## 平台兼容性

- **PC / Quest**: 完全相同
- **VR / Desktop**: 完全相同

---

## 最佳实践

1. **总是设置 Enter 和 Exit Point**: 避免玩家被卡在物体内部
2. **Enter Point 略向上偏移**: 0.1-0.2 单位,避免卡进地面
3. **Exit Point 放在安全位置**: 玩家退座时不会卡进墙
4. **禁用移动用 Immobilize**: 不要用 Mobile + 阻挡实现"不可移动",浪费资源
5. **Anim 优化**: 复杂的自定义 Animator Controller 限制为必须时使用
6. **强制退座用 trigger**: 而不是禁用 Station 物体

---

## 常见陷阱

1. **VRCStation 与 UdonBehaviour 不在同一 GameObject**: 事件不触发
2. **Enter/Exit Point 留空**: SDK 警告,功能异常
3. **移动 Station 网络未同步**: 玩家 A 移动 Station,玩家 B 看到 Station 在原位
4. **Avatar 上 6 个 Station 上限**: 超出被禁用
5. **Avatar Station 红色框未启用**: 上传后 Station 失效
6. **忘记 Seated 参数**: Avatar 站姿而非坐姿

---

## 跨页引用

- **VRC_SceneDescriptor**: [./vrc-scenedescriptor.md](./vrc-scenedescriptor.md)
- **VRCPickup**: [../../../api/pickups.md](../../../api/pickups.md) (可与 Station 组合)
- **VRCObjectSync**: [./vrc-objectsync.md](./vrc-objectsync.md) (用于移动 Station)
- **事件参考**: [../../../api/events-reference.md](../../../api/events-reference.md#station-事件)
- **Udon 编程**: [../../udon/](../../udon/)

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_station
- 关联组件: [VRC_SceneDescriptor](./vrc-scenedescriptor.md)
- SDK StationGraph 示例: [../../sdk-prefabs.md](../../sdk-prefabs.md)
- Player API: [../../../api/player-api.md](../../../api/player-api.md)
