---
title: "Poiyomi Shaders - 安装与版本"
category: avatar
subcategory: shader
poiyomi_subdir: true
knowledge_level: applied
status: active
source: "本地知识库整理(2026-07-01) + Poiyomi 官方文档 v10.0"
source_type: official
version: 1.0
upstream_version: "10.0 (分阶段推出)"
last_review: 2026-07-01
confidence: High
tags:
  - avatar
  - shader
  - poiyomi
  - installation
  - vpm
  - patreon
aliases:
  - "Poiyomi 安装"
  - "Poiyomi Download & Install"
  - "Poiyomi VPM"
related:
  - "./pro-vs-toon.md"
  - "./shader-variants.md"
  - "../../../sources/vpm-mirrors/samples/poiyomi.md"
  - "../../../../参考文献/Poiyomi/01-download-install.md"
  - "../../../../参考文献/Poiyomi/00-introduction.md"
---

# Poiyomi Shaders — 安装与版本

> **Domain**: Avatar → Shader → Poiyomi → 安装与版本
> **原始参考**: `参考文献/Poiyomi/00-introduction.md` + `01-download-install.md`
> **状态**: 活跃(Active)

---

## 1. 概述

Poiyomi Shaders 是 VRChat 改模界主流的 Toon Shader,与 lilToon 并列第一梯队。提供 5 个分级变体(Nano→Tera)覆盖 PC→Quest 全部场景。本文档聚焦**安装、版本选择、Pro 鉴权**三件事。

---

## 2. 关键决策树

```
你想用 Poiyomi 做什么?
│
├─ 基础 Toon/PBR 切换 + 兼容老 Avatar
│   └─ 安装 Poiyomi Toon(免费, com.poiyomi.toon)
│
├─ 需要 Modular Shader / Fur 31 层 / ShatterWave
│   └─ 订阅 Patreon $10+/月 → Poiyomi Pro (com.poiyomi.pro)
│
├─ Quest Avatar 优化
│   └─ 选 .poiyomi/Poiyomi Toon Micro 变体
│
└─ 顶级视觉效果(PC 高端机)
    └─ 选 .poiyomi/Poiyomi Pro Tera 变体
```

---

## 3. 安装方法

### 3.1 推荐:VCC / ALCOM 安装

| 项目 | Toon(免费) | Pro($10+/月) |
|------|-----------|-------------|
| **VPM URL** | `https://poiyomi.github.io/vpm/index.json` | 同左(需 Discord 鉴权) |
| **包 ID** | `com.poiyomi.toon` | `com.poiyomi.pro` |
| **VCC 操作** | Add Repository → 粘贴 URL | 同左,Pro 需额外认证步骤 |

> ⚠️ **国内访问警告**: Poiyomi VPM 在 `vcc.vrczh.org` 镜像站**同步失败**(2026-07-01 状态)。建议:
> 1. 直连 `https://poiyomi.github.io/vpm/index.json`
> 2. 或使用 ALCOM 内置源
> 3. 详见 `sources/vpm-mirrors/samples/poiyomi.md`

### 3.2 手动安装(替代方案)

1. 从 `https://poiyomi.com/download` 下载 `.unitypackage`
2. Unity → Assets → Import Package → Custom Package
3. 拖入下载的包

### 3.3 安装验证

```text
Project/
├── Packages/
│   └── vpm-manifest.json    ← 应包含 com.poiyomi.toon / com.poiyomi.pro
├── Assets/
│   └── Poiyomi Shaders/     ← 资源文件
└── Library/
    └── ShaderCache/         ← 编译缓存
```

Unity 重新加载后,Material Inspector 的 Shader 下拉应出现 `.poiyomi/Poiyomi Toon` 系列选项。

---

## 4. 版本演进

### 4.1 完整时间线

| 版本 | 时期 | 状态 | 关键变化 |
|------|------|------|----------|
| **8.x** | 2020-2023 | 🟡 维护中 | Toon/PBR 切换、视频纹理、渐变遮罩 |
| **9.x** | 2023-2026 | 🟢 主流 | Pro 添加 Lighting/Tessellation;VPM 9.3.66 当前 |
| **10.0** | 2026+ 分阶段 | 🆕 新 | Shader Graph 基础架构、5 变体分级、Modular Shader System(Pro)、9 种 Lighting Type |

### 4.2 关键差异

| 维度 | 8.x / 9.x | 10.0 |
|------|-----------|------|
| **架构** | 传统 Shader Lab | Shader Graph 9.x+ Pro 基础 |
| **变体** | 主要 1 个 Toon + 1 Pro | 5 个变体 (Nano/Micro/Mega/Giga/Tera) |
| **Modular System** | ❌ | ✅ (Pro 专属) |
| **Lighting Type** | 几种 | 9 种 (Texture Ramp / Multilayer Math / Wrapped / Skin / ShadeMap / Flat / Realistic / Cloth / SDF) |
| **AudioLink** | ✅ | ✅ 更完善 |
| **VRC Light Volumes** | ✅ 9.2.67+ | ✅ |

### 4.3 10.0 文档"分阶段推出"风险

> ⚠️ **重要**: Poiyomi 10.0 文档声明"正在分阶段推出"。这意味着:
> - 文档中描述的某些功能**实际可能尚未在 VPM 包中提供**
> - VPM 实际可用版本可能仍为 9.3.x(2026-07-01)
> - 建议**双轨验证**:文档查功能 + 实际安装查 VPM 包

---

## 5. Pro 鉴权流程(Patreon $10+)

### 5.1 鉴权必要性

Poiyomi Pro **不能**通过镜像站或 VPM 公开下载,必须经 Patreon 鉴权后从 Discord 渠道获取:

```
Patreon $10+/月订阅
    ↓
登录 Discord 并绑定 Patreon 账户
    ↓
进入 #pro-downloads 频道
    ↓
下载 com.poiyomi.pro .unitypackage
    ↓
手动 Import 到 Unity
```

### 5.2 关键约束

| 约束 | 说明 |
|------|------|
| **最低 Patreon 等级** | $10/月(不含 $2/$5 等级) |
| **绑定时效** | 取消订阅后,Pro 功能持续可用至订阅期结束 |
| **分发限制** | Pro .unitypackage **不可**二次分发,不可镜像 |
| **商业项目** | Patreon ToS 允许商业 Avatar 使用 Pro |
| **离线使用** | 鉴权通过后可离线使用(无需持续联网) |

### 5.3 鉴权失败排查

| 症状 | 原因 | 解决 |
|------|------|------|
| 看不到 Pro 选项 | 未订阅 / 未绑定 Discord | 检查 Patreon → Settings → Connected accounts |
| 导入后 Pro 失效 | .unitypackage 损坏 / 鉴权过期 | 重新下载 + 检查订阅状态 |
| 国内下载慢 | Discord CDN 限速 | 使用下载工具 + 离线导入 |

---

## 6. 5 个变体快速选择

详见 `shader-variants.md`。速查表:

| 变体 | 平台 | 性能 | 适用 |
|------|------|------|------|
| **Nano** | PC + Quest | ⭐⭐⭐⭐⭐ | 极简 Avatar, 优先级性能 |
| **Micro** | Quest 首选 | ⭐⭐⭐⭐ | Quest Avatar, 移动端 |
| **Mega** | PC 通用 | ⭐⭐⭐ | 通用 PC Avatar |
| **Giga** | PC 高端 | ⭐⭐ | 复杂效果 PC |
| **Tera** | 顶级 PC | ⭐ | 顶级视觉效果 |

---

## 7. Pro vs Toon 关键功能差异

详见 `pro-vs-toon.md`。速查表:

| 功能 | Toon | Pro |
|------|------|-----|
| 5 变体 + 基础效果 | ✅ | ✅ |
| Modular Shader System | ❌ | ✅ |
| Poiyomi Fur(1-31 层) | ❌ | ✅ |
| ShatterWave | ❌ | ✅ |
| Geometric Dissolve | ❌ | ✅ |
| Constellation | ❌ | ✅ |
| Voronoi 3D | ❌ | ✅ |
| Internal Parallax | ❌ | ✅ |
| Lil Fur(基于 LilToon) | ✅ | ✅ |

---

## 8. 系统要求

| 项目 | 最低 | 推荐 |
|------|------|------|
| **Unity(BRP)** | 2021.3 LTS | 2022.3.22f1(VRChat 官方版本) |
| **Unity(URP)** | 6000.0(6.x) | BETA, 不稳定 |
| **HDRP** | ❌ **不支持** | - |
| **平台(VRChat)** | Windows + VRChat SDK | - |
| **平台(其他)** | Windows | - |

> 🔴 **重要**: Poiyomi **不支持 HDRP**。若项目用 HDRP,需迁移到 BRP 或 URP。

---

## 9. 实战陷阱

### 9.1 常见安装错误

| 错误 | 症状 | 修复 |
|------|------|------|
| **项目用 HDRP** | Material 全紫 | 迁移到 BRP(VRChat 唯一支持) |
| **忘装 VRC SDK** | 无法上传 Avatar | 先装 VRChat SDK 3.4.2+ |
| **Unity 版本不对** | Shader 编译失败 | 用 2022.3.22f1(VRChat 推荐) |
| **国内 mirror 失败** | VCC 拉不到 Poiyomi | 用 GitHub Pages 直连 URL |
| **Pro 鉴权后仍 Toon** | 看不到 Pro Shader 选项 | 检查导入路径 + 重启 Unity |

### 9.2 Warudo VTubing 特殊要求

> **警告**: Poiyomi 在 Warudo Mods 中受支持,但需注意:
> - Warudo 要求 Unity **`2021.3.45f2`**(与 VRChat 2022.3 不同)
> - 必须**手动锁定 Materials** 后才能构建 Warudo Mods
> - 可用 Pumkin's Warudo Exporter 自动从 VRChat Avatar 转换

---

## 10. 引用与原始数据

| 引用目标 | 位置 |
|----------|------|
| **Poiyomi Introduction 原文** | `参考文献/Poiyomi/00-introduction.md` |
| **Poiyomi Download & Install 原文** | `参考文献/Poiyomi/01-download-install.md` |
| **VPM 包元数据** | `memory/sources/vpm-mirrors/samples/poiyomi.md` |
| **5 变体详解** | `./shader-variants.md` |
| **Pro vs Toon 详解** | `./pro-vs-toon.md` |
| **Poiyomi 主索引** | `./index.md` |

---

## 元信息

| 字段 | 值 |
|------|-----|
| **文档版本** | 1.0 |
| **创建日期** | 2026-07-01 |
| **上游版本** | Poiyomi 10.0(分阶段推出) |
| **VPM 实际版本** | 8.1.166 Toon / 9.3.66 Pro(2026-07-01) |
| **评审状态** | Stage 2.1 完成 |
| **下一步** | 评审 1 周后(2026-07-08) |
