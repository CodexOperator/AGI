"""Tests for bin/adapters/claude_code_adapter.py. `goal:g4.6`, second harness.

Each test below guards a fact about the `claude` CLI that was measured with a
one-turn probe on 2026-09-03 rather than assumed, and that a naive port of the
pi spelling would get wrong:

1. `--append-system-prompt` repeated is LAST-WINS. pi's one-flag-per-segment
   spelling would silently discard every brief segment but the last.
2. Variadic flags (`--tools`, `--allowedTools`, `--add-dir`, ...) swallow a
   trailing positional prompt; the closing line must be fenced behind `--`.
3. `child_env` must hand back what `dispatch.scrubbed_env` took, because for
   this harness the subscription is the sanctioned path -- and must still
   never hand down the key that mints keys (`goal:g1.11`).
4. The harness enforces the two bounds the brief only requests: a closed tool
   list with no `Agent`, and git write verbs refused.
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
import provisioning  # noqa: E402

cc = adapters.load("claude_code")

HARNESS = {"adapter": "claude_code",
           "models": {"kid": "claude-sonnet-5", "parent": "claude-opus-5"}}

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


def build(rig, tier="kid", harness=HARNESS, **kw):
    kw.setdefault("scaffold", SCAFFOLD if tier == "kid" else None)
    kw.setdefault("skill_prompt", rig["skill"])
    kw.setdefault("cli_py", "/x/cli.py")
    kw.setdefault("dispatch_py", "/x/dispatch.py")
    kw.setdefault("target", "goal:g4.6")
    return cc.build_command(
        harness=harness, tier=tier, context_file=str(rig["ctx"]),
        agent_id="a00-test", iter_n=1, sess_dir=rig["sess"], **kw)


def value(args, flag):
    return args[args.index(flag) + 1] if flag in args else None


def variadic_values(args, flag):
    """Everything after `flag` up to the next `--`-prefixed token."""
    out, i = [], args.index(flag) + 1
    while i < len(args) and not args[i].startswith("--"):
        out.append(args[i])
        i += 1
    return out


# ---------------------------------------------------------------- interface


def test_adapter_implements_the_whole_interface_not_a_stub():
    """The stub raised NotImplementedError from every function. The interface
    check in `adapters.load` only proves the names exist; this proves they
    run."""
    assert cc.NAME == "claude-code"
    for fn in adapters.REQUIRED:
        assert callable(getattr(cc, fn))
    assert cc.is_alive(os.getpid())


def test_config_entry_resolves_to_this_adapter():
    cfg = {"harnesses": {"claude-code": HARNESS, "pi": {"adapter": "pi"}},
           "spawn": {"harness": "pi"}}
    name, harness = adapters.resolve(cfg, "claude-code")
    assert name == "claude-code"
    assert adapters.load(harness["adapter"]) is cc


# ---------------------------------------------------------------- the argv


def test_headless_and_the_model_follows_the_tier(rig):
    kid = build(rig, "kid")
    parent = build(rig, "parent")
    assert kid[0] == "claude" and kid[1] == "-p"
    assert value(kid, "--model") == "claude-sonnet-5"
    assert value(parent, "--model") == "claude-opus-5"


def test_missing_tier_is_a_named_error_not_a_fallback(rig):
    with pytest.raises(KeyError) as exc:
        build(rig, "parent", harness={"models": {"kid": "only"}})
    assert "parent" in str(exc.value)


def test_no_models_block_passes_no_model_flag(rig):
    args = build(rig, harness={})
    assert "--model" not in args


def test_every_brief_segment_lands_in_one_system_prompt_file(rig):
    """Measured 2026-09-03: `--append-system-prompt A --append-system-prompt B`
    answered as if only B had been given. So the adapter may not spell the
    brief the way pi does. Everything the agent is told -- zoom context, every
    brief segment, the skill prompt -- goes into ONE file passed ONCE."""
    args = build(rig)
    assert "--append-system-prompt" not in args, "last-wins: segments would be lost"
    assert args.count("--append-system-prompt-file") == 1
    prompt_file = Path(value(args, "--append-system-prompt-file"))
    assert prompt_file == rig["sess"] / cc.SYSTEM_PROMPT_FILE
    text = prompt_file.read_text()
    assert "ZOOM CONTEXT MARKER" in text
    assert "SKILL PROMPT MARKER" in text
    # Every kid brief segment, not just the last one.
    assert "fill in the scaffolded node file" in text
    assert "DO NOT run git" in text
    assert "RUN THE REPO TEST SUITE" in text
    assert SCAFFOLD["path"] in text and "--node-id hypothesis:h" in text
    # And in pi's order: context before brief before skill prompt.
    assert text.index("ZOOM CONTEXT MARKER") < text.index("fill in the scaffolded") \
        < text.index("SKILL PROMPT MARKER")


def test_parent_tier_gets_the_parent_brief_on_the_parent_model(rig):
    """`goal:g4.8`'s falsifier: tiering is verified by inspecting the spawned
    command, never assumed."""
    args = build(rig, "parent")
    text = Path(value(args, "--append-system-prompt-file")).read_text()
    assert "--tier kid" in text and "fill in the scaffolded" not in text
    assert value(args, "--model") == "claude-opus-5"
    assert args[-1].startswith("Begin iteration 1 as parent agent")


def test_closing_line_is_fenced_behind_a_double_dash(rig):
    """Measured 2026-09-03: a prompt placed after `--tools ...` was read as
    another tool name and `claude -p` exited with 'Input must be provided'.
    Every variadic flag must precede `--`; the prompt must be the last arg."""
    args = build(rig)
    fence = args.index("--")
    assert args[-2] == "--"
    assert args[-1].startswith("Begin iteration 1 as agent a00-test")
    for flag in ("--tools", "--allowedTools", "--disallowedTools", "--add-dir"):
        assert flag in args and args.index(flag) < fence, flag


def test_missing_context_is_an_error_not_a_quiet_omission(rig):
    with pytest.raises(FileNotFoundError):
        cc.build_command(harness=HARNESS, tier="kid",
                         context_file=str(rig["sess"] / "nope.md"),
                         agent_id="a", iter_n=1, sess_dir=rig["sess"])
    with pytest.raises(FileNotFoundError):
        cc.build_command(harness=HARNESS, tier="kid", context_file="",
                         agent_id="a", iter_n=1, sess_dir=rig["sess"])


def test_output_streams_so_a_killed_agent_leaves_a_log(rig):
    args = build(rig)
    assert value(args, "--output-format") == "stream-json"
    assert "--verbose" in args
    with pytest.raises(ValueError):
        build(rig, harness=dict(HARNESS, output_format="yaml"))
    plain = build(rig, harness=dict(HARNESS, output_format="json"))
    assert value(plain, "--output-format") == "json" and "--verbose" not in plain


def test_add_dir_is_the_repo_root_so_edits_outside_dot_agi_are_allowed(rig):
    """The child runs with cwd = the graph root (`.agi/`), where Claude Code
    permits edits without asking. The engine source lives one level up."""
    args = build(rig)
    assert Path(value(args, "--add-dir")) == rig["repo"]


def test_mcp_servers_are_off_unless_the_harness_names_them(rig):
    args = build(rig)
    assert "--strict-mcp-config" in args and "--mcp-config" not in args
    args = build(rig, harness=dict(HARNESS, mcp_config="/x/mcp.json"))
    assert value(args, "--mcp-config") == "/x/mcp.json"


def test_tools_are_a_closed_list_with_no_agent_and_git_writes_are_refused(rig):
    args = build(rig)
    tools = variadic_values(args, "--tools")
    assert "Bash" in tools and "Edit" in tools
    assert "Agent" not in tools and "Task" not in tools
    assert variadic_values(args, "--allowedTools") == tools
    denied = variadic_values(args, "--disallowedTools")
    for verb in ("commit", "add", "push", "stash", "checkout"):
        assert f"Bash(git {verb}:*)" in denied, verb


def test_tool_lists_come_from_config_when_declared(rig):
    harness = dict(HARNESS, tools=["Read", "Grep"],
                   disallowed_tools="Bash(rm:*), Bash(git push:*)")
    args = build(rig, harness=harness)
    assert variadic_values(args, "--tools") == ["Read", "Grep"]
    assert variadic_values(args, "--allowedTools") == ["Read", "Grep"]
    # Comma-split only: a rule with a space of its own stays one item.
    assert variadic_values(args, "--disallowedTools") == ["Bash(rm:*)", "Bash(git push:*)"]


def test_optional_knobs_are_omitted_unless_set(rig):
    args = build(rig)
    for flag in ("--effort", "--max-budget-usd"):
        assert flag not in args
    args = build(rig, harness=dict(HARNESS, effort="high", max_budget_usd=2.5,
                                   extra_args=["--no-session-persistence"]))
    assert value(args, "--effort") == "high"
    assert value(args, "--max-budget-usd") == "2.5"
    assert "--no-session-persistence" in args


def test_bin_env_var_wins_over_config(monkeypatch):
    assert cc.resolve_bin({"bin": "/from/config"}) == "/from/config"
    monkeypatch.setenv("CLAUDE_BIN", "/from/env")
    assert cc.resolve_bin({"bin": "/from/config"}) == "/from/env"


# ---------------------------------------------------------------- the env


SCRUBBED = {"PATH": "/bin", "HOME": "/h", "OPENROUTER_API_KEY": "rt-key"}
INHERITED = {**SCRUBBED,
             "ANTHROPIC_BASE_URL": "https://host-proxy",
             "ANTHROPIC_API_KEY": "sk-sub",
             "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "0",
             "CLAUDECODE": "1",
             "CLAUDE_AGENT_SDK_VERSION": "0.3",
             "UNRELATED_SECRET": "no",
             provisioning.PROVISIONING_KEY_VAR: "mints-keys"}


def test_child_env_hands_back_what_the_shared_scrub_took():
    """The pi scrub exists so a pi child cannot bill the subscription. For a
    Claude Code child that billing IS the sanctioned path."""
    env = cc.child_env(harness={}, base=dict(SCRUBBED), inherited=INHERITED)
    assert env["ANTHROPIC_BASE_URL"] == "https://host-proxy"
    assert env["ANTHROPIC_API_KEY"] == "sk-sub"
    assert env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] == "0"
    assert env["CLAUDECODE"] == "1"
    assert env["CLAUDE_AGENT_SDK_VERSION"] == "0.3"
    assert env["PATH"] == "/bin" and env["OPENROUTER_API_KEY"] == "rt-key"
    # Restoration is by namespace, not "everything the parent had".
    assert "UNRELATED_SECRET" not in env


def test_child_env_never_hands_down_the_key_that_mints_keys():
    """`goal:g1.11`. From the base (a restart passes the raw environment),
    from the inherited environment, and from `harness.env` -- all three."""
    key = provisioning.PROVISIONING_KEY_VAR
    env = cc.child_env(harness={"env": {key: "via-config"}},
                       base={**SCRUBBED, key: "via-base"}, inherited=INHERITED)
    assert key not in env


def test_child_env_base_wins_over_inherited_and_harness_env_wins_over_both():
    env = cc.child_env(harness={"env": {"ANTHROPIC_MODEL": "cfg", "X": 1}},
                       base={"ANTHROPIC_BASE_URL": "from-base"},
                       inherited={"ANTHROPIC_BASE_URL": "from-parent",
                                  "ANTHROPIC_MODEL": "from-parent"})
    assert env["ANTHROPIC_BASE_URL"] == "from-base"
    assert env["ANTHROPIC_MODEL"] == "cfg"
    assert env["X"] == "1"


def test_child_env_defaults_to_the_real_environment(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://real")
    env = cc.child_env(harness={}, base={"PATH": "/bin"})
    assert env["ANTHROPIC_BASE_URL"] == "https://real"


# ---------------------------------------------------------------- liveness


def test_is_alive_distinguishes_a_reaped_pid():
    proc = subprocess.Popen(["true"])
    proc.wait()
    assert cc.is_alive(os.getpid())
    assert not cc.is_alive(proc.pid)


def test_restart_rebuilds_the_command_and_spawns_from_the_root(rig, monkeypatch):
    seen = {}

    class _Proc:
        pid = 4242

    def fake_popen(args, **kw):
        seen["args"] = args
        seen["kw"] = kw
        return _Proc()

    monkeypatch.setattr(cc.subprocess, "Popen", fake_popen)
    monkeypatch.setenv(provisioning.PROVISIONING_KEY_VAR, "mints-keys")
    record = {"id": "a00-test", "status": "running", "pid": 1}
    pid = cc.restart(harness=HARNESS, tier="kid", context_file=str(rig["ctx"]),
                     agent_id="a00-test", iter_n=1, sess_dir=rig["sess"],
                     scaffold=SCAFFOLD, agent_record=record)
    assert pid == 4242
    assert seen["args"][:2] == ["claude", "-p"]
    assert value(seen["args"], "--model") == "claude-sonnet-5"
    assert Path(seen["kw"]["cwd"]) == rig["root"]
    assert seen["kw"]["start_new_session"] is True
    assert provisioning.PROVISIONING_KEY_VAR not in seen["kw"]["env"]
    assert record["pid"] == 4242 and record["status"] == "restarted"
    assert (rig["sess"] / "agent.json").exists()
