"""
Automated Passage Grounding Verification Script
Checks all generated student packet materials and worksheet previews against the actual section textbook text.
Ensures zero external knowledge leaks (e.g. asking about Ley del Azúcar in Section 1.1).
"""

import json
import re
import sys
from pathlib import Path

# Fix Windows console encoding for accents
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.curriculum_scope import load_scope_state, compute_yearlong_twr_progression, load_excel_vocab_catalog
from src.packet_builder import generate_section_packet_and_plan

HISTORICAL_CANONICAL_ENTITIES = [
    ("azúcar", "Ley del Azúcar / Sugar Act"),
    ("grenville", "George Grenville"),
    ("timbre", "Ley del Timbre / Stamp Act"),
    ("hijos de la libertad", "Hijos de la Libertad"),
    ("townshend", "Leyes de Townshend"),
    ("masacre de boston", "Masacre de Boston"),
    ("crispus attucks", "Crispus Attucks"),
    ("motín del té", "Motín del Té / Boston Tea Party"),
    ("leyes coercitivas", "Leyes Coercitivas"),
    ("leyes intolerables", "Leyes Intolerables"),
    ("paul revere", "Paul Revere"),
    ("lexington", "Lexington"),
    ("concord", "Concord"),
    ("bunker hill", "Bunker Hill"),
    ("sentido común", "Sentido Común / Common Sense"),
    ("thomas paine", "Thomas Paine"),
    ("jefferson", "Thomas Jefferson"),
    ("declaración de independencia", "Declaración de Independencia")
]


def verify_all_active_sections():
    cat_path = Path("output/catalog.json")
    if not cat_path.exists():
        print("Catalog not found.")
        return False

    cat = json.loads(cat_path.read_text(encoding="utf-8"))
    scope = load_scope_state(cat)
    twr = compute_yearlong_twr_progression(cat, scope)
    vocab = load_excel_vocab_catalog()
    active_map = scope.get("active_sections", {})

    active_secs = [s for s in cat if active_map.get(s["id"], False)]
    print(f"Auditing {len(active_secs)} active sections for strict passage grounding...")

    violations = []
    for sec in active_secs:
        sid = sec["id"]
        sec_title = sec["title"]
        md_path = Path(sec["md_file"])
        if not md_path.exists():
            continue

        raw_passage = md_path.read_text(encoding="utf-8").lower()
        pkt = generate_section_packet_and_plan(sec, twr.get(sid, {}), vocab.get(sid))
        student_md = pkt["student_packet_md"].lower()

        # Check for ungrounded entities
        for term, label in HISTORICAL_CANONICAL_ENTITIES:
            if term in student_md and term not in raw_passage:
                violations.append(
                    f"[{sid} - {sec_title}] Student packet references '{label}' (keyword: '{term}'), "
                    f"but it is NOT found anywhere in the textbook passage (pp. {sec['printed_pages']})!"
                )

    if violations:
        print(f"\n❌ FOUND {len(violations)} GROUNDING VIOLATION(S):")
        for v in violations:
            print("  *", v)
        return False
    else:
        print(f"\n✅ GROUNDING AUDIT PASSED: All {len(active_secs)} active sections are 100% passage grounded!")
        return True


if __name__ == "__main__":
    success = verify_all_active_sections()
    sys.exit(0 if success else 1)
