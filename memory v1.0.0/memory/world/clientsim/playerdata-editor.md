# PlayerData Editor

> 来源: [VRChat Creator Docs - PlayerData Editor](https://creators.vrchat.com/worlds/clientsim/playerdata-editor-window)
> 索引日期: 2026-06-15

---

## 概述

ClientSim 可以模拟 VRChat SDK 的 **Persistence** 特性。PlayerData Editor Window 允许你在 World 中调试持久化数据。

**打开方式**:`VRChat SDK` > `ClientSim PlayerData`

---

## Window 字段

| 元素 | 说明 |
|------|------|
| **Player 选择下拉框** | 选择查看哪个玩家的 PlayerData。默认本地玩家;Play Mode 中生成的远程玩家也可选择。 |
| **PlayerData 列表** | 展示选中玩家的 PlayerData 键、值、数据类型。**实时更新**。 |
| **Clear All PlayerData** | 删除当前场景的所有 PlayerData。用于"重置"测试。 |
| **Refresh** | 刷新列表。当手动编辑 JSON 文件时需点击此按钮查看更改(Play Mode 中更改立即生效)。 |
| **Open Local Data Folder** | 打开 ClientSim 存储当前场景 JSON 数据的文件夹。 |
| **Add Test Data For Remote Player** | 为远程玩家创建 PlayerData(仅在 Play Mode 中选中远程玩家且本地玩家有数据时显示)。 |

### 实时性

- 列表会随 PlayerData 更新**实时刷新**
- 手动编辑 JSON 文件后,需点击 `Refresh` 按钮才在 UI 中看到变化
- JSON 文件的修改在 Play Mode 中**立即生效**(即使不点击 Refresh)

### "Add Test Data For Remote Player" 行为

| 条件 | 说明 |
|------|------|
| **可见性** | 仅在 Play Mode 中选中远程玩家,且本地玩家有数据时显示 |
| **实现机制** | 复制本地玩家的测试数据 JSON 文件,随机化每个值 |
| **设计假设** | PlayerData 结构在不同玩家间应一致,仅值不同 |
| **副作用** | 会触发 `OnPlayerDataUpdated` 事件,便于测试多玩家数据更新路径 |
| **可重复性** | 每次点击都重新随机化,生成新的测试数据 |

### 数据存储位置

PlayerData 数据存储在 **项目根目录**(Assets 文件夹**外**):

```
/ClientSimStorage/PlayerData/
```

- **场景隔离**:PlayerData 文件与场景一一对应,关联依据为场景名
- **持久化**:在 Play Mode 会话之间保留
- **场景重命名**:重命名场景时需同步重命名 JSON 文件,否则数据视为"新场景"重新开始

---

## 工程意义

| 维度 | 说明 |
|------|------|
| **无 VRChat 测试** | 在编辑器中即可调试 PlayerData 逻辑 |
| **多玩家路径** | "Add Test Data For Remote Player" 模拟多玩家数据更新,验证 `OnPlayerDataUpdated` 事件路径 |
| **手动编辑友好** | JSON 文件可外部编辑(如脚本生成测试数据),需点 `Refresh` 同步 UI |
| **场景迁移** | 重命名场景必须同步迁移 JSON 文件 |
| **与 VRChat 差异** | ClientSim 的 PlayerData 模拟可能与真实 VRChat 服务端存在差异(数值范围、容量限制等) |

---

## 相关页面

- [PlayerObject Editor](playerobject-editor.md) - 调试 PlayerObject(对象级持久化)
- [ClientSim Index](index.md) - 回到主目录
- [Script Execution Order](systems/script-execution-order.md) - 系统中 `UdonManager` 的执行位置
