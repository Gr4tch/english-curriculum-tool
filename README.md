# 8th Grade U.S. History (English) — AI Curriculum & Packet Co-Designer

A custom curriculum & student packet co-design web application built for 8th-grade U.S. History in **English** (**40-minute daily class periods**), grounded 100% in National Geographic / Cengage's ***American Stories: Beginnings to 1877***.

---

## ✨ Key Capabilities

1. **Complete Offline English Textbook Repository (194 Searchable 2-Page Spreads)**
   - Compiled from the Cengage HTML5 eReader into **194 searchable 2-page PDFs** (`output/sections/` and `output/American Stories (Sections)/Unit X/Chapter Y/Sec Z.pdf`) with an embedded selectable text layer.
   - **194 paragraph-tagged Markdown files** (`output/markdown/`) with `[¶1]..[¶N]` locators, extracted printed `MAIN IDEA` statements, `HISTORICAL THINKING` (`#1 Reading Check`, `#2 Skill`, `#3 Determine Word Meaning`), `CRITICAL VIEWING` map/image questions, back-of-book Official Content & Academic Vocabulary (`pp. R44–R58`, `output/vocab_index.json`), and end-of-chapter `CHAPTER REVIEW` sets (`output/chapter_reviews.json`).

2. **Blank-Slate Teacher Agency & Interactive AI Co-Designer (`app.py`)**
   - **Blank-Slate Section Checklist**: Chapters open with zero sections pre-selected (`selected_sections: []`) so the teacher chooses only the sections he wants to teach.
   - **Central Idea Strategy Bank + Anti-Copycat Modes**:
     - **4 Visual Central Idea Templates**: *Subheading Gists → Central Idea*, *Box & Bullets*, *Historical "What + So What?"*, and *Claim–Evidence–Reasoning (CER)*.
     - **3 Anti-Copycat Modes** for the textbook's printed `MAIN IDEA` box (*"Prove the Textbook's Main Idea"*, *"Subheading Central Ideas"*, and *"Upgrade the Textbook's Main Idea"*) so students never copy the printed 1-sentence Main Idea verbatim.
   - **40-Minute Pacing & Dual-Tier Scaffolding**:
     - Choose **1-Page per Section** (ultra-compact: e.g., 11 sections + Cover Tracker = 12 pages = 6 double-sided sheets) or **2-Page per Section** layouts.
     - Generate **Standard Edition**, **Scaffolded Support Edition** (with sentence starters & word banks), or **Both Editions**.
     - Includes a **Chapter Central Idea Study Guide Tracker Cover Page**, an **All-in-One Teacher Clipboard Answer Key** with exact `[p. XXX, "SUBHEADING", ¶Y]` citations, and an **End-of-Chapter Central Idea Review & Assessment Generator**.

3. **Locked-In `vibrant-lovelace` Aesthetics & Google Drive Export**
   - Every Word (`.docx`) and native Google Doc export automatically enforces your locked-in formatting rules (`src/gdrive_exporter.py` + `src/agent_team.py`): Calibri Navy/Slate hierarchy, `0.85"/0.90"` booklet margins, isolated `WD_SECTION_START.NEW_PAGE` breaks with unlinked footers, `#F1F5F9` shaded table headers, `#94A3B8` solid vs. dotted handwriting lines, zero emojis, and an **Automatic Page-Budget Fit Guardrail**.
   - Exports to an isolated Google Drive root folder (`#US History (English) Curriculum Materials`) using link-based sharing (`Anyone with link`) so no partner email address is required upfront.

---

## 🚀 Quick Start

```powershell
# Activate the virtual environment and launch the Streamlit web interface:
.\.venv\Scripts\streamlit.exe run app.py
```
