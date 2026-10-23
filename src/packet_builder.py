import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

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
from src.blueprint_designer import recommend_section_strategies
from src.agent_team import (
    SOLID_LINE,
    DOTTED_LINE,
    sanitize_aesthetics,
    enforce_page_budget_guardrail,
)


# ─────────────────────────────────────────────────────────────────────────────
# CURATED 100% PASSAGE-GROUNDED KNOWLEDGE BASE FOR CHAPTER 5 (ALL 17 SPREADS)
# ─────────────────────────────────────────────────────────────────────────────

CHAPTER_5_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "1.1": {
        "printed_main_idea": "After the French and Indian War, the British government enacted laws that restricted some of the colonies' freedoms.",
        "exemplar_central_idea": "Although colonists felt optimistic after helping Britain win the French and Indian War, King George III and Parliament angered both western settlers and eastern city residents by passing the Proclamation of 1763 and the Quartering Act of 1765 to control the colonies.",
        "scaffolded_central_idea_stem": "Although colonists were optimistic after the French and Indian War, tensions grew because King George III passed the _________________________ (which banned settling west of the Appalachians) and Parliament passed the _________________________ (which forced colonists to house British soldiers).",
        "word_bank": ["Proclamation of 1763", "Quartering Act", "Appalachian Mountains", "militias", "Covenant Chain", "freedoms"],
        "subheadings": [
            {
                "name": "PROBLEMS ARISE (p. 178)",
                "gist": "King George III issued the Proclamation of 1763 to ban colonial settlement west of the Appalachian Mountains and keep peace with Native Americans.",
                "cause": "After the costly French and Indian War, King George III wanted to maintain control of the colonies and limit conflict between colonists and Native Americans.",
                "effect": "The king issued the **Proclamation of 1763**, ordering colonists to stay east of the Appalachian Mountains, which angered western settlers.",
                "say_something_q": "Why did King George III issue the Proclamation of 1763, and how did western settlers react to it?",
                "cloze_stmt": "To prevent costly fighting with Native Americans after the war, King George III issued the _________________________, which banned colonists from settling west of the _________________________ Mountains.",
                "citation": '[p. 178, "PROBLEMS ARISE", ¶3–4]',
            },
            {
                "name": "SOLDIERS IN THE COLONIES (pp. 178–179)",
                "gist": "Parliament passed the Quartering Act in 1765 requiring colonists to house British troops in port cities, while western migration strained the Covenant Chain.",
                "cause": "Britain moved soldiers into port cities like New York and Boston to enforce laws and passed the **Quartering Act (1765)** requiring colonists to house them.",
                "effect": "The New York assembly refused to enforce the law, and the presence of troops provoked hostility among civilians who began identifying more as Americans.",
                "say_something_q": "What did the Quartering Act of 1765 require, and how did it affect relations between British soldiers and colonial civilians?",
                "cloze_stmt": "In 1765, Parliament passed the _________________________, forcing colonists in port cities like New York and Boston to provide housing for British soldiers in inns, stables, and barns.",
                "citation": '[pp. 178–179, "SOLDIERS IN THE COLONIES", ¶1–4]',
            },
        ],
        "perspectives": {
            "side_a_label": "British Government (King George III & Parliament)",
            "side_a_point": "Believed the colonies existed to support the mother country, needed to stay east of the Appalachians to keep peace, and should house British troops enforcing the law [p. 178, ¶3; p. 179, ¶1].",
            "side_b_label": "American Colonists (Western Settlers & Port Cities)",
            "side_b_point": "Felt the Proclamation of 1763 restricted their freedom to expand westward and resented being forced to house peacetime soldiers under the Quartering Act [p. 178, ¶4; p. 179, ¶3–4].",
        },
        "reading_check_a": "The Proclamation of 1763 aimed to limit contact and keep peace between colonists and Native Americans by banning settlement west of the Appalachians [p. 178, ¶3–4]; the Quartering Act required colonists to provide housing for British soldiers enforcing laws in port cities [pp. 178–179, ¶1–3].",
        "skill_q2_a": "Both eastern and western colonists felt British laws restricted their freedoms: western settlers objected to the Proclamation of 1763 blocking westward expansion [p. 178, ¶4], while eastern city residents resented being forced to house British troops under the Quartering Act [pp. 178–179, ¶1–4].",
        "word_meaning_q3_a": "'Prosperous' means economically successful and thriving after decades of economic growth [p. 178, \"PROBLEMS ARISE\", ¶2].",
        "critical_viewing_a": "The engraving of British troops in a colonial home shows the resentment and tension caused by forcing residents to quarter soldiers [p. 178]; the 1763 map shows that settlers pushing west of the Proclamation Line broke the peaceful promises of the Covenant Chain with the Iroquois League [p. 179, ¶5–6].",
    },
    "1.2": {
        "printed_main_idea": "British attempts to impose taxes and exert greater control over the colonies caused growing anger and resentment among colonists.",
        "exemplar_central_idea": "To pay off heavy debt from the French and Indian War and fund 10,000 soldiers, Prime Minister George Grenville and Parliament passed the Sugar Act and Currency Act of 1764, prompting colonists to protest 'no taxation without representation.'",
        "scaffolded_central_idea_stem": "To pay off its debt from the French and Indian War, Prime Minister _________________________ and Parliament passed the _________________________ and Currency Act of 1764, which colonists opposed because they had no _________________________ in Parliament.",
        "word_bank": ["revenue", "George Grenville", "Sugar Act", "Currency Act", "tyranny", "representation"],
        "subheadings": [
            {
                "name": "WAR DEBT (p. 180)",
                "gist": "Faced with huge war debt and the cost of keeping 10,000 troops in North America, Prime Minister George Grenville decided to tax the colonies directly for revenue.",
                "cause": "Britain had a hefty debt from the French and Indian War and was still paying to keep 10,000 soldiers in North America.",
                "effect": "Prime Minister **George Grenville** decided to seek **revenue** by taxing the colonies directly rather than letting colonial assemblies pass taxes.",
                "say_something_q": "Why did Britain need revenue after the French and Indian War, and what did Prime Minister George Grenville decide to do?",
                "cloze_stmt": "Because Britain needed _________________________ (income) to pay off its war debt and maintain 10,000 soldiers, Prime Minister _________________________ decided to tax the colonies directly.",
                "citation": '[p. 180, "WAR DEBT", ¶1–3]',
            },
            {
                "name": "ACTS OF PARLIAMENT (p. 181)",
                "gist": "Parliament passed the Sugar Act and Currency Act in 1764 and tightened the Navigation Acts, leading colonists to protest 'no taxation without representation.'",
                "cause": "In 1764, Parliament passed the **Sugar Act** (to stop molasses smuggling), the **Currency Act** (banning colonial paper money), and tightened the Navigation Acts.",
                "effect": "Colonists suffered money shortages, accused Britain of **tyranny**, and rallied behind the slogan **'no taxation without representation.'**",
                "say_something_q": "How did the Sugar Act and Currency Act of 1764 affect the colonies, and why did colonists call direct British taxes 'tyranny'?",
                "cloze_stmt": "In 1764, the _________________________ taxed molasses to stop smuggling and the _________________________ banned colonial paper money, leading colonists to protest 'no taxation without _________________________.'",
                "citation": '[p. 181, "ACTS OF PARLIAMENT", ¶1–5]',
            },
        ],
        "perspectives": {
            "side_a_label": "Prime Minister George Grenville & Parliament",
            "side_a_point": "Reasoned that because the colonies benefited most from the French and Indian War and were protected by 10,000 troops, Parliament had the right to tax them directly [p. 180, ¶1–3].",
            "side_b_label": "Colonial Merchants & Assemblies",
            "side_b_point": "Voiced grievances against mercantilist restrictions and argued Parliament could not impose direct taxes because colonists had no elected representatives in Parliament [p. 181, ¶3–5].",
        },
        "reading_check_a": "Britain tried to raise revenue and control the colonies by passing the Sugar Act (lowering the molasses duty to stop smuggling and collect revenue), passing the Currency Act (requiring British currency only), and tightening the Navigation Acts [p. 181, \"ACTS OF PARLIAMENT\", ¶1–4].",
        "skill_q2_a": "Both acts reinforced mercantilism—trade designed to bring wealth primarily to the mother country—by stopping colonial smuggling, banning colonial paper money, and forcing trade to benefit Britain [p. 181, ¶1–4].",
        "word_meaning_q3_a": "The Sugar and Currency Acts created a shortage of British currency, made business harder for colonial merchants, and provoked widespread grievances [p. 181, ¶1–3].",
        "critical_viewing_a": "The 1756 and 1759 colonial currency notes show how colonies relied on their own detailed paper money before the Currency Act of 1764 made colonial paper money useless [p. 181, ¶2–3, ¶6].",
    },
    "1.3": {
        "printed_main_idea": "Colonists united in protest against the Stamp Act, forcing the British Parliament to repeal the unpopular law.",
        "exemplar_central_idea": "When Parliament passed the Stamp Act of 1765 taxing all colonial paper goods, colonists united through Patrick Henry's resolutions, the Sons of Liberty, the Stamp Act Congress, and boycotts until Britain repealed the law in 1766.",
        "scaffolded_central_idea_stem": "When Parliament passed the _________________________ of 1765 taxing paper items, colonists united through groups like the _________________________, the Stamp Act Congress, and boycotts, forcing Parliament to _________________________ the law in 1766.",
        "word_bank": ["Stamp Act", "Sons of Liberty", "Patrick Henry", "boycott", "repeal", "Declaratory Act"],
        "subheadings": [
            {
                "name": "A NEW TAX ON PAPER (p. 182)",
                "gist": "Parliament passed the Stamp Act in 1765 requiring colonists to buy an official British stamp on legal documents, newspapers, and playing cards.",
                "cause": "Parliament passed the **Stamp Act of 1765**, requiring an official government stamp on all colonial paper items (wills, newspapers, playing cards).",
                "effect": "Unlike earlier trade duties, this direct internal tax affected almost every colonist and sparked immediate outrage.",
                "say_something_q": "What did the Stamp Act of 1765 tax, and why did it anger so many colonists?",
                "cloze_stmt": "In 1765, Parliament passed the _________________________, which required colonists to buy an official tax stamp for all paper goods, including legal documents and newspapers.",
                "citation": '[p. 182, ¶1–2]',
            },
            {
                "name": "COLONIAL RESISTANCE AND REPEAL (pp. 182–183)",
                "gist": "Patrick Henry, the Sons of Liberty, the Stamp Act Congress, and widespread boycotts pressured Parliament to repeal the Stamp Act in 1766, though Parliament passed the Declaratory Act.",
                "cause": "Patrick Henry passed resolutions in Virginia, the **Sons of Liberty** protested in the streets, 9 colonies met at the **Stamp Act Congress**, and merchants organized a **boycott** of British goods.",
                "effect": "British merchants lost money and pressured Parliament to **repeal** the Stamp Act in 1766, though Parliament immediately passed the **Declaratory Act** claiming full authority over the colonies.",
                "say_something_q": "How did the Sons of Liberty, the Stamp Act Congress, and colonial boycotts convince Parliament to repeal the Stamp Act in 1766?",
                "cloze_stmt": "Colonial protests led by the _________________________ and a widespread _________________________ of British goods forced Parliament to repeal the Stamp Act in 1766, though it passed the _________________________ Act to assert its authority.",
                "citation": '[pp. 182–183, ¶3–6]',
            },
        ],
        "perspectives": {
            "side_a_label": "British Parliament (Declaratory Act of 1766)",
            "side_a_point": "Repealed the Stamp Act only because boycotts hurt British trade, while passing the Declaratory Act stating Parliament had total authority to make laws for the colonies [p. 183].",
            "side_b_label": "Patrick Henry, Sons of Liberty & Stamp Act Congress",
            "side_b_point": "Insisted that only colonial assemblies had the right to tax colonists and used petitions and boycotts to resist unjust taxation [pp. 182–183].",
        },
        "reading_check_a": "Colonists opposed the Stamp Act through legislative resolutions (Patrick Henry), street protests by the Sons of Liberty, petitions from the Stamp Act Congress, and boycotts of British goods [pp. 182–183].",
        "skill_q2_a": "Boycotts reduced British merchants' sales and profits, leading British business owners to pressure Parliament to repeal the Stamp Act in 1766 [p. 183].",
        "word_meaning_q3_a": "To 'repeal' means to officially cancel or revoke a law, as Parliament did with the Stamp Act in 1766 [p. 183].",
        "critical_viewing_a": "The skull-and-crossbones anti-Stamp Act emblem shows that colonial printers viewed the Stamp Act as the 'death' of a free press and colonial liberty [p. 182].",
    },
    "1.4": {
        "printed_main_idea": "Benjamin Franklin served as a colonial spokesperson in London and warned Parliament that colonists would never submit to internal taxes without representation.",
        "exemplar_central_idea": "Testifying before Parliament in 1766, Benjamin Franklin defended colonial self-taxation and warned that British troops enforcing the Stamp Act would find no rebellion—Wait, they would actually create one.",
        "scaffolded_central_idea_stem": "When _________________________ testified before Parliament in 1766, he explained that colonists had lost respect for Britain and warned that sending troops to enforce the _________________________ would cause a rebellion.",
        "word_bank": ["Benjamin Franklin", "Stamp Act", "Parliament", "rebellion", "respect"],
        "subheadings": [
            {
                "name": "BENJAMIN FRANKLIN TESTIFIES BEFORE PARLIAMENT (pp. 184–185)",
                "gist": "In February 1766, Benjamin Franklin answered 174 questions before Parliament, explaining why colonists rejected the Stamp Act.",
                "cause": "Parliament questioned Benjamin Franklin in London in 1766 about whether colonists would pay the Stamp Act if it were moderated.",
                "effect": "Franklin declared colonists would never pay it unless forced by arms, warning that soldiers sent to enforce it would not find a rebellion, 'they may indeed make one.'",
                "say_something_q": "What warning did Benjamin Franklin give Parliament about sending soldiers to enforce the Stamp Act?",
                "cloze_stmt": "Testifying before Parliament in 1766, _________________________ warned that British soldiers sent to enforce the Stamp Act would not find a rebellion, but might _________________________ one.",
                "citation": '[pp. 184–185, ¶1–4]',
            },
        ],
        "perspectives": {
            "side_a_label": "Members of Parliament Questioning Franklin",
            "side_a_point": "Asked why colonists refused to pay a small stamp tax when British troops protected them [p. 184].",
            "side_b_label": "Benjamin Franklin (Colonial Agent)",
            "side_b_point": "Explained that colonists gladly taxed themselves through their own assemblies, but would never submit to taxes imposed without their consent [pp. 184–185].",
        },
        "reading_check_a": "Franklin told Parliament that colonial attitudes toward Britain had changed from deep respect to resentment because of new taxes and laws passed without colonial representation [pp. 184–185].",
        "skill_q2_a": "Franklin's testimony helped convince Parliament that enforcing the Stamp Act by force would backfire and trigger a rebellion, leading to its repeal [p. 185].",
        "word_meaning_q3_a": "Franklin meant that colonists were not currently rebelling, but using military force to collect the tax would provoke an armed uprising [p. 185].",
        "critical_viewing_a": "The illustration of Franklin before the House of Commons highlights his role as the leading diplomatic voice defending colonial rights in London [pp. 184–185].",
    },
    "2.1": {
        "printed_main_idea": "The Townshend Acts sparked new colonial boycotts, the formation of the Daughters of Liberty, and appeals to John Locke's ideas of natural rights.",
        "exemplar_central_idea": "When Parliament passed the Townshend Acts of 1767 taxing everyday imports and authorizing writs of assistance, colonists drew on John Locke's philosophy of natural rights and organized widespread boycotts led by the Daughters of Liberty.",
        "scaffolded_central_idea_stem": "In response to the _________________________ of 1767, colonists cited John Locke's ideas of _________________________ and organized boycotts supported by the _________________________.",
        "word_bank": ["Townshend Acts", "writs of assistance", "Daughters of Liberty", "John Locke", "natural rights", "boycott"],
        "subheadings": [
            {
                "name": "THE TOWNSHEND ACTS AND WRITS OF ASSISTANCE (p. 186)",
                "gist": "In 1767, Parliament passed the Townshend Acts taxing glass, paper, paint, lead, and tea, and used writs of assistance to search colonial property.",
                "cause": "Parliament passed the **Townshend Acts (1767)** placing duties on imported glass, lead, paint, paper, and tea, and allowed customs officers to use **writs of assistance**.",
                "effect": "Colonists viewed the import duties as disguised taxes and protested that writs of assistance violated their rights by allowing searches without specific warrants.",
                "say_something_q": "What did the Townshend Acts of 1767 tax, and why did colonists object to writs of assistance?",
                "cloze_stmt": "The _________________________ of 1767 taxed imports like glass, paper, and tea, while _________________________ allowed customs officers to search colonial ships and homes.",
                "citation": '[p. 186, ¶1–3]',
            },
            {
                "name": "BOYCOTTS AND NATURAL RIGHTS (pp. 186–187)",
                "gist": "The Daughters of Liberty made homespun goods to support boycotts, while Patriots used John Locke's ideas of natural rights and consent of the governed to challenge British rule.",
                "cause": "Colonial leaders organized boycotts of British imports, the **Daughters of Liberty** wove homespun cloth, and thinkers cited **John Locke's** natural rights.",
                "effect": "Locke's argument that government requires the **consent of the governed** and must protect life, liberty, and property gave colonists a powerful philosophical justification for protest.",
                "say_something_q": "How did the Daughters of Liberty and John Locke's ideas of natural rights strengthen colonial resistance to the Townshend Acts?",
                "cloze_stmt": "The _________________________ supported boycotts by weaving homespun cloth, while Patriots used philosopher _________________________'s idea that government must protect natural rights.",
                "citation": '[pp. 186–187, ¶4–6]',
            },
        ],
        "perspectives": {
            "side_a_label": "Charles Townshend & British Customs Officials",
            "side_a_point": "Argued external duties on imported goods were legal regulation of trade and used writs of assistance to crack down on colonial smuggling [p. 186].",
            "side_b_label": "Daughters of Liberty & Enlightenment Patriots",
            "side_b_point": "Boycotted British goods and argued from John Locke that any tax or search without the consent of the governed violated natural rights [pp. 186–187].",
        },
        "reading_check_a": "The Townshend Acts taxed imported glass, lead, paint, paper, and tea and authorized writs of assistance; colonists responded with boycotts and homespun goods made by the Daughters of Liberty [pp. 186–187].",
        "skill_q2_a": "John Locke argued that all people possess natural rights to life, liberty, and property, and that government power comes from the consent of the governed—ideas colonists used to argue Parliament's taxes were unjust [p. 187].",
        "word_meaning_q3_a": "A 'writ of assistance' was a legal document functioning as a general search warrant allowing British customs officials to search any ship or building for smuggled goods [p. 186].",
        "critical_viewing_a": "Colonial women spinning cloth and brewing herbal tea showed how the Daughters of Liberty turned everyday household choices into effective economic resistance [p. 187].",
    },
    "2.2": {
        "printed_main_idea": "Growing tensions between Bostonians and British soldiers erupted into violence in the Boston Massacre of 1770.",
        "exemplar_central_idea": "In March 1770, rising hostility between Boston colonists and British troops erupted into the Boston Massacre, killing Crispus Attucks and four others, which Samuel Adams and Paul Revere used as propaganda while John Adams defended the soldiers in court.",
        "scaffolded_central_idea_stem": "On March 5, 1770, tensions in Boston led to the _________________________, where five colonists including _________________________ were killed, an event Patriots used as anti-British propaganda.",
        "word_bank": ["Boston Massacre", "Crispus Attucks", "Paul Revere", "Samuel Adams", "John Adams", "committees of correspondence"],
        "subheadings": [
            {
                "name": "VIOLENCE IN BOSTON (p. 188)",
                "gist": "On March 5, 1770, a confrontation between an angry Boston crowd and British soldiers resulted in soldiers firing and killing five colonists, including Crispus Attucks.",
                "cause": "On March 5, 1770, a crowd of Boston colonists insulted and threw snowballs and ice at British soldiers guarding the Customs House.",
                "effect": "In the confusion, British soldiers fired into the crowd, killing five people—including dockworker **Crispus Attucks**—in what became known as the **Boston Massacre**.",
                "say_something_q": "What happened outside the Boston Customs House on March 5, 1770, and who was Crispus Attucks?",
                "cloze_stmt": "On March 5, 1770, British soldiers fired into a crowd in the _________________________, killing five colonists including _________________________, a dockworker of African and Native American descent.",
                "citation": '[p. 188, ¶1–3]',
            },
            {
                "name": "PROPAGANDA AND TRIAL (p. 189)",
                "gist": "Paul Revere's engraving and Samuel Adams's committees of correspondence rallied colonial outrage, while John Adams defended the soldiers to prove colonial fairness.",
                "cause": "**Paul Revere** created a dramatic engraving of the shooting, **Samuel Adams** organized **committees of correspondence**, and **John Adams** agreed to defend the soldiers in court.",
                "effect": "The engraving fueled anti-British anger across the colonies, while John Adams won acquittal for most soldiers to show colonists believed in the rule of law.",
                "say_something_q": "How did Paul Revere's response to the Boston Massacre differ from John Adams's response?",
                "cloze_stmt": "While _________________________'s engraving stirred outrage against Britain, lawyer _________________________ defended the British soldiers in court to show colonists valued fair trials.",
                "citation": '[p. 189, ¶1–4]',
            },
        ],
        "perspectives": {
            "side_a_label": "Paul Revere & Samuel Adams (Patriot Propaganda)",
            "side_a_point": "Portrayed the shooting as a deliberate, unprovoked 'massacre' of peaceful citizens by British troops to unite the colonies against British rule [p. 189].",
            "side_b_label": "John Adams (Defense Attorney at the Trial)",
            "side_b_point": "Argued that even unpopular British soldiers deserved a fair trial under the law and that the soldiers had acted in self-defense against an unruly crowd [p. 189].",
        },
        "reading_check_a": "The Boston Massacre occurred when tensions between Boston civilians and British soldiers boiled over on March 5, 1770, leaving Crispus Attucks and four others dead [p. 188].",
        "skill_q2_a": "Paul Revere's engraving showed Captain Preston ordering troops to fire in an orderly line at peaceful citizens, omitting the crowd throwing snowballs and ice at the soldiers [p. 189].",
        "word_meaning_q3_a": "Committees of correspondence were networks organized by Samuel Adams to share news and coordinate colonial responses to British actions [p. 189].",
        "critical_viewing_a": "Paul Revere's engraving 'The Bloody Massacre' depicts British soldiers firing in formation at helpless townspeople, shaping public opinion against Britain [p. 189].",
    },
    "2.3": {
        "printed_main_idea": "The Boston Tea Party led Parliament to pass the Coercive Acts, which colonists called the Intolerable Acts.",
        "exemplar_central_idea": "To protest the Tea Act of 1773, the Sons of Liberty staged the Boston Tea Party by dumping 342 chests of tea into Boston Harbor, prompting Parliament to punish Massachusetts with the Coercive (Intolerable) Acts of 1774.",
        "scaffolded_central_idea_stem": "In December 1773, the Sons of Liberty protested the _________________________ by staging the _________________________, which led Parliament to punish Massachusetts with the _________________________ Acts.",
        "word_bank": ["Tea Act", "Boston Tea Party", "East India Company", "Coercive Acts", "Intolerable Acts", "Boston Harbor"],
        "subheadings": [
            {
                "name": "THE TEA ACT AND BOSTON TEA PARTY (pp. 190–191)",
                "gist": "In 1773, Parliament passed the Tea Act giving the British East India Company a monopoly, prompting the Sons of Liberty to dump 342 chests of tea into Boston Harbor.",
                "cause": "Parliament passed the **Tea Act of 1773**, giving the British **East India Company** control over the colonial tea trade while keeping the tax on tea.",
                "effect": "On December 16, 1773, the **Sons of Liberty** disguised themselves as Native Americans, boarded three ships, and dumped 342 chests of tea in the **Boston Tea Party**.",
                "say_something_q": "Why did colonists oppose the Tea Act of 1773 even though it made tea cheaper, and what happened on December 16, 1773?",
                "cloze_stmt": "To protest the _________________________ of 1773, members of the Sons of Liberty boarded ships on December 16, 1773, and dumped 342 chests of tea in the _________________________.",
                "citation": '[pp. 190–191, ¶1–3]',
            },
            {
                "name": "THE COERCIVE (INTOLERABLE) ACTS (p. 191)",
                "gist": "Outraged by the destroyed tea, King George III and Parliament passed the Coercive Acts in 1774 to close Boston Harbor and place Massachusetts under military control.",
                "cause": "King George III and Parliament were furious over the destruction of the tea and wanted to punish Massachusetts until the tea was paid for.",
                "effect": "In 1774, Parliament passed the **Coercive Acts** (called the **Intolerable Acts** by colonists), closing Boston Harbor, limiting town meetings, and placing Boston under military rule.",
                "say_something_q": "How did Parliament punish Massachusetts in 1774, and why did colonists call these laws the 'Intolerable Acts'?",
                "cloze_stmt": "In 1774, Parliament punished Boston by passing the _________________________ Acts (which colonists called the _________________________ Acts), closing Boston Harbor until the ruined tea was paid for.",
                "citation": '[p. 191, ¶4–6]',
            },
        ],
        "perspectives": {
            "side_a_label": "Sons of Liberty (Boston Tea Party)",
            "side_a_point": "Viewed the Tea Act as a trick to make colonists accept taxation without representation and destroyed 342 chests of tea as a peaceful political protest [p. 191].",
            "side_b_label": "King George III & Parliament (Coercive Acts)",
            "side_b_point": "Saw the Boston Tea Party as illegal destruction of property and passed the Coercive Acts to force Massachusetts into submission [p. 191].",
        },
        "reading_check_a": "Colonists objected to the Tea Act because it gave the British East India Company an unfair monopoly and kept the tax on tea without colonial representation [p. 191].",
        "skill_q2_a": "Instead of isolating Massachusetts, the harsh Intolerable Acts outraged other colonies, who sent food and supplies to Boston and united in support [p. 191].",
        "word_meaning_q3_a": "'Coercive' means using force or threats to make people obey; colonists called them 'Intolerable' because they were too harsh to endure [p. 191].",
        "critical_viewing_a": "The painting of the Boston Tea Party shows disguised colonists methodically dumping tea chests into the harbor while crowds watch from the wharf [pp. 190–191].",
    },
    "2.4": {
        "printed_main_idea": "Artifacts at the Museum of the American Revolution preserve the everyday objects and symbols used by colonists during the revolutionary era.",
        "exemplar_central_idea": "Through preserved artifacts like the Liberty Tree tavern sign, colonial newspapers, and Washington's headquarters tent, the Museum of the American Revolution shows how ordinary people experienced the struggle for independence.",
        "scaffolded_central_idea_stem": "The Museum of the American Revolution preserves historical artifacts such as _________________________ to help visitors understand how colonists united for independence.",
        "word_bank": ["artifacts", "Liberty Tree", "Museum of the American Revolution", "primary sources"],
        "subheadings": [
            {
                "name": "CURATING HISTORY: MUSEUM OF THE AMERICAN REVOLUTION (pp. 192–193)",
                "gist": "Located in Philadelphia, the Museum of the American Revolution displays artifacts like the Liberty Tree sign and George Washington's war tent.",
                "cause": "Historians and curators collected authentic objects, weapons, documents, and George Washington's field tent from the Revolutionary era.",
                "effect": "These physical artifacts allow modern students and visitors to see how ordinary colonists organized protests and fought for independence.",
                "say_something_q": "How do physical artifacts in the Museum of the American Revolution help historians understand the colonial protest movement?",
                "cloze_stmt": "In Philadelphia, the _________________________ preserves artifacts like the Liberty Tree sign and George Washington's tent.",
                "citation": '[pp. 192–193, ¶1–3]',
            },
        ],
        "perspectives": {
            "side_a_label": "Patriot Symbols (Liberty Tree)",
            "side_a_point": "Served as gathering places where colonists met to protest British taxes and share news [p. 192].",
            "side_b_label": "Museum Curators Today",
            "side_b_point": "Preserve objects from diverse participants—Patriots, Loyalists, women, and African Americans—to tell the full story of the Revolution [pp. 192–193].",
        },
        "reading_check_a": "Curators preserve objects like the Liberty Tree sign and Washington's tent to connect visitors with the real experiences of Revolutionary Americans [pp. 192–193].",
        "skill_q2_a": "Physical artifacts provide concrete primary-source evidence of what people wore, carried, and valued during historical events [pp. 192–193].",
        "word_meaning_q3_a": "To 'curate' means to select, organize, and care for historical items in a museum collection [p. 192].",
        "critical_viewing_a": "The preserved artifacts illustrate the transition from tavern protests to organized military campaigns [pp. 192–193].",
    },
    "3.1": {
        "printed_main_idea": "Colonial leaders met at the First Continental Congress in 1774 while local militias and Minutemen prepared for possible armed conflict.",
        "exemplar_central_idea": "In response to the Intolerable Acts, delegates from 12 colonies met at the First Continental Congress in 1774 to petition King George III and expand boycotts, while colonial militias and Minutemen stockpiled weapons for war.",
        "scaffolded_central_idea_stem": "In 1774, delegates from 12 colonies met at the _________________________ to petition the king and boycott British goods, while citizen soldiers called _________________________ trained to fight at a minute's notice.",
        "word_bank": ["First Continental Congress", "Patrick Henry", "Minutemen", "militias", "Philadelphia", "Intolerable Acts"],
        "subheadings": [
            {
                "name": "THE FIRST CONTINENTAL CONGRESS (p. 194)",
                "gist": "In September 1774, 55 delegates from 12 colonies met in Philadelphia at the First Continental Congress to demand the repeal of the Intolerable Acts.",
                "cause": "To respond to the Intolerable Acts, 55 delegates from 12 colonies (all except Georgia) met in Philadelphia in September 1774 for the **First Continental Congress**.",
                "effect": "Delegates petitioned King George III to respect their rights, halted trade with Britain, and urged each colony to train its own **militia**.",
                "say_something_q": "What three main actions did the delegates at the First Continental Congress take in 1774?",
                "cloze_stmt": "Meeting in Philadelphia in 1774, the _________________________ sent a petition to King George III, expanded colonial boycotts, and urged colonies to prepare their _________________________.",
                "citation": '[p. 194, ¶1–3]',
            },
            {
                "name": "MILITIAS AND MINUTEMEN PREPARE (pp. 194–195)",
                "gist": "Patrick Henry declared 'Give me liberty, or give me death!' while New England militias and Minutemen stored gunpowder and trained in Concord.",
                "cause": "King George III rejected the Congress's petition, and **Patrick Henry** urged Virginia to arm itself ('Give me liberty, or give me death!').",
                "effect": "New England towns trained **Minutemen**—volunteer soldiers ready to fight at a minute's notice—and stored military supplies in towns like Concord, Massachusetts.",
                "say_something_q": "Who were the Minutemen, and what did Patrick Henry mean when he declared, 'I am not a Virginian, but an American'?",
                "cloze_stmt": "_________________________ declared 'Give me liberty, or give me death!' while New England volunteer soldiers called _________________________ trained to defend their towns at a minute's notice.",
                "citation": '[pp. 194–195, ¶4–6]',
            },
        ],
        "perspectives": {
            "side_a_label": "Moderate Delegates at the First Continental Congress",
            "side_a_point": "Hoped King George III would repeal the Intolerable Acts peacefully once he read their petition and felt the impact of trade boycotts [p. 194].",
            "side_b_label": "Patrick Henry & New England Minutemen",
            "side_b_point": "Believed war with Britain was unavoidable and that colonies had to unite as Americans and arm their militias immediately [pp. 194–195].",
        },
        "reading_check_a": "The First Continental Congress petitioned the king to repeal the Intolerable Acts, banned trade with Britain, and called on each colony to train militias [p. 194].",
        "skill_q2_a": "Patrick Henry's statement 'I am not a Virginian, but an American' showed that colonists were uniting across colony lines behind a shared national identity [p. 194].",
        "word_meaning_q3_a": "'Minutemen' were colonial militia members who boasted they could be ready to march and fight at just a minute's notice [p. 195].",
        "critical_viewing_a": "The painting of Patrick Henry addressing the Virginia convention captures the emotional intensity of Patriots calling for armed defense of liberty [p. 195].",
    },
    "3.2": {
        "printed_main_idea": "On the night of April 18, 1775, Paul Revere, William Dawes, and Samuel Prescott rode through the Massachusetts countryside to warn that British troops were marching toward Concord.",
        "exemplar_central_idea": "When British General Thomas Gage sent 700 troops on April 18, 1775, to seize colonial weapons in Concord, two lanterns in the Old North Church signaled Paul Revere and William Dawes to ride through the night and alert the Minutemen.",
        "scaffolded_central_idea_stem": "On April 18, 1775, when British General _________________________ sent troops across the Charles River toward Concord, _________________________ and William Dawes rode through the night to warn the colonial militias.",
        "word_bank": ["Paul Revere", "William Dawes", "Samuel Prescott", "Thomas Gage", "Old North Church", "Concord"],
        "subheadings": [
            {
                "name": "TWO IF BY SEA (p. 196)",
                "gist": "General Thomas Gage ordered 700 British soldiers to march secretly to Concord, prompting two signal lanterns to be hung in Boston's Old North Church.",
                "cause": "In April 1775, British General **Thomas Gage** ordered 700 troops to march from Boston to **Concord** to seize colonial gunpowder and arrest Samuel Adams and John Hancock.",
                "effect": "Patriot lookouts hung **two lanterns** in the steeple of the **Old North Church** ('one if by land, two if by sea') to signal that British troops were crossing the Charles River by boat.",
                "say_something_q": "What was General Thomas Gage's secret plan in April 1775, and what did the two lanterns in the Old North Church mean?",
                "cloze_stmt": "When General _________________________ sent 700 soldiers to seize colonial weapons in Concord, Patriots hung two lanterns in the _________________________ to show troops were crossing by water.",
                "citation": '[p. 196, ¶1–3]',
            },
            {
                "name": "THE MIDNIGHT RIDE (pp. 196–197)",
                "gist": "Paul Revere and William Dawes warned Lexington and Samuel Adams, and after Revere was detained by a British patrol, Samuel Prescott carried the warning to Concord.",
                "cause": "**Paul Revere** and **William Dawes** rode along separate routes to **Lexington** to warn Samuel Adams, John Hancock, and local Minutemen.",
                "effect": "Although a British patrol detained Revere after Lexington, fellow rider **Samuel Prescott** escaped and reached **Concord** in time to alert the militia.",
                "say_something_q": "How did Paul Revere, William Dawes, and Samuel Prescott work together to make sure the warning reached both Lexington and Concord?",
                "cloze_stmt": "_________________________ and William Dawes warned Samuel Adams and John Hancock in Lexington, and rider _________________________ escaped a British patrol to warn Concord.",
                "citation": '[pp. 196–197, ¶4–6]',
            },
        ],
        "perspectives": {
            "side_a_label": "General Thomas Gage (British Commander)",
            "side_a_point": "Attempted a secret nighttime march on April 18, 1775, to confiscate Patriot weapons at Concord before a full rebellion could start [p. 196].",
            "side_b_label": "Midnight Riders (Revere, Dawes & Prescott)",
            "side_b_point": "Used an organized alarm network of church lanterns and horseback riders to alert every town along the road before the British arrived [pp. 196–197].",
        },
        "reading_check_a": "General Gage sent troops to arrest Patriot leaders Samuel Adams and John Hancock in Lexington and destroy colonial military supplies stored in Concord [p. 196].",
        "skill_q2_a": "Using two lanterns in the Old North Church and multiple riders on different roads ensured that even when Revere was captured, Samuel Prescott still reached Concord [pp. 196–197].",
        "word_meaning_q3_a": "The signal 'one if by land, two if by sea' referred to whether British troops marched out of Boston by land or rowed across the Charles River [p. 196].",
        "critical_viewing_a": "The map of the Midnight Ride traces the separate routes of Revere and Dawes converging at Lexington and Prescott's final dash to Concord [p. 197].",
    },
    "3.3": {
        "printed_main_idea": "The first battles of the American Revolution took place at Lexington and Concord on April 19, 1775.",
        "exemplar_central_idea": "On April 19, 1775, the American Revolution began when an unknown 'shot heard round the world' sparked gunfire at Lexington and colonial Minutemen forced British troops to retreat from Concord's North Bridge all the way back to Boston.",
        "scaffolded_central_idea_stem": "On April 19, 1775, the first battles of the Revolutionary War broke out at _________________________ and _________________________, where Minutemen forced the British army to retreat back to Boston.",
        "word_bank": ["Lexington", "Concord", "John Parker", "North Bridge", "shot heard round the world", "retreat"],
        "subheadings": [
            {
                "name": "CONFRONTATION AT LEXINGTON (p. 198)",
                "gist": "At dawn on April 19, 1775, Captain John Parker's 70 Minutemen faced 700 British soldiers on Lexington Green when the 'shot heard round the world' was fired.",
                "cause": "At dawn on April 19, 1775, about 70 Minutemen led by Captain **John Parker** stood on **Lexington Green** facing 700 British troops.",
                "effect": "Someone fired an unknown first shot—the **'shot heard round the world'**—and British soldiers fired a volley that killed 8 Minutemen and wounded 10.",
                "say_something_q": "What happened at Lexington Green at dawn on April 19, 1775, and why is that first gunshot called the 'shot heard round the world'?",
                "cloze_stmt": "At dawn on April 19, 1775, Captain _________________________ and 70 Minutemen faced British troops at _________________________, where the 'shot heard round the world' killed 8 colonists.",
                "citation": '[p. 198, ¶1–3]',
            },
            {
                "name": "FIGHTING AT CONCORD AND RETREAT (pp. 198–199)",
                "gist": "Finding most weapons hidden in Concord, British troops fought militiamen at the North Bridge and suffered heavy casualties from colonial sharpshooters on the march back to Boston.",
                "cause": "British troops marched on to **Concord**, where women and militia had already hidden most weapons, and clashed with hundreds of militiamen at **Concord's North Bridge**.",
                "effect": "Thousands of colonial militiamen fired from behind stone walls and trees along the 16-mile retreat to Boston, inflicting over 250 British casualties.",
                "say_something_q": "Why did the British march to Concord fail, and how did colonial militiamen turn the British return to Boston into a costly retreat?",
                "cloze_stmt": "After a battle at Concord's _________________________, colonial militiamen fired from behind trees and stone walls as the British retreated to Boston, causing over 250 British casualties.",
                "citation": '[pp. 198–199, ¶4–6]',
            },
        ],
        "perspectives": {
            "side_a_label": "Captain John Parker & Colonial Minutemen",
            "side_a_point": "Stood their ground to defend their towns and used guerrilla tactics—firing from behind trees, fences, and stone walls—to drive the British back to Boston [pp. 198–199].",
            "side_b_label": "British Redcoats Marching from Concord",
            "side_b_point": "Expected poorly trained militia to scatter, but found most weapons hidden and suffered heavy losses on the 16-mile retreat to Boston [p. 199].",
        },
        "reading_check_a": "At Lexington, 8 Minutemen were killed when gunfire erupted on the town green; at Concord, militiamen fought back at the North Bridge and ambushed the British column all the way back to Boston [pp. 198–199].",
        "skill_q2_a": "Ralph Waldo Emerson called it the 'shot heard round the world' because the battle at Lexington and Concord launched the American Revolution and inspired democratic movements worldwide [p. 198].",
        "word_meaning_q3_a": "A 'retreat' is a military withdrawal away from enemy forces, as the British troops were forced to do from Concord back to Boston [p. 199].",
        "critical_viewing_a": "The battle painting shows Minutemen and British regulars exchanging fire at close range, marking the point of no return between Britain and the colonies [pp. 198–199].",
    },
    "3.4": {
        "printed_main_idea": "Concord's Old North Bridge stands preserved today at Minute Man National Historical Park to commemorate the spot where colonial militia first fired back at British soldiers.",
        "exemplar_central_idea": "Preserved within Minute Man National Historical Park, Concord's North Bridge and the Minute Man statue honor the April 19, 1775 battle where colonists were ordered for the first time to fire upon British troops.",
        "scaffolded_central_idea_stem": "At Concord's _________________________, preserved today in Minute Man National Historical Park, colonial officers first ordered militiamen to return fire against British soldiers.",
        "word_bank": ["North Bridge", "Concord", "Minute Man statue", "Ralph Waldo Emerson"],
        "subheadings": [
            {
                "name": "AMERICAN PLACES: NORTH BRIDGE (pp. 200–201)",
                "gist": "Concord's North Bridge and Daniel Chester French's Minute Man statue memorialize the April 19, 1775 clash where militia pushed back British soldiers.",
                "cause": "At the North Bridge on April 19, 1775, Major John Buttrick ordered colonial militiamen, 'Fire, fellow soldiers, for God's sake, fire!'",
                "effect": "The battle became a symbol of American resistance and is memorialized today by the reconstructed bridge and the **Minute Man statue** inscribed with Ralph Waldo Emerson's poem.",
                "say_something_q": "Why is the fight at Concord's North Bridge considered a historic turning point compared to Lexington earlier that morning?",
                "cloze_stmt": "Unlike at Lexington, at Concord's _________________________ colonial officers deliberately ordered militiamen to fire back at British troops.",
                "citation": '[pp. 200–201, ¶1–3]',
            },
        ],
        "perspectives": {
            "side_a_label": "Lexington Green (Dawn, April 19, 1775)",
            "side_a_point": "Outnumbered Minutemen were ordered not to fire unless fired upon and suffered 8 deaths in a brief skirmish [p. 198, p. 200].",
            "side_b_label": "Concord's North Bridge (Later That Morning)",
            "side_b_point": "Hundreds of organized militiamen returned fire under direct orders and forced British regulars to retreat [pp. 200–201].",
        },
        "reading_check_a": "North Bridge is the site where colonial militia first fought back under orders and forced British soldiers to retreat on April 19, 1775 [pp. 200–201].",
        "skill_q2_a": "Monuments like the Minute Man statue and preserved battlefields help future generations understand the physical geography and sacrifices of 1775 [pp. 200–201].",
        "word_meaning_q3_a": "Commemorate means to honor and preserve the memory of an important historical event or person [p. 200].",
        "critical_viewing_a": "The photograph of North Bridge and the Minute Man statue shows a citizen-farmer leaving his plow with musket in hand to defend his community [pp. 200–201].",
    },
    "4.1": {
        "printed_main_idea": "In 1775, the Second Continental Congress formed the Continental Army under George Washington while Patriots captured Fort Ticonderoga and fought fiercely at Bunker Hill.",
        "exemplar_central_idea": "Meeting in May 1775, the Second Continental Congress sent the Olive Branch Petition as a final peace effort while appointing George Washington to lead the new Continental Army, even as Patriots seized cannons at Fort Ticonderoga and proved their resolve at the Battle of Bunker Hill.",
        "scaffolded_central_idea_stem": "In 1775, the Second Continental Congress sent the _________________________ to seek peace while naming _________________________ to command the Continental Army, and Patriots proved they could fight the British at the Battle of _________________________.",
        "word_bank": ["Second Continental Congress", "Continental Army", "George Washington", "Olive Branch Petition", "Fort Ticonderoga", "Bunker Hill"],
        "subheadings": [
            {
                "name": "SECOND CONTINENTAL CONGRESS AND TICONDEROGA (p. 202)",
                "gist": "In May 1775, the Second Continental Congress created the Continental Army under George Washington and sent the Olive Branch Petition, while Ethan Allen and Benedict Arnold captured Fort Ticonderoga.",
                "cause": "After Lexington and Concord, the **Second Continental Congress** met in Philadelphia in May 1775, while **Ethan Allen**'s Green Mountain Boys and **Benedict Arnold** attacked **Fort Ticonderoga**.",
                "effect": "Congress formed the **Continental Army** under **George Washington** and sent the **Olive Branch Petition** to King George III, while Patriots captured heavy British cannons at Ticonderoga.",
                "say_something_q": "How did the Second Continental Congress prepare for war while still trying to make peace in 1775?",
                "cloze_stmt": "The Second Continental Congress appointed _________________________ to lead the Continental Army and sent the _________________________ Petition for peace, while Ethan Allen captured cannons at Fort _________________________.",
                "citation": '[p. 202, ¶1–4]',
            },
            {
                "name": "THE BATTLE OF BUNKER HILL (p. 203)",
                "gist": "In June 1775, colonial militia on Breed's Hill repelled two British assaults before running out of ammunition at the Battle of Bunker Hill, proving Patriots could stand up to the British army.",
                "cause": "In June 1775, colonial militia fortified **Breed's Hill** (near **Bunker Hill**) overlooking Boston, and British troops charged uphill three times.",
                "effect": "Short on gunpowder ('Don't fire until you see the whites of their eyes'), colonists retreated on the third charge, but inflicted over 1,000 British casualties and King George rejected the Olive Branch Petition.",
                "say_something_q": "Why did Patriots consider the Battle of Bunker Hill a moral victory even though the British ultimately took the hill?",
                "cloze_stmt": "At the Battle of _________________________ (fought on Breed's Hill), colonial militia held off two British charges and inflicted over 1,000 British casualties before running low on gunpowder.",
                "citation": '[p. 203, ¶1–4]',
            },
        ],
        "perspectives": {
            "side_a_label": "War Preparations (Continental Army, Ticonderoga, Bunker Hill)",
            "side_a_point": "Appointed George Washington commander, seized artillery at Fort Ticonderoga, and fought British regulars on Breed's Hill [pp. 202–203].",
            "side_b_label": "Peace Effort (The Olive Branch Petition)",
            "side_b_point": "Pledged loyalty to King George III and asked him to protect colonial rights peacefully—which the king refused to read, declaring the colonies in open rebellion [pp. 202–203].",
        },
        "reading_check_a": "The Second Continental Congress created the Continental Army, appointed George Washington as its commander, authorized printing paper money, and sent the Olive Branch Petition to King George III [p. 202].",
        "skill_q2_a": "Capturing Fort Ticonderoga gave the Patriots heavy cannons they badly needed, and the Battle of Bunker Hill proved colonial militia could stand up to professional British troops [pp. 202–203].",
        "word_meaning_q3_a": "An 'olive branch' is an ancient symbol of peace; the Olive Branch Petition was the colonists' final peaceful attempt to avoid full-scale war with Britain [p. 202].",
        "critical_viewing_a": "The painting of the Battle of Bunker Hill shows colonial militiamen firing down from earthen fortifications on Breed's Hill against advancing rows of British Redcoats [p. 203].",
    },
    "4.2": {
        "printed_main_idea": "Glacial hills and peninsulas around Boston Harbor gave colonial forces critical high-ground advantages during the siege of Boston.",
        "exemplar_central_idea": "Shaped by ancient glaciers, the steep hills called drumlins surrounding Boston—such as Breed's Hill, Bunker Hill, and Dorchester Heights—gave whoever controlled the high ground command over Boston Harbor.",
        "scaffolded_central_idea_stem": "Steep glacial hills called _________________________, including Breed's Hill and Dorchester Heights, gave colonial forces a military advantage by overlooking _________________________.",
        "word_bank": ["drumlins", "glaciers", "Breed's Hill", "Bunker Hill", "Dorchester Heights", "high ground"],
        "subheadings": [
            {
                "name": "GEOLOGY IN HISTORY: HOW GEOLOGY SHAPES THE BATTLEFIELD (pp. 204–205)",
                "gist": "Glaciers formed steep hills called drumlins around Boston Harbor, making Breed's Hill, Bunker Hill, and Dorchester Heights strategic military positions.",
                "cause": "Ice Age glaciers left behind steep, elongated hills called **drumlins** on the Charlestown and Dorchester peninsulas overlooking Boston Harbor.",
                "effect": "Controlling this high ground allowed militiamen on Breed's Hill to fire down on advancing British troops and later allowed cannons on **Dorchester Heights** to threaten the British fleet.",
                "say_something_q": "How did glacial hills (drumlins) around Boston affect the outcome of military clashes in 1775 and 1776?",
                "cloze_stmt": "Steep hills formed by glaciers, known as _________________________, gave soldiers on Breed's Hill and Dorchester Heights a commanding view over Boston Harbor.",
                "citation": '[pp. 204–205, ¶1–3]',
            },
        ],
        "perspectives": {
            "side_a_label": "Defenders on the High Ground (Patriots)",
            "side_a_point": "Could see enemy movements across the harbor and fire down from behind fortifications while enemy soldiers struggled up steep slopes [pp. 204–205].",
            "side_b_label": "Attackers at Water Level (British Troops & Fleet)",
            "side_b_point": "Faced exhausting uphill marches carrying heavy gear at Bunker Hill and were vulnerable to cannon fire from Dorchester Heights [pp. 204–205].",
        },
        "reading_check_a": "Drumlins—steep hills formed by glaciers—created natural high ground around Boston Harbor that gave defenders a major tactical advantage [pp. 204–205].",
        "skill_q2_a": "Boston's narrow neck and surrounding peninsulas allowed the Continental Army to bottle up British forces inside the city and control the harbor from the hills [pp. 204–205].",
        "word_meaning_q3_a": "A 'drumlin' is an elongated, steep-sided hill formed by glacial drift [p. 204].",
        "critical_viewing_a": "The 3D terrain map of Boston Harbor clearly shows how Charlestown (Bunker/Breed's Hill) and Dorchester Heights tower directly above the harbor and city [pp. 204–205].",
    },
    "4.3": {
        "printed_main_idea": "Washington's capture of Boston and Thomas Paine's pamphlet Common Sense convinced many colonists that it was time to declare independence from Great Britain.",
        "exemplar_central_idea": "In early 1776, George Washington forced the British to evacuate Boston by placing Fort Ticonderoga's cannons on Dorchester Heights, while Thomas Paine's bestselling pamphlet Common Sense persuaded thousands of colonists to support complete independence.",
        "scaffolded_central_idea_stem": "In early 1776, George Washington forced the British out of Boston using cannons from _________________________, while _________________________'s pamphlet *Common Sense* convinced colonists to declare independence.",
        "word_bank": ["Henry Knox", "Fort Ticonderoga", "Dorchester Heights", "Thomas Paine", "Common Sense", "Loyalists"],
        "subheadings": [
            {
                "name": "THE BRITISH EVACUATE BOSTON (p. 206)",
                "gist": "Colonel Henry Knox hauled 59 cannons 300 miles from Fort Ticonderoga to Boston, allowing Washington to fortify Dorchester Heights and force the British to evacuate in March 1776.",
                "cause": "Colonel **Henry Knox** dragged 59 heavy cannons 300 miles over snow and ice from **Fort Ticonderoga**, and Washington placed them on **Dorchester Heights** overlooking Boston.",
                "effect": "Realizing the cannons could destroy his ships, British General William Howe evacuated 9,000 British soldiers and 1,000 **Loyalists** from Boston to Canada in March 1776.",
                "say_something_q": "How did Henry Knox and George Washington force the British army to evacuate Boston in March 1776 without a major battle?",
                "cloze_stmt": "After Colonel _________________________ hauled cannons 300 miles from Fort Ticonderoga, Washington placed them on _________________________, forcing the British to evacuate Boston in March 1776.",
                "citation": '[p. 206, ¶1–3]',
            },
            {
                "name": "THOMAS PAINE'S COMMON SENSE (pp. 206–207)",
                "gist": "In January 1776, Thomas Paine published Common Sense in plain language, attacking monarchy and convincing thousands of undecided colonists to support independence.",
                "cause": "In January 1776, **Thomas Paine** published a 47-page pamphlet titled ***Common Sense***, written in plain, powerful language for ordinary readers.",
                "effect": "*Common Sense* sold some 500,000 copies, condemned rule by kings as tyranny, and persuaded undecided colonists and Congress delegates that it was time to part with Britain.",
                "say_something_q": "Why was Thomas Paine's pamphlet *Common Sense* so persuasive to ordinary colonists in 1776?",
                "cloze_stmt": "In January 1776, _________________________ published the pamphlet _________________________, arguing in plain language that colonists should break away from British monarchy.",
                "citation": '[pp. 206–207, ¶4–6]',
            },
        ],
        "perspectives": {
            "side_a_label": "Thomas Paine (*Common Sense*, January 1776)",
            "side_a_point": "Argued in plain language that hereditary monarchy was corrupt, an island should not rule a continent, and America should form an independent republic [pp. 206–207].",
            "side_b_label": "Loyalists (Colonists Loyal to King George III)",
            "side_b_point": "Remained loyal to the British Crown, feared chaos without British protection, and fled Boston with General Howe's troops in March 1776 [p. 206].",
        },
        "reading_check_a": "Henry Knox hauled cannons from Fort Ticonderoga to Boston, and Washington positioned them on Dorchester Heights, forcing the British fleet and army to evacuate Boston in March 1776 [p. 206].",
        "skill_q2_a": "Unlike legalistic pamphlets written for educated elites, Thomas Paine wrote *Common Sense* in direct, everyday language that ordinary farmers and workers could read and understand [pp. 206–207].",
        "word_meaning_q3_a": "'Loyalists' were American colonists who remained loyal to King George III and opposed independence from Great Britain [p. 206].",
        "critical_viewing_a": "The portrait of Thomas Paine and title page of *Common Sense* highlight how the printed word mobilized public opinion across all 13 colonies [p. 207].",
    },
    "4.4": {
        "printed_main_idea": "On July 4, 1776, the Continental Congress adopted the Declaration of Independence, written primarily by Thomas Jefferson.",
        "exemplar_central_idea": "Drafted by Thomas Jefferson and adopted by the Continental Congress on July 4, 1776, the Declaration of Independence proclaimed that all people have unalienable rights to life, liberty, and the pursuit of happiness and listed colonial grievances against King George III to justify forming a free nation.",
        "scaffolded_central_idea_stem": "Written primarily by _________________________ and adopted on _________________________, the Declaration of Independence stated that government must protect _________________________ rights and listed grievances against King George III.",
        "word_bank": ["Thomas Jefferson", "July 4, 1776", "Declaration of Independence", "unalienable rights", "Richard Henry Lee", "consent of the governed"],
        "subheadings": [
            {
                "name": "MOVING TOWARD INDEPENDENCE (p. 208)",
                "gist": "In June 1776, Richard Henry Lee proposed independence, and Congress appointed a committee led by Thomas Jefferson to draft the formal declaration.",
                "cause": "In June 1776, Virginia delegate **Richard Henry Lee** introduced a resolution declaring that the colonies 'are, and of right ought to be, free and independent States.'",
                "effect": "Congress appointed a five-member committee—including John Adams, Benjamin Franklin, and **Thomas Jefferson**—and chose Jefferson to write the **Declaration of Independence**.",
                "say_something_q": "What did Richard Henry Lee propose in June 1776, and who was chosen to write the draft of the Declaration of Independence?",
                "cloze_stmt": "After _________________________ proposed that the colonies be free and independent states, Congress chose _________________________ to write the Declaration of Independence.",
                "citation": '[p. 208, ¶1–3]',
            },
            {
                "name": "IDEALS AND ADOPTION OF THE DECLARATION (pp. 208–209)",
                "gist": "Adopted on July 4, 1776, the Declaration asserted unalienable rights and consent of the governed, listed grievances against King George III, and declared the United States independent.",
                "cause": "Drawing on John Locke, Jefferson wrote that all people have **unalienable rights** (life, liberty, and the pursuit of happiness) and listed specific grievances against King George III.",
                "effect": "On **July 4, 1776**, Congress approved the Declaration of Independence, turning the colonial protest into a war to establish an independent nation—though women, Native Americans, and enslaved African Americans were initially left out of its promises.",
                "say_something_q": "What are the main sections of the Declaration of Independence, and why was signing it dangerous for the delegates?",
                "cloze_stmt": "Approved on _________________________, the Declaration proclaimed that people have _________________________ rights (life, liberty, and the pursuit of happiness) and that governments derive power from the consent of the governed.",
                "citation": '[pp. 208–209, ¶4–7]',
            },
        ],
        "perspectives": {
            "side_a_label": "Preamble & Philosophy of Natural Rights",
            "side_a_point": "States that 'all men are created equal' with unalienable rights to life, liberty, and the pursuit of happiness, and that people may alter or abolish a government that destroys these rights [pp. 208–209].",
            "side_b_label": "List of Grievances Against King George III",
            "side_b_point": "Proves that King George III established 'an absolute Tyranny' over the colonies by imposing taxes without consent, quartering troops, and ignoring colonial petitions [p. 209].",
        },
        "reading_check_a": "The two main goals of the Declaration of Independence were to state the philosophical ideals of natural rights/consent of the governed and to list specific grievances against King George III justifying independence [pp. 208–209].",
        "skill_q2_a": "Signing the Declaration was considered treason against Great Britain; if the Patriots lost the war, every signer risked being hanged [p. 209].",
        "word_meaning_q3_a": "An 'unalienable right' is a fundamental natural right granted by the Creator that cannot be lawfully taken away by any government [p. 208].",
        "critical_viewing_a": "John Trumbull's painting 'Declaration of Independence' shows the drafting committee (Jefferson, Adams, Franklin, Sherman, Livingston) presenting the document to John Hancock and Congress [pp. 208–209].",
    },
    "4.5": {
        "printed_main_idea": "Primary source documents from the Revolutionary era reveal how diverse Americans—including enslaved people and women—appealed to the ideals of liberty and equality.",
        "exemplar_central_idea": "Comparing the Declaration of Independence with petitions by enslaved African Americans and letters like Abigail Adams's 'Remember the Ladies' shows that the ideals of 1776 immediately inspired excluded groups to demand freedom and equality.",
        "scaffolded_central_idea_stem": "Primary sources from the Revolutionary era show that the ideals of liberty in the _________________________ inspired enslaved African Americans and women like _________________________ to call for equal rights.",
        "word_bank": ["Declaration of Independence", "Abigail Adams", "natural rights", "petitions", "equality"],
        "subheadings": [
            {
                "name": "DOCUMENT-BASED QUESTION: DECLARATIONS OF FREEDOM (pp. 210–211)",
                "gist": "Historical documents from the 1770s show how Patriots, women, and enslaved African Americans used the language of natural rights to argue for freedom.",
                "cause": "The Declaration of Independence proclaimed universal ideals that 'all men are created equal' and possess unalienable rights to liberty.",
                "effect": "Enslaved African Americans petitioned colonial legislatures for emancipation and women like Abigail Adams urged leaders to 'Remember the Ladies' in the new code of laws.",
                "say_something_q": "How did excluded groups use the arguments of the Declaration of Independence to challenge inequality in the colonies?",
                "cloze_stmt": "Comparing primary sources shows that the language of _________________________ in the Declaration of Independence inspired abolitionist petitions and calls for women's rights.",
                "citation": '[pp. 210–211, Documents 1–4]',
            },
        ],
        "perspectives": {
            "side_a_label": "Continental Congress (1776 Declaration)",
            "side_a_point": "Focused on political independence from Great Britain while leaving colonial slavery and legal restrictions on women intact [pp. 210–211].",
            "side_b_label": "Freedom Petitioners & Abigail Adams",
            "side_b_point": "Pointed out the contradiction between demanding liberty from Britain while denying freedom and representation to enslaved people and women at home [pp. 210–211].",
        },
        "reading_check_a": "The primary sources share a central theme: that liberty and natural rights belong to all human beings and cannot justly be denied [pp. 210–211].",
        "skill_q2_a": "Both the Declaration and the freedom petitions argue that people have a natural right to freedom and that unjust power violates moral and natural law [pp. 210–211].",
        "word_meaning_q3_a": "A Document-Based Question (DBQ) requires analyzing multiple historical primary sources to build an evidence-based claim [p. 210].",
        "critical_viewing_a": "Analyzing the historical documents side-by-side reveals how the rhetoric of 1776 sparked ongoing movements for equality in American history [pp. 210–211].",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# DYNAMIC KNOWLEDGE FALLBACK FOR SECTIONS IN CHAPTERS 1–4 & 6–17
# ─────────────────────────────────────────────────────────────────────────────

def build_dynamic_section_knowledge(section_meta: Dict[str, Any], markdown_text: str) -> Dict[str, Any]:
    """
    Constructs a 100% passage-grounded knowledge object for any section outside Chapter 5
    directly from its extracted subheadings, paragraphs, printed Main Idea, and built-in questions.
    """
    sec_code = str(section_meta["section_code"])
    if section_meta["chapter_num"] == 5 and sec_code in CHAPTER_5_KNOWLEDGE_BASE:
        return CHAPTER_5_KNOWLEDGE_BASE[sec_code]

    printed_mi = section_meta.get("printed_main_idea") or (
        f"In Section {sec_code} ({section_meta['title']}), historical developments shaped the growth and conflicts of the nation."
    )
    vocab_list = [v["word"] for v in section_meta.get("official_vocab", [])][:6]

    # Parse subheadings and first paragraphs from markdown_text
    sh_blocks = re.findall(
        r"####\s+\d+\.\s+([^\n(]+)\s+\(p\.\s*(\d+)\)\n(.*?)(?=(?:\n####\s+\d+\.|\n---|\Z))",
        markdown_text or "",
        flags=re.DOTALL,
    )
    subheadings = []
    for sh_title, sh_pg, sh_body in sh_blocks[:3]:
        clean_title = sh_title.strip()
        paras = [
            re.sub(r"^\*\*\[¶\d+\]\*\*\s*", "", p.strip())
            for p in sh_body.strip().split("\n\n")
            if p.strip()
        ]
        first_sent = re.split(r"(?<=[.!?])\s+", paras[0])[0] if paras else clean_title
        second_sent = re.split(r"(?<=[.!?])\s+", paras[1])[0] if len(paras) > 1 else first_sent
        subheadings.append({
            "name": f"{clean_title} (p. {sh_pg})",
            "gist": first_sent,
            "cause": first_sent,
            "effect": second_sent,
            "say_something_q": f"What is the most important historical development explained under '{clean_title}' on page {sh_pg}?",
            "cloze_stmt": f"Under *{clean_title}* (p. {sh_pg}), the text explains that _________________________________________________________.",
            "citation": f'[p. {sh_pg}, "{clean_title}", ¶1–2]',
        })

    if not subheadings:
        subheadings = [
            {
                "name": f"{section_meta['title'].upper()} (pp. {section_meta['printed_pages']})",
                "gist": printed_mi,
                "cause": f"Key historical developments described on pages {section_meta['printed_pages']}.",
                "effect": printed_mi,
                "say_something_q": f"What is the central historical development explained on pages {section_meta['printed_pages']}?",
                "cloze_stmt": f"On pages {section_meta['printed_pages']}, the reading explains that _________________________________________________________.",
                "citation": f"[pp. {section_meta['printed_pages']}, ¶1–2]",
            }
        ]

    ht = section_meta.get("historical_thinking", {})
    return {
        "printed_main_idea": printed_mi,
        "exemplar_central_idea": f"{printed_mi} Specifically, {', '.join(s['name'] for s in subheadings[:2])} show how these events shaped this era.",
        "scaffolded_central_idea_stem": f"The central idea of Section {sec_code} is that _________________________________________________________, which mattered because _________________________________________________________.",
        "word_bank": vocab_list if vocab_list else ["Key Term 1", "Key Term 2", "Central Idea"],
        "subheadings": subheadings,
        "perspectives": {
            "side_a_label": f"Part 1: {subheadings[0]['name']}",
            "side_a_point": f"{subheadings[0]['gist']} {subheadings[0]['citation']}",
            "side_b_label": f"Part 2: {subheadings[-1]['name']}",
            "side_b_point": f"{subheadings[-1]['gist']} {subheadings[-1]['citation']}",
        },
        "reading_check_a": f"Verify student response cites explicit details from pp. {section_meta['printed_pages']} ({ht.get('q1_reading_check', 'Reading Check')}).",
        "skill_q2_a": f"Verify student response connects ideas across subheadings on pp. {section_meta['printed_pages']} ({ht.get('q2_skill', 'Historical Thinking')}).",
        "word_meaning_q3_a": f"Verify student defines the target term using context clues on pp. {section_meta['printed_pages']} ({ht.get('q3_word_meaning', 'Word Meaning')}).",
        "critical_viewing_a": f"Verify student references specific visual/map details on pp. {section_meta['printed_pages']}.",
    }


# ─────────────────────────────────────────────────────────────────────────────
# MODULAR COMPONENT RENDERERS (STANDARD + SCAFFOLDED + TEACHER KEY)
# ─────────────────────────────────────────────────────────────────────────────

def _render_vocab_component(
    section_meta: Dict[str, Any],
    kb: Dict[str, Any],
    vocab_mode: str,
    is_scaffolded: bool
) -> Tuple[str, List[str]]:
    """Renders the teacher's chosen Vocabulary block (or empty if embedded only or zero vocab)."""
    if vocab_mode in ("vocab_embedded_only", "vocab_none"):
        return "", []

    ht = section_meta.get("historical_thinking", {})
    if vocab_mode == "vocab_word_meaning_q3" and ht.get("q3_word_meaning"):
        q3_str = ht["q3_word_meaning"]
        lines = [
            f"**Context Vocabulary Check (p. {section_meta['end_page']}):** {q3_str}",
        ]
        if is_scaffolded:
            lines.append("*Sentence Starter: Based on the context of the sentence, this word means* ____________________________________.")
        else:
            lines.append(SOLID_LINE)
        return "\n".join(lines), [f"Context Vocab (#3): {kb['word_meaning_q3_a']}"]

    # Default: Compact Official Textbook Vocabulary Box (2-4 terms from R44-R58 & spread)
    vocab_items = section_meta.get("official_vocab", [])[:3]
    if not vocab_items:
        return "", []

    rows = [
        "**Part 1: Key Section Vocabulary in Context** — *Review each textbook definition and complete the quick check in the right column.*",
        "| Key Term & Page | Official Textbook Definition | How does this term connect to this section? (Brief Note) |",
        "| :--- | :--- | :--- |",
    ]
    key_list = []
    for v in vocab_items:
        w = v["word"]
        pg = v.get("page", section_meta["start_page"])
        defn = v.get("definition") or "Key historical term defined in the reading."
        if is_scaffolded:
            prompt_cell = f"*In this section, **{w}** is important because* ..............................."
        else:
            prompt_cell = "..........................................................................................."
        rows.append(f"| **{w}** (p. {pg}) | {defn} | {prompt_cell} |")
        key_list.append(f"**{w}** (p. {pg}): {defn} — Connected directly to events in Section {section_meta['section_code']}.")

    return "\n".join(rows), key_list


def _render_reading_organizer_component(
    section_meta: Dict[str, Any],
    kb: Dict[str, Any],
    read_code: str,
    reading_mode_code: str,
    is_scaffolded: bool,
    custom_prefix: str = "",
) -> Tuple[str, List[str]]:
    """Renders the active reading organizer for the section."""
    rm_obj = get_strategy_by_code(READING_MODES, reading_mode_code)
    prefix = custom_prefix.strip() if (reading_mode_code == "mode_custom_other" and custom_prefix.strip()) else rm_obj.get("directions_prefix", "As we read each subheading,")
    subs = kb["subheadings"]
    keys = []

    if read_code == "read_01_cause_effect":
        lines = [
            f"**Directions:** {prefix} complete the **Historical Cause & Effect** table using specific facts from pages {section_meta['printed_pages']}.",
            "| Historical Cause<br>What happened first? | Historical Effect<br>What happened as a result? |",
            "| :--- | :--- |",
        ]
        for idx, sh in enumerate(subs, start=1):
            if idx % 2 == 1:
                c_cell = f"**{idx}. {sh['name']}:** {sh['cause']}"
                if is_scaffolded:
                    e_cell = f"**Effect {idx}:** As a result, {sh['effect'][:28]} _____________________________<br>______________________________________________________."
                else:
                    e_cell = f"**Effect {idx}:** ______________________________________________________<br>______________________________________________________"
                keys.append(f"Row {idx} Effect ({sh['name']}): {sh['effect']} {sh['citation']}")
            else:
                if is_scaffolded:
                    c_cell = f"**{idx}. {sh['name']}:** Because {sh['cause'][:28]} _____________________________<br>______________________________________________________."
                else:
                    c_cell = f"**{idx}. {sh['name']}:** ______________________________________________________<br>______________________________________________________"
                e_cell = f"**Effect {idx}:** {sh['effect']}"
                keys.append(f"Row {idx} Cause ({sh['name']}): {sh['cause']} {sh['citation']}")
            lines.append(f"| {c_cell} | {e_cell} |")
        return "\n".join(lines), keys

    elif read_code == "read_04_sequence_timeline":
        lines = [
            f"**Directions:** {prefix} trace the **Chronological Sequence** of events across pages {section_meta['printed_pages']} in complete sentences.",
            "| Step & Subheading Locator | What Happened at This Stage? (Key Event & Outcome) |",
            "| :--- | :--- |",
        ]
        for idx, sh in enumerate(subs, start=1):
            if is_scaffolded:
                body_cell = f"*{sh['gist'][:36]}* ______________________________________________________<br>______________________________________________________."
            else:
                body_cell = "______________________________________________________________________<br>______________________________________________________________________"
            lines.append(f"| **Step {idx}: {sh['name']}** | {body_cell} |")
            keys.append(f"Step {idx} ({sh['name']}): {sh['gist']} {sh['citation']}")
        return "\n".join(lines), keys

    elif read_code == "read_05_compare_perspectives":
        persp = kb["perspectives"]
        lines = [
            f"**Directions:** {prefix} compare the two historical perspectives or developments in Section {section_meta['section_code']} (pp. {section_meta['printed_pages']}).",
            f"| Historical Perspective / Group | Core Position, Actions & Text Evidence (pp. {section_meta['printed_pages']}) |",
            "| :--- | :--- |",
        ]
        if is_scaffolded:
            c1 = f"*{persp['side_a_point'][:38]}* ______________________________________________________."
            c2 = f"*{persp['side_b_point'][:38]}* ______________________________________________________."
        else:
            c1 = "______________________________________________________________________<br>______________________________________________________________________"
            c2 = "______________________________________________________________________<br>______________________________________________________________________"
        lines.append(f"| **1. {persp['side_a_label']}** | {c1} |")
        lines.append(f"| **2. {persp['side_b_label']}** | {c2} |")
        keys.append(f"Perspective 1 ({persp['side_a_label']}): {persp['side_a_point']}")
        keys.append(f"Perspective 2 ({persp['side_b_label']}): {persp['side_b_point']}")
        return "\n".join(lines), keys

    elif read_code == "read_03_cloze_guided":
        lines = [
            f"**Directions:** {prefix} fill in the missing historical terms in each **Guided Cloze** statement from pages {section_meta['printed_pages']}.",
        ]
        if is_scaffolded and kb.get("word_bank"):
            lines.append(f"*Word Bank:* **{', '.join(kb['word_bank'])}**")
        for idx, sh in enumerate(subs, start=1):
            lines.append(f"**{idx}. {sh['name']}:** {sh['cloze_stmt']}")
            keys.append(f"Cloze {idx} ({sh['name']}): {sh['gist']} {sh['citation']}")
        return "\n".join(lines), keys

    else:  # read_02_say_something (Default Stop & Jot by Subheading)
        lines = [
            f"**Directions:** {prefix} pause after each subheading to **'Say Something!'** in 1 complete sentence answering the guiding question.",
        ]
        for idx, sh in enumerate(subs, start=1):
            lines.append(f"**{idx}. {sh['name']}** — *{sh['say_something_q']}*")
            if is_scaffolded:
                lines.append(f"*Sentence Starter: In this part of the reading, {sh['gist'][:32]}* _________________________________________.")
            else:
                lines.append(SOLID_LINE)
            keys.append(f"{idx}. {sh['name']}: {sh['gist']} {sh['citation']}")
        return "\n".join(lines), keys


def _render_central_idea_and_anti_copycat_component(
    section_meta: Dict[str, Any],
    kb: Dict[str, Any],
    ci_code: str,
    pmi_code: str,
    is_scaffolded: bool
) -> Tuple[str, List[str]]:
    """
    Renders the Central Idea Synthesis block combined with the selected Anti-Copycat Mode
    so students never copy the textbook's printed MAIN IDEA verbatim.
    """
    printed_mi = kb["printed_main_idea"]
    subs = kb["subheadings"]
    lines = []
    keys = []

    # 1. Anti-Copycat Framing Header
    if pmi_code == "pmi_01_prove_it":
        lines.extend([
            f"**Central Idea & Evidence Check ('Prove the Textbook's Main Idea'):**",
            "",
            f"> **Textbook Printed Main Idea (p. {section_meta['start_page']}):** *\"{printed_mi}\"*",
            "",
        ])
    elif pmi_code == "pmi_03_upgrade_it":
        lines.extend([
            f"**Central Idea Synthesis ('Upgrade the Textbook's Main Idea'):**",
            "",
            f"> **Textbook Basic Main Idea (p. {section_meta['start_page']}):** *\"{printed_mi}\"*",
            "",
        ])
    else:
        lines.extend([
            f"**Central Idea Synthesis (Section {section_meta['section_code']}: {section_meta['title']}):**",
            "",
        ])

    # 2. Render specific Central Idea template
    if ci_code == "ci_01_subheading_gist":
        lines.append("**Directions:** Write a brief 10-word gist for each subheading on the dotted lines, then combine them into a detailed Whole-Section Central Idea on the solid lines.")
        for idx, sh in enumerate(subs, start=1):
            lines.append(f"- **Gist for {sh['name']}:** {DOTTED_LINE}")
            keys.append(f"Subheading {idx} Gist ({sh['name']}): {sh['gist']} {sh['citation']}")
        if is_scaffolded:
            lines.append(f"**Whole-Section Central Idea:** *{kb['scaffolded_central_idea_stem']}*")
        else:
            lines.append("**Whole-Section Central Idea (1–2 complete sentences):**")
            lines.append(SOLID_LINE)
            lines.append(SOLID_LINE)
        keys.append(f"Whole-Section Central Idea Exemplar: {kb['exemplar_central_idea']}")

    elif ci_code == "ci_02_box_and_bullets":
        if pmi_code == "pmi_01_prove_it":
            box_prompt = f"**Textbook Main Idea to Prove:** *{printed_mi}*"
        elif is_scaffolded:
            box_prompt = f"**Central Idea Claim:** *{kb['scaffolded_central_idea_stem']}*"
        else:
            box_prompt = f"**Central Idea Claim (State the main historical point of pp. {section_meta['printed_pages']}):**<br>{SOLID_LINE}"

        lines.extend([
            "",
            "| BOX & BULLETS: CENTRAL IDEA + SUPPORTING TEXT EVIDENCE |",
            "| :--- |",
            f"| {box_prompt} |",
            "",
        ])
        for idx, sh in enumerate(subs, start=1):
            lines.append(f"- **Supporting Evidence {idx} from {sh['name']}:** {DOTTED_LINE}")
            keys.append(f"Bullet {idx} Evidence ({sh['name']}): {sh['gist']} {sh['citation']}")
        keys.insert(0, f"Box & Bullets Central Idea Exemplar: {kb['exemplar_central_idea']}")

    elif ci_code == "ci_04_cer_paragraph":
        lines.append(f"**Directions:** Write a 3-part **Claim–Evidence–Reasoning (CER)** response explaining the central idea of pages {section_meta['printed_pages']}.")
        if is_scaffolded:
            lines.append(f"- **CLAIM (Central Idea):** *{kb['scaffolded_central_idea_stem']}*")
            lines.append(f"- **EVIDENCE (Cite a specific law/event from p. {section_meta['start_page']} or p. {section_meta['end_page']}):** *For example, on page {section_meta['start_page']}, the text states that* _________________________________________________________.")
            lines.append("- **REASONING (Why it mattered):** *This evidence proves the central idea because* _________________________________________________________.")
        else:
            lines.append(f"- **CLAIM (State the Central Idea in 1 complete sentence):**\n{SOLID_LINE}")
            lines.append(f"- **EVIDENCE (Cite 1–2 specific facts or laws from pp. {section_meta['printed_pages']}):**\n{SOLID_LINE}")
            lines.append(f"- **REASONING (Explain how your evidence supports the Central Idea):**\n{SOLID_LINE}")
        keys.append(f"CER Claim Exemplar: {kb['exemplar_central_idea']}")
        keys.append(f"CER Evidence & Reasoning: {subs[0]['gist']} {subs[0]['citation']}; {subs[-1]['gist']} {subs[-1]['citation']}")

    else:  # ci_03_what_so_what (or Upgrade It synthesis)
        if pmi_code == "pmi_03_upgrade_it":
            lines.append(
                f"**Directions:** Upgrade the textbook's basic Main Idea above into 1–2 detailed sentences that name the specific laws, historical figures, and consequences from pages {section_meta['printed_pages']}."
            )
        else:
            lines.append(
                f"**Directions ('What Happened? + So What?'):** In 1–2 complete sentences, state the **Central Idea** of Section {section_meta['section_code']} by connecting *what happened* to *why it mattered historically*."
            )
        if is_scaffolded:
            if kb.get("word_bank"):
                lines.append(f"*Key Terms to Include:* **{', '.join(kb['word_bank'][:4])}**")
            lines.append(f"*{kb['scaffolded_central_idea_stem']}*")
        else:
            lines.append(SOLID_LINE)
            lines.append(SOLID_LINE)
        keys.append(f"Central Idea ('What + So What' / Upgraded Main Idea): {kb['exemplar_central_idea']}")

    return "\n".join(lines), keys


def _render_builtin_questions_and_optional_twr(
    section_meta: Dict[str, Any],
    kb: Dict[str, Any],
    blueprint: Dict[str, Any],
    rec_info: Dict[str, Any],
    is_scaffolded: bool
) -> Tuple[str, List[str]]:
    """Renders any toggled-on Textbook Historical Thinking / Critical Viewing questions or Optional TWR."""
    ht = section_meta.get("historical_thinking", {})
    cv = section_meta.get("critical_viewing", [])
    blocks = []
    keys = []

    if blueprint.get("include_reading_check_q1") and ht.get("q1_reading_check"):
        q1 = ht["q1_reading_check"]
        blocks.append(f"**Textbook Reading Check (p. {section_meta['end_page']}):** *{q1}*")
        if is_scaffolded:
            blocks.append(f"*Sentence Starter: {kb['reading_check_a'][:38]}* _________________________________________________________.")
        else:
            blocks.append(SOLID_LINE)
        keys.append(f"Textbook #1 Reading Check (p. {section_meta['end_page']}): {kb['reading_check_a']}")

    if blueprint.get("include_skill_q2") and ht.get("q2_skill"):
        q2 = ht["q2_skill"]
        blocks.append(f"**Historical Thinking Skill (p. {section_meta['end_page']}):** *{q2}*")
        blocks.append(SOLID_LINE)
        keys.append(f"Textbook #2 Skill Question (p. {section_meta['end_page']}): {kb['skill_q2_a']}")

    if rec_info.get("include_critical_viewing") and cv:
        blocks.append(f"**Critical Viewing — Map & Visual Analysis:** *{cv[0]}*")
        blocks.append(SOLID_LINE)
        keys.append(f"Critical Viewing Analysis: {kb['critical_viewing_a']}")

    twr_code = blueprint.get("optional_twr_strategy", "twr_none")
    if twr_code and twr_code != "twr_none":
        stem_base = f"In Section {section_meta['section_code']} ({section_meta['title']}), tensions grew between Britain and the colonies"
        if twr_code == "twr_because_but_so":
            blocks.extend([
                "**Optional Writing Extension (Because, But, So):** Complete each sentence using specific facts from the reading.",
                f"1. {stem_base} **because** _________________________________________________________________.",
                f"2. {stem_base}, **but** ____________________________________________________________________.",
                f"3. {stem_base}, **so** _____________________________________________________________________.",
            ])
            keys.append(f"Optional TWR (Because/But/So): Verify causal, contrasting, and consequent facts from pp. {section_meta['printed_pages']}.")
        elif twr_code == "twr_subordinating":
            blocks.extend([
                "**Optional Writing Extension (Subordinating Conjunctions):** Complete each complex sentence after the comma.",
                f"1. **Although** {kb['subheadings'][0]['gist'][:45].lower()}..., _________________________________________________________.",
                f"2. **When** {kb['subheadings'][-1]['gist'][:45].lower()}..., ___________________________________________________________.",
            ])
            keys.append(f"Optional TWR (Subordinating Conjunctions): {kb['exemplar_central_idea']}")

    return "\n\n".join(blocks), keys


def _format_grade_box_token(grade_box_mode: str, label_prefix: str = "Section Check") -> str:
    if grade_box_mode == "points_10":
        return f"[GRADE_BOX: {label_prefix}: ______ / 10 pts   Initials: ________]"
    elif grade_box_mode == "points_100":
        return f"[GRADE_BOX: {label_prefix}: ______ / 100 pts   Initials: ________]"
    elif grade_box_mode == "stamp_box":
        return f"[GRADE_BOX: {label_prefix} Complete   Teacher Stamp / Initials: ________]"
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# MAIN SECTION PACKET GENERATOR (1-PAGE OR 2-PAGE, STANDARD & SCAFFOLDED)
# ─────────────────────────────────────────────────────────────────────────────

def generate_section_packet(
    section_meta: Dict[str, Any],
    blueprint: Dict[str, Any],
    markdown_text: str = ""
) -> Dict[str, Any]:
    """
    Generates the complete Student Section Packet (both Standard and Scaffolded editions)
    and the Section Teacher Plan & Clipboard Answer Key (with exact [p. X, "SUBHEADING", ¶Y] citations)
    strictly following the teacher's custom Blueprint.
    """
    if not markdown_text and section_meta.get("md_file"):
        md_p = Path(section_meta["md_file"])
        if md_p.exists():
            markdown_text = md_p.read_text(encoding="utf-8")

    kb = build_dynamic_section_knowledge(section_meta, markdown_text)
    rec = recommend_section_strategies(section_meta, markdown_text, blueprint)

    ch_num = section_meta["chapter_num"]
    sec_code = str(section_meta["section_code"])
    sec_title = section_meta["title"]
    pp = section_meta["printed_pages"]
    pages_per_sec = int(blueprint.get("pages_per_section", 1))
    vocab_mode = blueprint.get("vocab_mode", "vocab_official_box")
    reading_mode = blueprint.get("reading_mode", "mode_mixed_flexible")
    grade_box_mode = blueprint.get("grade_box_mode", "stamp_box")

    def _assemble_edition(is_scaf: bool) -> Tuple[str, List[str], Dict[str, Any]]:
        ed_tag = " *(Scaffolded Support Edition)*" if is_scaf else ""
        header_line = f"## Section {sec_code}: {sec_title} (Textbook pp. {pp}){ed_tag}"

        v_md, v_keys = _render_vocab_component(section_meta, kb, vocab_mode, is_scaf)
        custom_pfx = blueprint.get("custom_reading_mode_text", "")
        r_md, r_keys = _render_reading_organizer_component(
            section_meta, kb, rec["reading_organizer_code"], reading_mode, is_scaf, custom_prefix=custom_pfx
        )
        c_md, c_keys = _render_central_idea_and_anti_copycat_component(
            section_meta, kb, rec["central_idea_code"], rec["printed_main_idea_mode_code"], is_scaf
        )
        q_md, q_keys = _render_builtin_questions_and_optional_twr(
            section_meta, kb, blueprint, rec, is_scaf
        )

        all_keys = v_keys + r_keys + c_keys + q_keys

        if pages_per_sec == 1:
            # 1-Page Compact Mode: Fit cleanly onto a single page
            blocks = [header_line]
            if v_md:
                blocks.append(v_md)
            blocks.append(r_md)
            blocks.append(c_md)
            if q_md:
                blocks.append(q_md)
            gb = _format_grade_box_token(grade_box_mode, f"Sec {sec_code}")
            if gb:
                blocks.append(gb)
            raw_md = "\n\n".join(b for b in blocks if b.strip())
            fitted_md, budget_info = enforce_page_budget_guardrail(sanitize_aesthetics(raw_md), target_pages=1)
            return fitted_md, all_keys, budget_info
        else:
            # 2-Page Front-and-Back Mode: Page 1 = Vocab + Active Reading Organizer; Page 2 = Central Idea + Built-In Questions
            p1_blocks = [f"{header_line} — Part 1: Active Reading"]
            if v_md:
                p1_blocks.append(v_md)
            p1_blocks.append(r_md)
            gb1 = _format_grade_box_token(grade_box_mode, f"Sec {sec_code} (Pt 1)")
            if gb1:
                p1_blocks.append(gb1)

            p2_blocks = [f"## Section {sec_code}: {sec_title} (pp. {pp}) — Part 2: Central Idea & Synthesis"]
            p2_blocks.append(c_md)
            if q_md:
                p2_blocks.append(q_md)
            gb2 = _format_grade_box_token(grade_box_mode, f"Sec {sec_code} (Pt 2)")
            if gb2:
                p2_blocks.append(gb2)

            p1_str, b1 = enforce_page_budget_guardrail(sanitize_aesthetics("\n\n".join(p1_blocks)), target_pages=1)
            p2_str, b2 = enforce_page_budget_guardrail(sanitize_aesthetics("\n\n".join(p2_blocks)), target_pages=1)
            combined_md = f"{p1_str}\n\n[PAGE_BREAK]\n\n{p2_str}"
            return combined_md, all_keys, {
                "target_pages": 2,
                "final_layout_units": round(b1["final_layout_units"] + b2["final_layout_units"], 1),
                "max_budget_units": 56,
                "was_auto_compacted": b1["was_auto_compacted"] or b2["was_auto_compacted"],
                "fits_cleanly": b1["fits_cleanly"] and b2["fits_cleanly"],
            }

    std_md, key_items, std_budget = _assemble_edition(is_scaf=False)
    scaf_md, _, scaf_budget = _assemble_edition(is_scaf=True)

    # Build Section Teacher Plan & Clipboard Answer Key
    rm_obj = get_strategy_by_code(READING_MODES, reading_mode)
    teacher_lines = [
        f"# Teacher Plan & Clipboard Key: Chp {ch_num:02d}, Sec. {sec_code} — {sec_title}",
        f"**Textbook Pages:** {pp}  |  **Class Period:** 40 Minutes ({pages_per_sec} Page{'s' if pages_per_sec > 1 else ''} in Packet)  |  **Reading Mode:** {rm_obj['short_name']}",
        "",
        "### Suggested 40-Minute Pacing & Facilitation Guide",
        "| Time | Classroom Routine | Facilitation & Grounding Focus |",
        "| :--- | :--- | :--- |",
        f"| **0–5 min** | **Preview & Official Vocab** | Preview section subheadings on pp. {pp} and key terms (*{', '.join(kb.get('word_bank', [])[:4])}*). |",
        f"| **5–25 min** | **Chunked Reading & Organizer** | **{rec['reading_organizer_short']}** ({rm_obj['short_name']}). Pause after each subheading so students complete the organizer using text evidence. |",
        f"| **25–35 min** | **Central Idea Synthesis** | **{rec['central_idea_short']}** + *{rec['printed_main_idea_mode_short']}*. Ensure students cite details rather than copying the p. {section_meta['start_page']} Main Idea box verbatim. |",
        f"| **35–40 min** | **Check & Stamp / Tracker** | Circulate with the Clipboard Key below; students log their 1-sentence Central Idea on the Chapter Cover Study Guide Tracker. |",
        "",
        "---",
        f"## Clipboard Answer Key & Exact Paragraph Locators (Section {sec_code}: pp. {pp})",
        f"- **Textbook Printed Main Idea (p. {section_meta['start_page']}):** *\"{kb['printed_main_idea']}\"*",
        f"- **Exemplar Whole-Section Central Idea:** **{kb['exemplar_central_idea']}**",
        f"- **Scaffolded Stem Key:** *{kb['scaffolded_central_idea_stem']}*",
        "",
        "### Item-by-Item Key & Textbook Paragraph Citations",
    ]
    for k_item in key_items:
        teacher_lines.append(f"- {k_item}")

    teacher_md = sanitize_aesthetics("\n".join(teacher_lines))

    return {
        "section_id": section_meta["id"],
        "chapter_num": ch_num,
        "chapter_title": section_meta["chapter_title"],
        "section_code": sec_code,
        "section_title": sec_title,
        "printed_pages": pp,
        "pages_per_section": pages_per_sec,
        "recommendations": rec,
        "page_budget": std_budget,
        "student_standard_md": std_md,
        "student_scaffolded_md": scaf_md,
        "teacher_key_md": teacher_md,
        "clipboard_entry": {
            "section_code": sec_code,
            "section_title": sec_title,
            "printed_pages": pp,
            "reading_organizer_short": rec["reading_organizer_short"],
            "central_idea_short": rec["central_idea_short"],
            "anti_copycat_short": rec["printed_main_idea_mode_short"],
            "printed_main_idea": kb["printed_main_idea"],
            "exemplar_central_idea": kb["exemplar_central_idea"],
            "key_items": key_items,
            "vocab_words": [v["word"] for v in section_meta.get("official_vocab", [])[:4]],
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER-LEVEL STUDENT BOOKLET, COVER TRACKER & MASTER CLIPBOARD KEY BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def build_chapter_student_booklet(
    chapter_num: int,
    chapter_title: str,
    section_packets: List[Dict[str, Any]],
    blueprint: Dict[str, Any],
    edition: str = "standard"
) -> str:
    """
    Compiles the complete Chapter Student Packet Booklet (either 'standard' or 'scaffolded' edition):
      - Configurable Front Cover Page:
          * 'central_idea_tracker': Chapter Essential Question + 1-row-per-section Central Idea Study Guide Tracker
          * 'score_checklist': Section Completion & Score/Stamp Summary Table
          * 'none': Starts directly with the first selected section
      - Auto-aligned [PAGE_BREAK] dividers between every page so double-sided printing is 100% clean.
    """
    ch_std = CHAPTER_STANDARDS_MAP.get(str(chapter_num), CHAPTER_STANDARDS_MAP["5"])
    eq = ch_std.get("essential_question", "What key historical developments shaped this era?")
    cover_mode = blueprint.get("cover_page_mode", "central_idea_tracker")
    is_scaf = (edition == "scaffolded")
    ed_badge = " (Scaffolded Support Edition)" if is_scaf else ""

    all_blocks: List[str] = []

    if cover_mode != "none" and section_packets:
        cover_lines = [
            f"# Chapter {chapter_num}: {chapter_title} — Student Packet{ed_badge}",
            f"**Chapter Essential Question:** *{eq}*",
        ]
        if cover_mode == "central_idea_tracker":
            cover_lines.extend([
                "**Chapter Central Idea Study Guide Tracker:** After completing each section in this packet, write your **1-sentence Central Idea takeaway** in the table below. By the end of the chapter, this cover page becomes your complete study guide!",
                "[CENTER_HEADING: Chapter Central Idea Study Guide & Section Tracker]",
                "| Section & Pages | My 1-Sentence Central Idea Takeaway (Study Guide Log) | Teacher Stamp / Score |",
                "| :--- | :--- | :--- |",
            ])
            for pkt in section_packets:
                sc = pkt["section_code"]
                stitle = pkt["section_title"]
                pp = pkt["printed_pages"]
                cover_lines.append(
                    f"| **Sec. {sc}:** {stitle}<br>*(pp. {pp})* | ________________________________________________________________<br>________________________________________________________________ | __________ |"
                )
        else:
            cover_lines.extend([
                "**Packet Instructions:** Complete each section as we read together in class and record your scores or stamps below.",
                "[CENTER_HEADING: Chapter Section Completion & Score Table]",
                "| Section | Section Title & Textbook Pages | Active Reading & Central Idea | Score / Stamp |",
                "| :--- | :--- | :--- | :--- |",
            ])
            for pkt in section_packets:
                sc = pkt["section_code"]
                stitle = pkt["section_title"]
                pp = pkt["printed_pages"]
                rec = pkt["recommendations"]
                cover_lines.append(
                    f"| **Sec. {sc}** | {stitle} (pp. {pp}) | {rec['reading_organizer_short']} + {rec['central_idea_short']} | __________ |"
                )

        all_blocks.append("\n".join(cover_lines).strip())

    for pkt in section_packets:
        md_key = "student_scaffolded_md" if is_scaf else "student_standard_md"
        all_blocks.append(pkt[md_key].strip())

    return "\n\n[PAGE_BREAK]\n\n".join(all_blocks)


def build_chapter_master_teacher_plan(
    chapter_num: int,
    chapter_title: str,
    section_packets: List[Dict[str, Any]],
    blueprint: Dict[str, Any]
) -> str:
    """
    Compiles the Chapter Master Teacher Plan & All-in-One Clipboard Answer Key:
      1. Compact Standards Alignment Table (OSPI 8th Grade Social Studies + Supporting ELA Central Idea Standards)
      2. Chapter Pacing & Strategy Matrix across all teacher-selected sections
      3. All-in-One Clipboard Answer Key with exemplar Central Ideas and exact [p. XXX, "SUBHEADING", ¶Y] citations
    """
    ch_std = CHAPTER_STANDARDS_MAP.get(str(chapter_num), CHAPTER_STANDARDS_MAP["5"])
    eq = ch_std.get("essential_question", "")
    pages_per_sec = blueprint.get("pages_per_section", 1)
    total_student_pages = len(section_packets) * pages_per_sec + (1 if blueprint.get("cover_page_mode") != "none" else 0)

    lines = [
        f"# Master Teacher Plan & Clipboard Answer Key: Chapter {chapter_num:02d} — {chapter_title}",
        f"**Essential Question:** *{eq}*  |  **Selected Sections:** {len(section_packets)}  |  **Student Booklet Length:** {total_student_pages} Pages ({(total_student_pages + 1) // 2} Sheets Double-Sided)",
        "",
        "### Chapter Standards Alignment (OSPI Social Studies & Supporting ELA Central Idea)",
        "| Standard Category | Aligned Standards |",
        "| :--- | :--- |",
        f"| **OSPI 8th Grade Social Studies** | {'<br>'.join(ch_std.get('ospi_standards', []))} |",
        f"| **Supporting ELA (Central Idea & Literacy)** | {'<br>'.join(ch_std.get('ela_support_standards', []))} |",
        "",
        "### Chapter Section Scope & Strategy Matrix (40-Minute Daily Pacing)",
        "| Section & Pages | Official Vocab | Active Reading Organizer | Central Idea Template | Anti-Copycat Mode |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for pkt in section_packets:
        ce = pkt["clipboard_entry"]
        v_str = ", ".join(ce["vocab_words"]) if ce["vocab_words"] else "Embedded in reading"
        lines.append(
            f"| **Sec. {ce['section_code']}:** {ce['section_title']} (pp. {ce['printed_pages']}) | *{v_str}* | {ce['reading_organizer_short']} | {ce['central_idea_short']} | {ce['anti_copycat_short']} |"
        )

    lines.extend([
        "",
        "[PAGE_BREAK]",
        "",
        "# All-in-One Teacher Clipboard Answer Key (With Exact Page & Paragraph Citations)",
        "**How to Use During Your 40-Minute Class:** Carry this single condensed guide on your clipboard while students read and work. Every answer includes the exact **[Page #, Subheading, Paragraph ¶]** locator so you can immediately point any stuck student to the exact paragraph in the textbook.",
        "",
    ])

    for pkt in section_packets:
        ce = pkt["clipboard_entry"]
        lines.append(f"## Sec. {ce['section_code']}: {ce['section_title']} (Textbook pp. {ce['printed_pages']})")
        lines.append(f"- **Printed Textbook Main Idea (p. {ce['printed_pages'].split('–')[0]}):** *\"{ce['printed_main_idea']}\"*")
        lines.append(f"- **Exemplar Central Idea Takeaway:** **{ce['exemplar_central_idea']}**")
        for item in ce["key_items"]:
            lines.append(f"  - {item}")
        lines.append("")

    return sanitize_aesthetics("\n".join(lines))


# ─────────────────────────────────────────────────────────────────────────────
# END-OF-CHAPTER CENTRAL IDEA REVIEW & ASSESSMENT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def build_chapter_review_and_assessment(
    chapter_num: int,
    chapter_title: str,
    section_packets: List[Dict[str, Any]],
    chapter_review_data: Optional[Dict[str, Any]] = None
) -> Dict[str, str]:
    """
    Generates an End-of-Chapter Central Idea Review & Assessment (Standard Test,
    Scaffolded Test with Word Bank & Sentence Stems, and Teacher Answer Key) built
    directly from the sections the teacher selected for the chapter packet plus the
    official textbook Chapter Review (pp. 212–213).
    """
    ch_std = CHAPTER_STANDARDS_MAP.get(str(chapter_num), CHAPTER_STANDARDS_MAP["5"])
    eq = ch_std.get("essential_question", "")

    all_vocab = []
    seen_v = set()
    for pkt in section_packets:
        for w in pkt["clipboard_entry"]["vocab_words"]:
            if w.lower() not in seen_v:
                all_vocab.append(w)
                seen_v.add(w.lower())

    def _build_test_md(is_scaf: bool) -> str:
        badge = " *(Scaffolded Edition)*" if is_scaf else ""
        t_lines = [
            f"# Chapter {chapter_num}: {chapter_title} — Central Idea Review & Assessment{badge}",
            f"**Chapter Essential Question:** *{eq}*",
            "",
            "### Part 1: Key Historical Vocabulary in Context",
            "**Directions:** Complete each historical statement using the correct vocabulary term from this chapter.",
        ]
        if is_scaf or all_vocab:
            t_lines.append(f"**Word Bank:** *{', '.join(all_vocab[:8] if all_vocab else ['militia', 'revenue', 'tyranny', 'boycott', 'unalienable rights', 'Loyalists'])}*")
        t_lines.append("")

        for idx, pkt in enumerate(section_packets[:5], start=1):
            ce = pkt["clipboard_entry"]
            target_w = ce["vocab_words"][0] if ce["vocab_words"] else "key concept"
            t_lines.append(
                f"{idx}. In Section {ce['section_code']} (*{ce['section_title']}*, pp. {ce['printed_pages']}), the term **_________________________** was important because:"
            )
            if is_scaf:
                t_lines.append(f"*Hint: Think about {ce['printed_main_idea'][:55]}...*")
            t_lines.append(SOLID_LINE)

        t_lines.extend([
            "",
            "### Part 2: Section Central Ideas & Supporting Evidence",
            "**Directions:** For each section we studied in our packet, state the **Central Idea** and cite 1 supporting historical fact.",
            "| Section Studied | Central Idea & Supporting Historical Detail |",
            "| :--- | :--- |",
        ])
        for pkt in section_packets[:6]:
            ce = pkt["clipboard_entry"]
            if is_scaf:
                cell_p = f"<b>Central Idea:</b> <i>{ce['exemplar_central_idea'][:42]}...</i><br><b>Supporting Historical Detail:</b> ____________________________________"
            else:
                cell_p = "<b>1. Central Idea:</b> ____________________________________<br><b>2. Supporting Historical Detail:</b> ____________________________________"
            t_lines.append(f"| **Sec. {ce['section_code']}:** {ce['section_title']} *(pp. {ce['printed_pages']})* | {cell_p} |")

        t_lines.extend([
            "",
            "### Part 3: Chapter Essential Question & Historical Thinking Synthesis",
            f"**Synthesis Prompt:** *{eq}* Answer in a 3-sentence **Claim–Evidence–Reasoning (CER)** paragraph connecting at least **two sections** from your Chapter {chapter_num} packet.",
        ])
        if is_scaf:
            t_lines.extend([
                "- **CLAIM (Answer the Essential Question):** *British policies after 1763 led the colonies to declare independence because* _________________________________________________________.",
                "- **EVIDENCE (Cite 2 specific laws or events from our packet):** *First, in Section ____, Britain passed _________________________. Second, in Section ____, _________________________.*",
                "- **REASONING (Explain why this led to 1776):** *These events convinced colonists that* _________________________________________________________.",
            ])
        else:
            t_lines.extend([SOLID_LINE, SOLID_LINE, SOLID_LINE, SOLID_LINE])

        return sanitize_aesthetics("\n".join(t_lines))

    key_lines = [
        f"# Teacher Answer Key: Chapter {chapter_num} Central Idea Review & Assessment",
        f"**Essential Question:** *{eq}*",
        "",
        "### Part 1 & Part 2 Answer Key (By Active Section)",
    ]
    for pkt in section_packets:
        ce = pkt["clipboard_entry"]
        key_lines.append(
            f"- **Sec. {ce['section_code']} ({ce['section_title']}, pp. {ce['printed_pages']}):** "
            f"Vocab: *{', '.join(ce['vocab_words'])}* | **Central Idea:** {ce['exemplar_central_idea']}"
        )

    if chapter_review_data and chapter_review_data.get("questions"):
        key_lines.extend([
            "",
            f"### Official Textbook Chapter {chapter_num} Review Questions (pp. {chapter_review_data.get('printed_pages', '')})",
        ])
        for q in chapter_review_data["questions"][:10]:
            key_lines.append(f"- **Q{q['num']}:** {q['question']}")

    return {
        "standard_test_md": _build_test_md(is_scaf=False),
        "scaffolded_test_md": _build_test_md(is_scaf=True),
        "teacher_key_md": sanitize_aesthetics("\n".join(key_lines)),
    }
