"""
High-Fidelity PDF Export & Google Drive Synchronization Engine.
Compiles professional, print-ready vector PDFs directly from curriculum HTML/CSS
layouts via headless Chromium and handles dual-delivery uploads to Google Drive.
"""

import io
import json
import logging
import re
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

from googleapiclient.http import MediaIoBaseUpload

from doc_exporter import (
    get_gdrive_service,
    get_or_create_folder,
    get_target_chapter_folder,
    get_target_section_folder,
    grant_file_permissions,
    ROOT_FOLDER_NAME,
)
from src.preview_renderer import COMMON_CSS

logger = logging.getLogger(__name__)

PRINT_PAGE_CSS = """
<style>
@page {
    size: letter;
    margin: 0.45in;
}
@media print {
    body {
        margin: 0;
        padding: 0;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    .page-break {
        page-break-after: always !important;
        break-after: page !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        display: block !important;
    }
    .ws-container, .ws-exemplar-container {
        page-break-inside: avoid;
        break-inside: avoid;
        box-shadow: none !important;
        margin-bottom: 0.5rem !important;
    }
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    margin: 0;
    padding: 0;
    line-height: 1.45;
}
</style>
"""


def _wrap_in_full_html_doc(html_fragment: str, title: str = "Curriculum Document") -> str:
    """Wraps an HTML fragment inside a complete, standalone HTML5 document optimized for PDF rendering."""
    # Replace web page break markers with printable page breaks
    cleaned_fragment = html_fragment
    if "Page Break" in cleaned_fragment or "[PAGE_BREAK]" in cleaned_fragment:
        # Replace the dotted web page break box with print-only page break
        cleaned_fragment = re.sub(
            r'<div style="margin: 2\.5rem 0 2rem 0; border-top: 2px dashed #cbd5e1; text-align: center;">.*?Page Break.*?</div>\n*',
            '<div class="page-break"></div>',
            cleaned_fragment,
            flags=re.DOTALL,
        )
        cleaned_fragment = cleaned_fragment.replace("[PAGE_BREAK]", '<div class="page-break"></div>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    {COMMON_CSS}
    {PRINT_PAGE_CSS}
</head>
<body>
{cleaned_fragment}
</body>
</html>"""


def html_to_pdf_bytes(html_content: str, title: str = "Curriculum Document") -> bytes:
    """
    Compiles styled HTML/CSS into a letter-size, print-ready PDF binary using Playwright Chromium.
    Preserves exact font typography, border colors, badges, dotted handwriting lines, and answer pills.
    """
    from playwright.sync_api import sync_playwright

    full_html = _wrap_in_full_html_doc(html_content, title=title)

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            logger.info(f"Playwright chromium binary not detected ({e}). Attempting auto-installation...")
            import subprocess
            import sys
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            browser = p.chromium.launch()

        page = browser.new_page()
        page.set_content(full_html, wait_until="networkidle")
        pdf_bytes = page.pdf(
            format="Letter",
            print_background=True,
            margin={"top": "0.45in", "bottom": "0.45in", "left": "0.45in", "right": "0.45in"},
            prefer_css_page_size=True,
        )
        browser.close()

    return pdf_bytes


def create_pdf_bundle_zip(files_dict: Dict[str, bytes]) -> bytes:
    """
    Packages multiple PDF files into an in-memory ZIP archive.
    Ensures teachers can download student packets and matching teacher answer keys in a single file.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename, data in files_dict.items():
            clean_name = filename if filename.endswith(".pdf") else f"{filename}.pdf"
            zf.writestr(clean_name, data)

    return zip_buffer.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE DRIVE DESTINATION FOLDER RESOLUTION
# ─────────────────────────────────────────────────────────────────────────────

def get_target_multi_section_folder(
    service,
    chapter_num: int,
    chapter_title: str,
    additional_email: Optional[str] = None,
) -> Tuple[str, str, str]:
    """
    Resolves the folder hierarchy for packets covering multiple sections within a chapter:
      #US History (English) Curriculum Materials / Chp XX - [Title] / Multi-Section Packets
    Returns (folder_id, path_display, folder_url).
    """
    ch_id, ch_path, _ = get_target_chapter_folder(
        service,
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        additional_email=additional_email,
    )
    folder_name = "Multi-Section Packets"
    folder_id, folder_url = get_or_create_folder(
        service,
        folder_name,
        parent_id=ch_id,
        additional_email=additional_email,
    )
    path_display = f"{ch_path} > {folder_name}"
    return folder_id, path_display, folder_url


def get_target_custom_units_folder(
    service,
    additional_email: Optional[str] = None,
) -> Tuple[str, str, str]:
    """
    Resolves the folder hierarchy for custom multi-chapter packets:
      #US History (English) Curriculum Materials / Custom Multi-Chapter Units
    Returns (folder_id, path_display, folder_url).
    """
    root_id, _ = get_or_create_folder(service, ROOT_FOLDER_NAME, additional_email=additional_email)
    folder_name = "Custom Multi-Chapter Units"
    folder_id, folder_url = get_or_create_folder(
        service,
        folder_name,
        parent_id=root_id,
        additional_email=additional_email,
    )
    path_display = f"{ROOT_FOLDER_NAME} > {folder_name}"
    return folder_id, path_display, folder_url


def upload_pdf_to_google_drive(
    service,
    pdf_bytes: bytes,
    filename: str,
    parent_folder_id: str,
    replace_existing: bool = True,
    additional_email: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Uploads a PDF directly into Google Drive as a native application/pdf file.
    Optionally replaces previous version to prevent duplicate cluttered files.
    """
    clean_filename = filename if filename.endswith(".pdf") else f"{filename}.pdf"

    if replace_existing:
        safe_name = clean_filename.replace("'", "\\'")
        query = (
            f"name = '{safe_name}' and '{parent_folder_id}' in parents "
            f"and mimeType = 'application/pdf' and trashed = false"
        )
        res = service.files().list(q=query, fields="files(id, name)").execute()
        existing = res.get("files", [])
        for f in existing:
            try:
                service.files().delete(fileId=f["id"]).execute()
            except Exception as e:
                logger.debug(f"Could not delete older version {f['id']}: {e}")

    file_metadata = {
        "name": clean_filename,
        "parents": [parent_folder_id],
        "mimeType": "application/pdf",
    }
    media = MediaIoBaseUpload(io.BytesIO(pdf_bytes), mimetype="application/pdf", resumable=False)
    created = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, webViewLink, webContentLink",
    ).execute()

    grant_file_permissions(
        service,
        created["id"],
        role="reader",
        share_public=True,
        additional_email=additional_email,
    )

    return {
        "id": created["id"],
        "name": created.get("name", clean_filename),
        "link": created.get("webViewLink", f"https://drive.google.com/file/d/{created['id']}/view"),
    }


def upload_packet_bundle_to_google_drive(
    service,
    student_pdf_bytes: bytes,
    student_filename: str,
    teacher_pdf_bytes: bytes,
    teacher_filename: str,
    parent_folder_id: str,
    folder_path_display: str,
    additional_email: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Uploads both the student packet and the teacher answer key together into the designated
    Google Drive folder so the teacher never loses the matching answer key.
    """
    student_res = upload_pdf_to_google_drive(
        service,
        student_pdf_bytes,
        student_filename,
        parent_folder_id,
        replace_existing=True,
        additional_email=additional_email,
    )

    teacher_res = upload_pdf_to_google_drive(
        service,
        teacher_pdf_bytes,
        teacher_filename,
        parent_folder_id,
        replace_existing=True,
        additional_email=additional_email,
    )

    return {
        "student": student_res,
        "teacher": teacher_res,
        "folder_path": folder_path_display,
    }
