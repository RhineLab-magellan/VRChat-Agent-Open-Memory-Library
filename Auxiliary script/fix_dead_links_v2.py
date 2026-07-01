#!/usr/bin/env python3
"""
A10-Fix-Dead-Links v2: 修复 backup 原本就有的死链
====================================================
backup v1.0.0 本身就有 22 条死链(主要是路径错误)。
策略: 根据实际文件位置修正路径。
"""
import sys
import re
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')

# 修复映射: (源文件, 旧链接) -> 新链接
FIXES = {
    'avatar/shader/liltoon/audiolink.md': {
        '../advanced-settings.md#距離フェード': './advanced-settings.md#距離フェード',
        '../color-settings.md#発光設定': './color-settings.md#発光設定',
        '../reflection-settings.md#ラメ設定': './reflection-settings.md#ラメ設定',
    },
    'avatar/shader/liltoon/dissolve.md': {
        '../color-settings.md#メインカラー2nd3rd-layer-system': './color-settings.md#メインカラー2nd3rd-layer-system',
        '../color-settings.md#発光設定': './color-settings.md#発光設定',
    },
    'avatar/shader/liltoon/overview.md': {
        '../README.md': './index.md',
    },
    'world/scene-components/vrc-avatarpedestal.md': {
        '../../sdk-prefabs.md': '../sdk-prefabs.md',
    },
    'world/scene-components/vrc-mirrorreflection.md': {
        '../../performance-guide.md': '../performance-guide.md',
        '../../reflection-probes.md': '../reflection-probes.md',
    },
    'world/scene-components/vrc-scenedescriptor.md': {
        '../../layers.md': '../layers.md',
        '../../performance-guide.md': '../performance-guide.md',
    },
    'world/scene-components/vrc-station.md': {
        '../../sdk-prefabs.md': '../sdk-prefabs.md',
        '../../udon/': '../udon/',
    },
    'world/udon/players/player-positions.md': {
        '../networking/network-components/#ondeserialization': '../networking/network-components.md#ondeserialization',
    },
}


def fix_file(rel, fixmap):
    fp = CURRENT / rel
    if not fp.exists():
        return False
    content = fp.read_text(encoding='utf-8', errors='replace')
    new_content = content
    changes = 0
    for old, new in fixmap.items():
        if old in new_content:
            new_content = new_content.replace(old, new)
            changes += 1
    if new_content != content and changes > 0:
        # 备份
        backup_dir = CURRENT / '_curator_tools' / 'a10_dead_links_v2_pre'
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fp, backup_dir / f"{rel.replace('/', '_')}.bak")
        fp.write_text(new_content, encoding='utf-8')
        return True
    return False


def main():
    print("=" * 80)
    print("A10-Fix-Dead-Links v2: 修复 backup 原本就有的死链")
    print("=" * 80)

    total_fixed = 0
    for rel, fixmap in FIXES.items():
        if fix_file(rel, fixmap):
            total_fixed += 1
            print(f"  [FIXED] {rel}: {len(fixmap)} links")

    print()
    print("=" * 80)
    print(f"完成: 修复 {total_fixed} 个文件")
    return 0


if __name__ == '__main__':
    sys.exit(main())
