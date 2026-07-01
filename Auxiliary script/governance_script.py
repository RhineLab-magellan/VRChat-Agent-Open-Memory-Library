#!/usr/bin/env python3
"""
A5 治理脚本: 死链/孤立扫描
================================
扫描 memory/ 知识库的:
1. 死链(dead links): markdown 链接 / frontmatter.related 指向不存在的文件
2. 孤立文档(orphan docs): 被引=0 且 引=0 的真正孤立文档
3. 长尾文档(tail docs): 被引=0 但 主动引用其它的单向依赖
4. 引用图谱统计: 引用频度 Top/Bottom
"""
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import date

# ==================== 配置 ====================
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'
TODAY = "2026-06-20"
EXCLUDE_DIRS = {'_curator_tools', '__pycache__'}


# ==================== YAML 解析(简化版) ====================
class SimpleYAML:
    @staticmethod
    def extract_frontmatter(content: str) -> tuple:
        m = re.match(r'^---\n(.+?)\n---\n?(.*)', content, re.DOTALL)
        if m:
            return m.group(1), m.group(2)
        return None, content

    @staticmethod
    def parse_related(yaml_text: str) -> list:
        if not yaml_text:
            return []
        m = re.search(r'related:\n((?:\s+-\s+.+\n)+)', yaml_text)
        if not m:
            return []
        rels = re.findall(r'^\s+-\s+(.+?)\s*$', m.group(1), re.MULTILINE)
        # 去除双引号包裹(A6 精修会给含特殊字符的路径加引号)
        cleaned = []
        for r in rels:
            r = r.strip()
            if r.startswith('"') and r.endswith('"'):
                r = r[1:-1]
            elif r.startswith("'") and r.endswith("'"):
                r = r[1:-1]
            cleaned.append(r)
        return cleaned


# ==================== 工具函数 ====================
def find_all_md_files() -> list:
    """扫描 memory/ 下所有 .md(排除 _curator_tools)"""
    md_files = []
    for path in MEMORY_ROOT.rglob('*.md'):
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        md_files.append(path.relative_to(MEMORY_ROOT).as_posix())
    return sorted(md_files)


def normalize_path(target: str, source: str) -> str:
    """规范化链接目标为相对路径(以 memory/ 为根)

    规则:
    1. 协议 URL / 锚点: 跳过(None)
    2. 含 memory/ 前缀: 去掉前缀
    3. 解析策略: 依次尝试(绝对路径,相对路径),哪个存在用哪个
    """
    target = target.replace('\\', '/').strip()
    # 去掉锚点
    target = re.sub(r'\.md#.*$', '.md', target)
    # 协议 URL 不处理
    if target.startswith(('http://', 'https://', '#')):
        return None
    # 绝对路径(以 memory/ 开头)→ 相对路径
    if target.startswith('memory/'):
        target = target[7:]
    # 根绝对路径(以 / 开头)
    if target.startswith('/'):
        target = target.lstrip('/')

    source_dir = str(Path(source).parent)
    if source_dir == '.':
        source_dir = ''

    # 候选路径列表(按优先级)
    candidates = []

    # 1. 显式以 ./ 或 ../ 开头: 仅作为相对路径
    if target.startswith('./') or target.startswith('../'):
        if source_dir:
            base = MEMORY_ROOT / source_dir
        else:
            base = MEMORY_ROOT
        try:
            resolved = (base / target).resolve()
            rel = resolved.relative_to(MEMORY_ROOT.resolve())
            return rel.as_posix()
        except Exception:
            return None

    # 2. 否则: 尝试多个候选
    # 候选 A: 绝对路径(MEMORY_ROOT / target)
    candidates.append(MEMORY_ROOT / target)
    # 候选 B: 相对路径(MEMORY_ROOT / source_dir / target)
    if source_dir:
        candidates.append(MEMORY_ROOT / source_dir / target)
    # 候选 C: 裸名(用于同目录文件,如 FACT.md 在根但被其他文件引用)
    if '/' not in target:
        # 仅尝试 MEMORY_ROOT / target
        pass

    for cand in candidates:
        try:
            resolved = cand.resolve()
            if resolved.exists() and resolved.is_file():
                rel = resolved.relative_to(MEMORY_ROOT.resolve())
                return rel.as_posix()
        except Exception:
            continue

    # 所有候选都不存在,但仍返回最合理的(用于死链记录)
    # 优先返回相对路径版本(更符合用户意图)
    if source_dir:
        return str(Path(source_dir) / target).replace('\\', '/')
    return target


def extract_markdown_links(content: str) -> list:
    """提取所有 markdown 链接 [text](path.md)"""
    return re.findall(r'\[[^\]]*\]\(([^)]+\.md)(?:#[^)]*)?\)', content)


def extract_code_md_refs(content: str) -> list:
    """提取 `path/to/file.md` 形式的引用"""
    return re.findall(r'`([^`]+\.md)`', content)


# ==================== 主扫描 ====================
def main():
    print("=" * 80)
    print("A5 Governance Scan: Dead Links & Orphan Docs")
    print(f"Date: {TODAY}")
    print("=" * 80)

    # 确保输出目录存在(若被误删则自动重建)
    (MEMORY_ROOT / '_curator_tools').mkdir(exist_ok=True)

    # 1. 收集所有 .md 文件
    all_files = find_all_md_files()
    file_set = set(all_files)
    print(f"Total .md files: {len(all_files)}")

    # 2. 初始化引用图谱
    # out_refs[file] = [ref1, ref2, ...]  (该文档引用的其它文件)
    # in_refs[file] = [ref1, ref2, ...]  (引用该文档的其它文件)
    out_refs = defaultdict(list)
    in_refs = defaultdict(list)
    dead_links = []  # (source, target, type, line_no)

    # 3. 扫描每个文件
    for rel_path in all_files:
        filepath = MEMORY_ROOT / rel_path
        content = filepath.read_text(encoding='utf-8')

        # 3.1 frontmatter.related
        yaml_text, _ = SimpleYAML.extract_frontmatter(content)
        related = SimpleYAML.parse_related(yaml_text or '')
        for ref in related:
            normalized = normalize_path(ref, rel_path)
            if normalized is None:
                continue
            if normalized not in file_set:
                dead_links.append((rel_path, ref, 'related', 0))
            else:
                out_refs[rel_path].append(normalized)
                in_refs[normalized].append(rel_path)

        # 3.2 markdown 链接
        for i, line in enumerate(content.split('\n'), 1):
            for m in re.finditer(r'\[[^\]]*\]\(([^)]+\.md)(?:#[^)]*)?\)', line):
                target = m.group(1)
                normalized = normalize_path(target, rel_path)
                if normalized is None:
                    continue
                if normalized not in file_set:
                    dead_links.append((rel_path, target, 'markdown', i))
                else:
                    out_refs[rel_path].append(normalized)
                    in_refs[normalized].append(rel_path)

    # 4. 统计孤立文档
    orphan_docs = []  # 引=0 且 被引=0
    tail_docs = []    # 被引=0 但 主动引用其它
    popular_docs = [] # 被引>5

    for f in all_files:
        in_count = len(set(in_refs.get(f, [])))
        out_count = len(set(out_refs.get(f, [])))
        if in_count == 0 and out_count == 0:
            orphan_docs.append(f)
        elif in_count == 0 and out_count > 0:
            tail_docs.append((f, out_count))
        elif in_count > 5:
            popular_docs.append((f, in_count))

    # 5. 去重 dead_links
    dead_unique = sorted(set(dead_links))

    # 6. 输出报告
    report_path = MEMORY_ROOT / '_curator_tools' / 'a5_governance_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# A5 治理报告(死链 + 孤立文档)\n\n")
        f.write(f"**生成时间**: {TODAY}\n")
        f.write(f"**扫描范围**: memory/ 全库(排除 _curator_tools/)\n")
        f.write(f"**总文档数**: {len(all_files)}\n\n")
        f.write("---\n\n")

        # 概览
        f.write("## 概览\n\n")
        f.write("| 指标 | 数量 |\n|------|------|\n")
        f.write(f"| 总文档数 | {len(all_files)} |\n")
        f.write(f"| 死链数(去重) | {len(dead_unique)} |\n")
        f.write(f"| 真正孤立文档(被引=0 且 引=0) | {len(orphan_docs)} |\n")
        f.write(f"| 长尾文档(被引=0 但 主动引用) | {len(tail_docs)} |\n")
        f.write(f"| 高被引文档(被引>5) | {len(popular_docs)} |\n\n")
        f.write("---\n\n")

        # 死链
        f.write(f"## 死链清单({len(dead_unique)} 条)\n\n")
        if dead_unique:
            f.write("| 源文档 | 死链目标 | 类型 |\n|--------|----------|------|\n")
            for src, tgt, type_, _ in dead_unique[:50]:
                f.write(f"| `{src}` | `{tgt}` | {type_} |\n")
            if len(dead_unique) > 50:
                f.write(f"\n*仅显示前 50 条,完整 {len(dead_unique)} 条见 a5_dead_links_full.md*\n")
        else:
            f.write("**无死链。**\n")
        f.write("\n---\n\n")

        # 真正孤立文档
        f.write(f"## 真正孤立文档({len(orphan_docs)} 个)\n\n")
        f.write("**定义**: 被引=0 且 引=0\n\n")
        if orphan_docs:
            f.write("| # | 文档 | category |\n|---|------|----------|\n")
            for i, doc in enumerate(orphan_docs[:50], 1):
                # 读 frontmatter 获取 category
                content = (MEMORY_ROOT / doc).read_text(encoding='utf-8')
                yaml_text, _ = SimpleYAML.extract_frontmatter(content)
                cat_m = re.search(r'^category:\s*(.+?)\s*$', yaml_text or '', re.MULTILINE)
                cat = cat_m.group(1) if cat_m else '?'
                f.write(f"| {i} | `{doc}` | {cat} |\n")
            if len(orphan_docs) > 50:
                f.write(f"\n*仅显示前 50 个,完整 {len(orphan_docs)} 个见 a5_orphan_full.md*\n")
        else:
            f.write("**无真正孤立文档。**\n")
        f.write("\n---\n\n")

        # 长尾文档
        f.write(f"## 长尾文档({len(tail_docs)} 个,被引=0)\n\n")
        if tail_docs:
            tail_docs.sort(key=lambda x: -x[1])
            f.write("| 文档 | 主动引用数 |\n|------|----------|\n")
            for doc, out_count in tail_docs[:30]:
                f.write(f"| `{doc}` | {out_count} |\n")
        else:
            f.write("**无长尾文档。**\n")
        f.write("\n---\n\n")

        # 高被引文档
        f.write(f"## 高被引文档(Top {min(20, len(popular_docs))})\n\n")
        if popular_docs:
            popular_docs.sort(key=lambda x: -x[1])
            f.write("| 文档 | 被引数 |\n|------|--------|\n")
            for doc, in_count in popular_docs[:20]:
                f.write(f"| `{doc}` | {in_count} |\n")
        else:
            f.write("**无高被引文档。**\n")
        f.write("\n---\n\n")

        # 治理建议
        f.write("## 治理建议\n\n")
        if dead_unique:
            f.write(f"### 🔴 死链({len(dead_unique)} 条)\n\n")
            f.write("- **行动**: 修复或删除死链引用\n")
            f.write("- **优先**: Tier A 核心文档的死链先修\n\n")
        if orphan_docs:
            f.write(f"### 🟡 真正孤立文档({len(orphan_docs)} 个)\n\n")
            f.write("- **行动**: 评估是否有保留价值\n")
            f.write("- **选项**: (1) 建立引用关系 (2) 合并到父文档 (3) 标记 deprecated/archived\n\n")
        if tail_docs:
            f.write(f"### 🟢 长尾文档({len(tail_docs)} 个)\n\n")
            f.write("- **行动**: 评估是否被遗漏引用\n")
            f.write("- **选项**: (1) 添加到相关文档的 related (2) 降低为 archived\n\n")
        if not dead_unique and not orphan_docs and not tail_docs:
            f.write("**知识库健康,无需治理。**\n")

    # 输出详细列表(始终写入,即使数量较少,保证报告是最新的)
    if dead_unique:
        full_dead = MEMORY_ROOT / '_curator_tools' / 'a5_dead_links_full.md'
        with open(full_dead, 'w', encoding='utf-8') as f:
            f.write(f"# A5 死链完整清单\n\n")
            f.write(f"**总数**: {len(dead_unique)} 条\n\n")
            f.write("| 源文档 | 死链目标 | 类型 |\n|--------|----------|------|\n")
            for src, tgt, type_, line in dead_unique:
                f.write(f"| `{src}` | `{tgt}` | {type_} |\n")

    if len(orphan_docs) > 50:
        full_orphan = MEMORY_ROOT / '_curator_tools' / 'a5_orphan_full.md'
        with open(full_orphan, 'w', encoding='utf-8') as f:
            f.write(f"# A5 真正孤立文档完整清单\n\n")
            f.write(f"**总数**: {len(orphan_docs)} 个\n\n")
            f.write("| # | 文档 |\n|---|------|\n")
            for i, doc in enumerate(orphan_docs, 1):
                f.write(f"| {i} | `{doc}` |\n")

    print(f"\n{'='*80}")
    print(f"Report: {report_path}")
    print(f"Dead links (unique): {len(dead_unique)}")
    print(f"Orphan docs: {len(orphan_docs)}")
    print(f"Tail docs: {len(tail_docs)}")
    print(f"Popular docs (>5 refs): {len(popular_docs)}")
    print("=" * 80)

    return 0


if __name__ == '__main__':
    sys.exit(main())
