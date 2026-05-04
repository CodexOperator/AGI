#!/usr/bin/env python3
"""render-context.py — load a nodes dir, render to ASCII, write INJECTION_FILE.

Output: `context/INJECTION.md` containing:
- ASCII rendering (≤200 lines)
- chain-stat summary
- top-N attractive chains
- big-vs-small idea pool

Usage:
    python3 bin/render-context.py [nodes_dir]
    (default nodes_dir = ./nodes)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(
    os.environ.get("AUTORESEARCH_TREE_PROJECT_ROOT")
    or os.environ.get("PROJECT_ROOT")
    or os.getcwd()
).resolve()
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
from renderers import build_representation, render_ascii

# Detect sqlite config for optional DB-backed loading
def _load_graph_sqlite(nodes_dir: Path) -> tuple[Graph, list]:
    """Load graph via SQLiteBackend if persistence.type=sqlite, else None."""
    cfg_path = PROJECT_ROOT / "autoresearch-tree.config.json"
    if not cfg_path.exists():
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

    rep = build_representation(g)
    ascii_out = render_ascii(rep)
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
    
    # Also compute spawns-based longest chain for comparison
    spawns_longest = _longest_chain_length(g)

    # Attractive chains: ideas sorted by descendant count
    idea_attract = []
    for n in g.nodes:
        if n.type == "idea":
            descendants = _count_descendants(g, n.id)
            idea_attract.append((n.id, descendants))
    idea_attract.sort(key=lambda x: -x[1])

    # Build INJECTION.md
    out_lines = [
        "# autoresearch-tree INJECTION CONTEXT",
        f"_generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}_",
        "",
        "## graph snapshot",
        f"- nodes: {len(g)}",
        f"- edges: {g.edge_count}",
        "- by type: " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())),
        f"- longest chain: {longest_len} hops (via next edges)",
        f"- chain count: {chain_count}",
        "",
        "## attractive ideas (descendant count, top 10)",
    ]
    for nid, count in idea_attract[:10]:
        out_lines.append(f"- {nid} :: {count} descendants")

    out_lines.extend([
        "",
        "## ASCII view (≤200 lines)",
        "```",
        ascii_out.rstrip(),
        "```",
        "",
        "## big-vs-small decision",
        "Each iteration MUST first answer: **explore a big idea or small idea?**",
        "- big = fresh chain, broad concept (default 30%)",
        "- small = extend existing chain mid-way (default 70%)",
        "",
        "## verdict taxonomy",
        "`proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending`",
        "",
        "## chain rules",
        "- longest-chain attracts but mid-chain join allowed",
        "- forks welcome — same idea may spawn multiple hypotheses",
        "- new ideas spawn from any node type (idea/hypothesis/experiment/verdict)",
        "",
        "## next-step suggestions",
    ])
    # Suggest pending tasks of small effort first
    pending = []
    for ln in loaded:
        if ln.node.type == "task" and "tier-" in " ".join(ln.node.tags):
            pending.append(ln.node.id)
    out_lines.append(f"- pending tasks: {len(pending)} (see nodes/task/)")
    out_lines.append("")

    out_path = PROJECT_ROOT / "context" / "INJECTION.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote: {out_path}")
    return 0


def _longest_chain_length(g: Graph) -> int:
    """DFS longest path via next_edges (verdict→experiment→verdict cycles).
    
    Fixed in iter30: previously walked n.children (spawns edges) which gave
    depth=0 because ideas→hypotheses→tasks forms a shallow tree.
    Chains are built on next_edges, which produce ~200-hop chains.
    """
    # Build next_edges adjacency from all nodes that have it
    next_adj: dict[str, list[str]] = {}
    for n in g.nodes:
        if hasattr(n, 'next_edges') and n.next_edges:
            next_adj[n.id] = n.next_edges

    cache: dict[str, int] = {}

    def depth(nid: str) -> int:
        if nid in cache:
            return cache[nid]
        if nid not in next_adj or not next_adj[nid]:
            cache[nid] = 0
            return 0
        best = 0
        for c in next_adj[nid]:
            if c == nid:
                continue
            best = max(best, depth(c) + 1)
        cache[nid] = best
        return best

    if not next_adj:
        return 0
    return max(depth(nid) for nid in next_adj)


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
