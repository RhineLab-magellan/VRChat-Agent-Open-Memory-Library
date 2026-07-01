#!/usr/bin/env python3
"""
A19-2 修复脚本: fix_related_v2
=================================
为 123 个 `related` 缺失或 < 3 项的文档补全。

补全策略(基于"同域 + 同子目录 + 共享 tags"启发式):
1. 同子目录优先 (权重 +3)
2. 共享 tags 评分 (按交集数量)
3. 限制: 补到 target_related (默认 5)
4. 排除: 自身、已存在的 related、_curator_tools、journal
5. 路径格式: 相对路径(相对于当前文件)

使用:
    python fix_related_v2.py --dry-run   # 默认,只预览
    python fix_related_v2.py --apply     # 实际修改
"""
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# 确保 _fix_common 可被 import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _fix_common import (
    SCRIPT_DIR, MEMORY_ROOT, CURATOR_TOOLS,
    iter_markdown_files, parse_frontmatter, rebuild_file,
    backup_files, write_report, setup_console,
)

setup_console()

BACKUP_DIR = CURATOR_TOOLS / 'a19-2_pre_fix_fix_related'
REPORT_DIR = CURATOR_TOOLS
TARGET_RELATED = 5
MIN_RELATED = 3


def build_index() -> Dict[Path, Dict]:
    """构建内存索引: file_path -> {yaml_dict, tags, rel_path}"""
    index = {}
    for fp in iter_markdown_files(MEMORY_ROOT):
        try:
            content = fp.read_text(encoding='utf-8')
        except Exception:
            continue
        parsed = parse_frontmatter(content)
        if not parsed:
            continue
        yaml_dict, _, _ = parsed
        tags = yaml_dict.get('tags', [])
        if not isinstance(tags, list):
            tags = []
        rel = str(fp.relative_to(MEMORY_ROOT))
        index[fp] = {
            'yaml': yaml_dict,
            'tags': set(str(t) for t in tags),
            'rel': rel,
            'title': yaml_dict.get('title', ''),
        }
    return index


def compute_rel_path(from_fp: Path, to_fp: Path) -> str:
    """计算 from 相对到 to 的 POSIX 路径"""
    to_fp = Path(to_fp)
    from_fp = Path(from_fp)
    try:
        rel = to_fp.relative_to(from_fp.parent)
    except ValueError:
        # 不在同一父目录,使用 ../ 形式
        try:
            from_parts = from_fp.parent.parts
            to_parts = to_fp.parts
            # 找共同前缀
            common = 0
            for a, b in zip(from_parts, to_parts):
                if a == b:
                    common += 1
                else:
                    break
            ups = len(from_parts) - common
            rel = Path('../' * ups + '/'.join(to_parts[common:]))
        except Exception:
            rel = Path(to_fp.name)
    return rel.as_posix()


def find_related(
    target_fp: Path,
    target_dict: Dict,
    index: Dict[Path, Dict],
    target_count: int = TARGET_RELATED,
) -> List[str]:
    """为目标文件找 related 列表(已规范化为相对路径字符串)"""
    parent_dir = target_fp.parent
    current_tags = index[target_fp]['tags']
    current_related_raw = target_dict.get('related', [])
    if not isinstance(current_related_raw, list):
        current_related_raw = []

    # 规范化已有 related 为绝对路径
    existing_abs: Set[Path] = set()
    for rel in current_related_raw:
        rel_str = str(rel).strip().strip('"').strip("'")
        # 解析为绝对路径
        try:
            abs_path = (parent_dir / rel_str).resolve()
            # 转为相对 MEMORY_ROOT
            try:
                abs_path = abs_path.relative_to(MEMORY_ROOT.resolve())
                existing_abs.add(MEMORY_ROOT / abs_path)
            except ValueError:
                pass
        except Exception:
            pass
    # 也加自身
    existing_abs.add(target_fp)

    # 评分
    candidates = []
    for other_fp, other_info in index.items():
        if other_fp in existing_abs:
            continue
        score = 0
        # 同父目录 +3
        if other_fp.parent == parent_dir:
            score += 3
        # 同祖父目录 +1
        elif other_fp.parent.parent == parent_dir.parent:
            score += 1
        # 共享 tags
        score += len(current_tags & other_info['tags'])
        if score > 0:
            candidates.append((score, other_fp))

    # 排序: 高分优先,同分按字母顺序
    candidates.sort(key=lambda x: (-x[0], str(x[1])))

    # 取前 N
    selected = []
    existing_rel_strs = set(str(r).strip().strip('"').strip("'") for r in current_related_raw)
    for _, other_fp in candidates:
        rel_path = compute_rel_path(target_fp, other_fp)
        # 避免与现有的重复(字符串比较)
        if rel_path in existing_rel_strs:
            continue
        selected.append(rel_path)
        existing_rel_strs.add(rel_path)
        if len(selected) >= target_count - len(current_related_raw):
            break

    return selected


def process_file(fp: Path, index: Dict[Path, Dict], apply: bool) -> Dict:
    """处理单个文件,返回结果字典"""
    rel = str(fp.relative_to(MEMORY_ROOT))
    info = index.get(fp)
    if not info:
        return {'file': rel, 'status': 'ERROR', 'note': 'not in index'}

    yaml_dict = info['yaml'].copy()
    related = list(yaml_dict.get('related', []))
    if not isinstance(related, list):
        related = []

    current_count = len(related)
    if current_count >= MIN_RELATED:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': f'related count = {current_count} (>= {MIN_RELATED})'}

    # 找新 related
    new_related_paths = find_related(fp, yaml_dict, index, TARGET_RELATED)

    if not new_related_paths:
        return {'file': rel, 'status': 'SKIP', 'note': f'related count = {current_count}, no candidates found'}

    # 合并
    final_related = list(related) + new_related_paths
    # 去重
    seen = set()
    deduped = []
    for r in final_related:
        r_str = str(r).strip().strip('"').strip("'")
        if r_str not in seen:
            seen.add(r_str)
            deduped.append(r_str)
    final_related = deduped[:TARGET_RELATED]

    if final_related == related:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no effective change after dedup'}

    # 读 body 以重建文件
    try:
        content = fp.read_text(encoding='utf-8')
    except Exception as e:
        return {'file': rel, 'status': 'ERROR', 'note': f'read error: {e}'}

    parsed = parse_frontmatter(content)
    if not parsed:
        return {'file': rel, 'status': 'ERROR', 'note': 'frontmatter re-parse failed'}

    yaml_full, fm_text, body = parsed
    yaml_full['related'] = final_related
    new_content = rebuild_file(yaml_full, fm_text, body)

    if new_content == content:
        return {'file': rel, 'status': 'NO_CHANGE', 'note': 'no effective change'}

    if apply:
        try:
            fp.write_text(new_content, encoding='utf-8')
        except Exception as e:
            return {'file': rel, 'status': 'ERROR', 'note': f'write error: {e}'}
        return {'file': rel, 'status': 'FIXED', 'note': f'related: {current_count} -> {len(final_related)} items'}
    else:
        return {'file': rel, 'status': 'PENDING', 'note': f'related: {current_count} -> {len(final_related)} items'}


def main():
    parser = argparse.ArgumentParser(description='A19-2 修复 related < 3 项')
    parser.add_argument('--dry-run', action='store_true', help='只预览不修改(默认)')
    parser.add_argument('--apply', action='store_true', help='实际修改文件')
    parser.add_argument('--target', type=int, default=TARGET_RELATED, help=f'目标 related 数 (默认 {TARGET_RELATED})')
    args = parser.parse_args()

    apply = args.apply
    if not (args.dry_run or args.apply):
        apply = False

    mode = 'apply' if apply else 'dry-run'
    target = args.target

    # 日志
    log_lines = []
    def log(msg=''):
        print(msg)
        log_lines.append(str(msg))

    log('=' * 70)
    log(f'A19-2 fix_related_v2.py ({mode}, target={target})')
    log('=' * 70)

    log('构建索引...')
    index = build_index()
    log(f'索引大小: {len(index)} 个文件')

    details = []
    to_modify = []
    for fp in index.keys():
        result = process_file(fp, index, apply=apply)
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
        'target_related': target,
        'scanned': len(index),
        'to_modify': sum(1 for d in details if d['status'] in ('FIXED', 'PENDING')),
        'modified': sum(1 for d in details if d['status'] == 'FIXED'),
        'skipped_no_change': sum(1 for d in details if d['status'] == 'NO_CHANGE'),
        'skipped_no_candidate': sum(1 for d in details if d['status'] == 'SKIP'),
        'errors': sum(1 for d in details if d['status'] == 'ERROR'),
        'backed_up': backed_up,
    }

    md_path, json_path = write_report(REPORT_DIR, 'fix_related', summary, details)
    log(f'\n报告: {md_path}')
    log(f'JSON: {json_path}')

    log(f'\n扫描文件: {summary["scanned"]}')
    log(f'需修改: {summary["to_modify"]}')
    log(f'已修改(apply): {summary["modified"]}')
    log(f'待修改(dry-run): {summary["to_modify"] - summary["modified"]}')
    log(f'跳过(无需修改): {summary["skipped_no_change"]}')
    log(f'跳过(无候选): {summary["skipped_no_candidate"]}')
    log(f'错误: {summary["errors"]}')

    if not apply:
        log('\n*** DRY-RUN 模式,文件未实际修改 ***')
        log('使用 --apply 参数实际执行修复')

    # 写 dry-run 日志
    log_path = REPORT_DIR / f'a19-2_fix_related_{mode}.log'
    log_path.write_text('\n'.join(log_lines), encoding='utf-8')
    print(f'\n日志: {log_path}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
