import html
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

import pymupdf

SCRATCH_DIR = Path(r"C:\Users\Jared\.gemini\antigravity\brain\92772fbc-5c9c-4123-a8d8-418629612250\scratch")
LOCAL_CACHE_DIR = Path("input/cengage_cache")

SECTIONS_DIR = Path("output/sections")
MARKDOWN_DIR = Path("output/markdown")
CATALOG_PATH = Path("output/catalog.json")
VOCAB_INDEX_PATH = Path("output/vocab_index.json")
CHAPTER_REVIEWS_PATH = Path("output/chapter_reviews.json")
HIERARCHY_BASE_DIR = Path("output/American Stories (Sections)")

UNIT_NAMES = {
    1: "Unit 1 - Early Encounters (Beginnings–1650)",
    2: "Unit 2 - English Settlement (1585–1763)",
    3: "Unit 3 - A New Nation (1763–1791)",
    4: "Unit 4 - The Early Republic (1789–1844)",
    5: "Unit 5 - Pushing Boundaries (1821–1860)",
    6: "Unit 6 - Civil War and Reconstruction (1846–1877)",
}

SPECIAL_SPREAD_MARKERS = [
    ("american voices", "Biography / Primary Voice"),
    ("curating history", "Museum / Artifact Feature"),
    ("preserving history", "Historic Site Feature"),
    ("american places", "Historic Landmark Feature"),
    ("geography in history", "Geography & Map Feature"),
    ("geology in history", "Geography & Science Feature"),
    ("national geographic explorer", "Explorer Feature"),
    ("document-based question", "Document-Based Question (DBQ)"),
]


def classify_section_type(title: str) -> Dict[str, Any]:
    """Classifies whether a 2-page spread is a Core Narrative section or a Special Feature spread."""
    t_low = title.lower()
    for marker, badge in SPECIAL_SPREAD_MARKERS:
        if marker in t_low:
            return {
                "is_special_feature": True,
                "section_type": badge,
            }
    return {
        "is_special_feature": False,
        "section_type": "Core Historical Narrative",
    }


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "_", text).strip("_")
    return text[:48]


def get_cache_paths() -> Tuple[Path, Path]:
    """Returns (structure_json_path, book_cache_dir), copying from scratch to input/ if needed."""
    local_struct = LOCAL_CACHE_DIR / "structure.json"
    local_book = LOCAL_CACHE_DIR / "book_cache"
    if local_struct.exists() and local_book.exists():
        return local_struct, local_book

    scratch_struct = SCRATCH_DIR / "structure.json"
    scratch_book = SCRATCH_DIR / "book_cache"
    if scratch_struct.exists() and scratch_book.exists():
        LOCAL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        if not local_struct.exists():
            shutil.copy2(scratch_struct, local_struct)
        return scratch_struct, scratch_book

    raise FileNotFoundError("Cached Cengage structure.json and book_cache not found.")


def parse_html_spans(html_text: str) -> List[Dict[str, Any]]:
    """
    Extracts positioned text spans from the Cengage HTML5 page's <div class="textLayer">.
    Returns a list of dicts with keys: text, left, top, font_size, font_family.
    """
    span_pattern = re.compile(r'<span\s+style="([^"]+)"[^>]*>(.*?)</span>', re.DOTALL)
    spans = []
    for style_str, raw_inner in span_pattern.findall(html_text):
        clean_txt = html.unescape(re.sub(r"<[^>]+>", "", raw_inner))
        # Fix common mojibake / ligatures from PDF encoding
        clean_txt = (
            clean_txt.replace("\ufffd", "'")
            .replace("\u2019", "'")
            .replace("\u2018", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2013", "–")
            .replace("\u2014", "—")
        )
        if not clean_txt.strip():
            continue

        left_m = re.search(r"left:\s*([0-9.]+)px", style_str)
        top_m = re.search(r"top:\s*([0-9.]+)px", style_str)
        fs_m = re.search(r"font-size:\s*([0-9.]+)px", style_str)
        ff_m = re.search(r"font-family:\s*([^;]+)", style_str)

        left = float(left_m.group(1)) if left_m else 0.0
        top = float(top_m.group(1)) if top_m else 0.0
        font_size = float(fs_m.group(1)) if fs_m else 12.0
        font_family = ff_m.group(1).strip() if ff_m else "sans-serif"

        # Filter out bottom copyright boilerplate (typically at top > 2020px or tiny 5px-10px font)
        if "Copyright 2025 Cengage" in clean_txt or "Editorial review has deemed" in clean_txt:
            continue

        spans.append({
            "text": clean_txt,
            "left": left,
            "top": top,
            "font_size": font_size,
            "font_family": font_family,
        })
    return spans


def parse_reference_vocab(page_map: Dict[str, Path]) -> Dict[str, Any]:
    """
    Parses pages R44 ('Vocabulary Words by Chapter') and R45 ('Academic Vocabulary')
    plus the English Glossary (R46..R53) to build a structured vocabulary index.
    """
    vocab_by_chapter: Dict[str, List[Dict[str, Any]]] = {}
    academic_vocab_by_page: Dict[int, List[Dict[str, Any]]] = {}
    glossary_defs: Dict[str, str] = {}

    # 1. Parse Glossary pages R46..R53 for official definitions
    for pg_num in range(46, 54):
        lp_key = f"R{pg_num}"
        if lp_key not in page_map:
            continue
        html_txt = page_map[lp_key].read_text(encoding="utf-8", errors="ignore")
        spans = parse_html_spans(html_txt)
        full_glossary_text = " ".join(s["text"].strip() for s in spans)
        # Match patterns like: word n./v./adj. (pronunciation) definition (page XXX)
        entries = re.findall(
            r"([A-Za-z][A-Za-z\s\-']{1,30}?)\s+(?:n\.|v\.|adj\.|adv\.)?\s*(?:\([^)]+\)\s*)?([^()]+?)\s*\(page\s+(\d+)\)",
            full_glossary_text
        )
        for term, defn, _pg in entries:
            clean_term = term.strip().lower()
            clean_def = re.sub(r"\s+", " ", defn).strip(" .,;")
            if 2 <= len(clean_term) <= 35 and len(clean_def) > 8:
                glossary_defs[clean_term] = clean_def

    # 2. Parse R45 Academic Vocabulary (includes pronunciation, POS, definition, and page number)
    if "R45" in page_map:
        html_r45 = page_map["R45"].read_text(encoding="utf-8", errors="ignore")
        spans_r45 = parse_html_spans(html_r45)
        r45_text = " ".join(s["text"].strip() for s in spans_r45)
        acad_matches = re.findall(
            r"([a-z][a-z\-]+)\s+(n\.|v\.|adj\.|adv\.)\s*\(([^)]+)\)\s*([^()]+?)\s*\(page\s+(\d+)\)",
            r45_text
        )
        for word, pos, pron, defn, pg_str in acad_matches:
            pg_int = int(pg_str)
            clean_def = re.sub(r"\s+", " ", defn).strip(" .,;")
            academic_vocab_by_page.setdefault(pg_int, []).append({
                "word": word.strip(),
                "type": "Academic Vocabulary",
                "pos": pos.strip(),
                "pronunciation": pron.strip(),
                "definition": clean_def,
                "page": pg_int,
            })

    # 3. Parse R44 Vocabulary Words by Chapter
    if "R44" in page_map:
        html_r44 = page_map["R44"].read_text(encoding="utf-8", errors="ignore")
        spans_r44 = parse_html_spans(html_r44)
        r44_text = " ".join(s["text"].strip() for s in spans_r44)
        ch_splits = re.split(r"Chapter\s+(\d+)", r44_text)
        # ch_splits[0] is header; then pairs of (ch_num, ch_block)
        for idx in range(1, len(ch_splits) - 1, 2):
            ch_num_str = ch_splits[idx].strip()
            ch_block = ch_splits[idx + 1]
            word_matches = re.findall(r"([A-Za-z][A-Za-z0-9\s\-’']{1,45}?)\s*\(page\s+(\d+)\)", ch_block)
            ch_words = []
            for raw_w, pg_str in word_matches:
                clean_w = raw_w.strip()
                # If clean_w has a leading chapter title (not in glossary), find the matching glossary sub-phrase
                if clean_w.lower() not in glossary_defs:
                    parts = clean_w.split()
                    for k in range(1, len(parts)):
                        cand = " ".join(parts[k:]).strip()
                        if cand.lower() in glossary_defs:
                            clean_w = cand
                            break

                pg_int = int(pg_str)
                defn = glossary_defs.get(clean_w.lower(), "")
                ch_words.append({
                    "word": clean_w,
                    "type": "Content Vocabulary",
                    "definition": defn,
                    "page": pg_int,
                })
            vocab_by_chapter[ch_num_str] = ch_words

    return {
        "by_chapter": vocab_by_chapter,
        "academic_by_page": {str(k): v for k, v in academic_vocab_by_page.items()},
        "glossary_definitions": glossary_defs,
    }


def extract_inline_definitions(body_text: str) -> Dict[str, str]:
    """
    Finds inline textbook definitions such as:
      - 'needed revenue, or income, to pay off...'
      - 'accused the British of tyranny, or unjust rule by an absolute ruler.'
      - 'A covenant is an agreement or promise between two parties.'
    """
    inline_defs: Dict[str, str] = {}
    stopwords = {
        "and", "or", "in", "with", "to", "for", "from", "on", "at", "by",
        "if", "when", "that", "this", "these", "those", "either", "whether",
        "more", "less", "one", "two", "the", "a", "an", "as", "their", "his", "her"
    }

    # Pattern 1: '<term>, or <definition>,' or '<term>, or <definition>.'
    for m in re.finditer(r"\b([A-Za-z][A-Za-z\-]+(?:\s+[A-Za-z\-]+)?),\s+or\s+([^,.;]{6,85})[,.;]", body_text):
        term = m.group(1).strip()
        defn = m.group(2).strip()
        t_words = term.lower().split()
        if not t_words or t_words[0] in stopwords or t_words[-1] in stopwords:
            continue
        inline_defs[term.lower()] = defn

    # Pattern 2: 'A/An <term> is a/an <definition>.'
    for m in re.finditer(r"\b(?:A|An|The)\s+([a-z][a-z\s\-]{2,25}?)\s+(?:is|was)\s+((?:an?|the)\s+[^.]{8,95})\.", body_text):
        term = m.group(1).strip()
        defn = m.group(2).strip()
        t_words = term.lower().split()
        if not t_words or t_words[0] in stopwords or t_words[-1] in stopwords:
            continue
        inline_defs[term.lower()] = defn

    return inline_defs


def parse_spread_pedagogical_blocks(
    left_spans: List[Dict[str, Any]],
    right_spans: List[Dict[str, Any]],
    start_page: int,
    end_page: int,
    section_title: str
) -> Dict[str, Any]:
    """
    Reconstructs clean structured text, subheadings, printed MAIN IDEA,
    HISTORICAL THINKING (#1-3), and CRITICAL VIEWING prompts from the 2-page spread spans.
    """
    all_page_pairs = [(start_page, left_spans), (end_page, right_spans)]

    subheadings: List[Dict[str, Any]] = []
    printed_main_idea = ""
    historical_thinking: Dict[str, str] = {}
    critical_viewing: List[str] = []
    paragraphs_by_page: Dict[int, List[str]] = {start_page: [], end_page: []}

    for pg_num, spans in all_page_pairs:
        # Join spans in reading order as contained in the HTML
        lines = [s["text"].strip() for s in spans if s["text"].strip()]
        raw_joined = " ".join(lines)
        raw_joined = re.sub(r"\s+", " ", raw_joined)

        # 1. Extract MAIN IDEA if present on this page
        mi_match = re.search(
            r"MAIN\s+IDEA\s+(.+?)(?=(?:CRITICAL\s+VIEWING|HISTORICAL\s+THINKING|\b1\s*·\s*\d|\b\d{3}\s+CHAPTER|$))",
            raw_joined
        )
        if mi_match and not printed_main_idea:
            mi_candidate = mi_match.group(1).strip()
            # Keep first sentence or two up to 240 chars
            mi_sentences = re.split(r"(?<=[.!?])\s+", mi_candidate)
            printed_main_idea = mi_sentences[0].strip()

        # 2. Extract HISTORICAL THINKING (#1, #2, #3)
        ht_match = re.search(
            r"HISTORICAL\s+THINKING\s+1\.\s*([A-Z]+(?:\s+[A-Z]+){0,3})\s+([^?]+\?)\s*2\.\s*([A-Z]+(?:\s+[A-Z]+){0,4})\s+([^?]+\?)(?:\s*3\.\s*([A-Z]+(?:\s+[A-Z]+){0,4})\s+([^?]+\?))?",
            raw_joined
        )
        if ht_match:
            q1_label = ht_match.group(1).strip()
            q1_text = ht_match.group(2).strip()
            q2_label = ht_match.group(3).strip()
            q2_text = ht_match.group(4).strip()
            historical_thinking["q1_reading_check"] = f"{q1_label}: {q1_text}"
            historical_thinking["q2_skill"] = f"{q2_label}: {q2_text}"

            if ht_match.group(5) and ht_match.group(6):
                q3_label = ht_match.group(5).strip()
                q3_text = ht_match.group(6).strip()
                historical_thinking["q3_word_meaning"] = f"{q3_label}: {q3_text}"

        # 3. Extract CRITICAL VIEWING prompts
        for cv_m in re.finditer(r"CRITICAL\s+VIEWING\s+([^?]+\?)", raw_joined):
            cv_txt = cv_m.group(1).strip()
            if 15 < len(cv_txt) < 380 and cv_txt not in critical_viewing:
                critical_viewing.append(f"(p. {pg_num}) {cv_txt}")

        # Remove the extracted callout boxes from raw_joined before body/subheading parsing
        # Filter spans to exclude HISTORICAL THINKING box, MAIN IDEA box, and CRITICAL VIEWING box
        excluded_caps = {
            "MAIN IDEA", "HISTORICAL THINKING", "CRITICAL VIEWING", "READING CHECK",
            "COMPARE AND CONTRAST", "ANALYZE CAUSE AND EFFECT", "DETERMINE WORD MEANING",
            "MAKE INFERENCES", "SYNTHESIZE", "EVALUATE", "INTERPRET MAPS", "PRIMARY SOURCE",
            "AMERICAN VOICES", "CURATING HISTORY", "AMERICAN PLACES", "GEOLOGY IN HISTORY",
            "GEOGRAPHY IN HISTORY", "DOCUMENT-BASED QUESTION", "BACKGROUND", "VOCABULARY"
        }

        current_sub = None
        current_buf: List[str] = []
        skip_mode = None  # 'ht', 'mi', 'cv'

        for s in spans:
            txt = s["text"].strip()
            if not txt or re.match(r"^\d+$", txt) or txt == "·":
                continue
            if txt.upper().startswith("CHAPTER "):
                continue

            if txt == "HISTORICAL THINKING":
                skip_mode = "ht"
                continue
            elif txt == "MAIN IDEA":
                skip_mode = "mi"
                continue
            elif txt == "CRITICAL VIEWING":
                skip_mode = "cv"
                continue

            # Check if a new subheading starts (ends any active skip_mode)
            is_subheading_span = (
                s["font_size"] >= 23.0
                and txt.isupper()
                and len(txt) >= 4
                and not any(ex in txt for ex in excluded_caps)
                and txt != section_title.upper()
            )
            if is_subheading_span:
                skip_mode = None
                if current_sub and current_buf:
                    sub_body = re.sub(r"\s+", " ", " ".join(current_buf)).strip()
                    subheadings.append({
                        "title": current_sub,
                        "page": pg_num,
                        "content": sub_body,
                    })
                    current_buf = []
                    current_sub = None
                if current_sub and not current_buf and subheadings and subheadings[-1]["page"] == pg_num:
                    current_sub = f"{current_sub} {txt}"
                else:
                    current_sub = txt
                continue

            # If inside HISTORICAL THINKING box, skip until after question 3 (or question 2) ends with '?'
            if skip_mode == "ht":
                if "?" in txt and s["top"] > 200 and not any(k in txt for k in ("1.", "2.", "3.")):
                    # Check if next body text starts (font_size >= 25.0 is main body text in Cengage!)
                    pass
                if s["font_size"] >= 25.5 and not any(ex in txt for ex in excluded_caps):
                    skip_mode = None
                else:
                    continue
            elif skip_mode in ("mi", "cv"):
                if s["font_size"] >= 25.5 and not any(ex in txt for ex in excluded_caps):
                    skip_mode = None
                else:
                    continue

            # Skip main section title banner (font_size >= 45)
            if s["font_size"] >= 45.0:
                continue

            # Main body text in American Stories has font_size around 26.67px
            if current_sub is None and subheadings:
                subheadings[-1]["content"] += " " + txt
            elif current_sub is not None:
                current_buf.append(txt)
            else:
                paragraphs_by_page[pg_num].append(txt)

        if current_sub and current_buf:
            sub_body = re.sub(r"\s+", " ", " ".join(current_buf)).strip()
            subheadings.append({
                "title": current_sub,
                "page": pg_num,
                "content": sub_body,
            })

    # Clean subheading bodies and split into logical paragraphs for [¶1], [¶2] citation accuracy
    for sh in subheadings:
        cleaned = re.sub(r"\s+", " ", sh["content"]).strip()
        sh["content"] = cleaned
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", cleaned)
        paras = []
        chunk = []
        for sent in sentences:
            chunk.append(sent)
            if len(" ".join(chunk)) >= 280:
                paras.append(" ".join(chunk))
                chunk = []
        if chunk:
            paras.append(" ".join(chunk))
        sh["paragraphs"] = paras if paras else [cleaned]

    # Fallback if a special feature spread has no standard ALL-CAPS subheadings
    if not subheadings:
        for pg_num in (start_page, end_page):
            raw_p = " ".join(paragraphs_by_page.get(pg_num, [])).strip()
            raw_p = re.split(r"\b(?:MAIN IDEA|HISTORICAL THINKING|CRITICAL VIEWING)\b", raw_p)[0].strip()
            if raw_p:
                subheadings.append({
                    "title": f"{section_title.upper()} (PART {1 if pg_num == start_page else 2})",
                    "page": pg_num,
                    "content": raw_p,
                    "paragraphs": [raw_p],
                })

    full_spread_text = " ".join(sh["content"] for sh in subheadings)
    inline_defs = extract_inline_definitions(full_spread_text)

    return {
        "printed_main_idea": printed_main_idea,
        "subheadings": subheadings,
        "historical_thinking": historical_thinking,
        "critical_viewing": critical_viewing,
        "inline_definitions": inline_defs,
        "full_text": full_spread_text,
    }


def build_two_page_pdf(
    left_html_path: Path,
    right_html_path: Path,
    book_cache_dir: Path,
    out_pdf_path: Path
):
    """
    Builds a crisp, searchable 2-page PDF for the section using the cached high-res
    1584x2088 JPG page images and overlays an invisible selectable text layer.
    """
    if out_pdf_path.exists():
        return

    doc = pymupdf.open()
    # Standard textbook page size in points (792 x 1044 pt = 11" x 14.5" or scaled to 612 x 807 pt)
    page_w, page_h = 612.0, 807.0
    scale_x = page_w / 1584.0
    scale_y = page_h / 2088.0

    for html_path in (left_html_path, right_html_path):
        if not html_path or not html_path.exists():
            continue
        html_str = html_path.read_text(encoding="utf-8", errors="ignore")
        page = doc.new_page(width=page_w, height=page_h)

        # 1. Insert high-res page image
        m_img = re.search(r'src="(assets/[^"]+\.jpg)"', html_str)
        if m_img:
            img_path = book_cache_dir / m_img.group(1)
            if img_path.exists():
                page.insert_image(pymupdf.Rect(0, 0, page_w, page_h), filename=str(img_path))

        # 2. Overlay invisible searchable text spans (render_mode=3 is invisible text)
        spans = parse_html_spans(html_str)
        for sp in spans:
            x = sp["left"] * scale_x
            y = (sp["top"] + sp["font_size"] * 0.85) * scale_y
            fs = max(4.0, sp["font_size"] * scale_y * 0.85)
            try:
                page.insert_text(
                    pymupdf.Point(x, y),
                    sp["text"],
                    fontsize=fs,
                    render_mode=3
                )
            except Exception:
                pass

    out_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_pdf_path), deflate=True)
    doc.close()


def format_section_markdown(
    unit_num: int,
    ch_num: int,
    ch_title: str,
    sec_code: str,
    sec_title: str,
    start_page: int,
    end_page: int,
    section_type: str,
    spread_data: Dict[str, Any],
    sec_vocab: List[Dict[str, Any]]
) -> str:
    """Formats the rich, structured English Markdown file for a 2-page section."""
    lines = [
        f"# Chapter {ch_num}: {ch_title}",
        f"## Section {sec_code}: {sec_title}",
        f"**Unit {unit_num}** | **Textbook Pages:** {start_page}–{end_page} | **Section Type:** {section_type}",
        "",
        "---",
        "",
    ]

    if spread_data.get("printed_main_idea"):
        lines.extend([
            f"> **TEXTBOOK PRINTED MAIN IDEA (p. {start_page}):** {spread_data['printed_main_idea']}",
            "",
        ])

    if sec_vocab:
        lines.append("### Official Section Vocabulary")
        for v in sec_vocab:
            v_def = v.get("definition") or "Defined in context below."
            lines.append(f"- **{v['word']}** *({v['type']}, p. {v['page']})*: {v_def}")
        lines.append("")

    lines.append("### Section Reading Passage (By Subheading)")
    lines.append("")
    for idx, sh in enumerate(spread_data.get("subheadings", []), start=1):
        lines.append(f"#### {idx}. {sh['title']} (p. {sh['page']})")
        for p_idx, para in enumerate(sh.get("paragraphs", [sh["content"]]), start=1):
            lines.append(f"**[¶{p_idx}]** {para}")
            lines.append("")

    ht = spread_data.get("historical_thinking", {})
    if ht:
        lines.append("---")
        lines.append(f"### Built-In Textbook Questions: Historical Thinking (p. {end_page})")
        if ht.get("q1_reading_check"):
            lines.append(f"1. **{ht['q1_reading_check']}**")
        if ht.get("q2_skill"):
            lines.append(f"2. **{ht['q2_skill']}**")
        if ht.get("q3_word_meaning"):
            lines.append(f"3. **{ht['q3_word_meaning']}**")
        lines.append("")

    cv = spread_data.get("critical_viewing", [])
    if cv:
        lines.append("### Built-In Visual & Map Analysis: Critical Viewing")
        for item in cv:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def parse_chapter_review(
    ch_num: int,
    ch_title: str,
    page_map: Dict[str, Path],
    review_pages: List[int]
) -> Dict[str, Any]:
    """Extracts the official end-of-chapter Review questions (Vocabulary, Main Ideas, Historical Thinking, Map)."""
    spans = []
    for pg in review_pages:
        p_path = page_map.get(str(pg))
        if p_path and p_path.exists():
            spans.extend(parse_html_spans(p_path.read_text(encoding="utf-8", errors="ignore")))

    raw_text = re.sub(r"\s+", " ", " ".join(s["text"].strip() for s in spans)).strip()
    questions = []
    for m in re.finditer(r"\b(\d{1,2})\.\s+([^0-9]{10,260}?\?)", raw_text):
        q_num = int(m.group(1))
        q_body = m.group(2).strip()
        questions.append({"num": q_num, "question": q_body})

    return {
        "chapter_num": ch_num,
        "chapter_title": ch_title,
        "printed_pages": f"{review_pages[0]}–{review_pages[-1]}" if review_pages else "",
        "questions": questions,
        "raw_review_text": raw_text[:4000],
    }


def run_cengage_compiler() -> List[Dict[str, Any]]:
    """
    Main offline compiler entry point.
    Processes all 699 cached pages into:
      - 194 searchable 2-page PDFs in output/sections/
      - Organized folder hierarchy in output/American Stories (Sections)/
      - 194 structured Markdown files in output/markdown/
      - output/vocab_index.json
      - output/chapter_reviews.json
      - output/catalog.json
    """
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)

    struct_path, book_cache_dir = get_cache_paths()
    data = json.loads(struct_path.read_text(encoding="utf-8"))

    # 1. Build logicalPageNumber -> HTML Path map across the entire book
    page_map: Dict[str, Path] = {}

    def walk_pages(nodes):
        for n in nodes:
            lp = n.get("localPath")
            log_pg = str(n.get("logicalPageNumber", "")).strip()
            if lp and log_pg:
                full_p = book_cache_dir / lp
                if full_p.exists():
                    page_map[log_pg] = full_p
            if n.get("content"):
                walk_pages(n["content"])

    walk_pages(data["book"]["content"])

    # 2. Parse Official Content & Academic Vocabulary from R44..R53
    vocab_index = parse_reference_vocab(page_map)
    VOCAB_INDEX_PATH.write_text(json.dumps(vocab_index, indent=2, ensure_ascii=False), encoding="utf-8")

    # 3. Walk Units and Chapters to extract all 2-page sections and Chapter Reviews
    catalog: List[Dict[str, Any]] = []
    chapter_reviews: Dict[str, Any] = {}

    for top_node in data["book"]["content"]:
        u_title = top_node.get("title", "").strip()
        u_match = re.match(r"Unit\s+(\d+):\s*(.*)", u_title, re.IGNORECASE)
        if not u_match:
            continue
        unit_num = int(u_match.group(1))

        for ch_node in top_node.get("content", []):
            ch_raw_title = ch_node.get("title", "").strip()
            ch_match = re.match(r"Chapter\s+(\d+):\s*(.*)", ch_raw_title, re.IGNORECASE)
            if not ch_match:
                continue
            ch_num = int(ch_match.group(1))
            ch_title = re.sub(r"\s*\(\d+[-–]\d+\)\s*$", "", ch_match.group(2)).strip()

            ch_pages_nodes = ch_node.get("content", [])
            all_ch_page_nums = []
            raw_sections = []

            for p_node in ch_pages_nodes:
                p_title = p_node.get("title", "").strip()
                log_pg_str = str(p_node.get("logicalPageNumber", "")).strip()
                if log_pg_str.isdigit():
                    all_ch_page_nums.append(int(log_pg_str))

                sec_m = re.match(r"^(\d+\.\d+)\s+(.+)$", p_title)
                if sec_m and log_pg_str.isdigit():
                    sec_code = sec_m.group(1).strip()
                    sec_title = sec_m.group(2).strip()
                    toc_pg = int(log_pg_str)
                    # Every section in American Stories is a 2-page even-odd spread
                    start_pg = toc_pg if (toc_pg % 2 == 0) else (toc_pg - 1)
                    end_pg = start_pg + 1
                    raw_sections.append({
                        "section_code": sec_code,
                        "title": sec_title,
                        "start_page": start_pg,
                        "end_page": end_pg,
                    })

            # Parse Chapter Review from the last 2 pages of the chapter
            if len(all_ch_page_nums) >= 2:
                rev_pages = sorted(all_ch_page_nums)[-2:]
                chapter_reviews[str(ch_num)] = parse_chapter_review(ch_num, ch_title, page_map, rev_pages)

            # Process each 2-page section in this chapter
            ch_content_vocab = vocab_index["by_chapter"].get(str(ch_num), [])

            for sec_info in raw_sections:
                sec_code = sec_info["section_code"]
                sec_title = sec_info["title"]
                start_pg = sec_info["start_page"]
                end_pg = sec_info["end_page"]

                left_html = page_map.get(str(start_pg))
                right_html = page_map.get(str(end_pg))

                left_spans = parse_html_spans(left_html.read_text(encoding="utf-8", errors="ignore")) if left_html else []
                right_spans = parse_html_spans(right_html.read_text(encoding="utf-8", errors="ignore")) if right_html else []

                spread_data = parse_spread_pedagogical_blocks(
                    left_spans, right_spans, start_pg, end_pg, sec_title
                )

                # Match Official Content & Academic Vocabulary to this 2-page spread
                sec_vocab = []
                seen_v = set()
                for cv_item in ch_content_vocab:
                    if start_pg <= cv_item["page"] <= end_pg:
                        w_low = cv_item["word"].lower()
                        defn = cv_item["definition"] or spread_data["inline_definitions"].get(w_low, "")
                        sec_vocab.append({
                            "word": cv_item["word"],
                            "type": "Content Vocabulary",
                            "definition": defn,
                            "page": cv_item["page"],
                        })
                        seen_v.add(w_low)

                for pg_k in (str(start_pg), str(end_pg)):
                    for av_item in vocab_index["academic_by_page"].get(pg_k, []):
                        w_low = av_item["word"].lower()
                        if w_low not in seen_v:
                            sec_vocab.append(av_item)
                            seen_v.add(w_low)

                # Also add any inline-defined terms not yet in sec_vocab
                for in_word, in_def in spread_data["inline_definitions"].items():
                    if in_word not in seen_v and len(sec_vocab) < 6:
                        sec_vocab.append({
                            "word": in_word,
                            "type": "Key Concept",
                            "definition": in_def,
                            "page": start_pg,
                        })
                        seen_v.add(in_word)

                type_info = classify_section_type(sec_title)
                slug = slugify(sec_title)
                filename_base = f"Ch{ch_num:02d}_Sec{sec_code}_{slug}"
                pdf_out_path = SECTIONS_DIR / f"{filename_base}.pdf"
                md_out_path = MARKDOWN_DIR / f"{filename_base}.md"

                # 1. Build searchable 2-page PDF
                build_two_page_pdf(left_html, right_html, book_cache_dir, pdf_out_path)

                # 2. Copy into Unit > Chapter > Section local hierarchy
                u_folder = UNIT_NAMES.get(unit_num, f"Unit {unit_num}")
                ch_folder = f"Chapter {ch_num:02d} - {ch_title}"
                target_dir = HIERARCHY_BASE_DIR / u_folder / ch_folder
                target_dir.mkdir(parents=True, exist_ok=True)
                clean_sec_title = re.sub(r'[\\/*?:"<>|]', "", sec_title).strip()
                hier_pdf_path = target_dir / f"Sec {sec_code} - {clean_sec_title}.pdf"
                if pdf_out_path.exists() and not hier_pdf_path.exists():
                    shutil.copy2(pdf_out_path, hier_pdf_path)

                # 3. Write structured Markdown
                md_text = format_section_markdown(
                    unit_num=unit_num,
                    ch_num=ch_num,
                    ch_title=ch_title,
                    sec_code=sec_code,
                    sec_title=sec_title,
                    start_page=start_pg,
                    end_page=end_pg,
                    section_type=type_info["section_type"],
                    spread_data=spread_data,
                    sec_vocab=sec_vocab,
                )
                md_out_path.write_text(md_text, encoding="utf-8")

                word_count = len(spread_data["full_text"].split())

                catalog.append({
                    "id": f"ch{ch_num:02d}_sec{sec_code.replace('.', '_')}",
                    "unit_num": unit_num,
                    "unit_title": UNIT_NAMES.get(unit_num, f"Unit {unit_num}"),
                    "chapter_num": ch_num,
                    "chapter_title": ch_title,
                    "section_code": sec_code,
                    "title": sec_title,
                    "section_type": type_info["section_type"],
                    "is_special_feature": type_info["is_special_feature"],
                    "printed_pages": f"{start_pg}–{end_pg}",
                    "start_page": start_pg,
                    "end_page": end_pg,
                    "pdf_file": str(pdf_out_path),
                    "hierarchy_pdf_file": str(hier_pdf_path),
                    "md_file": str(md_out_path),
                    "word_count": word_count,
                    "printed_main_idea": spread_data["printed_main_idea"],
                    "subheadings": [
                        {"title": sh["title"], "page": sh["page"], "paragraph_count": len(sh.get("paragraphs", []))}
                        for sh in spread_data["subheadings"]
                    ],
                    "historical_thinking": spread_data["historical_thinking"],
                    "critical_viewing": spread_data["critical_viewing"],
                    "official_vocab": sec_vocab,
                })

    CATALOG_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    CHAPTER_REVIEWS_PATH.write_text(json.dumps(chapter_reviews, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Compiled {len(catalog)} two-page English sections across {len(chapter_reviews)} chapters.")
    return catalog


if __name__ == "__main__":
    run_cengage_compiler()
