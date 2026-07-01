---
title: "Modular Avatar 组件教学卡（27 个完整版）"
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
  - modular-avatar
aliases:
  - "27 个完整版"
  - "Modular Avatar 组件教学卡（27 个完整版）"
related:
  - ma2bt.md
  - modular-avatar.md
  - avatar-modding-guide.md
  - lac-avatar-compressor.md
  - modular-avatar-tutorials-detailed.md
---
# Modular Avatar 组件教学卡（27 个完整版）

> 来源: [官方 Component Reference](https://modular-avatar.nadena.dev/docs/reference)
> 颗粒度: 每个组件一张"教学卡" = When / How / How it works / Limitations / 教学要点
> 与 `modular-avatar.md` §7 速查表的关系: 速查表是分类鸟瞰,本文是**逐组件精读**
> 教学目标对象: 默认玩家**没有/仅有少量 Unity + 动画器 + Avatars3 基础**

---

## 0. 卡片阅读说明

| 字段 | 含义 |
|------|------|
| **一句话** | 用一句话说清"这个组件干什么" |
| **何时用** | 来自官方 When should I use it? |
| **何时不用** | 来自官方 When shouldn't I use it? |
| **怎么用** | 3-5 步操作流程 |
| **怎么工作** | 30-50 字的"原理透明"段(官方 How does it work? 提炼) |
| **已知限制** | 来自官方 warning / caution / Limitations |
| **教学要点** | Agent 教学时的"该什么时候用 + 配合什么 + 语言风格示例" |

**难度标记**:
- ⭐ 入门(零基础也能懂)
- ⭐⭐ 进阶(需要基础 Animator 概念)
- ⭐⭐⭐ 高级(需要理解动画器参数、PhysBone、约束等)

**Reactive 标记**:
- `[R]` = Reactive Component(响应 GameObject 激活状态 + Menu Item 选中状态)

---

## 1. 核心合并三件套

### 1.1 Merge Armature ⭐⭐⭐（必学）

**一句话**: 把衣服/头饰等 Skinned Mesh 的骨骼"挂"到你的 Avatar 上,自动处理引用。

**何时用**:
- 装衣服、头饰、尾巴等所有 Skinned Mesh 配件
- 任何想"跟着 Avatar 身体动"的物件
- 衣服原本不是为你的 Avatar 设计(骨骼名不同也行)

**何时不用**:
- 想做一个**通用 Prefab** 能套到任何 Avatar 上(用 Bone Proxy)
- 手上挂个 Cube(用 Bone Proxy)
- 不同 Avatar 都能用的"通用道具"(Merge Armature 假设骨骼不动,绑死后只能用在特定 Avatar)

**怎么用**(3 步):
1. 组件加到源层级根对象
2. 拖入 Avatar 对应骨骼到 `Merge Target`
3. `Prefix`/`Suffix` 通常自动设置

**怎么工作**:
MA 遍历 GameObject 树,按名字找素体对应骨骼。找到 → 引用指向素体;找不到 → 在对应父骨骼下创建子骨骼。组件配置和动画路径会**自动修正**指向新位置(PhysBone/Contact 的 target 也会更新)。

**已知限制**:
- ⚠️ 不要在素体**通用**骨骼(如 Hips、Chest)上放 PhysBone —— MA 会尝试删除,行为不可预测
- ⚠️ 避免和素体**完全相同**的骨骼名(会触发 Unity bug)
- 📌 1.7.0+ 支持嵌套 merge(A→B→C)
- 📌 `Reset position to base avatar` 提供"Do It!"+ 4 个选项(Also set rotation / local scale / Adjust outfit overall scale / 默认复位)
- 📌 Object references 是 **path reference**(内部实现),所以 Prefab 保存后 Merge Target 能**自动恢复**(不用担心断开)

**Setup Outfit 自动化**(右键菜单):
- 自动找衣服的 Hips(名字要包含素体 Hips 名字)
- 自动 T-Pose / A-Pose 转换(手臂位置不同时)
- 自动创建 Mesh Settings

**Position Lock 模式**:

| 模式 | 行为 | 何时用 |
|------|------|--------|
| Not locked | 编辑模式不跟随 | 几乎不用 |
| Base → Target(单向) | 素体动 → 衣服跟 | **默认**,日常用 |
| Base ↔ Target(双向) | 互相跟 | 高级场景(如动素体头发) |

**匹配骨骼名失败**:
- 点 `Adjust bone names to match target` 让 MA 改名
- `Avoid name collisions` 默认勾选,自动给新骨骼加后缀(避免与其他装备冲突)

**教学要点**:
- 🎯 玩家第一次学改模 **90% 都是用这个**
- 🎯 教程 1 = 教学范本
- 🎯 教学时强调"右键 → Setup Outfit 一键搞定"
- 🎯 已知限制必须提前说,**否则玩家买了衣服穿不上,会以为 MA 有 bug**
- 💬 语言示例(零基础): "把衣服当成'裁缝的样板',MA 就是'自动裁缝'——你只要把样板和身体对上,它就帮你把衣服缝上去"
- 💬 语言示例(高级): "Merge Armature 通过 Bone Name + Prefix/Suffix 匹配策略,使用 SkinnedMeshRenderer.rootBone 重写 + 骨骼对象再父化实现 Just Work"

---

### 1.2 Merge Animator ⭐⭐

**一句话**: 把小组件的 Animator 合并到 Avatar 指定层(FX/Action/Gesture/Base/Additive)。

**何时用**:
- 任何带 Animator 的小组件(手拍效果、笔道具)
- 想"拖到 Avatar 上就播动画"
- 跟 Merge Armature 配合(衣服带动态效果)

**何时不用**:
- 想**完全替换** Avatar 原本的 Animator 层(用 Replace 模式可以,但要小心)
- 简单开/关(用 Object Toggle)

**怎么用**(5 步):
1. 组件加到 Prefab 对象
2. `Animator to merge` 拖入 Animator Controller
3. `Layer Type` 选层(FX / Action / Gesture 等)
4. (推荐)勾上 `delete attached animator`(让 Unity 允许录制)
5. (推荐)勾上 `match avatar write defaults`(避免 WD 混用)

**怎么工作**:
MA 把你的 Animator 按优先级合并到目标层。Path Mode = Relative 时,所有路径相对于 Merge Animator 组件本身(便于录制);Absolute 时用绝对路径(便于引用 Avatar 已存在对象)。

**Path Mode**:

| 模式 | 行为 | 何时用 |
|------|------|--------|
| Relative | 路径相对 Merge Animator 组件 | 通用 Prefab(推荐) |
| Absolute | 路径绝对 | 引用 Avatar 上原本就有的对象 |

**Layer Priority**:
- 数字小 → 先应用
- 数字大 → 后应用(覆盖)
- 同优先级按 Hierarchy 顺序

**Merge Mode**:
- `Add`(默认): 追加层
- `Replace Existing Animator`: 替换层(同层多个 Replace 会**报错**)

**Write Defaults 匹配**:
- 自动检测 Avatar 用 WD ON 还是 OFF
- 调整你的动画器以匹配
- 混用会出 bug(状态卡住不恢复)

**已知限制**:
- ⚠️ VRCAnimatorLayerControl 只能引用**同一 Animator 内的层**,**跨 Animator 引用不支持**(例如你的 FX 里的 VRCAnimatorLayerControl 不能指向 Gesture 层的索引)
- 📌 `Playable` 字段 = Merge Animator 的层
- 📌 `Layer` 字段 = 你动画器内的层索引

**Humanoid Bone 动画**:
- 移动 Humanoid 骨骼的动画**忽略 Relative Path**
- 永远应用到整个 Avatar
- AFK 动画可以**直接用**

**录制动画**:
- 在**同一 GameObject** 上加 Animator 组件(让 Unity 允许录制)
- Animation 窗口(Ctrl+6)录制,路径自动相对
- 勾 `Delete attached animator` → build 时自动移除该 Animator(不影响最终效果)

**教学要点**:
- 🎯 中级功能,**新手可跳过**
- 🎯 与 Object Toggle 教学对比:"简单开/关用 Object Toggle,复杂动画用 Merge Animator"
- 💬 语言示例(零基础): "Merge Animator 像'动画传送门'——把你的动画贴到 Avatar 的'大脑'里"
- 💬 语言示例(高级): "Write Defaults 匹配在 OnEnable 阶段运行,通过反射读取 Avatar 动画器状态;混用 WD 会导致 OnDisable 状态污染"

---

### 1.3 Merge Motion (Blend Tree) ⭐⭐(原 Merge Blend Tree)

**一句话**: 合并多个 Blend Tree / Animation Clip / 持续动画到单一 FX 层,**始终运行**。

**何时用**:
- 始终运行的动作(表情、idle 循环)
- 多个小组件合并到一层(省 layer 数量)
- AFK 动画
- 直接合并**单个 animation clip**(不一定要 blend tree)

**何时不用**:
- 需要禁用/启用动画(用 Merge Animator)
- 动画值会随时间变化(Direct Blend Tree 会调整时长,**速度不可预测**)

**怎么用**(2 步):
1. 创建 Blend Tree 资产(右键 Project → Create → BlendTree)
2. 加 Merge Motion 组件,拖入 Blend Tree 到 `Motion` 字段

**怎么工作**:
MA 在 FX 控制器**顶层**创建**新层** + 单状态 + Write Defaults ON + **Direct Blend Tree**。每个合并的动作权重恒为 1。

**已知限制**:
- ⚠️ 1.12 前叫 "Merge Blend Tree",旧资产自动升级
- 📌 内部类名仍叫 `ModularAvatarMergeBlendTree`(API 兼容)
- ⚠️ 所有动画会被调整为**相同有效时长**(播放速度可能不一致) → **不适合随时间变化的动画**(如"3 秒后抬手"这类)

**教学要点**:
- 🎯 高级组件,**只有需要"始终运行"才用**
- 🎯 不当使用会导致**性能问题**(Direct Blend Tree 计算开销)
- 💬 语言示例(零基础): "Blend Tree 像'调音台',Merge Motion 是把所有调音台合并到一台"
- 💬 语言示例(高级): "Direct Blend Tree 没有 Normalized Time,Unity 引擎会强制所有子动画 rebase 到同一长度,这就是为什么不能用于随时间变化的动画"

---

## 2. 反应式组件（Reactive Components）

### 2.0 Reactive 系统总览（先读这个）

> 6 个 Reactive 组件: Object Toggle / Shape Changer / Material Setter / Material Swap / Mesh Cutter / 隐含的 Invert condition

**Active 判定**(同时满足):
1. GameObject 自身 + 所有父级在 Hierarchy 中 active
2. 如果在 Menu Item 同级或子级,该菜单项**被选中**(只算**第一层**父菜单,子菜单被忽略)

**响应触发**:
- 动画控制 GameObject 激活
- 其他 Object Toggle 联动
- Menu Item 选中状态

**Invert 条件**: 勾选后,在"条件不满足"时生效

**优先级**: 多个 Reactive 组件冲突 → **Hierarchy 中最下方的胜出**

**Reaction Timing 关键**:
- 1 帧延迟(防"闪烁"问题的核心)
- A → B → C 链式,A 关掉时:
  - 帧 1: 不发生任何事(A 的 disable 被延迟)
  - 帧 2: A 真正 disable(B 的 disable 被延迟)
  - 帧 3: B 和 C **同时** disable
- ⚠️ 精确时序**未来可能改变**,不要依赖

**Reaction Debugger**(调试工具):
- 右键 GameObject → `Modular Avatar → Show Reaction Debugger`
- 虚拟改变状态 + 菜单选中状态
- 不用进 Play 模式就能验证

### 2.1 [R] Object Toggle ⭐

**一句话**: 根据 Active 状态,启用/禁用**其他** GameObject。

**何时用**:
- 一个 mesh 完全被另一个 mesh 盖住时(关掉被盖的)
- 装上外套 → 自动关掉内衣
- 戴帽子 → 自动关掉头发后部分

**怎么用**(3 步):
1. 组件加到**控制对象**
2. 点 `+` 添加目标对象
3. **勾选** = 启用时启用 / **不勾选** = 启用时禁用

**冲突解决**:
- 多个 Object Toggle 控制同一对象 → Hierarchy 中**最下方的胜出**
- 所有都没 active → 用对象原状态/动画状态

**响应时序**:
- 1 帧延迟(参考系统总览)
- A → B → C 链式,逐级延迟
- 💡 **设计意图**: 关外层衣服时,内层衣服晚 1 帧禁用 → **防止"脱衣服时裸体闪现"**(disable 在 enable 之前执行)

**教学要点**:
- 🎯 **100% 玩家第一个要学的功能**
- 🎯 别教手动 Animator 方案
- 💬 语言示例(零基础): "Object Toggle 就像'一键开关'——打开就亮,关掉就暗"
- 💬 语言示例(高级): "Reactive 组件响应 GameObject active 状态,优先级按 Hierarchy 末位胜出;1 帧延迟是 'disable-then-enable' 顺序保证"

---

### 2.2 [R] Shape Changer ⭐⭐

**一句话**: 根据 Active 状态,改形态键(blendshape)值,或**直接删除多边形**。

**何时用**:
- 衣服覆盖了身体某部位 → 缩/删那个部位的形态键
- 鞋子穿模 → 缩脚部形态键
- **省性能**: 没有动画时用 Delete 模式(直接删 mesh,省 GPU)

**何时不用**:
- ⚠️ 改的形态键**也会被其他动画影响** → 改为**开关控制 GameObject** 而不是直接改形态键

**怎么用**(5 步):
1. 组件加到要影响的对象(通常是 SkinnedMeshRenderer)
2. `Target Renderer` 拖入要改的 Renderer
3. 点 `+` 选形态键
4. 选模式: **Delete** 或 **Set**
5. (推荐)用 Scene View 的 `Overdraw` 调试叠加看效果

**模式对比**:

| 模式 | 效果 | 何时用 |
|------|------|--------|
| **Delete** | 直接删多边形(性能好) | 不会被动画的情况 |
| **Set** | 设为指定值 | 会被其他动画影响 |

**Threshold**:
- 决定"哪些顶点算被影响"
- 降低 → 影响更多顶点
- 升高 → 更少

**冲突**:
- 多个 Shape Changer 改同一形态键 → Hierarchy 中**最下方的胜出**

**已知限制**:
- ⚠️ **不能与其他动画同时改同一个 blendshape**(会互相覆盖,行为不可预测)
- ⚠️ 编辑器**无法预览**形态键联动效果
- 用 Avatar 3.0 Emulator 或 Gesture Manager 在 Play 模式测试
- 💡 调试技巧: Scene View 的 **Overdraw debug overlay** 可以看到衣服下的形态(验证 Delete 模式是否真的删掉了多边形)

**教学要点**:
- 🎯 教程 4 核心内容
- 🎯 新手**可以跳过**,等遇到穿模再学
- 💬 语言示例(零基础): "Shape Changer 是'隐形斗篷'——把身体被盖住的部分用魔法藏起来"
- 💬 语言示例(高级): "Delete 模式调用 Mesh.SetTriangles 删除顶点,运行时零开销;Set 模式依赖 Animator 控制 blendshape 值,有动画时性能较高"

---

### 2.3 [R] Material Setter ⭐

**一句话**: 根据 Active 状态,**替换某个 Renderer 的材质**。

**何时用**:
- 换某个对象的材质(如衣服发光版)
- 配合菜单项切换外观

**与 Material Swap 的区别**:
- **Material Setter**: 你指定**要改的 Renderer**(精确控制某个对象)
- **Material Swap**: 你指定**要换的 Material**(批量替换)

**怎么用**(5 步):
1. 组件加到控制对象(动画控制 / Menu Item 同级 / 始终启用)
2. 点 `+` 添加条目
3. 拖入要操作的 Renderer 到上字段
4. 右边下拉选**材质槽位**
5. 拖入**目标材质**到 `Set material to`

**Invert**:
- 默认: GameObject 启用时换
- 勾选 Invert: GameObject 禁用时换

**教学要点**:
- 🎯 与 Material Swap 配合教
- 💬 语言示例(零基础): "Material Setter 就像'换装按钮'——按一下换一套衣服的样子"

---

### 2.4 [R] Material Swap ⭐

**一句话**: 批量替换 Avatar 上的材质。

**何时用**:
- 换衣服颜色主题(红/蓝/绿多套)
- 批量改主题色
- **Quick Swap**: 编辑器内快速预览不同材质

**怎么用**(3 步):
1. 组件加到控制对象
2. 点 `+` 添加条目: 拖入"原材质" + 拖入"目标材质"
3. (可选)设置 `Target Root` 限定范围

**Quick Swap 模式**:

| 模式 | 行为 |
|------|------|
| None | 关闭 |
| Same Folder | 同文件夹找同前缀材质 |
| Adjacent Folders | 找相邻文件夹的同名材质 |

启用后,Inspector 出现 ← → 按钮,可**点一下切换预览**

**Adjacent Folders 示例**:
- 原材质: `Assets/SomeOutfit/Materials/Blue/Outer.mat`
- 切换时找: `Assets/SomeOutfit/Materials/Red/Outer.mat`(同级其他文件夹的同名文件)
- 典型用法: 衣服作者按颜色分文件夹,Quick Swap 在编辑器内快速预览

**教学要点**:
- 🎯 衣服"调色板"功能
- 💬 语言示例(零基础): "Material Swap 是'颜料盒'——红色蓝色绿色一次准备好,随时切换"

---

### 2.5 [R] Mesh Cutter ⭐⭐

**一句话**: 按条件删/隐藏**多边形**(4 种 Vertex Filter)。

**何时用**:
- 衣服覆盖的身体部位会穿模 → 删掉
- 美学目的(如缩短缎带一边)
- 减少多边形数(Always Active 时)

**何时不用**:
- ⚠️ 整个 mesh 被另一个完全盖住 → **用 Object Toggle**(Mesh Cutter 还是要处理整个 mesh)
- 简单开/关(用 Object Toggle)

**怎么用**(3 步):
1. 加 Mesh Cutter 组件,设 `Object` 字段
2. 至少加一个 Vertex Filter(`Add Vertex Filter` 按钮)
3. (可选)勾 Invert

**4 种 Vertex Filter**:

| Filter | 选什么 | 何时用 |
|--------|-------|--------|
| By Mask | 蒙版纹理指定区域 | 复杂形状 |
| By Axis | 平面一侧 | 上下左右分割 |
| By Bone | 骨骼权重 | 身体/手部分割 |
| By Blendshape | 形态键激活时移动的顶点 | 表情时删除 |

**多 Filter 组合**:
- Combine: 任一 Filter 选中的顶点都包括
- Intersect: 所有 Filter 都选中的顶点才包括
- 例子: 缎带 UV 共享 → By Mask 选整条 + By Axis 选左边 + By Axis 选多长

**效率**:
- Always active → **删除多边形**(省性能)
- Sometimes inactive → **隐藏**(可能加 constraint,占性能)

**教学要点**:
- 🎯 高级组件
- 💬 语言示例(零基础): "Mesh Cutter 是'裁剪刀'——把不需要的部分剪掉"
- 💬 语言示例(高级): "Always-active Mesh Cutter 在编译时通过 Mesh.SetTriangles 静态裁剪;有时 inactive 则保留顶点,通过 Skin Weight 切换到 proxy 骨骼"

---

### 2.6 Reaction Debugger（不挂载,是工具）

**一句话**: 调试器,虚拟改变状态看 Reactive 行为,**不用进 Play 模式**。

**打开方式**:
- 右键 GameObject → `Modular Avatar → Show Reaction Debugger`
- 或点 Reactive 组件的 `Open reaction debugger` 按钮

**两个区域**:
- **Object state** — 强制对象 active/inactive + 菜单选中/取消
  - `Inspecting object` 字段(可锁)
  - `Clear all active overrides` 按钮
  - `-` / `+` 按钮强制状态
- **Reaction section** — 列出所有影响这个对象的 Reactive 组件 + 触发条件 + 可覆盖

**特性**:
- "Forcing active" **不真的改 Hierarchy 状态**,只在 Scene View 模拟显示

**教学要点**:
- 🎯 **教玩家"先 Debugger 验证,再 Play 模式"**,省时
- 💬 语言示例(零基础): "Debugger 就像'彩排'——不用真演,先看效果对不对"

---

## 3. 菜单系统（4 个组件）

### 3.1 Menu Item ⭐

**一句话**: 在 Hierarchy 定义菜单项,**不用创建 VRC 资产**。

**何时用**:
- 任何需要菜单项的场景(默认方式)
- 想拖拽重组菜单结构

**怎么用**(3 步):
1. 改名(菜单名 = 对象名)
2. 选 Type(Toggle / Sub Menu / ...)
3. 配参数(从下拉选已定义的 MA Parameters)

**子菜单配置**:
- `Submenu Source = Children` → 用子级作菜单项(推荐)
- `Submenu Source = Expressions Menu Asset` → 用 VRC 资产

**绑定方式**(3 种):
1. 作为另一个 Menu Item(Sub Menu 模式)的子
2. 与 Menu Installer 同对象
3. Menu Group 的子级

**Source Object Override**:
- 用其他对象的子级作为子菜单源

**自动参数创建**:
- 参数名未在 MA Parameters 或 VRC Parameters 中声明 → **自动创建**
- 控制 Saved / Synced
- ⚠️ 多个 `Is Default` 冲突 → **未定义行为**

**自动分页**:
- 当菜单项数量超过 VRC 单页最大条目数(通常 7-8 个),MA **自动生成 "Next" 分页**
- 无需手动拆分

**Unbound menu items**(未绑定的菜单项):
- ⚠️ 不在以上 3 种绑定方式中的 Menu Item **完全无效果**(不会出现在任何菜单里)
- 如果菜单项"消失了",先检查它是否绑到了某个 Menu Installer / Sub Menu / Menu Group

**教学要点**:
- 🎯 改模新手**用 Hierarchy 方式**比 VRC 资产**直观 10 倍**
- 💬 语言示例(零基础): "Menu Item 就像'文件夹里的按钮'——每个按钮是一个开关"

---

### 3.2 Menu Installer ⭐

**一句话**: 把菜单项装到 Avatar 主菜单。

**何时用**:
- 几乎所有需要菜单的场景

**怎么用**(端用户):
1. 默认装到 **Avatar Action Menu 顶层**
2. 点 `Select Menu` 选目标菜单(自动创建 Menu Install Target)
3. 满了自动分页(自动生成 "Next")
4. 取消勾选 Inspector **左上角 checkbox** 可完全禁用 menu installation

**Prefab 开发者**:
1. 创建 Expressions Menu 资产
2. 加 Menu Installer 到与 MA Parameters 同一级
3. Prefab Developer Options → `Menu to install` 选菜单

**Menu sources**(除了装资产):
- 加 Menu Item / Menu Group → 自动生成菜单

**Extending 别人的菜单**:
- 用 `Install To` 字段指定其他 Menu Installer 的菜单

**教学要点**:
- 🎯 必学
- 💬 语言示例(零基础): "Menu Installer 是'菜单总入口'——你做的开关都从这里挂到 Avatar 上"

---

### 3.3 Menu Group ⭐

**一句话**: 多个 Menu Item 不分组(直接装到目标菜单)。

**何时用**:
- 想装多个 Menu Item 但**不创建子菜单**
- 主要是 **Extract Menu 系统的内部组件**(转换已有 expression menus 时用)
- 玩家**一般不需要直接添加**,MA 在内部自动使用

**怎么用**:
- 加 Menu Group 组件(默认包含所有直接子级 Menu Item)
- 可设 `Source Object Override` 选其他源

**教学要点**:
- 🎯 高级玩家才用
- 💬 提示: "对新手:用 Sub Menu 模式代替,菜单更清晰"

---

### 3.4 Menu Install Target ⭐⭐

**一句话**: 支持 Menu Installer 的 `Select Menu` 按钮,**大多数情况不用手创建**。

**何时用**:
- 几乎不用手创建
- MA 用 `Select Menu` 时会自动生成
- 玩家**不需要手动添加此组件**

**怎么工作**:
- 覆盖 Menu Installer 的目标菜单选项
- 相当于"菜单被复制到 Menu Install Target 位置"

**教学要点**:
- 💬 "如果看到 Inspector 出现这个组件,**不要删**——是 MA 自动生成的"

---

## 4. 骨骼相关（4 个组件）

### 4.1 Bone Proxy ⭐

**一句话**: 把对象挂到素体的**指定骨骼**上(可保持世界坐标)。

**何时用**:
- ✅ 在手上挂个 Cube
- ✅ 头上挂发饰
- ✅ 想做**通用 Prefab**(套到任何 Avatar 都能用)
- ✅ 配合 PhysBone Blocker 做 Rigid 配件

**何时不用**:
- ⚠️ **装衣服**(用 Merge Armature)
- Merge Armature 会合并骨骼,Bone Proxy 只是重新父化

**怎么用**(2 步):
1. 组件加到要挂的对象
2. 拖入目标骨骼到 `Target`

**Attachment Mode**:

| 模式 | 行为 | 何时用 |
|------|------|--------|
| As child at root | 位置/旋转归零 | 通用 Prefab(推荐) |
| As child keep world pose | 保留世界位置 | Avatar 专用 Prefab(精确位置,如 Cloth collider) |

**Match Parent Scale**:
- 启用 → 局部 scale 变 (1,1,1)
- 关闭 → 保留原世界 scale
- 当目标骨骼有缩放时,启用更可靠

**与 Merge Armature 的核心区别**:

| 维度 | Bone Proxy | Merge Armature |
|------|------------|----------------|
| 骨骼合并 | ❌ 不合并 | ✅ 合并 |
| 跨 Avatar 通用 | ✅ 通用 | ❌ Avatar 专用 |
| 开/关父对象影响子 | ❌ 不影响 | ✅ 影响 |
| 动画路径调整 | ✅ 修 | ✅ 更深(还修 toggle 父) |

**教学要点**:
- 🎯 与 Merge Armature **必须对比教学**
- 🎯 通用小物件(项链、戒指)用 Bone Proxy
- 💬 语言示例(零基础): "Bone Proxy 是'挂钩'——你想挂哪就挂哪,不用关心 Avatar 怎么造"

---

### 4.2 PhysBone Blocker ⭐

**一句话**: 阻止父 PhysBone 链影响子对象。

**何时用**:
- 配件想**刚性附着**到 PhysBone 链(尾巴、耳朵上的装饰)
- 与 Bone Proxy **配合**(挂在 PhysBone 链的某骨骼)

**怎么工作**:
把子对象加到任何父对象 PhysBone 的 Ignore 列表。

**配合 Bone Proxy**:
- Bone Proxy 挂到 PhysBone 链的某骨骼
- 同一对象加 PhysBone Blocker
- 确保刚性附着

**已知限制**:
- ⚠️ 不能用在 PhysBone 链**子级** — 在父级加

**教学要点**:
- 🎯 与 Bone Proxy 配合教
- 💬 "想让发饰不被头发甩动?加这个"

---

### 4.3 Scale Adjuster ⭐⭐

**一句话**: 单独调某骨骼的 X/Y/Z 缩放,**不影响子骨骼**。

**何时用**:
- ✅ **主要用途**: fitting clothing not originally designed for your avatar(衣服偏胖/偏矮/比例不对)
- X/Y/Z 不同缩放(只胖不高等)
- 多骨骼**同时**缩放(批量)

**何时不用**:
- 等比缩放(用 Unity 自带 Scale 工具)

**怎么用**(2 步):
1. 组件加到目标骨骼
2. 用 Scale 工具调

**Adjust child positions**:
- 调整子级**位置**(不缩放)以补偿父级缩放

**多骨骼**:
- 加 Scale Adjuster 到所有目标骨骼
- 选中多个后同时缩放
- ⚠️ 骨骼有旋转时效果不完美

**已知限制**:
- ⚠️ 只对 Unity Scale 工具生效
- 组合工具(Move/Rotate/Scale)仍影响所有子级

**教学要点**:
- 🎯 高级组件,只用于"等比缩放不够"的场景
- 💬 "如果衣服整体偏胖,但 X/Y/Z 比例是对的,Scale Adjuster 不行,改用普通 Scale 工具"

---

### 4.4 Move Independently ⭐⭐

**一句话**: 编辑模式独立移动对象,**不影响子级**。**运行时无效**。

**何时用**:
- 调衣服贴合(移动 Hips 不影响其他)
- "Objects to move together" 组合移动(比如 Hips + Upper Leg 一起)

**已知限制**:
- ⚠️ 运行时**完全无效**
- ⚠️ 非均匀缩放(各轴不同)**未完全支持**,可能怪行为
- 单独缩放轴 → 用 Scale Adjuster 配合

**教学要点**:
- 🎯 编辑模式工具
- 💬 "这个只是帮你微调用,运行时不存在"

---

### 4.5 Global Collider ⭐⭐

**一句话**: 让一个物件的 Collider **跨 Avatar 互动**——别人家的 PhysBone 可以撞到它。

**何时用**:
- 给武器、道具加 collider,让它们能**碰别人家的 PhysBone**(头发/衣服/尾巴)
- 把手指 collider 移到嘴里(模拟咬东西)
- 给拳头加 collider 去撞别人(动画驱动 GameObject 实现"冲击波/后坐力")

**何时不用**:
- ⚠️ **超过 6 个 = 自己手指 collider 被侵占**(VRChat 硬上限)
- 不到处用——global collider 有性能成本
- 想做"自己的 PhysBone 撞自己 Avatar 上的东西"——这个组件是给别人撞的

**怎么用**(3 步):
1. 选中要变成 global collider 的 GameObject(必须有 Collider 组件)
2. Add Component → **MA Global Collider**
3. (可选)勾 `Manual Remap` 手动指定占用哪个 collider slot
4. (可选)勾 `Low Priority Collider` 标记为"可被覆盖"

**怎么工作**:
MA 把这个 collider 注册为"global collider",VRChat 引擎会把它和别人的 PhysBone 互动。VRChat 里默认只有手指的 collider 是 global(能撞别人),这个组件会"借用(hijack)"一个 finger collider slot 来挂载你的 collider。

**Manual Remap 选项**:
- **未启用**(默认):MA 自动选一个可用的 collider slot
- **启用**:手动选要 hijack 哪个 slot
  - 可选:Head / Torso / Feet
  - ⚠️ **但 Head/Torso/Feet 不是 physics collider**——它们只是 contact sender,**不会跟别人 PhysBone 互动**
  - 这个选项主要是让你**避开**不想被侵占的 slot(如保留手指 collider)

**Low Priority Collider**:
- 必须配合 Manual Remap 使用
- 标记后,被别人同名占用时**无警告被覆盖**
- 用法:多个"次要" global collider + 1 个"主要"的,避免互相冲突

**已知限制**:
- ⚠️ **VRChat 硬上限 6 个**——超过 6 个 → 自动侵占 index finger collider(用手指 collider 的人**手指就没法抓东西了**)
- ⚠️ 平台差异:VRChat 用"侵占 slot"方式,其他平台(Resonite 等)MA 可能用不同实现
- 📌 Shape 任意:capsule / sphere / PhysBone 风格 collider 都行
- 📌 6 个限制是 **VRChat SDK 限制**,不是 MA 限制
- 📌 Manual Remap 选 Head/Torso/Feet 不会增加 physics 互动,只是避开 slot

**教学要点**:
- 🎯 这个组件**不是给普通玩家**用的——90% 玩家不需要
- 🎯 主要场景:做"互动道具"创作者(咬人/打人的手、武器、冲击波)
- 🎯 **关键风险**:超过 6 个 = 自己手指被侵占,用户体验崩
- 🎯 "想用别人的 PhysBone"和"不想被别人的 PhysBone 影响自己"是两件事——后者用 PhysBone Blocker
- 💬 简单叙述(给玩家): "你想做的道具能**碰别人家的头发/衣服**?加这个。但 6 个是上限,超过了你自己手指就废了——所以**绝对不要乱加**"
- 💬 专业叙述(给创作者): "MA Global Collider 在 VRChat 上 hijack 一个 finger collider slot,通过 VRCPhysBone 内部 API 把这个 collider 注册为 global collider 列表;6 个限制是 VRChat SDK hard cap,不是 MA 限制;Manual Remap 让你选避开哪个 slot,但 Head/Torso/Feet 不是 physics collider——它们是 VRC Contact sender,只能触发 contact,不会跟别人 PhysBone 互动"
- 💬 对比教学(给玩家): "Global Collider 是'**我撞别人**';PhysBone Blocker 是'**别人不撞我**'——别搞反"
- 🔗 关联: PhysBone Blocker(反向——阻止别人 PhysBone 影响自己)、Bone Proxy(挂 collider 用的载体)

---

## 5. 服装专用（4 个组件）

### 5.1 Blendshape Sync ⭐

**一句话**: 把一个 Renderer 的形态键值**同步**到另一个。

**何时用**:
- 衣服的形态键跟素体(胸部大小、身体形状)
- Avatar 内不同 Mesh 间同步

**怎么用**(3 步):
1. 组件加到 Prefab 对象
2. 点 `+` 打开选择窗口
3. 双击形态键添加

**多选编辑**: 选中多个 mesh 一次配

**已知限制**:
- ⚠️ 不能链式(A→B→C 不行,只能 A→B 和 A→C 分开配)
- ⚠️ 不支持通过多层(只一级)
- ⚠️ 运行时**只支持** Animator 控制的形态键——VRChat 内置的 **EyeLook / Viseme 系统不经过 Animator**,所以 Blendshape Sync 无法准确同步这些 blendshape

**怎么工作**:
- **编辑模式**: 自动复制形态键值到目标 renderer(改了基对象 → 衣服跟着变,实时预览)
- **Play 模式**: 修改任何动画基础对象的 blendshape 也影响其他同步对象

**教学要点**:
- 🎯 调体型不变形 → 99% 是缺这个
- 💬 "调胸部大小,衣服不变?加 Blendshape Sync"

---

### 5.2 PhysBone Blocker（见 4.2）

### 5.3 Replace Object ⭐⭐

**一句话**: 完全替换 Avatar 上的对象。

**何时用**:
- 替换 Avatar 的 PhysBones 配置
- 替换 Body 网格
- 替换 Head 网格(保留 Bone Proxy 引用)

**何时不用**:
- ⚠️ 一个对象只能被另一个替换(限制多组合并性)
- 多人想替换同一对象 → **冲突**

**怎么工作**:
- 子对象处理: 原对象和替换对象的子级**都保留**,都装到替换对象下
- 命名: **不改名**(替换对象保持原名),但**更新动画路径**指向新位置
- 动画路径: **更新**指向新对象
- 组件引用: 按"同类型同索引"匹配(无模糊匹配)
  - Box → Sphere 引用 → **null**

**已知限制**:
- ⚠️ **晚**执行(avatar processing 晚期,影响少数 MMD World 兼容性——替换 Body mesh 时需特别注意)
- ⚠️ 引用匹配**不模糊**
- ⚠️ 一个对象只能被**一个**其他对象替换 → 限制与其他资产的兼容性

**教学要点**:
- 🎯 高级组件
- 💬 "如果你做了新身体想替换旧身体,这个组件让你不用拆 Avatar"

---

### 5.4 Mesh Settings ⭐⭐

**一句话**: 设置 mesh 的 anchor override 和 bounds,**对所有子 mesh 生效**。

**何时用**:
- 装到 Avatar 根 → 保证所有 mesh 的 bounds/light probe anchor 一致
- **Setup Outfit 自动加这个**

**怎么用**:
- 组件加到对象
- 设 `Anchor Override Mode` + `Bounds Override Mode`

**Root Bone 字段**:
- Bounds 相对此 transform 计算
- 通常设为 Skinned Mesh Renderer 的 rootBone 对应骨骼
- 确保 bounds 跟随骨骼移动,避免裁剪错误

**4 种模式**(Anchor / Bounds 各自):

| 模式 | 行为 |
|------|------|
| Inherit | 继承父级(不做事) |
| Set | 设置子 mesh 的值 |
| Don't set | 阻止父级,保留默认 |
| Set or inherit | 父级 Set 用父级,否则用自己(给 outfit prefab 用) |

**已知限制**:
- ⚠️ Bounds 只对 Skinned Mesh Renderer 生效
- ⚠️ Anchor Override 对所有 Renderer 生效(Mesh / Line Renderer 等)
- ⚠️ 卖给别人的 outfit 不要乱设(可能与 Avatar 不一致)

**教学要点**:
- 🎯 中级,大多数玩家不用手动碰
- 💬 "Setup Outfit 帮你设好了,看不懂别动"

---

## 6. Avatar 配置（4 个组件）

### 6.1 Floor Adjuster ⭐

**一句话**: 调 Avatar 垂直位置(鞋底对齐地板)。

**何时用**:
- 装鞋子时,避免陷进地板

**何时不用**:
- ⚠️ VRChat **不能动态调** Avatar 高度
- 多个 Floor Adjuster 同时存在 → **不调整**
- 未来可能改变

**怎么用**(2 步):
1. 新建 GameObject,加 Floor Adjuster
2. 调 Y 位置垂直对齐鞋底

**提示**:
- 用 **Scene View side-on isometric 视图**调整(最直观看到鞋底与地板的对齐)
- 一次只能调一个,多个冲突
- 多个 outfit 不同鞋底高度 → 当前**无法动态调整**(未来可能变)

**教学要点**:
- 🎯 简单,但**要主动告诉玩家 VRChat 限制**
- 💬 "装上鞋子陷地了?加 Floor Adjuster;**但一次只能调一个高度**,有多个鞋子需要不同高度?现在不支持"

---

### 6.2 Visible Head Accessory ⭐

**一句话**: 让头部子对象在**第一人称**可见。

**何时用**:
- 头发、配饰在第一人称可见
- 不用照镜子就能看到自己

**何时不用**:
- ⚠️ 不能是 PhysBone 链的**子级**(在父级加)
- ⚠️ 全部 Head 子级都用 → 视线被挡(只挑主要的)

**怎么用**(1 步):
- 加在 Head 子级下,无需配置

**怎么工作**:
- 用 VRCHeadChop 让骨骼可见
- **调整 mesh** 确保三角形不穿过视角
  - 找"有部分顶点 visible bone,有部分 hidden bone"的三角形
  - 加 proxy 骨骼 + 切换权重

**教学要点**:
- 💬 "想戴眼镜第一人称能看到?加这个;但别全加,挡视线"

---

### 6.3 World Fixed Object ⭐

**一句话**: 让对象跟着世界,不跟 Avatar。

**何时用**:
- 浮空剑、悬浮装饰
- 任何"Avatar 动但对象不动"的场景

**怎么用**(1 步):
- 加到 GameObject,无需配置

**怎么工作**:
- 自动生成 world-origin fixed GameObject 在 Avatar 根
- 把你的对象移到其子级
- 可用 Parent Constraints 等控制位置

**性能**:
- ⚠️ **只生成一个 constraint**,1 个或多个 World Fixed Object 性能相同

**教学要点**:
- 💬 "想做悬空剑?加这个"

---

### 6.4 World Scale Object ⭐

**一句话**: 强制 scale = (1,1,1),不受 Avatar 缩放影响。

**何时用**:
- 复杂 constraint 道具(scale 不变很重要)
- 任何需要"世界尺寸"的道具

**怎么用**(1 步):
- 加到 GameObject,无需配置

**已知限制**:
- ⚠️ 编辑器**不预览**,Play Mode / 游戏中才生效

**怎么工作**:
- 自动添加 **VRC Scale Constraint**(scale 1,1,1 relative to world)
- 确保对象始终保持世界尺寸,不受 Avatar 缩放影响

**教学要点**:
- 💬 "复杂的链子道具?用这个避免缩放污染"

---

## 7. 平台/通用（5 个组件）

### 7.1 Platform Filter ⭐

**一句话**: 按平台启用/禁用对象。

**何时用**:
- 想要 VRChat 专用小道具只在 VRChat 出现
- 跨平台兼容

**何时不用**:
- ⚠️ 很多 MA 组件已自动处理平台限制(如 Merge Animator 只对 VRChat)
- **不要重复设置**

**怎么用**(3 步):
1. 加组件到 GameObject
2. 选 Platform + Include/Exclude
3. (可选)加多个 Platform Filter 组件到同一对象

**Include vs Exclude**:
- **Include**: 只在指定平台存在
- **Exclude**: 在指定平台被移除

**已知限制**:
- ⚠️ Include + Exclude 同时存在 → **报错**

**例子**:
- VRChat 专用 → Platform = VRChat,Include
- Resonite 隐藏 → Platform = Resonite,Exclude

**教学要点**:
- 🎯 简单,**但要主动说"很多情况不用"**
- 💬 "你想让 VRChat 专用道具在其他平台消失?加 Platform Filter"

---

### 7.2 Remove Vertex Color ⭐

**一句话**: 移除对象及子对象的顶点色。

**何时用**:
- 模型带"不打算显示"的顶点色
- 切到 VRChat Mobile Shader(用顶点色)导致变色

**怎么用**:
- 加到 root(所有子对象都受影响)
- 想保留某对象 → 加 Remove Vertex Color + 模式 = "Keep Vertex Colors"

**教学要点**:
- 🎯 简单,但**仅当遇到变色问题**才需要
- 💬 "头发变色了?加 Remove Vertex Color 试试"

---

### 7.3 Rename VRChat Collision Tags ⭐

**一句话**: 重命名 VRChat Contacts 的标签(避免冲突)。

**何时用**:
- 不想你的 contacts 干扰其他 Avatar
- 想和特定组件用相同 tag(主动建立联系)
- 多个组件可能冲突

**怎么用**:
- 加到 GameObject
- 添加要重命名的 tags
- "Auto rename" 自动选唯一名

**嵌套**:
- 内层 Rename → 外层 Rename → 两层规则叠加

**已知限制**:
- ⚠️ 加在 contact 的 Root Transform 父级 → 不会重命名该 contact

**教学要点**:
- 🎯 高级组件
- 💬 "做了咬人头发等 contact 小道具?加这个避免和别人撞名"

---

### 7.4 Convert Constraints ⭐

**一句话**: 编译时把 Unity Constraints 转成 VRChat Constraints。

**何时用**:
- 默认装到 Avatar 根
- VRChat Auto Fix 会自动加这个(MA 装了之后)

**怎么工作**:
- 转换同对象 + 所有子对象的 Unity Constraints
- 也尝试修复旧 VRCSDK Auto Fix 弄坏的动画

**已知限制**:
- 主要提供"禁用"接口(移除此组件 = 禁用功能)

**教学要点**:
- 🎯 "如果有这个组件,**别删**——它帮你优化性能"
- 💬 "VRChat Constraints 比 Unity Constraints 性能好,自动转换"

---

### 7.5 VRChat Settings ⭐

**一句话**: Avatar-wide 配置(VRChat 特定)。

**唯一设置**:
- **MMD World Support** — 启用/禁用 MMD World 处理

**已知限制**:
- 整个 Avatar 只能**一个实例**
- 没找到 → 用默认设置

**教学要点**:
- 🎯 简单
- 💬 "如果 MMD World 里你的表情被禁用?检查这里"

---

## 8. MMD 与高级（3 个组件）

### 8.1 MMD Layer Control ⭐⭐（State Machine Behavior,不是普通组件）

**一句话**: 让 Merge Animator 加的层**也被 MMD World 控制**。

**何时用**:
- 默认: 通过 Merge Animator 加的层**不被** MMD World 禁用
- 想让自定义层也被禁用 → 加这个

**怎么用**:
- 装到想要被 MMD 控制的**层**(State Machine Behavior)
- 装到**层**(不是 state) ⚠️

**已知限制**:
- ⚠️ 必须直接装到层(不能装到 state,否则 build 失败)
- ⚠️ 只对禁用 layer 2 & 3 的 MMD World 有效

**教学要点**:
- 🎯 高级组件
- 💬 "你想在 MMD World 里表情也乖乖听话?加这个 state machine behavior 到 FX 层"

---

### 8.2 MMD World Workarounds（系统行为,不是组件）

**背景**:
- 部分 MMD World **禁用 FX 层 2、3**(原本禁表情)

**MA 自动处理**:
- 自动保护"原本是 2、3 的层"
- 通过 Merge Animator 加的层**默认不受影响**
- 必要时加 padding 层

**禁用整个机制**:
- VRChat Settings 组件
- 关掉 `MMD World Support`

**教学要点**:
- 🎯 大多数玩家**完全不需要管这个**
- 💬 "如果你的表情在某个 World 突然不工作?可能是 MMD World,加 VRChat Settings 关掉 MA 处理"

---

### 8.3 Sync Parameter Sequence ⭐⭐⭐（高级）

**一句话**: 确保 PC 和 Android 版本的 Avatar 共享参数顺序。

**何时用**:
- 同一 Avatar 多个平台版本(PC + Android)
- 跨平台同步 synced 参数

**何时不用**:
- ⚠️ 与 VRCFury Parameter Compressor 不兼容

**怎么用**(5 步):
1. 组件加到 Avatar 任意对象
2. 选 `primary platform`(含所有参数的版本)
3. **先**在 primary 平台 Build & Upload
4. **再**在其他平台 Build & Upload
5. MA 自动同步参数顺序

**VRChat per-platform overrides**:
- 只在**主 Avatar** 加
- Override Avatar **不用加**
- 自动从主 Avatar 同步缺失参数

**要求**:
- Primary 平台必须**包含所有**要同步的参数
- 缺失会 Build 失败
- **共享参数必须在参数列表开头且顺序一致**(PC 和 Android 同步的前提条件)

**教学要点**:
- 🎯 高级创作者专用
- 💬 "你做 PC + Quest 双版本?主版本加这个,先传 PC"

---

## 9. 高级：参数与菜单组合

### 9.1 MA Parameters ⭐⭐（必学）

**一句话**: 定义/重命名参数(VRChat 表达式参数)。

**何时用**:
- 任何用了 Animator 参数的小组件
- 想要 Internal 参数避免冲突
- 想要 Synced/Saved 控制

**参数类型详解**:

| 类型 | 说明 | 何时用 |
|------|------|--------|
| Bool | 布尔 | 开关(Toggle 类菜单项) |
| Int | 整型 | 计数器(多状态切换) |
| Float | 浮点 | 滑块(连续值控制) |
| Animator Only | **不加到** Expressions Parameters,但仍可重命名 | 内部动画参数(不占 256 限额) |
| Prefix | 用于 PhysBone / Raycast 组件的**前缀参数**(这些组件一次生成多个参数) | 配置 PhysBone 链路 |

**怎么用**(2 种创建方式):
1. 点 `+` 手动加参数
2. 展开 `Unregistered Parameters` 自动添加(动画器里用了但没声明的参数会出现在这里)

**重命名**:
- `Change name to` 输入新名
- **只影响组件外**的引用
- 勾 `Auto rename` 自动选未用名

**默认值**:
- Avatar 重置后用
- 留空 → 用 Expression Parameters 的值或 0/false
- `Override Animator Defaults` → 覆盖 Animator Controller 的默认值(当 Animator 里也有默认值时,MA Parameters 的优先)

**Saved/Synced**:
- Saved: 跨 Avatar 更改和重启保存(本地持久化)
- Synced: 网络同步(**消耗参数限额**,VRChat 总共 256)
- Animator Only 类型**不会**加到 Expressions Parameters,但仍可重命名(不占限额)

**嵌套**(Nesting 规则——多个 MA Parameters 嵌套时):
- **Saved**: 取**最外层**;非嵌套时任意一个 Saved 都会保存
- **Default Value**: 取**最外层**;空白取最内层非空;多个非嵌套非空 → **会警告**
- **Synced**: 取最外层
- 内部重命名可被外层引用

**已知限制**:
- ⚠️ Synced 参数**很贵**——VRChat 总共 256 个
- 📌 教玩家从一开始就用 Internal

**教学要点**:
- 🎯 教参数**第一时间教 Internal**
- 🎯 256 上限必须**明确告知**
- 💬 "参数像口袋——VRChat 只给你 256 个格子,别乱装"

---

## 10. 横切页（4 个）

### 10.1 Manual processing

**何时用**:
- 想看 MA 编译后的最终结果
- 给其他工具用(如 UniVRM 导出)
- 调试问题

**怎么用**:
- 选中 Avatar
- `Tools → Modular Avatar → Manual bake avatar`
- 自动复制 Avatar + 所有 MA 处理
- 结果在 `ModularAvatarOutput` 文件夹

**生成资源**:
- 默认打包成单文件(避免 Unity bug + 加快处理)
- 可点 `Unpack` 拆开

**清理**:
- 不用时记得删 `ModularAvatarOutput`

### 10.2 Dealing with problems

**错误窗口**:
- 工具栏 `Tools → Modular Avatar → Show Error Report`
- 自动随编辑更新
- 点对象名跳到 Hierarchy 选中

**"Nothing is getting processed at all!"**:
- 检查 `Apply On Play` 是否勾选
- 路径: Avatar 根 → Inspector → VRC Avatar Descriptor → Apply On Play

### 10.3 FAQ

**Q: 能导出到 VRM 吗?**
- A: 不能自动。但可 `Tools → Modular Avatar → Manual bake avatar` 先输出到 UniVRM

**Q: 衣服原本不是为我的 Avatar 设计的,能用吗?**
- A: 可以。Merge Armature 按名字匹配骨骼。装好后用 `Reset position to base avatar` 大致对齐,再微调

### 10.4 Distributing Prefabs（创作者向）

**3 条核心建议**:
1. **引导用户去官方仓库**(不要在 Prefab 里夹带 MA 副本)
2. **用嵌套 Prefab** 兼容非 MA 用户
3. **用 Internal 参数**避免参数冲突

**Compatible vs Preset**:

| 类型 | 含 MA 组件 | 兼容性 | 适用 |
|------|-----------|--------|------|
| **MA Compatible** | ❌ | 任何安装方式 | 不强求 MA |
| **MA Preset** | ✅ | 需 MA 安装 | 卖装有 MA 的用户 |

**Setup Outfit 怎么工作**:
1. 找 `OutfitRoot → [Armature] → Hips`(名字要包含素体 Hips 名字)
2. T-Pose / A-Pose 转换
3. 创建 Merge Armature 组件
4. 创建 Mesh Settings 组件

**Things to avoid**:
- ⚠️ **PhysBones on humanoid bones** (MA 会尝试删除,行为不可预测)
- 推荐:PhysBones 放在 Merge Armature 组件**外部**

### 10.5 Experimental features（高级）

**当前实验**:
- Resonite 支持
- Portable Avatar Components

**启用**:
- 装最新 beta 版 MA + NDMF
- `Tools → NDM Framework → Experimental Features`

⚠️ 实验性功能**可能不向后兼容**变化

**Resonite 支持现状**:

| 组件 | 支持 |
|------|------|
| Bone Proxy | ✅ |
| Merge Armature | ✅ |
| Move Independently | ✅ |
| Physbone Blocker | ✅ |
| Replace Object | ✅ |
| Remove Vertex Color | ✅ |
| Scale Adjuster | ✅ |
| Merge Animator / Merge Blend Tree | ✖ VRChat only |
| Menu 系 | ⌛ 计划中 |
| Reactive Components | ⌛ 计划中 |

---

## 11. 教学决策：玩家问 X,我该教哪个组件?

| 玩家问题 | 教这个组件 | 教学关键 |
|----------|------------|----------|
| "衣服穿不上" | Merge Armature + Setup Outfit | "右键 → Setup Outfit" 一键 |
| "调体型衣服不变" | Blendshape Sync | "加这个,选基对象形态键" |
| "想加个开关" | Object Toggle | "Create Toggle 一键" |
| "穿模了" | Shape Changer | "Delete 模式省性能" |
| "想换衣服颜色" | Material Swap | "Quick Swap 编辑器预览" |
| "鞋子陷地" | Floor Adjuster | "VRChat 限制:一次只能一个" |
| "想做通用小道具" | Bone Proxy | "通用 vs Avatar 专用" |
| "头发想刚性挂" | PhysBone Blocker | "配 Bone Proxy" |
| "做表情菜单" | Menu Item + Installer | "Hierarchy 模式直观" |
| "参数冲突" | MA Parameters + Internal | "Internal 自动改名" |
| "想用 MMD World" | VRChat Settings | "默认开,想禁用就关" |
| "跨平台同步参数" | Sync Parameter Sequence | "先传 primary 平台" |

---

**参考链接**:
- [Modular Avatar Component Reference](https://modular-avatar.nadena.dev/docs/reference)
- [Modular Avatar Tutorials](https://modular-avatar.nadena.dev/docs/tutorials)
- [Modular Avatar GitHub](https://github.com/bdunderscore/modular-avatar)
