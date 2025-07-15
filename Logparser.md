Below is a hands-on blueprint for reproducing “stage-that-failed” detection in Python, inspired by the way Jenkins’ open-source Log Parser Plugin works.


---

1  | How the original plugin does it (quick reverse-engineering)

Concern	What the Jenkins plugin does	Where to see it

Load user rules	Reads a plain-text rules file (one regex per category)	LogParserUtils.readParsingRules() in the parser class 
Compile once	Compiles each regex only once and keeps the compiled array in memory	constructor of LogParserParser 
Stream the log	Reads the console log line-by-line to avoid RAM blow-ups	parseLog() loop 
Track counts & produce HTML	Keeps hash maps of error/warn/info counts, writes colored HTML + index pages as it goes	same method
Affect build result	If a rule tagged ERROR matches, can mark the build failed/unstable	LogParserPublisher.perform() 


The core pattern is therefore:

open(log_stream)
for line in log_stream:
    status = classify(line)     # regex table lookup
    update_counters(status)
    if status == ERROR: mark_fail


---

2  | A Python version focused on stages rather than generic errors

2.1 Console-log anatomy for Pipeline jobs

Typical entries created by Jenkins classic / Blue Ocean:

[Pipeline] stage
[Pipeline] { (Checkout)
...
[Pipeline] } // (Checkout)
...
ERROR: script returned exit code 1

That means we need to:

1. Detect “entering stage” lines → remember current stage name.


2. Observe failure patterns inside that stage.


3. Emit a summary like {'Build': 'FAILED', 'Test': 'OK', …}.



2.2 Minimal parser module (stage_log_parser.py)

import re
from pathlib import Path
from typing import Dict, List, Iterable

# --- Regex patterns (tweak if your log format differs) ----------------------
STAGE_START  = re.compile(r'Pipeline\s+stage.*?([^)]+)')  # Capture stage name
STAGE_WRAPPED= re.compile(r'Pipeline\s+\{\s+([^)]+)')     # Blue Ocean alt
STAGE_END    = re.compile(r'Pipeline\s+\}')                   # closing brace
FAIL_PATTERN = re.compile(r'(?i)\b(FATAL|ERROR|FAILURE|exception)\b')
SKIP_PATTERN = re.compile(r'\bstage was skipped due to\W+', re.I)  # optional

def analyse_log(lines: Iterable[str]) -> Dict[str, Dict]:
    """
    Return {stage_name: {'failed': bool, 'first_fail_line': int, 'start': int, 'end': int}}
    """
    result, cur_stage = {}, None
    cur_start = None

    for idx, line in enumerate(lines, 1):
        m_start = STAGE_START.search(line) or STAGE_WRAPPED.search(line)
        if m_start:
            cur_stage  = m_start.group(1).strip()
            result.setdefault(cur_stage, dict(start=idx, end=None, failed=False,
                                              first_fail_line=None))
            cur_start  = idx
            continue

        if STAGE_END.search(line) and cur_stage:
            result[cur_stage]['end'] = idx
            cur_stage = None
            continue

        if cur_stage and FAIL_PATTERN.search(line) and not SKIP_PATTERN.search(line):
            st = result[cur_stage]
            st['failed'] = True
            st.setdefault('first_fail_line', idx)

    return result

# ---------------------------------------------------------------------------

def parse_file(path: Path) -> Dict:
    with path.open('r', errors='replace') as fh:
        return analyse_log(fh)

2.3 CLI utility for bulk processing (jenkins_parse.py)

import csv, concurrent.futures, json, sys
from pathlib import Path
from stage_log_parser import parse_file

ROOT = Path(sys.argv[1])  # dir containing console logs e.g. build_*/log

def parse_one(path: Path):
    build_id = path.parent.name          # e.g. build_4832
    return {'build': build_id,
            'stages': parse_file(path)}

def main():
    logs = list(ROOT.rglob('log'))       # adapt pattern for your storage
    with concurrent.futures.ProcessPoolExecutor() as ex:
        parsed = list(ex.map(parse_one, logs))

    # Write summary CSV
    with open('stage_failures.csv', 'w', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(['build', 'stage', 'failed', 'first_fail_line'])
        for row in parsed:
            for st, meta in row['stages'].items():
                writer.writerow([row['build'], st, meta['failed'],
                                 meta.get('first_fail_line')])

    # Optional: write JSON blob for BI tools
    Path('stage_failures.json').write_text(json.dumps(parsed, indent=2))

if __name__ == '__main__':
    main()

Run

python jenkins_parse.py /var/jenkins_home/jobs/my-pipeline/builds


---

3  | Scaling to 100 k builds / 20 k devs

Challenge	Python tactic

I/O throughput (each console log can be 5–50 MB)	Stream line-by-line (no read-all-into-RAM).
CPU (regex heavy)	Pre-compile regex once per worker process. Use concurrent.futures.ProcessPoolExecutor so each CPU core handles a different log file.
Storage of results	Emit CSV/JSON then bulk-load into a columnar store (DuckDB, BigQuery, ClickHouse) for dashboarding.
Incremental updates	Wrap script in a cron job; skip logs whose parsed.marker file already exists.
Integration with Jenkins	1. Use Jenkins REST API /consoleText to fetch fresh logs; or 2. Configure archiveArtifacts to copy logs to an NFS/S3 bucket that the parser can read.



---

4  | Optional: make it look like the Jenkins plugin

If your devs like the colorised HTML view:

1. Re-use the rules-file idea – a simple text file:

ERROR /FATAL|ERROR|FAILURE|Exception/
WARNING /WARN|deprecated/
INFO    /INFO/


2. In Python, wrap each matched line with <span class="error">, <span class="warn"> etc.
Alternatively, output ANSI color codes and let modern terminals render them.


3. Generate a small index.html with links to each stage section exactly as the Java plugin does.
All the plumbing is visible in LogParserWriter.writeReferenceHtml() if you need HTML details .




---

5  | Next steps

Goal	Add-on idea

Alert the right squad immediately	Feed the CSV into Grafana Loki, use label {stage="Build",failed="true"} for alert-rules.
Auto-open a Jira ticket	Call Jira REST in the “post-parse” script when failed == True and no ticket exists.
Feedback to developers in PR	Post a GitHub check with the failing stage summary so a dev sees it before merge.



---

TL;DR

1. The original plugin just streams the log, applies a pre-compiled regex table, counts, and writes HTML.


2. In Python we can achieve the stage-failure subset with ~100  lines of code.


3. Parallelise with ProcessPoolExecutor; store results in CSV/DB for 100 k-build scale.


4. Keep the rules file external so ops can update patterns without redeploying code.



This mirrors the proven Jenkins design while fitting naturally into a Python toolchain.

