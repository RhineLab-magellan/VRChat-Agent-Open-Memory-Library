---
title: VPM Repos URL 索引 (vcc.vrczh.org)
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - vcc
  - mirror
  - index
  - url
  - reference

aliases:
  - "VPM URL 索引"
  - "VPM Repos URL Index"
  - "57 个 VPM 仓库 URL 清单"

related:
  - sources/vpm-mirrors/vcc-vrczh.md
  - sources/vpm-mirrors/samples/index.md
  - sources/index.md
  - hybrid/vcc.md

source: https://vpm.vrczh.org/vpm/repos (2026-07-01 快照)
source_type: community
version: 1.0
last_review: 2026-07-01
confidence: High
---

# VPM Repos URL 索引 (vcc.vrczh.org)

> **本文定位**: 极简 URL 索引, 仅包含 **VPM 仓库 (repo) 级** 的上游 URL 与镜像 URL, **不含子包 (package) 级数据**。
> **数据快照**: 2026-07-01 09:30 UTC+8
> **数据源**: `https://vpm.vrczh.org/vpm/repos` (57 个 repo)
> **查询入口**: 详细元数据 / 站点文档 → [vcc-vrczh.md](vcc-vrczh.md); 子包级完整数据 → `参考文献/VPM-镜像站包信息/`

---

## 1. 完整 57 Repo URL 表

> **状态图例**: ✅ 同步成功 | 🔴 同步失败 | ⚠️ 占位 (description 缺失) | ❌ 废弃
>
> **使用建议**:
> - VCC/ALCOM 添加仓库: 复制 `镜像 URL` 列 (国内快)
> - 调试/最新版本: 复制 `上游 URL` 列 (实时, GitHub Pages)
> - 同步失败的包: 必须用上游 URL (mirror 无法拉取)

| # | apiId | 名称 | 上游 URL | 镜像 URL | 状态 |
|---|-------|------|----------|----------|------|
| 1 | `curated` | VRChat 官方精选 | <https://packages.vrchat.com/curated> | <https://vpm.vrczh.org/vpm/curated> | ✅ |
| 2 | `official` | VRChat 官方 SDK | <https://packages.vrchat.com/official> | <https://vpm.vrczh.org/vpm/official> | ✅ |
| 3 | `lilxyzw` | lilxyzw (lilToon) | <https://lilxyzw.github.io/vpm-repos/vpm.json> | <https://vpm.vrczh.org/vpm/lilxyzw> | ✅ |
| 4 | `nadena` | nadena (Modular Avatar) | <https://vpm.nadena.dev/vpm.json> | <https://vpm.vrczh.org/vpm/nadena> | ✅ |
| 5 | `pi` | _pi_'s VPM | <https://vpm.pimaker.at/index.json> | <https://vpm.vrczh.org/vpm/pi> | ✅ |
| 6 | `poiyomi` | Poiyomi Shader | <https://poiyomi.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/poiyomi> | 🔴 |
| 7 | `vrcft-jerry` | VRCFT - Jerry's Templates | <https://adjerry91.github.io/VRCFaceTracking-Templates/index.json> | <https://vpm.vrczh.org/vpm/vrcft-jerry> | 🔴 |
| 8 | `vrcfury` | VRCFury | <https://vcc.vrcfury.com> | <https://vpm.vrczh.org/vpm/vrcfury> | ✅ |
| 9 | `anatawa12` | anatawa12 (AAO) | <https://vpm.anatawa12.com/vpm.json> | <https://vpm.vrczh.org/vpm/anatawa12> | ✅ |
| 10 | `hai-vr` | Haï~ 工具集 | <https://hai-vr.github.io/vpm-listing/index.json> | <https://vpm.vrczh.org/vpm/hai-vr> | ✅ |
| 11 | `vrm-converter-for-vrchat` | VRM Converter for VRChat | <https://esperecyan.github.io/VRMConverterForVRChat/registry.json> | <https://vpm.vrczh.org/vpm/vrm-converter-for-vrchat> | ⚠️ |
| 12 | `yagihata` | Yagihata | <https://www.negura-karasu.net/vpm/> | <https://vpm.vrczh.org/vpm/yagihata> | ⚠️ |
| 13 | `gyoku` | gyokute | <https://vpm.gyoku.tech/vpm.json> | <https://vpm.vrczh.org/vpm/gyoku> | ⚠️ |
| 14 | `architech` | ArchiTech Assets | <https://vpm.techanon.dev/index.json> | <https://vpm.vrczh.org/vpm/architech> | ⚠️ |
| 15 | `vrlabs-system` | VRLabs: Systems | <https://api.vrlabs.dev/listings/category/systems> | <https://vpm.vrczh.org/vpm/vrlabs-system> | ⚠️ |
| 16 | `guribo` | Guribo (UdonVoiceUtils) | <https://Guribo.github.io/TLP/index.json> | <https://vpm.vrczh.org/vpm/guribo> | ⚠️ |
| 17 | `d4rkc0d3r` | d4rkpl4y3r | <https://d4rkc0d3r.github.io/vpm-repos/main.json> | <https://vpm.vrczh.org/vpm/d4rkc0d3r> | ⚠️ |
| 18 | `azukimochi` | Azukimochi | <https://azukimochi.github.io/vpm-repos/index.json> | <https://vpm.vrczh.org/vpm/azukimochi> | ⚠️ |
| 19 | `hfcred` | hfcRed's VPM | <https://hfcred.github.io/VPM-Listing/index.json> | <https://vpm.vrczh.org/vpm/hfcred> | ⚠️ |
| 20 | `rurre` | Pumkin's VPM | <https://rurre.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/rurre> | ⚠️ |
| 21 | `Hirami` | Modular Auto Toggle Tool | <https://github.com/HiramiO/Modular-Auto-Toggle/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/Hirami> | ⚠️ |
| 22 | `kurotu` | kurotu VPM | <https://kurotu.github.io/VPM-Listing/vpm.json> | <https://vpm.vrczh.org/vpm/kurotu> | ⚠️ |
| 23 | `ni-rila` | ni rila | <https://ni-rila.github.io/vpm/vpm.json> | <https://vpm.vrczh.org/vpm/ni-rila> | ⚠️ |
| 24 | `orels-unity-shaders` | orels Unity Shaders | <https://orels1.github.io/UnityShaders/index.json> | <https://vpm.vrczh.org/vpm/orels-unity-shaders> | ⚠️ |
| 25 | `pokeyi` | Pokeyi's Udon Tools | <https://pokeyi.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/pokeyi> | ⚠️ |
| 26 | `raitichan` | Raitichan's store | <https://raitichan.github.io/Raitichan-VPM/vpm.json> | <https://vpm.vrczh.org/vpm/raitichan> | ⚠️ |
| 27 | `raz` | Raz's VPM | <https://github.com/RazgrizHsu/VRChat-Modules/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/raz> | ⚠️ |
| 28 | `suzuryg` | suzuryg (FaceEmo) | <https://suzuryg.github.io/face-vtuber-book/vpm.json> | <https://vpm.vrczh.org/vpm/suzuryg> | ⚠️ |
| 29 | `USLOG` | Easy Avatar Uploader | <https://uslog.github.io/EAUploader/vpm.json> | <https://vpm.vrczh.org/vpm/USLOG> | ⚠️ |
| 30 | `vr-stage-lighting` | VR Stage Lighting | <https://github.com/AcChosen/VR-Stage-Lighting/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/vr-stage-lighting> | ⚠️ |
| 31 | `vrsuya` | VRSuya | <https://vpm.vrsuya.com/vpm.json> | <https://vpm.vrczh.org/vpm/vrsuya> | ⚠️ |
| 32 | `xtlcdn` | Explosive Theorem Lab | <https://xtlcdn.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/xtlcdn> | ⚠️ |
| 33 | `z3y` | z3y's packages | <https://z3y.github.io/vpm/main.json> | <https://vpm.vrczh.org/vpm/z3y> | ⚠️ |
| 34 | `whiteflare` | whiteflare | <https://vpm.whiteflare.com/vpm.json> | <https://vpm.vrczh.org/vpm/whiteflare> | ⚠️ |
| 35 | `orels1-udontoolkit` | Udon Toolkit | <https://orels1.github.io/UdonToolkit/index.json> | <https://vpm.vrczh.org/vpm/orels1-udontoolkit> | ⚠️ |
| 36 | `VRCxiaoye97AvatarToolkit` | xiaoye97 Avatar Toolkit | <https://github.com/VRCxiaoye97/AvatarToolkit/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/VRCxiaoye97AvatarToolkit> | ⚠️ |
| 37 | `vrcd` | VRCD 社区源 | <https://github.com/vrcd-community/vpm-listing/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/vrcd> | ⚠️ |
| 38 | `narazaka` | Narazaka VPM | <https://narazaka.github.io/vpm-repository/vpm.json> | <https://vpm.vrczh.org/vpm/narazaka> | ⚠️ |
| 39 | `yueby` | Yueby | <https://yueby.github.io/YuebyVPM/vpm.json> | <https://vpm.vrczh.org/vpm/yueby> | ⚠️ |
| 40 | `enitimeago` | enitimeago | <https://enitimeago.github.io/vpm-listing/vpm.json> | <https://vpm.vrczh.org/vpm/enitimeago> | ⚠️ |
| 41 | `thry` | Thry's VPM | <https://thryrallo.github.io/VPMListing/vpm.json> | <https://vpm.vrczh.org/vpm/thry> | ⚠️ |
| 42 | `vrlabs-components` | VRLabs: Components | <https://api.vrlabs.dev/listings/category/components> | <https://vpm.vrczh.org/vpm/vrlabs-components> | ⚠️ |
| 43 | `vrlabs-dependencies` | VRLabs: Dependencies | <https://api.vrlabs.dev/listings/category/dependencies> | <https://vpm.vrczh.org/vpm/vrlabs-dependencies> | ⚠️ |
| 44 | `vrlabs-essentials` | VRLabs: Essentials | <https://api.vrlabs.dev/listings/category/essentials> | <https://vpm.vrczh.org/vpm/vrlabs-essentials> | ⚠️ |
| 45 | `shino-hinaduki` | Expression Parameter Import | <https://shino-hinaduki.github.io/ExpressionParameterImport/index.json> | <https://vpm.vrczh.org/vpm/shino-hinaduki> | ⚠️ |
| 46 | `triturbo-blendshare` | BlendShare | <https://Tr1turbo.github.io/BlendShare/index.json> | <https://vpm.vrczh.org/vpm/triturbo-blendshare> | ⚠️ |
| 47 | `sonic853` | The 53 Labs | <https://53lts.github.io/53-labs-vpm/vpm.json> | <https://vpm.vrczh.org/vpm/sonic853> | ⚠️ |
| 48 | `cyanlaser` | Cyan Player Object Pool | <https://github.com/CyanLaser/Cyan-Player-Object-Pool/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/cyanlaser> | ⚠️ |
| 49 | `dreadscripts` | (已废弃) | <https://vpm.dreadscripts.com/listing/main.json> | <https://vpm.vrczh.org/vpm/dreadscripts> | ❌ |
| 50 | `hhotatea` | AvatarPoseLibrary | <https://github.com/HhotateA/AvatarPoseLibrary/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/hhotatea> | ⚠️ |
| 51 | `nekobako` | nekobako | <https://vpm.nekobako.net/index.json> | <https://vpm.vrczh.org/vpm/nekobako> | ⚠️ |
| 52 | `triturbo` | BlendShare (重复) | <https://Tr1turbo.github.io/BlendShare/index.json> | <https://vpm.vrczh.org/vpm/triturbo> | ⚠️ |
| 53 | `project-vrcz` | project-vrcz | <https://project-vrcz.github.io/vpm/vpm.json> | <https://vpm.vrczh.org/vpm/project-vrcz> | ⚠️ |
| 54 | `vrlabs-rehosted` | VRLabs: Rehosted | <https://api.vrlabs.dev/listings/category/rehosted> | <https://vpm.vrczh.org/vpm/vrlabs-rehosted> | ⚠️ |
| 55 | `Tr1turbo` | Triturbo (重复) | <https://Tr1turbo.github.io/BlendShare/index.json> | <https://vpm.vrczh.org/vpm/Tr1turbo> | ⚠️ |
| 56 | `LuiStudio` | LuiStudio's VPM | <https://github.com/LuiStudio/packages/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/LuiStudio> | ⚠️ |
| 57 | `vrcd-community` | VRCD 社区源 (重复) | <https://github.com/vrcd-community/vpm-listing/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/vrcd-community> | ⚠️ |

---

## 2. 状态汇总

| 状态 | 数量 | 占比 | 说明 |
|------|------|------|------|
| ✅ 同步成功 | 10 | 17.5% | mirror 拉取成功, 国内访问快 (推荐生产环境使用) |
| 🔴 同步失败 | 2 | 3.5% | `poiyomi`, `vrcft-jerry` — 需用上游 URL 替代 |
| ⚠️ 占位 | 44 | 77.2% | 元数据正常但顶层 description 为占位符 — 真实功能需查子包 |
| ❌ 废弃 | 1 | 1.8% | `dreadscripts` — 仓库已删库, **不要添加到 VCC** |
| **总计** | **57** | **100%** | — |

---

## 3. 特殊 Repo 备注

### 3.1 同步失败 (2 个) — 必须用上游

| apiId | 上游 URL |
|-------|----------|
| `poiyomi` | <https://poiyomi.github.io/vpm/index.json> |
| `vrcft-jerry` | <https://adjerry91.github.io/VRCFaceTracking-Templates/index.json> |

### 3.2 仓库已废弃 (1 个) — 不要添加

| apiId | 原因 |
|-------|------|
| `dreadscripts` | mirror 描述明确警告: "此上游已被删库废弃, 我们不推荐您在未来使用它" |

### 3.3 重复 apiId (内容相同, 添加一个即可)

| 多个 apiId | 共享上游 URL |
|-----------|-------------|
| `triturbo-blendshare`, `triturbo`, `Tr1turbo` | <https://Tr1turbo.github.io/BlendShare/index.json> |
| `vrcd`, `vrcd-community` | <https://github.com/vrcd-community/vpm-listing/releases/latest/download/vpm.json> |

---

## 4. 速查分流

### 4.1 添加到 VCC/ALCOM

```
VCC → Settings → User Packages → Add Repository
  ↓
粘贴镜像 URL: https://vpm.vrczh.org/vpm/{apiId}
  ↓
等待 VCC 拉取 index → Manage Projects 看到对应包
```

### 4.2 跳转到详细文档

| 需求 | 跳转 |
|------|------|
| **站点完整文档** (API/抓取方式/数据流) | [vcc-vrczh.md](vcc-vrczh.md) |
| **7 个示例包详细整理** (含子包) | [samples/index.md](samples/index.md) |
| **子包级完整数据** (10 MD + 56 JSON 原始快照) | `参考文献/VPM-镜像站包信息/` |
| **VRCD 社区** | `https://vrcd.org.cn/` |

### 4.3 详细包文档快速跳转

| apiId | 详细文档 |
|-------|---------|
| `curated` | [samples/curated.md](samples/curated.md) |
| `official` | [samples/official.md](samples/official.md) |
| `nadena` | [samples/nadena.md](samples/nadena.md) |
| `anatawa12` | [samples/anatawa12.md](samples/anatawa12.md) |
| `lilxyzw` | [samples/lilxyzw.md](samples/lilxyzw.md) |
| `poiyomi` | [samples/poiyomi.md](samples/poiyomi.md) |
| `vrcfury` | [samples/vrcfury.md](samples/vrcfury.md) |
| `hai-vr` | [samples/hai-vr.md](samples/hai-vr.md) |

> **未完成整理的 49 个 repo**: 当前仅完成 7 个示例详细整理, 剩余 50 个仅保留 URL 索引, 如需详细文档可参考 `参考文献/VPM-镜像站包信息/`。

---

## 5. 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| 完整 repo 数 | 57 |
| 文档定位 | URL 索引 (无子包) |
| 与 vcc-vrczh.md 关系 | vcc-vrczh.md = 站点全文档; 本文档 = 纯 URL 速查 |
| 与 samples/index.md 关系 | samples/index.md = 7 个详细知识单元; 本文档 = 57 个 URL 索引 |
| 整理者 | CherryClaw (V2 修订方案) |
| 用户审查 | ⏳ 待审查 |
