"""Identity scheme for graph-core (T-005 / R3).

ID scheme: ``<type-prefix>:<short-slug>``
- Slug is kebab-case, 2..5 tokens, derived deterministically from source text.
- Collisions append ``:n`` starting at ``:2`` in stable insertion order (R3.2).
- IDs longer than 40 chars trigger a non-fatal :class:`UserWarning` (R3.3).
- Same source text yields same id across rebuilds (R3.4).
"""

from __future__ import annotations

import re
import warnings
from typing import Optional

# Module-level config (R3.1: 2..5 tokens). Override per-call via min_tokens/max_tokens kwargs.
DEFAULT_MIN_TOKENS = 2
DEFAULT_MAX_TOKENS = 5
LENGTH_WARN_THRESHOLD = 40

_PUNCT_RE = re.compile(r"[^a-z0-9\s-]")
_WS_RE = re.compile(r"\s+")


def derive_slug(
    source_text: str,
    min_tokens: int = DEFAULT_MIN_TOKENS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Derive a kebab-case slug from arbitrary text deterministically (R3.1)."""
    if not source_text or not source_text.strip():
        return "untitled"
    s = source_text.lower()
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    tokens = [t for t in s.split(" ") if t]
    if not tokens:
        return "untitled"
    tokens = tokens[:max_tokens]
    if len(tokens) < min_tokens:
        # Pad nothing — return what we have. Slug stability over min-token enforcement.
        pass
    return "-".join(tokens)


def _build_id(type_prefix: str, slug: str) -> str:
    return f"{type_prefix}:{slug}"


class IdRegistry:
    """Mints stable ids and tracks collisions (T-005 / R3.2, R3.4)."""

    def __init__(self) -> None:
        self._issued: dict[str, int] = {}  # base id -> last suffix used (1 means base)

    def mint(
        self,
        type_prefix: str,
        source_text: str,
        min_tokens: int = DEFAULT_MIN_TOKENS,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        """Mint an id. Same (type_prefix, source_text) yields same base; collisions append :n.

        Stability: feeding the same source text twice in distinct registries yields the
        same id (no collision suffix). Within ONE registry, the second call collides and
        receives ``:2``.
        """
        slug = derive_slug(source_text, min_tokens=min_tokens, max_tokens=max_tokens)
        base = _build_id(type_prefix, slug)
        if base not in self._issued:
            self._issued[base] = 1
            final = base
        else:
            self._issued[base] += 1
            final = f"{base}:{self._issued[base]}"
        if len(final) > LENGTH_WARN_THRESHOLD:
            warnings.warn(
                f"id '{final}' exceeds {LENGTH_WARN_THRESHOLD} chars",
                UserWarning,
                stacklevel=2,
            )
        return final

    def issued(self) -> set[str]:
        """Return the full set of issued ids (including suffixed variants)."""
        result: set[str] = set()
        for base, count in self._issued.items():
            result.add(base)
            for n in range(2, count + 1):
                result.add(f"{base}:{n}")
        return result


def mint_id(
    type_prefix: str,
    source_text: str,
    registry: Optional[IdRegistry] = None,
    min_tokens: int = DEFAULT_MIN_TOKENS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Convenience wrapper. Without a registry, returns the base id (no collision tracking)."""
    if registry is None:
        slug = derive_slug(source_text, min_tokens=min_tokens, max_tokens=max_tokens)
        out = _build_id(type_prefix, slug)
        if len(out) > LENGTH_WARN_THRESHOLD:
            warnings.warn(
                f"id '{out}' exceeds {LENGTH_WARN_THRESHOLD} chars",
                UserWarning,
                stacklevel=2,
            )
        return out
    return registry.mint(type_prefix, source_text, min_tokens=min_tokens, max_tokens=max_tokens)
