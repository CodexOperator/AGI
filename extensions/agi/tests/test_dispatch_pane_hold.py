"""`goal:g7.31.1.2` residual closure, END TO END through DISPATCH.

The prior rounds proved the adapter's own `spawn`/`restart` reuse `%N`, but
`dispatch._open_round` still called `subprocess.Popen` directly and the config
had no generic `pane` cell -- so a real persistent round was fire-and-forget
and there was nothing for a restart to reattach to.

This file drives the REAL `dispatch.main()` spawn path:

  1. `--persistent` dispatch of a sleeping fake harness with `pane: true`,
  2. a live NAMED tmux pane exists and the manifest record carries `pane`,
  3. SIGKILL the pane's process,
  4. the persistent supervisor's `reopen` reattaches the SAME `%N`/window
     with a NEW `pane_pid`.

A throwaway `-L` tmux socket is used; the live `agi-rc` session is never
touched (the tmux shim below delegates to real tmux on that socket, and
conftest's autouse guard answers any unshimmed tmux call rc-1).
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

from adapters import pane_hold  # noqa: E402

REAL_TMUX = shutil.which("tmux")
_REAL_RUN = subprocess.run  # captured BEFORE conftest's autouse guard


def _load_dispatch():
    spec = importlib.util.spec_from_file_location(
        "agi_dispatch_pane", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()


def _project(tmp_path: Path, session: str) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"grok-bot": {
            "adapter": "grok_bot", "provider": "fake",
            "models": {"kid": "grok-4-fast"}, "allowed_extra": ["grok-4-fast"],
            "bin": str(tmp_path / "seat.sh"), "pane": True,
            "pane_session": session,
        }},
        "spawn": {"harness": "grok-bot", "parallel": 1, "max_live": 25,
                  "memory_max": None},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: grok-bot, model: grok-4-fast}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    seat = tmp_path / "seat.sh"
    seat.write_text("#!/bin/bash\nsleep 300\n")
    seat.chmod(0o755)
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR", dispatch._PERSIST_STOP_ENV):
        os.environ.pop(k, None)
    return tmp_path


def _wait(pred, timeout: float, what: str):
    deadline = time.time() + timeout
    while time.time() < deadline:
        value = pred()
        if value:
            return value
        time.sleep(0.05)
    raise AssertionError(f"timed out waiting for {what}")


def _windows(session: str) -> list[str]:
    out = subprocess.run(
        ["tmux", "list-windows", "-t", session, "-F", "#{window_name}"],
        capture_output=True, text=True)
    return [w for w in out.stdout.split() if w] if out.returncode == 0 else []


def test_persistent_dispatch_births_a_pane_and_reattaches_the_same_id(
        tmp_path, monkeypatch):
    if not REAL_TMUX:
        pytest.skip("tmux not installed")
    session = f"agi-dispatch-{os.getpid()}-{os.urandom(3).hex()}"
    project = _project(tmp_path, session)
    sock = f"agi-dispatch-pane-{os.getpid()}-{os.urandom(4).hex()}"
    monkeypatch.setenv("FAKE_TMUX_SOCKET", sock)
    guard = subprocess.run

    def _run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            return _REAL_RUN([REAL_TMUX, "-L", sock, *cmd[1:]], *a, **k)
        return guard(cmd, *a, **k)

    monkeypatch.setattr(subprocess, "run", _run)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", lambda s: time.sleep(0.05))
    monkeypatch.setattr(sys, "argv", [
        str(BIN / "dispatch.py"), str(project), "1",
        "--level", "small", "--harness", "grok-bot", "--tier", "kid",
        "--target", "hypothesis:x", "--persistent"])

    result: dict = {}

    def _run_dispatch():
        try:
            result["rc"] = dispatch.main()
        except BaseException as exc:  # noqa: BLE001
            result["err"] = exc

    thread = threading.Thread(target=_run_dispatch, daemon=True)
    thread.start()
    try:
        name = _wait(lambda: (_windows(session) or [None])[0], 20,
                     "the seat's named pane")
        pane0 = _wait(lambda: pane_hold.pane_id(tmux_session=session,
                                                name=name), 20, "pane %N")
        pid0 = pane_hold.pane_pid(tmux_session=session, name=name)
        assert pid0, "the pane must have a live process"

        os.kill(pid0, signal.SIGKILL)
        pid1 = _wait(
            lambda: (lambda p: p if p and p != pid0 else None)(
                pane_hold.pane_pid(tmux_session=session, name=name)),
            120, "the supervisor's restart in the SAME pane")
        assert pane_hold.pane_id(tmux_session=session, name=name) == pane0, (
            "restart must reattach the SAME %N")
        assert pid1 != pid0
        assert pane_hold.pane_field(tmux_session=session, name=name,
                                    field="pane_dead") == "0"

        os.environ[dispatch._PERSIST_STOP_ENV] = "1"
        thread.join(timeout=20)
        assert not thread.is_alive(), "the supervisor must stop on the signal"

        assert result.get("rc") == 0, result
        agents = json.loads(sorted(
            project.glob(".agi/sessions/**/manifest.json"))[0].read_text())["agents"]
        assert agents and agents[0].get("pane") == name, agents
        assert agents[0].get("pane_id") == pane0, agents
        assert agents[0].get("pane_session") == session, agents
    finally:
        os.environ.pop(dispatch._PERSIST_STOP_ENV, None)
        _REAL_RUN([REAL_TMUX, "-L", sock, "kill-server"], check=False)
