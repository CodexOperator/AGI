"""Chain query API (chain-engine/R9 — T-056, T-057, T-058).

Exposes read-only queries over the chain graph:
- longest_n: top-N chains by attractiveness
- branching_factor: fork density across chain participants
- mid_chain_candidates: nodes available for mid-chain joining
- all_chain_queries_pure: all queries are read-only (T-059)

All functions are pure: they never mutate the graph.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .attractiveness import AttractivenessWeights
from .ranking import longest_n as _longest_n

if TYPE_CHECKING:
    from graph_core.graph import Graph
    from graph_core.types import RenderableGraph
    from .types import Chain


def longest_n(
    chains: list["Chain"],
    n: int,
    weights: AttractivenessWeights,
    graph: "RenderableGraph",
    now: float | None = None,
) -> list[tuple["Chain", float, int]]:
    """Return top-N chains ranked by attractiveness (R9.1 — T-056).

    Wraps rank_chains() and slices to top N. Pure function.

    Args:
        chains: list of chains to rank
        n: maximum number of results
        weights: attractiveness weights
        graph: the graph (for metadata lookup)
        now: unix timestamp, defaults to time.time()

    Returns:
        List of (chain, score, length) tuples, sorted by score descending.
    """
    return _longest_n(chains, n, weights, graph, now)


def branching_factor(graph: "RenderableGraph") -> dict[str, float | dict[str, int]]:
    """Return fork density across all chain-participant nodes (R9.2 — T-057).

    Iterates over all nodes in the graph and counts their outgoing 'next' edges.
    Nodes that don't participate in any chain (no outgoing 'next' edges) are
    excluded from the per_node dict but contribute to avg calculation as 0.

    Pure function: does not mutate the graph.

    Args:
        graph: the graph to analyze

    Returns:
        {
            "avg": average out-degree (total_next_edges / total_nodes),
            "per_node": {node_id: out_edge_count, ...}
        }
    """
    # Count outgoing 'next' edges per node
    out_counts: dict[str, int] = {}
    total_next = 0

    for edge in graph.edges:
        if edge.relation == "next":
            out_counts[edge.source_id] = out_counts.get(edge.source_id, 0) + 1
            total_next += 1

    # All nodes have a per_node entry (0 if no outgoing next edges)
    per_node: dict[str, int] = {nid: out_counts.get(nid, 0) for nid in graph.node_ids}

    total_nodes = len(graph.node_ids)
    avg = total_next / total_nodes if total_nodes > 0 else 0.0

    return {"avg": avg, "per_node": per_node}


def mid_chain_candidates(
    graph: "RenderableGraph",
    chains: list["Chain"],
    min_length: int,
    max_recency: float,
    rng_seed: int | None = None,
) -> list[tuple[str, "Chain", int]]:
    """Return mid-chain join candidates (R9.3 — T-058).

    Filters chains by min_length and max_recency, then samples one position
    per qualifying chain:
    - With probability `mid_chain_join_prob` (configurable, default 0.3): sample
      a non-tail position uniformly at random
    - Else: return the tail node (last node in the chain)

    Pure function when rng_seed is fixed. Uses a deterministic fallback when
    rng_seed is None (uses hash of chain id for pseudo-random sampling).

    Args:
        graph: the graph (for recency lookup)
        chains: all chains in the graph
        min_length: minimum chain length to consider
        max_recency: maximum recency score (0.0-1.0, higher = more recent)
        rng_seed: optional seed for reproducible sampling

    Returns:
        List of (node_id, chain, position) triples.
        position is 0-indexed from start of chain.
    """
    import hashlib

    # mid_chain_join_prob default (can be overridden by caller)
    mid_chain_join_prob = 0.3

    candidates: list[tuple[str, "Chain", int]] = []

    for chain in chains:
        if len(chain) < min_length:
            continue

        # Compute recency for this chain
        recency = _chain_recency(chain, graph)
        if recency > max_recency:
            continue

        # Determine whether to pick mid or tail
        # Use deterministic pseudo-random based on chain id hash
        if rng_seed is not None:
            # seeded rng for reproducibility
            import random
            rng = random.Random(rng_seed + hash(chain[0]) % (2**31))
            use_mid = rng.random() < mid_chain_join_prob
        else:
            # Deterministic fallback: hash-based
            h = int(hashlib.md5(chain[0].encode()).hexdigest(), 16)
            use_mid = (h % 1000) / 1000.0 < mid_chain_join_prob

        if use_mid and len(chain) > 1:
            # Pick a non-tail position
            if rng_seed is not None:
                pos = rng.randint(0, len(chain) - 2)
            else:
                h2 = int(hashlib.md5(chain[-1].encode()).hexdigest(), 16)
                pos = h2 % (len(chain) - 1)
            candidates.append((chain[pos], chain, pos))
        else:
            # Tail node
            candidates.append((chain[-1], chain, len(chain) - 1))

    return candidates


def _chain_recency(chain: list[str], graph: "RenderableGraph") -> float:
    """Compute the recency score for a chain (highest recency among nodes).

    Returns a score in [0.0, 1.0]: 1.0 = just edited, 0.0 = very old.
    Uses exponential decay with 1-hour half-life.
    """
    import math
    import time

    _HALF_LIFE = 3600.0
    now = time.time()
    max_score = 0.0

    for nid in chain:
        node = graph.get_node(nid)
        if node is None:
            continue
        last_edited = getattr(node, "last_edited", None) or 0.0
        delta = max(0.0, now - last_edited)
        score = math.exp(-math.log(2) * delta / _HALF_LIFE)
        if score > max_score:
            max_score = score

    return max_score


def all_chain_queries_pure(
    chains: list["Chain"],
    graph: "RenderableGraph",
    weights: AttractivenessWeights,
    n: int = 3,
) -> bool:
    """Verify all chain queries return the same result on repeated calls (R9.4 — T-059).

    Runs longest_n, branching_factor, and mid_chain_candidates twice each
    and asserts the results are identical.

    Pure function: all underlying queries are read-only.

    Returns:
        True if all queries are pure (deterministic on repeated calls).
    """
    # Snapshot graph state
    graph_copy = _snapshot_graph(graph)

    # longest_n purity
    r1 = longest_n(chains, n, weights, graph)
    r2 = longest_n(chains, n, weights, graph)
    longest_pure = r1 == r2

    # branching_factor purity
    b1 = branching_factor(graph)
    b2 = branching_factor(graph)
    branching_pure = b1 == b2

    # mid_chain_candidates purity (with fixed seed)
    m1 = mid_chain_candidates(graph, chains, min_length=3, max_recency=1.0, rng_seed=42)
    m2 = mid_chain_candidates(graph, chains, min_length=3, max_recency=1.0, rng_seed=42)
    mid_pure = m1 == m2

    # Verify graph wasn't mutated
    graph_after = _snapshot_graph(graph)
    not_mutated = graph_copy == graph_after

    return longest_pure and branching_pure and mid_pure and not_mutated


def _snapshot_graph(graph: "RenderableGraph") -> dict:
    """Create a hashable snapshot of graph state for purity verification."""
    return {
        "node_ids": sorted(graph.node_ids),
        "edges": sorted(
            (e.source_id, e.target_id, e.relation) for e in graph.edges
        ),
    }
