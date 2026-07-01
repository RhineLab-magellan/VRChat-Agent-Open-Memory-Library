---
title: FACT.md - VRChat 技术知识库
category: misc

knowledge_level: applied
status: active

tags:
  - misc
  - knowledge-graph
  - meta

aliases:
  - FACT
  - 知识库事实库
  - "Knowledge Base Facts"
  - 顶层索引

related:
  - index.md
  - _always-load.md
  - "sources/index.md"
  - "patterns/index.md"
  - "avatar/avatar-fallback-system.md"
  - "avatar/avatar-dynamic-bone-limits.md"
  - "avatar/avatar-particle-system-limits.md"
  - "avatar/full-body-tracking.md"
  - "avatar/ik-2.0.md"
  - "world/community-labs.md"

source: 本地知识库整理
source_type: community
version: 3.0
last_review: 2026-07-01
confidence: High
---
# FACT.md - VRChat 技术知识库

> 长期有效的知识库结构、核心约束、设计模式索引与工程经验。
>
> **本文件保留原则**:仅存储长期有效的**知识性内容**(结构/约束/经验),不记录过程性整理日志。详细工作模式、阶段历史、规则沉淀等过程性产物见 `特殊Agent提示词/知识库整理Agent_V3.1.md`。

---

## 知识库结构

```
memory/
├── avatar/                    # Avatar 相关
│   ├── shader/               # Shader 知识库
│   │   ├── index.md          # 索引
│   │   ├── liltoon/         # lilToon 详细文档（16个文件）
│   │   ├── scss/            # SCSS 详细文档
│   │   ├── orl/             # ORL Shaders World 通用着色器
│   │   ├── filamented/      # Filamented PBR 着色器
│   │   ├── unlitwf/         # UnlitWF Unlit 扩展专业效果
│   │   └── poiyomi/         # Poiyomi Shaders 8 主题知识
│   ├── vrc-constraints.md    # VRC Constraints
│   ├── playable-layers.md   # Playable Layers
│   ├── optimization-guide.md
│   ├── performance-rank.md
│   └── ...（其他 Avatar 文档）
├── world/                    # World 相关
│   ├── performance-guide.md # World 性能优化
│   ├── vrc-light-volumes.md  # VRCLightVolumes 光照系统
│   ├── occlusion-culling-guide.md  # 遮挡剔除优化
│   ├── reflection-probes.md  # 反射探针系统
│   ├── examples/             # SDK 内置示例
│   │   └── udon-example-scene/  # Udon Example Scene 13+ Prefab
│   ├── creator-economy.md    # 创作者经济 SDK
│   ├── scene-components/     # Scene Components 子分类
│   │   ├── index.md
│   │   ├── textmeshpro.md
│   │   ├── vrc-avatarpedestal.md
│   │   ├── vrc-cameradolly.md
│   │   ├── vrc-mirrorreflection.md
│   │   ├── vrc-objectsync.md  # ⭐核心:物理对象同步
│   │   ├── vrc-portalmarker.md
│   │   ├── vrc-scenedescriptor.md  # ⭐World 必含核心
│   │   ├── vrc-station.md
│   │   └── vrc-enablepersistence.md
│   ├── bakery/              # Bakery 光照烘焙
│   └── udon/                # Udon 域(子域化后)
│       ├── networking/
│       ├── udonsharp/
│       ├── data-containers/
│       ├── persistence/
│       ├── players/
│       ├── video-players/
│       ├── vrctween/
│       ├── vrc-graphics/
│       └── ...
├── vrchatsdk/                # VRChatSDK (HTTP API, 18 个文档)
├── platform/                 # 跨平台开发(4 个文档)
├── hybrid/                   # Hybrid 系统(OSC 协议)
├── sources/                  # 工具/项目/参考实现来源
├── patterns/                 # 核心设计模式
├── reviews/                  # 审查与整合计划
├── references/               # 知识源对比
├── api/                      # API 参考(8 个文件)
├── rules/                    # UdonSharp 语言/工程规则
└── meta/                     # 元协议(仅 Curator 模式使用)
```

---

## ⚠️ 核心约束（绝对规则）

### 渲染管线

> **🔴 最高优先级：VRChat 只支持 BRP (Built-in Rendering Pipeline)**

| 规则 | 说明 |
|------|------|
| **只支持 BRP** | VRChat **只支持** Built-in Rendering Pipeline |
| **禁止切换管线** | 任何更改渲染管线的行为都是**致命的** |
| **禁止 URP/HDRP** | 项目中不得使用 Universal 或 High Definition Render Pipeline |
| **Unity 版本绑定** | SDK 3.4.2+ 绑定 Unity 2022.3.22f1（LTS） |

**违反后果**：切换渲染管线会导致 VRChat 项目完全无法工作。

### Editor 脚本与构建

> 🔴 **任何引用 `UnityEditor.*` 命名空间的脚本必须放在 `Editor` 文件夹内**

| 规则 | 说明 |
|------|------|
| **根因** | 脚本先在编辑器下编译（包含 `UnityEditor` 程序集），再为目标平台重新编译（**不包含** `UnityEditor` 程序集） |
| **触发条件** | `using UnityEditor;` 等编辑器命名空间 |
| **解决路径 1** | 将脚本放到**父目录为 `Editor`** 的任意路径下，构建时自动排除 |
| **解决路径 2** | 创建 asmdef，**Include Platforms** 仅勾选 Editor |

**常见场景**（VRChat World 开发中）：
- 自定义 Inspector (`[CustomEditor]`)
- Gizmo 调试 (`OnDrawGizmos`)
- Build Pipeline 后处理 (`IPreprocessBuildWithReport`)
- AssetPostprocessor
- AssetDatabase / EditorUtility / EditorPrefs 调用

**易错点**：
- ❌ 脚本必须挂在 GameObject 上才能编译 → 实际由**文件夹路径**决定
- ❌ 用 `Assets/Scripts/MyEditor.cs` → 跨平台构建时找不到 `UnityEditor` 程序集，报错
- ✅ 用 `Assets/Editor/MyEditor.cs` 或 `Assets/Scripts/Editor/MyEditor.cs` → 正常

**参考**：
- Unity 特殊文件夹：https://docs.unity3d.com/6000.3/Documentation/Manual/SpecialFolders.html

---

## 高优先级知识（已完成）

### Avatar Pipeline
- VRCPipelineManager ✅
- Avatar 3.0 四行架构 ✅

### VRC Constraints (Avatar 域)
- 6 种约束类型 ✅
- 高级设置（Local Space/Freeze To World）✅
- 性能分类（Count/Depth）✅
- Constraints API ✅

### Playable Layers
- Humanoid vs Generic ✅
- 5 层详解（Base/Additive/Gesture/Action/FX）✅
- Avatar Mask 规则 ✅
- T-Pose/IK Pose/Sitting Pose ✅
- **Avatar Animator = 参数驱动系统** ✅（核心：Expression Menu → Parameter → Playable Layer → Animator）

### Unity Animator（World 上下文）
- **World Animator = 逻辑驱动系统** ✅（核心：Udon Event → SetBool/SetTrigger → State Machine）
- Udon Animator API（SetBool/SetFloat/SetTrigger/SetInteger/Play/CrossFade）✅
- 网络同步注意事项 ✅

### World 性能优化
- 预算规划 ✅
- 材质/Shader/纹理管理 ✅
- 光照系统（烘焙/动态）✅
- 测试方法 ✅

### Bakery 光照烘焙 ✅
- 系统要求（Windows + NVIDIA Kepler+）✅
- 6 种 Render Mode ✅
- 5 种 Directional Mode ✅
- 8 种组件 ✅
- 材质兼容性 ✅
- FAQ + 故障排除 ✅

### OSC 协议
- 完整协议数据库 ✅

### 音频同步系统架构 ✅ (参考工程)
- **纹理编码数据传递**：音频数据通过 CustomRenderTexture 传递 Shader，零网络同步开销
- **时间同步系统**：Master 权威时间锚点 + 双时间源融合 + 漂移校正
- **同步策略**：Manual Sync + Owner Transfer 混合模式
- **位域压缩**：byte 存储多个 bool(`_flags`)→ 详见 `memory/world/udon/data-containers/byte-and-bit-operations.md`
- **性能热点**：SendAudioOutputData 每帧 8 次 SetFloatArray(约 2ms 开销)
- **实验性功能保护**：audioDataToggle 默认关闭(VRCAsyncGPUReadback 成本高)

> **📚 参考实现**:本节提炼自开源 VRChat 音频同步框架,见 `memory/sources/open-source-projects.md` §音频同步类目

### 多机位导演系统网络同步架构 ✅ (参考工程)
- **5 层同步体系**：Manual + Continuous + NetworkCallable + SafeMod(排除) + NoVariableSync
- **NetworkCallable RPC**：参数化远程调用 + 批量延迟提交
- **双缓冲预览模式**：`_isPreviewActive` + `_serializationPending`
- **指数衰减插值**：Continuous 值平滑(Compensation 因子)
- **Slerp/Slerp 本地缓动**：位置+旋转独立插值
- **所有权分层**：操作者 vs 被跟踪者所有权分离
- **UI 转发模式**：NoVariableSync + SetProgramVariable

> **📚 参考实现**:本节提炼自开源 VRChat 多机位导演系统,见 `memory/sources/open-source-projects.md` §多机位导演类目

---

## 核心设计模式与案例研究索引（精简版）

> 以下为知识库中已验证的核心设计模式和案例研究索引。
> 完整实现代码、详细架构分析、对比表格均在对应文档中，按需检索。

| 类别 | 数量 | 索引位置 |
|------|------|---------|
| 核心设计模式 | 14 个 | `memory/patterns/index.md` + 各模式独立文档 |
| LuraSwitch2 实战模式 | 6 个 | `memory/patterns/index.md` #8-#13 |
| UdonVoiceUtils 工程化模式 | 10 个 | `memory/patterns/index.md` #14-#23 |
| ULocalization 沙箱适配模式 | 5 个 | `memory/patterns/index.md` #24-#28 |
| Sardinal 消息总线模式 | 3 个 | `memory/patterns/index.md` #29-#31 |
| 案例研究 A1-A9 | 9 个 | `memory/sources/open-source-projects.md` |
| 推荐工具 C1-C16 | 16 个 | `memory/hybrid/udon-world-plugins.md` |

**快速查阅入口**：
- 网络同步：`memory/patterns/manual-sync-state.md` / `advanced-sync-patterns.md`
- 沙箱适配：`memory/patterns/hash-based-dispatch.md` / `build-time-vs-runtime-separation.md`
- 消息总线：`memory/patterns/channel-routing.md` / `hybrid-subscription-modes.md`
- 视频同步：`memory/sources/vvmw.md`（案例）/ `memory/world/vvmw.md`（工具）
- Shader 选型：`memory/avatar/shader/index.md`
- VRChatSDK 概览：`memory/vrchatsdk/index.md`

---

## 知识完整性原则

> ⚠️ **所有知识库索引必须指向 memory/ 目录内部**
> - 外部文档随时可能删除或丢失
> - 工具安装链接（VPM/BOOTH）可以保留（操作指引，非知识本身）
> - 知识来源路径必须本地化（`参考工程/`、`参考文献/`）

---

## 重要工程经验

### ⚠️ PowerShell 5.1 + 中文 Windows 路径双重编码 Bug

**触发场景**：在中文 Windows (Windows 10/11) 上使用 PowerShell 5.1 处理包含中文（UTF-8）的文件路径。

**症状**：
- PowerShell 5.1 进程内的字符串 "参考文献" 被错误编码为 "鍙傝€冩槩"（UTF-8 字节被当 Latin-1 解释后再 UTF-16 化）
- 文件实际写入到一个**乱码目录**，而非用户看到的中文目录
- 同一路径用 `Get-ChildItem`（UTF-16 字符串）、`bash ls`（UTF-8）能正确看到；`[System.IO.FileInfo]::Exists` 在 PowerShell 进程内对**真实中文目录**返回 False，但能访问**乱码目录**中文件返回 True
- 路径中含 `$env:USERPROFILE\参考文献\...` 这样的中文段时高概率触发

**根因**：
- PowerShell 5.1 默认按系统 ANSI 代码页（中文 = GBK 936）读取 UTF-8 编码的脚本文件
- 但 .NET 内部统一用 UTF-16 字符串
- 双重转换后形成"看起来像中文的 Unicode 字符序列"（U+9359, U+509D, U+20AC, U+51A9, U+6783, U+941A, U+751B）
- Windows NTFS 是 Unicode 存储，因此这些乱码字符**确实对应**文件系统中的一个真实目录
- 脚本中所有路径操作都通过这个乱码字符序列进行，文件被写到乱码目录

**修复方案**：
1. **优先方案**：用 `chcp 65001` 启动 PowerShell（切换到 UTF-8 代码页）
2. **次优方案**：把脚本存为 GBK 编码（与系统 ANSI 一致）
3. **稳妥方案**：路径用 8.3 短名（如 `REFEREN~1\SP`）
4. **终极方案**：在 bash + Python/Node 中执行文件操作（绕过 PowerShell 编码层）

**诊断命令**：
```powershell
$path = "C:\Users\xxx\参考文献\SP"
for ($i=0; $i -lt $path.Length; $i++) {
    "{0:X4}" -f [int][char]$path[$i]   # 看实际字符码点
}
```
如果"参考文献"对应的码点不是 `U+53C2 U+8003 U+6587 U+732E`，说明已损坏。

**经验教训**：
- PowerShell 5.1 处理 UTF-8 中文路径**不可靠**，跨 PowerShell 与 bash/Cmd 的脚本要注意
- 下载大量文件到中文目录时，先用 ASCII 临时目录下载，再 mv 到目标位置
- 或直接用 Python 脚本（pathlib 自动处理编码）

### 远程下载任务参考实现

**任务**：下载 `https://docs.vrchat.com/llms.txt` 中所有 267 个文档到 `参考文献\SP` 目录。

**结果**：
- 267/267 成功下载
- 总大小 2.07 MB, 19910 行
- 文档分类：用户指南 45 个 + Avatar 3 个 + OSC 10 个 + 版本发布 209 个

**脚本位置**：`C:\CherryStudio\Agent\UdonSharpAgent\参考文献\SP\download-vrchat-docs.ps1`
- ✅ 子目录: `kebab-case/`
- ⚠️ `vrchatsdk/`: 中英混合命名（建议未来统一）

### 关键工程 Specs（从 2026-06-10 知识库更新中沉淀）

> 这些规格是 VRChat 平台的硬性限制,不属于过程性记录,沉淀在此供长期参考。

#### VRCShader.SetGlobal 限制
- 属性名必须以 `_Udon` 为前缀(用于全局设置)
- 详见 `memory/world/udon/vrc-graphics/`

#### Networking Specs
- **总带宽**: ~11 KB/s
- **Manual sync**: 280,496 bytes/serialization
- **Continuous sync**: ~200 bytes/serialization
- 详见 `memory/api/networking.md`

#### Persistence Compression
- 实际存储: 100 KB/player/world（压缩后）
- 可压缩数据: ~300 KB 原始数据
- 详见 `memory/api/persistence.md`

---

## 最低限度原则（SOUL / FACT 边界）

> 本文件(SOUL.md + FACT.md)仅存储**长期有效的最低限度原则**,不存储过程性工作协议。

| 内容类别 | 存储位置 | 理由 |
|---------|---------|------|
| 人格身份、语气、核心使命 | `SOUL.md` | 每个会话必须加载 |
| 知识库结构、核心约束、长期经验 | `memory/FACT.md`(本文件) | 每个会话必须加载 |
| 6 工作模式、Domain/Knowledge First、Knowledge Priority、Evidence、Failure Policy、Output、Retrieval、Entry Points、Ultimate Goal | `特殊Agent提示词/知识库整理Agent_V3.1.md` | 仅 Curator 模式按需参考 |
| 废弃文件处理规则、多文档同步 Checklist、Phase 历史、A 阶段记录 | `特殊Agent提示词/知识库整理Agent_V3.1.md` | 过程性/规则性,无需每次加载 |
