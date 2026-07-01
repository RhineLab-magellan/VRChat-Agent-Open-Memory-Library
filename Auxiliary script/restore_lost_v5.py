#!/usr/bin/env python3
"""
A10-Restore v5: 用 backup body 重建 backup > current 的文件
==========================================================
这些文件 current 缺内容(backup > current),用 backup body 重建可补齐 H2/H3 缺失。
"""
import sys
import re
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP = Path('C:/CherryStudio/Agent/UdonSharpAgent/知识库备份/memory v1.0.0/memory')


def split_frontmatter(content):
    m = re.match(r'^(---\n.+?\n---\n?)(.*)', content, re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return '', content


def main():
    print("=" * 80)
    print("A10-Restore v5: 用 backup body 重建 backup > current 的文件")
    print("=" * 80)

    backup_dir = CURRENT / '_curator_tools' / 'a10_v5_pre_restore'
    backup_dir.mkdir(parents=True, exist_ok=True)

    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    fixed_count = 0
    files_fixed = []

    for cur_fp in all_files:
        rel = cur_fp.relative_to(CURRENT).as_posix()
        bk_fp = BACKUP / rel
        if not bk_fp.exists():
            continue

        cur_size = len(cur_fp.read_text(encoding='utf-8', errors='replace'))
        bk_size = len(bk_fp.read_text(encoding='utf-8', errors='replace'))

        if bk_size <= cur_size:
            continue

        cur_content = cur_fp.read_text(encoding='utf-8', errors='replace')
        bk_content = bk_fp.read_text(encoding='utf-8', errors='replace')

        cur_fm, _ = split_frontmatter(cur_content)
        _, bk_body = split_frontmatter(bk_content)

        new_content = cur_fm + bk_body

        if new_content == cur_content:
            continue

        # 备份
        shutil.copy2(cur_fp, backup_dir / f"{rel.replace('/', '_')}.bak")
        cur_fp.write_text(new_content, encoding='utf-8')
        fixed_count += 1
        files_fixed.append((rel, cur_size, bk_size))
        print(f"  [FIXED] {rel}: {cur_size} -> {bk_size} (+{bk_size - cur_size})")

    print()
    print("=" * 80)
    print(f"完成: 修复 {fixed_count} 个文件")
    print(f"备份到: {backup_dir}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
