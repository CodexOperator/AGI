"""goal:g7.31.3.1 — the cold seat brief lists the five pane-facing routes.

The brief is the custom-instruction surface injected into every spawned seat
(`extensions/agi/lib/agent-prompt.md`, passed as `--append-system-prompt` by
the pi adapter). The route block must name all five routes and their engine
seams. Assertions are scoped to the section, not the whole file, so deleting
a route line fails the test.

``COLD_SEAT_BRIEF`` overrides the file under test — used by the negative check
to point this test at a deliberately broken copy. The name must not begin
``AGI_``: the suite conftest pops every ``AGI_*`` var before fixtures run, so
such an override is silently ignored (measured — a broken copy still passed).
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROMPT = REPO_ROOT / "extensions" / "agi" / "lib" / "agent-prompt.md"

SECTION_HEADING = "## The five pane-facing routes"
ROUTE_NAMES = ("write", "read", "send", "dispatch", "workflow", "rotate", "spawn")
ENGINE_SEAMS = (
    "write.py",
    "commands.py",
    "viewport",
    "send.py",
    "dispatch.py",
    "workflow.py",
    "rotate.py",
)


def _brief_text() -> str:
    path = Path(os.environ.get("COLD_SEAT_BRIEF", str(DEFAULT_PROMPT)))
    return path.read_text(encoding="utf-8")


def _route_section(text: str) -> str:
    assert SECTION_HEADING in text, f"brief has no '{SECTION_HEADING}' section"
    tail = text.split(SECTION_HEADING, 1)[1]
    end = tail.find("\n## ")
    return tail if end == -1 else tail[:end]


def test_brief_names_five_routes_and_engine_seams():
    section = _route_section(_brief_text())
    for name in ROUTE_NAMES:
        assert name in section, f"route name '{name}' missing from route section"
    for seam in ENGINE_SEAMS:
        assert seam in section, f"engine seam '{seam}' missing from route section"
