# Journal — 会话记忆目录

> Type: EPHEMERAL
> Purpose: 非知识类记忆存储，定期清理防止污染知识库
> Last Updated: 2026-06-15

---

## 目录用途与状态

| 目录 | 用途 | 状态 | 占位 |
|------|------|------|------|
| **`sessions/`** | 工作会话记录 | ✅ 3 个文件 | — |
| **`reviews/`** | 代码审查记录 | ⚠️ 空 | `.gitkeep` |
| **`issues/`** | 问题追踪 | ⚠️ 空 | `.gitkeep` |
| **`drafts/`** | 临时草稿 | ⚠️ 空 | `.gitkeep` |

> 状态说明：⚠️ 空目录保留 `.gitkeep` 文件作为占位符，等待首次记录。

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

示例：
- `2026-06-11_session_udon-type-exposure-analysis.md` ✅ 已存在
- `2026-06-15_session_knowledge-base-audit-refactor.md` ← **本次重构 session 应记录**
- `2026-06-12_review_player-script-check.md` ← 未来审查记录
- `2026-06-11_issue_compilation-error-debug.md` ← 未来问题追踪

---

## 与知识库的区别

| Journal (临时) | Knowledge (持久) |
|----------------|------------------|
| 会话工作记录 | 架构设计决策 |
| 代码审查结果 | 验证过的模式 |
| 问题调试过程 | 已确认的限制 |
| 临时方案草稿 | 可复用的模板 |

**原则**：知识入库后，从 Journal 删除对应记录。

---

## 当前已存在文件

### sessions/
- `2026-06-11_session_udon-type-exposure-analysis.md` — Udon Type Exposure Tree 解析 + 4 个 API 文档创建
- `2026-06-15_session_knowledge-base-audit-refactor.md` — 首次审计:5 个 index.md + 3 个 redirect + 3 个 .gitkeep
- `2026-06-15_session_second-audit.md` — 二次审计:1 个 outline.md 修复 + 4 个新域索引(vrchatsdk/platform/misc/references)|

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
