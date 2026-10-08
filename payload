"""Mid-chain join candidate selection (chain-engine/R4).

Acceptance criteria (R4):
- R4.1: join candidates from anywhere in chains, not only tails
- R4.2: configurable mid-chain join probability
- R4.3: minimum-chain-length filter
- R4.4: probability zero → only tail nodes
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from graph_core.graph import Graph

# Runtime import
from graph_core.graph import Graph  # noqa: E402


@dataclass
class MidChainConfig:
    """Configuration for mid-chain join behavior."""
    mid_chain_join_prob: float = 0.3  # R4.2: probability of joining mid-chain
    min_chain_length: int = 3         # R4.3: minimum chain length to consider


def mid_chain_join_candidates(
    chains: Sequence[Sequence[str]],
    g,  # type: Graph  # noqa: F821
    config: MidChainConfig | None = None,
) -> list[str]:
    """Return candidate node IDs for joining a chain.

    R4.1: Returns nodes from anywhere in chains, not only tails.
    R4.2: Uses mid_chain_join_prob to decide whether to sample from
          mid-chain positions vs tail nodes.
    R4.3: Filters out chains shorter than min_chain_length.
    R4.4: With prob=0, returns only tail nodes.

    Args:
        chains: List of chains, each a sequence of node IDs in order.
        g: Graph (used for metadata lookups if needed).
        config: Mid-chain join configuration. Defaults to MidChainConfig().

    Returns:
        List of candidate node IDs to join.
    """
    if config is None:
        config = MidChainConfig()

    candidates: list[str] = []

    for chain in chains:
        chain_len = len(chain)

        # R4.3: skip chains shorter than minimum
        if chain_len < config.min_chain_length:
            continue

        if config.mid_chain_join_prob <= 0.0:
            # R4.4: only tail nodes
            candidates.append(chain[-1])
        elif config.mid_chain_join_prob >= 1.0:
            # Always mid-chain: sample from all non-tail positions
            mid_positions = chain[1:-1] if len(chain) > 2 else chain
            candidates.append(random.choice(mid_positions))
        else:
            # R4.2: probabilistic split
            if random.random() < config.mid_chain_join_prob:
                # Mid-chain: all positions except tail
                mid_positions = chain[:-1]
                candidates.append(random.choice(mid_positions))
            else:
                # Tail-only
                candidates.append(chain[-1])

    return candidates


def all_chain_nodes(
    chains: Sequence[Sequence[str]],
    config: MidChainConfig | None = None,
) -> list[str]:
    """Return all non-tail nodes from chains (R4.1 verification helper).

    For verifying that mid-chain join can reach any position.
    """
    if config is None:
        config = MidChainConfig()

    nodes: list[str] = []
    for chain in chains:
        if len(chain) >= config.min_chain_length:
            nodes.extend(chain[:-1])  # exclude tail
    return nodes
