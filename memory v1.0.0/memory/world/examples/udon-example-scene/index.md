# Udon Example Scene

> SDK 内置示例场景 · VRChat Worlds 官方标准参考
> 源文档:https://creators.vrchat.com/worlds/examples/udon-example-scene/
> 最后更新:2026-06-15
> SDK 版本参考:VRChat Worlds SDK(含 VRCWorldSettings、UdonProgramSources 等)

---

## 概述

Udon Example Scene 是 VRChat 官方 Worlds SDK 内置的标准示例场景,位于:

```
Packages/com.vrchat.worlds/Samples/UdonExampleScene/
```

该场景演示了 World 中常见的 Udon 交互模式,**所有 Prefab 都可以直接拖入自定义 World 复用**。包含 13+ 个 Prefab 演示,涵盖按钮、Avatar 切换、Station、Mirror、Cube 交互、变量同步、Pickup、玩家检测、对象池、视频同步等核心范式。

> **重要价值**:这是 VRChat 官方推荐的 Udon 学习起点,所有 Udon Graph / UdonSharp 程序均经过官方验证。

---

## Prefab 分类索引

| 分类 | Prefab | 关键程序 | 核心模式 |
|------|--------|---------|---------|
| **World 初始化** | VRCWorld | VRC Scene Descriptor / VRC Pipeline Manager / VRCWorldSettings / Avatar Scaling Settings | World 上传与配置 |
| **玩家交互** | AvatarPedestal | (内置切换) | 玩家点击切换 Avatar |
| **玩家交互** | VRCChair3 | StationGraph | 玩家坐下(Station) |
| **玩家交互** | MirrorSystem | ToggleGameObject | Interact 翻转对象 |
| **Cube 演示** | InteractCube | SendEventOnInteract + ChangeMaterialOnEvent | Interact 事件传播 |
| **Cube 演示** | TimerCube | SendEventOnTimer | 定时器事件 |
| **Cube 演示** | UseCube | SendEventOnUse + VRCObjectSync | 持有 + 同步 |
| **变量同步** | ButtonSyncOwner | ButtonSyncOwner(Manual Sync) | Owner 同步点击计数 |
| **变量同步** | ButtonSyncAnyone | ButtonSyncAnyone | 非 Owner 发送事件给 Owner |
| **变量同步** | ButtonSyncBecomeOwner | ButtonSyncBecomeOwner | 转移所有权后修改 |
| **变量同步** | SliderSync | SliderSync | 滑块 + 同步 |
| **变量同步** | Toggle | ToggleSync | 开关 + 同步 |
| **变量同步** | Dropdown | DropdownSync | 下拉框 + 同步 |
| **变量同步** | InputField | InputFieldSync | 输入框 + 同步 |
| **Pickup** | PickupCube | SyncPickupColor(Continuous Sync) | 持有 + 颜色变化 |
| **Pickup** | PickupSphere | (无 Udon,纯 VRCObjectSync) | 同步持有物体 |
| **玩家检测** | PlayerTrigger | PlayerTrigger | Trigger 区域 |
| **玩家检测** | PlayerCollision | FireOnTrigger + Projectile | 物理碰撞 + 投射物 |
| **玩家检测** | PlayerParticleCollision | PlayerCollisionParticles | 粒子碰撞 |
| **视频播放** | UdonSyncPlayer | UdonSyncPlayer | URL + 播放时间同步 |
| **数组同步** | CubeArraySync | CubeArraySync | Boolean Array 同步 |
| **对象池** | ObjectPool | ObjectPool + Pooled Box | 对象池 + 重生 |

---

## 一、World 初始化 Prefabs

### 1.1 VRCWorld

**位置**:`\Packages\com.vrchat.worlds\Samples\VRCPrefabs\VRCWorld.prefab`

VRCWorld 是上传 World 到 VRChat 的标准入口 Prefab,包含四个组件:

| 组件 | 职责 |
|------|------|
| **VRC Scene Descriptor** | 定义 World 基础属性,**每个 VRChat World 必需** |
| **VRC Pipeline Manager** | 包含 World ID,添加 Scene Descriptor 时自动生成 |
| **VRCWorldSettings**(Udon Graph) | 调整玩家移动速度(详见 [player-mod-setter.md](player-mod-setter.md)) |
| **Avatar Scaling Settings**(Udon Graph) | 限制 Avatar 缩放范围(详见 [avatar-scaling-settings.md](avatar-scaling-settings.md)) |

> VRCWorld 默认已包含在多数 VRChat 场景中。

### 1.2 AvatarPedestal

可作为 Prefab 直接使用,内置程序支持玩家 Interact 时切换 Avatar(Prefab 默认行为)。

**修改交互距离**:解包 Prefab(Unpack) → 修改 Udon Behaviour 组件的 "Proximity" 设置。

### 1.3 VRCChair3

可作为 Prefab 直接使用,包含 `StationGraph` 程序:

- 玩家 Interact 时坐下
- 玩家进入/离开时记录 displayName

### 1.4 MirrorSystem

`MirrorSystem` 对象包含 `ToggleGameObject` 程序,使用 Interact 事件翻转目标对象 Active/Inactive 状态。此例中控制一个 `VRCMirror` 子对象。

---

## 二、Cubes 演示

### 2.1 InteractCube

**核心组件**:
- `SendEventOnInteract` — 监听 Interact 事件(玩家指向对象并按 Use 键时触发)
- `ChangeMaterialOnEvent`(子对象)— 接收事件后从材质数组切换材质

**事件传播链**:
```
玩家 Interact → SendEventOnInteract 触发 → 发送自定义事件 "changeMaterial"
→ ChangeMaterialOnEvent 接收 → 切换材质
```

**复用方式**:在 UdonBehaviour Inspector 中修改 SendEventOnInteract 的 eventName。

### 2.2 TimerCube

**核心组件**:
- `SendEventOnTimer` — 运行指定时长的定时器,到时发送指定事件
- `ChangeMaterialOnEvent`(子对象)

**配置参数**:
- `duration`:定时时长(秒)
- `eventName`:发送的自定义事件名

**复用方式**:修改 duration 控制触发频率,修改 eventName 适配其他程序。

### 2.3 UseCube

**核心组件**:
- `SendEventOnUse`(Model 子对象)— Pickup 状态下"Use"时发送事件
- `VRCObjectSync`(Model 子对象)— 同步物体移动到其他用户
- `ChangeMaterialOnEvent`(MaterialChanger 子对象)

**事件传播链**:
```
玩家 Pickup + Use → SendEventOnUse 触发 → 发送 "changeMaterial" 
→ ChangeMaterialOnEvent 接收 → 切换材质
+ VRCObjectSync 同步 Model 位置
```

**复用方式**:Inspector 中修改 SendEventOnUse 的 eventName。

---

## 三、Udon Variable Sync(变量同步)

> 演示如何将变量值从 Owner 同步给所有其他用户。**核心区域**:Canvas 上的多个 UI 元素。

### 3.1 ButtonSyncOwner(Manual Sync 第一个示例)

**同步模式**:**Manual Sync** ← 第一个使用 Manual Sync 模式的程序

**工作流程**:

```
1. UI Button OnClick() → UdonBehaviour.SendCustomEvent("OnClick")
2. OnClick 事件检查点击者是否为 Owner
3. 如果是 Owner:
   - clickCount 自增 1
   - 调用 RequestSerialization(通知 Udon 更新数据)
4. 'Set clickCount' 节点 sendChange = ON → 触发 Variable Change 事件
5. Variable Change 事件 → 更新 Button 文本(对所有人生效)
```

**关键节点**:
- `RequestSerialization` — Manual Sync 程序通知 Udon 序列化的标准调用
- `sendChange` 开关 — 触发 Variable Change 事件,让所有人响应新值

**参见**:`memory/api/networking.md` 的 Manual Sync 模式

### 3.2 ButtonSyncAnyone(扩展:非 Owner 也能点击)

在 ButtonSyncOwner 基础上增加非 Owner 处理逻辑:

```
非 Owner 点击 → 发送 Custom Event "OnClick" 给 Owner
→ Owner 接收事件 → 走标准处理流程
```

**优势**:玩家不必关心所有权,UI 永远可点击。

### 3.3 ButtonSyncBecomeOwner(扩展:转移所有权)

演示如何改变对象所有权:

```
非 Owner 点击 → 分配所有权给该玩家
→ 玩家成为 Owner → 修改 clickCount → RequestSerialization
```

**适用场景**:
- 需要修改多个变量
- 逻辑复杂(不止是自增)

**所有权转移规则**:
- 自定义 `OnOwnershipRequest` 逻辑决定是否批准
- 如果不添加自定义逻辑,所有所有权请求自动批准
- 可基于 `requester`、`newOwner` 或两者构建自定义逻辑

**参见**:`memory/api/networking.md` 所有权系统

### 3.4 SliderSync(滑块 + 同步)

工作模式与 ButtonSyncBecomeOwner 类似,差异点:

**防无限循环**:
```
OnValueChanged 触发 → 检查新值是否与 sliderValue 相同
- 如果相同 → 跳过(避免 Udon 更新 Slider 时再次触发)
- 如果不同 → 转移所有权 + 发送新值
```

**额外**:使用 Variable Change 事件更新 Text 字段显示当前值。

### 3.5 Toggle(ToggleSync)

工作模式与 SliderSync 一致:**值变化时 → 检查是否相同 → 转移所有权 + 发送新值**。

### 3.6 Dropdown(DropdownSync)

工作模式与 Toggle/Slider 一致:值变化时 → 检查差异 → 转移所有权 + 发送新值。

### 3.7 InputField(InputFieldSync)

工作模式与 Dropdown 一致:值变化时 → 检查差异 → 转移所有权 + 发送新值。

---

## 四、Pickup 同步

### 4.1 PickupCube

**组件**:
- `VRCPickup` — 支持 Pickup
- `VRCObjectSync` — 自动同步位置
- `UdonBehaviour`(Sync Mode: **Continuous**)— `SyncPickupColor` 程序

**为什么是 Continuous 而非 Manual**:Transform 变化频繁,需要持续更新。

**SyncPickupColor 工作原理**:
```csharp
// Update 事件中
if (localPlayer == Owner && VRCPickup.Get.isHeld) {
    // 平滑改变颜色
    // 无需调用 RequestSerialization(Continuous 模式自动序列化)
}
```

### 4.2 PickupSphere

**完全无 Udon 程序**!仅使用 `VRCPickup` + `VRCObjectSync` 实现持有与同步。**最简 Pickup 实现范式**。

---

## 五、Player Detection(玩家检测)

### 5.1 PlayerTrigger

**最常用的玩家进入/离开区域检测方式**。

**配置**:
- `TriggerArea` 对象
- 半透明蓝色材质
- `Box Collider` 勾选 `IsTrigger`
- `UdonBehaviour` + `PlayerTrigger` 程序源

**事件**:
- `OnPlayerTriggerEnter` — 玩家进入触发器
- `OnPlayerTriggerExit` — 玩家离开触发器

**实现**:获取玩家 displayName → 更新 Canvas 文本。

### 5.2 PlayerCollision

演示 `OnPlayerCollisionEnter/Exit`(物理对象进入玩家 Collider 时触发)。

**事件链**:
```
玩家进入 TriggerArea → FireOnTrigger 程序触发
→ 发送自定义事件 "Fire" 给 Projectile
→ Projectile 添加自身 Force → 飞向玩家
→ 与玩家碰撞 → 写入玩家 displayName 到 Text
```

> **注意**:PlayerCollision 事件**仅在受影响的玩家本地触发**。如需通知其他玩家,必须自行通过 Synced Variables 或 Custom Network Events 实现。

### 5.3 PlayerParticleCollision

工作方式类似 PlayerCollision,使用 Trigger Area 启动事件链:

```
玩家进入 Trigger Area → SetActiveFromPlayerTrigger 启用 CollisionParticles
→ ParticleSystem 发射(World Collision + Send Collision Messages)
→ PlayerCollisionParticles 触发 OnPlayerParticleCollision
→ 写入 displayName 到目标 Text
```

---

## 六、Udon Sync Player(视频同步)

**详见** [udon-video-sync-player.md](udon-video-sync-player.md)

`UdonSyncPlayer` 演示如何使用 Unity / AVPro 视频播放器加载并同步视频播放。**该程序较复杂,单独成页**。

**同步双要素**:
- **URL**:所有人观看相同视频
- **Playback Time**:所有人同步时间点

---

## 七、CubeArraySync(数组同步)

**核心价值**:演示**用极少带宽同步 25 个 Boolean 值**。

**程序结构**:
```csharp
public class CubeArraySync : UdonSharpBehaviour {
    [UdonSynced] public bool[] data = new bool[25];  // 25 个 bool 值
    public GameObject[] cubes = new GameObject[25];   // 25 个 Cube
}
```

**工作流程**:
```
1. 任何人点击包含所有 Cube 的对象
2. 发送 Custom Network Event "Randomize" 给 Owner
3. Owner 端 For 循环:
   - 生成 0~1 随机数
   - 如果 > 0.5 → 设为 on
   - 更新 data[i] = true/false
4. Owner 调用 RequestSerialization + 自定义事件 UpdateCubes
5. OnDeserialization(其他用户):
   - 遍历 data[i] → 设置对应 Cube 激活/禁用
```

**关键点**:
- **使用 OnDeserialization 而非 OnVariableChange**:**Array 类型变量不触发 Variable Change 事件**,所以需要等 OnDeserialization 拿到新数据后再更新场景。

---

## 八、Object Pool(对象池)

**组件**:`ObjectPool` — 帮助管理对象集合,**自动同步对象 Active 状态**。

**示例行为**:
- 物体从天空一个一个掉落到堆叠网格
- 点击 Box → 移除并从天空重生

**程序结构**:
```csharp
public class ObjectPool : UdonSharpBehaviour {
    // 定时器:定期尝试 Spawn 对象
    private void Update() { ... }
}

public class PooledBox : UdonSharpBehaviour {
    Vector3 initialPosition;
    public void Start() {
        initialPosition = transform.position;  // 保存初始位置
    }
    public void OnEnable() {
        transform.position = initialPosition;  // 重置位置(Spawn 时触发)
    }
}
```

---

## 九、Simple Pen System(画笔系统)

**详见** [simple-pen-system.md](simple-pen-system.md)

基础画笔也需要相当工作量,**单独成页**。

---

## 五种同步模式总结(本场景中演示)

| 模式 | 在 Udon Example Scene 中的体现 | 用途 |
|------|-------------------------------|------|
| **None** | `MirrorSystem` (ToggleGameObject) | 仅本地,无需网络同步 |
| **Manual** | `ButtonSyncOwner` / `SliderSync` 等变量同步程序 | 显式控制序列化时机(事件驱动) |
| **Continuous** | `PickupCube` (`SyncPickupColor`) | 高频自动序列化(Transform、Color 等) |
| **NoVariableSync** | (本场景未直接展示,但 UI 转发模式常配合) | 跨组件通信,变量不同步 |
| **Trigger** | `ObjectPool` Active 状态同步 | 由父级 ObjectPool 触发子对象同步 |

---

## 关键设计模式提取

### 1. 事件传播模式(SendEvent + ChangeMaterialOnEvent)

```
SendEventOn{Interact/Use/Timer} → 自定义事件 → ChangeMaterialOnEvent 接收
```

**复用**:
- 发送者程序可改 eventName
- 接收者程序保持不变(只听固定事件名)

### 2. 所有权检查 + Manual Sync 范式

```csharp
if (Networking.IsOwner(gameObject)) {
    // 修改 synced 变量
    RequestSerialization();
}
```

### 3. 防无限循环检测

```csharp
// SliderSync 中
if (newValue != currentValue) {
    // 避免 Udon 更新 UI 时再触发 OnValueChanged
    currentValue = newValue;
    RequestSync();
}
```

### 4. Array 同步必须用 OnDeserialization

```csharp
// CubeArraySync 中
public override void OnDeserialization() {
    // Array 变量不支持 Variable Change
    // 在这里更新本地状态
    for (int i = 0; i < data.Length; i++) {
        cubes[i].SetActive(data[i]);
    }
}
```

---

## 相关知识库关联

- **Networking 模式**:`memory/api/networking.md` 包含 Manual Sync / Continuous 完整规范
- **Pickup 行为**:`memory/api/pickups.md` 包含 VRCPickup / VRCObjectSync 完整 API
- **UI 转发**:`memory/api/ui.md` 包含 VRC_UIShape 使用规范
- **性能基线**:`memory/world/performance-guide.md` 可引用本场景作为 **基础性能基线**
- **事件驱动状态机**:`memory/patterns/event-driven-state-machine.md` 关联 Sync 程序的 Variable Change 事件模式

---

## 风险与版本注意

- **SDK 版本依赖**:Prefabs 与程序源文件结构可能随 SDK 版本变化,**以实际 Packages/com.vrchat.worlds/Samples/UdonExampleScene/ 为准**
- **Udon Graph 限制**:本场景部分程序仅提供 Udon Graph 版本,无 UdonSharp 等价实现(如 `VRCWorldSettings`);部分有两者(参见 [player-mod-setter.md](player-mod-setter.md))
- **World Audio Settings**:**当前不在 SDK 示例场景中**(详见 [world-audio-settings.md](world-audio-settings.md))
