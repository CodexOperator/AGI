"""Named tmux hold/start seam for durable agent seats."""
from __future__ import annotations
import os, shlex, subprocess
from pathlib import Path

SESSION = "agi-rc"

def _run(*args: str) -> str:
    return subprocess.run(["tmux", *args], text=True, capture_output=True, check=True).stdout.strip()

def pane(session: str, name: str) -> str | None:
    """Return the live pane id for a named seat, never inventing one."""
    try:
        found = _run("display-message", "-p", "-t", f"{session}:{name}", "#{pane_id}")
        return found if found.startswith("@") else None
    except (OSError, subprocess.CalledProcessError):
        return None

def start(*, name: str, argv: list[str], cwd: str | Path,
          env: dict[str, str], log_file: str | Path,
          session: str = SESSION) -> int:
    """Found (or reuse) a held pane and launch argv in it; return shell pid."""
    target = pane(session, name)
    if target is None:
        target = _run("new-window", "-d", "-P", "-F", "#{pane_id}", "-t", session, "-n", name)
    command = f"cd {shlex.quote(str(cwd))}; exec env {shlex.join([f'{k}={v}' for k,v in env.items()])} {shlex.join(argv)} >>{shlex.quote(str(log_file))} 2>&1"
    _run("send-keys", "-t", target, command, "Enter")
    return int(_run("display-message", "-p", "-t", target, "#{pane_pid}"))
