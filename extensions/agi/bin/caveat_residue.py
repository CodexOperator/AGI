#!/usr/bin/env python3
"""SCOPED form of goal:g1.31.4.1 falsifier 2 (the "bad --target" caveat).

The goal's own negative falsifier greps the WHOLE .agi/nodes tree, so the
goal's two legitimate quotes of the retired phrase (target end-state line 33,
falsifier line 42) satisfy the bar themselves and a real residue is
unreadable behind them. A goal legitimately QUOTES the caveat it retired; a
ROUND node that ASSERTS a finding may not. Scope = the node kinds that assert
findings; `goal/` is excluded BY NAME, and the exclusion is part of the claim.

    scan(<nodes_root>) -> [(relpath, lineno, line), ...]
    PHRASE / SCOPE    the mechanism, importable so a test can drive it.

The caller decides the exit code; the check is a function so it can be tested
red as easily as green.
"""

# The retired caveat, verbatim, as goal:g1.31.4.1 quotes it.
PHRASE = "bad --target is not caught|bad --target uncaught"

# Node kinds that ASSERT findings. `goal` is deliberately absent: a goal
# quotes the caveat it retired on purpose. `deprecated` is a status, not a
# kind, and holds prior art -- excluded with goal for the same reason.
SCOPE = ("experiment", "hypothesis", "verdict", "build", "mvp", "outcome")


def scan(nodes_root):
    """Return every (relpath, lineno, line) in SCOPE carrying the phrase."""
    import re
    pat = re.compile(PHRASE)
    hits = []
    for kind in SCOPE:
        d = nodes_root / kind
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*.md")):
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                if pat.search(line):
                    hits.append((str(f.relative_to(nodes_root)), i, line.strip()))
    return hits


def main(argv=None):
    """`caveat_residue.py [nodes_root]` — exit 1 on a live residue."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from agi.bin import locations
    argv = sys.argv[1:] if argv is None else argv
    root = Path(argv[0]) if argv else locations.find_project_root(Path(__file__).resolve()) / "nodes"
    hits = scan(root)
    for rel, ln, text in hits:
        print(f"{rel}:{ln}: {text}")
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
