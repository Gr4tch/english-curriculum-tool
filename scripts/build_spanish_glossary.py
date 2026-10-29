import re
import json
from pathlib import Path
import pymupdf

def extract_spanish_glossary():
    pdf_path = Path("input/Historias Americanas.pdf")
    doc = pymupdf.open(str(pdf_path))
    
    glossary = {}
    for p_idx in range(637, 647):
        txt = doc[p_idx].get_text()
        txt = re.sub(r'G\s+L\s+O\s+S\s+A\s+R\s+I\s+O', '', txt)
        txt = re.sub(r'^[A-Z]\b', '', txt, flags=re.MULTILINE)
        pattern = re.compile(
            r'([^\n\u2002]+)\u2002\s*(?:s\.|adj\.|v\.|adv\.|conj\.)\s*(.*?)(?=\n[^\n\u2002]+\u2002\s*(?:s\.|adj\.|v\.|adv\.|conj\.)|\Z)',
            re.DOTALL
        )
        for m in pattern.finditer(txt):
            term = m.group(1).strip()
            defn = ' '.join(m.group(2).split()).strip()
            defn = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', defn)
            if term and defn:
                glossary[term] = defn
                
    out_path = Path("output/spanish/glossary.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(glossary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(glossary)} glossary terms to {out_path}")
    return glossary

if __name__ == "__main__":
    extract_spanish_glossary()
