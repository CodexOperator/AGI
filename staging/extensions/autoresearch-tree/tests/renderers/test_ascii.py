"""T-061 tests: ASCII renderer (renderers/R2)."""

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from renderers import build_representation, render_ascii
from renderers.ascii import MAX_COLS, MAX_LINES


def _chain(ids: list[str]) -> Graph:
    g = Graph()
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))
    return g


def test_bounded_200_lines() -> None:
    """R2.1 + R2.2: a 1000-node fixture rendered must produce <= 200 lines with a truncation marker."""
    g = _chain([f"n{i:04d}" for i in range(1000)])
    rep = build_representation(g)
    out = render_ascii(rep)
    lines = out.splitlines()
    assert len(lines) <= MAX_LINES
    assert any("truncated" in line for line in lines)


def test_bounded_200_cols() -> None:
    """R2.1: no line exceeds 200 columns."""
    g = Graph()
    long_id = "x" * 300
    g.add_node(Node(id=long_id, type="x"))
    rep = build_representation(g)
    out = render_ascii(rep)
    for line in out.splitlines():
        assert len(line) <= MAX_COLS


def test_byte_equal_across_runs() -> None:
    """R2.4: two runs over same graph → byte-equal output."""
    g = _chain([f"n{i}" for i in range(20)])
    rep = build_representation(g)
    a = render_ascii(rep)
    b = render_ascii(rep)
    assert a == b


def test_summary_header_present() -> None:
    g = _chain(["a", "b"])
    rep = build_representation(g)
    out = render_ascii(rep)
    lines = out.splitlines()
    assert lines[0].startswith("# graph: 2 nodes")
    assert "types:" in lines[1]


def test_empty_graph_renders_header_only() -> None:
    g = Graph()
    rep = build_representation(g)
    out = render_ascii(rep)
    lines = out.splitlines()
    assert "0 nodes" in lines[0]
    assert len(lines) <= 5  # header lines only


def test_indent_reflects_depth() -> None:
    g = _chain(["a", "b", "c"])
    rep = build_representation(g)
    out = render_ascii(rep)
    # Find lines containing each id
    a_line = next(l for l in out.splitlines() if "a ::" in l)
    b_line = next(l for l in out.splitlines() if "b ::" in l)
    c_line = next(l for l in out.splitlines() if "c ::" in l)
    # Higher depth → more leading spaces
    assert len(a_line) - len(a_line.lstrip()) == 0
    assert len(b_line) - len(b_line.lstrip()) == 2
    assert len(c_line) - len(c_line.lstrip()) == 4
