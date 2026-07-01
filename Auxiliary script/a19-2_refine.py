#!/usr/bin/env python3
"""
A19-2 精修脚本 v2:使用 _fix_common 中的正确 YAML 解析器
"""
import json
import os
import re
import sys
from pathlib import Path

# Force UTF-8 output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from _fix_common import (
    parse_frontmatter, build_frontmatter, iter_markdown_files,
    MEMORY_ROOT, CURATOR_TOOLS, has_chinese
)

TOOLS_DIR = CURATOR_TOOLS

PREFIX_PATTERN = re.compile(r"^([a-zA-Z\-_/]+):\s*")


def detect_prefix_variant(aliases):
    """Detect aliases that are 'category: same_text' prefix variants.
    Returns list of (index, alias) to remove.
    """
    removals = []  # (index, reason)

    for i, a in enumerate(aliases):
        stripped = PREFIX_PATTERN.sub("", a).strip()
        if stripped == a:
            # No prefix - check if it has Chinese characters that look like
            # a category prefix; skip
            continue

        # Check if the stripped version exists as another alias
        for j, other in enumerate(aliases):
            if i == j:
                continue
            other_stripped = PREFIX_PATTERN.sub("", other).strip()
            if stripped == other_stripped:
                # Found a prefix variant
                removals.append((i, f"prefix-variant of '{other}'"))
                break

    return removals


def detect_duplicates(aliases):
    """Detect true exact duplicates."""
    seen = {}
    removals = []
    for i, a in enumerate(aliases):
        if a in seen:
            removals.append((i, f"duplicate of index {seen[a]}"))
        else:
            seen[a] = i
    return removals


def refine_aliases(aliases):
    """Refine aliases. Return (new_aliases, action, reason)."""
    if not aliases or len(aliases) < 2:
        return aliases, "noop", "ok"

    # Find prefix variants and duplicates
    prefix_to_remove = detect_prefix_variant(aliases)
    duplicates_to_remove = detect_duplicates(aliases)

    if not prefix_to_remove and not duplicates_to_remove:
        return aliases, "noop", "ok"

    # Combine indices to remove
    to_remove = {}
    for i, reason in prefix_to_remove:
        to_remove[i] = f"prefix-variant ({reason})"
    for i, reason in duplicates_to_remove:
        to_remove[i] = f"duplicate ({reason})"

    # Build new list
    new_aliases = []
    actions = []
    for i, a in enumerate(aliases):
        if i in to_remove:
            actions.append(f"removed '{a}' ({to_remove[i]})")
            continue
        new_aliases.append(a)

    if new_aliases != aliases:
        return new_aliases, "refined", "; ".join(actions)
    return aliases, "noop", "ok"


def refine_related(related, file_dir):
    """Refine related. Remove dead links. Return (new_related, action, reason)."""
    if not related or len(related) < 1:
        return related, "noop", "ok"

    new_related = []
    actions = []
    for r in related:
        # Try resolving relative to file_dir
        candidates = [
            file_dir / r,
            file_dir / ".." / r,
        ]
        # Also try relative to MEMORY_ROOT (in case related is absolute from KB root)
        candidates.append(MEMORY_ROOT / r)
        # Try with .md suffix
        if not r.endswith(".md"):
            for c in [file_dir / r, file_dir / ".." / r, MEMORY_ROOT / r]:
                candidates.append(c.with_suffix(".md"))

        found = False
        for cand in candidates:
            try:
                if cand.exists() and cand.is_file():
                    found = True
                    break
            except Exception:
                continue

        if found:
            new_related.append(r)
        else:
            actions.append(f"removed dead link '{r}'")

    if actions:
        return new_related, "refined", "; ".join(actions)
    return related, "noop", "ok"


def main():
    # Load reports
    with open(TOOLS_DIR / "a19-2_fix_aliases_report.json", "r", encoding="utf-8") as f:
        aliases_report = json.load(f)
    with open(TOOLS_DIR / "a19-2_fix_related_report.json", "r", encoding="utf-8") as f:
        related_report = json.load(f)
    with open(TOOLS_DIR / "a19-2_refine_shader_source_type_report.json", "r", encoding="utf-8") as f:
        shader_report = json.load(f)

    # Collect all modified files (union of three reports)
    all_files = {}  # file -> {"types": set, "info": dict}
    for entry in aliases_report["details"]:
        if entry["status"] == "FIXED":
            f = entry["file"].replace("\\", "/")
            all_files.setdefault(f, {"types": set(), "notes": {}})["types"].add("aliases")
            all_files[f]["notes"]["aliases"] = entry.get("note", "")
    for entry in related_report["details"]:
        if entry["status"] == "FIXED":
            f = entry["file"].replace("\\", "/")
            all_files.setdefault(f, {"types": set(), "notes": {}})["types"].add("related")
            all_files[f]["notes"]["related"] = entry.get("note", "")
    for entry in shader_report["details"]:
        if entry["status"] == "FIXED":
            f = entry["file"].replace("\\", "/")
            all_files.setdefault(f, {"types": set(), "notes": {}})["types"].add("shader")
            all_files[f]["notes"]["shader"] = entry.get("note", "")

    print(f"Total files to check: {len(all_files)}")

    results = []
    files_modified = 0
    ratings = {"A": 0, "B": 0, "C": 0}

    for rel_path in sorted(all_files.keys()):
        file_types = all_files[rel_path]["types"]
        file_path = MEMORY_ROOT / rel_path
        if not file_path.exists():
            print(f"  [SKIP] {rel_path}: file not found")
            continue

        content = file_path.read_text(encoding="utf-8")
        parsed = parse_frontmatter(content)
        if not parsed:
            print(f"  [SKIP] {rel_path}: frontmatter parse failed")
            continue

        yaml_dict, fm_text, body = parsed

        file_rating = "A"
        file_actions = []

        # 1. Refine aliases
        if "aliases" in yaml_dict and isinstance(yaml_dict["aliases"], list):
            new_aliases, action, reason = refine_aliases(yaml_dict["aliases"])
            if action == "refined":
                file_rating = "B"
                file_actions.append(f"aliases: {reason}")
                yaml_dict["aliases"] = new_aliases

        # 2. Refine related
        if "related" in yaml_dict and isinstance(yaml_dict["related"], list):
            file_dir = file_path.parent
            new_related, action, reason = refine_related(yaml_dict["related"], file_dir)
            if action == "refined":
                file_rating = "B"
                file_actions.append(f"related: {reason}")
                yaml_dict["related"] = new_related

        # 3. Shader source_type - just check current state matches
        # (no action - just verify it exists)

        if file_actions:
            new_frontmatter = build_frontmatter(yaml_dict)
            new_content = new_frontmatter + body
            file_path.write_text(new_content, encoding="utf-8")
            files_modified += 1
            print(f"  [{file_rating}] {rel_path}: {'; '.join(file_actions)}")
        else:
            print(f"  [A] {rel_path}: no changes needed")

        ratings[file_rating] += 1
        results.append({
            "file": rel_path,
            "rating": file_rating,
            "types": sorted(file_types),
            "actions": file_actions
        })

    # Write refinement report
    report_path = TOOLS_DIR / "a19-2_refine_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# A19-2 精修报告\n\n")
        f.write("## 摘要\n\n")
        f.write(f"- 总检查文件: {len(all_files)}\n")
        f.write(f"- A 评级(可接受): {ratings['A']}\n")
        f.write(f"- B 评级(已精修): {ratings['B']}\n")
        f.write(f"- C 评级(已还原): {ratings['C']}\n")
        f.write(f"- 修改文件数: {files_modified}\n\n")
        f.write("## 详情\n\n")
        f.write("| 文件 | 类型 | 评级 | 原因/修改 |\n")
        f.write("|------|------|------|----------|\n")
        for r in results:
            types = "+".join(r["types"])
            actions = "; ".join(r["actions"]) if r["actions"] else "OK"
            f.write(f"| `{r['file']}` | {types} | {r['rating']} | {actions} |\n")

    print(f"\nReport written to {report_path}")
    print(f"Summary: A={ratings['A']}, B={ratings['B']}, C={ratings['C']}, modified={files_modified}")


if __name__ == "__main__":
    main()
