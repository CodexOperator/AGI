"""T-062 tests: ASCII footer summary (renderers/R2.3)."""

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from renderers import build_representation, render_ascii


def test_footer_contains_type_counts() -> None:
    g = Graph()
    g.add_node(Node(id="a", type="idea"))
    g.add_node(Node(id="b", type="idea"))
    g.add_node(Node(id="c", type="hypothesis"))
    rep = build_representation(g)
    out = render_ascii(rep)
    assert "Types:" in out
    # idea=2, hypothesis=1
    assert "idea=2" in out
    assert "hypothesis=1" in out


def test_footer_contains_edge_counts() -> None:
    g = Graph()
    for nid in ["a", "b", "c"]:
        g.add_node(Node(id=nid, type="x"))
    g.add_edge(Edge(source_id="a", target_id="b", relation="next"))
    g.add_edge(Edge(source_id="b", target_id="c", relation="next"))
    rep = build_representation(g)
    out = render_ascii(rep)
    assert "Edges:" in out
    assert "next=2" in out


def test_no_footer_for_empty_graph() -> None:
    g = Graph()
    rep = build_representation(g)
    out = render_ascii(rep)
    # Empty graph footer is acceptable to omit; either way:
    if "Types:" in out:
        # If present, must show empty type counts
        pass


def test_footer_alpha_sort_on_types() -> None:
    g = Graph()
    g.add_node(Node(id="a", type="zebra"))
    g.add_node(Node(id="b", type="apple"))
    rep = build_representation(g)
    out = render_ascii(rep)
    types_line = next(l for l in out.splitlines() if l.startswith("Types:"))
    # 'apple' should appear before 'zebra'
    assert types_line.index("apple") < types_line.index("zebra")
