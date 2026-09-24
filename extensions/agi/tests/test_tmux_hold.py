import importlib
import sys
from pathlib import Path


def _module():
    root = Path(__file__).parents[1]
    sys.path.insert(0, str(root / "bin"))
    return importlib.import_module("adapters.tmux_hold")


def test_fallback_preserves_env_when_tmux_unavailable(monkeypatch):
    m = _module()
    calls = []
    def popen(argv, **kw):
        calls.append((argv, kw))
        return type("Child", (), {"pid": 17})()
    out = m.restart(["agent"], {"KEEP": "yes"}, tmux_available=False,
                    session_exists=False, reattach=lambda: None, popen=popen)
    assert out == 17
    assert calls == [(["agent"], {"env": {"KEEP": "yes"}})]


def test_fallback_when_session_missing(monkeypatch):
    m = _module()
    def popen(*args, **kwargs):
        return type("Child", (), {"pid": 18})()
    assert m.restart(["agent"], {}, tmux_available=True, session_exists=False,
                     reattach=lambda: 99, popen=popen) == 18


def test_healthy_session_prefers_reattach(monkeypatch):
    m = _module()
    def popen(*args, **kwargs):
        raise AssertionError("must not spawn")
    assert m.restart(["agent"], {}, tmux_available=True, session_exists=True,
                     reattach=lambda: 21, popen=popen) == 21
