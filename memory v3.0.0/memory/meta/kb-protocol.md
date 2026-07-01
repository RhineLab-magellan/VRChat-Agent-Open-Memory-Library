---
title: 知识库写入与维护协议
category: meta
status: active
tags:
  - meta
  - protocol
  - maintenance
knowledge_level: applied
aliases:
  - "知识库协议"
  - "KB Protocol"
  - "知识库写入协议"
  - "知识库维护协议"
related:
  - ../FACT.md
  - ../index.md
  - working-modes.md
source: SOUL.md v4.0 迁移
version: 1.0
last_review: 2026-06-21
confidence: High
---

# 知识库写入与维护协议

> 本文件从 SOUL.md v4.0 迁移。定义了知识写入流程和 Curator 模式维护协议。

---

## 知识写入流程

```
新发现 → journal append → 更新具体文件 → 更新域 index.md
                                         → 更新 _always-load.md（如核心约束）
                                         → 同步 FACT.md（如重大发现）
                                         → 更新 patterns/index.md（如新模式）
```

### 写入规则

1. **单一来源原则**：每份知识只存在于一个权威位置，其他地方只放引用指针
2. **先 journal 后 KB**：新发现先 append 到 journal，验证后再入知识库
3. **同步更新索引**：修改文件后必须更新对应的域 index.md
4. **核心约束升级**：如果新发现影响跨域约束，同步更新 `_always-load.md`

---

## 知识维护 Protocol（Curator 模式）

```
1. 审计：运行辅助脚本（validation → governance → version_audit → url_health）
2. 分析：识别 P0(严重)/P1(警告)/P2(建议) 分级问题
3. 修复："1 Agent 1 文档" 策略 + 二次独立验证
4. 验证：validation_script 全通过 + governance_script 无新增死链
5. 记录：FACT.md 追加时间戳条目 + journal 追加 session 记录
```

### 修复策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| 1 Agent 1 文档 | 每个 Agent 只负责一个文档的修复 | P0/P1 精确修复 |
| 二次独立验证 | 修复后由另一个 Agent 独立验证 | 所有 P0 修复 |
| 批量脚本修复 | 使用 Python 脚本批量替换 | URL 301、版本号等系统性问题 |

### 审计得分标准

| 等级 | 分数 | 状态 |
|------|------|------|
| A | 90+/100 | 优秀 |
| B | 70-89/100 | 良好（当前: 78/100） |
| C | 50-69/100 | 需改进 |
| D | <50/100 | 严重问题 |

---

## 文件职责边界

| 文件 | 职责 | 不应包含 |
|------|------|---------|
| `SOUL.md` | Agent 身份、行为准则、Domain Router | 详细案例、代码示例、工具表 |
| `FACT.md` | KB 结构、核心约束、修正记录、维护状态 | 设计模式代码实现、完整案例研究 |
| `_always-load.md` | 跨域约束速查、自检清单、文件路由 | 域内专业知识 |
| `index.md` | 多领域路由地图、完整文件清单 | 约束定义、行为准则 |
| `memory/meta/` | 工作模式定义、维护协议、脚本说明 | 领域知识 |
