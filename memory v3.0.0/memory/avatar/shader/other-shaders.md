---
title: "其他 Shader 知识库"
category: avatar
subcategory: shader
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.1
last_review: 2026-07-01
confidence: Medium
tags:
  - avatar
  - shader
  - liltoon
  - bakery
  - light
aliases:
  - 着色器
  - "其他 Shader 知识库"
related:
  - "avatar/performance-rank.md"
  - index.md
  - scss.md
  - "filamented/comparison.md"
  - "liltoon/reflection-settings.md"
---
# 其他 Shader 知识库

> 记录 Avatar 制作中除 lilToon 以外的其他着色器
>
> **2026-07-01 更新**: Poiyomi Shaders 65 个文档已完整入库,详情见 `../../参考文献/Poiyomi/INDEX.md`

---

## 目录

```
avatar/shader/
├── index.md                  ← 主索引(含 Poiyomi ⭐2026-07-01)
├── liltoon/                  ← lilToon（30%+ VRChat 模型使用）
├── ../../参考文献/Poiyomi/   ← Poiyomi 65 个文档(完整)
│   └── INDEX.md
└── other-shaders.md          ← 本文件
```

---

## World/Object Shader（不适用于 Avatar）

### Poiyomi Shaders ⭐ VRChat Avatar 主流 ⭐ 已完整入库

> **2026-07-01 完成**: 65 个文档从 `https://www.poiyomi.com/intro` 系统化下载,详见 `../../参考文献/Poiyomi/INDEX.md`

| 属性 | 说明 |
|------|------|
| **定位** | VRChat Avatar 主流 Toon Shader(与 lilToon 并列第一梯队) |
| **许可证** | Patreon 订阅(免费 Toon 版,Pro 完整版 $10/月+) |
| **官网** | https://www.poiyomi.com/ |
| **文档版本** | 10.0 |
| **本地路径** | `参考文献/Poiyomi/INDEX.md` |

**核心特性摘要**:
- 5 个 Shader 变体(Nano/Micro/Mega/Giga/Tera,覆盖 PC → Quest)
- 完整 AudioLink 集成(5 频段 + AL Spectrum)
- 模块化 Shader 系统(Pro)
- Thry Editor UI 框架
- 16 通道 Global Masking + 4 个 Global Themes
- 9 种 Lighting Type(Texture Ramp / Multilayer Math / Wrapped / Skin / ShadeMap / Flat / Realistic / Cloth / SDF)
- LTCGI / VRC Light Volumes 集成
- 专业效果: Fur(31 层) / ShatterWave / Geometric Dissolve / Voronoi / Constellation / Internal Parallax

**优势**:
- VRChat Avatar 主流(与 lilToon 并列)
- 变体分级清晰(Quest 优化独立)
- 风格化效果远超 lilToon
- Thry Editor 是 VRChat 社区事实标准 UI 框架
- 模块化系统可大幅减少重复工作

**劣势**:
- 高级功能需 Pro 订阅
- 配置项极多,学习曲线高
- 仅支持 BRP

**详细文档**: `../../参考文献/Poiyomi/INDEX.md`(65 个 .md 文件)

---

### Graphlit ⭐ 推荐

| 属性 | 说明 |
|------|------|
| **项目地址** | https://github.com/z3y/Graphlit |
| **类型** | 节点式 Shader 编辑器 |
| **适用场景** | World 物体、高质量 PBR、光照烘焙 |
| **许可证** | MIT |
| **开发者** | z3y |

**核心特性：**
- 基于 Google Filament 的顶级 PBR 实现
- 完整支持 Bakery / LTCGI / AreaLit / VRCLightVolumes
- 节点编辑器，完全可定制
- 不适合 Avatar（无 fur/dissolve 等功能）

**详细文档**：`memory/world/shader/graphlit.md`

---

## 不推荐的着色器

| 着色器 | 状态 | 说明 |
|--------|------|------|
| URP/HDRP 着色器 | ❌ 禁止 | VRChat 只支持 BRP |

> 📌 VRCFury 是 Avatar 自动化**工具**（不是 Shader），不在本知识库范围内。详见 `memory/avatar/vrcfury-reference.md`

---

## 相关文档

- `memory/world/shader/` — World Shader 知识库
- `memory/avatar/performance-rank.md` — Avatar 性能排名
- `memory/world/bakery/` — Bakery 光照烘焙