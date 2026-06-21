---
title: Player Join Zones
category: world
subcategory: examples

knowledge_level: applied
status: active

tags:
  - world
  - udonsharp
  - avatar

aliases:
  - "Player Join Zones"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Player Join Zones

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/player-join-zones)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/player-join-zones/
> 文档版本: Last updated Oct 30, 2024
> SDK: 3.5+ (DataList, FieldChangeCallback, OnPlayerTriggerStay)

## Example Central Package

> ✅ **需要 Example Central Package**
> 通过 `VRChat SDK → 🏠 Example Central` 导入
> 包含 PlayerJoinZone Prefab、JoinZoneWithDisplay 扩展、BossPicker 扩展

### Example World
- **World ID**: `wrld_12492ad5-ff17-445d-9f90-7b14376b1f32`
- **URL**: https://vrchat.com/home/world/wrld_12492ad5-ff17-445d-9f90-7b14376b1f32

> ⚠️ **此 World ID 与 Minimap 共享**

---

## 概述

演示基于**玩家位置**收集玩家、构建**简单大厅流程**(加入→游戏→结束→重新开始)。
- **核心模式**: Trigger 区域 + 玩家列表同步
- **两种扩展**:
  - `JoinZoneWithDisplay` - 带 UI 显示的"加入大厅"
  - `BossPicker` - 随机选一个玩家作为"Boss"(变巨大)
- **典型场景**: 投票系统、阵营分配、小游戏组队

---

## 关键 Udon API

| API | 用途 |
|-----|------|
| `OnPlayerTriggerStay(VRCPlayerApi)` | 玩家在 Trigger 区域内持续触发 |
| `OnPlayerTriggerExit(VRCPlayerApi)` | 玩家离开 Trigger 区域 |
| `OnPlayerLeft(VRCPlayerApi)` | 玩家离开实例 |
| `VRCPlayerApi.displayName` | 玩家显示名 |
| `VRCPlayerApi.playerId` | 玩家 ID(int) |
| `VRCPlayerApi.AvatarEyeHeight` | 设置玩家 Avatar 眼睛高度(用于"变大") |
| `[FieldChangeCallback]` | UdonSharp 特性,字段变化触发回调 |
| `DataList` | Udon 中的列表容器 |

---

## 三种 Mode 状态机

```
MODE_JOIN (加入中)
  ↓ 玩家按按钮
MODE_GAME (游戏中,锁定名单)
  ↓ 游戏结束
MODE_END (结束,显示结果)
  ↓ 玩家按按钮
回到 MODE_JOIN
```

**额外的 Mode**:
- `JoinZoneWithDisplay` 扩展: `MODE_WAIT` 冻结 UI 按钮 3 秒
- `BossPicker` 扩展: `MODE_CHOSEN`(已选 Boss) + `MODE_GAMEOVER`(游戏结束回顾)

---

## 核心架构: PlayerJoinZone 基类

### Modes 字段
```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PlayerJoinZone : UdonSharpBehaviour
{
    [UdonSynced] [FieldChangeCallback(nameof(OnModeChanged))]
    public int Mode = MODE_JOIN;  // MODE_JOIN / MODE_GAME / MODE_END
    
    public DataList Players = new DataList();
    public Transform[] targets;  // 需要通知的其他 Udon 程序
}
```

### 玩家追踪三事件

| 事件 | 触发 | 行为 |
|------|------|------|
| `OnPlayerTriggerStay` | 玩家进入或在区域内 | Owner 检查并加入 DataList |
| `OnPlayerTriggerExit` | 玩家离开 | Owner 从 DataList 移除 |
| `OnPlayerLeft` | 玩家离开实例 | 防止"卡在列表" |

### 关键交互流程示例

> 场景: 玩家 Dingbat 进入区域,接着 SquirrelFam 也进入

1. Zone 初始化 Mode = `MODE_JOIN` → 触发 Owner 的 `ResetPlayers()` → 新建 DataList
2. Dingbat 踏入区域 → `OnPlayerTriggerStay` 触发 → Owner 加入 DataList
3. SquirrelFam 踏入 → 同上
4. Dingbat 离开实例 → `OnPlayerLeft` → 移除 Dingbat
5. SquirrelFam 离开区域 → `OnPlayerTriggerExit` → 移除 SquirrelFam

---

## 扩展 1: JoinZoneWithDisplay

### 额外字段

| 名称 | 类型 | 说明 |
|------|------|------|
| `_playerNamesField` | `Text` | 显示当前区域中所有玩家名 |
| `_buttonLabelField` | `Text` | 按钮内的文本 |
| `_toggleButton` | `Button` | 触发 `_ToggleMode` 的 UI 按钮 |
| `_ownerField` | `Text` | 显示当前 Owner(调试用) |
| `PlayerNamesString` | `string` (synced) | 所有玩家名拼接的字符串 |
| `MODE_WAIT` | 常量 | 等待状态(冻结按钮 3 秒) |
| `_waitDuration` | `float` | 等待时长 |

### 同步字符串构造

```csharp
// 构造 "Dingbat, SquirrelFam, OtherPlayer" 这样的字符串
public string GetPlayersAsStringList()
{
    return string.Join(", ", Players.ToArray());
}
```

### Mode 切换流程(关键)

```csharp
// 任何玩家都可以点按钮
public void _ToggleMode()
{
    if (!Networking.IsOwner(gameObject))
    {
        // Non-Owner: 发送网络事件给 Owner
        SendCustomNetworkEvent(NetworkEventTarget.Owner, nameof(ToggleModeRPC));
    }
    else
    {
        // Owner: 本地调用
        ToggleModeRPC();
    }
}

public void ToggleModeRPC()
{
    // Owner 端循环 Mode: JOIN → GAME → END → JOIN
    Mode = (Mode + 1) % 3;  // 假设 3 个 Mode
    
    // FieldChangeCallback 触发 OnModeChanged
    // 同步到所有玩家后,每玩家本地执行 OnModeChanged
}
```

---

## 扩展 2: BossPicker

### 核心特性

1. **随机选 Boss**: `Mode` 进入 `MODE_CHOSEN` 时,Owner 随机从 DataList 选一个 playerId
2. **同步 Boss ID**: 通过 `[UdonSynced] [FieldChangeCallback]` 的 `_bossPlayerId` 字段
3. **本地应用**: 每玩家在 `OnBossChanged` 中检查自己是否是 Boss
4. **Boss 变大**:
   ```csharp
   if (VRCPlayerApi.GetPlayerById(_bossPlayerId) == Networking.LocalPlayer)
   {
       Networking.LocalPlayer.SetAvatarEyeHeight(5f);  // 最大 5 单位
   }
   ```

### 关键字段

| 名称 | 类型 | 说明 |
|------|------|------|
| `_bossPlayerId` | `int` (synced) | Boss 的 playerId |
| `_maxPlayerHeight` | `float` | 非 Boss 玩家允许的最大身高 |
| `gameDuration` | `float` | `MODE_CHOSEN` 持续时间,默认 5 秒 |

### Mode 状态机(扩展后)

```
MODE_JOIN → MODE_GAME → MODE_CHOSEN (选 Boss)
  → 自动 5 秒后 → MODE_GAMEOVER → MODE_END
  → 玩家按按钮 → MODE_JOIN (Boss 恢复原大小)
```

---

## Networking 模式: 多层级 Manual Sync ⭐

### 关键设计
> 这个示例展示了**多个独立同步字段**协同工作的模式

| 字段 | 同步模式 | 触发 |
|------|----------|------|
| `Mode` | Manual + FieldChangeCallback | 任何玩家按钮(通过 RPC) |
| `Players` (DataList) | Manual | Owner 自动触发 |
| `PlayerNamesString` | Manual + FieldChangeCallback | 每次 `OnPlayersChanged` |
| `_bossPlayerId` | Manual + FieldChangeCallback | Owner 在 `MODE_CHOSEN` 时 |

### 同步链
```
玩家按按钮
  ↓
Non-Owner: SendCustomNetworkEvent(Owner, "ToggleModeRPC")
  ↓
Owner 执行 ToggleModeRPC()
  ↓
修改 Mode → FieldChangeCallback 触发 OnModeChanged
  ↓
RequestSerialization() 发送 Mode
  ↓
所有 Non-Owner 接收 → OnModeChanged 本地执行
```

---

## 跨程序通信: `targets` 数组

```csharp
[SerializeField] private UdonBehaviour[] targets;

// 在 OnModeChanged 末尾
foreach (var target in targets)
{
    target.SetProgramVariable("Mode", Mode);
    target.SendCustomEvent("OnModeChanged");
}
```

**UdonSharp SetProgramVariable + SendCustomEvent 模式**:
- 详细参考 `memory/api/udonsharp-runtime.md`
- 这种模式允许**中央协调者**通知**多个观察者**同时更新

### 可观察变量(供其他程序订阅)

| 变量 | 触发回调 |
|------|----------|
| `int Mode` | `OnModeChanged` |
| `DataList Players` | `OnPlayersChanged` |
| `int BossPlayerId` | `OnBossChanged` |

---

## 二次开发建议

- **投票系统**: DataList 改为 DataDict(playerId → vote)
- **队伍分配**: 在 `OnModeChanged` 中按某种规则分配队伍
- **观战模式**: Non-Boss 玩家摄像机锁定到 Boss
- **复活机制**: 多个 Zone 串联(死亡 → 复活点 → 重进游戏)

---

## 与知识库互补

- **DataList / DataDict**: `memory/world/data-containers.md` ⭐ 直接互链
- **FieldChangeCallback**: `memory/api/udonsharp-runtime.md` ⭐
- **SetProgramVariable 模式**: `memory/api/udonsharp-runtime.md` ⭐
- **OnPlayerTriggerStay 完整 API**: `memory/api/events-reference.md`
- **AvatarEyeHeight**: `memory/api/player-api.md`(待建)
- **Mute Others(基于区域静音)**: `memory/world/examples/mute-others.md` ⭐ Challenge 提示直接引用本示例

## 相关 Udon 文档链接

- [DataList 完整文档](/worlds/udon/data-containers/data-lists)
- [FieldChangeCallback 完整文档](https://udonsharp.docs.vrchat.com/udonsharp/#fieldchangecallback)
- [Player Collisions - Trigger](/worlds/udon/players/player-collisions)
