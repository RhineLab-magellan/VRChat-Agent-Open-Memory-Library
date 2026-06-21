# Simple Pen System

> Udon Example Scene · 画笔系统子页面
> 源文档:https://creators.vrchat.com/worlds/examples/udon-example-scene/simple-pen-system
> 最后更新:2026-06-15

---

## 概述

Simple Pen System 是**基础画笔**的实现范式,由**两个程序**组成:

| 程序 | 同步模式 | 同步对象 |
|------|---------|---------|
| **Pen**(画笔本身)| **Continuous** | 配合 VRCPickup + VRCObjectSync |
| **Line**(每条画线)| **Manual** | `points: Vector3[]` 数组 |

> **关键设计**:Pen 用 Continuous 模式(需要频繁同步位置),Line 用 Manual 模式(不需要那么频繁)

---

## 程序结构

### Pen

**组件**:
- `VRCPickup`
- `VRCObjectSync`
- `UdonBehaviour`(Sync Mode: Continuous)

### Lines

**组件**:
- `LineRenderer`
- `UdonBehaviour`(Sync Mode: Manual)
- `[UdonSynced] Vector3[] points` — 线条点位同步数组

---

## 绘制流程

### 1. 绘制开始(Drawing Starts)

玩家 Use Pen → 触发 `OnPickupUseDown` → 执行:

```csharp
public override void OnPickupUseDown() {
    // 1. 从对象池获取一个新 Line
    Line newLine = linePool.Get();
    
    // 2. 将 Pen 持有者设为 Line 的 Owner
    Networking.SetOwner(Networking.LocalPlayer, newLine.gameObject);
    
    // 3. 设置 isDrawing = true
    isDrawing = true;
    
    // 4. 重置 Line 为两个点位(都在 penTip 位置)
    line.points[0] = penTip.position;
    line.points[1] = penTip.position;
    
    // 5. 增加 lineIndex(追踪下一条线)
    lineIndex++;
}
```

### 2. 绘制继续(Drawing Continues)

每帧 `Update` 事件执行:

```csharp
public override void Update() {
    if (!isDrawing) return;
    
    // 1. 检查 Pen 是否移动了超过 minMoveDistance
    if (Vector3.Distance(penTip.position, lastPosition) < minMoveDistance) return;
    
    // 2. 在 LineRenderer 添加 penTip 位置的新点
    AddPointToLine(penTip.position);
    
    // 3. 检查是否累积了足够点位(pointsPerUpdate)
    if (currentIndex < pointsPerUpdate) return;
    
    // 4. 调用目标 Line 的 OnUpdate
    targetLine.SendCustomEvent("OnUpdate");
}
```

**Line 的 OnUpdate(仅 Owner 端执行)**:

```csharp
public void OnUpdate() {
    // 1. 检索 Line 的当前点位
    Vector3[] currentPoints = GetLinePoints();
    
    // 2. 更新 synced points 变量
    points = currentPoints;
    
    // 3. 通知 Udon 发送数据
    RequestSerialization();
}
```

**其他用户的 OnDeserialization**(所有人接收新数据后触发):

```csharp
public override void OnDeserialization() {
    // 读取 synced points 数组 → 更新 LineRenderer 的位置
    for (int i = 0; i < points.Length; i++) {
        lineRenderer.SetPosition(i, points[i]);
    }
}
```

### 3. 绘制结束(Drawing Finishes)

玩家松开 Use 按钮 → 触发 `OnPickupUseUp`:

```csharp
public override void OnPickupUseUp() {
    isDrawing = false;
    targetLine.SendCustomEvent("OnFinish");  // 最后一次 OnUpdate 确保数据最新
}
```

---

## 关键设计模式

### 模式 1:同步模式分层

| 元素 | 模式 | 原因 |
|------|------|------|
| Pen | Continuous | 位置变化频繁(每帧移动) |
| Line | Manual | 点位变化不频繁(按累积批量更新) |

### 模式 2:对象池复用 Line

避免每次绘制都创建新 LineRenderer,提升性能。

### 模式 3:所有权转移分层

- Pen Owner = 持笔玩家(VRCPickup 自动管理)
- Line Owner = 持笔玩家(每次新 Line 转移所有权)
- 其他用户 = 接收 OnDeserialization 后更新本地 LineRenderer

### 模式 4:Manual Sync 批量更新

`pointsPerUpdate` 阈值避免每帧调用 RequestSerialization,**减少网络流量**。

### 模式 5:OnDeserialization 同步更新

> **注**:Vector3[] 数组同步需要 OnDeserialization 处理(参考 [index.md#cubearraysync](index.md#七cubearraysync数组同步) 同样模式)

---

## 限制与扩展点

- **无 Persistence 集成**:绘制结果**不持久化**,重进 World 丢失
- **性能瓶颈**:极长 Line 的 points 数组可能超出 Manual Sync 单次序列化限制(约 200 字节/serialization for continuous;280,496 字节 for manual,详见 `memory/api/networking.md`)
- **可扩展**:
  - 颜色/粗细变化(添加 synced color/width 变量)
  - 撤销功能(添加栈结构)
  - 多人协作画布(扩展 Line 数量)

---

## 与相关知识库关联

- **Manual Sync 模式**:`memory/api/networking.md`
- **VRCPickup 行为**:`memory/api/pickups.md`
- **OnDeserialization 数组同步**:[index.md#cubearraysync](index.md)
- **Continuous Sync 模式**:参考 [index.md#pickupcube](index.md#41-pickupcube) 的 `SyncPickupColor` 模式
