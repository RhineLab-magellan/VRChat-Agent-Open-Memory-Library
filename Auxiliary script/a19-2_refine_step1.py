#!/usr/bin/env python3
"""A19-2 精修:逐个文件评估并修复"""
import sys
import re
import json
import shutil
from pathlib import Path
from typing import Optional, List, Dict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fix_common import parse_frontmatter, rebuild_file

MEMORY_ROOT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
BACKUP_ALIASES = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_fix_aliases')
BACKUP_RELATED = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_fix_related')
BACKUP_SHADER = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_pre_fix_refine_shader_source_type')
REPORT_PATH = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_refine_report.md')

# Counters
stats = {'A': 0, 'B': 0, 'C': 0, 'errors': 0}
results = []  # list of (file, type, grade, reason)


def has_chinese(s):
    return bool(s) and any('\u4e00' <= c <= '\u9fff' for c in s)


def read_fm(path):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        return None, None, None
    parsed = parse_frontmatter(text)
    if parsed is None:
        return None, None, None
    yaml_dict, fm_text, body = parsed
    return yaml_dict, fm_text, body


def write_fm(path, yaml_dict, fm_text, body):
    new_content = rebuild_file(yaml_dict, fm_text, body)
    path.write_text(new_content, encoding='utf-8')


def restore_from_backup(rel, backup_dir, grade, reason):
    """Restore file from backup. Returns True on success."""
    src = backup_dir / rel
    dst = MEMORY_ROOT / rel
    if not src.exists():
        return False
    shutil.copy2(src, dst)
    return True


def grade_aliases(rel, fm, pre_a):
    """Evaluate and possibly fix aliases. Return (grade, reason, modified)."""
    aliases = fm.get('aliases', [])
    if not isinstance(aliases, list):
        return 'A', 'aliases is not a list', False

    if len(aliases) < 2:
        # Less than 2 aliases is the original problem the script tried to fix
        # Don't touch (out of scope of refinement)
        return 'A', f'aliases len={len(aliases)} (out of refinement scope)', False

    # Check for "category: 旧alias" pattern
    bad_indexes = []
    for i, a in enumerate(aliases):
        s = str(a)
        if re.match(r'^[\w-]+:\s', s):  # "word: word" pattern
            # Check if it's a "category: oldalias" pattern
            parts = s.split(':', 1)
            if len(parts) == 2:
                prefix, rest = parts
                rest = rest.strip()
                # If the "rest" portion (without prefix) exists as another alias, this is bad
                for j, other in enumerate(aliases):
                    if j != i and str(other).strip() == rest:
                        bad_indexes.append(i)
                        break

    if not bad_indexes:
        return 'A', 'no category prefix pattern', False

    # B grade: try to fix
    # Strategy: remove the bad "category: x" duplicate, keep the clean one
    new_aliases = [a for i, a in enumerate(aliases) if i not in bad_indexes]
    # Check for duplicates now
    seen = set()
    deduped = []
    for a in new_aliases:
        s = str(a).strip()
        if s and s not in seen:
            seen.add(s)
            deduped.append(a)
    if len(deduped) < 2:
        return 'A', f'only {len(deduped)} aliases after dedup, skip', False

    fm['aliases'] = deduped
    return 'B', f'removed {len(bad_indexes)} category-prefix duplicates: {bad_indexes}', True


def grade_related(rel, fm, pre_r, current_fm):
    """Evaluate and possibly fix related. Return (grade, reason, modified)."""
    related = fm.get('related', [])
    if not isinstance(related, list):
        return 'A', 'related is not a list', False

    if len(related) < 3:
        # Less than 3 was the problem
        return 'A', f'related len={len(related)} (out of refinement scope)', False

    # Check each related file exists and is relevant
    bad_indexes = []
    for i, ref in enumerate(related):
        ref_clean = str(ref).strip().strip('"')
        # Resolve path
        ref_path = MEMORY_ROOT / ref_clean
        if not ref_path.exists():
            bad_indexes.append((i, 'dead_link', ref_clean))
            continue
        # Check relevance: read target frontmatter
        target_fm = read_fm(ref_path)
        if target_fm is None:
            continue
        target_title = target_fm[0].get('title', '').strip().strip('"')
        target_tags = target_fm[0].get('tags', [])
        my_title = current_fm.get('title', '').strip().strip('"')
        my_tags = current_fm.get('tags', [])
        # Compute relevance score
        # Tags overlap
        if isinstance(target_tags, list) and isinstance(my_tags, list):
            tag_overlap = len(set(target_tags) & set(my_tags))
        else:
            tag_overlap = 0
        # Title keyword overlap (simple)
        my_kw = set(re.findall(r'[\w\u4e00-\u9fff]+', my_title.lower()))
        tgt_kw = set(re.findall(r'[\w\u4e00-\u9fff]+', target_title.lower()))
        title_overlap = len(my_kw & tgt_kw)
        if tag_overlap < 1 and title_overlap < 1:
            bad_indexes.append((i, 'irrelevant', f'no overlap with {ref_clean}'))

    if not bad_indexes:
        return 'A', f'all {len(related)} related are relevant', False

    # B grade: remove dead_links and irrelevant
    new_related = [r for i, r in enumerate(related) if i not in [b[0] for b in bad_indexes]]
    if len(new_related) < 3:
        # Don't reduce below 3
        return 'A', f'after filtering {len(new_related)} < 3, skip', False

    current_fm['related'] = new_related
    notes = [f'{b[1]}({b[2]})' for b in bad_indexes]
    return 'B', f'removed {len(bad_indexes)} bad related: {", ".join(notes)}', True


def grade_shader(rel, fm, pre_s):
    """Evaluate shader source_type. Return (grade, reason, modified)."""
    if 'source_type' not in fm:
        return 'A', 'no source_type', False
    cur = fm.get('source_type', '')
    # Check the source URL or name
    source = str(fm.get('source', '')).lower()
    # Official repos for shaders: liltoon (lilxyzw/lilLab), poiyomi (poiyomi/PoiyomiToonShader), orels1 (orels1/orels-Unity-Shader)
    is_official = any(s in source for s in ['lilxyzw', 'liltoon', 'lil lab', 'poiyomi', 'orels1', 'orels'])
    if cur == 'official' and is_official:
        return 'A', 'official source confirmed', False
    if cur == 'official' and not is_official:
        return 'B', f'source={source!r} but source_type=official, check needed', False
    return 'A', f'source_type={cur}', False


def process_file(rel):
    """Process a single file. Returns (grade, reason, modified, file_type)."""
    cur_path = MEMORY_ROOT / rel
    fm, fm_text, body = read_fm(cur_path)
    if fm is None:
        return 'A', 'no frontmatter', False, 'unknown'

    grades = []
    reasons = []
    modified = False
    file_types = []

    # Check aliases
    if (BACKUP_ALIASES / rel).exists():
        pre_a = read_fm(BACKUP_ALIASES / rel)
        g, r, m = grade_aliases(rel, fm, pre_a)
        if g == 'B':
            grades.append('B')
            reasons.append(f'aliases: {r}')
            modified = modified or m
        else:
            grades.append('A')
            reasons.append(f'aliases: {r}')
        file_types.append('aliases')

    # Check related
    if (BACKUP_RELATED / rel).exists():
        pre_r = read_fm(BACKUP_RELATED / rel)
        g, r, m = grade_related(rel, fm, pre_r, fm)
        if g == 'B':
            grades.append('B')
            reasons.append(f'related: {r}')
            modified = modified or m
        else:
            grades.append('A')
            reasons.append(f'related: {r}')
        file_types.append('related')

    # Check shader
    if (BACKUP_SHADER / rel).exists():
        pre_s = read_fm(BACKUP_SHADER / rel)
        g, r, m = grade_shader(rel, fm, pre_s)
        if g == 'B':
            grades.append('B')
            reasons.append(f'shader: {r}')
            modified = modified or m
        else:
            grades.append('A')
            reasons.append(f'shader: {r}')
        file_types.append('shader')

    if not grades:
        return 'A', 'no applicable category', False, ','.join(file_types)

    # Final grade: worst of all
    final = 'A' if 'B' not in grades else 'B'

    if modified:
        write_fm(cur_path, fm, fm_text, body)

    return final, '; '.join(reasons), modified, ','.join(file_types)


def main():
    # Collect all files
    all_files = set()
    for backup in (BACKUP_ALIASES, BACKUP_RELATED, BACKUP_SHADER):
        for p in backup.rglob('*.md'):
            all_files.add(p.relative_to(backup).as_posix())

    print(f'Total files: {len(all_files)}')

    for rel in sorted(all_files):
        try:
            grade, reason, modified, ftype = process_file(rel)
        except Exception as e:
            print(f'ERROR {rel}: {e}')
            grade = 'A'
            reason = f'error: {e}'
            modified = False
            ftype = 'unknown'
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
        reason_short = reason[:200] + ('...' if len(reason) > 200 else '')
        lines.append(f'| `{rel}` | {ftype} | {grade} | {reason_short} |')

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nReport: {REPORT_PATH}')

    # Save JSON
    Path('a19-2_refine_results.json').write_text(
        json.dumps([{'file': r[0], 'type': r[1], 'grade': r[2], 'reason': r[3], 'modified': r[4]} for r in results], ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    print(f'\nFinal stats: {stats}')


if __name__ == '__main__':
    main()
