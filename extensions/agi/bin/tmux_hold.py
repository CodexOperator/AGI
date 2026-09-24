#!/usr/bin/env python3
"""Named tmux hold for a dispatch round.

The dispatcher owns the name; the pane remains addressable after a dispatcher
or model process dies.  This is deliberately a small seam around tmux rather
than a second lifecycle implementation.
"""
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


def start(argv, *, cwd: Path, env: dict, log: Path, name: str):
    """Start ``argv`` in a named tmux session and return the tmux client."""
    log.parent.mkdir(parents=True, exist_ok=True)
    command = "exec " + shlex.join(argv) + " >>" + shlex.quote(str(log)) + " 2>&1"
    with log.open("ab") as out:
        return subprocess.Popen(
            ["tmux", "new-session", "-s", name, "sh", "-lc", command],
            cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
            stdout=out, stderr=subprocess.STDOUT, start_new_session=True)


def reattach(name: str):
    """Reattach an existing hold (used by restart/reattach callers)."""
    return subprocess.run(["tmux", "attach-session", "-t", name], check=False)


def pane(name: str) -> str:
    """Return the stable session:window pane address, or '' when absent."""
    r = subprocess.run(["tmux", "display-message", "-p", "-t", name,
                        "#{session_name}:#{window_index}.#{pane_index}"],
                       text=True, capture_output=True, check=False)
    return r.stdout.strip() if r.returncode == 0 else ""
