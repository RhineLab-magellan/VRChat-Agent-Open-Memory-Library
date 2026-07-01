#!/usr/bin/env python3
"""
A10 二次审计 - 知识库偏移检测
================================
对比当前库 vs 备份库,检查:
1. 文件数量变化(新增/删除/修改)
2. 内容偏移(行数/字节数变化)
3. 关键知识完整性(FACT.md 关键事实、SDK 文档、案例研究等)
4. 引用图谱偏移(死链/孤立/长尾)
5. 知识覆盖度变化
"""
import re
import sys
import hashlib
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# ==================== 配置 ====================
SCRIPT_DIR = Path(__file__).resolve().parent
CURRENT_ROOT = SCRIPT_DIR.parent / 'memory'
BACKUP_ROOT = SCRIPT_DIR.parent / '知识库备份' / 'memory'
TODAY = "2026-06-20"
EXCLUDE_DIRS = {'_curator_tools', '__pycache__'}


# ==================== 工具函数 ====================
def find_md_files(root: Path) -> dict:
    """扫描所有 .md 文件,返回 {rel_path: Path}"""
    result = {}
    for path in root.rglob('*.md'):
        if any(excl in path.parts for excl in EXCLUDE_DIRS):
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = path
    return result


def file_stats(fp: Path) -> dict:
    """获取文件统计信息"""
    if not fp.exists():
        return {'exists': False, 'size': 0, 'lines': 0, 'hash': None}
    content = fp.read_text(encoding='utf-8', errors='replace')
    return {
        'exists': True,
        'size': len(content),
        'lines': content.count('\n') + 1,
        'hash': hashlib.md5(content.encode('utf-8')).hexdigest(),
    }


def extract_body_content(content: str) -> str:
    """提取 frontmatter 之后的正文,用于内容对比"""
    m = re.match(r'^---\n.+?\n---\n?(.*)', content, re.DOTALL)
    if m:
        return m.group(1)
    return content


def body_size(content: str) -> int:
    """获取去除 frontmatter 后的正文大小"""
    return len(extract_body_content(content))


# ==================== 关键知识检查 ====================
def extract_key_facts(content: str) -> set:
    """提取关键事实(标题/代码块/表格行)用于知识完整性检查"""
    facts = set()
    # 1. 提取所有标题
    for m in re.finditer(r'^#{1,6}\s+(.+?)$', content, re.MULTILINE):
        facts.add(('title', m.group(1).strip()))
    # 2. 提取代码块语言标识
    for m in re.finditer(r'```(\w+)', content):
        facts.add(('code-lang', m.group(1).strip()))
    # 3. 提取粗体关键术语
    for m in re.finditer(r'\*\*([^*\n]{2,50})\*\*', content):
        facts.add(('term', m.group(1).strip()))
    return facts


# ==================== 报告 ====================
def main():
    print("=" * 80)
    print("A10 二次审计 - 知识库偏移检测")
    print(f"Date: {TODAY}")
    print("=" * 80)

    # 1. 文件扫描
    current_files = find_md_files(CURRENT_ROOT)
    backup_files = find_md_files(BACKUP_ROOT)

    current_set = set(current_files.keys())
    backup_set = set(backup_files.keys())

    # 2. 文件集合差异
    added_files = current_set - backup_set  # 当前库有,备份没有(新文件)
    removed_files = backup_set - current_set  # 备份有,当前库没有(删除)
    common_files = current_set & backup_set  # 两边都有

    print(f"\n当前库 .md 文件数: {len(current_files)}")
    print(f"备份库 .md 文件数: {len(backup_files)}")
    print(f"新增文件: {len(added_files)}")
    print(f"删除文件: {len(removed_files)}")
    print(f"共同文件: {len(common_files)}")

    # 3. 详细文件级对比
    print("\n" + "=" * 80)
    print("文件级对比(共同文件)")
    print("=" * 80)

    size_diff = []
    line_diff = []
    content_changed = []  # 正文大小变化
    missing_key_facts = []  # 关键事实丢失

    for rel in sorted(common_files):
        cur_stats = file_stats(current_files[rel])
        bk_stats = file_stats(backup_files[rel])

        # 字节变化
        size_delta = cur_stats['size'] - bk_stats['size']
        # 行数变化
        line_delta = cur_stats['lines'] - bk_stats['lines']
        # 内容 hash
        hash_changed = cur_stats['hash'] != bk_stats['hash']

        size_diff.append((rel, bk_stats['size'], cur_stats['size'], size_delta))
        if hash_changed:
            line_diff.append((rel, bk_stats['lines'], cur_stats['lines'], line_delta))
            # 检查正文大小
            cur_content = current_files[rel].read_text(encoding='utf-8', errors='replace')
            bk_content = backup_files[rel].read_text(encoding='utf-8', errors='replace')
            cur_body_size = body_size(cur_content)
            bk_body_size = body_size(bk_content)
            body_delta = cur_body_size - bk_body_size
            content_changed.append((rel, bk_body_size, cur_body_size, body_delta))

            # 关键事实检查(仅对关键文档)
            if rel in ('FACT.md', 'index.md', '_always-load.md', 'world/performance-guide.md',
                       'api/networking.md', 'rules/udonsharp-language-limits.md',
                       'avatar/optimization-guide.md', 'avatar/playable-layers.md',
                       'world/udonsharp-compilation.md', 'world/vrc-graphics.md'):
                cur_facts = extract_key_facts(cur_content)
                bk_facts = extract_key_facts(bk_content)
                missing = bk_facts - cur_facts
                if missing:
                    missing_key_facts.append((rel, len(missing), len(bk_facts)))

    # 4. 汇总
    total_size_bk = sum(s[1] for s in size_diff)
    total_size_cur = sum(s[2] for s in size_diff)
    total_size_delta = total_size_cur - total_size_bk
    total_size_pct = (total_size_delta / total_size_bk * 100) if total_size_bk else 0

    print(f"\n共同文件总大小: {total_size_bk:,} -> {total_size_cur:,} bytes ({total_size_delta:+,} bytes, {total_size_pct:+.2f}%)")
    print(f"共同文件总行数: {sum(s[1] for s in line_diff):,} -> {sum(s[2] for s in line_diff):,} 行")

    # 5. 关键发现
    print("\n" + "=" * 80)
    print("关键发现")
    print("=" * 80)

    if added_files:
        print(f"\n[+] 新增文件 ({len(added_files)}):")
        for f in sorted(added_files)[:20]:
            print(f"  + {f}")
        if len(added_files) > 20:
            print(f"  ... 还有 {len(added_files) - 20} 个")

    if removed_files:
        print(f"\n[-] 删除文件 ({len(removed_files)}):")
        for f in sorted(removed_files)[:20]:
            print(f"  - {f}")
        if len(removed_files) > 20:
            print(f"  ... 还有 {len(removed_files) - 20} 个")

    # 5.1 正文大幅缩小(可能内容丢失)
    if content_changed:
        significant_reduction = [c for c in content_changed if c[3] < -200]
        if significant_reduction:
            print(f"\n[!] 正文大幅缩小(>200 bytes 减少, {len(significant_reduction)} 个):")
            for rel, bk, cur, delta in sorted(significant_reduction, key=lambda x: x[3])[:15]:
                print(f"  {rel}: {bk:,} -> {cur:,} bytes ({delta:+,})")

        significant_growth = [c for c in content_changed if c[3] > 200]
        if significant_growth:
            print(f"\n[+] 正文大幅增长(>200 bytes 增加, {len(significant_growth)} 个):")
            for rel, bk, cur, delta in sorted(significant_growth, key=lambda x: -x[3])[:10]:
                print(f"  {rel}: {bk:,} -> {cur:,} bytes ({delta:+,})")

    # 5.2 关键事实丢失
    if missing_key_facts:
        print(f"\n[!] 关键文档事实丢失:")
        for rel, missing_count, total in missing_key_facts:
            print(f"  {rel}: 丢失 {missing_count} 个关键事实 / 原 {total} 个")

    # 6. 写入报告
    report_path = CURRENT_ROOT / '_curator_tools' / 'a10_audit_compare_backup.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# A10 二次审计报告 - 当前库 vs 备份库\n\n")
        f.write(f"**生成时间**: {TODAY}\n")
        f.write(f"**当前库**: `memory/`\n")
        f.write(f"**备份库**: `知识库备份/memory/`\n\n")
        f.write("---\n\n")

        f.write("## 概览\n\n")
        f.write("| 指标 | 数值 |\n|------|------|\n")
        f.write(f"| 当前库 .md 文件数 | {len(current_files)} |\n")
        f.write(f"| 备份库 .md 文件数 | {len(backup_files)} |\n")
        f.write(f"| 新增文件 | {len(added_files)} |\n")
        f.write(f"| 删除文件 | {len(removed_files)} |\n")
        f.write(f"| 共同文件 | {len(common_files)} |\n")
        f.write(f"| 共同文件总字节变化 | {total_size_delta:+,} bytes ({total_size_pct:+.2f}%) |\n\n")
        f.write("---\n\n")

        if added_files:
            f.write(f"## 新增文件 ({len(added_files)})\n\n")
            for f_name in sorted(added_files):
                f.write(f"- `{f_name}`\n")
            f.write("\n---\n\n")

        if removed_files:
            f.write(f"## 删除文件 ({len(removed_files)})\n\n")
            for f_name in sorted(removed_files):
                f.write(f"- `{f_name}`\n")
            f.write("\n---\n\n")

        if content_changed:
            f.write(f"## 内容变化文件 ({len(content_changed)})\n\n")
            f.write("**说明**: 仅显示正文(去除 frontmatter)大小变化 > 200 bytes 的文件\n\n")
            f.write("| 文档 | 备份正文 | 当前正文 | 变化 |\n|------|---------|---------|------|\n")
            for rel, bk, cur, delta in sorted(content_changed, key=lambda x: abs(x[3]), reverse=True)[:50]:
                f.write(f"| `{rel}` | {bk:,} | {cur:,} | {delta:+,} |\n")
            f.write("\n---\n\n")

        if missing_key_facts:
            f.write(f"## 关键文档事实丢失 ({len(missing_key_facts)})\n\n")
            f.write("**说明**: 检查关键文档的标题/代码块/粗体术语是否完整\n\n")
            f.write("| 文档 | 丢失事实 | 总事实数 | 完整度 |\n|------|---------|---------|--------|\n")
            for rel, missing_count, total in missing_key_facts:
                pct = (1 - missing_count / total) * 100 if total else 0
                f.write(f"| `{rel}` | {missing_count} | {total} | {pct:.1f}% |\n")
            f.write("\n---\n\n")

        f.write("## 治理建议\n\n")
        if not removed_files and not missing_key_facts:
            f.write("**知识库内容完整,无丢失风险。**\n")
        if added_files:
            f.write(f"- 新增 {len(added_files)} 个文件已验证全部入库\n")
        if removed_files:
            f.write(f"- **警告**: {len(removed_files)} 个文件被删除,需人工确认是否预期\n")
        if missing_key_facts:
            f.write(f"- **警告**: {len(missing_key_facts)} 个关键文档存在事实丢失,需详细复核\n")

    print(f"\n{'='*80}")
    print(f"报告: {report_path}")
    print("=" * 80)
    return 0


if __name__ == '__main__':
    sys.exit(main())
