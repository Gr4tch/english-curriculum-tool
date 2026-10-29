"""
Standalone Spanish Textbook Extractor for 'Historias Americanas'
Processes all 194 sections from 'input/Historias Americanas.pdf' using
this project's exact structural rules and schemas.

Outputs:
  - output/spanish/catalog.json
  - output/spanish/markdown/ChXX_SecY.Y_[Title].md
  - output/spanish/sections/ChXX_SecY.Y_[Title].pdf
  - output/spanish/Historias Americanas (Secciones)/...
"""

import sys
import os
import re
import json
import logging
from pathlib import Path
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PDF_PATH = Path("input/Historias Americanas.pdf")
ENGLISH_CATALOG_PATH = Path("output/catalog.json")

SPANISH_OUTPUT_DIR = Path("output/spanish")
SECTIONS_DIR = SPANISH_OUTPUT_DIR / "sections"
MARKDOWN_DIR = SPANISH_OUTPUT_DIR / "markdown"
HIERARCHY_DIR = SPANISH_OUTPUT_DIR / "Historias Americanas (Secciones)"
SPANISH_CATALOG_PATH = SPANISH_OUTPUT_DIR / "catalog.json"

SPANISH_CHAPTER_TITLES = {
    1: "Tres mundos antes del siglo XVI",
    2: "La exploración europea de las Américas",
    3: "Las trece colonias",
    4: "El desarrollo de las colonias",
    5: "El camino a la guerra",
    6: "La Guerra de Independencia de los EE. UU.",
    7: "Crear la república",
    8: "Primeros pasos de la república",
    9: "La sociedad en la nueva república",
    10: "Expansión y crecimiento",
    11: "La era de Jackson",
    12: "El cambio social en el siglo XIX",
    13: "Hacia el oeste",
    14: "Una nación dividida",
    15: "La Guerra Civil comienza",
    16: "Momentos cruciales de la guerra",
    17: "La Reconstrucción",
}

SPANISH_UNIT_TITLES = {
    1: "Unidad 1 - Primeros encuentros (Inicios–1650)",
    2: "Unidad 2 - Los asentamientos coloniales (1585–1763)",
    3: "Unidad 3 - Una nueva nación (1763–1791)",
    4: "Unidad 4 - Los primeros pasos de la república (1789–1844)",
    5: "Unidad 5 - Ampliación de fronteras (1821–1860)",
    6: "Unidad 6 - Guerra Civil y Reconstrucción (1846–1877)",
}


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "_", text).strip("_")
    return text[:45]


def clean_text(text: str) -> str:
    text = (
        text.replace("\u2009", " ")
        .replace("\u2002", " ")
        .replace("\xa0", " ")
        .replace("\t", " ")
        .replace("\r", "")
    )
    text = re.sub(r"[ ]+", " ", text)
    return text.strip()


def parse_toc_index(doc: pymupdf.Document) -> dict:
    """Extracts (chapter_num, section_code) -> (spanish_title, start_page) directly from TOC pages 6-16."""
    ch_toc_map = {}
    current_ch = 1
    for pno in range(5, 16):
        lines = [clean for l in doc[pno].get_text().split("\n") if (clean := l.strip())]
        i = 0
        while i < len(lines):
            line = lines[i]
            m_ch = re.search(r"^(?:CAPÍTULO|Capítulo)\s*(\d+)?", line)
            if m_ch:
                if m_ch.group(1):
                    current_ch = int(m_ch.group(1))
                elif i > 0 and lines[i - 1].isdigit() and 1 <= int(lines[i - 1]) <= 17:
                    current_ch = int(lines[i - 1])
                elif i + 1 < len(lines) and lines[i + 1].isdigit() and 1 <= int(lines[i + 1]) <= 17:
                    current_ch = int(lines[i + 1])

            m_sec = re.match(r"^(\d+\.\d+)\s*(.*)", line)
            if m_sec:
                sc = m_sec.group(1)
                rest = m_sec.group(2).strip()
                m_pg = re.search(r"\b(\d{1,3})$", rest)
                if m_pg:
                    pg = int(m_pg.group(1))
                    t = rest[: m_pg.start()].strip()
                    ch_toc_map[(current_ch, sc)] = (t, pg)
                else:
                    acc = rest
                    for j in range(i + 1, min(i + 5, len(lines))):
                        nl = lines[j]
                        if re.match(r"^\d+\.\d+", nl) or "SECCIÓN" in nl or "CAPÍTULO" in nl:
                            break
                        m_next = re.search(r"\b(\d{1,3})$", nl)
                        if m_next:
                            pg = int(m_next.group(1))
                            acc += " " + nl[: m_next.start()].strip()
                            ch_toc_map[(current_ch, sc)] = (acc.strip(), pg)
                            i = j
                            break
                        else:
                            acc += " " + nl
            i += 1
    return ch_toc_map


def parse_section_spread(doc: pymupdf.Document, start_page: int, end_page: int, official_title: str):
    pdf_start = start_page + 19
    pdf_end = end_page + 19
    total_pages = len(doc)

    pdf_start = min(pdf_start, total_pages - 1)
    pdf_end = min(pdf_end, total_pages - 1)

    p1 = doc[pdf_start]
    p2 = doc[pdf_end] if pdf_end != pdf_start else None

    pages_to_process = [(start_page, p1)]
    if p2:
        pages_to_process.append((end_page, p2))

    printed_main_idea = ""
    ht_q1 = ""
    ht_q2 = ""
    ht_q3 = ""
    critical_viewing = []
    vocab_terms = []
    seen_vocab = set()

    subheadings = []
    current_sub = None
    current_paras = []

    excluded_headers = {
        "IDEA PRINCIPAL",
        "RAZONAMIENTO HISTÓRICO",
        "HISTORICAL THINKING",
        "VISIÓN CRÍTICA",
        "OBSERVACIÓN CRÍTICA",
        "PRESERVAR LA HISTORIA",
        "SITIOS AMERICANOS",
        "VOCES AMERICANAS",
        "LA GEOGRAFÍA EN LA HISTORIA",
        "LA GEOLOGÍA EN LA HISTORIA",
        "EXPLORADOR DE NATIONAL GEOGRAPHIC",
        "EXPLORADORA DE NATIONAL GEOGRAPHIC",
        "PREGUNTA BASADA EN UN DOCUMENTO",
        "COMPROBAR LA LECTURA",
        "COMPARAR Y CONTRASTAR",
        "ANALIZAR CAUSA Y EFECTO",
        "DETERMINAR EL SIGNIFICADO DE LAS PALABRAS",
        "INTERPRETAR MAPAS",
        "RESUMIR",
        "HACER INFERENCIAS",
        "SINTETIZAR",
        "VOCABULARIO",
        "ESTRATEGIA DE LECTURA",
    }

    # Extract vocabulary words tagged with thin space \u2009
    raw_combined = p1.get_text() + ("\n" + p2.get_text() if p2 else "")
    raw_v_matches = re.findall(r"\u2009([^\u2009\n]{2,40}?)\u2009", raw_combined)
    for rv in raw_v_matches:
        v_clean = clean_text(rv)
        if v_clean.lower() not in seen_vocab and not v_clean.isdigit() and len(v_clean) > 2:
            seen_vocab.add(v_clean.lower())
            vocab_terms.append(v_clean)

    for pg_num, page in pages_to_process:
        page_blocks = page.get_text("blocks")
        for b in page_blocks:
            txt = clean_text(b[4])
            if not txt:
                continue

            # Check Main Idea
            if not printed_main_idea and "IDEA PRINCIPAL" in txt.upper():
                m_mi = re.search(r"IDEA\s+PRINCIPAL\s*(.*)", txt, flags=re.IGNORECASE | re.DOTALL)
                if m_mi:
                    printed_main_idea = clean_text(m_mi.group(1))

            # Check Historical Thinking
            if re.match(r"^1\.\s*(?:COMPROBAR\s+LA\s+LECTURA)?[^\w?]*", txt, flags=re.IGNORECASE):
                q_clean = re.sub(
                    r"^1\.\s*(?:COMPROBAR\s+LA\s+LECTURA)?[^\w?]*", "", txt, flags=re.IGNORECASE
                ).strip()
                ht_q1 = clean_text(q_clean)
            elif re.match(r"^2\.\s*", txt):
                m2 = re.match(r"^2\.\s*([A-ZÁÉÍÓÚ\s]{3,})\s*(.*)", txt, flags=re.DOTALL)
                if m2:
                    ht_q2 = f"{clean_text(m2.group(1))}: {clean_text(m2.group(2))}"
                else:
                    ht_q2 = clean_text(re.sub(r"^2\.\s*", "", txt))
            elif re.match(r"^3\.\s*", txt):
                m3 = re.match(r"^3\.\s*([A-ZÁÉÍÓÚ\s]{3,})\s*(.*)", txt, flags=re.DOTALL)
                if m3:
                    ht_q3 = f"{clean_text(m3.group(1))}: {clean_text(m3.group(2))}"
                else:
                    ht_q3 = clean_text(re.sub(r"^3\.\s*", "", txt))

            # Check Critical Viewing
            if "VISIÓN CRÍTICA" in txt.upper() or "OBSERVACIÓN CRÍTICA" in txt.upper():
                m_cv = re.search(r"(?:VISIÓN|OBSERVACIÓN)\s+CRÍTICA\s*(.*)", txt, flags=re.IGNORECASE | re.DOTALL)
                if m_cv:
                    cv_body = clean_text(m_cv.group(1))
                    if len(cv_body) > 12:
                        critical_viewing.append(f"(pág. {pg_num}) {cv_body}")

            # Check Subheadings
            is_all_caps = txt.isupper() and len(txt) >= 4 and not re.search(r"\d", txt)
            is_subheading_candidate = (
                is_all_caps
                and len(txt) <= 55
                and txt not in excluded_headers
                and not txt.startswith("CAPÍTULO")
                and not txt.startswith("SECCIÓN")
            )

            if is_subheading_candidate:
                if current_sub and current_paras:
                    subheadings.append({
                        "title": current_sub["title"],
                        "page": current_sub["page"],
                        "paragraphs": current_paras,
                    })
                    current_paras = []
                current_sub = {"title": txt, "page": pg_num}
            else:
                if (
                    not txt.startswith("IDEA PRINCIPAL")
                    and not txt.startswith("RAZONAMIENTO HISTÓRICO")
                    and not re.match(r"^[123]\.\s*", txt)
                    and not txt.startswith("VISIÓN CRÍTICA")
                    and not txt.startswith("OBSERVACIÓN CRÍTICA")
                    and not re.match(r"^\d+\s*CAPÍTULO", txt)
                    and not re.match(r"^El camino a la guerra\s*\d+", txt)
                    and len(txt) > 25
                ):
                    if current_sub:
                        current_paras.append(txt)

    if current_sub and current_paras:
        subheadings.append({
            "title": current_sub["title"],
            "page": current_sub["page"],
            "paragraphs": current_paras,
        })

    if not subheadings:
        subheadings = [
            {
                "title": official_title.upper(),
                "page": start_page,
                "paragraphs": [printed_main_idea or official_title],
            }
        ]

    # Build structured vocabulary items
    vocab_items = []
    full_body_text = " ".join(" ".join(sh["paragraphs"]) for sh in subheadings)
    for v_word in vocab_terms[:5]:
        m_def = re.search(
            re.escape(v_word) + r"[,\s]+(?:o\s+([^,.;]{6,85})[,.;]|es\s+(?:un\s+|una\s+)?([^,.;]{6,85})[,.;])",
            full_body_text,
            flags=re.IGNORECASE,
        )
        if m_def:
            defn = clean_text(m_def.group(1) or m_def.group(2) or "")
        else:
            defn = f"Concepto histórico clave definido en la lectura (pág. {start_page})."

        vocab_items.append({
            "word": v_word,
            "type": "Vocabulario de contenido",
            "definition": defn,
            "page": start_page,
        })

    return {
        "title": official_title,
        "printed_main_idea": printed_main_idea,
        "historical_thinking": {
            "q1_reading_check": ht_q1,
            "q2_skill": ht_q2,
            "q3_word_meaning": ht_q3,
        },
        "critical_viewing": critical_viewing,
        "subheadings": subheadings,
        "official_vocab": vocab_items,
        "pdf_start": pdf_start,
        "pdf_end": pdf_end,
    }


def format_spanish_markdown(ch_num: int, sec_code: str, unit_num: int, spread_data: dict, start_pg: int, end_pg: int) -> str:
    ch_title = SPANISH_CHAPTER_TITLES.get(ch_num, f"Capítulo {ch_num}")
    sec_title = spread_data["title"]
    pmi = spread_data["printed_main_idea"]
    vocab = spread_data["official_vocab"]
    subs = spread_data["subheadings"]
    ht = spread_data["historical_thinking"]
    cv = spread_data["critical_viewing"]

    lines = [
        f"# Capítulo {ch_num}: {ch_title}",
        f"## Sección {sec_code}: {sec_title}",
        f"**Unidad {unit_num}** | **Páginas del libro:** {start_pg}–{end_pg} | **Tipo de sección:** Narrativa histórica fundamental",
        "",
        "---",
        "",
    ]

    if pmi:
        lines.extend([
            f"> **IDEA PRINCIPAL DEL LIBRO (pág. {start_pg}):** {pmi}",
            "",
        ])

    if vocab:
        lines.extend([
            "### Vocabulario oficial de la sección",
        ])
        for v in vocab:
            lines.append(f"- **{v['word']}** *({v['type']}, pág. {v['page']})*: {v['definition']}")
        lines.append("")

    lines.extend([
        "### Lectura de la sección (por subtítulo)",
        "",
    ])

    for idx, sh in enumerate(subs, 1):
        lines.append(f"#### {idx}. {sh['title']} (pág. {sh['page']})")
        for p_idx, para in enumerate(sh["paragraphs"], 1):
            lines.append(f"**[¶{p_idx}]** {para}\n")

    lines.extend([
        "---",
        f"### Preguntas del libro: Razonamiento histórico (pág. {end_pg})",
    ])
    if ht.get("q1_reading_check"):
        lines.append(f"1. **COMPROBAR LA LECTURA: {ht['q1_reading_check']}**")
    if ht.get("q2_skill"):
        lines.append(f"2. **{ht['q2_skill']}**")
    if ht.get("q3_word_meaning"):
        lines.append(f"3. **{ht['q3_word_meaning']}**")
    lines.append("")

    if cv:
        lines.append("### Análisis visual y de mapas: Visión crítica")
        for item in cv:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines)


def run_extractor():
    logger.info("Initializing Spanish Textbook Extractor...")
    if not PDF_PATH.exists():
        logger.error(f"Master PDF not found at {PDF_PATH}")
        sys.exit(1)

    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
    HIERARCHY_DIR.mkdir(parents=True, exist_ok=True)

    eng_catalog = json.load(open(ENGLISH_CATALOG_PATH, encoding="utf-8"))
    logger.info(f"Loaded English catalog with {len(eng_catalog)} sections.")

    doc = pymupdf.open(PDF_PATH)
    logger.info(f"Opened master PDF: {PDF_PATH} ({len(doc)} pages).")

    # 1. Parse official TOC mapping
    toc_map = parse_toc_index(doc)
    logger.info(f"Extracted {len(toc_map)} section entries from Spanish TOC.")

    spanish_catalog = []

    for idx, s_meta in enumerate(eng_catalog, 1):
        ch_num = s_meta["chapter_num"]
        sec_code = s_meta["section_code"]
        unit_num = s_meta.get("unit_num", 1)

        # Lookup in TOC mapping
        toc_entry = toc_map.get((ch_num, sec_code))
        if toc_entry:
            sec_title, start_pg = toc_entry
            end_pg = start_pg + 1
        else:
            sec_title = s_meta.get("title", f"Sección {sec_code}")
            start_pg = s_meta["start_page"]
            end_pg = s_meta["end_page"]

        spread_data = parse_section_spread(doc, start_pg, end_pg, sec_title)
        slug = slugify(sec_title)

        filename_base = f"Ch{ch_num:02d}_Sec{sec_code}_{slug}"
        sec_pdf_path = SECTIONS_DIR / f"{filename_base}.pdf"
        sec_md_path = MARKDOWN_DIR / f"{filename_base}.md"

        # 1. Slice 2-page spread PDF
        if not sec_pdf_path.exists():
            sec_doc = pymupdf.open()
            sec_doc.insert_pdf(doc, from_page=spread_data["pdf_start"], to_page=spread_data["pdf_end"])
            sec_doc.save(sec_pdf_path)
            sec_doc.close()

        # 2. Render clean Markdown
        md_content = format_spanish_markdown(ch_num, sec_code, unit_num, spread_data, start_pg, end_pg)
        sec_md_path.write_text(md_content, encoding="utf-8")

        # 3. Save copy to hierarchy folder
        ch_title = SPANISH_CHAPTER_TITLES.get(ch_num, f"Capítulo {ch_num}")
        unit_title = SPANISH_UNIT_TITLES.get(unit_num, f"Unidad {unit_num}")
        ch_folder = HIERARCHY_DIR / unit_title / f"Chapter {ch_num:02d} - {ch_title}"
        ch_folder.mkdir(parents=True, exist_ok=True)
        clean_file_title = re.sub(r'[<>:"/\\|?*\x00-\x1f\[\]]', "", sec_title).strip()
        hier_pdf_path = ch_folder / f"Sec {sec_code} - {clean_file_title[:40]}.pdf"
        if not hier_pdf_path.exists() and sec_pdf_path.exists():
            hier_pdf_path.write_bytes(sec_pdf_path.read_bytes())

        # 4. Catalog entry
        cat_entry = {
            "id": f"ch{ch_num:02d}_sec{sec_code.replace('.', '_')}",
            "unit_num": unit_num,
            "unit_title": unit_title,
            "chapter_num": ch_num,
            "chapter_title": ch_title,
            "section_code": sec_code,
            "title": sec_title,
            "section_type": s_meta.get("section_type", "Core Historical Narrative"),
            "is_special_feature": s_meta.get("is_special_feature", False),
            "printed_pages": f"{start_pg}–{end_pg}",
            "start_page": start_pg,
            "end_page": end_pg,
            "pdf_file": str(sec_pdf_path).replace("\\", "/"),
            "hierarchy_pdf_file": str(hier_pdf_path).replace("\\", "/"),
            "md_file": str(sec_md_path).replace("\\", "/"),
            "word_count": len(md_content.split()),
            "printed_main_idea": spread_data["printed_main_idea"],
            "subheadings": [
                {"title": sh["title"], "page": sh["page"], "paragraph_count": len(sh["paragraphs"])}
                for sh in spread_data["subheadings"]
            ],
            "historical_thinking": spread_data["historical_thinking"],
            "critical_viewing": spread_data["critical_viewing"],
            "official_vocab": spread_data["official_vocab"],
        }
        spanish_catalog.append(cat_entry)

        if idx % 25 == 0 or idx == len(eng_catalog):
            logger.info(f"Processed {idx:3d}/{len(eng_catalog)} sections: Ch {ch_num:02d} Sec {sec_code:4s} -> {sec_title[:32]}")

    SPANISH_CATALOG_PATH.write_text(json.dumps(spanish_catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"Successfully generated Spanish catalog: {SPANISH_CATALOG_PATH} with {len(spanish_catalog)} sections.")
    doc.close()


if __name__ == "__main__":
    run_extractor()
