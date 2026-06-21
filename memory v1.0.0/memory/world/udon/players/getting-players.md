# Getting Players — 获取玩家对象

> Domain: World / Udon / Players
> Subtype: API 详解
> Source: https://creators.vrchat.com/worlds/udon/players/getting-players (Last updated: 2025-11-14)
> 底层引用: `memory/api/player-api.md`
> 抓取日期: 2026-06-15

---

## 概述

本文档涵盖获取**单个玩家、玩家群组或全部玩家**的 API,以及 **Player Tag System**(轻量级 string → string 标签系统)。

---

## 核心 API

### Networking.get LocalPlayer

- **返回**: `VRCPlayerApi`
- **来源**: `Networking` 类的静态方法
- **说明**: 获取**本地玩家**(当前运行此 Udon 脚本的玩家,即"你")
- **关键**: "Know yourself!" — 在 OnPlayerJoined 中调用时,LocalPlayer 已可用

> ⚠️ **官方说明**: 虽然此函数是 `Networking` 类的成员,但被列在 Player API 文档中。

```csharp
VRCPlayerApi localPlayer = Networking.LocalPlayer;
```

---

### GetPlayerCount

- **返回**: `int`
- **说明**: 获取调用时实例中的**实际玩家数**
- **用途**: 与 `GetPlayers` 配合遍历玩家

```csharp
int count = VRCPlayerApi.GetPlayerCount();
```

---

### GetPlayers

- **签名**: `VRCPlayerApi[] GetPlayers()` 或 `void GetPlayers(VRCPlayerApi[] buffer)`
- **说明**: 获取实例中**所有玩家**
- **用途**: For 循环遍历、应用设置、查找特定玩家

#### ⚠️ 关键: 分配 vs 非分配版本

| 方式 | 内存行为 | 适用场景 |
|---|---|---|
| `VRCPlayerApi.GetPlayers()` | **每次分配新数组** | 偶尔调用 |
| `VRCPlayerApi.GetPlayers(VRCPlayerApi[] buffer)` | **复用传入数组,无分配** | 高频调用 (如 `Update`) |

#### 版本 1: 简单但每次分配

```csharp
VRCPlayerApi[] players = VRCPlayerApi.GetPlayers();
for (int i = 0; i < players.Length; i++)
{
    VRCPlayerApi player = players[i];
    // Do something with the player...
}
```

> ⚠️ **Udon VM 风险**: 每次调用都重建数组,在 `Update` 中使用会产生持续 GC 压力。

#### 版本 2: 预分配,无 GC (推荐)

```csharp
private VRCPlayerApi[] players;

private void Start()
{
    players = new VRCPlayerApi[100]; // 数组大小需能容纳世界的最大玩家数
}

private void Update()
{
    VRCPlayerApi.GetPlayers(players);
    int playerCount = VRCPlayerApi.GetPlayerCount();
    for (int i = 0; i < playerCount; i++)
    {
        VRCPlayerApi player = players[i];
        // Do something with the player...
    }
}
```

> 📌 **重要约束**: 数组必须**足够大**,否则会越界。在 Quest 等内存受限平台需谨慎估算最大玩家数。

---

### GetPlayerById

- **输入**: `int playerId`
- **返回**: `VRCPlayerApi` (可能为 `null`)
- **说明**: 根据 Player ID 获取 `VRCPlayerApi` 对象(若存在)
- **用途**: 通过持久化 ID 跨实例恢复玩家引用

---

### get playerId

- **类型**: `int` (属性)
- **说明**: 获取**缓存**的 PlayerId
- **行为**: 若未缓存,自动调用 `GetPlayerId()`

---

### GetPlayerId

- **返回**: `int`
- **说明**: 从源数据获取 Player 的网络 ID
- **使用**: 需获取权威 PlayerId 时调用

---

## Player Tag System (玩家标签系统)

> 一种**快速而粗暴**的 string → string 玩家标签机制,无需自建变量和集合。

### SetPlayerTag / GetPlayerTag

- **Set**: `_string, string_` (玩家, key, value)
- **Get**: `_string, string_` (玩家, key) → value
- **说明**: 设置/获取玩家关联的字符串变量

**示例**: 烹饪游戏中给玩家分配"角色"
```csharp
// 玩家加入时设置角色
public override void OnPlayerJoined(VRCPlayerApi player)
{
    player.SetPlayerTag("role", "chef");  // 或 "customer"
}

// 查询时获取角色
string role = player.GetPlayerTag("role");
```

> 📝 **注意**: Tag 数据由 VRChat SDK 管理,跨 World 状态保留规则需参考 SDK 文档。

---

### ClearPlayerTags

- **输入**: `VRCPlayerApi`
- **说明**: 清除该玩家上的**所有** tag

---

### GetPlayersWithTag

- **状态**: ⚠️ **官方明确标注: 当前不可用**
- **原因**: 返回类型是 `List<VRCPlayerApi>`,Udon 暂不支持 `List`
- **预期用法**: 传入 `VRCPlayerApi[]` 数组和 tag,该方法会用具有该 tag 的玩家填充数组
- **建议**: 在 `GetPlayersWithTag` 可用前,改用 `GetPlayers` + 手动遍历 + `GetPlayerTag` 过滤

```csharp
// 替代实现: 手动过滤
VRCPlayerApi[] allPlayers = VRCPlayerApi.GetPlayers(playersBuffer);
int count = VRCPlayerApi.GetPlayerCount();
List<VRCPlayerApi> chefs = new List<VRCPlayerApi>();
for (int i = 0; i < count; i++)
{
    if (allPlayers[i].GetPlayerTag("role") == "chef")
    {
        chefs.Add(allPlayers[i]);
    }
}
```

> ⚠️ **List<VRCPlayerApi> 在 Udon 中受限**,如需动态集合可参考 `memory/world/udon/data-containers.md` 的 Data Lists 方案。

---

## 与底层 API 的对照

| 本文件 API | 底层 `player-api.md` |
|---|---|
| `GetPlayers` | `VRCPlayerApi.GetPlayers()` 数组版本 |
| `LocalPlayer` | `Networking.LocalPlayer` (跨类引用) |
| `GetPlayerById` / `GetPlayerId` / `playerId` | `playerId` 字段(底层标注"需验证具体 API 名") |
| `SetPlayerTag` / `GetPlayerTag` / `ClearPlayerTags` | 本文件首次出现 |
| `GetPlayersWithTag` | 当前不可用 |

---

## 风险与限制

| 风险 | 说明 |
|---|---|
| **GC 压力** | `GetPlayers()` 无参版本在 `Update` 中持续调用会产生大量 GC,改用预分配版本 |
| **数组大小** | 预分配数组必须容纳**世界允许的最大玩家数** |
| **`GetPlayersWithTag` 不可用** | 官方明确说明,需手动遍历实现 |
| **Tag 跨 World 行为** | Tag 在玩家离开 World 后是否保留需参考 SDK 文档,不可假设持久性 |
| **PlayerId 跨实例** | PlayerId 在同一实例中稳定,跨实例可能变化,不能作为永久身份 |

---

## 最佳实践

1. **优先使用预分配版本**: 在 `Update`/Tick 类代码中,务必用 `GetPlayers(buffer)`
2. **缓存 `LocalPlayer`**: 在 `Start()` 中缓存 `Networking.LocalPlayer` 引用,避免每帧调用
3. **Tag 命名空间**: 使用前缀避免冲突,如 `"game1234:role"` 而非 `"role"`
4. **Tag 限制**: Tag 是 string-to-string,不能存对象/数组;复杂数据用 `VRCJson` 或 Data Containers
5. **遍历时检查 IsValid**: 玩家可能在遍历过程中离开,谨慎处理引用失效

```csharp
// 推荐模式: 缓存 + 预分配 + IsValid 检查
private VRCPlayerApi _localPlayer;
private VRCPlayerApi[] _playerBuffer;

private void Start()
{
    _localPlayer = Networking.LocalPlayer;
    _playerBuffer = new VRCPlayerApi[80]; // Quest 限制更严,需评估
}

public override void OnPlayerJoined(VRCPlayerApi player)
{
    player.SetPlayerTag("game:role", "spectator");
}
```
