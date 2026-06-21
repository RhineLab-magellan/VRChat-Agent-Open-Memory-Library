# Rules — 约束与强制要求速查

> Type: INDEX
> Last Updated: 2026-06-15
> 状态: ✅ 7 个 Rule Set / 80+ 规则已就位

---

## 概述

本目录存储**强制约束**（硬规则）。违反这些规则会导致编译失败、运行时崩溃、或严重性能问题。
所有规则必须 `FACT` 级别可信度，附带 `Source` + `Last Verified` 标注。

---

## Rule Set 索引

### 🌐 网络同步约束 (RULE-NW-*)

**[networking-rules.md](networking-rules.md)** — 22 条规则

涵盖：
- 所有权写入 (NW-01, 12)
- Manual Sync + RequestSerialization (NW-02, 16)
- Late Joiner 同步 (NW-03, 11, 20)
- Network Event 限制 (NW-04, 14, 22)
- 带宽预算 (NW-05, 13, 16)
- 同步模式选择 (NW-06, 07)
- 所有权转移 (NW-08, 10, 19, 21)
- 反序列化 (NW-09, 11, 17, 18)

**何时使用**: 任何涉及 `[UdonSynced]` / `SendCustomNetworkEvent` / `OnDeserialization` 的代码

---

### 🧠 Udon VM 架构 (RULE-VM-*)

**[udon-vm-architecture.md](udon-vm-architecture.md)** — VM 内部机制

涵盖：
- 9 条指令的字节码实现
- StrongBox<T> 装箱/拆箱
- EXTERN 调用成本
- 10 秒硬限制
- LightweightStack 实现
- Heap 数据结构

**何时使用**: 性能分析、字节码调优、底层调试

---

### ⚡ UdonSharp 语言限制 (RULE-LL-*)

**[udonsharp-language-limits.md](udonsharp-language-limits.md)** — 14 条规则

涵盖：
- 集合类禁止 (LL-01, 02)
- 异步/异常/委托禁止 (LL-02)
- 条件编译 (LL-04)
- GetComponent 限制 (LL-05)
- Struct 不可变 (LL-06)
- 字段初始化器 (LL-07)
- ProgramAsset 配置 (LL-08, 09)
- 递归与回调 (LL-10, 11, 12)
- SDK 3.7.1+ 可用特性 (LL-13)
- VRC Graphics 限制 (LL-14)

**何时使用**: 任何 C# 语法→Udon 转换的判断

---

### ⚡ 性能约束 (RULE-PR-*)

**[performance-rules.md](performance-rules.md)** — 12 条规则

涵盖：
- Update 成本
- EXTERN 调用频率
- 内存分配 (GC)
- 字符串拼接
- 集合类型
- 事件处理
- 字符串到值类型转换

**何时使用**: 任何性能敏感代码的审计

---

### 🤝 多 VM 协作约束 (RULE-MV-*)

**[multi-vm-rules.md](multi-vm-rules.md)** — 9 条规则

涵盖：
- SendCustomEvent 跨脚本
- SetProgramVariable 用法
- Update 顺序
- 初始化时序
- 公共状态管理
- 死亡螺旋防护

**何时使用**: 任何涉及 2+ UdonBehaviour 协作的代码

---

### ⚠️ UdonSharp 深度陷阱 (RULE-DP-*)

**[udonsharp-deep-pitfalls.md](udonsharp-deep-pitfalls.md)** — 19 条规则

涵盖：
- 静默失败（编译通过但行为异常）
- 编译器 bug
- API 边界情况
- 数据类型转换
- Update/事件时序
- SetProgramVariable 风险
- 静态字段陷阱

**何时使用**: 排查"代码看起来对但不工作"的问题

---

### 🔌 API 暴露判断 (RULE-AE-*)

**[vrchat-api-exposure.md](vrchat-api-exposure.md)** — API 暴露规则

涵盖：
- 暴露判断标准
- 编译时检查
- 运行时回退行为
- 自定义类型暴露要求

**何时使用**: 使用任何 C# API 前先查

---

## 规则使用工作流

```
1. 编码前
   ↓ 查 udonsharp-language-limits.md → 确认语法合规
   ↓ 查 performance-rules.md → 确认性能预算
   ↓
2. 编码中
   ↓ 涉及 [UdonSynced] → 查 networking-rules.md
   ↓ 涉及跨脚本 → 查 multi-vm-rules.md
   ↓ 涉及 Unity API → 查 vrchat-api-exposure.md
   ↓
3. 调试时
   ↓ 行为异常 → 查 udonsharp-deep-pitfalls.md
   ↓ 性能问题 → 查 udon-vm-architecture.md
```

---

## 规则严重度

| 等级 | 后果 | 行动 |
|------|------|------|
| **P0 编译失败** | 编译直接失败 | 必须避免 |
| **P0 运行时崩溃** | VRChat 客户端崩溃 | 必须避免 |
| **P1 静默失败** | 编译通过但不工作 | 必须验证 |
| **P2 性能问题** | 帧率/CPU 影响 | 高频路径必须验证 |
| **P3 反模式** | 可用但应避免 | 审查时建议改写 |

> 完整严重度模型见 `memory/reviews/severity-model.md`

---

## 与其他目录的关系

| 关系 | 目录 |
|------|------|
| **设计模式（合规实现）** | `memory/patterns/` |
| **审查清单（如何检查）** | `memory/reviews/` |
| **失败案例（违反后果）** | `memory/reviews/common-failures.md` |
| **API 速查（暴露状态）** | `memory/api/` |
| **应用层详解** | `memory/world/udon/networking/` |

---

## 规则更新流程

新增规则需满足：
1. 来源可信（Tier A/B）
2. 标注 SDK 版本
3. 提供反例 + 修复
4. 标注发现日期
5. 关联现有规则或失败案例

详见 `memory/_always-load.md` 中"知识优先级"部分。
