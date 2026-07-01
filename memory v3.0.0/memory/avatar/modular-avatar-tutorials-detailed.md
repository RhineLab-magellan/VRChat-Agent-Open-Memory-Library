---
title: "Modular Avatar 教程深度精读（玩家视角完整版）"
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
  - modular-avatar
aliases:
  - 玩家视角完整版
  - "Modular Avatar 教程深度精读（玩家视角完整版）"
related:
  - avatar-modding-guide.md
  - ma-component-cards.md
  - ma2bt.md
  - modular-avatar.md
  - animator-system.md
---
# Modular Avatar 教程深度精读（玩家视角完整版）

> 来源: [官方教程](https://modular-avatar.nadena.dev/docs/tutorials)
> 范围: **6 个教程的官方原文 + 玩家视角操作分解 + 验证步骤 + 易错点 + 教学衔接逻辑**
> 配套文档: `memory/avatar/modular-avatar.md`(主文档)
> 教学法归属: `memory/avatar/teaching-methodology.md`

---

## 0. 文档定位

本文档**不是教程的翻译**——而是基于官方教程的**完整精读 + 玩家操作视角转化**。每个教程包含 4 部分：

1. **官方原文步骤**（忠实摘录关键操作）
2. **玩家视角操作**（新手友好的动作分解，每步 1 动作）
3. **验证步骤**（如何判断"这一步成功了"）
4. **常见踩坑**（这一步最容易卡在哪里）

适用对象：**默认玩家没有 / 仅有少量 Unity + Animator + Avatars3 基础**。

---

## 教程地图：先学哪个？

| 玩家诉求 | 起点 | 备注 |
|---------|------|------|
| "我想装个衣服" | 教程 1 | 90% 玩家的第一个需求 |
| "我想开关一个物件" | 教程 3 | 不需要懂 Animator |
| "装上衣服身体穿模 / 鞋子陷地" | 教程 5 | 涉及形态键联动 |
| "我想做菜单二级页面" | 教程 4 | 教程 1+3 之后 |
| "我想做自己的小组件卖出去" | 教程 6 | **必须**先学 1+3+4 |
| "我有布娃娃衣服（Cloth）" | 教程 2 | 教程 1 之后 |

> **核心建议**：90% 的玩家**只需要教程 1 + 教程 3**。其他都是遇到具体问题再来学。

---

## 教程 1: Configuring a simple outfit（配置简单服装）

> 官方举例：Capettiya 的 **Sailor Onepiece** 装到 **Nagatoro Koyori 的 Anon-chan**

### 1.1 官方原文要点

```
步骤:
1. 把衣服 Prefab 拖到场景里 Avatar 的子级
2. 右键衣服根对象 → [ModularAvatar] Setup Outfit
3. MA 自动添加 Merge Armature 组件
4. 如果 Avatar 自带衣服,关闭它的可见性（教程里关闭 SailorOnepiece_Anon_PB）
5. 进 Play 模式 → 衣服应该跟着素体动

附加: Blendshape Sync（链接身体形状）
- 在衣服的 Mesh Renderer 上加 MA Blendshape Sync
- 点 + 按钮 → 弹出选择器
- 双击选中的形态键
- Target blendshape 字段可改名（留空则用原名）

What happened: 自动找到 Armature 下挂 Merge Armature,
  合并骨骼时:同名骨骼共享、衣服独有骨骼移到对应素体骨骼下、
  含组件的骨骼保留为单独对象
```

### 1.2 玩家视角操作分解（6 步）

```
Step 1: 把衣服拖到 Avatar 身上
  - 在 Project 窗口找到衣服 Prefab
  - 拖到 Hierarchy 里 Avatar（你的素体名字）的子级
  - ⚠️ 不要拆 Prefab!

Step 2: 右键衣服根对象
  - 在 Hierarchy 选中衣服最顶层的 GameObject
  - 右键 → 选 Modular Avatar → Setup Outfit
  - 你应该看到衣服根对象上多了 "Merge Armature" 组件

Step 3: 隐藏 Avatar 自带的衣服（如果有）
  - 找到 Avatar 自带的衣服对象（比如教程里的 SailorOnepiece_Anon_PB）
  - 取消勾选它（让眼睛图标变灰）
  - 这样新衣服看起来才不会被原衣服挡住

Step 4: 进入 Play 模式验证
  - 点 Unity 上方的 ▶ Play 按钮
  - 你应该看到衣服跟着素体动（移动、转头都跟随）
  - 如果不动 → 见 §1.4 易错点

Step 5: 退出 Play 模式
  - 点 ■ Stop 按钮
  - 注意:Play 模式下做的修改不会保存,这是正常的

Step 6 (可选): 链接身体形态键
  - 选中衣服的 Mesh Renderer 对象
  - Add Component → 搜 "Blendshape Sync"
  - 点组件上的 + 按钮
  - 弹出窗口:展开你的素体 Mesh,双击要同步的形态键
  - 完成后,改素体形态键 → 衣服跟着变
```

### 1.3 验证步骤（如何判断"成功了"）

| 检查点 | 通过标志 | 失败标志 |
|--------|---------|---------|
| Step 2 后 | 衣服根对象 Inspector 上出现 `Merge Armature` 组件 | 菜单里没有 `Modular Avatar → Setup Outfit` 选项 |
| Step 4 Play 中 | 衣服跟着 Avatar 动,无明显错位 | 衣服原地不动 / T-Pose 状悬空 |
| Step 4 转动 | 头/手/腰活动时衣服同步 | 部分身体部位不跟动 |
| Step 6 调体型 | 改素体形态键（如胸部大小）→ 衣服形状跟着变 | 衣服形状不变 |

### 1.4 易错点（这一步最容易卡哪里）

| 错误 | 原因 | 修复 |
|------|------|------|
| 菜单里找不到 `Modular Avatar → Setup Outfit` | MA 没装 / 没 Apply | VCC/ALCOM 检查 MA 仓库是否勾选 |
| Play 模式衣服不动 | 没执行 Setup Outfit | 回到 Step 2 重做 |
| 衣服部分身体跟动,部分不动 | 衣服骨骼名不匹配 | 改衣服骨骼名包含素体骨骼名 |
| Play 模式能动,但 Upload 后不能动 | GameObject 路径问题 | 用 `Manual Bake Avatar` 看最终结果 |
| 形态键同步不生效 | 链接的形态键名错 | 选形态键时检查名称拼写 |

### 1.5 官方原话中的"设计哲学"

> **"With Modular Avatar, you don't need to unpack the original avatar or outfit prefab!"**

**翻译**：用 MA 你不需要拆开原本的 Avatar 或衣服 Prefab。

**含义**（教学要点）：
- 玩家**永远不要手动拆 Prefab**
- 拆了反而麻烦（升级困难、容易坏）
- 教玩家时强调：**保留 Prefab 完整 = 一键升级**

---

## 教程 2: Configuring a complex (cloth) outfit（配置布料服装）

> 官方举例：Lachexia 的 **Dress Lumi** 装到 Anon-chan
>
> 前置：**已完成教程 1**

### 2.1 官方原文要点

```
前置准备（教程假设已完成）:
- 拖入并 Setup Outfit
- 关闭冲突对象:Cloth 整体,Underwear 设为 bra_off

新增步骤:
1. Setup Outfit（基础流程,教程 1 内容）
2. 处理 Colliders:
   - 选中所有 Hips_Collider 对象
   - 一次性加 MA Bone Proxy 到所有
   - Target 拖入素体的 Hips
   - "Attachment Mode" 自动变成 "As child; keep position"
3. 对其他 Collider 重复（Spine_Collider、Chest_Collider 等）
4. Blendshape Sync 处理 Skirt 和 Tops

Other extensions（高级,可不做）:
- 加 Merge Animator 自动化设置:
  - Body blendshape: torso_thin=100, elbow_off=0, bra_off=100
  - disable Cloth
- ⚠️ 警告: 这会和 Outfit Changer 冲突
```

### 2.2 玩家视角操作分解

```
Step 1: 先做教程 1 的全部步骤（Setup Outfit + 隐藏原衣）

Step 2: 处理 Cloth 碰撞体（最难的部分）
  - 在衣服层级下找到带 "_Collider" 后缀的对象
    (Hips_Collider, Spine_Collider 等)
  - 在 Hierarchy 里用 Ctrl/Cmd 多选所有 Collider
  - 在 Inspector 里 Add Component → MA Bone Proxy
  - 把素体的同名骨骼（Hips, Spine...）拖到 Target 字段
  - 你应该看到 Attachment Mode 自动变成 "As child; keep position"

Step 3: 对每个 Collider 重复（教程里 Hips / Spine / Chest 都做一遍）

Step 4: 链接身体形态键
  - 跟教程 1 Step 6 一样
  - 但要分别对 Skirt 和 Tops 两个对象做

Step 5: 验证
  - 进 Play 模式
  - 衣服布料应该跟着素体移动而不穿透身体
```

### 2.3 验证步骤

| 检查点 | 通过标志 | 失败标志 |
|--------|---------|---------|
| Step 2 Collider 配 Bone Proxy | Inspector 显示 Attachment Mode = "As child; keep position" | Mode 还是 "As child; at root" → 没拖骨骼 |
| Play 模式 | 衣服布料自然摆动,不穿模身体 | 布料穿过身体 / 布料乱抖 |

### 2.4 易错点

| 错误 | 原因 | 修复 |
|------|------|------|
| Bone Proxy 加了但布料穿透 | Target 拖错了骨骼 | 检查 Target 是不是同名骨骼（如衣服 Hips → 素体 Hips）|
| Attachment Mode 不自动变 | Target 字段为空 | 先拖 Target 骨骼,Mode 才会自动设置 |
| 布料抖动 / 异常 | Bone Proxy 加在了错误的对象层级 | 只对 **Collider 对象**加,不要加到衣服根 |

### 2.5 何时该学这个

- ✅ 衣服有布娃娃 Cloth 物理效果
- ✅ 衣服有多个 Collider 对象
- ❌ 普通硬质衣服（教程 1 就够）

---

## 教程 3: Simple Object Toggle（简单对象开关）

> 官方举例：开关 **Anon-chan 的连帽衫（hoodie）**
>
> **本文档最重要的教学章节**——90% 玩家第一个要学的功能

### 3.1 官方原文要点

```
步骤:
1. 右键 Avatar → Modular Avatar → Create Toggle
2. 新建的 GameObject 上有 3 个组件:
   - MA Menu Item（菜单项）
   - MA Menu Installer（菜单装到主菜单）
   - MA Object Toggle（实际的开关逻辑）
3. 在 Object Toggle 上点 + → 拖入要开关的对象
4. 勾选 = 选中时"启用"; 不勾选 = 选中时"禁用"
5. 验证:点 Menu Item 上的 Default 复选框,看到物件变化
```

### 3.2 玩家视角操作分解（5 步）

```
Step 1: 右键 Avatar 根对象
  - 在 Hierarchy 选中你的 Avatar（不是衣服、不是配件）
  - 右键 → Modular Avatar → Create Toggle
  - 你应该看到 Avatar 下面多了一个 GameObject

Step 2: 改名（强烈推荐）
  - 选中新建的 GameObject
  - 按 F2 改名（教程里叫 "Hoodie"，你按物件名起）
  - 名字会显示在菜单里

Step 3: 配置 Object Toggle
  - 在 Inspector 找到 MA Object Toggle 组件
  - 点 + 按钮添加一项
  - 把要开关的对象（衣服、配件、发型等）拖到出现的空槽
  - 决定勾选状态:
    * 想"打开菜单时 = 启用物件"→ 勾选
    * 想"打开菜单时 = 禁用物件"→ 不勾选（默认）

Step 4: 验证（不需要进 Play 模式）
  - 在 Inspector 找到 MA Menu Item 组件
  - 点 Default 复选框
  - 你应该**立刻**在 Scene 视图看到物件出现/消失

Step 5: 上传 VRChat 后测试
  - 进 VRChat → 打开菜单
  - 应该看到你命名的开关项
```

### 3.3 验证步骤（**教程 3 最大的特色**）

> ⭐ **MA 最友好的设计**：不需要进 Play 模式,直接点 Inspector 的 Default 复选框就能预览效果！

| 检查点 | 通过标志 | 失败标志 |
|--------|---------|---------|
| Step 1 后 | Avatar 下面多了一个 GameObject,有 3 个组件 | 右键菜单里没有 Create Toggle |
| Step 3 后 | Object Toggle 列表里有你拖入的对象 | 列表为空 → 没拖对象 |
| Step 4 后 | 点 Default 复选框 → 物件出现/消失 | 没反应 → 检查物件路径是否对 |
| 上传 VRChat | 菜单里能看到开关项 | 没有 → Menu Installer 没起作用 |

### 3.4 易错点

| 错误 | 原因 | 修复 |
|------|------|------|
| 右键菜单没 Create Toggle | MA 没装 | 检查 VCC/ALCOM 仓库 |
| 点 Default 没反应 | 没拖对象到 Object Toggle | 回到 Step 3 |
| 上传 VRChat 没看到菜单项 | Menu Installer 配置问题 | 检查 Install To 字段（默认装顶级） |
| 多个物件都开不了 | 参数冲突 | 加 MA Parameters + Internal 模式 |

### 3.5 为什么这个教程最重要

```
教程 3 在整个 6 个教程里的定位:

┌──────────────────────────────────────┐
│  90% 玩家只需要学这一个教程          │
│  + 教程 1（换装）                    │
└──────────────────────────────────────┘

它对应玩家的最高频需求:
- 开关衣服 / 配饰 / 发型
- 切换多个发型
- 关闭显眼的物理效果
```

### 3.6 教学要点

- **不要教手动 Animator 方案**：教程 6 就是手动方案,官方原话"why would you?"
- **永远从 Create Toggle 开始**：除非 Object Toggle 不够用
- **教"Default 复选框预览"**：让玩家秒验证,**降低焦虑**

---

## 教程 4: Edit menus（编辑菜单）

> 教程 4 教两种用法：
> - A. 把 Avatar 现有菜单转成 Hierarchy 对象（编辑）
> - B. 在小组件上加菜单项（重用）

### 4.1 官方原文要点

#### 4.1.1 转换现有 Avatar 菜单

```
步骤:
1. 右键 Avatar → Modular Avatar → Extract menu
2. 新增 Avatar Menu 对象,包含顶级菜单项
3. 展开看菜单项 → 想编辑子菜单 → 点 "extract to objects" 按钮
4. 用拖拽重新组织菜单结构
5. 加新项 → 点 "Add menu item" 按钮（位于菜单列表底部）
```

#### 4.1.2 创建子菜单

```
步骤:
1. 创建子菜单对象
2. 同一对象上加:
   - MA Menu Installer（安装器）
   - MA Menu Item（菜单项，Type = Sub Menu）
3. Submenu Source = Children（让子级成为菜单项）
4. 子级加 MA Menu Item 作为子项
```

#### 4.1.3 Parameter Search（**教学要点**）

```
点参数名旁的下拉箭头（▼）
→ 会搜索所有父级 MA Parameters 组件
→ 自动列出可用参数名
→ 不用手写参数名（容易拼错）
```

#### 4.1.4 菜单不分组（**Menu Group** 高级用法）

```
场景: 想要多个菜单项,但不想创建子菜单

方法:
- 同一对象加 MA Menu Installer + MA Menu Group
- Menu Group 让 Installer 装多个 Item 而不创建 Sub Menu
- 这是 Extract Menu 系统在内部重建菜单的方式
```

### 4.2 玩家视角操作分解

#### 场景 A：编辑现有菜单

```
Step 1: 备份（可选）
  - 复制 Avatar Prefab 一份作为备份
  - 万一改坏了可以恢复

Step 2: 提取菜单
  - 选中 Avatar 根对象
  - 右键 → Modular Avatar → Extract menu
  - 你应该看到 Avatar 下面多了 "Avatar Menu" 对象

Step 3: 查看菜单结构
  - 展开 Avatar Menu
  - 你能看到顶级菜单项（衣服 / 表情 / 状态等）
  - 点某个子菜单项的 "extract to objects" 按钮
  - 能看到嵌套层级的菜单

Step 4: 重新组织
  - 拖拽菜单项改顺序 / 移到不同父级
  - 点 "Add menu item" 加新项

Step 5: 验证
  - 进 Play 模式
  - 打开 VRChat 风格的 Quick Menu
  - 检查菜单结构是否对
```

#### 场景 B：在小组件上创建菜单项

```
Step 1: 创建 GameObject
  - 在小组件的根对象下创建一个子对象（命名随意）

Step 2: 加组件
  - Add Component → MA Menu Installer
  - Add Component → MA Menu Item

Step 3: 配置 MA Menu Item
  - Type = Toggle（开关）或 Sub Menu（子菜单）
  - Parameter = 你要的参数名
    * 点参数名旁的 ▼ 按钮搜索
    * 选你已注册的参数

Step 4: 子菜单的话
  - 改 Type = Sub Menu
  - Submenu Source = Children
  - 给这个对象加子级,每个子级加 MA Menu Item
```

### 4.3 验证步骤

| 检查点 | 通过标志 | 失败标志 |
|--------|---------|---------|
| Extract menu 后 | Avatar 下有 Avatar Menu 对象 | 没有 → MA 没装 |
| 提取子菜单 | 子级嵌套层级可见 | 只有一层 → 没点 "extract to objects" |
| Add menu item | 列表底部出现新项 | 没出现 → 没点对按钮 |
| 上传后 | VRChat 菜单按预期 | 顺序乱 / 缺失 |

### 4.4 易错点

| 错误 | 原因 | 修复 |
|------|------|------|
| Extract menu 后菜单消失了 | 提取时不小心删了原菜单 | 备份！菜单数据本身没丢,只是转成对象 |
| 多个 Is Default 项冲突 | 多个菜单项默认选中 | MA Parameters 里只保留一个 Is Default |
| 参数搜不到 | 没在父级加 MA Parameters 组件 | 在 Avatar 根加 MA Parameters 注册参数 |
| 菜单不显示 | Menu Installer 没启用 | 检查 Installer 组件 enabled |

### 4.5 何时该学这个

- ✅ 想重新组织现有菜单
- ✅ 自己做小组件 / 衣服卖出去
- ❌ 用别人做好的小组件（不需要）

---

## 教程 5: Advanced toggles（高级开关）

> 教程 5 = 教程 3 + 形态键联动
> 官方举例：开关鞋子时**同时**缩袜子形态键（避免穿模）

### 5.1 官方原文要点

```
背景:
- 很多 Avatar 有 "shrink blendshapes"（缩身体部位的形态键）
- 用来在穿衣服时隐藏身体部位避免穿模
- 手动管理这些形态键很烦

步骤:
1. 观察问题:
   - 关闭鞋子后,看到袜子和脚之间有缝
   - 因为两层都被 shrink 形态键缩了

2. 找到两个 shrink 形态键:
   - Anon_body 上的某个形态键
   - Socks 上的某个形态键
   - 全部重置为 0

3. 在鞋子对象上加 Shape Changer:
   - 缩底层形态键
   - 模式选 Delete（性能更好,直接删多边形）

4. 在袜子对象上加 Shape Changer（同样）

5. 用 Overdraw 调试模式（Scene 视图调试叠加）验证
   - Scene 视图 → 调试叠加 → Overdraw
   - 半透明查看穿模

6. 创建菜单子菜单,加开关项

⚠️ 警告: 形态键联动效果在编辑器无法预览
   → 用 Avatar 3.0 Emulator 或 Gesture Manager 在 Play 模式测试
   → 这个限制在未来版本会改进
```

### 5.2 玩家视角操作分解

```
前置: 已完成教程 3（有 Object Toggle）

Step 1: 观察穿模问题
  - 进 Play 模式
  - 开 / 关鞋子 / 袜子,看哪里穿模

Step 2: 找形态键
  - 在衣服 / 身体对象的 Inspector 找到 Skinned Mesh Renderer
  - 展开 Blendshapes 列表
  - 找到名字包含 "shrink" 或 "_off" 的形态键
  - 全部拖到 0（关闭所有缩）

Step 3: 加 Shape Changer
  - 在鞋子对象上:Add Component → Shape Changer
  - Target Renderer: 拖入身体或袜子（被遮挡的那一层）
  - 点 + → 选要影响的形态键
  - 模式选 Delete（默认,且性能更好）

Step 4: 重复袜子对象
  - 同样的步骤

Step 5: 用 Overdraw 验证（**关键调试技巧**）
  - 在 Scene 视图左上角点 "Shaded" 按钮
  - 选 Overdraw
  - 现在场景变半透明,可以"透视"看穿模
  - 如果缩太多 / 缩错,会立刻看到不该空的区域变空

Step 6: 创建菜单
  - 创建子菜单 GameObject
  - 加 Menu Installer + Menu Item (Sub Menu)
  - 子级加 Menu Item (Toggle) → 拖鞋子 / 袜子对象
```

### 5.3 验证步骤

| 检查点 | 通过标志 | 失败标志 |
|--------|---------|---------|
| Step 3 后 | 鞋子对象有 Shape Changer,模式 = Delete | 模式默认应该是 Delete |
| Step 5 Overdraw | 半透明视图能清楚看到重叠 | 看不出来 → 缩的程度太小 |
| Play 模式关鞋 | 没有穿模缝隙 | 还是有缝 → 形态键没选对 |

### 5.4 易错点

| 错误 | 原因 | 修复 |
|------|------|------|
| 编辑器里预览不到效果 | MA 当前版本的限制 | 用 Avatar 3.0 Emulator 或 Gesture Manager 在 Play 模式测试 |
| Overdraw 视图没反应 | 没选对调试模式 | Scene 视图 → Shaded 按钮 → Overdraw |
| 缩了不该缩的部位 | 形态键选错了 | 重置形态键,重新选 |
| 性能变差 | 用了 Set 模式而非 Delete | 没动画 → 用 Delete |

### 5.5 重要概念：Delete vs Set

| 模式 | 行为 | 何时用 |
|------|------|--------|
| **Delete** | 直接删除多边形（性能好,不可动画） | 没有动画控制这个对象时（**90% 情况**） |
| **Set** | 设置形态键为指定值（保留多边形,可通过动画改变） | 有动画可能修改这个对象时 |

> **默认用 Delete**。只有在对象会被其他动画/系统修改时才用 Set。

### 5.6 教学要点

- **教程 5 是教程 3 的延伸**：先学 3,遇到穿模再学 5
- **Overdraw 调试**：教玩家"用眼睛看穿模"而不是"猜"
- **诚实告知限制**：编辑器无法预览 → 告诉玩家怎么绕过

### 5.7 官方原话中的"提示"

> **Outfit authors can preset these Shape Changers**, to allow for easy installation of clothing, with automatically configured blendshapes. The Reactive Object system responds to animations created by other NDMF-compatible systems, so your users don't necessarily need to use Modular Avatar's toggle system to get the benefits of these blendshapes.

**翻译**（创作者向）：
- 服装作者可以**预设** Shape Changers
- 用户装上衣服时自动配置好形态键
- 即使不用 MA 的 toggle 系统,Reactive Object 系统也能响应 NDMF 兼容系统的动画
- → **重用价值很高**：做衣服的人应该预设这些

---

## 教程 6: Building an animator manually（手动构建 Animator）

> ⚠️ **官方原话**："You can also do this by building an animator manually, **but why would you?**"
>
> 这是给**创作者**看的教程,玩家通常不需要学。

### 6.1 教程目标

做一个简单 Prefab：在手上挂个 Cube,通过菜单开关。
**用传统 Animator 方式**实现（教程 3 的 Object Toggle 是更快的方式）。

### 6.2 官方 6 步（不是 9 步）

#### Step 1: 创建 GameObjects

```
- 测试 Avatar 拖到场景
- 在 Avatar 下创建空对象 ToggleDemo
- 在 ToggleDemo 下创建 HandRef
- 在 HandRef 下放 Cube

⚠️ 删 Cube 的 Box Collider（否则影响手部追踪）
```

#### Step 2: 把 Cube 挂到手上

```
- 选中 HandRef
- Add Component → MA Bone Proxy
- Target: 拖入 Avatar 的右手骨头
- Attachment Mode = "As child; at root"
- Cube 会立即 snap 到手上
- 调位置 / 缩放,不要挡住手
```

#### Step 3: 创建 Animator Controller

```
- 创建新 Animator Controller
- 创建 2 个动画 Clip:CubeOff + CubeOn
- Animator 窗口:拖入 2 个 Clip
- 右键 Any State → Add Transition → CubeOff（重复到 CubeOn）
- 加 bool 参数 "Cube"
- Transition Duration = 0
- Can Transition to Self = off
- CubeOff 条件: Cube = false
- CubeOn 条件: Cube = true
```

#### Step 4: 加 MA Merge Animator + 录制动画

```
- 选中 ToggleDemo
- Add Component → MA Merge Animator
- Animator to merge: 拖 Animator Controller
- ✅ delete attached animator（build time 删除）
- ✅ match avatar write defaults（避免 WD 冲突）
- **也加 Animator 组件**,指向同一个 Controller
  → 目的是让 Unity 允许录制动画
  → build time 会被删除

- 打开 Animation 窗口（Ctrl+6）
- 选 CubeOff → 红点录制 → 关 Cube
- 选 CubeOn → 红点录制 → 关 Cube,再开 Cube
```

#### Step 5: 设置参数

```
- 选中 ToggleDemo
- Add Component → MA Parameters
- ✅ Show Prefab Developer Options
- "Cube" 参数自动出现
- Sync Mode = Bool
- ✅ Internal（**重要**: 防止参数冲突）
```

#### Setup 6: 设置菜单

```
- 创建 Expressions Menu 资产
- 加一个 Control,Name = Cube, Type = Toggle
- Parameter = Cube（输入,这时还没在下拉里,正常）

- 选中 ToggleDemo
- Add Component → MA Menu Installer
- 打开 Prefab Developer Options
- Menu to install: 拖刚才创建的 Menu 资产
```

#### Finishing Up: 调整 + 转 Prefab

```
- 调整组件顺序:Menu Installer 放最上面（玩家最常改的）
- 拖 ToggleDemo 到 Project 窗口 → 做成 Prefab
- 拖到任何 Avatar 上 → 直接能用
```

### 6.3 关键设计哲学

#### 6.3.1 Internal Checkbox（**最重要的概念**）

> **If you set the internal checkbox, modular avatar will ensure that your `Cube` parameter doesn't interfere with anything else on the avatar using the same parameter name.**

| 选项 | 行为 | 何时用 |
|------|------|--------|
| **Internal ✅** | MA 自动避免参数名冲突 | **默认推荐**,99% 情况用这个 |
| **Internal ❌** | 用户可手动改名,可能冲突 | 多个小组件需要共享参数时 |

#### 6.3.2 MA Parameters 的位置约束

> **Make sure that `MA Parameters` is on either the same object, or a parent of all your `Merge Animator`s and `Menu Installers`!**

**翻译**：`MA Parameters` 必须放在：
- 所有 `Merge Animator` 的**同一对象**
- **或父级**

否则参数找不到！

#### 6.3.3 "也加 Animator 组件" 的目的

> **Merge Animator doesn't need to be at the top level GameObject. Feel free to put it further down the hierarchy if you prefer.**

> **Adding an Animator here is also optional; we're just using it so that Unity allows us to record animations. By checking the `delete attached animator` box, Modular Avatar will delete the `Animator` component at build time.**

**翻译**：
- Animator 组件加不加都无所谓
- 只是为了让 Unity 允许录制动画（Unity 的限制）
- `delete attached animator` 会在 build time 删除

### 6.4 验证步骤

| 检查点 | 通过标志 | 失败标志 |
|--------|---------|---------|
| Step 2 后 | Cube 在右手位置 | Cube 在原点 → Bone Proxy 没配 |
| Step 4 后 | Animation 窗口能看到 CubeOff / CubeOn | 没有 → 没选 ToggleDemo |
| Step 5 Internal | Cube 参数出现,Internal 勾选 | 没勾选 → 命名可能冲突 |
| 上传 VRChat | 菜单有 Cube 开关,开关 Cube 出现/消失 | 没出现 → Menu Installer 没装 |

### 6.5 易错点

| 错误 | 原因 | 修复 |
|------|------|------|
| 参数冲突 | 没勾 Internal | 勾上 Internal |
| 菜单没显示 | MA Parameters 位置不对 | 移到 Merge Animator / Menu Installer 的同一对象或父级 |
| Cube 不出现 | Animator 录制时没开 Cube | 重录 CubeOn |
| WD 警告 | 没勾 match avatar write defaults | 勾上 |
| Write Defaults 警告 | Avatar 用 ON,你用 OFF（或反之） | 勾上 match avatar write defaults |

### 6.6 教程 6 vs 教程 3 对比

| 维度 | 教程 3 (Object Toggle) | 教程 6 (Manual Animator) |
|------|----------------------|-------------------------|
| 难度 | ⭐ 新手友好 | ⭐⭐⭐ 需要 Animator 基础 |
| 步骤 | 5 步 | 6 步（实际更繁琐） |
| 玩家 | 适合所有玩家 | 适合创作者 |
| 维护 | 加新开关 = 加新 GameObject | 加新开关 = 改 Animator + 加新 Controller |
| **官方建议** | **默认用这个** | "why would you?" |

> **教学要点**：**90% 玩家永远不应该学这个教程**。但创作者必须理解,因为某些复杂场景（如复杂多状态机）必须用 Animator。

---

## 教学衔接：先学哪个？

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

---

## 教学决策表（玩家提问时怎么定位）

| 玩家问题 | 教哪一节 | 关键概念 |
|---------|---------|---------|
| "我刚买了个衣服,怎么装？" | 教程 1 | Setup Outfit |
| "想加个开关菜单" | 教程 3 | Create Toggle |
| "装上了但和身体穿模" | 教程 5 | Shape Changer + Overdraw |
| "调体型衣服不变形" | 教程 1 Step 6 | Blendshape Sync |
| "装上鞋子陷地了" | 主文档 §7.11 | Floor Adjuster |
| "多个小组件参数冲突了" | 主文档 §7.3 | MA Parameters + Internal |
| "我想做自己的衣服卖给别人" | 教程 4 + 教程 6 | Menu + Animator |
| "我有布娃娃衣服" | 教程 2 | Bone Proxy + Collider |
| "我想重新组织现有菜单" | 教程 4 | Extract menu |
| "完全不会 Unity" | 教程 1 + 教程 3（先看） | 看不懂再来问 |

---

## 教学语言风格（玩家 vs 高级）

### 默认叙述（新手）

```
✅ "把衣服拖到 Avatar 身上"
✅ "右键选 Setup Outfit"
✅ "你应该看到 X"
❌ "执行 NDMF 编译管线"
❌ "调用 Merge Armature 组件的 merge 流程"
```

### 专业叙述（高级玩家）

```
✅ "NDMF 在 Generating 阶段执行 Merge Armature pass"
✅ "Layer Priority 控制 Animator 合并顺序"
✅ "Write Defaults 匹配避免混用 ON/OFF 状态"
```

### 转换触发

当玩家说出这些词时,可切换专业叙述：
- Animator Layer
- Write Defaults
- Blend Tree
- NDMF
- Constraint
- Expression Parameter
- PhysBone

---
