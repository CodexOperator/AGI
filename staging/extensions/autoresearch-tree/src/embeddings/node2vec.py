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
import random
from dataclasses import dataclass
from typing import Callable

from graph_core.graph import Graph


@dataclass(frozen=True)
class EmbeddingConfig:
    dim: int = 64
    walk_length: int = 16
    walks_per_node: int = 4
    seed: int = 42
    p: float = 1.0  # return parameter (kept for API parity with classic Node2Vec)
    q: float = 1.0  # in-out parameter


def default_config() -> EmbeddingConfig:
    return EmbeddingConfig()


def embed_graph(
    graph: Graph,
    config: EmbeddingConfig | None = None,
) -> dict[str, list[float]]:
    """Return {node_id -> dim-length float vector}. Deterministic for fixed seed."""
    cfg = config or default_config()
    if len(graph) == 0:
        return {}

    # Build deterministic adjacency in sorted order so RNG sequence is stable.
    adjacency: dict[str, list[str]] = {}
    for nid in sorted(graph.node_ids):
        targets = []
        for e in sorted(graph.edges, key=lambda x: x.triple):
            if e.source_id == nid:
                targets.append(e.target_id)
        adjacency[nid] = targets

    rng = random.Random(cfg.seed)

    # Generate walks (deterministic: per-node seeded mini-RNG so adding new nodes
    # doesn't perturb existing nodes' walks too much).
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

    # Project walks to a vector via hash-based binning. The seed is folded into
    # the hash so that even when walks are structurally identical (e.g. on a
    # branchless chain) different seeds yield different vectors.
    return {
        nid: _walks_to_vector(walks, dim=cfg.dim, seed=cfg.seed)
        for nid, walks in all_walks.items()
    }


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
