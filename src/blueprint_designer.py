import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

def _load_env_file():
    for candidate in [Path(".env"), Path("../.env"), Path("C:/Users/Jared/Documents/antigravity/vibrant-lovelace/.env")]:
        if candidate.exists():
            try:
                for line in candidate.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            except Exception:
                pass

_load_env_file()

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from src.strategy_bank import (
    CENTRAL_IDEA_STRATEGIES,
    PRINTED_MAIN_IDEA_MODES,
    READING_ORGANIZERS,
    VOCAB_MODES,
    READING_MODES,
    OPTIONAL_TWR_STRATEGIES,
    CHAPTER_STANDARDS_MAP,
    get_strategy_by_code,
)

BLUEPRINTS_PATH = Path("output/teacher_blueprints.json")


def get_default_chapter_blueprint(chapter_num: int) -> Dict[str, Any]:
    """
    Returns a clean, blank-slate blueprint for a chapter.
    Notice that 'selected_sections' starts empty ([]) so the teacher makes the
    active section decisions from scratch when opening a chapter.
    """
    return {
        "chapter_num": chapter_num,
        "selected_sections": [],  # True blank slate! Teacher checks sections to include
        "pages_per_section": 1,   # 1-Page Compact (40-min friendly) or 2-Page Front/Back
        "reading_mode": "mode_mixed_flexible",
        "scaffolding_mode": "both",  # 'standard', 'scaffolded', or 'both'
        "cover_page_mode": "central_idea_tracker",  # 'central_idea_tracker', 'score_checklist', 'none'
        "grade_box_mode": "points_100",  # 'points_100', 'points_10', 'stamp_box', 'none'
        "vocab_mode": "vocab_official_box",
        "central_idea_strategy": "auto_recommend",
        "printed_main_idea_mode": "auto_recommend",
        "reading_organizer": "auto_recommend",
        "include_reading_check_q1": True,
        "include_skill_q2": False,
        "include_critical_viewing": False,
        "optional_twr_strategy": "twr_none",
        "section_overrides": {},  # sec_id -> {reading_organizer, central_idea_strategy, printed_main_idea_mode, include_critical_viewing, custom_note}
        "chat_history": [],
    }


def load_all_blueprints() -> Dict[str, Any]:
    if not BLUEPRINTS_PATH.exists():
        return {}
    try:
        return json.loads(BLUEPRINTS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_chapter_blueprint(chapter_num: int, chapter_title: str = "") -> Dict[str, Any]:
    all_bp = load_all_blueprints()
    key = str(chapter_num)
    default_bp = get_default_chapter_blueprint(chapter_num)
    if chapter_title:
        default_bp["chapter_title"] = chapter_title
    if key in all_bp:
        merged = {**default_bp, **all_bp[key]}
        return merged
    return default_bp


def get_chapter_blueprint(chapter_num: int, chapter_title: str = "") -> Dict[str, Any]:
    return load_chapter_blueprint(chapter_num, chapter_title)


def save_chapter_blueprint(chapter_num: int, blueprint: Dict[str, Any]) -> None:
    all_bp = load_all_blueprints()
    all_bp[str(chapter_num)] = blueprint
    BLUEPRINTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    BLUEPRINTS_PATH.write_text(json.dumps(all_bp, indent=2, ensure_ascii=False), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# AGENT 1: AUTOMATED TEXT STRUCTURE & CENTRAL IDEA RECOMMENDER PER SECTION
# ─────────────────────────────────────────────────────────────────────────────

def recommend_section_strategies(
    section_meta: Dict[str, Any],
    markdown_text: str,
    blueprint: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Agent 1 (Text Structure & Central Idea Auditor):
    Analyzes the 2-page English section's subheadings, causal/chronological/perspective
    markers, printed MAIN IDEA, and CRITICAL VIEWING prompts to recommend the optimal
    Reading Organizer, Central Idea Template, and Anti-Copycat Mode for an 8th-grade
    40-minute U.S. History period.
    Respects any explicit teacher choice or per-section override in the blueprint.
    """
    sec_id = section_meta["id"]
    sec_code = str(section_meta["section_code"])
    sec_title = section_meta["title"]
    sec_ov_map = blueprint.get("section_overrides", {})
    overrides = sec_ov_map.get(sec_code) or sec_ov_map.get(sec_id) or {}

    txt_low = (markdown_text or "").lower() + " " + sec_title.lower()

    # 1. Determine optimal Reading Organizer
    causal_markers = [
        "because", "therefore", "as a result", "led to", "caused", "in response",
        "forced", "due to", "consequence", "protest", "tax", "act", "debt", "anger"
    ]
    seq_markers = [
        "first", "then", "next", "finally", "midnight", "dawn", "morning", "march",
        "april", "may", "june", "july", "1770", "1773", "1774", "1775", "1776", "battle", "ride"
    ]
    comp_markers = [
        "on the other hand", "unlike", "both", "similar", "different", "loyalist",
        "patriot", "eastern", "western", "british", "colonists", "debate", "divided", "sides"
    ]

    causal_hits = sum(1 for m in causal_markers if m in txt_low)
    seq_hits = sum(1 for m in seq_markers if m in txt_low)
    comp_hits = sum(1 for m in comp_markers if m in txt_low)

    # Curated high-precision recommendations for Chapter 5 sections
    ch5_curated_map = {
        "1.1": ("read_01_cause_effect", "ci_03_what_so_what", "pmi_01_prove_it", "Strong cause-and-effect structure (French & Indian War -> Proclamation of 1763 & Quartering Act -> colonial resentment)."),
        "1.2": ("read_02_say_something", "ci_01_subheading_gist", "pmi_03_upgrade_it", "Two clear thematic subheadings ('War Debt' and 'Acts of Parliament') ideal for Subheading Gists and upgrading the printed Main Idea with the Sugar & Currency Acts."),
        "1.3": ("read_01_cause_effect", "ci_02_box_and_bullets", "pmi_01_prove_it", "Direct cause-and-effect chain from the Stamp Act to the Sons of Liberty, Patrick Henry, and the Stamp Act Congress."),
        "1.4": ("read_02_say_something", "ci_04_cer_paragraph", "pmi_02_subheading_focus", "Primary voice biography of Benjamin Franklin ideal for partner stop-and-jot and a short CER claim."),
        "2.1": ("read_01_cause_effect", "ci_03_what_so_what", "pmi_03_upgrade_it", "Connects the Townshend Acts and Writs of Assistance to colonial boycotts, the Daughters of Liberty, and John Locke's natural rights."),
        "2.2": ("read_05_compare_perspectives", "ci_02_box_and_bullets", "pmi_01_prove_it", "Contrasts British vs. Patriot perspectives on the Boston Massacre and Paul Revere's engraving."),
        "2.3": ("read_04_sequence_timeline", "ci_03_what_so_what", "pmi_02_subheading_focus", "Chronological escalation from the Tea Act (1773) to the Boston Tea Party and the Coercive/Intolerable Acts (1774)."),
        "2.4": ("read_02_say_something", "ci_01_subheading_gist", "pmi_02_subheading_focus", "Museum artifact spread best suited for brief subheading reactions."),
        "3.1": ("read_03_cloze_guided", "ci_02_box_and_bullets", "pmi_01_prove_it", "Covers the First Continental Congress, Patrick Henry, and militias/Minutemen—ideal for Guided Cloze Notes + Box & Bullets."),
        "3.2": ("read_04_sequence_timeline", "ci_01_subheading_gist", "pmi_02_subheading_focus", "Hour-by-hour narrative of Paul Revere and William Dawes's midnight ride on April 18, 1775."),
        "3.3": ("read_04_sequence_timeline", "ci_03_what_so_what", "pmi_03_upgrade_it", "Chronological battle sequence from Lexington at dawn to Concord's North Bridge and the British retreat to Boston."),
        "3.4": ("read_02_say_something", "ci_01_subheading_gist", "pmi_02_subheading_focus", "Historic landmark spread on Concord's North Bridge."),
        "4.1": ("read_05_compare_perspectives", "ci_03_what_so_what", "pmi_01_prove_it", "Compares peace efforts (Olive Branch Petition) with war preparations (Continental Army, Fort Ticonderoga, Bunker Hill)."),
        "4.2": ("read_01_cause_effect", "ci_03_what_so_what", "pmi_02_subheading_focus", "Geography feature explaining how Breed's Hill, Bunker Hill, and Dorchester Heights shaped the Battle of Boston."),
        "4.3": ("read_01_cause_effect", "ci_04_cer_paragraph", "pmi_03_upgrade_it", "Explains how the evacuation of Boston and Thomas Paine's 'Common Sense' convinced colonists to break with Britain."),
        "4.4": ("read_03_cloze_guided", "ci_02_box_and_bullets", "pmi_01_prove_it", "Breaks down the structure and natural-rights philosophy of the Declaration of Independence."),
        "4.5": ("read_05_compare_perspectives", "ci_04_cer_paragraph", "pmi_02_subheading_focus", "Document-Based Question comparing primary source excerpts on freedom and independence."),
    }

    if section_meta["chapter_num"] == 5 and sec_code in ch5_curated_map:
        rec_read, rec_ci, rec_pmi, rationale = ch5_curated_map[sec_code]
    else:
        if seq_hits >= 4 and seq_hits >= causal_hits:
            rec_read = "read_04_sequence_timeline"
            rec_ci = "ci_01_subheading_gist"
            rec_pmi = "pmi_02_subheading_focus"
            rationale = f"Detected {seq_hits} chronological/date markers suitable for a Sequence Tracker."
        elif comp_hits >= 4:
            rec_read = "read_05_compare_perspectives"
            rec_ci = "ci_02_box_and_bullets"
            rec_pmi = "pmi_01_prove_it"
            rationale = f"Detected {comp_hits} perspective/comparison markers suitable for a Competing Perspectives Matrix."
        elif causal_hits >= 4:
            rec_read = "read_01_cause_effect"
            rec_ci = "ci_03_what_so_what"
            rec_pmi = "pmi_03_upgrade_it"
            rationale = f"Detected {causal_hits} causal markers suitable for a Cause & Effect Table."
        else:
            rec_read = "read_02_say_something"
            rec_ci = "ci_01_subheading_gist"
            rec_pmi = "pmi_01_prove_it"
            rationale = "Aligned directly to section subheadings for clear 8th-grade comprehension."

    # Apply blueprint-level setting or section-level override
    bp_read = overrides.get("reading_organizer") or blueprint.get("reading_organizer", "auto_recommend")
    bp_ci = overrides.get("central_idea_strategy") or blueprint.get("central_idea_strategy", "auto_recommend")
    bp_pmi = overrides.get("printed_main_idea_mode") or blueprint.get("printed_main_idea_mode", "auto_recommend")

    final_read_code = rec_read if bp_read == "auto_recommend" else bp_read
    final_ci_code = rec_ci if bp_ci == "auto_recommend" else bp_ci
    final_pmi_code = rec_pmi if bp_pmi == "auto_recommend" else bp_pmi

    read_obj = get_strategy_by_code(READING_ORGANIZERS, final_read_code)
    ci_obj = get_strategy_by_code(CENTRAL_IDEA_STRATEGIES, final_ci_code)
    pmi_obj = get_strategy_by_code(PRINTED_MAIN_IDEA_MODES, final_pmi_code)

    has_cv = bool(section_meta.get("critical_viewing"))
    inc_cv = overrides.get("include_critical_viewing", blueprint.get("include_critical_viewing", False)) and has_cv

    return {
        "section_id": sec_id,
        "section_code": sec_code,
        "reading_organizer_code": final_read_code,
        "reading_organizer_name": read_obj["name"],
        "reading_organizer_short": read_obj["short_name"],
        "central_idea_code": final_ci_code,
        "central_idea_name": ci_obj["name"],
        "central_idea_short": ci_obj["short_name"],
        "printed_main_idea_mode_code": final_pmi_code,
        "printed_main_idea_mode_name": pmi_obj["name"],
        "printed_main_idea_mode_short": pmi_obj["short_name"],
        "include_critical_viewing": inc_cv,
        "has_critical_viewing_on_spread": has_cv,
        "rationale": rationale,
        "reason": rationale,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CONVERSATIONAL AI BLUEPRINT CO-DESIGNER
# ─────────────────────────────────────────────────────────────────────────────

def _answer_pedagogical_question(
    msg_low: str,
    blueprint: Dict[str, Any],
    chapter_num: int,
    chapter_title: str
) -> Optional[str]:
    """Provides high-quality, instant pedagogical answers to teacher questions."""
    # 1. Flexible reading mode / reading modes
    if any(k in msg_low for k in ["reading mode", "flexible", "routine", "read aloud", "partner", "independent reading"]):
        return (
            "### What is 'Flexible Reading Mode' and How Do Reading Routines Work?\n\n"
            "**Flexible Reading Mode** prints versatile, neutral directions on every student worksheet:\n"
            "> *\"As we read each subheading together or with your partner, record your answers below.\"*\n\n"
            "**Why is it the recommended default?**\n"
            "In a fast-paced 40-minute history class, your lesson flow changes day-to-day. On Monday you might read aloud as a whole class, on Tuesday students might partner read, and on Wednesday they might read independently. Flexible mode means your printed handouts **work seamlessly with any classroom format** without needing to reprint or reformat.\n\n"
            "**Other Modes You Can Choose:**\n"
            "- **Whole-Class Pause & Jot:** Best for teacher-led reading or audiobooks. Prompts students to listen and pause for 60-second writing check-ins after each subheading.\n"
            "- **Partner Chunked Reading:** Prompts student pairs to take turns reading paragraphs aloud, discuss the checkpoint prompt, and agree on their written answer.\n"
            "- **Independent Silent Reading:** Directs students to work solo using paragraph numbers `[¶1]..[¶N]`.\n"
            "- **Custom Routine (Other):** Lets you write your own custom instructions (e.g. for audio listening stations or station rotations)!"
        )

    # 2. Anti-copycat modes / prove it / upgrade it
    if any(k in msg_low for k in ["copycat", "prove it", "upgrade", "printed main idea", "main idea box"]):
        return (
            "### What are Anti-Copycat Modes?\n\n"
            "Every 2-page spread in the National Geographic textbook prints a **1-sentence 'MAIN IDEA' box** on the top-left of the page (for example: *'The British government made new laws that tightened control over the American colonies'*).\n\n"
            "If your worksheet simply asks *'What is the main idea?'*, 8th graders will spot that box and copy it word-for-word in 15 seconds without doing any reading!\n\n"
            "**How the 3 Anti-Copycat Modes solve this:**\n"
            "1. **Mode A ('Prove the Textbook's Main Idea'):** Pre-prints the textbook's exact sentence on the worksheet, marks it with a clear warning (*'DO NOT copy this statement!'*), and challenges students to find 2 specific historical facts from the subheadings that prove it is true.\n"
            "2. **Mode B ('Subheading Central Ideas'):** Directs students to ignore the general spread summary and instead determine the unprinted Central Idea of each individual subsection.\n"
            "3. **Mode C ('Upgrade the Textbook's Main Idea'):** Shows the textbook's basic 5th-grade sentence and challenges students to upgrade it into a mature 8th-grade historical claim naming the specific tax, the people who resisted, and the outcome."
        )

    # 3. Vocabulary / 0 vocab
    if "vocab" in msg_low or "vocabulary" in msg_low:
        return (
            "### How Does Vocabulary Work & Can I Choose 0 Vocab?\n\n"
            "Yes! You have 4 vocabulary options depending on how much time and page space you want to dedicate to vocabulary:\n\n"
            "1. **Zero Vocab (Skip Vocabulary):** Completely removes the vocabulary block from student worksheets and answer keys, dedicating 100% of your 1-page budget to historical reading, questions, and Central Idea synthesis. Perfect if you don't have to teach formal ELA standards!\n"
            "2. **Official Vocab Box (Default):** Prints 2–4 official glossary terms with student-friendly textbook definitions and a quick context check in a neat table.\n"
            "3. **Built-In #3 Word Meaning Check:** Uses the textbook's own '#3 Determine Word Meaning' question (takes under 2 minutes).\n"
            "4. **Embedded Terms Only:** Weaves vocabulary words in bold directly into the reading questions without a separate box."
        )

    # 4. Central Idea templates
    if any(k in msg_low for k in ["central idea", "box and bullet", "gist", "so what", "cer", "synthesis"]):
        return (
            "### Central Idea Strategy Breakdown\n\n"
            "All Central Idea templates target **CCSS RH.6-8.2** (identifying central historical claims distinct from supporting details):\n\n"
            "1. **Subheading Gists -> Central Idea:** Students write a concise 10-word gist after each subheading, then combine those gists into a 1–2 sentence Central Idea on solid lines.\n"
            "2. **Box & Bullets:** A prominent top box holds the section's overarching historical claim, followed by 3 bulleted evidence lines citing specific page facts.\n"
            "3. **'What Happened? + So What?':** A 3-column table separating what happened (facts) from why it mattered (historical significance).\n"
            "4. **Claim–Evidence–Reasoning (CER):** Structured 3-sentence frame (Claim, Evidence, Reasoning) ideal for the final 10 minutes of class.\n\n"
            "*(Tip: Choosing 'Use Recommended Templates per Section' automatically assigns varied formats across different days.)*"
        )

    # 5. Front cover / study guide tracker
    if any(k in msg_low for k in ["cover", "study guide", "tracker"]):
        return (
            "### Booklet Front Cover Options\n\n"
            "1. **Central Idea Study Guide Tracker (Recommended):** Formats the front cover as a cumulative chapter study guide. Every section in your packet has a row with its title and lines for students to copy their final 1-sentence Central Idea, creating a ready-to-study review sheet for the chapter test.\n"
            "2. **Section Score / Stamp Table:** An accountability table where you can stamp, initial, or record daily scores (e.g. 10 pts per section) as you check work.\n"
            "3. **No Front Cover Page:** Leaves out the cover entirely and begins immediately on Section 1, saving 1 sheet of paper per student when photocopying."
        )

    # 6. Page footer check box / stamp box / 10-point
    if any(k in msg_low for k in ["footer", "stamp", "point", "grade box", "check box"]):
        return (
            "### Page Footer Check Box Options\n\n"
            "Every section worksheet can include a walkthrough grading box at the bottom of the page:\n\n"
            "- **Teacher Stamp Box:** Clean box for a quick stamp or initials during classroom walkthroughs.\n"
            "- **10-Point Score Box:** `Score: ____ / 10 pts   Init: [ ]` for daily gradebook entry.\n"
            "- **100-Point Score Box:** `Score: ____ / 100 pts   Init: [ ]` for percentage grading.\n"
            "- **No Footer Box:** Omits the box for maximum writing space."
        )

    # 7. Pacing / 40 minutes / 1 page vs 2 pages
    if any(k in msg_low for k in ["40 min", "pacing", "time", "1 page", "2 page", "dense", "length"]):
        return (
            "### ⏱️ Pacing for a 40-Minute Class\n\n"
            "The **1-Page Compact format** is engineered specifically for a 40-minute daily schedule:\n\n"
            "- **Minutes 0–5:** Warm-up / Vocab preview (or jump straight to reading if using Zero Vocab)\n"
            "- **Minutes 5–20:** Section reading (partner, read-aloud, or independent) & Active Reading Organizer\n"
            "- **Minutes 20–35:** Central Idea Synthesis (Subheading Gists, Box & Bullets, or CER) / Anti-Copycat Check\n"
            "- **Minutes 35–40:** Teacher Walkthrough Stamp / Quick Exit Check\n\n"
            "Choosing **1 page per section** prevents student cognitive fatigue and guarantees the entire spread fits on a single side of paper!"
        )

    return None


def run_blueprint_codesigner_chat(
    user_message: str,
    chapter_num: int,
    chapter_title: str,
    chapter_sections: List[Dict[str, Any]],
    current_blueprint: Dict[str, Any],
    chat_history: Optional[List[Dict[str, str]]] = None,
    api_key: str = ""
) -> Tuple[str, Dict[str, Any]]:
    """
    Conversational AI Co-Designer that answers teacher questions with pedagogical depth
    and updates the blueprint when the teacher expresses a clear configuration preference.
    """
    updated_bp = dict(current_blueprint)
    msg_low = user_message.lower().strip()

    is_question = (
        bool(re.search(r"\b(what|how|why|which|explain|tell me|can i|is there|difference|mean)\b", msg_low))
        or "?" in user_message
    )

    # Check for direct commands / preferences to update the blueprint
    modifications = []

    if ("1 page" in msg_low or "one page" in msg_low or "single page" in msg_low) and not is_question:
        updated_bp["pages_per_section"] = 1
        modifications.append("Packet Density -> 1 Page per Section (Ultra-Compact)")
    elif ("2 page" in msg_low or "two page" in msg_low or "front and back" in msg_low) and not is_question:
        updated_bp["pages_per_section"] = 2
        modifications.append("Packet Density -> 2 Pages per Section (Front & Back)")

    if ("all core" in msg_low or "core narrative" in msg_low) and not is_question:
        core_codes = [str(s["section_code"]) for s in chapter_sections if s.get("section_type", "Core Narrative") == "Core Narrative"]
        updated_bp["selected_sections"] = core_codes
        modifications.append(f"Selected Sections -> {len(core_codes)} Core Narrative Spreads")
    elif ("select all" in msg_low or "every section" in msg_low) and not is_question:
        all_codes = [str(s["section_code"]) for s in chapter_sections]
        updated_bp["selected_sections"] = all_codes
        modifications.append(f"Selected Sections -> All {len(all_codes)} Chapter Spreads")

    if ("zero vocab" in msg_low or "0 vocab" in msg_low or "no vocab" in msg_low or "skip vocab" in msg_low) and not is_question:
        updated_bp["vocab_mode"] = "vocab_none"
        modifications.append("Vocabulary Mode -> Zero Vocab (Skip Vocabulary Section)")
    elif ("official vocab" in msg_low) and not is_question:
        updated_bp["vocab_mode"] = "vocab_official_box"
        modifications.append("Vocabulary Mode -> Official Vocab Box")

    if ("box and bullet" in msg_low or "box & bullet" in msg_low) and not is_question:
        updated_bp["central_idea_strategy"] = "ci_02_box_and_bullets"
        modifications.append("Central Idea Strategy -> Box & Bullets (Claim + 3 Details)")
    elif ("gist" in msg_low) and not is_question:
        updated_bp["central_idea_strategy"] = "ci_01_subheading_gist"
        modifications.append("Central Idea Strategy -> Subheading Gists -> Central Idea")
    elif ("cer" in msg_low or "claim evidence" in msg_low) and not is_question:
        updated_bp["central_idea_strategy"] = "ci_04_cer_paragraph"
        modifications.append("Central Idea Strategy -> Claim–Evidence–Reasoning (CER)")
    elif ("auto" in msg_low or "recommend" in msg_low or "varied" in msg_low) and not is_question:
        updated_bp["central_idea_strategy"] = "auto_recommend"
        updated_bp["reading_organizer"] = "auto_recommend"
        modifications.append("Central Idea Strategy -> Use Recommended Templates per Section (AI Varied Variety)")

    if ("partner" in msg_low) and not is_question:
        updated_bp["reading_mode"] = "mode_partner"
        modifications.append("Classroom Routine -> Partner Chunked Reading")
    elif ("read aloud" in msg_low) and not is_question:
        updated_bp["reading_mode"] = "mode_read_aloud"
        modifications.append("Classroom Routine -> Whole-Class Teacher Read-Aloud")
    elif ("independent" in msg_low) and not is_question:
        updated_bp["reading_mode"] = "mode_independent"
        modifications.append("Classroom Routine -> Independent Reading")
    elif ("flexible" in msg_low) and not is_question:
        updated_bp["reading_mode"] = "mode_mixed_flexible"
        modifications.append("Classroom Routine -> Flexible Reading Mode (Daily Mix)")

    # 1. If it's a question, try answering it with pedagogical knowledge
    ped_answer = _answer_pedagogical_question(msg_low, updated_bp, chapter_num, chapter_title)
    if ped_answer:
        if modifications:
            ped_answer += f"\n\n---\n*Also applied requested change:* {', '.join(modifications)}"
        return ped_answer, updated_bp

    # 2. Try Gemini API for conversational inquiries
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    if GENAI_AVAILABLE and key_to_use:
        try:
            client = genai.Client(api_key=key_to_use)
            selected_codes = set(str(c) for c in updated_bp.get("selected_sections", []))
            selected_secs = [s for s in chapter_sections if str(s["section_code"]) in selected_codes or s["id"] in selected_codes]
            sec_summary = "\n".join(
                f"- Sec {s['section_code']}: {s['title']} (pp. {s['printed_pages']}, {s['section_type']})"
                for s in chapter_sections
            )
            sys_prompt = f"""You are an expert 8th-Grade U.S. History and Adolescent Literacy curriculum co-designer.
You are helping an 8th-grade U.S. History teacher design materials for a 40-minute daily period in English using National Geographic "American Stories: Beginnings to 1877".
He does NOT have to teach ELA standards, and his main literacy focus is Central Idea and distinguishing central ideas from supporting historical details.
Always answer his questions thoroughly, practically, and warmly with concrete classroom advice. Do NOT give boilerplate template status messages if he is asking a question."""

            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.3,
                )
            )
            if resp and resp.text:
                reply_text = resp.text.strip()
                if modifications:
                    reply_text += f"\n\n---\n*Updated your blueprint:* {', '.join(modifications)}"
                return reply_text, updated_bp
        except Exception:
            pass

    # 3. If modifications were made, confirm them clearly
    if modifications:
        reply = (
            f"**Updated Chapter {chapter_num} ({chapter_title}) Blueprint!**\n\n"
            f"**Applied Changes:**\n"
            + "\n".join(f"- {m}" for m in modifications)
            + f"\n\nYour live packet preview in Step 2 and Step 3 has been refreshed automatically."
        )
        return reply, updated_bp

    # 4. Helpful general assistant fallback
    selected_codes = set(str(c) for c in updated_bp.get("selected_sections", []))
    selected_secs = [s for s in chapter_sections if str(s["section_code"]) in selected_codes or s["id"] in selected_codes]
    reply = (
        f"Hi! I'm your AI curriculum co-designer for **Chapter {chapter_num}: {chapter_title}**.\n\n"
        f"You currently have **{len(selected_secs)} sections** selected ({updated_bp['pages_per_section']} page per section).\n\n"
        f"**You can ask me questions anytime like:**\n"
        f"- *\"What is 'Flexible Reading Mode'?\"*\n"
        f"- *\"How do the Anti-Copycat modes stop students from copying the textbook?\"*\n"
        f"- *\"Can I choose Zero Vocab to save space for history?\"*\n"
        f"- *\"What is the Central Idea Study Guide Tracker on the cover?\"*\n"
        f"- *\"Recommend the best templates for a 2-week unit.\"*"
    )
    return reply, updated_bp
