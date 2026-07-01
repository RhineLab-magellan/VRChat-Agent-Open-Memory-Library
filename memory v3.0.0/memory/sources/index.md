---
title: Sources — 来源分类与导航
category: sources

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "Sources Index"
  - 来源索引
  - Sources
  - 参考工程索引

related:
  - "sources/open-source-projects.md"
  - "sources/example-central.md"
  - "sources/ulocalization.md"
  - "sources/sardinal.md"
  - "sources/vvmw.md"
  - "sources/udonvoiceutils.md"
  - "sources/quickbrown-luraswitch2.md"
  - "hybrid/udon-world-plugins.md"
  - FACT.md
  - "patterns/index.md"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Sources — 来源分类与导航

> 状态: ✅ 11 个来源文件已分类(含 QuickBrown LuraSwitch2 双重身份 A6+C15 + TLP UdonVoiceUtils + HoshinoLabs ULocalization + HoshinoLabs Sardinal)

---

## 概述

本目录记录知识库中的**信息源**。每个来源标注：
- 可信度（Tier A/B/C）
- 维护状态
- 知识库引用

**核心原则**: Evidence supports conclusions, but **is not the conclusion itself**。来源必须通过验证才能晋升到 `memory/rules/`、`memory/api/`、`memory/patterns/`。

---

## 信任层级

| Tier | 类型 | 处理方式 |
|------|------|----------|
| **A** | 官方文档、官方源码、直接验证 | 直接采纳为 FACT |
| **B** | 高质量开源项目、跨验证发现 | 采纳但标注项目来源 |
| **C** | 社区帖子、Discord 分享 | 标记为【未验证】+ 列入 `community-notes.md` |

---

## 来源文件分类

### 🏛 官方文档源

| 文档 | 内容 | Tier | 状态 |
|------|------|------|------|
| **[official-docs.md](official-docs.md)** | VRChat/UdonSharp 官方文档 URL + 版本信息 | A | ⚠️ 占位为主 |

**对应本地化**: `memory/world/udon/` (15+ 文档)、`memory/world/scene-components/` (9 文档)、`memory/world/examples/` (10+ 文档)

### 🌍 社区来源

| 文档 | 内容 | Tier | 状态 |
|------|------|------|------|
| **[community-notes.md](community-notes.md)** | 社区工程经验记录 | C | ⚠️ 仅有模板，待填充 |

**使用指南**: 社区来源的工程经验先在 `community-notes.md` 暂存，验证后再晋升到 `patterns/` 或 `rules/`

### 🛠 开发工具源

| 文档 | 内容 | Tier | 状态 |
|------|------|------|------|
| **[clientsim.md](clientsim.md)** | ClientSim 编辑器模拟工具 | A | ✅ 完整 |
| **[example-central.md](example-central.md)** | Example Central 使用 | A | ✅ 完整 |
| **[vrc-avatar-performance-tools.md](vrc-avatar-performance-tools.md)** ⭐NEW | Thry Avatar Evaluator + VRAM Checker(409 Stars / 7 项官方未覆盖指标 + PC/Quest 双套 VRAM 阈值) | A | ✅ 完整 (2026-06-17) |

**关联**: `memory/world/clientsim/` (4 系统文档 + 3 编辑器文档) 详细记录 ClientSim 架构
**关联**: `memory/avatar/thry-avatar-evaluator-metrics.md` — 工具检测的 7 项指标详细阈值与方法

### 📦 开源项目源

| 文档 | 内容 | Tier | 状态 |
|------|------|------|------|
| **[open-source-projects.md](open-source-projects.md)** | 开源项目参考 | A | ✅ 完整 |
| **[quickbrown-luraswitch2.md](quickbrown-luraswitch2.md)** | QuickBrown LuraSwitch2 通用开关+滑块组件库 | B | ✅ 完整 (2026-06-20) |
| **[udonvoiceutils.md](udonvoiceutils.md)** ⭐NEW | TLP UdonVoiceUtils 玩家语音/音频动态控制库 | B | ✅ 完整 (2026-06-20) |
| **[ulocalization.md](ulocalization.md)** ⭐NEW | HoshinoLabs ULocalization Unity Localization 的 UdonSharp 适配层 | A | ✅ 完整 (2026-06-20) |
| **[sardinal.md](sardinal.md)** ⭐NEW | HoshinoLabs Sardinal UdonSharp 通用消息总线(Pub/Sub with parameters) | A | ✅ 完整 (2026-06-20) |

**涵盖项目**: 多机位导演系统(参考工程), 视频播放器(参考工程), 音频同步系统(参考工程), QuickBrown LuraSwitch2(参考工程), **TLP UdonVoiceUtils(参考工程)**, **HoshinoLabs ULocalization(参考工程)**, **HoshinoLabs Sardinal(参考工程)**, lilToon, SCSS, ORL, Filamented, UnlitWF, VPM Package Template, VRChat Agent Skills(参考工程), VRCX(参考工程)

**QuickBrown LuraSwitch2 沉淀内容**:
- 6 个新 Pattern 文档(master-follower-syncer / exclusive-control-selector / soft-detent-interpolation / fade-then-snap / editor-preview-component / material-propertyblock-safe-update)
- 4 个新 FAIL 案例(FAIL-29 ~ FAIL-32)
- **双重身份**: A6 案例研究 (`memory/sources/quickbrown-luraswitch2.md`) + C15 工具使用指南 (`memory/world/luraswitch2.md`)
- 创作者可直接从 BOOTH 下载使用：https://booth.pm/en/items/1969082

**TLP UdonVoiceUtils 沉淀内容** (2026-06-20 ⭐NEW):
- **10 个核心模式** (已登记到 `patterns/index.md` 14-23 号):
  - 双副本同步模型 (Dual-Copy Sync) / 执行顺序链 (ExecutionOrder Chain) / 策略模式 (Strategy Pattern) / 对象池化 (Object Pool) / 优先级仲裁 (Priority Arbitration) / Master 所有权三层防御 / Gizmos 关系可视化 / Trigger 事件兜底 / 编译期 DEBUG 剥离 / 自动宏定义
- **8 大难题与解决方案** (P0-P3 分级)
- **完整架构 8 层职责** (Controller / Model / Override / OverrideList / OcclusionStrategy / View / IgnoredPlayers / Pool)
- **VRChat Player Audio API 完整列表** (UVU 涉及的所有 Setter + 部分 Getter)

**HoshinoLabs ULocalization 沉淀内容** (2026-06-20 ⭐NEW):
- **5 个 Udon 沙箱适配核心模式** (已登记到 `patterns/index.md` 24-28 号):
  - 哈希方法分派 (Hash-Based Method Dispatch) / 整数身份映射 (IID Object Identity) / 槽位参数传递 (Slot-Based Parameter Passing) / 代码生成 + 类型擦除 (Code Generation with Type Erasure) / 构建时与运行时分离 (Build-Time vs Runtime Separation)
- **工程参数**: 145 个 .cs / 27 个 Shim 字段 / 500+ 哈希方法 / 16 种 IVariable 类型 / 100+ Component 类型分派白名单
- **架构核心**: God Shim 模式 + Sardinal Signal + Sardinject DI 容器 + 大量代码生成
- **特殊机制**: CloneDetector 重建 VRCPlayerObject 引用 + SmartLiteFormatter 重写 SmartFormat 子集

**HoshinoLabs Sardinal 沉淀内容** (2026-06-20 ⭐NEW):
- **3 个 Sardinal 独有新模式** (已登记到 `patterns/index.md` 29-31 号):
  - 频道路由 (Channel-Based Pub/Sub Routing) / 基类订阅者继承 (Inherited Subscriber) / 静态+动态双订阅 (Hybrid Static+Dynamic Subscription)
- **5 大 ULocalization 模式精简版**: Sardinal 与 ULocalization 共享 5 大沙箱适配模式但**不重复沉淀**;Sardinal 实现更精简(10 字段 vs 27 字段;类型 hash vs 方法 hash)
- **工程参数**: 36 个 .cs / 10 个 Shim 字段 / 16 个 Publish 重载 / Sardinject DI 容器依赖
- **架构核心**: God Shim 模式 + Sardinal Signal + Sardinject DI 容器(与 ULocalization 同思想)+ 3 层代码分离(Runtime + Runtime/Udon + Editor/Udon)
- **特殊机制**: 频道路由三态过滤 + 基类订阅者递归反射 + `_7[i]++` 动态扩容

### 📦 VPM 包开发源

| 文档 | 内容 | Tier | 状态 |
|------|------|------|------|
| **[vpm-package-template.md](vpm-package-template.md)** | VPM Package 开发模板 | A | ✅ 完整 |
| **[vpm-mirrors/vcc-vrczh.md](vpm-mirrors/vcc-vrczh.md)** ⭐NEW 2026-07-01 | VCC vrczh 镜像站元数据 + 57 个 VPM repo 完整列表 | A | ⚠️ 示例流程 (7/57 包详细, 12.3%) |
| **[vpm-mirrors/samples/](vpm-mirrors/samples/index.md)** ⭐NEW 2026-07-01 | 7 个示例包详细文档 (curated, official, nadena, anatawa12, lilxyzw, poiyomi, vrcfury, hai-vr) | A | ⚠️ 示例流程 |

**vpm-mirrors 内容**:
- 站点: <https://vcc.vrczh.org/> (VRCD 社区维护的 VPM 镜像)
- API 端点:
  - `https://vpm.vrczh.org/vpm/repos` — **完整 57 个 repo** (推荐入口)
  - `https://vpm.vrczh.org/repos?page=N&count=10` — 分页 API (含 description 但都是占位符 "Description")
  - `https://vpm.vrczh.org/vpm/{apiId}` — 单个 repo VPM index
- 完整 57 个 apiId 列表 (含 镜像 URL / 上游 URL / 同步状态)
- 7 个核心包详细 (官方 SDK, MA, AAO, lilToon, Poiyomi, VRCFury, Haï~)
- 已识别 7 类模式 (描述缺失, Unity 标注陷阱, 同步失败, 重复 apiId, 仓库废弃, mirror 注入, 字节数异常)

**vpm-package-template 内容**: GitHub Actions CI/CD、VPM CLI、Repo Listing 格式

### 🔌 VRChatSDK 外部 API 源

| 文档 | 内容 | Tier | 状态 |
|------|------|------|------|
| **[vrcx.md](vrcx.md)** | VRCX 工具参考 | A | ✅ 完整 |

**说明**: VRCX 是 VRChat 第三方工具，提供 API 调试辅助

---

## 来源 → 知识库映射

```
official-docs.md
    ↓
world/udon/ (15+ 文档)
world/scene-components/ (9 文档)
world/examples/ (10+ 文档)

clientsim.md + open-source-projects.md
    ↓
world/clientsim/ (4 系统文档)
FACT.md §多机位导演系统(参考工程) / §视频播放器(参考工程) / §音频同步系统(参考工程)
avatar/shader/ (5 家族 30+ 文档)
world/performance-guide.md

vpm-package-template.md
    ↓
未直接入库（仅作 VPM 开发参考）
```

---

## 使用工作流

### 添加新知识时

```
1. 识别来源
   ↓
   - 官方文档 → 直接写入目标位置
   - 社区帖子 → 先 community-notes.md
   - 源码 → 按 Trust Tier 处理

2. 验证（必要时）
   ↓
   - Tier A: 信任
   - Tier B: 多源交叉验证
   - Tier C: 需要独立测试

3. 分类存储
   ↓
   - 概念/API → memory/api/ 或 memory/world/
   - 规则 → memory/rules/
   - 模式 → memory/patterns/
   - 阶段报告 → 特殊Agent提示词/

4. 更新来源文件
   ↓
   - 添加新源到对应 sources/ 文档
   - 更新本 index.md
```

### 引用来源时

```
1. 在 memory 文件中标注 Source 字段
   ↓
2. 必要时分级标注置信度
   - FACT (Tier A 直接采纳)
   - INFERENCE (基于 FACT 推导)
   - UNKNOWN (Tier C 待验证)
```

---

## 来源元数据标准

每个 memory 文件应在开头标注：

```markdown
> Last Verified: YYYY-MM-DD
```

---

## 当前缺口

| 缺口 | 建议 |
|------|------|
| `official-docs.md` 仅占位 | 建议合并到 `vrchatsdk/homepage.md` 或扩展内容 |
| `community-notes.md` 无实际记录 | 建议在出现新社区经验时填充 |
| `references/` 仅 1 个文件 | 建议增加跨项目对比分析 |

---

## 关联目录

| 目录 | 关系 |
|------|------|
| `memory/references/` | 对比分析、跨验证记录 |
| `特殊Agent提示词/` | 阶段报告(取代 V3.0 前的 journal/) |
| `memory/FACT.md` | 案例研究来源标注(多机位导演系统 / 视频播放器 / 音频同步系统 参考工程) |
