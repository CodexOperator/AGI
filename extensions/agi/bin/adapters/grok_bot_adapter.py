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
    """Grok Bot uses its own auth channel; no minted OpenRouter key."""
    return False


# --- OPTIONAL pane surface (`goal:g7.32.3`), NOT in `adapters.REQUIRED`: a
# caller feature-detects with `hasattr(mod, "pane_send")`, so a pane-free
# harness (pi, claude_code, copilot_cli) simply omits these. Every method
# WRAPS a handle the seat already holds -- none creates, attaches or re-owns a
# pane (durable hold is `goal:g7.31.1`) -- and with no held pane fails closed
# with `NoHeldPaneError` BEFORE any tmux call, never hanging.
class NoHeldPaneError(RuntimeError):
    """A pane method was called with no held pane (goal:g7.32.3)."""


def held_pane_id(handle) -> str:
    """The pane token in a held handle: a pane-id string or {"pane": ...}."""
    if isinstance(handle, str):
        pane = handle.strip()
    elif isinstance(handle, dict):
        pane = str(handle.get("pane") or "").strip()
    else:
        pane = ""
    if not pane:
        raise NoHeldPaneError(
            "no held pane: pass the handle the seat holds, e.g. {'pane': '%3'}; "
            "this adapter never attaches one (goal:g7.31.1 owns the hold)"
        )
    return pane


def has_pane(handle) -> bool:
    """Feature-detectable predicate: does this handle name a held pane?"""
    try:
        held_pane_id(handle)
    except NoHeldPaneError:
        return False
    return True


def pane_send(handle, text: str, *, enter: bool = True) -> None:
    """Type `text` into the already-held pane (wraps `tmux send-keys`)."""
    pane = held_pane_id(handle)
    keys = ["tmux", "send-keys", "-t", pane, "--", str(text)]
    if enter:
        keys.append("Enter")
    subprocess.run(keys, check=True)


def pane_read(handle, *, lines: int = 200) -> str:
    """Return the held pane's visible text (wraps `tmux capture-pane`)."""
    pane = held_pane_id(handle)
    proc = subprocess.run(
        ["tmux", "capture-pane", "-p", "-t", pane, "-S", f"-{int(lines)}"],
        check=True, capture_output=True, text=True,
    )
    return proc.stdout
