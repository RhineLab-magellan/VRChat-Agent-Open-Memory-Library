# Filamented 与同类项目对比

## 一、对比矩阵总览

| 项目 | Filament 基础 | 功能定位 | 复杂度 | VRChat 集成 | 维护状态 |
|------|---------------|----------|--------|-------------|----------|
| **Filamented** | ✅ 核心 | PBR 质量提升 | 低 | Light Volumes | 活跃 |
| z3y/shaders | ✅ 完整 | 完整 Standard 替代 | 中 | LTCGI/AreaLit/Light Volumes | 活跃 |
| GeneLit | ✅ 完整 | PBR 增强 | 高 | LTCGI/Light Volumes | 活跃 |
| peppermint | ✅ 基础 | VRChat 专用精简 | 低 | Light Volumes | 一般 |
| GeenzShade | ❌ | glTF 兼容 | 中 | Light Volumes | 活跃 |

## 二、功能特性对比

### 2.1 核心 PBR 特性

| 特性 | Filamented | z3y/shaders | GeneLit | peppermint |
|------|------------|-------------|---------|-------------|
| Fresnel 修复 | ✅ | ✅ | ✅ | ✅ |
| Specular Occlusion | ✅ | ✅ | ✅ | ✅ |
| Anisotropy | ❌ | ✅ | ✅ | ❌ |
| Subsurface Scattering | ❌ | ✅ | ✅ | ❌ |
| Clearcoat | ❌ | ✅ | ✅ | ❌ |
| Refraction | ❌ | ✅ | ✅ | ❌ |
| Sheen | ❌ | ✅ | ✅ | ❌ |

### 2.2 VRChat 特性

| 特性 | Filamented | z3y/shaders | GeneLit | peppermint |
|------|------------|-------------|---------|-------------|
| VRC Light Volumes | ✅ | ✅ | ✅ | ✅ |
| LTCGI | ❌ | ✅ | ✅ | ❌ |
| Bakery 完整集成 | ❌ | ✅ | ✅ | ❌ |
| Geometric Specular AA | ❌ | ✅ | ❌ | ❌ |
| Alpha to Coverage | ❌ | ✅ | ✅ | ❌ |
| Box Projection Quest | ❌ | ✅ | ❌ | ❌ |
| Non-Important Lights | ❌ | ✅ | ✅ | ❌ |

### 2.3 工具与工作流

| 特性 | Filamented | z3y/shaders | GeneLit | peppermint |
|------|------------|-------------|---------|-------------|
| Shader Config 系统 | ❌ | ✅ | ❌ | ❌ |
| 纹理打包工具 | ❌ | ✅ | ❌ | ❌ |
| 一键材质转换 | ✅ | ✅ | ❌ | ❌ |
| ORM 工作流 | ❌ | ✅ | ✅ | ✅ |

## 三、定位分析

### Filamented 的独特价值

```
优势定位：
"用最小侵入性方式，将 Standard Shader 升级到现代 PBR 标准"

目标用户：
- 已经熟悉 Standard 的创作者
- 不想学习复杂 Shader 配置的用户
- 需要快速提升渲染质量的项目
```

### 与 z3y/shaders 的差异

| 维度 | Filamented | z3y/shaders |
|------|------------|-------------|
| 目标 | 替换 Standard 核心 | 完整重建 Standard |
| 学习成本 | 极低 | 中等 |
| 功能密度 | 低 | 高 |
| 适用场景 | 基础 PBR | 专业光照 |

### 与 GeneLit 的差异

| 维度 | Filamented | GeneLit |
|------|------------|---------|
| 目标 | 精确替换 Standard | 高级 PBR 增强 |
| Shader 变体 | 少 | 多 |
| 高级特性 | 缺失 | 丰富 |
| 适用场景 | 简单项目 | 复杂项目 |

## 四、选择指南

### 选 Filamented 当：

- ✅ 现有 Standard 项目需要升级
- ✅ 需要 VRC Light Volumes
- ✅ 不需要 Anisotropy/Subsurface/Clearcoat
- ✅ 想要最小迁移成本
- ✅ 喜欢 Standard 的简洁工作流

### 选 z3y/shaders 当：

- ✅ 需要 LTCGI Area Lights
- ✅ 需要 Anisotropy（拉丝金属）
- ✅ 需要 Subsurface（皮肤透光）
- ✅ 需要完整 Bakery 集成
- ✅ 想要 Shader Config 自定义

### 选 GeneLit 当：

- ✅ 需要高级 PBR 特性
- ✅ 需要 Clearcoat/Sheen
- ✅ 需要 Height Map Shadow
- ✅ 需要 Triplanar Sampling

### 选 lilToon/Poiyomi 当：

- ❌ 需要动漫风格渲染
- ❌ 需要丰富的材质预设
- ❌ 需要 Toon Shading

## 五、知识点总结

### Filament 系列 Shader 的共同特征

| 特征 | 说明 |
|------|------|
| Fresnel 修复 | 核心改进，统一解决 Standard 问题 |
| Specular Occlusion | 基于 Lightmap 的 Specular 遮挡 |
| VRC Light Volumes | 标准支持 |
| 简洁工作流 | 保持与 Standard 的兼容性 |

### 知识库索引

```
memory/
├── avatar/shader/           # Avatar Shader 知识
│   ├── liltoon/            # lilToon（动漫风格）
│   ├── scss/              # SCSS（双阴影系统）
│   └── filamented/        # Filamented（PBR 质量）
└── world/                 # World 相关知识
```

### 相关参考

| 来源 | 说明 |
|------|------|
| Google Filament Docs | https://google.github.io/filament/ |
| s-ilent/SCSS Wiki | Standard Shader 对比 |
| VRCLightVolumes | 光照体积系统 |