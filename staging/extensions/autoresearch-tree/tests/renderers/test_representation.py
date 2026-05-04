"""T-060 tests: shared representation (renderers/R1)."""

from dataclasses import fields

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from renderers import RenderToken, Representation, build_representation


def _make_chain_graph(ids: list[str]) -> Graph:
    g = Graph()
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))
    return g


def test_render_token_field_surface_seven() -> None:
    """R1.1: RenderToken exposes id, label, type, depth, x, y, edges."""
    declared = {f.name for f in fields(RenderToken)}
    assert declared == {"id", "label", "type", "depth", "x", "y", "edges"}


def test_build_is_deterministic() -> None:
    """R1.2: same graph twice → same token sequence (id-by-id)."""
    g = _make_chain_graph(["a", "b", "c", "d"])
    r1 = build_representation(g)
    r2 = build_representation(g)
    assert [t.id for t in r1.tokens] == [t.id for t in r2.tokens]
    for t1, t2 in zip(r1.tokens, r2.tokens):
        assert t1 == t2


def test_depth_is_bfs_from_roots() -> None:
    """Depth assignment is BFS from in-degree-0 nodes."""
    g = _make_chain_graph(["a", "b", "c"])
    r = build_representation(g)
    by_id = r.by_id()
    assert by_id["a"].depth == 0
    assert by_id["b"].depth == 1
    assert by_id["c"].depth == 2


def test_default_xy_zero_for_embeddings_overwrite() -> None:
    """R1.4 contract: x, y default to 0.0; embeddings will overwrite."""
    g = _make_chain_graph(["a", "b"])
    r = build_representation(g)
    for t in r.tokens:
        assert t.x == 0.0
        assert t.y == 0.0


def test_edges_in_token_match_graph_edges() -> None:
    """Edges field carries (target_id, relation) tuples."""
    g = _make_chain_graph(["a", "b", "c"])
    r = build_representation(g)
    by_id = r.by_id()
    assert by_id["a"].edges == [("b", "next")]
    assert by_id["b"].edges == [("c", "next")]
    assert by_id["c"].edges == []


def test_label_truncated_at_40_chars() -> None:
    """label_fn output is capped at 40 chars (label-as-id-rendering target)."""
    g = Graph()
    long_label = "x" * 60
    g.add_node(Node(id="hyp:long", type="hypothesis"))
    r = build_representation(g, label_fn=lambda n: long_label)
    assert len(r.tokens[0].label) == 40


def test_tokens_sorted_by_id() -> None:
    """R1.2: emission order is sorted by id."""
    g = Graph()
    for nid in ["zeta", "alpha", "mu"]:
        g.add_node(Node(id=nid, type="x"))
    r = build_representation(g)
    assert [t.id for t in r.tokens] == ["alpha", "mu", "zeta"]


def test_empty_graph_yields_empty_representation() -> None:
    g = Graph()
    r = build_representation(g)
    assert len(r) == 0
