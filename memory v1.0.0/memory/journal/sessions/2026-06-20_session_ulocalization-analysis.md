# 会话记录:ULocalization 项目分析(2026-06-20)

## 任务

根据"参考项目分析总结 Agent"v1.0 方法论,对 VRChat UdonSharp 参考项目 `C:\CherryStudio\Agent\UdonSharpAgent\参考工程\ULocalization` 进行系统分析,提取设计时遇到的问题、解决方案,以及设计方案的优势、劣势、难度、应用方向。

完成分析后,**记录到数据库中**(遵循三层架构: Sources / Memory / Journal)。

## 执行流程

### 1. 项目概况

- **项目**: HoshinoLabs ULocalization
- **作者**: @ikuko (HoshinoLabs) — https://x.com/magi_ikuko
- **仓库**: https://github.com/ikuko/ULocalization
- **License**: MIT
- **VPM 分发**: HoshinoLabs VPM Listing
- **依赖**: `com.unity.localization`, `com.hoshinolabs.sardinal`, `com.hoshinolabs.sardinject`
- **SDK 版本**: VRChat SDK 3.10.x / UdonSharp 1.x / Unity 2022.3+
- **总规模**: 145 个 .cs 文件 (Runtime 107 / Editor 33 / Shim 73 + Shim Editor 27)

### 2. 关键源文件分析

按 7 步标准过程(参考项目分析总结 Agent v1.0)执行:

| 步骤 | 关键源文件 | 分析深度 |
|------|------------|----------|
| 1. 入口与定位 | `Runtime/Localization.cs` (40 行) | ✅ 完整 |
| 2. 核心实现 | `Runtime/Udon/LocalizationShim.cs` (624 行) | ✅ 完整 |
| 3. 代码生成 | `Runtime/Udon/LocalizationShim_Generated.cs` (535 行) | ✅ 完整 |
| 4. 智能格式化 | `Runtime/Udon/LocalizationShim_SmartLiteFormatter.cs` | ✅ 完整 |
| 5. 引用更新 | `Runtime/Udon/CloneDetector.cs` | ✅ 完整 |
| 6. Editor 数据组装 | `Editor/Udon/LocalizationResolver.cs` (600+ 行) | ✅ 完整 |
| 7. Build 清理 | `Editor/Udon/LocalizationCleanup.cs` | ✅ 完整 |

**分析覆盖**: 35+ 关键 .cs 文件深度阅读(Runtime/Editor 各 15+)

### 3. 11 大设计问题与解决方案

| # | 问题 | 解决方案 | 沉淀模式 |
|---|------|----------|----------|
| 1 | Udon 无泛型分派 | IID + int 索引 | iid-object-identity |
| 2 | Udon 无委托/函数指针 | MD5 hash + 预生成 wrapper | hash-based-dispatch |
| 3 | Udon `SendCustomEvent` 无参数 | 3 object 槽位(`_l_t`/`_l_p`/`_l_a`) | slot-parameter-passing |
| 4 | Udon 无反射 | ID + Array + Slot 三件套 | (无独立模式,组合实现) |
| 5 | Udon 无泛型集合 | Type-Erasure via `object[2]` 元组 | code-generation-type-erasure |
| 6 | Udon 不能用 SmartFormat | SmartLiteFormatter 子集重写 | (Shim 内置) |
| 7 | Udon 无 Instantiate 引用重建 | CloneDetector + RenewPrefab | (Shim 内置) |
| 8 | Udon 不能用 UnityEditor.* | `#if UNITY_EDITOR` 隔离 | build-time-vs-runtime-separation |
| 9 | Udon 字段类型限制 | ISerializable + Sardinject `[Inject]` | build-time-vs-runtime-separation |
| 10 | Udon 大 object[] 调度慢 | 并行 `int[]` / `object[]` 数组 | (无独立模式) |
| 11 | Udon 事件重复触发 | Build 阶段反射清理 | build-time-vs-runtime-separation |

### 4. 工程评价

| 维度 | 评分 | 说明 |
|------|------|------|
| **架构清晰度** | ⭐⭐⭐⭐⭐ | God Shim + Sardinal Signal + Sardinject DI,职责清晰 |
| **代码生成规模** | ⭐⭐⭐⭐⭐ | 500+ hash 方法自动化生成,几乎无限扩展 |
| **Build-Runtime 分离** | ⭐⭐⭐⭐⭐ | Editor 反射 + LINQ + 缓存,Runtime O(1) 查表 |
| **Udon 沙箱适配深度** | ⭐⭐⭐⭐⭐ | 5 大模式覆盖所有 Udon 限制(无泛型/无委托/无参/无反射/无 Dict) |
| **CloneDetector 创新** | ⭐⭐⭐⭐⭐ | 解决 VRCPlayerObject 克隆重建引用难题 |
| **文档完整度** | ⭐⭐⭐ | 仅 README,需读源码理解 |
| **学习曲线** | ⭐⭐ (难) | 需理解 Sardinal/Sardinject/Source Generator/Reflection 全栈 |
| **Quest 兼容** | ⭐⭐⭐ | `BehaviourSyncMode.None` 完全本地,无网络开销 |
| **性能** | ⭐⭐⭐⭐ | Runtime 查表 O(1),但 27 字段序列化初始开销 |

### 5. 优势 vs 劣势

#### 优势
1. **零网络开销**: `BehaviourSyncMode.None` 完全本地,Locale 切换不消耗带宽
2. **强扩展性**: 新增 LocalizeEvent 类型无需改 Runtime 端,只需更新 Editor 端白名单 + 重新 Build
3. **类型安全**: 编译期生成的 wrapper 强转 type,运行时无 cast 风险
4. **完美适配 Udon 沙箱**: 5 大模式 + 3 大子机制覆盖所有限制

#### 劣势
1. **修改 Scene 后必须重建**: 任何 LocalizeEvent / LocalizedString 变更都需重新 Build
2. **白名单约束**: UnityEvent listener 必须白名单内,否则 Build 阶段被过滤
3. **CloneDetector 仅处理 VRCPlayerObject**: 手动 Instantiate 不走此路径
4. **学习曲线陡**: Sardinal + Sardinject + Source Generator + Reflection 全栈知识

### 6. 应用方向

| 方向 | 适用度 | 说明 |
|------|--------|------|
| **Unity 系统 → Udon 适配** | ⭐⭐⭐⭐⭐ | 任何"想把 Unity 高层系统包装到 Udon"的项目(序列化/输入/动画/物理/AI 等) |
| **大型多 LocalizeEvent 场景** | ⭐⭐⭐⭐⭐ | 100+ LocalizeEvent 场景的标准实现 |
| **中等规模 Udon 工具** | ⭐⭐⭐⭐ | Hash Dispatch + Slot Passing 2 个模式即可大幅简化 |
| **小型 Udon 项目** | ⭐⭐ | 学习曲线太陡,直接 `SendCustomEvent` 硬编码更简单 |
| **VRCPlayerObject 克隆项目** | ⭐⭐⭐⭐⭐ | CloneDetector + RenewPrefab 是解决该问题的标准方案 |

### 7. 知识库更新执行

| 动作 | 文件 | 内容 |
|------|------|------|
| 新建 Source | `memory/sources/ulocalization.md` | 完整项目档案(145 .cs + God Shim + 27 字段 + 500+ hash + 16 IVariable + 11 设计问题 + 工程评价) |
| 新建 Pattern 1 | `memory/patterns/hash-based-dispatch.md` | 哈希方法分派完整模式 + 代码骨架 + 500+ 预生成示例 |
| 新建 Pattern 2 | `memory/patterns/iid-object-identity.md` | 整数身份映射完整模式 + Editor/ID + 3 缓存分离 |
| 新建 Pattern 3 | `memory/patterns/slot-parameter-passing.md` | 槽位参数传递完整模式 + 3 槽位选择表 |
| 新建 Pattern 4 | `memory/patterns/code-generation-type-erasure.md` | 代码生成 + 类型擦除 + `object[2]` 元组模式 |
| 新建 Pattern 5 | `memory/patterns/build-time-vs-runtime-separation.md` | Build-Runtime 分离 + Editor 注入 + Cleanup 钩子 |
| 更新 Index | `memory/sources/open-source-projects.md` | A8 案例研究型参考工程(7→8) |
| 更新 Index | `memory/sources/index.md` | 注册新源 + 沉淀内容摘要 |
| 更新 Index | `memory/patterns/index.md` | 模式从 23 扩展到 28 + 选择决策树第 6 节 + 速查表更新 + 案例研究列表更新 |
| 更新 Index | `memory/FACT.md` | 新增 § ULocalization 沙箱适配模式(参考工程) + 时间戳追加 |
| 新建 Session | `memory/journal/sessions/2026-06-20_session_ulocalization-analysis.md` | 本文件 |

### 8. 关键发现

> **ULocalization 是"Udon 沙箱适配典范"**

与其他 3 个 VRChat World 域参考工程(VRCTD / VVMW / AudioLink / QuickBrown / TLP UVU)不同,ULocalization 解决的核心问题**不是多人交互 / 网络同步 / 物理模拟**,而是:

> **"如何在 Udon VM 沙箱限制下,完整包装 Unity 高层复杂系统"**

5 大模式都是"Udon VM 沙箱适配"的方法论范本,适用于:
- 包装 Unity Localization(本项目)
- 包装 Unity Input System
- 包装 Unity Animation Rigging
- 包装 Unity Physics (Ragdoll / Joint)
- 包装 Unity AI (NavMesh / Behavior Tree)
- 包装 Unity Cinemachine
- 任何"想把 Unity 高层系统适配到 Udon"的项目

**填补了知识库"如何在 Udon 写 Adapter"的空白** — 这是与此前所有 Pattern 库的根本差异。

### 9. 模式决策树(已加入 patterns/index.md)

```
### 6. Udon 沙箱适配(绕过 VM 限制)

Q9: 需要绕过 Udon VM 限制?
├── 动态分派 100+ 方法 → hash-based-dispatch.md
├── 对象跨 Editor-Runtime 引用 → iid-object-identity.md
├── UnityEvent 需传参 → slot-parameter-passing.md
├── 多种类型统一处理(泛型替代) → code-generation-type-erasure.md
└── Editor 端预处理 + 运行时查表 → build-time-vs-runtime-separation.md
```

### 10. 与其他参考工程对比

| 维度 | VRCTD (A1) | VVMW (A2) | AudioLink (A3) | QuickBrown (A6) | UVU (A7) | **ULocalization (A8)** |
|------|-----------|-----------|----------------|----------------|----------|----------------------|
| 核心问题 | 多人导演 | 视频同步 | 音频同步 | UI 组件 | 语音控制 | **Udon 沙箱适配** |
| 主导技术 | 5 层同步 | 时间锚点 | Shader-Centric | 4 层职责 | 8 层职责 | **代码生成 + 类型擦除** |
| 模式数量 | 7 | 1 | 5 | 6 | 10 | **5** |
| 模式类别 | 同步架构 | 时间算法 | 同步架构 | UI 交互 | 音频控制 | **VM 沙箱** |
| 复用度 | 中 | 高 | 中 | 高 | 高 | **⭐⭐⭐⭐⭐** |

ULocalization 的 5 个模式**复用度最高** — 任何"包装 Unity 高层系统"的项目都能用,远比特定领域的同步/UI/音频模式更通用。

## 学到的核心方法论

### 1. "包装类项目"的设计三件套

任何"把 Unity 系统包装到 Udon"的项目都应具备:

| 件 | 作用 |
|----|------|
| **God Shim** | 单一入口持有所有数据 + 所有方法 |
| **Sardinject `[Inject]`** | Editor 端依赖注入,Runtime 端零反射 |
| **Build 钩子** | 清理被替代的原组件,避免重复触发 |

### 2. "Udon 沙箱适配"的 5 大问题与 5 大解法

| 限制 | 解决 |
|------|------|
| 无委托 | Hash 分派 |
| 无 Dictionary 索引 | IID 整数映射 |
| 无参数 | Slot 槽位 |
| 无泛型 | Type Erasure |
| 无 Editor API | Build-Runtime 分离 |

### 3. "代码生成 + 类型擦除"双剑合璧

- **代码生成**(Hash Dispatch)解决"动态选择方法"
- **类型擦除**(`object[2]` 元组)解决"动态处理多类型"
- 两者结合可以"用静态代码模拟任何动态行为"

### 4. "元组模式"的妙用

```csharp
// 看似是 LocalizedString,实际是 object[2]
var localized = (object[])(object)myLocalizedString;
var shim = (LocalizationShim)localized[0];
var id = (int)localized[1];
```

Udon VM 不做类型检查,可直接强转。这是**零开销**的"伪类型",可绕过 Udon 沙箱的"类型擦除不彻底"问题。

### 5. "Build 清理"的必要性

Editor 端"接管"原生 Unity 组件(如 LocalizeEvent)后,必须:
1. 禁用原组件(`enabled = false`)
2. 设置 `hideFlags`(`NotEditable | DontSaveInBuild`)
3. 反射清空所有 UnityEvent 持久 listener(避免重复触发)

否则 Build 后原组件仍会触发,造成事件重复。

## 待沉淀(后续 Session)

- [ ] 8 大难题中"CloneDetector 时序"可能值得加 FAIL 案例(暂未独立建文档,留待 common-failures.md)
- [ ] 5 大模式可单独写"代码生成器实现指南",含 Roslyn Source Generator / T4 模板对比
- [ ] Sardinal + Sardinject 的 Udon 适配机制可独立入库(目前作为依赖被简述)

## 关联文档

- `memory/sources/ulocalization.md` — 项目溯源
- `memory/patterns/hash-based-dispatch.md` — 24 号模式
- `memory/patterns/iid-object-identity.md` — 25 号模式
- `memory/patterns/slot-parameter-passing.md` — 26 号模式
- `memory/patterns/code-generation-type-erasure.md` — 27 号模式
- `memory/patterns/build-time-vs-runtime-separation.md` — 28 号模式
- `memory/patterns/index.md` — 决策树第 6 节 + 速查表
- `memory/sources/open-source-projects.md` — A8 案例研究
- `memory/sources/index.md` — 新源注册
- `memory/FACT.md` — § ULocalization 沙箱适配模式
