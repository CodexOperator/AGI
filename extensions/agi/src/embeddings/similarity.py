"""Cosine-similarity query API (T-073 / embeddings R5).

Acceptance criteria (R5):
- R5.1: returns up to k (id, score) pairs ordered by descending score
- R5.2: missing embedding → empty list + warning, NOT raise
- R5.3: scores in [-1.0, 1.0]
- R5.4: deterministic for same inputs and state
"""

from __future__ import annotations

import math
import warnings


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity in [-1.0, 1.0]. 0 vectors yield 0."""
    if len(a) != len(b):
        raise ValueError(f"dim mismatch: {len(a)} vs {len(b)}")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    val = dot / (na * nb)
    # Clamp tiny float drift outside [-1, 1].
    if val > 1.0:
        return 1.0
    if val < -1.0:
        return -1.0
    return val


def similar_to(
    node_id: str,
    k: int,
    vectors: dict[str, list[float]],
) -> list[tuple[str, float]]:
    """Return top-k cosine-similar (id, score) for ``node_id``.

    - R5.1: descending score, max ``k`` items, excluding the query node itself.
    - R5.2: if ``node_id`` not in vectors → ``[]`` + UserWarning (no raise).
    - R5.3: all scores ∈ [-1.0, 1.0].
    - R5.4: deterministic — ties broken by lexicographic node_id.
    """
    if node_id not in vectors:
        warnings.warn(
            f"node '{node_id}' has no embedding; similarity query returns empty list",
            UserWarning,
            stacklevel=2,
        )
        return []
    if k <= 0:
        return []
    qv = vectors[node_id]
    scored: list[tuple[str, float]] = []
    for other_id, ov in vectors.items():
        if other_id == node_id:
            continue
        s = cosine(qv, ov)
        scored.append((other_id, s))
    # Sort by (-score, id) so ties break deterministically.
    scored.sort(key=lambda x: (-x[1], x[0]))
    return scored[:k]
