---
title: Udon 版主工具开发准则
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - networking

aliases:
  - "Udon 版主工具开发准则"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Udon 版主工具开发准则

> 来源:https://creators.vrchat.com/worlds/udon/udon-moderation-tool-guidelines/
> 本地化日期:2026-06-15
> 状态:FACT(知识库完整记录)

---

## ⚠️ 重要定位说明

VRChat 官方将 **Udon 版主工具的具体规则集中在 Creator Guidelines(创作者准则)的 Worlds 章节**。本节是入口,详细规则不重复发布。

> **🔴 关键原则:Udon 版主工具是"工具"而非"绕过手段"**

版主工具的设计目的是**辅助版主执行已存在的 VRChat 平台规则**,**不替代、也不绕过** VRChat 平台内置的版主系统。

---

## 一、设计原则(【推断】基于 Creator Guidelines 综合)

### 1.1 不绕过平台系统

| ❌ 禁止 | ✅ 允许 |
|---------|---------|
| 自行实现反作弊、封禁系统 | 调用 `VRC.SDKBase.VRCPlayerApi` 平台 API |
| 绕过 Instance 权限系统 | 使用 `Networking.IsMaster` 进行能力判断 |
| 实现账号验证 | 信任 VRChat 账号系统 |
| 隐藏/遮蔽版主行为 | 透明地提示玩家"你已被踢出" |

### 1.2 工具而非替代

- **辅助决策**:让版主更容易看到违规行为(报告按钮、证据收集)
- **不替代决策**:最终决策权在 VRChat 平台
- **不自动化禁令**:禁止自动踢人脚本(由版主手动触发)

### 1.3 数据隐私

| 原则 | 说明 |
|------|------|
| **不收集未公开数据** | 仅使用 `VRCPlayerApi.displayName` / `playerId` / `isMaster` 等公开 API |
| **不外传数据** | 玩家行为数据不应发送至外部服务器 |
| **不持久化隐私** | 避免 `PlayerData` 存储聊天内容、个人信息 |

---

## 二、推荐 API(白名单内)

### 2.1 玩家检测 API

```csharp
using VRC.SDKBase;

// 玩家存在性
bool exists = player != null;

// 玩家身份
int playerId = player.playerId;                    // 唯一 ID
string name = player.displayName;                  // 显示名
bool isMaster = player.isMaster;                   // 是否 Master
bool isInstanceOwner = player.isInstanceOwner;     // 是否 Instance Owner
bool isLocal = player.isLocal;                     // 是否本地玩家
```

### 2.2 玩家操作 API(Moderation)

| API | 用途 | 注意 |
|-----|------|------|
| `player.SetPlayerTag("tag")` | 标记玩家 | 仅本世界有效 |
| `player.EnablePickups(false)` | 禁用 Pickup | 临时控制 |
| `player.SetGravity(strength)` | 修改重力 | 物理沙盒工具 |
| `player.SetRunSpeed(speed)` | 修改移速 | 反作弊需谨慎 |
| `player.SetJumpImpulse(impulse)` | 修改跳跃 | 同上 |
| `player.SetWalkSpeed(speed)` | 修改行走 | 同上 |
| `player.TeleportTo(pos, rot)` | 强制传送 | "请去隔离区" |

### 2.3 触发流放(Limited 工具)

> **FACT**:Udon 没有直接"踢人" API。以下为间接实现:

```csharp
// 方式 1: 强制传送至游戏内"隔离区"
player.TeleportTo(quarantinePosition, quarantineRotation);

// 方式 2: 启用/禁用玩家组件
player.EnablePickups(false);
player.SetGravity(0);  // 飘起来无法移动

// 方式 3: 提示玩家自行离开
SendNotification("你已被本世界版主限制行动,请前往隔离区");
```

**【推断】实际踢人需通过:VRChat 平台用户举报系统**。

---

## 三、禁止模式

### 3.1 自动化禁令 ❌

```csharp
// ❌ 禁止:自动踢人
if (badWordDetected) {
    player.TeleportTo(quarantine, quarantine);
    player.SetGravity(0);
}

// ✅ 允许:标记 + 提示版主
if (badWordDetected) {
    player.SetPlayerTag("flagged_" + System.DateTime.Now);
    SendNotificationToMaster("玩家 " + player.displayName + " 检测到违规行为");
}
```

### 3.2 隐藏式监管 ❌

- 禁止"默默观察玩家"而玩家不知情
- 禁止"间谍模式" UI
- 必须有**透明提示**:"你正在被监控"

### 3.3 滥用 API ❌

| 滥用 | 说明 |
|------|------|
| 频繁调用 `SetPlayerTag` | 触发限流,可能影响其他玩家 |
| 对全实例广播敏感数据 | 增加网络负担 |
| 滥用 `PlayerData` | 跨世界数据,需严格区分 |

---

## 四、版主工具 UI 模式

### 4.1 Master 工具面板

```csharp
public class ModeratorPanel : UdonSharpBehaviour
{
    [SerializeField] private GameObject[] modMenus;  // 多个工具菜单
    [SerializeField] private VRCPlayerApi localPlayer;
    
    void Start()
    {
        localPlayer = Networking.LocalPlayer;
        // 初始隐藏所有菜单
        foreach (var menu in modMenus) menu.SetActive(false);
    }
    
    public override void OnPlayerTriggerEnter(Collider other)
    {
        if (!localPlayer.isMaster) return;  // 仅 Master 可触发
        // 显示工具菜单
    }
}
```

### 4.2 报告按钮模式

```csharp
public class ReportButton : UdonSharpBehaviour
{
    [SerializeField] private UdonSharpBehaviour modPanel;
    
    public void OnReportPressed()
    {
        // 仅在玩家自己选择时触发
        if (!localPlayer.isMaster) {
            Debug.Log("Only Master can report");
            return;
        }
        
        // 收集上下文(可选,避免隐私)
        var reported = modPanel.GetProgramVariable("targetPlayer");
        // ... 发送至版主日志
    }
}
```

---

## 五、与其他文档的关系

| 相关文档 | 用途 |
|----------|------|
| `memory/api/events-reference.md` | 完整 Udon 事件 API |
| `memory/api/networking.md` | Networking API |
| `memory/world/udon/using-build-test.md` | 测试版主工具 |
| VRChat Creator Guidelines (官方) | 完整规则定义 |

---

## 六、Missing Information

> **【未确认】** 以下信息需要查询 Creator Guidelines 完整文档:
>
> - 具体哪些 API 属于"版主工具白名单"
> - 自动化踢人是否被绝对禁止
> - PlayerData 在版主工具中的使用限制
>
> **建议**:实施前查阅 https://creators.vrchat.com/guidelines/

---

## 七、风险分级

| 风险 | 等级 | 说明 |
|------|------|------|
| 实现自动踢人脚本 | 🔴 严重 | 违反 Creator Guidelines |
| 滥用 `SetPlayerTag` | 🟡 中等 | 触发平台限流 |
| 隐藏式监管 UI | 🟡 中等 | 玩家投诉风险 |
| 不持久化隐私数据 | 🟢 低 | 最佳实践 |
| 仅 Master 可用工具 | 🟢 低 | 推荐模式 |
