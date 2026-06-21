# Configurable Shader 系统

> ORL Shaders 的核心创新 - 模块化可组合着色器

## 概念

Configurable Shader 是一种 **模块化 Uber Shader 系统**，允许用户：
- 自由组合 ORL 提供的功能模块
- 基于已有 Shader（如 Vertex Animation）扩展新功能（如添加 LTCGI）
- 减少材质变体数量，提升 Draw Call Batching

## 创建流程

### 1. 创建 Configurable Shader

```
右键 Project Window → Create → Shader → orels1 → Configurable Shader
```

### 2. 命名并添加模块

在 Inspector 中：
1. 设置 Shader 名称
2. 点击 `+` 添加模块
3. 选择模块类型（Dissolve/LTCGI 等）

### 3. 使用 Base Shader（可选）

不想从头组合？可以直接基于已有 Shader：
1. 选择 Base Shader 下拉框（如 `ORL Standard Vertex Animation`）
2. 移除不需要的模块（如 `BaseColor`）
3. 添加新模块（如 `LTCGI`）

## 可用模块

### 基础模块

| 模块 | 说明 |
|------|------|
| **BaseColor** | 基础颜色纹理 |
| **Custom GI Diffuse Ramp** | 自定义 GI 漫反射渐变 |
| **Depth Fade** | 深度淡入效果 |
| **Dither Fade** | 抖动淡入效果 |
| **Masked Tweaks** | 遮罩调整 |
| **SSR** | 屏幕空间反射 |
| **Vertex Colors** | 顶点颜色支持 |

### 功能模块（来自 Standard Shader）

| 模块 | 来源 | 说明 |
|------|------|------|
| **Dissolve** | Standard Dissolve | 溶解效果 |
| **AudioLink** | Standard AudioLink | 音频响应 |
| **Puddles** | Standard Puddles | 水坑效果 |
| **Neon** | Standard Neon Light | 霓虹灯光 |
| **Vertex Animation** | Standard Vertex Animation | 顶点动画 |
| **LTCGI** | Standard LTCGI | LTCGI 光照 |
| **Layered Parallax** | Standard Layered Parallax | 分层视差 |

## 高级功能

### 自定义模块

如果你是 Shader 开发者：

1. 创建 `.orlsource` 文件（ORL Shader 源文件）
2. 在 Configurable Shader Inspector 中勾选 `Custom Module`
3. 选择你的自定义模块文件

### 自定义 Lighting Models

ORL Shader Generator 支持创建自定义光照模型：

1. 创建 Lighting Model 定义
2. 在 Configurable Shader 中选择
3. 支持 Toon/PBR 等模式

## 使用限制与注意事项

| 限制 | 说明 |
|------|------|
| **禁止重复模块** | 不应添加两个相同的模块 |
| **BaseShader 冲突** | 使用 Base Shader 时不应再添加 BaseColor |
| **Toon 模式** | Toon 模块建议配合 Toon Lighting Model |
| **性能考量** | VFX 模块性能优于 PBR，除非需要光照/反射功能 |

## 性能优化建议

| 建议 | 说明 |
|------|------|
| **使用 VFX 模块** | 除非需要 PBR 特性（光照/反射），否则使用 VFX 版本 |
| **减少变体数量** | Configurable 可以合并多个效果，减少 Draw Call |
| **模块组合测试** | 复杂组合可能影响性能，需测试 |

## 示例

### 示例 1: Vertex Animation + LTCGI

```
1. 新建 Configurable Shader
2. Base Shader → 选择 "ORL Standard Vertex Animation"
3. 移除 BaseColor 模块
4. 添加 LTCGI 模块
5. 完成！该 Shader 继承 Vertex Animation 并支持 LTCGI
```

### 示例 2: 音频响应护盾

```
1. 新建 Configurable Shader
2. 使用 PBR Lighting Model
3. 添加 BaseColor 模块
4. 添加 Dissolve 模块
5. 添加 AudioLink 模块（Band Selection）
6. 完成！护盾材质 + 溶解 + 音频响应
```

## 与其他系统的对比

| 系统 | 灵活性 | 性能 | 学习成本 |
|------|--------|------|----------|
| **Standard Shader** | 低（固定功能组合） | 优化 | 低 |
| **Configurable Shader** | 高（自由组合） | 中等 | 中 |
| **手动编写 Shader** | 最高 | 最优 | 高 |

## 相关文档

- [Overview](./overview.md) - 项目概览
- [Shader List](./shader-list.md) - 详细列表
- [Comparison](./comparison.md) - Shader 对比