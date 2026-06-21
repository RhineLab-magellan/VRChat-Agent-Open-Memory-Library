# lilToon 轮廓线设置

> 二次审计补充(2026-06-15):此文件原被 `index.md` / `advanced-settings.md` / `stencil.md` / `fur.md` / `variations.md` / `reflection-settings.md` 引用,但实际不存在,已通过整合 `advanced-settings.md` 中的内容创建。

---

## 概述

**轮廓线(Outline)** 是 lilToon 的线画效果,支持纹理控制粗细和颜色。
- 独立 Shader 关键词:`LILTOON_OUTLINE`
- 在 3D 空间叠加于主着色器之上
- 可通过 Mask 通道、顶点颜色控制

---

## 主要参数

| 参数 | 说明 |
|------|------|
| **テクスチャ** | 轮廓线纹理/颜色 |
| **色相/彩度/明度/ガンマ** | 颜色调整 |
| **焼き込み** | 导出校正后纹理 |
| **ハイライト** | 轮廓高光设置 |
| **ライティングを適用** | 应用光照 |
| **マスクと太さ** | 轮廓粗细遮罩 (R 通道) |
| **太さを補正** | 距离粗细校正 |
| **頂点カラー** | 顶点颜色:None / R→Width / RGBA→Normal&Width |
| **太さ0の頂点を削除** | 删除零粗细顶点 |
| **Z Bias** | 前后移动轮廓 |
| **ノーマルマップ** | 轮廓挤出方向调整 |

---

## 顶点颜色烘焙

用于硬边模型的光滑轮廓:

```
步骤:顶点颜色烘焙工具
1. 准备光滑法线模型
2. 应用烘焙工具
3. 分配给轮廓线着色器
```

---

## Stencil 中的轮廓线协同

轮廓与主材质的 Stencil 配置需要协调(详见 `stencil.md` 第 143 节):

| 属性 | 本体 | 轮廓线 |
|------|------|--------|
| Ref | 1 | 1 |
| Pass | Replace | Replace |

---

## 相关文档

- [扩展功能设置](advanced-settings.md) — 视差/轮廓线原始章节
- [Stencil 设置](stencil.md) — 3D 空间遮罩与轮廓线协同
- [基本设置](basic-settings.md) — `LILTOON_OUTLINE` Shader 关键词
- [优化指南](optimization.md) — 轮廓线遮罩优化

---

## 修复审计(2026-06-15)

| 项 | 状态 |
|----|------|
| 引用方 | 6 个文件(`index.md` / `variations.md` / `fur.md` / `stencil.md` / `advanced-settings.md` / `reflection-settings.md`)|
| 内容来源 | `advanced-settings.md` 第 5-35 行 |
| 修复方式 | 创建本文件作为主题页,引用原始详细章节 |
| 状态 | ✅ 已修复 |
