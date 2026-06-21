# Obstacle Course(障碍赛 / World Jam 2)

> **Domain**: World
> **来源**: VRChat Creator Docs — https://creators.vrchat.com/worlds/examples/obstacle-course/
> **本地化日期**: 2026-06-15
> **文档原始更新**: 2024-10-28
> **官方 GitHub**: https://github.com/vrchat/VRChat-Obstacle-Jam
> **Release zip**: https://github.com/vrchat/VRChat-Obstacle-Jam/releases/download/1.0.3/obstacle-jam-public_v1.0.3.zip(最后验证:2026-06-15)
> **示例 World**: https://vrchat.com/home/world/wrld_39c422c4-ab87-4cc1-a4d1-390af2e45c74

---

## Overview

Obstacle Course 是 VRChat **第二次 World Jam(2021)** 的官方出品,作为 **Time Trial(计时赛)** 游戏世界的完整入门套件。

**设计目标**:让几乎零 Udon 经验的创作者也能通过拼接预制件快速构建一条可玩的障碍赛跑道,并能基于已有模型创建或导入自定义内容。

**核心模块**:

| 模块 | 职责 |
|------|------|
| **PlayerDataManager** | 为每个进入世界的玩家分配 `PlayerData` 对象(通过 `VRCObjectPool`) |
| **PlayerData** | 单个玩家的状态/进度/时间数据 |
| **Course / Checkpoint** | 时间追踪与检查点激活(Start / Mid / Finish Gate) |
| **PlayerModsManager** | 集中管理 PowerUp / Hazard 对玩家速度/跳跃的临时修改 |
| **PowerUp** | 加/减速、加/减跳跃力的拾取道具 |
| **Hazard** | 减速或使玩家 Respawn 的障碍物 |
| **Score / HighScore** | 同步排行榜与最佳成绩 |
| **OnPlayerDataEnter** | 统一的事件分发桥接程序(Trigger Collider 模式) |
| **Toolkit Window** | Unity Editor 扩展窗口,集中管理所有上述内容 |

**Demo Scene 路径**:`Assets/_WorldJam2/Scenes/DemoScene`

---

## Quick Start

1. **下载**:从 GitHub Release 下载 `obstacle-jam-public_v1.0.3.zip`(链接见顶部)
2. **打开场景**:`Build & Test` `Assets/_WorldJam2/Scenes/DemoScene`
3. **打开 Toolkit 窗口**:菜单栏 → `▶ Obstacle Course Toolkit` → `Open Window`
4. **修改默认值**:见下方的 Move & Jump、Number of Players、PowerUp Properties 三个段落

---

## Move & Jump(默认速度/跳跃)

在 Toolkit 窗口的 **Power Ups** 区域可修改 **Move Power** 和 **Jump Power** 的世界默认值。所有 PowerUp 的 speedChange / jumpChange 都是相对这些默认值的偏移量(正负值皆可)。

> **注意**:Walk / Run / Strafe 三个轴默认使用相同速度,玩家拾取 PowerUp 时三个轴一起偏移。
> **工程意义**:这是设计上的简化——避免策划平衡 3 个独立参数;劣势是玩家只能"全方向变快/变慢",无法做"加速跑但不能 Strafe"之类的精细效果。

---

## Number of Players(玩家容量)

**关键工程参数**(在 Toolkit 窗口的 **Player Manager** 区域设置):

| Toolkit 中设置 | Publish 时 SDK 容量限制应为 |
|----------------|----------------------------|
| `Number of Players` = N | **N / 2**(必须为该值一半) |

> **为什么是一半**:Number of Players = 实际 PlayerData 对象数量(每个进入世界的玩家占用一个 ObjectPool 实例);SDK Publish 的 Capacity 是同时能容纳多少个独立玩家(VRChat 实例 + 资源开销安全系数)。举例:Toolkit 设 8 → Publish 时设 4。
>
> **风险**:如果 Publish 容量设得与 Number of Players 一致,PlayerDataManager 的 `TryToSpawn` 会在实例满载时失败,玩家进入世界后无法获得 PlayerData,等同于无 PowerUp、无 Checkpoint 触发、无法计分。
>
> **【未确认】**:VRChat 内部是否对此比例有更严格规则;该比例为官方文档建议,实际应保留一定冗余。

---

## PowerUp Properties(已放置的 PowerUp 调整)

在 Toolkit 窗口 **Power Ups** 区域下的 **PowerUps in Scene** 列表:

1. **点击 PowerUp 名称** → Scene View 自动聚焦到该对象
2. 检视面板可修改:
   - `speedChange` — 速度偏移量(可为负)
   - `jumpChange` — 跳跃力偏移量(可为负)
   - `effectDuration` — 效果持续时间(秒,必须 > 0)

> **【推断】**:所有 PowerUp 的属性修改在 `OnRefresh` 时被 UtilityWindow 注入;如果直接在运行时改 Inspector,可能需要重新 Refresh 才能生效。

---

## 相关链接

- 父: [Obstacle Course](https://creators.vrchat.com/worlds/examples/obstacle-course/)
- 子:
  - [Build From Custom Parts](./build-from-custom-parts.md)
  - [Build From Demo Parts](./build-from-demo-parts.md)
  - [Flythrough(预览相机)](./uoc-flythrough.md)
  - [How Stuff Works(内部机制)](./uoc-how-stuff-works.md)
  - [Obstacle Course Toolkit(Editor 窗口)](./uoc-window.md)

---

## 与已有知识库的关系

- **World 项目结构参考**:World Jam 是官方工程模板,可作为大型 World 项目的目录结构参考(Assets/_WorldJam2/{Scenes, Prefabs, _SubSystems})
- **Editor 工具链对比**:Toolkit 窗口属于 Editor-only 工具,与 `memory/sources/example-central.md` 中的 Example Central、ClientSim 工具同属"VRChat 官方 Editor 工具"范式
- **Object Pool 模式**:PlayerDataManager 使用 `VRCObjectPool` 模式,建议在 `memory/patterns/` 考虑新增 `object-pool.md` 模式文档
- **Trigger Collider 模式**:`OnPlayerDataEnter` 程序 + 自定义 Layer(`CoursePlayer` / `CourseTrigger`)是值得提炼的设计模式

---

**最后验证日期**:2026-06-15
