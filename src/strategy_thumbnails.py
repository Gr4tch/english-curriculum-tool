"""
Visual Strategy Thumbnail Grid Component.
Provides styled, compact graphical miniature mockups of each curriculum strategy
for the all-in-one visual selection grid.
"""

from typing import Dict, List, Any, Optional

ALL_STRATEGY_TILES: List[Dict[str, Any]] = [
    # ── 1. CENTRAL IDEA STRATEGIES ──
    {
        "code": "ci_01_subheading_gist",
        "category": "Central Idea",
        "category_badge": "ws-badge-blue",
        "name": "Subheading Gists",
        "subtitle": "10-Word Subheading Checkpoints",
        "best_for": "Chunked partner reading across 2–3 subheadings; prevents cognitive overload.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="height:6px; width:45%; background:#3b82f6; border-radius:2px;"></div>
            <div style="font-size:8px; font-weight:700; color:#1e3a8a;">1. SUBHEADING (p. 1)</div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
            <div style="font-size:8px; font-weight:700; color:#1e3a8a;">2. SUBHEADING (p. 2)</div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
            <div style="border-top:1px dashed #cbd5e1; padding-top:2px; font-size:7px; color:#475569; font-weight:600;">Whole-Section Central Idea:</div>
            <div style="border-bottom:1px solid #64748b; height:4px;"></div>
        </div>
        """,
    },
    {
        "code": "ci_02_box_and_bullets",
        "category": "Central Idea",
        "category_badge": "ws-badge-blue",
        "name": "Box & Bullets",
        "subtitle": "Claim Box + 3 Supporting Details",
        "best_for": "Teaching students how specific historical facts prove an overarching central claim.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="background:#eff6ff; border:1px solid #bfdbfe; border-left:3px solid #1e3a8a; border-radius:3px; padding:3px;">
                <div style="font-size:7px; font-weight:700; color:#1e3a8a;">CENTRAL IDEA BOX</div>
                <div style="border-bottom:1px solid #64748b; height:3px; margin-top:2px;"></div>
            </div>
            <div style="display:flex; align-items:center; gap:4px; margin-top:2px;">
                <div style="width:4px; height:4px; background:#1e3a8a; border-radius:50%;"></div>
                <div style="flex:1; border-bottom:1px dotted #94a3b8;"></div>
            </div>
            <div style="display:flex; align-items:center; gap:4px;">
                <div style="width:4px; height:4px; background:#1e3a8a; border-radius:50%;"></div>
                <div style="flex:1; border-bottom:1px dotted #94a3b8;"></div>
            </div>
            <div style="display:flex; align-items:center; gap:4px;">
                <div style="width:4px; height:4px; background:#1e3a8a; border-radius:50%;"></div>
                <div style="flex:1; border-bottom:1px dotted #94a3b8;"></div>
            </div>
        </div>
        """,
    },
    {
        "code": "ci_03_what_so_what",
        "category": "Central Idea",
        "category_badge": "ws-badge-blue",
        "name": "What? + So What?",
        "subtitle": "Historical Fact + Significance Table",
        "best_for": "Helping 8th graders explain historical significance instead of just listing facts.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:4px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="display:flex; background:#e2e8f0; border-radius:2px; font-size:7px; font-weight:700; padding:2px;">
                <div style="width:50%; color:#1e293b;">WHAT HAPPENED?</div>
                <div style="width:50%; color:#1e3a8a;">SO WHAT?</div>
            </div>
            <div style="display:flex; gap:4px; padding:2px 0;">
                <div style="width:50%; border-bottom:1px dotted #94a3b8; height:12px;"></div>
                <div style="width:50%; border-bottom:1px dotted #94a3b8; height:12px;"></div>
            </div>
            <div style="display:flex; gap:4px; padding:2px 0;">
                <div style="width:50%; border-bottom:1px dotted #94a3b8; height:12px;"></div>
                <div style="width:50%; border-bottom:1px dotted #94a3b8; height:12px;"></div>
            </div>
            <div style="border-top:1px dashed #cbd5e1; font-size:6px; color:#475569; font-weight:600;">Synthesis Claim:</div>
            <div style="border-bottom:1px solid #64748b; height:3px;"></div>
        </div>
        """,
    },
    {
        "code": "ci_04_cer_paragraph",
        "category": "Central Idea",
        "category_badge": "ws-badge-blue",
        "name": "CER Frame",
        "subtitle": "Claim, Evidence, Reasoning Structure",
        "best_for": "Structured 3-sentence historical writing that fits in the last 10 minutes of class.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <span style="font-size:7px; font-weight:800; background:#dbeafe; color:#1e3a8a; padding:1px 3px; border-radius:2px;">CLAIM</span>
                <div style="border-bottom:1px solid #64748b; height:3px; margin-top:2px;"></div>
            </div>
            <div>
                <span style="font-size:7px; font-weight:800; background:#dcfce7; color:#166534; padding:1px 3px; border-radius:2px;">EVIDENCE</span>
                <div style="border-bottom:1px solid #64748b; height:3px; margin-top:2px;"></div>
            </div>
            <div>
                <span style="font-size:7px; font-weight:800; background:#fef3c7; color:#92400e; padding:1px 3px; border-radius:2px;">REASONING</span>
                <div style="border-bottom:1px solid #64748b; height:3px; margin-top:2px;"></div>
            </div>
        </div>
        """,
    },

    # ── 2. ANTI-COPYCAT MECHANICS ──
    {
        "code": "pmi_01_prove_it",
        "category": "Anti-Copycat",
        "category_badge": "ws-badge-amber",
        "name": "Prove It!",
        "subtitle": "Textbook Claim + Student Proofs",
        "best_for": "Pre-prints the textbook's printed Main Idea so students cannot copy it as their own answer.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="background:#fef2f2; border-left:3px solid #ef4444; padding:3px; font-size:7px; color:#991b1b; font-style:italic;">
                "Textbook Main Idea..."
            </div>
            <div style="font-size:7px; font-weight:700; color:#b45309;">DO NOT COPY! Find 2 proofs:</div>
            <div>
                <div style="font-size:7px; font-weight:600; color:#1e3a8a;">• Proof 1:</div>
                <div style="border-bottom:1px dotted #94a3b8; height:3px;"></div>
            </div>
            <div>
                <div style="font-size:7px; font-weight:600; color:#1e3a8a;">• Proof 2:</div>
                <div style="border-bottom:1px dotted #94a3b8; height:3px;"></div>
            </div>
        </div>
        """,
    },
    {
        "code": "pmi_02_subheading_focus",
        "category": "Anti-Copycat",
        "category_badge": "ws-badge-amber",
        "name": "Subheading Focus",
        "subtitle": "Unprinted Section Central Ideas",
        "best_for": "Forces students to analyze the unprinted subsections instead of copying the section summary.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; color:#64748b; font-style:italic;">Textbook printed only 1 sentence:</div>
            <div>
                <div style="font-size:7px; font-weight:700; color:#0f172a;">Subheading 1 Idea:</div>
                <div style="border-bottom:1px solid #64748b; height:3px;"></div>
            </div>
            <div>
                <div style="font-size:7px; font-weight:700; color:#0f172a;">Subheading 2 Idea:</div>
                <div style="border-bottom:1px solid #64748b; height:3px;"></div>
            </div>
            <div style="font-size:6px; color:#1e3a8a; font-weight:700;">Historical Connection:</div>
            <div style="border-bottom:1px solid #64748b; height:3px;"></div>
        </div>
        """,
    },
    {
        "code": "pmi_03_upgrade_it",
        "category": "Anti-Copycat",
        "category_badge": "ws-badge-amber",
        "name": "Upgrade the Claim",
        "subtitle": "5th-Grade Sentence → 8th-Grade Claim",
        "best_for": "Shows a basic 5th-grade sentence and challenges students to rewrite it with historical depth.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="background:#f1f5f9; text-decoration:line-through; font-size:7px; color:#94a3b8; padding:2px;">
                "Basic 5th-grade sentence..."
            </div>
            <div style="font-size:7px; font-weight:700; color:#1e3a8a;">UPGRADE CHALLENGE:</div>
            <div style="font-size:6px; color:#475569;">Include law, who resisted, and method:</div>
            <div style="border-bottom:1px solid #64748b; height:4px;"></div>
            <div style="border-bottom:1px solid #64748b; height:4px;"></div>
        </div>
        """,
    },

    # ── 3. ACTIVE READING ORGANIZERS ──
    {
        "code": "read_01_cause_effect",
        "category": "Active Reading",
        "category_badge": "ws-badge-green",
        "name": "Cause & Effect Table",
        "subtitle": "2-Column Causal Analysis",
        "best_for": "Tracking historical actions, British policies, and immediate colonial responses.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:4px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="display:flex; background:#dcfce7; border-radius:2px; font-size:7px; font-weight:700; padding:2px; color:#166534;">
                <div style="width:50%;">CAUSE (Action)</div>
                <div style="width:50%;">EFFECT (Result)</div>
            </div>
            <div style="display:flex; gap:4px; padding:2px 0;">
                <div style="width:50%; font-size:6px; color:#334155;">Stamp Act passed</div>
                <div style="width:50%; border-bottom:1px solid #64748b; height:6px;"></div>
            </div>
            <div style="display:flex; gap:4px; padding:2px 0;">
                <div style="width:50%; border-bottom:1px solid #64748b; height:6px;"></div>
                <div style="width:50%; font-size:6px; color:#334155;">Boycotts started</div>
            </div>
        </div>
        """,
    },
    {
        "code": "ro_02_multi_section_cause_effect",
        "category": "Active Reading",
        "category_badge": "ws-badge-green",
        "name": "Multi-Section Cause & Effect",
        "subtitle": "Cross-Section Flow (2–3 Spreads)",
        "best_for": "Tracing escalating historical causes and consequences across 2 or 3 sections.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:4px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="display:flex; background:#dcfce7; border-radius:2px; font-size:7px; font-weight:700; padding:2px; color:#166534;">
                <div style="width:34%;">SECTION</div>
                <div style="width:33%;">CAUSE</div>
                <div style="width:33%;">EFFECT</div>
            </div>
            <div style="display:flex; gap:2px; padding:1px 0; font-size:6px; color:#334155;">
                <div style="width:34%; font-weight:700;">Sec 1.1</div>
                <div style="width:33%;">War debt...</div>
                <div style="width:33%; border-bottom:1px solid #64748b; height:5px;"></div>
            </div>
            <div style="display:flex; gap:2px; padding:1px 0; font-size:6px; color:#334155;">
                <div style="width:34%; font-weight:700;">Sec 1.2</div>
                <div style="width:33%; border-bottom:1px solid #64748b; height:5px;"></div>
                <div style="width:33%;">Protests...</div>
            </div>
            <div style="display:flex; gap:2px; padding:1px 0; font-size:6px; color:#334155;">
                <div style="width:34%; font-weight:700;">Sec 1.3</div>
                <div style="width:33%;">Stamp Act...</div>
                <div style="width:33%; border-bottom:1px solid #64748b; height:5px;"></div>
            </div>
        </div>
        """,
    },
    {
        "code": "read_05_compare_perspectives",
        "category": "Active Reading",
        "category_badge": "ws-badge-green",
        "name": "Dual Perspectives",
        "subtitle": "Competing Historical Viewpoints",
        "best_for": "Comparing British Crown vs. Patriot colonists, or Loyalist vs. Patriot stances.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:4px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="display:flex; gap:4px; height:100%;">
                <div style="flex:1; background:#eff6ff; border:1px solid #bfdbfe; border-radius:3px; padding:3px;">
                    <div style="font-size:6px; font-weight:800; color:#1e3a8a;">SIDE A (British)</div>
                    <div style="border-bottom:1px dotted #94a3b8; height:4px; margin-top:4px;"></div>
                    <div style="border-bottom:1px dotted #94a3b8; height:4px; margin-top:2px;"></div>
                </div>
                <div style="flex:1; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:3px; padding:3px;">
                    <div style="font-size:6px; font-weight:800; color:#166534;">SIDE B (Colonists)</div>
                    <div style="border-bottom:1px dotted #94a3b8; height:4px; margin-top:4px;"></div>
                    <div style="border-bottom:1px dotted #94a3b8; height:4px; margin-top:2px;"></div>
                </div>
            </div>
        </div>
        """,
    },
    {
        "code": "read_04_sequence_timeline",
        "category": "Active Reading",
        "category_badge": "ws-badge-green",
        "name": "Chronological Timeline",
        "subtitle": "Sequential Event Tracker",
        "best_for": "Narrative battles, campaigns, and chronological escalations of crises.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:4px;">
                <div style="font-size:6px; font-weight:700; background:#3b82f6; color:#fff; padding:1px 3px; border-radius:2px;">STEP 1</div>
                <div style="flex:1; border-bottom:1px dotted #94a3b8;"></div>
            </div>
            <div style="display:flex; align-items:center; gap:4px;">
                <div style="font-size:6px; font-weight:700; background:#3b82f6; color:#fff; padding:1px 3px; border-radius:2px;">STEP 2</div>
                <div style="flex:1; border-bottom:1px dotted #94a3b8;"></div>
            </div>
            <div style="display:flex; align-items:center; gap:4px;">
                <div style="font-size:6px; font-weight:700; background:#3b82f6; color:#fff; padding:1px 3px; border-radius:2px;">STEP 3</div>
                <div style="flex:1; border-bottom:1px dotted #94a3b8;"></div>
            </div>
        </div>
        """,
    },
    {
        "code": "read_02_say_something",
        "category": "Active Reading",
        "category_badge": "ws-badge-green",
        "name": "'Say Something!' Jot",
        "subtitle": "Structured Stop & Jot Prompts",
        "best_for": "Collaborative paired reading where students stop at subheadings to discuss and jot.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="display:flex; gap:4px; align-items:center;">
                <span style="font-size:7px; font-weight:800; background:#dbeafe; color:#1e3a8a; padding:1px 3px; border-radius:2px;">TALK</span>
                <span style="font-size:7px; font-weight:700; color:#0f172a;">Stop & Discuss (p. 1)</span>
            </div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
            <div style="display:flex; gap:4px; align-items:center; margin-top:4px;">
                <span style="font-size:7px; font-weight:800; background:#dbeafe; color:#1e3a8a; padding:1px 3px; border-radius:2px;">TALK</span>
                <span style="font-size:7px; font-weight:700; color:#0f172a;">Stop & Discuss (p. 2)</span>
            </div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
        </div>
        """,
    },
    {
        "code": "read_03_cloze_guided",
        "category": "Active Reading",
        "category_badge": "ws-badge-green",
        "name": "Guided Cloze Notes",
        "subtitle": "Fill-in-the-Blank Scaffold",
        "best_for": "High-support reading for ELL and IEP students requiring structured sentence stems.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; color:#334155; line-height:1.3;">
                After the war, Britain had <span style="border-bottom:1px solid #1e3a8a; font-weight:700; color:#1e3a8a;">______</span>. King George issued the <span style="border-bottom:1px solid #1e3a8a; font-weight:700; color:#1e3a8a;">______</span> of 1763 to stop western settlement.
            </div>
            <div style="background:#e2e8f0; border-radius:2px; font-size:6px; padding:2px; color:#475569;">
                Word Bank: debt, Proclamation, taxes
            </div>
        </div>
        """,
    },

    # ── 4. THE WRITING REVOLUTION (TWR) ──
    {
        "code": "twr_because_but_so",
        "category": "The Writing Revolution",
        "category_badge": "ws-badge-amber",
        "name": "Because, But, So",
        "subtitle": "Cause, Contrast, and Effect Stems",
        "best_for": "Hochman method sentence expansion; trains complex historical reasoning.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; font-weight:600; color:#334155;">Britain passed taxes...</div>
            <div style="font-size:7px; color:#1e3a8a;"><b>...because</b> <span style="border-bottom:1px solid #94a3b8; display:inline-block; width:55%;"></span></div>
            <div style="font-size:7px; color:#1e3a8a;"><b>...but</b> <span style="border-bottom:1px solid #94a3b8; display:inline-block; width:68%;"></span></div>
            <div style="font-size:7px; color:#1e3a8a;"><b>...so</b> <span style="border-bottom:1px solid #94a3b8; display:inline-block; width:72%;"></span></div>
        </div>
        """,
    },
    {
        "code": "twr_subordinating",
        "category": "The Writing Revolution",
        "category_badge": "ws-badge-amber",
        "name": "Subordinating Conjunctions",
        "subtitle": "Although / Since / Even Though",
        "best_for": "Teaching students to vary sentence structure and express conditional historical claims.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; color:#1e3a8a;"><b>Although</b> Parliament repealed...</div>
            <div style="border-bottom:1px solid #64748b; height:3px;"></div>
            <div style="font-size:7px; color:#1e3a8a;"><b>Since</b> colonists lacked votes...</div>
            <div style="border-bottom:1px solid #64748b; height:3px;"></div>
        </div>
        """,
    },
    {
        "code": "twr_kernel_expansion",
        "category": "The Writing Revolution",
        "category_badge": "ws-badge-amber",
        "name": "Sentence Expansion",
        "subtitle": "Kernel + Who, What, Where, Why",
        "best_for": "Expanding a bare 4-word historical kernel into a rich, evidence-based compound sentence.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; font-weight:700; color:#334155;">Kernel: Colonists protested.</div>
            <div style="font-size:6px; color:#64748b;">Who? / Where? / Why?</div>
            <div style="border-bottom:1px solid #64748b; height:4px;"></div>
            <div style="border-bottom:1px solid #64748b; height:4px;"></div>
        </div>
        """,
    },
    {
        "code": "twr_appositives",
        "category": "The Writing Revolution",
        "category_badge": "ws-badge-amber",
        "name": "Appositive Phrases",
        "subtitle": "Historical Noun Renaming",
        "best_for": "Integrating historical context and roles smoothly with commas (e.g., Patrick Henry, a fiery Virginia lawyer,...).",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; color:#334155; line-height:1.3;">
                Samuel Adams, <span style="background:#fef3c7; color:#92400e; padding:1px 2px; border-radius:2px;">[appositive]</span>, organized protests.
            </div>
            <div style="border-bottom:1px solid #64748b; height:4px;"></div>
            <div style="border-bottom:1px solid #64748b; height:4px;"></div>
        </div>
        """,
    },

    # ── 5. VOCABULARY & ASSESSMENT ──
    {
        "code": "vocab_deep_dive",
        "category": "Vocabulary",
        "category_badge": "ws-badge-blue",
        "name": "Vocabulary Practice",
        "subtitle": "Context Clues & Cloze Application",
        "best_for": "Reinforcing Tier-2/Tier-3 historical vocabulary directly from the textbook section.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; font-weight:700; color:#1e3a8a;">Section Official Vocabulary:</div>
            <div style="display:flex; gap:2px;">
                <span style="font-size:6px; background:#dbeafe; color:#1e3a8a; padding:1px 3px; border-radius:2px;">boycott</span>
                <span style="font-size:6px; background:#dbeafe; color:#1e3a8a; padding:1px 3px; border-radius:2px;">repeal</span>
                <span style="font-size:6px; background:#dbeafe; color:#1e3a8a; padding:1px 3px; border-radius:2px;">duty</span>
            </div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
        </div>
        """,
    },
    {
        "code": "section_assessment",
        "category": "Assessment",
        "category_badge": "ws-badge-blue",
        "name": "Section Check & Quiz",
        "subtitle": "Reading Checks & Critical Viewing",
        "best_for": "Formative section check with textbook questions and primary source image analysis.",
        "thumbnail_svg": """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:6px; height:74px; display:flex; flex-direction:column; justify-content:space-between;">
            <div style="font-size:7px; font-weight:700; color:#0f172a;">1. Reading Check Question:</div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
            <div style="font-size:7px; font-weight:700; color:#0f172a;">2. Critical Viewing Question:</div>
            <div style="border-bottom:1px dotted #94a3b8; height:4px;"></div>
        </div>
        """,
    },
]


import re

# Pre-clean all thumbnail HTML strings to prevent multiline indentation leaks in Markdown
for _t in ALL_STRATEGY_TILES:
    _t["thumbnail_svg"] = re.sub(r">\s*\n\s*<", "><", re.sub(r"\n\s*", " ", _t["thumbnail_svg"].strip()))


def get_tile_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Retrieves a strategy tile definition by code."""
    for t in ALL_STRATEGY_TILES:
        if t["code"] == code:
            return t
    return None
