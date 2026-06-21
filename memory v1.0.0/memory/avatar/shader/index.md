# Avatar Shader 知识库索引

> 记录 Avatar 制作中常用的着色器及其配置知识
>
> **最后更新**: 2026-06-11
> **来源**: Agent 会话 Shader 分析结果整合

---

## 快速检索：按用途分类

> 🎯 **一键定位**：根据你的需求选择对应分类

### 🎭 Avatar 专用 Shader（VRChat 改模首选）

| Shader | 核心优势 | 文档 |
|--------|----------|------|
| **lilToon** | 30%+ 市场占有率、功能最全面、预设丰富 | `liltoon/` |
| **SCSS** | 双阴影系统、UV 服装切换零 Draw Call、Matcap 最灵活 | `scss.md` |

> 📌 特点：Avatar 动态骨骼优化、Expression Menu 集成、Quest 详细指南

---

### 🌍 World 专用 Shader（World 开发首选）

| Shader | 核心优势 | 文档 |
|--------|----------|------|
| **ORL Shaders** | 40+ 模块化 Shader、Configurable 系统、VFX 特效库 | `orl/` |
| **Filamented** | Standard 一键替换、Fresnel 修复、VRC Light Volumes | `filamented/` |

> 📌 特点：非 Avatar 专用，无 DynamicBone 优化；面向 World 环境/VFX/PBR 需求

---

### 🔧 通用 Shader（Avatar + World 皆可）

| Shader | 核心优势 | 文档 |
|--------|----------|------|
| **UnlitWF** | Fur/Water/Grass/Gem 专业效果、BRP+URP 双支持 | `unlitwf/index.md` |

> 📌 特点：基于 Unlit 扩展，效果专业；需根据平台选择变体

---

### 📦 其他 Shader（参考）

| Shader | 定位 | 说明 |
|--------|------|------|
| **z3y/shaders** | World PBR 高级 | LTCGI/Bakery 完整集成，暂未详细分析 |
| **GeneLit** | World PBR 高级 | Clearcoat/Sheen 等高级特性，暂未详细分析 |
| **Graphlit** | World 节点编辑器 | Google Filament 节点式编辑，暂未详细分析 |

---

## 目录

```
avatar/shader/
├── index.md                    ← 本索引文件（含用途分类快速检索）
│
├── 🎭 Avatar 专用
├── liltoon/                    ← lilToon（30%+ VRChat 模型使用）
│   ├── index.md               ← lilToon 总览
│   ├── overview.md            ← 概述与特性
│   ├── installation.md        ← 安装与配置
│   ├── render-modes.md        ← 渲染模式详解
│   ├── basic-settings.md      ← 基本设置
│   ├── color-settings.md      ← 颜色与阴影设置
│   ├── reflection-settings.md  ← 反射与光泽设置
│   ├── advanced-settings.md    ← 扩展功能设置
│   ├── outline.md             ← 轮廓线设置
│   ├── fur.md                 ← 毛发设置
│   ├── stencil.md             ← Stencil 设置
│   ├── audiolink.md           ← AudioLink 集成
│   ├── dissolve.md            ← Dissolve 效果
│   ├── optimization.md        ← 优化指南
│   ├── vrchat-specific.md     ← VRChat 特定配置
│   ├── troubleshooting.md      ← 常见问题解决
│   └── variations.md          ← 着色器变体
├── scss.md                    ← SCSS（双阴影系统/UV服装切换）
│
├── 🌍 World 专用
├── orl/                       ← ORL Shaders（模块化着色器套件）
│   ├── index.md              ← ORL 总览
│   ├── overview.md           ← 项目概览与安装
│   ├── shader-list.md        ← 详细 Shader 列表
│   ├── configurable.md       ← Configurable 模块化系统
│   └── comparison.md         ← 与其他 Shader 对比
├── filamented/                ← Filamented（Google Filament PBR 替代）
│   ├── index.md              ← Filamented 总览
│   ├── overview.md           ← 项目概览
│   ├── pbr-improvements.md   ← PBR 改进详解
│   └── comparison.md         ← 与同类项目对比
│
├── 🔧 通用（Avatar + World）
├── unlitwf/                   ← UnlitWF（Unlit 扩展专业效果）
│   └── index.md              ← UnlitWF 总览、Shader 家族、效果系统
│
└── 📦 其他
└── other-shaders.md          ← 其他着色器（Graphlit 等）
```

---

## Shader 总览对比表

| Shader | 用途 | 市场占有率 | 许可证 | 渲染管线 | 活跃度 |
|--------|------|-----------|--------|----------|--------|
| **lilToon** | 🎭 Avatar | 30%+ VRChat | MIT | BRP/URP/HDRP | ⭐⭐⭐⭐⭐ |
| **SCSS** | 🎭 Avatar | 较低 | MIT | BRP Only | ⭐⭐⭐ |
| **ORL Shaders** | 🌍 World | 较高 | MIT | BRP | ⭐⭐⭐⭐ |
| **Filamented** | 🌍 World | 较小众 | Apache 2.0 | BRP | ⭐⭐⭐ |
| **UnlitWF** | 🔧 通用 | 较小众 | zlib | BRP/URP | ⭐⭐⭐⭐⭐ |

---

## 一、Avatar 专用 Shader

### 1.1 lilToon(主流首选)

| 属性 | 说明 |
|------|------|
| **定位** | VRChat 改模界主流 Toon Shader,功能全面、社区资源最丰富 |
| **文档** | https://lilxyzw.github.io/lilToon/ja_JP/ |
| **VCC 安装** | `https://lilxyzw.github.io/vpm-repos/vpm.json` |

**核心特性**：
- ✨ **简单 (Easy)**: 预设一键设置、色调校正、自定义预设保存
- 🎨 **美观 (Beautiful)**: 动漫渲染、抗锯齿、白飞防止、半透明穿透防止
- 🎈 **轻量 (Lightweight)**: 编辑器自动优化、Build Size 最小化、Avatar 容量削减
- 🔑 **稳定 (Stable)**: 全 Unity 照明支持、Standard Shader 相似亮度

**优势**：
- ✅ 全渲染管线支持（BRP/URP/HDRP）
- ✅ 功能最全面（fur/dissolve/stencil 等）
- ✅ 社区资源最丰富（教程/预设最多）
- ✅ 新手友好（一键预设）
- ✅ 详细 Quest 优化指南

**劣势**：
- ❌ 无 Configurable 模块化
- ❌ AudioLink 需手动配置
- ❌ 非 World 首选

**适用场景**：
- VRChat Avatar 通用选择
- 新手入门首选
- 需要大量社区资源/教程
- Quest Avatar 优化

**详细文档**：`memory/avatar/shader/liltoon/`（16个文件）

---

### 1.2 SCSS（Silent's Cel Shading Shader）

| 属性 | 说明 |
|------|------|
| **定位** | 功能全面的 Cel Shading 工具箱 |
| **许可证** | MIT License |
| **仓库** | https://github.com/s-ilent/scss |
| **文档** | https://gitlab.com/s-ilent/SCSS/-/wikis/Manual/Setting-Overview |

**核心特性**：
- 🎨 **双阴影系统**: Lightramp（纹理）+ Crosstone（参数）
- 👔 **UV Inventory System**: 零额外 Draw Call 服装切换
- ✨ **4 槽位 Matcap**: World/Tangent 空间（VR 优化）
- 📐 **VR 优化 Outline**: 距离自适应 + 顶点色控制
- 🎵 **AudioLink**: 每频段独立配置

**优势**：
- ✅ 双阴影系统业界领先
- ✅ UV 服装切换零额外 draw call
- ✅ Matcap 系统最灵活（多槽位+多模式）
- ✅ VR Outline 优化完善
- ✅ 开源透明（MIT License）

**劣势**：
- ❌ 仅支持 BRP（不支持 URP/HDRP）
- ❌ 无一键预设（需手动配置）
- ❌ 学习曲线较高（设置项繁多）
- ❌ 文档分散（GitLab Wiki）
- ❌ 社区资源较少

**服装切换对比**：
| 方法 | Draw Calls | 性能 | 限制 |
|------|-----------|------|------|
| **SCSS UV 切换** | 1 | 最低 | 需要 UV 编辑 |
| 分离网格 | N+1 | 较高 | 合并后更优 |
| ShapeKeys | - | 最高 | 每激活都昂贵 |
| 材质槽+隐形 | N+1 | 较高 | 每槽=1 drawcall |

**适用场景**：
- 需要精细 Matcap 控制的 Avatar
- 服装切换需求（高效零 Draw Call）
- 复杂 Outline 控制
- 双色调系统（Crosstone）

**详细文档**：`memory/avatar/shader/scss.md`

---

## 二、World 通用 Shader

### 2.1 ORL Shaders（模块化着色器套件）

| 属性 | 说明 |
|------|------|
| **定位** | VRChat World 通用模块化着色器套件(非 Avatar 专用) |
| **许可证** | MIT License |
| **仓库** | https://github.com/orels1/orels-Unity-Shaders |
| **文档** | https://shaders.orels.sh |
| **VCC 安装** | `https://orels1.github.io/orels-Unity-Shaders/index.json` |

**核心特性**：
- 🎛️ **Configurable Shader**: 可自由组合功能模块
- 🎨 **40+ Shader**: Standard PBR / Toon / VFX / UI
- 🎵 **AudioLink 内置**: 5 种模式（Band/UV/Waveform/Bar/Pulse）
- 💡 **VRChat 深度集成**: Shader Fallback / VRCLightVolumes / Camera View
- ✨ **丰富 VFX**: Shield / Laser / Clouds / Dissolve / Glitch

**Shader 分类**：
| 类别 | 数量 | 说明 |
|------|------|------|
| Standard Shaders (PBR) | 22 | 基础 PBR + 功能扩展 |
| Toon Shaders | 3 | 卡通渲染（v1/v2） |
| Special Shaders | 1 | 积雪覆盖 |
| VFX Shaders | 9 | 视觉效果特效 |
| UI Shaders | 5 | UI 专用着色器 |

**优势**：
- ✅ Configurable 模块化系统（自由组合功能）
- ✅ 丰富的 VFX 特效库（护盾/激光/云等）
- ✅ 内置 AudioLink 支持（5种模式）
- ✅ VRCLightVolumes 集成
- ✅ 专业的 PBR 实现（Parallax OM / GSAA / Mobile Tonemapping）

**劣势**：
- ❌ 非 Avatar 专用（DynamicBone 未优化）
- ❌ Quest 兼容性无明确分级
- ❌ Toon Shader 功能较少
- ❌ 学习曲线（Generator 工具）

**适用场景**：
- World 环境构建（地面/墙壁/建筑）
- 复杂材质组合（Configurable 系统）
- AudioLink 音频响应效果
- VFX 特效（护盾/激光/故障等）
- 需要 LTCGI / AreaLit 光照的 World

**详细文档**：`memory/avatar/shader/orl/`（4个文件）

---

### 2.2 Filamented（Google Filament PBR 替代）

| 属性 | 说明 |
|------|------|
| **定位** | Google Filament PBR 计算，Standard 替代 |
| **许可证** | Apache License 2.0 |
| **仓库** | https://gitlab.com/s-ilent/filamented |
| **Unity 版本** | 2022.3+ |

**核心特性**：
- 🔧 **100% 属性兼容**: 与 Standard 一键切换，无需重新制作材质
- ✨ **改进的 Fresnel**: 非金属不再过度反射
- 🌟 **Specular Occlusion**: Exposure 遮挡修正
- 💡 **VRC Light Volumes**: 完整支持

**优势**：
- ✅ 最小侵入性（Standard 一键替换）
- ✅ 改进的 Fresnel 计算
- ✅ Specular Occlusion
- ✅ VRC Light Volumes 完整支持
- ✅ 零迁移成本

**劣势**：
- ❌ 无 Anisotropy（切线方向高光拉伸）
- ❌ 无 Subsurface（次表面散射）
- ❌ 无 Clearcoat（清漆层）
- ❌ 无 LTCGI（Area Lights）
- ❌ 社区较小

**适用场景**：
- World 静态物体需要精确 PBR
- 从 Standard 升级，期望最小侵入性
- 需要 VRC Light Volumes 但不需要重型 Shader

**与其他 PBR Shader 对比**：
| 特性 | Filamented | z3y/shaders | GeneLit |
|------|------------|-------------|---------|
| Fresnel 修复 | ✅ | ✅ | ✅ |
| Specular Occlusion | ✅ | ✅ | ✅ |
| Anisotropy | ❌ | ✅ | ✅ |
| Subsurface | ❌ | ✅ | ✅ |
| LTCGI | ❌ | ✅ | ✅ |
| 复杂度 | 低 | 中 | 高 |

**详细文档**：`memory/avatar/shader/filamented/`（4个文件）

---

## 三、Unlit 扩展 Shader

### 3.1 UnlitWF Shader Suite（专业效果套件）

| 属性 | 说明 |
|------|------|
| **定位** | 基于 Unlit 的专业效果 Shader 套件 |
| **许可证** | zlib License |
| **仓库** | https://github.com/whiteflare/Unlit_WF_ShaderSuite |
| **Releases** | 102(持续维护) |

**核心架构 - drawing struct 模式**：

```hlsl
struct drawing {
    float4 color;         // 主颜色
    float3 ws_vertex;     // 世界空间位置
    float3 ws_normal;     // 世界空间法线
    float3 light_color;   // 光照颜色
};
```

**效果链式调用**：每个 `draw*()` 函数修改 `drawing` struct，实现模块化效果组合。

**Shader 家族**：
| 家族 | 特点 | 使用场景 |
|------|------|---------|
| Base UnToon | 基础 Toon 着色，完整效果链 | 通用 Avatar |
| PowerCap | 增强 Matcap，多个 Matcap 槽位 | 高级视觉效果 |
| TriShade | 三层阴影渐变 | 细腻阴影控制 |
| Tessellation | 硬件细分，平滑模型 | 高精度模型 |
| Outline | 内置轮廓线渲染 | 需要描边的模型 |

**专业效果系统**：
| 效果 | 说明 | 变体 |
|------|------|------|
| **FakeFur** | Geometry Shader 生成毛发（1-6层） | TransCutout/Transparent/Mix/FurOnly |
| **Water** | 波浪+焦散+Cubemap 反射 | Standard/Refracted/Opaque/Caustics |
| **Grass** | 风力模拟+高度染色 | WORLD_Y/UV/VERTEX_COLOR/MASK |
| **Gem** | Flake 效果+双面渲染 | Transparent/Opaque |
| **Particle** | 帧动画+顶点色混合 | Multiple blend modes |

**4 种透明度模式**：
| 模式 | Queue | 适用场景 |
|------|-------|---------|
| **Opaque** | Geometry | 实体对象 |
| **TransCutout** | AlphaTest | 叶子、头发 |
| **Transparent** | Transparent | 标准透明 |
| **Transparent3Pass** | Transparent | 玻璃、水 |

**优势**：
- ✅ drawing struct 模式使效果可组合、可复用
- ✅ 统一前缀命名规范（`_TX2_/_MT_/_TS_/_TR_/_NM_/_HL_/_ES_`）
- ✅ 4 种透明度模式覆盖所有场景
- ✅ 跨平台抽象（BRP/URP 兼容层）
- ✅ 丰富的专业效果（Fur/Water/Grass/Gem/Particle）
- ✅ Editor 工具完善
- ✅ 持续维护（102 releases）

**劣势**：
- ❌ 基于 Unlit（不是真正的 PBR）
- ❌ FakeFur 需要 SM5.0（不支持 Quest/移动端）
- ❌ 文档语言（日语为主）
- ❌ 社区规模较小

**适用场景**：
- 需要 Fur（毛发）/ Water（水面）/ Grass（草地）/ Gem（宝石）特效
- 独特 Toon 效果需求（非标准 PBR）
- 与 lilToon 形成互补的专业效果选择

**详细文档**：`memory/avatar/shader/unlitwf/index.md`

---

## 四、完整功能对比矩阵

### 4.1 Avatar 核心功能

| 功能 | lilToon | SCSS | UnlitWF | 说明 |
|------|---------|------|---------|------|
| **Toon 阴影** | ✅ 阶梯/平滑 | ✅ 双阴影系统 | ✅ 阶梯阴影 | SCSS 最灵活 |
| **Outline** | ✅ 内置 | ✅ VR 优化 | ✅ 多种模式 | 各有优势 |
| **Fur 毛发** | ✅ 噪声采样 | ❌ | ✅ Geometry | lilToon 跨平台 |
| **Water** | ⚠️ 基础 | ❌ | ✅ 波浪+焦散 | UnlitWF 最完整 |
| **Gem** | ⚠️ 折射 | ❌ | ✅ Flake 效果 | UnlitWF 独特 |
| **Grass** | ❌ | ❌ | ✅ 风力模拟 | UnlitWF 独有 |
| **PBR 支持** | ✅ 完整 | ❌ | ⚠️ 有限 | lilToon 最完善 |
| **Matcap** | ✅ | ✅ 多槽位 | ✅ 多种模式 | SCSS 最灵活 |
| **Dissolve** | ✅ | ✅ | ✅ | 均支持 |
| **Stencil** | ✅ | ⚠️ | ✅ | lilToon 最完善 |

### 4.2 World/平台支持

| 维度 | lilToon | SCSS | ORL | Filamented | UnlitWF |
|------|---------|------|-----|------------|---------|
| **BRP** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **URP** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **HDRP** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Quest 支持** | ✅ 详细指南 | ✅ | ⚠️ 无分级 | ⚠️ | ✅ Mobile 变体 |
| **AudioLink** | ⚠️ 手动 | ✅ 每频段 | ✅ 5种模式 | ❌ | ❌ |
| **VRCLightVolumes** | ❌ | ❌ | ✅ | ✅ | ✅ v2.0.1+ |

### 4.3 社区与资源

| 维度 | lilToon | SCSS | ORL | Filamented | UnlitWF |
|------|---------|------|-----|------------|---------|
| **市场占有率** | 30%+ | 较低 | 较高 | 较小众 | 较小众 |
| **社区活跃度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **文档质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **预设/教程** | 丰富 | 较少 | 良好 | 有限 | 有限 |
| **许可证** | MIT | MIT | MIT | Apache 2.0 | zlib |

---

## 五、选择指南

### 5.1 按场景推荐

| 场景 | 推荐 Shader | 原因 |
|------|------------|------|
| **VRChat Avatar 通用** | lilToon | 功能全面、文档完善、社区大 |
| **Cel Shader 优先** | SCSS | 双阴影系统、UV 服装切换 |
| **独特效果需求** | UnlitWF | Fur/Water/Grass/Gem 专业系统 |
| **日系动漫风格** | SCSS / lilToon | 专用 Cel Shader |
| **水/宝石特效** | UnlitWF | 专用效果系统 |
| **World 环境构建** | ORL Shaders | 模块化、丰富的 PBR 功能 |
| **World VFX 特效** | ORL Shaders | Shield/Laser/Clouds 专属 |
| **Standard 升级** | Filamented | 零成本迁移、现代 PBR |
| **需要 LTCGI/AreaLit** | ORL / z3y/shaders | 内置支持 |

### 5.2 按用户类型推荐

| 用户类型 | 推荐 Shader | 说明 |
|----------|------------|------|
| **新手用户** | lilToon | 一键预设，简单上手 |
| **进阶用户** | SCSS + lilToon | 精细控制 + 功能全面 |
| **专业 Avatar 创作者** | SCSS / UnlitWF | 独特效果 + 高端控制 |
| **World 开发者** | ORL Shaders | 模块化 + VFX 丰富 |
| **PBR 升级需求** | Filamented | 最小侵入性 |

### 5.3 互补使用建议

| 项目部分 | 推荐 Shader | 组合方式 |
|----------|-------------|----------|
| **Avatar 身体** | lilToon | 双阴影 + SSS + 优化 |
| **Avatar 服装** | SCSS 或 lilToon | UV 切换或模块化 |
| **Avatar 特效** | UnlitWF | Fur/Water/Gem 专业系统 |
| **World 环境** | ORL Standard | PBR + Parallax + Details |
| **World VFX** | ORL VFX | Shield + Laser + Clouds |
| **共享特效** | ORL Dissolve | 溶解效果通用 |

---

## 六、知识库状态

| Shader | 文档状态 | 分析完成度 |
|--------|----------|-----------|
| **lilToon** | ✅ 完整（16个文件） | 100% |
| **SCSS** | ✅ 完整（1个文件 + 详细分析） | 100% |
| **ORL Shaders** | ✅ 完整（4个文件） | 100% |
| **Filamented** | ✅ 完整（4个文件） | 100% |
| **UnlitWF** | ✅ 完整（1个文件 + 详细分析） | 100% |
| **z3y/shaders** | ⚠️ 待补充 | 引用但未详细分析 |
| **GeneLit** | ⚠️ 待补充 | 引用但未详细分析 |
| **Graphlit** | ⚠️ 待补充 | 引用但未详细分析 |

---

## 七、相关文档

- `memory/avatar/performance-rank.md` — Avatar 性能排名
- `memory/avatar/optimization-guide.md` — Avatar 优化指南
- `memory/avatar/ndmf-tools.md` — NDMF 工具链
- `memory/world/shader/` — World Shader 知识库
- `memory/world/bakery/` — Bakery 光照烘焙

---

## 更新记录

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-06-11 | 整合 | 完成所有 Shader 分析结果整合 |
| 2026-06-11 | 新增 | UnlitWF Shader Suite 完整分析 |
| 2026-06-11 | 新增 | ORL Shaders 完整分析（4个文件） |
| 2026-06-11 | 新增 | Filamented 完整分析（4个文件） |
| 2026-06-11 | 新增 | SCSS 详细分析报告 |
| 2026-06-11 | 更新 | lilToon 知识库（16个文件） |