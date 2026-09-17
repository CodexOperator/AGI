#!/usr/bin/env python3
"""Tool-call trajectory capture driver (hypothesis:l4-every-pi-kid-keeps-its-
full-tool-call-trajectory-at-spawn-never-pruned-never-rebuilt).

pi's session store prunes tool RESULTS, and dispatch.py exits right after
spawn (inline reaper off by default), so no parent may tee the child: the pi
adapter spawns THIS wrapper instead of bare pi. It runs the real pi under
`--mode json`, tees pi's stdout to output.log (dispatch redirects the
wrapper's stdout there) while parsing each `tool_execution_end` into one
ordered jsonl entry on trajectory.jsonl, forwards SIGTERM/SIGINT to pi and
exits with pi's code. A trajectory path that cannot open/write yields exactly
ONE named line -- never silence, never a fabricated record.

usage: pi_trajectory.py --wrapper <pi-bin> <trajectory.jsonl> -- [pi args...]
"""
from __future__ import annotations

import json
import signal
import subprocess
import sys

_NAMED = "trajectory: not captured: {}\n"


def main(argv):
    a = argv[1:]
    if len(a) < 5 or a[0] != "--wrapper" or a[3] != "--":
        return 2
    pi_bin, traj_path, pi_args = a[1], a[2], a[4:]
    pi = subprocess.Popen([pi_bin, *pi_args], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda s, f, p=pi: p.send_signal(s))
    trajf, failed = None, False
    try:
        trajf = open(traj_path, "a", encoding="utf-8")
    except OSError as exc:
        failed = True
        sys.stdout.write(_NAMED.format(exc))
        sys.stdout.flush()
    for raw in pi.stdout:
        sys.stdout.buffer.write(raw)
        sys.stdout.flush()
        if trajf is None:
            continue
        try:
            ev = json.loads(raw)
        except Exception:
            continue  # not a json event (e.g. pi's plain-text stream error)
        if ev.get("type") != "tool_execution_end":
            continue
        try:
            trajf.write(json.dumps({
                "ts": ev.get("timestamp"), "tool": ev.get("toolName"),
                "args": ev.get("args"), "result": ev.get("result"),
                "isError": bool(ev.get("isError"))}) + "\n")
            trajf.flush()
        except Exception as exc:
            if not failed:
                sys.stdout.write(_NAMED.format(exc))
                sys.stdout.flush()
                failed = True
            trajf.close()
            trajf = None
    if trajf is not None:
        trajf.close()
    return pi.wait()


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)