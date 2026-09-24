"""Durable launch seam for dispatch rounds.

The default is deliberately the safe Popen fallback. Deployments that provide
an adapter can install ``LAUNCHER`` with the same call shape; the name is a
stable identity, not a generated tmux window.
"""
from __future__ import annotations
import subprocess
from typing import Any, Callable

LAUNCHER: Callable[..., tuple[Any, bool]] | None = None

def open_round(argv, log, cwd, env, *, name, wrap_argv):
    """Open one round and return ``(process, created)``.

    ``created`` is true only when the durable adapter actually created a new
    launch. Popen fallback and adapter reuse are both false.
    """
    wrapped = wrap_argv(argv)
    if LAUNCHER is not None:
        proc, created = LAUNCHER(wrapped, log, cwd=cwd, env=env, name=name)
        return proc, bool(created)
    with open(log, "wb") as logf:
        proc = subprocess.Popen(wrapped, stdout=logf, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, start_new_session=True,
                                cwd=cwd, env=env)
    return proc, False
