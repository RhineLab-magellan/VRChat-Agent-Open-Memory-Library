# Udon Node Graph | 主页

> 来源: https://creators.vrchat.com/worlds/udon/graph/
> 更新日期: 2024-08-21
> 索引日期: 2026-06-15
> Domain: World / Udon

Udon Node Graph 是 Udon 程序的**默认可视化创建界面**。如果你想直接看示例,可以参考 Udon Example Scene。

> **本 Agent 主要服务 UdonSharp 工程师**,但 Node Graph 文档对理解**节点/事件/类型系统**至关重要,常用于调试和参考。
> 两种入口对比:
> - **Node Graph** (本文件) — 可视化编程,无类型错误,即时编译
> - **UdonSharp** — C# 入口,工程化、版本控制友好(详见 `../udonsharp/` 目录)

---

## Interface

打开 Udon Graph 窗口有两种方式:
1. **菜单栏**: `VRChatSDK > Udon Graph`
2. **组件按钮**: 在 `UdonBehaviour` 组件上点击 `Open Udon Graph` 按钮

通过菜单打开时,会看到 **Welcome Screen**(欢迎屏幕),包含 Changelog 和一些设置。

### 多标签支持

- 可以**同时打开多个 Graph**
- 顶部 **Tabs** 切换
- 点击 Tab 角落的 `X` 关闭

> ⚠️ Graph Tabs **不是真正的 Unity Tab 系统**,每次切换 = 重新打开 = 切换开销
> **【推断】** 多 Tab 时建议只保留当前活动的 1-2 个窗口,避免内存与重编译开销

---

## Flow(流)

**Flow** 定义了哪些节点会运行,以及它们的执行顺序。

### 核心概念

- 图中的**三角形 (Flow ports)** 触发顺序:**从左到右**,沿连接的 Noodles 传递
- 阅读/编写 Graph 时,**沿 Flow 顺序阅读**是第一步
- **Highlight Flow** 开关(顶栏)可高亮所有通过 Flow 边连接的节点,辅助理解执行路径

### 规则

> 如果节点**没有任何 Flow 连接**,则**什么都不会发生**(节点不会被执行)

### 示例:Hello / Goodbye

```
Start ─→ Branch(checkbox) ─┬─ True  ─→ SendCustomEvent("Hello")
                            └─ False ─→ SendCustomEvent("Goodbye")
```

1. `Start` 事件在世界加载时触发
2. `Branch` 检查其 checkbox 值
3. True → 触发 "Hello" 自定义事件
4. False → 触发 "Goodbye" 自定义事件

---

## Creating Nodes

Node 是代表可触发方法的盒子。构建 Graph = 创建 + 连接节点。

### 创建节点的 3 种方式

| 方式 | 适用场景 |
|------|---------|
| **Hotkeys(快捷键)** | 快速插入常用节点 |
| **Drag-and-Drop(拖放)** | 从 Hierarchy 拖入 GameObject/Component,或从 Variables 面板拖入变量 |
| **Search Menus(搜索菜单)** | 通过 Quick Search / Full Search 搜索任意方法 |

### Hotkeys(创建节点的快捷键)

按住以下键,然后**点击 Graph 任意位置**即可创建对应节点:

| 快捷键 | 节点 |
|--------|------|
| `1` | float |
| `2` | Vector2 |
| `3` | Vector3 |
| `4` | Vector4 |
| `+` | float addition(加法) |
| `-` | float subtraction(减法) |
| `=` | float equality comparison(等于比较) |
| `b` | Branch |
| `shift+b` | Block |

### Other Hotkeys(其他快捷键)

| 快捷键 | 功能 |
|--------|------|
| `C + click` | 将**常量**转换为**变量** |
| `Shift + A` | 对齐选中节点 |
| `Ctrl + G` | 快速分组(Quick Grouping) |
| `L + click` | 记录选中节点的值到日志 |
| `Shift + F + click` | 对输出**数组类型**的节点,自动生成 `foreach` 循环 |

> 大多数这些功能也可以在节点的**右键菜单**中找到。

### Drag and Drop

#### 拖入 GameObject / Component

从 Hierarchy 拖动一个 Light 组件的 `'Light'` 标题到 Graph 上:
- 自动创建一个**绑定到该组件的 Variable**
- 在 Variables 窗口出现新变量
- Graph 中生成一个**预配置的 Get Variable 节点**

#### 拖入 Variables(从 Variables 面板)

| 操作 | 行为 |
|------|------|
| 点击 Variables 面板的 `+` | 任意类型创建变量 |
| 拖动变量名到 Graph | 创建 **Get Variable** 节点 |
| `Ctrl + 拖动` | 创建 **Set Variable** 节点 |
| `Alt + 拖动` | 创建 **On Variable Changed** 节点 |

### Searching for Nodes

按 `Space` 打开 **Quick Search**,输入要交互的类的前几个字母。
此方法最适合**了解 Unity 基础类与对象类型**的用户。

> 详细搜索语法见 [`searching-for-nodes.md`](./searching-for-nodes.md)

---

## Compiling the Graph(编译)

Graph **自动在后台以固定间隔编译**:
- 编译时,Graph 右上角**闪烁**
- **Status box**:
  - 🟢 **绿色** = 成功
  - 🔴 **红色** = 出错
- 点击 Status box 可查看:
  - 成功 → 生成的 **Assembly Code**
  - 失败 → **错误列表**

> **【推断】** 自动编译的频率可降低"忘记编译"的失误,但对于大型 Graph 可能产生频繁重编译开销

---

## Running the Graph(运行)

### Running In-Editor(在编辑器中运行)

使用 Unity 的 `Play` 按钮直接运行场景测试。

⚠️ 以下功能**不会按预期工作**:
- **Synced Variables(同步变量)**
- **Networked Events(网络事件)**

### Running Build & Test(构建并测试)

通过 **VRChat SDK Window** 进行 Local Testing:
- 将内容打包为**离线世界**
- 启动**真正的 VRChat 客户端**
- 提供可与对象交互的 Avatar 与 VRCPlayerAPI 请求

#### 测试多客户端

使用 `Number of Clients` 字段启动**最多 8 个本地客户端**:
- 所有客户端使用**相同 DisplayName**
- 但被识别为**独立玩家**
- 适合测试交互

> 如果 `Force Non-VR` 不生效:切换到 VRChat SDK Window 的 `Settings` 选项卡,设置 **VRChat Client Path** 指向实际安装路径。

---

## Uploading Your World

- **Build & Test**: 创建 VRChat Account 后即可使用
- **发布世界**: 需在 VRChat 中度过一些时间(访问世界、结交朋友、获取灵感)

---

## 视觉编程核心优势

> **【推断】** 相对于 UdonSharp 的优势

| 优势 | 说明 |
|------|------|
| **无类型错误** | 端口类型匹配由系统强制,端口之间用颜色区分 |
| **即时编译** | 自动后台编译,所见即所得 |
| **节点式调试** | 节点可视化,Highlight Flow 可追踪执行路径 |
| **学习曲线低** | 非程序员也可入门,适合快速原型 |
| **API 探索** | 通过 Quick Search 浏览可用的 VRC/Unity API |

## 相关知识库

- `event-nodes.md` — 完整 Event 节点列表
- `graph-elements.md` — Graph 元素(Groups/Comments/Noodles)
- `searching-for-nodes.md` — 节点搜索方法
- `special-nodes.md` — 特殊节点(Block/Branch/Loop/ForEach/...)
- `type-nodes.md` — 类型引用节点
- `../udonsharp/` — C# 入口
- `../../api/events-reference.md` — Udon 事件完整参考
