"""goal:g7.31.3.1 -- every cold-seat brief/custom-instruction surface names the
five pane-facing engine routes.

The five routes are the contract table in `goal:g7.31.3`:

    write | read | send | dispatch|workflow | rotate|spawn

This test PINS that each cold-seat surface carries ONE line naming all five,
by token, so a silent deletion of any route name from a brief goes RED. It is
a drift detector, not a generator: it never edits a brief, it only reads the
live files. A deliberate rename must update the brief AND this token list in
one edit, which is exactly the "old->new" the falsifier asks for.

`_missing_routes(text)` is pure so the negative probe can run it against a
mutated COPY without touching the shared tree (measured in the experiment
node: a copy with `send` deleted returns the full token list, i.e. non-empty).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]

#: the five routes, spelled as the paired seams the table uses.
ROUTE_TOKENS = ("write", "read", "send", "dispatch", "workflow", "rotate", "spawn")

#: cold-seat brief / custom-instruction surfaces that state the routes.
SURFACES = (
    "extensions/agi/briefs/director-belam-duties.md",
    ".agi/nodes/doc/unified-director-brief.md",
    ".agi/nodes/doc/director-grok-internals.md",
)


def _missing_routes(text: str) -> list[str]:
    """First line naming all five routes; return tokens absent from it.

    An empty list means a single line carries every route token. If NO line
    carries all seven tokens, every token is reported missing for that line
    (the surface has no routes line at all).
    """
    for line in text.splitlines():
        if all(re.search(rf"\b{re.escape(t)}\b", line) for t in ROUTE_TOKENS):
            return []
    return list(ROUTE_TOKENS)


@pytest.mark.parametrize("rel", SURFACES)
def test_surface_names_all_five_routes(rel: str) -> None:
    path = REPO / rel
    assert path.exists(), f"cold-seat surface missing: {rel}"
    missing = _missing_routes(path.read_text(encoding="utf-8"))
    assert missing == [], (
        f"{rel} has no line naming the five routes; "
        f"missing tokens {missing}"
    )


def test_negative_probe_is_load_bearing() -> None:
    """The checker itself: a routes line with `send` deleted goes RED.

    Guards against a checker that always passes (e.g. a token list that got
    emptied, or a regex that matches the empty string).
    """
    good = "routes: write·read·send·dispatch/workflow·rotate/spawn"
    assert _missing_routes(good) == []
    mutated = _missing_routes(good.replace("send", ""))
    assert mutated != [] and "send" in mutated
