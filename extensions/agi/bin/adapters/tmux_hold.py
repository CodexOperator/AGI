"""Small tmux hold seam used by durable restart paths.

The environment is passed with tmux ``-e`` rather than relying on the tmux
server's own environment, so a held child sees the same credential policy as a
direct Popen child.
"""
from __future__ import annotations

import subprocess
from collections.abc import Mapping, Sequence


def _cmd(args: Sequence[str], *, env: Mapping[str, str] | None = None,
          cwd: str | None = None) -> list[str]:
    """Return a tmux command with the requested child environment."""
    env_args = [arg for item in list((env or {}).items())
                for arg in ("-e", f"{item[0]}={item[1]}")]
    return ["tmux", *env_args, *args]


def start(*, session: str, name: str, command: Sequence[str],
          env: Mapping[str, str] | None = None, cwd: str | None = None) -> str:
    """Start (or replace) a named held pane and return its pane id."""
    args = ["new-session", "-d", "-s", session, "-n", name]
    if cwd:
        args += ["-c", cwd]
    args += [*command]
    proc = subprocess.run(_cmd(args, env=env), capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or "tmux start failed")
    return proc.stdout.strip()


def reattach(*, session: str, name: str,
             env: Mapping[str, str] | None = None) -> str:
    """Reattach a held pane, carrying the same environment contract."""
    proc = subprocess.run(
        _cmd(["attach-session", "-t", f"{session}:{name}"], env=env),
        capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or "tmux reattach failed")
    return proc.stdout.strip()


def restart(*, session: str, name: str, command: Sequence[str],
            env: Mapping[str, str] | None = None, cwd: str | None = None) -> str:
    """Start a held pane, the restart entry point used by dispatch."""
    return start(session=session, name=name, command=command, env=env, cwd=cwd)


__all__ = ["_cmd", "start", "reattach", "restart"]
