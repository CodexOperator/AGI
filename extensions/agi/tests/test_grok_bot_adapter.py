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
    callable. Practice stub: `restart` raises NotImplementedError until CLI
    flags are measured (Belam locked stub restart OK for g17.14)."""
    for fn in adapters.REQUIRED:
        assert callable(getattr(grok, fn)), fn
    with pytest.raises(NotImplementedError) as exc:
        grok.restart(harness=HARNESS, tier="kid", context_file="/tmp/x")
    msg = str(exc.value).lower()
    assert "unmeasured" in msg or "flag" in msg or "build_command" in msg


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


# -------------------------------------------------------- live config row
# The tests above build their `cfg` in memory, so they would stay green even
# if the shipped `.agi/config.json` lost the `grok-bot` row. These read the
# REAL config from disk -- read-only, never written -- so the row the live
# harnesses actually use is the thing asserted (`hypothesis:grok-bot-live-
# config-row-has-a-pytest`).


def _project_root() -> Path:
    """Nearest ancestor holding a real `.agi/config.json` (`goal:g11`).

    Walked up from this file, never hardcoded: the root is three levels above
    `extensions/agi/tests/` today, and the walk survives the test moving.
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / ".agi" / "config.json").is_file():
            return parent
    raise AssertionError(f"no .agi/config.json above {__file__}")


@pytest.fixture(scope="module")
def live_cfg() -> dict:
    """The project's real config, loaded read-only."""
    import json

    path = _project_root() / ".agi" / "config.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_live_config_grok_row_resolves(live_cfg):
    """The on-disk `grok-bot` row resolves to the adapter, with the live bin.

    `bin` is asserted against the loaded cell, not a literal, so the test
    tracks the config instead of freezing one path.
    """
    name, row = adapters.resolve(live_cfg, "grok-bot")
    assert name == "grok-bot"
    assert row["adapter"] == "grok_bot"
    assert row["bin"] == live_cfg["harnesses"]["grok-bot"]["bin"]


def test_live_config_peers_still_resolve(live_cfg):
    """Adding the fourth harness did not disturb the three already declared."""
    pname, prow = adapters.resolve(live_cfg, "pi")
    assert pname == "pi"
    assert prow["adapter"] == "pi"
    cname, crow = adapters.resolve(live_cfg, "copilot-cli")
    assert cname == "copilot-cli"
    assert crow["adapter"] == "copilot_cli"


def test_dispatch_still_has_zero_grok_hits():
    """The whole point of `goal:g4.6`: adding a harness edits no dispatch code."""
    dispatch = _project_root() / "extensions" / "agi" / "bin" / "dispatch.py"
    assert "grok" not in dispatch.read_text(encoding="utf-8").lower()
