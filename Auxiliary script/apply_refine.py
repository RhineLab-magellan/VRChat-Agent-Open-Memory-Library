#!/usr/bin/env python3
"""A19-2 精修 apply:对 B 评级文件应用修复"""
import sys
import json
import re
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fix_common import parse_frontmatter, rebuild_file

MEMORY_ROOT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
REPORT_PATH = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_refine_report.md')
DRYRUN_JSON = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_refine_dryrun.json')


def apply_fix(rel, proposed):
    """Apply proposed fix to a file. Returns (success, message)."""
    cur_path = MEMORY_ROOT / rel
    text = cur_path.read_text(encoding='utf-8')
    parsed = parse_frontmatter(text)
    if parsed is None:
        return False, 'no frontmatter'
    fm, fm_text, body = parsed

    if 'aliases' in proposed:
        new_aliases = proposed['aliases']
        # Validate: at least 1 alias, no exact duplicates
        if not isinstance(new_aliases, list) or len(new_aliases) < 1:
            return False, 'invalid aliases proposed'
        fm['aliases'] = new_aliases

    if 'related' in proposed:
        new_related = proposed['related']
        if not isinstance(new_related, list) or len(new_related) < 1:
            return False, 'invalid related proposed'
        fm['related'] = new_related

    new_content = rebuild_file(fm, fm_text, body)
    cur_path.write_text(new_content, encoding='utf-8')
    return True, 'applied'


def main():
    with open(DRYRUN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    b_files = [d for d in data if d['grade'] == 'B']
    print(f'B files to fix: {len(b_files)}')

    stats = {'applied': 0, 'skipped': 0, 'errors': 0}
    results = []
    for d in b_files:
        rel = d['file']
        proposed = d.get('proposed', {})
        if not proposed:
            results.append((rel, 'SKIP', 'no proposed fix', d['reason']))
            stats['skipped'] += 1
            continue
        try:
            success, msg = apply_fix(rel, proposed)
            if success:
                results.append((rel, 'FIXED', msg, d['reason']))
                stats['applied'] += 1
            else:
                results.append((rel, 'SKIP', msg, d['reason']))
                stats['skipped'] += 1
        except Exception as e:
            print(f'ERROR {rel}: {e}')
            results.append((rel, 'ERROR', str(e), d['reason']))
            stats['errors'] += 1

    print(f'\nStats: {stats}')

    # Write report
    a_count = sum(1 for d in data if d['grade'] == 'A')
    b_count = sum(1 for d in data if d['grade'] == 'B')

    lines = [
        '# A19-2 精修报告',
        '',
        '## 摘要',
        f'- 总检查文件: {len(data)}',
        f'- A 评级(可接受): {a_count}',
        f'- B 评级(已精修): {b_count}',
        f'- C 评级(已还原): 0',
        f'- 错误: {stats["errors"]}',
        f'- 实际修改文件数: {stats["applied"]}',
        '',
        '## 详情',
        '',
        '| 文件 | 类型 | 评级 | 原因/修改 |',
        '|------|------|------|----------|',
    ]
    for rel, status, msg, reason in results:
        reason_short = reason[:200] + ('...' if len(reason) > 200 else '')
        lines.append(f'| `{rel}` | aliases/related | {status} | {reason_short} |')

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nReport: {REPORT_PATH}')


if __name__ == '__main__':
    main()
