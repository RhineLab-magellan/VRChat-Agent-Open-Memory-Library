"""检查当前 aliases 数量分布"""
import sys
sys.path.insert(0, 'Auxiliary script')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from _fix_common import iter_markdown_files, parse_frontmatter, MEMORY_ROOT
from pathlib import Path

counts = {}
files_by_count = {0: [], 1: [], 2: [], 3: []}

for fp in iter_markdown_files(MEMORY_ROOT):
    content = fp.read_text(encoding='utf-8')
    parsed = parse_frontmatter(content)
    if parsed:
        yaml_dict = parsed[0]
        aliases = yaml_dict.get('aliases', [])
        n = len(aliases) if isinstance(aliases, list) else 0
        counts[n] = counts.get(n, 0) + 1
        if n in files_by_count:
            files_by_count[n].append(str(fp.relative_to(MEMORY_ROOT)))

print('=== 当前 aliases 数量分布 ===')
for n in sorted(counts.keys()):
    print(f'  {n} 个: {counts[n]}')

print()
print('=== 1 个 alias 的文件(应被修复) ===')
for f in files_by_count[1][:20]:
    print(f'  {f}')
print(f'  ... 共 {len(files_by_count[1])} 个' if len(files_by_count[1]) > 20 else f'  共 {len(files_by_count[1])} 个')

print()
print('=== 0 个 alias 的文件 ===')
for f in files_by_count[0][:20]:
    print(f'  {f}')
print(f'  ... 共 {len(files_by_count[0])} 个' if len(files_by_count[0]) > 20 else f'  共 {len(files_by_count[0])} 个')
