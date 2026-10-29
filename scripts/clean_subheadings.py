import json
import re
from pathlib import Path

NON_BLUE_PATTERNS = [
    r"FUENTE[S]?\s+PRIMARIA[S]?",
    r"PRIMARY\s+SOURCE[S]?",
    r"DRAW\s+CONCLUSIONS",
    r"SACAR\s+CONCLUSIONES",
    r"IDENTIFY\s+PROBLEMS(?:\s+AND\s+SOLUTIONS)?",
    r"IDENTIFICAR\s+IDEAS(?:\s+PRINCIPALES)?",
    r"E\s*VALUATE",
    r"DESCRIBE",
    r"CONSTRUCTED\s+RESPONSE",
    r"CRITICAL\s+VIEWING",
    r"VISI[ÓO]N\s+CR[ÍI]TICA",
    r"OBSERVACI[ÓO]N\s+CR[ÍI]TICA",
    r"READING\s+CHECK",
    r"COMPROBAR\s+LA\s+LECTURA",
    r"INTERPRETAR\s+MAPAS",
    r"SINTETIZAR",
    r"THINK\s+LIKE\s+A\s+GEOGRAPHER",
    r"CONSTRUCT\b",
    r"RECALL\b",
]

def is_non_blue(title: str) -> bool:
    clean = title.strip().upper()
    for pat in NON_BLUE_PATTERNS:
        if re.search(pat, clean):
            return True
    return False

def clean_catalog(cat_path: Path):
    with open(cat_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    modified_count = 0
    for s in data:
        old_subs = s.get("subheadings", [])
        clean_subs = [sh for sh in old_subs if not is_non_blue(sh.get("title", ""))]
        
        # If it's a standard core narrative section and still has > 2, keep the top 2
        is_standard = not s.get("is_special_feature", False) and "Core Historical Narrative" in s.get("section_type", "Core")
        if is_standard and len(clean_subs) > 2:
            clean_subs = clean_subs[:2]
            
        if len(clean_subs) != len(old_subs):
            modified_count += 1
            s["subheadings"] = clean_subs
            
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Cleaned {cat_path}: modified {modified_count} sections.")

def clean_markdown_dir(md_dir: Path):
    files = list(md_dir.glob("*.md"))
    modified_count = 0
    for f in files:
        txt = f.read_text(encoding="utf-8")
        
        # Find all #### blocks
        # Split on #### lines
        parts = re.split(r"(?=\n####\s+\d+\.)", txt)
        if len(parts) <= 1:
            continue
            
        header_part = parts[0]
        sub_parts = parts[1:]
        
        kept_sub_parts = []
        for part in sub_parts:
            # Extract heading title
            m = re.match(r"\n####\s+\d+\.\s+([^\n(]+)", part)
            if m:
                title = m.group(1).strip()
                if is_non_blue(title):
                    continue
            kept_sub_parts.append(part)
            
        # Renumber kept sub_parts
        renumbered_parts = []
        for idx, part in enumerate(kept_sub_parts, start=1):
            renumbered = re.sub(r"^\n####\s+\d+\.", f"\n#### {idx}.", part)
            renumbered_parts.append(renumbered)
            
        new_txt = header_part + "".join(renumbered_parts)
        if new_txt != txt:
            f.write_text(new_txt, encoding="utf-8")
            modified_count += 1
            
    print(f"Cleaned {md_dir}: modified {modified_count} files.")

if __name__ == "__main__":
    clean_catalog(Path("output/catalog.json"))
    clean_catalog(Path("output/spanish/catalog.json"))
    clean_markdown_dir(Path("output/markdown"))
    clean_markdown_dir(Path("output/spanish/markdown"))
