"""T-003: Edge primitive tests (graph-core/R2)."""

from dataclasses import fields

from graph_core.edge import Edge


def test_edge_field_surface_is_four() -> None:
    """R2.2: edge exposes exactly source_id, target_id, relation, tags."""
    declared = {f.name for f in fields(Edge)}
    assert declared == {"source_id", "target_id", "relation", "tags"}


def test_edge_idempotent_set_insert() -> None:
    """R2.3: inserting same triple twice yields a single set member."""
    e1 = Edge(source_id="hyp:a", target_id="exp:b", relation="tested_by")
    e2 = Edge(source_id="hyp:a", target_id="exp:b", relation="tested_by")
    s = {e1, e2}
    assert len(s) == 1


def test_edge_distinct_relation_distinct_identity() -> None:
    """Different relations on the same node pair are distinct edges."""
    e1 = Edge(source_id="hyp:a", target_id="exp:b", relation="tested_by")
    e2 = Edge(source_id="hyp:a", target_id="exp:b", relation="contradicts")
    s = {e1, e2}
    assert len(s) == 2


def test_edge_tags_dont_affect_identity() -> None:
    """Tags are metadata, not identity (R2.3 strict reading)."""
    e1 = Edge(source_id="hyp:a", target_id="exp:b", relation="tested_by")
    e2 = Edge(source_id="hyp:a", target_id="exp:b", relation="tested_by", tags={"strong"})
    assert e1 == e2
    assert hash(e1) == hash(e2)
    assert {e1, e2} == {e1}


def test_edge_triple_property() -> None:
    """`.triple` returns the identity tuple."""
    e = Edge(source_id="idea:x", target_id="hyp:y", relation="spawns")
    assert e.triple == ("idea:x", "hyp:y", "spawns")
