#!/usr/bin/env python3
"""
A10-Restore v3: 用 backup body 重建 v1 破坏的文件
====================================================
v1 restore_lost_content.py 错误地将 backup H3 块(含 H2 标题)插入到 current H3 块中
导致 159 个文件出现 986 个重复 H2 标题。

修复策略:
- 检测有 v1 引入 H2 重复的文件(current 有重复, backup 无重复)
- 用 backup 的 body 替换 current 的 body(保留 current 的 YAML frontmatter)
- 这可以一次性清除 v1 引入的所有 H2 重复 + H3 内容丢失
"""
import sys
import re
import shutil
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP = Path('C:/CherryStudio/Agent/UdonSharpAgent/知识库备份/memory v1.0.0/memory')


def split_frontmatter(content):
    """分离 frontmatter 和 body"""
    m = re.match(r'^(---\n.+?\n---\n?)(.*)', content, re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return '', content


def get_h2_titles(content):
    return re.findall(r'^##\s+(.+?)$', content, re.MULTILINE)


def has_v1_h2_dup(cur_h2, bk_h2):
    """检测 v1 引入的 H2 重复: current 有重复且 backup 无重复"""
    cur_dup = {t: c for t, c in Counter(cur_h2).items() if c > 1}
    bk_dup = {t: c for t, c in Counter(bk_h2).items() if c > 1}
    return bool(cur_dup) and not bool(bk_dup)


def main():
    print("=" * 80)
    print("A10-Restore v3: 用 backup body 重建 v1 破坏的文件")
    print("=" * 80)

    # 备份目录
    backup_dir = CURRENT / '_curator_tools' / 'a10_v3_pre_restore'
    backup_dir.mkdir(parents=True, exist_ok=True)

    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    fixed_count = 0
    files_fixed = []
    files_skipped = []

    for cur_fp in all_files:
        rel = cur_fp.relative_to(CURRENT).as_posix()
        bk_fp = BACKUP / rel
        if not bk_fp.exists():
            files_skipped.append((rel, 'no backup'))
            continue

        cur_content = cur_fp.read_text(encoding='utf-8', errors='replace')
        bk_content = bk_fp.read_text(encoding='utf-8', errors='replace')

        cur_h2 = get_h2_titles(cur_content)
        bk_h2 = get_h2_titles(bk_content)

        if not has_v1_h2_dup(cur_h2, bk_h2):
            continue

        # 分离 frontmatter
        cur_fm, _ = split_frontmatter(cur_content)
        _, bk_body = split_frontmatter(bk_content)

        # 用 backup body 重建
        new_content = cur_fm + bk_body

        if new_content == cur_content:
            continue

        # 备份原文件
        shutil.copy2(cur_fp, backup_dir / f"{rel.replace('/', '_')}.bak")

        cur_fp.write_text(new_content, encoding='utf-8')
        fixed_count += 1
        files_fixed.append(rel)

        cur_dup = {t: c for t, c in Counter(cur_h2).items() if c > 1}
        dup_count = sum(c - 1 for c in cur_dup.values())
        print(f"  [FIXED] {rel}: -{dup_count} duplicate H2")

    print()
    print("=" * 80)
    print(f"完成: 修复 {fixed_count} 个 v1 破坏的文件")
    print(f"备份到: {backup_dir}")
    if files_skipped:
        print(f"跳过: {len(files_skipped)} 个文件(无 backup)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
