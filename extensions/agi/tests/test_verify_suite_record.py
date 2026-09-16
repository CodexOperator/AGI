"""Conjunct 4 of hypothesis:l4-the-full-suite-runs-under-600-s-solo-real-waits
-and-process-reaps-are-seamed-not-slept: `verification.py --suite` records the
wall time and the slowest-15 table beside `suite_ran_at`.

Four edges, one file:

1. The SUITE argv gains `--durations=15` and ONLY the suite argv does.
2. The table is parsed from pytest's own output into test+seconds rows.
3. No table -> `[]` recorded, never an invented one (the honesty gate).
4. The record MERGES over the existing keys the way `ring_decision` already
   does: one record, no second ledger, and a caller that names no wall time
   never erases one that is already there.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import commands  # noqa: E402
import verification  # noqa: E402

TABLE = (
    "============================= slowest 15 durations "
    "=============================\n"
    "20.00s call     extensions/agi/tests/test_rotation_alerts.py::test_slow\n"
    "0.02s setup    extensions/agi/tests/test_x.py::test_fast\n"
    "0.01s teardown extensions/agi/tests/test_x.py::test_fast\n"
    "12 passed in 519.42s\n"
)


def _stub_suite(monkeypatch, body: str, seen: dict):
    """Point `commands.load` at a suite command that prints `body`, and
    record the argv `run_check` actually executed."""
    real_run = verification.subprocess.run

    def spy(argv, **kw):
        seen["argv"] = list(argv)
        return real_run(argv, **kw)

    monkeypatch.setattr(verification.subprocess, "run", spy)
    monkeypatch.setattr(
        verification.commands, "load",
        lambda root: {"tests": commands.Command(
            name="tests", argv=[sys.executable, "-c", body], raw_argv=[])})


def test_suite_argv_gains_durations_and_parses_the_table(tmp_path, monkeypatch):
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    seen: dict = {}
    _stub_suite(monkeypatch, "print(%r)" % TABLE, seen)
    r = verification.run_check(groot, "tests", verbose=False)
    assert seen["argv"][-1] == "--durations=15", seen["argv"]
    assert r.durations == [
        {"test": "extensions/agi/tests/test_rotation_alerts.py::test_slow",
         "seconds": 20.0},
        {"test": "extensions/agi/tests/test_x.py::test_fast", "seconds": 0.02},
        {"test": "extensions/agi/tests/test_x.py::test_fast", "seconds": 0.01},
    ]
    assert r.elapsed > 0  # the wall time IS this check's own .seconds


def test_no_durations_table_records_empty_never_invented(tmp_path, monkeypatch):
    """The falsifier: a passing run whose output carries no table must not
    fabricate one."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    seen: dict = {}
    _stub_suite(monkeypatch, "print('12 passed in 3.21s')", seen)
    r = verification.run_check(groot, "tests", verbose=False)
    assert r.status == "PASS"
    assert r.durations == []


def test_non_suite_check_argv_untouched(tmp_path, monkeypatch):
    """Only the suite asks for the table: another check's argv is verbatim."""
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True)
    seen: dict = {}
    real_run = verification.subprocess.run
    monkeypatch.setattr(verification.subprocess, "run",
                        lambda argv, **kw: (seen.__setitem__("argv", list(argv)),
                                            real_run(argv, **kw))[1])
    monkeypatch.setattr(
        verification.commands, "load",
        lambda root: {"links": commands.Command(
            name="links", argv=[sys.executable, "-c", "print('ok')"],
            raw_argv=[])})
    verification.run_check(groot, "links", verbose=False)
    assert "--durations=15" not in seen["argv"]


def test_record_merges_wall_and_slowest_beside_ts(tmp_path):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    verification._record_suite_ts(groot, {"ring": "suite-grant"})
    verification._record_suite_ts(
        groot, None, wall_s=519.42,
        slowest_15=[{"test": "t", "seconds": 20.0}])
    doc = json.loads((groot / "sessions" / verification.SUITE_TS_FILE)
                     .read_text(encoding="utf-8"))
    assert "suite_ran_at" in doc
    assert doc["suite_wall_s"] == 519.42
    assert doc["slowest_15"] == [{"test": "t", "seconds": 20.0}]
    assert doc["ring_decision"] == {"ring": "suite-grant"}  # merged, not lost


def test_record_without_wall_leaves_the_prior_one(tmp_path):
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    verification._record_suite_ts(groot, None, wall_s=100.0, slowest_15=[])
    verification._record_suite_ts(groot)  # a caller that ran no suite
    doc = json.loads((groot / "sessions" / verification.SUITE_TS_FILE)
                     .read_text(encoding="utf-8"))
    assert doc["suite_wall_s"] == 100.0
    assert doc["slowest_15"] == []
