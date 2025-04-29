
#!/usr/bin/env python3
import re
import json
import pathlib
from markdownify import markdownify as md
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
HTML_DIR      = pathlib.Path("html_pages")      # ← put your .html exports here
OUTPUT_JSON   = pathlib.Path("training_pairs.json")
HEADINGS      = ["Problem", "Root Cause", "Solution"]

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def clean_markdown(text: str) -> str:
    """
    Tidy up the raw markdown that markdownify produces.
    - Strip stray leading asterisks or blank space
    - Normalize bullets
    - Turn **Heading:** into ## Heading
    - Collapse multiple blank lines
    """
    # strip stray leading bullets/asterisks
    text = text.lstrip("* \n")
    # normalize lists: two-space “  * ” → “- ”
    text = re.sub(r"^\s*\*\s+", "- ", text, flags=re.M)
    # headings
    text = re.sub(r"\*\*(Problem|Root Cause|Solution)\*\*[:\s]*",
                  lambda m: f"## {m.group(1)}\n\n", text)
    # code-style lists: `files: []` → keep as is
    # collapse 3+ blank lines → 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def html_section_to_md(nodes) -> str:
    """
    Given a list of BeautifulSoup nodes belonging to one section,
    convert them to markdown and clean up.
    """
    html = "".join(str(n) for n in nodes).strip()
    raw_md = md(html, heading_style="ATX")
    return clean_markdown(raw_md)

def extract_sections_from_html(html: str) -> dict:
    """
    Parse the HTML, find each section by its <h2> (or <h1>) heading,
    and return a dict { "Problem": md, "Root Cause": md, "Solution": md }.
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {}
    # look for headings in document order
    for heading in soup.find_all(re.compile(r"^h[1-3]$")):
        title = heading.get_text(strip=True)
        if title not in HEADINGS:
            continue
        # collect everything until the next h1–h3
        section_nodes = []
        for sib in heading.next_siblings:
            if getattr(sib, "name", None) and re.match(r"^h[1-3]$", sib.name):
                break
            section_nodes.append(sib)
        result[title] = html_section_to_md(section_nodes)
    return result

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    out = {"data": []}

    for html_file in sorted(HTML_DIR.glob("*.html")):
        html = html_file.read_text(encoding="utf-8")
        secs = extract_sections_from_html(html)

        # require at least Problem + one of the others
        if "Problem" not in secs or not ("Root Cause" in secs or "Solution" in secs):
            print(f"⚠️  skipping {html_file.name}: missing sections")
            continue

        # build input/target
        inp = secs["Problem"]
        tgt_parts = []
        if "Root Cause" in secs:
            tgt_parts.append("## Root Cause\n\n" + secs["Root Cause"])
        if "Solution" in secs:
            tgt_parts.append("## Solution\n\n" + secs["Solution"])
        tgt = "\n\n".join(tgt_parts)

        out["data"].append({
            "input": inp,
            "target": tgt
        })

    # write JSON
    OUTPUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n✅ Wrote {len(out['data'])} examples to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
