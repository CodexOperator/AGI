"""goal:g7.31.1.2 -- the three parent-verified defects in the pane hold.

A (auth/wire): the pane spawn must thread the SAME scrubbed `child_env` the
direct `Popen` path uses, so `drop_unneeded_credential` is not lost.
C (gate): tmux PRESENT but failing must be a NAMED refusal, never a silent
anonymous `Popen`.
D (gate): a successful respawn followed by a failing `list-panes` must not
return a bare `None`.

No live tmux: a stateful reporting shim on PATH that HONOURS `-e NAME=VALUE`
and records the child's effective env, so defect A is measured, not asserted.
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

SHIM = r'''#!/usr/bin/env python3
import json, os, subprocess, sys
log, state_path = os.environ["TMUX_SHIM_LOG"], os.environ["TMUX_SHIM_STATE"]
argv = sys.argv[1:]
with open(log, "a") as fh:
    fh.write(" ".join(argv) + "\n")
if os.environ.get("TMUX_SHIM_FAIL_ALL") == "1":
    sys.exit(1)
state = json.load(open(state_path)) if os.path.exists(state_path) else {}
sub = argv[0] if argv else ""
def name_of():
    return argv[argv.index("-t") + 1] if "-t" in argv else argv[argv.index("-s") + 1]
def env_of():
    env, i = {}, 0
    while i < len(argv):
        if argv[i] == "-e" and i + 1 < len(argv):
            k, _, v = argv[i + 1].partition("=")
            env[k] = v
            i += 2
        else:
            i += 1
    return env
if sub == "has-session":
    sys.exit(0 if name_of() in state else 1)
if sub in ("new-session", "respawn-pane"):
    name, cwd = name_of(), argv[argv.index("-c") + 1]
    cmd = argv[argv.index("-c") + 2:]
    old = state.get(name, {}).get("pid")
    if old:
        try: os.kill(old, 9)
        except OSError: pass
    child_env = env_of()
    child_env.setdefault("PATH", os.environ.get("PATH", ""))
    proc = subprocess.Popen(cmd, cwd=cwd, env=child_env,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    state[name] = {"pid": proc.pid, "env_keys": sorted(child_env),
                   "respawned": sub == "respawn-pane"}
    json.dump(state, open(state_path, "w"))
    sys.exit(0)
if sub == "list-panes":
    if (os.environ.get("TMUX_SHIM_LIST_PANES_RC") == "1"
            and state.get(name_of(), {}).get("respawned")):
        sys.exit(1)
    if name_of() in state:
        print("%s %d" % (name_of(), state[name_of()]["pid"]))
    sys.exit(0)
sys.exit(0)
'''


@pytest.fixture(autouse=True)
def _no_real_tmux(tmux_shim):
    """Shadow conftest's rc-1 tmux guard so the recording shim is reachable."""
    yield


@pytest.fixture
def tmux_shim(tmp_path, monkeypatch):
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


def _restart(tmp_path, record=None):
    sess = _sess(tmp_path)
    return grok.restart(
        harness={**HARNESS, "bin": _sleeper(tmp_path)}, tier="kid",
        context_file=str(sess / "context.md"), agent_id="a00-seat", iter_n=1,
        sess_dir=sess, agent_record=record, hold_pane=True)


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


# ---------------------------------------------------------------- defect A

def test_pane_spawn_carries_the_scrubbed_child_env(tmp_path, tmux_shim,
                                                   monkeypatch):
    """The pane's child must see the scrubbed env: a non-secret marker kept,
    the grok-bot-forbidden OpenRouter key dropped by the ONE rule."""
    log, state = tmux_shim
    monkeypatch.setenv("OPENROUTER_API_KEY", "SENTINEL-DO-NOT-LEAK")
    monkeypatch.setenv("GROK_TEST_MARKER", "kept")
    pid = _restart(tmp_path)
    text = log.read_text()
    assert "new-session" in text, "non-vacuity: the shim must record a call"
    assert "-e" in text, "the pane spawn must carry env flags"
    keys = json.loads(state.read_text())[grok.pane_name("a00-seat")]["env_keys"]
    assert keys, "non-vacuity: the shim recorded an env"
    assert "GROK_TEST_MARKER" in keys, "the scrubbed env must reach the pane"
    assert "OPENROUTER_API_KEY" not in keys, (
        "drop_unneeded_credential must survive the pane path")
    _reap(pid)


# ---------------------------------------------------------------- defect C

def test_present_but_failing_tmux_is_a_named_refusal(tmp_path, tmux_shim,
                                                     monkeypatch):
    """Every tmux call rc-1 (tmux present, failing): restart must raise
    PaneHoldError and must NOT reach the anonymous Popen fallback."""
    log, _ = tmux_shim
    monkeypatch.setenv("TMUX_SHIM_FAIL_ALL", "1")
    with pytest.raises(grok.PaneHoldError):
        _restart(tmp_path)
    # The fallback opens output.log BEFORE its Popen. It raising instead, and
    # that file being absent, is the observable proof no anonymous spawn ran.
    assert not (_sess(tmp_path) / "output.log").exists(), (
        "failing tmux must never fall back to an anonymous Popen")
    assert "has-session" in log.read_text(), "non-vacuity: tmux was invoked"


# ---------------------------------------------------------------- defect D

def test_failed_list_panes_after_successful_respawn_is_named(tmp_path,
                                                            tmux_shim,
                                                            monkeypatch):
    """A successful respawn whose pid read fails is a NAMED partial state,
    never a bare None that reads as 'not restarted'."""
    log, state = tmux_shim
    rec = {}
    first = _restart(tmp_path, record=rec)
    _reap(first)
    monkeypatch.setenv("TMUX_SHIM_LIST_PANES_RC", "1")
    with pytest.raises(grok.PaneHoldError):
        _restart(tmp_path, record=rec)
    assert log.read_text().count("respawn-pane") == 1, (
        "the respawn itself must have succeeded")
    pid = json.loads(state.read_text())[grok.pane_name("a00-seat")]["pid"]
    assert grok.is_alive(pid), "the pane IS up -- the only thing that failed " \
        "was the pid read"
    _reap(pid)


# -------------------------------------------------------- core, re-anchored

def test_one_new_session_then_one_respawn_at_the_same_name(tmp_path,
                                                           tmux_shim):
    """The kid-1 core claim still holds under the env-threaded spawn."""
    log, state = tmux_shim
    rec = {}
    _restart(tmp_path, record=rec)
    _restart(tmp_path, record=rec)
    text = log.read_text()
    name = grok.pane_name("a00-seat")
    assert text.count("new-session") == 1
    assert text.count("respawn-pane") == 1
    assert name in state.read_text()
    _reap(json.loads(state.read_text())[name]["pid"])
