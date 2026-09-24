"""Restart a held seat, preferring tmux but never depending on it."""
from __future__ import annotations

import subprocess


def restart(command, child_env, *, tmux_available, session_exists,
            reattach, popen=subprocess.Popen):
    """Return the tmux reattach result, or spawn one direct child as fallback."""
    if tmux_available and session_exists:
        return reattach()
    child = popen(list(command), env=dict(child_env))
    return getattr(child, "pid", None)
