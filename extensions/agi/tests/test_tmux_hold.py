from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
from adapters import tmux_hold  # noqa: E402


def test_unset_session_falls_back_to_direct_popen(monkeypatch):
    calls = []
    spawner = lambda *a, **kw: calls.append((a, kw)) or "direct"
    result = tmux_hold.hold(["seat"], session="", pane="prime", spawner=spawner)
    assert result == "direct"
    assert calls[0][0] == (["seat"],)


def test_missing_tmux_falls_back_to_direct_popen(monkeypatch):
    calls = []
    def absent(*_a, **_kw):
        raise FileNotFoundError("tmux")
    spawner = lambda *a, **kw: calls.append((a, kw)) or "direct"
    result = tmux_hold.hold(["seat"], session="agi", pane="prime",
                            runner=absent, spawner=spawner)
    assert result == "direct"
    assert calls == [((["seat"],), {"cwd": None, "env": None})]


def test_existing_named_pane_reattaches(monkeypatch):
    calls = []
    def run(argv, **_kw):
        calls.append(argv)
        return SimpleNamespace(returncode=0)
    result = tmux_hold.hold(["seat"], session="agi", pane="prime", runner=run)
    assert result.returncode == 0
    assert calls == [["tmux", "has-session", "-t", "agi:prime"],
                     ["tmux", "attach-session", "-t", "agi:prime"]]


def test_new_named_pane_is_started_detached(monkeypatch):
    calls = []
    def run(argv, **_kw):
        calls.append(argv)
        return SimpleNamespace(returncode=1 if "has-session" in argv else 0)
    result = tmux_hold.hold(["seat"], session="agi", pane="prime", runner=run)
    assert result.returncode == 0
    assert calls[-1] == ["tmux", "new-session", "-d", "-s", "agi",
                         "-n", "prime", "seat"]
