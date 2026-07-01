#!/usr/bin/env python3
"""A19-2 精修分析:对比 pre_fix 和当前状态,识别每个文件的修改类型"""
import sys
import re
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fix_common import parse_frontmatter

MEMORY_ROOT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP_ALIASES = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_fix_aliases')
BACKUP_RELATED = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_fix_related')
BACKUP_SHADER = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_refine_shader_source_type')


def read_fm_dict(path):
    """Read frontmatter as a dict using simple parser"""
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        return None
    parsed = parse_frontmatter(text)
    if parsed is None:
        return None
    yaml_dict, _, _ = parsed
    return yaml_dict


def read_text(path):
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return None


def main():
    # Collect all files (set union)
    all_files = set()
    for backup in (BACKUP_ALIASES, BACKUP_RELATED, BACKUP_SHADER):
        for p in backup.rglob('*.md'):
            all_files.add(p.relative_to(backup).as_posix())

    print(f'Total unique files: {len(all_files)}')

    results = []
    for rel in sorted(all_files):
        cur_path = MEMORY_ROOT / rel
        if not cur_path.exists():
            results.append({'file': rel, 'error': 'current file missing'})
            continue

        cur_fm = read_fm_dict(cur_path)
        pre_a = read_fm_dict(BACKUP_ALIASES / rel) if (BACKUP_ALIASES / rel).exists() else None
        pre_r = read_fm_dict(BACKUP_RELATED / rel) if (BACKUP_RELATED / rel).exists() else None
        pre_s = read_fm_dict(BACKUP_SHADER / rel) if (BACKUP_SHADER / rel).exists() else None

        entry = {'file': rel}

        if pre_a:
            cur_aliases = cur_fm.get('aliases', []) if cur_fm else []
            pre_aliases = pre_a.get('aliases', [])
            if cur_aliases == pre_aliases:
                entry['aliases_status'] = 'NO_CHANGE'
            else:
                added_category = []
                for a in cur_aliases:
                    if a not in pre_aliases and re.match(r'^\w+:\s', str(a)):
                        added_category.append(a)
                if added_category and len(cur_aliases) == len(pre_aliases) + 1:
                    entry['aliases_status'] = 'CATEGORY_PREFIX'
                    entry['aliases_added'] = added_category
                else:
                    entry['aliases_status'] = 'OTHER'
                    entry['aliases_old'] = pre_aliases
                    entry['aliases_new'] = cur_aliases

        if pre_r:
            cur_related = cur_fm.get('related', []) if cur_fm else []
            pre_related = pre_r.get('related', [])
            if cur_related == pre_related:
                entry['related_status'] = 'NO_CHANGE'
            else:
                added = [r for r in cur_related if r not in pre_related]
                removed = [r for r in pre_related if r not in cur_related]
                if added or removed:
                    entry['related_status'] = 'CHANGED'
                    entry['related_added'] = added
                    entry['related_removed'] = removed

        if pre_s:
            cur_st = cur_fm.get('source_type', '') if cur_fm else ''
            pre_st = pre_s.get('source_type', '')
            if cur_st == pre_st:
                entry['shader_status'] = 'NO_CHANGE'
            else:
                entry['shader_status'] = 'CHANGED'
                entry['shader_old'] = pre_st
                entry['shader_new'] = cur_st

        results.append(entry)

    # Print summary
    alias_patterns = {}
    related_summary = []
    shader_summary = []
    for r in results:
        if 'aliases_status' in r:
            tag = r['aliases_status']
            alias_patterns[tag] = alias_patterns.get(tag, 0) + 1
        if r.get('related_status') == 'CHANGED':
            related_summary.append(r)
        if r.get('shader_status') == 'CHANGED':
            shader_summary.append(r)

    print('\n=== Aliases patterns ===')
    for k, v in sorted(alias_patterns.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')

    print(f'\n=== Related changes: {len(related_summary)} files ===')

    print(f'\n=== Shader changes: {len(shader_summary)} files ===')
    for r in shader_summary:
        print(f'  {r["file"]}: {r["shader_old"]} -> {r["shader_new"]}')

    # Save full results
    Path('a19-2_refine_analysis.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f'\nFull results: a19-2_refine_analysis.json')


if __name__ == '__main__':
    main()
