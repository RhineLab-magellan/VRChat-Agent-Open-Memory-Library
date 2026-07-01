#!/usr/bin/env python3
"""
A3+ Tier A 重新迁移脚本
========================
从用户备份恢复的 28 个 Tier A 文件还停留在迁移前状态(带 > Type: 块)。
本脚本只对这 28 个文件重新执行 A3 迁移逻辑。
"""
import sys
from pathlib import Path

# 导入 migration_script 的核心函数
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migration_script import (
    build_frontmatter,
    parse_existing_block,
    MEMORY_ROOT as DEFAULT_MEM_ROOT,
    TODAY,
)

# 28 个 Tier A 文件
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
    'platform/easyquestswitch.md', 'vrchatsdk/01_首页.md',
    'rules/index.md', 'patterns/index.md', 'sources/index.md',
]


def remigrate_file(rel_path: str) -> dict:
    """重新迁移单个文件"""
    filepath = DEFAULT_MEM_ROOT / rel_path
    if not filepath.exists():
        return {'file': rel_path, 'status': 'MISSING'}

    content = filepath.read_text(encoding='utf-8')

    # 如果已经有 YAML frontmatter,跳过
    if content.startswith('---\n'):
        return {'file': rel_path, 'status': 'ALREADY_MIGRATED'}

    # 解析旧的 > 块
    old_block = parse_existing_block(content)
    if old_block is None:
        return {'file': rel_path, 'status': 'NO_OLD_BLOCK'}

    # 构建新 frontmatter
    yaml_text, cleaned_body = build_frontmatter(rel_path, content)

    # 写入新文件(确保 yaml_text 末尾有换行,避免 '---' 粘连 bug)
    new_content = f'---\n{yaml_text}\n---\n{cleaned_body}'
    filepath.write_text(new_content, encoding='utf-8')

    return {
        'file': rel_path,
        'status': 'REMIGRATED',
        'old_size': len(content),
        'new_size': len(new_content),
    }


def main():
    print("=" * 80)
    print("A3+ Tier A 重新迁移")
    print("=" * 80)
    print(f"目标: {len(TIER_A)} 个 Tier A 文件")
    print()

    results = []
    for rel_path in TIER_A:
        result = remigrate_file(rel_path)
        results.append(result)
        status = result['status']
        if status == 'REMIGRATED':
            print(f"  [OK] {rel_path}: {result['old_size']:,} -> {result['new_size']:,} bytes")
        else:
            print(f"  [SKIP/ERR] {rel_path}: {status}")

    remigrated = sum(1 for r in results if r['status'] == 'REMIGRATED')
    skipped = sum(1 for r in results if r['status'] in ('ALREADY_MIGRATED', 'NO_OLD_BLOCK'))
    errored = sum(1 for r in results if r['status'] in ('MISSING',))

    print()
    print(f"=" * 80)
    print(f"完成: {remigrated} 重新迁移, {skipped} 跳过, {errored} 错误")
    return 0


if __name__ == '__main__':
    sys.exit(main())
