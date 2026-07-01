---
title: "VRC Mirror Reflection"
category: world
subcategory: scene-components
knowledge_level: applied
status: active
source: "本地知识库整理 + VRChat 2026.1.3 / 2026.1.3p2 / 2026.2.1 Release Notes"
source_type: community
version: 1.1
last_review: 2026-06-30
confidence: Medium
tags:
  - world
  - shader
  - mirror
  - light
  - occlusion
  - reflection
aliases:
  - "VRC Mirror Reflection"
  - vrc-mirrorreflection
related:
  - "../reflection-probes.md"
  - "../performance-guide.md"
  - textmeshpro.md
  - vrc-avatarpedestal.md
  - vrc-cameradolly.md
---
# VRC Mirror Reflection

> 实时反射镜面组件
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_mirrorreflection/
> 官方类名: `VRC_MirrorReflection`
> 最新更新日期: 2024-07-31 (基础) / 2026-05-28 (2026.2.1 Open Beta Build 1832 时序变更修复)

---

## 🔄 Mirror Render Timing 变更历史 (2026.1.3 - 2026.2.1)

> **FACT**:VRChat 在 2026.1.3 改动了 Mirror 渲染时序,引发问题后回滚,最终在 2026.2.1 修复后重新启用。

### 时间线

| 版本 | 变更 | 结果 |
|------|------|------|
| 2026.1.3 | Mirror 渲染从 `OnWillRenderObject` 改为 `Camera.onPreCull` | 性能改进预期 |
| 2026.1.3 (同期) | 出现**性能回归** | 客户端普遍卡顿 |
| 2026.1.3p2 | **回滚** 渲染时序变更 | 性能恢复 |
| 2026.2.1 Open Beta Build 1832 | 确认是**根因**,修复后**重新启用** `OnPreCull` | 性能改进 + 无回归 |

### 官方原话(2026.2.1 Open Beta Build 1832)

> "Small update on the performance regressions from 2026.1.3:
> - The mirror-timing change (`OnWillRenderObject` -> `OnPreCull`) that was reverted in 2026.1.3p2 is now confirmed to be the root cause of the issue.
> - This update adds it back into the open-beta branch, but with a fix for the part that caused the performance issue, we hope."

### 对创作者的影响

| 影响 | 说明 |
|------|------|
| **无代码改动** | 现有 VRC_MirrorReflection 用法无需修改 |
| **性能改进** | 2026.2.1+ 客户端性能更好(理论上) |
| **旧版客户端行为** | 2026.1.3p2 - 2026.2.0 客户端使用 `OnWillRenderObject`(旧行为) |
| **测试建议** | World 发布前在最新客户端测试 Mirror 性能 |

---

## 概述

`VRC_MirrorReflection` 用于在 VRChat World 中创建镜面,玩家可以看到自己的倒影。

> **FACT** (来自官方文档): 组件要求同一 GameObject 上有 `MeshRenderer` 组件。它会写入 MeshRenderer 第一个材质的 `_MainTex` 字段。
> **FACT**: SDK 中提供了 `VRCMirror.prefab` 作为示例 Prefab。

---

## Inspector 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| **Disable Pixel Lights** | Bool | false | 禁用实时像素着色点光源和聚光灯。启用时像素光源回退到顶点着色 |
| **Turn Off Mirror Occlusion** | Bool | false | 禁用镜面遮挡剔除。镜面中物体闪烁时启用此选项 |
| **Reflect Layers** | LayerMask | Default | 选择要反射的层。**Water 层永远不会在镜面中渲染** |
| **Mirror Resolution** | enum | Auto | 镜面渲染分辨率(VR 中每只眼睛)。Auto 渲染与用户 HMD/显示器相同分辨率,**最大 2048x2048** |
| **Maximum Antialiasing** | enum | 1x | 镜面图像 MSAA 最大级别。可被客户端图形设置覆盖 |
| **Custom Shader** | Shader | null | 若提供,镜面将使用此 Shader 替代默认 |
| **Camera Clear Flags** | enum | From Reference Camera | 镜面清除背景的方式。"From Reference Camera" 使用与相机相同的标志 |
| **Custom Skybox** | Material | null | 当 "Camera Clear Flags" 设为 "Custom Skybox" 时显示的天空盒。若 "Custom Skybox" 模式但未提供,背景为黑色 |
| **Custom Clear Color** | Color | 黑色 | 当 "Camera Clear Flags" 设为 "Solid Color" 时使用的颜色。**注意 alpha 通道会被尊重**,可用于自定义 Shader 的 cutout 镜面 |

---

## Mirror Resolution 选项

| 值 | 分辨率 |
|----|--------|
| **Low (256x256)** | 低质量,性能最佳 |
| **Medium (512x512)** | 中等质量,推荐 Quest |
| **High (1024x1024)** | 高质量,PC 推荐 |
| **Ultra (2048x2048)** | 最高质量,**仅 PC 支持** |
| **Auto** | 渲染与 HMD/显示器相同,最大 2048x2048 |

> **FACT**: 显示分辨率超过 2048px 时,镜面质量反而下降。
> 用户可在 VRChat 设置中将镜面分辨率切换为 "Unlimited",可提高质量但**显著降低 VRChat 性能**。

---

## ⚠️ 性能警告

> **FACT** (来自官方文档): 镜面会**大幅降低** VRChat 世界的帧率。

### 优化建议

1. **默认关闭镜面** - 仅在玩家接近时自动启用,或允许玩家手动开启
2. **不要反射所有层** - 允许玩家选择反射哪些层("高质量"和"低质量"镜面)
3. **降低镜面分辨率** - 用户仍遇到性能问题时,降低 Mirror Resolution
4. **避免多个镜面** - 2 个以上镜面可能造成严重性能下降
5. **Quest 特别注意** - 推荐 Low/Medium,**Ultra 仅 PC 支持**

### 平台性能分级

| 平台 | 推荐 Mirror Resolution | 同时镜面数 |
|------|----------------------|----------|
| **Quest 2/3** | Low (256) 或 Medium (512) | 1 个 |
| **PC (低端)** | Medium (512) | 1-2 个 |
| **PC (高端)** | High (1024) 或 Ultra (2048) | 2-3 个 |

---

## U# 引用方式

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Reflection;

public class MirrorController : UdonSharpBehaviour
{
    [SerializeField] private VRC_MirrorReflection mirror;
    [SerializeField] private float enableDistance = 5f;
    
    private Transform playerTransform;
    
    private void Update()
    {
        // 根据玩家距离动态启用/禁用
        if (playerTransform == null) return;
        
        float distance = Vector3.Distance(transform.position, playerTransform.position);
        bool shouldEnable = distance <= enableDistance;
        
        if (mirror.enabled != shouldEnable)
        {
            mirror.enabled = shouldEnable;
        }
    }
}
```

> **FACT**: 直接启用/禁用 `VRC_MirrorReflection` 组件即可控制镜面显示。**禁用后零渲染开销**。

---

## 关键行为

### Reflect Layers

通过 `Reflect Layers` LayerMask 控制反射范围:
- **Default**: 反射大部分物体
- **TransparentFX + UI**: 不反射(避免 UI 镜面污染)
- **Player**: 可选择是否反射玩家(默认包含)
- **Water**: **永远不会在镜面中渲染**(VRChat 强制)

### Render Order

镜面使用额外相机渲染,层级为:
1. 镜面相机渲染 → 写入 `_MainTex`
2. MeshRenderer 使用更新后的 `_MainTex` 渲染镜面平面
3. 镜面平面按 normal 方向作为反射向量

### Occlusion 问题

如果镜面中物体**闪烁/消失**:
- 启用 `Turn Off Mirror Occlusion`
- 缺点: 失去遮挡剔除优化,降低性能
- 替代方案: 调整镜面 Reflect Layers 减少渲染对象

---

## Custom Shader 用例

通过 `Custom Shader` 字段可以:
1. **扭曲效果** - 使用噪声扭曲反射
2. **半透明镜面** - 修改 alpha 通道实现半透明
3. **着色效果** - 添加色相、色调调整
4. **性能优化** - 自定义 LOD 镜面

```csharp
[SerializeField] private VRC_MirrorReflection mirror;
[SerializeField] private Shader customShader;

public void ApplyCustomShader()
{
    // 注意:Custom Shader 在 Inspector 中设置,通常不在 U# 中动态修改
    // 运行时修改 Shader 需要访问 Material 实例
}
```

---

## 典型应用场景

### 1. 浴室 / 化妆镜

经典应用。Mirror Resolution 推荐 High,Reflect Layers 包含 Player。

### 2. 反光地板

`VRC_MirrorReflection` 只能用于垂直镜面,水平反射(如地板)需要其他技术:
- Reflection Probe(静态反射,详见 [../reflection-probes.md](../reflection-probes.md))
- 平铺镜面(昂贵)

### 3. VR 视线跟踪

VR 用户通过镜面查看自己,Mirror Resolution 建议 Medium 避免眩晕。

### 4. 反光表面艺术效果

使用 Custom Shader 实现扭曲、模糊、玻璃感效果。

---

## 与其他组件的依赖

| 关联组件 | 关系 |
|----------|------|
| **MeshRenderer** | 强依赖,镜面必须有网格渲染器 |
| **Material** | 强依赖,镜面使用材质的 `_MainTex` |
| **VRC_SceneDescriptor** | 无直接依赖 |
| **VRC_UIShape** | 可与 UI 配合,提供"开关镜面"按钮 |
| **Reflection Probe** | 互补,处理静态反射 |

---

## 最佳实践

1. **远离玩家自动关闭**: 用 `OnTriggerEnter`/`OnTriggerExit` 控制
2. **提供开关**: 玩家在性能受限时手动关闭
3. **使用 LayerMask**: 限制反射范围,减少 GPU 负载
4. **Quest 限制**: 同时镜面数 ≤ 1,Mirror Resolution ≤ Medium
5. **不要滥用 Custom Shader**: 自定义 Shader 增加开发复杂度

---

## 常见陷阱

1. **忘加 MeshRenderer**: 镜面无视觉显示
2. **材质无 `_MainTex`**: 自定义 Shader 没有 `_MainTex` 时镜面失效
3. **Mirror Resolution 设为 Ultra 在 Quest**: 不支持,自动降级或黑屏
4. **多个镜面同时启用**: 性能急剧下降
5. **Water 层误包含**: 永远不会被反射,不必担心
6. **未启用 MeshRenderer 材质的 Read/Write**: 某些情况下需要

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_mirrorreflection/
- 静态反射: [../reflection-probes.md](../reflection-probes.md)
- 性能指南: [../performance-guide.md](../performance-guide.md)
- 模式: `patterns/distance-based-mirror-toggle.md` (后续任务)
