"""Type aliases and protocols for graph-core (T-010 / R5.3).

A `RenderableGraph` is anything that quacks like the `Graph` class:
exposes `nodes`, `node_ids`, `edges`, `get_node`, `has_node`. Both
the top-level Graph and nested subgraphs (loaded via T-009) satisfy
this protocol — renderers must be callable on either.
"""

from __future__ import annotations

from typing import Iterator, Protocol, runtime_checkable

from .edge import Edge
from .node import Node


@runtime_checkable
class RenderableGraph(Protocol):
    """Protocol satisfied by Graph (top-level) and any inner subgraph."""

    @property
    def nodes(self) -> Iterator[Node]: ...

    @property
    def node_ids(self) -> set[str]: ...

    @property
    def edges(self) -> Iterator[Edge]: ...

    def get_node(self, node_id: str) -> Node | None: ...

    def has_node(self, node_id: str) -> bool: ...
