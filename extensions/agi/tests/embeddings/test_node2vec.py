"""T-069 tests: Node2Vec embedding (embeddings/R1)."""

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from embeddings import EmbeddingConfig, default_config, embed_graph


def _chain(ids: list[str]) -> Graph:
    g = Graph()
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))
    return g


def test_zero_node_graph_returns_empty() -> None:
    """R1.4: zero-node graph completes successfully with empty vector set."""
    g = Graph()
    assert embed_graph(g) == {}


def test_one_node_graph_yields_one_vector() -> None:
    """R1.1: every node has exactly one vector."""
    g = Graph()
    g.add_node(Node(id="a", type="x"))
    out = embed_graph(g)
    assert set(out.keys()) == {"a"}
    assert len(out["a"]) == 64


def test_ten_node_graph_yields_ten_vectors() -> None:
    """R1.1: every node has exactly one vector for a 10-node chain."""
    g = _chain([f"n{i}" for i in range(10)])
    out = embed_graph(g)
    assert len(out) == 10
    assert all(len(v) == 64 for v in out.values())


def test_dim_is_configurable() -> None:
    """R1.2: dimensionality is configurable."""
    g = _chain(["a", "b", "c"])
    cfg = EmbeddingConfig(dim=16)
    out = embed_graph(g, cfg)
    assert all(len(v) == 16 for v in out.values())


def test_default_dim_is_64() -> None:
    """R1.2: default dim documented as 64."""
    assert default_config().dim == 64


def test_seeded_runs_identical() -> None:
    """R1.3: two runs over same graph + config + seed → identical vectors."""
    g = _chain([f"n{i}" for i in range(8)])
    cfg = EmbeddingConfig(seed=42)
    a = embed_graph(g, cfg)
    b = embed_graph(g, cfg)
    assert a == b


def test_different_seeds_yield_different_vectors() -> None:
    g = _chain([f"n{i}" for i in range(8)])
    a = embed_graph(g, EmbeddingConfig(seed=1))
    b = embed_graph(g, EmbeddingConfig(seed=2))
    assert a != b
