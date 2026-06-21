---
title: AAO: Avatar Optimizer 完整知识库
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - shader
  - json

aliases:
  - "AAO： Avatar Optimizer 完整知识库"

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: v1.9.14 (2026-06-03)
last_review: 2026-06-21
confidence: Medium
---
# AAO: Avatar Optimizer 完整知识库

> 来源: https://github.com/anatawa12/AvatarOptimizer
> 文档: https://vpm.anatawa12.com/avatar-optimizer/en/
> 当前版本: **v1.9.14** (2026-06-03)
> 置信度: High (Tier A — 开源项目官方文档)

---

## 1. 概述

**AAO (Avatar Optimizer)** 是非破坏性 Avatar 优化工具集，专为 VRChat Avatar 设计（也支持其他 NDMF 兼容平台）。

| 属性 | 值 |
|------|-----|
| **运行方式** | NDMF 插件，在 Play Mode 进入或 Avatar Build 时自动应用 |
| **核心理念** | 非破坏性（Non-Destructive）：不修改原始 Prefab，仅影响编译时的临时副本 |
| **设计目标** | 在不影响外观的前提下优化性能，**不改变 Avatar 行为** |
| **版本策略** | Semantic Versioning 2.0.0，同 Major 版本内已添加组件行为不变 |
| **依赖** | NDMF + VRChat SDK + Unity 2022.3.22f1 |

### 核心特性

- **非破坏性**: 无需 Unpack Prefab，只需添加组件
- **自动优化**: `Trace And Optimize` 一键处理多种优化
- **组件化**: 每个优化步骤是独立组件，可组合使用
- **语义版本控制**: 组件行为在同 Major 版本内保证稳定
- **开发者 API**: Component API + Shader Information API + Asset Description

---

## 2. 安装

### 方式 1: ALCOM / VCC (推荐)

```
1. 添加 VPM 仓库: https://vpm.anatawa12.com/vpm.json
2. 在 ALCOM / VCC 中安装 Avatar Optimizer
```

### 方式 2: vrc-get (命令行)

```bash
vrc-get repo add https://vpm.anatawa12.com/vpm.json
cd /path/to/your-unity-project
vrc-get install com.anatawa12.avatar-optimizer
```

### 方式 3: VPM CLI

```bash
vpm add repo https://vpm.anatawa12.com/vpm.json
cd /path/to/your-unity-project
vpm add package com.anatawa12.avatar-optimizer
```

### 方式 4: UnityPackage

从 GitHub Releases 下载 installer unitypackage 直接导入。

---

## 3. 组件分类体系

AAO 组件按 **Kind (种类)** 和 **安装位置** 分类：

### 3.1 Avatar Global Components (Avatar 全局组件)

> 必须添加到 Avatar Root (VRC Avatar Descriptor 所在 GameObject)

| 组件 | 说明 |
|------|------|
| **AAO Trace And Optimize** | 核心组件，自动追踪并优化整个 Avatar |
| **UnusedBonesByReferencesTool** | 标记 EditorOnly 骨骼（已过时，推荐用 T&O） |

### 3.2 Edit Skinned Mesh Components (网格编辑组件)

> 必须添加到有 SkinnedMeshRenderer 的 GameObject 上

#### Source 组件 (生成新 Mesh)

| 组件 | 说明 |
|------|------|
| **AAO Merge Skinned Mesh** | 合并多个 SkinnedMeshRenderer / MeshRenderer 为一个 |

#### Modifying 组件 (修改现有 Mesh)

| 组件 | 支持 MeshRenderer | 说明 |
|------|:-:|------|
| **AAO Freeze BlendShape** | ❌ | 冻结并移除 BlendShape |
| **AAO Remove Mesh By BlendShape** | ❌ | 通过 BlendShape 移除顶点/多边形 |
| **AAO Remove Mesh By Mask** | ✅ (v1.9+) | 通过遮罩贴图移除多边形 |
| **AAO Remove Mesh By Box** | ✅ (v1.9+) | 通过包围盒移除多边形 |
| **AAO Remove Mesh By UV Tile** | ✅ (v1.9+) | 通过 UV Tile 区域移除多边形 |
| **AAO Merge Material** | ✅ (v1.9+) | 合并多个材质为一个 (贴图打包) |
| **AAO Max Texture Size** | — | 限制纹理最大尺寸 (mipmap 提取) |

### 3.3 PhysBone 相关组件

| 组件 | 添加位置 | 说明 |
|------|----------|------|
| **AAO Merge PhysBone** | 新 GameObject | 合并多个 PhysBone 为一个 |
| **AAO Clear Endpoint Position** | PhysBone 所在 GO | 将 EndpointPosition 清零并添加 _EndPhysBone |

### 3.4 骨骼组件

| 组件 | 添加位置 | 说明 |
|------|----------|------|
| **AAO Merge Bone** | 要合并的骨骼 GO | 将骨骼合并到父骨骼 |

---

## 4. 核心组件详解

### 4.1 AAO Trace And Optimize (T&O) ⭐核心

> Kind: Avatar Global Component
> 位置: Avatar Root

**这是 AAO 最重要的组件。** 自动追踪 Avatar 并应用多种优化，设计原则是 **"绝不改变外观"**。

#### 自动优化项目

| 优化 | 说明 | 影响维度 |
|------|------|----------|
| **Remove Unused Objects** | 扫描动画等，自动移除未使用的 GameObjects、Components、Textures | 面数 / DrawCall / 内存 |
| ├─ Preserve EndBone | 防止移除父骨未被移除的 end bones | — |
| **Optimize PhysBone Settings** | 优化 PhysBone 设置 | PhysBone 性能 |
| ├─ 合并相同 Collider | 完全相同设置的 PhysBone Collider 合并为一个 | Collider 数 |
| ├─ 取消 Is Animated | 不需要动画时自动取消勾选 | 计算量 |
| ├─ 合并 PhysBone | 行为无变化时合并多个 PB（如不可抓取时）| PB 组件数 |
| └─ Endpoint Position 替代 | 用 Endpoint Position 替代 end bone | 骨骼数 |
| **Merge Skinned Meshes** | 合并不需要分离的蒙皮网格 | DrawCall / CPU |
| └─ Allow Shuffling Material Slots | 重排材质槽减少 DrawCall | DrawCall |
| **Optimize Texture** | UV Packing + 减小贴图尺寸（仅支持的 Shader） | VRAM |
| **MMD World Compatibility** | 不冻结 MMD World 使用的 BlendShape | 兼容性 |
| **Remove Zero Sized Polygons** ⚠️ | 移除面积为零的多边形 (Advanced) | 面数 |

#### Animator Optimizer (动画优化器)

| 优化 | 说明 |
|------|------|
| **Convert AnyState to Entry-Exit** | 将 AnyState 层转换为 Diamond/Linear Entry-Exit 类型 |
| **Convert Complete Graph to Entry-Exit** | 将完全图结构层转换为 Entry-Exit |
| **Convert Entry-Exit to BlendTree** | 将 Entry-Exit 层转换为 BlendTree |
| **Merge BlendTree Layers** | 将多个 BlendTree 层合并为单个 Direct BlendTree |
| **Remove Meaningless Layers** | 移除没有状态或过渡的层 |

> 💡 **Animator Optimizer 的核心价值**: AnyState → Entry-Exit → BlendTree 的级联转换，可显著减少每帧计算的 Transition 数量。

#### 设计保证

- **默认设置绝不改变 Avatar 外观或行为**
- 如果 T&O 改变了外观 → 这是 **Bug**，应上报
- Debug Options 不受稳定性保证

---

### 4.2 AAO Merge Skinned Mesh (MergeSMR)

> Kind: Source Edit Skinned Mesh Component
> 位置: 新建空 GameObject (需有 SkinnedMeshRenderer 且无 Mesh)

#### 功能

将多个 SkinnedMeshRenderer 和 MeshRenderer 合并为一个 SkinnedMeshRenderer。

#### 关键设置

| 设置 | 说明 |
|------|------|
| **Skinned Renderers** | 要合并的 SkinnedMeshRenderer 列表 |
| **Basic Renderers** | 要合并的 MeshRenderer 列表 (v1.9+) |
| **Copy Everything** | 复制源渲染器的所有设置 |
| **BlendShape Mode** | 处理同名 BlendShape 的方式 |
| **Merge Materials** | 合并使用相同材质的材质槽 (减少 DrawCall) |

#### BlendShape Mode 选项

| 模式 | 说明 | 推荐 |
|------|------|------|
| **Rename to avoid conflict** | 重命名避免冲突 | ✅ 默认推荐 |
| **Merge with same name** | 合并同名 BlendShape | 需要同步动画时使用 |
| **v1.7.x compatibility** | 旧版兼容模式 | ❌ 不推荐 |

#### 注意事项

- T&O 会自动执行相同操作，大多数情况无需手动添加
- **不会自动设置 Root Bone**，需手动设置
- 合并后无法单独开关某个物件（不能穿脱衣服）
- Face (头) 因 BlendShape 最多，建议保持独立

---

### 4.3 AAO Freeze BlendShape

> Kind: Modifying Edit Skinned Mesh Component
> 位置: 有 SkinnedMeshRenderer 的 GameObject

#### 功能

冻结 BlendShape 的当前状态并将其从 Mesh 中移除。

#### 优化效果

| 场景 | 效果 |
|------|------|
| **非零权重** BlendShape | 冻结后减少处理成本 (CPU) |
| **零权重** BlendShape | 移除后减少 Avatar 体积 (内存) |

#### 注意事项

> ⚠️ 冻结后 BlendShape 权重将无法在动画中改变

#### 典型用法

```
1. 设置好 BlendShape 权重（如衣服隐藏身体 = 100）
2. 添加 AAO Freeze BlendShape
3. 勾选要冻结的 BlendShape
4. Build 时自动冻结并移除
```

---

### 4.4 AAO Remove Mesh By BlendShape

> Kind: Modifying Edit Skinned Mesh Component
> 位置: 有 SkinnedMeshRenderer 的 GameObject

#### 功能

根据指定的 BlendShape 移除被变换的顶点及其多边形。

#### 核心设置

| 设置 | 说明 |
|------|------|
| **BlendShape 列表** | 勾选用于隐藏身体的 BlendShape |
| **Tolerance** | 顶点移动超过此阈值即被移除 |
| **Invert** | 反转移除逻辑 (v1.9+) |
| **Auto Preview** | 切换时自动设置权重为 100/0 以预览效果 |

#### 典型场景

```
衣服遮挡身体 → 身体 BlendShape 缩小 → 用该 BlendShape 移除被遮挡的面
```

> 💡 这是减少面数和 BlendShape 处理成本的核心手段之一

---

### 4.5 AAO Remove Mesh By Mask (v1.9+)

> Kind: Modifying Edit Skinned Mesh Component (支持 MeshRenderer)
> 位置: 有 SkinnedMeshRenderer / MeshRenderer 的 GameObject

#### 功能

通过遮罩贴图指定区域来移除多边形。

#### 核心设置

| 设置 | 说明 |
|------|------|
| **Material Slots** | 选择要处理的材质槽 |
| **Mask Texture** | 遮罩贴图（可创建新贴图或用现有） |
| **Remove Mode** | `Remove Black` (黑色区域移除) 或 `Remove White` (白色区域移除) |

#### Mask Texture Editor

内置贴图编辑器:
- 左键拖拽: 绘制遮罩
- 右键拖拽 / Shift+左键: 移动视图
- 滚轮: 缩放
- Shift+滚轮: 调整笔刷大小

#### 兼容

支持 gatosyocora 的 MeshDeleterWithTexture 遮罩贴图。

---

### 4.6 AAO Remove Mesh By Box

> Kind: Modifying Edit Skinned Mesh Component (支持 MeshRenderer)
> 位置: 有 SkinnedMeshRenderer / MeshRenderer 的 GameObject

#### 功能

通过一个或多个包围盒 (Box) 来移除多边形。

#### 核心设置

| 设置 | 说明 |
|------|------|
| **Remove Polygons** | 选择移除 Box 内部还是外部 |
| **Boxes** | 包围盒列表（位置、大小、旋转） |

#### 编辑方式

- Inspector 中调整 Center / Size / Rotation (本地坐标)
- 点击 `Edit This Box` 使用 Gizmo 可视化编辑

---

### 4.7 AAO Remove Mesh By UV Tile

> Kind: Modifying Edit Skinned Mesh Component (支持 MeshRenderer)
> 位置: 有 SkinnedMeshRenderer / MeshRenderer 的 GameObject

#### 功能

通过 UV Tile 区域来移除多边形。

#### 适用场景

- 配合 Poiyomi / lilToon 的 UV Tile Discard 设计
- 移除特定材质球的所有面数
- 可指定使用哪个 UV Channel

---

### 4.8 AAO Merge PhysBone (MergePB)

> 位置: 新建 GameObject

#### 功能

将多个 PhysBone 组件合并为一个 (MultiChildType = Ignore)。

#### 关键约束

| 约束 | 说明 |
|------|------|
| **共同父级** | 合并目标 PB 必须是同一 GameObject 的子级 |
| **Make Children of Me** | 或使用此选项使 PB 成为当前 GO 的子级 |
| **抓取限制** | 合并后只能同时抓取一个 PB（原来可以各抓一个） |
| **Affected Transforms +1** | 每个 MergePB 会增加一个 Affected Transform |

#### Override 模式

| 属性 | Copy | Override | Merge | Fix | Clear |
|------|:----:|:--------:|:-----:|:---:|:-----:|
| 通用设置 | ✅ | ✅ | — | — | — |
| Colliders | — | — | ✅ | — | — |
| Endpoint Position | — | — | — | — | ✅ |
| Limit Rotation | — | — | — | ✅ | — |

- **Copy**: 复制源值（仅当所有源值相同时可用）
- **Override**: 手动设置新值
- **Merge**: 合并所有源的 Collider 数组
- **Fix**: 修正不同 roll axis（骨骼旋转轴不同时使用）
- **Clear**: 将 EndpointPosition 清零

---

### 4.9 AAO Merge Bone

> 位置: 要合并的骨骼 GameObject

#### 功能

将目标骨骼合并到父骨骼，减少骨骼数量。

#### 行为

- 目标 GameObject 被移除，合并到父级
- 目标上的其他组件也被移除
- 所有子对象归属于父对象
- 如果父级也有 Merge Bone，则级联合并到更上一级

#### 设置

| 设置 | 说明 |
|------|------|
| **Avoid Name Conflict** | 重命名子对象避免动画名称冲突 |

> 💡 T&O 会自动执行相同操作，大多数情况无需手动添加

---

### 4.10 AAO Clear Endpoint Position

> 位置: 有 PhysBone 的 GameObject

#### 功能

将 EndpointPosition 清零 (设为 0) 并添加 `_EndPhysBone` GameObject 来替代。

- 可通过 `Apply and Remove component` 按钮在编辑器中直接应用
- T&O 的 Optimize PhysBone Settings 会自动执行类似操作

---

### 4.11 AAO Merge Material (v1.9+) ⭐NEW

> Kind: Modifying Edit Skinned Mesh Component (支持 MeshRenderer)
> 位置: 有 SkinnedMeshRenderer / MeshRenderer 的 GameObject

#### 功能

将使用相同 Shader 的多个材质合并为一个材质，通过手动贴图打包实现。

#### 核心特性

| 特性 | 说明 |
|------|------|
| **Shader 支持** | 通过 ShaderInformation API 支持 (lilToon, Standard, ToonLit, ToonStandard 等) |
| **贴图打包** | 手动指定每个源材质的贴图位置 (X, Y, W, H) |
| **参考材质** | 指定 Reference Material 用于非 UV 属性 |
| **纹理配置** | 可设置生成纹理的尺寸和格式 |

#### 限制

- ❌ 不支持动画替换材质
- ❌ 不支持 UV 滚动/视差等动态 UV 变换
- 由 Merge Material 创建的材质不会被 Merge Skinned Mesh 合并

> 💡 **Merge Material 是 Merge ToonLit Material 的继任者**。Merge ToonLit Material 已废弃，将在下个大版本移除。

---

### 4.12 AAO Max Texture Size (v1.9+) ⭐NEW

> 位置: 任意 GameObject（影响该 GO 及所有子级）

#### 功能

通过提取指定 mipmap 级别来减小纹理尺寸，保留原始纹理格式和设置。

#### 规则

- 多个 Max Texture Size 组件存在时，使用最近父级的设置
- 同一纹理受多个设置影响时，取最大值

#### 限制

| 限制 | 说明 |
|------|------|
| **需要 Mipmaps** | 纹理必须启用 mipmaps 才能被缩放 |
| **不兼容 Crunch** | Crunch 压缩的纹理无法被缩放 |

---

## 5. 优化方向总结

### 5.1 各优化维度与组件映射

| 优化维度 | 自动 (T&O) | 手动组件 | 影响指标 |
|----------|:----------:|----------|----------|
| **移除未使用对象** | ✅ | — | 面数 / DrawCall / 内存 |
| **冻结 BlendShape** | ✅ | Freeze BlendShape | CPU / 内存 |
| **移除遮挡面数** | — | Remove Mesh By BlendShape/Mask/Box/UV Tile | 面数 / BlendShape CPU |
| **合并 Skinned Mesh** | ✅ | Merge Skinned Mesh | DrawCall / CPU |
| **合并材质 (Atlas)** | — | Merge Material | DrawCall / Material Slots |
| **合并骨骼** | ✅ | Merge Bone | 骨骼数 / PB Transforms |
| **合并 PhysBone** | ✅ | Merge PhysBone | PB 组件数 / Colliders |
| **优化 PB 设置** | ✅ | Clear Endpoint Position | PB 计算量 |
| **优化贴图** | ✅ | Max Texture Size | VRAM |
| **优化 Animator** | ✅ (Animator Optimizer) | — | CPU (Transition 计算) |

### 5.2 性能影响矩阵

```
                  CPU    GPU    VRAM   DrawCall   面数    PB     骨骼
T&O 自动优化      ✅     —      ✅     ✅         ✅     ✅     ✅
Remove Mesh       ✅     ✅     —      —          ✅     —      —
Freeze BlendShape ✅     —      ✅     —          —      —      —
Merge SMR         ✅     —      —      ✅         —      —      —
Merge Material    —      —      —      ✅         —      —      —
Merge PhysBone    —      —      —      —          —      ✅     —
Merge Bone        —      —      —      —          —      ✅     ✅
Animator Opt      ✅     —      —      —          —      —      —
Max Texture Size  —      —      ✅     —          —      —      —
```

### 5.3 优化工作流推荐顺序

```
1. 添加 AAO Trace And Optimize (全自动基础优化)
   ↓
2. Remove Mesh By BlendShape (利用身体隐藏 BlendShape 去面)
   ↓
3. Freeze BlendShape (冻结固定外观的 BlendShape)
   ↓
4. Merge Material / Atlas (合并材质减少 DrawCall)
   ↓
5. 检查自动合并结果，手动补充 Merge Skinned Mesh
   ↓
6. 手动合并 PhysBone (如 T&O 未能完全合并)
   ↓
7. Max Texture Size (限制贴图分辨率)
   ↓
8. 使用 lilAvatarUtils / Actual Performance Window 验证
```

---

## 6. 与 Modular Avatar 的协作

### 执行顺序

AAO 在 NDMF 管线中**尽量晚执行**（v1.9+ 默认），确保 MA 等其他工具先完成处理。

```
1. Modular Avatar (处理组件、菜单、参数等)
2. 其他 NDMF 工具 (新增内容)
3. AAO (最后执行优化)
```

### 典型组合

| 场景 | MA 职责 | AAO 职责 |
|------|---------|----------|
| 换装 Avatar | 合并菜单、管理参数 | 合并网格、优化骨骼 |
| PhysBone 优化 | 无直接关系 | 合并 PB、优化 Collider |
| 材质优化 | 管理材质引用 | Merge Material、UV Packing |
| 动画系统 | 构建 Animator | Animator Optimizer |

### 兼容性问题

> ⚠️ 如果你的插件需要在 AAO 之后运行，使用 NDMF `AfterPlugin` API:
> `AfterPlugin("com.anatawa12.avatar-optimizer")`

---

## 7. 开发者 API

### 7.1 Component API (v1.7+)

通过脚本添加和配置 AAO 组件。

#### 支持的组件

| 组件 | 添加 + 配置 | 仅添加 |
|------|:-----------:|:------:|
| RemoveMeshInBox | ✅ | — |
| RemoveMeshByBlendShape | ✅ | — |
| RemoveMeshByMask | ✅ | — |
| MergePhysBone | ✅ | — |
| TraceAndOptimize | — | ✅ |

#### 使用方式

```csharp
// 引用 com.anatawa12.avatar-optimizer.runtime 程序集
using Anatawa12.AvatarOptimizer.API;

// 添加组件
var component = gameObject.AddComponent<RemoveMeshByBlendShape>();

// 初始化（确保版本兼容性）
component.Initialize(1); // version = 配置版本号

// 配置...
```

#### 重要规则

1. 添加后**立即**调用 `Initialize(version)` 确保兼容性
2. **仅支持**刚添加的组件配置，不支持已存在的组件
3. 运行时程序集中**不应**引用 AAO runtime

### 7.2 Shader Information API (v1.8+)

告诉 AAO 你的 Shader 如何使用纹理和 UV，以启用高级优化。

#### 注册方式

```csharp
using Anatawa12.AvatarOptimizer.API;

[InitializeOnLoad]
public class MyShaderInfo
{
    static MyShaderInfo()
    {
        ShaderInformationRegistry.RegisterShaderInformation<MyCustomShaderInfo>();
    }
}

public class MyCustomShaderInfo : ShaderInformation
{
    public override void GetMaterialInformation(MaterialInformationCallback callback)
    {
        // 注册纹理和 UV 使用信息
        callback.RegisterTextureUVUsage(
            "_MainTex",
            // UV channel, transform 等
        );
    }
}
```

#### 功能标志

| 标志 | 说明 |
|------|------|
| **TextureAndUVUsage** | 提供纹理使用的 UV 通道信息 |
| **VertexIndexUsage** | Shader 使用顶点索引（AAO 会保留顶点顺序） |

#### 优化效果

- **UV Packing**: 重新打包 UV 以减少贴图尺寸
- **Texture Atlasing**: 合并多个材质贴图
- **Vertex Shuffling**: 优化顶点顺序（无 VertexIndexUsage 时）

### 7.3 Asset Description (v1.7+)

为 AAO 提供资产信息的配置文件。

#### 创建方式

`Create > Avatar Optimizer > Asset Description` (Project 窗口右键菜单)

#### 可配置信息

| 信息 | 说明 |
|------|------|
| **Meaningless Components** | AAO 应忽略的组件类型（Script Asset） |
| **Parameters Read By External Tools** | OSC 等外部工具读取的参数 |
| **Parameters Changed By External Tools** | OSC 等外部工具修改的参数 |

#### OSC 兼容性关键用例

> ⚠️ 如果 PhysBone/Contact Receiver 的参数仅用于 OSC 开关（未在 Animator/Expression 中定义），AAO 会误删。

**解决方案**:
1. 将 OSC 使用的参数添加到 Expression Parameters 列表
2. 或在 Asset Description 中声明这些参数

---

## 8. 常见问题与解决方案

### 8.1 OSC 相关组件被误删

**原因**: PhysBone/Contact Receiver 的参数未在任何 Animator/Expression 中定义，AAO 认为是未使用的。

**解决**:
```
方案 A: 在 Expression Parameters 中添加 OSC 使用的参数名
方案 B: 创建 Asset Description 文件，声明被 OSC 读取的参数
```

### 8.2 VRCSDK 预构建检查阻止上传

**原因**: VRCSDK 在编译前检查性能等级，但 NDMF 工具尚未运行，显示的是编译前状态。

**解决**: 参考 AAO FAQ 中的跳过预构建检查方法。

### 8.3 Performance Rank 不可靠

**原因**: NDMF 非破坏性工具在编译时才生效，VRCSDK Control Panel 显示的是编译前状态。

**解决**: 使用 anatawa12's Gist Pack 的 Actual Performance Window 在 Play Mode 中查看真实性能。

### 8.4 Merge Skinned Mesh 后 Root Bone 不正确

**原因**: AAO Merge Skinned Mesh 不会自动设置 Root Bone。

**解决**: 手动设置合并后 Mesh 的 Root Bone（通常是 Hips）。

### 8.5 合并材质后出问题

**原因**: 不同性质的材质被错误合并（如透明材质和实体材质）。

**解决**:
- Merge Material: 确保同一合并组内使用完全相同的 Shader
- 取消勾选 Merge Materials 中的 Merge 选项

---

## 9. 版本历史关键节点

| 版本 | 关键变化 |
|------|----------|
| **v1.7.0** | Component API 引入、Asset Description 引入 |
| **v1.8.0** | Shader Information API 引入 |
| **v1.9.0** | MeshRenderer 支持 (Remove Mesh By Box/Mask/UV Tile, Merge Material)、Merge ToonLit Material 废弃、NDMF 管线延迟执行、RemoveMeshByMask 组件 API |
| **v1.9.13** | (前一稳定版) 维护性更新 |
| **v1.9.14** | **当前版本 (2026-06-03)** — 维护性更新 + 性能 Linting 持续迭代 |
| **v1.9.x** | Animator Optimizer (AnyState → Entry-Exit → BlendTree 转换)、Merge Material 继任 Merge ToonLit Material、Max Texture Size 组件、Performance Linting |

---

## 10. 与其他优化工具的关系

| 工具 | 职责 | 与 AAO 关系 |
|------|------|-------------|
| **Modular Avatar** | 非破坏性 Avatar 构建 | AAO 在 MA 之后执行 |
| **lilAvatarUtils** | 性能检测 | 互补（检测 + 优化） |
| **TexTransTool** | 材质 Atlas 化 | AAO v1.9 Merge Material 部分替代 |
| **Meshia Mesh Simplification** | 自动减面（Burst+Job，替代 lilNDMF） | 互补（AAO 去遮挡 + 减面工具减面） |
| **Meshia Cascading Avatar Mesh Simplifier** | 级联减面 | 互补 |
| **anatawa12's Gist Pack** | Actual Performance Window | 验证 AAO 优化效果 |

---

## 11. 相关文档

- `optimization-guide.md` — 完整最佳化实操指南（含 AAO 操作步骤）
- `ndmf-tools.md` — NDMF 工具生态与安装方式
- `performance-rank.md` — PC/Quest 性能等级标准
- `modular-avatar.md` — Modular Avatar 完整知识库
- `teaching-methodology.md` — Avatar 改模教学法与问题诊断框架
