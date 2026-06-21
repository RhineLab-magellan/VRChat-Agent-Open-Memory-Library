# Thry Avatar Evaluator 7 项指标完整阈值

> Type: RULE / METRIC
> Source: Thryrallo/VRC-Avatar-Performance-Tools v1.3.7 (AvatarEvaluator.cs + TextureVRAM.cs)
> Confidence: High (Tier A — 源码验证)

---

## 概述

本文档是 VRChat 官方 Performance Rank 系统(`performance-rank.md`)的**重要补充**。官方系统只检测基础指标,而 **Thry Avatar Evaluator** 检测了 7 项官方未覆盖或检测方式不同的关键指标。

**使用建议**:优化 Avatar 时,**同时运行两个工具**——官方 Performance Rank + Thry Evaluator。

---

## 指标速查表(全部 7 项)

| # | 指标 | 单位 | Excellent | Good | Medium | Poor | Very Poor |
|---|------|------|-----------|------|--------|------|-----------|
| 1 | VRAM (Texture, PC) | MiB | < 40 | < 75 | < 110 | < 150 | ≥ 150 |
| 2 | VRAM (Texture, Quest) | MiB | < 10 | < 18 | < 25 | < 40 | ≥ 40 |
| 3 | VRAM (Mesh, PC) | MiB | < 20 | < 35 | < 55 | < 80 | ≥ 80 |
| 4 | VRAM (Mesh, Quest) | MiB | < 5 | < 10 | < 15 | < 25 | ≥ 25 |
| 5 | GrabPass 数量 | 个 | 0 | 0 | 1 | 1+ | 2+ |
| 6 | Blendshape 影响三角形 | 个 | < 8,000 | < 16,000 | < 32,000 | < 50,000 | ≥ 50,000 |
| 7 | AnyState Transitions | 个 | < 50 | < 80 | < 100 | < 150 | ≥ 150 |
| 8 | Animator Layer Count | 层 | < 12 | < 20 | < 30 | < 45 | ≥ 45 |

> 注:工具本身的 AvatarEvaluator.cs 中只检测 1-7 项的前 4 项使用统一阈值;Layer Count 是独立的 5 级阈值(来源:AvatarEvaluator.cs:51-55)。

---

## 1. VRAM Size

### 1.1 检测方法

调用 `TextureVRAM.QuickCalc(avatar)` 累加:
- 所有 Texture (含 Material 的 TextureProperty + AnimationClip 的 Material Override)
- 所有 SkinnedMeshRenderer / MeshRenderer 的 sharedMesh

**关键排除**:Tag 为 `EditorOnly` 的对象会被跳过。

### 1.2 计算公式

**Texture VRAM**:
```
VRAM_texture = Σ_mipmap (width × height × bpp / 8)
```

**Mipmap 链累计**:
- Mipmap 0(原图):`width × height × bpp / 8`
- Mipmap N:`(width × height >> 2N) × bpp / 8`
- 总倍数 ≈ 1.33(等比数列)

**Mesh VRAM**:
```
VRAM_mesh = Σ_vertexAttributes (byte × dimension × vertexCount) + blendShapeVRAM
```

**SkinnedMesh 特殊处理**:Position / Normal / Tangent 各占 **2 倍**(同时存储未蒙皮和蒙皮后数据)。

**BlendShape 额外开销**:每个受影响的顶点 +40 bytes。

### 1.3 PC vs Quest 双套阈值

```csharp
// 来源: TextureVRAM.cs:38-57
const long PC_TEXTURE_MEMORY_EXCELLENT_MiB = 40;
const long PC_TEXTURE_MEMORY_GOOD_MiB = 75;
const long PC_TEXTURE_MEMORY_MEDIUM_MiB = 110;
const long PC_TEXTURE_MEMORY_POOR_MiB = 150;
const long PC_MESH_MEMORY_EXCELLENT_MiB = 20;
const long PC_MESH_MEMORY_GOOD_MiB = 35;
const long PC_MESH_MEMORY_MEDIUM_MiB = 55;
const long PC_MESH_MEMORY_POOR_MiB = 80;

const long QUEST_TEXTURE_MEMORY_EXCELLENT_MiB = 10;
const long QUEST_TEXTURE_MEMORY_GOOD_MiB = 18;
const long QUEST_TEXTURE_MEMORY_MEDIUM_MiB = 25;
const long QUEST_TEXTURE_MEMORY_POOR_MiB = 40;
const long QUEST_MESH_MEMORY_EXCELLENT_MiB = 5;
const long QUEST_MESH_MEMORY_GOOD_MiB = 10;
const long QUEST_MESH_MEMORY_MEDIUM_MiB = 15;
const long QUEST_MESH_MEMORY_POOR_MiB = 25;
```

### 1.4 优化建议(来自工具内置提示)

```
1. 分辨率:从 1 米距离看 Avatar,降低直到出现明显质量下降
2. 压缩格式:
   - 有 Alpha / NormalMap → BC7 (8 bpp, 质量高) 或 DXT5 (8 bpp, 下载体积小)
   - 无 Alpha → DXT1 (4 bpp)
3. BC7 和 DXT5 的 VRAM 大小相同,差别在下载体积和质量
4. >2048 纹理一键缩小到 2K(质量损失很小)
```

### 1.5 多 Avatar 累加效应

工具硬编码的提示信息(应作为常识记住):

```
"Taking into account a world VRAM usage of 2GB:
 - 40 个 Avatar × 150MB = 6GB(RTX 3070 8GB 几乎用完)
 - 80 个 Avatar × 150MB = 12GB(超额,GPU 必须 swap 到系统内存)"
```

**这就是为什么 Avatar VRAM 控制对多人场景至关重要。**

---

## 2. GrabPass

### 2.1 检测方法

Regex 匹配 shader 源文件:

```csharp
// 来源: AvatarEvaluator.cs:436
Regex.Match(File.ReadAllText(shaderPath), @"GrabPass\s*{\s*""(\w|_)+""\s*}")
```

匹配标准格式:`GrabPass { "TextureName" }`。

### 2.2 阈值(简化分级)

```csharp
// 来源: AvatarEvaluator.cs:41-42
const int GRABPASS_LIMIT_EXCELLENT = 0;
const int GRABPASS_LIMIT_MEDIUM = 1;
// > 1 → VeryPoor
```

| 数量 | 等级 |
|------|------|
| 0 | Excellent |
| 1 | Medium |
| ≥ 2 | Very Poor |

### 2.3 为什么 GrabPass 危险

**原理**:GrabPass 在某一渲染点抓取**整个屏幕内容**保存为纹理,供后续 Shader 采样。

**性能成本**(每次 GrabPass):
1. CPU 端:触发一次额外的 RenderTexture 分配
2. GPU 端:把当前 framebuffer 重新拷贝一遍到显存
3. 分辨率成本:如果屏幕 4K,一次 GrabPass 占用 ≈ 4K RGBA32 = 33.18 MiB 临时显存

**典型应用**(几乎都有更好替代方案):
- 折射玻璃 / 水面 → 用 RenderTexture + 平面反射代替
- 屏幕扭曲后处理 → 用 PostProcess Volume 代替
- 描边 / Outline → 用 Mesh 复制 + 缩放代替

### 2.4 优化建议

| 原方案 | 替代方案 |
|--------|----------|
| 折射玻璃 | BoxProjection + Environment Reflection |
| 屏幕扭曲后处理 | PostProcess Volume + Shader Graph |
| 实时反射 | Bakery Reflection Probe(预烘焙) |

### 2.5 检测盲点

- ❌ **检测不到**无名称的 `GrabPass {}`(工具会漏报)
- ❌ **检测不到**通过 `#define` 启用的 GrabPass
- ❌ **检测不到**自定义 Shader 关键字触发的 GrabPass
- 仅适用于**本地源文件**的 Shader,无法处理二进制 Shader

---

## 3. Blendshapes (影响三角形总数)

### 3.1 检测方法

```csharp
// 来源: AvatarEvaluator.cs:445
_skinendMeshesWithBlendshapes = avatar.GetComponentsInChildren<SkinnedMeshRenderer>(true)
    .Where(r => r.sharedMesh != null && r.sharedMesh.blendShapeCount > 0)
    .Select(r => (r, r.sharedMesh.triangles.Length / 3, r.sharedMesh.blendShapeCount))
    .OrderByDescending(i => i.Item2)
    .ToArray();
_totalBlendshapeVerticies = _skinendMeshesWithBlendshapes.Sum(i => i.verticies);
```

**关键**:统计的是**有 BlendShape 的 SkinnedMeshRenderer 的三角形总数**,不是 BlendShape 个数本身。

### 3.2 阈值

```csharp
// 来源: AvatarEvaluator.cs:47-50
const int BLENDSHAPE_DATA_LIMIT_EXCELLENT = 8000;
const int BLENDSHAPE_DATA_LIMIT_GOOD = 16000;
const int BLENDSHAPE_DATA_LIMIT_MEDIUM = 32000;
const int BLENDSHAPE_DATA_LIMIT_POOR = 50000;
```

| 三角形数 | 等级 |
|---------|------|
| < 8,000 | Excellent |
| < 16,000 | Good |
| < 32,000 | Medium |
| < 50,000 | Poor |
| ≥ 50,000 | Very Poor |

### 3.3 性能影响原理

**Mesh 的 BlendShape 系统每帧**:
1. 对每个 BlendShape 通道
2. 计算每个顶点的偏移(delta position / normal / tangent)
3. 加到原始顶点上,生成新的 GPU buffer
4. 上传 GPU → 触发顶点 shader 重计算

**所以**:即使是 1 个 BlendShape,如果作用在 50,000 三角形的 mesh 上,每帧都要处理 50,000 顶点 × 3 (pos/normal/tangent) = 150,000 次运算。

### 3.4 优化建议(工具内置提示)

工具对 >32,000 三角形的 mesh 直接给出 Error 级警告:

```
"Consider splitting '[mesh_name]' into multiple meshes where only one 
 has blendshapes. This will reduce the amount polygons actively 
 affected by blendshapes."
```

**标准做法**:
```
优化前: 1 个 50,000 三角形 mesh + 10 个 BlendShape
        → 每帧处理 500,000 顶点偏移

优化后: 
  - 静态 mesh(45,000 三角形,无 BlendShape)
  - 动态 mesh(5,000 三角形,10 个 BlendShape)
        → 每帧只处理 50,000 顶点偏移(减少 10 倍)
```

**应用工具**:
- AAO (AvatarOptimizer) - Merge Skinned Mesh / Remove Mesh in Box
- Modular Avatar - 不直接处理,可结合使用

---

## 4. AnyState Transitions

### 4.1 检测方法

```csharp
// 来源: AvatarEvaluator.cs:428-429
IEnumerable<AnimatorControllerLayer> layers = descriptor.baseAnimationLayers
    .Union(descriptor.specialAnimationLayers)
    .Select(a => a.animatorController)
    .Where(a => a != null)
    .SelectMany(a => (a as AnimatorController).layers)
    .Where(l => l != null);
_anyStateTransitions = layers.SelectMany(l => l.stateMachine).SelectMany(m => m.anyStateTransitions).Count();
```

### 4.2 阈值

```csharp
// 来源: AvatarEvaluator.cs:43-46
const int ANYSTATE_LIMIT_EXCELLENT = 50;
const int ANYSTATE_LIMIT_GOOD = 80;
const int ANYSTATE_LIMIT_MEDIUM = 100;
const int ANYSTATE_LIMIT_POOR = 150;
```

| AnyState 数量 | 等级 |
|--------------|------|
| < 50 | Excellent |
| < 80 | Good |
| < 100 | Medium |
| < 150 | Poor |
| ≥ 150 | Very Poor |

### 4.3 性能影响原理

工具内置解释:

```
"For each any state transition the conditions are checked every frame. 
 This makes them expensive compared to normal transitions and a large 
 number of them can seriously impact the CPU usage. A healthy limit 
 is around 50 transitions."
```

**核心问题**:AnyState Transition 在 Unity Animator 中是**贪婪匹配**:
- 每个 AnyState Transition 都会对当前所有参数求值
- 即使条件不满足,每帧都要检查
- 而 Normal Transition 只在源 State 激活时才检查

**示例**:100 个 Toggle × 2 AnyState Transition(开/关) = 200 个 AnyState,每帧要检查 200 次条件。

### 4.4 优化建议

**方法 1: 合并条件**
```
优化前: 50 个 Toggle 各 2 个 AnyState(On/Off) = 100 个 AnyState
优化后: 使用 Animator Parameter Driver + 1 个总开关
```

**方法 2: 使用 Modular Avatar 的 Merge Animator**
- MA Merge Animator 会自动合并重叠的 Layer
- 减少 Layer 数同时减少 AnyState 数

**方法 3: 用 Bool Trigger 替代 AnyState**
- 在 State 内用 Trigger Transition 而非 AnyState
- Trigger 只在该 State 激活时检查

### 4.5 与性能基准测试的对照

`performance-benchmarks.md` 显示:

> | AnyState 切换数量 | 无显著影响 |
> | 启用"可以过渡到自身" | +20% 开销 |

**注意**:JustSleightly 的测试显示 AnyState 数量本身影响不大,但 **+ "可以过渡到自身"(Can Transition To Self)** 会带来 20% 开销。

**实践**:超过 100 个 AnyState 时,即便单项性能不显著,**累积效应**会导致其他指标恶化(主线程占用增加)。

---

## 5. Layer Count

### 5.1 检测方法

```csharp
// 来源: AvatarEvaluator.cs:443
_layerCount = layers.Count();
```

统计 `baseAnimationLayers + specialAnimationLayers` 的总和。

### 5.2 阈值

```csharp
// 来源: AvatarEvaluator.cs:51-54
const int LAYER_LIMIT_EXCELLENT = 12;
const int LAYER_LIMIT_GOOD = 20;
const int LAYER_LIMIT_MEDIUM = 30;
const int LAYER_LIMIT_POOR = 45;
```

| Layer 数 | 等级 |
|---------|------|
| < 12 | Excellent |
| < 20 | Good |
| < 30 | Medium |
| < 45 | Poor |
| ≥ 45 | Very Poor |

### 5.3 性能影响原理

工具内置解释:

```
"The more layers you have the more expensive the animator is to run. 
 Animators run on the CPU, so in a CPU-limited game like VRC the 
 smaller the layer count, the better."
```

**每 Layer 的成本**:
- 每帧处理 Layer 内的所有 State
- 计算权重、混合 BlendTree
- 检查 Transition 条件

`performance-benchmarks.md` 给出基准:

> | 主动频繁切换 | 比被动高 20-30% |
> | 每增加1层额外开销 | ~0.01 ms |

虽然单层便宜,但**累积效应**显著:
- 45 层 × 0.01 ms = 0.45 ms/帧(占 90 FPS 预算的 4.1%)
- 加上主动切换的 20-30% 增量 = 0.55-0.6 ms/帧

### 5.4 优化建议

**方法 1: 合并冗余 Layer**
- 用 Modular Avatar 的 Merge Animator
- 把 Base / Additive / Gesture 合并到同一 Controller

**方法 2: 使用 Animator Parameter 替代独立 Layer**
- 不要每个 Toggle 一个 Layer
- 用 1 个 Layer + BlendTree + Parameter Driver

**方法 3: 删除空 Layer**
- 工具的 "Empty States Check" 会提示

---

## 6. Write Defaults Check

### 6.1 检测方法

```csharp
// 来源: AvatarEvaluator.cs:431-434
IEnumerable<(AnimatorState, string)> wdOn = states.Where(s => s.Item1.writeDefaultValues);
IEnumerable<(AnimatorState, string)> wdOff = states.Where(s => !s.Item1.writeDefaultValues);
_writeDefault = wdOn.Count() >= wdOff.Count();
if (_writeDefault) _writeDefaultoutliers = wdOff.Select(s => s.Item2).ToArray();
else _writeDefaultoutliers = wdOn.Select(s => s.Item2).ToArray();
```

**算法**:多数方为推荐设置,少数方为 outliers(不一致项)。

### 6.2 工作原理

Animator State 的 "Write Defaults" 决定:当**退出**该 State 时,所有被该 State 动画化的属性是否**恢复到默认值**。

**Write Defaults ON**(True):
- State 退出时,所有动画属性 → 默认值
- 适合简单的开关 Toggle
- 容易出问题:跨 Layer 时如果 Layer A 的 State 没动画化 Layer B 控制的属性,Layer A 退出时会把 Layer B 的属性"重置"到默认值

**Write Defaults OFF**(False):
- State 退出时,属性保持当前值
- 适合复杂系统
- 不会"重置"其他 Layer 的属性

### 6.3 为什么必须一致

工具提示:

```
"Unity needs all the states in your animator to have the same write 
 default value: Either all off or all on."
```

**技术原因**:Animator 在 Layer 之间混合时,会用**统一规则**处理所有属性。如果不一致,会导致属性在 State 切换时出现**抖动 / 跳变**。

### 6.4 优化建议

**统一策略**:
- 在 Project Settings → 选择"All Off"或"All On"为默认值
- Unity 2018+ 默认是 Off(更安全)

**修复 outliers**:
1. 工具列出所有不一致的 State 路径:`LayerName/StateName`
2. 在 Animator 窗口中选中该 State
3. 在 Inspector 中勾选/取消 "Write Defaults"
4. 重新运行工具确认

---

## 7. Empty States Check

### 7.1 检测方法

```csharp
// 来源: AvatarEvaluator.cs:430
_emptyStates = states.Where(s => s.Item1.motion == null).Select(s => s.Item2).ToArray();
```

扫描所有 state.motion == null 的 state,输出路径列表。

### 7.2 常见原因

1. **制作疏忽**:删除 Motion 后忘了清理 State
2. **导入 Avatar 时丢失**:从其他工程导入的 Controller 可能引用了丢失的 AnimationClip
3. **MA / Fury 生成**:某些模块化组件可能生成空 State(尤其是使用 MA Merge Animator 时)

### 7.3 为什么 Empty States 有问题

工具提示:

```
"Some of your states do not have a motion. This might cause issues. 
 You can place an empty animation clip in them to prevent this."
```

**潜在问题**:
- Unity 在某些情况下会发出警告
- 可能影响 Layer Weight 计算
- 在 VRC 上传时可能被 Performance Rank 误判

### 7.4 优化建议

**修复方法**:
1. 创建 1 个 0 长度的 Empty AnimationClip(右键 → Create → Animation)
2. 把它拖到所有空 State 的 Motion 槽
3. 重新运行工具确认 outliers 为空

**预防**:
- 使用 MA Merge Animator 时检查生成结果
- 在 Animator 窗口用 `Select > Missing Motion` 过滤

---

## 工作流集成

### 优化前检测

```bash
# 在 Unity 中:
1. 选中 Avatar
2. 右键 → Thry/Avatar/Evaluator
3. 记录 6 项指标的当前等级 + outliers
4. 右键 → Thry/Avatar/VRAM
5. 记录每纹理 / 每 Mesh 的 VRAM 用量
```

### 优化决策树

```
Total VRAM VeryPoor?
├─ 是 → VRAM Checker 一键优化(降分辨率 / 改压缩)
└─ 否
   │
   └─ Blendshape VeryPoor?
      ├─ 是 → AAO Remove Mesh in Box 或手动拆分 Mesh
      └─ 否
         │
         └─ AnyState VeryPoor?
            ├─ 是 → 重构 Animator(合并 Toggle / 用 Trigger)
            └─ 否
               │
               └─ Layer Count VeryPoor?
                  ├─ 是 → MA Merge Animator
                  └─ 否
                     │
                     └─ GrabPass VeryPoor?
                        └─ 是 → 替换 Shader(BoxProjection / Probe)
```

### 优化后验证

```bash
1. 再次运行 Avatar Evaluator
2. 确认所有指标 ≤ Medium
3. 再次运行官方 Performance Rank(SDK Build & Test)
4. 两者都通过 → 上传 VRChat
```

---

## 与官方 Performance Rank 的对照表

| 维度 | 官方 Performance Rank | Thry Evaluator |
|------|----------------------|----------------|
| 面数 | ✅ | ❌ |
| 材质球数 | ✅ | ❌ |
| 材质内存(总 Texture) | ✅ | ❌(但 VRAM Checker 更细) |
| Skinned Mesh Renderer 数 | ✅ | ❌ |
| PhysBone 元件数 | ✅ | ❌ |
| **VRAM 详细分解** | ❌ | ✅ |
| **Mesh VRAM** | ❌ | ✅ |
| **GrabPass** | ❌ | ✅ |
| **Blendshape 三角形** | ❌ | ✅ |
| **AnyState Transitions** | ❌ | ✅ |
| **Layer Count** | ❌ | ✅ |
| **Write Defaults** | ❌ | ✅ |
| **Empty States** | ❌ | ✅ |
| 审核依据 | ✅(VRChat 官方) | ❌(参考用) |

**结论**:**两者互补使用**。Thry 工具是开发者自检工具,官方 Performance Rank 是上传门槛。

---

## 关联文档

- `memory/sources/vrc-avatar-performance-tools.md` — 工具本身介绍
- `memory/avatar/performance-rank.md` — 官方 Performance Rank 标准
- `memory/avatar/performance-benchmarks.md` — JustSleightly 性能基准
- `memory/avatar/optimization-guide.md` — Kuriko 完整最佳化实操
- `memory/avatar/ndmf-tools.md` — NDMF 工具生态(AAO / Meshia / TexTransTool)
- `memory/avatar/animator-system.md` — Animator 基础知识