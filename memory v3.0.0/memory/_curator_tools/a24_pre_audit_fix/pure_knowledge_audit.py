#!/usr/bin/env python3
"""
A11 审计 - 纯粹知识覆盖度 + 知识遗漏/描述错误检测
=================================================
对比当前库 vs 备份库 v1.0.0,只关注"纯粹知识"段落(技术概念/机制/参数/API/最佳实践等),
排除:
  - YAML frontmatter
  - 内部 markdown 链接
  - 外部 URL
  - 文件路径标记
  - 日期/版本号
  - 索引块(纯链接列表)
  - "详见 X.md" 类内部引用
  - H1/H2/H3 标题行(只作为锚点)
"""
import re
import sys
import hashlib
import difflib
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# ==================== 配置 ====================
SCRIPT_DIR = Path(__file__).resolve().parent
CURRENT_ROOT = SCRIPT_DIR.parent / 'memory'
BACKUP_ROOT = SCRIPT_DIR.parent / '知识库备份' / 'memory v1.0.0' / 'memory'

EXCLUDE_DIRS = {'_curator_tools', '__pycache__'}
TODAY = datetime.now().strftime('%Y-%m-%d')

# 报告输出位置(用户指定)
REPORT_DIR = SCRIPT_DIR.parent / '特殊Agent提示词'
REPORT_PATH = REPORT_DIR / 'A11_纯粹知识审计_新旧库对比报告.md'

# 排除文件(元数据/审计日志型文档,内容会随时间正常演进)
EXCLUDE_FILES = {
    'FACT.md',                          # 知识库元信息 - 持续追加
    'journal/sessions/2026-06-21_session_a11-pure-knowledge-audit-fix.md',  # 审计记录本身
    'journal/sessions/2026-06-21_session_backup-restore-recovery.md',      # 审计关联的 session
}


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


def remove_frontmatter(content: str) -> str:
    """移除 YAML frontmatter"""
    m = re.match(r'^---\n.+?\n---\n?', content, re.DOTALL)
    if m:
        return content[m.end():]
    return content


# 非纯粹知识内容的过滤正则
NOISE_PATTERNS = [
    # 外部 URL
    (r'https?://[^\s)\]<>"]+', 'URL'),
    # 内部 markdown 链接 [text](path)
    (r'\[([^\]]+)\]\(([^)]+)\)', 'MDLINK'),
    # 纯路径引用 ./foo/bar.md 或 foo/bar.md
    (r'(?<![\w/.])(?:[\w-]+/)+[\w-]+\.md(?:#[\w-]+)?', 'PATHREF'),
    # 表格分隔行 |---|---|
    (r'^\s*\|[\s\-:|]+\|\s*$', 'TABLESEP'),
    # 日期 YYYY-MM-DD / YYYY/MM/DD
    (r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b', 'DATE'),
    # 版本号 v1.2.3 / v1.0
    (r'\bv\d+\.\d+(?:\.\d+)?\b', 'VERSION'),
    # 章节锚点行(以 # 开头)
    (r'^#{1,6}\s+.*$', 'HEADER'),
    # 块引用 > xxx (开箱即用的引用)
    (r'^\s*>\s*', 'QUOTE'),
    # 内部引用 "详见 X" / "见 X 文档" / "参考 X" / "参见 X"
    (r'(?:详见|参见|参考|参阅|参考见|详见见|参照)(?:[^。\n]*?(?:\.md|文档|教程|章节))', 'INTREF'),
    # 工具/脚本路径引用
    (r'Auxiliary script/[\w_/.\-]+\.py', 'SCRIPTPATH'),
    # 单独的 emoji
    (r'[\U0001F300-\U0001FAFF\U00002600-\U000027BF]', 'EMOJI'),
    # 旧版块引用元数据: > Type: / > Confidence: / > Source: / > Last Updated: / > 版本: / > 来源:
    (r'(?:Type|Confidence|Source|Last Updated|Update|Updated|版本|来源|状态|Status|Created|Date|Time)(?:\s*[:：])[^>\n]*', 'LEGACY_META'),
    # SDK 版本元数据(行内)
    (r'SDK\s*Version\s*[:：][^|。\n]*', 'SDK_VER'),
    # Last Verified 元数据
    (r'Last\s*Verified\s*[:：][^|。\n]*', 'LAST_VER'),
    # Reference 占位(空引用)
    (r'Reference\s*[:：]\s*`\s*`', 'REF_EMPTY'),
    # 来源标注
    (r'来源标注\s*[:：][^|。\n]*', 'SOURCE_TAG'),
    # 收录 / 适用水平 / 前置知识 元数据
    (r'收录\s*[:：][^|。\n]*|适用水平\s*[:：][^|。\n]*|前置知识\s*[:：][^|。\n]*|所属域\s*[:：][^|。\n]*|难度\s*[:：][^|。\n]*', 'META_FIELD'),
    # Unity / SDK / 更新: 等摘要元数据
    (r'(?:Unity|SDK|更新|状态|性质|适用|收录)\s*[:：][^|。\n]+', 'SUMMARY_META'),
]


def is_metadata_paragraph(para: str) -> bool:
    """判断段落是否为元数据描述(应被过滤)"""
    # 整段都是 SDK Version / Last Verified / Reference 等元数据
    meta_patterns = [
        r'^\s*SDK\s*Version\s*[:：].*$',
        r'^\s*Last\s*Verified\s*[:：].*$',
        r'^\s*Reference\s*[:：]\s*`\s*`.*$',
        r'^\s*来源标注\s*[:：].*$',
        r'^\s*(?:收录|适用水平|前置知识|所属域|难度|适用水平|状态|分类)\s*[:：].*$',
        r'^\s*本文档为.{0,30}见\s*`?\s*`?.*$',
        r'^\s*二次审计补充.*$',
        r'^\s*Purpose\s*[:：].*$',
        r'^\s*Domain\s*[:：].*$',
        r'^\s*索引日期\s*[:：].*$',
        r'^\s*父级\s*[:：].*$',
        r'^\s*关联底层(?:文档)?\s*[:：].*$',
        r'^\s*关联文档\s*[:：].*$',
        r'^\s*\(?关联[^:]{0,20}\)?\s*[:：].*$',
        r'^\s*原始仓库\s*[:：].*$',
        r'^\s*置信度\s*[:：].*$',
        r'^\s*\*\*状态\*\*\s*[:：].*$',
        r'^\s*\*\*迁移日期\*\*\s*[:：].*$',
        r'^\s*\*\*保留原因\*\*\s*[:：].*$',
        r'^\s*\*\*结论\*\*\s*[:：].*$',
        r'^\s*\*\*免责\*\*\s*[:：].*$',
        r'^\s*\*\*任务范围说明\*\*\s*[:：].*$',
        r'^\s*任务范围说明\s*[:：].*$',
    ]
    for pat in meta_patterns:
        if re.match(pat, para, re.IGNORECASE):
            return True
    return False


def clean_paragraph(para: str) -> str:
    """清洗段落,移除非知识内容"""
    cleaned = para
    for pattern, _ in NOISE_PATTERNS:
        cleaned = re.sub(pattern, ' ', cleaned, flags=re.MULTILINE)
    # 合并多空格
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


def is_empty_list_garbage(para: str) -> bool:
    """判断段落是否为空的列表项垃圾(只有数字/标点的列表)"""
    lines = [l.strip() for l in para.split('\n') if l.strip()]
    if not lines:
        return True
    # 全部是数字/标点列表项
    junk_count = 0
    for line in lines:
        # 匹配 "1." "2." "a." "i." 等
        if re.match(r'^[\s\-\*]?\s*[\da-zA-Z]+[\.\)、]?\s*$', line):
            junk_count += 1
        # 匹配纯数字列表
        elif re.match(r'^[\s\-\*]?\s*\d+[\.\)、]?\s*$', line):
            junk_count += 1
    return junk_count / len(lines) >= 0.6


def is_index_paragraph(para: str) -> bool:
    """判断是否为索引块(纯链接列表 / TOC)"""
    lines = [l.strip() for l in para.split('\n') if l.strip()]
    if not lines or len(lines) < 3:
        return False
    # 至少 70% 是链接项(TOC 形式:`1. [text](#anchor)` 或 `- [text](path)`)
    link_lines = [l for l in lines if '[' in l and '](' in l]
    if len(link_lines) / len(lines) >= 0.7:
        return True
    # 或者每行都很短(< 80 字符)且都是参考资料
    if all(len(l) < 80 for l in lines) and len(lines) >= 3:
        ref_count = sum(1 for l in lines if re.search(r'\(\.\./|\.md#?|http', l))
        if ref_count / len(lines) >= 0.6:
            return True
    return False


def split_paragraphs(content: str) -> list:
    """按空行分块"""
    raw_blocks = re.split(r'\n\s*\n', content)
    result = []
    for block in raw_blocks:
        if block.strip():
            result.append(block)
    return result


def extract_knowledge_paragraphs(content: str) -> list:
    """提取知识段落(已清洗)"""
    body = remove_frontmatter(content)
    paragraphs = split_paragraphs(body)
    knowledge = []
    for para in paragraphs:
        # 跳过元数据段落(整段都是元数据)
        if is_metadata_paragraph(para):
            continue
        # 跳过索引块
        if is_index_paragraph(para):
            continue
        # 跳过空列表垃圾(只有数字/字母编号的列表)
        if is_empty_list_garbage(para):
            continue
        # 跳过纯代码块
        stripped = para.strip()
        if stripped.startswith('```') and stripped.endswith('```'):
            continue
        # 跳过纯表格(每行都是 | 开头)
        lines = stripped.split('\n')
        if lines and all(re.match(r'^\s*\|', l) for l in lines):
            continue
        # 清洗
        cleaned = clean_paragraph(para)
        if len(cleaned) < 20:  # 太短的段落通常是噪音
            continue
        # 再次检查: 清洗后整段都是元数据(SDKV/Last Verified 残留)
        if is_metadata_paragraph(cleaned):
            continue
        knowledge.append(cleaned)
    return knowledge


# ==================== 知识单元哈希 ====================
def paragraph_hash(para: str) -> str:
    """段落的归一化哈希(忽略空格/标点差异)"""
    normalized = re.sub(r'[\s\u3000]+', '', para.lower())
    normalized = re.sub(r'[\s,。、;!?\.\-\(\)\[\]【】,!?]', '', normalized)
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


# ==================== 主分析 ====================
def main():
    print("=" * 80)
    print(f"A11 审计 - 纯粹知识覆盖度 + 知识遗漏/描述错误检测")
    print(f"日期: {TODAY}")
    print(f"当前库: {CURRENT_ROOT}")
    print(f"备份库: {BACKUP_ROOT}")
    print("=" * 80)

    # 0. 验证路径
    if not CURRENT_ROOT.exists():
        print(f"[ERROR] 当前库路径不存在: {CURRENT_ROOT}")
        return 1
    if not BACKUP_ROOT.exists():
        print(f"[ERROR] 备份库路径不存在: {BACKUP_ROOT}")
        return 1

    # 1. 扫描文件
    current_files = find_md_files(CURRENT_ROOT)
    backup_files = find_md_files(BACKUP_ROOT)

    current_set = set(current_files.keys())
    backup_set = set(backup_files.keys())

    added_files = current_set - backup_set
    removed_files = backup_set - current_set
    common_files = current_set & backup_set

    print(f"\n[扫描结果]")
    print(f"  当前库 .md 文件数: {len(current_files)}")
    print(f"  备份库 .md 文件数: {len(backup_files)}")
    print(f"  新增文件: {len(added_files)}")
    print(f"  删除文件: {len(removed_files)}")
    print(f"  共同文件: {len(common_files)}")

    # 2. 逐文件分析
    print(f"\n[逐文件分析 - 知识段落提取]")

    file_analyses = []  # (rel, cur_paras, bk_paras, cur_hashes, bk_hashes)

    for rel in sorted(common_files):
        # 跳过元数据/审计日志型文档
        if rel in EXCLUDE_FILES:
            continue
        cur_content = current_files[rel].read_text(encoding='utf-8', errors='replace')
        bk_content = backup_files[rel].read_text(encoding='utf-8', errors='replace')

        cur_paras = extract_knowledge_paragraphs(cur_content)
        bk_paras = extract_knowledge_paragraphs(bk_content)

        cur_hashes = {paragraph_hash(p): p for p in cur_paras}
        bk_hashes = {paragraph_hash(p): p for p in bk_paras}

        file_analyses.append((rel, cur_paras, bk_paras, cur_hashes, bk_hashes))

    # 3. 全局汇总统计
    total_cur_paras = sum(len(c[1]) for c in file_analyses)
    total_bk_paras = sum(len(c[2]) for c in file_analyses)

    print(f"\n[知识段落总数]")
    print(f"  当前库: {total_cur_paras} 段")
    print(f"  备份库: {total_bk_paras} 段")

    # 4. 知识遗漏检测 + 描述改写检测
    print(f"\n[知识遗漏 + 描述改写检测]")

    missing_knowledge = []  # 真正丢失(best_match 相似度 < 0.4)
    modified_knowledge = []  # 描述改写(0.4 <= 相似度 < 0.95)
    near_duplicate = []  # 近重复(相似度 >= 0.95,通常为格式调整)

    for rel, cur_paras, bk_paras, cur_hashes, bk_hashes in file_analyses:
        # 备份有,当前无 = 可能是遗漏或改写
        for bk_h, bk_p in bk_hashes.items():
            if bk_h in cur_hashes:
                continue  # 规范化后相同,跳过

            # 在当前文件中找最相似的段落
            best_match = None
            best_ratio = 0.0
            for c_h, c_p in cur_hashes.items():
                ratio = difflib.SequenceMatcher(None, bk_p[:300], c_p[:300]).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = c_p

            record = {
                'file': rel,
                'bk_para': bk_p,
                'best_match': best_match,
                'similarity': best_ratio,
            }

            if best_ratio >= 0.95:
                # 近重复:文本基本一致但规范化后不同(可能是格式调整)
                near_duplicate.append(record)
            elif best_ratio >= 0.4:
                # 描述改写:0.4-0.95 相似度 = 可能是合理优化也可能是错误
                modified_knowledge.append(record)
            else:
                # 真正丢失:相似度 < 0.4 = 当前库无相关段落
                missing_knowledge.append(record)

    print(f"  知识遗漏: {len(missing_knowledge)} 处")
    print(f"  描述改写(潜在错误): {len(modified_knowledge)} 处")

    # 5. 按文件聚合
    missing_by_file = defaultdict(list)
    for m in missing_knowledge:
        missing_by_file[m['file']].append(m)

    modified_by_file = defaultdict(list)
    for m in modified_knowledge:
        modified_by_file[m['file']].append(m)

    # 6. 写出报告
    write_report(
        added_files, removed_files, common_files,
        file_analyses, missing_knowledge, modified_knowledge, near_duplicate,
        missing_by_file, modified_by_file,
        total_cur_paras, total_bk_paras
    )

    print(f"\n[报告已生成]")
    print(f"  {REPORT_PATH}")
    return 0


def write_report(added, removed, common, file_analyses,
                 missing, modified, near_dup,
                 missing_by_file, modified_by_file,
                 total_cur, total_bk):
    """生成 Markdown 审计报告"""

    lines = []
    p = lines.append

    p(f"# A11 纯粹知识审计报告 - 新旧库对比")
    p("")
    p(f"**生成时间**: {TODAY}")
    p(f"**当前库**: `memory/`")
    p(f"**备份库**: `知识库备份/memory v1.0.0/memory/`")
    p(f"**审计模式**: 纯粹知识(技术概念/机制/参数/API/最佳实践等)")
    p(f"**审计范围**: 293 个 .md 文件(共同文件 {len(common)} 个)")
    p("")
    p("---")
    p("")

    # 1. 概览
    p("## 1. 概览")
    p("")
    p("| 指标 | 数值 |")
    p("|------|------|")
    p(f"| 当前库 .md 文件数 | {len(common) + len(added)} |")
    p(f"| 备份库 .md 文件数 | {len(common) + len(removed)} |")
    p(f"| 新增文件 | {len(added)} |")
    p(f"| 删除文件 | {len(removed)} |")
    p(f"| 共同文件 | {len(common)} |")
    p(f"| 知识段落(当前库总计) | {total_cur} |")
    p(f"| 知识段落(备份库总计) | {total_bk} |")
    p(f"| **🔴 知识遗漏(相似度 < 0.4)** | **{len(missing)}** |")
    p(f"| **🟡 描述改写(0.4 ≤ 相似度 < 0.95)** | **{len(modified)}** |")
    p(f"| 🟢 近重复(相似度 ≥ 0.95,通常为格式调整) | {len(near_dup)} |")
    p("")
    p("---")
    p("")
    p("### 分类标准")
    p("")
    p("| 类型 | 阈值 | 含义 |")
    p("|------|------|------|")
    p("| 🔴 知识遗漏 | 相似度 < 0.4 | 旧库段落在新库对应文件中**无相关段落**,可能是真的丢失 |")
    p("| 🟡 描述改写 | 0.4 ≤ 相似度 < 0.95 | 旧库段落在新库有**相似但措辞不同**的段落,需要人工核实是否语义保持 |")
    p("| 🟢 近重复 | 相似度 ≥ 0.95 | 文本基本一致,只是格式调整,通常无需处理 |")
    p("")
    p("---")
    p("")

    # 1.1 高风险速查
    p("## 1.1 高风险条目速查")
    p("")
    p("> 优先复核以下条目(相似度最低、知识段落较长)")
    p("")

    # 按相似度排序,优先低相似度的真实长段落
    high_risk = sorted(missing, key=lambda x: (x['similarity'], -len(x['bk_para'])))[:15]
    if high_risk:
        p("| # | 文件 | 相似度 | 旧库段落长度 | 性质 |")
        p("|---|------|--------|------------|------|")
        for idx, m in enumerate(high_risk, 1):
            p(f"| {idx} | `{m['file']}` | {m['similarity']:.2f} | {len(m['bk_para'])} 字 | 详见 §3 |")
    else:
        p("_无_")
    p("")
    p("---")
    p("")

    # 2. 文件级差异
    p("## 2. 文件级差异")
    p("")
    if added:
        p(f"### 2.1 新增文件 ({len(added)})")
        p("")
        p("> 当前库独有,在备份库 v1.0.0 中不存在。可能是新版本新增。")
        p("")
        for f in sorted(added):
            p(f"- `{f}`")
        p("")
    if removed:
        p(f"### 2.2 删除文件 ({len(removed)})")
        p("")
        p("> 备份库 v1.0.0 有,但当前库已删除。")
        p("")
        for f in sorted(removed):
            p(f"- `{f}`")
        p("")
    p("---")
    p("")

    # 3. 知识遗漏清单
    p("## 3. 知识遗漏清单(备份有 / 当前无)")
    p("")
    p("> 旧库存在的知识段落,在新库对应文件中找不到相同或高度相似的段落。")
    p("> 每条记录包含:文件路径、备份原文、当前最相似段落(可能为空)、相似度。")
    p("> ⚠️ 风险等级标记:")
    p("> - 🔴 高风险: 相似度 < 0.2,新库无相关段落,可能是真丢失")
    p("> - 🟡 中风险: 0.2 ≤ 相似度 < 0.4,可能是改写/翻译/重组,需复核")
    p("")

    if not missing:
        p("_未发现知识遗漏。_")
    else:
        # 按文件分组
        for f in sorted(missing_by_file.keys()):
            items = missing_by_file[f]
            p(f"### 3.{sorted(missing_by_file.keys()).index(f) + 1} `{f}`")
            p("")
            p(f"> 本文件 {len(items)} 处知识遗漏")
            p("")

            # 按相似度排序,优先看低相似度的(可能真丢失)
            items_sorted = sorted(items, key=lambda x: x['similarity'])

            for idx, item in enumerate(items_sorted, 1):
                sim = item['similarity']
                level = "🔴" if sim < 0.2 else "🟡" if sim < 0.4 else "🟢"
                p(f"#### 3.{sorted(missing_by_file.keys()).index(f) + 1}.{idx} {level} 相似度 {sim:.2f}")
                p("")
                p(f"**旧库路径**: `知识库备份/memory v1.0.0/memory/{item['file']}`")
                p("")
                p(f"**新库路径**: `memory/{item['file']}`")
                p("")
                p(f"**遗漏内容(旧库原文)**:")
                p("")
                # 限制长度
                content = item['bk_para']
                if len(content) > 800:
                    content = content[:800] + "..."
                p("```")
                p(content)
                p("```")
                p("")
                if item['best_match']:
                    p(f"**当前库最相似段落**(可能为改写后版本,相似度 {sim:.2f}):")
                    p("")
                    match = item['best_match']
                    if len(match) > 500:
                        match = match[:500] + "..."
                    p("```")
                    p(match)
                    p("```")
                else:
                    p("**当前库中无相似段落**")
                p("")
                p("---")
                p("")

    p("")
    p("---")
    p("")

    # 4. 描述改写清单
    p("## 4. 描述改写清单(潜在描述错误)")
    p("")
    p("> 旧库与新库都有相关段落,但文本相似度在 0.4~0.95 之间,可能是:")
    p("> 1. 合理的措辞优化(无需修复)")
    p("> 2. **描述错误**(表述与原意不符,需要核实)")
    p("> 人工核实优先级:低相似度(< 0.75)优先排查。")
    p(">")
    p("> 与「知识遗漏」的区别:本节中的项目都能在新库找到**相关段落**,只是措辞不同。")
    p("> 知识遗漏中的项目在新库中**无相关段落**。")
    p("")

    if not modified:
        p("_未发现描述改写。_")
    else:
        for f in sorted(modified_by_file.keys()):
            items = modified_by_file[f]
            p(f"### 4.{sorted(modified_by_file.keys()).index(f) + 1} `{f}`")
            p("")
            p(f"> 本文件 {len(items)} 处描述改写")
            p("")

            # 按相似度排序,低相似度优先
            items_sorted = sorted(items, key=lambda x: x['similarity'])

            for idx, item in enumerate(items_sorted[:20], 1):  # 每文件最多展示 20 条
                sim = item['similarity']
                level = "🔴" if sim < 0.75 else "🟡" if sim < 0.85 else "🟢"
                p(f"#### 4.{sorted(modified_by_file.keys()).index(f) + 1}.{idx} {level} 相似度 {sim:.2f}")
                p("")
                p(f"**旧库路径**: `知识库备份/memory v1.0.0/memory/{item['file']}`")
                p("")
                p(f"**新库路径**: `memory/{item['file']}`")
                p("")
                p("**旧库原文**:")
                p("")
                bk = item['bk_para']
                if len(bk) > 500:
                    bk = bk[:500] + "..."
                p("```")
                p(bk)
                p("```")
                p("")
                p("**新库现文**:")
                p("")
                cur = item.get('best_match', '')
                if len(cur) > 500:
                    cur = cur[:500] + "..."
                p("```")
                p(cur)
                p("```")
                p("")
                p("---")
                p("")

            if len(items) > 20:
                p(f"_...还有 {len(items) - 20} 处,本报告省略_")
                p("")

    p("")
    p("---")
    p("")

    # 5. 附录:逐文件知识段落统计
    p("## 5. 附录:逐文件知识段落统计")
    p("")
    p("| 文档 | 旧库段数 | 新库段数 | 差值 |")
    p("|------|---------|---------|------|")
    for rel, cur_paras, bk_paras, _, _ in sorted(file_analyses, key=lambda x: x[0]):
        delta = len(cur_paras) - len(bk_paras)
        p(f"| `{rel}` | {len(bk_paras)} | {len(cur_paras)} | {delta:+d} |")
    p("")

    # 6. 治理建议
    p("---")
    p("")
    p("## 6. 治理建议")
    p("")
    if not missing and not modified:
        p("**当前审计未发现显著知识遗漏或描述错误。** 建议下次大版本更新前再次审计。")
    else:
        p(f"### 建议优先级")
        p("")
        p(f"1. **P0 - 高风险遗漏(相似度 < 0.2,{sum(1 for m in missing if m['similarity'] < 0.2)} 条)**")
        p(f"   - 新库无相关段落,可能是真丢失,优先人工核对")
        p(f"   - 详见 §1.1 高风险条目速查")
        p(f"")
        p(f"2. **P0 - 低相似度描述改写(< 0.6,{sum(1 for m in modified if m['similarity'] < 0.6)} 条)**")
        p(f"   - 措辞可能与原意偏差较大,需逐条人工核对")
        p(f"")
        p(f"3. **P1 - 中相似度问题(0.2-0.4 遗漏 + 0.6-0.95 改写)**")
        p(f"   - 可能是翻译/重组/合理优化,选择性复核")
        p(f"")
        p(f"### 审查策略")
        p("")
        p(f"- 本报告**不立即修复**,作为审计记录")
        p(f"- 修复时按 P0 → P1 顺序处理")
        p(f"- 每修复一条,记录到 journal/sessions/ 下")
        p("")

    p("---")
    p("")
    p(f"_报告生成完毕。审计工具: `Auxiliary script/pure_knowledge_audit.py`_")

    # 写文件
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # 摘要写控制台
    print(f"\n  [报告路径] {REPORT_PATH}")
    print(f"  [文件大小] {REPORT_PATH.stat().st_size:,} bytes")
    print(f"  [知识遗漏] {len(missing)} 条 (按文件: {len(missing_by_file)})")
    print(f"  [描述改写] {len(modified)} 条 (按文件: {len(modified_by_file)})")
    print(f"  [近重复] {len(near_dup)} 条")


if __name__ == '__main__':
    sys.exit(main())
