#!/usr/bin/env python3
"""
A24 P1-5: 批量清理 body 纯净化违反
====================================
识别并删除 body 开头的治理元信息引用块(>)。不动 frontmatter 也不动真正的内容引用。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

MEMORY = Path('memory')
BACKUP = Path('memory/_curator_tools/a24_pre_audit_fix')

# 治理元信息模式(行首 > 后跟这些前缀)
META_PATTERNS = [
    r'VRChatAgent v',
    r'^\s*\*?\*?版本[:：]',
    r'更新日期',
    r'最后更新',
    r'知识库索引',
    r'索引日期',
    r'维护[:：]',
    r'生成于',
    r'Domain[:：]',
    r'Source[:：]\s*`',
    r'@claude',
    r'本文档由',
    r'由.{0,6}(整理|维护|补全)',
    r'收录于',
    r'建议查看',
    r'\*\*更新日期\*\*',
    r'更新[:：]\s*\d{4}',  # "更新: 2026-..."
]
META_RE = re.compile(r'^\s*>\s*(?:' + '|'.join(META_PATTERNS) + r')', re.IGNORECASE)


def is_meta_line(line: str) -> bool:
    """判断一行是否为治理元信息"""
    return bool(META_RE.match(line))


def clean_file(md: Path) -> tuple:
    """清理单个文件,返回 (是否修改, 删除行数)"""
    text = md.read_text(encoding='utf-8', errors='replace')

    # 拆 frontmatter + body
    m = re.match(r'^(---\n.*?\n---\n)(.*)', text, re.DOTALL)
    if not m:
        return False, 0
    fm, body = m.group(1), m.group(2)

    lines = body.split('\n')
    new_lines = []
    removed = 0
    in_meta_block = True  # 仅在 body 前 30 行内扫描

    for i, line in enumerate(lines):
        if i > 30:
            in_meta_block = False
        if in_meta_block and is_meta_line(line):
            removed += 1
            continue
        # 保留
        new_lines.append(line)

    # 清理因删除行产生的连续空行
    new_body = '\n'.join(new_lines)
    new_body = re.sub(r'\n{4,}', '\n\n\n', new_body)

    if removed == 0:
        return False, 0

    new_text = fm + new_body
    md.write_text(new_text, encoding='utf-8')
    return True, removed


def main():
    # 先备份原版
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True, exist_ok=True)

    modified = []
    for md in MEMORY.rglob('*.md'):
        if '_curator_tools' in md.parts:
            continue
        changed, count = clean_file(md)
        if changed:
            modified.append((str(md), count))

    print(f'=== A24 P1-5 body 纯净化清理 ===')
    print(f'扫描范围: memory/ 全库(排除 _curator_tools/)')
    print(f'修改文件数: {len(modified)}')
    print(f'删除行数总计: {sum(c for _, c in modified)}')
    print()
    for f, c in modified:
        print(f'  [{c:>2} 行] {f}')

    # 写报告
    report = MEMORY / '_curator_tools' / 'a24_body_purify_report.md'
    with open(report, 'w', encoding='utf-8') as f:
        f.write('# A24 P1-5 Body 纯净化清理报告\n\n')
        f.write(f'**日期**: 2026-07-01\n')
        f.write(f'**修改文件数**: {len(modified)}\n')
        f.write(f'**删除行数**: {sum(c for _, c in modified)}\n\n')
        f.write('## 修改清单\n\n')
        f.write('| 文件 | 删除行数 |\n|------|---------|\n')
        for fp, c in modified:
            f.write(f'| `{fp}` | {c} |\n')
    print(f'\n报告: {report}')


if __name__ == '__main__':
    main()
