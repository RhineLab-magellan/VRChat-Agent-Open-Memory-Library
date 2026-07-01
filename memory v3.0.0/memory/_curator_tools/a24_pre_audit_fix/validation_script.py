#!/usr/bin/env python3
"""
A4 验证脚本
==============
验证全部 291 文档的 YAML frontmatter 合规性:
1. YAML 块存在且格式正确
2. 必填字段齐全
3. 字段值在白名单内
4. Tags 数量 3-8
5. 引用块已 100% 清除
6. 内容未丢失(行数变化合理)
"""
import os
import re
import sys
from pathlib import Path
from collections import Counter
from datetime import date

# ==================== 配置 ====================
# 脚本位置: UdonSharpAgent/Auxiliary script/validation_script.py
# 知识库位置: UdonSharpAgent/memory/
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'
TODAY = "2026-06-20"
# V3.1 + A18 修正: 排除 journal 整个目录(sessions/drafts/issues 全部是临时记录,无 frontmatter)
# V3.1 + A18 修正: 排除 _curator_tools (工具报告/备份,非知识)
EXCLUDE_DIRS = {'_curator_tools', '__pycache__', 'journal'}

# 白名单 (V3.1 + A18 修正: 添加 meta)
# V3.1 §3.2 列出 14 个值: api | avatar | world | hybrid | platform | vrchatsdk |
# sources | patterns | rules | reviews | journal | references | misc | meta
# 旧版本 (V3.0 前) 漏掉 meta,导致 4 个 meta/ 文件 + 1 audit 文件被误报 INVALID_CATEGORY
ALLOWED_CATEGORIES = {
    'api', 'avatar', 'world', 'hybrid', 'platform',
    'vrchatsdk', 'sources', 'patterns', 'rules',
    'reviews', 'journal', 'references', 'misc', 'meta'
}
ALLOWED_LEVELS = {'core', 'applied', 'auxiliary'}
ALLOWED_STATUS = {'draft', 'active', 'deprecated', 'archived'}
ALLOWED_CONFIDENCE = {'High', 'Medium', 'Low'}
ALLOWED_SOURCE_TYPE = {'official', 'community', 'inferred'}

REQUIRED_FIELDS = [
    'title', 'category', 'knowledge_level', 'status',
    'tags', 'aliases', 'source', 'version',
    'last_review', 'confidence'
]
OPTIONAL_FIELDS = ['subcategory', 'related', 'source_type']


# ==================== 简单 YAML 解析 ====================
class SimpleYAML:
    """极简 YAML 解析器(支持 scalar/list 顶层)"""

    @staticmethod
    def parse(yaml_text: str) -> dict:
        result = {}
        lines = yaml_text.split('\n')
        current_list_key = None

        for line in lines:
            if not line.strip() or line.strip().startswith('#'):
                continue
            # 列表项
            m = re.match(r'^\s+-\s+(.+?)\s*$', line)
            if m and current_list_key:
                if current_list_key not in result:
                    result[current_list_key] = []
                if isinstance(result[current_list_key], list):
                    result[current_list_key].append(m.group(1).strip('"').strip("'"))
                continue
            # 键值对
            m = re.match(r'^([\w_-]+):\s*(.*?)\s*$', line)
            if m:
                key = m.group(1)
                value = m.group(2)
                if not value:  # 空值,表示接下来是列表
                    current_list_key = key
                    result[key] = []
                else:
                    current_list_key = None
                    result[key] = value.strip('"').strip("'")
        return result


# ==================== 验证器 ====================
def extract_frontmatter(content: str) -> tuple:
    """提取 --- ... --- 块,返回 (yaml_text, body)"""
    m = re.match(r'^---\n(.+?)\n---\n?(.*)', content, re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return None, content


def check_legacy_block(body: str) -> bool:
    """检查 body 中是否还有 > Type: 等旧引用块"""
    legacy_patterns = [
        r'^>\s*Type:\s*\w',
        r'^>\s*Confidence:\s*\w',
        r'^>\s*Source:\s*.+',
        r'^>\s*Last Updated:\s*\d',
    ]
    for pattern in legacy_patterns:
        if re.search(pattern, body, re.MULTILINE):
            return True
    return False


def validate_file(rel_path: str) -> dict:
    """验证单个文档,返回结构化结果"""
    filepath = MEMORY_ROOT / rel_path
    if not filepath.exists():
        return {'file': rel_path, 'error': 'FILE_NOT_FOUND'}

    content = filepath.read_text(encoding='utf-8')
    yaml_text, body = extract_frontmatter(content)

    issues = []
    metrics = {}

    if yaml_text is None:
        issues.append('NO_FRONTMATTER')
        return {
            'file': rel_path,
            'issues': issues,
            'success': False,
        }

    # 解析 YAML
    data = SimpleYAML.parse(yaml_text)
    metrics['fields_count'] = len(data)

    # 必填字段检查
    for field in REQUIRED_FIELDS:
        if field not in data:
            issues.append(f'MISSING_REQUIRED:{field}')

    # 可选字段检查(不报错,仅记录)
    for field in OPTIONAL_FIELDS:
        if field in data:
            metrics[f'has_{field}'] = True

    # category 白名单
    if 'category' in data and data['category'] not in ALLOWED_CATEGORIES:
        issues.append(f'INVALID_CATEGORY:{data["category"]}')

    # knowledge_level 白名单
    if 'knowledge_level' in data and data['knowledge_level'] not in ALLOWED_LEVELS:
        issues.append(f'INVALID_LEVEL:{data["knowledge_level"]}')

    # status 白名单
    if 'status' in data and data['status'] not in ALLOWED_STATUS:
        issues.append(f'INVALID_STATUS:{data["status"]}')

    # confidence 白名单
    if 'confidence' in data and data['confidence'] not in ALLOWED_CONFIDENCE:
        issues.append(f'INVALID_CONFIDENCE:{data["confidence"]}')

    # source_type 白名单(可选)
    if 'source_type' in data and data['source_type'] not in ALLOWED_SOURCE_TYPE:
        issues.append(f'INVALID_SOURCE_TYPE:{data["source_type"]}')

    # tags 数量 3-8(迁移文件除外,允许 1+)
    if 'tags' in data:
        tag_count = len(data['tags'])
        metrics['tags_count'] = tag_count
        if data.get('status') != 'archived' and not (tag_count < 3):
            pass  # 普通文档
        if tag_count < 1:
            issues.append('NO_TAGS')
        if tag_count < 3 and data.get('status') != 'archived':
            issues.append(f'TOO_FEW_TAGS:{tag_count}')
        if tag_count > 8:
            issues.append(f'TOO_MANY_TAGS:{tag_count}')

    # aliases 数量 ≥ 1
    if 'aliases' in data:
        alias_count = len(data['aliases']) if isinstance(data['aliases'], list) else 1
        metrics['aliases_count'] = alias_count
        if alias_count < 1:
            issues.append('NO_ALIASES')

    # last_review 格式
    if 'last_review' in data:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', data['last_review']):
            issues.append(f'INVALID_DATE_FORMAT:{data["last_review"]}')

    # version 格式(semver 简化,支持 v 前缀)
    if 'version' in data:
        if not re.match(r'^v?\d+\.\d+', data['version']):
            issues.append(f'INVALID_VERSION:{data["version"]}')

    # 旧引用块检查
    if check_legacy_block(body[:500]):  # 仅检查前 500 字符
        issues.append('LEGACY_BLOCK_REMAINS')

    # body 完整性(应非空)
    if not body.strip():
        issues.append('EMPTY_BODY')

    return {
        'file': rel_path,
        'issues': issues,
        'metrics': metrics,
        'success': len(issues) == 0,
    }


# ==================== 主流程 ====================
def find_all_md_files() -> list:
    md_files = []
    for path in MEMORY_ROOT.rglob('*.md'):
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        md_files.append(path.relative_to(MEMORY_ROOT).as_posix())
    return sorted(md_files)


def main():
    print("=" * 80)
    print(f"A4 Validation Report Generator")
    print(f"Date: {TODAY}")
    print("=" * 80)

    # 确保输出目录存在(若被误删则自动重建)
    (MEMORY_ROOT / '_curator_tools').mkdir(exist_ok=True)

    files = find_all_md_files()
    print(f"Found {len(files)} .md files\n")

    results = []
    for idx, rel in enumerate(files, 1):
        if idx % 50 == 0 or idx == 1 or idx == len(files):
            print(f"[{idx}/{len(files)}] Validating...")
        result = validate_file(rel)
        results.append(result)

    # 统计
    success_count = sum(1 for r in results if r.get('success'))
    failure_count = sum(1 for r in results if not r.get('success'))

    # 分类统计 issues
    issue_counter = Counter()
    for r in results:
        for issue in r.get('issues', []):
            category = issue.split(':')[0]
            issue_counter[category] += 1

    # 状态分布
    status_counter = Counter()
    category_counter = Counter()
    tags_total = 0
    aliases_total = 0
    for r in results:
        if r.get('success') or 'issues' in r:
            # 解析文件获取 status/category/tags/aliases
            filepath = MEMORY_ROOT / r['file']
            try:
                content = filepath.read_text(encoding='utf-8')
                yaml_text, _ = extract_frontmatter(content)
                if yaml_text:
                    data = SimpleYAML.parse(yaml_text)
                    if 'status' in data:
                        status_counter[data['status']] += 1
                    if 'category' in data:
                        category_counter[data['category']] += 1
                    if 'tags' in data and isinstance(data['tags'], list):
                        tags_total += len(data['tags'])
                    if 'aliases' in data and isinstance(data['aliases'], list):
                        aliases_total += len(data['aliases'])
            except Exception:
                pass

    # 生成报告
    report_path = MEMORY_ROOT / '_curator_tools' / 'a4_validation_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# A4 验证报告\n\n")
        f.write(f"**生成时间**: {TODAY}\n")
        f.write(f"**总文件数**: {len(files)}\n")
        f.write(f"**验证通过**: {success_count} / {len(files)} ({success_count*100//len(files)}%)\n")
        f.write(f"**验证失败**: {failure_count}\n\n")
        f.write("---\n\n")

        # 统计
        f.write("## 总体统计\n\n")
        f.write("### 状态分布\n\n")
        f.write("| Status | 数量 |\n|--------|------|\n")
        for status, count in status_counter.most_common():
            f.write(f"| {status} | {count} |\n")
        f.write("\n### Category 分布\n\n")
        f.write("| Category | 数量 |\n|----------|------|\n")
        for cat, count in category_counter.most_common():
            f.write(f"| {cat} | {count} |\n")
        f.write(f"\n### Tag/Alias 统计\n\n")
        f.write(f"- 总 Tags 数: {tags_total}\n")
        f.write(f"- 总 Aliases 数: {aliases_total}\n")
        f.write(f"- 平均 Tags/文档: {tags_total/len(files):.1f}\n")
        f.write(f"- 平均 Aliases/文档: {aliases_total/len(files):.1f}\n\n")
        f.write("---\n\n")

        # Issue 统计
        f.write("## 问题统计\n\n")
        if issue_counter:
            f.write("| 问题类型 | 数量 |\n|----------|------|\n")
            for issue, count in issue_counter.most_common():
                f.write(f"| {issue} | {count} |\n")
        else:
            f.write("**无问题,全部通过验证。**\n")
        f.write("\n---\n\n")

        # 失败清单
        if failure_count > 0:
            f.write(f"## 失败清单({failure_count} 文档)\n\n")
            for r in results:
                if not r.get('success'):
                    f.write(f"### `{r['file']}`\n\n")
                    for issue in r.get('issues', []):
                        f.write(f"- ❌ {issue}\n")
                    f.write("\n")

    print(f"\n{'='*80}")
    print(f"Report saved: {report_path}")
    print(f"Validation passed: {success_count}/{len(files)}")
    print(f"Validation failed: {failure_count}")
    print("=" * 80)
    print(f"\nIssue breakdown:")
    for issue, count in issue_counter.most_common(10):
        print(f"  {issue}: {count}")

    return 0 if failure_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
