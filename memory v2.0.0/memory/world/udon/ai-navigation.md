---
title: AI Navigation
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - udonsharp

aliases:
  - "AI Navigation"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# AI Navigation

> 来源: https://creators.vrchat.com/worlds/udon/ai-navigation/
> 抓取日期: 2026-06-15
> SDK: 3.7.2+ (Unity AI Navigation Package)
> 状态: ✅ FACT (官方文档)

---

## 概述

**AI Navigation** 允许创建能在世界中智能移动的 **NPC(Non-Player Character)**,使用从场景几何自动生成的 **NavMesh**。

- **动态障碍物**: 运行时修改导航
- **Off-Mesh Links**: 开门、跳台阶等特定动作

> **官方提示**: AI Navigation 是 **Unity 内置功能**。使用前请阅读 [Unity 官方文档](https://docs.unity3d.com/Packages/com.unity.ai.navigation@1.1/manual/index.html) 理解核心概念。

---

## 与 Unity 2019 Navigation 的差异

> **关键变化**: 2022 LTS 中,AI Navigation 改为**独立 Package**,不再集成到 Unity 核心

| 变化点 | 说明 |
|---|---|
| 独立 Package | 由 Unity 维护的独立 Package |
| **运行时 NavMesh 生成** | **在 VRChat 客户端中可运行时创建/更新 NavMesh** (之前只能在 Editor 中) |
| NavMesh Links & Off-Mesh Links | 简化使用 |
| NavMesh 生成 | 整体更鲁棒 |
| 动态障碍物 | 支持 |
| **多 NavMesh Surface** | 世界中可使用**多个 NavMesh Surface** |
| **NavMeshModifier / Modifier Volume** | 提供细粒度控制 |
| Area Costs | 正确导出到世界数据,加入世界时恢复 |

---

## VRChat 中的限制

### 🚫 Custom Agent Types(自定义代理类型)

- **Unity 支持**: Radius / Height / Step Height / Max Slope 等
- **VRChat 限制**: 信息打包到世界数据,**但 VRChat 没有方法检索/应用自定义 agent 类型**
- **现状**: **必须使用 default agent type**
- **计划**: 官方表示"正在考虑",但当前不可用

### 🚫 不支持的方法/属性

| 限制项 | 原因 | 替代方案 |
|---|---|---|
| `NavMeshLink.agentTypeID` | 自定义 agent 的运行时 baking 无效 | **避免使用** |
| `NavMeshSurface.CollectObjects` | **Udon 中 Enum 数组不可用** | 在 Editor 中预设 |
| `NavMeshSurface.agentTypeID` | 同上 | **避免使用** |
| `NavMeshSurface.UpdateNavMesh()` | 返回 `AsyncOperation`(Udon 不可用) | 方法本身**仍可工作**,但忽略返回值 |

---

## 关键 Udon 集成模式

### 模式 1: 运行时 NavMesh 重建

```
玩家拾取/放下方块
  → 触发 NavMeshSurface.BuildNavMesh()
  → NavMeshAgent 自动重新计算路径
```

### 模式 2: Owner 端 NavMesh 计算(关键!)

> **🔴 关键**: NavMesh 计算是 CPU 密集操作,**只应在 Owner 端执行**

```csharp
public class NavigationOwner : UdonSharpBehaviour
{
    [SerializeField] private NavMeshSurface navMeshSurface;

    public void RebuildNavMesh()
    {
        if (!Networking.IsOwner(gameObject)) return;  // 关键:只在 Owner 端
        navMeshSurface.BuildNavMesh();
    }
}
```

### 模式 3: NPC 位置同步

> **推荐**: 使用 `VRCObjectSync` 而非手动同步位置

- VRCObjectSync = Continuous 同步(高频位置自动同步)
- 避免在 Update 中手动 `RequestSerialization()`

### 模式 4: 进度广播

```csharp
// Owner 计算 NPC 进度
if (Networking.IsOwner(gameObject))
{
    float progress = CalculateProgress();
    if (progressReached(progress))
    {
        SendCustomNetworkEvent(NetworkEventTarget.All, nameof(Win));
    }
}

public void Win()
{
    // 所有客户端触发
}
```

---

## 完整示例场景

> 官方提供完整 AI Navigation Example 场景

- **World ID**: `wrld_b7b99484-d92f-403d-ac10-4da7e5a9ce14`
- **URL**: https://vrchat.com/home/world/wrld_b7b99484-d92f-403d-ac10-4da7e5a9ce14
- **导入**: VRChat SDK → 🏠 Example Central
- **内容**: NavMesh 场景、NPC Prefab、Course Prefab

> **详细示例分析**: `memory/world/examples/ai-navigation.md` ⭐ 完整代码 + 网络同步模式

---

## 与 Udon 的 API 集成

### 关键组件

| 组件 | 角色 | Udon 控制方式 |
|---|---|---|
| `NavMeshAgent` | 寻路执行者 | `agent.SetDestination(target.position)` |
| `NavMeshSurface` | 寻路网络 | `surface.BuildNavMesh()`(仅 Owner) |
| `NavMeshModifier` | 路径修改 | 通过 GameObject 父子级自动 |
| `NavMeshModifierVolume` | 区域修改 | 同上 |
| `NavMeshLink` / `OffMeshLink` | 链接 | 静态配置 |

### 关键约束

| 约束 | 影响 |
|---|---|
| **VRChat 仅支持 default agent type** | 不要尝试自定义 |
| **NavMesh 计算只在 Owner 端** | 否则 20 玩家同时计算 = 灾难 |
| **Udon 无 Enum 数组** | `NavMeshSurface.CollectObjects` 等不可用 |
| **`AsyncOperation` 不可用** | 忽略 `UpdateNavMesh()` 返回值 |

---

## 风险与陷阱

| 风险 | 等级 | 说明 |
|---|---|---|
| 所有客户端同时 BuildNavMesh | 🔴 严重 | 强制 Owner Only 检查 |
| 自定义 Agent Type | 🟡 中等 | 当前不可用,会被忽略 |
| `AsyncOperation` 使用 | 🟡 中等 | Udon 中返回 null/无效 |
| 大型 NavMesh 运行时重建 | 🟡 中等 | 卡顿,应分帧或预烘焙 |
| 多 NavMesh Surface 冲突 | 🟢 低 | 注意配置 agentTypeID 一致 |

---

## 与知识库互补

- **完整 AI Navigation 示例**: `memory/world/examples/ai-navigation.md` ⭐ 包含 Manual Sync 模式
- **Networking 模式**: `memory/api/networking.md` ⭐ Manual + Owner Authority
- **VRCObjectSync**: `memory/world/sdk-prefabs.md` ⭐ 自动位置同步
- **VRC Pickup**: `memory/world/whitelisted-world-components.md`
- **NavMesh API 暴露**: `memory/api/udon-type-exposure.md` → Grep "NavMesh"

---

## 相关 VRChat 官方文档

- [AI Navigation 完整指南](/worlds/udon/ai-navigation)
- [Unity NavMeshSurface](https://docs.unity3d.com/Packages/com.unity.ai.navigation@1.1/manual/NavMeshSurface.html)
- [Unity NavMeshAgent](https://docs.unity3d.com/ScriptReference/AI.NavMeshAgent.html)
- [Unity NavMeshLink](https://docs.unity3d.com/Packages/com.unity.ai.navigation@1.1/manual/NavMeshLink.html)
