"""
8th Grade U.S. History (English) — Curriculum Design Studio
National Geographic: American Stories (Beginnings to 1877)

Features a 2-Path Guided Wizard:
  1. Modular Curriculum Packet Builder (Dynamic Horizontal Page Tray, Scope Chooser, Presets, Cover & Footer options)
  2. Standalone Strategy Worksheet Gallery (All-in-One Visual Thumbnail Grid across 18 strategies, Side-by-Side Review)

Exports directly to 100% Vector Print-Ready PDFs (Letter size) and synchronized Google Drive folders.
"""

import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

import streamlit as st

from src.strategy_bank import (
    CENTRAL_IDEA_STRATEGIES,
    PRINTED_MAIN_IDEA_MODES,
    READING_ORGANIZERS,
    VOCAB_MODES,
    READING_MODES,
    COVER_PAGE_MODES,
    GRADE_BOX_MODES,
    OPTIONAL_TWR_STRATEGIES,
    CHAPTER_STANDARDS_MAP,
    get_strategy_by_code,
)
from src.blueprint_designer import (
    load_all_blueprints,
    get_chapter_blueprint,
    save_chapter_blueprint,
    recommend_section_strategies,
)
from src.packet_builder import (
    generate_section_packet,
    build_standalone_strategy_handout,
    build_chapter_student_booklet,
    build_chapter_master_teacher_plan,
    build_chapter_review_and_assessment,
    build_custom_modular_packet,
)
from src.strategy_thumbnails import (
    ALL_STRATEGY_TILES,
    get_tile_by_code,
)
from pdf_exporter import (
    html_to_pdf_bytes,
    create_pdf_bundle_zip,
    upload_pdf_to_google_drive,
    upload_packet_bundle_to_google_drive,
    get_target_multi_section_folder,
    get_target_custom_units_folder,
)
from doc_exporter import (
    ROOT_FOLDER_NAME,
    TEMP_DOCS_DIR,
    get_gdrive_service,
    get_target_chapter_folder,
    get_target_section_folder,
    grant_file_permissions,
    build_docx_file,
    get_docx_bytes,
)
from src.preview_renderer import (
    render_preview_handout,
    render_preview_exemplar,
    render_preview_scaffold,
    render_preview_cover,
    render_preview_footer,
    format_booklet_for_web,
)

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION & MODERN RESPONSIVE STYLING
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="8th Grade U.S. History Curriculum Studio",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    /* Hide Streamlit header, deploy button, toolbar, and hamburger menu */
    header,
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    .stAppToolbar,
    .stAppDeployButton,
    [data-testid="stAppDeployButton"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    footer {
        visibility: hidden !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1400px !important;
    }

    /* Top Banner Styling */
    .top-thin-bar {
        background: #0f172a;
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        margin-bottom: 1.0rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
    }
    .top-thin-bar h2 {
        color: white !important;
        font-size: 1.25rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Navigation Breadcrumbs */
    .breadcrumb-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 0.5rem 1.0rem;
        margin-bottom: 1.0rem;
    }
    .breadcrumb-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e3a8a;
    }

    /* Hero Pathway Cards */
    .hero-card {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem 1.4rem 1.0rem 1.4rem;
        min-height: 190px;
        display: block;
        text-decoration: none !important;
        color: inherit !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        margin-bottom: 0.75rem;
    }
    .hero-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px -3px rgba(15, 23, 42, 0.10);
    }
    .hero-blue {
        border-top: 5px solid #2563eb !important;
        background: linear-gradient(180deg, #eff6ff 0%, #ffffff 42%);
    }
    .hero-blue:hover {
        border-color: #93c5fd;
        border-top: 5px solid #1d4ed8 !important;
    }
    .hero-indigo {
        border-top: 5px solid #6366f1 !important;
        background: linear-gradient(180deg, #eef2ff 0%, #ffffff 42%);
    }
    .hero-indigo:hover {
        border-color: #c7d2fe;
        border-top: 5px solid #4f46e5 !important;
    }
    .hero-teal {
        border-top: 5px solid #0d9488 !important;
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 42%);
    }
    .hero-teal:hover {
        border-color: #99f6e4;
        border-top: 5px solid #0f766e !important;
    }
    .hero-title {
        font-size: 1.20rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.45rem;
        line-height: 1.3;
        display: block;
    }
    .hero-desc {
        font-size: 0.90rem;
        color: #475569;
        line-height: 1.45;
        margin-bottom: 0.75rem;
        display: block;
    }

    /* Horizontal Page Tray Styling */
    .tray-container {
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 10px;
        padding: 0.85rem 1.0rem;
        margin-bottom: 1.25rem;
    }
    .tray-header {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #475569;
        margin-bottom: 0.65rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .page-chip-box {
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        padding: 0.6rem 0.75rem;
        text-align: center;
        min-height: 68px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .page-chip-active {
        border-color: #1e3a8a !important;
        background: #eff6ff !important;
        box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.25) !important;
    }

    /* Badges & Pills */
    .badge-pill {
        display: inline-block;
        padding: 0.20rem 0.65rem;
        border-radius: 999px;
        font-size: 0.80rem;
        font-weight: 600;
        background: #dbeafe;
        color: #1e3a8a;
        margin-right: 0.35rem;
    }
    .badge-scaf {
        background: #fef3c7;
        color: #92400e;
    }
    .badge-gray {
        background: #f1f5f9;
        color: #475569;
    }

    /* Visual Strategy Grid Cards */
    .visual-grid-card {
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        border-radius: 10px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        transition: all 0.15s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 245px;
    }
    .visual-grid-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    .visual-grid-card-selected {
        border: 2px solid #1e3a8a !important;
        background: #f0f7ff !important;
        box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.3) !important;
    }

    /* Action Buttons (Strictly zero emojis) */
    div.stDownloadButton > button:not([kind="primary"]),
    div.stDownloadButton > button:first-child:not([kind="primary"]) {
        background-color: #f8fafc !important;
        color: #1e3a8a !important;
        border: 2px solid #1e3a8a !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 2px 4px rgba(30, 58, 138, 0.08) !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    div.stDownloadButton > button:not([kind="primary"]):hover {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.22) !important;
        transform: translateY(-1px) !important;
    }
    div.stDownloadButton > button:not([kind="primary"]):hover p {
        color: #ffffff !important;
    }

    div.stDownloadButton > button[kind="primary"],
    div.stDownloadButton > button[data-testid="baseButton-primary"],
    div.stDownloadButton > button[data-testid="stBaseButton-primary"] {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border: 2px solid #172554 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 2px 4px rgba(30, 58, 138, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    div.stDownloadButton > button[kind="primary"]:hover {
        background-color: #172554 !important;
        border-color: #0f172a !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.38) !important;
        transform: translateY(-1px) !important;
    }

    /* Google Drive Action Buttons */
    button[aria-label*="Google Drive"],
    button[aria-label*="google drive"],
    .gdrive-action-btn button {
        background-color: #1e40af !important;
        color: #ffffff !important;
        border: 1.5px solid #1d4ed8 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 2px 4px rgba(30, 64, 175, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    button[aria-label*="Google Drive"]:hover,
    button[aria-label*="google drive"]:hover,
    .gdrive-action-btn button:hover {
        background-color: #1e3a8a !important;
        border-color: #172554 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(30, 64, 175, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* General Primary Action Buttons */
    div.stButton > button[kind="primary"]:not([aria-label*="Google Drive"]),
    div.stButton > button[data-testid="baseButton-primary"]:not([aria-label*="Google Drive"]),
    div.stButton > button[data-testid="stBaseButton-primary"]:not([aria-label*="Google Drive"]),
    button[kind="primary"]:not([aria-label*="Google Drive"]) {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border: 2px solid #172554 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 2px 4px rgba(30, 58, 138, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    div.stButton > button[kind="primary"]:not([aria-label*="Google Drive"]):hover,
    button[kind="primary"]:not([aria-label*="Google Drive"]):hover {
        background-color: #172554 !important;
        border-color: #0f172a !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        margin-bottom: 0.85rem !important;
    }
    div[data-testid="stExpander"] details summary {
        font-weight: 700 !important;
        color: #0f172a !important;
        font-size: 0.94rem !important;
        padding: 0.65rem 0.85rem !important;
        background-color: #f8fafc !important;
    }
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        background-color: #ffffff !important;
        padding: 1rem !important;
    }
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] span,
    div[data-testid="stExpander"] label,
    div[data-testid="stExpander"] li {
        color: #1e293b !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADERS & HELPERS
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_catalog() -> List[Dict[str, Any]]:
    cat_path = Path("output/catalog.json")
    if not cat_path.exists():
        return []
    return json.loads(cat_path.read_text(encoding="utf-8"))


@st.cache_data
def load_vocab_index() -> Dict[str, Any]:
    vp = Path("output/vocab_index.json")
    if not vp.exists():
        return {}
    return json.loads(vp.read_text(encoding="utf-8"))


@st.cache_data
def load_chapter_reviews() -> Dict[str, Any]:
    rp = Path("output/chapter_reviews.json")
    if not rp.exists():
        return {}
    return json.loads(rp.read_text(encoding="utf-8"))


def resolve_file_path(path_str: Optional[str]) -> Path:
    """Safely resolves file paths across Windows and Linux (Streamlit Cloud)."""
    if not path_str:
        return Path("")
    clean = str(path_str).replace("\\", "/")
    p = Path(clean)
    if p.exists():
        return p
    root_p = Path(__file__).resolve().parent / clean
    if root_p.exists():
        return root_p
    return p


def render_clean_html(html_str: str) -> None:
    """
    Safely renders HTML in Streamlit by collapsing inter-tag newlines and leading indentation.
    Guarantees CommonMark/Markdown never coerces indented HTML or empty conditional lines into <pre><code> blocks.
    """
    clean = re.sub(r">\s*\n\s*<", "><", html_str.strip())
    clean = re.sub(r"\n\s*", " ", clean)
    st.markdown(clean, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CLOUD SECRETS & PASSCODE AUTHENTICATION GATE
# ─────────────────────────────────────────────────────────────────────────────

try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass


@st.cache_resource(show_spinner=False)
def ensure_playwright_ready():
    """Installs Playwright Chromium browser binaries on cloud startup."""
    import subprocess
    import sys
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
    except Exception as e:
        logger.info(f"Playwright cloud startup check: {e}")
    return True


ensure_playwright_ready()


@st.cache_data(show_spinner=False)
def compile_pdf_cached(html_content: str, title: str) -> bytes:
    """Caches compiled vector PDF bytes by HTML content hash to maximize performance and avoid redundant renders."""
    return html_to_pdf_bytes(html_content, title=title)


def verify_access() -> bool:
    """Passcode protection gate for secure multi-user and cloud access."""
    if st.session_state.get("authenticated", False):
        return True

    if st.query_params.get("auth") == "ok":
        st.session_state["authenticated"] = True
        return True

    expected = "HMS8thushistory"
    try:
        if "APP_PASSCODE" in st.secrets:
            expected = str(st.secrets["APP_PASSCODE"]).strip()
    except Exception:
        pass
    if "APP_PASSCODE" in os.environ:
        expected = os.environ["APP_PASSCODE"].strip()

    st.markdown(
        """
        <div style="max-width: 520px; margin: 3.5rem auto 1.5rem auto; text-align: center; background: #ffffff; padding: 2.25rem; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);">
            <div style="font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">
                8th Grade U.S. History Curriculum Studio
            </div>
            <div style="font-size: 0.92rem; color: #475569; margin-bottom: 0.25rem;">
                National Geographic: American Stories (Beginnings to 1877)
            </div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.75rem;">
                Enter your department access passcode to open the curriculum studio.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("teacher_login_form"):
            entered_code = st.text_input("Teacher Passcode", type="password", placeholder="Enter passcode...")
            login_btn = st.form_submit_button("Access Studio", use_container_width=True, type="primary")
            if login_btn:
                if entered_code and entered_code.strip() == expected:
                    st.session_state["authenticated"] = True
                    st.query_params["auth"] = "ok"
                    st.rerun()
                else:
                    st.error("Incorrect passcode. Please check your credentials.")
    return False


if not verify_access():
    st.stop()


catalog = load_catalog()
vocab_index = load_vocab_index()
chapter_reviews = load_chapter_reviews()

if not catalog:
    st.error("Textbook catalog (`output/catalog.json`) not found. Please run the compiler first.")
    st.stop()

# Group catalog by chapter
chapters_map: Dict[int, Dict[str, Any]] = {}
for item in catalog:
    cnum = item["chapter_num"]
    if cnum not in chapters_map:
        chapters_map[cnum] = {
            "chapter_num": cnum,
            "chapter_title": item["chapter_title"],
            "unit_num": item["unit_num"],
            "unit_title": item["unit_title"],
            "sections": [],
        }
    chapters_map[cnum]["sections"].append(item)

sorted_chapter_nums = sorted(chapters_map.keys())

# Initialize navigation session state
if "nav_view" not in st.session_state:
    st.session_state["nav_view"] = "home"
if "selected_ch_num" not in st.session_state:
    st.session_state["selected_ch_num"] = 5 if 5 in sorted_chapter_nums else sorted_chapter_nums[0]

# Direct navigation via query parameters
if "nav" in st.query_params:
    target_nav = str(st.query_params["nav"]).strip().lower()
    if target_nav in ["packet", "gallery", "home"]:
        st.session_state["nav_view"] = target_nav
    has_auth = st.query_params.get("auth") == "ok" or st.session_state.get("authenticated", False)
    try:
        del st.query_params["nav"]
    except Exception:
        pass
    if has_auth:
        st.query_params["auth"] = "ok"


# ─────────────────────────────────────────────────────────────────────────────
# 1. TOP BAR: CHAPTER SELECTOR, ESSENTIAL QUESTION & LOG OUT
# ─────────────────────────────────────────────────────────────────────────────

top_col1, top_col2 = st.columns([1.5, 1.2])

with top_col1:
    cur_ch = st.session_state["selected_ch_num"]
    cur_ch_idx = sorted_chapter_nums.index(cur_ch) if cur_ch in sorted_chapter_nums else 0

    def on_ch_change():
        st.session_state["selected_ch_num"] = st.session_state["top_ch_select"]

    st.selectbox(
        "Current Textbook Chapter:",
        options=sorted_chapter_nums,
        index=cur_ch_idx,
        format_func=lambda n: f"Chapter {n:02d}: {chapters_map[n]['chapter_title']} ({len(chapters_map[n]['sections'])} spreads)",
        key="top_ch_select",
        on_change=on_ch_change,
        label_visibility="collapsed",
    )

selected_ch_num = st.session_state["selected_ch_num"]
ch_info = chapters_map[selected_ch_num]
ch_sections = ch_info["sections"]
ch_std_info = CHAPTER_STANDARDS_MAP.get(str(selected_ch_num), CHAPTER_STANDARDS_MAP.get("5", {}))

with top_col2:
    tc_pill, tc_out = st.columns([3.2, 1])
    with tc_pill:
        render_clean_html(
            f"""
            <div style="text-align: right; padding-top: 0.25rem; white-space: nowrap;">
                <span class="badge-pill" style="font-size: 0.88rem; padding: 0.35rem 0.85rem;">
                    <b>Chapter {selected_ch_num:02d}:</b> {len(ch_sections)} Sections Available
                </span>
            </div>
            """
        )
    with tc_out:
        if st.button("Log Out", key="top_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

raw_unit = str(ch_info['unit_title'])
display_unit = raw_unit if raw_unit.lower().startswith("unit") else f"Unit {ch_info['unit_num']}: {raw_unit}"
eq_text = ch_std_info.get('essential_question', '')

banner_html = (
    '<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 5px solid #1e3a8a; border-radius: 8px; padding: 0.85rem 1.15rem; margin-bottom: 1.0rem; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap;">'
    '<div style="flex: 1.2; min-width: 200px;">'
    '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Curriculum Unit</div>'
    f'<div style="font-size: 0.95rem; font-weight: 600; color: #0f172a; line-height: 1.35;">{display_unit}</div>'
    '</div>'
    '<div style="width: 1.5px; height: 38px; background: #cbd5e1;"></div>'
    '<div style="flex: 2; min-width: 260px;">'
    '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Essential Question</div>'
    f'<div style="font-size: 0.88rem; font-style: italic; color: #1e293b; line-height: 1.4;">"{eq_text}"</div>'
    '</div>'
    '<div style="width: 1.5px; height: 38px; background: #cbd5e1;"></div>'
    '<div style="flex-shrink: 0;">'
    '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Google Drive Folder</div>'
    f'<div style="font-size: 0.82rem; background: #e2e8f0; padding: 0.35rem 0.75rem; border-radius: 6px; color: #0f172a; font-family: monospace; font-weight: 600; white-space: nowrap;">{ROOT_FOLDER_NAME}</div>'
    '</div>'
    '</div>'
)
render_clean_html(banner_html)


# ─────────────────────────────────────────────────────────────────────────────
# 2. SCREEN 0: THE GATEWAY (HOME SCREEN)
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state["nav_view"] == "home":
    st.markdown("### Curriculum Design Studio — What would you like to create today?")
    st.caption("Select one of the two primary pathways below to design print-ready materials for your 40-minute U.S. History class:")

    h_col1, h_col2 = st.columns(2)

    with h_col1:
        render_clean_html(
            """
            <a href="?nav=packet&auth=ok" target="_self" class="hero-card hero-blue">
                <span class="hero-title" style="color: #1d4ed8;">1. Modular Curriculum Packet Builder</span>
                <span class="hero-desc">
                    Assemble custom 2-page, 3-page, or chapter unit packets page-by-page. Dynamic Page Tray gives you complete modular control to mix active reading organizers, central idea synthesizers, writing extensions, vocabulary practice, or assessments. Exports directly to print-ready vector PDF.
                </span>
            </a>
            """
        )
        if st.button("Open Packet Builder ->", use_container_width=True, key="btn_hero_packet", type="primary"):
            st.session_state["nav_view"] = "packet"
            st.rerun()

    with h_col2:
        render_clean_html(
            """
            <a href="?nav=gallery&auth=ok" target="_self" class="hero-card hero-indigo">
                <span class="hero-title" style="color: #4338ca;">2. Standalone Strategy Worksheet Gallery</span>
                <span class="hero-desc">
                    Explore all 18 pedagogical strategy templates in an interactive visual thumbnail grid. Preview student worksheets with scaffolded support and authentic 8th-grade student exemplars grounded in any textbook section spread, then download vector PDFs or save directly to Google Drive.
                </span>
            </a>
            """
        )
        if st.button("Open Worksheet Gallery ->", use_container_width=True, key="btn_hero_gallery", type="primary"):
            st.session_state["nav_view"] = "gallery"
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# 3. PATH A: MODULAR CURRICULUM PACKET BUILDER
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "packet":

    # Breadcrumb Header
    b_col1, b_col2 = st.columns([1.2, 2.5])
    with b_col1:
        if st.button("<- Return to Main Menu", use_container_width=True, key="btn_back_packet"):
            st.session_state["nav_view"] = "home"
            st.rerun()
    with b_col2:
        render_clean_html(
            """
            <div style="text-align: right; padding-top: 0.2rem;">
                <span class="badge-pill" style="font-size: 0.88rem; padding: 0.35rem 0.85rem;">
                    <b>Pathway 1:</b> Modular Curriculum Packet Builder
                </span>
            </div>
            """
        )

    st.divider()

    # Initialize Page Tray state if not present
    if "tray_pages" not in st.session_state:
        # Default start: 2-page section spread for first section in active chapter
        default_sec = ch_sections[0] if ch_sections else None
        if default_sec:
            sec_p = resolve_file_path(default_sec.get("md_file"))
            sec_md = sec_p.read_text(encoding="utf-8") if sec_p.exists() else ""
            st.session_state["tray_pages"] = [
                {
                    "section_meta": default_sec,
                    "strategy_type": "reading_organizer",
                    "strategy_code": "read_01_cause_effect",
                    "is_scaffolded": False,
                    "raw_passage_md": sec_md,
                },
                {
                    "section_meta": default_sec,
                    "strategy_type": "central_idea",
                    "strategy_code": "ci_01_subheading_gist",
                    "is_scaffolded": False,
                    "raw_passage_md": sec_md,
                },
            ]
        else:
            st.session_state["tray_pages"] = []

    if "active_tray_idx" not in st.session_state:
        st.session_state["active_tray_idx"] = 0

    tray_pages = st.session_state["tray_pages"]
    if st.session_state["active_tray_idx"] >= len(tray_pages):
        st.session_state["active_tray_idx"] = max(0, len(tray_pages) - 1)
    active_idx = st.session_state["active_tray_idx"]

    # ── Step 1: Packet Scope & Mode Presets ──
    st.markdown("#### Step 1: Packet Scope & Mode Presets")
    sc_c1, sc_c2 = st.columns(2)
    with sc_c1:
        packet_scope = st.radio(
            "Packet Scope:",
            options=["Section Packet (Single Spread Focus)", "Chapter Packet (Unit Booklet)"],
            horizontal=True,
            key="packet_scope_radio",
        )
    with sc_c2:
        creation_mode = st.radio(
            "Configuration Mode:",
            options=["Pre-Built Presets (Recommended)", "Start from Scratch (Blank Canvas)"],
            horizontal=True,
            key="packet_mode_radio",
        )

    # If Pre-Built Presets is selected, offer 1-click preset buttons
    if creation_mode == "Pre-Built Presets (Recommended)":
        st.caption("Apply a pre-configured pedagogical structure to your dynamic page tray:")
        p_c1, p_c2, p_c3 = st.columns(3)

        with p_c1:
            if st.button("Quick 2-Page Section Spread", use_container_width=True, key="preset_2page"):
                sec_target = ch_sections[0] if ch_sections else None
                if sec_target:
                    sec_p = resolve_file_path(sec_target.get("md_file"))
                    sec_md = sec_p.read_text(encoding="utf-8") if sec_p.exists() else ""
                    st.session_state["tray_pages"] = [
                        {
                            "section_meta": sec_target,
                            "strategy_type": "reading_organizer",
                            "strategy_code": "read_01_cause_effect",
                            "is_scaffolded": False,
                            "raw_passage_md": sec_md,
                        },
                        {
                            "section_meta": sec_target,
                            "strategy_type": "central_idea",
                            "strategy_code": "ci_01_subheading_gist",
                            "is_scaffolded": False,
                            "raw_passage_md": sec_md,
                        },
                    ]
                    st.session_state["active_tray_idx"] = 0
                    st.session_state["include_cover_toggle"] = False
                    st.rerun()

        with p_c2:
            if st.button("3-Page Complete Lesson", use_container_width=True, key="preset_3page"):
                sec_target = ch_sections[0] if ch_sections else None
                if sec_target:
                    sec_p = resolve_file_path(sec_target.get("md_file"))
                    sec_md = sec_p.read_text(encoding="utf-8") if sec_p.exists() else ""
                    st.session_state["tray_pages"] = [
                        {
                            "section_meta": sec_target,
                            "strategy_type": "reading_organizer",
                            "strategy_code": "read_01_cause_effect",
                            "is_scaffolded": False,
                            "raw_passage_md": sec_md,
                        },
                        {
                            "section_meta": sec_target,
                            "strategy_type": "central_idea",
                            "strategy_code": "ci_01_subheading_gist",
                            "is_scaffolded": False,
                            "raw_passage_md": sec_md,
                        },
                        {
                            "section_meta": sec_target,
                            "strategy_type": "twr",
                            "strategy_code": "twr_01_because_but_so",
                            "is_scaffolded": False,
                            "raw_passage_md": sec_md,
                        },
                    ]
                    st.session_state["active_tray_idx"] = 0
                    st.session_state["include_cover_toggle"] = False
                    st.rerun()

        with p_c3:
            if st.button("Full Chapter Unit Booklet", use_container_width=True, key="preset_full_unit"):
                new_pages = []
                for s in ch_sections:
                    sec_p = resolve_file_path(s.get("md_file"))
                    sec_md = sec_p.read_text(encoding="utf-8") if sec_p.exists() else ""
                    new_pages.append({
                        "section_meta": s,
                        "strategy_type": "reading_organizer",
                        "strategy_code": "read_01_cause_effect",
                        "is_scaffolded": False,
                        "raw_passage_md": sec_md,
                    })
                    new_pages.append({
                        "section_meta": s,
                        "strategy_type": "central_idea",
                        "strategy_code": "ci_01_subheading_gist",
                        "is_scaffolded": False,
                        "raw_passage_md": sec_md,
                    })
                st.session_state["tray_pages"] = new_pages
                st.session_state["active_tray_idx"] = 0
                st.session_state["include_cover_toggle"] = True
                st.rerun()

    # ── Step 2: Dynamic Horizontal Page Tray ──
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("#### Step 2: Dynamic Page Tray — Configure Every Page")

    total_pages = len(tray_pages)
    total_sheets = (total_pages + 1) // 2

    # Render horizontal sequence
    tray_cols = st.columns(total_pages + 1 if total_pages > 0 else 1)

    for i, p in enumerate(tray_pages):
        with tray_cols[i]:
            is_active = (i == active_idx)
            card_class = "page-chip-box page-chip-active" if is_active else "page-chip-box"
            s_meta = p.get("section_meta", {})
            s_code = s_meta.get("section_code", "?")
            s_strat = p.get("strategy_code", "")
            tile_match = get_tile_by_code(s_strat)
            s_name = tile_match["name"] if tile_match else s_strat.replace("_", " ").title()
            scaf_badge = '<span class="badge-pill badge-scaf" style="font-size:0.65rem; padding:1px 4px;">Scaffolded</span>' if p.get("is_scaffolded") else ''

            btn_label = f"Page {i+1}: Sec {s_code}"
            if st.button(
                btn_label,
                key=f"tray_chip_btn_{i}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["active_tray_idx"] = i
                st.rerun()

            render_clean_html(
                f"""
                <div style="font-size: 0.76rem; text-align: center; color: #475569; margin-top: -0.3rem;">
                    <b>{s_name}</b> {scaf_badge}
                </div>
                """
            )

    # "+ Add Page" Slot
    with tray_cols[-1 if total_pages > 0 else 0]:
        if st.button("+ Add Page", key="btn_add_tray_page", use_container_width=True):
            # Append copy of last page or default to current chapter's section
            fallback_sec = ch_sections[0] if ch_sections else {}
            sec_target = tray_pages[-1]["section_meta"] if tray_pages else fallback_sec
            sec_p = resolve_file_path(sec_target.get("md_file"))
            sec_md = sec_p.read_text(encoding="utf-8") if sec_p.exists() else ""
            st.session_state["tray_pages"].append({
                "section_meta": sec_target,
                "strategy_type": "central_idea",
                "strategy_code": "ci_01_subheading_gist",
                "is_scaffolded": False,
                "raw_passage_md": sec_md,
            })
            st.session_state["active_tray_idx"] = len(st.session_state["tray_pages"]) - 1
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # ── Active Page Editor Container ──
    if tray_pages and 0 <= active_idx < len(tray_pages):
        active_p = tray_pages[active_idx]

        with st.container(border=True):
            render_clean_html(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #1e3a8a;">
                        Editing Page {active_idx + 1} of {total_pages}
                    </div>
                    <div>
                        <span class="badge-pill badge-gray">Total Packet: {total_pages} pgs ({total_sheets} sheets)</span>
                    </div>
                </div>
                """
            )

            ed_c1, ed_c2 = st.columns(2)

            with ed_c1:
                st.markdown("##### 1. Section Spread Selection")
                cur_page_ch = active_p["section_meta"].get("chapter_num", selected_ch_num)
                ch_choice = st.selectbox(
                    "Chapter:",
                    options=sorted_chapter_nums,
                    index=sorted_chapter_nums.index(cur_page_ch) if cur_page_ch in sorted_chapter_nums else 0,
                    format_func=lambda n: f"Chapter {n:02d}: {chapters_map[n]['chapter_title']}",
                    key=f"ed_page_ch_{active_idx}",
                )
                avail_secs = chapters_map[ch_choice]["sections"]
                cur_sec_code = str(active_p["section_meta"].get("section_code", ""))
                sec_indices = [str(s["section_code"]) for s in avail_secs]
                sec_default_idx = sec_indices.index(cur_sec_code) if cur_sec_code in sec_indices else 0

                sec_choice = st.selectbox(
                    "Section Spread:",
                    options=avail_secs,
                    index=sec_default_idx,
                    format_func=lambda s: f"Sec. {s['section_code']}: {s['title']} (pp. {s['printed_pages']})",
                    key=f"ed_page_sec_{active_idx}",
                )
                active_p["section_meta"] = sec_choice
                sec_p = resolve_file_path(sec_choice.get("md_file"))
                active_p["raw_passage_md"] = sec_p.read_text(encoding="utf-8") if sec_p.exists() else ""

            with ed_c2:
                st.markdown("##### 2. Strategy & Text Structure")
                cat_options = [
                    ("Active Reading Graphic Organizer", "reading_organizer"),
                    ("Central Idea Synthesis", "central_idea"),
                    ("Anti-Copycat (Textbook Main Idea)", "anti_copycat"),
                    ("Writing Extension (The Writing Revolution)", "twr"),
                    ("Vocabulary Practice", "vocab"),
                    ("Section Assessment & Reading Checks", "assessment"),
                ]
                cat_labels = [c[0] for c in cat_options]
                cat_values = [c[1] for c in cat_options]
                cur_cat = active_p.get("strategy_type", "central_idea")
                cat_idx = cat_values.index(cur_cat) if cur_cat in cat_values else 0

                sel_cat_label = st.selectbox(
                    "Strategy Category:",
                    options=cat_labels,
                    index=cat_idx,
                    key=f"ed_page_cat_{active_idx}",
                )
                sel_cat = cat_values[cat_labels.index(sel_cat_label)]
                active_p["strategy_type"] = sel_cat

                # Select strategy within category
                if sel_cat == "reading_organizer":
                    strat_opts = [r["code"] for r in READING_ORGANIZERS]
                    strat_names = {r["code"]: r["name"] for r in READING_ORGANIZERS}
                elif sel_cat == "central_idea":
                    strat_opts = [s["code"] for s in CENTRAL_IDEA_STRATEGIES]
                    strat_names = {s["code"]: s["name"] for s in CENTRAL_IDEA_STRATEGIES}
                elif sel_cat == "anti_copycat":
                    strat_opts = [m["code"] for m in PRINTED_MAIN_IDEA_MODES]
                    strat_names = {m["code"]: m["name"] for m in PRINTED_MAIN_IDEA_MODES}
                elif sel_cat == "twr":
                    twr_sub = [t for t in OPTIONAL_TWR_STRATEGIES if t["code"] != "twr_none"]
                    strat_opts = [t["code"] for t in twr_sub]
                    strat_names = {t["code"]: t["name"] for t in twr_sub}
                elif sel_cat == "vocab":
                    strat_opts = ["vocab_deep_dive"]
                    strat_names = {"vocab_deep_dive": "Vocabulary Practice (Context Clues & Cloze)"}
                else:
                    strat_opts = ["section_assessment"]
                    strat_names = {"section_assessment": "Section Check & Quiz (Textbook Questions)"}

                cur_strat = active_p.get("strategy_code", strat_opts[0])
                strat_idx = strat_opts.index(cur_strat) if cur_strat in strat_opts else 0
                sel_strat = st.selectbox(
                    "Specific Strategy Model:",
                    options=strat_opts,
                    index=strat_idx,
                    format_func=lambda c: strat_names.get(c, c),
                    key=f"ed_page_strat_{active_idx}",
                )
                active_p["strategy_code"] = sel_strat

            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            scaf_checked = st.checkbox(
                "Scaffolded Support Edition for this page (sentence starters, word banks, paragraph frames)",
                value=active_p.get("is_scaffolded", False),
                key=f"ed_page_scaf_{active_idx}",
            )
            active_p["is_scaffolded"] = scaf_checked

            # Page management buttons
            ctrl_c1, ctrl_c2, ctrl_c3, ctrl_c4 = st.columns([1, 1, 1, 1.5])
            with ctrl_c1:
                if active_idx > 0:
                    if st.button("<- Move Left", use_container_width=True, key=f"btn_left_{active_idx}"):
                        tray_pages[active_idx - 1], tray_pages[active_idx] = tray_pages[active_idx], tray_pages[active_idx - 1]
                        st.session_state["active_tray_idx"] = active_idx - 1
                        st.rerun()
            with ctrl_c2:
                if active_idx < len(tray_pages) - 1:
                    if st.button("Move Right ->", use_container_width=True, key=f"btn_right_{active_idx}"):
                        tray_pages[active_idx + 1], tray_pages[active_idx] = tray_pages[active_idx], tray_pages[active_idx + 1]
                        st.session_state["active_tray_idx"] = active_idx + 1
                        st.rerun()
            with ctrl_c3:
                if len(tray_pages) > 1:
                    if st.button("Delete Page", use_container_width=True, key=f"btn_del_{active_idx}"):
                        tray_pages.pop(active_idx)
                        st.session_state["active_tray_idx"] = max(0, active_idx - 1)
                        st.rerun()

    # ── Step 3: Packet-Level Options (Cover & Footer) ──
    with st.expander("Packet-Level Options: Cover Page & Footer Style (Optional)", expanded=False):
        opt_c1, opt_c2 = st.columns(2)
        with opt_c1:
            include_cov = st.checkbox(
                "Include Front Cover Page (Cumulative Unit Study Guide)",
                value=st.session_state.get("include_cover_toggle", False),
                key="include_cover_toggle",
            )
            cover_style_opts = [
                ("Central Idea Study Guide Tracker (Recommended)", "central_idea_tracker"),
                ("Section Score & Stamp Table", "score_checklist"),
            ]
            cover_mode_choice = st.selectbox(
                "Cover Page Format:",
                options=[c[1] for c in cover_style_opts],
                format_func=lambda c: [x[0] for x in cover_style_opts if x[1] == c][0],
                key="cover_style_select",
                disabled=not include_cov,
            )
        with opt_c2:
            footer_opts = [
                ("Section Points Stamp Box (____/100)", "gb_01_points_stamp"),
                ("Blank Score Line (Score: _____)", "gb_02_blank_score"),
                ("Page Numbers Only", "none"),
            ]
            footer_mode_choice = st.selectbox(
                "Page Footer Style:",
                options=[f[1] for f in footer_opts],
                format_func=lambda f: [x[0] for x in footer_opts if x[1] == f][0],
                key="footer_style_select",
            )

    # ── Step 4: Real-Time Packet Compilation ──
    with st.spinner("Compiling modular packet and rendering letter-size vector PDFs..."):
        modular_result = build_custom_modular_packet(
            pages_config=tray_pages,
            include_cover=st.session_state.get("include_cover_toggle", False),
            cover_mode=st.session_state.get("cover_style_select", "central_idea_tracker"),
            footer_mode=st.session_state.get("footer_style_select", "gb_01_points_stamp"),
        )

    base_name = modular_result["base_filename"]
    student_pdf = modular_result["student_pdf_bytes"]
    teacher_pdf = modular_result["teacher_pdf_bytes"]
    bundle_zip = modular_result["bundle_zip_bytes"]
    total_pkt_pages = modular_result["total_pages"]

    # ── Step 5: 1-Click Exports & Google Drive Synchronization ──
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("#### Step 3: Print, Download & Google Drive Export")
    st.caption("Download letter-size vector PDFs or synchronize both copies directly to Google Drive:")

    if student_pdf and teacher_pdf and bundle_zip:
        dl_c1, dl_c2, dl_c3, dl_c4 = st.columns([1.5, 1.2, 1.2, 1.6])

        with dl_c1:
            st.download_button(
                "Download Complete Bundle (.zip)",
                data=bundle_zip,
                file_name=f"{base_name}_Complete_Bundle.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True,
                help="Contains both the Student Packet PDF and the matching Teacher Answer Key PDF in a single file.",
            )

        with dl_c2:
            st.download_button(
                "Download Student PDF",
                data=student_pdf,
                file_name=f"{base_name}_Student.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with dl_c3:
            st.download_button(
                "Download Teacher Key PDF",
                data=teacher_pdf,
                file_name=f"{base_name}_Teacher_Key.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with dl_c4:
            if st.button("Save Both to Google Drive (PDFs)", use_container_width=True, key="btn_gdrive_packet"):
                with st.spinner("Connecting to Google Drive and uploading packet bundle..."):
                    try:
                        drive_service = get_gdrive_service()
                        if not drive_service:
                            st.error("Google Drive API service could not be initialized. Please check credentials or token.")
                        else:
                            is_single = modular_result["is_single_section"]
                            p_ch_num = modular_result["primary_chapter_num"]
                            p_ch_title = modular_result["primary_chapter_title"]
                            p_sec_code = modular_result["primary_section_code"]
                            p_sec_title = modular_result["primary_section_title"]

                            if is_single:
                                target_f_id, target_f_path, _ = get_target_section_folder(
                                    drive_service,
                                    chapter_num=p_ch_num,
                                    chapter_title=p_ch_title,
                                    section_code=p_sec_code,
                                    section_title=p_sec_title,
                                )
                            elif len(set(p["section_meta"].get("chapter_num") for p in tray_pages)) == 1:
                                target_f_id, target_f_path, _ = get_target_multi_section_folder(
                                    drive_service,
                                    chapter_num=p_ch_num,
                                    chapter_title=p_ch_title,
                                )
                            else:
                                target_f_id, target_f_path, _ = get_target_custom_units_folder(drive_service)

                            upload_res = upload_packet_bundle_to_google_drive(
                                service=drive_service,
                                student_pdf_bytes=student_pdf,
                                student_filename=f"{base_name}_Student.pdf",
                                teacher_pdf_bytes=teacher_pdf,
                                teacher_filename=f"{base_name}_Teacher_Answer_Key.pdf",
                                parent_folder_id=target_f_id,
                                folder_path_display=target_f_path,
                            )

                            s_link = upload_res["student"]["link"]
                            t_link = upload_res["teacher"]["link"]
                            st.success(
                                f"**Uploaded successfully to Google Drive!**\n\n"
                                f"- Destination Folder: `{target_f_path}`\n"
                                f"- Student Packet: [View PDF in Google Drive]({s_link})\n"
                                f"- Teacher Answer Key: [View PDF in Google Drive]({t_link})"
                            )
                    except Exception as ex:
                        logger.error(f"Google Drive upload error: {ex}", exc_info=True)
                        st.error(f"Google Drive synchronization encountered an issue: {ex}")
    else:
        st.info("PDF compilation is initializing. You can review the complete interactive previews below immediately or print directly via your browser (Ctrl+P / Cmd+P).")

    # ── Step 6: Live Multi-Page Preview ──
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("#### Step 4: Live Multi-Page Preview")

    preview_tab1, preview_tab2 = st.tabs([
        f"Student Packet Preview ({total_pkt_pages} Pages)",
        "Teacher Answer Key Preview",
    ])

    with preview_tab1:
        st.markdown(modular_result["student_packet_html"], unsafe_allow_html=True)

    with preview_tab2:
        st.markdown(modular_result["teacher_key_html"], unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 4. PATH B: STANDALONE STRATEGY WORKSHEET GALLERY
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "gallery":

    # Breadcrumb Header
    b_col1, b_col2 = st.columns([1.2, 2.5])
    with b_col1:
        if st.button("<- Return to Main Menu", use_container_width=True, key="btn_back_gallery"):
            st.session_state["nav_view"] = "home"
            st.rerun()
    with b_col2:
        render_clean_html(
            """
            <div style="text-align: right; padding-top: 0.2rem;">
                <span class="badge-pill" style="font-size: 0.88rem; padding: 0.35rem 0.85rem;">
                    <b>Pathway 2:</b> Standalone Strategy Worksheet Gallery
                </span>
            </div>
            """
        )

    st.divider()

    # ── Step 1: Select Textbook Context ──
    st.markdown("#### Step 1: Select Textbook Chapter & Section Spread")

    gal_c_ch, gal_c_sec = st.columns([1.2, 2.0])
    with gal_c_ch:
        gal_ch_idx = sorted_chapter_nums.index(selected_ch_num) if selected_ch_num in sorted_chapter_nums else 0
        gal_ch_num = st.selectbox(
            "Textbook Chapter:",
            options=sorted_chapter_nums,
            index=gal_ch_idx,
            format_func=lambda n: f"Chapter {n:02d}: {chapters_map[n]['chapter_title']}",
            key="gal_select_ch",
        )
    gal_ch_sections = chapters_map[gal_ch_num]["sections"]

    with gal_c_sec:
        gal_selected_sec = st.selectbox(
            "Section Spread to Practice:",
            options=gal_ch_sections,
            format_func=lambda s: f"Sec. {s['section_code']}: {s['title']} (pp. {s['printed_pages']}) — [{s.get('section_type', 'Core Narrative')}]",
            key=f"gal_select_sec_{gal_ch_num}",
        )

    gal_sec_code = str(gal_selected_sec["section_code"])
    gal_md_path = resolve_file_path(gal_selected_sec.get("md_file"))
    gal_raw_md = gal_md_path.read_text(encoding="utf-8") if gal_md_path.exists() else ""

    # Section Context Card
    sec_vocab = gal_selected_sec.get("official_vocab", [])
    vocab_summary = ", ".join([v["word"] for v in sec_vocab[:5]]) if sec_vocab else "None listed"
    if len(sec_vocab) > 5:
        vocab_summary += f" (+{len(sec_vocab) - 5} more)"

    render_clean_html(
        f"""
        <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1.15rem; margin-bottom: 1.0rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em;">Active Section Spread</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a;">Sec. {gal_sec_code}: {gal_selected_sec['title']} (pp. {gal_selected_sec['printed_pages']})</div>
                </div>
                <div style="text-align: right;">
                    <span class="badge-pill">{gal_selected_sec.get('section_type', 'Core Narrative')}</span>
                    <span class="badge-pill">{gal_selected_sec.get('word_count', 0)} Words</span>
                </div>
            </div>
            <div style="margin-top: 0.45rem; font-size: 0.84rem; color: #334155;">
                <b>Textbook Main Idea:</b> <i>"{gal_selected_sec.get('printed_main_idea', 'None listed')}"</i>
            </div>
            <div style="margin-top: 0.25rem; font-size: 0.84rem; color: #334155;">
                <b>Official Vocabulary:</b> {vocab_summary}
            </div>
        </div>
        """
    )

    # ── Step 2: All-in-One Visual Strategy Grid ──
    st.markdown("#### Step 2: All-in-One Visual Strategy Grid — Choose a Worksheet Layout")
    st.caption("Select any template card below to generate a focused 1-page worksheet and authentic student exemplar grounded in this section:")

    category_filter = st.radio(
        "Filter by Pedagogical Category:",
        options=[
            "All Strategies (18)",
            "Central Idea (4)",
            "Anti-Copycat (3)",
            "Active Reading (5)",
            "The Writing Revolution (4)",
            "Vocabulary & Assessment (2)",
        ],
        horizontal=True,
        key="gal_cat_filter_radio",
    )

    if "All" in category_filter:
        filtered_tiles = ALL_STRATEGY_TILES
    elif "Central Idea" in category_filter:
        filtered_tiles = [t for t in ALL_STRATEGY_TILES if t["category"] == "Central Idea"]
    elif "Anti-Copycat" in category_filter:
        filtered_tiles = [t for t in ALL_STRATEGY_TILES if t["category"] == "Anti-Copycat"]
    elif "Active Reading" in category_filter:
        filtered_tiles = [t for t in ALL_STRATEGY_TILES if t["category"] == "Active Reading"]
    elif "Writing Revolution" in category_filter:
        filtered_tiles = [t for t in ALL_STRATEGY_TILES if t["category"] == "The Writing Revolution"]
    else:
        filtered_tiles = [t for t in ALL_STRATEGY_TILES if t["category"] in ["Vocabulary", "Assessment"]]

    if "gal_active_tile_code" not in st.session_state:
        st.session_state["gal_active_tile_code"] = "ci_01_subheading_gist"

    active_tile_code = st.session_state["gal_active_tile_code"]

    # Render responsive 3-column visual card grid
    grid_cols_per_row = 3
    for row_start in range(0, len(filtered_tiles), grid_cols_per_row):
        row_tiles = filtered_tiles[row_start : row_start + grid_cols_per_row]
        cols = st.columns(grid_cols_per_row)

        for col_idx, tile in enumerate(row_tiles):
            with cols[col_idx]:
                is_sel = (tile["code"] == active_tile_code)
                border_style = "border: 2.5px solid #1e3a8a; background: #f0f7ff;" if is_sel else "border: 1px solid #cbd5e1; background: #ffffff;"
                sel_badge_html = '<span style="font-size: 0.72rem; font-weight: 700; color: #1e3a8a;">Selected</span>' if is_sel else ''
                clean_thumb = re.sub(r">\s*\n\s*<", "><", re.sub(r"\n\s*", " ", tile["thumbnail_svg"].strip()))

                card_html = (
                    f'<div style="{border_style} border-radius: 10px; padding: 0.75rem; margin-bottom: 0.6rem; min-height: 255px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">'
                    f'<div>'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">'
                    f'<span class="badge-pill" style="font-size: 0.72rem; padding: 0.15rem 0.5rem;">{tile["category"]}</span>'
                    f'{sel_badge_html}'
                    f'</div>'
                    f'<div style="font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-bottom: 0.2rem;">{tile["name"]}</div>'
                    f'<div style="font-size: 0.78rem; color: #64748b; margin-bottom: 0.5rem;">{tile["subtitle"]}</div>'
                    f'<div style="margin-bottom: 0.5rem;">{clean_thumb}</div>'
                    f'</div>'
                    f'<div style="font-size: 0.76rem; color: #334155; margin-top: 0.35rem; line-height: 1.35;"><b>Target:</b> {tile["best_for"]}</div>'
                    f'</div>'
                )

                render_clean_html(card_html)

                if st.button(
                    "Selected Layout" if is_sel else "Select This Layout",
                    key=f"btn_tile_{tile['code']}",
                    use_container_width=True,
                    type="primary" if is_sel else "secondary",
                ):
                    st.session_state["gal_active_tile_code"] = tile["code"]
                    st.rerun()

    # ── Step 3: Worksheet Settings & Live Side-by-Side Review ──
    active_tile = get_tile_by_code(active_tile_code) or ALL_STRATEGY_TILES[0]
    cat_lookup = {
        "Central Idea": "central_idea",
        "Anti-Copycat": "anti_copycat",
        "Active Reading": "reading_organizer",
        "The Writing Revolution": "twr",
        "Vocabulary": "vocab",
        "Assessment": "assessment",
    }
    active_cat_key = cat_lookup.get(active_tile["category"], "central_idea")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"#### Step 3: Live Preview & Export — {active_tile['name']}")

    ws_opt_c1, ws_opt_c2 = st.columns([1.5, 2.5])
    with ws_opt_c1:
        is_scaf_ws = st.checkbox(
            "Generate Scaffolded Support Edition (sentence stems, word banks)",
            value=st.session_state.get("gal_scaf_toggle", False),
            key="gal_scaf_toggle",
        )

    # Build focused handout
    handout_data = build_standalone_strategy_handout(
        section_meta=gal_selected_sec,
        strategy_category=active_cat_key,
        strategy_code=active_tile_code,
        markdown_text=gal_raw_md,
        is_scaffolded=is_scaf_ws,
    )

    std_md = handout_data["student_standard_md"]
    scaf_md = handout_data["student_scaffolded_md"]
    ex_md = handout_data["exemplar_md"]

    active_student_md = scaf_md if is_scaf_ws else std_md
    student_html = format_booklet_for_web(active_student_md)
    teacher_html = format_booklet_for_web(ex_md)

    try:
        student_pdf_bytes = compile_pdf_cached(student_html, title=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Student")
        teacher_pdf_bytes = compile_pdf_cached(teacher_html, title=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Exemplar")
        single_bundle_zip = create_pdf_bundle_zip({
            f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Student.pdf": student_pdf_bytes,
            f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Teacher_Key.pdf": teacher_pdf_bytes,
        })
    except Exception as pdf_err:
        logger.warning(f"Could not compile standalone worksheet PDFs: {pdf_err}")
        student_pdf_bytes = b""
        teacher_pdf_bytes = b""
        single_bundle_zip = b""

    # Download & Google Drive Action Bar
    if student_pdf_bytes and teacher_pdf_bytes and single_bundle_zip:
        w_dl1, w_dl2, w_dl3, w_dl4 = st.columns([1.3, 1.3, 1.3, 1.6])
        with w_dl1:
            st.download_button(
                "Download Student PDF",
                data=student_pdf_bytes,
                file_name=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Student.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
        with w_dl2:
            st.download_button(
                "Download Exemplar PDF",
                data=teacher_pdf_bytes,
                file_name=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Exemplar.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with w_dl3:
            st.download_button(
                "Download Both (.zip)",
                data=single_bundle_zip,
                file_name=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Bundle.zip",
                mime="application/zip",
                use_container_width=True,
            )
        with w_dl4:
            if st.button("Save to Google Drive (PDFs)", use_container_width=True, key="btn_gdrive_gallery"):
                with st.spinner("Uploading worksheet & exemplar to Google Drive..."):
                    try:
                        drive_service = get_gdrive_service()
                        if not drive_service:
                            st.error("Google Drive API service could not be initialized.")
                        else:
                            ch_title = chapters_map[gal_ch_num]["chapter_title"]
                            target_f_id, target_f_path, _ = get_target_section_folder(
                                drive_service,
                                chapter_num=gal_ch_num,
                                chapter_title=ch_title,
                                section_code=gal_sec_code,
                                section_title=gal_selected_sec["title"],
                            )
                            upload_res = upload_packet_bundle_to_google_drive(
                                service=drive_service,
                                student_pdf_bytes=student_pdf_bytes,
                                student_filename=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Student.pdf",
                                teacher_pdf_bytes=teacher_pdf_bytes,
                                teacher_filename=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Teacher_Key.pdf",
                                parent_folder_id=target_f_id,
                                folder_path_display=target_f_path,
                            )
                            s_link = upload_res["student"]["link"]
                            t_link = upload_res["teacher"]["link"]
                            st.success(
                                f"**Saved to Google Drive!**\n\n"
                                f"- Destination: `{target_f_path}`\n"
                                f"- Student Handout: [View PDF in Drive]({s_link})\n"
                                f"- Teacher Answer Key: [View PDF in Drive]({t_link})"
                            )
                    except Exception as ex:
                        logger.error(f"Google Drive upload error: {ex}", exc_info=True)
                        st.error(f"Google Drive synchronization encountered an issue: {ex}")
    else:
        st.info("PDF compilation is initializing. You can review the complete interactive previews below immediately or print directly via your browser (Ctrl+P / Cmd+P).")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Preview Tabs
    ws_tab1, ws_tab2, ws_tab3 = st.tabs([
        f"Student Handout Preview ({'Scaffolded' if is_scaf_ws else 'Standard'})",
        "Teacher Answer Key & Student Exemplar",
        "Textbook Source Passage Grounding",
    ])

    with ws_tab1:
        st.markdown(student_html, unsafe_allow_html=True)
        if not is_scaf_ws:
            with st.expander("Compare with Scaffolded Support Edition"):
                st.markdown(format_booklet_for_web(scaf_md), unsafe_allow_html=True)
        else:
            with st.expander("Compare with Standard Edition"):
                st.markdown(format_booklet_for_web(std_md), unsafe_allow_html=True)

    with ws_tab2:
        st.markdown(teacher_html, unsafe_allow_html=True)

    with ws_tab3:
        if gal_raw_md:
            with st.container(height=520):
                st.markdown(gal_raw_md)
        else:
            st.warning("Textbook passage markdown file could not be loaded.")
