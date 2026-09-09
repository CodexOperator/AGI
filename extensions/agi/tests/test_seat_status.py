"""Tests for `bin/seat_status.py` — hypothesis:l3w4-telemetry-seat-status.

The load-bearing assertion is that **both** viewport readers state the same
`SeatsView`: one `collect()` computes it, `render_human` and `render_llm` each
render it, and both must carry the same seat names and the same summaries —
the one-render-two-readers invariant `goal:g9.7` demands one layer down.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import viewport as V  # noqa: E402  (bin is on sys.path above)
import seat_status as SS  # noqa: E402


def _load_seat_status():
    spec = importlib.util.spec_from_file_location("seat_status", BIN / "seat_status.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["seat_status"] = m
    spec.loader.exec_module(m)
    return m


S = _load_seat_status()


def _make_fixture(tmp_path):
    """A project dir with two declared seats, both pinned to a healthy meter."""
    geoms = tmp_path / "nodes" / ".geometry"
    geoms.mkdir(parents=True)
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir(parents=True)
    # ladder: context budget so the meter fraction is defined
    (geoms / "ladder.md").write_text(
        "---\nid: config:ladder\ncurrent_season: 2\n"
        "director_context_tokens: 1000000\n---\n",
        encoding="utf-8")
    (geoms / "seats.md").write_text(
        "---\nid: config:seats\nseats:\n"
        '  - {"name": "belam", "role": "prime_director", "session_kind": '
        '"remote-control", "rotated_by": "quorum"}\n'
        '  - {"name": "dir-g16", "role": "director", "session_kind": "tty", '
        '"rotated_by": "advisor", "worktree": ".agi/worktrees/seat-dir-g16", '
        '"session_ref": "518293"}\n'
        "---\n",
        encoding="utf-8")
    # one healthy transcript shared by both pins
    transcript_path = sessions_dir / "t.jsonl"
    transcript_path.write_text(
        json.dumps({"message": {"role": "assistant", "usage": {
            "input_tokens": 100_000, "cache_read_input_tokens": 50_000,
            "cache_creation_input_tokens": 0}}}) + "\n",
        encoding="utf-8")
    for name in ("belam", "dir-g16"):
        (sessions_dir / f"{name}.meter").write_text(str(transcript_path),
                                                     encoding="utf-8")
    # a report node carrying the roll-up's own field
    (tmp_path / "nodes" / "outcome").mkdir(parents=True)
    return tmp_path


def test_seat_status_reaches_both_readers(tmp_path):
    """One `collect()` output appears in both `render_human` and `render_llm`."""
    root = _make_fixture(tmp_path)
    fm_by_id = {
        "outcome:s2": {"id": "outcome:s2", "type": "outcome", "season": "2",
                       "cost_usd_total": 12.5},
        "outcome:other-s": {"id": "outcome:other-s", "type": "outcome",
                            "season": "1", "cost_usd_total": 999.0},
    }
    view = SS.collect(root, fm_by_id)

    assert view.registry_present is True
    names = {s["name"] for s in view.seats}
    assert {"belam", "dir-g16"} <= names
    # the two 100k+50k = 150k / 1M token fractions measure to 0.15 (cache hits
    # fraction math: 150000 / 1000000)
    for s in view.seats:
        assert s["fraction"] == pytest.approx(0.15)
    # only the season-2 report counts for the roll-up
    assert view.rollup_reports_measured == 1
    assert view.rollup_cost_usd_total == pytest.approx(12.5)

    human = "\n".join(V.render_human([], 0, 0, 40, 10_000, "", None, view))
    llm = V.render_llm([], 0, 0, 40, 10_000, "", None, view)

    for seat in ("belam", "dir-g16"):
        assert seat in human, "seat name missing from the human view"
        assert seat in llm, "seat name missing from the llm view"
    assert "cost_usd_total=12.50" in llm
    assert "rollup" in human
    assert "15%" in human
    # worktree (hypothesis:l3w4-hierarchy-one-source): a row that declares
    # one surfaces it; a row that doesn't (belam here) renders fine empty.
    assert "worktree=.agi/worktrees/seat-dir-g16" in llm
    # session_ref: disambiguates a collision-prone ListAgents name so a
    # cross-session SendMessage can address `name [ref]` unambiguously.
    assert "dir-g16 [518293]" in llm
    by_name = {s["name"]: s for s in view.seats}
    assert by_name["belam"]["worktree"] == ""
    assert by_name["belam"]["session_ref"] == ""
    assert by_name["dir-g16"]["session_ref"] == "518293"


def test_no_seats_md_fails_open(tmp_path):
    """Absent registry: both views say so, and neither tracebacks."""
    root = tmp_path  # no seats.md anywhere
    view = SS.collect(root, {})
    assert view.registry_present is False
    assert view.seats == []
    human = str("\n".join(V.render_human([], 0, 0, 40, 120, "", seats=view)))
    llm = V.render_llm([], 0, 0, 40, 120, "", seats=view)
    assert "no seat registry yet" in human
    assert "no seat registry yet" in llm


def test_registry_rows_read_through_hierarchy_single_reader(tmp_path, monkeypatch):
    """The seat reader delegates to hierarchy.load_seats — ONE reader (L3w4).

    hypothesis:l3w4-hierarchy-one-source's "make the view derive" leg: the
    view must read the seat/ladder declarations through hierarchy.py — the
    single reader of the two frontmatter sources — not keep its own copy of
    the seats.md read, or the renderings can diverge from the chart the way
    the prose sources used to. Proved by patching hierarchy.load_seats to a
    sentinel and asserting seat_status returns exactly what the one reader
    returned: if seat_status ever reads seats.md itself instead, the sentinel
    cannot come back and the assertion fails.
    """
    import hierarchy as H
    root = _make_fixture(tmp_path)  # real seats.md, so present=True
    sentinel = [{"name": "single-reader-marker", "role": "director"}]
    monkeypatch.setattr(H, "load_seats", lambda _r: sentinel)
    rows, present = S._load_registry_rows(root)
    assert present is True
    assert rows == sentinel, (
        "seat_status must read through hierarchy.load_seats, not seats.md")


def test_no_engine_write_imports():
    """The status reader must import neither write.py nor node_writer (gate)."""
    src = (Path(__file__).resolve().parent.parent / "bin" / "seat_status.py").read_text()
    assert "import write" not in src
    assert "import node_writer" not in src