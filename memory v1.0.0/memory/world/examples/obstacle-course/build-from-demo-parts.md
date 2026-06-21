# Obstacle Course: Build From Demo Parts(基于预制件构建)

> **Domain**: World
> **来源**: VRChat Creator Docs — https://creators.vrchat.com/worlds/examples/obstacle-course/build-from-demo-parts
> **本地化日期**: 2026-06-15
> **文档原始更新**: 2024-10-28

---

## 前置说明

> **强烈建议**:先用 Demo 预制件 + Starter Scene 跑通一个简单 Remix,再尝试 Build From Custom Parts。
> 原文链接: [Build From Demo Parts](./build-from-demo-parts.md)

---

## Open Starter Scene

最快上手方式:**打开 `Assets/_WorldJam2/Scenes/Starter.unity`**

---

## Make your own Folder(避免更新覆盖)

**重要工程实践**:把你自己的所有内容放在 `_WorldJam2` 文件夹 **外**,这样从 GitHub Pull 新版本时不会覆盖你的工作。

- 推荐做法:在 `Assets/` 下新建一个独立文件夹,例如 `_MyProject`
- 命名约定:用下划线开头(如 `_MyProject`),使其在按字母顺序排列时排在顶部

---

## Make New Course Asset

`ObstacleCourseAsset` 是一个 ScriptableObject,持有以下信息:
- Checkpoints 列表
- Player Prefab
- Score Display 配置
- PowerUps 列表
- 默认速度/跳跃值

**步骤**:
1. 在 **Project** 窗口定位到 `_WorldJam2/Courses/StarterCourse.asset`
2. **Duplicate** 该 Asset
3. 重命名为自定义名称(如 `MyCourse.asset`),移到你的 `_MyProject` 文件夹
4. 在 Hierarchy 中选中 `Udon/CourseManager/CourseManager`
5. 把新建的 Course Asset **拖拽**到 `CourseManager` 上 `Obstacle Course Data` 脚本的 `Asset` 字段

**结果**:从此 Toolkit 窗口的所有修改会保存到你的自定义 Course,而不是 Starter。

---

## Add Course Pieces(添加赛道部件)

**预制件位置**:`Assets/_WorldJam2/Prefabs/Course Pieces`

**操作**:
1. 直接 **拖拽** 部件到 Scene View
2. 按住 **CTRL** 拖拽可启用 **Grid Snapping**(网格对齐)

> **重要**:如果部件带 Udon,先 **Unpack Prefab**(右键 → Unpack Prefab),否则:
> - 你可能改不动它的内部参数
> - 后续 Pull 新版 Jam 包时会覆盖你的修改
> - **【推断】**:`Udon` 字段引用的是包内原始预制件,Unpack 后可解除引用
>
> **Grid Snapping 进阶**:Unity 内置多种对齐模式,详见 [Unity Manual: Grid Snapping](https://docs.unity3d.com/2022.3/Documentation/Manual/GridSnapping.html)

---

## Add Checkpoints(添加检查点)

Start Gate、Mid Checkpoint、Finish Gate 应通过 Toolkit 窗口添加,不要手动拖。

**步骤**:
1. 菜单栏 → `⏵Obstacle Jam Utilities` → `Open Window`
2. 从 **Checkpoint Prefabs** 列表选择一个预制件
3. **鼠标移到 Scene View** → 会出现选中预制件的预览(会自动尝试吸附到所指表面)
4. **按 Space 键** 确认放置,自动接线

> **【推断】**:Space 键的确认是 Toolkit 的特殊 Input,不同于普通 GameObject 创建——它会触发 `InjectVariableReferences` 自动注入 CourseManager 引用。

放置后,新的 Checkpoint 会自动出现在 **Checkpoints In Scene** 列表中。选中某个 Checkpoint 可在 Scene View 中定位它,Hierarchy 选中 `UdonProgram` 子对象可看到 `index` 已被自动设置为正确顺序。

---

## Add PowerUps(添加 PowerUp)

**步骤**:
1. 打开 Toolkit 窗口
2. **Power Ups** 区域 → **Power Up Prefabs** 列表
3. 选择一个预制件 → 移动到 Scene View → **Space** 确认
4. 在 **Power Ups In Scene** 区域调整每个 PowerUp 的 `speedChange` / `jumpChange` / `effectDuration`

> **【未确认】**:Demo 提供的 PowerUp 类型详细列表(Speed Up、Jump Boost、Speed Down 等)需打开项目后查看 `Assets/_WorldJam2/Prefabs/PowerUps/`。

---

## Add Hazards(添加障碍物)

**步骤**:
1. 从 `Assets/_WorldJam2/Prefabs/Hazards/` 拖拽 Hazard 到场景
2. 同样建议先 **Unpack** 后再修改

Hazard 类型(见 [Build From Custom Parts](./build-from-custom-parts.md)):
- **RespawnOnCourse** — 触碰后传送回最近 Checkpoint
- **SpawnedHazard + HazardSpawner** — 定时生成移动障碍
- **FallingBlock** — 玩家踩上去后定时掉落
- **Autorotate** — 简单持续旋转

---

## 工程要点小结

| 要点 | 说明 |
|------|------|
| **不修改 `_WorldJam2/` 内任何文件** | 保持可升级性;所有定制放入 `_MyProject/` |
| **先 Duplicate Course Asset** | 避免污染 Starter 默认值 |
| **Unpack 所有带 Udon 的预制件** | 否则后续 Package 更新会覆盖 |
| **用 Toolkit 窗口放置** | 自动注入引用,手动拖拽会丢失 `InjectVariableReferences` |
| **Grid Snapping 加速** | 拖拽时按 CTRL |
| **Hub / Minimap / Score Field** | 可复制 `ScoreField` 预制件并修改外观,拖入 **Score Object Prefab** 槽 |

---

**最后验证日期**:2026-06-15
