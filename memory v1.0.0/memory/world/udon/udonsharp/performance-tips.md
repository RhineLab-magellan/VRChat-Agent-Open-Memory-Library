# UdonSharp Performance Tips

> Type: BEST PRACTICE
> Domain: World
> Source: creators.vrchat.com/worlds/udon/udonsharp/performance-tips
> SDK Version: 3.10.x
> Last Updated (官方): 2025-01-13
> Last Updated (本地化): 2026-06-15
> Confidence: High

---

## Domain Detection

- **领域**: World
- **子领域**: Udon VM / 运行时性能
- **核心服务对象**: U# 工程师 / 性能优化负责人

---

## 概述

**【FACT - 关键】** UdonSharp 性能**显著低于**原生 C#：

> **Udon 运行一段代码比等效的 C# 慢约 200x 到 1000x**，具体取决于操作类型。

**【FACT】** 这是 Udon VM 解释执行 + 安全沙箱 + 字段访问间接化的固有开销。

> **【R-CRITICAL】** 此页是 **U# 工程师必读**，所有 U# 代码都应考虑这些性能约束。

---

## 1. 关键性能准则（Quick Reference）

| 准则 | 优先级 | 说明 |
|------|--------|------|
| 避免大规模复杂算法（迭代千次） | 🔴 高 | 时间分片（time-slicing） |
| 避免每帧迭代大数组 | 🔴 高 | 时间分片 |
| 优先用原生 Unity / VRC 组件 | 🟡 中 | 例：用动画代替 40 个 GameObject 旋转 |
| 缓存方法结果 | 🟡 中 | `Start()` 中缓存，`Update()` 复用 |
| 用 `private` 方法 | 🟡 中 | 减少 Udon 方法搜索时间 |
| 合并跨 Behaviour 调用 | 🟡 中 | 同一 Behaviour 内聚相关逻辑 |
| 谨慎使用 `GetComponent<T>` | 🔴 高 | 仅在 `Start()` 或低频事件中调用 |

---

## 2. UdonSharp 性能差于 C#（详细）

### 2.1 性能量级

**【FACT】** Udon 运行一段代码比等效的 C# 慢 **200x ~ 1000x**。

**【推断】** 不同操作的性能开销差异巨大：
- 字段访问：~10-50x 慢
- 方法调用：~50-200x 慢
- 复杂逻辑（如字符串拼接）：~500-1000x 慢

### 2.2 优化原则

#### 2.2.1 避免大规模算法

```csharp
// ❌ 避免：每帧遍历 10000 个数组元素
private void Update()
{
    for (int i = 0; i < 10000; i++)
    {
        _array[i] = Process(_array[i]);
    }
}

// ✅ 优化：时间分片（每帧处理 100 个）
private int _sliceIndex = 0;
private const int SLICE_SIZE = 100;

private void Update()
{
    int end = Mathf.Min(_sliceIndex + SLICE_SIZE, _array.Length);
    for (int i = _sliceIndex; i < end; i++)
    {
        _array[i] = Process(_array[i]);
    }
    _sliceIndex = end;
    if (_sliceIndex >= _array.Length) _sliceIndex = 0;
}
```

#### 2.2.2 优先用原生组件

```csharp
// ❌ 避免：用 Udon 旋转 40 个 GameObject
private void Update()
{
    for (int i = 0; i < 40; i++)
    {
        _objects[i].transform.Rotate(Vector3.up, 90f * Time.deltaTime);
    }
}

// ✅ 优化：用 Animator / Animation Clip 一次处理
// 在 Unity Editor 中制作动画，让 GPU/动画系统处理
```

#### 2.2.3 缓存方法结果

```csharp
// ❌ 避免：每帧调用
private void Update()
{
    Vector3 pos = transform.position;       // 属性访问
    VRCPlayerApi player = Networking.LocalPlayer;  // API 调用
}

// ✅ 优化：在 Start() 中缓存
private Transform _cachedTransform;
private VRCPlayerApi _localPlayer;

private void Start()
{
    _cachedTransform = transform;
    _localPlayer = Networking.LocalPlayer;
}

private void Update()
{
    Vector3 pos = _cachedTransform.position;  // 字段访问更快
    // 复用 _localPlayer
}
```

---

## 3. 使用 `private` 方法

### 3.1 原理

**【FACT】** Udon 搜索方法时，**公开方法越少性能越好**。应将**不跨脚本调用**的方法标为 `private`。

### 3.2 跨 Behaviour 调用

**【FACT】** 跨 Behaviour 调用**比本地方法调用慢**。应将相关行为**合并到一个 UdonSharpBehaviour** 中。

```csharp
// ❌ 避免：拆分为多个 Behaviour
public class PlayerStats : UdonSharpBehaviour { ... }
public class PlayerHealth : UdonSharpBehaviour { ... }  // 调用 PlayerStats
public class PlayerCombat : UdonSharpBehaviour { ... }  // 调用 PlayerHealth

// ✅ 优化：合并到一个 Behaviour
public class PlayerController : UdonSharpBehaviour 
{
    // Stats, Health, Combat 在同一类
    // 内部方法调用更快
}
```

### 3.3 CustomNetworkEvent 注意事项

> **【FACT】** 发送 `CustomNetworkEvent` 时，目标方法**必须**是 `public`。否则不会触发。

> **【FACT】** 以下划线开头的方法（如 `_MyLocalMethod`）**不会**接收网络事件。

```csharp
// ✅ 正确：public 方法接收网络事件
public void OnInteract()  // public, 会被 SendCustomNetworkEvent 调用
{
    // ...
}

// ❌ 错误：private / 下划线方法不接收网络事件
private void OnInteract() { }  // 不会触发
public void _MyLocalMethod() { }  // 不会触发（_ 前缀）
```

---

## 4. 谨慎使用 `GetComponent<T>`

### 4.1 原理

**【FACT】** `GetComponent<T>()` 调用**慢**，特别是在 Udon 中获取 UdonSharpBehaviour 类型时。

**【FACT】** 原因：UdonSharp 需插入循环检查**所有 UdonBehaviours** 以确认它们是正确的 UdonSharpBehaviour 类型。

### 4.2 优化

**【FACT】** 应**仅在 `Start()` 事件或不频繁的事件中**使用 `GetComponent<T>()`。

```csharp
// ❌ 避免：每帧调用
private void Update()
{
    var renderer = GetComponent<Renderer>();
    renderer.material.color = Color.red;
}

// ✅ 优化：在 Start() 中缓存
private Renderer _cachedRenderer;

private void Start()
{
    _cachedRenderer = GetComponent<Renderer>();
}

private void Update()
{
    _cachedRenderer.material.color = Color.red;
}
```

---

## 5. 字符串操作（未在官方 performance-tips 中提及但重要）

**【未确认】** 官方 performance-tips 页面**未明确**提到字符串性能，但 Udon VM 中字符串操作有显著开销。

**【FACT - memory/api/udonsharp-runtime.md / 视频播放器(参考工程)验证】**：

### 5.1 避免 `String +=` 累积

```csharp
// ❌ 避免：在循环中拼接字符串
string result = "";
for (int i = 0; i < 100; i++)
{
    result += "Item" + i + ";";  // 每次生成临时 string 对象
}

// ✅ 优化：使用 StringBuilder（U# 支持）
System.Text.StringBuilder sb = new System.Text.StringBuilder();
for (int i = 0; i < 100; i++)
{
    sb.Append("Item");
    sb.Append(i);
    sb.Append(";");
}
string result = sb.ToString();
```

### 5.2 字符串驻留与缓存

```csharp
// ✅ 缓存常用字符串
private string _cachedPrefix;

private void Start()
{
    _cachedPrefix = "Player_";
}

private string GetPlayerLabel(int id)
{
    return _cachedPrefix + id;  // 拼接一次
}
```

---

## 6. foreach vs for（未在官方 performance-tips 中提及但重要）

**【未确认】** 官方 performance-tips 页面**未明确**提到 foreach，但 Udon VM 中 foreach 涉及迭代器对象创建。

**【推断】** 对**大数组**，优先用 `for (int i = 0; i < array.Length; i++)`。

```csharp
// ⚠️ foreach 涉及迭代器抽象
foreach (var item in _array) { ... }

// ✅ 优先用 for 索引
for (int i = 0; i < _array.Length; i++) { var item = _array[i]; ... }
```

> **【未确认】** 实际性能差异需用 Profiler 验证。短数组（< 10 元素）差异不显著。

---

## 7. Instantiate / Destroy 优化（未在官方 performance-tips 中提及）

**【未确认】** 官方 performance-tips 页面**未明确**提到 Instantiate 优化，但视频播放器等大型参考工程普遍使用对象池。

**【FACT - 视频播放器(参考工程)验证】**：

```csharp
// ❌ 避免：频繁 Instantiate / Destroy
private void FireBullet()
{
    GameObject bullet = Instantiate(_bulletPrefab);
    // ... 3 秒后
    Destroy(bullet);
}

// ✅ 优化：对象池
private GameObject[] _bulletPool;
private int _nextBullet = 0;

private void Start()
{
    _bulletPool = new GameObject[POOL_SIZE];
    for (int i = 0; i < POOL_SIZE; i++)
    {
        _bulletPool[i] = Instantiate(_bulletPrefab);
        _bulletPool[i].SetActive(false);
    }
}

private void FireBullet()
{
    GameObject bullet = _bulletPool[_nextBullet];
    _nextBullet = (_nextBullet + 1) % POOL_SIZE;
    bullet.SetActive(true);
    // ... 3 秒后
    bullet.SetActive(false);  // 回收而非销毁
}
```

> **【R-HIGH】** Instantiate 在 Udon VM 中**极慢**，且产生大量 GC 压力。**必须**用对象池处理频繁生成的对象（子弹、特效、UI 元素等）。

---

## 8. Update 优化（综合）

**【FACT】** `Update()` 每帧执行，**任何**在 `Update()` 中的低效代码都会被放大 60+ 倍/秒。

### 8.1 早退原则

```csharp
private void Update()
{
    if (!_isActive) return;              // 快速退出
    if (_timeSinceLastAction < INTERVAL)  // 限流
    {
        _timeSinceLastAction += Time.deltaTime;
        return;
    }
    _timeSinceLastAction = 0;
    
    // ... 实际逻辑
}
```

### 8.2 避免昂贵 API

```csharp
// ❌ 避免在 Update 中：
// - FindObjectOfType<T>()
// - GetComponent<T>()
// - Instantiate / Destroy
// - Raycast 大量射线
// - Physics.OverlapSphere 频繁调用
// - StringBuilder.ToString()（频繁）
```

### 8.3 状态机驱动

```csharp
// ✅ 用状态机驱动而非每帧轮询
private int _state;
private float _stateTime;

private void Update()
{
    _stateTime += Time.deltaTime;
    switch (_state)
    {
        case 0: // Idle
            if (_isTriggered) { _state = 1; _stateTime = 0; }
            break;
        case 1: // Action
            if (_stateTime > 1.0f) { _state = 2; _stateTime = 0; }
            break;
        // ...
    }
}
```

---

## 9. 网络同步优化（与 performance-tips 互补）

**【FACT - memory/patterns/manual-sync-state.md 验证】**：

| 优化 | 说明 |
|------|------|
| **Manual Sync** | 避免无意义序列化（[attributes.md](./attributes.md#3-udonbehavioursyncmode-详解)） |
| **阈值触发** | 避免每帧同步（值变化 > 阈值才 RequestSerialization） |
| **批量提交** | 多次修改合并为单次序列化（NetworkCallable 配合延迟） |
| **位域压缩** | 多个 bool 压缩为单个 byte |
| **Master 时间锚点** | 同步一个时间戳，客户端本地计算 |

> **【未确认】** 网络同步性能影响未在官方 performance-tips 中直接讨论，但 `memory/api/networking.md` 中有详细带宽限制（~11KB/s、280KB/serialization）。

---

## 10. 性能 Profile 方法

### 10.1 Unity Profiler

**【推断】** Unity Profiler（Window > Analysis > Profiler）可用于：
- 测量 U# 脚本的 CPU 占用
- 识别 GC 分配（Instantiate / String +=）
- 定位长时间运行的 Update 方法

### 10.2 VRChat ClientSim

**【FACT - memory/sources/clientsim.md 验证】** ClientSim 模拟 VRChat 客户端环境，可用于：
- 在 Editor 中测试 U# 性能
- 验证同步行为
- 无需进入 VRChat 实例即可调试

### 10.3 Debug Build / Inline Code

**【FACT - configuration.md 验证】** 启用 `Debug build` + `Inline Code` 可在 Udon Graph 中查看 C# 源码，便于定位性能热点。

---

## 11. 性能优化检查清单

| ✅ | 检查项 |
|---|--------|
| ☐ | 缓存 `transform` 引用（在 `Start()` 中） |
| ☐ | 缓存 `Networking.LocalPlayer`（在 `Start()` 中） |
| ☐ | 缓存 `GetComponent<T>()` 结果（在 `Start()` 中） |
| ☐ | 所有非跨脚本方法标 `private` |
| ☐ | 大数组用时间分片（每帧处理 N 个） |
| ☐ | 用 Animator/Animation 代替 Udon 驱动的循环 |
| ☐ | 用对象池处理 Instantiate / Destroy |
| ☐ | 字符串拼接用 StringBuilder |
| ☐ | 同步用 Manual 模式 + 阈值触发 |
| ☐ | Update 中避免 FindObjectOfType / GetComponent / Instantiate |

---

## 12. 与已有知识库的关系

| 现有知识库 | 应补充/引用 |
|-----------|----------|
| `memory/api/networking.md` | 同步模式选择与带宽限制 |
| `memory/patterns/manual-sync-state.md` | Manual Sync + 阈值触发范式 |
| `memory/patterns/owner-authoritative-interaction.md` | Owner Authority 模式 |
| `memory/api/udonsharp-runtime.md` | Odin Serializer、GetProgramVariable 性能 |
| `memory/world/performance-guide.md` | World 综合性能（材质、光照）|
| `memory/sources/clientsim.md` | 性能测试环境 |
| `memory/rules/udonsharp-language-limits.md` | 语言限制（无 Generic 等）的性能影响 |

---

## 13. 风险与未知

### 风险

- **【R-CRITICAL】** Udon 200-1000x 慢于 C#，未优化的 U# 代码会导致**帧率灾难**
- **【R-HIGH】** Instantiate 在 Udon 中**极慢**，必须用对象池
- **【R-HIGH】** 字符串 `+=` 累积触发 GC，导致**周期性卡顿**
- **【R-MED】** Update 中 `GetComponent<T>()` 是常见的**性能黑名单**
- **【R-MED】** 跨 Behaviour 调用比本地调用慢，应合并相关行为

### 未知

- **【未确认】** foreach 与 for 在 Udon VM 中的**精确**性能差异
- **【未确认】** 字符串 `+` 拼接在 Udon 中的 GC 行为细节
- **【未确认】** `Update` 中允许的**最大**操作次数（依场景复杂度而异）
- **【未确认】** Profiler 在 U# 脚本上的具体指标
- **【未确认】** 不同 VRChat 客户端平台（PC / Quest）下的性能差异量化数据

---

## 14. 实践建议

### 14.1 开发流程

1. **先实现功能** → 用清晰的逻辑结构
2. **运行 Profiler** → 识别热点
3. **针对性优化** → 缓存、合并、池化
4. **再次 Profile** → 验证效果
5. **测试边缘情况**（高玩家数、Quest 端）

### 14.2 性能预算

**【推断 - 经验值】** 100 个 U# 脚本的复杂 World：
- 总体 CPU 预算：< 5ms/帧（目标 60fps）
- 单个 `Update()`：< 0.1ms（典型）
- 关键系统：< 0.5ms（Networking、Player Tracking）

> **【未确认】** 具体预算需用 Profiler 在目标平台（PC / Quest）实测确定。
