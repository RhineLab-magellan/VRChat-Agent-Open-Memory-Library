"""检查当前 related 数量分布"""
import sys
sys.path.insert(0, 'Auxiliary script')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from _fix_common import iter_markdown_files, parse_frontmatter, MEMORY_ROOT
from pathlib import Path

counts = {}
files_by_count = {0: [], 1: [], 2: [], 3: [], 4: []}

for fp in iter_markdown_files(MEMORY_ROOT):
    content = fp.read_text(encoding='utf-8')
    parsed = parse_frontmatter(content)
    if parsed:
        yaml_dict = parsed[0]
        related = yaml_dict.get('related', [])
        n = len(related) if isinstance(related, list) else 0
        counts[n] = counts.get(n, 0) + 1
        if n in files_by_count:
            files_by_count[n].append(str(fp.relative_to(MEMORY_ROOT)))

print('=== 当前 related 数量分布 ===')
for n in sorted(counts.keys()):
    print(f'  {n} 个: {counts[n]}')

total = sum(counts.values())
print(f'  总计: {total}')

print()
print('=== < 5 个 related 的文件(可能需补全) ===')
short_files = []
for n in [0, 1, 2, 3, 4]:
    short_files.extend(files_by_count[n])
print(f'  共 {len(short_files)} 个')
for f in short_files[:30]:
    print(f'  {f}')

print()
print('=== 0 个 related 的文件 ===')
print(f'  共 {len(files_by_count[0])} 个')
for f in files_by_count[0][:10]:
    print(f'  {f}')
