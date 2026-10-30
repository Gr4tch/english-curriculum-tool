"""
Bilingual Localization Module (English & Spanish)
Provides translation dictionaries and helpers for student handouts and teacher answer keys.
Ensures that when the language toggle is set to 'Español', all student worksheet content
renders with authentic academic Spanish terminology.
"""

from typing import Dict, Any

STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        # Worksheet Header & Badges
        "section_badge": "Section {code}: {title} (pp. {pages})",
        "section_badge_short": "Sec. {code}",
        "scaffolded_edition_tag": " *(Scaffolded Support Edition)*",
        "strategy_focus_label": "Strategy Focus: {name}",
        "strategy_focus_prefix": "Strategy Focus:",

        # Student Metadata Line
        "directions_label": "Directions:",
        "name_label": "Name:",
        "date_label": "Date:",
        "period_label": "Per:",

        # Vocabulary Practice
        "vocab_practice_title": "Official Section Vocabulary Practice:",
        "vocab_directions_std": "Read each clue below. Using the section reading on pages {pages}, write the key vocabulary term that best matches each historical definition:",
        "vocab_directions_scaf": "Use the **Word Bank** above to complete each clue with the correct vocabulary term from pages {pages}:",
        "word_bank_label": "Word Bank:",
        "vocab_key_label": "Vocabulary Term {idx} ({word}):",

        # Reading Organizers
        "cause_effect_directions": "{prefix} complete the **Historical Cause & Effect** table using specific facts from pages {pages}.",
        "cause_header": "Historical Cause<br>What happened first?",
        "effect_header": "Historical Effect<br>What happened as a result?",
        "say_something_directions": "{prefix} pause after each subheading to **'Say Something!'** in 1 complete sentence answering the guiding question.",
        "say_something_starter": "Sentence Starter: In this part of the reading, {gist}",
        "cloze_directions": "{prefix} fill in the missing historical terms in each **Guided Cloze** statement from pages {pages}.",
        "sequence_directions": "{prefix} trace the **Chronological Sequence** of events across pages {pages} in complete sentences.",
        "sequence_header": "What Happened at This Stage? (Key Event & Outcome)",
        "perspectives_directions": "{prefix} compare the two historical perspectives or developments in Section {code} (pp. {pages}).",
        "perspectives_header": "Core Position, Actions & Text Evidence (pp. {pages})",

        # Central Idea Synthesis
        "subheading_gist_directions": "Write a brief 10-word gist for each subheading on the dotted lines, then combine them into a detailed Whole-Section Central Idea on the solid lines.",
        "gist_label": "Gist for {name}:",
        "whole_section_ci_label": "Whole-Section Central Idea (1–2 complete sentences):",
        "whole_section_ci_scaf_label": "Whole-Section Central Idea:",
        "box_bullets_table_header": "BOX & BULLETS: CENTRAL IDEA + SUPPORTING TEXT EVIDENCE",
        "box_bullets_claim_prompt": "Central Idea Claim (State the main historical point of pp. {pages}):",
        "box_bullets_evidence_label": "Supporting Evidence {idx} from {name}:",
        "cer_directions": "Write a 3-part **Claim–Evidence–Reasoning (CER)** response explaining the central idea of pages {pages}.",
        "cer_claim_label": "CLAIM (State the Central Idea in 1 complete sentence):",
        "cer_evidence_label": "EVIDENCE (Cite 1–2 specific facts or laws from pp. {pages}):",
        "cer_reasoning_label": "REASONING (Explain how your evidence supports the Central Idea):",
        "cer_evidence_starter": "For example, on page {page}, the text states that",
        "cer_reasoning_starter": "This evidence proves the central idea because",
        "prove_it_header": "Textbook Printed Main Idea (p. {page}):",
        "prove_it_directions": "DO NOT copy the textbook statement above. Cite 1 specific historical fact or law from each subheading that proves the textbook's claim is true:",
        "prove_it_label": "Proof {idx} from {name}:",
        "what_so_what_directions": "In 1–2 complete sentences, state the **Central Idea** of Section {code} by connecting *what happened* to *why it mattered historically*.",

        # The Writing Revolution (TWR)
        "twr_bbs_directions": "Complete each sentence using specific facts from the reading.",
        "twr_bbs_because": "because",
        "twr_bbs_but": "but",
        "twr_bbs_so": "so",
        "twr_subordinating_directions": "Complete each complex historical sentence using facts from pages {pages}.",
        "twr_kernel_directions": "Expand the short kernel sentence below by answering the guiding questions with facts from pages {pages}.",
        "twr_kernel_label": "Kernel Sentence:",
        "twr_kernel_expanded_label": "Expanded Historical Sentence (1–2 complete sentences):",
        "twr_appositives_directions": "Insert a descriptive noun phrase between commas to define each historical term:",

        # Grade Box & Exemplars
        "grade_box_text": "[GRADE_BOX: Sec {code}   _____/100]",
        "exemplar_header": "# Student Exemplar & Answer Key: Sec. {code} — {strategy_name}",
        "exemplar_meta": "**Textbook Reference:** pp. {pages}  |  **Target Standard:** {standard}  |  **Score:** 100/100",
        "exemplar_model_heading": "### Authentic 8th-Grade Student Model Response",

        # Critical Thinking / Inference
        "crit_focus_focus": "Reading Between the Lines → Text-Based Inference",
        "crit_menu_focus": "Historical Perspectives & Inquiry → Student Choice Inference",
        "crit_focus_directions": "Read the inferential question below. In history, an inference combines facts from the reading with logical reasoning. Complete Steps 1–3 to build your answer.",
        "crit_menu_directions": "Review the three inferential questions below. Check ONE question you want to investigate, then complete Steps 1–3 below using evidence from the text.",
        "crit_step1_label": "Step 1: Text Clues (What the book explicitly says)",
        "crit_step2_label": "Step 2: My Reasoning (What these clues suggest)",
        "crit_step3_label": "Step 3: Inferred Conclusion (Complete answer in 2–3 sentences)",
        "crit_step2_prompt": "How these clues connect to answer the question:",
        "crit_step3_prompt": "Inferred Claim & Historical Explanation:",
    },
    "es": {
        # Worksheet Header & Badges
        "section_badge": "Sección {code}: {title} (págs. {pages})",
        "section_badge_short": "Sec. {code}",
        "scaffolded_edition_tag": " *(Edición con apoyo didáctico)*",
        "strategy_focus_label": "Enfoque de la estrategia: {name}",
        "strategy_focus_prefix": "Enfoque de la estrategia:",

        # Student Metadata Line
        "directions_label": "Instrucciones:",
        "name_label": "Nombre:",
        "date_label": "Fecha:",
        "period_label": "Período:",

        # Vocabulary Practice
        "vocab_practice_title": "Práctica del vocabulario oficial de la sección:",
        "vocab_directions_std": "Lee cada pista a continuación. Con base en la lectura de las páginas {pages}, escribe el término de vocabulario que mejor corresponda a cada definición histórica:",
        "vocab_directions_scaf": "Utiliza el **Banco de palabras** anterior para completar cada pista con el término de vocabulario correcto de las páginas {pages}:",
        "word_bank_label": "Banco de palabras:",
        "vocab_key_label": "Término de vocabulario {idx} ({word}):",

        # Reading Organizers
        "cause_effect_directions": "{prefix} completa la tabla de **Causa y efecto histórico** con información específica de las páginas {pages}.",
        "cause_header": "Causa histórica<br>¿Qué ocurrió primero?",
        "effect_header": "Efecto histórico<br>¿Qué ocurrió como resultado?",
        "say_something_directions": "{prefix} detente después de cada subtítulo para **'¡Dí algo!'** en 1 oración completa respondiendo la pregunta orientadora.",
        "say_something_starter": "Inicio de oración: En esta parte de la lectura, {gist}",
        "cloze_directions": "{prefix} completa los términos históricos que faltan en cada enunciado guiado de las páginas {pages}.",
        "sequence_directions": "{prefix} sigue la **Secuencia cronológica** de los acontecimientos de las páginas {pages} en oraciones completas.",
        "sequence_header": "¿Qué ocurrió en esta etapa? (Acontecimiento clave y resultado)",
        "perspectives_directions": "{prefix} compara las dos perspectivas o acontecimientos históricos de la Sección {code} (págs. {pages}).",
        "perspectives_header": "Postura principal, acciones y evidencia del texto (págs. {pages})",

        # Central Idea Synthesis
        "subheading_gist_directions": "Escribe una idea clave de 10 palabras para cada subtítulo en las líneas punteadas y luego combínalas en una Idea Central completa de la sección en las líneas continuas.",
        "gist_label": "Idea clave para {name}:",
        "whole_section_ci_label": "Idea central de toda la sección (1–2 oraciones completas):",
        "whole_section_ci_scaf_label": "Idea central de toda la sección:",
        "box_bullets_table_header": "ESQUEMA DE CUADRO Y DETALLES: IDEA CENTRAL + EVIDENCIA DEL TEXTO",
        "box_bullets_claim_prompt": "Afirmación de la idea central (Explica el punto histórico principal de las págs. {pages}):",
        "box_bullets_evidence_label": "Evidencia de apoyo {idx} de {name}:",
        "cer_directions": "Redacta una respuesta de 3 partes de **Afirmación–Evidencia–Razonamiento (AER)** explicando la idea central de las páginas {pages}.",
        "cer_claim_label": "AFIRMACIÓN (Expresa la idea central en 1 oración completa):",
        "cer_evidence_label": "EVIDENCIA (Cita 1–2 hechos o leyes específicos de las págs. {pages}):",
        "cer_reasoning_label": "RAZONAMIENTO (Explica cómo tu evidencia respalda la idea central):",
        "cer_evidence_starter": "Por ejemplo, en la página {page}, el texto explica que",
        "cer_reasoning_starter": "Esta evidencia demuestra la idea central porque",
        "prove_it_header": "Idea principal del libro de texto (pág. {page}):",
        "prove_it_directions": "NO copies la afirmación del libro de texto. Cita 1 hecho o ley histórica específica de cada subtítulo que demuestre que la afirmación es verdadera:",
        "prove_it_label": "Prueba {idx} de {name}:",
        "what_so_what_directions": "En 1–2 oraciones completas, expresa la **Idea central** de la Sección {code} conectando *qué ocurrió* con *por qué tuvo importancia histórica*.",

        # The Writing Revolution (TWR)
        "twr_bbs_directions": "Completa cada oración utilizando hechos específicos de la lectura.",
        "twr_bbs_because": "porque",
        "twr_bbs_but": "pero",
        "twr_bbs_so": "por lo tanto",
        "twr_subordinating_directions": "Completa cada oración histórica compleja utilizando hechos de las páginas {pages}.",
        "twr_kernel_directions": "Expande la siguiente oración núcleo respondiendo las preguntas orientadoras con hechos de las páginas {pages}.",
        "twr_kernel_label": "Oración núcleo:",
        "twr_kernel_expanded_label": "Oración histórica expandida (1–2 oraciones completas):",
        "twr_appositives_directions": "Inserta una frase sustantiva descriptiva entre comas para definir cada término histórico:",

        # Grade Box & Exemplars
        "grade_box_text": "[GRADE_BOX: Sec {code}   _____/100]",
        "exemplar_header": "# Modelo y clave de respuestas para el docente: Sec. {code} — {strategy_name}",
        "exemplar_meta": "**Referencia del libro:** págs. {pages}  |  **Estándar:** {standard}  |  **Puntuación:** 100/100",
        "exemplar_model_heading": "### Respuesta modelo auténtica de estudiante de 8.º grado",

        # Critical Thinking / Inference
        "crit_focus_focus": "Lectura entre líneas → Inferencias basadas en el texto",
        "crit_menu_focus": "Perspectivas históricas e indagación → Inferencia con opción a elegir",
        "crit_focus_directions": "Lee la pregunta de inferencia a continuación. En historia, una inferencia combina hechos de la lectura con el razonamiento lógico. Completa los Pasos 1 al 3 para elaborar tu respuesta.",
        "crit_menu_directions": "Revisa las tres preguntas de inferencia a continuación. Marca UNA pregunta que desees investigar y luego completa los Pasos 1 al 3 usando evidencia del texto.",
        "crit_step1_label": "Paso 1: Pistas del texto (Lo que dice el libro)",
        "crit_step2_label": "Paso 2: Mi razonamiento (Lo que estas pistas indican)",
        "crit_step3_label": "Paso 3: Conclusión inferida (Respuesta completa en 2–3 oraciones)",
        "crit_step2_prompt": "Cómo se conectan estas pistas para responder a la pregunta:",
        "crit_step3_prompt": "Afirmación inferida y explicación histórica:",
    },
}

# Spanish strategy focus names (displayed on the student handout under 'Enfoque de la estrategia')
SPANISH_STRATEGY_NAMES: Dict[str, str] = {
    # Central Idea
    "Subheading Gists → Whole-Section Central Idea": "Ideas clave por subtítulo → Idea central",
    "Subheading Gists → Central Idea": "Ideas clave por subtítulo → Idea central",
    "Box & Bullets (Topic + Author's Point = Central Idea)": "Cuadro y viñetas (Idea central + 3 detalles)",
    "Box & Bullets (Central Idea + 3 Details)": "Cuadro y viñetas (Idea central + 3 detalles)",
    "Historical 'What Happened? + So What?' Synthesis": "'¿Qué ocurrió? + ¿Qué importancia tuvo?'",
    "'What Happened? + So What?'": "'¿Qué ocurrió? + ¿Qué importancia tuvo?'",
    "Claim–Evidence–Reasoning (CER) Central Idea Frame": "Afirmación–Evidencia–Razonamiento (AER)",
    "Claim–Evidence–Reasoning (CER)": "Afirmación–Evidencia–Razonamiento (AER)",
    "Claim-Evidence-Reasoning (CER) Central Idea Frame": "Afirmación–Evidencia–Razonamiento (AER)",
    "Claim-Evidence-Reasoning (CER)": "Afirmación–Evidencia–Razonamiento (AER)",
    "Cornell Notes": "Notas Cornell (2 columnas)",

    # Reading Organizers
    "Text Structure: Historical Cause & Effect Table": "Causa y efecto histórico",
    "Cause & Effect Table": "Causa y efecto histórico",
    "Cause & Effect": "Causa y efecto histórico",
    "Multi-Section Cause & Effect": "Causa y efecto multisección",
    "Multi-Section Cause & Effect Synthesis": "Síntesis de causa y efecto multisección",
    "'Say Something!' Subheading Check-Ins (Stop & Jot)": "¡Dí algo! (Reacción por subtítulo)",
    "'Say Something!' by Subheading": "¡Dí algo! (Reacción por subtítulo)",
    "Say Something! (Stop & Jot)": "¡Dí algo! (Reacción por subtítulo)",
    "Say Something!": "¡Dí algo! (Reacción por subtítulo)",
    "Guided Cloze Notes by Subheading (Key Concepts)": "Notas guiadas (Cloze)",
    "Guided Cloze Notes": "Notas guiadas (Cloze)",
    "Text Structure: Chronological Sequence / Event Tracker": "Secuencia cronológica",
    "Chronological Sequence": "Secuencia cronológica",
    "Chronological Sequence Timeline": "Secuencia cronológica",
    "Text Structure: Competing Perspectives / Compare & Contrast": "Comparar perspectivas históricas",
    "Competing Perspectives Matrix": "Comparar perspectivas históricas",
    "Compare Perspectives": "Comparar perspectivas históricas",

    # Anti-Copycat / Printed Main Idea Modes
    "Mode A: 'Prove the Textbook's Main Idea' (Pre-Print & Cite Evidence)": "Demostrar la idea principal del libro",
    "Prove the Textbook's Main Idea": "Demostrar la idea principal del libro",
    "Mode B: 'Subheading Central Ideas' (Target the Unprinted Subsections)": "Enfoque por subtítulo",
    "Subheading Central Ideas": "Enfoque por subtítulo",
    "Subheading Focus": "Enfoque por subtítulo",
    "Mode C: 'Upgrade the Textbook's Main Idea' (Expand with Specifics)": "Ampliar la afirmación histórica",
    "Upgrade the Textbook's Main Idea": "Ampliar la afirmación histórica",
    "Upgrade the Claim": "Ampliar la afirmación histórica",

    # The Writing Revolution (TWR)
    "Because, But, So (Cause, Contrast, Effect)": "Porque, Pero, Por lo tanto (Causa, Contraste, Efecto)",
    "Because, But, So": "Porque, Pero, Por lo tanto",
    "Subordinating Conjunctions (Although, When, After, Since)": "Conjunciones subordinantes (Aunque, Cuando, Si)",
    "Subordinating Conjunctions": "Conjunciones subordinantes (Aunque, Cuando, Si)",
    "Sentence Expansion (When? Where? Why?)": "Expansión de oraciones (Oración núcleo)",
    "Sentence Expansion": "Expansión de oraciones (Oración núcleo)",
    "Kernel Sentence Expansion": "Expansión de oraciones (Oración núcleo)",
    "Appositives (Defining Historical Figures & Laws)": "Aposiciones (Frases explicativas entre comas)",
    "Appositives": "Aposiciones (Frases explicativas entre comas)",
    "Appositive Phrases": "Aposiciones (Frases explicativas entre comas)",
    "Single-Paragraph Outline (SPO – Topic Sentence + 4 Notes + Clincher)": "Esquema de un solo párrafo (EOP)",
    "Single-Paragraph Outline (SPO)": "Esquema de un solo párrafo (EOP)",

    # Vocab and Assessment
    "Vocabulary Practice": "Práctica de vocabulario",
    "Section Assessment": "Evaluación de la sección",
    "Section Check & Quiz": "Evaluación de la sección",

    # Critical Thinking
    "Critical Thinking": "Pensamiento crítico",
    "Read and Infer: Target Question": "Leer e inferir: Pregunta clave",
    "Read & Infer: Target Question": "Leer e inferir: Pregunta clave",
    "Read and Infer: Choice Menu": "Leer e inferir: Menú de opciones",
    "Read & Infer: Choice Menu": "Leer e inferir: Menú de opciones",
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translates a key into the chosen language, falling back to English if missing."""
    lang_dict = STRINGS.get(lang, STRINGS["en"])
    template = lang_dict.get(key, STRINGS["en"].get(key, key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template


def get_localized_strategy_name(name: str, lang: str = "en") -> str:
    """Returns the translated strategy focus name if in Spanish mode."""
    if lang == "es":
        clean_name = name.replace("Optional TWR: ", "").replace("TWR: ", "").strip()
        return SPANISH_STRATEGY_NAMES.get(clean_name, clean_name)
    return name


# ─────────────────────────────────────────────────────────────────────────────
# SPANISH CATALOG AND MARKDOWN LOOKUP HELPERS
# ─────────────────────────────────────────────────────────────────────────────

_SPANISH_CATALOG_CACHE = None
_SPANISH_LOOKUP_MAP = None


def get_spanish_catalog() -> list:
    """Returns the parsed Spanish catalog list, caching in memory."""
    global _SPANISH_CATALOG_CACHE
    if _SPANISH_CATALOG_CACHE is None:
        import json
        from pathlib import Path
        p = Path("output/spanish/catalog.json")
        if p.exists():
            _SPANISH_CATALOG_CACHE = json.loads(p.read_text(encoding="utf-8"))
        else:
            _SPANISH_CATALOG_CACHE = []
    return _SPANISH_CATALOG_CACHE


def get_spanish_section_lookup() -> dict:
    """Returns a map of (chapter_num, str(section_code)) -> section dict."""
    global _SPANISH_LOOKUP_MAP
    if _SPANISH_LOOKUP_MAP is None:
        cat = get_spanish_catalog()
        _SPANISH_LOOKUP_MAP = {
            (s["chapter_num"], str(s["section_code"]).strip()): s
            for s in cat
        }
    return _SPANISH_LOOKUP_MAP


def get_localized_section_meta(section_meta: Dict[str, Any], lang: str = "en") -> Dict[str, Any]:
    """
    Given a section_meta dict (which may be English or Spanish), returns the appropriate
    metadata object for the requested language.
    """
    if lang != "es":
        return section_meta

    cnum = section_meta.get("chapter_num")
    scode = str(section_meta.get("section_code", "")).strip()
    if cnum is None or not scode:
        return section_meta

    lookup = get_spanish_section_lookup()
    return lookup.get((cnum, scode), section_meta)

