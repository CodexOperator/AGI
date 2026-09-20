"""Probe: is `grok_bot_adapter.restart` a REAL respawn (`goal:g4.7`)?

The restart tests in `test_grok_bot_adapter.py` fake `Popen`, so they prove the
argv and the record stamp but not that a detached process actually comes up.
This probe does not mock anything: it writes a throwaway shell script that
echoes its argv to a marker and sleeps, points the harness `bin` at it, and
calls `restart` through the real `subprocess.Popen`. It then prints the new
pid, `is_alive(new_pid)`, the argv the child saw, the stamped record, whether
`sess_dir/agent.json` exists, and whether `sess_dir/output.log` exists — and
kills the child at the end.

The committed `.out` beside this file is the real capture; a live pid 1..N and
`is_alive True` are the evidence a stub cannot produce. This is the in-tree
path that clears residue R1: the DT.14 probe lived under `.agi/sessions/...`
(gitignored), so nothing the merge target could resolve backed the claim.

Run from the repo root:

    python3 extensions/agi/tests/probes/probe_grok_bot_restart.py
"""
import json
import os
import signal
import sys
import tempfile
import time
from pathlib import Path

BIN = Path("extensions/agi/bin")
sys.path.insert(0, str(BIN))
import adapters  # noqa: E402

grok = adapters.load("grok_bot")

# 1. surface facts
print("NAME", grok.NAME)
print("DEFAULT_BIN", grok.DEFAULT_BIN)
print("needs_credential", grok.needs_credential({"adapter": "grok_bot"}))
print("REQUIRED", list(adapters.REQUIRED))

# 2. real respawn through actual Popen, throwaway grok-bot binary
tmp = Path(tempfile.mkdtemp(prefix="grokprobe-"))
binp = tmp / "grok-bot"
marker = tmp / "ran.txt"
binp.write_text(f'#!/bin/bash\necho "$@" > {marker}\nsleep 30\n')
binp.chmod(0o755)
sess = tmp / "sess"
sess.mkdir()
ctx = tmp / "context.md"
ctx.write_text("ctx")
rec = {"id": "probe", "worktree": str(tmp)}
pid = grok.restart(
    harness={"adapter": "grok_bot", "bin": str(binp),
             "models": {"kid": "grok-4-fast"}},
    tier="kid", context_file=str(ctx), agent_id="probe",
    iter_n=1, sess_dir=sess, agent_record=rec)
alive = grok.is_alive(pid)
for _ in range(100):
    if marker.exists() and marker.read_text().strip():
        break
    time.sleep(0.05)
print("new_pid", pid, "is_alive", alive)
print("argv_seen", marker.read_text().strip() if marker.exists() else "<none>")
print("record", json.dumps(rec))
print("agent_json", (sess / "agent.json").read_text())
print("output_log_exists", (sess / "output.log").exists())

# 3. reap the child so the probe leaves nothing behind
os.kill(pid, signal.SIGKILL)