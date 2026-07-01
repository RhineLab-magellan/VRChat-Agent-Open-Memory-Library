#!/usr/bin/env python3
"""
A13 URL 健康检查脚本
====================
每月自动扫描 memory/ 知识库中所有 .md 文件里的外部 URL,
使用 urllib 检测可达性 + HTTP 状态码 + 301 重定向,
生成 Markdown 格式月度健康报告到 memory/_curator_tools/。
功能要点:
1. 扫描所有 .md(排除 _curator_tools / __pycache__)
2. 提取 markdown 链接 [text](url) 与 frontmatter.source 字段
3. 并发请求(线程池 16) + 单 URL 5s 超时 + 全局 30 分钟超时
4. 分类: 200 / 301 / 4xx / 5xx / 超时错误
5. 输出报告: a13_url_health_report.md(UTF-8)
"""
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

# ==================== 配置 ====================
# 脚本位置: UdonSharpAgent/Auxiliary script/url_health_check.py
# 知识库位置: UdonSharpAgent/memory/
SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parent / 'memory'
TODAY = date.today().isoformat()
EXCLUDE_DIRS = {'_curator_tools', '__pycache__'}

# 报告输出
REPORT_PATH = MEMORY_ROOT / '_curator_tools' / 'a13_url_health_report.md'

# 网络参数
PER_URL_TIMEOUT = 5          # 单 URL 超时(秒)
GLOBAL_TIMEOUT = 30 * 60     # 全局超时(秒)
MAX_WORKERS = 16             # 并发线程数
USER_AGENT = 'KB-URL-Health-Bot/1.0'

# 状态码: stdout 强制 UTF-8(Windows 兼容)
sys.stdout.reconfigure(encoding='utf-8')


# ==================== URL 提取 ====================
MD_LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
SOURCE_FIELD_RE = re.compile(r'^\s*source:\s*(\S+)\s*$', re.MULTILINE)
# 裸 URL(不在 markdown 链接内): 匹配 http(s):// 后跟非空白/控制字符
# 允许括号内字符(Wikipedia 风格,如 https://en.wikipedia.org/wiki/Udon_(food))
# 要求协议后至少 1 个非 / 字符(避免匹配孤立的 https://)
# 排除: 空白 / < > " ` / 中文句末标点
BARE_URL_RE = re.compile(r'(?<!\])\b(https?://[^\s<>"`\u3002\uff0c\uff1b\uff1a][^\s<>"`\u3002\uff0c\uff1b\uff1a]*)')
# 清理 URL 末尾的常见标点
TRAILING_PUNCT_RE = re.compile(r'[\.,;:!?)\]\}`]+$')


def clean_url(url: str) -> str:
    """清理 URL: 去掉锚点 + 末尾标点"""
    # 去掉 # 锚点
    url = url.split('#', 1)[0]
    # 去掉末尾标点(但保留内部括号,如 Wikipedia)
    while True:
        new = TRAILING_PUNCT_RE.sub('', url)
        if new == url:
            break
        url = new
    return url


def is_valid_url(url: str) -> bool:
    """检查 URL 是否合法(基本格式校验)"""
    if not url or len(url) < 10:
        return False
    if not url.startswith(('http://', 'https://')):
        return False
    # 协议后必须有内容
    after_proto = url.split('://', 1)[1]
    if not after_proto or after_proto.startswith('/'):
        # 必须是 host 开头
        return False
    return True


def extract_urls_from_file(filepath: Path) -> list:
    """从单个 .md 文件提取所有外部 URL

    返回: [(url, context, filepath), ...]
        - url: 完整 URL
        - context: 链接文本或 'frontmatter.source' 或 'bare'
        - filepath: 源文件 Path 对象

    去重策略: 文件内去重(同一 URL 只记一次,保留首次出现的 context)
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return []

    urls = []
    seen_in_file = set()  # 文件内已见 URL,避免重复
    # markdown 链接的字符范围,用于避免重复匹配裸 URL
    md_link_spans = []  # [(start, end), ...]

    def _add(url: str, ctx: str):
        url = url.strip()
        if not url or url in seen_in_file:
            return
        clean = clean_url(url)
        if not clean or not is_valid_url(clean):
            return
        seen_in_file.add(clean)
        urls.append((clean, ctx, filepath))

    # 1. markdown 链接 [text](url) - 记录 span,避免裸 URL 重复匹配
    for match in MD_LINK_RE.finditer(content):
        link_text = match.group(1)
        url = match.group(2).strip()
        md_link_spans.append((match.start(), match.end()))
        # 跳过锚点 / 空
        if not url or url.startswith('#'):
            continue
        _add(url, link_text or 'md-link')

    # 2. 裸 URL(纯文本里的 URL) - 排除 markdown 链接内部
    for match in BARE_URL_RE.finditer(content):
        ms, me = match.start(), match.end()
        # 跳过 markdown 链接内部
        if any(s <= ms < e for s, e in md_link_spans):
            continue
        url = match.group(1)
        # 上下文: 取前 30 字符作为 hint
        ctx_start = max(0, ms - 30)
        ctx = content[ctx_start:ms].strip()
        # 去掉 markdown 标签残留
        ctx = re.sub(r'[\[\]\(\)]', '', ctx).strip()
        _add(url, ctx or 'bare')

    # 3. frontmatter source 字段(优先级最高,通常是 source of truth)
    fm_match = FRONTMATTER_RE.match(content)
    if fm_match:
        fm_body = fm_match.group(1)
        for m in SOURCE_FIELD_RE.finditer(fm_body):
            url = m.group(1).strip().strip('"').strip("'")
            _add(url, 'frontmatter.source')

    return urls


def find_all_md_files() -> list:
    """扫描 memory/ 下所有 .md(排除 _curator_tools)"""
    md_files = []
    for path in MEMORY_ROOT.rglob('*.md'):
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        md_files.append(path)
    return sorted(md_files)


# ==================== URL 检测 ====================
def check_url(url: str, timeout: int = PER_URL_TIMEOUT) -> dict:
    """检查 URL 可达性 + 状态码 + 重定向

    返回: dict {url, status, final_url, redirected, error, error_type}
        - status: HTTP 状态码; -1 表示网络/超时错误
        - redirected: bool,是否发生重定向
    """
    result = {
        'url': url,
        'status': -1,
        'final_url': url,
        'redirected': False,
        'error': None,
        'error_type': None,
    }
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        # 不自动跟随重定向以便检测 301
        # 但实际使用 default 跟随,只记 final_url
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result['status'] = response.status
            result['final_url'] = response.url
            result['redirected'] = (response.url != url)
    except urllib.error.HTTPError as e:
        result['status'] = e.code
        result['error'] = f'HTTP {e.code}: {e.reason}'
        result['error_type'] = 'HTTPError'
    except urllib.error.URLError as e:
        result['status'] = -1
        result['error'] = f'URLError: {e.reason}'
        result['error_type'] = 'URLError'
    except TimeoutError:
        result['status'] = -1
        result['error'] = f'请求超时(>{timeout}s)'
        result['error_type'] = 'Timeout'
    except Exception as e:
        result['status'] = -1
        result['error'] = f'{type(e).__name__}: {e}'
        result['error_type'] = type(e).__name__

    return result


# ==================== 分类 ====================
def real_status_category(result: dict) -> str:
    """更精确的分类: 区分 200 OK 与 200 via redirect"""
    if result['status'] == -1:
        return 'timeout'
    if result['status'] == 200 and result['redirected']:
        return 'redirect_200'  # 通过重定向后 200(更新建议)
    if result['status'] == 200:
        return 'ok_200'
    if 300 <= result['status'] < 400:
        return 'redirect_3xx'  # 未跟随,原始就是 3xx
    if 400 <= result['status'] < 500:
        return '4xx'
    if 500 <= result['status'] < 600:
        return '5xx'
    return 'other'


# ==================== 主流程 ====================
def main():
    import time
    start_time = time.time()

    print("=" * 80)
    print("A13 URL Health Check")
    print(f"Date: {TODAY}")
    print("=" * 80)

    # 1. 扫描 .md
    md_files = find_all_md_files()
    print(f"Scanning {len(md_files)} .md files...")

    # 2. 提取 URL(带去重)
    url_to_sources = defaultdict(list)  # url -> [(text, filepath), ...]
    for filepath in md_files:
        try:
            urls = extract_urls_from_file(filepath)
        except Exception as e:
            print(f"  WARN: extract failed for {filepath}: {e}")
            continue
        for url, text, src in urls:
            url_to_sources[url].append((text, src))

    unique_urls = sorted(url_to_sources.keys())
    total_refs = sum(len(v) for v in url_to_sources.values())
    print(f"Found {len(unique_urls)} unique URLs ({total_refs} total references)")

    # 3. 并发检查
    print(f"Checking with {MAX_WORKERS} workers (timeout {PER_URL_TIMEOUT}s/URL)...")
    results = []
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {
            executor.submit(check_url, url, PER_URL_TIMEOUT): url
            for url in unique_urls
        }
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result(timeout=PER_URL_TIMEOUT + 2)
            except Exception as e:
                result = {
                    'url': url,
                    'status': -1,
                    'final_url': url,
                    'redirected': False,
                    'error': f'Executor: {e}',
                    'error_type': 'ExecutorError',
                }
            results.append(result)
            completed += 1
            # 进度
            if completed % 20 == 0 or completed == len(unique_urls):
                elapsed = time.time() - start_time
                if elapsed > GLOBAL_TIMEOUT:
                    print(f"  TIMEOUT! Aborting at {completed}/{len(unique_urls)}")
                    break
                print(f"  [{completed}/{len(unique_urls)}] elapsed={elapsed:.1f}s")
            if time.time() - start_time > GLOBAL_TIMEOUT:
                print(f"  Global timeout reached ({GLOBAL_TIMEOUT}s)")
                break

    # 4. 分类统计
    by_category = defaultdict(list)
    for r in results:
        cat = real_status_category(r)
        by_category[cat].append(r)

    n_ok = len(by_category['ok_200'])
    n_redirect_via_200 = len(by_category['redirect_200'])  # 自动跟随后 200,但原 URL 已重定向
    n_redirect_3xx = len(by_category['redirect_3xx'])
    n_4xx = len(by_category['4xx'])
    n_5xx = len(by_category['5xx'])
    n_timeout = len(by_category['timeout'])
    n_other = len(by_category['other'])

    n_total = len(results)
    pct = lambda n: f"{(n * 100 // n_total) if n_total else 0}%"

    # 5. 失败 URL(>=400 或超时)
    failed = []
    for r in results:
        if r['status'] == -1 or r['status'] >= 400:
            failed.append(r)
    failed.sort(key=lambda r: (r['status'] == -1, -r['status'], r['url']))

    # 6. 301 重定向(只要原始 3xx 或被自动跟随后 200 但 redirected)
    redirected = []
    for r in results:
        if r['redirected'] or (300 <= r['status'] < 400):
            redirected.append(r)
    redirected.sort(key=lambda r: r['url'])

    # 7. 健康 URL(只显示状态 200 且未重定向的前 20)
    healthy = [r for r in results if r['status'] == 200 and not r['redirected']]
    healthy.sort(key=lambda r: r['url'])

    # 8. 生成报告
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("# URL 健康检查报告\n\n")
        f.write(f"> 扫描时间: {TODAY}\n")
        f.write(f"> 扫描文件: {len(md_files)}\n")
        f.write(f"> 唯一 URL: {len(unique_urls)}\n")
        f.write(f"> 总引用数: {total_refs}\n")
        f.write(f"> 全局耗时: {time.time() - start_time:.1f}s\n\n")
        f.write("---\n\n")

        # 摘要表
        f.write("## 摘要\n\n")
        f.write("| 状态 | 数量 | 占比 |\n")
        f.write("|------|------|------|\n")
        f.write(f"| 200 OK (直连) | {n_ok} | {pct(n_ok)} |\n")
        f.write(f"| 200 via 301 (重定向后) | {n_redirect_via_200} | {pct(n_redirect_via_200)} |\n")
        f.write(f"| 3xx 未跟随 | {n_redirect_3xx} | {pct(n_redirect_3xx)} |\n")
        f.write(f"| 4xx 客户端错误 | {n_4xx} | {pct(n_4xx)} |\n")
        f.write(f"| 5xx 服务端错误 | {n_5xx} | {pct(n_5xx)} |\n")
        f.write(f"| 超时/网络错误 | {n_timeout} | {pct(n_timeout)} |\n")
        if n_other:
            f.write(f"| 其他 | {n_other} | {pct(n_other)} |\n")
        f.write(f"| **总计** | **{n_total}** | **100%** |\n\n")
        f.write("---\n\n")

        # 失败 URL
        f.write(f"## 失败 URL({len(failed)} 条,必须修复)\n\n")
        if failed:
            f.write("| URL | 状态 | 错误类型 | 来源文件 |\n")
            f.write("|-----|------|----------|----------|\n")
            for r in failed:
                sources = url_to_sources.get(r['url'], [])
                src_files = sorted(set(str(s[1].relative_to(MEMORY_ROOT)) for s in sources))
                src_str = '<br>'.join(f"`{s}`" for s in src_files[:3])
                if len(src_files) > 3:
                    src_str += f"<br>...+{len(src_files) - 3} more"
                err = r.get('error') or ''
                err_type = r.get('error_type') or 'HTTPError'
                f.write(f"| `{r['url']}` | {r['status']} | {err_type}: {err} | {src_str} |\n")
        else:
            f.write("**无失败 URL。**\n")
        f.write("\n---\n\n")

        # 301 重定向
        f.write(f"## 301 重定向 URL({len(redirected)} 条,建议更新)\n\n")
        if redirected:
            f.write("| 原 URL | 最终 URL | 来源文件 |\n")
            f.write("|--------|----------|----------|\n")
            for r in redirected:
                sources = url_to_sources.get(r['url'], [])
                src_files = sorted(set(str(s[1].relative_to(MEMORY_ROOT)) for s in sources))
                src_str = '<br>'.join(f"`{s}`" for s in src_files[:3])
                if len(src_files) > 3:
                    src_str += f"<br>...+{len(src_files) - 3} more"
                final = r.get('final_url', r['url'])
                if final == r['url']:
                    final = '(未跟随)'
                f.write(f"| `{r['url']}` | `{final}` | {src_str} |\n")
        else:
            f.write("**无重定向 URL。**\n")
        f.write("\n---\n\n")

        # 健康 URL
        f.write(f"## 健康 URL(Top 20,共 {len(healthy)} 条)\n\n")
        if healthy:
            for r in healthy[:20]:
                sources = url_to_sources.get(r['url'], [])
                src_files = sorted(set(str(s[1].relative_to(MEMORY_ROOT)) for s in sources))
                src_str = ', '.join(f"`{s}`" for s in src_files[:2])
                f.write(f"- `{r['url']}` — {src_str}\n")
        else:
            f.write("**无健康 URL。**\n")
        f.write("\n---\n\n")

        # 统计脚注
        f.write("## 扫描参数\n\n")
        f.write(f"- 单 URL 超时: {PER_URL_TIMEOUT}s\n")
        f.write(f"- 全局超时: {GLOBAL_TIMEOUT}s\n")
        f.write(f"- 并发线程: {MAX_WORKERS}\n")
        f.write(f"- User-Agent: `{USER_AGENT}`\n")
        f.write(f"- 排除目录: {sorted(EXCLUDE_DIRS)}\n")

    # 9. 终端输出
    elapsed = time.time() - start_time
    print()
    print("=" * 80)
    print(f"Report saved: {REPORT_PATH}")
    print(f"Total unique URLs: {len(unique_urls)}")
    print(f"  200 OK (direct)  : {n_ok}")
    print(f"  200 via redirect : {n_redirect_via_200}")
    print(f"  3xx              : {n_redirect_3xx}")
    print(f"  4xx (client err) : {n_4xx}")
    print(f"  5xx (server err) : {n_5xx}")
    print(f"  timeout/network  : {n_timeout}")
    print(f"  Failed total     : {len(failed)}")
    print(f"  Redirected total : {len(redirected)}")
    print(f"Elapsed: {elapsed:.1f}s")
    print("=" * 80)

    return 0


if __name__ == '__main__':
    sys.exit(main())
