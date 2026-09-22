#!/usr/bin/env python3
"""send_seat_seam.py — owns every rotate-dependent call send.py makes
(goal:g7.32.4, falsifier 1). A BOUNDARY, not a decoupling: this module still
imports rotate, so rotate stays on send.py's import graph through one edge,
while send.py's bytes carry ZERO `import rotate`."""
import rotate

DEFAULT_TMUX_SESSION = rotate.DEFAULT_TMUX_SESSION


def git_toplevel(root):
    return rotate._git_toplevel(root)


def push_season_branch(root):
    return rotate._push_season_branch(root)


def finish_pending_swap_on_push(root, name, push):
    return rotate._finish_pending_swap_on_push(root, name, push)


def normalize_settings(settings):
    return rotate._normalize_settings(settings)


def commit_spawn_row(root, *, seat, generation, session_id, window, pid):
    return rotate._commit_spawn_row(
        root, seat=seat, generation=generation,
        session_id=session_id, window=window, pid=pid)