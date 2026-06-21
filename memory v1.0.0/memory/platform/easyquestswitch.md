# EasyQuestSwitch 知识库

> 来源: deepwiki.com/vrchat-community/EasyQuestSwitch

---

## 目录

1. [概述](#1-概述)
2. [核心架构](#2-核心架构)
3. [类型处理系统](#3-类型处理系统)
4. [SharedField 系统](#4-sharedfield-系统)
5. [UI 集成](#5-ui-集成)
6. [本地化系统](#6-本地化系统)
7. [Bakery 集成](#7-bakery-集成)
8. [自定义类型扩展](#8-自定义类型扩展)

---

## 1. 概述

EasyQuestSwitch 是 VRChat 官方社区（vrchat-community）开发的 Unity 编辑器工具，专门帮助 VRChat 世界创作者自动化处理 **PC 平台和 Quest（Android）平台**之间的组件切换。

### 1.1 核心功能

| 功能 | 说明 |
|------|------|
| **自动平台切换** | 监听 Unity 的构建目标变更，自动应用平台特定配置 |
| **无需手动调整** | 在 PC ↔ Android/Quest 切换时，自动更新场景组件 |
| **集中数据管理** | 通过 EQS_Data 作为中央控制器协调各组件 |
| **反射式发现** | 自动发现并实例化类型处理器，无需手动注册 |

### 1.2 系统架构概览

```
EQS_Data          ← 中央控制器
├── Type_Base     ← 抽象处理器基类
├── Type_Material ← 材质处理
├── Type_Light    ← 光照处理
├── Type_Bakery_* ← Bakery 光照组件
└── Shared* Types ← 平台共享值存储

EQS_Window        ← 主编辑器窗口
EQS_HierarchyController ← 层级视图图标
EQS_PropertyDrawers     ← 检查器 UI
EQS_Localization        ← 多语言支持
```

---

## 2. 核心架构

### 2.1 EQS_Data 控制器

EQS_Data 是整个系统的核心 MonoBehaviour，负责：
- 存储组件引用列表
- 管理类型处理器生命周期
- 监听平台切换事件
- 协调处理器的 Setup 和 Process 调用

**关键方法**:
| 方法 | 用途 |
|------|------|
| `ValidateData()` | 验证并初始化组件列表 |
| `Setup()` | 调用所有处理器的 Setup |
| `OnChangedBuildTarget()` | 平台切换时自动触发 |
| `Process(BuildTarget)` | 应用目标平台的配置 |

### 2.2 工作流程

```
1. 设置阶段
   ├── 打开 EQS 窗口
   ├── 拖放组件到对象列表
   ├── ValidateData() & Setup()
   └── 读取当前属性，存储到 Shared* 字段

2. 平台切换
   ├── Unity 构建目标变更
   ├── OnChangedBuildTarget() 触发
   ├── Process(buildTarget) 调用
   └── 每个处理器应用平台特定值
```

---

## 3. 类型处理系统

### 3.1 类层次结构

```
Type_Base (抽象基类)
├── Type_Behaviour (MonoBehaviour 组件基类)
│   └── Type_Light
├── Type_Material
└── Type_Bakery_* (Bakery 专用处理器)
    ├── Type_Bakery_PointLight
    ├── Type_Bakery_SkyLight
    ├── Type_Bakery_DirectLight
    └── Type_Bakery_LightMesh
```

### 3.2 类型发现机制

EasyQuestSwitch 使用**反射**自动发现处理器类：

1. 调用 `Assembly.GetExecutingAssembly().GetTypes()`
2. 过滤 `EasyQuestSwitch.Types` 命名空间
3. 查找包含 `type` 字段的类（使用 BindingFlags）
4. 匹配目标组件类型（精确匹配 → 子类匹配）
5. 实例化处理器并调用 Setup()

### 3.3 处理器接口

所有处理器必须实现：

```csharp
// 初始化：从组件读取当前值
public abstract void Setup(Object type);

// 处理：根据平台应用配置
public abstract void Process(Object type, BuildTarget buildTarget);
```

---

## 4. SharedField 系统

SharedField 是 EasyQuestSwitch 的核心数据结构，用于**存储平台特定值**。

### 4.1 可用类型

| 类型 | 对应 Unity 属性 | 示例 |
|------|----------------|------|
| SharedBool | bool | `component.enabled` |
| SharedColor | Color | `material.color` |
| SharedFloat | float | `light.intensity` |
| SharedInt | int | `light.samples` |
| SharedShader | Shader | `material.shader` |

### 4.2 使用模式

```csharp
// 声明
public SharedFloat intensity = new SharedFloat();

// Setup（读取当前值）
intensity.Setup(component.intensity);

// Process（应用平台值）
component.intensity = intensity.Get(buildTarget);
```

### 4.3 内部结构

每个 SharedField 内部存储 PC 和 Quest 两个值：

```csharp
public T Get(BuildTarget target) {
    return target == BuildTarget.Android ? questValue : pcValue;
}
```

---

## 5. UI 集成

### 5.1 EQS_Window

主编辑器窗口，提供：
- 组件列表管理（拖放）
- 平台切换按钮
- 设置/验证功能

### 5.2 EQS_HierarchyController

层级视图集成：
- 为 EQS 管理的对象添加图标标记
- 快速识别哪些对象受 EasyQuestSwitch 管理

### 5.3 EQS_PropertyDrawers

检查器自定义属性抽屉：
- 在组件检查器中显示 Shared* 字段
- 直接编辑 PC/Quest 分离的值

---

## 6. 本地化系统

### 6.1 支持语言

| 语言 | 代码 | 贡献者 |
|------|------|--------|
| English | en | Jordo |
| 日本語 | jp | Tony_Lewis |
| 简体中文 | cn | CallMeReznov |
| Español | es | RadAngelZero |
| Français | fr | Jordo |

### 6.2 本地化文件格式

JSON 格式存储在 `Runtime/Resources/EQS_Localizations/`：

```json
{
  "code": "cn",
  "displayName": "Simplified Chinese",
  "author": "CallMeReznov",
  "settings": {
    "SettingsButton": "设置",
    "SettingsLanguage": "语言"
  },
  "popup": {
    "PopupDeleteWarning": "确定要删除吗？",
    "PopupAccept": "是",
    "PopupDecline": "否"
  },
  "log": {
    "LogSwitchSuccess": "[EasyQuestSwitch] 切换成功",
    "LogSwitchFailure": "[EasyQuestSwitch] 切换失败: {0}"
  }
}
```

### 6.3 API 使用

```csharp
// 设置语言
EQS_Localization.SetLanguage("cn");
EQS_Localization.SetLanguage(0);  // 按索引

// 访问本地化字符串
EQS_Localization.Current.SettingsButton  // "设置"
EQS_Localization.Current.LogSwitchSuccess  // "[EasyQuestSwitch] 切换成功"
```

---

## 7. Bakery 集成

EasyQuestSwitch 提供了 Bakery 光照组件的 PC/Quest 切换支持。

### 7.1 支持的 Bakery 组件

| 处理器 | 支持属性 |
|--------|----------|
| Type_Bakery_PointLight | Range, Color, Samples |
| Type_Bakery_SkyLight | Intensity, Color |
| Type_Bakery_DirectLight | Intensity, Color |
| Type_Bakery_LightMesh | Intensity, Color |

### 7.2 与知识库 Bakery 的关系

> **补充说明**: EasyQuestSwitch 的 Bakery 集成与 `memory/world/bakery/index.md` 是**互补关系**：
> - 知识库 Bakery = 光照烘焙技术文档
> - EasyQuestSwitch = Bakery 组件的 PC/Quest 切换方案

### 7.3 使用场景

在 VRChat World 中，Bakery 光照通常需要针对 PC 和 Quest 平台使用不同配置：

| 平台 | 建议配置 |
|------|----------|
| **PC** | 高质量光照、高 Samples、高分辨率 |
| **Quest** | 降低 Samples、降低分辨率、优化性能 |

---

## 8. 自定义类型扩展

### 8.1 添加自定义处理器的步骤

1. **创建类文件**
   - 位置: `Runtime/EQS_Types/` 或子目录
   - 命名空间: `EasyQuestSwitch.Types`
   - 类名: `Type_[组件名]`

2. **继承基类**
   - `Type_Base`: 非 MonoBehaviour 组件
   - `Type_Behaviour`: MonoBehaviour 组件

3. **声明目标组件字段**
   ```csharp
   [System.NonSerialized]
   private MyComponent type;
   ```

4. **实现 Shared* 字段**
   ```csharp
   public SharedFloat myProperty = new SharedFloat();
   ```

5. **实现 Setup 和 Process**
   ```csharp
   public override void Setup(Object type) {
       this.type = (MyComponent)type;
       myProperty.Setup(this.type.myProperty);
   }

   public override void Process(Object type, BuildTarget buildTarget) {
       this.type.myProperty = myProperty.Get(buildTarget);
   }
   ```

### 8.2 模板代码

```csharp
using UnityEngine;
using EasyQuestSwitch.Types;

namespace EasyQuestSwitch.Types {
    [AddComponentMenu("")]
    public class Type_MyComponent : Type_Behaviour {
        [System.NonSerialized]
        private MyComponent type;

        public SharedFloat myFloat = new SharedFloat();
        public SharedBool myBool = new SharedBool();

        public override void Setup(Object type) {
            this.type = (MyComponent)type;
            myFloat.Setup(this.type.myFloat);
            myBool.Setup(this.type.myBool);
        }

        public override void Process(Object type, BuildTarget buildTarget) {
            this.type.myFloat = myFloat.Get(buildTarget);
            this.type.myBool = myBool.Get(buildTarget);
        }
    }
}
```

---

## 参考文件

| 文件 | 说明 |
|------|------|
| `Runtime/EQS_Data.cs` | 中央控制器 |
| `Runtime/EQS_Localization.cs` | 本地化系统 |
| `Runtime/EQS_Types/Type_Base.cs` | 抽象基类 |
| `Runtime/EQS_Types/Type_Material.cs` | 材质处理器 |
| `Runtime/EQS_Types/Type_Light.cs` | 灯光处理器 |
| `Runtime/EQS_Types/Bakery/*.cs` | Bakery 处理器 |
| `Editor/EQS_Window.cs` | 主编辑器窗口 |
| `Editor/EQS_HierarchyController.cs` | 层级集成 |
| `Editor/EQS_PropertyDrawers.cs` | 属性抽屉 |

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-06-10 | 初始创建，来源 deepwiki.com |