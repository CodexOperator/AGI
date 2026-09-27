"""Graph container — implements graph-core/R2 (T-004).

Acceptance criteria (R2):
- R2.1: cycle insert returns structured error and leaves graph unchanged
- R2.4: removing node removes all incident edges (no dangling refs)

Cycle detection: DFS from edge target back to source.
Atomic add_edge: rollback if cycle would close.
"""

from __future__ import annotations

from typing import Iterator, Optional

from .edge import Edge
from .errors import CycleError, GraphCoreError
from .node import Node


class GraphError(GraphCoreError):
    """Raised for graph-level errors not covered by more specific subclasses."""


class Graph:
    """In-memory DAG container. Nodes by id, edges as a set."""

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: set[Edge] = set()
        # Adjacency for fast cycle DFS: source_id -> set of target_ids
        self._out: dict[str, set[str]] = {}

    # ---------- Nodes ----------

    def add_node(self, node: Node) -> None:
        """Insert a node. Re-insert with same id is a no-op (idempotent)."""
        if node.id in self._nodes:
            # Idempotent — same id is treated as already-present.
            return
        self._nodes[node.id] = node
        self._out.setdefault(node.id, set())

    def get_node(self, node_id: str) -> Optional[Node]:
        return self._nodes.get(node_id)

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    def remove_node(self, node_id: str) -> int:
        """Remove a node and ALL incident edges. Returns count of edges dropped (R2.4)."""
        if node_id not in self._nodes:
            return 0
        # Collect incident edges (incoming + outgoing).
        incident = {
            e for e in self._edges if e.source_id == node_id or e.target_id == node_id
        }
        for e in incident:
            self._edges.discard(e)
            self._out.get(e.source_id, set()).discard(e.target_id)
        del self._nodes[node_id]
        self._out.pop(node_id, None)
        # Also strip the id from any other node's _out adjacency that points TO it.
        for src, targets in self._out.items():
            targets.discard(node_id)
        return len(incident)

    @property
    def nodes(self) -> Iterator[Node]:
        return iter(self._nodes.values())

    @property
    def node_ids(self) -> set[str]:
        return set(self._nodes.keys())

    # ---------- Edges ----------

    def add_edge(self, edge: Edge) -> None:
        """Add an edge. Raises :class:`CycleError` if it would close a directed cycle (R2.1).

        Atomic: on cycle detection, the graph is unchanged.
        """
        if edge.source_id not in self._nodes:
            raise GraphError(f"edge source not in graph: {edge.source_id}")
        if edge.target_id not in self._nodes:
            raise GraphError(f"edge target not in graph: {edge.target_id}")
        if edge in self._edges:
            return  # idempotent (R2.3)
        # Cycle check BEFORE mutating.
        path = self._cycle_path(edge.source_id, edge.target_id)
        if path is not None:
            raise CycleError(edge.source_id, edge.target_id, path)
        self._edges.add(edge)
        self._out.setdefault(edge.source_id, set()).add(edge.target_id)

    def remove_edge(self, edge: Edge) -> bool:
        """Remove an edge. Returns True if removed, False if absent."""
        if edge not in self._edges:
            return False
        self._edges.discard(edge)
        # _out may still have the (source -> target) pair from another edge with a different
        # relation; only remove the adjacency if no remaining edges connect them.
        still_connected = any(
            e.source_id == edge.source_id and e.target_id == edge.target_id
            for e in self._edges
        )
        if not still_connected:
            self._out.get(edge.source_id, set()).discard(edge.target_id)
        return True

    @property
    def edges(self) -> Iterator[Edge]:
        return iter(self._edges)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    # ---------- Internal: cycle detection ----------

    def _cycle_path(self, source: str, target: str) -> Optional[list[str]]:
        """Return path target -> ... -> source if adding source->target would close a cycle.

        DFS from `target` following outgoing edges. If we reach `source`, the new edge
        source->target would create a cycle (the path target ... source plus the new edge).
        """
        if source == target:
            return [source]
        stack: list[tuple[str, list[str]]] = [(target, [target])]
        seen: set[str] = set()
        while stack:
            current, path = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            for nxt in self._out.get(current, set()):
                if nxt == source:
                    return path + [source]
                stack.append((nxt, path + [nxt]))
        return None

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, node_id: object) -> bool:
        return isinstance(node_id, str) and node_id in self._nodes
