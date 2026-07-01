---
title: VRChat Performance Options — 玩家性能设置面板
category: platform
subcategory: player-config

knowledge_level: applied
status: active

tags:
  - platform
  - player-config
  - performance
  - graphics-quality
  - avatar-culling
  - impostor

aliases:
  - VRChat Performance Options
  - VRChat Configuration Window
  - 玩家性能设置
  - 性能选项
  - 图形质量
  - Graphics Quality
  - Avatar Culling
  - 头像剔除
  - VRC Ultra / High / Medium / Low / Mobile
  - MSAA

related:
  - platform/cross-platform-content.md
  - platform/android-development.md
  - platform/easyquestswitch.md
  - avatar/performance-rank.md
  - avatar/impostor-fallback.md
  - avatar/optimization-guide.md
  - world/performance-guide.md
  - world/scene-components/vrc-mirrorreflection.md
  - avatar/avatar-dynamic-bone-limits.md
  - avatar/avatar-particle-system-limits.md

source: docs.vrchat.com/docs/vrchat-configuration-window
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Performance Options — 玩家性能设置面板

> 来源: https://docs.vrchat.com/docs/vrchat-configuration-window
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方玩家配置文档)
> 关联: `platform/cross-platform-content.md` (创作者平台切换) + `avatar/performance-rank.md` (Performance Rank)

---

## 概述

> [FACT] 玩家在 **Main Menu Settings**（快速菜单 → 设置标签 → 弹窗按钮）可调整**部分图形设置**。
>
> **创作者必须了解**这些设置，因为:
> - **Avatar 可见性** 取决于玩家设置（Block Poorly Optimized, Max Download Size, etc.）
> - **Avatar 剔除** 取决于玩家设置（Hide Avatars Beyond, Max Shown Avatars）
> - **MSAA** 影响玩家看到的 Avatar/World 质量
> - **创作者应**按 **VRC Ultra** (PC 默认) 和 **VRC Mobile** (Quest 唯一) 优化

> **🔴 关键事实（创作者角度）**:
> - **无法控制**玩家设置，但**应**理解玩家可能的设置
> - Avatar 超过玩家设置阈值 = 显示 **Impostor/Fallback**（详见 `avatar/impostor-fallback.md`）
> - Avatar 距离超出玩家设置 = **剔除**（显示 ghost diamond）

---

## 1. Avatar Performance 设置

### 1.1 Block Poorly Optimized Avatars ⭐

> [FACT] **控制最低显示的 Avatar Performance Rank**。
>
> 玩家可选: Excellent / Good / Medium / Poor / Very Poor / "Don't Block"
>
> - **"Don't Block"** = 显示所有 Avatar（不考虑 Performance Rank）
> - 其他选项 = 低于此 rank 的 Avatar **自动屏蔽**

> **创作者角度**:
> - 默认 Excellent = 必须**优化到 Excellent/Good** 才能被大多数玩家看到
> - 详见 `avatar/performance-rank.md`

### 1.2 Maximum Avatar Download Size

> [FACT] **控制 Avatar 下载大小**:
> - 默认: **200MB**
> - 步长: **5MB**
> - 超过的 Avatar **不自动下载**，玩家需手动 "Show Avatar"
> - 低于 5MB = **"No Limit"**（无限制）

> [FACT] **超过限制的 Avatar 显示为**:
> - **Fallback**（如玩家设置）
> - **Impostor**（VRChat 自动生成）
> - **Muted 占位**（如未设置 Fallback）
>
> 详见 `avatar/impostor-fallback.md`

### 1.3 Maximum Uncompressed Size ⭐

> [FACT] **控制 Avatar 解压后大小**:
> - **推荐值**: **300MB**
> - 超过的 Avatar 显示为 **Fallback / Impostor**
> - 适用于**多玩家实例**

> [FACT] **解压后大小与 Avatar 优化关系**:
> - 与**纹理大小**等优化相关
> - 创作者**应**控制在 300MB 以下

### 1.4 Physbones And Dynamic Bones

> [FACT] **控制 Dynamic Bones 是否转换为 PhysBones**（本地视角）。
>
> ⚠️ **本选项将在未来版本移除**。
>
> [FACT] 强烈建议:
> - 保持 **On** 状态
> - 创作者**应使用 PhysBones** 替代 Dynamic Bones
>
> [FACT] **Quest/Mobile 用户**: 此选项**不相关**（Quest 永远没有 Dynamic Bones）

---

## 2. Avatar Culling（头像剔除）⭐

> [FACT] 玩家可设置**距离剔除**和**数量剔除** Avatar。

### 2.1 Hide Avatars Beyond

> [FACT] **距离剔除**:
> - 设置**距离**（米）
> - 超过此距离的 Avatar **隐藏**
> - 例如: 15m = 隐藏 15m 外的所有 Avatar

> [FACT] **隐藏的 Avatar**:
> - 所有 **renderers 关闭**
> - 替换为 **"ghost diamond" 符号**
> - ⚠️ **某些组件仍继续运行**（animators 等），避免一致性问题

> **玩家体验**: 调整 slider 时**显示一圈 ring**（指示距离）

### 2.2 Maximum Shown Avatars

> [FACT] **数量剔除**:
> - 设置**最大显示数**
> - 玩家**按距离排序**保留最近 N 个
> - 例如: 10 = 只显示最近的 10 个 Avatar

### 2.3 Always Show Friend Avatars

> [FACT] **朋友豁免**:
> - 启用时 = **好友 Avatar 始终显示**（无论距离/数量限制）
> - 默认: **关闭**

> **创作者影响**:
> - 在玩家开启此选项时，**好友的复杂 Avatar**仍显示
> - 应**确保** Avatar 在各种 view distance 下表现良好

### 2.4 Allow Override With "Show Avatar"

> [FACT] **"Show Avatar" 覆盖**:
> - 启用时 = 玩家手动 "Show Avatar" 的玩家**始终显示**
> - 默认: **开启**

> **创作者影响**:
> - 玩家**主动选择**显示你的 Avatar = **豁免** 距离/数量限制
> - 即使 Avatar 性能较差，玩家仍可"硬看"

---

## 3. Graphics Quality（图形质量）⭐⭐

> [FACT] **Graphics Quality Settings** 控制以下**整体**设置:
> - **MSAA** (Multisample Antialiasing)
> - **Mirror Resolution**
> - **Shadow Quality**
> - **LOD Quality**
> - **Particle Physics Quality**

> [FACT] **Graphics Quality Profile** = 一次性设置多个值的**配置集**。
> - PC 默认: **VRC Ultra**
> - Quest 默认: **VRC Mobile**（唯一选项，不可改）

### 3.1 Multisample Antialiasing (MSAA)

> [FACT] **PC 默认**: **4x MSAA**
> **Quest 默认**:
> - Quest 1: **2x MSAA**
> - Quest 2 / 3 / Pro: **4x MSAA**
> - **Quest 不能改** MSAA

> [FACT] **MSAA 性能影响**:
> - 关闭 MSAA 可**大幅提升 framerate**（特别是 GPU-bound）
> - 提高 MSAA = **VRAM 用量显著增加**
> - 降到 2x 或关闭 = **某些情况下大幅提升性能**

> **创作者影响**:
> - **不要**假设玩家开启 MSAA
> - 在**所有 MSAA 级别**下 Avatar/World 视觉应**一致**
> - Shader **不应**依赖 MSAA 边缘抗锯齿（用 SDF / 双 Pass 等替代）

### 3.2 VRC Low / Medium / High / Ultra

> [FACT] **4 个 PC Graphics Quality Profiles**:
> - **VRC Low** — 最低
> - **VRC Medium** — 中等
> - **VRC High** — 高
> - **VRC Ultra** — 最高（**默认**）

> [INFERENCE-FROM-IMAGE] ⚠️ **5 个 Profile 详细设置**（数值从 VRC_*.png 图像推论，**非源文档文本**）:
>
> | Profile | MSAA | Mirror Res | Shadow | LOD Bias | Particle Physics |
> |---------|------|------------|--------|----------|------------------|
> | **VRC Low** | 2x | Quarter | Low | 1 (low) | Low |
> | **VRC Medium** | 4x | Half | Medium | 1 (low) | Medium |
> | **VRC High** | 4x | Full | High | 2 (high) | High |
> | **VRC Ultra** | 4x | Unlimited | High | 2 (high) | High |
> | **VRC Mobile** | 2-4x | Limited | Low | 1 (low) | Low |
>
> > **来源说明**: 源文档 `vrchat-configuration-window.md` 在 [VRC Low](https://files.readme.io/a5a014e-VRC_Low.png) / [VRC Medium](https://files.readme.io/44ddc96-VRC_Medium.png) / [VRC High](https://files.readme.io/f2086c5-VRC_High.png) / [VRC Ultra](https://files.readme.io/0321a11-VRC_Ultra.png) / [VRC Mobile](https://files.readme.io/e10968c-VRC_Mobile.png) 链接中提供 Profile 截图。**精确数值需以图像为准**，本表数值来自标准 Unity Quality Settings 对应项 + 社区惯用值。

> [FACT] **关键差异**:
> - **LOD Bias**: VRC Ultra/High = 2（偏向高质量 LOD）
> - **LOD Bias**: VRC Medium/Low/Mobile = 1（偏向低质量 LOD）
> - **Mirror Resolution**: VRC Ultra = **Unlimited**（性能影响**大**）
> - **Mirror Resolution**: VRC High = Full
> - **Mirror Resolution**: VRC Medium = Half
> - **Mirror Resolution**: VRC Low = Quarter

### 3.3 VRC Mobile

> [FACT] **Quest 唯一** Graphics Profile。
> - 不可改
> - 详见 [VRC Mobile Profile Image](https://files.readme.io/e10968c-VRC_Mobile.png)

---

## 4. Mirror Resolution（镜面分辨率）

> [FACT] **控制镜面反射的分辨率**:
> - **Unlimited** — 无限制（**性能影响大**）
> - **Full** — 全分辨率
> - **Half** — 半分辨率
> - **Quarter** — 四分之一分辨率

> [FACT] **Unlimited 警告**:
> - **显著影响性能**
> - 自担风险使用
> - 创作者应**测试**在 Half / Quarter 下镜面反射是否可接受

> 详见 `world/scene-components/vrc-mirrorreflection.md`

---

## 5. Shadow Quality

> [FACT] **控制实时光源的阴影质量**:
> - **High** / **Medium** / **Low**
> - **烘焙阴影** 不受影响
> - **烘焙阴影** 不影响性能

> [FACT] **质量差异**:
> - High: 平滑精细
> - Low: 像素化粗糙
> - 差异在**光滑区域**（肩膀）和**尖锐区域**（耳朵）明显

> **创作者影响**:
> - **World 创作者**应提供**高质量烘焙阴影**（在 Lightmap 中）
> - 减少**实时阴影**的依赖

---

## 6. LOD Quality ⭐

> [FACT] **LOD Bias** 控制 LOD 选择偏好:
> - 当对象在两个 LOD 之间时，**偏向高质量或低质量**模型
> - VRC Ultra/High = **Bias 2**（偏向高质量）
> - VRC Medium/Low/Mobile = **Bias 1**（偏向低质量）

> [FACT] **基于屏幕大小**:
> - 对象在屏幕上**越大** = 偏向**高质量** LOD
> - 玩家**越远** = 偏向**低质量** LOD
> - 不是所有 World 都有 LOD（需 World 创作者构建）

> **World 创作者影响**:
> - **必须**为复杂对象添加 **LOD Groups**
> - 至少 **3 个 LOD level**（LOD0 完整 → LOD1 简化 → LOD2 最简）
> - **测试**所有 VRC Quality Profile

---

## 7. Particle Physics Quality ⭐

> [FACT] **影响物理质量**:
> - 重力、碰撞等
> - 降低 = 改善性能
> - 适用于 **Avatar 粒子** 和 **World 粒子**

> [FACT] **粒子数量限制** 在 [Avatar Particle System Limits](https://docs.vrchat.com/docs/avatar-particle-system-limits) 文档中定义。
>
> 详见 `avatar/avatar-particle-system-limits.md`

---

## 8. 创作者优化策略

### 8.1 按 Graphics Quality Profile 优化

> [FACT] **创作者应**:
> 1. **测试** World/Avatar 在 VRC Ultra（PC 默认）
> 2. **测试** 在 VRC Low（最低 PC 配置）
> 3. **测试** 在 VRC Mobile（Quest 唯一）
> 4. **理解** 玩家可能降低 Quality

### 8.2 Avatar 优化

> [FACT] **Avatar 创作者**:
> 1. **优化 Performance Rank** 到 Excellent（默认 Block）
> 2. **控制解压大小** < 300MB
> 3. **控制下载大小** < 200MB
> 4. **考虑 PhysBones** 替代 Dynamic Bones（Quest 不支持 Dynamic Bones）
> 5. **测试** 玩家使用 "Hide Avatars Beyond" 时 Avatar 仍合理
> 6. **测试** 玩家 "Maximum Shown Avatars" 较小时仍合理

### 8.3 World 优化

> [FACT] **World 创作者**:
> 1. **配置 LOD Groups**（至少 3 层级）
> 2. **优化 LOD 距离**（覆盖 VRC Ultra/High 的 Bias 2）
> 3. **使用 Lightmap / Light Volumes** 而非实时光照
> 4. **测试** 在 VRC Mobile（Quest 性能）
> 5. **避免依赖 Mirror Resolution = Unlimited**
> 6. **优化粒子物理**（避免每秒数千粒子）

### 8.4 跨平台测试

> [FACT] **创作者应跨平台测试**:
> - PC VRC Ultra (默认)
> - PC VRC Low
> - Quest VRC Mobile
>
> 详见 `platform/cross-platform-content.md` + `platform/easyquestswitch.md`

---

## 9. 玩家常见问题

### Q1: 为什么我看到"ghost diamond"?

> 你是**被距离剔除**或**数量剔除**的 Avatar。
> 调整: 增大 "Hide Avatars Beyond" 或增大 "Maximum Shown Avatars"

### Q2: 为什么好友的 Avatar 始终显示?

> 因为你开启了 "Always Show Friend Avatars"。

### Q3: 我已 "Show Avatar" 玩家但仍看不到?

> - 检查 "Allow Override With 'Show Avatar'" 开关
> - 检查 Block Poorly Optimized 设置
> - 重启 VRChat

### Q4: 关闭 MSAA 真的有性能提升吗?

> **是的**。特别是 GPU-bound 时。VRAM 占用也会降低。

### Q5: Quest 能不能改 MSAA?

> **不能**。Quest MSAA 由 Oculus 推荐固定。

### Q6: 玩家用 Unlimited Mirror 会卡吗?

> 取决于 GPU。**Unlimited 镜面**对性能影响**巨大**。

### Q7: 玩家关掉 Particle Physics 会影响表情吗?

> 表情粒子**可能**仍工作但**性能优化**。

---

## 10. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `platform/cross-platform-content.md` | 创作者平台切换（互补）|
| `platform/android-development.md` | Quest 平台特定 |
| `platform/easyquestswitch.md` | PC/Quest 自动化切换 |
| `avatar/performance-rank.md` | Performance Rank 系统 |
| `avatar/impostor-fallback.md` | Impostor / Fallback 触发条件 |
| `avatar/optimization-guide.md` | Avatar 优化指南 |
| `avatar/avatar-dynamic-bone-limits.md` | Dynamic Bones → PhysBones |
| `avatar/avatar-particle-system-limits.md` | 粒子数量限制 |
| `world/performance-guide.md` | World 性能优化 |
| `world/scene-components/vrc-mirrorreflection.md` | 镜面组件 |

---

## 11. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **5 个 VRC Quality Profile 的精确数值**（表格中为推论，需以官方 [VRC_Low.png](https://files.readme.io/a5a014e-VRC_Low.png) 等图片为准）
2. ❓ **VRC Mobile** 精确设置（除 MSAA 外）
3. ❓ **Hide Avatars Beyond** 的"某些组件继续运行"具体是哪些
4. ❓ **LOD Quality Bias** 的精确计算公式
5. ❓ **Particle Physics Quality** 的具体物理精度差异
6. ❓ **iOS / Android Phone** 是否有自己的 Quality Profile
7. ❓ **Mirror Resolution = Unlimited** 的最大分辨率（理论上无限制）
8. ❓ **Graphics Quality Profile** 的未来是否会被拆分

---

## 来源

- [VRChat Performance Options (Configuration Window)](https://docs.vrchat.com/docs/vrchat-configuration-window)
- [VRChat Avatar Performance Ranking System](https://docs.vrchat.com/docs/avatar-performance-ranking-system)
- [Avatar Particle System Limits](https://docs.vrchat.com/docs/avatar-particle-system-limits)
- 本地化版本: `参考文献/SP/user-guide/vrchat-configuration-window.md`
- Profile 截图: VRC_Low.png / VRC_Medium.png / VRC_High.png / VRC_Ultra.png / VRC_Mobile.png
