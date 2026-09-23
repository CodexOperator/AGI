"""goal:g7.31.2.1 — seat-start registry pin certified against a REAL tmux server.

experiment:a00-046bc37a-live-tmux (hypothesis:a00-046bc37a-4d3d2a).

Every prior certificate for this falsifier ran against the `window_path`
fixture seam. This file starts a REAL tmux 3.4 server on an ISOLATED
`TMUX_TMPDIR` (the default socket dir fails on this host with "server exited
unexpectedly") and reads the REAL `@id` through the committed bytes:
`rotate._successor_window_id(..., window_path=None)` -> `tmux list-windows`.

Re-runnable command:

    python3 -m pytest extensions/agi/tests/test_seat_pane_live_tmux.py -q

The project-wide `_no_real_tmux` autouse guard is opted out by the module-level
`real_tmux` marker (registered in conftest.pytest_configure); the server is
killed in teardown even when an assertion fails, and the session name
(`agi-live-probe`) is deliberately not the live `agi-rc`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
from agi.bin import rotate  # noqa: E402
import seat_status as SS  # noqa: E402

#: Never the live session. The socket dir is a per-test temp dir via
#: TMUX_TMPDIR, so a stray server can never reach the seat's own tmux.
SESSION = "agi-live-probe"
SEAT = "live-probe-seat"

pytestmark = pytest.mark.real_tmux


def _tmux(*args):
    return subprocess.run(["tmux", *args], capture_output=True, text=True,
                          timeout=10)


def _live_id(name):
    """The REAL tmux @id for window `name` in SESSION, or None."""
    r = _tmux("list-windows", "-t", SESSION, "-F",
              "#{window_id} #{window_name}")
    for ln in r.stdout.splitlines():
        wid, _, wn = ln.partition(" ")
        if wn.strip() == name:
            return wid.strip()
    return None


@pytest.fixture
def live_tmux(tmp_path, monkeypatch):
    """A REAL tmux server whose only window is named SEAT.

    Isolated by BOTH a per-test `TMUX_TMPDIR` and a session name that is not
    the live `agi-rc`; `TMUX`/`TMUX_PANE` are removed so a test run from
    inside a tmux session still targets the private server. Teardown runs
    `kill-server` in `finally`, so a failed assertion never leaks a server.
    """
    sock = tmp_path / "tmuxsock"
    sock.mkdir()
    monkeypatch.setenv("TMUX_TMPDIR", str(sock))
    monkeypatch.delenv("TMUX", raising=False)
    monkeypatch.delenv("TMUX_PANE", raising=False)
    r = _tmux("new-session", "-d", "-s", SESSION, "-n", SEAT, "sleep 3600")
    assert r.returncode == 0, (r.returncode, r.stderr)
    try:
        yield {"seat": SEAT, "session": SESSION}
    finally:
        _tmux("kill-server")


def _graph(tmp_path, rows):
    """A real `.agi` graph root whose config:seats registry carries `rows`
    (same shape as test_seat_pane_registry._graph)."""
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


def _row(graph, name):
    fm = yaml.safe_load((graph / "nodes" / ".geometry" / "seats.md")
                        .read_text(encoding="utf-8").split("---")[1])
    return next(r for r in fm["seats"] if r.get("name") == name)


# ---- WIRE: the seat-start row carries the REAL tmux @id ---------------- #

def test_seat_start_pin_matches_a_real_tmux_id(live_tmux, tmp_path):
    """The falsifier, on real bytes: seat start pins the live tmux @id and the
    occupation read says `occupied` with that same pin."""
    seat = live_tmux["seat"]
    wid = _live_id(seat)
    assert wid, "the fixture's own window must be visible to real tmux"
    # the committed READER, window_path=None -> real tmux list-windows
    assert rotate._successor_window_id(seat, SESSION, None) == wid
    graph = _graph(tmp_path, [{"name": seat, "role": "director",
                              "pubkey": "dummy-self-row-key"}])
    # the seat-start WRITER (cmd_spawn's `_first_seating_spawn_writes` passes
    # session_ref="" and the @id it just derived from tmux)
    out = rotate._successor_row_write(
        graph, actor=seat, seat=seat, role="director", session_ref="",
        generation=1, window=wid, pid=0)
    assert out, out
    row = _row(graph, seat)
    assert row.get("window") == wid, row
    occ = SS.seat_occupation(row, SESSION, None)
    assert occ is not None, occ
    assert occ["state"] == "occupied", occ
    assert occ["window"] == wid and occ["live"] == wid, occ
    # SESSION HALF, measured honestly: the pane pin is present; the JOIN
    # identity (`session_ref`) and harness `session_name` are EMPTY until
    # `rotate.py ack` back-fills them (rotate.py `_backfill_session_ref`).
    assert row.get("session_ref") in ("", None), row
    assert row.get("session_name") in ("", None), row


# ---- GATE: a pin tmux does not have is drift, not occupation ----------- #

def test_real_tmux_flags_a_foreign_pin(live_tmux):
    seat = live_tmux["seat"]
    occ = SS.seat_occupation({"name": seat, "window": "@9999", "pid": 0},
                             SESSION, None)
    assert occ is not None and occ["state"] == "pane-drift", occ
    assert occ["window"] == "@9999", occ
    assert occ["live"] and occ["live"] != "@9999", occ


def test_killed_window_reads_unoccupied(live_tmux):
    """The negative that proves the positive needed a real server: kill the
    real window and the same row stops reading `occupied`."""
    seat = live_tmux["seat"]
    wid = _live_id(seat)
    assert wid
    _tmux("kill-window", "-t", f"{SESSION}:{seat}")
    assert _live_id(seat) is None
    occ = SS.seat_occupation({"name": seat, "window": wid, "pid": 0},
                             SESSION, None)
    assert occ is not None and occ["state"] == "unoccupied", occ
    assert occ["live"] is None, occ


def test_no_server_is_never_occupied(tmp_path, monkeypatch):
    """Falsifier for this file itself: with a private empty socket dir and no
    server, the READER returns None and occupation is `unoccupied` — so the
    `occupied` assertion above cannot pass without a live tmux."""
    sock = tmp_path / "dead-socket"
    sock.mkdir()
    monkeypatch.setenv("TMUX_TMPDIR", str(sock))
    monkeypatch.delenv("TMUX", raising=False)
    monkeypatch.delenv("TMUX_PANE", raising=False)
    try:
        assert rotate._successor_window_id(SEAT, SESSION, None) is None
        occ = SS.seat_occupation({"name": SEAT, "window": "@0"}, SESSION, None)
        assert occ is not None and occ["state"] == "unoccupied", occ
    finally:
        _tmux("kill-server")
