"""Falsifiers for goal:g7.31.3.3.1 + goal:g7.31.3.3.2 (parent slots).

.3.3.1 — committed parent-slot rows under post geometry; defs hold no live
         occupancy fields as SoT.
.3.3.2 — occupy+clear via local runtime file without editing committed defs.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import parent_slots  # noqa: E402


SAMPLE_BODY = """---
id: config:parent-slots
type: config
parents:
  - goal:g7.31.3.3
title: "Committed parent-slot definitions (g7.31.3.3.1)"
---
# config:parent-slots

Committed **definitions only**. Live occupancy is the runtime file owned by
`goal:g7.31.3.3.2` (`.agi/sessions/parent-occupancy.json`) — never these rows.

parent_slots:
  director-helper:
    - {"id": "parent-0", "kind": "parent"}
  director-engine:
    - {"id": "parent-0", "kind": "parent"}
    - {"id": "parent-1", "kind": "parent"}
"""


@pytest.fixture
def graph(tmp_path):
    root = tmp_path / "proj"
    geo = root / ".agi" / "nodes" / ".geometry"
    geo.mkdir(parents=True)
    (geo / "parent-slots.md").write_text(SAMPLE_BODY, encoding="utf-8")
    (root / ".agi" / "sessions").mkdir(parents=True)
    return root


def test_committed_path_names_geometry_file(graph):
    p = parent_slots.committed_path(graph)
    assert p.name == "parent-slots.md"
    assert p.parts[-3:] == ("nodes", ".geometry", "parent-slots.md")
    assert p.is_file()


def test_load_committed_sample_posts(graph):
    defs = parent_slots.load_committed(graph)
    assert "director-helper" in defs
    assert "director-engine" in defs
    assert [s["id"] for s in defs["director-helper"]] == ["parent-0"]
    assert [s["id"] for s in defs["director-engine"]] == ["parent-0", "parent-1"]
    parent_slots.assert_defs_hold_no_occupancy(defs)


def test_committed_defs_refuse_occupancy_fields_as_sot(graph):
    """Negative: a def row carrying live occupancy fields fails the guard."""
    bad = {
        "director-helper": [
            {"id": "parent-0", "kind": "parent", "occupant": "a00-dead"},
        ]
    }
    with pytest.raises(AssertionError, match="occupancy SoT"):
        parent_slots.assert_defs_hold_no_occupancy(bad)


def test_slot_count_contract_is_concurrency_times_parallel():
    assert parent_slots.slot_count_contract({}) == 1
    assert parent_slots.slot_count_contract({"spawn": {"parallel": 2}}) == 2
    assert parent_slots.slot_count_contract(
        {"spawn": {"concurrency": 3, "parallel": 2}}
    ) == 6
    assert parent_slots.slot_count_contract({"spawn": "nope"}) == 1


def test_occupy_and_clear_do_not_touch_committed_defs(graph):
    defs_path = parent_slots.committed_path(graph)
    before = hashlib.sha256(defs_path.read_bytes()).hexdigest()
    occ_path = parent_slots.occupy(
        graph, "director-helper", "parent-0", "a00-probe"
    )
    assert occ_path == parent_slots.occupancy_path(graph)
    assert occ_path.is_file()
    data = parent_slots.read_occupancy(graph)
    assert data["posts"]["director-helper"]["parent-0"]["occupant"] == "a00-probe"
    after_occupy = hashlib.sha256(defs_path.read_bytes()).hexdigest()
    assert after_occupy == before, "occupy must not edit committed slot defs"
    parent_slots.clear(graph, "director-helper", "parent-0")
    data2 = parent_slots.read_occupancy(graph)
    assert "director-helper" not in data2.get("posts", {})
    after_clear = hashlib.sha256(defs_path.read_bytes()).hexdigest()
    assert after_clear == before, "clear must not edit committed slot defs"


def test_seat_tip_geometry_holds_sample_parent_slots():
    """Live falsifier on the seat tip: committed defs exist for a sample post."""
    root = Path(__file__).resolve().parents[3]
    path = parent_slots.committed_path(root)
    assert path.is_file(), f"missing committed parent-slots at {path}"
    defs = parent_slots.load_committed(root)
    assert defs, "parent-slots.md parsed zero posts"
    assert any(defs.values()), "no slot rows under any post"
    parent_slots.assert_defs_hold_no_occupancy(defs)
    # at least one sample post used by directors on this stop-line
    assert "director-helper" in defs or "director-engine" in defs
