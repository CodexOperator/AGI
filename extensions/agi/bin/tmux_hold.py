"""Explicit-environment seam for a held tmux pane.

The dispatcher must not rely on the tmux server's ambient environment.  The
module keeps the tmux command boundary small and injectable for tests.
"""
from __future__ import annotations
import subprocess
from collections.abc import Mapping, Sequence


def _cmd(argv: Sequence[str], *, env: Mapping[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run one tmux command with the caller's complete child environment."""
    return subprocess.run(["tmux", *argv], env=dict(env or {}), check=True,
                          capture_output=True, text=True)


def start(*, pane: str, argv: Sequence[str], env: Mapping[str, str]) -> subprocess.CompletedProcess:
    """Create the held pane without substituting server inheritance."""
    return _cmd(["new-window", "-t", pane, "-n", pane, "--", *argv], env=env)


def reattach(*, pane: str, env: Mapping[str, str]) -> subprocess.CompletedProcess:
    """Reattach a held pane with the same explicit environment contract."""
    return _cmd(["attach-session", "-t", pane], env=env)
