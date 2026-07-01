---
title: "VRChat Constraints 知识库"
category: avatar
knowledge_level: applied
status: active
source: "creators.vrchat.com/common-components/constraints/"
source_type: community
version: 1.0
last_review: 2026-06-05
confidence: High
tags:
  - avatar
  - constraint
  - udonsharp
aliases:
  - "VRC Constraints"
  - 约束系统
  - "Avatar Constraints"
  - "VRC 约束"
related:
  - animator-system.md
  - modular-avatar.md
  - teaching-methodology.md
  - tex-trans-tool.md
  - accessories.md
---

---
# VRChat Constraints 知识库


---

## 目录

1. [概述](#1-概述)
2. [约束类型](#2-约束类型)
3. [高级设置](#3-高级设置)
4. [性能](#4-性能)
5. [使用技巧](#5-使用技巧)
6. [Constraints API](#6-constraints-api)

---

## 1. 概述

VRChat 提供自定义约束系统，允许 Avatar 或 World 中的 Transform 相对于其他 Transform 进行移动、旋转和缩放。

### 与 Unity Constraints 的区别

| 方面 | VRChat Constraints | Unity Constraints |
|------|-------------------|-------------------|
| Avatar | ✅ 推荐使用 | 自动转换 |
| World | 均可 | 均可 |
| 性能 | 更好 | 可能性能问题 |
| 功能 | 更多可选功能 | 基础功能 |

**重要**: Avatar 必须使用 VRChat Constraints。如果包含 Unity Constraints，上传时自动转换为 VRChat Constraints。

### 命名空间

```
VRC.SDK3.Dynamics.Constraint.Components
VRC.Dynamics
```

---

## 2. 约束类型

### 2.1 VRCAimConstraint（目标约束）

旋转目标 Transform，使其朝向源。可自定义前进方向。

**参数**:
- `Is Active` - 控制约束是否评估
- `Weight` - 整体权重 (0-1)
- `Aim Vector` - 控制朝向源的轴
- `Up Vector` - 控制向上轴
- `World Up Type`:
  - Scene Up (Y轴)
  - Object Up (指定对象)
  - Object Up Rotation (局部空间)
  - Vector (世界空间向量)
  - None (无)

**Constraint Settings**:
- `Rotation At Rest` - 权重为0时的旋转
- `Rotation Offset` - 结果偏移
- `Lock` - 锁定 At Rest 和 Offset
- `Freeze Rotation Axes` - 冻结特定轴

### 2.2 VRCLookAtConstraint（注视约束）

简化的 Aim Constraint，使目标 Transform 的正Z轴朝向源。

**参数**:
- `Is Active` - 控制约束是否评估
- `Weight` - 整体权重 (0-1)
- `Use Up Object` - 是否使用单独的对象控制翻滚
- `Roll` - 绕Z轴的角度（无Up Object时）
- `World Up Object` - 翻滚目标对象

### 2.3 VRCParentConstraint（父约束）

移动和旋转目标 Transform，如同其是源的子对象。

**参数**:
- `Is Active` - 控制约束是否评估
- `Weight` - 整体权重 (0-1)

**Constraint Settings**:
- `Position/Rotation At Rest` - 静止位置/旋转
- `Position/Rotation Offset` - 偏移量
- `Lock` - 锁定设置
- `Freeze Position/Rotation Axes` - 冻结轴

**注意**: 每个源的偏移是独立设置的。

### 2.4 VRCPositionConstraint（位置约束）

改变目标 Transform 的位置以匹配源的位置。

**参数**:
- `Is Active` - 控制约束是否评估
- `Weight` - 整体权重 (0-1)

**Constraint Settings**:
- `Position At Rest` - 静止位置
- `Position Offset` - 位置偏移
- `Lock` - 锁定设置
- `Freeze Position Axes` - 冻结轴

### 2.5 VRCRotationConstraint（旋转约束）

改变目标 Transform 的旋转以匹配源的旋转。

**参数**:
- `Is Active` - 控制约束是否评估
- `Weight` - 整体权重 (0-1)

**Constraint Settings**:
- `Rotation At Rest` - 静止旋转
- `Rotation Offset` - 旋转偏移
- `Lock` - 锁定设置
- `Freeze Rotation Axes` - 冻结轴

### 2.6 VRCScaleConstraint（缩放约束）

改变目标 Transform 的缩放以匹配源的缩放。

**参数**:
- `Is Active` - 控制约束是否评估
- `Weight` - 整体权重 (0-1)

**Constraint Settings**:
- `Scale At Rest` - 静止缩放
- `Scale Offset` - 缩放偏移
- `Lock` - 锁定设置
- `Freeze Scale Axes` - 冻结轴

---

## 3. 高级设置

### Target Transform

更改约束目标的 Transform。默认为空，约束应用于附加到的 Transform。

**限制**: 不能通过动画更改此设置。

### Solve In Local Space

- **关闭**: 世界空间求解（匹配源的**世界**位置/旋转/缩放）
- **开启**: 局部空间求解（匹配源的**局部**位置/旋转/缩放）

**用途**: 假肢体、跟随骨骼链等。

### Freeze To World

启用后，约束忽略所有源，锁定目标 Transform 在世界空间。

**用途**: 在世界中放下物体，物体不会跟随 Avatar 移动。

**限制**:
- 必须冻结所有轴才能完全停止
- 与禁用约束组件不同：
  - 禁用约束：Transform 停止在局部空间移动，但仍跟随父对象
  - Freeze To World：主动移动 Transform 防止在世界空间移动

### Rebake Offsets When Unfrozen

启用后，解冻时重新计算相对于源的偏移（而非保持原始偏移）。

---

## 4. 性能

### Avatar 性能分类

| 分类 | 说明 |
|------|------|
| **Constraint Count** | 约束总数（含禁用），VRChat + Unity |
| **Constraint Depth** | 最长约束链的深度 |

### Constraint Depth 说明

约束链按特定顺序逐个评估，从链底部到顶部。

**示例**: 3个旋转约束链 = 深度为3

```
约束1 (臀部) → 约束2 (膝盖) → 约束3 (脚)
     深度 1        深度 2        深度 3
```

**优化建议**:
- 减少最长链的长度
- 关注最长链，非总链数
- 多条深度为3的链 = 总体深度仍为3（如果无更长链）

### Unity Constraints 影响

- Unity Constraints 可能导致深度被**高估**
- 建议使用 SDK Control Panel 的 Auto Fix 转换所有 Unity Constraints

---

## 5. 使用技巧

### 故障排除

1. 检查 `Is Active` 是否启用
2. 检查组件本身是否启用
3. 检查 `Lock` 是否启用

### 限制

1. **Target Transform 不能被动画或 Udon 更改**（性能缓存）
2. **不要动画更改约束引用的 Transform**（性能问题）
   - 动画 Transform 的位置/旋转/缩放是可以的
3. **Avatar 上不能动画单个源的变换引用**
   - 替代方案：设置多个源，动画它们的权重

### 按钮功能

| 按钮 | 功能 |
|------|------|
| **Activate** | 保存当前偏移，激活并锁定约束 |
| **Zero out** | 重置偏移为默认值，激活并锁定约束 |

---

## 6. Constraints API

### 命名空间

```csharp
using VRC.SDK3.Dynamics.Constraint.Components;
using VRC.Dynamics;
```

### 通用属性和方法

#### ApplyConfigurationChanges()

修改约束后**必须调用此方法**，否则更改可能不生效。

```csharp
constraint.PositionOffset = new Vector3(1, 0, 0);
constraint.ApplyConfigurationChanges();
```

#### IsActive

- `bool`: 约束是否正在评估

#### GlobalWeight

- `float`: 全局权重

#### Locked

- `bool`: 约束是否锁定（播放模式始终锁定）

#### Sources

- `VRCConstraintSourceKeyableList`: 源列表

**注意**: Avatar 上只能动画前16个源元素。

```csharp
// 修改源权重
for (int i = 0; i < constraint.Sources.Count; i++)
{
    VRCConstraintSource source = constraint.Sources[i];
    source.Weight = UnityEngine.Random.value;
    constraint.Sources[i] = source;
}

// 添加源
VRCConstraintSource source = new VRCConstraintSource(transform, 1.0f);
constraint.Sources.Add(source);

// 移除源
constraint.Sources.Remove(source);
constraint.Sources.RemoveAt(i);
```

#### TargetTransform

- `Transform`: 受约束影响的 Transform

#### SolveInLocalSpace

- `bool`: 是否在局部空间求解

#### FreezeToWorld

- `bool`: 是否冻结在世界空间

#### RebakeOffsetsWhenUnfrozen

- `bool`: 解冻时是否重新计算偏移

#### ActivateConstraint()

激活并锁定约束，保持当前偏移。

#### ZeroConstraint()

激活并锁定约束，重置偏移。

### At-Rest 和 Offset 值

每个约束类型有不同的 At-Rest 和 Offset 值：

| 约束类型 | At-Rest | Offset |
|----------|---------|--------|
| Position | Vector3 | Vector3 |
| Rotation | Quaternion | Quaternion |
| Scale | Vector3 | Vector3 |
| Parent | Vector3 + Quaternion | Vector3 + Quaternion |
| Aim | Quaternion | Quaternion |
| Look At | Quaternion | Quaternion |

### 约束类型特定 API

#### PositionConstraint

```csharp
Vector3 PositionAtRest { get; set; }
Vector3 PositionOffset { get; set; }
bool GetPositionAxisIsFrozen(int axis);
void SetPositionAxisIsFrozen(int axis, bool value);
```

#### RotationConstraint

```csharp
Quaternion RotationAtRest { get; set; }
Quaternion RotationOffset { get; set; }
bool GetRotationAxisIsFrozen(int axis);
void SetRotationAxisIsFrozen(int axis, bool value);
```

#### ScaleConstraint

```csharp
Vector3 ScaleAtRest { get; set; }
Vector3 ScaleOffset { get; set; }
bool GetScaleAxisIsFrozen(int axis);
void SetScaleAxisIsFrozen(int axis, bool value);
```

#### ParentConstraint

```csharp
Vector3 PositionAtRest { get; set; }
Quaternion RotationAtRest { get; set; }
Vector3 PositionOffset { get; set; }
Quaternion RotationOffset { get; set; }
bool GetPositionAxisIsFrozen(int axis);
void SetPositionAxisIsFrozen(int axis, bool value);
bool GetRotationAxisIsFrozen(int axis);
void SetRotationAxisIsFrozen(int axis, bool value);
```

#### AimConstraint

```csharp
Quaternion RotationAtRest { get; set; }
Quaternion RotationOffset { get; set; }
bool GetRotationAxisIsFrozen(int axis);
void SetRotationAxisIsFrozen(int axis, bool value);
```

#### LookAtConstraint

```csharp
Quaternion RotationAtRest { get; set; }
Quaternion RotationOffset { get; set; }
bool GetRotationAxisIsFrozen(int axis);
void SetRotationAxisIsFrozen(int axis, bool value);
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-06-05 | 初始创建 |

## 来源

- creators.vrchat.com/common-components/constraints/
- creators.vrchat.com/common-components/constraints/vrc-*-constraint
- creators.vrchat.com/common-components/constraints/constraints-api