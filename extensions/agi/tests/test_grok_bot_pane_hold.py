"""goal:g7.31.1.2 -- durable named tmux pane hold in `grok_bot_adapter.restart`.

The claim: `restart(hold_pane=True)` holds the seat's process in ONE named
tmux pane, the name derived from the seat identity and NEVER a pid; a second
restart targets that SAME pane and opens no second; killing the process leaves
the pane (durable hold); and with tmux unusable the adapter falls back to
today's direct `Popen` and never raises.

No live tmux: a stateful recording `tmux` shim on PATH. The shim tracks
sessions by NAME (not pid) and actually spawns the argv, so the durability
conjunct is measured against a real dead pid rather than asserted.
"""
from __future__ import annotations

import json
import os
import signal
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

grok = adapters.load("grok_bot")

HARNESS = {"adapter": "grok_bot", "bin": "SLEEPER",
           "models": {"kid": "grok-kid"}}

#: Stateful recording tmux. Sessions are keyed by NAME; `list-panes` reads the
#: session table, never the pid, so a dead pid cannot hide the pane.
SHIM = r'''#!/usr/bin/env python3
import json, os, subprocess, sys
log, state_path = os.environ["TMUX_SHIM_LOG"], os.environ["TMUX_SHIM_STATE"]
argv = sys.argv[1:]
with open(log, "a") as fh:
    fh.write(" ".join(argv) + "\n")
state = json.load(open(state_path)) if os.path.exists(state_path) else {}
sub = argv[0] if argv else ""
def name_of():
    return argv[argv.index("-t") + 1] if "-t" in argv else argv[argv.index("-s") + 1]
if sub == "has-session":
    sys.exit(0 if name_of() in state else 1)
if sub in ("new-session", "respawn-pane"):
    name, cwd = name_of(), argv[argv.index("-c") + 1]
    cmd = argv[argv.index("-c") + 2:]
    old = state.get(name, {}).get("pid")
    if old:
        try: os.kill(old, 9)
        except OSError: pass
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    state[name] = {"pid": proc.pid, "argv": cmd}
    json.dump(state, open(state_path, "w"))
    sys.exit(0)
if sub == "list-panes":
    if name_of() in state:
        print("%s %d" % (name_of(), state[name_of()]["pid"]))
    sys.exit(0)
sys.exit(0)
'''


@pytest.fixture(autouse=True)
def _no_real_tmux(tmux_shim):
    """Override the conftest project-wide tmux guard for this module.

    The conftest guard answers every `subprocess.run(["tmux", ...])` with a
    bare rc-1 BEFORE the call reaches PATH -- so this module's recording shim
    would never see a call and every test would measure the fallback. A
    module-level fixture of the same name shadows it (as test_send_surface
    does); with the shim on PATH the shim itself is the tether, never live
    tmux. `tmux_shim` is requested so the shim is installed for every test.
    """
    yield


@pytest.fixture
def tmux_shim(tmp_path, monkeypatch):
    """A recording tether shim on PATH; yields (log, state) paths."""
    shim_dir = tmp_path / "shim"
    shim_dir.mkdir()
    log = tmp_path / "tmux.log"
    state = tmp_path / "tmux-state.json"
    tmux = shim_dir / "tmux"
    tmux.write_text(SHIM)
    tmux.chmod(0o755)
    monkeypatch.setenv("TMUX_SHIM_LOG", str(log))
    monkeypatch.setenv("TMUX_SHIM_STATE", str(state))
    monkeypatch.setenv(
        "PATH", f"{shim_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return log, state


def _sleeper(tmp_path) -> str:
    p = tmp_path / "sleeper.sh"
    p.write_text("#!/bin/bash\nexec sleep 60\n")
    p.chmod(0o755)
    return str(p)


def _sess(tmp_path) -> Path:
    s = tmp_path / "iter-X" / "a00-seat"
    s.mkdir(parents=True, exist_ok=True)
    return s


def _restart(tmp_path, hold_pane=True, agent_id="a00-seat", record=None):
    sess = _sess(tmp_path)
    return grok.restart(
        harness={**HARNESS, "bin": _sleeper(tmp_path)}, tier="kid",
        context_file=str(sess / "context.md"), agent_id=agent_id, iter_n=1,
        sess_dir=sess, agent_record=record, hold_pane=hold_pane)


def _reap(pid):
    try:
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass
    try:
        os.waitpid(pid, 0)
    except OSError:
        pass
    time.sleep(0.05)


def test_first_restart_opens_exactly_one_named_pane(tmp_path, tmux_shim):
    log, _ = tmux_shim
    pid = _restart(tmp_path)
    text = log.read_text()
    assert "new-session" in text, "non-vacuity: the shim must record a call"
    assert text.count("new-session") == 1
    name = grok.pane_name("a00-seat")
    assert f"new-session -d -s {name}" in text
    assert pid and grok.is_alive(pid)
    _reap(pid)


def test_second_restart_reuses_the_same_named_pane(tmp_path, tmux_shim):
    log, _ = tmux_shim
    rec = {}
    first = _restart(tmp_path, record=rec)
    second = _restart(tmp_path, record=rec)
    text = log.read_text()
    name = grok.pane_name("a00-seat")
    assert text.count("new-session") == 1, "no second pane may open"
    assert text.count("respawn-pane") == 1
    assert f"respawn-pane -k -t {name}" in text
    assert first != second, "respawn must have replaced the process"
    assert not grok.is_alive(first)
    assert grok.is_alive(second)
    assert rec["tmux_pane"] == name
    _reap(second)


def test_killing_the_process_leaves_the_named_pane(tmp_path, tmux_shim):
    log, state = tmux_shim
    pid = _restart(tmp_path)
    name = grok.pane_name("a00-seat")
    before = grok.pane_listing(name)
    assert before and before[0].split()[0] == name, "pane must exist first"
    _reap(pid)
    assert not grok.is_alive(pid), "the seat process must be genuinely dead"
    after = grok.pane_listing(name)
    assert after and after[0].split()[0] == name, (
        "the pane must outlive the pid (durable hold): " + json.dumps(
            {"state": json.loads(state.read_text()) if state.exists() else {}}))


def test_default_restart_touches_no_tmux(tmp_path, tmux_shim, monkeypatch):
    """The default (no pane requested) stays byte-for-byte today's Popen path:
    dispatch's existing call sites must not start shelling out to tmux."""
    log, _ = tmux_shim
    captured = {}

    class FakeProc:
        pid = 4141

    def fake_popen(args, **kwargs):
        captured["args"] = args
        return FakeProc()

    monkeypatch.setattr(grok.subprocess, "Popen", fake_popen)
    pid = _restart(tmp_path, hold_pane=False)
    assert pid == 4141
    assert captured["args"][0].endswith("sleeper.sh")
    assert not log.exists(), "default restart must make zero tmux invocations"


def test_tmux_unavailable_falls_back_to_direct_popen(tmp_path, monkeypatch):
    """tmux absent: the adapter runs the same argv through Popen and never
    raises (pane mode is an enhancement, not a new failure mode)."""
    captured = {}

    class FakeProc:
        pid = 5151

    def fake_popen(args, **kwargs):
        captured["args"] = args
        return FakeProc()

    def no_tmux(*a, **k):
        raise FileNotFoundError("tmux")

    monkeypatch.setattr(grok.subprocess, "run", no_tmux)
    monkeypatch.setattr(grok.subprocess, "Popen", fake_popen)
    rec = {}
    pid = _restart(tmp_path, record=rec)
    assert pid == 5151
    assert captured["args"] == grok.build_command(
        harness={**HARNESS, "bin": captured["args"][0]}, tier="kid",
        context_file=str(_sess(tmp_path) / "context.md"))
    assert "tmux_pane" not in rec
