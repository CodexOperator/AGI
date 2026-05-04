"""Fingerprint-similarity step of the auto-discovery cascade (T-026 / R5.2).

Compute a fingerprint = set of frontmatter keys observed in candidate files in
the directory. Compute the union of declared fields per registered schema.
Score = Jaccard(observed, schema_keys). Pick highest score >= 0.7.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from graph_core.persistence import load_node_file

from .cascade import DiscoveryResult, register_extra_step
from .loader import Schema, SchemaRegistry


SIMILARITY_THRESHOLD = 0.7


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def collect_fingerprint(directory: str | Path) -> set[str]:
    """Union of frontmatter keys across .md/.json files in `directory`."""
    base = Path(directory)
    keys: set[str] = set()
    if not base.is_dir():
        return keys
    for p in sorted(base.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".json"}:
            continue
        try:
            nf = load_node_file(p, body=False)
        except Exception:
            continue
        keys.update(nf.frontmatter.keys())
    return keys


def schema_field_keys(schema: Schema) -> set[str]:
    out = set(schema.fields.keys())
    # Plus any top-level frontmatter we treat as schema fields. Exclude
    # schema-metadata keys (`name`, `fields`, `validation`) that are not
    # node-level frontmatter keys.
    fm = schema.frontmatter or {}
    for k in fm:
        if k in {"name", "fields", "validation"}:
            continue
        out.add(k)
    return out


def cascade_step_2(
    directory: str | Path,
    registry: SchemaRegistry,
    threshold: float = SIMILARITY_THRESHOLD,
) -> DiscoveryResult:
    """Step 2 (R5.2): fingerprint similarity match (only against ACTIVE schemas)."""
    observed = collect_fingerprint(directory)
    if not observed:
        return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)
    best: tuple[float, Schema | None] = (0.0, None)
    for name, schema in registry.schemas.items():
        if not schema.active:
            continue
        score = jaccard(observed, schema_field_keys(schema))
        if score > best[0]:
            best = (score, schema)
    if best[1] is not None and best[0] >= threshold:
        return DiscoveryResult(schema=best[1], step="fingerprint", candidate_score=best[0])
    return DiscoveryResult(schema=None, step="no-match", candidate_score=best[0])


# Self-register at import.
register_extra_step(cascade_step_2)
