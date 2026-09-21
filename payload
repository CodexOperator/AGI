"""SQLite-backed graph loader (T-011 / R6 alternative path).

Mirrors loader.py's logic but reads from a SQLiteBackend instead of
filesystem node files.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

from .edge import Edge
from .graph import Graph
from .identity import IdRegistry, mint_id
from .node import Node
from .persistence.sqlite_backend import SQLiteBackend


@dataclass
class LoadedNode:
    """Container for a loaded node + optional subgraph (mirrors loader.LoadedNode)."""

    node: Node
    body: str
    subgraph: Optional["Graph"] = None
    nested_loaded: list["LoadedNode"] = field(default_factory=list)


_SUBGRAPH_LINE_RE = re.compile(
    r"^\s*-\s+(?P<src>[^\s>]+)(?:\s*->\s*(?P<dst>[^\s]+))?(?:\s*\[(?P<rel>[^\]]+)\])?\s*$"
)


def _node_from_frontmatter(
    fm: dict,
    source_path: Path,
    registry: Optional[IdRegistry],
) -> Node:
    """Build a Node from a frontmatter dict (DB-loaded variant)."""
    nid = fm.get("id")
    if not isinstance(nid, str) or not nid:
        nid = mint_id(
            type_prefix=str(fm.get("type", "node")),
            source_text=str(fm.get("title") or source_path.stem),
            registry=registry,
        )
    type_str = str(fm.get("type", "node"))
    parents = set(fm.get("parents", []) or [])
    children = set(fm.get("children", []) or [])
    tags = set(fm.get("tags", []) or [])
    payload_ref = fm.get("payload_ref")
    origin = fm.get("origin")
    if not isinstance(origin, str):
        origin = None
    return Node(
        id=nid,
        type=type_str,
        payload_ref=payload_ref if isinstance(payload_ref, str) else None,
        parents=parents,
        children=children,
        tags=tags,
        origin=origin,
    )


def _split_type(node_id: str) -> str:
    if ":" in node_id:
        return node_id.split(":", 1)[0]
    return "node"


def _parse_subgraph_body(
    body: str,
    parent_id: str,
    registry: Optional[IdRegistry],
) -> tuple[Graph, list[LoadedNode]]:
    """Parse subgraph lines from body content (same logic as loader.py)."""
    g = Graph()
    nested: list[LoadedNode] = []
    for raw in body.splitlines():
        m = _SUBGRAPH_LINE_RE.match(raw)
        if not m:
            continue
        src = m.group("src").strip()
        dst = m.group("dst")
        rel = m.group("rel") or "next"
        if not g.has_node(src):
            g.add_node(Node(id=src, type=_split_type(src)))
        if dst:
            dst = dst.strip()
            if not g.has_node(dst):
                g.add_node(Node(id=dst, type=_split_type(dst)))
            try:
                g.add_edge(Edge(source_id=src, target_id=dst, relation=rel.strip()))
            except Exception:
                # Cycles in inner subgraph: skip the offending edge silently.
                pass
    return g, nested


class DBLoader:
    """Loads graph data from a SQLiteBackend.

    Usage:
        backend = SQLiteBackend("nodes.db")
        loader = DBLoader(backend)
        graph, loaded_nodes = loader.load_directory()

    The loader reconstructs Node objects from the DB-backed NodeFile format
    and assembles them into a Graph.
    """

    def __init__(self, backend: SQLiteBackend) -> None:
        self._backend = backend

    def load_node(self, node_id: str) -> LoadedNode:
        """Load a single node from the DB."""
        nf = self._backend.load(node_id)
        node = _node_from_frontmatter(nf.frontmatter, source_path=Path(node_id), registry=None)
        body = nf.body
        if not nf.frontmatter.get("subgraph", False):
            return LoadedNode(node=node, body=body, subgraph=None, nested_loaded=[])
        inner_graph, nested = _parse_subgraph_body(body, parent_id=node.id, registry=None)
        return LoadedNode(node=node, body=body, subgraph=inner_graph, nested_loaded=nested)

    def load_directory(self) -> tuple[Graph, list[LoadedNode]]:
        """Load all nodes from the DB into a Graph.

        Returns (graph, list_of_loaded_nodes) — same contract as loader.load_directory().
        """
        g = Graph()
        loaded: list[LoadedNode] = []
        for node_path in self._backend.list(""):
            node_id = node_path.name if node_path.name else str(node_path)
            try:
                ln = self.load_node(node_id)
            except Exception:
                continue
            if not g.has_node(ln.node.id):
                g.add_node(ln.node)
                loaded.append(ln)
        return g, loaded

    def save_graph(self, g: Graph, loaded_nodes: Iterable[LoadedNode]) -> None:
        """Persist a Graph and its loaded nodes to the DB.

        Saves all nodes (from loaded_nodes) and then all edges from the Graph.
        """
        from .persistence.frontmatter import NodeFile

        # Save nodes
        for ln in loaded_nodes:
            fm = {
                "id": ln.node.id,
                "type": ln.node.type,
                "payload_ref": ln.node.payload_ref,
                "parents": list(ln.node.parents),
                "children": list(ln.node.children),
                "tags": list(ln.node.tags),
                "origin": ln.node.origin,
                "body": ln.body,
            }
            nf = NodeFile(frontmatter=fm, body=ln.body, suffix=".json")
            self._backend.save(ln.node.id, nf)

        # Save edges
        self._backend.clear_edges()
        for edge in g.edges:
            self._backend.save_edge(
                edge.source_id, edge.target_id, edge.relation, edge.tags
            )
