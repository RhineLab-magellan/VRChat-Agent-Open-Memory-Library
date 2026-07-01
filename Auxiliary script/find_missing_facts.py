#!/usr/bin/env python3
"""
A10-Missing-Facts 关键事实差异检测
==================================
对比关键文档,详细列出丢失的关键事实(标题/代码语言/粗体术语)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
CURRENT_ROOT = SCRIPT_DIR.parent / 'memory'
BACKUP_ROOT = SCRIPT_DIR.parent / '知识库备份' / 'memory'

KEY_FILES = [
    'FACT.md',
    'api/networking.md',
    'avatar/optimization-guide.md',
    'rules/udonsharp-language-limits.md',
    'world/udonsharp-compilation.md',
    'world/vrc-graphics.md',
]


def extract_facts(content: str) -> dict:
    """提取关键事实"""
    titles = set()
    code_langs = set()
    terms = set()
    for m in re.finditer(r'^#{1,6}\s+(.+?)$', content, re.MULTILINE):
        titles.add(m.group(1).strip())
    for m in re.finditer(r'```(\w+)', content):
        code_langs.add(m.group(1).strip())
    for m in re.finditer(r'\*\*([^*\n]{2,50})\*\*', content):
        terms.add(m.group(1).strip())
    return {'titles': titles, 'code_langs': code_langs, 'terms': terms}


def main():
    print("=" * 80)
    print("A10-Missing-Facts 关键事实差异检测")
    print("=" * 80)

    for rel in KEY_FILES:
        cur_path = CURRENT_ROOT / rel
        bk_path = BACKUP_ROOT / rel

        if not cur_path.exists() or not bk_path.exists():
            print(f"\n[SKIP] {rel}")
            continue

        cur = cur_path.read_text(encoding='utf-8', errors='replace')
        bk = bk_path.read_text(encoding='utf-8', errors='replace')

        cur_facts = extract_facts(cur)
        bk_facts = extract_facts(bk)

        print(f"\n{'='*80}")
        print(f"[FILE] {rel}")
        print(f"{'='*80}")

        # 标题差异
        missing_titles = bk_facts['titles'] - cur_facts['titles']
        added_titles = cur_facts['titles'] - bk_facts['titles']
        if missing_titles:
            print(f"\n  [-] Missing titles ({len(missing_titles)}):")
            for t in sorted(missing_titles)[:15]:
                print(f"    - {t}")
            if len(missing_titles) > 15:
                print(f"    ... and {len(missing_titles) - 15} more")
        if added_titles:
            print(f"\n  [+] Added titles ({len(added_titles)}):")
            for t in sorted(added_titles)[:10]:
                print(f"    + {t}")

        # 代码语言差异
        missing_lang = bk_facts['code_langs'] - cur_facts['code_langs']
        if missing_lang:
            print(f"\n  [-] Missing code languages: {sorted(missing_lang)}")

        # 关键术语差异
        missing_terms = bk_facts['terms'] - cur_facts['terms']
        if len(missing_terms) > 5:
            print(f"\n  [-] Missing bold terms (top 20):")
            for t in sorted(missing_terms)[:20]:
                print(f"    - {t}")


if __name__ == '__main__':
    main()
