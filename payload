"""Type definitions for chain-engine."""

from __future__ import annotations

# Chain = ordered list of node ids forming a valid autoresearch path.
Chain = list[str]

# Ordered type sequence for a valid chain.
# Each entry is a node type; + means one or more of that type.
CHAIN_TYPE_SEQUENCE: list[str] = [
    "idea",
    "hypothesis",
    "experiment",
    "verdict",
    "mvp",
    "outcome",
    "bigger_outcome",
    "app_purpose",
]

# Valid transition pairs: (from_type, to_type)
# hypothesis -> hypothesis allowed (multiple consecutive)
# experiment -> experiment allowed (multiple consecutive)
# All other transitions must follow the sequence strictly.
_VALID_TRANSITIONS: set[tuple[str, str]] = {
    ("idea", "hypothesis"),
    ("hypothesis", "hypothesis"),
    ("hypothesis", "experiment"),
    ("experiment", "experiment"),
    ("experiment", "verdict"),
    ("verdict", "experiment"),  # Allow verdict → experiment for chain extension
    ("verdict", "mvp"),
    ("mvp", "outcome"),
    ("outcome", "bigger_outcome"),
    ("bigger_outcome", "app_purpose"),
}


def is_valid_transition(from_type: str, to_type: str) -> bool:
    """Check if transitioning from from_type to to_type is valid in a chain."""
    return (from_type, to_type) in _VALID_TRANSITIONS
