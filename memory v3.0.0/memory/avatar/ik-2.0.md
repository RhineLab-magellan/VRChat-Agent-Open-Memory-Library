---
title: IK 2.0 Features and Options — IK 2.0 完整特性
category: avatar

knowledge_level: applied
status: active

tags:
  - avatar
  - ik
  - tracking
  - fbt
  - launch-options

aliases:
  - "IK 2.0"
  - "IK2.0"
  - "新 IK 系统"
  - "Avatar Measurement"
  - "Lock Types"

related:
  - "avatar/full-body-tracking.md"
  - "world/udon/players/player-positions.md"
  - "platform/cross-platform-content.md"

source: https://docs.vrchat.com/docs/ik-20-features-and-options
source_type: community
version: 1.0
last_review: 2026-06-30
confidence: High
---

# IK 2.0 Features and Options — IK 2.0 完整特性

> 来源: VRChat 官方文档 - IK 2.0 Features and Options
> 抓取日期: 2026-06-30
> 状态: ✅ FACT (官方文档)
> **关键 Insight**: IK 2.0 是 VRChat 追踪系统的**完整重做**,改善 FBT **和 3 点追踪**。

---

## 1. 概述

**IK 2.0** 是 VRChat 追踪系统的**完整重做**,包括:

- ✅ 支持更多追踪点
- ✅ 校准保存
- ✅ 新 IK 设置
- ✅ 新启动参数
- ✅ Lock Types(锁定类型)

**适用范围**: 改善 FBT **和** 3 点追踪用户

**版本**: 2022.2.1 引入

---

## 2. IK Legacy / IK 2.0 切换

### 2.1 切换按钮

- 切换旧 Legacy IK vs 新 IK 2.0 行为
- **仅影响 IK avatar motion**
- 新追踪器校准检测/保存方案**不受影响**

### 2.2 不受切换影响的行为

- 新行为"忽略远距离追踪器"不受 toggle 影响
- `--calibration-range="0.6"` 启动参数行为不受 toggle 影响

### 2.3 Legacy 副作用

- 校准保存可能也工作于 Legacy 模式
- **未来不打算**为 Legacy 添加功能或维护
- ⚠️ **未来某时点可能移除 Legacy 切换**

---

## 3. Avatar Measurement(Avatar 测量)

### 3.1 两种模式

| 模式 | 描述 |
|------|------|
| **Arm Span(手臂展开)** | 旧版默认,手臂展开测量 |
| **Height(身高)** | 新增,身高测量 |

### 3.2 切换方式

- Settings 菜单 → Avatar Measurement 选项
- 切换测试,选最合适的

### 3.3 经验建议

> In our testing, measure-by-height mode tended to work better for full-body tracking.

**FBT 用户推荐用身高模式**

---

## 4. Lock Types(锁定类型)

定义**脊椎如何锁定**到 tracker 位置。

### 4.1 三种 Lock Type

| 类型 | 行为 | Chest Tracker 行为 |
|------|------|-------------------|
| **Lock Hip** | 严格髋部追踪,允许头部漂移(避免奇怪脊椎角度) | rotation-only |
| **Lock Head** | 严格头部/视角追踪,允许髋部漂移(避免奇怪脊椎角度) | rotation-only |
| **Lock Both** | 头部和髋部都严格追踪,可能产生奇怪脊椎/脖子角度 | rotation + position |

### 4.2 选择建议

- **Lock Hip**: 通常自然感好(头部跟随身体)
- **Lock Head**: 视角稳定(适合需要稳定视角的应用)
- **Lock Both**: 严格控制(可能产生奇怪姿态)

---

## 5. Locomotion Animation 切换

### 5.1 适用条件

- ⚠️ **仅 FBT + IK 2.0 模式显示**(Legacy IK 不显示)
- 切换可禁用 Locomotion Animations
- 同时禁用 Base layer 蹲伏/趴下动画(FBT 中常见问题)

### 5.2 行为对比

| 状态 | 行为 |
|------|------|
| **关闭(默认)** | 静态站立姿势(FBT 友好) |
| **开启** | 使用现有 Base layer(未修改) |

### 5.3 与 Animator 交互

> if the avatar's animator also disables FBT locomotion, it will remain that way regardless of this toggle.

- 如果 avatar Animator 自身禁用了 FBT locomotion → 无论此 toggle 如何,保持禁用
- Animator 优先级高于本 toggle

---

## 6. 新启动参数

### 6.1 `--custom-arm-ratio="0.4537"`

- 调整 arm-span 模式下 avatar 缩放比例
- 默认 `0.4537`
- 较小值(~`0.415`)可能改善 fit

### 6.2 `--disable-shoulder-tracking`

- 避免某些 IMU-only 手臂 tracker 问题
- 用 IMU-only tracker 的用户推荐

### 6.3 `--enable-ik-debug-logging`

- 在 log 中添加额外 IK 输出
- 报告 IK bug 时使用

### 6.4 `--calibration-range="0.6"`

- 校准时从预测支持绑定点的搜索距离(米)
- 默认 `0.6` 米(60cm 球体)
- 适用于: 脚、大腿、髋、上臂、胸 tracker

### 6.5 `--freeze-tracking-on-disconnect`

- 启用后,tracker 断连时**冻结**在原地
- 重新校准可移除冻结 tracker
- 如果所有 tracker 都断连导致 Calibrate 不可见 → 切换 Avatar Measurement 选项也可解冻

---

## 7. 与 Legacy 的差异

| 维度 | Legacy IK | IK 2.0 |
|------|-----------|--------|
| 校准 | 不保存 | **保存** |
| 追踪点 | 较少 | **更多** |
| Avatar Measurement | 仅 arm span | arm span **+ height** |
| Lock Types | 无 | **Lock Hip/Head/Both** |
| Locomotion toggle | 无 | **有** |
| 启动参数 | 少 | **5 个新增** |
| 维护 | ⚠️ 未来移除 | ✅ 当前主线 |
| FBT 体验 | 良好 | **更好** |
| 3 点追踪 | 良好 | **更好** |

---

## 8. 工程实践

### 8.1 推荐配置

| 用户类型 | 推荐配置 |
|---------|---------|
| FBT 用户 | IK 2.0 + Lock Hip + Height Measurement |
| 3 点追踪 | IK 2.0 + Lock Head(视角稳定) |
| IMU 手臂 tracker | `--disable-shoulder-tracking` |
| 多人追踪环境 | `--calibration-range="0.8"`(稍大搜索) |

### 8.2 故障排查

| 问题 | 解决方案 |
|------|---------|
| 校准困难 | 调整 `--calibration-range` |
| IMU tracker 异常 | `--disable-shoulder-tracking` |
| 报告 bug | `--enable-ik-debug-logging` 后复现并附 log |
| 冻结 tracker | 重新校准 / 切换 Avatar Measurement |

### 8.3 World/Avatar 创作者

- World 中追踪玩家朝向用 `GetRotation` 而非 `AvatarRoot`(FBT 不旋转)
- Avatar 设计参考 `full-body-tracking.md` §Rigging 要求

---

## 9. 风险与陷阱

| 风险 | 等级 | 说明 |
|------|------|------|
| **Legacy 未来移除** | 🟡 中 | Legacy 用户需规划迁移到 IK 2.0 |
| **Lock Both 姿势异常** | 🟡 中 | 严格锁定可能产生奇怪脊椎角度 |
| **--custom-arm-ratio 影响 fit** | 🟡 中 | 默认值不是万能,可能需调整 |
| **冻结 tracker** | 🟡 中 | 断连冻结可能需手动解冻 |
| **IMU 手臂 tracker 兼容** | 🟢 低 | `--disable-shoulder-tracking` 解决 |

---

## 10. 相关文档

- `memory/avatar/full-body-tracking.md` — FBT 完整设置
- `memory/world/udon/players/player-positions.md` — FBT 与 AvatarRoot
- `memory/platform/cross-platform-content.md` — 跨平台

---

## 11. 文档元信息

- **源文档 URL**: https://docs.vrchat.com/docs/ik-20-features-and-options
- **官方版本**: 2022.2.1 引入(与 v2022.2.1 release notes 一致)
- **本地化时间**: 2026-06-30
- **知识等级**: Applied
- **可信度**: High(官方文档)
