"""T-010 tests: uniform renderer contract (graph-core/R5.3)."""

from pathlib import Path

from graph_core.graph import Graph
from graph_core.loader import load_node_with_subgraph
from graph_core.types import RenderableGraph


NESTED = Path(__file__).parent.parent / "fixtures" / "nested"


def _count_nodes(g: RenderableGraph) -> int:
    """Stub renderer: counts nodes via the protocol (no type discrimination)."""
    return len(list(g.nodes))


def test_top_level_graph_satisfies_protocol() -> None:
    g = Graph()
    assert isinstance(g, RenderableGraph)


def test_inner_subgraph_satisfies_protocol() -> None:
    ln = load_node_with_subgraph(NESTED / "top.md")
    assert ln.subgraph is not None
    assert isinstance(ln.subgraph, RenderableGraph)


def test_same_callable_works_on_both() -> None:
    """One stub callable accepts both outer and inner without branching."""
    outer = Graph()
    ln = load_node_with_subgraph(NESTED / "top.md")
    assert ln.subgraph is not None
    # Both work via the same protocol-typed function.
    _count_nodes(outer)
    _count_nodes(ln.subgraph)
