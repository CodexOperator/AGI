"""Tests for bin/adapters/grok_bot_adapter.py. `goal:g17.14.3`, fourth harness.

Mirror of `test_claude_code_adapter.py` / `test_copilot_cli_adapter.py`: guard
the surface every adapter must expose (`goal:g4.6`) and the tier contract this
one must not soften. After g17.14.1/.2 land, import the module directly (same
as copilot/claude) so a present-but-broken adapter fails the suite instead of
being swallowed by `importorskip`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

grok = adapters.load("grok_bot")

#: A config row shaped the way `adapters.resolve` synthesizes the adapter stem
#: for a `grok-bot` harness name.
HARNESS = {"adapter": "grok_bot",
           "models": {"kid": "grok-kid", "parent": "grok-parent"}}


# ---------------------------------------------------------------- interface


def test_name_is_the_harness_literal():
    """NAME must be the harness string seats/config use, not a non-empty guess."""
    assert grok.NAME == "grok-bot"


def test_adapter_implements_the_whole_interface():
    """`adapters.load` only proves the names exist; every REQUIRED name is
    callable. `restart` is now a real respawn (`goal:g4.7`) — the locked
    NotImplementedError stub is gone (goal:g17.14.1)."""
    for fn in adapters.REQUIRED:
        assert callable(getattr(grok, fn)), fn
    with pytest.raises(TypeError):
        grok.restart()  # keyword-only contract, but no longer NotImplementedError


def test_is_alive_tracks_a_live_pid_and_not_a_reaped_one():
    assert grok.is_alive(os.getpid()) is True
    pid = os.fork()
    if pid == 0:
        os._exit(0)
    os.waitpid(pid, 0)
    assert grok.is_alive(pid) is False


def test_needs_no_openrouter_credential():
    """grok-bot authenticates on its own channel, so dispatch must not mint a
    per-spawn OpenRouter key for it: the EXPLICIT `False` claude_code and
    copilot_cli return -- a bool, not `None`, not an AttributeError."""
    assert grok.needs_credential(HARNESS) is False


# ------------------------------------------------------------- tier contract


def test_missing_tier_is_a_named_error_not_a_fallback():
    """A tier absent from a declared `models` block must raise a KeyError
    naming the tier, never quietly run on another tier's model."""
    with pytest.raises(KeyError) as exc:
        grok.model_args({"adapter": "grok_bot", "models": {"kid": "only"}}, "parent")
    assert "parent" in str(exc.value)


def test_no_models_block_passes_no_model_flags():
    assert "--model" not in grok.model_args({"adapter": "grok_bot"}, "kid")


# ------------------------------------------------------------ config resolve


def test_config_entry_resolves_to_this_adapter():
    cfg = {"harnesses": {"grok-bot": HARNESS, "pi": {"adapter": "pi"}},
           "spawn": {"harness": "pi"}}
    name, harness = adapters.resolve(cfg, "grok-bot")
    assert name == "grok-bot"
    assert adapters.load(harness["adapter"]) is grok


def test_bare_row_defaults_the_adapter_to_the_module_stem():
    """A `grok-bot` row with no `adapter` key defaults to `grok_bot`, the
    module stem `adapters.load` expects (the `.` -> `_` mapping)."""
    cfg = {"harnesses": {"grok-bot": {"models": {"kid": "grok-kid"}}}}
    name, harness = adapters.resolve(cfg, "grok-bot")
    assert name == "grok-bot"
    assert harness["adapter"] == "grok_bot"
    assert adapters.load(harness["adapter"]) is grok


# ----------------------------------------------------------------- restart

RESTART_HARNESS = {"adapter": "grok_bot", "bin": "grok-bot",
                   "models": {"kid": "grok-kid", "parent": "grok-parent"}}


def test_restart_is_a_real_respawn_not_a_stub():
    """The old stub raised NotImplementedError; the contract is now the same
    as copilot_cli/pi (`goal:g4.7`): callable, returns a pid."""
    assert callable(grok.restart)


def test_restart_returns_the_new_pid_and_stamps_the_record(monkeypatch, tmp_path):
    """Popen faked so no real `grok-bot` binary is needed. Rebuilds the
    identical argv via build_command, spawns detached, stamps the record."""
    captured = {}

    class FakeProc:
        pid = 5252

    def fake_popen(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeProc()

    monkeypatch.setattr(grok.subprocess, "Popen", fake_popen)
    sess = tmp_path / "sess"
    sess.mkdir()
    rec = {"worktree": str(tmp_path)}
    pid = grok.restart(harness=RESTART_HARNESS, tier="kid",
                       context_file=str(tmp_path / "context.md"),
                       agent_id="a00-test", iter_n=1, sess_dir=sess,
                       scaffold=None, target="goal:g17.14.1",
                       agent_record=rec)
    assert pid == 5252
    # argv is exactly what build_command produces (stub argv today)
    assert captured["args"] == grok.build_command(
        harness=RESTART_HARNESS, tier="kid",
        context_file=str(tmp_path / "context.md"))
    assert captured["kwargs"]["cwd"] == str(tmp_path)
    assert captured["kwargs"]["start_new_session"] is True
    assert rec["pid"] == 5252
    assert rec["status"] == "restarted"
    assert isinstance(rec["restarted_at"], int)
    import json as _json
    written = _json.loads((sess / "agent.json").read_text())
    assert written["pid"] == 5252 and written["status"] == "restarted"


def test_restart_returns_none_when_popen_fails(monkeypatch, tmp_path):
    """An OSError from Popen yields None, never a raised exception — same as
    the other adapters."""
    def boom(args, **kwargs):
        raise OSError("no such binary")

    monkeypatch.setattr(grok.subprocess, "Popen", boom)
    sess = tmp_path / "sess"
    sess.mkdir()
    assert grok.restart(harness=RESTART_HARNESS, tier="kid",
                        context_file=str(tmp_path / "context.md"),
                        agent_id="a00-test", iter_n=1, sess_dir=sess) is None
