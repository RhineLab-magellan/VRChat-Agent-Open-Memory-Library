# Pattern: Build-Time vs Runtime Separation (构建时与运行时分离)

> Type: PATTERN
> Source: ULocalization(参考工程)
> Confidence: High
> SDK Version: 3.10.x
> Last Verified: 2026-06-20
> Reference: `memory/sources/ulocalization.md`

---

## Problem / Context

Udon VM 限制 + Unity 编辑器 API 限制 + 性能优化需求 三重压力下，需要明确划分"哪些在 Editor 做、哪些在 Runtime 做"。

具体痛点：
- ❌ Unity Editor API（如 `LocalizationSettings.GetStringTableCollection`）在 Udon 运行时不可用
- ❌ Udon 没有 LINQ / 反射 / 复杂集合，运行时做数据组装极慢
- ❌ `IStartupLocaleSelector` / `LocalizeEvent` 配置变更需要重新构建依赖
- ❌ 任何运行时修改配置都需要重新 Build 才能生效

ULocalization 场景：
- 50+ LocalizeEvent + 100+ UnityEvent listener + 30+ Variable + 16 IVariable 类型
- 全部需要 Editor 端扫描、归一化、注入；Runtime 端仅做查表

---

## Udon Constraints 影响

| 约束 | 影响 |
|------|------|
| 无 `IEnumerator` / 复杂循环 | 运行时不能做复杂数据组装 |
| 无 LINQ | 运行时不能用 `Where` / `Select` |
| 无反射 | 运行时不能 `Type.GetMethods()` |
| 无 `GetComponent<T>` | 运行时不能查 Component |

---

## Solution

**核心思想**：Editor 端用完整 C# 能力（反射 + LINQ + 缓存），把所有数据**编译期**预处理好，注入到 Udon 字段。Runtime 端仅做 O(1) 数组查表。

### 关键机制

#### 1. Editor 端：完整数据组装

```csharp
// Editor/Udon/LocalizationResolver.cs
internal sealed class LocalizationResolver : IBindingResolver {
    public object Resolve(Type type, Container container) {
        // 1. 扫描场景所有 LocalizeEvent
        var localizeEvents = BuildLocalizeEvents(scene);

        // 2. 收集所有 LocalizedString
        var localizeds = BuildLocalizeds();

        // 3. 读 LocalizationSettings StringTable
        var entries = BuildEntries(localizeds);

        // 4. 收集所有 PersistentVariables
        var variables = BuildVariables();

        // 5. 处理 VRCPlayerObject 克隆
        var cloneDetectorData = BuildCloneDetectors(container, scene, localizeEvents);

        // 6. 注入到 shim
        builder.RegisterComponentInstance(localization)
            .As<Localization>()
            .WithParameter("_0", availableLocalesCodes)         // string[]
            .WithParameter("_1", cultureInfos)                  // CultureInfo[]
            .WithParameter("_2", projectLocale)                 // string
            .WithParameter("_3", projectCulture)                // CultureInfo
            .WithParameter("_4", startupSelectors)              // IStartupLocaleSelector[]
            .WithParameter("_5", entryValues)                   // object[][]
            .WithParameter("_6", entryIsSmarts)                 // bool[][]
            .WithParameter("_7", localizeEventCount)            // int
            .WithParameter("_8", localizeEventLocalized)        // int[]
            .WithParameter("_9", listenerCount)                 // int[]
            .WithParameter("_10", listenerMethods)              // string[][]
            .WithParameter("_11", listenerTargets)              // object[][]
            .WithParameter("_12", listenerArguments)            // object[][]
            // ... 共 27 个 _0 ~ _26 参数
    }
}
```

#### 2. Udon 端：仅查表

```csharp
// LocalizationShim.cs (运行时)
public override string[] AvailableLocales => _0;  // 直接数组访问
public override string SelectedLocale {
    get => locale;
    set => SetSelectedLocale(value);
}

public void SetSelectedLocale(string locale) {
    if (this.locale == locale) return;
    var idx = Array.IndexOf(_0, locale);
    if (idx < 0) {
        Logger.LogWarning($"Locale {locale} is not supported, ignoring the change.");
        return;
    }
    this.locale = locale;
    culture = _1[idx];
    entries = _5[idx];
    smarts = _6[idx];
    signal.Publish(locale);
    for (var i = 0; i < _7; i++) {
        RefreshLocalizeEvent(i);
    }
}
```

#### 3. Build 阶段：清理被替代的组件

```csharp
// LocalizationCleanup.cs (Build 钩子)
internal sealed class LocalizationCleanup : IVRCSDKBuildProcessScene {
    public override int callbackOrder => 100;

    public override void OnBuildProcessScene(Scene scene) {
        if (!LocalizationSettings.HasSettings) return;
        CleanupScene(scene);
    }

    static void CleanupScene(Scene scene) {
        foreach (var localizeEvent in LocalizeEventCache.GetAll()) {
            // 1. 禁用原组件
            localizeEvent.hideFlags = HideFlags.NotEditable | HideFlags.DontSaveInBuild;
            localizeEvent.enabled = false;

            // 2. 清空所有 UnityEvent 持久监听（避免重复触发）
            var fields = localizeEvent.GetType().GetBaseTypes()
                .SelectMany(x => x.GetFields(BindingFlags.Instance | BindingFlags.NonPublic))
                .Where(x => x.FieldType.IsSubclassOf(typeof(UnityEventBase)));
            foreach (var field in fields) {
                var unityEventBase = (UnityEventBase)field.GetValue(localizeEvent);
                if (unityEventBase == null) continue;
                // 用反射清空所有持久 listener
                field.SetValue(localizeEvent, Activator.CreateInstance(unityEventBase.GetType()));
            }
        }

        // 3. 隐藏所有 IBehaviourExtension 组件
        var behaviourExtensions = scene.GetRootGameObjects()
            .SelectMany(x => x.GetComponentsInChildren(typeof(IBehaviourExtension)));
        foreach (var behaviourExtension in behaviourExtensions) {
            behaviourExtension.hideFlags = HideFlags.NotEditable | HideFlags.DontSaveInBuild;
        }
    }
}
```

#### 4. Build 阶段：注册 CloneDetector

```csharp
// LocalizationResolver.BuildCloneDetectors (Editor 端)
for (var i = 0; i < markers.Length; i++) {
    container.Scope(builder => {
        builder.RegisterEntryPoint(
            CloneDetectorUtility.ImplementationType,
            Lifetime.Transient
        )
            .UnderTransform(() => {
                var go = new GameObject($"{CloneDetectorUtility.ImplementationType.Name} [{markers[i].GetHashCode():x8}]");
                go.transform.SetParent(markers[i].transform, true);
                go.hideFlags = HideFlags.HideInHierarchy;
                return go.transform;
            })
            .WithParameter("_0", markers[i].gameObject)
            .WithParameter("_1", i)
            .WithParameter("_2", refs[i].ToArray());
    });
}
```

#### 5. Runtime 端：CloneDetector 触发重建

```csharp
// CloneDetector.cs
internal sealed class CloneDetector : UdonSharpBehaviour {
    [Inject] Localization localization;
    [Inject] GameObject _0;
    [Inject] int _1;
    [Inject] object[] _2;

    private void Start() {
        var _localization = (LocalizationShim)localization;
        _localization.RenewPrefab(_0, _1, _2);
        DestroyImmediate(gameObject);
    }
}
```

---

## Networking Model

| 维度 | 取值 |
|------|------|
| State Owner | Editor 拥有所有计算责任 |
| Source of Truth | Editor 注入的 int[] / object[] / string[] |
| Sync Type | N/A（不需网络） |
| Synced Variables | 无 |
| Mutation Path | Editor `WithParameter` 注入 |
| Ownership Path | 无 |
| Serialization Path | 无 |
| Receive Path | Runtime 数组查表 |
| Late Joiner | 自动（场景数据一致） |
| Conflict Strategy | 无 |
| Bandwidth Budget | 0 |
| Failure Mode | 改 Scene 后未重建 → 引用失效 |

---

## Implementation Sketch

```csharp
// === Editor 端：完整数据准备 ===
public class MyBuildProcessor {
    public static (object[] data, string[] names) PrepareData(Scene scene) {
        // 1. 反射扫描
        var allObjects = scene.GetRootGameObjects()
            .SelectMany(x => x.GetComponentsInChildren<MyComponent>(true))
            .ToList();

        // 2. LINQ 归一化
        var dataArray = allObjects
            .Select(x => ExtractValue(x))
            .ToArray();
        var namesArray = allObjects
            .Select(x => x.name)
            .ToArray();

        // 3. 类型分组
        var typeGroups = allObjects
            .GroupBy(x => x.GetType().Name)
            .ToDictionary(g => g.Key, g => g.ToList());

        return (dataArray, namesArray);
    }
}

// === Runtime 端：O(1) 查表 ===
public partial class MyRuntime : UdonSharpBehaviour {
    [Inject] object[] _data;
    [Inject] string[] _names;

    public object Get(int idx) => _data[idx];
    public string GetName(int idx) => _names[idx];
}

// === Build 钩子：清理原组件 ===
public class Cleanup : IVRCSDKBuildProcessScene {
    public override void OnBuildProcessScene(Scene scene) {
        foreach (var c in scene.GetRootGameObjects()
            .SelectMany(x => x.GetComponentsInChildren<MyComponent>(true))) {
            c.enabled = false;
            c.hideFlags = HideFlags.NotEditable | HideFlags.DontSaveInBuild;
        }
    }
}
```

---

## When To Use

✅ **适用**：
- 数据可在编译期完全确定
- 运行时仅做查表/分派
- 性能敏感（避免运行时 LINQ/反射）
- 配置与逻辑解耦

❌ **不适用**：
- 运行时需要动态添加组件
- 运行时需要根据用户输入计算
- 修改 Scene 后不想重建

---

## 关键约束

| 约束 | 说明 |
|------|------|
| **修改 Scene 后必须重建** | 任何 LocalizeEvent / LocalizedString 变更都需要重新 Build |
| **UnityEvent listener 必须白名单内** | 否则在 Build 阶段被过滤 |
| **CloneDetector 仅处理 VRCPlayerObject** | 手动 Instantiate 不走此路径 |
| **不要运行时改 IVariable 集合** | 数组长度在 Build 时固定 |

---

## 项目实例

| 项目 | 用法 | 变体 |
|------|------|------|
| **ULocalization** | Editor 扫描 + 27 字段注入 + Build 清理 | 完整 |
| Modular Avatar | NDMF Build Pipeline | 部分（仍允许运行时） |
| ORL Shaders | Material 配置预生成 | 简化 |

---

## 关联文档

- `memory/sources/ulocalization.md` — 项目溯源
- `memory/patterns/iid-object-identity.md` — 配套 ID 映射
- `memory/patterns/code-generation-type-erasure.md` — 配套类型擦除
- `memory/FACT.md` § ULocalization
