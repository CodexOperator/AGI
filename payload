"""T-070 tests: UMAP projection (embeddings/R2)."""

import warnings

import pytest

from embeddings import EmbeddingConfig, embed_graph
from embeddings.projection import ProjectionConfig, project
from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph


def _chain(ids: list[str]) -> Graph:
    g = Graph()
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))
    return g


def test_every_node_gets_xy() -> None:
    """R2.1: every embedded node has (x, y) coordinate pair."""
    g = _chain([f"n{i}" for i in range(5)])
    vecs = embed_graph(g)
    coords = project(vecs)
    assert set(coords.keys()) == set(vecs.keys())
    for c in coords.values():
        assert len(c) == 2


def test_default_dim_is_two() -> None:
    """R2.2: default projection dim is 2."""
    assert ProjectionConfig().dim == 2


def test_three_dim_configurable() -> None:
    """R2.2: dim configurable to 3."""
    g = _chain([f"n{i}" for i in range(5)])
    vecs = embed_graph(g)
    coords = project(vecs, ProjectionConfig(dim=3))
    for c in coords.values():
        assert len(c) == 3


def test_invalid_dim_raises() -> None:
    """Validation: only 2 or 3 accepted."""
    with pytest.raises(ValueError):
        project({"a": [1.0, 2.0]}, ProjectionConfig(dim=5))


def test_seeded_runs_identical() -> None:
    """R2.3: two runs over same vectors + config + seed → identical coords."""
    g = _chain([f"n{i}" for i in range(8)])
    vecs = embed_graph(g, EmbeddingConfig(seed=7))
    cfg = ProjectionConfig(seed=7)
    a = project(vecs, cfg)
    b = project(vecs, cfg)
    assert a == b


def test_zero_nodes_empty() -> None:
    """No nodes → empty result."""
    assert project({}) == {}


def test_one_node_degenerate() -> None:
    """R2.4: one node → zero-coord with warning, no exception."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        coords = project({"only": [1.0, 2.0, 3.0]})
        assert coords == {"only": (0.0, 0.0)}
        assert any(issubclass(item.category, UserWarning) for item in w)


def test_two_nodes_no_warning() -> None:
    """R2.4: two nodes → real projection, no degenerate warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        coords = project({"a": [1.0, 0.0], "b": [0.0, 1.0]})
        assert len(coords) == 2
        # No "requires >= 2 nodes" warning
        msgs = [str(item.message) for item in w]
        assert not any("requires >= 2" in m for m in msgs)
