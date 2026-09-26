"""The GitHub Copilot CLI harness. `goal:g4.6`, third harness.

The parent hypothesis (`hypothesis:l4-copilot-cli-is-a-third-harness-with-the-
same-hooks-as-claude-code-and-pi`) claims the `copilot` binary is a third
spawn target that fits the existing adapter seam with **no edit to
`dispatch.py`**: one config entry plus this file. It is, and this file is the
proof — nothing here is imported by dispatch except through
`adapters.load()`, which reads `harnesses.copilot-cli.adapter`.

Five facts about the CLI shape the argv, each read from the installed binary
(v1.0.83) on 2026-09-14 rather than assumed:

  - **There is no system-prompt flag.** `copilot --help` has no
    `--append-system-prompt`, no `--append-system-prompt-file`, no
    `--system-prompt`. The documented instruction channels are AGENTS.md /
    repo custom instructions (`--no-custom-instructions` turns them off) and
    the `-p` prompt body itself. So the brief is assembled through
    `brief.assemble` exactly as pi and Claude Code do, then written into the
    session as `prompt.md` and handed to the CLI as the `-p` text — a LEADING
    INSTRUCTION BLOCK in the one turn the CLI runs. This is the fallback the
    parent claim allowed when "the only route is a leading instruction block
    in the prompt"; it is stated here because a reader who greps for a
    `--system-prompt` flag will not find one and must know why.
  - **`-p` is the non-interactive contract.** `-p, --prompt <text> Execute a
    prompt in non-interactive mode (exits after completion)`.
  - **`--allow-all-tools` is required for non-interactive mode** ("required
    for non-interactive mode", env `COPILOT_ALLOW_ALL`), so a `-p` run
    without it would block on the first tool prompt off a TTY.
  - **Auth is an environment token, not a keychain entry.** The CLI checks
    `COPILOT_GITHUB_TOKEN` > `GH_TOKEN` > `GITHUB_TOKEN`. Measured on this
    box: `copilot login --with-token` exits 1 with "Login succeeded, but the
    token was not saved. Install a system keychain", so NOTHING persists and
    every spawn must carry a token. `child_env` therefore resolves one (env
    first, then `gh auth token`) and injects it as `GH_TOKEN`; absent a token
    the spawn is left to fail as itself rather than being silently mangled
    here.
  - **`--model <name>` takes the config value verbatim.** The shipped row
    uses `auto` because this account's `models.list` returns only `auto`
    (experiment:a00-4e3f8a7b-8edc1e, conjunct 3), but the adapter still
    emits `--model <models[tier]>` so a Pro entitlement can name a model by
    editing one config cell, never this file.

Which credential a spawn needs: none of the OpenRouter kind. Copilot
authenticates through the GitHub token above, so `needs_credential` returns
False and dispatch mints no per-spawn OpenRouter key for it — the same rule
Claude Code's subscription auth already earned.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import adapters
import brief
import harness_template

NAME = "copilot-cli"

#: Fallback only. `$COPILOT_BIN`, then `harness["bin"]`, then this (a bare
#: PATH name; `adapters.resolve_bin` consults PATH at resolve time).
DEFAULT_BIN = "copilot"

#: The ONE override name; `harness_template._first_arg` reads it too.
ENV_VAR = "COPILOT_BIN"

#: The one prompt artefact per agent, beside `context.md` and `agent.json`.
#: Copilot Code has no system-prompt flag, so what the agent was told is
#: materialized here and passed whole as the `-p` text (module docstring).
PROMPT_FILE = "prompt.md"

#: Token names the Copilot CLI checks, in ITS precedence order (highest
#: first). The adapter reads an already-present value before running `gh`;
#: it writes back under `GH_TOKEN`, which is the middle name and is accepted.
TOKEN_VARS = ("COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")


def resolve_bin(harness: dict) -> str:
    """`$COPILOT_BIN` wins over config, which wins over the built-in default.

    Same precedence as `pi_adapter.resolve_bin` and for the same reason: an
    env var is how a machine with the binary somewhere else runs the loop
    without editing a tracked config file. Delegates to the one shared
    resolver in `adapters.resolve_bin`.
    """
    return adapters.resolve_bin(harness, ENV_VAR, DEFAULT_BIN)


def model_args(harness: dict, tier: str) -> list[str]:
    """`models[tier]` -> `--model`; `effort` -> `--effort`.

    A tier missing from a declared `models` block is an error naming both the
    tier and the harness, never a fallback to the other tier's model -- the
    same rule pi and Claude Code carry, because tiering the model is the point
    of tiers and a parent quietly running on the kid's cheap model would look
    like it worked. A model of `auto` is passed through: it is a real model
    selector to this CLI ("use 'auto' to let Copilot pick automatically"), not
    an absent value.

    `effort` is Copilot's reasoning dial (`--effort, --reasoning-effort`,
    none|minimal|low|medium|high|xhigh|max). A per-tier map names the tier; a
    tier it does not name gets no flag, never another tier's value.
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
        effort = effort.get(tier)
    if isinstance(effort, str) and effort.strip():
        args += ["--effort", effort.strip()]
    return args


def _resolve_token() -> str | None:
    """A GitHub token for a Copilot spawn, or None when none is available.

    An inherited name wins (it is the one the CLI itself would read); only
    when none is set does this shell out to `gh auth token`, which is the
    measured-working source on this box. Never raises: a host without `gh`
    still spawns, and the failure lands where it belongs -- in the CLI.
    """
    for name in TOKEN_VARS:
        value = os.environ.get(name)
        if value and value.strip():
            return value.strip()
    try:
        out = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True, text=True, timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode == 0 and out.stdout.strip():
        return out.stdout.strip()
    return None


def child_env(*, harness: dict, base: dict[str, str],
              tier: str | None = None) -> dict[str, str]:
    """The environment the `copilot` process runs in.

    `base` arrives already scrubbed by `dispatch.scrubbed_env`, which strips
    pi's Anthropic credentials. Copilot needs a GitHub token in the
    environment instead -- nothing persists on disk (measured: no keychain),
    so a spawn with no `GH_TOKEN` is an unauthenticated spawn. `harness.env`
    wins over the resolved token, and an inherited token (if the dispatcher
    has one) is used before shelling out to `gh`.
    """
    env = {k: v for k, v in base.items()}
    if not any(env.get(name) for name in TOKEN_VARS):
        token = _resolve_token()
        if token:
            env["GH_TOKEN"] = token
    extra = harness.get("env") or {}
    env.update({k: str(v) for k, v in extra.items()})
    # hypothesis:l4-needs-credential-is-provider-gated -- the one shared
    # credential-none rule; copilot needs no OpenRouter key today, and its
    # restart path reaches the rule through this same `child_env`.
    return adapters.forward_named_env(
        adapters.drop_unneeded_credential(env, harness), harness)


def write_prompt(*, sess_dir: Path, context_file: str, segments: list[str],
                 skill_prompt: Path | None, closing: str) -> str:
    """Materialize the whole brief as `prompt.md` and return its text.

    Order matches the other two adapters: zoom context first, then the tier
    brief, then the skill prompt, then the closing turn. The context file is
    required and must exist -- a spawn that quietly proceeds without its map
    is the failure mode this project pays for most often. The skill prompt
    stays optional, as it is for pi and Claude Code.

    The file is a session artefact (what this agent was told, materialized)
    AND the argv source, because Copilot has no system-prompt flag to carry
    the brief any other way (module docstring).
    """
    if not context_file:
        raise FileNotFoundError(
            f"{NAME}: no context file for this agent; refusing to spawn without "
            f"the zoom context (an agent with no map is not a cheaper agent)"
        )
    ctx = Path(context_file)
    if not ctx.exists():
        raise FileNotFoundError(f"{NAME}: context file {ctx} does not exist")
    # Survival profile (move FIVE, hypothesis:l3w4-context-load-minimal): the
    # INJECTION graph stream is goal-listing/traps/history -- exactly what
    # survival drops. Skip the ctx first-part so a survival seat pays ~0 for
    # the map and reads it on demand; same switch (AGI_BRIEF_PROFILE) as pi.
    parts: list[str] = []
    if not brief.survival_selected():
        parts.append(ctx.read_text(encoding="utf-8"))
    parts.extend(segments)
    if skill_prompt is not None and Path(skill_prompt).exists():
        parts.append(Path(skill_prompt).read_text(encoding="utf-8"))
    if closing:
        parts.append(closing)
    text = "\n\n".join(p.rstrip("\n") for p in parts) + "\n"
    sess_dir = Path(sess_dir)
    sess_dir.mkdir(parents=True, exist_ok=True)
    (sess_dir / PROMPT_FILE).write_text(text, encoding="utf-8")
    return text


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
    source_root: str | Path | None = None,
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
    kid_ceiling: int | None = None,
    # hypothesis:l3-parent-never-told-to-iterate, carry-forward axis (SD.12)
    # -- per-kid brief channel threaded into the assembled brief. dispatch.py
    # reads --prompt-file <path|-> and passes the text here; absent (None)
    # leaves the brief byte-identical to today.
    addendum: str | None = None,
    brief_tier: str | None = None,
    session_dir: Path | None = None,
    # hypothesis:l3-pi-adapter-role-kwarg -- dispatch.py passes role= and
    # ladder_tier= to EVERY adapter since hypothesis:l3-cc-tools-by-tier.
    # Copilot has no per-role tool bundle yet, so they are accepted and
    # unused (a spawn must not die on a TypeError at the call site).
    role: str | None = None,
    ladder_tier: int | None = None,
    # hypothesis:l4-brief-resolves-g15-lineage-from-the-nearest-agi -- the
    # project graph root the dispatcher resolved, threaded into the brief so
    # the g15 build-order rule reads the project's `.agi`, not brief.py's own.
    project_root: str | Path | None = None,
    rendered_brief: str | None = None,  # dispatch's ONE render; None assembles here
) -> list[str]:
    """The argv that starts one Copilot CLI agent.

    Shape:

        copilot [--model M] [--effort E] --allow-all --remote
                [extra_args...]
                -p "<zoom context + tier brief + skill prompt + closing line>"

    `brief_tier` lets a spawn keep the model tier (parent) while assembling a
    different tier's brief (advisor), exactly as the other two adapters allow.
    """
    sess_dir = Path(sess_dir)
    # goal:g1.9 -- the brief is assembled once, by tier, outside every harness.
    # This adapter decides only how to SPELL it; for Copilot that spelling is
    # the `-p` text, because the CLI has no system-prompt flag.
    _btier = brief_tier or tier
    _sess = session_dir or sess_dir
    segments = [rendered_brief] if rendered_brief is not None else brief.assemble(
        tier=_btier, agent_id=agent_id, iter_n=iter_n, cli_py=cli_py,
        dispatch_py=dispatch_py, scaffold=scaffold, target=target,
        parallel=parallel, max_live=max_live, session_dir=_sess,
        source_root=source_root, kid_ceiling=kid_ceiling,
        addendum=addendum, project_root=project_root,
    )
    prompt = write_prompt(
        sess_dir=sess_dir, context_file=context_file, segments=segments,
        skill_prompt=skill_prompt,
        closing=brief.closing_line(_btier, agent_id, iter_n, cli_py=cli_py),
    )

    # hypothesis:harness-arg-builders-are-templates-only: argv is DATA
    # (copilot-cli.toml `[shapes.dispatch]`); this fills the slots.
    return harness_template.render(
        NAME, shape="dispatch", bin_path=resolve_bin(harness),
        model_args=model_args(harness, tier),
        extra_args=harness.get("extra_args") or [],
        prompt=prompt,
    )


def is_alive(pid: int) -> bool:
    """Is the process with `pid` still running?

    A zombie (state `Z`) counts as **dead** (`hypothesis:l3-cc-adapter-
    zombie-lease`), same rule as `pi_adapter.is_alive` and
    `claude_code_adapter.is_alive`: its code has exited and only reaping by
    its parent is outstanding, but `os.kill(pid, 0)` answers true for a
    defunct child regardless. Off `/proc` (non-Linux, or the pid raced out of
    the table) falls back to signal-existence rather than guess wrong.
    """
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
            state = fh.read().rsplit(") ", 1)[1].split()[0]
        if state == "Z":
            return False
    except (OSError, IndexError, ValueError):
        pass
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _restart_cwd(sess_dir: Path, agent_record: dict | None) -> Path:
    """The working directory a restarted agent must be born into.

    Mirrors `pi_adapter._restart_cwd` (`hypothesis:l3-branch-isolation-
    partial-break`): a `--branch` spawn's agent_record carries `worktree`, and
    the restarted process must re-enter THAT worktree or its relative source
    edits land in the MAIN checkout. A record with no usable `worktree` falls
    back to the historical derivation, so non-branch restarts behave exactly
    as before.
    """
    if agent_record:
        wt = agent_record.get("worktree")
        if wt:
            worktree = Path(wt).resolve()
            if worktree.is_dir():
                return worktree
    return Path(sess_dir).parent.parent.parent


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
    role: str | None = None,
    ladder_tier: int | None = None,
    rendered_brief: str | None = None,
    # hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env --
    # the base the child env is built from; None means dispatch's scrubbed env.
    base_env: dict | None = None,
) -> int | None:
    """Re-spawn a dead agent. Returns new pid, or None on failure.

    Same contract as `pi_adapter.restart` (`goal:g4.7`): rebuild the identical
    argv, spawn detached in the same session directory appending to the
    existing log, and stamp the record.
    """
    import json

    args = build_command(
        harness=harness, tier=tier, context_file=context_file,
        agent_id=agent_id, iter_n=iter_n, sess_dir=sess_dir,
        scaffold=scaffold, cli_py=cli_py, skill_prompt=skill_prompt,
        dispatch_py=dispatch_py, target=target, parallel=parallel,
        max_live=max_live, brief_tier=brief_tier, role=role,
        ladder_tier=ladder_tier,
        rendered_brief=rendered_brief,
    )
    log_file = sess_dir / "output.log"
    env = child_env(harness=harness, base=adapters.scrubbed_base(base_env), tier=tier)
    try:
        with open(log_file, "ab") as logf:
            proc = subprocess.Popen(
                args,
                stdout=logf,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                cwd=str(_restart_cwd(sess_dir, agent_record)),
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


def needs_credential(harness: dict) -> bool:
    """Copilot authenticates through its own GitHub token (env, no keychain);
    it does not need a minted OpenRouter key."""
    return False
