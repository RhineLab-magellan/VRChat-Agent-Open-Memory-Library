# Changelog

## v2.0.0 (2026-06-21)

### 架构升级：新增 Agent 身份系统

根目录新增 `SOUL.md`（v5.0-slim），定义 Agent 为"知识驱动型 VRChat 技术架构师"，包含 6 种工作模式自动选择、6 域路由表和工程人格设定。

### 元数据标准化

所有核心文件新增 YAML frontmatter（title、category、tags、confidence 等），实现可机器解析的知识图谱层。

### 知识库治理体系建立

新增 `meta/` 目录，含知识写入协议、工作模式详细定义、辅助脚本清单三项核心治理文件，从 SOUL.md 迁移瘦身而来。`_curator_tools/` 为未来策展工具预留。

### 内容增量

- 文件从 295 增至 313（+18），总规模从 2.5MB 增至 2.8MB
- 新增 VRCTween 官方补间文档
- 新增 Udon Persistence 实战子目录（8 文档）
- Data Containers 子路径重构
- LuraSwitch2 更新至 v1.06（VN3 License）
- VRCGraphics 重构纳入 udon 子目录

### 总结

v2.0.0 是一次架构性升级，核心变化是 Agent 身份定义 + 元数据标准化 + 治理体系建立，为知识库的可持续维护奠定基础。

---

## v1.0.0 (初始版本)

VRChat 技术知识库初始版本，包含 295 个文件，覆盖 World、Avatar、Hybrid、Platform、VRChatSDK、Sources 六大领域。
