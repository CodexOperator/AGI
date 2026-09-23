#!/usr/bin/env python3
"""seat_registry_commit.py — the ONE seam through which send.py reaches
rotate's spawn/push/pending-swap internals (goal:g7.32.4).

send.py is the thin transport router: it chooses a transport and never embeds
rotation/formation/push policy. The three acts below are the only operations
send.py needs from rotate's orchestration, so they live here behind this
seam; send.py calls this module and never `rotate._commit_spawn_row`,
`rotate._push_season_branch` or `rotate._finish_pending_swap_on_push`
directly. Rotate keeps the implementations; this module is the address
send.py is allowed to know.

`rotate` is imported lazily inside each act (the send.py pattern: same
directory, no import cycle at module load). Each act forwards verbatim and
returns rotate's return value unchanged.
"""
from __future__ import annotations

from pathlib import Path


def commit_spawn_row(root: Path, *, seat: str, generation: int,
                     session_id: str | None = None,
                     window: str = "",
                     pid: int | None = None) -> str:
    """Commit a seat's own spawn row — the ONE seam to
    `rotate._commit_spawn_row`. Returns rotate's one-line outcome."""
    import rotate  # local: same dir, no import cycle
    return rotate._commit_spawn_row(
        root, seat=seat, generation=generation,
        session_id=session_id, window=window, pid=pid)


def push_season_branch(root: Path) -> str:
    """Push the season branch — the ONE seam to
    `rotate._push_season_branch`. Returns rotate's push line."""
    import rotate  # local: same dir, no import cycle
    return rotate._push_season_branch(root)


def finish_pending_swap_on_push(root: Path, seat_name: str,
                                push: str | None) -> str:
    """Complete a deferred pending-key swap when `push` reports success —
    the ONE seam to `rotate._finish_pending_swap_on_push`. Returns rotate's
    one-line outcome ('' when it is a no-op)."""
    import rotate  # local: same dir, no import cycle
    return rotate._finish_pending_swap_on_push(root, seat_name, push)
