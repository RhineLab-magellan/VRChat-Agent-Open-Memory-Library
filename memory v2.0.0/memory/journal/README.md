---
title: Journal — 会话记忆目录
category: journal

knowledge_level: applied
status: active

tags:
  - journal
  - udonsharp
  - navigation

aliases:
  - "Journal — 会话记忆目录"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-15
confidence: Medium
---
# Journal — 会话记忆目录


---

## 目录用途与状态

| 目录 | 用途 | 状态 | 占位 |
|------|------|------|------|
| **`sessions/`** | 工作会话记录 | ⚠️ 空(2026-06-21 清理:12 个 session 已沉淀到长期知识库) | `.gitkeep` |
| **`reviews/`** | 代码审查记录 | ⚠️ 空 | `.gitkeep` |
| **`issues/`** | 问题追踪 | ⚠️ 空 | `.gitkeep` |
| **`drafts/`** | 临时草稿 | ⚠️ 空 | `.gitkeep` |

> 状态说明:⚠️ 空目录保留 `.gitkeep` 文件作为占位符,等待首次记录。
> 2026-06-21 精简:sessions 内的 12 个过程记录已全部沉淀到 `sources/`、`patterns/`、`FACT.md` 等长期知识库,按"短期记忆删除,长期记忆提炼"原则清理。

---

## 清理策略

| 类型 | 保留时间 |
|------|----------|
| 会话记录 | 30 天 |
| 审查记录 | 60 天 |
| 问题追踪 | 问题关闭后 7 天 |
| 临时草稿 | 7 天后自动清理 |

---

## 文件命名规范

```
YYYY-MM-DD_[类型]_[摘要].md
```

---

## 与知识库的区别

| Journal (临时) | Knowledge (持久) |
|----------------|------------------|
| 会话工作记录 | 架构设计决策 |
| 代码审查结果 | 验证过的模式 |
| 问题调试过程 | 已确认的限制 |
| 临时方案草稿 | 可复用的模板 |

**原则**:知识入库后,从 Journal 删除对应记录(2026-06-21 已执行)。

---

## 推荐工作流

1. **每次重要操作结束** → 在 `sessions/` 创建 session 记录
2. **每次代码审查** → 在 `reviews/` 创建审查记录
3. **发现新问题** → 在 `issues/` 创建追踪记录
4. **临时草稿** → 放在 `drafts/`，7 天后清理或晋升

---

## 维护建议

- 月度清理：删除超过保留时间的记录
- 季度审查：检查是否有记录应晋升到 `memory/`
- 自动清理：可通过 cron 任务实现（详见 `mcp__claw__cron`）
