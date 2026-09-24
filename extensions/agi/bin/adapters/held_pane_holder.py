"""Initial-spawn holder for a named tmux pane (goal:g7.31.1.2.2)."""
from __future__ import annotations
import os
import re
import shlex
import subprocess

def pane_name(agent_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", agent_id).strip("-")
    if not safe:
        raise ValueError(f"agent id has no tmux-safe characters: {agent_id!r}")
    return "agi-agent-" + safe

def _tmux(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["tmux", *args], text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError((result.stderr or result.stdout or "tmux failed").strip())
    return result.stdout.strip()

class HeldProc:
    def __init__(self, pid: int, pane_id: str):
        self.pid = pid
        self.pane_id = pane_id
    def poll(self):
        try:
            os.kill(self.pid, 0)
        except ProcessLookupError:
            return 1
        return None

def start(*, agent_id: str, argv: list[str], cwd: str, env: dict[str, str],
          log_file: str, **_: object) -> tuple[HeldProc, str]:
    name = pane_name(agent_id)
    if _tmux("has-session", "-t", name, check=False):
        pane_id = _tmux("display-message", "-p", "-t", name, "#{pane_id}")
        pid = int(_tmux("display-message", "-p", "-t", name, "#{pane_pid}"))
        return HeldProc(pid, pane_id), pane_id
    command = f"exec {shlex.join(argv)} >>{shlex.quote(log_file)} 2>&1"
    env_args = [v for key, value in env.items() for v in ("-e", f"{key}={value}")]
    _tmux("new-session", "-d", "-s", name, *env_args, "-c", cwd,
          "sh", "-c", command)
    pane_id = _tmux("display-message", "-p", "-t", name, "#{pane_id}")
    pid = int(_tmux("display-message", "-p", "-t", name, "#{pane_pid}"))
    return HeldProc(pid, pane_id), pane_id
