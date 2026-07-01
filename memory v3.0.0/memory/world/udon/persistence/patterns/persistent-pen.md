---
title: 持久画笔实现(Pattern)
category: world
subcategory: udon/persistence/patterns
knowledge_level: applied
status: active
tags:
  - world
  - udon
  - persistence
  - patterns
  - pen
  - drawing
  - playerobject
  - line
aliases:
  - 持久画笔
  - Persistent Pen
  - 画线系统
  - 涂鸦
related:
  - ../../../../api/persistence.md
  - ../../index.md
  - ../player-object.md
  - ../serialization.md
  - ../limits-and-quirks.md
  - ../../../examples/persistence/persistent-pen.md
  - ../../../examples/persistence/health-bar.md
source: VRChat Creator Docs(https://creators.vrchat.com/worlds/examples/persistence/persistent-pen/)
source_type: official
version: 1.0
last_review: 2026-06-21
confidence: High
---
# 持久画笔实现(Pattern)

> 数据层:**PlayerObject**(大量数据 + 高频变化)
> 关键 API:`VRCPlayerObject` + `VRCEnablePersistence` + `[UdonSynced]`
> 官方示例:https://creators.vrchat.com/worlds/examples/persistence/persistent-pen/
> 适用 SDK:3.7+ / UdonSharp C#

---

## 概述

持久画笔是 **PlayerObject** 的经典应用:
- **大量数据**:20 条线,每条最多 100 个点
- **高频变化**:画线过程中每帧更新
- **跨设备同步**:PC 画的线在 Quest 上看到
- **可被擦除**:玩家可以删除自己画的线

**官方示例架构**:
- 1 个 `SimplePenSystem`(场景级,挂 VRCPlayerObject)
- 20 个 `Line` 子 GameObject(挂 UdonBehaviour)
- 1 个 `Pen` 子 GameObject(挂 UdonBehaviour,VRCPickup)

**关键设计**:用 **PlayerObject** 而非 PlayerData:
- 每次画新点 = 改 [UdonSynced] Vector3[]
- PlayerData 每次写 = 发 **全部** 20 条线
- PlayerObject = 单独同步,不影响其他 Prefab

---

## 完整实现(简化版)

### Prefab 结构

```
SimplePenSystem (场景中 1 个,VRC 自动 disable)
├── VRCPlayerObject          ← 让 VRChat 为每个玩家实例化
├── VRCEnablePersistence    ← 持久化 UdonSynced 字段
├── UdonBehaviour (PenSystem.cs)
│   ├── [UdonSynced] LineData[] _allLines
│   ├── [UdonSynced] int _activeLineCount
│   └── [UdonSynced] int _currentLineIndex
│
├── Pen (VRCPickup)
│   └── UdonBehaviour (PenTool.cs)
│       └── OnPickupUse() → 添加点到当前线
│
├── Line_0 (LineRenderer)
│   └── UdonBehaviour (LineRenderer.cs)
│       └── [UdonSynced] Vector3[] _points
│       └── [UdonSynced] Color _color
│
├── Line_1
├── ... (共 20 个 Line_X)
└── Eraser (VRCPickup)
    └── UdonBehaviour (EraserTool.cs)
        └── OnPickupUse() → 删除碰到的线
```

---

### 文件 1:LineData.cs(数据结构)

```csharp
using UnityEngine;

[System.Serializable]
public class LineData {
    public Vector3[] points;  // 最多 100 个点
    public Color color;
    public int pointCount;    // 实际点数(可能 < 100)
    public bool active;       // 是否正在使用
    
    public LineData() {
        points = new Vector3[100];
        color = Color.white;
        pointCount = 0;
        active = false;
    }
    
    public void CopyFrom(LineData other) {
        System.Array.Copy(other.points, points, other.pointCount);
        color = other.color;
        pointCount = other.pointCount;
        active = other.active;
    }
}
```

### 文件 2:PenSystem.cs(场景级,挂 SimplePenSystem Prefab)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class PenSystem : UdonSharpBehaviour {
    [Header("Line Configuration")]
    [SerializeField] private int maxLines = 20;
    [SerializeField] private int maxPointsPerLine = 100;
    
    [Header("References")]
    [SerializeField] private PenTool penTool;
    [SerializeField] private EraserTool eraserTool;
    [SerializeField] private LineRenderer[] lineRenderers;  // 20 个 Line 子物体
    
    [UdonSynced] private LineData[] _allLines = new LineData[20];
    [UdonSynced] private int _activeLineCount = 0;
    [UdonSynced] private int _currentLineIndex = -1;
    
    private bool _dataReady = false;
    
    public override void OnPlayerRestored(VRCPlayerApi player) {
        if (!Networking.IsOwner(gameObject)) return;
        _dataReady = true;
        RenderAllLines();
    }
    
    public override void OnDeserialization() {
        if (!_dataReady) return;
        RenderAllLines();
    }
    
    // 玩家开始画线(从 PenTool 调用)
    public void StartNewLine(Color color) {
        if (!Networking.IsOwner(gameObject)) return;
        if (!_dataReady) return;
        
        // 找一个空的 line slot
        int slot = FindEmptyLineSlot();
        if (slot < 0) {
            // 没有空 slot,循环覆盖最旧的
            slot = FindOldestLineSlot();
        }
        
        _currentLineIndex = slot;
        _allLines[slot] = new LineData();
        _allLines[slot].color = color;
        _allLines[slot].active = true;
        _allLines[slot].pointCount = 0;
        
        if (slot >= _activeLineCount) _activeLineCount = slot + 1;
        RequestSerialization();
    }
    
    // 玩家持续画线(每帧从 PenTool 调用)
    public void AddPointToCurrentLine(Vector3 point) {
        if (!Networking.IsOwner(gameObject)) return;
        if (!_dataReady) return;
        if (_currentLineIndex < 0) return;
        if (_currentLineIndex >= maxLines) return;
        
        LineData line = _allLines[_currentLineIndex];
        if (line == null) return;
        if (line.pointCount >= maxPointsPerLine) return;
        
        line.points[line.pointCount] = point;
        line.pointCount++;
        RequestSerialization();
    }
    
    // 玩家停止画线
    public void FinishCurrentLine() {
        if (!Networking.IsOwner(gameObject)) return;
        _currentLineIndex = -1;
    }
    
    // 玩家擦除一条线
    public void EraseLine(int slot) {
        if (!Networking.IsOwner(gameObject)) return;
        if (slot < 0 || slot >= maxLines) return;
        
        _allLines[slot].active = false;
        _allLines[slot].pointCount = 0;
        RequestSerialization();
        RenderLine(slot);
    }
    
    private int FindEmptyLineSlot() {
        for (int i = 0; i < _activeLineCount; i++) {
            if (_allLines[i] == null || !_allLines[i].active) return i;
        }
        return -1;
    }
    
    private int FindOldestLineSlot() {
        // 简化:返回第一个 slot(可改为基于时间戳)
        for (int i = 0; i < _activeLineCount; i++) {
            if (_allLines[i] == null || !_allLines[i].active) return i;
        }
        return 0;
    }
    
    private void RenderAllLines() {
        for (int i = 0; i < maxLines; i++) {
            RenderLine(i);
        }
    }
    
    private void RenderLine(int slot) {
        if (slot < 0 || slot >= lineRenderers.Length) return;
        
        LineData line = _allLines[slot];
        LineRenderer renderer = lineRenderers[slot];
        if (line == null || !line.active || line.pointCount == 0) {
            renderer.positionCount = 0;
            return;
        }
        
        renderer.positionCount = line.pointCount;
        renderer.startColor = line.color;
        renderer.endColor = line.color;
        for (int i = 0; i < line.pointCount; i++) {
            renderer.SetPosition(i, line.points[i]);
        }
    }
}
```

### 文件 3:PenTool.cs(挂在 Pen 子物体)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class PenTool : UdonSharpBehaviour {
    [Header("Configuration")]
    [SerializeField] private PenSystem penSystem;
    [SerializeField] private Color[] availableColors = {
        Color.red, Color.green, Color.blue, Color.yellow,
        Color.cyan, Color.magenta, Color.white, Color.black
    };
    [SerializeField] private float minDistanceBetweenPoints = 0.05f;
    
    private int _currentColorIndex = 0;
    private bool _isDrawing = false;
    private Vector3 _lastPoint;
    
    public override void OnPickupUseDown() {
        if (penSystem == null) return;
        Color color = availableColors[_currentColorIndex];
        penSystem.StartNewLine(color);
        _isDrawing = true;
    }
    
    public override void OnPickupUseUp() {
        if (penSystem == null) return;
        penSystem.FinishCurrentLine();
        _isDrawing = false;
    }
    
    // 切换颜色:轻点 Use(无移动)
    private float _useDownTime = 0f;
    private Vector3 _useDownPosition;
    
    public override void OnPickupUseDown() {
        _useDownTime = Time.time;
        _useDownPosition = transform.position;
        // 同时:开始新线
        penSystem.StartNewLine(availableColors[_currentColorIndex]);
        _isDrawing = true;
    }
    
    public override void OnPickup() {
        _useDownTime = Time.time;
        _useDownPosition = transform.position;
    }
    
    public override void OnPickupUseUp() {
        // 判断是 tap 还是 hold
        float duration = Time.time - _useDownTime;
        float distance = Vector3.Distance(transform.position, _useDownPosition);
        
        if (duration < 0.3f && distance < 0.1f) {
            // Tap: 切换颜色
            _currentColorIndex = (_currentColorIndex + 1) % availableColors.Length;
        }
        
        // 结束画线
        penSystem.FinishCurrentLine();
        _isDrawing = false;
    }
    
    void Update() {
        if (!_isDrawing) return;
        if (penSystem == null) return;
        
        Vector3 currentPoint = transform.position;
        float distance = Vector3.Distance(currentPoint, _lastPoint);
        if (distance < minDistanceBetweenPoints) return;
        
        penSystem.AddPointToCurrentLine(currentPoint);
        _lastPoint = currentPoint;
    }
}
```

### 文件 4:EraserTool.cs(挂在 Eraser 子物体)

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class EraserTool : UdonSharpBehaviour {
    [SerializeField] private PenSystem penSystem;
    [SerializeField] private float eraserRadius = 0.3f;
    
    public override void OnPickupUseDown() {
        if (penSystem == null) return;
        // 检测最近的可擦除线
        int slot = FindClosestLine();
        if (slot >= 0) {
            penSystem.EraseLine(slot);
        }
    }
    
    private int FindClosestLine() {
        Vector3 eraserPos = transform.position;
        float closestDistance = float.MaxValue;
        int closestSlot = -1;
        
        // 通过 public getter 访问 _allLines(简化:实际可加 getter)
        LineData[] lines = penSystem.GetAllLines();
        for (int i = 0; i < lines.Length; i++) {
            if (lines[i] == null || !lines[i].active || lines[i].pointCount == 0) continue;
            // 简化:检查第一个点(实际应检查最近点)
            float dist = Vector3.Distance(eraserPos, lines[i].points[0]);
            if (dist < eraserRadius && dist < closestDistance) {
                closestDistance = dist;
                closestSlot = i;
            }
        }
        return closestSlot;
    }
}
```

---

## 关键设计点

### 1. 为什么用 PlayerObject 而非 PlayerData

| 维度 | PlayerObject | PlayerData |
|------|-------------|-----------|
| 数据大小 | 20 lines × 100 points × 12B = 24KB | 同 24KB |
| 每次同步开销 | **仅 PenSystem** | **全部 PlayerData**(其他 Prefab 也跟着发) |
| 高频写(10Hz) | PenSystem 24KB × 10 = 240KB/s | 全 World × 10 = 1MB+(超 11KB 上限) |
| 网络影响 | 独立带宽 | 全局拥塞 |
| Late Joiner | 自动 | 自动 |

> **结论**:画笔这种"大量数据 + 高频写"场景,**必须**用 PlayerObject。

### 2. 配额计算

```
20 lines × 100 points × 12 bytes (Vector3) = 24,000 bytes ≈ 24KB
+ 20 colors × 4 bytes (Color32) = 80 bytes
+ 20 pointCount × 4 bytes (int) = 80 bytes
+ 20 active × 1 byte (bool) = 20 bytes
─────────────────────────────────────────
总计: ~24.2 KB(压缩前)

VRChat 压缩后:大部分数据是零,压缩率 ~10-20%
压缩后: ~5 KB(远低于 100KB 配额)
```

> 还有大量余量可以扩展(更多线、更多点、颜色 RGBA 等)

### 3. 所有权模型

> 🔑 **PenSystem 玩家永远拥有自己的 PenSystem**(不能被偷)

**含义**:
- 玩家 A 画的线,**只有玩家 A 可以擦除**
- 玩家 B 拿自己的 Eraser 碰玩家 A 的线 → 不能擦(所有权)
- 这是 **特性** - 防止恶意擦除别人的创作

> **实际实现**:EraserTool 调用 `penSystem.EraseLine()` 时,PenSystem 内部 `if (!Networking.IsOwner(gameObject)) return;` 守卫

### 4. Late Joiner 处理

> **自动** - PlayerObject 走 [UdonSynced] 字段,VRChat 自动同步给新玩家

**新玩家加入**:
1. VRChat 为该玩家创建 PenSystem PlayerObject 实例
2. 从服务器拉取该玩家 **之前** 的 [UdonSynced] 字段值
3. 触发 `OnPlayerRestored` → `RenderAllLines()` → 重建 20 条 LineRenderer
4. 新玩家看到 **该玩家** 之前的所有画线

> **关键**:新玩家**只能**看到 **自己** 的画线(因为 PenSystem 是 per-player)

### 5. Manual Sync + RequestSerialization

```csharp
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]

public void AddPointToCurrentLine(Vector3 point) {
    // 修改 [UdonSynced] 字段
    line.points[line.pointCount] = point;
    line.pointCount++;
    RequestSerialization();  // 手动触发同步
}
```

**为什么用 Manual**:
- 画线时每帧都可能增加点(高频)
- Continuous 太频繁(200B 上限,容易超)
- Manual + RequestSerialization 让你控制节奏

### 6. 网络优化:批量同步

```csharp
// ❌ 错误:每点同步
public void AddPointToCurrentLine(Vector3 point) {
    line.points[line.pointCount] = point;
    line.pointCount++;
    RequestSerialization();  // 每点 1 次网络
}

// ✅ 优化:每 N 点同步
private int _pointsSinceLastSync = 0;
private const int SYNC_EVERY_N_POINTS = 5;

public void AddPointToCurrentLine(Vector3 point) {
    line.points[line.pointCount] = point;
    line.pointCount++;
    _pointsSinceLastSync++;
    if (_pointsSinceLastSync >= SYNC_EVERY_N_POINTS) {
        RequestSerialization();
        _pointsSinceLastSync = 0;
    }
}
```

---

## 性能优化

### 1. 降低同步频率

```csharp
// 5 Hz 同步(每 200ms 一次)
private float _lastSyncTime = 0;

public void AddPointToCurrentLine(Vector3 point) {
    line.points[line.pointCount] = point;
    line.pointCount++;
    
    if (Time.time - _lastSyncTime > 0.2f) {
        RequestSerialization();
        _lastSyncTime = Time.time;
    }
}
```

### 2. 简化线段(去除过近点)

```csharp
private const float MIN_POINT_DISTANCE = 0.05f;

public void AddPointToCurrentLine(Vector3 point) {
    if (line.pointCount > 0) {
        float distance = Vector3.Distance(point, line.points[line.pointCount - 1]);
        if (distance < MIN_POINT_DISTANCE) return;  // 跳过过近点
    }
    line.points[line.pointCount] = point;
    line.pointCount++;
}
```

### 3. 100KB 配额管理

```csharp
// 检测配额(SDK 3.10+)
public void CheckQuota() {
    int used = Networking.LocalPlayer.GetPlayerObjectStorageUsage();
    int limit = Networking.LocalPlayer.GetPlayerObjectStorageLimit();
    if ((float)used / limit > 0.9f) {
        Debug.LogWarning("PenSystem 接近 100KB 配额,删除旧线");
        // 自动删除最旧的线
        EraseLine(0);
    }
}
```

---

## 跨设备同步(核心特性)

> 玩家在 PC 上画线 → Quest 上看到自己的线(自己重新进入)

**数据流**:
1. PC 上 AddPoint → 修改 [UdonSynced] Vector3[] + RequestSerialization
2. VRChat 服务器保存完整 _allLines
3. 玩家 Quest 重新加入 → 服务器发该玩家数据
4. Quest 上的 PenSystem.OnPlayerRestored 触发
5. RenderAllLines() 重建 LineRenderer
6. Quest 看到完全相同的线

> **不是 "同步给其他玩家"** - 画笔数据是 **per-player** 的(每个人有自己的 PenSystem)

---

## 与协作画板的区别

| 维度 | 持久画笔(本例) | 协作画板 |
|------|---------------|---------|
| 所有权 | per-player PlayerObject | 场景级 [UdonSynced] |
| 可见性 | 只有自己看到 | 所有人看到 |
| 擦除权 | 只有自己可擦 | 通常有 Moderator 角色 |
| Late Joiner | 自己看到自己之前的线 | 看到当前画板状态 |

> **协作画板**:用场景级 [UdonSynced] 字段(不走 PlayerObject 持久化)
> **持久画笔**:用 PlayerObject(本 Pattern)

---

## 完整文件清单

```
Assets/
└── PersistentPen/
    ├── LineData.cs                 ← 数据结构
    ├── PenSystem.cs                ← 场景级核心(挂 SimplePenSystem)
    ├── PenTool.cs                  ← 挂在 Pen 子物体
    ├── EraserTool.cs               ← 挂在 Eraser 子物体
    ├── SimplePenSystem.prefab      ← PlayerObject 模板
    │   ├── VRCPlayerObject
    │   ├── VRCEnablePersistence
    │   ├── UdonBehaviour (PenSystem.cs)
    │   ├── Pen (VRCPickup + PenTool.cs)
    │   ├── Eraser (VRCPickup + EraserTool.cs)
    │   ├── Line_0 (LineRenderer)
    │   ├── Line_1
    │   ├── ... (20 个)
    │   └── Line_19
    └── PenMaterials/
        ├── Red.mat
        ├── Green.mat
        └── ...
```

---

## 测试清单

- [ ] ClientSim 模拟画线
- [ ] Build & Test 画线 + 退出 + 重新进入(线保留)
- [ ] PC 画线 → Quest 重新进入(跨设备)
- [ ] 擦除功能正常
- [ ] 切换颜色正常
- [ ] 20 条线满后循环覆盖最旧
- [ ] 100KB 配额警告测试

---

## 拓展应用

### 3D 笔刷(Brush)
- 用 particle system 模拟笔刷
- 每点同步粒子位置

### 多人协作白板
- 用 [UdonSynced] 字段(非 PlayerObject)
- 加 Moderator 权限管理

### 笔触重放
- 加时间戳 + 笔刷事件流
- 玩家可以"重放"自己的画线过程

---

## 相关知识库

- `memory/api/persistence.md` - API 速查
- `memory/world/udon/persistence/player-object.md` - PlayerObject 详细 API
- `memory/world/udon/persistence/limits-and-quirks.md` - 100KB 限制
- `memory/world/examples/persistence/persistent-pen.md` - 官方 Example Central 笔记
- `memory/world/udon/networking/ownership.md` - 所有权机制
- `memory/world/udon/networking/variables.md` - UdonSynced 字段类型
- `memory/patterns/manual-sync-state.md` - Manual Sync 模式
