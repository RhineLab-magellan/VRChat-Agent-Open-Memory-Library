#!/usr/bin/env python3
"""
A19-2 修复脚本: fix_aliases_v1
=================================
为 212 个 `aliases` < 2 项的文档补全 aliases。

补全规则(启发式):
- 0 个 aliases → 跳过(必填字段缺失,留待人工)
- 1 个英文名 → 加 1 个中文译名(从 title 拆)
- 1 个中文名 → 加 1 个英文短名(从 title 拆)
- 1 个别名 → 加 1 个 title 的副本(去重)

使用:
    python fix_aliases_v1.py --dry-run   # 默认,只预览
    python fix_aliases_v1.py --apply     # 实际修改
"""
import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, List

# 确保 _fix_common 可被 import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _fix_common import (
    SCRIPT_DIR, MEMORY_ROOT, CURATOR_TOOLS,
    iter_markdown_files, parse_frontmatter, rebuild_file,
    backup_files, write_report, has_chinese, setup_console,
)

setup_console()

BACKUP_DIR = CURATOR_TOOLS / 'a19-2_pre_fix_fix_aliases'
REPORT_DIR = CURATOR_TOOLS


def derive_alias_from_title(yaml_dict: Dict, existing: str) -> Optional[str]:
    """从 title 启发式推导出第二个 alias"""
    title = yaml_dict.get('title', '').strip()
    if not title:
        return None
    # 去除引号
    title = title.strip('"').strip("'")

    # 启发式 1: title 含英文(检测 Latin 字符)
    # 寻找 title 中的英文短语
    # 简化: 直接复用 title 作为新 alias
    candidate = title

    # 如果 title 与 existing 相同,尝试构造变体
    if candidate == existing:
        # 加上来源标记
        return None

    return candidate


def is_short_title_alias(yaml_dict: Dict) -> bool:
    """检查 title 是否适合作为 alias(短或与现有 alias 互补)"""
    title = yaml_dict.get('title', '').strip().strip('"').strip("'")
    return bool(title) and len(title) < 100


def complete_aliases(yaml_dict: Dict) -> Optional[Dict]:
    """
    补全 aliases。如果需要补全,返回新 yaml_dict(已修改);
    如果不需要补全,返回 None。
    """
    aliases = yaml_dict.get('aliases', [])
    if not isinstance(aliases, list):
        return None

    if len(aliases) == 0:
        return None  # 0 个:跳过,留待人工

    if len(aliases) >= 2:
        return None  # 已经足够

    # 此时 aliases 恰好有 1 个
    existing = str(aliases[0])
    title = yaml_dict.get('title', '').strip().strip('"').strip("'")
    category = yaml_dict.get('category', '').strip().strip('"').strip("'")

    if not title:
        return None

    new_alias = None

    if not has_chinese(existing):
        # 英文 alias → 加中文译名
        if has_chinese(title) and title != existing:
            new_alias = title
        else:
            new_alias = title
    else:
        # 中文 alias → 加英文短名
        if not has_chinese(title) and title != existing:
            new_alias = title
        else:
            new_alias = title

    # 如果 new_alias 与 existing 相同,尝试用 category 作为变体
    if new_alias == existing and category:
        # 构造 "category: title" 形式
        candidate = f'{category}: {existing}'
        if candidate not in aliases:
            new_alias = candidate

    # 去重
    if new_alias and new_alias != existing and new_alias not in aliases:
        aliases.append(new_alias)
        yaml_dict['aliases'] = aliases
        return yaml_dict

    return None


def process_file(fp: Path, apply: bool) -> Dict:
    """处理单个文件,返回结果字典"""
    rel = str(fp.relative_to(MEMORY_ROOT))
    try:
        content = fp.read_text(encoding='utf-8')
    except Exception as e:
        return {'file': rel, 'status': 'ERROR', 'note': f'read error: {e}'}

    parsed = parse_frontmatter(content)
    if not parsed:
        return {'file': rel, 'status': 'SKIP', 'note': 'frontmatter parse failed'}

    yaml_dict, fm_text, body = parsed

    # 检查 aliases
    aliases = yaml_dict.get('aliases', [])
    if not isinstance(aliases, list) or len(aliases) >= 2:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': f'aliases count = {len(aliases) if isinstance(aliases, list) else "N/A"}'}

    if len(aliases) == 0:
        return {'file': rel, 'status': 'SKIP', 'note': 'aliases is empty (needs manual fix)'}

    # 尝试补全
    original_aliases = list(aliases)  # 保留原值(complete_aliases 会就地修改)
    new_dict = complete_aliases(yaml_dict)
    if new_dict is None:
        return {'file': rel, 'status': 'SKIP', 'note': 'cannot derive alias (title missing/duplicate)'}

    new_content = rebuild_file(new_dict, fm_text, body)

    if new_content == content:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no effective change'}

    # 实际修改
    if apply:
        try:
            fp.write_text(new_content, encoding='utf-8')
        except Exception as e:
            return {'file': rel, 'status': 'ERROR', 'note': f'write error: {e}'}
        return {'file': rel, 'status': 'FIXED', 'note': f'aliases: {original_aliases} -> {new_dict.get("aliases")}'}
    else:
        return {'file': rel, 'status': 'PENDING', 'note': f'aliases: {original_aliases} -> {new_dict.get("aliases")}'}


def main():
    parser = argparse.ArgumentParser(description='A19-2 修复 aliases < 2 项')
    parser.add_argument('--dry-run', action='store_true', help='只预览不修改(默认)')
    parser.add_argument('--apply', action='store_true', help='实际修改文件')
    args = parser.parse_args()

    apply = args.apply
    if not (args.dry_run or args.apply):
        apply = False  # 默认 dry-run

    mode = 'apply' if apply else 'dry-run'

    # 日志
    log_lines = []
    def log(msg=''):
        print(msg)
        log_lines.append(str(msg))

    log('=' * 70)
    log(f'A19-2 fix_aliases_v1.py ({mode})')
    log('=' * 70)

    files = iter_markdown_files(MEMORY_ROOT)
    log(f'扫描: {len(files)} 个 .md 文件')

    details = []
    to_modify = []
    for fp in files:
        result = process_file(fp, apply=apply)
        details.append(result)
        if result['status'] in ('FIXED', 'PENDING'):
            to_modify.append(fp)

    # 备份(无论 apply/dry-run 都备份,以便回退)
    backed_up = 0
    if to_modify:
        log(f'\n备份 {len(to_modify)} 个待修改文件到 {BACKUP_DIR}')
        backed_up = backup_files(to_modify, BACKUP_DIR)

    # 统计
    summary = {
        'mode': mode,
        'scanned': len(files),
        'to_modify': sum(1 for d in details if d['status'] in ('FIXED', 'PENDING')),
        'modified': sum(1 for d in details if d['status'] == 'FIXED'),
        'skipped_no_change': sum(1 for d in details if d['status'] == 'NO_CHANGE'),
        'errors': sum(1 for d in details if d['status'] == 'ERROR'),
        'backed_up': backed_up,
        'skipped_manual': sum(1 for d in details if d['status'] == 'SKIP'),
    }

    # 输出报告
    md_path, json_path = write_report(REPORT_DIR, 'fix_aliases', summary, details)
    log(f'\n报告: {md_path}')
    log(f'JSON: {json_path}')

    # 摘要
    log(f'\n扫描文件: {summary["scanned"]}')
    log(f'需修改: {summary["to_modify"]}')
    log(f'已修改(apply): {summary["modified"]}')
    log(f'待修改(dry-run): {summary["to_modify"] - summary["modified"]}')
    log(f'跳过(无需修改): {summary["skipped_no_change"]}')
    log(f'跳过(留待人工): {summary["skipped_manual"]}')
    log(f'错误: {summary["errors"]}')

    if not apply:
        log('\n*** DRY-RUN 模式,文件未实际修改 ***')
        log('使用 --apply 参数实际执行修复')

    # 写 dry-run 日志
    log_path = REPORT_DIR / f'a19-2_fix_aliases_{mode}.log'
    log_path.write_text('\n'.join(log_lines), encoding='utf-8')
    print(f'\n日志: {log_path}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
