---
title: Skeletal Input & Finger Tracking — Avatar 手指骨骼追踪
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - skeletal-input
  - finger-tracking
  - muscle-definition
  - legacy-fingers
  - steamvr

aliases:
  - Skeletal Input
  - 骨骼输入
  - Finger Tracking
  - 手指追踪
  - Hand Tracking
  - Legacy Fingers
  - Muscle Definition
  - 肌肉定义

related:
  - avatar/standard-hand-poses.md
  - avatar/animator-system.md
  - avatar/avatar-modding-guide.md
  - avatar/modular-avatar.md
  - avatar/playable-layers.md

source: docs.vrchat.com/docs/steamvr-input-20 + creators.vrchat.com (Muscle Definitions)
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Skeletal Input & Finger Tracking — Avatar 手指骨骼追踪

> 来源:
> - https://docs.vrchat.com/docs/steamvr-input-20
> - Unity 文档: https://docs.unity3d.com/Manual/MuscleDefinitions.html
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方 + Unity 官方)
> 关联: `avatar/standard-hand-poses.md` (手势定义) + `avatar/animator-system.md` (手势参数)

---

## 概述

> [FACT] **Skeletal Input** 允许 VR 控制器**提供尽可能精确的姿势**给 VRChat，**无需为每个控制器做特定支持**。
>
> VRChat 通过 **SteamVR Input 2.0 API** 接收 Skeletal Input。
>
> 适用场景:
> - HTC Vive Wands 增强姿势
> - Oculus / Quest Touch 控制器
> - 全手姿势（Hand Tracking）

> **🔴 关键事实**: 从 **VRChat 2024.3.1** 开始使用 SteamVR Input 2.0。

---

## 1. 玩家侧：3 个相关开关

> [FACT] 玩家可以**通过 3 个开关**控制 Skeletal Input 行为。

### 1.1 Legacy Fingers（per-avatar 开关）

> [FACT] **Legacy Fingers** 是 **per-avatar 开关**。
>
> 位置: Action Menu → Quick Actions
>
> 启用时:
> - **Quest / Index 控制器**等部分 Skeletal Finger Tracking 通过**旧版方法**处理
> - **与 Index 控制器过去用的方式相同**
> - **可以**针对每个 Avatar **独立切换**

> **重要**: Hand Tracking 忽略此开关（不兼容旧方法）。

### 1.2 Avatars Use Finger Tracking（全局开关）

> [FACT] **Avatars Use Finger Tracking** 是**全局开关**。
>
> 位置: Main Menu → Controls
>
> 关闭时:
> - Avatar 手部**回退到动画手部状态**，即使有 Skeletal Tracking 数据
> - **手势参数检测**（包括依赖手指追踪的检测）**仍工作**
> - Gestures Toggle 仍影响手的动画

### 1.3 Gesture Toggle

> [FACT] **Gesture Toggle** 控制是否尝试将手指姿势**与标准手姿匹配**。
>
> - 关闭时: 不会尝试匹配
> - 开启时: 正常匹配

> 详见 `avatar/standard-hand-poses.md` (7 种标准手姿定义)

---

## 2. 创作者侧：Avatar 手指配置

> [FACT] **创作者可以通过调整 Avatar Rig 的肌肉配置**控制手指如何解释 Skeletal Tracking。
>
> Unity 文档: [Muscle Definitions](https://docs.unity3d.com/Manual/MuscleDefinitions.html)

### 2.1 配置入口

```
Unity → Project → 选中 Avatar FBX →
Inspector → Rig tab →
Animation Type: Humanoid →
Configure... →
Muscle & Settings tab
```

### 2.2 关键调整点

> [FACT] **调整手指静止和展开位置**:
> - 在 **Avatar Muscles & Settings** 标签
> - 找到 Finger bones
> - 调整 **Per-Muscle Settings** 的 **min / max** 范围
> - **必须**同时调整左右手

### 2.3 测试工具

> [FACT] Unity 提供 **Muscle Group Preview** 测试:
> - **Finger Open Close** slider: 测试开/合
> - **Finger In Out** slider: 测试收/展
>
> 这两个 slider 可以**实时预览** Avatar 手部在 Skeletal Input 下的表现。

### 2.4 微调选项

> [FACT] 进一步微调手指姿势:
> - **Intermediate bone ranges** (中间骨骼)
> - **Distal bone ranges** (远端骨骼)
>
> 这两个微调可以**更精确**控制手指形状。

### 2.5 推荐流程

> [FACT] 创作者推荐的手指配置流程:
> 1. 设置 Humanoid Rig
> 2. Configure Avatar Muscles
> 3. 调整 Finger bones 的 min/max 范围
> 4. 用 Finger Open Close 测试
> 5. 必要时微调 Intermediate / Distal
> 6. 在 VRChat 中测试 Skeletal Input 效果
> 7. 如有问题，启用 **Legacy Fingers** 兼容性测试

---

## 3. Hand Tracking（完整手部追踪）

> [FACT] VRChat 通过 **SteamVR Input 2.0 API** 支持**完整手部追踪**（相机追踪、手套等）。
>
> 行为类似于 Quest 版 VRChat:
> - 不仅驱动 Avatar 动画
> - 也作为**菜单导航、麦克风切换**的输入
> - 替代传统控制器的部分输入

### 3.1 SteamVR Skeleton 高保真要求

> [FACT] SteamVR API 提供**高保真度描述值**。
>
> **只有最高保真度的 skeleton 才能用于完整手部追踪**。
>
> 当 full identity skeleton 可用时，VRChat **同时**用于:
> - Avatar 动画
> - 菜单/麦克风输入

### 3.2 第三方驱动

> [FACT] 在 SteamVR 生态中，**控制器支持**（包括虚拟控制器如手）由**驱动**提供。
>
> - 一个驱动处理一个或多个控制器
> - 装好后 SteamVR 自动识别
> - 第三方驱动可能需要**手动安装**或更新

### 3.3 驱动管理

> [FACT] 查看已安装的第三方驱动:
> ```
> SteamVR Settings → Startup/Shutdown page → Manage Add-Ons
> ```

### 3.4 驱动配置位置不固定

> [FACT] **第三方驱动可能有自己的配置位置** — 没有标准位置。
>
> 需要参考每个驱动的文档。

### 3.5 创作者驱动开发

> [FACT] 如果你是**驱动开发者**且 Hand Tracking 行为异常:
>
> 参考 [SteamVR Skeletal Hand Tracking Driver Guide](https://creators.vrchat.com/platforms/pc/steamvr-drivers/)
>
> ⚠️ 该页是**高级驱动开发**专用，不适合普通用户。

---

## 4. Skeletal Input 兼容性表

> [FACT] Skeletal Input 兼容性:

| 设备 | 兼容性 | 备注 |
|------|--------|------|
| **Quest 2/3/Pro** | ✅ 原生支持 | 通过 Quest 自身 + Virtual Desktop/ALVR |
| **Valve Index** | ✅ 完全支持 | 历史最长支持 |
| **Oculus Touch** | ✅ 支持 | Skeletal Input |
| **HTC Vive Wands** | ✅ 增强 | Skeletal Input 增强 |
| **Tracking Gloves** | ✅（如果驱动支持）| 通过 SteamVR 驱动 |
| **Leap Motion** | ✅（如果驱动支持）| 通过 SteamVR 驱动 |
| **Virtual Desktop** | ⚠️ 需要 ≥ 1.32.13 | 早期版本可能有问题 |

### 4.1 Virtual Desktop 特殊注意

> [FACT] 使用 **Virtual Desktop** 时遇到手部异常?
> 1. 升级到 **Virtual Desktop 1.32.13+**
> 2. 早期版本可能有问题，但**最新版本应已解决**

---

## 5. Skeletal Input 的限制

> [FACT] Skeletal Input 在**以下情况可能异常**:

| 场景 | 表现 | 解决 |
|------|------|------|
| **Avatar 没有正确配置肌肉范围** | 手指摆动奇怪 | 调整 Per-Muscle Settings |
| **驱动不兼容** | 手指不显示或显示错误 | 升级驱动 |
| **VRAM 紧张** | 手部更新延迟 | 优化 Avatar |
| **手部追踪源不是 high-fidelity** | 不支持完整手部输入 | 用传统控制器 |

---

## 6. SteamVR Input 2.0 Action Sets

> [FACT] VRChat 有 **4 个 Action Sets** 用于不同上下文。

| Action Set | 用途 | Mirror |
|------------|------|--------|
| **global** | 全局（所有上下文）| - |
| **one_hand** | 单手模式（一个控制器关）| ✅ |
| **menu** | 菜单操作（Quick / Main Menu）| ✅ |
| **action_menu** | 圆形 Action Menu | ✅ |

> **优先级**: **global** 始终激活，除非相同输入在**其他 Action Set** 绑定。

### 6.1 Action Set 排错

> [FACT] 添加/删除绑定无效或找不到绑定?
> - 检查**每个 Action Set** 中的绑定
> - **global** 和 **one_hand** 共享**很多 actions**
> - 检查**绑定类型**是否匹配（Vector1/Vector2）

---

## 7. 创作者实践指南

### 7.1 Avatar 手指配置最佳实践

> [FACT] 创作者推荐:
>
> 1. **不要假设 Index 控制器**为标准（因为 Skeletal Input 现在应用到所有控制器）
> 2. **调整肌肉范围**以适应多种手指配置
> 3. 提供 **Legacy Fingers** 兼容性（per-avatar 开关）
> 4. **测试** 多种控制器：Quest Touch / Index / Vive
> 5. **避免**手指大幅度反向（muscle range 限制）

### 7.2 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 手指方向奇怪 | Muscle range 太宽/窄 | 调整 Per-Muscle Settings |
| 手指不响应 Skeletal Input | 驱动问题 | 升级驱动 |
| 部分 Avatar 正常，部分异常 | Avatar 肌肉配置 | 在肌肉配置中调整 |
| 完整手部输入失效 | 非 high-fidelity skeleton | 升级硬件/驱动 |
| Virtual Desktop 异常 | 旧版本 | 升级到 1.32.13+ |

### 7.3 与 Legacy 系统对比

> [FACT] **旧版（Skeletal Input 前）**:
> - Quest / Touch 用户**没有** Skeletal Tracking
> - 依赖 Avatar 动画 + Gesture 匹配
> - Index 用户有简单的 finger-curl-only tracking

> [FACT] **新版（Skeletal Input 后）**:
> - **所有控制器**应用 SteamVR Skeletal Tracking
> - 通过 **Humanoid Muscle Range** 控制
> - **Legacy Fingers** 兼容旧版 Index 行为

### 7.4 恢复旧版行为

> [FACT] 玩家可以恢复旧版行为:
> - **Quest/Touch 用户**: Main Menu → Controls → 关闭 "Avatars Use Finger Tracking"
> - **Index 用户**: Action Menu → Quick Actions → 启用 "Legacy Fingers" (per-avatar)
>
> 创作者角度: **Legacy Fingers 启用时**，Avatar 应**保持 Index 旧版风格**（简单 finger-curl）

---

## 8. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `avatar/standard-hand-poses.md` | 7 种标准手姿定义（用于 Gesture）|
| `avatar/animator-system.md` | Gesture Animator Parameters 接收手指输入 |
| `avatar/playable-layers.md` | Gesture Layer 接收 Skeletal Input 数据 |
| `avatar/avatar-modding-guide.md` | 修复 Avatar 姿势问题 |
| `platform/mobile-ui-optimization.md` | 移动端 UI 替代手势 |

---

## 9. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **Muscle range** 推荐的精确值（min/max 数值）
2. ❓ **驱动** 列表和推荐配置
3. ❓ **Hand Tracking** 在 Quest 独立版与 PC 版的具体差异
4. ❓ **Skeletal Input** 对**性能**的具体影响（FPS 影响）
5. ❓ Quest 3 增强版 Hand Tracking 是否需要特殊配置
6. ❓ Muscle range 调整不当是否会导致 Avatar 审核失败
7. ❓ 多个驱动并存时如何选择
8. ❓ Skeletal Input 与 PhysBone 是否有冲突

---

## 来源

- [SteamVR Input 2.0](https://docs.vrchat.com/docs/steamvr-input-20)
- [Input 2.0 FAQ](https://docs.vrchat.com/docs/input-20-faq)
- [Unity Muscle Definitions](https://docs.unity3d.com/Manual/MuscleDefinitions.html)
- [SteamVR Skeletal Hand Tracking Driver Guide](https://creators.vrchat.com/platforms/pc/steamvr-drivers/)
- 本地化版本: `参考文献/SP/user-guide/steamvr-input-20.md` + `input-20-faq.md`
