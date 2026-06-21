---
title: 辅助脚本清单
category: meta
status: active
tags:
  - meta
  - scripts
  - maintenance
related:
  - ../FACT.md
  - working-modes.md
source: SOUL.md v4.0 迁移
version: 1.0
last_review: 2026-06-21
confidence: High
---

# 辅助脚本清单

> 本文件从 SOUL.md v4.0 迁移。仅 Curator 模式使用。
> 所有脚本位于项目根目录 `Auxiliary script/` 下。

---

## 脚本列表

| 脚本 | 用途 | 运行频率 |
|------|------|---------|
| `validation_script.py` | YAML frontmatter + 链接结构验证 | 每次维护必跑 |
| `governance_script.py` | 孤立文件 + 死链 + 尾部页面检测 | 每次维护必跑 |
| `version_audit_script.py` | GitHub Releases 版本号批量核对 | 季度 / SDK 更新后 |
| `url_health_check.py` | 16 线程并发 URL 健康检查 | 季度 / 大规模修改后 |
| `pure_knowledge_audit.py` | 新旧库纯粹知识差异分析 | 库迁移/重构后 |

## 维护周期建议

- **常规维护**：季度运行 validation + governance + url_health
- **SDK 更新后**：加跑 version_audit
- **大规模重构后**：全量 5 脚本
- **GitHub 限流**：配 GitHub token 提升 rate limit

## 运行顺序

```
1. validation_script.py    → 确保 frontmatter 和链接结构正确
2. governance_script.py    → 检测孤立文件、死链、尾部页面
3. version_audit_script.py → 核对工具版本号是否过期
4. url_health_check.py     → 检查所有 URL 是否可达
5. pure_knowledge_audit.py → (可选) 与备份库对比纯粹知识差异
```
