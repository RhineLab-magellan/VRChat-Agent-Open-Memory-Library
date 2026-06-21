# VRChat-Agent-Open-Memory-Library v2.0.0

> 🧬 SOUL + Memory 双层架构，Agent 身份驱动型 VRChat 技术知识库。

## 概述

v2.0.0 架构性升级：新增 SOUL.md Agent 身份系统（6 领域路由 + 6 工作模式 + 4 级证据体系），形成 **SOUL（定义 Agent 是谁）+ Memory（定义 Agent 知道什么）** 双层设计。全库 YAML 元数据标准化，新增 `meta/` 治理体系，文件从 295 增至 313，总量 2.8 MB。

## 新增

- **SOUL.md** — Agent 工程人格 + Domain Router + Architect/Engineer/Reviewer/Teacher/Researcher/Curator 六模式
- **VRCTween** — 官方补间系统（7 大类 + 12 实战模式）
- **Udon Persistence** — 8 文档 + 3 实战 Pattern（PlayerData/PlayerObject）
- **Data Containers 重构** — DataToken/DataList/DataDictionary/VRCJSON 独立子路径
- **YAML frontmatter** — 全库标准化元数据（title/category/tags/confidence）
- **meta/ 治理体系** — 写入协议 + 工作模式完整定义 + 5 维护脚本

## 使用

支持 GitHub Copilot、Cursor、Cherry Studio、通用 LLM Chat、OpenAI GPTs 五种 Agent 平台。将 `SOUL.md` 设为 System Prompt，`memory/` 作为知识库加载即可。

```bash
git clone https://github.com/RhineLab-magellan/VRChat-Agent-Open-Memory-Library.git
```

详细文档见 [README.md](README.md) | 变更记录见 [CHANGELOG.md](CHANGELOG.md)。
