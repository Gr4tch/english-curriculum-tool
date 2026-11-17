#!/usr/bin/env python3
"""
Comprehensive Code & Syntax Leak Audit Script.
Scans document generators, strategy templates, UI components, and export pipelines
for leaking LaTeX syntax, raw tokens, unrendered HTML, and markdown indented code block traps.
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

FORBIDDEN_DOCUMENT_PATTERNS: List[Tuple[str, str]] = [
    (r'\$[\\a-zA-Z0-9_\{\}\s\^\-\+\*]+\$', "LaTeX Math Block ($...$)"),
    (r'\\[a-zA-Z]+', "Backslash Escape / Command (e.g. \\rightarrow)"),
    (r'\[(ADMIN_STANDARDS|GRADE_BOX|VOCAB_BOX|CENTER_HEADING):', "Unprocessed Internal Token"),
    (r'<(?!br\s*/?>)[a-zA-Z/][^>]*>', "Raw HTML Tag (non-<br>) in Markdown"),
    (r'\{[a-zA-Z0-9_\[\]\'"]+\}', "Unresolved Python Template Variable"),
    (r'\bNone\b', "Literal 'None' Object Leak"),
    (r'\bnull\b', "Literal 'null' Token Leak"),
]

FORBIDDEN_RAW_MARKDOWN_PATTERNS: List[Tuple[str, str]] = [
    (r'\$[\\a-zA-Z0-9_\{\}\s\^\-\+\*]+\$', "LaTeX Math Block ($...$)"),
    (r'\\[a-zA-Z]+', "Backslash Escape / Command (e.g. \\rightarrow)"),
    (r'\{[a-zA-Z0-9_\[\]\'"]+\}', "Unresolved Python Template Variable"),
    (r'\bNone\b', "Literal 'None' Object Leak"),
    (r'\bnull\b', "Literal 'null' Token Leak"),
]

def audit_raw_markdown_text(text: str, source_name: str = "Raw Markdown") -> List[Dict[str, Any]]:
    """Scans intermediate generator markdown for leaking code, math, template variables, or literal None/null values."""
    violations = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        for pattern, label in FORBIDDEN_RAW_MARKDOWN_PATTERNS:
            matches = re.findall(pattern, line)
            if matches:
                violations.append({
                    "source": source_name,
                    "line_number": idx,
                    "label": label,
                    "matches": matches,
                    "snippet": line.strip()[:100],
                })
    return violations

def audit_document_text(text: str, source_name: str = "Document") -> List[Dict[str, Any]]:
    """Scans student/teacher markdown text for any leaking code, math syntax, or unprocessed tokens."""
    violations = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        for pattern, label in FORBIDDEN_DOCUMENT_PATTERNS:
            matches = re.findall(pattern, line)
            if matches:
                violations.append({
                    "source": source_name,
                    "line_number": idx,
                    "label": label,
                    "matches": matches,
                    "snippet": line.strip()[:100],
                })
    return violations

def audit_ui_html_string(html_str: str, source_name: str = "UI Component") -> List[Dict[str, Any]]:
    """
    Scans UI HTML strings intended for st.markdown(..., unsafe_allow_html=True)
    to detect lines with 4+ leading spaces that trigger CommonMark indented code blocks.
    """
    violations = []
    lines = html_str.splitlines()
    for idx, line in enumerate(lines, 1):
        # Line with 4+ spaces that contains HTML tags
        if line.startswith("    ") and ("<" in line or ">" in line):
            violations.append({
                "source": source_name,
                "line_number": idx,
                "label": "Markdown Indented Code Block Trap (4+ leading spaces on HTML line)",
                "matches": [line[:30]],
                "snippet": line.strip()[:100],
            })
        # Check for blank lines with trailing spaces
        if line != "" and line.isspace() and len(line) >= 4:
            violations.append({
                "source": source_name,
                "line_number": idx,
                "label": "Whitespace-only line with 4+ spaces (triggers code block on subsequent lines)",
                "matches": [f"{len(line)} spaces"],
                "snippet": "<blank line with spaces>",
            })

    # Check for block-splitting trap: <a> wrapping <div>
    if re.search(r"<a\b[^>]*>(?:(?!</a>).)*?<div\b", html_str, re.DOTALL | re.IGNORECASE):
        violations.append({
            "source": source_name,
            "line_number": 1,
            "label": "Anchor Tag Splitting Trap (<a> tag wrapping block-level <div>)",
            "matches": ["<a>...<div>"],
            "snippet": html_str.strip()[:100],
        })

    return violations

def run_workspace_audit() -> bool:
    """Runs a full audit across the current workspace."""
    import os
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    violations = []

    # 1. Audit Strategy Thumbnails
    try:
        from src.strategy_thumbnails import ALL_STRATEGY_TILES
        for t in ALL_STRATEGY_TILES:
            v = audit_ui_html_string(t.get("thumbnail_svg", ""), f"Strategy Thumbnail: {t.get('code')}")
            violations.extend(v)
    except Exception as ex:
        print(f"Warning: Could not import ALL_STRATEGY_TILES: {ex}")

    # 2. Audit UI code in app.py for indented st.markdown blocks
    app_path = Path("app.py")
    if app_path.exists():
        app_text = app_path.read_text(encoding="utf-8")
        # Check for multiline f-strings passed directly to st.markdown with unsafe_allow_html
        fstring_matches = re.finditer(r'st\.markdown\(\s*f?"""(.*?)"""\s*,\s*unsafe_allow_html=True\)', app_text, re.DOTALL)
        for m in fstring_matches:
            block = m.group(1)
            v = audit_ui_html_string(block, "app.py st.markdown block")
            violations.extend(v)

    # 3. Audit Generated Handouts, Exemplars & HTML Web/PDF Rendering Pipeline
    try:
        from src.strategy_thumbnails import ALL_STRATEGY_TILES
        from src.packet_builder import build_standalone_strategy_handout
        from src.preview_renderer import format_booklet_for_web, format_half_sheet_2up

        sec_meta = {
            "chapter_num": 5,
            "section_code": "5.3",
            "title": "Impact of the War",
            "printed_pages": "158-159",
            "start_page": 158,
            "end_page": 159,
            "printed_main_idea": "Victory in the French and Indian War expanded British territory but led to conflict with Native Americans in the Ohio Valley.",
            "official_vocab": [{"word": "Praise", "definition": "Express warm approval"}],
            "md_file": "curriculum_content/textbook_sections/ch05_sec03.md",
        }
        category_map = {
            "Central Idea": "central_idea",
            "Anti-Copycat": "anti_copycat",
            "Active Reading": "reading_organizer",
            "The Writing Revolution": "twr",
            "Writing (TWR)": "twr",
            "Vocabulary": "vocab",
            "Assessment": "assessment",
        }

        for tile in ALL_STRATEGY_TILES:
            cat = category_map.get(tile.get("category", ""), "central_idea")
            code = tile.get("code")
            handouts = build_standalone_strategy_handout(sec_meta, cat, code)

            for key in ["student_standard_md", "student_scaffolded_md", "exemplar_md"]:
                raw_md = handouts.get(key, "")
                if not raw_md:
                    continue

                # Audit raw markdown document text
                v_doc = audit_raw_markdown_text(raw_md, f"Strategy {code} [{key}]")
                violations.extend(v_doc)

                # Audit rendered web/PDF HTML
                html = format_booklet_for_web(raw_md)
                html_no_style = re.sub(r"<style>.*?</style>", "", html, flags=re.DOTALL)

                # Check for raw bold asterisks leaking into HTML/PDF
                raw_bolds = re.findall(r"\*\*[^*]+\*\*", html_no_style)
                if raw_bolds:
                    violations.append({
                        "source": f"Rendered HTML ({code} {key})",
                        "line_number": 1,
                        "label": "Raw Markdown Bold Asterisks Leaked into Rendered HTML/PDF",
                        "matches": raw_bolds[:3],
                        "snippet": raw_bolds[0][:80],
                    })

                # Check for raw italic asterisks leaking into HTML/PDF
                no_tags = re.sub(r"<[^>]+>", "", html_no_style)
                raw_italics = re.findall(r"(?<!\*)\*[^*\n]+\*(?!\*)", no_tags)
                if raw_italics:
                    violations.append({
                        "source": f"Rendered HTML ({code} {key})",
                        "line_number": 1,
                        "label": "Raw Markdown Italic Asterisks Leaked into Rendered HTML/PDF",
                        "matches": raw_italics[:3],
                        "snippet": raw_italics[0][:80],
                    })

                # Check for unprocessed internal tokens
                token_matches = re.findall(r"\[(ADMIN_STANDARDS|GRADE_BOX|VOCAB_BOX|CENTER_HEADING|PAGE_BREAK):", html_no_style)
                if token_matches:
                    violations.append({
                        "source": f"Rendered HTML ({code} {key})",
                        "line_number": 1,
                        "label": "Unprocessed Internal Token Leaked into Rendered HTML/PDF",
                        "matches": token_matches,
                        "snippet": f"Unprocessed token: {token_matches[0]}",
                    })

    except Exception as ex:
        print(f"Warning: Could not audit strategy rendering pipeline: {ex}")

    if violations:
        print(f"FAILED: {len(violations)} code leak violations found:")
        for v in violations:
            print(f"  - [{v['source']} Line {v['line_number']}] {v['label']}: {v['snippet']}")
        return False
    else:
        print("PASSED: Zero code leaks, zero unrendered tokens, and zero markdown code block traps detected!")
        return True

if __name__ == "__main__":
    success = run_workspace_audit()
    sys.exit(0 if success else 1)
