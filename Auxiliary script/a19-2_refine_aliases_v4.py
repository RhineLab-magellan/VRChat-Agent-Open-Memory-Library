"""A19-2 aliases 精修脚本 v4 - 处理 API: / Pattern: / Domain: 等更多变体"""
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

BACKUP_DIR = CURATOR_TOOLS / 'a19-2_pre_fix_refine_aliases_v4'
REPORT_DIR = CURATOR_TOOLS


def is_prefix_pair(alias1: str, alias2: str) -> Tuple[Optional[str], Optional[str]]:
    """检查是否是 "Prefix: x" 前缀变体对
    返回 (原 alias, 前缀变体 alias) 或 (None, None)
    """
    a, b = str(alias1), str(alias2)
    if ':' in a:
        prefix, rest = a.split(':', 1)
        rest = rest.strip()
        if rest == b.strip() and len(prefix) <= 20:
            return b, a
    if ':' in b:
        prefix, rest = b.split(':', 1)
        rest = rest.strip()
        if rest == a.strip() and len(prefix) <= 20:
            return a, b
    return None, None


def generate_replacement_v4(original: str, category: str, title: str, filename: str) -> Optional[str]:
    """更激进的 alias 生成策略"""
    # 启发式 1:使用 title(去除常见后缀)
    title_clean = title.strip().strip('"').strip("'").strip()
    if title_clean and title_clean != original:
        for suffix in [' — 完整知识库', ' 完整知识库', '— 完整参考', ' 完整参考',
                       ' — Knowledge Base', ' Knowledge Base',
                       ' — 跨领域杂项知识', ' — 总览', ' — 索引',
                       ' — 索引', ' - 索引']:
            if title_clean.endswith(suffix):
                title_clean = title_clean[:-len(suffix)].strip()
                break
        return title_clean

    # 启发式 2:使用 filename
    if filename:
        name_no_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
        if name_no_ext != original and len(name_no_ext) < 50:
            return name_no_ext

    # 启发式 3:对纯中文 original,使用 filename
    if has_chinese(original) and filename:
        name_no_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
        if name_no_ext and not has_chinese(name_no_ext) and name_no_ext != original:
            return name_no_ext

    # 启发式 4:对纯英文 original,加 "VRChat" 前缀
    if not has_chinese(original) and not original.startswith('VRChat'):
        return 'VRChat ' + original

    return None


def refine_aliases(yaml_dict: Dict, filename: str) -> Optional[Dict]:
    """精修 aliases 字段 - v4 更激进"""
    aliases = yaml_dict.get('aliases', [])
    if not isinstance(aliases, list) or len(aliases) != 2:
        return None

    category = yaml_dict.get('category', '')
    title = yaml_dict.get('title', '')

    a_str, b_str = str(aliases[0]), str(aliases[1])
    original, prefix_variant = is_prefix_pair(a_str, b_str)

    if original is None or prefix_variant is None:
        return None

    better = generate_replacement_v4(original, category, title, filename)

    if not better:
        return None

    if better == original or better == prefix_variant:
        return None

    new_aliases = [original, better]
    yaml_dict['aliases'] = new_aliases
    return yaml_dict


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

    new_dict = refine_aliases(yaml_dict, fp.name)
    if new_dict is None:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'cannot refine'}

    new_aliases = new_dict.get('aliases', [])
    if new_aliases == old_aliases:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no change'}

    new_content = rebuild_file(new_dict, fm_text, body)
    if new_content == content:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no effective change'}

    if apply:
        try:
            fp.write_text(new_content, encoding='utf-8')
        except Exception as e:
            return {'file': rel, 'status': 'ERROR', 'note': f'write error: {e}'}
        return {'file': rel, 'status': 'FIXED', 'note': f'{old_aliases} -> {new_aliases}'}
    else:
        return {'file': rel, 'status': 'PENDING', 'note': f'{old_aliases} -> {new_aliases}'}


def main():
    import argparse
    parser = argparse.ArgumentParser(description='A19-2 aliases 精修 v4')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    apply = args.apply
    if not (args.dry_run or args.apply):
        apply = False

    mode = 'apply' if apply else 'dry-run'

    print('=' * 70)
    print(f'A19-2 refine_aliases v4 ({mode})')
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

    md_path, json_path = write_report(REPORT_DIR, 'refine_aliases_v4', summary, details)
    print(f'\n报告: {md_path}')
    print(f'JSON: {json_path}')

    print(f'\n扫描文件: {summary["scanned"]}')
    print(f'需修改: {summary["to_modify"]}')
    print(f'已修改(apply): {summary["modified"]}')
    print(f'无需修改: {summary["no_change"]}')

    pending = [d for d in details if d['status'] in ('FIXED', 'PENDING')]
    if pending:
        print(f'\n待修改样本(全部):')
        for d in pending:
            print(f'  {d["file"]}: {d["note"]}')

    if not apply:
        print('\n*** DRY-RUN 模式 ***')
    return 0


if __name__ == '__main__':
    sys.exit(main())
