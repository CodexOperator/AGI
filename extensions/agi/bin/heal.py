#!/usr/bin/env python3
"""heal.py — monitor agent timeouts; spawn healer subagent for hung agents.

Polls <project>/sessions/iter-NNN/manifest.json (or iter-L1.08 for a
loop-scoped id; `locations.iteration_dir`) + each agent.json. For agents
whose status is still 'running' past `timeout_seconds`:
  1. Kill the pid (gracefully → SIGKILL after grace)
  2. Mark agent.json status=hung
  3. Spawn a HEALER pi subprocess with:
     - The hung agent's last log tail
     - Diagnose-and-patch instruction
     - Completion CLI signal

Usage:
    heal.py <project_root> <iter_n> [--poll-interval-s 30] [--max-wait-mins 30]

Returns 0 when ALL agents are in terminal status (done/pending/hung-then-healed/failed).
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
CLI_PY = PLUGIN_ROOT / "bin" / "cli.py"

# goal:g11.1 / goal:s8 — one definition of "which env is safe to hand pi" and
# one of "which model does a pi child run", shared with the other spawner
# rather than re-derived here. `bin/` is on sys.path when this runs as a
# script; the insert makes it so when it is imported as a module too.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import adapters  # noqa: E402 -- the shared (tier, role, harness) resolver
import spawn_gate  # noqa: E402
def _default_role_for_tier(tier):
    """Mirror dispatch's default (role == tier) for the heal path."""
    return tier or "kid"


def _default_tier_for_role(role):
    """The canonical ladder tier a role lives at (mirror of dispatch's)."""
    return {"kid": 0, "parent": 1, "director": 1, "prime_director": 3}.get(
        role, 0)
from dispatch import pi_model_args, scrubbed_env as _scrubbed_env  # noqa: E402
from spawn_budget import TERMINAL  # noqa: E402 -- the ONE terminal-status set (hyp:l4-one-definition-of-terminal)


def _pi_model_args(root: Path, tier: str = "kid",
                   role: str | None = None) -> list[str]:
    """Model flags for the healer, from the ladder when a row exists
    (hypothesis:l4-a-model-change-is-one-write), else the legacy config path.

    Sits on the same shared resolver (`adapters.ladder_role_row` +
    `adapters.spec_from_ladder_row`) dispatch.py uses, so a `write.py` on the
    ladder changes what a healed agent is re-spawned with -- same "one write"
    contract as a fresh dispatch. Never raises: healing runs when something is
    already broken, so a missing or malformed config must cost the healer its
    model preference, not its existence.
    """
    try:
        cfg_path = locations.config_path(root)
        if cfg_path is None:
            return []
        cfg = json.loads(cfg_path.read_text())
        roles = spawn_gate.read_ladder_roles(root / "nodes" if root else None)
        # `tier` here is the HEALED AGENT's record "tier" — a role-string like
        # `parent`/`kid` (dispatch writes args.tier), not the ladder's int. Map
        # the role to its canonical int tier for the lookup.
        _role = role or _default_role_for_tier(tier)
        if str(tier).isdigit():
            _tier_int = int(tier)
        else:
            _tier_int = _default_tier_for_role(_role)
        row = adapters.ladder_role_row(roles, _tier_int, _role)
        if row is not None and (row.get("model") or "").strip():
            spec = adapters.spec_from_ladder_row(row)
            harness = {"adapter": "pi", "models": {_role: spec["model"]}}
            if spec.get("thinking"):
                harness["thinking"] = spec["thinking"]
            return adapters.load("pi").model_args(harness, _role)
        return pi_model_args(cfg)
    except Exception as exc:  # noqa: BLE001 — see docstring
        print(f"heal: could not read model config ({exc}); using pi defaults",
              file=sys.stderr)
        return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=locations.iteration_id)
    ap.add_argument("--poll-interval-s", type=int, default=30)
    ap.add_argument("--max-wait-mins", type=int, default=30)
    args = ap.parse_args()

    # goal:g11.1 — resolve the given path the way every other entry point
    # resolves cwd, rather than demanding it already BE the graph root.
    # Identity when driver.sh passes an already-resolved root, so nothing
    # changes for the caller that exists today.
    given = Path(args.project_root).resolve()
    root = locations.find_project_root(given) or given
    iter_dir = locations.iteration_dir(root, args.iter_n)
    manifest_path = iter_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"ERR: no manifest at {manifest_path}", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text())
    timeout_s = int(manifest.get("timeout_seconds", 600))

    deadline = time.time() + args.max_wait_mins * 60
    healed_already: set[str] = set()

    while time.time() < deadline:
        all_terminal = True
        for entry in manifest["agents"]:
            agent_id = entry["id"]
            ap_file = iter_dir / agent_id / "agent.json"
            if not ap_file.exists():
                continue
            rec = json.loads(ap_file.read_text())
            status = rec.get("status", "running")
            # Sync manifest status from agent.json so post_wire sees current state
            if entry.get("status") != status:
                entry["status"] = status
            if status in TERMINAL:
                continue
            if status != "running":
                continue
            all_terminal = False
            elapsed = int(time.time()) - int(rec.get("started_at", 0))
            if elapsed > timeout_s and agent_id not in healed_already:
                _heal(root, args.iter_n, agent_id, rec)
                healed_already.add(agent_id)
                # hypothesis:l4-a-round-alarms-its-dispatcher-by-default — the
                # TIMEOUT event: exactly ONE dm to the seat that dispatched it,
                # naming the reason. No flag; the stamp came from dispatch.
                _alarm_dispatcher(rec, args.iter_n, "timeout", root)
            else:
                # Also detect if pid is dead w/o status update → mark failed.
                pid = int(rec.get("pid", 0))
                if pid > 0 and not _pid_alive(pid):
                    rec["status"] = "failed"
                    rec["finished_at"] = int(time.time())
                    rec["fail_reason"] = "pid disappeared without completion signal"
                    ap_file.write_text(json.dumps(rec, indent=2))
                    # Sync to manifest too
                    entry["status"] = "failed"
                    print(f"agent {agent_id} marked failed (pid {pid} gone)")
                    # hypothesis:l4-a-round-alarms-its-dispatcher-by-default —
                    # the DEATH event: exactly ONE dm naming the reason.
                    _alarm_dispatcher(rec, args.iter_n, "death", root)
        # Persist manifest so post_wire sees current status
        manifest_path.write_text(json.dumps(manifest, indent=2))
        if all_terminal:
            print("all agents terminal")
            return 0
        time.sleep(args.poll_interval_s)

    print("ERR: max-wait exceeded; some agents still non-terminal", file=sys.stderr)
    return 2


def _alarm_dispatcher(rec: dict, iter_n: int | str, reason: str, root: Path) -> None:
    """hypothesis:l4-a-round-alarms-its-dispatcher-by-default — a round that
    DIES or TIMES OUT sends the seat that dispatched it exactly ONE dm naming
    the reason. ids/numbers plus a short reason token only. Absent stamp -> one
    stderr line, no crash; an undeliverable dm is logged, never fatal to a heal
    that is already handling a bad day. The dm must go to the ONE shared inbox
    (send.py resolves it through `locations.shared_sessions_dir`), never a
    CWD-local sessions dir that looks delivered to the recipient but is not
    the file they read.
    """
    dispatcher = rec.get("dispatched_by")
    agent_id = rec.get("id", "?")
    if not dispatcher:
        print(f"warn: no dispatcher stamp for {agent_id}; no {reason} dm "
              "(l4-a-round-alarms-its-dispatcher-)", file=sys.stderr)
        return
    try:
        import send as _send
        _send.send(root, dispatcher,
                   f"iter={iter_n} agent={agent_id} reason={reason}",
                   agent_id)
    except Exception as exc:
        print(f"warn: {reason} dm to {dispatcher} failed: {exc}",
              file=sys.stderr)


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _heal_cwd(root: Path, rec: dict) -> Path:
    """The working tree a healer must patch: the agent's OWN worktree when
    the record says it was a `--branch` spawn, else the resolved root.

    `hypothesis:l3-branch-isolation-partial-break`. A healer's cwd decides
    which tree its source edits touch. The old `cwd=str(root)` re-entered the
    MAIN checkout for every healer, so a healer for a branch agent wrote
    main's `extensions/` while the coherent work sat in the worktree. Prefer
    the recorded `worktree` when it is real on disk; fall back to `root`.
    """
    rec_wt = rec.get("worktree")
    if rec_wt:
        wt = Path(rec_wt).resolve()
        if wt.is_dir():
            return wt
    return Path(root)


def _heal(root: Path, iter_n: int | str, agent_id: str, rec: dict) -> None:
    pid = int(rec.get("pid", 0))
    print(f"healer: agent {agent_id} timed out (pid={pid}), killing + spawning healer")
    if pid > 0 and _pid_alive(pid):
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        time.sleep(2)
        if _pid_alive(pid):
            try:
                os.killpg(os.getpgid(pid), signal.SIGKILL)
            except ProcessLookupError:
                pass

    sess_dir = locations.iteration_dir(root, iter_n) / agent_id
    heal_root = _heal_cwd(root, rec)
    log_path = Path(rec.get("log_file", ""))
    log_tail = ""
    if log_path.exists():
        try:
            data = log_path.read_bytes()
            log_tail = data[-4096:].decode("utf-8", errors="replace")
        except Exception:
            log_tail = "(log unreadable)"

    healer_id = f"heal-{uuid.uuid4().hex[:8]}"
    healer_dir = sess_dir / healer_id
    healer_dir.mkdir(parents=True, exist_ok=True)

    healer_ctx = healer_dir / "context.md"
    healer_ctx.write_text(
        f"""# HEALER for hung agent {agent_id} (iter {iter_n})

The original agent timed out. Diagnose what blocked it and patch.

## Original Agent Record
```json
{json.dumps(rec, indent=2)}
```

## Last 4 KiB of Agent Output
```
{log_tail}
```

## Your Task
1. Identify the failure mode: stuck command, missing dep, infinite loop, syntax error, etc.
2. Apply the smallest patch that unblocks it. Leave it UNCOMMITTED in the
   working tree.
   **Do not commit. Do not push. Do not run git at all.** The loop owns every
   commit, and a commit made here is authored as the repo owner, lands
   unreviewed on the checked-out branch, and says something untrue about who
   changed the engine. This line used to read "NEW commit; do not amend" and a
   healer correctly obeyed it on 2026-09-01 (`7b57b5955`) -- the kid contract
   had forbidden git since 2026-08-31 and this one was never updated to match.
3. If unfixable in <5 turns, mark this agent's verdict as `pending` with reason.
4. When done:
   ```
   python3 {CLI_PY} done {iter_n} {agent_id} --verdict pending --confidence 0.0 \\
     --notes "healed by {healer_id}: <one-line diagnosis>"
   ```
   (Use the ORIGINAL `{agent_id}`, not your healer id, so the manifest closes out.)

Stay surgical. Don't refactor unrelated code.
"""
    )

    pi_bin = os.environ.get("PI_BIN", "/home/ubuntu/.npm-global/bin/pi")
    healer_log = healer_dir / "output.log"
    # Two defects fixed here on 2026-08-31, both silent, both on the path that
    # only runs once something else has already gone wrong:
    #
    #   `--max-turns 8`  pi has no such flag. It printed "Unknown option:
    #                    --max-turns" and exited — *with status 0* — so every
    #                    healer this file ever spawned died before reading its
    #                    own context, and the loop recorded it as launched.
    #   raw environment  this Popen had no `env=`, so a healer inherited the
    #                    ANTHROPIC_*/CLAUDE_CODE_* variables dispatch.py
    #                    scrubs, and billed the interactive Claude Code
    #                    subscription. The scrub existed; the healer sat
    #                    outside it.
    #
    # The model flags are new for the same reason dispatch.py grew them: a
    # healer that silently runs a different model than the kid it is repairing
    # is a confusing thing to debug.
    pi_args = [
        pi_bin,
        *_pi_model_args(root, rec.get("tier", "kid"), rec.get("role")),
        # Headless, matching `pi_adapter.build_command`. Note this path ran
        # WITHOUT `-p` and did not hang, which is why the hang that prompted
        # adding it is still unexplained -- see `7b57b5955`.
        "-p",
        "--append-system-prompt", f"@{healer_ctx}",
        f"You are healer {healer_id}. Diagnose and patch.",
    ]
    with open(healer_log, "wb") as logf:
        proc = subprocess.Popen(
            pi_args,
            stdout=logf,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            cwd=str(heal_root),
            env=_scrubbed_env(),
        )

    rec["status"] = "hung-healed"
    rec["healer"] = {
        "id": healer_id,
        "pid": proc.pid,
        "context_file": str(healer_ctx),
        "log_file": str(healer_log),
        "command": " ".join(shlex.quote(a) for a in pi_args),
    }
    rec["finished_at"] = int(time.time())
    (sess_dir / "agent.json").write_text(json.dumps(rec, indent=2))
    print(f"healer {healer_id} spawned pid={proc.pid} for hung agent {agent_id}")


if __name__ == "__main__":
    sys.exit(main())
