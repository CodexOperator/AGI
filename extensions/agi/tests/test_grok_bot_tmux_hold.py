"""Grok bot restart uses the same opt-in holder contract as pi."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
from adapters import grok_bot_adapter, tmux_hold


def _sess(tmp_path):
    p = tmp_path / "sess"
    p.mkdir()
    return p


def test_restart_held_uses_exact_child_env(tmp_path, monkeypatch):
    seen = {}
    def start(args, env, *, cwd, pane_name, log_file):
        seen.update(args=args, env=env, cwd=cwd, pane=pane_name)
        return 321
    monkeypatch.setattr(tmux_hold, "enabled", lambda: True)
    monkeypatch.setattr(tmux_hold, "start_held", start)
    monkeypatch.setattr(grok_bot_adapter, "build_command", lambda **kw: ["grok", "run"])
    pid = grok_bot_adapter.restart(
        harness={"needs_credential": False}, tier="kid", context_file="x",
        agent_id="grok-a", iter_n=1, sess_dir=_sess(tmp_path))
    assert pid == 321
    assert seen["pane"] == "agi-grok-a"
    assert seen["env"] == grok_bot_adapter.child_env(
        harness={"needs_credential": False}, base=dict(os.environ), tier="kid")
    assert "OPENROUTER_API_KEY" not in seen["env"]


def test_restart_without_hold_uses_direct_popen(tmp_path, monkeypatch):
    seen = {}
    class P: pid = 123
    monkeypatch.setattr(tmux_hold, "enabled", lambda: False)
    monkeypatch.setattr(grok_bot_adapter, "build_command", lambda **kw: ["grok"])
    monkeypatch.setattr(grok_bot_adapter.subprocess, "Popen",
                        lambda *a, **kw: seen.update(kwargs=kw) or P())
    assert grok_bot_adapter.restart(
        harness={"needs_credential": False}, tier="kid", context_file="x",
        agent_id="grok-b", iter_n=1, sess_dir=_sess(tmp_path)) == 123
    assert seen["kwargs"]["env"] == grok_bot_adapter.child_env(
        harness={"needs_credential": False}, base=dict(os.environ), tier="kid")


def test_restart_missing_tmux_keeps_sanitized_fallback(tmp_path, monkeypatch):
    seen = {}
    class P: pid = 123
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    (tmp_path / "empty").mkdir()
    monkeypatch.setattr(tmux_hold, "enabled", lambda: True)
    monkeypatch.setattr(grok_bot_adapter, "build_command", lambda **kw: ["grok"])
    monkeypatch.setattr(tmux_hold.subprocess, "Popen",
                        lambda *a, **kw: seen.update(kwargs=kw) or P())
    assert grok_bot_adapter.restart(
        harness={"needs_credential": False}, tier="kid", context_file="x",
        agent_id="grok-c", iter_n=1, sess_dir=_sess(tmp_path)) == 123
    assert "OPENROUTER_API_KEY" not in seen["kwargs"]["env"]
