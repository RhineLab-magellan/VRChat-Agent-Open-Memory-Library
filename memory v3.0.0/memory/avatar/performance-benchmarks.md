---
title: "Unity/VRChat 性能基准测试"
category: avatar
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - avatar
  - animator
  - performance
aliases:
  - "Unity/VRChat 性能基准测试"
  - performance-benchmarks
related:
  - thry-avatar-evaluator-metrics.md
  - animator-system.md
  - avatar-dynamic-bone-limits.md
  - avatar-fallback-system.md
  - avatar-modding-guide.md
---
# Unity/VRChat 性能基准测试

> **来源**: VRCLibrary - Unity/VRChat Performance Benchmarks
> **原作者**: JustSleightly
> **翻译**: LIII Works 你亲爱的酒保K
> **翻译截止**: 2024-08-08
> **数据仓库**: https://github.com/jellejurre/UnityBenchmark
> **置信度**: High（权威基准测试，数据来自实测）

---

## 简介

### 测试方法论

收集数据的主要方法不是仅仅关注单个组件的性能，而是逐步添加更多组件，并从这些数据中推导出性能消耗的数学公式。

例如：如果想知道在FX控制器上增加一个额外的动画层会增加多少帧时间，可以设置1层、8层、64层和256层，绘制图表，将数据拟合成一条线，并利用这条线的公式来计算增加一个额外层所需的帧时间。

### 测试环境

- CPU: AMD Ryzen 7 5800X
- 内存: DDR4 2x16GB 3200 MHz CL18
- GPU: NVIDIA GeForce RTX 4090

---

## 帧时间预算

| 目标 FPS | 帧时间预算 | 说明 |
|---|---|---|
| 90 fps | **11 ms** | Quest 标准 |
| 60 fps | **16 ms** | PC 标准 |
| 40 fps | **25 ms** | 低性能设备 |

> 如果某个操作消耗了1毫秒，这约占90fps预算的**9.1%**。

---

## 动画控制器 (Animator Controllers)

### 测试说明

- 所有测试都没有包括任何状态行为(State Behaviour)。如果一个控制器的任何动画层上有一个或多个状态行为，所有控制器的运行时间会增加**50%**。
- 由于默认的Action & Gesture层中包含状态行为，这种额外开销可能会出现在每个使用的Avatar上。
- Animator Controller的性能**不会线性缩放**。两个拥有100个动画层的Avatar并不会比一个拥有200个动画层的头像更慢。

### 参考基准：双状态切换

| 场景 | 每增加1层的额外开销 |
|---|---|
| 被动切换（无主动切换） | **~0.01 ms** |
| 主动频繁切换 | **比被动高 20-30%** |

### AnyState 行为

| 配置 | 性能影响 |
|---|---|
| AnyState 切换数量 | **无显著影响** |
| 启用"可以过渡到自身" | **+20% 开销**（即使不切换也生效） |

### Direct Blend Trees 优化效果

| 设置方式 | 帧时间减少 | 说明 |
|---|---|---|
| 1D Blend Tree（多个子项） | **~75%** | 较慢但简单 |
| 默认动画层 + Direct BT | **~80%** | 比1D再减少50% |

> 除非是面部追踪等频繁切换场景，否则建议继续使用双状态设置。

### VRCFT 控制器对比（37个面部追踪参数）

| 控制器类型 | 帧时间 | 优化幅度 |
|---|---|---|
| 普通 VRCFT 控制器 | 0.1733 ms | — |
| VRCFTGenerator（Blend Tree版） | 0.066 ms | **-62%** |

### 其他发现

| 因素 | 影响 |
|---|---|
| 每层状态/过渡数量 | **无显著影响**（单状态>1000布尔过渡除外：1000个过渡需要1ms） |
| 人形/非人形骨架 vs 无Avatar | 每层帧时间 **减少 ~50%** |
| 遮罩 | **无显著影响** |
| 子状态机 | **无显著影响** |
| 嵌套 Blend Trees | **几乎无影响** |
| WD Off（Direct BT） | **无显著影响** |
| WD Off（动画层） | **帧时间 +50%** |
| 本地Avatar参数 | 每1000个参数 **+1.5 ms**（远程Avatar不适用） |

### 多控制器缩放关系

- **非线性**：2个100层控制器 < 1个200层控制器
- 1个100层 ≈ 10个30层的开销
- 所有控制器层数减半 → 总帧时间减少 **50%**

> 优化结论：**拆分大型控制器比合并更优**

---

## 约束 (Constraints)

### 性能数据

| 启用约束总数 | 帧时间 | 备注 |
|---|---|---|
| 1~680 | ~1.7 ms | 缓慢上升 |
| **681+** | **~2.4 ms** | 跃升41%，VRChat 限制设为681 |

### 禁用条件（约束不计入总数）

以下情况约束组件不计入总启用数：
- GameObject 被关闭 (Disabled)
- Constraint 组件被关闭 (Disabled)
- Constraint 设置为"关闭" (Disabled)

> ⚠️ 单纯将权重设置为0而不是上述的关闭，约束仍然会影响性能！

---

## 音源 (Audio Source)

| 测试项 | 帧时间影响 |
|---|---|
| Audio Source 数量 | **无法测出影响**（即使64个上限） |

> VRChat 每个角色限制 3 个

---

## 接触发射器/接收器 (Contacts)

### 性能数据

| 配置 | 每1000个 Contacts 的帧时间 |
|---|---|
| 关闭状态 | **0.5 ms** |
| 开启 Receivers | **0.75 ms**（+50%） |

### 注意事项

- 形状、类型、参数数量、碰撞标签 → **无显著差异**
- 本地Avatar参数 → **每1000个额外 +1.5 ms**
- **房间最大上限：4096 个 Contacts**（超出部分停止工作）

---

## 布料 (Cloth)

### 性能数据

| 顶点范围 | 每1000顶点帧时间 |
|---|---|
| ≤ 20万顶点 | **+0.2 ms** |
| > 20万顶点 | **急剧增加** |

### 注意事项

> ⚠️ 限制针对**整个房间**，非单个角色
> ⚠️ 本地Avatar的Cloth被模拟**3次**（Mirror + Shadow Clones），顶点需×3
> ⚠️ Colliders 使帧时间**翻倍**，每10个 Colliders 每个额外 **+7%**

---

## 物理骨骼 (PhysBones)

### 性能数据

| 因素 | 每1000个带顶点权重的骨头 |
|---|---|
| 主要成本 | **+2 ms** |

### 其他因素

| 因素 | 影响程度 |
|---|---|
| 层级结构（父子关系） | **轻微**（组件少时较好，极端情况差异33%） |
| Colliders 数量 | **非常微小** |
| 其他设置 | **无明显影响** |

> ⚠️ 数据来自 VRChat 内部测试（因 PhysBones 在 Unity/VRChat 中行为差异较大）

---

## 待测组件（后续计划）

- PhysBones/PhysBone colliders ✅ 已完成
- Skinned mesh renderers（材质数量与网格数量的关系）
- Lights
- Animations（数值/引用的影响，动画属性数量的影响）
- 不同类型的开关
- AAPs

---

## 快速参考表

### 帧时间消耗（每1000个实例）

| 组件 | 帧时间 | 备注 |
|---|---|---|
| 双状态切换动画层（被动） | ~10 ms | 每1000层 |
| 双状态切换动画层（主动） | ~12-13 ms | 每1000层 |
| Direct Blend Tree（1D） | ~2.5 ms | 每1000层 |
| Direct Blend Tree（双层） | ~2 ms | 每1000层 |
| Constraints（≤680） | 1.7 ms | 总计 |
| Constraints（681+） | 2.4 ms | 总计 |
| Contacts（关闭） | 0.5 ms | 每1000个 |
| Contacts（开启Receivers） | 0.75 ms | 每1000个 |
| Cloth（≤20万顶点） | 0.2 ms | 每1000顶点 |
| PhysBones | 2 ms | 每1000个带权重骨头 |