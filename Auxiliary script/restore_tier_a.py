#!/usr/bin/env python3
"""
A6 灾难恢复脚本 v2 - 从用户备份恢复
=====================================
从 C:/CherryStudio/Agent/UdonSharpAgent/知识库备份/memory 恢复 28 个 Tier A 文件
保留本地的 frontmatter(因为 A6 已经更新了 confidence/aliases/related)
"""
import shutil
import sys
from pathlib import Path

BACKUP_ROOT = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\知识库备份\memory')
CURRENT_ROOT = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\memory')

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


def restore_file(rel_path: str) -> dict:
    """从备份恢复单个文件"""
    src = BACKUP_ROOT / rel_path
    dst = CURRENT_ROOT / rel_path

    if not src.exists():
        return {'file': rel_path, 'status': 'MISSING_IN_BACKUP'}

    if not dst.parent.exists():
        return {'file': rel_path, 'status': 'MISSING_DIR_IN_CURRENT'}

    # 直接覆盖(备份是 A3 后的状态,即 frontmatter 完整、body 完整)
    shutil.copy2(src, dst)

    return {
        'file': rel_path,
        'status': 'RESTORED',
        'backup_size': src.stat().st_size,
        'current_size': dst.stat().st_size,
    }


def main():
    print("=" * 80)
    print("A6 灾难恢复 v2:从用户备份恢复 28 个 Tier A 文件")
    print("=" * 80)
    print(f"备份源: {BACKUP_ROOT}")
    print(f"恢复目标: {CURRENT_ROOT}")
    print(f"文件数: {len(TIER_A)}")
    print()

    results = []
    for rel_path in TIER_A:
        result = restore_file(rel_path)
        results.append(result)
        if result['status'] == 'RESTORED':
            print(f"  [OK] {rel_path}: {result['backup_size']:,} -> {result['current_size']:,} bytes")
        else:
            print(f"  [ERR] {rel_path}: {result['status']}")

    ok = sum(1 for r in results if r['status'] == 'RESTORED')
    err = sum(1 for r in results if r['status'] != 'RESTORED')
    print()
    print(f"=" * 80)
    print(f"恢复完成: {ok} 成功, {err} 失败")
    return 0 if err == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
