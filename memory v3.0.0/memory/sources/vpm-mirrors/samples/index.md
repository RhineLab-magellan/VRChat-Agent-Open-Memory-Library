---
title: VCC vrczh 镜像站 — 示例包索引
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - vcc
  - mirror
  - index
  - navigation

aliases:
  - "VPM Mirrors Samples Index"
  - "示例包索引"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/index.md
  - FACT.md

source: 本地知识库整理
source_type: community
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: High
---

# VCC vrczh 镜像站 — 示例包索引

> **状态**: ⚠️ 示例流程文档 — 仅完成 7 个示例包详细整理 (curated, official, nadena, anatawa12, lilxyzw, poiyomi, vrcfury, hai-vr)
> **完成度**: 7/57 = 12.3%
> **后续计划**: 用户审查示例流程后决定是否完成剩余 50 个包

---

## 域名分类

### 🏛 VRChat 官方源 (2)

| apiId | 名称 | 包数 | 状态 | 文档 |
|-------|------|------|------|------|
| `curated` | VRChat 官方精选 (社区审核包) | 9 | ✅ 同步 | [curated.md](curated.md) |
| `official` | VRChat 官方 SDK | 4 | ✅ 同步 | [official.md](official.md) |

### 🎭 Avatar 核心框架 (2)

| apiId | 名称 | 包数 | 状态 | 文档 |
|-------|------|------|------|------|
| `nadena` | Modular Avatar + NDMF (bd_) | 4 | ✅ 同步 | [nadena.md](nadena.md) |
| `vrcfury` | VRCFury (Avatar 工具链) | 1 (1281 版本) | ✅ 同步 | [vrcfury.md](vrcfury.md) |

### 🛠 Avatar 优化与工具 (1)

| apiId | 名称 | 包数 | 状态 | 文档 |
|-------|------|------|------|------|
| `anatawa12` | AAO + 工具集 | 14 | ✅ 同步 | [anatawa12.md](anatawa12.md) |

### 🎨 Avatar Shader (2)

| apiId | 名称 | 包数 | 状态 | 文档 |
|-------|------|------|------|------|
| `lilxyzw` | lilToon + 工具 (lilxyzw) | 9 | ✅ 同步 | [lilxyzw.md](lilxyzw.md) |
| `poiyomi` | Poiyomi Shader | 2 | 🔴 **同步失败** | [poiyomi.md](poiyomi.md) |

### 🌍 World 工具 (1)

| apiId | 名称 | 包数 | 状态 | 文档 |
|-------|------|------|------|------|
| `hai-vr` | Haï~ 工具集 (跨域) | 27 (upstream) / 34 (mirror) | ✅ 同步 | [hai-vr.md](hai-vr.md) |

---

## 选包建议矩阵

### 优先级矩阵 (按国内用户使用频率)

| 优先级 | apiId | 推荐理由 |
|--------|-------|----------|
| ⭐⭐⭐⭐⭐ | `official` | VRChat SDK 必备 |
| ⭐⭐⭐⭐⭐ | `nadena` | Modular Avatar 必备 |
| ⭐⭐⭐⭐⭐ | `lilxyzw` | lilToon 主流 Shader |
| ⭐⭐⭐⭐ | `curated` | 9 个官方精选包集合 |
| ⭐⭐⭐⭐ | `anatawa12` | AAO Quest 性能优化必备 |
| ⭐⭐⭐⭐ | `vrcfury` | Avatar 复杂工具链 |
| ⭐⭐⭐ | `hai-vr` | 跨域工具, CGE 复杂菜单 |
| ⭐⭐ | `poiyomi` | 镜像同步失败, 需 upstream |

### 按场景推荐

**最小 Avatar 项目** (新手):
- `official` (SDK)
- `nadena` (MA 装配)
- `lilxyzw` (Shader)

**Quest 性能优化** (老手机用户):
- `official` + `nadena` + `anatawa12` (AAO) + `lilxyzw` (含 NDMF Mesh Simplifier)

**复杂 Avatar** (高级):
- + `vrcfury` (复杂 Toggle/约束)
- + `hai-vr` (CGE 复杂菜单)

**World 项目** (任意):
- `official` (SDK) + `curated` (含 UdonSharp, Client Simulator, VRWorld Toolkit, EasyQuestSwitch)

**Shader 切换**:
- 偏好 lilToon → `lilxyzw`
- 偏好 Poiyomi → `poiyomi` (用 upstream) 或转 lilToon

---

## 已知模式 (示例包观察总结)

### 1. 描述缺失的 3 种情况

| 类型 | 占比 | 示例 | 建议 |
|------|------|------|------|
| **完全空** | 多数 | VRCFury, Poiyomi 顶层 | 知识库补充官方文档摘要 |
| **占位 "CHANGEME"** | 少数 | hai-vr external-expressions-menu | 视为未完成包, 不建议使用 |
| **重复 (历史版本)** | 少数 | NDMF 在 nadena + anatawa12 双源 | 信任源: 原始作者仓库 |

### 2. Unity 版本标注的"陷阱"

| 标注 | 实际 | 例子 |
|------|------|------|
| 标 `2019.4` | 通常 2019.4 + 2022.3 双兼容 | VRCFury, hai-vr 多数包 |
| 标 `2022.3` | 严格 2022.3 | AAO, MA |
| 标 `2018.1` | 历史兼容性, 实际 2018 起 | lilToon |
| 标 `?` (缺失) | 实际有值, mirror 解析问题 | curated 中 AudioLink, EasyQuestSwitch |

### 3. 同步失败的 2 个包

| apiId | 名称 | 替代 |
|-------|------|------|
| `poiyomi` | Poiyomi Shader | upstream `https://poiyomi.github.io/vpm/index.json` |
| `vrcft-jerry` | VRCFT - Jerry's Templates Listing | upstream `https://adjerry91.github.io/VRCFaceTracking-Templates/index.json` |

### 4. 重复 apiId (同一上游, 多个 ID)

| 上游 URL | 多个 apiId |
|----------|-----------|
| `https://Tr1turbo.github.io/BlendShare/index.json` | `triturbo-blendshare`, `triturbo`, `Tr1turbo` |
| `https://github.com/vrcd-community/vpm-listing/...` | `vrcd`, `vrcd-community` |

**建议**: 添加任意一个即可, 内容相同。

### 5. 仓库废弃

| apiId | 状态 |
|-------|------|
| `dreadscripts` | ⚠️ 已删库废弃, **不要添加到 VCC** |

### 6. Mirror 注入包 (识别模式)

- `com.vrchat.*` → 任何 mirror 注入 (因为 VRChat 官方包会被注入到多个 mirror repo 以解决依赖)
- `name == "{apiId}@VPM Repos Synchronizer"` → mirror 改写了顶层元数据
- `author == "VPM Repos Synchronizer"` → 同上

### 7. 字节数异常 (Mirror > Upstream 显著大)

| 异常包 | 字节 (mirror / upstream) | 倍数 | 原因 |
|--------|--------------------------|------|------|
| hai-vr | 454967 / 220117 | 2.1x | mirror 注入 VRChat SDK (4 个) + hai-vr basis (2 个) |
| anatawa12 | 494223 / 355344 | 1.4x | 未知 (镜像可能含完整版本历史 + headers/samples) |
| vrcfury | 951246 / 575636 | 1.7x | 未知 (mirror 注入可能性, 待查) |

---

## 整理建议 (剩余 50 个包)

### 第一批: 高频包 (建议优先)
| apiId | 名称 | 推测内容 |
|-------|------|----------|
| `d4rkc0d3r` | d4rkpl4y3r | Avatar 优化工具集 |
| `vrlabs-system` | VRLabs Packages: Systems | World 工具集 (与 curated 中 VRWorld Toolkit 互补) |
| `vrlabs-components` | VRLabs Packages: Components | 通用组件 |
| `vrlabs-essentials` | VRLabs Packages: Essentials | 通用必备 |
| `thry` | Thry's VPM Listing | Avatar 优化器 (与 AAO 互补) |
| `USLOG` | Easy Avatar Uplaoder | 批量 Avatar 上传 |
| `project-vrcz` | project-vrcz listing | VRCD 内部项目 |
| `LuiStudio` | LuiStudio's VPM Packages | 工具集 |
| `vrcd` | VRCD 社区源 | 中文社区包 |
| `vrcd-community` | VRCD 社区源 (重复) | 同上 |
| `kurotu` | kurotu VPM Packages | Avatar 工具 |
| `suzuryg` | suzuryg | FaceEmo (表情系统) |
| `yueby` | Yueby | 工具集 |
| `azukimochi` | Azukimochi | Avatar 工具 |
| `rurre` | Pumkin's VPM Repo | Avatar 工具 |

### 第二批: 垂直领域包
| apiId | 名称 | 推测内容 |
|-------|------|----------|
| `architech` | ArchiTech Assets | World/Avatar 资产 |
| `raz` | Raz's VPM Repo | 工具集 |
| `whiteflare` | whiteflare | Shader/工具 |
| `orels-unity-shaders` | orels Unity Shaders | 通用 Shader |
| `orels1-udontoolkit` | Udon Toolkit | Udon 工具 |
| `Hirami` | Modular Auto Toggle Tool Listing | MA Toggle 工具 |
| `hfcred` | hfcReds VPM Packages | 工具集 |
| `enitimeago` | enitimeago | 工具集 |
| `VRCxiaoye97AvatarToolkit` | xiaoye97 Avatar Toolkit Listing | Avatar 工具 |
| `yagihata` | Yagihata | 工具集 |
| `narazaka` | Narazaka VPM Listing | Avatar 工具 |
| `pokeyi` | Pokeyi's Udon Tools | Udon 工具 |
| `raitichan` | Raitichan's General store | 工具集 |
| `ni-rila` | ni rila | 工具集 |
| `guribo` | Guribo's VPM Listing | Avatar 工具 |

### 第三批: 长尾/垂直包
| apiId | 名称 | 推测内容 |
|-------|------|----------|
| `z3y` | z3y's packages | 编辑器工具 |
| `vrsuya` | VRSuya | World 工具 |
| `vr-stage-lighting` | VR Stage Lighting VPM Repo | World 灯光 |
| `xtlcdn` | Explosive Theorem Lab | 工具集 |
| `shino-hinaduki` | Expression Parameter Import Listing | Avatar 工具 |
| `triturbo-blendshare` | BlendShare Listing | 工具 (重复) |
| `triturbo` | BlendShare Listing | 工具 (重复) |
| `Tr1turbo` | Triturbo | 工具 (重复) |
| `sonic853` | The 53 Labs vpm | 工具集 |
| `cyanlaser` | Cyan Player Object Pool | Player Object Pool |
| `dreadscripts` | (废弃) | **跳过** |
| `hhotatea` | AvatarPoseLibrary Listing | Avatar 姿态库 |
| `nekobako` | nekobako | Avatar 工具 |
| `vrlabs-dependencies` | VRLabs Packages: Dependencies | 通用依赖 |
| `vrlabs-rehosted` | VRLabs Packages: Rehosted | 重托管包 |
| `pi` | _pi_'s funky fresh VPM repository | 工具集 |
| `gyoku` | gyokute | 工具集 |
| `vrm-converter-for-vrchat` | VRM Converter for VRChat Packages | VRM 转换 |

---

## 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| 完成度 | 7/57 = 12.3% |
| 已识别模式 | 7 类 (描述缺失, Unity 标注陷阱, 同步失败, 重复 apiId, 仓库废弃, mirror 注入, 字节数异常) |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
