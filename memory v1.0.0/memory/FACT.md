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
│   ├── udonsharp-compilation.md  # UdonSharp 编译管线
│   ├── vrc-graphics.md       # VRCGraphics/VRCShader API
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

## 视频播放器时间同步算法模式(参考工程) ✅ (2026-06-06)

> **本节定位**:通过分析开源视频播放器项目提炼的时间同步算法设计模式,适用于多人同步媒体播放场景
> **知识模式**:Manual Sync + Owner Authority + 服务器时间锚点

### 核心架构(三层职责分离)

| 组件 | 职责 |
|------|------|
| **主控制器** | 状态机、视频控制、时间同步 |
| **前端处理器** | 播放列表、队列、历史记录 |
| **播放后端抽象** | 视频后端实现隔离(便于切换不同播放器) |

### 同步模式: Manual Sync + Owner Authority

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public partial class VideoCore : UdonSharpEventSender {
    bool RequestSync() {
        if (!synced) return false;
        if (!Networking.IsOwner(gameObject)) 
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        RequestSerialization();
        return true;
    }
}
```

### Core 同步变量设计

| 变量 | 类型 | 说明 |
|------|------|------|
| `pcUrl/questUrl` | VRCUrl | 跨平台 URL |
| `activePlayer` | byte | 活跃播放器 (1-based) |
| `state` | byte | 0=Idle, 1=Loading, 2=Playing, 3=Paused |
| `loop` | bool | 循环状态 |
| `time` | int | 毫秒 (视频时间或暂停进度) |
| `ownerNetworkTime` | int | 服务器时间锚点 |
| `rangeLoopStart/End` | int | A-B 循环范围 |
| `syncedSpeed` | float | 播放速度 |
| `performerId` | ushort | 表演者 ID |

### 时间同步算法

**Owner 端计算**(服务器时间锚点):
```csharp
double CalcSyncTime(out float actualSpeed) {
    actualSpeed = activeHandler.Speed;
    var videoTime = Mathf.Repeat(activeHandler.Time, duration);
    double syncTime = videoTime / actualSpeed - syncOffset + PerformerLatency;
    if (activeHandler.IsPlaying) {
        long serverTimeMs = Networking.GetServerTimeInMilliseconds() - (long)(syncTime * 1000);
        syncTime = serverTimeMs * 0.001;
    }
    return syncTime;
}
```

**Non-Owner 端计算**(本地推算视频时间):
```csharp
float CalcVideoTime() {
    switch (state) {
        case PLAYING: 
            videoTime = (float)((Networking.CalculateServerDeltaTime(
                Networking.GetServerTimeInSeconds(), time * 0.001) 
                + syncOffset + syncLatency - PerformerLatency) * actualSpeed);
            break;
        case PAUSED: 
            videoTime = time * 0.001F;
            break;
    }
}
```

### 关键设计模式

| 模式 | 实现 |
|------|------|
| **服务器时间锚点** | `ownerNetworkTime` 作为同步基准 |
| **阈值同步** | `timeDriftDetectThreshold = 0.9F`，减少序列化频率 |
| **双缓冲状态** | `localXxx` + `[UdonSynced] xxx` 分离网络/本地 |
| **冷却期** | `OWNER_SYNC_COOLDOWN_TICKS = 3s`，防止同步风暴 |
| **双击同步** | 快速双击请求 Owner 同步，单击本地重新加载 |
| **表演者模式** | `PerformerLatency` 动态补偿网络延迟 |
| **缓冲保护** | 缓冲时不强制同步，避免卡顿 |

### 序列化生命周期

1. **OnPreSerialization**: 打包完整状态（URL + 播放器 + 状态 + 时间）
2. **OnDeserialization**: 解析并同步状态，计算延迟补偿

### 前端处理器同步设计

- **播放列表**: `playListOrder`, `playingIndex`, `playListIndex`
- **队列**: `queuedUrls`, `queuedTitles`, `queuedPlayerIndex`
- **字符串拼接**: 使用 `\u2029` (Paragraph Separator) 避免冲突

---

> **📚 参考实现**
>
> 本节"视频播放器时间同步算法"提炼自开源 VRChat 视频播放器项目(VRChat World 域)。
> 该项目是 VRChat 创作者生态中最流行的同步视频播放方案之一。
>
> 详细项目信息见:[`memory/sources/open-source-projects.md`](sources/open-source-projects.md) §视频播放器类目

---

## 核心设计模式（已验证）

### 1. Shader-Centric 数据传递(参考工程)
**原理**：将高频变化数据编码为纹理，Shader 直接采样，避免网络同步

```csharp
audioMaterial.SetFloatArray(_Samples0L, _samples);  // 零网络同步
audioMaterial.SetFloatArray(_Samples1L, _samples);
```

**适用场景**：位置历史、轨迹、音频数据、粒子系统状态
**优势**：同步成本从 O(n) 降为 O(1)
**【验证:开源音频同步系统源码】**

### 2. Master 权威时间锚点(参考工程)
**原理**：Master 写入实例加入时间，其他客户端本地计算 elapsed time

```csharp
[UdonSynced] private double _masterInstanceJoinTime;

if (Networking.IsMaster)
{
    _masterInstanceJoinTime = startTime;
    RequestSerialization();
}
```

**长运行时保护**：MSW 分层防止浮点精度丢失

```csharp
const double elapsedTimeMSWBoundary = 1024;
if (_elapsedTime >= elapsedTimeMSWBoundary)
{
    _fpsTime = 0;
    _elapsedTime -= elapsedTimeMSWBoundary;
    _elapsedTimeMSW++;
}
```

**【验证:开源音频同步系统源码】**

### 3. 位域压缩同步(参考工程)
**原理**：用单个 byte/bit 字段存储多个布尔值，减少序列化带宽

```csharp
[UdonSynced] byte _flags = 0b10;  // bit0=playing, bit1=locked

private void CopyIntoFlags()
{
    _flags = 0;
    if (_syncOwnerPlaying) _flags |= 1;
    if (_syncLocked) _flags |= 2;
}
```

**【验证:开源音频同步系统源码】**

> **底层原理与位运算完整参考**: `memory/world/udon/data-containers/byte-and-bit-operations.md`
> **同步模式应用**: `memory/patterns/bit-packed-flags.md`

### 4. 漂移校正算法(参考工程)
**原理**：本地时间与网络时间差值缓慢收敛，避免瞬时抖动

```csharp
int networkTimeDelta = networkTimeMSNow - _networkTimeMS;
if (networkTimeDelta > 3000)
{
    _networkTimeMS = networkTimeMSNow;  // 重大中断，重置
}
else
{
    _networkTimeMS += networkTimeDelta / 20;  // 缓慢校正 (5%)
}
```

**【验证:开源音频同步系统源码】**

### 5. 平台兼容预处理(参考工程)
**原理**：#if UDONSHARP 区分 Udon 和 Standalone 代码路径

```csharp
#if UDONSHARP
    using UdonSharp;
    using VRC.SDKBase;
    public class X : UdonSharpBehaviour { ... }
#else
    public class X : MonoBehaviour { ... }  // Editor 工具等
#endif
```

**【验证:开源音频同步系统源码】**

### 6. Manual Sync + Owner Authority(参考工程)
**原理**：显式控制同步时机，Owner 计算同步值，Non-Owner 接收并计算

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
bool RequestSync() {
    if (!Networking.IsOwner(gameObject))
        Networking.SetOwner(Networking.LocalPlayer, gameObject);
    RequestSerialization();
}
```

**时间同步核心**：服务器时间锚点 + 阈值触发 + 延迟补偿
**【验证:开源视频播放器源码】**

### 7. NetworkCallable RPC + 批量延迟提交(参考工程)
**原理**：`[NetworkCallable]` 封装参数化远程调用，`_serializationPending` 合并多次修改，单次序列化

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PlayerTrackingSystem : UdonSharpBehaviour
{
    private bool _serializationPending = false;

    [NetworkCallable]
    public void SetTrackingDataType(int TempType)
    {
        TrackingID = TempType;
        TrackingDataType = (VRCPlayerApi.TrackingDataType)TempType;
        ScheduleSerialization();
    }

    private void ScheduleSerialization()
    {
        if (!_serializationPending)
        {
            _serializationPending = true;
            SendCustomEventDelayedSeconds(nameof(NetworkingCall), 1f);
        }
    }

    public void NetworkingCall()
    {
        if (!Networking.IsOwner(this.gameObject)) return;
        if (_serializationPending)
        {
            RequestSerialization();
            _serializationPending = false;
        }
    }

    public override void OnPlayerJoined(VRCPlayerApi player)
    {
        if (Networking.IsOwner(gameObject))
            RequestSerialization();  // 新玩家加入时主动同步
    }
}
```

**优势**：多次快速修改合并为单次序列化；`SendCustomEventDelayedSeconds` 提供自然的冷却期
**适用场景**：UI 滑块、配置参数等频繁修改但需网络同步的场景
**【验证:开源多机位导演系统源码】**

### 8. 双缓冲预览模式(参考工程)
**原理**：`_isPreviewActive` 区分本地预览状态与网络同步状态，预览值不会意外覆盖网络值

```csharp
private bool _isPreviewActive = false;

public void TempWriteIn()
{
    _isPreviewActive = true;  // 进入预览模式
    OnDeserialization();      // 本地应用预览值
}

public override void OnPlayerJoined(VRCPlayerApi player)
{
    if (Networking.IsOwner(gameObject) && !_isPreviewActive)
    {
        RequestSerialization();  // 仅非预览状态下才同步
    }
}

private void ScheduleSerialization()
{
    _isPreviewActive = false;  // 退出预览模式
    // ...
}
```

**设计意图**：编辑器中实时预览参数调整，不触发网络同步；用户确认后才真正同步
**【验证:开源多机位导演系统源码】**

### 9. 指数衰减插值同步(参考工程)
**原理**：Continuous 同步值通过指数衰减逐步逼近目标，平滑网络抖动

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Continuous)]
public class AnimatorFastSYNC : UdonSharpBehaviour
{
    [UdonSynced] private float SliderValue;

    private void Update()
    {
        if (LocalPlayer == Owner) return;
        var FloatV = AnimatorUSE.GetFloat("Float1");
        FloatV = (SliderValue - FloatV) * Time.deltaTime * Compensation;
        AnimatorUSE.SetFloat("Float1", FloatV);
    }
}
```

**公式**：
$$v_{local} = v_{local} + (v_{remote} - v_{local}) \cdot \Delta t \cdot K$$

**优势**：网络抖动被平滑，不依赖服务器时间戳
**劣势**：Continuous 每帧序列化，带宽较高
**适用场景**：连续参数同步(UI 动画、缓动跟随)
**替代方案**：高频场景建议改用 Manual + 阈值触发
**【验证:开源多机位导演系统源码】**

### 10. Slerp/Slerp 本地缓动插值(参考工程)
**原理**：相机等高平滑需求使用 `Quaternion.Slerp` + `Vector3.Slerp`，支持位置/旋转独立插值

```csharp
private void Update()
{
    if (Ready)
    {
        var quaternion = Quaternion.Slerp(
            Camera.transform.rotation,
            transformTarget.transform.rotation,
            SlarpV * Time.deltaTime * 20);

        Vector3 vector3;
        if (!positionSlarp)
        {
            vector3 = Vector3.Slerp(
                Camera.transform.position,
                transformTarget.transform.position,
                SlarpV * Time.deltaTime * 20);
        }
        else
        {
            vector3 = Vector3.Slerp(
                Camera.transform.position,
                transformTarget.transform.position,
                positionSlarpV * Time.deltaTime * 20);
        }

        Camera.transform.SetPositionAndRotation(vector3, quaternion);
    }
}
```

**关键参数**：
| 参数 | 说明 |
|------|------|
| `SlarpV` | 旋转插值因子 |
| `positionSlarpV` | 位置插值因子(可独立于旋转) |
| `positionSlarp` | 启用独立位置插值 |

**适用场景**：相机跟随、轨道运动、特效轨迹
**注意**：无网络同步，纯本地插值；目标位置由上层网络系统提供
**【验证:开源多机位导演系统源码】**

### 11. 所有权分层设计(参考工程)
**原理**：不同职责对象分配不同 Owner，避免单一 Owner 瓶颈

```
中央控制器(导演控制)→ 拥有全局状态
├── 跟踪相机(独立所有权 = 导演可抢)
├── 相机游戏对象(独立所有权 = 导演可抢)
└── 玩家跟踪系统(Owner = 被跟踪玩家)
```

```csharp
// 中央控制器:分配所有权
int Index = Array.IndexOf(Displayers, DisPlayName);
Networking.SetOwner(Players[Index], TrackingCamera.gameObject);
TrackingOwner = Networking.GetOwner(TrackingCamera.gameObject).displayName;

// 飞行相机系统:Station 进入时
Networking.SetOwner(Networking.LocalPlayer, this.gameObject);
Networking.SetOwner(Networking.LocalPlayer, Drone);

// 飞行相机系统:所有权转移
if (player == LocalPlayer)
    Managerudon.SendCustomEvent("ChangerUsingPlayer");
```

**设计原则**：
- **操作者** 控制设备/相机 → 拥有中央控制器/飞行相机系统
- **被跟踪者** 控制自身数据 → 拥有玩家跟踪系统
- **所有权转移** 通过 `Networking.SetOwner` + `OnOwnershipTransferred` 回调通知管理器

**【验证:开源多机位导演系统源码】**

### 12. NoVariableSync UI 转发模式(参考工程)
**原理**：UI 面板使用 `BehaviourSyncMode.None`，仅转发事件和 SetProgramVariable，不同步变量

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.NoVariableSync)]
public class UISignalForwarder : UdonSharpBehaviour
{
    public void InteractStart()
    {
        MainControl.SetProgramVariable("VoidNameID", VoidNameID);
        MainControl.SetProgramVariable("CameraTrackingTarget", CameraTrackingTarget);
        MainControl.SendCustomEvent("StartChanger");
    }
}

public void QuickSave()
{
    CameraName.value = SystemIndex;
    VoidName.value = VoidNameID;
    // 读取本地 UI 状态,不依赖网络同步
    InteractStart();
}
```

**设计意图**：UI 面板是本地控制器，将配置通过 SetProgramVariable 传递给主控制器
**优势**：UI 修改不触发网络序列化，性能最优
**适用场景**：控制面板、预设切换、调试 UI
**【验证:开源多机位导演系统源码】**

### 14. 带参网络同步 (NetworkCalling) ✅ (2026-06-09)

**使用场景**：需要直接传递参数的网络事件调用

**必须条件**：
| 条件 | 说明 |
|------|------|
| **using 语句** | `using VRC.SDK3.UdonNetworkCalling;` |
| **调用方式** | 必须使用 `NetworkCalling.SendCustomNetworkEvent` |
| **目标指定** | `(IUdonEventReceiver)target` 指定目标脚本（等效于 `udon.SendCustomNetworkEvent` 的 `udon` 部分） |

**语法**：
```csharp
using VRC.SDK3.UdonNetworkCalling;

// 调用带参网络事件
NetworkCalling.SendCustomNetworkEvent(
    (IUdonEventReceiver)targetUdonBehaviour,  // 目标脚本（强制转型）
    NetworkEventTarget.All/Owner/AllBuffered/...,  // 发送目标
    "MethodName",    // 方法名（字符串）
    P0, P1, P2...    // 参数（白名单类型）
);
```

**对比**：
| 方式 | 带参能力 | 调用语法 |
|------|----------|----------|
| `SendCustomNetworkEvent` | ❌ 无参 | `udon.SendCustomNetworkEvent(target, "Method")` |
| `NetworkCalling.SendCustomNetworkEvent` | ✅ 带参 | `NetworkCalling.SendCustomNetworkEvent((IUdonEventReceiver)udon, target, "Method", P0, P1...)` |

**参数白名单**：int, float, string, VRCUrl, Vector3, Quaternion, bool, VRCPlayerApi 及对应数组

---

### 13. SetProgramVariable 跨组件通信(参考工程)
**原理**：子系统间通过 `SetProgramVariable` + `SendCustomEvent` 传递配置，无需网络同步

```csharp
// 中央控制器:配置模块
UdonBehaviour ModUdon = ModName[VoidNameID - 1].GetComponent<UdonBehaviour>();
ModUdon.SetProgramVariable("CameraTrackingTarget", CameraTrackingTarget);
ModUdon.SetProgramVariable("Slarp", Slarp);
ModUdon.SetProgramVariable("VoidObjectActive", VoidObjectActive);
ModUdon.SendCustomEvent("ChangerTarget");

// 子系统:接收配置
UdonBehaviour udonBehaviour = SystemUdon[CameraTrackingTarget].GetComponent<UdonBehaviour>();
udonBehaviour.SetProgramVariable("VoidObjectActive", VoidObjectActive);
udonBehaviour.SendCustomEventDelayedFrames("OnEnable", 1);
```

**模式**：中央控制器 → SetProgramVariable → 子系统
**优势**：解耦子系统，子系统无需知道网络层细节
**注意**：需确保 SetProgramVariable 在目标脚本 enabled 之后调用
**【验证:开源多机位导演系统源码】**

---

## ULocalization 沙箱适配模式(参考工程) ✅ (2026-06-20)

> **本节定位**:通过分析 HoshinoLabs ULocalization 项目提炼的"如何用 Editor 端代码生成绕过 Udon VM 限制"的设计模式,适用于"包装 Unity 高层系统"的所有场景(序列化/输入/动画/物理/AI 等)
> **知识模式**:Build-Time vs Runtime Separation + Hash-Based Dispatch + IID + Slot Passing + Type Erasure

### 项目概况

ULocalization 是 VRChat UdonSharp 的本地化系统,**不是从零构建的本地化系统**,而是**Unity 官方 Localization 系统的 UdonSharp 适配层**。

| 指标 | 数值 |
|------|------|
| 总 .cs 文件 | 145 |
| Shim 字段数 | 27 (`_0` ~ `_26`) |
| 生成的 hash 方法数 | 500+ |
| 支持的 UnityEvent 目标类型 | 100+ |
| 支持的 IVariable 类型 | 16 + 4 扩展 |
| 支持的 LocalizeEvent 类型 | 5 |
| 支持的 LocalizedReference 类型 | 6 |
| `[RecursiveMethod]` 标注 | 6 处 |
| 同步模式 | `BehaviourSyncMode.None` |

### 5 大核心模式

| 模式 | 解决的问题 | 关键机制 |
|------|------------|----------|
| **Hash-Based Method Dispatch** | Udon 无委托/无函数指针 | `MD5(TypeName+MethodName)` → 500+ 预生成 wrapper → `SendCustomEvent(hash)` |
| **IID Object Identity** | Udon 无 Dictionary 索引 Object | Editor `IID.GenerateId` 顺序分配 int + 运行时 `int[]` 数组 |
| **Slot-Based Parameter Passing** | `SendCustomEvent` 无参数 | 3 个 object 字段(`_l_t`/`_l_p`/`_l_a`)作为参数槽位 |
| **Code Generation with Type Erasure** | Udon 无泛型方法 | `Type.FullName` MD5 作为 type ID + switch case + `object[2]` 元组 |
| **Build-Time vs Runtime Separation** | Unity Editor API 不可用 | Editor 端反射 + LINQ + 缓存 → 注入 27 字段 → Runtime O(1) 查表 |

### 5 模式协同工作流

```
[Editor Build 阶段]
1. 反射扫描所有 LocalizeEvent / LocalizedString / Variable
2. 给每个 (Type, Method) 生成 MD5 hash
3. 代码生成 500+ 个 hash 命名 wrapper 方法
4. 通过 Sardinject [Inject] 注入 27 个 object[] 字段到 LocalizationShim
5. IVRCSDKBuildProcessScene 钩子清理被替代的 LocalizeEvent

[Runtime 阶段]
1. Locale 变化 → Sardinal Signal 发布
2. LocalizationShim.SetSelectedLocale(locale)
3. 遍历所有 LocalizeEvent:
   a. 从 _8[idx] 获取 Localized 引用 (IID)
   b. 调用 _l_t = target, _l_p = value 填槽
   c. SendCustomEvent(hash) 触发 wrapper 方法
   d. wrapper 强转 type 后设置属性

[克隆重建阶段 - VRCPlayerObject]
1. CloneDetector.Start 触发
2. LocalizationShim.RenewPrefab(go, prefab, refs)
3. 遍历所有 UdonBehaviour 的 UsbTypeNameHeapKey
4. 用 type ID 索引调用对应 Clone* 方法
5. 替换 int[] 中的 ID → 新克隆的 int ID
```

### 三大配套子机制

| 子机制 | 作用 |
|--------|------|
| **God Shim 模式** | 单一 `LocalizationShim` 处理所有 LocalizeEvent / LocalizedString / Variable(Udon 限制下的不可避免选择) |
| **CloneDetector + RenewPrefab** | VRCPlayerObject 克隆后重建引用(`VRCPlayerObject` 克隆后是"新对象",原 int 引用失效) |
| **SmartLiteFormatter** | 重写 SmartFormat 最小子集(Udon 不能直接调用 SmartFormat 库) |

### 借鉴决策树

```
Q: 你的 Udon 项目是否需要包装 Unity 高层系统?
├── 是 → 借鉴 ULocalization 5 大模式
│   ├── 动态分派多方法 → Hash-Based Dispatch
│   ├── 索引访问多对象 → IID Object Identity
│   ├── UnityEvent 需传参 → Slot-Based Parameter Passing
│   ├── 多类型统一处理 → Code Generation + Type Erasure
│   └── 性能敏感且配置静态 → Build-Time vs Runtime Separation
└── 否(单类型简单逻辑) → 直接 SendCustomEvent
```

### 知识沉淀位置

- 5 个新 Pattern 文档(`memory/patterns/hash-based-dispatch.md` / `iid-object-identity.md` / `slot-parameter-passing.md` / `code-generation-type-erasure.md` / `build-time-vs-runtime-separation.md`)
- 1 个新 Source 文档(`memory/sources/ulocalization.md`)
- 5 大模式登记到 `memory/patterns/index.md` 24-28 号
- A8 案例研究型参考工程登记到 `memory/sources/open-source-projects.md`

> **📚 参考实现**
>
> 本节"ULocalization 沙箱适配模式"提炼自 HoshinoLabs ULocalization 项目(VRChat World 域,SDK 3.10.x)。
> 该项目是 VRChat 创作者生态中**唯一**将 Unity 完整系统(Localization) 适配到 Udon VM 的成熟方案,具有极高的"包装类项目"参考价值。
> 详细项目信息见:`memory/sources/ulocalization.md`

---

## Sardinal 通用消息系统(参考工程) ✅ (2026-06-20)

> **本节定位**:通过分析 HoshinoLabs Sardinal 项目提炼的"Udon 端类型安全 Pub/Sub 消息总线"设计模式,适用于"跨模块解耦通信 / 频道路由 / 基类继承事件 / 混合订阅"的所有场景
> **知识模式**:5 大 ULocalization 模式(精简版) + 3 个 Sardinal 独有模式(Channel / Inherited / Hybrid Subscription)

### 项目概况

Sardinal 是 HoshinoLabs 推出的**通用消息总线（Pub/Sub with parameters）**，专为 Unity C# 和 VRChat UdonSharp 设计。**不是包装某个 Unity 现有系统**(与同作者的 ULocalization 包装 Unity Localization 不同),而是**从零实现了一个完整的事件系统**。

| 指标 | 数值 | 与 ULocalization 对比 |
|------|------|---------------------|
| 总 .cs 文件 | 36 | ULocalization: 145 (Sardinal 精简 75%) |
| Shim 字段数 | **10** (`_0` ~ `_9`) | ULocalization: 27 (精简 60%) |
| Publish 重载数 | **16** (arg0 ~ arg15) | ULocalization: 3 槽位 (Sardinal 数量更多) |
| 依赖 | com.hoshinolabs.sardinject | ULocalization: Unity Localization + Sardinal + Sardinject |
| 复杂度 | ⭐⭐ 中 | ULocalization: ⭐⭐⭐⭐⭐ 高 |
| 同步模式 | `BehaviourSyncMode.None` | 相同 |

> **关键洞察**:Sardinal 是 ULocalization 的**精简 + 通用化**版本 —— 同样的 5 大沙箱适配模式 + Sardinject + God Shim,但**聚焦消息系统**而非本地化系统。

### 3 大 Sardinal 独有新模式

| 模式 | 解决的问题 | 关键机制 |
|------|------------|----------|
| **Channel-Based Pub/Sub Routing** ⭐S NEW | 同主题下多模块差异化响应 | `[Subscriber(Topic, "UI")]` 频道标记 + `signal.WithChannel("UI")` 过滤 + `object.Equals` 三态匹配 |
| **Inherited Subscriber** ⭐S NEW | 抽象基类需"统一事件处理"被所有子类自动继承 | Editor 端 `Concat(self.BaseType?.GetSubscriberSchemas())` 递归反射 + 编译期确定 |
| **Hybrid Static+Dynamic Subscription** ⭐S NEW | 混合场景常驻 + 动态生成对象 | Editor 端反射预注入静态订阅者(到 `_7`/`_9`) + 运行时 `Subscribe/Unsubscribe` API 动态追加 |

### 5 大与 ULocalization 共享的模式（精简版）

| 模式 | Sardinal 实现 | 与 ULocalization 差异 |
|------|--------------|---------------------|
| **Hash-Based Method Dispatch** | `MD5(Type.FullName)` 主题签名 | ULocalization hash **方法**;Sardinal hash **类型**(更精简) |
| **IID Object Identity** | `GetUdonTypeID()` + `long[] _2` | ULocalization 用 IID 跨 Build 引用;Sardinal 仅单 Build 内 |
| **Slot-Based Parameter Passing** | 16 个 `Publish` 重载 + `SetProgramVariable` | ULocalization 用 3 槽位;Sardinal 用 16 重载(boilerplate 多) |
| **Code Generation with Type Erasure** | 10 字段注入 | ULocalization 27 字段;Sardinal 精简 60% |
| **Build-Time vs Runtime Separation** | Editor 反射 → 10 字段 → Runtime O(1) 查表 | 模式相同,工程量更小 |

### 8 个关键学习点

1. **3 层分离**: Runtime (C#) + Runtime/Udon (Udon VM) + Editor/Udon (代码生成)
2. **Sardinject 强依赖**: `[Inject, SerializeField, HideInInspector]` 自动注入 10 字段
3. **MD5 主题 ID**: `MD5(Type.FullName) + "__" + ParamType1 + "__" + ParamType2` 构造完整签名
4. **16 重载绕开无参限制**: `SendCustomEvent` 不接受参数 → 16 个 `Publish(arg0~arg15)` 重载 + `SetProgramVariable` 传参
5. **频道路由三态过滤**: 发布有 channel + 订阅无 channel = **不触发**(Sardinal 隐含设计)
6. **基类继承**: `Concat(BaseType?.GetSubscriberSchemas())` 递归向上收集订阅者
7. **静态+动态双订阅**: `_7[i]++` + `Array.Copy` 扩容追加动态订阅者
8. **God Shim 模式**: 单一 `SardinalShim` 持有所有数据,与 ULocalization 一致

### 关键工程参数

| 参数 | 值 | 说明 |
|------|----|------|
| 主题 ID 长度 | 32 字符 | MD5 hex |
| 频道比较 | `object.Equals` | 值类型会装箱 |
| 冷启动反射 | 100~500ms | 100+ 类型时编辑器卡顿 |
| 内存占用 | 10~20 KB | 100 订阅者 |
| 动态 Subscribe 复杂度 | O(当前订阅数) | `Array.Copy` 扩容 |
| 静态注入数据来源 | Editor `BuildSubscriberData` | 扫描场景所有 UdonSharpBehaviour |

### 借鉴决策树

```
Q: 你的 Udon 项目需要"跨模块事件通信"吗?
├── 是 → 借鉴 Sardinal
│   ├── 同主题多模块差异化 → Channel Routing
│   ├── 抽象基类需统一事件 → Inherited Subscriber
│   ├── 混合场景常驻+动态 → Hybrid Subscription
│   └── 频繁事件触发(UI 反馈/成就) → Sardinal 整框架
└── 否(单模块内部) → 直接 SendCustomEvent
```

### 知识沉淀位置

- 1 个新 Source 文档(`memory/sources/sardinal.md`)
- 3 个新 Pattern 文档(`memory/patterns/channel-routing.md` / `inherited-subscriber.md` / `hybrid-subscription-modes.md`)
- 3 大新模式登记到 `memory/patterns/index.md` 29-31 号
- A9 案例研究型参考工程登记到 `memory/sources/open-source-projects.md`

> **📚 参考实现**
>
> 本节"Sardinal 通用消息系统"提炼自 HoshinoLabs Sardinal 项目(VRChat World 域,SDK 3.10.x)。
> 该项目是 VRChat 创作者生态中**最受欢迎的通用消息总线**,由 ULocalization 同作者开发,代码量精简 75% 但**额外贡献 3 个新模式**(频道/继承/双订阅)。
> 详细项目信息见:`memory/sources/sardinal.md`

---

---

## 核心工具与插件

### Avatar Shader 知识库（2026-06-11 整合）

#### Shader 用途分类

| 分类 | Shader | 核心优势 | 文档 |
|------|--------|----------|------|
| **🎭 Avatar 专用** | lilToon | 30%+ 市场、功能最全、预设丰富 | `memory/avatar/shader/liltoon/` |
| **🎭 Avatar 专用** | SCSS | 双阴影、UV服装切换零DrawCall、Matcap | `memory/avatar/shader/scss.md` |
| **🌍 World 专用** | ORL Shaders | 40+模块化、Configurable、VFX特效库 | `memory/avatar/shader/orl/` |
| **🌍 World 专用** | Filamented | Standard一键替换、Fresnel修复 | `memory/avatar/shader/filamented/` |
| **🔧 通用** | UnlitWF | Fur/Water/Grass/Gem专业效果、BRP+URP | `memory/avatar/shader/unlitwf/` |
| **📦 参考** | z3y/shaders | LTCGI/Bakery高级集成 | 待补充 |

#### Shader 总览对比

| Shader | 用途 | 市场占有率 | 渲染管线 | 活跃度 | 详细文档 |
|--------|------|-----------|----------|--------|----------|
| **lilToon** | 🎭 Avatar | 30%+ VRChat | BRP/URP/HDRP | ⭐⭐⭐⭐⭐ | `memory/avatar/shader/liltoon/` |
| **SCSS** | 🎭 Avatar | 较低 | BRP Only | ⭐⭐⭐ | `memory/avatar/shader/scss.md` |
| **ORL Shaders** | 🌍 World | 较高 | BRP | ⭐⭐⭐⭐ | `memory/avatar/shader/orl/` |
| **Filamented** | 🌍 World | 较小众 | BRP | ⭐⭐⭐ | `memory/avatar/shader/filamented/` |
| **UnlitWF** | 🔧 通用 | 较小众 | BRP/URP | ⭐⭐⭐⭐⭐ | `memory/avatar/shader/unlitwf/` |

#### Avatar 核心功能对比

| 功能 | lilToon | SCSS | UnlitWF | 说明 |
|------|---------|------|---------|------|
| **Toon 阴影** | ✅ 阶梯/平滑 | ✅ 双阴影系统 | ✅ 阶梯阴影 | SCSS 最灵活 |
| **Fur 毛发** | ✅ 噪声采样 | ❌ | ✅ Geometry | lilToon 跨平台 |
| **Water** | ⚠️ 基础 | ❌ | ✅ 波浪+焦散 | UnlitWF 最完整 |
| **Gem** | ⚠️ 折射 | ❌ | ✅ Flake 效果 | UnlitWF 独特 |
| **Grass** | ❌ | ❌ | ✅ 风力模拟 | UnlitWF 独有 |
| **PBR 支持** | ✅ 完整 | ❌ | ⚠️ 有限 | lilToon 最完善 |
| **Matcap** | ✅ | ✅ 多槽位 | ✅ 多种模式 | SCSS 最灵活 |
| **UV 服装切换** | ⚠️ 需第三方 | ✅ 零 Draw Call | ❌ | SCSS 独有优势 |

#### 平台支持对比

| 维度 | lilToon | SCSS | ORL | Filamented | UnlitWF |
|------|---------|------|-----|------------|---------|
| **BRP** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **URP** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Quest 支持** | ✅ 详细指南 | ✅ | ⚠️ 无分级 | ⚠️ | ✅ Mobile 变体 |
| **AudioLink** | ⚠️ 手动 | ✅ 每频段 | ✅ 5种模式 | ❌ | ❌ |
| **VRCLightVolumes** | ❌ | ❌ | ✅ | ✅ | ✅ v2.0.1+ |

#### 选择指南

| 场景 | 推荐 Shader | 原因 |
|------|------------|------|
| **VRChat Avatar 通用** | lilToon | 功能全面、文档完善、社区大 |
| **Cel Shader 优先** | SCSS | 双阴影系统、UV 服装切换 |
| **独特效果需求** | UnlitWF | Fur/Water/Grass/Gem 专业系统 |
| **World 环境构建** | ORL Shaders | 模块化、丰富的 PBR 功能 |
| **World VFX 特效** | ORL Shaders | Shield/Laser/Clouds 专属 |
| **Standard 升级** | Filamented | 零成本迁移、现代 PBR |
| **需要 LTCGI/AreaLit** | ORL / z3y/shaders | 内置支持 |

#### 互补使用建议

| 项目部分 | 推荐 Shader | 组合方式 |
|----------|-------------|----------|
| **Avatar 身体** | lilToon | 双阴影 + SSS + 优化 |
| **Avatar 服装** | SCSS 或 lilToon | UV 切换或模块化 |
| **Avatar 特效** | UnlitWF | Fur/Water/Gem 专业系统 |
| **World 环境** | ORL Standard | PBR + Parallax + Details |
| **World VFX** | ORL VFX | Shield + Laser + Clouds |

#### VCC 安装源

| Shader | 安装源 |
|--------|--------|
| lilToon | `https://lilxyzw.github.io/vpm-repos/vpm.json` |
| ORL Shaders | `https://orels1.github.io/orels-Unity-Shaders/index.json` |
| UnlitWF | `https://whiteflare.github.io/vpm-repos/docs/unlitwf` |

**详细文档索引**：`memory/avatar/shader/index.md`

### World 开发工具

| 工具 | 说明 |
|------|------|
| UdonSharp | VRChat World 编程语言（C# → Udon Assembly） |
| **UdonSharp 编译管线** | 四阶段编译（Setup → Roslyn → Bind → Emit）|
| **Bakery** | GPU 光照烘焙 | VRChat 光照贴图最优选择 |
| **VVMW(参考工程 + 推荐插件 A2/C16 双重身份)** | 视频播放器 | VRChat 多人同步视频播放方案 + 5 大模块 + 9 大集成 + 13 个 Releases + PC/Quest 跨平台 + 12+ 语言本地化 |
| **VRCTD(参考工程)** | 多机位导演系统 | 5 层网络同步体系参考 |
| **EasyQuestSwitch** | PC/Quest 平台切换 | VRChat 官方自动化平台切换工具 |
| **VRCLightVolumes** | 光照系统 | 体素化 Light Probes + Point Light Volumes（v2.0.0+）|
| VRCFury | ⚠️ Avatar 工具（不是 Shader/World 工具），仍维护但与 MA 重叠 → 详见 `avatar/vrcfury-reference.md` |

### Avatar 自动化

| 工具 | 说明 |
|------|------|
| Modular Avatar | ✅ 推荐（VPM 一键 + 文档完善 + NDMF 生态） |
| VRCFury | ⚠️ 仍活跃，但非 VPM 分发 + 与 MA 重叠 → 详见 `avatar/vrcfury-reference.md` |

### Avatar 优化工具 ✅ (2026-06-17)

| 工具 | 说明 | 文档 |
|------|------|------|
| **AAO: Avatar Optimizer** | 非破坏性自动优化（12 组件 + T&O + Animator Optimizer）| `memory/avatar/avatar-optimizer.md` |
| **Meshia Mesh Simplification** | Burst 高速减面（3 组件 + BlendShape 保留 + 防破洞）| `memory/avatar/meshia-mesh-simplification.md` |
| **lilAvatarUtils** | 性能检测（贴图/材质/动画/PB/光照等）| `memory/avatar/ndmf-tools.md` |
| **TexTransTool** | 材质 Atlas 化（合并贴图）| — |

> ⚠️ lilNDMFMeshSimplifier 已被官方废弃，请改用 Meshia

---

## VRChatSDK 层级 ✅ (2026-06-10)

> **定义**：VRChatSDK 是直接与 VRChat 服务器和玩家数据进行交互的 SDK，与 World、Avatar 位于同一阶层
> **定位**：外部应用 / Unity Editor 工具 / 第三方服务

### 与 UdonSharp 的区别

| 维度 | UdonSharp | VRChatSDK |
|------|-----------|-----------|
| **运行位置** | VRChat 游戏内 Udon VM | Unity Editor / 外部应用 |
| **通信对象** | VRChat 世界内其他玩家 | VRChat 服务器 |
| **功能范围** | 游戏逻辑、网络同步、UI 交互 | 用户数据、世界数据、文件管理、实时事件 |
| **延迟** | 游戏内实时（~50-200ms） | HTTP 请求（~100-500ms） |

### 数据源

| 来源 | 说明 |
|------|------|
| vrchat.community | 社区维护的 API 文档（非官方） |
| vrchat.hexdocs.pm | vrchat v1.20.0 (Elixir SDK) |

### VRChatSDK 模块概览

| 模块 | 功能 | 关键端点 |
|------|------|----------|
| **Authentication** | 登录/登出/2FA | getCurrentUser, login, logout, verifyAuthToken |
| **Users** | 用户查询/更新/标签 | getUser, searchUsers, updateUser, addTags |
| **Worlds** | 世界 CRUD/发布/搜索 | getWorld, searchWorlds, publishWorld |
| **Avatars** | Avatar CRUD/切换 | getAvatar, selectAvatar, searchAvatars |
| **Friends** | 好友列表/请求 | getFriends, friend, unfriend |
| **Notifications** | 通知管理 | getNotifications, acceptFriendRequest |
| **Favorites** | 收藏分组管理 | addFavorite, getFavorites |
| **Instances** | 实例查询/创建/关闭 | getInstance, createInstance, closeInstance |
| **Files** | 文件上传/下载/分析 | uploadImage, downloadFileVersion |
| **Groups** | 群组完整管理 | createGroup, joinGroup, getGroupMembers |
| **WebSocket** | 实时事件订阅 | friend-online, notification, user-update |

### 重要限制

| 限制 | 说明 |
|------|------|
| **会话限制** | 每次登录凭据认证算作一个会话，数量有限。生产环境务必保存并重用 auth cookie |
| **限流 (429)** | 必须实现指数退避（1s → 2s → 4s → ...） |
| **非官方 API** | VRChat 不官方支持此 API，端点可能随时变更 |
| **滥用后果** | 可能导致账户终止 |

### SDK 多语言支持

- JavaScript (vrchat.js) - npm: `npm install vrchat`
- Python, .NET, Dart, Java, Rust
- Elixir (vrchat v1.20.0)

---

## 最后更新

- 2026-06-20：**VizVid (VVMW) 升级 A2/C16 双重身份（VVMW 推荐插件索引入库）** — 完整执行 LuraSwitch2 双重身份方法论到第二个项目,跨 6 个文件受影响:(1) `memory/sources/vvmw.md` 新建 — 完整 A2 案例研究源文档(5 大模块 + 13 个 Releases + 9 大功能 + 9 大集成 + 4 种显示模式 + 8 模式沉淀 + 工程评价);(2) `memory/world/vvmw.md` 新建 — 完整 C16 工具使用指南(VPM 仓库 `https://xtlcdn.github.io/vpm/` + 5 大模块详解 + 9 大功能 + 4 种显示模式 + 9 大集成 + 13 个 Releases 演进 + 平台兼容性 + 9 项已知限制 + 与官方 `UdonSyncPlayer` 14 维度对比 + 7 步快速使用 + 5 步高级配置);(3) `memory/sources/open-source-projects.md` A2 行升级为 A2/C16 双重身份 + C 区从 15 扩展到 16 个(新增 C16 VizVid) + 双重身份特例说明;(4) `memory/hybrid/udon-world-plugins.md` 添加 VVMW 完整章节(10 维度推荐理由 + 14 维度对比表 + 5 大模块概览 + 适用/不适用场景 + 完整资源 + VPM 安装方式),收录数量从 1 扩展到 2;(5) `memory/hybrid/index.md` 子域表更新(2 个插件);(6) `memory/index.md` World Domain 添加 VVMW 链接 + `memory/_always-load.md` 文件速查表添加 VVMW 双条目(A2 源 + C16 工具) + `memory/FACT.md` 工具表 VVMW 行升级;**关键发现**:本项目将"双重身份方法论"扩展到视频播放器域,验证了方法的**普遍适用性** —— 不只 UI 组件库,多媒体同步系统也适用;**与 LuraSwitch2 双重身份方法论对齐**:A2 沉淀 8 个去项目化通用 Pattern(Manual Sync + Owner Authority + 时间同步算法 + 阈值同步 + 冷却期 + 双缓冲 + Performer + Strategy),C16 保留项目元数据 + VPM 仓库(创作者直接安装),形成"原理 + 实践"双层互补;**VVMW 是 VRChat 生态最受欢迎的多人视频播放器**(169 stars + 13 个 Releases + 9 大集成 + 12+ 语言),沉淀的"服务器时间锚点 + 阈值触发 + 延迟补偿 + Performer 模式"是 VRChat 多人音视频同步的**最完善实现**
- 2026-06-20：**Sardinal 通用消息系统案例入库(A9)** — 新建 1 个 Source 文档 + 3 个 Sardinal 独有新 Pattern,跨 6 个文件受影响:(1) `memory/sources/sardinal.md` 新建 — 完整项目档案(36 个 .cs + 10 字段 + 16 Publish 重载 + 8 关键学习点 + 与 ULocalization 对比表 + 知识提取记录);(2) `memory/patterns/channel-routing.md` 新建 — 频道路由完整模式(三态过滤表 + 命名规范 + 性能开销 + 与 UnityEvent 对比);(3) `memory/patterns/inherited-subscriber.md` 新建 — 基类订阅者自动继承模式(递归反射 + override 注意事项 + 5 条关键约束);(4) `memory/patterns/hybrid-subscription-modes.md` 新建 — 静态+动态双订阅模式(Subscribe/Unsubscribe O(n) 扩容 + 内存泄漏防护 + OnEnable/OnDisable 配对);(5) `memory/patterns/index.md` 模式从 28 扩展到 31 + 决策树新增第 7 节(Pub/Sub 选择树)+ 速查表追加 3 行;(6) `memory/sources/open-source-projects.md` A9 行新增 + C 区保持不变;`memory/sources/index.md` 注册新源 + 沉淀内容摘要;`memory/index.md` Sources Domain 添加 Sardinal 链接;`memory/_always-load.md` 文件速查表添加 3 条 Sardinal 模式路由;`memory/FACT.md` 新增 § Sardinal 案例研究章节(接在 ULocalization 之后)+ 时间戳条目;**关键发现**:Sardinal 是同作者 ULocalization 的**精简 + 通用化版本**(36 .cs vs 145 .cs;10 字段 vs 27 字段;16 重载 vs 3 槽位),**共享 5 大 ULocalization 沙箱适配模式但不重复沉淀**;**额外贡献 3 个新模式**:①Channel Routing 解决"同主题多模块差异化响应"(三态过滤:发布有/订阅有/都没有 5 种组合)②Inherited Subscriber 解决"抽象基类需统一事件"(Editor 端 `Concat(BaseType?.GetSubscriberSchemas())` 递归)③Hybrid Subscription 解决"混合场景常驻+动态对象"(Editor 反射静态注入 + 运行时 Subscribe API 动态追加 + `_7[i]++` 扩容);**与 ULocalization 互补**:ULocalization 沉淀"包装 Unity 高层系统"的 5 大模式,Sardinal 沉淀"通用消息系统"的 3 大独有模式 + 同思想精简版;**填补知识库"跨模块解耦通信"场景空白** — 此前所有模式都聚焦"网络同步/UI 交互/音频控制"等特定领域,Sardinal 是第一个"通用 Pub/Sub 基础设施"案例研究
- 2026-06-20：**TLP UdonVoiceUtils 推荐插件索引入库（C16 双重身份 + 推荐分类新建）** — UVU 升级为 A7 案例研究 + C16 工具使用指南 双重身份（参考 LuraSwitch2 的 A6/C15 双重身份方法论），跨 3 个文件受影响：(1) `memory/hybrid/udon-world-plugins.md` **新建分类** — "推荐 Udon 世界插件"索引（创作者安装 / 玩家识别），收录 UVU 作为首个推荐插件，含仓库/VPM/许可证/推荐理由/适用场景/与官方 `mute-others` 对比表（10 维度）/安装方式/评估标准/与其他知识库关系；(2) `memory/hybrid/index.md` 核心文档表格新增"udon-world-plugins.md ⭐NEW"行 + 子域表新增"推荐 Udon 世界插件"行（2026-06-20 ✅ 已完成）；(3) `memory/world/examples/mute-others.md` 添加 "⭐ 工业级升级方案: TLP UdonVoiceUtils" 章节（含 6 维度对比表 + 完整资源链接），让官方教学示例指向 UVU 工业级方案；**关键发现**：**"推荐插件分类" 是知识库的新维度** —— `sources/open-source-projects.md`（案例研究）≠ `hybrid/udon-world-plugins.md`（推荐插件），案例研究提炼"去项目化模式"（让 Agent 理解原理），推荐插件保留"项目元数据 + VPM 链接"（让创作者直接拿来用），**两个分类互不冲突但需明确边界**：晋升条件 = 工具稳定性 + 社区反馈 + 文档完整度 + 长期维护承诺（已在 `udon-world-plugins.md` 明确列出 7 条评估标准）；**与 LuraSwitch2 双重身份方法论一致**：A7 沉淀 10 个 ⭐U 通用 Pattern（理解原理），C16 保留项目元数据 + VPM 仓库（直接安装），形成"原理 + 实践"双层互补
- 2026-06-20：**HoshinoLabs ULocalization 案例研究入库** — 新建 5 个 Pattern 文档 + 1 个 Source 文档,跨 6 个文件受影响:(1) `memory/sources/ulocalization.md` 新建 — 完整项目档案(145 个 .cs + God Shim 架构 + 27 字段注入 + 500+ 哈希方法 + 16 IVariable 类型 + 11 大设计问题 + 工程评价);(2) `memory/patterns/hash-based-dispatch.md` 新建 — 哈希方法分派模式(MD5 Type+Method + 预生成 500+ wrapper + `SendCustomEvent(hash)`);(3) `memory/patterns/iid-object-identity.md` 新建 — 整数身份映射模式(Editor 端 `IID.GenerateId` + int[] 数组 + RenewPrefab 重建);(4) `memory/patterns/slot-parameter-passing.md` 新建 — 槽位参数传递模式(3 object 字段 `_l_t`/`_l_p`/`_l_a` 绕开无参限制);(5) `memory/patterns/code-generation-type-erasure.md` 新建 — 代码生成 + 类型擦除模式(Type.FullName MD5 + switch case + `object[2]` 元组);(6) `memory/patterns/build-time-vs-runtime-separation.md` 新建 — 构建时与运行时分离模式(Editor 端反射 LINQ → 注入 27 字段 → Runtime O(1) 查表);**关键发现**:ULocalization 是一个"**Udon 沙箱适配典范**",与 LuraSwitch2/UVU 不同,该项目核心问题不是"多人交互/同步"而是"如何在 Udon VM 限制下包装 Unity 复杂系统(Localization)"。5 大模式可作为"任何想把 Unity 高层 API 包装到 Udon"的模板: ①**Hash-Based Method Dispatch** = 绕开无委托(动态分派 100+ 目标类型方法) ②**IID Object Identity** = 绕开无 Dictionary(用 int 索引代替对象引用) ③**Slot-Based Parameter Passing** = 绕开无参数 SendCustomEvent(用 object 槽位传参) ④**Code Generation with Type Erasure** = 绕开无泛型(用 MD5 type ID + switch case) ⑤**Build-Time vs Runtime Separation** = 绕开无 Editor API(预处理 + 27 字段注入 + Cleanup);**借鉴价值**:5 个模式都是"Udon VM 沙箱适配"的方法论范本,适用于"包装 Unity 高层系统"的场景(序列化/输入/动画/物理/AI 等),填补了此前知识库"如何在 Udon 写 Adapter"的空白
- 2026-06-20：**TLP UdonVoiceUtils (UVU) 案例研究入库** — 新建 1 个 Source 文档 + 1 个模式选择决策树,跨 4 个文件受影响:(1) `memory/sources/udonvoiceutils.md` 新建 — 完整项目档案(35 个 .cs + 8 层职责 + 2 同步模型 + 10 大难题 + 工程评价);(2) `memory/sources/open-source-projects.md` 案例研究型参考工程从 6 个扩展到 7 个 (新增 A7 UVU,定位"音频/语音控制领域的最佳实践");(3) `memory/sources/index.md` 注册新源 + 沉淀内容摘要;(4) `memory/patterns/index.md` 模式从 13 扩展到 23 (新增 10 个 UVU 模式,后缀 `⭐U` 区分来源: dual-copy-sync / execution-order-chain / strategy-pattern-udon / object-pool-udon / priority-arbitration / master-ownership-defense / gizmos-relationship / trigger-event-fallback / compile-time-debug-strip / auto-scripting-symbol);**关键发现**:UVU 是一个"工程深度极高"的项目,5 个层次创新 —— ①**架构层**采用 MVC + Strategy + ExecutionOrder 链,8 层职责清晰分离 ②**同步层**采用 Dual-Copy 模型(`[UdonSynced] _xxx` + 本地 `xxx`)避免热路径访问慢变量 ③**冲突层**采用优先级仲裁 + PrivacyChannel 分组,支持多 Override 重叠 ④**稳定性层**采用 Master 所有权三层防御(OnPlayerJoined / OnOwnershipTransfer / 周期检查) ⑤**性能层**采用 `Physics.RaycastNonAlloc` + 零分配 `PlayerAudioOverrideList.GetMaxPriority` + `PlayerUpdateRate` 节流,与传统 Udon 教程形成"工程化深度"互补;**待沉淀**:8 大难题与解决方案的 FAIL 案例已识别但**未单独建文档**(原计划在 `memory/reviews/common-failures.md` 追加 FAIL-33 ~ FAIL-40),**本次仅入 Source 文档**,FAIL 案例沉淀留待后续 session
- 2026-06-20：**QuickBrown LuraSwitch2 案例研究入库** — 新建 6 个 Pattern 文档 + 1 个 Source 文档 + 4 个 FAIL 案例，跨 6 个文件受影响：(1) `memory/sources/quickbrown-luraswitch2.md` 新建 — 完整项目档案(39 个 .cs + 4 层职责 + 3 同步模式 + 12 大难题 + 工程评价);(2) `memory/patterns/master-follower-syncer.md` 新建 — Master-Follower Syncer 模式(SwitchSyncer 提炼,节流窗口 + Owner 抢占 + 双标志回声排除);(3) `memory/patterns/exclusive-control-selector.md` 新建 — 互斥选择器模式(集中 synced + 强制子 syncMode None + 1 帧延迟初始化);(4) `memory/patterns/soft-detent-interpolation.md` 新建 — 软吸附插值模式(SmoothStep 软磁力公式 + 完全吸附阈值);(5) `memory/patterns/fade-then-snap.md` 新建 — 淡入淡出移动模式(3 阶段隐藏移动 + FadeInStep 重入 token);(6) `memory/patterns/editor-preview-component.md` 新建 — Editor 预览组件模式([ExecuteAlways] MonoBehaviour + TrackingState 变更检测);(7) `memory/patterns/material-propertyblock-safe-update.md` 新建 — 共享材质安全更新模式(MPB vs sharedMaterial vs material 4 种方式对比);(8) `memory/reviews/common-failures.md` 追加 4 个 FAIL 案例(FAIL-29 Selector 时序错乱 / FAIL-30 滑块插值自我回声 / FAIL-31 Editor 反射访问私有字段 / FAIL-32 SendCustomEventDelayedFrames 在低帧率不可靠);(9) `memory/sources/open-source-projects.md` 案例研究型参考工程从 5 个扩展到 6 个 (新增 A6 QuickBrown);(10) `memory/sources/index.md` 注册新源;(11) `memory/patterns/index.md` 模式从 7 扩展到 13 + 选择决策树 + 速查表更新;**关键发现**:LuraSwitch2 是一个"超高质量 Udon 实战范本",4 层职责划分 × 3 种同步模式可插拔组合,提炼的 6 个 Pattern 都是非典型但工程价值高的"实战模式",与传统 Udon 教程形成互补
- 2026-06-20：**Lura's Switch 工具使用指南入库（C15 双重身份）** — 新建 `memory/world/luraswitch2.md` 工具使用文档 + 升级 A6 案例研究为双重身份（A6 案例研究 + C15 工具使用指南），跨 4 个文件受影响：(1) `memory/world/luraswitch2.md` 新建 — 工具使用指南（BOOTH 下载 https://booth.pm/en/items/1969082 + UV License 免费商用 + 9 种开关 Prefab 一览 + 3 种同步模式说明 + 多种入口 + 平台兼容性 + 版本演进 + 已知限制 + 安装教程 VCC/手动双路径 + 关联知识库索引）; (2) `memory/sources/quickbrown-luraswitch2.md` 顶部添加 BOOTH/UV License 元数据 + 双重身份说明（A6 案例研究 + C15 工具使用指南互补）; (3) `memory/sources/open-source-projects.md` A6 行标记为 **A6/C15 双重身份** + C 区从 14 扩展到 15 个（新增 C15 Lura's Switch）; (4) `memory/sources/index.md` / `memory/index.md` / `memory/_always-load.md` 全部添加工具路径;**关键发现**: 一个开源项目可以同时是"模式来源"和"可推荐工具"——A6 沉淀 6 个去项目化通用 Pattern（让 Agent "理解原理"），C15 保留项目元数据 + BOOTH 链接（让创作者"直接拿来用"），两层互补不冲突
- 2026-06-20：**Editor 脚本与构建约束入库** — 在 `## ⚠️ 核心约束` 新增 `### Editor 脚本与构建` 子节，记录 Unity 通用规则：`using UnityEditor.*` 命名空间的脚本必须放在 `Editor` 文件夹内（或 asmdef 限制 Include Platforms = Editor），原因 = 目标平台编译不包含 `UnityEditor` 程序集；列出会触发该问题的常见场景（CustomEditor / OnDrawGizmos / IPreprocessBuildWithReport / AssetPostprocessor）+ 易错点（以为脚本必须挂 GameObject 上才能编译 → 实际由文件夹路径决定）；引用 Unity 官方 Special Folders 文档
- 2026-06-17：**VRCFury 完整参考深度更新** — 大幅扩充 `memory/avatar/vrcfury-reference.md`（225 行 → 460+ 行，16 节），从官方文档 + PR#238 + 组件页面全面提取：**核心优化技术** ①Parameter Compressor（16 bit 指针式浮点同步，253→125 bit 实测）②Direct Tree Optimizer（非冲突层合并为单个 Direct Blend Tree）③Blendshape Optimizer（烘焙非动画 BlendShape 减 VRAM）④Fix Write Defaults（自动对齐 WD 设置）；**完整组件清单**（6 主要 + 4 优化 + 17 功能 + SPS）；**Actions 系统**（16 种 Action 类型）；**自动修复 60+ 项**（Avatar/VRCSDK/Unity 三类）；**优化场景对比矩阵**（新增 d4rk 列，11 维度 × 5 工具）；**Quest 兼容性规则**；**Toggle 详细功能**（14 选项 + 2 种 Toggle Sets）；**Full Controller 详细功能**（路径重写 + 参数命名空间 + 平滑参数）；**常见故障排除**（6 常见问题解决方案）；同步更新 `index.md`（描述更新为完整参考）+ `FACT.md`（优先级调整条目更新）；3 个文件受影响；**关键发现**：VRCFury 的 Parameter Compressor 使用 Pointer-Based Float Sync 技术（PR#238 sentfromspacevr），是目前 VRChat Avatar 生态中最强的参数压缩方案（16 bit 同步任意数量 Float）
- 2026-06-17：**MA2BT (Modular Avatar to BlendTree) 完整知识库** — 新建 `memory/avatar/ma2bt.md`（~530 行,16 节），系统化分析 Null-K/MA2BT v2.0.2（Unlicense/13 commits/7 stars）；涵盖：①工具定位（"将 MA 响应式层压缩为 Direct BlendTree,减少 FX 层数"）②工作原理（NDMF `BuildPhase.Optimizing` + `seq.AfterPlugin("nadena.dev.modular-avatar")` + 复用同名 `MA_To_BlendTree_Layer` 注入策略 + 根直混参数 `zhz/1` 硬编码）③系统要求（Unity 2022.3+/MA ≥1.10/NDMF ≥1.4/仅 VRChat Avatar 3.0）④安装方式（VPM `https://null-k.github.io/vpm-listing/index`）⑤使用方法（Inspector 三选项：Compact Mode/Multi-State Layers/Scan All Layers）⑥7 种可转换条件 + 4 种支持 Condition Mode（Greater/Less/If/IfNot;**不支持 Equals/NotEqual**）⑦20+ 跳过原因完整枚举（层结构/条件参数/转换三大类）⑧与其他优化器关系（与 AAO 互补,在 MA 之后 + AAO Animator Optimizer 之前）⑨功能限制与已知边界 ⑩反馈渠道（中文 QQ 群 1047423396 / EN/JP GitHub Issues）⑪Release 历史 5 个版本 ⑫架构与依赖（核心插件注册代码 + 4 个数据模型 + 核心常量 + asmdef 引用）⑬鸣谢（丨丿・丶乛 灵感 + 浊鸷 原始作者）⑭6 个 cross-reference ⑮16 节速查表;同步更新 `index.md`（核心文档 + VPM 速查）、`ndmf-tools.md`（工具一览 + NDMF 内部执行顺序新增第 2 步 + VPM 导入清单）、`_always-load.md`（文件速查表补充 8 条 Avatar 工具路由）;5 个文件受影响;**关键发现**:MA2BT 是 MA 响应式层 → Direct BlendTree 的**专用压缩器**,与 AAO 处理 Mesh/Bone/PhysBone 互补,是 Animator 层数优化的最直接手段
- 2026-06-17：**AAO: Avatar Optimizer 完整知识库** — 新建 `memory/avatar/avatar-optimizer.md`（~450 行），系统化分析 anatawa12/AvatarOptimizer v1.9.x；涵盖 12 个组件完整文档（Trace And Optimize / Merge Skinned Mesh / Freeze BlendShape / Remove Mesh By BlendShape/Mask/Box/UV Tile / Merge PhysBone / Merge Bone / Clear Endpoint Position / Merge Material / Max Texture Size）、组件分类体系（Avatar Global / Source Edit / Modifying Edit）、Animator Optimizer（AnyState→Entry-Exit→BlendTree 级联转换）、开发者 API（Component API / Shader Information API / Asset Description）、优化方向矩阵（9 维度 × 7 指标）、性能影响矩阵、优化工作流推荐顺序、与 MA/lilAvatarUtils/TexTransTool/Meshia 协作关系、OSC 兼容性解决方案、常见问题 FAQ；FACT.md 新增 "Avatar 优化工具" 小节（4 工具对比）；同步更新 `index.md`、`optimization-guide.md` 添加交叉引用；4 个文件受影响
- 2026-06-17：**Modular Avatar 官方教程深度精读** — 新建 `memory/avatar/modular-avatar-tutorials-detailed.md`(789 行),涵盖 6 个教程的官方原文精读 + 玩家视角操作分解(每步 1 动作) + 验证步骤表 + 易错点表 + 教学衔接路径;修正主文档 `modular-avatar.md` 教程 6 步骤(9→6 步,新增三个关键概念: Internal Checkbox / MA Parameters 位置约束 / "也加 Animator 组件" 目的);主文档顶部速查表增加 3 个新条目(Default 复选框 / Overdraw / Internal);新增 §4.6 "MA 教程中可提取的玩家友好设计模式"(5 种) + §4.7 教程衔接路径;教学法文档追加 §BB-§FF(MA 教程的 5 大玩家友好设计 + 句式清单 + 反面教材 + 应用模板 + 来源配套);关键 takeaway: 教程 3 的"Default 复选框预览"是教学金矿(不用进 Play 模式即可验证),教程 5 的"Overdraw 调试视图"是可视化诊断,教程 6 的"Internal Checkbox"是 99% 情况的默认;同步更新 `index.md` 和 `FACT.md` 注册新文档;详见 journal/sessions/2026-06-16
- 2026-06-17：**Avatar 改模教学法 & 问题诊断框架** — 新建 `memory/avatar/teaching-methodology.md`，基于 vrnavi.jp 教程（dressup-ma + modular-avatar-komono）分析教学法/玩家常见踩坑/问题分类/术语口语化翻译/5 步回答流程；目标：让 Agent 给玩家 Avatar 改模提问时能给出"有意义的问题解决方案"；同步更新 `memory/avatar/index.md` 注册新文档
- 2026-06-17：**vrcmaster.com 教程风格分析（第二来源）** — 追加到 `teaching-methodology.md` 第二部分；从 vrcmaster.com 下载 10 篇相关文章（主页 avatar-clothing-guide + 9 篇相关），分发给 4 个 subagent 并行提炼；新增原则 11-22（陪伴语气、emoji 标题、三段式拆概念、幼儿园比喻、戏剧化开场、心理安抚、跨文章互链、严守版本号、固定模板、反直觉诚实、版权声明）；与 vrnavi 形成"深度系列型 vs 工具链普及型"互补；teaching-methodology.md 从 264 行扩展到 505 行；同步更新 `index.md` 标注 22 条原则 + 双源
- 2026-06-17：**Kuriko HackMD 教程分析（第三来源）** — 追加到 `teaching-methodology.md` 第三部分；从 Kuriko 5.5 万字长文（9 工具 + 5 大类优化技术）分发给 6 个 subagent 并行分章节分析；**重要发现**：技术内容**早已入库**（2026-06-05 ndmf-tools/optimization-guide/performance-rank），本次学习**不产生新**技术知识，价值在 **第三种教学风格**；新增原则 23-34（懒人包置顶/代價-好處框架/挑战者机制/传送门/数字具象化/惨剧图/社区致谢/工具维护标注/作者名片/复制安全网/备份 GIF 置顶/未实测免责）；teaching-methodology.md 扩展到 850+ 行，形成"**vrnavi 深度系列 + vrcmaster 工具链普及 + Kuriko 工程实践百科**"三源互补；同步建立三源融合的"综合使用指南"（M 节）与升级版自我检查清单（O 节）；详见 `journal/sessions/2026-06-17_session_kuriko-tutorial-learning.md`
- 2026-06-17：**MA Samples 实战案例学习（Fingerpen + Clap 拆解）** — 学习官方 Samples 页面（modular-avatar.nadena.dev/docs/samples），在 `modular-avatar.md` 新增 §9.6 章节（6 个子节：§9.6.1 是什么 / §9.6.2 Fingerpen 拆解 / §9.6.3 Clap 拆解 / §9.6.4 教学应用指南 / §9.6.5 元学习价值 / §9.6.6 关联知识），完整覆盖 2 个示范 Prefab 的内部结构 + 教学应用 + 元方法论；§11 教学决策树新增 2 条 Samples 入口（"装了多个小组件菜单打架" / "想看一个 MA 小组件内部什么样"）；在 `teaching-methodology.md` 新增 §V.Samples "Samples 拆解教学法"，3 条新教学原则（43-45："用现成 Prefab 拆解 > 从零搭建" / "递进式 Sample > 并列式" / "展示完成效果 + 制作过程 都要教"）；**关键发现**：Samples 是"递进式"而非"并列式"（Clap 在 Fingerpen 之上 +1 知识点），官方文档三层结构（Samples → Tutorials → Reference）应作为教学文档组织范本；§0 速查表新增 "想看一个 MA 小组件内部什么样" 入口；详见 `journal/entries/2026-06-17_ma-samples-study`
- 2026-06-17：**TexTransTool (TTT) 完整知识库入库** — 新建 `memory/avatar/tex-trans-tool.md`(15 核心组件 + AtlasTexture 完整参数表 + Quest 适配 + 与 AAO 协作 + v0.10.0/v1.0.0 破坏性变更 + 故障排查)；**关键认知修正**：TTT 可压**材质球** + **VRAM**，**不直接压材质槽**（Material Slot），想真正减少 Material Slot → 必须配合 AvatarOptimizer.MergeSkinnedMesh；同步更新 `ndmf-tools.md`(TexTransTool 行加链接) + `optimization-guide.md`(Atlas 化章节扩充：能力边界 + Quest 适配 + AAO 协作 + 故障排查) + `index.md`(注册新文档)；参考源：ReinaS-64892/TexTransTool GitHub (142 Stars / 3360 commits / v1.0.1) + ttt.rs64.net 官方文档 + CHANGELOG.md 完整版本历史
- 2026-06-17：**MA "Dealing with problems" 章节精读** — 学习官方 problems 章节（仅 2 个子页面：主页 1 个常见问题 + install 1 个常见问题）；**核心发现**：内容少但**设计哲学丰富**——MA 把"问题诊断责任"分散到 6 个地方（Dealing with problems / Component Reference / General Behavior / FAQ / GitHub Issues / Discord），这是"分布式问题诊断"设计；扩充 `modular-avatar.md` §8 节（从 4 子节扩展到 8 子节）：§8.0 官方问题诊断设计哲学 / §8.1 错误窗口（Console vs MA 错误窗口对比表 + 自动弹出/手动重开 + 教学要点）/ §8.2 安装问题（VCC "Failed to add Repo" 已知 bug + 3 步精确操作 + 教学话术）/ §8.3 "Nothing is getting processed at all"（Apply On Play 路径精确到字段）/ §8.4 错误报告更新机制（自动 vs 需重新 Build + 3 种重新 Build 方法）/ §8.5 常见问题诊断表（从 9 行扩展到 14 行，新增 5 条 problems 章节问题）/ §8.6 5 步问题诊断法（升级版）/ §8.7 教学风格速记（8 条写作原则 + 5 条写作禁忌）；§0 速查表新增 4 行（装上没反应/错误窗口打不开/改完错误不消失/VCC Failed to add Repo）；在 `teaching-methodology.md` 追加"第七部分:问题诊断教学法" §MM-PP（分布式问题诊断哲学 + 三段式模式 + 8 条写作原则 + 5 步问题诊断法 + 3 个回答模板示例 NN.1-NN.3 + 7 条写作禁忌 + 9 项自检表）；**教学价值**：为 Agent 回答"Avatar 改模问题"提供标准化模板（症状→原因→3 步修复），以及"什么时候自己答、什么时候引导玩家去 Discord/GitHub"的边界判断；同步更新 `index.md`
- 2026-06-17：**Meshia Mesh Simplification 完整技术入库** — 新建 `memory/avatar/meshia-mesh-simplification.md`（550 行），系统化分析 RamType0/Meshia.MeshSimplification v3.2.0；涵盖 3 个核心组件（MeshSimplifier C# API / MeshiaMeshSimplifier NDMF / MeshiaCascadingAvatarMeshSimplifier）、4 阶段 Job 流水线、完整 API 参考（`MeshSimplificationTarget` 6 种 Kind + `MeshSimplifierOptions` 9 字段）、BlendShape 保留机制、与 lilNDMFMeshSimplifier/Mantis/OverallNDMFMeshSimplifier 对比、3 个关键修复选项（PreserveBorderEdges / UseBarycentricCoordinateInterpolation / PreserveSurfaceCurvature）、v3.1 新功能（按骨保留 Border Edges）、NDMF 工具链协同顺序、与 AAO 互补关系、VPM 安装、4 张速查卡片；**关键事实修正**：lilNDMFMeshSimplifier 已被官方废弃（README 明确指向 Meshia），更新 `ndmf-tools.md` 减面对比表 + 移除辅助工具表 + 导入清单、更新 `optimization-guide.md` 减面章节 + 速查懒人包、更新 `index.md` 速查懒人包 + VPM 链接 + 文档注册；7 个文件受影响
- 2026-06-15：**知识库二次审计与修复** — 二次审计发现 1 个 broken reference(`liltoon/outline.md` 缺失,被 7 个文件引用) + 4 个缺失域索引(vrchatsdk/platform/misc/references),共创建 5 个新文件,更新 2 个旧路径引用,更新 `index.md` 和 `_always-load.md`,更新 `FACT.md`;8 个文件受影响;详见 `journal/sessions/2026-06-15_session_second-audit.md`
- 2026-06-15：**知识库全面审计与重构** — 创建 5 个缺失 index.md（api/rules/patterns/sources/reviews），合并 3 个重复内容到权威位置（vrc-graphics/udonsharp-compilation/data-containers），清理空 journal 子目录（添加 .gitkeep）；11 个文件受影响；详见 `journal/sessions/2026-06-15_session_knowledge-base-audit-refactor.md`
- 2026-06-15：**Scene Components 子分类知识库** — 新建 `memory/world/scene-components/`,10 个 .md 文件(1 索引 + 9 子页),覆盖 VRChat World 9 个核心 Scene Components:TextMesh Pro、VRC_AvatarPedestal、VRC_CameraDolly、VRC_MirrorReflection、VRCObjectSync、VRC_PortalMarker、VRCSceneDescriptor、VRCStation、VRCEnablePersistence;**关键事实**:VRCSceneDescriptor 缺失 World 无法加载、VRCObjectSync 与 Manual Sync 选型决策、PhysBone/Contact 1024 上限、VRC_MirrorReflection Quest 性能警告、VRCStation 事件触发位置、持久化 100KB 限制;与 `patterns/` 添加 4 处 cross-reference
- 2026-06-15：**Obstacle Course(World Jam 2)知识库** — 新建 `world/examples/obstacle-course/`,6 个 .md 文件(index + build-from-demo-parts + build-from-custom-parts + uoc-flythrough + uoc-how-stuff-works + uoc-window),涵盖 Time Trial 模式完整参考实现(13+ Udon 程序、OnPlayerDataEnter 桥接模式、VRCObjectPool 动态重建、Toolkit Editor 窗口、PowerUp/Hazard 系统);**关键工程参数**:Number of Players = N → SDK Publish Capacity = N/2
- 2026-06-15：**Udon Example Scene 知识库** — 新建 `world/examples/udon-example-scene/`,6 个 .md 文件(14.5K index + 5 个子页面),涵盖 13+ Prefab 详解、5 种同步模式范式、5 个专项子页面(Avatar Scaling / Player Mod Setter / Pen System / Video Sync / World Audio)
- 2026-06-15：**Udon Node Graph 知识库** — 新建 `memory/world/udon/graph/`,6 个 .md 文件(40.7K),涵盖 Interface/Flow/创建节点(快捷键 `1/2/3/4/+/=/b/shift+b/C+click/Shift+F`)/Event 节点(Interact/Pickup/Player/Video 完整列表 + `OnPlayerSuspendChanged` 等设备挂起事件)/Graph 元素(Groups/Comments/Noodles)/5 种搜索方式(Quick/Full/Search Bar/Focused/Noodle Drop)/特殊节点(Block/Branch/For/While/Get-Set Variable/Get-Set ProgramVariable/SendCustomEvent 家族)/类型引用节点(VRCPickup/VRCMirrorReflection/VRCStation/VRCPlayerApi/VRCInputMethod 19 种枚举值)
- 2026-06-11：**知识库结构整理** — 删除非标准目录（unity/cases/pending/reference），移动文件到正确位置（avatar-modding-guide/light-baking-guide/occlusion-culling-guide/reflection-probes/vrc-light-volumes），更新 index.md/_always-load.md/FACT.md 索引

- 2026-06-11：**UnlitWF Shader Suite 知识库** — 新建 `avatar/shader/unlitwf/`，分析 whiteflare/Unlit_WF_ShaderSuite（Unlit 扩展专业效果 Shader/298 Stars/102 Releases），drawing struct 效果管线、4种透明度模式、5大专业效果系统（FakeFur/Water/Grass/Gem/Particle），与 lilToon/SCSS/ORL 对比
- 2026-06-11：**ORL Shaders 知识库** — 新建 `avatar/shader/orl/`（4个文档），分析 orels Unity Shaders v7.2.0（40+ Shader/Configurable模块化/AudioLink内置/VFX特效库），与 lilToon/SCSS/VRCLightVolumes 对比
- 2026-06-11：**SCSS 知识库** — 新建 `avatar/shader/scss.md`，完整分析 Silent's Cel Shading Shader（双阴影系统/Lightramp/Crosstone/UV服装切换/Matcap/AudioLink/Outline VR优化），与 lilToon 对比
- 2026-06-11：**Filamented 知识库** — 新建 `avatar/shader/filamented/`（4个文档），分析 Google Filament PBR 着色器（Fresnel 修复/Specular Occlusion/VRC Light Volumes），与 z3y/shaders/GeneLit 对比
- 2026-06-11：**VRCLightVolumes 知识库更新** — 补充 v2.0.0 Point Light Volumes 系统（128 动态光源、LUT/Cookie/Cubemap、阴影遮罩）、完整 UdonSharp API、Shader 集成接口、兼容 Shaders 列表（16+）
- 2026-06-11：**Journal 会话记忆目录** — 新建 `memory/journal/` 层级，非知识类记忆（会话记录、代码审查、问题追踪、临时草稿）独立存储，定期清理防止污染知识库
- 2026-06-10：**知识本地化完成** — VRChatSDK 18 个文档已复制到 `memory/vrchatsdk/`，creator-docs 对比记录已复制到 `memory/references/`，所有外部路径引用已移除
- 2026-06-10：**UdonSharp 运行时系统** — 新建 `api/udonsharp-runtime.md`，含 GetProgramVariable/SetProgramVariable、类型识别系统、FieldChangeCallback、代理系统、构建时组件处理
- 2026-06-10：**UdonSharp 编译管线** — 新建 `world/udonsharp-compilation.md`，四阶段编译流程（Setup → Roslyn → Bind → Emit）
- 2026-06-10：**UdonSyncMode 插值模式** — 更新 `api/networking.md`，补充 None/Linear/Smooth/NotSynced 模式说明
- 2026-06-10：**VPM Package Template 知识库** — VRChat 官方 Package 开发模板，含 GitHub Actions CI/CD 自动化、VPM CLI 命令、Repo Listing 格式、Package Maker Tool 迁移流程
- 2026-06-10：**VRChatSDK 知识库** — 新建层级，HTTP API 文档入库（18个文件），包含 Authentication/Users/Worlds/Avatars/Friends/Notifications/Favorites/Instances/Files/Groups/WebSocket/Models/Tags
- 2026-06-10：**EasyQuestSwitch 知识库** — VRChat 官方 PC/Quest 平台切换工具，含类型处理器架构、SharedField 系统、Bakery 集成、自定义类型扩展
- 2026-06-09：**带参网络同步 (NetworkCallable)** — 语法、必须条件、对比表格
- 2026-06-09：**Avatar/World Animator 知识修正** — 删除学习方法文件，核心知识整合到 playable-layers.md + animator-system.md（参数驱动 vs 逻辑驱动）
- 2026-06-06：**多机位导演系统网络同步架构(参考工程)** 入库(7 种新设计模式，排除 SafeMod)
- 2026-06-06：**视频播放器时间同步算法模式(参考工程)** 入库(Manual Sync + Owner Authority + 时间同步算法)
- 2026-06-06：**音频同步系统架构(参考工程)** + 5 种核心设计模式 入库
- 2026-06-05：VRC Constraints + Playable Layers + World 性能优化 入库
- 2026-06-05：BRP 强制约束入库（最高优先级）
- 2026-06-05：Bakery GPU Lightmapper 知识库入库

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