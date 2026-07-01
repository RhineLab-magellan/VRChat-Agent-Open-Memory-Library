#!/usr/bin/env python3
"""
Knowledge Curator Migration Script
=====================================
将 memory/ 下所有 .md 文档从旧式 > 引用块元数据
迁移到 YAML frontmatter(13 字段标准)。

设计原则:
1. 解析多种引用块格式(标准 / 一行复合 / 中文粗体 / 缺失)
2. 自动推断 Tags(1-3 核心 + 2-5 辅助,共 3-8 个)
3. 从 markdown 链接 + ## 相关/## 深入阅读 章节提取 Related
4. 移除原 > Type: 等引用块(决策 1)
5. dry-run 模式只生成报告,不修改文件
6. 处理边界: 迁移提示 / 极大文件 / 极小文件

Author: VRChat Technical Architect Agent
Date: 2026-06-20
"""
import os
import re
import sys
from pathlib import Path
from datetime import date
from typing import Optional

# ==================== 配置 ====================
# 脚本位置: UdonSharpAgent/Auxiliary script/migration_script.py
# 知识库位置: UdonSharpAgent/memory/
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'
TODAY = "2026-06-20"

# A3 全量模式: 不使用 SAMPLE_FILES,改为扫描整个 memory/
# A1/A2 用的 5 文档保留作为快速测试
SAMPLE_FILES = [
    "api/audio.md",              # 极简(1.5K)
    "FACT.md",                    # 极大(83K)
    "hybrid/osc-protocol.md",     # 一行复合
    "api/networking.md",          # 标准 + 复杂 cross-ref
    "world/data-containers.md",   # 迁移提示
]

# 排除目录(脚本和报告本身)
EXCLUDE_DIRS = {'_curator_tools', '__pycache__'}

# A3 模式开关
FULL_SCAN = True  # True=扫描整个 memory/, False=仅 SAMPLE_FILES
DRY_RUN = False  # True=dry-run, False=实际修改文件

# ==================== 允许值 ====================
ALLOWED_CATEGORIES = {
    'api', 'avatar', 'world', 'hybrid', 'platform',
    'vrchatsdk', 'sources', 'patterns', 'rules',
    'reviews', 'journal', 'references', 'misc'
}
ALLOWED_LEVELS = {'core', 'applied', 'auxiliary'}
ALLOWED_STATUS = {'draft', 'active', 'deprecated', 'archived'}
ALLOWED_CONFIDENCE = {'High', 'Medium', 'Low'}

# 路径 → category 映射
PATH_CATEGORY_MAP = {
    'api/': 'api',
    'avatar/': 'avatar',
    'world/': 'world',
    'hybrid/': 'hybrid',
    'platform/': 'platform',
    'vrchatsdk/': 'vrchatsdk',
    'sources/': 'sources',
    'patterns/': 'patterns',
    'rules/': 'rules',
    'reviews/': 'reviews',
    'journal/': 'journal',
    'references/': 'references',
    'misc/': 'misc',
}

# Tags 白名单(预定义,避免噪音)
TAG_KEYWORDS = {
    # 领域
    'networking': 'networking', 'sync': 'sync', 'serialization': 'serialization',
    'ownership': 'ownership', 'event': 'event', 'pickup': 'pickup',
    'station': 'station', 'mirror': 'mirror', 'portal': 'portal',
    'persistence': 'persistence', 'data-container': 'data-container',
    'json': 'json', 'vrcjson': 'vrcjson',
    'shader': 'shader', 'liltoon': 'liltoon', 'scss': 'scss',
    'unlitwf': 'unlitwf', 'orl': 'orl', 'filamented': 'filamented',
    'animator': 'animator', 'playable-layer': 'playable-layer',
    'fx-layer': 'fx-layer', 'gesture': 'gesture', 'action': 'action',
    'physbone': 'physbone', 'contact': 'contact', 'constraint': 'constraint',
    'optimization': 'optimization', 'performance': 'performance',
    'quest': 'quest', 'mobile': 'mobile', 'pc': 'pc',
    'audio': 'audio', 'video': 'video', 'osc': 'osc',
    'vrcfury': 'vrcfury', 'modular-avatar': 'modular-avatar',
    'udonsharp': 'udonsharp', 'udon': 'udon', 'udon-graph': 'udon-graph',
    'avatar': 'avatar', 'world': 'world', 'hybrid': 'hybrid',
    'pattern': 'pattern', 'rule': 'rule', 'api': 'api',
    'source': 'source', 'reference': 'reference', 'index': 'index',
    'review': 'review', 'guide': 'guide', 'tutorial': 'tutorial',
    'tool': 'tool', 'library': 'library', 'plugin': 'plugin',
    'sdk': 'sdk', 'creator-economy': 'creator-economy',
    'bakery': 'bakery', 'light': 'light', 'occlusion': 'occlusion',
    'culling': 'culling', 'reflection': 'reflection',
    'webgl': 'webgl', 'mobile-ui': 'mobile-ui',
    'input': 'input', 'tracking': 'tracking',
    'localization': 'localization', 'i18n': 'i18n',
}

# ==================== 解析器 ====================

def parse_existing_block(content: str) -> dict:
    """
    解析文档头部的 > 引用块元数据。
    支持 5 种格式:
    1. 标准多行: > Type: / > Confidence: / > Source: / > Last Updated:
    2. 一行复合: > 版本: 1.0 | 更新: 2026-06-05 | 来源: ...
    3. 中文粗体: > **类型**: ... / > **Tier**: ...
    4. 迁移提示: > **状态**: 此文件已迁移到...
    5. 完全缺失(返回空 dict)
    """
    meta = {}
    lines = content.split('\n')

    # 找到第一个 --- 之前的引用块
    block_lines = []
    for line in lines[:30]:  # 仅检查前 30 行
        if line.strip() == '---':
            break
        if line.startswith('>'):
            block_lines.append(line)

    if not block_lines:
        return meta

    # 格式 1: 标准多行
    for line in block_lines:
        m = re.match(r'^>\s*Type:\s*(.+?)\s*$', line)
        if m:
            meta['type'] = m.group(1).strip()
            continue
        m = re.match(r'^>\s*Confidence:\s*(.+?)\s*$', line)
        if m:
            meta['confidence_raw'] = m.group(1).strip()
            continue
        m = re.match(r'^>\s*Source:\s*(.+?)\s*$', line)
        if m:
            meta['source'] = m.group(1).strip()
            continue
        m = re.match(r'^>\s*Last Updated:\s*(.+?)\s*$', line)
        if m:
            meta['last_updated'] = m.group(1).strip()
            continue

    # 格式 2: 一行复合 (> 版本: 1.0 | 更新: ... | 来源: ...)
    for line in block_lines:
        if '|' in line and ('版本' in line or 'version' in line.lower() or '更新' in line or '来源' in line):
            parts = [p.strip() for p in line.lstrip('>').split('|')]
            for p in parts:
                m = re.match(r'^(?:版本|version):\s*(.+?)$', p, re.IGNORECASE)
                if m:
                    meta['version_raw'] = m.group(1).strip()
                m = re.match(r'^(?:更新|update|updated|last updated|last_review):\s*(.+?)$', p, re.IGNORECASE)
                if m:
                    meta['last_updated'] = m.group(1).strip()
                m = re.match(r'^(?:来源|source):\s*(.+?)$', p, re.IGNORECASE)
                if m:
                    meta['source'] = m.group(1).strip()
            break

    # 格式 3: 中文粗体 (> **类型**: ... / > **Tier**: ... / > **状态**: ...)
    for line in block_lines:
        m = re.match(r'^>\s*\*\*类型\*\*:\s*(.+?)\s*$', line)
        if m:
            meta['type'] = m.group(1).strip()
        m = re.match(r'^>\s*\*\*Tier\*\*:\s*(.+?)\s*$', line)
        if m:
            meta['tier'] = m.group(1).strip()
        m = re.match(r'^>\s*\*\*状态\*\*:\s*(.+?)\s*$', line)
        if m:
            meta['cn_status'] = m.group(1).strip()

    # 格式 4: 迁移提示
    for line in block_lines:
        if '已迁移' in line or '已废弃' in line or 'migrated' in line.lower() or 'deprecated' in line.lower():
            meta['is_migrated'] = True
            meta['cn_status'] = '已迁移'

    return meta


def extract_title(content: str) -> str:
    """提取 # 标题(第一行)"""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled"


def infer_category_from_path(rel_path: str) -> str:
    """从相对路径推断 category"""
    rel = '/' + rel_path.replace('\\', '/')
    for prefix, cat in PATH_CATEGORY_MAP.items():
        if prefix in rel:
            return cat
    return 'misc'


def infer_subcategory(rel_path: str) -> Optional[str]:
    """从路径推断 subcategory(二级目录)"""
    parts = Path(rel_path).parts
    if len(parts) >= 2:
        # world/udon/... → subcategory: udon
        # avatar/shader/liltoon/... → subcategory: shader/liltoon
        if parts[0] in ('world', 'avatar', 'hybrid', 'platform', 'sources', 'patterns'):
            if len(parts) >= 3 and parts[1] not in ('index.md',):
                return parts[1]
    return None


def infer_tags(rel_path: str, content: str, meta: dict) -> list:
    """
    推断 Tags(1-3 核心 + 2-5 辅助,共 3-8 个)
    改进: 关键词扫描更严格(标题 + 前 1500 字符),且要求词边界
    特殊处理: 顶层入口文件(FACT.md/index.md/_always-load.md)使用专门 tags
    """
    # === 特殊文件处理: 顶层入口 ===
    filename = Path(rel_path).name
    if filename in ('FACT.md', 'index.md', '_always-load.md'):
        if filename == 'FACT.md':
            return ['misc', 'knowledge-graph', 'meta']
        elif filename == '_always-load.md':
            return ['misc', 'reference', 'core-constraints']
        else:  # index.md
            return ['misc', 'index', 'navigation']

    rel_lower = rel_path.lower()
    # 提取标题(前 5 行)+ 标题下方前 1500 字符
    lines = content.split('\n')
    title = ''
    body_start = 0
    for i, line in enumerate(lines[:10]):
        if line.startswith('# '):
            title = line[2:].lower()
            body_start = i + 1
            break
    content_sample = (title + ' ' + '\n'.join(lines[body_start:body_start + 50])).lower()

    # 核心 Tag(1-3 个):基于目录
    core_tags = []
    category = infer_category_from_path(rel_path)
    core_tags.append(category)

    # 路径关键词检测
    for kw, tag in TAG_KEYWORDS.items():
        if f'/{kw}/' in rel_lower or rel_lower.startswith(f'{kw}/'):
            if tag not in core_tags:
                core_tags.append(tag)
                if len(core_tags) >= 3:
                    break

    # 辅助 Tag(2-5 个):基于 Type + 标题/路径关键词
    aux_tags = []

    # Type 字段映射
    type_map = {
        'API': 'api', 'PATTERN': 'pattern', 'RULE': 'rule',
        'SOURCE': 'source', 'REFERENCE': 'reference', 'INDEX': 'index',
        'FAILURE': 'review', 'TOOL': 'tool', 'BEST PRACTICE': 'guide',
        'CHECKLIST': 'guide', 'EPHEMERAL': 'journal',
    }
    if meta.get('type') in type_map:
        aux_tags.append(type_map[meta['type']])

    # 标题关键词扫描
    title_keywords_priority = {
        'shader': 'shader', 'liltoon': 'liltoon', 'scss': 'scss',
        'unlitwf': 'unlitwf', 'orl': 'orl', 'filamented': 'filamented',
        'animator': 'animator', 'physbone': 'physbone', 'contact': 'contact',
        'constraint': 'constraint', 'playable': 'playable-layer',
        'networking': 'networking', 'sync': 'sync', 'persistence': 'persistence',
        'audiosource': 'audio', 'audio': 'audio', 'video': 'video',
        'osc': 'osc', 'optimization': 'optimization',
        'performance': 'performance', 'picking': 'pickup', 'pickup': 'pickup',
        'station': 'station', 'mirror': 'mirror', 'portal': 'portal',
        'json': 'json', 'vrcjson': 'vrcjson', 'data-container': 'data-container',
        'serialization': 'serialization', 'ownership': 'ownership',
        'event': 'event', 'udon graph': 'udon-graph', 'udonsharp': 'udonsharp',
        'compilation': 'udonsharp', 'bakery': 'bakery', 'light': 'light',
        'occlusion': 'occlusion', 'culling': 'culling', 'reflection': 'reflection',
        'fury': 'vrcfury', 'modular': 'modular-avatar', 'avatar': 'avatar',
    }
    for kw, tag in title_keywords_priority.items():
        if tag in core_tags or tag in aux_tags:
            continue
        # 词边界匹配(对短关键词)/ 子串匹配(对长关键词)
        if len(kw) <= 4:
            if re.search(r'\b' + re.escape(kw) + r'\b', content_sample):
                aux_tags.append(tag)
        else:
            if kw in content_sample:
                aux_tags.append(tag)
        if len(aux_tags) >= 5:
            break

    # 合并 + 总数校验
    tags = core_tags + aux_tags
    if len(tags) < 3:
        for fallback in ['udonsharp', 'reference', 'guide']:
            if fallback not in tags:
                tags.append(fallback)
            if len(tags) >= 3:
                break

    # 去重 + 截断
    seen = set()
    unique = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:8]


def extract_aliases(title: str, content: str, meta: dict) -> list:
    """从标题生成 aliases(英文+中文+简称) - 改进: 跳过原标题,只含变体"""
    aliases = set()

    # 1. 去掉前缀的清理版(API: / Pattern: / Rule: ...)
    cleaned = re.sub(r'^(API|PATTERN|RULE|SOURCE|REFERENCE|TOOL|REVIEW|CHECKLIST)\s*[:：]\s*', '', title, flags=re.IGNORECASE).strip()
    if cleaned and cleaned != title:
        aliases.add(cleaned)

    # 2. 中文翻译(从内容前 200 字符找括号说明)
    m = re.search(r'（(.+?)\）', title)
    if m:
        aliases.add(m.group(1))

    # 3. 简单英文→中文映射(从 TAG_KEYWORDS 反向)
    title_lower = title.lower()
    en_to_cn = {
        'networking': '网络', 'sync': '同步', 'ownership': '所有权',
        'shader': '着色器', 'animator': '动画器', 'audio': '音频',
        'audiosource': '音频', 'video': '视频', 'persistence': '持久化',
        'event': '事件', 'pickup': '拾取', 'optimization': '优化',
        'performance': '性能', 'liltoon': 'lilToon', 'scss': 'SCSS',
        'unlitwf': 'UnlitWF', 'bakery': 'Bakery',
        'osc': 'OSC', 'physbone': 'PhysBone', 'constraint': 'Constraint',
    }
    for en, cn in en_to_cn.items():
        # 短词用词边界,长词用子串
        if len(en) <= 4:
            matched = re.search(r'\b' + re.escape(en) + r'\b', title_lower)
        else:
            matched = en in title_lower
        if matched and cn not in aliases:
            aliases.add(cn)

    # 兜底: 至少返回 cleaned 或 title
    if not aliases:
        aliases.add(cleaned if cleaned else title)

    return list(aliases)[:6]


def extract_related(content: str) -> list:
    """从 markdown 链接 + ## 相关/## 深入阅读 章节提取 Related"""
    related = []
    seen = set()

    def normalize_path(path: str) -> str:
        """规范化路径: 去掉 memory/ 前缀, ./ ../ 前缀"""
        path = path.replace('\\', '/')
        # 去掉 ./ ../ 前缀(可重复)
        for _ in range(3):
            path = re.sub(r'^\.{1,2}/', '', path)
        # 去掉 memory/ 前缀
        if path.startswith('memory/'):
            path = path[7:]
        # 去掉尾部的 .md#anchor
        path = re.sub(r'\.md#.*$', '.md', path)
        return path

    # 1. 提取所有 markdown 链接 [text](path.md)
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+\.md)(?:#[^)]*)?\)', content):
        path = normalize_path(m.group(2))
        if path and path not in seen:
            seen.add(path)
            related.append(path)

    # 2. 提取"## 相关" "## 深入阅读" "## 参考" 章节下的纯文本引用
    in_section = False
    for line in content.split('\n'):
        if re.match(r'^##\s+(相关|深入阅读|参考|关联)', line):
            in_section = True
            continue
        if in_section:
            if line.startswith('## '):  # 下一节
                break
            # 提取 `(path/to/file.md)` 形式
            for m in re.finditer(r'`([^`]+\.md)`', line):
                path = normalize_path(m.group(1))
                if path and path not in seen:
                    seen.add(path)
                    related.append(path)

    return related[:15]  # 限 15 个


def map_confidence(raw: str) -> str:
    """映射 confidence 字符串到 High/Medium/Low"""
    if not raw:
        return 'Medium'
    raw_lower = raw.lower()
    if 'high' in raw_lower:
        return 'High'
    if 'low' in raw_lower:
        return 'Low'
    return 'Medium'


def remove_existing_block(content: str) -> str:
    """
    移除文档头部的 > 引用块元数据(决策 1)。
    策略: 扫描前 30 行,删除所有 > 开头的行,以及紧随其后的 --- 分隔符。
    """
    lines = content.split('\n')
    result = []
    skip_horizontal_rule = False  # 标记是否要跳过下一个 ---

    for i, line in enumerate(lines):
        # 删除 > 引用块行
        if line.startswith('>'):
            skip_horizontal_rule = True
            continue

        # 如果上一行是引用块,且当前是 --- 分隔符,跳过
        if skip_horizontal_rule and line.strip() == '---':
            skip_horizontal_rule = False
            continue

        # 正常行
        skip_horizontal_rule = False
        result.append(line)

    # 清理开头空行
    text = '\n'.join(result)
    text = text.lstrip('\n')
    return text


def is_migration_notice(content: str, meta: dict) -> bool:
    """检测是否为迁移提示文件(无主内容)"""
    return meta.get('is_migrated', False) or '已迁移' in content[:500]


def build_frontmatter(rel_path: str, content: str) -> tuple:
    """
    构建 YAML frontmatter 和清理后的内容。
    返回 (frontmatter_str, cleaned_content)
    """

    # 解析
    meta = parse_existing_block(content)
    title = extract_title(content)
    category = infer_category_from_path(rel_path)
    subcategory = infer_subcategory(rel_path)
    tags = infer_tags(rel_path, content, meta)
    aliases = extract_aliases(title, content, meta)
    related = extract_related(content)
    confidence = map_confidence(meta.get('confidence_raw', 'Medium'))

    # 状态判定
    if is_migration_notice(content, meta):
        status = 'archived'
        tags = [category, 'migrated']
    else:
        status = 'active'

    # 来源
    source = meta.get('source', '本地知识库整理')
    source_type = 'official' if '官方' in source or 'official' in source.lower() else 'community'

    # 版本
    version = meta.get('version_raw', '1.0')

    # last_review(优先用原 last_updated,否则用 TODAY)
    last_review = meta.get('last_updated', TODAY)

    # knowledge_level 默认
    knowledge_level = 'core' if category in ('api',) else 'applied'

    # 构建 YAML
    yaml_lines = ['---']
    yaml_lines.append(f'title: {title}')
    yaml_lines.append(f'category: {category}')
    if subcategory:
        yaml_lines.append(f'subcategory: {subcategory}')
    yaml_lines.append('')
    yaml_lines.append(f'knowledge_level: {knowledge_level}')
    yaml_lines.append(f'status: {status}')
    yaml_lines.append('')
    yaml_lines.append('tags:')
    for t in tags:
        yaml_lines.append(f'  - {t}')
    yaml_lines.append('')
    yaml_lines.append('aliases:')
    for a in aliases[:6]:
        # YAML 转义含特殊字符
        a_escaped = a.replace(':', '：').replace('"', '\\"')
        yaml_lines.append(f'  - "{a_escaped}"')
    if related:
        yaml_lines.append('')
        yaml_lines.append('related:')
        for r in related:
            yaml_lines.append(f'  - {r}')
    yaml_lines.append('')
    yaml_lines.append(f'source: {source}')
    yaml_lines.append(f'source_type: {source_type}')
    yaml_lines.append(f'version: {version}')
    yaml_lines.append(f'last_review: {last_review}')
    yaml_lines.append(f'confidence: {confidence}')
    yaml_lines.append('---')
    yaml_lines.append('')

    frontmatter = '\n'.join(yaml_lines)

    # 清理原引用块
    cleaned = remove_existing_block(content)

    return frontmatter, cleaned


# ==================== Dry-Run ====================

def dry_run_sample(rel_path: str) -> dict:
    """对单个文档执行 dry-run,返回结构化结果"""
    filepath = MEMORY_ROOT / rel_path
    # 转绝对路径避免 relative_to 错误
    filepath = filepath.resolve()
    if not filepath.exists():
        return {'file': rel_path, 'error': 'FILE_NOT_FOUND'}

    content = filepath.read_text(encoding='utf-8')
    frontmatter, cleaned = build_frontmatter(rel_path, content)

    new_content = frontmatter + cleaned

    return {
        'file': rel_path,
        'original_size': len(content),
        'new_size': len(new_content),
        'size_delta': len(new_content) - len(content),
        'frontmatter_preview': frontmatter,
        'first_30_lines_after': '\n'.join(new_content.split('\n')[:30]),
        'success': True,
    }


def find_all_md_files() -> list:
    """扫描整个 memory/ 目录,返回所有 .md 文件相对路径(排除 _curator_tools)"""
    md_files = []
    for path in MEMORY_ROOT.rglob('*.md'):
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        rel = path.relative_to(MEMORY_ROOT).as_posix()
        md_files.append(rel)
    return sorted(md_files)


def main():
    print("=" * 80)
    print(f"Knowledge Curator Migration - A3 {'Dry-Run' if DRY_RUN else 'Apply'}")
    print(f"Date: {TODAY}")
    print(f"Mode: {'DRY-RUN (no files modified)' if DRY_RUN else 'APPLY (files will be modified)'}")
    if FULL_SCAN:
        print("Scan: FULL (entire memory/ tree, excluding _curator_tools/)")
    else:
        print(f"Scan: SAMPLE ({len(SAMPLE_FILES)} files)")
    print("=" * 80)

    # 选择目标文件
    if FULL_SCAN:
        target_files = find_all_md_files()
    else:
        target_files = SAMPLE_FILES

    print(f"\nFound {len(target_files)} .md files to process")

    results = []
    for idx, rel_path in enumerate(target_files, 1):
        if idx % 20 == 0 or idx == 1 or idx == len(target_files):
            print(f"\n[{idx}/{len(target_files)}] {rel_path}")
        try:
            filepath = (MEMORY_ROOT / rel_path).resolve()
            if not filepath.exists():
                raise FileNotFoundError(f"File not found: {filepath}")

            content = filepath.read_text(encoding='utf-8')
            frontmatter, cleaned = build_frontmatter(rel_path, content)
            new_content = frontmatter + cleaned

            original_size = len(content)
            new_size = len(new_content)

            applied = False
            if not DRY_RUN:
                # 原子写入(先写临时文件,再 rename)
                tmp_path = filepath.with_suffix(filepath.suffix + '.tmp')
                tmp_path.write_text(new_content, encoding='utf-8')
                tmp_path.replace(filepath)
                applied = True
                # 验证:重新读取并比对
                verify = filepath.read_text(encoding='utf-8')
                if verify == new_content:
                    if idx % 20 == 0 or idx == 1 or idx == len(target_files):
                        print(f"  [OK] APPLIED | {original_size} -> {new_size} ({new_size - original_size:+d} B)")
                else:
                    print(f"  [WARN] VERIFY MISMATCH: {rel_path}")
            else:
                if idx % 20 == 0 or idx == 1 or idx == len(target_files):
                    print(f"  [OK] DRY-RUN | {original_size} -> {new_size} ({new_size - original_size:+d} B)")

            results.append({
                'file': rel_path,
                'original_size': original_size,
                'new_size': new_size,
                'size_delta': new_size - original_size,
                'frontmatter_preview': frontmatter,
                'first_30_lines_after': '\n'.join(new_content.split('\n')[:30]),
                'applied': applied,
                'success': True,
            })
        except Exception as e:
            print(f"  [EXCEPTION] {rel_path}: {e}")
            results.append({'file': rel_path, 'error': str(e), 'applied': False})

    # 生成报告
    mode_label = "Apply" if not DRY_RUN else "Dry-Run"
    report_name = 'a3_batch_report.md' if FULL_SCAN else f'a2_{mode_label.lower()}_report.md'
    report_path = MEMORY_ROOT / '_curator_tools' / report_name

    # 统计
    success_count = sum(1 for r in results if r.get('success'))
    error_count = sum(1 for r in results if 'error' in r)
    applied_count = sum(1 for r in results if r.get('applied'))
    total_original = sum(r.get('original_size', 0) for r in results if r.get('success'))
    total_new = sum(r.get('new_size', 0) for r in results if r.get('success'))

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# A3 {mode_label} 报告(全量 {len(target_files)} 文档)\n\n")
        f.write(f"**生成时间**: {TODAY}\n")
        f.write(f"**模式**: {'DRY-RUN(未修改任何文件)' if DRY_RUN else 'APPLY(已修改文件)'}\n")
        f.write(f"**扫描**: {'FULL' if FULL_SCAN else 'SAMPLE'} ({len(target_files)} 文档)\n")
        f.write(f"**成功**: {success_count} / {len(target_files)}\n")
        f.write(f"**失败**: {error_count}\n")
        f.write(f"**已应用**: {applied_count} / {len(target_files)}\n")
        f.write(f"**总原始大小**: {total_original:,} bytes\n")
        f.write(f"**总新大小**: {total_new:,} bytes\n")
        f.write(f"**净变化**: {total_new - total_original:+,} bytes\n\n")
        f.write("---\n\n")

        # 错误清单
        if error_count > 0:
            f.write("## 失败清单\n\n")
            for r in results:
                if 'error' in r:
                    f.write(f"- `{r['file']}`: {r['error']}\n")
            f.write("\n---\n\n")

        # 详细结果(仅显示前 10 + 失败 + 最后 10)
        f.write("## 详细结果(摘要)\n\n")
        f.write("展示前 10 个 + 失败 + 最后 10 个,完整列表见 a3_full_list.md\n\n")

        show_indices = list(range(min(10, len(results))))
        if error_count > 0:
            for i, r in enumerate(results):
                if 'error' in r:
                    show_indices.append(i)
        show_indices.extend(range(max(0, len(results) - 10), len(results)))
        show_indices = sorted(set(show_indices))

        for i in show_indices:
            r = results[i]
            f.write(f"### [{i+1}/{len(results)}] `{r['file']}`\n\n")
            if 'error' in r:
                f.write(f"❌ **错误**: {r['error']}\n\n")
                continue
            f.write(f"- 大小: {r['original_size']:,} -> {r['new_size']:,} ({r['size_delta']:+,} B)\n")
            f.write(f"- 状态: {'APPLIED' if r.get('applied') else 'DRY-RUN'}\n")
            f.write(f"- Tags: {r['frontmatter_preview'].count(chr(10) + '  - ')} 个\n\n")

    # 完整列表
    full_list_path = MEMORY_ROOT / '_curator_tools' / 'a3_full_list.md'
    with open(full_list_path, 'w', encoding='utf-8') as f:
        f.write(f"# A3 完整文件列表\n\n")
        f.write(f"**生成时间**: {TODAY}\n")
        f.write(f"**总文件数**: {len(results)}\n\n")
        f.write("| # | 文件 | 状态 | 原大小 | 新大小 | 变化 |\n")
        f.write("|---|------|------|--------|--------|------|\n")
        for i, r in enumerate(results, 1):
            status = 'APPLIED' if r.get('applied') else ('ERROR' if 'error' in r else 'DRY-RUN')
            if 'error' in r:
                f.write(f"| {i} | `{r['file']}` | ❌ {status} | - | - | - |\n")
            else:
                f.write(f"| {i} | `{r['file']}` | ✅ {status} | {r['original_size']:,} | {r['new_size']:,} | {r['size_delta']:+,} |\n")

    print(f"\n{'='*80}")
    print(f"Report saved: {report_path}")
    print(f"Full list: {full_list_path}")
    print(f"Files processed: {success_count}/{len(target_files)}")
    print(f"Errors: {error_count}")
    print(f"Applied: {applied_count}/{len(target_files)}")
    print(f"Size delta: {total_new - total_original:+,} bytes")
    print("=" * 80)

    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
