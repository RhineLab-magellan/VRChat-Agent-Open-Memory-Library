# Minimap

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/minimap)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/minimap
> 文档版本: Last updated Nov 6, 2024
> SDK: 3.5+ (VRCGraphics.Blit / RenderTexture)

## Example Central Package

> ✅ **需要 Example Central Package**
> 通过 `VRChat SDK → 🏠 Example Central` 导入
> 包含 Minimap Prefab、Camera、Custom Shader (MiniMap Blit)、Pickup 逻辑

### Example World
- **World ID**: `wrld_12492ad5-ff17-445d-9f90-7b14376b1f32`
- **URL**: https://vrchat.com/home/world/wrld_12492ad5-ff17-445d-9f90-7b14376b1f32

> ⚠️ **此 World ID 与 Player Join Zones 共享**

---

## 概述

演示一个 **可拾取的小地图**:
- 蓝色点: 本地玩家位置
- 绿色点: 其他玩家(可选显隐)
- 顶部摄像机俯视捕获场景
- 通过 Custom Shader 在纹理上叠加玩家位置点
- 可拾取,随玩家移动

---

## 关键 Udon API

| API | 角色 | 说明 |
|-----|------|------|
| `VRCGraphics.Blit(Texture source, RenderTexture dest, Material mat, int pass)` | 渲染管线 | 等同 Unity `Graphics.Blit`,但可用于 Udon |
| `RenderTexture` | 渲染目标 | 摄像机输出和 Shader 处理的中间介质 |
| `Custom Material/Shader` | 视觉效果 | 在地图上叠加玩家位置点 |

### 与 Unity `Graphics.Blit` 的关系

> 文档原话: "One of the benefits of Graphics.Blit is that you get a regular texture out of it, which you can in turn use for anything you want!"

**优势**:
- 输出是**普通 Texture**,可用于任何用途(UI、材质、贴图等)
- 可通过控制 `Graphics.Blit` 调用频率**控制更新率**
- 通过 Shader 实现复杂视觉效果

---

## 核心架构

### 渲染管线

```
┌─────────────────┐
│ 场景 + Player   │
└────────┬────────┘
         │ (Camera from above)
         ▼
┌─────────────────┐
│  MiniMap RT     │ (RenderTexture)
│  (基础俯视图)    │
└────────┬────────┘
         │ (VRCGraphics.Blit + Material)
         ▼
┌─────────────────┐
│  Final Texture  │ (叠加了 Player 圆点)
│  MiniMap Blit   │
└────────┬────────┘
         │ (应用为 Main Texture + Emission)
         ▼
┌─────────────────┐
│  Pickup 的材质   │ (玩家手中的小地图)
└─────────────────┘
```

---

## 核心 Udon 逻辑

### Start 阶段
- 启动场景中的 Camera(俯视玩家)
- Camera 渲染到 `RenderTexture` (MiniMap RT)

### Update 阶段

```csharp
private void Update()
{
    // 获取本地玩家位置
    Vector3 playerPos = Networking.LocalPlayer.GetPosition();

    // 通过 Blit 把玩家位置传入 Shader
    VRCGraphics.Blit(
        _miniMapRT,           // source
        _finalTexture,        // destination
        _miniMapMaterial,     // material
        0                     // pass
    );

    // Shader 通过 _PlayerPos 知道在哪个位置画点
    _miniMapMaterial.SetVector("_PlayerPos", playerPos);
    _miniMapMaterial.SetVector("_MapMin", _mapMin);
    _miniMapMaterial.SetVector("_MapMax", _mapMax);
}
```

### 关键点
- 玩家位置每帧传递给 Material
- Shader 在 Blit 时叠加圆点
- 可选: 遍历所有其他玩家,叠加绿色点(用 `_ShowOthersToggle` 控制)

---

## Pickup 实现

文档原话: "The pickup, in turn, is incredibly simple."

```csharp
// Pickup 本身无逻辑,只依赖材质配置
// Material 的 Main Texture 和 Emission = MiniMap RT (最终输出纹理)
```

**实现技巧**:
- 整个 Prefab 可被玩家拾取
- 拾取后随玩家移动
- 材质自动应用最新的 Minimap 纹理

---

## 自定义要点

### 1. 调整更新率
```csharp
// 在 Update 中:
if (Time.frameCount % 5 == 0)  // 每 5 帧更新一次
    VRCGraphics.Blit(_src, _dst, _mat, 0);
```
- 高频更新 = 更流畅但更耗 GPU
- 低频更新 = 省 GPU 但有滞后

### 2. 显示其他玩家
- Inspector 暴露 `_ShowOthersToggle` 变量
- 切换时遍历玩家列表,调用 `player.GetPosition()`
- 所有玩家位置传入 Shader,叠加绿色点

### 3. MaxPlayers 设置
> ⚠️ 文档原话: "If you're going to use this Example Prefab in your world, don't forget to adjust `MaxPlayers` variable to match your `World Capacity`."

- World Capacity 决定实例最大玩家数
- `MaxPlayers` 影响 Shader 中循环展开的数量
- 两者不一致会导致数组越界

---

## 重要: 配套 Shader

本页使用的 `MiniMap Blit` 是**自定义 Shader**,不是 SDK 自带。
- 通过 Example Central Package 导入时一并提供
- 使用 SetVector API 向 Shader 传玩家位置和地图范围
- 详细 Shader 代码需查看导入的 Package

---

## 与知识库互补

- **VRCGraphics 完整 API**: `memory/world/vrc-graphics.md` ⭐ 直接互链
- **RenderTexture 概念**: 通用 Unity 知识,`memory/unity-rendering.md`(待建)
- **VRCPickup**: `memory/world/components/pickup.md`(待建)
- **Networking.LocalPlayer.GetPosition()**: `memory/api/player-api.md`(待建)
- **VRCShader.SetGlobal**: `memory/world/vrc-graphics.md` 中相关章节

## 相关 Udon 文档链接

- [VRCGraphics API 完整文档](/worlds/udon/graphics) (待链接验证)
- [VRCShader 完整文档](/worlds/udon/shader-programming) (待链接验证)
- [Unity Graphics.Blit](https://docs.unity3d.com/ScriptReference/Graphics.Blit.html)
