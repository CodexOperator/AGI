"""T-002: parent/child invariant guards (graph-core/R1.3)."""

import pytest

from graph_core import Node
from graph_core.errors import SelfLoopError


def test_self_loop_parents_rejected() -> None:
    """Adding own id as parent must raise SelfLoopError."""
    n = Node(id="hyp:loops", type="hypothesis")
    with pytest.raises(SelfLoopError) as exc:
        n.add_parent("hyp:loops")
    assert exc.value.node_id == "hyp:loops"
    assert exc.value.side == "parents"
    assert "hyp:loops" in str(exc.value)


def test_self_loop_children_rejected() -> None:
    """Adding own id as child must raise SelfLoopError."""
    n = Node(id="hyp:loops", type="hypothesis")
    with pytest.raises(SelfLoopError) as exc:
        n.add_child("hyp:loops")
    assert exc.value.side == "children"
    assert "hyp:loops" in str(exc.value)


def test_duplicate_parent_silently_absorbed() -> None:
    """Set semantics drop duplicates without error."""
    n = Node(id="exp:run-001", type="experiment")
    n.add_parent("hyp:lru-saturates")
    n.add_parent("hyp:lru-saturates")
    assert n.parents == {"hyp:lru-saturates"}
    assert len(n.parents) == 1


def test_duplicate_child_silently_absorbed() -> None:
    """Set semantics drop duplicates without error."""
    n = Node(id="hyp:lru-saturates", type="hypothesis")
    n.add_child("exp:run-001")
    n.add_child("exp:run-001")
    assert n.children == {"exp:run-001"}
    assert len(n.children) == 1


def test_self_loop_error_subclasses_graph_core_error() -> None:
    """SelfLoopError is a structured exception type (R1.3)."""
    from graph_core.errors import GraphCoreError

    assert issubclass(SelfLoopError, GraphCoreError)
