# Pattern: Hybrid Static+Dynamic Subscription (静态+动态双订阅)

> Type: PATTERN
> Source: Sardinal(参考工程)
> Confidence: High
> SDK Version: 3.10.x
> Last Verified: 2026-06-20
> Reference: `memory/sources/sardinal.md`
> 来源标注: ⭐S (Sardinal 独有模式)

---

## Problem / Context

VRChat World 中，**Udon 对象的来源有 2 种**：

| 来源 | 时机 | 例子 |
|------|------|------|
| **场景常驻对象** | 场景加载时已存在 | 场景中的 NPC / 门 / 机关 / UI |
| **运行时生成对象** | 玩家交互后才存在 | Pool 出来的子弹 / 动态生成的敌人 / 容器中的 UI |

**痛点**：
- ❌ 只支持静态订阅：动态对象无法注册（实例化时错过扫描时机）
- ❌ 只支持动态订阅：场景常驻对象每次都手动 Subscribe 麻烦
- ❌ 两套 API 维护成本高

Sardinal 场景：场景里的 50 个 NPC（静态订阅）+ 玩家动态生成的 20 个 Pool 敌人（动态订阅），都需响应 `OnCombatEvent`。

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| 无运行时反射 | 静态订阅必须在 Editor 期"穷举"完成 |
| 无 `Instantiate` 引用稳定 | 动态对象每次 `new` 都是新引用，订阅表需手动管理 |
| 无 `FindObjectsOfType` 在 Udon | 动态对象不能反向查找订阅表 |

---

## Solution

**核心思想**：**静态订阅**靠 Editor 反射（场景加载时自动注册），**动态订阅**靠运行时 API（`Subscribe` / `Unsubscribe`）。两套共用同一个订阅表 + 同一套发布机制。

### 关键机制

#### 1. SardinalShim 双 10 字段设计

```csharp
// SardinalShim.cs
[Inject, SerializeField, HideInInspector] int _0;        // 总订阅主题数
[Inject, SerializeField, HideInInspector] string[] _1;   // 主题签名（MD5）
[Inject, SerializeField, HideInInspector] long[] _2;     // Udon TypeID
[Inject, SerializeField, HideInInspector] string[] _3;   // 方法符号
[Inject, SerializeField, HideInInspector] string[][] _4; // 参数符号
[Inject, SerializeField, HideInInspector] string[][] _5; // 参数类型
[Inject, SerializeField, HideInInspector] bool[] _6;     // Networked
[Inject, SerializeField, HideInInspector] int[] _7;      // ⭐ 动态订阅数（每主题独立计数）
[Inject, SerializeField, HideInInspector] object[][] _8; // 频道
[Inject, SerializeField, HideInInspector] IUdonEventReceiver[][] _9; // 接收者（含静态 + 动态）
```

**关键**：
- `_7[i]` 初始 = 静态订阅者数（Editor 注入）
- `_9[i]` 初始 = 静态订阅者列表
- 动态订阅时 `_7[i]++` + 数组扩容 + 把动态订阅者追加到 `_9[i]`

#### 2. 静态订阅（Editor 端一次性）

```csharp
// Editor: SardinalResolver.BuildSubscriberData
static SubscriberData[] BuildSubscriberData(Scene scene) {
    return subscriberSchema
        .SelectMany(schema => {
            return scene.GetRootGameObjects()
                .SelectMany(x => x.GetComponentsInChildren(schema.Type, true))  // 扫描场景
                .OfType<UdonSharpBehaviour>()
                .Select(x => UdonSharpEditorUtility.GetBackingUdonBehaviour(x))
                .Select(x => new SubscriberData(schema.Signature, x, schema.Channel, 0))
                .ToArray();
        })
        .ToArray();
}
```

→ 场景加载时（`SceneContainerBuilt` 钩子），所有 `UdonSharpBehaviour` + 类型匹配的 `[Subscriber]` 方法自动注册。

#### 3. 动态订阅（运行时 API）

```csharp
// SignalExtensions.cs
public static void Subscribe(this Signal self, UdonSharpBehaviour subscriber) {
    var _self = (object[])(object)self;
    var _sardinal = (SardinalShim)_self[0];
    var _topic = (string)_self[1];
    var _channel = _self[2];
    _sardinal.Subscribe($"{_topic}.", _channel, subscriber);  // 转发到 Shim
}

// SardinalShim.Subscribe
internal void Subscribe(string topic, object channel, UdonSharpBehaviour subscriber) {
    var udonId = subscriber.GetUdonTypeID();
    var receiver = (IUdonEventReceiver)(object)subscriber;
    for (var i = 0; i < _0; i++) {
        if (_2[i] != udonId) continue;             // 1. Type 匹配
        if (!_1[i].StartsWith(topic)) continue;     // 2. 主题匹配
        if (Array.IndexOf(_9[i], receiver) >= 0) continue;  // 3. 防重复

        // 4. 扩容：count+1 + 数组拷贝
        var newCount = _7[i] + 1;
        var newChannels = new object[newCount];
        Array.Copy(_8[i], newChannels, _7[i]);
        newChannels[_7[i]] = channel;
        _8[i] = newChannels;

        var newReceivers = new IUdonEventReceiver[newCount];
        Array.Copy(_9[i], newReceivers, _7[i]);
        newReceivers[_7[i]] = receiver;
        _9[i] = newReceivers;
        _7[i] = newCount;
    }
}
```

#### 4. 动态取消订阅

```csharp
// SardinalShim.Unsubscribe
internal void Unsubscribe(string topic, UdonSharpBehaviour subscriber) {
    var udonId = subscriber.GetUdonTypeID();
    var receiver = (IUdonEventReceiver)(object)subscriber;
    for (var i = 0; i < _0; i++) {
        if (_2[i] != udonId) continue;
        if (!_1[i].StartsWith(topic)) continue;

        var dest = Array.IndexOf(_9[i], receiver);
        if (dest < 0) continue;  // 未订阅

        // 移除：缩容 + 双数组拷贝
        var newCount = _7[i] - 1;
        var src = dest + 1;
        var length = newCount - dest;
        var newChannels = new object[newCount];
        Array.Copy(_8[i], 0, newChannels, 0, dest);
        Array.Copy(_8[i], src, newChannels, dest, length);
        _8[i] = newChannels;

        var newReceivers = new IUdonEventReceiver[newCount];
        Array.Copy(_9[i], 0, newReceivers, 0, dest);
        Array.Copy(_9[i], src, newReceivers, dest, length);
        _9[i] = newReceivers;
        _7[i] = newCount;
    }
}
```

#### 5. 统一发布（不区分静态/动态）

```csharp
// SardinalShim.Publish
internal void Publish(string topic, object channel, params object[] args) {
    // ... 找 idx
    for (var i = 0; i < _7[idx]; i++) {  // _7[idx] 包含静态 + 动态
        // ... 频道过滤
        // ... SetProgramVariable + SendCustomEvent
    }
}
```

→ **完全统一**：发布方不需知道订阅方是静态还是动态。

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | Editor 拥有静态，Runtime 拥有动态 |
| Source of Truth | `_7` 计数器 + `_8`/`_9` 数组 |
| Sync Type | N/A（本地） |
| Synced Variables | 无 |
| Mutation Path | Editor 注入（静态）+ `Subscribe` / `Unsubscribe`（动态） |
| Ownership Path | 无 |
| Serialization Path | 无 |
| Receive Path | `SendCustomEvent`（静态 + 动态都走同一路径） |
| Late Joiner | 静态自动（场景一致）；动态需手动 |
| Conflict Strategy | 防重复订阅（`Array.IndexOf`） |
| Bandwidth Budget | 0 |
| Failure Mode | 动态对象销毁时未 Unsubscribe → 死引用 + 内存泄漏 |

---

## Implementation Sketch

### 简化版：双模式订阅

```csharp
// === Subscriber 计数 + 数组 ===
int[] _subscriberCount;          // 每主题订阅数（含静态+动态）
object[][] _channels;            // 频道（可选）
IUdonEventReceiver[][] _subs;    // 接收者（含静态+动态）

// === 静态初始化（编译期）===
void InitStatic(UdonSharpBehaviour[] sceneObjs, string topic) {
    var count = sceneObjs.Length;
    _subscriberCount[topic] = count;  // 初始 = 静态数
    _channels[topic] = new object[count];
    _subs[topic] = new IUdonEventReceiver[count];
    for (var i = 0; i < count; i++) {
        _subs[topic][i] = (IUdonEventReceiver)sceneObjs[i];
    }
}

// === 动态订阅（运行时）===
public void SubscribeDynamic(string topic, UdonSharpBehaviour sub, object ch) {
    var newCount = _subscriberCount[topic] + 1;
    var newSubs = new IUdonEventReceiver[newCount];
    Array.Copy(_subs[topic], newSubs, _subscriberCount[topic]);
    newSubs[_subscriberCount[topic]] = (IUdonEventReceiver)sub;
    _subs[topic] = newSubs;
    // 同步处理 _channels
    _subscriberCount[topic] = newCount;
}

// === 动态取消 ===
public void UnsubscribeDynamic(string topic, UdonSharpBehaviour sub) {
    var dest = Array.IndexOf(_subs[topic], sub);
    if (dest < 0) return;
    // 缩容 + Array.Copy（同 Sardinal）
    // ...
}

// === 统一发布 ===
public void Publish(string topic, object channel, params object[] args) {
    var count = _subscriberCount[topic];
    for (var i = 0; i < count; i++) {
        if (channel != null && _channels[topic][i] != null
            && !_channels[topic][i].Equals(channel))
            continue;
        var sub = _subs[topic][i];
        for (var j = 0; j < args.Length; j++)
            sub.SetProgramVariable(_paramSymbols[topic][j], args[j]);
        sub.SendCustomEvent(_methodSymbols[topic]);
    }
}
```

---

## When To Use

✅ **适用**：
- 混合场景常驻 + 动态生成对象（绝大多数 VRChat World）
- 静态对象订阅主题稳定（不需运行时变更）
- 动态对象生命周期可控（销毁时 Unsubscribe）

❌ **不适用**：
- 全部静态 → 只用静态订阅即可
- 全部动态 → 只用动态 API 即可
- 动态对象高频创建/销毁（每次 Subscribe 都有 O(n) 拷贝成本）→ 考虑用对象池 + 一次性 Subscribe

---

## 性能开销

| 操作 | 开销 |
|------|------|
| 静态订阅（编译期） | 0（一次性） |
| 动态 Subscribe | O(当前订阅数) — `_7[i]++` + `Array.Copy` × 2 数组 |
| 动态 Unsubscribe | O(当前订阅数) — `Array.IndexOf` + 缩容 + `Array.Copy` × 2 |
| Publish | O(总订阅数) — 不区分静态/动态 |
| 内存 | 每订阅者 1 个 `IUdonEventReceiver` 引用（4-8 字节） |

**对比纯静态**：
- 100 个订阅者中 50 静态 + 50 动态
- 动态 Subscribe 100 次：每次 ~50 次 Array.Copy（O(当前)）
- 总成本 ~50×100 = 5000 次拷贝 = 几十 µs（一次性）

**对比纯动态**：
- 纯动态每次都要手动 Subscribe → 重复开发 + 容易漏

→ **混合模式是最实用的方案**。

---

## 关键约束

| 约束 | 说明 |
|------|------|
| **动态订阅 O(n) 扩容** | 高频 Subscribe/Unsubscribe 会卡（n > 1000 时明显） |
| **未 Unsubscribe 内存泄漏** | 动态对象销毁时必须 Unsubscribe，否则订阅表持有死引用 |
| **静态订阅不可运行时变更** | 修改 `[Subscriber]` 后必须重新 Build |
| **`_9` 数组扩容会触发 GC** | Sardinal 没优化，可用 `List<T>`（Udon 部分支持）替代 |
| **静态 + 动态顺序未保证** | 同一主题订阅者被调用顺序不可预测（依赖数组存储顺序） |

---

## 防止内存泄漏的最佳实践

```csharp
// ✅ 推荐：OnDestroy 中 Unsubscribe
public class PooledBullet : UdonSharpBehaviour {
    [SerializeField] Signal signal = new Signal<BulletHit>();

    public override void OnEnable() {
        signal.Subscribe(this);  // 启用时订阅
    }

    public override void OnDisable() {
        signal.Unsubscribe(this);  // 禁用时取消
    }
}

// ⚠️ 必须配对：Subscribe 和 Unsubscribe 次数一致
```

**坑**：
- 容器/Pool 中对象多次启用/禁用 → 必须成对 Subscribe/Unsubscribe
- 场景销毁时 Unity 自动调用 OnDisable，但 OnDestroy 不保证在 OnDisable 之后

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **Sardinal** | `_7` 计数 + `_9` 数组 + Editor 静态注入 | 完整 |
| 自建消息总线 | 单一 `Subscribe` API（不区分） | 简化 |
| 静态事件系统 | 仅 `OnEnable` 注册 + `OnDisable` 注销 | 简化 |

---

## 与其他模式的关系

| 模式 | 关系 |
|------|------|
| **Inherited Subscriber** | 静态订阅自动包含基类继承的订阅者 |
| **Channel Routing** | 静态 + 动态订阅都可指定 channel |
| **Build-Time vs Runtime Separation** | 静态订阅数据来自 Editor 注入 |
| **IID Object Identity** | 动态订阅时用 Udon Type ID 快速过滤 |

---

## 关联文档

- `memory/sources/sardinal.md` — 项目溯源
- `memory/patterns/channel-routing.md` — 配套频道路由
- `memory/patterns/inherited-subscriber.md` — 配套基类继承
- `memory/patterns/build-time-vs-runtime-separation.md` — 静态订阅数据来源
- `memory/patterns/iid-object-identity.md` — 动态订阅类型匹配
- `memory/FACT.md` § Sardinal
