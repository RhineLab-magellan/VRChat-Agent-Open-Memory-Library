# KB Index — Multi-Domain 路由地图

> VRChatAgent v3.0 | 2026-06-20 | Sardinal 案例入库 ✅ 3 Sardinal 独有 Pattern + A9 参考工程 + ULocalization A8 已沉淀

## 启动协议

```
1. Domain Detection（确定领域）
2. 读本文件 → 确定相关域目录
3. 读 _always-load.md（30s 核心约束）
4. Goto 具体文件
```

## 按 Domain 路由

### World Domain ← 当前主力 ✅

| 需求 | 路径 |
|---|---|
| UdonSharp 代码 | `rules/udonsharp-language-limits.md` |
| **Udon 官方文档本地化** | `world/udon/` ← ⭐ 10 个核心单页 + 子目录(2026-06-15) |
| **Udon 总览** | `world/udon/index.md` ← ⭐ 概念 + 3 种创建方式 + VM 关系 |
| **Udon 事件执行顺序** | `world/udon/event-execution-order.md` ← ⭐ _onEnable→_start 无间隔 |
| **Udon VM 字节码** | `world/udon/vm-and-assembly.md` ← 9 Opcodes 官方规范 |
| **Udon 调试** | `world/udon/debugging-udon-projects.md` |
| **Animation/Avatar/Input Events** | `world/udon/animation-events.md` + `avatar-events.md` + `input-events.md` |
| **Image/String Loading** | `world/udon/image-loading.md` + `string-loading.md` + `external-urls.md` |
| **AI Navigation** | `world/udon/ai-navigation.md` ← NavMeshAgent + Owner 计算 |
| **Using Build & Test** | `world/udon/using-build-test.md` ← 本地测试 |
| **Udon 版主工具** | `world/udon/udon-moderation-tool-guidelines.md` |
| 网络同步 | `rules/networking-rules.md` → `patterns/manual-sync-state.md` |
| 性能优化 | `rules/performance-rules.md` → `rules/udon-vm-architecture.md` |
| 陷阱排查 | `rules/udonsharp-deep-pitfalls.md` → `reviews/common-failures.md` |
| API 参考 | `api/` 目录（grep 关键词） |
| 设计模式 | `patterns/` 目录 |
| 脚本审查 | `reviews/review-checklist.md` |
| 后处理 | `misc/postprocessing-principles.md` → `misc/postprocessing-usage.md` |
| **光照系统** | `world/vrc-light-volumes.md` ← ⭐ 体素光照 + Point Light Volumes |
| **光照烘焙** | `world/bakery/light-baking-guide.md` ← ⭐ Bakery 烘焙指南 |
| **遮挡剔除** | `world/occlusion-culling-guide.md` ← 性能优化 |
| **反射探针** | `world/reflection-probes.md` ← 光照系统 |
| **World Shader** | `world/shader/` ← ⭐ Graphlit 节点编辑器 |
| **VRCGraphics** | `world/vrc-graphics.md` ← ⭐ 着色器全局变量 |
| **VRCCameraSettings** | `world/vrc-camera-settings.md` ← ⭐ 屏幕/手持相机 + VR 双眼 ⭐NEW |
| **VRCQualitySettings** | `world/vrc-quality-settings.md` ← ⭐ 阴影距离覆盖 + 质量只读 ⭐NEW |
| **Data Containers** | `world/data-containers.md` ← ⭐ JSON 序列化 |
| **Creator Economy** | `world/creator-economy.md` ← ⭐ 产品集成 |
| **Udon Example Scene** | `world/examples/udon-example-scene/` ← ⭐SDK 内置标准示例(13+ Prefab)⭐NEW |
| **Obstacle Course** | `world/examples/obstacle-course/` ← ⭐World Jam 2 官方套件(Time Trial 模式 + 6 文档)⭐NEW 2026-06-15 |
| **Lura's Switch 通用开关套件** | `world/luraswitch2.md` ← ⭐ 9 种 Prefab + 3 同步模式 + PC/Quest 自动适配 + UV License 免费商用 ⭐NEW 2026-06-20 |
| **VizVid (VVMW) 视频播放器** | `world/vvmw.md` ← ⭐ 5 大模块 + 9 大集成 + 13 个 Releases + PC/Quest 跨平台 + 12+ 语言本地化 ⭐NEW 2026-06-20 (A2/C16 双重身份) |

### Platform Domain ← ✅ 新增

| 需求 | 路径 |
|---|---|
| Android/Quest 开发 | `platform/android-development.md` |
| 跨平台内容 | `platform/cross-platform-content.md` |
| 移动端 UI | `platform/mobile-ui-optimization.md` |

### VRChatSDK Domain ← ✅ 已本地化

| 需求 | 路径 |
|---|---|
| SDK 概览 | `vrchatsdk/01_首页.md` |
| 认证 API | `vrchatsdk/07_API_认证.md` |
| 用户/世界/Avatar API | `vrchatsdk/08~10_API_*.md` |
| 好友/通知/收藏 API | `vrchatsdk/11~13_API_*.md` |
| 实例/文件/群组 API | `vrchatsdk/14~18_API_*.md` |
| WebSocket 实时事件 | `vrchatsdk/03_Websocket_API.md` |
| 数据模型 | `vrchatsdk/16~17_模型_*.md` |

### Sources Domain ← ✅ 新增

| 需求 | 路径 |
|---|---|
| Example Central | `sources/example-central.md` |
| **VPM Package Template** | `sources/vpm-package-template.md` ← ⭐NEW |
| **HoshinoLabs ULocalization 源(A8)** | `sources/ulocalization.md` ← ⭐NEW 2026-06-20 |
| **HoshinoLabs Sardinal 源(A9)** | `sources/sardinal.md` ← ⭐NEW 2026-06-20 (通用消息总线) |

### Avatar Domain ← ✅ 已建设

| 需求 | 路径 |
|---|---|
| **Animator 系统** | `avatar/animator-system.md` ← ⭐ 参数驱动系统 |
| **VRC Constraints** | `avatar/vrc-constraints.md` ← ⭐ 6 种约束类型 |
| **Playable Layers** | `avatar/playable-layers.md` ← ⭐ 5 层详解 |
| 性能等级标准 | `avatar/performance-rank.md` |
| NDMF 工具生态 | `avatar/ndmf-tools.md` |
| 最佳化实操指南 | `avatar/optimization-guide.md` |
| **Modular Avatar** | `avatar/modular-avatar.md` ← ⭐ VRChat改模必备插件(§0 速查 40 条 + §9 高级) |
| **MA 组件教学卡** | `avatar/ma-component-cards.md` ← ⭐ 28 个组件完整教学卡(含 Global Collider) |
| **Shader 索引** | `avatar/shader/index.md` ← ⭐ 完整对比矩阵 + 选择指南 |
| **Shader (lilToon)** | `avatar/shader/liltoon/` ← ⭐ 16 个文档，30%+ VRChat 使用 |
| **Shader (SCSS)** | `avatar/shader/scss.md` ← ⭐ 双阴影系统 + UV 服装切换 |
| **Shader (ORL)** | `avatar/shader/orl/` ← ⭐ World 通用模块化着色器（4个文档）|
| **Shader (Filamented)** | `avatar/shader/filamented/` ← ⭐ Google Filament PBR 替代（4个文档）|
| **Shader (UnlitWF)** | `avatar/shader/unlitwf/` ← ⭐ Unlit 扩展专业效果（Fur/Water/Grass/Gem）|
| **Shader (其他)** | `avatar/shader/other-shaders.md` ← Graphlit 等 |
| 入口文件 | `avatar/index.md` |

### Hybrid Domain ← ✅ 已建设

| 需求 | 路径 |
|---|---|
| **OSC 系统** | `hybrid/osc-protocol.md` ← ⭐ 完整协议数据库 |
| **AudioLink 系统** | `hybrid/audio-link.md` ← ⭐ 音频可视化核心 |
| Avatar↔World 交互 | `hybrid/` 目录（待建设） |
| 设计模式借鉴 | `memory/FACT.md` → 核心设计模式 section |

---

## World Domain 文件清单

```
rules/
  udonsharp-language-limits.md    ← C# 限制 (13 rules)
  networking-rules.md             ← 网络同步 (22 rules)
  performance-rules.md            ← 性能优化 (12 rules)
  multi-vm-rules.md               ← 多 VM 协作 (9 rules)
  udon-vm-architecture.md         ← VM 逆向 (9 指令/EXTERN/Heap)
  udonsharp-deep-pitfalls.md      ← 深度陷阱 (19 rules)
  vrchat-api-exposure.md          ← API 暴露判断

patterns/
  owner-authoritative-interaction.md
  manual-sync-state.md
  late-joiner-state-restore.md
  bit-packed-flags.md
  event-driven-state-machine.md
  advanced-sync-patterns.md
  unorthodox-patterns.md
  master-follower-syncer.md        ⭐NEW 2026-06-20
  exclusive-control-selector.md    ⭐NEW 2026-06-20
  soft-detent-interpolation.md     ⭐NEW 2026-06-20
  fade-then-snap.md                ⭐NEW 2026-06-20
  editor-preview-component.md      ⭐NEW 2026-06-20
  material-propertyblock-safe-update.md ⭐NEW 2026-06-20

api/
  networking.md  player-api.md  persistence.md  dynamics.md
  animator.md    audio.md       pickups.md      ui.md
  vrchat-advanced-apis.md  official-doc-clarifications.md
  events-reference.md
  udon-type-exposure.md     ← Udon Type Exposure Tree 索引 ⭐NEW
  exposed-types.md         ← 已暴露类型详细清单 ⭐NEW
  not-exposed.md           ← 未暴露 API 黑名单 ⭐NEW
  api-checker.md           ← API 检查器/代码模式 ⭐NEW

world/
  vrc-graphics.md              ← VRCGraphics/VRCShader API
  vrc-camera-settings.md      ← VRCCameraSettings（屏幕/手持相机 + VR 双眼）⭐NEW
  vrc-quality-settings.md     ← VRCQualitySettings（阴影距离覆盖 + 质量只读）⭐NEW
  data-containers.md          ← Data Lists/Dicts/VRCJson
  creator-economy.md          ← 创作者经济 SDK
  performance-guide.md        ← World 性能优化
  vrc-light-volumes.md        ← VRCLightVolumes 工具
  occlusion-culling-guide.md  ← 遮挡剔除优化
  reflection-probes.md        ← 反射探针系统
  udonsharp-compilation.md    ← UdonSharp 编译管线
  udon/                       ← Udon 编程完整子目录(可视化 + C# 入口) ⭐NEW 2026-06-15
    graph/                    ← Udon Node Graph(可视化编程)⭐NEW 2026-06-15
      index.md                ← 主页:Interface/Flow/创建节点/编译/运行
      event-nodes.md           ← Event 节点(Interact/Player/Video/...)⭐NEW
      graph-elements.md       ← Graph 元素(Groups/Comments/Noodles)⭐NEW
      searching-for-nodes.md   ← 5 种节点搜索方式 ⭐NEW
      special-nodes.md         ← 特殊节点(Block/Branch/Loop/Variable/...)⭐NEW
      type-nodes.md            ← 类型引用节点(VRCPickup/PlayerApi/...)⭐NEW
    udonsharp/                ← UdonSharp C# 入口子目录
    players/                  ← Players API 子目录
    ui-events.md              ← UI Events(Input Events 单独页)
    using-build-test.md       ← Build & Test 本地测试
    vm-and-assembly.md        ← Udon VM 与 Udon Assembly
    world-debug-views.md      ← World Debug Views
    udon-moderation-tool-guidelines.md
    index.md                  ← Udon 总览(3 种创建方式 + VM 关系)⭐NEW 2026-06-15
    ai-navigation.md          ← AI Navigation(NavMeshAgent + Owner 计算)⭐NEW 2026-06-15
    animation-events.md       ← Animation Events 白名单(12 个方法)⭐NEW 2026-06-15
    avatar-events.md          ← Avatar Events(OnAvatarChanged/EyeHeight)⭐NEW 2026-06-15
    debugging-udon-projects.md← Debugging(Debug 模式 + 错误日志)⭐NEW 2026-06-15
    event-execution-order.md  ← ⭐事件执行顺序(_onEnable→_start 无间隔)⭐NEW 2026-06-15
    external-urls.md          ← External URLs(VRCUrl + 域白名单)⭐NEW 2026-06-15
    image-loading.md          ← Image Loading(VRCImageDownloader)⭐NEW 2026-06-15
    input-events.md           ← Input Events(Button/Axis + UdonInputEventArgs)⭐NEW 2026-06-15
    string-loading.md         ← String Loading(VRCStringDownloader)⭐NEW 2026-06-15
  items.md                    ← Items in Udon Worlds (Layer 3 + Udon 不可引用) ⭐NEW 2026-06-15
  layers.md                   ← Unity Layers (32 Layer 分配 + Physics 安全模式) ⭐NEW 2026-06-15
  sdk-prefabs.md              ← SDK Prefabs (8 个 Udon 示例 Prefab) ⭐NEW 2026-06-15
  supported-assets.md         ← Supported Scripted Assets (TMP/PPSv2/FinalIK/DynamicBone) ⭐NEW 2026-06-15
  whitelisted-world-components.md  ← 完整 Script 白名单 (10 个组件集合) ⭐NEW 2026-06-15
  scene-components/           ← ⭐Scene Components 子分类(World 核心组件 9 选)⭐NEW 2026-06-15
    index.md                  ← Scene Components 总览(9 个核心组件索引 + PhysBone/Contact 1024 限制)
    textmeshpro.md            ← TextMesh Pro 集成/字体/Fallback 字体/本地化
    vrc-avatarpedestal.md     ← Avatar Pedestal 展示与切换(Blueprint ID + Scale)
    vrc-cameradolly.md        ← Camera Dolly 相机轨道(Animation/Path/Point 3 层)
    vrc-mirrorreflection.md   ← Mirror Reflection 实时反射(Quest 性能警告)
    vrc-objectsync.md         ← ⭐Object Sync 物理对象同步(SetKinematic/SetGravity/Respawn)
    vrc-portalmarker.md       ← Portal Marker 传送门(World ID/None/Home/Hub)
    vrc-scenedescriptor.md    ← ⭐Scene Descriptor World 必含核心(Spawn/Respawn/Order)
    vrc-station.md            ← Station 玩家固定座位(OnStationEntered + Avatar Station)
    vrc-enablepersistence.md  ← Enable Persistence 持久化(PlayerObject + 100KB 限制)
  bakery/                     ← Bakery 光照烘焙
    index.md
    light-baking-guide.md      ← Bakery 烘焙指南
  shader/                     ← World Shader 知识库
    index.md
    graphlit.md               ← Graphlit 节点编辑器
  examples/                   ← SDK 内置示例 ⭐NEW
    udon.md                   ← Udon 基础 4 模式 (旋转/交互/传送/事件) ⭐NEW 2026-06-15
    ai-navigation.md          ← AI Navigation 寻路 + Manual Sync ⭐NEW 2026-06-15
    detect-controller-collide.md ← OnControllerColliderHit + HitPlayer ⭐NEW 2026-06-15
    image-loading.md          ← VRCImageDownloader + GitHub Pages ⭐NEW 2026-06-15
    midi-playback.md          ← VRCMidiPlayer + Note On/Off 12 音位 ⭐NEW 2026-06-15
    minimap.md                ← VRCGraphics.Blit + RenderTexture + Shader ⭐NEW 2026-06-15
    mute-others.md            ← SetVoiceDistanceFar(0) 模拟静音 ⭐NEW 2026-06-15
    player-join-zones.md      ← DataList + FieldChangeCallback + 3 Mode 状态机 ⭐NEW 2026-06-15
    screen-canvas.md          ← IsUserInVR + VRC_UIShape + TeleportTo ⭐NEW 2026-06-15
    obstacle-course/          ← ⭐Obstacle Course(World Jam 2 官方套件)NEW 2026-06-15
      index.md                ← Overview + Quick Start + Player/PowerUp 配置
      build-from-demo-parts.md
      build-from-custom-parts.md
      uoc-flythrough.md
      uoc-how-stuff-works.md
      uoc-window.md
    persistence/              ← Persistence Examples 子目录
    udon-example-scene/       ← Udon Example Scene(13+ Prefab)
      index.md                ← 主页 13+ Prefab 详解 + 5 种同步模式
      avatar-scaling-settings.md
      player-mod-setter.md
      simple-pen-system.md
      udon-video-sync-player.md
      world-audio-settings.md

reviews/
  review-checklist.md  common-failures.md  severity-model.md

misc/
  postprocessing-principles.md    ← 后处理原理（现实参照）
  postprocessing-usage.md        ← Unity 参数与最佳实践
  accessibility-guide.md         ← 无障碍设计指南

platform/                      ← ⭐NEW 跨平台开发
  android-development.md
  cross-platform-content.md
  mobile-ui-optimization.md

sources/
  example-central.md           ← Example Central 使用
  vpm-package-template.md      ← VPM Package 开发模板 ⭐NEW
  clientsim.md                  ← ClientSim 编辑器模拟工具
  open-source-projects.md      ← 开源项目参考
  quickbrown-luraswitch2.md    ← QuickBrown LuraSwitch2 案例研究 ⭐NEW 2026-06-20
  udonvoiceutils.md            ← TLP UdonVoiceUtils 案例研究 ⭐NEW 2026-06-20
  ulocalization.md             ← HoshinoLabs ULocalization 案例研究 ⭐NEW 2026-06-20
  sardinal.md                  ← HoshinoLabs Sardinal 案例研究 ⭐NEW 2026-06-20 (通用消息总线)

vrchatsdk/                     ← VRChatSDK HTTP API (18 个文档) ✅
  index.md                    ← VRChatSDK 总览 + 端点分类 ⭐NEW 2026-06-15
```

### 域索引文件总览(2026-06-15 二次审计补全)

| 域 | index.md | 文件数 | 状态 |
|---|---------|-------|------|
| `world/udon/` | ✅ | ~60 | 已就位 |
| `world/scene-components/` | ✅ | 10 | 已就位 |
| `world/bakery/` | ✅ | 2 | 已就位 |
| `world/clientsim/` | ✅ | 8 | 已就位 |
| `world/shader/` | ✅ | 2 | 已就位 |
| `world/examples/` | ❌ (使用 README.md) | 31 | 用 README 替代 |
| `avatar/` | ✅ | 9 | 已就位 |
| `avatar/shader/` | ✅ | 4 + 子目录 | 已就位 |
| `avatar/shader/liltoon/` | ✅ | **17**(新增 outline.md)| ✅ 已修复 outline 缺失 |
| `avatar/shader/orl/` | ✅ | 5 | 已就位 |
| `avatar/shader/filamented/` | ✅ | 4 | 已就位 |
| `avatar/shader/unlitwf/` | ✅ | 1 | 已就位 |
| `hybrid/` | ✅ | 3 | 已就位 |
| **`vrchatsdk/`** | ✅ ⭐NEW | 19(+1) | **二次审计补全** |
| **`platform/`** | ✅ ⭐NEW | 5(+1) | **二次审计补全** |
| **`misc/`** | ✅ ⭐NEW | 4(+1) | **二次审计补全** |
| **`references/`** | ✅ ⭐NEW | 2(+1) | **二次审计补全** |
| `sources/` | ✅ | 11 (+1) | 已就位(2026-06-20 +1 Sardinal) |
| `rules/` | ✅ | 8 | 已就位 |
| `patterns/` | ✅ | 31 (+17) | 已就位(2026-06-20 +3 Sardinal 独有) |
| `api/` | ✅ | 17 | 已就位 |
| `reviews/` | ✅ | 4 (32 FAILs) | 已就位(2026-06-20 +4 FAILs) |
| `journal/` | ✅ (README.md) | 3 | 用 README 替代 |

## VRChatSDK Domain 文件清单

```
vrchatsdk/
  01_首页.md                   ← 层级概览
  02_TypeScript_SDK.md        ← SDK 多语言支持
  03_Websocket_API.md         ← WebSocket 实时事件
  04_Instances.md             ← 实例管理
  05_Tags.md                  ← 标签系统
  06_FAQ.md                   ← 常见问题
  07_API_认证.md              ← 认证 API
  08_API_用户.md              ← 用户 API
  09_API_世界.md              ← 世界 API
  10_API_Avatar.md            ← Avatar API
  11_API_好友.md              ← 好友 API
  12_API_通知.md              ← 通知 API
  13_API_收藏.md              ← 收藏 API
  14_API_实例.md              ← 实例 API
  15_API_文件.md              ← 文件 API
  16_模型_User.md             ← User 数据模型
  17_模型_CurrentUser.md      ← CurrentUser 数据模型
  18_API_群组.md              ← 群组 API
```

## Avatar Domain 文件清单

```
avatar/
  index.md                     ← 域名索引
  animator-system.md           ← Write Defaults/Avatar Mask/Playable Layers
  vrc-constraints.md           ← VRC Constraints 6 种类型
  playable-layers.md           ← 5 层详解
  performance-rank.md          ← PC/Quest 性能等级
  performance-benchmarks.md    ← 性能基准测试
  ndmf-tools.md                ← NDMF 工具生态
  optimization-guide.md        ← 最佳化实操指南
  avatar-modding-guide.md      ← Bike Pose 修复等改模知识
  modular-avatar.md            ← Modular Avatar 插件
  avatar-parameter-staged-sync.md
  shader/
    index.md                   ← Shader 索引（完整对比矩阵 + 选择指南）⭐2026-06-11
    liltoon/                   ← lilToon 详细文档（16个文件）
    scss.md                    ← SCSS 详细分析报告（双阴影/UV切换）⭐2026-06-11
    orl/                       ← ORL Shaders World 通用（4个文档）⭐NEW
    filamented/                ← Filamented PBR 替代（4个文档）⭐NEW
    unlitwf/                   ← UnlitWF Unlit 扩展（1个文件 + 详细分析）⭐NEW
    other-shaders.md           ← 其他 Shader（Graphlit 等）
```

## Hybrid Domain 文件清单

```
hybrid/
  index.md                ← 域名索引
  osc-protocol.md         ← OSC 协议数据库 ✅
  audio-link.md            ← AudioLink 系统架构 ✅
```

---

## 搜索关键词

| 领域 | Grep pattern | 路径 |
|---|---|---|
| World/网络 | `networking\|sync\|SetOwner\|RequestSerialization` | `memory/rules/` |
| World/性能 | `EXTERN\|boxing\|Update\|GC\|loop` | `memory/rules/` |
| World/陷阱 | `FAIL-\|静默\|陷阱` | `memory/reviews/` |
| World/后处理 | `bloom\|vignette\|grain\|motion blur\|chromatic` | `memory/misc/` |
| API | API 方法名 | `memory/api/` |
| Avatar | `animator\|physbone\|contact\|constraint\|cloth\|benchmark` | `memory/avatar/` |
| **Shader/Avatar专用** | `liltoon\|scss\|cel.*shader\|toon.*shadow` | `memory/avatar/shader/` |
| **Shader/World专用** | `orl.*shader\|filamented\|pbr.*world\|configurable` | `memory/avatar/shader/` |
| **Shader/通用** | `unlitwf\|fur\|water.*shader\|gem.*shader\|grass.*shader` | `memory/avatar/shader/` |
| Hybrid/OSC | `osc\|hybrid\|cross-domain\|AudioLink\|ALPass` | `memory/hybrid/` |
| **VRCGraphics** | `VRCGraphics\|VRCShader\|SetGlobal\|Blit` | `memory/world/` |
| **VRCCameraSettings** | `VRCCameraSettings\|GetEyePosition\|GetCurrentCamera\|OnVRCCameraSettingsChanged` | `memory/world/` |
| **VRCQualitySettings** | `VRCQualitySettings\|SetShadowDistance\|OnVRCQualitySettingsChanged` | `memory/world/` |
| **Data Containers** | `DataList\|DataDictionary\|DataToken\|VRCJson` | `memory/world/` |
| **Platform** | `android\|quest\|mobile\|cross-platform` | `memory/platform/` |
| **Creator Economy** | `Store\|UdonProduct\|OpenListing` | `memory/world/` |
| **光照系统** | `LightVolume\|PointLight\|SH\|体素` | `memory/world/` |
| **World Shader** | `Graphlit\|node editor\|PBR\|Filament` | `memory/world/shader/` |
| **Udon Example** | `ButtonSync\|SendEventOn\|PlayerTrigger\|UdonSyncPlayer\|VRCWorldSettings` | `memory/world/examples/udon-example-scene/` |

---

## Journal — 会话记忆（临时）

> ⚠️ 定期清理，防止污染知识库

| 用途 | 路径 | 保留时间 |
|------|------|----------|
| 会话工作记录 | `journal/sessions/` | 30 天 |
| 代码审查记录 | `journal/reviews/` | 60 天 |
| 问题追踪 | `journal/issues/` | 关闭后 7 天 |
| 临时草稿 | `journal/drafts/` | 7 天 |

**原则**：知识入库后，从 Journal 删除对应记录。