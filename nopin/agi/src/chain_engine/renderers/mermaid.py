"""Mermaid chain renderer (chain-engine/R11).

Builds a Representation from chain objects (lists of node ids) and delegates
to the shared src/renderers/mermaid.render_mermaid().

render_mermaid_chains(chains, max_chains=10) -> str
  chains: list of list[str] — each inner list is a chain of node ids
  max_chains: max number of chains to render (None = all)
  Returns: Mermaid flowchart TD syntax string
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow import from sibling chain_engine module and the shared renderers
_SRC = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(_SRC))

from chain_engine.types import Chain
from renderers.representation import RenderToken, Representation
from renderers.mermaid import render_mermaid as _render_mermaid


# ---------------------------------------------------------------------------
# Node type to label prefix
# ---------------------------------------------------------------------------
_TYPE_LABELS: dict[str, str] = {
    "idea":         "💡 idea",
    "hypothesis":    "🎯 hyp",
    "experiment":   "🔬 exp",
    "verdict":      "⚖️ verdict",
    "mvp":          "🚀 mvp",
    "outcome":      "📊 outcome",
    "bigger_outcome": "🌐 bigger",
    "app_purpose":  "🎯 app",
}


def _chain_label(chain_id: int, node_id: str) -> str:
    """Human-readable label for a chain node."""
    # Extract domain from idea id e.g. "idea:domain-chain-engine" -> "chain-engine"
    if node_id.startswith("idea:"):
        domain = node_id.split(":", 1)[1]
        return f"idea:{domain[:20]}"
    # For other types, use the id after the prefix
    if ":" in node_id:
        rest = node_id.split(":", 1)[1]
        return f"{rest[:30]}"
    return node_id[:35]


def _infer_type_from_id(node_id: str) -> str:
    """Infer node type from id prefix."""
    if ":" in node_id:
        return node_id.split(":", 1)[0]
    return "unknown"


def _build_representation_from_chains(
    chains: list[Chain], max_chains: int | None = None
) -> Representation:
    """Build a Representation from chain objects.

    Each chain contributes its nodes and the 'next' edges between consecutive nodes.
    Nodes are deduplicated across chains.
    """
    if max_chains is not None:
        chains = chains[:max_chains]

    tokens: list[RenderToken] = []
    seen_ids: set[str] = set()

    for chain_idx, chain in enumerate(chains):
        for node_id in chain:
            if node_id in seen_ids:
                continue
            seen_ids.add(node_id)

            ntype = _infer_type_from_id(node_id)
            label = _chain_label(chain_idx, node_id)

            tokens.append(
                RenderToken(
                    id=node_id,
                    label=label,
                    type=ntype,
                    depth=0,  # Chain nodes don't have graph-depth here
                    x=0.0,
                    y=0.0,
                    edges=[],  # Will add next edges below
                )
            )

    # Build token-by-id lookup
    token_by_id: dict[str, RenderToken] = {t.id: t for t in tokens}

    # Add 'next' edges within each chain (chain is ordered)
    for chain_idx, chain in enumerate(chains):
        for i in range(len(chain) - 1):
            src_id = chain[i]
            tgt_id = chain[i + 1]
            if src_id in token_by_id and tgt_id in token_by_id:
                token_by_id[src_id].edges.append((tgt_id, "next"))

    # Set depth as position in chain (0-indexed)
    for chain in chains:
        for depth, node_id in enumerate(chain):
            if node_id in token_by_id:
                token_by_id[node_id].depth = depth

    return Representation(tokens=tokens)


def render_mermaid_chains(
    chains: list[Chain], max_chains: int | None = 10
) -> str:
    """Render chains as Mermaid flowchart TD.

    Args:
        chains: list of chains (each chain is a list of node id strings)
        max_chains: max number of chains to render (default 10, None = all)

    Returns:
        Mermaid flowchart TD syntax string
    """
    if not chains:
        return "flowchart TD\n    note\n"

    repr_ = _build_representation_from_chains(chains, max_chains=max_chains)
    return _render_mermaid(repr_)
