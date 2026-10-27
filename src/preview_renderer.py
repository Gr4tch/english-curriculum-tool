"""
Worksheet Visual Preview & Exemplar Renderer
Renders crisp, professionally formatted HTML mockups of student worksheets,
authentic 8th-grade exemplars, and scaffolded support boxes.
"""

from typing import Dict, Any, Optional
import re
import textwrap


def _detect_strategy_category(strategy_code: str) -> str:
    if strategy_code.startswith("ci_"):
        return "central_idea"
    elif strategy_code.startswith("pmi_") or strategy_code.startswith("mode_"):
        return "anti_copycat"
    elif strategy_code.startswith("read_") or strategy_code.startswith("ro_"):
        return "reading_organizer"
    elif strategy_code.startswith("twr_"):
        return "twr"
    return "central_idea"


def _dedent_html(fn):
    """Ensures HTML preview strings have zero leading indentation to prevent Markdown code-block interpretation."""
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if isinstance(res, str):
            # Strip all leading/trailing whitespace from every line so no line ever starts with >=4 spaces
            return "\n".join(line.strip() for line in res.splitlines() if line.strip())
        return res
    return wrapper


COMMON_CSS = """
<style>
.ws-container {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 1.15rem 1.25rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04);
    margin-bottom: 0.75rem;
}
.ws-exemplar-container {
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-left: 5px solid #10b981;
    border-radius: 8px;
    padding: 1.15rem 1.25rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #14532d;
    line-height: 1.5;
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.05);
    margin-bottom: 0.75rem;
}
.ws-scaffold-container {
    background: #eff6ff;
    border: 1.5px solid #bfdbfe;
    border-left: 5px solid #3b82f6;
    border-radius: 8px;
    padding: 0.95rem 1.15rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e3a8a;
    line-height: 1.5;
    margin-top: 0.75rem;
}
.ws-title-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
}
.ws-badge-blue { background: #dbeafe; color: #1e3a8a; }
.ws-badge-green { background: #dcfce7; color: #15803d; }
.ws-badge-amber { background: #fef3c7; color: #b45309; }

.ws-callout {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #1e3a8a;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin: 0.65rem 0;
}
.ws-table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.75rem 0;
    font-size: 0.86rem;
}
.ws-table th {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    padding: 0.55rem 0.75rem;
    text-align: left;
    font-weight: 700;
    color: #0f172a;
}
.ws-table td {
    border: 1px solid #cbd5e1;
    padding: 0.6rem 0.75rem;
    vertical-align: top;
    color: #334155;
}
.ws-dotted-line {
    border-bottom: 1.5px dotted #94a3b8;
    height: 20px;
    margin: 3px 0 6px 0;
}
.ws-solid-line {
    border-bottom: 1.5px solid #64748b;
    height: 22px;
    margin: 4px 0 7px 0;
}
.ws-student-answer {
    color: #15803d;
    font-weight: 600;
    background: #dcfce7;
    padding: 0.1rem 0.35rem;
    border-radius: 3px;
}
</style>
"""


@_dedent_html
def render_preview_handout(
    strategy_code: str,
    section_meta: Optional[Dict[str, Any]] = None,
    is_scaffolded: bool = False,
    raw_passage_md: str = "",
) -> str:
    """Renders a realistic, clean printed student worksheet format."""
    if section_meta is not None:
        from src.packet_builder import build_standalone_strategy_handout
        cat_name = _detect_strategy_category(strategy_code)
        handout = build_standalone_strategy_handout(
            section_meta=section_meta,
            strategy_category=cat_name,
            strategy_code=strategy_code,
            markdown_text=raw_passage_md,
            is_scaffolded=is_scaffolded,
        )
        md_text = handout["student_scaffolded_md" if is_scaffolded else "student_standard_md"]
        return format_booklet_for_web(md_text)

    # ── CENTRAL IDEA STRATEGIES (Generic Template Fallback) ──
    if strategy_code == "ci_01_subheading_gist":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Model Strategy Template • Subheading Gists</div>
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.4rem;">Part 1: Subheading Gist Checkpoints</div>
            
            <div style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: #1e3a8a; font-size: 0.88rem;">1. PROBLEMS ARISE (p. 178)</div>
                <div style="font-style: italic; color: #64748b; font-size: 0.82rem;">10-Word Subheading Gist:</div>
                <div class="ws-dotted-line"></div>
                <div class="ws-dotted-line"></div>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: #1e3a8a; font-size: 0.88rem;">2. SOLDIERS IN THE COLONIES (p. 178)</div>
                <div style="font-style: italic; color: #64748b; font-size: 0.82rem;">10-Word Subheading Gist:</div>
                <div class="ws-dotted-line"></div>
                <div class="ws-dotted-line"></div>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: #1e3a8a; font-size: 0.88rem;">3. A PROCLAMATION LINE (p. 179)</div>
                <div style="font-style: italic; color: #64748b; font-size: 0.82rem;">10-Word Subheading Gist:</div>
                <div class="ws-dotted-line"></div>
                <div class="ws-dotted-line"></div>
            </div>

            <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed #cbd5e1;">
                <div style="font-weight: 700; color: #0f172a;">Part 2: Whole-Section Central Idea</div>
                <div style="font-style: italic; color: #64748b; font-size: 0.82rem; margin-bottom: 0.35rem;">
                    Combine your 3 gists into 1–2 complete sentences that state the author's overarching point:
                </div>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "ci_02_box_and_bullets":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Model Strategy Template • Box & Bullets</div>
            
            <div class="ws-callout" style="border-left: 5px solid #1e3a8a;">
                <div style="font-weight: 700; color: #1e3a8a; font-size: 0.88rem; margin-bottom: 0.25rem;">
                    CENTRAL IDEA BOX (Topic + Author's Overarching Claim)
                </div>
                <div style="font-style: italic; color: #64748b; font-size: 0.80rem; margin-bottom: 0.35rem;">
                    Write the main historical claim that explains the entire 2-page spread:
                </div>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>

            <div style="margin-top: 0.85rem;">
                <div style="font-weight: 700; color: #0f172a; font-size: 0.88rem; margin-bottom: 0.4rem;">
                    Supporting Bullets (Cite 3 specific details from the reading that prove your box):
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <b>• Supporting Detail 1 (p. 180):</b>
                    <div class="ws-dotted-line"></div>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <b>• Supporting Detail 2 (p. 180):</b>
                    <div class="ws-dotted-line"></div>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <b>• Supporting Detail 3 (p. 181):</b>
                    <div class="ws-dotted-line"></div>
                </div>
            </div>
        </div>
        """

    elif strategy_code == "ci_03_what_so_what":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Model Strategy Template • Historical 'What + So What?'</div>
            
            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 28%;">Subheading & Page</th>
                        <th style="width: 36%;">WHAT HAPPENED? (Key Fact)</th>
                        <th style="width: 36%;">SO WHAT? (Why did this matter?)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>1. The Townshend Acts (p. 182)</b></td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                    </tr>
                    <tr>
                        <td><b>2. Protests & Boycotts (p. 183)</b></td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                    </tr>
                </tbody>
            </table>

            <div style="margin-top: 0.75rem;">
                <b>Central Idea Synthesis:</b> <span style="font-style: italic; color: #64748b;">How did these events shift the relationship between Britain and the colonies?</span>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "ci_04_cer_paragraph":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Model Strategy Template • Claim–Evidence–Reasoning Frame</div>
            
            <div class="ws-callout" style="background: #f1f5f9; border-left: 4px solid #0f172a;">
                <b>Focus Question:</b> Why was the Boston Massacre a critical catalyst for the American Revolution?
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>CLAIM:</b> <span style="font-style: italic; color: #64748b; font-size: 0.82rem;">(State the section's central idea in 1 complete sentence)</span>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>EVIDENCE:</b> <span style="font-style: italic; color: #64748b; font-size: 0.82rem;">(Cite 1 specific detail, quote, or event from page 184)</span>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>REASONING:</b> <span style="font-style: italic; color: #64748b; font-size: 0.82rem;">(Explain how this evidence proves why colonial attitudes shifted)</span>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    # ── ANTI-COPYCAT MODES ──
    elif strategy_code == "pmi_01_prove_it":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-amber">Anti-Copycat Mode A • Prove the Textbook's Main Idea</div>

            <div class="ws-callout" style="background: #f8fafc; border-left: 4px solid #1e3a8a;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #1e3a8a; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.2rem;">
                    Textbook Printed Main Idea (p. 178)
                </div>
                <div style="font-style: italic; color: #1e293b; font-size: 0.92rem;">
                    "The British government made new laws that tightened control over the American colonies."
                </div>
            </div>

            <div style="color: #b45309; font-weight: 600; font-size: 0.85rem; margin: 0.65rem 0;">
                <b>Note: DO NOT copy the statement above!</b> Prove that it is true by finding 2 specific historical facts from the reading:
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>• Proof 1 (from Subheading 1: PROBLEMS ARISE, p. 178):</b>
                <div class="ws-dotted-line"></div>
                <div class="ws-dotted-line"></div>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>• Proof 2 (from Subheading 2: SOLDIERS IN THE COLONIES, p. 178):</b>
                <div class="ws-dotted-line"></div>
                <div class="ws-dotted-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "pmi_02_subheading_focus":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-amber">Anti-Copycat Mode B • Subheading Central Ideas</div>

            <div style="font-style: italic; color: #475569; font-size: 0.85rem; margin-bottom: 0.75rem;">
                <i>Notice: The textbook only gave 1 general sentence for the whole spread. Your job is to determine the unprinted Central Idea of each individual subsection:</i>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <b>Subheading 1 Central Idea (PROBLEMS ARISE, p. 178):</b>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <b>Subheading 2 Central Idea (A PROCLAMATION LINE, p. 179):</b>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>

            <div style="margin-top: 0.75rem;">
                <b>Historical Connection:</b> <span style="font-style: italic; color: #64748b;">How did the events in Subheading 1 directly cause the conflict in Subheading 2?</span>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "pmi_03_upgrade_it":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-amber">Anti-Copycat Mode C • Upgrade the Textbook's Main Idea</div>

            <div class="ws-callout" style="background: #fef2f2; border-left: 4px solid #ef4444;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #991b1b; text-transform: uppercase; margin-bottom: 0.2rem;">
                    Textbook's Basic Main Idea (5th Grade Level)
                </div>
                <div style="font-style: italic; color: #7f1d1d; font-size: 0.92rem;">
                    "Colonists protested British taxes."
                </div>
            </div>

            <div style="font-weight: 700; color: #0f172a; font-size: 0.88rem; margin: 0.65rem 0;">
                UPGRADE CHALLENGE: Rewrite this basic sentence into a mature 8th-grade historical claim.
            </div>
            <div style="font-size: 0.82rem; color: #475569; margin-bottom: 0.5rem;">
                You must include: (1) The specific tax or law, (2) Who resisted, and (3) The specific method of resistance:
            </div>

            <div class="ws-solid-line"></div>
            <div class="ws-solid-line"></div>
        </div>
        """

    # ── ACTIVE READING ORGANIZERS ──
    elif strategy_code == "read_01_cause_effect":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Text Structure: Historical Cause & Effect</div>
            
            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 50%;">HISTORICAL CAUSE<br><span style="font-weight:400; font-size:0.78rem;">What happened first?</span></th>
                        <th style="width: 50%;">HISTORICAL EFFECT<br><span style="font-weight:400; font-size:0.78rem;">What happened as a result?</span></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Cause 1:</b> Britain stationed 10,000 soldiers in the colonies and passed the Quartering Act (p. 178).</td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                    </tr>
                    <tr>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                        <td><b>Effect 2:</b> Pontiac led Native American attacks on British frontier forts (p. 179).</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    elif strategy_code == "read_04_sequence_timeline":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Text Structure: Chronological Sequence Tracker</div>
            
            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 15%; text-align: center;">ORDER</th>
                        <th style="width: 35%;">HISTORICAL EVENT & PAGE</th>
                        <th style="width: 50%;">WHAT OCCURRED? (Brief Summary)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="text-align: center; font-weight: 700;">STEP 1</td>
                        <td><b>1763: Treaty of Paris & Debt (p. 178)</b></td>
                        <td>Britain defeats France and gains Canada and land east of Mississippi River.</td>
                    </tr>
                    <tr>
                        <td style="text-align: center; font-weight: 700;">STEP 2</td>
                        <td><b>Spring 1763: Pontiac's War (p. 179)</b></td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                    </tr>
                    <tr>
                        <td style="text-align: center; font-weight: 700;">STEP 3</td>
                        <td><b>Fall 1763: Proclamation of 1763 (p. 179)</b></td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    elif strategy_code == "read_05_compare_perspectives":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Text Structure: Competing Perspectives Matrix</div>
            
            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 25%;">ISSUE / POLICY</th>
                        <th style="width: 37%;">BRITISH GOVERNMENT PERSPECTIVE</th>
                        <th style="width: 38%;">AMERICAN COLONISTS PERSPECTIVE</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Stationing Troops in America (p. 178)</b></td>
                        <td>Believed troops were needed to protect frontiers and colonies should contribute to defense.</td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                    </tr>
                    <tr>
                        <td><b>Proclamation of 1763 (p. 179)</b></td>
                        <td><div class="ws-dotted-line"></div><div class="ws-dotted-line"></div></td>
                        <td>Believed Britain had no right to trap them east of the mountains after they fought for the land.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    elif strategy_code == "read_02_say_something":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">'Say Something!' Subheading Check-Ins</div>
            
            <div style="margin-bottom: 0.85rem;">
                <b>1. PROBLEMS ARISE (p. 178)</b>
                <div style="font-style: italic; color: #64748b; font-size: 0.84rem;">
                    Stop & Jot: What was the most serious problem Great Britain faced after winning the French and Indian War?
                </div>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>

            <div style="margin-bottom: 0.85rem;">
                <b>2. SOLDIERS IN THE COLONIES (p. 178)</b>
                <div style="font-style: italic; color: #64748b; font-size: 0.84rem;">
                    Stop & Jot: Why did American colonists view the presence of British peacetime soldiers with suspicion?
                </div>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "read_03_cloze_guided":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">Guided Cloze Notes by Subheading</div>

            <div class="ws-callout" style="background: #f1f5f9; padding: 0.5rem 0.75rem; margin-bottom: 0.75rem;">
                <b>Word Bank:</b> <i>Proclamation of 1763, debt, Quartering Act, Appalachian, 10,000</i>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <b>1. PROBLEMS ARISE & SOLDIERS (p. 178):</b><br>
                Following the French and Indian War, Great Britain had huge war <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 100px;">&nbsp;</span>. 
                To maintain control, Parliament kept <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 80px;">&nbsp;</span> troops stationed in the colonies and passed the <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 140px;">&nbsp;</span>, requiring colonists to house them.
            </div>

            <div style="margin-bottom: 0.75rem;">
                <b>2. A PROCLAMATION LINE (p. 179):</b><br>
                To prevent further conflicts with Native Americans, King George issued the <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 160px;">&nbsp;</span>, forbidding settlers from moving west of the <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 110px;">&nbsp;</span> Mountains.
            </div>
        </div>
        """

    elif strategy_code == "twr_because_but_so":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">The Writing Revolution • Sentence Expansion: Because, But, So</div>
            <div style="font-weight: 600; color: #1e3a8a; margin-bottom: 0.5rem;">
                <b>Core Historical Stem:</b> Great Britain passed new taxes on American colonists...
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>• ...because:</b>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>• ...but:</b>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>• ...so:</b>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "twr_subordinating":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">The Writing Revolution • Subordinating Conjunctions</div>
            <div style="font-style: italic; color: #475569; font-size: 0.85rem; margin-bottom: 0.6rem;">
                Complete each historical sentence starter using evidence from the reading:
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>1. Although</b> Britain repealed the Stamp Act,
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>2. Before</b> colonial merchants initiated boycotts,
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>3. Even though</b> the Boston Massacre began as a riot,
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "twr_appositives":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">The Writing Revolution • Historical Appositive Frames</div>
            <div style="font-style: italic; color: #475569; font-size: 0.85rem; margin-bottom: 0.6rem;">
                Insert an appositive phrase between the commas to rename and define the historical figure or group:
            </div>
            <div style="margin-bottom: 0.75rem;">
                <b>1. King George III,</b> <span style="font-style: italic; color: #94a3b8;">[insert appositive phrase]</span>,
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <b>2. The Sons of Liberty,</b> <span style="font-style: italic; color: #94a3b8;">[insert appositive phrase]</span>,
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "twr_kernel_expansion":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">The Writing Revolution • Kernel Sentence Expansion</div>
            <div class="ws-callout" style="background: #f8fafc; border-left: 4px solid #1e3a8a;">
                <b>Kernel Sentence:</b> Colonists protested.
            </div>
            <div style="margin-bottom: 0.45rem;">
                <b>• When?</b>
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.45rem;">
                <b>• Where?</b>
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.45rem;">
                <b>• Why?</b>
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-top: 0.75rem;">
                <b>Expanded 8th-Grade Historical Sentence:</b>
                <div class="ws-solid-line"></div>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    elif strategy_code == "twr_spo":
        return f"""
        {COMMON_CSS}
        <div class="ws-container">
            <div class="ws-title-badge ws-badge-blue">The Writing Revolution • Single-Paragraph Outline (SPO)</div>
            <div style="margin-bottom: 0.65rem;">
                <b>Topic Sentence (Central Idea):</b>
                <div class="ws-solid-line"></div>
            </div>
            <div style="margin-bottom: 0.45rem; padding-left: 1rem;">
                <b>1. Detail 1:</b>
                <div class="ws-dotted-line"></div>
            </div>
            <div style="margin-bottom: 0.45rem; padding-left: 1rem;">
                <b>2. Detail 2:</b>
                <div class="ws-dotted-line"></div>
            </div>
            <div style="margin-bottom: 0.45rem; padding-left: 1rem;">
                <b>3. Detail 3:</b>
                <div class="ws-dotted-line"></div>
            </div>
            <div style="margin-top: 0.65rem;">
                <b>Concluding Sentence (Clincher):</b>
                <div class="ws-solid-line"></div>
            </div>
        </div>
        """

    return f"""
    {COMMON_CSS}
    <div class="ws-container">
        <div class="ws-title-badge ws-badge-blue">Worksheet Layout</div>
        <div>Preview for template: <code>{strategy_code}</code></div>
    </div>
    """


@_dedent_html
def render_preview_exemplar(
    strategy_code: str,
    section_meta: Optional[Dict[str, Any]] = None,
    raw_passage_md: str = "",
) -> str:
    """Renders a realistic, clean completed 8th-grade student exemplar response."""
    if section_meta is not None:
        from src.packet_builder import build_standalone_strategy_handout
        cat_name = _detect_strategy_category(strategy_code)
        handout = build_standalone_strategy_handout(
            section_meta=section_meta,
            strategy_category=cat_name,
            strategy_code=strategy_code,
            markdown_text=raw_passage_md,
        )
        return format_booklet_for_web(handout["exemplar_md"])

    # ── Generic Model Exemplar Fallback (Chapter 5) ──
    if strategy_code == "ci_01_subheading_gist":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Chapter 5 (Road to Revolution)</div>
            
            <div style="font-weight: 700; color: #064e3b; margin-bottom: 0.4rem;">Part 1: Subheading Gist Checkpoints (Student Exemplar)</div>

            <div style="margin-bottom: 0.65rem;">
                <b>1. PROBLEMS ARISE (p. 178):</b><br>
                <span class="ws-student-answer">Britain gained vast North American territory but faced massive wartime debts after 1763.</span>
                <span style="font-size: 0.78rem; color: #16a34a; font-weight: 600;">(12 words)</span>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>2. SOLDIERS IN THE COLONIES (p. 178):</b><br>
                <span class="ws-student-answer">Parliament passed Quartering Act forcing colonists to house British troops in towns.</span>
                <span style="font-size: 0.78rem; color: #16a34a; font-weight: 600;">(11 words)</span>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>3. A PROCLAMATION LINE (p. 179):</b><br>
                <span class="ws-student-answer">King George banned western migration past Appalachians, angering land-hungry settlers.</span>
                <span style="font-size: 0.78rem; color: #16a34a; font-weight: 600;">(10 words)</span>
            </div>

            <div style="margin-top: 0.85rem; padding-top: 0.65rem; border-top: 1px dashed #86efac;">
                <div style="font-weight: 700; color: #064e3b; margin-bottom: 0.25rem;">Part 2: Whole-Section Central Idea (Student Exemplar)</div>
                <div class="ws-student-answer" style="display: block; padding: 0.5rem 0.65rem; font-size: 0.90rem; line-height: 1.45;">
                    After 1763, Great Britain tried to manage its expanded empire by restricting colonial westward settlement and quartering soldiers, which sparked widespread colonial anger over losing their traditional freedoms.
                </div>
            </div>
        </div>
        """

    elif strategy_code == "ci_02_box_and_bullets":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Chapter 5</div>

            <div class="ws-callout" style="background: #ecfdf5; border: 1.5px solid #a7f3d0; border-left: 5px solid #10b981;">
                <div style="font-weight: 700; color: #065f46; font-size: 0.88rem; margin-bottom: 0.25rem;">
                    CENTRAL IDEA BOX (Student Exemplar)
                </div>
                <div class="ws-student-answer" style="display: block; padding: 0.45rem 0.65rem; font-size: 0.90rem;">
                    The Stamp Act provoked fierce resistance across the colonies because colonists believed only their own elected colonial assemblies had the legal right to tax them.
                </div>
            </div>

            <div style="margin-top: 0.75rem;">
                <div style="font-weight: 700; color: #064e3b; margin-bottom: 0.4rem;">Supporting Bullets (Student Exemplar):</div>
                <div style="margin-bottom: 0.45rem;">
                    <b>• Supporting Detail 1 (p. 180):</b> <span class="ws-student-answer">Patrick Henry declared in the Virginia House of Burgesses that taxing colonists without consent was an act of tyranny.</span>
                </div>
                <div style="margin-bottom: 0.45rem;">
                    <b>• Supporting Detail 2 (p. 180):</b> <span class="ws-student-answer">Colonial merchants signed nonimportation agreements, boycotting British manufactured imports until Parliament repealed the tax.</span>
                </div>
                <div style="margin-bottom: 0.45rem;">
                    <b>• Supporting Detail 3 (p. 181):</b> <span class="ws-student-answer">The Sons of Liberty organized protests, burned effigies of royal stamp distributors in the streets, and forced officials to resign.</span>
                </div>
            </div>
        </div>
        """

    elif strategy_code == "ci_03_what_so_what":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • What + So What?</div>

            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 28%;">Subheading & Page</th>
                        <th style="width: 36%;">WHAT HAPPENED? (Student Fact)</th>
                        <th style="width: 36%;">SO WHAT? (Historical Significance)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>1. The Townshend Acts (p. 182)</b></td>
                        <td><span class="ws-student-answer">Parliament placed duties on imported tea, glass, lead, paper, and paint.</span></td>
                        <td><span class="ws-student-answer">It showed Parliament still insisted on taxing colonists without consent, even after repealing the Stamp Act.</span></td>
                    </tr>
                    <tr>
                        <td><b>2. Protests & Boycotts (p. 183)</b></td>
                        <td><span class="ws-student-answer">Women formed the Daughters of Liberty and urged colonists to weave homespun fabric.</span></td>
                        <td><span class="ws-student-answer">It mobilized entire colonial communities and proved economic boycotts could hurt British merchants.</span></td>
                    </tr>
                </tbody>
            </table>

            <div style="margin-top: 0.75rem;">
                <b>Central Idea Synthesis (Student Exemplar):</b>
                <div class="ws-student-answer" style="display: block; padding: 0.5rem 0.65rem; margin-top: 0.35rem; font-size: 0.90rem;">
                    The Townshend Acts reignited colonial outrage and united everyday colonists, including women, to resist British taxation through economic boycotts and domestic manufacturing.
                </div>
            </div>
        </div>
        """

    elif strategy_code == "ci_04_cer_paragraph":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Claim–Evidence–Reasoning</div>

            <div style="margin-bottom: 0.65rem;">
                <b>CLAIM:</b><br>
                <span class="ws-student-answer">The Boston Massacre served as powerful anti-British propaganda that united colonial outrage against military occupation.</span>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>EVIDENCE:</b><br>
                <span class="ws-student-answer">According to page 184, Paul Revere created an engraving titled "The Bloody Massacre" showing armed soldiers firing into an orderly crowd of unarmed citizens.</span>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>REASONING:</b><br>
                <span class="ws-student-answer">Even though the clash began as a chaotic riot, the widely distributed image convinced colonists throughout North America that British troops were dangerous oppressors who would kill their own subjects.</span>
            </div>
        </div>
        """

    elif strategy_code == "pmi_02_subheading_focus":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Subheading Central Ideas</div>

            <div style="margin-bottom: 0.65rem;">
                <b>Subheading 1 Central Idea (PROBLEMS ARISE, p. 178):</b><br>
                <span class="ws-student-answer">Winning the French and Indian War gave Britain vast new western territory but left the empire with staggering debt that British leaders expected colonies to finance.</span>
            </div>

            <div style="margin-bottom: 0.65rem;">
                <b>Subheading 2 Central Idea (A PROCLAMATION LINE, p. 179):</b><br>
                <span class="ws-student-answer">To avoid expensive conflicts with Native American nations, Britain banned colonial settlement west of the Appalachians, enraging land speculators and colonists who fought for that land.</span>
            </div>

            <div style="margin-top: 0.75rem;">
                <b>Historical Connection (Student Exemplar):</b><br>
                <span class="ws-student-answer">Because Britain was deep in debt from the war, it could not afford new frontier wars, leading directly to the unpopular Proclamation Line.</span>
            </div>
        </div>
        """

    elif strategy_code == "read_01_cause_effect":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Cause & Effect Table</div>

            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 50%;">HISTORICAL CAUSE</th>
                        <th style="width: 50%;">HISTORICAL EFFECT</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Cause 1:</b> Britain stationed 10,000 soldiers in the colonies and passed the Quartering Act (p. 178).</td>
                        <td><span class="ws-student-answer">Colonists, especially in New York, felt their rights were violated and assemblies refused to pay for soldiers' supplies.</span></td>
                    </tr>
                    <tr>
                        <td><span class="ws-student-answer">British settlers moved onto Native American lands west of the Appalachian Mountains without compensation (p. 179).</span></td>
                        <td><b>Effect 2:</b> Pontiac led Native American attacks on British frontier forts (p. 179).</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    elif strategy_code == "read_02_say_something":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • 'Say Something!' Stop & Jot</div>

            <div style="margin-bottom: 0.75rem;">
                <b>1. PROBLEMS ARISE (p. 178) — Stop & Jot Response:</b><br>
                <span class="ws-student-answer">The most serious problem was that Britain was left with massive war debt of over 130 million pounds, while gaining a vast frontier that was expensive to defend.</span>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <b>2. SOLDIERS IN THE COLONIES (p. 178) — Stop & Jot Response:</b><br>
                <span class="ws-student-answer">Colonists feared the soldiers were stationed in colonial cities not to protect them from enemies, but to enforce royal laws and strip away colonial self-government.</span>
            </div>
        </div>
        """

    elif strategy_code == "read_03_cloze_guided":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Guided Cloze Notes</div>

            <div style="margin-bottom: 0.75rem;">
                <b>1. PROBLEMS ARISE & SOLDIERS (p. 178):</b><br>
                Following the French and Indian War, Great Britain had huge war <span class="ws-student-answer">debt</span>. 
                To maintain control, Parliament kept <span class="ws-student-answer">10,000</span> troops stationed in the colonies and passed the <span class="ws-student-answer">Quartering Act</span>, requiring colonists to house them.
            </div>

            <div style="margin-bottom: 0.75rem;">
                <b>2. A PROCLAMATION LINE (p. 179):</b><br>
                To prevent further conflicts with Native Americans, King George issued the <span class="ws-student-answer">Proclamation of 1763</span>, forbidding settlers from moving west of the <span class="ws-student-answer">Appalachian</span> Mountains.
            </div>
        </div>
        """

    elif strategy_code == "read_05_compare_perspectives":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Competing Perspectives</div>

            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 25%;">ISSUE / POLICY</th>
                        <th style="width: 37%;">BRITISH GOVERNMENT PERSPECTIVE</th>
                        <th style="width: 38%;">AMERICAN COLONISTS PERSPECTIVE</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Stationing Troops in America</b></td>
                        <td>Believed troops were needed to protect frontiers and colonies should pay for defense.</td>
                        <td><span class="ws-student-answer">Feared peacetime troops were stationed in cities to intimidate citizens and suppress colonial liberties.</span></td>
                    </tr>
                    <tr>
                        <td><b>Proclamation of 1763</b></td>
                        <td><span class="ws-student-answer">Wanted to prevent costly wars with Native American tribes and stabilize the imperial frontier.</span></td>
                        <td>Believed Britain had no right to trap them east of the mountains after they fought for the land.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    elif strategy_code == "pmi_03_upgrade_it":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Upgraded Claim</div>

            <div style="font-weight: 700; color: #064e3b; margin-bottom: 0.4rem;">Upgraded 8th-Grade Historical Claim:</div>
            <div class="ws-student-answer" style="display: block; padding: 0.6rem 0.85rem; font-size: 0.92rem; line-height: 1.5;">
                "When Parliament imposed the Stamp Act to tax colonial documents without consent, organized groups like the Sons of Liberty and colonial merchants launched widespread boycotts and protests that forced Britain to repeal the act."
            </div>
        </div>
        """

    elif strategy_code == "read_04_sequence_timeline":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Sequence Tracker</div>
            
            <table class="ws-table">
                <thead>
                    <tr>
                        <th style="width: 15%; text-align: center;">ORDER</th>
                        <th style="width: 35%;">HISTORICAL EVENT & PAGE</th>
                        <th style="width: 50%;">WHAT OCCURRED? (Student Exemplar)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="text-align: center; font-weight: 700;">STEP 1</td>
                        <td><b>1763: Treaty of Paris & Debt (p. 178)</b></td>
                        <td>Britain defeats France and gains Canada and land east of Mississippi River.</td>
                    </tr>
                    <tr>
                        <td style="text-align: center; font-weight: 700;">STEP 2</td>
                        <td><b>Spring 1763: Pontiac's War (p. 179)</b></td>
                        <td><span class="ws-student-answer">Ottawa chief Pontiac unites tribes to attack British forts to defend lands.</span></td>
                    </tr>
                    <tr>
                        <td style="text-align: center; font-weight: 700;">STEP 3</td>
                        <td><b>Fall 1763: Proclamation of 1763 (p. 179)</b></td>
                        <td><span class="ws-student-answer">King George forbids colonial settlement west of the Appalachians to calm frontier.</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    elif strategy_code == "twr_because_but_so":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Because, But, So</div>
            <div style="font-weight: 600; color: #065f46; margin-bottom: 0.5rem;">
                Core Stem: Great Britain passed new taxes on American colonists...
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>• ...because</b> <span class="ws-student-answer">Britain was deep in debt from fighting the French and Indian War and wanted the colonies to help pay for defense.</span>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>• ...but</b> <span class="ws-student-answer">colonists had no elected representatives in Parliament to vote on those taxes.</span>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>• ...so</b> <span class="ws-student-answer">colonial leaders organized boycotts of British goods and formed the Stamp Act Congress.</span>
            </div>
        </div>
        """

    elif strategy_code == "twr_subordinating":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Subordinating Conjunctions</div>
            <div style="margin-bottom: 0.65rem;">
                <b>1. Although</b> Britain eventually repealed the Stamp Act, <span class="ws-student-answer">Parliament immediately passed the Declaratory Act claiming absolute authority over the colonies.</span>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>2. Before</b> colonists initiated widespread boycotts, <span class="ws-student-answer">British authorities did not believe colonial protests would threaten British profits.</span>
            </div>
            <div style="margin-bottom: 0.65rem;">
                <b>3. Even though</b> the Boston Massacre involved a small mob, <span class="ws-student-answer">colonial leaders used Paul Revere's engraving as propaganda to unite colonial resistance.</span>
            </div>
        </div>
        """

    elif strategy_code == "twr_appositives":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Appositives</div>
            <div style="margin-bottom: 0.75rem;">
                <b>1. King George III,</b> <span class="ws-student-answer">the head of the British Empire</span>, refused to compromise with colonial petitions and ordered military enforcement of tax laws.
            </div>
            <div style="margin-bottom: 0.75rem;">
                <b>2. The Sons of Liberty,</b> <span class="ws-student-answer">an organized network of colonial activists led by Samuel Adams</span>, held public rallies and intimidated royal tax collectors.
            </div>
        </div>
        """

    elif strategy_code == "twr_kernel_expansion":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Kernel Expansion</div>
            <div style="font-weight: 600; color: #065f46; margin-bottom: 0.4rem;">Kernel: Colonists protested.</div>
            <div style="margin-bottom: 0.35rem;">• <i>When?</i> <span class="ws-student-answer">In 1765 after the Stamp Act was announced</span></div>
            <div style="margin-bottom: 0.35rem;">• <i>Where?</i> <span class="ws-student-answer">In port cities like Boston and New York</span></div>
            <div style="margin-bottom: 0.45rem;">• <i>Why?</i> <span class="ws-student-answer">To demand that only their elected assemblies could tax them</span></div>
            <div style="margin-top: 0.65rem; font-weight: 700; color: #064e3b;">Expanded Historical Sentence:</div>
            <div class="ws-student-answer" style="display: block; padding: 0.5rem 0.65rem; margin-top: 0.25rem;">
                In 1765, colonists in port cities like Boston and New York actively protested against the Stamp Act to demand that only their elected assemblies could impose taxes.
            </div>
        </div>
        """

    elif strategy_code == "twr_spo":
        return f"""
        {COMMON_CSS}
        <div class="ws-exemplar-container">
            <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar • Single-Paragraph Outline</div>
            <div style="margin-bottom: 0.5rem;">
                <b>• Topic Sentence:</b> <span class="ws-student-answer">British economic policies after 1763 pushed American colonists toward open rebellion.</span>
            </div>
            <div style="margin-bottom: 0.35rem; padding-left: 1rem;">
                1. <b>Detail 1:</b> <span class="ws-student-answer">Stamp Act taxed everyday legal documents without consent.</span>
            </div>
            <div style="margin-bottom: 0.35rem; padding-left: 1rem;">
                2. <b>Detail 2:</b> <span class="ws-student-answer">Quartering Act forced colonial assemblies to house peacetime British troops.</span>
            </div>
            <div style="margin-bottom: 0.35rem; padding-left: 1rem;">
                3. <b>Detail 3:</b> <span class="ws-student-answer">Boston Massacre highlighted growing violence between citizens and redcoats.</span>
            </div>
            <div style="margin-top: 0.5rem;">
                <b>• Concluding Sentence:</b> <span class="ws-student-answer">As Parliament continued to ignore colonial petitions, colonists concluded that peaceful compromise within the empire was no longer possible.</span>
            </div>
        </div>
        """

    return f"""
    {COMMON_CSS}
    <div class="ws-exemplar-container">
        <div class="ws-title-badge ws-badge-green">8th-Grade Student Exemplar</div>
        <div>Completed exemplar response available for this template.</div>
    </div>
    """


@_dedent_html
def render_preview_cover(cover_code: str) -> str:
    """Renders a clean mockup of the student booklet cover page layout."""
    if cover_code == "central_idea_tracker":
        return f"""
        {COMMON_CSS}
        <div class="ws-container" style="border: 2px solid #0f172a; max-width: 620px; margin: 0 auto;">
            <div style="text-align: center; border-bottom: 2px solid #0f172a; padding-bottom: 0.75rem; margin-bottom: 0.75rem;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase;">8th Grade U.S. History • Student Chapter Booklet</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #0f172a; margin-top: 0.2rem;">CHAPTER 5: THE ROAD TO REVOLUTION</div>
                <div style="font-size: 0.85rem; color: #475569; margin-top: 0.3rem;"><b>Essential Question:</b> Why did British policies after 1763 lead colonies to declare independence?</div>
            </div>

            <div style="display: flex; gap: 1rem; margin-bottom: 1rem; font-size: 0.88rem;">
                <div style="flex: 2;"><b>Student Name:</b> <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 75%;">&nbsp;</span></div>
                <div style="flex: 1;"><b>Period:</b> <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 60%;">&nbsp;</span></div>
            </div>

            <div style="font-weight: 700; font-size: 0.85rem; color: #1e3a8a; margin-bottom: 0.4rem;">MASTER CENTRAL IDEA TRACKER & PROGRESS TABLE</div>
            <table class="ws-table" style="font-size: 0.82rem;">
                <thead>
                    <tr>
                        <th style="width: 20%;">Section</th>
                        <th style="width: 55%;">Student Central Idea Mastery Statement</th>
                        <th style="width: 25%; text-align: center;">Verified / Score</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><b>Sec 5.1</b> (p. 178)</td><td><div class="ws-dotted-line"></div></td><td style="text-align: center;">[ &nbsp; ] ___ / 10</td></tr>
                    <tr><td><b>Sec 5.2</b> (p. 180)</td><td><div class="ws-dotted-line"></div></td><td style="text-align: center;">[ &nbsp; ] ___ / 10</td></tr>
                    <tr><td><b>Sec 5.3</b> (p. 182)</td><td><div class="ws-dotted-line"></div></td><td style="text-align: center;">[ &nbsp; ] ___ / 10</td></tr>
                    <tr><td><b>Sec 5.4</b> (p. 184)</td><td><div class="ws-dotted-line"></div></td><td style="text-align: center;">[ &nbsp; ] ___ / 10</td></tr>
                </tbody>
            </table>
        </div>
        """
    elif cover_code == "score_checklist":
        return f"""
        {COMMON_CSS}
        <div class="ws-container" style="border: 2px solid #0f172a; max-width: 620px; margin: 0 auto;">
            <div style="text-align: center; border-bottom: 2px solid #0f172a; padding-bottom: 0.75rem; margin-bottom: 0.75rem;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase;">8th Grade Social Studies • Chapter Packet</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #0f172a; margin-top: 0.2rem;">CHAPTER 5 BOOKLET & SCORE CHECKLIST</div>
            </div>

            <div style="display: flex; gap: 1rem; margin-bottom: 1rem; font-size: 0.88rem;">
                <div style="flex: 2;"><b>Student:</b> <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 75%;">&nbsp;</span></div>
                <div style="flex: 1;"><b>Period:</b> <span style="display:inline-block; border-bottom: 1.5px solid #0f172a; width: 60%;">&nbsp;</span></div>
            </div>

            <table class="ws-table" style="font-size: 0.82rem;">
                <thead>
                    <tr>
                        <th style="width: 30%;">Packet Section</th>
                        <th style="width: 35%;">Required Tasks</th>
                        <th style="width: 15%; text-align: center;">Done</th>
                        <th style="width: 20%; text-align: center;">Score</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><b>Section 5.1</b></td><td>Vocab + Reading + Central Idea</td><td style="text-align: center;">[ &nbsp; ]</td><td style="text-align: center;">___ / 10</td></tr>
                    <tr><td><b>Section 5.2</b></td><td>Vocab + Reading + Central Idea</td><td style="text-align: center;">[ &nbsp; ]</td><td style="text-align: center;">___ / 10</td></tr>
                    <tr><td><b>Section 5.3</b></td><td>Vocab + Reading + Central Idea</td><td style="text-align: center;">[ &nbsp; ]</td><td style="text-align: center;">___ / 10</td></tr>
                    <tr><td><b>Chapter Review</b></td><td>Vocabulary Match + DBQ Syntheses</td><td style="text-align: center;">[ &nbsp; ]</td><td style="text-align: center;">___ / 25</td></tr>
                </tbody>
            </table>
        </div>
        """
    else:
        return f"""
        {COMMON_CSS}
        <div class="ws-container" style="text-align: center; padding: 1.5rem; color: #64748b;">
            <b>No Front Cover Page Selected</b><br>
            <span style="font-size: 0.82rem;">The booklet begins directly on Section Page 1 without an extra front cover.</span>
        </div>
        """


@_dedent_html
def render_preview_footer(footer_code: str) -> str:
    """Renders a clean mockup of the page footer check box layout."""
    if footer_code == "stamp_box":
        return f"""
        {COMMON_CSS}
        <div class="ws-container" style="border: 1.5px solid #cbd5e1; max-width: 520px; margin: 0 auto; padding: 0.75rem 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Teacher Checkpoint</div>
                    <div style="font-size: 0.95rem; font-weight: 800; color: #0f172a;">Section Completion Verification</div>
                </div>
                <div style="border: 2px dashed #94a3b8; border-radius: 6px; width: 140px; height: 55px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; color: #64748b; text-align: center;">
                    [ TEACHER STAMP / INITIALS ]
                </div>
            </div>
        </div>
        """
    elif footer_code == "points_10":
        return f"""
        {COMMON_CSS}
        <div class="ws-container" style="border: 1.5px solid #cbd5e1; max-width: 540px; margin: 0 auto; padding: 0.75rem 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 0.85rem; color: #334155;">
                    <b>Scoring:</b> Vocab: ___/3 &nbsp;|&nbsp; Reading: ___/3 &nbsp;|&nbsp; Central Idea: ___/4
                </div>
                <div style="background: #f1f5f9; border: 1.5px solid #94a3b8; border-radius: 6px; padding: 0.35rem 0.75rem; font-weight: 800; font-size: 1rem; color: #0f172a;">
                    Total: ______ / 10 pts
                </div>
            </div>
        </div>
        """
    elif footer_code == "points_100":
        return f"""
        {COMMON_CSS}
        <div class="ws-container" style="border: 1.5px solid #cbd5e1; max-width: 540px; margin: 0 auto; padding: 0.75rem 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 0.85rem; color: #334155;">
                    <b>Percent Grading Scale (Weighted Accuracy & Effort)</b>
                </div>
                <div style="background: #f1f5f9; border: 1.5px solid #94a3b8; border-radius: 6px; padding: 0.35rem 0.75rem; font-weight: 800; font-size: 1rem; color: #0f172a;">
                    Grade: ______ / 100%
                </div>
            </div>
        </div>
        """
    else:
        return f"""
        {COMMON_CSS}
        <div class="ws-container" style="text-align: center; padding: 0.75rem; color: #64748b; font-size: 0.82rem;">
            <b>No Footer Grading Box</b> (Section page ends cleanly after the Central Idea synthesis lines).
        </div>
        """


@_dedent_html
def render_preview_scaffold(scaffold_text: str) -> str:
    """Renders the blue callout box for scaffolded support elements."""
    if not scaffold_text:
        return ""
    
    # Clean text lines into bullet items
    raw_lines = scaffold_text.strip().splitlines()
    cleaned_items = []
    for l in raw_lines:
        l = l.strip()
        if not l or l.startswith("*Scaffolded Support"):
            continue
        cleaned_items.append(f"<li>{l.lstrip('-* ')}</li>")
    
    items_html = "".join(cleaned_items) if cleaned_items else f"<div>{scaffold_text}</div>"

    return f"""
    {COMMON_CSS}
    <div class="ws-scaffold-container">
        <div style="font-weight: 700; color: #1e40af; font-size: 0.88rem; margin-bottom: 0.45rem;">
            Possible Scaffolded Support Elements (Differentiated Edition)
        </div>
        <ul style="margin: 0; padding-left: 1.25rem; font-size: 0.85rem; color: #1e3a8a;">
            {items_html}
        </ul>
    </div>
    """


def _convert_md_table_to_html(md: str) -> str:
    """Converts standard markdown tables into styled .ws-table HTML."""
    table_pattern = re.compile(r'((?:^\|[^\n]+\|\r?\n)+)', re.MULTILINE)

    def _rep_table(match):
        raw_table = match.group(1).strip()
        lines = [line.strip() for line in raw_table.splitlines() if line.strip()]
        if len(lines) < 2:
            return raw_table

        header_line = lines[0]
        sep_line = lines[1]
        if not re.match(r'^\|[\s\:\-\|]+\|$', sep_line):
            return raw_table

        headers = [h.strip() for h in header_line.strip('|').split('|')]
        th_html = ''.join(f'<th>{h}</th>' for h in headers)

        rows_html = []
        for row_line in lines[2:]:
            cells = [c.strip() for c in row_line.strip('|').split('|')]
            td_html = ''.join(f'<td>{c}</td>' for c in cells)
            rows_html.append(f'<tr>{td_html}</tr>')

        tbody_content = ''.join(rows_html)
        return f'<table class="ws-table"><thead><tr>{th_html}</tr></thead><tbody>{tbody_content}</tbody></table>'

    return table_pattern.sub(_rep_table, md)


def format_booklet_for_web(booklet_md: str) -> str:
    """
    Transforms compiled booklet and standalone strategy markdown into spectacular,
    museum-quality HTML layouts matching the visual excellence of the model templates.
    """
    if not booklet_md:
        return ""

    pages = booklet_md.split("[PAGE_BREAK]")
    formatted_pages = []

    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F9FF"
        "\U00002600-\U000027BF"
        "\U0001FA00-\U0001FAFF"
        "\U00002702-\U000027B0"
        "]+",
        flags=re.UNICODE,
    )

    for page_idx, raw_page in enumerate(pages):
        page = emoji_pattern.sub("", raw_page)
        if not page.strip():
            continue

        # 1. Convert handwriting lines: ASCII dots and underscores
        page = re.sub(r"\.{10,}", '<div class="ws-dotted-line"></div>', page)
        page = re.sub(r"_{8,}", '<div class="ws-solid-line"></div>', page)

        # 2. Convert markdown tables
        page = _convert_md_table_to_html(page)

        # 3. Handle [CENTER_HEADING: ...]
        page = re.sub(
            r'\[CENTER_HEADING:\s*([^\]]+)\]',
            r'<div style="text-align: center; font-size: 1.05rem; font-weight: 700; color: #1e3a8a; margin: 1.15rem 0 0.5rem 0; letter-spacing: 0.02em;">\1</div>',
            page,
        )

        # 4. Handle [GRADE_BOX: ...]
        def _replace_grade_box(match):
            box_text = match.group(1).strip()
            return (
                f'<div style="display: flex; justify-content: flex-end; margin: 1.15rem 0 0.35rem 0;">'
                f'<div style="font-size: 0.88rem; font-weight: 700; color: #1e3a8a; background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 4px; padding: 0.35rem 0.85rem; letter-spacing: 0.03em;">'
                f'{box_text}'
                f'</div></div>'
            )
        page = re.sub(r'\[GRADE_BOX:\s*([^\]]+)\]', _replace_grade_box, page)

        # 5. Check if page is an Exemplar page
        if re.search(r"^#\s+Student Exemplar & Answer Key:", page, flags=re.MULTILINE):
            def _rep_ex_header(m):
                sec_id = m.group(1).strip()
                strat = m.group(2).strip()
                return (
                    f'<div class="ws-title-badge ws-badge-green">Authentic 8th-Grade Student Exemplar • Sec. {sec_id}</div>\n'
                    f'<div style="font-size: 1.15rem; font-weight: 700; color: #064e3b; margin: 0.15rem 0 0.25rem 0;">{strat} — <span style="color: #10b981;">Score: 100/100</span></div>\n'
                )
            page = re.sub(
                r"^#\s+Student Exemplar & Answer Key:\s*Sec\.\s*([^\s—]+)\s*—\s*([^\n]+)",
                _rep_ex_header,
                page,
                flags=re.MULTILINE,
            )

            # Style Textbook Reference line
            page = re.sub(
                r"^\*\*Textbook Reference:\*\*\s*(.*?)(?=\n)",
                r'<div style="font-size: 0.82rem; color: #047857; margin-bottom: 0.75rem; border-bottom: 1px solid #bbf7d0; padding-bottom: 0.4rem;"><b>Textbook Reference:</b> \1</div>',
                page,
                flags=re.MULTILINE,
            )

            # Remove redundant headers
            page = re.sub(r"^###\s+Authentic 8th-Grade Student Model Response\n+", "", page, flags=re.MULTILINE)
            page = re.sub(r"^>\s*\*Student Response Sample for [^\*]+\*:\n+", "", page, flags=re.MULTILINE)

            # Transform bullet exemplar answers into styled green pills
            def _rep_ex_bullet(m):
                label = m.group(1).strip()
                ans = m.group(2).strip()
                return (
                    f'<div style="margin-bottom: 0.75rem;">\n'
                    f'<div style="font-weight: 700; color: #064e3b; font-size: 0.86rem; margin-bottom: 0.2rem;">{label}:</div>\n'
                    f'<div class="ws-student-answer" style="display: block; padding: 0.45rem 0.65rem; font-size: 0.88rem; line-height: 1.45;">{ans}</div>\n'
                    f'</div>'
                )
            page = re.sub(
                r"^\s*-\s+\*\*([^\:]+)\:\s*(.*?)\*\*",
                _rep_ex_bullet,
                page,
                flags=re.MULTILINE,
            )

            # Style Textbook Source Grounding callout
            def _rep_grounding(m):
                pg = m.group(1).strip()
                raw_txt = m.group(2).strip()
                clean_txt = re.sub(r'^[\s*"\']+|[\s*"\']+$', '', raw_txt)
                return (
                    f'<div class="ws-callout" style="background: #ffffff; border: 1.5px solid #a7f3d0; border-left: 5px solid #10b981; margin-top: 0.85rem; font-size: 0.83rem; color: #14532d;">\n'
                    f'<b>Textbook Source Grounding (p. {pg}):</b> "<i>{clean_txt}</i>"\n'
                    f'</div>'
                )
            page = re.sub(
                r"^\*Textbook Source Grounding \(p\.\s*(\d+)\):\*\s*(.*)",
                _rep_grounding,
                page,
                flags=re.MULTILINE,
            )

            wrapped_page = f'<div class="ws-exemplar-container">\n{page.strip()}\n</div>'
            formatted_pages.append(wrapped_page)

        # 6. Check if page is Cover Page
        elif re.search(r"^#\s+Chapter\s+\d+:", page, flags=re.MULTILINE):
            def _rep_cov_header(m):
                cnum = m.group(1).strip()
                ctitle = m.group(2).strip()
                edition = m.group(3).strip()
                return (
                    f'<div class="ws-title-badge ws-badge-blue">Chapter {cnum} • {edition}</div>\n'
                    f'<div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0.2rem 0 0.35rem 0;">Chapter {cnum}: {ctitle}</div>\n'
                )
            page = re.sub(
                r"^#\s+Chapter\s+(\d+):\s*([^\n—]+)\s*—\s*([^\n]+)",
                _rep_cov_header,
                page,
                flags=re.MULTILINE,
            )
            wrapped_page = f'<div class="ws-container" style="border: 2px solid #3b82f6; background: #ffffff;">\n{page.strip()}\n</div>'
            formatted_pages.append(wrapped_page)

        # 7. Standard Student Section Handout
        elif re.search(r"^##\s+Section\s+[\d\.]+", page, flags=re.MULTILINE):
            def _rep_handout_header(m):
                sec_id = m.group(1).strip()
                full_rest = m.group(2).strip()
                is_scaf = "scaffolded" in full_rest.lower()

                pg_match = re.search(r'\((?:Textbook\s+)?pp?\.\s*([^\)]+)\)', full_rest)
                pgs_str = f"(pp. {pg_match.group(1)})" if pg_match else ""

                clean_title = re.sub(r'\((?:Textbook\s+)?pp?\.[^\)]+\)', '', full_rest)
                clean_title = re.sub(r'\*?\([^\)]*scaffolded[^\)]*\)\*?', '', clean_title, flags=re.IGNORECASE).strip()

                scaf_badge = ' <span style="background: #fef3c7; color: #b45309; font-size: 0.72rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 4px; text-transform: uppercase; margin-left: 0.4rem;">Scaffolded Edition</span>' if is_scaf else ""

                return (
                    f'<div class="ws-title-badge ws-badge-blue">Section {sec_id} Handout • {clean_title}</div>{scaf_badge}\n'
                    f'<div style="font-size: 1.15rem; font-weight: 700; color: #0f172a; margin: 0.15rem 0 0.25rem 0;">Section {sec_id}: {clean_title} <span style="font-size: 0.85rem; font-weight: 500; color: #64748b;">{pgs_str}</span></div>\n'
                    f'<div style="display: flex; justify-content: space-between; font-size: 0.80rem; color: #64748b; margin-bottom: 0.75rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.35rem;">\n'
                    f'<span><b>Name:</b> ___________________________</span><span><b>Date:</b> _____________</span><span><b>Class:</b> ________</span>\n'
                    f'</div>\n'
                )
            page = re.sub(
                r"^##\s+Section\s+([\d\.]+):?\s+(.*)",
                _rep_handout_header,
                page,
                flags=re.MULTILINE,
            )

            # Style Strategy Focus badge
            page = re.sub(
                r"^>\s*\*\*Strategy Focus:\*\*\s*(.*?)(?=\n)",
                r'<div style="background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #3b82f6; border-radius: 6px; padding: 0.45rem 0.75rem; margin-bottom: 0.75rem; font-size: 0.85rem; color: #1e3a8a;">'
                r'<b>Strategy Focus:</b> \1'
                r'</div>',
                page,
                flags=re.MULTILINE,
            )

            # Style Textbook Printed Main Idea callout
            def _rep_pmi_callout(m):
                pg = m.group(1).strip()
                raw_txt = m.group(2).strip()
                clean_txt = re.sub(r'^[\s*"\']+|[\s*"\']+$', '', raw_txt)
                return (
                    f'<div class="ws-callout" style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-left: 4px solid #1e3a8a; margin: 0.75rem 0;">\n'
                    f'<div style="font-size: 0.75rem; font-weight: 700; color: #1e3a8a; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.2rem;">Textbook Printed Main Idea (p. {pg})</div>\n'
                    f'<div style="font-style: italic; color: #1e293b; font-size: 0.90rem;">"{clean_txt}"</div>\n'
                    f'</div>'
                )
            page = re.sub(
                r"^>\s*\*\*Textbook Printed Main Idea \(p\.\s*(\d+)\):\*\s*(.*)",
                _rep_pmi_callout,
                page,
                flags=re.MULTILINE,
            )

            # Clean prompt subheading labels
            page = re.sub(
                r"^\s*-\s+\*\*Gist for ([^\n:]+):\*\*",
                r'<div style="font-weight: 600; color: #1e3a8a; font-size: 0.88rem; margin: 0.65rem 0 0.15rem 0;">• \1:</div><div style="font-style: italic; color: #64748b; font-size: 0.80rem;">10-Word Subheading Gist:</div>',
                page,
                flags=re.MULTILINE,
            )

            # Style sub-headings / parts
            page = re.sub(
                r"^###\s+([^\n]+)",
                r'<div style="font-weight: 700; color: #0f172a; font-size: 0.95rem; margin: 0.85rem 0 0.35rem 0;">\1</div>',
                page,
                flags=re.MULTILINE,
            )

            wrapped_page = f'<div class="ws-container">\n{page.strip()}\n</div>'
            formatted_pages.append(wrapped_page)

        else:
            formatted_pages.append(f'<div class="ws-container">\n{page.strip()}\n</div>')

    page_break_divider = (
        '\n\n<div style="margin: 2.5rem 0 2rem 0; border-top: 2px dashed #cbd5e1; text-align: center;">'
        '<span style="background: #ffffff; color: #64748b; font-size: 0.78rem; font-weight: 700; padding: 0.25rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 9999px; position: relative; top: -12px; text-transform: uppercase; letter-spacing: 0.06em;">'
        'Page Break'
        '</span></div>\n\n'
    )

    full_html = page_break_divider.join(formatted_pages)
    return f"{COMMON_CSS}\n{full_html}"
