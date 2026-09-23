"""`goal:g7.31.3.1` falsifier 1 — the cold-seat brief lists the five routes.

The claim: a cold seat's custom-instruction surface lists the five pane-facing
routes by their contract names (write / read / send / dispatch|workflow /
rotate|spawn), each mapped to its engine seam. This file reads the live SoT
node `doc:director-grok-internals` (`SECTION:PROFILE`, the region a grok seat
syncs into its profile description per `doc:grok-harness-internals-sync`
`SECTION:ROUTINE_SYNC`), extracts the `routes:` line, and requires all five
names and all five seams.

The falsifier half runs the SAME extractor over mutated copies of the live
bytes: delete one route -> red, add a sixth -> red. A checker that cannot go
red on a copy proves nothing about the real artifact, so both halves are here.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
NODES = REPO / ".agi" / "nodes" / "doc"
BRIEF = NODES / "director-grok-internals.md"
WIRE = NODES / "grok-harness-internals-sync.md"

#: Contract names, `/` and `|` read as the same disjunction.
ROUTES = ["write", "read", "send", "dispatch/workflow", "rotate/spawn"]
#: Engine seams named by goal:g7.31.3's table.
SEAMS = ["write.py", "commands.py", "viewport", "send.py",
         "dispatch.py", "workflow.py", "rotate.py"]

_SECTION = re.compile(
    r"(?ms)^### SECTION:PROFILE\b(.*?)(?=^### SECTION:|\Z)")


def _profile_block(text: str) -> str:
    m = _SECTION.search(text)
    assert m, "no SECTION:PROFILE block in doc:director-grok-internals"
    return m.group(1)


def _routes_line(text: str) -> str | None:
    m = re.search(r"(?m)^routes:\s*(.+)$", _profile_block(text))
    return m.group(1).strip() if m else None


def _norm(name: str) -> str:
    return name.replace("|", "/")


def check(text: str) -> list[str]:
    """Violations of the claim on `text`. Empty list == the brief complies."""
    line = _routes_line(text)
    if line is None:
        return ["SECTION:PROFILE has no routes: line"]
    segments = [s.strip() for s in line.split("\u00b7") if s.strip()]
    names = [_norm(re.split(r"\s*\(", s, 1)[0].strip()) for s in segments]
    seams_text = " ".join(re.findall(r"\((.*?)\)", line))
    bad: list[str] = []
    for route in ROUTES:
        if route not in names:
            bad.append(f"missing route {route!r}")
    for seam in SEAMS:
        if seam not in seams_text:
            bad.append(f"missing engine seam {seam!r}")
    unexpected = [n for n in names if n not in ROUTES]
    if unexpected:
        bad.append(f"unexpected routes {unexpected!r}")
    return bad


def _mutate_routes(text: str, fn) -> str:
    """Rewrite the routes line in place; keeps every other byte."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("routes:"):
            lines[i] = "routes: " + fn(line[len("routes:"):].strip())
            return "\n".join(lines)
    raise AssertionError("no routes: line to mutate")


def test_real_brief_names_all_five_routes_and_seams():
    assert check(BRIEF.read_text(encoding="utf-8")) == []


def test_brief_is_the_cold_seat_surface_the_sync_recipe_names():
    wire = WIRE.read_text(encoding="utf-8")
    assert "SECTION:PROFILE" in wire
    assert "per-post SoT" in wire
    assert "routes:" in BRIEF.read_text(encoding="utf-8")


def test_checker_goes_red_on_a_deleted_route():
    broken = _mutate_routes(
        BRIEF.read_text(encoding="utf-8"),
        lambda rest: "\u00b7".join(
            s for s in rest.split("\u00b7") if "send" not in s))
    assert check(broken)


def test_checker_goes_red_on_a_sixth_route():
    broken = _mutate_routes(
        BRIEF.read_text(encoding="utf-8"),
        lambda rest: rest + " \u00b7 grok-only (sneaky.py)")
    assert any("unexpected" in v for v in check(broken))


def test_checker_goes_red_on_a_deleted_seam():
    broken = _mutate_routes(
        BRIEF.read_text(encoding="utf-8"),
        lambda rest: rest.replace("(commands.py+viewport)", ""))
    assert any("commands.py" in v for v in check(broken))
