"""goal:g7.31.2.1 — seat-start occupation against REAL tmux, not a seam.

hypothesis:a00-4c8d9dd8-6f89c2.

Every DH.17/DH.26 test feeds `window_path` a STUB file; the parent's own
caveat says so: "no live tmux was ever read". This file removes that seam. It
creates a throwaway tmux session (unique name, killed in teardown), names a
window for the seat, and calls `rotate._successor_window_id` /
`seat_status.seat_occupation` / `seat_status.pane_coherent` with
`window_path=None`, so they run `/usr/bin/tmux` itself.

It ALSO settles the SESSION half of the falsifier: what session identity the
registry row carries at a spawn-only seat start. The result, measured here:
the only tmux-matching cell at seat start is `window` (the pane @id). The
"session pin" cells (`session_ref`/`session_name`) are empty by design at
spawn and back-filled later by `rotate.py ack`; `session_id` is the harness
session uuid, filled from the registry JOIN — never from tmux. No cell
carries the tmux SESSION name at all.

Skips cleanly when tmux is absent.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
from agi.bin import rotate  # noqa: E402
from agi.tests.test_seat_pane_registry import _graph, _row  # noqa: E402
import seat_status as SS  # noqa: E402

TMUX = shutil.which("tmux")
pytestmark = pytest.mark.skipif(TMUX is None, reason="tmux binary absent")

#: The TRUE subprocess.run, captured at import time -- before the project-wide
#: autouse `_no_real_tmux` guard (conftest.py) replaces `subprocess.run` at
#: test setup. Module-level code runs at collection, so this is the real one.
_REAL_RUN = subprocess.run

SEAT = "director-seat"
#: Deliberately the LIVE pytest process: the positive occupation test runs the
#: REAL rotate._pid_alive alive branch against an actually-alive pid.
_LIVE_PID = os.getpid()
#: The tmux session name is a SPAWN parameter, never a registry cell. The
#: settlement test asserts it does not appear in the row.
TMP_SESSION_PREFIX = "agi-rtt"


@pytest.fixture(autouse=True)
def _allow_real_tmux_for_our_throwaway_session(monkeypatch):
    """conftest's `_no_real_tmux` answers EVERY `tmux` call with rc-1 so no
    test can reach the live `agi-rc` session. This file exists to read the
    real binary, so it re-arms `subprocess.run` -- but ONLY for calls that
    name our throwaway session prefix. A tmux call touching any other
    session (in particular the live `agi-rc`) keeps the guard's no-session
    answer, so the hazard the guard exists for stays closed."""
    def _scoped(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            if any(TMP_SESSION_PREFIX in str(t) for t in cmd):
                return _REAL_RUN(cmd, *a, **k)
            return subprocess.CompletedProcess(cmd, 1)
        return _REAL_RUN(cmd, *a, **k)

    monkeypatch.setattr(subprocess, "run", _scoped)


def _tmux(*argv):
    return subprocess.run(["tmux", *argv], capture_output=True, text=True,
                          timeout=10)


def _live_id(sess, name):
    """The @id real tmux reports for `name` in `sess`, or None."""
    r = _tmux("list-windows", "-t", sess, "-F", "#{window_id} #{window_name}")
    assert r.returncode == 0, r.stderr
    for ln in r.stdout.splitlines():
        ident, _, wname = ln.partition(" ")
        if wname.strip() == name:
            return ident.strip()
    return None


def _add_seat_window(sess, name):
    """Create a REAL tmux window `name` in `sess`; return its live @id."""
    r = _tmux("new-window", "-t", sess, "-n", name, "sleep 300")
    assert r.returncode == 0, r.stderr
    live = _live_id(sess, name)
    assert live, f"tmux made no window named {name!r}"
    return live


@pytest.fixture
def tmux_session():
    """A real throwaway tmux session with a placeholder window; killed after."""
    sess = f"{TMP_SESSION_PREFIX}-{uuid.uuid4().hex[:8]}"
    r = _tmux("new-session", "-d", "-s", sess, "-n", "placeholder", "sleep 300")
    assert r.returncode == 0, r.stderr
    try:
        yield sess
    finally:
        _tmux("kill-session", "-t", sess)


# ---- READ side against the real binary ---------------------------------- #

def test_successor_window_id_reads_real_tmux(tmux_session):
    """The ONE pane derivation, no seam: it returns tmux's own @id."""
    assert _live_id(tmux_session, SEAT) is None      # absent before the launch
    live = _add_seat_window(tmux_session, SEAT)
    assert rotate._successor_window_id(SEAT, tmux_session, None) == live, live


def test_seat_occupation_occupied_against_real_tmux(tmux_session):
    """A row pinned to the @id tmux really reports reads occupied."""
    live = _add_seat_window(tmux_session, SEAT)
    occ = SS.seat_occupation(
        {"name": SEAT, "window": live, "pid": _LIVE_PID},
        tmux_session, None)
    assert occ is not None, occ
    assert occ["state"] == "occupied", occ
    assert occ["window"] == live and occ["live"] == live, occ
    assert occ["pid_alive"] is True, occ


def test_seat_occupation_pane_drift_on_a_stale_pin_against_real_tmux(
        tmux_session):
    live = _add_seat_window(tmux_session, SEAT)
    occ = SS.seat_occupation(
        {"name": SEAT, "window": "@999999", "pid": _LIVE_PID},
        tmux_session, None)
    assert occ["state"] == "pane-drift", occ
    assert occ["window"] == "@999999" and occ["live"] == live, occ


def test_seat_occupation_unoccupied_when_real_tmux_lacks_the_name(
        tmux_session):
    """Negative control: a real session with a foreign window only."""
    _add_seat_window(tmux_session, "somebody-else")
    occ = SS.seat_occupation({"name": SEAT, "window": "@7"},
                             tmux_session, None)
    assert occ["state"] == "unoccupied", occ
    assert occ["live"] is None, occ


def test_pane_coherent_true_against_real_tmux(tmux_session):
    live = _add_seat_window(tmux_session, SEAT)
    assert SS.pane_coherent({"name": SEAT, "window": live},
                            tmux_session, None) is True


# ---- WRITE side through cmd_spawn, the launch boundary stubbed only ----- #

def _spawn_args(tmux_session, seat=SEAT, reg=None):
    return SimpleNamespace(
        name=None, tier="kid", prompt_file=None, model=None, effort=None,
        settings=None, tmux_session=tmux_session, window_path=None,
        dry_run=False, successor_argv=None, seat=seat, pid=None,
        no_autopsy=True, registry_dir=reg, harness=None,
    )


@pytest.fixture
def real_spawn(monkeypatch, tmux_session):
    """Model the real launch sequence: the seat window is ABSENT at the
    pre-spawn gate and a REAL tmux window is created by the launch. Only the
    process-launch boundary is stubbed; the pin derivation afterwards reads
    the tmux binary (window_path is None)."""
    calls = []

    def fake_spawn_window(**kw):
        calls.append(kw)
        assert kw.get("window_path") is None, kw
        _add_seat_window(tmux_session, kw["name"])
        return 0, "echo ok"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn_window)
    monkeypatch.setattr(rotate, "_first_seating_run",
                        lambda *a, **k: ("", []))
    return calls


def _seat_start(tmp_path, real_spawn, tmux_session, rows, seat=SEAT):
    graph = _graph(tmp_path, rows)
    rc = rotate.cmd_spawn(
        _spawn_args(tmux_session, seat=seat, reg=str(tmp_path / "noreg")),
        graph)
    assert rc == 0, rc
    return graph, _row(graph, seat)


def test_seat_start_writes_the_real_tmux_pin(tmp_path, real_spawn,
                                             tmux_session):
    """The committed row's `window` cell IS the @id real tmux reports, and a
    real-tmux occupation read of that row is `occupied`."""
    graph, row = _seat_start(
        tmp_path, real_spawn, tmux_session,
        [{"name": SEAT, "role": "director", "session_kind": "remote-control"}])
    live = _live_id(tmux_session, SEAT)
    assert live, "the launch did not create a real tmux window"
    assert row.get("window") == live, row
    occ = SS.seat_occupation(row, tmux_session, None)
    assert occ and occ["state"] == "occupied", occ
    assert occ["live"] == live, occ


def test_seat_start_session_half_is_empty_by_design(tmp_path, real_spawn,
                                                    tmux_session):
    """SETTLEMENT: at a spawn-only seat start the pane pin is real and
    matching, but the session-identity cells are EMPTY -- `session_ref` and
    `session_name` await `rotate.py ack`, `session_id` awaits the harness
    registry JOIN -- and NO cell carries the tmux session name at all. The
    falsifier's "session pin matching tmux" is therefore satisfied on the
    PANE half only."""
    graph, row = _seat_start(
        tmp_path, real_spawn, tmux_session,
        [{"name": SEAT, "role": "director", "session_kind": "remote-control"}])
    # pane half: real and matching
    live = _live_id(tmux_session, SEAT)
    assert row.get("window") == live, row
    # session half: empty by design at spawn
    assert row.get("session_ref") in ("", None), row
    assert row.get("session_name") in ("", None), row
    assert row.get("session_id") in ("", None), row
    # no cell anywhere carries the tmux SESSION name
    assert all(tmux_session not in str(v) for v in row.values()), row
