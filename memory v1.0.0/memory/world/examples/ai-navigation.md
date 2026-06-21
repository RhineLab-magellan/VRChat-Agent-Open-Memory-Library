# AI Navigation Example

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/ai-navigation)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/ai-navigation
> 文档版本: Last updated Nov 5, 2024
> SDK: 3.7.2+ (Unity AI Navigation Package)

## Example Central Package

> ✅ **需要 Example Central Package**
> 通过 `VRChat SDK → 🏠 Example Central` 导入
> 包含完整 NavMesh 场景、NPC Prefab、Course Prefab

### Example World
- **World ID**: `wrld_b7b99484-d92f-403d-ac10-4da7e5a9ce14`
- **URL**: https://vrchat.com/home/world/wrld_b7b99484-d92f-403d-ac10-4da7e5a9ce14

---

## 概述

演示 Udon 配合 Unity **AI Navigation Package** 实现:
- 运行时 NavMesh 重建
- NPC 寻路
- 多人同步的进度追踪

**典型场景**: 一群 NPC 试图从红方块到达绿方块,玩家可以移动蓝色方块作为路径,NPC 自动重新计算路径。

---

## 关键 Udon API 与组件

| 组件/API | 角色 | 说明 |
|----------|------|------|
| `NavMeshAgent` | 寻路执行者 | 提供基础导航与移动 |
| `NavMeshSurface` | 寻路网络 | 允许运行时 `BuildNavMesh` |
| `NavMeshModifier` | 路径修改 | 将方块表面加入主 NavMesh |
| `VRCObjectSync` | 位置同步 | 自动同步 NPC 位置给其他玩家 |
| `SendCustomNetworkEvent` | 进度广播 | 通知所有人 `Win` 事件 |

---

## 场景结构

```
World
├── (SceneDescriptor, floor, lighting)
└── Course
    ├── NavMeshSurface (runtime rebuild)
    ├── CourseManager (UdonBehaviour - 进度条/重置)
    ├── NPC Start (Transform)
    ├── NPC Finish (Transform)
    └── NPC Step × 3
        ├── NavMeshModifier
        ├── VRCPickup
        └── UdonBehaviour (锁旋转 + BuildNavMesh)
└── NPCs
    └── NPC × 4
        ├── Capsule Mesh
        ├── NavMeshAgent
        └── UdonBehaviour (自定义逻辑)
└── Canvas
    ├── Progress Indicator
    └── Reset Button
```

---

## 核心逻辑

### 启动流程
1. 场景初始化: 每个 NPC 的 `destination` = "NPC Finish" 方块
2. 直接无通路,NPC 失败
3. 玩家拾取 `NPC Step` 放下,触发 `NavMeshSurface.BuildNavMesh`
4. 如果路径改善,所有 Agent 跳上方块继续前进

### 进度检测
- **频率**: 每 0.5 秒
- **方法**: 比较"第一个 NPC 与目标方块的距离"与"初始距离"
- **成功阈值**: 距离 < 0.15 单位,触发粒子效果并停止进度检测
- **网络同步**: `Win` 事件通过 `SendCustomNetworkEvent` 通知所有玩家

---

## Networking 策略 ⭐ 重要设计

### 核心模式: **Manual Sync + Owner Authority**

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class CourseManager : UdonSharpBehaviour
{
    [UdonSynced] private float progress;

    void Update()
    {
        if (Networking.IsOwner(gameObject))
        {
            // Owner 计算 progress,仅在变化时同步
            if (progressChanged)
                RequestSerialization();
        }
        else
        {
            // Non-Owner 监听 progress 变化更新 UI
        }
    }
}
```

### 关键设计原则

| 元素 | 同步策略 | 原因 |
|------|----------|------|
| `progress` 浮点数 | Manual Sync | 仅 Owner 计算,避免重复逻辑 |
| NPC 位置 | VRCObjectSync (Continuous) | 高频位置,自动同步 |
| Win 事件 | NetworkEvent | 一次性广播,低开销 |
| NavMesh 重建 | Owner 端执行 | Non-Owner 不需要重建 |

### 成功阈值 `successThreshold = 0.8`
> 文档明示: 设为 0.8 是为了"补偿其他 NPC 干扰主测 NPC"的情况
> 这是**带容错的同步阈值**经典设计 — 单一权威值,容忍一定抖动

---

## 关键 Insight 总结

| 模式 | 价值 |
|------|------|
| **Owner-Only 寻路** | 避免 20 玩家同时计算 NavMesh 的 CPU 浪费 |
| **VRCObjectSync 替代手动位置同步** | 利用 SDK 内置同步,代码更简洁 |
| **阈值触发 + 容差** | 0.8 而非 1.0,容忍真实世界抖动 |
| **NetworkEvent 一次性广播** | 进度增量 vs 事件广播的清晰分离 |

---

## 二次开发建议(文档原话)

- 改变起点和终点距离
- 减少可用方块数(3→2)增加难度
- 让目标点随时间移动
- 每人一个 NPC 变成"赛跑游戏"

---

## 与知识库互补

- **Udon Animator + Udon API**: `memory/world/animator-system.md`
- **Networking 模式**: `memory/api/networking.md`
- **VRCObjectSync**: `memory/sources/supported-assets.md`(待建)
- **VRC Pickup**: `memory/world/components/pickup.md`(待建)

## 相关 Udon 文档链接

- [AI Navigation 完整指南](/worlds/udon/ai-navigation)
- [Unity NavMeshSurface](https://docs.unity3d.com/Packages/com.unity.ai.navigation@1.1/manual/NavMeshSurface.html)
- [Unity NavMeshAgent](https://docs.unity3d.com/ScriptReference/AI.NavMeshAgent.html)
