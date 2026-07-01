---
title: Avatar Impostor & Fallback — 替代 Avatar 机制
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - impostor
  - fallback
  - fallback-avatar
  - performance
  - api

aliases:
  - Impostor
  - Fallback
  - Fallback Avatar
  - 替代 Avatar
  - Impostor Avatar
  - "Avatar Impostor"
  - "Avatar Fallback"

related:
  - avatar/performance-rank.md
  - avatar/safety-system.md
  - avatar/optimization-guide.md
  - avatar/thry-avatar-evaluator-metrics.md
  - vrchatsdk/api-avatars.md

source: docs.vrchat.com/docs/vrchat-configuration-window + vrchat-python (Avatar API)
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Avatar Impostor & Fallback — 替代 Avatar 机制

> 来源:
> - https://docs.vrchat.com/docs/vrchat-configuration-window
> - https://vrchat.community/categories/avatars/ (Avatar API)
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方 + 社区 API 文档)
> 关联: `avatar/performance-rank.md` (Performance Rank) + `avatar/safety-system.md` (Safety 屏蔽)

---

## 概述

> [FACT] 当玩家**主动选择不显示**或**被动屏蔽**某个 Avatar 时，VRChat 可以用**两种替代机制**显示:
>
> 1. **Fallback Avatar**（用户设置的手动备用 Avatar）
> 2. **Impostor Avatar**（VRChat 自动生成的低精度模型）

> **🔴 关键事实**:
> - Avatar **超过** "Maximum Uncompressed Size" 阈值 → 自动用 Impostor/Fallback
> - 用户**主动 Hide Avatar** → 用 Impostor/Fallback
> - 用户**未设置 Fallback** → 用默认 muted 占位

---

## 1. 玩家侧：触发条件

> [FACT] 玩家 Avatar 显示设置在 **Main Menu → Settings**。

### 1.1 Maximum Avatar Download Size

> [FACT] **Maximum Avatar Download Size** 控制 Avatar **下载大小**。
>
> - 默认: **200MB**
> - 步长: **5MB**
> - 超过的 Avatar **不会自动下载**直到玩家点击 "Show Avatar"
> - **小于 5MB** 自动设为 **"No Limit"**（显示所有）

### 1.2 Maximum Uncompressed Size ⭐

> [FACT] **Maximum Uncompressed Size** 控制 Avatar **解压后大小**。
>
> - **推荐值**: **300MB**
> - 超过的 Avatar **用 Impostor 或 Fallback 显示**
> - 适用于**多玩家实例**（性能优化）

> [FACT] **创作者角度**:
> - Avatar **解压后 > 300MB** → 玩家看到 **Impostor/Fallback** 而不是你的 Avatar
> - 应**始终优化** Avatar 在 300MB 以下

### 1.3 Block Poorly Optimized Avatars

> [FACT] **Block Poorly Optimized Avatars** 控制**最低 Performance Rank**。
>
> - 默认: Excellent
> - 选择"最低 rank"以下 → 自动屏蔽
> - 选 "Don't Block" → 不屏蔽（按下载大小等条件）

---

## 2. Impostor Avatar（自动生成的低精度模型）

> [FACT] **Impostor** 是由 VRChat **自动生成**的**低精度静态模型**。

### 2.1 Impostor 特性

| 特性 | 描述 |
|------|------|
| **生成方式** | VRChat 自动（不需要创作者手动）|
| **精度** | 低（类似 thumbnail）|
| **是否动画** | ❌ **静态**，无动画 |
| **创建时间** | Avatar 上传后**异步生成** |
| **使用场景** | Avatar 隐藏 / 超过性能限制时 |

### 2.2 Impostor 生成 API

> [FACT] **VRChat 提供 Impostor 相关 API**:

| API 函数 | 说明 |
|----------|------|
| `enqueue_impostor` | 排队生成该 Avatar 的 Impostor |
| `delete_impostor` | 删除生成的 Impostor |
| `get_impostor_queue_stats` | 获取排队 Impostor 的服务统计 |

> 详见 `vrchatsdk/api-avatars.md`

### 2.3 创作者角度

> [FACT] **创作者**通常**不需要手动**调用 Impostor API。
>
> Impostor 由 VRChat 平台**自动管理**。
>
> 创作者应**关注**:
> - 提供 **Fallback Avatar**（手动备用）
> - Avatar 性能**优化**到 < 300MB

---

## 3. Fallback Avatar（用户设置的手动备用）

> [FACT] **Fallback Avatar** 是玩家**自己设置**的备用 Avatar。
>
> - 玩家在 **Avatar 菜单** 中设置
> - 触发时显示此 Avatar 代替原始 Avatar
> - 玩家**完全控制**用什么 Avatar 作为 Fallback

### 3.1 Fallback 设置方法

> [FACT] **设置 Fallback Avatar**:
> 1. 打开 **Avatar 菜单**（在 Main Menu）
> 2. 选择要设置为 Fallback 的 Avatar
> 3. 点击 **"Select Fallback Avatar"** 选项

### 3.2 Fallback 触发场景

> [FACT] Fallback 在以下情况显示:
> 1. **原始 Avatar 超过 Maximum Uncompressed Size**
> 2. **玩家 Hide Avatar**（per-user 覆盖 Safety）
> 3. **Safety 屏蔽 Avatar**

### 3.3 Fallback Avatar 选择建议

> [FACT] **玩家应选择**:
> - ✅ **轻量**（低 Performance Rank）
> - ✅ **简单**（少骨骼、少材质）
> - ✅ **稳定**（不出问题）
> - ❌ **避免**复杂 Avatar（可能比原始 Avatar 更慢）

### 3.4 创作者角度

> [FACT] 创作者**不能强制**玩家设置自己的 Avatar 为 Fallback。
>
> 但创作者**可以**:
> - 在 Avatar 描述中**建议**玩家设置 Fallback
> - 设计**基础版 Avatar**作为公共 Fallback
> - **优化** Avatar 让 Fallback 不必要

---

## 4. 默认 muted 占位（无 Fallback 时）

> [FACT] **如果玩家没有设置 Fallback Avatar**:
> - VRChat 显示**默认 muted 占位** Avatar
> - 占位 Avatar 是**通用简单模型**
> - 不显示原始 Avatar 任何特性

> [FACT] **m Safety 屏蔽 + 无 Fallback**:
> - 显示 "muted" 头像占位
> - 所有 Avatar 特性（动画/音效/灯光/Shader）**全部禁用**
> - 用户**仍能看到**用户 Nameplate 和 Trust Rank

---

## 5. 触发场景总结

> [FACT] 何时显示 Impostor/Fallback/muted 占位?

| 场景 | Impostor | Fallback | Muted 占位 |
|------|----------|----------|-----------|
| **超过下载大小** | ❌ 需手动 "Show Avatar" | - | - |
| **超过解压大小** | ✅ | ✅（如设置）| ✅（如未设置）|
| **玩家 Hide Avatar** | ✅ | ✅（如设置）| ✅（如未设置）|
| **Safety 屏蔽 Avatar** | ❌ | ❌ | ✅ |
| **Nuisance 标签** | ❌ | ❌ | ✅（默认全屏蔽）|

> [FACT] **Safety 屏蔽不会用 Impostor/Fallback** — 直接用 muted 占位。
>
> 这是因为 Safety 屏蔽是**安全考虑**（不是性能），不应让 Avatar 仍可见。

---

## 6. 创作者最佳实践

### 6.1 必须优化的场景

> [FACT] 创作者**应当**:
> 1. **控制 Avatar 解压大小** < 300MB（推荐 < 200MB）
> 2. **控制 Performance Rank** 在 Excellent/Good
> 3. **测试** Avatar 在 Maximum Uncompressed Size = 300MB 时的显示
> 4. **优化纹理**（用 Avatar Compressor LAC）

### 6.2 工具与流程

> [FACT] 优化 Avatar 工具链:
>
> ```
> 1. Avatar Compressor (LAC)  ← 纹理压缩（4 策略/5 预设）
> 2. AAO Trace And Optimize     ← 自动化 Mesh/Animator 优化
> 3. Meshia Mesh Simplification ← 减面（Burst+Job 算法）
> 4. TexTransTool               ← Atlas 化
> ```
>
> 详见:
> - `avatar/lac-avatar-compressor.md`
> - `avatar/avatar-optimizer.md`
> - `avatar/meshia-mesh-simplification.md`
> - `avatar/tex-trans-tool.md`

### 6.3 不能做的事

> [FACT] 创作者**不应**:
> - ❌ **依赖** Impostor 作为 "正常显示"（Impostor 是降级方案）
> - ❌ **故意**让 Avatar 大（"反正有 Impostor"）— 影响用户口碑
> - ❌ **混淆** Impostor 和 Fallback 概念

---

## 7. Impostor vs Fallback 对比表

> [FACT] 完整对比表:

| 维度 | Impostor | Fallback | Muted 占位 |
|------|----------|----------|-----------|
| **创建者** | VRChat 平台 | 玩家选择 | VRChat 平台 |
| **创建时机** | Avatar 上传后 | 玩家设置时 | 自动 |
| **精度** | 低（静态）| 玩家选择 | 极简 |
| **动画** | ❌ 静态 | ✅（玩家选）| ❌ 静态 |
| **自定义** | ❌ | ✅（玩家选）| ❌ |
| **API 控制** | ✅ `enqueue_impostor` | ❌（玩家设置）| ❌ |
| **触发场景** | 性能/下载限制 | 性能/下载限制 | Safety 屏蔽 |
| **玩家体验** | "看起来像 Avatar" | "是另一个 Avatar" | "占位图标" |

---

## 8. Impostor 生成机制

> [FACT] Impostor 由 **VRChat 后台服务**异步生成。
>
> - Avatar 上传后，**排队等待**生成
> - 生成时间取决于 **VRChat 服务队列负载**
> - 可通过 `get_impostor_queue_stats` 查询

> [FACT] Impostor **更新触发**:
> - Avatar 重新上传时（Impostor 重新生成）
> - 队列空闲时

---

## 9. 创作者 FAQ

### Q1: 我应该提供 Impostor 吗？

> **不需要**。Impostor 是 VRChat 自动管理的，创作者无需手动提供。

### Q2: 玩家说"我的 Avatar 显示是占位"？

> 可能原因:
> 1. Avatar 超过 **Maximum Uncompressed Size (300MB)** — 优化
> 2. 玩家**手动 Hide** — 让玩家重新 Show
> 3. 玩家**未设置 Fallback** — 让玩家设置
> 4. Safety 设置屏蔽 — 玩家个人设置

### Q3: 如何测试 Avatar 是否会触发 Impostor？

> 1. 自己创建**另一个 Profile**
> 2. 进入世界时**下载**自己的 Avatar
> 3. 设置 **Maximum Uncompressed Size** 为 300MB
> 4. 进入多玩家实例看自己的 Avatar
>
> 如果 Avatar 大于 300MB 会显示 Impostor。

### Q4: Fallback Avatar 选什么好？

> 推荐:
> - 系统自带的简单 Avatar
> - 公开的低多边形 Avatar
> - 知名稳定的轻量 Avatar

### Q5: 优化 Avatar 后还需要 Impostor 吗？

> 优化后 Avatar < 300MB **不需要** Impostor 显示（正常显示）。
>
> 但 Impostor **仍会被生成**（作为备选）。

---

## 10. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `avatar/performance-rank.md` | Performance Rank 决定 Avatar 是否被屏蔽 |
| `avatar/safety-system.md` | Safety 屏蔽用 muted 占位（不用 Impostor）|
| `avatar/optimization-guide.md` | 优化 Avatar 避免 Impostor |
| `avatar/thry-avatar-evaluator-metrics.md` | Thry 工具检测的 7 项指标 |
| `vrchatsdk/api-avatars.md` | Impostor API 详细 |

---

## 11. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **Impostor 生成的精确触发条件**（上传后多久开始）
2. ❓ **Impostor 的多分辨率版本**（是否有 LOD）
3. ❓ **Maximum Uncompressed Size** 的历史变化（官方是否调整过）
4. ❓ **Impostor 在 Quest** 的具体行为（Quest 没有 Impostor API？）
5. ❓ **Fallback Avatar** 是否能继承原始 Avatar 的某些属性
6. ❓ **VRChat 平台** 是否有**官方推荐**的 Fallback Avatar
7. ❓ Impostor 与 **Performance Rank** 的精确关系

---

## 来源

- [VRChat Configuration Window](https://docs.vrchat.com/docs/vrchat-configuration-window)
- [VRChat Avatar API](https://vrchat.community/categories/avatars/)
- [VRChatSDK Avatar API (vrchatsdk/api-avatars.md)](https://vrchat.com/)
- 本地化版本: `参考文献/SP/user-guide/vrchat-configuration-window.md`
