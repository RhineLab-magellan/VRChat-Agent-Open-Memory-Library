---
title: "Meshia Mesh Simplification"
category: avatar
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - avatar
  - physbone
  - performance
aliases:
  - "Meshia Mesh Simplification"
  - meshia-mesh-simplification
related:
  - avatar-dynamic-bone-limits.md
  - performance-rank.md
  - avatar-fallback-system.md
  - avatar-particle-system-limits.md
  - impostor-fallback.md
---
# Meshia Mesh Simplification

> 来源: RamType0/Meshia.MeshSimplification (GitHub) + 官方文档站
> 置信度: High
> 包名: `com.ramtype0.meshia.mesh-simplification` | Unity: 2022.3+ | VRChat SDK: 2022.1.1+

---

## 0. 速查表

| 用户场景 | 推荐入口 | 关键参数 |
|----------|----------|----------|
| 想自动让整个 Avatar 面数降到目标 Performance Rank | `MeshiaCascadingAvatarMeshSimplifier` | Target Performance Rank + `Preserve Border Edges=true` |
| 想单独控制某个 Mesh 的面数（保形状/纹理） | `MeshiaMeshSimplifier` | `UseBarycentricCoordinateInterpolation=true`（防纹理扭曲） |
| 想在 C# 代码中生成多 LOD | `MeshSimplifier` Stateful API + `ScheduleSimplify` 重复调用 | Allocator.Persistent + `MeshSimplificationTarget.AbsoluteTriangleCount` |
| 想替换已废弃的 `lilNDMFMeshSimplifier` | 直接迁移到 Meshia | 旧 `lilNDMF` README 已明确声明废弃 |

---

## 1. 是什么 / 不是什么

### 是什么

**Meshia Mesh Simplification** 是一套基于 **Unity Job System + Burst Compiler + Unity Collections** 的高性能、异步网格轻量化（mesh decimation）工具库，专为 **Unity / VRChat** 设计。

- **核心定位**: Avatar/World 网格面数（polygon / triangle count）减少
- **运行时机**: Editor（实时预览 + NDMF 构建时）+ Runtime（C# API）
- **核心优势**: Burst 编译 + 异步 + Job 化 → 处理速度远超传统同步简化器
- **Avatar 特有能力**: **保留 Blend Shape**（表情系统）、按骨保留 Border Edges（避免指尖破洞）

### 不是什么

- ❌ 不是 Atlas/Texture 合并工具（→ 用 TexTransTool）
- ❌ 不是 Skinned Mesh 合并工具（→ 用 AvatarOptimizer / AAO）
- ❌ 不是动画/PhysBone 优化工具（→ 用 AAO MergePhysBone / MergeBone）
- ❌ 不是材质球合并工具（→ 用 TexTransTool）

### 在 Avatar 优化工具链中的位置

```
[原始 Avatar 模型]
    ↓
1. AAO Trace And Optimize        ← 合并 Skinned Mesh、删未用物件
2. TexTransTool                  ← 合并贴图 Atlas
3. Meshia Mesh Simplifier        ← 单独 Mesh 减面（细节控制）
   OR
   Meshia Cascading ...          ← 自动按目标 Performance Rank 分配面数
4. AAO Remove Mesh By BlendShape ← 删隐藏面
5. AAO Merge PhysBone            ← 合并 PhysBone
```

---

## 2. 三个核心组件

Meshia 提供 **三个不同抽象层级** 的入口：

| 组件 | 形态 | 适用人群 | 安装依赖 |
|------|------|----------|----------|
| **`MeshSimplifier`** (C# Struct) | 编程 API | UdonSharp/工具开发者 | 仅 Burst + Collections + Mathematics |
| **`MeshiaMeshSimplifier`** (MonoBehaviour) | NDMF 组件 | Avatar 改模玩家 | NDMF (≥ 1.5.0) |
| **`MeshiaCascadingAvatarMeshSimplifier`** (MonoBehaviour) | NDMF 组件（Avatar 级） | Avatar 改模玩家 | Modular Avatar |

---

## 3. 架构原理（**FACT**，来源: 官方 README + API docs）

### 3.1 计算流水线

Meshia 不同于传统的同步简化器，它把整个流程拆成 **4 个可调度的 Job**：

```
Mesh.MeshData
    │
    ▼ ScheduleLoadMeshData    ← Job 1: 读 mesh 数据到 NativeContainer
    │
MeshSimplifier 内部 Native 数据
    │
    ▼ ScheduleSimplify        ← Job 2: 执行 quadric 简化算法（可重复调用，多 LOD）
    │
简化后的中间数据
    │
    ▼ ScheduleWriteMeshData   ← Job 3: 写回 Mesh.MeshData
    │
简化后的 Mesh（保留 BlendShape）
```

**关键设计**:
- **Job System**: 所有计算跑在 Worker Thread，不阻塞主线程
- **Burst**: SIMD + IL2CPP 编译后的本地代码，速度比纯 C# 快 5-20×
- **NativeContainer**: 使用 `NativeList<T>` / `UnsafeList<T>` 等非托管内存，避免 GC
- **BlendShape 保护**: 通过 `BlendShapeData.GetMeshBlendShapes` 单独处理，不被简化破坏

### 3.2 核心算法（**推断 + 已验证**）

基于 API 文档（`MeshSimplificationTarget.ScaledTotalError` / `AbsoluteTotalError` 等）和 UnityMeshSimplifier 上游实现，Meshia 使用 **Quadric Error Metrics (QEM)** 算法：

- 每个顶点计算一个 4×4 误差矩阵
- 合并边时选择误差最小的 pair
- `Agressiveness` 因子控制每次迭代的合并激进程度（来源: 上游 UnityMeshSimplifier）

> 注：Meshia 的 `MeshSimplifierOptions` 未暴露 `Agressiveness`，可能使用默认值 7.0（来自上游）

---

## 4. C# API 完整参考（**FACT**，来源: API docs index.json）

### 4.1 `MeshSimplifier` 静态 API（无状态）

```csharp
using Meshia.MeshSimplification;

// 同步版本（阻塞当前线程）
MeshSimplifier.Simplify(
    Mesh originalMesh,                              // 源 mesh
    MeshSimplificationTarget target,                // 目标规格
    MeshSimplifierOptions options,                  // 选项
    Mesh destination                                // 输出 mesh
);

// 异步版本（Task，可取消）
await MeshSimplifier.SimplifyAsync(
    Mesh originalMesh,
    MeshSimplificationTarget target,
    MeshSimplifierOptions options,
    Mesh destination,
    CancellationToken cancellationToken = default
);

// 批量版本（一次处理多个 mesh）
MeshSimplifier.SimplifyBatch(
    IReadOnlyList<(Mesh, MeshSimplificationTarget, MeshSimplifierOptions, Mesh)> parameters
);
```

### 4.2 `MeshSimplifier` 实例 API（有状态，生成多 LOD）

```csharp
using Meshia.MeshSimplification;
using Unity.Collections;

// Allocator 选择规则:
//   - 多帧异步处理 → Allocator.Persistent
//   - 单帧完成     → Allocator.TempJob（不能用 Allocator.Temp）
using var simplifier = new MeshSimplifier(Allocator.Persistent);

// Job 1: 加载 mesh 数据
JobHandle loadHandle = simplifier.ScheduleLoadMeshData(
    mesh.MeshData,
    MeshSimplifierOptions.Default
);

// Job 2: 简化（可重复调用 → 同一 mesh 的多 LOD）
JobHandle simplifyHandle = simplifier.ScheduleSimplify(
    mesh.MeshData,
    blendShapes,                                     // NativeList<BlendShapeData>
    new MeshSimplificationTarget {
        Kind = MeshSimplificationTargetKind.AbsoluteTriangleCount,
        Value = 5000f
    },
    loadHandle                                       // 依赖 Job 1
);

// Job 3: 写回
JobHandle writeHandle = simplifier.ScheduleWriteMeshData(
    mesh.MeshData,
    blendShapes,
    destinationMesh.MeshData,
    destinationBlendShapes,
    simplifyHandle                                   // 依赖 Job 2
);

writeHandle.Complete();  // 阻塞等待所有 Job 完成
```

**多 LOD 模式**: 重复 4-5 步骤（ScheduleSimplify + ScheduleWriteMeshData）可对同一 mesh 生成多份简化结果

### 4.3 `MeshSimplificationTarget` — 目标规格

```csharp
public struct MeshSimplificationTarget {
    public MeshSimplificationTargetKind Kind;
    public float Value;
}

public enum MeshSimplificationTargetKind {
    RelativeVertexCount   = 0,  // 相对原 mesh 的顶点比例（0.0~1.0）
    AbsoluteVertexCount   = 1,  // 绝对目标顶点数
    ScaledTotalError      = 2,  // 总误差上限，按 bbox + 顶点数缩放
    AbsoluteTotalError    = 3,  // 绝对总误差上限
    RelativeTriangleCount = 4,  // 相对原 mesh 的三角面比例（0.0~1.0，**最常用**）
    AbsoluteTriangleCount = 5,  // 绝对目标三角面数
}
```

**实践推荐**:
- Avatar Cascading 模式 → `RelativeTriangleCount` (0~1)
- 精确控制 LOD 数 → `AbsoluteTriangleCount`
- 自动视觉质量保真 → `ScaledTotalError` / `AbsoluteTotalError`

### 4.4 `MeshSimplifierOptions` — 算法选项（**关键**）

```csharp
[Serializable]
public struct MeshSimplifierOptions {
    public bool EnableSmartLink;                       // 默认 true：合并相近顶点（推荐）
    [Range(0, 1)] public float MinNormalDot;          // 法线过滤阈值
    public bool PreserveBorderEdges;                   // **防止破洞**（指尖/边缘）
    public bool PreserveSurfaceCurvature;             // 曲面感知（更慢但更准）
    public bool UseBarycentricCoordinateInterpolation; // **防止纹理扭曲**
    public float VertexLinkColorDistance;              // SmartLink 颜色距离阈值
    public float VertexLinkDistance;                   // SmartLink 位置距离阈值
    [Range(0, 1)] public float VertexLinkMinNormalDot;// SmartLink 法线阈值
    public float VertexLinkUvDistance;                 // SmartLink UV 距离阈值
    
    public static MeshSimplifierOptions Default { get; }
}
```

**关键选项实战选择**:

| 场景 | 推荐配置 |
|------|----------|
| 默认（一般 Avatar） | `MeshSimplifierOptions.Default` |
| 指尖/边缘出现破洞 | `PreserveBorderEdges = true` |
| UV 接缝处纹理错位 | `UseBarycentricCoordinateInterpolation = true` |
| 曲面/球面/曲面 Avatar 失真严重 | `PreserveSurfaceCurvature = true`（计算成本↑） |
| 同一位置顶点被分成两份 | `EnableSmartLink = true` + 调高 `VertexLinkDistance` |

> ⚠️ **lilNDMFMeshSimplifier 时代没有 PreserveBorderEdges 等选项**，这是 Meshia 相比 lilNDMF 的核心进步

### 4.5 BlendShape 处理（**关键能力**）

```csharp
using Meshia.MeshSimplification;
using Unity.Collections;

// 读取 mesh 的 BlendShapes
NativeList<BlendShapeData> blendShapes = BlendShapeData.GetMeshBlendShapes(
    mesh,
    Allocator.Persistent  // 或 TempJob
);

// ... 传给 ScheduleSimplify / ScheduleWriteMeshData ...

// 简化完成后写回
BlendShapeData.SetBlendShapes(destinationMesh, blendShapes.AsReadOnlySpan());

blendShapes.Dispose();
```

**重要性**: 大多数传统简化器会**破坏 BlendShape**，导致 Avatar 表情失效。Meshia 通过单独处理 BlendShape 数据保证表情系统正常（**FACT**，来源: API docs 中 `BlendShapeData` / `BlendShapeFrameData` 独立结构）

---

## 5. NDMF 组件使用（**FACT**，来源: docs/en/vrchat/*）

### 5.1 安装前置

| 用途 | 必须依赖 |
|------|----------|
| Avatar 改模（使用两个组件） | **Modular Avatar** |
| World 改模（仅 MeshiaMeshSimplifier） | **NDMF** (≥ 1.5.0) |

### 5.2 `MeshiaMeshSimplifier`（单 Mesh 控制）

> 官方原文: "Attach `MeshiaMeshSimplifier` to your models. You can preview the result in EditMode."

**使用步骤**:
```
1. 选择目标 GameObject（带 MeshFilter / SkinnedMeshRenderer）
2. Add Component → MeshiaMeshSimplifier
3. 在 Inspector 中调整参数：
   - Target: 选择 MeshSimplificationTargetKind + Value
   - Options: MeshSimplifierOptions 字段
4. EditMode 下实时预览效果
```

**适用场景**: 需要精细控制某个特定 mesh 的面数（如手部、装饰品）

### 5.3 `MeshiaCascadingAvatarMeshSimplifier`（Avatar 级级联）

> 官方原文: "Create a Meshia Cascading Avatar Mesh Simplifier GameObject directly under the target avatar. Select the target performance rank. Adjust the polygon count distribution, options, etc. while checking the appearance."

**使用步骤**:
```
1. 在 Avatar 根节点下创建空 GameObject
2. Add Component → MeshiaCascadingAvatarMeshSimplifier
3. 选择目标 Performance Rank（Excellent / Good / Medium / Poor）
4. 检查预览，调整每个 Mesh 的面数分配
5. 启用关键选项（见下）
```

**与单 Mesh 组件的区别**:
- 自动发现 Avatar 下所有 Mesh
- 按目标 Rank 自动分配面数预算
- 支持单个 Mesh 锁定（不简化）
- 支持 `Enable Auto Adjust` 批量调整（来源: Kuriko 笔记）

### 5.4 三个关键选项（**FACT**，来源: 官方文档 "Tip"）

> 官方强调："There is a particularly important option."

#### Preserve Border Edges（保留边界边）

```
场景: 指尖、衣物边缘出现破洞（三角面被合并导致开口）
解决: 启用 Preserve Border Edges = true
原理: 标记 mesh 边界为不可合并边
```

**对比图**（来源: 官方文档截图描述）:
- Disabled: 指尖有可见孔洞
- Enabled: 指尖完整保留

#### 其他两个常用修复

| 问题 | 解决选项 |
|------|----------|
| 纹理 UV 接缝错位 | `UseBarycentricCoordinateInterpolation = true` |
| 曲面失真（球/管状结构） | `PreserveSurfaceCurvature = true` |

### 5.5 v3.1 新功能

> 来源: GitHub Releases 3.1.0

| 变更 | 意义 |
|------|------|
| **Configure preserve border edges per bone** (#25) | 按骨配置 Border Edges 保留（之前是全局开关） |
| **Toggle `MeshiaMeshSimplifier.enabled`** (#28) | 不移除组件的情况下禁用 |
| Fix: 无有效合并候选时异常 (#32) | 稳定性修复 |
| Fix: `MeshiaCascadingAvatarMeshSimplifier` 在目标 mesh 被其他 NDMF 工具销毁时异常 (#33) | **关键**：与 NDMF 工具链集成稳定性 |

---

## 6. 与其他减面工具对比

### 6.1 综合对比表

| 工具 | 算法来源 | 性能 | BlendShape | 边界保护 | 异步 | 价格 | 状态 |
|------|----------|------|------------|----------|------|------|------|
| **Meshia Mesh Simplification** | QEM + Burst | ⭐⭐⭐⭐⭐ | ✅ 完整 | ✅ 可配置 | ✅ | 免费 | ✅ 活跃 |
| **lilNDMFMeshSimplifier** | 上游 UnityMeshSimplifier | ⭐⭐⭐ | ⚠️ 部分 | ❌ | ❌ | 免费 | ❌ **已废弃** |
| **Mantis LOD Editor** | 商业 | ⭐⭐⭐⭐ | ⚠️ 部分 | ✅ | ❌ | **$50** | ✅ 活跃 |
| **Overall NDMF Mesh Simplifier** (Tliks) | 封装 Meshia | ⭐⭐⭐⭐⭐ | ✅ | 继承 Meshia | ✅ | 免费 | ✅ 活跃（0.1.2） |

### 6.2 关键演进史

**lilNDMFMeshSimplifier 已被官方废弃**（来源: GitHub README）:

> # This project is discontinued and is no longer maintained.
> # Please use Meshia Mesh Simplification instead.

**迁移路径**:
```
lilNDMFMeshSimplifier → Meshia Mesh Simplification
  ↓
- 删除 lilNDMFMeshSimplifier VPM (lilxyzw)
- 安装 Meshia VPM (RamType0)
- 重新配置 MeshiaMeshSimplifier 组件
- 启用 PreserveBorderEdges + UseBarycentricCoordinateInterpolation
  （旧 lilNDMF 没有这些选项，是默认行为差异）
```

### 6.3 选择决策树

```
想减面？
├─ 只需基础质量
│   └─ 用 MeshiaMeshSimplifier + Default 选项
│
├─ 自动按目标 Performance Rank 分配
│   └─ 用 MeshiaCascadingAvatarMeshSimplifier
│
├─ 指尖/边缘破洞
│   └─ Enable Preserve Border Edges
│
├─ UV/纹理扭曲
│   └─ Enable UseBarycentricCoordinateInterpolation
│
├─ 多 LOD 生成（运行时）
│   └─ 用 MeshSimplifier Stateful API + 重复 ScheduleSimplify
│
└─ 想要 Mantis 质量但没钱
    └─ 用 Meshia + PreserveSurfaceCurvature=true（慢但更接近商业质量）
```

---

## 7. 最佳实践与陷阱

### 7.1 DO ✅

1. **在 EditMode 预览后再 Build**: Meshia 提供实时预览，不要盲 Build
2. **Cascading 模式优先于逐 Mesh 模式**: 对 Avatar 整体优化更高效
3. **启用 PreserveBorderEdges**: 几乎是无副作用的"安全选项"
4. **多 LOD 重复调用 ScheduleSimplify**: 比单次大压缩更灵活（保留更多 LOD 切换控制）
5. **搭配 AAO Trace And Optimize 先合并 Skinned Mesh**: 减少 Mesh 数量后再简化效果更好

### 7.2 DON'T ❌

1. **不要对表情 Mesh (Face) 做大幅减面**: 即使有 BlendShape 保护，过度简化也会失真
2. **不要在 Build 后修改目标**: EditMode 预览是离线的，Build 触发重新计算
3. **不要混用 lilNDMF + Meshia**: 同类工具重复执行，浪费 NDMF 构建时间
4. **不要对 PhysBone 末端的 Mesh 设过低保真**: 会让动态效果看起来像棱角分明
5. **不要忽视 TargetKind 选错**: `AbsoluteVertexCount` 不考虑当前 mesh 大小，可能破坏小部件

### 7.3 性能对比直觉（**推断**，无硬数据）

> ⚠️ 以下为基于架构分析的定性比较，非实测 benchmark

| 操作 | Meshia (Burst+Job) | 传统同步简化器 |
|------|-------------------|----------------|
| 单 mesh 简化 (中等 10k 面) | 数十 ms（异步，不卡 UI） | 数百 ms（卡 UI） |
| 批量 50 mesh | 1-2 秒（分帧调度） | 5-10 秒（主线程阻塞） |
| 多 LOD (3 档) | 复用已加载数据，仅重复 Simplify | 每次重新加载 |

---

## 8. 与其他 NDMF 工具的协同

### 8.1 执行顺序（**FACT**，基于 NDMF 管线 + 3.1 修复 #33）

> ⚠️ 3.1.0 修复 #33 后，MeshiaCascadingAvatarMeshSimplifier 不再因其他工具销毁目标 mesh 而抛异常，但仍建议放在最后以获得最优结果

**推荐顺序**:
```
1. Modular Avatar 组件（添加服装/物体）
2. lilAvatarUtils / 分析工具（只读）
3. AAO Merge Skinned Mesh（合并 SMR）
4. TexTransTool（合并贴图）
5. AAO Trace And Optimize（自动优化）
6. AAO Remove Mesh By BlendShape（删除隐藏面） ← 新增
7. Meshia Mesh Simplifier（减面） ← **最后**
```

### 8.2 与 AvatarOptimizer (AAO) 互补

| 工具 | 解决什么问题 |
|------|--------------|
| AAO Merge Skinned Mesh | 减少 Material Slot / Draw Call |
| AAO Remove Mesh By BlendShape | 删掉被 BlendShape 隐藏的面（0 成本） |
| **Meshia** | **简化剩余 Mesh 的多边形数（智能减面）** |

三者配合：
- AAO 先合并 SMR → mesh 数量变少
- AAO Remove Mesh → 部分面被剔除
- Meshia 处理剩余 mesh → 在更小基础上减面

---

## 9. VPM 安装

### 9.1 VPM Repository

```
https://ramtype0.github.io/VpmRepository/index.json
```

### 9.2 VPM 链接速查

| 工具 | VPM 仓库 |
|------|----------|
| **Meshia Mesh Simplification** | `https://ramtype0.github.io/VpmRepository/index.json` |
| lilNDMFMeshSimplifier（已废弃） | `https://lilxyzw.github.io/vpm-repos/redirect.html` |
| Overall NDMF Mesh Simplifier | （依赖 Meshia 2.1.0+，单独仓库） |

### 9.3 直接 UPM（备选）

```json
{
  "dependencies": {
    "com.ramtype0.meshia.mesh-simplification": "3.2.0"
  }
}
```

### 9.4 依赖项

**直接依赖**:
- `com.unity.burst` ≥ 1.8.21
- `com.unity.collections` ≥ 2.5.7
- `com.unity.mathematics` ≥ 1.3.2

**VPM 依赖**:
- `com.anatawa12.custom-localization-for-editor-extension` ≥ 1.2.1

---

## 10. 局限性与未解决问题

### 10.1 已知问题

- **v3.1 修复记录**:
  - 无有效合并候选时异常 (#32)
  - 目标 mesh 被其他 NDMF 工具销毁时异常 (#33)
  - **保留边界边配置从全局改为按骨** (#25，旧版本可能需要迁移配置）

### 10.2 未覆盖场景

| 场景 | 状态 |
|------|------|
| Quest 移动端特殊处理 | 未优化（任何 mesh 减面工具对 Quest 都有效） |
| 与 VRCFury 协同 | NDMF 工具通用问题，需关注执行顺序 |
| Shader 顶点依赖（VertexID-based） | 未文档化，可能破坏自定义 shader |
| 实时 LOD 切换 | 需用 Stateful API 自行实现 |

### 10.3 验证方法

> 由于 UdonSharp Agent 不直接跑 Unity，构建/效果验证需用户本地完成。建议流程：
> 1. 复制 Avatar → 应用 Meshia → 比较 SDK Performance Rank
> 2. 在客户端查看模型外观是否破洞
> 3. 用 lilAvatarUtils 对比性能数据

---

## 11. 相关文档

### 知识库内链

- `memory/avatar/ndmf-tools.md` — NDMF 生态体系总览
- `memory/avatar/optimization-guide.md` — 减面章节
- `memory/avatar/optimization-guide.md#polygons面数减面` — 减面工具对比表
- `memory/avatar/performance-rank.md` — 性能等级标准

### 外部权威

- GitHub: https://github.com/RamType0/Meshia.MeshSimplification
- 官方文档站: https://ramtype0.github.io/Meshia.MeshSimplification/
- API Reference: https://ramtype0.github.io/Meshia.MeshSimplification/api/Meshia.MeshSimplification.html
- 上游算法参考: https://github.com/Whinarn/UnityMeshSimplifier
- 已废弃工具: https://github.com/lilxyzw/lilNDMFMeshSimplifier

---

## 12. 关键事实卡片（Quick Reference）

> 用于教学/快速问答时复制粘贴

**Meshia 是什么？**
> 基于 Unity Burst + Job System 的高速异步网格简化库，专为 VRChat Avatar/World 设计，2025-2026 年最活跃的 NDMF 减面工具，已取代 lilNDMFMeshSimplifier。

**Meshia 怎么用？**
> Avatar 改模装 Modular Avatar → 装 Meshia → 加 `MeshiaCascadingAvatarMeshSimplifier` 到 Avatar 根节点 → 选目标 Performance Rank → 启用 `Preserve Border Edges`。

**为什么要用 Meshia 而不是 lilNDMF？**
> lilNDMFMeshSimplifier 已于 2024-2025 年被官方废弃。Meshia 提供 Burst 加速、BlendShape 完整保留、`PreserveBorderEdges`（防破洞）、`UseBarycentricCoordinateInterpolation`（防纹理扭曲）等更多能力。

**什么时候不用 Meshia？**
> - 想保留 Mantis 商业级曲面质量且愿付费
> - 只想删被 BlendShape 隐藏的面（→ 用 AAO Remove Mesh By BlendShape，零成本）
> - mesh 已经是低保真，没什么可简化的
