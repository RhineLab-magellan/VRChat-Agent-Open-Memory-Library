---
title: Graph Elements | Graph 元素
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - udonsharp

aliases:
  - "Graph Elements | Graph 元素"

related:
  - special-nodes.md
  - index.md
  - event-nodes.md
  - searching-for-nodes.md
  - type-nodes.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Graph Elements | Graph 元素

> 来源: https://creators.vrchat.com/worlds/udon/graph/graph-elements/
> 更新日期: 2024-05-29
> 索引日期: 2026-06-15
> Domain: World / Udon

Graph 中除 **Nodes(节点)** 外的其他元素。**这些元素不影响 Graph 的功能或编译**,只影响可读性。

> **任务提示词原文**提到 "Variable、Float、Block、Comment、Group" 作为基础元素。
> **实际官方文档** 本页面只覆盖 **Groups / Comments / Noodles** 三类,Variable/Float/Block 在 [`special-nodes.md`](./special-nodes.md) 详述。

---

## Overview(概览)

构建 Graph 程序时,主要使用 **Nodes**。本页描述的少量其他元素用于组织与可读性。

> **【推断】** 任务提示词中的"Variable / Float / Block"实际上是**特殊节点**或**变量面板对象**,并非"Graph 元素"。本文件按官方文档结构忠实记录。

---

## Groups(分组)

**作用**:组织和描述 Graph。**不影响**功能与编译。

### 创建 Groups

**方法 A — 选中后创建**:
1. 通过**框选(box-drag)**或**按住 Ctrl 点击**选中元素
2. 右键 Graph,选择 `Create Group`
3. **快捷键**: 按 `Ctrl+G` 快速分组

**方法 B — 创建后拖入**:
1. 右键 Graph 空白处,选择 `Create Group`
2. **拖动元素**到 Group 中

### 从 Group 中移除元素

| 方法 | 操作 |
|------|------|
| 菜单移除 | 选中元素 → 右键 → `Remove From Group` |
| 拖出移除 | 选中元素 → **按住 Shift** → **拖出 Group** |

### 跳转到 Group

在 **Graph Sidebar** 中点击 Group 项即可跳转。

### 嵌套 Group(不支持)

> ⚠️ **目前不支持嵌套 Group**。当前行为: 试图**选中并包围**已有 Group 创建新 Group 时,**会删除现有 Group**。

> **【风险】** 复杂 Graph 分层请使用 Comments + 编号方案(例如 `// === SECTION A ===` / `// --- Sub A1 ---`)

---

## Comments(注释)

简单的**文本块**,放置在需要更多信息的项附近。

### 创建方式

**右键 Graph → Create Comment**

### 特性

- 可**添加到 Groups** 中
- 与 Groups 配合使用 = **最佳可读性**

> **【推断】** 与代码注释不同,Comments **不参与编译**,仅作 Graph 内文档。适合标记:
> - 模块入口
> - 待办事项
> - 复杂逻辑的说明
> - 作者/最后修改时间

---

## Noodles(连接线,Edges)

> **"Noodle"** 是 Udon Graph 社区对**连接节点端口的曲线**的称呼。Unity 文档中称为 **"edges"**。

### 关键特性

- **连接节点端口**
- **端口颜色编码**:
  - 同类型端口连接 → 整条 Noodle 同色
  - 不同类型端口连接 → Noodle 中间**渐变**表示类型转换
- **类型不匹配的端口无法连接**(但 Noodle 颜色变化提示隐式转换)

> **【推断】** Noodle 颜色遵循 Unity 约定:
> - float = 绿色
> - Vector3 = 蓝色
> - bool = 红色
> - string = 黄色
> - object = 灰色
> (具体配色以 SDK 内置为准)

---

## 任务提示词对照

| 任务要求元素 | 实际文档位置 |
|------------|------------|
| **Variable** | 不在本页 → 详情见 `special-nodes.md` 的 Get/Set Variable 节点,以及 `index.md` 的 Drag and Drop for Variables |
| **Float** | 不在本页 → Float 是**基础类型**,通过快捷键 `1` 创建(见 `index.md`) |
| **Block** | 不在本页 → 详情见 `special-nodes.md` |
| **Comment** | ✅ 在本页(Comments 章节) |
| **Group** | ✅ 在本页(Groups 章节) |
| **Noodle** | ✅ 在本页(Noodles 章节) |

---

## 相关知识库

- [`index.md`](./index.md) — Udon Node Graph 主页
- [`event-nodes.md`](./event-nodes.md) — Event 节点
- [`searching-for-nodes.md`](./searching-for-nodes.md) — 节点搜索
- [`special-nodes.md`](./special-nodes.md) — 特殊节点(Variable/Block/...)
- [`type-nodes.md`](./type-nodes.md) — 类型引用节点
