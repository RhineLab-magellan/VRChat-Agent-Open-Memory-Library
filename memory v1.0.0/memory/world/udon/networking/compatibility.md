# Network Compatibility 跨版本兼容

> Type: WORLD / Udon API Reference
> Confidence: High
> Source: VRChat 官方 Creator Docs (Network Compatibility)
> SDK Version: 3.x
> Last Updated: 2026-06-15

---

## 简介

当你 **更新 World** 时,如果修改了同步对象的结构,**会与所有正在运行旧版本的实例不兼容**。这意味着使用旧版本的玩家会被强制踢出实例。

> ⚠️ **生产环境警告**:不兼容变更会导致活跃实例崩溃,所有用户必须重新加入。设计 World 时必须考虑版本演进。

---

## 不兼容触发条件

如果一个对象 **同时存在于新旧两个版本** 中,并且它同步了网络数据,则以下任一条件即触发不兼容:

| 条件 | 说明 | 示例 |
|------|------|------|
| ❌ 组件类型不匹配 | `UdonBehaviour` 上的组件类型不一致 | 添加/删除同步组件 |
| ❌ 组件数量不匹配 | 组件总数变化 | 增加新 `VRCObjectSync` |
| ❌ 组件顺序不匹配 | 同类组件在 Hierarchy 中的顺序不同 | 重新排序 `UdonBehaviour` |
| ❌ 变量类型不匹配 | 同一字段的类型变了 | `int` → `float` |
| ❌ 变量数量不匹配 | 同步变量数量变化 | 增加/删除 `[UdonSynced]` 字段 |
| ❌ 变量顺序不匹配 | 字段声明顺序变化 | 重新排列字段 |

### 哪些操作会破坏兼容?

| 操作 | 兼容性 | 原因 |
|------|-------|------|
| 添加新 `[UdonSynced]` 字段 | ❌ 不兼容 | 数量变化 |
| 删除 `[UdonSynced]` 字段 | ❌ 不兼容 | 数量变化 |
| 修改 `[UdonSynced]` 字段类型 | ❌ 不兼容 | 类型变化 |
| 重排字段声明顺序 | ❌ 不兼容 | 顺序变化 |
| 添加非同步变量 | ✅ 兼容 | 不参与序列化 |
| 修改方法实现 | ✅ 兼容 | 不影响变量结构 |
| 修改本地逻辑 | ✅ 兼容 | 纯行为变更 |

---

## 影响范围

当 World 触发不兼容时:

```
活跃实例运行旧版 World
  ↓
新玩家尝试加入
  ↓
检测到版本不兼容
  ↓
新玩家被强制踢出
  ↓
弹出通知:"The world is running an incompatible version"
  ↓
玩家必须确认通知,才能继续使用 VRChat
```

### 实例恢复

> **重要规则**:**当所有玩家离开实例后,实例变为非活跃状态**。此时如果有玩家重新加入,可以使用 **新版本** 而不触发不兼容问题。

**示例时间线**:

```
10:00 - 上传 World V1,10 名玩家加入
10:30 - 上传 World V2(包含不兼容变更)
10:31 - 新玩家尝试加入 → 被踢出(不兼容)
10:45 - 所有 V1 玩家离开,实例失效
10:50 - 玩家用 V2 重新加入 → 正常进入
```

---

## 兼容设计模式

### 模式 1:永远不删除变量

```csharp
// ❌ 错误:删除旧变量
public class Weapon : UdonSharpBehaviour {
    [UdonSynced] public int damage; // 删除会破坏兼容
}

// ✅ 正确:废弃但保留
public class Weapon : UdonSharpBehaviour {
    [System.Obsolete("Use baseDamage instead")]
    [UdonSynced] public int damage; // 保留字段,标 Obsolete
    
    [UdonSynced] public int baseDamage; // 新字段
}
```

### 模式 2:用位域添加布尔状态(代替新变量)

```csharp
// ❌ 错误:加新 bool
[UdonSynced] public bool isActive;     // V1
[UdonSynced] public bool isHidden;     // V2 - 数量变化,不兼容

// ✅ 正确:用位域
[UdonSynced] private byte _flags;     // V1: bit0=isActive
// V2 仍然用 _flags,但 bit1=isHidden(不增加变量)
```

### 模式 3:永远在末尾追加

```csharp
// ✅ 兼容的添加方式
public class Player : UdonSharpBehaviour {
    [UdonSynced] public int health;     // V1 字段 0
    [UdonSynced] public int score;      // V1 字段 1
    // V2 在末尾添加
    [UdonSynced] public int level;      // V2 字段 2
}
// 删除中间的字段(如 score)仍然不兼容
```

### 模式 4:数据类型扩展(可选)

```csharp
// ❌ 改变类型
[UdonSynced] public int damage;        // V1: int
[UdonSynced] public float damage;      // V2: float - 不兼容

// ✅ 使用更大的类型
[UdonSynced] public int damage;        // V1: int
[UdonSynced] public long damage;       // V2: long - 仍然不兼容(类型变了)
```

> **结论**:数据类型一旦确定,不能改变;不要尝试"先小后大"的扩展。

### 模式 5:重命名但保持类型和顺序

```csharp
// ⚠️ 风险:重命名
[UdonSynced] public int a;             // V1
[UdonSynced] public int b;             // V2 (重命名 a→b)
```

VRChat 序列化基于 **字段声明顺序**,不基于名称。重命名不影响兼容性(只要类型不变)。

---

## 版本演进策略

### 阶段 1:规划字段

```csharp
[UdonSynced] private int _version;     // 预留给未来扩展
[UdonSynced] private int _coreData;     // 当前数据
[UdonSynced] private byte _flags;       // 预留给位扩展
[UdonSynced] private int _reserved1;    // 预留
[UdonSynced] private int _reserved2;    // 预留
```

> **核心思想**:**预留字段 + 位域扩展**,把不兼容变更压缩到接近零。

### 阶段 2:发布前验证

在上传 World 前,自问:

| 检查项 | 答案 |
|-------|------|
| 是否新增了 `[UdonSynced]` 字段? | → 不兼容 |
| 是否修改了 `[UdonSynced]` 字段类型? | → 不兼容 |
| 是否重排了字段声明顺序? | → 不兼容 |
| 是否只添加了普通 `[SerializeField]`? | → 兼容 ✅ |
| 是否只修改了方法体实现? | → 兼容 ✅ |

### 阶段 3:灰度发布

```
1. 上传到 Private 测试世界 → 测试
2. 部署到 Public,观察前 24 小时
3. 如发现问题,准备 "兼容补丁":
   - 旧版玩家强制升级
   - 新版 World 自动检测旧版活跃实例
```

---

## 兼容性检查工具

| 工具 | 用法 |
|------|------|
| **VRChat SDK Control Panel** | 上传前显示字段结构 |
| **Unity Console** | 编译时警告字段变化 |
| **World Debug Views** | 运行时检查对象 sync 状态 |
| **ClientSim(Editor)** | 本地模拟多个版本 |

---

## 平台变体(Platform Variants)

> ⚠️ **重要**:PC 和 Quest 平台的 World **必须保持同步结构**。如果 PC 版本新增变量,Quest 版本必须同步更新,否则玩家跨平台时会看到不一致。

```csharp
// PC/Quest 必须保持字段一致
[UdonSynced] public Vector3 position;
// 不要在 #if UNITY_ANDROID 中移除
```

---

## 兼容性与 Late Joiner 的关系

| 场景 | Late Joiner 表现 |
|------|----------------|
| 新玩家加入运行中的 V1 实例 | 收到 V1 同步状态 |
| 新玩家加入运行中的 V2 实例 | 收到 V2 同步状态 |
| V1 实例 + V2 World 上传 | 新玩家被踢出 |
| V1/V2 混用(灰度) | ❌ 不允许,VRChat 不支持混版本实例 |

---

## 风险与陷阱

| 风险 | 严重度 | 缓解 |
|------|-------|------|
| 生产环境误触发不兼容 | 🔴 Critical | 永远在 Private 测试世界验证 |
| 字段顺序误调整 | 🟠 High | 使用 IDE 的"格式化"按钮前先备份 |
| Quest 平台不匹配 | 🟠 High | 平台变体必须同步字段 |
| 删字段导致旧版崩溃 | 🔴 Critical | 永远标 Obsolete 而非删除 |
| 跨版本数据残留 | 🟡 Medium | 文档化字段生命周期 |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/variables.md` | UdonSynced 字段定义 |
| `memory/world/udon/networking/events.md` | Network Events(同样受兼容约束) |
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/api/networking.md` | API 速查 |
