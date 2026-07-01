---
title: "World Shader 知识库索引"
category: world
subcategory: shader
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - misc
  - index
  - navigation
aliases:
  - 着色器
  - "World Shader 知识库索引"
related:
  - "world/performance-guide.md"
  - "world/shader/graphlit.md"
  - "../bakery/index.md"
  - "../clientsim/index.md"
  - "../scene-components/index.md"
---
# World Shader 知识库索引

记录 World 制作中使用的着色器及其配置知识。

---

## 目录结构

```
world/shader/
├── index.md           ← 本索引文件
└── graphlit.md        ← Graphlit 节点编辑器
```

---

## 核心着色器

### Graphlit（World/Object 首选）

| 属性 | 说明 |
|------|------|
| **市场占有率** | World 开发领域热门 |
| **开发者** | z3y |
| **许可证** | MIT License |
| **文档** | https://z3y.github.io/Graphlit/ |
| **VPM 包** | `https://z3y.github.io/vpm-package-listing/` |

**核心特性：**
- 节点式 Shader 编辑器，完全可定制
- 基于 Google Filament 的顶级 PBR 实现
- 完整支持 Bakery / LTCGI / AreaLit / VRCLightVolumes v2.0
- 适合高质量 World 物体着色

**定位**：World/Object 场景首选，Avatar 场景使用 lilToon

---

## 使用建议

1. **World 物体首选 Graphlit** — PBR 质量最高，光照系统集成最全面
2. **Avatar 使用 lilToon** — 完整 Avatar 功能套件
3. **禁止使用 URP/HDRP** — VRChat 只支持 Built-in Rendering Pipeline
4. **结合 Bakery 使用** — Graphlit 的 Bakery 特性需配合 Bakery 烘焙

---

## 相关文档

- `memory/world/bakery/` — Bakery GPU Lightmapper
- `memory/avatar/shader/` — Avatar Shader 知识库
- `memory/world/performance-guide.md` — World 性能优化指南