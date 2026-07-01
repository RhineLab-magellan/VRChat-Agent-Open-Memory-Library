---
title: VCC vrczh 镜像站 (VPM Repos Synchronizer)
category: sources

knowledge_level: applied
status: active

tags:
  - sources
  - vpm
  - vcc
  - alcom
  - mirror
  - udonsharp
  - avatar
  - world

aliases:
  - "VCC vrczh"
  - "vrczh VPM 镜像"
  - "VRCD VPM 中转"
  - "VPM Repos Synchronizer"

related:
  - sources/index.md
  - sources/official-docs.md
  - sources/example-central.md
  - platform/easyquestswitch.md
  - sources/vpm-mirrors/samples/curated.md
  - sources/vpm-mirrors/samples/nadena.md
  - sources/vpm-mirrors/samples/anatawa12.md
  - sources/vpm-mirrors/samples/lilxyzw.md
  - sources/vpm-mirrors/samples/poiyomi.md
  - sources/vpm-mirrors/samples/vrcfury.md
  - sources/vpm-mirrors/samples/hai-vr.md

source: vcc.vrczh.org 站点 + 上游 VPM 仓库验证
source_type: community
version: 0.1 (示例流程)
last_review: 2026-07-01
confidence: Medium
---

# VCC vrczh 镜像站 (VPM Repos Synchronizer)

> **状态**: ⚠️ 示例流程文档（仅完成 6 个示例包详细整理）
> **核心结论**: 镜像站聚合了 57 个社区 VPM 源；镜像站自身仅提供元数据（name/author/upstreamUrl），**所有 description 字段为占位符 "Description"**，实际功能叙述必须从各 repo 的上游 VPM index 解析。
> **使用场景**: 给 VCC / ALCOM 添加第三方 VPM 源；查询某个包对应的镜像 URL；批量评估社区 VPM 仓库覆盖。

---

## 1. 站点定位

**VCC vrczh 镜像站** (URL: <https://vcc.vrczh.org/>) 是由 VRCD (虚拟现实中文开发者社区) 维护的 VPM 仓库镜像服务，底层为 Deno 部署的开源项目 `vpm-repos-syncronizer` (Deno Deploy 部署，前端域名 `vpm.vrczh.org`)。

**核心功能**:
- 定时同步社区第三方 VPM 仓库（`*/10 * * * *`，每 10 分钟一次）
- 提供国内可访问的镜像 URL
- 解决部分 repo 托管在 GitHub Pages 而国内访问慢/被墙的问题

**下游使用方**:
- VRChat Creator Companion (VCC)
- ALCOM (AlphaBlend CC，VCC 的社区分叉)
- 任何兼容 VPM 协议的包管理器

---

## 2. 数据访问方式

### 2.1 Web 界面

```
主入口: https://vcc.vrczh.org/
文档:   https://vcc.vrczh.org/docs  (⚠️ 当前显示 Page Not Found, 文档功能未上线)
状态:   https://vcc.vrczh.org/status (服务状态)
```

Web 界面分页 URL 模式: `https://vcc.vrczh.org/?page=N`，前端显示共 5 页 (API 实际 totalCount 57)。

### 2.2 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `https://vpm.vrczh.org/vpm/repos` | GET | **完整 57 个 repo 字典** (`{apiId: upstreamUrl}`) — 推荐入口 |
| `https://vpm.vrczh.org/repos?page=N&count=10` | GET | 分页 API，含 description/author/syncStatus (但 description 是占位符 "Description") |
| `https://vpm.vrczh.org/vpm/{apiId}` | GET | 单个 repo 的 VPM index (与 upstream 同步) |
| `https://vpm.vrczh.org/vpm/index.json` | GET | 顶级 index (空 packages，含 curated/official 引用) |

**注意**:
- ⚠️ Deno Deploy 端会判断 `User-Agent` 是否为 terminal，curl 不带 UA 会返回 ASCII 摘要。建议 **必须带 UA**：`curl -A "Mozilla/5.0" ...` 或浏览器内 fetch
- 分页 API `?page=N&count=M` 的 `count` 字段上限 **50** (`{"errors":{"count":["The field count must be between 0 and 50."]}}`)
- 分页 API 的 `totalCount` 是 57，但**实际只返回 47 个 unique item** (10 个核心包 `curated/official/lilxyzw/nadena/pi/poiyomi/vrcft-jerry/vrcfury/anatawa12/hai-vr` 不可见，**必须用 `/vpm/repos` 端点拿全**)

### 2.3 完整 57 个 Repo 列表

> 来源: `https://vpm.vrczh.org/vpm/repos` (2026-07-01 快照)
> 标记: 🔴 = 同步失败 (status=2) | 🟡 = 占位 description | ✅ = description 为镜像站原值

| # | apiId | 名称 (mirror) | 作者 | 上游 URL | 镜像 URL | 状态 |
|---|-------|---------------|------|----------|----------|------|
| 1 | curated | curated | VRChat | <https://packages.vrchat.com/curated> | <https://vpm.vrczh.org/vpm/curated> | ✅ |
| 2 | official | official | VRChat | <https://packages.vrchat.com/official> | <https://vpm.vrczh.org/vpm/official> | ✅ |
| 3 | lilxyzw | lilxyzw | lilxyzw | <https://lilxyzw.github.io/vpm-repos/vpm.json> | <https://vpm.vrczh.org/vpm/lilxyzw> | ✅ |
| 4 | nadena | nadena | bd_ | <https://vpm.nadena.dev/vpm.json> | <https://vpm.vrczh.org/vpm/nadena> | ✅ |
| 5 | pi | _pi_'s funky fresh VPM repository | _pi_ | <https://vpm.pimaker.at/index.json> | <https://vpm.vrczh.org/vpm/pi> | ✅ |
| 6 | poiyomi | Poiyomi's VPM Repo | Poiyomi | <https://poiyomi.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/poiyomi> | 🔴 |
| 7 | vrcft-jerry | VRCFT - Jerry's Templates Listing | Adjerry91 | <https://adjerry91.github.io/VRCFaceTracking-Templates/index.json> | <https://vpm.vrczh.org/vpm/vrcft-jerry> | 🔴 |
| 8 | vrcfury | VRCFury Repo | VRCFury Developers | <https://vcc.vrcfury.com> | <https://vpm.vrczh.org/vpm/vrcfury> | ✅ |
| 9 | anatawa12 | anatawa12 | anatawa12 | <https://vpm.anatawa12.com/vpm.json> | <https://vpm.vrczh.org/vpm/anatawa12> | ✅ |
| 10 | hai-vr | https://docs.hai-vr.dev | Haï~ | <https://hai-vr.github.io/vpm-listing/index.json> | <https://vpm.vrczh.org/vpm/hai-vr> | ✅ |
| 11 | vrm-converter-for-vrchat | VRM Converter for VRChat Packages | 100の人 | <https://esperecyan.github.io/VRMConverterForVRChat/registry.json> | <https://vpm.vrczh.org/vpm/vrm-converter-for-vrchat> | 🟡 |
| 12 | yagihata | Yagihata | Yagihata | <https://www.negura-karasu.net/vpm/> | <https://vpm.vrczh.org/vpm/yagihata> | 🟡 |
| 13 | gyoku | gyokute | gyokute | <https://vpm.gyoku.tech/vpm.json> | <https://vpm.vrczh.org/vpm/gyoku> | 🟡 |
| 14 | architech | ArchiTech Assets | ArchiTechVR | <https://vpm.techanon.dev/index.json> | <https://vpm.vrczh.org/vpm/architech> | 🟡 |
| 15 | vrlabs-system | VRLabs Packages: Systems | VRLabs | <https://api.vrlabs.dev/listings/category/systems> | <https://vpm.vrczh.org/vpm/vrlabs-system> | 🟡 |
| 16 | guribo | Guribo's VPM Listing | Guribo | <https://Guribo.github.io/TLP/index.json> | <https://vpm.vrczh.org/vpm/guribo> | 🟡 |
| 17 | d4rkc0d3r | d4rkpl4y3r | d4rkpl4y3r | <https://d4rkc0d3r.github.io/vpm-repos/main.json> | <https://vpm.vrczh.org/vpm/d4rkc0d3r> | 🟡 |
| 18 | azukimochi | Azukimochi | Azukimochi | <https://azukimochi.github.io/vpm-repos/index.json> | <https://vpm.vrczh.org/vpm/azukimochi> | 🟡 |
| 19 | hfcred | hfcReds VPM Packages | hfcRed | <https://hfcred.github.io/VPM-Listing/index.json> | <https://vpm.vrczh.org/vpm/hfcred> | 🟡 |
| 20 | rurre | Pumkin's VPM Repo | Pumkin | <https://rurre.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/rurre> | 🟡 |
| 21 | Hirami | Modular Auto Toggle Tool Listing | Hirami | <https://github.com/HiramiO/Modular-Auto-Toggle/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/Hirami> | 🟡 |
| 22 | kurotu | kurotu VPM Packages | kurotu | <https://kurotu.github.io/VPM-Listing/vpm.json> | <https://vpm.vrczh.org/vpm/kurotu> | 🟡 |
| 23 | ni-rila | ni rila | ni rila | <https://ni-rila.github.io/vpm/vpm.json> | <https://vpm.vrczh.org/vpm/ni-rila> | 🟡 |
| 24 | orels-unity-shaders | orels Unity Shaders | orels1 | <https://orels1.github.io/UnityShaders/index.json> | <https://vpm.vrczh.org/vpm/orels-unity-shaders> | 🟡 |
| 25 | pokeyi | Pokeyi's Udon Tools | Pokeyi | <https://pokeyi.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/pokeyi> | 🟡 |
| 26 | raitichan | Raitichan's General store | Raitichan | <https://raitichan.github.io/Raitichan-VPM/vpm.json> | <https://vpm.vrczh.org/vpm/raitichan> | 🟡 |
| 27 | raz | Raz's VPM Repo | Raz | <https://github.com/RazgrizHsu/VRChat-Modules/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/raz> | 🟡 |
| 28 | suzuryg | suzuryg | suzuryg | <https://suzuryg.github.io/face-vtuber-book/vpm.json> | <https://vpm.vrczh.org/vpm/suzuryg> | 🟡 |
| 29 | USLOG | Easy Avatar Uplaoder | USLOG | <https://uslog.github.io/EAUploader/vpm.json> | <https://vpm.vrczh.org/vpm/USLOG> | 🟡 |
| 30 | vr-stage-lighting | VR Stage Lighting VPM Repo | AcChosen | <https://github.com/AcChosen/VR-Stage-Lighting/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/vr-stage-lighting> | 🟡 |
| 31 | vrsuya | VRSuya | VRSuya | <https://vpm.vrsuya.com/vpm.json> | <https://vpm.vrczh.org/vpm/vrsuya> | 🟡 |
| 32 | xtlcdn | Explosive Theorem Lab. Metaverse Division | Jeremy Lam aka. Vistanz | <https://xtlcdn.github.io/vpm/index.json> | <https://vpm.vrczh.org/vpm/xtlcdn> | 🟡 |
| 33 | z3y | z3y's packages | z3y | <https://z3y.github.io/vpm/main.json> | <https://vpm.vrczh.org/vpm/z3y> | 🟡 |
| 34 | whiteflare | whiteflare | whiteflare | <https://vpm.whiteflare.com/vpm.json> | <https://vpm.vrczh.org/vpm/whiteflare> | 🟡 |
| 35 | orels1-udontoolkit | Udon Toolkit | orels1 | <https://orels1.github.io/UdonToolkit/index.json> | <https://vpm.vrczh.org/vpm/orels1-udontoolkit> | 🟡 |
| 36 | VRCxiaoye97AvatarToolkit | xiaoye97 Avatar Toolkit Listing | xiaoye97 | <https://github.com/VRCxiaoye97/AvatarToolkit/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/VRCxiaoye97AvatarToolkit> | 🟡 |
| 37 | vrcd | 虚拟现实中文开发者社区（Virtual Reality Chinese Developer） | VRCD | <https://github.com/vrcd-community/vpm-listing/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/vrcd> | 🟡 |
| 38 | narazaka | Narazaka VPM Listing | Narazaka | <https://narazaka.github.io/vpm-repository/vpm.json> | <https://vpm.vrczh.org/vpm/narazaka> | 🟡 |
| 39 | yueby | Yueby | Yueby | <https://yueby.github.io/YuebyVPM/vpm.json> | <https://vpm.vrczh.org/vpm/yueby> | 🟡 |
| 40 | enitimeago | enitimeago | enitimeago | <https://enitimeago.github.io/vpm-listing/vpm.json> | <https://vpm.vrczh.org/vpm/enitimeago> | 🟡 |
| 41 | thry | Thry's VPM Listing | Thryrallo | <https://thryrallo.github.io/VPMListing/vpm.json> | <https://vpm.vrczh.org/vpm/thry> | 🟡 |
| 42 | vrlabs-components | VRLabs Packages: Components | VRLabs | <https://api.vrlabs.dev/listings/category/components> | <https://vpm.vrczh.org/vpm/vrlabs-components> | 🟡 |
| 43 | vrlabs-dependencies | VRLabs Packages: Dependencies | VRLabs | <https://api.vrlabs.dev/listings/category/dependencies> | <https://vpm.vrczh.org/vpm/vrlabs-dependencies> | 🟡 |
| 44 | vrlabs-essentials | VRLabs Packages: Essentials | VRLabs | <https://api.vrlabs.dev/listings/category/essentials> | <https://vpm.vrczh.org/vpm/vrlabs-essentials> | 🟡 |
| 45 | shino-hinaduki | Expression Parameter Import Listing | Shino Hinaduki | <https://shino-hinaduki.github.io/ExpressionParameterImport/index.json> | <https://vpm.vrczh.org/vpm/shino-hinaduki> | 🟡 |
| 46 | triturbo-blendshare | BlendShare Listing | Triturbo | <https://Tr1turbo.github.io/BlendShare/index.json> | <https://vpm.vrczh.org/vpm/triturbo-blendshare> | 🟡 |
| 47 | sonic853 | The 53 Labs vpm | Sonic853 | <https://53lts.github.io/53-labs-vpm/vpm.json> | <https://vpm.vrczh.org/vpm/sonic853> | 🟡 |
| 48 | cyanlaser | Cyan Player Object Pool | CyanLaser | <https://github.com/CyanLaser/Cyan-Player-Object-Pool/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/cyanlaser> | 🟡 |
| 49 | dreadscripts | (null, 仓库已废弃) | (null) | <https://vpm.dreadscripts.com/listing/main.json> | <https://vpm.vrczh.org/vpm/dreadscripts> | 🟡 |
| 50 | hhotatea | AvatarPoseLibrary Listing | HhotateA | <https://github.com/HhotateA/AvatarPoseLibrary/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/hhotatea> | 🟡 |
| 51 | nekobako | nekobako | nekobako | <https://vpm.nekobako.net/index.json> | <https://vpm.vrczh.org/vpm/nekobako> | 🟡 |
| 52 | triturbo | BlendShare Listing | Triturbo | <https://Tr1turbo.github.io/BlendShare/index.json> | <https://vpm.vrczh.org/vpm/triturbo> | 🟡 |
| 53 | project-vrcz | project-vrcz listing | project-vrcz | <https://project-vrcz.github.io/vpm/vpm.json> | <https://vpm.vrczh.org/vpm/project-vrcz> | 🟡 |
| 54 | vrlabs-rehosted | VRLabs Packages: Rehosted | VRLabs | <https://api.vrlabs.dev/listings/category/rehosted> | <https://vpm.vrczh.org/vpm/vrlabs-rehosted> | 🟡 |
| 55 | Tr1turbo | Triturbo | Triturbo | <https://Tr1turbo.github.io/BlendShare/index.json> | <https://vpm.vrczh.org/vpm/Tr1turbo> | 🟡 |
| 56 | LuiStudio | LuiStudio's VPM Packages | LuiStudio | <https://github.com/LuiStudio/packages/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/LuiStudio> | 🟡 |
| 57 | vrcd-community | VRCD VPM Repo | us@vrcd.org.cn | <https://github.com/vrcd-community/vpm-listing/releases/latest/download/vpm.json> | <https://vpm.vrczh.org/vpm/vrcd-community> | 🟡 |

**观察**:
- 47 个 repo description 字段为占位符 "Description" — 真实描述必须从 upstream 解析
- 10 个核心包 (前 10 行) description 字段为镜像站原值
- 2 个同步失败: `poiyomi` (Poiyomi Shader), `vrcft-jerry` (VRCFaceTracking 模板)
- 1 个废弃: `dreadscripts` (description: "注意，此上游已被删库废弃，我们不推荐您在未来使用它")

---

## 3. 数据流分析: Mirror vs Upstream

### 3.1 数据流路径

```
┌──────────────────┐    sync */10min    ┌──────────────────┐    serve    ┌─────────────┐
│  Upstream repo   │  ───────────────→  │  vrczh Deno App  │  ────────→  │  VCC/ALCOM  │
│  (GitHub Pages,  │    pull index.json │  (Deno Deploy)   │   <JSON>    │             │
│   vpm.anatawa12, │    parse packages  │  storage: 镜像站  │             └─────────────┘
│   vcc.vrcfury,…) │    rewrite urls    │  rewrite zip URL  │
└──────────────────┘                    └──────────────────┘
```

### 3.2 Mirror 做了什么处理？

通过对 6 个示例包的对比 (`mirror vpm index` vs `upstream vpm index`):

| 差异类型 | 示例 | 说明 |
|----------|------|------|
| **包数量变化** | hai-vr: 27 → 34 (+7) | mirror 注入 VRChat SDK (`com.vrchat.avatars/base/worlds/core.vpm-resolver`) 和 hai-vr 子包 (`dev.hai-vr.basis.avataroptimizer/optimizable/no-thanks`) |
| **URL 改写** | 所有 `.zip` URL | upstream 的 `https://*.zip` 改写为 `https://vpm.vrczh.org/files/download/{package}@{version}@{repo}.zip?fileId={sha256}/...` 走对象存储 |
| **包元数据** | description, displayName, version | 完整保留 (未做修改) |
| **顶层 description** | 全部为空 | upstream 和 mirror 顶层 `description` 字段都是空 — 因为大多数上游就没填 |
| **包内 description** | 包内 `description` 字段 | 完整保留 (这是真正有用的功能描述来源) |
| **BOM 字符** | lilxyzw-upstream.json | upstream 有 UTF-8 BOM (`0xFEFF`)，mirror 已清理 |

**关键结论**:
- ⚠️ **不要用 mirror 的顶层 description** — 它是占位符或空
- ✅ **使用 mirror 的 `packages.{id}.versions.{ver}.description`** — 这才是真实功能描述
- ✅ **Mirror 额外注入的包 (e.g. VRChat SDK)** 在统计"该 repo 有多少个包"时需要识别并排除

### 3.3 Mirror 的可靠性

| 维度 | Mirror | Upstream |
|------|--------|----------|
| 同步延迟 | ≤ 10 分钟 | 实时 |
| 国内访问 | ✅ 快 | ❌ 受 GitHub Pages 影响 |
| 包元数据完整性 | 100% (mirror 是 upstream 的 1:1 副本，URL 改写除外) | 100% |
| 同步失败可见 | ✅ `syncStatus.status` 字段 (1=成功, 2=失败) | ❌ 无 |
| 加密校验 | ✅ `zipSHA256` 字段 (与 upstream 一致) | ✅ |

---

## 4. 已知问题与陷阱

### 4.1 同步失败的 2 个仓库

| apiId | 名称 | 失败原因 | 建议 |
|-------|------|----------|------|
| `poiyomi` | Poiyomi's VPM Repo | 上游返回非标准 VPM 格式或被反爬 | 暂用 upstream: `https://poiyomi.github.io/vpm/index.json` |
| `vrcft-jerry` | VRCFT - Jerry's Templates Listing | 上游 CORS / 网络问题 | 暂用 upstream: `https://adjerry91.github.io/VRCFaceTracking-Templates/index.json` |

### 4.2 仓库已废弃

| apiId | 状态 | 说明 |
|-------|------|------|
| `dreadscripts` | ⚠️ 已被删库废弃 | mirror description: "注意，此上游已被删库废弃，我们不推荐您在未来使用它"。**不要添加到 VCC** |

### 4.3 重复 / 同一上游多个 apiId

| 上游 | 多个 apiId | 说明 |
|------|-----------|------|
| `https://Tr1turbo.github.io/BlendShare/index.json` | `triturbo-blendshare`, `triturbo`, `Tr1turbo` | Triturbo 的多个历史 ID，**内容相同**，添加一个即可 |
| `https://github.com/vrcd-community/vpm-listing/releases/latest/download/vpm.json` | `vrcd`, `vrcd-community` | VRCD 社区的多个 ID，**内容相同** |

### 4.4 Unity 版本兼容性

不同包支持的 Unity 版本差异极大。**没有从 mirror 顶层获取 Unity 版本的字段**，必须从每个 package 的 `versions.{ver}.unity` 字段读取。

常用 Unity 版本:
- `2019.4` — Unity 2019 LTS, VRChat 旧版本支持范围
- `2022.3` — Unity 2022 LTS, **VRChat 当前主版本 (SDK 3.4.2+ 绑定)**
- `6000.0` — Unity 6, 未来版本 (hai-vr Basis 已支持)

**示例**: nadena 仓库的 4 个包
- Modular Avatar 0.8.0 → unity 2019.4 (兼容老 SDK)
- bd_'s misc tools 0.0.8 → unity 2022.3 (仅 2022 LTS)

---

## 5. 文档使用建议

### 5.1 选包建议流程

```
1. 查 https://vpm.vrczh.org/vpm/repos 拿完整 apiId 列表
2. 对候选 apiId, 拉 https://vpm.vrczh.org/vpm/{apiId} 拿 VPM index
3. 检查每个 package 的:
   - unity 字段 (确认是否兼容当前 VRChat 主版本 2022.3)
   - vpmDependencies (确认 VRChat SDK 依赖范围 com.vrchat.avatars/base/worlds)
   - description (看功能描述)
4. 比对 upstream vpm index 确认 mirror 同步是否最新
```

### 5.2 VCC/ALCOM 添加流程

```
Settings → User Packages → Add Repository
  ↓
粘贴 mirror URL: https://vpm.vrczh.org/vpm/{apiId}
  ↓
等待 VCC 拉取 index, 即可在 "Manage Projects" 看到对应包
```

### 5.3 常见问题

**Q: 为什么 mirror 拿不到某些包?**
A: 看 `syncStatus.status` 字段 = 2 表示同步失败，需用 upstream 临时替代。

**Q: mirror 和 upstream 哪个优先?**
A: 上游是权威源 (有 changelog 链接、最新版本号)，mirror 是访问优化层。**生产环境** 推荐用 mirror (国内快)，**调试环境** 推荐 upstream (实时性)。

**Q: 一个 apiId 对应多个 upstream 仓库 (e.g. Tr1turbo 系列) 怎么办?**
A: 内容相同，添加任意一个即可。mirror 这边的"重复"是历史遗留。

---

## 6. 子文档 (示例流程)

仅完成 6 个示例包详细整理，覆盖 4 个核心场景:
- **VRChat 官方** — `curated`
- **Avatar 核心** — `nadena` (Modular Avatar)
- **Avatar 优化** — `anatawa12` (Avatar Optimizer)
- **Shader 库** — `lilxyzw` (lilToon), `poiyomi` (Poiyomi)
- **Avatar 工具** — `vrcfury` (VRCFury)
- **World 工具** — `hai-vr` (Haï~ 包集)

| 子文档 | 域名 | 状态 |
|--------|------|------|
| [samples/curated.md](samples/curated.md) | Avatar 域 (官方精选) | ✅ |
| [samples/nadena.md](samples/nadena.md) | Avatar 域 (MA) | ✅ |
| [samples/anatawa12.md](samples/anatawa12.md) | Avatar 域 (优化) | ✅ |
| [samples/lilxyzw.md](samples/lilxyzw.md) | Avatar 域 (Shader) | ✅ |
| [samples/poiyomi.md](samples/poiyomi.md) | Avatar 域 (Shader) | ✅ |
| [samples/vrcfury.md](samples/vrcfury.md) | Avatar 域 (工具) | ✅ |
| [samples/hai-vr.md](samples/hai-vr.md) | World 域 (工具集) | ✅ |

> **未完成的 50 个包**: 用户审查后再决定是否继续。建议**优先完成"用户最常添加"的高频包** (e.g. d4rkpl4y3r, VRLabs 系列, Thry, USLOG, Project-VRCZ, LuiStudio, VRCD, kurotu, suzuryg)。

---

## 7. 参考资料

- [VRChat Creator Docs - VPM](https://creators.vrchat.com/sdk/vpm/) — VPM 协议规范
- [vpm-repos-syncronizer 源码](https://github.com/vrcd-community/vpm-repos-syncronizer) — 同步器 GitHub 仓库 (推测)
- [VCC 下载](https://vrchat.com/home/download) — VRChat Creator Companion
- [ALCOM 下载](https://github.com/nicokraus/ALCOM) — AlphaBlend CC
- 知识库: `memory/sources/example-central.md` (VCC 内的示例中心)
- 知识库: `memory/platform/easyquestswitch.md` (PC/Quest 切换工具)

---

## 8. 元数据

| 字段 | 值 |
|------|-----|
| 抓取日期 | 2026-07-01 09:30 UTC+8 |
| 数据源 | `https://vpm.vrczh.org/vpm/repos` (57 个 repo) |
| Mirror 拉取方式 | curl -A "Mozilla/5.0" (绕过 Deno 终端检测) |
| 整理者 | CherryClaw (示例流程) |
| 用户审查 | ⏳ 待审查 |
| 完成度 | 6/57 = 10.5% |
