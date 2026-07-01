---
title: "Channel-Based Pub/Sub Routing (频道路由)"
category: patterns
knowledge_level: applied
status: active
source: Sardinal(参考工程)
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - patterns
  - patterns
  - constraint
  - audio
aliases:
  - "Channel-Based Pub/Sub Routing (频道路由)"
  - channel-routing
related:
  - "sources/sardinal.md"
  - "patterns/inherited-subscriber.md"
  - "patterns/hybrid-subscription-modes.md"
  - "patterns/slot-parameter-passing.md"
  - FACT.md
---
# Pattern: Channel-Based Pub/Sub Routing (频道路由)

> SDK Version: 3.10.x
> Last Verified: 2026-06-20
> Reference: `memory/sources/sardinal.md`
> 来源标注: ⭐S (Sardinal 独有模式)

---

## Problem / Context

在 Pub/Sub 消息系统中，**同一信号可能被多组订阅者需要差异化处理**：

- UI 订阅者需要"按钮变色"
- Audio 订阅者需要"播放音效"
- Network 订阅者需要"转发给其他玩家"

**传统方案**：
- ❌ 定义多个信号（`UI_EnemyKilled` / `Audio_EnemyKilled`）→ 维护成本高、调用方需选错
- ❌ 所有订阅者全部触发 + 在方法内 `if (channel == "UI")` → 散落判断、性能浪费
- ❌ 用 Dictionary 索引 channel → Udon 不支持 Dictionary

Sardinal 场景：`EnemyKilled` 事件需要 4 个模块独立响应（UI / Audio / 成就 / 统计），但每个模块只关心自己那一份。

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| 无 `Dictionary<object, T>` | 无法用 channel 作 key 索引 |
| 无泛型委托 | 无法 `Action<ChannelType>` 区分 |
| 无运行时类型检查 | 频道比较需用 `object.Equals`（值类型装箱） |

---

## Solution

**核心思想**：在 `[Subscriber]` 特性上加可选的 `object Channel` 参数，Publish 时可选 `WithChannel(...)`，运行时按 channel 过滤。

### 关键机制

#### 1. Subscriber 特性支持可选 channel

```csharp
// SubscriberAttribute.cs
[AttributeUsage(AttributeTargets.Method, AllowMultiple = false, Inherited = false)]
public sealed class SubscriberAttribute : Attribute {
    public readonly Type Topic;
    public readonly object Channel;  // 可选

    public SubscriberAttribute(Type topic, object channel = null) {
        Topic = topic;
        Channel = channel;
    }
}
```

#### 2. Subscriber 标记时声明所属 channel

```csharp
public class UISystem : UdonSharpBehaviour {
    [Subscriber(typeof(EnemyKilled), "UI")]
    public void OnEnemyKilledUI(Enemy e) {
        // 更新血条、击杀计数
    }
}

public class AudioSystem : UdonSharpBehaviour {
    [Subscriber(typeof(EnemyKilled), "Audio")]
    public void OnEnemyKilledAudio(Enemy e) {
        // 播放击杀音效
    }
}

public class UniversalSystem : UdonSharpBehaviour {
    [Subscriber(typeof(EnemyKilled)]  // 无 channel = 接收所有
    public void OnEnemyKilledUniversal(Enemy e) {
        // 统计、成就、日志（全部需要）
    }
}
```

#### 3. Publish 时可选指定 channel

```csharp
// SignalExtensions.cs: WithChannel
public static Signal WithChannel(this Signal self, object channel) {
    var _self = (object[])(object)self;
    _self[2] = channel;  // 频道存在 _self[2] 槽位
    return (Signal)(object)_self;
}

// 调用方
signal.WithChannel("UI").Publish(enemy);     // 只触发 UI
signal.Publish(enemy);                        // 触发所有（频道=null 广播）
```

#### 4. 运行时过滤（核心热路径）

```csharp
// SardinalShim.Publish
for (var i = 0; i < _7[idx]; i++) {
    // 关键：频道匹配检查
    if (channel != null && _8[idx][i] != null && !_8[idx][i].Equals(channel))
        continue;  // channel 不匹配则跳过
    // ... 触发
}
```

**过滤逻辑三态**：

| 发布方 channel | 订阅方 channel | 触发？ | 说明 |
|----------------|----------------|--------|------|
| `null` | `null` | ✅ | 广播模式，触发所有 |
| `null` | `"UI"` | ✅ | 广播模式也触发有 channel 的 |
| `"UI"` | `null` | ❌ | 订阅方未指定 channel = 接收所有，但发布指定 → 实际不匹配？**【待验证】** |
| `"UI"` | `"UI"` | ✅ | 精确匹配 |
| `"UI"` | `"Audio"` | ❌ | 频道不同 |

> ⚠️ **第 3 行的语义**：Sardinal 的代码逻辑是 `channel != null && _8[idx][i] != null && !Equals(channel)` —— 即当**发布方有 channel 但订阅方无 channel** 时，**不会触发**。这是 Sardinal 隐含的设计选择（"无 channel = 不接受定向广播"）。

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | Publisher 决定 channel |
| Source of Truth | Subscriber 特性 + Publish 时 channel 参数 |
| Sync Type | N/A（本地路由） |
| Synced Variables | 无（channel 是方法参数，不是状态） |
| Mutation Path | Publisher 调 `WithChannel(channel).Publish(...)` |
| Ownership Path | 无（与所有权无关） |
| Serialization Path | 无 |
| Receive Path | 频道匹配 → `SetProgramVariable` + `SendCustomEvent` |
| Late Joiner | 自动（订阅表在 Build 期固定） |
| Conflict Strategy | channel 唯一性（业务约束，框架不强制） |
| Bandwidth Budget | 0（纯本地路由） |
| Failure Mode | 发布/订阅 channel 字符串不匹配 → 静默失败 |

---

## Implementation Sketch

### 简化版：单 channel 字段

```csharp
// === Subscriber 特性 ===
[AttributeUsage(AttributeTargets.Method)]
public sealed class SubscriberAttribute : Attribute {
    public Type Topic { get; }
    public object Channel { get; }
    public SubscriberAttribute(Type topic, object channel = null) {
        Topic = topic; Channel = channel;
    }
}

// === Signal 类 ===
public class Signal {
    string topic;        // MD5 hash
    object channel;      // 可选频道

    public Signal WithChannel(object ch) {
        var s = new Signal { topic = topic, channel = ch };
        return s;
    }

    public void Publish(params object[] args) {
        // 1. 找匹配 topic 的订阅者
        var subscribers = GetSubscribers(topic);
        // 2. 频道过滤
        foreach (var sub in subscribers) {
            if (channel != null && sub.Channel != null && !sub.Channel.Equals(channel))
                continue;
            // 3. 触发
            sub.Target.SetProgramVariable(sub.ParamSymbol, args[0]);
            sub.Target.SendCustomEvent(sub.MethodSymbol);
        }
    }
}

// === 使用 ===
[Subscriber(typeof(EnemyKilled), "UI")]
public void OnUI(Enemy e) { /* ... */ }

signal.WithChannel("UI").Publish(enemy);  // 只触发 UI
signal.Publish(enemy);                     // 触发所有
```

---

## When To Use

✅ **适用**：
- 同一事件需多模块差异化响应（UI / Audio / Network / 成就）
- 模块边界清晰，channel 名稳定
- 频道数 ≤ 5-10（避免 hardcode 维护）

❌ **不适用**：
- 频道数 > 20 → 考虑拆成多个 Signal
- 频道内容是动态数据（如 `playerId`）→ 改用 `object` 引用（值类型会装箱）
- 频道需要运行时注册 → Udon 反射限制做不到

---

## 频道命名规范建议

| 模式 | 示例 | 适用 |
|------|------|------|
| **字符串常量** | `"UI"` / `"Audio"` | 简单场景，编译期固定 |
| **类引用** | `typeof(UISystem)` | 类型安全，编译期检查 |
| **枚举** | `Channel.UI` | 受 Udon Enum 限制（见 always-load Enum 5 陷阱） |

**Sardinal 用字符串** —— 因为 Udon Enum 有 5 大陷阱（ToString 输出数字、cast 不能与操作符写一起等），字符串是最稳的选择。

---

## 性能开销

| 阶段 | 开销 |
|------|------|
| 编译期 | 频道字符串存入 SubscriberSchema |
| Publish 时 | 1 次 `object.Equals` / 订阅者（值类型装箱 1 次） |
| 内存 | 每订阅者多 1 个 `object Channel` 引用（4-8 字节） |

> **对比全触发**：100 订阅者中只有 10 个匹配 channel → 节省 90 次 `SetProgramVariable` + `SendCustomEvent`（~5-10 µs / 次）

---

## 关键约束

| 约束 | 说明 |
|------|------|
| **频道比较是 `object.Equals`** | 值类型（int / enum）会装箱，慢 5-10 倍 |
| **频道字符串硬编码** | typo 不会编译期报错（运行时静默失败） |
| **频道语义不对称** | 发布方有 channel + 订阅方无 channel = 不触发（Sardinal 设计） |
| **无 channel 冲突检查** | 多个 Subscriber 用同 channel 是合法的 |

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **Sardinal** | `object Channel` + `WithChannel(...)` + `object.Equals` 过滤 | 完整 |
| 自建轻量 Pub/Sub | 字符串 channel + Dictionary（仅非 Udon） | 简化 |
| 业务硬编码 | `if (moduleType == "UI")` 写在 Subscriber 内 | ❌ 反例 |

---

## 关联文档

- `memory/sources/sardinal.md` — 项目溯源
- `memory/patterns/inherited-subscriber.md` — 配套基类继承
- `memory/patterns/hybrid-subscription-modes.md` — 配套双订阅模式
- `memory/patterns/slot-parameter-passing.md` — 配套参数传递（16 重载）
- `memory/FACT.md` § Sardinal
