"""Wire-level checks for the first-spawn tmux hold seam."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
spec = importlib.util.spec_from_file_location("tmux_hold", BIN / "tmux_hold.py")
tmux_hold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tmux_hold)


def test_start_is_a_named_tmux_session_not_anonymous_popen(monkeypatch, tmp_path):
    calls = []
    class P:
        pid = 4242

    def popen(argv, **kw):
        calls.append((argv, kw))
        return P()

    monkeypatch.setattr(tmux_hold.subprocess, "Popen", popen)
    proc = tmux_hold.start(["pi", "--model", "fake"], cwd=tmp_path,
                           env={"A": "B"}, log=tmp_path / "output.log",
                           name="a00-first-spawn")
    assert proc.pid == 4242
    argv, kw = calls[0]
    assert argv[:3] == ["tmux", "new-session", "-s"]
    assert argv[3] == "a00-first-spawn"
    assert "pi --model fake" in argv[-1]
    assert kw["start_new_session"] is True


def test_reattach_and_pane_use_the_same_name(monkeypatch):
    calls = []
    monkeypatch.setattr(tmux_hold.subprocess, "run",
                        lambda argv, **kw: calls.append(argv))
    tmux_hold.reattach("a00-first-spawn")
    assert calls[0][-1] == "a00-first-spawn"
    # A reattach after kill -9 is addressed to the durable name, not a PID.
    assert "kill" not in calls[0]


def test_dispatch_first_spawn_reaches_the_hold_module():
    source = (BIN / "dispatch.py").read_text()
    assert "def _open_round(mode: str):" in source
    assert "tmux_hold.start(" in source
    assert "subprocess.Popen(\n                    mem_cap.wrap_argv" not in source
