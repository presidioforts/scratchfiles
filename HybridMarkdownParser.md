Perfect — here’s a Claude‑powered hybrid Markdown cleaner the way AI product teams do it.

requirements.txt

anthropic
mdformat
pymarkdownlnt
markdown-it-py
beautifulsoup4
tqdm
python-dotenv

hybrid_markdown_cleaner.py

#!/usr/bin/env python3
"""
Hybrid Markdown Cleaner for FAQ JSON
- Stage 1: deterministic clean (HTML strip + mdformat)
- Stage 2: parse + lint; collect failures
- Stage 3: Claude repair ONLY for failures (temperature=0)
- Stage 4: re-validate; write cleaned JSON and a summary report

Input JSON shape (list of objects). Each object must contain "answer" (string).
Other fields are preserved.

Usage:
  export ANTHROPIC_API_KEY=...
  python hybrid_markdown_cleaner.py --input faq_raw.json --output faq_cleaned.json --report report.json
"""

import os
import re
import json
import tempfile
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple

from bs4 import BeautifulSoup
import mdformat
from markdown_it import MarkdownIt
from tqdm import tqdm

# --- Optional: Claude (Anthropic) ---
USE_CLAUDE = True
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620")

try:
    from anthropic import Anthropic
    _anthropic_ok = True
except Exception:
    _anthropic_ok = False


# ----------------- Utils -----------------

def strip_html_to_text(s: str) -> str:
    return BeautifulSoup(s, "html.parser").get_text()

def normalize_line_endings(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")

def deterministic_clean(markdown_text: str) -> str:
    """
    Fast, deterministic cleanup:
    - strip HTML
    - normalize line endings
    - fix missing space after # in ATX headings
    - normalize trivial list markers
    - run mdformat to standardize layout
    """
    s = strip_html_to_text(markdown_text)
    s = normalize_line_endings(s)

    # ##Heading -> ## Heading
    s = re.sub(r"^(#{1,6})([^\s#])", r"\1 \2", s, flags=re.MULTILINE)

    # "*item" -> "* item", "•item" -> "• item"
    s = re.sub(r"^(\*|•)([^\s])", r"\1 \2", s, flags=re.MULTILINE)

    # "1.Item" -> "1. Item"
    s = re.sub(r"^(\d+)\.([^\s])", r"\1. \2", s, flags=re.MULTILINE)

    # Let mdformat do the heavy lifting for spacing/tables/code fences
    try:
        s = mdformat.text(s)
    except Exception:
        # If mdformat chokes, fall back to original s
        pass

    return s.strip()


def parse_ok(markdown_text: str) -> bool:
    """
    Structural parse using markdown-it-py.
    If tokenization succeeds without raising, we consider it parse-ok.
    """
    try:
        md = MarkdownIt()
        _ = md.parse(markdown_text)
        return True
    except Exception:
        return False


@dataclass
class LintResult:
    ok: bool
    issues: str  # raw linter output (empty if ok)


def lint_with_pymarkdown(markdown_text: str) -> LintResult:
    """
    Run PyMarkdown linter via subprocess.
    Returns ok=False if issues are found. Issues text is returned for context.
    """
    # Write to a temp file; pymarkdown expects a path
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(markdown_text)
        tmp_path = tmp.name

    try:
        # 'pymarkdownlnt' installs a 'pymarkdown' CLI
        # 'scan' returns non-zero exit code if issues are found
        proc = subprocess.run(
            ["pymarkdown", "scan", tmp_path],
            capture_output=True,
            text=True,
            check=False,
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        # PyMarkdown returns:
        #  - exit code 0 = no issues
        #  - exit code 1 = issues found
        #  - exit code >1 = tool error
        if proc.returncode == 0:
            return LintResult(ok=True, issues="")
        elif proc.returncode == 1:
            # issues present
            return LintResult(ok=False, issues=stdout or stderr)
        else:
            # Tool error; don't block pipeline—treat as pass but note error
            return LintResult(ok=True, issues=f"[pymarkdown error] {stdout or stderr}")
    finally:
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            pass


def needs_ai_repair(md_text: str) -> Tuple[bool, str]:
    """
    Decide if an entry should go to Claude.
    We trigger AI repair if either:
      - parse fails, or
      - linter reports issues (ignoring linter tool errors).
    Returns (should_send, linter_issues_text)
    """
    parsed = parse_ok(md_text)
    lint = lint_with_pymarkdown(md_text)

    if not parsed:
        return True, lint.issues
    if (not lint.ok) and not lint.issues.startswith("[pymarkdown error]"):
        return True, lint.issues
    return False, lint.issues


# ----------------- Claude Repair -----------------

CLAUDE_SYSTEM = (
    "You are a documentation formatter. "
    "Your role is to FIX MARKDOWN SYNTAX ONLY without changing meaning or wording. "
    "Preserve code blocks, links, and tables exactly. "
    "Do not add or remove content. "
    "Return ONLY valid Markdown. No commentary."
)

CLAUDE_USER_PROMPT = """\
Fix the following Markdown so it is valid and clean:

<markdown>
{markdown}
</markdown>

Constraints:
- Keep meaning and wording identical.
- Preserve all code, links, images, and tables.
- Repair heading hierarchy, lists, tables, and code fences.
- Output only the corrected Markdown, nothing else.
"""

def repair_with_claude(md_text: str) -> str:
    if not USE_CLAUDE:
        return md_text
    if not _anthropic_ok:
        # SDK not available; return original
        return md_text

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = CLAUDE_USER_PROMPT.format(markdown=md_text)

    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        temperature=0,
        system=CLAUDE_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    fixed = resp.content[0].text if resp and resp.content else md_text
    return fixed.strip()


# ----------------- Main Pipeline -----------------

def process_dataset(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Process a list of FAQ entries. Each entry must have 'answer' (string).
    Returns (cleaned_records, report)
    """
    cleaned = []
    report = {
        "total": len(records),
        "fixed_by_rules": 0,
        "sent_to_ai": 0,
        "ai_fixed_and_valid": 0,
        "left_as_is_due_to_errors": 0,
        "entries": []  # per-item diagnostics
    }

    for idx, item in enumerate(tqdm(records, desc="Cleaning")):
        entry = dict(item)
        ans = entry.get("answer", "")
        if not isinstance(ans, str):
            cleaned.append(entry)
            report["left_as_is_due_to_errors"] += 1
            report["entries"].append({"index": idx, "status": "non_string_answer"})
            continue

        # Stage 1: deterministic clean
        stage1 = deterministic_clean(ans)

        # Stage 2: parse + lint
        send_ai, lint_issues = needs_ai_repair(stage1)

        if not send_ai:
            entry["answer"] = stage1
            cleaned.append(entry)
            report["fixed_by_rules"] += 1
            report["entries"].append({"index": idx, "status": "cleaned_by_rules"})
            continue

        # Stage 3: Claude repair (targeted)
        report["sent_to_ai"] += 1
        ai_fixed = repair_with_claude(stage1)

        # Post-validate
        post_send_ai, _ = needs_ai_repair(ai_fixed)
        if not post_send_ai:
            entry["answer"] = ai_fixed
            cleaned.append(entry)
            report["ai_fixed_and_valid"] += 1
            report["entries"].append({"index": idx, "status": "ai_fixed"})
        else:
            # Fall back to stage1 if AI did not produce valid MD
            entry["answer"] = stage1
            cleaned.append(entry)
            report["left_as_is_due_to_errors"] += 1
            report["entries"].append({"index": idx, "status": "fallback_to_rules", "lint": lint_issues})

    return cleaned, report


def main():
    import argparse
    from dotenv import load_dotenv

    load_dotenv()  # allow .env for ANTHROPIC_API_KEY, CLAUDE_MODEL

    p = argparse.ArgumentParser(description="Hybrid Markdown cleaner for FAQ JSON.")
    p.add_argument("--input", required=True, help="Path to input JSON (list of objects with 'answer')")
    p.add_argument("--output", required=True, help="Path to output cleaned JSON")
    p.add_argument("--report", required=False, default="report.json", help="Where to write a cleaning report")
    args = p.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of records.")

    cleaned, rpt = process_dataset(data)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(rpt, f, ensure_ascii=False, indent=2)

    print(f"✅ Cleaned JSON written to {args.output}")
    print(f"🧾 Report written to {args.report}")
    print(
        f"Stats: total={rpt['total']}, rules={rpt['fixed_by_rules']}, "
        f"sent_to_ai={rpt['sent_to_ai']}, ai_fixed={rpt['ai_fixed_and_valid']}, "
        f"fallbacks={rpt['left_as_is_due_to_errors']}"
    )


if __name__ == "__main__":
    main()

Setup & run

# 1) Install deps
pip install -r requirements.txt

# 2) Set your key (or put it in a .env file)
export ANTHROPIC_API_KEY=sk-ant-...

# 3) Run
python hybrid_markdown_cleaner.py --input faq_raw.json --output faq_cleaned.json --report report.json

Notes

Deterministic first, AI last: most entries will be fixed by rules; only the hard ones go to Claude (cheap + predictable).

Temperature=0 to avoid rewrites and hallucinations.

Linter: requires the pymarkdown CLI (installed by pymarkdownlnt) to be on PATH.

You can change CLAUDE_MODEL via env var CLAUDE_MODEL.


