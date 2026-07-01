---
title: LuraSwitch2 通用开关套件(2026 重写版)
category: world
knowledge_level: applied
status: active
tags:
  - world
  - luraswitch2
  - recommended-plugin
  - udonsharp
  - vpm
  - 2026-rewrite
aliases:
  - "Lura's Switch"
  - LuraSwitch2
  - luraswitch
  - 开关套件
related:
  - world/vvmw.md
  - sources/quickbrown-luraswitch2.md
  - hybrid/udon-world-plugins.md
  - patterns/master-follower-syncer.md
  - patterns/exclusive-control-selector.md
  - patterns/soft-detent-interpolation.md
  - patterns/fade-then-snap.md
  - patterns/editor-preview-component.md
  - patterns/material-propertyblock-safe-update.md
  - reviews/common-failures.md
  - world/performance-guide.md
  - rules/networking-rules.md
  - api/persistence.md
  - platform/cross-platform-content.md
source: QuickBrown LuraSwitch2 + lurathunder 文档站
source_type: community
version: 1.06
last_review: 2026-06-21
confidence: High
---
# LuraSwitch2 通用开关套件(2026 重写版)

> ⚠️ **2026-02-11 迁移声明**:旧版 **Lura's Switch v3.00 (Persistence)** 已被 **LuraSwitch2 v1.06** 取代。
> 旧版本包保留为 **LuraSwitch (Legacy)**,支持已终止。Legacy 下载迁移至 Google Drive。
> 本文档自 2026-06-21 起基于 v1.06 (2026-03-06) 重写。

---

## 速览

| 项 | 值 |
|---|---|
| **当前版本** | **LuraSwitch2 v1.06** (2026-03-06) |
| **作者** | Lura (@Lu_Ra_999) / QuickBrown Design Studio |
| **BOOTH 下载** | https://lura.booth.pm/items/1969082 (37.2 MB, 免费) |
| **官方文档站** | https://lurathunder.github.io/lura-switch-docs/ |
| **文档仓库** | https://github.com/LuraThunder/lura-switch-docs |
| **许可证** | **VN3 License**(取代旧版 UV License) |
| **VN3 License 全文** | https://drive.google.com/drive/folders/1g4-V0d1sjvLI22GfQ7PUsd0ZmxJBDCCp |
| **旧版 Legacy 下载** | https://drive.google.com/drive/folders/1iEdCZLwvuorDIdn5Yc4e7Nk8HHzVzoXb |
| **Discord** | https://discord.com/invite/qXs66HEhVY |
| **示例 World** | `wrld_79a83daf-c551-451f-a332-588ae4a5aea0` |
| **SDK 兼容** | VRChat SDK3 + UdonSharp 3.10+,Unity 2022.3.22f1+ |
| **类别** | 3D Props / World / VRChat(免费) |
| **沉淀日期** | 2026-06-21(A13 重写) |

---

## 概述

**LuraSwitch2** 是 VRChat 创作者生态中**最受欢迎的免费通用开关 Prefab 集**,由 QuickBrown Design Studio 维护。
2026-02-11 发布 v1.00 完全重写,基于 **UdonSharp** 从零重新设计,把 9 种以上常见 World 交互场景封装成可拖拽 Prefab,
附 Inspector 双语说明 + Editor 实时预览 + 跨平台自动优化 + 哈普提克斯反馈。

**核心优势**:
- **零代码使用**:拖 Prefab 即可,几乎所有需求无需写 Udon
- **9+ 种现成 Prefab**:Mirror / Switch / Slider / ModeSwitch / Syncer / Selector / Slider_Night / Slider_Video / PlatformOverride
- **3 种同步模式可插拔**:Local(本地) / Global(手动同步) / LocalSave(持久化)
- **多种入口互操作**:Interact(点击) / PhysBone Contact(Avatar 接触) / Pickup(拾取) / **Contact Touch(手指触摸,v1.05+)**
- **PC / Quest 跨平台**:`SwitchPlatformOverride` 组件 + 条件编译
- **现代化设计**:2D/3D 双形态,带 Emission 反馈和哈普提克斯
- **完整 Editor 体验**:`[ExecuteAlways]` 预览 + HelpBox + Custom Inspector

> **对 Agent 的意义**:该 Prefab 集已沉淀出 6 个**通用 Udon 模式**(参见 `memory/sources/quickbrown-luraswitch2.md`),
> 同时也是**工具使用指南型参考工程**(C15)。两层身份互补:模式层给创作者"理解原理",工具层给创作者"直接用"。
> 注意:这 6 个 Pattern 提炼自旧 v3.00,LuraSwitch2 v1.06 内部 API 已完全重写,二开参考时请以新源码为准。

---

## 系统架构(v1.06 重写)

```
LuraSwitch2 项目结构
│
├── Assets/QuickBrown/LuraSwitch2/
│   ├── 01_PREFAB/                  ← 可用 Prefab(9+ 种)
│   │   ├── Mirror/                 (LuraMirror + LuraMirror_SwitchSet)
│   │   ├── Switch/                 (BaseSwitch + 变体)
│   │   ├── Slider/                 (Slider 3D / 2D 双向)
│   │   ├── ModeSwitch/             (互斥选择器)
│   │   ├── SwitchSelector/         (枚举选择)
│   │   ├── SwitchBoard/            (移动平台 + Pickup)
│   │   ├── SwitchSyncer/           (主从同步)
│   │   ├── Slider_Night/           (移动端夜间模式 v1.04+)
│   │   ├── Slider_Video/           (VizVid 集成 v1.05+)
│   │   └── SwitchPlatformOverride/ (平台覆盖 v1.04+)
│   │
│   ├── 02_CORE/                    ← 核心 UdonSharp 脚本
│   │   ├── BaseSwitch.cs           (基础开关)
│   │   ├── SliderSwitch.cs         (滑块 + 软吸附)
│   │   ├── SwitchSyncer.cs         (主从同步器)
│   │   ├── SwitchSelector.cs       (互斥选择器)
│   │   ├── SwitchBoard.cs          (移动平台)
│   │   ├── LuraMirror/             (高功能镜像)
│   │   └── ...
│   │
│   └── SCENE/
│       └── LuraSwitch2_SAMPLE.unity  (示例场景)
│
└── 文档:lurathunder.github.io/lura-switch-docs/
```

> ⚠️ **重要变化**:v1.06 内部 API 与 v3.00 不兼容(完全重写),v3.00 的 39 .cs 文件已废弃。
> 直接拿 v3.00 的 ScriptableObject / Prefab 引用到 v1.06 会丢失。

---

## 9+ 种 Prefab 一览

| 序号 | Prefab | 用途 | 关键组件 | 引入版本 |
|------|--------|------|---------|---------|
| 1 | **LuraMirror_SwitchSet** | 整套镜像 + 开关组合(推荐起点) | `LuraMirror` + `Switch` + `ModeSwitch` + `Slider` + `Syncer` + `Board` | v1.00 |
| 2 | **Switch** (BaseSwitch) | 标准 ON/OFF 开关 | `BaseSwitch` | v1.00 |
| 3 | **Slider** | 连续值滑块(3D/2D) | `SliderSwitch` | v1.00 |
| 4 | **ModeSwitch** | 互斥模式选择(HQ/LQ 等) | `ModeSwitch` | v1.00 |
| 5 | **SwitchSelector** | 枚举值选择(关卡、模式、楼层) | `SwitchSelector` | v1.00 |
| 6 | **SwitchSyncer** | 多个开关状态同步 | `SwitchSyncer` | v1.00 |
| 7 | **SwitchBoard** | 移动平台 + Pickup 入口 | `SwitchBoard` | v1.00 |
| 8 | **LuraMirror** | 高功能镜像(HQ/LQ/透明度/距离淡出) | `LuraMirror` | v1.00 |
| 9 | **Slider_Night (Mobile)** | Quest/Android 夜间模式(替代 PostEffect) | `Slider_Night` | **v1.04** |
| 10 | **Slider_Video (VizVid)** | VizVid 视频音量滑块控制 | `Slider_Video` | **v1.05** |
| 11 | **SwitchPlatformOverride** | 平台默认状态覆盖(Android/iOS 隐藏) | `SwitchPlatformOverride` | **v1.04** |

> **配色规则**(来自作者访谈):白=Mirror / 橙=Object / 粉=Media / 水蓝=功能切换 / 深绿=Collider / 薄紫=视觉 / 米=Light / 黄绿=即发火脚本

---

## 3 种同步模式

通过 `BaseSwitch.SyncMode` 字段切换,无需写代码:

| 模式 | 值 | 适用场景 | 同步主体 | 持久化 |
|------|----|---------|---------|--------|
| **Local** | 0 | 单玩家本地状态(个人偏好) | 仅本地 | ❌ |
| **Global** | 1 | 全员同步(房间设置) | Manual Sync + 节流 | ❌ |
| **LocalSave** | 2 | 全员同步 + 玩家重连后恢复 | Manual Sync + PlayerData | ✅ (100KB 限制) |

**示例**:
- 床的开关 → `LocalSave`(玩家重连后还能用)
- 房间灯光 → `Global`(所有人共享当前状态)
- 玩家音量 → `Local`(仅本机)

> ⚠️ **v1.06 修复**:SwitchSelector 在 Global 模式下 LateJoiner 行为异常已在 v1.06 修复(2026-03-06)。
> 早于此版本请升级。

---

## 多种入口(Activator)

| 入口组件 | 触发条件 | 用途 | 引入版本 |
|---------|---------|------|---------|
| **Interact** | 玩家 Interact(点击 / 凝视) | 标准 UI 按钮 | v1.00 |
| **PhysBone Contact** | Avatar 接触(PhysBone) | 触碰式机关 | v1.00 |
| **Pickup** | 拾起(手持) | 可移动开关 | v1.00 |
| **Contact Touch** | 手指直接触摸(Quest 控制器 / Index) | 体感开关 | **v1.05** |
| **Haptics** | 操作反馈振动 | 操作反馈 | v1.00 |

**可叠加**:同一个 `BaseSwitch` 可同时挂多个 Activator 组件。

---

## v1.04-v1.06 新功能(2026 大重写核心)

### Slider_Video (VizVid 集成)— v1.05+

LuraSwitch2 与 **VizVid** 视频播放器的官方集成,允许滑块直接控制 VizVid 实例的音量。
适用场景:背景音乐音量、视频通话音量、影院模式音量调节。

### Slider_Night (Mobile)— v1.04+

Quest / Android / iOS 等**无法使用 PostEffect** 的平台的夜间模式替代方案。
通过调整灯光和环境参数模拟夜间观感,而非依赖 PostProcess Volume。

### SwitchPlatformOverride — v1.04+

允许 Android/iOS 等 PC 以外平台**覆盖**开关的默认状态。
- 隐藏特定开关(`HIDE` 状态)
- 强制默认 ON / OFF
- 控制对象 GameObject 的 active 状态

> v1.04 同时为 `BaseSwitch` 增加了 `HIDE` 状态视觉,以便恢复 PlatformOverride 隐藏的开关。

### Contact Touch — v1.05+

Quest 控制器和 Valve Index 用户可用**手指直接触摸**触发开关(无需按键)。
- 触觉反馈(哈普提克斯)
- 关闭时仍可使用 Interact
- 配置文件 `Switch_Contact` 中可关闭此功能

### Haptics (哈普提克斯反馈)— v1.00+ 强化

v1.05 强化了**所有操作反馈**:
- 按下:短促振动 + 高品质音效(由 wakaran @wakaran4 制作)
- 滑动:连续振动反馈
- 3D / 2D 模式切换有不同音效

---

## 平台兼容性

| 平台 | 兼容性 | 备注 |
|------|--------|------|
| **PC VR** | ✅ 完整功能 | 最佳体验 |
| **PC Desktop** | ✅ 完整功能 | — |
| **Android (Quest)** | ✅ 自动优化 | 同步节流 + 材质简化 + Contact Touch |
| **iOS** | ✅ 理论支持 | PlatformOverride 支持 |

**自动平台适配**:
- `SwitchPlatformOverride` 组件 + `#if UNITY_ANDROID` 条件编译
- Quest 端自动调整:
  - 滑块同步节流 0.1s → 0.3s
  - Mirror 强制 LQ 模式(可选)
  - Light 数量减半
  - PostEffect 不可用时自动 fallback 到 Slider_Night

---

## 安装与使用

### 方式 1:通过 VCC(推荐)

1. 打开 VCC → New Project → 选 VRChat World 模板
2. VCC Settings → Add Package → 输入:
   ```
   https://lura.booth.pm/items/1969082 (BOOTH)
   ```
3. 在项目中打开示例场景:
   ```
   Assets/QuickBrown/LuraSwitch2/SCENE/LuraSwitch2_SAMPLE.unity
   ```
4. 从 Project 面板找到 `LuraMirror_SwitchSet[SAMPLE]`,拖入自己的场景

### 方式 2:手动导入 .unitypackage(无 VCC)

1. 从 BOOTH 下载 `LuraSwitch2__Ver1.06_.zip`
2. 解压后双击 `LuraSwitch2.unitypackage` 导入
3. 打开 `LuraSwitch2_SAMPLE.unity` 示例场景
4. 复制 Prefab 到自己的场景

### 快速入门(7 步)

1. **选 Prefab**:从 Project 面板拖入场景
2. **Inspector 配置**:
   - `SyncMode` 选择 Local / Global / LocalSave
   - `Target Object` 字段绑定被控制对象
   - 调整颜色 / 段位数等参数
3. **可选**:添加多个 Activator(Interact / Contact / Pickup / Touch)
4. **同步**:`SwitchSyncer` 拖入场景,设置 Master/Follower
5. **多选一**:`SwitchSelector` 拖入,设置多个目标
6. **平台差异**:`SwitchPlatformOverride` 处理 Quest/iOS 端
7. **测试**:进 Play Mode 或用 ClientSim 验证

---

## 版本演进(LuraSwitch2)

| 版本 | 发布时间 | 关键更新 |
|------|----------|---------|
| **v1.00** | 2026-02-11 | LuraSwitch 2 新版本发布(UdonSharp 完全重写) |
| **v1.01** | 2026-02-12 | `Slider_Light` 支持 VRCLV PointLightVolume;修复 Emission 对象镜内 Bloom 问题 |
| **v1.02** | 2026-02-12 | 修复 `Slider_Audio` 多 AudioSource 控制问题 |
| **v1.03** | 2026-02-14 | `SwitchSelector` 新增"全部关闭"选项 |
| **v1.04** | 2026-02-19 | `Slider_Night (Mobile)` 加入;`SwitchPlatformOverride` Prefab 加入;`Slider_Light` 支持 LightVolume Intensity;`BaseSwitch` 增加 HIDE 状态 |
| **v1.05** | 2026-03-01 | Contact Touch 功能;`Slider_Video (VizVid)` 加入;2DUI 着色器 EmissionMultiplier;多项同步 bug 修复 |
| **v1.06** | 2026-03-06 | 修复 SwitchSelector Global + LateJoiner 异常;SavePoint 非激活时的 Respawn 误调用 |

> **当前推荐**:**v1.06**(2026-03-06)。SDK3 World 必备。

### 旧版 Legacy 时间线(参考)

| 版本 | 时间 | 备注 |
|------|------|------|
| Lura's Switch v1.x | 2019 | SDK2 时代基础版 |
| Lura's Switch v2.00-v2.02 | 2019-2025 | VCC 兼容 + ManualSync |
| **Lura's Switch v3.00 (Persistence)** | 2025 | 最后 Legacy 版本 |
| LuraSwitch2 v1.00-v1.06 | 2026-02-11 ~ 2026-03-06 | 完全重写,目前 active |

> 旧 LuraSwitch 包已迁移到 Google Drive:`https://drive.google.com/drive/folders/1iEdCZLwvuorDIdn5Yc4e7Nk8HHzVzoXb`
> 旧版支持已终止,**强烈建议迁移到 LuraSwitch2 v1.06**。

---

## 已知限制

来自官方说明 + Agent 分析(v1.06):

| 限制 | 说明 | 影响 |
|------|------|------|
| **v1.06 与 v3.00 API 不兼容** | 内部完全重写 | 旧 Prefab 引用丢失,需重新设置 |
| **不包含视频播放器** | Slider_Video 仅控制 VizVid 音量 | 需自行配置 VizVid Prefab |
| **Light/PostEffect 参数为示例** | 需根据场景调整 | 创作者需自定义 |
| **注释以日文为主** | 国际化差 | 中/英 Creator 阅读有门槛 |
| **Skybox FogMode 限制** | VRChat 不允许运行时修改 FogMode | SkyboxSetter 强制匹配场景 |

---

## 沉淀到知识库的内容

### 通用模式(6 个)→ `memory/patterns/`

| 模式 | 文档 | 来源文件(v3.00) | v1.06 适配 |
|------|------|-------------|----------|
| Master-Follower Syncer | `patterns/master-follower-syncer.md` | `SwitchSyncer.cs` | ✅ API 名称略变,核心思想一致 |
| Exclusive Control Selector | `patterns/exclusive-control-selector.md` | `SwitchSelector.cs` | ✅ |
| Soft Detent Interpolation | `patterns/soft-detent-interpolation.md` | `SliderSwitch.cs` | ✅ |
| Fade-Then-Snap | `patterns/fade-then-snap.md` | `SwitchBoard.cs` | ✅ |
| Editor Preview Component | `patterns/editor-preview-component.md` | `MirrorAreaPreview.cs` | ✅ |
| MaterialPropertyBlock Safe Update | `patterns/material-propertyblock-safe-update.md` | `SwitchBase.cs` | ✅ |

> ⚠️ **历史说明**:这 6 个 Pattern 提炼自 v3.00 (Persistence)。LuraSwitch2 v1.06 内部 API 已完全重写,
> 模式**思想仍然适用**,但直接拷贝 v3.00 代码到 v1.06 项目会失败。二开时请以 v1.06 源码为准。

### 失败案例(4 个)→ `memory/reviews/common-failures.md`

| ID | 标题 | 来源 | v1.06 状态 |
|----|------|------|-----------|
| FAIL-29 | 父 Selector 强制覆盖子 syncMode 时序错乱 | `SwitchSelector.cs` | v1.06 已修复 |
| FAIL-30 | 滑块插值自我回声导致抖动 | `SliderSwitch.cs` | v1.06 已修复 |
| FAIL-31 | Editor 反射访问私有字段导致重命名后静默崩 | `MirrorControllerEditor.cs` | v1.06 已重构 |
| FAIL-32 | `SendCustomEventDelayedFrames(1)` 在低帧率设备不可靠 | 全局 | v1.06 SavePoint 改用延迟初始化 |

### 溯源 → `memory/sources/quickbrown-luraswitch2.md`

包含完整项目档案(基于 v3.00 案例研究,作为历史参考)

---

## 适用场景

✅ **最直接的应用**:
- 任何 World 需要的"开关"(灯光、门、机关、视频、椅子)
- 调节类控件(音量、亮度、PostEffect 强度)
- 多选一控制(关卡、模式、楼层)
- 移动平台(电梯、门廊、载具)
- 玩家身高适配(不同 Avatar 高度)
- 移动端夜间模式(Slider_Night)
- VizVid 视频音量控制(Slider_Video)

❌ **不适合**:
- 需要深度自定义的复杂系统(应自行开发)
- 想要学习 Udon 基础(应看官方教程)
- 商业项目需要付费支持(免费但无 SLA)

---

## 引用格式

**向创作者推荐时**:
> 推荐使用 **LuraSwitch2 v1.06** (2026-03-06),QuickBrown Design Studio (Lura) 维护,
> 免费 + VN3 License,涵盖 9+ 种 World 常用开关/滑块/镜像 Prefab,完美支持 PC/Quest 跨平台。
> 官方文档:https://lurathunder.github.io/lura-switch-docs/
> BOOTH:https://lura.booth.pm/items/1969082

**作为知识来源时**:
> 来源:`memory/sources/quickbrown-luraswitch2.md`(基于 v3.00 案例研究 + 6 个 Pattern 来源)
> 工具使用:`memory/world/luraswitch2.md`(本文档,基于 v1.06 重写)

---

## 关联知识库

| 文档 | 关系 |
|------|------|
| `memory/sources/quickbrown-luraswitch2.md` | **本项目的案例研究型源文档**(基于 v3.00,作为历史参考) |
| `memory/sources/udon-world-plugins.md` | Udon World 插件索引 |
| `memory/world/vvmw.md` | VVMW 视频管理(可与 Slider_Video 配合) |
| `memory/patterns/master-follower-syncer.md` | Syncer 模式(来自本项目) |
| `memory/patterns/exclusive-control-selector.md` | 互斥控制(来自本项目) |
| `memory/patterns/soft-detent-interpolation.md` | 软吸附(来自本项目) |
| `memory/patterns/fade-then-snap.md` | 淡入淡出(来自本项目) |
| `memory/patterns/editor-preview-component.md` | Editor 预览(来自本项目) |
| `memory/patterns/material-propertyblock-safe-update.md` | MPB 共享材质(来自本项目) |
| `memory/reviews/common-failures.md` | FAIL-29 ~ FAIL-32 |
| `memory/world/performance-guide.md` | World 性能优化(背景知识) |
| `memory/rules/networking-rules.md` | 网络同步规则 |
| `memory/api/persistence.md` | PlayerData API(LocalSave 用) |
| `memory/platform/cross-platform-content.md` | PC/Quest 平台适配 |
