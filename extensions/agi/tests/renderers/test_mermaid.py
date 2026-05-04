"""T-063 tests: Mermaid renderer (renderers/R3)."""

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from renderers import build_representation, render_mermaid


def _chain(ids: list[str]) -> Graph:
    g = Graph()
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))
    return g


def test_starts_with_mermaid_directive() -> None:
    """R3.1: output begins with a recognized Mermaid directive."""
    g = _chain(["a", "b"])
    rep = build_representation(g)
    out = render_mermaid(rep)
    first = out.splitlines()[0]
    assert first.strip() in {"flowchart TD", "graph TD"}


def test_byte_equal_across_runs() -> None:
    """R3.4: two runs → byte-equal output."""
    g = _chain([f"n{i}" for i in range(10)])
    rep = build_representation(g)
    a = render_mermaid(rep)
    b = render_mermaid(rep)
    assert a == b


def test_node_dedup() -> None:
    """R3.3: each node id appears at most once in the output."""
    g = _chain(["a", "b", "c"])
    rep = build_representation(g)
    out = render_mermaid(rep)
    # Count node-decl lines (have `["...`)
    node_lines = [l for l in out.splitlines() if '["' in l]
    ids_seen = set()
    for line in node_lines:
        # Extract first whitespace-separated token
        tok = line.strip().split("[")[0]
        assert tok not in ids_seen, f"duplicate node decl: {tok}"
        ids_seen.add(tok)


def test_edge_dedup() -> None:
    """R3.3: each edge appears at most once."""
    g = _chain(["a", "b"])
    rep = build_representation(g)
    out = render_mermaid(rep)
    # Edge lines contain ' -->|'
    edge_lines = [l for l in out.splitlines() if "-->|" in l]
    assert len(edge_lines) == len(set(edge_lines))


def test_handles_special_chars_in_id() -> None:
    """Ids with `:` (our id scheme) sanitize to mermaid-safe identifiers."""
    g = Graph()
    g.add_node(Node(id="hyp:lru-saturates", type="hypothesis"))
    g.add_node(Node(id="exp:run-001", type="experiment"))
    g.add_edge(Edge(source_id="hyp:lru-saturates", target_id="exp:run-001", relation="tested_by"))
    rep = build_representation(g)
    out = render_mermaid(rep)
    # No raw `:` in mermaid identifiers (would break parsing)
    for line in out.splitlines():
        if line.strip().startswith("flowchart") or line.strip().startswith("classDef"):
            continue
        if '"' in line:
            # Label is quoted — colons inside labels are fine. Check the identifier portion only.
            ident_part = line.strip().split("[")[0].split(" ")[0] if "[" in line else line.strip().split(" ")[0]
            assert ":" not in ident_part


def test_empty_graph_yields_directive_only() -> None:
    g = Graph()
    rep = build_representation(g)
    out = render_mermaid(rep)
    lines = [l for l in out.splitlines() if l.strip()]
    assert lines[0].startswith("flowchart")
    # No node/edge lines
    assert not any('["' in l for l in lines)
    assert not any('-->|' in l for l in lines)
