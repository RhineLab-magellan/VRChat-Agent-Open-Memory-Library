#!/usr/bin/env python3
"""
A19-2 修复脚本: refine_shader_source_type
==========================================
优化 27 个 shader 文件的 `source_type` 标注精度。

映射表(静态):
- avatar/shader/liltoon/*   → official (lilLab GitHub 开源 + VRChat 集成)
- avatar/shader/poiyomi/*   → official (Poiyomi 作者官方)
- avatar/shader/orl/*       → official (orels1 GitHub 官方)
- avatar/shader/filamented/ → community (暂不修改,待确认)
- avatar/shader/unlitwf/    → community (暂不修改,待确认)
- avatar/shader/index.md    → inferred (索引页)
- avatar/shader/other-shaders.md → community
- avatar/shader/scss.md     → community

使用:
    python refine_shader_source_type.py --dry-run   # 默认,只预览
    python refine_shader_source_type.py --apply     # 实际修改
"""
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 确保 _fix_common 可被 import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _fix_common import (
    SCRIPT_DIR, MEMORY_ROOT, CURATOR_TOOLS,
    iter_markdown_files, parse_frontmatter, rebuild_file,
    backup_files, write_report, setup_console,
)

setup_console()

BACKUP_DIR = CURATOR_TOOLS / 'a19-2_pre_fix_refine_shader_source_type'
REPORT_DIR = CURATOR_TOOLS

# shader 静态映射表
# key: 路径前缀或精确路径
# value: (新 source_type, 是否修改)
# 'community' 表示不修改,只是标记(因为 status='community' 即合适)
SHADER_SOURCE_TYPE_MAP: Dict[str, Tuple[str, bool]] = {
    'avatar/shader/liltoon/': ('official', True),
    'avatar/shader/poiyomi/': ('official', True),
    'avatar/shader/orl/': ('official', True),
    'avatar/shader/filamented/': ('community', False),  # 待确认,不修改
    'avatar/shader/unlitwf/': ('community', False),     # 待确认,不修改
    'avatar/shader/index.md': ('inferred', True),      # 索引
    'avatar/shader/other-shaders.md': ('community', True),
    'avatar/shader/scss.md': ('community', True),
}


def resolve_target(rel_path: str) -> Optional[Tuple[str, bool]]:
    """
    解析相对路径到目标值。
    返回 (new_source_type, should_modify)
    """
    # 精确匹配
    if rel_path in SHADER_SOURCE_TYPE_MAP:
        return SHADER_SOURCE_TYPE_MAP[rel_path]

    # 前缀匹配(只对以 / 结尾的键)
    for prefix, (new_value, should_mod) in SHADER_SOURCE_TYPE_MAP.items():
        if prefix.endswith('/') and rel_path.startswith(prefix):
            return (new_value, should_mod)

    return None


def process_file(fp: Path, apply: bool) -> Dict:
    """处理单个文件,返回结果字典"""
    rel = str(fp.relative_to(MEMORY_ROOT)).replace('\\', '/')

    target = resolve_target(rel)
    if target is None:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'not in shader map'}

    new_value, should_mod = target

    try:
        content = fp.read_text(encoding='utf-8')
    except Exception as e:
        return {'file': rel, 'status': 'ERROR', 'note': f'read error: {e}'}

    parsed = parse_frontmatter(content)
    if not parsed:
        return {'file': rel, 'status': 'ERROR', 'note': 'frontmatter parse failed'}

    yaml_dict, fm_text, body = parsed
    current = yaml_dict.get('source_type', '')

    if not should_mod:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': f'marked community (待确认), current={current}'}

    if current == new_value:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': f'source_type already = {new_value}'}

    yaml_dict['source_type'] = new_value
    new_content = rebuild_file(yaml_dict, fm_text, body)

    if new_content == content:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no effective change'}

    if apply:
        try:
            fp.write_text(new_content, encoding='utf-8')
        except Exception as e:
            return {'file': rel, 'status': 'ERROR', 'note': f'write error: {e}'}
        return {'file': rel, 'status': 'FIXED', 'note': f'source_type: {current} -> {new_value}'}
    else:
        return {'file': rel, 'status': 'PENDING', 'note': f'source_type: {current} -> {new_value}'}


def main():
    parser = argparse.ArgumentParser(description='A19-2 优化 shader source_type 标注')
    parser.add_argument('--dry-run', action='store_true', help='只预览不修改(默认)')
    parser.add_argument('--apply', action='store_true', help='实际修改文件')
    args = parser.parse_args()

    apply = args.apply
    if not (args.dry_run or args.apply):
        apply = False

    mode = 'apply' if apply else 'dry-run'

    # 日志
    log_lines = []
    def log(msg=''):
        print(msg)
        log_lines.append(str(msg))

    log('=' * 70)
    log(f'A19-2 refine_shader_source_type.py ({mode})')
    log('=' * 70)

    # 只处理 shader 路径下的文件
    shader_root = MEMORY_ROOT / 'avatar' / 'shader'
    if not shader_root.exists():
        log(f'错误: shader 根目录不存在: {shader_root}')
        return 1

    files = []
    for fp in shader_root.rglob('*.md'):
        # 排除 _curator_tools 等
        if any(ex in fp.parts for ex in ['_curator_tools', '__pycache__', 'journal']):
            continue
        files.append(fp)
    files = sorted(files)

    log(f'扫描 shader 目录: {len(files)} 个 .md 文件')
    log(f'映射表项: {len(SHADER_SOURCE_TYPE_MAP)}')

    details = []
    to_modify = []
    for fp in files:
        result = process_file(fp, apply=apply)
        details.append(result)
        if result['status'] in ('FIXED', 'PENDING'):
            to_modify.append(fp)

    # 备份
    backed_up = 0
    if to_modify:
        log(f'\n备份 {len(to_modify)} 个待修改文件到 {BACKUP_DIR}')
        backed_up = backup_files(to_modify, BACKUP_DIR)

    summary = {
        'mode': mode,
        'scanned': len(files),
        'to_modify': sum(1 for d in details if d['status'] in ('FIXED', 'PENDING')),
        'modified': sum(1 for d in details if d['status'] == 'FIXED'),
        'skipped_no_change': sum(1 for d in details if d['status'] == 'NO_CHANGE'),
        'errors': sum(1 for d in details if d['status'] == 'ERROR'),
        'backed_up': backed_up,
    }

    md_path, json_path = write_report(REPORT_DIR, 'refine_shader_source_type', summary, details)
    log(f'\n报告: {md_path}')
    log(f'JSON: {json_path}')

    # 按映射组统计
    by_target = {}
    for d in details:
        if d['status'] in ('FIXED', 'PENDING'):
            note = d.get('note', '')
            target_val = 'unknown'
            for v in ['official', 'inferred', 'community']:
                if v in note:
                    target_val = v
                    break
            by_target[target_val] = by_target.get(target_val, 0) + 1

    log(f'\n扫描文件: {summary["scanned"]}')
    log(f'需修改: {summary["to_modify"]}')
    log(f'已修改(apply): {summary["modified"]}')
    log(f'待修改(dry-run): {summary["to_modify"] - summary["modified"]}')
    log(f'跳过(无需修改): {summary["skipped_no_change"]}')
    log(f'错误: {summary["errors"]}')
    if by_target:
        log('按目标值分布:')
        for k, v in by_target.items():
            log(f'  - {k}: {v}')

    if not apply:
        log('\n*** DRY-RUN 模式,文件未实际修改 ***')
        log('使用 --apply 参数实际执行修复')

    # 写 dry-run 日志
    log_path = REPORT_DIR / f'a19-2_refine_shader_source_type_{mode}.log'
    log_path.write_text('\n'.join(log_lines), encoding='utf-8')
    print(f'\n日志: {log_path}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
