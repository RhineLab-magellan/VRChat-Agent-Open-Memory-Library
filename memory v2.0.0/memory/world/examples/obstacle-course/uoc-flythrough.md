---
title: Obstacle Course: Flythrough(预览相机 / 飞行通过)
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - udonsharp
  - reference

aliases:
  - "Obstacle Course： Flythrough(预览相机 / 飞行通过)"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Obstacle Course: Flythrough(预览相机 / 飞行通过)

> **Domain**: World
> **来源**: VRChat Creator Docs — https://creators.vrchat.com/worlds/examples/obstacle-course/uoc-flythrough/
> **本地化日期**: 2026-06-15
> **文档原始更新**: 2023-05-18

---

## 用途

Obstacle Course 包内置了 **Cinemachine 飞行通过(Flythrough)系统**,自动为你的赛道路径生成一条相机轨迹,可用于:

- 制作宣传视频
- 玩家预览赛道布局
- 高质量 In-Game 录制(进阶)

---

## Basic Setup

1. **拖入 Flythrough 预制件**:从 `Assets/_WorldJam2/_SubSystems/Flythrough` 拖到场景
2. **Toolkit Refresh**:Toolkit 窗口按 `Refresh` → 系统会扫描场景中所有 Checkpoint,自动生成路径
3. **查看生成的路径**:选中 `FlythroughPrefab/RecordCamPath` 即可在 Scene View 中看到路径
4. **播放预览**:Game View 按 `Play`,退出 Play Mode 前即可预览

---

## Modifying the Path

### 全局 Y 轴偏移

默认路径在每个 Checkpoint 起点 **上方 0.5 单位**。

修改:`VRC Obstacle Window` → **Recording** 区域 → `Record Path Y Offset`

- 在 label 上 **左右拖动** 可连续微调
- 调整后所有 Checkpoint 同步偏移

### 手动编辑 Waypoint

1. 关闭 `Auto Update Checkpoints`(Recording 区域)
2. 选中 `RecordCamPath`,在 Inspector 直接修改 waypoint 数字
3. 或:点击 Inspector 左侧的 waypoint 编号 → 在 Scene View 中用 Transform 工具移动

### 修改飞行速度

选中 `RecordCamTarget` → `Cinemachine Dolly Cart` 组件 → 修改 `Speed`:

- **默认**:Normalized Position Units,Speed = `0.03`(约 30 秒跑完)
- 增大 Speed → 飞行更快

---

## Recording the Output

### 方式 1:直接录屏(简单)

- 任何屏幕录制软件(OBS、Bandicam 等)直接录制 Game View
- 质量一般,够用

### 方式 2:Unity Recorder Package(高质量)

1. **Package Manager** 安装 **Unity Recorder**
2. 官方测试与本系统兼容
3. 详细使用:
   - [Unity Recorder 1.0 User Manual](https://unitytech.github.io/unity-recorder/manual/index.html)
   - [Working with Unity Recorder](https://learn.unity.com/tutorial/working-with-unity-recorder)

---

## Cleaning Up

> **⚠️ 发布前必须移除 Recorder 相关的所有 GameObject!**

- 删除 Flythrough Prefab 实例
- 删除任何测试用的 Capsule / Transform
- 检查 Hierarchy 中没有调试用的对象残留

> **【未确认】**:VRChat SDK Build 阶段是否自动检测并报错;建议手动删除避免 Publish 失败或性能问题。

**保存自定义路径**:对路径做了修改,可以把 Prefab 复制一份(右键 Duplicate)以备后用。

---

## Extra Credit(进阶玩法)

### 与现有 Cinemachine 系统集成

本项目已有 Cinemachine 用于 **Minimap 渲染** 和 **In-Game Jumbotron(大屏)**。可让 Flythrough 相机共享这些 VCam:

- **好处**:统一管理,切换路径时不影响其他相机
- **思路**:把 Flythrough 的 `CinemachineVirtualCamera` 添加到现有 `CinemachineBrain` 优先级队列

### 高质量 In-Game 录制

基于 Flythrough + Recorder Package 构建一个独立的"录制系统":
- 提供 UI 按钮开始/停止录制
- 录制到本地文件
- **【推断】**:In-Game 录制受限于 VRChat 沙箱权限,实际可行性需测试

---

## 工程要点

| 注意点 | 说明 |
|--------|------|
| **Flythrough 依赖 Cinemachine** | 不在包内,需要单独导入(VRChat 项目通常已带 Cinemachine) |
| **自动生成的路径基于 Checkpoint 顺序** | 调换 Checkpoint 顺序即改变路径 |
| **Y Offset 0.5 是经验值** | 不同赛道高度需调整 |
| **Dolly Cart vs Dolly Track** | 本系统用 Dolly Cart(基于 Waypoint 数组);非 Dolly Track(基于 Spline 曲线) |

---

**最后验证日期**:2026-06-15
