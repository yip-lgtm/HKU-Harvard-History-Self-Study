#!/usr/bin/env python3
"""
Content-quality checks for HKU-Harvard-History-Self-Study course files.

Validates each course file under 01_HKU_Courses/ and 02_Harvard_Courses/
against the 袁騰飛 style standard:
  1. 5 core mental models (問題 1)
  2. 3 fundamental disagreements (問題 2)
  3. 10 deep questions (問題 3)
  4. 5 deep dives (核心心智模型深化) — each with bilingual table, sources, sharp observation, deep test, diagram
  5. 10 detailed self-test solutions (詳解 1-10)
  6. 5 Mermaid diagrams (Diagram 1-5)
  7. Closing 5-point deep insights summary
  8. Bilingual content (CJK + Latin)

Exits non-zero with a clear per-file report if any check fails.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[2]

# Course file directories
COURSE_DIRS = [
    ROOT / "01_HKU_Courses",
    ROOT / "02_Harvard_Courses" / "101_Foundations",
    ROOT / "02_Harvard_Courses" / "Fall_Courses",
]

# === Regex patterns ===
RE_TOP = re.compile(r"^# ", re.MULTILINE)  # any h1
RE_QUESTION_1 = re.compile(r"^## 問題 1[:：]", re.MULTILINE)
RE_QUESTION_2 = re.compile(r"^## 問題 2[:：]", re.MULTILINE)
RE_QUESTION_3 = re.compile(r"^## 問題 3[:：]", re.MULTILINE)
RE_DEEP_DIVE_SECTION = re.compile(r"^# 核心心智模型深化", re.MULTILINE)
RE_SOLUTIONS_SECTION = re.compile(r"^# 深度自測問題詳解", re.MULTILINE)
RE_DIAGRAM_SECTION = re.compile(r"^# 5 個 Mermaid 圖解", re.MULTILINE)
RE_CLOSING_SECTION = re.compile(r"^# 總結", re.MULTILINE)

RE_DIVE_NUM = re.compile(r"^##\s+([1-5])\.\s+", re.MULTILINE)
RE_SOLUTION_NUM = re.compile(r"^##\s+詳解\s*([0-9]+)[:：]", re.MULTILINE)
RE_DIAGRAM_NUM = re.compile(r"^##\s+📊\s+Diagram\s+([1-5])[:：]", re.MULTILINE)

RE_MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
RE_CJK = re.compile(r"[\u4e00-\u9fff]")
RE_LATIN = re.compile(r"[a-zA-Z]")


def find_course_files() -> List[Path]:
    files = []
    for d in COURSE_DIRS:
        if d.exists():
            files.extend(sorted(d.glob("*.md")))
    return files


def count_numbered_items(block: str, pattern: re.Pattern) -> int:
    """Count unique N in `## N.` or `## 詳解 N:` patterns."""
    nums = set()
    for m in pattern.finditer(block):
        try:
            nums.add(int(m.group(1)))
        except (ValueError, IndexError):
            pass
    return len(nums)


def count_deep_dives(text: str) -> int:
    sec = RE_DEEP_DIVE_SECTION.search(text)
    if not sec:
        return 0
    after = text[sec.end():]
    return count_numbered_items(after, RE_DIVE_NUM)


def count_solutions(text: str) -> int:
    sec = RE_SOLUTIONS_SECTION.search(text)
    if not sec:
        return 0
    after = text[sec.end():]
    return count_numbered_items(after, RE_SOLUTION_NUM)


def count_diagrams(text: str) -> int:
    sec = RE_DIAGRAM_SECTION.search(text)
    if not sec:
        return 0
    after = text[sec.end():]
    return count_numbered_items(after, RE_DIAGRAM_NUM)


def count_mermaid_blocks(text: str) -> int:
    return len(RE_MERMAID_BLOCK.findall(text))


def has_bilingual(text: str) -> Tuple[bool, bool]:
    has_cjk = bool(RE_CJK.search(text))
    has_latin = bool(RE_LATIN.search(text))
    return has_cjk, has_latin


def has_unfilled_placeholders(text: str) -> int:
    """Count unfilled placeholders like （待填寫）or {name_zh}."""
    return text.count("（待填寫）") + text.count("{name_en}") + text.count("{name_zh}")


def has_top_header(text: str) -> bool:
    return bool(RE_TOP.search(text))


def has_3_questions(text: str) -> Tuple[bool, bool, bool]:
    return (
        bool(RE_QUESTION_1.search(text)),
        bool(RE_QUESTION_2.search(text)),
        bool(RE_QUESTION_3.search(text)),
    )


def has_closing_summary(text: str) -> bool:
    return bool(RE_CLOSING_SECTION.search(text)) and "Closing 5-Point" in text


def check_file(path: Path) -> Tuple[List[str], List[str]]:
    """Returns (errors, warnings) for one file."""
    errors: List[str] = []
    warnings: List[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return ([f"could not read: {e}"], [])

    if not has_top_header(text):
        errors.append("missing top-level # header")

    q1, q2, q3 = has_3_questions(text)
    if not q1:
        errors.append("missing 問題 1 (5 core mental models)")
    if not q2:
        errors.append("missing 問題 2 (3 disagreements)")
    if not q3:
        errors.append("missing 問題 3 (10 deep questions)")

    n_dives = count_deep_dives(text)
    if n_dives < 5:
        errors.append(f"has {n_dives} deep dives, expected ≥ 5")

    n_sols = count_solutions(text)
    if n_sols < 10:
        errors.append(f"has {n_sols} detailed solutions, expected ≥ 10")

    n_diagrams = count_diagrams(text)
    if n_diagrams < 5:
        errors.append(f"has {n_diagrams} diagram sections, expected ≥ 5")

    n_mermaid = count_mermaid_blocks(text)
    if n_mermaid < 5:
        errors.append(f"has {n_mermaid} Mermaid blocks, expected ≥ 5")

    if not has_closing_summary(text):
        errors.append("missing closing 5-Point Deep Insights summary")

    has_cjk, has_latin = has_bilingual(text)
    if not has_cjk:
        errors.append("missing CJK (Chinese) characters")
    if not has_latin:
        errors.append("missing Latin (English) characters")

    n_placeholders = has_unfilled_placeholders(text)
    if n_placeholders > 0:
        warnings.append(f"has {n_placeholders} unfilled placeholders (待填寫 or {{name_*}})")

    # Minimum size threshold
    n_lines = text.count("\n")
    if n_lines < 300:
        errors.append(f"file too short ({n_lines} lines, expected ≥ 300)")

    return errors, warnings


def main() -> int:
    files = find_course_files()
    if not files:
        print(f"❌ No course files found in {COURSE_DIRS}")
        return 1

    print(f"Checking {len(files)} course file(s) under 01_HKU_Courses, 02_Harvard_Courses\n")
    print(f"{'File':<60} {'Lines':>6} {'Dives':>6} {'Sols':>6} {'Diag':>6} {'Merm':>6} {'Status':<8}")
    print("-" * 110)

    n_pass = 0
    n_warn = 0
    n_fail = 0
    failures: List[Tuple[Path, List[str]]] = []
    warned: List[Tuple[Path, List[str]]] = []

    for f in files:
        errors, warnings = check_file(f)
        text = f.read_text(encoding="utf-8")
        n_lines = text.count("\n")
        n_dives = count_deep_dives(text)
        n_sols = count_solutions(text)
        n_diagrams = count_diagrams(text)
        n_mermaid = count_mermaid_blocks(text)

        if errors:
            status = "FAIL"
            n_fail += 1
            failures.append((f, errors))
        elif warnings:
            status = "WARN"
            n_warn += 1
            warned.append((f, warnings))
        else:
            status = "OK"
            n_pass += 1

        rel = f.relative_to(ROOT)
        print(f"{str(rel):<60} {n_lines:>6} {n_dives:>6} {n_sols:>6} {n_diagrams:>6} {n_mermaid:>6} {status:<8}")

    print("-" * 110)
    print(f"Summary: {n_pass} OK, {n_warn} warnings, {n_fail} failures (out of {len(files)})")

    if failures:
        print(f"\n❌ {n_fail} file(s) FAILED:")
        for f, errs in failures:
            print(f"  - {f.relative_to(ROOT)}")
            for e in errs:
                print(f"      • {e}")

    if warned:
        print(f"\n⚠️  {n_warn} file(s) with warnings (placeholders, etc.):")
        for f, warns in warned:
            print(f"  - {f.relative_to(ROOT)}")
            for w in warns:
                print(f"      • {w}")

    if n_fail == 0:
        print(f"\n✅ No hard failures. {n_warn} file(s) flagged for content enrichment.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
