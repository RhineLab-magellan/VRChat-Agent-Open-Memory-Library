# Sardinal — 知识库溯源

> **类型**: Udon 沙箱适配 / 通用消息系统（Pub/Sub with parameters）
> **Tier**: A (作者活跃维护 + VPM 官方分发 + 高质量源码)
> **仓库**: https://github.com/ikuko/Sardinal
> **作者**: [@ikuko](https://x.com/magi_ikuko) (HoshinoLabs)
> **License**: MIT (2024)
> **VPM 仓库**: `https://vpm.hoshinolabs.com/vpm.json`
> **包名**: `com.hoshinolabs.sardinal`
> **最后查看**: 2026-06-20
> **SDK 版本**: VRChat SDK 3.10.x / UdonSharp 1.x / Unity 2022.3+
> **依赖**: `com.hoshinolabs.sardinject` (HoshinoLabs 自家 DI 容器)

---

## 项目概述

Sardinal 是 HoshinoLabs 推出的**通用消息总线（Pub/Sub with parameters）**，专为 Unity C# 和 VRChat UdonSharp 设计。

它**不是包装某个 Unity 现有系统**（与同作者的 ULocalization 包装 Unity Localization 不同），而是**从零实现了一个完整的事件系统**，让 Udon 行为之间能以"主题 + 参数"形式解耦通信。

**核心创新**：
- 在 Udon 端实现了 **类型安全**的 Pub/Sub（Type.FullName MD5 哈希作主题 ID）
- 支持**频道过滤**（同一主题下多组订阅者可独立响应）
- 支持**编译期 + 运行时双订阅模式**（场景常驻 + 动态生成）
- **16 个 Publish 重载**（0~15 参数，绕开 `SendCustomEvent` 无参限制）
- **基类订阅者自动继承**（`Concat(BaseType?.GetSubscriberSchemas())`）

---

## 项目规模

| 指标 | 数值 |
|------|------|
| 总 .cs 文件 | 36 |
| Runtime 文件 | 10 |
| Runtime/Udon 文件 | 11 |
| Editor/Udon 文件 | 14 |
| Shim 字段数 | **10** (`_0` ~ `_9`) |
| Publish 重载数 | **16** (arg0 ~ arg15) |
| Subscriber 特性参数数 | 2 (Topic + 可选 Channel) |
| 同步模式 | `BehaviourSyncMode.None` |

**与同作者 ULocalization 对比**：

| 维度 | Sardinal | ULocalization |
|------|----------|---------------|
| 总 .cs | 36 | 145 |
| Shim 字段 | 10 | 27 |
| 槽位数 | 16 (Publish 重载) | 3 (Slot) |
| 主题数 | 无限（动态哈希） | 有限（16 IVariable + 5 LocalizeEvent） |
| 复杂度 | ⭐⭐ 中 | ⭐⭐⭐⭐⭐ 高 |
| 依赖 | Sardinject | Unity Localization + Sardinal + Sardinject |

> Sardinal 是 **ULocalization 的"精简版 + 通用化"**：同样的 5 大沙箱适配模式 + Sardinject + God Shim，但**聚焦消息系统**而非本地化系统。

---

## 核心功能

1. **类型安全 Pub/Sub**：`Signal<TopicType>` + `[Subscriber(typeof(MySignal))]`
2. **频道路由**：同主题下多组订阅者（`[Subscriber(typeof(X), "UI")]` vs `[Subscriber(typeof(X), "Audio")]`）
3. **16 参数 Publish**：0~15 个 `object` 参数（编译期重载）
4. **静态订阅**：场景常驻对象自动注册（Editor 端反射）
5. **动态订阅**：运行时 `signal.Subscribe(this)` / `signal.Unsubscribe(this)`
6. **基类继承**：抽象基类订阅者方法被子类自动继承
7. **网络能力标记**：`_6` 字段已存 `[NetworkCallable]` 标志（待完善网络分派）

---

## 关键学习点

### 1. Hash-Based Method Dispatch（与 ULocalization 同源，但更精简）

Udon 没有委托/函数指针，Sardinal 用 `MD5(Type.FullName)` 作为主题 ID，运行时 `Array.IndexOf` 查表。比 ULocalization 的 500+ hash 方法精简得多 —— Sardinal 只需 hash **类型**，不需要 hash **方法**。

→ 沉淀到 `memory/patterns/hash-based-dispatch.md`（变体，10-字段版）

### 2. Slot-Based Parameter Passing（16 槽位变体）

`SendCustomEvent` 不支持参数，Sardinal 用 **16 个 `Publish` 重载**（每个 `params object[]`），运行时通过 `SetProgramVariable` 传参。比 ULocalization 的 3 object 槽位**数量更多但模式相同**。

→ 沉淀到 `memory/patterns/slot-parameter-passing.md`（变体，16-参数版）

### 3. Code Generation with Type Erasure（10 字段变体）

Udon 没有泛型，Sardinal 用 Sardinject 注入 **10 个 `object[]` / `string[]` / `int[]` 字段**（`_0`~`_9`）作为统一存储。比 ULocalization 的 27 字段**精简 60%**。

→ 沉淀到 `memory/patterns/code-generation-type-erasure.md`（变体，10-字段版）

### 4. Build-Time vs Runtime Separation（同 ULocalization 模式）

Editor 端用 C# 反射 + Sardinject 注入 10 字段到 Udon Shim；Runtime 端仅做 O(1) 数组查表。

→ 沉淀到 `memory/patterns/build-time-vs-runtime-separation.md`（变体，更精简的 10 字段版）

### 5. IID Object Identity（部分使用）

Udon 不能用 Dictionary 索引对象，Sardinal 用 `GetUdonTypeID()`（long）+ `long[] _2` 做 Udon Type 索引，但不像 ULocalization 那样用 IID 跨 Build 引用 —— Sardinal 是**单 Build 内**使用。

→ 沉淀到 `memory/patterns/iid-object-identity.md`（变体，Udon Type ID 版）

### 6. 🆕 Channel-Based Pub/Sub Routing（频道路由）⭐S NEW

同一信号下，多组订阅者可按频道过滤：

```csharp
[Subscriber(typeof(EnemyKilled), "UI")]      // UI 频道
public void OnEnemyKilledUI(Enemy e) { ... }

[Subscriber(typeof(EnemyKilled), "Audio")]   // Audio 频道
public void OnEnemyKilledAudio(Enemy e) { ... }

// 发布时可选频道
signal.WithChannel("UI").Publish(enemy);     // 只触发 UI
signal.Publish(enemy);                        // 触发所有（频道=null）
```

→ 沉淀到 `memory/patterns/channel-routing.md`（**Sardinal 独有**）

### 7. 🆕 Inherited Subscriber（基类订阅者自动继承）⭐S NEW

```csharp
public abstract class BaseEnemy : UdonSharpBehaviour {
    [Subscriber(typeof(GameOver))]
    public virtual void OnGameOver() { /* 默认实现 */ }  // 子类自动继承
}

public class Goblin : BaseEnemy {  // 无需重写 OnGameOver
    // OnGameOver 自动注册
}
```

通过 `Concat(self.BaseType?.GetSubscriberSchemas())` 递归扫描基类。

→ 沉淀到 `memory/patterns/inherited-subscriber.md`（**Sardinal 独有**）

### 8. 🆕 Hybrid Static+Dynamic Subscription（双订阅模式）⭐S NEW

| 模式 | 触发时机 | 实现 |
|------|----------|------|
| **静态订阅** | 场景加载时（Editor 反射） | `_9` 数组中预填充的 `IUdonEventReceiver` |
| **动态订阅** | 运行时 `signal.Subscribe(this)` | `_7[i]++` + `Array.Copy` 扩容 |

适用：场景常驻对象（静态）+ 容器/Pool 动态生成（动态）混合场景。

→ 沉淀到 `memory/patterns/hybrid-subscription-modes.md`（**Sardinal 独有**）

### 9. Sardinject 强依赖（DI 容器集成）

通过 `[Inject, SerializeField, HideInInspector]` 属性，Sardinject 在 Build 阶段自动注入 10 字段。这是 Sardinal 能"零反射运行"的关键。

---

## 关键代码骨架（去项目化）

### 1. 主题签名构造

```csharp
// 编译期：MD5(Type.FullName) + "__" + Param1.FullName + "__" + Param2 ...
var signature = $"{topic.FullName.ComputeHashMD5()}.";
foreach (var p in method.GetParameters()) {
    signature += $"__{p.ParameterType.FullName.Replace(".", "")}";
}
// 示例: "5d41402abc4b2a76b9719d911017c592.__SystemString"
```

### 2. Publish 路径（运行时热路径）

```csharp
// O(args) 拼 topic + O(subscribers) 数组 IndexOf + O(receivers) SetProgramVariable
internal void Publish(string topic, object channel, params object[] args) {
    // 1. 用参数运行时类型拼出完整 topic
    for (var i = 0; i < args.Length; i++) {
        var id = args[i] is UdonSharpBehaviour usb
            ? usb.GetUdonTypeName()
            : args[i].GetType().FullName;
        topic += $"__{id.Replace(".", "")}";
    }
    // 2. 数组 IndexOf 找匹配主题
    var idx = Array.IndexOf(_1, topic);
    if (idx < 0) return;  // 无订阅者，静默退出
    // 3. 遍历该主题的所有订阅者，过滤频道
    for (var i = 0; i < _7[idx]; i++) {
        if (channel != null && _8[idx][i] != null && !_8[idx][i].Equals(channel))
            continue;
        // 4. SetProgramVariable 传参
        for (var j = 0; j < args.Length; j++)
            _9[idx][i].SetProgramVariable(_4[idx][j], args[j]);
        // 5. SendCustomEvent 触发
        _9[idx][i].SendCustomEvent(_3[idx]);
    }
}
```

### 3. 动态订阅（O(n) 扩容）

```csharp
internal void Subscribe(string topic, object channel, UdonSharpBehaviour subscriber) {
    var udonId = subscriber.GetUdonTypeID();
    var receiver = (IUdonEventReceiver)(object)subscriber;
    for (var i = 0; i < _0; i++) {
        if (_2[i] != udonId) continue;          // 1. Type 匹配
        if (!_1[i].StartsWith(topic)) continue; // 2. 主题匹配
        if (Array.IndexOf(_9[i], receiver) >= 0) continue;  // 3. 防重复
        // 4. 扩容：count+1 + 数组拷贝
        var newCount = _7[i] + 1;
        var newChannels = new object[newCount];
        Array.Copy(_8[i], newChannels, _7[i]);
        newChannels[_7[i]] = channel;
        _8[i] = newChannels;
        // 5. 同步扩容 _9 数组
        var newReceivers = new IUdonEventReceiver[newCount];
        Array.Copy(_9[i], newReceivers, _7[i]);
        newReceivers[_7[i]] = receiver;
        _9[i] = newReceivers;
        _7[i] = newCount;
    }
}
```

### 4. 基类订阅者继承（Editor 端）

```csharp
// Editor: TypeExtensions.cs
public static SubscriberSchema[] GetSubscriberSchemas(this Type self) {
    return self.GetMethods(BindingFlags.DeclaredOnly | BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
        .Where(x => x.IsDefined(typeof(SubscriberAttribute), false))
        .Select(x => x.ToSubscriberSchema(self))
        .Concat(self.BaseType?.GetSubscriberSchemas() ?? Array.Empty<SubscriberSchema>())  // 关键
        .ToArray();
}
```

### 5. 频道路由（运行时）

```csharp
// Publish 时
if (channel != null && _8[idx][i] != null && !_8[idx][i].Equals(channel))
    continue;  // 频道不匹配则跳过

// Subscribe 时
[Subscriber(typeof(MySignal), "UI")]
public void HandleUI(...) { ... }
```

---

## 知识提取记录（反向索引）

| 沉淀位置 | 提取内容 |
|----------|----------|
| `memory/FACT.md` § Sardinal(参考工程) | 5 核心模式摘要 + 3 个新模式 + 8 字段工程参数 + 与 ULocalization 对比 |
| `memory/patterns/hash-based-dispatch.md` | 变体：10 字段版 + 16 参数 Publish（更精简） |
| `memory/patterns/slot-parameter-passing.md` | 变体：16-参数 Publish 重载（vs ULocalization 3 槽位） |
| `memory/patterns/code-generation-type-erasure.md` | 变体：10 字段注入（vs ULocalization 27 字段） |
| `memory/patterns/build-time-vs-runtime-separation.md` | 变体：10 字段 + 编译期 `Array.IndexOf` 查表 |
| `memory/patterns/iid-object-identity.md` | 变体：Udon Type ID + `long[] _2` |
| `memory/patterns/channel-routing.md` ⭐S NEW | Sardinal 独有：频道过滤 |
| `memory/patterns/inherited-subscriber.md` ⭐S NEW | Sardinal 独有：基类订阅者自动继承 |
| `memory/patterns/hybrid-subscription-modes.md` ⭐S NEW | Sardinal 独有：静态+动态双订阅 |
| `memory/sources/open-source-projects.md` | A9 案例研究型参考工程条目 |
| `memory/sources/index.md` | 新来源登记 |
| `memory/patterns/index.md` | 29-31 号新模式 + 决策树更新 + 速查表 |
| `memory/journal/sessions/2026-06-20_session_sardinal-analysis.md` | Session 记录 |

---

## 元数据

| 字段 | 值 |
|------|-----|
| **Stars** | 100+ (仅本文件保留，不外流) |
| **License** | MIT |
| **依赖** | com.hoshinolabs.sardinject |
| **维护状态** | 活跃（VPM 分发 + GitHub Releases） |
| **首次分析** | 2026-06-20 |
| **最后更新** | 2026-06-20 |
| **分析覆盖** | 36/36 .cs 文件 + README + LICENSE 100% 深度阅读 |

---

## 相关项目

| 项目 | 关系 |
|------|------|
| `HoshinoLabs ULocalization` | 同作者同思想，但聚焦**包装 Unity Localization**；Sardinal 聚焦**通用消息总线** |
| `HoshinoLabs Sardinject` | Sardinal 的 DI 容器依赖，被 Sardinal 用于 `[Inject]` 注入 10 字段 |
| `VRChat SDK` | 消费 `UdonSharpBehaviour` + `IUdonEventReceiver` + `SetProgramVariable` |
| `UdonSharp` | 消费 `[UdonBehaviourSyncMode]` + `BehaviourSyncMode.None` |

---

## 借鉴点总览

| 借鉴点 | 如何借鉴到自己的项目 |
|--------|---------------------|
| **MD5 主题 ID** | 任何需要"类型安全事件路由"的 Udon 项目 |
| **10 字段 SoA 注入** | 任何"在 Editor 预处理、Runtime 查表"的场景 |
| **频道路由** | 多模块订阅同一信号需差异化响应的场景 |
| **基类订阅者** | 抽象基类需要"统一事件处理"的场景 |
| **静态+动态双订阅** | 混合"场景常驻 + 运行时生成"对象的场景 |
| **Sardinject 依赖** | 复杂 Udon 项目应引入 DI 容器 |
| **God Shim 模式** | 与 ULocalization 一致，单一入口持有所有数据 |

---

## 与其他参考工程的模式重叠

| 模式 | ULocalization (A8) | Sardinal (A9) | 差异 |
|------|---------------------|---------------|------|
| Hash-Based Method Dispatch | 500+ 方法 hash | **类型** hash | Sardinal 更精简 |
| IID Object Identity | Editor IID + int | Udon Type ID + long | Sardinal 跨 Build 不稳定 |
| Slot-Based Parameter Passing | 3 object 槽位 | **16 Publish 重载** | Sardinal 参数更多但 boilerplate 多 |
| Code Generation with Type Erasure | 27 字段 | **10 字段** | Sardinal 精简 60% |
| Build-Time vs Runtime Separation | 完整 | 完整 | 模式相同，工程量更小 |
| **频道路由** | ❌ 无 | ✅ 有 | Sardinal 独有 |
| **基类继承** | ❌ 无 | ✅ 有 | Sardinal 独有 |
| **双订阅模式** | ❌ 无 | ✅ 有 | Sardinal 独有 |

> **关键洞察**：Sardinal 不是 ULocalization 的"子集"，而是**同思想的不同表达**。Sardinal 更聚焦、更精简，但额外贡献了 3 个新模式（频道、继承、双订阅）。
