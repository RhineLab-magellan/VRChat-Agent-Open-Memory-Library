"""A19-2 修复 title 字段错误 + aliases"""
import re
import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _fix_common import (
    SCRIPT_DIR, MEMORY_ROOT, CURATOR_TOOLS,
    iter_markdown_files, parse_frontmatter, rebuild_file,
    backup_files, write_report, has_chinese, setup_console,
)

setup_console()

BACKUP_DIR = CURATOR_TOOLS / 'a19-2_pre_fix_bad_titles'
REPORT_DIR = CURATOR_TOOLS


def fix_bad_titles(yaml_dict: Dict, aliases: List[str], filename: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """检测并修复错误的 title 和 aliases 组合
    返回 (new_yaml_dict, fix_info) 或 (None, None)
    """
    title = yaml_dict.get('title', '').strip().strip('"').strip("'")
    if not title or not isinstance(aliases, list) or len(aliases) != 2:
        return None, None

    a, b = str(aliases[0]), str(aliases[1])

    # 模式 1: title 等于 prefix variant (e.g., title="API: Player API", aliases=['Player API', 'API: Player API'])
    for prefix_variant, original in [(a, b), (b, a)]:
        if ':' in prefix_variant:
            prefix, rest = prefix_variant.split(':', 1)
            rest = rest.strip()
            if rest == original and title == prefix_variant:
                # title 是 prefix variant,应该改为 original
                # 同时 aliases 应该用 filename 替换 prefix_variant
                name_no_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
                if name_no_ext and name_no_ext != original:
                    new_yaml = yaml_dict.copy()
                    new_yaml['title'] = original
                    new_yaml['aliases'] = [original, name_no_ext]
                    return new_yaml, {'title': title, 'new_title': original, 'aliases': aliases, 'new_aliases': [original, name_no_ext]}
                else:
                    new_yaml = yaml_dict.copy()
                    new_yaml['title'] = original
                    new_yaml['aliases'] = [original, prefix_variant]
                    return new_yaml, {'title': title, 'new_title': original, 'aliases': aliases, 'new_aliases': [original, prefix_variant]}

    return None, None


def process_file(fp: Path, apply: bool) -> Dict:
    """处理单个文件"""
    rel = str(fp.relative_to(MEMORY_ROOT)).replace('\\', '/')
    try:
        content = fp.read_text(encoding='utf-8')
    except Exception as e:
        return {'file': rel, 'status': 'ERROR', 'note': f'read error: {e}'}

    parsed = parse_frontmatter(content)
    if not parsed:
        return {'file': rel, 'status': 'SKIP', 'note': 'frontmatter parse failed'}

    yaml_dict, fm_text, body = parsed
    old_aliases = list(yaml_dict.get('aliases', []))
    old_title = yaml_dict.get('title', '')

    new_yaml, fix_info = fix_bad_titles(yaml_dict, old_aliases, fp.name)
    if new_yaml is None:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no fix needed'}

    new_content = rebuild_file(new_yaml, fm_text, body)
    if new_content == content:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no effective change'}

    if apply:
        try:
            fp.write_text(new_content, encoding='utf-8')
        except Exception as e:
            return {'file': rel, 'status': 'ERROR', 'note': f'write error: {e}'}
        return {'file': rel, 'status': 'FIXED', 'note': f'title: {old_title!r} -> {new_yaml.get("title")!r}, aliases: {old_aliases} -> {new_yaml.get("aliases")}'}
    else:
        return {'file': rel, 'status': 'PENDING', 'note': f'title: {old_title!r} -> {new_yaml.get("title")!r}, aliases: {old_aliases} -> {new_yaml.get("aliases")}'}


def main():
    import argparse
    parser = argparse.ArgumentParser(description='A19-2 修复错误 title')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    apply = args.apply
    if not (args.dry_run or args.apply):
        apply = False

    mode = 'apply' if apply else 'dry-run'

    print('=' * 70)
    print(f'A19-2 fix_bad_titles ({mode})')
    print('=' * 70)

    files = iter_markdown_files(MEMORY_ROOT)
    print(f'扫描: {len(files)} 个 .md 文件')

    details = []
    to_modify = []
    for fp in files:
        result = process_file(fp, apply=apply)
        details.append(result)
        if result['status'] in ('FIXED', 'PENDING'):
            to_modify.append(fp)

    if to_modify:
        print(f'\n备份 {len(to_modify)} 个待修改文件到 {BACKUP_DIR}')
        backed_up = backup_files(to_modify, BACKUP_DIR)
    else:
        backed_up = 0

    summary = {
        'mode': mode,
        'scanned': len(files),
        'to_modify': sum(1 for d in details if d['status'] in ('FIXED', 'PENDING')),
        'modified': sum(1 for d in details if d['status'] == 'FIXED'),
        'no_change': sum(1 for d in details if d['status'] == 'NO_CHANGE'),
        'errors': sum(1 for d in details if d['status'] == 'ERROR'),
        'backed_up': backed_up,
    }

    md_path, json_path = write_report(REPORT_DIR, 'fix_bad_titles', summary, details)
    print(f'\n报告: {md_path}')
    print(f'JSON: {json_path}')

    print(f'\n扫描文件: {summary["scanned"]}')
    print(f'需修改: {summary["to_modify"]}')
    print(f'已修改(apply): {summary["modified"]}')
    print(f'无需修改: {summary["no_change"]}')

    pending = [d for d in details if d['status'] in ('FIXED', 'PENDING')]
    if pending:
        print(f'\n修复详情:')
        for d in pending:
            print(f'  {d["file"]}: {d["note"]}')

    if not apply:
        print('\n*** DRY-RUN 模式 ***')
    return 0


if __name__ == '__main__':
    sys.exit(main())
