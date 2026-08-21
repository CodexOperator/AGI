"""Chain ranking by attractiveness (chain-engine/R3 — T-049).

Ranks chains so the longest-chain attractor can select which chains to
prioritize. Ranking is a pure function: identical inputs produce
identical outputs across runs.

Acceptance criteria (R3):
- R3.1: rank chains by attractiveness with deterministic tie-break
- R3.2: longest chain among top-ranked when no other factor dominates
- R3.3: short chains can rank above longer ones when non-length scores are higher
- R3.4: ranking is pure — equal inputs → equal outputs
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from .attractiveness import (
    AttractivenessWeights,
    attractiveness,
    score_all_chains,
)
from .types import Chain

if TYPE_CHECKING:
    from graph_core.types import RenderableGraph


def rank_chains(
    chains: list[Chain],
    weights: AttractivenessWeights,
    graph: RenderableGraph,
    now: float | None = None,
) -> list[tuple[Chain, float, int]]:
    """Rank chains by attractiveness score descending.

    Args:
        chains: list of chains to rank
        weights: attractiveness weights
        graph: the graph to look up node metadata in
        now: unix timestamp; defaults to time.time()

    Returns:
        List of (chain, score, length) tuples sorted by score descending,
        with ties broken by chain id sequence lexicographically.

    Pure function: does not mutate inputs or the graph (R3.4).
    """
    if now is None:
        now = time.time()

    scored = score_all_chains(chains, weights, now, graph)

    # Sort: score descending, then chain ids ascending (deterministic tie-break)
    scored.sort(key=lambda item: (-item[1], [n for n in item[0]]))

    return [(chain, score, len(chain)) for chain, score in scored]


def longest_n(
    chains: list[Chain],
    n: int,
    weights: AttractivenessWeights,
    graph: RenderableGraph,
    now: float | None = None,
) -> list[tuple[Chain, float, int]]:
    """Return the top-N chains ranked by attractiveness (chain-engine/R9 — T-056)."""
    ranked = rank_chains(chains, weights, graph, now)
    return ranked[:n]
