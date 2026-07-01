#!/usr/bin/env python3
"""
A8 孤立文档修复
=================
为 34 个孤立文档中的大部分建立引用关系(添加到父索引的 related 字段):
1. world/examples/* → world/examples/README.md
2. world/udon/* (10) → world/udon/index.md
3. reviews/* (3) → reviews/index.md
4. patterns/unorthodox-patterns.md → patterns/index.md
5. avatar/* (2) → avatar/index.md
6. world/bakery/index.md → _always-load.md
7. journal/README.md → index.md

跳过(故意孤立):
- journal/sessions/* (6 个) - 会话日志,临时记录
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

MEMORY_ROOT = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\memory')

# 父索引 → 需要添加的孤儿文件列表
PARENT_TO_ORPHANS = {
    'world/examples/README.md': [
        'world/examples/ai-navigation.md',
        'world/examples/detect-controller-collide.md',
        'world/examples/image-loading.md',
        'world/examples/minimap.md',
        'world/examples/mute-others.md',
        'world/examples/player-join-zones.md',
        'world/examples/screen-canvas.md',
        'world/examples/udon.md',
    ],
    'world/udon/index.md': [
        'world/udon/ai-navigation.md',
        'world/udon/animation-events.md',
        'world/udon/avatar-events.md',
        'world/udon/debugging-udon-projects.md',
        'world/udon/event-execution-order.md',
        'world/udon/image-loading.md',
        'world/udon/input-events.md',
        'world/udon/string-loading.md',
        'world/udon/udon-moderation-tool-guidelines.md',
    ],
    'reviews/index.md': [
        'reviews/review-checklist.md',
        'reviews/severity-model.md',
    ],
    'patterns/index.md': [
        'patterns/unorthodox-patterns.md',
    ],
    'avatar/index.md': [
        'avatar/avatar-parameter-staged-sync.md',
        'avatar/ma-component-cards.md',
    ],
    '_always-load.md': [
        'world/bakery/index.md',
    ],
    'index.md': [
        'journal/README.md',
    ],
}


def add_to_related_field(rel_path: str, orphans: list) -> dict:
    """为文件添加 orphans 到 related 字段"""
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
        # 已存在 related 块,追加
        existing_block = related_match.group(1)
        existing_lines = [l.strip() for l in existing_block.strip().split('\n')]
        # 解析已有条目
        existing_items = set()
        for line in existing_lines:
            m2 = re.match(r'-\s+["\']?([^"\']+)["\']?\s*$', line)
            if m2:
                existing_items.add(m2.group(1))

        # 添加新的
        new_items = []
        for orphan in orphans:
            if orphan not in existing_items:
                new_items.append(orphan)

        if new_items:
            # 追加到 related 块末尾
            new_block = existing_block
            for item in new_items:
                new_block += f'  - {item}\n'

            yaml_text = yaml_text.replace(existing_block, new_block)
            changes.append(f'related: +{len(new_items)} entries')
    else:
        # 没有 related 块,创建一个
        # 找到合适的位置插入(在 source 字段之前)
        new_block = 'related:\n'
        for orphan in orphans:
            new_block += f'  - {orphan}\n'

        # 尝试在 source 字段前插入
        source_match = re.search(r'^source:\s*', yaml_text, re.MULTILINE)
        if source_match:
            yaml_text = yaml_text[:source_match.start()] + new_block + '\n' + yaml_text[source_match.start():]
        else:
            # 追加到末尾
            yaml_text = yaml_text.rstrip() + '\n' + new_block
        changes.append(f'related: created with {len(orphans)} entries')

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
    print("A8 孤立文档修复 - 为 28 个孤儿建立引用关系")
    print("=" * 80)
    print(f"父索引数: {len(PARENT_TO_ORPHANS)}")
    total_orphans = sum(len(v) for v in PARENT_TO_ORPHANS.values())
    print(f"孤儿文件数: {total_orphans}")
    print()

    results = []
    for parent_rel, orphans in PARENT_TO_ORPHANS.items():
        result = add_to_related_field(parent_rel, orphans)
        results.append(result)
        if result['status'] == 'FIXED':
            print(f"  [FIXED] {parent_rel}: {', '.join(result['changes'])}")
        elif result['status'] == 'NO_CHANGES':
            print(f"  [NO_CHANGE] {parent_rel}: all orphans already referenced")
        else:
            print(f"  [ERROR] {parent_rel}: {result['status']}")

    fixed = sum(1 for r in results if r['status'] == 'FIXED')
    print()
    print("=" * 80)
    print(f"完成: {fixed}/{len(results)} 父索引已更新")
    print(f"跳过的孤立: 6 个 journal/sessions/* (会话日志,故意孤立)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
