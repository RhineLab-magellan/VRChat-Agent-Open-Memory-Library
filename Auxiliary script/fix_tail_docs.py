#!/usr/bin/env python3
"""
A9 长尾文档修复
=================
为部分"内容型"长尾文档建立反向引用(添加到相关父文档的 related 字段):
- world/occlusion-culling-guide.md → world/performance-guide.md
- world/creator-economy.md → _always-load.md
- avatar/shader/other-shaders.md → avatar/index.md
- world/shader/graphlit.md → world/shader/index.md
- world/shader/index.md → _always-load.md
- avatar/shader/unlitwf/index.md → avatar/index.md
- avatar/shader/orl/index.md → avatar/index.md
- avatar/shader/filamented/index.md → avatar/index.md

跳过(故意作为 tail):
- 所有 index.md(本身就是入口)
- 所有 README.md(本身就是入口)
- world/luraswitch2.md, world/vvmw.md, world/udonsharp-compilation.md
  (这些是工具使用指南,被 _always-load.md 反引号引用,已通过文本关联)
- journal/sessions/*(会话日志)
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

MEMORY_ROOT = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\memory')

# 父索引 → 需要添加的长尾文件
PARENT_TO_TAILS = {
    'world/performance-guide.md': [
        'world/occlusion-culling-guide.md',
    ],
    '_always-load.md': [
        'world/creator-economy.md',
        'world/shader/index.md',
    ],
    'avatar/index.md': [
        'avatar/shader/other-shaders.md',
        'avatar/shader/unlitwf/index.md',
        'avatar/shader/orl/index.md',
        'avatar/shader/filamented/index.md',
    ],
    'world/shader/index.md': [
        'world/shader/graphlit.md',
    ],
}


def add_to_related_field(rel_path: str, tails: list) -> dict:
    """为文件添加 tails 到 related 字段"""
    fp = MEMORY_ROOT / rel_path
    if not fp.exists():
        return {'file': rel_path, 'status': 'MISSING', 'changes': []}

    content = fp.read_text(encoding='utf-8')
    original = content
    changes = []

    # 1. 找到 frontmatter
    m = re.match(r'^(---\n)(.+?)(\n---\n?)(.*)', content, re.DOTALL)
    if not m:
        return {'file': rel_path, 'status': 'NO_FRONTMATTER', 'changes': []}

    opening, yaml_text, closing, body = m.group(1), m.group(2), m.group(3), m.group(4)

    # 2. 检查现有 related 字段
    related_match = re.search(r'^related:\s*\n((?:\s+-\s+.+\n?)+)', yaml_text, re.MULTILINE)
    if related_match:
        existing_block = related_match.group(1)
        existing_lines = [l.strip() for l in existing_block.strip().split('\n')]
        existing_items = set()
        for line in existing_lines:
            m2 = re.match(r'-\s+["\']?([^"\']+)["\']?\s*$', line)
            if m2:
                existing_items.add(m2.group(1))

        new_items = []
        for tail in tails:
            if tail not in existing_items:
                new_items.append(tail)

        if new_items:
            new_block = existing_block
            for item in new_items:
                new_block += f'  - {item}\n'

            yaml_text = yaml_text.replace(existing_block, new_block)
            changes.append(f'related: +{len(new_items)} entries')
    else:
        new_block = 'related:\n'
        for tail in tails:
            new_block += f'  - {tail}\n'

        source_match = re.search(r'^source:\s*', yaml_text, re.MULTILINE)
        if source_match:
            yaml_text = yaml_text[:source_match.start()] + new_block + '\n' + yaml_text[source_match.start():]
        else:
            yaml_text = yaml_text.rstrip() + '\n' + new_block
        changes.append(f'related: created with {len(tails)} entries')

    content = opening + yaml_text + closing + body
    if content != original:
        fp.write_text(content, encoding='utf-8')

    return {
        'file': rel_path,
        'status': 'FIXED' if changes else 'NO_CHANGES',
        'changes': changes,
    }


def main():
    print("=" * 80)
    print("A9 长尾文档修复")
    print("=" * 80)
    print(f"父索引数: {len(PARENT_TO_TAILS)}")
    total_tails = sum(len(v) for v in PARENT_TO_TAILS.values())
    print(f"长尾文件数: {total_tails}")
    print()

    results = []
    for parent_rel, tails in PARENT_TO_TAILS.items():
        result = add_to_related_field(parent_rel, tails)
        results.append(result)
        if result['status'] == 'FIXED':
            print(f"  [FIXED] {parent_rel}: {', '.join(result['changes'])}")
        elif result['status'] == 'NO_CHANGES':
            print(f"  [NO_CHANGE] {parent_rel}: all tails already referenced")
        else:
            print(f"  [ERROR] {parent_rel}: {result['status']}")

    fixed = sum(1 for r in results if r['status'] == 'FIXED')
    print()
    print("=" * 80)
    print(f"完成: {fixed}/{len(results)} 父索引已更新")
    return 0


if __name__ == '__main__':
    sys.exit(main())
