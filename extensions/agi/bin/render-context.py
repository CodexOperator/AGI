#!/usr/bin/env python3
"""render-context.py — load a nodes dir, render to ASCII, write INJECTION_FILE.

Output: `context/INJECTION.md` containing:
- graph snapshot, led by the project's `metric_primary`
- chain statistics, labelled as diagnostics (never targets — TODO.md H3)
- top-N attractive chains
- the loop's rules: big-vs-small, verdict taxonomy, chain rules
- ASCII rendering (≤200 lines)

Section order is load-bearing: both injectors (the CC SessionStart hook and
the pi bridge) take only the first 80 lines, so every rule an agent must read
is emitted *before* the ASCII block.

Usage:
    python3 bin/render-context.py [nodes_dir]
    (default nodes_dir = ./nodes)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# goal:g11.1 — one resolver for every path. `bin/` goes on sys.path so the
# hyphenated filename can still reach its importable siblings.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

#: Was `... or os.getcwd()` with no ancestor walk, so this resolved the repo
#: root when run from it and the graph root when run from `.agi/` — two
#: different answers to one question, neither of them a walk.
PROJECT_ROOT = locations.project_root_from_env() or Path(os.getcwd()).resolve()

#: Re-exported from `locations` rather than redefined: the accepted marker
#: names are a property of the layout, not of this script.
config_path = locations.config_path

# Ensure project src (which has chain_engine) is on sys.path.
# Append it AFTER plugin src so plugin's graph_core takes precedence
# (graph_core types must come from plugin, chain_engine from project).
SRC = PLUGIN_ROOT / "src"
sys.path.insert(0, str(SRC))
PROJ_SRC = PROJECT_ROOT / "src"
if PROJ_SRC.is_dir():
    sys.path.append(str(PROJ_SRC))

try:
    from chain_engine.chains import find_chains
    _HAS_CHAIN_ENGINE = True
except ImportError:
    _HAS_CHAIN_ENGINE = False
    find_chains = None  # type: ignore[assignment]

from collections import defaultdict
from datetime import datetime, timezone

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from graph_core.loader import load_directory
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location('metrics_mod', Path(__file__).resolve().parent / 'metrics.py')
metrics_mod = _ilu.module_from_spec(_spec); _spec.loader.exec_module(metrics_mod)
from renderers import build_representation, render_ascii

# Sibling script: one definition of what the loop is scored on, shared so the
# injected map and the METRIC lines can never disagree (TODO.md H3).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from metrics import (  # noqa: E402
    DEFAULT_METRIC_PRIMARY,
    GAMEABLE_METRICS,
    outcome_coverage,
    primary_metric_name,
    read_config,
)

# Detect sqlite config for optional DB-backed loading

class _LiveOnly:
    """A read-only view of a Graph with retired nodes hidden. `goal:s23`.

    A view rather than `Graph.remove_node`, because `g` is still needed whole
    a few lines below -- `by_type` counts and `find_chains` both read it, and
    mutating it here would silently change what the map REPORTS as well as
    what it draws. `build_representation` touches exactly three members, so
    the view is three members wide.
    """

    def __init__(self, graph, hidden: frozenset):
        self._g, self._hidden = graph, hidden

    @property
    def node_ids(self):
        return self._g.node_ids - self._hidden

    @property
    def edges(self):
        return (e for e in self._g.edges
                if e.source_id not in self._hidden and e.target_id not in self._hidden)

    def get_node(self, node_id):
        return None if node_id in self._hidden else self._g.get_node(node_id)


def _load_graph_sqlite(nodes_dir: Path) -> tuple[Graph, list]:
    """Load graph via SQLiteBackend if persistence.type=sqlite, else None."""
    cfg_path = config_path(PROJECT_ROOT)
    if cfg_path is None:
        return None, []
    import json
    cfg = json.loads(cfg_path.read_text())
    if cfg.get("persistence", {}).get("type") != "sqlite":
        return None, []
    db_path = PROJECT_ROOT / cfg["persistence"]["path"]
    from graph_core.persistence.sqlite_backend import SQLiteBackend
    from graph_core.db_loader import DBLoader
    return DBLoader(SQLiteBackend(db_path)).load_directory()



def main() -> int:
    nodes_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT_ROOT / "nodes"
    if not nodes_dir.is_dir():
        print(f"ERR: nodes dir not found: {nodes_dir}", file=sys.stderr)
        return 1

    # Try SQLite first if configured, fall back to filesystem
    g, loaded = None, []
    sq_g, sq_loaded = _load_graph_sqlite(nodes_dir)
    if sq_g is not None:
        g, loaded = sq_g, sq_loaded
        print(f"loaded {len(loaded)} nodes from SQLite (persistence.type=sqlite)")
    else:
        g, loaded = load_directory(nodes_dir)
        print(f"loaded {len(loaded)} nodes from {nodes_dir}")

    # Wire parent/child edges from frontmatter; also populate child sets so
    # chain-walking (longest_chain_length, descendant counts) reflects the DAG.
    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                try:
                    g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
                except Exception:
                    pass
                parent_node = g.get_node(parent_id)
                if parent_node is not None:
                    parent_node.children.add(ln.node.id)

    # goal:s23 — LOAD retired nodes, do not RENDER them. The two are different
    # operations and collapsing either way breaks something real:
    #   * loading must keep them — `stitch.py`, `level3.py`, `node_writer.py`
    #     and `zoom.py` read `nodes/deprecated/` deliberately, and a reader
    #     that stops seeing a retired node fails quietly and in its own way
    #     (orphaned engine file, re-minted duplicate, unresolvable edge).
    #   * injecting them must stop — context is the scarcest thing an agent
    #     has, and a retired node in the map is weight every agent carries for
    #     the rest of the project's life to describe work deliberately not
    #     being done.
    # Measured before the fix: `build:TODO.md` was deprecated AND moved to
    # `.agi/nodes/deprecated/` and still sat at INJECTION.md line 85.
    # This is also why no new `legacy` status was minted — `deprecated` already
    # meant exactly this; only the renderer had never honoured it.
    retired = metrics_mod.deprecated_node_ids(nodes_dir)
    rep = build_representation(_LiveOnly(g, retired) if retired else g)
    ascii_out = render_ascii(rep)
    if retired:
        print(f"map: {len(retired)} retired node(s) loaded but not rendered (goal:s23)")
    lines = ascii_out.splitlines()
    print(f"ASCII rendering: {len(lines)} lines")
    if len(lines) > 200:
        print(f"WARN: exceeded 200 lines ({len(lines)})", file=sys.stderr)

    # Type counts
    by_type: dict[str, int] = defaultdict(int)
    for n in g.nodes:
        by_type[n.type] += 1

    # Chain stats: use find_chains() for chain-based longest path (via 'next' edges)
    # NOTE: find_chains reads next_edges from YAML frontmatter directly (loader does
    # not parse next_edges into g.edges). No post_wire call needed.
    if _HAS_CHAIN_ENGINE and find_chains is not None:
        chains = find_chains(g, graph_dir=str(nodes_dir))
        longest_len = max((len(c) for c in chains), default=0)
        chain_count = len(chains)
    else:
        chains = []
        longest_len = 0
        chain_count = 0

    # What the loop is actually scored on. Read from the project's config so
    # the map never advertises a target the project has not chosen; the
    # fallback is goal-attributable, never chain length (TODO.md H3).
    cfg = read_config(PROJECT_ROOT)
    primary = primary_metric_name(cfg)
    coverage = outcome_coverage(by_type.get("mvp", 0), by_type.get("hypothesis", 0))

    # Attractive chains: ideas sorted by descendant count
    idea_attract = []
    for n in g.nodes:
        if n.type == "idea":
            descendants = _count_descendants(g, n.id)
            idea_attract.append((n.id, descendants))
    idea_attract.sort(key=lambda x: -x[1])

    # Build INJECTION.md. Rules first, ASCII last — both injectors truncate at
    # 80 lines, and the rules are the part an agent must not miss.
    #
    # The nine briefing sections between the header and the ASCII view are
    # composed by `briefing.py` rather than written here (L1.04, 2026-09-03).
    # They used to be literal text in this list, which made this file the sole
    # owner of the chain rules and the verdict taxonomy -- so `viewport.py`
    # could not show an agent the same contract without restating it, and a
    # restated contract drifts. Extracted BEFORE this renderer is deleted, so
    # the deletion takes nothing with it.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import briefing as _briefing  # noqa: E402

    brief = _briefing.build(
        PROJECT_ROOT, g, loaded,
        descendants_fn=lambda nid: _count_descendants(g, nid),
        chain_stats=(chain_count, longest_len) if _HAS_CHAIN_ENGINE else None,
    )

    out_lines = [
        "# agi-tree INJECTION CONTEXT",
        f"_generated {brief.generated_at}_",
        "",
        *_briefing.to_markdown(brief),
    ]

    out_lines.extend([
        "",
        "## ASCII view (≤200 lines)",
        "```",
        ascii_out.rstrip(),
        "```",
        "",
    ])

    out_path = PROJECT_ROOT / "context" / "INJECTION.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote: {out_path}")
    return 0


def _count_descendants(g: Graph, root: str) -> int:
    """BFS descendants count."""
    seen = {root}
    stack = [root]
    while stack:
        cur = stack.pop()
        n = g.get_node(cur)
        if n is None:
            continue
        for c in n.children:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return len(seen) - 1  # exclude root itself


if __name__ == "__main__":
    sys.exit(main())
