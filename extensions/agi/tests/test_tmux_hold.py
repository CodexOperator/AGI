"""The tmux hold seam must carry an explicit, sanitized environment."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
from adapters import tmux_hold


def test_start_only_creates_absent_window_with_explicit_env(monkeypatch):
    calls = []
    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs["env"]))
        if argv[1] == "list-windows":
            raise tmux_hold.subprocess.CalledProcessError(1, argv)
        return object()
    monkeypatch.setattr(tmux_hold.subprocess, "run", fake_run)
    env = {"PATH": "/bin", "SENTINEL": "yes"}
    tmux_hold.start(pane="seat", argv=["agent"], env=env)
    assert calls[-1][0] == ["tmux", "new-window", "-t", "seat", "-n", "seat", "--",
                            "env", "PATH=/bin", "SENTINEL=yes", "agent"]
    assert calls[-1][1] == env


def test_hold_pane_respawns_existing_window_and_returns_live_pid(monkeypatch):
    calls = []
    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs["env"]))
        if argv[-1] == "#{pane_pid}":
            return type("Result", (), {"stdout": "4242"})()
        return type("Result", (), {"stdout": "@1"})()
    monkeypatch.setattr(tmux_hold.subprocess, "run", fake_run)
    env = {"PATH": "/bin", "SENTINEL": "yes"}
    assert tmux_hold.hold_pane(pane="seat", argv=["agent"], env=env) == 4242
    assert calls[1][0] == ["tmux", "respawn-window", "-k", "-t", "seat", "--",
                            "env", "PATH=/bin", "SENTINEL=yes", "agent"]
    assert all(call[1] == env for call in calls)
    assert calls[-1][0] == ["tmux", "display-message", "-p", "-t", "seat", "#{pane_pid}"]


def test_missing_environment_is_not_server_inheritance(monkeypatch):
    seen = {}
    monkeypatch.setattr(tmux_hold.subprocess, "run",
                        lambda argv, **kw: seen.update(kw) or object())
    tmux_hold.reattach(pane="seat", env={})
    assert seen["env"] == {}
