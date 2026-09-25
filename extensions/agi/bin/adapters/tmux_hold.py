"""Explicit-environment seam for a held tmux pane."""
from __future__ import annotations
import subprocess
from collections.abc import Mapping, Sequence


def _cmd(argv: Sequence[str], *, env: Mapping[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run one tmux command with the caller's complete child environment."""
    return subprocess.run(["tmux", *argv], env=dict(env or {}), check=True,
                          capture_output=True, text=True)


def _window_exists(*, pane: str, env: Mapping[str, str]) -> bool:
    """Whether the configured named window already exists in tmux."""
    try:
        _cmd(["list-windows", "-t", pane, "-F", "#{window_id}"], env=env)
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


def _with_env(argv: Sequence[str], env: Mapping[str, str]) -> list[str]:
    """Prefix the launched process with the complete sanitized environment."""
    assignments = [f"{key}={value}" for key, value in sorted(env.items())]
    return ["env", *assignments, *argv]


def start(*, pane: str, argv: Sequence[str], env: Mapping[str, str]) -> subprocess.CompletedProcess:
    """Create the held pane only when its named window is absent."""
    if _window_exists(pane=pane, env=env):
        return _cmd(["display-message", "-p", "-t", pane, "#{window_id}"], env=env)
    return _cmd(["new-window", "-t", pane, "-n", pane, "--",
                 *_with_env(argv, env)], env=env)


def respawn(*, pane: str, argv: Sequence[str], env: Mapping[str, str]) -> subprocess.CompletedProcess:
    """Replace the dead process in the existing window/pane, never create one."""
    return _cmd(["respawn-window", "-k", "-t", pane, "--",
                 *_with_env(argv, env)], env=env)


def reattach(*, pane: str, env: Mapping[str, str]) -> subprocess.CompletedProcess:
    """Reattach a held pane with the same explicit environment contract."""
    return _cmd(["attach-session", "-t", pane], env=env)


def hold_pane(*, pane: str, argv: Sequence[str], env: Mapping[str, str]) -> int:
    """Preserve one named pane, respawning it or creating it when absent."""
    operation = respawn if _window_exists(pane=pane, env=env) else start
    operation(pane=pane, argv=argv, env=env)
    result = _cmd(["display-message", "-p", "-t", pane, "#{pane_pid}"], env=env)
    return int(result.stdout.strip())
