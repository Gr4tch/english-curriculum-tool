import sys
import re
import json
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
doc = pymupdf.open("input/Historias Americanas.pdf")
cat = json.load(open("output/catalog.json", encoding="utf-8"))

ch_toc_map = {}

current_ch = 1
for pno in range(5, 16):
    lines = [clean for l in doc[pno].get_text().split("\n") if (clean := l.strip())]
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check chapter header
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

print(f"Total sections indexed by (ch, sec_code): {len(ch_toc_map)}")
matched_count = 0
for s in cat:
    ch = s["chapter_num"]
    sc = s["section_code"]
    if (ch, sc) in ch_toc_map:
        matched_count += 1

print(f"Matched {matched_count} out of {len(cat)} catalog sections!")

for ch in [16, 17]:
    for s in [s for s in cat if s["chapter_num"] == ch]:
        key = (ch, s["section_code"])
        info = ch_toc_map.get(key, ("NOT FOUND", 0))
        print(f"Ch {ch:02d} Sec {s['section_code']}: Spanish title: '{info[0]}', page: {info[1]} (English was p.{s['start_page']})")
