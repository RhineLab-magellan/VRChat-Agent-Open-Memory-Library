---
title: "示例包: vrcfury (VRCFury)"
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - example
  - avatar
  - vrcfury
  - toolchain

aliases:
  - "VRCFury"
  - "com.vrcfury.vcc"
  - "VRCFury Developers"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/nadena.md
  - avatar/vrcfury-reference.md
  - avatar/optimization-guide.md
  - avatar/playable-layers.md

source: vcc.vrczh.org + upstream vcc.vrcfury.com
source_type: official
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# vrcfury — VRCFury (Avatar 工具链)

> **📦 VPM 仓库速查**:
> - **apiId**: `vrcfury`
> - **上游 URL**: <https://vcc.vrcfury.com> (VCC 嵌入式源)
> - **镜像 URL**: <https://vpm.vrczh.org/vpm/vrcfury>
> - **状态**: ✅ 同步成功
> - **完整 57 repo URL 索引**: [vpm-repos-url-index.md](../vpm-repos-url-index.md)

---

> **数据来源**:
> - Mirror VPM index: <https://vpm.vrczh.org/vpm/vrcfury> (951246 bytes, 2026-07-01)
> - Upstream VPM index: <https://vcc.vrcfury.com> (575636 bytes, 2026-07-01)
> - 顶层 description: 镜像站未提供；upstream 同样为空 (VRCFury Developers 不写顶层描述)
> - 包内 description: **空** (VRCFury 不填 description 字段)

---

## 基础信息

| 字段 | 值 |
|------|-----|
| **apiId** | `vrcfury` |
| **作者** | VRCFury Developers |
| **类型** | Avatar 工具链 (整合 VCC + Unity 工具) |
| **镜像 URL** | <https://vpm.vrczh.org/vpm/vrcfury> |
| **上游 URL** | <https://vcc.vrcfury.com> (VCC 嵌入式源) |
| **包数量** | 1 个 (但单包内**1281 个历史版本**, 是 VPM 史上版本数最多包之一) |
| **同步状态** | ✅ 同步成功 |

---

## 包含的 1 个包

| # | Package ID | Display Name | 最新 stable | Unity | 描述 |
|---|------------|--------------|------------|-------|------|
| 1 | `com.vrcfury.vrcfury` | **VRCFury** | v1.137.0 | ? | (description 为空) |

> **单包结构**: VRCFury 历史上每个版本都包含完整的编辑器扩展、Prefab Blueprint 系统、约束应用、动画生成器等。**版本数 1281** (mirror 完整保留) — 体现了工具链的快速迭代。

---

## Unity 支持版本

| Unity 版本 | 覆盖包数 | 说明 |
|------------|---------|------|
| **2019.4** | ? | VRCFury 早期版本主要针对 2019.4 |
| **2022.3** | ? | **当前主版本**, 几乎所有功能支持 |
| **6000.0** | 0/1 | 不支持 Unity 6 (VRCFury 1.x 系列) |

> ⚠️ mirror 解析 VRCFury 单包时 `unity` 字段为 `?` (缺失), 但**实际 VRCFury 1.x 系列明确支持 2022.3** (知识库已确认)

---

## 主要功能详细说明

> 来源: 知识库 `memory/avatar/vrcfury-reference.md` (基于 2026-06-17 深度更新)

### 核心架构
- **Prefab Blueprint 系统**: 复制一个 GameObject 作为模板, 自动应用到所有引用者
- **Constraint 应用**: 比 Unity Constraints 更灵活的 Avatar 装配约束
- **动画生成器**: 编程式生成 Animator Controller (类似 HAIC Animator As Code)
- **菜单生成器**: 编程式生成 Expression Menu
- **安全合并**: 自动合并多个 VRC Fury 处理的 Avatar 而不冲突

### VRCFury 工具菜单
- `VRCFury → Create →` 提供以下创建器:
  - **Toggle**: 创建可切换的 Mesh/Material
  - **Blendshape**: 创建 Blendshape 控制
  - **Material**: 创建材质切换
  - **Pose**: 创建姿态菜单
  - **Constraint**: 创建约束
  - **Cross-Prefab**: 跨 Prefab 共享
  - **Full Controller**: 完整 Animator Controller

### 60+ 自动修复 (2026 更新)
- 自动修复常见的 Avatar SDK 上传错误
- 包括 PhysBone 链断裂、Material 槽溢出、Animator 引用丢失等

### Direct Tree Optimizer (2026 新增)
- 与 AAO 直接树优化器集成
- 自动合并相邻 Transform 链

### Blendshape Optimizer (2026 新增)
- 优化 Blendshape 网格, 减少多边形数
- 与 Quest 性能优化强相关

### Parameter Compressor (2026 新增)
- 16 位压缩 Animator 参数
- 减少 Avatar 内存占用, 适合复杂菜单

### 与 Modular Avatar 关系
- **不冲突**, 但**有功能重叠** (Avatar 装配/组件化)
- **简单 Avatar**: MA 够用
- **复杂 Avatar (大量 Toggle, 复杂约束)**: VRCFury 优势更大
- **决策树**: 见 `memory/avatar/vrcfury-reference.md` §3

---

## 已知差异 (Mirror vs Upstream)

| 维度 | Mirror | Upstream | 说明 |
|------|--------|----------|------|
| 包数量 | 1 | 1 | ✅ 一致 |
| 顶层 description | 空 | 空 | 不写 |
| 包内 description | 空 | 空 | VRCFury **不填 description**, 这是 VRCFury 团队的设计选择 |
| 版本数 | 1281 | 1281 | ✅ 一致 (mirror 完整保留所有历史版本) |
| URL 改写 | ✅ | 原 URL | |
| 字节数 | 951246 | 575636 | ⚠️ **Mirror 比 Upstream 大 65%** — 原因待查 (可能 mirror 注入更多 VPM 字段如 samples/headers) |

---

## ⚠️ 描述缺失问题

VRCFury 是少数**完全不写 description 的社区包**, 这导致:
- 知识库无法从 VPM 提取功能描述
- 必须依赖**知识库 `memory/avatar/vrcfury-reference.md`** 或**官方文档** 了解功能
- 对自动化工具有挑战 (e.g. AI Agent 无法从 VPM index 推断 VRCFury 能做什么)

**建议**: 给 VRCFury 写补丁, 在 `packages.{id}.versions.{ver}.description` 填入官方文档摘要
- 官方文档: <https://vrcfury.com/docs>
- 完整功能列表: <https://vrcfury.com/docs/getting-started/what-is-vrcfury>

---

## 必装建议

**任何 Avatar 创作者 (强推荐)**:
- `com.vrcfury.vrcfury` (必备工具)

**MA 用户**:
- VRCFury 和 MA 可共存, VRCFury 处理 "复杂部件", MA 处理 "整体组装"
- 注意不要在同一个 GameObject 上同时使用两者的等价组件

**Quest 性能敏感**:
- VRCFury 的 Blendshape Optimizer + Direct Tree Optimizer 是 Quest 性能优化的关键工具

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| Mirror 字节 | 951246 |
| Upstream 字节 | 575636 |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
