---
title: NDMF 工具生态体系
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - physbone
  - json
  - modular-avatar

aliases:
  - "NDMF 工具生态体系"

related:
  - performance-rank.md
  - optimization-guide.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# NDMF 工具生态体系

> 来源: Kuriko Avatar 最佳化笔记
> 置信度: High

---

## 什么是 NDMF

**NDMF (Non-Destructive Modular Framework)** 是一种非破坏性最佳化框架。

| 特性 | 说明 |
|------|------|
| **非破坏性** | 原始文件完整保留，最佳化仅在编译时生效 |
| **组件化** | 每个优化步骤是独立组件，便于组合 |
| **MA 依赖** | 大部分工具依赖 Modular Avatar 运行 |
| **可叠加** | 可以多个工具组合使用（组合技）|

> 💡 NDMF 体系的工具，最佳化不会破坏原始档案，且支援用 Modular Avatar 穿的衣服

---

## 工具一览

### 核心依赖

| 工具 | VPM 链接 | 说明 |
|------|----------|------|
| **Modular Avatar (MA)** | `vcc://vpm/addRepo?url=https://vpm.nadena.dev/vpm.json` | 必装，NDMF 核心 |
| **Non-Destructive Modular Framework** | 随 MA 自动安装 | NDMF 基础框架 |

### 最佳化工具

| 工具 | VPM 链接 | 价格 | 主要功能 |
|------|----------|------|----------|
| **Avatar Compressor (LAC)** ⭐NEW 2026-06-17 | `https://vpm.limitex.dev/` | 免费 | **全自动纹理压缩**（复杂度感知 + 平台自动 + VRAM 预估 + 类型感知）。详见 `lac-avatar-compressor.md` |
| **AvatarOptimizer (AAO)** | `https://vpm.anatawa12.com/add-repo` | 免费 | 合并 Skinned Mesh/Bones/PhysBone、Remove Mesh、各类最佳化 |
| **lilAvatarUtils** | 随 AAO repo | 免费 | 性能检测（贴图/材质/动画/Skinned Mesh/PhysBone/光照等） |
| **TexTransTool** | `vcc://vpm/addRepo?url=https://vpm.rs64.net/vpm.json` | 免费 | 材质球 Atlas 化（合并贴图）— 详见 `tex-trans-tool.md` |
| **MA2BT** ⭐NEW 2026-06-17 | `https://null-k.github.io/vpm-listing/index` | 免费 | **MA 响应式层合并优化**：将 `MA Responsive:*` 层压缩为单一 Direct BlendTree，减少 FX 层数与空动画。详见 `ma2bt.md` |

### 减面工具

| 工具 | VPM 链接 | 价格 | 优点 | 缺点 | 状态 |
|------|----------|------|------|------|------|
| **Mantis LOD Editor** | Unity Asset Store | **$50** | 模型不易破洞 | 调整时卡顿 | ✅ 活跃 |
| **Mantis NDMF 化工具** | Booth 直接下载 | 免费 | NDMF 封装 | 依赖 Mantis | ✅ 活跃 |
| **Meshia Mesh Simplification** | `https://ramtype0.github.io/VpmRepository/index.json` | 免费 | Burst+Job 高速、BlendShape 完整保留、`PreserveBorderEdges` 防破洞 | 需要手动配置选项 | ✅ **活跃（推荐）** |
| **lilNDMFMeshSimplifier** | `https://lilxyzw.github.io/vpm-repos/redirect.html` | 免费 | 导入即见效 | 看不到面数，已废弃 | ❌ **已废弃**（README 明确指向 Meshia） |

> 📖 **Meshia 完整技术文档**: `meshia-mesh-simplification.md`（架构、API、Options、与 lilNDMF/Mantis 对比）

### 辅助工具

| 工具 | VPM 链接 | 说明 |
|------|----------|------|
| **ContinuousAvatarUploader** | 随 AAO repo | 批次上传 Avatar |

---

## MA 与 VRCFury 兼容性问题

> ⚠️ Fury 与 MA 互相不知道对方做了什么，容易出错

### 推荐执行顺序（来源：きくじん）

```
1. MA + 其他新增内容 NDMF 工具（Mantis、MeshSimplifier 等）
2. Fury
3. 所有 NDMF 最佳化工具（整合、删除系工具等）
```

### NDMF 内部执行顺序（2026 更新）

> ⚠️ 同一阶段内的多个工具仍需注意顺序

```
1. Modular Avatar（穿脱服装）
2. MA2BT                      ← MA 响应式层 → Direct BlendTree（必须在 MA 之后）
3. Avatar Compressor (LAC)    ← 自动纹理压缩（先处理贴图）
4. Avatar Optimizer (AAO)     ← 合并 Mesh/Bone/PhysBone（在压缩后的贴图上工作）
5. TexTransTool               ← Atlas 化（最后）
6. Meshia / 其他减面工具      ← 减面（按需）
```

**为什么 MA2BT 在 LAC 之前**（2026 新增）:
- MA2BT 强制 `seq.AfterPlugin("nadena.dev.modular-avatar")`，必须在 MA 之后
- MA2BT 处理的是 Animator 层结构（与贴图无关），顺序可与 LAC 互换
- 推荐放在靠前位置，让后续工具基于"已合并的 Animator 层"工作

**为什么 LAC 在 AAO 之前**（2026 新增）:
- AAO 的 Trace & Optimize 涉及 Skinned Mesh 合并、PhysBone 合并
- 这些操作基于"贴图状态"做决策
- 先压缩贴图可以让 AAO 看到"最优贴图状态"
- 详见 `lac-avatar-compressor.md` 与 `avatar-optimizer.md`

### 思路

完全理解 MA 和 Fury 各自做了什么，避免让他们处理同一个区块。

---

## VPM Package 导入清单

初次导入需要安装以下 Package（导入后在 Settings > Packages 启用）：

- AAO: Avatar Optimizer
- anatawa12's gists pack
- **Avatar Compressor (LAC)** ⭐NEW 2026-06-17
- Continuous Avatar Uploader
- lilAvatarUtils
- **MA2BT** ⭐NEW 2026-06-17
- Meshia Mesh Simplification
- Modular Avatar
- Non-Destructive Modular Framework
- TexTransTool

> ❌ `lilNDMFMeshSimplifier` 已废弃，不再列入导入清单

---

## 辅助窗口

### Actual Performance Window

由于 NDMF 是非破坏型最佳化，VRChat SDK 只显示编译前状态（通常是 Very Poor）。

**启用方法**:
```
1. 功能列 Tools > anatawa12's gist selector
2. 勾选 ActualPerformanceWindow 后，点击 Apply Changes
3. 功能列 Tools > anatawa12's gist
4. 勾选 Compute actual Performance on Play
```

进入 Play-mode 即可查看编译后真实效能。

### AvatarUtils 窗口

性能检测工具，可查看 Avatar 各部位数值。

**启用方法**: `Tools > AvatarUtils`

将 Avatar 拖入窗口即可查看各参数值。

---

## 相关文档

- `performance-rank.md` — Performance Rank 标准
- `optimization-guide.md` — 完整最佳化实操指南
