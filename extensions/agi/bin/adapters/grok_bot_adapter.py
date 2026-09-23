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


def resolve_bin(harness: dict) -> str:
    """$GROK_BOT_BIN > harness bin > default (pi_adapter's precedence)."""
    return os.environ.get("GROK_BOT_BIN") or harness.get("bin") or DEFAULT_BIN


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
                  **kwargs) -> list[str]:
    """STUB argv: `<bin> [--model M] -p <context_file>`. `**kwargs` swallows
    the channels dispatch.py passes every adapter, so a spawn cannot die on a
    TypeError before the flags land."""
    return [resolve_bin(harness), *model_args(harness, tier),
            "-p", str(context_file)]


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


def pane_name(*, harness: dict, agent_id: str,
              agent_record: dict | None = None) -> str | None:
    """Generic pane opt-in (`goal:g7.31.1.2`): the stable tmux window name
    for this seat, or None when nothing opted in.

    The record's own `pane` (stamped by the first spawn) wins; then a harness
    `pane` cell -- a name when it is a string, else the agent id when the
    cell is a bare `true`. No harness literal appears here, so the seam stays
    harness-agnostic."""
    existing = (agent_record or {}).get("pane")
    if isinstance(existing, str) and existing:
        return existing
    cell = harness.get("pane")
    if isinstance(cell, str) and cell:
        return cell
    return agent_id if cell else None


def spawn(*, harness: dict, tier: str, context_file: str, agent_id: str,
          iter_n: int, sess_dir: Path, agent_record: dict | None = None,
          argv: list[str] | None = None, env: dict | None = None,
          cwd: str | None = None, log_file: Path | None = None,
          log_mode: str = "ab", **kwargs) -> "pane_hold.PaneProc":
    """First-spawn lifecycle entry (`goal:g7.31.1.2`) -- the twin of
    `restart`: the SAME `build_command` argv builder and the SAME
    `ensure_pane` seam.

    When the harness opts into a pane, the seat is BORN inside the named pane
    and the record is stamped `pane`/`pane_session`/`pane_id`, so a later
    `restart` reattaches to a REAL pane -- no hand-injected record field.
    Without the opt-in the ordinary detached Popen path is used.

    `argv`/`env`/`cwd`/`log_file` let a caller (`dispatch._open_round`) hand
    in the ONE already-rendered round it owns -- no second argv path. The
    return is a Popen-compatible `PaneProc` either way."""
    from adapters import pane_hold
    args = argv if argv is not None else build_command(
        harness=harness, tier=tier, context_file=context_file,
        agent_id=agent_id, iter_n=iter_n, sess_dir=sess_dir, **kwargs)
    name = pane_name(harness=harness, agent_id=agent_id,
                     agent_record=agent_record)
    env = env if env is not None else child_env(
        harness=harness, base=dict(os.environ), tier=tier)
    cwd = cwd if cwd is not None else str(_restart_cwd(sess_dir, agent_record))
    log_file = log_file or (sess_dir / "output.log")
    if not name:
        with open(log_file, log_mode) as logf:
            proc = subprocess.Popen(args, stdout=logf,
                                    stderr=subprocess.STDOUT,
                                    stdin=subprocess.DEVNULL,
                                    start_new_session=True, cwd=cwd, env=env)
        return pane_hold.PaneProc(proc.pid, proc=proc)
    session = ((agent_record or {}).get("pane_session")
               or harness.get("pane_session")
               or pane_hold.DEFAULT_TMUX_SESSION)
    if agent_record is not None:
        agent_record["pane"] = name
        agent_record["pane_session"] = session
    pid = pane_hold.ensure_pane(tmux_session=session, name=name, argv=args,
                                cwd=cwd, env=env, log_file=str(log_file))
    if agent_record is not None:
        agent_record["pane_id"] = pane_hold.pane_id(tmux_session=session,
                                                    name=name)
    return pane_hold.PaneProc(pid or 0, tmux_session=session, name=name)


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
) -> int | None:
    """Re-spawn a dead agent. Returns new pid, or None on failure.

    Same contract as `copilot_cli_adapter.restart` (`goal:g4.7`): rebuild the
    identical argv through `build_command`, spawn detached in the same session
    directory appending to the existing log, and stamp the record.
    """
    args = build_command(
        harness=harness, tier=tier, context_file=context_file,
        agent_id=agent_id, iter_n=iter_n, sess_dir=sess_dir,
        scaffold=scaffold, cli_py=cli_py, skill_prompt=skill_prompt,
        dispatch_py=dispatch_py, target=target, parallel=parallel,
        max_live=max_live, brief_tier=brief_tier, role=role,
        ladder_tier=ladder_tier,
    )
    log_file = sess_dir / "output.log"
    env = child_env(harness=harness, base=dict(os.environ), tier=tier)
    cwd = str(_restart_cwd(sess_dir, agent_record))
    _pane = pane_name(harness=harness, agent_id=agent_id,
                      agent_record=agent_record)
    if _pane:
        # Opt-in durable pane hold (`goal:g7.31.1.2`). The pane NAME comes
        # from the record (stamped by this adapter's own `spawn`) or a
        # generic harness cell, so no harness is named here; when nothing
        # opts in, the direct-Popen path below stays byte-identical.
        from adapters import pane_hold
        session = ((agent_record or {}).get("pane_session")
                   or harness.get("pane_session")
                   or pane_hold.DEFAULT_TMUX_SESSION)
        try:
            new_pid = pane_hold.ensure_pane(
                tmux_session=session, name=_pane, argv=args, cwd=cwd,
                env=env, log_file=str(log_file))
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"restart failed for {agent_id}: {exc}", file=sys.stderr)
            return None
        if agent_record is not None:
            agent_record["pid"] = new_pid or 0
            agent_record["status"] = "restarted"
            agent_record["restarted_at"] = int(time.time())
            agent_record["pane_id"] = pane_hold.pane_id(
                tmux_session=session, name=_pane)
            (sess_dir / "agent.json").write_text(
                json.dumps(agent_record, indent=2))
        return new_pid
    try:
        with open(log_file, "ab") as logf:
            proc = subprocess.Popen(
                args,
                stdout=logf,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                cwd=cwd,
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
    """Grok Bot uses its own auth channel; no minted OpenRouter key."""
    return False
