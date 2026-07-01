#!/usr/bin/env python3
"""
A4 修复脚本
==============
自动修复 A4 验证发现的 6 个问题:
1. TOO_FEW_TAGS (4 文档): 补充 tags 到 3+
2. INVALID_VERSION (1 文档): 清理括号后缀
3. INVALID_DATE_FORMAT (1 文档): 清理括号后缀
"""
import re
from pathlib import Path

# 脚本位置: UdonSharpAgent/Auxiliary script/fix_script.py
# 知识库位置: UdonSharpAgent/memory/
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'

# 修复清单
FIXES = {
    'api/animator.md': {
        'add_tags': ['udonsharp'],  # 补到 3 个
    },
    'api/player-api.md': {
        'add_tags': ['udonsharp'],
    },
    'api/ui.md': {
        'add_tags': ['reference'],
    },
    'journal/README.md': {
        'add_tags': ['navigation'],
    },
    'world/luraswitch2.md': {
        'fix_version': 'v3.00',
    },
    'world/udon/networking/index.md': {
        'fix_date': r'2026-06-15',
    },
}


def fix_file(rel_path: str, fix: dict) -> bool:
    """修复单个文档,返回是否成功"""
    filepath = MEMORY_ROOT / rel_path
    content = filepath.read_text(encoding='utf-8')

    modified = False

    # 修复 tags(添加)
    if 'add_tags' in fix:
        for new_tag in fix['add_tags']:
            # 在 tags 块内,最后一个 - xxx 后插入
            # 找到最后一行 `  - xxx`
            pattern = r'(tags:\n((?:\s*-\s*[^\n]+\n)+))'
            m = re.search(pattern, content)
            if m:
                tags_block = m.group(1)
                # 检查是否已存在
                if f'  - {new_tag}' not in tags_block:
                    new_tags_block = tags_block.rstrip() + f'\n  - {new_tag}\n'
                    content = content.replace(tags_block, new_tags_block, 1)
                    modified = True

    # 修复 version(提取数字模式)
    if 'fix_version' in fix:
        pattern = r'^version:\s*v?(\d+\.\d+).*$'
        replacement = f"version: {fix['fix_version']}"
        new_content = re.sub(pattern, replacement, content, count=1, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            modified = True

    # 修复 last_review(提取日期模式)
    if 'fix_date' in fix:
        pattern = r'^last_review:\s*(\d{4}-\d{2}-\d{2}).*$'
        replacement = f"last_review: {fix['fix_date']}"
        new_content = re.sub(pattern, replacement, content, count=1, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            modified = True

    if modified:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    print("=" * 80)
    print("A4 Fix Script")
    print("=" * 80)

    fixed_count = 0
    for rel_path, fix in FIXES.items():
        print(f"\n[Fixing] {rel_path}")
        try:
            if fix_file(rel_path, fix):
                print(f"  [OK] Fixed: {fix}")
                fixed_count += 1
            else:
                print(f"  [WARN] No changes applied")
        except Exception as e:
            print(f"  [ERROR] {e}")

    print(f"\n{'='*80}")
    print(f"Fixed: {fixed_count} / {len(FIXES)}")
    print("=" * 80)


if __name__ == '__main__':
    main()
