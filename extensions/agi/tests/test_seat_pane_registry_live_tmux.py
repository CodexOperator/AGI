"""goal:g7.31.2.1 — LIVE tmux end-to-end for the seat pane pin.

Closes the open caveat recorded on experiment:seat-occupation-view, verbatim:

    Caveat: the seam is `window_path` ... not a live `tmux` binary. The live
    tmux path is exercised only through the fail-open branch; this experiment
    certifies the read logic and the render seam, not an end-to-end tmux
    invocation.

Every test here drives the REAL /usr/bin/tmux through
`rotate._successor_window_id`'s `window_path=None` branch — the
`subprocess.run(["tmux", "list-windows", ...])` arm at rotate.py, never a
`window_path` fixture file. `test_live_tmux_wire_reaches_subprocess_not_a_seam`
asserts the subprocess was actually issued, so a silent fall back to a seam
cannot pass.

ISOLATION. The suite's autouse `_no_real_tmux` fixture rewrites every tmux
subprocess to rc=1 (see conftest). This module overrides `subprocess.run` in
its own fixture body — the documented precedence — but only to pass tmux
through to the REAL runner, and only after pointing `TMUX_TMPDIR` at a fresh
per-test directory. The tmux client with no `-L`/`-S` then uses the DEFAULT
socket INSIDE that directory: the same socket the production call (which
passes neither flag) reaches, and a socket no other test can see or touch.

On a host with no `tmux` binary every test SKIPS — never a false pass.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
from agi.bin import rotate  # noqa: E402
import seat_status as SS  # noqa: E402

#: The real runner, captured at IMPORT time — before the autouse guard fixture
#: replaces `subprocess.run`. The fixture below hands tmux calls to THIS.
_REAL_RUN = subprocess.run

pytestmark = pytest.mark.skipif(shutil.which("tmux") is None,
                                reason="live-tmux test: no tmux binary")


class _LiveTmux:
    """A private tmux server reachable by the production `tmux` calls."""

    def __init__(self, session: str, env: dict, calls: list):
        self.session = session
        self.env = env
        self.calls = calls

    def run(self, *args):
        r = _REAL_RUN(["tmux", *args], capture_output=True, text=True,
                      timeout=5, env=self.env)
        return r.returncode, r.stdout, r.stderr

    def list_windows(self, session: str | None = None) -> dict[str, str]:
        """`{window_name: @id}` — the TRUTH, read from tmux itself."""
        rc, out, err = self.run("list-windows", "-t",
                                session or self.session,
                                "-F", "#{window_id} #{window_name}")
        assert rc == 0, (out, err)
        out_map = {}
        for ln in out.splitlines():
            wid, _, name = ln.partition(" ")
            if name.strip():
                out_map[name.strip()] = wid.strip()
        return out_map

    def new_window(self, name: str) -> str:
        rc, out, err = self.run("new-window", "-t", self.session, "-n", name)
        assert rc == 0, (out, err)
        return self.list_windows()[name]

    def kill_window(self, name: str):
        rc, out, err = self.run("kill-window", "-t",
                                f"{self.session}:{name}")
        assert rc == 0, (out, err)


@pytest.fixture
def live_tmux(tmp_path, monkeypatch):
    """Private tmux server + a `subprocess.run` override that lets tmux out."""
    if shutil.which("tmux") is None:
        pytest.skip("live-tmux test: no tmux binary")
    sock_dir = tmp_path / "tmuxdir"
    sock_dir.mkdir()
    env = dict(os.environ)
    env["TMUX_TMPDIR"] = str(sock_dir)
    env.pop("TMUX", None)
    # the production subprocess inherits os.environ: point IT at the same dir
    monkeypatch.setenv("TMUX_TMPDIR", str(sock_dir))
    monkeypatch.delenv("TMUX", raising=False)
    # the autouse _no_real_tmux guard, captured before we wrap it
    guard = subprocess.run
    calls: list = []

    def _run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            calls.append(list(cmd))
            return _REAL_RUN(cmd, *a, **k)
        return guard(cmd, *a, **k)          # non-tmux: the guard's own passthrough

    monkeypatch.setattr(subprocess, "run", _run)

    session = f"agi-rc-live-{os.getpid()}-{uuid.uuid4().hex[:6]}"
    srv = _LiveTmux(session, env, calls)
    rc, out, err = srv.run("new-session", "-d", "-s", session,
                           "-n", "belam-placeholder")
    if rc != 0:
        pytest.skip(f"cannot start an isolated tmux server: {out!r} {err!r}")
    try:
        yield srv
    finally:
        srv.run("kill-server")


# ---- the live READ path: seat_status over a real tmux window -------------- #

def test_live_tmux_seat_occupation_reads_the_real_window_id(live_tmux):
    """Occupied iff the row pin IS the live @id and the pid is alive."""
    live_id = live_tmux.new_window("director-seat")
    row = {"name": "director-seat", "window": live_id, "pid": os.getpid()}
    occ = SS.seat_occupation(row, live_tmux.session, window_path=None)
    assert occ is not None, occ
    assert occ["state"] == "occupied", occ
    assert occ["window"] == live_id and occ["live"] == live_id, occ
    assert occ["pid_alive"] is True, occ
    assert SS.pane_coherent(row, live_tmux.session, None) is True


def test_live_tmux_wire_reaches_subprocess_not_a_seam(live_tmux):
    """The live arm is the subprocess `tmux list-windows`, never a seam file."""
    live_id = live_tmux.new_window("director-seat")
    live_tmux.calls.clear()
    got = rotate._successor_window_id("director-seat", live_tmux.session,
                                      None)
    assert got == live_id, (got, live_id)
    assert any(c[:2] == ["tmux", "list-windows"] for c in live_tmux.calls), \
        live_tmux.calls


def test_live_tmux_occupation_goes_unoccupied_when_the_window_is_killed(
        live_tmux):
    """Killing the pane names the drift; the SAME call reads unoccupied."""
    live_id = live_tmux.new_window("director-seat")
    row = {"name": "director-seat", "window": live_id, "pid": os.getpid()}
    live_tmux.kill_window("director-seat")
    occ = SS.seat_occupation(row, live_tmux.session, window_path=None)
    assert occ is not None, occ
    assert occ["state"] == "unoccupied", occ
    assert occ["live"] is None, occ
    coh = SS.pane_coherent(row, live_tmux.session, None)
    assert isinstance(coh, str) and "director-seat" in coh, coh


def test_live_tmux_pane_drift_when_the_row_pin_is_stale(live_tmux):
    """A row pin tmux does not have reads pane-drift, live = the real @id."""
    live_id = live_tmux.new_window("director-seat")
    row = {"name": "director-seat", "window": "@999", "pid": os.getpid()}
    occ = SS.seat_occupation(row, live_tmux.session, window_path=None)
    assert occ["state"] == "pane-drift", occ
    assert occ["live"] == live_id, occ
    coh = SS.pane_coherent(row, live_tmux.session, None)
    assert isinstance(coh, str) and "director-seat" in coh, coh


# ---- the WRITE path: a seat start lands the LIVE @id in the registry ------ #

def _graph(tmp_path, rows):
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


def _spawn_args(seat="director-seat"):
    from types import SimpleNamespace
    return SimpleNamespace(
        name=seat, tier="kid", prompt_file=None, model=None, effort=None,
        settings=None, tmux_session=None, window_path=None,
        dry_run=False, successor_argv=None, seat=seat, pid=None,
        no_autopsy=True, registry_dir=None, harness=None,
    )


def _row(graph, name):
    fm = yaml.safe_load((graph / "nodes" / ".geometry" / "seats.md")
                        .read_text(encoding="utf-8").split("---")[1])
    return next(r for r in fm["seats"] if r.get("name") == name)


def test_live_tmux_cmd_spawn_lands_the_live_window_pin(tmp_path, live_tmux,
                                                       monkeypatch):
    """Falsifier: after seat start the registry shows the live pane pin.

    The launch is stubbed (no real agent is started) but the WINDOW it leaves
    behind is a REAL tmux window on the private server, created with the real
    binary — so the row's `window` cell must land that window's live @id.
    """
    monkeypatch.setattr(rotate, "_first_seating_run", lambda *a, **k: ("", []))

    def fake_spawn_window(**kw):
        assert kw.get("window_path") is None, kw.get("window_path")
        live_tmux.new_window("director-seat")           # the real tmux window
        return 0, "echo ok"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn_window)
    graph = _graph(tmp_path, [{"name": "director-seat", "role": "director",
                               "session_kind": "remote-control"}])
    args = _spawn_args()
    args.tmux_session = live_tmux.session
    rc = rotate.cmd_spawn(args, graph)
    assert rc == 0, rc
    live_id = live_tmux.list_windows()["director-seat"]
    r = _row(graph, "director-seat")
    assert r.get("window") == live_id, r
    occ = SS.seat_occupation(r, live_tmux.session, window_path=None)
    assert occ is not None and occ["state"] == "occupied", (occ, r)
    assert occ["live"] == live_id, occ
