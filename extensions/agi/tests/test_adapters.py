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
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402


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
    assert harness["models"] == {"kid": "m", "parent": "m"}


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


def test_pi_bin_env_var_wins_over_config(monkeypatch):
    pi = adapters.load("pi")
    assert pi.resolve_bin({"bin": "/from/config"}) == "/from/config"
    monkeypatch.setenv("PI_BIN", "/from/env")
    assert pi.resolve_bin({"bin": "/from/config"}) == "/from/env"


def test_child_env_passes_the_scrubbed_base_through():
    pi = adapters.load("pi")
    out = pi.child_env(harness={}, base={"PATH": "/bin"})
    assert out == {"PATH": "/bin"}


def test_child_env_can_inject_harness_specific_values():
    pi = adapters.load("pi")
    out = pi.child_env(harness={"env": {"X": 1}}, base={"PATH": "/bin"})
    assert out["X"] == "1" and out["PATH"] == "/bin"


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
