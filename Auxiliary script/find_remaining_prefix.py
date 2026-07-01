"""查找剩余的 prefix variant aliases"""
import sys
sys.path.insert(0, 'Auxiliary script')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from _fix_common import iter_markdown_files, parse_frontmatter, MEMORY_ROOT
from pathlib import Path

for fp in iter_markdown_files(MEMORY_ROOT):
    content = fp.read_text(encoding='utf-8')
    parsed = parse_frontmatter(content)
    if parsed:
        yaml_dict = parsed[0]
        aliases = yaml_dict.get('aliases', [])
        if not isinstance(aliases, list) or len(aliases) != 2:
            continue
        a, b = str(aliases[0]), str(aliases[1])
        # 检查是否还有 prefix 变体
        for alias in [a, b]:
            if ':' in alias:
                prefix, rest = alias.split(':', 1)
                rest = rest.strip()
                # 检查 rest 是否是另一个 alias
                if rest == a.strip() or rest == b.strip():
                    if alias != rest and len(prefix) <= 20:
                        print(f'{str(fp.relative_to(MEMORY_ROOT))}: {aliases}')
                        break
