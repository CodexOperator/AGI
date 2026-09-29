#!/usr/bin/env python3
"""dm_nudge_gate.py — nudge fires only from sync on local unread (g7.32.6.4).

Owner design (goal:g7.32.6 design line 4 + quiet HOLD): nudge = the box
sync; it fires only from the sync, on an unread dm for a post local to
this box. Quiet row blocks unless a [red] item comes through.

Public API
----------
is_unread(dm) -> bool
may_nudge(root, row, dm, *, from_sync=False) -> bool
    True only when ALL hold: from_sync, boxes.row_is_local, unread,
    and (not quiet OR body carries [red]).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import boxes


def is_unread(dm: dict | None) -> bool:
    """True when dm read flag is false/absent."""
    if not isinstance(dm, dict):
        return False
    if "read" not in dm:
        return True
    return dm.get("read") is False


def _quiet(row: dict | None) -> bool:
    if not isinstance(row, dict):
        return False
    q = row.get("quiet")
    if q is True or str(q).strip().lower() in {"true", "1", "yes"}:
        return True
    # settings cell may carry 'quiet'
    settings = str(row.get("settings") or "").strip().lower()
    return settings == "quiet"


def _has_red(dm: dict | None) -> bool:
    if not isinstance(dm, dict):
        return False
    body = str(dm.get("body") or "")
    tag = str(dm.get("tag") or "")
    return "[red]" in body.lower() or tag.lower() == "red" or dm.get("red") is True


def may_nudge(
    root: Path | None,
    row: dict | None,
    dm: dict | None,
    *,
    from_sync: bool = False,
) -> bool:
    """Gate: sync-only + local post + unread + quiet/[red] rule."""
    if not from_sync:
        return False
    if root is None or not isinstance(row, dict) or not isinstance(dm, dict):
        return False
    if not boxes.row_is_local(Path(root), row):
        return False
    if not is_unread(dm):
        return False
    if _quiet(row) and not _has_red(dm):
        return False
    return True


if __name__ == "__main__":
    import argparse

    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
