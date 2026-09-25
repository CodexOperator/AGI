"""Durable tmux hold with a direct-process escape hatch."""
from __future__ import annotations

import subprocess
from pathlib import Path


def hold(command, *, session, pane, cwd=None, env=None,
         runner=subprocess.run, spawner=subprocess.Popen):
    """Hold ``command`` in a named tmux pane, or spawn it directly.

    A missing tmux binary, an unset durable name, or a failed tmux command
    must never turn restart into a no-op.  The direct path is therefore the
    explicit final fallback, not a configuration special case.
    """
    def direct():
        return spawner(command, cwd=cwd, env=env)

    if not session or not pane:
        return direct()
    target = f"{session}:{pane}"
    try:
        present = runner(["tmux", "has-session", "-t", target]).returncode == 0
        action = (["tmux", "attach-session", "-t", target] if present else
                  ["tmux", "new-session", "-d", "-s", session, "-n", pane,
                   *command])
        held = runner(action, env=env)
        if held.returncode == 0:
            return held
    except OSError:
        pass
    return direct()
