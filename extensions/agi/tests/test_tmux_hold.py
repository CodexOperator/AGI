"""The tmux hold seam must carry an explicit, sanitized environment."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import tmux_hold


def test_start_and_reattach_forward_environment(monkeypatch):
    calls = []
    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs["env"]))
        return object()
    monkeypatch.setattr(tmux_hold.subprocess, "run", fake_run)
    env = {"PATH": "/bin", "SENTINEL": "yes"}
    tmux_hold.start(pane="seat", argv=["agent"], env=env)
    tmux_hold.reattach(pane="seat", env=env)
    assert calls[0][0] == ["tmux", "new-window", "-t", "seat", "-n", "seat", "--", "agent"]
    assert calls[0][1] == calls[1][1] == env


def test_missing_environment_is_not_server_inheritance(monkeypatch):
    seen = {}
    monkeypatch.setattr(tmux_hold.subprocess, "run",
                        lambda argv, **kw: seen.update(kw) or object())
    tmux_hold.reattach(pane="seat", env={})
    assert seen["env"] == {}
