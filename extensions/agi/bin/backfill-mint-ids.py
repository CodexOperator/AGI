#!/usr/bin/env python3
"""backfill-mint-ids.py — one-time additive backfill: give every existing
node a permanent `mint_id`, without renaming, moving, or touching anything
else about it.

See goal:g2.5 ("Tension resolved 2026-08-25: two identifiers, two jobs") in
the graph repo for the design this implements: an *address* is short and
re-derived freely (retag a node, its address changes); the *mint id* is
opaque and never changes, and it is what `grid.py` keys per-node version
history on from here forward (see `grid.py`'s `write_ref_for` /
`mint_node_ref`). A node minted before this script existed has no mint id at
all, so every node in the corpus needs exactly one write to gain one.

**Purely additive.** This script:
  - never renames a node's `id`
  - never moves a grid ref (that is a SEPARATE, unrun step — see
    `grid.py plan-mint-refs`, report-only, no `--write`)
  - never rewrites a node that already carries a non-empty `mint_id`
  - never touches `body`, `parents`, `payload_ref`, or any field this script
    does not itself own

**Idempotent by construction.** A node is skipped, not re-minted, the
instant `fm.get("mint_id")` is a non-empty string — no file write happens
for it at all (not even a reformat), so running this twice over an
already-backfilled corpus writes zero files the second time. This is
verified in tests by hashing file contents before/after a repeat run, not
just by checking the printed counts.

**Reuses `write_frontmatter` from `snapshot-goals.py` — never a bespoke
serializer.** Imported by file path (the module's filename has a hyphen and
is not importable), the same convention `level3.py` and
`decompose-engine.py` already use for the identical reason: a project here
once lost fields to a from-scratch re-serialize (H0i), and `write_frontmatter`
is the one place that failure was fixed.

Usage:
  python3 bin/backfill-mint-ids.py --project PATH            # dry-run (default)
  python3 bin/backfill-mint-ids.py --project PATH --write    # apply
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import yaml

BIN_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = BIN_DIR.parent  # .../extensions/agi

# graph_core.identity — the ENGINE's own copy, always, regardless of what a
# project's src/ might shadow it with (mint_permanent_id is brand new; a
# project checkout cannot have its own compatible copy yet).
_graph_core_src = str(PLUGIN_ROOT / "src")
if _graph_core_src not in sys.path:
    sys.path.insert(0, _graph_core_src)
from graph_core.identity import mint_permanent_id  # noqa: E402
from frontmatter import split_frontmatter  # noqa: E402

# --- reuse snapshot-goals.py's write_frontmatter, by file path (see module
# docstring) — not a copy, the actual function. ---------------------------
_SNAPSHOT_GOALS_PATH = BIN_DIR / "snapshot-goals.py"
_spec = importlib.util.spec_from_file_location("snapshot_goals", _SNAPSHOT_GOALS_PATH)
snapshot_goals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_goals)
write_frontmatter = snapshot_goals.write_frontmatter


def iter_node_files(project_root: Path):
    nodes_dir = project_root / "nodes"
    if not nodes_dir.is_dir():
        return
    yield from sorted(nodes_dir.rglob("*.md"))


def read_node(path: Path) -> tuple[dict, str] | None:
    """Parse `path` into (frontmatter dict, body text). None if unparseable —
    never guessed, never repaired; those files are reported and skipped."""
    text = path.read_text(encoding="utf-8")
    if not text.strip().startswith("---"):
        return None
    parted = split_frontmatter(text)
    if parted is None:
        return None
    try:
        fm = yaml.safe_load(parted[0])
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    return fm, parted[1]


def backfill(project_root: Path, write: bool) -> dict:
    """Walk every node file once; mint and (optionally) write a `mint_id`
    for any that lack one. Returns the counts this run's report line uses,
    so tests can assert on the same numbers a human reads."""
    total = already = minted = unparseable = 0
    for path in iter_node_files(project_root):
        total += 1
        parsed = read_node(path)
        if parsed is None:
            unparseable += 1
            print(f"SKIP (unparseable frontmatter): {path}", file=sys.stderr)
            continue
        fm, body = parsed
        existing = fm.get("mint_id")
        if isinstance(existing, str) and existing.strip():
            already += 1
            continue  # idempotent: never re-minted, never rewritten
        new_id = mint_permanent_id()
        minted += 1
        verb = "MINT" if write else "WOULD-MINT"
        print(f"{verb}  {fm.get('id', path.name)}  mint_id={new_id}")
        if write:
            new_fm = dict(fm)
            new_fm["mint_id"] = new_id
            write_frontmatter(path, new_fm, body)
    return {
        "total": total,
        "already": already,
        "minted": minted,
        "unparseable": unparseable,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", default=None,
                    help="project root containing nodes/ (default: cwd)")
    ap.add_argument("--write", action="store_true",
                    help="apply; default is dry-run (report only, writes nothing)")
    args = ap.parse_args(argv)

    project_root = (Path(args.project).resolve() if args.project
                     else Path.cwd().resolve())
    if not (project_root / "nodes").is_dir():
        sys.exit(f"ERR: no nodes/ under {project_root}")

    counts = backfill(project_root, write=args.write)
    mode = "write" if args.write else "dry-run"
    print(f"backfill-mint-ids ({mode}): {counts['total']} node file(s), "
          f"{counts['already']} already had mint_id, "
          f"{counts['minted']} {'minted' if args.write else 'would mint'}, "
          f"{counts['unparseable']} unparseable/skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
