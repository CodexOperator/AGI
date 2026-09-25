from __future__ import annotations
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import tmux_hold


def test_empty_or_anonymous_pane_is_not_identity(monkeypatch):
    monkeypatch.setattr(tmux_hold, "_run", lambda *a: "")
    assert tmux_hold.pane("agi-rc", "seat") is None


def test_named_pane_is_reused_and_pid_stable(monkeypatch, tmp_path):
    calls = []
    def run(*args):
        calls.append(args)
        if args[:2] == ("display-message", "-p"):
            return "@7" if args[-1] == "#{pane_id}" else "42"
        return "@7"
    monkeypatch.setattr(tmux_hold, "_run", run)
    pid = tmux_hold.start(name="seat", argv=["agent", "-p", "ctx"], cwd=tmp_path,
                          env={"A": "B"}, log_file=tmp_path / "out.log")
    assert pid == 42
    assert not any(c and c[0] == "new-window" for c in calls)
    assert any(c[:2] == ("send-keys", "-t") and c[2] == "@7" for c in calls)


def test_first_spawn_names_the_pane(monkeypatch, tmp_path):
    def run(*args):
        if args[:2] == ("display-message", "-p"):
            return "" if args[-1] == "#{pane_id}" else "99"
        return "@8"
    monkeypatch.setattr(tmux_hold, "_run", run)
    assert tmux_hold.start(name="seat", argv=["agent"], cwd=tmp_path,
                           env={}, log_file=tmp_path / "out.log") == 99
