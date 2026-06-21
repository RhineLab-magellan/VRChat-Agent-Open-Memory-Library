---
title: Obstacle Course: How Stuff Works(内部机制详解)
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - serialization
  - ownership

aliases:
  - "Obstacle Course： How Stuff Works(内部机制详解)"

related:
  - build-from-custom-parts.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Obstacle Course: How Stuff Works(内部机制详解)

> **Domain**: World
> **来源**: VRChat Creator Docs — https://creators.vrchat.com/worlds/examples/obstacle-course/uoc-how-stuff-works/
> **本地化日期**: 2026-06-15
> **文档原始更新**: 2023-05-18

---

## 设计原则

> **Each system was designed to have a specific set of responsibilities, and to know about other systems as little as necessary.**

- **单一职责**:每个系统只负责一个清晰的功能域
- **低耦合**:系统间尽量少直接依赖
- **桥接模式**:`OnPlayerDataEnter` 是统一的 Trigger 分发桥

---

## 系统总览(Overview)

```
Player 进入世界
   ↓
PlayerDataManager: TryToSpawn(从 VRCObjectPool 取一个 PlayerData) → 赋予 Ownership
   ↓
PlayerData 进入 Start Gate Checkpoint
   ↓
Course: StartRace() → 记录 startTime, isRacing=true, nextIndex=1
   ↓
PlayerData 经过每个 Checkpoint
   ↓
Course: nextIndex 变化 → 激活下一 Checkpoint
   ↓
PlayerData 进入 Finish Gate
   ↓
Course: FinishRace() → 写入 timeElapsed → PlayerData.OnDeserialization → 所有人同步
   ↓
ScoreManager Owner: 处理新分数 → 同步给所有 ScoreField
   ↓
Reset (玩家 Respawn 或完成)
   ↓
回到初始状态
```

**PowerUp 流程**(并行):
```
PlayerData 碰到 PowerUp
   ↓
OnPlayerDataEnter.Trigger → PowerUp.Trigger()
   ↓
设置 PlayerModsManager.speedToProcess / jumpToProcess
   ↓
PlayerModsManager 启动定时器,到时恢复默认值
```

**Hazard 流程**(并行):
```
PlayerData 碰到 Hazard
   ↓
OnPlayerDataEnter.Trigger → RespawnOnCourse.Trigger() / SpawnedHazard.HitPlayer()
   ↓
传送回 Checkpoint / 触发 PlayerModsManager 减速效果
```

---

## Players(玩家管理)

### PlayerDataManager

**位置**:场景中 `Udon/PlayerDataManager` GameObject

**重要公开变量**:

| 变量 | 类型 | 用途 |
|------|------|------|
| `dataPool` | VRCObjectPool | 引用同对象上的 VRCObjectPool 组件;玩家加入时 `TryToSpawn` 一个 PlayerData 并给玩家所有权 |
| `followCam` | CinemachineVirtualCamera | 跟随玩家头顶的相机;设置好以便 Refresh 时把引用注入每个 PlayerData |

**`Number of Players` 行为**:Toolkit 中修改该值时:
1. 移除所有现有 PlayerData 对象
2. 添加新数量的 PlayerData 作为子对象
3. 自动设置每个 PlayerData 的 public 变量
4. 更新 ObjectPool 容量

> **工程意义**:这是 **动态 ObjectPool 重配** 的标准模式 —— 通过 Inspector 改 size,Refresh 时把 ObjectPool 重建为指定容量。

### PlayerObject Prefab

- 必备组件:**Rigidbody** + **Capsule Collider**
- **Layer**:`CoursePlayer`(只与 `CourseTrigger` 碰撞)
- 重要程序:`PlayerData`

> **Layer 设置的工程意义**:避免 PlayerObject 与世界中其他 Collider(地面、墙)发生物理交互,只响应 Trigger 事件。这是 **Layer-Based Collision Filtering** 模式。

### PlayerData

**核心程序**:所有玩家状态的中枢。

**变量详解**:

| 变量 | 类型 | 用途 |
|------|------|------|
| `timeElapsed` | `[UdonSynced] float` | 由 Course 写入;Owner 在 Scoreboard 显示自己的最新时间;ScoreManager Owner 收到变化后加入 Scoreboard |
| `isRacing` | `bool` | Course 在 StartRace 时置 true;FinishRace / 手动 Respawn / Course.Reset 时置 false |
| `rigidbody` | Rigidbody | Start 时缓存;每帧 Update 时同步到玩家位置和旋转(用 `Networking.GetOwner` 还是 LocalPlayer 的位置?) |
| `player` | VRCPlayerApi | 本地玩家的 VRCPlayerApi;在 `playerId` 变化时缓存;用于 `displayName` |
| `timeDisplay` | UdonBehaviour | 显示本地玩家最新时间的 UI |
| `scoreManager` | UdonBehaviour | ScoreManager 程序引用;Owner 收到 `timeElapsed` 变化时调用 `scoreToProcess` |
| `scoreManagerObject` | GameObject | ScoreManager 所在 GameObject(用于判断本地是否是 Owner) |
| `followCam` | CinemachineVirtualCamera | 跟随相机;`isRacing` 变化时切换 priority |

> **【推断】**:Rigidbody 同步通过直接 `transform.SetPositionAndRotation` 实现(非 Udon 物理同步),代价是 Collider 不会与场景交互(这是 design choice,避免 PlayerObject 卡墙)。

---

## OnPlayerDataEnter(统一桥接)

> **核心模式**:所有需要检测玩家进入的对象都使用此程序作为 Collider 的逻辑层。

**位置**:放任何需要"玩家进入触发"的对象的子对象上(Collider 必须 `isTrigger=true` 且 `Layer=CourseTrigger`)

**变量**:

| 变量 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `fxPrefab` | GameObject | 否 | Trigger 时 Instantiate 的特效;`null`/`self` 表示不生成 |
| `program` | UdonBehaviour | 是 | 目标脚本(Checkpoint / PowerUp / Hazard) |
| `eventName` | string | 是 | 调用的 Event 名 |
| `deactivateOnTrigger` | bool | 是 | 触发后 SetActive(false) |
| `lastCollider` | Collider | runtime | 缓存触发时的 Collider(用于回查 PlayerData) |
| `fxSpawn` | Transform | 否 | FX 生成位置;默认用 Collider 自己的 Transform(Finish Gate 可指向别处) |
| `sendPlayerData` | bool | 仅 StartGate | 是否传递 PlayerData 引用给目标程序 |

**Trigger 流程**:
1. PlayerData collider 进入 → 触发
2. 如果 `sendPlayerData=true` → 把 `playerData` 变量设到目标 program
3. 调用 `program.eventName`(StartRace / Trigger / FinishRace / HitPlayer 等)
4. 如果 `fxPrefab` 设置了 → Instantiate 并用 `fxSpawn` 设位置
5. 如果 `deactivateOnTrigger=true` → SetActive(false)

---

## Course & Checkpoints(核心)

### Course(主控制器)

**位置**:`Udon/CourseManager/CourseManager` 上的 `Course` 程序

**重要特性**:
- **没有任何 [UdonSynced] 变量** —— 只跟踪 **Local Player**
- 这是设计选择:每个客户端独立计算自己的时间,不需要同步

**生命周期**:

| Event | 行为 |
|-------|------|
| `Start()` | 调用 `Reset()` |
| `Reset()` | 关闭所有 Checkpoint(除 index=0 的 Start Gate);`nextIndex=-1`;`isRacing=false` |
| `StartRace()` | `startTime=当前时间`;`isRacing=true`;`nextIndex=1` |
| Checkpoint Triggered | Checkpoint 写入 `nextIndex = index + 1` → 触发 `nextIndexChange` 事件 → 激活下一 Checkpoint |
| `Update()` | 如果 `isRacing=true` → 计算 elapsed → 更新 `timeDisplay` 文本 |
| `FinishRace()` | `isRacing=false`;设置 PlayerData.`timeElapsed`;`playerData=null`;`resetDelay` 秒后 `Reset()` |
| `Respawn()` | 如果 `isRacing` → 传送到最近 Checkpoint;否则传送回世界初始 Spawn Point 附近 |

**Course.Reset 实现的细节**:
```csharp
// 伪代码(基于文档)
foreach (var checkpoint in checkpoints) {
    // 找到所有 isTrigger=true 的 Collider
    foreach (var col in checkpoint.GetComponentsInChildren<Collider>()) {
        if (col.isTrigger) {
            col.gameObject.SetActive(col == checkpoints[0]);  // 只激活 Start Gate
        }
    }
}
nextIndex = -1;
isRacing = false;
```

### ObstacleCourseData

**位置**:CourseManager 对象上的脚本(非 Udon)

**职责**:持有 `ObstacleCourseAsset` 引用。**Asset 由 Toolkit Window 加载**。

> **【重要】**:**创建你自己的 Asset**(Duplicate Starter),不要直接用 Starter —— 升级包时 Starter 会被覆盖。

### Checkpoint

**位置**:每个 Checkpoint Prefab 的子对象上的 `UdonBehaviour` + **Checkpoint program**

**3 个 Event**:
- `StartRace` → 设置 Course.`playerData` = 触发的 PlayerData,触发 Course 启动比赛
- `Trigger` → 设置 Course.`nextIndex` = `index + 1`
- `FinishRace` → 直接调 Course.`FinishRace()`

---

## Score(排行榜)

### ScoreManager

**位置**:`Udon/ScoreManager` 上的 `ScoreManager` 程序

**重要特性**:
- **没有任何 [UdonSynced] 变量**
- 依赖各个 `ScoreField` 来同步值
- **Number of Scores to Show** 字段在 Toolkit 中改变时,ScoreField 会被自动生成

**事件流**:

| Event | 行为 |
|-------|------|
| `Start()` | 调 `Render()` 一次 |
| `Render()` | 调 `scoreCam.Render()` 把当前 View 渲到 RenderTexture(用于 In-Game 展示) |
| `scoreToProcess` 变化(仅 Owner) | 调 `MakeRoom()` → `ProcessNextScore()` |
| `MakeRoom()` | 如果 ScoreField 都满了,迭代下移腾出空位 |
| `ProcessNextScore()` | 解析 displayName + time,设置到对应 ScoreField 的 `targetVarName`;对比 High Score 并可能更新;清空 `scoreToProcess`;对所有人发 `Render` 事件 |

**为什么是队列系统**:每个玩家跑完时都会触发 `timeElapsed` 变化 → 都需要处理;用队列保证不会丢失。

### ScoreField

**模式**:**`[UdonSynced] log` 变量变化时更新文本**

```csharp
// 伪代码
public override void OnDeserialization() {
    text.text = log;
}
```

**同步原理**:
1. ScoreManager.Owner 设置 `log` 字段
2. 自动 `RequestSerialization`
3. 所有客户端收到 → `OnDeserialization` 更新本地文本

> **【未确认】**:此模式使用 `[UdonSynced] string` 同步而非 `SendCustomNetworkEvent`,后者更精确但开销大;字符串同步实现简单但带宽占用较高。

### HighScoreField

同 ScoreField 模式,额外有:
- `[UdonSynced] float score` — 用于比较
- `prefix` 字符串(通常 `"High Score:"`)

---

## PowerUps(增益/减益)

### PowerUp 程序

**位置**:Toolkit Refresh 时自动作为 `PlayerModsManager` 的子对象创建

**变量**:

| 变量 | 说明 |
|------|------|
| `playerModsManager` | Toolkit Refresh 时自动注入 |
| `speedChange` | 浮点;0 跳过 |
| `jumpChange` | 浮点;0 跳过 |
| `effectDuration` | 秒;>0 |

**Trigger 流程**:
1. `OnPlayerDataEnter` 调 `program.Trigger()`
2. PowerUp 把 `speedToProcess` / `jumpToProcess` 设到 PlayerModsManager(打包为 Vector2: x=amount, y=duration)
3. PlayerModsManager 启动倒计时 + HUD 显示

### PlayerModsManager

**核心特性**:
- **Speed / Jump 独立队列**
- **同类相消** —— 新 PowerUp 取消同类旧 PowerUp 效果,重置计时
- 集中处理:不在 PowerUp 程序里直接改 `VRCPlayerApi.WalkSpeed`,统一在 PlayerModsManager 里改

**为什么不在 PowerUp 里直接改**:
1. **取消语义**:取消时需要知道当前值并重置
2. **HUD 显示**:统一在 PlayerModsManager 里画提示
3. **避免竞态**:多个 PowerUp 同时触发时,集中处理避免状态不一致

---

## 杂项程序

### DestroyAfterXSeconds

**用途**:FX Prefab 自动销毁(避免音效应粒子系统堆积)

**使用场景**:`fxPrefab` 实例化后挂在上面

### PlayClipFromArray

**用途**:随机播放一组 AudioClip(避免重复感)

**使用场景**:FX Prefab 上的音效组件

### Autorotate

**用途**:持续旋转 Transform

**变量**:`amount` (Vector3, 每轴旋转速度,乘以 Time.deltaTime)

> **【未确认】**:用 Udon 而非 Animator 的原因 —— 性能?快速迭代?纯简陋?

### SpawnedHazard

**变量**:
- `lifeDuration` — 销毁时间
- `playerModsManager` — 由 HazardSpawner 设置
- `speedChange` — Vector2(`x`=amount, `y`=duration)

> **【未确认】**:"用 `GameObject.Find` 找 PlayerModsManager —— 不 performant 但能用"。**风险**:Find 在大场景中昂贵。

### HazardSpawner

**逻辑**:`SendCustomEventDelayedSeconds` + `delay` 实现定时生成

**使用场景**:Demo 中的"滚木山"

### FallingBlock

**特殊**:**唯一** 不使用 `OnPlayerDataEnter` 的 Hazard 程序(因为需要 Enter + Exit 状态)

**逻辑**:
1. Player 进入 → 启动 `SendCustomEventDelayedSeconds(CheckForDrop, triggerTime)`
2. `CheckForDrop` → 如果 Player 还没退出 → 把 Rigidbody 设为 non-kinematic → 自由落体
3. `resetTime` 后调 `Reset`

---

## Injection(自动注入)

> **详细内容**:见 [Build From Custom Parts](./build-from-custom-parts.md#advanced扩展-variable-to-scene-object-lookup)

**核心机制**:
- Course Asset 持有 "Variable to Scene Object Lookup" 表
- Toolkit Refresh 时按名字在场景中查找并注入引用
- 避免手动拖拽引用 → Prefab 完全可序列化、可重定位

**支持类型**:`GameObject` / `UdonBehaviour` / `CinemachineVirtualCamera`

**扩展**:修改 `ObstacleCourseEditorWindow.InjectVariableReferences` 添加新类型

---

## 系统依赖图

```
Toolkit Window (Editor-only)
    └─> ObstacleCourseAsset
            └─> Course (Runtime)
                    ├─> PlayerData[]
                    │       └─> PlayerModsManager (Owner 共享)
                    ├─> Checkpoints[]
                    │       └─> OnPlayerDataEnter (每帧检测 PlayerData 进入)
                    └─> ScoreManager
                            └─> ScoreField[] / HighScoreField
```

**数据流向**:
- **下行**(`PlayerData → Course`):`OnPlayerDataEnter` 触发 `Trigger` 事件
- **上行**(`Course → PlayerData`):Course 写 `timeElapsed` 同步变量
- **广播**(`PlayerData → ScoreManager Owner`):`timeElapsed` 变化触发 Owner 处理

---

## 工程要点(供设计参考)

| 模式 | 应用场景 |
|------|---------|
| **VRCObjectPool + 动态重建** | 玩家数量可配的游戏 |
| **OnPlayerDataEnter 桥接** | 任何 Collider-Trigger 逻辑(避免重复 OnTriggerEnter 代码) |
| **同名查找 + 注入** | 避免拖引用;Prefab 可完全序列化 |
| **分数同步用 synced 变量** | 简单可靠;但带宽高,不适合高频数据 |
| **Effect Queue + 同类相消** | 任何 Buff/Debuff 系统(可推广到战斗游戏) |
| **Course 不同步状态** | 计时类游戏的设计原则:本地时间不需同步 |
| **FallingBlock 用 OnTriggerExit** | OnPlayerDataEnter 不支持 Exit 状态;特殊需求需特殊程序 |

---

**最后验证日期**:2026-06-15
