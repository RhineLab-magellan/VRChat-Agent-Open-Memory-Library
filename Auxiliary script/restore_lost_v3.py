#!/usr/bin/env python3
"""
A10-Restore v4: 用 backup 的 H3 body 恢复 current 的空/减少 H3 块
=============================================================
仅针对 backup 有内容但 current 为空/减少的 H3 块,不影响其他 H3 块。
这适用于 v3 没有完全覆盖的文件(liltoon shader 等)。
"""
import sys
import re
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP = Path('C:/CherryStudio/Agent/UdonSharpAgent/知识库备份/memory v1.0.0/memory')


def is_h2(line):
    return bool(re.match(r'^##\s+([^#].+?)$', line))


def is_h3(line):
    return bool(re.match(r'^###\s+([^#].+?)$', line))


def parse_title(line):
    m = re.match(r'^#{2,3}\s+(.+?)$', line)
    return m.group(1).strip() if m else None


def split_frontmatter(content):
    m = re.match(r'^(---\n.+?\n---\n?)(.*)', content, re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return '', content


def get_h3_blocks_with_positions(content):
    """返回 [(h3_title, start_line_idx, end_line_idx), ...]
    start_line_idx 是 H3 标题行号,end_line_idx 是该 H3 块最后一行(不含下一个 H2/H3)
    """
    lines = content.split('\n')
    blocks = []
    current_h2 = None
    current_h3 = None
    current_h3_start = None
    current_h3_lines = []

    for i, line in enumerate(lines):
        if is_h2(line):
            if current_h3 is not None:
                blocks.append((current_h2, current_h3, current_h3_start, i - 1, current_h3_lines[:]))
            current_h2 = parse_title(line)
            current_h3 = None
            current_h3_start = None
            current_h3_lines = []
        elif is_h3(line):
            if current_h3 is not None:
                blocks.append((current_h2, current_h3, current_h3_start, i - 1, current_h3_lines[:]))
            current_h3 = parse_title(line)
            current_h3_start = i
            current_h3_lines = [line]
        else:
            if current_h3 is not None:
                current_h3_lines.append(line)

    if current_h3 is not None:
        blocks.append((current_h2, current_h3, current_h3_start, len(lines) - 1, current_h3_lines[:]))

    return blocks


def count_non_empty(lines):
    return sum(1 for l in lines if l.strip())


def extract_h3_body_from_backup(bk_content, target_h2, target_h3):
    """从 backup 提取目标 H3 的 body 块(不含 H3 标题行)"""
    blocks = get_h3_blocks_with_positions(bk_content)
    for h2, h3, _, _, block_lines in blocks:
        if h2 == target_h2 and h3 == target_h3:
            # 跳过 H3 标题行,返回 body
            return block_lines[1:]
    return None


def restore_h3_in_file(cur_fp, bk_fp):
    """对单个文件,查找空/减少的 H3 块,用 backup 的对应 H3 body 恢复"""
    cur_content = cur_fp.read_text(encoding='utf-8', errors='replace')
    bk_content = bk_fp.read_text(encoding='utf-8', errors='replace')

    cur_fm, cur_body_str = split_frontmatter(cur_content)

    cur_blocks = get_h3_blocks_with_positions(cur_body_str)
    bk_blocks = get_h3_blocks_with_positions(bk_content)

    bk_dict = {(h2, h3): lines for h2, h3, _, _, lines in bk_blocks}

    # 找到需要恢复的 H3
    to_restore = []
    for h2, h3, start, end, lines in cur_blocks:
        bk_lines = bk_dict.get((h2, h3))
        if bk_lines is None:
            continue
        bk_body = bk_lines[1:]  # 跳过 H3 标题
        cur_h3_body = lines[1:]  # 跳过 H3 标题
        bk_count = count_non_empty(bk_body)
        cur_count = count_non_empty(cur_h3_body)
        if bk_count > 0 and cur_count < bk_count:
            to_restore.append((start, end, h2, h3, bk_body))

    if not to_restore:
        return None

    # 重建 body
    cur_lines = cur_body_str.split('\n')
    # 创建替换映射: (start_line, end_line) -> bk_body
    # 但因为是从后往前替换,避免行号偏移
    new_lines = cur_lines[:]
    for start, end, h2, h3, bk_body in sorted(to_restore, key=lambda x: -x[0]):
        # 替换: new_lines[start+1:end+1] 应该是 bk_body
        new_lines = new_lines[:start + 1] + bk_body + new_lines[end + 1:]

    new_content = cur_fm + '\n'.join(new_lines)
    return new_content


def main():
    print("=" * 80)
    print("A10-Restore v4: 用 backup H3 body 恢复 current 空/减少的 H3 块")
    print("=" * 80)

    backup_dir = CURRENT / '_curator_tools' / 'a10_v4_pre_restore'
    backup_dir.mkdir(parents=True, exist_ok=True)

    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    total_restored = 0
    files_modified = []

    for cur_fp in all_files:
        rel = cur_fp.relative_to(CURRENT).as_posix()
        bk_fp = BACKUP / rel
        if not bk_fp.exists():
            continue

        new_content = restore_h3_in_file(cur_fp, bk_fp)
        if new_content is None:
            continue

        old_content = cur_fp.read_text(encoding='utf-8', errors='replace')
        if new_content == old_content:
            continue

        # 备份
        shutil.copy2(cur_fp, backup_dir / f"{rel.replace('/', '_')}.bak")
        cur_fp.write_text(new_content, encoding='utf-8')
        total_restored += 1
        files_modified.append(rel)
        print(f"  [RESTORED] {rel}")

    print()
    print("=" * 80)
    print(f"完成: 修改 {total_restored} 个文件")
    print(f"备份到: {backup_dir}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
