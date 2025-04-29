
from bs4 import BeautifulSoup
from markdownify import markdownify as md   # if you want Markdown
import html2text                            # produces neater lists

html = open("example_storage.html", encoding="utf-8").read()
soup = BeautifulSoup(html, "xml")           # use XML parser for ac: tags

def section(label):
    h = soup.find(lambda t: t.name.startswith("h")
                           and label.lower() in t.text.lower())
    if not h:
        return ""
    parts = []
    for sib in h.find_next_siblings():
        if sib.name and sib.name.startswith("h"):   # next heading -> stop
            break
        parts.append(str(sib))
    # convert to markdown; html2text keeps bullets nicely
    return html2text.html2text("".join(parts)).strip()

problem   = section("problem")
rootcause = section("root cause")
solution  = section("solution")

print("INPUT  :", problem.splitlines()[0][:80], "…")
print("TARGET :\n", "### Problem\n"+problem,
                      "\n\n### Root cause\n"+rootcause if rootcause else "",
                      "\n\n### Solution\n"+solution)
