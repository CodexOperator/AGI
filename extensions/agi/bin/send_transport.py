"""Narrow transport seam for send.py.

The comms writer owns inbox policy; these helpers isolate the small amount of
rotate orchestration needed to publish a seat-row change or resolve tmux
metadata.  Keeping the import here prevents the transport writer from
acquiring an orchestration dependency.
"""
from __future__ import annotations


def commit_spawn_row(*args, **kwargs):
    import rotate
    return rotate._commit_spawn_row(*args, **kwargs)


def git_toplevel(*args, **kwargs):
    import rotate
    return rotate._git_toplevel(*args, **kwargs)


def push_season_branch(*args, **kwargs):
    import rotate
    return rotate._push_season_branch(*args, **kwargs)


def finish_pending_swap_on_push(*args, **kwargs):
    import rotate
    return rotate._finish_pending_swap_on_push(*args, **kwargs)


def normalize_settings(*args, **kwargs):
    import rotate
    return rotate._normalize_settings(*args, **kwargs)


def default_tmux_session():
    import rotate
    return rotate.DEFAULT_TMUX_SESSION
