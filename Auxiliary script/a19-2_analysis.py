"""A19-2 详细分析脚本"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools')

print('=' * 70)
print('A19-2 Dry-Run 详细分析')
print('=' * 70)

# ============================================================
# 1. ALIASES 分析
# ============================================================
print('\n## 1. ALIASES 分析 (236 PENDING)')

with open(ROOT / 'a19-2_fix_aliases_report.json', 'r', encoding='utf-8') as f:
    aliases_data = json.load(f)

pending = [d for d in aliases_data['details'] if d['status'] == 'PENDING']

# 按顶级域统计
domain_counter = Counter()
for d in pending:
    file_path = d['file'].replace('\\', '/')
    if file_path.startswith('_curator_tools/') or file_path.startswith('journal/'):
        continue
    parts = file_path.split('/')
    domain_counter[parts[0]] += 1

print('\n按顶级域分布:')
for d, c in sorted(domain_counter.items(), key=lambda x: -x[1]):
    print(f'  {d}: {c}')

# 分类模式
print('\n变更模式分类:')
patterns = {'category_prefix': [], 'title_dup': []}
for d in pending:
    note = d.get('note', '')
    if any(p in note for p in [' api:', ' avatar:', ' world:', ' patterns:', ' sources:',
                                ' meta:', ' references:', ' hybrid:', ' platform:',
                                ' rules:', ' reviews:', ' sessions:']):
        patterns['category_prefix'].append(d['file'])
    else:
        patterns['title_dup'].append(d['file'])

print(f'  category 前缀变体(原 0-alias): {len(patterns["category_prefix"])}')
print(f'  title 副本(原 1-alias): {len(patterns["title_dup"])}')

# 展示 category 前缀变体的样本(每个域 1 个)
print('\ncategory 前缀变体样本(每个域 1 个):')
shown = set()
for f in patterns['category_prefix']:
    domain = f.replace('\\', '/').split('/')[0]
    if domain not in shown:
        shown.add(domain)
        # 找到这个文件的 note
        for d in pending:
            if d['file'] == f:
                print(f'  [{domain}] {f}')
                print(f'    {d["note"]}')
                break

print('\ntitle 副本样本(前 5 个):')
for f in patterns['title_dup'][:5]:
    for d in pending:
        if d['file'] == f:
            print(f'  {f}')
            print(f'    {d["note"]}')
            break

# ============================================================
# 2. RELATED 分析
# ============================================================
print('\n\n## 2. RELATED 分析 (170 PENDING)')

with open(ROOT / 'a19-2_fix_related_report.json', 'r', encoding='utf-8') as f:
    related_data = json.load(f)

related_pending = [d for d in related_data['details'] if d['status'] == 'PENDING']

# 按顶级域统计
rel_domain_counter = Counter()
for d in related_pending:
    file_path = d['file'].replace('\\', '/')
    if file_path.startswith('_curator_tools/') or file_path.startswith('journal/'):
        continue
    parts = file_path.split('/')
    rel_domain_counter[parts[0]] += 1

print('\n按顶级域分布:')
for d, c in sorted(rel_domain_counter.items(), key=lambda x: -x[1]):
    print(f'  {d}: {c}')

# 起始 related 数量分布
start_counts = Counter()
for d in related_pending:
    note = d.get('note', '')
    if 'related: 0 ->' in note:
        start_counts['0'] += 1
    elif 'related: 1 ->' in note:
        start_counts['1'] += 1
    elif 'related: 2 ->' in note:
        start_counts['2'] += 1
    else:
        start_counts['other'] += 1

print('\n起始 related 数量分布:')
for k, v in sorted(start_counts.items()):
    print(f'  {k} 个 → 5 个: {v} 个文件')

# ============================================================
# 3. SHADER 分析
# ============================================================
print('\n\n## 3. SHADER source_type 分析 (32 PENDING)')

with open(ROOT / 'a19-2_refine_shader_source_type_report.json', 'r', encoding='utf-8') as f:
    shader_data = json.load(f)

shader_pending = [d for d in shader_data['details'] if d['status'] == 'PENDING']

# 按子目录
shader_subdir = Counter()
for d in shader_pending:
    parts = d['file'].split('/')
    if len(parts) >= 2:
        shader_subdir[parts[1]] += 1
    else:
        shader_subdir['(root)'] += 1

print('\n按子目录分布:')
for k, v in sorted(shader_subdir.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

# 显示每个子目录的样本
print('\n样本变更(每子目录 1 个):')
shown_subdir = set()
for d in shader_pending:
    parts = d['file'].split('/')
    subdir = parts[1] if len(parts) >= 2 else '(root)'
    if subdir not in shown_subdir:
        shown_subdir.add(subdir)
        print(f'  [{subdir}] {d["file"]}')
        print(f'    {d["note"]}')

# ============================================================
# 4. 备份总览
# ============================================================
print('\n\n## 4. 备份验证')

import os
backup_dirs = [
    'a19-2_pre_fix_fix_aliases',
    'a19-2_pre_fix_fix_related',
    'a19-2_pre_fix_refine_shader_source_type',
]
for d in backup_dirs:
    backup_path = ROOT / d
    if backup_path.exists():
        files = list(backup_path.rglob('*.md'))
        total_size = sum(f.stat().st_size for f in files)
        print(f'  {d}:')
        print(f'    文件数: {len(files)}')
        print(f'    总大小: {total_size/1024:.1f} KB')
        print(f'    目录结构示例:')
        for f in sorted(files)[:3]:
            rel = f.relative_to(backup_path)
            print(f'      {rel}')
        if len(files) > 3:
            print(f'      ... ({len(files) - 3} more)')

# ============================================================
# 5. 跨脚本冲突检查
# ============================================================
print('\n\n## 5. 跨脚本冲突检查 (是否有同一文件被多个脚本修改)')

aliases_files = set(d['file'] for d in pending)
related_files = set(d['file'] for d in related_pending)
shader_files = set(d['file'] for d in shader_pending)

overlap_ar = aliases_files & related_files
overlap_as = aliases_files & shader_files
overlap_rs = related_files & shader_files
overlap_all = aliases_files & related_files & shader_files

print(f'  aliases ∩ related: {len(overlap_ar)} 个文件')
if overlap_ar:
    for f in list(overlap_ar)[:5]:
        print(f'    - {f}')

print(f'  aliases ∩ shader: {len(overlap_as)} 个文件')
if overlap_as:
    for f in list(overlap_as)[:5]:
        print(f'    - {f}')

print(f'  related ∩ shader: {len(overlap_rs)} 个文件')
if overlap_rs:
    for f in list(overlap_rs)[:5]:
        print(f'    - {f}')

if not overlap_ar and not overlap_as and not overlap_rs:
    print('  ✅ 3 个脚本修改文件无重叠,可以安全并发执行')

# 总修改数
total_unique = len(aliases_files | related_files | shader_files)
print(f'\n总唯一文件数: {total_unique}')
print(f'  aliases: {len(aliases_files)}')
print(f'  related: {len(related_files)}')
print(f'  shader: {len(shader_files)}')

print('\n' + '=' * 70)
print('分析完成')
print('=' * 70)
