"""Structured exceptions for graph-core (T-002 / graph-core R1.3 + R2)."""

from __future__ import annotations


class GraphCoreError(Exception):
    """Base for all graph-core exceptions."""


class SelfLoopError(GraphCoreError):
    """Raised when a node id is added to its own parents/children set."""

    def __init__(self, node_id: str, side: str) -> None:
        self.node_id = node_id
        self.side = side  # "parents" | "children"
        super().__init__(
            f"self-loop rejected: cannot add node id '{node_id}' to its own {side}"
        )


class CycleError(GraphCoreError):
    """Raised when adding an edge would create a directed cycle (T-004)."""

    def __init__(self, source_id: str, target_id: str, path: list[str]) -> None:
        self.source_id = source_id
        self.target_id = target_id
        self.path = path
        super().__init__(
            f"cycle rejected: edge {source_id} -> {target_id} closes path {' -> '.join(path)}"
        )


# Re-export FrontmatterError from persistence so callers can `from graph_core.errors import FrontmatterError`
def _frontmatter_error_proxy():
    from .persistence.frontmatter import FrontmatterError
    return FrontmatterError
