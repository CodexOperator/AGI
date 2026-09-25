"""First-spawn and restart use one reusable held-pane seam."""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import tmux_hold  # noqa: E402


def test_first_start_reuses_the_same_pane_and_receives_child_env(monkeypatch, tmp_path):
    calls = []

    def run(argv, **kwargs):
        calls.append(argv)
        if argv[-1] == "Enter":
            (tmp_path / "state/hold.pid").write_text("77")
        return SimpleNamespace(stdout="%42" if "#{pane_id}" in argv else "")

    monkeypatch.setattr(subprocess, "run", run)
    env = {"AGI_TREE_PROJECT_ROOT": "/tree", "SECRET": "value"}
    first = tmux_hold.start(
        ["pi", "run"], env=env, cwd=tmp_path, log=tmp_path / "out.log",
        mode="wb", seat="sanctuary-director", agent_id="a00-one",
        state_dir=tmp_path / "state")

    assert first.pid == 77
    assert first.pane_id == "%42"
    spec = json.loads((tmp_path / "state/hold.json").read_text())
    assert spec["env"] == env
    assert ["tmux", "new-session", "-d", "-s",
            "agi-hold-sanctuary-director-a00-one"] in calls
    literal = next(c for c in calls
                   if c[:5] == ["tmux", "send-keys", "-t", "%42", "-l"])
    assert "SECRET" not in literal[-1]  # secrets ride the local spec, not tmux argv

    (tmp_path / "state/hold.done").write_text("1")
    assert first.poll() == 1
    assert first.returncode == 1
    second = tmux_hold.start(
        ["pi", "again"], env=env, cwd=tmp_path, log=tmp_path / "out.log",
        mode="ab", seat="sanctuary-director", agent_id="a00-one",
        state_dir=tmp_path / "state", pane_id=first.pane_id)
    assert second.pane_id == first.pane_id
    assert not any("new-session" in c for c in calls[4:])


def test_tmux_unavailable_falls_back_to_direct_popen(monkeypatch, tmp_path):
    seen = {}

    def unavailable(*args, **kwargs):
        raise FileNotFoundError("tmux")

    def popen(argv, **kwargs):
        seen.update(argv=argv, kwargs=kwargs)
        return SimpleNamespace(pid=123)

    monkeypatch.setattr(subprocess, "run", unavailable)
    monkeypatch.setattr(subprocess, "Popen", popen)
    proc = tmux_hold.start_or_popen(
        ["pi", "run"], env={"A": "B"}, cwd=tmp_path, log=tmp_path / "out.log",
        mode="wb", seat="seat", agent_id="a00-two", state_dir=tmp_path / "state")
    assert proc.pid == 123
    assert seen["kwargs"]["env"] == {"A": "B"}
    assert seen["kwargs"]["start_new_session"] is True


def test_dispatch_open_round_calls_only_the_named_hold_seam():
    tree = ast.parse((BIN / "dispatch.py").read_text())
    open_round = next(n for n in ast.walk(tree)
                      if isinstance(n, ast.FunctionDef) and n.name == "_open_round")
    calls = [n for n in ast.walk(open_round) if isinstance(n, ast.Call)]
    assert any(isinstance(c.func, ast.Attribute)
               and c.func.attr == "start_or_popen" for c in calls)
    assert not any(isinstance(c.func, ast.Attribute) and c.func.attr == "Popen"
                   for c in calls)
