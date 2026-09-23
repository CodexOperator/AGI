"""Durable named tmux pane seam (goal:g7.31.1.2).

A persistent seat keeps ONE named tmux window across process churn. The first
launch creates that window with `remain-on-exit on`, so a dead command leaves
the pane standing; a later restart calls `ensure_pane` again and it
`respawn-window`s the SAME window by name instead of issuing a second
`new-window`. The runner is injectable so a test drives a fake tmux and
asserts on the recorded argv.
"""
from __future__ import annotations

import subprocess


def _default_runner(argv):
    """The real tmux call. `ensure_pane` treats its result like any runner's."""
    return subprocess.run(argv, capture_output=True, text=True, timeout=10)


def _window_names(runner, session):
    proc = runner(["tmux", "list-windows", "-t", session,
                   "-F", "#{window_name}"])
    return (getattr(proc, "stdout", "") or "").split()


def ensure_pane(session, name, shell_cmd, *, runner=None):
    """Launch, or reattach to, the durable pane named `name`.

    Returns `("new", proc)` on first launch (the window is then made durable
    with `remain-on-exit on`) and `("respawn", proc)` when a window of that
    name already exists, in which case the command is sent into that SAME
    window with `respawn-window -k`. A second `new-window` is never issued for
    an existing name.
    """
    run = runner or _default_runner
    target = f"{session}:{name}"
    if name in _window_names(run, session):
        # `respawn-window` in tmux 3.4 does NOT accept `-P` (`unknown flag`),
        # so the @id is not printed on reattach; the caller that needs it may
        # read it separately. Never a second `new-window`.
        proc = run(["tmux", "respawn-window", "-k", "-t", target,
                    shell_cmd])
        return "respawn", proc
    proc = run(["tmux", "new-window", "-t", session, "-n", name,
                "-P", "-F", "#{window_id}", shell_cmd])
    if getattr(proc, "returncode", 1) == 0:
        run(["tmux", "set-option", "-w", "-t", target,
             "remain-on-exit", "on"])
    return "new", proc
