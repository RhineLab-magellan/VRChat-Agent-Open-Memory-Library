#!/usr/bin/env python3
"""
A19 修复脚本共享基础库
=====================
提供 frontmatter 解析/重建、文件遍历、备份等公用函数。
"""
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 路径硬编码
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'
CURATOR_TOOLS = MEMORY_ROOT / '_curator_tools'

# 排除目录
EXCLUDE_DIRS = {'_curator_tools', '__pycache__', 'journal'}

# 标量字段顺序
SCALAR_FIELDS = [
    'title', 'category', 'subcategory', 'poiyomi_subdir',
    'knowledge_level', 'status', 'source', 'source_type',
    'version', 'upstream_version', 'last_review', 'confidence',
    'module', 'summary', 'date', 'author',
]

# 列表字段
LIST_FIELDS = ['tags', 'aliases', 'related']


def iter_markdown_files(root: Path = MEMORY_ROOT) -> List[Path]:
    """遍历所有 .md 文件,排除 _curator_tools/journal/__pycache__"""
    result = []
    for fp in root.rglob('*.md'):
        if not any(ex in fp.parts for ex in EXCLUDE_DIRS):
            result.append(fp)
    return sorted(result)


def parse_frontmatter(content: str) -> Optional[Tuple[Dict, str, str]]:
    """
    解析 frontmatter,返回 (yaml_dict, frontmatter_text, body_text)
    失败返回 None
    """
    if not content.startswith('---'):
        return None
    # 找到第二个 ---
    # 注意:文件可能用 \r\n 行尾
    newline = '\n'
    if content.startswith('---\r\n'):
        newline = '\r\n'
        content_after_first = content[5:]
        end_marker = '---' + newline
    elif content.startswith('---\n'):
        content_after_first = content[4:]
        end_marker = '---\n'
    else:
        return None

    end_idx = content_after_first.find(end_marker)
    if end_idx == -1:
        return None

    yaml_text = content_after_first[:end_idx]
    body = content_after_first[end_idx + len(end_marker):]
    yaml_dict = parse_yaml_simple(yaml_text)
    if yaml_dict is None:
        return None
    frontmatter = content[:len(yaml_text) + (4 if newline == '\n' else 5) + len(end_marker)]
    return yaml_dict, frontmatter, body


def parse_yaml_simple(yaml_text: str) -> Optional[Dict]:
    """
    简单 YAML 解析(仅支持本项目使用的 scalar 和 list 顶层结构)
    失败返回 None
    """
    yaml_dict = {}
    current_list_key = None
    current_list = None
    blank_count = 0
    pending_blank = False

    lines = yaml_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # 跳过空行
        if not stripped.strip():
            if current_list_key is not None:
                pending_blank = True
            i += 1
            continue

        # 处理列表项
        if current_list_key is not None and re.match(r'^\s+-\s+', line):
            item_text = re.sub(r'^\s+-\s+', '', stripped)
            item_text = unquote(item_text)
            current_list.append(item_text)
            pending_blank = False
            i += 1
            continue
        elif current_list_key is not None and not re.match(r'^\s', line):
            # 列表结束
            yaml_dict[current_list_key] = current_list
            current_list_key = None
            current_list = None
            pending_blank = False

        # 处理 key: value 或 key:
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', stripped)
        if m:
            key = m.group(1)
            value = m.group(2).strip()
            if value == '':
                # 可能是列表
                current_list_key = key
                current_list = []
            else:
                value = unquote(value)
                yaml_dict[key] = value
            pending_blank = False
            i += 1
            continue

        # 未知行,跳过
        i += 1

    if current_list_key is not None and current_list is not None:
        yaml_dict[current_list_key] = current_list

    return yaml_dict


def unquote(s: str) -> str:
    """去掉包裹的引号(单/双)"""
    s = s.strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return s[1:-1]
    return s


def quote_if_needed(s: str) -> str:
    """如果需要则加引号"""
    if not s:
        return '""'
    # 含空格/冒号/特殊字符则加双引号
    if ' ' in s or ':' in s or '/' in s or '#' in s or ',' in s:
        # 转义双引号
        s = s.replace('"', '\\"')
        return f'"{s}"'
    return s


def build_frontmatter(yaml_dict: Dict) -> str:
    """重建 frontmatter 字符串(完整保留所有字段)"""
    lines = []

    # 标量字段(按预定顺序)
    used_keys = set()
    for key in SCALAR_FIELDS:
        if key in yaml_dict and yaml_dict[key] is not None:
            val = str(yaml_dict[key])
            lines.append(f'{key}: {quote_if_needed(val)}')
            used_keys.add(key)

    # 其他标量字段(未在预定顺序里)
    for key, val in yaml_dict.items():
        if key in used_keys:
            continue
        if key in LIST_FIELDS:
            continue
        if isinstance(val, (list, dict)):
            continue
        lines.append(f'{key}: {quote_if_needed(str(val))}')
        used_keys.add(key)

    # 列表字段
    for key in LIST_FIELDS:
        if key not in yaml_dict:
            continue
        val = yaml_dict[key]
        if not val:
            continue
        if not isinstance(val, list):
            continue
        if not val:
            continue
        lines.append(f'{key}:')
        for item in val:
            lines.append(f'  - {quote_if_needed(str(item))}')

    return '---\n' + '\n'.join(lines) + '\n---\n'


def rebuild_file(yaml_dict: Dict, original_frontmatter: str, body: str) -> str:
    """重建完整文件内容"""
    new_frontmatter = build_frontmatter(yaml_dict)
    return new_frontmatter + body


def backup_files(file_paths: List[Path], backup_dir: Path) -> int:
    """
    备份文件到指定目录。
    保留相对路径结构以避免同名文件覆盖。
    返回实际备份数。
    """
    backup_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for fp in file_paths:
        try:
            # 用相对 MEMORY_ROOT 的路径作为子目录结构
            rel = fp.relative_to(MEMORY_ROOT)
            target = backup_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fp, target)
            count += 1
        except Exception as e:
            print(f'  [BACKUP_FAIL] {fp}: {e}', file=sys.stderr)
    return count


def write_report(report_dir: Path, name: str, summary: Dict, details: List[Dict]) -> Tuple[Path, Path]:
    """
    写报告(.md 和 .json)
    """
    report_dir.mkdir(parents=True, exist_ok=True)
    md_path = report_dir / f'a19-2_{name}_report.md'
    json_path = report_dir / f'a19-2_{name}_report.json'

    # JSON
    import json
    json_data = {
        'summary': summary,
        'details': details,
    }
    json_path.write_text(
        json.dumps(json_data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    # Markdown
    md_lines = [
        f'# A19-2 {name} 报告',
        '',
        '## 摘要',
        '',
        f'- 模式: **{summary.get("mode", "unknown")}**',
        f'- 扫描文件数: {summary.get("scanned", 0)}',
        f'- 需修改文件数: {summary.get("to_modify", 0)}',
        f'- 实际修改文件数: {summary.get("modified", 0)}',
        f'- 跳过(无需修改)文件数: {summary.get("skipped_no_change", 0)}',
        f'- 错误文件数: {summary.get("errors", 0)}',
        f'- 备份文件数: {summary.get("backed_up", 0)}',
        '',
    ]

    if details:
        md_lines.extend([
            '## 详情',
            '',
            '| 文件 | 状态 | 说明 |',
            '|------|------|------|',
        ])
        for d in details[:200]:  # 限制前 200 行
            md_lines.append(f'| `{d.get("file", "")}` | {d.get("status", "")} | {d.get("note", "")} |')
        if len(details) > 200:
            md_lines.append(f'| ... | ... | 共 {len(details)} 条,详见 JSON 报告 |')

    md_path.write_text('\n'.join(md_lines) + '\n', encoding='utf-8')
    return md_path, json_path


def has_chinese(s: str) -> bool:
    """字符串是否含中文字符"""
    return any('\u4e00' <= c <= '\u9fff' for c in s)


def setup_console():
    """配置控制台 UTF-8"""
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass
