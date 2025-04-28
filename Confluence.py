import pathlib, json, re
from bs4 import BeautifulSoup
from markdownify import markdownify as md

RAW_DIR  = pathlib.Path("pages_raw")
OUT_FILE = "training_pairs.json"

def extract(html: str):
    """return (problem, cause, solution) from one page"""
    soup = BeautifulSoup(html, "html.parser")

    # headings could be h1..h6 and text may vary slightly — include synonyms
    def grab(section_words):
        h = soup.find(lambda tag:
                      tag.name.startswith("h") and
                      any(word in tag.text.lower() for word in section_words))
        if not h:
            return ""
        bits = []
        for sib in h.find_all_next():
            if sib.name and sib.name.startswith("h"):
                break
            bits.append(str(sib))
        return md("".join(bits)).strip()

    problem  = grab(["problem", "issue"])    # synonyms allowed
    cause    = grab(["cause", "root cause"])
    solution = grab(["solution", "resolution", "fix"])

    if not problem:
        problem = soup.title.string if soup.title else "Unknown problem"

    target_parts = [problem, cause, solution]
    target_text  = "\n\n".join(p for p in target_parts if p)

    return problem, target_text

pairs = []
for html_file in RAW_DIR.glob("*.html"):
    html = html_file.read_text(encoding="utf-8", errors="ignore")
    try:
        problem, target = extract(html)
        pairs.append({"input": problem, "target": target})
        print("✓", html_file.name)
    except Exception as e:
        print("⚠️  skip", html_file.name, e)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"data": pairs}, f, ensure_ascii=False, indent=2)

print("\nWrote", len(pairs), "pairs to", OUT_FILE)
