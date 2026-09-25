"""Production first-spawn founds a durable named tmux pane."""
from __future__ import annotations

import ast
import hashlib
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dispatch  # noqa: E402


def test_tmux_start_founds_named_pane_and_truthful_created(monkeypatch, tmp_path):
    calls, state = [], {}

    def run(argv, **kwargs):
        calls.append(list(argv))
        out = ""
        if argv[1:2] == ("list-panes",):
            out = "other %9\n"
        elif argv[1:2] == ("display-message",):
            out = "%42" if argv[-1] == "#{pane_id}" else "77"
        return SimpleNamespace(stdout=out)

    monkeypatch.setattr(subprocess, "run", run)
    proc = dispatch._tmux_start(
        ["sleep", "600"], env={"SECRET": "value"}, cwd=tmp_path,
        log=tmp_path / "out.log", seat="point director", agent_id="a00-x",
        state=state)
    assert proc.pid == 77
    expected = ("agi-hold-pointdirector-a00-x-" +
                hashlib.sha256("point director\0a00-x".encode()).hexdigest()[:16])
    assert state == {"held": True, "created": True, "pane_id": "%42",
                     "session": expected, "pid": 77}
    assert ["tmux", "new-session", "-d", "-s", state["session"], "-c",
            str(tmp_path), 'sh -c "sleep 86400"'] in calls
    respawn = next(c for c in calls if c[1] == "respawn-pane")
    assert respawn[:7] == ["tmux", "respawn-pane", "-k", "-t", "%42",
                           "-c", str(tmp_path)]
    assert "SECRET=value" in respawn
    assert "sleep" in respawn[-1] and "600" in respawn[-1]


def test_long_names_with_shared_prefix_get_distinct_sessions(monkeypatch, tmp_path):
    sessions = []

    def run(argv, **kwargs):
        if argv[1:2] == ("list-panes",):
            return SimpleNamespace(stdout="")
        if argv[1:2] == ("display-message",):
            return SimpleNamespace(stdout="%99" if argv[-1] == "#{pane_id}" else "88")
        return SimpleNamespace(stdout="")

    monkeypatch.setattr(subprocess, "run", run)
    for agent in ("a00-" + "x" * 50, "a00-" + "x" * 51):
        state = {}
        dispatch._tmux_start(["sleep"], env={}, cwd=tmp_path,
                             log=tmp_path / "log", seat="s" * 70,
                             agent_id=agent, state=state)
        sessions.append(state["session"])
    assert sessions[0] != sessions[1]
    assert all(s.startswith("agi-hold-") and len(s) > 60 for s in sessions)


def test_tmux_absent_falls_back_and_names_degradation(monkeypatch, tmp_path):
    calls, state = [], {}

    def absent(argv, **kwargs):
        calls.append(argv)
        if argv[0] == "tmux":
            raise FileNotFoundError("tmux")
        return SimpleNamespace(pid=123)

    monkeypatch.setattr(subprocess, "run", absent)
    monkeypatch.setattr(subprocess, "Popen", absent)
    assert dispatch._tmux_start(
        ["sleep"], env={}, cwd=tmp_path, log=tmp_path / "log", seat="seat",
        agent_id="a00-y", state=state) is None
    assert state["held"] is False and state["created"] is False
    assert "tmux" in state["reason"]


def test_open_round_has_no_direct_popen_fallback_of_its_own():
    tree = ast.parse((BIN / "dispatch.py").read_text())
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "_open_round")
    assert any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == "_tmux_start" for n in ast.walk(fn))
