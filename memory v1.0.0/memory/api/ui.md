# API: UI (VRChat World UI)

> Type: API
> Confidence: Medium
> Source: 社区经验
> Last Updated: 2026-06-04

---

## VRChat World UI

VRChat 使用 Unity UI (Canvas) 作为世界内 UI。UdonSharp 可以操作 Canvas 元素。

### Canvas / UdonBehaviour 通信

UI 元素的交互通常通过以下方式：
1. UI 元素挂载 UdonBehaviour
2. UdonBehaviour 的方法绑定到 Button.onClick 等
3. 或者通过 Interact 触发的物理按钮

### 常用 API (需要验证)

#### Text / TextMeshPro
- `Text.text` 设置
- **暴露**: ✅ (基本文本设置)
- **注意**: TMP 的某些高级功能可能不可用

#### Button
- `Button.onClick` 在编辑器绑定 UdonBehaviour 方法
- **暴露**: ✅ (编辑器绑定，非 runtime AddListener)

#### Slider
- `Slider.value` 读写
- `Slider.onValueChanged` — 需要验证 runtime 绑定是否可用

#### Image
- `Image.sprite`
- `Image.color`
- **暴露**: ✅ (基本属性)

### 网络同步

UI 状态通常不需要直接同步，而是：
1. 同步底层数据（score、state 等）
2. 远端根据 synced variable 本地更新 UI

### 性能注意事项
- Canvas 的 rebuild 在 Udon VM 中可能有额外成本
- 频繁更新 Text 文本可能造成 UI 重绘
- 考虑节流 UI 更新频率（如 2-5 Hz）

## 常见错误
- Runtime AddListener 绑定 UI 事件（Udon 不支持）
- 高频更新 UI Text（如每帧更新计时器文本）
- 尝试同步 UI 状态而非底层数据
