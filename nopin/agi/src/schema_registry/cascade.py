"""Auto-discovery cascade (T-025 step 1; T-026 step 2; T-028 step 3) — R5.

Given a directory of unstructured node files, decide which registered schema
applies. The cascade has three steps; this file implements step 1 (bracket name
match) and provides an extension point for steps 2 (fingerprint similarity) and
3 (LM hook fallback).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from .loader import Schema, SchemaRegistry


@dataclass
class DiscoveryResult:
    """The outcome of one cascade run."""

    schema: Optional[Schema]
    step: str  # 'bracket' | 'fingerprint' | 'lm-hook' | 'generic' | 'no-match'
    candidate_score: float = 0.0


def cascade_step_1(directory: str | Path, registry: SchemaRegistry) -> DiscoveryResult:
    """Step 1: bracket-name match (R5.1).

    The directory's basename is the candidate name. If `[name].md` is in the
    active set, return that schema and short-circuit.
    """
    dirname = Path(directory).name
    schema = registry.schemas.get(dirname)
    if schema is not None and schema.active:
        return DiscoveryResult(schema=schema, step="bracket", candidate_score=1.0)
    return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)


# T-026 will register a fingerprint step here.
_extra_steps: list[Callable[[str | Path, SchemaRegistry], DiscoveryResult]] = []


def register_extra_step(fn: Callable[[str | Path, SchemaRegistry], DiscoveryResult]) -> None:
    _extra_steps.append(fn)


def discover_schema(directory: str | Path, registry: SchemaRegistry) -> DiscoveryResult:
    """Run the cascade. T-025: only step 1; T-026/T-028 extend."""
    r = cascade_step_1(directory, registry)
    if r.schema is not None:
        return r
    for step in _extra_steps:
        r = step(directory, registry)
        if r.schema is not None:
            return r
    return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)
