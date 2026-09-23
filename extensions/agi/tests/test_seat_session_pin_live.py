"""goal:g7.31.2.1 — the SESSION half of the seat-start pin, LIVE.

hypothesis:a00-03083f0a-d7d355.

The PANE half is proved live by `test_seat_pane_registry_live.py`
(hypothesis:a00-d8d8a1f0-1137fc). Its own body then states the residue in
prose: tmux witnesses the pane and only the pane, so the row's
`session_id` / `session_name` / `session_ref` cells are asserted nowhere.

Falsifier, verbatim: after seat start, posts/seat registry shows occupied
with the live pane/session pin matching `tmux`.

This module settles the SESSION half by driving the REAL `rotate.cmd_spawn`
seat-start path against BOTH witnesses at once:

  * a private real tmux server (own `TMUX_TMPDIR`, `window_path=None`), so
    the pane @id the row commits is read from tmux itself, and
  * a REAL registry JOIN: a `<pid>.json` file whose content carries that
    live `@id` token, the exact shape `rotate._join_successor` consumes.

It then reads the COMMITTED `config:seats` row (the wire bytes) for every
session cell, runs the real `rotate.cmd_ack` ack path with the `--ref` the
claim describes, and reads the row again.

The suite's project-wide autouse tmux guard (`conftest._no_real_tmux`)
answers every `["tmux", ...]` subprocess with a safe rc-1. This module
re-arms the real runner ONLY for tmux calls whose `TMUX_TMPDIR` is its own
private socket dir, so no live session can ever be reached from here. If
tmux is missing or the private server will not start the module SKIPS.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
from agi.bin import rotate  # noqa: E402

TMUX = shutil.which("tmux")
SESSION = "live-seat-session"
SEAT = "director-seat"
#: the harness-side registry facts a real successor would register.
JOIN_PID = 4242
JOIN_SID = "abcd1234-aaaa-bbbb-cccc-dddd12345678"
JOIN_NAME = "agi-d7"
#: a bare ListAgents ref, never a uuid shape (F15 refuses uuid-shaped refs).
REF = "caa927"

#: Captured at import, before any conftest fixture swaps it out.
_REAL_RUN = subprocess.run
#: The one socket dir this module is allowed to talk to.
_PRIVATE_SOCKDIR = {"dir": None}

pytestmark = pytest.mark.skipif(
    TMUX is None, reason="tmux not installed; the live witness needs it")


def _private_tmux_run(cmd, *a, **kw):
    """Re-arm real tmux ONLY against this module's private server."""
    if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
        env = kw.get("env") or os.environ
        if (_PRIVATE_SOCKDIR["dir"]
                and str(env.get("TMUX_TMPDIR")) == _PRIVATE_SOCKDIR["dir"]):
            return _REAL_RUN(cmd, *a, **kw)
        return subprocess.CompletedProcess(cmd, 1)
    return _REAL_RUN(cmd, *a, **kw)


def _tmux(*args: str) -> subprocess.CompletedProcess:
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
    """A private tmux server whose session has NO seat window yet.

    The seat window must be absent at the pre-spawn gate and created by the
    launch, exactly as a real first seating does; the fixture leaves that to
    the `spawn_window` stub. Skips (never fails) when the server cannot start.
    """
    sockdir = tmp_path / "tmuxpriv"
    sockdir.mkdir()
    _PRIVATE_SOCKDIR["dir"] = str(sockdir)
    monkeypatch.setenv("TMUX_TMPDIR", str(sockdir))
    monkeypatch.setattr(subprocess, "run", _private_tmux_run)
    if _tmux("new-session", "-d", "-s", SESSION, "-n", "bootstrap") \
            .returncode != 0:
        _PRIVATE_SOCKDIR["dir"] = None
        pytest.skip("could not start a private tmux server")
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


def _row(graph: Path, name: str) -> dict:
    """The seat row exactly as it lives on the wire in seats.md."""
    fm = yaml.safe_load((graph / "nodes" / ".geometry" / "seats.md")
                        .read_text(encoding="utf-8").split("---")[1])
    return next(r for r in fm["seats"] if r.get("name") == name)


def _spawn_args(seat=SEAT, reg=None):
    return SimpleNamespace(
        name=seat, tier="kid", prompt_file=None, model=None, effort=None,
        settings=None, tmux_session=SESSION, window_path=None,
        dry_run=False, successor_argv=None, seat=seat, pid=None,
        no_autopsy=True, registry_dir=reg, harness=None,
    )


def _ack_args(sid, reg=None):
    return SimpleNamespace(seat=SEAT, gen=None, session=sid, ref=REF,
                           answer="continue", text="",
                           registry_dir=(str(reg) if reg else None),
                           window_path=None, no_commit=True, wait=0)


def _drive_seat_start(tmp_path, monkeypatch, live_tmux):
    """Drive the REAL `cmd_spawn` against live tmux + a real registry JOIN.

    The `spawn_window` stub plays the launch: it creates the real seat window
    in the private server, reads the `@id` tmux itself reports, and writes a
    registry record carrying that token — the exact fact the JOIN consumes.
    Returns (graph, registry_dir, window_id).
    """
    graph = _graph(tmp_path, [{"name": SEAT, "role": "director",
                               "session_kind": "remote-control"}])
    reg = tmp_path / "registry"
    box: dict = {}
    calls: list = []

    def fake_spawn_window(**kw):
        calls.append(kw)
        assert _tmux("new-window", "-t", SESSION, "-n", SEAT).returncode == 0
        wid = _live_id(SEAT)
        reg.mkdir(parents=True, exist_ok=True)
        # registry content carries `@<id> ` as a DELIMITED token, tmux's own
        # `view:@<id>.%<pane>` shape — never a bare substring.
        (reg / f"{JOIN_PID}.json").write_text(json.dumps({
            "session_id": JOIN_SID, "name": JOIN_NAME,
            "cwd": "/home/u/proj/.agi", "tmux": f"view:{wid}.%0",
        }), encoding="utf-8")
        box["window"] = wid
        return 0, "echo ok"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn_window)
    monkeypatch.setattr(rotate, "_first_seating_run",
                        lambda *a, **k: ("", []))
    rc = rotate.cmd_spawn(_spawn_args(reg=str(reg)), graph)
    assert rc == 0, rc
    assert box["window"] == _live_id(SEAT), (box, _live_windows())
    return graph, reg, box["window"]


def test_session_pin_at_seat_start_is_the_joined_registry_fact(
        tmp_path, monkeypatch, live_tmux):
    """The SESSION cells the seat-start row commits, versus the live JOIN."""
    graph, _reg, wid = _drive_seat_start(tmp_path, monkeypatch, live_tmux)
    row = _row(graph, SEAT)
    # the PANE pin is tmux's own @id (the sibling's proved half, re-asserted)
    assert row.get("window") == wid, row
    # the JOINED session identity lands at seat start from the registry file
    # keyed on that @id -- measured, not assumed.
    assert row.get("session_id") == JOIN_SID, row
    assert row.get("pid") == JOIN_PID, row
    assert "generation" in row, row
    # and the SHORT ref + the harness NAME are the cells that do NOT.
    assert row.get("session_ref") in ("", None), row
    assert row.get("session_name") in ("", None), row


def test_ack_backfills_the_ref_and_the_name_but_no_earlier(
        tmp_path, monkeypatch, live_tmux, capsys):
    """The ack path: which session cells the back-fill lands, and when."""
    graph, reg, wid = _drive_seat_start(tmp_path, monkeypatch, live_tmux)
    start = _row(graph, SEAT)
    assert start.get("session_id") == JOIN_SID, start

    rc = rotate.cmd_ack(_ack_args(start["session_id"], reg=reg), graph)
    assert rc == 0, rc
    after = _row(graph, SEAT)
    assert after.get("session_ref") == REF, after
    assert after.get("session_name") == JOIN_NAME, after
    # the JOIN re-finds the same identity by the row's OWN window @id and
    # leaves pid/session_id byte-identical (they already hold).
    assert after.get("session_id") == JOIN_SID, after
    assert after.get("pid") == JOIN_PID, after
    assert after.get("window") == wid, after
