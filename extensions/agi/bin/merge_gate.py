#!/usr/bin/env python3
"""merge_gate.py -- ONE word from the council report (hypothesis:g716107-...).
`check BASE TIP [--prime-count N]` prints `merge` or `hold` FIRST, then one line per
reason; rc 0/1/2. Rules are IMPORTED, never copied: `reds` in-process,
`council_report` (reader, HEADER, state vocabulary), `locations`. An absent
`merge_gate.review_paths` cell = rc 2 naming it, never a silent merge.
"""
from __future__ import annotations
import argparse, io, json, re, subprocess, sys
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import council_report, locations, reds  # noqa: E402

CELL = "merge_gate.review_paths"
BUDGET = council_report.BUDGET_STATE
_MARK, _CAP = "@@", 20
_ROW = re.compile(r"^\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


def _git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"git {args[0]} exit {p.returncode}")  # the VERB and the code, never git's stderr BYTES
    return p.stdout


def review_paths(root: Path) -> list[str]:
    """The ONE cell. Absent, not a list of strings, or empty = rc 2 naming it."""
    cfg = locations.config_path(root)
    try:
        cell = (json.loads(cfg.read_text(encoding="utf-8")).get("merge_gate") or {}
                if cfg and cfg.is_file() else {})
    except ValueError as exc:
        raise RuntimeError(f"{CELL}: {cfg.name} does not parse ({type(exc).__name__})") from None
    want = cell.get("review_paths")
    if not isinstance(want, list) or not want or not all(isinstance(p, str) and p for p in want):
        raise RuntimeError(f"config cell {CELL} is absent -- name the review paths and the gate can answer")
    return list(want)


def report_rows(root: Path) -> list[tuple[str, ...]]:
    """[(round, old, new, state, verdict)] per doc:council-report row, read through
    council_report's OWN node reader and keyed on its HEADER; no usable old..new row = rc 2."""
    body = council_report.node_body(root, council_report.REPORT_NODE)
    out = []
    for line in map(str.strip, body.splitlines()):
        m = None if line.startswith("|-") or line in council_report.HEADER else _ROW.match(line)
        old, _, new = (m.group(2).partition("..") if m else ("", "", ""))
        if m and old and new and old != "?" and new != "?":
            out.append((m.group(1), old, new, m.group(3), m.group(4)))
    if not out:
        raise RuntimeError(f"{council_report.REPORT_NODE} holds no old..new row -- the gate cannot answer")
    return out


def _reds(repo: Path, root: Path, base: str, tip: str) -> list[str]:
    """The RED lines reds.py printed over BASE..TIP -- reds' check, never a copy."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = reds.main(["check", base, tip, "--root", str(root), "--repo", str(repo)])
    if rc == 2:
        raise RuntimeError("reds.py cannot answer over this range")
    return [ln.rstrip() for ln in buf.getvalue().splitlines() if ln.startswith("RED ") and not ln.startswith("RED none")]


def uncovered(repo: Path, base: str, tip: str, prefixes: list[str],
              rows: list[tuple[str, ...]]) -> list[str]:
    """Non-merge commits in BASE..TIP touching a review path and lying in NO ACCEPTING
    row's range: coverage is `rev-list --first-parent --no-merges old..new` per row
    (a merged trunk never counts), walked ONCE by one `git log`."""
    covered: set[str] = set()
    for _r, old, new, _s, verdict in rows:
        if verdict.startswith("accept"):
            covered |= set(_git(repo, "rev-list", "--first-parent", "--no-merges", f"{old}..{new}").split())
    walk = _git(repo, "log", "--no-merges", "--name-only", f"--format={_MARK}%H", f"{base}..{tip}").splitlines()
    out, sha, paths = [], None, []
    for line in [*walk, _MARK]:      # the trailing marker flushes the last commit
        if line.startswith(_MARK):
            if sha and sha not in covered and any(q == p.rstrip("/") or q.startswith(p.rstrip("/") + "/")
                                                  for q in paths for p in prefixes):
                out.append(sha[:20])
            sha, paths = line[len(_MARK):].strip() or None, []
        elif sha and line.strip():
            paths.append(line.strip())
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
        unc = uncovered(repo, a.base, a.tip, prefixes, rows)
        why += [f"uncovered review-path commit {s}" for s in unc[:_CAP]] + \
               ([f"... {len(unc) - _CAP} more (total {len(unc)})"] if len(unc) > _CAP else [])
        why += [f"round {rnd} does not accept its range (verdict {vd or 'empty'!r})"
                for rnd, _o, _n, _st, vd in rows if not vd.startswith("accept")]
        budget = [r for r in rows if r[3] == BUDGET]
        if budget and a.prime_count != len(budget):
            why.append(f"{len(budget)} {BUDGET} rows, --prime-count {a.prime_count}")
    except Exception as exc:
        print(f"merge_gate: {exc if type(exc) is RuntimeError else type(exc).__name__}", file=sys.stderr)
        return 2
    print("hold" if why else "merge", *("  " + ln for ln in why), sep="\n")
    return 1 if why else 0


if __name__ == "__main__":
    raise SystemExit(main())
