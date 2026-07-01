---
title: "Modular Avatar (MA) 完整知识库"
category: avatar
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - avatar
  - animator
  - physbone
  - constraint
  - sync
  - modular-avatar
aliases:
  - "Modular Avatar (MA) 完整知识库"
  - modular-avatar
related:
  - modular-avatar-tutorials-detailed.md
  - ma-component-cards.md
  - ma2bt.md
  - avatar-modding-guide.md
  - lac-avatar-compressor.md
---
# Modular Avatar (MA) 完整知识库

> 来源: [官方文档](https://modular-avatar.nadena.dev/docs)
> 范围: 6 个教程 + 2 个官方 Samples + 全部 25+ 组件 + Reactive 系统 + 教学法分析 + Experimental Features (Resonite + Portable)

---

## 0. 速查表（玩家最常问的 5 个问题）

| 问题 | 解答 | 跳转 |
|------|------|------|
| 装上衣服不动？ | 检查 `Setup Outfit` 是否执行；骨骼名是否匹配 | [§6 教程 1](#六教程-1-配置简单服装) |
| 装上衣服破洞？ | 可能是 PhysBone 穿模 → 加 `PhysBone Blocker`；或开启 `Shape Changer` | [§6 教程 4](#六教程-4-高级开关) |
| 调体型时衣服不变形？ | 添加 `Blendshape Sync` 同步形态键 | [§6 教程 1](#六教程-1-配置简单服装) |
| 装上鞋子陷进地板？ | 添加 `Floor Adjuster` 调整垂直位置 | [§7 组件 5](#7-floor-adjuster) |
| 多个发型不能同时存在？ | 把发型做成可切换菜单 `Object Toggle` | [§6 教程 3](#六教程-3-简单对象开关) |
| MMD 跳舞世界表情不对？ | 99% 是 World 自己行为问题，不是你的 Avatar | [§14.3 场景 A](#场景-ammd-world-表情不对) |
| MMD Layer Control build 失败？ | 装错位置了——必须装到 layer 不是 state | [§14.3 场景 B](#场景-bmmd-layer-control-装错位置) |
| 小组件在 MMD 世界不工作了？ | 默认是 MA 在保护你，**这可能是对的** | [§14.3 场景 C](#场景-cmerge-animator-在-mmd-世界失效) |
| 怎么快速验证开关生效？ | 点 Inspector 的 `Default` 复选框即可预览（不用进 Play） | [教程 3 §验证步骤](#六教程-3-简单对象开关) |
| 衣服跟身体穿模怎么看穿模程度？ | Scene 视图 → Shaded → `Overdraw` 半透明视图 | [教程 5](#六教程-4-高级开关形态键联动) |
| 我做的 Prefab 跟别人组件参数冲突？ | MA Parameters 勾上 `Internal` 防止冲突 | [教程 6 §概念 A](#六教程-6-手动构建动画器为什么用) |
| 装上衣服没反应？ | 99% 是 `Apply On Play` 没勾；Avatar 根 → VRC Avatar Descriptor → Apply On Play | [§8.3](#83-nothing-is-getting-processed-at-all最高频问题) |
| 错误窗口打不开？ | Tools → Modular Avatar → Show Error Report | [§8.1](#81-错误窗口ma-的核心诊断工具) |
| 改完错误不消失？ | 重新 Build：进 Play 模式 / Tools → Manual Bake Avatar | [§8.4](#84-错误报告的更新机制进阶) |
| VCC 提示 Failed to add Repo？ | VCC 已知 bug，点 Cancel，确认 bd_ 仓库已勾选 | [§8.2](#82-安装问题failed-to-add-repo) |
| 想看一个 MA 小组件内部什么样？ | 拆 Samples 的 Fingerpen / Clap，学 Prefab 内部结构 | [§9.6 Samples 实战](#96-samples-实战案例fingerpen--clap-拆解) |
| 衣服换颜色/材质怎么切？ | 加 Material Swap 组件，配 Quick Swap 一键预览 | [§7.17](#717-material-setter--material-swap-) |
| 换衣服时衣服会"闪现"裸体？ | Object Toggle 自带 1 帧延迟保护（自动处理） | [§5.2 Reaction Timing](#52-reaction-timing重要) |
| 想删除衣服某部分（如袖子）保留其他？ | Mesh Cutter + By Mask Vertex Filter | [§7.18](#718-mesh-cutter-) |
| 衣服有顶点颜色导致头发变色？ | Remove Vertex Color 组件加到 Avatar root | [§7 组件分类](#组件分类) |
| 多个小组件的菜单混在一起？ | Menu Installer 可指定 Install To 子菜单 | [§7.9](#79-menu-installer-) |
| 想让某个道具"钉"在世界不动？ | World Fixed Object（只生成 1 个 constraint，多个不费性能） | [§7.20](#720-world-fixed-object--world-scale-object-) |
| 想让某个道具不随 Avatar 缩放？ | World Scale Object | [§7.20](#720-world-fixed-object--world-scale-object-) |
| 想让手指 collider 移到嘴里（模拟咬东西）？ | Global Collider + Manual Remap | [§7.19](#719-global-collider-) |
| 想让自己的 PhysBone 撞到别人的 PhysBone？ | Global Collider（⚠️ 6 个上限） | [§7.19](#719-global-collider-) |
| 跨 PC/Android 上传参数顺序对不上？ | Sync Parameter Sequence（⚠️ 与 VRCFury Parameter Compressor 冲突） | [§7.21](#721-sync-parameter-sequence-高级) |
| 第一人称看不到自己头发？ | Visible Head Accessory（不能挂在 PhysBone 链子级） | [§7.13](#713-visible-head-accessory-) |
| 想把 Avatar 整体比例调大？ | Move Independently + 配合 Scale Adjuster（non-uniform scale 必须用 Scale Adjuster） | [§7.15](#715-scale-adjuster-) |
| Reactive 组件"优先级"怎么决定？ | 层级顺序最低的赢（最后面的） | [§5.1](#51-通用规则) |
| Reactive 时序不对（动画延迟）？ | 官方明确警告：不要依赖精确 timing | [§5.2](#52-reaction-timing重要) |
| 菜单项参数名自动创建了但不想保存/同步？ | Menu Item 的自动参数创建，取消 Saved/Synced 复选框 | [§7.8](#78-menu-item-) |
| Blendshape Sync 链式同步（A→B→C）不工作？ | 官方不支持链式，只能 A→B 和 A→C | [§7.10](#710-blendshape-sync-) |
| MMD World 支持开关在哪？ | VRChat Settings 组件的 MMD World Support 复选框 | [§7.16 VRChat Settings](#716-mmd-layer-control-) |
| 多个 World Fixed Object 费性能吗？ | 不会，只生成 1 个 constraint（多个不额外费） | [§7.20](#720-world-fixed-object--world-scale-object-) |
| 想把一个 GameObject 完全替换 Avatar 上的另一个？ | Replace Object（⚠️ 一个只能被一个替换） | [§7.14](#714-replace-object-) |
| 动画路径 Relative vs Absolute 怎么选？ | Merge Animator 的 Path mode：Relative 相对当前，Absolute 绝对路径 | [§7.2](#72-merge-animator-) |
| Merge Motion 播放速度不对？ | Direct Blend Tree 会把所有动画对齐到同一时长，用 Merge Animator 替代 | [§7.2](#72-merge-animator-) |
| 想禁用 MA 的 Convert Constraints 自动转换？ | 删除 Avatar root 上的 Convert Constraints 组件 | [§7.22](#722-convert-constraints-) |
| Scale Adjuster 调整时子对象也动了？ | 取消勾选 "Adjust child positions" | [§7.15](#715-scale-adjuster-) |
| 想让某个菜单只在 VRChat 出现？ | Platform Filter 加 Include VRChat | [§7.12](#712-platform-filter-) |

> **配套详细教程**（每个教程的"官方原文 + 玩家视角操作 + 验证 + 易错点"）：
> [`memory/avatar/modular-avatar-tutorials-detailed.md`](./modular-avatar-tutorials-detailed.md)

---

## 0.5 General Behavior 概览

> 来源：[General Behavior](https://modular-avatar.nadena.dev/docs/general-behavior)

**定位**：官方文档"General Behavior"章节定位为 **MA 的"通用行为说明"**（"general information on the behavior of Modular Avatar"），属于**机制解释**而非**操作教程**——告诉玩家"MA 在特定场景下会自动做什么 / 为什么这么做"。

**当前包含的子页面**（截至文档版本）：

| 子页面 | 主题 | 关键概念 |
|--------|------|---------|
| [MMD World Workarounds](https://modular-avatar.nadena.dev/docs/general-behavior/mmd) | MMD World 自动行为与应对 | relay layers, padding layers, MMD Layer Control |

**与本知识库章节的对应关系**：

| 官方文档 | 本知识库 | 覆盖度 |
|---------|---------|--------|
| General Behavior 主页 | §0.5 本节 | ✅ |
| MMD World Workarounds | §7.16 (组件) + §9.2 (行为) + §15 (教学法) | ✅✅ 完整覆盖 |

**与操作教程的区别**：

| 维度 | Tutorials（教程） | General Behavior（行为） |
|------|----------------|------------------------|
| 视角 | "**我**要做 X" | "MA 会**自动**做 X" |
| 颗粒度 | 操作步骤 | 机制原理 |
| 触发阅读 | 遇到具体任务 | 遇到异常/疑问 |
| 教学意义 | "跟着做" | "理解为什么这样做有效" |

---

## 1. MA 是什么 / 解决什么问题

**一句话**: 把"拖一个 Prefab 到 Avatar 身上就完成换装"变成现实的工具。

| 痛点 | MA 解决方式 |
|------|-------------|
| 衣服要手动合并骨骼、动骨、菜单 | 拖入 → 右键 `Setup Outfit` → 完成 |
| 多个小组件参数冲突 | `MA Parameters` 自动重命名 |
| 衣服影响别的部位 | `Shape Changer` 自动隐藏被遮挡的身体 |
| 不同玩家的骨骼名不一样 | `Merge Armature` 智能匹配 |
| 装上衣服后表情/动画坏掉 | `Merge Animator` 自动修正动画路径 |

> **类比**: MA 就像 Unity 的"包管理器"——你下载的衣服/小组件都自带说明书,MA 这个包管理器帮你把所有说明书翻译一遍,正确地装到你的 Avatar 上。

---

## 2. 安装 (3 步)

```
1. ALCOM/VCC 添加仓库: https://vpm.nadena.dev/vpm.json
2. 项目中点击 Modular Avatar 的 + 
3. Apply → 装好了
```

> ⚠️ 预发布版请用 **ALCOM**（VCC 依赖解析有 bug）

---

## 3. 核心概念（5 分钟理解）

### 3.1 编译时 vs 运行时

| 阶段 | 何时 | 做了什么 |
|------|------|---------|
| **编辑模式** | 你在 Unity 里操作 | 摆放组件、配参数、调骨骼 |
| **编译时**（Build Time） | 进 Play 模式 / 上传 Avatar 时 | MA 把所有"说明书"翻译成最终 Avatar |
| **运行时**（Runtime） | 在 VRChat 里 | 跑编译后的 Avatar |

**重点**: MA 组件**不是运行时组件**，它们在编译时完成所有工作。

### 3.2 三个核心组件

| 组件 | 干什么 | 什么时候用 |
|------|--------|-----------|
| **Merge Armature** | 把衣服的骨骼"挂"到素体上 | 装衣服/头饰/尾巴等所有 Skinned Mesh 物件 |
| **Merge Animator** | 把小组件的动画合并到 Avatar 动画器 | 任何带 Animator 的小组件 |
| **MA Parameters** | 注册/重命名参数 | 任何用了 Animator 参数的小组件 |

> **剩下 20+ 组件都是这 3 个的"快捷方式"或"附加功能"**

### 3.3 反应式组件（Reactive Components）

**核心思想**: 不写一行动画 = 让 GameObject **启用时**自动触发某些效果。

| 组件 | 启用时效果 |
|------|-----------|
| Object Toggle | 启用/禁用其他 GameObject |
| Shape Changer | 改形态键值（或直接删多边形） |
| Material Setter | 替换材质 |
| Material Swap | 批量替换材质 |
| Mesh Cutter | 删/隐藏多边形 |

**为什么会自动工作**？因为这些组件**响应**：
- 动画控制 GameObject 激活
- 其他 Object Toggle 联动
- 菜单选中状态

详见 [§5 Reactive 系统](#5-reactive-系统详解)

---

## 4. 教学法归纳：怎么教玩家

> 适用对象：默认玩家**没有/仅有少量 Unity + 动画器 + Avatars3 基础**

### 4.1 官方教程的 6 个隐含教学原则

| 原则 | 官方做法 | 我们教玩家时的应用 |
|------|---------|------------------|
| **截图说话** | 每一步 1-2 张图 | "看到 Inspector 出现 X 字段就对了" |
| **步骤颗粒度 = 1 步 1 动作** | 教程 1 共 4 步,教程 6 共 6 步 | 把"装衣服"拆成"拖入 → Setup → 隐藏原衣 → Play 看效果" |
| **明确预期结果** | 每步结尾"应该看到..." | "现在你应该看到...如果没看到,回去检查 X" |
| **给出失败模式** | 教程 4 用大段讲"可能没效果"的诊断 | "如果 Play 模式没动,99% 是 Y 原因" |
| **先 1 步做完 1 步** | 不假设你会后面才用到的 | "今天先做步骤 1-3,熟练了再做 4-6" |
| **用具体 Avatar / 服装举例** | Sailor Onepiece + Anon-chan | "用你自己的素体 + 衣服,先按教程走一遍" |

### 4.2 三种典型玩家问题 & 回答框架

| 玩家类型 | 典型提问 | 回答框架 |
|---------|---------|---------|
| **"我刚装上没反应"** | "衣服在场景里能看到,Play 模式不见了" | 检查 Merge Armature → 验证骨骼名 → 试 Manual Bake |
| **"我想加个开关"** | "我想让帽子能开能关" | 教 Object Toggle 教程（最简单） |
| **"衣服和身体穿模"** | "穿衣服后腰那里有缝" | Shape Changer + Blendshape Sync 联合方案 |

### 4.3 5 步问题诊断法（玩家自己也能用）

```
步骤 1: 看到问题 → 拍照/截图保存
步骤 2: 检查最简单原因
  ├─ 组件没添加？
  ├─ 拖的对象拖错了？
  └─ 没 Play 模式就期待效果？
步骤 3: 检查 Setup Outfit 是否成功
  └─ 看 Outfit 根上有没有 Merge Armature 组件
步骤 4: 检查骨骼名
  └─ 衣服的 Hips 名字包含素体的 Hips 名字吗？
步骤 5: 用 Manual Bake Avatar 看最终结果
  └─ 右键 Avatar → Modular Avatar → Manual bake avatar
```

### 4.4 不要这样教玩家

| ❌ 反例 | ✅ 正确 |
|---------|--------|
| "你装好了吗?现在点击 Play" | "你应该看到 X。**如果没看到**,回去检查 Y" |
| "这个组件用 NDMF 编译时会处理" | "你**不用理解**这个,Unity 帮你做了" |
| "写一个空对象" | "新建一个空 GameObject (右键 → Create Empty)" |
| "你应该知道 Animator 怎么用" | "**先确认**你打开过 Unity 的 Animator 窗口" |

### 4.5 高级玩家的分层教学

| 玩家水平 | 推荐起点 | 跳过 |
|---------|---------|------|
| 纯新手 | 教程 1 (简单服装) + 教程 3 (对象开关) | 跳过 NDMF 概念、跳过参数 |
| 入门 | + 教程 2 (复杂服装) + 教程 4 (高级开关) | 跳过手动动画 |
| 进阶 | + 教程 5 (编辑菜单) + 教程 6 (手动动画) | - |
| 高级创作者 | Component Reference 全集 + Distributing Prefabs | - |

### 4.6 MA 教程中可提取的"玩家友好"设计模式
> 基于官方 6 个教程原文精读，提炼 MA 文档中的**优秀设计模式**——这些是教玩家时可直接复用的技巧。

#### 模式 1：Default 复选框预览（**最重要的设计**）

**官方做法**：教程 3 中，点 Inspector 的 `MA Menu Item` 上的 `Default` 复选框，**立即**在 Scene 视图看到物件出现/消失。

**教学价值**：
- 玩家**不需要进 Play 模式**就能验证
- 减少"我做了但不知道对不对"的焦虑
- 教学时强调："**点 Default 复选框就能看到效果**"

**类比**：VSCode 改 CSS 实时预览、Dashboard 设置面板预览。

#### 模式 2：Overdraw 调试视图（**可视化诊断**）

**官方做法**：教程 5 中，教玩家用 Scene 视图 → Shaded → Overdraw 来**半透明看穿模**。

**教学价值**：
- 让玩家"看到"问题，而不是猜
- 比"截图+文字描述"直观 10 倍
- 教学时教"用眼睛看穿模"

**应用**：
- 调形态键时 → 用 Overdraw 验证
- 调 Collider 时 → 用 Overdraw 验证
- 任何"是否重叠"问题 → 用 Overdraw

#### 模式 3：组件顺序作为信息架构

**官方做法**：教程 6 中，调整组件顺序——把 `Menu Installer` 放在最上面（玩家最常改的放最前）。

**教学价值**：
- 告诉玩家"组件顺序是 UI 优先级"
- 创作者应该把用户最可能改的放最前

#### 模式 4：自动机制降低门槛

**官方做法**：教程 1 中，`Setup Outfit` 自动找 Armature、自动加 Merge Armature、自动处理 A-Pose/T-Pose。

**教学价值**：
- "你**不需要理解**这个，MA 帮你做了"
- 教玩家时不要讲"为什么能自动"，只讲"它会自动"
- 把高级概念（骨骼合并、A-Pose 转换）封装起来

#### 模式 5：诚实告知限制 + 给出替代方案

**官方做法**：教程 5 的 Warning 框："形态键联动效果编辑器无法预览 → 用 Avatar 3.0 Emulator 或 Gesture Manager 在 Play 模式测试"。

**教学价值**：
- 不隐藏限制
- 给出绕过限制的方法
- 教学时保持这种诚实

### 4.7 教程衔接路径
```
完全新手路径（90% 玩家）:
教程 1 (换装) → 教程 3 (开关) → 完成 ✅

遇到穿模:
教程 1 → 教程 3 → 教程 5 (形态键联动)

有布娃娃衣服:
教程 1 → 教程 2 (布料)

想编辑菜单 / 做小组件:
教程 1 → 教程 3 → 教程 4 (菜单) → 教程 6 (手动) [可选]
```

> **核心建议**：90% 玩家**只需要教程 1 + 教程 3**。其他都是遇到具体问题再来学。

### 4.8 MA 改模教学的 7 条核心原则
> 来源：基于官方教程、Samples、Distributing Prefabs 三个章节综合提炼
> **适用对象**：教玩家 MA 改模的所有场景
> **核心思想**：官方教程面向"工程师给工程师"，我们补足"如何给新手讲明白"这层

#### 原则 1：Prefab-First（prefab 优先）

- **官方做法** [FACT]：Sample 与 Preset 都把配置封装成单个 prefab，玩家拖入即用
- **我们的应用**：教学 demo **必须**以"双击 prefab→生效"为最小单位，禁止散件讲
- **反例**：截图罗列组件 Inspector 字段，让学员手动拼装 → 学习曲线崩溃
- **教学话术**："先别看里面有什么——你**先拖进去看效果**。看完效果我们再拆"

#### 原则 2：抽象层对学员透明

- **官方做法** [FACT]：Setup Outfit 自动识别 Hips、T/A-pose、骨骼轴向，隐藏 90% 机械工作
- **我们的应用**：演示时分两层——"这是什么"（Merge Armature 卡片）+ "它替你做了什么"（内部流程 1 句话）
- **反例**：教 Bone Proxy 时塞 50 行矩阵/四元数公式 → 学员被劝退
- **教学话术**："你**不需要理解**它怎么算的，你只需要知道它会**自动帮你做**"

#### 原则 3：兼容降级路径必须明示

- **官方做法** [FACT]：Compatible（无 MA 组件）与 Preset（含 MA 组件）两级支持
- **我们的应用**：讲每个组件时问一句"如果不装 MA 会怎样？"——让学员理解 fallback
- **反例**：默认学员必装 MA，不解释 Bone Proxy vs Merge Armature 选择标准
- **教学话术**："这个组件依赖 MA。没装 MA 的话用 Bone Proxy 替代"

#### 原则 4：命名约定 > 自动匹配

- **官方做法** [FACT]：文档明确说"exact name matching 比 fuzzy matching 可靠"
- **我们的应用**：第一节课就定下**命名规范**（Hips 包含底模名、Armature 父级等）
- **反例**：让学员随便命名，靠模糊匹配救场 → 多次安装后参数爆炸
- **教学话术**："Hips 骨骼**必须**包含你素体的 Hips 名——**从一开始**就这么做"

#### 原则 5：危险操作先警告再教学

- **官方做法** [FACT]："Things to avoid" 单独成节——PhysBone on humanoid bones、完全同名 Armature、错误 Pose 转换
- **我们的应用**：每个组件教学**前置**"3 个常见踩坑"清单，用真截图标记红框
- **反例**：只讲 happy path，学员到 Discord 求助才发现踩坑 → 信任崩塌
- **教学话术**："在教你组件之前先说**3 个会坑死你**的点"

#### 原则 6：验证手段三件套

- **官方做法** [FACT]：Edit mode sync / Play mode / Manual Bake 三种调试法
- **我们的应用**：每章节配"**自检 3 问**"——旋转骨骼是否跟随？进 play mode 看效果？Manual Bake 克隆是否正常？
- **反例**：只教点击 Setup Outfit 后无验证步骤，学员盲信
- **教学话术**："做完一步**自己检查一下**——教你怎么检查"

#### 原则 7：版本与品牌边界提前划清

- **官方做法** [FACT]：SemVer 明确（Minor 反向不可用）、logo 决定权在 bd_/pumo、不允许暗示背书
- **我们的应用**：教学发布物标注"基于 MA 1.x.x"；教学素材**不放** MA logo
- **反例**：教学视频挂 MA logo 做封面 → 学员误以为官方教程，且违反品牌准则
- **教学话术**："基于 MA 1.x.x。**不要**在作品页面挂 MA logo——你只是**用**它，不是**做**它"

#### 原则 8（补充）：MA 的"三段式"教学法

基于 Samples 章节提取的元学习方法论：

| 阶段 | 时间 | 目标 | 玩家心理 |
|------|------|------|---------|
| **玩** | 5 分钟 | 拖一个 prefab 看效果 | "哦,这么简单" |
| **拆** | 10 分钟 | 展开 prefab 看内部组件 | "哦,原来是这样" |
| **造** | 30+ 分钟 | 用教程方法自己做一个 | "哦,我也能造" |

**关键洞察**：**不要跳过"玩"直接教"造"**——90% 新手看到概念就放弃了。

---

## 5. Reactive 系统详解

### 5.1 通用规则

**Active 判定**（同时满足）：
1. GameObject 自身 + 所有父级都在 Hierarchy 中 active
2. 如果在 Menu Item 同级或子级，该菜单项**被选中**（注意：只算**第一层**父菜单，子菜单被忽略）

**优先级**：多个 Reactive 组件冲突时，**Hierarchy 中最下方的**胜出

**Invert 条件**：勾选后，组件在"条件不满足"时生效

### 5.2 Reaction Timing（重要！）

> ⚠️ 完整时序细节可能在未来版本变化,但**核心特性**是稳定的。

**1 帧延迟** = 防止"闪烁"问题的核心机制。

**时序**（A→B→C 链式，A 关掉时）：

| 帧 | 发生什么 |
|----|---------|
| 1 | 不发生任何事（A 的 disable 被延迟）|
| 2 | A 真正 disable（B 的 disable 被延迟）|
| 3 | B 和 C 同时 disable |

**为什么会这样**？因为"关掉外套"必须等"内衣先显形"再发生，否则中间会有 1 帧"裸体"。

### 5.3 Reaction Debugger（高级调试工具）

**用途**：不用真的去 VRChat 就能模拟各种开关状态。

**打开方式**：
- 右键 GameObject → Modular Avatar → Show Reaction Debugger
- 或点击 Reactive 组件的"Open reaction debugger"按钮

**两个区域**：
- **Object state** — 强制这个对象 active/inactive、菜单选中/取消
- **Reaction section** — 列出所有影响这个对象的 Reactive 组件及其触发条件

> **教学要点**：教玩家"在 Play 模式前先用 Debugger 验证一下,省得每次都要进 Play 模式"。

---

## 6. 六教程详解

### 六教程 1: 配置简单服装

**目标**：把 Capettiya 的 Sailor Onepiece 装到 Anon-chan 素体上。

**步骤**：

1. **拖衣服到 Avatar**
   - 把衣服 Prefab 拖到场景里 Avatar 的子级
   - ⚠️ 不要拆 Prefab

2. **右键 Setup Outfit**
   - 在 Hierarchy 右键衣服根对象
   - 选 `Modular Avatar → Setup Outfit`
   - MA 自动添加 `Merge Armature` 组件

3. **隐藏原衣服（可选）**
   - 如果 Avatar 自带衣服,关闭它的可见性
   - 教程里关闭了 `SailorOnepiece_Anon_PB`

4. **Play 模式验证**
   - 进 Play 模式,衣服应该跟着素体动

**发生了什么**（教学用）：
```
衣服 Hierarchy:
OutfitName (GameObject) ← MA 加了 Merge Armature
  └─ Armature (GameObject)
      └─ Hips (Bone, 名字要包含素体 Hips 名字)
          └─ Spine
              └─ ...
```

**Merge Armature 智能行为**：
- 同名骨骼 → 共享素体骨骼（不重复创建）
- 衣服独有骨骼 → 移到对应素体骨骼下
- 含组件的骨骼 → 保留为单独对象

**形态键同步（Blendshape Sync）**：
- 装好衣服后,在衣服的 Mesh Renderer 上加 `Blendshape Sync`
- 点 `+` → 选素体的形态键（胸部大小、身体形状等）
- 自动同步,改素体 → 衣服跟着变

> **教学要点**：这是 90% 玩家需要的"换装"流程。**第一次教就讲这个**。

---

### 六教程 2: 配置复杂（布料）服装

**目标**：处理 Cloth 材质、多个 collider、特殊形态键。

**完整流程**（以 Dress Lumi 为例）：

```
1. 拖入 → Setup Outfit（基础流程）
2. 处理 Colliders:
   - 选中所有 Hips_Collider 对象
   - 一次性加 MA Bone Proxy
   - Target 拖入素体的 Hips
   - Attachment Mode 自动变为 "As child; keep position"
3. 对其他 Collider 重复
4. Blendshape Sync 处理 Skirt 和 Tops
```

**关键组件**：
- **MA Bone Proxy**：把对象挂到**素体的特定骨骼**上（保持世界坐标）
- **Blendshape Sync**：同步身体形状相关的形态键

**高级选项（教程不强制）**：
- 可加 `Merge Animator` 自动化：胸部大形态键=100、bra_off=100、关闭 Cloth
- ⚠️ **警告**：这会和 Outfit Changer 冲突，谨慎使用

> **教学要点**：新手阶段**通常不需要这个**。遇到 Cloth 破洞才回来学。

---

### 六教程 3: 简单对象开关

**目标**：用菜单开关一个物件（比如开关 Anon-chan 的连帽衫）。

**最快流程（推荐）**：

```
1. 右键 Avatar → Modular Avatar → Create Toggle
2. 在新创建的 GameObject 上：
   - 改名（如 "Hoodie"）
   - Object Toggle 组件点 + → 拖入要开关的对象
   - 是否勾选 = 选中时"启用"还是"禁用"
3. 测试：
   - Menu Item 上的 "Default" 勾选 → 应该看到物件变化
```

**这个方法生成的组件**：
- `MA Menu Item`：菜单项
- `MA Menu Installer`：把菜单项装到主菜单
- `MA Object Toggle`：实际的开关逻辑

> **教学要点**：**这是 100% 玩家第一个要学的功能**。**别教手动方案**。

---

### 六教程 4: 高级开关（形态键联动）

**目标**：开关鞋子时**同时**缩掉脚部形态键（避免穿模）。

**背景**：很多 Avatar 有"shrink blendshapes"用于在穿衣服时缩身体部位。手动管理很烦。

**步骤**：

```
1. 先观察问题：
   - 关闭鞋子后，看到袜子和脚之间有缝
   - 因为两层都被 shrink 形态键缩了
2. 找到两个 shrink 形态键：
   - Anon_body 上的某个形态键
   - Socks 上的某个形态键
   - 全部重置为 0
3. 在鞋子 GameObject 上加 Shape Changer：
   - 缩底层形态键
   - 模式选 Delete（性能更好，删多边形）
4. 在袜子 GameObject 上加 Shape Changer（同样）
5. 用 Overdraw 调试模式（Scene 视图调试）验证
6. 创建菜单子菜单，把开关项放进去
```

**关键教学点**：

| 概念 | 简单解释 |
|------|---------|
| **Shape Changer Delete 模式** | 直接删多边形，省 GPU。**没有动画时自动用这个** |
| **Shape Changer Set 模式** | 把形态键设为指定值。**有动画时用这个** |
| **Overdraw 调试** | Scene 视图 → 调试叠加 → Overdraw，半透明查看穿模 |

**已知限制**（提前告诉玩家）：
> ⚠️ 形态键联动效果**在编辑器无法预览**。要用 Avatar 3.0 Emulator 或 Gesture Manager 在 Play 模式测试。

> **教学要点**：这是中高级功能。**新手可以跳过**，等遇到穿模再学。

---

### 六教程 5: 编辑菜单

**目标**：不用手动创建 VRC Expressions Menu 资产，而是用 Hierarchy 对象管理。

**两种场景**：

**A. 转换现有 Avatar 菜单**：
```
1. 右键 Avatar → Modular Avatar → Extract menu
2. 出现 Avatar Menu 对象（包含顶级菜单项）
3. 想编辑子菜单 → 点 "extract to objects" 按钮
4. 用拖拽重新组织菜单结构
5. 加新项 → 点 "Add menu item"
```

**B. 在可重用资源上加菜单**：
```
1. 创建子菜单对象
2. 同一 GameObject 上加：
   - MA Menu Installer（安装器）
   - MA Menu Item（菜单项，Type = Sub Menu）
3. Submenu Source 设为 Children
4. 子级加 MA Menu Item 作为子项
```

**参数搜索技巧**：
- 参数名旁有个下拉箭头
- 点它会搜索所有父级 MA Parameters 组件
- **不用手写参数名**

**支持不分组**（Menu Group）：
- `MA Menu Group` + `MA Menu Installer` 在同一对象
- 把多个 Menu Item 装到目标菜单**而不创建子菜单**
- 这是 Extract Menu 系统的内部实现方式

> **教学要点**：菜单编辑的"对象模式"比 VRC 资产方式**直观 10 倍**。**优先教这个**。

---

### 六教程 6: 手动构建动画器（为什么用？）

**目标**：用传统 Animator 方式做开关（**教学用，实际应该用 Object Toggle**）。

**官方原话**："You can also do this by building an animator manually, **but why would you?**"

**官方 6 步**（**注意**：标题写"6 步"但表格列了 9 行,实际官方分 Step 1-5 + Setup 6 + Finishing Up）：

| 步 | 动作 | 关键点 |
|---|------|--------|
| **Step 1** | 创建 GameObjects：`ToggleDemo/HandRef/Cube` | ⚠️ **删 Cube 的 Box Collider**（否则影响手部追踪） |
| **Step 2** | 把 Cube 挂到手上：HandRef 加 `MA Bone Proxy`，Target = 右手骨头，Attachment Mode = "As child; at root" | Bone Proxy 不需要放顶层 |
| **Step 3** | 创建 Animator Controller + 2 个动画（CubeOff, CubeOn）+ Any State 转换 | bool 参数 `Cube`，Transition Duration = 0，Can Transition to Self = off |
| **Step 4** | 加 `MA Merge Animator` + **也加 Animator 组件** | 勾上 `delete attached animator` 和 `match avatar write defaults`；Animator 只是为了让 Unity 允许录制 |
| **Step 5** | 加 `MA Parameters`（点 Show Prefab Developer Options）→ 加 Cube 参数 → Sync Mode = Bool，**Internal = true** | Internal 防止参数冲突 |
| **Setup 6** | 创建 Expressions Menu 资产 + 加 `MA Menu Installer` 引用 Menu | VRC 资产方式 |
| **Finishing Up** | 调整组件顺序（Menu Installer 放最上面） → 拖到 Project 做成 Prefab | 拖到任何 Avatar 上 → 都能用 |

**三个关键概念（必学）**：

#### 概念 A：Internal Checkbox（**最常被忽略**）

| 选项 | 行为 | 何时用 |
|------|------|--------|
| **Internal ✅** | MA 自动避免参数名冲突 | **默认推荐**，99% 情况用 |
| **Internal ❌** | 用户可手动改名，可能冲突 | 多个小组件需要共享同一参数时 |

> **官方原话**："If you set the internal checkbox, modular avatar will ensure that your `Cube` parameter doesn't interfere with anything else on the avatar using the same parameter name."

#### 概念 B：MA Parameters 位置约束（**易错**）

> **官方原话**："Make sure that `MA Parameters` is on either the same object, or a parent of all your `Merge Animator`s and `Menu Installers`!"

**翻译**：`MA Parameters` 必须放在所有 `Merge Animator` 和 `Menu Installer` 的**同一对象或父级**。

#### 概念 C："也加 Animator 组件" 的真实目的

> **官方原话**："Adding an Animator here is also optional; we're just using it so that Unity allows us to record animations. By checking the `delete attached animator` box, Modular Avatar will delete the `Animator` component at build time."

**翻译**：Animator 组件只是为了让 Unity 允许录制动画（Unity 的限制），**build time 会被自动删除**。

**教程 6 vs 教程 3 对比**：

| 维度 | 教程 3 (Object Toggle) | 教程 6 (Manual Animator) |
|------|----------------------|-------------------------|
| 难度 | ⭐ 新手友好 | ⭐⭐⭐ 需要 Animator 基础 |
| 步骤 | 5 步 | 6 步（实际更繁琐） |
| 适用 | 所有玩家 | 仅创作者 |
| 维护 | 加新开关 = 加新 GameObject | 加新开关 = 改 Animator + 加新 Controller |
| **官方建议** | **默认用这个** | "why would you?" |

> **教学要点**：**90% 玩家永远不应该学这个教程**。但创作者必须理解，因为某些复杂场景（复杂多状态机、多参数联动）必须用 Animator。

> **配套详细教程**（包含完整玩家操作分解、验证步骤、易错点）：
> [`memory/avatar/modular-avatar-tutorials-detailed.md` 教程 6](./modular-avatar-tutorials-detailed.md#六教程-6-手动构建动画器为什么用)

---

## 7. 全部组件速查（25+ 个）

### 组件分类

| 类别 | 组件 | 何时用 | 难度 |
|------|------|--------|------|
| **核心合并** | Merge Armature | 装衣服/头饰等 | ⭐ |
| | Merge Animator | 合并 Animator Controller | ⭐⭐ |
| | Merge Motion (Blend Tree) | 合并 Blend Tree / 持续动画 | ⭐⭐ |
| | Bone Proxy | 把对象挂到指定骨头 | ⭐ |
| **反应式** | Object Toggle | 开关对象 | ⭐ |
| | Shape Changer | 形态键删除/缩放 | ⭐⭐ |
| | Material Setter | 替换材质 | ⭐ |
| | Material Swap | 批量替换材质 | ⭐ |
| | Mesh Cutter | 删除/隐藏多边形 | ⭐⭐ |
| **菜单系统** | Menu Item | 定义菜单项 | ⭐ |
| | Menu Installer | 装到主菜单 | ⭐ |
| | Menu Group | 不分组多菜单项 | ⭐ |
| | Menu Install Target | 菜单安装目标 | ⭐⭐ |
| **参数** | MA Parameters | 注册/重命名参数 | ⭐⭐ |
| | Sync Parameter Sequence | 跨平台参数顺序同步 | ⭐⭐⭐ |
| | Rename Collision Tags | 重命名 Contact 标签 | ⭐⭐ |
| **服装专用** | Blendshape Sync | 同步形态键 | ⭐ |
| | PhysBone Blocker | 阻止父 PhysBone 影响子 | ⭐ |
| | Replace Object | 替换 Avatar 上的对象 | ⭐⭐ |
| | Mesh Settings | 网格设置 | ⭐⭐ |
| **Avatar 配置** | Floor Adjuster | 调垂直位置 | ⭐ |
| | Visible Head Accessory | 第一人称可见 | ⭐ |
| | Scale Adjuster | 单独缩放某骨骼 | ⭐⭐ |
| | Move Independently | 编辑模式独立移动 | ⭐ |
| **平台/通用** | Platform Filter | 平台过滤 | ⭐ |
| | Remove Vertex Color | 移除顶点色 | ⭐ |
| | Global Collider | 全局碰撞体 | ⭐⭐ |
| | World Fixed Object | 世界固定对象 | ⭐ |
| | World Scale Object | 世界缩放 | ⭐ |
| | Convert Constraints | 转换 Unity → VRC 约束 | ⭐ |
| | VRChat Settings | MMD World 支持开关 | ⭐ |
| | MMD Layer Control | 控制 MMD 层 | ⭐⭐ |

### 7 组件详解（重要者）

#### 7.1 Merge Armature ⭐⭐⭐（必学）

**用途**：把对象树合并到 Avatar 骨骼上（专为 Skinned Mesh 服装设计）。

**何时用**：
- ✅ 装衣服/头饰/尾巴
- ✅ 装任何 Skinned Mesh 配件
- ❌ 不用于"放个 Cube 在手上"（用 Bone Proxy）
- ❌ 不用于通用 Prefab（不同 Avatar 不能用）

**关键功能**：
- 更新 SkinnedMeshRenderer 引用
- 最小化生成的骨骼数量
- 复用现有骨骼

**配置方法**（3 步）：
```
1. 组件加到源层级根对象
2. 拖入 Avatar 对应骨骼到 Merge Target
3. Prefix/Suffix 通常自动设置
```

**位置锁定模式**：

| 模式 | 行为 | 何时用 |
|------|------|--------|
| Not locked | 编辑模式不跟随 | 几乎不用 |
| Base → Target (单向) | 素体动 → 衣服跟 | **默认**，日常用 |
| Base ↔ Target (双向) | 互相跟 | 高级场景（如动素体头发）|

**Setup Outfit 自动**：
- 自动找衣服的 Hips 骨骼（名字要包含素体 Hips 名字）
- A-Pose/T-Pose 转换（手臂位置不同时）
- 创建 Mesh Settings 组件

**已知陷阱**：
- ⚠️ 不要让 PhysBone 在素体骨骼上（如 Hips、Chest）— MA 会尝试删除，导致不可预测
- ⚠️ 避免和素体**完全相同**的骨骼名（会触发 Unity bug）

#### 7.2 Merge Animator ⭐⭐

**用途**：把小组件的 Animator 合并到 Avatar 指定层。

**关键功能**：
- 路径模式（Relative / Absolute）
- 层级优先级（控制合并顺序）
- 合并模式（Add / Replace）
- Write Defaults 匹配

**配置**：
```
1. 组件加到 Prefab 对象
2. Animator to merge 拖入 Animator Controller
3. Layer Type 选层（FX、Action 等）
4. (推荐) 勾上 "delete attached animator"
5. (推荐) 勾上 "match avatar write defaults"
```

**Write Defaults 匹配**：
- 自动检测 Avatar 用 WD ON 还是 OFF
- 调整你的动画器以匹配
- 混合使用会出 bug

**限制**：
- VRCAnimatorLayerControl 只能引用**同一 Animator** 内的层
- 不替换原有 Animator 层（用 Replace 模式可替换）

**Layer Priority**：
- 数字小 → 先应用
- 数字大 → 后应用（覆盖）
- 同优先级按 Hierarchy 顺序

#### 7.3 MA Parameters ⭐⭐

**用途**：定义/重命名参数。

**参数类型**：
| 类型 | 说明 | 何时用 |
|------|------|--------|
| Bool | 布尔 | 开关 |
| Int | 整型 | 计数器 |
| Float | 浮点 | 滑块 |
| Animator Only | 不加到 Expression Parameters | 内部用 |
| Prefix | 用于 PhysBone/Raycast | 配置 PhysBone 链路 |

**重命名参数**：
- Change name to 输入新名
- **只影响组件外**的引用
- 勾选 "Auto rename" 自动选未用名

**默认值**：
- Avatar 重置后用
- 留空 → 用 Expression Parameters 的值或 0/false
- Override Animator Defaults → 覆盖 Animator Controller 的默认

**Saved/Synced**：
- Saved：跨 Avatar 更改和重启保存
- Synced：网络同步（**消耗参数限额**！）

**嵌套**：
- 嵌套使用
- 外层 Saved/默认值**优先**
- 内部重命名可被外层引用

> **教学要点**：参数限额很贵（VRChat 总共 256 个）。**教玩家从一开始就用 Internal**。

#### 7.4 Object Toggle ⭐

**用途**：根据 Active 状态启用/禁用其他对象。

**配置**：
```
1. 组件加到控制对象
2. 点 + 添加目标对象
3. 勾选 = 启用时启用 / 不勾选 = 启用时禁用
```

**冲突解决**：
- 多个 Object Toggle 控制同一对象时，**Hierarchy 中最后的胜出**
- 所有都没 active → 用对象原状态/动画状态

**响应时序**（1 帧延迟）：
- 防止"瞬时穿模"
- A→B→C 链式时,逐级延迟

#### 7.5 Shape Changer ⭐⭐

**用途**：根据 Active 状态改形态键。

**配置**：
```
1. 组件加到要影响的对象（通常是 SkinnedMeshRenderer）
2. Target Renderer 拖入要改的 Renderer
3. 点 + 选形态键
4. 选模式：Delete 或 Set
```

**模式对比**：

| 模式 | 效果 | 何时用 |
|------|------|--------|
| **Delete** | 直接删多边形（性能好） | 不会被动画的情况 |
| **Set** | 把形态键设为指定值 | 会被其他动画影响 |

**Threshold**：
- 决定"哪些顶点算被影响"
- 降低 → 影响更多顶点
- 升高 → 更少

**冲突**：
- 多个 Shape Changer 改同一形态键 → **Hierarchy 中最下方的胜出**

#### 7.6 Bone Proxy ⭐

**用途**：把对象挂到素体特定骨骼上。

**何时用**：
- ✅ 在手上挂个 Cube
- ✅ 在头上挂个发饰
- ❌ 装衣服（用 Merge Armature）

**配置**：
```
1. 组件加到要挂的对象
2. Target 拖入目标骨骼
3. Attachment Mode 自动设置
```

**Attachment Mode**：

| 模式 | 行为 | 何时用 |
|------|------|--------|
| As child at root | 位置/旋转归零 | 通用 Prefab（推荐） |
| As child keep world pose | 保留世界位置 | Avatar 专用 Prefab |

**Match Parent Scale**：
- 启用 → 局部 scale 变 (1,1,1)
- 关闭 → 保留原世界 scale
- 当目标骨骼有缩放时,启用更可靠

#### 7.7 PhysBone Blocker ⭐

**用途**：阻止父 PhysBone 链影响子对象。

**何时用**：
- 配件想刚性附着到 PhysBone 链（如尾巴、耳朵）
- 与 Bone Proxy **配合使用**
- 建议**同一对象**

**与 Bone Proxy 配合**：
- Bone Proxy 挂到 PhysBone 链的某个骨骼
- 加上 PhysBone Blocker → 父 PhysBone 不影响这个对象
- 确保刚性附着

#### 7.8 Menu Item ⭐

**用途**：在 Hierarchy 定义菜单项（不用 VRC 资产）。

**子菜单配置**：
- Submenu Source = Children → 用子级作为菜单项
- Submenu Source = Expressions Menu Asset → 用 VRC 资产
- Source Object Override → 指定其他对象作为子菜单源

**绑定方式**（3 种）：
1. 作为另一个 Menu Item（Sub Menu 模式）的子
2. 与 Menu Installer 同对象
3. Menu Group 的子级

**自动参数创建**：
- 未在 MA Parameters 声明的参数名 → 自动创建
- 控制 Saved/Synced
- ⚠️ Is Default 多个会冲突

#### 7.9 Menu Installer ⭐

**用途**：把菜单项装到 Avatar 主菜单。

**使用方法**：
- 默认装到顶级菜单
- 点 "Select Menu" 选目标菜单
- 满了自动分页
- 勾 Disable 完全禁用

**Prefab 开发者选项**：
- Menu to install → 选 Menu 资产
- Install To → 装到其他组件的菜单

#### 7.10 Blendshape Sync ⭐

**用途**：把一个 Renderer 的形态键值同步到另一个。

**何时用**：
- 衣服的形态键跟素体身体形状（胸部大小等）
- Avatar 内不同 Mesh 间同步

**限制**：
- 不能链式（A→B→C 不行）
- 不支持通过多层（只支持一级）
- 运行时**只支持** Animator 控制的形态键（不支持 Viseme/EyeLook）

#### 7.11 Floor Adjuster ⭐

**用途**：调 Avatar 垂直位置（鞋底对齐地板）。

**何时用**：装鞋子时,避免陷进地板。

**限制**：
- ⚠️ VRChat **不能动态调** Avatar 高度
- 多个 Floor Adjuster 同时存在 → **不调整**
- 未来可能改变

**使用方法**：
```
1. 新建 GameObject,加 Floor Adjuster
2. 调位置垂直对齐鞋底
3. 用侧视/等距视图调
```

#### 7.12 Platform Filter ⭐

**用途**：按平台启用/禁用对象。

**配置**：
- Include → 只在该平台存在
- Exclude → 在该平台移除

**注意**：很多 MA 组件已自动处理平台限制（如 Merge Animator 只对 VRChat）。**不要重复设置**。

#### 7.13 Visible Head Accessory ⭐

**用途**：让头部子对象在第一人称可见。

**何时用**：
- 头发、配饰在第一人称可见
- 不用照镜子

**限制**：
- ⚠️ 不能是 PhysBone 链的子级
- 全部 Head 子级都用 → 视线被挡

**工作原理**：
- 用 VRCHeadChop 让骨骼可见
- 调整网格避免三角形穿过视角
- 用 proxy 骨骼和权重调整

#### 7.14 Replace Object ⭐⭐

**用途**：完全替换 Avatar 上的对象。

**何时用**：
- 替换 Avatar 的 PhysBones 配置
- 替换 Avatar 的 Body 网格

**限制**：
- 一个对象只能被另一个替换（限制多组合并性）

**子对象处理**：
- 替换对象的子级**和**原对象子级都会保留
- 装到替换对象下

**组件引用**：
- 尝试修复旧对象的引用 → 指向新对象
- 按"同类型同索引"匹配（无模糊匹配）

**对象命名**：
- 替换对象的名字可以不同
- **会更新动画路径**指向新对象

#### 7.15 Scale Adjuster ⭐⭐

**用途**：单独调某骨骼的 X/Y/Z 缩放（不影响子骨骼）。

**何时用**：
- 调整衣服贴合（不原设计的 Avatar）
- X/Y/Z 不同时缩放

**限制**：
- 只对 Unity Scale 工具生效
- 组合工具（Move/Rotate/Scale）仍影响所有子级

**Adjust child positions**：
- 调整子级**位置**（不缩放）以补偿父级缩放

#### 7.16 MMD Layer Control ⭐⭐

**用途**：主动让 Merge Animator 添加的层**参与** MMD World 的"禁用层 2&3"行为（默认 Merge Animator 层是被保护的）。

**背景**：
- 部分 MMD World 会**禁用 FX 动画器的第 2、3 层**
- 原本是禁表情
- MA 默认**保护** Merge Animator 添加的层（不受 MMD 影响），见 §9.2
- 想让 Merge Animator 层也被 MMD 控制？→ 加这个组件

**使用**：
- 装到**目标层本身**（state machine behavior）
- 或用 VRChat Settings 完全禁用整个 MMD World 处理机制

**关联组件 VRChat Settings**：
- **唯一性**：一个 avatar **只能有一个实例**
- **位置**：可放在 avatar 上**任意 GameObject** 上
- **关键设置**：`MMD World Support` 开关
  - 开启 → MA 自动处理 MMD World 行为
  - 关闭 → 完全禁用，不做任何保护

**限制**：
- ⚠️ **必须直接装到层**（不能装到 state）。装到 state 会**破坏 build**
- 官方原话："I can't stop you from attaching them to individual states - but this will break your build (so don't do that)"
- 这是因为 state machine behaviors 只能附加在 layer 上才有意义

#### 7.17 Material Setter / Material Swap ⭐

| 组件 | 用法 | 何时用 |
|------|------|--------|
| Material Setter | 拖 Renderer 进去,改指定槽 | 精确控制某个对象的材质 |
| Material Swap | 拖 Material 进去,批量替换 | 换衣服颜色主题（大量替换） |

**Material Swap 高级功能**：
- Quick Swap 模式：编辑器内快速预览不同材质
- Same Folder / Adjacent Folders
- 在 Inspector 点箭头切换

#### 7.18 Mesh Cutter ⭐⭐

**用途**：按条件删/隐藏多边形。

**4 种 Vertex Filter**：
| Filter | 选什么 | 何时用 |
|--------|-------|--------|
| By Mask | 蒙版纹理指定区域 | 复杂形状 |
| By Axis | 平面一侧 | 上下左右分割 |
| By Bone | 骨骼权重 | 身体/手部分割 |
| By Blendshape | 形态键激活时移动的顶点 | 表情时删除 |

**效率提示**：
- 总是 active → 直接删多边形（省性能）
- 有时 inactive → 隐藏（可能加 constraint,占性能）

**何时不该用**：
- 完全被其他网格盖住 → 用 Object Toggle

#### 7.19 Global Collider ⭐⭐

**用途**：让你的对象**能跟其他 Avatar 的 PhysBone 互动**。

**何时用**：
- 配件想跟别人头发互动
- 武器想被 PhysBone 抓住
- 把 Hand Collider 移到嘴里（模拟咬）

**限制**：
- VRChat 限制 6 个
- 超过 6 个 → **覆盖食指 Collider**
- **慎用**

**Manual Remap**：
- 手动指定占用哪个 Collider
- Head/Torso/Feet 只是 contact sender,不算物理碰撞

#### 7.20 World Fixed Object / World Scale Object ⭐

| 组件 | 用途 | 何时用 |
|------|------|--------|
| World Fixed Object | 跟着世界,不跟 Avatar | 浮空剑、悬浮装饰 |
| World Scale Object | 强制 scale = (1,1,1),不受 Avatar 缩放影响 | 复杂 constraint 道具 |

**World Scale Object 注意**：
- ⚠️ 编辑器**不预览**,游戏中才生效

#### 7.21 Sync Parameter Sequence ⭐⭐⭐（高级）

**用途**：确保 PC 和 Android 版本的 Avatar 共享参数顺序。

**何时用**：
- 同一 Avatar 多个平台版本
- 跨平台同步

**使用方法**：
```
1. 组件加到 Avatar 任意对象
2. 选 "primary platform"（含所有参数的版本）
3. 先在 primary 平台 Build & Upload
4. 再在其他平台 Build & Upload
5. MA 自动同步参数顺序
```

**与 VRChat per-platform overrides**：
- 只在**主 Avatar** 加 Sync Parameter Sequence
- Override Avatar **不用加**
- 自动从主 Avatar 同步缺失参数

**要求**：
- Primary 平台必须**包含所有**要同步的参数
- 缺失会 Build 失败

**限制**：
- ⚠️ 与 VRCFury Parameter Compressor 不兼容

#### 7.22 Convert Constraints ⭐

**用途**：在编译时把 Unity Constraints 转成 VRC Constraints。

**何时用**：
- 默认：装到 Avatar 根
- VRChat Auto Fix 会自动加这个
- **性能优化**（VRC Constraints 比 Unity 性能好）

---

#### 7.23 8 个核心组件 API 字段表（精读官方 Reference）
> **定位**：本节汇总**玩家/创作者最常用的 8 个核心组件**的完整 Inspector 字段，作为 §7 速查表的"深度版"参考。
> 数据来源：逐个抓取 [官方 Reference 章节](https://modular-avatar.nadena.dev/docs/reference) 全部页面。
> 标注：**[FACT]** = 官方原文/直译；**[INFERENCE]** = 基于文档的合理总结/经验归纳。

##### 7.23.1 Merge Armature

| 字段 | 类型 | 说明 |
|------|------|------|
| **Merge Target** | GameObject / path | 拖入 avatar 上对应的目标骨骼。内部以 path 形式保存以保证 prefab 序列化后可恢复。 |
| **Prefix / Suffix** | string | 查找匹配骨骼时自动剥离的前后缀（通常 Setup Outfit 时自动设置）。 |
| **Position Lock Mode** | enum | `Not locked` / `Base==>Target`（单向）/ `Base<==>`（双向）。默认 Setup Outfit 时为单向。 |
| **Avoid Name Collisions** | bool | 默认开启，为新增骨骼改名以避免与其它合并资产冲突。 |
| **Reset Position to Base Avatar** | 按钮 + 3 子选项 | "Do It!" + `Also set rotation` / `Also set local scale` / `Adjust outfit overall scale to match base avatar` |

**关键限制 [FACT]**：
- ❌ "**The Merge Armature component is not designed for use in prefabs that are intended to be able to apply generically to many different avatars.**"（不适合通用 prefab，比如 finger-pen）
- ❌ "Because the Merge Armature component assumes that the bones you are binding to do not move, it is not able to generalize to avatars other than the one it was set up with."
- ✅ 自 1.7.0 起支持**嵌套合并**（A→B→C），MA 自动决定顺序。

**常见误用 [INFERENCE]**：把通用化 prefab 用 Merge Armature，导致换 avatar 就骨骼错位；不理解 `Avoid Name Collisions` 关掉后会与他人物资冲突；以为 `Reset Position` 是一次性永久调整。

##### 7.23.2 Merge Animator

| 字段 | 类型 | 说明 |
|------|------|------|
| **Animator to merge** | AnimatorController | 要合并的动画控制器。 |
| **Layer Type** | enum | 目标 layer（FX / Action / Base / Additive / Gesture）。 |
| **Path Mode** | enum | `Relative`（以本组件所在对象为根）/ `Absolute`（以 avatar 根） |
| **Relative Path Root** | GameObject | Relative 模式下作为路径根的对象。 |
| **Layer Priority** | int | 数字越小越先应用，相同 priority 按 hierarchy 顺序。 |
| **Merge Mode** | enum | `Add`（追加）/`Replace Existing Animator`（替换 Avatar Descriptor 上的同 layer animator） |
| **Match Avatar Write Defaults** | bool | 匹配 Avatar 写默认值设置（**避免混用 ON/OFF**） |
| **Delete attached animator** | bool | build 时移除临时 Animator 组件。 |

**关键限制 [FACT]**：
- ❌ "Merge Animator adds to, but **does not replace** existing animator layers. If you want the end-user to completely replace an animator layer, it may be better to have them replace it in the avatar descriptor in the traditional way."
- ❌ "Having **multiple Merge Animators set to the same Layer Type and Replace mode will result in an error**."（多个 Replace 模式同 layer 会报错）
- ❌ VRCAnimatorLayerControl "only supports ... which reference layers within the same animator. ... ensure the `Playable` field matches the layer set on the Merge Animator component, and set the `Layer` field to be the index of the layer within your animator."
- ⚠️ 部分 blend tree 类型不支持 write defaults OFF 转换。

**常见误用 [INFERENCE]**：在 Absolute 模式下用 Unity 临时 Animator 在 prefab 内录动画导致路径错位；为"覆盖"官方动画层却忘切 Replace Mode；忽略 humanoid bone 动画无视 Relative Path 而误调路径。

##### 7.23.3 Parameters

| 字段 | 类型 | 说明 |
|------|------|------|
| **Name** | string | 参数名或 PhysBone prefix。 |
| **Parameter Type** | enum | `Bool` / `Int` / `Float` / `Animator Only` / `Prefix` |
| **Change name to** | string | 把本作用域内引用重映射到外部名字。 |
| **Auto rename** | bool | 自动选未用名。 |
| **Default Value** | 多种类型 | avatar reset 时使用。 |
| **Override Animator Defaults** | bool | 还会改写 Animator Controller 的 default。 |
| **Saved** | bool | 跨 avatar 切换/重启保留。 |
| **Synced** | bool | 占用网络 parameter 配额（VRChat 总共 256 个） |

**关键类型说明**：
- `Animator Only` 和 `Prefix` **不会**加入 Expressions Parameters
- `Prefix` 用于 PhysBone / Raycast 链路配置

**关键限制 [FACT]**：
- "The 'Saved' parameter will take the **outermost** 'Saved' setting. However, when multiple MA Parameters components which are not nested set 'Saved' to different values, the parameter will be saved **if any of the components** set it to be saved."
- "If multiple components which are not nested set a non-blank default value, a **warning will be shown**, as it's unclear which should be used."

**常见误用 [INFERENCE]**：把所有 bool 全勾 Synced 撞到 VRC 256 上限；忘开 Override Animator Defaults 导致 reset 不生效；不嵌套拆分导致多 prefab 重命名冲突。

##### 7.23.4 Object Toggle (Reactive Component)

| 字段 | 类型 | 说明 |
|------|------|------|
| **Target** | List<GameObject> + bool | `+` 添加目标，勾选 = 启用时目标 active=true；不勾选 = 启用时目标 active=false |
| **Invert condition** | bool | 反转触发条件（详见 §5.1） |
| **控制对象** | GameObject | 自身所在 GameObject 即为"控制对象" |

**关键限制 [FACT]**：
- ❌ 冲突时 "the Object Toggle that appears **last in hierarchy order** will take precedence."
- ⏱️ "Object Toggle updates affected objects **one frame after** the controlling object is updated."（1 帧延迟）"when an Object Toggle is disabled, the disabled object ... is disabled one frame later than usual."
- "If all Object Toggle components controlling a target object are **inactive**, the object's original state, or (if other animations are manipulating that object) animated state will be used."

**常见误用 [INFERENCE]**：用 Object Toggle 反向控制同一个父级导致循环；不知道 1 帧延迟在快速连切时看到闪烁；多 prefab 冲突时未留意 hierarchy 顺序而错认为 bug。

##### 7.23.5 Shape Changer (Reactive Component)

| 字段 | 类型 | 说明 |
|------|------|------|
| **Target Renderer** | SkinnedMeshRenderer | 要操作的目标网格（一般是 body） |
| **Blendshape 列表** | List<BlendShape> | 每条可选 `Delete` 或 `Set` 模式 |
| **Mode** per shape | enum | `Delete`（删多边形）/ `Set`（设为指定值） |
| **Value** (Set 模式下) | float | 目标 blendshape 值 |
| **Threshold** | float | 判定顶点"被 blendshape 影响"的阈值，**减小**可让更多顶点被删除 |

**关键限制 [FACT]**：
- ❌ "This component should **not be used to modify blendshapes that are also animated by other animations**. Animate the on/off state of the object containing the Shape Changer component instead."
- ❌ "If multiple shape changers try to operate the same blendshape at the same time, the **lowest one in the hierarchy** will generally win."
- ✅ Delete 在无动画时**减少实测多边形数**（性能最优）；有动画时仍完全隐藏但不减少多边形数。

**常见误用 [INFERENCE]**：用 Shape Changer 改被表情动画驱动的 blendshape，结果表情失效；Threshold 不调导致隐藏不完全；混淆 Delete 与 Set 模式用途。

##### 7.23.6 Bone Proxy

| 字段 | 类型 | 说明 |
|------|------|------|
| **Target** | GameObject / humanoid bone + path | 内部以 humanoid bone + relative path 形式保存，便于 prefab 序列化 |
| **Attachment Mode** | enum | `As child at root`（位置旋转归零、保持世界 scale）/ `As child keep world pose`（保留世界坐标姿态） |
| **Match Parent Scale** | bool | 开启时 local scale 会被调为 (1,1,1)，用于目标骨骼父级被缩放场景 |
| **Advanced** 折叠 | - | 手动调整 humanoid bone / relative path |

**Attachment Mode 子选项 [FACT]**：
- 可仅保留 position 或 rotation 之一
- `As child keep world pose` "is usually only useful for **avatar-specific** prefabs"（不适合跨 avatar 通用）

**关键限制 [FACT]**：
- ❌ "Bone Proxy **isn't intended** to be used to configure clothing. Try using Merge Armature instead."（不要拿 Bone Proxy 做衣服合并）

**常见误用 [INFERENCE]**：用 Bone Proxy 装衣服（应该用 Merge Armature）；在非专用 prefab 上选 keep world pose 导致换 avatar 错位；忽略 Match Parent Scale 导致父骨骼被缩放时饰品变畸形。

##### 7.23.7 Menu Item

| 字段 | 类型 | 说明 |
|------|------|------|
| **Menu Item Name** | string | 取自所在 GameObject 的名字（在 hierarchy 直接改名即可） |
| **Menu Type** | enum | Toggle / SubMenu 等 |
| **Icon** | Texture2D | 菜单图标 |
| **Parameter** | string | 关联的 Animator 参数名 |
| **Submenu Source** | enum | `Expressions Menu Asset`（用 VRC 资产）/ `Children`（用子级） |
| **Source Object Override** | GameObject | Children 模式下替换子节点来源 |
| **Is Default** | bool | 默认是否启用（**多个勾 = 行为未定义**） |
| **Saved / Synced** | bool | 参数自动创建时显示 |

**关键限制 [FACT]**：
- ⚠️ "If the number of items in the submenu exceeds the maximum number of items on a VRC menu, a 'next' item will **automatically be created** to split up the menu."（自动分页）
- ❌ "If multiple menu items are set to 'Is Default', the **results are undefined**. Don't do that!"
- ❌ "**Unbound menu items have no effect**."（必须通过子层级 / Menu Installer / Menu Group 三选一绑定）
- ✅ 参数名未在 MA Parameters 或 VRC Expressions Parameter 声明时会被**自动创建**。

**常见误用 [INFERENCE]**：Menu Item 没绑到 Installer/Group 导致表情菜单里没出现；多菜单项勾 Is Default 行为未定义；改 GameObject 名字却没意识到这就是菜单显示名。

##### 7.23.8 Menu Installer

| 字段 | 类型 | 说明 |
|------|------|------|
| **Disable** | bool | 勾选后完全关闭本 prefab 的菜单安装 |
| **Install To** | Menu path | "Select Menu" 双击选择目标子菜单；支持引用其它 Menu Installer 正在安装的子菜单以"扩展" |
| **Menu to install** | VRCExpressionsMenu | 在 Prefab Developer Options 标签下添加要追加的菜单 |
| **Menu sources** | 自动 | 附加 Menu Item / Menu Group 后会自动生成菜单条目 |

**关键限制 [FACT]**：
- "By default, the prefab's menu will be installed at the **top level** of your avatar's action menu."
- "If the selected menu gets full, it will be **automatically split** into multiple pages (submenus)."
- ⚠️ "if you want a submenu of your own, you will need to create **two menu assets**: One for the submenu control, and one for the inner menu itself."

**常见误用 [INFERENCE]**：把"submenu 控件"和"内层菜单"合并成一个 asset，导致 submenu 内容与 control 重复或缺失；用户点击 Select Menu 选错位置而把 prefab 菜单装到错误分组；期望 Installer 会替换而不是追加。

---

## 8. 安装 / 配置 / 故障排查（官方 Dealing with problems 完整版）
> **来源**：[Dealing with problems 主页](https://modular-avatar.nadena.dev/docs/problems) + [Installation issues](https://modular-avatar.nadena.dev/docs/problems/install) + 综合教学法归纳
> **关键事实**：官方"Dealing with problems"章节**只有 2 个子页面 + 1 个主页常见问题**——这是**"问题诊断分布式设计"哲学**的体现

### 8.0 官方问题诊断的设计哲学
**观察**：MA 官方"Dealing with problems"章节**异常精简**：
- 主页：1 个常见问题（"Nothing is getting processed at all"）
- 子页面 install：1 个常见问题（"Failed to add Repo"）
- 整个 problems 章节**只覆盖 2 个问题**

**为什么这么少**？—— **问题诊断的责任分散到了多个地方**：

| 位置 | 责任 | 示例 |
|------|------|------|
| **Dealing with problems** | **最高频、影响最大**的 2-3 个问题 | Apply On Play、Failed to add Repo |
| **Component Reference** | 每个组件带"Known limitations"段 | 哪些情况不能用、已知 bug |
| **General Behavior** | MA 的"自动行为" + 玩家需要知道的平台行为 | MMD World 自动处理 |
| **FAQ** | "能不能 X / 怎么处理 Y"类问题 | 导出 VRM、跨 Avatar 衣服 |
| **GitHub Issues** | 实际遇到的 bug、新功能请求 | 错误堆栈、性能问题 |
| **Discord** | 实时问题讨论、社区经验 | 玩家互助 |

**给 Agent 的启示**（**重要**）：

> ✅ **不要"假装权威"** —— 只覆盖知识库有的内容
> ✅ **主动告诉玩家**"这个问题可能要去 Discord / GitHub 问"（不要硬猜）
> ✅ **问题诊断是分布式责任** —— 一个文档不可能覆盖所有问题
> ✅ **教学最高优先级**：让玩家**自己学会查**这些问题诊断渠道

**教学意义**（写教学文档时）：
- ❌ 不要写"Avatar 改模 100 个常见问题"——**水分太大**
- ✅ 写"**最高频 5 个问题 + 如何找到其他问题的答案**"
- ✅ "Discord 关键词搜索" "GitHub Issue 搜索" 是必备教学内容

---

### 8.1 错误窗口（MA 的核心诊断工具）
> 来源：[Dealing with problems 主页](https://modular-avatar.nadena.dev/docs/problems)

**为什么用错误窗口而不是 Console**（**重要教学点**）：

| 维度 | Console | MA 错误窗口 |
|------|---------|-----------|
| 信息杂度 | 极高（所有 Unity/SDK/MA 错误混在一起）| **只显示 MA 相关错误** |
| 更新机制 | 静态（需要重新触发） | **实时**跟随编辑更新 |
| 跳转到对象 | 自己搜 Hierarchy | **点对象名直接跳** |
| 适合人群 | 高级用户 | **新手友好** |

**打开方式**：

```
自动：MA 检测到错误时自动弹出
手动：Unity 工具栏 → Tools → Modular Avatar → Show Error Report
```

**错误窗口能做什么**（**精确步骤**）：

| 操作 | 教学价值 |
|------|---------|
| **点对象名** | 跳到 Hierarchy 选中，**不需自己找** |
| **实时更新** | 改完代码/组件，错误**自动消失**或变化 |
| **查看错误详情** | 显示具体哪个组件、哪个字段出问题 |

**教学要点**：
- ✅ 教玩家"看到错误**先看错误窗口**，不要慌"
- ✅ 教玩家"**点对象名**能跳过去"——不抽象
- ❌ 不要教玩家"看 Console 找 MA 错误"——**这条路是错的**

**对应"5 步诊断法"的步骤 2**（见 §8.6）—— **永远先看错误窗口**。

---

### 8.2 安装问题（"Failed to add Repo"）
> 来源：[Installation issues](https://modular-avatar.nadena.dev/docs/problems/install)

**症状**：在 VCC 添加 Modular Avatar 仓库时弹出 "Failed to add Repo" 错误。

**根因**：**VCC 已知 bug**（MA 官方原话："due to a bug in the VCC"）。

**正确处理（3 步精确操作）**：

```
步骤 1: 点 "Cancel" 取消错误
步骤 2: 看左侧 "Community Repositories" 列表
步骤 3: 找到 "bd_" 仓库 → 确认 checkbox 已勾选
```

**99% 实际情况**：仓库**已经添加成功了**，VCC 误报错误。

**如果列表里没有 bd_**：
- 重新添加仓库 URL：`https://vpm.nadena.dev/vpm.json`
- 重启 VCC
- 用 ALCOM 代替 VCC（VCC 已知问题较多）

**教学价值**（**提炼自官方页面**）：

| 原则 | 官方做法 | 教学启示 |
|------|---------|---------|
| **诚实告知工具 bug** | "due to a bug in the VCC" | 不要掩饰第三方工具问题 |
| **给绕过方案** | "Click Cancel, look in the list..." | 不要只说"这是 bug" |
| **反直觉但对** | "Canceled 是对的" | 教玩家**正确的反直觉行为** |
| **99% 情况是误报** | "Usually this means the repository has already been added" | 教玩家**不要重复操作** |

**教学话术**（教玩家时直接用）：
> "看到 Failed to add Repo 不要慌——**99% 是 VCC 误报**。点 Cancel 取消，然后看左侧 Community Repositories 列表，确认 bd_ 已勾选。如果勾选了就**没问题**，不用管那个错误。"

---

### 8.3 "Nothing is getting processed at all"（最高频问题）
> 来源：[Dealing with problems 主页 Common problems](https://modular-avatar.nadena.dev/docs/problems)

**症状**：你做了操作（加了组件、点了 Setup Outfit），但**什么都没发生**。

**根因（99% 的情况）**：`Apply On Play` 没勾选。

**修复路径**（**精确到字段**）：

```
步骤 1: 选中 Avatar 根 GameObject
步骤 2: 看 Inspector 面板
步骤 3: 找到 VRC Avatar Descriptor 组件
步骤 4: 在该组件内找到 "Apply On Play" 复选框
步骤 5: 勾上它
步骤 6: 进 Play 模式 → MA 自动处理
```

**关键事实**（玩家必须知道的）：
- **Apply On Play** 是 VRC Avatar Descriptor 的一个**字段**，不是独立组件
- 在 Avatar 根 GameObject 上
- 必须**进 Play 模式**才会触发处理

**教学要点**（**重要**）：
- ✅ "99% 的情况"是友好教学——**不是"绝对"**（不绝对化）
- ✅ 路径精确到"组件 + 字段名"——**不抽象**（不写"勾上那个选项"）
- ✅ 玩家**不需要理解"为什么"**——只需要照做
- ❌ 不要说"MA 在 Editor 不会自动处理"——**玩家不需要这个抽象**

**教学话术**（教玩家时直接用）：
> "装上组件没反应？99% 是没勾 Apply On Play。**选中 Avatar 根**（你素体最外层那个对象）→ 看右边 Inspector → 找 VRC Avatar Descriptor 组件 → 找里面那个 Apply On Play 复选框 → 勾上 → 进 Play 模式看看。"

---

### 8.4 错误报告的更新机制（进阶）
> 来源：[Dealing with problems 主页](https://modular-avatar.nadena.dev/docs/problems)（原话："Most errors on this report will update automatically as you edit your avatar, but for some types of errors a new build may be required"）

**两种错误更新机制**：

| 类型 | 行为 | 何时遇到 |
|------|------|---------|
| **自动更新**（大多数）| 改完组件，错误窗口**立即重新评估** | 配置错误、组件缺失 |
| **需要重新 Build**（少数）| 错误窗口提示"需要重新 Build" | Animator 错误、骨骼结构问题 |

**需要重新 Build 的场景**：
- Animator Controller 报错
- 骨骼名不匹配
- 某些 NDMF 错误

**重新 Build 的方法**（**3 选 1**）：

```
方法 A: 进 Play 模式一次（最简单）
方法 B: Tools → Modular Avatar → Manual Bake Avatar（最干净）
方法 C: Tools → NDM Framework → Force Reserialize（最彻底）
```

**教学意义**（**重要**）：
- 玩家改了组件后看到错误**还在**会很慌
- 提前告诉"**有些错误需要重新 Build**"避免恐慌
- **教学要点**：改完不消失？→ "**进 Play 模式 / 重新 Build**"

---

### 8.5 常见问题快速诊断表（症状 → 原因 → 修复）

| 症状 | 可能原因 | 修复 |
|------|---------|------|
| 装上衣服原地不动 | Setup Outfit 没执行 | 右键衣服 → Setup Outfit |
| 装上衣服没反应 | Apply On Play 没勾 | Avatar 根 → VRC Avatar Descriptor → Apply On Play 勾上 |
| 错误窗口打不开 | 出错时未弹出 | Tools → Modular Avatar → Show Error Report |
| 改完错误还在 | 需要重新 Build | 进 Play 模式 / Manual Bake Avatar |
| 衣服部分穿模 | Shrink 形态键没联动 | 装衣服的对象加 Shape Changer |
| 调体型衣服不变形 | 没加 Blendshape Sync | 加 Blendshape Sync |
| 鞋子陷地 | 衣服层级 Y 位置不对 | 加 Floor Adjuster |
| 多个小组件参数冲突 | 参数名相同 | 加 MA Parameters → Internal |
| 编辑器有效果,VRChat 无 | GameObject 路径不对 | 检查 Setup Outfit 是否成功 |
| 装上后报错 | 骨骼名不匹配 | 手动改衣服骨骼名 + 重做 Setup Outfit |
| Apply On Play 灰了 | 没装 VRCSDK | 装 VRCSDK |
| VCC 提示 Failed to add Repo | VCC 已知 bug | 点 Cancel，确认 bd_ 仓库已勾选 |
| 衣服跟着 Avatar 反而错乱 | Position Lock 模式不对 | 改 "Not locked" 测试 |
| Console 找不到 MA 错误 | 看错地方了 | 看错误窗口，不是 Console |

---

### 8.6 5 步问题诊断法（玩家也能用）
> 综合官方 problems 章节 + FAQ + 教学法归纳
> **核心思想**：从"最高频"开始 → 逐步深入

```
步骤 1: 看到问题 → 截图保存
  └─ 错误窗口截图 + Scene 视图截图

步骤 2: 看错误窗口（不是 Console！）
  ├─ 打开方式：Tools → Modular Avatar → Show Error Report
  ├─ 点对象名跳到 Hierarchy
  └─ 大多数错误会自动更新

步骤 3: 检查最高频原因（按官方顺序）
  ├─ Apply On Play 勾了吗？（最常见 90%）
  ├─ Setup Outfit 执行了吗？
  └─ VRCSDK 装了吗？（Apply On Play 灰了的情况）

步骤 4: 检查组件配置
  ├─ 组件有没有添加？
  ├─ 拖的对象拖对了吗？
  ├─ MA Parameters 位置对吗？（教程 6 易错点）
  └─ 骨骼名匹配吗？（衣服 Hips 含素体 Hips 名）

步骤 5: 用 Manual Bake Avatar 看最终结果
  └─ 选中 Avatar → Tools → Modular Avatar → Manual bake avatar
  └─ 看 ModularAvatarOutput 文件夹的结果
```

**反向使用**（**重要**）：
- **99% 玩家**做完步骤 1-3 就解决了
- **进阶玩家**才需要做步骤 4-5
- **最后手段**：GitHub Issues 搜 / Discord 问（不要硬猜）

---

### 8.7 教学风格速记：问题诊断文档如何写
> 从官方 problems 章节提取的 **8 条设计原则**

| # | 原则 | 官方做法 | 我们写文档时的应用 |
|---|------|---------|-----------------|
| 1 | **只列最高频问题** | 整个章节就 2 个问题 | 不要"为了完整"列 20 个问题 |
| 2 | **错误窗口 > Console** | 专门有"Show Error Report"按钮 | 教玩家"先看错误窗口，不要看 Console" |
| 3 | **诚实告知工具 bug** | "due to a bug in the VCC" | 不要掩饰工具问题 |
| 4 | **路径精确到字段** | "VRC Avatar Descriptor → Apply On Play" | "这个组件 + 这个字段"——不抽象 |
| 5 | **错误自动更新提示** | "Most errors ... will update automatically" | 提前说"有些错误需要重新 Build" |
| 6 | **给出绕过方案** | "Click Cancel, look in the list..." | 不要只说"这是 bug"——给替代方案 |
| 7 | **不假设完美** | "Usually this means..." | 用"99%"/"通常"——不绝对化 |
| 8 | **错误窗口可重开** | 工具栏菜单明文 | 教玩家"出错关掉了也没事" |

**5 条禁忌**（写问题诊断文档时不要）：

| ❌ 反例 | ✅ 正确 |
|---------|--------|
| "可能有很多原因" | "**99% 是 X**" |
| "检查你的设置" | "**VRC Avatar Descriptor → Apply On Play**" |
| "看 Console 找错误" | "**打开 MA 错误窗口**" |
| "这是 VCC 的问题" | "**VCC 已知 bug**，点 Cancel..." |
| "如果还不行..." | "**重新 Build**（进 Play 模式）" |

---

### 8.8 FAQ （基于最新官方 FAQ 学习）

> 来源: [官方 FAQ 页面](https://modular-avatar.nadena.dev/docs/faq)

#### Q1: 能导出到其他格式（如 VRM）吗？

**官方回答**：**不能自动**导出。但可以**手动执行 MA 转换**,然后用其他工具（如 UniVRM）转换格式。

**具体操作**：
```
1. 选中 Avatar
2. Unity 工具栏:Tools → Modular Avatar → Manual bake avatar
3. 自动复制 Avatar + 应用所有 MA 转换
4. 结果在 ModularAvatarOutput 文件夹
5. 之后用 UniVRM 之类的工具正常转换
```

**⚠️ 警告**：手动 Bake 时 MA 会生成**一堆生成的 Mesh 和资源**,**不会自动清理**。完成后可以放心删除 ModularAvatarOutput 文件夹。

**教学要点（玩家向）**：
- 99% 玩家**不需要这个**——只在你"想把 Avatar 弄到 VRM 平台"才用
- 这是一个**创作者/特殊场景**工具,不是日常操作
- 教学时**不要主动推荐**——除非玩家明确问"我想导出到 XXX"

#### Q2: 能用 MA 装别人 Avatar 的衣服吗？（跨 Avatar 衣服）

**官方回答**：**可以**——前提是**骨骼名匹配**。

**原理**：
- Modular Avatar 假设**源 Avatar 和衣服**的**骨骼名相同**
- 如果**不匹配**,你需要**重命名衣服的骨骼**来匹配你的 Avatar
- 一旦骨骼名匹配,你调整衣服骨骼位置 → Merge Armature 会保留这些调整

**实操流程**：
```
1. 把衣服 Prefab 拖到你的 Avatar 下
2. 右键 → Setup Outfit
3. 如果 Setup Outfit 失败(找不到 Hips 匹配):
   → 进入衣服的 Armature,重命名骨骼以匹配你的 Avatar
4. 用 "Reset position to base avatar" 功能大致对齐衣服位置
5. 手动微调
```

**教学要点（玩家向）**：
- 这是**创作者向问题**——普通玩家**几乎不会遇到**
- 偶尔玩家买了一个"通用衣服"想装到自己的小众 Avatar 上 → 才需要这个
- **诚实告知**：跨 Avatar 衣服**经常**需要手动调位置,不是"拖一下就好"
- **不替玩家做判断**：玩家要不要折腾,让玩家自己决定

#### Q3: 多语言界面？

**官方回答**：官方有**日语翻译**——点页面右上角"🌐"切换。

**支持的语言**（截至文档版本）：
- English（默认）
- 日本語（Japanese）

**教学要点**：
- 中文玩家**没有官方翻译**
- 但截图 + 简单英文术语玩家都能看懂
- 教学时**用中文**,但**保留英文 UI 字段名**（如 "MA Menu Item"、"Bone Proxy"）—— 玩家在 Unity 里看到的是英文

---

## 9. 高级话题

### 9.1 手动 Bake Avatar（Manual Processing 完整版）
> 来源：[官方 Manual processing 页面](https://modular-avatar.nadena.dev/docs/manual-processing)
> **定位**：99% 的 VRChat Avatar 玩家**不需要这个功能**——但创作者或导出到其他平台时**必须知道**。

#### 9.1.1 何时需要手动 Bake

| 场景 | 是否需要手动 Bake | 原因 |
|------|------------------|------|
| 普通 VRChat 上传 | ❌ 不需要 | Play 模式 / Build 时 MA 自动处理 |
| 调试 Avatar 问题 | ✅ **需要** | 看"MA 处理完的真实 Avatar"长什么样 |
| 导出到 UniVRM | ✅ **需要** | UniVRM 不认识 MA 组件，需要先转成普通 Avatar |
| 导出到 Resonite | ✅ **需要** | 同上 |
| 给非 VRChat 平台用 | ✅ **需要** | MA 是 VRChat 专用，其他平台不会自动触发 |
| 验证"我的组件配置正确吗" | ✅ **需要** | 直接看最终结果，不用进 Play 模式 |

#### 9.1.2 完整操作步骤（5 步）

```
步骤 1: 选中 Avatar 根 GameObject
  └─ 必须是带 VRC Avatar Descriptor 的那个对象

步骤 2: 工具栏 Tools → Modular Avatar → Manual bake avatar
  └─ 也可以右键 Avatar → 同一选项

步骤 3: MA 自动复制 Avatar + 应用所有 MA 转换
  └─ 注意:是"复制",原 Avatar 不变

步骤 4: 查看 ModularAvatarOutput 文件夹
  └─ 位置:Assets/ModularAvatarOutput/
  └─ 默认所有资产打包成单个文件
  └─ 选中文件 → Inspector → 点 "Unpack" 拆开

步骤 5: 删 baked avatar 副本时,ModularAvatarOutput 也可安全删除
  └─ 中间产物,不留垃圾
```

#### 9.1.3 ModularAvatarOutput 详解

**为什么有这个文件夹**：
- 避免 Unity 已知 bug
- 提升处理速度
- 保持工程文件整洁

**默认打包成单个文件的原因**：
- 多个文件易触发 Unity 导入 bug
- 打包后处理速度更快

**Unpack 按钮何时用**：
- 想看每个生成资源**单独**什么样
- 想用 git diff 等版本控制工具对比变化
- 调试单个组件错误
- **不需要** Unpack 时 → 保持打包状态即可

#### 9.1.4 关键警告

> ⚠️ **不要把 ModularAvatarOutput 当作核心资源长期保留**——它是**中间产物**
> ⚠️ **不要在没删除 baked avatar 时单独删 ModularAvatarOutput**——会引发引用丢失
> ⚠️ **不要期望手动 Bake 后原 Avatar 会变**——它只生成**副本**

#### 9.1.5 教学要点（玩家向）

- 99% 玩家**不需要这个**——只在玩家问"我想把 Avatar 弄到 VRM 平台"时教
- **不要主动推荐**——除非玩家明确问
- 教学时强调:这是**创作者/特殊场景**工具,不是日常操作
- 教学话术:"99% 玩家不需要这个。它是给'想把 Avatar 弄到其他平台'的人用的。"
- 详见 §8.8 Q1 FAQ

### 9.2 MMD World 行为（General Behavior 核心子页面）

> 来源：[MMD World Workarounds](https://modular-avatar.nadena.dev/docs/general-behavior/mmd)

**问题背景**：
- 部分 **MMD Worlds** 在 VRChat 中会主动**禁用** Avatar FX Animator Controller 的**第 2 层和第 3 层**
- 原本目的是**禁表情**，让 MMD World 接管表情控制
- 这是 VRChat MMD World 圈子的**约定行为**

**MA 自动处理机制（完整）**：

| 步骤 | MA 做什么 | 为什么 |
|------|---------|--------|
| 1 | 识别"**原本是层 2、3**"的层 | 这些层就是 MMD World 想禁的 |
| 2 | 让它们在 MMD World 中被禁用 | 满足 MMD World 的预期 |
| 3 | 如果新层插入到它们之前，**添加 relay layers** | 中继层用于在 MMD World 之外时**重新启用**原 2、3 层（"drive layers 2 and 3 off and on appropriately"） |
| 4 | **Merge Animator 添加的层不参与** | 见下方"保护机制" |
| 5 | 必要时**添加 padding layers** | 用来"垫"出位置，让 Merge Animator 的层落在非 2、3 的位置 |

**保护机制（关键细节）**：

> 官方原话："Layers added via Merge Animator **(even in replace mode)** will not be affected by this MMD world behavior; **if necessary, padding layers will be added to protect them**."

| 情况 | 是否受 MMD 影响 | 原因 |
|------|---------------|------|
| 原本在层 2、3 | ✅ 是 | MMD World 设计如此 |
| Merge Animator 添加的层 | ❌ 否 | MA 主动保护 |
| Merge Animator + Replace 模式 | ❌ 否 | 即使 replace 也保护 |
| 手动添加到层 2、3 的层 | ⚠️ 取决于手动管理 | MA 不能自动管理手动添加的层 |

**主动 opt-in 让 Merge Animator 层参与 MMD 控制**：
- 加 `MA MMD Layer Control` state machine behavior 到目标层
- 默认行为：Merge Animator 层**不**受 MMD 影响
- 主动 opt-in 后：该层会像原层 2、3 一样被 MMD World 禁用

**完全禁用整个机制**：
- 加 `VRChat Settings` 组件（**一个 avatar 只能有一个实例**，可放任意位置）
- 关掉 `MMD World Support` 设置
- 关闭后 MA 不做任何 MMD 相关处理

**已知警告**：

> ⚠️ **MA MMD Layer Control 必须直接装到层**，不能装到 state。装到 state 会**破坏 build**。
> 官方原话："Due to how state machine behaviors work, I can't stop you from attaching them to individual states - but this will break your build (so don't do that)."

**已知限制（官方明确声明）**：

> ⚠️ **这个 workaround 只对禁用层 2&3 的世界有效**。
> 官方原话："This workaround only works for worlds which specifically disable layers 2 & 3. Given current VRChat constraints, **it's not possible to provide a more general solution**."

**实操含义**：
- 如果某个 MMD World 禁的不是 2&3（比如禁 4&5），MA 无能为力
- VRChat 当前 API 不支持通用方案 → 这是**平台限制**，不是 MA 缺陷
- 玩家遇到这种情况 → 需要联系 World 作者，或放弃该 World 的 MMD 集成

**关联知识**：
- 组件详情：`§7.16 MMD Layer Control`
- 教学法：`§14 MMD World 玩家教学法`

### 9.3 分发预制件（创作者向 · 完整版）

> **定位**：基于官方 4 个子页面（Distributing Prefabs / Versioning Policy / Logo Usage / For Outfit Creators）整理的**完整版**。
> 适用对象：**Avatar 配件/服装创作者**。玩家向教学见 §4 / §6 / §11。

#### 9.3.1 引导用户去官方仓库

**核心原则**：MA 许可证**允许**在 Prefab 里夹带 MA 副本，但作者"**strongly recommend**"引导用户去 [GitHub Releases](https://github.com/bdunderscore/modular-avatar/releases)。

**为什么不要夹带**：
- 用户可能装到**很旧**的 MA 版本
- 可能**降级**装坏其他 Prefab
- 跨 Prefab 容易出现版本错乱

**未来计划**：作者打算做 **VCC-based 安装方式**，但需等 VCC 自身改进。

#### 9.3.2 用嵌套 Prefab 兼容非 MA 用户

**场景**：加了 MA 组件的 Prefab 强制要求用户装 MA。部分用户可能不想用 MA。

**核心思想**：把"outfit 核心"和"MA 配置"**解耦**——通过嵌套 Prefab 分离。

**完整 4 步操作流程**：

```
1. 正常创建 outfit prefab
2. 在 Project 视图双击 prefab → 进入 prefab mode
3. 把 prefab 根对象拖到 Project 窗口
   → 弹窗点 "Create Base"
   → 重命名为 "Outfit without Modular Avatar" 之类（你记得住的名字）
4. 在"原 prefab"上设置 MA 组件
   在"新 base prefab"上设置非 MA 设置
```

**关键技巧：Apply as Override 菜单**
- 在测试场景改设置后，用 Prefab Overrides 菜单选择"应用到哪个 prefab"
- 可以把同一个修改**选择性地**应用到 base prefab 或 MA prefab

**效果**：
- 用户装了 MA → 用原 prefab（带 MA 配置），一键完成
- 用户没装 MA → 用 base prefab（手动配置）

#### 9.3.3 用 Internal 参数避免冲突

使用 [Internal 参数](https://modular-avatar.nadena.dev/docs/reference/parameters) 可避免小组件参数名冲突。

**核心机制**：Internal 参数在**编译时**自动重命名为唯一名字 → 不与别的 Prefab 撞名。

**推荐做法**：
- 任何"用 Animator 参数实现的小组件" → 把参数标记为 **Internal**
- 多个小组件用同一参数名不会冲突

详见 [§7.3 MA Parameters](#73-ma-parameters-)。

#### 9.3.4 版本策略（Semantic Versioning）

MA 遵循 [Semantic Versioning](https://semver.org/)：

| 版本变化 | 含义 | 对你的 Prefab 影响 |
|---------|------|-------------------|
| **主版本** (1.x.x → 2.x.x) | 不兼容变更 | Prefab **必须更新**才能用 |
| **次版本** (1.0.x → 1.1.x) | 向后兼容的新功能 | 1.0.x 做的 Prefab 在 1.1.x 上仍可用；1.1.x 做的 Prefab **不保证**能在 1.0.x 上用 |
| **补丁** (1.0.0 → 1.0.1) | Bugfix（不破坏存档格式） | 一般无影响；个别 bugfix 可能影响 |

**推荐策略**：建议用户装**同主版本**下**最新版**（如 1.x.x → 1.20.x）。

**API 稳定性（重要！）**：

| 类别 | 稳定性 |
|------|--------|
| `nadena.dev.modular-avatar`（**Qualified Name** 本身） | ✅ **唯一稳定的 API** |
| `internal` class 名称 | ❌ **不稳定**（补丁版本都可能变） |
| `internal` method 名称 | ❌ **不稳定** |
| NDMF pass 的 "Qualified Name" | ❌ **不稳定** |
| NDMF pass 的**执行顺序** | ❌ **不稳定** |

**给插件开发者的建议**：
- 想依赖特定 MA pass？→ 在 GitHub 提 [Feature Request](https://github.com/bdunderscore/modular-avatar)，说明你的用例，作者会考虑加稳定 API
- 不要在代码里 hardcode `internal` 类的名字或方法签名
- 用 `nadena.dev.modular-avatar` 作为插件本身的 Qualified Name

#### 9.3.5 Logo 使用合规（创作者必读）

> 完整官方规则：https://modular-avatar.nadena.dev/docs/distributing-prefabs/logo-usage

**Logo 政策的目的**：向用户表明"该产品可通过 MA 一致地一键安装"。

**许可前置**：
- 无需**提前申请**许可
- 但 [bd_](https://misskey.niri.la/@bd_) 与 [pumo](https://twitter.com/pumony) 保留最终裁决权
- **被要求撤下时必须撤**

**我能不能用 Logo？决策表**：

| 产品类型 | 能否用 Logo | 条件 |
|---------|-----------|------|
| **带 MA 组件的 Avatar/服装 Prefab** | ✅ 可以 | Prefab 必须含**预配置**的 MA 组件；MA 必须是**主要**安装方式 |
| **NDMF 非破坏性编辑器扩展** | ✅ 可以 | 必须兼容或依赖 MA；详见下方"编辑器扩展额外约束" |
| **不含 MA 组件的 Prefab**（纯 Compatible） | ❌ **不可用** | - |
| **手工安装流程**的 Prefab | ❌ **不可用** | - |

**编辑器扩展的额外约束**（容易踩坑）：
- 卸载只需"删除 prefab"即可（**非破坏性**）
- 不要求用户**手动**触发任何处理/生成操作
- **不能在自家 UI 中用 MA Logo**（避免和 MA 自带 UI 混淆）
- 不能暗示 MA 官方**背书/认可**

**Logo 摆放红线**：
- 必须**整体使用、不得改动**（例外：可加描边/阴影以提升对比度）
- 禁止**动画**、禁止**作为图案/背景**
- 视频中过渡动画例外（不得显著改变形状/风格）
- 必须**足够对比度**、与其他元素**保持合理距离**
- 必须使用**原始颜色**（多色变体可选）

**资源下载**：[Logo 资源包](https://modular-avatar.nadena.dev/assets/files/modular_avatar_logo-711f570c8ad26b2b46d46b44e198f647.zip)

**联系 bd_**（边界情况 / 特殊许可）：
- Discord: `bd_`
- Twitter: `@bd_j`
- Misskey: `@bd_@misskey.niri.la`
- Email: `bd_@nadena.dev`

#### 9.3.6 创作者支持等级：Compatible vs Preset

MA 提供**两个等级**的创作者支持：

| 维度 | **Modular Avatar Compatible** | **Modular Avatar Preset** |
|------|------------------------------|--------------------------|
| 含 MA 组件 | ❌ 无 | ✅ 含 |
| 依赖 MA 安装 | 不需要 | **需要** |
| 创作者成本 | 低（保证命名规范即可） | 高（需预跑 Setup + 加增强组件） |
| Logo 使用权 | ❌ **不可用** | ✅ 可用 |
| 用户操作 | 拖入后**自己**右键 Setup Outfit | 拖入后**无需任何操作** |
| 适用对象 | 通用服装、跨生态分销 | MA 用户专享 |

**关键洞察**：创作者可**同时发布两个版本**——一个含 MA 组件（Preset）、一个不含（Compatible base）——覆盖两类用户。详见 [§9.3.2 用嵌套 Prefab 兼容非 MA 用户](#932-用嵌套-prefab-兼容非-ma-用户)。

#### 9.3.7 Setup Outfit 深度解析

**Setup Outfit 做什么**（4 阶段）：

| 阶段 | 做什么 | 关键点 |
|------|--------|--------|
| **① 识别骨骼** | 找衣服的 Hips 骨骼 | 路径：`OutfitRoot → [Armature] → Hips`；Hips 名必须**含**素体 Hips 名 |
| **② T/A Pose 转换** | 旋转手臂对齐 | ⚠️ **手臂长度必须完全相同**才能转换 |
| **③ 创建 Merge Armature** | 合并骨骼树 | 同名骨骼复用；**含组件的骨骼不合并**（移到对应素体骨骼下） |
| **④ 创建 Mesh Settings** | 配置 Light Probe + Bounding Box | 与素体保持一致 |

**骨骼命名规则**：
- 允许在骨骼名前后加**统一**的前缀/后缀
- **所有骨骼**前缀/后缀必须一致（大小写敏感）
- 没有统一前后缀的骨骼 → **不会**被合并到素体

**Armature 对象名**：**任意**都行。Setup Outfit 不关心 Armature GameObject 叫什么。

**模糊匹配模式（兜底）**：
- 当衣服骨骼名不规范时 → Setup Outfit 会尝试**重命名**衣服骨骼以匹配素体
- ⚠️ **官方建议避免**这种模式（可靠性差）
- **最佳实践**：从一开始就让衣服骨骼**精确包含**素体骨骼名

**智能行为**：
- 同名骨骼 → **共享素体骨骼**（不重复创建）
- **含组件**（非 Transform）的骨骼 → **不合并**，移到对应素体骨骼下作为子级
- 素体没有的骨骼（如 Upper Chest）→ 保留为独立骨骼
- 上半身有特殊骨骼时 → 自动用**多个 Merge Armature** 协同

#### 9.3.8 Bone Proxy vs Merge Armature 对比

| 维度 | **Merge Armature** | **Bone Proxy** |
|------|-------------------|---------------|
| **作用** | 合并**整棵骨骼树** | 移动**单个对象**到指定骨骼 |
| **目标匹配方式** | 按**骨骼名**匹配 | 按 **Humanoid 角色**匹配（与骨骼名无关）|
| **通用性** | 弱（依赖命名约定） | 强（可适配任意 Avatar）|
| **位置/旋转控制** | 自动 | 可选 snap / keep pose |
| **整体开关联动** | ✅ 是（开关联动所有从 outfit scatter 出的对象）| ❌ 否 |
| **典型场景** | 多骨骼服装（衣服、头饰、尾巴）| 单点小物件（发卡、手持物）|

**核心区别**：
- Bone Proxy 用 Humanoid 角色匹配 → 可制作**跨 Avatar 通用**的 Prefab
- Merge Armature 智能合并 → 用户用任何动画开关联动**整组**散落对象

#### 9.3.9 Things to Avoid（创作者避坑必读）

##### 雷区 1：PhysBones on humanoid bones

**问题**：很多衣服的 PhysBone 组件是**复制自素体**未删除，落在 Hips/Chest 等 humanoid 骨骼上。

**后果**：MA 会**试图删除**这些 PhysBone → 行为不可预测。

**避坑方法**：
- 确保 PhysBone 组件在 **Merge Armature 范围外**的 GameObject 上
- 或者用 PhysBone 在衣服**独有**骨骼上

##### 雷区 2：完全相同的骨骼名 + 完全相同的 Armature 名

**问题**：衣服的 Armature GameObject 和所有骨骼都和素体**完全同名** → 触发 Unity 已知 bug。

**MA 兜底机制**：Setup Outfit 会给 Armature 加 `.1` 后缀回避。

**创作者应做**：**从一开始**就改名 Armature 或 Hips，避免触发 bug 兜底逻辑。

##### 其他注意事项

| 事项 | 建议 |
|------|------|
| A-pose / T-pose 不一致 | ⚠️ 手臂长度必须**完全相同**才能转换；长度不同 → 转换被跳过 |
| 不同骨骼轴向 | X/Y/Z 任意，**Merge Armature 自动处理** |
| Armature 对象名 | 任意都行，**不强制**叫 Armature |

#### 9.3.10 Preset 增强组件清单

如果做 **Modular Avatar Preset**（预先跑 Setup Outfit），可加这些增强组件：

| 组件 | 用途 | 关键点 |
|------|------|--------|
| **Blendshape Sync** | 同步体型形态键 | 胸部大小等跨服装同步 |
| **Shape Changer** | 缩/藏被衣服遮挡的身体部位 | 响应 Object Toggle + 动画；**always-enabled 时直接删多边形**（性能最优）|
| **Object Toggle** | 菜单开关物件 | 详见 [§6 教程 3](#六教程-3-简单对象开关) |
| **Menu Item Grouping** | 把多个 Toggle 合并为子菜单 | 父对象 = Sub Menu，子级 = Toggle |

**子菜单组织示例**：
```
Outfit (Root)
├─ TopToggle (MA Object Toggle + MA Menu Item)
├─ BottomToggle (MA Object Toggle + MA Menu Item)
└─ SubMenu (MA Menu Item, Type=Sub Menu) ← 作为"上衣"父菜单
   ├─ ShirtToggle
   └─ JacketToggle
```

详见 [§7.10 Blendshape Sync](#710-blendshape-sync-) / [§7.5 Shape Changer](#75-shape-changer-) / [§7.4 Object Toggle](#74-object-toggle-)。

#### 9.3.11 NDMF 生态执行顺序

**正确的执行顺序**（**不按此顺序会出错**）：

```
1. 所有 NDMF 优化工具（AAO、Meshia 等）
2. Fury
3. MA + 其他新内容 NDMF 工具
```

**为什么这样**：
- NDMF 优化工具改 Mesh → 必须先于一切合并
- Fury 的换装逻辑需要先于 MA 注入
- MA 是"最后一棒"——把所有组件翻译成最终 Avatar

#### 9.3.12 创作者向 3 种调试方法

| 方法 | 操作 | 适用场景 |
|------|------|---------|
| **Edit mode sync** | Setup Outfit 后**旋转基骨骼**，看衣服是否跟随 | 快速肉眼验证（无需进 Play） |
| **Testing in play mode** | Play 模式下 MA 自动合并 Avatar；推荐 **Avatar 3.0 Emulator** 或 **Gesture Manager** 验证菜单 | 接近上传的最终效果 |
| **Manual Bake** | 右键 Avatar → `Modular Avatar → Manual Bake Avatar`，生成 Avatar 克隆 | 调试 + 导出到其他工具（如 UniVRM） |

**最短诊断路径**：
```
玩家反馈"装上衣服不动"
  ↓
创作者先做 Edit mode sync → 转素体 Hip 验证
  ↓ 失败
Play 模式（Avatar 3.0 Emulator）
  ↓ 还失败
Manual Bake 一次性看最终结果
```

#### 9.3.13 创作者 SOP（标准操作流程）

```
1. 检查骨骼命名：OutfitRoot → [任意名] → Hips 含素体 Hips 名
2. 拖到任意素体 → Setup Outfit → Play 模式验证
3. 检查 PhysBone：确保不在 humanoid 骨骼上（移到 Merge Armature 外）
4. Armature 或 Hips 至少一个改名 → 避开 Unity bug
5. 决定做 Compatible 还是 Preset
6. Preset：加 Blendshape Sync + Shape Changer + Object Toggle + Menu Installer
7. Logo 决策：Preset 才能用 Logo；按 §9.3.5 合规使用
8. 引导用户装官方版 MA（不要夹带）
9. 版本号：遵守 Semantic Versioning；用 Internal 参数防冲突
```

### 9.4 NDMF 扩展（高级）

```csharp
[assembly: ExportsPlugin(typeof(MyPlugin))]
namespace nadena.dev.ndmf.sample
{
    public class MyPlugin : Plugin<MyPlugin>
    {
        protected override void Configure()
        {
            InPhase(BuildPhase.Generating)
                .BeforePlugin("nadena.dev.modular-avatar")
                .Run("Do something", ctx => { /* ... */ });
        }
    }
}
```

**提示**：NDMF 内部 API 不稳定，仅主版本"nadena.dev.modular-avatar"稳定。

### 9.5 实验性功能 
> 来源：[Experimental features](https://modular-avatar.nadena.dev/docs/experimental-features) + [Resonite support](https://modular-avatar.nadena.dev/docs/experimental-features/resonite-support) + [Portable Avatar Components](https://modular-avatar.nadena.dev/docs/experimental-features/portable-avatar-components)

⚠️ 实验性功能可能在未来版本以**不向后兼容**方式变化。

**当前实验**：
- **Resonite 支持**：构建 Resonite Avatar
- **Portable Avatar Components**：跨平台 Avatar 组件

**启用流程**：
```
1. 装最新 beta 版 MA + NDMF
2. Unity 菜单栏:Tools → NDM Framework → Experimental Features
3. 在弹出窗口勾选需要的实验性功能
```

⚠️ **必须使用 beta 版 NDMF/MA**才能看到这些开关。

---

#### 9.5.1 Resonite 支持（实验性）⭐完整

##### 9.5.1.1 安装 Resonite 支持包

⚠️ Resonite 支持**不是默认 MA 包的一部分**——需独立安装：

```
步骤 1: VCC → Manage Project → 点 + 添加 "Modular Avatar - Resonite support"
步骤 2: 点 APPLY
步骤 3: Unity 菜单栏 Tools → NDM Framework → NDMF Console
步骤 4: 顶部选 Avatar
步骤 5: 底部 "Avatar platform" 选 "Resonite"
步骤 6: 点 Build
  └─ 成功时底部显示 "Build finished!"
  └─ 失败时:看 Console tab 找红色感叹号
```

##### 9.5.1.2 Resonite Avatar Features 支持矩阵

| 功能 | 状态 | 备注 |
|------|------|------|
| Avatar viewpoint | ✅ | 无限制 |
| Visemes | ⚠️ Partial | **仅支持 Blendshape visemes** |
| Dynamic bones | ⚠️ Partial | 见下方"Dynamic Bones 转换规则" |
| Reactive Components | ⌛ Planned | - |
| Unity Constraints | ⌛ Planned | - |
| 半加载 Avatar 防护 | ✅ | - |

##### 9.5.1.3 Resonite MA 组件支持矩阵（完整）

| 组件 | 支持状态 |
|------|---------|
| Bone Proxy | ✅ 已支持 |
| Merge Armature | ✅ 已支持 |
| Move Independently | ✅ 已支持 |
| Physbone Blocker | ✅ 已支持 |
| Replace Object | ✅ 已支持 |
| Remove Vertex Color | ✅ 已支持 |
| Scale Adjuster | ✅ 已支持 |
| Convert Constraints | ✖ **VRChat only** |
| Merge Animator | ✖ **VRChat only** |
| Merge Blend Tree | ✖ **VRChat only** |
| MMD Layer Control | ✖ **VRChat only** |
| Sync Parameter Sequence | ✖ **VRChat only** |
| VRChat Settings | ✖ **VRChat only** |
| Blendshape Sync | ⌛ Planned |
| Menu Group / Install Target / Installer / Item | ⌛ Planned |
| Mesh Settings | ⌛ Planned |
| Parameters | ⌛ Planned（将转为 Dynamic Variables） |
| Visible Head Accessory | ⌛ Planned |
| World Fixed Object | ⌛ Planned |
| World Scale Object | ⌛ Planned |

##### 9.5.1.4 Dynamic Bones 转换规则

**自动检测源**：
- Portable Dynamic Bones（NDMF 跨平台版）
- VRChat PhysBones

**自动转换为** Resonite dynamic bones（含 colliders）

**转换的配置项**（**有限**）：
- ✅ exclusions（包括 Physbone Blockers）
- ✅ colliders
- ✅ collision radius
- ✅ grabbability

**不转换的配置项**：
- ❌ 大多数其他参数（Inertia、Stiffness 等会按"命名 templates"归类）

**Templates 命名规则**（自动按骨骼名分组）：
- skirt
- breast
- hair
- long_hair
- ear
- tail
- generic

**同 template 的 dynamic bone 共享设置**：
- Inertia
- InertiaForce
- Damping
- Elasticity
- Stiffness

##### 9.5.1.5 MA Settings Copier（设置复制器）

**用途**：在 Resonite 中**跨 Avatar 版本复制设置**。

**复制范围**：`Avatar Settings` 槽下**所有子 Slot**。

**使用流程**：
```
步骤 1: 戴上旧 Avatar
步骤 2: 用激光拾取新 Avatar
步骤 3: 右键菜单 → MA Settings Copier → Copy To Avatar
```

**前置条件**：
- 必须在 `Avatar Settings` 槽下放设置（不能放别处）
- 旧 Avatar 和新 Avatar 必须都已加载到 Resonite

##### 9.5.1.6 Resonite 安装到游戏的方式

Build 完成后有 2 种安装方式：

| 方式 | 步骤 | 适用场景 |
|------|------|---------|
| **Copy to Clipboard** | 点 NDMF Console 按钮 → 在 Resonite Dash 菜单选 "Paste content from clipboard" | 临时测试 |
| **Save as...** | 保存为 Resonite Package 文件 → 拖入 Resonite | 长期使用 / 分发 |

##### 9.5.1.7 Resonite 警告与限制

> ⚠️ "**项目正在重开发**——API 与存档**不保证兼容**"（官方原话）
> ⚠️ 反馈/Bug 需到独立仓库 `bdunderscore/modular-avatar-resonite` 的 GitHub Issues
> ⚠️ Dynamic Variable 命名与值将来可能变化（如 `modular_avatar/MeshNotLoaded`、`modular_avatar/HumanBone.*`）

**教学要点**：
- 99% 玩家**不需要** Resonite 支持
- 只在玩家**明确要做 Resonite Avatar** 时教
- **强调"实验性"**——别让玩家把它当生产工具

---

#### 9.5.2 Portable Avatar Components（实验性）

**定位**：NDMF 提供的**不依赖具体平台 SDK**（如 VRCSDK）的 Avatar 组件，用于构建**跨平台** Avatar。

##### 9.5.2.1 最小可用配置（3 个组件）

```
步骤 1: Avatar 根挂载 NDMFAvatarRoot（必需）
步骤 2: 在视点位置创建空 GameObject → 挂载 NDMF Viewpoint（推荐放根）
步骤 3: 若 Avatar 用 Blendshape visemes 嘴型 → 挂载 NDMF Blendshape Visemes
  └─ 配置面部 mesh 与 viseme blendshape
```

##### 9.5.2.2 Portable Dynamic Bones

**用途**：在不依赖特定 SDK 的前提下，标记骨骼为物理模拟。

**特点**：
- 只配置**跨平台共有**的最小属性集
- 具体行为由 "settings template" 名称控制
- 平台层可做特定配置覆盖

**优先级规则**：
- 同一骨骼根 transform 上**同时存在** portable + 平台特定 dynamic bone 组件
- → **平台特定组件优先**

⚠️ **尚未完全可用**——能用，但**未来极有可能不兼容地变更**（官方警告）。

##### 9.5.2.3 教学要点

- 99% 玩家**不需要** Portable Avatar Components
- 这是为**未来跨平台 Avatar 工具链**打基础的实验性功能
- **不要教玩家现在使用**——除非他们明确要"做跨平台 Avatar 工具"

### 9.6 Samples 实战案例（Fingerpen + Clap 拆解）
> 来源: [官方 Samples 页面](https://modular-avatar.nadena.dev/docs/samples)
> **定位**: 与 §6 教程 1-6 的"从零搭建"互补——本节是"**现成 Prefab 拆解**"型教学素材
> **核心目标**: 让玩家**看懂一个完整的 MA 小组件长什么样**,而不必从零造
> **位置**: `Packages → Modular Avatar → Samples`

#### 9.6.1 Samples 是什么 / 为什么只有 2 个

**官方在 MA 包里塞了 2 个示范 Prefab**：

| Prefab | 名字 | 教学定位 | 演示了哪些组件 |
|--------|------|---------|---------------|
| **Fingerpen** | 指间笔 | **MA 组件全家福迷你版** | Merge Animator + 自动 Synced Parameters + Menu Installer + Bone Proxy |
| **Clap** | 拍手 | **避坑教学（递进）** | Fingerpen 的全部 + Contact Receivers + Internal Parameters |

**为什么只有 2 个？** 这不是偷懒，是**官方精心设计的"最小教学样本"**：
- **Fingerpen = 4 个核心组件的最小集** — 让玩家"先把整头牛看一遍"
- **Clap = 1 个新知识点（参数冲突）+ 物理交互（Contact）** — 在 Fingerpen 之上递进

**核心学习路径**：玩 Fingerpen（拖一下能用）→ 拆 Fingerpen（看内部组件）→ 玩 Clap（多了一个功能）→ 拆 Clap（看参数怎么防冲突）→ **认知模型升级**为"我能看穿任何 MA 小组件的结构"

#### 9.6.2 Fingerpen（指间笔）拆解

**这个 Prefab 内部大概长什么样**：

> **简单说**：层级就是 Unity 左侧那棵树状图,每个东西是一个 GameObject,相当于一个文件夹或一个物体。

```
Fingerpen  (根对象)
├── Armature（或直接挂 Mesh）
│   └── HandRef            ← 这里有个 MA Bone Proxy 组件
│       └── PenMesh         ← 笔的 3D 模型
├── Animator Controller    ← 一个动画控制器(不在层级里,在 Project 窗口)
├── MenuInstaller          ← 顶层对象,带 "Select Menu" 按钮的那个
└── Parameters            ← MA Parameters 组件,登记参数用的
```

**玩家不需要现在就懂每个名字**。只需知道：Prefab 里有 **一个笔的模型**、**几块挂在上面的"配置说明牌"(MA 组件)**、还有一个**让笔能动起来的动画控制器**。

**三个核心教学点("玩 + 拆"两阶段)**：

**教学点 1: 拖入 = 完成 80% 的工作**

| 阶段 | 玩家做什么 | 看到什么 |
|------|----------|---------|
| 玩 | 把 Fingerpen Prefab 拖到 Avatar 子级 | 完事了,笔已经能用 |
| 拆 | 看 Fingerpen 根对象 | 一串 MA 组件（Merge Animator、Menu Installer、Parameters 等） |
| 思 | 官方为什么敢让玩家**只拖一下**？ | 因为"配置说明牌"都已经在 Prefab 里写好了 — MA 设计核心承诺：**让卖 Prefab 的人把所有复杂配置都封装好,买的人零配置上手** |

**教学点 2: Select Menu 按钮 = "菜单装到哪"的开关**

```
步骤:
1. 选中 Fingerpen 根对象 → 右侧 Inspector（简单说:就是 Unity 右侧那块显示所有"说明书"的区域）
2. 找到 MA Menu Installer 组件
3. 点 "Select Menu" 按钮
4. 弹出窗口:双击你想把笔的开关装进哪个菜单（默认是 Avatar 顶级菜单）
5. 上传 VRChat 后,菜单里就有 "Fingerpen On/Off" 这一项了
```

**为什么需要"选菜单"**：VRChat 玩家的菜单**格子数有上限**(256 个参数限额的一部分)。`MA Menu Installer` 让你**自己决定**这支笔的开关装在主菜单还是某个子菜单,灵活但不强制。

**教学点 3: Bone Proxy = "笔自动挂到手指上"**

| 阶段 | 玩家做什么 | 看到什么 |
|------|----------|---------|
| 玩 | 进 Play 模式 → 把 Avatar 的右手手指合拢 | 笔出现在指间 → 跟着手指一起动 |
| 拆 | 打开 Fingerpen 的子对象,找 `HandRef` 这个空对象（简单说:就是个看不见的"挂载点"） | 上面有个 MA Bone Proxy 组件,`Target` 字段拖的是"Avatar 的右手手指骨头" |
| 思 | MA 在编译时把这个挂载点**重新连接**到 Avatar 上对应的手指骨头 — 不管是哪个 Avatar,只要它有手指骨头,笔就挂上去 | **avatar-agnostic**(与 Avatar 无关):同一个笔 Prefab,能用在任何有手指的 Avatar 上 |

**Bone Proxy 详细机制**（高级叙述）：
- 通过 humanoid bone + 相对路径引用
- Prefab 保存时会自动转译
- `Attachment Mode` 有 `As child at root`(位置归零,通用 Prefab)和 `As child keep world pose`(保留世界位置,Avatar 专用)
- 详见 [§7.6 Bone Proxy](#76-bone-proxy)

**动手复刻一个简化版（5 步）**：

> 假设玩家**完全没有 Unity 经验**

```
Step 1: 准备
  - 需要:一个能进 Play 模式的 Avatar 工程
  - 没有的话:先按 vrnavi / vrcmaster 教程装好 Unity + VCC + MA + 一个测试 Avatar

Step 2: 拿到 Fingerpen
  - Project 窗口 → Packages → Modular Avatar → Samples → Fingerpen
  - (如果看不到,说明 MA 没正确导入,回头检查)

Step 3: 拖上去
  - 把 Fingerpen Prefab 拖到 Hierarchy 里 Avatar 的子级
  - ⚠️ 不要拖到场景根目录,要拖到 Avatar 里面

Step 4: 选菜单
  - 选中 Fingerpen 根对象
  - 在 Inspector 找到 MA Menu Installer
  - 点 "Select Menu" → 双击你想用的菜单(默认即可)
  - 看到 Selected Menu 字段显示菜单名 = 成功

Step 5: 验证
  - 点 Unity 上方 ▶ Play 按钮
  - 在 Game 视图你应该看到笔已经挂在手指上
  - 上传 VRChat 之前这一步不算完,但你能确认 Prefab 内部没坏
```

**易错点(这一步最容易卡哪里)**：

| 现象 | 原因 | 修复 |
|------|------|------|
| Project 窗口找不到 Fingerpen | MA 没装 / 没启用 Samples | 装 MA 后,在 Project 搜索框输入 `Fingerpen` 试 |
| 拖进去笔位置不对 | 没拖到 Avatar 子级 | 删掉,重新拖到 Avatar 下面 |
| 笔在场景里但不跟手 | 没进 Play 模式 | 点 ▶ Play |
| 选菜单没反应 | Avatar 没有菜单结构 | 确认 Avatar 上有 VRC Avatar Descriptor 组件 |

#### 9.6.3 Clap（拍手）拆解

**什么是"拍手"——先解释 Contact Receiver**：

> **完全没听过 Contact Receiver？** 先理解场景：在 VRChat 里,你把双手合拢的时候,Avatar 之间会发生"接触"。VRChat 系统能检测到这种接触事件（简单说:你的两只手"撞"到一起了）。MA 的 **Contact Receiver**（接触接收器）就是用来"接收这种接触事件"的组件。

**打个比方**：你家有个**门铃按钮**（Contact Sender,按下去会响）和一个**门铃接收器**（Contact Receiver,听到响声就知道有人按）。拍手这里,**两只手互相撞就是"按门铃",拍手 Prefab 里那个接收器听到响声后,就触发拍手音效和粒子**。

**所以"拍手"在 VRChat 里的真实含义**：两只手的位置在空间里**接近到一定距离**,且**接近的速度够快**——这样才会被判定为"拍手"（而不是"缓慢合掌"）。

**Clap Prefab 内部比 Fingerpen 多了什么**：

```
Clap  (根对象)
├── ... (和 Fingerpen 一样的所有组件)
├── ContactReceiver ← 多出来的！监听"拍手"事件
├── AudioSource     ← 拍手音效播放器
└── ParticleSystem  ← 拍手粒子效果
```

**关键不同**：Clap Prefab 里**多了一个 MA Parameters 组件 + 多个 Contact Receiver**,每个 Receiver 监听不同的身体接触(比如左手碰右手、左手碰头、右手碰头……)

**核心教学点:为什么必须用 Internal Parameters**

**问题场景(玩家角度的"为什么")**：

> 你装了 Clap,又装了个别人做的"心跳特效",**两个小组件都用了同一个参数名**——比如都叫 `On`。VRChat 的菜单系统会**报错或行为异常**:菜单里只有一个开关,但控制的是哪个组件说不清。

**没勾 Internal 时的痛**：你的 Avatar 上现在有 2 个叫 `On` 的参数,VRChat **不让这么干**(参数限额 + 命名冲突)。

**Internal Parameters 怎么解决**：

> 看 Clap 的 Inspector → MA Parameters 组件。每个参数旁边有一个 **Internal 复选框**。**勾上**的意思是:
>
> "这个参数是我们组件**内部用**的,MA 帮我在生成 Avatar 时**自动改名**(比如 `On` → `_On_internal_1`),让它**永远不会**和别人冲突。"

**对玩家的含义**：
- 不需要手动想参数名
- 不需要担心和别人组件打架
- MA 在编译时**自动改名 + 自动把组件内部引用同步到新名字**
- **99% 的情况下,Internal 应该勾上**——这是 MA 设计的"无脑安全默认"

**用具体场景展示**：

| 同时装了 3 个小组件 | 没勾 Internal 时 | 都勾 Internal 时 |
|------------------|----------------|----------------|
| Fingerpen（用 `On`） | 3 个组件都往 VRChat 菜单塞 `On` 开关 | MA 自动给每个 `On` 起不同内部名字 |
| Clap（用 `On`） | 菜单里只有 1 个 `On` | 菜单里有 3 个独立开关 |
| 别人的发型切换（用 `On`） | 按下去 3 个东西同时切换,**一团乱** | 各自管各自的东西 |

**三个核心教学点("玩 + 拆"两阶段)**：

**教学点 1: 拍手 = 物理交互触发**

| 阶段 | 玩家做什么 | 看到什么 |
|------|----------|---------|
| 玩 | 进 VRChat → 双手快速合拢 | 听到"啪"一声 + 看到粒子 |
| 拆 | Clap 的工作链路 | Contact Receiver 检测接触 → 触发 Animator 参数 → Animator 播放音效和粒子动画 |
| 思 | 和 Fingerpen 用菜单开关的"主动控制"不同,Clap 是**物理事件驱动**的 | 你的身体动作就是"按钮" |

**教学点 2: 所有 Fingerpen 的教学点全部适用**

> Clap 在 Fingerpen 之上,**没改任何 Fingerpen 教的结构**——只是**额外加了** Contact Receiver 和 Internal Parameters。这就是 MA 的"组件叠加"哲学:**功能像乐高一样往上拼,不重写底层**。

**教学点 3: Internal = 默认安全选项**

> 官方把这个 Sample 做成"所有参数都勾 Internal"的样子,是**让玩家抄作业**。你以后做任何 MA Prefab,**第一步就是把所有参数勾 Internal**,除非你有"必须和别的组件共享参数"的需求(极少见)。

**动手复刻一个简化版**：

```
Step 1-3: 跟 Fingerpen 一样(装 MA、拿到 Clap Prefab、拖到 Avatar)

Step 4: 看 Internal 勾选情况
  - 选中 Clap 根对象
  - Inspector 找到 MA Parameters 组件
  - 展开参数列表
  - 你应该看到每个参数名右边都有 Internal ✅ 复选框
  - 这就是"防冲突"的关键开关

Step 5: 选菜单 + 验证
  - 点 "Select Menu" → 双击目标菜单
  - 进 Play 模式 → 看 Prefab 正常出现
  - (拍手效果只能在 VRChat 里实测,编辑器里看不到完整效果)
```

**易错点**：
- 看不到 Internal 复选框 → MA 版本太老 → 升级 MA
- 多个 Contact Receiver 没反应 → Avatar 没启用 Contact 特性 → 检查 Avatar Descriptor 的 Contact 字段
- 装上后菜单里看不到开关 → 没选菜单,或 Menu Installer 没启用

#### 9.6.4 Samples 教学的应用指南

**何时该把玩家引到 Samples**：

| 玩家提问 | 推荐起始点 | 原因 |
|---------|----------|------|
| "MA 是什么/解决什么问题" | Samples 简介 + §1 | 先看"完成效果"再学"怎么造" |
| "怎么用别人做的 MA 小组件" | Fingerpen 拆解（§9.6.2） | 玩 + 拆两阶段 |
| "我装了多个组件参数冲突" | Clap 拆解（§9.6.3） | Internal Parameters 是核心 |
| "我想看一个 MA Prefab 内部什么样" | Samples 整体 | 唯一官方"内部样本" |
| "我完全不会 Unity" | §1 → Fingerpen 拖入 → 看效果 | **不要先教组件定义** |
| "我想自己造一个 MA Prefab" | 教程 1-6 + Samples 作参考 | 教程教搭建,Samples 作参考 |

**教法框架("先玩 → 再拆 → 最后造")**：

```
阶段 1: 玩（5 分钟）
  - 拖 Fingerpen 到 Avatar
  - 选菜单
  - 进 Play 模式看效果
  - 玩家心理: "哦,原来这么简单"

阶段 2: 拆（10 分钟）
  - 展开 Fingerpen 根对象
  - 逐一介绍 4 个核心组件
  - 强调"avatar-agnostic"和"封装"
  - 玩家心理: "哦,原来内部是这样"

阶段 3: 进阶（15 分钟）
  - 玩 Clap → 拆 Clap
  - 解释 Internal Parameters 解决参数冲突
  - 解释 Contact Receivers 的物理交互
  - 玩家心理: "哦,原来可以这样扩展"

阶段 4: 造（30+ 分钟,可选）
  - 教玩家自己从零搭一个简化版
  - 用教程 1-6 的方法
  - 玩家心理: "原来我也能造一个"
```

**4 个常见误用 Samples 的场景**：

| ❌ 错误做法 | ✅ 正确做法 |
|---------|---------|
| "MA 是一个工具,先学 25 个组件的定义" | "MA 是一个工具,先看一个能用的 Prefab 什么样" |
| "我教你写一个 Object Toggle" | "我教你装一个 Fingerpen,然后你**自己**拆开看怎么搭的" |
| "Internal Parameters 是用来节省参数限额的" | "Internal Parameters 是**让两个组件不打架**" — 用 Clash 真实场景讲 |
| "Samples 里的东西太简单,先不教" | "Samples 是**唯一官方权威**的'完整 Prefab 长什么样'参考" |

#### 9.6.5 Samples 的元学习价值

> **给 Agent 自己的元认知**: Samples 教我们的不只是 MA,还有一种**"用现成 Prefab 教学"的方法论**

| 价值维度 | 体现 | 应用到其他工具教学 |
|---------|------|------------------|
| **"看穿"能力** | 玩家能"看穿"任何 BOOTH 上卖的 MA 小组件 | 任何"组件库"型工具都可借鉴: 给一个完整 Prefab → 玩家学会看穿所有类似物 |
| **"递进式教学"** | Fingerpen → Clap,后者在前者之上 +1 个知识点 | 不要写 5 个并列例子,要写"在 N 之上 +1"的递进链 |
| **"展示完成效果 > 展示制作过程"** | 玩家先看能用的东西,再拆内部 | 入门阶段先给"能用的成品",拆解阶段再讲"怎么搭" |
| **"官方文档三层结构"** | 展示效果(Samples)→ 展示搭建(教程)→ 展示组件(Reference) | 任何工具文档都应分这三层,新手从第一层进入 |

#### 9.6.6 关联知识

- **§6 教程 1-6**: 从零搭建,5-10 步 / 教程
- **§7 组件速查**: 25+ 组件的 When/How/Limitations
- **§5 Reactive 系统**: 为什么 Internal Parameters + Contact Receiver 能"链式工作"
- **§7.2 Merge Animator**: Fingerpen 的核心组件详解
- **§7.6 Bone Proxy**: Fingerpen 把笔挂到手指上的机制
- **§7.9 Menu Installer**: 选菜单按钮的实现
- **§14 MMD 教学法**: Samples 在 MMD World 中的行为(MA 默认保护 Merge Animator 层)

---

## 10. 与 NDMF 生态协作

| 工具 | 用途 | 配合 |
|------|------|------|
| **Avatar Optimizer (AAO)** | 性能优化 | 装在 MA 之前 |
| **Meshia Mesh Simplification** | 网格简化（推荐，替代已废弃的 lilNDMFMeshSimplifier） | 装在 MA 之前 |
| **Cascading Avatar Mesh Simplifier** | 级联简化 | 装在 MA 之前 |
| **Mantis LOD Editor NDMF** | LOD 编辑 | 装在 MA 之前 |
| **EasyQuestSwitch** | PC/Quest 切换 | 任意顺序 |
| **VRCFury** | 老式换装 | **注意顺序冲突** |

**VRCFury 共存警告**：
- 两者互不感知
- 执行顺序错会出 bug
- 推荐：NDMF 优化 → Fury → MA/NDMF 新内容

---

## 11. 教学决策树（速查）

玩家提问时,如何快速定位教学起点？

```
玩家问题
├─ "刚买了个衣服,怎么装？"
│   └─ → 教程 1 (配置简单服装)
│
├─ "装上了但和身体穿模"
│   └─ → 教程 4 (高级开关: Shape Changer)
│
├─ "想加个开关菜单"
│   └─ → 教程 3 (简单对象开关)
│
├─ "想让 Avatar 跟视频/音频互动"
│   └─ → 教程 6 (Merge Animator) + Samples (§9.6 Fingerpen)
│
├─ "装了多个小组件,菜单打架/参数冲突"
│   └─ → MA Parameters (§7.3) + Samples (§9.6 Clap, Internal 复选框)
│
├─ "我想看一个 MA 小组件内部什么样"
│   └─ → Samples (Fingerpen + Clap) 拆解 (§9.6)
│
├─ "我想做自己的衣服卖给别人"
│   └─ → §9.3 创作者向完整版（必读）
│       + §9.3.6 决定做 Compatible 还是 Preset
│       + §9.3.13 SOP 标准操作流程
│       + Logo 决策：见 §9.3.5 合规清单
│
├─ "我做了衣服但玩家反馈装上不动"
│   └─ → §9.3.12 创作者向调试方法（Edit sync / Play / Manual Bake）
│
├─ "我做的衣服能不能用 MA Logo？"
│   └─ → §9.3.5 Logo 使用决策表
│
├─ "我想做跨 Avatar 通用的小组件（发卡/手持物）"
│   └─ → §9.3.8 Bone Proxy vs Merge Armature 决策表
│
├─ "我的 Prefab 升级 MA 后坏了"
│   └─ → §9.3.4 版本策略（Semantic Versioning + 稳定 API）
│
├─ "我想用 MA 内部 API 写插件"
│   └─ → §9.3.4 API 稳定性表（"nadena.dev.modular-avatar" 是唯一稳定 API）
│
├─ "装上鞋子陷地了"
│   └─ → Floor Adjuster (§7 组件 5)
│
├─ "多个小组件参数冲突了"
│   └─ → MA Parameters (§7 组件 3)
│
├─ "调体型时衣服不变"
│   └─ → Blendshape Sync (§7 组件 10)
│
├─ "VRChat 看着错,编辑器正常"
│   └─ → Manual Bake Avatar + 错误窗口
│
├─ "我完全不会 Unity"
│   └─ → 先学基础: VRChat 官方教程 + 教程 1
│
├─ "我在 MMD 跳舞世界表情不对"
│   └─ → §14.3 场景 A（先确认 World 行为）
│
├─ "MMD Layer Control 装上了没生效/build 失败"
│   └─ → §14.3 场景 B（检查装到 layer 还是 state）
│
├─ "我的小组件在 MMD 世界不工作了"
│   └─ → §14.3 场景 C（默认保护，可能正是想要的）
│
└─ "我想完全关掉 MMD 处理"
    └─ → §7.16 VRChat Settings + 关掉 MMD World Support
```

---

## 12. 文档结构参考

| 知识类别 | 文档位置 | 状态 |
|---------|---------|------|
| **官方教程** | `memory/avatar/modular-avatar.md`（本文）§6 | ✅ |
| **组件参考** | `memory/avatar/modular-avatar.md` §7 | ✅ |
| **反应式系统** | `memory/avatar/modular-avatar.md` §5 | ✅ |
| **高级话题** | `memory/avatar/modular-avatar.md` §9 | ✅ |
| **Samples 实战** | `memory/avatar/modular-avatar.md`（本文）§9.6 | |
| **教学法** | `memory/avatar/teaching-methodology.md` | ✅ |
| **教学法（MA 专项）** | `memory/avatar/modular-avatar.md` §4 | ✅（本文）|
| **创作者向完整版** | `memory/avatar/modular-avatar.md` §9.3 | |

---

## 13. 教学语言风格

**默认玩家**：无 / 少量 Unity 基础

### 13.1 简单叙述（默认）

```
✅ "把衣服拖到 Avatar 身上"
✅ "右键选 Setup Outfit"
✅ "如果没动,可能是 X"
❌ "执行 NDMF 编译管线"
❌ "调用 Merge Armature 组件的 merge 流程"
```

### 13.2 专业叙述（高级玩家用）

```
✅ "NDMF 在 Generating 阶段执行 Merge Armature pass"
✅ "Layer Priority 控制 Animator 合并顺序"
✅ "Write Defaults 匹配避免混用 ON/OFF 状态"
```

### 13.3 转换触发条件

当玩家说出这些词时,可以切换到专业叙述：
- "Animator Layer"
- "Write Defaults"
- "Blend Tree"
- "NDMF"
- "Constraint"
- "Expression Parameter"
- "PhysBone"

---

## 14. MMD World 玩家教学法

> 适用对象：默认玩家**不知道 MMD World 是什么**
> 来源：综合官方文档 + 玩家教学经验

### 14.1 什么是 MMD World（一句话给玩家）

```
MMD World 是 VRChat 里一类特殊的世界（通常带音乐和舞蹈），
它们会**自动接管**你的表情控制，让所有 Avatar 的表情同步成它们的舞蹈动作。
```

**为什么玩家需要知道这个**：
- 90% 玩家**永远不需要关心** MMD World（这是给"会去 MMD 世界的玩家"的进阶知识）
- 只有 5% 的玩家会因为"我装了 MMD Layer Control 但没生效"或"我在 MMD 世界的表情不对"来问
- 教学优先级：**低**。**不要主动教**。

### 14.2 三种玩家提问场景

| 玩家提问 | 实际意思 | 教学起点 |
|---------|---------|---------|
| "我去 MMD 跳舞世界表情不对" | 可能 MMD World 想禁的表情没禁 | §14.3 场景 A |
| "我的小组件装了 MMD Layer Control 没生效" | 可能装错位置（装到 state 而不是 layer） | §14.3 场景 B |
| "我装了个小组件，进 MMD 世界后它的动画不播了" | 用了 Merge Animator，MA 默认保护 | §14.3 场景 C |

### 14.3 三种场景的回应（5 步诊断法）

**场景 A：MMD World 表情不对**

```
玩家："我去 MMD 跳舞世界，表情没被禁掉，看着很怪"

诊断步骤：
1. 问玩家：哪个 MMD World？（不同 World 行为不同）
2. 解释：这个 World 是禁层 2&3 来禁表情的
3. 让玩家检查：Avatar 是否有层 2、3 是表情控制？
   - 如果玩家不知道怎么查 → 教"打开 Animator 窗口，看 FX 层 2 和 3 名字"
4. 99% 情况：玩家根本没用层 2、3 做表情，所以 World 禁不掉
5. 解决方案：要么 World 作者修复，要么换 World

✅ 不要说："执行 MMD Layer Control" —— 99% 玩家不需要这个
✅ 不要让玩家"加 MMD Layer Control"——玩家没在层 2、3 加东西，加了也没用
```

**场景 B：MMD Layer Control 装错位置**

```
玩家："我按教程加了 MMD Layer Control，没效果，还 build 失败"

诊断步骤：
1. 让玩家截图：组件在 Hierarchy 哪里？
2. 检查点：组件是不是装到 **state**（Animator 里的状态）而不是 **layer**（整个层）？
3. 解释："必须直接装到 layer，不能装到里面的 state"
4. 修复：右键 layer 标题 → Add Behavior → MMD Layer Control
5. 重新 build

✅ 关键句："layer 是大盒子，state 是盒子里的小球。你要把组件放到大盒子上，不是小球上"
```

**场景 C：Merge Animator 在 MMD 世界失效**

```
玩家："我装了个小组件，进 MMD World 它的动画不播了"

诊断步骤：
1. 问玩家：小组件用什么组件做的？（很可能是 Merge Animator）
2. 解释："MA 默认**保护** Merge Animator 添加的层，**不让** MMD World 禁"
3. 这就是为什么你的小组件在 MMD World 里**还在动**——MA 帮你保住了
4. 如果你**希望**它被 MMD 禁掉 → 加 MMD Layer Control（注意装对位置）
5. 如果你**不希望**它被 MMD 禁掉 → 什么都不用做，已经是对的

✅ 关键句："MA 帮你把你的小组件保护起来了。如果你想让它在 MMD World 被禁掉，加一个组件"
```

### 14.4 何时升级到专业叙述

当玩家问到这些时，可以切换到专业叙述：

| 玩家提到 | 可以升级到 |
|---------|----------|
| "FX 动画器的第 2 层和第 3 层" | 专业叙述（说明他们懂 Avatar 3.0）|
| "Animator Layer Priority" | 专业叙述（说明他们懂 Animator）|
| "Write Defaults" | 专业叙述 |
| "Relay layer / Padding layer" | 专业叙述（说明他们读 MA 文档）|
| "VRChat Settings 的 MMD World Support" | 专业叙述 |

### 14.5 玩家不需要知道的细节

> ⚠️ 教学时**主动跳过**这些（避免信息过载）：

- relay layers 具体怎么实现（MA 内部机制）
- padding layers 具体怎么插入（MA 内部机制）
- "VRChat 当前 API 不支持通用方案"（平台限制，玩家改不了）
- replace 模式下的具体行为（Merge Animator 内部细节）

### 14.6 教学决策树（MMD 相关）

```
玩家问题
├─ "完全不知道 MMD World 是什么"
│   └─ → §14.1 一句话介绍，跳过详细机制
│
├─ "我在 MMD World 表情不对"
│   └─ → §14.3 场景 A
│
├─ "MMD Layer Control 没生效/build 失败"
│   └─ → §14.3 场景 B（检查装到 layer 还是 state）
│
├─ "Merge Animator 在 MMD World 不工作了"
│   └─ → §14.3 场景 C（默认就是保护，可能正是想要的）
│
├─ "我想让小组件被 MMD 控制"
│   └─ → §14.3 场景 B + 提示装到 layer
│
└─ "我想完全关掉 MMD 处理"
    └─ → §7.16 VRChat Settings + 关掉 MMD World Support
```

### 14.7 不要这样教玩家（MMD 反例）

| ❌ 反例 | ✅ 正确 |
|---------|--------|
| "MMD World 会禁你的 layer 2 和 3" | "有些世界会接管你的表情（叫 MMD World）" |
| "MA 会加 relay layer 和 padding layer" | "MA 会自动帮你处理这些" |
| "VRChat API 不支持通用方案" | 跳过，**不要讲平台限制**（玩家改不了）|
| "这个 workaround 只对禁用 2&3 的 World 有效" | 跳过，**不要讲**，除非玩家问"那别的 World 呢" |
| "你在 Animator state machine behavior 上加错了" | "你装错了——应该装到大盒子（layer）不是小球（state）" |

---

**参考链接**：
- [Modular Avatar 官方文档](https://modular-avatar.nadena.dev/docs)
- [Modular Avatar GitHub](https://github.com/bdunderscore/modular-avatar)
- [NDMF 框架](https://github.com/bdunderscore/ndmf)
- [Samples 页面](https://modular-avatar.nadena.dev/docs/samples)
- [Reference 页面](https://modular-avatar.nadena.dev/docs/reference)
- [Experimental Features 页面](https://modular-avatar.nadena.dev/docs/experimental-features)

**相关知识库**：
- `memory/avatar/modular-avatar-tutorials-detailed.md` — 教程精读详细版（27KB）
- `memory/avatar/teaching-methodology.md` — 教学法原则
- `memory/avatar/animator-system.md` — Animator 系统
- `memory/avatar/ndmf-tools.md` — NDMF 生态
- `memory/avatar/optimization-guide.md` — 性能优化
- `memory/avatar/avatar-modding-guide.md` — 改模指南
