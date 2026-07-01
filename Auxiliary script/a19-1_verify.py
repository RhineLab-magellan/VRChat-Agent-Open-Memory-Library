"""A19-1 修复验证脚本"""
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent

files_to_check = [
    ROOT / 'SOUL.md',
    ROOT / 'memory/journal/reviews/2026-07-01_review_a18-v31-publish.md',
    ROOT / 'memory/journal/sessions/2026-07-01_session_a18-v31-publish-plan.md',
    ROOT / 'memory/journal/reviews/RELEASE-NOTES-VS-KB-AUDIT-2026-06-30.md',
]

log = []

# 检查 SOUL.md
soul = files_to_check[0]
soul_content = soul.read_text(encoding='utf-8')
has_lr = 'Last Review' in soul_content or 'last_review' in soul_content
has_ver = 'Version:' in soul_content
log.append(f'[SOUL.md] Last Review: {"OK" if has_lr else "FAIL"}, Version: {"OK" if has_ver else "FAIL"}')

# 检查 3 个 journal 文件
for f in files_to_check[1:]:
    content = f.read_text(encoding='utf-8')
    has_yaml = content.startswith('---')
    has_title = bool(re.search(r'^title:', content[:600], re.MULTILINE))
    has_cat = bool(re.search(r'^category:\s*(\S+)', content[:600], re.MULTILINE))
    has_status = bool(re.search(r'^status:\s*(\S+)', content[:600], re.MULTILINE))
    has_kl = bool(re.search(r'^knowledge_level:', content[:600], re.MULTILINE))
    has_src = bool(re.search(r'^source:', content[:600], re.MULTILINE))
    has_ver2 = bool(re.search(r'^version:', content[:600], re.MULTILINE))
    has_lr2 = bool(re.search(r'^last_review:', content[:600], re.MULTILINE))
    has_conf = bool(re.search(r'^confidence:\s*(\S+)', content[:600], re.MULTILINE))

    cat_match = re.search(r'^category:\s*(\S+)', content[:600], re.MULTILINE)
    cat = cat_match.group(1) if cat_match else 'MISSING'

    status_match = re.search(r'^status:\s*(\S+)', content[:600], re.MULTILINE)
    status = status_match.group(1) if status_match else 'MISSING'

    conf_match = re.search(r'^confidence:\s*(\S+)', content[:600], re.MULTILINE)
    conf = conf_match.group(1) if conf_match else 'MISSING'

    rel = "memory/_curator_tools/a19-1_pre_fix/" + f.name
    log.append(f'[{f.name}]')
    log.append(f'  YAML: {has_yaml}, title: {has_title}, category: {cat}, status: {status}, confidence: {conf}')
    log.append(f'  knowledge_level: {has_kl}, source: {has_src}, version: {has_ver2}, last_review: {has_lr2}')

# 检查 _always-load.md line 268 (T3 误判验证)
af = ROOT / 'memory/_always-load.md'
af_content = af.read_text(encoding='utf-8')
line_268 = af_content.split('\n')[267] if len(af_content.split('\n')) > 267 else 'LINE_268_MISSING'
log.append(f'[_always-load.md line 268]: {line_268}')
log.append(f'  Has "slot-based-parameter-passing" (T3 误判): {"slot-based-parameter-passing" in af_content}')

# 写日志
log_path = ROOT / 'memory/_curator_tools/a19-1_verify.log'
log_path.write_text('\n'.join(log), encoding='utf-8')
print('LOG WRITTEN:', log_path)
print('SIZE:', log_path.stat().st_size, 'bytes')
