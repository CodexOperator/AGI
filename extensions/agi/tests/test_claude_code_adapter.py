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


def test_no_settings_flag_when_absent(rig):
    """A row with no settings emits no --settings flag at all."""
    args = build(rig, "kid")
    assert "--settings" not in args


def test_settings_ultracode_appends_settings_flag(rig):
    """hypothesis:l3w0-ladder-roles-table — a row whose settings is the
    string 'ultracode' must append `--settings` carrying {"ultracode": true}."""
    import json
    harness = dict(HARNESS, settings="ultracode")
    args = build(rig, "kid", harness=harness)
    i = args.index("--settings")
    assert json.loads(args[i + 1]) == {"ultracode": True}


def test_settings_per_tier_map(rig):
    """Settings may be a per-tier map (ultracode on directors, none on kids)."""
    import json
    harness = dict(HARNESS, models=dict(HARNESS["models"], director="claude-fable-5-1"),
                   settings={"director": "ultracode"})
    args = build(rig, "kid", harness=harness)
    assert "--settings" not in args  # kid tier not in the map
    args_d = build(rig, "director", harness=harness)
    assert json.loads(args_d[args_d.index("--settings") + 1]) == {"ultracode": True}


def test_effort_and_settings_combine(rig):
    """A row carries both effort (as today) and settings; both reach the CLI."""
    harness = dict(HARNESS, effort={"kid": "max"}, settings="ultracode")
    args = build(rig, "kid", harness=harness)
    assert args[args.index("--effort") + 1] == "max"
    assert "--settings" in args


def test_ultracode_tier_sets_env_var(rig):
    """hypothesis:l3-rotate-ultracode-env -- the env var gates ultracode for
    a spawned advisor: a tier whose settings resolve to ultracode must have
    CLAUDE_CODE_WORKFLOWS set in its child environment."""
    env = cc.child_env(harness=dict(HARNESS, settings="ultracode"),
                       base={}, inherited={}, tier="kid")
    assert env.get("CLAUDE_CODE_WORKFLOWS") == "1"


def test_non_ultracode_tier_no_env_var(rig):
    """An ultracode setting names no tier (or no ultracode at all) injects
    no env var."""
    env = cc.child_env(harness=HARNESS, base={}, inherited={}, tier="kid")
    assert "CLAUDE_CODE_WORKFLOWS" not in env
    # per-tier map: ultracode on directors, not kids
    env2 = cc.child_env(
        harness=dict(HARNESS, settings={"director": "ultracode"}),
        base={}, inherited={}, tier="kid")
    assert "CLAUDE_CODE_WORKFLOWS" not in env2
    env3 = cc.child_env(
        harness=dict(HARNESS, settings={"director": "ultracode"}),
        base={}, inherited={}, tier="director")
    assert env3.get("CLAUDE_CODE_WORKFLOWS") == "1"


def test_ultracode_tier_keyword_opens_user_turn(rig):
    """hypothesis:l3-rotate-ultracode-env -- an ultracode tier's `claude -p`
    user turn (the closing line fenced behind `--`) opens with the keyword
    `ultracode`."""
    harness = dict(HARNESS, settings="ultracode")
    args = build(rig, "kid", harness=harness)
    i = args.index("--")
    assert args[i + 1].startswith("ultracode")
    assert "Begin iteration" in args[i + 1]


def test_non_ultracode_tier_no_keyword(rig):
    """A plain tier's closing line is untouched."""
    args = build(rig, "kid")
    i = args.index("--")
    assert not args[i + 1].startswith("ultracode")


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


# hypothesis:l3w3-advisor-brief — a parent-tier spawn can carry the advisor brief
# ------------------------------------------------------------


def test_adapter_threads_brief_tier_while_keeping_the_model_tier(rig):
    """The advisor is a tier-3 parent: its MODEL comes from the parent row
    (claude-opus-5, effort max) but its BRIEF is the advisor brief (the
    vision body, the tier3-quorum seat, the perpetual-director spawn
    primitive). The adapter must let dispatch route a vision-targeted tier-3
    parent spawn to `assemble(tier='advisor')` without changing the tier
    that selects the model."""
    harness = dict(HARNESS, effort={"parent": "max"}, settings="ultracode")
    args = build(rig, "parent", harness=harness,
                 brief_tier="advisor", target="vision:alive",
                 scaffold=None)
    # model/effort still the parent row's
    assert value(args, "--model") == "claude-opus-5"
    assert value(args, "--effort") == "max"
    # the brief is the advisor's, not the generic parent's
    prompt = (rig["sess"] / "system-prompt.md").read_text()
    assert "THE VISION YOU EMBODY" in prompt
    assert "tier3-quorum" in prompt
    assert "perpetual" in prompt.lower()
    # and it closes like an advisor
    i = args.index("--")
    assert "ADVISOR" in args[i + 1]


def test_adapter_brief_tier_defaults_to_the_spawn_tier(rig):
    """Without brief_tier the adapter keeps today's behaviour exactly: a
    plain parent spawn gets the generic parent brief. The new routing must
    be opt-in, never the default."""
    args = build(rig, "parent", target="vision:alive", scaffold=None)
    prompt = (rig["sess"] / "system-prompt.md").read_text()
    assert "THE VISION YOU EMBODY" not in prompt
    assert "tier3-quorum" not in prompt
    # and it still closes like a plain parent (no brief_tier given)
    i = args.index("--")
    assert "spawn and review kids" in args[i + 1]


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
    for verb in ("commit", "add", "push", "stash", "checkout", "reset", "rm"):
        assert f"Bash(git {verb}:*)" in denied, verb
    # goal:s34 item 10: HANDOFF.md writes, CLAUDE.md writes, dispatch.py runs
    assert "Bash(*HANDOFF.md:*)" in denied, "HANDOFF.md writes must be disallowed"
    assert "Bash(*CLAUDE.md:*)" in denied, "CLAUDE.md writes must be disallowed"
    assert "Bash(*dispatch.py:*)" in denied, "dispatch.py runs must be disallowed"


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


# ----------------------------------------- hypothesis:l3-cc-tools-by-tier ---
# Tools resolve per (role, ladder tier): kids keep the full closed default
# list; advisors (parent@tier3) and directors (director@tier1) add the
# ultracode/loop tools and drop the dispatch.py refusal; git verbs, HANDOFF.md
# and CLAUDE.md stay refused for every role below the prime.


def test_kid_with_role_keeps_the_full_default_block_list(rig):
    args = build(rig, "kid", role="kid", ladder_tier=4)
    tools = variadic_values(args, "--tools")
    denied = variadic_values(args, "--disallowedTools")
    for t in ("Workflow", "Agent", "ToolSearch", "Monitor", "TaskOutput", "TaskStop"):
        assert t not in tools, t
    assert "Bash(*dispatch.py:*)" in denied
    for rule in ("Bash(git commit:*)", "Bash(*HANDOFF.md:*)", "Bash(*CLAUDE.md:*)"):
        assert rule in denied, rule


def _advisor_tools(rig):
    """Resolve the variadic blocks for a tier-3 advisor (parent role)."""
    args = build(rig, "parent", role="parent", ladder_tier=3,
                 brief_tier="advisor", target="vision:alive", scaffold=None)
    return {
        "tools": variadic_values(args, "--tools"),
        "allowed": variadic_values(args, "--allowedTools"),
        "denied": variadic_values(args, "--disallowedTools"),
    }


def test_advisor_parent_at_tier3_adds_ultracode_tools(rig):
    blk = _advisor_tools(rig)
    for t in ("Workflow", "Agent", "ToolSearch", "Monitor", "TaskOutput", "TaskStop"):
        assert t in blk["tools"], t
        assert t in blk["allowed"], t  # auto-approved, since -p cannot prompt


def test_advisor_parent_at_tier3_drops_dispatch_rule_but_keeps_others(rig):
    blk = _advisor_tools(rig)
    assert "Bash(*dispatch.py:*)" not in blk["denied"]
    # rotate.py / send.py / season.py never blocked by the defaults anyway
    assert not any("rotate.py" in r or "send.py" in r or "season.py" in r
                   for r in blk["denied"])
    # git verbs and the handoff files stay refused below the prime
    for rule in ("Bash(git commit:*)", "Bash(git add:*)",
                 "Bash(*HANDOFF.md:*)", "Bash(*CLAUDE.md:*)"):
        assert rule in blk["denied"], rule


def test_director_at_tier1_gets_the_same_tools_as_advisor(rig):
    harness = dict(HARNESS, models=dict(HARNESS["models"],
                                        director="claude-fable-5-1"))
    args = build(rig, "director", harness=harness, role="director",
                 ladder_tier=1, scaffold=None, target="vision:alive")
    tools = variadic_values(args, "--tools")
    denied = variadic_values(args, "--disallowedTools")
    for t in ("Workflow", "Agent", "ToolSearch", "Monitor", "TaskOutput", "TaskStop"):
        assert t in tools, t
    assert "Bash(*dispatch.py:*)" not in denied
    assert "Bash(git push:*)" in denied


def test_privileged_only_for_the_exact_role_and_tier(rig):
    # a parent but not at tier 3 stays on the closed list
    args = build(rig, "parent", role="parent", ladder_tier=2,
                 scaffold=None, target="vision:alive")
    assert "Workflow" not in variadic_values(args, "--tools")
    assert "Bash(*dispatch.py:*)" in variadic_values(args, "--disallowedTools")


def test_no_role_given_keeps_todays_behaviour(rig):
    """Privacy is opt-in: a call that passes no role/ladder_tier resolves to
    the old flat defaults, so the legacy shim and any out-of-tree callers are
    unchanged."""
    args = build(rig, "parent", scaffold=None, target="vision:alive")
    assert "Workflow" not in variadic_values(args, "--tools")
    assert "Bash(*dispatch.py:*)" in variadic_values(args, "--disallowedTools")


def test_per_role_config_override_wins_over_flat_and_default(rig):
    harness = dict(HARNESS,
                   tools_by_role={"parent": "Read, Workflow"},
                   disallowed_tools_by_role={"parent": ["Bash(rm:*)"]})
    args = build(rig, "parent", harness=harness, role="parent", ladder_tier=3,
                 scaffold=None, target="vision:alive")
    assert variadic_values(args, "--tools") == ["Read", "Workflow"]
    assert variadic_values(args, "--allowedTools") == ["Read", "Workflow"]
    assert variadic_values(args, "--disallowedTools") == ["Bash(rm:*)"]


def test_per_role_override_only_claims_the_named_role(rig):
    """A per-role map that does not name this role falls back to the flat key,
    then to the tier-aware default."""
    harness = dict(HARNESS, tools_by_role={"parent": ["Read"]},
                   disallowed_tools="Bash(rm:*)")
    # a kid with the map present, not named -> flat/default
    args = build(rig, "kid", harness=harness, role="kid", ladder_tier=4)
    assert "Read" in variadic_values(args, "--tools")
    assert variadic_values(args, "--disallowedTools") == ["Bash(rm:*)"]


def test_effort_may_be_a_per_tier_map():
    """2026-09-06: `effort` may map tier -> level. A tier the map does not
    name gets no --effort at all -- never another tier's value, the same
    no-fallback rule `models` has -- so a director at `max` cannot leak its
    dial onto a kid. Exercised on model_args directly: brief.py has no
    director brief yet (loop L2 wave 3), so build_command cannot be used."""
    from adapters import claude_code_adapter as cc
    harness = {"adapter": "claude_code", "effort": {"director": "max"},
               "models": {"kid": "k", "director": "d"}}
    args = cc.model_args(harness, "director")
    assert args[args.index("--effort") + 1] == "max"
    assert "--effort" not in cc.model_args(harness, "kid")


# --- hypothesis:l3-meter-own-transcript: session pinning --------------------


def test_session_id_from_stream_json_log():
    """The first stream-json event line carries the session_id; a raw line or
    an empty log yields None."""
    from adapters import claude_code_adapter as cc
    log = Path("/tmp") / "cc-sess-unittest.jsonl"
    log.write_text(
        '{"type":"assistant","session_id":"abc-123","message":{"role":"assistant","usage":{"input_tokens":1}}}\n'
        '{"type":"assistant","session_id":"ignored","message":{"role":"assistant","usage":{"input_tokens":2}}}\n'
    )
    assert cc.session_id_from_stream_json(log) == "abc-123"
    # a log with no session_id yet
    empty = Path("/tmp") / "cc-sess-empty.jsonl"
    empty.write_text("not json\n")
    assert cc.session_id_from_stream_json(empty) is None
    empty.unlink()
    log.unlink()




# --- hypothesis:l3-meter-own-transcript: session pinning --------------------


def test_session_id_from_stream_json_log(tmp_path):
    """The first stream-json event line carries the session_id; a raw line or
    an empty log yields None."""
    from adapters import claude_code_adapter as cc
    log = tmp_path / "cc-sess-unittest.jsonl"
    log.write_text(
        '{"type":"assistant","session_id":"abc-123","message":{"role":"assistant","usage":{"input_tokens":1}}}\n'
        '{"type":"assistant","session_id":"ignored","message":{"role":"assistant","usage":{"input_tokens":2}}}\n'
    )
    assert cc.session_id_from_stream_json(log) == "abc-123"
    empty = tmp_path / "cc-sess-empty.jsonl"
    empty.write_text("not json\n")
    assert cc.session_id_from_stream_json(empty) is None




# --- hypothesis:l3-meter-own-transcript: session pinning --------------------


def test_session_id_from_stream_json_log(tmp_path):
    """The first stream-json event line carries the session_id; a raw line or
    an empty log yields None."""
    from adapters import claude_code_adapter as cc
    log = tmp_path / "cc-sess-unittest.jsonl"
    log.write_text(
        '{"type":"assistant","session_id":"abc-123","message":{"role":"assistant","usage":{"input_tokens":1}}}\n'
        '{"type":"assistant","session_id":"ignored","message":{"role":"assistant","usage":{"input_tokens":2}}}\n'
    )
    assert cc.session_id_from_stream_json(log) == "abc-123"
    empty = tmp_path / "cc-sess-empty.jsonl"
    empty.write_text("not json\n")
    assert cc.session_id_from_stream_json(empty) is None


def test_record_session_pin_derives_transcript_then_meter_reads_it(monkeypatch, tmp_path, capsys):
    """Dispatch captures the child's session_id into a `.meter` pin; the rotate
    meter's pin rule then reads THAT transcript even when a newer foreign one
    sits in the shared project dir (the hypothesis's bug without the fix)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import locations
    from adapters import claude_code_adapter as cc
    import agi.bin.rotate as rotate

    # a fake graph: config marks tmp_path/.agi as the graph dir; sessions under it
    graph = tmp_path / ".agi"
    graph.mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text("{}")
    sess = graph / "sessions" / "iter-001" / "a00-test"
    sess.mkdir(parents=True)
    logf = sess / "output.log"
    logf.write_text('{"type":"assistant","session_id":"own-sess-1","message":{"role":"assistant","usage":{"input_tokens":5000}}}\n')

    our_slug = cc._cc_slug(str(tmp_path))
    proj = tmp_path / ".claude" / "projects"
    (proj / our_slug).mkdir(parents=True, exist_ok=True)
    own = proj / our_slug / "own-sess-1.jsonl"
    own.write_text('{"message":{"role":"assistant","usage":{"input_tokens":5000,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}\n')
    foreign = proj / our_slug / "foreign-newer.jsonl"
    foreign.write_text('{"message":{"role":"assistant","usage":{"input_tokens":99500,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}\n')

    monkeypatch.setattr(cc, "CC_PROJECTS_DIR", proj)
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", proj)
    # the meter resolves its root the same way both sides do: the graph dir
    monkeypatch.setattr(rotate, "find_project_root", lambda: graph)
    monkeypatch.setattr(locations, "find_project_root", lambda start=None: graph)
    monkeypatch.setattr(rotate, "load_ladder_field",
                        lambda root, field, default: {"director_context_tokens": 100000}.get(field, default))
    monkeypatch.setattr(rotate, "_derive_cc_slug", lambda cwd: cc._cc_slug(cwd))

    pin = cc.record_session_pin(sess_dir=sess, agent_id="a00-test",
                                cwd=str(tmp_path), log_file=logf)
    assert pin is not None and pin.exists()
    assert (graph / "sessions" / "a00-test.meter").exists()

    result = rotate.main(["meter"])
    out = capsys.readouterr().out
    assert result == 0
    assert "0.0500" in out, out          # ours (pinned), not foreign (0.995)
    assert "source=claude-code transcript (pinned)" in out


# --- hypothesis:l3-cc-adapter-zombie-lease: session-limit + reaping ---------


def test_limit_from_result_text_detects_subscription_limit():
    """A result line carrying Claude Code's own session-limit text answers the
    reset time; a clean finished turn answers None."""
    from adapters import claude_code_adapter as cc
    hit = "You've hit your session limit \u00b7 resets 5:20am (America/New_York)"
    assert cc.limit_from_result_text(hit) == "5:20am (America/New_York)"
    assert cc.limit_from_result_text("The hedging trade closed cleanly.") is None
    assert cc.limit_from_result_text("") is None


def test_scan_log_for_session_limit_yields_no_retry_and_one_limit_line(tmp_path):
    """The fake stream carrying the limit text yields a detected limit (no
    retry: the close is a single non-zero return) and exactly one LIMIT line."""
    from adapters import claude_code_adapter as cc
    import json as _json
    log = tmp_path / "output.log"
    events = [
        {"type": "assistant", "text": "working..."},
        {"type": "result", "subtype": "success", "text": "Work finished."},
        {"type": "result",
         "text": "You've hit your session limit \u00b7 resets 5:20am (America/New_York)"},
    ]
    log.write_text("".join(_json.dumps(e) + "\n" for e in events))
    is_limit, reset = cc.scan_log_for_session_limit(log)
    assert is_limit is True
    assert reset == "5:20am (America/New_York)"

    # close: one LIMIT line appended, no stream of retries, non-zero return.
    rc = cc.close_session_limit(log_file=log, reset_time=reset)
    assert rc == cc.SESSION_LIMIT_EXIT and rc != 0
    body = log.read_text()
    assert body.count('"subtype": "session_limit"') == 1


def test_close_session_limit_releases_the_lease(tmp_path):
    """A real spawn-budget lease a session-limited child would hold must be
    released at close, not left for the next sweep."""
    from adapters import claude_code_adapter as cc
    import spawn_budget
    root = tmp_path / "repo"
    cap = 10
    lease = spawn_budget.acquire(root, cap, agent_id="a00-limit",
                                 tier="director", iter_n=3)
    assert lease is not None
    spawn_budget.commit(lease, os.getpid())  # a live pid: the lease is held
    assert lease.path.exists()

    log = tmp_path / "output.log"
    rc = cc.close_session_limit(log_file=log, reset_time="5:20am",
                                lease=lease)
    assert rc == cc.SESSION_LIMIT_EXIT
    assert spawn_budget.live_count(root) == 0  # released at exit, not sweep
    assert not lease.path.exists()


def test_finished_child_leaves_no_zombie_not_a_real_spawn():
    """A completed claude-code child must leave no state-Z entry in
    /proc/<pid>/stat after its turn -- a fake child that os._exit(0)s and is
    never wait()ed is exactly the defunct the hypothesis measured holding its
    slot. We fork for real and reap with the adapter's helper."""
    from adapters import claude_code_adapter as cc
    pid = os.fork()
    if pid == 0:
        os._exit(0)
    # leave it un-waited: the parent must not reap before we assert Z
    import time as _t
    _t.sleep(0.1)
    assert cc._procstate(pid) == "Z"          # the unreaped-defunct condition
    assert cc.is_alive(pid) is False          # a zombie is NOT a live slot
    assert cc.reap_child(pid, timeout=3.0) is True  # reaped, no Z remains
    assert cc._procstate(pid) is None


def test_is_alive_still_true_for_a_live_pid():
    from adapters import claude_code_adapter as cc
    assert cc.is_alive(os.getpid()) is True
