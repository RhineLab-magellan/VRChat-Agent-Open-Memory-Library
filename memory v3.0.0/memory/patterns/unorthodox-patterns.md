---
title: "Unorthodox UdonSharp Patterns (邪修技法)"
category: patterns
knowledge_level: applied
status: active
source: "VRChat 社区 UdonSharp 实战案例库 (udonsharp-udon.md, vrcd.org.cn)"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High
tags:
  - patterns
  - patterns
  - event
  - udonsharp
aliases:
  - "Unorthodox UdonSharp Patterns (邪修技法)"
  - unorthodox-patterns
related:
  - hash-based-dispatch.md
  - inherited-subscriber.md
  - advanced-sync-patterns.md
  - build-time-vs-runtime-separation.md
  - code-generation-type-erasure.md
---
# Pattern: Unorthodox UdonSharp Patterns (邪修技法)


---

## Pattern 1: Toggle 数组替代 Button 实现参数化按钮

### Problem
Udon 中 Unity Button 只能通过 `SendCustomEvent` 发送**无参事件**。要为每个按钮传递参数（如按钮 ID），传统做法需要为每个按钮挂载独立 UdonBehaviour，导致 VM 数量爆炸。

### Solution
用 Toggle 组件数组替代 Button。所有 Toggle 共享一个 UdonBehaviour。触发时遍历 Toggle 数组，找到 `isOn=true` 的那个——**它在数组中的位置就是参数**。

### Key Insight
- 无需为每个按钮单独挂载 UdonBehaviour
- 参数自然编码为数组索引
- 额外参数可建立与 Toggle 数组索引对应的数据数组
- 可扩展通过解析 `Toggle.name` 嵌入更多参数

### Implementation Sketch
```csharp
public Toggle[] Toggles; // 通过 Inspector 绑定所有 Toggle

void Start() {
    for (int i = 0; i < Toggles.Length; i++)
        Toggles[i].SetIsOnWithoutNotify(false);
}

private int CheckToggleIndex() {
    for (int i = 0; i < Toggles.Length; i++) {
        if (Toggles[i].isOn) {
            Toggles[i].SetIsOnWithoutNotify(false); // 重置
            return i;
        }
    }
    return -1;
}

public void OnToggleUse() { // 所有 Toggle 的 OnValueChanged 绑定此方法
    int index = CheckToggleIndex();
    if (index < 0) return;
    // index 即为按钮参数
    ProcessButton(index);
}
```

### Performance
- 遍历数组：O(n)，n = 按钮数量
- 单 UdonBehaviour 替代 N 个 Behaviour，节省 N-1 个 Udon VM

### When To Use
- 批量相同功能的按钮（道具选择、场景切换、菜单项）
- 按钮数量可动态增长（只需扩展数组）

### When Not To Use
- 按钮数量极大（>100）且功能差异大（遍历成本上升 + 管理困难）
- 按钮需要不同的视觉效果/布局（Toggle 的视觉限制）
- 分区建议：按功能分组（"场景切换组"、"道具选择组"），每组共享一个 Toggle 数组

---


## Pattern 2: SendCustomEvent 发布-订阅模式

### Problem
Udon 中 Unity Button 只能通过 `SendCustomEvent` 发送**无参事件**。要为每个按钮传递参数（如按钮 ID），传统做法需要为每个按钮挂载独立 UdonBehaviour，导致 VM 数量爆炸。

### Solution
用 Toggle 组件数组替代 Button。所有 Toggle 共享一个 UdonBehaviour。触发时遍历 Toggle 数组，找到 `isOn=true` 的那个——**它在数组中的位置就是参数**。

### Implementation Sketch

**主脚本（发布者）：**
```csharp
private UdonBehaviour[] _targets = new UdonBehaviour[0];

public void RegisterOnMoneyChanged(GameObject target) {
    UdonBehaviour udonBehaviour = (UdonBehaviour)target.GetComponent(typeof(UdonBehaviour));
    if (udonBehaviour == null) { Debug.LogError("No UdonBehaviour"); return; }
    // 动态扩展数组
    UdonBehaviour[] newTargets = new UdonBehaviour[_targets.Length + 1];
    for (int i = 0; i < _targets.Length; i++) newTargets[i] = _targets[i];
    newTargets[_targets.Length] = udonBehaviour;
    _targets = newTargets;
}

public void ChangeMoneyAndUpdate(float value) {
    money += value;
    NotifyMoneyChanged();
}

private void NotifyMoneyChanged() {
    for (int i = 0; i < _targets.Length; i++)
        _targets[i].SendCustomEvent("UdonChipsMoneyChanged");
}
```

**子脚本（订阅者）：**
```csharp
private UdonChips udonChips;
void Start() {
    udonChips = (UdonChips)GameObject.Find("UdonChips").GetComponent(typeof(UdonChips));
    udonChips.RegisterOnMoneyChanged(this.gameObject);
}

public void UdonChipsMoneyChanged() {
    currentMoney = udonChips.money; // 读取最新值
}
```

### Performance
- 事件驱动：0 次 Update 轮询
- 仅在值变化时触发 SendCustomEvent 链
- 缺点：数组动态扩展涉及重新分配（注册时一次性成本）

### When To Use
- 多个脚本依赖同一个脚本的变量变化
- 变量变化频率远低于 `Update()` 帧率
- 场景中有明确的主-从关系

### When Not To Use
- 订阅者数量极大且频繁注册/注销（数组频繁重分配）
- 变量变化频率极高（每秒 > 10 次，SendCustomEvent 成本累积）
- 传统做法通过 `Update()` 每帧轮询其他脚本的变量来检测变化。高频轮询浪费 Udon VM 执行步骤

主脚本维护一个订阅者数组。子脚本在 `Start()` 中注册自身。主脚本仅在**变量实际变化时**遍历订阅者数组，发送 `SendCustomEvent` 推送更新。

---


## Pattern 3: 动态数组简易对象池

### Problem
频繁 `Instantiate()` + `Destroy()` Udon prefab 性能开销大。实测数据：
- Instantiate prefab: ~1ms
- Udon VM 创建: ~1ms
- 合计每个实例 ~2ms

### Solution
使用动态数组作为简易对象池。数组自动 grow/shrink：
- 需要更多对象 → `Instantiate` 追加到数组末尾
- 需要更少对象 → `Destroy` 数组末尾的冗余对象
- 对象数量不变 → 通过 `SetProgramVariable` + `SendCustomEvent("InitXxx")` 重新初始化已有对象

### Implementation Sketch
```csharp
private GameObject[] _pool = new GameObject[0];

private void EnsurePoolSize(int needed) {
    if (needed > _pool.Length) {
        // Grow
        GameObject[] newPool = new GameObject[needed];
        for (int i = 0; i < _pool.Length; i++) newPool[i] = _pool[i];
        for (int i = _pool.Length; i < needed; i++)
            newPool[i] = Instantiate(_prefab, _parent);
        _pool = newPool;
    } else if (needed < _pool.Length) {
        // Shrink — Destroy excess from end
        for (int i = needed; i < _pool.Length; i++)
            Destroy(_pool[i]);
        GameObject[] newPool = new GameObject[needed];
        for (int i = 0; i < needed; i++) newPool[i] = _pool[i];
        _pool = newPool;
    }
    // Reinitialize all active objects
    for (int i = 0; i < needed; i++) {
        UdonBehaviour comp = (UdonBehaviour)_pool[i].GetComponent(typeof(UdonBehaviour));
        comp.SetProgramVariable("Index", i);
        comp.SetProgramVariable("Data", _data[i]);
        comp.SendCustomEvent("InitElement");
    }
}
```

### Performance
- 避免重复的 Instantiate/Destroy 循环
- Grow 仅在首次达到新容量时发生
- Shrink 回收多余 VM，减少常驻 Udon VM 数量

### When To Use
- 对象数量波动但不会极端变化（如购物车、玩家列表）
- 需要频繁复用同一 Prefab
- 不需要完全持续不分配的对象池（VRCObjectPool 更合适）

### When Not To Use
- 对象需要物理/网络同步 → 考虑 VRCObjectPool
- 对象数量变化极频繁且幅度大 → 数组频繁重新分配
- 每个对象需要独立的复杂状态管理 → 专用对象池更合适

---


## Pattern 4: 将计算卸载到并行线程


### 核心思路
Udon VM 是单线程解释执行。但 Unity 引擎的其他子系统（音频、渲染、动画）在独立线程中运行。利用这些并行上下文可以将计算从 Udon 主线程卸载。

### 代价
所有这些技术都**提高了 Udon 运行时的整体代价**——只是将代价从主线程转移到了并行线程。并行线程的 CPU 时间仍然消耗在 VRChat 进程中，总 CPU 预算不变。适用场景仅限于**计算瓶颈在主线程而非总 CPU 的情况**。

---

### 4a. Animator BlendTree 卸载计算

> 状态: **❌ 未验证 — Idea** ⚠️

**思路**: 通过 `Animator.SetFloat()` 写入输入参数 → BlendTree 计算 → `Animator.GetFloat()` 读取结果。

**风险**: 
- 未有任何社区实测验证
- BlendTree 的数学能力有限（不是通用计算单元）
- 可能 BlendTree 计算仍然在 Unity 主线程执行而非独立线程
- 即使可行，一帧延迟 + 调试复杂度 → 成本可能高于收益

**Reference**: vrc.school/docs/Other/Advanced-BlendTrees

---

### 4b. OnAudioFilterRead 音频线程卸载

> 状态: **✅ 特性确认** — 与主线程并行 ⚠️ 但需小心数据竞争

**机制**: `OnAudioFilterRead` 是 Unity 音频系统的回调。它**在音频线程中执行，与 Udon 主线程并行**。这意味着：
- 可以将计算逻辑写入 `OnAudioFilterRead`，在音频线程中执行
- 释放 Udon 主线程

**并行事故风险**: 
- 音频线程和主线程可能**同时**访问 UdonBehaviour 的成员变量
- 无锁无同步机制 → 数据竞争 → 不可预期的结果
- 需要在设计上保证两个线程不操作同一数据

**UdonSharp 中的特殊问题**: 
`OnAudioFilterRead` 在 Unity Editor 的 U# 代理对象上行为可能与实际 UdonBehaviour 不同。参见 `rules/udonsharp-deep-pitfalls.md` RULE-DP-16 (Proxy Object)。

---

### 4c. GPU Callback 卸载

> 状态: **✅ 特性确认** — 社区有使用案例 ⚠️

**机制**: 利用 Unity 的 GPU 回调机制（如 `OnAsyncGpuReadbackComplete` 等），将计算委托给 GPU 完成。

**原理**: GPU 天然并行。适合大规模并行数据（向量运算、矩阵变换、粒子数据）。GPU 完成计算后通过 callback 返回结果。

**代价**:
- GPU → CPU 数据回传有延迟
- 适合批量数据，不适合单个小值
- 进一步增加整体运行时负担

---

### 总结

| 技术 | 验证状态 | 并行线程 | 主要风险 |
|---|---|---|---|
| Animator BlendTree | ❌ Idea | 未知（可能仍在主线程） | 完全未验证 |
| OnAudioFilterRead | ✅ 特性确认 | 音频线程 | 数据竞争 |
| GPU Callback | ✅ 社区使用 | GPU | 延迟 + 仅适合批量数据 |

### When To Use (适用场景)
- Udon 主线程是明确的计算瓶颈（Profiler 确认）
- 计算可接受异步结果（不需要立即同步）
- 并行上下文与主线程的数据可以完全隔离

### When Not To Use
- 简单运算（不需要卸载）
- 需要同步结果（网络同步、即时 UI 更新）
- 无法隔离并行线程与主线程的数据访问

---

**整体置信度: Low-Medium** — 以下技术中，OnAudioFilterRead 和 GPU Callback 由社区确认存在并行特性，但 **Animator BlendTree 卸载计算未经验证，仅为 Idea**。所有并行卸载技术都面临**数据竞争**风险——并行线程与 Udon 主线程同时操作同一数据会导致不可预期的行为。


## Pattern 5: Bit-Packing for PlayerData

### Problem
Udon 中 Unity Button 只能通过 `SendCustomEvent` 发送**无参事件**。要为每个按钮传递参数（如按钮 ID），传统做法需要为每个按钮挂载独立 UdonBehaviour，导致 VM 数量爆炸。

### Solution
使用整数类型作为 bit carrier：
- `ushort`: 16 bit → 可存 16 个 bool 或 4 个 0-15 范围的值
- `uint`: 32 bit
- `ulong`: 64 bit

### Bit Allocation Strategy
```
最大值 0-1   → 1 bit per value
最大值 0-3   → 2 bit per value
最大值 0-15  → 4 bit per value
最大值 0-255 → 8 bit per value
负数        → 第一位做符号位
```

### Implementation (conceptual)
```csharp
// Pack 4 values (max 15 each) into one ushort
ushort Pack(byte a, byte b, byte c, byte d) {
    return (ushort)(a | (b << 4) | (c << 8) | (d << 12));
}

// Save packed value
PlayerData.SetInt(player, "packedFlags", (int)packedValue);

// Restore
PlayerData.TryGetInt(player, "packedFlags", out int raw);
ushort packed = (ushort)raw;
byte a = (byte)(packed & 0xF);
byte b = (byte)((packed >> 4) & 0xF);
// ...
```

### When To Use
- PlayerData 存储多个小值
- 接近 100KB 配额上限
- bool flags、小范围整数状态

### When Not To Use
- 单个大值（不需要压缩）
- 调试频繁需要检查原始值时（packed 值不可读）

---

> PlayerData 每个 key 存储一个值。16 个 bool 需要 16 个 key → 浪费配额。

