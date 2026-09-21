"""The Grok Bot harness — REQUIRED surface, MEASURED argv (goal:g7.31.1.1).

CLI flags are NOT guessed. `build_command` emits the bare bin, measured
against a recorded `grok-bot --help` (grok-bot-cli@0.3.1, 46 lines, pasted in
the child experiment of `goal:g7.31.1.1`): the help exposes no `--model` and no
`-p`. The seat's brief is delivered by `send <bot-or-group> <message...>`, not
by argv (`goal:g7.31.2` / `goal:g7.31.4`), so `context_file` stays accepted
but is NOT emitted. `restart` is a real respawn (`goal:g4.7`) that rebuilds
that same argv.
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
    """VALIDATION ONLY — always returns `[]` (goal:g7.31.1.1).

    Model selection is a Grok Bot app/profile field, not a CLI flag: the
    measured 0.3.1 `--help` has no `--model`. The helper is kept so the tier
    contract still fires — a tier absent from a declared `models` block raises
    a KeyError naming the tier, never another tier's model (a silent fallback
    would look like it worked) — but it never emits a flag."""
    models = harness.get("models") or {}
    if models and tier not in models:
        raise KeyError(
            f"harness {harness.get('adapter', NAME)!r} declares no model for "
            f"tier {tier!r}; known tiers: {sorted(models)}"
        )
    return []


def child_env(*, harness: dict, base: dict[str, str],
              tier: str | None = None) -> dict[str, str]:
    """The environment a `grok-bot` process runs in.

    Applies the ONE credential-none rule here so no spawn path drifts from
    the mint gate (hypothesis:l4-needs-credential-is-provider-gated).

    `goal:g7.31.1.1` residue 3 (DT.27 close): the measured 0.3.1 `--help` has
    no `--model`, so the configured tier can only reach `grok-bot` as
    `AGI_MODEL`. dispatch.py exports it on the main spawn path, but the
    `restart` path inherits whatever `os.environ` it was invoked from -- under
    heal/rotate that env may carry no `AGI_MODEL` at all, and the configured
    tier was silently dropped. Stamp it here from the ROW that owns the tier so
    every spawn path carries the same resolved model. The row's `models` cell
    is authoritative (dispatch has already landed ladder/seat overrides into
    it), so it WINS over a stale inherited `AGI_MODEL`.

    MEASURED, DT.29, re-measured DT.32, CORRECTED DT.35 -- compat/no-delivery
    on this CLI: the 0.3.1 SOURCE reads no `AGI_MODEL` (`grep -rn 'AGI_MODEL'
    node_modules/grok-bot-cli/src` exits 1), and that absence holds under the
    full UNION measurement of the source-read env set (25 names, FOUR scans:
    literal dot-accesses; the two `truthyEnv(...)` literals; ALIASED
    DEFAULT-PARAMETER reads `env.<NAME>` (`CODEX_HOME` codex-bridge.js:27-28;
    `APPDATA`/`XDG_CONFIG_HOME` app-session.js:104-110); and a check that the
    only computed `process.env[name]` site in `url-policy.js:13` is called
    with those two truthyEnv literals, never `AGI_MODEL`). So the stamp
    reaches the process env but NOT
    grok-bot's model choice.
    Model selection stays the app/profile field; this is kept for a CLI that
    later reads the name, not a claim of delivery. Test:
    `test_agi_model_is_not_read_by_the_0_3_1_cli_source`."""
    env = {**base, **{k: str(v) for k, v in (harness.get("env") or {}).items()}}
    model_val = (harness.get("models") or {}).get(tier) if tier else None
    if model_val:
        env["AGI_MODEL"] = str(model_val)
    return adapters.forward_named_env(
        adapters.drop_unneeded_credential(env, harness), harness)


def build_command(*, harness: dict, tier: str, context_file: str,
                  **kwargs) -> list[str]:
    """MEASURED argv: the bare resolved bin (goal:g7.31.1.1).

    `grok-bot --help` (grok-bot-cli@0.3.1) offers no `--model` and no `-p`, so
    neither is emitted; the seat's brief travels over `send`, not argv
    (`goal:g7.31.4`). `model_args` still runs for its tier validation, and
    `context_file` stays in the signature for seam compatibility but is not
    emitted. `**kwargs` swallows the channels dispatch.py passes every
    adapter, so a spawn cannot die on a TypeError before the flags land."""
    model_args(harness, tier)  # validation only; --model is not a CLI flag
    return [resolve_bin(harness)]


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
