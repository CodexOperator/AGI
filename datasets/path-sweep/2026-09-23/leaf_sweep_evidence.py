#!/usr/bin/env python3
"""Director-side evidence for one LEAF sweep kid (hypothesis:lm-town-code-host-paths-resolve-through-paths-cells).

Writes <label>-evidence.json under paths.local_maxxing.path_sweep_out_dir: the node's FALSIFIERS regex over
the kid's files at the base and at the harvest tip, and the value table -- each cell the kid used, the literal
it replaced, what paths.get() and the paths.py CLI return now, and whether they are byte-identical.

Run from the checkout root:
  python3 datasets/path-sweep/2026-09-23/leaf_sweep_evidence.py <label> <base> <tip> <cells.json> <file>...
cells.json maps cell -> the literal it replaced.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, ".agi", "context", "local-maxxing"))
import paths  # noqa: E402

REGEX = r"""(['"=( ]|^)(/data/|/home/|/mnt/|/media/|/tmp/|/opt/|~/)"""


def grep(rev, files):
    r = subprocess.run(["git", "grep", "-n", "-I", "-E", REGEX, rev, "--"] + files,
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode not in (0, 1):  # 1 = no match; anything else (a bad rev) must not read as "0 hits"
        raise SystemExit("git grep failed on %r: %s" % (rev, r.stderr.strip()))
    return [ln.split(":", 1)[1] for ln in r.stdout.splitlines() if ln]


def main():
    label, base, tip, cells_path = sys.argv[1:5]
    files = sys.argv[5:]
    cells = json.load(open(cells_path))
    table = []
    for cell, literal in sorted(cells.items()):
        got = paths.get(cell)
        cli = subprocess.run([sys.executable, ".agi/context/local-maxxing/paths.py", cell],
                             cwd=ROOT, capture_output=True, text=True).stdout.strip()
        table.append({"cell": cell, "old_literal": literal, "get": got, "cli": cli,
                      "identical": got == literal and cli == literal})
    before, after = grep(base, files), grep(tip, files)
    rec = {"label": label, "base": base, "tip": tip, "regex": REGEX, "files": files,
           "before_hits": len(before), "before": before, "after_hits": len(after), "after": after,
           "cells": len(table), "cells_identical": sum(r["identical"] for r in table), "table": table}
    out = os.path.join(paths.get_local("path_sweep_out_dir"), label + "-evidence.json")
    with open(out, "w") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    print(out, "before", len(before), "after", len(after), "identical", rec["cells_identical"], "of", len(table))


if __name__ == "__main__":
    main()
