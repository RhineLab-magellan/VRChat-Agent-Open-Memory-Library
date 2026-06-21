# PlayerObject Editor

> 来源: [VRChat Creator Docs - PlayerObject Editor](https://creators.vrchat.com/worlds/clientsim/playerObject-editor)
> 索引日期: 2026-06-15

---

## 概述

ClientSim 可以模拟 VRChat 的 **PlayerObject** 机制。**进入 Play Mode 时**,ClientSim 会自动 spawn PlayerObject 并恢复其持久化属性。

---

## Usage 用法

进入 Play Mode 后,ClientSim 会:

1. Spawn 所有 PlayerObject
2. 恢复其持久化属性
3. 在 Hierarchy 中选中 PlayerObject,可看到两个自动添加的组件:
   - **`ClientSimNetworkingView`**
   - **`ClientSimNetworkIdHolder`**

### ClientSimNetworkIdHolder 组件

该组件显示 GameObject 上组件的 synced 属性名称和值。

| 字段 | 说明 |
|------|------|
| **Network Id** | GameObject 的网络 ID。**在 Unity 加载场景前填入**,若场景存在 Network ID 冲突则 **不会** 运行。 |
| **Network Components** | GameObject 上保存的组件列表,包含该对象的所有持久化数据。 |

### 数据存储位置

ClientSim 用于 PlayerObject 的数据存储在项目内:

```
projectName/ClientSimStorage/PlayerObjects/PlayerObjects_#_SceneName.json
```

- 可通过系统文件浏览器查找
- 文件名中 `#` 为占位符,实际为场景 ID
- 重命名场景时需同步重命名 JSON 文件,否则持久化数据丢失

---

## 工程意义

| 维度 | 说明 |
|------|------|
| **调试便捷性** | 无需 VRChat 客户端即可查看 PlayerObject 持久化数据 |
| **数据隔离** | 模拟数据存储在 `ClientSimStorage/` 目录,与发布无关 |
| **网络 ID 冲突检测** | 进入 Play Mode 前即校验,避免运行时崩溃 |
| **场景迁移** | 重命名场景必须同步迁移 JSON 文件,否则数据丢失 |

---

## 相关页面

- [PlayerData Editor](playerdata-editor.md) - 调试 PlayerData(全局键值对)
- [ClientSim Index](index.md) - 回到主目录
- [Script Execution Order](systems/script-execution-order.md) - 系统中 `SyncedObjectManager` 的执行位置
