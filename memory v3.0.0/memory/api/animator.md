---
title: "API: Animator"
category: api
knowledge_level: core
status: active
source: "社区经验 + 项目实测"
source_type: community
version: 1.0
last_review: 2026-06-04
confidence: High
tags:
  - api
  - animator
  - udonsharp
aliases:
  - 动画器
  - Animator
related:
  - not-exposed.md
  - official-doc-clarifications.md
  - player-api.md
  - udonsharp-runtime.md
  - ui.md
---
# API: Animator

---

## Animator 在 Udon 中的暴露

### Animator.SetInteger(string name, int value)
- **暴露**: ✅
- **热路径**: ✅ (轻量参数设置)
- **说明**: 设置 Animator int 参数。推荐用 int 驱动状态而不是 Trigger。

### Animator.SetFloat(string name, float value)
- **暴露**: ✅
- **热路径**: ✅
- **说明**: 设置 Animator float 参数。

### Animator.SetBool(string name, bool value)
- **暴露**: ✅
- **热路径**: ✅
- **说明**: 设置 Animator bool 参数。

### Animator.SetTrigger(string name)
- **暴露**: ⚠️ 需要验证
- **说明**: 不确定在 Udon VM 中是否稳定。推荐用 SetInteger 替代。

### Animator.GetInteger / GetFloat / GetBool
- **暴露**: ⚠️ 需要验证
- **说明**: 读取 Animator 参数值。

### Animator.Play(string stateName)
- **暴露**: ⚠️ 需要验证
- **说明**: 直接播放指定动画。可能不受 Animator Controller 过渡条件约束。

### Animator.speed
- **暴露**: ✅
- **说明**: 动画播放速度倍率。

## 推荐用法

### 用 int 状态参数替代 Trigger
```csharp
// ✅ 推荐: int 参数驱动
_animator.SetInteger("DoorState", 1);  // 1 = Open

// ⚠️ 可能不稳定: Trigger
_animator.SetTrigger("OpenDoor");
```

### 网络同步模式
- Animator 参数由本地 UdonBehaviour 设置
- 状态变化通过 `[UdonSynced]` 变量同步
- 远端在 `FieldChangeCallback` 中设置 Animator 参数
- 不直接在 Network Event 中操作 Animator

## 常见错误
- 频繁设置 Animator 参数（每帧 SetFloat 等）
- 依赖 Trigger 的瞬时性做同步（Trigger 状态不可查询）
- 多个 Behaviour 同时设置同一个 Animator 参数

## 高级技巧（未验证）: BlendTree 卸载计算

> ⚠️ **未验证 Idea** — Animator BlendTree 是否运行在独立线程仍不确定。可能仍在 Unity 主线程执行，因此不能保证真正"卸载"Udon VM。使用风险自负。

### 思路
1. `Animator.SetFloat()` 写入输入参数
2. BlendTree 进行计算
3. 下一帧 `Animator.GetFloat()` 读取结果

### 限制
- 完全未实测验证
- BlendTree 数学能力有限（非通用计算单元）
- 一帧延迟

### 替代的并行卸载技术
- `OnAudioFilterRead`: 音频线程中执行，**确认并行，但有数据竞争风险**
- GPU Callback: 将计算委托给 GPU，**确认可用，延迟高，仅适合批量数据**

### Reference
- vrc.school/docs/Other/Advanced-BlendTrees
- `patterns/unorthodox-patterns.md` Pattern 4（含三种并行卸载技术对比）
