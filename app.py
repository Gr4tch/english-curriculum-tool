import json
from pathlib import Path
from typing import Dict, List, Any, Optional

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
    run_blueprint_codesigner_chat,
)
from src.packet_builder import (
    generate_section_packet,
    build_chapter_student_booklet,
    build_chapter_master_teacher_plan,
    build_chapter_review_and_assessment,
)
from src.agent_team import (
    run_live_section_revision_chat,
    sanitize_aesthetics,
    enforce_page_budget_guardrail,
)
from doc_exporter import (
    ROOT_FOLDER_NAME,
    TEMP_DOCS_DIR,
    get_gdrive_service,
    build_docx_file,
    get_docx_bytes,
    export_section_packet_to_google_drive,
    export_chapter_package_to_google_drive,
    export_assessment_package_to_google_drive,
)
from src.preview_renderer import (
    render_preview_handout,
    render_preview_exemplar,
    render_preview_scaffold,
    render_preview_cover,
    render_preview_footer,
    format_booklet_for_web,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION & MODERN RESPONSIVE STYLING
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="8th Grade U.S. History (English) — AI Curriculum Co-Designer",
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
    /* Hide the collapsed sidebar toggle to give maximum widescreen real estate */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1400px !important;
    }
    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] label p,
    div[data-testid="stCheckbox"] label span,
    div[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        word-break: normal !important;
        font-size: 0.88rem !important;
    }
    .top-thin-bar {
        background: #0f172a;
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        margin-bottom: 1.25rem;
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
    .tile-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem 1.25rem 0.85rem 1.25rem;
        min-height: 165px;
        display: block;
        text-decoration: none !important;
        color: inherit !important;
        cursor: pointer;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        margin-bottom: 0.5rem;
    }
    .tile-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px -3px rgba(15, 23, 42, 0.10);
    }
    .tile-blue {
        border-top: 4px solid #2563eb !important;
        background: linear-gradient(180deg, #eff6ff 0%, #ffffff 42%);
    }
    .tile-blue:hover {
        border-color: #93c5fd;
        border-top: 4px solid #1d4ed8 !important;
    }
    .tile-indigo {
        border-top: 4px solid #6366f1 !important;
        background: linear-gradient(180deg, #eef2ff 0%, #ffffff 42%);
    }
    .tile-indigo:hover {
        border-color: #c7d2fe;
        border-top: 4px solid #4f46e5 !important;
    }
    .tile-amber {
        border-top: 4px solid #d97706 !important;
        background: linear-gradient(180deg, #fffbeb 0%, #ffffff 42%);
    }
    .tile-amber:hover {
        border-color: #fde68a;
        border-top: 4px solid #b45309 !important;
    }
    .tile-teal {
        border-top: 4px solid #0d9488 !important;
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 42%);
    }
    .tile-teal:hover {
        border-color: #99f6e4;
        border-top: 4px solid #0f766e !important;
    }
    .tile-emerald {
        border-top: 4px solid #059669 !important;
        background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 42%);
    }
    .tile-emerald:hover {
        border-color: #a7f3d0;
        border-top: 4px solid #047857 !important;
    }
    .tile-title {
        font-size: 1.10rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.45rem;
        min-height: 2.75rem;
        line-height: 1.35;
    }
    .tile-desc {
        font-size: 0.88rem;
        color: #475569;
        line-height: 1.45;
        margin-bottom: 0.75rem;
        min-height: 4.75rem;
    }
    .step-pill-active {
        display: inline-block;
        background: #1e3a8a;
        color: white;
        padding: 0.45rem 1.1rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.88rem;
    }
    .step-pill-inactive {
        display: inline-block;
        background: #f1f5f9;
        color: #64748b;
        padding: 0.45rem 1.1rem;
        border-radius: 999px;
        font-weight: 500;
        font-size: 0.88rem;
    }
    .strategy-card {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #1e3a8a;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.65rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: #dbeafe;
        color: #1e3a8a;
        margin-right: 0.4rem;
    }
    /* 1. Standard Download Buttons (Outline Style: Navy border & text) */
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
    div.stDownloadButton > button:not([kind="primary"]) p {
        color: #1e3a8a !important;
        font-weight: 700 !important;
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

    /* 2. Primary Download Buttons (e.g. 2-Page Section PDF in Textbook Browser) */
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
    div.stDownloadButton > button[kind="primary"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* 3. Google Drive Export Buttons (Calm Deep Royal Navy + Official Drive Icon Badge) */
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
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
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
    button[aria-label*="Google Drive"]::before,
    button[aria-label*="google drive"]::before,
    .gdrive-action-btn button::before {
        content: "" !important;
        display: inline-block !important;
        width: 22px !important;
        height: 22px !important;
        background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz1odHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyB2aWV3Qm94PTAgMCA4Ny4zIDc4PjxwYXRoIGZpbGw9IzAwNjZEQSBkPU02LjYgNjYuODVsMy44NSA2LjY1Yy44IDEuNCAxLjk1IDIuNSAzLjMgMy4zbDEzLjc1LTIzLjhIMGMwIDEuNTUuNCAzLjEgMS4yIDQuNXovPjxwYXRoIGZpbGw9IzAwQUM0NyBkPU00My42NSAyNUwyOS45IDEuMmMtMS4zNS44LTIuNSAxLjktMy4zIDMuM2wtMjUuNCA0NEMuNCA0OS45IDAgNTEuNDUgMCA1M2gyNy41ei8+PHBhdGggZmlsbD0jRUE0MzM1IGQ9TTczLjU1IDc2LjhjMS4zNS0uOCAyLjUtMS45IDMuMy0zLjNsOS4yNS0xNmMuOC0xLjQgMS4yLTIuOTUgMS4yLTQuNUg1OS44bDEzLjc1IDIzLjh6Lz48cGF0aCBmaWxsPSMwMDgzMkQgZD1NNDMuNjUgMjVsMTMuNzUtMjMuOGMtMS4zNS0uOC0yLjktMS4yLTQuNS0xLjJIMzQuNGMtMS42IDAtMy4xNS40NS00LjUgMS4yei8+PHBhdGggZmlsbD0jMjY4NEZDIGQ9TTU5LjggNTNoMjcuNWMwLTEuNTUtLjQtMy4xLTEuMi00LjVMNzIuMzUgMjIuN2MtLjgtMS40LTEuOTUtMi41LTMuMy0zLjN6Lz48cGF0aCBmaWxsPSNGRkJBMDAgZD1NNzMuNTUgNzYuOEw1OS44IDUzSDMyLjNsMTMuNzUgMjMuOGMxLjM1LjggMi45IDEuMiA0LjUgMS4yaDE4LjVjMS42IDAgMy4xNS0uNDUgNC41LTEuMnovPjwvc3ZnPg==") !important;
        background-repeat: no-repeat !important;
        background-size: 15px 14px !important;
        background-position: center !important;
        background-color: #ffffff !important;
        border-radius: 4px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12) !important;
        flex-shrink: 0 !important;
    }
    button[aria-label*="Google Drive"] p,
    button[aria-label*="google drive"] p,
    .gdrive-action-btn button p {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    /* 4. AI Revision Buttons (Distinctive Rich Indigo + White Sparkles Badge) */
    button[aria-label*="Apply AI Revision"],
    button[aria-label*="AI Revision"] {
        background-color: #4338ca !important;
        color: #ffffff !important;
        border: 1.5px solid #3730a3 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 2px 4px rgba(67, 56, 202, 0.22) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    button[aria-label*="Apply AI Revision"]:hover,
    button[aria-label*="AI Revision"]:hover {
        background-color: #3730a3 !important;
        border-color: #312e81 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(67, 56, 202, 0.38) !important;
        transform: translateY(-1px) !important;
    }
    button[aria-label*="Apply AI Revision"]::before,
    button[aria-label*="AI Revision"]::before {
        content: "" !important;
        display: inline-block !important;
        width: 22px !important;
        height: 22px !important;
        background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz1odHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyB2aWV3Qm94PTAgMCAyNCAyNCBmaWxsPSNmZmZmZmYgd2lkdGg9MjQgaGVpZ2h0PTI0PjxwYXRoIGQ9TTE5IDlsMS4yNS0yLjc1TDIzIDVsLTIuNzUtMS4yNUwxOSAxbC0xLjI1IDIuNzVMMTUgNWwyLjc1IDEuMjVMMTkgOXptLTcuNS41TDkgNCA2LjUgOS41IDEgMTJsNS41IDIuNUw5IDIwbDIuNS01LjVMMTcgMTJsLTUuNS0yLjV6TTE5IDE1bC0xLjI1IDIuNzVMMTUgMTlsMi43NSAxLjI1TDE5IDIzbDEuMjUtMi43NUwyMyAxOWwtMi43NS0xLjI1TDE5IDE1ei8+PC9zdmc+") !important;
        background-repeat: no-repeat !important;
        background-size: 14px 14px !important;
        background-position: center !important;
        background-color: rgba(255, 255, 255, 0.18) !important;
        border-radius: 4px !important;
        flex-shrink: 0 !important;
    }
    button[aria-label*="Apply AI Revision"] p,
    button[aria-label*="AI Revision"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    /* 5. General Primary Action Buttons (Next, Generate, Access Studio) */
    div.stButton > button[kind="primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]),
    div.stButton > button[data-testid="baseButton-primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]),
    div.stButton > button[data-testid="stBaseButton-primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]),
    button[kind="primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]) {
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
    div.stButton > button[kind="primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]):hover,
    div.stButton > button[data-testid="baseButton-primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]):hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]):hover,
    button[kind="primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]):hover {
        background-color: #172554 !important;
        border-color: #0f172a !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.35) !important;
        transform: translateY(-1px) !important;
    }
    div.stButton > button[kind="primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]) p,
    button[kind="primary"]:not([aria-label*="Google Drive"]):not([aria-label*="AI Revision"]) p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Prominent Expander & High-Contrast Light Theme Container Styling */
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
        border-radius: 8px 8px 0 0 !important;
    }
    div[data-testid="stExpander"] details summary svg {
        fill: #1e3a8a !important;
    }
    div[data-testid="stExpander"] details[open] summary {
        border-bottom: 1.5px solid #e2e8f0 !important;
    }
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        background-color: #ffffff !important;
        padding: 1rem !important;
    }
    /* Enforce Dark Slate Text on All Text Elements Inside Expanders Regardless of OS Dark Mode */
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] span,
    div[data-testid="stExpander"] label,
    div[data-testid="stExpander"] li,
    div[data-testid="stExpander"] strong,
    div[data-testid="stExpander"] em,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] strong,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] em,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stExpander"] div[data-testid="stCaptionContainer"] p,
    div[data-testid="stExpander"] .stCaption {
        color: #1e293b !important;
    }
    div[data-testid="stExpander"] div[data-testid="stCaptionContainer"] p,
    div[data-testid="stExpander"] .stCaption {
        color: #475569 !important;
    }
    /* Tabs Inside Expanders */
    div[data-testid="stExpander"] button[data-baseweb="tab"] {
        color: #475569 !important;
    }
    div[data-testid="stExpander"] button[data-baseweb="tab"][aria-selected="true"] {
        color: #1e3a8a !important;
        font-weight: 700 !important;
        border-bottom-color: #1e3a8a !important;
    }
    div[data-testid="stExpander"] button[data-baseweb="tab"] p {
        color: inherit !important;
    }
    /* Form Labels inside Expanders (Selectboxes, text inputs) */
    div[data-testid="stExpander"] label p {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    /* Preserve Button Text Colors Inside Expanders */
    div[data-testid="stExpander"] button[kind="primary"] p,
    div[data-testid="stExpander"] button[aria-label*="Google Drive"] p,
    div[data-testid="stExpander"] button[aria-label*="AI Revision"] p,
    div[data-testid="stExpander"] div.stDownloadButton > button[kind="primary"] p {
        color: #ffffff !important;
    }
    div[data-testid="stExpander"] div.stDownloadButton > button:not([kind="primary"]) p {
        color: #1e3a8a !important;
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


def bump_checklist_version(ch_num: int) -> None:
    k = f"chk_ver_{ch_num}"
    st.session_state[k] = st.session_state.get(k, 0) + 1


def render_metric_card(label: str, value: str) -> str:
    """Renders a clean, balanced metric card with legible headings and proportional text."""
    return (
        '<div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 0.65rem 0.95rem; min-height: 76px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 1px 3px rgba(15,23,42,0.04);">'
        f'<div style="font-size: 0.92rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.2rem;">{label}</div>'
        f'<div style="font-size: 1.05rem; font-weight: 600; color: #0f172a; line-height: 1.35;">{value}</div>'
        '</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# CLOUD SECRETS & PASSCODE AUTHENTICATION GATE
# ─────────────────────────────────────────────────────────────────────────────

# Synchronize Streamlit Secrets to environment variables (for Gemini API & cloud config)
try:
    if "GEMINI_API_KEY" in st.secrets:
        import os
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass


def verify_access() -> bool:
    """Passcode protection gate for secure multi-user and cloud access."""
    # 1. Check if already authenticated in session
    if st.session_state.get("authenticated", False):
        return True

    # 2. Check if auth query parameter is present (preserves session across link clicks)
    if st.query_params.get("auth") == "ok":
        st.session_state["authenticated"] = True
        return True

    expected = "HMS8thushistory"
    try:
        if "APP_PASSCODE" in st.secrets:
            expected = str(st.secrets["APP_PASSCODE"]).strip()
    except Exception:
        pass
    import os
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
                Enter your department access passcode to open the curriculum co-designer.
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
if "designer_step" not in st.session_state:
    st.session_state["designer_step"] = 1
if "selected_ch_num" not in st.session_state:
    st.session_state["selected_ch_num"] = 5 if 5 in sorted_chapter_nums else sorted_chapter_nums[0]

# Direct tile click navigation via query parameters
if "nav" in st.query_params:
    target_nav = str(st.query_params["nav"]).strip().lower()
    if target_nav in ["designer", "studio", "assessment", "browser", "gallery", "home"]:
        st.session_state["nav_view"] = target_nav
        if target_nav == "designer":
            st.session_state["designer_step"] = 1
    has_auth = st.query_params.get("auth") == "ok" or st.session_state.get("authenticated", False)
    try:
        del st.query_params["nav"]
    except Exception:
        pass
    if has_auth:
        st.query_params["auth"] = "ok"


# ─────────────────────────────────────────────────────────────────────────────
# 1. THIN TOP BAR: CHAPTER SELECTOR, ESSENTIAL QUESTION & STATUS PILL
# ─────────────────────────────────────────────────────────────────────────────

top_col1, top_col2 = st.columns([1.5, 1.2])

with top_col1:
    cur_ch = st.session_state["selected_ch_num"]
    cur_ch_idx = sorted_chapter_nums.index(cur_ch) if cur_ch in sorted_chapter_nums else 0

    def on_ch_change():
        st.session_state["selected_ch_num"] = st.session_state["top_ch_select"]
        for k in list(st.session_state.keys()):
            if k.startswith("compiled_chapter_pkts_"):
                del st.session_state[k]

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
ch_blueprint = get_chapter_blueprint(selected_ch_num, ch_info["chapter_title"])
ch_std_info = CHAPTER_STANDARDS_MAP.get(str(selected_ch_num), CHAPTER_STANDARDS_MAP["5"])

checked_codes = ch_blueprint.get("selected_sections", [])
active_sections = [s for s in ch_sections if str(s["section_code"]) in checked_codes]
pages_per_sec = int(ch_blueprint.get("pages_per_section", 1))
has_cover = ch_blueprint.get("cover_page_mode", "central_idea_tracker") != "none"
total_pkt_pages = len(checked_codes) * pages_per_sec + (1 if (has_cover and checked_codes) else 0)
total_sheets = (total_pkt_pages + 1) // 2

with top_col2:
    tc_pill, tc_out = st.columns([3.2, 1])
    with tc_pill:
        st.markdown(
            f"""
            <div style="text-align: right; padding-top: 0.25rem; white-space: nowrap;">
                <span class="badge-pill" style="font-size: 0.88rem; padding: 0.35rem 0.85rem;">
                    <b>{len(checked_codes)} of {len(ch_sections)}</b> Sections Selected &nbsp;|&nbsp; <b>{total_pkt_pages} pgs</b> ({total_sheets} sheets)
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with tc_out:
        if st.button("Log Out", key="top_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

raw_unit = str(ch_info['unit_title'])
display_unit = raw_unit if raw_unit.lower().startswith("unit") else f"Unit {ch_info['unit_num']}: {raw_unit}"
eq_text = ch_std_info.get('essential_question', '')

banner_html = (
    '<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 5px solid #1e3a8a; border-radius: 8px; padding: 0.9rem 1.25rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap;">'
    '<div style="flex: 1.2; min-width: 220px;">'
    '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Curriculum Unit</div>'
    f'<div style="font-size: 0.95rem; font-weight: 600; color: #0f172a; line-height: 1.35;">{display_unit}</div>'
    '</div>'
    '<div style="width: 1.5px; height: 42px; background: #cbd5e1;"></div>'
    '<div style="flex: 2; min-width: 280px;">'
    '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Essential Question</div>'
    f'<div style="font-size: 0.88rem; font-style: italic; color: #1e293b; line-height: 1.4;">"{eq_text}"</div>'
    '</div>'
    '<div style="width: 1.5px; height: 42px; background: #cbd5e1;"></div>'
    '<div style="flex-shrink: 0;">'
    '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Google Drive Folder</div>'
    f'<div style="font-size: 0.82rem; background: #e2e8f0; padding: 0.35rem 0.75rem; border-radius: 6px; color: #0f172a; font-family: monospace; font-weight: 600; white-space: nowrap;">{ROOT_FOLDER_NAME}</div>'
    '</div>'
    '</div>'
)
st.markdown(banner_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2. SCREEN 0: "WHAT WOULD YOU LIKE TO DO?" MAIN HUB (TILES)
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state["nav_view"] == "home":
    st.markdown("### What would you like to do?")
    st.caption("Select a tool below to co-design materials for your 40-minute U.S. History class:")

    tile_row1_c1, tile_row1_c2 = st.columns(2)

    with tile_row1_c1:
        st.markdown(
            """
            <a href="?nav=designer&auth=ok" target="_self" class="tile-card tile-blue">
                <div>
                    <div class="tile-title" style="color: #1d4ed8;">1. AI Packet Co-Designer & Chapter Builder</div>
                    <div class="tile-desc">
                        Step-by-step guided wizard to select sections from scratch, configure Central Idea synthesis & anti-copycat modes, adapt to 40-minute pacing, and compile complete student booklets + teacher clipboard answer keys.
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Packet Co-Designer ->", use_container_width=True, key="btn_tile_1"):
            st.session_state["nav_view"] = "designer"
            st.session_state["designer_step"] = 1
            st.rerun()

    with tile_row1_c2:
        st.markdown(
            """
            <a href="?nav=studio&auth=ok" target="_self" class="tile-card tile-indigo">
                <div>
                    <div class="tile-title" style="color: #4338ca;">2. Interactive Section Studio & Live Revision</div>
                    <div class="tile-desc">
                        Inspect any individual 2-page spread, compare Standard and Scaffolded worksheets side-by-side with the textbook passage, chat with AI to tweak questions, and download section-level Word documents or 2-page PDFs.
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Section Studio ->", use_container_width=True, key="btn_tile_2"):
            st.session_state["nav_view"] = "studio"
            st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    tile_row2_c1, tile_row2_c2 = st.columns(2)

    with tile_row2_c1:
        st.markdown(
            """
            <a href="?nav=assessment&auth=ok" target="_self" class="tile-card tile-amber">
                <div>
                    <div class="tile-title" style="color: #b45309;">3. End-of-Chapter Central Idea Review & Assessment</div>
                    <div class="tile-desc">
                        Generate a passage-grounded chapter review test, scaffolded review with word banks & sentence starters, and access the official textbook Chapter Review questions.
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Chapter Assessment ->", use_container_width=True, key="btn_tile_3"):
            st.session_state["nav_view"] = "assessment"
            st.rerun()

    with tile_row2_c2:
        st.markdown(
            """
            <a href="?nav=browser&auth=ok" target="_self" class="tile-card tile-teal">
                <div>
                    <div class="tile-title" style="color: #0f766e;">4. English Textbook PDF, Markdown & Vocab Browser</div>
                    <div class="tile-desc">
                        Browse and download all 194 searchable 2-page English Section PDFs, view paragraph-numbered markdown ([¶1]..[¶N]), and inspect clean official vocabulary.
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Textbook & Vocab Browser ->", use_container_width=True, key="btn_tile_4"):
            st.session_state["nav_view"] = "browser"
            st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <a href="?nav=gallery&auth=ok" target="_self" class="tile-card tile-emerald">
            <div>
                <div class="tile-title" style="color: #047857;">5. Individual Section Worksheet Printer & Strategy Gallery</div>
                <div class="tile-desc">
                    Select any chapter and section to preview, customize, and print or export standalone student worksheets (Standard & Scaffolded), Teacher Answer Keys, or browse the strategy template models.
                </div>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Section Worksheet Printer & Gallery ->", use_container_width=True, key="btn_tile_5"):
        st.session_state["nav_view"] = "gallery"
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# 3. TOOL 1: AI PACKET CO-DESIGNER & CHAPTER BUILDER (3 SEPARATE SCREENS)
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "designer":

    # Top Breadcrumb & Step Navigation Header
    b_col1, b_col2 = st.columns([1.2, 2.5])
    with b_col1:
        if st.button("Return to Main Menu", use_container_width=True):
            st.session_state["nav_view"] = "home"
            st.rerun()

    current_step = st.session_state.get("designer_step", 1)
    with b_col2:
        s1_cls = "step-pill-active" if current_step == 1 else "step-pill-inactive"
        s2_cls = "step-pill-active" if current_step == 2 else "step-pill-inactive"
        s3_cls = "step-pill-active" if current_step == 3 else "step-pill-inactive"
        st.markdown(
            f"""
            <div style="text-align: right; padding-top: 0.2rem;">
                <span class="{s1_cls}">Step 1: Choose Sections</span> &nbsp;->&nbsp;
                <span class="{s2_cls}">Step 2: Architecture & Strategies</span> &nbsp;->&nbsp;
                <span class="{s3_cls}">Step 3: Generate & Download</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ═════════════════════════════════════════════════════════════════════════
    # SCREEN 1: CHOOSE SECTIONS TO TEACH (BLANK SLATE)
    # ═════════════════════════════════════════════════════════════════════════
    if current_step == 1:
        st.markdown("### Step 1: Blank-Slate Section Checklist — Choose Which Sections You Want to Teach")
        st.caption(
            "Start from scratch: check only the 2-page spreads you plan to cover in your 40-minute classes. "
            "Your Student Packet Booklet, Cover Study Guide Tracker, and Master Clipboard Answer Key will dynamically include only the sections you select below."
        )

        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("Select Core Narrative Spreads (No Special Features)", use_container_width=True):
                core_codes = [str(s["section_code"]) for s in ch_sections if not s.get("is_special_feature")]
                ch_blueprint["selected_sections"] = core_codes
                save_chapter_blueprint(selected_ch_num, ch_blueprint)
                bump_checklist_version(selected_ch_num)
                st.rerun()
        with btn_c2:
            if st.button("Select All Chapter Spreads", use_container_width=True):
                ch_blueprint["selected_sections"] = [str(s["section_code"]) for s in ch_sections]
                save_chapter_blueprint(selected_ch_num, ch_blueprint)
                bump_checklist_version(selected_ch_num)
                st.rerun()
        with btn_c3:
            if st.button("Clear All (Blank Slate)", use_container_width=True):
                ch_blueprint["selected_sections"] = []
                save_chapter_blueprint(selected_ch_num, ch_blueprint)
                bump_checklist_version(selected_ch_num)
                st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        updated_selected: List[str] = []
        current_checked_set = set(str(c) for c in ch_blueprint.get("selected_sections", []))

        grid_cols = st.columns(2)
        chk_v = st.session_state.get(f"chk_ver_{selected_ch_num}", 0)
        for idx, sec in enumerate(ch_sections):
            scode = str(sec["section_code"])
            stype = sec.get("section_type", "Core Narrative")
            v_words = [v["word"] for v in sec.get("official_vocab", [])]
            v_str = f" • Vocab: {', '.join(v_words[:3])}" if v_words else ""
            label = (
                f"**Sec. {scode}: {sec['title']}** (pp. {sec['printed_pages']}) "
                f"— *[{stype} • {sec.get('word_count', 0)} words{v_str}]*"
            )
            col_target = grid_cols[idx % 2]
            is_checked = col_target.checkbox(
                label,
                value=(scode in current_checked_set),
                key=f"chk_ch{selected_ch_num}_v{chk_v}_sec_{scode}",
            )
            if is_checked:
                updated_selected.append(scode)

        if updated_selected != ch_blueprint.get("selected_sections", []):
            ch_blueprint["selected_sections"] = updated_selected
            save_chapter_blueprint(selected_ch_num, ch_blueprint)
            st.rerun()

        st.divider()
        nav_next_c1, nav_next_c2 = st.columns([2, 1])
        with nav_next_c2:
            if st.button("Next: Configure Architecture & Strategies ->", type="primary", use_container_width=True):
                st.session_state["designer_step"] = 2
                st.rerun()

    # ═════════════════════════════════════════════════════════════════════════
    # SCREEN 2: PACKET ARCHITECTURE, STRATEGY BANK & AI CO-DESIGNER
    # ═════════════════════════════════════════════════════════════════════════
    elif current_step == 2:
        st.markdown("### Step 2: Packet Architecture, Strategy Bank & AI Co-Designer")
        st.caption(
            "Configure how your 40-minute packet is structured: select Central Idea templates, Anti-Copycat mode, density, scaffolding, and chat with AI for suggestions."
        )

        col_controls, col_ai = st.columns([1.1, 1.0])

        with col_controls:
            st.markdown("#### Packet Architecture Controls")
            st.caption(
                "**How Dropdowns Work:** Choosing *'Use Recommended Templates per Section'* lets AI assign varied templates across different days based on each section's text structure. Selecting a specific strategy locks every section in this chapter into that single format."
            )

            AUTO = "auto_recommend"
            AUTO_CI_LABEL = "Use Recommended Templates per Section (AI Varied Variety)"
            AUTO_PMI_LABEL = "Use Recommended Modes per Section (AI Varied Variety)"
            AUTO_RO_LABEL = "Use Recommended Organizers per Section (AI Varied Variety)"

            ci_options = [s["code"] for s in CENTRAL_IDEA_STRATEGIES]
            ci_labels = {
                AUTO: AUTO_CI_LABEL,
                "ci_01_subheading_gist": "Subheading Gists -> Central Idea (All Sections)",
                "ci_02_box_and_bullets": "Box & Bullets: Claim + 3 Details (All Sections)",
                "ci_03_what_so_what": "'What Happened? + So What?' Synthesis (All Sections)",
                "ci_04_cer_paragraph": "Claim–Evidence–Reasoning CER (All Sections)",
            }
            ci_choices = [AUTO] + ci_options
            cur_ci = ch_blueprint.get("central_idea_strategy", AUTO)
            new_ci_default = st.selectbox(
                "Central Idea Strategy (Chapter Default):",
                options=ci_choices,
                index=ci_choices.index(cur_ci) if cur_ci in ci_choices else 0,
                format_func=lambda c: ci_labels.get(c, c),
                help="Default provides tailored variety across sections. Selecting a specific template locks every section in this chapter into that format.",
            )

            pmi_options = [m["code"] for m in PRINTED_MAIN_IDEA_MODES]
            pmi_labels = {
                AUTO: AUTO_PMI_LABEL,
                "pmi_01_prove_it": "'Prove the Textbook's Main Idea' (Cite Evidence from Each Subheading)",
                "pmi_02_subheading_focus": "'Subheading Central Ideas' (Find Ideas for Unprinted Subsections)",
                "pmi_03_upgrade_it": "'Upgrade the Textbook's Main Idea' (Rewrite into a Rich Historical Claim)",
            }
            pmi_choices = [AUTO] + pmi_options
            cur_pmi = ch_blueprint.get("printed_main_idea_mode", AUTO)
            new_pmi_default = st.selectbox(
                "Anti-Copycat Mode for Textbook's Printed MAIN IDEA:",
                options=pmi_choices,
                index=pmi_choices.index(cur_pmi) if cur_pmi in pmi_choices else 0,
                format_func=lambda c: pmi_labels.get(c, c),
                help="Guarantees students cannot copy the textbook's printed 1-sentence Main Idea box verbatim.",
            )

            ro_options = [r["code"] for r in READING_ORGANIZERS]
            ro_labels = {
                AUTO: AUTO_RO_LABEL,
                "read_01_cause_effect": "Cause & Effect Table (All Sections)",
                "read_02_say_something": "Subheading 'Say Something!' Stop & Jot (All Sections)",
                "read_03_cloze_guided": "Guided Cloze Summary (All Sections)",
                "read_04_sequence_timeline": "Chronological Sequence Tracker (All Sections)",
                "read_05_compare_perspectives": "Competing Perspectives Matrix (All Sections)",
            }
            ro_choices = [AUTO] + ro_options
            cur_ro = ch_blueprint.get("reading_organizer", AUTO)
            new_ro_default = st.selectbox(
                "Active Reading Organizer (Chapter Default):",
                options=ro_choices,
                index=ro_choices.index(cur_ro) if cur_ro in ro_choices else 0,
                format_func=lambda c: ro_labels.get(c, c),
                help="Default chooses the best organizer per section based on text structure. Selecting a specific one forces it across all sections.",
            )

            c_p1, c_p2 = st.columns(2)
            with c_p1:
                new_pages_per_sec = st.radio(
                    "Packet Density (Pages per Section):",
                    options=[1, 2],
                    index=0 if int(ch_blueprint.get("pages_per_section", 1)) == 1 else 1,
                    format_func=lambda p: "1 Page / Sec (Ultra-Compact)" if p == 1 else "2 Pages / Sec (Front & Back)",
                )
            with c_p2:
                scaf_opts = ["both", "standard", "scaffolded"]
                scaf_lbls = {
                    "both": "Both Editions (Standard + Scaffolded)",
                    "standard": "Standard Edition Only",
                    "scaffolded": "Scaffolded Edition Only (Stems + Word Banks)",
                }
                new_scaf_mode = st.selectbox(
                    "Student Edition Output:",
                    options=scaf_opts,
                    index=scaf_opts.index(ch_blueprint.get("scaffolding_mode", "both")),
                    format_func=lambda k: scaf_lbls[k],
                )

            c_v1, c_v2 = st.columns(2)
            with c_v1:
                v_opts = [v["code"] for v in VOCAB_MODES]
                v_lbls = {v["code"]: v["short_name"] for v in VOCAB_MODES}
                cur_v = ch_blueprint.get("vocab_mode", "vocab_official_box")
                new_vocab_mode = st.selectbox(
                    "Official Textbook Vocabulary Mode:",
                    options=v_opts,
                    index=v_opts.index(cur_v) if cur_v in v_opts else 0,
                    format_func=lambda c: v_lbls[c],
                    help="Choose 'Zero Vocab' to omit vocabulary and save maximum space for history reading.",
                )
                v_obj = get_strategy_by_code(VOCAB_MODES, new_vocab_mode)
                st.caption(f"**Vocab Setup:** {v_obj['description']}")

            with c_v2:
                rm_opts = [m["code"] for m in READING_MODES]
                rm_lbls = {m["code"]: m["short_name"] for m in READING_MODES}
                cur_rm = ch_blueprint.get("reading_mode", "mode_mixed_flexible")
                new_reading_mode = st.selectbox(
                    "40-Minute Classroom Routine:",
                    options=rm_opts,
                    index=rm_opts.index(cur_rm) if cur_rm in rm_opts else 0,
                    format_func=lambda c: rm_lbls[c],
                    help="Determines the instruction prompt printed on student worksheets.",
                )
                rm_obj = get_strategy_by_code(READING_MODES, new_reading_mode)
                st.caption(f"**Routine:** {rm_obj['description']}")
                st.markdown(
                    f"<div style='font-size:0.80rem; background:#f1f5f9; padding:0.35rem 0.6rem; border-radius:4px; color:#334155; margin-bottom:0.4rem;'>"
                    f"<b>Printed Directions:</b> <i>\"{rm_obj.get('preview_text', '')}\"</i></div>",
                    unsafe_allow_html=True,
                )

            custom_routine_input = ""
            if new_reading_mode == "mode_custom_other":
                custom_routine_input = st.text_input(
                    "Custom Worksheet Directions (Other):",
                    value=ch_blueprint.get("custom_reading_mode_text", "With your table group, discuss each subheading and"),
                    help="This exact sentence prefix will be printed on student worksheets at the top of the reading organizer.",
                )

            st.markdown("**Built-In Textbook Questions (`HISTORICAL THINKING` & Maps):**")
            q_c1, q_c2, q_c3 = st.columns([1.1, 1.1, 1.25])
            new_q1 = q_c1.checkbox(
                "#1 Reading Check",
                value=bool(ch_blueprint.get("include_reading_check_q1", True)),
                help="Textbook's built-in comprehension check",
            )
            new_q2 = q_c2.checkbox(
                "#2 Skill Question",
                value=bool(ch_blueprint.get("include_skill_q2", False)),
                help="Textbook's built-in Historical Thinking Skill question",
            )
            new_cv = q_c3.checkbox(
                "Critical Viewing (Maps/Art)",
                value=bool(ch_blueprint.get("include_critical_viewing", False)),
                help="Textbook's built-in image, map, and primary visual analysis questions",
            )

            c_cov, c_gb = st.columns(2)
            with c_cov:
                cov_opts = [c["code"] for c in COVER_PAGE_MODES]
                cov_lbls = {c["code"]: c["name"] for c in COVER_PAGE_MODES}
                cur_cov = ch_blueprint.get("cover_page_mode", "central_idea_tracker")
                new_cover_mode = st.selectbox(
                    "Booklet Front Cover Page:",
                    options=cov_opts,
                    index=cov_opts.index(cur_cov) if cur_cov in cov_opts else 0,
                    format_func=lambda c: cov_lbls[c],
                    help="Choose what kind of tracking or study guide page appears on the booklet front cover.",
                )
                cov_obj = get_strategy_by_code(COVER_PAGE_MODES, new_cover_mode)
                st.markdown(
                    f"""<div style="min-height: 85px; font-size: 0.84rem; color: #475569; line-height: 1.45;">
                    <strong>Cover Layout:</strong> {cov_obj['description']}
                    </div>""",
                    unsafe_allow_html=True,
                )

            with c_gb:
                gb_opts = [g["code"] for g in GRADE_BOX_MODES]
                gb_lbls = {g["code"]: g["name"] for g in GRADE_BOX_MODES}
                cur_gb = ch_blueprint.get("grade_box_mode", "stamp_box")
                new_gb_mode = st.selectbox(
                    "Page Footer Check Box:",
                    options=gb_opts,
                    index=gb_opts.index(cur_gb) if cur_gb in gb_opts else 0,
                    format_func=lambda c: gb_lbls[c],
                    help="Prints a grading or stamp box at the bottom of every student worksheet.",
                )
                gb_obj = get_strategy_by_code(GRADE_BOX_MODES, new_gb_mode)
                st.markdown(
                    f"""<div style="min-height: 85px; font-size: 0.84rem; color: #475569; line-height: 1.45;">
                    <strong>Footer Box:</strong> {gb_obj['description']}
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Row 2: Aligned expanders at the exact same horizontal level
            exp_cov, exp_gb = st.columns(2)
            with exp_cov:
                if new_cover_mode != "none":
                    with st.expander("Preview Cover Page Format", expanded=False):
                        st.markdown(render_preview_cover(new_cover_mode), unsafe_allow_html=True)
                else:
                    st.empty()
            with exp_gb:
                if new_gb_mode != "none":
                    with st.expander("Preview Footer Box Layout", expanded=False):
                        st.markdown(render_preview_footer(new_gb_mode), unsafe_allow_html=True)
                else:
                    st.empty()

            with st.expander("Optional Writing Extension (The Writing Revolution — Off by Default)", expanded=False):
                twr_opts = [t["code"] for t in OPTIONAL_TWR_STRATEGIES]
                twr_lbls = {t["code"]: t["name"] for t in OPTIONAL_TWR_STRATEGIES}
                new_twr = st.selectbox(
                    "Sentence-Level Writing Extension:",
                    options=twr_opts,
                    index=twr_opts.index(ch_blueprint.get("optional_twr_strategy", "twr_none")),
                    format_func=lambda c: twr_lbls[c],
                )

            updated_bp_fields = {
                "central_idea_strategy": new_ci_default,
                "printed_main_idea_mode": new_pmi_default,
                "reading_organizer": new_ro_default,
                "pages_per_section": new_pages_per_sec,
                "scaffolding_mode": new_scaf_mode,
                "vocab_mode": new_vocab_mode,
                "reading_mode": new_reading_mode,
                "custom_reading_mode_text": custom_routine_input if new_reading_mode == "mode_custom_other" else ch_blueprint.get("custom_reading_mode_text", ""),
                "include_reading_check_q1": new_q1,
                "include_skill_q2": new_q2,
                "include_critical_viewing": new_cv,
                "cover_page_mode": new_cover_mode,
                "grade_box_mode": new_gb_mode,
                "optional_twr_strategy": new_twr,
            }
            if any(ch_blueprint.get(k) != v for k, v in updated_bp_fields.items()):
                ch_blueprint.update(updated_bp_fields)
                save_chapter_blueprint(selected_ch_num, ch_blueprint)
                st.rerun()

        with col_ai:
            # 1. LIVE ASSEMBLED WORKSHEET PREVIEW
            preview_candidates = [s for s in ch_sections if str(s["section_code"]) in ch_blueprint.get("selected_sections", [])]
            if not preview_candidates:
                preview_candidates = ch_sections

            st.markdown(
                """
                <div style="background: #ffffff; border: 2px solid #1e3a8a; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.5rem; box-shadow: 0 2px 6px rgba(30, 58, 138, 0.08);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
                        <span style="background: #1e3a8a; color: #ffffff; font-size: 0.72rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em;">
                            Live Assembled Worksheet Preview
                        </span>
                    </div>
                    <div style="font-size: 0.83rem; color: #475569; line-height: 1.4;">
                        Updates dynamically as you adjust the <strong>Packet Architecture Controls</strong> on the left.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if len(preview_candidates) > 1:
                sample_sec = st.selectbox(
                    "Select section spread to preview:",
                    options=preview_candidates,
                    format_func=lambda s: f"Sec. {s['section_code']}: {s['title']} (pp. {s.get('printed_pages', '')})",
                    key="step2_preview_sec_select",
                    help="Choose which section from your chapter to inspect with your current architecture settings.",
                )
            else:
                sample_sec = preview_candidates[0]

            s_code = str(sample_sec["section_code"])

            # Generate real assembled sample section packet
            live_sample_pkt = generate_section_packet(sample_sec, ch_blueprint)

            prev_tab1, prev_tab2 = st.tabs([
                f"Standard Worksheet (Sec. {s_code})",
                "Scaffolded Support Edition",
            ])
            with prev_tab1:
                st.markdown(format_booklet_for_web(live_sample_pkt["student_standard_md"]), unsafe_allow_html=True)
            with prev_tab2:
                if live_sample_pkt.get("student_scaffolded_md"):
                    st.markdown(format_booklet_for_web(live_sample_pkt["student_scaffolded_md"]), unsafe_allow_html=True)
                else:
                    st.info("Scaffolded edition is disabled in Packet Architecture Controls.")

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # 2. STRATEGY REFERENCE LIBRARY (Clearly labeled as isolated models)
            with st.expander("Strategy Reference Library (Individual Template Examples)", expanded=False):
                st.caption(
                    "Note: These are isolated pedagogical models from the strategy library for inspection. "
                    f"Your active chapter worksheet for Chapter {selected_ch_num} is displayed in the Live Preview above."
                )
                g_tab1, g_tab2, g_tab3, g_tab4, g_tab5 = st.tabs([
                    "Central Idea (4)",
                    "Anti-Copycat (3)",
                    "Reading Organizers (5)",
                    "Covers & Footers (7)",
                    "Writing Extensions (5)",
                ])

                with g_tab1:
                    sel_ci_prev = st.selectbox(
                        "Select Central Idea Template to Preview:",
                        options=[s["code"] for s in CENTRAL_IDEA_STRATEGIES],
                        format_func=lambda c: get_strategy_by_code(CENTRAL_IDEA_STRATEGIES, c)["name"],
                        key="prev_ci_select_box",
                    )
                    ci_item = get_strategy_by_code(CENTRAL_IDEA_STRATEGIES, sel_ci_prev)
                    st.markdown(f"**Target ELA Standard:** CCSS RH.6-8.2 (Central Idea & Summary)")
                    st.markdown(f"**Best For:** {ci_item['best_for']}")
                    st.markdown(f"**How It Works:** {ci_item['description']}")

                    ci_sub1, ci_sub2 = st.tabs(["Printed Student Handout Format", "8th-Grade Student Exemplar"])
                    with ci_sub1:
                        st.markdown(render_preview_handout(sel_ci_prev), unsafe_allow_html=True)
                        if ci_item.get("scaffolded_md"):
                            st.markdown(render_preview_scaffold(ci_item["scaffolded_md"]), unsafe_allow_html=True)
                    with ci_sub2:
                        st.markdown(render_preview_exemplar(sel_ci_prev), unsafe_allow_html=True)

                with g_tab2:
                    sel_pmi_prev = st.selectbox(
                        "Select Anti-Copycat Mode to Preview:",
                        options=[m["code"] for m in PRINTED_MAIN_IDEA_MODES],
                        format_func=lambda c: get_strategy_by_code(PRINTED_MAIN_IDEA_MODES, c)["name"],
                        key="prev_pmi_select_box",
                    )
                    pmi_item = get_strategy_by_code(PRINTED_MAIN_IDEA_MODES, sel_pmi_prev)
                    st.markdown(f"**Anti-Copycat Rationale:** {pmi_item['description']}")

                    pmi_sub1, pmi_sub2 = st.tabs(["Handout Layout", "8th-Grade Student Exemplar"])
                    with pmi_sub1:
                        st.markdown(render_preview_handout(sel_pmi_prev), unsafe_allow_html=True)
                        if pmi_item.get("scaffolded_md"):
                            st.markdown(render_preview_scaffold(pmi_item["scaffolded_md"]), unsafe_allow_html=True)
                    with pmi_sub2:
                        st.markdown(render_preview_exemplar(sel_pmi_prev), unsafe_allow_html=True)

                with g_tab3:
                    sel_ro_prev = st.selectbox(
                        "Select Active Reading Organizer to Preview:",
                        options=[r["code"] for r in READING_ORGANIZERS],
                        format_func=lambda c: get_strategy_by_code(READING_ORGANIZERS, c)["name"],
                        key="prev_ro_select_box",
                    )
                    ro_item = get_strategy_by_code(READING_ORGANIZERS, sel_ro_prev)
                    st.markdown(f"**Target ELA Standard:** CCSS RH.6-8.5 (Text Structure)")
                    st.markdown(f"**Text Structure Focus:** {ro_item['description']}")

                    ro_sub1, ro_sub2 = st.tabs(["Handout Layout", "8th-Grade Student Exemplar"])
                    with ro_sub1:
                        st.markdown(render_preview_handout(sel_ro_prev), unsafe_allow_html=True)
                        if ro_item.get("scaffolded_md"):
                            st.markdown(render_preview_scaffold(ro_item["scaffolded_md"]), unsafe_allow_html=True)
                    with ro_sub2:
                        st.markdown(render_preview_exemplar(sel_ro_prev), unsafe_allow_html=True)

                with g_tab4:
                    st.markdown("##### Booklet Front Cover Pages")
                    sel_cov_prev = st.selectbox(
                        "Choose Cover Page Layout to Preview:",
                        options=[c["code"] for c in COVER_PAGE_MODES],
                        format_func=lambda c: get_strategy_by_code(COVER_PAGE_MODES, c)["name"],
                        key="prev_cov_select_box",
                    )
                    cov_item = get_strategy_by_code(COVER_PAGE_MODES, sel_cov_prev)
                    st.markdown(f"**How It Functions:** {cov_item['description']}")
                    st.markdown(render_preview_cover(sel_cov_prev), unsafe_allow_html=True)

                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    st.markdown("##### Page Footer Check Boxes")
                    sel_gb_prev = st.selectbox(
                        "Choose Footer Box Layout to Preview:",
                        options=[g["code"] for g in GRADE_BOX_MODES],
                        format_func=lambda c: get_strategy_by_code(GRADE_BOX_MODES, c)["name"],
                        key="prev_gb_select_box",
                    )
                    gb_item = get_strategy_by_code(GRADE_BOX_MODES, sel_gb_prev)
                    st.markdown(f"**Grading Use:** {gb_item['description']}")
                    st.markdown(render_preview_footer(sel_gb_prev), unsafe_allow_html=True)

                with g_tab5:
                    twr_active = [t for t in OPTIONAL_TWR_STRATEGIES if t["code"] != "twr_none"]
                    sel_twr_prev = st.selectbox(
                        "Select Writing Extension to Preview:",
                        options=[t["code"] for t in twr_active],
                        format_func=lambda c: get_strategy_by_code(twr_active, c)["name"],
                        key="prev_twr_select_box",
                    )
                    twr_item = get_strategy_by_code(twr_active, sel_twr_prev)
                    st.markdown(f"**Writing Objective:** {twr_item['description']}")

                    twr_sub1, twr_sub2 = st.tabs(["Handout Layout", "8th-Grade Student Exemplar"])
                    with twr_sub1:
                        st.markdown(render_preview_handout(sel_twr_prev), unsafe_allow_html=True)
                    with twr_sub2:
                        st.markdown(render_preview_exemplar(sel_twr_prev), unsafe_allow_html=True)

            st.markdown("#### Chat with Your AI Packet Co-Designer")
            st.caption("Ask questions or get suggestions on how to pace and structure your packet:")

            chat_key = f"blueprint_chat_ch_{selected_ch_num}"
            if chat_key not in st.session_state:
                st.session_state[chat_key] = [
                    {
                        "role": "assistant",
                        "content": (
                            f"Hi! I'm your AI curriculum co-designer for **Chapter {selected_ch_num}: {ch_info['chapter_title']}**. "
                            f"You currently have **{len(ch_blueprint.get('selected_sections', []))} sections** selected.\n\n"
                            "Ask me anything like:\n"
                            "- *\"How do I stop students from copying the textbook's printed Main Idea?\"*\n"
                            "- *\"Recommend the best templates for a 2-week unit.\"*"
                        ),
                    }
                ]

            chat_box = st.container(height=300)
            with chat_box:
                for msg in st.session_state[chat_key]:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            chat_in = st.chat_input("Ask your AI Co-Designer...", key=f"chat_in_screen2_{selected_ch_num}")
            if chat_in:
                st.session_state[chat_key].append({"role": "user", "content": chat_in})
                with st.spinner("Thinking..."):
                    reply, updated_bp = run_blueprint_codesigner_chat(
                        user_message=chat_in,
                        chapter_num=selected_ch_num,
                        chapter_title=ch_info["chapter_title"],
                        chapter_sections=ch_sections,
                        current_blueprint=ch_blueprint,
                        chat_history=st.session_state[chat_key][:-1],
                    )
                    save_chapter_blueprint(selected_ch_num, updated_bp)
                    bump_checklist_version(selected_ch_num)
                st.session_state[chat_key].append({"role": "assistant", "content": reply})
                st.rerun()

        st.divider()
        nav2_c1, nav2_c2 = st.columns([1, 1])
        with nav2_c1:
            if st.button("Back to Step 1: Choose Sections", use_container_width=True):
                st.session_state["designer_step"] = 1
                st.rerun()
        with nav2_c2:
            if st.button("Next: Step 3 — Strategy Matrix & Generate Packet ->", type="primary", use_container_width=True):
                st.session_state["designer_step"] = 3
                st.rerun()

    # ═════════════════════════════════════════════════════════════════════════
    # SCREEN 3: PER-SECTION STRATEGY MATRIX & GENERATED BOOKLETS
    # ═════════════════════════════════════════════════════════════════════════
    elif current_step == 3:
        st.markdown("### Step 3: Per-Section Strategy Matrix & Generated Chapter Booklets")

        selected_sec_codes = [str(c) for c in ch_blueprint.get("selected_sections", [])]
        active_sections = [s for s in ch_sections if str(s["section_code"]) in selected_sec_codes]

        if not active_sections:
            st.warning("No sections are selected yet. Go back to Step 1 to check sections!")
            if st.button("Back to Step 1: Select Sections"):
                st.session_state["designer_step"] = 1
                st.rerun()
        else:
            st.markdown(
                f"""
                <div style="background: #f8fafc; border: 1.5px solid #3b82f6; border-left: 5px solid #2563eb; border-radius: 8px; padding: 0.85rem 1.15rem; margin-bottom: 0.65rem;">
                    <div style="font-weight: 700; color: #1e3a8a; font-size: 0.95rem;">Customize Per-Section Strategies ({len(active_sections)} Active Spreads)</div>
                    <div style="font-size: 0.83rem; color: #475569; margin-top: 0.2rem;">
                        Override individual section templates below to introduce variety across different textbook spreads (e.g. switch between Cause & Effect, What/So What, and Chronological Sequences).
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander(f"Open Per-Section Strategy Overrides Table ({len(active_sections)} Active Spreads)", expanded=False):
                sec_overrides = dict(ch_blueprint.get("section_overrides", {}))
                override_changed = False

                ro_opts = [r["code"] for r in READING_ORGANIZERS]
                ro_lbls = {r["code"]: f"{r['short_name']} — {r['name']}" for r in READING_ORGANIZERS}
                ci_opts = [s["code"] for s in CENTRAL_IDEA_STRATEGIES]
                ci_lbls = {s["code"]: f"{s['short_name']} — {s['name']}" for s in CENTRAL_IDEA_STRATEGIES}
                pmi_opts = [m["code"] for m in PRINTED_MAIN_IDEA_MODES]
                pmi_lbls = {m["code"]: m["name"] for m in PRINTED_MAIN_IDEA_MODES}

                for sec in active_sections:
                    scode = str(sec["section_code"])
                    rec = recommend_section_strategies(sec, "", ch_blueprint)
                    bp_without_ov = dict(ch_blueprint)
                    bp_without_ov["section_overrides"] = {k: v for k, v in sec_overrides.items() if k != scode}
                    base_rec = recommend_section_strategies(sec, "", bp_without_ov)

                    m1, m2, m3, m4 = st.columns([1.4, 1.2, 1.2, 1.1])
                    with m1:
                        st.markdown(f"**Sec. {scode}: {sec['title']}** *(pp. {sec['printed_pages']})*")
                        st.caption(f"{rec['reason']}")
                    with m2:
                        sel_ro = st.selectbox(
                            "Reading Organizer",
                            options=ro_opts,
                            index=ro_opts.index(rec["reading_organizer_code"]),
                            format_func=lambda c: ro_lbls[c].split(" — ")[0],
                            key=f"ov_ro_ch{selected_ch_num}_{scode}_{base_rec['reading_organizer_code']}",
                        )
                    with m3:
                        sel_ci = st.selectbox(
                            "Central Idea Template",
                            options=ci_opts,
                            index=ci_opts.index(rec["central_idea_code"]),
                            format_func=lambda c: ci_lbls[c].split(" — ")[0],
                            key=f"ov_ci_ch{selected_ch_num}_{scode}_{base_rec['central_idea_code']}",
                        )
                    with m4:
                        sel_pmi = st.selectbox(
                            "Anti-Copycat Mode",
                            options=pmi_opts,
                            index=pmi_opts.index(rec["printed_main_idea_mode_code"]),
                            format_func=lambda c: pmi_lbls[c].split(" (")[0],
                            key=f"ov_pmi_ch{selected_ch_num}_{scode}_{base_rec['printed_main_idea_mode_code']}",
                        )

                    new_sec_ov = {}
                    if sel_ro != base_rec["reading_organizer_code"]:
                        new_sec_ov["reading_organizer"] = sel_ro
                    if sel_ci != base_rec["central_idea_code"]:
                        new_sec_ov["central_idea_strategy"] = sel_ci
                    if sel_pmi != base_rec["printed_main_idea_mode_code"]:
                        new_sec_ov["printed_main_idea_mode"] = sel_pmi

                    if new_sec_ov != sec_overrides.get(scode, {}):
                        if new_sec_ov:
                            sec_overrides[scode] = new_sec_ov
                        else:
                            sec_overrides.pop(scode, None)
                        override_changed = True

                if override_changed:
                    ch_blueprint["section_overrides"] = sec_overrides
                    save_chapter_blueprint(selected_ch_num, ch_blueprint)
                    st.rerun()

            # Compile/Generate Packets
            pkt_cache_key = f"compiled_chapter_pkts_{selected_ch_num}"
            bp_sig = json.dumps({k: v for k, v in ch_blueprint.items() if k != "chat_history"}, sort_keys=True, default=str)
            cached_b = st.session_state.get(pkt_cache_key)

            st.markdown(
                f"""
                <div style="background: #eff6ff; border: 1.5px solid #bfdbfe; border-left: 5px solid #3b82f6; border-radius: 8px; padding: 0.75rem 1.15rem; margin-top: 1rem; margin-bottom: 0.65rem; font-size: 0.85rem; color: #1e3a8a; line-height: 1.45;">
                    <strong>Why regenerate?</strong> Click the button below whenever you change any strategy settings above (such as Central Idea, Anti-Copycat mode, Reading Organizers, Covers, Footers, or per-section overrides) to rebuild all 3 booklets and the master key with your updated selections.
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"Regenerate Chapter {selected_ch_num} Packet Booklet & Master Clipboard Key ({len(active_sections)} Active Spreads)",
                type="primary",
                use_container_width=True,
            ) or not cached_b or cached_b.get("signature") != bp_sig:
                with st.spinner("Compiling packets with 100% textbook passage grounding & locked-in styling..."):
                    compiled_packets = [generate_section_packet(sec, ch_blueprint) for sec in active_sections]
                    std_bk = build_chapter_student_booklet(selected_ch_num, ch_info["chapter_title"], compiled_packets, ch_blueprint, edition="standard")
                    scaf_bk = build_chapter_student_booklet(selected_ch_num, ch_info["chapter_title"], compiled_packets, ch_blueprint, edition="scaffolded")
                    m_plan = build_chapter_master_teacher_plan(selected_ch_num, ch_info["chapter_title"], compiled_packets, ch_blueprint)
                    ch_rev_data = chapter_reviews.get(str(selected_ch_num), {})
                    asmt = build_chapter_review_and_assessment(selected_ch_num, ch_info["chapter_title"], compiled_packets, ch_rev_data)

                    st.session_state[pkt_cache_key] = {
                        "section_packets": compiled_packets,
                        "standard_booklet_md": std_bk,
                        "scaffolded_booklet_md": scaf_bk,
                        "master_plan_md": m_plan,
                        "assessment_pkg": asmt,
                        "signature": bp_sig,
                    }

            compiled_bundle = st.session_state.get(pkt_cache_key)
            if compiled_bundle:
                st.markdown("#### Print-Ready Word (.docx) Downloads & Google Drive Export")
                d_c1, d_c2, d_c3, d_c4 = st.columns(4)

                with d_c1:
                    std_bytes = get_docx_bytes(
                        compiled_bundle["standard_booklet_md"],
                        f"Chp_{selected_ch_num:02d}_Student_Booklet_Standard",
                        is_student_handout=True,
                    )
                    st.download_button(
                        "Standard Booklet (.docx)",
                        data=std_bytes,
                        file_name=f"Chp_{selected_ch_num:02d}_Student_Booklet_Standard.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )

                with d_c2:
                    scaf_bytes = get_docx_bytes(
                        compiled_bundle["scaffolded_booklet_md"],
                        f"Chp_{selected_ch_num:02d}_Student_Booklet_Scaffolded",
                        is_student_handout=True,
                    )
                    st.download_button(
                        "Scaffolded Booklet (.docx)",
                        data=scaf_bytes,
                        file_name=f"Chp_{selected_ch_num:02d}_Student_Booklet_Scaffolded.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )

                with d_c3:
                    key_bytes = get_docx_bytes(
                        compiled_bundle["master_plan_md"],
                        f"Chp_{selected_ch_num:02d}_Master_Teacher_Plan_and_Clipboard_Key",
                        is_student_handout=False,
                        include_top_student_header=False,
                    )
                    st.download_button(
                        "Master Clipboard Key (.docx)",
                        data=key_bytes,
                        file_name=f"Chp_{selected_ch_num:02d}_Master_Teacher_Plan_and_Clipboard_Key.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )

                with d_c4:
                    if st.button("Export to Google Drive", type="primary", use_container_width=True, key="btn_gdrive_export_ch"):
                        prog = st.empty()
                        try:
                            sec_map_by_code = {str(s["section_code"]): s for s in active_sections}
                            sec_pairs = [
                                (sec_map_by_code[p["section_code"]], p)
                                for p in compiled_bundle["section_packets"]
                                if p["section_code"] in sec_map_by_code
                            ]
                            scaf_to_send = (
                                compiled_bundle["scaffolded_booklet_md"]
                                if ch_blueprint.get("scaffolding_mode", "both") in ("both", "scaffolded")
                                else None
                            )
                            exp_res = export_chapter_package_to_google_drive(
                                chapter_num=selected_ch_num,
                                chapter_title=ch_info["chapter_title"],
                                master_plan_md=compiled_bundle["master_plan_md"],
                                standard_booklet_md=compiled_bundle["standard_booklet_md"],
                                scaffolded_booklet_md=scaf_to_send,
                                assessment_data=compiled_bundle["assessment_pkg"],
                                section_items_with_packets=sec_pairs,
                                progress_callback=lambda msg: prog.info(f"{msg}"),
                            )
                            prog.empty()
                            st.success(
                                f"Exported to Google Drive Folder: **{exp_res['chapter_folder_path']}**\n\n"
                                f"- [Open Chapter Folder in Google Drive]({exp_res['chapter_folder_url']})\n"
                                f"- [Master Teacher Plan & Clipboard Key]({exp_res['master_teacher_plan']['url']})\n"
                                f"- [Student Booklet (Standard)]({exp_res['standard_student_booklet']['url']})"
                            )
                        except Exception as e:
                            prog.empty()
                            st.error(f"Google Drive export error: {e}")

                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                prev_1, prev_2, prev_3 = st.tabs(
                    [
                        "Standard Student Booklet",
                        "Scaffolded Support Booklet",
                        "Master Teacher Plan & Clipboard Key",
                    ]
                )
                with prev_1:
                    st.markdown(format_booklet_for_web(compiled_bundle["standard_booklet_md"]), unsafe_allow_html=True)
                with prev_2:
                    st.markdown(format_booklet_for_web(compiled_bundle["scaffolded_booklet_md"]), unsafe_allow_html=True)
                with prev_3:
                    st.markdown(format_booklet_for_web(compiled_bundle["master_plan_md"]), unsafe_allow_html=True)

            st.divider()
            nav3_c1, nav3_c2 = st.columns([1, 1])
            with nav3_c1:
                if st.button("Back to Step 2: Architecture & Strategies", use_container_width=True):
                    st.session_state["designer_step"] = 2
                    st.rerun()
            with nav3_c2:
                if st.button("Start Over / Return to Main Menu", use_container_width=True):
                    st.session_state["nav_view"] = "home"
                    st.session_state["designer_step"] = 1
                    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# 4. TOOL 2: INTERACTIVE SECTION STUDIO & LIVE REVISION
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "studio":
    st_top_c1, st_top_c2 = st.columns([1.2, 2.5])
    with st_top_c1:
        if st.button("Return to Main Menu", use_container_width=True):
            st.session_state["nav_view"] = "home"
            st.rerun()
    with st_top_c2:
        st.markdown("<h3 style='margin:0; text-align:right;'>Interactive Section Studio</h3>", unsafe_allow_html=True)

    st.divider()

    st.markdown(
        """
        <div style="background: #ffffff; border: 1.5px solid #bfdbfe; border-left: 5px solid #1e3a8a; border-radius: 8px; padding: 0.85rem 1.15rem 0.65rem 1.15rem; margin-bottom: 0.85rem; box-shadow: 0 2px 6px rgba(30, 58, 138, 0.05);">
            <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem;">
                <div style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #1e3a8a;">
                    Select Section Spread to Inspect or Revise
                </div>
                <div style="font-size: 0.80rem; color: #64748b;">
                    Choose an 8th-grade textbook spread to view student worksheets, scaffolds, textbook passages, and customize:
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    studio_sel_c0, studio_sel_c1, studio_sel_c2 = st.columns([1.5, 3.2, 1.2])
    with studio_sel_c0:
        cur_studio_ch = st.session_state.get("studio_ch_num", selected_ch_num)
        studio_ch_idx = sorted_chapter_nums.index(cur_studio_ch) if cur_studio_ch in sorted_chapter_nums else 0
        studio_ch_num = st.selectbox(
            "Select Chapter:",
            options=sorted_chapter_nums,
            index=studio_ch_idx,
            format_func=lambda n: f"Ch. {n:02d}: {chapters_map[n]['chapter_title']}",
            key="studio_ch_select",
        )
        st.session_state["studio_ch_num"] = studio_ch_num
        studio_ch_info = chapters_map[studio_ch_num]
        studio_ch_sections = studio_ch_info["sections"]
        studio_blueprint = get_chapter_blueprint(studio_ch_num, studio_ch_info["chapter_title"])

    with studio_sel_c1:
        selected_studio_sec = st.selectbox(
            "Select Section Spread to Inspect or Revise:",
            options=studio_ch_sections,
            format_func=lambda s: f"Sec. {s['section_code']}: {s['title']} (pp. {s['printed_pages']}) — [{s.get('section_type', 'Core Narrative')}]",
            key=f"studio_sec_{studio_ch_num}",
        )

    s_code = str(selected_studio_sec["section_code"])
    studio_pkt_key = f"studio_pkt_ch{studio_ch_num}_sec_{s_code}"

    md_path = resolve_file_path(selected_studio_sec.get("md_file"))
    raw_passage_md = md_path.read_text(encoding="utf-8") if md_path.exists() else ""

    with studio_sel_c2:
        if st.button("Reset to Defaults", key=f"rst_{studio_pkt_key}", use_container_width=True):
            st.session_state[studio_pkt_key] = generate_section_packet(
                selected_studio_sec, studio_blueprint, raw_passage_md
            )
            st.rerun()

    if studio_pkt_key not in st.session_state:
        st.session_state[studio_pkt_key] = generate_section_packet(
            selected_studio_sec, studio_blueprint, raw_passage_md
        )

    sec_pkt = st.session_state[studio_pkt_key]
    pb_info = sec_pkt.get("page_budget", {})

    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        st.markdown(render_metric_card("Density", f"{sec_pkt['pages_per_section']} Page(s)"), unsafe_allow_html=True)
    with b_col2:
        st.markdown(render_metric_card("Page Budget Fit", f"{pb_info.get('final_layout_units', 0)} / {pb_info.get('max_budget_units', 28)} units"), unsafe_allow_html=True)
    with b_col3:
        st.markdown(render_metric_card("Reading Organizer", sec_pkt["recommendations"]["reading_organizer_short"]), unsafe_allow_html=True)
    with b_col4:
        st.markdown(render_metric_card("Central Idea Mode", sec_pkt["recommendations"]["central_idea_short"]), unsafe_allow_html=True)

    st_left, st_right = st.columns([1.35, 1.0])

    with st_left:
        sub_std, sub_scaf, sub_tkey, sub_text = st.tabs(
            [
                "Standard Worksheet",
                "Scaffolded Worksheet",
                "Clipboard Answer Key (Exact Citations)",
                "2-Page Textbook Passage",
            ]
        )
        with sub_std:
            st.markdown(format_booklet_for_web(sec_pkt["student_standard_md"]), unsafe_allow_html=True)
        with sub_scaf:
            st.markdown(format_booklet_for_web(sec_pkt["student_scaffolded_md"]), unsafe_allow_html=True)
        with sub_tkey:
            st.markdown(sec_pkt["teacher_key_md"])
        with sub_text:
            if selected_studio_sec.get("printed_main_idea"):
                st.info(f"**Printed Textbook MAIN IDEA (p. {selected_studio_sec.get('start_page', '')}):** *{selected_studio_sec['printed_main_idea']}*")
            if raw_passage_md:
                with st.container(height=520):
                    st.markdown(raw_passage_md)
            else:
                st.warning("Textbook passage markdown file could not be loaded.")

    with st_right:
        st.markdown("#### Live AI Revision Chat")
        st.caption("Ask AI to tweak questions or adjust prompts (applied to both Standard & Scaffolded editions):")

        rev_req = st.text_area(
            "Revision Request:",
            placeholder="e.g. Add a question about the Boston Tea Party, or adjust the sentence starter.",
            height=90,
            key=f"rev_txt_{studio_pkt_key}",
            label_visibility="collapsed",
        )
        if st.button("Apply AI Revision", type="primary", use_container_width=True):
            if rev_req.strip():
                with st.spinner("Applying revision..."):
                    rev_out = run_live_section_revision_chat(
                        user_instruction=rev_req.strip(),
                        section_meta=selected_studio_sec,
                        markdown_text=raw_passage_md,
                        current_student_md=sec_pkt["student_standard_md"],
                        current_scaffolded_md=sec_pkt["student_scaffolded_md"],
                        current_teacher_md=sec_pkt["teacher_key_md"],
                    )
                    t_pgs = int(sec_pkt["pages_per_section"])
                    std_fit, b_fit = enforce_page_budget_guardrail(rev_out["student_standard_md"], target_pages=t_pgs)
                    scaf_fit, _ = enforce_page_budget_guardrail(rev_out["student_scaffolded_md"], target_pages=t_pgs)
                    sec_pkt["student_standard_md"] = std_fit
                    sec_pkt["student_scaffolded_md"] = scaf_fit
                    sec_pkt["teacher_key_md"] = rev_out["teacher_key_md"]
                    sec_pkt["page_budget"] = b_fit
                    st.session_state[studio_pkt_key] = sec_pkt
                    st.success("Revision applied!")
                    st.rerun()

        st.divider()
        st.markdown("#### Download or Export This Section")

        s1, s2 = st.columns(2)
        with s1:
            st.download_button(
                "Standard (.docx)",
                data=get_docx_bytes(sec_pkt["student_standard_md"], f"Chp_{studio_ch_num:02d}_Sec_{s_code}_Standard", True),
                file_name=f"Chp_{studio_ch_num:02d}_Sec_{s_code}_Standard.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with s2:
            st.download_button(
                "Scaffolded (.docx)",
                data=get_docx_bytes(sec_pkt["student_scaffolded_md"], f"Chp_{studio_ch_num:02d}_Sec_{s_code}_Scaffolded", True),
                file_name=f"Chp_{studio_ch_num:02d}_Sec_{s_code}_Scaffolded.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

        st.download_button(
            "Section Teacher Plan & Clipboard Key (.docx)",
            data=get_docx_bytes(sec_pkt["teacher_key_md"], f"Chp_{studio_ch_num:02d}_Sec_{s_code}_Key", False, False),
            file_name=f"Chp_{studio_ch_num:02d}_Sec_{s_code}_Teacher_Key.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

        if st.button(f"Export Sec. {s_code} + 2-Page PDF to Google Drive", type="primary", use_container_width=True, key=f"btn_gdrive_export_sec_{s_code}"):
            with st.spinner("Uploading to Google Drive..."):
                try:
                    s_res = export_section_packet_to_google_drive(
                        section_meta=selected_studio_sec,
                        packet_data=sec_pkt,
                        include_scaffolded=True,
                        include_section_pdf=True,
                    )
                    st.success(
                        f"Uploaded to **{s_res['folder_path']}**\n\n"
                        f"- [Open Section Folder]({s_res['folder_url']})\n"
                        f"- [Standard Worksheet]({s_res['student_standard']['url']})\n"
                        f"- [Scaffolded Worksheet]({s_res['student_scaffolded']['url']})\n"
                        f"- [Teacher Key]({s_res['teacher_key']['url']})"
                    )
                except Exception as e:
                    st.error(f"Google Drive upload error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. TOOL 3: END-OF-CHAPTER CENTRAL IDEA REVIEW & ASSESSMENT
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "assessment":
    as_top_c1, as_top_c2 = st.columns([1.2, 2.5])
    with as_top_c1:
        if st.button("Return to Main Menu", use_container_width=True):
            st.session_state["nav_view"] = "home"
            st.rerun()
    with as_top_c2:
        st.markdown(f"<h3 style='margin:0; text-align:right;'>Chapter {selected_ch_num} Central Idea Review & Assessment</h3>", unsafe_allow_html=True)

    st.divider()

    selected_sec_codes_t3 = [str(c) for c in ch_blueprint.get("selected_sections", [])]
    active_secs_t3 = [s for s in ch_sections if str(s["section_code"]) in selected_sec_codes_t3]
    if not active_secs_t3:
        st.info("No sections checked in Step 1 — previewing using all Core Narrative spreads.")
        active_secs_t3 = [s for s in ch_sections if not s.get("is_special_feature")]

    pkts_for_test = [generate_section_packet(s, ch_blueprint) for s in active_secs_t3]
    ch_rev_obj = chapter_reviews.get(str(selected_ch_num), {})
    test_bundle = build_chapter_review_and_assessment(selected_ch_num, ch_info["chapter_title"], pkts_for_test, ch_rev_obj)

    t_dl1, t_dl2, t_dl3, t_dl4 = st.columns(4)
    with t_dl1:
        st.download_button(
            "Standard Assessment (.docx)",
            data=get_docx_bytes(test_bundle["standard_test_md"], f"Chp_{selected_ch_num:02d}_Assessment_Standard", True),
            file_name=f"Chp_{selected_ch_num:02d}_Assessment_Standard.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with t_dl2:
        st.download_button(
            "Scaffolded Assessment (.docx)",
            data=get_docx_bytes(test_bundle["scaffolded_test_md"], f"Chp_{selected_ch_num:02d}_Assessment_Scaffolded", True),
            file_name=f"Chp_{selected_ch_num:02d}_Assessment_Scaffolded.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with t_dl3:
        st.download_button(
            "Assessment Answer Key (.docx)",
            data=get_docx_bytes(test_bundle["teacher_key_md"], f"Chp_{selected_ch_num:02d}_Assessment_Key", False, False),
            file_name=f"Chp_{selected_ch_num:02d}_Assessment_Key.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with t_dl4:
        if st.button("Export to Google Drive", type="primary", use_container_width=True, key="btn_gdrive_export_assessment"):
            with st.spinner("Uploading Assessment docs to Google Drive..."):
                try:
                    as_res = export_assessment_package_to_google_drive(
                        chapter_num=selected_ch_num,
                        chapter_title=ch_info["chapter_title"],
                        assessment_data=test_bundle,
                    )
                    st.success(
                        f"Uploaded to **{as_res['chapter_folder_path']}**\n\n"
                        f"- [Open Chapter Folder]({as_res['chapter_folder_url']})\n"
                        f"- [Standard Assessment]({as_res['docs'].get('standard_test_md', {}).get('url', '#')})\n"
                        f"- [Scaffolded Assessment]({as_res['docs'].get('scaffolded_test_md', {}).get('url', '#')})\n"
                        f"- [Answer Key]({as_res['docs'].get('teacher_key_md', {}).get('url', '#')})"
                    )
                except Exception as e:
                    st.error(f"Google Drive upload error: {e}")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    rev_t1, rev_t2, rev_t3, rev_t4 = st.tabs(
        [
            "Standard Review & Assessment",
            "Scaffolded Review & Assessment",
            "Teacher Answer Key",
            f"Official Textbook Review (pp. {ch_rev_obj.get('printed_pages', 'End of Chapter')})",
        ]
    )
    with rev_t1:
        st.markdown(format_booklet_for_web(test_bundle["standard_test_md"]), unsafe_allow_html=True)
    with rev_t2:
        st.markdown(format_booklet_for_web(test_bundle["scaffolded_test_md"]), unsafe_allow_html=True)
    with rev_t3:
        st.markdown(format_booklet_for_web(test_bundle["teacher_key_md"]), unsafe_allow_html=True)
    with rev_t4:
        if ch_rev_obj and ch_rev_obj.get("questions"):
            st.markdown(f"#### Official American Stories Chapter {selected_ch_num} Review Questions (pp. {ch_rev_obj.get('printed_pages', '')})")
            for q in ch_rev_obj["questions"]:
                st.markdown(f"- **Question {q['num']}** *(Category: {q.get('category', 'Review')})*: {q['question']}")
        else:
            st.info("No end-of-chapter review questions found for this chapter.")


# ─────────────────────────────────────────────────────────────────────────────
# 6. TOOL 4: ENGLISH TEXTBOOK PDF, MARKDOWN & VOCAB BROWSER
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "browser":
    br_top_c1, br_top_c2 = st.columns([1.2, 2.5])
    with br_top_c1:
        if st.button("Return to Main Menu", use_container_width=True):
            st.session_state["nav_view"] = "home"
            st.rerun()
    with br_top_c2:
        st.markdown(f"<h3 style='margin:0; text-align:right;'>English Textbook Repository & Vocab</h3>", unsafe_allow_html=True)

    st.divider()

    br_col1, br_col2 = st.columns([1.15, 1.0])

    with br_col1:
        st.markdown(f"#### Chapter {selected_ch_num} Searchable 2-Page Section PDFs")
        selected_pdf_sec = st.selectbox(
            "Choose Section Spread:",
            options=ch_sections,
            format_func=lambda s: f"Sec. {s['section_code']}: {s['title']} (pp. {s['printed_pages']})",
            key=f"pdf_browser_sec_{selected_ch_num}",
        )

        pdf_file_path = resolve_file_path(selected_pdf_sec.get("pdf_file"))
        hier_pdf_path = selected_pdf_sec.get("hierarchy_pdf_file", "")

        if pdf_file_path.exists():
            st.download_button(
                f"Download 2-Page PDF: Sec. {selected_pdf_sec['section_code']} - {selected_pdf_sec['title']} (pp. {selected_pdf_sec['printed_pages']})",
                data=pdf_file_path.read_bytes(),
                file_name=f"Chp{selected_ch_num:02d}_Sec{selected_pdf_sec['section_code']}_{selected_pdf_sec['title']}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
            st.caption(f"Archived high-resolution 2-page textbook spread for Sec. {selected_pdf_sec['section_code']} (pp. {selected_pdf_sec['printed_pages']}).")

        st.markdown("##### Pedagogical Structure & Architecture")
        sec_type_badge = selected_pdf_sec.get("section_type", "Core Narrative")
        pages_disp = f"pp. {selected_pdf_sec.get('printed_pages', '')}"
        pmi_val = selected_pdf_sec.get("printed_main_idea", "None (Special Feature Spread)")

        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #1e3a8a; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.85rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                <div style="margin-bottom: 0.45rem;">
                    <span style="background: #dbeafe; color: #1e40af; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.55rem; border-radius: 4px; text-transform: uppercase;">{sec_type_badge}</span>
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.55rem; border-radius: 4px; margin-left: 0.35rem;">{pages_disp}</span>
                </div>
                <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #64748b; margin-bottom: 0.2rem;">Printed Textbook Main Idea:</div>
                <div style="font-size: 0.85rem; font-style: italic; color: #0f172a; line-height: 1.4;">"{pmi_val}"</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        subhs = selected_pdf_sec.get("subheadings", [])
        if subhs:
            st.markdown("**Subheadings in this 2-page spread:**")
            for sh in subhs:
                st.markdown(f"- **{sh['title']}** *(p. {sh.get('page', '')}, ~{sh.get('paragraph_count', 1)} paragraphs)*")

        sec_voc = selected_pdf_sec.get("official_vocab", [])
        if sec_voc:
            st.markdown("**Section Vocabulary:**")
            for v in sec_voc:
                st.markdown(f"- **{v['word']}**: *{v.get('definition', '')}*")



    with br_col2:
        st.markdown("#### Official Content & Academic Vocabulary (pp. R44–R58)")
        ch_vocab_list = vocab_index.get("by_chapter", {}).get(str(selected_ch_num), [])
        if ch_vocab_list:
            c_v_list = [v["word"] for v in ch_vocab_list if v.get("type") == "Content Vocabulary"]
            a_v_list = [v["word"] for v in ch_vocab_list if v.get("type") == "Academic Vocabulary"]
            st.markdown(f"- **Content Vocabulary ({len(c_v_list)} terms):**\n  {', '.join(c_v_list)}")
            if a_v_list:
                st.markdown(f"- **Academic Vocabulary ({len(a_v_list)} terms):**\n  {', '.join(a_v_list)}")

        st.markdown("##### Paragraph-Tagged Section Markdown ([¶1]..[¶N])")
        md_p4 = resolve_file_path(selected_pdf_sec.get("md_file"))
        if md_p4.exists():
            with st.container(height=480):
                st.markdown(md_p4.read_text(encoding="utf-8"))
        else:
            st.warning("Section markdown passage file could not be found.")


# ─────────────────────────────────────────────────────────────────────────────
# 6. TOOL 5: STANDALONE STRATEGY & WORKSHEET TEMPLATE GALLERY
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "gallery":
    g_top_c1, g_top_c2, g_top_c3 = st.columns([1.2, 1.5, 1.5])
    with g_top_c1:
        if st.button("Return to Main Menu", use_container_width=True):
            st.session_state["nav_view"] = "home"
            st.rerun()
    with g_top_c2:
        if st.button("Go to Packet Co-Designer (Step 2)", use_container_width=True):
            st.session_state["nav_view"] = "designer"
            st.session_state["designer_step"] = 2
            st.rerun()
    with g_top_c3:
        st.markdown("<h3 style='margin:0; text-align:right;'>Individual Section Worksheet Printer & Gallery</h3>", unsafe_allow_html=True)

    st.divider()

    main_gal_tab1, main_gal_tab2 = st.tabs([
        "Print Individual Section Worksheets",
        "Strategy & Template Models (Exemplar Gallery)",
    ])

    with main_gal_tab1:
        st.markdown(
            """
            <div style="background: #ffffff; border: 1.5px solid #bbf7d0; border-left: 5px solid #16a34a; border-radius: 8px; padding: 0.85rem 1.15rem 0.65rem 1.15rem; margin-bottom: 0.95rem; box-shadow: 0 2px 6px rgba(22, 163, 74, 0.05);">
                <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem;">
                    <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #166534;">
                        Select Chapter and Section Spread to Print
                    </div>
                    <div style="font-size: 0.80rem; color: #64748b;">
                        Print standalone 1-day student handouts (Standard & Scaffolded) and Teacher Keys for any specific section spread:
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c_ch, c_sec = st.columns([1.1, 1.9])
        with c_ch:
            cur_gal_ch = st.session_state.get("gal_print_ch_num", selected_ch_num)
            gal_ch_idx = sorted_chapter_nums.index(cur_gal_ch) if cur_gal_ch in sorted_chapter_nums else 0
            gal_print_ch_num = st.selectbox(
                "1. Select Chapter:",
                options=sorted_chapter_nums,
                index=gal_ch_idx,
                format_func=lambda n: f"Chapter {n:02d}: {chapters_map[n]['chapter_title']} ({len(chapters_map[n]['sections'])} spreads)",
                key="gal_print_ch_select",
            )
            st.session_state["gal_print_ch_num"] = gal_print_ch_num

        gal_ch_info = chapters_map[gal_print_ch_num]
        gal_ch_sections = gal_ch_info["sections"]
        gal_ch_bp = get_chapter_blueprint(gal_print_ch_num, gal_ch_info["chapter_title"])

        with c_sec:
            gal_selected_sec = st.selectbox(
                "2. Select Section Spread to Print:",
                options=gal_ch_sections,
                format_func=lambda s: f"Sec. {s['section_code']}: {s['title']} (pp. {s['printed_pages']}) — [{s.get('section_type', 'Core Narrative')}]",
                key=f"gal_print_sec_select_{gal_print_ch_num}",
            )

        gal_sec_code = str(gal_selected_sec["section_code"])
        gal_md_path = resolve_file_path(gal_selected_sec.get("md_file"))
        gal_raw_passage_md = gal_md_path.read_text(encoding="utf-8") if gal_md_path.exists() else ""

        # Section Info Card
        sec_vocab = gal_selected_sec.get("official_vocab", [])
        vocab_preview = ", ".join([v["word"] for v in sec_vocab[:4]]) if sec_vocab else "None listed"
        if len(sec_vocab) > 4:
            vocab_preview += f" (+{len(sec_vocab) - 4} more)"

        st.markdown(
            f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1.15rem; margin-bottom: 0.95rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                    <div>
                        <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em;">Selected Section Spread</div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a;">Sec. {gal_sec_code}: {gal_selected_sec['title']} (pp. {gal_selected_sec['printed_pages']})</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge-pill" style="font-size: 0.78rem; padding: 0.25rem 0.65rem;">
                            {gal_selected_sec.get('section_type', 'Core Narrative')}
                        </span>
                        &nbsp;
                        <span class="badge-pill" style="font-size: 0.78rem; padding: 0.25rem 0.65rem;">
                            {gal_selected_sec.get('word_count', 0)} Words
                        </span>
                    </div>
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.84rem; color: #334155;">
                    <b>Official Content Vocab:</b> {vocab_preview}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Strategy Customization Expander
        with st.expander("Customize Strategy & Architecture for this Worksheet (Optional)", expanded=False):
            st.caption("Change the pedagogical strategy for this specific printed worksheet. Leave on defaults to use the recommended textbook structure.")
            cust_c1, cust_c2 = st.columns(2)
            with cust_c1:
                ci_opts = [s["code"] for s in CENTRAL_IDEA_STRATEGIES]
                rec_ci = gal_ch_bp.get("central_idea_strategy", "ci_claims_evidence")
                selected_ci = st.selectbox(
                    "Central Idea Synthesis Model:",
                    options=ci_opts,
                    index=ci_opts.index(rec_ci) if rec_ci in ci_opts else 0,
                    format_func=lambda c: get_strategy_by_code(CENTRAL_IDEA_STRATEGIES, c)["name"],
                    key=f"gal_ci_{gal_print_ch_num}_{gal_sec_code}",
                )
                pmi_opts = [m["code"] for m in PRINTED_MAIN_IDEA_MODES]
                rec_pmi = gal_ch_bp.get("printed_main_idea_mode", "pmi_paraphrase_challenge")
                selected_pmi = st.selectbox(
                    "Anti-Copycat Mechanic (Textbook Main Idea Box):",
                    options=pmi_opts,
                    index=pmi_opts.index(rec_pmi) if rec_pmi in pmi_opts else 0,
                    format_func=lambda c: get_strategy_by_code(PRINTED_MAIN_IDEA_MODES, c)["name"],
                    key=f"gal_pmi_{gal_print_ch_num}_{gal_sec_code}",
                )
            with cust_c2:
                ro_opts = [r["code"] for r in READING_ORGANIZERS]
                rec_ro = gal_ch_bp.get("reading_organizer", "read_01_cause_effect")
                selected_ro = st.selectbox(
                    "Active Reading Graphic Organizer:",
                    options=ro_opts,
                    index=ro_opts.index(rec_ro) if rec_ro in ro_opts else 0,
                    format_func=lambda c: get_strategy_by_code(READING_ORGANIZERS, c)["name"],
                    key=f"gal_ro_{gal_print_ch_num}_{gal_sec_code}",
                )
                twr_opts = [t["code"] for t in OPTIONAL_TWR_STRATEGIES]
                rec_twr = gal_ch_bp.get("optional_twr_strategy", "twr_none")
                selected_twr = st.selectbox(
                    "Optional Writing Extension (The Writing Revolution):",
                    options=twr_opts,
                    index=twr_opts.index(rec_twr) if rec_twr in twr_opts else 0,
                    format_func=lambda c: get_strategy_by_code(OPTIONAL_TWR_STRATEGIES, c)["name"],
                    key=f"gal_twr_{gal_print_ch_num}_{gal_sec_code}",
                )

        # Build custom blueprint for this generation
        cur_bp = dict(gal_ch_bp)
        cur_bp["central_idea_strategy"] = selected_ci
        cur_bp["printed_main_idea_mode"] = selected_pmi
        cur_bp["reading_organizer"] = selected_ro
        cur_bp["optional_twr_strategy"] = selected_twr

        pkt_cache_key = f"gal_pkt_ch{gal_print_ch_num}_sec{gal_sec_code}_{selected_ci}_{selected_ro}_{selected_pmi}_{selected_twr}"
        if pkt_cache_key not in st.session_state:
            st.session_state[pkt_cache_key] = generate_section_packet(
                gal_selected_sec, cur_bp, gal_raw_passage_md
            )
        gal_pkt = st.session_state[pkt_cache_key]

        st.markdown("#### Print, Download & Export Options")
        d_c1, d_c2, d_c3, d_c4 = st.columns([1.2, 1.2, 1.3, 1.3])
        with d_c1:
            std_bytes = get_docx_bytes(
                gal_pkt["student_standard_md"],
                f"Chp_{gal_print_ch_num:02d}_Sec_{gal_sec_code}_Standard",
                is_student_handout=True,
            )
            st.download_button(
                "Standard Worksheet (.docx)",
                data=std_bytes,
                file_name=f"Chp_{gal_print_ch_num:02d}_Sec_{gal_sec_code}_Standard.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with d_c2:
            scaf_bytes = get_docx_bytes(
                gal_pkt["student_scaffolded_md"],
                f"Chp_{gal_print_ch_num:02d}_Sec_{gal_sec_code}_Scaffolded",
                is_student_handout=True,
            )
            st.download_button(
                "Scaffolded Worksheet (.docx)",
                data=scaf_bytes,
                file_name=f"Chp_{gal_print_ch_num:02d}_Sec_{gal_sec_code}_Scaffolded.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with d_c3:
            key_bytes = get_docx_bytes(
                gal_pkt["teacher_key_md"],
                f"Chp_{gal_print_ch_num:02d}_Sec_{gal_sec_code}_Teacher_Key",
                is_student_handout=False,
                include_top_student_header=False,
            )
            st.download_button(
                "Teacher Clipboard Key (.docx)",
                data=key_bytes,
                file_name=f"Chp_{gal_print_ch_num:02d}_Sec_{gal_sec_code}_Teacher_Key.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with d_c4:
            sec_pdf_path = resolve_file_path(gal_selected_sec.get("pdf_file"))
            if sec_pdf_path and sec_pdf_path.exists():
                st.download_button(
                    "Original Textbook 2-Page PDF",
                    data=sec_pdf_path.read_bytes(),
                    file_name=sec_pdf_path.name,
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.button("Textbook PDF Unavailable", disabled=True, use_container_width=True)

        g_col1, g_col2 = st.columns([1.5, 1.2])
        with g_col1:
            if st.button(
                f"Export Sec. {gal_sec_code} to Google Drive",
                type="primary",
                use_container_width=True,
                key=f"btn_gal_gdrive_{gal_print_ch_num}_{gal_sec_code}",
            ):
                with st.spinner("Exporting Section to Google Drive..."):
                    try:
                        g_res = export_section_packet_to_google_drive(
                            section_meta=gal_selected_sec,
                            packet_data=gal_pkt,
                            include_scaffolded=True,
                            include_section_pdf=True,
                        )
                        st.success(
                            f"Exported to Google Drive Folder: **{g_res['folder_path']}**\n\n"
                            f"- [Open Folder in Drive]({g_res['folder_url']})\n"
                            f"- [Standard Worksheet (Google Doc)]({g_res['student_standard']['url']})\n"
                            f"- [Scaffolded Worksheet (Google Doc)]({g_res['student_scaffolded']['url']})\n"
                            f"- [Teacher Answer Key (Google Doc)]({g_res['teacher_key']['url']})"
                        )
                    except Exception as e:
                        st.error(f"Google Drive export error: {e}")
        with g_col2:
            st.info("Tip: Open the downloaded .docx in Word / Google Docs for native printing, or print directly from your browser (Ctrl+P) on the preview below.")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        prev_std, prev_scaf, prev_key, prev_text = st.tabs([
            "Standard Student Worksheet",
            "Scaffolded Student Worksheet",
            "Teacher Clipboard Answer Key",
            "2-Page Textbook Passage",
        ])
        with prev_std:
            st.markdown(format_booklet_for_web(gal_pkt["student_standard_md"]), unsafe_allow_html=True)
        with prev_scaf:
            st.markdown(format_booklet_for_web(gal_pkt["student_scaffolded_md"]), unsafe_allow_html=True)
        with prev_key:
            st.markdown(gal_pkt["teacher_key_md"])
        with prev_text:
            if gal_selected_sec.get("printed_main_idea"):
                st.info(f"**Printed Textbook MAIN IDEA (p. {gal_selected_sec.get('start_page', '')}):** *{gal_selected_sec['printed_main_idea']}*")
            if gal_raw_passage_md:
                with st.container(height=520):
                    st.markdown(gal_raw_passage_md)
            else:
                st.warning("Textbook passage markdown file could not be loaded.")

    with main_gal_tab2:
        st.markdown("### Interactive Worksheet Strategy & Template Models")
        st.caption(
            "Browse concrete student handout formats, anti-copycat mechanics, and completed 8th-grade student exemplars based on **Chapter 5: The Road to Revolution**. "
            "Use this gallery to see exactly what students will see and write on their printed worksheets before you generate your chapter package."
        )

        gal_tab1, gal_tab2, gal_tab3, gal_tab4, gal_tab5 = st.tabs([
            "1. Central Idea Strategies (4 Models)",
            "2. Anti-Copycat Modes (3 Mechanics)",
            "3. Active Reading Organizers (5 Structures)",
            "4. Covers & Footers (7 Layouts)",
            "5. Writing Extensions (The Writing Revolution)",
        ])

        with gal_tab1:
            st.markdown("#### Central Idea Synthesis Templates (CCSS RH.6-8.2)")
            st.caption("Teach 8th graders to determine the central ideas of a historical text and formulate concise, evidence-based historical claims.")

            ci_choice = st.selectbox(
                "Select Central Idea Template to Explore:",
                options=[s["code"] for s in CENTRAL_IDEA_STRATEGIES],
                format_func=lambda c: get_strategy_by_code(CENTRAL_IDEA_STRATEGIES, c)["name"],
                key="gal_ci_select",
            )
            ci_curr = get_strategy_by_code(CENTRAL_IDEA_STRATEGIES, ci_choice)

            c_info_c1, c_info_c2 = st.columns([1.5, 1.0])
            with c_info_c1:
                st.markdown(f"**Target ELA Standard:** `CCSS RH.6-8.2` (Determine Central Idea & Summary)")
                st.markdown(f"**Best For:** {ci_curr['best_for']}")
                st.markdown(f"**How It Works:** {ci_curr['description']}")
            with c_info_c2:
                if st.button(f"Apply '{ci_curr['short_name']}' to Chapter {selected_ch_num} Blueprint", use_container_width=True, key=f"btn_apply_ci_{selected_ch_num}"):
                    ch_blueprint["central_idea_strategy"] = ci_choice
                    save_chapter_blueprint(selected_ch_num, ch_blueprint)
                    st.success(f"Saved! '{ci_curr['short_name']}' is now set as the active Central Idea strategy for Chapter {selected_ch_num} in the Packet Co-Designer.")
                st.caption(f"Applies this strategy directly to Chapter {selected_ch_num} in Step 2 of the Packet Co-Designer.")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            ci_view1, ci_view2 = st.columns(2)
            with ci_view1:
                st.markdown("##### Printed Student Handout Format")
                st.markdown(render_preview_handout(ci_choice), unsafe_allow_html=True)
                if ci_curr.get("scaffolded_md"):
                    st.markdown(render_preview_scaffold(ci_curr["scaffolded_md"]), unsafe_allow_html=True)

            with ci_view2:
                st.markdown("##### Authentic 8th-Grade Student Exemplar (Ch. 5)")
                st.markdown(render_preview_exemplar(ci_choice), unsafe_allow_html=True)

        with gal_tab2:
            st.markdown("#### Anti-Copycat Modes for Textbook's Printed MAIN IDEA Box")
            st.caption("Guarantees students cannot blindly copy the textbook's printed 1-sentence Main Idea box as their own answer.")

            pmi_choice = st.selectbox(
                "Select Anti-Copycat Mode to Explore:",
                options=[m["code"] for m in PRINTED_MAIN_IDEA_MODES],
                format_func=lambda c: get_strategy_by_code(PRINTED_MAIN_IDEA_MODES, c)["name"],
                key="gal_pmi_select",
            )
            pmi_curr = get_strategy_by_code(PRINTED_MAIN_IDEA_MODES, pmi_choice)

            p_info_c1, p_info_c2 = st.columns([1.5, 1.0])
            with p_info_c1:
                st.markdown(f"**Pedagogical Mechanic:** {pmi_curr['description']}")
            with p_info_c2:
                if st.button(f"Apply '{pmi_curr['short_name']}' to Chapter {selected_ch_num} Blueprint", use_container_width=True, key=f"btn_apply_pmi_{selected_ch_num}"):
                    ch_blueprint["printed_main_idea_mode"] = pmi_choice
                    save_chapter_blueprint(selected_ch_num, ch_blueprint)
                    st.success(f"Saved! '{pmi_curr['short_name']}' is now set as the active anti-copycat mechanic for Chapter {selected_ch_num} in the Packet Co-Designer.")
                st.caption(f"Applies this mechanic directly to Chapter {selected_ch_num} in Step 2 of the Packet Co-Designer.")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            pmi_view1, pmi_view2 = st.columns(2)
            with pmi_view1:
                st.markdown("##### Printed Student Handout Format")
                st.markdown(render_preview_handout(pmi_choice), unsafe_allow_html=True)
                if pmi_curr.get("scaffolded_md"):
                    st.markdown(render_preview_scaffold(pmi_curr["scaffolded_md"]), unsafe_allow_html=True)

            with pmi_view2:
                st.markdown("##### Authentic 8th-Grade Student Exemplar (Ch. 5)")
                st.markdown(render_preview_exemplar(pmi_choice), unsafe_allow_html=True)

        with gal_tab3:
            st.markdown("#### Active Reading & Text Structure Organizers (CCSS RH.6-8.5)")
            st.caption("Active reading organizers guide students through each 2-page spread according to its specific historical text structure.")

            ro_choice = st.selectbox(
                "Select Active Reading Organizer to Explore:",
                options=[r["code"] for r in READING_ORGANIZERS],
                format_func=lambda c: get_strategy_by_code(READING_ORGANIZERS, c)["name"],
                key="gal_ro_select",
            )
            ro_curr = get_strategy_by_code(READING_ORGANIZERS, ro_choice)

            r_info_c1, r_info_c2 = st.columns([1.5, 1.0])
            with r_info_c1:
                st.markdown(f"**Target ELA Standard:** `CCSS RH.6-8.5` (Analyze Text Structure)")
                st.markdown(f"**Text Structure Focus:** {ro_curr['description']}")
            with r_info_c2:
                if st.button(f"Apply '{ro_curr['short_name']}' to Chapter {selected_ch_num} Blueprint", use_container_width=True, key=f"btn_apply_ro_{selected_ch_num}"):
                    ch_blueprint["reading_organizer"] = ro_choice
                    save_chapter_blueprint(selected_ch_num, ch_blueprint)
                    st.success(f"Saved! '{ro_curr['short_name']}' is now set as the active graphic organizer for Chapter {selected_ch_num} in the Packet Co-Designer.")
                st.caption(f"Applies this structure directly to Chapter {selected_ch_num} in Step 2 of the Packet Co-Designer.")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            ro_view1, ro_view2 = st.columns(2)
            with ro_view1:
                st.markdown("##### Printed Student Handout Format")
                st.markdown(render_preview_handout(ro_choice), unsafe_allow_html=True)
                if ro_curr.get("scaffolded_md"):
                    st.markdown(render_preview_scaffold(ro_curr["scaffolded_md"]), unsafe_allow_html=True)

            with ro_view2:
                st.markdown("##### Authentic 8th-Grade Student Exemplar (Ch. 5)")
                st.markdown(render_preview_exemplar(ro_choice), unsafe_allow_html=True)

        with gal_tab4:
            st.markdown("#### Booklet Front Cover Pages & Page Footer Check Boxes")
            st.caption("Inspect how the cumulative front cover study guide and daily footer check boxes look when printed.")

            cov_c1, cov_c2 = st.columns(2)
            with cov_c1:
                st.markdown("##### Booklet Front Cover Options")
                gal_cov_choice = st.selectbox(
                    "Choose Cover Format to Preview:",
                    options=[c["code"] for c in COVER_PAGE_MODES],
                    format_func=lambda c: get_strategy_by_code(COVER_PAGE_MODES, c)["name"],
                    key="gal_cov_select_box",
                )
                g_cov_item = get_strategy_by_code(COVER_PAGE_MODES, gal_cov_choice)
                st.markdown(f"**How It Functions:** {g_cov_item['description']}")
                st.markdown(render_preview_cover(gal_cov_choice), unsafe_allow_html=True)
                if st.button(f"Apply '{g_cov_item['short_name']}' to Chapter {selected_ch_num}", key="btn_apply_cov"):
                    ch_blueprint["cover_page_mode"] = gal_cov_choice
                    save_chapter_blueprint(selected_ch_num, ch_blueprint)
                    st.success(f"Saved! '{g_cov_item['short_name']}' is now set as the active cover page for Chapter {selected_ch_num} in the Packet Co-Designer.")
                st.caption(f"Applies this cover style directly to Chapter {selected_ch_num} in Step 2 of the Packet Co-Designer.")

            with cov_c2:
                st.markdown("##### Page Footer Check Box Options")
                gal_gb_choice = st.selectbox(
                    "Choose Footer Check Box Layout to Preview:",
                    options=[g["code"] for g in GRADE_BOX_MODES],
                    format_func=lambda c: get_strategy_by_code(GRADE_BOX_MODES, c)["name"],
                    key="gal_gb_select_box",
                )
                g_gb_item = get_strategy_by_code(GRADE_BOX_MODES, gal_gb_choice)
                st.markdown(f"**Grading Use:** {g_gb_item['description']}")
                st.markdown(render_preview_footer(gal_gb_choice), unsafe_allow_html=True)
                if st.button(f"Apply '{g_gb_item['short_name']}' to Chapter {selected_ch_num}", key="btn_apply_gb"):
                    ch_blueprint["grade_box_mode"] = gal_gb_choice
                    save_chapter_blueprint(selected_ch_num, ch_blueprint)
                    st.success(f"Saved! '{g_gb_item['short_name']}' is now set as the active footer layout for Chapter {selected_ch_num} in the Packet Co-Designer.")
                st.caption(f"Applies this footer layout directly to Chapter {selected_ch_num} in Step 2 of the Packet Co-Designer.")

        with gal_tab5:
            st.markdown("#### Optional Writing Extensions (The Writing Revolution)")
            st.caption("Sentence-level writing extensions grounded in Judith Hochman's The Writing Revolution (TWR) — completely optional and turned off by default.")

            twr_active = [t for t in OPTIONAL_TWR_STRATEGIES if t["code"] != "twr_none"]
            twr_choice = st.selectbox(
                "Select Writing Extension to Explore:",
                options=[t["code"] for t in twr_active],
                format_func=lambda c: get_strategy_by_code(twr_active, c)["name"],
                key="gal_twr_select",
            )
            twr_curr = get_strategy_by_code(twr_active, twr_choice)

            w_info_c1, w_info_c2 = st.columns([1.5, 1.0])
            with w_info_c1:
                st.markdown(f"**Target Standard:** `CCSS WHST.6-8.2` (Informative Historical Writing)")
                st.markdown(f"**Writing Objective:** {twr_curr['description']}")
            with w_info_c2:
                if st.button(f"Apply '{twr_curr['short_name']}' to Chapter {selected_ch_num} Blueprint", use_container_width=True, key=f"btn_apply_twr_{selected_ch_num}"):
                    ch_blueprint["optional_twr_strategy"] = twr_choice
                    save_chapter_blueprint(selected_ch_num, ch_blueprint)
                    st.success(f"Saved! '{twr_curr['short_name']}' is now set as the active writing extension for Chapter {selected_ch_num} in the Packet Co-Designer.")
                st.caption(f"Applies this writing extension directly to Chapter {selected_ch_num} in Step 2 of the Packet Co-Designer.")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            twr_view1, twr_view2 = st.columns(2)
            with twr_view1:
                st.markdown("##### Printed Student Handout Format")
                st.markdown(render_preview_handout(twr_choice), unsafe_allow_html=True)
            with twr_view2:
                st.markdown("##### Authentic 8th-Grade Student Exemplar (Ch. 5)")
                st.markdown(render_preview_exemplar(twr_choice), unsafe_allow_html=True)
