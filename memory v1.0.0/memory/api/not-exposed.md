# NOT EXPOSED API 黑名单 - VRChat SDK 3.10.3

> Type: REFERENCE
> Source: `参考文献/UdonTypeExposure.txt` 解析
> SDK Version: 3.10.3
> Confidence: High
> Last Updated: 2026-06-11

---

## ⚠️ 重要说明

以下 API 在 Udon 中**不可用**。使用这些 API 会导致：
1. **编译错误**：UdonSharp 编译器直接报错
2. **运行时无效果**：静默失败，行为异常
3. **崩溃风险**：可能导致 Udon VM 不稳定

**在使用任何 Unity API 前，请先查阅此文档确认可用性。**

---

## System 命名空间（禁止使用）

| 类型/成员 | 原因 |
|-----------|------|
| `System.IO` 命名空间全部 | 文件操作被禁止 |
| `System.Net` 命名空间全部 | 网络请求被禁止 |
| `System.Threading` 命名空间全部 | 多线程被禁止 |
| `System.Reflection` 命名空间全部 | 反射被禁止 |
| `System.Type.GetType()` | 反射相关 |
| `System.Activator.CreateInstance()` | 动态创建被禁止 |

---

## UnityEngine 核心（部分不可用）

### GameObject

| 成员 | 状态 | 替代方案 |
|------|------|----------|
| `CompareTag(string)` | ❌ NOT EXPOSED | 使用 `tag == "xxx"` |
| `SendMessage()` | ❌ NOT EXPOSED | 使用 `SendCustomEvent()` |
| `BroadcastMessage()` | ❌ NOT EXPOSED | 使用 `SendCustomEvent()` |
| `SendMessageUpwards()` | ❌ NOT EXPOSED | 使用 `SendCustomEvent()` |

### Component

| 成员 | 状态 | 替代方案 |
|------|------|----------|
| `tag` 属性 | ❌ NOT EXPOSED | 使用 LayerMask 或自定义标记 |
| `TryGetComponent<T>()` | ❌ NOT EXPOSED | 使用 `GetComponent<T>()` + null 检查 |
| `CompareTag()` | ❌ NOT EXPOSED | 使用 `tag == "xxx"` |
| `SendMessage*()` | ❌ NOT EXPOSED | 使用 `SendCustomEvent()` |

### Object

| 成员 | 状态 | 替代方案 |
|------|------|----------|
| `FindObjectsOfType<T>()` | ❌ NOT EXPOSED | 场景加载时缓存引用 |
| `FindObjectOfType<T>()` | ❌ NOT EXPOSED | 场景加载时缓存引用 |
| `Destroy()` | ❌ NOT EXPOSED | 使用 `SetActive(false)` 或对象池 |
| `DestroyImmediate()` | ❌ NOT EXPOSED | 禁止使用 |
| `Instantiate()` | ⚠️ 受限 | 谨慎使用，可能影响性能 |

### Time

| 成员 | 状态 | 说明 |
|------|------|------|
| `timeAsDouble` | ❌ NOT EXPOSED | 使用 `time` |
| `unscaledTime` | ❌ NOT EXPOSED | 使用 `time` |
| `unscaledTimeAsDouble` | ❌ NOT EXPOSED | 使用 `time` |
| `fixedTime` | ❌ NOT EXPOSED | 使用 `time` |
| `frameCount` | ❌ NOT EXPOSED | 自行维护计数器 |
| `maximumDeltaTime` | ❌ NOT EXPOSED | 不可配置 |

### Input

| 成员 | 状态 | 替代方案 |
|------|------|----------|
| `mousePosition` | ❌ NOT EXPOSED | 使用 VRC SDK 输入 API |
| `mouseScrollDelta` | ❌ NOT EXPOSED | 使用 VRC SDK 输入 API |
| `GetTouch()` | ❌ NOT EXPOSED | VR 不需要 Touch |
| `touches` | ❌ NOT EXPOSED | VR 不需要 Touch |
| `acceleration` | ❌ NOT EXPOSED | VR 不需要 |
| `gyro` | ❌ NOT EXPOSED | VR 不需要 |
| `ResetInputAxes()` | ❌ NOT EXPOSED | 不可用 |
| `IsJoystickPreconfigured()` | ❌ NOT EXPOSED | 不可用 |

### Camera

| 成员 | 状态 | 替代方案 |
|------|------|----------|
| `main` | ❌ NOT EXPOSED | 场景加载时缓存引用 |
| `current` | ❌ NOT EXPOSED | 使用 VRC 相机 API |
| `Render()` | ❌ NOT EXPOSED | 禁止调用渲染 |
| `ScreenPointToRay()` | ❌ NOT EXPOSED | 使用 VRCPhysics 或 Contact |
| `ScreenToWorldPoint()` | ⚠️ 受限 | 部分重载可用 |

### Transform

| 成员 | 状态 | 替代方案 |
|------|------|----------|
| `parent` 属性 set | ⚠️ 受限 | 仅某些场景可用 |
| `DetachChildren()` | ❌ NOT EXPOSED | 手动设置 parent = null |
| `Find()` | ❌ NOT EXPOSED | 场景加载时缓存引用 |

---

## UnityEngine.UI（部分不可用）

### Event System

| 成员 | 状态 | 说明 |
|------|------|------|
| `Event` 类全部 | ❌ NOT EXPOSED (2.56%) | VRChat 不使用传统 Event |
| `PointerEventData` | ❌ 大部分 NOT EXPOSED | 仅部分 UI 交互可用 |

### Text

| 成员 | 状态 | 说明 |
|------|------|------|
| `font` 属性 | ❌ NOT EXPOSED | 材质配置 |
| `text` 动态更新 | ⚠️ 受限 | 低频更新可用 |

---

## Collections 泛型（禁止使用）

| 类型 | 状态 | 替代方案 |
|------|------|----------|
| `List<T>` | ❌ 构造函数和大部分方法 NOT EXPOSED | 使用 `DataList` 或数组 |
| `Dictionary<TKey, TValue>` | ❌ 全部 NOT EXPOSED | 使用 `DataDictionary` |
| `HashSet<T>` | ❌ 全部 NOT EXPOSED | 使用数组 + 手动查找 |
| `Queue<T>` | ❌ 全部 NOT EXPOSED | 使用数组模拟 |
| `Stack<T>` | ❌ 全部 NOT EXPOSED | 使用数组模拟 |

**注意**：`List<T>` 类型本身标记为暴露（1.89%），但其所有方法都是 NOT EXPOSED。只有特定类型的 `List<T>` 可用：
- `List<ConstraintSource>` — 用于约束 API
- `List<KeyValuePair<AnimationClip, AnimationClip>>` — 用于 AnimatorOverrideController

---

## Animation/Legacy（禁止使用）

| 类型 | 状态 | 说明 |
|------|------|------|
| `Animation` | ❌ NOT EXPOSED | 使用 Animator |
| `AnimationClip.SetCurve()` | ❌ NOT EXPOSED | 运行时不可修改曲线 |
| `Keyframe` 构造函数 | ❌ NOT EXPOSED | 不可动态创建关键帧 |

---

## Physics/Raycast

| 成员 | 状态 | 替代方案 |
|------|------|----------|
| `Physics.Raycast()` 静态方法 | ⚠️ 部分可用 | 使用 NavMesh 或 Contact |
| `Physics.SphereCast()` | ❌ NOT EXPOSED | 使用 VRCContactReceiver |
| `Physics.CapsuleCast()` | ❌ NOT EXPOSED | 使用 VRCContactReceiver |
| `Physics.BoxCast()` | ❌ NOT EXPOSED | 使用 VRCContactReceiver |

---

## 已知限制

### 构造函数限制
大多数 Unity 组件的构造函数是 NOT EXPOSED，不能使用 `new` 创建：
- `new GameObject()` — ❌
- `new Rigidbody()` — ❌
- `new Mesh()` — ❌

### ref/out 参数
部分方法使用 `ByRef` 参数（ref/out）在 Udon 中可能有问题：
- `NavMeshHit` 作为 out 参数 — ✅ 可用
- `SmoothDamp` ref 参数 — ⚠️ 谨慎使用

### 回调/事件
以下回调机制在 Udon 中不可用：
- UnityEvent / UnityAction — ❌
- Delegate / Action / Func — ❌
- Callback 函数 — ❌

---

## 验证方法

### 1. 查看暴露树
检查 `参考文献/UdonTypeExposure.txt` 中该类型是否有 `[EXPOSED]` 标记。

### 2. 编译测试
在 Unity 中编译 UdonSharp 脚本，查看是否有编译错误。

### 3. 运行时测试
在 VRChat 中测试功能，确认行为符合预期。

---

## 相关知识

- `memory/api/udon-type-exposure.md` — Udon Type Exposure Tree 索引
- `memory/api/exposed-types.md` — 已暴露类型详细清单
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制