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
    format_half_sheet_2up,
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
        margin: 0 auto !important;
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
        border-radius: 14px;
        padding: 2.2rem 2.0rem 2.0rem 2.0rem;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-decoration: none !important;
        color: inherit !important;
        box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.06);
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.22s ease;
        margin-bottom: 0.75rem;
    }
    .hero-blue {
        border-top: 6px solid #2563eb !important;
        background: linear-gradient(180deg, #eff6ff 0%, #ffffff 48%);
    }
    .hero-indigo {
        border-top: 6px solid #6366f1 !important;
        background: linear-gradient(180deg, #eef2ff 0%, #ffffff 48%);
    }
    .hero-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.75rem;
        line-height: 1.25;
        display: block;
    }
    .hero-desc {
        font-size: 1.05rem;
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0;
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

    /* Selectbox Dropdowns: Visible Border & Contrast */
    div[data-testid="stSelectbox"] div[role="group"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border: 1.5px solid #94a3b8 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
        transition: all 0.15s ease-in-out !important;
    }
    div[data-testid="stSelectbox"] div[role="group"]:hover,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
        border-color: #1e3a8a !important;
        box-shadow: 0 2px 4px rgba(30, 58, 138, 0.12) !important;
    }
    div[data-testid="stSelectbox"] div[role="group"]:focus-within,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
        border-color: #1e3a8a !important;
        box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.20) !important;
    }

    /* Strategy Gallery Tiles: Interactive Card & Hover Zoom */
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]) {
        position: relative !important;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]):hover {
        transform: translateY(-4px) scale(1.025) !important;
        z-index: 20 !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]) div.strategy-tile-card {
        transition: border-color 0.22s ease, box-shadow 0.22s ease !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]):hover div.strategy-tile-card {
        border-color: #1e3a8a !important;
        box-shadow: 0 12px 28px -4px rgba(30, 58, 138, 0.16), 0 6px 12px -4px rgba(15, 23, 42, 0.08) !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]):active {
        transform: translateY(-1px) scale(0.99) !important;
    }

    /* Full Tile Invisible Button Overlay */
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]) div[class*="st-key-btn_tile_"],
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]) div[class*="st-key-btn_hero_"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]) div[class*="st-key-btn_tile_"] div.stButton,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tile_"]) div[class*="st-key-btn_tile_"] div.stButton button,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]) div[class*="st-key-btn_hero_"] div.stButton,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]) div[class*="st-key-btn_hero_"] div.stButton button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }

    /* Hero Pathway Cards Column Hover */
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]) {
        position: relative !important;
        cursor: pointer !important;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]):hover {
        transform: translateY(-4px) scale(1.015) !important;
        z-index: 10 !important;
    }
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]):hover .hero-card {
        box-shadow: 0 16px 32px -4px rgba(15, 23, 42, 0.12), 0 6px 12px -4px rgba(15, 23, 42, 0.06) !important;
    }
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]):hover .hero-blue {
        border-color: #93c5fd !important;
        border-top: 6px solid #1d4ed8 !important;
    }
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_hero_"]):hover .hero-indigo {
        border-color: #c7d2fe !important;
        border-top: 6px solid #4f46e5 !important;
    }

    /* Dynamic Page Tray Horizontal Scrolling Container */
    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-btn_tray_tile_"]) {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        flex-wrap: nowrap !important;
        display: flex !important;
        align-items: stretch !important;
        gap: 14px !important;
        padding: 0.6rem 0.4rem 1.1rem 0.4rem !important;
        scrollbar-width: thin !important;
        scrollbar-color: #3b82f6 #f1f5f9 !important;
        -webkit-overflow-scrolling: touch !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-btn_tray_tile_"])::-webkit-scrollbar {
        height: 10px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-btn_tray_tile_"])::-webkit-scrollbar-track {
        background: #f1f5f9 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-btn_tray_tile_"])::-webkit-scrollbar-thumb {
        background: #cbd5e1 !important;
        border-radius: 6px !important;
        border: 2px solid #f1f5f9 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-btn_tray_tile_"])::-webkit-scrollbar-thumb:hover {
        background: #1e3a8a !important;
    }

    /* Fixed Card Dimensions for Tray Tiles (Prevents Squishing on Many Pages) */
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]),
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_add_tray_page"]) {
        flex: 0 0 185px !important;
        min-width: 185px !important;
        max-width: 185px !important;
        width: 185px !important;
        position: relative !important;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]):hover,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_add_tray_page"]):hover {
        transform: translateY(-4px) scale(1.025) !important;
        z-index: 15 !important;
    }

    .tray-preview-card {
        transition: border-color 0.22s ease, box-shadow 0.22s ease !important;
        border-radius: 10px;
        padding: 0.75rem;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        position: relative;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]):hover .tray-preview-card {
        border-color: #1e3a8a !important;
        box-shadow: 0 12px 28px -4px rgba(30, 58, 138, 0.16), 0 6px 12px -4px rgba(15, 23, 42, 0.08) !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]):active .tray-preview-card,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_add_tray_page"]):active .tray-add-card {
        transform: translateY(-1px) scale(0.99) !important;
    }

    /* Invisible overlay button that turns the whole tile into a button */
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]) div[class*="st-key-btn_tray_tile_"],
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_add_tray_page"]) div[class*="st-key-btn_add_tray_page"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]) div[class*="st-key-btn_tray_tile_"] div.stButton,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]) div[class*="st-key-btn_tray_tile_"] div.stButton button,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_add_tray_page"]) div[class*="st-key-btn_add_tray_page"] div.stButton,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_add_tray_page"]) div[class*="st-key-btn_add_tray_page"] div.stButton button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }

    /* Small, visible 'X' Delete Button on the Tile */
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_del_"]) div[class*="st-key-btn_tray_del_"] {
        position: absolute !important;
        top: 8px !important;
        right: 10px !important;
        z-index: 25 !important;
        width: 24px !important;
        height: 24px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_del_"]) div[class*="st-key-btn_tray_del_"] div.stButton,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_del_"]) div[class*="st-key-btn_tray_del_"] div.stButton button {
        width: 24px !important;
        height: 24px !important;
        min-height: 24px !important;
        max-height: 24px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.70rem !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        background: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        color: #64748b !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08) !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        opacity: 1 !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_del_"]) div[class*="st-key-btn_tray_del_"] div.stButton button:hover {
        background: #fee2e2 !important;
        border-color: #ef4444 !important;
        color: #b91c1c !important;
        transform: scale(1.15) !important;
    }

    .tray-sheet-mockup {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.45rem;
        height: 110px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin: 0.35rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_tray_tile_"]):hover .tray-sheet-mockup {
        transform: scale(1.03) !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
    }

    .tray-add-card {
        border: 2px dashed #94a3b8;
        background: #f8fafc;
        border-radius: 10px;
        padding: 0.75rem;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-bottom: 0.5rem;
        transition: all 0.22s ease !important;
    }

    div[data-testid="stColumn"]:has(div[class*="st-key-btn_add_tray_page"]):hover .tray-add-card {
        border-color: #1e3a8a !important;
        background: #eff6ff !important;
    }

    /* ── Horizontal Page Inspector Navigation ── */
    .inspector-tile {
        border-radius: 8px;
        padding: 0.5rem 0.6rem;
        cursor: pointer;
        transition: all 0.18s ease;
        text-align: center;
        height: 75px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 0.35rem;
    }
    .inspector-tile-active {
        border: 2.5px solid #1e3a8a !important;
        background: #eff6ff !important;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.12) !important;
    }
    .inspector-tile-inactive {
        border: 1.5px solid #cbd5e1 !important;
        background: #ffffff !important;
    }
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_insp_page_"]):hover .inspector-tile-inactive {
        border-color: #1e3a8a !important;
        background: #f8fafc !important;
        transform: translateY(-2px);
    }

    /* Invisible overlay button on inspector tiles */
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_insp_page_"]) {
        position: relative !important;
        cursor: pointer !important;
    }
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_insp_page_"]) div[class*="st-key-btn_insp_page_"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_insp_page_"]) div[class*="st-key-btn_insp_page_"] div.stButton,
    div[data-testid="stColumn"]:has(div[class*="st-key-btn_insp_page_"]) div[class*="st-key-btn_insp_page_"] div.stButton button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }

    /* Arrow buttons in-line with inspector tiles */
    div[class*="st-key-btn_prev_page"] div.stButton button,
    div[class*="st-key-btn_next_page"] div.stButton button {
        height: 75px !important;
        min-height: 75px !important;
        max-height: 75px !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #f1f5f9 !important;
        border: 1.5px solid #cbd5e1 !important;
        color: #1e293b !important;
    }
    div[class*="st-key-btn_prev_page"] div.stButton button:hover,
    div[class*="st-key-btn_next_page"] div.stButton button:hover {
        background: #e2e8f0 !important;
        border-color: #1e3a8a !important;
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
def load_catalog(_mtime: float = 0.0) -> List[Dict[str, Any]]:
    cat_path = Path("output/catalog.json")
    if not cat_path.exists():
        return []
    return json.loads(cat_path.read_text(encoding="utf-8"))


@st.cache_data
def load_vocab_index(_mtime: float = 0.0) -> Dict[str, Any]:
    vp = Path("output/vocab_index.json")
    if not vp.exists():
        return {}
    return json.loads(vp.read_text(encoding="utf-8"))


@st.cache_data
def load_chapter_reviews(_mtime: float = 0.0) -> Dict[str, Any]:
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


def _render_strategy_card_grid(
    tiles_list: List[Dict[str, Any]],
    active_code: Optional[str],
    key_prefix: str,
    btn_label_selected: str = "Active Layout",
    btn_label_unselected: str = "Select This Layout",
) -> None:
    """Renders a responsive 3-column card grid where the tiles themselves are the interactive buttons with hover zoom."""
    grid_cols_per_row = 3
    for row_start in range(0, len(tiles_list), grid_cols_per_row):
        row_tiles = tiles_list[row_start : row_start + grid_cols_per_row]
        cols = st.columns(grid_cols_per_row)

        for col_idx, tile in enumerate(row_tiles):
            with cols[col_idx]:
                is_sel = (tile["code"] == active_code)
                border_style = "border: 2.5px solid #1e3a8a; background: #f0f7ff;" if is_sel else "border: 1.5px solid #cbd5e1; background: #ffffff;"
                sel_badge_html = '<span style="font-size: 0.72rem; font-weight: 700; color: #1e3a8a;">Active</span>' if is_sel else ''
                clean_thumb = re.sub(r">\s*\n\s*<", "><", re.sub(r"\n\s*", " ", tile["thumbnail_svg"].strip()))

                card_html = (
                    f'<div class="strategy-tile-card{" strategy-tile-active" if is_sel else ""}" '
                    f'style="{border_style} border-radius: 10px; padding: 0.75rem; margin-bottom: 0.85rem; min-height: 255px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">'
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

                # Invisible full-card overlay button: clicking anywhere on the tile selects that layout
                btn_acc_label = f"{tile['name']} - Active" if is_sel else f"Select {tile['name']}"
                if st.button(
                    btn_acc_label,
                    key=f"btn_tile_{key_prefix}_{tile['code']}",
                    use_container_width=True,
                ):
                    st.session_state["gal_active_tile_code"] = tile["code"]
                    st.rerun()


@st.dialog("Full-Size Page Preview", width="large")
def show_page_preview_modal(p_cfg: Dict[str, Any], page_num: int):
    """Renders a responsive, full-size modal dialog for inspecting an individual page from the Dynamic Page Tray."""
    s_meta = p_cfg.get("section_meta", {})
    s_code = s_meta.get("section_code", "?")
    s_type = p_cfg.get("strategy_type", "central_idea")
    s_strat = p_cfg.get("strategy_code", "ci_01_subheading_gist")
    is_scaf = bool(p_cfg.get("is_scaffolded", False))
    raw_md = p_cfg.get("raw_passage_md", "")

    tile = get_tile_by_code(s_strat)
    strat_name = tile["name"] if tile else s_strat.replace("_", " ").title()

    render_clean_html(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; padding-bottom: 0.45rem; border-bottom: 1.5px solid #e2e8f0;">
            <div>
                <span class="badge-pill" style="font-size: 0.85rem; padding: 0.22rem 0.65rem; background: #dbeafe; color: #1e3a8a;">Page {page_num}: Sec {s_code}</span>
                <span style="font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-left: 0.4rem;">{strat_name}</span>
            </div>
            <div>
                {'<span class="badge-pill badge-scaf">Scaffolded Edition</span>' if is_scaf else '<span class="badge-pill badge-gray">Standard Edition</span>'}
            </div>
        </div>
        """
    )

    handout = build_standalone_strategy_handout(
        section_meta=s_meta,
        strategy_category=s_type,
        strategy_code=s_strat,
        markdown_text=raw_md,
        is_scaffolded=is_scaf,
    )

    std_md = handout["student_scaffolded_md" if is_scaf else "student_standard_md"]
    ex_md = handout["exemplar_md"]

    std_html = format_booklet_for_web(std_md)
    ex_html = format_booklet_for_web(ex_md)

    tab_std, tab_ex = st.tabs([
        f"Student Handout ({'Scaffolded' if is_scaf else 'Standard'})",
        "Teacher Answer Key & Exemplar",
    ])
    with tab_std:
        st.markdown(std_html, unsafe_allow_html=True)
    with tab_ex:
        st.markdown(ex_html, unsafe_allow_html=True)


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


cat_p = Path("output/catalog.json")
cat_mtime = cat_p.stat().st_mtime if cat_p.exists() else 0.0
catalog = load_catalog(cat_mtime)

vocab_p = Path("output/vocab_index.json")
vocab_mtime = vocab_p.stat().st_mtime if vocab_p.exists() else 0.0
vocab_index = load_vocab_index(vocab_mtime)

reviews_p = Path("output/chapter_reviews.json")
reviews_mtime = reviews_p.stat().st_mtime if reviews_p.exists() else 0.0
chapter_reviews = load_chapter_reviews(reviews_mtime)

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
    if target_nav in ["packet", "packet_export", "gallery", "home"]:
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

selected_ch_num = st.session_state["selected_ch_num"]
ch_info = chapters_map[selected_ch_num]
ch_sections = ch_info["sections"]
ch_std_info = CHAPTER_STANDARDS_MAP.get(str(selected_ch_num), CHAPTER_STANDARDS_MAP.get("5", {}))
raw_unit = str(ch_info['unit_title'])
display_unit = raw_unit if raw_unit.lower().startswith("unit") else f"Unit {ch_info['unit_num']}: {raw_unit}"
eq_text = ch_std_info.get('essential_question', '')

# Render full contextual banner & chapter selector on Home Gateway screen
if st.session_state["nav_view"] == "home":
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

    banner_html = (
        '<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 5px solid #1e3a8a; border-radius: 8px; padding: 0.85rem 1.15rem; margin-bottom: 1.0rem; display: grid; grid-template-columns: 1fr auto 2fr auto 1fr; align-items: center; gap: 1.25rem;">'
        '<div style="text-align: left;">'
        '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Curriculum Unit</div>'
        f'<div style="font-size: 0.95rem; font-weight: 600; color: #0f172a; line-height: 1.35;">{display_unit}</div>'
        '</div>'
        '<div style="width: 1.5px; height: 38px; background: #cbd5e1;"></div>'
        '<div style="text-align: center; padding: 0 0.5rem;">'
        '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Essential Question</div>'
        f'<div style="font-size: 0.88rem; font-style: italic; color: #1e293b; line-height: 1.4;">"{eq_text}"</div>'
        '</div>'
        '<div style="width: 1.5px; height: 38px; background: #cbd5e1;"></div>'
        '<div style="text-align: right;">'
        '<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.2rem;">Google Drive Folder</div>'
        f'<div style="font-size: 0.82rem; background: #e2e8f0; padding: 0.35rem 0.75rem; border-radius: 6px; color: #0f172a; font-family: monospace; font-weight: 600; white-space: nowrap; display: inline-block;">{ROOT_FOLDER_NAME}</div>'
        '</div>'
        '</div>'
    )
    render_clean_html(banner_html)


# ─────────────────────────────────────────────────────────────────────────────
# 2. SCREEN 0: THE GATEWAY (HOME SCREEN)
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state["nav_view"] == "home":
    render_clean_html(
        """
        <div style="text-align: center; margin-top: 0.5rem; margin-bottom: 2.0rem;">
            <div style="font-size: 2.25rem; font-weight: 800; color: #0f172a; letter-spacing: -0.025em; line-height: 1.15; margin: 0 0 0.25rem 0;">
                Curriculum Design Studio
            </div>
            <div style="font-size: 1.22rem; font-weight: 600; color: #2563eb; font-style: italic; margin: 0 0 0.65rem 0;">
                What would you like to create today?
            </div>
            <div style="width: 44px; height: 3px; background: #93c5fd; border-radius: 2px; margin: 0 auto 0.65rem auto;"></div>
            <div style="font-size: 0.92rem; color: #64748b; font-weight: 400; letter-spacing: 0.01em;">
                Select one of the options below to get started!
            </div>
        </div>
        """
    )

    h_col1, h_col2 = st.columns(2)

    with h_col1:
        render_clean_html(
            """
            <div class="hero-card hero-blue">
                <span class="hero-title" style="color: #1d4ed8;">Packet Builder</span>
                <span class="hero-desc">
                    Customize 2-page, 3-page, or chapter packets, page-by-page. Then export them as PDFs!
                </span>
            </div>
            """
        )
        if st.button("Packet Builder", use_container_width=True, key="btn_hero_packet"):
            st.session_state["nav_view"] = "packet"
            st.rerun()

    with h_col2:
        render_clean_html(
            """
            <div class="hero-card hero-indigo">
                <span class="hero-title" style="color: #4338ca;">Worksheet Gallery</span>
                <span class="hero-desc">
                    Explore the full run of available strategies, and print individual student handouts!
                </span>
            </div>
            """
        )
        if st.button("Worksheet Gallery", use_container_width=True, key="btn_hero_gallery"):
            st.session_state["nav_view"] = "gallery"
            st.session_state["gal_active_tile_code"] = None
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# 3. PATH A: MODULAR CURRICULUM PACKET BUILDER
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "packet":

    # Breadcrumb Header
    b_col1, b_col2, b_col3, b_col4 = st.columns([1.1, 2.5, 0.8, 0.7])
    with b_col1:
        if st.button("<- Main Menu", use_container_width=True, key="btn_back_packet"):
            st.session_state["nav_view"] = "home"
            st.rerun()
    with b_col2:
        render_clean_html(
            f"""
            <div style="padding-top: 0.2rem;">
                <span class="badge-pill" style="font-size: 0.86rem; padding: 0.30rem 0.75rem;">
                    <b>Pathway 1:</b> Modular Packet Builder &bull; Chapter {selected_ch_num:02d}
                </span>
            </div>
            """
        )
    with b_col3:
        with st.popover("Context"):
            st.markdown(f"**Curriculum Unit:** {display_unit}")
            st.markdown(f"**Essential Question:** *\"{eq_text}\"*")
            st.markdown(f"**Google Drive Folder:** `{ROOT_FOLDER_NAME}`")
    with b_col4:
        if st.button("Log Out", key="packet_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

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

    def _apply_packet_scope(scope_name: str):
        if scope_name == "Chapter Packet (Unit Booklet)":
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
        else:
            # Section Packet (Single Spread Focus)
            cur_active_sec = None
            if tray_pages and 0 <= active_idx < len(tray_pages):
                cur_active_sec = tray_pages[active_idx].get("section_meta")
            sec_target = cur_active_sec or (ch_sections[0] if ch_sections else None)
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
            else:
                st.session_state["tray_pages"] = []
            st.session_state["active_tray_idx"] = 0
            st.session_state["include_cover_toggle"] = False

    def on_packet_scope_change():
        scope = st.session_state.get("packet_scope_radio")
        _apply_packet_scope(scope)

    sc_c1, sc_c2 = st.columns(2)
    with sc_c1:
        packet_scope = st.radio(
            "Packet Scope:",
            options=["Section Packet (Single Spread Focus)", "Chapter Packet (Unit Booklet)"],
            horizontal=True,
            key="packet_scope_radio",
            on_change=on_packet_scope_change,
        )
    with sc_c2:
        creation_mode = st.radio(
            "Configuration Mode:",
            options=["Pre-Built Presets (Recommended)", "Start from Scratch (Blank Canvas)"],
            horizontal=True,
            key="packet_mode_radio",
        )

    def on_click_preset_2page():
        st.session_state["packet_scope_radio"] = "Section Packet (Single Spread Focus)"
        _apply_packet_scope("Section Packet (Single Spread Focus)")

    def on_click_preset_3page():
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
                    "strategy_code": "twr_because_but_so",
                    "is_scaffolded": False,
                    "raw_passage_md": sec_md,
                },
            ]
        st.session_state["active_tray_idx"] = 0
        st.session_state["include_cover_toggle"] = False
        st.session_state["packet_scope_radio"] = "Section Packet (Single Spread Focus)"

    def on_click_preset_full_unit():
        st.session_state["packet_scope_radio"] = "Chapter Packet (Unit Booklet)"
        _apply_packet_scope("Chapter Packet (Unit Booklet)")

    # If Pre-Built Presets is selected, offer 1-click preset buttons
    if creation_mode == "Pre-Built Presets (Recommended)":
        st.caption("Apply a pre-configured pedagogical structure to your dynamic page tray:")
        p_c1, p_c2, p_c3 = st.columns(3)

        with p_c1:
            st.button(
                "Quick 2-Page Section Spread",
                use_container_width=True,
                key="preset_2page",
                on_click=on_click_preset_2page,
            )

        with p_c2:
            st.button(
                "3-Page Complete Lesson",
                use_container_width=True,
                key="preset_3page",
                on_click=on_click_preset_3page,
            )

        with p_c3:
            st.button(
                "Full Chapter Unit Booklet",
                use_container_width=True,
                key="preset_full_unit",
                on_click=on_click_preset_full_unit,
            )

    # ── Step 2: Dynamic Horizontal Page Tray with Live Preview Tiles ──
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    total_pages = len(tray_pages)
    total_sheets = (total_pages + 1) // 2

    t_head_c1, t_head_c2 = st.columns([2.3, 1.7])
    with t_head_c1:
        st.markdown("#### Step 2: Dynamic Page Tray — Live Preview & Configure Every Page")
        st.caption("Click any page tile below to edit its section spread and strategy. If a page is already active, clicking it again opens the full-size preview modal.")
    with t_head_c2:
        if total_pages > 4:
            jp_prev, jp_sel, jp_next = st.columns([0.6, 2.2, 0.6])
            with jp_prev:
                if st.button("◀", key="btn_tray_prev_quick", help="Previous Page", disabled=(active_idx == 0), use_container_width=True):
                    st.session_state["active_tray_idx"] = max(0, active_idx - 1)
                    st.rerun()
            with jp_sel:
                def on_tray_jump_change():
                    st.session_state["active_tray_idx"] = st.session_state["tray_jump_selector"]

                st.selectbox(
                    "Quick Jump:",
                    options=list(range(total_pages)),
                    index=active_idx,
                    format_func=lambda idx: f"Page {idx+1}: Sec {tray_pages[idx]['section_meta'].get('section_code', '?')} ({tray_pages[idx].get('strategy_code', '').replace('_', ' ').title()[:16]})",
                    key="tray_jump_selector",
                    on_change=on_tray_jump_change,
                    label_visibility="collapsed",
                )
            with jp_next:
                if st.button("▶", key="btn_tray_next_quick", help="Next Page", disabled=(active_idx >= total_pages - 1), use_container_width=True):
                    st.session_state["active_tray_idx"] = min(total_pages - 1, active_idx + 1)
                    st.rerun()

    total_pages = len(tray_pages)
    total_sheets = (total_pages + 1) // 2

    # Render horizontal sequence of live preview tiles
    tray_cols = st.columns(total_pages + 1 if total_pages > 0 else 1)

    for i, p in enumerate(tray_pages):
        with tray_cols[i]:
            is_active = (i == active_idx)
            s_meta = p.get("section_meta", {})
            s_code = s_meta.get("section_code", "?")
            s_strat = p.get("strategy_code", "")
            tile_match = get_tile_by_code(s_strat)
            s_name = tile_match["name"] if tile_match else s_strat.replace("_", " ").title()
            is_scaf = p.get("is_scaffolded", False)
            scaf_badge = '<span class="badge-pill badge-scaf" style="font-size: 0.65rem; padding: 1px 5px; margin-left: 0.25rem;">Scaffolded</span>' if is_scaf else ''
            clean_thumb = re.sub(r">\s*\n\s*<", "><", re.sub(r"\n\s*", " ", tile_match["thumbnail_svg"].strip())) if tile_match else ""

            if is_active:
                status_pill = '<span class="badge-pill" style="font-size: 0.68rem; padding: 2px 7px; background: #1e3a8a; color: #ffffff; font-weight: 700;">Editing • Zoom</span>'
            else:
                status_pill = f'<span class="badge-pill badge-gray" style="font-size: 0.68rem; padding: 2px 7px;">Page {i+1}</span>'

            card_border = "border: 2.5px solid #1e3a8a; background: #f0f7ff;" if is_active else "border: 1.5px solid #cbd5e1; background: #ffffff;"
            card_shadow = "box-shadow: 0 4px 12px rgba(30, 58, 138, 0.12);" if is_active else "box-shadow: 0 1px 3px rgba(0,0,0,0.05);"
            header_pr = "28px" if len(tray_pages) > 1 else "0px"

            tile_html = f"""
            <div class="tray-preview-card {'tray-preview-active' if is_active else ''}" style="{card_border} {card_shadow}">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; padding-right: {header_pr};">
                        <span style="font-size: 0.88rem; font-weight: 700; color: #0f172a;">Page {i+1}: Sec {s_code}</span>
                        {status_pill}
                    </div>
                    <div style="font-size: 0.78rem; font-weight: 600; color: #334155; margin-bottom: 0.35rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {s_name} {scaf_badge}
                    </div>
                    <div class="tray-sheet-mockup">
                        {clean_thumb}
                    </div>
                </div>
                <div style="font-size: 0.70rem; color: #64748b; text-align: center; margin-top: 0.2rem;">
                    {'Click again to open full preview' if is_active else 'Click to edit this page'}
                </div>
            </div>
            """
            render_clean_html(tile_html)

            # 1. Full-tile button overlay (two-state click)
            tile_acc_label = f"Page {i+1}: {s_name} ({'Active - Click to Zoom' if is_active else 'Click to Edit'})"
            if st.button(tile_acc_label, key=f"btn_tray_tile_{i}", use_container_width=True):
                if i != active_idx:
                    st.session_state["active_tray_idx"] = i
                    st.rerun()
                else:
                    show_page_preview_modal(p, i + 1)

            # 2. Delete 'X' button on the tile (only if total_pages > 1)
            if len(tray_pages) > 1:
                if st.button("✕", key=f"btn_tray_del_{i}", help=f"Remove Page {i+1} from packet"):
                    tray_pages.pop(i)
                    st.session_state["active_tray_idx"] = max(0, min(active_idx, len(tray_pages) - 1))
                    st.rerun()

    # "+ Add Page" Slot
    with tray_cols[-1 if total_pages > 0 else 0]:
        add_card_html = """
        <div class="tray-add-card">
            <div style="font-size: 1.6rem; font-weight: 700; color: #1e3a8a; line-height: 1; margin-bottom: 0.35rem;">+</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem;">Add New Page</div>
            <div style="font-size: 0.74rem; color: #64748b; line-height: 1.35;">Append another section spread to packet</div>
        </div>
        """
        render_clean_html(add_card_html)
        if st.button("+ Add Page", key="btn_add_tray_page", use_container_width=True):
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
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.65rem;">
                    <span style="font-size: 1.05rem; font-weight: 700; color: #1e3a8a;">
                        Editing Page {active_idx + 1} of {total_pages}
                    </span>
                    <span class="badge-pill badge-gray">Total Packet: {total_pages} pgs ({total_sheets} sheets)</span>
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

    # ── Final Step Navigation Button ──
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    if not tray_pages:
        st.warning("Your dynamic page tray is currently empty. Add at least 1 page above to review and export.")
    else:
        if st.button(
            "Final Step: Review & Export Packet →",
            key="btn_goto_packet_export",
            type="primary",
            use_container_width=True,
            help="Proceed to final packet review, page-by-page inspector, and PDF / Google Drive exports.",
        ):
            st.session_state["nav_view"] = "packet_export"
            st.session_state["export_preview_idx"] = 0
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# 3B. PATH A (PART 2): FINAL STEP - REVIEW & EXPORT SCREEN
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "packet_export":

    # Guard: Ensure tray_pages exists
    if "tray_pages" not in st.session_state or not st.session_state["tray_pages"]:
        st.warning("No pages found in your packet. Returning to Packet Editor...")
        st.session_state["nav_view"] = "packet"
        st.rerun()

    tray_pages = st.session_state["tray_pages"]

    # Breadcrumb Header
    b_col1, b_col2, b_col3, b_col4 = st.columns([1.2, 2.4, 0.8, 0.7])
    with b_col1:
        if st.button("← Back to Packet Editor", use_container_width=True, key="btn_back_packet_export"):
            st.session_state["nav_view"] = "packet"
            st.rerun()
    with b_col2:
        render_clean_html(
            f"""
            <div style="padding-top: 0.2rem;">
                <span class="badge-pill" style="font-size: 0.86rem; padding: 0.30rem 0.75rem;">
                    <b>Final Step:</b> Review & Export Packet &bull; Chapter {selected_ch_num:02d} ({len(tray_pages)} Pages)
                </span>
            </div>
            """
        )
    with b_col3:
        with st.popover("Context"):
            st.markdown(f"**Curriculum Unit:** {display_unit}")
            st.markdown(f"**Essential Question:** *\"{eq_text}\"*")
            st.markdown(f"**Google Drive Folder:** `{ROOT_FOLDER_NAME}`")
    with b_col4:
        if st.button("Log Out", key="packet_export_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

    # Real-Time Packet Compilation
    include_cov = st.session_state.get("include_cover_toggle", False)
    cov_mode = st.session_state.get("cover_style_select", "central_idea_tracker")
    foot_mode = st.session_state.get("footer_style_select", "gb_01_points_stamp")

    # Cache compiled packet bundle so navigating between pages in the inspector is instant
    pkt_cache_key = (
        str([(p.get("section_meta", {}).get("section_code"), p.get("strategy_code"), p.get("is_scaffolded")) for p in tray_pages])
        + f"_{include_cov}_{cov_mode}_{foot_mode}"
    )
    if "cached_modular_result" not in st.session_state or st.session_state.get("cached_pkt_key") != pkt_cache_key:
        with st.spinner("Compiling modular packet and rendering letter-size vector PDFs..."):
            modular_result = build_custom_modular_packet(
                pages_config=tray_pages,
                include_cover=include_cov,
                cover_mode=cov_mode,
                footer_mode=foot_mode,
            )
            st.session_state["cached_modular_result"] = modular_result
            st.session_state["cached_pkt_key"] = pkt_cache_key
    else:
        modular_result = st.session_state["cached_modular_result"]

    base_name = modular_result["base_filename"]
    student_pdf = modular_result["student_pdf_bytes"]
    teacher_pdf = modular_result["teacher_pdf_bytes"]
    bundle_zip = modular_result["bundle_zip_bytes"]
    total_pkt_pages = modular_result["total_pages"]
    student_pages_md = modular_result.get("student_pages_md", [])
    teacher_pages_md = modular_result.get("teacher_pages_md", [])
    has_cover = modular_result.get("has_cover", False)

    # Step 3: Print, Download & Google Drive Export
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

    # Horizontal Page Inspector Expander
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    insp_pages_count = len(student_pages_md)
    if "export_preview_idx" not in st.session_state:
        st.session_state["export_preview_idx"] = 0
    preview_idx = max(0, min(st.session_state["export_preview_idx"], insp_pages_count - 1))

    with st.expander(f"Complete Packet Page-by-Page Inspector ({insp_pages_count} Pages)", expanded=True):
        # In-line navigation bar
        nav_cols = st.columns([0.8] + [1.8] * insp_pages_count + [0.8])

        # Left Arrow
        with nav_cols[0]:
            if st.button("←", key="btn_prev_page", disabled=(preview_idx == 0), use_container_width=True, help="Previous Page"):
                st.session_state["export_preview_idx"] = preview_idx - 1
                st.rerun()

        # Page Tiles
        for i in range(insp_pages_count):
            with nav_cols[i + 1]:
                is_active = (i == preview_idx)
                active_cls = "inspector-tile-active" if is_active else "inspector-tile-inactive"

                if has_cover and i == 0:
                    tile_title = "Cover Page"
                    tile_sub = "Packet Cover"
                else:
                    p_idx = (i - 1) if has_cover else i
                    p_data = tray_pages[p_idx]
                    s_code = p_data.get("section_meta", {}).get("section_code", "?")
                    s_strat = p_data.get("strategy_code", "")
                    tile_match = get_tile_by_code(s_strat)
                    tile_sub = tile_match["name"] if tile_match else s_strat.replace("_", " ").title()
                    page_label_num = p_idx + 1
                    tile_title = f"Page {page_label_num}: Sec {s_code}"

                render_clean_html(
                    f"""
                    <div class="inspector-tile {active_cls}">
                        <div style="font-size: 0.82rem; font-weight: 700; color: {'#1e3a8a' if is_active else '#0f172a'};">
                            {tile_title}
                        </div>
                        <div style="font-size: 0.72rem; color: #475569; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px;">
                            {tile_sub}
                        </div>
                        <div style="font-size: 0.65rem; color: {'#2563eb' if is_active else '#94a3b8'}; font-weight: 600; margin-top: 2px;">
                            {'Viewing' if is_active else 'Click to View'}
                        </div>
                    </div>
                    """
                )
                if st.button(f"View Page {i+1}", key=f"btn_insp_page_{i}", use_container_width=True):
                    st.session_state["export_preview_idx"] = i
                    st.rerun()

        # Right Arrow
        with nav_cols[-1]:
            if st.button("→", key="btn_next_page", disabled=(preview_idx == insp_pages_count - 1), use_container_width=True, help="Next Page"):
                st.session_state["export_preview_idx"] = preview_idx + 1
                st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Render selected page
        std_page_md = student_pages_md[preview_idx] if preview_idx < len(student_pages_md) else ""
        tch_page_md = teacher_pages_md[preview_idx] if preview_idx < len(teacher_pages_md) else ""

        std_page_html = format_booklet_for_web(std_page_md)
        tch_page_html = format_booklet_for_web(tch_page_md)

        if has_cover and preview_idx == 0:
            tab_title_std = "Student Cover Page"
            tab_title_tch = "Teacher Packet Cover"
        else:
            p_idx = (preview_idx - 1) if has_cover else preview_idx
            p_is_scaf = tray_pages[p_idx].get("is_scaffolded", False) if p_idx < len(tray_pages) else False
            edition_lbl = "Scaffolded Edition" if p_is_scaf else "Standard Edition"
            tab_title_std = f"Student Handout ({edition_lbl})"
            tab_title_tch = "Teacher Answer Key & Exemplar"

        preview_tab1, preview_tab2 = st.tabs([tab_title_std, tab_title_tch])
        with preview_tab1:
            st.markdown(std_page_html, unsafe_allow_html=True)
        with preview_tab2:
            st.markdown(tch_page_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 4. PATH B: STANDALONE STRATEGY WORKSHEET GALLERY
# ─────────────────────────────────────────────────────────────────────────────

elif st.session_state["nav_view"] == "gallery":

    # ── Tier 1: Single-Row Universal Navigation & Scope Bar (~38px) ──
    nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([1.1, 1.8, 2.4, 0.9, 0.7])
    with nav_c1:
        if st.button("<- Main Menu", use_container_width=True, key="btn_back_gallery"):
            st.session_state["nav_view"] = "home"
            st.session_state["gal_active_tile_code"] = None
            st.rerun()

    with nav_c2:
        def on_gal_ch_change():
            st.session_state["selected_ch_num"] = st.session_state["gal_select_ch"]

        cur_ch = st.session_state["selected_ch_num"]
        cur_ch_idx = sorted_chapter_nums.index(cur_ch) if cur_ch in sorted_chapter_nums else 0
        gal_ch_num = st.selectbox(
            "Textbook Chapter:",
            options=sorted_chapter_nums,
            index=cur_ch_idx,
            format_func=lambda n: f"Chp {n:02d}: {chapters_map[n]['chapter_title']}",
            key="gal_select_ch",
            on_change=on_gal_ch_change,
            label_visibility="collapsed",
        )
        gal_ch_sections = chapters_map[gal_ch_num]["sections"]

    with nav_c3:
        gal_selected_sec = st.selectbox(
            "Section Spread to Practice:",
            options=gal_ch_sections,
            format_func=lambda s: f"Sec. {s['section_code']}: {s['title']} (pp. {s['printed_pages']})",
            key=f"gal_select_sec_{gal_ch_num}",
            label_visibility="collapsed",
        )

    with nav_c4:
        with st.popover("Context"):
            st.markdown(f"**Curriculum Unit:** {display_unit}")
            st.markdown(f"**Essential Question:** *\"{eq_text}\"*")
            st.markdown(f"**Google Drive Folder:** `{ROOT_FOLDER_NAME}`")
            st.caption(f"{len(gal_ch_sections)} section spreads in Chapter {gal_ch_num:02d}.")

    with nav_c5:
        if st.button("Log Out", key="gal_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

    gal_sec_code = str(gal_selected_sec["section_code"])
    gal_md_path = resolve_file_path(gal_selected_sec.get("md_file"))
    gal_raw_md = gal_md_path.read_text(encoding="utf-8") if gal_md_path.exists() else ""

    active_tile_code = st.session_state.get("gal_active_tile_code", None)

    if not active_tile_code:
        # ── Step 2: All-in-One Visual Strategy Grid (Open Browsing Mode) ──
        st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-bottom: 0.20rem;'>All-in-One Visual Strategy Grid — Choose a Worksheet Layout</div>", unsafe_allow_html=True)
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
            filtered_tiles = [t for t in ALL_STRATEGY_TILES if t.get("category") == "Central Idea"]
        elif "Anti-Copycat" in category_filter:
            filtered_tiles = [t for t in ALL_STRATEGY_TILES if t.get("category") == "Anti-Copycat"]
        elif "Active Reading" in category_filter:
            filtered_tiles = [t for t in ALL_STRATEGY_TILES if t.get("category") == "Active Reading"]
        elif "Writing Revolution" in category_filter:
            filtered_tiles = [t for t in ALL_STRATEGY_TILES if t.get("category") in ["The Writing Revolution", "Writing (TWR)"]]
        else:
            filtered_tiles = [t for t in ALL_STRATEGY_TILES if t.get("category") in ["Vocabulary", "Assessment"]]

        _render_strategy_card_grid(
            tiles_list=filtered_tiles,
            active_code=None,
            key_prefix="open",
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.info("Select any template card above to generate and preview your 1-page student worksheet, exemplar key, and PDF downloads.")

    else:
        # ── Strategy Selected: Action & Format Toolbar + Immediate Full-Sized Preview ──
        active_tile = get_tile_by_code(active_tile_code) or ALL_STRATEGY_TILES[0]
        cat_lookup = {
            "Central Idea": "central_idea",
            "Anti-Copycat": "anti_copycat",
            "Active Reading": "reading_organizer",
            "The Writing Revolution": "twr",
            "Writing (TWR)": "twr",
            "Vocabulary": "vocab",
            "Assessment": "assessment",
        }
        active_cat_key = cat_lookup.get(active_tile["category"], "central_idea")

        # ── Compact Action & Format Toolbar (~40px) ──
        tb_col1, tb_col2 = st.columns([1.6, 2.2])
        with tb_col1:
            t_sub1, t_sub2 = st.columns([2.3, 1.2])
            with t_sub1:
                render_clean_html(
                    f"""
                    <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 6px; padding: 0.30rem 0.60rem; display: flex; align-items: center; justify-content: space-between; height: 38px; box-sizing: border-box;">
                        <span style="font-size: 0.85rem; font-weight: 700; color: #166534; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {active_tile['name']}
                        </span>
                        <span class="badge-pill" style="font-size: 0.68rem; padding: 0.10rem 0.35rem; background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; margin-left: 0.35rem;">{active_tile['category']}</span>
                    </div>
                    """
                )
            with t_sub2:
                if st.button("Change", key="btn_clear_active_tile", use_container_width=True, help="Switch to a different curriculum strategy layout"):
                    st.session_state["gal_active_tile_code"] = None
                    st.rerun()

        with tb_col2:
            scaf_c, hs_c = st.columns(2)
            with scaf_c:
                is_scaf_ws = st.checkbox(
                    "Scaffolded Edition",
                    value=st.session_state.get("gal_scaf_toggle", False),
                    key="gal_scaf_toggle",
                    help="Adds sentence starters, word banks, and structured fill-in-the-blanks for differentiated support.",
                )
            with hs_c:
                is_half_sheet = st.checkbox(
                    "2-Up Half-Sheets (50% Paper)",
                    value=st.session_state.get("gal_half_sheet_toggle", False),
                    key="gal_half_sheet_toggle",
                    help="Formats two identical compact worksheets onto a single 8.5x11 letter page separated by a dashed cut line to cut photocopy usage in half.",
                )

        # Minimized Expander for Quick Layout Switching
        with st.expander(f"Quick-Switch Layout (Currently: {active_tile['name']})", expanded=False):
            min_cat_filter = st.radio(
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
                key="gal_cat_filter_radio_min",
            )

            if "All" in min_cat_filter:
                min_filtered = ALL_STRATEGY_TILES
            elif "Central Idea" in min_cat_filter:
                min_filtered = [t for t in ALL_STRATEGY_TILES if t.get("category") == "Central Idea"]
            elif "Anti-Copycat" in min_cat_filter:
                min_filtered = [t for t in ALL_STRATEGY_TILES if t.get("category") == "Anti-Copycat"]
            elif "Active Reading" in min_cat_filter:
                min_filtered = [t for t in ALL_STRATEGY_TILES if t.get("category") == "Active Reading"]
            elif "Writing Revolution" in min_cat_filter:
                min_filtered = [t for t in ALL_STRATEGY_TILES if t.get("category") in ["The Writing Revolution", "Writing (TWR)"]]
            else:
                min_filtered = [t for t in ALL_STRATEGY_TILES if t.get("category") in ["Vocabulary", "Assessment"]]

            _render_strategy_card_grid(
                tiles_list=min_filtered,
                active_code=active_tile_code,
                key_prefix="min",
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

        if is_half_sheet:
            student_html = format_half_sheet_2up(student_html)
            teacher_html = format_half_sheet_2up(teacher_html)

        hs_suffix = "_2Up_HalfSheet" if is_half_sheet else ""
        student_filename = f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Student{hs_suffix}.pdf"
        teacher_filename = f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Exemplar{hs_suffix}.pdf"
        bundle_filename = f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Bundle{hs_suffix}.zip"

        try:
            student_pdf_bytes = compile_pdf_cached(student_html, title=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Student{hs_suffix}")
            teacher_pdf_bytes = compile_pdf_cached(teacher_html, title=f"Chp{gal_ch_num:02d}_Sec{gal_sec_code}_{active_tile_code}_Exemplar{hs_suffix}")
            single_bundle_zip = create_pdf_bundle_zip({
                student_filename: student_pdf_bytes,
                teacher_filename: teacher_pdf_bytes,
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
                    file_name=student_filename,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )
            with w_dl2:
                st.download_button(
                    "Download Exemplar PDF",
                    data=teacher_pdf_bytes,
                    file_name=teacher_filename,
                    mime="application/pdf",
                    use_container_width=True,
                )
            with w_dl3:
                st.download_button(
                    "Download Both (.zip)",
                    data=single_bundle_zip,
                    file_name=bundle_filename,
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
                                    student_filename=student_filename,
                                    teacher_pdf_bytes=teacher_pdf_bytes,
                                    teacher_filename=teacher_filename,
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

        edition_desc = "Scaffolded" if is_scaf_ws else "Standard"
        layout_desc = "2-Up Half-Sheet" if is_half_sheet else "Full Page"

        # Preview Tabs
        ws_tab1, ws_tab2, ws_tab3 = st.tabs([
            f"Student Handout Preview ({edition_desc} — {layout_desc})",
            f"Teacher Answer Key & Student Exemplar ({layout_desc})",
            "Textbook Source Passage Grounding",
        ])

        with ws_tab1:
            st.markdown(student_html, unsafe_allow_html=True)
            if not is_scaf_ws:
                with st.expander("Compare with Scaffolded Support Edition"):
                    alt_html = format_booklet_for_web(scaf_md)
                    if is_half_sheet:
                        alt_html = format_half_sheet_2up(alt_html)
                    st.markdown(alt_html, unsafe_allow_html=True)
            else:
                with st.expander("Compare with Standard Edition"):
                    alt_html = format_booklet_for_web(std_md)
                    if is_half_sheet:
                        alt_html = format_half_sheet_2up(alt_html)
                    st.markdown(alt_html, unsafe_allow_html=True)

        with ws_tab2:
            st.markdown(teacher_html, unsafe_allow_html=True)

        with ws_tab3:
            if gal_raw_md:
                with st.container(height=520):
                    st.markdown(gal_raw_md)
            else:
                st.warning("Textbook passage markdown file could not be loaded.")
