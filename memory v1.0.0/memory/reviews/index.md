# Reviews — 审查方法论入口

> Type: INDEX
> Last Updated: 2026-06-15
> 状态: ✅ 3 个核心审查文档已就位

---

## 概述

本目录提供 UdonSharp 脚本的**审查标准、检查清单、失败案例**。审查者（人类或 Agent）应按以下流程工作：

```
脚本/项目 → review-checklist.md（15 项检查）
         → severity-model.md（如何分级）
         → common-failures.md（已知失败模式）
         → 反馈给开发
```

---

## 3 个核心审查文档

### 📋 review-checklist.md

**15 项 UdonSharp 脚本审查清单**

覆盖：
- 基础身份（继承、SyncMode）
- 语言合规（禁用特性检查）
- API 合规（暴露状态、热路径）
- 网络同步（所有权、序列化、Late Joiner）
- 性能（Update、EXTERN、内存）
- 协作（多 VM 通信、初始化时序）

**何时使用**: 任何代码审查的第一步

---

### ⚖️ severity-model.md

**风险分级标准**

| 等级 | 后果 | 修复优先级 |
|------|------|----------|
| **Critical (严重)** | 编译失败、运行时崩溃、网络状态错误、Late Joiner 数据永久缺失 | 立即修复，阻塞合并 |
| **High (高)** | 性能严重下降、关键功能失效、用户可见错误 | 24h 内修复 |
| **Medium (中)** | 性能下降、边界场景失效、可避免的反模式 | 1 周内修复 |
| **Low (低)** | 代码异味、可读性、未来兼容性风险 | 改善，不阻塞 |

**何时使用**: 审查后给出风险分级，决定修复优先级

---

### 🚨 common-failures.md

**已知失败模式集合 (FAIL-* ID)**

按 ID 分类：
- **FAIL-01 ~ FAIL-10**: 网络同步类（最常见）
- **FAIL-11 ~ FAIL-20**: 性能类
- **FAIL-21 ~ FAIL-30**: API 误用类
- **FAIL-31+**: 边界情况类

每条失败模式包含：
- 症状（如何识别）
- 原因（为什么会发生）
- 修复（如何解决）
- 规则引用（关联 RULE-* ID）

**何时使用**: 
- 审查时对比检查
- 调试时定位问题
- 培训新人时作为反面教材

---

## 审查工作流

### 1. 审查准备

```
□ 确认审查范围（单文件/多文件/整个项目）
□ 加载 review-checklist.md
□ 加载 severity-model.md
□ 加载 common-failures.md
```

### 2. 逐项检查

```
按 review-checklist.md 的 15 项顺序检查
    ↓
对每项不通过项查找 common-failures.md 是否已有 FAIL-* 记录
    ↓
按 severity-model.md 评估等级
```

### 3. 输出审查报告

```markdown
# 审查报告

## 总结
- 审查范围: XXX
- Critical: N
- High: N
- Medium: N
- Low: N

## Critical 问题
### [FAIL-01] 忘记 RequestSerialization
- 文件: X.cs:25
- 描述: ...
- 修复: ...

## 建议（非阻塞）
...
```

### 4. 后续追踪

```
□ 记录到 journal/reviews/（60 天保留）
□ 失败模式新增 → 更新 common-failures.md
□ 规则缺失 → 更新 rules/ 目录
```

---

## 与其他目录的关系

| 关系 | 目录 |
|------|------|
| **执行规则** | `memory/rules/` |
| **实现模式** | `memory/patterns/` |
| **API 速查** | `memory/api/` |
| **审查记录** | `memory/journal/reviews/` |
| **失败案例** | `memory/reviews/common-failures.md` |
| **设计模式来源** | `memory/FACT.md` §VRCTD/§VVMW/§AudioLink |

---

## 审查者工具

| 工具 | 用途 | 位置 |
|------|------|------|
| **API Checker** | C# 代码静态分析（Udon 暴露检查） | `memory/api/api-checker.md` |
| **Udon Type Exposure Tree** | API 暴露状态查询 | `memory/api/udon-type-exposure.md` |
| **Common Failures** | 失败模式匹配 | `memory/reviews/common-failures.md` |

---

## 案例参考

完整的审查应用案例：
- VRCTD 5 层同步体系审查（参见 `memory/FACT.md` §VRCTD）
- VVMW 时间同步审查（参见 `memory/FACT.md` §VVMW）
- AudioLink 数据传递审查（参见 `memory/FACT.md` §AudioLink）

---

## 维护

| 任务 | 频率 | 责任 |
|------|------|------|
| 更新 common-failures.md | 每次发现新 FAIL | 任何审查者 |
| 更新 review-checklist.md | SDK 重大更新时 | Curator |
| 更新 severity-model.md | 季度评审 | Curator |
| 清理 journal/reviews/ | 60 天滚动 | 自动/手动 |
