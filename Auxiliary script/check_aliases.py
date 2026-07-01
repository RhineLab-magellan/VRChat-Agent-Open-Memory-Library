"""检查实际 aliases 数据"""
import sys
sys.path.insert(0, 'Auxiliary script')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from _fix_common import iter_markdown_files, parse_frontmatter, MEMORY_ROOT
from pathlib import Path
import re

# 找几个文件来检查
samples = [
    'api/audio.md',
    'api/animator.md',
    'api/index.md',
    'avatar/avatar-modding-guide.md',
    'avatar/shader/liltoon/basic-settings.md',
    'world/whitelisted-world-components.md',
]

for s in samples:
    target = MEMORY_ROOT / s.replace('/', '\\')
    if not target.exists():
        print(f'\n[NOT FOUND] {s}')
        continue

    content = target.read_text(encoding='utf-8')
    parsed = parse_frontmatter(content)
    if parsed:
        yaml_dict = parsed[0]
        aliases = yaml_dict.get('aliases', [])
        print(f'\n{s} aliases ({len(aliases)}):')
        for a in aliases:
            print(f'  - {a!r}')
