#!/usr/bin/env python3
"""
A10-Restore v2 修复版内容恢复
=============================
从备份恢复丢失的 H3 章节内容(修复 v1 的 H2 误识别 bug)
"""
import sys
import re
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP = Path('C:/CherryStudio/Agent/UdonSharpAgent/知识库备份/memory v1.0.0/memory')


def is_h2(line):
    """判断是否是 H2 标题(精确匹配)"""
    return bool(re.match(r'^##\s+([^#].+?)$', line))


def is_h3(line):
    """判断是否是 H3 标题(精确匹配)"""
    return bool(re.match(r'^###\s+([^#].+?)$', line))


def parse_title(line):
    """从 H2/H3 行提取标题"""
    m = re.match(r'^#{2,3}\s+(.+?)$', line)
    return m.group(1).strip() if m else None


def extract_h3_body(content):
    """从内容中提取 H3 块字典 {h3_title: (body_lines, parent_h2)}
    body_lines 不含 H3 标题行本身
    """
    lines = content.split('\n')
    blocks = {}  # {h3_title: {'h2': parent_h2, 'body': [lines after H3 title]}}

    current_h2 = None
    current_h3 = None
    current_h3_body = []

    for line in lines:
        if is_h2(line):
            current_h2 = parse_title(line)
        elif is_h3(line):
            if current_h3 is not None:
                blocks[current_h3] = {'h2': current_h2, 'body': current_h3_body}
            current_h3 = parse_title(line)
            current_h3_body = []
        else:
            if current_h3 is not None:
                current_h3_body.append(line)

    if current_h3 is not None:
        blocks[current_h3] = {'h2': current_h2, 'body': current_h3_body}

    return blocks


def count_non_empty(lines):
    return sum(1 for l in lines if l.strip())


def split_frontmatter(content):
    m = re.match(r'^(---\n.+?\n---\n?)(.*)', content, re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return '', content


def restore_file(cur_fp, bk_fp):
    """恢复单个文件: 用 backup 的 H3 body 填充 current 的 H3 body"""
    cur_content = cur_fp.read_text(encoding='utf-8', errors='replace')
    bk_content = bk_fp.read_text(encoding='utf-8', errors='replace')

    cur_fm, cur_body = split_frontmatter(cur_content)
    _, bk_body = split_frontmatter(bk_content)

    cur_blocks = extract_h3_body(cur_body)
    bk_blocks = extract_h3_body(bk_body)

    # 找到需要恢复的 H3 (bk 有内容, cur 少)
    h3_to_restore = []
    for h3, bk_data in bk_blocks.items():
        bk_body_lines = bk_data['body']
        bk_count = count_non_empty(bk_body_lines)
        cur_data = cur_blocks.get(h3)
        cur_count = count_non_empty(cur_data['body']) if cur_data else 0
        if bk_count > 0 and cur_count < bk_count:
            h3_to_restore.append((h3, bk_data))

    if not h3_to_restore:
        return None

    # 重建 body: 用 backup 的 H3 body 替换
    new_body_lines = []
    lines = cur_body.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_h3(line):
            h3_title = parse_title(line)
            # 查找是否需要恢复
            bk_data = None
            for h3, data in h3_to_restore:
                if h3 == h3_title:
                    bk_data = data
                    break

            if bk_data:
                # 添加 H3 标题 + backup 的 body
                new_body_lines.append(line)
                new_body_lines.extend(bk_data['body'])
                i += 1
                # 跳过 current 中此 H3 之后到下一个 H2/H3 之前的内容
                while i < len(lines):
                    if is_h2(lines[i]) or is_h3(lines[i]):
                        break
                    i += 1
                continue
            else:
                new_body_lines.append(line)
                i += 1
        else:
            new_body_lines.append(line)
            i += 1

    new_content = cur_fm + '\n'.join(new_body_lines)
    return new_content


def main():
    print("=" * 80)
    print("A10-Restore v2: 修复 H2 误识别 bug")
    print("=" * 80)

    # 备份到版本化目录
    backup_dir = CURRENT / '_curator_tools' / 'a10_v2_pre_restore'
    backup_dir.mkdir(parents=True, exist_ok=True)

    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    restored_count = 0
    files_modified = []

    for cur_fp in all_files:
        rel = cur_fp.relative_to(CURRENT).as_posix()
        bk_fp = BACKUP / rel
        if not bk_fp.exists():
            continue

        # 用 v1 备份的副本(如果存在)作为输入,避免 v1 错误
        v1_bk = CURRENT / '_curator_tools' / 'a10_pre_restore_backup' / cur_fp.name
        if v1_bk.exists():
            # 用 v1 备份作为输入(其结构是正确的)
            input_fp = v1_bk
        else:
            input_fp = cur_fp

        new_content = restore_file(input_fp, bk_fp)
        if new_content and new_content != input_fp.read_text(encoding='utf-8', errors='replace'):
            # 备份当前文件
            shutil.copy2(cur_fp, backup_dir / f"{rel.replace('/', '_')}.bak")
            cur_fp.write_text(new_content, encoding='utf-8')
            # 统计
            _, old_body = split_frontmatter(input_fp.read_text(encoding='utf-8', errors='replace'))
            _, new_body = split_frontmatter(new_content)
            old_count = count_non_empty(old_body.split('\n'))
            new_count = count_non_empty(new_body.split('\n'))
            restored_count += (new_count - old_count)
            files_modified.append((rel, new_count - old_count))
            print(f"  [RESTORED] {rel}: +{new_count - old_count} 行")

    print()
    print("=" * 80)
    print(f"完成: 恢复 {restored_count} 行内容,修改 {len(files_modified)} 个文件")
    print(f"备份到: {backup_dir}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
