---
title: "Special Nodes | 特殊节点"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - udonsharp
aliases:
  - "Special Nodes | 特殊节点"
  - special-nodes
related:
  - index.md
  - event-nodes.md
  - graph-elements.md
  - searching-for-nodes.md
  - type-nodes.md
  - "api/networking.md"
  - "patterns/event-driven-state-machine.md"
---
# Special Nodes | 特殊节点

> 来源: https://creators.vrchat.com/worlds/udon/graph/special-nodes/

"Special" 类别包含**自定义变量、自定义事件、流程控制、与其他 UdonBehaviours 通信**的节点。

---

## 1. Block

**功能**: 将 Flow **分裂为多个段**。1 个 Flow 输入,多个 Flow 输出。**从上到下**依次执行所有右侧 Flow。

**适用场景**:
- 顺序执行多个独立操作
- 等价于 C# 中的语句序列

**对应 C#**:
```csharp
void Start() {
    DoA();
    DoB();
    DoC();
}
```

---

## 2. Branch

| 输入 | 类型 |
|------|------|
| `Bool` | `System.Boolean` |

**功能**: 根据条件分支执行。
- `Bool` = **True** → 执行 `True` 路径
- `Bool` = **False** → 执行 `False` 路径

**对应 C#**:
```csharp
if (condition) {
    // True path
} else {
    // False path
}
```

---

## 3. Comment(节点版本)

**功能**: 提供**评论字符串输入框**。**此字符串不参与编译**(纯 Graph 文档)。

> ⚠️ 与 `graph-elements.md` 中的 Graph Comment **不同** — 那是**放置在 Graph 任意位置的文本框**;此节点是**附加到节点上**的注释输入框(虽不编译,无运行时效果)。

---

## 4. Const Null

**功能**: 提供 **`null` 值**用于空检查。

---

## 5. Const This

**功能**: 提供**当前 UdonBehaviour 所在 GameObject** 的引用。

**对应 C#**:
```csharp
this.gameObject
```

---

## 6. Event Custom

| 输入 | 类型 |
|------|------|
| `name` | `System.String` |

**功能**: 自定义事件,可由 UdonBehaviour 节点触发。

**约束**:
- 必须在 Graph 中**输入名称**
- **程序运行时不能修改** Event 名称

**对应 C#(UdonSharp)**:
```csharp
public void MyCustomEvent() {
    // ...
}
```

---

## 7. For

| 输入 | 类型 | 说明 |
|------|------|------|
| `start` | `System.Int32` | 计数器**初始值** |
| `end` | `System.Int32` | 计数器**终止值**(不含) |
| `step` | `System.Int32` | 每次**增量** |
| `Body` | (Flow) | 循环体 |
| `Exit` | (Flow) | 循环结束后的下一个节点 |

| 输出 | 类型 |
|------|------|
| `index` | `System.Int32` | 当前计数器值 |

**执行流程**:
1. 计数器初始化为 `start`
2. 执行 `Body` Flow
3. 计数器 += `step`
4. 若计数器 `>= end`,执行 `Exit` Flow
5. 否则跳回 Body

**对应 C#**:
```csharp
for (int i = start; i < end; i += step) {
    // Body
}
```

---

## 8. Get Variable

| 输入 | 类型 |
|------|------|
| `name` | `System.String` |

| 输出 | 类型 |
|------|------|
| - | `System.Object` |

**功能**: 获取名为 `name` 的 Udon 变量值。

---

## 9. Set Variable

| 输入 | 类型 | 说明 |
|------|------|------|
| `name` | `System.String` | 变量名 |
| `value` | `System.Object` | 要设置的值 |
| `sendChange` | `Boolean` | 是否触发 `OnVariableChanged` 事件 |

**功能**: Flow 执行时设置变量。
- `sendChange` 勾选 → 同时触发该变量的 `OnVariableChanged` 事件
- 对**同步变量**也有效

---

## 10. Get Program Variable

| 输入 | 类型 |
|------|------|
| `instance` | `UdonBehaviour` |
| `symbolName` | `string` |

**功能**: 从**另一个 UdonBehaviour `instance`** 获取变量 `symbolName` 的值。

**最佳实践**:
- 目标 UdonBehaviour 是 **public 变量**且在 Inspector 中连接 → 可在**下拉菜单**中选择目标变量名
- 否则:用 `String const` 节点手动写入变量名

**未连接 `instance` 时**: 使用**当前 UdonBehaviour** 的变量名。

---

## 11. Set Program Variable

| 输入 | 类型 |
|------|------|
| `instance` | `UdonBehaviour` |
| `symbolName` | `string` |
| `value` | `Object` |

**功能**: 设置**另一个 UdonBehaviour `instance`** 的变量 `symbolName` 为 `value`。

**附加行为**: 会触发目标变量的 `OnVariableChanged` 事件。

**使用技巧**:
- 解耦子系统: 中央控制器 → `SetProgramVariable` → 子系统(多机位导演系统 已知模式,参考工程)
- 详见 `../../patterns/event-driven-state-machine.md`

---

## 12. On Variable Changed

| 输出 | 类型 | 说明 |
|------|------|------|
| `newValue` | (变量类型) | 新值 |
| `oldValue` | (变量类型) | 旧值 |

**触发时机**:
- `SetProgramVariable` 被调用
- `Set Variable` 节点 `sendChange` 勾选时
- **对同步变量也有效**(网络同步时触发)

---

## 13. While

| 输入 | 类型 |
|------|------|
| `Bool` | `System.Boolean` |

**执行流程**:
- `Bool` = **True** → 循环执行 `Body`
- `Bool` = **False** → 执行 `Exit` Flow

**对应 C#**:
```csharp
while (condition) {
    // Body
}
```

> **【风险】** While 循环无 `step`,**容易写成死循环**导致 Udon 帧卡死。请确保循环条件能退出。

---

## UdonBehaviour Nodes

> 用于与其他 UdonBehaviour 交互 — **本地**、**延迟**、或**网络**。

### UdonSharp 兼容性警告

> ⚠️ 以下节点**仅对 `public` 事件有效**。
> - **Udon Graph**: 自定义事件**始终是 public**
> - **UdonSharp**: 必须显式使用 `public` 而非 `private`

---

### 14. SendCustomEvent

| 输入 | 类型 |
|------|------|
| `instance` | `UdonBehaviour` |
| `eventName` | String |

**功能**: 在目标 UdonBehaviour 上**运行事件 `eventName`**。
- **`instance` 留空** → 指向**自身**的事件

**对应 C#**:
```csharp
// UdonSharp
targetUdon.SendCustomEvent("EventName");
```

---

### 15. SendCustomEventDelayedFrames

| 输入 | 类型 |
|------|------|
| `instance` | `UdonBehaviour` |
| `eventName` | String |
| `delayFrames` | int |
| `eventTiming` | EventTiming |

**功能**: 等待 `delayFrames` 帧后,运行事件 `eventName`。
- `eventTiming` 决定在哪个 Unity 阶段执行:`Update` / `LateUpdate` / `FixedUpdate` / `PostLateUpdate`
- **最小延迟 1 帧**

> ⚠️ **Timing 注意事项**:
> Unity 的 frame count 基于 **Update 事件**。如果在 Update 之前调用(如 `Start` 或 Input 事件),实际延迟可能**比预期少 1 帧**。

---

### 16. SendCustomEventDelayedSeconds

| 输入 | 类型 |
|------|------|
| `instance` | `UdonBehaviour` |
| `eventName` | String |
| `delaySeconds` | float |
| `eventTiming` | EventTiming |

**功能**: 等待 `delaySeconds` 秒后,运行事件 `eventName`。
- `eventTiming` 决定在哪个 Unity 阶段执行

> **`delaySeconds = 0` 的行为**: 事件将在**同一帧或下一帧**执行(参考 `SendCustomEventDelayedFrames` 说明)

---

### 17. SendCustomNetworkEvent

| 输入 | 类型 |
|------|------|
| `instance` | `UdonBehaviour` |
| `target` | NetworkEventTarget |
| `eventName` | String |

**功能**: 根据 `target` 在**远程玩家**上运行事件 `eventName`。
- **支持重载**用于传参

> 详细说明参见官方 **Network Events** 页面。

**对应 C#**:
```csharp
targetUdon.SendCustomNetworkEvent(NetworkEventTarget.All, "EventName");
```

> **【推断】** 带参版本在 UdonSharp 中需使用 `[NetworkCallable]` + `NetworkCalling.SendCustomNetworkEvent`(SDK 3.8.1+),详见 `../../api/networking.md`

---

## 流程控制节点汇总

| 节点 | 输入 | 输出 | 用途 |
|------|------|------|------|
| **Block** | 1 Flow | N Flow | 顺序执行 |
| **Branch** | Bool | True/False Flow | 条件分支 |
| **For** | start/end/step | index | 计数循环 |
| **While** | Bool | Body/Exit Flow | 条件循环 |
| **Const Null** | - | null | 空值 |
| **Const This** | - | GameObject | 自身引用 |
| **Event Custom** | name | Flow | 自定义事件 |

## 变量与通信节点汇总

| 节点 | 主要功能 |
|------|---------|
| **Get Variable** | 读取变量 |
| **Set Variable** | 写入变量(可选触发 OnChange) |
| **Get Program Variable** | 跨脚本读取 |
| **Set Program Variable** | 跨脚本写入(触发 OnChange) |
| **On Variable Changed** | 监听变量变化 |
| **SendCustomEvent** | 本地调用 |
| **SendCustomEventDelayedFrames** | 延迟帧调用 |
| **SendCustomEventDelayedSeconds** | 延迟秒调用 |
| **SendCustomNetworkEvent** | 网络调用 |

---

## 相关知识库

- [`index.md`](./index.md) — Udon Node Graph 主页
- [`event-nodes.md`](./event-nodes.md) — Event 节点
- [`graph-elements.md`](./graph-elements.md) — Graph 元素
- [`searching-for-nodes.md`](./searching-for-nodes.md) — 节点搜索
- [`type-nodes.md`](./type-nodes.md) — 类型引用节点
- `../../api/networking.md` — Networking(含 NetworkCallable)
- `../../patterns/event-driven-state-machine.md` — 状态机模式
