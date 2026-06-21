# UdonSharpBehaviour Runtime System

> Type: API REFERENCE
> Source: vrchat-community/UdonSharp (DeepWiki, commit 5d1a2b3d) + VRChat 官方文档
> Confidence: High
> Last Updated: 2026-06-15
> **关联参考**:`memory/world/udon/vm-and-assembly.md` - EXTERN 签名规则、Udon Types 命名、9 Opcodes 详解

---

## 概述

`UdonSharpBehaviour` 是所有 UdonSharp 脚本的基类，提供 C# 代码与 VRChat Udon 运行时系统之间的桥梁接口。

---

## 变量管理系统

### GetProgramVariable / SetProgramVariable

通过反射访问脚本字段，支持私有字段：

```csharp
// 获取字段值
object GetProgramVariable(string name);

// 设置字段值
void SetProgramVariable(string name, object value);
```

**实现机制**：
- 使用 `BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance`
- 支持访问 private 字段
- 通过 `GetField()` + `GetValue()` / `SetValue()` 实现

**使用场景**：
- 跨 UdonSharpBehaviour 组件通信
- 动态字段访问
- 与 FieldChangeCallback 配合使用

```csharp
// 示例：跨组件通信
UdonBehaviour target = otherObject.GetComponent<UdonBehaviour>();
target.SetProgramVariable("myField", 42);
target.SendCustomEvent("OnValueChanged");
```

---

## FieldChangeCallback 属性

当字段通过网络同步或 `SetProgramVariable` 修改时自动触发回调：

```csharp
[UdonSynced, FieldChangeCallback(nameof(OnToggleChanged))]
private bool _syncedToggle;

public bool SyncedToggle {
    set {
        _syncedToggle = value;
        toggleObject.SetActive(value);
    }
    get => _syncedToggle;
}

private void OnToggleChanged() {
    // 自动调用
}
```

### 关键行为

| 行为 | 说明 |
|------|------|
| 触发条件 | 网络同步 + `SetProgramVariable` 调用 |
| 不触发条件 | 同脚本内直接字段赋值 |
| 编译要求 | backing field 必须通过 property setter 修改 |

---

## 类型识别系统

运行时类型检查和比较：

| 方法 | 返回类型 | 说明 |
|------|---------|------|
| `GetUdonTypeID()` | long | 获取实例类型 ID |
| `GetUdonTypeID<T>()` | long | 获取泛型类型 ID |
| `GetUdonTypeName()` | string | 获取实例类型名 |
| `GetUdonTypeName<T>()` | string | 获取泛型类型名 |

**用途**：
- 动态行为交互时的类型检查
- UdonSharpBehaviour 子类识别
- 调试和日志记录

```csharp
long typeId = GetUdonTypeID();           // 实例类型 ID
long typeId2 = GetUdonTypeID<MyClass>(); // 泛型版本
string typeName = GetUdonTypeName();     // "MyClass"
```

---

## 序列化系统

### Odin Serializer

UdonSharp 使用 **Odin Serializer** 处理 Unity 标准序列化不支持的复杂数据类型：

- Jagged arrays（锯齿数组）
- Nested collections（嵌套集合）
- 复杂数据结构

**知识库关联**：`memory/rules/udonsharp-language-limits.md` 禁止使用 `List<T>` 等集合类，但支持通过 Odin Serializer 实现复杂数据序列化。

---

## 代理系统（Editor Integration）

### 核心概念

UdonSharp 使用代理系统维持编辑器时间和运行时状态的同步：

```
_udonSharpBackingUdonBehaviour 字段
    ↓
编辑器时间 C# 对象 ↔ 运行时 UdonBehaviour
```

### 代理生命周期操作

| 操作 | 方法 | 说明 |
|------|------|------|
| 创建 | `CreateProxyBehaviour()` | 从 UdonBehaviour 创建代理 |
| 同步→ | `CopyProxyToUdon()` | 将 C# 代理数据同步到 UdonBehaviour |
| 同步← | `CopyUdonToProxy()` | 将 UdonBehaviour 数据同步到 C# 代理 |
| 验证 | `SanitizeProxyBehaviours()` | 确保代理/后端配对有效 |
| 清理 | `DestroyProxyBehaviour()` | 移除孤立代理 |

**使用场景**：
- 编辑器中修改脚本属性
- 运行时读取初始状态
- Prefab 变体管理

---

## 构建时组件处理

UdonSharp 在构建过程中自动处理组件转换：

| 阶段 | 操作 | 方法 |
|------|------|------|
| Pre-Build | 复制代理数据到 UdonBehaviour | `CopyProxyToUdon()` |
| Preparation | 为播放模式准备组件 | `PrepareUdonSharpBehavioursForPlay()` |
| Component Removal | 从构建中移除代理组件 | `DestroyImmediate(behaviour)` |
| Post-Build | 恢复编辑器状态 | `RunPostBuildSceneFixup()` |

---

## 相关知识

- `memory/api/events-reference.md` — Udon 事件完整参考
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制
- `memory/rules/udon-vm-architecture.md` — Udon VM 架构
- `memory/world/udon/vm-and-assembly.md` — **官方 Udon 字节码规范**(EXTERN 签名格式、Udon Types 命名规则、9 Opcodes 详解)
- `memory/world/udon/ui-events.md` — Unity UI 事件白名单(直接调用组件方法)

---

## Udon 官方文档本地化索引(2026-06-15)

> 10 个 Udon 核心单页已本地化到 `memory/world/udon/`,跨引用如下:

| 主题 | 本地化文档 |
|---|---|
| Udon 总览 | `memory/world/udon/index.md` |
| 事件执行顺序 | `memory/world/udon/event-execution-order.md` |
| Animation Events | `memory/world/udon/animation-events.md` |
| Avatar Events | `memory/world/udon/avatar-events.md` |
| Input Events | `memory/world/udon/input-events.md` |
| External URLs | `memory/world/udon/external-urls.md` |
| Image Loading | `memory/world/udon/image-loading.md` |
| String Loading | `memory/world/udon/string-loading.md` |
| AI Navigation | `memory/world/udon/ai-navigation.md` |
| Debugging Udon | `memory/world/udon/debugging-udon-projects.md` |

### 跨引用要点

- **`SetProgramVariable` 在 Input Events 上下文中**: `memory/world/udon/input-events.md` 中跨脚本通信模式
- **`SetProgramVariable` 在 String Loading 上下文中**: `memory/world/udon/string-loading.md` 中配置注入模式
- **`GetProgramVariable` 在 UI Events 上下文**: `memory/world/udon/ui-events.md` 中 UI 触发器模式
- **`FieldChangeCallback` 时序**: `memory/world/udon/event-execution-order.md` 中同步变量触发时序