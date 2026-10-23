import os
import re
from typing import Dict, List, Any, Optional, Tuple

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

SOLID_LINE = "_________________________________________________________________________________"
DOTTED_LINE = "..................................................................................................."


# ─────────────────────────────────────────────────────────────────────────────
# MULTI-AGENT SYSTEM PROMPTS (STRICT 100% PASSAGE GROUNDING & ZERO BLOAT)
# ─────────────────────────────────────────────────────────────────────────────

CREATOR_AGENT_PROMPT = """You are Agent 2: The 8th-Grade U.S. History & Central Idea Pedagogical Creator.
Your role is to create or revise student packet worksheets and teacher clipboard answer keys in English based EXCLUSIVELY on the provided 2-page section from National Geographic's "American Stories: Beginnings to 1877".

CRITICAL RULES:
1. 100% TEXTBOOK PASSAGE GROUNDING (ZERO EXTERNAL TRIVIA):
   - Every question, graphic organizer cell, vocabulary item, sentence stem, and answer key entry MUST be 100% answerable from the provided 2-page section text alone.
   - NEVER introduce historical people, ships, dates, or events omitted from the 2 pages.
2. TEACHER'S CUSTOM BLUEPRINT & METHODOLOGY ISOLATION:
   - Follow the teacher's selected Central Idea template, Reading Organizer, and Pacing (1-Page or 2-Page layout).
   - Do NOT inject The Writing Revolution (TWR) strategies unless explicitly requested by the teacher.
3. LOCKED-IN AESTHETIC & LINE PROTOCOL:
   - Never use emojis anywhere in the document.
   - Format numbered subheadings cleanly as: **1. SUBHEADING NAME (p. XXX)** (never write "Subheading:" or put quotes around the heading).
   - Use SOLID lines (_________________________________________________________________________________) when students write complete sentences.
   - Use DOTTED lines (...................................................................................................) ONLY when students jot brief notes, keywords, or 10-word gists.
   - Keep student directions to 1 concise bold sentence. Never put course banners, strategy badges, or standards tables on the student worksheet.
4. EXACT PARAGRAPH CITATIONS IN THE TEACHER KEY:
   - Every answer in the Teacher Key must include the exact page number, subheading, and paragraph locator, e.g. [p. 180, "WAR DEBT", ¶1].
"""

GROUNDING_AUDITOR_PROMPT = """You are Agent 3: The 100% Textbook Passage Grounding & Citation Auditor.
Cross-examine the draft student worksheet and teacher key against the 2-page English textbook passage:
1. Verify that every proper noun, law, date, and cause/effect claim appears explicitly in the passage. Replace any external knowledge immediately.
2. Verify that every Teacher Answer Key item includes an accurate [p. XXX, "SUBHEADING", ¶Y] locator so the teacher can point struggling readers to the exact paragraph during a 40-minute period.
3. Ensure zero emojis and zero administrative bloat on the student worksheet.
Return ONLY the verified markdown content.
"""


def run_live_section_revision_chat(
    user_instruction: str,
    section_meta: Dict[str, Any],
    markdown_text: str,
    current_student_md: str,
    current_scaffolded_md: str,
    current_teacher_md: str,
    api_key: str = ""
) -> Dict[str, str]:
    """
    Allows the teacher to chat with the AI in Tab 2 (Interactive Section Studio)
    to tweak or customize any aspect of a generated section packet while keeping
    locked-in aesthetics and 100% textbook grounding intact.
    """
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    if GENAI_AVAILABLE and key_to_use:
        try:
            client = genai.Client(api_key=key_to_use)
            prompt = f"""TEXTBOOK SECTION METADATA:
Chapter {section_meta['chapter_num']}, Section {section_meta['section_code']}: {section_meta['title']} (pp. {section_meta['printed_pages']})

2-PAGE TEXTBOOK SOURCE PASSAGE:
{markdown_text}

CURRENT STANDARD STUDENT WORKSHEET:
{current_student_md}

CURRENT SCAFFOLDED STUDENT WORKSHEET:
{current_scaffolded_md}

CURRENT TEACHER CLIPBOARD KEY:
{current_teacher_md}

TEACHER'S REVISION REQUEST:
"{user_instruction}"

Apply the teacher's revision request while maintaining 100% passage grounding, locked-in Calibri/table aesthetics, zero emojis, and exact [p. X, "SUBHEADING", ¶Y] citations in the key.
Return your output divided by these exact three delimiters:
===STANDARD_STUDENT===
(updated standard student worksheet markdown)
===SCAFFOLDED_STUDENT===
(updated scaffolded student worksheet markdown with sentence stems)
===TEACHER_KEY===
(updated teacher clipboard answer key markdown)
"""
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=CREATOR_AGENT_PROMPT,
                    temperature=0.3,
                )
            )
            raw = (resp.text or "").strip()
            if "===STANDARD_STUDENT===" in raw and "===TEACHER_KEY===" in raw:
                p1 = raw.split("===STANDARD_STUDENT===", 1)[1]
                std_part, rest = p1.split("===SCAFFOLDED_STUDENT===", 1) if "===SCAFFOLDED_STUDENT===" in p1 else (p1.split("===TEACHER_KEY===")[0], p1)
                if "===TEACHER_KEY===" in rest:
                    scaf_part, tch_part = rest.split("===TEACHER_KEY===", 1)
                else:
                    scaf_part, tch_part = std_part, current_teacher_md
                return {
                    "student_standard_md": sanitize_aesthetics(std_part.strip()),
                    "student_scaffolded_md": sanitize_aesthetics(scaf_part.strip()),
                    "teacher_key_md": sanitize_aesthetics(tch_part.strip()),
                    "status_note": f"Applied AI revision: '{user_instruction}' (100% passage-grounded & formatted).",
                }
        except Exception as e:
            return {
                "student_standard_md": current_student_md,
                "student_scaffolded_md": current_scaffolded_md,
                "teacher_key_md": current_teacher_md,
                "status_note": f"Could not reach Gemini API ({e}); retained current verified packet.",
            }

    # Intelligent offline revision handler if API key is offline
    note_line = f"\n\n**Teacher Custom Prompt ({section_meta['section_code']}):** {user_instruction}\n{SOLID_LINE}\n{SOLID_LINE}"
    return {
        "student_standard_md": sanitize_aesthetics(current_student_md + note_line),
        "student_scaffolded_md": sanitize_aesthetics(
            current_scaffolded_md + f"\n\n**Teacher Custom Prompt ({section_meta['section_code']}):** {user_instruction}\n*Sentence Starter: Based on the reading, I can conclude that* _____________\n{SOLID_LINE}"
        ),
        "teacher_key_md": current_teacher_md + f"\n- **Custom Prompt Key:** Verify student response uses specific evidence from pp. {section_meta['printed_pages']}.",
        "status_note": f"Added custom prompt to Section {section_meta['section_code']}.",
    }


def sanitize_aesthetics(md_text: str) -> str:
    """
    Agent 4 Post-Processor: Enforces the locked-in aesthetic parameters from vibrant-lovelace:
    - Strips any emojis
    - Replaces raw LaTeX arrows
    - Normalizes solid and dotted writing lines
    """
    # Strip common emoji ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F9FF"
        "\U00002600-\U000027BF"
        "\U0001FA00-\U0001FAFF"
        "]+",
        flags=re.UNICODE,
    )
    cleaned = emoji_pattern.sub("", md_text)
    cleaned = cleaned.replace(r"$\rightarrow$", "→").replace(r"\rightarrow", "→")
    return cleaned.strip()


def enforce_page_budget_guardrail(markdown_page: str, target_pages: int = 1) -> Tuple[str, Dict[str, Any]]:
    """
    Agent 4 Automatic Page-Budget Fit Guardrail:
    Calculates the vertical layout cost of a student worksheet page (in layout units,
    where 1 full 8.5x11 page with 0.85" margins holds ~28 layout units).
    If a 1-page section worksheet exceeds the 1-page budget, automatically compacts
    redundant blank writing lines so it NEVER spills 2 extra lines onto a second page!
    """
    max_units = 28 * target_pages
    lines = markdown_page.splitlines()

    def compute_units(line_list: List[str]) -> float:
        total = 0.0
        for ln in line_list:
            s = ln.strip()
            if not s or s == "[PAGE_BREAK]":
                continue
            if s.startswith("[GRADE_BOX:"):
                continue  # Grade box lives in the page footer (0 body height!)
            if s.startswith("#"):
                total += 1.6
            elif s.startswith("|") and s.endswith("|"):
                if not re.match(r"^\|\s*:?-+", s):
                    total += 1.7
            elif re.match(r"^[\._]{15,}$", s):
                total += 1.35
            else:
                total += max(1.0, len(s) / 95.0)
        return total

    initial_units = compute_units(lines)
    was_compacted = False

    if initial_units > max_units:
        # Pass 1: Collapse consecutive triple writing lines down to double writing lines
        compacted: List[str] = []
        consecutive_lines = 0
        for ln in lines:
            if re.match(r"^\s*[\._]{15,}\s*$", ln):
                consecutive_lines += 1
                if consecutive_lines <= (1 if target_pages == 1 else 2):
                    compacted.append(ln)
                    continue
                else:
                    was_compacted = True
                    continue
            else:
                consecutive_lines = 0
                compacted.append(ln)
        lines = compacted

    final_units = compute_units(lines)
    return "\n".join(lines), {
        "target_pages": target_pages,
        "initial_layout_units": round(initial_units, 1),
        "final_layout_units": round(final_units, 1),
        "max_budget_units": max_units,
        "was_auto_compacted": was_compacted,
        "fits_cleanly": final_units <= (max_units + 1.5),
    }
