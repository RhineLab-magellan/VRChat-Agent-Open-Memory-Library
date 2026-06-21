---
title: Severity Model
category: reviews

knowledge_level: applied
status: active

tags:
  - reviews
  - guide
  - sync
  - serialization
  - ownership
  - event

aliases:
  - "Severity Model"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-04
confidence: High
---
# Severity Model


---

## 风险分级

Agent 在审查 UdonSharp 脚本时，按以下标准分级：

## 严重 (Critical)

**会导致以下任一后果：**

- ❌ UdonSharp 编译失败
- ❌ VRChat 运行时崩溃或脚本禁用
- ❌ 网络状态错误（所有玩家看到不一致的状态）
- ❌ Late joiner 数据永久缺失
- ❌ 使用了 VRChat 禁止的 API
- ❌ Ownership 冲突导致状态反复翻转
- ❌ 非 owner 写入 synced variable 无保护

**示例：**
- 使用 `List<T>` 导致编译错误
- 只靠 Network Event 传递 late joiner 需要的状态
- Manual Sync 修改后忘记 `RequestSerialization()`
- 没有 owner 检查就修改 synced variable

---

## 中等 (Moderate)

**会导致以下任一后果：**

- ⚠️ 明显的性能下降（帧率降低、延迟增加）
- ⚠️ 不必要的网络带宽消耗
- ⚠️ 潜在的竞态条件（在特定条件下才会触发）
- ⚠️ 多人频繁操作时的不稳定行为
- ⚠️ 数组越界或空引用未防护
- ⚠️ Continuous Sync 用于离散状态

**示例：**
- Update 中 GetComponent
- 高频 Debug.Log
- 多个 bool 应合并为 bit flags 但未合并
- 缺少 debounce 的重度交互按钮

---

## 轻微 (Minor)

**代码质量或可维护性问题：**

- ℹ️ 代码风格不一致
- ℹ️ 魔法数字未用 const 定义
- ℹ️ 变量命名不清晰
- ℹ️ 注释与代码不符
- ℹ️ 可合并的重复代码
- ℹ️ 不必要的 SerializeField（仅用 Start 赋值的字段）
- ℹ️ 过度拆分简单逻辑到多个方法

**示例：**
- `if (state == 3)` 而不是 `if (state == STATE_ENDED)`
- 重复的状态转换代码没有抽取成方法
- 变量名 `x`, `a1`, `t` 等无意义缩写

---

## 审查输出格式

对每个问题必须输出：

```
[{严重级}] [{类别}] {简述}
  位置: {行号或方法名}
  原因: {为什么这是一个问题}
  影响: {对运行/网络/性能的影响}
  修复: {建议的修改方式}
```

## 总体评分

按以下格式总结：

```text
严重: N 个  → {结论: 是否可编译/可运行/网络正确/late joiner 正确}
中等: N 个  → {结论: 性能/带宽/稳定性是否有明显问题}
轻微: N 个  → {结论: 代码质量评估}
```
