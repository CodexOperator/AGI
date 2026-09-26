"""Conjunct (2) of hypothesis:pin-reap-never-names-a-live-session-and-a-
reap-leaves-no-stale-app-session — the LATE s12 WAIT IS BOUNDED.

`_late_reap_for_skipped` used to return `waiting` with no age bound, so a
pre-reboot window whose successor never registers was waited on forever, one
log line per pass. Now the bound is `reaper.late_reap_wait_max_s` (a declared
config cell; the code default is only the resolver for a missing cell) and
past it the record is closed `abandoned` with exactly ONE log line.

Fixtures only: fixture graph root, fixture registry dir, fixture window-path
file. No real pane, pid, unit, crontab or `~/.claude/sessions`.
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
rot = _load("rotate")


@pytest.fixture
def graph(tmp_path: Path) -> Path:
    g = tmp_path / "repo" / ".agi"
    g.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    return g


def _rec(seat="belam", recorded_at="2026-09-26T00:00:00Z"):
    return {
        "rotation": "rotate-self",
        "seat": seat,
        "recorded_at": recorded_at,
        "result": "skipped",
        "refusal_reason": "registry file for @6 not found in X within the "
                          "bounded join poll",
        "handover": {"own_window": {"name": "belam-S1-L4-V", "id": "@5"},
                     "successor_window": {"name": "belam-S1-L4-VI",
                                          "id": "@6"}},
    }


def _rec_path(tmp_path, rec):
    p = tmp_path / "belam.t1.json"
    p.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    return p


def _now(offset_s: float) -> float:
    return datetime.datetime(2026, 9, 26, 0, 0, 0,
                             tzinfo=datetime.timezone.utc).timestamp() + offset_s


def _wait(graph, rec, now, *, record_path=None):
    """One waiting-branch call with NO successor registry anywhere."""
    return heal._late_reap_for_skipped(
        graph, rec, record_path=record_path,
        rows=[{"name": rec["seat"], "role": "director", "pid": 31337}],
        tmux_session="", window_path=None,
        registry_dir=str((record_path.parent if record_path
                          else Path("/nope")) / "no-such-registry"),
        pids_for=lambda n: [1], rot=rot, now=now)


# (a) under the bound -> still waiting, no close, no write
def test_under_bound_still_waiting(graph, tmp_path):
    rec = _rec()
    out = _wait(graph, rec, _now(60.0))
    assert out["action"] == "waiting", out
    assert out["waited_s"] == 60.0 and out["bound_s"] == 1800.0, out
    assert "s12_self_reap" not in rec, "no close under the bound"


# (b) past the bound -> abandoned, one write, one shape
def test_past_bound_closed_abandoned(graph, tmp_path):
    rec = _rec()
    p = _rec_path(tmp_path, rec)
    out = _wait(graph, rec, _now(7200.0), record_path=p)
    assert out["action"] == "abandoned" and out["already"] is False, out
    doc = json.loads(p.read_text())
    sr = doc["s12_self_reap"]
    assert sr["state"] == "abandoned" and sr["performer"] == "watch"
    assert sr["bound_s"] == 1800.0 and sr["waited_s"] == 7200.0, sr
    assert sr["successor_id"] == "@6", sr


# (c) twice -> still abandoned, still ONE line (driver level)
def test_second_pass_no_second_line(graph, tmp_path, monkeypatch):
    lines = []
    monkeypatch.setattr(heal, "_watch_log", lines.append)
    # an OLD record: the driver reads the wall clock itself
    rec = _rec(recorded_at="2020-01-01T00:00:00Z")
    rot_dir = rot._rotations_dir(graph)
    rot_dir.mkdir(parents=True, exist_ok=True)
    (rot_dir / "belam.t1.json").write_text(json.dumps(rec) + "\n")
    reg = tmp_path / "nope-reg"
    for _ in range(2):
        heal._late_reap_skipped_pass(
            graph, registry_dir=str(reg), rot=rot,
            pids_for=lambda n: [1], loadavg=lambda: (0.0, 0.0, 0.0))
    abandoned = [ln for ln in lines if "ABANDONED" in ln]
    waiting = [ln for ln in lines if "still absent" in ln and "ABANDONED" not in ln]
    assert len(abandoned) == 1, lines
    assert "1800" in abandoned[0] and "@6" in abandoned[0], abandoned
    assert waiting == [], "the per-pass waiting line must stop once abandoned"
    doc = json.loads((rot_dir / "belam.t1.json").read_text())
    assert doc["s12_self_reap"]["state"] == "abandoned"
    # a third direct call reports already-closed, and writes nothing new
    out = _wait(graph, doc, _now(9000.0),
                record_path=rot_dir / "belam.t1.json")
    assert out["action"] == "abandoned" and out["already"] is True, out


# (d) the bound cell ABSENT -> the code default applies, no raise
def test_absent_bound_cell_uses_code_default(graph, tmp_path):
    cfg = graph / "config.json"
    assert "late_reap_wait_max_s" not in cfg.read_text()
    rec = _rec()
    out = _wait(graph, rec, _now(10.0))
    assert out["action"] == "waiting" and out["bound_s"] == 1800.0, out
    # ...and a DECLARED cell is honoured (declared, not literal)
    cfg.write_text(json.dumps({"reaper": {"late_reap_wait_max_s": 30}}))
    assert _wait(graph, rec, _now(60.0))["action"] == "abandoned"
    # a malformed cell must not raise either
    cfg.write_text(json.dumps({"reaper": {"late_reap_wait_max_s": "soon"}}))
    assert _wait(graph, rec, _now(60.0))["bound_s"] == 1800.0


# CONJUNCT A (hypothesis:heal-late-reap-bound-covers-an-unparsable-record-
# and-stale-pin-logs-once). The test below USED TO assert the UNBOUNDED wait
# was correct — that was a test of the gap, not of the product. The contract
# is now: a record whose recorded_at will not parse is aged from a PERSISTED
# first-seen stamp, so it CLOSES past the declared bound like any other.
LATE_REAP_SEEN = "late-reap-first-seen.json"


def _state_file(graph: Path) -> Path:
    return heal._reaper_state_file(graph, LATE_REAP_SEEN)


def test_unparsable_recorded_at_is_bounded_not_unbounded(graph, tmp_path):
    rec = _rec(recorded_at="")            # unparsable
    p = _rec_path(tmp_path, rec)
    first = _wait(graph, rec, _now(60.0), record_path=p)
    assert first["action"] == "waiting", first
    assert first["ts_source"] in ("mtime", "first-pass"), first
    # the stamp is PERSISTED, not `now` re-read every pass
    assert _state_file(graph).is_file(), "no persisted first-seen stamp"
    second = _wait(graph, rec, _now(960.0), record_path=p)
    assert second["ts_source"] == "first-seen", second
    # ...and the wait ACCUMULATES (900s, not a reset 0) and crosses the bound
    assert second["waited_s"] >= 900.0, second
    third = _wait(graph, rec, _now(3660.0), record_path=p)
    assert third["action"] == "abandoned" and third["waited_s"] > 1800.0, third
    doc = json.loads(p.read_text())
    assert doc["s12_self_reap"]["state"] == "abandoned", doc
    # the next pass is the existing idempotence guard, nothing re-closes
    assert _wait(graph, doc, _now(7200.0), record_path=p)["already"] is True


def test_unparsable_recorded_at_bounded_across_processes(graph, tmp_path,
                                                         monkeypatch):
    """The stamp lives on DISK, not in module memory: a FRESH interpreter
    keeps accumulating the wait (the probe the parent runs)."""
    rec = _rec(recorded_at="not a timestamp")
    p = _rec_path(tmp_path, rec)
    first = _wait(graph, rec, _now(10.0), record_path=p)
    assert first["action"] == "waiting", first
    import subprocess  # noqa: PLC0415
    script = (
        "import json, sys, datetime, rotate, heal\n"
        "from pathlib import Path\n"
        "g, p = Path(sys.argv[1]), Path(sys.argv[2])\n"
        "rec = json.loads(p.read_text())\n"
        "now = datetime.datetime(2026, 9, 26, tzinfo=datetime.timezone.utc)"
        ".timestamp() + 960.0\n"
        "o = heal._late_reap_for_skipped(g, rec, record_path=p,"
        " rows=[{'name': 'belam', 'role': 'director', 'pid': 1}],"
        " tmux_session='', window_path=None,"
        " registry_dir=str(p.parent / 'nope'), pids_for=lambda n: [1],"
        " rot=rotate, now=now)\n"
        "print(json.dumps(o))\n"
    )
    env = dict(os.environ, PYTHONPATH=str(BIN))
    out = subprocess.run([sys.executable, "-c", script, str(graph), str(p)],
                         capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stderr
    got = json.loads(out.stdout.strip().splitlines()[-1])
    assert got["action"] == "waiting", got
    assert got["ts_source"] == "first-seen" and got["waited_s"] > 900.0, got
