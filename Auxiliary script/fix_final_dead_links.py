#!/usr/bin/env python3
"""
A7-Final 死链修复 - 清理 8 条剩余死链
====================================
剩余 8 条死链:
1. rules/index.md -> security-rules.md (文件不存在) - 移除引用
2. sources/example-central.md -> world/media-systems.md (文件不存在) - 移除引用
3. world/bakery/light-baking-guide.md -> misc/maebbie.md (文件不存在) - 移除引用
4. world/clientsim/systems/index.md -> playerdata-editor.md (文件不存在) - 移除引用
5. world/scene-components/textmeshpro.md -> textmeshpro/tmp_text.md (相关字段 + markdown) - 移除
6. world/scene-components/vrc-objectsync.md -> patterns/physics-object-lifecycle.md (文件不存在) - 移除引用
7. world/udon/udonsharp/attributes.md -> ../../FACT.md (related 字段,应为 ../../../FACT.md) - 修正路径
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

MEMORY_ROOT = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\memory')

# 修复策略:
# - REMOVE: 完全删除该行(从 related 块 / markdown 链接中)
# - FIX_PATH: 修正路径
ACTIONS = {
    # 1. rules/index.md - 移除 security-rules.md
    ('rules/index.md', 'rules/security-rules.md', 'related'): None,
    # 2. sources/example-central.md - 移除 world/media-systems.md (related)
    ('sources/example-central.md', 'world/media-systems.md', 'related'): None,
    # 3. world/bakery/light-baking-guide.md - 移除 misc/maebbie.md (related)
    ('world/bakery/light-baking-guide.md', 'misc/maebbie.md', 'related'): None,
    # 4. world/clientsim/systems/index.md - 移除 playerdata-editor.md (related)
    ('world/clientsim/systems/index.md', 'playerdata-editor.md', 'related'): None,
    # 5a. world/scene-components/textmeshpro.md - 移除 textmeshpro/tmp_text.md (related)
    ('world/scene-components/textmeshpro.md', 'textmeshpro/tmp_text.md', 'related'): None,
    # 5b. world/scene-components/textmeshpro.md - 移除 markdown 链接
    ('world/scene-components/textmeshpro.md', './textmeshpro/tmp_text.md', 'markdown'): None,
    # 6. world/scene-components/vrc-objectsync.md - 移除 patterns/physics-object-lifecycle.md
    ('world/scene-components/vrc-objectsync.md', 'patterns/physics-object-lifecycle.md', 'related'): None,
    # 7. world/udon/udonsharp/attributes.md - 修正 ../../FACT.md -> ../../../FACT.md (related)
    ('world/udon/udonsharp/attributes.md', '../../FACT.md', 'related'): '../../../FACT.md',
}


def remove_related_line(yaml_text: str, target: str) -> str:
    """从 related 块中删除包含 target 的整行(支持带引号和不带引号)"""
    new_lines = []
    # 转义 target 用于正则(以防 target 本身含正则特殊字符)
    target_esc = re.escape(target)
    for line in yaml_text.split('\n'):
        # 匹配 - target(不带引号)或 - "target"(双引号)或 - 'target'(单引号)
        if re.match(rf'^\s+-\s+["\']?{target_esc}["\']?\s*$', line):
            continue
        new_lines.append(line)
    return '\n'.join(new_lines)


def remove_markdown_link(content: str, target: str) -> str:
    """从 markdown 内容中删除引用 target 的链接"""
    # 处理 [text](target) 和 [text](target#anchor)
    pattern = rf'\[([^\]]*)\]\({re.escape(target)}(?:#[^)]*)?\)'
    new_content = re.sub(pattern, '', content)
    # 清理 "  - " 残留(只对相关字段有效,但安全起见清理空 list item)
    return new_content


def fix_related_path(yaml_text: str, old_path: str, new_path: str) -> str:
    """修正 related 字段中的路径"""
    # 处理带引号和不带引号两种情况
    pattern_with_quote = rf'^(\s+-\s+)(["\']){re.escape(old_path)}\2\s*$'
    pattern_without_quote = rf'^(\s+-\s+){re.escape(old_path)}\s*$'

    new_yaml = re.sub(
        pattern_with_quote,
        lambda m: f'{m.group(1)}{m.group(2)}{new_path}{m.group(2)}',
        yaml_text,
        flags=re.MULTILINE,
    )
    if new_yaml == yaml_text:
        new_yaml = re.sub(
            pattern_without_quote,
            lambda m: f'{m.group(1)}{new_path}',
            yaml_text,
            flags=re.MULTILINE,
        )
    return new_yaml


def fix_file(rel_path: str) -> dict:
    """修复单个文件的所有死链"""
    fp = MEMORY_ROOT / rel_path
    if not fp.exists():
        return {'file': rel_path, 'status': 'MISSING', 'changes': []}

    content = fp.read_text(encoding='utf-8')
    original = content
    changes = []

    # 收集本文件需要处理的所有 action
    file_actions = [
        (key[1], key[2]) for key in ACTIONS.keys() if key[0] == rel_path
    ]
    # 调试:rules/index.md
    if rel_path == 'rules/index.md':
        print(f"  [DEBUG] rules/index.md file_actions: {file_actions}")

    # 1. 处理 related 字段
    m = re.match(r'^(---\n)(.+?)(\n---\n?)(.*)', content, re.DOTALL)
    if m:
        opening, yaml_text, closing, body = m.group(1), m.group(2), m.group(3), m.group(4)

        related_modified = False
        for target, action_type in file_actions:
            # 找到对应的 action
            for (src, tgt, atype), replacement in ACTIONS.items():
                if src == rel_path and tgt == target and atype == action_type and action_type == 'related':
                    if replacement is None:
                        # 移除
                        new_yaml = remove_related_line(yaml_text, target)
                        if new_yaml != yaml_text:
                            yaml_text = new_yaml
                            related_modified = True
                            changes.append(f'related: removed {target}')
                    else:
                        # 修正路径
                        new_yaml = fix_related_path(yaml_text, target, replacement)
                        if new_yaml != yaml_text:
                            yaml_text = new_yaml
                            related_modified = True
                            changes.append(f'related: {target} -> {replacement}')

        if related_modified:
            content = opening + yaml_text + closing + body

    # 2. 处理 markdown 链接
    for target, action_type in file_actions:
        for (src, tgt, atype), replacement in ACTIONS.items():
            if src == rel_path and tgt == target and atype == action_type and action_type == 'markdown':
                if replacement is None:
                    new_content = remove_markdown_link(content, target)
                    if new_content != content:
                        content = new_content
                        changes.append(f'markdown: removed {target}')

    if content != original:
        fp.write_text(content, encoding='utf-8')

    return {
        'file': rel_path,
        'status': 'FIXED' if changes else 'NO_CHANGES',
        'changes': changes,
    }


def main():
    print("=" * 80)
    print("A7-Final 死链修复 - 清理 8 条剩余死链")
    print("=" * 80)
    print(f"Action 数: {len(ACTIONS)}")
    print(f"涉及源文件数: {len(set(k[0] for k in ACTIONS.keys()))}")
    print()

    results = []
    source_files = sorted(set(k[0] for k in ACTIONS.keys()))
    for rel_path in source_files:
        result = fix_file(rel_path)
        results.append(result)
        if result['status'] == 'FIXED':
            print(f"  [FIXED] {rel_path}: {len(result['changes'])} change(s)")
            for c in result['changes']:
                print(f"    - {c}")
        else:
            print(f"  [NO_CHANGE] {rel_path}")

    fixed = sum(1 for r in results if r['status'] == 'FIXED')
    print()
    print("=" * 80)
    print(f"完成: {fixed}/{len(results)} 文件已修复")
    return 0


if __name__ == '__main__':
    sys.exit(main())
