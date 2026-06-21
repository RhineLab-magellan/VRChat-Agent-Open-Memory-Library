---
title: Network ID Utility | VRChat Creation
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - networking
  - udon
  - json

aliases:
  - "Network ID Utility | VRChat Creation"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Network ID Utility | VRChat Creation

> 来源:https://creators.vrchat.com/worlds/udon/networking/network-id-utility/
> SDK 版本:VRChat SDK 3.10.x+ (2025-08-11)
> 分类:Networking 工具 → Editor 工具
> **注意**:本文档描述的是 **Unity Editor 工具**,不打包到 World 中。

---

## 概述

**Network ID** 是 VRChat 在运行时分配给 GameObject 的唯一标识符,用于确定网络同步时 "哪个对象是哪个对象"。

> 大多数情况下你不需要关心它,但在 **跨平台世界**(PC/Quest 各自不同 scene)时会遇到 ID 不一致的问题。

**为什么需要这个工具**:
- 跨平台 World 中,PC 和 Quest 加载的是两个不同 scene
- Network ID 是不同 scene 之间维持同步状态的"链接"
- 如果 ID 错乱,可能出现 "你踢的是沙滩球,别人看到的是冰淇淋"

---

## Network ID Import and Export Utility(网络 ID 导入导出工具)

### 工具位置

```
VRChat SDK / Utilities / Network ID Import and Export Utility
```

### 用途

| 场景 | 说明 |
|------|------|
| **跨平台 World 开发** | PC scene 与 Quest scene 的 Network ID 同步 |
| **跨项目迁移** | 把一个项目的 Network ID 导出,导入到另一个项目 |
| **版本对齐** | 确保两个 scene 的 Network ID 完全一致 |

### 使用流程

```
PC Scene (已分配 Network ID)
  ↓ Export
  network_ids.json
  ↓ Import
Quest Scene (无 Network ID 或 ID 不一致)
  ↓ Accept All
  ID 对齐完成
```

### 导出文件格式

工具导出 **场景层级路径** 与 Network ID 的对应关系:

```json
{
  "10": "/CubePickup",
  "11": "/Prefabs/SyncedPen"
}
```

> 文件中的 **路径** 必须与目标 scene 的层级结构 **完全匹配**。
> 非网络对象不需要一致(只要不与需要同步的对象冲突)。

### ⚠️ 命名警告

> **禁止在网络对象的名称中使用正斜杠 `/`**!

- 原因:GameObject 路径使用 `/` 作为分隔符
- 影响:导入时路径解析错乱,导致 ID 匹配失败
- 实践:用 `_` 或空格替代(如 `Cube_Pickup` 而非 `Cube/Pickup`)

---

## 工作流程详解

### 1. 初始状态(无 Network ID)

打开工具,看到场景中所有 GameObject 的 Network ID 列表。

**如果没有 ID 显示**:
1. 点击 **Regenerate Scene IDs**
2. 工具自动为场景中所有需要同步的对象分配 ID
3. 检查列表确保分配合理

### 2. 导出 Network ID

1. 在 PC scene 中打开工具
2. 点击 **Export** 按钮
3. 选择保存路径,生成 `.json` 文件
4. 文件包含所有网络对象的 ID + 层级路径

### 3. 导入到另一场景

1. 在 Quest scene 中打开工具
2. 点击 **Import**,选择刚才的 `.json` 文件
3. 工具扫描当前 scene,寻找匹配路径
4. 如果所有路径都匹配:
   - 显示一个大区块,带 **Accept All** 按钮
   - 点击 → 完成 ID 同步

---

## 冲突解决(Resolving Conflicts)

### 触发条件

| 冲突类型 | 触发场景 |
|---------|---------|
| **对象不存在** | 文件中有 ID 路径,但 scene 中找不到该对象 |
| **ID 不匹配** | 对象 A 声明 ID = 20,但文件说路径 B 应该是 20 |
| **重复 ID** | 多个对象争夺同一个 ID |

### 扫描方式

- **Scan For Conflicts**:手动扫描一次
- **Auto Scan**:实时自动扫描(推荐在修改 scene 时开启)

### 冲突处理策略

| 选项 | 行为 | 适用场景 |
|------|------|---------|
| **Ignore** | 跳过该冲突对象 | 确认该对象不需要同步 |
| **Select** | 手动指定一个 GameObject 接收该 ID | 对象已重命名/移动 |
| **Ignore All** | 全部忽略,不修改 scene | 仅查看冲突 |
| **Accept All** | 接受所有自动匹配 | 无冲突时 |

### 最佳实践

> **跨 scene 复制 ID 前,先清除目标 scene 的现有 Network ID**!

否则可能出现 "旧 ID 与新 ID 互相覆盖" 的混乱。`Ignore / Select` 选项用于以下高级场景:
- 修复破损的 scene
- 保留部分 scene 已有 ID
- 不希望破坏某些特定对象的同步关系

---

## 典型使用场景

### 场景 1:跨平台 World 开发

```
项目结构:
  /Project
    /Scenes
      PC_World.unity
      Quest_World.unity
    
工作流:
  1. 在 PC scene 中分配 Network ID
  2. Export → network_ids.json
  3. 在 Quest scene 中 Import 该文件
  4. Accept All → ID 同步完成
  5. 发布到 VRChat
```

### 场景 2:调试 "GameObject not found" 错误

```
错误: Network ID 23 not found on remote client
排查:
  1. 打开 Network ID Utility
  2. Scan For Conflicts
  3. 查找 ID = 23 的对象路径
  4. 比对本地 scene 与远程客户端路径
  5. 修复后重新 Export / Import
```

### 场景 3:重命名同步对象

```
问题: 重命名了 /CubePickup → /PickupCube
解决:
  1. Network ID 还在旧路径上
  2. 打开工具
  3. Scan For Conflicts → 出现 "object not found"
  4. Select 新路径 /PickupCube
  5. Accept
```

---

## 与其他工具的区分

| 工具 | 用途 | 运行时 / Editor |
|------|------|----------------|
| **Network ID Utility** | 管理 GameObject 的网络 ID 分配 | **Editor Only** |
| **Network Stats**(见 `network-stats.md`) | 运行时监控网络流量 | Runtime (Udon) |
| **ClientSim**(见 `memory/sources/clientsim.md`) | Editor 内模拟网络环境 | **Editor Only** |

---

## 关键要点

| 要点 | 说明 |
|------|------|
| **工具定位** | Editor 工具,**不打包到 World** |
| **核心场景** | 跨平台 World 开发(PC/Quest 独立 scene) |
| **关键文件** | 导出 `.json`,包含 ID + 层级路径 |
| **命名规范** | 禁止在网络对象名中使用 `/` |
| **冲突解决** | Ignore / Select / Accept All |
| **最佳实践** | 导入前清空目标 scene 的 ID |
| **SDK 版本** | 适用 SDK 3.10.x+(可能随 SDK 更新) |

---

## Missing Information

- 工具是否支持 **多个 Project 之间的 ID 同步**(文档只提到 scene 之间)
- 工具是否提供 **CI/CD 集成**(命令行调用)
- 工具是否区分 **[UdonSynced] 变量** 与 **普通网络事件** 的 Network ID 分配策略
- Network ID 的 **最大值** 是否有上限(VRChat 实例对象数限制)

> 以上信息文档未明确说明,需要进一步实验或查阅 SDK 源码。
