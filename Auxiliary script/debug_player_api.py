"""Debug: 检查 player-api.md"""
import sys
sys.path.insert(0, 'Auxiliary script')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from _fix_common import iter_markdown_files, parse_frontmatter, MEMORY_ROOT
from pathlib import Path

target = MEMORY_ROOT / 'api' / 'player-api.md'
print(f'File: {target}')
print(f'Exists: {target.exists()}')

if target.exists():
    content = target.read_text(encoding='utf-8')
    print(f'Length: {len(content)}')

    parsed = parse_frontmatter(content)
    if parsed:
        yaml_dict = parsed[0]
        aliases = yaml_dict.get('aliases', [])
        print(f'aliases: {aliases}')
        print(f'category: {yaml_dict.get("category")}')
        print(f'title: {yaml_dict.get("title")}')
        print(f'len aliases: {len(aliases)}')

        # 模拟 v4 的判断
        if len(aliases) == 2:
            a, b = str(aliases[0]), str(aliases[1])
            print(f'a: {a!r}')
            print(f'b: {b!r}')
            print(f'has colon in a: {":" in a}')
            print(f'has colon in b: {":" in b}')

            if ':' in b:
                prefix, rest = b.split(':', 1)
                rest = rest.strip()
                print(f'prefix: {prefix!r}, rest: {rest!r}')
                print(f'rest == a.strip(): {rest == a.strip()}')
                print(f'len(prefix) <= 20: {len(prefix) <= 20}')
