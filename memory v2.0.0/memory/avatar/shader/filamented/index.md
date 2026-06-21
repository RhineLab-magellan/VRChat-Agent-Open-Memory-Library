---
title: Filamented Shader 知识库
category: avatar
subcategory: shader

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "着色器"

related:
  - overview.md
  - pbr-improvements.md
  - comparison.md

source: 本地知识库整理
source_type: community
version: 1.0
upstream_version: v1.4.0 (2024-03)
last_review: 2026-06-21
confidence: Medium
---
# Filamented Shader 知识库

基于 Google Filament 渲染引擎的 Unity Standard Shader 替代方案。

## 索引

| 文档 | 说明 |
|------|------|
| [overview.md](overview.md) | 项目概览、安装、基本使用 |
| [pbr-improvements.md](pbr-improvements.md) | 核心 PBR 改进详解 |
| [comparison.md](comparison.md) | 与同类项目对比分析 |

## 快速参考

| 属性 | 值 |
|------|-----|
| **基于引擎** | Google Filament v1.9.23 |
| **主要仓库** | https://gitlab.com/s-ilent/filamented |
| **Unity 版本** | 2022.3+ |
| **定位** | Standard Shader 替代，专注 PBR 质量提升 |

## 核心特点

- ✅ 与 Standard 属性完全兼容（一键转换）
- ✅ 改进的 Fresnel 计算（非金属不再过度反射）
- ✅ Exposure Occlusion（Specular 遮挡）
- ✅ VRC Light Volumes 完整支持
- ❌ 不支持 Anisotropy/Subsurface/Clearcoat

## 适用场景

- World 静态物体需要精确 PBR
- 从 Standard 升级，期望最小侵入性
- 需要 VRC Light Volumes 但不需要重型 Shader

## 相关项目

| 项目 | Filament 基础 | 高级特性 | 复杂度 |
|------|---------------|----------|--------|
| **Filamented** | ✅ 核心 | ⭐ 基础 | 低 |
| z3y/shaders | ✅ 完整 | ⭐⭐⭐⭐ 丰富 | 中 |
| GeneLit | ✅ 完整 | ⭐⭐⭐ 高级 | 高 |
| peppermint | ✅ 基础 | ⭐ 精简 | 低 |