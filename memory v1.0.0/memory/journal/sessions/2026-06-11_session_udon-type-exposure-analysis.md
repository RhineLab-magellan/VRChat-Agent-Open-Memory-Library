# Session: Udon Type Exposure Tree 分析与知识库建设

> Date: 2026-06-11
> Duration: ~2 hours
> Agent: UdonSharpAgent

---

## 任务目标

基于用户提供的 Udon Type Exposure Tree (SDK 3.10.3) 完善 UdonSharp API 支持情况知识库。

---

## 完成的工作

### 1. 数据解析
- **源文件**: `参考文献/UdonTypeExposure.txt` (1.2MB, 17442 行)
- **解析脚本**: `参考文献/generate_exposed_types.py`
- **发现**: 1387 个类型，1067 个有暴露成员，9579 个暴露 API

### 2. 新建知识库文件

| 文件 | 说明 |
|------|------|
| `memory/api/udon-type-exposure.md` | Udon Type Exposure Tree 索引 |
| `memory/api/exposed-types.md` | 已暴露类型详细清单 (自动生成) |
| `memory/api/not-exposed.md` | 未暴露 API 黑名单 |
| `memory/api/api-checker.md` | API 检查器/代码模式 |

### 3. 更新索引文件
- `memory/index.md` — 添加 API 目录路由
- `memory/FACT.md` — 添加 API 文件到知识库结构
- `memory/_always-load.md` — 添加 API 暴露检查自检项

### 4. 解析器修复
- **问题**: 命名空间中的 `<namespace>` 占位符导致类型名解析错误
- **解决**: 过滤 `current_ns` 中的 `<namespace>` 占位符
- **结果**: GameObject 等类型正确解析为 `Playables.GameObject`

---

## 关键发现

### 暴露统计
- 总类型数：1387
- 有暴露成员的类型：1067 (76.9%)
- 暴露成员总数：9579
- 未暴露成员总数：6323

### 命名空间分布
- `Playables`: 542 类型 (UnityEngine 核心)
- `Diagnostics`: 62 类型 (System)
- `UI`: 108 类型
- `Platform`: 36 类型 (VRC 平台 API)
- `Data`: 13 类型 (VRC 数据容器)

### 重要限制
1. **List<T>**: 只有特定类型可用 (ConstraintSource, KeyValuePair)
2. **Dictionary<K,V>**: 完全不可用 → 使用 DataDictionary
3. **构造函数**: 大部分 NOT EXPOSED
4. **禁止**: 反射、线程、异步、协程

---

## 新建 Journal 目录

应用户要求，创建 `memory/journal/` 目录用于非知识类记忆：
- `sessions/` — 会话记录 (30天清理)
- `reviews/` — 审查记录 (60天清理)
- `issues/` — 问题追踪 (关闭后7天清理)
- `drafts/` — 临时草稿 (7天清理)

---

## 待办/后续

- [ ] 用户可能会提供代码文件进行 API 检查
- [ ] 如有新 SDK 版本，更新暴露树
- [ ] 定期清理 Journal 目录