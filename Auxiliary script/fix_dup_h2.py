#!/usr/bin/env python3
"""
A10-Fix-Dup-H2 修复 v1 恢复脚本的 H2 重复 bug
=============================================
v1 restore_lost_content.py 错误地将 H2 标题插入到 H3 块中
结果: 大量文件出现连续重复的 H2 标题

修复策略:
- 检测连续两行相同 H2 标题
- 删除其中一行(优先保留第一行)
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')


def is_h2(line):
    return bool(re.match(r'^##\s+([^#].+?)$', line))


def parse_title(line):
    m = re.match(r'^##\s+(.+?)$', line)
    return m.group(1).strip() if m else None


def fix_dup_h2(content):
    """删除连续重复的 H2 行(允许中间有空行),保留第一行,删除重复行"""
    lines = content.split('\n')
    new_lines = []
    i = 0
    fixed = 0
    while i < len(lines):
        line = lines[i]
        if is_h2(line):
            t1 = parse_title(line)
            new_lines.append(line)  # 保留第一个 H2
            i += 1
            # 向前看,跳过重复(中间可有空行)
            while i < len(lines) and lines[i].strip() == '':
                new_lines.append(lines[i])
                i += 1
            while i < len(lines) and is_h2(lines[i]) and parse_title(lines[i]) == t1:
                # 跳过重复的 H2
                fixed += 1
                i += 1
                # 跳过中间的空行
                while i < len(lines) and lines[i].strip() == '':
                    i += 1
        else:
            new_lines.append(line)
            i += 1
    return '\n'.join(new_lines), fixed


def main():
    print("=" * 80)
    print("A10-Fix-Dup-H2: 修复 v1 恢复脚本的 H2 重复 bug")
    print("=" * 80)

    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    total_fixed = 0
    files_fixed = 0

    for fp in all_files:
        content = fp.read_text(encoding='utf-8')
        new_content, fixed = fix_dup_h2(content)
        if fixed > 0:
            fp.write_text(new_content, encoding='utf-8')
            total_fixed += fixed
            files_fixed += 1
            print(f"  [FIXED] {fp.relative_to(CURRENT).as_posix()}: -{fixed} duplicate H2")

    print()
    print("=" * 80)
    print(f"完成: 修复 {total_fixed} 个重复 H2,涉及 {files_fixed} 个文件")
    return 0


if __name__ == '__main__':
    sys.exit(main())
