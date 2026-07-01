---
title: "Searching for Nodes | 节点搜索"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - udon
  - udon-graph
aliases:
  - "Searching for Nodes | 节点搜索"
  - searching-for-nodes
related:
  - index.md
  - event-nodes.md
  - graph-elements.md
  - special-nodes.md
  - type-nodes.md
  - "api/exposed-types.md"
  - "api/not-exposed.md"
---
# Searching for Nodes | 节点搜索

> 来源: https://creators.vrchat.com/worlds/udon/graph/searching-for-nodes/

5 种节点搜索方式,适用于不同场景。

---

## 1. Quick Search(快速搜索)

> **快捷键**: `Spacebar`

输入要交互的**类的前几个字母**。

**最佳场景**:**了解 Unity 基础类与对象类型**的用户
- 例如: 输入 `vec3` 快速找到 `Vector3` 相关节点
- 适合知道目标类型,只想找方法的场景

**优势**: 速度最快

---

## 2. Full Search(完整搜索)

> **快捷键**: `Tab`

搜索**任何对象上的任何方法**。

### 搜索语法

| 模式 | 示例 | 结果 |
|------|------|------|
| **方法名模糊匹配** | `getname` | 所有能"获取名称"的对象 |
| **完全限定名** | `gameobject.getname` | 精确定位到 `GameObject.GetName` 节点 |

**优势**: 即使不知道目标类,也能通过方法名反向搜索
**劣势**: 速度比 Quick Search 慢

**建议**: **仅在 Quick Search 中不确定类名时使用**

---

## 3. Search Bar(Graph 内搜索)

Udon Graph Sidebar 顶部的搜索栏。

| 行为 | 说明 |
|------|------|
| 快捷键 | `Ctrl + F` 在 Graph Window 中聚焦 |
| 触发阈值 | 输入**超过 3 个字符**后开始返回结果 |
| 结果跳转 | 按 `Enter` 在结果间跳转,顺序为 **"最佳匹配优先"** |

**最佳场景**: 在大型 Graph 中**快速定位特定节点**

---

## 4. Focused Search(聚焦搜索)

> **默认关闭**,需手动启用。

### 启用步骤

1. 点击 Graph 左上角的 **`'Welcome'`** 打开欢迎屏幕
2. 勾选 **`'Focus Search On Selected Node'`**

### 功能

选中节点(如 `GameObject.GetName`)后按 `Spacebar` → 自动**跳到 Quick Search 第二部分**:
- 即只显示**相同类的其他方法**(快速浏览该类的所有方法)

**最佳场景**:
- 已经写了一个 `GetName` 节点,想继续添加 `SetName` 等同类的其他方法
- 浏览某类的完整 API

---

## 5. Search on Noodle Drop(Noodle 拖放搜索)

> **默认关闭**,需手动启用。

### 启用步骤

1. 点击 Graph 左上角的 **`'Welcome'`** 打开欢迎屏幕
2. 勾选 **`'Search on Noodle Drop'`**

### 功能

从任何端口**拖出一条 Noodle** → 拖到**空白处松开** → 弹出搜索框:
- 列出**所有能连接到该端口的节点**
- **同时搜索可以连接到这个端口的 Variables**

**方向支持**:
- ✅ 正向搜索(从输出端口拖出)
- ✅ 反向搜索(从输入端口拖出)

**最佳场景**:
- 想要查找"我应该往这个端口接什么"
- 减少对 API 签名的记忆负担

---

## 5 种搜索方式对比

| 方式 | 快捷键 | 速度 | 适用场景 | 启用状态 |
|------|--------|------|---------|---------|
| **Quick Search** | `Space` | ⚡ 最快 | 知道类名,找方法 | 默认 |
| **Full Search** | `Tab` | 慢 | 不知道类名,反向找 | 默认 |
| **Search Bar** | `Ctrl + F` | 快 | 在 Graph 内搜索 | 默认 |
| **Focused Search** | `Space`(选中节点后) | 快 | 查找同类其他方法 | 需启用 |
| **Search on Noodle Drop** | 拖动 Noodle | 快 | 查找能连接什么 | 需启用 |

---

## 实用技巧

### 搜索语法建议

| 想要找... | 推荐搜索 |
|----------|---------|
| 类的所有方法 | `classname.` (如 `transform.`) |
| 特定方法 | `classname.methodname` (如 `gameobject.setactive`) |
| 类型转换 | `cast`, `convert` |
| 流程控制 | `branch`, `loop`, `for`, `while` |
| 网络 | `networking`, `owner`, `sync` |
| 事件 | `event`, `onplayer` |

### 【推断】常见问题

| 问题 | 解决 |
|------|------|
| 找不到某个 API | 检查是否在白名单中(参见 `../../api/exposed-types.md` 与 `../../api/not-exposed.md`) |
| 搜索结果太多 | 用 `classname.methodname` 精确限定 |
| 不知道从哪个类找 | 用 Full Search 配合方法名 |

---

## 相关知识库

- [`index.md`](./index.md) — Udon Node Graph 主页(快捷键汇总)
- [`event-nodes.md`](./event-nodes.md) — Event 节点
- [`graph-elements.md`](./graph-elements.md) — Graph 元素
- [`special-nodes.md`](./special-nodes.md) — 特殊节点
- [`type-nodes.md`](./type-nodes.md) — 类型引用节点
- `../../api/exposed-types.md` — 已暴露类型详细清单
- `../../api/not-exposed.md` — 未暴露 API 黑名单
