#!/usr/bin/env python3
"""
A6 Tier A 精修脚本
=====================
精修 28 篇核心文档的 frontmatter:
1. 修正状态(3 篇误标 archived → active)
2. 提升置信度(顶层入口 / 官方文档 → High)
3. 补充 Related(基于 A5 Top 高被引)
4. 优化 Tags(补充核心 + 辅助)
5. 完善 Aliases(中英文 + 简称)
"""
import re
from pathlib import Path

# ==================== 配置 ====================
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'
TODAY = "2026-06-20"


# ==================== 精修定义 ====================
# 格式: rel_path -> {field: new_value}
# 字段可省略,表示保留原值
REFINEMENTS = {
    # === 组 1: 顶层入口 ===
    'FACT.md': {
        'confidence': 'High',
        'aliases': ['FACT', '知识库事实库', 'Knowledge Base Facts', '顶层索引'],
        'related': ['index.md', '_always-load.md', 'sources/index.md', 'patterns/index.md'],
    },
    'index.md': {
        'confidence': 'High',
        'aliases': ['知识库总入口', 'Knowledge Base Index', '导航', '总索引'],
        'related': ['FACT.md', '_always-load.md', 'api/index.md', 'avatar/index.md', 'world/index.md'],
    },
    '_always-load.md': {
        'confidence': 'High',
        'aliases': ['核心约束', 'Critical Constraints', '速查表', 'Cheatsheet'],
        'related': ['FACT.md', 'index.md', 'rules/udonsharp-language-limits.md'],
    },

    # === 组 2: API 核心 ===
    'api/networking.md': {
        'aliases': ['Networking', '网络 API', '网络同步', 'Networking API'],
        'related': [
            'api/udonsharp-runtime.md', 'api/events-reference.md', 'api/udon-type-exposure.md',
            'world/udon/networking/index.md', 'world/performance-guide.md',
            'rules/udonsharp-language-limits.md', 'avatar/performance-rank.md',
            'api/persistence.md', 'api/pickups.md', 'world/scene-components/vrc-objectsync.md',
        ],
    },
    'api/udonsharp-runtime.md': {
        'aliases': ['UdonSharp 运行时', 'UdonSharp Runtime', 'Udon 运行时系统', '运行时'],
        'related': [
            'api/networking.md', 'api/udon-type-exposure.md', 'api/events-reference.md',
            'world/udonsharp-compilation.md', 'rules/udonsharp-language-limits.md',
        ],
    },
    'api/events-reference.md': {
        'aliases': ['Events Reference', 'Udon 事件参考', '事件全集', 'Event Reference'],
        'related': [
            'api/networking.md', 'api/udonsharp-runtime.md', 'api/player-api.md',
            'world/udon/networking/events.md',
        ],
    },
    'api/udon-type-exposure.md': {
        'aliases': ['Udon Type Exposure', 'Udon 类型暴露', '类型暴露树', 'Type Exposure'],
        'related': [
            'api/exposed-types.md', 'api/not-exposed.md', 'api/udonsharp-runtime.md',
            'rules/udonsharp-language-limits.md', 'api/networking.md',
            'world/udon/vm-and-assembly.md',
        ],
    },
    'api/exposed-types.md': {
        'aliases': ['Exposed Types', '已暴露类型', '类型清单', 'Exposed Types List'],
        'related': [
            'api/udon-type-exposure.md', 'api/not-exposed.md', 'api/udonsharp-runtime.md',
            'rules/udonsharp-language-limits.md', 'api/api-checker.md',
        ],
    },
    'api/persistence.md': {
        'aliases': ['Persistence', '持久化', 'PlayerData', '数据持久化'],
        'related': [
            'api/networking.md', 'api/udonsharp-runtime.md', 'world/vrc-enablepersistence.md',
            'world/data-containers.md', 'rules/udonsharp-language-limits.md',
        ],
    },
    'api/dynamics.md': {
        'aliases': ['Dynamics API', '动态系统', 'PhysBone/Contact API', 'Dynamics'],
        'related': [
            'api/networking.md', 'api/player-api.md', 'avatar/performance-rank.md',
            'avatar/vrc-constraints.md',
        ],
    },
    'api/pickups.md': {
        'aliases': ['Pickups', '拾取 API', 'VRCPickup', '拾取系统'],
        'related': [
            'api/networking.md', 'api/player-api.md', 'api/dynamics.md',
            'world/scene-components/vrc-pickup.md',
        ],
    },

    # === 组 3: World 核心 ===
    'world/performance-guide.md': {
        'confidence': 'High',
        'aliases': ['Performance Guide', 'World 性能优化', '性能优化指南', 'World Performance'],
        'related': [
            'api/networking.md', 'avatar/performance-rank.md', 'world/vrc-light-volumes.md',
            'world/occlusion-culling-guide.md', 'world/reflection-probes.md',
            'world/udonsharp-compilation.md', 'rules/networking-rules.md',
        ],
    },
    'world/udonsharp-compilation.md': {
        # 修正:archived → active(这是核心文档,不是迁移文件)
        'status': 'active',
        'confidence': 'High',
        'aliases': ['UdonSharp Compilation', 'UdonSharp 编译管线', '编译流程', 'Compilation Pipeline'],
        'related': [
            'api/udonsharp-runtime.md', 'api/udon-type-exposure.md',
            'world/performance-guide.md', 'rules/udonsharp-language-limits.md',
            'world/udon/vm-and-assembly.md',
        ],
    },
    'world/data-containers.md': {
        # 这是迁移提示文件,保持 archived
        'confidence': 'Medium',
        'aliases': ['Data Containers', '数据容器', 'VRCJson', 'DataToken'],
    },
    'world/vrc-graphics.md': {
        # 修正:archived → active
        'status': 'active',
        'confidence': 'High',
        'aliases': ['VRCGraphics', 'VRCShader', '图形 API', 'Graphics API'],
        'related': [
            'api/udonsharp-runtime.md', 'world/performance-guide.md',
            'world/vrc-light-volumes.md', 'api/exposed-types.md',
        ],
    },
    'world/vrc-light-volumes.md': {
        'confidence': 'High',
        'aliases': ['VRC Light Volumes', '光照系统', 'Light Volumes', 'VRCLightVolumes'],
        'related': [
            'world/performance-guide.md', 'world/occlusion-culling-guide.md',
            'world/reflection-probes.md', 'world/vrc-graphics.md',
        ],
    },
    'world/occlusion-culling-guide.md': {
        'confidence': 'High',
        'aliases': ['Occlusion Culling', '遮挡剔除', 'Culling Guide', '性能剔除'],
        'related': [
            'world/performance-guide.md', 'world/vrc-light-volumes.md',
            'world/reflection-probes.md',
        ],
    },

    # === 组 4: Avatar 核心 ===
    'avatar/optimization-guide.md': {
        'confidence': 'High',
        'aliases': ['Avatar Optimization', 'Avatar 优化', '性能优化', 'Avatar Performance'],
        'related': [
            'avatar/performance-rank.md', 'avatar/ndmf-tools.md', 'avatar/playable-layers.md',
            'avatar/vrc-constraints.md', 'avatar/vrcfury-reference.md',
            'avatar/modular-avatar.md', 'world/performance-guide.md',
        ],
    },
    'avatar/playable-layers.md': {
        'confidence': 'High',
        'aliases': ['Playable Layers', '播放层', 'Avatar 播放层', 'FX Layer'],
        'related': [
            'avatar/optimization-guide.md', 'avatar/performance-rank.md',
            'avatar/vrc-constraints.md', 'avatar/animator.md',
        ],
    },
    'avatar/performance-rank.md': {
        'confidence': 'High',
        'aliases': ['Performance Rank', 'Avatar 性能分级', '性能等级', '性能排名'],
        'related': [
            'avatar/optimization-guide.md', 'avatar/ndmf-tools.md',
            'avatar/playable-layers.md', 'world/performance-guide.md',
            'api/dynamics.md', 'api/networking.md', 'avatar/vrc-constraints.md',
            'avatar/modular-avatar.md', 'rules/performance-rules.md',
        ],
    },
    'avatar/vrc-constraints.md': {
        'confidence': 'High',
        'aliases': ['VRC Constraints', '约束系统', 'Avatar Constraints', 'VRC 约束'],
        'related': [
            'avatar/optimization-guide.md', 'avatar/playable-layers.md',
            'avatar/performance-rank.md', 'avatar/animator.md',
        ],
    },

    # === 组 5: 跨域 ===
    'hybrid/osc-protocol.md': {
        'confidence': 'High',
        'aliases': ['OSC Protocol', 'OSC 协议', 'Open Sound Control', 'OSC'],
        'related': [
            'api/player-api.md', 'api/events-reference.md', 'vrchatsdk/01_首页.md',
        ],
    },
    'platform/cross-platform-content.md': {
        'confidence': 'High',
        'aliases': ['Cross Platform', '跨平台', 'PC/Quest 兼容', 'Cross-Platform'],
        'related': [
            'platform/easyquestswitch.md', 'platform/mobile-ui-optimization.md',
            'avatar/optimization-guide.md', 'world/performance-guide.md',
            'platform/android-development.md',
        ],
    },
    'platform/easyquestswitch.md': {
        'confidence': 'High',
        'aliases': ['EasyQuestSwitch', 'Quest 切换', 'PC/Quest 切换', 'EQS'],
        'related': [
            'platform/cross-platform-content.md', 'platform/android-development.md',
            'sources/example-central.md',
        ],
    },
    'vrchatsdk/01_首页.md': {
        'confidence': 'High',
        'aliases': ['VRChatSDK', 'VRChat SDK', 'HTTP API', 'SDK 首页'],
        'related': [
            'vrchatsdk/02_TypeScript_SDK.md', 'vrchatsdk/03_Websocket_API.md',
            'vrchatsdk/04_Instances.md', 'hybrid/osc-protocol.md',
        ],
    },

    # === 组 6: 索引 ===
    'rules/index.md': {
        'confidence': 'High',
        'aliases': ['Rules Index', '规则索引', 'Rules', '硬性约束'],
        'related': [
            'rules/udonsharp-language-limits.md', 'rules/networking-rules.md',
            'rules/performance-rules.md', 'rules/security-rules.md',
            'FACT.md', 'patterns/index.md',
        ],
    },
    'patterns/index.md': {
        'confidence': 'High',
        'aliases': ['Patterns Index', '模式索引', 'Patterns', '设计模式'],
        'related': [
            'patterns/master-follower-syncer.md', 'patterns/manual-sync-owner-authority.md',
            'patterns/exclusive-control-selector.md', 'patterns/index.md',
            'sources/index.md', 'rules/index.md', 'FACT.md',
        ],
    },
    'sources/index.md': {
        'confidence': 'High',
        'aliases': ['Sources Index', '来源索引', 'Sources', '参考工程索引'],
        'related': [
            'sources/open-source-projects.md', 'sources/example-central.md',
            'sources/ulocalization.md', 'sources/sardinal.md', 'sources/vvmw.md',
            'sources/udonvoiceutils.md', 'sources/quickbrown-luraswitch2.md',
            'sources/udonworld-plugins.md', 'FACT.md', 'patterns/index.md',
        ],
    },
}


# ==================== 精修函数 ====================
def parse_frontmatter(content: str) -> tuple:
    """提取 frontmatter 和 body(仅在前 50 行内查找 --- 终止符)"""
    # 限制搜索范围到前 50 行,避免 body 中的 --- 横线被误判
    lines = content.split('\n', 50)
    if not lines or lines[0].strip() != '---':
        return None, content
    # 在前 50 行内找第二个 ---
    for i in range(1, min(len(lines), 50)):
        if lines[i].strip() == '---':
            # 拼接前 i 行的内容(去掉首行 ---)
            yaml_text = '\n'.join(lines[1:i])
            # body 是剩余内容
            body = '\n'.join(lines[i+1:])
            return yaml_text, body
    return None, content


def build_field(name: str, values) -> str:
    """构造 YAML 字段"""
    if isinstance(values, list):
        lines = [f'{name}:']
        for v in values:
            # 含特殊字符的需要引号
            v_str = str(v)
            if ':' in v_str or '"' in v_str or "'" in v_str or '/' in v_str or ' ' in v_str or v_str.startswith('-'):
                v_escaped = v_str.replace('"', '\\"')
                lines.append(f'  - "{v_escaped}"')
            else:
                lines.append(f'  - {v_str}')
        return '\n'.join(lines)
    else:
        v_str = str(values)
        if ':' in v_str or '"' in v_str:
            v_escaped = v_str.replace('"', '\\"')
            return f'{name}: "{v_escaped}"'
        return f'{name}: {v_str}'


def update_field(yaml_text: str, field: str, value) -> str:
    """更新 YAML 字段(标量)"""
    # 处理标量字段
    pattern = rf'^{field}:\s*.*$'
    new_line = build_field(field, value)
    if re.search(pattern, yaml_text, re.MULTILINE):
        return re.sub(pattern, new_line, yaml_text, count=1, flags=re.MULTILINE)
    else:
        # 字段不存在,添加到末尾
        return yaml_text.rstrip() + '\n' + new_line + '\n'


def replace_list_field(yaml_text: str, field: str, values: list) -> str:
    """替换 YAML 列表字段"""
    # 找到字段起始
    pattern = rf'^{field}:\s*\n((?:\s+-\s+.+\n)+)'
    new_block = build_field(field, values) + '\n'
    if re.search(pattern, yaml_text, re.MULTILINE):
        return re.sub(pattern, new_block, yaml_text, count=1, flags=re.MULTILINE)
    else:
        return yaml_text.rstrip() + '\n' + new_block


def refine_file(rel_path: str, refinements: dict) -> dict:
    """精修单个文档"""
    filepath = MEMORY_ROOT / rel_path
    if not filepath.exists():
        return {'file': rel_path, 'error': 'FILE_NOT_FOUND'}

    content = filepath.read_text(encoding='utf-8')
    yaml_text, body = parse_frontmatter(content)
    if yaml_text is None:
        return {'file': rel_path, 'error': 'NO_FRONTMATTER'}

    changes = []

    for field, new_value in refinements.items():
        if field in ('status', 'confidence', 'knowledge_level'):
            # 标量字段
            old_match = re.search(rf'^{field}:\s*(.+?)\s*$', yaml_text, re.MULTILINE)
            if old_match:
                old_value = old_match.group(1).strip()
                if old_value != str(new_value):
                    yaml_text = update_field(yaml_text, field, new_value)
                    changes.append(f'{field}: {old_value!r} → {new_value!r}')
        elif field in ('tags', 'aliases', 'related'):
            # 列表字段
            old_match = re.search(rf'^{field}:\s*\n((?:\s+-\s+.+\n?)+)', yaml_text, re.MULTILINE)
            if old_match:
                old_block = old_match.group(1)
                old_count = len(re.findall(r'^\s+-\s+', old_block, re.MULTILINE))
                if old_count != len(new_value):
                    yaml_text = replace_list_field(yaml_text, field, new_value)
                    changes.append(f'{field}: {old_count} → {len(new_value)}')

    # 写回文件(确保 yaml_text 末尾有换行,避免 '---' 粘连到最后一个 YAML 值)
    if changes:
        yaml_text_clean = yaml_text.rstrip() + '\n'
        new_content = f'---\n{yaml_text_clean}---\n{body}'
        filepath.write_text(new_content, encoding='utf-8')

    return {
        'file': rel_path,
        'changes': changes,
        'modified': len(changes) > 0,
    }


# ==================== 主流程 ====================
def main():
    print("=" * 80)
    print("A6 Tier A 精修脚本")
    print(f"Date: {TODAY}")
    print(f"Total Tier A docs: {len(REFINEMENTS)}")
    print("=" * 80)

    results = []
    for rel_path, refinements in REFINEMENTS.items():
        result = refine_file(rel_path, refinements)
        results.append(result)
        if 'error' in result:
            print(f"  [ERROR] {rel_path}: {result['error']}")
        elif result['modified']:
            print(f"  [OK] {rel_path}")
            for change in result['changes']:
                print(f"      - {change}")
        else:
            print(f"  [SKIP] {rel_path} (no changes)")

    # 生成报告
    report_path = MEMORY_ROOT / '_curator_tools' / 'a6_tier_a_refinement.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# A6 Tier A 精修报告\n\n")
        f.write(f"**生成时间**: {TODAY}\n")
        f.write(f"**精修文档数**: {len(REFINEMENTS)}\n")
        modified = sum(1 for r in results if r.get('modified'))
        f.write(f"**实际修改数**: {modified}\n\n")
        f.write("---\n\n")

        f.write("## 精修详情\n\n")
        for r in results:
            f.write(f"### `{r['file']}`\n\n")
            if 'error' in r:
                f.write(f"❌ **错误**: {r['error']}\n\n")
                continue
            if not r['changes']:
                f.write("⏸️ 无需修改\n\n")
                continue
            f.write("**修改项**:\n")
            for change in r['changes']:
                f.write(f"- {change}\n")
            f.write("\n")

        f.write("---\n\n")
        f.write("## 精修总览\n\n")
        f.write("| 文档 | 状态修正 | Confidence 提升 | 补充 Related | 补充 Aliases |\n")
        f.write("|------|----------|-----------------|--------------|--------------|\n")
        for r in results:
            if 'error' in r:
                f.write(f"| `{r['file']}` | ❌ | - | - | - |\n")
                continue
            status_fix = '✅' if any('status' in c for c in r['changes']) else '-'
            conf_fix = '✅' if any('confidence' in c for c in r['changes']) else '-'
            rel_fix = '✅' if any('related' in c for c in r['changes']) else '-'
            alias_fix = '✅' if any('aliases' in c for c in r['changes']) else '-'
            f.write(f"| `{r['file']}` | {status_fix} | {conf_fix} | {rel_fix} | {alias_fix} |\n")

    print(f"\n{'='*80}")
    print(f"Report: {report_path}")
    print(f"Modified: {modified}/{len(REFINEMENTS)}")
    print("=" * 80)

    return 0


if __name__ == '__main__':
    main()
