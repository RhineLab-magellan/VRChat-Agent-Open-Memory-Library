# Avatar 最佳化实操指南

> 来源: Kuriko Avatar 最佳化笔记（HackMD）
> 置信度: High | 更新: 2026-06-05

---

## 速查懒人包

```
1. 复制 Avatar 的 FX Layer、Expression Menu、Expression Parameter
2. 删除所有跟开关物件相关的设定（保留表情 Blend Shape）
3. 复制 Avatar 本身
4. 导入 **AAO + Avatar Compressor (LAC) + Meshia** Mesh Simplification
5. 运行 AAO Trace And Optimize（自动 + LAC 自动纹理压缩 + Meshia 减面）
6. 面数还太多 → Remove Mesh By BlendShape / Meshia 减面 / 脱掉
7. 把 FX、参数、选单塞回复制出来的 Avatar
```

> 💡 **2026 推荐做法**：在第 4 步加入 Avatar Compressor (LAC) 自动处理纹理压缩，详见 `lac-avatar-compressor.md`

---

## AAO Trace And Optimize（自动最佳化）

> 📚 **完整 AAO 组件知识库**: `avatar-optimizer.md` — 12 个组件详解 + API + 优化方向矩阵
> 文档: https://vpm.anatawa12.com/avatar-optimizer/en/docs/reference/trace-and-optimize/

### 自动处理项目

- ✅ 合并 Skinned Mesh
- ✅ 固定目前状态的 Blend Shape 并删除
- ✅ 删除未使用物件
- ✅ 删除没有实质作用的 end 骨
- ✅ 删除没有作用的 PhysBone
- ✅ Animator 最佳化

### 使用方法

```
1. 选择 Avatar 物件本身
2. Inspector > Add Component > AAO Trace And Optimize
3. 完成
```

### 注意事项

> ⚠️ 若 Animator 中有开关物件的 Animation，会跳过 Skinned Mesh 合并

---

## Light（光源）

**规则：没事不要放。**

| Excellent | Good | Medium | Poor |
|-----------|------|--------|------|
| 0 | 0 | 0 | 1 |

如果嫌 Avatar 太暗，调整 Shader，而非加灯。

---

## Particle System（粒子系统）

**无法最佳化，只能控制数量。**

| 指标 | Excellent | Good | Medium | Poor |
|------|-----------|------|--------|------|
| 粒子系统数 | 0 | 4 | 8 | 16 |
| 粒子总数量 | 0 | 300 | 1,000 | 2,500 |
| 粒子系统面数 | 0 | 1,000 | 2,000 | 5,000 |

**控制要点**：
- Max Particles 调整粒子最大数量
- Poor 极限是 2,500，超出会 Very Poor
- 粒子轨迹/碰撞根据需求开关
- Trail Renderer 会吃掉 2 个材质球

---

## Texture Memory（材质贴图内存）

### 关键原则

> 💡 无论原档是 PNG/JPG/PSD，解析度多高多低，**最终 VRAM 使用量只依 Unity 内设定决定**

### 降分辨率技巧

| 物件类型 | 推荐分辨率 |
|----------|-----------|
| 主贴图 | 2048 以下 |
| 鞋子等不明显物件 | 512 附近 |
| 遮罩贴图 | 128 也行 |
| MatCap 部位 | 32 级别 |

### 压缩建议

| 压缩方式 | 适用场景 | 注意 |
|----------|----------|------|
| Normal | 普通贴图 | 对 R 频道破坏大 |
| High Quality | 皮肤等贴图 | 无 A 频道的贴图用 High 会 VRAM 加倍 |
| Crunch | 下载大小优化 | VRAM 不变，不推荐 |

> ⚠️ Crunch Compression：下载变小，但贴图破坏 + 解压资源 + VRAM 不变

### 全自动纹理压缩方案（2026 推荐）⭐NEW

> 工具: **Avatar Compressor (LAC)** — 详见 `lac-avatar-compressor.md`
> VPM: `https://vpm.limitex.dev/`

**为什么不手动设置**:
- 每张贴图都要设 Max Size + Compression + 平台格式（繁琐）
- 容易把 Normal Map 当 Albedo 压缩（破坏法线）
- 共享贴图容易重复处理
- 无 VRAM 预估（盲调）

**LAC 自动化**:
- 4 种分析策略（Fast / HighAccuracy / Perceptual / Combined）
- 5 个内置预设（开箱即用）
- 自动平台格式选择（PC: BC7 / Quest: ASTC_4x4）
- 自动贴图类型识别（Normal/Emission/Metallic 等）
- 共享贴图识别
- 编译前 VRAM 预估

**与 AAO 协作顺序**: LAC → AAO（详见 `ndmf-tools.md`）

### VRAM 与分辨率关系

- 每降一级分辨率 → VRAM 变为 **1/4**
- 每升一级分辨率 → VRAM **×4**

**推荐目标**: 单 Avatar VRAM < 75MB（Good），活动用 < 40MB（Excellent）

> 💡 **2026 推荐做法**：使用 Avatar Compressor (LAC) 自动达成上述目标，无需手动逐张设置。详见 `lac-avatar-compressor.md`

---

## Skinned Mesh Renderer（蒙皮网格）

### 合并条件

能配合身体骨架变形的物件可以合并。

### 合并好处

- CPU 处理负担降低
- Material Slots 同步合并（同一材质球的多 Mesh 算一个 Slot）

### 代价

> ⚠️ 无法单独开关其中某个物件（不能穿脱衣服）

### Face（头）特殊处理

Face 的 Blend Shape 数量通常最多，全部合并反而增加负担。

**建议**：头髮、身体等可合并，Face 保持独立。

### Excellent 挑战

1. 把 `Body` 也扔进 MergeMesh
2. 使用 `Freeze BlendShape` 固定外观并删除 Blend Shape

### AAO Merge Skinned Mesh 步骤

```
1. 在 Avatar 物件上 Add Component > AAO Merge Skinned Mesh
2. 绑定 Root Transform（通常是 Hips）
3. 设置 Anchor Override（建议用 Body）
4. 将要合并的物件拖入「添加元素」
5. 取消勾选 Optimize BlendShape（如需保留）
```

---

## Material Slots（材质栏位）

### Material vs Material Slots

| 概念 | 定义 | 影响 |
|------|------|------|
| Material（材质球） | 以文件为单位 | 无 |
| Material Slots（材质栏位） | 编译后实际数量 | 影响 Performance Rank |

### 减少方式

1. **合并 Skinned Mesh** — 同材质球的多 Mesh 合并后算一个 Slot
2. **合并材质球（Atlas 化）** — 使用 TexTransTool

### TexTransTool Atlas 化

> 工具: https://ttt.rs64.net/ — **完整文档: `tex-trans-tool.md`**
> 当前版本: v1.0.1（2025-12-26）

#### ⚠️ 能力边界（重要）

> TexTransTool 可以压**材质球** + **VRAM**，但**不直接压材质槽**（Material Slot）
> 想真正减少 Material Slot → **必须配合 AvatarOptimizer.MergeSkinnedMesh**

#### 注意事项

> ⚠️ 必须按材质性质分组（皮肤/头髮/衣服/半透明/玻璃/金属），否则透明材质会混合错误

#### 分组方法（v1.0.1 当前）

```
AtlasTexture GameObject:
├ Material Selector: 勾选要合并的材质球
├ Material Merge Group: 按性质分组（实验性→稳定）
├ All Material Merge Reference: 指定所有材质合并目标
├ Atlas Texture Size: 输出纹理大小（2 的幂）
└ Force Set Texture: 强制覆盖纹理（Quest 适配用）
```

> 💡 v0.10.0 后：`MergeMaterial` → `AllMaterialMergeReference`（语义更清晰）

#### Quest 适配关键步骤

```
1. Material Selector 全选所有材质
2. All Material Merge Reference → Quest 专用材质
3. Force Set Texture → True
4. Build → Quest 端：1 个材质 + 1 张图集
```

#### 烘焙技巧

复杂材质合并出问题？尝试烘焙：

```
1. 备份该材质球
2. 选择适合的烘焙选项
3. 完成
```

感谢 Touma 分享。

#### 与 AvatarOptimizer 协作（v0.9.0+）

```
执行顺序（关键）：
1. TTT AtlasTexture（图集化、合并材质球）
2. AAO MergeSkinnedMesh（合并 Mesh + Material Slot）
3. AAO TraceAndOptimize（最终优化）
```

v0.9.0 起 TTT 与 AAO 通过 API 深度协作：
- AAO RemoveMeshBy* 删除的区域不会分配图集空间
- AAO UV 写入 UV1 时 TTT 通过 API 报告改写位置

#### 故障排查速查

| 问题 | 原因 | 解决 |
|------|------|------|
| 上传不生效 | 组件未 Active | 激活组件 |
| 上传不生效 | NDMF 未安装 | 安装 NDMF v1.7.0+ |
| GTX10/9 + DX11 故障 | 已知 GPU 兼容问题 | 升级 v0.10.0+ 或用 Vulkan |
| Gizmo 不显示 | SceneView 开关 | 启用 Gizmo 总开关 |
| 旧资产不工作 | SaveData 不兼容 | Tools > TexTransTool > Migrator |

---

## PhysBone 最佳化

> 简称 PB

### 两种实装方式

| 方式 | 优点 | 缺点 |
|------|------|------|
| 直接建立在 Transform | 安装简单，不需指定 Root | 管理困难，散布各处 |
| 建立在空白物件内 | 管理方便，可批量启用/停用 | 需手动指定 Root Transform |

### 合并 PhysBone

#### 合并条件

1. 不同 PB 的上一级必须有共同 Root Transform（不可超过两级）
2. 设定数值必须**完全一致**

#### 限制

> ⚠️ 抓取只能抓一边（同时抓两边有一边没反应），摇晃与碰撞不受影响

#### 合并步骤（Transform 内）

```
1. 展开 Armature，找到有相同设定的 PB
2. 在共同 Root Transform 上新建空白物件（如 Hair_Side）
3. 将左右 PB 拉入该物件层级
4. Add Component > AAO Merge PhysBone
5. 将左右 PB 拖入添加元素
```

#### 合并步骤（空白物件内）

```
1. 展开物件，检查所有 PB 的 Root Transform 位置
2. 找到可合并的 PB（如 Ear_L 和 Ear_R）
3. 新建空白物件（如 Ear），将 PB 拉入
4. Add Component > AAO Merge PhysBone
5. 拖入目标 PB
```

### 停用/删除 PhysBone

**停用方向**：
- 会捏/拽但很少人用的 PB（脸颊等）
- 太小/移动幅度不明显的 PB

**终极做法**：如果 PB 影响物件关闭后不影响整体，直接删除。

### 碰撞器优化

> 💡 大多数 Avatar 本身已内建完善 Collider，衣服自带的可以替换

**替换步骤**：
```
1. 固定 PB 的 Inspector
2. 找到 Avatar 本体相同位置的 Collider
3. 替换衣服自带的 Collider
4. 删除衣服自带 Collider 元件
```

---

## Bones（骨頭）合并

> 工具: AAO Merge Bone

### 作用

将目标骨融合至上一级父骨，减少一根骨。

**一举三得**：
1. 减少 Bones 数量
2. 减少 PB 影响骨头数
3. 避免设定 PhysBone Ignore 时末端不能动的问题

### 合并技巧

> 💡 融合间隔选择（上半部移动幅度小的保留，下半部移动幅度大的也保留）

### 注意事项

> ⚠️ 融合后若有 PhysBone，动态效果可能变僵硬

**调整方法**：降低 Pull、Momentum、Immobile。

感谢 Touma 与夜嵐蝶 Alma 介绍。

---

## Polygons（面数）减面

### AAO Remove Mesh 系列

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| **Remove Mesh By BlendShape** | 删除隐藏身体部位的面数 | 使用 Blend Shape 隐藏身体防止穿模时 |
| **Remove Mesh By Mask** | 用遮罩贴图移除 | 多物件做在同 Skinned Mesh 时 |
| **Remove Mesh By Box** | 用方块裁切 | 无法用 Blend Shape 或 UV 时 |
| **Remove Mesh By UV Tile** | 按 UV Tile 移除 | 移除特定材质球的所有面数 |

### Remove Mesh By BlendShape

> 💡 Blend Shape 隐藏身体后，隐藏部分面数不会消失，只是被挤成一坨看不见的东西

**使用方法**：
```
1. 选择有 Blend Shape 的物件
2. Add Component > Remove Mesh By BlendShape
3. 勾选用于隐藏身体的 Blend Shape
4. 完成
```

### Remove Mesh By Box

可以与 Mask 组合使用，砍得更精准。

### 减面工具对比

| 工具 | 优点 | 缺点 | 价格 | 状态 |
|------|------|------|------|------|
| Mantis LOD Editor | 模型不易破洞 | 调整时卡顿 | **$50** | ✅ 活跃 |
| **Meshia Mesh Simplification** | Burst 高速、BlendShape 保留、防破洞选项丰富 | 需配置 Options | 免费 | ✅ **推荐** |
| lilNDMFMeshSimplifier | 导入即见效 | 看不到面数、无防破洞 | 免费 | ❌ **已废弃** |

### Meshia Mesh Simplification 使用技巧

> 📖 **完整技术文档**: `meshia-mesh-simplification.md`
> 💡 该工具不会计算其他 NDMF 工具处理过的结果，实际面数可能低于目标

#### 单 Mesh 模式（`MeshiaMeshSimplifier`）

```
1. 选择目标 GameObject
2. Add Component → MeshiaMeshSimplifier
3. 配置 Target（MeshSimplificationTargetKind + Value）
4. EditMode 实时预览
```

#### Avatar 级联模式（`MeshiaCascadingAvatarMeshSimplifier`）

```
1. 在 Avatar 根节点下创建空 GameObject
2. Add Component → MeshiaCascadingAvatarMeshSimplifier
3. 选择目标 Performance Rank
4. 调整每个 Mesh 的面数分配 + Options
```

#### 三个关键修复选项

| 问题 | 启用选项 |
|------|----------|
| 指尖/边缘破洞 | `PreserveBorderEdges = true` |
| UV 接缝纹理扭曲 | `UseBarycentricCoordinateInterpolation = true` |
| 曲面失真 | `PreserveSurfaceCurvature = true` |

#### 其他技巧

- 使用 `Enable Auto Adjust` 批量调整
- 使用锁头固定特定物件面数
- v3.1+ 支持按骨配置 Border Edges（更精细）
- 目标面数设太低时调高预期
- **不要混用 lilNDMF + Meshia**（同类工具重复执行）

---

## 批次上传

> 工具: Continuous Avatar Uploader

**建议**：
- 分散到多个 Asset 管理（建议每个 5~10 只）
- 出错时从出错那组重新上传（类似存档点）
- 单个 Asset 建议不超过 10 只

---

## 相关文档

- `avatar-optimizer.md` — AAO: Avatar Optimizer 完整组件知识库 (12 组件 + API)
- `performance-rank.md` — Performance Rank 标准
- `ndmf-tools.md` — NDMF 工具生态与获取方式
- `meshia-mesh-simplification.md` — Meshia 减面工具完整技术文档
