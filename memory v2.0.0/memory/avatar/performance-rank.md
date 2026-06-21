---
title: Avatar Performance Ranking System
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - physbone
  - performance
  - light

aliases:
  - "Performance Rank"
  - "Avatar 性能分级"
  - 性能等级
  - 性能排名

related:
  - "avatar/optimization-guide.md"
  - "avatar/ndmf-tools.md"
  - "avatar/playable-layers.md"
  - "world/performance-guide.md"
  - "api/dynamics.md"
  - "api/networking.md"
  - "avatar/vrc-constraints.md"
  - "avatar/modular-avatar.md"
  - "rules/performance-rules.md"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-05
confidence: High
---

---
# Avatar Performance Ranking System


---

## PC 平台 Performance Rank 标准

| 指标 | Excellent | Good | Medium | Poor |
|------|-----------|------|--------|------|
| **面数 (Polygons)** | 32,000 | 70,000 | 70,000 | 70,000 |
| **材质内存 (Texture Memory)** | 40MB | 75MB | 110MB | 150MB |
| **Skinned Mesh Renderer** | 1 | 2 | 8 | 16 |
| **材质球 (Material Slots)** | 4 | 8 | 16 | 32 |
| **PhysBone 元件数** | 4 | 8 | 16 | 32 |
| **PB 影响骨头数** | 16 | 64 | 128 | 256 |
| **PB 碰撞器数** | 4 | 8 | 16 | 32 |
| **碰撞检测数** | 32 | 128 | 256 | 512 |
| **骨头数 (Bones)** | 75 | 150 | 256 | 400 |
| **光源 (Lights)** | 0 | 0 | 0 | 1 |
| **粒子系统数** | 0 | 4 | 8 | 16 |
| **粒子总数量** | 0 | 300 | 1,000 | 2,500 |
| **粒子系统面数** | 0 | 1,000 | 2,000 | 5,000 |
| **粒子系统轨迹** | 禁用 | 禁用 | 启用 | 启用 |
| **粒子系统碰撞** | 禁用 | 禁用 | 启用 | 启用 |

> ⚠️ **Very Poor**: 超过 Poor 标准即为 Very Poor

---

## Quest (Mobile) 平台标准

> Quest 标准极为严格，Very Poor 会强制不显示

| 指标 | Excellent | Good | Medium | Poor |
|------|-----------|------|--------|------|
| **面数** | 32,000 | 70,000 | 70,000 | 70,000 |
| **材质内存** | 40MB | 75MB | 110MB | 150MB |
| **Skinned Mesh** | 1 | 2 | 4 | 8 |
| **材质球** | 2 | 4 | 8 | 16 |
| **PhysBone 元件** | 2 | 4 | 8 | 16 |
| **PB 影响骨头数** | 8 | 32 | 64 | 128 |
| **PB 碰撞器** | 2 | 4 | 8 | 16 |
| **碰撞检测数** | 16 | 64 | 128 | 256 |
| **骨头数** | 38 | 75 | 128 | 200 |
| **光源** | 0 | 0 | 0 | 0 |
| **粒子系统** | 0 | 2 | 4 | 8 |
| **粒子总数量** | 0 | 150 | 500 | 1,000 |

> 📖 参考: [VRChat 官方 Avatar Performance Ranking 文档](https://creators.vrchat.com/avatars/avatar-performance-ranking-system/)

---

## 常见导致 Very Poor 的原因

1. **Skinned Mesh Renderer 过多** — 最常见的 CPU 杀手
2. **材质球过多** — 可以填满一座泳池
3. **PhysBone 元件过多** — 走在路上都能踢到
4. **面数过多** — 让 3D 龙看了直摇头
5. **贴图过大** — 非常「肥美」的贴图

---

## 最佳化优先级（从易到难）

```
1. Light (光源)          → 能不要就不要
2. Particle System      → 控制数量
3. Texture Memory       → 降分辨率/压缩
4. Skinned Mesh         → 合并
5. Material Slots       → Atlas 化
6. PhysBones            → 合并 + 精简
7. Bones                → 合并
8. Polygons             → Remove + Simplify
```

---

## 相关文档

- `ndmf-tools.md` — NDMF 工具生态与获取方式
- `optimization-guide.md` — 完整最佳化实操指南
