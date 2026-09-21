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

#: Verbatim `grok-bot --help` from the published package, recorded by the
#: child experiment of `goal:g7.31.1.1`:
#:   mkdir measure && cd measure && npm init -y
#:   npm install grok-bot-cli@0.3.1
#:   node_modules/.bin/grok-bot --help
#: 46 lines, exit 0. This is the RECORDED measurement the adapter argv is
#: bound to; `latest` (0.9.0) and 0.8.0 print nothing (bundled TUI), so 0.3.1
#: is the last version publishing static help. Do not hand-edit this block:
#: re-run the command and paste.
RECORDED_HELP_0_3_1 = """\
gbot - manage Grok Bot agents and groups

Usage:
  gbot [--dir DIR] [--json] <command>

Commands:
  doctor
  bots list
  bots create --name NAME [--description TEXT] [--instructions TEXT] [--title TEXT]
           [--avatar-shape SHAPE] [--avatar-color COLOR]
  bots update <id-or-name> [--name NAME] [--description TEXT] [--instructions TEXT]
           [--title TEXT] [--avatar-shape SHAPE] [--avatar-color COLOR]
           [--notify on|off] [--hidden on|off]
  bots get <id-or-name>
  bots delete <id-or-name>
  groups list
  groups create --name NAME --member ID_OR_NAME [--member ...]
           [--description TEXT] [--instructions TEXT] [--title TEXT]
           [--avatar-shape SHAPE] [--avatar-color COLOR]
  groups update <id-or-name>  (same flags as bots update; members stay on set/add/remove)
  groups get <id-or-name>
  groups members <id-or-name>
  groups add <group> <bot>
  groups remove <group> <bot>
  groups set <group> --member ID [--member ...]
  groups delete <id-or-name>
  send <bot-or-group> <message...>
  thread <bot-or-group> [--limit N] [--root MESSAGE_ID] [--full]
  chat <bot-or-group>     alias for thread
  history [bot-or-group] [--search TEXT] [--limit N]  (offline)
  history --path         print the local JSONL file path
  codex status
  codex list-threads [--limit N]
  codex send <threadId> <message...>

Max group members: 6
--description / --instructions is the UI Instructions field (same key).
Avatar shapes: blob pebble bean egg squircle tablet capsule cylinder hex gem crystal wedge shield dome arch cloud teardrop leaf
Avatar colors: black brown red orange yellow green cyan blue violet magenta gray
Flags: --gateway  --files  --dir DIR  --json
Auth: GROK_BOT_GATEWAY_URL + GROK_BOT_GATEWAY_TOKEN, or the Grok Bot app session, or CURSOR_ACCESS_TOKEN
File fallback: GROK_BOT_AGENTS_DIR
Codex: talks to the local app-server daemon socket under CODEX_HOME (default ~/.codex)
History: opt-in plaintext JSONL at ~/.grok-bot-cli/history.jsonl
         GROK_BOT_HISTORY=on to record; --history-dir / GROK_BOT_HISTORY_DIR to relocate
         --no-history to skip one command
"""

#: Env names `grok-bot-cli@0.3.1`'s SOURCE actually reads, measured VERBATIM in
#: the DT.29 experiment and RE-MEASURED in DT.32. The measurement is a UNION
#: of three commands over `node_modules/grok-bot-cli/src` (scratch
#: `measure-0.3.1/`); none alone is complete:
#:   npm install grok-bot-cli@0.3.1 --no-audit --no-fund
#:   grep -rn 'AGI_MODEL' src                              # no matches, exit 1
#:   (a) grep -rhoE 'process\.env\.[A-Za-z_][A-Za-z0-9_]*' src | sort -u
#:       -> 20 LITERAL dot-access names
#:   (b) grep -rhoE 'truthyEnv\("([A-Za-z_][A-Za-z0-9_]*)"\)' src | sort -u
#:       -> 2 names read through the COMPUTED accessor
#:          (GROK_BOT_ALLOW_ANY_GATEWAY, GROK_BOT_ALLOW_LOCAL_GATEWAY)
#:   (c) grep -rn 'process\.env\[' src
#:       -> exactly ONE dynamic site, url-policy.js:13, the generic helper
#:          `process.env[name]` whose only callers pass the two literals in (b);
#:          no other computed access exists whose name is uncounted
#: UNION = 20 + 2 = 22 names.
#: A narrow (a)-only scan MISSES (b) because `process.env[name]` is invisible
#: to a dot-access grep. (`process.env.S` seen under the narrower `[A-Z_]+`
#: class is the truncation of `process.env.SystemRoot` -- named, not dropped.)
RECORDED_CLI_SOURCE_ENV_0_3_1 = frozenset({
    "CURSOR_ACCESS_TOKEN", "CURSOR_API_BASE_URL",
    "GROK_BOT_ACCESS_TOKEN", "GROK_BOT_AGENTS_DIR",
    "GROK_BOT_ALLOW_ANY_GATEWAY", "GROK_BOT_ALLOW_LOCAL_GATEWAY",
    "GROK_BOT_GATEWAY_HEADERS", "GROK_BOT_GATEWAY_TOKEN",
    "GROK_BOT_GATEWAY_URL", "GROK_BOT_HISTORY", "GROK_BOT_HISTORY_DIR",
    "SAND_ACCESS_TOKEN", "SAND_AGENTS_DIR", "SAND_BACKEND_URL",
    "SAND_BOX_NAMESPACE", "SAND_CLIENT_VERSION", "SAND_DATA_ROOT",
    "SAND_GATEWAY_TOKEN", "SAND_HOST_GATEWAY_TOKEN",
    "SAND_HOST_GATEWAY_URL", "SAND_HOST_PORT", "SystemRoot",
})

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


def test_configured_tier_reaches_the_spawn_env_not_argv():
    """DT.27 R3 close: the configured tier is NOT discarded on this path.

    The measured help has no `--model`, so the row's model for the requested
    tier must reach the process as `AGI_MODEL`; and because the row owns the
    resolved model (dispatch lands ladder/seat overrides in that cell), it
    WINS over a stale inherited value -- a restart invoked from an environment
    carrying another tier must not silently keep the wrong model.
    """
    env = grok.child_env(harness=HARNESS, base={}, tier="kid")
    assert env["AGI_MODEL"] == "grok-kid"
    env = grok.child_env(harness=HARNESS, base={}, tier="parent")
    assert env["AGI_MODEL"] == "grok-parent"
    env = grok.child_env(harness=HARNESS, base={"AGI_MODEL": "stale-model"},
                         tier="parent")
    assert env["AGI_MODEL"] == "grok-parent"
    # No tier / no models cell -> nothing invented.
    assert "AGI_MODEL" not in grok.child_env(harness=HARNESS, base={})
    assert "AGI_MODEL" not in grok.child_env(
        harness={"adapter": "grok_bot"}, base={}, tier="kid")


def test_recorded_help_names_no_model_selector_so_residual_is_the_cli():
    """DT.27 R3 measured re-scope: where the remaining gap lives.

    The recorded 0.3.1 `--help` documents no `--model` flag and no
    model-selecting env var; its only env names are auth/agents/history/codex.
    The adapter therefore carries the tier in `AGI_MODEL`, and whether
    `grok-bot-cli` CONSUMES that name is the CLI's app/profile field -- the
    residual named here, not silently dropped.
    """
    assert "--model" not in RECORDED_HELP_0_3_1
    assert "AGI_MODEL" not in RECORDED_HELP_0_3_1
    for name in ("GROK_BOT_GATEWAY_URL", "GROK_BOT_GATEWAY_TOKEN",
                 "CURSOR_ACCESS_TOKEN", "GROK_BOT_AGENTS_DIR", "CODEX_HOME",
                 "GROK_BOT_HISTORY", "GROK_BOT_HISTORY_DIR"):
        assert name in RECORDED_HELP_0_3_1, name


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


#: Tokens the recorded help documents as subcommands / flags. Used by the
#: binding predicate below; kept OUT of argv -- the adapter emits none of them.
DOCUMENTED_FLAGS = ("--gateway", "--files", "--dir", "--json")


def _documented_tokens() -> set[str]:
    """The help's whitespace tokens, stripped of `[]()|,:` syntax punctuation.

    Token-aware, not substring: `-p` is a SUBSTRING of the documented `--path`,
    so a substring test would accept the retired guess. `[--json]` must reduce
    to `--json` to be findable.
    """
    strip = "[]()|,:"
    return {tok.strip(strip) for tok in RECORDED_HELP_0_3_1.split()}


def _unbound_tokens(argv: list[str]) -> list[str]:
    """argv tokens the recorded `--help` does NOT document.

    argv[0] is the bin and is exempt; every other `-`-prefixed token must be
    findable in the recorded help. DT.27 R2: the old loop this replaces was
    VACUOUS -- `build_command` returns a one-element list, so the loop body
    never ran and the binding asserted nothing. Extracting it into a predicate
    makes it callable on a real multi-token argv, so there is now at least one
    token (`--model`, `-p`) whose presence it REJECTS.
    """
    documented = _documented_tokens()
    return [tok for tok in argv[1:]
            if tok.startswith("-") and tok not in documented]


def test_agi_model_is_not_read_by_the_0_3_1_cli_source():
    """DT.29 D2: the CLI's SOURCE, not just its `--help`, re-scopes the stamp.

    `grep -rn AGI_MODEL node_modules/grok-bot-cli/src` exits 1 (no matches) on
    the published 0.3.1 source, and the env set the CLI reads is exactly
    `RECORDED_CLI_SOURCE_ENV_0_3_1` (22 names, measured as the UNION of literal
    dot-accesses, `truthyEnv(...)` string args, and a check that the one
    computed `process.env[name]` site has no uncounted callers -- commands in
    the constant's docstring). So on THIS
    CLI the adapter's `AGI_MODEL` stamping is **compat/no-delivery**: the
    configured tier does NOT reach grok-bot through the environment, and
    model selection stays the app/profile field. The stamp is kept -- a later
    CLI that adds the name would receive it -- but nothing here claims
    delivery, and "absent from the recorded help" is NOT called closed.

    The one `model` token in that source is `model: resumed.model`
    (`codex-bridge.js:489`), a passthrough of a Codex daemon response field,
    NOT a selector -- named so it is not mistaken for one.
    """
    assert "AGI_MODEL" not in RECORDED_CLI_SOURCE_ENV_0_3_1
    assert not any("MODEL" in name.upper()
                   for name in RECORDED_CLI_SOURCE_ENV_0_3_1), (
        "the CLI reads a model-selecting env name; re-measure and re-scope")
    # The stamp really is carried -- and it really is not in what the CLI
    # reads. The two facts together are the re-scope, not a closure.
    env = grok.child_env(harness=HARNESS, base={}, tier="kid")
    assert env["AGI_MODEL"] == "grok-kid"


def test_the_binding_predicate_is_falsifiable():
    """Negative control for the binding (DT.27 R2): the predicate rejects the
    retired stub flags and accepts documented ones, so it can fail."""
    bin0 = grok.resolve_bin(HARNESS)
    assert _unbound_tokens([bin0, "--model", "grok-kid"]) == ["--model"]
    assert _unbound_tokens([bin0, "-p", "/tmp/ctx.md"]) == ["-p"]
    assert _unbound_tokens([bin0, "--json", "--dir", "/x"]) == []
    # The help really is where the rejection comes from: the guess is absent
    # from the recorded bytes, which is why there is something to reject.
    assert "--model" not in _documented_tokens()
    assert "-p" not in _documented_tokens()


def test_argv_is_bound_to_the_recorded_help():
    """The measurement-bound guard (goal:g7.31.1.1, DT.27 R2).

    argv[0] is the resolved bin and every other flag token it emits is
    documented in the RECORDED `--help`. The predicate is exercised on a real
    multi-token argv in `test_the_binding_predicate_is_falsifiable`, so this
    is not the vacuous one-element loop it replaces.
    """
    argv = grok.build_command(harness=HARNESS, tier="kid",
                              context_file="/tmp/ctx.md")
    assert argv[0] == grok.resolve_bin(HARNESS)
    assert _unbound_tokens(argv) == [], (
        f"undocumented argv tokens: {_unbound_tokens(argv)}")
    assert "-p" not in argv
    assert "--model" not in argv
    # 0.3.1 is the last version with static help; named so drift is visible.
    for cmd in ("send", "thread", "history", *DOCUMENTED_FLAGS):
        assert cmd in RECORDED_HELP_0_3_1


def test_no_model_flag_survives_into_argv():
    """`--model` is a Grok Bot app/profile field, not a CLI flag; a declared
    models block must not leak one into the measured argv (goal:g7.31.1.1)."""
    argv = grok.build_command(harness=RESTART_HARNESS, tier="parent",
                              context_file="/tmp/ctx.md")
    assert argv == [grok.resolve_bin(RESTART_HARNESS)]


def test_restart_is_a_real_respawn_not_a_stub():
    """The old stub raised NotImplementedError; the contract is now the same
    as copilot_cli/pi (`goal:g4.7`): callable, returns a pid."""
    assert callable(grok.restart)


#: A synthetic argv that is DEFINITELY not the bare bin: restart must pass
#: through whatever `build_command` produced, never a constant of its own.
SENTINEL_ARGV = ["/sentinel/bin", "--dir", "/sentinel"]


def test_restart_passes_through_the_built_argv(monkeypatch, tmp_path):
    """DT.27 R1: the old test pinned `args == [RESTART_HARNESS['bin']]`, i.e. it
    certified the measured no-op argv as the CORRECT restart. Restart's actual
    contract is compositional -- Popen receives exactly `build_command`'s
    output -- so this injects a sentinel argv and asserts it arrives unchanged.
    A restart that hardcoded its own argv fails here.
    """
    seen = {}

    def fake_build(**kwargs):
        seen["build_kwargs"] = kwargs
        return list(SENTINEL_ARGV)

    monkeypatch.setattr(grok, "build_command", fake_build)
    spawned = {}

    class FakeProc:
        pid = 4848

    def fake_popen(args, **kwargs):
        spawned["args"] = args
        spawned["kwargs"] = kwargs
        return FakeProc()

    monkeypatch.setattr(grok.subprocess, "Popen", fake_popen)
    sess = tmp_path / "sess"
    sess.mkdir()
    pid = grok.restart(harness=RESTART_HARNESS, tier="kid",
                       context_file=str(tmp_path / "context.md"),
                       agent_id="a00-test", iter_n=1, sess_dir=sess,
                       agent_record={"worktree": str(tmp_path)})
    assert pid == 4848
    assert spawned["args"] == SENTINEL_ARGV
    assert spawned["args"] != [RESTART_HARNESS["bin"]]
    assert seen["build_kwargs"]["tier"] == "kid"


def test_restart_spawns_a_live_process_and_is_killable(monkeypatch, tmp_path):
    """DT.27 R1 liveness half: this guard CAN go red.

    With an argv that really runs (`sleep`), restart must yield a pid that
    `is_alive` reports alive -- so a restart whose argv is a measured no-op
    (bare `grok-bot` prints help and exits) cannot be certified live. The
    process is killed and reaped, never left behind.
    """
    import signal
    import time as _time

    argv = [sys.executable, "-c", "import time; time.sleep(30)"]
    monkeypatch.setattr(grok, "build_command", lambda **kw: list(argv))
    sess = tmp_path / "sess"
    sess.mkdir()
    pid = grok.restart(harness=RESTART_HARNESS, tier="kid",
                       context_file=str(tmp_path / "context.md"),
                       agent_id="a00-test", iter_n=1, sess_dir=sess,
                       agent_record={"worktree": str(tmp_path)})
    assert pid is not None
    try:
        for _ in range(50):
            if grok.is_alive(pid):
                break
            _time.sleep(0.02)
        assert grok.is_alive(pid) is True, (
            "restart produced no live process; the respawn argv is a no-op")
        # A process that exits immediately is still alive for one scheduling
        # slice; requiring it to SURVIVE the window is what makes this guard
        # red on a no-op argv (measured: `-c pass` reads alive at t=0 and dead
        # at t=0.25, so the t=0 check alone was a race, not a guard).
        _time.sleep(0.25)
        assert grok.is_alive(pid) is True, (
            "restart respawn exited immediately -- a no-op argv was spawned")
    finally:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        try:
            os.waitpid(pid, 0)
        except (ChildProcessError, OSError):
            pass


def test_liveness_guard_goes_red_on_a_noop_argv(monkeypatch, tmp_path):
    """DT.29 D1 negative control: the liveness guard CAN read DEAD.

    The committed suite exercised the guard only on an argv that is ALIVE
    (`test_restart_spawns_a_live_process_and_is_killable`); the red half lived
    in an uncommitted scratch probe. An argv whose real process exits
    immediately -- the SHAPE of the measured real respawn, which prints help
    and exits 0 -- is driven through `restart` and must read DEAD after the
    0.25 s window. A guard that can only return True cannot pass this test.

    The published 0.3.1 binary is not installed on this box, so the argv is a
    self-owned immediate-exit program; the SHAPE (exit before the window) is
    what is measured. Real-binary measurement, from the DT.29 scratch dir,
    the bare resolved bin with NO subcommand (the exact respawn argv):
        is_alive t=0: True   is_alive t=0.25: False   exit 0
    The process is SIGKILLed (harmless if already gone) and `waitpid`-reaped
    in `finally`, so no child is left behind.
    """
    import signal
    import time as _time

    argv = [sys.executable, "-c", "raise SystemExit(0)"]
    monkeypatch.setattr(grok, "build_command", lambda **kw: list(argv))
    sess = tmp_path / "sess"
    sess.mkdir()
    pid = grok.restart(harness=RESTART_HARNESS, tier="kid",
                       context_file=str(tmp_path / "context.md"),
                       agent_id="a00-test", iter_n=1, sess_dir=sess,
                       agent_record={"worktree": str(tmp_path)})
    assert pid is not None
    try:
        _time.sleep(0.25)
        assert grok.is_alive(pid) is False, (
            "the liveness guard read an already-exited process as ALIVE -- "
            "it cannot go red, so its green certifies nothing")
    finally:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        try:
            os.waitpid(pid, 0)
        except (ChildProcessError, OSError):
            pass


def test_bare_bin_respawn_is_a_recorded_noop_residue():
    """The honest half of R1: `restart`'s real argv IS a measured no-op.

    `grok-bot` with no subcommand prints help and exits (recorded 0.3.1
    `--help`), so the respawn does not hold a seat. That liveness work is
    `goal:g7.31.1.2` and is NOT implemented here. This pins the RESIDUE, not a
    liveness claim -- and it goes red the day a subcommand lands in the
    respawn argv, so the gap cannot be silently forgotten.
    """
    argv = grok.build_command(harness=RESTART_HARNESS, tier="kid",
                              context_file="/tmp/ctx.md")
    subcommands = ("doctor", "bots", "groups", "send", "thread", "chat",
                   "history", "codex")
    assert not any(tok in subcommands for tok in argv[1:]), (
        "a subcommand now rides the respawn argv; if that is the "
        "goal:g7.31.1.2 fix, replace this residue test with a live-seat "
        "assert and delete it")
    assert argv == [grok.resolve_bin(RESTART_HARNESS)]


def test_restart_returns_the_new_pid_and_stamps_the_record(monkeypatch, tmp_path):
    """Popen faked so no real `grok-bot` binary is needed. Spawns detached,
    enters the record's worktree, stamps pid/status/restarted_at."""
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
    # No argv pin here (DT.27 R1): composition is asserted by
    # test_restart_passes_through_the_built_argv against an injected sentinel.
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


def test_live_tier_cell_reaches_the_spawn_env(live_cfg, monkeypatch):
    """The live `models` cell, not a fixture row, is what the spawn env carries.

    Reads the real `.agi/config.json` (read-only) so a config that lost the
    grok-bot models block -- or shipped one tier -- is caught here.
    """
    monkeypatch.delenv("AGI_MODEL", raising=False)
    _, row = adapters.resolve(live_cfg, "grok-bot")
    for tier, model in (row.get("models") or {}).items():
        assert grok.child_env(harness=row, base={}, tier=tier)["AGI_MODEL"] == model
    assert grok.build_command(harness=row, tier="kid",
                              context_file="/tmp/x") == [grok.resolve_bin(row)]


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

