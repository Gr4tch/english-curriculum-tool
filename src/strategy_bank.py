from typing import Dict, List, Any

# ─────────────────────────────────────────────────────────────────────────────
# 1. VISUAL CENTRAL IDEA STRATEGY GALLERY (PRIMARY ELA FOCUS: CCSS RH.6-8.2)
# ─────────────────────────────────────────────────────────────────────────────

CENTRAL_IDEA_STRATEGIES: List[Dict[str, str]] = [
    {
        "code": "ci_01_subheading_gist",
        "name": "Subheading Gists → Whole-Section Central Idea",
        "short_name": "Subheading Gists → Central Idea",
        "best_for": "Chunked partner or independent reading across 2–3 subheadings. Prevents cognitive overload by breaking the spread into 10-word checkpoints.",
        "description": "Students pause after each subheading to jot a concise 10-word gist on dotted lines, then combine those gists into a 1–2 sentence Central Idea on solid lines.",
        "visual_preview_md": """**Part 1: Subheading Gist Checkpoints**
- **PROBLEMS ARISE (p. 178):**
  *10-Word Subheading Gist:* ...................................................................................................
- **SOLDIERS IN THE COLONIES (p. 178):**
  *10-Word Subheading Gist:* ...................................................................................................
- **A PROCLAMATION LINE (p. 179):**
  *10-Word Subheading Gist:* ...................................................................................................

**Part 2: Whole-Section Central Idea (Combine your gists into 1–2 complete sentences):**
_________________________________________________________________________________
_________________________________________________________________________________""",
        "exemplar_md": """**Part 1: Subheading Gist Checkpoints (Student Exemplar):**
- **PROBLEMS ARISE (p. 178):**
  *10-Word Gist:* Britain gained vast North American territory but faced massive wartime debts after 1763. *(12 words)*
- **SOLDIERS IN THE COLONIES (p. 178):**
  *10-Word Gist:* Parliament passed Quartering Act forcing colonists to house British troops in towns. *(11 words)*
- **A PROCLAMATION LINE (p. 179):**
  *10-Word Gist:* King George banned western migration past Appalachians, angering land-hungry settlers. *(10 words)*

**Part 2: Whole-Section Central Idea (Student Exemplar):**
After 1763, Great Britain tried to manage its expanded empire by restricting colonial westward settlement and quartering soldiers, which sparked widespread colonial anger over losing their traditional freedoms.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Subheading 1 Stem:** Britain faced problems after the war because... [Word Bank: debt, territory, French]
- **Subheading 2 Stem:** The Quartering Act required colonists to... [Word Bank: soldiers, barracks, expense]
- **Subheading 3 Stem:** King George issued the Proclamation of 1763 to stop colonists from... [Word Bank: settlement, Appalachians]
- **Synthesis Frame:** Following the French and Indian War, Great Britain tightened control by [action 1] and [action 2], which caused colonists to believe their rights were being [threatened / violated].""",
    },
    {
        "code": "ci_02_box_and_bullets",
        "name": "Box & Bullets (Topic + Author's Point = Central Idea)",
        "short_name": "Box & Bullets (Central Idea + 3 Details)",
        "best_for": "Teaching students how specific historical facts directly support an overarching central claim.",
        "description": "Students state the overarching Central Idea of the 2-page reading in a top framing box and cite 3 specific supporting details from the subheadings as bullets below.",
        "visual_preview_md": """┌────────────────────────────────────────────────────────────────────────────────────────┐
│ CENTRAL IDEA BOX (Topic + Main Historical Claim of the Section)                        │
│ **Central Idea:** ____________________________________________________________________ │
│ ______________________________________________________________________________________ │
└────────────────────────────────────────────────────────────────────────────────────────┘

- **Supporting Detail 1 (p. 180):** .....................................................................................
- **Supporting Detail 2 (p. 180):** .....................................................................................
- **Supporting Detail 3 (p. 181):** .....................................................................................""",
        "exemplar_md": """┌────────────────────────────────────────────────────────────────────────────────────────┐
│ CENTRAL IDEA BOX (Student Exemplar)                                                    │
│ The Stamp Act provoked fierce resistance across the colonies because colonists         │
│ believed only their own elected colonial assemblies had the legal right to tax them.   │
└────────────────────────────────────────────────────────────────────────────────────────┘

- **Supporting Detail 1 (p. 180):** Patrick Henry declared in the Virginia House of Burgesses that taxing colonists without consent was an act of tyranny.
- **Supporting Detail 2 (p. 180):** Colonial merchants signed nonimportation agreements, boycotting British manufactured imports until Parliament repealed the tax.
- **Supporting Detail 3 (p. 181):** The Sons of Liberty organized protests, burned effigies of royal stamp distributors in the streets, and forced officials to resign.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Central Idea Frame:** The Stamp Act united colonial resistance because colonists believed [taxation without representation / Parliament's power] was unfair.
- **Detail 1 Starter (p. 180, ¶2):** In Virginia, Patrick Henry argued that...
- **Detail 2 Starter (p. 180, ¶4):** Colonial merchants organized against the tax by...
- **Detail 3 Starter (p. 181, ¶2):** A protest group called the Sons of Liberty took action by...
- **Word Bank:** representation, boycott, assemblies, nonimportation, protest""",
    },
    {
        "code": "ci_03_what_so_what",
        "name": "Historical 'What Happened? + So What?' Synthesis",
        "short_name": "'What Happened? + So What?'",
        "best_for": "Helping 8th graders move from merely listing historical facts ('What') to explaining their causal significance ('So What').",
        "description": "Students identify what happened in each part of the reading and explain why it mattered to the bigger historical conflict.",
        "visual_preview_md": """| Subheading & Page | WHAT HAPPENED? (Key Historical Fact) | SO WHAT? (Why did this matter to the crisis?) |
| :--- | :--- | :--- |
| **1. The Townshend Acts (p. 182)** | __________________________________________ | __________________________________________ |
| **2. Protests & Boycotts (p. 183)** | __________________________________________ | __________________________________________ |

**Central Idea Synthesis:** How did these events shift the relationship between Britain and the colonies?
_________________________________________________________________________________
_________________________________________________________________________________""",
        "exemplar_md": """| Subheading & Page | WHAT HAPPENED? (Key Historical Fact) | SO WHAT? (Why did this matter to the crisis?) |
| :--- | :--- | :--- |
| **1. The Townshend Acts (p. 182)** | Parliament placed duties on imported tea, glass, lead, paper, and paint. | It showed Parliament still insisted on taxing colonists without consent, even after repealing the Stamp Act. |
| **2. Protests & Boycotts (p. 183)** | Women formed the Daughters of Liberty and urged colonists to weave homespun fabric. | It mobilized entire colonial communities and proved economic boycotts could hurt British merchants. |

**Central Idea Synthesis (Student Exemplar):**
The Townshend Acts reignited colonial outrage and united everyday colonists, including women, to resist British taxation through economic boycotts and domestic manufacturing.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **What Happened Starter:** Parliament passed new taxes on imported goods including... [Word Bank: tea, glass, paper, duties]
- **So What Starter:** This was important because it proved that Parliament... [Word Bank: consent, authority, taxes]
- **Central Synthesis Frame:** Colonial resistance broadened during the Townshend Acts because [women / everyday colonists] took action by [boycotting / making homespun goods], showing Britain that colonies would resist unjust taxes.""",
    },
    {
        "code": "ci_04_cer_paragraph",
        "name": "Claim–Evidence–Reasoning (CER) Central Idea Frame",
        "short_name": "Claim–Evidence–Reasoning (CER)",
        "best_for": "Structured 3-sentence historical writing that fits cleanly in the last 10 minutes of a 40-minute class.",
        "description": "Students write a 1-sentence Claim stating the section's central idea, cite 1 specific piece of Evidence from the text, and add 1 sentence of Reasoning.",
        "visual_preview_md": """**Central Idea Focus Question:** Why was the Boston Massacre a critical turning point on the road to revolution?
- **CLAIM (State the central idea in 1 complete sentence):**
  _________________________________________________________________________________
- **EVIDENCE (Cite 1 specific detail, event, or quote from page 184):**
  _________________________________________________________________________________
- **REASONING (Explain how this evidence proves why colonial attitudes shifted):**
  _________________________________________________________________________________""",
        "exemplar_md": """**Central Idea Focus (Student Exemplar):**
- **CLAIM:** The Boston Massacre served as powerful anti-British propaganda that united colonial outrage against military occupation.
- **EVIDENCE:** According to page 184, Paul Revere created an engraving titled "The Bloody Massacre" showing armed soldiers firing into an orderly crowd of unarmed citizens.
- **REASONING:** Even though the clash began as a chaotic riot, the widely distributed image convinced colonists throughout North America that British troops were dangerous oppressors who would kill their own subjects.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Claim Starter:** The Boston Massacre was a turning point because colonial leaders used it as [propaganda] to... [Word Bank: unite, outrage, occupation]
- **Evidence Starter:** According to page 184 [¶3], Paul Revere created an engraving that depicted...
- **Reasoning Starter:** This evidence proves that colonial attitudes shifted because the image convinced people that British soldiers were...""",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 2. THREE ANTI-COPYCAT MODES FOR THE TEXTBOOK'S PRINTED "MAIN IDEA" BOX
# ─────────────────────────────────────────────────────────────────────────────

PRINTED_MAIN_IDEA_MODES: List[Dict[str, str]] = [
    {
        "code": "pmi_01_prove_it",
        "name": "Mode A: 'Prove the Textbook's Main Idea' (Pre-Print & Cite Evidence)",
        "short_name": "Prove the Textbook's Main Idea",
        "description": "Pre-prints the textbook's exact 1-sentence MAIN IDEA box right on the worksheet so students cannot copy it as their own answer—instead, they must cite 1 specific detail from each subheading that proves it.",
        "visual_preview_md": """┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TEXTBOOK PRINTED MAIN IDEA (p. 178)                                                    │
│ "The British government made new laws that tightened control over the American colonies."│
└────────────────────────────────────────────────────────────────────────────────────────┘

**Note: DO NOT copy the statement above!** Prove that this statement is true by finding 2 specific historical facts from the reading:
- **Proof 1 (from Subheading 1: PROBLEMS ARISE, p. 178):**
  ............................................................................................................................................
- **Proof 2 (from Subheading 2: SOLDIERS IN THE COLONIES, p. 178):**
  ............................................................................................................................................""",
        "exemplar_md": """**Student Exemplar:**
- **Proof 1 (PROBLEMS ARISE, p. 178):** Following the war, King George III issued the Proclamation of 1763, which legally forbade American settlers from moving west of the Appalachian Mountains.
- **Proof 2 (SOLDIERS IN THE COLONIES, p. 178):** Parliament passed the Quartering Act of 1765, requiring local colonial governments and citizens to supply barracks and housing for 10,000 British troops.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Proof 1 Stem (p. 178, ¶3):** The British government restricted colonists by issuing the... [Word Bank: Proclamation of 1763, Appalachian Mountains]
- **Proof 2 Stem (p. 178, ¶5):** Parliament exerted military control by passing the... [Word Bank: Quartering Act, soldiers, housing]""",
    },
    {
        "code": "pmi_02_subheading_focus",
        "name": "Mode B: 'Subheading Central Ideas' (Target the Unprinted Subsections)",
        "short_name": "Subheading Central Ideas",
        "description": "Since the textbook only prints a general section-wide Main Idea, students must determine the unprinted Central Idea of each individual subheading and explain how they connect.",
        "visual_preview_md": """*Notice: The textbook already printed a general summary for the whole spread. Your job is to determine the unprinted Central Idea for each individual section:*

- **Subheading 1 Central Idea (PROBLEMS ARISE, p. 178):**
  _________________________________________________________________________________
- **Subheading 2 Central Idea (A PROCLAMATION LINE, p. 179):**
  _________________________________________________________________________________

**Connection:** How did the events in Subheading 1 directly cause the conflict in Subheading 2?
_________________________________________________________________________________""",
        "exemplar_md": """**Student Exemplar:**
- **Subheading 1 Central Idea:** Winning the French and Indian War gave Britain vast new western territory but left the empire with staggering debt that British leaders expected colonies to finance.
- **Subheading 2 Central Idea:** To avoid expensive conflicts with Native American nations, Britain banned colonial settlement west of the Appalachians, enraging land speculators and colonists who fought for that land.
- **Connection:** Because Britain was deep in debt from the war, it could not afford new frontier wars, leading directly to the unpopular Proclamation Line.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Subheading 1 Stem:** After defeating France, Great Britain faced two major challenges: [land / territory] and [debt / money].
- **Subheading 2 Stem:** The Proclamation of 1763 angered colonists because they felt King George was taking away their right to... [Word Bank: settle, farm, western lands]
- **Connection Stem:** Because Britain was in debt from the war, King George tried to avoid further conflict by...""",
    },
    {
        "code": "pmi_03_upgrade_it",
        "name": "Mode C: 'Upgrade the Textbook's Main Idea' (Expand with Specifics)",
        "short_name": "Upgrade the Textbook's Main Idea",
        "description": "Shows the textbook's brief 1-sentence MAIN IDEA and challenges students to rewrite and upgrade it into a specific 8th-grade historical claim naming the exact laws, people, and consequences.",
        "visual_preview_md": """┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TEXTBOOK'S BASIC MAIN IDEA (5th Grade Level)                                           │
│ "Colonists protested British taxes."                                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘

**UPGRADE CHALLENGE:** Upgrade this basic sentence into a mature 8th-grade historical claim. You must include: (1) The specific tax or law, (2) Who protested, and (3) The specific method of resistance:
_________________________________________________________________________________
_________________________________________________________________________________""",
        "exemplar_md": """**Student Exemplar (Upgraded Claim):**
When Parliament imposed the Stamp Act to tax colonial documents without consent, organized groups like the Sons of Liberty and colonial merchants launched widespread boycotts and protests that forced Britain to repeal the act.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Upgrade Checklist:** [ ] Named the specific law (Stamp Act) | [ ] Named the resistance group (Sons of Liberty / Merchants) | [ ] Named the action (boycotts / protests)
- **Sentence Starter:** When Parliament passed the ______________, colonial groups like the ______________ resisted by ______________, proving that colonies would fight taxation without representation.""",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 3. FIVE ACTIVE READING & HISTORICAL TEXT STRUCTURE ORGANIZERS (CCSS RH.6-8.5)
# ─────────────────────────────────────────────────────────────────────────────

READING_ORGANIZERS: List[Dict[str, str]] = [
    {
        "code": "read_01_cause_effect",
        "name": "Text Structure: Historical Cause & Effect Table",
        "short_name": "Cause & Effect Table",
        "requires_audit": "cause_effect",
        "description": "Two-column graphic organizer where students connect explicit historical causes to their colonial/national effects across the section's subheadings.",
        "visual_preview_md": """| HISTORICAL CAUSE (Action / Policy / Event) | HISTORICAL EFFECT (Colonial Reaction / Outcome) |
| :--- | :--- |
| **Cause 1:** Britain stationed 10,000 soldiers in the colonies and passed the Quartering Act (p. 178). | **Effect 1:** .........................................................................<br>......................................................................................... |
| **Cause 2:** .........................................................................<br>......................................................................................... | **Effect 2:** Pontiac led Native American attacks on British frontier forts (p. 179). |""",
        "exemplar_md": """**Student Exemplar:**
| HISTORICAL CAUSE (Action / Policy / Event) | HISTORICAL EFFECT (Colonial Reaction / Outcome) |
| :--- | :--- |
| **Cause 1:** Britain stationed 10,000 soldiers in the colonies and passed the Quartering Act (p. 178). | **Effect 1:** Colonists, especially in New York, felt their rights were violated and assemblies refused to pay for soldiers' supplies. |
| **Cause 2:** British settlers moved onto Native American lands west of the Appalachian Mountains without compensation (p. 179). | **Effect 2:** Pontiac led Native American attacks on British frontier forts, prompting the Proclamation of 1763. |""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Effect 1 Starter:** *As a result,* ____________________________________
- **Cause 2 Starter:** *Because* _______________________________________""",
    },
    {
        "code": "ro_02_multi_section_cause_effect",
        "name": "Multi-Section Cause & Effect Synthesis",
        "short_name": "Multi-Section Cause & Effect",
        "requires_audit": "cause_effect",
        "description": "Cross-section synthesis organizer tracing cascading historical causes and consequences across 2 or 3 section spreads (4 to 6 rows).",
        "visual_preview_md": """| Section & Subheading | Historical Cause (Action / Policy / Event) | Historical Effect (Reaction / Outcome) |
| :--- | :--- | :--- |
| **Sec 1.1 • 1. PROBLEMS ARISE** | King George III wanted to maintain control after the French and Indian War. | **Effect 1:** ......................................................................... |
| **Sec 1.1 • 2. SOLDIERS IN THE COLONIES** | ......................................................................... | The king issued the Proclamation of 1763 to stop western settlement. |
| **Sec 1.2 • 3. WAR DEBT** | Britain accumulated massive debt from the French and Indian War. | **Effect 3:** ......................................................................... |""",
        "exemplar_md": """**Student Exemplar:**
| Section & Subheading | Historical Cause (Action / Policy / Event) | Historical Effect (Reaction / Outcome) |
| :--- | :--- | :--- |
| **Sec 1.1 • 1. PROBLEMS ARISE** | King George III wanted to maintain control after the French and Indian War. | Colonists grew resentful of royal proclamations restricting western expansion. |
| **Sec 1.1 • 2. SOLDIERS IN THE COLONIES** | Britain stationed 10,000 soldiers in colonial towns to enforce royal rule. | Parliament passed the Quartering Act forcing colonists to house British troops. |
| **Sec 1.2 • 3. WAR DEBT** | Britain accumulated massive debt from the French and Indian War. | Prime Minister George Grenville decided to tax the colonies directly for revenue. |""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Odd Row Starters:** *As a result,* ____________________________________
- **Even Row Starters:** *Because* _______________________________________""",
    },
    {
        "code": "read_02_say_something",
        "name": "'Say Something!' Subheading Check-Ins (Stop & Jot)",
        "short_name": "'Say Something!' by Subheading",
        "requires_audit": "always_valid",
        "description": "After reading each subheading (aloud, with a partner, or independently), students answer a targeted comprehension/central-idea question in a complete sentence.",
        "visual_preview_md": """- **Subheading 1: PROBLEMS ARISE (p. 178)**
  *Stop & Jot:* What was the most serious problem Great Britain faced after winning the French and Indian War?
  _________________________________________________________________________________
- **Subheading 2: SOLDIERS IN THE COLONIES (p. 178)**
  *Stop & Jot:* Why did American colonists view the presence of British peacetime soldiers with suspicion?
  _________________________________________________________________________________""",
        "exemplar_md": """**Student Exemplar:**
- **PROBLEMS ARISE (p. 178):** The most serious problem was that Britain was left with massive war debt of over 130 million pounds, while gaining a vast frontier that was expensive to defend.
- **SOLDIERS IN THE COLONIES (p. 178):** Colonists feared the soldiers were stationed in colonial cities not to protect them from enemies, but to enforce royal laws and strip away colonial self-government.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Subheading 1 Stem:** Great Britain's most urgent problem was [paying off wartime debts / governing new territory].
- **Subheading 2 Stem:** Colonists suspected the British soldiers were sent to [control colonial towns / enforce taxes], not protect them.""",
    },
    {
        "code": "read_03_cloze_guided",
        "name": "Guided Cloze Notes by Subheading (Key Concepts)",
        "short_name": "Guided Cloze Notes",
        "requires_audit": "always_valid",
        "description": "Structured statements organized by subheading where students fill in essential historical terms and answer a synthesis check.",
        "visual_preview_md": """*Word Bank: Proclamation of 1763, debt, Quartering Act, Appalachian, 10,000*

**1. PROBLEMS ARISE & SOLDIERS (p. 178):**
Following the French and Indian War, Great Britain had huge war ______________. To maintain control, Parliament kept ______________ troops stationed in the colonies and passed the ______________, requiring colonists to house them.

**2. A PROCLAMATION LINE (p. 179):**
To prevent further conflicts with Native Americans, King George issued the ______________, forbidding settlers from moving west of the ______________ Mountains.""",
        "exemplar_md": """**Student Exemplar:**
**1. PROBLEMS ARISE & SOLDIERS (p. 178):**
Following the French and Indian War, Great Britain had huge war **debt**. To maintain control, Parliament kept **10,000** troops stationed in the colonies and passed the **Quartering Act**, requiring colonists to house them.

**2. A PROCLAMATION LINE (p. 179):**
To prevent further conflicts with Native Americans, King George issued the **Proclamation of 1763**, forbidding settlers from moving west of the **Appalachian** Mountains.""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- Word bank included directly on page.
- First letter clues provided for struggling readers: d____ (debt), Q________ Act (Quartering Act).""",
    },
    {
        "code": "read_04_sequence_timeline",
        "name": "Text Structure: Chronological Sequence / Event Tracker",
        "short_name": "Chronological Sequence",
        "requires_audit": "sequence",
        "description": "Step-by-step chronological table tracking how a crisis, battle, or political process unfolded across the 2-page spread.",
        "visual_preview_md": """| CHRONOLOGICAL ORDER | HISTORICAL EVENT & PAGE | WHAT OCCURRED? (Brief Summary) |
| :---: | :--- | :--- |
| **STEP 1** | 1763: Treaty of Paris & Debt (p. 178) | Britain defeats France and gains Canada and land east of Mississippi. |
| **STEP 2** | Spring 1763: Pontiac's War (p. 179) | .................................................................................................... |
| **STEP 3** | Fall 1763: Proclamation of 1763 (p. 179) | .................................................................................................... |""",
        "exemplar_md": """**Student Exemplar:**
| CHRONOLOGICAL ORDER | HISTORICAL EVENT & PAGE | WHAT OCCURRED? (Brief Summary) |
| :---: | :--- | :--- |
| **STEP 1** | 1763: Treaty of Paris & Debt (p. 178) | Britain defeats France and gains Canada and land east of Mississippi. |
| **STEP 2** | Spring 1763: Pontiac's War (p. 179) | Ottawa chief Pontiac unites tribes to attack British forts to defend lands. |
| **STEP 3** | Fall 1763: Proclamation of 1763 (p. 179) | King George forbids colonial settlement west of the Appalachians to calm frontier. |""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Step 2 Starter:** Pontiac and Native allies attacked British forts because... [Word Bank: settlements, frontier, defend]
- **Step 3 Starter:** The British government reacted to the rebellion by issuing... [Word Bank: Proclamation, forbid, Appalachians]""",
    },
    {
        "code": "read_05_compare_perspectives",
        "name": "Text Structure: Competing Perspectives / Compare & Contrast",
        "short_name": "Competing Perspectives Matrix",
        "requires_audit": "compare",
        "description": "Side-by-side matrix comparing two historical viewpoints (e.g., British Parliament vs. Colonial Patriots, Loyalists vs. Patriots) using evidence from the page.",
        "visual_preview_md": """| ISSUE / POLICY (pp. 178–179) | BRITISH GOVERNMENT PERSPECTIVE | AMERICAN COLONISTS PERSPECTIVE |
| :--- | :--- | :--- |
| **Stationing Troops in America** | Believed troops were needed to protect frontiers and colonies should pay for defense. | __________________________________________<br>__________________________________________ |
| **Proclamation of 1763** | __________________________________________<br>__________________________________________ | Believed Britain had no right to trap them east of the mountains after they fought for the land. |""",
        "exemplar_md": """**Student Exemplar:**
| ISSUE / POLICY (pp. 178–179) | BRITISH GOVERNMENT PERSPECTIVE | AMERICAN COLONISTS PERSPECTIVE |
| :--- | :--- | :--- |
| **Stationing Troops in America** | Believed troops were needed to protect frontiers and colonies should pay for defense. | Feared peacetime troops were stationed in cities to intimidate citizens and suppress colonial liberties. |
| **Proclamation of 1763** | Wanted to prevent costly wars with Native American tribes and stabilize the imperial frontier. | Believed Britain had no right to trap them east of the mountains after they fought for the land. |""",
        "scaffolded_md": """*Scaffolded Support Elements:*
- **Colonist View Stem:** Colonists opposed the troops because they viewed them as... [Word Bank: threats, tyranny, unnecessary]
- **British View Stem:** King George issued the Proclamation because Britain could not afford... [Word Bank: war, debt, Native conflicts]""",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 4. PLUG-AND-PLAY TEXTBOOK BUILDING BLOCKS (VOCAB, READING CHECK, VISUALS)
# ─────────────────────────────────────────────────────────────────────────────

VOCAB_MODES: List[Dict[str, str]] = [
    {
        "code": "vocab_official_box",
        "name": "Compact Official Textbook Vocabulary Box (2–4 Terms from pp. R44–R58)",
        "short_name": "Official Vocab Box",
        "description": "Prints the section's official Content & Academic Vocabulary with student-friendly textbook definitions and a quick 2-minute context connection task in a neat 3-column table.",
        "preview_text": "| Key Term & Page | Official Textbook Definition | Connection to Section? |\n| :--- | :--- | :--- |",
    },
    {
        "code": "vocab_word_meaning_q3",
        "name": "Built-In '#3 Determine Word Meaning' Context Check (1 Fast Question)",
        "short_name": "Built-In #3 Word Meaning Check",
        "description": "Uses the textbook's own bottom-of-page '#3 Determine Word Meaning' question so students practice context-clue vocabulary in under 2 minutes without a full table.",
        "preview_text": "**Context Vocabulary Check (p. 179):** Determine the meaning of the word *tyranny* as used in paragraph 4.",
    },
    {
        "code": "vocab_embedded_only",
        "name": "Embedded Terms Only (Bold Terms Woven Into Reading Questions)",
        "short_name": "Embedded Terms Only",
        "description": "Weaves essential vocabulary words in bold directly into the reading organizer prompts rather than printing a separate vocabulary section.",
        "preview_text": "*No separate vocab table — key terms like **boycott** and **quartering** appear bolded in the questions below.*",
    },
    {
        "code": "vocab_none",
        "name": "No Vocabulary Section (Zero Vocab — Maximum Space for History Content)",
        "short_name": "Zero Vocab (Skip Vocabulary)",
        "description": "Completely removes the vocabulary block from worksheets and answer keys, dedicating 100% of page space to historical reading, questions, and Central Idea.",
        "preview_text": "*Zero vocabulary elements printed on worksheets. Maximum space reserved for historical analysis.*",
    },
]

READING_MODES: List[Dict[str, str]] = [
    {
        "code": "mode_mixed_flexible",
        "name": "Flexible Reading Mode (Daily Mix: Read-Aloud, Partner, or Independent)",
        "short_name": "Flexible Reading Mode",
        "description": "Neutral instructions that allow you to change your classroom routine day-by-day (e.g., teacher read-aloud on Monday, partner work on Tuesday) without needing different printed handouts.",
        "directions_prefix": "As we read each subheading together or with your partner,",
        "preview_text": "As we read each subheading together or with your partner, record your answers below.",
    },
    {
        "code": "mode_read_aloud",
        "name": "Whole-Class Teacher Read-Aloud (Whole-Class Pause & Jot)",
        "short_name": "Whole-Class Pause & Jot",
        "description": "Designed for teacher-led oral reading or playing textbook audio. Instructions tell students to listen during reading and pause for brief 60-second writing check-ins after each subheading.",
        "directions_prefix": "Pause after each subheading during our class reading to",
        "preview_text": "Pause after each subheading during our class reading to discuss and record your answer.",
    },
    {
        "code": "mode_partner",
        "name": "Partner Chunked Reading (Turn & Talk + Collaborative Writing)",
        "short_name": "Partner Turn & Talk",
        "description": "Designed for student pairs. Partners alternate reading paragraphs aloud, discuss the checkpoint prompt, and agree on their written answer before moving to the next section.",
        "directions_prefix": "Read each subheading with your partner, discuss the question, and",
        "preview_text": "Read each subheading with your partner, discuss the question, and write your answer together.",
    },
    {
        "code": "mode_independent",
        "name": "Independent Reading with Paragraph Locators ([¶1]..[¶N])",
        "short_name": "Independent Silent Reading",
        "description": "Designed for individual silent reading. Handouts feature specific paragraph number citations ([¶2], [¶4]) so students can locate evidence independently without teacher prompting.",
        "directions_prefix": "Read the assigned pages independently and use the paragraph locators to",
        "preview_text": "Read the assigned pages independently and use the paragraph locators [¶1]..[¶N] to complete your notes.",
    },
    {
        "code": "mode_custom_other",
        "name": "Custom Routine / Other (Teacher-Specified Directions)",
        "short_name": "Custom Routine (Other)",
        "description": "Allows you to write your own custom classroom routine or worksheet instructions (e.g., station rotations, audio listening stations, table group debriefs).",
        "directions_prefix": "Follow teacher directions to",
        "preview_text": "Follow teacher directions to complete your reading checkpoint.",
    },
]

COVER_PAGE_MODES: List[Dict[str, str]] = [
    {
        "code": "central_idea_tracker",
        "name": "Central Idea Study Guide Tracker (Recommended)",
        "short_name": "Central Idea Study Guide Tracker",
        "description": "Formats the front cover of the booklet as a cumulative study guide. Every section in the unit gets a row with its title and lines for students to record their 1-sentence Central Idea, creating an end-of-chapter review sheet.",
        "preview_text": "┌─────────────────────────────────────────────────────────────┐\n│ CHAPTER 5 CUMULATIVE CENTRAL IDEA STUDY GUIDE TRACKER      │\n├─────────────────────────────────────────────────────────────┤\n│ Sec 1.1: Tighter British Control (pp. 178–179)              │\n│ Central Idea: _____________________________________________ │\n│ Sec 1.2: Colonial Resistance (pp. 180–181)                  │\n│ Central Idea: _____________________________________________ │\n└─────────────────────────────────────────────────────────────┘",
    },
    {
        "code": "score_checklist",
        "name": "Section Score & Teacher Stamp Table",
        "short_name": "Section Score / Stamp Table",
        "description": "Formats the front cover as an accountability and grading tracker table where you can stamp, initial, or record points (e.g. 10 pts per section) as students finish each day's lesson.",
        "preview_text": "| Section # & Title | Date Assigned | Status / Points | Teacher Stamp / Initial |\n| :--- | :---: | :---: | :---: |\n| Sec 1.1: Tighter British Control | [   /   ] | _____ / 10 | [   STAMP   ] |\n| Sec 1.2: Colonial Resistance    | [   /   ] | _____ / 10 | [   STAMP   ] |",
    },
    {
        "code": "none",
        "name": "No Front Cover Page (Saves 1 Sheet of Paper)",
        "short_name": "No Front Cover Page",
        "description": "Leaves out the cover page entirely. The student booklet begins immediately on Section 1, saving 1 sheet of paper per student when stapling.",
        "preview_text": "*No separate front cover sheet. The packet starts immediately on Page 1 with your first selected section spread.*",
    },
]

GRADE_BOX_MODES: List[Dict[str, str]] = [
    {
        "code": "points_100",
        "name": "100-Point Score Notation (Sec X.X   ___/100) — Default",
        "short_name": "100-Point Score (___/100)",
        "description": "Prints a simple, clean right-aligned score line in the footer of every worksheet page for quick grading.",
        "preview_text": "Sec 1.1   _____/100",
    },
    {
        "code": "points_10",
        "name": "10-Point Score Notation (Sec X.X   ___/10)",
        "short_name": "10-Point Score (___/10)",
        "description": "Prints a simple 10-point daily score line in the footer of every worksheet page.",
        "preview_text": "Sec 1.1   _____/10",
    },
    {
        "code": "stamp_box",
        "name": "Teacher Stamp / Initials Box",
        "short_name": "Teacher Stamp / Initials Box",
        "description": "Prints a clean rectangular stamp/signature box in the footer of every worksheet page for quick classroom walkthrough grading.",
        "preview_text": "Teacher Stamp / Initials: [         ]",
    },
    {
        "code": "none",
        "name": "No Footer Check Box",
        "short_name": "No Footer Check Box",
        "description": "Omits any grading box from the bottom of the page, giving maximum vertical space for student writing.",
        "preview_text": "*No score box printed in the page footer.*",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 5. OPTIONAL WRITING REVOLUTION (TWR) DRAWER (OFF BY DEFAULT)
# ─────────────────────────────────────────────────────────────────────────────

OPTIONAL_TWR_STRATEGIES: List[Dict[str, str]] = [
    {
        "code": "twr_none",
        "name": "None (Pure Central Idea & Historical Literacy Focus — Default)",
        "short_name": "No TWR (Default)",
        "description": "Uses pure Central Idea, CER, or 1-sentence synthesis frames without Hochman TWR rules.",
        "visual_preview_md": "*No TWR writing extension selected. Worksheets will focus purely on passage reading comprehension, vocabulary, and Central Idea synthesis.*",
        "exemplar_md": "*Standard 40-minute layout without sentence-level conjunction exercises.*",
    },
    {
        "code": "twr_because_but_so",
        "name": "Because, But, So (Cause, Contrast, Effect)",
        "short_name": "Because, But, So",
        "description": "Expands a core historical stem from the section using 'because', 'but', and 'so'.",
        "visual_preview_md": """**Historical Sentence Expansion: Because, But, So**
*Core Stem:* Great Britain passed new taxes on American colonists...
- ...**because** _________________________________________________________________
- ...**but** _____________________________________________________________________
- ...**so** ______________________________________________________________________""",
        "exemplar_md": """**Student Exemplar:**
- ...**because** it needed revenue to pay down the massive imperial debts from the French and Indian War.
- ...**but** colonists argued Parliament had no legal right to tax them without representation in government.
- ...**so** merchants and citizens organized boycotts against British goods, forcing Parliament to reconsider.""",
    },
    {
        "code": "twr_subordinating",
        "name": "Subordinating Conjunctions (Although, When, After, Since)",
        "short_name": "Subordinating Conjunctions",
        "description": "Completes complex historical sentences starting with dependent clauses.",
        "visual_preview_md": """**Complex Historical Sentences:**
- **Although** Parliament repealed the Stamp Act, ___________________________________
- **After** King George issued the Proclamation of 1763, ___________________________
- **Since** colonists could not elect members to Parliament, _______________________""",
        "exemplar_md": """**Student Exemplar:**
- **Although** Parliament repealed the Stamp Act, it immediately passed the Declaratory Act asserting absolute authority over the colonies.
- **After** King George issued the Proclamation of 1763, angry colonial settlers and speculators ignored the law and moved west anyway.
- **Since** colonists could not elect members to Parliament, they rejected all direct taxes as unconstitutional violations of English rights.""",
    },
    {
        "code": "twr_appositives",
        "name": "Appositives (Defining Historical Figures & Laws)",
        "short_name": "Appositives",
        "description": "Inserts a descriptive noun phrase between commas immediately after a historical person, group, or act.",
        "visual_preview_md": """**Appositive Sentence Construction:**
*Insert a descriptive noun phrase between commas to define the historical term:*
1. Patrick Henry, _____________________________________, delivered a famous speech against the Stamp Act.
2. The Sons of Liberty, _____________________________________, organized street protests and enforced boycotts.""",
        "exemplar_md": """**Student Exemplar:**
1. Patrick Henry, **a fiery young member of the Virginia House of Burgesses**, delivered a famous speech against the Stamp Act.
2. The Sons of Liberty, **a secret colonial resistance network formed in Boston and New York**, organized street protests and enforced boycotts.""",
    },
    {
        "code": "twr_kernel_expansion",
        "name": "Sentence Expansion (When? Where? Why?)",
        "short_name": "Sentence Expansion",
        "description": "Expands a short kernel sentence using dotted question notes into one complete historical sentence.",
        "visual_preview_md": """**Sentence Expansion:**
*Kernel:* Colonists protested.
- *When?* ...........................................................................................................
- *Where?* ..........................................................................................................
- *Why?* ............................................................................................................
**Expanded Historical Sentence:**
_________________________________________________________________________________""",
        "exemplar_md": """**Student Exemplar:**
*Kernel:* Colonists protested.
- *When?* In 1765 after the Stamp Act was announced
- *Where?* In port cities like Boston and New York
- *Why?* To demand that only their elected assemblies could tax them
**Expanded Historical Sentence:**
In 1765, colonists in port cities like Boston and New York actively protested against the Stamp Act to demand that only their elected assemblies could impose taxes.""",
    },
    {
        "code": "twr_spo",
        "name": "Single-Paragraph Outline (SPO — Topic Sentence + 4 Notes + Clincher)",
        "short_name": "Single-Paragraph Outline (SPO)",
        "description": "Plans a central-idea paragraph with a Topic Sentence (solid line), 4 detail notes (dotted lines), and Concluding Sentence.",
        "visual_preview_md": """**Single-Paragraph Outline (SPO):**
- **Topic Sentence (Central Idea):** _____________________________________________
  1. Detail 1: ...................................................................................................
  2. Detail 2: ...................................................................................................
  3. Detail 3: ...................................................................................................
- **Concluding Sentence (Clincher):** ___________________________________________""",
        "exemplar_md": """**Student Exemplar:**
- **Topic Sentence:** British economic policies after 1763 pushed American colonists toward open rebellion.
  1. Detail 1: Stamp Act taxed everyday legal documents and newspapers without colonial consent.
  2. Detail 2: Quartering Act forced colonial assemblies to feed and house peacetime British troops.
  3. Detail 3: Boston Massacre highlighted growing violence between occupied citizens and British redcoats.
- **Concluding Sentence:** As Parliament continued to ignore colonial petitions, colonists concluded that peaceful compromise within the empire was no longer possible.""",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 6. OSPI 8TH GRADE SOCIAL STUDIES & SUPPORTING ELA STANDARDS BY CHAPTER
# ─────────────────────────────────────────────────────────────────────────────

CHAPTER_STANDARDS_MAP: Dict[str, Dict[str, Any]] = {
    "1": {
        "chapter_num": 1,
        "chapter_title": "Three Worlds Before 1500",
        "essential_question": "How did the diverse cultures of the Americas, Europe, and Africa develop and interact before 1500?",
        "ospi_standards": [
            "G1.6-8.5: Explain and analyze physical and cultural characteristics of places and regions.",
            "G2.6-8.6: Analyze how the environment has affected Indigenous peoples and how they adapted.",
            "H2.6-8.6: Explain how cultures and ethnic groups contributed to the history of the Americas.",
        ],
        "ela_support_standards": [
            "RH.6-8.2: Determine the central ideas of a primary or secondary source and provide an accurate summary.",
            "RH.6-8.1: Cite specific textual evidence to support analysis of primary and secondary sources.",
            "RH.6-8.4: Determine the meaning of domain-specific social studies words and phrases in a text.",
        ],
    },
    "2": {
        "chapter_num": 2,
        "chapter_title": "European Exploration of the Americas",
        "essential_question": "What drove European exploration, and what were the consequences of the encounter between worlds?",
        "ospi_standards": [
            "G2.6-8.7: Explain cultural diffusion and the Columbian Exchange among the Americas, Europe, and Africa.",
            "G2.6-8.8: Explain and analyze migration as a catalyst for historical change.",
            "E1.6-8.3: Analyze how groups and individuals considered economic costs and benefits.",
        ],
        "ela_support_standards": [
            "RH.6-8.2: Determine the central ideas of a source and provide an accurate summary distinct from prior knowledge.",
            "RH.6-8.5: Describe how a text presents information (e.g., sequentially, comparatively, causally).",
        ],
    },
    "3": {
        "chapter_num": 3,
        "chapter_title": "The Thirteen Colonies",
        "essential_question": "How did geography, religion, and economics shape the founding of the thirteen English colonies?",
        "ospi_standards": [
            "H2.6-8.6: Explain and analyze how cultures and ethnic groups contributed to U.S. history.",
            "G1.6-8.5: Explain and analyze physical and cultural characteristics of colonial regions.",
            "G2.6-8.8: Explain and analyze migration as a catalyst for the growth of the colonies.",
        ],
        "ela_support_standards": [
            "RH.6-8.2: Determine the central ideas of a historical source and summarize key developments.",
            "RH.6-8.1: Cite specific textual evidence to support analysis of historical texts.",
        ],
    },
    "4": {
        "chapter_num": 4,
        "chapter_title": "Colonial Development",
        "essential_question": "How did distinct economic, social, and political traditions develop across the American colonies?",
        "ospi_standards": [
            "E1.6-8.4: Analyze how colonial trade, agriculture, and mercantilism shaped regional economies.",
            "C1.6-8.1: Explain key ideals of representative government and colonial self-rule.",
            "H1.6-8.5: Explain how themes and developments help define eras in U.S. history.",
        ],
        "ela_support_standards": [
            "RH.6-8.2: Determine the central ideas or information of a primary or secondary source.",
            "RH.6-8.4: Determine the meaning of words and phrases as they are used in a text.",
        ],
    },
    "5": {
        "chapter_num": 5,
        "chapter_title": "The Road to Revolution",
        "essential_question": "Why did British policies after 1763 lead the American colonies to declare independence in 1776?",
        "ospi_standards": [
            "H1.6-8.6: Explain how themes and developments help to define eras in U.S. history from 1763 to 1877.",
            "H2.6-8.1: Explain and analyze how individuals and movements have shaped U.S. history (1763–1877).",
            "C1.6-8.2: Explain the structure of and key ideals set forth in the Declaration of Independence.",
            "E2.6-8.4: Analyze the role of government taxation, boycotts, and trade policies in the colonial crisis.",
            "SSS2.6-8.1: Create and use research questions to guide inquiry into historical issues.",
        ],
        "ela_support_standards": [
            "RH.6-8.2: Determine the central ideas or information of a primary or secondary source; provide an accurate summary of the source distinct from prior knowledge or opinions.",
            "RH.6-8.1: Cite specific textual evidence to support analysis of primary and secondary sources.",
            "RH.6-8.5: Describe how a text presents information (e.g., causally, chronologically, comparatively).",
            "WHST.6-8.2: Write informative/explanatory texts to examine a historical topic and convey ideas clearly.",
        ],
    },
}

# Populate sensible defaults for Chapters 6–17 so every chapter has standards ready
DEFAULT_LATER_CHAPTERS = {
    6: ("The American Revolution", "How were the American Patriots able to win independence against Great Britain?"),
    7: ("From Confederation to Constitution", "How did the Framers create a stronger national government while protecting individual rights?"),
    8: ("Launching a New Republic", "What precedents and challenges shaped the United States during its first presidencies?"),
    9: ("The Jefferson Era", "How did territorial expansion and foreign conflict test the young republic?"),
    10: ("Growth and Expansion", "How did the Industrial Revolution, cotton economy, and nationalism transform the nation?"),
    11: ("The Jackson Era", "How did political democracy expand while Native American nations faced forced removal?"),
    12: ("Manifest Destiny", "What motivated westward expansion, and what were its consequences for diverse peoples?"),
    13: ("Age of Reform", "How did reform movements, immigration, and abolitionism seek to reshape American society?"),
    14: ("A Divided Nation", "Why did compromises over slavery fail to prevent the nation from splitting apart?"),
    15: ("The Civil War Begins", "How did the resources, strategies, and early battles shape the course of the Civil War?"),
    16: ("Turning Points of the War", "How did emancipation and key military turning points lead to Union victory?"),
    17: ("Reconstruction", "How did Reconstruction transform the nation, and why did many of its promises go unfulfilled?"),
}

for _cnum, (_ctitle, _ceq) in DEFAULT_LATER_CHAPTERS.items():
    CHAPTER_STANDARDS_MAP[str(_cnum)] = {
        "chapter_num": _cnum,
        "chapter_title": _ctitle,
        "essential_question": _ceq,
        "ospi_standards": [
            "H1.6-8.6: Explain how themes and developments help to define eras in U.S. history (1763–1877).",
            "H2.6-8.1: Explain and analyze how individuals, movements, and events shaped U.S. history.",
            "C2.6-8.1: Analyze how constitutional principles and civic ideals were tested in U.S. history.",
        ],
        "ela_support_standards": [
            "RH.6-8.2: Determine the central ideas of a primary or secondary source and provide an accurate summary.",
            "RH.6-8.1: Cite specific textual evidence to support analysis of primary and secondary sources.",
            "RH.6-8.5: Describe how a text presents information (e.g., causally, chronologically, comparatively).",
        ],
    }


def get_strategy_by_code(collection: List[Dict[str, str]], code: str) -> Dict[str, str]:
    for item in collection:
        if item["code"] == code:
            return item
    return collection[0]
