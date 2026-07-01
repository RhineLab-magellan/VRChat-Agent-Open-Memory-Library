#!/usr/bin/env python3
"""
A10-Restore 内容恢复脚本
========================
从备份恢复丢失的 H3 章节内容:
1. 扫描 current vs backup
2. 找到完全空白 / 内容减少的 H3 章节
3. 用 backup 的正文替换 current 的对应章节

策略: 保留 current 的 YAML frontmatter,只恢复 H3 章节正文
"""
import sys
import re
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP = Path('C:/CherryStudio/Agent/UdonSharpAgent/知识库备份/memory v1.0.0/memory')


def split_frontmatter_and_body(content):
    """分离 frontmatter 和 body"""
    m = re.match(r'^(---\n.+?\n---\n?)(.*)', content, re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return '', content


def get_h3_blocks(content):
    """将 body 拆分为 [(h3_title_or_none, h3_content_text), ...]
    每个块是 H3 标题到下一个 H3/H2 之间的内容
    """
    lines = content.split('\n')
    blocks = []
    current_h2 = None
    current_h3 = None
    current_h3_lines = []

    # 跟踪每个块的位置
    current_block_start = 0  # 块起始行号

    for i, line in enumerate(lines):
        m2 = re.match(r'^##\s+(.+?)$', line)
        m3 = re.match(r'^###\s+(.+?)$', line)
        if m2:
            # H2 不单独算块,只是记上下文
            current_h2 = m2.group(1).strip()
        if m3:
            # flush previous h3
            if current_h3 is not None or current_h3_lines:
                blocks.append((current_h2, current_h3, current_h3_lines))
            current_h3 = m3.group(1).strip()
            current_h3_lines = [line]
        elif current_h3 is not None:
            # 累积当前 H3 块内容
            current_h3_lines.append(line)

    if current_h3 is not None or current_h3_lines:
        blocks.append((current_h2, current_h3, current_h3_lines))

    return blocks


def restore_h3_content(cur_content, bk_body):
    """恢复 H3 章节内容: 用 backup 的 H3 块替换 current 中对应的空块"""
    cur_fm, cur_body = split_frontmatter_and_body(cur_content)
    bk_blocks = get_h3_blocks(bk_body)

    # 用 backup 的 H3 块重建 current body
    cur_lines = cur_body.split('\n')
    new_lines = []

    # 状态机
    i = 0
    while i < len(cur_lines):
        line = cur_lines[i]
        m3 = re.match(r'^###\s+(.+?)$', line)
        if m3:
            h3_title = m3.group(1).strip()
            # 找到 backup 中匹配的 H3 块
            matching_bk_block = None
            for h2, h3, block_lines in bk_blocks:
                if h3 == h3_title:
                    matching_bk_block = block_lines
                    break

            if matching_bk_block:
                # 用 backup 块替换
                new_lines.extend(matching_bk_block)
                # 跳过 current 中此 H3 之后到下一个 H2/H3 之前的内容
                i += 1
                while i < len(cur_lines):
                    if cur_lines[i].startswith('##'):
                        break
                    i += 1
                continue
            else:
                # backup 中无此 H3,保留原内容
                new_lines.append(line)
                i += 1
        else:
            new_lines.append(line)
            i += 1

    return cur_fm + '\n'.join(new_lines)


def main():
    print("=" * 80)
    print("A10-Restore: 从备份恢复 H3 章节内容")
    print("=" * 80)

    # 备份当前库(以防恢复出错)
    backup_current = CURRENT / '_curator_tools' / 'a10_pre_restore_backup'
    backup_current.mkdir(parents=True, exist_ok=True)
    print(f"\n[STEP 1] 备份当前库到: {backup_current}")
    # 简化:不复制整个库,只记录受影响文件

    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    restored_count = 0
    files_modified = []

    for cur_fp in all_files:
        rel = cur_fp.relative_to(CURRENT).as_posix()
        bk_fp = BACKUP / rel
        if not bk_fp.exists():
            continue

        cur_content = cur_fp.read_text(encoding='utf-8', errors='replace')
        bk_content = bk_fp.read_text(encoding='utf-8', errors='replace')

        cur_fm, cur_body = split_frontmatter_and_body(cur_content)
        bk_fm, bk_body = split_frontmatter_and_body(bk_content)

        # 对比 H3 块
        cur_blocks = get_h3_blocks(cur_body)
        bk_blocks = get_h3_blocks(bk_body)

        cur_dict = {h3: lines for h2, h3, lines in cur_blocks}
        bk_dict = {h3: lines for h2, h3, lines in bk_blocks}

        # 找到需要恢复的 H3 (bk 有内容, cur 空 / 减少)
        h3_to_restore = []
        for h3, bk_lines in bk_dict.items():
            cur_lines = cur_dict.get(h3, [])
            bk_non_empty = sum(1 for l in bk_lines if l.strip() and not l.strip().startswith('###'))
            cur_non_empty = sum(1 for l in cur_lines if l.strip() and not l.strip().startswith('###'))
            if bk_non_empty > 0 and cur_non_empty < bk_non_empty:
                h3_to_restore.append((h3, bk_non_empty, cur_non_empty))

        if not h3_to_restore:
            continue

        # 恢复
        new_content = restore_h3_content(cur_content, bk_body)

        if new_content != cur_content:
            # 备份原文件
            shutil.copy2(cur_fp, backup_current / cur_fp.name)
            # 写入恢复后的内容
            cur_fp.write_text(new_content, encoding='utf-8')
            restored_count += len(h3_to_restore)
            files_modified.append((rel, h3_to_restore))
            print(f"  [RESTORED] {rel}: {len(h3_to_restore)} H3 恢复")

    print()
    print("=" * 80)
    print(f"完成: 恢复 {restored_count} 个 H3 章节,修改 {len(files_modified)} 个文件")
    print(f"原文件备份: {backup_current}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
