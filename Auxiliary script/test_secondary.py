import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
from refine_dryrun import has_chinese, make_secondary_alias
from _fix_common import parse_frontmatter
from pathlib import Path
fm = parse_frontmatter(Path('C:/CherryStudio/Agent/UdonSharpAgent/memory/api/api-checker.md').read_text(encoding='utf-8'))[0]
print('title:', fm.get('title'))
print('aliases:', fm.get('aliases'))
print('secondary:', make_secondary_alias(fm))
