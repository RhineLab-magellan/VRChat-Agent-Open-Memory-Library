#!/usr/bin/env python3
"""
A10-Strip-Legacy: 移除 body 开头的旧引用块
============================================
v3 重建文件时引入了 backup 中的旧引用块(`> Type:` 等),需要清除。
"""
import sys
import re
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CURRENT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')

LEGACY_PATTERNS = [
    r'^>\s*Type:\s*\w',
    r'^>\s*Confidence:\s*\w',
    r'^>\s*Source:\s*.+',
    r'^>\s*Last Updated:\s*\d',
]


def has_legacy_block(content):
    """检查文件是否含有旧引用块(在 body 前 500 字符内)"""
    m = re.match(r'^---\n.+?\n---\n?(.*)', content, re.DOTALL)
    if not m:
        return False
    body = m.group(1)[:500]
    for p in LEGACY_PATTERNS:
        if re.search(p, body, re.MULTILINE):
            return True
    return False


def strip_legacy_block(content):
    """移除 body 开头的旧引用块"""
    m = re.match(r'^(---\n.+?\n---\n?)(.*)', content, re.DOTALL)
    if not m:
        return content
    fm, body = m.group(1), m.group(2)

    # 移除连续的 `> Type:` `> Confidence:` `> Source:` `> Last Updated:` 块
    lines = body.split('\n')
    new_lines = []
    i = 0
    in_legacy = False
    removed_any = False
    while i < len(lines):
        line = lines[i]
        is_legacy = any(re.match(p, line) for p in LEGACY_PATTERNS)
        if is_legacy:
            in_legacy = True
            removed_any = True
            i += 1
            continue
        if in_legacy and not line.strip():
            # 跳过空行
            i += 1
            continue
        if in_legacy and line.strip() and not is_legacy:
            # 退出 legacy 块
            in_legacy = False
        new_lines.append(line)
        i += 1

    if not removed_any:
        return content

    # 确保 body 开头没有多余空行
    new_body = '\n'.join(new_lines)
    new_body = re.sub(r'^\n+', '\n', new_body)
    return fm + new_body


def main():
    print("=" * 80)
    print("A10-Strip-Legacy: 移除 body 开头的旧引用块")
    print("=" * 80)

    backup_dir = CURRENT / '_curator_tools' / 'a10_strip_legacy_pre'
    backup_dir.mkdir(parents=True, exist_ok=True)

    all_files = sorted(CURRENT.rglob('*.md'))
    all_files = [f for f in all_files if '_curator_tools' not in f.parts]

    fixed = 0
    for fp in all_files:
        content = fp.read_text(encoding='utf-8', errors='replace')
        if not has_legacy_block(content):
            continue
        new_content = strip_legacy_block(content)
        if new_content != content:
            shutil.copy2(fp, backup_dir / f"{fp.relative_to(CURRENT).as_posix().replace('/', '_')}.bak")
            fp.write_text(new_content, encoding='utf-8')
            fixed += 1
            print(f"  [STRIPPED] {fp.relative_to(CURRENT).as_posix()}")

    print()
    print("=" * 80)
    print(f"完成: 清理 {fixed} 个文件")
    return 0


if __name__ == '__main__':
    sys.exit(main())
