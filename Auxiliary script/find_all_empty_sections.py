#!/usr/bin/env python3
"""
A10-Critical 关键发现: H3 章节内容丢失检测
============================================
扫描所有 291 文件,找出 backup 有内容但 current 为空的 H3 章节
"""
import sys
import re
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP = Path('C:/CherryStudio/Agent/UdonSharpAgent/知识库备份/memory v1.0.0/memory')


def get_h3_sections(content):
    """返回 [(h3_title, body_text, h2_parent), ...]"""
    lines = content.split('\n')
    sections = []
    current_h2 = None
    current_h3 = None
    current_h3_lines = []
    for line in lines:
        m2 = re.match(r'^##\s+(.+?)$', line)
        m3 = re.match(r'^###\s+(.+?)$', line)
        if m2:
            # Flush current h3
            if current_h3 is not None:
                sections.append((current_h2, current_h3, '\n'.join(current_h3_lines)))
            current_h2 = m2.group(1).strip()
            current_h3 = None
            current_h3_lines = []
        elif m3:
            if current_h3 is not None:
                sections.append((current_h2, current_h3, '\n'.join(current_h3_lines)))
            current_h3 = m3.group(1).strip()
            current_h3_lines = []
        else:
            if current_h3 is not None:
                current_h3_lines.append(line)
    if current_h3 is not None:
        sections.append((current_h2, current_h3, '\n'.join(current_h3_lines)))
    return sections


def main():
    print("=" * 80)
    print("A10-Critical: 扫描所有 291 文件的 H3 章节内容丢失")
    print("=" * 80)

    # 找到所有 .md 文件
    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    total_empty = 0
    total_reduced = 0
    file_issues = []

    for cur_fp in all_files:
        rel = cur_fp.relative_to(CURRENT).as_posix()
        bk_fp = BACKUP / rel
        if not bk_fp.exists():
            continue

        cur_content = cur_fp.read_text(encoding='utf-8', errors='replace')
        bk_content = bk_fp.read_text(encoding='utf-8', errors='replace')

        cur_sections = get_h3_sections(cur_content)
        bk_sections = get_h3_sections(bk_content)

        cur_dict = {(h2, h3): body for h2, h3, body in cur_sections}
        bk_dict = {(h2, h3): body for h2, h3, body in bk_sections}

        # 对比共同章节
        empty_in_cur = []
        reduced_in_cur = []

        for key in bk_dict.keys():
            bk_body = bk_dict[key]
            cur_body = cur_dict.get(key, '')

            bk_non_empty = sum(1 for line in bk_body.split('\n') if line.strip())
            cur_non_empty = sum(1 for line in cur_body.split('\n') if line.strip())

            if bk_non_empty > 0 and cur_non_empty == 0:
                empty_in_cur.append((key, bk_non_empty))
            elif bk_non_empty > cur_non_empty:
                reduced_in_cur.append((key, bk_non_empty, cur_non_empty))

        if empty_in_cur or reduced_in_cur:
            total_empty += len(empty_in_cur)
            total_reduced += len(reduced_in_cur)
            file_issues.append((rel, empty_in_cur, reduced_in_cur))

    print(f"\n扫描完成: {len(all_files)} 文件")
    print(f"完全空白的 H3 章节: {total_empty}")
    print(f"内容减少的 H3 章节: {total_reduced}")
    print(f"涉及文件: {len(file_issues)}")

    # 详细列出前 30 个问题最严重的文件
    print("\n" + "=" * 80)
    print("问题最严重的 30 个文件")
    print("=" * 80)

    file_issues.sort(key=lambda x: -(len(x[1]) * 100 + len(x[2])))

    for rel, empty, reduced in file_issues[:30]:
        print(f"\n[FILE] {rel}")
        if empty:
            print(f"  !!! {len(empty)} 个完全空白 H3 章节:")
            for (h2, h3), bk_count in empty[:5]:
                print(f"    - [{h2 or '(top)'} > {h3}] backup 有 {bk_count} 行, current 为 0")
        if reduced:
            print(f"  ! {len(reduced)} 个内容减少 H3 章节:")
            for (h2, h3), b, c in reduced[:5]:
                print(f"    - [{h2 or '(top)'} > {h3}] backup {b} 行, current {c} 行")

    # 写入报告
    report_path = CURRENT / '_curator_tools' / 'a10_critical_content_loss.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# A10 关键发现: H3 章节内容丢失清单\n\n")
        f.write(f"**生成时间**: 2026-06-21\n")
        f.write(f"**对比基准**: 知识库备份/memory v1.0.0/memory\n\n")
        f.write("## 概览\n\n")
        f.write(f"- 扫描文件: {len(all_files)}\n")
        f.write(f"- 完全空白 H3 章节: {total_empty}\n")
        f.write(f"- 内容减少 H3 章节: {total_reduced}\n")
        f.write(f"- 涉及文件: {len(file_issues)}\n\n")
        f.write("---\n\n")

        f.write("## 详细清单\n\n")
        for rel, empty, reduced in file_issues:
            f.write(f"### `{rel}`\n\n")
            if empty:
                f.write(f"**完全空白 H3 章节 ({len(empty)})**:\n\n")
                for (h2, h3), bk_count in empty:
                    f.write(f"- `[{h2 or '(top)'} > {h3}]` backup 有 {bk_count} 行, current 为 0\n")
                f.write("\n")
            if reduced:
                f.write(f"**内容减少 H3 章节 ({len(reduced)})**:\n\n")
                for (h2, h3), b, c in reduced:
                    delta = b - c
                    f.write(f"- `[{h2 or '(top)'} > {h3}]` backup {b} 行 → current {c} 行 (减少 {delta} 行)\n")
                f.write("\n")

    print(f"\n报告: {report_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
