---
title: 其他 Shader 知识库
category: avatar
subcategory: shader

knowledge_level: applied
status: active

tags:
  - avatar
  - shader
  - liltoon
  - bakery
  - light

aliases:
  - "着色器"

related:
  - avatar/performance-rank.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# 其他 Shader 知识库

> 记录 Avatar 制作中除 lilToon 以外的其他着色器

---

## 目录

```
avatar/shader/
├── index.md           ← 主索引
├── liltoon/           ← lilToon（30%+ VRChat 模型使用）
└── other-shaders.md   ← 本文件
```

---

## World/Object Shader（不适用于 Avatar）

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