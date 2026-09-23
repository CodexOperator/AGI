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


# --------------------------------------------------------- durable pane hold
#: A held seat is named from its SEAT identity, NEVER a pid: a pid would mint
#: a fresh pane on every restart and the hold would not hold (goal:g7.31.1.2).
PANE_PREFIX = "agi-seat-"


def pane_name(agent_id: str) -> str:
    """The stable tmux pane name a seat's process is held in."""
    return f"{PANE_PREFIX}{agent_id}"


class PaneHoldError(RuntimeError):
    """tmux is PRESENT but the named-pane hold failed: a NAMED refusal, never
    an anonymous fire-and-forget seat (goal:g7.31.1.2)."""


def _tmux(argv: list[str]) -> subprocess.CompletedProcess | None:
    """Run tmux, or None only when tmux is ABSENT (caller falls back).
    A timeout is a present-but-unresponsive tmux, so it is named."""
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=10)
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired as exc:
        raise PaneHoldError(f"tmux {' '.join(argv[1:2])} timed out: {exc}") from exc
    except OSError:
        return None


def pane_listing(name: str) -> list[str]:
    """`tmux list-panes`-shaped view of the seat's durable hold."""
    out = _tmux(["tmux", "list-panes", "-t", name,
                 "-F", "#{session_name} #{pane_pid}"])
    if out is None or out.returncode != 0:
        return []
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def hold_in_pane(*, name: str, args: list[str], cwd: Path,
                 env: dict[str, str] | None = None) -> bool:
    """Run `args` in the ONE named pane: open it once, respawn it thereafter.

    False only when tmux is ABSENT (caller falls back to the direct Popen).
    tmux present but failing raises PaneHoldError -- a named refusal, never
    a silent anonymous process. `env` threads as `-e NAME=VALUE` (before
    `-c`, so the command argv stays last), giving the pane the SAME scrubbed
    child env the direct Popen uses. `remain-on-exit` holds the NAME.
    """
    probe = _tmux(["tmux", "has-session", "-t", name])
    if probe is None:
        return False
    if probe.returncode not in (0, 1):
        raise PaneHoldError(
            f"tmux has-session rc={probe.returncode} for {name}")
    env_flags = [f for k, v in (env or {}).items()
                 for f in ("-e", f"{k}={v}")]
    if probe.returncode == 0:
        cmd = ["tmux", "respawn-pane", "-k", "-t", name,
               *env_flags, "-c", str(cwd)]
    else:
        cmd = ["tmux", "new-session", "-d", "-s", name,
               *env_flags, "-c", str(cwd)]
    started = _tmux([*cmd, *args])
    if started is None:
        return False
    if started.returncode != 0:
        raise PaneHoldError(
            f"tmux {cmd[1]} rc={started.returncode} for pane {name}")
    if probe.returncode != 0:
        _tmux(["tmux", "set-option", "-t", name, "remain-on-exit", "on"])
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
    hold_pane: bool = False,
) -> int | None:
    """Re-spawn a dead agent. Returns new pid, or None on failure.

    Same contract as `copilot_cli_adapter.restart` (`goal:g4.7`): rebuild the
    identical argv through `build_command`, spawn detached in the same session
    directory appending to the existing log, and stamp the record.

    `hold_pane=True` runs that same argv inside ONE named tmux pane
    (`pane_name(agent_id)`) instead -- the durable hold. Absent (the default),
    this is byte-for-byte the direct Popen path (`goal:g7.31.1.2`).
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
    cwd = _restart_cwd(sess_dir, agent_record)
    if hold_pane and hold_in_pane(name=pane_name(agent_id), args=args,
                                  cwd=cwd, env=env):
        name = pane_name(agent_id)
        pane_pid = None
        for line in pane_listing(name):
            try:
                pane_pid = int(line.split()[1])
            except (IndexError, ValueError):
                pass
        if pane_pid is None:
            raise PaneHoldError(
                f"pane {name} is up but its pid could not be read")
        if agent_record is not None:
            agent_record["pid"] = pane_pid
            agent_record["tmux_pane"] = name
            agent_record["status"] = "restarted"
            agent_record["restarted_at"] = int(time.time())
            (sess_dir / "agent.json").write_text(
                json.dumps(agent_record, indent=2))
        return pane_pid
    try:
        with open(log_file, "ab") as logf:
            proc = subprocess.Popen(
                args,
                stdout=logf,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                cwd=str(cwd),
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
