import pathlib, json, re
from bs4 import BeautifulSoup
from markdownify import markdownify as md

RAW_DIR  = pathlib.Path("pages_raw")      # folder of .html files
OUT_FILE = "training_pairs.json"

def extract_sections(html: str):
    soup = BeautifulSoup(html, "html.parser")

    def grab(label: str):
        """return markdown under first heading containing label"""
        tag = soup.find(lambda t:
                        t.name and t.name.startswith("h") and
                        label.lower() in t.get_text(strip=True).lower())
        if not tag:
            return ""
        bits = []
        for sib in tag.find_all_next():
            if sib.name and sib.name.startswith("h"):
                break
            bits.append(str(sib))
        return md("".join(bits)).strip()

    problem   = grab("problem")
    rootcause = grab("root cause") or grab("cause")
    solution  = grab("solution")

    if not problem:
        raise ValueError("No Problem section")

    target_md = "\n\n".join(x for x in (problem, rootcause, solution) if x)
    return problem, target_md

pairs = []
bad   = []
for f in RAW_DIR.glob("*.html"):
    try:
        prob, targ = extract_sections(f.read_text(encoding="utf-8", errors="ignore"))
        pairs.append({"input": prob, "target": targ})
        print("✓", f.name)
    except Exception as e:
        bad.append(f"{f.name} ({e})")

with open(OUT_FILE, "w", encoding="utf-8") as fp:
    json.dump({"data": pairs}, fp, ensure_ascii=False, indent=2)

print("\nGenerated", len(pairs), "pairs →", OUT_FILE)
if bad:
    print("Skipped:", *bad, sep="\n  - ")
