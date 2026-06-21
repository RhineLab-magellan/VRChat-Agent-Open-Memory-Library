# Lura's Switch（LuraSwitch2）— Udon 通用开关套件

> 来源: https://booth.pm/en/items/1969082
> 作者: QuickBrown Design Studio (https://lura.booth.pm/)
> 版本: v3.00 (Persistence) | v2.02 (VCC) | v1.2 (SDK2)
> 价格: **免费**
> 许可协议: **UV License**（允许个人商用 / 法人商用 / 二次配布 / 成人向）
> SDK 兼容: SDK 2.x / SDK 3.x / VCC
> 类别: 3D Props / World / VRChat
> 沉淀日期: 2026-06-20

---

## 概述

**Lura's Switch**（内部名 LuraSwitch2）是 VRChat 创作者生态中**最受欢迎的免费通用开关 Prefab 集之一**，由 QuickBrown Design Studio 维护。把 9 种常见 World 交互场景封装成可拖拽 Prefab，附 Inspector HelpBox 双语说明 + Editor 实时预览 + 跨平台自动优化。

**核心优势**：
- **零代码使用**：拖 Prefab 即可，几乎所有需求无需写 Udon
- **9 种现成开关**：Mirror / DirectionalLight / PostEffect / 照明 / 视频 / 床 / 椅子 / 通用 / Voice Check
- **3 种同步模式可插拔**：Local（本地） / Global（手动同步） / LocalSave（持久化）
- **多种入口互操作**：Interact（点击）/ PhysBone Contact（Avatar 接触）/ Pickup（拾取）
- **PC / Quest 跨平台**：条件编译自动调整同步频率和材质复杂度
- **1 Material 轻量**：所有 Prefab 共享 1 个 Material Asset，VRAM 友好
- **完整 Editor 体验**：[ExecuteAlways] 预览 + HelpBox 双语 + Custom Inspector

> **对 Agent 的意义**：该 Prefab 集已沉淀出 6 个**通用 Udon 模式**（参见 `memory/sources/quickbrown-luraswitch2.md`），
> 同时也是**工具使用指南型参考工程**（C15）。两层身份互补：模式层给创作者"理解原理"，工具层给创作者"直接用"。

---

## 系统架构

```
Lura's Switch Prefab 集
│
├── 02_CORE/
│   ├── 01_Switch/                 ← 核心开关组件
│   │   ├── SwitchBase.cs          (1795 行,基础开关 + 3 同步模式)
│   │   ├── SliderSwitch.cs        (2218 行,5 段推子 + 软吸附)
│   │   ├── SwitchSyncer.cs        (主从同步器)
│   │   ├── SwitchSelector.cs      (互斥选择器)
│   │   ├── SwitchBoard.cs         (移动平台 + Pickup)
│   │   ├── Switch_Trigger.cs      (Interact 入口)
│   │   ├── Switch_Contact.cs      (PhysBone Contact 入口)
│   │   └── Switch_Pickup.cs       (Pickup 入口)
│   │
│   ├── 02_Mirror/                 ← 镜像系统
│   │   ├── MirrorController.cs    (LQ/HQ/Off 切换)
│   │   └── MirrorAreaPreview.cs   (Editor 实时预览)
│   │
│   ├── 03_ModeSwitch/             ← 互斥选择器
│   │   └── SwitchSelector.cs      (多选一 + 1 帧延迟初始化)
│   │
│   ├── 10_HeightOffsetter/        ← 玩家身高适配
│   │   ├── HeightOffsetter.cs     (双循环高度调节)
│   │   └── HeightOffsetterPreview.cs
│   │
│   └── 20_Extension/              ← 开关扩展功能
│       ├── 01_Respawn/            (重生点)
│       ├── 02_Teleport/           (传送点)
│       ├── 03_SavePoint/          (存档点 + LocalSave)
│       └── 04_Appearance/         (外观切换)
│
├── 03_UTIL/                       ← 实用控制器
│   ├── Controller_MirrorOpacity.cs
│   ├── Controller_ColliderHeight.cs
│   ├── Controller_LightIntensity.cs
│   ├── Controller_AudioVolume.cs
│   ├── Controller_PostEffect.cs
│   ├── Controller_TransformChange.cs
│   ├── Controller_ExternalParameter.cs
│   └── SkyboxSetter.cs
│
└── 04_MobileNightMode/            ← 移动端夜间模式
    └── HeadTracker.cs
```

**总计 39 个 .cs 文件 + 9 个 Prefab + 1 个 Sample Scene**

---

## 9 种开关 Prefab 一览

| 序号 | Prefab | 用途 | 关键组件 |
|------|--------|------|---------|
| 1 | **MirrorSwitch** | 控制 Mirror 反射 | `MirrorController` + `Controller_MirrorOpacity` |
| 2 | **DirectionalLightSwitch** | Avatar 5 段方向光（0/25/50/75/100%） | `SliderSwitch` + `Controller_LightIntensity` |
| 3 | **PostEffectSwitch** | 后处理 5 段强度 | `SliderSwitch` + `Controller_PostEffect` |
| 4 | **LightSwitch** | 世界灯组开关 | `SwitchBase` |
| 5 | **VideoPlayerSwitch** | 视频播放器开关（需自带播放器） | `SwitchBase` + 视频 Prefab |
| 6 | **BedSwitch** | 床用开关（可绑定 Station） | `SwitchBase` + Station |
| 7 | **ChairSwitch** | 椅子用开关 | `SwitchBase` + Station |
| 8 | **GenericObjectSwitch** | 通用对象开关（控制任意 GameObject） | `SwitchBase` + Target Object |
| 9 | **VoiceCheckSwitch** | 麦克风测试（玩家本地声音检测） | `HeadTracker` + AudioSource |

---

## 3 种同步模式

通过 `SwitchBase.SyncMode` 字段切换，无需写代码：

| 模式 | 值 | 适用场景 | 同步主体 | 持久化 |
|------|----|---------|---------|--------|
| **Local** | 0 | 单玩家本地状态（个人偏好） | 仅本地 | ❌ |
| **Global** | 1 | 全员同步（房间设置） | Manual Sync + 节流 | ❌ |
| **LocalSave** | 2 | 全员同步 + 玩家重连后恢复 | Manual Sync + PlayerData | ✅ (100KB 限制) |

**示例**：
- 床的开关 → `LocalSave`（玩家重连后还能用）
- 房间灯光 → `Global`（所有人共享当前状态）
- 玩家音量 → `Local`（仅本机）

---

## 多种入口（Activator）

| 入口组件 | 触发条件 | 用途 |
|---------|---------|------|
| `Switch_Trigger` | 玩家 Interact（点击 / 凝视） | 标准 UI 按钮 |
| `Switch_Contact` | PhysBone 接触（Avatar 触摸） | 触碰式机关 |
| `Switch_Pickup` | 拾起（手持） | 可移动开关 |

**可叠加**：同一个 `SwitchBase` 可同时挂多个 Activator 组件。

---

## 安装与使用

### 方式 1：通过 VCC（推荐）

1. 打开 VCC → New Project → 选 VRChat World 模板
2. VCC Settings → Add Package → 输入：
   ```
   https://lura.booth.pm/items/1969082 (BOOTH)
   ```
3. 在项目中打开示例场景：
   ```
   Assets/VirtualFoxDesignStudio/Lura'sSwitch/SCENE/SwitchSamples.unity
   ```
4. 在 Project 面板找到需要的 Prefab（如 `MirrorSwitch.prefab`），拖入自己的场景

### 方式 2：手动导入（无 VCC）

1. 从 BOOTH 下载 `_Persistence_Lura_sSwitch_ver3.00.zip`（SDK3 + Persistence）
2. Unity 中双击 `Lura'sSwitch.unitypackage` 导入
3. 打开 `SwitchSamples.unity` 示例场景
4. 复制 Prefab 到自己的场景

### 首次使用步骤

1. **选 Prefab**：从 Project 面板拖入场景
2. **Inspector 配置**：
   - `SyncMode` 选择 Local / Global / LocalSave
   - `Target Object` 字段绑定被控制对象（灯、Mirror、视频等）
   - 调整颜色 / 段位数等参数
3. **可选**：添加多个 Activator（Trigger / Contact / Pickup）
4. **测试**：进 Play Mode 或用 ClientSim 验证

---

## 版本演进

| 版本 | 发布时间 | 关键更新 |
|------|----------|---------|
| **v1.x** | 2019 | SDK2 时代基础版 |
| **v2.00** | — | 切换到 ManualSync（解决 Global 同步不稳），加 Object Reset 按钮 |
| **v2.01** | — | 修复 Global 同步 bug |
| **v2.02** | — | VCC 兼容 |
| **v3.00** | 2025+ | **Persistence（World Save）支持**（Local 模式）+ 脚本优化 |

> ⚠️ **当前推荐**：v3.00（Persistence）。SDK3 World 必备。

---

## 平台兼容性

| 平台 | 兼容性 | 备注 |
|------|--------|------|
| **PC VR** | ✅ 完整功能 | 最佳体验 |
| **PC Desktop** | ✅ 完整功能 | — |
| **Android (Quest)** | ✅ 自动优化 | 同步节流频率 + 0.5s、材质简化 |
| **iOS** | ⚠️ 理论支持 | 未经官方测试 |

**自动平台适配**：
- 通过 `SwitchPlatformOverride` 组件 + `#if UNITY_ANDROID` 条件编译
- Quest 端自动调整：
  - 滑块同步节流 0.1s → 0.3s
  - Mirror 强制 LQ 模式
  - Light 数量减半

---

## 已知限制

来自官方说明 + Agent 分析：

| 限制 | 说明 | 影响 |
|------|------|------|
| **不包含视频播放器** | 仅提供"开关"控制 | 需自行配置 Video Prefab |
| **麦克风测试无回声** | Voice Check 不模拟回声 | 仅检测声音强度 |
| **Light/PostEffect 参数为示例** | 需根据场景调整 | 创作者需自定义 |
| **单文件 2000+ 行** | SwitchBase 1795、SliderSwitch 2218 | 二开成本高 |
| **注释以日文为主** | 国际化差 | 中/英 Creator 阅读有门槛 |
| **Editor 反射访问私有字段** | `MirrorControllerEditor.cs` | 重命名字段后静默崩 |

---

## 沉淀到知识库的内容

### 通用模式（6 个）→ `memory/patterns/`

| 模式 | 文档 | 来源文件 |
|------|------|---------|
| Master-Follower Syncer | `patterns/master-follower-syncer.md` | `SwitchSyncer.cs` |
| Exclusive Control Selector | `patterns/exclusive-control-selector.md` | `SwitchSelector.cs` |
| Soft Detent Interpolation | `patterns/soft-detent-interpolation.md` | `SliderSwitch.cs` |
| Fade-Then-Snap | `patterns/fade-then-snap.md` | `SwitchBoard.cs` |
| Editor Preview Component | `patterns/editor-preview-component.md` | `MirrorAreaPreview.cs` 等 |
| MaterialPropertyBlock Safe Update | `patterns/material-propertyblock-safe-update.md` | `SwitchBase.cs` |

### 失败案例（4 个）→ `memory/reviews/common-failures.md`

| ID | 标题 | 来源 |
|----|------|------|
| FAIL-29 | 父 Selector 强制覆盖子 syncMode 时序错乱 | `SwitchSelector.cs` |
| FAIL-30 | 滑块插值自我回声导致抖动 | `SliderSwitch.cs` |
| FAIL-31 | Editor 反射访问私有字段导致重命名后静默崩 | `MirrorControllerEditor.cs` |
| FAIL-32 | `SendCustomEventDelayedFrames(1)` 在低帧率设备不可靠 | 全局 |

### 溯源 → `memory/sources/quickbrown-luraswitch2.md`

包含完整项目档案（39 .cs + 4 层职责 + 12 大难题 + 工程评价）

---

## 适用场景

✅ **最直接的应用**：
- 任何 World 需要的"开关"（灯光、门、机关、视频、椅子）
- 调节类控件（音量、亮度、PostEffect 强度）
- 多选一控制（关卡、模式、楼层）
- 移动平台（电梯、门廊、载具）
- 玩家身高适配（不同 Avatar 高度）

❌ **不适合**：
- 需要深度自定义的复杂系统（应自行开发）
- 想要学习 Udon 基础（应看官方教程）
- 商业项目需要付费支持（免费但无 SLA）

---

## 引用格式

**向创作者推荐时**：
> 推荐使用 **Lura's Switch【VCC／Persistence】** (v3.00)，QuickBrown Design Studio 维护，
> 免费 + UV License，涵盖 9 种 World 常用开关 Prefab。
> 下载：https://booth.pm/en/items/1969082

**作为知识来源时**：
> 来源：`memory/sources/quickbrown-luraswitch2.md`（案例研究 + 6 个 Pattern 来源）
> 工具使用：`memory/world/luraswitch2.md`（本文件）

---

## 关联知识库

| 文档 | 关系 |
|------|------|
| `memory/sources/quickbrown-luraswitch2.md` | **本项目的案例研究型源文档**（A6） |
| `memory/patterns/master-follower-syncer.md` | Syncer 模式（来自本项目） |
| `memory/patterns/exclusive-control-selector.md` | 互斥控制（来自本项目） |
| `memory/patterns/soft-detent-interpolation.md` | 软吸附（来自本项目） |
| `memory/patterns/fade-then-snap.md` | 淡入淡出（来自本项目） |
| `memory/patterns/editor-preview-component.md` | Editor 预览（来自本项目） |
| `memory/patterns/material-propertyblock-safe-update.md` | MPB 共享材质（来自本项目） |
| `memory/reviews/common-failures.md` | FAIL-29 ~ FAIL-32 |
| `memory/world/performance-guide.md` | World 性能优化（背景知识） |
| `memory/world/scene-components/vrc-objectsync.md` | VRCObjectSync（与 Manual Sync 选型对比） |
| `memory/rules/networking-rules.md` | 网络同步规则 |
| `memory/api/persistence.md` | PlayerData API（LocalSave 用） |
| `memory/platform/cross-platform-content.md` | PC/Quest 平台适配 |
