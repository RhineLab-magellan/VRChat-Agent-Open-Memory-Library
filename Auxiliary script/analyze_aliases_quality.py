"""A19-2 aliases 质量分析 - 当前状态"""
import sys
sys.path.insert(0, 'Auxiliary script')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from _fix_common import iter_markdown_files, parse_frontmatter, MEMORY_ROOT, has_chinese
from pathlib import Path
import re

# 分析每个 2-alias 文件,看是否有 "category: x" 模式
total_2_alias = 0
category_prefix_count = 0
samples = []

for fp in iter_markdown_files(MEMORY_ROOT):
    content = fp.read_text(encoding='utf-8')
    parsed = parse_frontmatter(content)
    if parsed:
        yaml_dict = parsed[0]
        aliases = yaml_dict.get('aliases', [])
        if not isinstance(aliases, list):
            continue
        n = len(aliases)
        if n != 2:
            continue
        total_2_alias += 1
        # 检查是否有 category 前缀变体
        a, b = str(aliases[0]), str(aliases[1])
        category = yaml_dict.get('category', '')
        # 检查 b 是否是 "category: a" 变体
        is_prefix = False
        if ':' in b:
            prefix, rest = b.split(':', 1)
            rest = rest.strip()
            if rest == a.strip():
                is_prefix = True
        if is_prefix:
            category_prefix_count += 1
            if len(samples) < 30:
                samples.append((str(fp.relative_to(MEMORY_ROOT)), a, b, category))

print(f'=== 2-alias 文件分析 ===')
print(f'  2-alias 总数: {total_2_alias}')
print(f'  category 前缀变体数: {category_prefix_count} ({category_prefix_count/total_2_alias*100:.1f}%)')
print(f'  其他类型: {total_2_alias - category_prefix_count}')

print()
print('=== category 前缀变体样本(前 30 个) ===')
for fp, a, b, cat in samples:
    print(f'  [{cat}] {fp}')
    print(f'    a: {a!r}')
    print(f'    b: {b!r}')

# 按域统计
domain_counter = {}
for fp, a, b, cat in samples:
    domain = fp.replace('\\', '/').split('/')[0]
    domain_counter[domain] = domain_counter.get(domain, 0) + 1

print()
print('=== category 前缀变体按域分布 ===')
for d, c in sorted(domain_counter.items(), key=lambda x: -x[1]):
    print(f'  {d}: {c}')
