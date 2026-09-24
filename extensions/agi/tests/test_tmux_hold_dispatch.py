import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "bin"))
from adapters import tmux_hold


def test_start_is_stable_and_fallback_is_honest(monkeypatch):
    calls = []
    rows = iter(["", "%1\t/seat\t101\n", "%1\t/seat\t202\n", "%1\t/seat\t202\n", "%1\t/seat\t202\n"])
    monkeypatch.setattr(tmux_hold, "_run", lambda argv, **kw: type("R", (), {
        "stdout": next(rows), "returncode": 0})())
    first = tmux_hold.start("seat", ["pi", "x"], cwd="/workspace")
    second = tmux_hold.reattach("seat", ["pi", "x"], cwd="/workspace")
    assert first["pane_id"] == second["pane_id"] == "%1"
    assert first["created"] is False and second["created"] is False
    assert calls == []


def test_start_returns_none_when_tmux_fails(monkeypatch):
    monkeypatch.setattr(tmux_hold, "_run", lambda argv, **kw: type("R", (), {
        "stdout": "", "returncode": 1})())
    assert tmux_hold.start("seat", ["pi"]) is None
