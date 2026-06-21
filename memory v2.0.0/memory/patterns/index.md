---
title: Patterns — 设计模式选择决策树
category: patterns

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "Patterns Index"
  - 模式索引
  - Patterns
  - 设计模式

related:
  - patterns/unorthodox-patterns.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Patterns — 设计模式选择决策树

> 状态: ✅ 31 个核心模式(7 原有 + 6 LuraSwitch2 + 10 UdonVoiceUtils + 5 ULocalization 沙箱适配 + 3 Sardinal 独有) + 选择决策树

---

## 概述

本目录存储**可复用实现模式**。每个模式针对特定 UdonSharp 场景，包含：
- Problem / Context
- Udon Constraints 影响
- Networking Model（12 维度）
- Implementation Sketch
- When To Use / Not Use
- 交叉引用

---

## 模式选择决策树

### 1. 你需要同步什么？

```
Q1: 同步的是状态还是动作？
├── 状态（持续可见）→ Q2
└── 动作（瞬时触发）→ Network Event（非模式）
   例: 音效、粒子、一次性动画 → memory/world/udon/networking/events.md

Q2: Late joiner 需要看到吗？
├── 否 → Network Event（不需模式）
└── 是 → Q3

Q3: 状态是连续变化还是离散？
├── 连续（位置、旋转、进度条）→ Continuous Sync
│   └── 物理对象 → VRCObjectSync（scene-components）
└── 离散（开关、状态机、分数）→ Q4
```

### 2. 离散状态同步模式选择

```
Q4: 多个 bool/小值需要同步？
├── 是（3+）→ bit-packed-flags.md
└── 否（1-2）→ manual-sync-state.md

Q5: 需要 late joiner 正确恢复？
├── 是 → late-joiner-state-restore.md（必加）
└── 否（罕见）→ 仅 manual-sync-state.md
```

### 3. 多人交互所有权

```
Q6: 多人可能同时交互同一对象？
├── 是 → owner-authoritative-interaction.md
│   └── 需要复杂状态合并 → advanced-sync-patterns.md
└── 否（单人触发）→ manual-sync-state.md
```

### 4. 复杂状态机

```
Q7: 多个状态、明确转换条件？
├── 是 → event-driven-state-machine.md
└── 否 → manual-sync-state.md
```

### 5. 非常规需求

```
Q8: 标准模式无法满足？
└── 是 → unorthodox-patterns.md（⚠️ 谨慎评估）
```

### 6. Udon 沙箱适配（绕过 VM 限制）

```
Q9: 需要绕过 Udon VM 限制？
├── 动态分派 100+ 方法 → hash-based-dispatch.md
├── 对象跨 Editor-Runtime 引用 → iid-object-identity.md
├── UnityEvent 需传参 → slot-parameter-passing.md
├── 多种类型统一处理(泛型替代) → code-generation-type-erasure.md
└── Editor 端预处理 + 运行时查表 → build-time-vs-runtime-separation.md
```

### 7. Udon 端消息总线 Pub/Sub（跨模块解耦通信）

```
Q10: 需要"跨模块解耦通信"吗?
├── 是 → Sardinal 模式
│   ├── 同主题多模块差异化响应 → channel-routing.md ⭐S
│   ├── 抽象基类需统一事件被所有子类继承 → inherited-subscriber.md ⭐S
│   └── 混合场景常驻+动态对象 → hybrid-subscription-modes.md ⭐S
└── 否(单模块内部) → 直接 SendCustomEvent
```

---

## 7 个核心模式

### 1️⃣ manual-sync-state.md
**适用**: 离散状态同步（门、灯、状态机）
**核心**: `[UdonSynced]` int + `RequestSerialization()` + `FieldChangeCallback`
**变体**: byte 代替 int、多个 synced 变量组合

### 2️⃣ owner-authoritative-interaction.md
**适用**: 多人可交互对象
**核心**: Owner 锁定写入 + 可选 ownership transfer
**变体**: `OnOwnershipRequest` 拒绝转移

### 3️⃣ late-joiner-state-restore.md
**适用**: 任何需要 late joiner 看到状态的世界（**几乎必需**）
**核心**: `[UdonSynced]` 变量 + `OnDeserialization()` 重建表现
**变体**: 配合 Persistence 实现跨实例

### 4️⃣ bit-packed-flags.md
**适用**: 3+ 关联 bool 状态
**核心**: int/uint 存储 32 个 flag
**变体**: byte 存 8 flag

### 5️⃣ event-driven-state-machine.md
**适用**: 多阶段逻辑（回合制游戏、关卡流程）
**核心**: int `_state` + `SendCustomEvent` 状态转换 + switch 调度
**变体**: FSM、Hierarchical FSM

### 6️⃣ advanced-sync-patterns.md
**适用**: 高级需求（packed data、rate-limited serialization、threshold change detection）
**核心**: 带宽优化技术
**变体**: Vector3 packed int、发送频率控制

### 7️⃣ unorthodox-patterns.md
**适用**: 标准模式无法满足时的"邪修"技法
**核心**: Toggle 数组、BlendTree 卸载、OnAudioFilterRead 并行
**风险**: 高（部分未验证、需谨慎评估）

---

## 6 个新增模式 (QuickBrown LuraSwitch2) ⭐NEW 2026-06-20

### 8️⃣ master-follower-syncer.md ⭐NEW
**适用**: 1 个 Master 集中控制 N 个同类型对象(音量推子组、关卡联动)
**核心**: 节流窗口(0.1s) + `EnsureGlobalOwnership` 抢占 + 双标志排除回声
**变体**: N=2 时简化,实时需求高时缩短窗口
**项目来源**: `SwitchSyncer.cs` (736 行)

### 9️⃣ exclusive-control-selector.md ⭐NEW
**适用**: "多选一"互斥场景(关卡选择、模式切换、楼层跳转)
**核心**: 集中 `[UdonSynced]` + 强制子 syncMode 改为 None + 1 帧延迟初始化
**变体**: `_allowAllOff` 支持取消选择
**项目来源**: `SwitchSelector.cs` (849 行)

### 🔟 soft-detent-interpolation.md ⭐NEW
**适用**: 滑块有"标准档位"(音量 0/25/50/75/100)
**核心**: SmoothStep 软磁力公式 + 完全吸附阈值 + 拖动/松手路径分离
**变体**: 4 段 OFF/LOW/MID/HIGH,5 段音量
**项目来源**: `SliderSwitch.cs` SoftDetent 部分 (2218 行)

### 1️⃣1️⃣ fade-then-snap.md ⭐NEW
**适用**: 玩家可见的"瞬时"位置更新(重置点、关卡切换、传送)
**核心**: 3 阶段(透明→移动→淡入) + FadeInStep 重入 token
**变体**: VR 用户用更长 fade(0.4-0.5s)
**项目来源**: `SwitchBoard.cs` (581 行)

### 1️⃣2️⃣ editor-preview-component.md ⭐NEW
**适用**: 复杂参数需要 Creator 实时反馈(Mirror 范围、Collider 体积)
**核心**: `[ExecuteAlways]` MonoBehaviour + TrackingState 变更检测 + `SceneView.RepaintAll`
**变体**: `_showOnlyWhenSelected` 控制显示时机
**项目来源**: `MirrorAreaPreview.cs`, `Collider_AreaPreview.cs`, `HeightOffsetterPreview.cs`

### 1️⃣3️⃣ material-propertyblock-safe-update.md ⭐NEW
**适用**: 多个 GameObject 共享同一 Material Asset,运行时改颜色不污染
**核心**: `MaterialPropertyBlock` + Get/Set 配对 + Editor `OnValidate` 预览
**变体**: 与 sharedMaterial / material 性能对比
**项目来源**: `SwitchBase.cs` HSV 部分 (1795 行)

---

## 10 个新增模式 (TLP UdonVoiceUtils) ⭐U 2026-06-20

> **来源标注**:`⭐U` = UdonVoiceUtils 模式,以区别于 LuraSwitch2 模式(无后缀)。所有 UVU 模式从 `memory/sources/udonvoiceutils.md` 提炼。

### 1️⃣4️⃣ dual-copy-sync.md ⭐U NEW
**适用**: 双源同步(本地热数据 + 网络冷数据)
**核心**: `[UdonSynced] _xxx`(网络)+ 本地 `xxx`(缓存)配对,Get/Set 桥接
**变体**: 13 字段对(PlayerAudioConfigurationModel)
**项目来源**: `SyncedPlayerAudioConfigurationModel.cs` (TLP UdonVoiceUtils)

### 1️⃣5️⃣ execution-order-chain.md ⭐U NEW
**适用**: UdonBehaviour 协作时序(Controller → Model → View)
**核心**: `const ExecutionOrder = X.ExecutionOrder + 1` 链式声明依赖
**变体**: Override 链,Microphone 链
**项目来源**: TLP UdonVoiceUtils 全局常量

### 1️⃣6️⃣ strategy-pattern-udon.md ⭐U NEW
**适用**: 运行时切换算法(遮挡检测、降噪、回声消除)
**核心**: 抽象基类 + 多个具体实现 + Get/Set 切换
**变体**: `PlayerOcclusionStrategy` 抽象(Null/Default/自定义)
**项目来源**: `PlayerOcclusionStrategy.cs` 系列 (TLP UdonVoiceUtils)

### 1️⃣7️⃣ object-pool-udon.md ⭐U NEW
**适用**: 大量对象复用(Override 列表、AudioSource、子弹)
**核心**: 预创建 + 索引回收 + 空闲队列
**变体**: `PlayerAudioOverrideList` 数组池(零分配 GetMaxPriority)
**项目来源**: `PlayerAudioOverrideList.cs` (TLP UdonVoiceUtils)

### 1️⃣8️⃣ priority-arbitration.md ⭐U NEW
**适用**: 多个 Override 冲突仲裁(房间静音 + 门关闭 + 区域)
**核心**: `GetMaxPriority` + Override 数组排序 + PrivacyChannel 分组
**变体**: `HasOverlappingChannels` 双向频道检查
**项目来源**: `PlayerAudioOverrideList.cs` (TLP UdonVoiceUtils)

### 1️⃣9️⃣ master-ownership-defense.md ⭐U NEW
**适用**: 关键配置需要 Master 权威(全局静音开关)
**核心**: 三层防御(`OnPlayerJoined` + `OnOwnershipTransfer` + 周期检查)
**变体**: `EnsureGlobalOwnership` 主动抢占
**项目来源**: `SyncedPlayerAudioConfigurationModel.cs` (TLP UdonVoiceUtils)

### 2️⃣0️⃣ gizmos-relationship.md ⭐U NEW
**适用**: Editor 调试复杂依赖关系(Override ↔ Player ↔ Channel)
**核心**: `[CustomEditor]` + `OnSceneGUI` + `Handles.DrawLine`
**变体**: Gizmos 颜色编码(Privacy 红色 / Priority 蓝色)
**项目来源**: `Editor/PlayerAudioControllerEditor.cs` (TLP UdonVoiceUtils)

### 2️⃣1️⃣ trigger-event-fallback.md ⭐U NEW
**适用**: 玩家离开 Collider 时事件丢失兜底
**核心**: `OnTriggerExit` + Update 距离检查 + `SendCustomEvent` 补发
**变体**: `VoiceOverrideTriggerZone` 3 层保险(Trigger/距离/重连)
**项目来源**: `VoiceOverrideTriggerZone.cs` (TLP UdonVoiceUtils)

### 2️⃣2️⃣ compile-time-debug-strip.md ⭐U NEW
**适用**: 性能关键代码的调试钩子剥离
**核心**: `#region TLP_DEBUG` + `TLP_DEBUG` 宏(asmdef versionDefines)
**变体**: `VoiceRangeVisualizer` 仅 DEBUG 编译,Release 零成本
**项目来源**: `Debug/VoiceRangeVisualizer.cs` (TLP UdonVoiceUtils)

### 2️⃣3️⃣ auto-scripting-symbol.md ⭐U NEW
**适用**: VPM 包自动配置 Scripting Symbol
**核心**: asmdef `versionDefines` 字段 + 链接 XML
**变体**: `TLP_UDONVOICEUTILS_DEBUG` 自动启用(用户装包即生效)
**项目来源**: TLP UdonVoiceUtils VPM 包配置

---

## 5 个新增模式 (HoshinoLabs ULocalization) ⭐L NEW 2026-06-20

> **来源标注**:`⭐L` = ULocalization 模式(全称 Localization)以区别于其他来源。所有 UL 模式从 `memory/sources/ulocalization.md` 提炼,聚焦于"如何用 Editor 端代码生成绕过 Udon VM 限制"。

### 2️⃣4️⃣ hash-based-dispatch.md ⭐L NEW
**适用**: UnityEvent listener 需要 Udon 端动态分派(100+ Component 类型 + 任意方法)
**核心**: MD5(`TypeName+MethodName+RetType`) 作为 hash ID + 预生成 500+ wrapper 方法 + `SendCustomEvent(hash)`
**变体**: 白名单约束(只允许 100+ Component × 5-10 方法)
**项目来源**: `LocalizationShim_Generated.cs` (535 行 / 500+ hash 方法)
**关键约束**: 编译期静态可枚举;非白名单方法在 Build 阶段被过滤

### 2️⃣5️⃣ iid-object-identity.md ⭐L NEW
**适用**: 场景中需要索引访问大量同类对象(50+ LocalizeEvent / 100+ Variable)
**核心**: Editor 端 `IID.GenerateId` 顺序分配 int + 运行时用 `int[]` 数组按索引访问
**变体**: 按类型分组缓存(`Dictionary<Type, List<object>>`),跨 Build 引用稳定
**项目来源**: `IID.cs` / `LocalizeEventCache.cs` / `VariableCache.cs`
**关键约束**: 运行时不能增删对象 → 数组长度 Build 期固定

### 2️⃣6️⃣ slot-parameter-passing.md ⭐L NEW
**适用**: `SendCustomEvent` 需要传 1-3 个参数(无返回值,无委托,无 Lambda)
**核心**: Shim 预定义 3 个 `object` 槽位(`_l_t` target / `_l_p` prefab / `_l_a` active) + 调用前填槽 + 生成方法从槽读取
**变体**: 1 槽(target only) / 2 槽(target + value) / 3 槽(target + prefab + active)
**项目来源**: `LocalizationShim.cs` `_l_t` / `_l_p` / `_l_a` 三字段
**关键约束**: 槽位数量 ≤ 3;类型 cast 在生成时已确定,运行时无 cast 风险

### 2️⃣7️⃣ code-generation-type-erasure.md ⭐L NEW
**适用**: 多种具体类型(16+ IVariable / 5+ LocalizeEvent)需要统一处理
**核心**: `Type.FullName` MD5 hash 作为 type ID + switch case 显式分派 + `object[2]` 元组模式(`[shim ref, int id]`)
**变体**: 16 IVariable + 5 LocalizeEvent + 6 LocalizedReference(UL 三组)
**项目来源**: `SmartLiteFormatter.cs` 16 case + `LocalizationShim.cs` 类型擦除扩展方法
**关键约束**: 类型集合有限(< 20)且编译期完全确定;运行时新增类型不可用

### 2️⃣8️⃣ build-time-vs-runtime-separation.md ⭐L NEW
**适用**: 配置/数据可在编译期完全确定 + 运行时仅需 O(1) 查表分派
**核心**: Editor 端反射 + LINQ + 缓存预处理 → 注入 27 个 `object[]` 字段到 Udon Shim → 运行时 O(1) 数组访问
**变体**: Editor 端 `[Inject]` (Sardinject) + `WithParameter("_0", ...)`;Runtime 端 `Shim._0[idx]`;Build 钩子清理被替代组件
**项目来源**: `LocalizationResolver.cs` (600+ 行) + `LocalizationCleanup.cs` + `CloneDetector.cs`
**关键约束**: 修改 Scene 后必须重新 Build;UnityEvent listener 必须在白名单内

---

## 模式速查表

| 模式 | 复杂度 | 性能 | 适用规模 | 风险 |
|------|--------|------|---------|------|
| **manual-sync-state** | 低 | ⭐⭐⭐⭐⭐ | 小→中 | 低 |
| **owner-authoritative** | 中 | ⭐⭐⭐⭐ | 小→中 | 低 |
| **late-joiner-restore** | 低 | ⭐⭐⭐⭐⭐ | 必需 | 低 |
| **bit-packed-flags** | 低 | ⭐⭐⭐⭐⭐ | 中→大 | 低 |
| **event-driven-fsm** | 中 | ⭐⭐⭐⭐ | 中→大 | 中 |
| **advanced-sync** | 中→高 | ⭐⭐⭐⭐⭐ | 中→大 | 中 |
| **unorthodox** | 高 | ⭐⭐ | 特定 | 🔴 高 |
| **master-follower-syncer** ⭐NEW 📜Legacy | 中 | ⭐⭐⭐⭐ | 中→大 | 低 |
| **exclusive-control-selector** ⭐NEW 📜Legacy | 中 | ⭐⭐⭐⭐⭐ | 中→大 | 低 |
| **soft-detent-interpolation** ⭐NEW 📜Legacy | 中 | ⭐⭐⭐⭐ | 中 | 低 |
| **fade-then-snap** ⭐NEW 📜Legacy | 低 | ⭐⭐⭐⭐ | 小→中 | 低 |
| **editor-preview-component** ⭐NEW 📜Legacy | 低 | ⭐⭐⭐⭐⭐ | 工具 | 低 |
| **material-propertyblock-safe-update** ⭐NEW 📜Legacy | 低 | ⭐⭐⭐⭐⭐ | 通用 | 低 |
| **dual-copy-sync** ⭐U NEW | 中 | ⭐⭐⭐⭐ | 中→大 | 低 |
| **execution-order-chain** ⭐U NEW | 低 | ⭐⭐⭐⭐⭐ | 中→大 | 低 |
| **strategy-pattern-udon** ⭐U NEW | 中 | ⭐⭐⭐⭐ | 中 | 中 |
| **object-pool-udon** ⭐U NEW | 中 | ⭐⭐⭐⭐⭐ | 大 | 中 |
| **priority-arbitration** ⭐U NEW | 高 | ⭐⭐⭐⭐ | 中→大 | 中 |
| **master-ownership-defense** ⭐U NEW | 中 | ⭐⭐⭐⭐ | 中 | 低 |
| **gizmos-relationship** ⭐U NEW | 低 | ⭐⭐⭐⭐⭐ | 工具 | 低 |
| **trigger-event-fallback** ⭐U NEW | 中 | ⭐⭐⭐⭐ | 小→中 | 低 |
| **compile-time-debug-strip** ⭐U NEW | 低 | ⭐⭐⭐⭐⭐ | 通用 | 低 |
| **auto-scripting-symbol** ⭐U NEW | 低 | ⭐⭐⭐⭐⭐ | VPM | 低 |
| **hash-based-dispatch** ⭐L NEW | 中 | ⭐⭐⭐⭐ | 中→大 | 中 |
| **iid-object-identity** ⭐L NEW | 低 | ⭐⭐⭐⭐⭐ | 中→大 | 低 |
| **slot-parameter-passing** ⭐L NEW | 低 | ⭐⭐⭐⭐⭐ | 通用 | 低 |
| **code-generation-type-erasure** ⭐L NEW | 中 | ⭐⭐⭐⭐ | 中 | 中 |
| **build-time-vs-runtime-separation** ⭐L NEW | 高 | ⭐⭐⭐⭐⭐ | 大 | 中 |
| **channel-routing** ⭐S NEW | 中 | ⭐⭐⭐⭐ | 中→大 | 中 |
| **inherited-subscriber** ⭐S NEW | 低 | ⭐⭐⭐⭐⭐ | 中→大 | 低 |
| **hybrid-subscription-modes** ⭐S NEW | 中 | ⭐⭐⭐⭐ | 中→大 | 中 |

---

## 模式组合建议

```
✅ 推荐组合:
   manual-sync-state + late-joiner-restore    （基础 + 必需）
   owner-authoritative + manual-sync-state    （多人交互）
   bit-packed-flags + late-joiner-restore     （多状态压缩）
   event-driven-fsm + owner-authoritative     （多人游戏）

⚠️ 谨慎组合:
   unorthodox + 其他（先单独验证）
   advanced-sync + bit-packed（先单独验证）
```

---

## 模式实现骨架

所有模式都包含 **Implementation Sketch** 代码示例 + **Networking Model** 12 维度表：

| 维度 | 说明 |
|------|------|
| State Owner | 状态的所有者 |
| Source of Truth | 真实数据源 |
| Sync Type | 同步模式 |
| Synced Variables | 同步变量 |
| Mutation Path | 写入路径 |
| Ownership Path | 所有权路径 |
| Serialization Path | 序列化路径 |
| Receive Path | 远端接收路径 |
| Late Joiner | 迟到玩家处理 |
| Conflict Strategy | 冲突策略 |
| Bandwidth Budget | 带宽预算 |
| Failure Mode | 失败模式 |

> 使用此表格可对比不同模式的取舍

---

## 与其他目录的关系

| 关系 | 目录 |
|------|------|
| **规则约束** | `memory/rules/networking-rules.md`, `memory/rules/udonsharp-language-limits.md` |
| **失败案例** | `memory/reviews/common-failures.md` |
| **API 速查** | `memory/api/networking.md` |
| **应用层详解** | `memory/world/udon/networking/` |
| **设计模式来源** | 3 个参考工程(多机位导演系统 / 视频播放器 / 音频同步系统) 已沉淀到 `memory/FACT.md`,具体项目信息见 `memory/sources/` |

---

## 案例研究(参考工程)

知识库中已沉淀 4 个参考工程的设计模式(已沉淀到 FACT.md,具体项目名见 sources/ 目录):

| 设计模式类别 | 主要模式 | 文档 |
|------|---------|------|
| **多机位导演系统(参考工程)** | 5 层同步 + NetworkCallable + 双缓冲 + 指数衰减 + Slerp + 所有权分层 + NoVariableSync UI | `memory/FACT.md` §多机位导演系统 |
| **视频播放器(参考工程)** | Manual Sync + Owner Authority + 时间同步算法 | `memory/FACT.md` §视频播放器 |
| **音频同步系统(参考工程)** | Shader-Centric + Master 时间锚点 + 位域压缩 + 漂移校正 | `memory/FACT.md` §音频同步系统 |
| **QuickBrown LuraSwitch2(参考工程)** ⭐NEW | Master-Follower Syncer + Exclusive Selector + SoftDetent + Fade-Snap + Editor Preview + MaterialPropertyBlock | `memory/sources/quickbrown-luraswitch2.md` + 6 个新 pattern 文档 |
| **TLP UdonVoiceUtils(参考工程)** ⭐NEW | 10 个核心模式: Dual-Copy Sync + ExecutionOrder Chain + Strategy + Object Pool + Priority Arbitration + Master Ownership Defense + Gizmos + Trigger Fallback + Compile DEBUG + Auto Symbol | `memory/sources/udonvoiceutils.md` + 10 个新 pattern 文档 |
| **HoshinoLabs ULocalization(参考工程)** ⭐NEW | 5 个 Udon 沙箱适配核心模式: Hash-Based Method Dispatch + IID Object Identity + Slot Parameter Passing + Code Generation Type Erasure + Build-Runtime Separation | `memory/sources/ulocalization.md` + 5 个新 pattern 文档 |
| **HoshinoLabs Sardinal(参考工程)** ⭐NEW | 5 大 ULocalization 模式精简版 + 3 个 Sardinal 独有模式: Channel Routing + Inherited Subscriber + Hybrid Static+Dynamic Subscription | `memory/sources/sardinal.md` + 3 个新 pattern 文档 |
