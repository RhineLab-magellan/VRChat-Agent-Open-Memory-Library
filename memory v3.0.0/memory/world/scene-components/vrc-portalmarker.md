---
title: "VRC Portal Marker"
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
  - portal
  - udonsharp
aliases:
  - "VRC Portal Marker"
  - vrc-portalmarker
related:
  - vrc-scenedescriptor.md
  - "vrchatsdk/api-instances.md"
  - textmeshpro.md
  - vrc-avatarpedestal.md
  - vrc-cameradolly.md
---
# VRC Portal Marker

> 传送门标记组件
>
> 来源: https://creators.vrchat.com/worlds/components/vrc_portalmarker/
> 官方类名: `VRC_PortalMarker`
> 最后更新: 2026-06-15
> 最新更新日期: 2025-05-14

---

## 概述

`VRC_PortalMarker` 创建指向其他 VRChat 世界的传送门。玩家可以**走入传送门**跳转到其他 World;当用户的 VRChat 菜单打开时,也可以**点击传送门**查看目标 World 的详细信息。

> **FACT** (来自官方文档):
> - **走入触发**: 玩家走入传送门 → 跳转到目标 World
> - **菜单触发**: 打开 VRChat 菜单 → 选中传送门 → 显示目标 World 详情

---

## 使用方法

### 配置 World ID 模式

设置 `World ID` 为具体 World,传送门将导向该 World 的**已存在的 Public Instance**。如果没有 Public Instance,传送门将创建一个新 Instance。

### 配置 World 选项 (None / Home / Hub)

- **None**: 跳转到 `World ID` 指定的 World
- **Home**: 跳转到用户**当前 Home World**(用户个性化设置中的 Home World)
- **Hub**: 跳转到 **VRChat Hub World**(官方中心)

> **FACT**: 选择 `Home` 或 `Hub` 时,`World ID` 字段被忽略。

---

## Inspector 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| **World ID** | String | 目标 World 的 ID,格式如 `wrld_f995a2eb-7ddc-4558-aef1-815c3b23df6c` |
| **Custom Portal Name** | String | 自定义传送门显示名称(覆盖 World 实际名称) |
| **World** | enum (None / Home / Hub) | 选择 World ID / Home / Hub |

---

## World ID 格式

```
wrld_<uuid>
例: wrld_f995a2eb-7ddc-4558-aef1-815c3b23df6c
```

> **FACT**: World ID 来自 VRChat API 的 `worlds` 端点,通常以 `wrld_` 前缀 + UUID 形式表示。

---

## U# 引用方式

### 基础引用

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.SDK3.Components;

public class PortalController : UdonSharpBehaviour
{
    [SerializeField] private VRC_PortalMarker portal;
    
    public override void Interact()
    {
        // 通常玩家走入传送门即可触发
        // 也可在 UI 中通过 SendCustomEvent 手动触发
    }
}
```

### 动态配置 Portal

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class DynamicPortal : UdonSharpBehaviour
{
    [SerializeField] private VRC_PortalMarker portal;
    [SerializeField] private VRCUrl[] worldUrls;  // 不适用,需直接赋值
    
    public void SetTargetWorld(string worldId)
    {
        // 注意:World ID 字段在 Inspector 中是公开 string,
        // 可以通过 SerializedObject 在编辑器中动态修改
        // 运行时修改可能不被 VRChat 支持,需测试
    }
}
```

> ⚠️ **限制**: World ID 字段在 VRChat 客户端可能是 **read-only at runtime**,需要在 Inspector 中预先配置。
> 实际开发中,通常用**预填多个 Portal + 显示/隐藏**的方式实现动态切换。

### 切换显示的 Portal

```csharp
[SerializeField] private VRC_PortalMarker[] portals;

public void ShowPortal(int index)
{
    for (int i = 0; i < portals.Length; i++)
    {
        portals[i].gameObject.SetActive(i == index);
    }
}
```

---

## Portal 行为细节

### Instance Access Type

VRChat 自动根据目标 World 的设置决定访问权限:
- **Public**: 任何用户可加入
- **Friends+**: 仅好友可加入
- **Friends of Friends**: 好友的好友可加入
- **Invite+**: 仅邀请可加入
- **Private**: 仅创建者可加入

> **FACT**: 玩家走入传送门时,如果目标 Instance 不满足用户的访问权限,VRChat 会创建新 Instance。

### 走入触发条件

> **FACT** (来自官方文档,验证于 2025-05-14):
> 1. 玩家走入 Portal Collider 范围
> 2. 短延迟(防误触)
> 3. 显示加载画面
> 4. 跳转到目标 World

### 菜单触发流程

1. 玩家打开 VRChat 菜单
2. 选中 Portal(基于视角)
3. 显示目标 World 详情面板
4. 点击 "Join" → 跳转

---

## 典型应用场景

### 1. World Hub

主 World 包含多个 Portal,每个指向不同的子 World:

```
World Hub
├── Portal 1 → wrld_aaa (Sub World 1)
├── Portal 2 → wrld_bbb (Sub World 2)
└── Portal 3 → wrld_ccc (Sub World 3)
```

### 2. Home World 引导

新手 World 包含一个 Portal,引导用户设置自己的 Home World(Portal 设为 `Home`)。

### 3. VRChat Hub 跳转

主 World 包含一个 Portal 跳转到 VRChat Hub(Portal 设为 `Hub`),方便用户从 Hub 跳回主 World。

### 4. 动态世界选择

UI 面板 + 多个 Portal,玩家选择后显示对应 Portal,走入即跳转。

---

## 性能考虑

- **多个 Portal**: 性能影响小,Portal 本身只是一个触发器
- **触发范围**: 取决于 Collider 大小,通常为 Portal 视觉大小
- **走入检测**: VRChat 客户端处理,无需 U# 代码

---

## 平台兼容性

- **PC**: 完全支持
- **Quest**: 完全支持
- **走动 vs 飞行**: Portal 适用于所有移动方式

---

## 与其他组件的依赖

| 关联组件 | 关系 |
|----------|------|
| **Collider** | 强依赖,必须配置 Trigger Collider |
| **VRC_SceneDescriptor** | 无直接依赖 |
| **UI 面板** | 配合 UI 切换显示的 Portal(用 `SetActive`) |
| **VRC_AvatarPedestal** | 在 Portal 前显示欢迎 Avatar |

---

## 最佳实践

1. **提供视觉提示**: Portal 应有清晰视觉(发光、动画),玩家知道是传送门
2. **配置 Custom Portal Name**: 自定义名称让玩家知道跳转到哪里
3. **避免多个 World 入口重叠**: 多个 Portal 位置应分开,避免误触发
4. **测试走入触发**: 验证 Collider 大小合适,不会误触
5. **使用 None / Home / Hub 选项**: 让玩家可跳到 Hub 或 Home,提升用户体验

---

## 常见陷阱

1. **World ID 错误**: 复制 ID 时漏掉前缀或 UUID 部分
2. **Collider 未配置 Trigger**: 必须勾选 "Is Trigger"
3. **多个 Portal 重叠**: 玩家走入冲突区域,优先级未定义
4. **World 未公开**: 设为 Private 的 World 无法被 Portal 跳转
5. **Custom Portal Name 过长**: 显示不全,需测试

---

## 与 Custom Portal 的区别

| 维度 | VRC_PortalMarker (标准) | 自定义 Portal |
|------|------------------------|--------------|
| **创建方式** | 添加组件 | 自行实现 UI + API 调用 |
| **跳转方式** | VRChat 客户端处理 | 需调用 REST API + 启动 VRChat |
| **可靠性** | 高(官方) | 取决于实现 |
| **复杂度** | 低 | 高 |
| **官方支持** | ✅ | ❌ (违反 ToS) |

> **FACT**: VRChat **不官方支持** 通过 REST API 创建 Instance 并跳转到该 Instance,需要用户在 VRChat 客户端手动操作。
> **合规建议**: 使用 VRC_PortalMarker,不要试图自动化 Portal 跳转。

---

## 引用

- 官方文档: https://creators.vrchat.com/worlds/components/vrc_portalmarker/
- 关联组件: [VRC_SceneDescriptor](./vrc-scenedescriptor.md)
- VRChat SDK (Instance API): [../../vrchatsdk/api-instances.md](../../vrchatsdk/api-instances.md)
- 模式: `patterns/dynamic-portal-marker.md` (后续任务)
