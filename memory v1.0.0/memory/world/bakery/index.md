# Bakery GPU Lightmapper 知识库

> 版本: 1.0 | 来源: geom.io/bakery/wiki/

---

## 目录

1. [概述](#1-概述)
2. [系统要求](#2-系统要求)
3. [安装](#3-安装)
4. [快速开始](#4-快速开始)
5. [渲染设置](#5-渲染设置)
6. [组件](#6-组件)
7. [材质兼容性](#7-材质兼容性)
8. [常见问题 FAQ](#8-常见问题-faq)
9. [故障排除](#9-故障排除)

---

## 1. 概述

Bakery 是一个 GPU 加速的光照贴图烘焙工具，专门为 Unity 设计。

### VRChat 中的地位

| 方案 | 说明 |
|------|------|
| **Bakery** | ✅ 最优选择，VRChat 首选 |
| Unity 内置 | ❌ 性能差，质量低 |
| 其他 | ❌ 不推荐 |

**关键点**: 在光照贴图方面，VRChat 可选方案只有 Bakery 和内置渲染器，**Bakery 总是最优选择**。

### 主要特性

- GPU 加速（基于 NVIDIA OptiX）
- 支持多 GPU
- 多种渲染模式（Full Lighting / Indirect / Shadowmask / Subtractive）
- 支持方向光照贴图（Baked Normal Maps / Dominant Direction / RNM / SH）
- 支持 Light Probes 和 Reflection Probes
- 降噪器支持
- 支持 RTX 模式

---

## 2. 系统要求

### 硬件要求

| 要求 | 规格 |
|------|------|
| 操作系统 | Windows 7+ (64位) |
| GPU | NVIDIA Kepler+ (GeForce 650 或更新) |
| Unity | 64位编辑器 (5.6 到 2022+) |

### 重要提示

- **使用 Game-Ready 驱动，不要用 Studio 驱动**
- 确保安装最新 GPU 驱动

---

## 3. 安装

### 安装步骤

1. 通过 Asset Store 导入 Bakery：`Asset Store → Bakery GPU Lightmapper`
2. 首次导入时点击 **Import**（或取消勾选 _examples_ 文件夹）
3. 文件导入到 `Assets/Bakery` 和 `Assets/Editor/x64/Bakery`
4. 如有编译错误，点击 "Go Ahead"
5. Bakery 菜单将添加到编辑器

### 前置条件

- 确保项目无脚本编译错误
- 更新到最新 GPU 驱动

---

## 4. 快速开始

### 基本流程

```
1. 添加模型，标记为 Static
2. 选择 Directional Light，添加 Bakery Direct Light 组件
3. 点击 "Match lightmapped to real-time" 匹配 Unity 默认灯光
4. 创建 Skylight (Bakery → Create → Skylight)
5. 点击 Bakery → Render Lightmap
6. 点击 Render
```

### 关键设置

| 步骤 | 设置 |
|------|------|
| Static 标记 | 确保模型有非重叠 UV |
| UV 生成 | 如无 UV2，勾选 "Generate Lightmap UVs" |
| Linear 模式 | 建议启用以获得更好的光照质量 |
| 修复 Gamma | 点击 "Fix" 按钮修复线性强度 |

---

## 5. 渲染设置

### 5.1 Render Mode（渲染模式）

| 模式 | 说明 |
|------|------|
| **Full Lighting** | 完整直接+间接光照（推荐） |
| **Indirect** | 混合模式：实时直接光 + 烘焙间接光/GI |
| **Shadowmask** | 烘焙阴影遮罩 |
| **Distance Shadowmask** | 距离遮罩（根据距离切换实时/烘焙阴影） |
| **Subtractive** | 减法模式（Unity 传统混合） |
| **Ambient Occlusion Only** | 仅环境光遮蔽 |

### 5.2 Directional Mode（方向模式）

| 模式 | 说明 | 质量 |
|------|------|------|
| **None** | 无方向信息 | 最低 |
| **Baked Normal Maps** | 烘焙法线贴图 | 高 |
| **Dominant Direction** | 主方向 | 中 |
| **RNM** | 方向编码（4通道） | 高 |
| **SH** | 球谐函数 | 中 |
| **MonoSH** | 单通道球谐 | 低 |

### 5.3 关键参数

| 参数 | 说明 | 建议值 |
|------|------|--------|
| **Texels per unit** | 每单位 Texel 数量 | 1-50（根据需求） |
| **Max resolution** | 最大光照贴图分辨率 | 2048-4096 |
| **Bounces** | 光反弹次数 | 2-4 |
| **Samples** | 采样数 | 512-2048 |
| **GPU Priority** | GPU 优先级 | 50-100 |

### 5.4 高级设置

| 设置 | 说明 |
|------|------|
| **Denoiser** | 降噪器（支持 OIDN） |
| **Fix Seams** | 修复接缝 |
| **Split by scene** | 按场景分割 |
| **Hole filling** | 填补空洞 |
| **Backface GI** | 背面 GI |
| **Ambient Occlusion** | 环境光遮蔽 |
| **RTX Mode** | RTX 加速模式 |

---

## 6. 组件

### 6.1 Bakery Lightmap Group Selector

控制对象的光照贴图分组。

### 6.2 Bakery Direct Light

替换 Unity Directional Light，支持烘焙。

| 功能 | 说明 |
|------|------|
| Match lightmapped to real-time | 匹配 Unity 实时灯光参数 |
| 修复线性强度 | 修复 Gamma 模式问题 |

### 6.3 Bakery Sky Light

环境光照/天光。

| 功能 | 说明 |
|------|------|
| Match scene skybox | 匹配场景天空盒 |

### 6.4 Bakery Light Mesh

发光网格（自发光光源）。

### 6.5 Bakery Point Light

点光源烘焙。

### 6.6 Bakery Volume

体积光照探针。

### 6.7 Bakery Light Filter

光照过滤器。

### 6.8 Bakery Sector

扇区（大型场景分区）。

---

## 7. 材质兼容性

### 7.1 Albedo 和 Emission

Bakery 从材质的 Albedo 和 Emission 通道读取数据。

### 7.2 Opacity

- 支持 Alpha 混合
- 可选 Alpha Meta Pass

### 7.3 Normal Mapping

支持法线贴图。

### 7.4 Front/Back Faces

可配置正面/背面烘焙。

---

## 8. 常见问题 FAQ

### Q: Bakery 支持实时 GI 吗？

**A**: 不支持。实时 GI 需要使用 Enlighten 或其他方案。

### Q: 支持混合光照吗？

**A**: 是的。支持烘焙间接光 + 实时直接光的混合模式，以及 Shadowmask 和 Subtractive 模式。

### Q: 支持多 GPU 吗？

**A**: 是的。基于 OptiX，支持多 GPU 加速。注意：RTX 模式下所有 GPU 必须都是 RTX。

### Q: 可以导出光照贴图到其他程序吗？

**A**: 可以。有两种方式：
1. 在建模软件中完整展开场景（推荐）
2. 使用 Make Exportable 脚本生成新 UV

### Q: 支持运行时烘焙吗？

**A**: 技术上可以，但需要大量编码。编辑器版本仅用于编辑器烘焙。

### Q: Unity Lighting 窗口需要修改什么？

**A**: 无需修改。唯一例外是使用 Subtractive 模式时的阴影颜色。

---

## 9. 故障排除

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 内存不足 | 降低 Texels per unit，减少 Max resolution |
| "Can't map texture" | 关闭其他程序，降低分辨率 |
| "Can't create texture" | 确保 UV2 无重叠，启用 Generate Lightmap UVs |
| 降噪器错误 505 | 更新驱动，使用 Legacy 降噪器（Kepler） |
| 烘焙崩溃 | 检查 GPU 驱动，更新到最新 |
| 阴影锯齿 | 增加 Samples 或启用降噪 |
| 场景在构建中为黑色 | 检查光照贴图是否正确打包 |

### 重要检查项

1. **Shadowmask 未烘焙**
   - 检查 Render Mode 是否为 Shadowmask
   - 确保灯光有 Bakery 组件
   - Baked contribution 设置为 "Indirect and shadowmask"

2. **实时阴影代替烘焙阴影**
   - 使用 Distance Shadowmask 模式
   - 或切换到 Subtractive 模式

3. **无高光**
   - 使用 Reflection Probes
   - 使用混合灯光
   - 烘焙 Dominant Direction 或 SH 模式

4. **版本控制问题**
   - 确保使用 Bakery 的版本控制指南

5. **UV 在场景间被破坏**
   - 使用 "Don't Change" 禁用 UV padding 调整
   - 使用自定义 UV
   - 使用 "Adjust UV padding only for new meshes"

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-06-05 | 初始创建 |

## 来源

- geom.io/bakery/wiki/index.php?title=Manual
- geom.io/bakery/wiki/index.php?title=FAQ
- geom.io/bakery/wiki/index.php?title=Troubleshooting