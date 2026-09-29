#!/usr/bin/env python3
"""dm_no_inbox.py — no separate inbox once post-branch route holds (g7.32.6.6).

Owner design (goal:g7.32.6 design line 6): no separate inbox system;
.agi/sessions/inbox/* retires once send/cron/nudge/read hold on the
post-branch route.

Public API
----------
is_inbox_path(path) -> bool
is_post_branch_dm_path(path) -> bool
assert_allowed_dm_path(path) -> str
    Return normalized path when it is a post-branch dm path; raise
    PermissionError naming inbox otherwise.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath


def _parts(path: str | Path) -> tuple[str, ...]:
    p = PurePosixPath(str(path).replace("\\", "/"))
    return tuple(x for x in p.parts if x not in {".", "/"})


def is_inbox_path(path: str | Path | None) -> bool:
    if path is None:
        return False
    parts = _parts(path)
    # .../sessions/inbox/... or bare inbox/<seat>.md under sessions
    for i, part in enumerate(parts):
        if part == "inbox":
            # classic sessions/inbox
            if i > 0 and parts[i - 1] == "sessions":
                return True
            if i > 0 and parts[i - 1] == ".agi" and i + 1 < len(parts):
                return True
    return "sessions/inbox" in str(path).replace("\\", "/")


def is_post_branch_dm_path(path: str | Path | None) -> bool:
    if path is None:
        return False
    parts = _parts(path)
    if "inbox" in parts:
        return False
    # comms/.../dm/<a>--<b>.md  OR  .../dm/<a>--<b>.md
    if "dm" not in parts:
        return False
    name = parts[-1]
    return name.endswith(".md") and "--" in name


def assert_allowed_dm_path(path: str | Path | None) -> str:
    """Refuse inbox paths by name; accept post-branch dm paths only."""
    if path is None or str(path).strip() == "":
        raise ValueError("dm_no_inbox: path required")
    text = str(path)
    if is_inbox_path(text):
        raise PermissionError(
            f"dm_no_inbox: inbox path refused by name: {text!r} — "
            f"post-branch dm route only (goal:g7.32.6.6)"
        )
    if not is_post_branch_dm_path(text):
        raise PermissionError(
            f"dm_no_inbox: not a post-branch dm path: {text!r}"
        )
    return text


if __name__ == "__main__":
    import argparse

    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
