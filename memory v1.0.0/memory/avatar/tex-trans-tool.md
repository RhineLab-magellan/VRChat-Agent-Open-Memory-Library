# TexTransTool (TTT) — 非破坏性纹理改写工具

> 来源: ReinaS-64892/TexTransTool + 官方文档 (ttt.rs64.net)
> 置信度: High
> GitHub: https://github.com/ReinaS-64892/TexTransTool
> 文档: https://ttt.rs64.net

---

## ⚠️ 能力边界（用户最关心的问题）

> **用户诉求**："压材质槽"
> **TTT 的实际能力**：压**材质球** + 压 **VRAM**，**不直接压材质槽**

| 优化对象 | TTT 是否能做 | 需要什么 |
|----------|--------------|----------|
| **Material（材质球）数量** | ✅ 可以 | `AtlasTexture` + `AllMaterialMergeReference` |
| **Texture VRAM 占用** | ✅ 可以 | `AtlasTexture` 图集化 |
| **Material Slot（材质槽位）数量** | ❌ **不可以** | 必须配合 `AvatarOptimizer.MergeSkinnedMesh` |
| **Skinned Mesh 数量** | ❌ 不做 | 由 AvatarOptimizer 处理 |
| **PhysBone 数量** | ❌ 不做 | 由 AvatarOptimizer 处理 |
| **Mesh 面数** | ❌ 不做 | 由 lilNDMFMeshSimplifier / Mantis 处理 |

**结论**：
- 想**真正减少材质槽** → TTT + AAO MergeSkinnedMesh 双管齐下
- 想**让 Avatar 看起来只有 N 个材质** → 用 TTT 的 AllMaterialMergeReference 把所有材质合并到 Quest 材质

官方文档原话（[Tutorial/ReductionTextureMemoryByAtlasing](https://ttt.rs64.net/docs/Tutorial/ReductionTextureMemoryByAtlasing)）：
> AtlasTexture のマテリアルの結合は **マテリアルをまとめるだけ** で、**マテリアルスロットの結合はできません**。
> メッシュをマージしながらマテリアルスロットも削減できる Anatawa12/AvatarOptimizer の TraceAndOptimize や MergeSkinnedMesh との併用を強く推奨します。

---

## 概述

**TexTransTool (TTT)** 是一个**非破坏性纹理改写工具**，在 Unity Editor 内提供：

1. **贴花（Decal）**：直观的颜色/图案覆盖，可跨越 UV 边界
2. **图集化（Atlas）**：智能合并多张纹理到一张，削减 VRAM
3. **专用纹理导入**：非破坏地为 Avatar 应用纹理替换
4. **PSD 导入与多层画布**：在 Unity 内编辑 PSD 层级

**与同类工具的根本区别**：

| 维度 | 传统做法 | TexTransTool |
|------|----------|--------------|
| **修改材质** | 直接编辑 .mat 文件（破坏性） | 添加 NDMF 组件，编译时改写 |
| **修改纹理** | Blender UV 重排 + 重导 PNG | Editor 内 AtlasTexture 一键完成 |
| **回滚** | 需要 Git/手动备份 | 禁用/删除组件即可 |
| **可叠加性** | 单次操作 | 多组件链式组合 |

---

## 安装

### VPM 安装（推荐）

```
VCC/ALCOM → Add Repo → 粘贴:
vcc://vpm/addRepo?url=https://vpm.rs64.net/vpm.json
```

然后在项目 Settings > Packages 中启用：
- ✅ **TexTransTool**
- ✅ **TexTransCore**（自动安装，TTT 唯一硬依赖）
- ✅ **NDMF**（如果项目已有 Modular Avatar / AvatarOptimizer 会自动安装）

### 必须依赖

| 包 | 说明 | 来源 |
|----|------|------|
| **NDMF** v1.7.0+ | Non-Destructive Modular Framework | 随 MA 自动安装 |
| **TexTransCore** v0.2.x+ | TTT 核心 C# 库（Generic 部分） | 随 TTT 自动安装 |

### 可选依赖

| 包 | 说明 | 备注 |
|----|------|------|
| **TTCE-Wgpu** v0.2.0+ | ComputeShader 后端（实验性） | TTT v0.10.7+ 可选启用 |
| **ReinaS' lilToon NDMF Utility** | lilToon 材质规范化 | AtlasTexture BakeProperty 替代品 |
| **AvatarOptimizer** | 强协作 | 减少 Material Slot |
| **Modular Avatar** | 强协作 | 兼容运行 |

---

## 架构与目录

```
TexTransTool/
├── Editor/              # 编辑器扩展（核心 UI）
├── Runtime/             # 运行时组件
├── MultiLayerImageData/ # 多层图像数据（PSD/Canvas 用）
├── ParserUtility/       # 解析器工具
├── TTCE-Unity/          # Texture Trans Core Engine (Unity 集成)
├── TTT-PSDImporter/     # PSD 导入器
├── TestCode/            # 测试代码
├── DependentUpdater~/   # 依赖更新（VPM）
├── CHANGELOG.md         # 完整版本历史
├── CHANGELOG-EXPERIMENTAL.md  # 实验性功能变更
├── LICENSE.md
└── package.json
```

**依赖分层**：
```
TexTransTool (TTT)
  └── TexTransCore (硬依赖，唯一)
        └── TTCE-Wgpu (可选，ComputeShader 后端)
```

---

## 核心组件清单（15 个）

### A. 优化类（核心：图集化）

| 组件 | 类型 | 说明 |
|------|------|------|
| **AtlasTexture** | MainComponent + OwnedComponent | **图集化（VRAM 削减 + 材质合并）** — 整个 TTT 的核心 |
| TextureFineTuning | OwnedComponent | AtlasTexture 的纹理压缩/格式配置 |

### B. 改类（Decal 系）

| 组件 | 类型 | 说明 |
|------|------|------|
| **SimpleDecal** | MainComponent | 简单贴花 — 直观、跨 UV 边界 |
| SingleGradationDecal | MainComponent | 单色渐变贴花（专用头发等） |
| DistanceGradationDecal | MainComponent | 距离渐变贴花 |
| ParallelProjectionWithlilToonDecal | MainComponent | lilToon 并行投影贴花 |
| MultiLayerImageCanvas | MainComponent | 多层图像画布（Photoshop-like） |

### C. 纹理改写/混合类

| 组件 | 类型 | 说明 |
|------|------|------|
| **TextureBlender** | MainComponent | 纹理混合（专用纹理导入） — Stable v0.9.0 |
| ColorDifferenceChanger | MainComponent | 颜色差异变换 |
| TextureConfigurator | OwnedComponent | 纹理配置（压缩/分辨率/MipMap） |
| MaterialModifier | MainComponent | 材质修改 |
| NearTransTexture | MainComponent | 近透明纹理 |
| MaterialOverrideTransfer | MainComponent | 材质覆盖传输 |

### D. 选择器/工具类

| 组件 | 类型 | 说明 |
|------|------|------|
| IslandSelector | MainComponent | UV 岛选择器 |
| BoxIslandSelector | OwnedComponent | 盒子范围选择 |
| SphereIslandSelector | OwnedComponent | 球形范围选择 |
| PinIslandSelector | OwnedComponent | 点选 |
| IslandSelectorAND/OR/XOR/NOT | OwnedComponent | 逻辑组合 |
| UVCopy | MainComponent | UV 复制 |

### E. 其他

| 组件 | 类型 | 说明 |
|------|------|------|
| TexTransToolPSDImporter | Importer | PSD 文件导入器 |

**组件稳定性**（v1.0.0 状态）：
- **Stable**：AtlasTexture / SimpleDecal / TextureBlender / SingleGradationDecal / IslandSelector 系
- **Experimental**：DistanceGradationDecal / NearTransTexture / MultiLayerImageCanvas / ColorDifferenceChanger

> 💡 **判断方法**：组件 Inspector 顶部会显示"实验的"警告横幅

---

## ⭐ AtlasTexture 详解（"压材质球"核心）

### 概述

> **核心定位**：通过收集纹理中"需要的部分"重新排列到一张图集，**减少 VRAM 占用**。
> **设计灵感**：AvatarOptimizer (AAO) 的非破坏性 Mesh 合并 → TTT 的非破坏性 Texture 合并
> **历史**：TTT v0.0.0 时期即存在，是 TTT 最早的核心组件（最初叫 AtlasSet，工具名也叫 TexturAtlasCompiler）

### 工作原理（两步核心算法）

1. **UV 再配置（2D Bin Packing）**：把每个材质的 UV island 重新排列到一张大纹理上
2. **UV 转写到新纹理**：根据新的 UV 重新生成纹理内容（早期用重心坐标系，现已改为矩形转写）

**性能**：v0.1.x 时单个图集化需 2 分半；现在秒级完成（GPU 加速）

### Atlas 化前置条件

**Renderer 必须满足**：
- ✅ 编译时 Active（或勾选「適用時に非アクティブなレンダラーを含める」）
- ✅ tag ≠ EditorOnly
- ✅ 有 Mesh + UV0
- ✅ 有 1+ 个材质

**材质 Shader 支持**：

| Shader | 支持度 |
|--------|--------|
| **lilToon** | ✅ 完全支持（含 MatCap / Shadow / 3rd / NormalMap / HSVG 等所有变体） |
| **Standard** | ✅ 支持 |
| **VRCSDK StandardLite** | ✅ 支持 |
| **VRCSDK ToonLit** | ✅ 支持 |
| **其它 Shader** | ⚠️ 默认按 `_MainTex` 走 UV0，可在 `ITTShaderTextureUsageInformation` 扩展 |

### 完整配置项

| 参数 | 日文原名 | 类型 | 说明 |
|------|----------|------|------|
| **Material Selector** | マテリアルセレクター | Material 列表 | 勾选要图集化的材质（未勾选的不参与） |
| **Refresh Materials** | - | 按钮 | 刷新材质列表 |
| **Island Size Priority** | アイランド大きさ優先度 | 结构 | 调整 Island 大小优先级 |
| └ Set From Material | - | 元素 | 按材质分配优先级 |
| └ Set From Island Selector | - | 元素 | 按 Island Selector 分配 |
| **Material Merge Group** | マテリアル結合グループ | 结构 | 分组合并材质 |
| └ Group | - | 结构 | 每组内的材质合并到指定 Reference |
| **All Material Merge Reference** | すべてのマテリアル結合時参照 | Material | 全材质合并目标（**Quest 适配关键**）|
| **Atlas Texture Size** | アトラステクスチャーサイズ | 2 的幂 | 输出纹理大小（默认正方形） |
| **Custom Aspect** | カスタムアスペクト | bool | 启用自定义宽高比 |
| └ Atlas Texture Height | アトラステクスチャーの縦のサイズ | int | 高度上限 |
| **Atlas Target UV Channel** | アトラス対象のUVチャンネル | enum | UV0 / UV1 / UV2 / UV3 |
| **Padding** | パディング | float | Island 间隔（UV 尺度） |
| **Include Disable Renderer** | 適用時に非アクティブなレンダラーを含める | bool | 包含非活跃 Renderer |
| **Force Size Priority** | 大きさの優先度を強制 | bool | 强制按优先级缩放（不因空间不足） |
| **Force Set Texture** | テクスチャーを強制的にセットする | bool | 强制覆盖材质纹理（无纹理也强制） |
| **Background Color** | 背景色 | Color | Atlas 背景色（影响 mipmap 和压缩） |
| **Pixel Normalize** | ピクセルノーマライズ | bool | 像素对齐（避免纹理劣化） |

### 标准工作流程

```
1. Avatar 根节点右键 → Create → TexTransTool/TTT AtlasTexture
   ↓ 自动在 Avatar 内创建 GameObject "AtlasTexture"，列出所有材质
2. 勾选要合并的材质（Material Selector）
3. 按性质分组（如皮肤/头发/衣服/半透明/金属）
   ↓ 不同性质的材质不能合在一组（透明混合会出错）
4. 设定合并目标（All Material Merge Reference）
   ↓ 可选：把所有材质合并到一个 Quest 材质
5. 调整 Atlas Texture Size（一般 2048 或 4096）
6. 运行 Manual Bake Avatar 或 Play 模式触发
   ↓ NDMF Console 应显示无错，并显示 Atlas 再配置结果
7. 验证：跟随 Renderer 的 Material → 查看新纹理
8. 上传时自动应用
```

### 关键设计原则

**按性质分组（必须）**：
> ⚠️ 必须按材质性质分组（皮肤/头发/衣服/半透明/玻璃/金属），否则透明材质会混合错误
> 复杂材质合并出问题？尝试烘焙：备份材质 → 选合适烘焙选项 → 完成

**材质合并不是材质槽合并**：
- 合并材质：减少 Material 文件数（用 Merge Reference）
- 合并材质槽：必须用 AAO MergeSkinnedMesh

### Quest 适配（关键工作流）

```
目标：让 Quest 端只看到 1 个材质（Quest Material）

1. 把所有材质都加入图集化（Material Selector 全选）
2. All Material Merge Reference → 设为 Quest 专用材质
3. Force Set Texture 勾选（强制覆盖纹理）
4. 运行 Build → Quest 端：所有材质合并到一个，纹理也合并
```

**原理**：PC 端保留原材质细节，Quest 端强制替换为 Quest Material（手 Mobile 优化的简单 Shader）

---

## SimpleDecal 详解（直观贴花）

### 核心优势

> **对比传统贴花**：传统需要 UV 编辑软件、可能跨越 UV 边界失败
> **TTT SimpleDecal**：Unity 内操作、直观、**可跨越 UV 边界**

### 标准工作流程

```
1. Avatar 根节点右键 → Create → TexTransTool/TTT SimpleDecal
2. 设置 Decal Texture（贴花纹理）
3. 调整位置/角度（Gizmo 直观操作）
4. 调整 Scale / MaxDistance
5. （可选）启用 Material Filtering 限制范围
6. （可选）启用 Island Selector 进一步限制
7. Manual Bake / Play / Upload
```

### 关键功能

| 功能 | 说明 |
|------|------|
| **Material Filtering** | 只对特定材质生效 |
| **Island Selector** | 用 UV Island 级别限制 |
| **Back Culling** | 背面剔除（v0.9.0 改名前叫 SideCulling） |
| **Auto / Manual Select** | v0.9.0 新增 Auto 自动选择模式 |
| **Color Multiply** | v0.3.0 起支持贴花颜色调整 |

### 性能

- v0.1.x：单个贴花需 5 秒（CPU 实现）
- v0.9.0：ComputeShader 实现，秒级
- v0.10.x：高质量 Padding（v0.2.x 风格回归）

---

## MultiLayerImageCanvas（Photoshop-like 多层画布）

### 是什么

> 在 Unity Editor 内直接编辑 PSD 多层图像，无需 Photoshop

### 关联组件

| 组件 | 说明 |
|------|------|
| **MultiLayerImageCanvas** | 画布主组件 |
| LayerFolder | 文件夹层 |
| RasterLayer | 光栅图层 |
| SolidLayer | 单色图层 |
| **TexTransToolPSDImporter** | PSD 导入器（右键 Asset 即可使用）|

### 使用场景

- ✅ 在 Unity 内直接编辑 Avatar 纹理的图层（添加新元素、修改颜色）
- ✅ PSD 文件作为 Avatar 纹理源的导入
- ⚠️ **状态**：Experimental（实验性）

---

## NDMF 协作：与 AvatarOptimizer 深度集成

### v0.9.0 起的关键集成

**集成 1：RemoveMeshBy\* 与 AtlasTexture 协作**

```
问题：AAO Remove Mesh By BlendShape 删除某些面，
      但 AtlasTexture 不知道，仍会为这些面预留图集空间 → 浪费
解决：AtlasTexture 通过 AAO API 知晓哪些区域将被删除，
      不为这些区域分配图集空间 → 节省图集面积
```

**集成 2：UV 通道共享**

```
问题：AAO 把原 UV 写入 Mesh UV1，
      AtlasTexture 改 UV0 会破坏 AAO 的引用
解决：AtlasTexture 通过 AAO API 报告 UV 改写位置，
      AAO 可正确同步
```

### 推荐 NDMF 执行顺序

```
1. MA + 其他 NDMF 工具（增加/修改内容类）
2. AtlasTexture / SimpleDecal / Decal 系（TTT）
3. AvatarOptimizer.MergeSkinnedMesh（合并 Mesh + Material Slot）
4. AAO.TraceAndOptimize（最终优化）
```

### Mantis LOD Editor 协作

> v0.8.11 起修复：TTT 必须在 Mantis LOD Editor **之后**执行（Mantis 可能减面）

---

## ⚠️ 重要故障排查（FAQ 精选）

### 1. 上传/Play/Manual Bake 时不生效

**原因**：
- 组件未 Active → **激活**组件
- NDMF 未安装 → **安装 NDMF**（v1.7.0+）
- 预发布版本不匹配 → 同时更新 NDMF 到预发布版

### 2. Gizmo 不显示

**原因 1**：SceneView 右上角 Gizmo 总开关关闭
- 解决：点击启用（图标变蓝）

**原因 2**：组件单独 Gizmo 开关关闭
- 解决：Gizmo 总开关右边的下拉菜单中重新启用

### 3. 图标碍事

**方案**：Gizmo 总开关下拉 → 调小 `3D Icons` 或单独禁用
**高级**：用[作者提供的脚本](https://gist.github.com/ReinaS-64892/ea5162bec70ab23404b4b0b4d9033726)批量禁用

### 4. GTX10XX/9XX + DirectX11 故障 ⚠️

**已知问题 GPU**：
- GTX 1080 / 1070 TI / 1070 / 1060
- GTX 980

**影响组件**：
- SimpleDecal / SingleGradationDecal（v0.9.x 必坏）
- TexTransTool PSD Importer

**修复**：
- ✅ **v0.10.0** 已修复（务必升级）
- 🔧 临时方案：UnityEditor 用 Vulkan 启动
  ```
  ALCOM → 项目管理 → 修改启动选项 → 定制命令行参数 → 添加 -force-vulkan → 保存
  ```

### 5. AMD Radeon + DirectX11 故障

**影响组件**：TTT PSD Importer（v0.9.x ~ v0.10.x）
**修复**：使用 Vulkan（方法同上）

### 6. VMware 故障

> 确认环境 VMware Workstation 17 Pro 17.6.2 build-24409262
> ComputeShader 实现与 VMware 不兼容，连最基础的 NotBlend Blending 都失败
> **无解**：换用其他环境

### 7. TTT 资产不工作

**原因**：资产由旧版本 TTT 创建
**修复**：
```
1. 备份 Prefab
2. Tools > TexTransTool > Migrator 打开
3. 运行迁移
```

### 8. 旧资产升级到 v0.8.x+ 后报错

> v0.8.x 移除了 `ReferenceResolver`，v0.9.x 移除了 `TexTransListGroup`
> **必须**：通过 Migrator 窗口执行迁移

---

## Quest 适配完整流程

### 设计目标

> Quest 端只有 1 个材质（Quest Material），占用最小 VRAM
> PC 端保留全部材质细节

### 推荐设置

```
AtlasTexture GameObject:
├ Material Selector:
│   ☑ All Materials（全部勾选）
├ All Material Merge Reference:
│   └ Quest Material（拖入 Quest 专用 Shader 的材质）
├ Force Set Texture:
│   ☑ True（强制覆盖）
├ Atlas Texture Size:
│   └ 2048 或 4096（视模型复杂度）
└ Material Merge Group:
    └ 留空（用 All Material Merge Reference 替代）
```

### 效果

- ✅ Quest 端所有 Renderer 用同一材质（节省 Material Slot 调用）
- ✅ 所有纹理合并到 1 张（节省 VRAM × N）
- ⚠️ Quest 材质必须用 Mobile 优化 Shader（推荐 lilToon）

### AAO 协作

```
1. TTT 处理：所有纹理合并 + Quest Material 替换
2. AAO 处理：Skinned Mesh 合并（Material Slot 真正减少）
3. 最终：Material Slot 极少 + VRAM 极小 + 性能 Excellent
```

---

## TexTransCore 是什么？

> TTT 唯一的硬依赖，托管在 [github.com/ReinaS-64892/TexTransCore](https://github.com/ReinaS-64892/TexTransCore)

**作用**：TTT 的 C# Generic 部分（与 Unity 解耦），因版本管理需要分离
**必要性**：无 TexTransCore 则 TTT 无法运行
**管理**：随 TTT 自动安装，无需手动操作

## TTCE-Wgpu 是什么？

**作用**：TTT 的 ComputeShader 后端（实验性）
**必要性**：可选
**何时使用**：解决特定 GPU 兼容性 / 性能优化
**文档**：[https://ttt.rs64.net/docs/TexTransTool-ExtensionPackages/TTCE-Wgpu](https://ttt.rs64.net/docs/TexTransTool-ExtensionPackages/TTCE-Wgpu)

---

## 版本演进（重点变更）

| 版本 | 日期 | 关键变更 |
|------|------|----------|
| **v0.1.0** | 2023-06-02 | 初次发布（SimpleDecal + TextureBlender + AtlasSet） |
| **v0.3.0** | 2023-09-04 | AtlasTexture 加入（取代 AtlasSet） |
| **v0.4.0** | 2023-10-07 | **NDMF 官方支持** |
| **v0.9.0** | 2025-02-17 | **NDMF Preview** + AAO RemoveMeshBy* 协作 + ComputeShader 实现 |
| **v0.10.0** | 2025-05-14 | **大改动**：Marge→Merge、BakeProperty 删除、TexTransGroup 删除、DirectX11+GTX10 修复 |
| **v1.0.0** | 2025-06-22 | **稳定版**：清理旧数据、ProjectMigrationDialog 删除 |
| **v1.0.1** | 2025-12-26 | IOS 构建修复 |

### ⚠️ v0.10.0 破坏性变更清单

| 旧名称 | 新名称 |
|--------|--------|
| AtlasTexture.MargeMaterial | AtlasTexture.AllMaterialMergeReference |
| AtlasTexture.MergeMaterialGroup | 标记为 Stable（不再实验） |
| MipMapRemove | MipMap（语义改变） |
| TexTransGroup | **删除** |
| HighQualityPadding（Decal 系） | **删除** |
| BakeProperty（AtlasTexture） | **删除**（功能迁至 ReinaS' lilToon NDMF Utility） |
| LimitCandidateMaterials | **删除**（合并到 Material Selector） |
| SimpleDecal.MultiRendererMode | **删除**（默认多 Renderer） |
| SimpleDecal.PolygonCulling | **删除**（修复后不再需要） |

### v1.0.0 进一步变更

- Minor 升级对话框删除（不再提示升级）
- v0.8.x 及更早的 SaveData **不再兼容**（需通过旧版本迁移）

---

## 设计哲学（ReinaSakiria's Note 摘录）

### 关于 AtlasTexture

> 「AtlasTexture 是 TTT 的第一个组件，v0.0.0 时代就有了」
> 「原型叫 AtlasSet，工具本身的名字是 TexturAtlasCompiler」
> 「当时候实现一个图集化要 2 分半，现在秒级」
> 「这个组件是为我自己做的——因为我受够了 UV パズル」

### 关于 v1.0.0 的承诺

> 「TTT v1.0.0 之后是最后的设计改动了」
> 「TexTransTool Unity 版不会到 v2.0.0」
> 「如果变，那也是 AtlasTextureV2 而不是改 AtlasTexture」

### 关于协作设计

> 「TTT 的设计哲学：让 Avatar 制作者摆脱 UV 拼图的痛苦」
> 「AAO 的 Mesh 合并能力 → TTT 的 Texture 合并能力」
> 「像 AAO 那样把所有东西在 Build 时合并——我不用再设计 UV」

---

## 调试技巧

### 查看图集化结果

```
1. NDMF Console → 查看 AtlasTexture 报告
   → 显示 UV 再配置详情、生成纹理大小
2. 在 Scene 中选中 Renderer → 查看 Material → 查看 Texture
   → 应该是图集化后的纹理（UV 已重映射）
```

### 性能验证

```
1. Tools > AvatarUtils（lilAvatarUtils）
   → 拖入 Avatar → 查看 Material Slot / Texture Memory
2. 启用 Actual Performance Window
   → Tools > anatawa12's gist selector → 勾选 ActualPerformanceWindow → Apply Changes
   → Tools > anatawa12's gist → 勾选 Compute actual Performance on Play
   → 进入 Play 模式查看真实性能
```

### 错误处理

- **NDMF Console 报错** → 展开错误详情，通常给出具体修复建议
- **Manual Bake Avatar 不可用** → 组件未 Active
- **NDMF Preview 不显示变化** → 检查 TexTransGroup 嵌套问题

---

## 实用组合配方

### 配方 1：完整 Avatar 优化流程

```
1. 复制 Avatar（备份原始）
2. 复制 FX Layer / Expression Menu / Expression Parameter
3. 删除开关物件相关 Animator（保留 Blend Shape）
4. 在复制 Avatar 上：
   a. TTT AtlasTexture（合并材质 + 图集化）
   b. TTT SimpleDecal（如果需要贴花）
   c. AAO Merge Skinned Mesh（合并 Skinned Mesh + Material Slot）
   d. AAO Trace And Optimize（一键最终优化）
   e. lilNDMFMeshSimplifier（如果面数过多）
5. 把 FX / 参数 / Menu 塞回复制的 Avatar
6. 上传
```

### 配方 2：Quest 适配（最低配置）

```
1. TTT AtlasTexture：
   - Material Selector: 全选
   - All Material Merge Reference: Quest Material
   - Force Set Texture: True
2. AAO Trace And Optimize
3. 验证 Quest 端：1 个材质 + 1 张图集
```

### 配方 3：专用纹理导入（Modular Avatar 用户）

```
1. Avatar 根 → 右键 → TTT TextureBlender
2. 选择要修改的纹理槽（如 Face 纹理）
3. Blend Texture: 拖入专用纹理
4. 上传：专用纹理生效
5. 不用时：禁用或删除 TextureBlender GameObject（不影响原 Avatar）
```

---

## 相关文档

### 内部知识库

- `memory/avatar/ndmf-tools.md` — NDMF 生态与 TexTransTool 简介
- `memory/avatar/optimization-guide.md` — 完整 Avatar 优化实操（AtlasTexture 章节）
- `memory/avatar/performance-rank.md` — Performance Rank 标准
- `memory/avatar/modular-avatar.md` — Modular Avatar（与 TTT 互补）
- `memory/avatar/avatar-modding-guide.md` — Avatar 改模通用指南

### 官方资源

- **GitHub**: https://github.com/ReinaS-64892/TexTransTool
- **文档站**: https://ttt.rs64.net
- **VPM**: `vcc://vpm/addRepo?url=https://vpm.rs64.net/vpm.json`
- **TexTransCore**: https://github.com/ReinaS-64892/TexTransCore
- **Discord**: https://discord.gg/dV4cVpewmM (NDMF Discord)

### 关键 PR/Issue 参考

- **#900** (v0.10.0 AtlasTexture 全面重构)
- **#904** (GTX10/9 + DX11 修复)
- **#908** (Mantis LOD Editor 协作)
- **#962** (NDMF v1.7.0+ 适配)
- **#1003** (lilycalInventory 优先级)
- **#1010** (v1.0.0 迁移警告)

---

## 速查决策表

| 用户需求 | 推荐方案 |
|----------|----------|
| 减少 Texture VRAM | TTT AtlasTexture |
| 减少 Material 数量 | TTT AtlasTexture + AllMaterialMergeReference |
| 减少 Material Slot | **AAO MergeSkinnedMesh**（TTT 不做） |
| 添加 Avatar 贴花 | TTT SimpleDecal |
| 头发渐变 | TTT SingleGradationDecal |
| 导入专用纹理 | TTT TextureBlender |
| PSD 文件作为纹理 | TTT PSD Importer |
| Quest 适配 | TTT AtlasTexture + AllMaterialMergeReference |
| 完整 Avatar 优化 | TTT + AAO + lilNDMFMeshSimplifier 组合 |
| GTX10/9 + DX11 故障 | 升级 TTT v0.10.0+ 或用 Vulkan |

---

## 知识库版本

- **v1.0** — 首次系统化入库
  - 从 GitHub README + 官方文档 ttt.rs64.net + CHANGELOG.md 整合
  - 重点确认了"压材质槽 vs 压材质球"的能力边界
  - 包含 15 个核心组件的完整清单
  - 包含 AtlasTexture 完整参数表
  - 包含 v0.10.0/v1.0.0 破坏性变更记录
  - 包含与 AAO 协作的设计细节