"""Tests for bin/adapters/ — the one spawn path. `goal:g4.6`.

What these guard, in the order the MVP's falsifiers name them:

1. A harness can be added with a config entry and one file, and nothing in
   `dispatch.py` is keyed on a harness name.
2. The legacy `agent_dispatch` synthesis works — and it is the MAINLINE path,
   not an edge, because this engine's own config took it until 2026-09-01
   (`outcome:a00-c8365a0c-85a6d1` measured that).
3. The moved pi functions behave identically. `test_dispatch.py` covers that
   half through the shims, with its assertions unchanged, which is the point.
4. A tier with no model is a named error, never a silent fallback to the other
   tier's model.
"""
from __future__ import annotations

import importlib.util
import os
import pwd
import re
import sys
import types
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
import harness_template  # noqa: E402


# ------------------------------------------------------------------ loading


def test_load_returns_a_module_with_the_required_interface():
    mod = adapters.load("pi")
    assert mod.NAME == "pi"
    for fn in adapters.REQUIRED:
        assert callable(getattr(mod, fn))


def test_unknown_harness_names_the_directory_not_just_the_module():
    """The common cause is a config entry naming a harness nobody wrote yet,
    and a bare ImportError sends the reader to the config when the fix is a
    new file."""
    with pytest.raises(adapters.AdapterError) as exc:
        adapters.load("nope")
    assert "bin/adapters/nope_adapter.py" in str(exc.value)


def test_an_adapters_own_missing_import_is_not_reported_as_unknown_harness():
    """An adapter that fails because IT imports something missing must not be
    reported as a missing harness — that would send the reader to write a file
    that already exists."""
    src = BIN / "adapters" / "brokenimport_adapter.py"
    src.write_text("import a_module_that_does_not_exist_anywhere\n")
    try:
        with pytest.raises(ModuleNotFoundError):
            adapters.load("brokenimport")
    finally:
        src.unlink()


def test_incomplete_adapter_is_rejected_at_load_not_at_spawn():
    src = BIN / "adapters" / "incomplete_adapter.py"
    src.write_text("NAME = 'incomplete'\ndef build_command(**kw):\n    return []\n")
    try:
        with pytest.raises(adapters.AdapterError) as exc:
            adapters.load("incomplete")
        assert "child_env" in str(exc.value)
    finally:
        src.unlink()


def test_the_second_harness_is_implemented_not_a_stub():
    """Until 2026-09-03 `claude_code_adapter` was a stub that raised
    `NotImplementedError` from every function, so `--harness claude-code`
    resolved to something honest and then refused to spawn. It is the second
    real harness now; its own facts live in `test_claude_code_adapter.py`.
    This guards only the seam: the config name loads a module that does not
    raise where the work used to go."""
    mod = adapters.load("claude_code")
    assert mod.NAME == "claude-code"
    assert mod.is_alive(__import__("os").getpid())
    # Behaviour, not a grep: the stub raised from here.
    assert mod.child_env(harness={}, base={"PATH": "/bin"})["PATH"] == "/bin"
    assert mod.model_args({"models": {"kid": "m"}}, "kid") == ["--model", "m"]


# ------------------------------------------------------------ config resolve


def test_legacy_config_synthesizes_pi_and_is_the_mainline_path():
    cfg = {"agent_dispatch": {"provider": "openrouter",
                              "model": "z-ai/glm-5.3-flash",
                              "thinking": "medium"}}
    name, harness = adapters.resolve(cfg)
    assert name == "pi"
    assert harness["adapter"] == "pi"
    assert harness["synthesized_from"] == "agent_dispatch"
    assert harness["provider"] == "openrouter"


def test_legacy_synthesis_populates_both_tiers_explicitly():
    """A legacy config genuinely has one model for everything. Saying so beats
    leaving `parent` absent for `model_args` to silently fall back on — the one
    thing it refuses to do."""
    cfg = {"agent_dispatch": {"model": "m"}}
    _n, harness = adapters.resolve(cfg)
    assert harness["models"] == {"kid": "m", "parent": "m", "director": "m", "prime_director": "m"}


def test_declared_harnesses_win_and_spawn_harness_selects():
    cfg = {"harnesses": {"pi": {"adapter": "pi", "models": {"kid": "a"}},
                         "claude-code": {"adapter": "claude_code", "models": {"kid": "b"}}},
           "spawn": {"harness": "claude-code"}}
    name, harness = adapters.resolve(cfg)
    assert name == "claude-code"
    assert harness["models"]["kid"] == "b"


def test_several_harnesses_and_no_choice_is_an_error_not_a_guess():
    cfg = {"harnesses": {"a": {"adapter": "pi"}, "b": {"adapter": "pi"}}}
    with pytest.raises(adapters.AdapterError):
        adapters.resolve(cfg)


def test_a_single_declared_harness_needs_no_spawn_block():
    cfg = {"harnesses": {"pi": {"adapter": "pi"}}}
    assert adapters.resolve(cfg)[0] == "pi"


def test_adapter_name_defaults_from_the_harness_name_with_dashes_mapped():
    cfg = {"harnesses": {"claude-code": {"models": {"kid": "x"}}}}
    _n, harness = adapters.resolve(cfg)
    assert harness["adapter"] == "claude_code"


def test_parallelism_prefers_spawn_but_reads_the_legacy_key():
    assert adapters.parallelism({"spawn": {"parallel": 3}}) == 3
    assert adapters.parallelism({"agent_dispatch": {"claude_max_parallel": 2}}) == 2
    assert adapters.parallelism({}) == 1


# ------------------------------------------------------------------ pi tier


def test_tier_selects_the_model():
    pi = adapters.load("pi")
    harness = {"models": {"kid": "cheap", "parent": "strong"}}
    assert pi.model_args(harness, "kid")[-1] == "cheap"
    assert pi.model_args(harness, "parent")[-1] == "strong"


def test_unknown_tier_is_an_error_naming_the_tier_not_a_silent_fallback():
    """Tiering the model is the entire point of having tiers; a fallback would
    let a parent quietly run on the kid's cheap model and look like it worked."""
    pi = adapters.load("pi")
    with pytest.raises(KeyError) as exc:
        pi.model_args({"models": {"kid": "cheap"}}, "parent")
    assert "parent" in str(exc.value)


def test_absent_keys_pass_no_flags_so_pis_own_settings_win():
    assert adapters.load("pi").model_args({}, "kid") == []


def test_pi_bin_env_var_wins_over_config(tmp_path, monkeypatch):
    pi = adapters.load("pi")
    monkeypatch.delenv("PI_BIN", raising=False)
    # Real files: a path-shaped cell that does not exist refuses by name now
    # (hypothesis:harness-bin-absolute-token-free-bins-refused-by-name), so
    # precedence is pinned with paths that can actually be resolved.
    cfg_bin = tmp_path / "config"
    env_bin = tmp_path / "env"
    for f in (cfg_bin, env_bin):
        f.write_text("#!/bin/sh\n")
        f.chmod(0o755)
    assert pi.resolve_bin({"bin": str(cfg_bin)}) == str(cfg_bin)
    monkeypatch.setenv("PI_BIN", str(env_bin))
    assert pi.resolve_bin({"bin": str(cfg_bin)}) == str(env_bin)


def test_child_env_passes_the_scrubbed_base_through():
    pi = adapters.load("pi")
    out = pi.child_env(harness={}, base={"PATH": "/bin"})
    assert out == {"PATH": "/bin"}


def test_child_env_can_inject_harness_specific_values():
    pi = adapters.load("pi")
    out = pi.child_env(harness={"env": {"X": 1}}, base={"PATH": "/bin"})
    assert out["X"] == "1" and out["PATH"] == "/bin"


def test_pi_argv_loads_no_context_files():
    """Pi discovers AGENTS.md/CLAUDE.md itself unless every prior argv element
    is preserved and exactly one --no-context-files token is present."""
    argv = harness_template.render(
        "pi", bin_path="pi", provider="p", model="m", thinking="medium",
        extra_args=["--append-system-prompt", "brief"], prompt="turn")
    assert argv == [
        "pi", "--provider", "p", "--model", "m", "--thinking", "medium",
        "--no-context-files", "-p", "--mode", "json",
        "--append-system-prompt", "brief", "turn",
    ]
    assert argv.count("--no-context-files") == 1


def test_pi_argv_does_not_duplicate_caller_no_context_files():
    argv = harness_template.render(
        "pi", bin_path="pi", provider="p", model="m", thinking="medium",
        extra_args=["--no-context-files", "--append-system-prompt", "brief"],
        prompt="turn")
    assert argv.count("--no-context-files") == 1


def test_pi_argv_no_context_files_stays_before_the_prompt_when_duplicated():
    """A caller-supplied duplicate must not relocate the flag after the
    positional prompt (mur-9-5) — count-only assertions can't catch this."""
    argv = harness_template.render(
        "pi", bin_path="pi", provider="p", model="m", thinking="medium",
        extra_args=["--no-context-files", "--append-system-prompt", "brief"],
        prompt="turn")
    assert argv == [
        "pi", "--provider", "p", "--model", "m", "--thinking", "medium",
        "--no-context-files", "-p", "--mode", "json",
        "--append-system-prompt", "brief", "turn",
    ]


# --------------------------------------------------- the seam itself (F1/F2)


def test_dispatch_is_not_keyed_on_any_harness_name():
    """MVP falsifier 2. `dispatch.py` may name a harness in a comment or in
    the legacy shims' docstrings; it must not branch on one. The live path
    goes through `adapters.load(harness["adapter"])` and nowhere else."""
    src = (BIN / "dispatch.py").read_text()
    code = "\n".join(
        line for line in src.splitlines()
        if not line.lstrip().startswith("#")
    )
    for banned in ('== "pi"', "== 'pi'", '== "claude-code"', "== 'claude-code'",
                   'harness == ', 'if pi_', 'elif pi_'):
        assert banned not in code, f"dispatch.py branches on a harness: {banned}"


def test_adding_a_harness_touches_only_config_and_one_file():
    """MVP falsifier 1, as far as a test can carry it: a brand-new adapter
    file is loadable and spawnable with no edit anywhere else."""
    src = BIN / "adapters" / "thirdparty_adapter.py"
    src.write_text(
        "NAME = 'thirdparty'\n"
        "def build_command(**kw):\n"
        "    return ['third', kw['tier'], kw['agent_id']]\n"
        "def child_env(*, harness, base):\n"
        "    return base\n"
        "def is_alive(pid):\n"
        "    return True\n"
        "def restart(**kw):\n"
        "    return None\n"
        "def needs_credential(harness):\n"
        "    return True\n"
    )
    try:
        cfg = {"harnesses": {"thirdparty": {"adapter": "thirdparty",
                                            "models": {"kid": "m"}}}}
        name, harness = adapters.resolve(cfg)
        mod = adapters.load(harness["adapter"])
        cmd = mod.build_command(harness=harness, tier="kid", context_file="c",
                                agent_id="a00", iter_n=1, sess_dir=Path("/tmp"))
        assert name == "thirdparty"
        assert cmd == ["third", "kid", "a00"]
    finally:
        src.unlink()


# ------------------------------------------- model/provider namespace guard

def test_claude_alias_on_openrouter_is_refused():
    """hypothesis:l3-workflow-model-crosses-harness-namespace. A Claude Code
    subscription alias resolved onto an OpenRouter provider bills Anthropic
    against an OpenRouter key -- the failure that reads as a mysterious bill
    rather than a wrong flag. It must refuse, and name both names."""
    with pytest.raises(adapters.AdapterError) as exc:
        adapters.assert_model_in_provider_namespace(
            "claude-sonnet-5", "openrouter")
    msg = str(exc.value)
    assert "claude-sonnet-5" in msg and "openrouter" in msg


@pytest.mark.parametrize("model", [
    "~z-ai/glm-flash-latest",
    "z-ai/glm-flash-latest",
    "~deepseek/deepseek-v4-flash-latest",
])
def test_openrouter_slugs_pass(model):
    """A slug is `provider/name`, optionally `~`-prefixed. Both spellings are
    in live use in this repo's own config and must not be refused."""
    adapters.assert_model_in_provider_namespace(model, "openrouter")


@pytest.mark.parametrize("provider", ["", "claude-code", "anthropic"])
def test_non_openrouter_providers_keep_their_aliases(provider):
    """The guard is one-directional on purpose: `sonnet` is CORRECT on the
    claude-code harness, whose namespace is subscription aliases. Refusing it
    there would break the drafting workflow, which names sonnet deliberately."""
    adapters.assert_model_in_provider_namespace("claude-sonnet-5", provider)


# -------------------------------------------------- one-write ladder resolver
# hypothesis:l4-a-model-change-is-one-write — the ladder `roles:` row is the
# ONE source of a (role, tier)'s model/effort/settings, and the allowlist is
# DERIVED from those rows. These test the shared resolver at the adapters
# layer (where dispatch.py, workflow.py and heal.py all import it from).

ROWS = [
    {"tier": 0, "role": "kid", "harness": "pi",
     "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""},
    {"tier": 1, "role": "parent", "harness": "pi",
     "model": "deepseek/deepseek-v4.1-flash", "effort": "", "settings": ""},
    {"tier": 3, "role": "parent", "harness": "claude-code",
     "model": "claude-opus-5", "effort": "max", "settings": "ultracode"},
]


def test_ladder_role_row_finds_by_tier_and_role():
    row = adapters.ladder_role_row(ROWS, 1, "parent")
    assert row is not None and row["model"] == "deepseek/deepseek-v4.1-flash"
    assert adapters.ladder_role_row(ROWS, 0, "parent") is None
    assert adapters.ladder_role_row(ROWS, "1", "parent")["model"] == \
        "deepseek/deepseek-v4.1-flash"  # string tiers coerce


def test_ladder_role_row_none_for_missing_roles():
    assert adapters.ladder_role_row(ROWS, 0, "nobody") is None
    assert adapters.ladder_role_row(None, 0, "kid") is None
    assert adapters.ladder_role_row([], 0, "kid") is None


def test_spec_from_ladder_row_maps_blank_cells_to_none():
    spec = adapters.spec_from_ladder_row(
        {"tier": 1, "role": "parent", "harness": "pi",
         "model": "  ~z-ai/glm-flash-latest  ", "effort": "",
         "thinking": "high", "settings": ""})
    assert spec["model"] == "~z-ai/glm-flash-latest"
    assert spec["effort"] is None
    assert spec["thinking"] == "high"
    assert spec["settings"] is None
    assert spec["harness"] == "pi"


def test_derived_allowed_models_is_ladder_rows_plus_extra():
    harness = {"allowed_extra": ["~z-ai/glm-flash-latest"]}
    allowed = adapters.derived_allowed_models(ROWS, "pi", harness)
    assert allowed == {"~deepseek/deepseek-v4-flash-latest",
                       "deepseek/deepseek-v4.1-flash",
                       "~z-ai/glm-flash-latest"}
    # claude-code rows are separate: only its own rows join
    cc = adapters.derived_allowed_models(ROWS, "claude-code", {})
    assert cc == {"claude-opus-5"}


def test_derived_allowed_models_still_unions_legacy_allowed_models():
    harness = {"allowed_extra": [],
               "allowed_models": ["claude-sonnet-5", "claude-fable-5-1"]}
    allowed = adapters.derived_allowed_models(ROWS, "claude-code", harness)
    # ladder row (claude-opus-5) ∪ legacy census — migration-safe
    assert "claude-opus-5" in allowed
    assert "claude-sonnet-5" in allowed


def test_derived_allowed_models_empty_when_nothing_names_a_model():
    assert adapters.derived_allowed_models(ROWS, "nobody", {}) == set()
    assert adapters.derived_allowed_models([], "pi",
                                           {"allowed_extra": []}) == set()


# ------------------------------------- credential allowlist (needs_credential)
# hypothesis:l4-needs-credential-is-provider-gated — the predicate is an
# ALLOWLIST read from the harness row, not a provider check. A row that
# explicitly carries `credential: "none"` gets no minted key; every other
# row, known or unknown, keeps the pre-existing default of minting.

def test_pi_local_harness_row_with_credential_none_needs_no_credential():
    """The pi adapter is shared by `pi` and `pi-local`; only the row
    distinguishes them. `pi-local` speaks to a $0 local model and must
    not mint an OpenRouter key it never uses."""
    pi = adapters.load("pi")
    row = {"adapter": "pi", "provider": "local-town", "credential": "none",
           "models": {"kid": "Qwen3.5-9B-Q4_K_M"}}
    assert pi.needs_credential(row) is False


def test_needs_credential_defaults_true_for_unmarked_and_unknown_rows():
    """The default mint direction is unchanged from before the fix: rows
    without the key — including the placeholder providers test fixtures
    use and providers nobody has written yet — still mint."""
    pi = adapters.load("pi")
    for row in (
        {"adapter": "pi", "provider": "openrouter"},
        {"adapter": "pi", "provider": "fake"},          # scaffold-test fixture
        {"adapter": "pi", "provider": "some-future-provider"},
        {"adapter": "pi"},                              # no provider at all
        {"adapter": "pi", "credential": "openrouter"},  # any other value
    ):
        assert pi.needs_credential(row) is True, row


# ------------------------------------- ONE bin resolver (goal:g15 config-max)
# hypothesis:harness-bin-paths-resolve-per-box. Env override, then the config
# `bin` cell, then PATH -- with `~`/`{home}` expanded against the CURRENT
# process HOME at resolve time and a named refusal when an override resolves
# nowhere. The four adapters must DELEGATE, not keep four copies.

def test_all_four_adapters_delegate_to_the_one_shared_resolver(monkeypatch):
    seen = []

    def fake(harness, env_var, default):
        seen.append((env_var, default))
        return "/resolved"

    monkeypatch.setattr(adapters, "resolve_bin", fake)
    for name in ("pi", "copilot_cli", "claude_code", "grok_bot"):
        assert adapters.load(name).resolve_bin({"bin": "/x"}) == "/resolved"
    assert [env for env, _ in seen] == [
        "PI_BIN", "COPILOT_BIN", "CLAUDE_BIN", "GROK_BOT_BIN"]


def test_tilde_expands_against_the_current_process_home(tmp_path, monkeypatch):
    """A config cell of `~/.npm-global/bin/pi` resolves to the binary under
    THIS box's HOME -- never a stored `/home/<user>` literal."""
    monkeypatch.setenv("HOME", str(tmp_path))
    fake = tmp_path / ".npm-global" / "bin" / "pi"
    fake.parent.mkdir(parents=True)
    fake.write_text("#!/bin/sh\n")
    fake.chmod(0o755)
    monkeypatch.delenv("PI_BIN", raising=False)
    got = adapters.resolve_bin(
        {"adapter": "pi", "bin": "~/.npm-global/bin/pi"}, "PI_BIN", "pi")
    assert got == str(fake)


def test_home_token_expands_the_same_way(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    fake = tmp_path / ".npm-global" / "bin" / "pi"
    fake.parent.mkdir(parents=True)
    fake.write_text("#!/bin/sh\n")
    fake.chmod(0o755)
    monkeypatch.delenv("PI_BIN", raising=False)
    got = adapters.resolve_bin(
        {"bin": "{home}/.npm-global/bin/pi"}, "PI_BIN", "pi")
    assert got == str(fake)


def test_tilde_user_expands_to_that_users_home_not_the_current_home(
        tmp_path, monkeypatch):
    """`~user/x` means THAT user's home (os.path.expanduser semantics), never
    the current HOME with `user/` spliced onto it. Pre-fix `home + raw[1:]`
    turned `~bob/.npm-global/bin/pi` into `<current home>bob/.npm-global/bin/pi`
    (goal:g15.29.2)."""
    monkeypatch.setenv("HOME", str(tmp_path / "me"))
    user_home = tmp_path / "bob-home"
    fake = user_home / ".npm-global" / "bin" / "pi"
    fake.parent.mkdir(parents=True)
    fake.write_text("#!/bin/sh\n")
    fake.chmod(0o755)
    monkeypatch.setattr(pwd, "getpwnam",
                        lambda name: types.SimpleNamespace(pw_dir=str(user_home)))
    monkeypatch.delenv("PI_BIN", raising=False)
    assert os.path.expanduser("~bob/.npm-global/bin/pi") == str(fake)
    got = adapters.resolve_bin(
        {"adapter": "pi", "bin": "~bob/.npm-global/bin/pi"}, "PI_BIN", "pi")
    assert got == str(fake)
    assert got != str(tmp_path / "me" / "bob/.npm-global/bin/pi")


def test_env_override_wins_over_the_config_cell(tmp_path, monkeypatch):
    cfg_bin = tmp_path / "config"
    env_bin = tmp_path / "env"
    for f in (cfg_bin, env_bin):
        f.write_text("#!/bin/sh\n")
        f.chmod(0o755)
    monkeypatch.setenv("PI_BIN", str(env_bin))
    assert adapters.resolve_bin(
        {"bin": str(cfg_bin)}, "PI_BIN", "pi") == str(env_bin)


def test_path_fallback_resolves_a_bare_name(tmp_path, monkeypatch):
    fake = tmp_path / "pi"
    fake.write_text("#!/bin/sh\n")
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.delenv("PI_BIN", raising=False)
    assert adapters.resolve_bin({"adapter": "pi"}, "PI_BIN", "pi") == "pi"


def test_a_missing_override_refuses_by_name(monkeypatch):
    """Never a bare `Popen` FileNotFoundError: the refusal says which harness
    and which name could not be resolved."""
    monkeypatch.delenv("PI_BIN", raising=False)
    with pytest.raises(FileNotFoundError) as exc:
        adapters.resolve_bin(
            {"adapter": "pi", "bin": "pi-not-installed-xyz"}, "PI_BIN", "pi")
    assert "pi-not-installed-xyz" in str(exc.value)


def test_a_missing_path_shaped_bin_refuses_by_name_with_the_expanded_path(
        tmp_path, monkeypatch):
    """Round 2 (`experiment:a00-73aeae86-75e0f3`): a `~`-cell whose expanded
    file does not exist must raise the SAME named refusal a missing bare name
    does. Before this fix the RAW cell was returned, so a caller got
    `'~/.npm-global/bin/nope'` and `Popen` died on a bare
    `FileNotFoundError('~/...')` that named nothing (the parent's gate probe).

    The message owes three names: the harness, the EXPANDED path tried, and
    the `$ENV_VAR` that would override it."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("ZEPHYR_BIN", raising=False)
    expanded = tmp_path / ".npm-global" / "bin" / "zephyr-nope"
    with pytest.raises(FileNotFoundError) as exc:
        adapters.resolve_bin(
            {"adapter": "zephyr", "bin": "~/.npm-global/bin/zephyr-nope"},
            "ZEPHYR_BIN", "zephyr")
    msg = str(exc.value)
    assert "'zephyr'" in msg, msg
    assert str(expanded) in msg, msg
    assert "ZEPHYR_BIN" in msg, msg


def test_no_home_user_literal_survives_in_any_adapter():
    """The falsifier as a test: no quoted `/home/<user>` path literal in the
    four adapter files (their defaults are bare PATH names now)."""
    offenders = []
    for path in sorted((BIN / "adapters").glob("*_adapter.py")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r'["\']/home/', line):
                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert offenders == []


def test_an_unresolvable_tilde_user_refuses_by_name(tmp_path, monkeypatch):
    """`~nosuchuser/bin/x` cannot expand: `os.path.expanduser` hands the raw
    token back unchanged, so the pre-fix `path == raw` branch returned the raw
    cell and `Popen` died on a bare `FileNotFoundError('~nosuchuser/...')`
    that named nothing. It now refuses BY NAME, naming the harness, the raw
    cell and the `$ENV_VAR` that would override it."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("NOPE_BIN", raising=False)
    with pytest.raises(FileNotFoundError) as exc:
        adapters.resolve_bin(
            {"adapter": "nope", "bin": "~nosuchuser_xyz/bin/nope"},
            "NOPE_BIN", "nope")
    msg = str(exc.value)
    assert "nosuchuser_xyz" in msg, msg
    assert "'nope'" in msg, msg
    assert "NOPE_BIN" in msg, msg


def test_a_missing_token_free_absolute_bin_refuses_by_name(monkeypatch):
    """`hypothesis:harness-bin-absolute-token-free-bins-refused-by-name`.

    The last carry-unchanged hole in `resolve_bin`: a CONFIGURED path-shaped
    cell that is already absolute and holds NO `~`/`{home}` token was returned
    verbatim when the file was absent, so `Popen` died on a bare
    `FileNotFoundError('/x/nope')` naming neither the harness nor the
    `$ENV_VAR` that would fix it -- the same unnamed death the home-token
    case was closed for. Precedence does not require carrying a value that
    cannot be exec'd: a bare NAME is still carried (the synthetic-template
    contract); a PATH is not.

    The message owes the same three names as its siblings: the harness, the
    path it tried, and the `$ENV_VAR` that would override it."""
    monkeypatch.delenv("ZEPHYR_BIN", raising=False)
    with pytest.raises(FileNotFoundError) as exc:
        adapters.resolve_bin(
            {"adapter": "zephyr", "bin": "/opt/zephyr/bin/zephyr-nope"},
            "ZEPHYR_BIN", "zephyr")
    msg = str(exc.value)
    assert "'zephyr'" in msg, msg
    assert "/opt/zephyr/bin/zephyr-nope" in msg, msg
    assert "ZEPHYR_BIN" in msg, msg


def test_an_EXISTING_absolute_bin_is_still_returned(tmp_path, monkeypatch):
    """The negative probe: the new refusal must not fire on a file that is
    there, or every live box with an absolute `bin` cell would fail closed."""
    fake = tmp_path / "zephyr"
    fake.write_text("#!/bin/sh\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.delenv("ZEPHYR_BIN", raising=False)
    assert adapters.resolve_bin(
        {"adapter": "zephyr", "bin": str(fake)}, "ZEPHYR_BIN", "zephyr") == str(fake)
