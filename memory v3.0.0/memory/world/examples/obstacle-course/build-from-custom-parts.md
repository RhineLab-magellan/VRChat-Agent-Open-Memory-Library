---
title: "Obstacle Course: Build From Custom Parts(自定义预制件)"
category: world
subcategory: examples
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - event
  - udonsharp
aliases:
  - "Obstacle Course： Build From Custom Parts(自定义预制件)"
  - "Obstacle Course: Build From Custom Parts(自定义预制件)"
related:
  - build-from-demo-parts.md
  - uoc-flythrough.md
  - uoc-window.md
  - uoc-how-stuff-works.md
  - "../persistence/post-processing-settings.md"
---
# Obstacle Course: Build From Custom Parts(自定义预制件)

> **Domain**: World
> **来源**: VRChat Creator Docs — https://creators.vrchat.com/worlds/examples/obstacle-course/build-from-custom-parts/
> **本地化日期**: 2026-06-15
> **文档原始更新**: 2023-06-20

---

## 前置说明

> **强烈建议**:先用 Demo 预制件跑通简单 Remix,再开始自定义。
> 详见 [Build From Demo Parts](./build-from-demo-parts.md)。

---

## 核心模式:Trigger Collider + 程序分发

**所有可与玩家交互的对象**(Checkpoint、PowerUp、Hazard、Respawner 等)都遵循 **统一模式**:

```
Trigger Collider (Layer = CourseTrigger, isTrigger = true)
    ↓ OnPlayerDataEnter 程序
    ↓ 查找 PlayerData 引用
    ↓ Instantiate FX Prefab
    ↓ 触发目标 UdonBehaviour 上的指定 Event
    ↓ 可选:deactivate 自身
目标 UdonBehaviour (Checkpoint / PowerUp / Hazard / ...)
```

**自定义 Layer 设置**:
- **`CourseTrigger`**:所有 Trigger Collider 必须放这一层
- **`CoursePlayer`**:PlayerObject 预制件所在的层
- 物理上只允许 `CoursePlayer` 与 `CourseTrigger` 之间发生碰撞事件

---

## 自定义 Checkpoint

### Checkpoint 预制件结构

```
Checkpoint.prefab
├── 视觉表现 (Mesh, Particles, etc.)
├── Trigger       (GameObject + Collider[CourseTrigger, isTrigger=true] + OnPlayerDataEnter)
└── UdonProgram   (UdonBehaviour + Checkpoint program)
```

### Trigger 必要变量(UdonBehaviour)

| 变量 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `fxPrefab` | GameObject | 否 | 触发时 Instantiate 的特效/音效预制件;**不填则跳过特效**;通常配合 `DestroyAfterXSeconds` 程序避免泄漏 |
| `program` | UdonBehaviour | 是 | 目标脚本引用,通常是同 Prefab 的子对象的 Checkpoint 程序 |
| `eventName` | string | 是 | 要调用的 Event 名(StartRace / Trigger / FinishRace) |
| `deactivateOnTrigger` | bool | 是 | Checkpoint 必须为 true —— 每局只能触发一次 |
| `sendPlayerData` | bool | 仅 StartGate | 是否传递 PlayerData 引用 |

### Checkpoint 程序(子对象上的 UdonBehaviour)

只要把 **`Checkpoint` 程序** 放到子对象上即可。所有变量在 Toolkit 放置时自动设置,运行时 `Trigger` 事件被调用时也会自动更新。

### Start Gate 配置

| 字段 | 值 |
|------|---|
| `eventName` | `"StartRace"` |
| `sendPlayerData` | **true** |

### Finish Gate 配置

| 字段 | 值 |
|------|---|
| `eventName` | `"FinishRace"` |

### 隐藏 Collider 时的行为

- 触发后 `deactivateOnTrigger=true` → **整个 Trigger Collider 所在 GameObject 设为 inactive**
- 想隐藏整个 Checkpoint:把 Collider 放最外层
- 想只隐藏部分:把要隐藏的子对象作为 Trigger Collider 的子对象

### Course Reset 行为

当 `Course.Reset()` 被调用(玩家完成跑道 / 通过菜单 Respawn):
- 遍历所有 Checkpoint
- 找到所有 Trigger Collider,`SetActive(true)` 给 index=0(Start Gate),其他 `SetActive(false)`
- 也就是说 **所有 isTrigger=true 的 Collider 所在 GameObject 都会受这个流程影响** —— 避免在 Prefab 上放额外的 `isTrigger=true` Collider

### 添加到 Toolkit 列表

把自定义 Prefab 拖到 Toolkit 窗口的 **Checkpoint Prefabs** 列表(可调整 Size)。

---

## 自定义 PowerUp

### PowerUp 程序必要变量

```
PowerUp (UdonBehaviour)
├── playerModsManager  // 自动注入,不要手动设
├── speedChange        // 浮点;0 跳过;正加/负减
├── jumpChange         // 浮点;0 跳过;正加/负减
├── effectDuration     // 浮点;>0;持续秒数
```

### 关键规则

- **`speedChange` 或 `jumpChange` 至少一个非 0**(否则 PowerUp 不会触发效果)
- 正值 → 加到 Toolkit 中设置的 `Move Power` / `Jump Impulse` 默认值
- 负值 → 减去默认值
- **可叠加**:Speed + Jump 同时修改,例如"跳得高但走超慢"的 PowerUp 完全合法
- **`effectDuration` 必须 > 0**(不接受负数) —— HUD 上的提示会按这个时间淡出

### PlayerModsManager 内部逻辑(关键)

> **重要的可取消设计**:`PlayerModsManager` 使用**队列 + 同类相消**策略。
>
> 例:玩家先吃 `Speed +3` 持续 2s,再吃 `Speed -1` 持续 3s:
> 1. 第一颗触发 → 当前速度 = `Move Power + 3`,倒计时 2s
> 2. 1s 后吃到第二颗 → **取消 Speed mod** → 当前速度 = `Move Power - 1`,倒计时 3s
> 3. 2s 后第一颗到期 → 不再生效(已被取代)
> 4. 3s 后第二颗到期 → 当前速度 = `Move Power`(默认)
>
> **设计意图**:实现"刷新计时器"效果,而非简单叠加。**Speed 与 Jump 互不影响**(独立队列)。

### 添加到 Toolkit 列表

拖到 **PowerUp Prefabs** 列表。

---

## 自定义 Hazard

Hazard 也使用 Trigger Collider 模式(同 Checkpoint)。

### Respawn Hazard(RespawnOnCourse 程序)

```
Hazard.prefab
├── 视觉表现
└── Trigger (Collider + OnPlayerDataEnter → 调用 program.Trigger)
    └── UdonProgram (UdonBehaviour + RespawnOnCourse)
```

- `course` 变量会被 Toolkit Refresh 时自动注入(指向 `CourseManager` UdonBehaviour)
- 触发时把玩家传送到最近 Checkpoint 的 Transform 位置

### Spawned Hazard(双层程序)

**适用场景**:移动/定时生成的障碍(如滚木、飞弹)。

**两部分**:
1. **HazardSpawner**(放置在场景中) — 定时生成 Hazard 实例
2. **SpawnedHazard**(被生成的 Prefab) — 触发时给玩家减速

#### HazardSpawner 必要变量

| 变量 | 说明 |
|------|------|
| `prefab` | 要生成的 Hazard 预制件 |
| `delay` | 生成间隔(秒) |
| `playerModsManager` | 自动注入;会传给 SpawnedHazard |

**逻辑**:每 `delay` 秒 `Instantiate(prefab)` → 找到新对象上的 UdonBehaviour → 设置 `playerModsManager` 引用。

#### SpawnedHazard 必要变量

| 变量 | 说明 |
|------|------|
| `lifeDuration` | 自动销毁时间(避免无玩家时堆积) |
| `playerModsManager` | 由 HazardSpawner 设置 |
| `speedChange` | **Vector2**;`x` = 速度偏移量,`y` = 持续时间 |

**示例**:设置 `(-3, 3)` 表示"减速 3,持续 3 秒"。

> **【未确认】**:SpawnedHazard 用 `GameObject.Find` 找 PlayerModsManager ——"不 performant 但能用"。

### ⚠️ 必须 Unpack Hazard 预制件

Hazard 预制件**不是**通过 Toolkit 窗口管理的,因此放置后必须 **Unpack**,否则自动注入的 `playerModsManager` 引用可能丢失。

---

## 其他自定义项

### Score Fields

- 复制 `ScoreField` 预制件 → 改外观
- 拖到 Toolkit 窗口 **Score Object Prefab** 槽
- 设置 **Number of Scores to Show** 自动重新生成 UI

### HUD

直接修改 `HUD` 对象的层级结构即可,无需代码改动。

### Minimap

- 找到 `MinimapCameraSystem/VCam-Follow` 上的 `CinemachineVirtualCamera`
- `Follow` / `LookAt` 在运行时设置
- **测试技巧**:在 Editor 中拖一个 Capsule 给 VCam 当目标,拖动它可即时看到 Minimap 效果

### Advanced:扩展 Variable to Scene Object Lookup

在 Project 窗口点击 Course Asset → **Variable to Scene Object Lookup** 区域:

- **左侧**:变量名
- **右侧**:场景中对象的名称(Component 会自动找)

**当前支持的 Component 类型**:
- `GameObject`
- `UdonBehaviour`
- `CinemachineVirtualCamera`

**扩展方法**:修改 `ObstacleCourseEditorWindow` 类的 `InjectVariableReferences` 方法,在 if-chain 中添加新类型。**写得好可向官方提 PR**。

> **设计意图**:用 **命名约定** 替代 **手动拖拽引用** — Toolkit Refresh 时通过名字自动查找并注入,实现 Prefab 完全可序列化。

---

## 自定义对象 Checklist

| 自定义类型 | 必填程序 | 关键变量 |
|-----------|---------|---------|
| Checkpoint | `OnPlayerDataEnter` + `Checkpoint` | `program`, `eventName`, `deactivateOnTrigger` |
| PowerUp | `OnPlayerDataEnter` + `PowerUp` | `speedChange` / `jumpChange`, `effectDuration` |
| Respawn Hazard | `OnPlayerDataEnter` + `RespawnOnCourse` | `course`(自动注入) |
| Spawned Hazard | `HazardSpawner` + `SpawnedHazard` | `prefab`, `delay`, `lifeDuration` |
| Falling Block | `FallingBlock` | `triggerTime`, `resetTime` |
| Auto Rotate | `Autorotate` | `amount` (Vector3) |

---

**最后验证日期**:2026-06-15
