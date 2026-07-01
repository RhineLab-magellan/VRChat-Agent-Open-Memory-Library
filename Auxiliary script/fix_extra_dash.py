#!/usr/bin/env python3
"""
A3+ 修复脚本 - 移除多余的 line 2 '---'
========================================
remigrate_tier_a.py 错误地在 yaml_text 前加了一次 '---\\n',
而 build_frontmatter 返回的 yaml_text 本身已包含 '---\\n'。
结果: line 1 和 line 2 都是 '---'。

本脚本: 删除 line 2 的多余 '---'。
"""
import sys
from pathlib import Path

MEMORY_ROOT = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\memory')

TIER_A = [
    'FACT.md', 'index.md', '_always-load.md',
    'api/networking.md', 'api/udonsharp-runtime.md', 'api/events-reference.md',
    'api/udon-type-exposure.md', 'api/exposed-types.md', 'api/persistence.md',
    'api/dynamics.md', 'api/pickups.md',
    'world/performance-guide.md', 'world/udonsharp-compilation.md',
    'world/data-containers.md', 'world/vrc-graphics.md',
    'world/vrc-light-volumes.md', 'world/occlusion-culling-guide.md',
    'avatar/optimization-guide.md', 'avatar/playable-layers.md',
    'avatar/performance-rank.md', 'avatar/vrc-constraints.md',
    'hybrid/osc-protocol.md', 'platform/cross-platform-content.md',
    'platform/easyquestswitch.md', 'rules/index.md', 'patterns/index.md', 'sources/index.md',
]


def fix_extra_dash(rel_path: str) -> dict:
    """移除 line 2 的多余 '---'"""
    fp = MEMORY_ROOT / rel_path
    if not fp.exists():
        matches = list(MEMORY_ROOT.rglob(fp.name))
        if matches:
            fp = matches[0]
        else:
            return {'file': rel_path, 'status': 'MISSING'}

    content = fp.read_text(encoding='utf-8')
    lines = content.split('\n')

    if len(lines) < 2 or lines[0].strip() != '---' or lines[1].strip() != '---':
        return {'file': rel_path, 'status': 'NO_EXTRA_DASH'}

    # 移除 line 2
    new_lines = [lines[0]] + lines[2:]
    new_content = '\n'.join(new_lines)
    fp.write_text(new_content, encoding='utf-8')

    return {
        'file': rel_path,
        'status': 'FIXED',
        'old_lines': len(lines),
        'new_lines': len(new_lines),
    }


def main():
    print("=" * 80)
    print("A3+ 修复: 移除 line 2 多余 '---'")
    print("=" * 80)
    print(f"目标: {len(TIER_A)} 个文件")
    print()

    results = []
    for rel_path in TIER_A:
        result = fix_extra_dash(rel_path)
        results.append(result)
        status = result['status']
        if status == 'FIXED':
            print(f"  [OK] {rel_path}: {result['old_lines']} -> {result['new_lines']} lines")
        elif status == 'NO_EXTRA_DASH':
            print(f"  [SKIP] {rel_path}: no extra dash")
        else:
            print(f"  [ERR] {rel_path}: {status}")

    fixed = sum(1 for r in results if r['status'] == 'FIXED')
    skipped = sum(1 for r in results if r['status'] == 'NO_EXTRA_DASH')
    print()
    print(f"=" * 80)
    print(f"完成: {fixed} 修复, {skipped} 跳过")
    return 0


if __name__ == '__main__':
    sys.exit(main())
