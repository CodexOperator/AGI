"""hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env.

Every adapter's `restart()` used to build its child env from a raw
`os.environ` base, while the first spawn and the dry-run mirror already went
through `dispatch.scrubbed_env()` -- so a RESTARTED round inherited what the
scrub list exists to remove (the Claude-Code Anthropic credentials, the
key-minting key, the AGI_ORDERS_* text, AGI_MODEL_SLOT_LOCK).

`subprocess.Popen` is stubbed throughout: no real harness process spawns
(TMM.202). The first test is the falsifier -- a restored key in a
`restart()` call turns it red.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
import dispatch  # noqa: E402
import provisioning  # noqa: E402

ADAPTERS = ("pi", "claude_code", "copilot_cli", "grok_bot")

#: `claude_code_adapter.child_env` deliberately hands `ANTHROPIC_*` /
#: `CLAUDE_CODE_*` back to its own child (RESTORED_PREFIXES) -- the CLI needs
#: them, and it does so on the FIRST spawn too. The rule under test is that
#: restart matches the first spawn, not that claude-code runs keyless.
CLAUDE_CODE_OWNS = tuple(
    k for k in dispatch.ENV_VARS_TO_SCRUB
    if k.startswith("ANTHROPIC_") or k.startswith("CLAUDE_CODE_")
    or k in ("CLAUDECODE", "CLAUDE_AGENT_SDK_VERSION"))

ROW = {"adapter": "pi", "provider": "fake", "credential": "none",
       "max_live": 1, "models": {"kid": "deepseek-v4"}}


def _restart_child_env(monkeypatch, adapter: str, sess_dir: Path, **extra):
    mod = adapters.load(adapter)
    captured: dict[str, str] = {}

    class _StubProc:
        pid = 4242
        def __enter__(self): return self
        def __exit__(self, *exc): return False
        def poll(self): return None
        def wait(self, timeout=None): return 0

    def _patched(argv, **kwargs):
        captured.update(kwargs.get("env") or {})
        return _StubProc()

    sess_dir.mkdir(parents=True, exist_ok=True)
    ctx = sess_dir / "context.md"
    ctx.write_text("fixture context\n")
    monkeypatch.setattr(subprocess, "Popen", _patched)
    mod.restart(harness=dict(ROW), tier="kid", context_file=str(ctx),
                agent_id="a00-restart", iter_n=1, sess_dir=sess_dir, **extra)
    return captured


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_restart_child_lacks_every_scrubbed_key(monkeypatch, tmp_path, adapter):
    """FALSIFIER 1: with each scrub key set in the restarting process, the
    restarted child's env must not carry it."""
    keys = [k for k in dispatch.ENV_VARS_TO_SCRUB
            if k not in CLAUDE_CODE_OWNS] + [provisioning.PROVISIONING_KEY_VAR]
    for key in keys:
        monkeypatch.setenv(key, f"leaked-{key}")
    monkeypatch.setenv("GH_TOKEN", "ghp_fixture")   # keep copilot off `gh`
    monkeypatch.setenv("KEEP_ME", "1")              # a non-scrubbed key stays
    env = _restart_child_env(monkeypatch, adapter, tmp_path / adapter)
    for key in keys:
        assert key not in env, (
            f"{adapter}.restart() handed the scrubbed key {key} to its child")
    assert env.get("KEEP_ME") == "1", "a non-scrubbed key must survive"


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_restart_child_matches_the_first_spawn_for_claude_code_keys(
        monkeypatch, tmp_path, adapter):
    """claude-code restores its own `ANTHROPIC_*` keys from the inherited env
    on BOTH spawn paths; restart must not diverge from the first spawn."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fixture")
    monkeypatch.setenv("GH_TOKEN", "ghp_fixture")   # keep copilot off `gh`
    mod = adapters.load(adapter)
    first = mod.child_env(harness=dict(ROW), base=dispatch.scrubbed_env(),
                          tier="kid")
    rest = _restart_child_env(monkeypatch, adapter, tmp_path / adapter)
    for key in CLAUDE_CODE_OWNS:
        assert (key in first) == (key in rest), (
            f"{adapter}: restart and first spawn disagree on {key}")


def test_no_adapter_carries_a_second_scrub_list():
    """FALSIFIER 2: one scrub list, `dispatch.ENV_VARS_TO_SCRUB`. No adapter
    may read a raw `os.environ` base on its restart path again."""
    for adapter in ADAPTERS:
        src = (BIN / "adapters" / f"{adapter}_adapter.py").read_text()
        assert "base=dict(os.environ)" not in src, (
            f"{adapter}_adapter still builds a restart child from raw "
            f"os.environ")
    assert callable(adapters.scrubbed_base)
    assert adapters.scrubbed_base({"EXPLICIT": "1"}) == {"EXPLICIT": "1"}, (
        "an explicit base from the caller must win over the inherited env")
    monkey = {k: "v" for k in ("ANTHROPIC_API_KEY", "AGI_MODEL_SLOT_LOCK")}
    with pytest.MonkeyPatch.context() as mp:
        for k, v in monkey.items():
            mp.setenv(k, v)
        base = adapters.scrubbed_base()
    assert "ANTHROPIC_API_KEY" not in base and "AGI_MODEL_SLOT_LOCK" not in base, (
        "the default base must be dispatch.scrubbed_env(), nothing else")


def test_scrubbed_base_filters_an_EXPLICIT_raw_environ():
    """FALSIFIER 3: an explicit base is scrubbed, not trusted.

    The parent's auth probe: `restart(base_env=dict(os.environ))` handed
    AGI_MODEL_SLOT_LOCK / ANTHROPIC_API_KEY / AGI_ORDERS_TEXT /
    PROVISIONING_KEY_VAR to the child, because the filter was a caller's
    discipline rather than this function's property. Reverting the filter in
    `scrubbed_base` turns this red.
    """
    dirty = {k: f"leaked-{k}" for k in dispatch.ENV_VARS_TO_SCRUB}
    dirty[provisioning.PROVISIONING_KEY_VAR] = "sk-or-v1-leak"
    dirty["KEEP_ME"] = "1"
    base = adapters.scrubbed_base(dirty)
    for key in dispatch.ENV_VARS_TO_SCRUB:
        assert key not in base, f"explicit base leaked the scrubbed key {key}"
    assert base == {"KEEP_ME": "1"}, (
        "the explicit base keeps ONLY its non-scrubbed names, verbatim")


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_restart_with_a_raw_environ_base_leaks_nothing(monkeypatch, tmp_path, adapter):
    """FALSIFIER 4: end to end, the caller's raw environ is harmless."""
    for key in list(dispatch.ENV_VARS_TO_SCRUB) + [provisioning.PROVISIONING_KEY_VAR]:
        monkeypatch.setenv(key, f"leaked-{key}")
    monkeypatch.setenv("GH_TOKEN", "ghp_fixture")
    raw = dict(os.environ)
    env = _restart_child_env(monkeypatch, adapter, tmp_path / adapter,
                             base_env=raw)
    for key in [k for k in dispatch.ENV_VARS_TO_SCRUB
                if k not in CLAUDE_CODE_OWNS] + [provisioning.PROVISIONING_KEY_VAR]:
        assert key not in env, (
            f"{adapter}.restart(base_env=dict(os.environ)) leaked {key}")
