# VRCFury 完整参考 — Non-Destructive Avatar 工具与优化系统

> 状态：⚠️ **仍活跃维护**（2026-05-02 最新提交），但被 Modular Avatar 覆盖部分场景
> 来源：https://github.com/VRCFury/VRCFury + https://vrcfury.com + https://github.com/VRCFury/vrcfury.com

---

## ⚠️ 重要修正记录

知识库 2026-06-05 曾将 VRCFury 标记为"❌ 已过时"——此判断**措辞不当**，事实反证：

| 维度 | 实际情况 |
|------|----------|
| **维护状态** | ✅ 活跃（2026-05-02 提交 "disable lv hook for now"） |
| **代码规模** | C# 98.9% + HLSL 1.1% |
| **官方下载页** | https://vrcfury.com 仍提供 |
| **核心定位** | "Non-Destructive Tools for VRChat Avatars" |

**正确表述**：VRCFury **不是过时**，而是 **"与 MA 功能重叠 + 共存有冲突 + 安装方式非 VPM"** 三重原因导致社区在大多数场景下推荐 MA。

---

## 1. 项目概览

| 属性 | 值 |
|------|-----|
| **仓库** | https://github.com/VRCFury/VRCFury |
| **官网** | https://vrcfury.com |
| **文档仓库** | https://github.com/VRCFury/vrcfury.com |
| **下载方式** | ❌ **非 VPM**，从官网下载 `.unitypackage` 手动导入 |
| **文档位置** | vrcfury.com 主页 + Discord 社区 |
| **维护状态** | ✅ 活跃（2026-05-02 最后提交） |
| **代码规模** | C# 98.9% + HLSL 1.1% |
| **核心哲学** | Non-Destructive（非破坏性）：上传前复制，原始文件永不修改 |
| **兼容 WD** | ✅ Write Defaults ON 和 OFF 均支持 |

---

## 2. 核心组件完整清单

### 2.1 主要组件

| 组件 | 用途 | MA 对应 | 评价 |
|------|------|---------|------|
| **Toggle** | 菜单开关/按钮/滑块（GameObject/BlendShape/Material/动画） | ✅ MA Toggle | 功能更丰富（Transition State、Exclusive Tags、Slider Wheel） |
| **Gestures** | 手势动画自动化 | ⚠️ 需手动 | VRCFury 优势 |
| **Full Controller** | 合并完整 Controller + Menu + Parameters | ✅ MA MenuInstaller | Prefab 制作者友好 |
| **Armature Link** | 服装/道具骨骼绑定 | ✅ Merge Armature | 类似 |
| **Global Collider** | 全局 PhysBone Collider / Contact Sender | ⚠️ 手动配置 | 方便 |
| **Toggle** | 菜单 Toggle / Button / Slider | ✅ 需手动组装 | MA 部分覆盖 |

### 2.2 优化组件（⭐ 核心优化能力）

| 组件 | 优化方向 | 原理 | 效果 |
|------|----------|------|------|
| **Parameter Compressor** ⭐ | 压缩同步参数 | 所有菜单控制的 Float/Int 参数压入 **16 bit** | 253 bit → 125 bit（实测） |
| **Direct Tree Optimizer** ⭐ | 减少 Animator 层数 | 非冲突层合并为**单个 Direct Blend Tree 层** | 显著减少 frametime |
| **Blendshape Optimizer** ⭐ | 减少 VRAM | 烘焙所有**非动画 BlendShape** 到 Mesh | 免费减少 VRAM |
| **Fix Write Defaults** | 修复 WD 冲突 | 自动检测并对齐所有状态的 WD 设置 | 消除 WD 混合导致的 bug |

### 2.3 功能组件

| 组件 | 用途 |
|------|------|
| **Advanced Visemes** | 用 VRCFury Action 作为口型（支持骨骼变换替代 BlendShape） |
| **Anchor Override Fix** | 确保所有 Mesh 使用同一 Anchor Override（统一环境光照） |
| **Apply During Upload** | 上传时执行指定 Action（如：编辑器显示 BlendShape 但上传时关闭） |
| **Blendshape Link** | 服装 BlendShape 自动链接到身体 BlendShape |
| **Blink Controller** | 自定义眨眼控制（避免双击手势时的"双重眨眼"） |
| **Bounding Box Fix** | 确保所有 Mesh 有足够大的 Bounding Box（VR 视角不消失） |
| **Cross-Eye Fix** | 通过旋转约束消除眼球 Roll（斗鸡眼修复） |
| **Delete During Upload** | 上传时删除指定对象及其子对象 |
| **Droppable** | 添加"丢弃"功能（World Constraint） |
| **Gizmo** | 仅编辑器可见的标记（不影响游戏） |
| **MMD Compatibility** | MMD 世界兼容（保持 BlendShape、避免干扰层、禁用手势动画） |
| **Move Menu Item** | 移动菜单项路径 |
| **Override Menu Icon** | 覆盖菜单图标 |
| **Override Menu Settings** | 修改 VRCFury 默认 "Next" 菜单项 |
| **Remove Hand Gestures** | 移除非 VRCFury Controller 中的手势功能 |
| **Security Pin Number** | 安全密码锁（4-10 位数字 PIN） |
| **Security Restricted** | 需要 PIN 码才能启用的对象 |
| **Senky Gesture Driver** | 特定手势布局（Senky 风格） |
| **Show In First Person** | 第一人称视角可见（通过 Constraint 实现） |
| **Toes Puppet** | 脚趾控制滑块 |
| **When-Talking State** | 说话时激活指定 Action |

### 2.4 SPS (Super Plug Shader)

| 属性 | 说明 |
|------|------|
| **类型** | 免费变形 Shader（替代 DPS/TPS） |
| **兼容 Shader** | Poiyomi Toon/Pro 7/8+, lilToon, UTS, Mochie, XSToon, Silent, Standard 等 |
| **支持** | Rigged + Un-rigged Mesh、BlendShape 动画、Avatar Scaling |
| **向后兼容** | 所有 TPS 和 DPS 系统 |
| **限制** | 最多 2 Socket + 无限 Plug；附近有 Point Light 时降至 1 Socket |

---

## 3. ⭐ 核心优化技术详解

### 3.1 Parameter Compressor（参数压缩器）— 压参数核心

> **核心能力**：将所有菜单控制的 Float 和 Int 同步参数压缩为 **16 bit 总同步量**

#### 原理

VRChat Avatar 的 Expression Parameter 有 256 bit 同步预算。大量 Avatar（特别是有面部追踪的）很容易用完这些预算。Parameter Compressor 使用**指针式浮点同步**技术：

```
传统方式：10 个色相滑块 = 10 × 8 bit = 80 bit
压缩后  ：10 个色相滑块 = 16 bit（指针 + 数据）
节省    ：64 bit
```

#### 技术实现（Pointer-Based Float Sync）

1. **本地化**：所有 Radial Puppet 的 Float 参数变为**本地参数**（不同步）
2. **指针 + 数据**：使用 1 个 Int（指针，8 bit）+ 1 个 Float（数据，8 bit）= 16 bit 同步
3. **Copy Driver**：通过 `VRC Avatar Parameter Driver` 在数据字段和实际参数之间复制
4. **变更检测**：使用 Blend Tree 数学运算检测哪个参数发生了变化
5. **优先级发送**：变化的参数优先通过指针发送
6. **远程平滑**：远端 Avatar 上参数经过平滑处理（因 Copy Driver 丢失了 IK 同步）

#### 排除规则

| 排除类型 | 原因 |
|----------|------|
| **非菜单控制参数** | 可能由 OSC 驱动（面部追踪等） |
| **Two/Four Axis Puppet 参数** | 用于尾巴、耳朵等实时控制 |
| **Parameter Driver 驱动参数** | 可配置排除（避免与自动驱动冲突） |

#### ⚠️ 兼容性警告

| 冲突项 | 说明 |
|--------|------|
| **MA Sync Parameter Sequence** | ❌ 两者都重排参数槽位，不可共存 |
| **d4rkAvatarOptimizer** | ⚠️ VRCFury 在 d4rk 之后运行，可能影响优化 |

### 3.2 Direct Tree Optimizer（直接树优化器）— 减层数核心

> **核心能力**：将所有非冲突 Animator 层转换为**单个 Direct Blend Tree 层**

#### 原理

VRChat Avatar 的 FX Controller 通常有大量简单 Toggle 层（每个层只有 ON/OFF 两个状态）。每个 Animator 层都有**固定计算开销**（权重计算、状态机更新）。Direct Blend Tree 可以在**单层**内并行处理所有 Toggle。

```
优化前：50 个 Toggle = 50 个 Animator 层（每层独立计算）
优化后：50 个 Toggle = 1 个 Direct Blend Tree 层（并行计算）
```

#### Direct Blend Tree 技术

| 要素 | 说明 |
|------|------|
| **Blend Type** | `Direct`（每个子项由独立 Float 参数控制权重） |
| **Weight 参数** | 常量 `1`（不参与同步） |
| **Toggle 参数** | Bool 同步 → 自动转 Float（1 bit 成本） |
| **Write Defaults** | 必须 **ON**（否则 Blend Tree 行为异常） |
| **动画结构** | 每个 Toggle = 子 Blend Tree（Off 动画 + On 动画） |

#### 自动优化范围

以下 VRCFury 组件会自动应用 Direct Tree 优化：
- Toggles
- Gestures
- Full Controllers
- SPS
- Advanced Visemes

#### 可优化条件（层必须满足）

| 条件 | 说明 |
|------|------|
| **无 State Behaviour** | 层内没有 Animator Behaviour |
| **仅两状态** | 恰好两个 State（ON/OFF） |
| **互相转换** | 两个 State 的 Transition 互相指向对方 |
| **条件对称** | 一个 State 的条件是另一个的逆 |
| **无冲突属性** | 不与其他层动画化相同的属性 |

### 3.3 Blendshape Optimizer（BlendShape 优化器）— 减 VRAM

> **核心能力**：自动烘焙所有**非动画** BlendShape 到 Mesh 基础形状

#### 原理

Avatar Mesh 通常有大量 BlendShape（面部表情、身体调整等），但很多 BlendShape 在动画中**从未被使用**（如模型师预设的体型调整）。每个 BlendShape 都占用 VRAM（存储顶点偏移数据）。

```
优化前：Body Mesh 有 80 个 BlendShape（其中 50 个从未动画化）
优化后：Body Mesh 有 30 个 BlendShape（50 个已烘焙进基础形状）
VRAM 节省：50 个 BlendShape 的顶点偏移数据
```

#### 特性

| 特性 | 说明 |
|------|------|
| **零配置** | 无需任何设置，自动检测 |
| **非破坏性** | 原始 Mesh 不被修改（仅上传时处理） |
| **安全性** | 只烘焙确认未被动画引用的 BlendShape |
| **MMD 兼容** | 配合 MMD Compatibility 组件可保留 MMD 相关 BlendShape |

### 3.4 Fix Write Defaults（WD 修复器）

> **核心能力**：自动检测并对齐所有 Animator 状态的 Write Defaults 设置

#### WD 问题分类

| 问题 | 后果 | VRCFury 处理 |
|------|------|-------------|
| **Additive 层 WD Off** | BlendShape 值 ×3，无关 Transform 持续移动 | 自动标记 WD On |
| **Direct BlendTree WD Off** | 无关动画断裂 | 自动标记 WD On |
| **WD On/Off 混合** | Unity 破坏所有动画 | 检测并自动对齐 |
| **Missing Animation** | WD Off 时 Transform 断裂 | 替换为空 1 秒 Clip |

#### 工作模式

| 模式 | 说明 |
|------|------|
| **Auto** | 自动选择需要最少改动的方向（On 或 Off） |
| **Force On** | 强制所有状态 WD On |
| **Force Off** | 强制所有状态 WD Off |
| **Disabled** | 不做任何修改 |

---

## 4. Actions 系统

VRCFury 的 Toggle、Gesture、SPS 等组件都通过 **Actions** 执行具体操作：

| Action | 用途 |
|--------|------|
| **Object Toggle** | 开启/关闭 GameObject |
| **BlendShape** | 动画化 BlendShape 到指定值 |
| **Animation Clip** | 播放预制动画片段（路径自动重写） |
| **Poiyomi Flipbook Frame** | 动画化 Poiyomi Flipbook 当前帧 |
| **Poiyomi UV Tile** | Poiyomi UV Tile Discard 开关 |
| **SCSS Shader Inventory** | SCSS Shader 库存切换 |
| **Material Property** | 动画化材质属性（支持全 Renderer） |
| **Scale** | 缩放对象（乘数模式） |
| **Material Swap** | 替换材质 |
| **Enable SPS** | 启用/禁用 SPS Plug 变形 |
| **Set an FX Float** | 驱动 FX 参数到指定值 |
| **Disable Blinking** | 禁用眨眼和眼球追踪 |
| **Disable Visemes** | 禁用口型/嘴唇同步 |
| **Reset Physbone** | 重置 PhysBone 到静止位置 |
| **Flipbook Builder** | 翻页式动画（每页 = 一个关键帧） |
| **Smooth Loop Builder** | 平滑循环动画（呼吸等） |

---

## 5. Automatic Fixes（自动修复）

VRCFury 在项目存在时自动修复 **60+** 个已知 VRChat/Unity bug：

### 5.1 Avatar 修复（需包含 VRCFury 组件）

| 问题 | 修复方式 |
|------|----------|
| **Animator Override Controller 不支持** | 自动展平为普通 Controller |
| **肌肉动画 Transition 时间在 Layer 0 被忽略** | 插入空基础层 |
| **FX 层被损坏（Generic ↔ Humanoid 切换）** | 保留正确 FX Controller，替换损坏的 |
| **已删除层的资产仍包含在上传包中** | 重建 Controller，仅包含实际使用的层和状态 |
| **空 Controller 层仍消耗处理时间** | 自动移除保证为空且无副作用的层 |
| **目标无效对象的动画仍消耗处理时间** | 自动移除无效动画属性 |
| **Gesture/FX 层 Transform 冲突** | 将非肌肉动画从 Gesture 移到 FX 顶部 |
| **256 个唯一参数限制** | 检测并显示有用错误消息 |
| **256 个 Contact 限制** | 检测并显示有用错误消息 |
| **参数名空格/下划线冲突** | 自动重命名冲突参数 |
| **参数名包含 `[]`** | 自动重命名 |
| **参数类型不匹配（Int→Bool）** | 自动修正 Transition 条件 |
| **None Controller 导致 AudioSource 每帧重启** | 替换为空 Controller |
| **非移动材质仍包含在 Quest 上传包** | 自动移除 |
| **Tracking Control 过早执行被忽略** | 缓冲并多次重复执行 |
| **PhysBone 未标记 Animated 破坏全身动画** | 自动标记所有 Humanoid 骨骼上的 PhysBone |
| **VR 视角小 Bounding Box 消失** | 自动增大所有 Renderer Bounds（最多 1 米） |
| **VRCSDK 上传失败（Streaming Mip-Maps）** | 自动克隆纹理并启用 |
| **菜单图标过大/未压缩** | 自动克隆并压缩/调整大小 |
| **Audio Clip 未设置 Load in Background** | 自动克隆并启用 |
| **Unity Constraint → VRC Constraint** | 上传时自动升级 |
| **粒子系统触发安全检查** | 自动修正设置 |
| **FX Controller 无效参数类型破坏镜像克隆** | 自动移除 |
| **跨平台参数顺序对齐** | 自动对齐移动平台参数顺序 |
| **菜单项无效类型** | 转换为 Button |
| **材质属性默认值从错误 Material Slot 读取** | 在顶部 Defaults 层强制记录 |

### 5.2 VRCSDK 修复

| 问题 | 修复方式 |
|------|----------|
| **Android 验证在 Windows 模式错误触发** | 自动同步回正确值 |
| **Play Mode Contact Self/Others 不区分** | 自动调整 playerId |
| **无用 XR 文件夹** | 移入临时 Package |
| **Animator 窗口无法关闭** | 补丁修复 |
| **脚本重载后切换回 Authentication 标签** | 自动切换到 Builder |
| **Contact 相关 Animator 垃圾消息** | 补丁修复 |
| **AmplitudeAPI 错误（pihole/adguard）** | 隐藏非可操作消息 |
| **Collider Transform 被编辑器覆盖** | Play Mode 时阻止 |
| **Collider Transform 未正确计算** | 每次 Build 开始强制重算 |
| **Collider 镜像偏移不正确** | 补丁修复镜像逻辑 |

### 5.3 Unity 修复

| 问题 | 修复方式 |
|------|----------|
| **Mesh Data Optimization 耗时极长** | 自动禁用（不必要且极慢） |
| **Play Mode 脚本重载** | 改为 "Recompile After Finished Playing" |
| **Play Mode Domain Reload** | 自动禁用（大幅加速进入 Play Mode） |
| **Mono 非英语 locale + Harmony bug** | 补丁修复 Assembly.GetName() |
| **Animator Controller 编辑器 spam** | 补丁修复 |

---

## 6. Toggle 组件详细功能

### 6.1 核心选项

| 选项 | 说明 |
|------|------|
| **Menu Path** | 菜单路径（用 `/` 创建子菜单） |
| **Saved Between Worlds** | 跨世界保存状态 |
| **Use Slider Wheel** | 转为 Radial 滑块 |
| **Protect with Security** | PIN 码保护 |
| **Default On** | 默认开启（Rest Pose 可见） |
| **Show/Hide when animator disabled** | Animator 禁用时的显隐 |
| **Exclusive Tags** | 互斥标签（同时只能一个开启） |
| **Exclusive Off State** | 互斥组的"全关"默认选项 |
| **Set Custom Menu Icon** | 自定义菜单图标 |
| **Separate Local State** | 本地/远端分别动画 |
| **Enable Transition State** | 过渡动画（In/Out） |
| **Use a Global Parameter** | 使用指定参数名（OSC 兼容） |
| **Hold Button** | 按住按钮模式 |

### 6.2 Toggle Sets（互斥组）

**方案 1：Exclusive Tags**
- 每个 Toggle 设相同 Tag → 同时只能一个开启
- 支持多 Tag（逗号分隔）→ 复杂互斥逻辑
- 例：tops + bottoms + full-body（full-body 同时关 tops 和 bottoms）

**方案 2：Slider Wheel**
- 单个 Radial 滑块切换所有选项
- 使用 Flipbook Builder 每页一个预设

---

## 7. Full Controller 详细功能

### 7.1 核心特性

| 特性 | 说明 |
|------|------|
| **动画路径自动重写** | Prefab 根相对路径 → Avatar 绝对路径自动适配 |
| **参数自动命名空间** | `VF##` 前缀防止参数冲突 |
| **WD 自动转换** | 自动匹配 Avatar 的 WD 设置 |
| **Global Parameters** | 指定不加前缀的参数（OSC 兼容） |
| **Smooth Parameters** | 指定参数的平滑时间（秒到 90%） |
| **Path Rewrite Rules** | 手动路径重写规则 |

---

## 8. Quest 兼容性

VRCFury 自动辅助跨平台参数对齐：

| 规则 | 说明 |
|------|------|
| 参数名必须完全相同 | 顺序不再重要 |
| 可以使用不同参数文件 | Desktop/Mobile 可分离 |
| 可以删除整个资产/参数 | Mobile 版可减少内容 |
| **必须先上传 Desktop** | 然后才能上传 Mobile |
| 同项目须用同版本 VRCFury | Desktop/Mobile 项目必须一致 |
| Desktop 改参数后须重传 Mobile | 保持同步 |
| 必须从同一 PC 上传 | 本地临时文件传递数据 |

---

## 9. 与 Modular Avatar 的关系

### 9.1 功能重叠

| VRCFury | Modular Avatar |
|---------|----------------|
| Clothing Attacher (Armature Link) | Merge Armature |
| Modular Setup (Full Controller) | 整体思路 |
| Toggle Builder | 部分组件 |
| Gesture Manager | 需手动 |

### 9.2 关键差异

| 维度 | VRCFury | Modular Avatar |
|------|---------|----------------|
| **分发方式** | ❌ .unitypackage（手动） | ✅ VPM（一键安装） |
| **执行时机** | 上传前复制 | Apply On Play + 上传前 |
| **可逆性** | ✅ 完全可逆 | ⚠️ 部分可逆 |
| **文档** | 官网 + Discord | ✅ 官方文档完善（tutorials / samples / reference） |
| **社区** | 老牌 Avatar 圈 | 现代 NDMF 生态 |
| **与 AAO 协同** | 自动（上传前管线） | 自动（NDMF 链） |
| **参数压缩** | ✅ Parameter Compressor（16 bit） | ⚠️ Sync Parameter Sequence（排序） |
| **BlendShape 优化** | ✅ Blendshape Optimizer | ❌（需 AAO Freeze BlendShape） |
| **层数优化** | ✅ Direct Tree Optimizer | ⚠️ MA2BT 插件补充 |
| **WD 修复** | ✅ Fix Write Defaults | ❌ 手动 |

### 9.3 共存警告（已知冲突）

> ⚠️ **MA 与 VRCFury 互相不知道对方做了什么，容易出 bug**

**推荐执行顺序**（NDMF 管线）：
```
1. MA + 其他新增内容 NDMF 工具
2. Fury
3. 所有 NDMF 最佳化工具
```

### 9.4 不兼容项

| VRCFury 功能 | MA 功能 | 冲突 |
|--------------|---------|------|
| Parameter Compressor | Sync Parameter Sequence | ❌ 两者都重排参数槽位 |

### 9.5 与 d4rkAvatarOptimizer 共存

| 顺序 | 工具 | Callback Order |
|------|------|---------------|
| 1 | Modular Avatar | -25 |
| 2 | d4rkAvatarOptimizer | -15 |
| 3 | VRChat IEditorOnly | -1024 |
| 4 | VRCFury | Various |

⚠️ d4rkAvatarOptimizer 检测到 VRCFury 时禁用 "Create Optimized Copy"，只能 "Apply on Upload"。

---

## 10. Avatar 优化场景对比矩阵

用户原始问题"**压参数**"对应的能力矩阵：

| 优化方向 | VRCFury | MA | AAO | Meshia | d4rk |
|----------|---------|----|----|--------|------|
| **压缩同步参数** | ✅ Parameter Compressor (→16 bit) | ⚠️ Sync Parameter Sequence (排序) | ❌ | ❌ | ❌ |
| **合并 Animator 层** | ✅ Direct Tree Optimizer | ⚠️ MA2BT 插件 | ✅ Animator Optimizer | ❌ | ✅ Optimize FX Layer |
| **烘焙 BlendShape** | ✅ Blendshape Optimizer | ❌ | ✅ Freeze BlendShape | ❌ | ❌ |
| **合并 Mesh** | ⚠️ 间接（通过 Toggle） | ❌ 手动 | ✅ Merge Skinned Mesh | ❌ 减面 | ✅ NaNimation |
| **合并 Material** | ✅ | ❌ | ✅ Merge Material | ❌ | ✅ |
| **减少 Draw Call** | ✅ 自动 | ❌ 手动 | ✅ Trace And Optimize | ❌ | ✅ |
| **删除空动画状态** | ✅ 自动 | ❌ | ✅ Animator Optimizer | ❌ | ✅ Optimize FX Layer |
| **PhysBone 优化** | ⚠️ 手动 | ⚠️ 手动 | ✅ Merge PhysBone | ❌ | ❌ |
| **Mesh 减面** | ❌ | ❌ | ❌ | ✅ Burst+Job | ❌ |
| **纹理压缩** | ❌ | ❌ | ✅ Max Texture Size | ❌ | ❌ |
| **WD 修复** | ✅ Fix Write Defaults | ❌ | ❌ | ❌ | ❌ |
| **自动 Bug 修复** | ✅ 60+ 项 | ❌ | ❌ | ❌ | ❌ |

**结论**：
- **想要"参数压缩 + 自动修复 + 上传可逆"** → VRCFury
- **想要"几何级 + 深度优化"** → AAO + Meshia
- **想要"组件级装配"** → MA
- **三者不互斥，但共存有顺序要求**

---

## 11. 何时选择 VRCFury（决策树）

| 场景 | 推荐 |
|------|------|
| **新建 Avatar + 想用现代工具链** | ✅ **MA**（VPM + 文档完善 + NDMF 生态） |
| **已有 VRCFury 工作流，想保持"可逆"** | ⚠️ 继续用 VRCFury |
| **需要自动 Mesh 合并（多 SMR → 单 SMR）** | ⚠️ VRCFury Optimized Toggle |
| **需要压缩 Expression Parameter 数量** | ⭐ **VRCFury Parameter Compressor**（最强） |
| **需要减少 Animator 层数** | ⭐ VRCFury Direct Tree Optimizer 或 MA2BT |
| **需要减少 BlendShape VRAM** | ⭐ VRCFury Blendshape Optimizer（零配置） |
| **WD 问题频繁出现** | ⭐ VRCFury Fix Write Defaults |
| **与 MA 共存** | ⚠️ 谨慎，注意执行顺序与参数压缩冲突 |
| **想要最深度性能优化** | ✅ **AAO + Meshia**（更现代、文档完善） |
| **新装工具** | ✅ 优先 MA + AAO + Meshia（VPM 一键） |

---

## 12. 安装方式

### ❌ VRCFury 不通过 VPM 分发

**这是 VRCFury 在 2026 年最大的使用门槛**——必须从官网手动下载：

```
1. 访问 https://vrcfury.com
2. 点击 "Download VRCFury"
3. 下载 .unitypackage
4. 在 Unity 中: Assets → Import Package → Custom Package
5. 选择下载的 .unitypackage
6. 导入
```

**对比**：MA / AAO / Meshia 均通过 VPM 一键安装（推荐路径）。

---

## 13. 上传前复制机制（All Reversible）

**原理**：VRCFury 在 Avatar 上传时**复制一份**当前状态，添加完功能后再上传。原始 Controller 文件**永不被修改**。

**优势**：
- 移除 VRCFury 组件 = Avatar 恢复原状
- 不影响 TPS、VRCLens 等其他工具的产物
- 原始动画 Controller 文件永远不被触碰

**对比 MA**：MA 直接在 Avatar 上构建 ApplyOnPlay 逻辑，移除 MA 组件需要手动恢复。

---

## 14. 常见故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **Toggle "粘住"或不工作** | WD 混合问题 | Fix Write Defaults → Auto |
| **BlendShape 被限制 0-100** | VRChat 限制 | Player Settings → Clamp BlendShapes |
| **VRCFury 不显示/安装失败** | 项目中有其他脚本错误 | 修复其他脚本错误 |
| **Preprocess Callback Failed** | 构建失败的通用错误 | 查看之前的具体错误消息 |
| **Synced Layers 消失** | Unity bug | 不使用 Synced Layers |
| **Extra Field can't be serialized** | Unity 升级缓存 | 卸载 → 唤醒 Unity → 重装 |

---

## 15. 关键事实速查

| 事实 | 状态 |
|------|------|
| VRCFury 仍维护（2026-05-02） | ✅ FACT |
| VRCFury 不是 VPM 分发 | ✅ FACT |
| VRCFury 与 MA 共存有冲突 | ✅ FACT |
| Parameter Compressor 将所有 Float/Int 压到 16 bit | ✅ FACT（官网 + PR#238 验证） |
| Direct Tree Optimizer 合并层为 Direct Blend Tree | ✅ FACT（官网文档） |
| Blendshape Optimizer 烘焙非动画 BlendShape | ✅ FACT（官网 + YouTube 验证） |
| 上传前复制机制（All Reversible） | ✅ FACT（官网明确写明） |
| 自动修复 60+ 个 VRChat/Unity bug | ✅ FACT（fixes/ 页面逐项列举） |
| Pointer-Based Float Sync 技术 | ✅ FACT（PR#238 sentfromspacevr） |
| MA Sync Parameter Sequence 与 Parameter Compressor 不兼容 | ✅ FACT（多个文档交叉验证） |
| VRCFury 在 d4rkAvatarOptimizer 之后运行 | ✅ FACT（deepwiki 兼容性文档） |
| 实测 253 bit → 125 bit（Parameter Compressor） | ✅ FACT（VRChat 论坛用户报告） |

---

## 16. 参考来源

- **仓库**：https://github.com/VRCFury/VRCFury
- **官网**：https://vrcfury.com（核心功能 + 组件 + 修复 + SPS + 故障排除）
- **文档仓库**：https://github.com/VRCFury/vrcfury.com（MDX 源码，含完整组件文档）
- **PR#238**：https://github.com/VRCFury/VRCFury/pull/238（Pointer-Based Float Sync 技术实现）
- **社区**：Discord（技术支持）
- **知识库交叉引用**：
  - `memory/avatar/modular-avatar.md` §7.21 Sync Parameter Sequence 兼容性
  - `memory/avatar/ma-component-cards.md` Sync Parameter Sequence 卡片
  - `memory/avatar/ndmf-tools.md` §MA 与 VRCFury 兼容性
  - `memory/avatar/avatar-optimizer.md` AAO（功能更现代的优化工具）
  - `memory/avatar/ma2bt.md` MA2BT（MA 层的 Direct BlendTree 转换）
  - `memory/avatar/meshia-mesh-simplification.md` Meshia（Mesh 减面）
  - `memory/avatar/lac-avatar-compressor.md` LAC（纹理压缩）