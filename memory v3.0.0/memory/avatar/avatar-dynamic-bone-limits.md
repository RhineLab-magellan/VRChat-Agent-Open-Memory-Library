---
title: Avatar Dynamic Bone Limits — 用户端 Dynamic Bone 限制系统
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - performance
  - physbone
  - config

aliases:
  - "Dynamic Bone Limits"
  - "DB 限制"
  - "Avatar 端 Dynamic Bone 限制"
  - "用户端 Dynamic Bone 限制"

related:
  - "avatar/performance-rank.md"
  - "avatar/optimization-guide.md"
  - "avatar/avatar-particle-system-limits.md"
  - "avatar/performance-benchmarks.md"

source: https://docs.vrchat.com/docs/avatar-dynamic-bone-limits
source_type: community
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Avatar Dynamic Bone Limits — 用户端 Dynamic Bone 限制系统

> 来源: VRChat 官方文档 - Avatar Dynamic Bone Limits
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **关键 Insight**: 这是**用户端**限制系统,与 **Performance Rank**(上传时等级)**不同**。

---

## 1. 概述

**Dynamic Bone Limits** 是 VRChat 客户端为**其他玩家的 Avatar** 设置 Dynamic Bone 数量上限的**可选系统**。

**目的**:
- 防止他人 Avatar 上的过多 Dynamic Bone 拖累你的客户端性能
- 玩家可选择性地启用/禁用/调整

**默认行为**:
- 限制值与 Performance Rank **Medium** 等级匹配
- 如果你的 Avatar 被 Performance Rank 标记为 Poor / Very Poor,默认情况下 Dynamic Bone 会被禁用

---

## 2. 启用 / 禁用系统

### 2.1 路径

```
Settings → Safety tab → "Performance Options" 按钮(右上角)
```

### 2.2 启用方法

- 弹出窗口显示当前选项
- 点击 **"Limit Dynamic Bone Usage"** 切换开启/关闭
- 关闭弹窗即应用(无需重新加载 Avatar)

### 2.3 系统性质

- ✅ **可选系统** - 单个复选框禁用
- ✅ **立即生效** - 无需重启

---

## 3. 默认值

| Value Name | Description | Default Value |
| :--------- | :---------- | :------------ |
| **Max Affected Transforms** | 单个 Avatar Dynamic Bone Affected Transforms 超过此值,**所有** Dynamic Bone + Dynamic Bone Collider 组件禁用 | **32** |
| **Max Collision Checks** | Dynamic Bone Collider Checks 超过此值,Dynamic Bone Collider 组件禁用 | **8** |

> 详细定义见 `memory/avatar/performance-rank.md` §PhysBone 部分

### 3.1 超限行为(CRITICAL)

如果 Avatar 超过限制值:

> "All related components snap to their 'initial position' are disabled."

**含义**:
- 整个 Avatar 的所有 Dynamic Bone **和** Dynamic Bone Collider 组件**被禁用**
- 不是只禁用部分超限的组件,而是全部禁用
- 回到 T-Pose 初始位置(无动态效果)

### 3.2 动画触发场景

如果 Avatar 通过动画**启用/禁用** Dynamic Bone 组件,使总数跨越阈值:

- 跨过上限(向上)→ 组件**停止更新**
- 跨过下限(向下)→ 组件**开始更新**

**示例**:
```
默认 30 Dynamic Bone → 工作正常
动画启用 5 个 → 35 个超过 32 → 全部 35 个都停止更新
```

---

## 4. 修改默认值

### 4.1 配置文件位置

```
%AppData%\..\LocalLow\VRChat\vrchat
```

实际路径(Windows):
- `C:\Users\<Username>\AppData\LocalLow\VRChat\vrchat\config.json`

如果文件不存在,手动创建 `config.json`。

### 4.2 ⚠️ 需重启

> **修改配置需要重启 VRChat 才生效。**

### 4.3 可修改变量

| 变量名 | 描述 | 默认 |
|--------|------|------|
| `dynamic_bone_max_affected_transform_count` | Dynamic Bone Transforms 上限 | 32 |
| `dynamic_bone_max_collider_check_count` | Dynamic Bone Collider Transform Checks 上限 | 8 |

### 4.4 设为 0 = 完全禁用

> 📘 **Disable Completely**
>
> Setting values to 0 will *remove all relevant Dynamic Bone components on all avatars* no matter the result of the component scan.

**含义**: 设 0 = 强制移除所有 Avatar 的所有 Dynamic Bone 组件(无论 Performance Rank 等级)

---

## 5. 配置文件示例

### 5.1 完全禁用 Dynamic Bone(忽略 Particle 设置)

```json
{
  "dynamic_bone_max_affected_transform_count" : 0,
  "dynamic_bone_max_collider_check_count" : 0
}
```

### 5.2 与 Particle Limits 合并的完整配置

```json
{
  "betas": [
    "particle_system_limiter"
  ],
  "ps_max_particles": 50000,
  "ps_max_systems": 200,
  "ps_max_emission": 5000,
  "ps_max_total_emission": 40000,
  "ps_mesh_particle_divider": 60,
  "ps_mesh_particle_poly_limit": 50000,
  "ps_collision_penalty_high": 50,
  "ps_collision_penalty_med": 30,
  "ps_collision_penalty_low": 10,
  "ps_trails_penalty": 10,
  "dynamic_bone_max_affected_transform_count": 0,
  "dynamic_bone_max_collider_check_count": 0
}
```

---

## 6. 与 Performance Rank 的关系

| 维度 | Performance Rank | Dynamic Bone Limits |
|------|-----------------|---------------------|
| **触发时机** | 上传时 SDK 评估 | 运行时客户端检查 |
| **检查方** | VRChat 后端 | 本地 VRChat 客户端 |
| **影响** | 影响 Minimum Performance Rank 设置 | 影响实际看到的 Dynamic Bone 行为 |
| **默认值匹配** | Medium 等级 | 32 / 8 (等同 Medium) |
| **可调整** | 创作者优化 Avatar | 用户修改 config.json |
| **Quest 行为** | 不同阈值(更严) | 同 PC 客户端配置(Quest 自己的) |

### 关键区分 ⚠️

> - **Performance Rank**: 上传时的等级标签,影响其他人 Minimum Performance Rank 设置
> - **Dynamic Bone Limits**: 运行时阈值,直接决定 Dynamic Bone 是否被禁用
> - 两者独立,但默认值匹配

---

## 7. 创作者建议

### 7.1 避免触发限制

- 设计 Avatar 时,Dynamic Bone Affected Transforms **< 32**(Medium 等级)
- Dynamic Bone Collider Checks **< 8**
- 超出即被禁用,损失视觉效果

### 7.2 优化方向

- 合并冗余 Dynamic Bone
- 减小 Collider 影响范围
- 删除不必要的动态效果
- 详细优化见 `optimization-guide.md` §PhysBone 最佳化

---

## 8. 风险与陷阱

| 风险 | 等级 | 说明 |
|------|------|------|
| **全部禁用而非部分** | 🔴 高 | 超出限制会**全部**禁用,不是部分 |
| **动画跨越阈值** | 🟡 中 | 动态切换时行为可能不符合预期 |
| **设 0 完全禁用** | 🟡 中 | 所有 Avatar 的 Dynamic Bone 都被强制禁用 |
| **需重启生效** | 🟢 低 | 修改 config.json 后需重启 |
| **与 Performance Rank 混淆** | 🟡 中 | 创作者要理解两个系统的区别 |

---

## 9. 相关文档

- `memory/avatar/performance-rank.md` — Performance Rank 标准
- `memory/avatar/optimization-guide.md` — PhysBone 优化实操
- `memory/avatar/avatar-particle-system-limits.md` — 用户端 Particle Limits(同 config.json)
- `memory/avatar/performance-benchmarks.md` — PhysBone 性能基准

---

## 10. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/avatar-dynamic-bone-limits
- **官方版本**: 2019 初始发布
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)
