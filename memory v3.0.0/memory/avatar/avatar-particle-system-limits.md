---
title: Avatar Particle System Limits — 用户端粒子系统限制
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - performance
  - particles
  - config
  - quest

aliases:
  - "Particle System Limits"
  - "粒子系统限制"
  - "PS 限制"
  - "用户端 Particle Limits"

related:
  - "avatar/performance-rank.md"
  - "avatar/optimization-guide.md"
  - "avatar/avatar-dynamic-bone-limits.md"
  - "platform/android-development.md"

source: https://docs.vrchat.com/docs/avatar-particle-system-limits
source_type: community
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Avatar Particle System Limits — 用户端粒子系统限制

> 来源: VRChat 官方文档 - Avatar Particle System Limits
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **关键 Insight**: 这是**用户端**限制系统(Beta),与 **Performance Rank** 不同。

---

## 1. 概述

**Particle System Limits** 是 VRChat 客户端为其他玩家 Avatar 上的粒子系统设置上限的**Beta 系统**。

**目的**:
- 防止 Avatar 粒子系统滥用影响性能
- 提供细粒度的参数控制(数量、发射、网格、碰撞、轨迹)

---

## 2. ⚠️ 重要: Quest 行为

> 🚧 **Enabled on Quest**
>
> This system is enabled by default on Quest with the default settings and **cannot be disabled**.
> This is for performance and safety reasons.

**关键事实**:
- ✅ Quest 端**默认启用**
- ❌ Quest 端**不能禁用**
- ✅ Quest 端使用默认设置

### PlayerLocal 粒子碰撞

> ⚠️ The limiter will prevent any particles from colliding with PlayerLocal.
> There is no setting to disable this without disabling the limiter.

**含义**:
- 所有粒子与 PlayerLocal(本地玩家)碰撞都被阻止
- 不可单独关闭此行为
- 只能整体禁用 Limiter(但 Quest 端不能禁用)

---

## 3. Beta 状态

> This feature is in beta. This feature may be changed, modified, or removed with future releases.

- 当前为 Beta 功能
- 未来可能修改或删除
- VRChat 鼓励实验并反馈

---

## 4. 默认配置

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
  "ps_trails_penalty": 10
}
```

### 4.1 配置变量详解

| 变量名 | 描述 |
|--------|------|
| `betas` | 添加/删除 `"particle_system_limiter"` 字符串 = 启用/禁用 |
| `ps_max_particles` | 单个粒子系统最大粒子数 |
| `ps_max_systems` | 最大粒子系统数(配置示例中有,详细说明缺失) |
| `ps_max_emission` | 单个粒子系统最大发射 |
| `ps_max_total_emission` | 所有粒子系统总最大发射 |
| `ps_mesh_particle_divider` | 网格多边形惩罚 = 最高多边形数 / 此值 |
| `ps_mesh_particle_poly_limit` | 粒子网格最大多边形数 |
| `ps_collision_penalty_high` | 高质量碰撞惩罚(除数) |
| `ps_collision_penalty_med` | 中等质量碰撞惩罚 |
| `ps_collision_penalty_low` | 低质量碰撞惩罚 |
| `ps_trails_penalty` | Trail 启用惩罚(除数) |

### 4.2 Penalty 系统(CRITICAL)

> **关键 Insight**: 实际最大粒子数 = `base / (poly/divider) / collision_penalty / trails_penalty`

**计算公式**:
```
effective_max = ps_max_particles
              / (meshPoly / ps_mesh_particle_divider)
              / (collision_enabled ? ps_collision_penalty_X : 1)
              / (trails_enabled ? ps_trails_penalty : 1)
```

**示例**:
- 基础 50000 粒子
- 网格 6000 多边形 → penalty = 6000/60 = 100
- 高质量碰撞 → penalty = 50
- Trails 启用 → penalty = 10
- **实际最大 = 50000 / 100 / 50 / 10 = 1 粒子**(极其严格)

> ⚠️ 此公式为 [INFERENCE] 推断(基于官方文档对各 penalty 的描述推导)
> 实际计算逻辑可能与官方实现略有差异,建议根据实际表现验证

---

## 5. 修改配置

### 5.1 配置文件位置

```
%AppData%\..\LocalLow\VRChat\vrchat\config.json
```

实际 Windows 路径:
- `C:\Users\<Username>\AppData\LocalLow\VRChat\vrchat\config.json`

### 5.2 ⚠️ 需重启

> **修改需要重启 VRChat 才生效。**

### 5.3 预填默认配置下载

- URL: https://assets.vrchat.com/misc/vrchat%3Bconfig.json
- 如点击直接显示而非下载,右键 → Save As
- **必须重命名为 `config.json`**

---

## 6. 启用/禁用系统

```json
{
  "betas": [
    "particle_system_limiter"   // 包含 = 启用
    // 删除此字符串 = 禁用(Quest 端无效)
  ]
}
```

---

## 7. 与 Performance Rank 的关系

| 维度 | Performance Rank | Particle System Limits |
|------|-----------------|------------------------|
| **触发时机** | 上传时 SDK 评估 | 运行时客户端检查 |
| **检查方** | VRChat 后端 | 本地 VRChat 客户端 |
| **可调整** | 创作者优化 Avatar | 用户修改 config.json |
| **Quest 行为** | 不同阈值(更严) | 默认启用且**不可禁用** |
| **细粒度** | 数量级阈值 | Penalty 系统可细调 |

### 关键区分

> - **Performance Rank**: 上传时等级(粗粒度: 数量级)
> - **Particle System Limits**: 运行时阈值(细粒度: penalty 公式)
> - 两者独立,但都关注粒子数量

---

## 8. 创作者建议

### 8.1 避免触发限制

- **单个粒子系统粒子数 < 50000**(默认)
- **网格多边形 < 60000**(避免 mesh particle penalty 过重)
- **慎用高质量碰撞**(penalty 50,影响显著)
- **慎用 Trails**(penalty 10,严重影响)

### 8.2 优化方向

- 减少粒子数,提高单个粒子视觉密度
- Mesh 粒子用低多边形网格
- 用性能更好的碰撞层级
- Trails 是最贵的特性,能不用就不用

### 8.3 跨平台考虑

- Quest 端粒子限制**更严格**
- Particle System Limits 在 Quest **不可禁用**
- 关键: 你的 Avatar 在 Quest 端可能看到不同效果

---

## 9. 风险与陷阱

| 风险 | 等级 | 说明 |
|------|------|------|
| **Quest 端不可禁用** | 🔴 高 | 必须在 Avatar 设计时考虑 |
| **PlayerLocal 碰撞被禁** | 🟡 中 | 任何粒子都不会与本地玩家碰撞 |
| **Penalty 复合** | 🟡 中 | 多个 penalty 复合可能让实际上限极低 |
| **Beta 不稳定** | 🟡 中 | 行为可能改变 |
| **与 Performance Rank 混淆** | 🟡 中 | 创作者需理解两个系统的区别 |

---

## 10. 相关文档

- `memory/avatar/performance-rank.md` — Performance Rank 标准
- `memory/avatar/optimization-guide.md` — Particle System 优化
- `memory/avatar/avatar-dynamic-bone-limits.md` — 用户端 DB Limits(同 config.json)
- `memory/platform/android-development.md` — Quest 端开发

---

## 11. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/avatar-particle-system-limits
- **官方版本**: 2018-06-19 建议版本
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)
- **Penalty 公式**: [INFERENCE] 推断(基于官方变量描述推导)
