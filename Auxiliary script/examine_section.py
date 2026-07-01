#!/usr/bin/env python3
"""
A10-Compare-Section 章节级正文对比
==================================
逐章节对比 backup vs current 的实际内容
"""
import re
import sys
from pathlib import Path
import difflib

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
CURRENT_ROOT = SCRIPT_DIR.parent / 'memory'
BACKUP_ROOT = SCRIPT_DIR.parent / '知识库备份' / 'memory'

# 重点审计文件
FILES = [
    'world/udon/vm-and-assembly.md',
    'avatar/avatar-optimizer.md',
    'avatar/tex-trans-tool.md',
    'world/udon/world-debug-views.md',
]


def extract_body(content: str) -> str:
    m = re.match(r'^---\n.+?\n---\n?(.*)', content, re.DOTALL)
    return m.group(1) if m else content


def extract_h2_sections(content: str) -> list:
    """提取 (H2_title, body) 列表"""
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
    for rel in FILES:
        cur_path = CURRENT_ROOT / rel
        bk_path = BACKUP_ROOT / rel
        if not cur_path.exists() or not bk_path.exists():
            continue

        cur_body = extract_body(cur_path.read_text(encoding='utf-8', errors='replace'))
        bk_body = extract_body(bk_path.read_text(encoding='utf-8', errors='replace'))

        cur_sections = extract_h2_sections(cur_body)
        bk_sections = extract_h2_sections(bk_body)

        # 对每个 H2 section 对比
        bk_dict = {title: body for title, body in bk_sections}
        cur_dict = {title: body for title, body in cur_sections}

        print(f"\n{'='*80}")
        print(f"[FILE] {rel}")
        print(f"{'='*80}")

        for title in bk_dict.keys() & cur_dict.keys():
            bk_body_sec = bk_dict[title]
            cur_body_sec = cur_dict[title]
            if abs(len(bk_body_sec) - len(cur_body_sec)) > 100:
                print(f"\n  Section: {title}")
                print(f"  Backup body: {len(bk_body_sec)} bytes")
                print(f"  Current body: {len(cur_body_sec)} bytes")
                print(f"  Delta: {len(cur_body_sec) - len(bk_body_sec):+}")
                print(f"  --- Backup 末尾 5 行 ---")
                for line in bk_body_sec.split('\n')[-5:]:
                    print(f"    | {line[:100]}")
                print(f"  --- Current 末尾 5 行 ---")
                for line in cur_body_sec.split('\n')[-5:]:
                    print(f"    | {line[:100]}")


if __name__ == '__main__':
    main()
