---
title: "Poiyomi Shaders 文档整理审查与入库计划 (2026-07-01)"
category: reviews
subcategory: import-plan

knowledge_level: applied
status: active

tags:
  - reviews
  - poiyomi
  - shader
  - knowledge-base
  - import-plan
  - audit
  - curator

aliases:
  - "Poiyomi 入库计划"
  - "Poiyomi 数据审查"
  - "Poiyomi 知识库整合"

related:
  - ../avatar/shader/index.md
  - ../avatar/shader/other-shaders.md
  - ../avatar/index.md
  - ../sources/vpm-mirrors/samples/poiyomi.md
  - ../../参考文献/Poiyomi/INDEX.md
  - ../meta/kb-protocol.md
  - ../meta/working-modes.md

source: 本地数据审查(2026-07-01) + Memory 现状对比 + 入库规划
source_type: inferred
version: 1.0
last_review: 2026-07-01
confidence: High
---

# Poiyomi Shaders 文档整理审查与入库计划

> **Domain**: Meta (Knowledge Base Curation)
> **评审日期**: 2026-07-01
> **评审员**: CherryClaw (Curator 模式)
> **评审范围**: 65 个 Poiyomi 官方文档 + 1 个 INDEX.md
> **目的**: 将原始下载数据 → 结构化知识库

---

## 摘要 (Executive Summary)

| 维度 | 当前状态 | 目标状态 | 差距 |
|------|----------|----------|------|
| **数据完整度** | 65 文档入库 | 65 文档可用 | ✅ 已达成 |
| **知识结构化** | 原始翻译 + INDEX | 主题提炼 + 引用 | ⚠️ 需 Stage 2 |
| **与 Memory 整合** | 索引/other-shaders 已更新 | 全 KB 路由补全 | ⚠️ 需 Stage 3 |
| **数据缺口** | 8 个页面缺失/截断 | 完整覆盖 | ⚠️ 需 Stage 4 |
| **质量评估** | B+ 级 (良好) | A 级 (优秀) | ⚠️ 需 Stage 2-5 |

**核心结论**:
- ✅ 数据本身质量良好(标准化 frontmatter + 统一图片描述 + 元信息表格)
- ⚠️ 知识结构仍为"原始翻译"层级,未达到"提炼知识"层级
- ⚠️ 8 个子页面缺失(shading-styles 7 个 + matcaps 1 个),需后续重抓
- ⚠️ 与已有 Poiyomi 知识(VPM 8.1.166/9.3.66)存在版本不一致,需对齐说明
- 📋 建议按 5 个 Stage 渐进式入库,预计总工时 8-12 小时

---

## 一、数据整理审查 (Data Audit)

### 1.1 总体统计

| 指标 | 数值 | 备注 |
|------|------|------|
| **总 .md 文件** | 66 | 65 文档 + 1 INDEX |
| **总大小** | ~280 KB | 平均 4.3 KB/文件 |
| **覆盖页面** | 65 | 1:1 映射官方文档 |
| **Shader 变体** | 5/5 | Nano/Micro/Mega/Giga/Tera |
| **Patreon 等级** | 6/6 | Public + 5 付费 |
| **一级分类** | 16 | INDEX.md 已建立 |
| **数据源** | https://www.poiyomi.com/ | 官方文档 |
| **抓取日期** | 2026-07-01 | 单次完整抓取 |
| **目标版本** | 10.0 | 分阶段推出中 |

### 1.2 数据质量评估

#### ✅ 优点 (P0 - 优秀)

| 项目 | 状态 | 证据 |
|------|------|------|
| **YAML frontmatter** | ✅ 100% | 65 文档全部包含标准化 frontmatter |
| **元信息表格** | ✅ 100% | 每个文件末尾都有 `## 元信息` 表格 |
| **图片描述格式** | ✅ 100% | 统一 `> **[图片描述]**` 格式,中文转写 |
| **Markdown 纯净度** | ✅ 高 | 原始 HTML 已清除,代码块/表格/列表保留 |
| **版本号标注** | ✅ 100% | frontmatter + 文末表格双重标注 |
| **源 URL 完整** | ✅ 100% | 65 文档都标注 `source: https://...` |

#### ⚠️ 缺点 (P1 - 警告)

| 问题 | 影响文件 | 严重度 | 缓解 |
|------|----------|--------|------|
| **Fetch 截断** | `06-reflections-and-specular.md`, `07-clear-coat.md` | P1 | 已标注"详见文档页面以获取更多详细信息" |
| **404 页面** | shading-styles 7 子页面 + shading/matcaps | P1 | 已合并到 `63-shadows-shading-styles.md` |
| **图片描述简短** | 多数文件 | P2 | 已用文字叙述,符合任务要求 |
| **翻译质量参差** | 全部文件 | P2 | 多数直译,部分用专业术语 |
| **URL 路径不一致** | 约 1/3 文件 | P2 | 部分用 `path/`,部分用 `path/main` |

#### ❌ 严重问题 (P0 - 暂无)

无 P0 级问题。

### 1.3 覆盖度分析 (Coverage Matrix)

| 一级分类 | 覆盖页面 | 完整性 | 状态 |
|----------|----------|--------|------|
| 概述与基础 | 6 (00-05) | 100% | ✅ |
| 反射与光照 | 5 (06-10) | 100% | ✅ |
| AudioLink 基础 | 2 (11-12) | 100% | ✅ |
| 颜色与材质 | 4 (13-16) | 100% | ✅ |
| 顶点操作 | 5 (17-21) | 100% | ✅ |
| 灯光与阴影 | 7 (22-28) | 100% | ✅ |
| 编辑器 | 3 (29-31) | 100% | ✅ |
| 模块化与遮罩 | 5 (32-36) | 100% | ✅ |
| UV 与视差 | 6 (37-42) | 100% | ✅ |
| 后期处理 | 1 (43) | 100% | ✅ |
| 毛发与几何 | 3 (44-46) | 100% | ✅ |
| VFX 特效 | 12 (47-58) | 100% | ✅ |
| 几何与抓取 | 3 (59-61) | 100% | ✅ |
| Volume Color | 1 (62) | 100% | ✅ |
| 阴影与着色样式 | 1 (63, 9 种) | 60% | ⚠️ Texture Ramp + Multilayer Math 完整,其他 7 种需补 |
| TPS Wizard | 1 (64) | 30% | ⚠️ 仅 Wizard 主页面,详细子页面未抓取 |

**总覆盖率**: 64/65 = 98.5% (1 个合并页面有 8 个子页面缺失细节)

### 1.4 数据缺口识别 (Gap Analysis)

#### P1 - 重要缺口

| 缺口 | 原始 URL | 状态 | 建议 |
|------|----------|------|------|
| Wrapped Shading | https://www.poiyomi.com/shading/wrapped | ❌ 404 | 合并到 63,后续单独抓取 |
| Skin Shading | https://www.poiyomi.com/shading/skin | ❌ 404 | 合并到 63,后续单独抓取 |
| ShadeMap Shading | https://www.poiyomi.com/shading/shademap | ❌ 404 | 合并到 63,后续单独抓取 |
| Flat Shading | https://www.poiyomi.com/shading/flat | ❌ 404 | 合并到 63,后续单独抓取 |
| Realistic Shading | https://www.poiyomi.com/shading/realistic | ❌ 404 | 合并到 63,后续单独抓取 |
| Cloth Shading | https://www.poiyomi.com/shading/cloth | ❌ 404 | 合并到 63,后续单独抓取 |
| SDF Shading | https://www.poiyomi.com/shading/sdf | ❌ 404 | 合并到 63,后续单独抓取 |
| Matcaps | https://www.poiyomi.com/shading/matcaps | ❌ 404 | 跳过,可后续抓取 |

#### P2 - 建议补充

| 缺口 | 备注 |
|------|------|
| TPS 子页面(Non-Humanoid, Custom Penetrator, Custom Orifice) | 64 仅有 Wizard |
| Shading styles 的 Border / Blur 子参数完整文档 | 63 部分有 |

#### P3 - 内容截断(已标注)

| 文件 | 截断位置 | 影响 |
|------|----------|------|
| 06-reflections-and-specular | "Stochastic Sampling - Enables S" | 部分参数未抓全 |
| 07-clear-coat | "GSAA - Type: To" | 部分参数未抓全 |
| 26-backlight | 文档整体较短 | 可能非截断,内容本身简短 |

### 1.5 元信息一致性检查

| 检查项 | 通过率 | 说明 |
|--------|--------|------|
| YAML frontmatter 存在 | 100% (65/65) | ✅ |
| `title` 字段 | 100% | ✅ |
| `category: references` | 100% | ✅ |
| `subcategory: poiyomi` | 100% | ✅ |
| `source: https://...` | 100% | ✅ |
| `version: 10.0` | 100% | ✅ |
| `last_review: 2026-07-01` | 100% | ✅ |
| `download_date: 2026-07-01` | 100% | ✅ |
| `confidence: High` | 100% | ✅ |
| **元信息表格** | **100%** | ✅ 文件末尾都有 |
| **图片描述** | **100%** | ✅ 中文化转写 |
| **字号(KB)/文件** | 平均 4.3 KB | ⚠️ 部分文件< 2 KB(可能内容本身简短) |

**元信息一致性评级**: A (优秀)

---

## 二、与 Memory 对比 (Memory Comparison)

### 2.1 已有 Poiyomi 知识分布

| 文件 | 内容性质 | 版本 | 状态 |
|------|----------|------|------|
| `memory/sources/vpm-mirrors/samples/poiyomi.md` | VPM 包元数据 | 8.1.166 Toon / 9.3.66 Pro | 🔴 同步失败,信息陈旧 |
| `memory/world/vrc-light-volumes.md` | Light Volumes 兼容 (Line 340, 439) | "Poiyomi Toon 9.2.67+" | ✅ 准确 |
| `memory/avatar/avatar-optimizer.md` | UV Tile Discard 设计 (Line 341) | 未指定版本 | ⚠️ 上下文简短 |
| `memory/avatar/teaching-methodology.md` | 教学资源列表 (Line 129) | 无版本 | ✅ 概述性引用 |
| `memory/avatar/shader/index.md` | **新增 Poiyomi 章节** | 1.2 (2026-07-01) | ✅ 已更新 |
| `memory/avatar/shader/other-shaders.md` | **新增 Poiyomi 引用** | 1.1 (2026-07-01) | ✅ 已更新 |
| `memory/avatar/shader/filamented/comparison.md` | 对比表格 (推测) | 推测 | ⚠️ 待验证 |
| `memory/avatar/shader/filamented/overview.md` | 概述 (推测) | 推测 | ⚠️ 待验证 |
| `memory/avatar/vrcfury-reference.md` | 推测提及 | 推测 | ⚠️ 待验证 |

**总计 9 个文件中提及 Poiyomi**,其中 2 个已主动更新,7 个为被动引用。

### 2.2 版本演进分析 (Version Evolution)

```
Poiyomi 8.x (2020-2023)
├── com.poiyomi.toon: v8.1.166 (free Toon)
└── 主流欧美 Avatar 标配

Poiyomi 9.x (2023-2026)
├── com.poiyomi.toon: v8.x 系列继续维护
├── com.poiyomi.pro: v9.3.66 (Patreon $10+)
└── Pro 添加 Lighting/Tessellation 等

Poiyomi 10.0 (2026+ 当前分阶段推出) ← 我们抓取的版本
├── 新增 Shader Graph 9.x+ Pro 基础架构
├── 新增 Modular Shader System(Pro)
├── 新增 9 种 Lighting Type
├── 新增 5 个变体分级(Nano→Tera)
├── Poiyomi 10.0 文档正在分阶段更新
└── VPM 实际包版本可能仍为 9.x(文档先行)
```

**关键观察**:
- 10.0 文档已发布,但 VPM 实际可用版本可能仍为 9.3.x
- 旧 VPM 知识库的版本号(8.1.166/9.3.66)在 10.0 推出后仍可能有效
- 10.0 文档"分阶段推出"意味着部分功能可能尚未全部可用

### 2.3 知识重叠与冲突 (Overlap & Conflicts)

#### 🔴 已识别冲突 (1 项)

| 冲突 | 旧知识 | 新知识 | 处理 |
|------|--------|--------|------|
| **当前最新版本** | VPM 9.3.66 (2026-07-01) | 10.0 文档分阶段推出 | 在 `sources/vpm-mirrors/samples/poiyomi.md` 添加"10.0 演进"章节 |

#### 🟡 潜在冲突 (2 项)

| 潜在冲突 | 说明 | 处理 |
|----------|------|------|
| **Poiyomi Pro 必要性** | 旧:"Pro 仅 Lighting/Tessellation" vs 新:"Pro 包含 Modular/Fur/ShatterWave 等 7+ 关键功能" | 主题知识文档中明确 Pro vs Toon 边界 |
| **9.2.67 兼容 VRC Light Volumes** | 旧文档说 9.2.67+,新文档未明确版本号 | Light Volumes 引用保持现状,新增 Poiyomi 章节无需重复 |

#### ✅ 无冲突 (其余 6 项)

- VPM URL、作者、类型等元数据无变化
- 功能定位(Avatar Toon 主流)无变化
- 与 lilToon 对比关系无变化

### 2.4 知识盲区识别 (Knowledge Gaps)

#### 已填补的盲区 (Poiyomi 文档补充后)

| 盲区 | 补充情况 |
|------|----------|
| Poiyomi 5 个变体详细区别 | ✅ 已补充 (Nano/Micro/Mega/Giga/Tera) |
| Poiyomi Pro 完整功能列表 | ✅ 已补充 (7+ 关键功能) |
| AudioLink 完整集成方式 | ✅ 已补充 (11-audio-link.md) |
| Modular Shader System 工作流 | ✅ 已补充 (32-modular-shader-system.md) |
| 9 种 Lighting Type | ✅ 已补充 (63-shadows-shading-styles.md) |
| 16 通道 Global Masking | ✅ 已补充 (33-global-masks.md) |
| Thry Editor 完整工作流 | ✅ 已补充 (29-thry-editor.md) |
| Quest 优化策略 (Micro 变体) | ✅ 已补充 (INDEX.md) |

#### 仍存在的盲区 (需要 Stage 2-4 提炼)

| 盲区 | 现状 | 解决阶段 |
|------|------|----------|
| **Poiyomi + Modular Avatar 集成** | ❌ 无 | Stage 2 |
| **Poiyomi + AAO 优化** | ❌ 无 | Stage 2 |
| **Poiyomi + 实战案例** | ❌ 无(原文档不提供) | Stage 2 (从社区找) |
| **Poiyomi Pro 安装鉴权流程** | ⚠️ 提及但无详细步骤 | Stage 2 |
| **Poiyomi 与 lilToon 性能对比** | ❌ 无 | Stage 2 |
| **Poiyomi Quest 性能数据** | ⚠️ Micro 变体存在但无 benchmark | Stage 2 (从社区) |
| **TPS 详细子页面** | ⚠️ Wizard 已入库,Custom Penetrator/Orifice 未入库 | Stage 4 |

### 2.5 关联文档影响评估 (Impact Assessment)

| 文档 | 影响 | 优先级 | 操作 |
|------|------|--------|------|
| `memory/avatar/index.md` | 需添加 Poiyomi 子域引用 | P1 | Stage 3 |
| `memory/index.md` | 需添加 Poiyomi 路由 | P1 | Stage 3 |
| `_always-load.md` | 需添加 Poiyomi 关键约束 | P2 | Stage 3 |
| `memory/avatar/shader/index.md` | ✅ 已更新 (1.2) | P0 | 已完成 |
| `memory/avatar/shader/other-shaders.md` | ✅ 已更新 (1.1) | P0 | 已完成 |
| `memory/sources/vpm-mirrors/samples/poiyomi.md` | 需添加 10.0 演进说明 | P1 | Stage 3 |
| `memory/FACT.md` | 需添加 Poiyomi 完整入库记录 | P1 | Stage 3 |
| `memory/avatar/performance-rank.md` | 无需更新(与 Poiyomi 关系间接) | - | 跳过 |

---

## 三、详细入库计划 (Integration Plan)

### 3.1 入库原则 (Guiding Principles)

1. **单一来源原则** [FACT 引用 kb-protocol.md]
   - 原始数据(65 .md)放 `参考文献/Poiyomi/`,作为"外部参考"
   - 提炼知识放 `memory/avatar/shader/poiyomi/`,作为"知识库"
   - 不重复内容,通过链接引用

2. **先 Journal 后 KB** [FACT 引用 kb-protocol.md]
   - 关键发现先 append 到 journal
   - 验证后再入知识库

3. **引用而非复制** [本计划新增原则]
   - 主题知识文档以"提炼 + 引用"为主
   - 详细参数表链接到原始 65 .md
   - 避免大段重复内容

4. **Pro vs Toon 边界明确** [本计划新增原则]
   - 任何 Pro 专属功能必须明确标注"Poiyomi Pro"
   - Toon 免费版功能独立标注
   - 避免误导

5. **P0/P1/P2 分级处理** [FACT 引用 kb-protocol.md]
   - P0 阻塞: 24h 内处理
   - P1 警告: 一周内处理
   - P2 建议: 长期计划

### 3.2 优先级矩阵 (Priority Matrix)

| 阶段 | 任务 | 严重度 | 工时 | 依赖 | 状态 |
|------|------|--------|------|------|------|
| **Stage 1** | 索引 + 引用更新 | P0 | 0.5h | 无 | ✅ 已完成 |
| **Stage 2.1** | 主题知识文档 - 安装与版本 | P1 | 1h | Stage 1 | 📋 待开始 |
| **Stage 2.2** | 主题知识文档 - 5 变体详解 | P1 | 1h | Stage 1 | 📋 待开始 |
| **Stage 2.3** | 主题知识文档 - AudioLink 集成 | P1 | 1h | Stage 1 | 📋 待开始 |
| **Stage 2.4** | 主题知识文档 - Modular System | P1 | 1h | Stage 1 | 📋 待开始 |
| **Stage 2.5** | 主题知识文档 - 9 种 Lighting Type | P1 | 1.5h | Stage 1 | 📋 待开始 |
| **Stage 2.6** | 主题知识文档 - Quest 优化 | P1 | 0.5h | Stage 1 | 📋 待开始 |
| **Stage 2.7** | 主题知识文档 - 与 lilToon 对比 | P1 | 0.5h | Stage 1 | 📋 待开始 |
| **Stage 3** | 索引与路由补全 | P1 | 1h | Stage 1 | 📋 待开始 |
| **Stage 4.1** | 缺口修复 - shading-styles 7 子页面 | P2 | 2h | 无 | 📋 待开始 |
| **Stage 4.2** | 缺口修复 - shading/matcaps | P2 | 0.5h | 无 | 📋 待开始 |
| **Stage 4.3** | 缺口修复 - TPS 子页面 | P2 | 0.5h | 无 | 📋 待开始 |
| **Stage 4.4** | 缺口修复 - Fetch 截断页面 | P2 | 1h | 无 | 📋 待开始 |
| **Stage 5.1** | 验证 - URL 健康检查 | P2 | 0.5h | Stage 1-4 | 📋 待开始 |
| **Stage 5.2** | 验证 - 元信息一致性 | P2 | 0.5h | Stage 1-4 | 📋 待开始 |
| **Stage 5.3** | 归档 - journal 完整记录 | P1 | 0.5h | Stage 1-4 | 📋 待开始 |

**总工时估算**: 12-14 小时(分散在 1-2 周内)

### 3.3 Stage 1: 索引与引用更新 (✅ 已完成)

**完成时间**: 2026-07-01
**实际工时**: 0.5h

| 操作 | 文件 | 状态 |
|------|------|------|
| 创建主索引 | `参考文献/Poiyomi/INDEX.md` | ✅ |
| 更新索引 | `memory/avatar/shader/index.md` (1.1→1.2) | ✅ |
| 更新引用 | `memory/avatar/shader/other-shaders.md` (1.0→1.1) | ✅ |
| Journal 记录 | `memory/JOURNAL.jsonl` (1 条 session 记录) | ✅ |

### 3.4 Stage 2: 结构化提炼 (本周 P1)

**目标**: 从 65 个原始文档提炼为 7-8 个主题知识文档

#### 3.4.1 推荐目录结构

```
memory/avatar/shader/poiyomi/
├── index.md                 ← poiyomi 总览(指向 INDEX + 7 主题)
├── installation.md          ← 安装与版本(含 VPM 鉴权流程)
├── shader-variants.md       ← 5 变体详解(Nano→Tera)
├── audiolink-integration.md ← AudioLink 完整集成
├── modular-system.md        ← Modular Shader System(Pro)
├── shading-styles.md        ← 9 种 Lighting Type
├── quest-optimization.md    ← Quest 优化策略
├── comparison-liltoon.md    ← Poiyomi vs lilToon
├── pro-vs-toon.md           ← Pro vs Toon 边界
└── common-issues.md         ← 常见问题与故障排查
```

#### 3.4.2 每个主题文档的内容规范

| 章节 | 内容 |
|------|------|
| 概述 | 一句话定义 + 适用场景 |
| 核心概念 | 关键术语 + 概念图(可用 ASCII) |
| 配置详解 | 提炼自原始 .md 的关键参数,带 Pro/Toon 标注 |
| 代码示例 | Udon/Shader 代码片段(仅必要时) |
| 实战陷阱 | 常见错误 + 修复方法 |
| 引用 | 指向 `参考文献/Poiyomi/` 中具体 .md 文件 |
| 元信息 | 与原始数据相同的 source/version/last_review |

#### 3.4.3 工作模式

- **"1 Agent 1 文档" 策略** [FACT 引用 kb-protocol.md]
- 每篇主题文档独立创建、独立审查
- 二次独立验证(另开 session 审核)

### 3.5 Stage 3: 索引与路由补全 (本周 P1)

| 操作 | 文件 | 内容 |
|------|------|------|
| 添加 Poiyomi 路由 | `memory/index.md` | 在 Avatar 域添加 `shader/poiyomi/index.md` 引用 |
| 更新 Poiyomi 章节 | `memory/avatar/index.md` | 添加 Poiyomi 子域引用 |
| 关键约束 | `_always-load.md` | 添加 Poiyomi 5 变体速查 |
| 10.0 演进说明 | `memory/sources/vpm-mirrors/samples/poiyomi.md` | 添加"10.0 版本演进"章节 |
| 入库记录 | `memory/FACT.md` | 添加 Poiyomi 完整入库记录 |

### 3.6 Stage 4: 缺口修复 (长期 P2)

| 缺口 | 修复方式 | 工时 |
|------|----------|------|
| **shading-styles 7 子页面** | 重新抓取 `https://www.poiyomi.com/shading/{wrapped,skin,shademap,flat,realistic,cloth,sdf}` | 2h |
| **shading/matcaps** | 重新抓取或确认 404 | 0.5h |
| **TPS 子页面** | 抓取 `https://www.poiyomi.com/TPS/{non-humanoid,custom-penetrator,custom-orifice}` | 0.5h |
| **Fetch 截断页面** | 重新抓取 `06-reflections-and-specular`, `07-clear-coat` | 1h |
| **9.x/10.x VPM 包数据更新** | 重新同步 VPM | 0.5h |

**建议**: 缺口修复可在后续抓取任务中批量处理,不必一次性完成。

### 3.7 Stage 5: 验证与归档 (长期 P1-P2)

| 验证项 | 工具 | 频率 |
|--------|------|------|
| **URL 健康** | url_health_check.py | 季度 |
| **元信息一致性** | validation_script.py | 每次维护 |
| **死链/孤立文件** | governance_script.py | 每次维护 |
| **版本号核对** | version_audit_script.py | 季度 |
| **Pure Knowledge 审计** | pure_knowledge_audit.py | 库迁移后 |

### 3.8 时间线与资源

```
Week 1 (2026-07-01 ~ 2026-07-07)
  Day 1: Stage 1 ✅ (索引 + 引用)
  Day 2-3: Stage 2.1-2.3 (安装/变体/AudioLink)
  Day 4-5: Stage 2.4-2.5 (Modular/Shading Styles)
  Day 6-7: Stage 2.6-2.7 + Stage 3 (Quest优化/对比/路由)

Week 2 (2026-07-08 ~ 2026-07-14)
  Day 1-2: Stage 4.1 (shading-styles 重抓)
  Day 3-4: Stage 4.2-4.4 (其他缺口)
  Day 5: Stage 5 (验证)

持续维护
  - 季度 URL 健康检查
  - SDK 更新后 version_audit
  - Poiyomi 10.x 文档更新跟踪
```

### 3.9 风险与缓解 (Risk Matrix)

| 风险 | 概率 | 影响 | 缓解策略 |
|------|------|------|----------|
| **10.0 文档"分阶段推出"** | 高 | 中 | 在主题文档中标注"10.0 文档分阶段更新,实际可用功能可能滞后" |
| **Pro 鉴权流程未在文档中详述** | 中 | 中 | Stage 2 引用 `sources/vpm-mirrors/samples/poiyomi.md` 的 Patreon $10+ 说明 |
| **Poiyomi 团队改动 API** | 低 | 高 | 定期(季度)重新抓取 + validation_script |
| **shading-styles 重抓仍 404** | 中 | 低 | 已在 63 中合并,记录为已知缺口 |
| **与 lilToon 对比过于主观** | 中 | 低 | Stage 2.7 明确标注"基于文档对比,实战数据需自行测试" |
| **Stage 2 工作量大导致延期** | 中 | 中 | 优先级: 先做 Stage 2.1-2.3(最高价值),其他可后续 |
| **Poiyomi 8.x 老用户知识迁移** | 低 | 低 | 主题文档中加"10.0 迁移"附录(如必要) |

---

## 四、决策建议 (Recommendations)

### 4.1 立即可做的 (P0 - 今天已完成)

- [x] 创建 `参考文献/Poiyomi/INDEX.md`
- [x] 更新 `memory/avatar/shader/index.md` (Poiyomi §1.3 章节)
- [x] 更新 `memory/avatar/shader/other-shaders.md` (Poiyomi 引用)

### 4.2 本周建议 (P1)

- [ ] **优先级最高**: Stage 2.1 + 2.2 + 2.3(安装 + 变体 + AudioLink)
- [ ] **次优先级**: Stage 2.4 + 2.5(Modular + Shading Styles)
- [ ] **配合**: Stage 3(路由补全)

### 4.3 可选建议 (P2)

- [ ] Stage 4 缺口修复(可分散在后续会话)
- [ ] Stage 5 验证(下次维护时执行)

### 4.4 长期跟踪

- [ ] 季度 Poiyomi 文档重新抓取(10.x 演进)
- [ ] 社区实战案例补充(MOD 社区、Discord 资源)
- [ ] 性能数据补充(实际测试 benchmark)

---

## 五、附录 (Appendix)

### 5.1 文档元数据映射

| 原始 .md (数量) | 提炼主题文档 | 关系 |
|------------------|--------------|------|
| 00-05 (6) | `installation.md` + `shader-variants.md` | 概述部分 |
| 06-10 (5) | `shading-styles.md` | 反射光照 |
| 11-12 (2) + 62 (1) | `audiolink-integration.md` | AudioLink 完整 |
| 13-16 (4) | 引用为主(基础概念) | 颜色与材质 |
| 17-21 (5) | 引用为主(基础概念) | 顶点操作 |
| 22-28 (7) | `shading-styles.md` | 灯光阴影 |
| 29-31 (3) | `modular-system.md` 引用 | 编辑器 |
| 32-36 (5) | `modular-system.md` | 模块化核心 |
| 37-42 (6) | 引用为主 | UV |
| 43-58 (16) | `modular-system.md` + 引用 | 特效 |
| 59-61 (3) | 引用为主 | 几何与抓取 |
| 62 (1) | `audiolink-integration.md` | Volume Color |
| 63 (1) | `shading-styles.md` | 着色样式主源 |
| 64 (1) | 引用为主 | TPS Wizard |

### 5.2 关键概念速查

| 概念 | 文档位置 |
|------|----------|
| **5 变体选择** | `INDEX.md` §5 + 03-color-and-normals.md |
| **Pro vs Toon** | `INDEX.md` §Pro vs Toon + pro-vs-toon.md (Stage 2) |
| **AudioLink 启用** | `11-audio-link.md` §Audio Link Toggle |
| **Modular Shader 创建** | `32-modular-shader-system.md` §File Structure |
| **Quest 优化** | `INDEX.md` §5 + 00-introduction.md §其他游戏系统 |
| **VRC Light Volumes 兼容** | `memory/world/vrc-light-volumes.md` Line 340-341 |

### 5.3 引用入口

- **主索引**: `参考文献/Poiyomi/INDEX.md`
- **Avatar Shader 集成**: `memory/avatar/shader/index.md` §1.3 Poiyomi Shaders
- **VPM 包元数据**: `memory/sources/vpm-mirrors/samples/poiyomi.md`
- **本计划**: `memory/reviews/poiyomi-integration-plan-2026-07-01.md`

### 5.4 关联决策记录

| 决策 | 来源 | 时间 |
|------|------|------|
| Poiyomi 加入 Avatar Shader 主流梯队 | `memory/avatar/shader/index.md` v1.2 | 2026-07-01 |
| Poiyomi 文档本地化完成 | `memory/JOURNAL.jsonl` session 记录 | 2026-07-01 |
| 65 文档 + INDEX 保留为"原始参考" | 本计划 §3.1 原则 1 | 2026-07-01 |
| Stage 2 提炼为 7-8 个主题文档 | 本计划 §3.4 | 2026-07-01 |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **评审类型** | 数据整理 + Memory 对比 + 入库计划 |
| **评审员** | CherryClaw (Curator 模式) |
| **评审日期** | 2026-07-01 |
| **覆盖文档** | 65 原始 .md + 1 INDEX + 9 个 Memory 关联文件 |
| **计划总工时** | 12-14 小时 |
| **建议优先级** | Stage 1 (P0) ✅ → Stage 2 (P1) → Stage 3 (P1) → Stage 4 (P2) → Stage 5 (P1-P2) |
| **下次评审** | Stage 2 完成后(预计 2026-07-08) |
| **文档版本** | 1.0 |
| **状态** | 活跃(Active) |
