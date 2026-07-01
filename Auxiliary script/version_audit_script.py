#!/usr/bin/env python3
"""
A13 阶段 4 版本核对脚本
========================
Phase: A13 (Tool Development, Stage 4)
目的: 批量核对所有外部工具的最新 GitHub Release 版本,
      与知识库 frontmatter 中记录的版本号比对,识别过期项。
策略: 通过 GitHub REST API (releases/latest + commits) 拉取信息,
      纯标准库(urllib/json/re)实现,单工具失败不影响全局。
"""
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date

# ==================== 配置 ====================
# 脚本位置: UdonSharpAgent/Auxiliary script/version_audit_script.py
# 知识库位置: UdonSharpAgent/memory/_curator_tools/
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'
REPORT_DIR = MEMORY_ROOT / '_curator_tools'
sys.stdout.reconfigure(encoding='utf-8')
TODAY = "2026-06-21"
EXCLUDE_DIRS = {'_curator_tools', '__pycache__'}

# GitHub API 公共端点(无需 token,限流 60 req/h)
GITHUB_API = "https://api.github.com"
HTTP_TIMEOUT = 10  # 秒
USER_AGENT = "KB-Version-Audit-Bot/1.0"

# 半停滞判定:超过此天数视为停滞(仅供参考)
STALE_DAYS = 365

# ==================== 工具清单 ====================
# (display_name, github_url, kb_claimed_version, repo_alias)
# 顺序: 核心 Avatar 工具 → Shader 工具 → 辅助工具
TOOLS = [
    # 核心 Avatar 工具
    ("Modular Avatar", "https://github.com/bdunderscore/modular-avatar", "1.17.1", "modular-avatar"),
    ("AvatarOptimizer", "https://github.com/anatawa12/AvatarOptimizer", "1.9.14", "AvatarOptimizer"),
    ("VRCFury", "https://github.com/VRCFury/VRCFury", "v1.1341.0", "VRCFury"),
    ("Meshia", "https://github.com/RamType0/Meshia.MeshSimplification", "3.2.0", "Meshia.MeshSimplification"),
    ("MA2BT", "https://github.com/Null-K/MA2BT", "v2.0.2", "MA2BT"),
    ("TexTransTool", "https://github.com/ReinaS-64892/TexTransTool", "v1.0.1", "TexTransTool"),
    ("LAC", "https://github.com/Limitex/avatar-compressor", "v0.8.0", "avatar-compressor"),
    # Shader 工具
    ("lilToon", "https://github.com/lilxyzw/lilToon", "2.3.3", "lilToon"),
    ("ORL Shaders", "https://github.com/orels1/orels-Unity-Shaders", "v7.2.0", "orels-Unity-Shaders"),
    ("UnlitWF", "https://github.com/whiteflare/Unlit_WF_ShaderSuite", "UnlitWF_Shader_20260208", "Unlit_WF_ShaderSuite"),
    ("Graphlit", "https://github.com/z3y/Graphlit", "v2.7.2", "Graphlit"),
    ("AudioLink", "https://github.com/llealloo/audiolink", "v3.1.2", "audiolink"),
    # 辅助工具
    ("VizVid (VVMW)", "https://github.com/JLChnToZ/VVMW", "1.7.5", "VVMW"),
    ("UdonVoiceUtils", "https://github.com/Guribo/UdonVoiceUtils", "5.1.4", "UdonVoiceUtils"),
    ("Sardinal", "https://github.com/ikuko/Sardinal", "v0.9.8", "Sardinal"),
    ("ULocalization", "https://github.com/ikuko/ULocalization", "v0.8.16", "ULocalization"),
    ("VRCLightVolumes", "https://github.com/REDSIM/VRCLightVolumes", "v2.1.3", "VRCLightVolumes"),
    ("EasyQuestSwitch", "https://github.com/vrchat-community/EasyQuestSwitch", "v1.4.0", "EasyQuestSwitch"),
    ("VPM Template", "https://github.com/vrchat-community/template-package", "1.0.0", "template-package"),
    ("VRCX", "https://github.com/vrcx-team/VRCX", "v2026.05.03", "VRCX"),
]


# ==================== 网络层 ====================
def parse_repo(github_url: str) -> tuple:
    """从 GitHub URL 提取 (owner, repo)"""
    m = re.search(r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$', github_url.rstrip('/'))
    if not m:
        return None, None
    return m.group(1), m.group(2)


def http_get_json(url: str) -> dict:
    """HTTP GET 返回 JSON 字典;失败/非200返回 {'error': ...}"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': USER_AGENT,
                'Accept': 'application/vnd.github+json',
            },
        )
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            if resp.status != 200:
                return {'error': f'HTTP {resp.status}'}
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code} {e.reason}'}
    except urllib.error.URLError as e:
        return {'error': f'URL error: {e.reason}'}
    except (TimeoutError, json.JSONDecodeError) as e:
        return {'error': str(e)}
    except Exception as e:  # noqa: BLE001
        return {'error': f'{type(e).__name__}: {e}'}


# ==================== GitHub 数据获取 ====================
def get_latest_release(github_url: str) -> dict:
    """获取最新 release 信息(版本号、发布时间)"""
    owner, repo = parse_repo(github_url)
    if not owner or not repo:
        return {'error': f'Invalid GitHub URL: {github_url}'}
    api_url = f"{GITHUB_API}/repos/{owner}/{repo}/releases/latest"
    data = http_get_json(api_url)
    if 'error' in data:
        return data
    tag = data.get('tag_name') or ''
    published = data.get('published_at') or ''
    return {
        'tag_name': tag,
        'published_at': published,
    }


def get_latest_commit(github_url: str) -> str:
    """获取默认分支最近一次 commit 时间(ISO8601)"""
    owner, repo = parse_repo(github_url)
    if not owner or not repo:
        return ''
    api_url = f"{GITHUB_API}/repos/{owner}/{repo}/commits?per_page=1"
    data = http_get_json(api_url)
    if 'error' in data or not isinstance(data, list) or not data:
        return ''
    return (data[0].get('commit', {}).get('committer', {}) or {}).get('date', '')


# ==================== 比对逻辑 ====================
def normalize_version(v: str) -> str:
    """规范化版本号:去前缀 v,提取数字段(用于粗比较)

    支持格式:
    - 1.17.1
    - v1.17.1
    - v.2.1.3 (VRCFury 等特殊命名)
    - com.vrcfury.vrcfury/1.1341.0 (包名/版本混合)
    - UnlitWF_Shader_20260208 (日期编码)
    - 1.7.0-beta.1 (含 pre-release)
    """
    if not v:
        return ''
    v = v.strip()
    # 优先尝试找 d+.d+... 模式
    m = re.search(r'(\d+(?:\.\d+){1,3})', v)
    return m.group(1) if m else ''


def compare_versions(kb_ver: str, latest_ver: str) -> str:
    """比较两个版本号,返回: latest / same / outdated"""
    if not latest_ver:
        return 'unknown'
    a = normalize_version(kb_ver)
    b = normalize_version(latest_ver)
    if not a:
        return 'unknown'
    if a == b:
        return 'same'
    # 简单按段比较
    try:
        a_parts = [int(x) for x in a.split('.')]
        b_parts = [int(x) for x in b.split('.')]
        # 补齐到等长
        n = max(len(a_parts), len(b_parts))
        a_parts += [0] * (n - len(a_parts))
        b_parts += [0] * (n - len(b_parts))
        if b_parts > a_parts:
            return 'outdated'
        if b_parts < a_parts:
            return 'latest'  # KB 比 GitHub 还新(可能记录的是预发布或本地版本)
        return 'same'
    except ValueError:
        # 包含非数字(如 beta/rc)
        return 'outdated' if a != b else 'same'


def days_since(iso_date: str) -> int:
    """计算距今天数;无效返回 -1"""
    if not iso_date:
        return -1
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', iso_date)
    if not m:
        return -1
    try:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        return (date(2026, 6, 21) - d).days
    except Exception:
        return -1


def status_emoji(diff: str, last_commit: str) -> str:
    """根据差异和活跃度返回状态 emoji"""
    days = days_since(last_commit)
    if diff == 'unknown':
        return '⚠️'
    if diff == 'same':
        if days >= 0 and days > STALE_DAYS:
            return '⚠️'  # 同版本但长期无更新
        return '✅'
    if diff == 'outdated':
        if days >= 0 and days > STALE_DAYS:
            return '⚠️'  # 已过期但项目停滞
        return '🔴'  # 已过期且仍活跃
    if diff == 'latest':
        return '✅'  # KB 比最新还新(本地预发)
    return '⚠️'


# ==================== 主流程 ====================
def audit_one_tool(name: str, url: str, kb_version: str, alias: str) -> dict:
    """核对单个工具"""
    release = get_latest_release(url)
    if 'error' in release:
        return {
            'name': name,
            'url': url,
            'kb_version': kb_version,
            'latest_version': '',
            'diff': 'unknown',
            'last_commit': '',
            'last_commit_days': -1,
            'status': '⚠️',
            'error': release['error'],
        }
    latest_ver = release.get('tag_name', '')
    diff = compare_versions(kb_version, latest_ver)
    last_commit = get_latest_commit(url)
    days = days_since(last_commit)
    return {
        'name': name,
        'url': url,
        'kb_version': kb_version,
        'latest_version': latest_ver,
        'diff': diff,
        'last_commit': last_commit,
        'last_commit_days': days,
        'status': status_emoji(diff, last_commit),
        'error': '',
    }


def build_markdown_report(results: list) -> str:
    """生成 Markdown 报告内容"""
    total = len(results)
    latest_count = sum(1 for r in results if r['diff'] == 'latest' or r['diff'] == 'same')
    outdated_count = sum(1 for r in results if r['diff'] == 'outdated')
    unknown_count = sum(1 for r in results if r['diff'] == 'unknown')
    stale_active = sum(
        1 for r in results
        if r['diff'] == 'same' and r['last_commit_days'] > STALE_DAYS
    )

    lines = []
    lines.append("# A13 工具版本审计报告\n")
    lines.append(f"**生成时间**: {TODAY}\n")
    lines.append(f"**审计工具数**: {total}\n")
    lines.append(f"**数据来源**: GitHub REST API (releases/latest + commits)\n")
    lines.append(f"**判定规则**: 停滞阈值 {STALE_DAYS} 天;版本按 major.minor.patch 段比较\n\n")
    lines.append("---\n\n")

    # 总体概览
    lines.append("## 总体概览\n\n")
    lines.append("| 指标 | 数量 | 占比 |\n|------|------|------|\n")
    lines.append(f"| 总工具数 | {total} | 100% |\n")
    lines.append(f"| 知识库最新或领先(latest/same) | {latest_count} | {latest_count*100//total if total else 0}% |\n")
    lines.append(f"| 已过期(outdated) | {outdated_count} | {outdated_count*100//total if total else 0}% |\n")
    lines.append(f"| 未知(查询失败) | {unknown_count} | {unknown_count*100//total if total else 0}% |\n")
    lines.append(f"| 同版本但已停滞(> {STALE_DAYS} 天) | {stale_active} | - |\n\n")
    lines.append("---\n\n")

    # 详细表
    lines.append("## 详细核对结果\n\n")
    lines.append("| # | 工具名 | 知识库版本 | 最新版本 | 差异 | 上次 Commit | 距今天数 | 状态 |\n")
    lines.append("|---|--------|------------|----------|------|-------------|----------|------|\n")
    for i, r in enumerate(results, 1):
        commit_short = r['last_commit'][:10] if r['last_commit'] else '-'
        days_str = f"{r['last_commit_days']}d" if r['last_commit_days'] >= 0 else '-'
        latest_disp = r['latest_version'] if r['latest_version'] else f"(error: {r['error']})"
        lines.append(
            f"| {i} | {r['name']} | `{r['kb_version']}` | `{latest_disp}` | "
            f"{r['diff']} | {commit_short} | {days_str} | {r['status']} |\n"
        )
    lines.append("\n---\n\n")

    # 分组明细
    lines.append("## 分组明细\n\n")
    outdated = [r for r in results if r['diff'] == 'outdated']
    unknown = [r for r in results if r['diff'] == 'unknown']
    stale = [r for r in results if r['diff'] == 'same' and r['last_commit_days'] > STALE_DAYS]

    if outdated:
        lines.append(f"### 🔴 已过期({len(outdated)} 个)\n\n")
        lines.append("**说明**: 知识库版本低于 GitHub 最新 Release,且项目仍活跃(> 0 天内有 commit)。\n\n")
        lines.append("| 工具 | 知识库 | 最新 | 差距 |\n|------|--------|------|------|\n")
        for r in outdated:
            lines.append(f"| {r['name']} | `{r['kb_version']}` | `{r['latest_version']}` | 见原文 |\n")
        lines.append("\n")
    else:
        lines.append("### ✅ 无过期工具\n\n")

    if unknown:
        lines.append(f"### ⚠️ 查询失败({len(unknown)} 个)\n\n")
        lines.append("| 工具 | GitHub URL | 错误 |\n|------|------------|------|\n")
        for r in unknown:
            lines.append(f"| {r['name']} | {r['url']} | {r['error']} |\n")
        lines.append("\n")

    if stale:
        lines.append(f"### 🟡 已停滞({len(stale)} 个,版本一致但无更新 > {STALE_DAYS} 天)\n\n")
        lines.append("| 工具 | 最后 Commit | 距今 |\n|------|-------------|------|\n")
        for r in stale:
            lines.append(
                f"| {r['name']} | {r['last_commit'][:10]} | {r['last_commit_days']}d |\n"
            )
        lines.append("\n")

    lines.append("---\n\n")

    # 治理建议
    lines.append("## 治理建议\n\n")
    if outdated_count == 0 and unknown_count == 0:
        lines.append("- 知识库所有工具版本均为最新或领先,无需更新。\n")
    else:
        if outdated_count > 0:
            lines.append(f"- **🔴 优先**:更新 {outdated_count} 个过期工具的 frontmatter.version。\n")
        if unknown_count > 0:
            lines.append(f"- **⚠️ 重试**:{unknown_count} 个工具查询失败(GitHub 限流或网络),可稍后重跑。\n")
    if stale_active > 0:
        lines.append(f"- **🟡 评估**::{stale_active} 个工具版本一致但长期无 commit,建议评估是否仍维护。\n")
    lines.append("\n---\n\n")

    # 附录:完整工具清单
    lines.append("## 附录:工具清单\n\n")
    lines.append("| # | 工具名 | 知识库版本 | GitHub 仓库 |\n|---|--------|------------|-------------|\n")
    for i, (name, url, kb_ver, alias) in enumerate(TOOLS, 1):
        lines.append(f"| {i} | {name} | `{kb_ver}` | {url} |\n")
    lines.append("\n")

    return ''.join(lines)


def main():
    print("=" * 80)
    print(f"A13 Version Audit: GitHub Releases 批量核对")
    print(f"Date: {TODAY}")
    print(f"Total tools: {len(TOOLS)}")
    print("=" * 80)

    results = []
    for idx, (name, url, kb_ver, alias) in enumerate(TOOLS, 1):
        print(f"[{idx}/{len(TOOLS)}] Auditing {name} ...", end=' ', flush=True)
        result = audit_one_tool(name, url, kb_ver, alias)
        if result['error']:
            print(f"ERR ({result['error']})")
        else:
            print(
                f"OK: kb={result['kb_version']} -> latest={result['latest_version']} "
                f"({result['diff']}, {result['last_commit_days']}d)"
            )
        results.append(result)

    # 写报告
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / 'a13_version_audit_report.md'
    content = build_markdown_report(results)
    report_path.write_text(content, encoding='utf-8')

    # 汇总
    outdated = sum(1 for r in results if r['diff'] == 'outdated')
    same_or_latest = sum(1 for r in results if r['diff'] in ('same', 'latest'))
    unknown = sum(1 for r in results if r['diff'] == 'unknown')

    print("\n" + "=" * 80)
    print(f"Report saved: {report_path}")
    print(f"Total: {len(results)}")
    print(f"  Up-to-date: {same_or_latest}")
    print(f"  Outdated:   {outdated}")
    print(f"  Unknown:    {unknown}")
    print("=" * 80)

    return 0 if outdated == 0 and unknown == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
