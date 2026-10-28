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

        # Check 4: Scaffolded edition should have first-letter hints on blanks
        if not re.search(r'\d+\.\s+[A-Za-z]_+', scaf_md):
            errors.append(f"Sec {sec_code}: Scaffolded edition missing first-letter cues on blanks")

        # Check 5: Badge styling in rendered HTML
        std_html = format_booklet_for_web(std_md)
        scaf_html = format_booklet_for_web(scaf_md)

        if "ws-badge-blue" not in std_html:
            errors.append(f"Sec {sec_code}: Standard edition HTML missing ws-badge-blue")
        if "ws-badge-amber" not in scaf_html:
            errors.append(f"Sec {sec_code}: Scaffolded edition HTML missing ws-badge-amber")
        if "Scaffolded Edition</span>" in scaf_html:
            errors.append(f"Sec {sec_code}: Scaffolded edition contains redundant rectangular badge")

    if errors:
        print(f"[FAIL] Vocabulary Generation Audit: Found {len(errors)} defects:")
        for err in errors:
            print(f"  - {err}")
        return len(errors)

    print(f"[PASS] Vocabulary Generation Audit: Passed for all {len(test_sections)} test sections.")
    return 0


def main():
    print("=" * 60)
    print("Curriculum Product Quality & Content Audit")
    print("=" * 60)

    total_failures = 0
    total_failures += audit_catalog_vocab_completeness()
    total_failures += audit_vocab_index_completeness()
    total_failures += audit_vocabulary_practice_generation()

    print("=" * 60)
    if total_failures == 0:
        print("ALL QUALITY AUDIT CHECKS PASSED (100% HEALTHY)")
        sys.exit(0)
    else:
        print(f"AUDIT FAILED WITH {total_failures} DEFECT(S)")
        sys.exit(1)


if __name__ == "__main__":
    main()
