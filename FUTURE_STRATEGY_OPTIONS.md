# Future Curriculum Strategy Options & DOK Roadmap

This document preserves researched strategy designs and pedagogical options for future expansion of the **Curriculum Design Studio** (`Worksheet Gallery` & `Packet Builder`).

---

## Depth of Knowledge (DOK) Strategy Options

While Webb's **Depth of Knowledge (DOK)** is a 4-level scale of cognitive rigor, middle school Social Studies departments frequently use structured **DOK Worksheets** to move students systematically from basic comprehension (DOK 1) to analytical reasoning with text evidence (DOK 3).

### Option 1: "DOK Questions (Level 1–2–3 Question Ladder)" — [IMPLEMENTED]
- **Strategy Code**: `crit_04_dok_questions`
- **Category**: `Critical Thinking` (`critical_thinking`)
- **Target Standards**: `CCSS RH.6-8.1 & RH.6-8.2`
- **Pedagogical Design**:
  A 3-step vertical cognitive ladder on a single page where students climb from **DOK Level 1** to **DOK Level 3** using the section spread:
  1. **Step 1 — DOK Level 1 (Recall & Identify — Who, What, When, Where)**:
     - Students identify explicit historical facts, laws, or actors from each blue subheading on the spread.
     - *Scaffolded Edition*: Provides a section Word Bank and structured cloze/fill-in-the-blank statements for each subheading.
  2. **Step 2 — DOK Level 2 (Skills & Concepts — How & Why / Cause & Effect)**:
     - Students explain how or why the historical developments in the first subheading influenced or led to the events in the second subheading.
     - *Scaffolded Edition*: Provides a cause-and-effect sentence frame connecting the two subheadings.
  3. **Step 3 — DOK Level 3 (Strategic Thinking — Claim & Text Evidence)**:
     - Students make an analytical claim evaluating the historical significance or competing perspectives in the section and justify it with specific text evidence and page citations.
     - *Scaffolded Edition*: Provides a two-part Claim + Text Evidence starter (`"Based on the reading..."` / `"This is proven on page ___, which states..."`).

---

### Option 2: "Two-Part Evidence Questions (Part A: DOK 2 / Part B: DOK 3)" — [SAVED FOR FUTURE]
- **Proposed Strategy Code**: `crit_05_dok_two_part_evidence`
- **Proposed Category**: `Critical Thinking` or `Assessment`
- **Target Standards**: `CCSS RH.6-8.1`
- **Pedagogical Design**:
  Modeled after two-part state assessment items (`Part A` + `Part B`) that train students to back up every comprehension or analysis claim with explicit textual proof:
  - **Item 1 (Subheading 1 Focus)**:
    - **Part A (DOK 2 — Concept / Analysis)**: Asks a *How* or *Why* question about the historical action or policy in Subheading 1 (using `subheadings[0]["say_something_q"]` or cause-and-effect relationship).
    - **Part B (DOK 3 — Text Evidence Justification)**: *"Which specific detail, law, or action from Subheading 1 best supports your answer to Part A? Cite the page number and explain how it proves your point."*
  - **Item 2 (Subheading 2 Focus)**:
    - **Part A (DOK 2 — Concept / Analysis)**: Asks a *How* or *Why* question about the historical reaction or outcome in Subheading 2.
    - **Part B (DOK 3 — Text Evidence Justification)**: *"Which specific detail or outcome from Subheading 2 best supports your answer to Part A? Cite the page number and explain how it proves your point."*
- **Scaffolded Edition Mechanics**:
  - *Part A*: Provides a sentence starter (`"The main reason for this action was..."`).
  - *Part B*: Provides an evidence-citation frame (`"On page ___, the text states that ___, which proves my answer to Part A because..."`).
- **Data Mapping Notes**:
  - Uses `kb["subheadings"][0]` and `kb["subheadings"][1]` (`say_something_q`, `cause`, `effect`, `gist`, `citation`).

---

### Option 3: "Student-Generated DOK Question Stems" — [SAVED FOR FUTURE]
- **Proposed Strategy Code**: `crit_06_dok_question_stems`
- **Proposed Category**: `Critical Thinking`
- **Target Standards**: `CCSS RH.6-8.1 & RH.6-8.4`
- **Pedagogical Design**:
  Students act as historians and test-makers by using a built-in **DOK Question Stem Bank** at the top of the handout to write and answer their own leveled questions from the textbook spread:
  - **Top Reference Box (DOK Question Stem Bank)**:
    - **DOK 1 Stems (Recall)**: *"What was the purpose of ___?"* | *"Who led ___?"* | *"When/where did ___ take place?"*
    - **DOK 2 Stems (Concepts)**: *"How did ___ cause or lead to ___?"* | *"How did ___'s perspective differ from ___'s?"*
    - **DOK 3 Stems (Strategic Thinking)**: *"What evidence on page ___ best proves that ___?"* | *"Why was ___ the most important turning point in this section?"*
  - **Student Task Table (3 Rows: DOK 1, DOK 2, DOK 3)**:
    - Column 1: **My Historical Question** (written using a stem from the bank and key terms from the section).
    - Column 2: **Complete Answer with Text Evidence & Page Number** (written in complete sentences).
- **Scaffolded Edition Mechanics**:
  - Pre-fills the question stem in Column 1 with blanks for the section's vocabulary/subheadings (e.g., *"How did _________________________ lead to _________________________?"*) and provides an answer starter in Column 2.
- **Data Mapping Notes**:
  - Uses `kb["word_bank"]`, `kb["subheadings"]`, and `kb["perspectives"]` to generate authentic exemplar student questions and answers for the Teacher Answer Key.
