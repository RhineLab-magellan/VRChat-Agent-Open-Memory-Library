---
title: VRCQualitySettings
category: world
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-15
confidence: Medium
tags:
  - world
  - light
  - udonsharp
aliases:
  - VRCQualitySettings
  - vrc-quality-settings
related:
  - "world/udon/vrc-graphics/index.md"
  - "world/vrc-camera-settings.md"
  - "world/performance-guide.md"
  - "world/bakery/light-baking-guide.md"
---
# VRCQualitySettings


---

## Overview

`VRCQualitySettings` 是 `UnityEngine.QualitySettings` 的**精简只读层**，加上**有限的阴影控制**。

**设计目的**:
- 让 World 脚本感知当前质量设置
- 允许 World 临时**覆盖**阴影距离和阴影级联
- 不暴露 `QualitySettings` 的全部 API（出于安全和性能考虑）

---

## 只读属性

```csharp
int     VRCQualitySettings.vSyncCount;
int     VRCQualitySettings.ShadowCascades;
float   VRCQualitySettings.ShadowDistance;
ShadowResolution VRCQualitySettings.ShadowResolution;
int     VRCQualitySettings.MaximumLODLevel;
float   VRCQualitySettings.LODBias;
int     VRCQualitySettings.PixelLightCount;
int     VRCQualitySettings.AntiAliasing;
```

| 属性 | 类型 | 说明 |
|------|------|------|
| `vSyncCount` | `int` | VSync 计数（0/1/2） |
| `ShadowCascades` | `int` | 阴影级联数（1/2/4） |
| `ShadowDistance` | `float` | 阴影距离（米） |
| `ShadowResolution` | `ShadowResolution` | 阴影贴图分辨率 |
| `MaximumLODLevel` | `int` | 最大 LOD 等级 |
| `LODBias` | `float` | LOD 偏置 |
| `PixelLightCount` | `int` | 逐像素光数量 |
| `AntiAliasing` | `int` | 抗锯齿采样数（1/2/4/8） |

**注意**:
- 部分属性可能受用户图形设置影响
- 所有属性**仅只读**
- World 加载时自动重置

---

## Shadow Distance（阴影距离覆盖）

### 基础 API

```csharp
VRCQualitySettings.SetShadowDistance(float value);  // 全部使用同一值
VRCQualitySettings.SetShadowDistance(float low, float medium, float high, float mobile);
VRCQualitySettings.ResetShadowDistance();
```

### 多档位 API 参数

| 参数 | 对应用户设置 | 适用平台 |
|------|--------------|----------|
| `low` | Low 阴影质量 | PC Low |
| `medium` | Medium 阴影质量 | PC Medium |
| `high` | High 阴影质量 | PC High |
| `mobile` | **强制**用于所有非 PC 平台 | Quest、Android 等 |

**使用规则**:
- 指定不同值时，VRChat 选用**匹配本地用户当前设置**的参数
- `mobile` 参数**无视**用户设置，**强制**用于所有非 PC 平台
- 4 个参数都相同时，使用单参数重载

### 约束

| 项目 | 值 |
|------|---|
| 最小 | `0.1f` |
| 最大 | `10000.0f` |
| 单位 | 米 |

**超出范围**会被自动 clamp。

### 副作用

调用 `SetShadowDistance()` 后：

1. **用户配置的 Shadow Quality 设置被覆盖**
2. 用户在图形设置中**看到警告**
3. 性能影响：
   - 较大的值 = 阴影计算范围更广 = 性能开销更大
4. 加载新 World 时**自动重置**

### 取消覆盖

```csharp
VRCQualitySettings.ResetShadowDistance();
```

恢复用户配置的阴影距离。

---

## 阴影级联（可读写）

```csharp
Vector3 VRCQualitySettings.shadowCascade4Split;  // 4 级联分割比例
float   VRCQualitySettings.shadowCascade2Split;  // 2 级联分割比例
```

**适用场景**:
- 4 级联时调整每级之间的深度分割
- 2 级联时调整近/远级联的比例
- 1 级联（无分割）时此值无意义

**注意**:
- 这两个属性在 World Load 时也会重置
- 写入时需根据 `ShadowCascades` 当前值选择调整哪个

---

## 事件

### OnVRCQualitySettingsChanged

```csharp
public override void OnVRCQualitySettingsChanged()
{
    // 用户改变了影响暴露属性的图形设置
    // 重新读取 vSyncCount, ShadowDistance 等
}
```

**触发场景**:
- 用户在图形设置中改动 Low/Medium/High 质量
- 移动端/桌面端切换
- 部分属性实时变化

---

## 使用模式

### 模式 1: 动态阴影管理

```csharp
public override void OnPlayerTriggerEnter(Collider other)
{
    if (!Networking.IsOwner(gameObject)) return;
    
    // 玩家进入大区域：扩大阴影范围
    VRCQualitySettings.SetShadowDistance(
        50f,   // PC Low
        100f,  // PC Medium
        200f,  // PC High
        30f    // Quest
    );
}

public override void OnPlayerTriggerExit(Collider other)
{
    if (!Networking.IsOwner(gameObject)) return;
    
    // 玩家离开：恢复用户配置
    VRCQualitySettings.ResetShadowDistance();
}
```

### 模式 2: 跨平台预设

```csharp
void Start()
{
    // 性能优先设置：所有平台用同一保守值
    VRCQualitySettings.SetShadowDistance(100f);
    
    // 4 级联优化：把更多分辨率给近处
    VRCQualitySettings.shadowCascade4Split = new Vector3(0.05f, 0.2f, 0.5f);
}
```

### 模式 3: 响应用户设置变化

```csharp
public override void OnVRCQualitySettingsChanged()
{
    Debug.Log($"[Quality] User changed settings. Shadow distance: " +
              $"{VRCQualitySettings.ShadowDistance}");
    // 重新校准 World 内的 LOD 切换、粒子密度等
}
```

---

## 性能陷阱

| 陷阱 | 后果 |
|------|------|
| 阴影距离设置过大 | 阴影计算成本指数级增长；Quest 尤其敏感 |
| 4 级联分割不合理 | 远级联分辨率浪费，附近阴影锯齿 |
| 设置后忘记 `ResetShadowDistance` | 用户切换 World 后还会保留你的设置（**自动重置只在新 World 加载时**） |
| 频繁调用 `SetShadowDistance` | 不会立即生效，VRChat 内部有去抖 |

---

## 与 Unity QualitySettings 关系

`VRCQualitySettings` 是 `UnityEngine.QualitySettings` 的**子集包装**：

| 能力 | `QualitySettings` | `VRCQualitySettings` |
|------|-------------------|----------------------|
| 读取 8 个核心属性 | ✅ | ✅ |
| 修改 vSync/LOD/抗锯齿 | ✅ | ❌ |
| 修改 Shadow Distance | ✅ | ✅（带约束） |
| 修改 Shadow Cascade | ✅ | ✅ |
| 切换 Quality Level | ✅ | ❌ |
| 设置 VSyncCount | ✅ | ❌ |

**为什么 Udon 不暴露全部 QualitySettings**:
- 防止恶意 World 强制低质量损害视觉体验
- 防止 World 强制修改用户偏好
- 阴影控制是 World 表现需求中的**核心需求**（大场景、室外昼夜）

---

## 相关文档

- `memory/world/udon/vrc-graphics/index.md` - VRCShader / VRCGraphics API
- `memory/world/vrc-camera-settings.md` - VRCCameraSettings
- `memory/world/performance-guide.md` - 渲染性能优化
- `memory/world/bakery/light-baking-guide.md` - Bakery 光照烘焙
