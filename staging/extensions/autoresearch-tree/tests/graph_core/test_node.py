"""Unit tests for graph-core Node primitive (T-001 / graph-core R1)."""

from dataclasses import fields

from graph_core import Node


def test_field_set_is_exactly_six() -> None:
    """R1.1: id, type, payload_ref, parents, children, tags. Nothing else."""
    declared = {f.name for f in fields(Node)}
    assert declared == {"id", "type", "payload_ref", "parents", "children", "tags"}


def test_node_with_no_parents_is_root() -> None:
    """R1.2: no-parent root accepted."""
    n = Node(id="idea:capillary-dag", type="idea")
    assert n.parents == set()
    assert n.is_root is True


def test_node_with_no_children_is_leaf() -> None:
    """R1.2: no-child leaf accepted."""
    n = Node(id="outcome:fast-warm-load", type="outcome")
    assert n.children == set()
    assert n.is_leaf is True


def test_tags_independent_of_parents_children() -> None:
    """R1.4: mutating tags does not affect parents/children (independent sets)."""
    n = Node(id="hyp:lru-saturates", type="hypothesis")
    assert n.tags == set()
    n.tags.add("performance")
    n.tags.add("warm-load")
    assert n.parents == set()
    assert n.children == set()
    # Cross-check: parents/children mutation does not bleed into tags
    n.parents.add("idea:capillary-dag")
    n.children.add("exp:lru-bench")
    assert n.tags == {"performance", "warm-load"}


def test_payload_ref_defaults_none_optional() -> None:
    """R1.1: payload_ref accepts None; lazy-loading deferred to T-009."""
    n = Node(id="exp:run-001", type="experiment")
    assert n.payload_ref is None
    n2 = Node(id="exp:run-002", type="experiment", payload_ref="nodes/experiment/run-002.md")
    assert n2.payload_ref == "nodes/experiment/run-002.md"
