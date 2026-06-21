---
title: lilToon 知识库索引
category: avatar
subcategory: shader

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "lilToon"

related:
  - overview.md
  - installation.md
  - render-modes.md
  - basic-settings.md
  - color-settings.md
  - reflection-settings.md
  - outline.md
  - fur.md
  - stencil.md
  - audiolink.md
  - dissolve.md
  - vrchat-specific.md
  - optimization.md
  - troubleshooting.md
  - variations.md

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: v2.3.2 (2025-10-29)
last_review: 2026-06-21
confidence: Medium
---
# lilToon 知识库索引

> VRChat 改模界主流的开源 Toon Shader,功能全面、社区资源丰富

---

## 快速导航

| 文档 | 说明 |
|------|------|
| [概述与特性](overview.md) | lilToon 的四大核心特性 |
| [安装与配置](installation.md) | VCC/BOOTH/手动安装 |
| [渲染模式](render-modes.md) | 不透明/透明/折射等模式详解 |
| [基本设置](basic-settings.md) | Cull Mode/ZWrite/Render Queue |
| [颜色设置](color-settings.md) | 色彩/色调校正/透明度 |
| [阴影设置](color-settings.md#阴影) | 动漫阴影/2D CG 阴影/3影系统 |
| [反射设置](reflection-settings.md) | 光泽/镜面反射/环境光 |
| [轮廓线](outline.md) | 线画/法线轮郭/顶点颜色 |
| [毛发系统](fur.md) | 毛发生成/物理模拟 |
| [Stencil 设置](stencil.md) | 3D 空间遮罩/描画顺序 |
| [AudioLink](audiolink.md) | 音频同步动画 |
| [Dissolve](dissolve.md) | 溶解/消失效果 |
| [VRChat 配置](vrchat-specific.md) | Safety Fallback 等 |
| [优化指南](optimization.md) | Bake/转换/容量削减 |
| [故障排除](troubleshooting.md) | 常见问题与解决方案 |
| [着色器变体](variations.md) | 全版本对比 |

---

## 核心参数速查

### 渲染模式优先级（性能）

```
不透明(Opaque) > カットアウト(Cutout) > 半透明(Transparent)
> 屈折(Refraction) > ファー(Fur) > 宝石(Gem)
```

### Mask 纹理通道映射

| 功能 | 使用的纹理通道 |
|------|---------------|
| 色調補正遮罩 | R |
| 影强度遮罩 | R |
| 轮廓线遮罩 | R |
| 法线遮罩 | R |
| 异方性遮罩 | R |
| MatCap 遮罩 | RGB |
| アルファ遮罩 | R |
| 顶点色(R->Width) | R |
| 顶点色(RGBA->Normal&Width) | RGBA |

---

## 版本历史

| 版本 | 主要变化 |
|------|---------|
| 1.x | 初代发布 |
| 2.x | 重大架构重构，asmdef 调整 |
| 当前 | 持续维护，支持 Unity 2022.3+/2023.x |

---

## 资源链接(项目官方下载入口)

> **安装说明**:以下链接是 lilToon 项目的**官方下载入口**,创作者需要使用这些链接安装到 Unity 项目

- **官方文档**: https://lilxyzw.github.io/lilToon/ja_JP/
- **VCC 添加**: `vcc://vpm/addRepo?url=https://lilxyzw.github.io/vpm-repos/vpm.json`
- **BOOTH 下载**: https://lilxyzw.booth.pm/items/3087170
- **GitHub**: https://github.com/lilxyzw/lilToon

---

## 相关知识库

- `memory/avatar/shader/index.md` — Shader 知识库索引
- `memory/avatar/optimization-guide.md` — Avatar 优化
- `memory/avatar/ndmf-tools.md` — NDMF 工具链
