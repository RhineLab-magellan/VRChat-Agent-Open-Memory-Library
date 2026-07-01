---
title: VRChat Community Labs — World 社区实验室发布系统
category: world

knowledge_level: applied
status: active

tags:
  - world
  - publishing
  - trust
  - community

aliases:
  - "Community Labs"
  - "World 发布"
  - "社区实验室"
  - "CL"

related:
  - "world/creator-economy.md"
  - ../avatar/trust-rank.md
  - "rules/vrchat-api-exposure.md"
  - ../FACT.md

source: https://docs.vrchat.com/docs/vrchat-community-labs
source_type: community
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat Community Labs — World 社区实验室发布系统

> 来源: VRChat 官方文档 - VRChat Community Labs
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **关键 Insight**: Community Labs 是 World 公开前的**过渡阶段**,自动晋升到 Public 基于用户参与度。

---

## 1. 概述

**Community Labs**(社区实验室)是 VRChat World 发布的过渡系统。

**当前状态**: **Stage 2**

### 1.1 默认状态

- 默认情况下,World 是 **Private**(私有)
- 只能被自己和持有链接的用户访问
- 提交到 Community Labs 后**停止** Private,所有用户可见

### 1.2 流程

```
Private World
   ↓ (提交到 Community Labs)
Community Labs
   ↓ (自动晋升基于用户参与度)
Public
```

---

## 2. 用户探索 Community Labs

### 2.1 入口

- Worlds tab → Community Labs 行
- 需在 "Comfort and Safety" 设置中启用 "Show Community Labs"

### 2.2 视觉识别

- Community Labs World 的 Portal 有**特殊图标和圆环**
- 加载时显示**警告**(World 未审核)

### 2.3 举报机制

- Quick Menu → "Report this world" 快捷按钮
- Recent Worlds 中也可举报
- 防止"report bombing"已有保护措施

---

## 3. 发布到 Community Labs

### 3.1 发布流程

**方法 A: SDK**
```
Build and Upload → "World Visibility" 区域
  → "Publish to Community Labs" 按钮
```

**方法 B: 网站**
```
vrchat.com/home/content/worlds
  → 选择 Private World
  → "Publish to Community Labs" 按钮
```

### 3.2 关键限制

| 限制 | 值 |
|------|-----|
| **每周发布新 World 数** | **1 个/周** |
| **最低 Trust Rank** | **User** 或更高 |
| **更新频率** | **任意**(不影响状态) |

### 3.3 自动晋升

- **基于用户参与度自动晋升**到 Public
- 无固定时间
- 参与度高的 World 快速晋升
- 参与度低的 World 长期停留
- 最终都会晋升(无时间上限)

### 3.4 失败处理

- 有效报告 → World 移出 Labs
- 严重违规 → 创作者可能被限制提交
- 修复后可重新提交

---

## 4. FAQ 关键问题

### Q1: 我有 Private World,如何放入 Community Labs?

> A: SDK 按 "Publish to Community Labs" 按钮,或网站按 "Publish" 按钮。每周只能发布 1 次。

### Q2: Public 状态需要多久?

> A: 无固定时间,基于用户参与度。因素可概括为"用户是否享受 World"。

### Q3: 发布到 Community Labs 需要什么 Trust Rank?

> A: **至少 User Trust Rank**。可能根据反馈调整。

### Q4: 每周只能发布 1 次?如何迭代更新?

> A: 限制**仅适用于发布全新 World**。已存在的 World(Private / CL / Public 状态)可**随时更新**,状态不变。

### Q5: 我已有 Public World,需要担心什么吗?

> A: **不需要**。你已 Grandfathered 进入 Public 流程。奖励:可随时更新而无须重新审批。

### Q6: 更新 Public World 会丢失统计吗?

> A: **不会**。统计完全保留。

### Q7: World 分类为 Avatar/Game World 如何做?

> A: 通过 VRChat 网站或 SDK 加适当 tag。**禁止**:
> - 错误分类
> - 滥用 tag 推广
> - "SEO-like" 技术
> VRChat 保留对违规用户的行动权。

### Q8: Community Labs 的内容规则与 VRChat 其他部分不同吗?

> A: **没有**。必须遵守:
> - VRChat Community Guidelines
> - VRChat Terms of Service
> - Creator Guidelines
> 违反可能导致**撤销**提交资格。

### Q9: World 如何"失败"离开 Community Labs?

> A: 被举报 → 调查 → 违规 → 移出 Labs。Public World 同理。

### Q10: World 失败后能做什么?

> A: 修复问题(如性能) → 重新提交到 Labs。严重违规(ToS 违反)可能限制提交资格。

### Q11: 如何防止 report bombs?

> A: VRChat 用**与现有用户/World 报告系统相同**的方法检测无效报告。这是经过测试的系统,防止恶意滥用。

### Q12: 如何撤回 Public/Community Labs World?

> A: VRChat Home 网站 → "Unpublish" 按钮。

**撤回效果**:
- 用户 Favorites 仍保留
- 部分 World 统计保留
- 用户列表显示 "world currently set to private"(看不到名字或图片)

---

## 5. Trust Rank 要求对照

| Trust Rank | 发布到 CL? | 备注 |
|------------|-----------|------|
| **Visitor** | ❌ | 未通过 Nuisance 过滤器 |
| **New User** | ❌ | 基础 Trust |
| **User** | ✅ | **最低要求** |
| **Known User** | ✅ | 正常 |
| **Trusted User** | ✅ | 正常 |
| **Developer** | ✅ | 高级功能 |

---

## 6. 与 Creator Economy 的关系

- **Community Labs** 是 World 发布通道
- **Creator Economy** 是销售虚拟产品
- 两者要求不同:
  - CL: Trust Rank "User" 或更高
  - CE: Trust Rank "New User" 或更高(更宽松)
  - 但 CL 和 CE 是独立的

详见 `memory/world/creator-economy.md`

---

## 7. 创作者策略

### 7.1 提升 World 参与度

| 因素 | 建议 |
|------|------|
| **性能** | 优化至 Good+,Quest 端 Good+ |
| **Tag 准确** | 正确分类(Avatar/Game) |
| **标题/描述** | 清晰、不夸张 |
| **首次体验** | 加载快、引导清晰 |
| **回访率** | 内容深度、可重复玩 |
| **社区反馈** | 监听报告并修复 |

### 7.2 更新策略

- **已发布 World 可随时更新** - 充分利用
- 修复 bug → 立刻更新
- 添加内容 → 保持活跃
- 更新不影响 CL 状态

### 7.3 避免违规

- 严格遵守 Community Guidelines
- 避免争议内容
- 性能优化(避免玩家卡顿报告)
- 正确的 tag(避免举报)

---

## 8. 风险与陷阱

| 风险 | 等级 | 说明 |
|------|------|------|
| **被举报移出 CL** | 🔴 高 | 违规内容会被移除,严重者失去提交权 |
| **参与度低长期停留** | 🟡 中 | World 可能长期在 CL,不影响更新但影响曝光 |
| **错误分类被举报** | 🟡 中 | 滥用 tag → 行动 |
| **每周限制** | 🟢 低 | 仅限新 World,更新无限 |
| **撤回后看不到名字** | 🟢 低 | 撤回 World 显示 "private",无名字 |
| **报告炸弹** | 🟢 低 | 系统已防护 |

---

## 9. 与其他系统的关系

### 9.1 World 分类

- Avatar World / Game World 等通过 **tag** 分类
- SDK 上传时可选 tag
- 网站可编辑 tag

### 9.2 World 实例

- Public World 可创建 Group/Group Public/Friends+ 实例
- CL World 同样支持实例

### 9.3 性能

- CL 不豁免 Performance Rank 检查
- 上传时仍需满足性能要求

---

## 10. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/vrchat-community-labs
- **官方版本**: Stage 2(当前)
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)

---

## 11. 相关文档

- `memory/world/creator-economy.md` — Creator Economy(不同发布通道)
- `memory/world/performance-guide.md` — World 性能优化
- `memory/world/scene-components/vrc-scenedescriptor.md` — World 场景配置
