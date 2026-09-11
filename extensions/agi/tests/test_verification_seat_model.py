"""Tests for the `seat-model` check in `bin/verification.py` (surface 2 of
hypothesis:l4-a-seats-live-model-is-measured-not-assumed).

The DATA half (experiment:a00-9af5f5f0-38aaed) proved message.model rides
every assistant turn and the real gen VII drift reads cleanly. This is the
READER half: walk config:seats rows with a live session_ref, resolve each
seat's OWN transcript through rotate.py's pin resolution (find_pin_log /
_parse_pin_record — identity supplied, never inferred, trap 0c), and FAIL on
drift. DETECT, NEVER REPAIR: nothing here may rewrite a row or restart a
session; a row with no session_ref, or a pin that does not resolve, is
SKIPPED silently.

The fixture `seat_gen_vii_drift.jsonl` is built from the REAL gen VII
transcript's shape: 129 claude-opus-5 assistant turns, one
model_refusal_fallback system event (2026-09-10T20:46:09.697Z, category
cyber, requestId req_011CevQvLvpbLcLv2GE49WA4), then 297 claude-opus-4-8
turns — the first drifted turn at 2026-09-10T20:46:21.957Z, the newest at
22:11:31.927Z.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402

FIXTURE = (Path(__file__).resolve().parent / "fixtures"
           / "seat_gen_vii_drift.jsonl")

DRIFT_SEAT_ROW = ("name: sanctuary-director, role: director, tier: 1, "
                  "model: claude-opus-5, session_ref: 4a9edc, "
                  "pin_ref: .agi/sessions/sanctuary-director.meter")


def _make_seats_node(groot: Path, rows: list[str]) -> None:
    node = groot / "nodes" / ".geometry" / "seats.md"
    node.parent.mkdir(parents=True, exist_ok=True)
    body = ["---", "type: config", "parents: [goal:g17]",
            "seats:"]
    for r in rows:
        body.append(f"  - {{{r}}}")
    body += ["---", ""]
    node.write_text("\n".join(body), encoding="utf-8")


def _make_pin(groot: Path, seat: str, transcript: Path) -> None:
    sess = groot / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    (sess / f"{seat}.meter").write_text(f"4\t{transcript}\n", encoding="utf-8")


def _no_drift_transcript(tmp_path: Path) -> Path:
    """A transcript with no drift: every assistant turn claude-opus-5."""
    p = tmp_path / "no_drift.jsonl"
    lines = []
    for i in range(5):
        lines.append({"type": "assistant",
                      "timestamp": f"2026-09-10T20:3{i}:00.0Z",
                      "message": {"role": "assistant", "model": "claude-opus-5"}})
    p.write_text("\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8")
    return p


def _restored_transcript(tmp_path: Path) -> Path:
    """The drift fixture with the model restored on a later turn — proof (b):
    clearing the drift means the newest turn matches the row again."""
    p = tmp_path / "restored.jsonl"
    text = FIXTURE.read_text(encoding="utf-8").rstrip("\n")
    text += ("\n" + json.dumps({"type": "assistant",
                                "timestamp": "2026-09-10T22:30:00.000Z",
                                "message": {"role": "assistant",
                                            "model": "claude-opus-5"}}))
    p.write_text(text + "\n", encoding="utf-8")
    return p


# --- proof (a): the real-shaped drift FAILS, naming the cause -------------


def test_seat_model_drift_fails_naming_live_row_first_turn_and_fallback(tmp_path):
    """(a) The fixture built from the REAL gen VII transcript makes the check
    FAIL, naming seat, live model, row model, the first drifted-turn timestamp
    20:46:21Z and requestId req_011CevQvLvpbLcLv2GE49WA4."""
    groot = tmp_path / ".agi"
    _make_seats_node(groot, [DRIFT_SEAT_ROW])
    _make_pin(groot, "sanctuary-director", FIXTURE)

    r = verification.check_seat_model(groot)
    assert r.status == "FAIL", r.note
    assert "sanctuary-director" in r.note
    assert "live=claude-opus-4-8" in r.note
    assert "row=claude-opus-5" in r.note
    assert "20:46:21" in r.note, "must name the first drifted-turn timestamp"
    assert "20:46:09" in r.note, "must name the fallback event timestamp"
    assert "cyber" in r.note, "must name the fallback category"
    assert "req_011CevQvLvpbLcLv2GE49WA4" in r.note, "must name the requestId"
    assert r.number["drifted"] == 1


# --- proof (b): restoring the model on a later turn clears the drift --------


def test_seat_model_restored_later_clears_drift(tmp_path):
    """(b) The same fixture with the model restored on a later turn clears the
    drift: the check PASSES because the newest turn matches the row again."""
    groot = tmp_path / ".agi"
    _make_seats_node(groot, [DRIFT_SEAT_ROW])
    _make_pin(groot, "sanctuary-director", _restored_transcript(tmp_path))

    r = verification.check_seat_model(groot)
    assert r.status == "PASS", r.note
    assert "model=claude-opus-5" in r.note
    assert "row=claude-opus-5" in r.note
    assert r.number["drifted"] == 0


# --- proof (c): a no-drift transcript passes with model=row -----------------


def test_seat_model_no_drift_passes(tmp_path):
    """(c) A transcript with no drift prints model=row and the check passes."""
    groot = tmp_path / ".agi"
    _make_seats_node(groot, [DRIFT_SEAT_ROW])
    _make_pin(groot, "sanctuary-director", _no_drift_transcript(tmp_path))

    r = verification.check_seat_model(groot)
    assert r.status == "PASS", r.note
    assert "model=claude-opus-5" in r.note
    assert "row=claude-opus-5" in r.note


# --- the HARD RULES: skip, don't guess, don't repair -----------------------


def test_seat_without_session_ref_is_skipped_silently(tmp_path):
    """A config:seats row with no session_ref is NEVER checked — not opened as
    'newest file in a directory', not an error. (No pin is written for it and
    the check must not look one up.)"""
    groot = tmp_path / ".agi"
    row = ("name: policy-master, role: director, model: claude-sonnet-5, "
           "session_ref: ''")
    _make_seats_node(groot, [row])
    r = verification.check_seat_model(groot)
    assert r.status == "PASS", r.note
    assert r.number["seats"] == 0
    assert r.number.get("skipped", 0) == 0, "no session_ref = not a candidate"


def test_seat_with_pin_to_missing_transcript_is_skipped_not_failed(tmp_path):
    """A row with a session_ref whose pin does not resolve to an existing
    transcript is skipped silently — the check must not open a transcript it
    cannot map to a row (trap 0c / the hypothesis HARD RULE)."""
    groot = tmp_path / ".agi"
    _make_seats_node(groot, [DRIFT_SEAT_ROW])
    _make_pin(groot, "sanctuary-director",
              tmp_path / "does-not-exist.jsonl")
    r = verification.check_seat_model(groot)
    assert r.status == "PASS", r.note
    assert r.number["skipped"] == 1


def test_no_seated_rows_is_a_pass_that_says_so(tmp_path):
    """An empty or absent seat registry is a PASS with no seats to check —
    not a failure (the check guards seats, it does not gate on them)."""
    groot = tmp_path / ".agi"
    r = verification.check_seat_model(groot)
    assert r.status == "PASS", r.note
    assert "no seated rows" in r.note
    assert r.number["seats"] == 0


# --- wiring: the check rides the run verify path ---------------------------


def test_seat_model_runs_in_rotation_and_full_levels(monkeypatch, tmp_path):
    """`verify` (verification.py) carries the seat-model check in its rotation
    and full rounds. run_level appends it exactly there — before the closing
    node-count compare."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    seen: list[str] = []

    def fake_run(groot, name, verbose):
        seen.append(name)
        return verification.CheckResult(name, "PASS", 0.0, None)

    monkeypatch.setattr(verification, "run_check", fake_run)
    monkeypatch.setattr(verification, "check_seat_model",
                        lambda g: verification.CheckResult(
                            "seat-model", "PASS", 0.0, None))
    results = verification.run_level(groot, "rotation", suite=False, verbose=False)
    assert "seat-model" in [r.name for r in results]
    assert results[-1].name == "node-count", "node-count stays the closing check"
    # and it is NOT in the quick pre-commit set
    results_q = verification.run_level(groot, "quick", suite=False, verbose=False)
    assert "seat-model" not in [r.name for r in results_q]