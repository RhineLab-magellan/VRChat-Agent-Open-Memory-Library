---
title: Avatar Animator System — Complete Guide
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - animator
  - udonsharp

aliases:
  - "动画器"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Avatar Animator System — Complete Guide

> 来源: VRCLibrary - Miscellaneous Avatar Knowledge (翻译版)
> 原文: https://notes.sleightly.dev/ | https://vrclibrary.com/wiki/books/miscellaneous-avatar-knowledge
> 译者: LIII Works / VRCD | 截止: 2024-09-05

---

## 1. Write Defaults（写入默认）

### 核心概念

Write Defaults 决定动画属性在**离开 Animator 状态后**是否保持更改。

| 设置 | 行为 |
|------|------|
| **WD On** | 离开状态时，属性返回到上传时的默认状态 |
| **WD Off** | 离开状态时，更改保持不变 |

**默认状态**：Avatar 上传时物体所处的状态（如缩放、启用状态）

### 核心规则（必须遵守）

> ⚠️ 违反这些规则会导致动画表现异常

1. **禁止同一控制器中混用 WD On/Off**
   - 例外：单 State 的 Direct Blend Tree 可单独使用任意 WD
   - 原因：播放单个 WD Off 状态会导致所有 WD On 状态无法写入默认值

2. **禁止 WD Off 的 Direct Blend Tree**
   - 会产生奇怪行为：影响其他 BT、输出被平滑化
   - 解决：使用 WD On，单 State 场景下安全

3. **WD Off 状态必须有填充动画**
   - 建议：空属性 + 至少 2 帧（约 0.0167 秒）
   - 原因：空状态可能用之前层的动画默认值覆盖之前动画

4. **Transform 动画会覆盖 Gesture 层**
   - FX 层用 WD Off 控制 Transform → 覆盖 Gesture 层所有 Transform
   - 解决：配合 Avatar Mask 使用

### 优点/缺点对比

| | Write Defaults On | Write Defaults Off |
|---|---|---|
| **优点** | 简单（可用空状态作 Buffer）<br>不覆盖 Gesture 层 Transform<br>2 状态切换帧时间少 33%（Unity 2019）<br>易修改默认状态 | 不依赖上传状态<br>可混用 WD（通常不受影响）<br>可使用序列操作 |
| **缺点** | 依赖上传状态<br>混用时出问题<br>无法使用序列操作 | 需要填充动画<br>覆盖 Gesture 层 Transform（无遮罩时）<br>2 状态切换帧时间多 50%（Unity 2019） |

### Blendshape 值翻三倍问题

**触发条件**：
- Additive 层为 WD Off
- 从空 WD On 状态过渡到 Blendshape WD On 状态

**解决方案**：
1. 每个状态都明确动画化 Blendshape 值（正确方法）
2. 将空闲层状态设为 WD On（快捷但不完善）

---

## 2. Avatar Mask（人形遮罩）

### Unity 行为

Avatar Mask 基于启用/禁用的选项，控制 Humanoid Muscle、材质球替换、Transform 动画：

| 遮罩设置 | 效果 |
|---|---|
| 启用 Humanoid Muscle | 该层可修改该 Humanoid 值 |
| 禁用 Humanoid Muscle | 该层不能修改该 Humanoid 值 |
| 启用/未指定 Transform | 该 Transform 可被动画修改位置/旋转/缩放 + 替换第一材质球 |
| 禁用 Transform | 该 Transform 不能被动画修改 |

**关键约束**：
- 有 Avatar Mask 的层 → 不能控制除第一个外的材质球
- 有 Avatar Mask 的层 → 不能控制 Animator 的根 Transform

### 为什么需要 Avatar Mask

- 动画层按顺序播放（下方层覆盖上方层）
- 如果你在 Gesture 层控制手部，FX 层也控制手部 → FX 覆盖 Gesture
- Transform 覆盖只在第二个动画使用 WD Off 且在稍后应用的层时发生

**示例**：FX 层控制面部表情（同时控制 Humanoid Muscle）→ 手部动作被覆盖

### Gesture 层特殊行为

VRChat 将第一层的 Avatar Mask 应用到其下所有动画层。如果某层遮罩禁用了 Humanoid 或 Transform，该属性无法被动画控制。

---

## 3. VRChat Playable Layers 行为

### 播放顺序（从上到下）

```
1. Base
2. Additive
3. Gesture
4. Action
5. FX（最后播放，优先级最高）
```

### 关键约束

> ⚠️ 前四层只在本地 Avatar 克隆体播放，VRChat 只复制 Transform 和 GameObject 开关状态到镜像/阴影克隆体

因此：
- Blendshape、材质替换、着色器动画等 → **必须在 FX 层**
- Base/Additive/Gesture/Action → **只控制 Transform 和物体开关**

### 各层详细说明

| 层 | 用途 | 内容限制 | 推荐 |
|---|---|---|---|
| **Base** | 运动（Humanoid Muscle） | Transform + GameObject 开关 | 仅 Humanoid Muscle |
| **Additive** | 运动调整（如呼吸） | Transform + GameObject 开关 | 仅 Humanoid Muscle，叠加方式 |
| **Gesture** | 手势 + 身体部分动画 | Transform + GameObject 开关 | Transform + 特定 Humanoid |
| **Action** | 覆盖前面 Humanoid（如表情） | Transform + GameObject 开关 | 权重从 0 开始，使用后归零 |
| **FX** | 所有其他动画 | 无限制 | 一切非 Transform 内容 |

### Action 层特殊说明

- 默认权重为 0
- 使用 `Playable Layer Control State Behavior` 将权重混合到有效值
- 完成后必须将权重调回 0，否则覆盖其他层

### FX 层特殊行为

- 第一层无 Avatar Mask → 创建默认遮罩（禁用所有 Humanoid + 启用所有 Transform）
- 第一层有 Avatar Mask → 应用到所有层
- 想要在 FX 控制 Humanoid → 制作专门遮罩并在最顶层设置
- VRChat 默认 FX 层有 WD Off 混合树，可能导致 Transform 动画问题

### 特殊层（独立，不受 Avatar Mask 影响）

| 层 | 用途 |
|---|---|
| **T-Pose** | 确定视点/视角球放置 |
| **IK Pose** | 确定关节弯曲方向（应略微弯曲） |
| **Sitting Pose** | 控制坐下姿势（覆盖 Humanoid 动画） |

---

## 4. Expression Parameter Mismatch（参数类型不一致）

### 兼容表格

#### Animator Bool →

| Expression | 结果 |
|---|---|
| Bool | Bool = False / True |
| Int | Int = 0 / 1 |
| Float | Float = 0.0 / 1.0 |

#### Animator Int →

| Expression | 结果 |
|---|---|
| Bool | Int > 0 → True |
| Int | 直接传递 |
| Float | 直接转换（如 2 → 2.0） |

#### Animator Float →

| Expression | 结果 |
|---|---|
| Bool | Float > 0 → True |
| Int | 四舍五入（≥0.5 → 1, <0.5 → 0） |
| Float | 直接传递 |

### 底层原理

- Unity Animator 后端使用 **Float** 处理参数
- VRChat 使用 **SBytes**（signed byte）代替 bool/int/float
- 参数不是"转换"，而是"不一致的兼容"

---

## 5. Direct Blend Tree（合并多动画层）

### 用途

将多个切换开关和转轮开关合并到**单层**，减少 Animator Layers 性能开销。

### 创建步骤

1. **创建 Blend Tree State**
   - 新建 Animator Layer → 右键创建 Blend Tree State
   - 设置 Write Defaults = **ON**（必要步骤）

2. **改为 Direct 类型**
   - 双击打开 → 检查器设置 Blend Type 为 `Direct`

3. **添加子项**
   - 添加新的 Blend Tree 子项
   - 创建 float 参数（如 `Weight`）设置为 1
   - 子项参数设为该 float（所有子项可共用）
   - **禁止勾选** `Normalized Blend Values`

4. **创建开关**
   - 子项 Blend Type 设为 `1D`
   - 创建 float 参数控制该子项
   - 添加动画（必须是独立动画，不能用 Motion Time 单动画）

5. **添加到 Expression Parameters**
   - 转轮开关 → `Float`
   - 切换开关 → `Bool`

### Write Defaults 处理

- 单 State 的 Direct BT 可安全使用 WD On
- 不受 Animator Controller 其他部分 WD Off 影响
- 名称前加 `WD On` 前缀可防止 VRLabs Avatar 3.0 Manager 批量修改时影响

### 嵌套技术

- 嵌套 Direct BT 模拟文件夹结构
- 每个文件夹是独立的 Direct BT
- 可在独立窗口中打开（大规模时性能友好）

### 当前限制

- 不支持动画切换（如溶解切换、Motion Time）
- 不支持驱动其他参数（排他性切换需 Parameter Driver）
- 首次运行时动画属性值可能在一帧内为 0

---

## 工具推荐

| 工具 | 用途 |
|---|---|
| [VRLabs Avatar 3.0 Manager](https://github.com/VRLabs/Avatars-3.0-Manager) | 检查 WD 混用、批量设置 WD |
| [AV3 Emulator](https://github.com/knob到来/VRC_Avatars_3.0_Emulator) | 模拟参数类型兼容 |
| [GestureManager](https://github.com/Black-Horse-Inc/GestureManager) | 模拟参数类型兼容 |

---

## 来源

- Write Defaults: https://notes.sleightly.dev/write-defaults/
- Avatar Mask: https://notes.sleightly.dev/animator-masks/
- Parameter Mismatch: https://notes.sleightly.dev/parameter-mismatching/
- Direct Blend Trees: https://notes.sleightly.dev/dbt-combining/
- 完整来源: https://vrclibrary.com/wiki/books/miscellaneous-avatar-knowledge
