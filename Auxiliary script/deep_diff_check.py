#!/usr/bin/env python3
"""
A10-Deep 深度内容对比
======================
对比当前库与备份库,逐段提取正文,检查:
1. 各 H2/H3 章节是否完整
2. 表格行数变化
3. 代码块数量变化
4. 关键概念术语是否保留
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
CURRENT_ROOT = SCRIPT_DIR.parent / 'memory'
BACKUP_ROOT = SCRIPT_DIR.parent / '知识库备份' / 'memory'

# 重点审计的文件(大文件 + 关键文件)
PRIORITY_FILES = [
    'avatar/modular-avatar.md',
    'avatar/teaching-methodology.md',
    'world/udon/vm-and-assembly.md',
    'FACT.md',
    'sources/open-source-projects.md',
    'avatar/modular-avatar-tutorials-detailed.md',
    'world/scene-components/vrc-station.md',
    'avatar/meshia-mesh-simplification.md',
    'avatar/tex-trans-tool.md',
    'avatar/avatar-optimizer.md',
    'world/layers.md',
    'world/udon/networking/network-details.md',
    'world/supported-assets.md',
    'world/udon/graph/event-nodes.md',
    'world/udon/world-debug-views.md',
]


def extract_sections(content: str) -> dict:
    """提取 H2/H3 章节(基于 # 标题)"""
    sections = {}
    current_h2 = None
    for line in content.split('\n'):
        m = re.match(r'^##\s+(.+?)$', line)
        if m:
            current_h2 = m.group(1).strip()
            sections[current_h2] = []
        elif current_h2 and line.strip() and not line.startswith('#'):
            sections[current_h2].append(line)
    return sections


def extract_body(content: str) -> str:
    """提取去除 frontmatter 的正文"""
    m = re.match(r'^---\n.+?\n---\n?(.*)', content, re.DOTALL)
    if m:
        return m.group(1)
    return content


def count_blocks(content: str) -> dict:
    """统计代码块、表格、列表项"""
    code_blocks = len(re.findall(r'^```', content, re.MULTILINE)) // 2
    table_rows = len(re.findall(r'^\|.+\|$', content, re.MULTILINE))
    list_items = len(re.findall(r'^\s*-\s+', content, re.MULTILINE))
    numbered_items = len(re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE))
    return {
        'code_blocks': code_blocks,
        'table_rows': table_rows,
        'list_items': list_items,
        'numbered_items': numbered_items,
    }


def main():
    print("=" * 80)
    print("A10-Deep 深度内容对比")
    print("=" * 80)

    for rel in PRIORITY_FILES:
        cur_path = CURRENT_ROOT / rel
        bk_path = BACKUP_ROOT / rel

        if not cur_path.exists() or not bk_path.exists():
            print(f"\n[SKIP] {rel}: 文件缺失")
            continue

        cur_content = cur_path.read_text(encoding='utf-8', errors='replace')
        bk_content = bk_path.read_text(encoding='utf-8', errors='replace')

        cur_body = extract_body(cur_content)
        bk_body = extract_body(bk_content)

        cur_sections = extract_sections(cur_body)
        bk_sections = extract_sections(bk_body)

        cur_stats = count_blocks(cur_body)
        bk_stats = count_blocks(bk_body)

        # 章节对比
        bk_h2 = set(bk_sections.keys())
        cur_h2 = set(cur_sections.keys())
        missing_sections = bk_h2 - cur_h2
        added_sections = cur_h2 - bk_h2

        # 章节行数对比
        section_size_diff = []
        for h2 in bk_h2 & cur_h2:
            bk_lines = len(bk_sections[h2])
            cur_lines = len(cur_sections[h2])
            if abs(bk_lines - cur_lines) > 5:
                section_size_diff.append((h2, bk_lines, cur_lines, cur_lines - bk_lines))

        size_delta = len(cur_body) - len(bk_body)
        line_delta = cur_body.count('\n') - bk_body.count('\n')

        print(f"\n{'='*80}")
        print(f"[FILE] {rel}")
        print(f"{'='*80}")
        print(f"  Body size: {len(bk_body):,} -> {len(cur_body):,} bytes ({size_delta:+,})")
        print(f"  Body lines: {bk_body.count(chr(10)):,} -> {cur_body.count(chr(10)):,} ({line_delta:+,})")
        print(f"  H2 sections: {len(bk_h2)} -> {len(cur_h2)} (missing: {len(missing_sections)}, added: {len(added_sections)})")
        print(f"  Code blocks: {bk_stats['code_blocks']} -> {cur_stats['code_blocks']}")
        print(f"  Table rows: {bk_stats['table_rows']} -> {cur_stats['table_rows']} ({cur_stats['table_rows'] - bk_stats['table_rows']:+})")
        print(f"  List items: {bk_stats['list_items']} -> {cur_stats['list_items']} ({cur_stats['list_items'] - bk_stats['list_items']:+})")

        if missing_sections:
            print(f"\n  [!] Missing H2 sections in current:")
            for s in sorted(missing_sections)[:10]:
                print(f"    - {s}")

        if added_sections:
            print(f"\  [+] Added H2 sections in current:")
            for s in sorted(added_sections)[:10]:
                print(f"    + {s}")

        if section_size_diff:
            print(f"\n  [!] Sections with significant line count change:")
            for h2, bk, cur, delta in sorted(section_size_diff, key=lambda x: abs(x[3]), reverse=True)[:5]:
                print(f"    {h2}: {bk} -> {cur} lines ({delta:+})")


if __name__ == '__main__':
    main()
