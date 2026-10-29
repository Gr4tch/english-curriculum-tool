import sys
import re
import json
from pathlib import Path
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

PDF_PATH = Path("input/Historias Americanas.pdf")
CATALOG_PATH = Path("output/catalog.json")

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


def clean_text(txt: str) -> str:
    txt = txt.replace("\u2009", " ").replace("\u2002", " ").replace("\xa0", " ")
    txt = re.sub(r"[ \t]+", " ", txt)
    return txt.strip()


def extract_section_sample(doc, s_meta):
    ch_num = s_meta["chapter_num"]
    sec_code = s_meta["section_code"]
    start_pg = s_meta["start_page"]
    end_pg = s_meta["end_page"]
    pdf_start = start_pg + 19
    pdf_end = end_pg + 19

    p1 = doc[pdf_start]
    p2 = doc[pdf_end] if pdf_end < len(doc) else p1

    b1 = p1.get_text("blocks")
    b2 = p2.get_text("blocks")

    # 1. Section Title
    raw_title = ""
    for b in b1[:3]:
        txt = b[4].strip()
        m = re.match(r"^\d+[·.]\d+\s+(.*)", txt)
        if m:
            raw_title = clean_text(m.group(1))
            break
    if not raw_title:
        raw_title = s_meta.get("title", f"Sección {sec_code}")

    # 2. Main Idea
    printed_mi = ""
    for b in b1 + b2:
        txt = b[4].strip()
        if "IDEA PRINCIPAL" in txt.upper():
            # Extract sentence following IDEA PRINCIPAL
            clean_b = clean_text(txt)
            m_mi = re.search(r"IDEA\s+PRINCIPAL\s*(.*)", clean_b, flags=re.IGNORECASE)
            if m_mi:
                printed_mi = m_mi.group(1).strip()
                break

    # 3. Historical Thinking Questions
    ht = {}
    ht_raw = ""
    for b in b2 + b1:
        txt = b[4].strip()
        if "RAZONAMIENTO HISTÓRICO" in txt.upper() or "COMPROBAR LA LECTURA" in txt.upper():
            ht_raw += "\n" + clean_text(txt)

    if ht_raw:
        m1 = re.search(r"1\.\s*COMPROBAR\s+LA\s+LECTURA\s*([^2]+?)(?=\s*2\.|\Z)", ht_raw, flags=re.DOTALL)
        if m1:
            ht["q1_reading_check"] = clean_text(m1.group(1))

        m2 = re.search(r"2\.\s*([A-ZÁÉÍÓÚ\s]{4,}?)\s*([^3]+?)(?=\s*3\.|\Z)", ht_raw, flags=re.DOTALL)
        if m2:
            ht["q2_skill"] = f"{clean_text(m2.group(1))}: {clean_text(m2.group(2))}"

        m3 = re.search(r"3\.\s*([A-ZÁÉÍÓÚ\s]{4,}?)\s*(.+?)(?=\n[a-z]|\Z)", ht_raw, flags=re.DOTALL)
        if m3:
            ht["q3_word_meaning"] = f"{clean_text(m3.group(1))}: {clean_text(m3.group(2))}"

    # 4. Critical Viewing
    cv = []
    for b in b1 + b2:
        txt = clean_text(b[4].strip())
        if "VISIÓN CRÍTICA" in txt.upper() or "OBSERVACIÓN CRÍTICA" in txt.upper():
            m_cv = re.search(r"(?:VISIÓN|OBSERVACIÓN)\s+CRÍTICA\s*(.*)", txt, flags=re.IGNORECASE)
            if m_cv and len(m_cv.group(1).strip()) > 10:
                cv.append(m_cv.group(1).strip())

    # 5. Vocabulary in context (thin-space tags)
    all_raw = p1.get_text() + "\n" + p2.get_text()
    raw_v = re.findall(r"\u2009([^\u2009\n]{2,40}?)\u2009", all_raw)
    vocab = []
    seen_v = set()
    for w in raw_v:
        w_clean = clean_text(w)
        if w_clean.lower() not in seen_v and not w_clean.isdigit():
            seen_v.add(w_clean.lower())
            vocab.append(w_clean)

    return {
        "chapter_num": ch_num,
        "section_code": sec_code,
        "printed_pages": f"{start_pg}–{end_pg}",
        "title": raw_title,
        "printed_main_idea": printed_mi,
        "historical_thinking": ht,
        "critical_viewing": cv,
        "vocab": vocab,
    }


def test_samples():
    doc = pymupdf.open(PDF_PATH)
    cat = json.load(open(CATALOG_PATH, encoding="utf-8"))

    sample_secs = [
        next(s for s in cat if s["chapter_num"] == 1 and s["section_code"] == "1.1"),
        next(s for s in cat if s["chapter_num"] == 1 and s["section_code"] == "1.2"),
        next(s for s in cat if s["chapter_num"] == 5 and s["section_code"] == "1.1"),
        next(s for s in cat if s["chapter_num"] == 5 and s["section_code"] == "1.2"),
    ]

    for s in sample_secs:
        res = extract_section_sample(doc, s)
        print(f"=== Ch {res['chapter_num']} Sec {res['section_code']} (pp. {res['printed_pages']}) ===")
        print("Title:", res["title"])
        print("Main Idea:", res["printed_main_idea"])
        print("HT q1:", res["historical_thinking"].get("q1_reading_check"))
        print("HT q2:", res["historical_thinking"].get("q2_skill"))
        print("HT q3:", res["historical_thinking"].get("q3_word_meaning"))
        print("Vocab:", res["vocab"])
        print("Critical Viewing:", res["critical_viewing"][:1])
        print()


if __name__ == "__main__":
    test_samples()
