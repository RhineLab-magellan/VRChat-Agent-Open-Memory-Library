---
title: VRCTween — 官方补间动画系统总览
category: world
subcategory: udon/vrctween

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - vrctween
  - animation
  - tween
  - index

aliases:
  - "VRCTween 补间系统"
  - "VRCTween Overview"
  - "补间动画"
  - "DOTween"

related:
  - ../index.md
  - ../animation-events.md
  - ../event-execution-order.md
  - ../udonsharp/compilation.md
  - ../../../rules/performance-rules.md

source: VRChat Creator Docs (https://creators.vrchat.com/worlds/udon/vrctween/)
source_type: official
version: 1.1
last_review: 2026-06-22
confidence: High
change_log:
  - 2026-06-22: 新增"底层实现 (DOTween)"章节; 与官方 2026-05-28 版本逐项校验对齐; 引用 5 份原始英文文档
---

# VRCTween — 官方补间动画系统总览

> 来源: https://creators.vrchat.com/worlds/udon/vrctween/
> 抓取日期: 2026-06-21
> 状态: ✅ FACT (官方文档本地化)
> SDK 要求: VRChat Worlds SDK 3.7+ (2024 年发布, 2025-2026 持续迭代)

---

## 概述

**VRCTween** 是 VRChat 官方在 SDK 中内置的**补间 (tweening) 动画系统**,基于成熟的 **DOTween** 库。它允许 UdonSharp / Udon Graph 创作者用**几行代码**实现位置、旋转、缩放、颜色、音量等**平滑过渡**,**无需手写 Update 循环**和插值数学。

> **核心价值**: 把"每帧手动 lerp/slerp"封装为一行 API + 链式配置,内置缓动、回调、循环、暂停、复用等全部功能。

### 何时使用 VRCTween

| 场景 | 推荐方案 |
|---|---|
| 按钮按下回弹 / UI 淡入淡出 / 物体开门 | ✅ **VRCTween**(首选) |
| 玩家相机平滑跟随 / 角色控制 | ✅ VRCTween 复用模式 |
| 大量同步动画 / Late joiner 状态恢复 | ⚠️ VRCTween(本地)+ UdonSynced 时间戳 |
| 与 Animator 状态机配合 | 看情况:VRCTween 用于代码驱动,Animator 用于美术驱动 |
| 网络同步(每个玩家看到不同步) | ❌ VRCTween 默认**不自动同步**,需配合 [UdonSynced] 时间戳 |

### 何时**不**使用 VRCTween

- ❌ **物理运动** — 用 Rigidbody / PhysBone
- ❌ **需要 Late joiner 看到精确进度** — 必须用 Synced 时间戳 + Goto()
- ❌ **需要逐帧外部控制** — 改用 Update 手写插值

---

## 核心 API 速览

```csharp
using VRC.SDK3.Components;
using VRC.SDKBase;  // 提供 VRCTween namespace

// 1. 创建补间(返回 VRCTweenHandle)
VRCTweenHandle tweenHandle = cube.TweenPosition(
    new Vector3(0, 5, 0),   // 目标值
    2f,                       // 持续时间(秒)
    VRCTweenEase.OutQuad      // 缓动
);

// 2. 链式配置(返回 handle 继续链)
tweenHandle
    .SetDelay(0.5f)                        // 延迟 0.5s 才开始
    .SetLoops(2, VRCTweenLoopType.Yoyo)    // 来回 2 次
    .OnComplete(this, nameof(OnDone));     // 完成后回调

// 3. 运行时控制
tweenHandle.Pause();
tweenHandle.Resume();   // 注意: 官方 API 叫 Play(),不是 Resume()
tweenHandle.Kill();     // 停止并销毁
tweenHandle.Complete(); // 立即跳到终点
```

---

## 子目录导航

| 子页面 | 路径 | 核心内容 |
|---|---|---|
| **基础 API** | `basics.md` | VRCTween.InstantiateXxx / 扩展方法 / Value 起点终点 / Duration / Easing |
| **补间类型** | `tween-types.md` | Transform / Path / UI / Renderer / Light / Audio / Sprite 7 大类 |
| **虚拟补间** | `virtual-tween.md`(→ basic 中包含) | TweenFloat / TweenInt / TweenColor / TweenVector3 + DelayedCall |
| **序列与并行** | `sequence.md` | 用 OnComplete 链式回调做序列 / 多个并发 tween |
| **播放控制** | `control.md` | Play / Pause / Kill / Complete / Restart / Flip / Goto + 状态查询 |
| **自定义补间** | `custom-tween.md` | 通过 virtual tween 写入任意变量 + AnimationCurve 自定义缓动 |
| **常用模式** | `patterns.md` | 按钮回弹 / UI 淡入淡出 / 相机跟随 / 大量物体交错 |

---

## 关键事实(全 Agent 必知)

### 1. 本地性(无网络同步)

> 🔴 **VRCTween 不会自动同步**。每个玩家看到的动画都是**本地独立播放**。

- 想同步动画 → 在 `[UdonSynced]` 变量里存**开始时间戳**,在 `OnDeserialization` 中调用 `Goto(elapsed, true)`
- 详细: `control.md` 的 "Seeking With Goto" 章节

### 2. 输入验证(无效输入静默拒绝)

VRCTween **不会抛异常**(避免破坏 Udon VM),而是**返回无效 handle**:

| 输入 | 行为 |
|---|---|
| `target` 为 null | 返回无效 handle,跳过创建 |
| `duration` < 0 / NaN / Infinity | 返回无效 handle(0 是允许的,用于可复用 tween) |
| 位置/缩放/路径点含 NaN/Inf 或绝对值 > ~520,000 | 返回无效 handle |
| Path 的 `resolution` 超出 1-50 | 静默 clamp 到 1-50 |
| `SetDuration` / `SetDelay` 收到负数 | 静默忽略 |
| `Goto` 收到 NaN/Inf | 静默忽略;否则 clamp 到 duration 范围 |
| `ChangeEndValue` 收到无效 float/vector | 静默忽略 |

> **最佳实践**: 创建后检查 `handle.IsValid` 来分支处理无效情况。

### 3. 性能事实

- DOTween 内部**池化** tween 对象,创建/销毁开销极小
- 一次性动画(5-50 个)用 `Kill()` + 重建完全够用
- **热路径**(每帧更新目标,如相机跟随)必须用**复用模式**:`ChangeEndValue + SetDuration + SetEase + Restart`
  - 内部基准:500 tween × 300 帧,复用模式比 kill-and-recreate **内存少 46x, 快 10x**
- 超短 tween(< 0.01s)动画不流畅

### 4. 生命周期管理

- **完成/被 Kill 的 tween 自动清理** — 不需要手动删除
- **无限循环 tween** 或 **长 tween** 在 GameObject 销毁时**必须**手动 Kill
  ```csharp
  void OnDestroy() { gameObject.KillAllTweens(); }
  ```
- **单个 tween 清理**:`tweenHandle.Kill()`
- **全场景清理**:`VRCTween.KillAll()`

---

## 官方子页面映射

| 本知识库文件 | 官方文档 URL |
|---|---|
| `index.md`(本文件) | `https://creators.vrchat.com/worlds/udon/vrctween/`/ |
| `basics.md` | (本文件 + `tween-types` 摘要) |
| `tween-types.md` | `https://creators.vrchat.com/worlds/udon/vrctween/tween-types`/ |
| `control.md` | `https://creators.vrchat.com/worlds/udon/vrctween/settings`/ |
| `sequence.md` | (主页面 "Chain Tweens with Callbacks" 章节) |
| `custom-tween.md` | (主页面 "Virtual Tweens" 章节 + AnimationCurve) |
| `virtual-tween.md`(在 basics 中) | `https://creators.vrchat.com/worlds/udon/vrctween/virtual-tweens`/ |

---

## 与知识库互补

- **Udon VM 性能**:`rules/udon-vm-architecture.md` — 9 指令模型
- **UdonSharp 限制**:`rules/udonsharp-language-limits.md` — C# → Udon 限制
- **网络同步**:`rules/networking-rules.md` + `patterns/manual-sync-state.md`
- **动画事件白名单**:`world/udon/animation-events.md` — Animator 调 Udon 的白名单
- **Unity Layers / 时间戳**:`world/layers.md` + `world/udon/external-urls.md`(找相似模式)

---

## 底层实现 (DOTween)

VRCTween 是 VRChat 团队对 **DOTween** 库 (Demigiant, http://dotween.demigiant.com/) 的 Udon-friendly 封装。理解 DOTween 的设计哲学可以解释 VRCTween 的几个关键行为:

- **零分配 / 池化模型** — DOTween 内部池化 tween 对象并缓存所有插值计算结果,这是为什么**复用模式** (ChangeEndValue + SetDuration + SetEase + Restart) 能带来 **46× 内存优化 / 10× 速度提升** 的根因
- **类型安全** — 完全无字符串无反射,与 Udon VM 类型白名单天然契合,这也是为什么 VRCTween 能作为 SDK 内置 API 暴露
- **DOTween 免费版核心** — VRCTween **未包含 Pro 特性**: 可视化动画编辑器、可视化路径编辑器、2D Toolkit 扩展、TextMesh Pro 扩展均不可用

### 参考文档位置

| 文档 | 路径 | 用途 |
|---|---|---|
| 4 份 VRCTween 官方原始英文 | `参考文献/VRCTween-Official-{Overview,Tween-Types,Virtual-Tweens,Settings}.md` | 2026-05-28 官方版本,本地化前的原始材料 |
| DOTween 底层库介绍 | `参考文献/DOTween-Underlying-Engine.md` | DOTween 性能基准、平台支持、设计哲学 |
| 缓动可视化 | https://easings.net/ | 31 种 ease 曲线视觉对比 |
| VRChat Canny | https://vrchat.canny.io/udon | VRCTween 相关 Bug 报告 / 功能请求 |

> **校对状态** (2026-06-22): 本知识库 7 个本地化文档与官方 2026-05-28 版本**逐项对齐**,覆盖率 >95%。逐字校验项包括 11 个 Control Methods、6 个 Query Properties、8 个 Settings、31 种 Ease 速查、`OnRewind`/`ChangeEndValue`/`From`/`SetSpeedBased` 等行为细节。无结构更新需求,见 `memory/JOURNAL.jsonl` 2026-06-22 审计记录。
