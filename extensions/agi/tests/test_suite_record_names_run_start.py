"""The suite record names the RUN START, never the write time
(hypothesis:l4-the-suite-record-names-the-run-start-never-the-write-time).

Four edges, one file:

1. main() captures the wall clock and `rev-parse HEAD` BEFORE pytest launches
   and the record carries them as `suite_ran_at` / `suite_ran_on` -- never the
   write time or the HEAD at write time.
2. A bin/*.py touched BETWEEN start and end FAILS `bin-suite-fresh` afterward.
3. An explicit `--stamp` whose HEAD moved past the run refuses by name.
4. The window line prints `ran on <sha>` beside the stamped sha.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402


def _mk_bin(tmp_path: Path, names: list[str]) -> Path:
    bdir = tmp_path / "bin"
    bdir.mkdir(parents=True, exist_ok=True)
    for n in names:
        (bdir / n).write_text("x = 1\n", encoding="utf-8")
    return bdir


def test_main_records_the_run_start_not_the_write_time(tmp_path, monkeypatch):
    """(1) The fake runner's HEAD does not change: the record's `suite_ran_at`
    is the captured start time and `suite_ran_on` is the start sha."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    monkeypatch.setattr(verification.locations, "find_project_root",
                        lambda p: groot)
    monkeypatch.setattr(verification.commands, "engine_for",
                        lambda g: str(groot))
    monkeypatch.setattr(verification, "_suite_lock_guard", lambda g: None)
    monkeypatch.setattr(verification, "_git", lambda g, a: "abc123")
    seen: dict = {}
    monkeypatch.setattr(verification, "run_level",
                        lambda *a, **k: seen.update(k) or [])
    before = time.time()
    assert verification.main(["--suite", "--root", str(tmp_path)]) == 0
    after = time.time()
    assert seen["run_ts"] is not None and before <= seen["run_ts"] <= after, seen
    assert seen["run_sha"] == "abc123", seen
    doc = json.loads((groot / "sessions"
                      / verification.SUITE_TS_FILE).read_text(encoding="utf-8"))
    assert doc["suite_ran_on"] == "abc123"
    assert doc["suite_ran_at"] == seen["run_ts"]


def test_bin_touched_mid_run_fails_freshness_afterward(tmp_path, monkeypatch):
    """(2) The falsifier this round kills: a bin/*.py whose mtime lands AFTER
    the run started must FAIL `bin-suite-fresh`, even though the suite passed."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    bdir = _mk_bin(tmp_path, ["touched.py"])
    start = time.time() - 60.0
    os.utime(bdir / "touched.py", (start + 30.0, start + 30.0))  # mid-run
    real = verification.check_bin_freshness
    seen: dict = {}

    def fake_run(groot, name, verbose):
        if name == verification.SUITE_CMD:
            return verification.CheckResult(verification.SUITE_CMD, "PASS",
                                            5.0, {"passed": 1})
        return verification.CheckResult(name, "PASS", 0.0, None)

    def spy(groot, **kw):
        seen.update(kw)
        return real(groot, bin_dir=bdir, tracked_of=lambda d: {"touched.py"},
                    **kw)

    monkeypatch.setattr(verification, "run_check", fake_run)
    monkeypatch.setattr(verification, "check_bin_freshness", spy)
    results = verification.run_level(groot, "rotation", suite=True,
                                     verbose=False, run_ts=start)
    fresh = next(r for r in results if r.name == "bin-suite-fresh")
    assert seen.get("effective_ts") == start, seen
    assert fresh.status == "FAIL", fresh.note
    assert "SUITE REQUIRED" in fresh.note and "touched.py" in fresh.note


def test_stamp_refuses_when_head_moved_mid_run(tmp_path, monkeypatch):
    """(3) `--stamp` names the movement instead of recording a HEAD the run
    never executed; an unmoved HEAD still stamps the run sha."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    monkeypatch.setattr(verification, "_git", lambda g, a: "moved999")
    monkeypatch.setattr(verification, "_node_dirt", lambda g: [])
    r = verification.compare_count(groot, {"active": 5}, stamp=True,
                                   run_sha="start111")
    assert r.status == "FAIL", r.note
    assert "HEAD moved999 moved past the run start111: re-run" in r.note
    # unmoved HEAD: stamps the run's own sha, no refusal
    monkeypatch.setattr(verification, "_git", lambda g, a: "same111")
    ok = verification.compare_count(groot, {"active": 5}, stamp=True,
                                    run_sha="same111")
    assert ok.status == "PASS", ok.note
    assert "same111" in ok.note


def test_live_stamp_names_the_recorded_run_not_the_invocation_start(
        tmp_path, monkeypatch, capsys):
    """(2) at the LIVE `--stamp` call site the refusal names the sha the SUITE
    ran on. An invocation that runs no pytest (the merge-up step) has its own
    start sha == HEAD, so only the RECORD can see the movement. HEAD shaB vs
    record shaA: FAIL by name, baseline untouched; HEAD shaA: PASS, stamps
    shaA."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    monkeypatch.setattr(verification.locations, "find_project_root",
                        lambda p: groot)
    monkeypatch.setattr(verification.commands, "engine_for", lambda g: str(groot))
    monkeypatch.setattr(verification, "_suite_lock_guard", lambda g: None)
    monkeypatch.setattr(verification, "_node_dirt", lambda g: [])
    monkeypatch.setattr(verification, "check_seat_model",
                        lambda g: verification.CheckResult(
                            "seat-model", "PASS", 0.0, None))

    def fake_run_check(g, name, verbose):
        if name == "smoke":
            return verification.CheckResult(
                "smoke", "PASS", 0.0,
                {"active": 7, "deprecated": 0, "total": 7})
        return verification.CheckResult(name, "PASS", 0.0, None)

    monkeypatch.setattr(verification, "run_check", fake_run_check)
    verification._record_suite_ts(groot, ran_at=1.0, ran_on="shaA")
    state_p = groot / "sessions" / verification.STATE_FILE
    state_p.write_text(json.dumps({
        "active": 7, "deprecated": 0, "total": 7, "sha": "baseline0",
        "stamped_at": 1.0, "reason": "kept"}), encoding="utf-8")

    # HEAD has moved past the run the suite record names: REFUSE BY NAME.
    monkeypatch.setattr(verification, "_git", lambda g, a: "shaB")
    rc = verification.main(["--level", "quick", "--stamp",
                            "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc != 0
    assert "HEAD shaB moved past the run shaA: re-run" in out
    assert json.loads(state_p.read_text())["sha"] == "baseline0", (
        "the baseline was re-stamped on a HEAD the recorded suite never ran on")

    # HEAD IS the recorded run: PASS, and the stamp names shaA.
    monkeypatch.setattr(verification, "_git", lambda g, a: "shaA")
    rc = verification.main(["--level", "quick", "--stamp",
                            "--root", str(tmp_path)])
    assert rc == 0, capsys.readouterr().out
    assert json.loads(state_p.read_text())["sha"] == "shaA"


def test_window_prints_the_sha_the_suite_ran_on(tmp_path):
    """(4) `ran on <sha>` beside the stamped sha."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    verification._record_suite_ts(groot, ran_at=1.0, ran_on="deadbee")
    (groot / "sessions" / verification.STATE_FILE).write_text(json.dumps({
        "active": 1, "deprecated": 0, "total": 1, "sha": "cafef00d",
        "stamped_at": time.time(), "reason": "kept",
    }), encoding="utf-8")
    out = verification.render_window(groot)
    assert "baseline:" in out
    assert "stamped sha=cafef00d" in out
    assert "ran on deadbee" in out
