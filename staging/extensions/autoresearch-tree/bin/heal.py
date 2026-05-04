#!/usr/bin/env python3
"""heal.py — monitor agent timeouts; spawn healer subagent for hung agents.

Polls <project>/sessions/iter-NNN/manifest.json + each agent.json. For agents
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

TERMINAL = {"done", "pending", "hung-healed", "failed"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=int)
    ap.add_argument("--poll-interval-s", type=int, default=30)
    ap.add_argument("--max-wait-mins", type=int, default=30)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
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
        # Persist manifest so post_wire sees current status
        manifest_path.write_text(json.dumps(manifest, indent=2))
        if all_terminal:
            print("all agents terminal")
            return 0
        time.sleep(args.poll_interval_s)

    print("ERR: max-wait exceeded; some agents still non-terminal", file=sys.stderr)
    return 2


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _heal(root: Path, iter_n: int, agent_id: str, rec: dict) -> None:
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

    sess_dir = root / "sessions" / f"iter-{iter_n:03d}" / agent_id
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
2. Apply the smallest patch that unblocks it (NEW commit; do not amend).
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
    pi_args = [
        pi_bin,
        "--append-system-prompt", f"@{healer_ctx}",
        "--max-turns", "8",
        f"You are healer {healer_id}. Diagnose and patch.",
    ]
    with open(healer_log, "wb") as logf:
        proc = subprocess.Popen(
            pi_args,
            stdout=logf,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            cwd=str(root),
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
