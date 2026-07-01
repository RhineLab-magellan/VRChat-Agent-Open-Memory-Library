---
title: "VRC Avatar Pedestal"
category: world
subcategory: scene-components
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udonsharp
  - avatar
aliases:
  - "VRC Avatar Pedestal"
  - vrc-avatarpedestal
related:
  - vrc-scenedescriptor.md
  - "../sdk-prefabs.md"
  - textmeshpro.md
  - vrc-cameradolly.md
  - vrc-enablepersistence.md
---
# VRC Avatar Pedestal

> Avatar 展示与切换展位
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_avatarpedestal/
> 官方类名: `VRC_AvatarPedestal`

---

## 概述

`VRC_AvatarPedestal` 用于在 World 中展示 Avatar,玩家可以与展位互动并切换到该 Avatar。

> **FACT** (来自官方文档): SDK 中提供了名为 `AvatarPedestal` 的示例 Prefab,演示了用户与展位交互时如何调用 `SetAvatarUse` 方法。

---

## Inspector 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **Blueprint Id** | String | ✅ | 要展示的 Avatar 的 Blueprint ID |
| **Placement** (可选) | Transform | ❌ | 放置 Avatar 的 Transform 位置 |
| **Change Avatar On Use** | Bool | ✅ | 是否在玩家 Interact 时切换为该 Avatar |
| **Scale** | Float | ✅ | Avatar 显示缩放(只影响 Pedestal 上的 Avatar) |

---

## Avatar 所有权行为

> **FACT** (来自官方文档,验证于 2025-08-01): Avatar Pedestal 的行为根据 Avatar 是 Public / Private / Marketplace 有所不同:

| Avatar 类型 | 行为 |
|------------|------|
| **Public Avatar** | 所有用户都能看到并使用 Pedestal |
| **Private Avatar** | 只有上传者(作者)能看到并使用 Pedestal,其他用户看到错误提示 |
| **Marketplace Avatar** | 所有用户都能看到并使用 Pedestal;若用户未持有该 Avatar,则看到 Avatar 详情页 |

> ⚠️ **重要**: Private Avatar Pedestal 对其他用户**完全不渲染**(显示错误或空白),用于创作者展示尚未公开的 Avatar。

---

## U# 引用方式

### 获取 Pedestal 引用

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.SDK3.Components;

public class PedestalController : UdonSharpBehaviour
{
    [SerializeField] private VRC_AvatarPedestal pedestal;
    
    public override void Interact()
    {
        // 切换本地玩家为 Pedestal 上的 Avatar
        pedestal.SetAvatarUse();
    }
}
```

### 动态切换 Blueprint

Blueprint ID 可以在运行时通过 `SetBlueprintId` 切换(假设有暴露的方法):

```csharp
// 方式 1: 预填多个 Pedestal,根据状态显示/隐藏
[SerializeField] private VRC_AvatarPedestal[] pedestals;

public void ShowAvatarAt(int index)
{
    for (int i = 0; i < pedestals.Length; i++)
    {
        pedestals[i].gameObject.SetActive(i == index);
    }
}
```

---

## 典型应用场景

### 1. Avatar 展示厅

玩家进入 World 后看到多个 Pedestal 展示不同 Avatar,Interacting 后切换为该 Avatar。

### 2. 试穿 Avatar 商店

Pedestal 配合 UI 面板展示 Marketplace Avatar,玩家点击后预览并跳转购买页(若未持有)。

### 3. 多 Avatar 角色扮演

每个 NPC 对应一个 Pedestal,玩家选择坐到哪个 Pedestal 上(配合 VRCStation)成为该角色。

### 4. Avatar 投票/评选

Pedestal 配合投票 UI,玩家在多个 Pedestal 中选择喜欢的 Avatar。

---

## 性能考虑

- **每个 Pedestal = 1 个 Avatar 实例**: 大量 Pedestal 会显著增加场景复杂度
- **Mesh / Material 共享**: Pedestal 复用相同 Avatar 时,Unity 会自动批处理
- **Blueprint 加载**: 切换 Blueprint 时会触发 Avatar 加载,首次有 1-3 秒延迟
- **Quest 限制**: 单个 Pedestal 资源压力可控,3-5 个以上需注意性能

---

## 与其他组件的依赖

| 关联组件 | 关系 |
|----------|------|
| **VRCStation** | 可与 Station 配合,坐到 Pedestal 上成为该 Avatar |
| **VRC_SceneDescriptor** | 无直接依赖,但 Pedestal 上 Avatar 的动画可能用到 Reference Camera |
| **UI 面板** | 配合 UI 触发 SetAvatarUse,实现远程切换 |
| **Pickup** | 玩家拾起物体时显示 Pedestal(慎用,语义混乱) |

---

## 最佳实践

1. **总是提供 Placement Transform**: 不要让 Avatar 出现在 Pedestal 默认位置,自行控制缩放和位置
2. **Scale 测试**: Quest 上 Avatar 缩放可能与 PC 不同,需双平台测试
3. **错误处理**: Private Avatar 对其他用户无效,需有视觉反馈(避免空白)
4. **同步状态**: Pedestal 的显示/隐藏应在 Master 端控制,Non-Master 端只读
5. **避免频繁切换**: 频繁切换 Pedestal 内的 Avatar 会造成网络抖动

---

## 常见陷阱

1. **Blueprint ID 错误**: 必须使用完整的 `avtr_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` 格式
2. **Placement 留空**: Avatar 出现在 (0,0,0) 位置,需明确指定
3. **Change Avatar On Use 误用**: 关闭后玩家点击 Pedestal 不会切换 Avatar(但仍显示)
4. **Private Avatar 误用**: 设置为 Private 后只有作者自己能看到,排查时容易忽略
5. **Quest Avatar 不兼容**: 某些 PC Avatar 在 Quest 上不显示或显示异常

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_avatarpedestal/
- 关联 API: [VRC_SceneDescriptor](./vrc-scenedescriptor.md)
- Avatar 域: [../../../memory/avatar/](../../../memory/avatar/)
- SDK Prefabs: [../sdk-prefabs.md](../sdk-prefabs.md)
