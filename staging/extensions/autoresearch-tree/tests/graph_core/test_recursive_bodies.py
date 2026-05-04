"""T-009 tests: recursive node bodies (graph-core/R5)."""

from pathlib import Path

from graph_core.loader import load_node_with_subgraph, load_directory

NESTED = Path(__file__).parent.parent / "fixtures" / "nested"


def test_subgraph_true_loads_inner_graph() -> None:
    """R5.1: subgraph: true treats body as graph using same loader."""
    ln = load_node_with_subgraph(NESTED / "top.md")
    assert ln.subgraph is not None
    assert "t:alpha" in ln.subgraph
    assert "t:beta" in ln.subgraph
    assert "t:gamma" in ln.subgraph


def test_three_levels_of_nesting() -> None:
    """R5.2: ≥3 levels of nesting loadable via load_directory."""
    g, loaded = load_directory(NESTED)
    # We expect to load top.md + outer.md + middle.md + leaf.md = 4 files.
    assert len(loaded) >= 4
    ids = {ln.node.id for ln in loaded}
    assert {"top", "outer-a", "middle-b", "leaf-c"}.issubset(ids)


def test_leaf_has_no_subgraph() -> None:
    """A leaf without subgraph: true exposes no subgraph."""
    ln = load_node_with_subgraph(NESTED / "level_a" / "level_b" / "level_c" / "leaf.md")
    assert ln.subgraph is None


def test_outer_query_independent_of_inner() -> None:
    """R5.4: outer parent queries continue to work; inner is opaque from outside."""
    g, loaded = load_directory(NESTED)
    top = g.get_node("top")
    assert top is not None
    # The inner subgraph is NOT a child of top in the outer graph.
    assert "t:alpha" not in top.children
    # Inner subgraph is reachable via the LoadedNode handle.
    top_loaded = next(ln for ln in loaded if ln.node.id == "top")
    assert "t:alpha" in top_loaded.subgraph
