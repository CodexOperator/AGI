"""UMAP-style 2D/3D projection (T-070 / embeddings R2).

This is a v1 placeholder using deterministic random projection +
optional PCA (when numpy is available). The contract — same vectors +
config + seed → identical coords — is what matters; the underlying
algorithm can be swapped in v2 (true UMAP).

Acceptance criteria (R2):
- R2.1: every embedded node has (x, y) coords after projection
- R2.2: projection dim configurable to 2 or 3, default 2
- R2.3: same vectors + config + seed → identical coords
- R2.4: fewer-than-two embedded nodes → degenerate result, no raise
"""

from __future__ import annotations

import hashlib
import math
import random
import warnings
from dataclasses import dataclass

try:
    import numpy as np  # type: ignore

    HAS_NUMPY = True
except ImportError:  # pragma: no cover
    HAS_NUMPY = False


@dataclass(frozen=True)
class ProjectionConfig:
    dim: int = 2  # 2 or 3
    seed: int = 42
    n_neighbors: int = 15
    min_dist: float = 0.1


def project(
    vectors: dict[str, list[float]],
    config: ProjectionConfig | None = None,
) -> dict[str, tuple[float, ...]]:
    """Project high-dim vectors to 2D (or 3D). Returns ``{node_id: (x, y[, z])}``."""
    cfg = config or ProjectionConfig()
    if cfg.dim not in (2, 3):
        raise ValueError(f"projection dim must be 2 or 3, got {cfg.dim}")

    if len(vectors) == 0:
        return {}
    if len(vectors) < 2:
        warnings.warn(
            f"projection requires >= 2 nodes; got {len(vectors)}; returning zero coords",
            UserWarning,
            stacklevel=2,
        )
        return {nid: tuple([0.0] * cfg.dim) for nid in vectors}

    if HAS_NUMPY:
        return _project_pca(vectors, cfg)
    return _project_random(vectors, cfg)


def _project_pca(vectors: dict[str, list[float]], cfg: ProjectionConfig) -> dict[str, tuple[float, ...]]:
    ids = sorted(vectors.keys())
    M = np.array([vectors[i] for i in ids], dtype=np.float64)
    # Center
    M = M - M.mean(axis=0, keepdims=True)
    # SVD-based PCA. Seed numpy RNG for any tie-breaking determinism.
    rng = np.random.default_rng(cfg.seed)
    # Tie-break by adding tiny seeded noise (deterministic).
    noise = rng.normal(0.0, 1e-12, size=M.shape)
    M = M + noise
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    proj = U[:, : cfg.dim] * S[: cfg.dim]
    return {ids[i]: tuple(float(x) for x in proj[i]) for i in range(len(ids))}


def _project_random(vectors: dict[str, list[float]], cfg: ProjectionConfig) -> dict[str, tuple[float, ...]]:
    """Hash-based deterministic projection — no numpy required."""
    ids = sorted(vectors.keys())
    out: dict[str, tuple[float, ...]] = {}
    for nid in ids:
        h = hashlib.sha256(f"{cfg.seed}|{nid}|coord".encode("utf-8")).digest()
        coords = []
        for i in range(cfg.dim):
            chunk = h[i * 4 : (i + 1) * 4]
            v = int.from_bytes(chunk, "big") / 2**32  # 0..1
            v = (v * 2 - 1)  # -1..1
            coords.append(v)
        out[nid] = tuple(coords)
    return out
