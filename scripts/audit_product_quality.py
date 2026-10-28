"""
Automated Curriculum Product Quality & Completeness Audit Script.
Audits the curriculum database, vocabulary definitions, and strategy worksheets
to ensure 100% complete content with zero missing definitions or empty prompts.
"""

import sys
import json
import re
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.packet_builder import build_standalone_strategy_handout
from src.preview_renderer import format_booklet_for_web


def audit_catalog_vocab_completeness(catalog_path: str = "output/catalog.json") -> int:
    """Verifies that 100% of vocabulary entries have non-empty definitions."""
    p = Path(catalog_path)
    if not p.exists():
        print(f"[FAIL] Catalog not found: {catalog_path}")
        return 1

    cat = json.loads(p.read_text(encoding="utf-8"))
    errors = []
    total_vocab = 0

    for s in cat:
        sec_code = s.get("section_code", "?")
        ch_num = s.get("chapter_num", "?")
        for v in s.get("official_vocab", []):
            total_vocab += 1
            word = v.get("word", "").strip()
            defn = (v.get("definition") or "").strip()
            if not word:
                errors.append(f"Ch {ch_num} Sec {sec_code}: Vocabulary item has empty word!")
            elif not defn or len(defn) < 5:
                errors.append(f"Ch {ch_num} Sec {sec_code}: Word '{word}' has missing or empty definition ('{defn}')")

    if errors:
        print(f"[FAIL] Catalog Vocab Audit: Found {len(errors)} missing definitions out of {total_vocab} entries:")
        for err in errors[:10]:
            print(f"  - {err}")
        return len(errors)
    
    print(f"[PASS] Catalog Vocab Audit: All {total_vocab} vocabulary entries have valid, complete definitions.")
    return 0


def audit_vocab_index_completeness(vocab_idx_path: str = "output/vocab_index.json") -> int:
    """Verifies that vocab_index.json contains zero empty definitions."""
    p = Path(vocab_idx_path)
    if not p.exists():
        print(f"[FAIL] Vocab index not found: {vocab_idx_path}")
        return 1

    v_data = json.loads(p.read_text(encoding="utf-8"))
    errors = []
    total_entries = 0

    for ch_key, items in v_data.get("by_chapter", {}).items():
        for v in items:
            total_entries += 1
            word = v.get("word", "")
            defn = (v.get("definition") or "").strip()
            if not defn or len(defn) < 5:
                errors.append(f"Chapter {ch_key}: Word '{word}' has empty definition")

    if errors:
        print(f"[FAIL] Vocab Index Audit: Found {len(errors)} missing definitions out of {total_entries} entries:")
        for err in errors[:10]:
            print(f"  - {err}")
        return len(errors)

    print(f"[PASS] Vocab Index Audit: All {total_entries} entries in by_chapter have valid definitions.")
    return 0


def audit_vocabulary_practice_generation() -> int:
    """Audits vocabulary practice generation across chapters for prompts and scaffolding."""
    cat = json.loads(Path("output/catalog.json").read_text(encoding="utf-8"))
    errors = []

    # Test key sections across chapters
    test_sections = [s for s in cat if s.get("official_vocab")][:10]

    for sec in test_sections:
        sec_code = sec.get("section_code", "?")
        md_p = Path(sec.get("md_file", ""))
        raw_md = md_p.read_text(encoding="utf-8") if md_p.exists() else ""

        handout = build_standalone_strategy_handout(
            section_meta=sec,
            strategy_category="vocab",
            strategy_code="vocab_deep_dive",
            markdown_text=raw_md,
            is_scaffolded=False,
        )

        std_md = handout["student_standard_md"]
        scaf_md = handout["student_scaffolded_md"]

        # Check 1: Standard edition must NOT have Word Bank
        if "Word Bank:" in std_md:
            errors.append(f"Sec {sec_code}: Standard edition contains Word Bank (should be at-level retrieval)")

        # Check 2: Scaffolded edition MUST have Word Bank
        if "Word Bank:" not in scaf_md:
            errors.append(f"Sec {sec_code}: Scaffolded edition missing Word Bank")

        # Check 3: Zero empty colons (orphan colons like ':\n' or ':  \n')
        if re.search(r'__+\s*:\s*(?:\n|$)', std_md) or re.search(r'__+\s*:\s*(?:\n|$)', scaf_md):
            errors.append(f"Sec {sec_code}: Found empty clue line ending with colon!")

        # Check 4: Neither standard nor scaffolded edition should have first-letter giveaways
        if re.search(r'\d+\.\s+[A-Za-z]_+', scaf_md):
            errors.append(f"Sec {sec_code}: Scaffolded edition contains first-letter giveaway on blanks")
        if re.search(r'\d+\.\s+[A-Za-z]_+', std_md):
            errors.append(f"Sec {sec_code}: Standard edition contains first-letter giveaway on blanks")

        # Check 5: Both editions must have clean, unassisted fill-in blanks
        if not re.search(r'\d+\.\s+_{10,}\s*:\s*\S+', scaf_md):
            errors.append(f"Sec {sec_code}: Scaffolded edition missing clean blank lines")
        if not re.search(r'\d+\.\s+_{10,}\s*:\s*\S+', std_md):
            errors.append(f"Sec {sec_code}: Standard edition missing clean blank lines")

        # Check 6: Zero fallback or generic placeholder definitions
        for placeholder in ["Key historical concept", "defined in context", "defined in section reading"]:
            if placeholder.lower() in scaf_md.lower() or placeholder.lower() in std_md.lower():
                errors.append(f"Sec {sec_code}: Found placeholder text '{placeholder}' in vocabulary handout!")

        # Check 7: Badge styling in rendered HTML
        std_html = format_booklet_for_web(std_md)
        scaf_html = format_booklet_for_web(scaf_md)

        if "ws-badge-blue" not in std_html:
            errors.append(f"Sec {sec_code}: Standard edition HTML missing ws-badge-blue")
        if "ws-badge-amber" not in scaf_html:
            errors.append(f"Sec {sec_code}: Scaffolded edition HTML missing ws-badge-amber")
        if "Scaffolded Edition</span>" in scaf_html:
            errors.append(f"Sec {sec_code}: Scaffolded edition contains redundant rectangular badge")

    # Specific check for Proclamation of 1763 in Section 5.1
    sec_51 = next((s for s in cat if str(s.get("section_code")) in ("5.1", "5.1.1", "1.1") and s.get("chapter_num") == 5), None)
    if sec_51:
        h51 = build_standalone_strategy_handout(sec_51, "vocab", "vocab_deep_dive")
        if "forbidding American colonists from settling west" not in h51["student_standard_md"]:
            errors.append("Section 5.1: Standard vocabulary handout missing authentic Proclamation of 1763 definition!")
        if "forbidding American colonists from settling west" not in h51["student_scaffolded_md"]:
            errors.append("Section 5.1: Scaffolded vocabulary handout missing authentic Proclamation of 1763 definition!")

    if errors:
        print(f"[FAIL] Vocabulary Generation Audit: Found {len(errors)} defects:")
        for err in errors:
            print(f"  - {err}")
        return len(errors)

    print(f"[PASS] Vocabulary Generation Audit: Passed for all {len(test_sections)} test sections.")
    return 0


def audit_twr_because_but_so_strategy() -> int:
    """Audits TWR 'Because, But, So' sentence expansion strategy across chapters for prompt cleanliness."""
    cat = json.loads(Path("output/catalog.json").read_text(encoding="utf-8"))
    errors = []

    # Sample sections across diverse chapters
    sample_sections = [
        s for s in cat
        if s.get("chapter_num") in [1, 2, 5, 6, 8]
    ][:12]

    for sec in sample_sections:
        sec_code = sec.get("section_code", "?")
        ch_num = sec.get("chapter_num", "?")
        sec_title = sec.get("title", "")
        md_p = Path(sec.get("md_file", ""))
        raw_md = md_p.read_text(encoding="utf-8") if md_p.exists() else ""

        handout = build_standalone_strategy_handout(
            section_meta=sec,
            strategy_category="twr",
            strategy_code="twr_because_but_so",
            markdown_text=raw_md,
            is_scaffolded=False,
        )

        std_md = handout["student_standard_md"]
        lines = [line.strip() for line in std_md.splitlines() if re.match(r"^\d+\.", line.strip())]

        for item_idx, line in enumerate(lines, 1):
            # Check 1: Must NOT contain "In Section X.X" in question prompt
            if re.search(r"In Section \d+", line, flags=re.IGNORECASE):
                errors.append(f"Ch {ch_num} Sec {sec_code}: Prompt contains redundant 'In Section' prefix: '{line}'")

            # Check 2: Must NOT repeat section title in prompt
            if sec_title and f"({sec_title})" in line:
                errors.append(f"Ch {ch_num} Sec {sec_code}: Prompt contains redundant section title '({sec_title})': '{line}'")

            # Check 3: Sentence stem must start with capital letter
            m = re.match(r"^\d+\.\s+([A-Za-z])", line)
            if m and not m.group(1).isupper():
                errors.append(f"Ch {ch_num} Sec {sec_code}: Prompt stem starts with lowercase letter '{m.group(1)}': '{line}'")

        # Check 4: Rendered HTML must not have orphan dot after solid line
        std_html = format_booklet_for_web(std_md)
        if "ws-solid-line\"></div>." in std_html or "ws-solid-line\"></div>\n." in std_html:
            errors.append(f"Ch {ch_num} Sec {sec_code}: Rendered HTML contains orphan period after solid line!")

    # Specific check for Ch 5 Sec 1.1
    sec_51 = next((s for s in cat if str(s.get("section_code")) in ("5.1", "5.1.1", "1.1") and s.get("chapter_num") == 5), None)
    if sec_51:
        h51 = build_standalone_strategy_handout(sec_51, "twr", "twr_because_but_so")
        md51 = h51["student_standard_md"]
        if "1. Tensions grew between Britain and the colonies **because**" not in md51:
            errors.append("Ch 5 Sec 1.1: Missing authentic capitalized stem 'Tensions grew between Britain and the colonies because'")
        if "In Section 1.1" in md51:
            errors.append("Ch 5 Sec 1.1: Still contains 'In Section 1.1' in prompt text")
        if "(Limits on Freedom)" in md51:
            errors.append("Ch 5 Sec 1.1: Still contains '(Limits on Freedom)' in question prompts")

    if errors:
        print(f"[FAIL] TWR Because/But/So Audit: Found {len(errors)} defects:")
        for err in errors:
            print(f"  - {err}")
        return len(errors)

    print(f"[PASS] TWR Because/But/So Audit: Passed across {len(sample_sections)} sample sections.")
    return 0


def main():
    print("=" * 60)
    print("Curriculum Product Quality & Content Audit")
    print("=" * 60)

    total_failures = 0
    total_failures += audit_catalog_vocab_completeness()
    total_failures += audit_vocab_index_completeness()
    total_failures += audit_vocabulary_practice_generation()
    total_failures += audit_twr_because_but_so_strategy()

    print("=" * 60)
    if total_failures == 0:
        print("ALL QUALITY AUDIT CHECKS PASSED (100% HEALTHY)")
        sys.exit(0)
    else:
        print(f"AUDIT FAILED WITH {total_failures} DEFECT(S)")
        sys.exit(1)


if __name__ == "__main__":
    main()
