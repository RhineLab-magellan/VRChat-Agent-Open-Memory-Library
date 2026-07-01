---
title: "Avatar Domain — Knowledge Base"
category: avatar
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.4
last_review: 2026-07-01
confidence: Medium
tags:
  - misc
  - index
  - navigation
aliases:
  - "Avatar Domain — Knowledge Base"
  - index
related:
  - animator-system.md
  - performance-rank.md
  - thry-avatar-evaluator-metrics.md
  - ndmf-tools.md
  - meshia-mesh-simplification.md
  - lac-avatar-compressor.md
  - avatar-optimizer.md
  - optimization-guide.md
  - teaching-methodology.md
  - modular-avatar.md
  - modular-avatar-tutorials-detailed.md
  - tex-trans-tool.md
  - vrcfury-reference.md
  - ma2bt.md
  - "avatar/avatar-parameter-staged-sync.md"
  - "avatar/ma-component-cards.md"
  - "avatar/contact.md"
  - "avatar/shader/other-shaders.md"
  - "avatar/shader/unlitwf/index.md"
  - "avatar/shader/orl/index.md"
  - "avatar/shader/filamented/index.md"
  - "avatar/shader/poiyomi/index.md"
  - "avatar/avatar-fallback-system.md"
  - "avatar/avatar-dynamic-bone-limits.md"
  - "avatar/avatar-particle-system-limits.md"
  - "avatar/full-body-tracking.md"
  - "avatar/ik-2.0.md"
  - "avatar/avatar-interaction-permissions.md"
  - "avatar/public-avatar-cloning.md"
---
# Avatar Domain — Knowledge Base


---

## 核心文档

| 文档 | 说明 | 来源 |
|------|------|------|
| **[animator-system.md](animator-system.md)** | Write Defaults、Avatar Mask、Playable Layers、参数类型、Direct Blend Tree | VRCLibrary |
| **[performance-rank.md](performance-rank.md)** | PC/Quest 性能等级标准、各指标限制 | 官方文档 |
| **[thry-avatar-evaluator-metrics.md](thry-avatar-evaluator-metrics.md)** ⭐NEW | Thry 工具检测的 7 项指标完整阈值(VRAM/GrabPass/Blendshape/AnyState/Layer/WriteDefaults/EmptyStates)+ 优化决策树 + 与官方 Performance Rank 对照表 | Thryrallo/VRC-Avatar-Performance-Tools v1.3.7 源码 (2026-06-17) |
| **[ndmf-tools.md](ndmf-tools.md)** | NDMF 工具生态、VPM 链接、执行顺序 | Kuriko 笔记 |
| **[meshia-mesh-simplification.md](meshia-mesh-simplification.md)** ⭐NEW | Meshia 完整技术文档（Burst+Job 算法、API、Options、BlendShape、与 lilNDMF/Mantis 对比） | RamType0 官方 (2026-06-17) |
| **[lac-avatar-compressor.md](lac-avatar-compressor.md)** ⭐NEW | **Avatar Compressor (LAC)** - 全自动纹理压缩工具（4 策略/5 预设/平台自动/VRAM 预估/类型感知）| Limitex 官方 (2026-06-17) |
| **[avatar-optimizer.md](avatar-optimizer.md)** ⭐NEW | AAO: Avatar Optimizer 完整知识库 (12 组件 + Trace And Optimize + Animator Optimizer + Component API + Shader Information API + Asset Description + 优化方向矩阵) | 官方文档 (2026-06-17) |
| **[optimization-guide.md](optimization-guide.md)** | 完整最佳化实操指南（Light→Particle→Texture→Mesh→Material→PhysBone→Bones→Polygon） | Kuriko 笔记 |
| **[teaching-methodology.md](teaching-methodology.md)** | Avatar 改模教学法、问题诊断框架、玩家常见踩坑分类(34 条原则 + 9 句式 + 6 禁忌 + 升级检查清单 + MA 5 大玩家友好设计 + **§MM-PP problems 章节教学法** 2026-06-17) | vrnavi.jp + vrcmaster.com + **Kuriko HackMD** 三源 + **MA 官方教程原文** + **MA 官方 problems 章节** (2026-06-17) |
| **[modular-avatar.md](modular-avatar.md)** | Modular Avatar 完整知识库(25+ 组件 + 教学决策树 + Reactive 系统 + **§8.0-§8.7 problems 章节完整版** 2026-06-17) | 官方文档 (2026-06-17) |
| **[modular-avatar-tutorials-detailed.md](modular-avatar-tutorials-detailed.md)** ⭐NEW | MA 6 个教程的官方原文精读 + 玩家视角操作分解 + 验证步骤 + 易错点 + 教学衔接路径 | 官方教程 (2026-06-17) |
| **[tex-trans-tool.md](tex-trans-tool.md)** ⭐NEW | **TexTransTool (TTT)** - 非破坏纹理改写工具完整知识库(15 组件 + AtlasTexture 完整参数表 + Quest 适配 + 与 AAO 协作 + v0.10.0/v1.0.0 破坏性变更 + 故障排查) | ReinaS-64892 官方 + ttt.rs64.net (2026-06-17) |
| **[vrcfury-reference.md](vrcfury-reference.md)** ⭐深度更新 | VRCFury 完整参考：Parameter Compressor (16 bit 压参数) + Direct Tree Optimizer (减层数) + Blendshape Optimizer (减 VRAM) + Fix Write Defaults + Actions 系统 + 60+ 自动修复 + SPS + 全组件清单 + Quest 兼容 + MA/d4rk 共存 + 优化场景对比矩阵(含 d4rk) | 官网 + 仓库 + PR#238 (2026-06-17) |
| **[ma2bt.md](ma2bt.md)** ⭐NEW | **MA2BT** (Modular Avatar to BlendTree) - 将 MA 响应式层合并为 Direct BlendTree 减少 FX 层数（Compact Mode / Multi-State / Scan All Layers 选项 + 完整跳过原因枚举 + 与 AAO 互补关系 + 16 节完整知识库） | Null-K 官方仓库 v2.0.2 (2026-06-17) |
| **[avatar-fallback-system.md](avatar-fallback-system.md)** ⭐NEW 2026-06-30 | Avatar Fallback 系统完整指南（5 种 Fallback 触发原因 + 自定义 Fallback 上传流程 + Grandfathered 规则 + 完整 FAQ + 文件大小 vs VRAM 区分） | VRChat 官方 docs (2026-06-30) |
| **[avatar-dynamic-bone-limits.md](avatar-dynamic-bone-limits.md)** ⭐NEW 2026-06-30 | 用户端 Dynamic Bone Limits 系统（默认值 32/8 + config.json 完整配置 + 与 Performance Rank 区分 + Quest 行为） | VRChat 官方 docs (2026-06-30) |
| **[avatar-particle-system-limits.md](avatar-particle-system-limits.md)** ⭐NEW 2026-06-30 | 用户端 Particle System Limits 系统（11 个配置变量 + Penalty 计算公式 + Quest 默认启用且不可禁用 + PlayerLocal 碰撞限制） | VRChat 官方 docs (2026-06-30) |
| **[full-body-tracking.md](full-body-tracking.md)** ⭐NEW 2026-06-30 | Full-Body Tracking 完整指南（8 tracker 限制 + SteamVR 配置 + 标准/Legacy 校准 + 10 条 Rigging 要求 + Avatars 3.0 集成 + 实验性状态） | VRChat 官方 docs (2026-06-30) |
| **[ik-2.0.md](ik-2.0.md)** ⭐NEW 2026-06-30 | IK 2.0 完整特性（IK Legacy 切换 + Avatar Measurement + Lock Types + Locomotion toggle + 5 个启动参数） | VRChat 官方 docs (2026-06-30) |
| **[avatar-interaction-permissions.md](avatar-interaction-permissions.md)** ⭐NEW 2026-06-30 | Avatar 交互权限设置（Mode/Allow-Pause/Self-Interact + 玩家级覆盖 + PANIC 按钮） | VRChat 官方 docs (2026-06-30) |
| **[public-avatar-cloning.md](public-avatar-cloning.md)** ⭐NEW 2026-06-30 | Public Avatar 克隆（克隆流程 + Allow Avatar Cloning 设置 + Private 化） | VRChat 官方 docs (2026-06-30) |
| **[accessories.md](accessories.md)** ⭐NEW 2026-06-30 | **Avatar Accessories 配件系统** - 2026.2.1+ 新功能，PC=240/Quest=80 全局渲染限制，Look Editor 整合，MA 集成，常见错误修复 | VRChat 2026.2.1 Release Notes |
| **[vrcraycast.md](vrcraycast.md)** ⭐NEW 2026-06-30 | **VRCRaycast 骨骼 raycast** - SDK 3.10.3+ 引入，2026.2.1 改进（自动剥离/Animator 修复/第一人称对称） | VRChat 2026.2.1 Release Notes |

---

## 子域

| 子域 | 内容 | 状态 |
|------|------|------|
| **Animator** | Write Defaults、Avatar Mask、Playable Layers、参数类型、Direct Blend Tree | ✅ 已收录 |
| **Dynamics** | PhysBone, Contact, Constraint, VRC Constraints | ✅ 已收录 |
| Expression | Expression Menu, Expression Parameter | 待建设 |
| **SDK** | Avatar SDK, Modular Avatar | ✅ 已收录 |
| **Optimization** | 性能等级, VRAM, NDMF 工具, 最佳化步骤 | ✅ 已收录 |
| **Shader** | lilToon, Poiyomi, SCSS, Avatar Shader, 特殊效果 | ✅ 已收录 (liltoon/ + poiyomi/ + scss.md) |
| Audio | Avatar Audio, 空间音效 | 待建设 |

---

## 快速入门

### 懒人包

```
1. 复制 Avatar 的 FX Layer、Expression Menu、Expression Parameter
2. 删除所有跟开关物件相关的设定（保留表情 Blend Shape）
3. 复制 Avatar 本身
4. 导入 AAO + Meshia Mesh Simplification
5. 运行 AAO Trace And Optimize
6. 面数还太多 → Remove Mesh / Meshia 减面 / 脱掉
7. 把 FX、参数、选单塞回复制出来的 Avatar
```

### 性能目标

| 目标等级 | 面数 | 材质内存 | VRAM |
|----------|------|----------|------|
| Excellent | 32,000 | 40MB | < 40MB |
| Good | 70,000 | 75MB | < 75MB |
| Medium | 70,000 | 110MB | < 110MB |
| Poor | 70,000 | 150MB | < 150MB |

> 💡 **2026 推荐做法**：使用 Avatar Compressor (LAC) 自动压缩贴图达成 VRAM 目标，详见 `lac-avatar-compressor.md`

---

## 工具 VPM 链接速查

```
Modular Avatar:
  vcc://vpm/addRepo?url=https://vpm.nadena.dev/vpm.json

AvatarOptimizer (AAO):
  https://vpm.anatawa12.com/add-repo

Avatar Compressor (LAC):  ← ⭐NEW 2026-06-17
  https://vpm.limitex.dev/

Meshia Mesh Simplification:
  https://ramtype0.github.io/VpmRepository/index.json

TexTransTool:
  vcc://vpm/addRepo?url=https://vpm.rs64.net/vpm.json

MA2BT:  ← ⭐NEW 2026-06-17
  https://null-k.github.io/vpm-listing/index
```

> ⚠️ `lilNDMFMeshSimplifier` 已于 2024-2025 被官方废弃，请改用 Meshia（详见 `meshia-mesh-simplification.md`）

---

## MA 与 VRCFury 兼容性

> ⚠️ 执行顺序错误会导致出错

```
1. MA + 其他新增内容 NDMF 工具
2. Fury
3. 所有 NDMF 最佳化工具
```

---

## 待收录内容

- VRChat Avatar 官方文档深入研究
- Quest 兼容性约束表
- 常见 Avatar 审核失败原因
- Avatar Audio 空间音效最佳实践
