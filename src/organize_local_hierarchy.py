import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

UNIT_NAMES = {
    1: "Unit 1 - Early Encounters (Beginnings–1650)",
    2: "Unit 2 - English Settlement (1585–1763)",
    3: "Unit 3 - A New Nation (1763–1791)",
    4: "Unit 4 - The Early Republic (1789–1844)",
    5: "Unit 5 - Pushing Boundaries (1821–1860)",
    6: "Unit 6 - Civil War and Reconstruction (1846–1877)",
}

CATALOG_PATH = Path("output/catalog.json")
BASE_EXPORT_DIR = Path("output/American Stories (Sections)")


def organize_hierarchy():
    if not CATALOG_PATH.exists():
        print("Catalog not found. Run src/cengage_processor.py first.")
        return

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    BASE_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    copied_count = 0

    for item in catalog:
        u_num = item["unit_num"]
        ch_num = item["chapter_num"]
        ch_title = item["chapter_title"]
        sec_code = item["section_code"]
        sec_title = item["title"]
        src_pdf = Path(item["pdf_file"])

        if not src_pdf.exists():
            continue

        u_folder = UNIT_NAMES.get(u_num, f"Unit {u_num}")
        ch_folder = f"Chapter {ch_num:02d} - {ch_title}"
        target_dir = BASE_EXPORT_DIR / u_folder / ch_folder
        target_dir.mkdir(parents=True, exist_ok=True)

        clean_sec_title = re.sub(r'[\\/*?:"<>|]', "", sec_title).strip()
        dest_filename = f"Sec {sec_code} - {clean_sec_title}.pdf"
        dest_path = target_dir / dest_filename
        shutil.copy2(src_pdf, dest_path)
        copied_count += 1

    print(f"Successfully organized {copied_count} section PDFs into '{BASE_EXPORT_DIR}'")


if __name__ == "__main__":
    organize_hierarchy()
