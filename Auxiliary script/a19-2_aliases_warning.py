"""A19-2 ALIASES 启发式质量警告"""
import json
from pathlib import Path
import re

ROOT = Path('C:/CherryStudio/Agent/UdonSharpAgent/memory')
TOOLS = ROOT / '_curator_tools'

# 强制 UTF-8 输出
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print('=' * 70)
print('A19-2 ALIASES 启发式质量分析')
print('=' * 70)

# 1. 加载所有 PENDING 详情
with open(TOOLS / 'a19-2_fix_aliases_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

pending = [d for d in data['details'] if d['status'] == 'PENDING']

# 2. 检查每个 PENDING:新增 alias 是否与现有 alias 重复(只是加了前缀)
print(f'\n总 PENDING: {len(pending)}')

duplicate_additions = []
unique_additions = []
for d in pending:
    note = d.get('note', '')
    # 解析: ['A'] -> ['A', 'B']
    m = re.match(r"aliases:\s*\[(.+?)\]\s*->\s*\[(.+?)\]", note)
    if m:
        before = m.group(1)
        after = m.group(2)
        # 提取新加入的(after 中不在 before 中的)
        before_items = [s.strip().strip("'").strip('"') for s in before.split(',') if s.strip()]
        after_items = [s.strip().strip("'").strip('"') for s in after.split(',') if s.strip()]

        new_items = [x for x in after_items if x not in before_items]
        if new_items:
            # 检查新加的是否就是"category: 现有"模式
            for new_item in new_items:
                # 移除可能的前缀(category: 或 api: 等)
                stripped = re.sub(r'^[a-z]+:\s*', '', new_item, flags=re.IGNORECASE)
                if stripped in before_items:
                    duplicate_additions.append((d['file'], before_items[0], new_item))
                else:
                    unique_additions.append((d['file'], before_items, new_item))

print(f'\n【重复型新增】新增 alias 实际是"category: 旧alias"前缀变体(质量较低):')
print(f'  数量: {len(duplicate_additions)} / {len(pending)} ({len(duplicate_additions)/len(pending)*100:.1f}%)')

print(f'\n【真正新增】新增 alias 是新内容(质量较高):')
print(f'  数量: {len(unique_additions)} / {len(pending)} ({len(unique_additions)/len(pending)*100:.1f}%)')

# 3. 展示样本
print('\n## 重复型新增 样本(前 10):')
for i, (fp, old, new) in enumerate(duplicate_additions[:10]):
    print(f'  {i+1}. {fp}')
    print(f'     旧: {old}')
    print(f'     新: {new}  (即 "{new.split(":", 1)[0].strip()}: {old}")')

print('\n## 真正新增 样本(前 10):')
for i, (fp, old, new) in enumerate(unique_additions[:10]):
    print(f'  {i+1}. {fp}')
    print(f'     旧: {old}')
    print(f'     新: {new}')

# 4. 结论
print('\n' + '=' * 70)
print('结论')
print('=' * 70)

if len(duplicate_additions) > len(pending) * 0.8:
    print('\n[WARN] 80%+ 的"补全"是添加 category 前缀变体,不是真正的语义补全')
    print('  这些 alias 提供少量检索价值(可通过 "category: xxx" 检索)')
    print('  但严格说不算"高质量 alias"')
    print('\n建议:')
    print('  - 方案 A: 接受当前启发式(简单,自动,效果一般)')
    print('  - 方案 B: 调整脚本,只处理 0-alias 文件,且只加 1 个真实新 alias')
    print('  - 方案 C: 推迟 A19-2 aliases,优先做 A19-2 related(对导航/检索影响更大)')

# 5. 进一步细化:检查 related 内容
print('\n\n## RELATED 内容质量(基于启发式评分)')
print('-' * 70)

with open(TOOLS / 'a19-2_fix_related_report.json', 'r', encoding='utf-8') as f:
    rel_data = json.load(f)

rel_pending = [d for d in rel_data['details'] if d['status'] == 'PENDING']
print(f'\nRELATED PENDING 总数: {len(rel_pending)}')
print('\n⚠️  IMPORTANT: related 内容的实际路径需要在 --apply 后才能看到')
print('  启发式评分:同父目录 +3 / 同祖父目录 +1 / 共享 tags +N')
print('  风险:可能选择"同目录但主题不相关"的文件(如 meta/working-modes.md)')
print('  验证 Agent 需要重点检查:related 引用的文件是否在主题上相关')
