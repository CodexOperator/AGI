#!/usr/bin/env python3
"""merge_gate.py -- ONE word from the council report (hypothesis:g716107-...).

`merge_gate.py check BASE TIP [--prime-count N]` prints `merge` or `hold` as its
FIRST line, then one line per reason, and exits 0 merge / 1 hold / 2 cannot
answer. The rules are IMPORTED, never copied: `reds` (the REDs, run in-process
over BASE..TIP), `council_report` (the ONE report node + its row shape), and
`locations` (the project root, the source root). The cell
`merge_gate.review_paths` names the path prefixes a commit must be covered for;
absent = rc 2 naming it -- never a silent merge.
"""
from __future__ import annotations
import argparse, io, json, re, subprocess, sys
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import council_report, locations, reds  # noqa: E402

CELL = "merge_gate.review_paths"
BUDGET = "unreviewed:budget"
_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")


def _git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"git {args[0]} exit {p.returncode}")  # the VERB and the code, never git's stderr BYTES
    return p.stdout


def review_paths(root: Path) -> list[str]:
    """The ONE cell `merge_gate.review_paths`, as `dir/` prefixes. Absent, not a
    list of strings, or empty = rc 2 naming the cell."""
    cfg = locations.config_path(root)
    try:
        cell = (json.loads(cfg.read_text(encoding="utf-8")).get("merge_gate") or {}
                if cfg and cfg.is_file() else {})
    except ValueError as exc:
        raise RuntimeError(f"{CELL}: {cfg.name} does not parse ({type(exc).__name__})") from None
    want = cell.get("review_paths")
    if not isinstance(want, list) or not want or not all(isinstance(p, str) and p for p in want):
        raise RuntimeError(f"config cell {CELL} is absent -- name the review paths "
                           f"and the gate can answer")
    return [p.rstrip("/") + "/" for p in want]


def report_rows(root: Path) -> list[tuple[str, str, str]]:
    """[(old, new, state)] per doc:council-report row, read through
    council_report's OWN reader. A report with no usable old..new row = rc 2:
    the gate has nothing to hold against."""
    body = council_report.node_body(root, council_report.REPORT_NODE)
    out = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("|-") or line == council_report.HEADER[0]:
            continue      # the header row is council_report's, never a round
        m = _ROW.match(line)
        old, _, new = (m.group(2).partition("..") if m else ("", "", ""))
        if m and old and new and old != "?" and new != "?":
            out.append((old, new, m.group(3)))
    if not out:
        raise RuntimeError(f"{council_report.REPORT_NODE} holds no old..new row -- "
                           f"the gate cannot answer")
    return out


def _reds(repo: Path, root: Path, base: str, tip: str) -> list[str]:
    """The RED lines reds.py printed over BASE..TIP -- the check is reds', never
    a copy here. reds rc 2 (it cannot answer) is rc 2 here too."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = reds.main(["check", base, tip, "--root", str(root), "--repo", str(repo)])
    if rc == 2:
        raise RuntimeError("reds.py cannot answer over this range")
    return [ln.rstrip() for ln in buf.getvalue().splitlines()
            if ln.startswith("RED ") and not ln.startswith("RED none")]


def uncovered(repo: Path, base: str, tip: str, prefixes: list[str],
              rows: list[tuple[str, str, str]]) -> list[str]:
    """Non-merge commits in BASE..TIP that touch a review path and lie in NO
    row's old..new range. Coverage is the union of `git rev-list old..new` over
    the rows -- one walk per row, never a pairwise ancestry loop."""
    covered: set[str] = set()
    for old, new, _state in rows:
        covered |= set(_git(repo, "rev-list", f"{old}..{new}").split())
    out = []
    for line in _git(repo, "rev-list", "--no-merges", f"{base}..{tip}").splitlines():
        sha = line.split()[0] if line.split() else line.strip()
        if not sha or sha in covered:
            continue
        paths = _git(repo, "show", "--name-only", "--format=", sha).splitlines()
        if any(p.startswith(pre) for p in paths if p.strip() for pre in prefixes):
            out.append(sha[:20])
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the merge gate: ONE word from the council report")
    ap.add_argument("verb", choices=["check"])
    ap.add_argument("base", help="a rev at the range's start")
    ap.add_argument("tip", help="a rev at the range's end")
    ap.add_argument("--prime-count", type=int, default=None,
                    help="the Prime's count of unreviewed:budget rows")
    ap.add_argument("--root", help="the project (default: the nearest enclosing .agi/)")
    ap.add_argument("--repo", help="the git repo (default: the source root)")
    a = ap.parse_args(argv)
    root = locations.find_project_root(a.root) if a.root else locations.find_project_root()
    if root is None:
        print("merge_gate: no agi project found", file=sys.stderr); return 2
    repo = Path(a.repo) if a.repo else locations.source_root(root)
    try:
        prefixes, rows = review_paths(root), report_rows(root)
        _git(repo, "rev-list", "--count", f"{a.base}..{a.tip}")   # a rev that cannot be read is rc 2
        why = [f"a RED holds it -- {ln}" for ln in _reds(repo, root, a.base, a.tip)]
        why += [f"uncovered review-path commit {s}"
                for s in uncovered(repo, a.base, a.tip, prefixes, rows)]
        budget = [r for r in rows if r[2] == BUDGET]
        if budget and a.prime_count != len(budget):
            why.append(f"{len(budget)} {BUDGET} rows, --prime-count {a.prime_count}")
    except Exception as exc:
        print(f"merge_gate: {exc if type(exc) is RuntimeError else type(exc).__name__}",
              file=sys.stderr)
        return 2
    print("hold" if why else "merge")
    for line in why:
        print(f"  {line}")
    return 1 if why else 0


if __name__ == "__main__":
    raise SystemExit(main())
