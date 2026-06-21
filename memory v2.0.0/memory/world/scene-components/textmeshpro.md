---
title: TextMesh Pro (TMP)
category: world
subcategory: scene-components

knowledge_level: applied
status: active

tags:
  - world
  - udonsharp
  - reference

aliases:
  - "TextMesh Pro (TMP)"

related:
  - ../whitelisted-world-components.md
  - world/data-containers.md
  - api/ui.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# TextMesh Pro (TMP)

> 高质量 2D/3D 文本显示组件
>
> 来源: https://creators.vrchat.com/worlds/components/textmeshpro/
> 官方类名: `TextMeshProUGUI`, `TextMeshPro` (基础类 `TMP_Text`)
> 最后更新: 2026-06-15

---

## 概述

[TextMesh Pro](https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/manual/index.html) 是 Unity 中用于显示高质量 2D 和 3D 文本的工具,被 VRChat Worlds 全面采用。

**Udon 暴露的 TMP 组件** (来自白名单):
- `TMP_Text` (TextMeshProUGUI 和 TextMeshPro 的基类)
- `TMP_Dropdown`
- `TMP_InputField`

其他 TMP 组件(来自 [Allowlisted World Components](../whitelisted-world-components.md))可在场景中使用,但 **不能从 Udon 访问**。

> ⚠️ **FACT**: 避免使用 Unity 内置的 [Text 组件](https://docs.unity3d.com/2018.1/Documentation/ScriptReference/UI.Text.html),因为:
> - 内置 Text 会有锯齿
> - 字符上限 16,250
> - TextMesh Pro 提供更好的渲染、[富文本](http://digitalnativestudios.com/textmeshpro/docs/rich-text/)支持,无字符限制

---

## 安装

TMP 包已包含在 Unity Editor 中。**首次使用**时,Unity 会提示导入必备资源:

1. 创建任何 TMP 组件会触发此提示
2. 也可以手动选择 `Window` > `TextMeshPro` > `Import TMP Essential Resources`

---

## 字体导入

### 默认字体

TextMesh Pro 包含一个名为 `LiberationSans SDF` 的默认字体资产,可立即开始使用。

### 自定义字体

通过 [Font Asset Creator](https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/manual/FontAssetsCreator.html) 导入自己的字体,生成的字体资产可在 TMP 组件中使用。

> 💡 **优化提示**:
> - 字体资产会增加 World 的下载大小和 RAM 占用
> - 降低 Atlas 分辨率
> - 仅导入需要的字符
> - **不要**导入整个 Unicode 范围(常用字符远少于全部)

### VRChat 内置 Fallback 字体

当导入自定义字体时,通常不会包含每个 Unicode 字符。如果 World 包含不在字体资产中的字符串或用户名,TMP 将无法渲染,显示为 "□□□"。

**使用 VRChat Fallback 字体**:
1. 打开 `Project Settings` > `TextMeshPro settings`
2. **移除** 所有的 "Fallback Font Assets"

> **FACT**: 配置正确后,Unity 编辑器中显示为方块的字符,上传到 VRChat 后将正确渲染。

---

## U# 引用方式

### TMP_Text 基础属性

```csharp
using TMPro;
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class TMPSample : UdonSharpBehaviour
{
    [SerializeField] private TMP_Text tmpText;
    [SerializeField] private TextMeshProUGUI uiText;
    [SerializeField] private TextMeshPro worldText;
    
    public override void Interact()
    {
        // 设置文本
        tmpText.text = "Hello VRChat!";
        
        // 修改样式
        tmpText.color = Color.red;
        tmpText.fontSize = 24f;
        
        // 对齐
        tmpText.alignment = TextAlignmentOptions.Center;
        
        // 富文本
        tmpText.richText = true;
        tmpText.text = "<color=red>Red</color> and <b>Bold</b>";
    }
}
```

### TMP_Text 主要属性表

| 属性 | 类型 | 说明 |
|------|------|------|
| `text` | `String` | 访问文本内容 |
| `isRightToLeftText` | `Bool` | 右到左显示(多语言) |
| `fontMaterial` | `Material` | 字体材质(访问会克隆) |
| `fontSharedMaterial` | `Material` | 共享字体材质(FontAsset 为 null 时返回 null) |
| `color` | `Color` | 文本颜色 |
| `alpha` | `Float` | 文本不透明度 |
| `fontSize` | `Float` | 字体大小 |
| `enableAutoSizing` | `Bool` | 自动调整大小 |
| `fontSizeMin` / `fontSizeMax` | `Float` | 自动大小最小/最大值 |
| `horizontalAlignment` | `HorizontalAlignmentOptions` | 水平对齐 |
| `verticalAlignment` | `VerticalAlignmentOptions` | 垂直对齐 |
| `alignment` | `TextAlignmentOptions` | 总体对齐 |
| `characterSpacing` | `Float` | 字符间距 |
| `wordSpacing` | `Float` | 单词间距 |
| `lineSpacing` | `Float` | 行间距 |
| `paragraphSpacing` | `Float` | 段落间距 |
| `characterWidthAdjustment` | `Float` | 字符重叠 |
| `enableWordWrapping` | `Bool` | 自动换行 |
| `overflowMode` | `TextOverflowModes` | 溢出处理(Truncate / Overflow / Ellipsis / Linked / Mask / Page) |
| `richText` | `Bool` | 富文本启用 |
| `maxVisibleCharacters` | `Int` | 可见字符数(打字机效果) |
| `maxVisibleWords` | `Int` | 可见单词数 |
| `maxVisibleLines` | `Int` | 可见行数 |
| `enable` | `bool` | 启用/禁用组件 |

---

## Canvas Render Mode

`TextMeshProUGUI` 必须配合 Canvas 使用。Canvas Render Mode 选择:

| Render Mode | 用途 |
|-------------|------|
| **World Space** | 将文本放置在世界中的任意位置(3D 文字招牌) |
| **Screen Space - Overlay** | 直接显示在用户屏幕上(HUD 元素) |
| **Screen Space - Camera** | 由 Camera 渲染,支持透视 |

### 性能影响

- TMP 文本一次性 batching,适合大量文本同时显示
- 频繁修改 `text` 会触发网格重建,谨慎使用
- 打字机效果:用 `maxVisibleCharacters` 替代 `text = "..."` 累加

---

## 本地化建议

### 方案 1: 简单字符串替换

```csharp
[SerializeField] private TMP_Text label;

public void SetLocalizedText(string languageCode)
{
    switch (languageCode)
    {
        case "zh-CN": label.text = "你好"; break;
        case "ja-JP": label.text = "こんにちは"; break;
        case "en-US": label.text = "Hello"; break;
    }
}
```

### 方案 2: StringVariables (推荐)

VRChat 自带 [StringVariables 资产系统](../../world/data-containers.md#string-variables),可通过 SDK 工具配置多语言字符串,运行时直接读取。

### 方案 3: TMP 富文本 + 内嵌多语言

```csharp
tmpText.richText = true;
tmpText.text = $"Player: <color=#FFD700>{playerName}</color>";
```

---

## 与其他组件的依赖

- **无强依赖**: TMP 是独立 UI 系统
- **常与 UI 交互组合**: [VRC_UIShape](../../api/ui.md) + TMP InputField
- **可与 Pickup 组合**: 玩家拿起物体时更新其标签文本
- **可与 VRC_AvatarPedestal 组合**: 展示 Avatar 名称

---

## 常见陷阱

1. **不在 Editor 中显示 Fallback 字符**: 这是预期行为,上传到 VRChat 后才生效
2. **Atlas 分辨率过高**: 导致内存和下载大小膨胀,建议 1024x1024 或更低
3. **频繁 text 赋值**: 触发网格重建,影响性能,使用 `maxVisibleCharacters`
4. **未导入 TMP Essential Resources**: 新建项目后忘记导入,所有 TMP 组件显示异常
5. **中文字符无法显示**: 字体资产未包含中文字符,要么导入大字体(慎用),要么使用 VRChat Fallback 字体

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/textmeshpro/
- TMP 子页面:
  - [TMP Text](./textmeshpro/tmp_text.md) (基础)
  - TMP Dropdown (后续任务)
  - TMP InputField (后续任务)
- TextMeshPro Unity 文档: https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/manual/
- API 文档: https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/api/TMPro.html
