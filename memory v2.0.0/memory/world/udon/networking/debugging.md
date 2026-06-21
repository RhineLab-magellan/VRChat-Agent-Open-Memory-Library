---
title: Debugging Network Issues 网络调试
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - networking
  - udon
  - sync
  - serialization
  - ownership

aliases:
  - "Debugging Network Issues 网络调试"

related:
  - world/udon/networking/index.md
  - world/udon/networking/ownership.md
  - world/udon/networking/late-joiners.md
  - world/udon/networking/performance.md
  - sources/clientsim.md
  - world/udon/world-debug-views.md
  - world/udon/using-build-test.md
  - api/networking.md

source: VRChat 官方 Creator Docs (Debugging Network Issues)
source_type: official
version: 1.0
last_review: 2026-06-15
confidence: High
---
# Debugging Network Issues 网络调试

> SDK Version: 3.x
---

## 简介

VRChat 提供多个调试工具,帮助开发者诊断 **所有权、同步状态、网络质量** 问题。本文档汇总三大问题场景的诊断方法 + 调试工具组合。

---

## 三大常见网络问题

### 问题 1:对象不同步(Object Sync Not Working)

#### 症状

- 玩家 A 修改对象,玩家 B 看不到变化
- 物理对象位置不一致
- Late Joiner 看到默认状态

#### 可能原因

| 原因 | 说明 |
|------|------|
| 同步模式错误 | 用了 `NoVariableSync` |
| Ownership 错误 | 修改者不是 Owner |
| 缺少 `RequestSerialization` | Manual 模式忘记调用 |
| 缺少 `VRCObjectSync` | 物理对象未挂载 |
| 数组未初始化 | synced 数组为 null |

#### 诊断步骤

```csharp
// 步骤 1:检查所有权
Debug.Log("Owner: " + Networking.GetOwner(gameObject).displayName);

// 步骤 2:检查同步模式(在 Inspector 中查看)
// 或运行时:
Debug.Log("SyncMode: " + ((UdonBehaviour)this).SyncMethod);

// 步骤 3:测试 OnDeserialization 是否触发
public override void OnDeserialization() {
    Debug.Log("Synced data received: " + syncedVariable);
}

// 步骤 4:检查 OnPostSerialization
public override void OnPostSerialization(SerializationResult result) {
    Debug.Log($"Serialize success: {result.success}, bytes: {result.byteCount}");
}
```

#### 修复

| 修复 | 操作 |
|------|------|
| 启用同步 | Inspector 勾选 "synced" 或加 `[UdonSynced]` |
| 改 Sync Mode | Inspector 选择 Manual/Continuous |
| 转移所有权 | `Networking.SetOwner(player, gameObject)` |
| 调用序列化 | `RequestSerialization()` |
| 添加 VRCObjectSync | 物理对象必备 |
| 初始化数组 | `new int[10]` 而非 null |

---

### 问题 2:Late Joiner 状态错误

#### 症状

- 新玩家加入,看到错误的门/灯/分数
- 玩家列表与实际不符
- 物理对象位置错误

#### 可能原因

| 原因 | 说明 |
|------|------|
| 用 Event 同步状态 | Late Joiner 收不到 Event |
| 变量未标记 `[UdonSynced]` | 不同步 |
| 数组未初始化 | 静默失败 |
| `Start()` 覆盖 synced 值 | 重新初始化抹掉了同步数据 |
| 跨平台字段不匹配 | PC/Quest 字段数量不同 |

#### 诊断步骤

```csharp
// 步骤 1:检查 OnDeserialization 是否触发
public override void OnDeserialization() {
    Debug.Log("OnDeserialization: state = " + _state);
}

// 步骤 2:检查变量是否有值
[UdonSynced] private int _state = -1;  // 默认 -1 用于检测
public override void OnDeserialization() {
    if (_state == -1) {
        Debug.LogWarning("Synced variable not received!");
    }
}

// 步骤 3:检查 IsNetworkSettled
public override void Update() {
    if (Networking.IsNetworkSettled) {
        Debug.Log("Network settled, all data received");
    }
}
```

#### 修复

| 修复 | 操作 |
|------|------|
| 改用 `[UdonSynced]` 变量 | 不要用 Event 同步状态 |
| 在 `OnDeserialization` 中应用状态 | Late Joiner 触发 |
| 移除 `Start()` 中的初始化 | 避免覆盖 synced 值 |
| 初始化数组 | `new int[10]` |
| 统一 PC/Quest 字段 | 跨平台字段一致 |

---

### 问题 3:所有权冲突(Ownership Conflicts)

#### 症状

- 多个玩家试图成为 Owner
- 所有权意外转移
- 修改无效

#### 可能原因

| 原因 | 说明 |
|------|------|
| 无限制的 Ownership Request | 任何玩家都能抢 |
| 多个脚本同时转移 | 竞争条件 |
| `OnOwnershipRequest` 逻辑不一致 | 双方执行导致 desync |
| 玩家频繁交互 | 频繁 SetOwner |

#### 诊断步骤

```csharp
// 步骤 1:检查当前 Owner
if (Networking.IsOwner(Networking.LocalPlayer, gameObject)) {
    Debug.Log("I am the owner");
} else {
    Debug.Log("Current owner: " + Networking.GetOwner(gameObject).displayName);
}

// 步骤 2:监听所有权变化
public override void OnOwnershipTransferred(VRCPlayerApi newOwner) {
    Debug.Log($"New owner: {newOwner.displayName}");
}

// 步骤 3:检查 Request 处理逻辑
public override bool OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner) {
    Debug.Log($"Request from: {requester.displayName}, requested new: {newOwner.displayName}");
    return true;  // 或 false
}
```

#### 修复

| 修复 | 操作 |
|------|------|
| 实现业务规则 | `OnOwnershipRequest` 中验证 |
| 最小化所有权转移 | 减少 `SetOwner` 调用 |
| 使用 Owner 模式 | 用 Network Event 通知 Owner |
| 双方逻辑一致 | `OnOwnershipRequest` 同步执行 |

---

## 调试工具组合

### 工具 1:World Debug Views(VRChat 客户端内置)

> 在 VRChat 客户端中按 **Debug Menu 6** 打开。

| 显示内容 | 用途 |
|---------|------|
| 每个对象的所有者 | 验证所有权 |
| 每个对象的网络状态 | 是否同步中 |
| 同步数据大小 | 字节数监控 |
| 同步频率 | 频率监控 |

> 详见 `memory/world/udon/world-debug-views.md`。

### 工具 2:Debug.Log 关键节点

```csharp
// 推荐的日志点
public override void OnPreSerialization() {
    Debug.Log($"[Serialize] _state = {_state}");
}

public override void OnDeserialization() {
    Debug.Log($"[Deserialize] _state = {_state}");
}

public override void OnPostSerialization(SerializationResult result) {
    if (!result.success) {
        Debug.LogError($"[Serialize FAIL] bytes: {result.byteCount}");
    }
}

public override void OnOwnershipTransferred(VRCPlayerApi newOwner) {
    Debug.Log($"[Ownership] New: {newOwner.displayName}");
}
```

### 工具 3:IsClogged + IsNetworkSettled 监控

```csharp
void Update() {
    // 网络状态指示器
    if (Networking.IsClogged) {
        Debug.LogWarning("[Network] Clogged!");
    }
    if (Networking.IsNetworkSettled) {
        // 数据已就绪
    }
}
```

### 工具 4:Network Stats API

> 通过 `VRC.SDK3.Network.Stats` 访问详细网络指标。

```csharp
using VRC.SDK3.Network;

// 全局统计
float throughput = Stats.ThroughputPercentage;
float bytesOut = Stats.BytesOutAverage;
float bytesIn = Stats.BytesInAverage;
bool isClogged = Stats.Suffering > 0.5f;  // 队列积压

// 单对象统计
float updateInterval = VRC.SDK3.Network.Stats.GetUpdateInterval(gameObject);
int totalBytes = VRC.SDK3.Network.Stats.GetTotalBytes(gameObject);
bool sleeping = VRC.SDK3.Network.Stats.IsSleeping(gameObject);
```

> 详细 API 见 `tools/network-stats.md`(task-15)。

### 工具 5:ClientSim(Editor 内模拟)

> 在 Editor 中模拟多个客户端,无需启动 VRChat。

| 窗口 | 用途 |
|------|------|
| **Settings** | 配置 Player Count、Latency、Jitter |
| **PlayerObject** | 测试 PlayerObject 行为 |
| **PlayerData** | 测试 PlayerData 持久化 |
| **Main** | 模拟多个玩家交互 |

> 详细文档见 `memory/world/clientsim/` 和 `memory/sources/clientsim.md`。

---

## 调试工作流

### 阶段 1:本地测试(Editor + ClientSim)

```
1. 编写 Udon 脚本
2. 用 ClientSim 模拟 2-3 个玩家
3. 验证基本功能
4. 检查 OnDeserialization 触发
5. 模拟 Late Joiner(关闭再打开连接)
```

### 阶段 2:Build & Test(本地 VRChat)

```
1. Build & Test 启动
2. 启动两个 VRChat 客户端
3. 测试同步、所有权、Late Joiner
4. 查看 Debug Menu 6 数据
5. 收集 Debug.Log
```

### 阶段 3:Private Test World

```
1. 上传 Private World
2. 邀请 2-3 名测试者
3. 多平台测试(PC + Quest)
4. 长时间运行(> 30 分钟)
5. 监控带宽(Stats API)
```

### 阶段 4:Public 发布

```
1. 灰度发布(小范围)
2. 监控反馈
3. 修复 Bug
4. 完整发布
```

---

## 性能调试模式

### 模式 1:实时带宽监控

```csharp
public class BandwidthMonitor : UdonSharpBehaviour {
    [SerializeField] private TextMeshProUGUI bandwidthText;
    
    void Update() {
        bandwidthText.text = $"Out: {VRC.SDK3.Network.Stats.BytesOutAverage / 1024:F2} KB/s";
        bandwidthText.text += $"\nClogged: {Networking.IsClogged}";
    }
}
```

### 模式 2:每对象字节数

```csharp
public class ObjectByteCounter : UdonSharpBehaviour {
    void Update() {
        int totalBytes = 0;
        foreach (var obj in syncedObjects) {
            totalBytes += VRC.SDK3.Network.Stats.GetTotalBytes(obj);
        }
        Debug.Log($"Total synced bytes: {totalBytes}");
    }
}
```

### 模式 3:拥塞时降级

```csharp
public class AdaptiveSync : UdonSharpBehaviour {
    void Update() {
        if (Networking.IsClogged) {
            // 降级:关闭粒子、降低频率
            particleSystem.Stop();
            CancelInvoke(nameof(PeriodicSync));
        } else {
            // 恢复
            if (!particleSystem.isPlaying) particleSystem.Play();
            if (!IsInvoking(nameof(PeriodicSync))) {
                InvokeRepeating(nameof(PeriodicSync), 0, 0.5f);
            }
        }
    }
    
    void PeriodicSync() {
        if (Networking.IsOwner(gameObject)) {
            RequestSerialization();
        }
    }
}
```

---

## 常见调试陷阱

### 陷阱 1:Debug.Log 本身消耗带宽

```csharp
// ❌ 大量日志可能影响性能
void Update() {
    Debug.Log("Frame: " + Time.frameCount);
}

// ✅ 条件日志
void Update() {
    if (Time.frameCount % 60 == 0) {  // 每 60 帧
        Debug.Log("Frame: " + Time.frameCount);
    }
}
```

### 陷阱 2:本地看不到同步效果

> **关键**:`[UdonSynced]` 变量在本地 **直接修改立即可见**(不需要网络)。但远端玩家需要时间接收。

```csharp
// 本地:立即看到 _state = true
// 远端:50-200ms 后看到 _state = true
```

### 陷阱 3:ClientSim 不模拟所有场景

> ClientSim 是 **网络行为模拟**,但 **不模拟**:
- 真实 VR 硬件
- 平台差异(Quest vs PC)
- 真实带宽限制
- Master 转移的所有场景

> **生产环境测试不可省略**。

---

## Debug 命令行参数

```bash
# 启用调试 GUI
VRChat.exe --enable-debug-gui

# 启用详细日志
VRChat.exe --enable-verbose-logging

# 指定日志文件
VRChat.exe --log-file "C:\path\to\logs.txt"
```

| 参数 | 用途 |
|------|------|
| `--enable-debug-gui` | 启用 World Debug Views |
| `--enable-verbose-logging` | 详细日志输出 |
| `--log-file <path>` | 输出日志到文件 |

---

## 完整调试代码模板

```csharp
using UdonSharp;
using VRC.SDKBase;
using VRC.SDK3.Network;
using VRC.Udon.Common;

[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class NetworkDebugger : UdonSharpBehaviour {
    [UdonSynced] private int _value = 0;
    [SerializeField] private bool _enableLogging = true;
    
    public void SetValue(int newValue) {
        if (!Networking.IsOwner(gameObject)) {
            if (_enableLogging) Debug.LogWarning("[NetDebug] Not owner, request transfer");
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
            return;
        }
        _value = newValue;
        if (_enableLogging) Debug.Log($"[NetDebug] SetValue: {_value}");
        RequestSerialization();
    }
    
    public override void OnPreSerialization() {
        if (_enableLogging) Debug.Log("[NetDebug] OnPreSerialization");
    }
    
    public override void OnDeserialization() {
        if (_enableLogging) Debug.Log($"[NetDebug] OnDeserialization: _value = {_value}");
    }
    
    public override void OnPostSerialization(SerializationResult result) {
        if (_enableLogging) {
            if (result.success) {
                Debug.Log($"[NetDebug] Serialized {result.byteCount} bytes");
            } else {
                Debug.LogError("[NetDebug] Serialization FAILED");
            }
        }
    }
    
    public override void OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner) {
        if (_enableLogging) {
            Debug.Log($"[NetDebug] Ownership request from {requester.displayName}");
        }
        return true;
    }
    
    public override void OnOwnershipTransferred(VRCPlayerApi newOwner) {
        if (_enableLogging) {
            Debug.Log($"[NetDebug] New owner: {newOwner.displayName}");
        }
    }
}
```

---

## 风险与陷阱

| 风险 | 严重度 | 说明 |
|------|-------|------|
| Debug.Log 过多 | 🟠 High | 影响性能,生产环境关闭 |
| 依赖 ClientSim 替代真机 | 🟠 High | 平台差异、VR 硬件无法模拟 |
| Master 判断权限 | 🔴 Critical | Master 不可靠 |
| 调试 UI 未在生产禁用 | 🟡 Medium | 暴露内部状态 |
| 未清理测试同步变量 | 🟠 High | 占用带宽 |

---

## 相关知识库

| 文档 | 关系 |
|------|------|
| `memory/world/udon/networking/index.md` | Networking 概述 |
| `memory/world/udon/networking/ownership.md` | 所有权调试 |
| `memory/world/udon/networking/late-joiners.md` | Late Joiner 调试 |
| `memory/world/udon/networking/performance.md` | 性能调试 |
| `memory/sources/clientsim.md` | ClientSim 使用 |
| `memory/world/udon/world-debug-views.md` | World Debug Views |
| `memory/world/udon/using-build-test.md` | Build & Test 模式 |
| `memory/api/networking.md` | API 速查 |
