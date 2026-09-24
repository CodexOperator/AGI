"""Bounded rotation adapter for the public ``send.py`` router.

The router chooses communication transport; rotation owns these lifecycle and
seat-settings primitives. Keeping their imports here makes that boundary
explicit without copying rotation behavior or widening the public send API.
"""
from __future__ import annotations

from pathlib import Path


def _rotate():
    """Load the sibling lazily, matching the router's prior import timing."""
    import rotate
    return rotate


def commit_spawn_row(root: Path, **fields):
    return _rotate()._commit_spawn_row(root, **fields)


def git_toplevel(root: Path):
    return _rotate()._git_toplevel(root)


def push_season_branch(root: Path) -> str:
    return _rotate()._push_season_branch(root)


def finish_pending_swap_on_push(root: Path, seat: str, push: str) -> None:
    _rotate()._finish_pending_swap_on_push(root, seat, push)


def normalize_settings(value):
    return _rotate()._normalize_settings(value)


def default_tmux_session() -> str:
    return _rotate().DEFAULT_TMUX_SESSION
