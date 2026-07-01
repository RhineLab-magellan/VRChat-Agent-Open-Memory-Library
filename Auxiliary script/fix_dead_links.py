#!/usr/bin/env python3
"""
A7 死链修复脚本
=================
基于 governance 扫描结果,自动修复 41 条死链。
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

MEMORY_ROOT = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\memory')

# 修复映射: (source_file, old_target) -> new_target
FIXES = {
    # === liltoon 相对路径错误 ===
    ('avatar/shader/liltoon/audiolink.md', '../advanced-settings.md'): 'advanced-settings.md',
    ('avatar/shader/liltoon/audiolink.md', '../color-settings.md'): 'color-settings.md',
    ('avatar/shader/liltoon/audiolink.md', '../reflection-settings.md'): 'reflection-settings.md',
    ('avatar/shader/liltoon/dissolve.md', '../color-settings.md'): 'color-settings.md',
    ('avatar/shader/liltoon/render-modes.md', '../reflection-settings.md'): 'reflection-settings.md',
    ('avatar/shader/liltoon/overview.md', '../README.md'): 'index.md',
    ('avatar/shader/liltoon/overview.md', 'README.md'): 'index.md',

    # === orl/comparison.md 路径错误 ===
    ('avatar/shader/orl/comparison.md', 'liltoon/index.md'): '../liltoon/index.md',
    ('avatar/shader/orl/comparison.md', 'scss.md'): '../scss.md',

    # === misc 路径错误 ===
    ('misc/postprocessing-principles.md', 'performance-rules.md'): '../rules/performance-rules.md',
    ('misc/postprocessing-usage.md', 'performance-rules.md'): '../rules/performance-rules.md',

    # === sources/index.md 文件名错误 ===
    ('sources/index.md', 'sources/udonworld-plugins.md'): 'hybrid/udon-world-plugins.md',

    # === world/scene-components 路径错误(related 字段)===
    ('world/scene-components/index.md', 'whitelisted-world-components.md'): '../whitelisted-world-components.md',
    ('world/scene-components/textmeshpro.md', 'whitelisted-world-components.md'): '../whitelisted-world-components.md',
    ('world/scene-components/vrc-avatarpedestal.md', 'sdk-prefabs.md'): '../sdk-prefabs.md',
    ('world/scene-components/vrc-station.md', 'sdk-prefabs.md'): '../sdk-prefabs.md',
    ('world/scene-components/vrc-mirrorreflection.md', 'performance-guide.md'): '../performance-guide.md',
    ('world/scene-components/vrc-mirrorreflection.md', 'reflection-probes.md'): '../reflection-probes.md',
    ('world/scene-components/vrc-scenedescriptor.md', 'layers.md'): '../layers.md',
    ('world/scene-components/vrc-scenedescriptor.md', 'performance-guide.md'): '../performance-guide.md',

    # === world/scene-components 路径错误(markdown 链接,多一个 ../)===
    ('world/scene-components/vrc-avatarpedestal.md', '../../sdk-prefabs.md'): '../sdk-prefabs.md',
    ('world/scene-components/vrc-station.md', '../../sdk-prefabs.md'): '../sdk-prefabs.md',
    ('world/scene-components/vrc-mirrorreflection.md', '../../performance-guide.md'): '../performance-guide.md',
    ('world/scene-components/vrc-mirrorreflection.md', '../../reflection-probes.md'): '../reflection-probes.md',
    ('world/scene-components/vrc-scenedescriptor.md', '../../layers.md'): '../layers.md',
    ('world/scene-components/vrc-scenedescriptor.md', '../../performance-guide.md'): '../performance-guide.md',

    # === world/udon/udonsharp/attributes.md 路径错误(markdown 和 related)===
    ('world/udon/udonsharp/attributes.md', '../FACT.md'): '../../FACT.md',
    ('world/udon/udonsharp/attributes.md', '../../../../FACT.md'): '../../../FACT.md',

    # === world/udon/vrc-graphics/index.md 文件名错误 ===
    ('world/udon/vrc-graphics/index.md', 'world/udon/async-gpu-readback.md'): 'asyncgpureadback.md',

    # === world/udon/midi/midi-playback.md 路径错误 ===
    ('world/udon/midi/midi-playback.md', 'examples/midi-playback.md'): '../../examples/midi-playback.md',

    # === textmeshpro 缺失文件(textmeshpro/tmp_text.md 不存在,需要删除引用)===
    # 这个无法修复,目标文件确实缺失,留待人工处理
}


def fix_related_field_text(rel_path, field_text):
    """修复 related 字段块"""
    for (src, old_t), new_t in FIXES.items():
        if src != rel_path:
            continue
        old_pattern = re.escape(old_t)
        new_field = re.sub(
            rf'^(\s+-\s+)(["\']?){old_pattern}(["\']?)\s*$',
            lambda mm: f'{mm.group(1)}{mm.group(2)}{new_t}{mm.group(3)}',
            field_text,
            flags=re.MULTILINE,
        )
        if new_field != field_text:
            field_text = new_field
    return field_text


def fix_file_dead_links(rel_path):
    """修复单个文件中的死链"""
    fp = MEMORY_ROOT / rel_path
    if not fp.exists():
        return {'file': rel_path, 'status': 'MISSING', 'changes': []}

    content = fp.read_text(encoding='utf-8')
    original = content
    changes = []

    # 1. 修复 related 字段
    def replace_related(m):
        new_text = fix_related_field_text(rel_path, m.group(0))
        if new_text != m.group(0):
            changes.append('related field updated')
        return new_text

    content = re.sub(
        r'^related:\n((?:\s+-\s+.+\n)+)',
        replace_related,
        content,
        flags=re.MULTILINE,
    )

    # 2. 修复 markdown 链接 [text](path)
    for (src, old_t), new_t in FIXES.items():
        if src != rel_path:
            continue
        old_pattern = re.escape(old_t)
        new_content = re.sub(
            rf'\[([^\]]*)\]\({old_pattern}(#[^)]*)?\)',
            lambda m: f'[{m.group(1)}]({new_t}{m.group(2) or ""})',
            content,
        )
        if new_content != content:
            content = new_content
            changes.append(f'markdown: {old_t} -> {new_t}')

    if content != original:
        fp.write_text(content, encoding='utf-8')

    return {
        'file': rel_path,
        'status': 'FIXED' if changes else 'NO_CHANGES',
        'changes': changes,
    }


def main():
    source_files = sorted(set(src for (src, _) in FIXES.keys()))

    print("=" * 80)
    print("A7 死链修复")
    print("=" * 80)
    print(f"修复映射数: {len(FIXES)}")
    print(f"涉及源文件数: {len(source_files)}")
    print()

    results = []
    for rel_path in source_files:
        result = fix_file_dead_links(rel_path)
        results.append(result)
        if result['status'] == 'FIXED':
            print(f"  [FIXED] {rel_path}: {len(result['changes'])} change(s)")
            for c in result['changes'][:3]:
                print(f"    - {c}")
            if len(result['changes']) > 3:
                print(f"    ... and {len(result['changes']) - 3} more")
        else:
            print(f"  [NO_CHANGE] {rel_path}")

    fixed = sum(1 for r in results if r['status'] == 'FIXED')
    print()
    print(f"=" * 80)
    print(f"完成: {fixed}/{len(results)} 文件已修复")
    return 0


if __name__ == '__main__':
    sys.exit(main())
