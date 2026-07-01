#!/usr/bin/env python3
"""
A10-Compare-Section v2 章节级正文对比(修复路径编码)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 使用字符串绝对路径(直接 UTF-8 字节)
CURRENT_ROOT = Path('C:\\CherryStudio\\Agent\\UdonSharpAgent\\memory')
# 备份目录: 知识库备份/memory v1.0.0/memory
BACKUP_PARENT = Path('C:\\CherryStudio\\Agent\\UdonSharpAgent')
BACKUP_DIR = b'\xe7\x9f\xa5\xe8\xaf\x86\xe5\xba\x93\xe5\xa4\x87\xe4\xbb\xbd'  # 知识库备份
BACKUP_MEMORY = BACKUP_PARENT / BACKUP_DIR.decode('utf-8') / 'memory v1.0.0' / 'memory'

FILES = [
    'world/udon/vm-and-assembly.md',
    'avatar/avatar-optimizer.md',
    'avatar/tex-trans-tool.md',
    'world/udon/world-debug-views.md',
]


def extract_body(content):
    m = re.match(r'^---\n.+?\n---\n?(.*)', content, re.DOTALL)
    return m.group(1) if m else content


def extract_h2_sections(content):
    sections = []
    current_title = None
    current_lines = []
    for line in content.split('\n'):
        m = re.match(r'^##\s+(.+?)$', line)
        if m:
            if current_title is not None:
                sections.append((current_title, '\n'.join(current_lines)))
            current_title = m.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title is not None:
        sections.append((current_title, '\n'.join(current_lines)))
    return sections


def main():
    print(f"CURRENT_ROOT: {CURRENT_ROOT}")
    print(f"BACKUP_MEMORY: {BACKUP_MEMORY}")
    print(f"BACKUP exists: {BACKUP_MEMORY.exists()}")

    for rel in FILES:
        cur_path = CURRENT_ROOT / rel
        bk_path = BACKUP_MEMORY / rel
        if not cur_path.exists() or not bk_path.exists():
            print(f"\n[SKIP] {rel} - current={cur_path.exists()}, backup={bk_path.exists()}")
            continue

        cur_body = extract_body(cur_path.read_text(encoding='utf-8', errors='replace'))
        bk_body = extract_body(bk_path.read_text(encoding='utf-8', errors='replace'))

        cur_sections = extract_h2_sections(cur_body)
        bk_sections = extract_h2_sections(bk_body)

        bk_dict = dict(bk_sections)
        cur_dict = dict(cur_sections)

        print(f"\n{'='*80}")
        print(f"[FILE] {rel}")
        print(f"{'='*80}")

        for title in bk_dict.keys() & cur_dict.keys():
            b = bk_dict[title]
            c = cur_dict[title]
            if abs(len(b) - len(c)) > 200:
                print(f"\n  Section: {title}")
                print(f"  Backup body: {len(b)} bytes")
                print(f"  Current body: {len(c)} bytes")
                print(f"  Delta: {len(c) - len(b):+}")
                print(f"  --- Backup 末尾 3 行 ---")
                for line in b.split('\n')[-3:]:
                    if line.strip():
                        print(f"    | {line[:100]}")
                print(f"  --- Current 末尾 3 行 ---")
                for line in c.split('\n')[-3:]:
                    if line.strip():
                        print(f"    | {line[:100]}")


if __name__ == '__main__':
    main()
