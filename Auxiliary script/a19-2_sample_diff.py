"""A19-2 真实内容样本对比 - 展示 5 个代表性文件的实际变化"""
import json
import re
from pathlib import Path

ROOT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
TOOLS = ROOT / '_curator_tools'

# 1. 加载 aliases 报告,找到 5 个不同域的代表性文件
with open(TOOLS / 'a19-2_fix_aliases_report.json', 'r', encoding='utf-8') as f:
    aliases_data = json.load(f)

# 选取样本:跨不同域
SAMPLE_ALIASES = [
    'api\\api-checker.md',
    'avatar\\avatar-modding-guide.md',
    'world\\whitelisted-world-components.md',
    'patterns\\hash-based-dispatch.md',
    'sources\\open-source-projects.md',
]

print('=' * 70)
print('A19-2 真实内容样本对比')
print('=' * 70)

print('\n## 1. ALIASES 真实变更 (5 个代表性文件)')
print('-' * 70)

for sample in SAMPLE_ALIASES:
    file_path = ROOT / sample.replace('\\', '/')
    if not file_path.exists():
        print(f'\n[SKIP] {sample} - 不存在')
        continue

    content = file_path.read_text(encoding='utf-8')

    # 提取 frontmatter 中的 aliases 段
    fm_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        continue

    fm_text = fm_match.group(1)

    # 找 aliases 字段
    alias_match = re.search(r'aliases:\n((?:\s+-\s+.*?\n)+)', fm_text, re.MULTILINE)
    if alias_match:
        aliases_block = alias_match.group(1)
        alias_count = len(re.findall(r'^\s+-\s+', aliases_block, re.MULTILINE))
    else:
        alias_count = 0

    # 找 title 字段
    title_match = re.search(r'^title:\s*(.+)$', fm_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else '(无 title)'

    # 找 category
    cat_match = re.search(r'^category:\s*(.+)$', fm_text, re.MULTILINE)
    category = cat_match.group(1).strip() if cat_match else '(无 category)'

    # 在报告中查找 PENDING note
    note = ''
    for d in aliases_data['details']:
        if d['file'] == sample:
            note = d.get('note', '')
            break

    print(f'\n文件: {sample}')
    print(f'  路径: {file_path.relative_to(ROOT)}')
    print(f'  title: {title}')
    print(f'  category: {category}')
    print(f'  当前 aliases 数: {alias_count}')
    print(f'  脚本计划变更: {note}')

# 2. RELATED 真实变更样本
print('\n\n## 2. RELATED 真实变更 (5 个代表性文件)')
print('-' * 70)

with open(TOOLS / 'a19-2_fix_related_report.json', 'r', encoding='utf-8') as f:
    related_data = json.load(f)

SAMPLE_RELATED = [
    'api\\animator.md',
    'avatar\\modular-avatar.md',
    'world\\whitelisted-world-components.md',
    'vrchatsdk\\01_首页.md',
    'patterns\\hash-based-dispatch.md',
]

for sample in SAMPLE_RELATED:
    file_path = ROOT / sample.replace('\\', '/')
    if not file_path.exists():
        continue

    content = file_path.read_text(encoding='utf-8')
    fm_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        continue
    fm_text = fm_match.group(1)

    related_match = re.search(r'related:\n((?:\s+-\s+.*?\n)+)', fm_text, re.MULTILINE)
    related_count = 0
    if related_match:
        related_count = len(re.findall(r'^\s+-\s+', related_match.group(1), re.MULTILINE))

    # 在报告中查找 PENDING note
    note = ''
    for d in related_data['details']:
        if d['file'] == sample:
            note = d.get('note', '')
            break

    print(f'\n文件: {sample}')
    print(f'  当前 related 数: {related_count}')
    print(f'  脚本计划变更: {note}')
    print(f'  ⚠️  重要:related 内容需执行 --apply 后才能看到具体路径')

# 3. SHADER 真实变更样本
print('\n\n## 3. SHADER source_type 真实变更 (3 个代表文件)')
print('-' * 70)

with open(TOOLS / 'a19-2_refine_shader_source_type_report.json', 'r', encoding='utf-8') as f:
    shader_data = json.load(f)

SAMPLE_SHADER = [
    'avatar/shader/liltoon/overview.md',
    'avatar/shader/poiyomi/index.md',
    'avatar/shader/orl/index.md',
]

for sample in SAMPLE_SHADER:
    file_path = ROOT / sample
    if not file_path.exists():
        continue

    content = file_path.read_text(encoding='utf-8')
    fm_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        continue
    fm_text = fm_match.group(1)

    src_match = re.search(r'^source_type:\s*(.+)$', fm_text, re.MULTILINE)
    src_type = src_match.group(1).strip() if src_match else '(无 source_type)'

    src_url_match = re.search(r'^source:\s*(.+)$', fm_text, re.MULTILINE)
    src_url = src_url_match.group(1).strip() if src_url_match else '(无 source)'

    note = ''
    for d in shader_data['details']:
        if d['file'] == sample:
            note = d.get('note', '')
            break

    print(f'\n文件: {sample}')
    print(f'  当前 source_type: {src_type}')
    print(f'  source URL: {src_url[:60]}...' if len(src_url) > 60 else f'  source: {src_url}')
    print(f'  脚本计划变更: {note}')

# 4. 关键风险:141 个 aliases ∩ related 文件
print('\n\n## 4. 关键风险: 141 个文件同时被 aliases 和 related 脚本修改')
print('-' * 70)

aliases_files = set(d['file'] for d in aliases_data['details'] if d['status'] == 'PENDING')
related_files = set(d['file'] for d in related_data['details'] if d['status'] == 'PENDING')

overlap = aliases_files & related_files
print(f'重叠文件数: {len(overlap)}')
print(f'总唯一文件数: {len(aliases_files | related_files)}')
print(f'占比: {len(overlap)/len(aliases_files|related_files)*100:.1f}%')

print('\n按顶级域分布:')
from collections import Counter
domain_counter = Counter()
for f in overlap:
    parts = f.replace('\\', '/').split('/')
    domain_counter[parts[0]] += 1

for d, c in sorted(domain_counter.items(), key=lambda x: -x[1]):
    print(f'  {d}: {c}')

print('\n前 10 个重叠文件样本:')
for i, f in enumerate(sorted(overlap)[:10]):
    print(f'  {i+1}. {f}')

# 5. 跨脚本同时修改的字段
print('\n\n## 5. 串行执行策略建议')
print('-' * 70)
print('由于 141 个文件会被两个脚本修改,建议串行执行:')
print('  Step 1: fix_aliases_v1.py --apply       (修改 236 个文件的 aliases)')
print('  Step 2: fix_related_v2.py --apply       (修改 170 个文件的 related)')
print('  Step 3: refine_shader_source_type.py --apply (修改 32 个文件的 source_type)')
print('\n并行执行风险:')
print('  - 两个脚本可能同时写同一文件,产生 race condition')
print('  - 备份目录可能错位(a19-2_pre_fix_fix_aliases 备份原版,但 fix_related 在它之上修改)')
print('  - YAML frontmatter 重写可能产生格式不一致')
print('\n正确串行执行:')
print('  - aliases 先改,备份在 a19-2_pre_fix_fix_aliases/')
print('  - related 再改,备份在 a19-2_pre_fix_fix_related/(含 aliases 改完的版本)')
print('  - 若需回滚,先从 fix_related 恢复,再从 fix_aliases 恢复')
