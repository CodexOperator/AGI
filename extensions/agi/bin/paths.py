#!/usr/bin/env python3
"""paths.py audit -- read-only lister of box-specific literals (SM.125 path_max).
Classes: home, logs, tmux, user, box; names and allowlist come from boxes.py."""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import boxes  # noqa: E402
import locations  # noqa: E402
HOME_RE = re.compile(r"/home/[A-Za-z0-9._-]+|~/|\$HOME|\bexpanduser\b")
def files(root, target):
    if target:
        return [str(p) for p in sorted(Path(target).rglob("*")) if p.is_file()]
    top = locations.repo_root(root)
    out = subprocess.run(["git", "ls-files"], cwd=str(top), capture_output=True, text=True).stdout
    return [str(top / r) for r in out.splitlines()]
def classify(line, cells, classes):
    hits = ["home"] if HOME_RE.search(line) else []
    for cls, key in classes:
        v = cells.get(key) or ""
        if v and re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(v), line):
            hits.append(cls)
    v = cells.get("root") or ""
    hits += ["box"] if v and v in line else []
    return [c for i, c in enumerate(hits) if c not in hits[:i]]  # no repeats
def findings(root, target=None):
    cells, allow = boxes.box_cells(root), boxes.allow_paths(root)
    boxes.require_box_cells(root)  # absent/empty [box].md refuses by name
    missing = sorted(k for k, v in cells.items() if not v)
    if missing:
        raise ValueError("missing box cells: %s" % ", ".join(missing))
    classes = [(k.split("_")[0], k) for k in boxes.require_box_cells(root) if k != "root"]
    out = []
    for name in files(root, target):
        if any(name.endswith(a) for a in allow):
            continue
        try:
            text = Path(name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            out += ["%s:%d: %s: %s" % (name, n, c, line.strip()) for c in classify(line, cells, classes)]
    return sorted(out)
def main(argv=None):
    ap = argparse.ArgumentParser(prog="paths.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit")
    a.add_argument("dir", nargs="?")
    a.add_argument("--root", default=str(Path(__file__).resolve().parents[3] / ".agi"))
    args = ap.parse_args(argv)
    cells = boxes.box_cells(Path(args.root))
    try:
        boxes.require_box_cells(Path(args.root))
    except boxes.BoxSchemaError as err:
        print(str(err))
        return 3
    missing = sorted(k for k, v in cells.items() if not v)
    if missing:
        print("missing box cells: %s" % ", ".join(missing))
        return 2
    try:
        found = findings(Path(args.root), args.dir)
    except boxes.BoxSchemaError as err:
        print(str(err))
        return 3
    if found:
        print("\n".join(found))
    return 1 if found else 0
if __name__ == "__main__":
    raise SystemExit(main())
