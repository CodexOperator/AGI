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
import dispatch  # noqa: E402
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


def test_new_session_is_killed_but_supplied_restart_pane_is_not(monkeypatch, tmp_path):
    created, restarted = [], []
    failure = subprocess.CalledProcessError(1, ["tmux"])

    def created_run(argv, **kwargs):
        created.append(argv)
        if "display-message" in argv:
            raise failure
        return SimpleNamespace(stdout="%9" if "new-session" in argv else "")

    def restarted_run(argv, **kwargs):
        restarted.append(argv)
        if "send-keys" in argv:
            raise failure
        return SimpleNamespace(stdout="")

    state = tmp_path / "state"
    common = dict(env={"A": "B"}, cwd=tmp_path, log=tmp_path / "out.log",
                  mode="wb", seat="seat", agent_id="a00-three",
                  state_dir=state)
    monkeypatch.setattr(subprocess, "run", created_run)
    assert tmux_hold.start(["pi"], **common) is None
    assert ["tmux", "kill-session", "-t",
            "agi-hold-seat-a00-three"] in created
    assert not (state / "hold.json").exists()

    monkeypatch.setattr(subprocess, "run", restarted_run)
    assert tmux_hold.start(["pi"], **common, pane_id="%7") is None
    assert not any("kill-session" in argv for argv in restarted)
    assert not (state / "hold.json").exists()


def test_run_consumes_spec_even_when_child_start_fails(monkeypatch, tmp_path):
    spec = tmp_path / "hold.json"
    spec.write_text(json.dumps({"argv": ["pi"], "env": {}, "cwd": str(tmp_path),
                                "log": str(tmp_path / "out.log"), "mode": "wb"}))
    monkeypatch.setattr(subprocess, "Popen",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("start")))
    try:
        tmux_hold._run(str(spec))
    except OSError:
        pass
    assert not spec.exists()


def test_fast_rc_zero_startup_skips_grace_wait(monkeypatch):
    def unexpected_sleep(_seconds):
        raise AssertionError("rc=0 process must not enter startup grace")

    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", unexpected_sleep)
    proc = SimpleNamespace(returncode=0)
    assert dispatch._startup_alive_or_complete(proc)


def test_dispatch_open_round_calls_only_the_named_hold_seam():
    tree = ast.parse((BIN / "dispatch.py").read_text())
    open_round = next(n for n in ast.walk(tree)
                      if isinstance(n, ast.FunctionDef) and n.name == "_open_round")
    calls = [n for n in ast.walk(open_round) if isinstance(n, ast.Call)]
    seam = next(c for c in calls if isinstance(c.func, ast.Attribute)
                and c.func.attr == "start_or_popen")
    keywords = {kw.arg for kw in seam.keywords}
    assert {"env", "cwd", "log", "mode", "seat", "agent_id", "state_dir"} <= keywords
    assert not any(isinstance(c.func, ast.Attribute) and c.func.attr == "Popen"
                   for c in calls)
