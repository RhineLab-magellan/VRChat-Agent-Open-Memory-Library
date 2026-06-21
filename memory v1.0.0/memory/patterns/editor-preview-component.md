# Pattern: Editor Preview Component（编辑器预览组件）

> Type: PATTERN
> Source: QuickBrown LuraSwitch2(参考工程) — `MirrorAreaPreview.cs`, `Collider_AreaPreview.cs`, `HeightOffsetterPreview.cs`
> Confidence: High
> SDK Version: VRChat SDK 3.x
> Last Verified: 2026-06-20

---

## Problem

Creator 在 Inspector 中调整参数（如 Mirror 范围、Collider 大小、Height Offset 高度）时，希望 Scene 视图实时看到反馈：
- 运行时组件（MonoBehaviour / UdonSharpBehaviour）**不进 Build** 或不提供 Editor 渲染
- 默认 Gizmo 只能画简单线框，无法表达复杂状态
- 想区分"仅 Editor 显示" vs "运行时生效"

## Context

- Mirror 反射区域的可视化
- Collider 体积显示
- Trigger 区域提示
- Height/Position 调整预览
- 任何"Editor 实时反馈 + 运行时可关闭"的需求

## Udon Constraints

- UdonSharpBehaviour 默认不执行 OnDrawGizmos
- `[ExecuteAlways]` 在 Editor 中也执行 Update
- Udon 组件**不能**直接用于 Editor-only 工具（编译限制）

## Solution: 独立 Editor-only 组件

```csharp
[ExecuteAlways]
[AddComponentMenu("LuraSwitch/Editor/Mirror Area Preview")]
public class MirrorAreaPreview : MonoBehaviour {  // 注意:不是 UdonSharpBehaviour
    [SerializeField] private Color _previewColor = new Color(0, 1, 1, 0.3f);

    private TrackingState _state;  // 用于变更检测

    private void OnDrawGizmos() {
        if (!ShouldDraw()) return;

        // 仅在状态变更时重绘(避免每帧 GC)
        if (_state.HasBoxChanged(transform.position, transform.lossyScale)) {
            _state.UpdateFrom(transform);
        }

        Gizmos.color = _previewColor;
        Gizmos.DrawCube(transform.position, transform.lossyScale);
        Gizmos.color = Color.cyan;
        Gizmos.DrawWireCube(transform.position, transform.lossyScale);
    }

    private bool ShouldDraw() {
        // 只在 Editor 模式 + 未运行 + 选中时显示
        return !Application.isPlaying;
    }
}
```

## Implementation Sketch: TrackingState + HasBoxChanged

```csharp
/// <summary>
/// Editor-only 状态追踪,避免每帧重绘
/// </summary>
public struct TrackingState {
    private Vector3 _lastPosition;
    private Vector3 _lastScale;
    private Quaternion _lastRotation;
    private bool _initialized;

    public bool HasBoxChanged(Vector3 pos, Vector3 scale) {
        if (!_initialized) return true;
        return _lastPosition != pos || _lastScale != scale;
    }

    public void UpdateFrom(Transform t) {
        _lastPosition = t.position;
        _lastScale = t.lossyScale;
        _lastRotation = t.rotation;
        _initialized = true;
    }
}
```

### 完整示例：MirrorAreaPreview

```csharp
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif

[ExecuteAlways]
[DisallowMultipleComponent]
public class MirrorAreaPreview : MonoBehaviour {
    [SerializeField] private bool _showOnlyWhenSelected = true;
    [SerializeField] private Color _fillColor = new Color(0, 0.8f, 1f, 0.2f);
    [SerializeField] private Color _wireColor = new Color(0, 0.8f, 1f, 1f);

    private TrackingState _state;

    private void OnEnable() {
#if UNITY_EDITOR
        EditorApplication.delayCall += OnEditorUpdate;
#endif
    }

    private void OnDisable() {
#if UNITY_EDITOR
        EditorApplication.delayCall -= OnEditorUpdate;
#endif
    }

#if UNITY_EDITOR
    private void OnEditorUpdate() {
        SceneView.RepaintAll();
    }
#endif

    private void OnDrawGizmos() {
        if (Application.isPlaying) return;  // 运行时隐藏
        if (_showOnlyWhenSelected && !IsSelected()) return;

        // 变更检测(避免 GC 分配)
        if (_state.HasBoxChanged(transform.position, transform.lossyScale)) {
            _state.UpdateFrom(transform);
        }

        // 绘制
        Gizmos.color = _fillColor;
        Gizmos.DrawCube(transform.position, transform.lossyScale);
        Gizmos.color = _wireColor;
        Gizmos.DrawWireCube(transform.position, transform.lossyScale);
    }

    private bool IsSelected() {
#if UNITY_EDITOR
        return Selection.activeGameObject == gameObject;
#else
        return false;
#endif
    }
}
```

## Networking Model

**Editor Preview 组件不参与网络同步**——它是 Editor-only 工具。

| 维度 | 决策 |
|------|------|
| 同步状态 | 完全不参与 |
| Build 中存在 | ❌ 不会进 Build（用 `[ExecuteAlways]` MonoBehaviour，运行时无行为） |
| 编辑器开销 | 仅 `OnDrawGizmos` 触发,延迟调用 `SceneView.RepaintAll` |

## Key Design Points

### 1. MonoBehaviour 而非 UdonSharpBehaviour

```csharp
// Editor-only 工具用 MonoBehaviour
public class MirrorAreaPreview : MonoBehaviour { ... }

// ❌ 错误:UdonSharpBehaviour 强制序列化到 Udon
public class MirrorAreaPreview : UdonSharpBehaviour { ... }
```

**为什么**:UdonSharpBehaviour 在 Build 中会产生 Udon VM 实例,即便代码为空。MonoBehaviour 不进 Build。

### 2. `[ExecuteAlways]` 属性

```csharp
[ExecuteAlways]
public class Foo : MonoBehaviour {
    void OnDrawGizmos() { ... }  // Editor + Runtime 都调用
    void Update() { ... }         // Editor + Runtime 都调用
}
```

**Editor-only 检查**:
```csharp
private void OnDrawGizmos() {
    if (Application.isPlaying) return;  // 运行时关闭
}
```

### 3. TrackingState 变更检测

**问题**:Gizmo 绘制每帧调用,但**只有状态变化时**才需要重绘。
**解决**:用 struct 记录上次值,`!=` 比较判断变更。

```csharp
if (_state.HasBoxChanged(transform.position, transform.lossyScale)) {
    _state.UpdateFrom(transform);
    // 重绘
}
```

**好处**:
- 避免无效的 Gizmo 调用
- 结构体比较无 GC（值类型）
- 仅在 `transform.position` / `lossyScale` 真改时才重绘

### 4. `EditorApplication.delayCall` 调度

```csharp
private void OnEnable() {
#if UNITY_EDITOR
    EditorApplication.delayCall += OnEditorUpdate;
#endif
}
```

**作用**:Editor 模式下不用 `Update()`,用 `delayCall` 订阅,SceneView 刷新时回调,降低空闲时的 CPU。

### 5. `SceneView.RepaintAll()`

```csharp
private void OnEditorUpdate() {
    SceneView.RepaintAll();
}
```

**作用**:主动请求 Scene 视图重绘(否则 Gizmo 可能不更新)。

## When To Use

✅ **适合**:
- 复杂参数需要可视化(Mirror 范围、Collider 体积、Trigger 区域)
- 多个 Creator 协作时,降低沟通成本
- 教学/演示项目(让用户看到"调整这个值会改变什么")
- Editor 调试(快速定位问题)

❌ **不适合**:
- 简单可视化(默认 Gizmo 够用)
- 性能敏感场景(Editor 工具不应进 Build)
- 运行时需要的功能(应拆为运行时组件)

## When Not To Use

- 状态简单且固定(直接画 Gizmo)
- Creator 不需要 Editor 反馈(纯代码用户)
- 项目已发布(关注运行时性能)

## Editor 工具标准模板

```csharp
#if UNITY_EDITOR
[CustomEditor(typeof(YourBehaviour))]
public class YourBehaviourEditor : Editor {
    public override void OnInspectorGUI() {
        DrawDefaultInspector();
        if (GUILayout.Button("Reset State")) {
            ((YourBehaviour)target).ResetState();
        }
    }
}
#endif
```

**Editor 工具三件套**:
1. **Preview 组件**(`[ExecuteAlways]` MonoBehaviour) - 实时显示
2. **Custom Editor** - Inspector 增强
3. **Undo 支持** - `Undo.RecordObject` / `Undo.postprocessModifications`

## Common Pitfalls

| 坑 | 后果 | 修复 |
|---|---|---|
| 用 UdonSharpBehaviour 作 Preview | 进 Build 时浪费 VM | 用 MonoBehaviour |
| 无 `Application.isPlaying` 守卫 | 运行时也显示 Gizmo | `if (Application.isPlaying) return` |
| `Update()` 中重计算 | Editor 卡顿 | 用 `EditorApplication.delayCall` |
| 直接对比 `transform.position` | 浮点噪声误判 | 用 HasChanged 模式 + epsilon |
| `SceneView.RepaintAll` 每帧调 | Scene 卡顿 | 仅在变更时调 |

## Cross-Reference

- `material-propertyblock-safe-update.md` - Editor 改材质的安全方式
- `multi-vm-rules.md` - Udon 组件不进 Build 的规则

## Reference Implementation

```
C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\02_Mirror\SCRIPT\MirrorAreaPreview.cs
C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\01_Switch\SCRIPT\Collider_AreaPreview.cs
C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\10_HeightOffsetter\SCRIPT\HeightOffsetterPreview.cs
```
