---
title: "Persistent Pen(持久化画笔)"
category: world
subcategory: examples
knowledge_level: applied
status: active
source: "https://creators.vrchat.com/worlds/examples/persistence/persistent-pen/"
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - world
  - persistence
  - udonsharp
aliases:
  - "Persistent Pen(持久化画笔)"
  - persistent-pen
related:
  - health-bar.md
  - leaderboard.md
  - position-sync.md
  - post-processing-settings.md
  - simple-rpg.md
---
# Persistent Pen(持久化画笔)


## 数据层选择

| 类型 | **PlayerObject** |
|------|------------------|
| 关键组件 | `VRCPlayerObject` + `UdonBehaviour` + `VRCEnablePersistence` |

## 概述

允许玩家使用画笔绘制最多 **20 条彩色线条**。线条对所有玩家同步。
橡皮擦可高亮和删除本地玩家绘制的线条。

## 使用方法

### 客户端测试
1. 拾取画笔,点击 "Use"(不移动)切换可用颜色
2. 长按 "Use" 并移动画笔在 3D 空间中绘制线条
3. 松开 "Use" 完成线条
4. 放下画笔,拾取橡皮擦,将其插入你的任何线条中
5. ⚠️ **已知问题**:在 ClientSim 中不会高亮线条 —— 仅在 VRChat Client 中有效
6. 按 "Use" 删除选中的线条 —— 这会将其添加回你的 20 条线集合
7. 停止场景然后重新启动以查看线条被恢复

## 技术分解

### SimplePenSystem 组件
`SimplePenSystem` 上有 `VRCPlayerObject` 组件,指示 VRChat **自动为世界中的每个玩家生成画笔系统副本**,并在玩家离开时移除。
`VRCEnablePersistence` 确保笔系统的所有同步属性(如线条的位置、点数和颜色)自动保存和加载。

### Udon 程序详情
此体验由两个程序提供支持 —— **Pen 一个 + 每条 Line 一个**。

#### Udon Pen
在场景中的 `SimplePenSystem/Pen` 下查看 `Udon Pen` 脚本。
- 更改用作 `Palette Color` 的 gradient 以交换可用颜色

#### Lines
在 `SimplePenSystem/Lines` 下找到画笔使用的线条。
- 可以对每条线进行更改,如设置不同的宽度或材质
- 如果想要每支笔有更多线条可用,只需复制一些现有线条即可!无需其他更改

## 数据流

```text
玩家持笔 → 长按 Use 移动 → 线条点累积
    ↓
[UdonSynced] linePoints 同步(在 PlayerObject 上)
    ↓
VRCEnablePersistence 自动持久化
    ↓
玩家离开 → 玩家重新加入 → 线条被恢复
    ↓
每个玩家的 20 条线独立保存(每个玩家一个 PlayerObject 副本)
```

## 限制

- **100 KB/player/world**(PlayerObject 配额)
- 20 条线 × 每条 N 个点 × Vector3 坐标
  - 单条线 ~50 个点 = ~600 bytes(float × 3)
  - 20 条线总计 ~12 KB
  - 远未触及上限
- ⚠️ 旧版限制 20 条线,roadmap 计划支持无限线条

## Roadmap(未来改进)

- Refactor the prefab to allow infinite lines
- Add a color picker where you hold a button to show a palette, then move to the color you want to use
- Respawn the pen whenever it's more than X units away from you

## Changelog

- 初始版本

## 验证清单

✅ 数据层:PlayerObject
✅ 关键组件:VRCPlayerObject + UdonBehaviour + VRCEnablePersistence
✅ 引用 100 KB 限制
✅ 容量估算(20 条线 ~12 KB)
✅ Key 命名空间前缀建议(隐含)

## Key 命名空间建议

由于线条数据是 PlayerObject 的 `[UdonSynced]` 字段,Key 命名空间概念不直接适用。
但应避免与其他示例的 PlayerData Key 冲突:

```text
# 如果混用 PlayerData(例如保存笔刷颜色偏好)
推荐前缀: PenSystem-
示例:
- PenSystem-Color-Preference
- PenSystem-MaxLines
```
