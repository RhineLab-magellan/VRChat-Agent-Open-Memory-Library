# Udon API 检查器

> Type: TOOL
> Purpose: 检查代码是否使用了未暴露的 Udon API
> Last Updated: 2026-06-11

---

## 使用方法

### 快速检查表

在编写 UdonSharp 代码时，对照以下清单检查 API 可用性：

### ❌ 禁止使用

| 类别 | API | 说明 |
|------|-----|------|
| 文件 | `System.IO.*` | 禁止文件操作 |
| 网络 | `System.Net.*` | 禁止网络请求 |
| 线程 | `System.Threading.*` | 禁止多线程 |
| 反射 | `System.Reflection.*` | 禁止反射 |
| 动态 | `dynamic` 关键字 | 禁止动态类型 |
| 异步 | `async/await` | 禁止异步模式 |
| 异常 | `try/catch/throw` | 禁止异常处理 |
| 协程 | `IEnumerator/StartCoroutine` | 使用 SendCustomEventDelayedSeconds |

### ⚠️ 需要注意

| 类别 | API | 可用性 | 注意 |
|------|-----|--------|------|
| 集合 | `List<T>` | 部分 | 只有特定类型的 List 可用 |
| 集合 | `Dictionary<K,V>` | ❌ | 使用 DataDictionary |
| 查找 | `FindObjectsOfType<T>()` | ❌ | 场景加载时缓存引用 |
| 销毁 | `Object.Destroy()` | ❌ | 使用 SetActive(false) |
| 创建 | `new GameObject()` | ❌ | 使用对象池或预制体 |
| 渲染 | `Camera.Render()` | ❌ | 禁止手动渲染 |
| 消息 | `SendMessage()` | ❌ | 使用 SendCustomEvent |
| 输入 | `Input.mousePosition` | ❌ | VRChat 不使用鼠标位置 |
| 时间 | `Time.frameCount` | ❌ | 自行维护计数器 |
| Transform | `Transform.DetachChildren()` | ❌ | 设置 parent = null |
| Component | `tag` 属性 | ❌ | 使用 LayerMask |

### ✅ 安全使用

| 类别 | API | 说明 |
|------|-----|------|
| 同步 | `DataList/DataDictionary` | VRC 数据容器 |
| 同步 | `VRCJson` | JSON 序列化 |
| 事件 | `SendCustomEvent/SendCustomNetworkEvent` | 安全的事件系统 |
| 网络 | `RequestSerialization/OnDeserialization` | 网络同步 |
| 输入 | `Input.GetKey/GetButton` | 标准输入 API |
| 物理 | `Rigidbody.velocity` | 刚体物理 |
| 动画 | `Animator.SetFloat/SetBool` | 动画参数控制 |

---

## 代码模式检查

### ❌ 错误模式

```csharp
// 错误 1: 使用 List<T>
List<GameObject> objects = new List<GameObject>();
objects.Add(target);

// 错误 2: 使用 Dictionary
Dictionary<string, int> dict = new Dictionary<string, int>();

// 错误 3: 使用反射
Type t = Type.GetType("MyClass");
var method = t.GetMethod("MyMethod");

// 错误 4: 使用异步
async void LoadData() {
    await Task.Delay(1000);
}

// 错误 5: 使用异常
try {
    DoSomething();
} catch (Exception e) {
    Debug.Log(e.Message);
}

// 错误 6: 使用协程
StartCoroutine(WaitAndDo());

// 错误 7: 动态查找对象
var obj = GameObject.Find("TargetObject");

// 错误 8: 销毁对象
Destroy(target);

// 错误 9: 创建对象
var newObj = new GameObject("NewObject");

// 错误 10: 使用 tag
if (other.CompareTag("Enemy")) { }

// 错误 11: 发送消息
other.SendMessage("OnHit");

// 错误 12: 使用 mousePosition
Vector3 mousePos = Input.mousePosition;
```

### ✅ 正确模式

```csharp
// 正确 1: 使用 DataList
VRC.SDKBase.DataList dataList = new VRC.SDKBase.DataList();
dataList.Add(target);

// 正确 2: 使用 DataDictionary
VRC.SDKBase.DataDictionary dict = new VRC.SDKBase.DataDictionary();

// 正确 3: 场景加载时缓存引用
[SerializeField] private GameObject targetObject;
void Start() {
    // targetObject 已在 Inspector 中赋值
}

// 正确 4: 使用延迟事件代替异步
SendCustomEventDelayedSeconds(nameof(_DelayedAction), 1.0f);
void _DelayedAction() {
    // 延迟执行的逻辑
}

// 正确 5: 使用条件判断代替异常
if (CanDoSomething()) {
    DoSomething();
}

// 正确 6: 使用对象池
VRC.SDKBase.VRCObjectPool pool;
void GetFromPool() {
    var obj = pool.TryToSpawn();
}

// 正确 7: 使用 SetActive
target.SetActive(false);

// 正确 8: 使用 LayerMask
if ((layerMask.value & (1 << other.gameObject.layer)) != 0) { }

// 正确 9: 使用 SendCustomEvent
other.SendCustomEvent("OnHit");
```

---

## 常见问题

### Q: 为什么 List<T> 不能用？
A: Udon VM 不支持大部分 `List<T>` 方法。只有特定类型的 List（如 `List<ConstraintSource>`）在某些 API 中可用。

### Q: 如何实现定时器？
A: 使用 `SendCustomEventDelayedSeconds()` 而不是协程。

### Q: 如何实现对象查找？
A: 在场景加载时通过 Inspector 或 `GetComponentInChildren` 缓存引用，避免运行时查找。

### Q: 如何处理错误？
A: 使用条件判断预检查，避免异常。或使用 `Debug.Log` 记录错误状态。

---

## 相关知识

- `memory/api/udon-type-exposure.md` — Udon Type Exposure Tree 索引
- `memory/api/exposed-types.md` — 已暴露类型详细清单
- `memory/api/not-exposed.md` — 未暴露 API 黑名单
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制