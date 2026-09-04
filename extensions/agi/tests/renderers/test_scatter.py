"""Tests: scatter renderer (renderers/scatter.py).

Tests cover:
- Determinism: two runs → byte-equal output
- Overlap: multiple nodes at same cell show digit or '@'
- Bounds: grid dimensions clamped to ≤200
- Empty graph outputs a sensible string
- Degenerate (all coords zero) does not crash
"""

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from renderers import build_representation, render_scatter
from renderers.scatter import MAX_GRID_H, MAX_GRID_W, OVERLAP_10PLUS, DEFAULT_GRID_W, DEFAULT_GRID_H


def _graph_with_coords(xy_pairs: dict[str, tuple[float, float]]) -> Graph:
    """Build a Graph and a Representation where tokens have (x, y) populated."""
    g = Graph()
    for nid, (_x, _y) in xy_pairs.items():
        g.add_node(Node(id=nid, type="test"))
    rep = build_representation(g)
    for t in rep.tokens:
        x, y = xy_pairs[t.id]
        t.x = x
        t.y = y
    return rep


def test_deterministic() -> None:
    """Two runs over same representation → byte-equal output."""
    rep = _graph_with_coords({
        "a": (0.0, 0.0),
        "b": (0.5, 0.5),
        "c": (1.0, 0.2),
        "d": (0.3, 0.8),
        "e": (0.9, 0.1),
    })
    a = render_scatter(rep)
    b = render_scatter(rep)
    assert a == b


def test_no_overlap_default_coords() -> None:
    """All coords at (0,0) — degenerate: all nodes map to same cell."""
    rep = _graph_with_coords({"a": (0.0, 0.0), "b": (0.0, 0.0), "c": (0.0, 0.0)})
    out = render_scatter(rep)
    # Should not crash; overlap marker expected
    assert "3" in out or OVERLAP_10PLUS in out
    assert "Overlap" in out


def test_overlap_two_nodes() -> None:
    """Two nodes at same coord → digit '2' at that cell."""
    rep = _graph_with_coords({"a": (0.0, 0.0), "b": (0.0, 0.0)})
    out = render_scatter(rep)
    assert "2" in out  # overlap count
    # The box borders exist
    assert "┌" in out
    assert "└" in out


def test_overlap_10plus() -> None:
    """Ten nodes at same cell → OVERLAP_10PLUS marker."""
    coords = {f"n{i}": (0.0, 0.0) for i in range(11)}
    rep = _graph_with_coords(coords)
    out = render_scatter(rep)
    assert OVERLAP_10PLUS in out


def test_bounds_200_max() -> None:
    """Grid dimensions clamped to MAX_GRID_W × MAX_GRID_H."""
    rep = _graph_with_coords({"a": (0.0, 0.0), "b": (1.0, 1.0)})
    out = render_scatter(rep, grid_width=500, grid_height=500)
    lines = out.splitlines()
    # Top border line has width + 2 (box chars)
    top = lines[0]
    assert len(top) <= MAX_GRID_W + 2  # +2 for ┌┐
    # The footer should say Grid: 200×200
    footer_line = [l for l in lines if "Grid:" in l]
    assert footer_line
    assert "200×200" in footer_line[0]


def test_empty_graph() -> None:
    """Empty representation → sensible output, not crash."""
    g = Graph()
    rep = build_representation(g)
    out = render_scatter(rep)
    assert "empty" in out


def test_single_node() -> None:
    """Single node renders a cell with its label initial."""
    rep = _graph_with_coords({"alpha": (0.5, 0.5)})
    out = render_scatter(rep)
    assert "a" in out  # first char of id
    assert "Nodes: 1" in out


def test_custom_grid_size() -> None:
    """Custom grid dimensions are respected (within max)."""
    rep = _graph_with_coords({"a": (0.0, 0.0), "b": (1.0, 1.0)})
    out = render_scatter(rep, grid_width=20, grid_height=10)
    lines = out.splitlines()
    top = lines[0]
    assert len(top) == 22  # 20 + 2 (box chars ┌┐)
    assert "20×10" in out


def test_negative_coords() -> None:
    """Negative coordinates (from UMAP projection) handled correctly."""
    rep = _graph_with_coords({
        "a": (-3.0, -2.0),
        "b": (5.0, 4.0),
        "c": (0.0, 0.0),
        "d": (-1.5, 3.0),
    })
    out = render_scatter(rep)
    # Should render without crash and have 4 nodes
    assert "Nodes: 4" in out
    # All four first chars should appear somewhere in grid body (between ┌ and └)
    for ch in ("a", "b", "c", "d"):
        assert ch in out


def test_deterministic_across_two_builds() -> None:
    """Two separate rep builds from same graph → deterministic output.
    (Tests that build_representation is itself deterministic.)"""
    g = Graph()
    for nid in ("alice", "bob", "charlie"):
        g.add_node(Node(id=nid, type="person"))
    g.add_edge(Edge("alice", "bob", "knows"))
    g.add_edge(Edge("bob", "charlie", "knows"))

    rep = build_representation(g)
    rep2 = build_representation(g)

    # Manually assign coords (simulating what projection layer would do)
    coords = {"alice": (0.2, 0.8), "bob": (0.5, 0.5), "charlie": (0.9, 0.1)}
    for t in rep.tokens:
        if t.id in coords:
            x, y = coords[t.id]
            t.x = x
            t.y = y
    for t in rep2.tokens:
        if t.id in coords:
            x, y = coords[t.id]
            t.x = x
            t.y = y

    a = render_scatter(rep)
    b = render_scatter(rep2)
    assert a == b