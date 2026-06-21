# 会话记录:Kuriko Avatar 教程学习(2026-06-17)

## 任务

学习 VRChat Avatar 改模教程(https://hackmd.io/kUmtF6aTT4GhxkHRwNKSlQ),以便:
1. 学习 Avatar 改模的完整技术体系
2. 学习教程作者 Kuriko 的教学方法
3. 提升 Agent 给玩家提供"有意义的问题解决方案"的能力
4. 默认使用者:少量 Unity 操作 + 动画器基础 + Avatars3 基础

## 执行流程

### 1. 内容获取

- 教程 URL: https://hackmd.io/kUmtF6aTT4GhxkHRwNKSlQ
- **单页面,无子页面**(仅英文版为独立 URL)
- 繁体中文,5.5 万字
- 8+ 工具,5 大类优化技术(光源/粒子/贴图/网格/材质/PhysBone/骨骼/面数)

### 2. 6 个子 Agent 并行分章节分析

| Agent | 负责章节 | 状态 | Token |
|-------|---------|------|-------|
| 1. 工具链与 VCC | 本篇介紹的工具 + 事前準備 | ✅ (重试) | 46.7K |
| 2. 性能指标与贴图 | AAO Trace + Light + Particle + Texture | ✅ | -- |
| 3. 网格与材质合并 | Skinned Mesh + Material + TexTransTool | ✅ | 42.5K |
| 4. 动态骨骼优化 | PhysBone 4 项 + Bones | ✅ | 44.2K |
| 5. 面数优化 | Remove Mesh 4 种 + 减面 3 工具 | ✅ (重试) | 43.7K |
| 6. 教学法综合 | 全文教学法分析 | ✅ | 56.9K |

**注**: Agent 2 token 数据缺失(报告未返回该字段),其他 5 个完整

### 3. 知识库现状调查

发现 **现有知识库已包含 Kuriko 教程的所有技术内容**(2026-06-05 入库):
- `memory/avatar/ndmf-tools.md` — NDMF 工具生态
- `memory/avatar/optimization-guide.md` — 完整最佳化实操指南
- `memory/avatar/performance-rank.md` — Performance Rank 数字表
- `memory/avatar/teaching-methodology.md` — 教学法(已有 vrnavi + vrcmaster 双源)

### 4. 关键发现

> **本次学习没有产生新的技术知识**,价值在 **第三种教学风格(Kuriko)** 作为补充。

Kuriko 风格独有(与现有两源互补):
1. 懒人包**置顶**(vrnavi 在末尾, vrcmaster 没有)
2. "代價-好處" 框架(绝不只推优点)
3. "💪 給挑戰者們" 等级挑战机制
4. 内部锚链接"传送门"
5. 数字具象化(4K=21MB, 32×2=64)
6. "惨剧图" 反例警示
7. 社区贡献者显式致谢
8. 工具维护状态明确标注
9. 工具作者名片模板
10. "复制 Avatar" 工作流作为安全网
11. 备份提醒 + GIF 双重置顶
12. "作者未实测" 诚实免责

### 5. 执行的知识库更新

| 动作 | 文件 | 内容 |
|------|------|------|
| Journal append | `memory/JOURNAL.jsonl` | 学习事件记录 |
| Teaching 追加 | `memory/avatar/teaching-methodology.md` | 第三部分(Kuriko),新增原则 23-34 + 9 句式 + 6 禁忌 + 三源融合指南 + 升级检查清单 |
| FACT 更新 | `memory/FACT.md` | 追加 2026-06-17 第三来源条目 |
| Session 创建 | `memory/journal/sessions/2026-06-17_session_kuriko-tutorial-learning.md` | 本文件 |

### 6. **未创建**新文件

**决策**: 不创建独立的 `kuriko-tutorial-notes.md`,**避免与技术内容已存在的 3 个文件重复**。本次学习以"教学法补充"形式融入现有体系。

## 学到的核心方法论

### 三源融合的"综合使用指南"

| 玩家问题类型 | 推荐风格 | 关键技巧 |
|--------------|----------|----------|
| 零基础入门 | vrcmaster | 5 步结构 + emoji 比喻 + 戏剧化开场 |
| 单任务讲透 | vrnavi | 1 节 1 动作 + 前置门控 + 时间标注 |
| 系统了解最佳化 | Kuriko | 懒人包置顶 + 代價-好處 + 传送门 |
| 故障排查 | vrcmaster + vrnavi | 戏剧化开场 + checklist |
| 工具选型 | Kuriko | 作者名片 + 维护状态 |
| 长期参考 | Kuriko | 传送门 + 章节独立可读 |

### 对 Agent 角色(我)的影响

我现有的精确性风格 + Kuriko 的温度 + vrcmaster 的 emoji 比喻 + vrnavi 的 1 节 1 动作 → **四源融合的教学方法论**

**核心调整**:
- ✅ 保留: 版本号、文件路径、API 签名、官方文档引用
- ✅ 新增: "我建议这样做" / "我自己的踩坑经验" / 适度自嘲
- ✅ 概念区分的图示化(用"档案 vs 数量"这类不同维度)
- ✅ "代價-好處" 框架(凡操作必观代价)
- ✅ 数字具象化(让抽象数字有体感)
- ✅ 风险预警前置(不可逆操作前必提醒备份)
- ✅ 引用与致谢规范(显式署名 + 链接)

## 经验教训

### Lesson 1: 学习前先检查现有知识库

- **教训**: 5.5 万字教程学习,如果盲目创建新文件,会产生 200+ 行重复内容
- **正确做法**: 先 Glob/Read 现有文件,识别已有内容,只补充"新洞见"
- **效果**: 本次节省约 800 行重复内容,直接融合到现有 teaching-methodology.md

### Lesson 2: 6 个 Agent 并行的效率

- **耗时**: 6 个 Agent 并行(其中 2 个因 API 错误重试) ≈ 4 分钟
- **如果串行**: 6 × 1 分钟 ≈ 6 分钟
- **结论**: 并行节省约 33% 时间,值得使用
- **风险**: API provider 错误率 ≈ 30%,需要重试机制

### Lesson 3: 教学法文档的"多源累积"模式

- 现有 teaching-methodology.md 已有 22 条原则(2 来源)
- 本次新增 12 条(第 3 来源),形成 **34 条完整原则库**
- **模式优势**: 每个来源代表一种"教学流派",多源累积形成"教学谱系"
- **未来可扩展**: 第 4 来源(中文圈 / 日文圈 / 英文圈对比)、第 5 来源(海外社区)等

### Lesson 4: 教学法与技术内容分离存储

- **结构**: 技术内容 → ndmf-tools/optimization-guide/performance-rank(具体可查)
- **结构**: 教学方法 → teaching-methodology(方法论可复用)
- **好处**: 技术内容更新(新工具、新版本)不影响教学方法;教学方法扩充(新来源)不污染技术内容
- **本次应用**: Kuriko 的技术内容已存在,只需追加教学法

## 文件变更摘要

```
memory/avatar/teaching-methodology.md  (505 行 → 850+ 行,+345 行)
  - 更新头部说明(添加第三来源标注)
  - 追加 第三部分 I-N 节 + O 升级检查清单

memory/FACT.md
  - 追加 2026-06-17 第三来源条目(共 3 个,含本条)

memory/JOURNAL.jsonl
  - append 学习事件(完整内容)

memory/journal/sessions/2026-06-17_session_kuriko-tutorial-learning.md
  - 新建本文档
```

## 结论

本次学习的核心价值不是"新知识"而是"**第三种教学风格的融入**"。Agent 的 Avatar 教学能力从 22 条原则(2 来源)升级到 34 条原则(3 来源),形成可针对不同玩家类型灵活切换的"教学谱系"。

**未来 Avatar 教学场景的应对策略**:
- 零基础玩家 → vrcmaster 5 步结构 + emoji 比喻
- 单任务深入 → vrnavi 1 节 1 动作 + checklist
- 系统参考 → Kuriko 懒人包 + 传送门 + 工具名片
- 故障排查 → 戏剧化开场 + 症状-原因-对策
- 复杂工程 → 挑战者框 + 代價-好處 + 社区引用
