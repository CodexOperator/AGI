"""Tests for hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
(kid 1 of 2: DETECT + CLASSIFY + RECORD).

The FIXTURE rows + a fake process table (`pid_alive`) + a fake window list
(AGI_WINDOW_PATH seam) + fake log tails never touch the live seats row. A seat
is DEAD only when ALL of: (1a) pid gone, (1b) window @id absent, (1c) no
window named for the seat, (1d) no rotation `started` in the last 10 min. The
pass NAMES a dead seat once (stderr + watch log) and writes exactly ONE
`crash-recovery` rotation record with a `probable_cause` from the seat-log tail
signature table — the record is ALSO the once-guard, so a second pass does
nothing. A `recover: false` row is NAMED but never recorded.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
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


@pytest.fixture
def graph(tmp_path: Path) -> Path:
    """A fixture graph root whose seats row + sessions dir are all ours."""
    g = tmp_path / "repo" / ".agi"
    g.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    (g / "sessions").mkdir(parents=True, exist_ok=True)
    return g


def _write_seats(graph: Path, rows: list[dict]) -> None:
    p = graph / "nodes" / ".geometry" / "seats.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "seats:"]
    for r in rows:
        lines.append("  - " + json.dumps(r))
    lines.append("---")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_log(graph: Path, seat: str, text: str) -> Path:
    p = graph / "sessions" / f"{seat}.log"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _rotations(graph: Path) -> Path:
    r = graph / "sessions" / "rotations"
    r.mkdir(parents=True, exist_ok=True)
    return r


def _write_record(graph: Path, seat: str, rec: dict, stamp: str) -> Path:
    p = _rotations(graph) / f"{seat}.{stamp}.json"
    p.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return p


def _crash_records(graph: Path, seat: str) -> list[Path]:
    return sorted(_rotations(graph).glob(f"{seat}.*.json")) if _rotations(graph).exists() else []


def _fake_launcher(records: list, pid: int = 424242,
                   window: str = "@556"):
    """A fake recover launcher seam: records what would be spawned and
    reports the successor landed (a positive pid + a window @id) without ever
    spawning a real model or touching real tmux."""
    def launch(root, name, shell_cmd, window_path=None):
        records.append({"name": name, "cmd": (shell_cmd or "")[:80],
                        "pid": pid, "window": window})
        return pid, window
    return launch


def _scan(graph: Path, *, dead: bool = True, wp: str | None = None,
          window_names=("", ""), launcher=None, records=None) -> list[dict]:
    """Run one seat-dead scan with a poked process table, a fake window list
    and (by default) a fake launcher so a detected dead seat is RESPAWNED
    through the seam. `dead=True` -> every pid is gone; `dead=False` -> every
    pid alive."""
    wf = Path(wp) if wp else graph / "windows.txt"
    if not wp:
        wf.write_text("\n".join(window_names) + "\n")
    if launcher is None:
        recs = records if records is not None else []
        launcher = _fake_launcher(recs)
    return heal._watch_seats(graph, pid_alive=(lambda pid: not dead),
                             window_path=str(wf), launcher=launcher)


def _seats_md(graph: Path) -> Path:
    return graph / "nodes" / ".geometry" / "seats.md"


# --- detection --------------------------------------------------------------

def test_dead_seat_one_naming_one_record_with_cause(graph, capsys):
    """A single dead seat (pid gone + no window) -> exactly ONE naming on
    stderr + in the watch log, ONE crash-recovery record carrying the
    probable_cause from the seat log tail AND the respawn outcome (kid 2:
    recovery is a respawn, and the record states that it happened)."""
    logp = graph / "reaper.log"
    os.environ["AGI_REAPER_LOG"] = str(logp)
    _write_seats(graph, [{"name": "seat-a", "role": "director",
                          "model": "claude-opus-5", "pid": 999999,
                          "window": "@50", "generation": 3}])
    _write_log(graph, "seat-a", "line1\nuds shutdown\nline3\n")
    spawns: list = []

    acted = _scan(graph, dead=True, records=spawns,
                  window_names=("", "@1 other"))

    assert len(acted) == 1
    assert acted[0]["seat"] == "seat-a"
    assert acted[0]["recorded"] is True
    assert acted[0]["respawned"] is True
    assert len(spawns) == 1 and spawns[0]["name"] == "seat-a"
    err = capsys.readouterr().err
    assert "DEAD seat seat-a" in err
    assert "probable_cause=" in err
    assert "role=director" in err and "model=claude-opus-5" in err

    recs = _crash_records(graph, "seat-a")
    assert len(recs) == 1, "exactly one crash-recovery record"
    rec = json.loads(recs[0].read_text())
    assert rec["rotation"] == "crash-recovery"
    assert rec["seat"] == "seat-a"
    assert rec["result"] == "respawned", \
        "the record states the respawn happened (kid 2 outcome guard)"
    assert rec["probable_cause"] == "idle-external-teardown"
    assert rec["row"]["pid"] == 999999
    assert rec["respawn_outcome"]["name"] == "seat-a"
    assert rec["respawn_outcome"]["generation"] == 4, \
        "plain-seat generation advances one past the row's 3"

    ltext = logp.read_text()
    assert ltext.count("DEAD seat seat-a") == 1, "named ONCE in watch log"
    assert "crash-recovery" in ltext


def test_alive_seat_nothing(graph):
    """A live pid is never touched: no naming, no record."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242,
                          "window": "@50"}])
    acted = _scan(graph, dead=False, window_names=("", "@50"))
    assert acted == []
    assert _crash_records(graph, "seat-a") == []


def test_corpse_detected_with_predecessor_windows_open(graph):
    """(1c) DELETED (prime XI ruling 2026-09-11 19:38Z: a tmux window NAME is
    not an address). The falsifier: the row's @id is gone and windows NAMED
    for the seat — a numeral-chain seat's idle predecessor chain, an owner
    standing rule, never killed — are still open -> the corpse IS detected.
    On the round's bytes this read `nothing` forever for any chain seat."""
    _write_seats(graph, [{"name": "belam", "pid": 424242, "window": "@289",
                          "role": "prime_director"}])
    acted = _scan(graph, dead=True,
                  window_names=("@244 belam-S1-L4-V", "@247 belam-S1-L4-VI",
                                "@272 belam-S1-L4-VIII", "@277 belam-S1-L4-IX",
                                "@1 other"))
    assert len(acted) == 1, "a corpse behind open predecessor windows is DEAD"


def test_row_window_id_present_nothing(graph):
    """(1b) the row's own window @id is still in tmux -> nothing."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242,
                          "window": "@50"}])
    acted = _scan(graph, dead=True, window_names=("", "@50"))
    assert acted == []


def test_rotation_started_3min_ago_nothing(graph):
    """(1d) a `started` rotation record within 10 min means in-flight, not a
    crash -> nothing."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242,
                          "window": "@50"}])
    _write_record(
        graph, "seat-a",
        {"rotation": "rotate-self", "seat": "seat-a", "result": "started",
         "recorded_at": time.strftime(
             "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 180)),
         "steps_reached": ["spawn"]},
        time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() - 180)))
    acted = _scan(graph, dead=True, window_names=("", "@1 other"))
    assert acted == []


def test_old_started_rotation_is_no_guard(graph):
    """A `started` rotation record OLDER than 10 min is not in flight ->
        the seat can still be declared dead."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242,
                          "window": "@50"}])
    _write_record(
        graph, "seat-a",
        {"rotation": "rotate-self", "seat": "seat-a", "result": "started",
         "recorded_at": time.strftime(
             "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 3600)),
         "steps_reached": ["spawn"]},
        time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() - 3600)))
    acted = _scan(graph, dead=True, window_names=("", "@1 other"))
    assert len(acted) == 1


def test_recover_false_named_no_record(graph):
    """`recover: false` -> NAMED (it is dead and the loop must know) but never
    recorded as a crash-recovery action."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242,
                          "window": "@50", "recover": False}])
    acted = _scan(graph, dead=True, window_names=("", "@1 other"))
    assert len(acted) == 1
    assert acted[0]["recorded"] is False
    assert _crash_records(graph, "seat-a") == [], "no record for recover:false"


def test_second_pass_nothing(graph):
    """The crash-recovery record is the once-guard: a second scan over the
    same dead row must not re-name or re-record."""
    _write_seats(graph, [{"name": "seat-a", "pid": 424242,
                          "window": "@50"}])
    _scan(graph, dead=True, window_names=("", "@1 other"))
    second = _scan(graph, dead=True, window_names=("", "@1 other"))
    assert second == []
    assert len(_crash_records(graph, "seat-a")) == 1


def test_dead_seat_end_to_end_through_watch(graph, monkeypatch, capsys):
    """One real `heal.py watch --once` pass (the whole `_watch` loop) drives
    the seat-dead scan: dead seat RESPAWNED through a fake launcher seam +
    recorded; live seat untouched."""
    logp = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(logp))
    monkeypatch.setenv("AGI_WINDOW_PATH", str(graph / "windows.txt"))
    _write_seats(graph, [
        {"name": "dead-a", "pid": 424242, "window": "@50"},
        {"name": "live-b", "pid": 424243, "window": "@51"},
    ])
    (graph / "windows.txt").write_text("", encoding="utf-8")
    spawns: list = []
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: pid == 424243)
    monkeypatch.setattr(heal, "_launch_recovered",
                        _fake_launcher(spawns, pid=777111, window="@912"))
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph), "--once"])
    assert heal.main() == 0
    assert len(spawns) == 1, "exactly one successor launched (dead-a only)"
    assert spawns[0]["name"] == "dead-a"
    recs = _crash_records(graph, "dead-a")
    assert len(recs) == 1
    rec = json.loads(recs[0].read_text())
    assert rec["result"] == "respawned"
    assert _crash_records(graph, "live-b") == []
    assert "DEAD seat dead-a" in capsys.readouterr().err


# --- classification ---------------------------------------------------------

def test_classify_pane_local_pytest_reap():
    tail = "running test_probe_postjoin.py ...\ncmd_rotate_self called no seam\n"
    assert heal._classify_death(tail) == "pane-local-pytest-reap"


def test_classify_idle_external_teardown_variants():
    for tail in ("...uds shutdown...\n",
                 "Epoch mismatch (409, session_not_active)\n",
                 "updatePidFile: [Errno 2] No such file\n"):
        assert heal._classify_death(tail) == "idle-external-teardown"


def test_classify_remote_control_disconnect():
    assert heal._classify_death("remote-control connection closed after read\n") \
        == "remote-control-disconnect"
    assert heal._classify_death("disconnect requested by peer\n") \
        == "remote-control-disconnect"


def test_classify_unknown_tail():
    assert heal._classify_death("some unrelated line\nanother line\n") \
        == "unknown"


def test_classify_pytest_needs_probe_marker():
    # cmd_rotate_self WITHOUT a pytest probe marker is NOT pane-local-pytest —
    # a normal seat's own rotate logs cmd_rotate_self all the time.
    tail = "cmd_rotate_self completed\n"
    assert heal._classify_death(tail) == "unknown"


# --- worktree live-first row ------------------------------------------------

def test_worktree_seat_read_live_first(graph):
    """A worktree seat's row is re-read live-first from the worktree's own
    geometry: the worktree copy's pid is what detection sees, not MAIN's."""
    wt = graph / "worktrees" / "seat-wt" / ".agi"
    _write_seats(graph, [{"name": "wt", "pid": 424242, "window": "@50",
                          "worktree": ".agi/worktrees/seat-wt"}])
    # worktree's own copy: a DIFFERENT (dead) pid -> wt is dead.
    _write_seats(wt, [{"name": "wt", "pid": 987654, "window": "@50",
                       "worktree": ".agi/worktrees/seat-wt"}])
    acted = _scan(graph, dead=True, window_names=("", "@1 other"))
    assert len(acted) == 1
    rec = json.loads(_crash_records(graph, "wt")[0].read_text())
    assert rec["row"]["pid"] == 987654, "the live-first worktree row won"