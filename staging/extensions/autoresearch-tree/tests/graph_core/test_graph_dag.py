"""T-004 tests: Graph DAG with cycle rejection (graph-core/R2)."""

import copy

import pytest

from graph_core import Node
from graph_core.edge import Edge
from graph_core.errors import CycleError
from graph_core.graph import Graph, GraphError


def _make_chain(g: Graph, ids: list[str]) -> None:
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))


def test_cycle_rejection_leaves_graph_unchanged() -> None:
    """R2.1: cycle insert raises CycleError; graph state unchanged."""
    g = Graph()
    _make_chain(g, ["a", "b", "c"])
    pre_nodes = set(g.node_ids)
    pre_edges = {e.triple for e in g.edges}
    # Closing edge c -> a would create cycle a->b->c->a
    with pytest.raises(CycleError) as exc:
        g.add_edge(Edge(source_id="c", target_id="a", relation="next"))
    assert "a" in exc.value.path
    assert g.node_ids == pre_nodes
    assert {e.triple for e in g.edges} == pre_edges


def test_self_loop_edge_rejected_as_cycle() -> None:
    """A self-edge a->a is a 1-cycle — must be rejected."""
    g = Graph()
    g.add_node(Node(id="a", type="x"))
    with pytest.raises(CycleError):
        g.add_edge(Edge(source_id="a", target_id="a", relation="self"))


def test_remove_node_drops_all_incident_edges() -> None:
    """R2.4: removing a node with 2 in + 3 out drops exactly 5 edges."""
    g = Graph()
    for i in ["a", "b", "c", "d", "e", "hub"]:
        g.add_node(Node(id=i, type="x"))
    # 2 incoming → hub
    g.add_edge(Edge(source_id="a", target_id="hub", relation="r1"))
    g.add_edge(Edge(source_id="b", target_id="hub", relation="r1"))
    # 3 outgoing from hub
    g.add_edge(Edge(source_id="hub", target_id="c", relation="r2"))
    g.add_edge(Edge(source_id="hub", target_id="d", relation="r2"))
    g.add_edge(Edge(source_id="hub", target_id="e", relation="r2"))
    assert g.edge_count == 5
    dropped = g.remove_node("hub")
    assert dropped == 5
    assert g.edge_count == 0
    assert "hub" not in g
    # No dangling refs anywhere
    for e in g.edges:
        assert e.source_id != "hub"
        assert e.target_id != "hub"


def test_idempotent_add_node() -> None:
    """Re-adding a node with same id is a no-op."""
    g = Graph()
    g.add_node(Node(id="a", type="x"))
    g.add_node(Node(id="a", type="x"))
    assert len(g) == 1


def test_idempotent_add_edge() -> None:
    """Re-adding identical edge triple is a no-op."""
    g = Graph()
    _make_chain(g, ["a", "b"])
    g.add_edge(Edge(source_id="a", target_id="b", relation="next"))
    assert g.edge_count == 1


def test_remove_edge_returns_status() -> None:
    """remove_edge returns True if removed, False if absent."""
    g = Graph()
    _make_chain(g, ["a", "b"])
    e = Edge(source_id="a", target_id="b", relation="next")
    assert g.remove_edge(e) is True
    assert g.remove_edge(e) is False


def test_edge_to_missing_node_raises() -> None:
    """Edge endpoints must already be in the graph."""
    g = Graph()
    g.add_node(Node(id="a", type="x"))
    with pytest.raises(GraphError):
        g.add_edge(Edge(source_id="a", target_id="ghost", relation="x"))


def test_cycle_path_in_error_message() -> None:
    """CycleError carries the path that would be closed."""
    g = Graph()
    _make_chain(g, ["a", "b", "c", "d"])
    with pytest.raises(CycleError) as exc:
        g.add_edge(Edge(source_id="d", target_id="a", relation="back"))
    assert exc.value.source_id == "d"
    assert exc.value.target_id == "a"
    # Path is the discovered route from target back to source plus the closing source.
    assert "a" in exc.value.path and "d" in exc.value.path
