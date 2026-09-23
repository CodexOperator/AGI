"""goal:g7.31.2.1 — LIVE tmux witness for the seat pane pin.

hypothesis:a00-d8d8a1f0-1137fc.

The sibling `test_seat_pane_registry.py` never talks to a real tmux: it stubs
the window list with a `window_path` seam file. That is exactly why the
falsifier still reads a lean rather than green. THIS file closes the gap.

Falsifier, verbatim: after seat start, posts/seat registry shows occupied
with the live pane/session pin matching `tmux`.

Witness design. The test starts its OWN throwaway tmux server under a private
`TMUX_TMPDIR`, so it can never see or disturb anyone else's session, then
reads the real `#{window_id} #{window_name}` pairs `tmux list-windows`
reports. `rotate._successor_window_id` shells out to plain `tmux`, so that
env var is what redirects EVERY subprocess it spawns at the same private
server — no seam file, `window_path=None`, tmux itself is the witness.

The suite's project-wide autouse tmux guard (`conftest._no_real_tmux`) answers
every `["tmux", ...]` subprocess with a safe rc-1. This module re-arms the
real runner ONLY for tmux calls whose `TMUX_TMPDIR` is its own private socket
dir, so no other session can ever be reached from here.

If tmux is missing or cannot start a private server the module SKIPS rather
than fails, so an ordinary box without tmux keeps a green suite.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
from agi.bin import rotate  # noqa: E402
import seat_status as SS  # noqa: E402

TMUX = shutil.which("tmux")
SESSION = "live-seat-pin"
SEAT = "director-seat"
OTHER = "other-seat"
GHOST = "ghost-seat"
_LIVE_PID = os.getpid()

#: Captured at import, before any conftest fixture swaps it out.
_REAL_RUN = subprocess.run
#: The one socket dir this module is allowed to talk to, set by `live_tmux`.
_PRIVATE_SOCKDIR = {"dir": None}

pytestmark = pytest.mark.skipif(
    TMUX is None, reason="tmux not installed; the live witness needs it")


def _private_tmux_run(cmd, *a, **kw):
    """Re-arm real tmux ONLY against this module's private server.

    Every other tmux call keeps the project-wide guard's answer (a safe rc-1,
    "no such session"), so re-arming cannot reach a live session.
    """
    if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
        env = kw.get("env") or os.environ
        if (_PRIVATE_SOCKDIR["dir"]
                and str(env.get("TMUX_TMPDIR")) == _PRIVATE_SOCKDIR["dir"]):
            return _REAL_RUN(cmd, *a, **kw)
        return subprocess.CompletedProcess(cmd, 1)
    return _REAL_RUN(cmd, *a, **kw)


def _tmux(*args: str) -> subprocess.CompletedProcess:
    """One plain `tmux` call against the private server in `TMUX_TMPDIR`."""
    return subprocess.run(["tmux", *args], capture_output=True, text=True,
                          timeout=10)


def _live_windows() -> list[str]:
    r = _tmux("list-windows", "-t", SESSION,
              "-F", "#{window_id} #{window_name}")
    assert r.returncode == 0, r.stderr
    return [ln for ln in r.stdout.splitlines() if ln.strip()]


def _live_id(name: str) -> str:
    for ln in _live_windows():
        ident, _, wname = ln.partition(" ")
        if wname.strip() == name:
            return ident.strip()
    raise AssertionError(f"no live window named {name!r} in {_live_windows()}")


@pytest.fixture
def live_tmux(tmp_path, monkeypatch):
    """A private tmux server holding `director-seat` and `other-seat`.

    `TMUX_TMPDIR` is monkeypatched into os.environ so rotate's own `tmux`
    subprocesses land on THIS server, and the real runner is re-armed for it
    only; the whole server is killed in the finalizer. Skips (never fails)
    when the server cannot be started.
    """
    sockdir = tmp_path / "tmuxpriv"
    sockdir.mkdir()
    _PRIVATE_SOCKDIR["dir"] = str(sockdir)
    monkeypatch.setenv("TMUX_TMPDIR", str(sockdir))
    monkeypatch.setattr(subprocess, "run", _private_tmux_run)
    if _tmux("new-session", "-d", "-s", SESSION, "-n", SEAT).returncode != 0:
        _PRIVATE_SOCKDIR["dir"] = None
        pytest.skip("could not start a private tmux server")
    if _tmux("new-window", "-t", SESSION, "-n", OTHER).returncode != 0:
        _tmux("kill-server")
        _PRIVATE_SOCKDIR["dir"] = None
        pytest.skip("could not add a second window to the private server")
    try:
        yield sockdir
    finally:
        _tmux("kill-server")
        _PRIVATE_SOCKDIR["dir"] = None


def _graph(tmp_path: Path, rows: list[dict]) -> Path:
    """A real `.agi` graph root whose `config:seats` registry carries `rows`."""
    graph = tmp_path / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "x"}',
                                       encoding="utf-8")
    schemas = graph / "context" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, session_name, session_id, generation, window, "
        "pid, pubkey, sig_scheme, enc_scheme, key_history, session_label]}\n"
        "---\nbody\n", encoding="utf-8")
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (graph / "nodes" / ".geometry" / "seats.md").write_text(body,
                                                            encoding="utf-8")
    return graph


# ---- the pin tmux itself reports ---------------------------------------- #

def test_successor_window_id_equals_the_real_live_tmux_id(live_tmux):
    """The pin the spawn writer would commit IS what tmux reports, live."""
    real = _live_id(SEAT)
    got = rotate._successor_window_id(SEAT, SESSION, window_path=None)
    assert got == real, (got, real, _live_windows())


def test_successor_window_id_is_none_for_a_seat_tmux_does_not_have(live_tmux):
    assert rotate._successor_window_id(GHOST, SESSION, window_path=None) is None


# ---- seat_occupation, read against live tmux ---------------------------- #

def test_seat_occupation_occupied_with_the_real_live_pin(live_tmux):
    real = _live_id(SEAT)
    occ = SS.seat_occupation(
        {"name": SEAT, "window": real, "pid": _LIVE_PID},
        SESSION, window_path=None)
    assert occ is not None, occ
    assert occ["state"] == "occupied", (occ, _live_windows())
    assert occ["window"] == real and occ["live"] == real, occ
    assert occ["pid_alive"] is True, occ


def test_seat_occupation_pane_drift_on_a_different_real_id(live_tmux):
    """A row pinning ANOTHER real window's @id drifts, naming both."""
    other = _live_id(OTHER)
    real = _live_id(SEAT)
    occ = SS.seat_occupation({"name": SEAT, "window": other},
                             SESSION, window_path=None)
    assert occ is not None, occ
    assert occ["state"] == "pane-drift", occ
    assert occ["window"] == other and occ["live"] == real, occ


def test_seat_occupation_unoccupied_when_tmux_has_no_such_seat(live_tmux):
    occ = SS.seat_occupation({"name": GHOST, "window": "@0"},
                             SESSION, window_path=None)
    assert occ is not None, occ
    assert occ["state"] == "unoccupied", occ
    assert occ["live"] is None, occ


# ---- the falsifier, end to end: registry renders occupied, live ---------- #

def test_collect_renders_occupied_from_the_live_registry(live_tmux, tmp_path):
    """The registry row + real tmux -> every view says pane=occupied(@id)."""
    real = _live_id(SEAT)
    graph = _graph(tmp_path, [{"name": SEAT, "role": "director",
                               "session_kind": "remote-control",
                               "window": real, "pid": _LIVE_PID}])
    view = SS.collect(graph, {}, tmux_session=SESSION, window_path=None)
    occ = view.seats[0]["occupation"]
    assert occ and occ["state"] == "occupied", (occ, _live_windows())
    assert occ["window"] == real and occ["live"] == real, occ
    compact = "\n".join(SS.to_compact(view))
    markdown = "\n".join(SS.to_markdown(view))
    assert f"pane=occupied({real})" in compact, compact
    assert f"pane=occupied({real})" in markdown, markdown


def test_collect_reads_no_occupation_without_a_tmux_session(live_tmux,
                                                            tmp_path):
    """The byte-identical contract survives a live tmux being available."""
    real = _live_id(SEAT)
    graph = _graph(tmp_path, [{"name": SEAT, "role": "director",
                               "window": real}])
    view = SS.collect(graph, {})
    assert view.seats[0]["occupation"] is None, view.seats
    assert "pane=" not in "\n".join(SS.to_compact(view))
