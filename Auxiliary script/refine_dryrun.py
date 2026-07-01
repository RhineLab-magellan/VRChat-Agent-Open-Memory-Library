#!/usr/bin/env python3
"""A19-2 精修 dry-run:分析当前状态,识别需要修复的文件(不修改)"""
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

stats = {'A': 0, 'B': 0, 'C': 0, 'errors': 0, 'no_change': 0}
results = []


def read_fm(path):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        return None
    parsed = parse_frontmatter(text)
    if parsed is None:
        return None
    return parsed[0]


def has_chinese(s):
    return bool(s) and any('\u4e00' <= c <= '\u9fff' for c in s)


def make_secondary_alias(fm, file_path=None):
    """Create a meaningful second alias from title (or other fields)."""
    title = str(fm.get('title', '')).strip().strip('"')
    aliases = fm.get('aliases', [])
    # Find an existing clean alias to use as basis
    existing_clean = None
    for a in aliases:
        s = str(a).strip()
        if not re.match(r'^[\w-]+:\s', s):
            existing_clean = s
            break
    if not existing_clean:
        return None
    # Strategy 1: derive from title (different language)
    if has_chinese(title) and not has_chinese(existing_clean):
        return title
    if not has_chinese(title) and has_chinese(existing_clean):
        return title
    # Strategy 2: if title is different, use it
    if title and title != existing_clean and title not in aliases:
        return title
    # Strategy 3: derive a short name from filename
    if file_path:
        stem = file_path.stem
        if stem and stem != existing_clean and stem not in aliases:
            short = stem.replace('-', ' ').replace('_', ' ').strip()
            if short and short not in aliases and short != existing_clean:
                return short
    return None


def normalize_alias(s):
    """Normalize for near-dup detection."""
    s = re.sub(r'[\s\W_]+', '', s.lower())
    return s


def analyze_aliases(fm, current_file_path=None):
    aliases = fm.get('aliases', [])
    if not isinstance(aliases, list):
        return 'A', 'not list', None
    if len(aliases) < 2:
        return 'A', f'len={len(aliases)}', None

    bad_indexes = set()
    # Pattern 1: "category: 旧alias" prefix duplicates
    for i, a in enumerate(aliases):
        s = str(a).strip()
        m = re.match(r'^([\w-]+):\s+(.+)$', s)
        if m:
            rest = m.group(2).strip()
            for j, other in enumerate(aliases):
                if j != i and str(other).strip().lower() == rest.lower():
                    bad_indexes.add(i)
                    break
    # Pattern 2: near-duplicates (ignoring punctuation/whitespace)
    for i in range(len(aliases)):
        ni = normalize_alias(str(aliases[i]))
        for j in range(i+1, len(aliases)):
            nj = normalize_alias(str(aliases[j]))
            if ni == nj:
                bad_indexes.add(j)  # Keep first, mark later as dup

    if not bad_indexes:
        return 'A', 'OK', None
    # B grade: remove bad, add meaningful second
    new_aliases = [a for i, a in enumerate(aliases) if i not in bad_indexes]
    seen = set()
    deduped = []
    for a in new_aliases:
        s = str(a).strip()
        if s and s not in seen:
            seen.add(s)
            deduped.append(a)
    # If we have only 1 alias, add a meaningful second
    if len(deduped) < 2:
        secondary = make_secondary_alias(fm, current_file_path)
        if secondary and secondary not in deduped:
            deduped.append(secondary)
    return 'B', f'bad_dup_count={len(bad_indexes)}: {[aliases[i] for i in sorted(bad_indexes)]}', deduped


def analyze_related(fm, file_path):
    related = fm.get('related', [])
    if not isinstance(related, list):
        return 'A', 'not list', None
    if len(related) < 3:
        return 'A', f'len={len(related)}', None

    my_title = str(fm.get('title', '')).strip().strip('"')
    my_tags = fm.get('tags', []) or []
    if not isinstance(my_tags, list):
        my_tags = []
    my_keywords = set(re.findall(r'[\w\u4e00-\u9fff]+', my_title.lower()))

    # File's directory (for resolving relative paths)
    file_dir = file_path.parent

    bad = []
    for i, ref in enumerate(related):
        ref_clean = str(ref).strip().strip('"').strip("'")
        # Try multiple path resolutions (relative to file first, then absolute)
        candidates = [
            file_dir / ref_clean,
            file_dir.parent / ref_clean,
            MEMORY_ROOT / ref_clean,
        ]
        ref_path = None
        for c in candidates:
            if c.exists():
                ref_path = c
                break
        if ref_path is None:
            bad.append((i, 'dead_link', ref_clean))
            continue
        target_fm = read_fm(ref_path)
        if target_fm is None:
            continue
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
            bad.append((i, 'irrelevant', ref_clean))

    if not bad:
        return 'A', 'OK', None
    new_related = [r for i, r in enumerate(related) if i not in [b[0] for b in bad]]
    if len(new_related) < 3:
        return 'A', f'after filter {len(new_related)}<3 skip', None
    return 'B', f'bad_count={len(bad)}: {[(b[1], b[2]) for b in bad]}', new_related


def analyze_shader(fm, file_path):
    cur = fm.get('source_type', '')
    source = str(fm.get('source', '')).lower()
    subcat = str(fm.get('subcategory', '')).lower()
    path_str = str(file_path).lower()
    # Check if this is a known official shader (liltoon, orels, poiyomi)
    is_liltoon = 'liltoon' in path_str or 'liltoon' in source
    is_orl = 'orl' in path_str or 'orels' in path_str or 'orels1' in source
    is_poiyomi = 'poiyomi' in path_str or 'poiyomi' in source
    is_official_shader = (is_liltoon or is_orl or is_poiyomi) and subcat == 'shader'
    if cur == 'official' and is_official_shader:
        return 'A', f'official {is_liltoon and "liltoon" or is_orl and "orl" or "poiyomi"}', None
    if cur == 'official' and not is_official_shader:
        return 'B', f'st=official but not liltoon/orl/poiyomi (sub={subcat})', None
    return 'A', f'st={cur}', None


def main():
    all_files = set()
    for backup in (BACKUP_ALIASES, BACKUP_RELATED, BACKUP_SHADER):
        for p in backup.rglob('*.md'):
            rel = p.relative_to(backup).as_posix()
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
        cur_path = MEMORY_ROOT / rel
        if not cur_path.exists():
            results.append((rel, ftype, 'C', 'current file missing', None))
            stats['C'] += 1
            continue

        fm = read_fm(cur_path)
        if fm is None:
            results.append((rel, ftype, 'A', 'no frontmatter', None))
            stats['A'] += 1
            continue

        grades = []
        reasons = []
        proposed = {}

        if 'aliases' in ftype:
            g, r, p = analyze_aliases(fm, cur_path)
            grades.append(g)
            reasons.append(f'AL:{r}')
            if p is not None: proposed['aliases'] = p
        if 'related' in ftype:
            g, r, p = analyze_related(fm, cur_path)
            grades.append(g)
            reasons.append(f'REL:{r}')
            if p is not None: proposed['related'] = p
        if 'shader' in ftype:
            g, r, p = analyze_shader(fm, cur_path)
            grades.append(g)
            reasons.append(f'SH:{r}')

        if 'B' in grades:
            stats['B'] += 1
        else:
            stats['A'] += 1

        results.append((rel, ftype, 'B' if 'B' in grades else 'A', '; '.join(reasons), proposed))

    # Stats summary
    print(f'\nStats: {stats}')

    # Show all B files
    b_files = [r for r in results if r[2] == 'B']
    print(f'\nB-graded files: {len(b_files)}')
    for rel, ftype, grade, reason, proposed in b_files[:30]:
        print(f'  {rel} ({ftype}): {reason[:200]}')

    # Save JSON
    out = []
    for rel, ftype, grade, reason, proposed in results:
        out.append({
            'file': rel, 'type': ftype, 'grade': grade,
            'reason': reason, 'proposed': proposed
        })
    Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_refine_dryrun.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(f'\nDry-run report: a19-2_refine_dryrun.json')


if __name__ == '__main__':
    main()
