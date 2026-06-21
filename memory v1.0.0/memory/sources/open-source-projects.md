# Open Source Projects — 知识库溯源层

> Type: SOURCE
> Last Updated: 2026-06-20
>
> **2026-06-20 更新**: 新增 A6 案例研究型参考工程 `QuickBrown LuraSwitch2`,沉淀 6 个新 Pattern + 4 个新 FAIL
>
> **2026-06-20 更新**: 新增 A7 案例研究型参考工程 `TLP UdonVoiceUtils` (Guribo),沉淀 10 个新 Pattern + 8 个新 FAIL/难题
>
> **2026-06-20 更新**: 新增 A8 案例研究型参考工程 `HoshinoLabs ULocalization` (ikuko),沉淀 5 个新 Pattern(全部聚焦"Udon 沙箱适配")
>
> **2026-06-20 更新**: 新增 A9 案例研究型参考工程 `HoshinoLabs Sardinal` (ikuko,同作者),沉淀 3 个 Sardinal 独有新 Pattern(Channel Routing 频道路由 + Inherited Subscriber 基类继承 + Hybrid Static+Dynamic Subscription 双订阅);Sardinal 是 ULocalization 的精简+通用化版本(36 .cs vs 145 .cs;10 字段 vs 27 字段)
>
> **2026-06-20 更新**: A6 LuraSwitch2 升级为**双重身份**（A6 案例研究 + C15 工具使用指南），新增 `memory/world/luraswitch2.md` 工具文档
>
> **2026-06-20 更新**: A2 VVMW (VizVid) 升级为**双重身份**（A2 案例研究 + C16 工具使用指南），新增 `memory/world/vvmw.md` 工具文档（5 大模块 + 9 大集成 + 13 个 Releases + PC/Quest 跨平台）
>
> **⚠️ 本目录是知识库溯源层**
>
> 本目录(`memory/sources/`)记录**所有参考工程和开源项目**的原始信息,作为知识主目录(`rules/`、`api/`、`patterns/`、`world/`、`avatar/`、`hybrid/`)中"去项目化"内容的**唯一溯源依据**。
>
> **设计原则**:
> - 知识主目录中的内容已"去项目化"(删除项目名/作者/Stars 等元数据)
> - `sources/` 目录保留所有项目元数据,**作为唯一溯源来源**
> - 知识主目录通过 "📚 参考实现" 链接到 `sources/`
> - **本目录是知识库完整性的基石**,不允许删除

---

## 知识库参考工程分类

### 🅰️ 案例研究型参考工程(8 个)

| 序号 | 项目 | 文档 | 沉淀位置 |
|------|------|------|---------|
| A1 | 多机位导演系统(VRCTD) | `memory/FACT.md` §多机位导演系统 | 5 层同步 + NetworkCallable + 双缓冲 + 指数衰减 + Slerp + 所有权分层 + NoVariableSync UI |
| **A2/C16** | **VizVid (VVMW)** | `memory/sources/vvmw.md` + `memory/world/vvmw.md` | **双重身份**: 案例研究沉淀 8 模式（Manual Sync + Owner Authority + 时间同步算法 + 阈值同步 + 冷却期 + 双缓冲 + Performer + Strategy）+ 工具推荐给创作者直接使用。5 大模块 + 9 大集成（AudioLink/LTCGI/VRCLightVolumes/Topaz/UdonAuth/YTTL）+ 13 个 Releases + PC/Quest 跨平台 + 12+ 语言本地化 |
| A3 | 音频同步系统(AudioLink) | `memory/FACT.md` §音频同步系统 + `memory/hybrid/audio-link.md` | Shader-Centric + Master 时间锚点 + 位域压缩 + 漂移校正 + 平台兼容预处理 |
| A4 | VRChat Agent Skills 模板(参考工程) | `memory/rules/`、`memory/patterns/advanced-sync-patterns.md` | SMART 原则 + 18 条 NEVER 清单 + 5 层存储决策框架 + 6 种 Networking Anti-Patterns |
| A5 | 第三方客户端(VRCX) | `memory/sources/vrcx.md` | API 客户端最佳实践 + 跨平台状态同步 UX |
| **A6/C15** | **QuickBrown LuraSwitch2 (Lura's Switch)** | `memory/sources/quickbrown-luraswitch2.md` + `memory/world/luraswitch2.md` | **双重身份**: 案例研究沉淀 6 模式 + 工具推荐给创作者直接使用。BOOTH 免费 + UV License。Master-Follower Syncer + Exclusive Selector + SoftDetent + Fade-Snap + Editor Preview + MaterialPropertyBlock + 4 个 FAIL 案例 |
| A7 | TLP UdonVoiceUtils (UVU) | `memory/sources/udonvoiceutils.md` | **10 个核心模式**: 双副本同步 + 执行顺序链 + 策略模式 + 对象池 + 优先级仲裁 + Master 所有权三层防御 + Gizmos 关系可视化 + Trigger 事件兜底 + 编译期 DEBUG 剥离 + 自动宏定义 |
| **A8** ⭐NEW 2026-06-20 | **HoshinoLabs ULocalization** | `memory/sources/ulocalization.md` | **5 个 Udon 沙箱适配核心模式**: Hash-Based Method Dispatch + IID Object Identity + Slot-Based Parameter Passing + Code Generation with Type Erasure + Build-Time vs Runtime Separation + CloneDetector + God Shim + SmartLiteFormatter |
| **A9** ⭐NEW 2026-06-20 | **HoshinoLabs Sardinal** | `memory/sources/sardinal.md` | **通用消息总线(Pub/Sub with parameters)** + 5 大 ULocalization 模式精简版(10 字段 vs 27 字段 + 16 Publish 重载 vs 3 槽位) + 3 个 Sardinal 独有新模式(Channel Routing 频道路由 / Inherited Subscriber 基类继承 / Hybrid Static+Dynamic Subscription 双订阅模式) |

> **设计说明**:这 9 个项目**不作为工具被创作者使用**,纯粹作为"案例研究"被分析,提炼出通用设计模式
> **沉淀位置**:知识已完全去项目化,沉淀到 FACT.md / patterns/ / rules/ 中,本目录仅作为溯源
> **更新策略**:当知识主目录需要更新时,先回查本目录的源信息

> **A2/C16 双重身份特例**：A2 VVMW (VizVid) 同时也是 C16 工具使用指南型——既提炼模式又直接可推荐使用。
> 案例研究视角看 `memory/sources/vvmw.md`，工具使用视角看 `memory/world/vvmw.md`。

> **A6/C15 双重身份特例**：A6 LuraSwitch2 同时也是 C15 工具使用指南型——既提炼模式又直接可推荐使用。
> 案例研究视角看 `memory/sources/quickbrown-luraswitch2.md`，工具使用视角看 `memory/world/luraswitch2.md`。

### 🅱️ 项目推荐型参考工程 — 完整元数据

**项目详情已沉淀到 `memory/avatar/shader/`,本节仅作为溯源索引**

| 序号 | 项目 | 完整文档 | 沉淀位置 |
|------|------|---------|---------|
| B1 | Avatar Toon Shader A | `memory/avatar/shader/liltoon/` | 16 文件 + 索引 |
| B2 | Cel Shading Shader(双阴影) | `memory/avatar/shader/scss.md` | 单文件 |
| B3 | World 模块化 Shader 套件 | `memory/avatar/shader/orl/` | 4 文件 + 索引 |
| B4 | Google Filament PBR 替代 | `memory/avatar/shader/filamented/` | 4 文件 + 索引 |
| B5 | Unlit 扩展专业效果 | `memory/avatar/shader/unlitwf/index.md` | 单文件 |

> **设计说明**:这 5 个项目**作为工具被创作者使用**(安装到 Avatar/World),保留项目名和 VPM 安装链接
> **元数据处理**:已删除 Stars/最后查看日期/作者/具体技术参数,保留项目名 + 优势描述 + VPM 链接

### 🅲️ 工具使用指南型参考工程 — 完整元数据

**项目详情已沉淀到 `memory/avatar/`,本节仅作为溯源索引**

| 序号 | 项目 | 完整文档 | 沉淀位置 |
|------|------|---------|---------|
| C1 | Avatar 自动化(MA) | `memory/avatar/modular-avatar.md` | 124K 完整文档 |
| C2 | Avatar 自动化(VRCFury) | `memory/avatar/vrcfury-reference.md` | 24K 完整文档 |
| C3 | Avatar 自动化(AAO) | `memory/avatar/avatar-optimizer.md` | 22K 完整文档 |
| C4 | Mesh 简化(Meshia) | `memory/avatar/meshia-mesh-simplification.md` | 20K |
| C5 | 贴图 Atlas 化(TTT) | `memory/avatar/tex-trans-tool.md` | 24K |
| C6 | MA 响应式层压缩(MA2BT) | `memory/avatar/ma2bt.md` | 20K |
| C7 | Avatar 性能检测 | `memory/avatar/lilAvatarUtils`、`memory/avatar/thry-avatar-evaluator-metrics.md` | — |
| C8 | Avatar 压缩(LAC) | `memory/avatar/lac-avatar-compressor.md` | 11K |
| C9 | PC/Quest 平台切换 | `memory/platform/easyquestswitch.md` | — |
| C10 | World 光照系统 | `memory/world/vrc-light-volumes.md` | 13K |
| C11 | 光照烘焙(Bakery) | `memory/world/bakery/` | 2 文件 |
| C12 | 编辑器模拟(ClientSim) | `memory/world/clientsim/` | 8 文件 |
| C13 | Creator Economy(SDK) | `memory/world/creator-economy.md` | — |
| C14 | Example Central(SDK) | `memory/sources/example-central.md` | — |
| **C15** ⭐NEW 2026-06-20 | **Lura's Switch (QuickBrown LuraSwitch2)** | `memory/world/luraswitch2.md` | 9 种开关 Prefab + 3 同步模式 + 多入口 + PC/Quest 适配 + UV License 免费商用 |
| **C16** ⭐NEW 2026-06-20 | **VizVid (VVMW)** | `memory/world/vvmw.md` | 5 大模块（Builtin/AVPro/Image/Playlist/Locale）+ 9 大功能（视频/直播/AVPro/低延迟/历史记录/本地化/UI 等）+ 9 大集成（AudioLink/LTCGI/VRCLightVolumes/Topaz/UdonAuth/YTTL/PlayerData/Stream Key/AVPro）+ 4 种显示模式 + 13 个 Releases + PC/Quest 跨平台 + 12+ 语言本地化 |

> **设计说明**:这 16 个项目**作为工具被创作者使用**(通过 VPM 安装),保留项目名 + 完整功能描述 + VPM 链接
> **元数据处理**:已删除 Stars/最后查看日期/作者名,保留项目功能描述

> **C15 双重身份特例**：C15 Lura's Switch 同时也是 A6 案例研究型——既可推荐使用又沉淀了 6 个通用模式。
> **C16 双重身份特例**：C16 VizVid (VVMW) 同时也是 A2 案例研究型——既可推荐使用又沉淀了 8 个时间同步算法模式。

---

### vrchat-community/ClientSim

- **仓库**: https://github.com/vrchat-community/ClientSim
- **类型**: VRChat 官方编辑器模拟工具
- **最后查看**: 2026-06-10

#### 项目概述
VRChat 官方维护的 Unity 编辑器模拟工具，让开发者可以在不发布到 VRChat 的情况下测试 SDK3 世界。

#### 核心功能
- **对象状态检查**: 实时查看对象属性和状态
- **行为验证**: 测试 Udon 脚本和世界逻辑
- **事件模拟**: 模拟玩家交互和触发器
- **性能测试**: 发布前识别潜在问题

#### 发展历史
1. **CyanEmu 时代**: 由 CyanLaser 创建的社区项目，提供基础模拟框架
2. **ClientSim 诞生**: CyanLaser 同时开发 CyanEmu 和 ClientSim，确保连续性
3. **VRChat 接管**: 2025 年官方接管并集成到 VRChat SDK

#### 2025 年仓库重构
| 项目 | 重构前 | 重构后 |
|------|--------|--------|
| 结构 | 独立 Unity 项目 | 源码仓库 (Source/) |
| 文档 | 本地 Documentation/ | 迁移至 Creator Docs |
| 测试 | Tests/ 文件夹 | 已移除 |
| 历史 | - | legacy 分支保留 |

#### 双向同步架构
- 公仓 `vrchat-community/ClientSim` 与 VRChat 私有仓库同步
- 源码: 双向同步
- 文档: 单向至 creator-docs
- Legacy 分支: 仅公仓

#### 关键学习点
1. **ClientSim 限制**: 作为本地模拟工具，无法完全替代真实网络测试
2. **与 SDK 集成**: ClientSim 是 VRChat SDK 的一部分，不是独立包
3. **测试策略**: ClientSim + Build & Test + 真实实例 的三层测试体系

#### 详细文档
见 `memory/sources/clientsim.md`

---

### niaka3dayo/agent-skills-vrc-udon

- **仓库**: https://github.com/niaka3dayo/agent-skills-vrc-udon
- **版本**: v2.3.0
- **Stars**: 173
- **License**: MIT
- **类型**: AI Agent Skills / Knowledge Base
- **最后查看**: 2026-06-04

#### 项目概述
Skills, rules, and validation hooks 项目，用于教 AI coding agents 生成正确的 UdonSharp 代码。不是 VRChat SDK 发行版，不是 Unity 项目。

#### 知识结构
- 2 个 Skill: `unity-vrc-udon-sharp` (核心) + `unity-vrc-world-sdk-3` (世界设置)
- 3 个 Rules: constraints, networking, sync-selection
- 23 个 Reference 文件: networking, persistence, dynamics, patterns, web-loading, testing 等
- 17 个 Code Templates: BasicInteraction 到 CloggedRetrySync
- 2 个 Validation Hooks: Bash + PowerShell PostToolUse 脚本
- SDK 覆盖: 3.7.1 - 3.10.3

#### 关键学习点
1. **SMART原则**: UdonSharp 的默认行为是静默失败，每个规则都源于此
2. **18 条 NEVER 清单**: 编译错误和静默运行时失败的具体场景
3. **Storage Layer Decision Tree**: 5 层存储选择的决策框架
4. **6 种 Networking Anti-Patterns**: Ownership Race Condition, String Truncation, Sync Buffer Overflow, Mixed Sync Modes, Sync Without Ownership, Excessive RequestSerialization
5. **5 种 Advanced Sync Patterns**: Packed Sync Data, Rate-Limited Serialization, Dual-Copy Variables, Delayed Batching, IsClogged Retry
6. **Persistence API**: PlayerData/PlayerObject 完整 API 参考和 Data Aging 模式
7. **Testing Guide**: ClientSim 限制、Build and Test multi-client、Late Joiner 测试流程
8. **UdonSharpProgramAsset**: 每个 .cs 需要 .asset，auto-generator 模式
9. **UI Anti-Pattern**: uGUI button owner check 使非 owner 按钮无响应
10. **SetOwner 本地立即生效**: SDK 3.7.1+ 的关键行为

#### 知识提取记录
- `rules/networking-rules.md`: +8 条新规则 (R10-R17)
- `rules/udonsharp-language-limits.md`: +9 条新规则 (R05-R13)
- `patterns/advanced-sync-patterns.md`: 新建，5 种高级同步模式
- `api/persistence.md`: 新建，PlayerData/PlayerObject 完整 API
- `api/dynamics.md`: 新建，PhysBones/Contacts/Constraints + SDK 版本时间线
- `reviews/common-failures.md`: +8 条新失败模式 (FAIL-11 到 FAIL-18)
- 已集成到 index.md v1.1

---

---

### vrchat-community/template-package

- **仓库**: https://github.com/vrchat-community/template-package
- **类型**: VPM Package 开发模板 / CI/CD 自动化
- **Stars**: 94 | Fork: 24
- **最后查看**: 2026-06-10

#### 项目概述
VRChat 官方提供的 VPM Package 开发模板，包含完整的 GitHub Actions 自动化工作流，用于创建、打包和分发 VPM 兼容的 Package。

#### 核心功能
1. **自动构建**: Push 代码后自动生成 .zip 和 .unitypackage
2. **自动发布**: GitHub Release + Git Tag 同步
3. **自动部署**: VPM Repo Listing 部署到 GitHub Pages
4. **Landing Page**: 自动生成 Package 展示页面

#### GitHub Actions 工作流

**release.yml**:
```
触发: 手动 (workflow_dispatch)
1. Validate PACKAGE_NAME 变量
2. 读取 package.json version
3. 创建 .zip 压缩包
4. 创建 .unitypackage (使用 create-unitypackage action)
5. 生成 Git Tag
6. 发布 GitHub Release
```

**build-listing.yml**:
```
触发: 手动 / Build Release 完成 / Release 事件
1. 检出 package-list-action (Nuke 项目)
2. 构建 VPM Repo Listing JSON
3. 部署到 GitHub Pages
```

#### 关键学习点
1. **GitHub Actions 集成**: 使用 `vars.PACKAGE_NAME` 仓库变量配置 Package 名称
2. **Nuke 构建系统**: package-list-action 使用 Nuke 构建 Repo Listing
3. **Scriban 模板**: Landing Page 使用 Scriban 填充动态内容
4. **元数据跟踪**: 使用 metaList 追踪 .meta 文件确保一致性

#### 详细文档
见 `memory/sources/vpm-package-template.md`

---

## 记录模板

```md
### {项目名}
- **仓库**: URL
- **类型**: World Prefab / Game System / Tool
- **关键模式**: 该项目使用了哪些值得学习的 UdonSharp 模式
- **Networking 特征**: synced variable 数量、sync mode 选择
- **性能特征**: UdonBehaviour 数量、Update 使用情况
- **学习点**: 具体值得记录的技术决策
- **SDK 版本**: 
- **最后查看**: 
```

---

### vrcx-team/VRCX

- **仓库**: github.com/vrcx-team/VRCX
- **类型**: VRChat 伴侣应用 / API 客户端
- **Stars**: 1,772 | Fork: 358
- **许可证**: MIT
- **最后查看**: 2026-06-11

#### 项目概述
VRCX 是 VRChat 官方 API 最成功的第三方客户端实现，为玩家提供好友管理、状态监控、通知、Rich Presence 等功能。

#### 技术栈
| 层级 | 技术 |
|------|------|
| 前端 | Vue.js (36.2%) |
| 核心逻辑 | JavaScript (47.1%) |
| 原生集成 | C# (.NET) |
| 通信 | VRChat HTTP API |
| 框架 | Electron（推断） |

#### 核心功能
1. **社交管理**: 好友/世界/Avatar 列表、状态监控、历史记录
2. **可自定义仪表盘**: Feed/GameLog/Instance 组件
3. **全局搜索**: 用户/世界/Avatar/群组搜索
4. **活动热力图**: 在线时间可视化
5. **截图元数据**: 记录拍照地点
6. **通知管理**: 邀请/好友请求收发
7. **Discord Rich Presence**: 增强的在线状态
8. **VR Overlay**: VR 内事件通知
9. **媒体管理**: 无需 Unity 上传图片
10. **自动化**: 启动联动、崩溃重启
11. **数据导出/导入**: 好友列表等

#### 关键学习点
1. **API 客户端最佳实践**: VRCX 展示了如何负责任地使用 VRChat HTTP API
2. **Rich Presence 集成**: 跨平台状态同步的 UX 设计
3. **数据可视化**: 热力图、活动统计的用户体验设计
4. **崩溃恢复**: 自动重启和实例恢复机制

#### 详细文档
见 `memory/sources/vrcx.md`
