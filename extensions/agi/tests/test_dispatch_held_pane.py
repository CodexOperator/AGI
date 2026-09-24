"""The dispatch spawn path must cross the held-pane seam, not anonymous Popen."""
from pathlib import Path
import sys

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import dispatch  # noqa: E402


def test_open_held_pane_returns_real_pane_identity(monkeypatch, tmp_path):
    calls = []

    class Result:
        stdout = "%7 4321\n"

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        return Result()

    monkeypatch.setattr(dispatch.subprocess, "run", run)
    proc, pane_id = dispatch._open_held_pane(
        ["pi", "run"], cwd=str(tmp_path), env={"AGI_TIER": "kid"},
        log_file=tmp_path / "output.log")
    assert pane_id == "%7"
    assert proc.pid == 4321
    assert calls[0][0][0] == "tmux"
    assert "new-window" in calls[0][0]
    assert calls[0][1]["check"] is True
