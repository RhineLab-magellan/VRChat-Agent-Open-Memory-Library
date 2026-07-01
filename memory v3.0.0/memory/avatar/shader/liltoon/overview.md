---
title: "lilToon — Avatar Toon Shader 推荐指南"
category: avatar
subcategory: shader
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: official
version: 1.0
upstream_version: "v2.3.2 (2025-10-29)"
last_review: 2026-06-21
confidence: Medium
tags:
  - avatar
  - shader
  - liltoon
aliases:
  - 着色器
  - lilToon
related:
  - installation.md
  - render-modes.md
  - basic-settings.md
  - optimization.md
  - troubleshooting.md
  - index.md
  - index.md
---
# lilToon — Avatar Toon Shader 推荐指南

> **本文定位**:为 Avatar 创作者介绍 lilToon Shader 的设计模式、优势、使用场景,并提供安装链接
> **本文性质**:项目推荐文档(Group B — 项目推荐型),不匿名化项目名,仅删除营销参数

---

## 项目定位

lilToon 是当前 VRChat 改模界**最主流的开源 Avatar Toon Shader**,为 Avatar(VRChat 等)开发的动漫风格着色器。

| 属性 | 说明 |
|------|------|
| **Shader 类型** | Toon (动漫风格) — 阶梯阴影 + 抗锯齿 |
| **主要场景** | VRChat Avatar 通用 |
| **许可证** | MIT License(开源) |
| **跨管线** | BRP / URP / HDRP 全支持 |

---

## 四大核心设计模式

### ✨ 简单 (Easy) — 预设与工作流

```
- 预设一键设置
- 自定义预设保存
- 色调校正功能
- 颜色导出为纹理
```

**预设系统**:
- 提供多种预设(通常/Only SRP 等)
- 用户可保存自定义预设
- 一键应用到材质

**色调校正**:
- 色相/饱和度/明度调整
- 伽马校正
- 渐变映射 (Gradient Map)
- 结果可导出为纹理

### 🎨 美观 (Beautiful) — 动漫渲染

```
- 深入研究动漫渲染
- 抗锯齿着色
- 白飞防止
- 半透明穿透防止
```

**动漫渲染**:
- 阴影渐变控制
- 3 阴影系统(可独立配色)
- 边界颜色(次表面散射效果)

**图像保护**:
- 白飞防止(亮度上限)
- 水/半透明物体穿透防止
- VRSNS 友好设计

### 🎈 轻量 (Lightweight) — 编辑器自动优化

```
- 编辑器自动优化
- 移除未使用功能
- Build Size 最小化
- Avatar 容量削减
```

**自动优化**:
- 编辑器自动重写着色器
- 按需启用/禁用功能
- 移除未使用的 Pass

### 🔑 稳定 (Stable) — 跨 Unity 兼容

```
- 全 Unity 照明支持
- Standard Shader 相似亮度
- 广泛 Unity 版本支持
- 轻松着色器迁移
```

**兼容性**:
- 兼容 Standard Shader 亮度
- Unity 版本:2022.3 / 2023.1-2023.3
- 所有渲染管线支持

---

## 支持的渲染管线

| 管线 | 支持情况 |
|------|---------|
| **Built-in Render Pipeline (BRP)** | ✅ 完整支持(VRChat 唯一) |
| **Lightweight Render Pipeline (LWRP)** | ✅ 完整支持 |
| **Universal Render Pipeline (URP)** | ✅ 完整支持 |
| **High Definition Render Pipeline (HDRP)** | ✅ 完整支持 |

> **VRChat 特别提示**:VRChat 仅支持 BRP 管线,跨管线适配能力用于创作者在其他场景(Unity Demo、影视预览)复用

---

## 支持的 Shader Model 变体

| 版本 | SM 版本 |
|------|---------|
| **通常版** | SM 4.0 / ES 3.0 |
| **轻量版 (Lite)** | SM 3.0 / ES 2.0 |
| **毛发版** | SM 4.0 / ES 3.1+AEP / ES 3.2 |
| **细分版** | SM 5.0 / ES 3.1+AEP / ES 3.2 |

---

## 优势与适用场景

| 优势 | 适用场景 |
|------|---------|
| ✅ 全渲染管线支持(BRP/URP/HDRP) | VRChat Avatar 通用选择 |
| ✅ 功能最全面(fur/dissolve/stencil 等) | 新手入门首选(预设一键) |
| ✅ 社区资源最丰富(教程/预设最多) | 需要大量社区资源/教程 |
| ✅ 新手友好(详细 Quest 优化指南) | Quest Avatar 优化 |
| ✅ 持续维护,版本稳定 | 生产环境 Avatar |
| ✅ 跨平台 Unity 版本支持 | 跨 Unity 项目复用 |

**与其他开源 Avatar Shader 的对比选择**:
- 需要 **Cel Shader 优先(双阴影系统)** → 考虑 SCSS
- 需要 **专业效果(毛发/水/宝石)** → 考虑 UnlitWF
- 默认选择 → lilToon(覆盖面最广)

---

## 安装与项目链接

| 安装方式 | 链接 |
|---------|------|
| **VCC/VPM** | `vcc://vpm/addRepo?url=https://lilxyzw.github.io/vpm-repos/vpm.json` |
| **BOOTH** | https://lilxyzw.booth.pm/items/3087170 |
| **GitHub** | https://github.com/lilxyzw/lilToon |
| **官方文档** | https://lilxyzw.github.io/lilToon/ja_JP/ |

> **📌 安装提示**:VRChat 创作者推荐使用 VCC 一键安装,可自动跟踪版本更新

---

## 相关文档

- [安装与配置](installation.md) — 详细安装指南
- [渲染模式](render-modes.md) — 各模式详解
- [基本设置](basic-settings.md) — 基础参数
- [优化指南](optimization.md) — 性能优化
- [故障排除](troubleshooting.md) — 常见问题与解决方案

---

## 📚 相关设计模式

本节是"项目推荐文档",介绍 lilToon 的优势与使用场景。如需了解 Avatar Toon Shader 通用设计模式综述(跨多个开源实现对比),请参阅:

- [Shader 知识库索引](../index.md) — 跨 Avatar/World Shader 对比与选型
- [开源 Avatar Toon Shader 模式综述(规划中)](./index.md) — 通用设计模式提炼
