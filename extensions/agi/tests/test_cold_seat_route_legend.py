"""Byte-level guard for the cold-seat pane-facing route legend."""

from pathlib import Path

NODES = Path(__file__).resolve().parents[3] / ".agi" / "nodes" / "doc"
CANONICAL = (NODES / "director-grok-internals.md", NODES / "belam-grok-internals.md")
LEGEND = "`write` · `read` · `send` · `dispatch | workflow` · `rotate | spawn`"


def test_both_canonical_cold_seats_carry_the_five_route_legend():
    for path in CANONICAL:
        text = path.read_bytes().decode("utf-8")
        assert LEGEND in text, f"missing exact five-contract legend: {path}"


def test_legend_is_not_the_old_unpaired_legend():
    for path in CANONICAL:
        text = path.read_bytes().decode("utf-8")
        assert "routes: write.py · read · send · dispatch/workflow · rotate/spawn" not in text
