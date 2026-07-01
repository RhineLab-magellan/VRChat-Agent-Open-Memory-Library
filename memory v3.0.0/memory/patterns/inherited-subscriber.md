---
title: "Inherited Subscriber (基类订阅者自动继承)"
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
  - event
  - udonsharp
aliases:
  - "Inherited Subscriber (基类订阅者自动继承)"
  - inherited-subscriber
related:
  - "sources/sardinal.md"
  - "patterns/channel-routing.md"
  - "patterns/hybrid-subscription-modes.md"
  - "patterns/build-time-vs-runtime-separation.md"
  - FACT.md
---
# Pattern: Inherited Subscriber (基类订阅者自动继承)

> SDK Version: 3.10.x
> Last Verified: 2026-06-20
> Reference: `memory/sources/sardinal.md`
> 来源标注: ⭐S (Sardinal 独有模式)

---

## Problem / Context

在面向对象设计中，**抽象基类常需要定义"通用行为"**：

```csharp
public abstract class BaseEnemy : UdonSharpBehaviour {
    // 问题：基类的 OnDamage 方法如何自动被所有子类订阅？
    public virtual void OnDamage(float amount) { /* 默认扣血逻辑 */ }
}

public class Goblin : BaseEnemy { /* 100 个子类 */ }
public class Dragon : BaseEnemy { /* ... */ }
```

传统 .NET 中可用 `event += handler`，但 **Udon 沙箱**：
- ❌ 无 `event` / `delegate`
- ❌ 无虚方法 dispatch（Udon 不支持 `override` + 反射调用）
- ❌ 无接口继承（Udon 接口限制多）

→ 业务需求："所有 `BaseEnemy` 子类都自动响应 `OnDamage` 事件"。

Sardinal 场景：抽象基类 `BaseCharacter` 定义 `OnGameOver` 订阅者方法，所有角色类（玩家/NPC/敌人）自动继承。

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| 无 `delegate` / `event` | 无法用 C# 事件机制 |
| 无虚方法动态分派 | 无法用 `virtual` + override |
| 无 `Type.GetMethods(BindingFlags.FlattenHierarchy)` | Udon 反射在运行时不可用，但 **Editor 反射可用** |
| 手动继承 attribute 需扫 `BaseType` | 框架需主动递归扫描 |

---

## Solution

**核心思想**：**Editor 端反射**扫描时，**递归扫描基类** 的 `[Subscriber]` 方法并入当前类的订阅表。

### 关键机制

#### 1. Editor 端递归扫描基类

```csharp
// Editor: TypeExtensions.cs
public static SubscriberSchema[] GetSubscriberSchemas(this Type self) {
    return self.GetMethods(
            BindingFlags.DeclaredOnly |   // 关键：只取本类声明的方法
            BindingFlags.Instance |
            BindingFlags.Public |
            BindingFlags.NonPublic
        )
        .Where(x => x.IsDefined(typeof(SubscriberAttribute), false))
        .Select(x => x.ToSubscriberSchema(self))
        .Concat(
            self.BaseType?.GetSubscriberSchemas() ?? Array.Empty<SubscriberSchema>()
        )  // 关键：递归基类
        .ToArray();
}
```

**关键点**：
- `BindingFlags.DeclaredOnly` 防止基类方法被重复包含（本类只查本类声明的）
- `self.BaseType?.GetSubscriberSchemas()` 递归向上收集
- 整条继承链都会合并到当前类的订阅表

#### 2. 抽象基类定义订阅者

```csharp
// Runtime: 抽象基类
public abstract class BaseCharacter : UdonSharpBehaviour {
    [Subscriber(typeof(GameOver))]
    public virtual void OnGameOver() {
        // 默认实现：所有角色共用的死亡逻辑
        Debug.Log($"{name} is game over");
    }
}
```

#### 3. 子类自动继承

```csharp
// Runtime: 子类无需重写
public class Player : BaseCharacter {
    // 继承自 BaseCharacter.OnGameOver，自动订阅 GameOver 主题
}

public class Goblin : BaseCharacter {
    // 同样自动订阅
}

public class Dragon : BaseCharacter {
    public override void OnGameOver() {
        // 可选：override 覆盖基类实现
        // 注意：Sardinal 当前实现是按方法签名查找，override 后方法仍会注册
    }
}
```

#### 4. 发布时所有子类响应

```csharp
// 任意发布点
signal.Publish();  // 所有 Player / Goblin / Dragon 都会调用 OnGameOver
```

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | Editor（编译期确定继承关系） |
| Source of Truth | `Type.BaseType` 反射链 |
| Sync Type | N/A（与网络无关） |
| Synced Variables | 无 |
| Mutation Path | 无（基类关系编译期固定） |
| Ownership Path | 无 |
| Serialization Path | 无 |
| Receive Path | 子类实例 `OnGameOver` 被 `SendCustomEvent` |
| Late Joiner | 自动（场景数据一致） |
| Conflict Strategy | 无（继承是单链） |
| Bandwidth Budget | 0 |
| Failure Mode | 反射中断（基类缺失）→ 静默丢失 |

---

## Implementation Sketch

### 简化版：3 层递归

```csharp
// === Editor 端：递归扫描 ===
public static SubscriberSchema[] GetSubscriberSchemas(Type t) {
    var schemas = new List<SubscriberSchema>();

    // 1. 本类声明的 [Subscriber] 方法
    foreach (var m in t.GetMethods(BindingFlags.DeclaredOnly | BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)) {
        var attr = m.GetCustomAttribute<SubscriberAttribute>();
        if (attr != null) {
            schemas.Add(new SubscriberSchema {
                Method = m,
                Topic = attr.Topic,
                DeclaringType = t,
            });
        }
    }

    // 2. 递归基类
    if (t.BaseType != null && t.BaseType != typeof(object)) {
        schemas.AddRange(GetSubscriberSchemas(t.BaseType));
    }

    return schemas.ToArray();
}
```

### 使用

```csharp
// 抽象基类
public abstract class BaseEnemy : UdonSharpBehaviour {
    [Subscriber(typeof(EnemyKilled)]  // 自动被所有子类继承
    public virtual void OnKilled() { /* ... */ }
}

// 子类
public class Goblin : BaseEnemy { /* 自动订阅 */ }
public class Dragon : BaseEnemy { /* 自动订阅 */ }

// 发布
signal.Publish();  // 所有 Goblin/Dragon 的 OnKilled 被调用
```

---

## When To Use

✅ **适用**：
- 抽象基类需要"统一事件处理"（如 `OnDeath` / `OnLevelUp` / `OnItemPickup`）
- 子类数量 ≥ 3（值得抽象）
- 业务逻辑是"默认实现 + 子类可选 override"

❌ **不适用**：
- 子类各自有完全不同的事件需求 → 不要用继承，用组合（每个类单独标 `[Subscriber]`）
- 继承链 > 5 层 → 反射成本高，且难以调试
- 需要"运行时切换基类" → Udon 不支持

---

## 关键约束

| 约束 | 说明 |
|------|------|
| **仅 Editor 反射有效** | Udon 运行时无反射，继承关系必须在编译期固定 |
| **同名方法 override 行为** | Sardinal 当前是按"方法签名"注册，override 后仍会注册（不会去重） |
| **基类订阅表 = 子类订阅表** | 子类不能"取消继承某个订阅者"，需通过 `override` + 显式判空 |
| **接口订阅不继承** | Sardinal 不支持接口订阅（仅类继承） |
| **多继承不支持** | C# 类只支持单继承 → 只能从一个基类继承订阅者 |

---

## 进阶：override 的处理

Sardinal 当前实现：

```csharp
// 基类
public class BaseEnemy {
    [Subscriber(typeof(GameOver))]
    public virtual void OnGameOver() { /* 基类实现 */ }
}

// 子类 override
public class Dragon : BaseEnemy {
    [Subscriber(typeof(GameOver))]
    public override void OnGameOver() { /* 子类实现 */ }  // 也被注册
}
```

**结果**：
- 反射时 `Dragon` 类会找到 2 个 `OnGameOver`（基类 + 子类）
- 都被注册到订阅表
- Publish 时**两个都会被调用**（基类先？子类先？**【未确认 Sardinal 行为】**）

**安全做法**：

```csharp
// 方案 1：子类不标 [Subscriber]，让基类负责
public class Dragon : BaseEnemy {
    public override void OnGameOver() {
        base.OnGameOver();  // 可选：调基类
        // 子类扩展逻辑
    }
}
```

→ 子类用 `override` 覆盖时**不重复标** `[Subscriber]`，避免重复注册。

---

## 与其他模式的关系

| 模式 | 关系 |
|------|------|
| **Template Method** | 同思想（基类定义骨架，子类扩展），但用反射实现而非虚方法 |
| **Channel Routing** | 可叠加：基类订阅者 + 子类不同 channel |
| **Hybrid Subscription** | 基类订阅者默认走静态模式 |

---

## 性能开销

| 阶段 | 开销 |
|------|------|
| 编译期反射 | 每继承链多扫 1 次 `Type.BaseType`（O(深度)） |
| 运行时 | 0 开销（与普通订阅者一样） |
| 内存 | 0 额外开销 |

> **几乎免费**——只在编译期多一次递归。

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **Sardinal** | `Concat(self.BaseType?.GetSubscriberSchemas())` 递归 | 完整 |
| 简单 .NET 事件总线 | `event` + 反射订阅 | 不同实现 |
| Unity MonoBehaviour | 虚方法 + override | Udon 不可用 |

---

## 关联文档

- `memory/sources/sardinal.md` — 项目溯源
- `memory/patterns/channel-routing.md` — 配套频道路由
- `memory/patterns/hybrid-subscription-modes.md` — 配套双订阅模式
- `memory/patterns/build-time-vs-runtime-separation.md` — 依赖 Editor 反射
- `memory/FACT.md` § Sardinal
