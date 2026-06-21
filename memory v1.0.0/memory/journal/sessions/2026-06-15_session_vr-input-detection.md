# Session: VR 控制器 X 键检测与 Udon Input 限制

> Date: 2026-06-15
> Agent: VRChat Technical Architect
> Scope: Hybrid (Avatar + World + OSC) — VR 控制器按键检测

---

## 任务目标

用户提问:"VRC有提供VR左手手柄的X键的识别方法吗?",并要求补充:
1. InputJump 能够检测到哪些按钮?
2. 将本次发现的知识补充到知识库

---

## 关键发现

### 1. 三个域的 X 键检测能力对比

| 域 | 官方支持 | 关键事实 |
|----|---------|---------|
| **Avatar (Expression Parameters)** | ✅ 框架支持 | 通过 VRChat 内置 InputDriver 绑定到 Animator 参数,但官方未公开完整按键名清单 |
| **World/UdonSharp (Udon Input Events)** | ❌ 抽象层 | 8 个事件(4 按钮 + 4 轴)无法识别具体 face 按钮;`handType` 仅区分左右手 |
| **World/UdonSharp (Unity Input.GetButton)** | ✅ 可用 | `Oculus_CrossPlatform_Button2` 等预设轴名;但 Unity 2022 `GetButtonDown/Up` 有 bug |
| **OSC (官方 Input Control)** | ❌ 不支持 | `/input/Jump`、`/input/Use` 等语义化地址,**不暴露 X/Y/A/B** |
| **OSC (第三方桥接)** | ✅ I5UCC/VRCThumbParamsOSC | 通过 SteamVR Controller Actions 读取,转 Avatar Parameters 输出 |

### 2. InputJump 精确检测范围(用户追问)

**【FACT,来自官方文档 `creators.vrchat.com/worlds/udon/input-events`】**

| 平台 | 触发按键 | 备注 |
|------|---------|------|
| Desktop | Spacebar | 明确 |
| VR 控制器 | "typically a face button" | **官方未明确**具体是哪个 face 按钮 |

**InputJump 是抽象跳跃动作**,无法识别:
- 哪个 face 按钮(X/Y/A/B)触发
- VR 控制器上的具体按键(只能通过 `handType` 知道左右手)

**【未确认】** 社区推断:Meta Quest Touch 上 InputJump 通常映射到右手 A 键或左手 X 键(取决于 VRChat 内部配置),但官方未公开此映射。

### 3. 精确识别 X 键的标准做法

#### Udon 域(World 交互)
```csharp
// ⚠️ Unity 2022 中 GetButtonDown/Up 损坏,需手动模拟
bool xHeld = Input.GetButton("Oculus_CrossPlatform_Button2");
```

**关键陷阱**:
- 🔴 VCC vs ALCOM:ALCOM 创建项目 InputManager 仅有 18 个默认轴(无 VR 预设),**必须用 VCC**
- 🔴 Unity 2022 `GetButtonDown/Up` 损坏(VRChat feedback 已知 bug)
- 🟡 Quest 2 上 X 键响应不稳定(社区报告"every ~10 clicks")
- 🟡 轴名跨厂商不通用(Oculus_CrossPlatform_* 是 Meta 命名)

#### Avatar 域(动效触发)
在 Expression Parameters 资产中 Add 参数,Inspector 选择 VR InputDriver,绑定到 Animator 的 FX/Action Layer。

#### OSC 域(外部应用)
**官方不支持**原始 VR 按键。必须用 [I5UCC/VRCThumbParamsOSC](https://github.com/I5UCC/VRCThumbParamsOSC):
- 命名约定:`LeftAButton` = 左手 X,`LeftBButton` = 左手 Y
- 通过 SteamVR Controller Actions 读取,转 Avatar Parameters
- 支持设备:Valve Index / Meta Touch / SteamVR Trackers / XInput

---

## 知识库更新

### 1. `memory/world/udon/input-events.md` — 新增"精确按键识别限制"章节

**位置**:在 "与知识库互补" 章节前

**新增内容**:
- ⚠️ 关键约束:Udon Input Events 是抽象动作层,无法识别 X/Y/A/B
- 官方 "typically" 描述分析
- 精确识别 X 键的代码示例(Unity Input + 手动 bool 模拟)
- 常用轴名清单(Oculus_CrossPlatform_Button0-10)
- 5 个关键陷阱(VCC/ALCOM 差异、Unity 2022 bug、Quest 兼容性、跨厂商、玩家重映射失效)
- 4 个场景的推荐策略

### 2. `memory/hybrid/osc-protocol.md` — 新增"官方 OSC 不暴露原始 VR 硬件按键"声明

**位置**:在 "4. Input Control API" 章节末尾(Tracking API 之前)

**新增内容**:
- 关键约束:官方 OSC Input Control API 不暴露 X/Y/A/B
- 官方语义化输入地址列表(~15 个)
- 第三方 OSC 桥接程序对比表
- I5UCC/VRCThumbParamsOSC 完整参数清单(LeftAButton 等)
- 使用方式(5 步) + 延迟警告(50-200ms)
- Udon 内直接读取的替代方案 cross-reference

### 3. Cross-references 已添加

`input-events.md` → `osc-protocol.md` → Avatar Expression Parameters
形成"抽象层 → Unity Input → 第三方 OSC"的完整导航

---

## 风险与未知

**【未确认】**
- Avatar Expression Parameters 的完整 VR InputDriver 名称清单(官方未公开)
- VRChat 内部 InputJump 在不同 VR 控制器上的精确 face 按钮映射
- I5UCC/VRCThumbParamsOSC 在 Quest 3 / Pico 上的兼容性

**【已知风险】**
- Unity 2022 的 GetButtonDown/Up bug 仍是 World 项目常见坑点
- ALCOM 项目 InputManager 不完整会导致"运行时 X 键无响应"
- X 键在 Quest 上的跨 SDK 版本表现可能不一致

---

## 反思

### 设计模式观察
- **抽象层 vs 硬件层**:VRChat InputJump 是语义化抽象(优点:跨平台/响应重映射,缺点:无法精确定位)
- **官方缺位 → 第三方补位**:OSC 缺 X 键 → VRCThumbParamsOSC 桥接 SteamVR
- **VCC 不可替代**:ALCOM 缺少 86 个 VR 预设轴,World 项目必须用 VCC

### 知识库改进点
- ✅ 已补:Input Events 抽象层限制 + Unity Input 陷阱 + OSC 缺位声明
- 🔴 仍缺:Avatar Expression Parameters InputDriver 完整列表(需要直接读 SDK 源码或实测)
- 🔴 仍缺:Quest 2 上 `Oculus_CrossPlatform_Button2` 实际可用性的实测数据

---

## 用户交互摘要

1. 用户问:"VRC有提供VR左手手柄的X键的识别方法吗?"
2. Agent 给出三层级答案(Avatar / World / OSC)
3. 用户问:"InputJump能够检测到哪些按钮?"
4. Agent 回答(基于知识库 + 外部搜索):Spacebar + face 按钮(官方未明确具体)
5. 用户说:"补充"
6. Agent 执行知识库更新(2 个 Edit + 1 个 journal 记录)
