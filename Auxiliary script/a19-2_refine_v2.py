#!/usr/bin/env python3
"""A19-2 精修 v2:只看当前状态,只处理 297 个被修改过的文件"""
import sys
import re
import json
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fix_common import parse_frontmatter, rebuild_file

MEMORY_ROOT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP_ALIASES = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_fix_aliases')
BACKUP_RELATED = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_fix_related')
BACKUP_SHADER = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_refine_shader_source_type')
REPORT_PATH = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_refine_report.md')

# Counters
stats = {'A': 0, 'B': 0, 'C': 0, 'errors': 0}
results = []


def read_fm(path):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        return None, None, None
    parsed = parse_frontmatter(text)
    if parsed is None:
        return None, None, None
    return parsed


def write_fm(path, yaml_dict, fm_text, body):
    new_content = rebuild_file(yaml_dict, fm_text, body)
    path.write_text(new_content, encoding='utf-8')


def grade_aliases(fm, is_in_aliases_backup):
    """Evaluate aliases. Return (grade, reason, modified)."""
    aliases = fm.get('aliases', [])
    if not isinstance(aliases, list):
        return 'A', 'aliases is not a list', False

    if len(aliases) < 2:
        # Out of scope (script tried to fix these)
        return 'A', f'aliases len={len(aliases)}', False

    # Find bad "category: oldalias" duplicates
    bad_indexes = []
    for i, a in enumerate(aliases):
        s = str(a).strip()
        m = re.match(r'^([\w-]+):\s+(.+)$', s)
        if m:
            prefix, rest = m.group(1).strip(), m.group(2).strip()
            for j, other in enumerate(aliases):
                if j != i and str(other).strip().lower() == rest.lower():
                    bad_indexes.append(i)
                    break

    if not bad_indexes:
        return 'A', f'aliases OK ({len(aliases)} items)', False

    new_aliases = [a for i, a in enumerate(aliases) if i not in bad_indexes]
    seen = set()
    deduped = []
    for a in new_aliases:
        s = str(a).strip()
        if s and s not in seen:
            seen.add(s)
            deduped.append(a)
    if len(deduped) < 2:
        return 'A', f'after dedup {len(deduped)} < 2, skip', False
    fm['aliases'] = deduped
    return 'B', f'removed {len(bad_indexes)} category-prefix dups', True


def grade_related(fm):
    """Evaluate related. Return (grade, reason, modified)."""
    related = fm.get('related', [])
    if not isinstance(related, list):
        return 'A', 'related is not a list', False

    if len(related) < 3:
        return 'A', f'related len={len(related)}', False

    my_title = str(fm.get('title', '')).strip().strip('"')
    my_tags = fm.get('tags', []) or []
    if not isinstance(my_tags, list):
        my_tags = []
    my_keywords = set(re.findall(r'[\w\u4e00-\u9fff]+', my_title.lower()))

    bad_indexes = []
    for i, ref in enumerate(related):
        ref_clean = str(ref).strip().strip('"').strip("'")
        ref_path = MEMORY_ROOT / ref_clean
        if not ref_path.exists():
            bad_indexes.append((i, 'dead_link', ref_clean))
            continue
        target = read_fm(ref_path)
        if target is None:
            continue
        target_fm = target[0]
        target_title = str(target_fm.get('title', '')).strip().strip('"')
        target_tags = target_fm.get('tags', []) or []
        if not isinstance(target_tags, list):
            target_tags = []
        if target_tags and my_tags:
            tag_overlap = len(set(target_tags) & set(my_tags))
        else:
            tag_overlap = 0
        tgt_keywords = set(re.findall(r'[\w\u4e00-\u9fff]+', target_title.lower()))
        title_overlap = len(my_keywords & tgt_keywords)
        if tag_overlap < 1 and title_overlap < 1:
            bad_indexes.append((i, 'irrelevant', f'{ref_clean}'))

    if not bad_indexes:
        return 'A', f'all {len(related)} related relevant', False

    new_related = [r for i, r in enumerate(related) if i not in [b[0] for b in bad_indexes]]
    if len(new_related) < 3:
        return 'A', f'after filtering {len(new_related)} < 3, skip', False
    fm['related'] = new_related
    notes = [f'{b[1]}({b[2]})' for b in bad_indexes]
    return 'B', f'removed {len(bad_indexes)} bad: {"; ".join(notes)}', True


def grade_shader(fm):
    """Evaluate source_type for shader files."""
    cur = fm.get('source_type', '')
    source = str(fm.get('source', '')).lower()
    is_official = any(s in source for s in [
        'lilxyzw', 'liltoon', 'lil lab', 'poiyomi', 'orels1', 'orels'
    ])
    if cur == 'official' and is_official:
        return 'A', 'official confirmed', False
    if cur == 'official' and not is_official:
        return 'B', f'source_type=official but source={source!r}', False
    return 'A', f'source_type={cur}', False


def process_file(rel, ftype):
    """Process a single file. Returns (grade, reason, modified)."""
    cur_path = MEMORY_ROOT / rel
    parsed = read_fm(cur_path)
    if parsed is None:
        return 'A', 'no frontmatter', False

    fm, fm_text, body = parsed
    grades = []
    reasons = []
    modified = False

    if 'aliases' in ftype:
        g, r, m = grade_aliases(fm, True)
        grades.append(g)
        reasons.append(f'AL: {r}')
        modified = modified or m

    if 'related' in ftype:
        g, r, m = grade_related(fm)
        grades.append(g)
        reasons.append(f'REL: {r}')
        modified = modified or m

    if 'shader' in ftype:
        g, r, m = grade_shader(fm)
        grades.append(g)
        reasons.append(f'SH: {r}')

    final = 'B' if 'B' in grades else 'A'

    if modified:
        write_fm(cur_path, fm, fm_text, body)

    return final, '; '.join(reasons), modified


def main():
    # Collect all files (set union)
    all_files = set()
    for backup in (BACKUP_ALIASES, BACKUP_RELATED, BACKUP_SHADER):
        for p in backup.rglob('*.md'):
            rel = p.relative_to(backup).as_posix()
            # Determine type from which backup(s) it's in
            in_a = (BACKUP_ALIASES / rel).exists()
            in_r = (BACKUP_RELATED / rel).exists()
            in_s = (BACKUP_SHADER / rel).exists()
            ftype = ''
            if in_a: ftype += 'aliases,'
            if in_r: ftype += 'related,'
            if in_s: ftype += 'shader,'
            ftype = ftype.rstrip(',')
            all_files.add((rel, ftype))

    print(f'Total files: {len(all_files)}')

    for rel, ftype in sorted(all_files):
        try:
            grade, reason, modified = process_file(rel, ftype)
        except Exception as e:
            print(f'ERROR {rel}: {e}')
            grade = 'A'
            reason = f'error: {e}'
            modified = False
            stats['errors'] += 1
        stats[grade] = stats.get(grade, 0) + 1
        results.append((rel, ftype, grade, reason, modified))
        if grade != 'A':
            print(f'  [{grade}] {rel} ({ftype}): {reason}')

    # Write report
    lines = [
        '# A19-2 精修报告',
        '',
        '## 摘要',
        f'- 总检查文件: {len(all_files)}',
        f'- A 评级(可接受): {stats["A"]}',
        f'- B 评级(已精修): {stats["B"]}',
        f'- C 评级(已还原): {stats["C"]}',
        f'- 错误: {stats["errors"]}',
        f'- 总修改文件数: {sum(1 for r in results if r[4])}',
        '',
        '## 详情',
        '',
        '| 文件 | 类型 | 评级 | 原因/修改 |',
        '|------|------|------|----------|',
    ]
    for rel, ftype, grade, reason, _ in results:
        if grade == 'A':
            continue  # Skip A for brevity
        reason_short = reason[:300] + ('...' if len(reason) > 300 else '')
        lines.append(f'| `{rel}` | {ftype} | {grade} | {reason_short} |')

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nReport: {REPORT_PATH}')

    # Save JSON
    Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_refine_results.json').write_text(
        json.dumps([{'file': r[0], 'type': r[1], 'grade': r[2], 'reason': r[3], 'modified': r[4]} for r in results], ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    print(f'\nFinal stats: {stats}')


if __name__ == '__main__':
    main()
