---
title: "Avatar 参数分步同步架构"
category: avatar
knowledge_level: applied
status: active
source: "VRCD 文档库 — LIII Works（酒保K）"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - avatar
  - playable-layer
  - sync
aliases:
  - "Avatar 参数分步同步架构"
  - avatar-parameter-staged-sync
related:
  - modular-avatar.md
  - playable-layers.md
  - accessories.md
  - animator-system.md
  - avatar-dynamic-bone-limits.md
---
# Avatar 参数分步同步架构


---

## 概述

**分步同步**是一种用于大幅减少 Synced Parameter Bit 消耗的主动系统，以容纳超过 256 bit 的同步参数。

### 核心思想
将参数同步从**同时**拆分为**多次**，在一段时间内**分批完成**，用时间换空间。

### 背包比喻
- 同时同步：一次性背上所有物品
- 分步同步：去上学装课本、去登山装食物、去旅行装地图
- 每次只用一个同步容器，分批传递所有参数

---

## 核心约束

### VRChat 参数同步限制
| 类型 | 占用 | 说明 |
|---|---|---|
| **Bool** | 1 bit | - |
| **Int/Float** | 8 bit | - |
| **总计上限** | 256 bit | 每个 Avatar |

### 同步间隔与延迟
| 参数 | 值 | 说明 |
|---|---|---|
| **Sync Interval** | 0.2s | 每 0.2 秒发起一次同步 |
| **Latency** | 0.1 ~ 1.0s | 抵达远端时间 |

---

## 同步类型（VRChat 官方）

| 类型 | 用途 | 更新频率 | 延迟 |
|---|---|---|---|
| **Speech** | Viseme（唇形同步） | 本地计算 | 无显著延迟 |
| **Playable** | 一般参数 | 每 0.1-1s | ~0.2s |
| **IK** | 频繁变化值 | 每 0.1s | 低 |

---

## 核心公式

### Bit 节省公式
```
节省 Bit = (N - ceil(N / Steps)) × BitPerParam
```
- N = 参数数量
- Steps = 同步步骤数
- BitPerParam = 每参数 bit 数（Bool=1, Int/Float=8）

**示例**: 10 个 Int，4 步同步
- 原始: `10 × 8 = 80 bit`
- 分步后: `ceil(10/4) × 8 = 24 bit`
- 节省: `56 bit`

### 延迟公式
```
Delay = Steps × 0.2s
```
**示例**: 4 步 = 0.8s 延迟

### 容器数量公式
```
Containers = ceil(ParamCount / Steps)
```
**示例**: 10 个 Int，4 步 = 3 个容器

---

## 架构组件

### 组件概述
```
┌─────────────────────────────────────────────────────────────┐
│                    分步同步架构                              │
├─────────────────────────────────────────────────────────────┤
│  远端区分 → 判断本地/远端，决定使用接收器或发射器            │
│                                                             │
│  发射器 ──→ 同步容器 + 时序标记 ──→ 接收器                  │
│    │              │                     │                  │
│    ↓              ↓                     ↓                  │
│  本地写入    每0.2s同步间隔      远端根据时序读取             │
└─────────────────────────────────────────────────────────────┘
```

### 远端区分
- **功能**: 区分 Avatar 由玩家穿着（本地）还是被观察（远端）
- **实现**: 使用 `IsLocal` 判断

### 发射器
- **功能**: 将本地参数值写入同步容器，设定同步时序
- **实现**: Parameter Driver (Set)
- **注意**: 每步骤间需间隔 0.2s

### 接收器
- **功能**: 根据时序标记，将同步容器内容写入对应参数
- **实现**: Parameter Driver (Copy)
- **注意**: 不需要关心 0.2s 间隔，不断尝试接收即可

### 同步容器
- **功能**: 承载要同步的参数数值
- **类型**: Bool / Int / Float
- **优化**: Int 和 Float 可互转，Float 精度 1/127，建议发送端转 Int，接收端逆转换

### 时序标记
- **功能**: 指示当前同步步骤
- **实现**: Bool 数组或 Int
- **位数计算**: `log2(Steps)`，超过7步用 Bool 更高效

#### 时序标记位数对照
| 步骤数 | 所需位数 | 备注 |
|---|---|---|
| 2步 | 1 bit | 2个状态 |
| 3-4步 | 2 bit | 4个状态 |
| 5-8步 | 3 bit | 8个状态 |
| 9+步 | 4+ bit | 用 Bool 效率更高 |

---

## 设计权衡

### 时间换空间
| 因素 | 说明 |
|---|---|
| **步骤越多** | 延迟越大，但 Bit 消耗越少 |
| **步骤越少** | 延迟越小，但容器数量增加 |

### 优化建议
- 根据功能延迟容忍度选择步骤数
- 高频交互功能 → 少步骤（2-3步）
- 低频功能 → 多步骤（4+步）
- 超过7步用 Bool 作为时序标记更高效

---

## Parameter Driver 参考

### 操作类型
| 操作 | 功能 | 约束 |
|---|---|---|
| **Set** | 设置指定值 | 无特殊限制 |
| **Add** | 添加值 | 建议仅本地运行 + 同步 |
| **Random** | 设为随机值 | 建议仅本地运行 + 同步 |
| **Copy** | 复制参数值 | 源：不能是 VRChat 内置参数；目标：必须在 Expression Parameters 中 |

### 数值范围限制
| 类型 | 范围 | 说明 |
|---|---|---|
| **Int** | [0, 255] | 同步限制 |
| **Float** | [-1, 1] | 同步限制 |
| **Float 精度** | 1/127 | 8 bit quantization |

### Local Only 选项
- 启用后仅在本地操作，不进行网络同步
- 可替代 `IsLocal` 判断的繁琐步骤

### 重要约束
- VRChat 内置参数（如 `GestureLeftWeight`）**不能**作为 Copy 的源参数
- 目标参数必须在 Expression Parameters 中才能同步
- 即使目标不在同步表中，Parameter Driver 仍可驱动（仅本地生效）

---

## 最佳实践

1. **分析功能延迟容忍度** — 确定合适的同步步骤数
2. **分组设计** — 将功能按更新频率分组，高频少量同步，低频多量同步
3. **时序标记优化** — 超过7步时使用 Bool 而非 Int
4. **精度管理** — Float 发送前转 Int，接收后逆转换保留最大精度
5. **测试验证** — 验证远端同步效果和延迟可接受性

---

## 相关资源

- [VRChat Animator Parameters 文档](https://creators.vrchat.com/avatars/animator-parameters/)
- [VRChat Avatar Parameter Driver](https://creators.vrchat.com/avatars/state-behaviors/#avatar-parameter-driver)