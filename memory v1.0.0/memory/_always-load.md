# VRChat 全领域核心约束速查

> Unity: 2022.3.22f1 LTS | SDK: 3.10.3 | 2026-06-20 更新:Sardinal 案例入库(3 Sardinal 独有 Pattern) + ULocalization 案例入库(5 Udon 沙箱适配 Pattern) + UVU 案例入库(10 Pattern) + VVMW 升级 A2/C16 双重身份

---

## 领域识别（回答前必做）

```
Avatar? → Animator/PhysBone/Contact/Constraint/Shader/Optimization
World?  → UdonSharp/Networking/Gameplay/Performance/Security
Hybrid? → OSC/Avatar↔World/External
不确定  → 必须询问用户
```

## 回答前自检

```
□ 领域识别完成? □ 知识检索完成? □ FACT/INFERENCE 区分?
□ 风险标记? □ 未知项标记? □ 知识充足?
→ 不足则输出 Missing Information，不强行回答
```

## 知识优先级

```
L1 官方规范 > L2 官方发布 > L3 社区标准 > L4 优秀案例 > L5 工程推理
L5 必须标注【推断】; 证据不足必须标注【未确认】
```

---

## World Domain — 立即检查（代码生成前 30s）

```
□ 是否使用了 List/Dictionary/LINQ/lambda?
□ 是否使用了 async/try-catch/coroutine?
□ 是否使用了 internal/NoVariableSync/partial?
□ Manual Sync → RequestSerialization()?
□ 同步了 String/DisplayName?
□ Update 中分配内存/调 EXTERN?
□ 热路径 GetComponent/Find?
□ 非 Owner 写入 UdonSynced?
□ Enum 比较 cast 到 int?
□ API 是否在 Udon 中暴露？ → 检查 memory/api/udon-type-exposure.md
```

## World Domain — 网络同步核心

```
1. Owner 写入 → Manual + RequestSerialization()
2. Late joiner → 必须 [UdonSynced]
3. Continuous → 丢包不重传，仅用于连续数据
4. Manual → 多变量时 OnDeserialization 可能分帧
5. [NetworkCallable] → SDK 3.8.1+，8 参数
6. SetOwner → 本地立即生效
7. 非 Owner 写入 → 静默回退
8. _ 前缀 public → 防网络事件调用
```

## World Domain — VM 性能事实

- 9 条指令，纯解释器，比 C# 慢 200x-1000x
- 每变量 = StrongBox<T>（装箱/拆箱）
- EXTERN = 最昂贵指令
- 10 秒硬限制 → Behaviour 永久停止
- Instantiate Udon prefab ≈ 2ms

## World Domain — 禁止清单

| 类别 | 禁止项 |
|---|---|
| 集合 | List<T>, Dictionary, LINQ |
| 异步 | async/await, try/catch, coroutine |
| 泛型 | lambda, delegate, AddListener |
| 关键字 | internal, partial, NoVariableSync |
| 热路径 | GetComponent, Find, Debug.Log, 字符串拼接, 分配内存, EXTERN |
| 同步 | String, DisplayName, Collision Ownership Transfer |

## World Domain — Enum 5 陷阱

1. ToString() → 输出数字
2. cast 不能与操作符写一起
3. 可选参数不能用 Enum 默认值
4. 非用户 Enum 比较 → cast 到 int
5. `var max = TWO; max >= TWO` → false（先转 int）

---

## Avatar Domain — Animator 核心约束

### Playable Layers 播放顺序

```
Base → Additive → Gesture → Action → FX（最后，最高优先级）
```

### 关键规则

```
1. 前四层（Base/Additive/Gesture/Action）只控制 Transform 和 GameObject 开关
2. Blendshape/材质替换/着色器动画 → 必须在 FX 层
3. 禁止同一控制器中混用 Write Defaults On/Off
4. WD Off 状态必须有填充动画（空属性 + 至少 2 帧）
5. FX 层用 WD Off 控制 Transform → 覆盖 Gesture 层所有 Transform
6. Direct Blend Tree → 必须 Write Defaults On
7. 单 State 的 Direct BT 例外，可单独使用任意 WD
```

### Expression Parameter 类型兼容

| Animator \ Expression | Bool | Int | Float |
|---|---|---|---|
| Bool → | 直接传递 | 0/1 | 0.0/1.0 |
| Int → | >0 = True | 直接传递 | 直接转换 |
| Float → | >0 = True | 四舍五入 | 直接传递 |

### Avatar Mask 行为

- 启用 Humanoid Muscle → 可修改该值
- 禁用 Humanoid Muscle → 不能修改
- 启用 Transform → 可修改位置/旋转/缩放 + 替换第一材质球
- 禁用 Transform → 不能修改
- 有 Avatar Mask → 不能控制除第一个外的材质球

---

## Hybrid Domain — ✅ 已建设

```
OSC 协议数据库 ✅ / AudioLink 系统架构 ✅ / Avatar↔World 交互（待建设）
External Integration / Tracking（待建设）
```

---

## 文件速查

| 需要 | 去 |
|---|---|
| World 代码/网络/性能 | `memory/rules/` |
| World API | `memory/api/` (grep) |
| **Udon 官方文档本地化** | `memory/world/udon/` ⭐ 10+ 单页(2026-06-15) |
| **Udon 事件执行顺序** | `memory/world/udon/event-execution-order.md` ⭐_onEnable→_start 无间隔 |
| **Udon VM 字节码** | `memory/world/udon/vm-and-assembly.md` 9 Opcodes 官方规范 |
| World 设计模式 | `memory/patterns/` ⭐ 31 个(7 原有 + 6 LuraSwitch2 + 10 UVU + 5 ULocalization 沙箱适配 + 3 Sardinal 独有) |
| **Master-Follower Syncer** | `memory/patterns/master-follower-syncer.md` ⭐NEW |
| **Exclusive Control Selector** | `memory/patterns/exclusive-control-selector.md` ⭐NEW |
| **Soft Detent Interpolation** | `memory/patterns/soft-detent-interpolation.md` ⭐NEW |
| **Fade-Then-Snap** | `memory/patterns/fade-then-snap.md` ⭐NEW |
| **Editor Preview Component** | `memory/patterns/editor-preview-component.md` ⭐NEW |
| **MaterialPropertyBlock Safe Update** | `memory/patterns/material-propertyblock-safe-update.md` ⭐NEW |
| **Hash-Based Method Dispatch** | `memory/patterns/hash-based-dispatch.md` ⭐NEW 2026-06-20 |
| **IID Object Identity** | `memory/patterns/iid-object-identity.md` ⭐NEW 2026-06-20 |
| **Slot-Based Parameter Passing** | `memory/patterns/slot-parameter-passing.md` ⭐NEW 2026-06-20 |
| **Code Generation with Type Erasure** | `memory/patterns/code-generation-type-erasure.md` ⭐NEW 2026-06-20 |
| **Build-Time vs Runtime Separation** | `memory/patterns/build-time-vs-runtime-separation.md` ⭐NEW 2026-06-20 |
| **QuickBrown LuraSwitch2 源（案例研究 A6）** | `memory/sources/quickbrown-luraswitch2.md` ⭐NEW |
| **Lura's Switch 工具使用指南（C15）** | `memory/world/luraswitch2.md` ⭐NEW 2026-06-20（推荐玩家使用） |
| **VizVid (VVMW) 源（案例研究 A2）** | `memory/sources/vvmw.md` ⭐NEW 2026-06-20（视频播放器） |
| **VizVid (VVMW) 工具使用指南（C16）** | `memory/world/vvmw.md` ⭐NEW 2026-06-20（推荐创作者使用） |
| **HoshinoLabs ULocalization 源** | `memory/sources/ulocalization.md` ⭐NEW 2026-06-20 |
| **HoshinoLabs Sardinal 源** | `memory/sources/sardinal.md` ⭐NEW 2026-06-20 (通用消息总线) |
| **Channel-Based Pub/Sub Routing** | `memory/patterns/channel-routing.md` ⭐NEW 2026-06-20 (Sardinal 独有) |
| **Inherited Subscriber** | `memory/patterns/inherited-subscriber.md` ⭐NEW 2026-06-20 (Sardinal 独有) |
| **Hybrid Static+Dynamic Subscription** | `memory/patterns/hybrid-subscription-modes.md` ⭐NEW 2026-06-20 (Sardinal 独有) |
| World 审查 | `memory/reviews/` |
| **光照系统** | `memory/world/vrc-light-volumes.md` |
| **光照烘焙** | `memory/world/bakery/light-baking-guide.md` |
| **遮挡剔除** | `memory/world/occlusion-culling-guide.md` |
| **World Shader** | `memory/world/shader/` ← Graphlit 节点编辑器 |
| **VRCGraphics / Shader Globals** | `memory/world/vrc-graphics.md` |
| **Udon Node Graph(可视化)** | `memory/world/udon/graph/` ← Interface/Flow/Event/搜索/类型 ⭐NEW 2026-06-15 |
| **VRCCameraSettings** | `memory/world/vrc-camera-settings.md` ⭐NEW |
| **VRCQualitySettings** | `memory/world/vrc-quality-settings.md` ⭐NEW |
| **ClientSim(World 测试)** | `memory/world/clientsim/index.md` ⭐NEW 2026-06-15 |
| **Obstacle Course(World Jam 2)** | `memory/world/examples/obstacle-course/` ⭐NEW 2026-06-15 |
| **Items in Udon Worlds** | `memory/world/items.md` ← ⭐ Layer 3 + Udon 不可引用 Items ⭐NEW 2026-06-15 |
| **Unity Layers in VRChat** | `memory/world/layers.md` ← ⭐ 32 Layer 分配 + Physics 安全模式 ⭐NEW 2026-06-15 |
| **SDK Prefabs** | `memory/world/sdk-prefabs.md` ← ⭐ 8 个 Udon 示例 Prefab ⭐NEW 2026-06-15 |
| **Supported Scripted Assets** | `memory/world/supported-assets.md` ← ⭐ TMP/PPSv2/FinalIK/DynamicBone 白名单 ⭐NEW 2026-06-15 |
| **Allowlisted World Components** | `memory/world/whitelisted-world-components.md` ← ⭐ 完整 Script 白名单 (10 集合) ⭐NEW 2026-06-15 |
| **Video Players** | `memory/world/udon/video-players/` ← ⭐ VRCUnityVideoPlayer / AVPro + URL 白名单 ⭐NEW 2026-06-15 |
| Avatar Animator | `memory/avatar/animator-system.md` |
| **Avatar 自动纹理压缩 (LAC)** | `memory/avatar/lac-avatar-compressor.md` ⭐NEW 2026-06-17 |
| **MA 响应式层合并 (MA2BT)** | `memory/avatar/ma2bt.md` ⭐NEW 2026-06-17 |
| **Avatar 优化器 (AAO)** | `memory/avatar/avatar-optimizer.md` ⭐NEW 2026-06-17 |
| **TexTransTool (TTT)** | `memory/avatar/tex-trans-tool.md` ⭐NEW 2026-06-17 |
| **VRCFury 客观参考** | `memory/avatar/vrcfury-reference.md` ⭐NEW 2026-06-17 |
| **Meshia 减面** | `memory/avatar/meshia-mesh-simplification.md` ⭐NEW 2026-06-17 |
| **Thry 性能检测指标** | `memory/avatar/thry-avatar-evaluator-metrics.md` ⭐NEW 2026-06-17 |
| **NDMF 工具生态** | `memory/avatar/ndmf-tools.md` ⭐执行顺序 |
| Avatar 其他 | `memory/avatar/` |
| Hybrid/OSC | `memory/hybrid/` |
| **VRChatSDK API** | `memory/vrchatsdk/index.md` ⭐NEW 2026-06-15 域索引 |
| 跨平台开发 | `memory/platform/index.md` ⭐NEW 2026-06-15 域索引 |
| 杂项(后处理/无障碍) | `memory/misc/index.md` ⭐NEW 2026-06-15 域索引 |
| 知识版本 | `memory/FACT.md` |
| 文档对比记录 | `memory/references/index.md` ⭐NEW 2026-06-15 域索引 |
| 会话记忆 | `memory/journal/` (临时，定期清理) |
