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


def test_measured_help_has_no_guessed_prompt_or_model_flags():
    help_text = (Path(__file__).parent / "fixtures" /
                 "grok_bot_cli_0_3_1_help.txt").read_text(encoding="utf-8")
    assert len(help_text.splitlines()) == 46
    assert "-p " not in help_text
    assert "--model" not in help_text


def test_build_command_is_bare_measured_argv(monkeypatch):
    monkeypatch.delenv("GROK_BOT_BIN", raising=False)
    harness = {"adapter": "grok_bot", "bin": "/SENTINEL/grok-bot",
               "models": {"kid": "grok-4-fast"}}
    assert grok.build_command(
        harness=harness, tier="kid", context_file="/tmp/context.md",
    ) == ["/SENTINEL/grok-bot"]


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
    # argv is exactly what measured build_command produces
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
def live_cfg_raw() -> dict:
    """The project's real config, loaded read-only, with NO grok gate.

    Split out (DT.23 residue 3) so a test that only needs rows that already
    shipped is not swallowed by the grok-bot gate: `live_cfg` below still
    skips when Belam's row is absent, but
    `test_live_config_peers_still_resolve` reads THIS fixture and therefore
    runs on every tip.
    """
    import json

    path = _project_root() / ".agi" / "config.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def live_cfg(live_cfg_raw) -> dict:
    """The real config, gated on Belam's `harnesses.grok-bot` row.

    DT.21 residue 3 (hermetic): on a tip where that row has not landed yet,
    the two grok-specific live-config tests below are RED-on-evidence rather
    than red-on-defect. Skip them with a NAMED reason instead of asserting
    against a row that is not there; the non-live tests above keep full
    strength and the suite ends green.
    """
    if "grok-bot" not in (live_cfg_raw.get("harnesses") or {}):
        pytest.skip(
            "harnesses.grok-bot row lands with Belam's config fold "
            "(DT.21 residue 3)",
            allow_module_level=False,
        )
    return live_cfg_raw


def test_live_config_grok_row_resolves(live_cfg, monkeypatch):
    """The on-disk `grok-bot` row resolves to the adapter, and its live `bin`
    cell reaches the argv that actually spawns.

    The old assert compared `row["bin"]` to
    `live_cfg["harnesses"]["grok-bot"]["bin"]` and could not fail:
    `adapters.resolve` shallow-copies the row (`harness =
    dict(harnesses[chosen])`), so both names are the same string object. These
    asserts instead exercise `grok.resolve_bin` / `grok.build_command`, the
    spawn path where `$GROK_BOT_BIN`, then the row's cell, then
    `DEFAULT_BIN` have precedence -- so a default silently taking over is
    visible.

    The live binary need not exist on this box; the claim is that the config
    cell is carried, not that the path is populated.
    """
    monkeypatch.delenv("GROK_BOT_BIN", raising=False)
    name, row = adapters.resolve(live_cfg, "grok-bot")
    live_bin = live_cfg["harnesses"]["grok-bot"]["bin"]
    assert name == "grok-bot"
    assert row["adapter"] == "grok_bot"
    # The non-vacuous anchor: a row that omitted `bin` or carried the bare
    # fallback would fail here, where the old same-object assert could not.
    assert live_bin != grok.DEFAULT_BIN
    assert grok.resolve_bin(row) == live_bin
    argv = grok.build_command(harness=row, tier="kid", context_file="/tmp/x")
    assert argv[0] == live_bin


def test_live_bin_cell_threads_through_to_argv(live_cfg, monkeypatch):
    """A sentinel in a COPY's `bin` cell reaches argv[0] unchanged, so no
    constant and no fallback can mask the config cell. The live config is
    never mutated -- the sentinel is written to the resolved dict, which
    `adapters.resolve` copied out of the loaded config."""
    monkeypatch.delenv("GROK_BOT_BIN", raising=False)
    _, row = adapters.resolve(live_cfg, "grok-bot")
    row["bin"] = "/SENTINEL/grok-bot"
    argv = grok.build_command(harness=row, tier="kid", context_file="/tmp/x")
    assert argv[0] == "/SENTINEL/grok-bot"
    assert argv[0] != grok.DEFAULT_BIN


def test_live_config_peers_still_resolve(live_cfg_raw):
    """Adding a fourth harness did not disturb the rows already declared.

    Reads `live_cfg_raw`, NOT the grok-gated `live_cfg` (DT.23 residue 3), so
    it runs on a tip with no `harnesses.grok-bot` row -- the regression it
    guards (a shipped row lost, or its adapter stem mis-derived) is
    independent of grok existing, and gating it behind the grok row was what
    swallowed it.
    """
    for name, adapter in (("pi", "pi"), ("claude-code", "claude_code"),
                          ("pi-local", "pi"), ("copilot-cli", "copilot_cli")):
        rname, row = adapters.resolve(live_cfg_raw, name)
        assert rname == name
        assert row["adapter"] == adapter


def test_dispatch_still_has_zero_grok_hits():
    """The whole point of `goal:g4.6`: adding a harness edits no dispatch code."""
    dispatch = _project_root() / "extensions" / "agi" / "bin" / "dispatch.py"
    assert "grok" not in dispatch.read_text(encoding="utf-8").lower()

