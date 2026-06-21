# VRC-Avatar-Performance-Tools (Thry)

> Type: SOURCE / TOOL
> Source: GitHub - Thryrallo/VRC-Avatar-Performance-Tools (MIT)
> Repository: https://github.com/Thryrallo/VRC-Avatar-Performance-Tools
> Author: Thryrallo (409 Stars / 18 Forks / 16 Releases)
> Latest Version: 1.3.7 (2024-08-05)
> Confidence: High (Tier A — 官方源码验证)
> Last Verified: 2026-06-17

---

## 概述

**Thryrallo/VRC-Avatar-Performance-Tools** 是 VRChat 社区最流行的 Avatar 性能分析工具之一,由 Thryrallo 开发并维护。该工具专注于检测 **VRChat 官方 Performance Rank 系统未覆盖** 的 6 项 Avatar 性能指标,以及详细的 VRAM 用量分析。

### 为什么需要这个工具

VRChat 官方的 Performance Rank 系统（Excellent / Good / Medium / Poor / Very Poor）只检测以下指标：

- 面数、材质内存、Skinned Mesh Renderer 数、材质球数
- PhysBone 元件数 / 影响骨头数 / 碰撞器数
- 骨头数、光源、粒子系统

但官方系统**不检测**以下这些对性能同样重要的指标：

- **VRAM 详细用量**(纹理 + Mesh 的 GPU 显存)
- **GrabPass** 数(极其昂贵的渲染技术)
- **Blendshape 影响三角形总数**(不只是 BlendShape 数量)
- **Animator AnyState Transitions 数**(每帧检查,CPU 杀手)
- **Animator Layer 数**(VRC CPU 限制)
- **Write Defaults 一致性**(Animator 状态正确性)
- **Empty States 数**(常见制作错误)

本工具正是为填补这些盲区而设计。

---

## 工具组成

### 1. Avatar Evaluator（菜单: `Thry/Avatar/Evaluator`）

通过菜单或右键 Avatar GameObject → Thry/Avatar/Evaluator 打开。计算并展示 6 项 Avatar 指标,每项都按 5 级质量分级(Excellent → Very Poor)。

### 2. VRAM Checker（菜单: `Thry/Avatar/VRAM`）

通过菜单或右键 Avatar GameObject → Thry/Avatar/VRAM 打开。详细列出 Avatar 上每个 Texture 和 Mesh 的 VRAM 占用,支持**一键优化**:

- 一键调整纹理分辨率（按钮直接修改 TextureImporter.maxTextureSize）
- 一键切换压缩格式（BC7 / DXT5 / DXT1）
- 一键将 >2048 纹理缩小到 2K
- 显示每个纹理被哪些 Material 引用

---

## 安装方式

### 方式 1: VCC（推荐,最新版）

```
Settings → Packages → Add Repository
URL: https://thryrallo.github.io/VRC-Avatar-Performance-Tools
（或使用 https://vpm.thry.dev/ 聚合源）
```

然后在 Creator Companion 的 "Manage Project" 中勾选 Avatar Performance Tools。

### 方式 2: OpenUPM

```bash
openupm add de.thryrallo.vrc.avatar-performance-tools
```

### 方式 3: Git URL

在 Unity Package Manager 中选择 "Add Package from Git URL",粘贴:

```
https://github.com/Thryrallo/VRC-Avatar-Performance-Tools.git
```

---

## 检测逻辑概览

### AvatarEvaluator 的 6 项检查（源码 `AvatarEvaluator.cs`）

| # | 指标 | 检测方法 | 关键阈值常量 |
|---|------|---------|-------------|
| 1 | **VRAM Size** | 调用 `TextureVRAM.QuickCalc()` | 见下表 |
| 2 | **Grabpasses** | Regex 匹配 shader 源文件中 `GrabPass { "name" }` | 0=Excellent, 1=Medium, >1=VeryPoor |
| 3 | **Blendshapes** | 累加所有有 BlendShape 的 SkinnedMeshRenderer 三角形数 | 8000/16000/32000/50000 |
| 4 | **Any State Transitions** | 累加所有 AnimatorControllerLayer 的 anyStateTransitions | 50/80/100/150 |
| 5 | **Write Defaults Check** | 比较 wdOn / wdOff 数量,输出一致性 outliers 列表 | — |
| 6 | **Empty States Check** | 扫描所有 state.motion == null 的 state | — |
| 7 | **Layer Count** | 累加 baseAnimationLayers + specialAnimationLayers | 12/20/30/45 |

### TextureVRAM 的 PC/Quest 双套阈值（源码 `TextureVRAM.cs`）

**Texture Memory(MiB)**:

| 等级 | PC | Quest |
|------|-----|-------|
| Excellent | < 40 | < 10 |
| Good | < 75 | < 18 |
| Medium | < 110 | < 25 |
| Poor | < 150 | < 40 |
| Very Poor | ≥ 150 | ≥ 40 |

**Mesh Memory(MiB)**:

| 等级 | PC | Quest |
|------|-----|-------|
| Excellent | < 20 | < 5 |
| Good | < 35 | < 10 |
| Medium | < 55 | < 15 |
| Poor | < 80 | < 25 |
| Very Poor | ≥ 80 | ≥ 25 |

### VRAM 计算公式

**Texture**:

```
VRAM = Σ_mipmap (width × height × bpp / 8)
```

Mipmap 链累加:第 N 级 = `width × height >> (2N)`,所以 Mipmap 占用 ≈ 原图的 1.33 倍。

**Mesh**:

```
VRAM = Σ_vertexAttributes (byte × dimension × vertexCount)
     + blendShapeVRAM
```

- SkinnedMesh 的 Position/Normal/Tangent 各占 **2 倍**(同时存储未蒙皮和蒙皮后数据)
- 每个受 BlendShape 影响的顶点额外 +40 bytes(uint index + 3×float position + 3×float normal + 3×float tangent)

### BPP(Bits Per Pixel)压缩格式表(部分关键)

| 格式 | BPP | 说明 |
|------|-----|------|
| DXT1 / BC1 / BC4 | 4 | 无 Alpha |
| DXT5 / BC5 / BC7 / BC6H | 8 | 有 Alpha / 高质量 |
| ASTC 4×4 | 8 | 移动端高质量 |
| ASTC 6×6 | 3.55 | 移动端均衡 |
| ASTC 8×8 | 2 | 移动端最小 |
| ASTC 12×12 | 1 | 移动端极小 |
| RGBA32 | 32 | 无压缩(慎用) |
| RGB24 | 24 | 无压缩(慎用) |

---

## 关键设计观察

### 1. PC vs Quest 阈值差距巨大

- Quest Texture Memory "Good" 上限 = **18 MiB**(仅为 PC 的 24%)
- Quest Mesh Memory "Excellent" 上限 = **5 MiB**(仅为 PC 的 25%)
- 这意味着为 PC 优化的 Avatar 在 Quest 上几乎一定会 Very Poor

### 2. 多 Avatar 累加效应

工具中硬编码的提示信息揭示了一个关键事实:

```
"Taking into account a world VRAM usage of 2GB - 
 If your model uses 150MB of VRAM and there were 40 of you, 
 all 8 GB of VRAM would be used up on an RTX 3070."
```

- 单个 Avatar 150MB × 40 = 6GB(超出 RTX 3070 的 8GB 总 VRAM)
- 单个 Avatar 150MB × 80 = 12GB(完全超额)
- **这就是为什么 Avatar VRAM 控制极其重要**

### 3. 自动化优化按钮

VRAM Checker 中每个纹理行都有"一键优化"按钮:

- `BC7 → -3.2 MiB`: 一键切换到 BC7 压缩
- `DXT1 → -2.4 MiB`: 一键切换到 DXT1 压缩(无 alpha 时)
- `2K → -5.1 MiB`: 一键缩小到 2048 分辨率

**警告**:压缩格式修改**不可撤销**(虽然有 ConfirmDialog,但 Unity Undo 不支持 TextureImporter 平台设置的修改)。

### 4. Inactive 对象不会真正卸载

工具显示 "Combined (only active)" 和 "Combined (all)" 两个数字,并标注:

```
"Inactive Objects are not unloaded. They are moved to system memory first 
 if you run out of VRAM, so they are not as bad as active textures, 
 but you should still try to keep their VRAM low."
```

这是 VRChat 资源管理的重要细节:**Disable GameObject ≠ 释放 VRAM**,只是降低优先级。

### 5. GrabPass 检测的局限性

工具使用 Regex `GrabPass\s*{\s*"(\w|_)+"\s*}` 匹配 shader 源文件:

- ✅ 能检测标准 `GrabPass { "TextureName" }`
- ❌ 检测不到无名称的 `GrabPass {}`(会漏报)
- ❌ 检测不到自定义 Shader 关键字
- ❌ 不适用于编译后的二进制 shader

---

## 在工作流中的位置

```
Avatar 制作完成
    ↓
运行本工具（Thry/Avatar/Evaluator）
    ↓
检查 6 项指标 + VRAM 详情
    ↓
[如果有 Very Poor 项]
    ↓
查看 outliers 列表,逐个修复
    ↓
再次运行,确认降到 Good 或 Excellent
    ↓
[可选] 运行 NDMF 工具链
    - AAO (Trace And Optimize)
    - Meshia (Mesh 减面)
    - TexTransTool (Atlas 合并)
```

---

## 与官方 Performance Rank 的差异

| 维度 | 官方系统 | Thry 工具 |
|------|---------|----------|
| **检测项数** | 15+ 项 | 7 项(补充) |
| **PC/Quest 区分** | ✅ | ✅ |
| **VRAM 详细分析** | 仅总体 Material Memory | 每纹理/每 Mesh 详细 |
| **GrabPass 检测** | ❌ | ✅ |
| **AnyState 检测** | ❌ | ✅ |
| **Layer Count 检测** | ❌ | ✅ |
| **Write Defaults 检测** | ❌ | ✅ |
| **Empty States 检测** | ❌ | ✅ |
| **一键优化** | ❌ | ✅(改 TextureImporter) |
| **可作为 VRC 审核依据** | ✅ | ❌(参考用) |

**结论**:两个工具互补使用。先用 Thry 工具排查细节,再用官方 Performance Rank 确认最终等级。

---

## 关联文档

- `memory/avatar/thry-avatar-evaluator-metrics.md` — 本工具检测的 7 项指标完整阈值与方法
- `memory/avatar/performance-rank.md` — VRChat 官方 Performance Rank 标准
- `memory/avatar/performance-benchmarks.md` — JustSleightly 性能基准测试
- `memory/avatar/optimization-guide.md` — Kuriko 完整最佳化实操指南
- `memory/avatar/ndmf-tools.md` — NDMF 工具生态

---

## 源码引用

- **AvatarEvaluator.cs**: `Editor/AvatarEvaluator.cs` (672 lines, VERSION = 1.3.6)
- **TextureVRAM.cs**: `Editor/VRAM Check/TextureVRAM.cs` (1100+ lines)
- **License**: MIT
- **维护状态**: 活跃(2024-08-05 最新 release 1.3.7)