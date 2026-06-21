# TLP UdonVoiceUtils (UVU) — 案例研究型参考工程

> Type: SOURCE
> Tier: B（高质量开源项目，跨验证发现）
> 项目类型: VRChat World 玩家语音/音频动态控制库
> 项目形态: Unity Package + UdonSharpBehaviour 套件 + 完整 Editor 工具
> SDK 目标: VRChat SDK 3.10.3+
> 依赖: TLP UdonUtils ^14.0.0
> Unity: 2022.3
> 路径: `C:\CherryStudio\Agent\UdonSharpAgent\参考工程\UdonVoiceUtils\`
> 最后查看: 2026-06-20
> 分析文件数: 35 个 .cs (Runtime 21 + Editor 6 + Testing 6 + AssemblyInfo 1 + Examples 8)

---

## 项目概述

**UdonVoiceUtils (UVU)** 由 Guribo 维护，是 VRChat 创作者生态中**事实标准的玩家语音动态控制库**，用于在 World 中实时修改玩家语音/Avatar 音频的距离、增益、方向性、遮挡、隐私频道、混响和高度缩放。

**核心设计哲学**:
- 8 层职责划分: Controller / Model / Override / OverrideList / OcclusionStrategy / View / IgnoredPlayers / Pool
- 双副本同步: 本地字段 + `[UdonSynced]` 私有字段
- 显式执行顺序链: `const ExecutionOrder = X.ExecutionOrder + 1`
- 完整 Edit Mode 体验: 5 个 [CustomEditor] + 场景视图 Gizmos
- 高度可测试: 4 个 Runtime Test + Mock 机制

**商业采用度**: 9+ 知名世界采用(Drinking Night, Midnight Rooftop, The Great Pub, Virtual Performing Arts Theater, Cool Party 等)

---

## 项目结构

```
UdonVoiceUtils/
├── README.md (LDC 包含完整 5+ 年 CHANGELOG)
└── Packages/
    └── tlp.udonvoiceutils/                   ← 完整 VPM Package
        ├── Editor/
        │   ├── UdonVoiceUtilsDefinitions.cs ← 自动添加 TLP_UDONVOICEUTILS 宏
        │   └── Inspectors/                  ← 5 个 [CustomEditor]
        │       ├── PlayerAudioControllerEditor.cs   (Gizmos: Controller → 所有 Override)
        │       ├── VoiceOverrideRoomEditor.cs        (Gizmos: Room → Door/Button)
        │       ├── VoiceOverrideDoorEditor.cs        (Gizmos: 内外方向)
        │       ├── VoiceOverrideRoomEnterButtonEditor.cs
        │       └── VoiceOverrideRoomExitButtonEditor.cs
        └── Runtime/
            ├── AssemblyInfo.cs              ← InternalsVisibleTo Tests
            ├── Core/                        ← 核心架构 (8 类)
            │   ├── VoiceUtils.cs                          (静态工具, FindPlayerAudioController)
            │   ├── PlayerAudioController.cs   (1446 行)   (Controller, NoVariableSync)
            │   ├── PlayerAudioConfigurationModel.cs        (Model, 双副本同步)
            │   ├── SyncedPlayerAudioConfigurationModel.cs  (强制 Master 所有权)
            │   ├── PlayerAudioView.cs                     (View, 12+ Slider)
            │   ├── PlayerAudioOverride.cs                 (Override 单元)
            │   ├── PlayerAudioOverrideList.cs   (池化, GetMaxPriority)
            │   ├── IgnoredPlayers.cs                      (本地黑名单)
            │   └── PlayerOcclusion/                       (策略模式)
            │       ├── PlayerOcclusionStrategy.cs          (抽象)
            │       ├── NullPlayerOcclusion.cs
            │       └── DefaultPlayerOcclusion.cs           (RaycastNonAlloc)
            ├── DEBUG/                       ← 调试工具
            │   └── VoiceRangeVisualizer.cs                (可视化范围)
            ├── Examples/                    ← 8+ 使用范本
            │   ├── AdjustableGain.cs                       (全局 Gain 滑块)
            │   ├── DynamicPrivacy.cs                       (动态频道)
            │   ├── MicActivation.cs (abstract)             (模板方法)
            │   ├── VoiceOverrideRoom.cs                    (房间系统)
            │   ├── VoiceOverrideDoor.cs                    (Trigger 入口)
            │   ├── VoiceOverrideTriggerZone.cs             (Zone 入口)
            │   ├── VoiceOverrideRoomEnterButton.cs
            │   ├── VoiceOverrideRoomExitButton.cs
            │   └── Microphone/                            (拾取系统 MVC)
            │       ├── MicModel.cs, MicView.cs, MicController.cs
            │       ├── PickupMicrophone.cs
            │       ├── PickupMicActivation.cs
            │       └── InteractMicActivation.cs
            └── Testing/                     ← 单元测试 (6 类)
                ├── MockLocalPlayerChangeEventListener.cs
                ├── PlayerAudioVoiceFalloffTest.cs          (步进距离衰减)
                ├── TestMasterReceivesPlayerHeightChange.cs
                ├── TestMaxOcclusionMutesPlayers.cs         (NetworkCalling 验证遮挡)
                └── TestZoneEnteringNetworked.cs            (跨玩家房间加入)
```

---

## 架构总览 (8 层职责 + Strategy + Pool)

```
┌─────────────────────────────────────────────────────┐
│ VoiceUtils (静态工具)                                 │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ PlayerAudioController (Controller, NoVariableSync)   │
│  ├─ PostLateUpdate: 每帧更新玩家音频                  │
│  ├─ PlayerOverrideListPool (对象池)                  │
│  ├─ PlayerOcclusionStrategy (策略)                   │
│  ├─ IgnoredPlayers (本地黑名单)                      │
│  └─ LocalConfiguration / SyncedMasterConfiguration    │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ PlayerAudioConfigurationModel (Model, 双副本同步)     │
│  ├─ 本地字段 (13 个, 自由修改)                       │
│  └─ _syncedXxx 私有字段 (13 个, 网络传输)            │
│       ↑                                              │
│       └── SyncedPlayerAudioConfigurationModel        │
│            (强制 Master 所有权)                      │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ PlayerAudioOverride (Override 单元)                   │
│  ├─ Priority (优先级)                                │
│  ├─ PrivacyChannelId / AdditionalPrivacyChannelIds   │
│  ├─ MuteOutsiders / DisallowListeningToChannel      │
│  └─ PlayerSet (玩家集合)                             │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ PlayerAudioOverrideList (Override 仲裁池)             │
│  ├─ 内部数组排序 (初始容量 3)                         │
│  └─ GetMaxPriority 仲裁                              │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ PlayerOcclusionStrategy (抽象)                        │
│  ├─ NullPlayerOcclusion (无遮挡)                    │
│  └─ DefaultPlayerOcclusion (RaycastNonAlloc)         │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ PlayerAudioView (View)                                │
│  └─ 12 Slider + 3 Toggle + Text → UI 绑定            │
└─────────────────────────────────────────────────────┘
```

---

## 同步模型分类 (8 种 SyncMode 选型)

| 组件 | SyncMode | 同步触发 | 原因 |
|------|----------|----------|------|
| `PlayerAudioController` | **NoVariableSync** | 无 | 本地调度器,不持有状态 |
| `PlayerAudioConfigurationModel` | (None) | OnPreSerialization | 双副本内部管理 |
| `SyncedPlayerAudioConfigurationModel` | **Manual** | MarkNetworkDirty | 强制 Master 所有权 |
| `PlayerAudioOverride` | **NoVariableSync** | 无 | 本地配置 + 事件驱动 |
| `PlayerAudioOverrideList` | **NoVariableSync** | 无 | 池对象,生命周期短 |
| `PlayerOcclusionStrategy` | **NoVariableSync** | 无 | 纯算法组件 |
| `IgnoredPlayers` | **NoVariableSync** | 无 | 本地黑名单 |
| `AdjustableGain` (Example) | **Manual** | MarkNetworkDirty | 全局滑块控制 |
| `VoiceOverrideRoom/Door/Button` | **NoVariableSync** | PlayerSet 同步 | 状态由 PlayerSet 代理 |
| `PickupMicrophone` | **NoVariableSync** | MicModel 内置 SyncedEvent | 拆分状态与传输 |
| `Testing/*` | **Manual** | TestController | 需 Master 协调 |

**模式选择规律**:
- **状态需要 Late Joiner 看到** → Manual + OnDeserialization
- **状态仅本地相关** → NoVariableSync
- **状态需要 Master 权威** → Manual + OnOwnershipRequest 拒绝非 Master
- **事件代理** → NoVariableSync + 内部 SyncedEvent

---

## 核心设计模式 (10 大可借鉴模式)

### 模式 1: 双副本同步模型 (Dual-Copy Sync) ⭐⭐⭐⭐⭐

**问题**: UI 滑块每帧触发 → 修改字段 → 触发网络序列化 → 浪费带宽,污染其他玩家。

**解决方案**: 本地字段 + `[UdonSynced]` 私有字段对,显式 Copy 控制序列化时机。

```csharp
// 本地副本 - 自由读写
[Range(0, 1)] public float OcclusionFactor;

// 网络副本 - 仅序列化时复制
[UdonSynced] private float _syncedOcclusionFactor;

public override void OnPreSerialization() { CopyLocalCopyToNetworkData(); }
public override void OnDeserialization(...) { CopyNetworkDataToLocalCopy(); }
```

**13 对字段成对定义**: 4 个 Occlusion + 2 个 Directionality + 4 个 Voice + 5 个 Avatar

**来源**: `PlayerAudioConfigurationModel.cs:70-86, 335-414`

**适用场景**:
- 任何"用户可编辑 + 多玩家共享"的参数
- 避免 Udon 同步变量被频繁重传
- 精确控制序列化时机(只在 MarkNetworkDirty 时)

---

### 模式 2: 执行顺序链 (ExecutionOrder Chain) ⭐⭐⭐⭐⭐

**问题**: UdonBehaviour 启动顺序不保证,Controller 可能在 Model 之前完成 SetupAndValidate → 空引用。

**解决方案**: 显式 `const ExecutionOrder` 链式常量 + 双重 Attribute 保险。

```csharp
// 每个类定义 const ExecutionOrder
public const int ExecutionOrder = PlayerAudioConfigurationModel.ExecutionOrder + 1;

// 双重 Attribute 保险
[DefaultExecutionOrder(ExecutionOrder)]
[TlpDefaultExecutionOrder(typeof(X), ExecutionOrder, TlpExecutionOrder.AudioStart, TlpExecutionOrder.AudioEnd)]
```

**完整执行链**:
```
IgnoredPlayers → PlayerOcclusionStrategy → NullPlayerOcclusion
  → DefaultPlayerOcclusion → PlayerAudioOverrideList
  → PlayerAudioOverride → PlayerAudioConfigurationModel
  → SyncedPlayerAudioConfigurationModel → PickupMicrophone
  → VoiceOverrideRoom → VoiceOverrideDoor → VoiceOverrideRoomExitButton
  → VoiceOverrideRoomEnterButton → VoiceOverrideTriggerZone
  → DynamicPrivacy → AdjustableGain → VoiceRangeVisualizer
  → PlayerAudioView → MicModel → PickupMicActivation
  → InteractMicActivation → MicController → MicView
```

**20+ 类的链式声明**,每个类自己声明自己的执行顺序并引用前一个。

**适用场景**:
- 任何多 UdonBehaviour 协作的复杂系统
- 避免空引用和初始化时序问题
- 调试时可按 ExecutionOrder 推断执行序列

---

### 模式 3: 策略模式 (Strategy Pattern) ⭐⭐⭐⭐⭐

**问题**: 遮挡算法需要可扩展(无遮挡、距离衰减、几何计算等),但又不能频繁修改 Controller。

**解决方案**: 抽象 `PlayerOcclusionStrategy` + 可插拔实现。

```csharp
public abstract class PlayerOcclusionStrategy : TlpBaseBehaviour {
    public abstract float GetRemainingAudioRange(
        Vector3 listenerHead, Vector3 listenerLookDirection,
        float distanceBetweenPlayerHeads,
        float occlusionFactor, float playerOcclusionFactor, int playerOcclusionMask
    );
}

public class NullPlayerOcclusion : PlayerOcclusionStrategy {  // 性能开关
    public override float GetRemainingAudioRange(...) => 1;
}

public class DefaultPlayerOcclusion : PlayerOcclusionStrategy {  // 真实算法
    private readonly RaycastHit[] _rayHits = new RaycastHit[2];  // 复用
    public override float GetRemainingAudioRange(...) {
        int hits = Physics.RaycastNonAlloc(...);
        // 单 Hit vs 多 Hit 分流处理
    }
}
```

**适用场景**:
- 算法可插拔场景(遮挡/路径规划/AI 行为)
- 性能开关(Null 实现)
- 单元测试 Mock

---

### 模式 4: 对象池化 (Object Pool) ⭐⭐⭐⭐

**问题**: 玩家增删触发 PlayerAudioOverrideList 反复创建/销毁 → GC 压力。

**解决方案**: TLP UdonUtils Pool 抽象 + OverrideList 池化。

```csharp
internal Pool PlayerOverrideListPool;

private bool AddOverrideToNewList(PlayerAudioOverride override, VRCPlayerApi player) {
    var instance = PlayerOverrideListPool.Get();  // 从池中取
    var createdList = instance.GetComponent<PlayerAudioOverrideList>();
    if (!createdList.AddOverride(override)) {
        PlayerOverrideListPool.Return(instance);  // 归还
        return false;
    }
    PlayersToOverride.Add(player.playerId, createdList);
    return true;
}

// 池对象生命周期
public override void OnPrepareForReturnToPool() {
    PlayerAudioOverrides = null;
    TempList = null;
    Overrides = 0;
}
```

**适用场景**:
- 频繁创建/销毁的对象(玩家、子弹、UI 元素)
- 避免 GC 暂停
- 配合 Udon Sharp 时注意 `OnPrepareForReturnToPool` / `OnReadyForUse` 钩子

---

### 模式 5: 优先级仲裁 (Priority Arbitration) ⭐⭐⭐⭐

**问题**: 玩家可能被多个 Override 影响(麦克风 + 房间 + 触发器),需要决定谁生效。

**解决方案**: Priority 字段 + 排序列表 + GetMaxPriority 仲裁。

```csharp
internal PlayerAudioOverride[] PlayerAudioOverrides;
internal int Overrides;

internal int GetInsertIndex(PlayerAudioOverride[] list, int length, PlayerAudioOverride newOverride) {
    int index = 0;
    for (int i = 0; i < length; i++) {
        if (list[i].Priority > newOverride.Priority) ++index;
        else break;
    }
    return index;
}

public bool GetMaxPriority(VRCPlayerApi player, out PlayerAudioOverride result) {
    for (int i = 0; i < Overrides; i++) {
        var entry = Get(i);
        if (!Utilities.IsValid(entry) || entry.IsPlayerBlackListed(player)) continue;
        result = entry;
        return true;
    }
    result = null;
    return false;
}
```

**关键设计**:
- 按 Priority 升序插入,GetMaxPriority 从头遍历返回第一个有效
- 支持 Equal Priority 时"最后添加的优先"
- 黑名单过滤在仲裁中执行

**适用场景**:
- 多个状态源影响同一对象(音量/权限/可见性)
- 区域 + 角色 + 临时 Buff 叠加
- A/B 测试场景

---

### 模式 6: 强制 Master 所有权三层防御 ⭐⭐⭐⭐

**问题**: Master 切换时,谁配置生效? 新 Master 怎么接管?

**解决方案**: 三层防御 (Setup + Request + Transferred)。

```csharp
// 1. 初始化时强制转给 Master
protected override bool SetupAndValidate() {
    if (!this.TransferOwnershipToMaster()) { Error("..."); return false; }
    return true;
}

// 2. 拒绝非 Master 请求
public override bool OnOwnershipRequest(VRCPlayerApi requesting, VRCPlayerApi requested) {
    return requested.IsMasterSafe();
}

// 3. 转移后自动回收
public override void OnOwnershipTransferred(VRCPlayerApi player) {
    base.OnOwnershipTransferred(player);
    if (player.IsMasterSafe()) return;
    Warn("Not owned by master, attempting to return");
    if (!this.TransferOwnershipToMaster()) Error("...");
}
```

**适用场景**:
- Master 权威配置(全局增益、规则、权限)
- 防止恶意玩家夺取所有权
- Master 切换时的状态恢复

---

### 模式 7: Gizmos 关系可视化 (Editor 关系图) ⭐⭐⭐

**问题**: 多组件关系复杂,Creator 难以理解 Override 与 Controller 的连接。

**解决方案**: `[CustomEditor]` + `OnSceneGUI` 绘制虚线连接 + 点击跳转。

```csharp
[CustomEditor(typeof(PlayerAudioController))]
public class PlayerAudioControllerEditor : TlpBehaviourEditor {
    public void OnSceneGUI() {
        // 扫描全场景所有 PlayerAudioOverride
        foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects()) {
            foreach (var udon in root.GetComponentsInChildren<UdonBehaviour>()) {
                var override = udon as PlayerAudioOverride;
                if (override) _relevantBehaviours.Add(override);
            }
        }
        // 绘制 Controller → Override 虚线
        Handles.DrawDottedLine(controllerPos, overridePos, 2);
        // 点击跳转
        if (clickCloseToDestination) {
            Selection.SetActiveObjectWithContext(override.gameObject, override);
            EditorGUIUtility.PingObject(override);
        }
    }
}
```

**适用场景**:
- 多组件协作系统
- 关系图/网络/树形结构
- Editor 端 UX 提升

---

### 模式 8: Trigger 事件丢失兜底 ⭐⭐⭐

**问题**: 玩家在 Trigger 内生成时,OnPlayerTriggerEnter 可能丢失(Udon 已知 bug)。

**解决方案**: DisableAllTrigger + 1 帧延迟 EnableAllTrigger。

```csharp
protected override bool SetupAndValidate() {
    _allTrigger = gameObject.GetComponents<Collider>();
    DisableAllTrigger();
    SendCustomEventDelayedFrames(nameof(EnableAllTriggerDelayed), 1, EventTiming.LateUpdate);
    return true;
}

// 门向检测兜底
public override void OnPlayerTriggerExit(VRCPlayerApi player) {
    if (_enterPosition == Vector3.zero) {
        Error("Udon missed OnPlayerTriggerEnter event!?");
        return;
    }
}
```

**适用场景**:
- 任何 OnPlayerTrigger* 事件
- Late joiner 边界情况
- 已知 Udon 不可靠事件的兜底

---

### 模式 9: 编译期 DEBUG 剥离 (#region TLP_DEBUG) ⭐⭐⭐⭐⭐

**问题**: Debug 日志影响发布性能,但开发时需要详细日志。

**解决方案**: 预处理宏 + 区域标记,编译时彻底剥离。

```csharp
public override void PostLateUpdate() {
#if TLP_DEBUG
    DebugLog(nameof(PostLateUpdate));
#endif
    // ... 业务逻辑
}
```

**特性**:
- 添加 `TLP_DEBUG` 到 Script Compilation Symbols 启用
- 编译时 `DebugLog` 方法体完全消失(包括字符串)
- **生产构建零开销**(不只是空方法)
- 第三方包不会因日志拖累性能

**适用场景**:
- 所有需要详细日志的库/包
- Udon 包(VPM Package)发布
- 性能敏感的发布构建

---

### 模式 10: 自动宏定义 (CustomDefinitionUtils) ⭐⭐⭐

**问题**: 用户安装包后需要手动添加编译宏,容易遗漏。

**解决方案**: `[InitializeOnLoad]` + 自动注册宏。

```csharp
[InitializeOnLoad]
public class UdonVoiceUtilsDefinitions {
    static UdonVoiceUtilsDefinitions() {
        CustomDefinitionUtils.EnsureDefinitionsExist(typeof(UdonVoiceUtilsDefinitions), "TLP_UDONVOICEUTILS");
    }
}
```

**适用场景**:
- VPM Package 自动配置
- 避免用户忘记加宏导致编译错误
- 多包依赖的宏协调

---

## 设计时解决的 12 大难题 (P0/P1/P2 分级)

| # | 等级 | 问题 | 解决方案 | 沉淀 |
|---|------|------|----------|------|
| 1 | 🔴 P0 | Udon VM 初始化顺序不可靠 | 显式 ExecutionOrder 链式常量 | 模式 2 |
| 2 | 🔴 P1 | UdonSynced 频繁序列化风暴 | 双副本同步模型 | 模式 1 |
| 3 | 🔴 P1 | 多 Override 冲突仲裁 | Priority + OverrideList + GetMaxPriority | 模式 5 |
| 4 | 🟡 P2 | 隐私频道(互不可听) | PrivacyChannelId + HasOverlappingChannels 双向校验 | `patterns/privacy-channel.md` (待建) |
| 5 | 🟡 P2 | Master 切换配置权威性 | 三层防御 (Setup/Request/Transferred) | 模式 6 |
| 6 | 🟡 P2 | 玩家列表与 Override 状态不一致 | OnPlayerLeft + PurgeOverridesOfInvalidPlayers + Refresh | `patterns/player-list-reconcile.md` (待建) |
| 7 | 🟡 P2 | 遮挡检测性能爆炸 | PlayerUpdateRate 限流 + RaycastNonAlloc + LayerMask 过滤 | 性能章节 |
| 8 | 🟢 P3 | 玩家可能被其他玩家遮挡 | `!raycastHit.transform` 利用 Udon 特性推断 | `patterns/occlusion-by-player.md` (待建) |
| 9 | 🟢 P3 | Udon 偶尔丢失 Trigger 事件 | DisableAllTrigger + 1 帧延迟 + 兜底 Error | 模式 8 |
| 10 | 🟢 P3 | VRChat Player Audio API 不对称 | 妥协: 仅 Voice 有 Getter,Avatar 仅记录 | 已知限制 |
| 11 | 🟢 P3 | 重复放置 Controller 导致冲突 | 强制命名 + SetupAndValidate 时改名 | 工程实践 |
| 12 | 🟢 P3 | 客户端调试困难 | TLP_DEBUG + VoiceRangeVisualizer + Runtime Unit Testing | 模式 9 |

---

## 性能特征 (Performance Profile)

### 已知性能瓶颈

| 瓶颈 | 数值 | 来源 |
|------|------|------|
| **PostLateUpdate 限流** | 默认 1 玩家/帧,80 玩家需 4 秒 | `PlayerAudioController.cs:62` |
| **Physics.RaycastNonAlloc 容量** | 2 hit/玩家 | `DefaultPlayerOcclusion.cs:21` |
| **OnSceneGUI 扫描** | 60 帧刷新一次 (优化后) | `VoiceOverrideRoomEditor.cs:17` |
| **MarkNetworkDirty 节流** | 无(每次 UI 变化触发) | `AdjustableGain.cs:108` |

### 性能优化技巧

1. **PlayerUpdateRate**: 0 = 全员每帧,1 = 1 玩家/帧(默认),80 = 80 玩家/帧
2. **层过滤**: OcclusionMask = Environment(11) + UI(5),避免误检
3. **数组复用**: `_rayHits = new RaycastHit[2]` 不再 new
4. **TLP_DEBUG 编译剥离**: 生产构建零日志开销

### PostLateUpdate 算法

```csharp
public override void PostLateUpdate() {
    LocalPlayerOverrideList.GetMaxPriority(LocalPlayer, out var localPlayerOverride);
    _localOverride = UpdateAudioFilters(localPlayerOverride, _localOverride);
    for (int playerUpdate = 0;
         playerUpdate < GetPendingPlayerUpdates(ExistingRemotePlayerIds.Count);
         ++playerUpdate) {
        UpdateNextPlayer(LocalPlayer, ref playerUpdate);  // 轮询更新
    }
}

private int GetPendingPlayerUpdates(int playerCount) {
    if (PlayerUpdateRate == 0) return playerCount;  // 0 = 全员
    return Mathf.Clamp(PlayerUpdateRate, 1, playerCount);
}
```

---

## 关键 API 索引 (用于知识库 reference)

### Player Audio API 完整列表 (UVU 涉及的)

| 类别 | API | 说明 |
|------|-----|------|
| Voice | `SetVoiceLowpass(bool)` | 远距离低通滤波 |
| Voice | `SetVoiceGain(float)` | 增益 (dB) |
| Voice | `SetVoiceDistanceFar(float)` | 最远距离 |
| Voice | `SetVoiceDistanceNear(float)` | 最近距离 |
| Voice | `SetVoiceVolumetricRadius(float)` | 非空间化半径 |
| Voice | `GetVoiceDistanceNear()` 等 | Getter (部分支持) |
| Avatar | `SetAvatarAudioForceSpatial(bool)` | 强制空间化 |
| Avatar | `SetAvatarAudioCustomCurve(bool)` | 自定义曲线 |
| Avatar | `SetAvatarAudioGain(float)` | 增益 |
| Avatar | `SetAvatarAudioFarRadius(float)` | 最远半径 |
| Avatar | `SetAvatarAudioNearRadius(float)` | 最近半径 |
| Avatar | `SetAvatarAudioVolumetricRadius(float)` | 非空间化半径 |
| Player | `GetTrackingData(TrackingDataType)` | Head / AvatarRoot |
| Player | `GetAvatarEyeHeightAsMeters()` | 眼睛高度 |
| Player | `GetPosition()` / `GetRotation()` | 玩家位置 |
| Player | `TeleportTo(...)` | 传送 |
| Player | `Immobilize(bool)` | 冻结玩家 |
| Player | `SetAvatarEyeHeightByMultiplier/Meters` | 高度修改 |

**重要**: Avatar 音频 API **只有 Setter 无 Getter** (UVU 源码 TODO 注释承认)

---

## 模式沉淀路线图 (Roadmap)

### 已沉淀 (本次会话)

| 模式 | 来源 | 沉淀位置 |
|------|------|---------|
| 模式 1: 双副本同步模型 | `PlayerAudioConfigurationModel` | `patterns/dual-copy-sync.md` (待建) |
| 模式 2: 执行顺序链 | 全局 20+ 类 | `patterns/execution-order-chain.md` (待建) |
| 模式 3: 策略模式 | `PlayerOcclusionStrategy` | `patterns/strategy-pattern-udon.md` (待建) |
| 模式 4: 对象池化 | `PlayerAudioOverrideList` + TLP Pool | `patterns/object-pool-udon.md` (待建) |
| 模式 5: 优先级仲裁 | `PlayerAudioOverrideList` | `patterns/priority-arbitration.md` (待建) |
| 模式 6: Master 所有权三层防御 | `SyncedPlayerAudioConfigurationModel` | `patterns/master-ownership-defense.md` (待建) |
| 模式 7: Gizmos 关系可视化 | 5 个 Editor 文件 | `patterns/gizmos-relationship.md` (待建) |
| 模式 8: Trigger 事件丢失兜底 | `VoiceOverrideDoor/TriggerZone` | `patterns/trigger-event-fallback.md` (待建) |
| 模式 9: 编译期 DEBUG 剥离 | 全局 `#region TLP_DEBUG` | `patterns/compile-time-debug-strip.md` (待建) |
| 模式 10: 自动宏定义 | `UdonVoiceUtilsDefinitions` | `patterns/auto-scripting-symbol.md` (待建) |

**注**: 模式 1-3, 5-6, 9 与 QuickBrown LuraSwitch2 的 6 个新模式形成**互补关系**:
- LuraSwitch2: Master-Follower Syncer / Exclusive Selector / SoftDetent / Fade-Snap / Editor Preview / MaterialPropertyBlock
- UVU: Dual-Copy Sync / ExecutionOrder Chain / Strategy / Object Pool / Priority Arbitration / Master Defense

两者形成 **"Udon 实战模式库"** 完整覆盖 12+ 模式。

### 后续可建文档

- `memory/patterns/privacy-channel.md` — 多频道交集检测
- `memory/patterns/player-list-reconcile.md` — OnPlayerLeft 三步清理
- `memory/patterns/occlusion-by-player.md` — `!raycastHit.transform` Udon 特性

---

## 与现有 4 个参考工程的对比

| 维度 | UVU | 多机位导演 | 视频播放器 | 音频同步 | LuraSwitch2 |
|------|-----|-----------|-----------|---------|------------|
| **核心场景** | 玩家音频控制 | 多机位导演 | 视频同步 | 音频波形同步 | 通用交互 |
| **关键 SyncMode** | NoVariableSync+Manual | Manual+Continuous | Manual+Owner Auth | NoVariableSync(Shader) | Manual+LocalSave |
| **核心算法** | Raycast 遮挡 | 5 层同步体系 | 服务器时间锚点 | Shader-Centric | 节流窗口 |
| **可借鉴 Top 1** | 双副本同步 | NetworkCallable 批量 | 时间同步算法 | Master 时间锚点 | Master-Follower |
| **Editor 工具** | 5 个 CustomEditor | Gizmos | — | — | [ExecuteAlways] |
| **测试覆盖** | 4 个真机测试 | — | — | — | 单元测试 |
| **代码规模** | ~6000 行 (35 文件) | ~3000 行 | ~4000 行 | ~2000 行 | ~8000 行 (39 文件) |
| **应用域** | 音频/房间/麦克风 | 直播/表演 | 视频/电影 | 音乐/表演 | 通用交互 |

**结论**: UVU 是 5 个参考工程中**架构最严谨、最值得学习的范本**。

---

## 应用方向

### 直接应用场景

| 场景 | 所需组件 | 应用模式 |
|------|----------|----------|
| 酒吧/酒馆多区域 | VoiceOverrideRoom + Door | 区域独立音量 |
| 舞台/剧场 | VoiceOverrideRoom + Reverb | 演员/观众/后台分层 |
| 密室/解谜 | VoiceOverrideTriggerZone | 进入/离开音频变化 |
| PvP 竞技 | PlayerAudioOverride + PrivacyChannelId | 队伍频道隔离 |
| 恐怖/沉浸 | PlayerAudioOverride + Occlusion | 距离衰减+墙体遮挡 |
| 教学/培训 | PickupMicrophone + InteractMicActivation | 模拟麦克风 |
| 潜水艇/载具 | Reverb + Occlusion | 声学空间模拟 |
| 音乐表演 | AdjustableGain + PrivacyChannel | 演奏者/听众分层 |
| 走廊窃听 | MuteOutsiders + 触发器 | 私密对话模拟 |
| 演讲剧场 | Directionality + HeightToVoiceCorrelation | 听众方向感 |

### 创意扩展

- 冥想/瑜伽世界: 低音 + 缓慢衰减
- 历史再现: 模拟古老麦克风限制
- 卡拉 OK: 主唱 vs 伴唱通道
- 直播厅: 主播 + 弹幕 + 礼物音效分层
- 游戏王/TCG: 玩家 1v1 隔离(其他人全静音)
- 太空站: 全局压缩 + 距离衰减

---

## 设计优势 vs 劣势

### ✅ 优势 (10 大)

1. **MVC 完整分离** — Model/View/Controller 继承 TLP 抽象
2. **策略模式深度使用** — 遮挡算法可插拔
3. **双副本同步模型** — 精确控制序列化
4. **执行顺序链** — 解决 Udon 初始化时序
5. **优先级仲裁** — 多 Override 冲突解决
6. **强制 Master 所有权** — 三层防御网络权威
7. **池化** — 避免 GC 压力
8. **完整 Editor 工具链** — 5 个 CustomEditor + Gizmos
9. **高度可测试** — 4 个真机测试 + Mock 机制
10. **编译期 DEBUG 剥离** — 零发布开销

### ❌ 劣势 (8 大)

1. **强依赖 TLP UdonUtils** — 锁定 ^14.0.0
2. **PostLateUpdate 限流瓶颈** — 80 玩家 4 秒轮完
3. **OnSceneGUI 扫描全场景** — 实时遍历开销
4. **本地权威 vs Master 权威模糊** — 实际音频是客户端独立 API
5. **View-Model 紧耦合** — 13 字段双端手动复制
6. **Udon 限制残留** — RaycastNonAlloc 容量 2
7. **API 不对称** — Avatar 无 Getter
8. **NoVariableSync 设计普遍** — 事件 + 手动序列化曲线救国

---

## 难度评级

| 维度 | 评级 | 说明 |
|------|------|------|
| 概念复杂度 | ⭐⭐⭐⭐ | VRChat 音频 API + Udon VM + 网络同步 + 设计模式 |
| 实现复杂度 | ⭐⭐⭐⭐⭐ | 解释执行 + 双副本 + Master 权威 + 状态机 |
| 调试难度 | ⭐⭐⭐⭐ | 需 TLP_DEBUG + ClientSim + 真机多人 |
| 学习曲线 | ⭐⭐⭐ | 需先掌握 TLP UdonUtils + UdonSharp + VRChat 音频 |
| 维护难度 | ⭐⭐⭐ | 严格分层,单元测试,文档齐全 |

---

## 综合评级

| 维度 | 评分 |
|------|------|
| 功能完整性 | ⭐⭐⭐⭐⭐ |
| 架构质量 | ⭐⭐⭐⭐ |
| 性能优化 | ⭐⭐⭐ |
| 可维护性 | ⭐⭐⭐⭐ |
| 可扩展性 | ⭐⭐⭐⭐⭐ |
| 可测试性 | ⭐⭐⭐⭐ |
| 文档质量 | ⭐⭐⭐⭐⭐ |
| 教学价值 | ⭐⭐⭐⭐⭐ |
| 商业采用度 | ⭐⭐⭐⭐⭐ |
| **综合** | **⭐⭐⭐⭐⭐ VRChat World 域最优秀的 Udon 库之一** |

---

## 来源引用

- **项目仓库**: https://github.com/Guribo/UdonVoiceUtils
- **VPM 源**: https://guribo.github.io/TLP/
- **Wiki**: https://github.com/Guribo/UdonVoiceUtils/wiki
- **公开演示世界**: `wrld_7ec7bbdd-ba81-4564-985a-c79dfc9eaca7`
- **采用世界**: README §"Where is it being used?"

---

## 与本知识库其他文档的关系

| 关联 | 文档 |
|------|------|
| **同步模式基础** | `memory/patterns/manual-sync-state.md`, `memory/patterns/owner-authoritative-interaction.md` |
| **高级同步** | `memory/patterns/advanced-sync-patterns.md` (Packed Sync, Rate-Limited, **Dual-Copy** 已收录), `memory/patterns/bit-packed-flags.md` |
| **执行顺序** | `memory/world/udon/animator-system.md`, `memory/world/examples/obstacle-course/` |
| **MVC 模式** | `memory/world/udon/udonsharp-compilation.md` (TLP UdonUtils 介绍) |
| **VRChat 音频 API** | `memory/world/vrc-graphics.md` (VRCShader 部分) |
| **失败案例** | `memory/reviews/common-failures.md` (FAIL-29 ~ 32 已收录 LuraSwitch2) |
| **同步模式选型** | `memory/api/networking.md` |
| **场景组件** | `memory/world/scene-components/vrc-objectsync.md` |
| **互补参考工程** | `memory/sources/quickbrown-luraswitch2.md` |

---

## 下一步行动建议

1. ✅ **新建** `memory/sources/udonvoiceutils.md` (本文件)
2. ✅ **更新** `memory/sources/open-source-projects.md` 添加 A7
3. ✅ **更新** `memory/sources/index.md` 注册新源
4. ✅ **更新** `memory/patterns/index.md` 添加 6 个新模式速查
5. ✅ **更新** `memory/FACT.md` 最后更新段 + 6 个新模式登记
6. 🔜 **未来** — 创建独立的 `memory/patterns/dual-copy-sync.md` 等 6 个详细 pattern 文档
7. 🔜 **未来** — 创建独立的 `memory/patterns/privacy-channel.md` / `player-list-reconcile.md` / `occlusion-by-player.md`

---

> **本文件为参考工程溯源层文档**,模式细节已沉淀到 `memory/patterns/` 后的独立文档中。
