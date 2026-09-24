"""Small hold/restart seam: tmux is preferred, direct Popen is guaranteed."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

__all__ = ["restart", "tmux_available"]


def tmux_available(session: str | None = None) -> bool:
    """Return whether tmux exists and the requested session is present."""
    if not session or not shutil.which("tmux"):
        return False
    try:
        return subprocess.run(["tmux", "has-session", "-t", session],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            check=False).returncode == 0
    except OSError:
        return False


def restart(command: list[str], *, session: str | None = None,
            env: dict | None = None, cwd: str | Path | None = None) -> int | None:
    """Restart ``command``; always use direct Popen when hold is unavailable."""
    if not command:
        return None
    if tmux_available(session):
        # Keep the target attached to the existing hold when possible.
        try:
            subprocess.run(["tmux", "new-window", "-t", session, "--", *command],
                           env=env, cwd=cwd, check=True)
            return None
        except (OSError, subprocess.CalledProcessError):
            pass
    try:
        proc = subprocess.Popen(command, env=env or os.environ.copy(), cwd=cwd)
        return proc.pid
    except OSError:
        return None
