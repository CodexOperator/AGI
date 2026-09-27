"""Tests for bin/adapters/copilot_cli_adapter.py. `goal:g4.6`, third harness.

Guard the facts the adapter was built on, each read from the installed
`copilot` v1.0.83 rather than assumed:

1. There is NO system-prompt flag, so the assembled brief becomes a leading
   instruction block in the single `-p` turn (the fallback the parent claim
   allowed) -- and every brief segment must still be present, not just the
   first.
2. `--allow-all` is what makes `-p` non-interactive; without it a spawn
   off a TTY blocks on the first tool prompt.
3. `--model` carries the config row's value verbatim (`auto` here), and a
   tier with no model is a named error, never another tier's model.
4. `child_env` must inject a GitHub token (nothing persists on disk -- no
   keychain), and must never need an OpenRouter credential.

Nothing here calls a live `copilot`: the argv is built against a fixture
session and, where a binary is needed, a fake shell script on PATH.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

cp = adapters.load("copilot_cli")

#: The `bin` cell is a BARE PATH NAME, not a literal absolute path: a
#: configured path-shaped cell that does not exist now refuses by name
#: (`hypothesis:harness-bin-absolute-token-free-bins-refused-by-name`), and
#: these tests are about argv SHAPE, not about bin resolution. A bare name is
#: still carried unchanged, so every `argv[0] == HARNESS["bin"]` assert below
#: means the same thing it meant against the old `/home/ubuntu/...` literal.
HARNESS = {"adapter": "copilot_cli",
           "bin": "copilot",
           "models": {"kid": "auto", "parent": "auto"}}

SCAFFOLD = {"path": "/x/nodes/hypothesis/h.md", "node_type": "hypothesis",
            "node_id": "hypothesis:h", "parent": "goal:g4.6"}


@pytest.fixture
def rig(tmp_path):
    """A `.agi/` project with one session directory, a zoom context and a
    skill prompt -- the three files `build_command` reads or writes."""
    repo = tmp_path / "repo"
    root = repo / ".agi"
    sess = root / "sessions" / "iter-001" / "a00-test"
    sess.mkdir(parents=True)
    ctx = sess / "context.md"
    ctx.write_text("# ZOOM CONTEXT MARKER\nsome map\n")
    skill = tmp_path / "agent-prompt.md"
    skill.write_text("SKILL PROMPT MARKER\n")
    return {"repo": repo, "root": root, "sess": sess, "ctx": ctx, "skill": skill}


@pytest.fixture
def fake_copilot(tmp_path):
    """A fake `copilot` binary on PATH: records its argv, calls no model."""
    bindir = tmp_path / "fakebin"
    bindir.mkdir()
    fake = bindir / "copilot"
    fake.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$0.args\"\n")
    fake.chmod(0o755)
    return fake


def build(rig, tier="kid", harness=HARNESS, **kw):
    kw.setdefault("scaffold", SCAFFOLD if tier == "kid" else None)
    kw.setdefault("skill_prompt", rig["skill"])
    kw.setdefault("cli_py", "/x/cli.py")
    kw.setdefault("dispatch_py", "/x/dispatch.py")
    kw.setdefault("target", "goal:g4.6")
    return cp.build_command(
        harness=harness, tier=tier, context_file=str(rig["ctx"]),
        agent_id="a00-test", iter_n=1, sess_dir=rig["sess"], **kw)


def value(args, flag):
    return args[args.index(flag) + 1] if flag in args else None


# ---------------------------------------------------------------- interface


def test_adapter_implements_the_whole_interface_not_a_stub():
    assert cp.NAME == "copilot-cli"
    for fn in adapters.REQUIRED:
        assert callable(getattr(cp, fn))
    assert cp.is_alive(os.getpid())


def test_config_entry_resolves_to_this_adapter():
    cfg = {"harnesses": {"copilot-cli": HARNESS, "pi": {"adapter": "pi"}},
           "spawn": {"harness": "pi"}}
    name, harness = adapters.resolve(cfg, "copilot-cli")
    assert name == "copilot-cli"
    assert adapters.load(harness["adapter"]) is cp


def test_the_live_config_declares_the_third_harness_and_it_loads():
    """A test of live config reads the live node, never a copied list: the
    row shipped in `.agi/config.json` must resolve through the same
    `adapters.resolve` the dispatcher uses."""
    cfg = json.loads((ROOT / ".agi" / "config.json").read_text())
    name, harness = adapters.resolve(cfg, "copilot-cli")
    assert name == "copilot-cli"
    assert adapters.load(harness["adapter"]) is cp
    assert set(harness.get("models") or {}) >= {"kid", "parent"}


def test_needs_no_openrouter_credential():
    """Copilot authenticates through a GitHub token, so dispatch must not
    mint a per-spawn OpenRouter key for it (the same rule Claude Code's
    subscription auth earned)."""
    assert cp.needs_credential(HARNESS) is False


# ---------------------------------------------------------------- the argv


def test_headless_uses_p_and_allow_all_tools(rig):
    args = build(rig)
    assert args[0] == HARNESS["bin"]
    assert "-p" in args
    assert "--allow-all" in args
    assert args[args.index("--allow-all") + 1] == "--remote"
    # the prompt is the argument to -p, and it is the LAST element
    assert args[args.index("-p") + 1] == args[-1]


def test_model_follows_the_tier_and_auto_is_a_real_value(rig):
    kid = build(rig, "kid")
    parent = build(rig, "parent")
    assert value(kid, "--model") == "auto"
    assert value(parent, "--model") == "auto"


def test_missing_tier_is_a_named_error_not_a_fallback(rig):
    with pytest.raises(KeyError) as exc:
        build(rig, "parent", harness={"models": {"kid": "only"}})
    assert "parent" in str(exc.value)


def test_no_models_block_passes_no_model_flag(rig):
    args = build(rig, harness={})
    assert "--model" not in args


def test_every_brief_segment_lands_in_the_one_prompt(rig):
    """Copilot has no system-prompt flag, so the whole brief must be the `-p`
    text: zoom context, every tier-brief segment, the skill prompt, and the
    closing turn, in the order the other two adapters use."""
    args = build(rig)
    prompt = value(args, "-p")
    assert "ZOOM CONTEXT MARKER" in prompt
    assert "SKILL PROMPT MARKER" in prompt
    assert "fill in the scaffolded node file" in prompt
    assert "DO NOT run git" in prompt
    assert "RUN THE REPO TEST SUITE" in prompt
    assert SCAFFOLD["path"] in prompt and "--node-id hypothesis:h" in prompt
    # And in pi/claude order: context before brief before skill before closing.
    assert prompt.index("ZOOM CONTEXT MARKER") < prompt.index("fill in the scaffolded") \
        < prompt.index("SKILL PROMPT MARKER") \
        < prompt.index("Begin iteration 1 as agent a00-test")


def test_parent_tier_gets_the_parent_brief(rig):
    args = build(rig, "parent")
    prompt = value(args, "-p")
    assert "--tier kid" in prompt and "fill in the scaffolded" not in prompt
    assert "Begin iteration 1 as parent agent" in prompt


def test_prompt_is_materialized_as_a_session_artefact(rig):
    build(rig)
    written = (rig["sess"] / cp.PROMPT_FILE).read_text()
    assert "ZOOM CONTEXT MARKER" in written


def test_brief_tier_swaps_the_brief_without_changing_the_model_tier(rig):
    """An advisor is a parent that carries another tier's brief: the model
    still resolves from `tier`, only the assembled brief changes."""
    harness = dict(HARNESS, models={"kid": "auto", "parent": "auto"})
    args = build(rig, "parent", harness=harness, brief_tier="advisor",
                 target="vision:alive", scaffold=None)
    assert value(args, "--model") == "auto"
    prompt = value(args, "-p")
    assert "THE VISION YOU EMBODY" in prompt
    assert "ADVISOR" in prompt


def test_missing_context_is_an_error_not_a_quiet_omission(rig):
    with pytest.raises(FileNotFoundError):
        cp.build_command(harness=HARNESS, tier="kid",
                         context_file=str(rig["sess"] / "nope.md"),
                         agent_id="a", iter_n=1, sess_dir=rig["sess"])
    with pytest.raises(FileNotFoundError):
        cp.build_command(harness=HARNESS, tier="kid", context_file="",
                         agent_id="a", iter_n=1, sess_dir=rig["sess"])


def test_extra_args_precede_the_prompt(rig):
    args = build(rig, harness=dict(HARNESS, extra_args=["--no-remote-export"]))
    assert "--no-remote-export" in args
    assert args.index("--no-remote-export") < args.index("-p")
    assert args[-1] == value(args, "-p")


# ---------------------------------------------------------------- the binary


def test_fake_copilot_on_path_is_the_built_argv_head(monkeypatch, rig,
                                                     fake_copilot):
    """The brief calls for a FAKE binary, never a live copilot call: put one
    on PATH, resolve through it, and assert the argv it would receive."""
    monkeypatch.setenv("PATH", f"{fake_copilot.parent}:{os.environ.get('PATH', '')}")
    assert shutil.which("copilot") == str(fake_copilot)
    monkeypatch.setenv("COPILOT_BIN", str(fake_copilot))
    args = build(rig, harness={"models": {"kid": "auto"}})
    assert args[0] == str(fake_copilot)
    # The argv is a valid process invocation: run the fake, read back argv.
    proc = subprocess.run(args, capture_output=True, text=True, timeout=20)
    assert proc.returncode == 0
    recorded = Path(str(fake_copilot) + ".args").read_text()
    assert "--allow-all" in recorded
    assert "--model" in recorded and "auto" in recorded


def test_resolve_bin_precedence(tmp_path, monkeypatch):
    # Real files: a path-shaped cell that does not exist REFUSES by name now
    # (hypothesis:harness-bin-absolute-token-free-bins-refused-by-name), so a
    # precedence test can no longer use `/env/copilot` as a stand-in value.
    env_bin = tmp_path / "env" / "copilot"
    cfg_bin = tmp_path / "cfg" / "copilot"
    for f in (env_bin, cfg_bin):
        f.parent.mkdir(parents=True)
        f.write_text("#!/bin/sh\n")
        f.chmod(0o755)
    monkeypatch.setenv("COPILOT_BIN", str(env_bin))
    assert cp.resolve_bin({"bin": str(cfg_bin)}) == str(env_bin)
    monkeypatch.delenv("COPILOT_BIN")
    assert cp.resolve_bin({"bin": str(cfg_bin)}) == str(cfg_bin)
    assert cp.resolve_bin({}) == cp.DEFAULT_BIN


# ---------------------------------------------------------------- the env


def test_child_env_passes_an_inherited_token_through(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "gho_inherited")
    env = cp.child_env(harness=HARNESS, base={"GH_TOKEN": "gho_inherited"})
    assert env["GH_TOKEN"] == "gho_inherited"


def test_child_env_resolves_a_token_from_gh_when_none_is_set(monkeypatch,
                                                              tmp_path):
    """Nothing persists on disk (no keychain), so with no token in the env
    `child_env` must shell out to `gh auth token` and inject the result."""
    for name in cp.TOKEN_VARS:
        monkeypatch.delenv(name, raising=False)
    bindir = tmp_path / "ghbin"
    bindir.mkdir()
    gh = bindir / "gh"
    gh.write_text("#!/bin/sh\necho gho_from_gh\n")
    gh.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bindir}:{os.environ.get('PATH', '')}")
    env = cp.child_env(harness=HARNESS, base={})
    assert env.get("GH_TOKEN") == "gho_from_gh"


def test_child_env_harness_env_wins_over_the_resolved_token(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "gho_inherited")
    env = cp.child_env(harness=dict(HARNESS, env={"GH_TOKEN": "gho_explicit"}),
                       base={"GH_TOKEN": "gho_inherited"})
    assert env["GH_TOKEN"] == "gho_explicit"


def test_child_env_does_not_invent_a_token_it_cannot_get(monkeypatch, tmp_path):
    """A host with no token and no `gh` must not have one fabricated; the
    spawn fails in the CLI, not silently here."""
    for name in cp.TOKEN_VARS:
        monkeypatch.delenv(name, raising=False)
    empty = tmp_path / "emptybin"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))
    env = cp.child_env(harness=HARNESS, base={})
    assert "GH_TOKEN" not in env


# ---------------------------------------------------------------- restart


def test_restart_rebuilds_argv_and_stamps_the_record(monkeypatch, rig, tmp_path):
    """`restart` is the same contract as the other two adapters: rebuild the
    identical argv and Popen it in the same session dir, stamping the record.
    Exercised with Popen faked -- no process is started."""
    captured = {}

    class FakeProc:
        pid = 4242

    def fake_popen(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeProc()

    monkeypatch.setattr(cp.subprocess, "Popen", fake_popen)
    monkeypatch.setenv("GH_TOKEN", "gho_test")
    rec = {"worktree": str(rig["repo"])}
    pid = cp.restart(harness=HARNESS, tier="kid", context_file=str(rig["ctx"]),
                     agent_id="a00-test", iter_n=1, sess_dir=rig["sess"],
                     scaffold=SCAFFOLD, target="goal:g4.6",
                     agent_record=rec)
    assert pid == 4242
    assert captured["args"][0] == HARNESS["bin"]
    i = captured["args"].index("-p")
    assert captured["args"][i + 1].startswith("# ZOOM CONTEXT MARKER")
    assert captured["kwargs"]["cwd"] == str(rig["repo"])
    assert captured["kwargs"]["env"]["GH_TOKEN"] == "gho_test"
    assert rec["pid"] == 4242 and rec["status"] == "restarted"
