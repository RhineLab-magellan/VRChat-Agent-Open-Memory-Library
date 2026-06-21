# ClientSim

> 来源: [VRChat Creator Docs - ClientSim](https://creators.vrchat.com/worlds/clientsim/)
> 索引日期: 2026-06-15
> 原始仓库: [github.com/vrchat-community/creator-docs](https://github.com/vrchat-community/creator-docs)

---

## 概述

**ClientSim**(Client Simulator)是 **VRChat Worlds SDK** 内置的 Unity Editor 模拟器,在编辑器中复刻 VRChat 客户端行为,用于加速 World 开发调试。

### 核心定位

| 维度 | 说明 |
|------|------|
| **运行位置** | Unity Editor(无需打开 VRChat 客户端) |
| **替代场景** | 减少 Build & Test 循环,提升迭代效率 |
| **集成方式** | 集成于 VRChat SDK3(2025 年后),非独立包 |

### ⚠️ 重要警告

> **ClientSim 无法模拟所有 VRChat 特性,公开发布前必须在 VRChat 客户端内进行完整测试。**

---

## Features 核心特性

- **无需 VRChat**:在 Unity Editor 中直接测试 World
- **键鼠 / 手柄控制**:使用鼠标键盘或 Gamepad 控制 Player
- **Udon 变量检查**:在 Play Mode 中实时检视 Udon 变量
- **完整交互模拟**:支持 Pickups、Interacts、UI、Stations
- **EditorOnly 清理**:进入 Play Mode 时自动删除 `EditorOnly` 标记的对象

---

## Windows 调试窗口

ClientSim 提供多个 Editor Window 辅助调试:

| 窗口 | 用途 | 访问方式 |
|------|------|----------|
| **ClientSim Settings** | 修改本地玩家名称、玩家身高、禁用 ClientSim 等 | Editor 菜单 |
| **In-Game Settings** | Play Mode 中按 `Escape` 键打开 | 运行时快捷键 |
| **ClientSim PlayerData** | 调试 PlayerData | `VRChat SDK` > `ClientSim PlayerData` |
| **ClientSim PlayerObject** | 调试 PlayerObjects | Hierarchy 选中 PlayerObject |

---

## Getting Started 快速开始

1. 打开你的 VRChat World 场景
2. 在 Unity 中按 Play
3. 在 Unity 的 "Game" 窗口中测试你的 World

详细的内部机制请参考 [Systems](systems/index.md) 子分类。

---

## Networking Differences in ClientSim

**核心限制**:ClientSim **只模拟本地 VRChat Player**,不模拟远程玩家。

- **本地玩家**:Deserialization 事件会被模拟
- **远程玩家**:Deserialization 事件 **不会** 触发
- **部分服务器行为已模拟**:例如生成远程玩家时本地玩家会收到 `OnPlayerRestored` 事件

> ClientSim 使用了与 VRChat 不同的网络序列化器实现,导致 `OnPostSerialization` 和 `OnDeserialization` 事件中传递的数据存在差异(详见下表)。

### `OnPostSerialization(SerializationResult)`

> ⚠️ **ClientSim 仅在 synced PlayerObject 上触发此事件。**

| 字段 | In ClientSim | In VRChat |
|------|--------------|-----------|
| `SerializationResult.success` | Always `true` | 序列化成功时为 `true` |
| `SerializationResult.byteCount` | 对象上序列化的 **属性数量** | 实际发送的 **字节数** |

### `OnDeserialization(DeserializationResult)`

> ⚠️ **ClientSim 仅在 synced PlayerObject 上触发此事件。**

| 字段 | In ClientSim | In VRChat |
|------|--------------|-----------|
| `DeserializationResult.sendTime` | Always `0` | 消息发送时间(秒) |
| `DeserializationResult.receiveTime` | Always `0` | 消息接收时间(秒) |
| `DeserializationResult.isFromStorage` | Works as normal | 若从持久化存储发送则为 `true` |

### 工程意义

| 影响 | 说明 | 缓解措施 |
|------|------|----------|
| `byteCount` 语义不同 | ClientSim 中是属性数量,VRChat 中是字节数 | 勿依赖 `byteCount` 做带宽统计 |
| 时间戳为零 | 客户端 `sendTime`/`receiveTime` 永远为 0 | 计算延迟需用 `Networking.GetServerTimeInMilliseconds()` |
| 远程玩家不触发 | 多个玩家的反序列化测试不完整 | 多玩家同步测试必须在 VRChat 中进行 |

---

## 相关页面

- [PlayerObject Editor](playerobject-editor.md) - 调试 PlayerObject
- [PlayerData Editor](playerdata-editor.md) - 调试 PlayerData
- [Systems](systems/index.md) - 内部架构与子系统
  - [Architecture](systems/architecture.md) - 观察者 + 依赖注入
  - [Editor](systems/editor.md) - Editor 子系统
  - [Runtime](systems/runtime.md) - Runtime 子系统
  - [Script Execution Order](systems/script-execution-order.md) - 11 个系统执行顺序

## 相关引用

- `memory/sources/clientsim.md` - ClientSim **项目仓库**元数据(发展历史、双向同步、贡献流程),与本目录的**用户使用文档**互补
- `memory/sources/example-central.md` - Example Central 中涉及的 ClientSim 相关引用
