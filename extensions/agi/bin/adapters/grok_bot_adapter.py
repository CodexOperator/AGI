"""The Grok Bot harness — REQUIRED surface, stub argv (goal:g17.14.1).

CLI flags are NOT guessed: `build_command` emits a minimal, measurable argv
(still a stub until `<bin> --help` is read the way `copilot_cli_adapter`'s
was). `restart` is a real respawn (`goal:g4.7`) that rebuilds that same argv —
a stub argv is no reason to refuse the restart contract.
`needs_credential` is False — Grok Bot authenticates through its own channel,
so no OpenRouter key is minted.

`DEFAULT_BIN` is a BARE program name, resolved on PATH by `Popen`, mirroring
`claude_code_adapter.py`. The box path lives in the config `harnesses.grok-bot`
`bin` cell (owned by `goal:g17.14.2`), so no `/home/<user>` literal is baked
into this file.
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import adapters

NAME = "grok-bot"

#: Fallback only. `$GROK_BOT_BIN`, then `harness["bin"]`, then this
#: (PATH-resolved by Popen). The configured box path is a config cell, not
#: a literal here.
DEFAULT_BIN = "grok-bot"

#: The ONE override name; `harness_template._first_arg` reads it too.
ENV_VAR = "GROK_BOT_BIN"


def resolve_bin(harness: dict) -> str:
    """$GROK_BOT_BIN > harness bin > default, via the ONE shared resolver
    in `adapters.resolve_bin` (env, `~`/`{home}`, PATH, named refusal)."""
    return adapters.resolve_bin(harness, ENV_VAR, DEFAULT_BIN)


def model_args(harness: dict, tier: str) -> list[str]:
    """models[tier] -> --model; a missing tier errors by name, never another
    tier's model (a silent fallback would look like it worked)."""
    models = harness.get("models") or {}
    if models and tier not in models:
        raise KeyError(
            f"harness {harness.get('adapter', NAME)!r} declares no model for "
            f"tier {tier!r}; known tiers: {sorted(models)}"
        )
    model = models.get(tier)
    return ["--model", model.strip()] if isinstance(model, str) and model.strip() else []


def child_env(*, harness: dict, base: dict[str, str],
              tier: str | None = None) -> dict[str, str]:
    """Apply the ONE credential-none rule here so no spawn path drifts from
    the mint gate (hypothesis:l4-needs-credential-is-provider-gated)."""
    env = {**base, **{k: str(v) for k, v in (harness.get("env") or {}).items()}}
    return adapters.forward_named_env(
        adapters.drop_unneeded_credential(env, harness), harness)


def build_command(*, harness: dict, tier: str, context_file: str,
                  rendered_brief: str | None = None, **kwargs) -> list[str]:
    """argv: `<bin> [--model M] -p <prompt>`, the copilot spelling.

    `<prompt>` is dispatch's ONE render when it handed one over
    (`rendered_brief`), else the zoom-context path. The flag SHAPE is still a
    stub (`<bin> --help` has not been read, goal:g17.14.1) -- but DISCARDING
    the render was not a stub, it was a silent loss: `context_file` is the
    agent's MAP, not its brief, so a grok-bot spawn would have started with no
    first turn at all. Carrying the render is the one thing here that is
    certain (hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief).

    Neither input present is the OTHER arm of the claim, and it is the arm
    that used to be missing: a falsy `rendered_brief` plus an empty
    `context_file` produced `-p ''` -- an EMPTY PROMPT, i.e. the same silent
    loss as the discarded render, one layer down, and with nothing to name
    it. So that state now refuses by name, the way copilot refuses a missing
    context file.

    `**kwargs` swallows the channels dispatch.py passes every adapter, so a
    spawn cannot die on a TypeError before the flags land."""
    if not rendered_brief and not context_file:
        raise ValueError(
            f"{NAME}: rendered_brief and context_file are both empty; refusing "
            f"to spawn with an empty prompt (an agent with neither its brief "
            f"nor its map is not a cheaper agent, it is a mute one)"
        )
    prompt = rendered_brief if rendered_brief else str(context_file)
    return [resolve_bin(harness), *model_args(harness, tier), "-p", prompt]


def is_alive(pid: int) -> bool:
    """A zombie counts as dead — same /proc rule as pi_adapter."""
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
            if fh.read().rsplit(") ", 1)[1].split()[0] == "Z":
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

    Mirrors `copilot_cli_adapter._restart_cwd` (`goal:g4.7`): a `--branch`
    spawn's record carries `worktree`, and the restarted process must re-enter
    THAT worktree or its relative edits land in the MAIN checkout. A record
    with no usable `worktree` falls back to the historical derivation.
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

    Same contract as `copilot_cli_adapter.restart` (`goal:g4.7`): rebuild the
    identical argv through `build_command`, spawn detached in the same session
    directory appending to the existing log, and stamp the record.
    """
    log_file = sess_dir / "output.log"
    env = child_env(harness=harness, base=adapters.scrubbed_base(base_env), tier=tier)
    try:
        # Inside the try: `build_command` may REFUSE by name (empty prompt),
        # and a restart degrades to None rather than raising through dispatch.
        args = build_command(
            harness=harness, tier=tier, context_file=context_file,
            agent_id=agent_id, iter_n=iter_n, sess_dir=sess_dir,
            scaffold=scaffold, cli_py=cli_py, skill_prompt=skill_prompt,
            dispatch_py=dispatch_py, target=target, parallel=parallel,
            max_live=max_live, brief_tier=brief_tier, role=role,
            ladder_tier=ladder_tier,
            rendered_brief=rendered_brief,
        )
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
    except (OSError, ValueError) as exc:
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
    """Grok Bot uses its own auth channel; no minted OpenRouter key."""
    return False
