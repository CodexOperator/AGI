from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import adapters.tmux_hold as hold


def test_restart_falls_back_to_popen_without_tmux(monkeypatch):
    calls = []
    monkeypatch.setattr(hold.shutil, "which", lambda _: None)
    monkeypatch.setattr(hold.subprocess, "Popen", lambda *a, **kw: calls.append((a, kw)) or type("P", (), {"pid": 91})())
    assert hold.restart(["agent", "--run"], session="agi") == 91
    assert calls and calls[0][0][0] == ["agent", "--run"]


def test_restart_falls_back_when_session_missing(monkeypatch):
    calls = []
    monkeypatch.setattr(hold, "tmux_available", lambda _: False)
    monkeypatch.setattr(hold.subprocess, "Popen", lambda *a, **kw: calls.append((a, kw)) or type("P", (), {"pid": 92})())
    assert hold.restart(["agent"], session=None) == 92
    assert calls
