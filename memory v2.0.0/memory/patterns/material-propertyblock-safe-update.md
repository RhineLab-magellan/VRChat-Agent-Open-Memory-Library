---
title: Pattern: MaterialPropertyBlock Safe Update（共享材质安全更新）
category: patterns

knowledge_level: applied
status: active

tags:
  - patterns
  - patterns
  - udonsharp

aliases:
  - "MaterialPropertyBlock Safe Update（共享材质安全更新）"
  - "共享材质安全更新"

source: QuickBrown LuraSwitch2(参考工程) — `SwitchBase.cs` (HSV 调整)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# Pattern: MaterialPropertyBlock Safe Update（共享材质安全更新）

> ⚠️ **历史版本标注** — 本 Pattern 基于 LuraSwitch2 v3.00 (2023) 提炼
> 当前 LuraSwitch2 已重写为 v1.06 (2026-03-06, VN3 License)
> Pattern 核心思想(MaterialPropertyBlock Get/Set 配对 + Editor OnValidate 预览)在 Udon 沙箱中仍是通用解法
> 详见 `world/luraswitch2.md` v1.06 工具使用指南

---

## Problem

多个 GameObject 共享同一 Material Asset，运行时修改材质属性会污染 Asset：
- 多个开关共享"亮起时"发光材质
- 运行时改 `material.SetColor()` → 同一 Asset 的所有实例都变
- 编辑器中改 material → 保存场景时**Asset 被永久修改**（污染源文件）
- 想区分"运行时实例级修改" vs "Editor 全局修改"

## Context

- 多对象共享"激活态"颜色
- 玩家个性化颜色（仅本机可见）
- 动态光照效果（按距离衰减）
- 任何"运行时改材质但不影响其他对象"的需求

## Solution: MaterialPropertyBlock

```csharp
private Renderer _renderer;
private MaterialPropertyBlock _mpb;

private void Start() {
    _mpb = new MaterialPropertyBlock();
}

private void SetActivationColor(Color color) {
    _renderer.GetPropertyBlock(_mpb);
    _mpb.SetColor("_EmissionColor", color);
    _renderer.SetPropertyBlock(_mpb);
}
```

## 4 种修改材质的方式对比

| 方式 | 性能 | 污染 Asset | 适用 |
|------|------|----------|------|
| `sharedMaterial.SetColor(...)` | ⚠️ 最快 | ✅ **会** | ❌ **永远不要用** |
| `material.SetColor(...)` | 慢(实例化) | ❌ 不会 | 单实例唯一材质 |
| `MaterialPropertyBlock` | 快 | ❌ 不会 | ✅ **推荐** |
| `MaterialPropertyBlock` + Editor | 快 | ❌ 不会 | ✅ **推荐** |

**`material` vs `MaterialPropertyBlock`**:
- `material` 属性访问时**自动 instantiate**（生成新实例），是 Renderer 私有的
- `MaterialPropertyBlock` 不创建新材质，覆盖在 GPU 端 per-Renderer
- MPB 性能略好（无新实例），但需要 Shader 支持 MPB 属性

## Implementation Sketch: 完整的颜色管理

```csharp
public class ColorManagedSwitch : UdonSharpBehaviour {
    [SerializeField] private Renderer _renderer;
    [SerializeField] private string _emissionPropertyName = "_EmissionColor";
    [SerializeField] private string _baseColorPropertyName = "_BaseColor";
    [SerializeField] private bool _isOn = false;

    private MaterialPropertyBlock _mpb;
    private Color _offEmission = Color.black;
    private Color _onEmission = Color.cyan;
    private Color _offBaseColor = new Color(0.5f, 0.5f, 0.5f);
    private Color _onBaseColor = Color.white;

    private void Start() {
        _mpb = new MaterialPropertyBlock();
        ApplyState();  // 初始化外观
    }

    public void SetOn(bool isOn) {
        _isOn = isOn;
        ApplyState();
    }

    private void ApplyState() {
        if (_renderer == null) return;
        _renderer.GetPropertyBlock(_mpb);
        _mpb.SetColor(_emissionPropertyName, _isOn ? _onEmission : _offEmission);
        _mpb.SetColor(_baseColorPropertyName, _isOn ? _onBaseColor : _offBaseColor);
        _renderer.SetPropertyBlock(_mpb);
    }
}
```

### Editor 预览(OnValidate)

```csharp
#if UNITY_EDITOR
private void OnValidate() {
    if (Application.isPlaying) return;  // 运行时让 Start 处理
    if (_renderer == null) {
        _renderer = GetComponent<Renderer>();
    }
    if (_mpb == null) {
        _mpb = new MaterialPropertyBlock();
    }
    ApplyState();  // Editor 中立即看到反馈
}
#endif
```

**关键**:
- Editor 中调 `OnValidate`（Inspector 改值时触发）
- 用 `Application.isPlaying` 区分路径
- Editor 中也用 MPB（不污染 Asset）

## Networking Model

**材质修改本身不参与网络同步**——它表示对象状态。

| 维度 | 决策 |
|------|------|
| 同步状态 | 对象的"激活态"(`[UdonSynced] bool _isOn`) |
| 材质更新 | OnDeserialization 中本地应用（无网络） |
| 远端表现 | OnDeserialization → SetOn → ApplyState（MPB） |

## Key Design Points

### 1. 为什么不能用 `sharedMaterial`

```csharp
// ❌ 致命错误:污染 Asset
_renderer.sharedMaterial.SetColor("_EmissionColor", color);
// 影响所有用同一 Asset 的 Renderer

// ❌ 也不推荐:每次访问实例化新材质,内存浪费
_renderer.material.SetColor("_EmissionColor", color);
// 虽然不会污染,但每次访问 material 属性都 new Material()

// ✅ 正确:用 MPB
_renderer.GetPropertyBlock(_mpb);
_mpb.SetColor("_EmissionColor", color);
_renderer.SetPropertyBlock(_mpb);
```

### 2. MPB 的 Get/Set 配对

```csharp
_renderer.GetPropertyBlock(_mpb);  // 读取当前 MPB
_mpb.SetColor(...);                 // 修改
_renderer.SetPropertyBlock(_mpb);  // 写回
```

**为什么 Get**:Renderer 已有其他属性的 MPB,Get 是为了保留它们。

**何时跳过 Get**:首次设置所有属性时,可直接 `new` 一个新 MPB(但会覆盖其他属性)。

### 3. Shader 必须支持 MPB 属性

**Shader 中属性必须**用 `[PerRendererData]` 或在 Shader Graph 中启用"Hybrid Instanced" / "Per Renderer"：

```hlsl
// Standard URP shader:
Properties {
    _BaseColor ("Base Color", Color) = (1,1,1,1)
    // ...
}
```

**Shader 中无需修改**,但**Shader 编译选项**中要勾选"Enable GPU Instancing"（或"HYBRID_INSTANCED"）。

### 4. Editor 实时预览

```csharp
#if UNITY_EDITOR
private void OnValidate() {
    if (Application.isPlaying) return;
    if (_renderer == null) _renderer = GetComponent<Renderer>();
    if (_mpb == null) _mpb = new MaterialPropertyBlock();
    ApplyState();
}
#endif
```

**用途**:Creator 在 Inspector 改颜色值时,Scene 视图立即看到效果。
**关键**:`#if UNITY_EDITOR` 包裹,Build 中不包含(节省字节)。

## When To Use

✅ **适合**:
- 多个对象共享同一 Material Asset
- 需要运行时改颜色/参数
- Editor 实时预览
- 性能敏感（每帧调材质）

❌ **不适合**:
- 单实例唯一材质（直接用 `material` 即可）
- 改变 Texture/Shader 切换（MPB 改不了）
- 需要材质实例持久化（MPB 是临时的）

## When Not To Use

- 修改 Material 的 Shader（必须创建新实例）
- 修改 MeshRenderer 的 Material 列表（MPB 不影响 Material Slot 分配）
- 跨 Renderer 共享的全局参数（用 VRCShader.SetGlobal）

## Performance

| 方式 | CPU 成本 | GC 分配 | GPU |
|------|----------|--------|-----|
| `sharedMaterial.SetColor` | 1 extern | 0 | 直接写 |
| `material.SetColor` | 1 extern + 1 instantiate | **0.5-1 KB** | 直接写 |
| `MaterialPropertyBlock` | 3 extern (Get/Set/Set) | 0 | GPU 端 per-Renderer |

**MPB 适合每帧调**（如 60fps 的颜色动画）,`material` 只适合偶尔调（启动时一次性）。

## Common Pitfalls

| 坑 | 后果 | 修复 |
|---|---|---|
| `sharedMaterial.SetColor` | 污染 Asset,多人协作出问题 | 改用 MPB |
| 首次设置时未 `GetPropertyBlock` | 覆盖其他属性 | Get + 修改 + Set |
| Shader 未启用 Instancing | MPB 失效 | Shader 选项勾选 |
| `#if UNITY_EDITOR` 漏掉 | Build 中也调 OnValidate,异常 | 加条件编译 |
| 反射访问私有 material 字段 | 同 sharedMaterial,污染 | 改用 MPB |

## Cross-Reference

- `editor-preview-component.md` - Editor 预览的姊妹模式
- `manual-sync-state.md` - 材质状态由 synced bool 驱动

## Reference Implementation

`C:\CherryStudio\Agent\UdonSharpAgent\参考工程\QuickBrown\LuraSwitch2\02_CORE\01_Switch\SCRIPT\SwitchBase.cs` (1795 行,HSV 颜色调整部分)
