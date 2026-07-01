#!/usr/bin/env python3
"""A23 audit: diagnose textmeshpro dead link reported by governance_script."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import re

MEMORY_ROOT = Path('memory')


def normalize_path(target, source):
    target = target.replace('\\', '/').strip()
    target = re.sub(r'\.md#.*$', '.md', target)
    if target.startswith(('http://', 'https://', '#')):
        return None
    if target.startswith('memory/'):
        target = target[7:]
    if target.startswith('/'):
        target = target.lstrip('/')
    source_dir = str(Path(source).parent)
    if source_dir == '.':
        source_dir = ''
    candidates = []
    if target.startswith('./') or target.startswith('../'):
        if source_dir:
            base = MEMORY_ROOT / source_dir
        else:
            base = MEMORY_ROOT
        try:
            resolved = (base / target).resolve()
            rel = resolved.relative_to(MEMORY_ROOT.resolve())
            return rel.as_posix()
        except Exception as e:
            return f"ERROR: {e}"
    candidates.append(MEMORY_ROOT / target)
    if source_dir:
        candidates.append(MEMORY_ROOT / source_dir / target)
    for cand in candidates:
        try:
            resolved = cand.resolve()
            if resolved.exists() and resolved.is_file():
                rel = resolved.relative_to(MEMORY_ROOT.resolve())
                return rel.as_posix()
        except Exception:
            continue
    if source_dir:
        return str(Path(source_dir) / target).replace('\\', '/')
    return target


src = 'world/scene-components/textmeshpro.md'
content = (MEMORY_ROOT / src).read_text(encoding='utf-8')
print(f'=== {src} markdown 链接 ===')
for i, line in enumerate(content.split('\n'), 1):
    for m in re.finditer(r'\[[^\]]*\]\(([^)]+\.md)(?:#[^)]*)?\)', line):
        target = m.group(1)
        norm = normalize_path(target, src)
        resolved = (MEMORY_ROOT / norm) if norm else None
        exists = resolved.exists() if (resolved and not str(resolved).startswith('ERROR')) else False
        print(f'  L{i}: {target} -> {norm} (exists: {exists})')
