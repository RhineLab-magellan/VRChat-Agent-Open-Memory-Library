---
title: "Items in Udon Worlds"
category: world
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - mirror
  - udonsharp
aliases:
  - "Items in Udon Worlds"
  - items
related:
  - creator-economy.md
  - layers.md
  - luraswitch2.md
  - sdk-prefabs.md
  - supported-assets.md
---
# Items in Udon Worlds

> 来源: VRChat 官方文档 (https://creators.vrchat.com/worlds/items/)
> 源 URL Last Updated: **Jun 12, 2025**
> 抓取日期: 2026-06-15
> 置信度: High
> Domain: World → Items / Layer / Physics

---

## Domain

**World → Udon / Layer / Physics** — 用户在世界中生成 Item 的机制及其与 Udon 脚本的交互约束。

## Subdomain

- Udon Physics 操作（Raycast/Overlap/Sweep）
- Unity Layer 约定
- 镜像渲染 (VRCMirror)
- World 配置（VRChat Website）

## Conclusion

Items 是 VRChat 提供的一项新特性，允许用户在世界中生成工具、玩具、装置。**Items 在 "Item" Layer (Layer 3) 上生成**，Udon 程序**无法引用 Items**——脚本中遇到 Item 会得到 `null` 引用并可能抛出异常导致自身被禁用。**Items 默认在所有世界中启用**，World 作者可通过 VRChat 网站禁用。

---

## FACT — 知识库已有事实

### 核心概念

- **Items** = 用户在世界中的可生成工具、玩具、装置
- **来源**: `creators.vrchat.com/worlds/items`
- **状态**: 新特性，可能对部分世界产生非预期影响
- **默认行为**: Items 默认在所有世界启用
- **Layer 名称变更**: 历史名称为 `reserved3`，新名称为 `Item`（Layer 3）

### 关键限制（来自原文）

> "Udon programs in your world cannot reference items. If one of your scripts finds an item, it appears as a `null` object. If an UdonBehaviour tries to process an item, it throws an exception and disables itself, so it's best to avoid items."

**推论**:
1. Items 在 Udon 中表现为 `null` GameObject
2. 任何引用 Item 的 Udon 行为会**抛出异常并自动禁用**
3. 这是 Udon VM 的一种**主动保护机制**——避免 Item 触发世界逻辑错误

---

## Evidence — 原文要点

### 1. 禁用 Items（在 World 中）

**操作路径**:
1. 访问 [My Worlds](https://vrchat.com/home/content/worlds) 页面
2. 点击世界缩略图打开 "Edit" 页面
3. 在 "Default Content Settings" 列表中找到 **"Items Enabled"**
4. 按按钮禁用，并在文本框说明原因
5. 滚到顶部按 "Save"

**页面图示**:
- `items-worldinfo-enabled-d92f257b420ff3a7a8030e778c24265e.png` — Items Enabled 状态
- `items-worldinfo-disabled-fc52b68e3555f677187f63249fc60416.png` — Items Disabled 状态

### 2. 在 World Mirrors 中显示 Items

> "Items spawn on the 'Item' layer, which used to be named 'reserved3' in old SDK versions."

**机制**:
- Items 始终生成在 **Layer 3 (`Item`)** 上
- 最新版 `VRCMirror` prefab 已正确配置 Item Layer
- 老 SDK / 旧 mirror / 自定义 Reflect Layers → **不会反射 Items**

**修复方法**:
- VRCMirror → Reflect Layers 下拉菜单 → 勾选 "Item" Layer
- 老 SDK 中选择 "reserved3" 同样有效

**页面图示**:
- `items-mirror-ignore-9cb52aef4a252d4acea7f59b95b8b67f.png` — 镜像不反射 Item
- `items-enable-mirror-layer-a4e50c43a78e87360460d4636199238d.png` — 启用 Item 反射

### 3. 避免 Physics 方法命中 Items

**两条核心建议**（原文）:

> 1. Use a [LayerMask](https://docs.unity3d.com/ScriptReference/LayerMask.html) when possible, and avoid the "Item" layer (previously "reserved3").
> 2. Call `Utilities.IsValid` on any object passed back through a Physics call and look for a `true` result to ensure you don't operate further on a "protected" object.

**适用 Physics 方法**: 详见 `memory/world/layers.md` → "Physics and Layers" 章节。

---

## Analysis — 与现有知识库交叉引用

| 现有知识 | 关联 |
|---|---|
| `memory/world/layers.md` | Layer 3 (`Item`) 定义、Physics 方法清单、LayerMask 用法 |
| `memory/api/udon-type-exposure.md` | `Utilities.IsValid` API（Udon 暴露的 Unity Object 验证方法） |
| `memory/rules/networking-rules.md` | Owner Authority、Manual Sync、连续同步模式 |
| `memory/api/pickups.md` | Pickup 系统（与 Item 不同的概念，Pickup 是 World 自带的对象） |

### Pickup vs Item 概念区分

| 维度 | Pickup | Item |
|---|---|---|
| 位置 | Layer 13 (`Pickup`) | Layer 3 (`Item`) |
| 创建者 | World 作者在场景中放置 | 用户在世界中生成 |
| Udon 引用 | ✅ 正常引用 | ❌ 始终为 `null` |
| 异常风险 | 无 | 命中后 UdonBehaviour 自禁用 |
| 同步 | 通过 Pickup 组件本身 | 由 VRChat 客户端管理 |

---

## Inference 【推断】

【推断 1】**Items 的同步由 VRChat 客户端管理**——文档未明确说明 Items 是否占用网络同步带宽，但从 "Udon cannot reference items" 推断 Items 状态对 Udon 完全透明，避免了 World 作者误用导致网络异常。

【推断 2】**禁用 Items 是 World 级别的"清场"机制**——通过 VRChat Website 设置（而非 World 内部脚本）控制，意味着 Items 启用状态保存在 VRChat 服务器端的 World 元数据中，每个 World 实例共享。

【推断 3】**Layer 3 之前叫 `reserved3`**——可能表明在某个 SDK 版本中 Items 功能就已存在但未公开，2024-2025 年正式开放并重命名为 `Item`。

---

## Risks

| 风险 | 严重度 | 说明 |
|---|---|---|
| **UdonBehaviour 自禁用** | 🔴 高 | 任何 Physics 方法命中 Item 会抛异常并禁用整个 UdonBehaviour，可能导致世界关键逻辑失效 |
| **镜像是老版本** | 🟡 中 | 旧版 VRCMirror prefab 不反射 Items，导致玩家在镜中看不到自己手持的 Item |
| **新功能稳定性** | 🟡 中 | 文档明确说 "may have unintended effects on some world"，建议重要 World 暂禁用 |
| **无 Layer 保护** | 🟢 低 | 用 LayerMask 排除 Item Layer 是基本防御，但未强制 |

---

## Unknowns & Open Questions

| 编号 | 问题 |
|---|---|
| U-1 | Items 同步是否占用 World 同步带宽？是否影响 `~11 KB/s` 总带宽限制？ |
| U-2 | 每个玩家最多可生成多少个 Item？是否有上限？ |
| U-3 | Items 在 World 卸载/实例关闭后是否清理？ |
| U-4 | "Items Enabled" 设置是否需要 World 重新发布？ |
| U-5 | 是否存在 World 内部脚本判断 "Items 是否启用" 的 API？ |

---

## Recommendations

### 设计阶段

1. **永远使用 LayerMask 排除 Item Layer**——Physics 方法默认应明确指定 layer mask
2. **Physics 返回结果必须 `Utilities.IsValid` 校验**——任何 null 引用前先验证
3. **新 World 默认禁用 Items**——除非明确设计为 Item 友好

### 实现阶段

```csharp
// 安全的 Physics.Raycast 模式
public GameObject RaycastSafe(Vector3 origin, Vector3 direction, float maxDistance)
{
    int layerMask = LayerMask.GetMask("Default", "Environment", "Pickup", "Interactive");
    // 注意: 故意排除 "Item", "Player", "PlayerLocal", "MirrorReflection" 等
    
    RaycastHit hit;
    if (Physics.Raycast(origin, direction, out hit, maxDistance, layerMask))
    {
        if (Utilities.IsValid(hit.gameObject))  // 防御 null/Item
        {
            return hit.gameObject;
        }
    }
    return null;
}
```

### 发布阶段

1. 重要 World 在 **VRChat Website → Edit → Default Content Settings** 主动禁用 Items
2. 在 mirror 使用最新 VRCMirror prefab
3. 写明 "Items Disabled" 原因（如果是为了兼容性）

---

## 引用

- **源页面**: https://creators.vrchat.com/worlds/items/
- **相关页面**: https://creators.vrchat.com/worlds/layers/ (Layer 3 Item, Physics 方法清单)
- **相关页面**: https://creators.vrchat.com/worlds/sdk-prefabs/#vrcmirror (VRCMirror prefab)
- **VRChat Website**: https://vrchat.com/home/content/worlds (World 编辑)
