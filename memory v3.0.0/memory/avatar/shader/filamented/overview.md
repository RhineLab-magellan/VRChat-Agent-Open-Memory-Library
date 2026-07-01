---
title: "Filamented Overview - 项目概览"
category: avatar
subcategory: shader
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: "v1.4.0 (2024-03)"
last_review: 2026-06-21
confidence: Medium
tags:
  - avatar
  - shader
  - filamented
  - json
aliases:
  - "Filamented Overview - 项目概览"
  - overview
related:
  - comparison.md
  - pbr-improvements.md
  - "../liltoon/installation.md"
  - "../orl/overview.md"
  - "../../avatar-optimizer.md"
---
# Filamented Overview - 项目概览

## 项目信息

| 属性 | 值 |
|------|-----|
| **名称** | Filamented (Filamented Standard) |
| **GitLab** | https://gitlab.com/s-ilent/filamented |
| **GitHub Fork** | https://github.com/Ivaj1/filamente |
| **基于引擎** | Google Filament v1.9.23 |
| **Unity 版本** | 2022.3+ |
| **主要语言** | HLSL (51.7%), ShaderLab (33.1%), C# (15.2%) |

## 核心定位

Filamented 的核心目标是将 Google Filament 渲染引擎的 PBR 计算逻辑移植到 Unity Standard Shader 框架中，用更现代、更精确的光照模型替换 Standard 着色器中过时且不精确的算法。

## 安装方式

### 方式一：Unity Package Manager
```bash
# 下载仓库，将包含 package.json 的文件夹放入 Packages/ 目录
```

### 方式二：本地 Package
```
下载仓库 → 将文件夹放入 Unity 项目的 Packages/ 目录
```

## 核心使用

### 材质转换
1. **手动转换**：在 Material Inspector 中将 Shader 从 Standard 切换为 Filamented
2. **自动转换**：Tools 菜单 → Filamented → 批量转换当前场景所有材质

### 支持的工作流
- Metallic Workflow（默认）
- Specular Workflow
- Roughness Workflow

## 工具菜单

| 工具 | 功能 |
|------|------|
| Filamented Material Swap | 自动转换 Standard → Filamented |

## Extras 扩展包

Filamented 提供了额外的变体 Shader：
- **Filamented Template**：精简版，所有属性打包到单张纹理
- **Filamented Painting Canvas**：高质量艺术品展示 Shader

## 项目结构

```
s-ilent.filamented/
├── Filamented/           # 主 Shader
├── Editor/               # 编辑器工具
├── Extras/               # 扩展变体
└── package.json
```

## 与 Standard 的兼容性

**100% 属性兼容** - 这是 Filamented 最大的设计目标：
- 所有 Standard 属性在 Filamented 中一一对应
- 从 Standard 切换后所有贴图和参数自动保留
- 无需重新制作材质

## 适用场景

| 场景 | 推荐度 | 说明 |
|------|--------|------|
| World 静态物体 PBR | ⭐⭐⭐⭐⭐ | 最佳选择 |
| Standard 升级 | ⭐⭐⭐⭐⭐ | 零成本迁移 |
| 角色 Avatar | ⭐⭐⭐ | 可用但非首选 |
| 需要 Anisotropy | ⭐ | 不支持 |
| 需要 Subsurface | ⭐ | 不支持 |
| 需要动漫风格 | ⭐ | 选 lilToon/Poiyomi |

## 局限性

| 限制 | 说明 |
|------|------|
| 无 Anisotropy | 不支持切线方向高光拉伸 |
| 无 Subsurface | 不支持次表面散射 |
| 无 Clearcoat | 不支持清漆层 |
| 无 LTCGI | 不支持 Area Lights |
| 社区较小 | 相比 lilToon 用户基数小 |