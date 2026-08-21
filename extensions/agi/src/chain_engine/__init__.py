"""Chain engine — virtual chain queries on top of graph-core.

Chains are computed from the graph, not stored separately.
"""
from .types import Chain
from .chains import find_chains, find_chains_from_node
from .attractiveness import (
    attractiveness,
    score_all_chains,
    AttractivenessWeights,
    ChainMetrics,
)
from .ranking import rank_chains, longest_n

__all__ = [
    "Chain",
    "find_chains",
    "find_chains_from_node",
    "attractiveness",
    "score_all_chains",
    "AttractivenessWeights",
    "ChainMetrics",
    "rank_chains",
    "longest_n",
]
