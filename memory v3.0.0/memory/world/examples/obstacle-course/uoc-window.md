---
title: "Obstacle Course Toolkit(Toolkit 窗口 / Editor 扩展)"
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
  - udonsharp
  - reference
aliases:
  - "Obstacle Course Toolkit(Toolkit 窗口 / Editor 扩展)"
  - uoc-window
related:
  - index.md
  - build-from-demo-parts.md
  - uoc-flythrough.md
  - build-from-custom-parts.md
  - uoc-how-stuff-works.md
---
# Obstacle Course Toolkit(Toolkit 窗口 / Editor 扩展)

> **Domain**: World
> **来源**: VRChat Creator Docs — https://creators.vrchat.com/worlds/examples/obstacle-course/uoc-window/
> **本地化日期**: 2026-06-15
> **文档原始更新**: 2023-05-18

---

## 概述

**Obstacle Course Toolkit** 是 VRChat 官方为 World Jam 2 编写的 **Unity Editor 扩展窗口**,集中管理 Jam 项目的所有特殊预制件、程序和参数。

**打开方式**:Unity 菜单栏 → `▶ Obstacle Course Toolkit` → `Open Window`

**注意**:某些文档中也写作 `⏵Obstacle Jam Utilities`(同一窗口的不同菜单名)。

---

## 窗口结构(5 大区域)

```
┌──────────────────────────────────────┐
│  Checkpoints                         │
│  ├─ Checkpoint Prefabs               │
│  └─ Checkpoints In Scene             │
│                                      │
│  Player Manager                      │
│  ├─ Player Object Prefab             │
│  └─ Number of Players                │
│                                      │
│  Score Manager                       │
│  ├─ Score Object Prefab              │
│  └─ Number of Scores to Show         │
│                                      │
│  Power Ups                           │
│  ├─ Power Up Prefabs                 │
│  └─ Power Ups In Scene               │
│                                      │
│  Defaults                            │
│  └─ (Move / Jump 默认值)             │
└──────────────────────────────────────┘
```

---

## Checkpoints 区域

### Checkpoint Prefabs(可用的 Checkpoint 预制件列表)

- 把想用的 Prefab 拖到列表中
- **Size** 字段控制列表长度
- 之后 Add Checkpoints 时可从列表选择

### Checkpoints In Scene(场景中已放置的 Checkpoint)

- 选中列表项 → Scene View 自动定位该 Checkpoint
- 可**重新排序**(同步重命名)
- 可**删除** Checkpoint
- **修改会同步更新 CourseManager 变量**

> **【推断】**:Reorder 会重新写入每个 Checkpoint 的 `index` 变量,确保 Course 知道触发顺序。

---

## Player Manager 区域

### Player Object Prefab

**默认**:Jam 包自带的 PlayerObject Prefab

**何时需要替换**:自己做了自定义 Player Object(需要承载 PlayerData 程序)

> **大多数创作者不需要改这个**。

### Number of Players(关键!)

**功能**:控制生成的 PlayerData 对象数量,自动填充 ObjectPool

| 设置 | 含义 |
|------|------|
| `Number of Players` = N | Toolkit 生成 N 个 PlayerData,ObjectPool 容量 = N |
| 玩家进入世界 | PlayerDataManager 从 Pool 取一个,赋予 Ownership |
| 玩家离开 | 归还 Pool |

> **⚠️ 重要工程约束**(详见 [index.md](./index.md#number-of-players玩家容量)):
>
> **VRChat Publish 时的 SDK Capacity 必须设为 `Number of Players / 2`**
>
> 例:Toolkit 设 8 → Publish 时 Capacity = 4

---

## Score Manager 区域

### Score Object Prefab

- 默认:Jam 自带的 ScoreField 预制件
- 自定义时:复制 + 修改外观 + 拖入此槽

### Number of Scores to Show

**功能**:生成指定数量的 ScoreField + 填充 ScoreManager 引用

> **与 Checkpoints In Scene 一样** —— 修改后会自动重新生成 UI 元素。

---

## Power Ups 区域

### Power Up Prefabs(可用的 PowerUp 预制件列表)

- 把自定义 PowerUp Prefab 拖到列表
- **Size** 字段控制长度

### Power Ups In Scene(场景中已放置的 PowerUp)

- 选中列表项 → Scene View 自动定位
- 可修改每个 PowerUp 的:
  - `speedChange`
  - `jumpChange`
  - `effectDuration`

**修改实时生效**(详见 [index.md](./index.md#powerup-properties已放置的-powerup-调整))

---

## Defaults 区域

**位置**:**Power Ups 区域下方**(不属于 Power Ups,是独立的 Defaults)

**字段**:**Move Power** 和 **Jump Impulse**(不是 VRCWorld 的字段,而是 Jam 包自定义)

**默认行为**:
- **Walk / Run / Strafe** 三个轴都使用相同 Move Power
- PowerUp 触发时,**三个轴一起**被 speedChange 偏移

> **设计含义**:策划平衡只需要调 1 个数值,不能做"加速跑但不能 Strafe"的效果。
> **如果需要**:直接改 `VRCWorld` 的 WalkSpeed / RunSpeed / StrafeSpeed(覆盖 Toolkit 默认值)。

---

## Refresh 机制(关键)

> **每次重要修改后必须按 Refresh** —— Toolkit 会:
> 1. 重建 ObjectPool(根据 Number of Players)
> 2. 重建 ScoreField 列表(根据 Number of Scores to Show)
> 3. 重新注入 Variable to Scene Object Lookup(按名字查找)
> 4. 同步 Checkpoint / PowerUp 的引用

**Refresh 触发点**:
- 显式按 `Refresh` 按钮
- 改变 `Number of Players` / `Number of Scores to Show` 时
- 添加 / 移除 Checkpoint / PowerUp 时

> **【未确认】**:Toolkit 是否对修改做实时检测自动 Refresh;建议每次大改后手动 Refresh。

---

## 与其他 Editor 工具的对比

| 工具 | 用途 | 文档 |
|------|------|------|
| **Obstacle Course Toolkit** | Jam 项目专用,集中管理 Checkpoint/PowerUp/Player 数量 | 本文档 |
| **Example Central** | 一站式获取 VRChat 官方示例项目 | `memory/sources/example-central.md` |
| **ClientSim** | Editor 内模拟 VRChat 客户端(无 VRChat 也能测试) | `memory/sources/clientsim.md` |
| **EasyQuestSwitch** | PC ↔ Quest 平台切换自动化 | `memory/platform/easyquestswitch.md` |
| **VRChat SDK Build Panel** | 通用 World/Avatar 上传 | (内建) |

**共同设计模式**:
- **Editor 窗口 + ScriptableObject 持久化**
- **Predefined List + Drag-and-Drop 槽位**
- **单按钮触发 Build / Refresh / Switch 等批量操作**

> **如果自己写 World Editor 工具**:可参考 Toolkit 的架构 —— `EditorWindow` + `ScriptableObject` 数据层 + `OnGUI` / UI Toolkit 表现层。

---

## 工程要点

| 要点 | 说明 |
|------|------|
| **打开窗口前确保场景有 CourseManager** | 否则部分操作无对象可管理 |
| **每次大改后按 Refresh** | 避免引用丢失 |
| **Number of Players 是 ObjectPool 容量,不是 Publish 容量** | Publish 时 SDK Capacity = N/2 |
| **Walk/Run/Strafe 三轴同速** | Jam 设计简化;自定义需绕过 |
| **Predefined List 而不是字符串输入** | 减少拼写错误,统一管理 Prefab |
| **Defaults 区是 Jam 内部字段** | 与 VRCWorld 字段独立;若需精细控制可手动改 VRCWorld |

---

## 风险与未确认项

| 风险/未确认 | 说明 |
|------------|------|
| **【未确认】** | 菜单名在不同版本可能略有差异(`▶ Obstacle Course Toolkit` vs `⏵Obstacle Jam Utilities`) |
| **【未确认】** | 关闭 Editor 后重新打开,是否需要手动 Refresh? |
| **【未确认】** | Toolkit 是否对 Package 版本有强依赖(低版本打开高版本项目可能失败) |
| **风险** | `Number of Players` 改大后忘记同步 Publish Capacity,导致玩家进入后无 PlayerData |
| **风险** | 自定义 Hazard(非通过 Toolkit 管理)未 Unpack,导致 Refresh 时引用丢失 |

---

**最后验证日期**:2026-06-15
