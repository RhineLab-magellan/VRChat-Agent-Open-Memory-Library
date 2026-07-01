#!/usr/bin/env python3
"""
A6 灾难恢复脚本
=================
修复 refine_tier_a.py 第二次运行时导致的所有 Tier A 文件 frontmatter 损坏。

损坏模式:
1. `confidence: [Value]---` - `---` 终止符粘连到 YAML 值末尾(无换行)
2. 重复 frontmatter 块(FACT.md 特殊)
3. 缺少 `---` 终止符(行直接连接 body)

修复策略:
- 对每个 Tier A 文件,定位 BODY(找到第一个看起来像 body 开头的行)
- 用 A6 REFINEMENTS 中定义的"正确 frontmatter"重写文件
"""
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'

# 正确的 Tier A frontmatter 定义(从 refine_tier_a.py 复制)
# 格式: rel_path -> 完整 frontmatter 字符串(不包含外层 ---)
TIER_A_FRONTMATTERS = {
    'FACT.md': """title: FACT.md - VRChat 技术知识库
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
  - sources/index.md
  - patterns/index.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'index.md': """title: KB Index — Multi-Domain 路由地图
category: misc

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - 知识库总入口
  - "Knowledge Base Index"
  - 导航
  - 总索引

related:
  - FACT.md
  - _always-load.md
  - api/index.md
  - avatar/index.md
  - world/index.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High""",

    '_always-load.md': """title: VRChat 全领域核心约束速查
category: misc

knowledge_level: applied
status: active

tags:
  - misc
  - reference
  - core-constraints

aliases:
  - 核心约束
  - "Critical Constraints"
  - 速查表
  - Cheatsheet

related:
  - FACT.md
  - index.md
  - rules/udonsharp-language-limits.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/networking.md': """title: API: Networking
category: api

knowledge_level: core
status: active

tags:
  - api
  - networking
  - sync
  - performance
  - serialization
  - ownership

aliases:
  - Networking
  - "网络 API"
  - 网络同步
  - "Networking API"

related:
  - api/udonsharp-runtime.md
  - api/events-reference.md
  - api/udon-type-exposure.md
  - world/udon/networking/index.md
  - world/performance-guide.md
  - rules/udonsharp-language-limits.md
  - avatar/performance-rank.md
  - api/persistence.md
  - api/pickups.md
  - world/scene-components/vrc-objectsync.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/udonsharp-runtime.md': """title: API: UdonSharp 运行时系统
category: api

knowledge_level: core
status: active

tags:
  - api
  - udonsharp
  - runtime
  - program-variable
  - field-callback

aliases:
  - UdonSharp 运行时
  - "UdonSharp Runtime"
  - Udon 运行时系统
  - 运行时

related:
  - api/networking.md
  - api/udon-type-exposure.md
  - api/events-reference.md
  - world/udonsharp-compilation.md
  - rules/udonsharp-language-limits.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/events-reference.md': """title: API: Udon Events Reference
category: api

knowledge_level: core
status: active

tags:
  - api
  - events
  - udon
  - reference
  - callback

aliases:
  - Events Reference
  - Udon 事件参考
  - 事件全集
  - Event Reference

related:
  - api/networking.md
  - api/udonsharp-runtime.md
  - api/player-api.md
  - world/udon/networking/events.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/udon-type-exposure.md': """title: API: Udon Type Exposure Tree
category: api

knowledge_level: core
status: active

tags:
  - api
  - udon
  - type-exposure
  - whitelist
  - reference

aliases:
  - Udon Type Exposure
  - Udon 类型暴露
  - 类型暴露树
  - Type Exposure

related:
  - api/exposed-types.md
  - api/not-exposed.md
  - api/udonsharp-runtime.md
  - rules/udonsharp-language-limits.md
  - api/networking.md
  - world/udon/vm-and-assembly.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/exposed-types.md': """title: API: Exposed Types List
category: api

knowledge_level: core
status: active

tags:
  - api
  - udon
  - type-exposure
  - whitelist
  - reference

aliases:
  - Exposed Types
  - 已暴露类型
  - 类型清单
  - Exposed Types List

related:
  - api/udon-type-exposure.md
  - api/not-exposed.md
  - api/udonsharp-runtime.md
  - rules/udonsharp-language-limits.md
  - api/api-checker.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/persistence.md': """title: API: Persistence
category: api

knowledge_level: core
status: active

tags:
  - api
  - persistence
  - playerdata
  - worlddata
  - storage

aliases:
  - Persistence
  - 持久化
  - PlayerData
  - 数据持久化

related:
  - api/networking.md
  - api/udonsharp-runtime.md
  - world/vrc-enablepersistence.md
  - world/data-containers.md
  - rules/udonsharp-language-limits.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/dynamics.md': """title: API: VRChat Dynamics for Worlds
category: api

knowledge_level: core
status: active

tags:
  - api
  - physbone
  - contact
  - constraint
  - event

aliases:
  - Dynamics API
  - 动态系统
  - "PhysBone/Contact API"
  - Dynamics

related:
  - api/networking.md
  - api/player-api.md
  - avatar/performance-rank.md
  - avatar/vrc-constraints.md

source: VRChat 官方文档 + VRChat Agent Skills 模块
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'api/pickups.md': """title: API: VRCPickup System
category: api

knowledge_level: core
status: active

tags:
  - api
  - pickup
  - interaction
  - vrcpickup

aliases:
  - Pickups
  - 拾取 API
  - VRCPickup
  - 拾取系统

related:
  - api/networking.md
  - api/player-api.md
  - api/dynamics.md
  - world/scene-components/vrc-pickup.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'world/performance-guide.md': """title: World Performance Optimization Guide
category: world

knowledge_level: core
status: active

tags:
  - world
  - performance
  - optimization
  - culling
  - lighting
  - quest

aliases:
  - Performance Guide
  - World 性能优化
  - 性能优化指南
  - World Performance

related:
  - api/networking.md
  - avatar/performance-rank.md
  - world/vrc-light-volumes.md
  - world/occlusion-culling-guide.md
  - world/reflection-probes.md
  - world/udonsharp-compilation.md
  - rules/networking-rules.md

source: VRChat 官方文档 + 本地整理
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'world/udonsharp-compilation.md': """title: UdonSharp Compilation Pipeline
category: world

knowledge_level: core
status: active

tags:
  - world
  - udonsharp
  - compilation
  - pipeline
  - roslyn

aliases:
  - UdonSharp Compilation
  - UdonSharp 编译管线
  - 编译流程
  - Compilation Pipeline

related:
  - api/udonsharp-runtime.md
  - api/udon-type-exposure.md
  - world/performance-guide.md
  - rules/udonsharp-language-limits.md
  - world/udon/vm-and-assembly.md

source: VRChat + UdonSharp 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'world/data-containers.md': """title: World Data Containers
category: world

knowledge_level: core
status: active

tags:
  - world
  - data
  - json
  - container
  - udonsharp

aliases:
  - Data Containers
  - 数据容器
  - VRCJson
  - DataToken

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: Medium""",

    'world/vrc-graphics.md': """title: VRC Graphics & Shader API
category: world

knowledge_level: core
status: active

tags:
  - world
  - graphics
  - shader
  - blit
  - global

aliases:
  - VRCGraphics
  - VRCShader
  - 图形 API
  - Graphics API

related:
  - api/udonsharp-runtime.md
  - world/performance-guide.md
  - world/vrc-light-volumes.md
  - api/exposed-types.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'world/vrc-light-volumes.md': """title: VRC Light Volumes
category: world

knowledge_level: core
status: active

tags:
  - world
  - lighting
  - light-probe
  - voxel
  - dynamic-light

aliases:
  - VRC Light Volumes
  - 光照系统
  - Light Volumes
  - VRCLightVolumes

related:
  - world/performance-guide.md
  - world/occlusion-culling-guide.md
  - world/reflection-probes.md
  - world/vrc-graphics.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'world/occlusion-culling-guide.md': """title: World Occlusion Culling Guide
category: world

knowledge_level: core
status: active

tags:
  - world
  - culling
  - performance
  - optimization
  - umbra

aliases:
  - Occlusion Culling
  - 遮挡剔除
  - Culling Guide
  - 性能剔除

related:
  - world/performance-guide.md
  - world/vrc-light-volumes.md
  - world/reflection-probes.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'avatar/optimization-guide.md': """title: Avatar Optimization Guide
category: avatar

knowledge_level: core
status: active

tags:
  - avatar
  - optimization
  - performance
  - mesh
  - shader

aliases:
  - Avatar Optimization
  - Avatar 优化
  - 性能优化
  - Avatar Performance

related:
  - avatar/performance-rank.md
  - avatar/ndmf-tools.md
  - avatar/playable-layers.md
  - avatar/vrc-constraints.md
  - avatar/vrcfury-reference.md
  - avatar/modular-avatar.md
  - world/performance-guide.md

source: VRChat 官方文档 + 本地整理
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'avatar/playable-layers.md': """title: Avatar Playable Layers
category: avatar

knowledge_level: core
status: active

tags:
  - avatar
  - playable-layers
  - animator
  - fx
  - gesture

aliases:
  - Playable Layers
  - 播放层
  - Avatar 播放层
  - FX Layer

related:
  - avatar/optimization-guide.md
  - avatar/performance-rank.md
  - avatar/vrc-constraints.md
  - avatar/animator.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'avatar/performance-rank.md': """title: Avatar Performance Rank
category: avatar

knowledge_level: core
status: active

tags:
  - avatar
  - performance
  - rank
  - benchmark
  - quest

aliases:
  - Performance Rank
  - Avatar 性能分级
  - 性能等级
  - 性能排名

related:
  - avatar/optimization-guide.md
  - avatar/ndmf-tools.md
  - avatar/playable-layers.md
  - world/performance-guide.md
  - api/dynamics.md
  - api/networking.md
  - avatar/vrc-constraints.md
  - avatar/modular-avatar.md
  - rules/performance-rules.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'avatar/vrc-constraints.md': """title: VRC Constraints
category: avatar

knowledge_level: core
status: active

tags:
  - avatar
  - constraint
  - vrc-constraint
  - animator
  - position

aliases:
  - VRC Constraints
  - 约束系统
  - Avatar Constraints
  - VRC 约束

related:
  - avatar/optimization-guide.md
  - avatar/playable-layers.md
  - avatar/performance-rank.md
  - avatar/animator.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'hybrid/osc-protocol.md': """title: OSC Protocol
category: hybrid

knowledge_level: core
status: active

tags:
  - hybrid
  - osc
  - protocol
  - external
  - api

aliases:
  - OSC Protocol
  - OSC 协议
  - "Open Sound Control"
  - OSC

related:
  - api/player-api.md
  - api/events-reference.md
  - vrchatsdk/01_首页.md

source: VRChat 官方文档 + 本地整理
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'platform/cross-platform-content.md': """title: Cross-Platform Content (PC/Quest)
category: platform

knowledge_level: core
status: active

tags:
  - platform
  - quest
  - pc
  - compatibility
  - avatar

aliases:
  - Cross Platform
  - 跨平台
  - "PC/Quest 兼容"
  - Cross-Platform

related:
  - platform/easyquestswitch.md
  - platform/mobile-ui-optimization.md
  - avatar/optimization-guide.md
  - world/performance-guide.md
  - platform/android-development.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'platform/easyquestswitch.md': """title: EasyQuestSwitch
category: platform

knowledge_level: core
status: active

tags:
  - platform
  - quest
  - tool
  - automation
  - type-handler

aliases:
  - EasyQuestSwitch
  - Quest 切换
  - "PC/Quest 切换"
  - EQS

related:
  - platform/cross-platform-content.md
  - platform/android-development.md
  - sources/example-central.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'vrchatsdk/01_首页.md': """title: VRChatSDK 首页
category: vrchatsdk

knowledge_level: core
status: active

tags:
  - vrchatsdk
  - api
  - http
  - websocket
  - sdk

aliases:
  - VRChatSDK
  - VRChat SDK
  - HTTP API
  - SDK 首页

related:
  - vrchatsdk/02_TypeScript_SDK.md
  - vrchatsdk/03_Websocket_API.md
  - vrchatsdk/04_Instances.md
  - hybrid/osc-protocol.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'rules/index.md': """title: Rules Index — 硬性约束目录
category: rules

knowledge_level: core
status: active

tags:
  - rules
  - constraints
  - reference
  - hard-limit

aliases:
  - Rules Index
  - 规则索引
  - Rules
  - 硬性约束

related:
  - rules/udonsharp-language-limits.md
  - rules/networking-rules.md
  - rules/performance-rules.md
  - rules/security-rules.md
  - FACT.md
  - patterns/index.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'patterns/index.md': """title: Patterns Index — 设计模式目录
category: patterns

knowledge_level: core
status: active

tags:
  - patterns
  - design-pattern
  - udon
  - networking
  - reference

aliases:
  - Patterns Index
  - 模式索引
  - Patterns
  - 设计模式

related:
  - patterns/master-follower-syncer.md
  - patterns/manual-sync-owner-authority.md
  - patterns/exclusive-control-selector.md
  - sources/index.md
  - rules/index.md
  - FACT.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High""",

    'sources/index.md': """title: Sources Index — 参考工程目录
category: sources

knowledge_level: core
status: active

tags:
  - sources
  - open-source
  - reference
  - architecture
  - case-study

aliases:
  - Sources Index
  - 来源索引
  - Sources
  - 参考工程索引

related:
  - sources/open-source-projects.md
  - sources/example-central.md
  - sources/ulocalization.md
  - sources/sardinal.md
  - sources/vvmw.md
  - sources/udonvoiceutils.md
  - sources/quickbrown-luraswitch2.md
  - sources/udonworld-plugins.md
  - FACT.md
  - patterns/index.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: High""",
}


def find_body_start(lines):
    """在损坏的文件中找到 body 的起始行(0-indexed)

    策略:
    1. 找到所有 '---' 行位置
    2. 对每对 (1, 2) 候选 frontmatter,检查后续内容
    3. body 通常以 `# `, `## `, `---`(horizontal rule) 开头
    4. 真正的 body 是最长的合法内容块
    """
    # 找到所有 '---' 行位置(0-indexed)
    dash_positions = [i for i, line in enumerate(lines) if line.strip() == '---']
    if not dash_positions:
        return None

    # 找到第一个 'title:' 行(代表 frontmatter 开始)
    title_pos = None
    for i, line in enumerate(lines[:60]):
        if re.match(r'^title:\s', line):
            title_pos = i
            break
    if title_pos is None:
        return None

    # 真正的 frontmatter 起始在 title_pos - 1 (即 '---' 行)
    # 真正的 frontmatter 结束在最后一个 '---' 行(在 title 之后)
    frontmatter_end = None
    for pos in dash_positions:
        if pos > title_pos:
            frontmatter_end = pos
            # 不要 break,要找最后一个

    if frontmatter_end is None:
        return None

    # body 起始在 frontmatter_end + 1
    body_start = frontmatter_end + 1

    # 验证 body 看起来合理
    if body_start < len(lines):
        # body 应该以非 frontmatter 内容开始
        # 但很多文件有 "---" 之后跟空行再跟 # 标题
        # 如果 body_start 行是空行,跳过到第一个非空行
        while body_start < len(lines) and lines[body_start].strip() == '':
            body_start += 1
        # 现在 body 应该在第一个 '---' 后的第一个非空行

    return body_start


def repair_file(rel_path, correct_frontmatter):
    """修复单个文件"""
    filepath = MEMORY_ROOT / rel_path
    if not filepath.exists():
        return {'file': rel_path, 'status': 'MISSING'}

    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    body_start = find_body_start(lines)
    if body_start is None:
        return {'file': rel_path, 'status': 'NO_BODY_FOUND'}

    # 提取 body(从 body_start 到文件末尾)
    body = '\n'.join(lines[body_start:])

    # 重新组装: ---\n[frontmatter]\n---\n[body]
    new_content = f'---\n{correct_frontmatter}\n---\n{body}'

    filepath.write_text(new_content, encoding='utf-8')
    return {
        'file': rel_path,
        'status': 'OK',
        'body_start_line': body_start + 1,
        'new_total_lines': new_content.count('\n') + 1,
    }


def main():
    print("=" * 80)
    print("A6 Tier A Disaster Recovery")
    print("=" * 80)
    print(f"Total files to repair: {len(TIER_A_FRONTMATTERS)}")

    results = []
    for rel_path, fm in TIER_A_FRONTMATTERS.items():
        result = repair_file(rel_path, fm)
        results.append(result)
        if result['status'] == 'OK':
            print(f"  [OK] {rel_path} (body start L{result['body_start_line']}, total {result['new_total_lines']} lines)")
        else:
            print(f"  [ERR] {rel_path}: {result['status']}")

    ok = sum(1 for r in results if r['status'] == 'OK')
    err = sum(1 for r in results if r['status'] != 'OK')
    print(f"\nSummary: {ok} repaired, {err} errors")
    return 0 if err == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
