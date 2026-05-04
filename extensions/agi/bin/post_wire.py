#!/usr/bin/env python3
"""post_wire.py — wire agent results back into the node graph after an iteration.

After agents complete (or after heal.py finishes retrying), this script:
1. Reads all agent.json records from the iteration session dir
2. For each agent that returned a verdict:
   - Updates the target node's frontmatter with verdict + confidence
   - Appends the next_edge suggestion to the parent's next_edges list
   - Creates a verdict node if one doesn't already exist for this experiment
3. Emits a wiring report (nodes updated, edges added, conflicts)

Usage:
    post_wire.py <project_root> <iter_n>
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SRC_GRAPH = PLUGIN_ROOT / "src" / "graph_core"


def _find_root(cwd: Path | None = None) -> Path:
    d = (cwd or Path.cwd()).resolve()
    while d != d.parent:
        if (d / "autoresearch-tree.config.json").exists():
            return d
        d = d.parent
    raise SystemExit("ERR: no autoresearch-tree.config.json found")


def _load_graph_core():
    """Ensure graph_core is on sys.path."""
    import sys as _sys
    plugin_root = Path(__file__).resolve().parent.parent
    proj_src = Path(_find_root()) / "src"
    if (proj_src / "graph_core").is_dir():
        _sys.path.insert(0, str(proj_src))
    _sys.path.insert(0, str(plugin_root / "src"))
    from graph_core.loader import load_directory
    from graph_core.edge import Edge
    from graph_core.node import Node
    return load_directory, Edge, Node


def _slug_from_node_id(node_id: str) -> str:
    """Extract slug (everything after the type: prefix)."""
    if ":" in node_id:
        return node_id.split(":", 1)[1]
    return node_id


def _node_file_path(root: Path, node_id: str) -> Path | None:
    """Find the .md file for a node_id."""
    if ":" not in node_id:
        return None
    ntype, slug = node_id.split(":", 1)
    type_dir = ntype.replace("-", "_")
    candidates = [
        root / "nodes" / type_dir / f"{slug}.md",
        root / "nodes" / ntype / f"{slug}.md",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def _read_frontmatter(body: str) -> tuple[dict, str]:
    """Split YAML frontmatter (between --- markers) from body."""
    if "---\n" not in body and "---\r\n" not in body:
        return {}, body
    parts = body.split("---", 2)
    if len(parts) < 3:
        return {}, body
    import yaml
    fm = yaml.safe_load(parts[1]) or {}
    return fm, parts[2]


def _write_node(path: Path, fm: dict, body: str) -> None:
    """Write frontmatter + body back to a node file."""
    import yaml
    fm_lines = yaml.dump(dict(fm), default_flow_style=False).splitlines()
    content = "---\n" + "\n".join(fm_lines) + "\n---\n" + body
    path.write_text(content, encoding="utf-8")


def cmd_wire(args: argparse.Namespace) -> int:
    root = _find_root()
    iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
    manifest_path = iter_dir / "manifest.json"

    if not manifest_path.exists():
        print(f"WARN: no manifest at {manifest_path}, nothing to wire", file=sys.stderr)
        return 0

    manifest = json.loads(manifest_path.read_text())
    load_directory, Edge, Node = _load_graph_core()

    # Build current graph
    g, loaded = load_directory(root / "nodes")
    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                try:
                    g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
                except Exception:
                    pass
                pn = g.get_node(parent_id)
                if pn is not None:
                    pn.children.add(ln.node.id)

    updated_nodes: list[str] = []
    added_edges: list[str] = []
    skipped: list[str] = []

    for agent in manifest.get("agents", []):
        if agent.get("status") != "done":
            continue
        verdict = agent.get("verdict")
        confidence = agent.get("confidence", 0.5)
        node_id = agent.get("node_id")
        parent = agent.get("parent", "")
        notes = agent.get("notes", "")
        strategy = agent.get("strategy", "unknown")

        if not node_id:
            skipped.append(f"{agent['id']}: no node_id")
            continue

        # 1. Update the node file with verdict
        node_path = _node_file_path(root, node_id)
        if node_path and node_path.exists():
            content = node_path.read_text(encoding="utf-8")
            fm, body = _read_frontmatter(content)
            fm["verdict"] = verdict
            fm["confidence"] = confidence
            fm["wired_at"] = int(time.time())
            fm["wired_from"] = agent["id"]
            if notes:
                body = body.rstrip() + f"\n\n## Agent Notes\n{notes}\n"
            _write_node(node_path, fm, body)
            updated_nodes.append(node_id)
        else:
            # No file yet — create a minimal verdict node
            verdict_dir = root / "nodes" / "verdict"
            verdict_dir.mkdir(parents=True, exist_ok=True)
            slug = _slug_from_node_id(node_id)
            vpath = verdict_dir / f"{slug}.md"
            import yaml
            fm = {
                "id": f"verdict:{agent['id']}",
                "type": "verdict",
                "verdict": verdict,
                "confidence": confidence,
                "parents": [node_id],
                "next_edges": [],
                "wired_from": agent["id"],
                "wired_at": int(time.time()),
            }
            vpath.write_text(
                "---\n"
                + yaml.dump(fm, default_flow_style=False)
                + "---\n\n"
                + (notes or ""),
                encoding="utf-8",
            )
            updated_nodes.append(f"verdict:{agent['id']}")

        # 2. Update parent's next_edges if parent exists
        if parent:
            parent_path = _node_file_path(root, parent)
            if parent_path and parent_path.exists():
                pcontent = parent_path.read_text(encoding="utf-8")
                pfm, pbody = _read_frontmatter(pcontent)
                next_edges = pfm.get("next_edges", [])
                if isinstance(next_edges, list):
                    # Must be plain node ID string for find_chains() compatibility
                    if node_id not in next_edges:
                        next_edges.append(node_id)
                        pfm["next_edges"] = next_edges
                        _write_node(parent_path, pfm, pbody)
                        added_edges.append(f"{parent} -> {node_id} [{strategy}]")
                        # Also update graph in memory for downstream use
                        if g.has_node(parent) and g.has_node(node_id):
                            try:
                                g.add_edge(
                                    Edge(
                                        source_id=parent,
                                        target_id=node_id,
                                        relation="next",
                                    )
                                )
                            except Exception:
                                pass

    # 3. Persist updated graph back (so subsequent iterations see wired edges)
    #    We write a .graph.json snapshot alongside the manifest
    graph_path = iter_dir / f"iter-{args.iter_n:03d}-graph.json"
    graph_data = {
        "nodes": [
            {
                "id": n.id,
                "type": n.type,
                "parents": list(n.parents),
                "children": list(n.children),
                "tags": list(n.tags),
            }
            for n in g.nodes
        ],
        "edges": [
            {"source": e.source_id, "target": e.target_id, "relation": e.relation}
            for e in g.edges
        ],
    }
    graph_path.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")

    # 4. Emit wiring report
    print(f"[post_wire] iter={args.iter_n}")
    print(f"  nodes updated: {len(updated_nodes)}")
    for n in updated_nodes:
        print(f"    - {n}")
    print(f"  edges added: {len(added_edges)}")
    for e in added_edges:
        print(f"    - {e}")
    if skipped:
        print(f"  skipped: {len(skipped)}")
        for s in skipped:
            print(f"    - {s}")
    print(f"  graph snapshot: {graph_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Wire agent verdicts back into the node graph.")
    ap.add_argument("project_root", nargs="?")
    ap.add_argument("iter_n", type=int)
    args = ap.parse_args()

    if args.project_root:
        import os
        os.chdir(args.project_root)

    return cmd_wire(args)


if __name__ == "__main__":
    sys.exit(main())
