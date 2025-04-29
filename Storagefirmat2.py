#!/usr/bin/env python3
import pathlib
import json
import logging

from bs4 import BeautifulSoup
import html2text

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

HTML_DIR = pathlib.Path("html")               # put your Confluence-exported .html files here
OUT_FILE = pathlib.Path("training_pairs.json")


def extract_sections(html: str) -> dict[str,str]:
    """
    Given a Confluence storage-format HTML page, find the sections
    headed by <h2> or <h3> with text "Problem", "Root Cause", "Solution"
    and return their contents as Markdown.
    """
    soup = BeautifulSoup(html, "lxml")
    converter = html2text.HTML2Text()
    converter.body_width = 0  # don’t wrap lines

    out: dict[str,str] = {}
    for section in ("Problem", "Root Cause", "Solution"):
        # locate the heading tag
        head = soup.find(lambda t: t.name in ("h2","h3") and t.get_text(strip=True)==section)
        if not head:
            logger.warning("No “%s” heading found", section)
            out[section] = ""
            continue

        # gather all siblings until the next heading of same level
        fragments = []
        for sib in head.find_next_siblings():
            if sib.name in ("h2","h3"):
                break
            fragments.append(str(sib))

        html_block = "".join(fragments)
        md = converter.handle(html_block).strip()
        out[section] = md

    return out


def main():
    data = []
    for html_path in sorted(HTML_DIR.glob("*.html")):
        logger.info("Processing %s", html_path.name)
        raw_html = html_path.read_text(encoding="utf-8")
        secs = extract_sections(raw_html)

        if not secs["Problem"].strip():
            logger.warning("Skipping %s — no Problem section", html_path.name)
            continue

        # build the JSON entry
        entry = {
            "input": secs["Problem"],
            "target": (
                "**Root Cause:**\n"
                f"{secs['Root Cause']}\n\n"
                "**Solution:**\n"
                f"{secs['Solution']}"
            )
        }
        data.append(entry)

    out = {"data": data}
    OUT_FILE.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Wrote %d pairs to %s", len(data), OUT_FILE)


if __name__ == "__main__":
    main()
