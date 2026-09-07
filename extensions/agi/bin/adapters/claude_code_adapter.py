"""The Claude Code harness. `goal:g4.6`.

Implemented 2026-09-03, the week the pi harness went dark: the OpenRouter
workspace hit its weekly budget and every pi spawn 403'd, which is exactly the
situation a second harness exists for. Same seam as `pi_adapter`: this file
owns the argv and the environment, `brief.py` owns what the agent is told, and
`dispatch.py` was not edited -- `mvp:unified-spawn-path`'s first falsifier
holds for the second harness too.

Four facts about the `claude` CLI that shape the argv, each measured on
2026-09-03 with a one-turn probe rather than assumed:

  - **`--append-system-prompt` repeated is last-wins.** Two flags carrying
    "codename ALPHA" and "colour BLUE" answered `UNKNOWN/blue`. pi's spelling
    (one flag per segment) would silently drop every brief segment but the
    last, so the whole brief -- zoom context, tier brief, skill prompt -- is
    written to ONE file per agent and passed once via
    `--append-system-prompt-file`. The file is a session artefact beside
    `context.md` and `agent.json`: what this agent was told, materialized.
  - **Variadic flags swallow the positional prompt.** `--tools`,
    `--allowedTools`, `--disallowedTools` and `--add-dir` all take `...` and a
    prompt placed after them is read as another tool name ("Input must be
    provided either through stdin or as a prompt argument"). The closing line
    is fenced behind `--`, and every variadic flag stays in front of it.
  - **`-p` is what makes it headless**, same as pi: without it the prompt
    opens the interactive TUI, which off a TTY renders nothing and never
    exits. `--output-format stream-json` is the default because it logs every
    turn as it happens; a `json` blob arrives only at the end, so an agent
    killed by the timeout would leave the same permanently empty `output.log`
    pi did on 2026-09-01.
  - **Auth is on disk, not in the environment.** `claude -p` answered under
    both the scrubbed and the full environment, because a subscription login
    lives in the credential store. So `child_env` has nothing to inject; what
    it must NOT do is inherit pi's scrub. `dispatch.scrubbed_env` strips
    `ANTHROPIC_*` / `CLAUDE_CODE_*` so a pi child cannot bill the interactive
    subscription -- for a Claude Code child that billing IS the sanctioned
    path, and a host-managed session (`ANTHROPIC_BASE_URL` pointing at the
    host's proxy) needs those names back to route through the same auth the
    director is using. They are restored by namespace, not by list, so a name
    added to the scrub tomorrow is handed back without editing this file.
    **The one exception is absolute**: `provisioning.PROVISIONING_KEY_VAR`,
    the key that mints keys, is never handed to a child on any path
    (`goal:g1.11`) -- not from the base, not from the inherited environment,
    not from `harness.env`.

Two bounds the harness enforces rather than requests, both config-overridable:

  - **Tools are a closed list** (`--tools`, and the same list auto-approved
    via `--allowedTools`, since `-p` cannot prompt). `Agent` is deliberately
    absent: a kid that spawns Claude Code subagents is a population
    `spawn_budget` cannot see, which is the unbounded-grandchildren failure
    `goal:g4.8` item 3 closed for `dispatch.py` spawns.
  - **Git write verbs, HANDOFF.md/CLAUDE.md writes, and dispatch.py runs are
    refused** (`--disallowedTools`). The kid brief says "DO NOT run git"; on
    2026-09-02 a kid ran `git add -A && git commit` and swept up a director's
    mid-edit CLAUDE.md anyway (`goal:g4.1`). `goal:s34` item 10 extends the
    same refusal to HANDOFF.md writes, CLAUDE.md writes, and dispatch.py runs
    -- every hazard carried in a handoff is closed in the loop, not carried
    again. A rule the harness enforces is worth more than the same rule in
    three documents.

MCP servers are off by default (`--strict-mcp-config` with none named). The
director's interactive session may carry trading, calendar and browser
servers; a detached kid inheriting them is the same shape of leak the env
scrub exists to close, one layer up.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import brief
import locations
import provisioning

NAME = "claude-code"

#: Fallback only. `harness["bin"]`, then $CLAUDE_BIN, then this (resolved on
#: PATH by Popen).
DEFAULT_BIN = "claude"

#: Built-in tools a spawned agent may reach; also the auto-approved list. No
#: `Agent`, no `WebFetch` -- a kid's job is the graph in front of it.
DEFAULT_TOOLS = ("Bash", "Read", "Edit", "Write", "Glob", "Grep")

#: Git verbs the kid brief forbids, refused by the harness rather than asked.
#: Read-only git (`status`, `diff`, `log`) stays available.
DEFAULT_DISALLOWED_TOOLS = tuple(
    f"Bash(git {verb}:*)"
    for verb in ("commit", "add", "push", "stash", "checkout", "reset", "rm")
) + (
    # goal:s34 item 10: refuse HANDOFF.md writes, CLAUDE.md writes, dispatch.py runs
    "Bash(*HANDOFF.md:*)",
    "Bash(*CLAUDE.md:*)",
    "Bash(*dispatch.py:*)",
)

#: Output formats `claude -p` accepts. `stream-json` is the default because it
#: logs as it goes -- see the module docstring.
OUTPUT_FORMATS = ("stream-json", "json", "text")
DEFAULT_OUTPUT_FORMAT = "stream-json"

#: Environment namespaces the shared scrub strips and this adapter hands back.
#: Namespaces rather than names, so a scrub entry added tomorrow is restored
#: without an edit here.
RESTORED_PREFIXES = ("ANTHROPIC_", "CLAUDE_CODE_")
RESTORED_NAMES = frozenset({"CLAUDECODE", "CLAUDE_AGENT_SDK_VERSION"})

#: Never handed to a child, from any source, on any path (`goal:g1.11`).
NEVER_HANDED_DOWN = frozenset({provisioning.PROVISIONING_KEY_VAR})

#: The one system-prompt file per agent, beside `context.md` and `agent.json`.
SYSTEM_PROMPT_FILE = "system-prompt.md"


def resolve_bin(harness: dict) -> str:
    """$CLAUDE_BIN wins over config, which wins over the built-in default.

    Same precedence as `pi_adapter.resolve_bin` and for the same reason: an
    env var is how a machine with the binary somewhere else runs the loop
    without editing a tracked config file.
    """
    return os.environ.get("CLAUDE_BIN") or harness.get("bin") or DEFAULT_BIN


def model_args(harness: dict, tier: str) -> list[str]:
    """`models[tier]` -> `--model`; `effort` -> `--effort`.

    A tier missing from a declared `models` block is an error naming both the
    tier and the harness, never a fallback to the other tier's model -- the
    same rule as pi, because tiering the model is the point of tiers and a
    parent quietly running on the kid's model would look like it worked.

    `effort` is Claude Code's reasoning dial (low|medium|high|xhigh|max),
    the `goal:g4.2` knob pi spells `thinking`. Passed through verbatim so the
    CLI, not this file, is what rejects an unknown level. Either one string
    for every tier, or a mapping by tier (2026-09-06: directors run
    `claude-fable-5-1` at `max`, kids do not need to).
    """
    args: list[str] = []
    models = harness.get("models") or {}
    if models:
        if tier not in models:
            raise KeyError(
                f"harness {harness.get('adapter', NAME)!r} declares no model for "
                f"tier {tier!r}; known tiers: {sorted(models)}"
            )
        model = models[tier]
        if isinstance(model, str) and model.strip():
            args += ["--model", model.strip()]
    effort = harness.get("effort")
    if isinstance(effort, dict):
        # Per-tier dial: {"kid": "high", "director": "max"}. A tier the map
        # does not name gets no --effort, never another tier's value -- the
        # same no-fallback rule as models, for the same reason.
        effort = effort.get(tier)
    if isinstance(effort, str) and effort.strip():
        args += ["--effort", effort.strip()]
    settings = harness.get("settings")
    if isinstance(settings, dict):
        # Per-tier settings (ladder rows resolve one row, so this is the
        # config-facing shape): a tier the map does not name gets none -- the
        # same no-fallback rule as models and effort.
        settings = settings.get(tier)
    if isinstance(settings, str) and settings.strip():
        val = settings.strip()
        # hypothesis:l3w0-ladder-roles-table -- "ultracode" is not an effort
        # level; it is a settings flag the remote ccd sessions on this box
        # run. The adapter spells it, only this file knows the CLI.
        if val == "ultracode":
            obj = {"ultracode": True}
        else:
            try:
                obj = json.loads(val)
            except (json.JSONDecodeError, ValueError):
                obj = val
        args += ["--settings", json.dumps(obj)]
    return args


def _tier_is_ultracode(harness: dict, tier: str | None) -> bool:
    """True when a tier's settings resolve to ultracode.

    Same resolution as `model_args`: a per-tier map names the tier; a whole-
    harness `ultracode` string (or flag dict) applies to every tier
    (hypothesis:l3-rotate-ultracode-env).
    """
    settings = harness.get("settings")
    if settings is None or settings == "":
        return False
    if isinstance(settings, str):
        return settings.strip() == "ultracode"
    if isinstance(settings, dict):
        if set(settings.keys()) == {"ultracode"}:
            return bool(settings.get("ultracode"))
        if tier is not None:
            val = settings.get(tier)
            if isinstance(val, str):
                return val.strip() == "ultracode"
            if isinstance(val, dict):
                return bool(val.get("ultracode"))
    return False


#: The env var that opens Claude Code's dynamic ("ultracode") workflows on
#: this box -- the launch gate the prime confirmed live
#: (hypothesis:l3-rotate-ultracode-env).
ULTRACODE_ENV_VAR = "CLAUDE_CODE_WORKFLOWS"


def child_env(*, harness: dict, base: dict[str, str],
              inherited: dict[str, str] | None = None,
              tier: str | None = None) -> dict[str, str]:
    """The environment the `claude` process runs in.

    `base` arrives already scrubbed by `dispatch.scrubbed_env`. That scrub is
    pi's protection against billing the subscription; for this harness the
    subscription is the sanctioned path, so everything the scrub removed
    under `RESTORED_PREFIXES` / `RESTORED_NAMES` is handed back from
    `inherited` (the dispatcher's own environment by default). `base` wins
    where both have a value; `harness.env` wins over both.

    `NEVER_HANDED_DOWN` is removed from every source, including `base` -- a
    restart path that passes the raw environment as `base` must not become
    the one place the provisioning key reaches a child.
    """
    src = os.environ if inherited is None else inherited
    env = {k: v for k, v in base.items() if k not in NEVER_HANDED_DOWN}
    for key, value in src.items():
        if key in env or key in NEVER_HANDED_DOWN:
            continue
        if key.startswith(RESTORED_PREFIXES) or key in RESTORED_NAMES:
            env[key] = value
    extra = harness.get("env") or {}
    env.update({k: str(v) for k, v in extra.items() if k not in NEVER_HANDED_DOWN})
    if _tier_is_ultracode(harness, tier):
        # the launch gate for ultracode workflows
        # (hypothesis:l3-rotate-ultracode-env)
        env[ULTRACODE_ENV_VAR] = "1"
    return env


def needs_credential(harness: dict) -> bool:
    """Claude Code authenticates through its own credential store on disk;
    it does not need a minted OpenRouter key."""
    return False


def _root_of(sess_dir: Path) -> Path:
    """`<root>/sessions/iter-NNN/<agent>` -> `<root>`.

    The same derivation `pi_adapter.restart` uses for its `cwd`. Falls back to
    `sess_dir` itself for a path too shallow to hold the layout, so a test
    handing in `/tmp` gets a command rather than an IndexError.
    """
    sess_dir = Path(sess_dir)
    parents = sess_dir.parents
    return parents[2] if len(parents) > 2 else sess_dir


def _tool_list(harness: dict, key: str, default) -> list[str]:
    """A config list, a comma-separated string, or the default.

    Strings split on commas only: a permission rule like `Bash(git add:*)`
    carries a space of its own and must stay one item.
    """
    if key not in harness:
        return [str(t) for t in default]
    value = harness[key]
    if value is None:
        return []
    if isinstance(value, str):
        return [t.strip() for t in value.split(",") if t.strip()]
    return [str(t) for t in value]


def write_system_prompt(
    *,
    sess_dir: Path,
    context_file: str,
    segments: list[str],
    skill_prompt: Path | None,
) -> Path:
    """Materialize the whole system prompt as one file in the session dir.

    Order matches pi's argv: zoom context first, then the tier brief, then the
    skill prompt. The context file is required and must exist -- a spawn that
    quietly proceeds without its map is the failure mode this project pays
    for most often, and the caller (zoom) has already produced it or exited
    non-zero. The skill prompt stays optional, as it is for pi.
    """
    if not context_file:
        raise FileNotFoundError(
            f"{NAME}: no context file for this agent; refusing to spawn without "
            f"the zoom context (an agent with no map is not a cheaper agent)"
        )
    ctx = Path(context_file)
    if not ctx.exists():
        raise FileNotFoundError(f"{NAME}: context file {ctx} does not exist")
    parts = [ctx.read_text(encoding="utf-8"), *segments]
    if skill_prompt is not None and Path(skill_prompt).exists():
        parts.append(Path(skill_prompt).read_text(encoding="utf-8"))
    sess_dir = Path(sess_dir)
    sess_dir.mkdir(parents=True, exist_ok=True)
    out = sess_dir / SYSTEM_PROMPT_FILE
    out.write_text("\n\n".join(p.rstrip("\n") for p in parts) + "\n", encoding="utf-8")
    return out


def build_command(
    *,
    harness: dict,
    tier: str,
    context_file: str,
    agent_id: str,
    iter_n: int,
    sess_dir: Path,
    scaffold: dict | None = None,
    cli_py: str | Path = "",
    skill_prompt: Path | None = None,
    dispatch_py: str | Path = "",
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
    brief_tier: str | None = None,
) -> list[str]:
    """The argv that starts one Claude Code agent.

    Shape, and the order is load-bearing (see the module docstring):

        claude -p [--model M] [--effort E]
               --output-format F [--verbose] --strict-mcp-config
               [--max-budget-usd N] --append-system-prompt-file <sess>/system-prompt.md
               [extra_args...]
               --add-dir <repo root> [--mcp-config ...]
               --tools T... --allowedTools T... --disallowedTools R...
               -- "<closing line>"

    `brief_tier` (hypothesis:l3w3-advisor-brief) lets a spawn keep the model
    tier (parent) while assembling a different tier's brief (advisor): the
    model/effort/settings still resolve from `tier`, only the assembled brief
    and its closing line change.
    """
    sess_dir = Path(sess_dir)
    root = _root_of(sess_dir)

    # goal:g1.9 -- the brief is assembled once, by tier, outside every harness.
    # This adapter decides only how to SPELL it, and for Claude Code the only
    # spelling that keeps every segment is one file.
    _btier = brief_tier or tier
    segments = brief.assemble(
        tier=_btier, agent_id=agent_id, iter_n=iter_n, cli_py=cli_py,
        dispatch_py=dispatch_py, scaffold=scaffold, target=target,
        parallel=parallel, max_live=max_live,
    )
    prompt_file = write_system_prompt(
        sess_dir=sess_dir, context_file=context_file, segments=segments,
        skill_prompt=skill_prompt,
    )

    args = [resolve_bin(harness), "-p"]
    args += model_args(harness, tier)

    fmt = str(harness.get("output_format") or DEFAULT_OUTPUT_FORMAT)
    if fmt not in OUTPUT_FORMATS:
        raise ValueError(
            f"harness {NAME!r}: output_format {fmt!r} is not one of {OUTPUT_FORMATS}")
    args += ["--output-format", fmt]
    if fmt == "stream-json":
        # Print mode refuses stream-json without it.
        args += ["--verbose"]
    args += ["--strict-mcp-config"]

    budget = harness.get("max_budget_usd")
    if budget is not None and str(budget).strip():
        args += ["--max-budget-usd", str(budget)]

    args += ["--append-system-prompt-file", str(prompt_file)]
    args += [str(a) for a in (harness.get("extra_args") or [])]

    # --- variadic flags: everything from here to `--` may swallow a positional.
    args += ["--add-dir", str(locations.repo_root(root))]
    mcp = harness.get("mcp_config")
    if mcp:
        args += ["--mcp-config", *([mcp] if isinstance(mcp, str) else [str(m) for m in mcp])]
    tools = _tool_list(harness, "tools", DEFAULT_TOOLS)
    if tools:
        args += ["--tools", *tools]
    allowed = _tool_list(harness, "allowed_tools", tools)
    if allowed:
        args += ["--allowedTools", *allowed]
    disallowed = _tool_list(harness, "disallowed_tools", DEFAULT_DISALLOWED_TOOLS)
    if disallowed:
        args += ["--disallowedTools", *disallowed]

    args += ["--", _closing_turn(harness=harness, tier=tier,
                                  agent_id=agent_id, iter_n=iter_n,
                                  brief_tier=_btier)]
    return args


def _closing_turn(*, harness: dict, tier: str, agent_id: str, iter_n: int,
                  brief_tier: str | None = None) -> str:
    """The `claude -p` closing line (the user turn), keyworded for ultracode.

    An ultracode tier's user turn opens with the bare keyword `ultracode` so
    the dynamic-workflow trigger opts the turn in (hypothesis:l3-rotate-
    ultracode-env; the prime measured live that the keyword must be in the
    user turn for the env var to take effect). The keyword is gated on the
    MODEL tier (`tier`, the parent row) — an advisor is a tier-3 parent and
    runs ultracode while closing as an advisor.
    """
    _btier = brief_tier or tier
    closing = brief.closing_line(_btier, agent_id, iter_n)
    if _tier_is_ultracode(harness, tier):
        closing = "ultracode\n" + closing
    return closing


def is_alive(pid: int) -> bool:
    """Is the process with `pid` still running? `os.kill(pid, 0)` sends no
    signal; it only checks existence. Same as `pi_adapter.is_alive`."""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def restart(
    *,
    harness: dict,
    tier: str,
    context_file: str,
    agent_id: str,
    iter_n: int,
    sess_dir: Path,
    scaffold: dict | None = None,
    cli_py: str | Path = "",
    skill_prompt: Path | None = None,
    dispatch_py: str | Path = "",
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
    agent_record: dict | None = None,
    brief_tier: str | None = None,
) -> int | None:
    """Re-spawn a dead agent. Returns the new pid, or None on failure.

    Same contract as `pi_adapter.restart` (`goal:g4.7`): rebuild the identical
    argv, spawn detached in the same session directory appending to the
    existing log, and stamp the record. A Claude Code agent restarts exactly
    as a pi one does -- there was never a reason for the stub's
    `NotImplementedError` here beyond the stub itself.
    """
    sess_dir = Path(sess_dir)
    args = build_command(
        harness=harness, tier=tier, context_file=context_file,
        agent_id=agent_id, iter_n=iter_n, sess_dir=sess_dir,
        scaffold=scaffold, cli_py=cli_py, skill_prompt=skill_prompt,
        dispatch_py=dispatch_py, target=target, parallel=parallel,
        max_live=max_live, brief_tier=brief_tier,
    )
    log_file = sess_dir / "output.log"
    env = child_env(harness=harness, base=dict(os.environ), tier=tier)
    try:
        with open(log_file, "ab") as logf:
            proc = subprocess.Popen(
                args,
                stdout=logf,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                cwd=str(_root_of(sess_dir)),
                env=env,
            )
    except OSError as exc:
        print(f"restart failed for {agent_id}: {exc}", file=sys.stderr)
        return None
    new_pid = proc.pid
    if agent_record is not None:
        agent_record["pid"] = new_pid
        agent_record["status"] = "restarted"
        agent_record["restarted_at"] = int(time.time())
        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))
    return new_pid
