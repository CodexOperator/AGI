"""Attractiveness scoring for chains (chain-engine/R6 — T-052).

The attractiveness score ranks chains so the longest-chain attractor can
select which chains to prioritize. Score is a weighted sum of four
dimensions: length, depth, recency, mvp_count.

Acceptance criteria (R6):
- R6.1: score = w.length*len + w.depth*depth + w.recency*recency + w.mvp_count*mvp_count
- R6.2: each weight from configuration, not hard-coded
- R6.3: all-zero weights → returns 0.0 (not a crash)
- R6.4: identical inputs → identical scores (pure function)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterator

from graph_core.types import RenderableGraph

from .types import Chain


@dataclass(frozen=True)
class AttractivenessWeights:
    """Four weights for the attractiveness score. Each is a float; defaults are 0.0."""

    length: float = 0.0
    depth: float = 0.0
    recency: float = 0.0
    mvp_count: float = 0.0

    def weight_delta(self, other: AttractivenessWeights) -> float:
        """Max absolute difference across any single weight component."""
        return max(
            abs(self.length - other.length),
            abs(self.depth - other.depth),
            abs(self.recency - other.recency),
            abs(self.mvp_count - other.mvp_count),
        )


@dataclass
class ChainMetrics:
    """Four measurable dimensions of a chain, computed from the graph."""

    length: int  # number of nodes in the chain
    depth: int  # BFS distance from nearest root (idea node)
    recency: float  # exponential-decay score over time since last node edit
    mvp_count: int  # count of mvp-typed nodes in the chain

    @classmethod
    def from_chain(
        cls, chain: Chain, graph: RenderableGraph, now: float
    ) -> ChainMetrics:
        length = len(chain)
        depth = _compute_depth(chain, graph)
        recency = _compute_recency(chain, graph, now)
        mvp_count = sum(
            1 for node_id in chain if (graph.get_node(node_id) or _null_node()).type == "mvp"
        )
        return cls(length=length, depth=depth, recency=recency, mvp_count=mvp_count)


def _null_node() -> "Node":
    """Placeholder returned when a node lookup fails."""
    from dataclasses import dataclass as dc

    @dc(frozen=True)
    class _NullNode:
        id: str = ""
        type: str = ""
        payload_ref: str | None = None
        parents: frozenset[str] = frozenset()
        children: frozenset[str] = frozenset()
        tags: frozenset[str] = frozenset()

    return _NullNode()


def _compute_depth(chain: Chain, graph: RenderableGraph) -> int:
    """Depth of the first node in the chain: length of shortest backward path to a root.

    A root is a node with no incoming 'next' edges (a true graph root).
    Depth = number of 'next' edges traversed backward from the chain's first node
    to reach any root. Idea nodes (roots) have depth 0; their direct children have
    depth 1; grandchildren have depth 2; and so on.

    This measures how "deep" the chain's origin is in the graph hierarchy,
    regardless of whether the chain itself starts at a root.
    """
    # Build incoming-edge map for 'next' relation: target_id -> [source_ids]
    incoming: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            incoming.setdefault(edge.target_id, []).append(edge.source_id)

    # Find roots: nodes with no incoming 'next' edges
    roots: set[str] = {nid for nid in graph.node_ids if nid not in incoming}

    first_node = chain[0]
    if first_node in roots:
        return 0

    # BFS backward from first_node toward the nearest root
    # (follow incoming 'next' edges in reverse direction)
    visited: set[str] = {first_node}
    queue: list[tuple[str, int]] = [(first_node, 0)]
    while queue:
        current, dist = queue.pop(0)
        for parent_id in incoming.get(current, []):
            if parent_id in roots:
                return dist + 1
            if parent_id not in visited:
                visited.add(parent_id)
                queue.append((parent_id, dist + 1))

    return 0  # no root found; default to 0


# Exponential decay half-life in seconds (1 hour)
_HALF_LIFE_SECONDS = 3600.0


def _compute_recency(chain: Chain, graph: RenderableGraph, now: float) -> float:
    """Exponential decay score for the most-recently-edited node in the chain.

    score = exp(-ln(2) * (now - last_edit) / half_life)
    score = 1.0 when node was just edited; ~0.5 after half_life; ~0.0 after many half-lives.
    """
    max_score = 0.0
    for node_id in chain:
        node = graph.get_node(node_id)
        if node is None:
            continue
        # Use last_edited if present, else 0 (oldest possible)
        last_edited = getattr(node, "last_edited", None) or 0.0
        delta = max(0.0, now - last_edited)
        score = math.exp(-math.log(2) * delta / _HALF_LIFE_SECONDS)
        if score > max_score:
            max_score = score
    return max_score


def attractiveness(chain: Chain, weights: AttractivenessWeights, now: float, graph: RenderableGraph) -> float:
    """Compute the attractiveness score for a chain (R6.1).

    Args:
        chain: ordered list of node ids
        weights: the four component weights
        now: current unix timestamp (seconds)
        graph: the graph to look up node metadata in

    Returns:
        The weighted sum of the four metrics. All-zero weights → 0.0 (R6.3).

    This is a pure function: identical inputs always produce identical outputs (R6.4).
    """
    metrics = ChainMetrics.from_chain(chain, graph, now)
    score = (
        weights.length * metrics.length
        + weights.depth * metrics.depth
        + weights.recency * metrics.recency
        + weights.mvp_count * metrics.mvp_count
    )
    return score


def score_all_chains(
    chains: list[Chain],
    weights: AttractivenessWeights,
    now: float,
    graph: RenderableGraph,
) -> list[tuple[Chain, float]]:
    """Score all chains with the given weights (R6).

    Returns list of (chain, score) pairs in the same order as the input chains.
    Pure function: does not mutate the graph.
    """
    return [(chain, attractiveness(chain, weights, now, graph)) for chain in chains]
