"""Tests for bin/adapters/grok_bot_adapter.py. `goal:g17.14.3`, fourth harness.

Mirror of `test_claude_code_adapter.py` / `test_copilot_cli_adapter.py`: guard
the surface every adapter must expose (`goal:g4.6`) and the tier contract this
one must not soften. The adapter and its live config row are owned by siblings
`goal:g17.14.1` (`bin/adapters/grok_bot_adapter.py`) and `goal:g17.14.2`
(`harnesses.grok-bot`). This file is TEST-ONLY: it neither implements the
adapter nor edits the config, so until `.1`/`.2` land the `importorskip` below
skips the whole file rather than collection-failing the suite.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

grok = pytest.importorskip(
    "adapters.grok_bot_adapter",
    reason="grok-bot adapter not yet landed (goal:g17.14.1 owns the module; "
           "goal:g17.14.2 owns its .agi/config.json row)",
)

#: A config row shaped the way `adapters.resolve` synthesizes the adapter stem
#: for a `grok-bot` harness name.
HARNESS = {"adapter": "grok_bot",
           "models": {"kid": "grok-kid", "parent": "grok-parent"}}


# ---------------------------------------------------------------- interface


def test_name_is_non_empty():
    assert isinstance(grok.NAME, str) and grok.NAME


def test_adapter_implements_the_whole_interface_not_a_stub():
    """`adapters.load` only proves the names exist; this proves `restart` is
    real (`goal:g4.7`), not a stub that raises where the work goes."""
    for fn in adapters.REQUIRED:
        assert callable(getattr(grok, fn)), fn
    assert callable(grok.restart)


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