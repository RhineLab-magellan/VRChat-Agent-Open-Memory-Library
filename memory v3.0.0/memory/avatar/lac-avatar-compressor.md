---
title: "Avatar Compressor (LAC)"
category: avatar
knowledge_level: applied
status: active
source: "github.com/limitex/avatar-compressor"
source_type: community
version: 1.0
upstream_version: "v0.8.0 (2026-05-01)"
last_review: 2026-06-21
confidence: Medium
tags:
  - avatar
  - animator
  - physbone
  - optimization
aliases:
  - "Avatar Compressor (LAC)"
  - lac-avatar-compressor
related:
  - "avatar/ndmf-tools.md"
  - "avatar/optimization-guide.md"
  - "avatar/performance-rank.md"
  - "platform/android-development.md"
  - "platform/easyquestswitch.md"
  - "avatar/modular-avatar.md"
---
# Avatar Compressor (LAC)

> 工具名: Limitex Avatar Compressor (LAC) | 来源: github.com/limitex/avatar-compressor
> 当前版本: **v0.8.0** (2026-05-01)
> 置信度: High (官方仓库)
> 语言占比: C# 87.1% / MDX 6.3% / TypeScript 4.3% / HLSL 2.3%

---

## 工具定位

**Avatar Compressor** 是 VRChat Avatar 非破坏性压缩工具，**全自动分析并压缩 Avatar 纹理**，解决"手动逐张调整贴图 Max Size / Compression"的痛点。

| 维度 | 说明 |
|------|------|
| **设计目标** | 让更多玩家能看见你的 Avatar（降低性能等级门槛） |
| **核心场景** | Texture Memory 优化（VRAM 压缩） |
| **非目标** | Mesh/Bone/Animator/PhysBone 优化（这些归 AAO） |
| **互补关系** | 与 Avatar Optimizer (AAO) 互补使用（LAC 处理贴图，AAO 处理几何） |

> 💡 **设计哲学**：LAC 与 AAO 是**互补而非竞争**关系。AAO 不处理贴图压缩（其 Trace & Optimize 主要处理 Skinned Mesh / Bone / PhysBone），LAC 专门处理 Texture Memory 维度。

---

## 核心特性

### Texture Compressor（核心功能）

**全自动贴图分析 + 压缩 + 平台分流**

| 特性 | 说明 |
|------|------|
| **Complexity-based analysis** | 根据贴图视觉复杂度动态选择压缩等级（而非一刀切） |
| **Multiple analysis strategies** | 4 种分析策略：Fast / HighAccuracy / Perceptual / Combined |
| **Preset configurations** | 5 个内置预设，开箱即用 |
| **Texture type awareness** | 区分 Normal Map / Emission Map 等类型（不同类型用不同算法） |
| **Platform-specific formats** | PC 自动选 BC 系列 / Quest 自动选 ASTC 系列 |
| **High-quality compression** | 高复杂度贴图自动使用 BC7 / ASTC_4x4 |
| **Memory estimation** | 编译前预览估算 VRAM 使用量 |
| **Shared texture optimization** | 共享贴图识别，仅处理一次，多处复用 |

### 与手动设置对比

| 维度 | 手动（传统方式） | LAC（自动） |
|------|------------------|-------------|
| **每张贴图设置** | 逐张调整 Max Size + Compression | 全自动 |
| **复杂度判断** | 凭眼睛/经验 | 算法分析 |
| **平台格式** | 手动切换 PC/Quest | 自动选择 |
| **共享贴图** | 容易重复处理 | 自动识别合并 |
| **VRAM 预估** | 无 | 编译前可见 |
| **适用人群** | 有经验的创作者 | 所有等级 |

---

## 系统要求

| 项目 | 版本 |
|------|------|
| **Unity** | 2022.3.22f1（VRChat 指定版本） |
| **VRChat SDK Avatars** | 3.10.0+ |
| **NDMF** | 1.10.0+ |
| **运行时框架** | Non-Destructive Modular Framework（随 MA 自动安装） |

---

## 安装方式

### 方式 1: ALCOM（推荐）

```
1. 打开 ALCOM
2. 添加仓库: https://vpm.limitex.dev/
3. 在项目里添加 Avatar Compressor
```

### 方式 2: VRChat Creator Companion

```
1. 打开 VCC
2. 添加仓库: https://vpm.limitex.dev/
3. 在项目里添加 Avatar Compressor
```

### 方式 3: 手动安装

```
从 GitHub Releases 下载最新 .zip
直接导入 Unity 项目
```

**VPM 仓库链接**:
```
https://vpm.limitex.dev/
```

---

## 使用方法

### 基本流程

```
1. 在 Avatar 根 GameObject 上添加 LAC 优化组件
2. 选择预设（5 个内置预设之一）
3. 选择分析策略（Fast / HighAccuracy / Perceptual / Combined）
4. 构建 Avatar
5. NDMF 管线自动在编译时应用所有优化
```

### 核心设计原则

> 所有优化在**编译时**通过 NDMF 自动应用，**原始文件不被修改**（非破坏性）

这意味着：
- 可以随时调整 LAC 设置重新构建
- 原始 .fbx / .png 永远保留原始状态
- 与 Modular Avatar 等其他 NDMF 工具完美兼容

---

## 与 AAO 的协作关系

### 官方推荐组合

> **官方原话**：For best results, we recommend using this tool together with Avatar Optimizer (AAO). Avatar Optimizer provides additional optimization features such as mesh merging, bone reduction, and more.

### 职责分工

| 工具 | 负责领域 | 不负责 |
|------|----------|--------|
| **LAC** | Texture Memory（贴图压缩/VRAM） | Mesh / Bone / PhysBone |
| **AAO** | Mesh / Bone / PhysBone / Animator | Texture Memory（不处理贴图压缩） |

### 关键执行顺序

> ⚠️ **LAC 在 AAO 之前运行**（保证其他优化在最佳贴图压缩基础上）

```
NDMF Pipeline 执行顺序:
1. LAC（Avatar Compressor）        ← 先压缩贴图
2. AAO（Trace And Optimize）        ← 再合并 Mesh / 删 Bone
3. 其他 NDMF 工具                  ← 在最优基础上继续优化
```

**为什么这个顺序很重要**:
- AAO 的 Merge Skinned Mesh 会基于当前贴图状态做决策
- 如果先合并 Mesh 再压缩贴图，可能错过"共享贴图识别"的优化机会
- 先压缩贴图可以让后续工具看到"真实优化后"的状态

---

## 与 NDMF 生态其他工具的关系

| 工具 | 互补/重叠 | 说明 |
|------|-----------|------|
| **Modular Avatar (MA)** | 互补 | MA 是 NDMF 框架基础，LAC 跑在 MA 之上 |
| **Avatar Optimizer (AAO)** | 互补 | LAC 处理贴图，AAO 处理几何（见上节） |
| **TexTransTool (TTT)** | 部分重叠 | TTT 做 Atlas 化（合并贴图），LAC 做单贴图压缩 |
| **lilAvatarUtils** | 无重叠 | lilAvatarUtils 是性能检测工具，不修改资源 |
| **lilNDMFMeshSimplifier** | 无重叠 | 减面工具，不涉及贴图 |

### 与 TexTransTool 的边界

```
TexTransTool:
  - 把多张贴图合成一张（Atlas 化）
  - 减少 Material Slot 数量
  - 适合：材质球数量过多的情况

Avatar Compressor (LAC):
  - 优化单张贴图的压缩格式与分辨率
  - 减少 VRAM 使用量
  - 适合：贴图体积过大/格式不当的情况
```

> 💡 **实务建议**：先跑 LAC 压缩单贴图，再用 TTT 做 Atlas 化（顺序：单图压缩 → Atlas 合并）

---

## 分析策略详解（4 种）

| 策略 | 速度 | 精度 | 适用场景 |
|------|------|------|----------|
| **Fast** | ⚡ 最快 | 较低 | 大批量 Avatar 初步优化 |
| **HighAccuracy** | 慢 | ⭐ 最高 | 最终发布前的精细优化 |
| **Perceptual** | 中 | 高（基于人眼视觉） | 强调视觉质量的场景 |
| **Combined** | 中 | 综合最优 | 默认推荐（多策略融合） |

**Combined 模式原理**【推断】:
- 综合多种分析维度的结果
- 取视觉/性能/质量的平衡点
- 适合绝大多数场景

---

## 平台格式自动选择

### PC 平台

| 复杂度 | 推荐格式 | 说明 |
|--------|----------|------|
| **低复杂度**（纯色/简单渐变） | BC1 (DXT1) | 4 bpp，最快 |
| **中复杂度** | BC3 (DXT5) | 8 bpp，带 Alpha |
| **高复杂度**（细节丰富） | BC7 | 8 bpp，最高画质 |

### Quest 平台

| 复杂度 | 推荐格式 | 说明 |
|--------|----------|------|
| **低复杂度** | ASTC_6x6 | 3.56 bpp，省 VRAM |
| **中复杂度** | ASTC_5x5 | 4.80 bpp |
| **高复杂度** | ASTC_4x4 | 8.00 bpp，最高画质 |

> ⚠️ Quest 平台严禁使用 DXT/BC 系列（详见 `memory/platform/android-development.md`）

---

## Texture Type Awareness（类型感知）

LAC 自动识别贴图类型并应用不同压缩策略：

| 贴图类型 | 处理要点 |
|----------|----------|
| **Albedo/Diffuse** | 标准压缩，重点保留色彩 |
| **Normal Map** | 特殊算法（保留法线方向），不能简单 RGB 压缩 |
| **Emission Map** | 保留高光细节，可能用更高精度 |
| **Metallic/Roughness** | 单通道优化，可极低精度 |
| **Occlusion Map** | 单通道优化 |
| **Mask Map** | 多通道打包优化 |

> 传统手动设置容易把 Normal Map 当成 Albedo 处理，破坏法线方向。LAC 的自动识别避免此问题。

---

## 性能等级提升预估（参考）

| 原始 Avatar | 应用 LAC 后（典型） |
|-------------|---------------------|
| Very Poor (150MB+ VRAM) | Good (75MB 以下) |
| Poor (150MB VRAM) | Medium → Good |
| Medium (110MB VRAM) | Good → Excellent |
| Good (75MB VRAM) | Excellent（基本到顶） |

> 💡 实际效果取决于原始贴图的"压缩浪费程度"。如果原始贴图本身就是 2048x2048 + RGBA32 + Uncompressed，压缩空间巨大。

---

## 与现有知识的关系

### 解决的痛点（optimization-guide.md Texture Memory 节）

传统 `optimization-guide.md` 中"Texture Memory"章节要求：
- 手动设置每张贴图 Max Size
- 手动选择 Compression 格式
- 手动区分 PC/Quest 平台

**LAC 自动化了以上全部步骤**，是 Texture Memory 优化章节的最佳实践补充。

### 与 performance-rank.md 关系

LAC 直接改善 `memory/avatar/performance-rank.md` 中的 **Texture Memory** 指标（PC < 75MB Good / < 40MB Excellent）。

---

## 限制与注意事项

| 限制 | 说明 |
|------|------|
| **依赖 NDMF 框架** | 必须先安装 Modular Avatar 或 NDMF 核心 |
| **依赖 VRChat SDK 3.10+** | 旧版 SDK 不兼容 |
| **不处理几何** | Mesh/Bone/PhysBone 优化仍需 AAO |
| **不处理材质球合并** | Material Slot 优化仍需 TexTransTool |
| **需要 Unity 2022.3.22f1** | 与 VRChat 强制版本绑定（详见 `memory/_always-load.md` 核心约束） |

---

## 推荐 Avatar 优化组合技（2026 更新版）

```
完整 NDMF 最佳化流水线（推荐顺序）:

1. Modular Avatar（穿脱服装、菜单系统）
2. Avatar Compressor（LAC）        ← 2026 新增:自动纹理压缩
3. Avatar Optimizer (AAO)            ← 合并 Mesh/Bone/PhysBone
4. TexTransTool (TTT)                ← Atlas 化（材质球合并）
5. lilNDMFMeshSimplifier / Meshia    ← 减面（按需）
6. Continuous Avatar Uploader        ← 批量上传

VPM 一键安装清单（更新版）:
- Modular Avatar
- Avatar Compressor (LAC)            ← 2026 新增
- Avatar Optimizer (AAO)
- TexTransTool
- lilNDMFMeshSimplifier
- Meshia Mesh Simplification
```

---

## 版本历史

| 版本 | 日期 | 关键变化 |
|------|------|----------|
| **v0.7.0** | 2025-12 ~ 2026-04 | 稳定版（5 种内置预设 + 4 种分析策略） |
| **v0.8.0** | 2026-05-01 | **当前版本** — ObjectRegistry 解析原始资产路径、未知 Shader 属性数据保护、按 GUID 排除特定贴图、GPU 加速纹理分析（Compute Shader）、Frozen/Preview 独立搜索框 |

---

## 相关文档

- `memory/avatar/ndmf-tools.md` — NDMF 工具生态总览（LAC 在 AAO 之前执行）
- `memory/avatar/optimization-guide.md` — Texture Memory 优化原则（LAC 自动化了这些原则）
- `memory/avatar/performance-rank.md` — 性能等级标准（LAC 主要改善 Texture Memory 指标）
- `memory/platform/android-development.md` — Quest 平台贴图格式限制
- `memory/platform/easyquestswitch.md` — PC/Quest 平台切换工具
- `memory/avatar/modular-avatar.md` — NDMF 框架基础

---

## 工具元信息

| 项目 | 值 |
|------|-----|
| 仓库 | github.com/limitex/avatar-compressor |
| 文档站 | lac.limitex.dev |