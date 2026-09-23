"""Falsifier for goal:g7.31.3.1 -- the universal cold-seat brief lists the
five pane-facing routes named in the `goal:g7.31.3` table.

`extensions/agi/lib/agent-prompt.md` is the file `dispatch.py` hands to every
pi seat as `skill_prompt` (dispatch.py:821), so bytes in this section reach a
cold seat. The check is SECTION-SCOPED: parse from the `## The five
pane-facing routes` heading to the next `## ` heading, then assert each route
name and its engine seam is present there. Deleting any one route row (or one
seam) must fail.

Set `COLD_SEAT_BRIEF_PATH` to a deliberately broken copy to prove the test
is non-vacuous. The name carries NO `AGI_`/`AUTORESEARCH_` prefix on purpose:
the parent `extensions/agi/conftest.py` `_agi_env_stripped` session-autouse
fixture deletes every such key before collection, so an `AGI_`-prefixed
override is silently popped and the broken copy is never read (measured
2026-09-23: `AGI_COLD_SEAT_BRIEF_PATH=<broken>` still passed 6/6).
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

ENV_OVERRIDE = "COLD_SEAT_BRIEF_PATH"
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BRIEF = REPO_ROOT / "extensions" / "agi" / "lib" / "agent-prompt.md"
SECTION = "## The five pane-facing routes"

#: route name -> seam bytes that must sit beside it in the section.
ROUTES = {
    "write": ["write.py"],
    "read": ["commands.py", "viewport"],
    "send": ["send.py"],
    "dispatch": ["dispatch.py", "workflow.py"],
    "rotate": ["rotate.py", "spawn"],
}


def _brief_text() -> str:
    override = os.environ.get(ENV_OVERRIDE)
    path = Path(override) if override else DEFAULT_BRIEF
    return path.read_text(encoding="utf-8")


def _route_section(text: str) -> str:
    assert SECTION in text, f"missing section heading: {SECTION!r}"
    rest = text[text.index(SECTION):]
    nxt = rest.find("\n## ", 1)
    return rest if nxt == -1 else rest[:nxt]


def test_section_present_with_exactly_five_route_rows():
    section = _route_section(_brief_text())
    rows = re.findall(r"^\|\s*\d+\s*\|", section, re.M)
    assert len(rows) == 5, f"expected 5 numbered route rows, saw {len(rows)}"


@pytest.mark.parametrize("route,seams", sorted(ROUTES.items()))
def test_route_name_and_seam_in_section(route, seams):
    section = _route_section(_brief_text())
    assert route in section, f"route {route!r} missing from the section"
    for seam in seams:
        assert seam in section, f"seam {seam!r} for route {route!r} missing"
