---
title: 100KB 限制与常见陷阱
category: world
subcategory: udon/persistence
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - limits
  - storage
  - optimization
  - pitfalls
aliases:
  - 100KB 限制
  - 持久化陷阱
  - 压缩策略
  - 写入时机
related:
  - ../../../api/persistence.md
  - ../index.md
  - player-data.md
  - player-object.md
  - serialization.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/udon/persistence/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# 100KB 限制与常见陷阱

> SDK Version: 3.7+
> 官方文档:https://creators.vrchat.com/worlds/udon/persistence/#limitations
> 主题:**深入 100KB 限制、压缩策略、写入时机、8 个常见陷阱**

---

## 概述

VRChat 对持久化有 **硬限制**。理解这些限制是设计持久化系统的关键。

**核心数字**:
- **100 KB** / 玩家 / World PlayerData(压缩后)
- **100 KB** / 玩家 / World PlayerObject(压缩后,**独立配额**)
- **~300 KB** 原始数据(高度可压缩时)
- **~50 字符** String 值(建议)
- **128 字符** Key 名(建议)
- **❌ 不支持** Key 删除

---

## 100KB 限制详解

### 三层数字关系

```
原始数据  ──[VRChat 压缩]──>  100KB 压缩后
         (高效压缩时)
~300KB                     =  100KB
         (低效压缩时)
~100KB                     =  100KB
```

> **关键**:VRChat 存储的是 **压缩后** 大小。原始数据可达 ~300KB(若数据高度可压缩,例如重复字符串、零字节数组)。

### 超限后果

| 触发条件 | 后果 |
|---------|------|
| 写操作使压缩后数据 > 100KB | VRChat 写 **错误日志**,数据 **未保存** |
| 玩家写时 | 触发 `OnPlayerDataStorageExceeded` 事件 |
| 写后接近 100KB | 触发 `OnPlayerDataStorageWarning` 事件 |

### 配额独立原则

```
PlayerData 配额: 100KB ←── 与 PlayerObject 配额完全独立
PlayerObject 配额: 100KB ←──
```

> **设计含义**:可以同时用满 200KB(100KB PlayerData + 100KB PlayerObject)。

---

## 字符串压缩策略

### 字符串越相似,压缩率越高

```text
数据                                原始大小    压缩后    压缩率
─────────────────────────────────────────────────────────────
"LevelComplete_1"                   15         8         47%
"LevelComplete_1"+"LevelComplete_2" 30         10        67%
"LevelComplete_1"+...+"LevelComplete_100"  ~2200  ~50    98%
```

> **最佳实践**:用 **公共前缀**(如 `LevelComplete_`、`Achievement_`)。VRChat 的 zstd 压缩能识别重复模式,极度压缩。

### 整数数组压缩

```text
数据                            原始大小    压缩后    压缩率
──────────────────────────────────────────────────────────
int[]{1,2,3,4,5}                20         12        40%
int[]{0,0,0,0,0,0,0,0,0,0}      40         4         90%
byte[]{0,...} (100 元素)        100        4         96%
```

> **最佳实践**:用 **byte[]** 替代 **int[]**(4x 节省空间)。稀疏数组(大量 0)压缩率极高。

### JSON 压缩

```text
JSON 字符串                      原始大小    压缩后    压缩率
──────────────────────────────────────────────────────────
{"score":100}                    13         12        8%
[{"score":100},{"score":200}]    31         17        45%
[{"score":100},...]×1000         13000      600       95%
```

---

## 写入时机优化

### 规则 1:避免每帧写入

```csharp
// ❌ 错误:每帧写入,触发网络拥塞
void Update() {
    PlayerData.SetFloat(Networking.LocalPlayer, "Position", transform.position.x);
}

// ✅ 正确:降频 + 阈值触发
private float _lastSentTime = 0;
private float _lastSentValue = 0;

void Update() {
    if (Time.time - _lastSentTime < 5f) return;  // 5 秒一次
    if (Mathf.Abs(transform.position.x - _lastSentValue) < 0.1f) return;  // 变化 < 0.1 不写
    _lastSentTime = Time.time;
    _lastSentValue = transform.position.x;
    PlayerData.SetFloat(Networking.LocalPlayer, "Position", transform.position.x);
}
```

### 规则 2:批量写入合并

```csharp
// ✅ 正确:同一帧内多次 Set 自动合并(类似 Manual Sync)
public void OnLevelComplete(int score, int time) {
    PlayerData.SetInt(Networking.LocalPlayer, "Game-LastScore", score);
    PlayerData.SetInt(Networking.LocalPlayer, "Game-LastTime", time);
    // 两次 Set 在帧末合并为 1 个网络包
}
```

### 规则 3:不要在 OnPlayerJoined/Start 写

```csharp
// ❌ 错误:OnPlayerJoined 写 → 被服务器拉来的数据覆盖
public override void OnPlayerJoined(VRCPlayerApi player) {
    PlayerData.SetInt(Networking.LocalPlayer, "score", 0);
}

// ✅ 正确:在 OnPlayerRestored 之后,只在用户操作时写
public override void OnPlayerRestored(VRCPlayerApi player) {
    if (player != Networking.LocalPlayer) return;
    _dataReady = true;
}

public void OnPlayerDied() {
    if (!_dataReady) return;
    PlayerData.SetInt(Networking.LocalPlayer, "Deaths", GetDeaths() + 1);
}
```

### 规则 4:写前检查容量

```csharp
public void SaveGameData(byte[] data) {
    // 估算新数据大小
    int currentUsed = Networking.LocalPlayer.GetPlayerDataStorageUsage();
    int limit = Networking.LocalPlayer.GetPlayerDataStorageLimit();
    int newSize = currentUsed + data.Length;
    
    if (newSize > limit * 0.9f) {
        Debug.LogWarning("PlayerData 即将超限,请清理");
        // 可选:压缩、删除旧 key(用 Set 覆盖)
    }
    
    PlayerData.SetBytes(Networking.LocalPlayer, "Game-Save", data);
}
```

---

## 带宽与同步开销

### PlayerData 同步模型

> PlayerData 写入 = **Manual Sync 模式**

| 特性 | 说明 |
|------|------|
| 同步触发 | Set 时入队,帧末发送 |
| 发送内容 | **全部** PlayerData(不只是变更的 key) |
| 同步开销 | 类似 1 个 UdonBehaviour Manual Sync |
| 全局拥塞 | 大量数据 + 高频写 → `IsClogged = true` |

### PlayerObject 同步模型

| 特性 | 说明 |
|------|------|
| 同步触发 | `RequestSerialization()`(Manual)或自动(Continuous) |
| 发送内容 | **仅该 PlayerObject** 的 [UdonSynced] 字段 |
| 同步开销 | 独立带宽,不影响其他数据 |
| 全局拥塞 | 每个 PlayerObject 独立计量 |

### 高频 + 大量数据 → 必须用 PlayerObject

```text
场景: 持久画笔 - 20 条线,每条线最多 100 个点
- 每次画一笔 = 改 [UdonSynced] Vector3[] (400 bytes)
- 频率 1 Hz
- 总 PlayerData 大小: 20 * 400 = 8000 bytes

如果用 PlayerData:
- 每次画 = 发全部 8000 bytes
- 1 Hz = 8KB/s → IsClogged 风险

用 PlayerObject:
- 每次画 = 发该 PlayerObject 自己的 400 bytes
- 1 Hz = 400B/s → 远低于 11KB/s 上限

✅ 大量数据 + 高频 → PlayerObject
```

---

## 5 个超限检测

### 检测方法 1:Storage Information API(SDK 3.10+)

```csharp
int used = player.GetPlayerDataStorageUsage();
int limit = player.GetPlayerDataStorageLimit();
float percent = (float)used / limit;
if (percent > 0.9f) {
    Debug.LogWarning($"PlayerData 用量 {percent*100:F1}%");
}
```

### 检测方法 2:Storage Events

```csharp
public override void OnPlayerDataStorageWarning(VRCPlayerApi player) {
    if (player == Networking.LocalPlayer) {
        ShowWarningUI("PlayerData 接近上限,部分新数据可能无法保存");
    }
}

public override void OnPlayerDataStorageExceeded(VRCPlayerApi player) {
    if (player == Networking.LocalPlayer) {
        ShowErrorUI("PlayerData 已满,新数据未保存");
    }
}
```

### 检测方法 3:写入后事件回调

```csharp
public override void OnPlayerDataUpdated(VRCPlayerApi player, PlayerData.Info[] infos) {
    // 注意:这里无法直接知道是否"写入失败"
    // 但 OnPlayerDataStorageExceeded 事件会触发
    // 可结合使用
}
```

---

## 8 个常见陷阱

### 陷阱 1:OnPlayerJoined 写数据 → 被覆盖

**症状**:你的 Set 看似成功,但下次进入时数据被服务器拉来的值覆盖

**原因**:`OnPlayerJoined` 触发时,服务器数据可能还没拉取完毕

**修复**:所有写操作在 `OnPlayerRestored` 之后触发

### 陷阱 2:每个玩家都执行完整 OnPlayerRestored

**症状**:Server 端日志显示 5 次相同的初始化

**原因**:`OnPlayerRestored` 在每个玩家的 PlayerObject 上都触发

**修复**:
```csharp
public override void OnPlayerRestored(VRCPlayerApi player) {
    if (!Networking.IsOwner(gameObject)) return;  // 关键守卫
    // ... 只处理 owner
}
```

### 陷阱 3:PlayerData 频繁 Set 触发全局拥塞

**症状**:`IsClogged = true`,其他玩家网络卡顿

**原因**:PlayerData 每次 Set = 发全部 PlayerData

**修复**:降频、合并写、改用 PlayerObject

### 陷阱 4:Key 命名冲突

**症状**:两个 Prefab 共用 key "score",互相覆盖

**原因**:PlayerData 跨 World 全部 Prefab 共享

**修复**:用 `<Prefab名>-<功能>` 前缀

### 陷阱 5:Key 删除

**症状**:试图 `PlayerData.DeleteKey(...)` 发现方法不存在

**原因**:API 不支持 Key 删除(只能 Set 覆盖)

**修复**:用 SetBool(key, false) 或 SetInt(key, 0) 软删除

### 陷阱 6:Get* vs TryGet* 误用

**症状**:用户明明没设置值,代码读到 0(或空字符串)以为是默认值

**原因**:`Get*` 在 key 不存在时返回默认值,无法区分"未设置"和"显式设为 0"

**修复**:用 `TryGet*` 检查 `bool success`

### 陷阱 7:在 OnPlayerLeft 中尝试保存

**症状**:玩家离开时数据丢失

**原因**:玩家离开时已经无法触发持久化写入

**修复**:**持续保存**(关键事件触发时立即 Set),不要等 OnPlayerLeft

### 陷阱 8:模板 GameObject 被销毁

**症状**:新玩家加入时,PlayerObject 没有正确实例化

**原因**:VRChat 不会在玩家进入时重新创建模板(它是 disabled 但存在)

**修复**:**永远不要销毁/重命名** 模板 GameObject(就算它被 disable)

---

## 数据存储位置(开发期)

| 环境 | 存储位置 | 注意事项 |
|------|---------|---------|
| **已发布 World** | VRChat 服务器(跨平台/跨实例) | 同账号同 World 多开 → 数据冲突 |
| **Build & Test** | 本地(测试客户端) | 关闭测试客户端 → 数据删除 |
| **ClientSim** | 项目内 JSON 文件 | 见 `memory/sources/clientsim.md` |
| 重新 Build & Reload | 数据 **不重置** | 可继续测试 |
| 关闭测试客户端 | 数据 **删除** | 重新 Build & Test → 全新数据 |

> **警告**:不要在 Build & Test 中依赖"旧数据",因为它随时会消失。

---

## 玩家手动重置数据

> 用户可手动重置自己的持久化数据(用于"重开"或修复)

| 方式 | 步骤 |
|------|------|
| **VRChat 客户端 - 单个 World** | 主菜单 → World → "Reset User Data"(仅当有数据时显示) |
| **VRChat 客户端 - 所有 World** | 设置 → Debug → User Data → Reset All User Data |
| **VRChat 网站 - 单个 World** | World 页面 → Persistent Data → Reset |
| **VRChat 网站 - 所有 World** | 设置 → Persistent Data → Reset All User Data |

> **不可逆**:重置后无法恢复。

### 创作者提供"重置"功能

```csharp
public void ResetAllMyData() {
    if (!Networking.IsOwner(Networking.LocalPlayer, gameObject)) return;
    
    // PlayerData: 用 Set 覆盖(无法删除)
    PlayerData.SetInt(Networking.LocalPlayer, "Game-Score", 0);
    PlayerData.SetInt(Networking.LocalPlayer, "Game-Level", 0);
    // ... 覆盖所有你的 key
    
    // PlayerObject: 重置 [UdonSynced] 字段
    // 然后 RequestSerialization()
}
```

---

## 压缩 vs 性能的权衡

### 优先压缩的数据

| 数据类型 | 压缩效果 | 建议 |
|---------|---------|------|
| 大量重复字符串(成就、物品名) | 极佳(95%+) | ✅ 放心存 |
| 大量零值(byte[]/Vector3[]) | 极佳(90%+) | ✅ 放心存 |
| JSON 数组(结构重复) | 好(50%+) | ✅ 推荐 |
| 唯一 UUID | 差(5%-) | ❌ 优先用 int ID |
| 高熵随机数据(密码学) | 差(0%) | ❌ 几乎不压缩 |

### 性能优化(写入时)

```csharp
// 用 byte[] + UTF8 替代 string
public static byte[] StringToBytes(string s) {
    return System.Text.Encoding.UTF8.GetBytes(s);
}

public static string BytesToString(byte[] b) {
    return System.Text.Encoding.UTF8.GetString(b);
}
```

---

## 配额监控最佳实践

```csharp
public class PlayerDataQuotaMonitor : UdonSharpBehaviour {
    private const float WARN_THRESHOLD = 0.9f;
    private const float UPDATE_INTERVAL = 30f;  // 30 秒检查一次
    private float _lastUpdate = 0;
    
    void Update() {
        if (Time.time - _lastUpdate < UPDATE_INTERVAL) return;
        _lastUpdate = Time.time;
        
        // 异步刷新用量
        Networking.LocalPlayer.RequestStorageUsageUpdate();
    }
    
    public override void OnPersistenceUsageUpdated(VRCPlayerApi player) {
        if (player != Networking.LocalPlayer) return;
        
        int dataUsed = player.GetPlayerDataStorageUsage();
        int dataLimit = player.GetPlayerDataStorageLimit();
        int objUsed = player.GetPlayerObjectStorageUsage();
        int objLimit = player.GetPlayerObjectStorageLimit();
        
        if ((float)dataUsed / dataLimit > WARN_THRESHOLD) {
            ShowWarningUI($"PlayerData: {dataUsed}/{dataLimit} bytes");
        }
        if ((float)objUsed / objLimit > WARN_THRESHOLD) {
            ShowWarningUI($"PlayerObject: {objUsed}/{objLimit} bytes");
        }
    }
    
    private void ShowWarningUI(string msg) {
        Debug.LogWarning(msg);
        // 可选:显示 UI 提示
    }
}
```

---

## 相关知识库

- `memory/api/persistence.md` - API 速查
- `memory/patterns/late-joiner-state-restore.md` - Late Joiner 状态恢复
- `memory/patterns/manual-sync-state.md` - Manual Sync 模式
- `memory/patterns/bit-packed-flags.md` - 位域压缩同步
- `memory/world/udon/networking/performance.md` - 网络性能优化
- `memory/world/udon/event-execution-order.md` - 事件时序
- `memory/sources/clientsim.md` - ClientSim 调试
