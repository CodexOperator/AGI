#!/usr/bin/env python3
"""Committed re-runnable gate for the `dh-54` MUR demote causes.

`mur-g7-31-2-2-dh-54-f5d58744e-lean` returned **demote** on `goal:g7.31.2.2`:
three refuted defects survived on the committed bytes and four residues the
verify pass missed. The DH.73 round closed all seven by text / frontmatter
correction plus one committed gate. This IS that gate.

The predecessor (`residue_gate.py`) lived under `.agi/sessions/`, which is
gitignored, so the only evidence for the round was uncommitted and
unreproducible. This script is tracked.

Each check prints `[PASS]` / `[FAIL]`; the process exits 0 only when all pass.
It reads the graph nodes only -- no production code is imported or executed.

Usage:
    python3 extensions/agi/tests/probes/dh54_mur_residue_gate.py [--root DIR]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CHECKS = []


def check(label: str):
    def deco(fn):
        CHECKS.append((label, fn))
        return fn
    return deco


def _find_graph_root(start: Path) -> Path:
    """Nearest enclosing `.agi/nodes` above the script, else cwd walk-up."""
    for base in (start, Path.cwd()):
        here = base.resolve()
        if here.is_file():
            here = here.parent
        for cand in (here, *here.parents):
            if (cand / ".agi" / "nodes").is_dir():
                return cand / ".agi"
    raise SystemExit("could not locate .agi/nodes from %s" % start)


def _nodes(root: Path) -> Path:
    return root / "nodes"


@check("Agent Notes on a00-3c0140ac does not claim 'Closed all three DH.45 residues'")
def check_3c0140ac(root: Path) -> tuple[bool, str]:
    text = (_nodes(root) / "hypothesis" / "a00-3c0140ac-0fa4dd.md").read_text()
    bad = "Closed all three DH.45 residues" in text
    return (not bad), ("stale closure claim present" if bad else "stale claim absent")


@check("a00-33653715 probes has no conjunct-3 pass entry; Evidence drops 'probes: list is inert'")
def check_0d018f(root: Path) -> tuple[bool, str]:
    text = (_nodes(root) / "hypothesis" / "a00-33653715-0d018f.md").read_text()
    problems = []

    # Frontmatter probes: no entry combining conjunct 3 with result "pass".
    for line in text.splitlines():
        if not line.strip().startswith("- {"):
            continue
        try:
            entry = json.loads(line.strip()[2:])
        except json.JSONDecodeError:
            continue
        if entry.get("conjunct") == 3 and entry.get("result") == "pass":
            problems.append("conjunct-3 probe still results 'pass'")

    # Evidence section only: the string must be gone from the cited command tail.
    evidence = _section(text, "## Evidence")
    if "probes: list is inert" in evidence:
        problems.append("Evidence still says 'probes: list is inert'")

    return (not problems), ("; ".join(problems) or "probe demoted; Evidence corrected")


@check("experiment a00-33653715-dh45-verify Evidence drops 'probes: list is inert'")
def check_dh45_verify(root: Path) -> tuple[bool, str]:
    text = (_nodes(root) / "experiment" / "a00-33653715-dh45-verify.md").read_text()
    evidence = _section(text, "## Evidence")
    bad = "probes: list is inert" in evidence
    return (not bad), ("stale annotation present" if bad else "stale annotation absent")


@check("goal:g7.31.2.2 drops 'NO merge-up while residues>0' as a live directive")
def check_goal(root: Path) -> tuple[bool, str]:
    text = (_nodes(root) / "goal" / "g7.31.2.2.md").read_text()
    # The phrase is allowed to survive as a backticked REFERENCE (the closed
    # residue table names the string it removed). It must not survive as a
    # live instruction, so strip inline-code spans before asserting absence.
    bad = "NO merge-up while residues>0" in _without_inline_code(text)
    return (not bad), ("stale line present" if bad else "stale line absent (only referenced)")


def _without_inline_code(text: str) -> str:
    """Drop ``` `...` ``` spans so a *reference* to a string is not a claim."""
    return re.sub(r"`[^`]*`", "", text)


def _section(text: str, header: str) -> str:
    """Return the body between `header` and the next `## ` header (or EOF)."""
    m = re.search(r"^%s\s*$" % re.escape(header), text, re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##? ", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None,
                    help="a path inside the project (default: walk up from this file)")
    args = ap.parse_args(argv)

    graph = _find_graph_root(Path(args.root or __file__))
    print("graph:", graph)
    failures = 0
    for label, fn in CHECKS:
        try:
            ok, detail = fn(graph)
        except Exception as exc:  # a missing/stale node is itself a failure
            ok, detail = False, "ERROR %s: %s" % (type(exc).__name__, exc)
        print("[%s] %s -- %s" % ("PASS" if ok else "FAIL", label, detail))
        if not ok:
            failures += 1

    print("%s: %d/%d checks passed" %
          ("ALL PASS" if not failures else "FAILURES", len(CHECKS) - failures, len(CHECKS)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())