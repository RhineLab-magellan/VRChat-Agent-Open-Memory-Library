---
title: FACT.md - VRChat 技术知识库
category: misc

knowledge_level: applied
status: active

tags:
  - misc
  - knowledge-graph
  - meta

aliases:
  - FACT
  - 知识库事实库
  - "Knowledge Base Facts"
  - 顶层索引

related:
  - index.md
  - _always-load.md
  - "sources/index.md"
  - "patterns/index.md"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# FACT.md - VRChat 技术知识库

> 长期有效的事实、决策、项目状态

---

## 知识库结构

```
memory/
├── avatar/                    # Avatar 相关
│   ├── shader/               # Shader 知识库
│   │   ├── index.md          # 索引
│   │   ├── liltoon/         # lilToon 详细文档（16个文件）
│   │   ├── scss/            # SCSS 详细文档
│   │   ├── orl/             # ORL Shaders World 通用着色器（NEW 2026-06-11）
│   │   ├── filamented/      # Filamented PBR 着色器 (NEW 2026-06-11)
│   │   └── unlitwf/         # UnlitWF Unlit 扩展专业效果 (NEW 2026-06-11)
│   ├── vrc-constraints.md    # VRC Constraints
│   ├── playable-layers.md   # Playable Layers
│   ├── optimization-guide.md
│   ├── performance-rank.md
│   └── ...（其他 Avatar 文档）
├── world/                    # World 相关
│   ├── performance-guide.md # World 性能优化
│   ├── vrc-light-volumes.md  # VRCLightVolumes 光照系统
│   ├── occlusion-culling-guide.md  # 遮挡剔除优化
│   ├── reflection-probes.md  # 反射探针系统
│   ├── examples/             # SDK 内置示例(NEW 2026-06-15)
│   │   └── udon-example-scene/  # Udon Example Scene 13+ Prefab
│   │       ├── index.md
│   │       ├── avatar-scaling-settings.md
│   │       ├── player-mod-setter.md
│   │       ├── simple-pen-system.md
│   │       ├── udon-video-sync-player.md
│   │       └── world-audio-settings.md
│   ├── data-containers.md    # Data Lists/Dicts/VRCJson
│   ├── creator-economy.md    # 创作者经济 SDK
│   ├── scene-components/     # Scene Components 子分类(NEW 2026-06-15)
│   │   ├── index.md          # Scene Components 总览(9 核心组件 + 1024 限制)
│   │   ├── textmeshpro.md    # TextMesh Pro 集成/字体/Fallback
│   │   ├── vrc-avatarpedestal.md
│   │   ├── vrc-cameradolly.md
│   │   ├── vrc-mirrorreflection.md
│   │   ├── vrc-objectsync.md # ⭐核心:物理对象同步
│   │   ├── vrc-portalmarker.md
│   │   ├── vrc-scenedescriptor.md # ⭐World 必含核心
│   │   ├── vrc-station.md
│   │   └── vrc-enablepersistence.md
│   └── bakery/              # Bakery 光照烘焙
├── vrchatsdk/                # VRChatSDK (HTTP API, 外部应用)
│   ├── 01_首页.md            # 层级概览
│   ├── 02_TypeScript_SDK.md
│   ├── 03_Websocket_API.md
│   ├── 04_Instances.md
│   ├── 05_Tags.md
│   ├── 06_FAQ.md
│   ├── 07_API_认证.md
│   ├── 08_API_用户.md
│   ├── 09_API_世界.md
│   ├── 10_API_Avatar.md
│   ├── 11_API_好友.md
│   ├── 12_API_通知.md
│   ├── 13_API_收藏.md
│   ├── 14_API_实例.md
│   ├── 15_API_文件.md
│   ├── 16_模型_User.md
│   ├── 17_模型_CurrentUser.md
│   └── 18_API_群组.md
├── platform/                 # 跨平台开发
│   ├── android-development.md
│   ├── cross-platform-content.md
│   ├── mobile-ui-optimization.md
│   └── easyquestswitch.md      # EasyQuestSwitch PC/Quest 切换工具 (NEW)
├── hybrid/                   # Hybrid 系统
│   └── osc-protocol.md      # OSC 完整协议数据库
├── sources/
│   ├── clientsim.md          # ClientSim VRChat 编辑器模拟工具 (NEW 2026-06-10)
│   ├── example-central.md    # Example Central 使用 (NEW)
│   ├── vpm-package-template.md # VPM Package 开发模板 (NEW 2026-06-10)
│   └── open-source-projects.md # 开源项目参考
└── api/                      # API 参考
    ├── networking.md         # 已更新：UdonSyncMode 插值模式 (2026-06-10)
    ├── udonsharp-runtime.md  # UdonSharpBehaviour 运行时系统 (NEW 2026-06-10)
    ├── events-reference.md   # Udon 事件完整参考
    ├── persistence.md        # 持久化 API
    ├── udon-type-exposure.md     # Udon Type Exposure Tree 索引 (NEW 2026-06-11)
    ├── exposed-types.md         # 已暴露类型详细清单 (NEW 2026-06-11)
    ├── not-exposed.md           # 未暴露 API 黑名单 (NEW 2026-06-11)
    └── api-checker.md           # API 检查器/代码模式 (NEW 2026-06-11)
└── journal/                    # 会话记忆（临时，定期清理）
    ├── README.md               # 目录说明
    ├── sessions/               # 会话记录 (30天)
    ├── reviews/                # 审查记录 (60天)
    ├── issues/                 # 问题追踪 (关闭后7天)
    └── drafts/                 # 临时草稿 (7天)
```

---

## ⚠️ 核心约束（绝对规则）

### 渲染管线

> **🔴 最高优先级：VRChat 只支持 BRP (Built-in Rendering Pipeline)**

| 规则 | 说明 |
|------|------|
| **只支持 BRP** | VRChat **只支持** Built-in Rendering Pipeline |
| **禁止切换管线** | 任何更改渲染管线的行为都是**致命的** |
| **禁止 URP/HDRP** | 项目中不得使用 Universal 或 High Definition Render Pipeline |
| **Unity 版本绑定** | SDK 3.4.2+ 绑定 Unity 2022.3.22f1（LTS） |

**违反后果**：切换渲染管线会导致 VRChat 项目完全无法工作。

### Editor 脚本与构建

> 🔴 **任何引用 `UnityEditor.*` 命名空间的脚本必须放在 `Editor` 文件夹内**

| 规则 | 说明 |
|------|------|
| **根因** | 脚本先在编辑器下编译（包含 `UnityEditor` 程序集），再为目标平台重新编译（**不包含** `UnityEditor` 程序集） |
| **触发条件** | `using UnityEditor;` 等编辑器命名空间 |
| **解决路径 1** | 将脚本放到**父目录为 `Editor`** 的任意路径下，构建时自动排除 |
| **解决路径 2** | 创建 asmdef，**Include Platforms** 仅勾选 Editor |

**常见场景**（VRChat World 开发中）：
- 自定义 Inspector (`[CustomEditor]`)
- Gizmo 调试 (`OnDrawGizmos`)
- Build Pipeline 后处理 (`IPreprocessBuildWithReport`)
- AssetPostprocessor
- AssetDatabase / EditorUtility / EditorPrefs 调用

**易错点**：
- ❌ 脚本必须挂在 GameObject 上才能编译 → 实际由**文件夹路径**决定
- ❌ 用 `Assets/Scripts/MyEditor.cs` → 跨平台构建时找不到 `UnityEditor` 程序集，报错
- ✅ 用 `Assets/Editor/MyEditor.cs` 或 `Assets/Scripts/Editor/MyEditor.cs` → 正常

**参考**：
- Unity 特殊文件夹：https://docs.unity3d.com/6000.3/Documentation/Manual/SpecialFolders.html

---

## 知识库修正记录 (2026-06-05~06)

### 新增参考工程
| 项目 | 说明 |
|------|------|
| VRCTD (VRChat Technical Director) | 多机位相机跟踪与切换系统，5 层网络同步体系(参考工程,已沉淀) |

### 域名更正
| 项目 | 修正 |
|------|------|
| Udon Graph | ❌ 标记过时，社区不建议使用 |
| VRCFury World | ❌ 不存在，删除 |
| VRC Constraints | ✅ Avatar 域，已入库 |
| **MA 教程深度精读** | ✅ 6 教程原文精读 + 玩家视角操作 + 验证 + 易错点 + 教学衔接 (2026-06-17) |
| **MA 教学法具体技术** | ✅ 5 大玩家友好设计 + 句式清单 + 反面教材 + 应用模板 (2026-06-17) |
| **MA Samples 实战案例** | ✅ Fingerpen + Clap 拆解（§9.6）+ 3 条新教学原则（43-45）(2026-06-17) |

### 优先级调整
| 项目 | 调整后 |
|------|--------|
| VRCFury Avatar | ⚠️ 仍活跃维护（2026-05-02），与 MA 功能重叠 + 共存冲突 + 非 VPM 分发 → 大多数场景用 MA 代替；**深度更新(2026-06-17)**: Parameter Compressor (16 bit 压参数) + Direct Tree Optimizer + Blendshape Optimizer + 60+ 自动修复 + 全组件清单 → 详见 `avatar/vrcfury-reference.md` |
| Shader 优化实操 | 🔽 极低优先级 |
| Quest Avatar 适配 | 🔽 优先级下降 |
| OSC 协议整理 | ✅ 已完成 |
| VRC Constraints | ✅ 已完成 |
| Playable Layers | ✅ 已完成 |
| World 性能优化 | ✅ 已完成 |
| Bakery 光照烘焙 | ✅ 已完成 |
| EasyQuestSwitch | ✅ 已完成 (2026-06-10) |
| ClientSim | ✅ 已完成 (2026-06-10) |

### 知识库修正 (2026-06-09)
| 操作 | 说明 |
|------|------|
| 删除 `avatar-vs-world-animator.md` | ❌ 学习方法文件，不应存储 |
| 知识整合到 `playable-layers.md` | Avatar 参数驱动系统 |
| 知识整合到 `animator-system.md` | World 逻辑驱动系统 + Udon API |

**原则**：只存储实际技术知识（How it works），不存储学习方法（How to learn）

---

## 知识库更新 (2026-06-10)

### 来源 1: VRChat Creator Docs
- URL: https://deepwiki.com/vrchat-community/creator-docs
- 索引日期: 2026-06-04 (commit 8be404)
- 原始仓库: github.com/vrchat-community/creator-docs

### 来源 2: EasyQuestSwitch
- URL: https://deepwiki.com/vrchat-community/EasyQuestSwitch
- 索引日期: 2025-07-03 (commit 283e873)
- 原始仓库: github.com/vrchat-community/EasyQuestSwitch

### 来源 3: VRChatSDK (HTTP API)
- vrchat.community: 社区维护的 API 文档（非官方）
- vrchat.hexdocs.pm: vrchat v1.20.0 (Elixir SDK)
- 文献位置: `memory/vrchatsdk/` (18 个文档，已本地化)

### 新增文件
| 文件 | 说明 |
|------|------|
| `world/vrc-graphics.md` | VRCGraphics.Blit, VRCShader.SetGlobal, Shader Globals |
| `world/data-containers.md` | Data Lists/Dicts/Tokens, VRCJson, JSON 同步 |
| `world/creator-economy.md` | Store API, Product API, 示例 Prefabs |
| `platform/android-development.md` | Quest 开发、着色器限制、Armature 要求 |
| `platform/cross-platform-content.md` | 平台切换、Avatar 一致性要求 |
| `platform/mobile-ui-optimization.md` | VRC_UIShape, Focus View, 触摸目标 |
| `platform/easyquestswitch.md` | **EasyQuestSwitch PC/Quest 切换工具** |
| `sources/example-central.md` | Example Central 使用、版本管理 |
| `vrchatsdk/01_首页.md` ~ `18_API_群组.md` | **VRChatSDK HTTP API 文档** (18个文件) |

### 更新文件
| 文件 | 新增内容 |
|------|---------|
| `api/networking.md` | 带宽限制 (~11KB/s, 280KB/200B), [NetworkCallable] (SDK 3.8.1+) |
| `api/persistence.md` | 压缩行为 (~300KB → 100KB) |

### 冲突记录
- 位置: `memory/references/creator-docs-comparison.md`
- 待用户判定: 无重大冲突，发现的差异已记录

### VRCShader.SetGlobal 限制
> 属性名必须以 `_Udon` 为前缀（用于全局设置）

### Networking Specs
- 总带宽: ~11 KB/s
- Manual sync: 280,496 bytes/serialization
- Continuous sync: ~200 bytes/serialization

### Persistence Compression
- 实际存储: 100 KB/player/world（压缩后）
- 可压缩数据: ~300 KB 原始数据

---

## 高优先级知识（已完成）

### Avatar Pipeline
- VRCPipelineManager ✅
- Avatar 3.0 四行架构 ✅

### VRC Constraints (Avatar 域)
- 6 种约束类型 ✅
- 高级设置（Local Space/Freeze To World）✅
- 性能分类（Count/Depth）✅
- Constraints API ✅

### Playable Layers
- Humanoid vs Generic ✅
- 5 层详解（Base/Additive/Gesture/Action/FX）✅
- Avatar Mask 规则 ✅
- T-Pose/IK Pose/Sitting Pose ✅
- **Avatar Animator = 参数驱动系统** ✅（核心：Expression Menu → Parameter → Playable Layer → Animator）

### Unity Animator（World 上下文）
- **World Animator = 逻辑驱动系统** ✅（核心：Udon Event → SetBool/SetTrigger → State Machine）
- Udon Animator API（SetBool/SetFloat/SetTrigger/SetInteger/Play/CrossFade）✅
- 网络同步注意事项 ✅

### World 性能优化
- 预算规划 ✅
- 材质/Shader/纹理管理 ✅
- 光照系统（烘焙/动态）✅
- 测试方法 ✅

### Bakery 光照烘焙 ✅
- 系统要求（Windows + NVIDIA Kepler+）✅
- 6 种 Render Mode ✅
- 5 种 Directional Mode ✅
- 8 种组件 ✅
- 材质兼容性 ✅
- FAQ + 故障排除 ✅

### OSC 协议
- 完整协议数据库 ✅

### 音频同步系统架构 ✅ (参考工程)
- **纹理编码数据传递**：音频数据通过 CustomRenderTexture 传递 Shader，零网络同步开销
- **时间同步系统**：Master 权威时间锚点 + 双时间源融合 + 漂移校正
- **同步策略**：Manual Sync + Owner Transfer 混合模式
- **位域压缩**：byte 存储多个 bool(`_flags`)→ 详见 `memory/world/udon/data-containers/byte-and-bit-operations.md`
- **性能热点**：SendAudioOutputData 每帧 8 次 SetFloatArray(约 2ms 开销)
- **实验性功能保护**：audioDataToggle 默认关闭(VRCAsyncGPUReadback 成本高)

> **📚 参考实现**:本节提炼自开源 VRChat 音频同步框架,见 `memory/sources/open-source-projects.md` §音频同步类目

### 多机位导演系统网络同步架构 ✅ (2026-06-06)(参考工程)
- **5 层同步体系**：Manual + Continuous + NetworkCallable + SafeMod(排除) + NoVariableSync
- **NetworkCallable RPC**：参数化远程调用 + 批量延迟提交
- **双缓冲预览模式**：`_isPreviewActive` + `_serializationPending`
- **指数衰减插值**：Continuous 值平滑(Compensation 因子)
- **Slerp/Slerp 本地缓动**：位置+旋转独立插值
- **所有权分层**：操作者 vs 被跟踪者所有权分离
- **UI 转发模式**：NoVariableSync + SetProgramVariable

> **📚 参考实现**:本节提炼自开源 VRChat 多机位导演系统,见 `memory/sources/open-source-projects.md` §多机位导演类目

---

## 核心设计模式与案例研究索引（精简版）

> 以下为知识库中已验证的核心设计模式和案例研究索引。
> 完整实现代码、详细架构分析、对比表格均在对应文档中，按需检索。

| 类别 | 数量 | 索引位置 |
|------|------|---------|
| 核心设计模式 | 14 个 | `memory/patterns/index.md` + 各模式独立文档 |
| LuraSwitch2 实战模式 | 6 个 | `memory/patterns/index.md` #8-#13 |
| UdonVoiceUtils 工程化模式 | 10 个 | `memory/patterns/index.md` #14-#23 |
| ULocalization 沙箱适配模式 | 5 个 | `memory/patterns/index.md` #24-#28 |
| Sardinal 消息总线模式 | 3 个 | `memory/patterns/index.md` #29-#31 |
| 案例研究 A1-A9 | 9 个 | `memory/sources/open-source-projects.md` |
| 推荐工具 C1-C16 | 16 个 | `memory/hybrid/udon-world-plugins.md` |

**快速查阅入口**：
- 网络同步：`memory/patterns/manual-sync-state.md` / `advanced-sync-patterns.md`
- 沙箱适配：`memory/patterns/hash-based-dispatch.md` / `build-time-vs-runtime-separation.md`
- 消息总线：`memory/patterns/channel-routing.md` / `hybrid-subscription-modes.md`
- 视频同步：`memory/sources/vvmw.md`（案例）/ `memory/world/vvmw.md`（工具）
- Shader 选型：`memory/avatar/shader/index.md`
- VRChatSDK 概览：`memory/vrchatsdk/index.md`

---

## 最后更新



## Memory Curator 初始化 (2026-06-11)

| 操作 | 说明 |
|------|------|
| UnlitWF Shader | 新建 UnlitWF Unlit 扩展专业效果知识库（2026-06-11）|
| ORL Shaders | 新建 World 通用着色器知识库（2026-06-11）|
| Hybrid 域索引更新 | 状态修正：OSC + 音频同步(参考工程) 已完成 |
| Avatar 域索引更新 | 状态修正：Dynamics/SDK/Shader 已收录 |
| Filamented Shader | 新增 PBR 着色器知识库（2026-06-11）|
| VRChatSDK 本地化 | 已复制 18 个文档到 `memory/vrchatsdk/` |
| FACT.md vrchatsdk 修正 | 已本地化到 `memory/vrchatsdk/` (18 个文档) |
| creator-docs 对比记录 | 已本地化到 `memory/references/` |
| memory/index.md 更新 | 同步所有域状态，添加 VRChatSDK 域路由 |
| _always-load.md 更新 | 同步所有域状态，添加 VRChatSDK 索引 |
| Journal 目录创建 | 新建 `memory/journal/` 及子目录 (sessions/reviews/issues/drafts)，更新 index.md 和 _always-load.md 路由 |

## 知识完整性原则

> ⚠️ **所有知识库索引必须指向 memory/ 目录内部**
> - 外部文档随时可能删除或丢失
> - 工具安装链接（VPM/BOOTH）可以保留（操作指引，非知识本身）
> - 知识来源路径必须本地化（`参考工程/`、`参考文献/`）

---

## 知识库维护状态 (2026-06-15)

### 总体规模（2026-06-15 二次审计后）
- **总文件数**: 253（首次审计后 248 → 二次审计 +5）
- **子目录数**: 18
- **索引文件**: 11 个（+4 新增 vrchatsdk/platform/misc/references，+1 outline.md 修复）
- **journal session 记录**: 3 个（2026-06-11、2026-06-15 第一次、2026-06-15 第二次）

### 信任层级分布
| Tier | 类型 | 文件数估计 |
|------|------|-----------|
| **A** | 官方文档/源码 | ~100 |
| **B** | 高质量社区项目 | ~50 |
| **C** | 推断/社区帖子 | ~10 |

### 完整性状态
- ✅ **11 个 index.md 已就位** (2026-06-15 二次审计后,首次+二次)
  - `api/index.md` (16 个 API 文件)
  - `rules/index.md` (7 个 Rule Set)
  - `patterns/index.md` (7 个核心模式)
  - `sources/index.md` (7 个来源)
  - `reviews/index.md` (3 个审查文档)
  - `vrchatsdk/index.md` ⭐NEW 2026-06-15 二次审计(18 个 SDK 文档)
  - `platform/index.md` ⭐NEW 2026-06-15 二次审计(4 个平台文档)
  - `misc/index.md` ⭐NEW 2026-06-15 二次审计(3 个杂项文档)
  - `references/index.md` ⭐NEW 2026-06-15 二次审计(1 个参考资料)
  - `avatar/shader/liltoon/index.md`(已就位)
  - `avatar/shader/index.md`(已就位)
- ✅ **3 个重复内容已迁移** (2026-06-15 首次重构)
  - `world/udonsharp-compilation.md` → `world/udon/udonsharp/compilation.md`
  - `world/data-containers.md` → `world/udon/data-containers/index.md`
  - `world/vrc-graphics.md` → `world/udon/vrc-graphics/index.md`
- ✅ **3 个空 journal 子目录已添加 .gitkeep** (2026-06-15 首次重构)
- ✅ **1 个断链修复** (2026-06-15 二次审计)
  - `avatar/shader/liltoon/outline.md` 创建(被 7 个文件引用,内容来自 `advanced-settings.md`)

### 知识缺口（已识别未建设）
- Expression Menu/Parameter 完整文档
- Avatar↔World 接触驱动 World 模式
- 跨域架构设计模式
- Quest 兼容性约束表
- Avatar Audio 空间音效最佳实践
- 常见 Avatar 审核失败原因
- 外部系统集成案例

### 命名一致性
- ✅ 主文档: `kebab-case.md`
- ✅ 子目录: `kebab-case/`
- ⚠️ `vrchatsdk/`: 中英混合命名（建议未来统一）