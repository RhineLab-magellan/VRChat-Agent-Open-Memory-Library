---
title: Full-Body Tracking — 全身追踪完整指南
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - fbt
  - tracking
  - hybrid
  - rigging
  - experimental

aliases:
  - "FBT"
  - "Full Body Tracking"
  - "全身追踪"
  - "6 点追踪"

related:
  - "avatar/ik-2.0.md"
  - "world/udon/players/player-positions.md"
  - "platform/cross-platform-content.md"
  - "../FACT.md#多机位导演系统"

source: https://docs.vrchat.com/docs/full-body-tracking
source_type: community
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Full-Body Tracking — 全身追踪完整指南

> 来源: VRChat 官方文档 - Full-Body Tracking
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **关键 Insight**: FBT 是**实验性功能**,行为可能随版本改变。绑骨要求是创作者**最常踩坑**的点。

---

## 1. 概述

VRChat 支持使用 Lighthouse 生态追踪器(HTC Vive Tracker / Tundra Tracker 等)实现**全身追踪**。

### 1.1 支持的追踪点

最多 **8 个附加 tracker**(头显 + 控制器之外):

| 位置 | 备注 |
|------|------|
| **Feet(脚)** | 左右脚 |
| **Knees(膝)** | 左右膝 |
| **Hip(髋)** | 1 个 |
| **Chest(胸)** | 1 个 |
| **Elbows + Shoulders(肘+肩)** | **1 个 tracker 同时控制**(必须戴在肘**以上**) |

### 1.2 实验性状态

> ❗️ **Experimental Implementation**
>
> This system is **experimental** and is subject to change or overhaul that may deprecate or modify previous behavior!
> If you're using this system, pay close attention to updates to ensure you are adapting to new behavior and requirements.

**含义**:
- 当前为实验性功能
- 未来可能**大改**或**废弃**当前行为
- 使用者必须**关注版本更新**

### 1.3 不官方支持的方法

- Kinect 等替代硬件:用户自解决,VRChat 不官方支持
- VRChat Support 无法协助

---

## 2. SteamVR Tracker 配置(最佳实践)

### 2.1 为什么要在 SteamVR 预配置

避免追踪器和控制器混淆。

### 2.2 配置步骤

```
1. 启动 SteamVR(不带头显)
2. 开启所有追踪设备(控制器 + tracker)
3. SteamVR 窗口 → 菜单(三横) → Devices → Manage Vive Trackers
4. 弹出窗口中再点 "Manage Vive Trackers"
5. 在列表中给每个 tracker 分配:
   - Left Foot
   - Right Foot
   - Waist
6. 识别方法:长按其他 tracker 的按钮直到关闭,屏幕显示绿/红图标
7. 重复给其他 tracker 分配
```

### 2.3 命名建议

- 可物理标记 tracker(L/R Foot / Waist)
- 记录分配,避免混用

> 💡 **实际上**只要不分配为 "Held in Hand" 即可,但**正确分配更兼容其他应用**和 VRChat 未来变化

---

## 3. VRChat 中使用 FBT

### 3.1 启动 FBT 模式

启动 VRChat(已配对 tracker):
- 自动检测 FBT 模式
- Quick Menu 出现新选项

### 3.2 标准校准流程

```
1. Quick Menu → "Calibrate FBT" 按钮
   → 进入 Calibration Mode
   → Avatar 出现追踪点 sphere

2. Settings 菜单 → 高度设置正确
   ⚠️ 高度不对会导致脚穿过地面

3. Playspace 归零
   ⚠️ 不要用 OpenVR Advanced Settings 或 Playspace Mover 偏移

4. Avatar 附着(pinned)到 HMD
   - 视角永远正确(假设 SDK 设置正确)

5. 低头看脚 → 确保实际脚分开一个脚宽
   - 因为 avatar pinned 到 HMD,看脚下时腿会"沉"入地面(正常)

6. 检查 Hip tracker 位置是否合理

7. 如果用 Elbow/Shoulder tracker → 手臂与 avatar 手臂对齐
   - 即使不用这些 tracker,这步也有助于校准身体旋转

8. **抬头看正前方!** ⚠️
   - 低头时按 trigger 会导致视角偏
   - 不站直会影响与脚/髋的对齐

9. 双 Interact 按钮(通常 Trigger)**同时按**

10. 完成!
```

### 3.3 Legacy 校准(旧方法)

启动参数: `--legacy-fbt-calibrate`

```
1. VRChat 启动 → Calibration Mode
2. 与 avatar 对齐("内部")
3. 脚与 avatar 脚对齐(腿长 avatar 可能脚在胫骨上,正常)
4. Hip tracker 与自己髋部对齐
5. 如用 Elbow/Shoulder → 手臂对齐
6. 抬头看正前方
7. 双 Trigger 同时按
```

---

## 4. ⚠️ Rigging 要求(CRITICAL)

### 4.1 术语表

| 术语 | 含义 |
|------|------|
| **Bone Head** | 骨骼位置(Blender 等 3D 软件有 Head/Tail 概念) |
| **IK-driven Bone** | 在 Mechanim Rigging 中映射的骨骼 |
| **Bone Roll** | 骨骼沿局部 Y 轴(上下)的旋转 |

### 4.2 FBT 最佳绑骨要求

| # | 要求 | 说明 |
|---|------|------|
| 1 | **比例接近真实人类** | 避免"手臂拉扯"和"高跷"现象 |
| 2 | **脊椎不要突然弯曲** | IK 会试图拉直,弯曲会被消除 |
| 3 | **IK-driven 骨骼 Roll = 0** | 或全部相同值 |
| 4 | **不要"FBT 黑客"** | 翻转髋骨 / 额外腿骨 / 零长脖子 → 未来会破坏 |
| 5 | **用户身高正确** | 校准时不要蹲 |
| 6 | **Playspace 归零** | 不要用 Playspace Mover 偏移 |
| 7 | **骨骼距离 > 0** | 不要堆叠骨骼,特别是 `Hip > Spine > Chest > Neck > Head` 链 |
| 8 | **髋骨底部 > 大腿骨顶部** | 防止髋骨"翻起" |
| 9 | **膝/肘轻微弯曲** | 膝向前、肘向后 |
| 10 | **不要内/外八字** | 正面看腿不能弯 |

### 4.3 Bone Roll 说明

> 📘 Keep in mind that Unity does not care about the "tail" or "length" of a bone as described in Blender and other 3D software, aside from using it to determine the rotation of the bone transform.

**关键 Insight**:
- Unity **不关心**骨骼 Tail/Length
- 仅用 Tail 确定 Transform 旋转
- Bone Roll 只要**一致**(全部为 0 或全部相同值)即可

### 4.4 校准困难:viewpoint 对齐

如果脚/髋比例不对,校准时 viewpoint 难以对齐
- `Legs > Hips > Spine > Chest > Neck > Head` 链比例影响大
- 极端比例会导致问题

---

## 5. Avatars 3.0 集成

### 5.1 Use Auto Footstep

- **默认开**
- 仅适用于 3-4 点追踪
- 关闭 = 禁用程序化下半身动画(room-scale 移动时)

**保持开启**:
- 仍可通过 Tracking Control state behavior 启用/禁用追踪

**关闭**:
- 腿/髋的追踪启用/禁用**无效果**
- 完全依赖 animation 驱动下半身

### 5.2 Force Locomotion Animations

- **默认开**
- 仅适用于 6 点+ 追踪

**开启**: 移动摇杆时播放 walk/run 动画(类似 Live 模式)

**关闭**: 移动摇杆时**不**播放 walk/run 动画(适合用 FBT 动作"模拟"行走)

> ⚠️ **如果关闭 Locomotion Animations,不要用默认 Base 和 Additive 层**
> 你需要自己制作!

---

## 6. Rig 调优资源

- **Kung's guide**: https://www.youtube.com/watch?v=2sfTEBAl8sA(优秀 FBT Rig 修复指南)
- 部分修复针对 **Pre-IK 2.0 / Legacy IK**
- 任何标为 "RIG HACK" 的修复**不推荐**
  - 用了 → VRChat 未来调整时你的 avatar 会有问题

---

## 7. 与其他系统的关系

### 7.1 与 IK 2.0

- 详见 `memory/avatar/ik-2.0.md`
- IK 2.0 是 FBT 系统的**重大更新**
- Lock Types(Lock Hip/Head/Both)是新功能
- 启动参数 `--calibration-range` 等

### 7.2 与 Avatar Animator

- `player-positions.md` 提到 FBT 用户 `AvatarRoot` 不随头部旋转
- 需用 `GetRotation` 而非 `GetTrackingData(AvatarRoot).rotation`

### 7.3 与 Performance Rank

- FBT 本身不直接关联 Performance Rank
- 但 PhysBone / Particle 等可能因 FBT 启用而增加负载
- Performance Rank 仍然适用

---

## 8. 风险与陷阱

| 风险 | 等级 | 说明 |
|------|------|------|
| **实验性功能** | 🔴 高 | 行为可能大改,需关注更新 |
| **绑骨要求严格** | 🔴 高 | 不满足 → 严重问题(viewpoint、动画错乱) |
| **FBT 黑客** | 🔴 高 | 用了 → 未来一定会坏 |
| **不官方支持 Kinect** | 🟡 中 | 自行解决,无 Support 协助 |
| **Playspace 偏移** | 🟡 中 | 校准时偏移会导致严重问题 |
| **Legacy 校准** | 🟢 低 | 旧方法,但可能未来移除 |
| **Avatar 比例** | 🟡 中 | 极端比例导致"高跷"或 viewpoint 校准困难 |

---

## 9. 创作者清单(FBT Avatar)

```
□ Avatar 比例接近真实人类
□ 脊椎无突然弯曲
□ 所有 IK-driven 骨骼 Roll 一致(推荐 0)
□ 无 FBT 黑客(翻转髋骨、额外腿骨、零长脖子)
□ 骨骼距离 > 0(特别是 Hip > Spine > Chest > Neck > Head 链)
□ 髋骨底部 > 大腿骨顶部
□ 膝向前、肘向后轻微弯曲
□ 腿无内/外八字
□ User Height 设置正确
□ 校准时 Playspace 归零
□ Avatars 3.0:Use Auto Footstep 配置(默认开)
□ Avatars 3.0:Force Locomotion Animations 配置(默认开)
□ 关闭 Locomotion 时:自定义 Base/Additive 层
```

---

## 10. 相关文档

- `memory/avatar/ik-2.0.md` — IK 2.0(FBT 重大更新)
- `memory/world/udon/players/player-positions.md` — FBT 与 AvatarRoot
- `memory/platform/cross-platform-content.md` — 跨平台
- `memory/FACT.md §多机位导演系统` — FBT 在 World 中的应用

---

## 11. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/full-body-tracking
- **官方版本**: 已更新至 IK 2.0(2022.2.1+)
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)
