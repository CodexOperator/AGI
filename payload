"""Unit tests for graph-core Node primitive (T-001 / graph-core R1)."""

from dataclasses import fields

from graph_core import Node


#: R1.1's six required fields. A reader may rely on every one of these.
REQUIRED_FIELDS = {"id", "type", "payload_ref", "parents", "children", "tags"}

#: Fields added since R1.1 was written, each with the reason it is load-bearing.
#: `origin` records which generator (if any) owns a node, and the origin-guarded
#: prune in the snapshot scripts is built on it — without it a snapshot cannot
#: tell its own output from an agent's and deleting becomes unsafe (TODO.md H0).
OPTIONAL_FIELDS = {"origin"}


def test_required_fields_are_all_present() -> None:
    """R1.1: id, type, payload_ref, parents, children, tags."""
    assert REQUIRED_FIELDS <= {f.name for f in fields(Node)}


def test_field_set_has_not_drifted() -> None:
    """Nothing else — and any addition must be declared above, with a reason.

    This assertion used to read `== REQUIRED_FIELDS` and had been failing ever
    since `origin` was added without updating it. A permanently-red test is a
    diagnostic that lies: it stopped distinguishing "someone added a field on
    purpose" from "someone added a field by accident", which is the only thing
    it existed to do. Widening it to the declared set restores that.
    """
    assert {f.name for f in fields(Node)} == REQUIRED_FIELDS | OPTIONAL_FIELDS


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
