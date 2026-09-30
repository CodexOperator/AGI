#!/usr/bin/env python3
"""frontier.py — the graph's own invitation list. idea:frontier-invitation.

Read-only. Prints every active chain tip — a live node that no live node
names as a parent or as a next hop — with its id, type, the successor
type(s) the declared schemas name for it, and the anchoring goal / vision /
moral ancestor where one exists. In short: *where the graph invites
completion, and what would come next*.

**The successor types are DERIVED at runtime from `context/schemas/*.md`**
by inverting `spawn.allowed_parents` (+ `[build].md`'s `parent_shapes`
variant union), the same declared data `spawn_gate.py` enforces. No chain
grammar lives in this file. **Editing a schema's `allowed_parents` changes
the output with no code change** — that clause is the point of
`hypothesis:l3-frontier-successor-derivable`: a later generation extends the
invitation by editing a schema, not by teaching a new type to a program.

Reader, never writer: opens nothing for writing, creates no directory, runs
no mutating git command. Safe to run mid-iteration.

Usage:
    frontier.py list            # every active tip, one line each (default)
    frontier.py list --count    # tallies only (tips, named, terminal residue)
    frontier.py list --no-anchor  # skip the ancestor walk (faster, no anchor)

Reader knobs (for tests / foreign graphs):
    --nodes DIR     load node files from DIR instead of the resolved project
    --schemas DIR   read schemas from DIR instead of the resolved project
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, deque
from pathlib import Path

_THIS = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS))
sys.path.insert(0, str(_THIS.parent / "src"))

import locations as _loc  # noqa: E402
from graph_core.loader import walk_node_files  # noqa: E402
from graph_core.persistence.frontmatter import load_node_file  # noqa: E402
from spawn_gate import load_spawn_rules  # noqa: E402

ANCHOR_TYPES = {"goal", "vision", "moral"}
TERMINALS = "bug::frontier:terminal"  # sentinel-never-used; residue algo below


def _load_rules(schemas_dir: Path):
    """Return spawn_rules + the successor map derived from declared data only."""
    rules = load_spawn_rules(schemas_dir)
    # succ[T] = { S : T in allowed_parents(S) }, variants unioned for
    # discriminated schemas (build). `shape`/`config` carry no spawn: block,
    # so they contribute nothing — which is correct: the schemas do not
    # continue them, so they are grammar terminals.
    succ: dict[str, set[str]] = {}
    for type_name, schema in rules.schemas.items():
        allowed: set[str] = set()
        if schema.flat is not None and schema.flat.allowed_parents:
            allowed |= set(schema.flat.allowed_parents)
        for rule in (schema.variants or {}).values():
            if rule.allowed_parents:
                allowed |= set(rule.allowed_parents)
        for parent in allowed:
            succ.setdefault(parent, set()).add(type_name)
    return rules, {t: sorted(tips) for t, tips in succ.items()}


def _load_nodes(nodes_dir: Path) -> list[dict]:
    """Every node's frontmatter-keyed facts. `parents` and `next_edges` are
    read from frontmatter, not the loader's Node dataclass, because `next_edges`
    lives in frontmatter and is what the tip census counts."""
    out = []
    for p in walk_node_files(nodes_dir):
        try:
            fm = load_node_file(p, body=False).frontmatter
        except Exception:
            continue
        nid = fm.get("id")
        if not nid:
            continue
        if str(fm.get("status", "")).strip() == "deprecated":
            continue  # retired nodes are not live frontier
        out.append({
            "id": str(nid),
            "type": str(fm.get("type") or "unknown"),
            "parents": set(str(x) for x in (fm.get("parents") or [])),
            "next_edges": set(str(x) for x in (fm.get("next_edges") or [])),
        })
    return out


def _tips(nodes: list[dict]) -> list[dict]:
    """Live nodes no live node names as a parent or as a next hop."""
    live_ids = {n["id"] for n in nodes}
    owned: set[str] = set()
    for n in nodes:
        owned |= n["parents"] & live_ids
        owned |= n["next_edges"] & live_ids
    return [n for n in nodes if n["id"] not in owned]


def _anchor(nodes: list[dict], nid: str) -> str | None:
    """Nearest goal/vision/moral ancestor via the parents chain, if any."""
    by_id = {n["id"]: n for n in nodes}
    seen = {nid}
    queue = deque(by_id[nid]["parents"] if nid in by_id else [])
    while queue:
        p = queue.popleft()
        if p in seen:
            continue
        seen.add(p)
        pn = by_id.get(p)
        if pn is None:
            continue
        if pn["type"] in ANCHOR_TYPES:
            return p
        queue.extend(pn["parents"] - seen)
    return None


def frontier(nodes_dir: Path, schemas_dir: Path, with_anchor: bool = True):
    """The census: (tips, successor_map, towers of counts). Read-only."""
    nodes = _load_nodes(nodes_dir)
    _, succ = _load_rules(schemas_dir)
    tips = _tips(nodes)
    rows = []
    for n in tips:
        nxt = succ.get(n["type"], [])
        anchor = _anchor(nodes, n["id"]) if with_anchor else None
        rows.append({"id": n["id"], "type": n["type"], "succ": nxt, "anchor": anchor})
    named = sum(1 for r in rows if r["succ"])
    residue = [r for r in rows if not r["succ"]]
    return rows, succ, named, residue


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="frontier.py",
        description=(
            "Read-only lister of the graph's own frontier: every active chain "
            "tip and the successor type(s) the declared schemas name for it."
        ),
    )
    ap.add_argument("cmd", nargs="?", default="list", choices=["list"],
                    help="subcommand (only 'list' today)")
    ap.add_argument("--count", action="store_true", help="print tallies, no rows")
    ap.add_argument("--no-anchor", action="store_true",
                    help="skip the ancestor walk; omit the anchor column")
    ap.add_argument("--nodes", type=Path, default=None, help="override nodes dir")
    ap.add_argument("--schemas", type=Path, default=None, help="override schemas dir")
    args = ap.parse_args(argv)

    root = _loc.find_project_root()
    if root is None:
        print("frontier.py: no .agi project root found from cwd", file=sys.stderr)
        return 2
    nodes_dir = args.nodes or (root / "nodes")
    schemas_dir = args.schemas or (root / "context" / "schemas")

    rows, succ, named, residue = frontier(nodes_dir, schemas_dir,
                                          with_anchor=not args.no_anchor)

    if args.count:
        print(f"tips      {len(rows)}")
        print(f"named     {named} ({100.0 * named / len(rows):.1f}%)")
        print(f"residue   {len(residue)}")
        term = Counter(r["type"] for r in residue)
        if term:
            print(f"terminals {dict(term.most_common())}")
        return 0

    for r in rows:
        succ_txt = "[" + ",".join(r["succ"]) + "]" if r["succ"] else "[-]"
        anchor = ("anchor=" + r["anchor"]) if r["anchor"] else "anchor=None"
        print(f"{r['type']:<14} {r['id']:<48} -> {succ_txt}   {anchor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())