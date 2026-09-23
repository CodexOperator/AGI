"""Durable named tmux pane hold — harness-agnostic (`goal:g7.31.1.2`).

A bare `new-session ... <cmd>` does NOT hold a pane: when its process dies the
session exits and the server with it. With `remain-on-exit on` the pane
survives (`pane_dead=1`, same `pane_id` `%N`, same window name), and
`respawn-pane -k` gives a NEW pid in that SAME pane. That is the hold.

No harness name lives here, and every tmux command is an argv LIST: a pane
name is never interpolated into a shell string.
"""
from __future__ import annotations

import subprocess

DEFAULT_TMUX_SESSION = "agi-rc"


def pane_target(session: str, name: str) -> str:
    """`<session>:<name>` — how every tmux command addresses one pane."""
    return f"{session}:{name}"


def _tmux(tmux_bin: str, *args: str, check: bool = True):
    return subprocess.run([tmux_bin, *args], check=check,
                          capture_output=True, text=True)


def pane_field(*, tmux_session: str, name: str, field: str,
               tmux_bin: str = "tmux") -> str | None:
    """One `#{field}` for the named pane, or None when it is not there."""
    out = _tmux(tmux_bin, "list-panes", "-t", pane_target(tmux_session, name),
                "-F", f"#{{{field}}}", check=False).stdout.strip()
    return out or None


def pane_id(**kw) -> str | None:
    """Live `%N` — stable across process pid churn."""
    return pane_field(field="pane_id", **kw)


def pane_pid(**kw) -> int | None:
    """Live pane pid read back from tmux, never a Popen pid."""
    value = pane_field(field="pane_pid", **kw)
    return int(value) if value else None


def has_pane(*, tmux_session: str, name: str, tmux_bin: str = "tmux") -> bool:
    """Is a window named `name` in `tmux_session`, dead or alive?"""
    proc = _tmux(tmux_bin, "list-windows", "-t", tmux_session,
                 "-F", "#{window_name}", check=False)
    return name in proc.stdout.splitlines() if proc.returncode == 0 else False


def ensure_pane(*, tmux_session: str, name: str, argv, cwd=None, env=None,
                log_file=None, tmux_bin: str = "tmux") -> int | None:
    """Put `argv` in the pane named `name`; return its live `pane_pid`.

    Existing window -> `respawn-pane -k` (same pane id/name, new pid); else
    `new-session -d` then `remain-on-exit on`.
    """
    target = pane_target(tmux_session, name)
    cmd = [str(a) for a in argv]
    if env:
        cmd = ["env", *[f"{k}={v}" for k, v in env.items()], *cmd]
    if log_file:
        # `$1` is the log; the rest is argv. `"$@"` execs without a shell
        # re-parsing a name, so no name can break out of a string.
        cmd = ["bash", "-c", 'exec >>"$1" 2>&1; shift; exec "$@"',
               "pane-hold", str(log_file), *cmd]
    where = ["-c", str(cwd)] if cwd else []
    if has_pane(tmux_session=tmux_session, name=name, tmux_bin=tmux_bin):
        _tmux(tmux_bin, "respawn-pane", "-k", "-t", target, *where, *cmd)
    else:
        _tmux(tmux_bin, "new-session", "-d", "-s", tmux_session, "-n", name,
              *where, *cmd)
        _tmux(tmux_bin, "set-option", "-w", "-t", target,
              "remain-on-exit", "on")
    return pane_pid(tmux_session=tmux_session, name=name, tmux_bin=tmux_bin)
