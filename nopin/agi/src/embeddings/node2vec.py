"""Node2Vec-style embedding (T-069 / embeddings R1).

Stdlib-only implementation: deterministic random walks + hash-based
projection. NOT a true skip-gram — the contract is:

- Every node has exactly one vector after embed (R1.1)
- Vector dimensionality is configurable; default 64 (R1.2)
- Seeded; identical inputs + seed → identical vectors (R1.3)
- Empty graph → empty result (R1.4)

The hash-projection approach lets us avoid gensim/numpy build-time
dependencies for v1. A future task may swap in a real skip-gram while
preserving this signature.

Document upgrade path: see ``cavekit-embeddings.md`` Out of Scope.
"""

from __future__ import annotations

import hashlib
import math
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from graph_core.graph import Graph
from graph_core.persistence.frontmatter import load_node_file, save_node_file, NodeFile


@dataclass(frozen=True)
class EmbeddingConfig:
    dim: int = 64
    walk_length: int = 16
    walks_per_node: int = 4
    seed: int = 42
    p: float = 1.0  # return parameter (kept for API parity with classic Node2Vec)
    q: float = 1.0  # in-out parameter
    store_in_graph: bool = False  # write vectors to node frontmatter; off by default


def default_config() -> EmbeddingConfig:
    return EmbeddingConfig()


def embed_graph(
    graph: Graph,
    config: EmbeddingConfig | None = None,
    graph_dir: str | None = None,
) -> dict[str, list[float]]:
    """Return {node_id -> dim-length float vector}. Deterministic for fixed seed.

    When ``config.store_in_graph`` is True, vectors are persisted to each node's
    ``.md`` frontmatter under an ``embedding`` key. On re-run, already-embedded
    nodes are read from frontmatter instead of recomputed.

    When ``store_in_graph=True``, ``graph_dir`` must be provided — it points to
    the base directory containing ``nodes/<type>/<id>.md``. Each node's file is
    resolved as ``graph_dir/nodes/<type>/<id>.md`` or via its ``payload_ref``.

    When ``store_in_graph=False`` (default), behaviour is unchanged and
    ``graph_dir`` is ignored.
    """
    cfg = config or default_config()
    if len(graph) == 0:
        return {}

    # --- In-graph read path: load pre-computed vectors from node frontmatter ---
    if cfg.store_in_graph:
        if graph_dir is None:
            raise ValueError(
                "store_in_graph=True requires graph_dir to locate node files"
            )
        stored = _read_stored_vectors(graph, graph_dir)
        # If ALL nodes already have stored vectors, return early.
        if len(stored) == len(graph):
            return stored
    else:
        stored = {}

    # Build deterministic adjacency in sorted order so RNG sequence is stable.
    adjacency: dict[str, list[str]] = {}
    for nid in sorted(graph.node_ids):
        targets = []
        for e in sorted(graph.edges, key=lambda x: x.triple):
            if e.source_id == nid:
                targets.append(e.target_id)
        adjacency[nid] = targets

    all_walks: dict[str, list[list[str]]] = {nid: [] for nid in adjacency}
    for nid in sorted(adjacency):
        node_seed_hash = int.from_bytes(
            hashlib.sha256(f"{cfg.seed}|{nid}".encode("utf-8")).digest()[:8],
            "big",
        )
        node_rng = random.Random(node_seed_hash)
        for _ in range(cfg.walks_per_node):
            walk = [nid]
            for _ in range(cfg.walk_length - 1):
                neighbours = adjacency.get(walk[-1], [])
                if not neighbours:
                    break
                walk.append(node_rng.choice(neighbours))
            all_walks[nid].append(walk)

    # Project walks to a vector via hash-based binning.
    result: dict[str, list[float]] = {}
    for nid, walks in all_walks.items():
        if nid in stored:
            result[nid] = stored[nid]
        else:
            result[nid] = _walks_to_vector(walks, dim=cfg.dim, seed=cfg.seed)

    # --- In-graph write path: persist computed vectors to node frontmatter ---
    if cfg.store_in_graph:
        _write_stored_vectors(graph, graph_dir, result)

    return result


def _node_file_path(node_id: str, graph_dir: str, graph: Graph) -> str:
    """Resolve the file path for a node ID."""
    n = graph.get_node(node_id)
    if n is not None and n.payload_ref is not None:
        p = n.payload_ref
        if os.path.isabs(p):
            return p
        return os.path.join(graph_dir, p)
    # Fall back to standard layout.
    node_type = n.type if n else "node"
    return os.path.join(graph_dir, "nodes", node_type, f"{node_id}.md")


def _read_stored_vectors(graph: Graph, graph_dir: str) -> dict[str, list[float]]:
    """Read pre-computed vectors from node frontmatter.

    Returns dict of {node_id: vector} for every node whose file has an
    ``embedding`` key in frontmatter. Silent if file missing or unparseable.
    """
    result: dict[str, list[float]] = {}
    for n in graph.nodes:
        path = _node_file_path(n.id, graph_dir, graph)
        if not os.path.isfile(path):
            continue
        try:
            nf = load_node_file(path, body=False)
        except Exception:
            continue
        emb = nf.frontmatter.get("embedding")
        if isinstance(emb, list) and len(emb) > 0:
            result[n.id] = [float(v) for v in emb]
    return result


def _write_stored_vectors(graph: Graph, graph_dir: str, vectors: dict[str, list[float]]) -> None:
    """Write vectors into each node's frontmatter under an ``embedding`` key.

    Idempotent: missing/unreadable node files are skipped silently. Existing
    frontmatter keys are preserved; only ``embedding`` is added/updated.
    """
    for n in graph.nodes:
        if n.id not in vectors:
            continue
        path = _node_file_path(n.id, graph_dir, graph)
        if not os.path.isfile(path):
            continue
        try:
            nf = load_node_file(path, body=True)
        except Exception:
            continue
        nf.frontmatter["embedding"] = vectors[n.id]
        try:
            save_node_file(path, nf)
        except Exception:
            continue


def _walks_to_vector(walks: list[list[str]], dim: int, seed: int) -> list[float]:
    """Hash each (seed, node, position) into a dim-bucket and accumulate magnitudes."""
    vec = [0.0] * dim
    if not walks:
        return vec
    for walk in walks:
        for pos, node_id in enumerate(walk):
            h = hashlib.sha256(f"{seed}|{node_id}|{pos}".encode("utf-8")).digest()
            # Two buckets per hash → spread mass across dimensions.
            b1 = int.from_bytes(h[:4], "big") % dim
            b2 = int.from_bytes(h[4:8], "big") % dim
            sign = 1.0 if (h[8] & 1) == 0 else -1.0
            vec[b1] += sign * 1.0 / (pos + 1)
            vec[b2] += sign * 0.5 / (pos + 1)
    # L2 normalize for stability.
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec