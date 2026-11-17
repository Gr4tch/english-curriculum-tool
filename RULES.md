# Curriculum Engineering & Quality Guidelines

This document consolidates the core pedagogical rules, quality assurance standards, and syntax guardrails for the English and Dual-Language Social Studies Curriculum Generator.

---

## 1. Curriculum Content Grounding & Passage Alignment

> [!IMPORTANT]
> **Strict Passage Grounding Mandate**: 8th-grade dual-language students must be able to complete 100% of the packet (Day 1 Cornell/Graphic Organizer notes, synthesis questions, Day 2 vocabulary reinforcement, and Day 2 TWR sentence activities) using **only** the assigned section pages from the textbook. Do **not** assume, test, or display outside historical knowledge.

### 1.1 Zero External Knowledge Dependency
- **Forbidden**: Introducing historical names, acts, ships, dates, or events not present in the section text:
  - *Example Violation*: Introducing *George Grenville* or *la Ley del Azúcar (Sugar Act)* into Section 1.1 (pages 178–179). In the National Geographic curriculum, Section 1.1 covers only Pontiac's Rebellion, the Proclamation of 1763, and the Quartering Act; Grenville and the Sugar Act are introduced in Section 1.2 (pages 180–181).
  - *Example Violation*: Asking about the ship *Liberty* in Section 2.1 when the text does not mention John Hancock or *Liberty*; naming the ship *Gaspee* in Section 2.3 when the text only says "un barco británico"; naming *Henry Knox* or *Dorchester Heights* in Section 4.3 when the text only mentions cannons from Ticonderoga placed on high ground.
- **Rule**: If a detail is omitted from the textbook passage, it **must not** appear in student prompts, questions, required answers, or visual previews. Always use the phrasing and terminology present in the student's text.

### 1.2 Minor Inferencing Standard
- Synthesis questions and open-ended prompts must require only **minor inferencing** directly scaffolded by the text.
  - *Acceptable*: Asking how John Locke's ideas of natural rights and consent of the governed justified the colonists' decision to protest the Townshend Acts (both concepts are explicitly explained on pages 186–187).
  - *Unacceptable*: Asking students to recall what happened when customs officials seized John Hancock's ship *Liberty* (absent from pages 186–187).
- When designing synthesis questions, prioritize the textbook's built-in **Razonamiento Histórico** / **Comprobar la lectura** questions or direct synthesis of the section's explicit cause-and-effect relationships.

### 1.3 Dynamic Visual Previews Grounding Mandate
- **No Mock Templates**: Web app worksheet previews must dynamically parse and render the **exact generated Markdown** from `pkt['student_packet_md']` and `pkt['teacher_plan_md']`.
- Never use static dummy text or mock question placeholders in visual renderers. What the teacher sees in the preview must be 1:1 identical to what prints in the student booklet and exports to Google Docs.

### 1.4 Student Page Layout & Clean Canvas Protocols
- **Header Block Placement**:
  - The student header block (`Nombre: ____________________ Fecha: __________ Período: _____`) is placed strictly on the **Front Cover** of the booklet and on **every Left Page** (Page 1 of Day 1, and Page 3 of Day 2).
  - Right Pages (Page 2 of Day 1 reading notes, and Page 4 of Day 2 TWR practice) must **omit** student name headers to maximize vertical writing room.
- **Zero Pill / Badge Leakage**:
  - Colored pill badges (`100 PUNTOS`, `HOJA DEL ESTUDIANTE`, `TWR 3+1: ...`) are **prohibited** inside the printable student worksheet canvas.
  - All teacher metadata (points, rubric, strategy name) must live in the web app UI header bar outside the worksheet canvas or in the Teacher Answer Key.

### 1.5 Automated Grounding Verification Script
Before releasing or exporting curriculum packages, run the automated verification script:
```powershell
python scripts/verify_grounding.py
```
This script audits every active section against a canonical chronological entity matrix to ensure no historical acts or figures leak into sections prior to their textbook introduction.

### 1.6 Grounding Verification Checklist
Before finalizing student packet content or visual previews, run this 5-point verification:
1. **Passage Search**: Search every proper noun, event, and cause/effect claim in the packet against the section markdown. If a word or concept does not appear, verify if it is an essential framing word or ungrounded external knowledge.
2. **Chronological Alignment**: Does this event occur in these specific pages, or does it belong to a later section?
3. **Student Feasibility**: Read each prompt from the perspective of an 8th-grade student. Can the student point their finger at the exact paragraph containing the answer?
4. **Answer Key Concordance**: Does the teacher answer key cite explicit phrases and concepts found in the student reading?
5. **Left-Page Header & Clean Margins**: Verify that student name headers only appear on left pages and front cover, with zero badge clutter.

---

## 2. Curriculum Product Quality & Content Audit

### 2.1 Complete Definitions Mandate
- Every vocabulary entry in `output/catalog.json` and `output/vocab_index.json` must possess a non-empty, textbook-grounded definition (`len(definition) >= 10`).
- Definitions must never be stored as empty strings `""` or placeholders like `"Defined in context below"`. If the textbook introduces a term in context, the grounded definition must be extracted from the section passage.

### 2.2 Zero Empty Prompts & Orphaned Colons
- No worksheet question, clue, or matching item may end in an orphaned colon (`:\n` or `:\s*$`) without clue text.
- Fill-in lines must always be accompanied by the historical clue or definition.

### 2.3 Scaffolded vs. Standard Differentiation
- **Standard Edition (At-Level)**:
  - Header badge uses `ws-badge-blue` (clean blue background).
  - Vocabulary practice exercises omit the word bank to encourage memory retrieval and close reading.
  - Clean open response lines (`1. _________________________ : [Definition]`).
- **Scaffolded Edition**:
  - Header badge uses `ws-badge-amber` (warm yellow background).
  - No redundant secondary rectangular badge (e.g. `SCAFFOLDED EDITION`).
  - Vocabulary practice exercises include a prominent `Word Bank` box.
  - Response lines must remain clean blanks (`1. _________________________ : [Definition]`) without first-letter giveaways, keeping cognitive demand appropriate while providing the word bank support.

### 2.4 Clean Question Stems & Header Separation Mandate
- Section code (`In Section X.X`) and section title (`(Title)`) must never be prepended to question stems or sentence completion prompts.
- All section metadata belongs strictly in the top header badge (`SECTION X.X HANDOUT • TITLE (PP. ...)`); duplicating it inside student prompts is prohibited.
- Every sentence completion stem (such as TWR 'Because, But, So') must start directly with a capitalized letter (e.g., `1. Tensions grew between Britain and the colonies because...`).
- Writing lines must not append trailing periods after solid line tokens that wrap as orphan punctuation on a subsequent line.

### 2.5 Automated Quality Audit Script
Run the automated product quality audit script before releasing changes:
```powershell
python scripts/audit_product_quality.py
```
**Verification Criteria**:
1. Scans 100% of vocabulary entries across all sections for missing definitions.
2. Scans `output/vocab_index.json` for empty definitions.
3. Generates standard and scaffolded handouts across chapters to verify zero giveaways, zero placeholder text, and authentic definitions.

---

## 3. Code & Syntax Leak Prevention Guardrails

Mandatory validation checks and programmatic guardrails to guarantee that no raw code, internal tokens, unrendered LaTeX/math syntax, unrendered HTML tags, or markdown code block traps leak into student packets, teacher plans, exported documents, or web UI previews.

### 3.1 Forbidden Leaks & Patterns

| Artifact Category | Forbidden Patterns | Correct Replacement |
| :--- | :--- | :--- |
| **Markdown Indented Code Block Traps (Streamlit UI)** | Multiline HTML strings in `st.markdown(..., unsafe_allow_html=True)` containing 4+ leading spaces on lines with tags or trailing empty conditional lines (`<span ...>Selected</span> if is_sel else ''`). Triggers CommonMark `<pre><code>` mode and displays raw HTML tags in UI. | Process all web HTML with `render_clean_html()` or collapse inter-tag newlines via `re.sub(r">\s*\n\s*<", "><", ...)`. Zero 4-space markdown indentations. |
| **Inline Anchor Wrapping Block Elements (Tag Splitting)** | Wrapping block tags (`<div>`, `<p>`) inside inline anchor tags (`<a class="hero-card"><div>...</div></a>`). CommonMark parser splits the anchor across each block child, multiplying styled card borders into multiple fragmented empty boxes. | Use `<span style="display:block;">` inside `<a>`, or use an outer `<div class="hero-card">` container with a native `st.button` below it. |
| **LaTeX / Math Symbols** | `$\rightarrow$`, `\rightarrow`, `$\leftarrow$`, `\leftarrow`, `$...$`, `$$...$$` | Typographical arrows (`→`, `←`) or plain text. |
| **Unrendered Special Tokens** | `[ADMIN_STANDARDS: ...]`, `[GRADE_BOX: ...]`, `[VOCAB_BOX: ...]`, `[PAGE_BREAK]` | Rendered structured tables, footer grade boxes, or page break sections. |
| **Raw HTML in Student Text** | `<mark>`, `</mark>`, `<p>`, `</p>`, `<div>`, `</div>`, `&nbsp;`, `&amp;` in markdown body | Markdown formatting (`**bold**`, `*italic*`) or plain text (only `<br>` allowed inside table cells). |
| **Template / Variable Leaks** | `{variable}`, `{pkt[...]`, `{{`, `}}`, `None`, `null` | Evaluated data or formatted fallback string. |
| **Corrupted Formats** | Dangling asterisks (`***`, unclosed `**`), orphan table pipes (`\|   \|`), broken backticks | Valid, closed markdown syntax. |
| **Unrendered Markdown in Web/PDF HTML** | Raw `**bold**`, `*italic*`, `> blockquote`, or unspaced lines inside `<div class="ws-container">`. Triggers literal asterisks and collapsed lines in web views and Chromium PDF prints. | Process all pages with `_convert_markdown_blocks_and_inlines()` in `format_booklet_for_web()`. Convert bold to `<b>`, italics to `<i>`, blockquotes to `.ws-callout`, and wrap paragraphs into individual spaced divs. |
| **Unwanted Headings in Quotes** | `"Subtítulo: ..."` or quotes around auto-generated subheadings | Clean headings without `"Subtítulo:"` or outer quotation marks. |

### 3.2 The Markdown Indented Code Block Trap & Prevention
Under CommonMark:
- Any line with **4 or more spaces of leading indentation** following a blank line or newline is automatically parsed as an **indented code block** (`<pre><code>...</code></pre>`).
- In Streamlit applications, multiline HTML f-strings containing empty conditional variables with indentation trigger this trap.

**Mandatory UI Prevention Function**:
```python
import re
import streamlit as st

def render_clean_html(html_str: str) -> None:
    """
    Safely renders HTML in Streamlit by collapsing inter-tag newlines and leading indentation.
    Guarantees CommonMark/Markdown never coerces indented HTML or empty conditional lines into <pre><code> blocks.
    """
    clean = re.sub(r">\s*\n\s*<", "><", html_str.strip())
    clean = re.sub(r"\n\s*", " ", clean)
    st.markdown(clean, unsafe_allow_html=True)
```

### 3.3 Exporter Sanitization Guarantee
In all exporter modules (`pdf_exporter.py`, `doc_exporter.py`), all text must be actively scrubbed before rendering:
```python
def sanitize_export_text(raw_text: str) -> str:
    """Active scrubber applied to all paragraphs and table cells before export."""
    text = raw_text
    # 1. LaTeX arrow replacements
    text = text.replace(r"$\rightarrow$", "→").replace(r"\rightarrow", "→")
    text = text.replace(r"$\leftarrow$", "←").replace(r"\leftarrow", "←")
    text = text.replace("$", "")

    # 2. HTML tag cleaning (preserving table cell <br>)
    text = re.sub(r'</?(?:mark|p|div|span)[^>]*>', '', text, flags=re.IGNORECASE)

    # 3. Clean template remnants
    text = re.sub(r'\{[a-zA-Z0-9_]+\}', '', text)
    return text
```

### 3.4 Verification Checklist
Prior to presenting any export link or confirming changes:
1. Run `python scripts/audit_code_leaks.py`.
2. Confirm zero violations reported across document markdown and web UI components.
3. Confirm that all web HTML blocks are rendered with `render_clean_html()`.
4. Confirm zero emojis are present across all responses, commits, comments, and code.
