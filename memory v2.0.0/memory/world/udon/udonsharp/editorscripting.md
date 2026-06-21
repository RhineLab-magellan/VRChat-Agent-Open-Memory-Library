---
title: UdonSharp Editor Scripting
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udonsharp
  - udon

aliases:
  - "UdonSharp Editor Scripting"

source: creators.vrchat.com/worlds/udon/udonsharp/editorscripting
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
---
# UdonSharp Editor Scripting

> Domain: World
> SDK Version: 3.10.x
> Last Updated (官方): 2024-08-07
> Last Updated (本地化): 2026-06-15
---

## Domain Detection

- **领域**: World
- **子领域**: UdonSharp 编辑器扩展
- **核心服务对象**: U# 工程师 / 工具开发者

---

## 概述

**【FACT】** UdonSharp 提供了**编辑器脚本 API**，允许开发者编写与 UdonSharpBehaviour 交互的自定义 Editor 脚本，行为与普通 C# 行为**基本一致**。

**核心机制**：UdonSharp 会在编辑器中创建 U# 脚本的 C# 版本"代理"（Proxy），并在其与 UdonBehaviour 后端之间自动同步字段。

---

## 1. Proxies（代理）系统

### 1.1 核心概念

**【FACT】** U# 脚本是**有效的 C# 代码**，可以与普通独立组件一起作为 Proxies 添加到 GameObject 上。

**类比**：
- Proxy ≈ Unity 的 `SerializedObject`（需手动应用变更）
- 在 Proxy 上的修改不会自动同步到 UdonBehaviour
- 在 UdonBehaviour 上的修改不会自动更新 Proxy

### 1.2 Proxy 特性

| 特性 | 说明 |
|------|------|
| **位置** | 与其后端 UdonBehaviour 在**同一 GameObject** 上 |
| **状态** | 始终**禁用**（防止 Unity 在 GameObject 上重复执行事件） |
| **Inspector 可见性** | 在 GameObject Inspector 中**隐藏**（marked as hidden） |
| **构建排除** | **不**保存到场景，**不**保存到构建（不增加包/下载体积） |
| **方法执行** | 可在 Proxy 上执行方法，效果与在 UdonBehaviour 上运行事件相同 |

### 1.3 关键限制

> **【R-HIGH】** 千万不要重新启用 Proxy。Proxy 保持禁用是为了**防止 Unity 调用事件并运行相同逻辑两次**。

如果 Proxy 上调用 `GetComponentInChildren` 等方法且**不包含禁用的行为**，**不会返回 Proxies**。

---

## 2. U# 与常规 C# 行为的关键差异

### 2.1 UdonSharpBehaviour 不是 UdonBehaviour

**【FACT】** 在 UdonSharp 代码中，可将 UdonBehaviour 视为 UdonSharpBehaviour（内部表示为同一对象）。

**【FACT】** 技术上，UdonSharpBehaviour **不**继承自 UdonBehaviour。

**【最佳实践】** 在 UdonSharp 中**始终**使用 `UdonSharpBehaviour` 作为变量类型，**不要**使用 `UdonBehaviour`，除非需要支持 Udon Graph 资源。

```csharp
// ✅ 推荐
[SerializeField] private MyUdonScript _myScript;

// ❌ 避免（除非需要支持 Graph 资产）
[SerializeField] private UdonBehaviour _myScript;
```

### 2.2 Proxy 引用自动处理仅对 UdonSharpBehaviour 变量生效

**【FACT】** 只有 UdonSharpBehaviour 类型的变量会自动处理其 Proxy 引用。

**【FACT】** 在 Proxy 行为中引用另一个 Proxy 行为时，引用会**自动转换**为 UdonBehaviour 引用。

| 字段类型 | Proxy 引用处理 |
|---------|--------------|
| `UdonSharpBehaviour`（或子类） | ✅ 自动处理 |
| `UdonBehaviour` | ❌ 填充为底层 UdonBehaviour 引用 |
| `Component` | ❌ 填充为底层 UdonBehaviour 引用 |

> **【R-HIGH】** 若变量类型**不是** UdonSharpBehaviour 或其子类，**构建时**引用会被**清空为 null**。

### 2.3 Proxies 始终禁用

**【FACT】** Proxies 保持禁用以防止 Unity 调用事件并运行逻辑两次。**永远不要重新启用** Proxy 行为。

**【R-HIGH】** 由于 Proxy 行为是禁用的，调用 `GetComponentInChildren` 等方法时，**不**会返回 Proxies（除非传 `includeInactive: true`）。

---

## 3. 自定义 Inspector

### 3.1 基础结构

**【FACT】** 大多数情况下，编写 U# 的自定义 Inspector 与编写普通自定义 Inspector **完全相同**。

**【FACT】** 必须用 `Editor` 派生类并添加 `[CustomEditor(typeof(YourBehaviour))]` attribute。

### 3.2 排除 Editor 代码

**【R-CRITICAL】** Editor 代码**必须**从 World 构建中排除。包含 Editor 库会导致**构建失败**。

**两种推荐方法**：

#### 方法 A: Editor 文件夹

```
Assets/MyWorld/
├── MyBehaviour.cs           # 运行时
└── Editor/
    └── MyBehaviourEditor.cs  # 编辑器（自动排除）
```

#### 方法 B: `#if UNITY_EDITOR` 包裹

```csharp
#if UNITY_EDITOR
[CustomEditor(typeof(CustomInspectorBehaviour))]
public class CustomInspectorEditor : Editor
{
    ...
}
#endif
```

### 3.3 同一文件中的 Inspector

**【FACT】** 若要在 U# 脚本**同一文件**中编写 Inspector，必须用 `COMPILER_UDONSHARP` 预处理器定义**防止 UdonSharp 解析 Editor 代码**。

```csharp
public class CustomInspectorBehaviour : UdonSharpBehaviour
{
    ...
}

#if !COMPILER_UDONSHARP && UNITY_EDITOR
[CustomEditor(typeof(CustomInspectorBehaviour))]
public class CustomInspectorEditor : Editor
{
    ...
}
#endif
```

> **【R-HIGH】** `COMPILER_UDONSHARP` 预处理器定义**仅在 UdonSharpBehaviour 所在脚本中**为 `true`。外部脚本（不含 UdonSharpBehaviour）**永远不会**将 `COMPILER_UDONSHARP` 设为 `true`。

> **【R-HIGH】** 不要用 `COMPILER_UDONSHARP` 或 `UNITY_EDITOR` **条件性增删 UdonSharpBehaviour 的字段**。这会导致**未定义行为**。

### 3.4 必需的头部绘制

**【FACT】** 自定义 Inspector 的 `OnInspectorGUI` 必须以以下代码开头：

```csharp
public override void OnInspectorGUI()
{
    if (UdonSharpGUI.DrawDefaultUdonSharpBehaviourHeader(target)) return;
    // ... 自定义 Inspector 代码
}
```

**【FACT】** `DrawDefaultUdonSharpBehaviourHeader()` 绘制的内容包括：
- "转换为 Behaviour" 按钮（C# 脚本）
- Program Asset 字段
- 同步设置
- 交互设置
- 工具菜单

也可**单独绘制**各个部分（参考 `DrawDefaultUdonSharpBehaviourHeader()` 的实现）。

### 3.5 完整示例

```csharp
using UnityEngine;
using VRC.SDK3.Components;
using VRC.SDKBase;
using VRC.Udon;

#if !COMPILER_UDONSHARP && UNITY_EDITOR
using UnityEditor;
using UdonSharpEditor;
#endif

namespace UdonSharp.Examples.Inspectors
{
    /// <summary>
    /// 带有自定义 Inspector 的示例行为
    /// </summary>
    public class CustomInspectorBehaviour : UdonSharpBehaviour
    {
        public string stringVal;
        
        private void Update()
        {
            Debug.Log($"CustomInspectorBehaviour: {stringVal}");
        }
    }

    #if !COMPILER_UDONSHARP && UNITY_EDITOR
    [CustomEditor(typeof(CustomInspectorBehaviour))]
    public class CustomInspectorEditor : Editor
    {
        public override void OnInspectorGUI()
        {
            // 绘制默认 U# 头部（转换按钮、Program Asset、同步设置等）
            if (UdonSharpGUI.DrawDefaultUdonSharpBehaviourHeader(target)) return;
            
            CustomInspectorBehaviour inspectorBehaviour = (CustomInspectorBehaviour)target;
            EditorGUI.BeginChangeCheck();
            
            // 简单的字符串字段修改（含 Undo 处理）
            string newStrVal = EditorGUILayout.TextField("String Val", inspectorBehaviour.stringVal);
            if (EditorGUI.EndChangeCheck())
            {
                Undo.RecordObject(inspectorBehaviour, "Modify string val");
                inspectorBehaviour.stringVal = newStrVal;
            }
        }
    }
    #endif
}
```

---

## 4. Handles 与 Gizmos

### 4.1 使用 Handles

**【FACT】** 与编写自定义 Inspector GUI 类似，基本是**自动处理**的。在 `Editor` 上使用 `OnSceneGUI` 事件即可。

### 4.2 使用 Gizmos

**【FACT】** Gizmos 需要**特殊处理**才能按预期工作。

**关键点**：
- 用 `#if !COMPILER_UDONSHARP && UNITY_EDITOR` 包裹 `OnDrawGizmos` 事件
- `OnDrawGizmos` 和 `OnDrawGizmosSelected` 事件**应在 behaviour 自身**中
- Gizmos 绘制使用附加到所有 UdonBehaviours 的 Proxy behaviour

**Proxy 同步调用**：

```csharp
// 调用此方法
UdonSharpEditorUtility.CopyUdonToProxy(this);

// 或等效的（模拟 Unity SerializedObject API）
this.UpdateProxy();

// 不要两者都调用，会做冗余工作
```

> **【R-MED】** Gizmos 事件**不**由 UdonSharp 管理，需手动调用 `UpdateProxy()` 或 `CopyUdonToProxy()` 保持 Proxy 最新。

**示例参考**：[UdonSharp GitHub CustomInspectorChildBehaviour.cs](https://github.com/vrchat-community/UdonSharp/blob/master/Packages/com.vrchat.UdonSharp/Samples~/CustomInspectors/CustomInspectorChildBehaviour.cs#L33)

---

## 5. 非 Inspector 的 Editor 脚本

### 5.1 添加 UdonSharpBehaviour

**【FACT】** 在 GameObject 上添加新的 UdonSharpBehaviour **非常简单**：

```csharp
GameObject targetGameObject = ...;
MyComponentType newComponent = targetGameObject.AddUdonSharpComponent<MyComponentType>();
```

**【FACT】** `newComponent` 是 MyComponentType 的有效 UdonSharpBehaviour Proxy，可像普通 C# 组件一样操作。

**支持 Undo 的版本**：

```csharp
GameObject targetGameObject = ...;
MyComponentType newComponent = UdonSharpUndo.AddComponent<MyComponentType>(targetGameObject);
```

### 5.2 获取现有 UdonSharpBehaviour

**【FACT】** UdonSharp 提供了 `GameObject` 的**扩展方法**：

| 普通 C# | UdonSharp Editor 等效 |
|--------|------------------|
| `GetComponent<T>()` | `GetUdonSharpComponent<T>()` |
| `GetComponents<T>()` | `GetUdonSharpComponents<T>()` |
| `GetComponentInChildren<T>()` | `GetUdonSharpComponentInChildren<T>()` |
| `GetComponentsInChildren<T>()` | `GetUdonSharpComponentsInChildren<T>()` |

```csharp
GameObject sourceGameObject = ...;
MyComponentType[] myComponents = sourceGameObject.GetUdonSharpComponentsInChildren<MyComponentType>();
```

### 5.3 修改 UdonSharpBehaviour

**【FACT】** 必须**手动管理** Proxy ↔ Udon 同步：

```csharp
MyComponentType myComponent = ...;

// 仅在持有持久引用时需要更新 Proxy
myComponent.UpdateProxy();

// 修改字段
myComponent.myFloatField += 5f;

// 将 Proxy 修改应用到 Udon
myComponent.ApplyProxyModifications();
```

**【推断】** 类比 Unity 的 `SerializedObject`：
- `UpdateProxy()` ↔ `serializedObject.Update()`
- `ApplyProxyModifications()` ↔ `serializedObject.ApplyModifiedProperties()`

---

## 6. 销毁 UdonSharpBehaviour

**【FACT】** **必须**使用 `UdonSharpEditorUtility.DestroyImmediate()` 销毁 UdonSharpBehaviour，并删除其底层 UdonBehaviour。

```csharp
UdonSharpEditorUtility.DestroyImmediate(target);
```

> **【R-MED】** 使用 `Object.DestroyImmediate()` 可能**不会**清理底层 UdonBehaviour，导致资源泄漏或构建异常。

---

## 7. 完整 API 速查

| 操作 | API | 命名空间 |
|------|-----|---------|
| 添加 U# 组件 | `gameObject.AddUdonSharpComponent<T>()` | `UdonSharpEditor` |
| 支持 Undo 的添加 | `UdonSharpUndo.AddComponent<T>(gameObject)` | `UdonSharpEditor` |
| 获取组件 | `gameObject.GetUdonSharpComponent<T>()` | `UdonSharpEditor` |
| 获取所有组件 | `gameObject.GetUdonSharpComponents<T>()` | `UdonSharpEditor` |
| 同步 Udon → Proxy | `component.UpdateProxy()` 或 `UdonSharpEditorUtility.CopyUdonToProxy(this)` | `UdonSharpEditor` |
| 同步 Proxy → Udon | `component.ApplyProxyModifications()` | `UdonSharpEditor` |
| 销毁 U# 组件 | `UdonSharpEditorUtility.DestroyImmediate(component)` | `UdonSharpEditor` |
| 绘制默认头部 | `UdonSharpGUI.DrawDefaultUdonSharpBehaviourHeader(target)` | `UdonSharpEditor` |

---

## 8. 与已有知识库的关系

| 现有知识库 | 应补充/引用 |
|-----------|----------|
| `memory/api/udonsharp-runtime.md` | **核心** — Proxy 系统、构建时组件处理与本文密切相关 |
| `memory/sources/vpm-package-template.md` | VPM Package 中 Editor 文件夹组织 |
| `memory/world/udon/vm-and-assembly.md` | Udon VM 与 Editor 集成 |

---

## 9. 风险与未知

### 风险

- **【R-CRITICAL】** Editor 代码未用 `UNITY_EDITOR` / Editor 文件夹排除 → **构建失败**
- **【R-HIGH】** 在同一文件用 `COMPILER_UDONSHARP` 条件性增删 U# 字段 → 未定义行为
- **【R-HIGH】** 用 `Object.DestroyImmediate()` 销毁 U# 组件 → 底层 UdonBehaviour 残留
- **【R-MED】** 重新启用 Proxy 行为 → 事件重复执行
- **【R-MED】** Gizmos 未调用 `UpdateProxy()` → 显示过期数据
- **【R-LOW】** 字段类型为 `Component` 或 `UdonBehaviour` 存储 Proxy 引用 → 构建时引用丢失

### 未知

- **【未确认】** `UdonSharpGUI` 提供的所有可单独绘制的方法签名
- **【未确认】** `UdonSharpUndo` 的完整 API（除 `AddComponent` 外）
- **【未确认】** Handles 在不同 Inspector 上下文（Hierarchy vs Project）下的差异
