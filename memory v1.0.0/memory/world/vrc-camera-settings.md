# VRCCameraSettings

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/udon/vrc-graphics/vrc-camera-settings/)
> 原始仓库: github.com/vrchat-community/creator-docs
> 索引日期: 2025-08-27
> 置信度: High
> SDK: 3.10.3+
> Last Updated: 2026-06-15

---

## Overview

`VRCCameraSettings` 暴露用户屏幕相机、手持相机以及 Unity 全局质量设置的**只读信息**和**有限控制**能力。

**重要限制**:
- 不能直接访问原始 `Camera` 组件（出于安全考虑）
- 用户自己放入 World 的 `Camera` 组件可正常访问
- 替换了 Unity 的 `Camera.current`（因为 `Camera.current` 仅在渲染事件中填充）

**使用场景**:
- 在 `OnWillRenderObject` 中判断当前是哪个相机正在渲染
- 获取 VR 双眼位置/旋转
- 检测手持相机是否启用（Active）
- 响应相机设置变化

---

## 静态实例

```csharp
VRCCameraSettings.ScreenCamera   // 屏幕主相机（始终存在）
VRCCameraSettings.PhotoCamera    // 手持拍照相机（Spout 推流启用时也 Active）
```

| 实例 | 说明 |
|------|------|
| `ScreenCamera` | 始终 Active，代表用户的主视点相机 |
| `PhotoCamera` | 手持拍照相机的预览相机，**按快门时**属性会与拍照/推流相机同步 |

**注意**: `PhotoCamera` 始终指向**预览图像**的相机，不是拍照本身的相机或推流相机的渲染视图。

---

## 实例属性

这些实例会暴露 `UnityEngine.Camera` 的部分属性（参考 Unity 文档获取详细信息）。

### Active

```csharp
bool VRCCameraSettings.ScreenCamera.Active;  // 始终为 true
bool VRCCameraSettings.PhotoCamera.Active;   // 手持相机启用时为 true
```

| 值 | 含义 |
|---|---|
| `ScreenCamera.Active` | 始终 `true` |
| `PhotoCamera.Active` | 手持相机启用时 `true`；Spout 推流启用时也 `true` |

**典型用法**: 检测手持相机是否启用。
```csharp
if (VRCCameraSettings.PhotoCamera.Active) { /* 手持相机已开 */ }
```

### StereoEnabled

```csharp
bool VRCCameraSettings.ScreenCamera.StereoEnabled;  // VR 用户为 true
```

**典型用法**: 检测用户是否在 VR 中（**比 `XR.enabled` 更可靠**）。

### CameraMode

```csharp
CameraMode VRCCameraSettings.ScreenCamera.CameraMode;
CameraMode VRCCameraSettings.PhotoCamera.CameraMode;
```

参见 [Camera Mode](#camera-mode) 章节。

### 屏幕 / 拍照相机 Pos/Rot

知识库 `vrc-graphics.md` 的 `_VRChatScreenCameraPos` / `_VRChatPhotoCameraPos` 等全局着色器变量有同样信息。VRCCameraSettings 提供 C# 端访问。

---

## Camera Mode

`CameraMode` 属性在 `ScreenCamera` 和 `PhotoCamera` 上可用。

| 值 | 含义 |
|---|---|
| 0 | 正常渲染（VR 双眼、Desktop 单眼） |
| 1 | VR 立体手持相机 |
| 2 | Desktop 单眼手持相机 |
| 3 | 截图模式 |

**典型用法**: 区分手持相机的 VR/Desktop 渲染。

---

## 静态函数

### GetEyePosition / GetEyeRotation

对 **VR 用户**最有用：

```csharp
Vector3 VRCCameraSettings.GetEyePosition(Camera.StereoscopicEye eye);
Quaternion VRCCameraSettings.GetEyeRotation(Camera.StereoscopicEye eye);
```

| 参数 | 值 | 说明 |
|------|---|------|
| `eye` | `Camera.StereoscopicEye.Left` | 左眼 |
| `eye` | `Camera.StereoscopicEye.Right` | 右眼 |

**注意**:
- 对**非 VR 用户**，调用是合法的，但**值等同于** `VRCCameraSettings.ScreenCamera` 的 Pos/Rot
- 推荐用 `StereoEnabled` 检测 VR 用户，**不要假设** `GetEyePosition` 双返回值

### GetCurrentCamera

```csharp
void VRCCameraSettings.GetCurrentCamera(
    out VRCCameraSettings internalComponent,
    out Camera externalComponent
);
```

`Camera.current` 的**安全替代**，因为 `Camera.current` 仅在渲染事件中填充。

| 场景 | `internalComponent` | `externalComponent` |
|------|---------------------|---------------------|
| 已知内部相机渲染中 | `ScreenCamera` / `PhotoCamera` | `null` |
| 用户自定义相机渲染中 | `null` | `UnityEngine.Camera` |
| `Camera.current` 为 null | `null` | `null` |
| Udon 无权访问的相机（如 Avatar 上的相机）| `null` | `null` |

**⚠️ 关键警告**:
- 即使没有 Avatar 相机，**这个函数可能**在渲染事件中**返回双 null**
- 原因：VRChat 内部渲染步骤（如内置菜单）
- **必须**处理 `internalComponent == null && externalComponent == null` 的情况

**典型用法**:
```csharp
public override void OnWillRenderObject()
{
    VRCCameraSettings.GetCurrentCamera(out var internalCam, out var externalCam);
    if (internalCam != null) {
        // 屏幕相机或手持相机渲染中
    } else if (externalCam != null) {
        // 用户自定义相机渲染中
    } else {
        // 不可访问的相机，或内置渲染步骤
        return;
    }
}
```

---

## 事件

### OnVRCCameraSettingsChanged

```csharp
public override void OnVRCCameraSettingsChanged(VRCCameraSettings camera)
{
    // camera 是变化的相机实例
    if (camera != VRCCameraSettings.ScreenCamera) return;
    // 处理分辨率等变化
}
```

**触发场景**:
- 分辨率变化
- 少数其他属性变化

**生命周期提示**:
- `Start()` 中**不会**自动调用
- 需要在 `Start()` 手动调用一次以初始化
- 配合 `OnVRCCameraSettingsChanged` 实现响应式更新

---

## 完整示例：CameraInfoDisplay

```csharp
using TMPro;
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Rendering;

public class CameraInfoDisplay : UdonSharpBehaviour
{
    [SerializeField] private TextMeshProUGUI info;

    void Start()
    {
        // 手动初始化一次（事件不会自动触发 Start）
        OnVRCCameraSettingsChanged(VRCCameraSettings.ScreenCamera);

        Debug.Log($"Started CameraInfoDisplay at resolution of " +
                  $"{VRCCameraSettings.ScreenCamera.PixelWidth}x" +
                  $"{VRCCameraSettings.ScreenCamera.PixelHeight}");
        Debug.Log($"The handheld photo camera is " +
                  $"{(VRCCameraSettings.PhotoCamera.Active ? "enabled" : "disabled")}");
    }

    public override void OnVRCCameraSettingsChanged(VRCCameraSettings camera)
    {
        // 忽略手持相机
        if (camera != VRCCameraSettings.ScreenCamera) return;

        info.text = $"{camera.PixelWidth}x{camera.PixelHeight} " +
                    $"fov={camera.FieldOfView} frame={Time.frameCount}°";
    }
}
```

**注意**:
- `using VRC.SDK3.Rendering;` 必须
- 完整字段列表（`PixelWidth` / `PixelHeight` / `FieldOfView` 等）参考 Unity `Camera` 文档

---

## 与 `_VRChatCameraMode` 全局变量对应

`VRCCameraSettings` 的 C# 端 `CameraMode` 与 Shader 全局变量 `_VRChatCameraMode` **值含义一致**：

| 用途 | C# API | Shader 全局 |
|------|--------|------------|
| 屏幕相机模式 | `VRCCameraSettings.ScreenCamera.CameraMode` | `_VRChatCameraMode` |
| 手持相机模式 | `VRCCameraSettings.PhotoCamera.CameraMode` | `_VRChatCameraMode` |
| 屏幕相机位置 | `VRCCameraSettings.ScreenCamera.transform.position` | `_VRChatScreenCameraPos` |
| 拍照相机位置 | `VRCCameraSettings.PhotoCamera.transform.position` | `_VRChatPhotoCameraPos` |

---

## 性能与陷阱

| 陷阱 | 说明 |
|------|------|
| `OnVRCCameraSettingsChanged` 不会自动触发 | `Start()` 中需手动调用一次 |
| `GetCurrentCamera` 可能返回双 null | 即便在渲染事件中也要处理 |
| `PhotoCamera` 不等于拍照相机 | 始终指向**预览**相机 |
| VR 双眼位置仅在 `StereoEnabled == true` 时有意义 | 非 VR 模式下与 `ScreenCamera` 相同 |

---

## 相关文档

- `memory/world/vrc-graphics.md` - VRCShader / VRCGraphics API + Shader Globals
- `memory/world/vrc-quality-settings.md` - VRCQualitySettings（同一上级页面）
- `memory/world/performance-guide.md` - 渲染性能优化
