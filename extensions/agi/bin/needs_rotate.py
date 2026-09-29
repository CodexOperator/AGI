#!/usr/bin/env python3
"""needs_rotate.py — AGI_BOX-gated act + clear for needs-rotate (g7.31.3.3.3).

Owner design (goal:g7.31.3.3.3): only the box hosting the post acts (checked
via AGI_BOX); the loop clears `needs-rotate: true` after acting.

Public API
----------
may_act(root, row) -> bool
    True iff boxes.row_is_local — non-matching AGI_BOX must not mutate.

actions_path(root) -> Path
    Local runtime action log (gitignored sessions/).

record_action(root, post, kind, detail="") -> str
    Append one action record; return its action_id.

clear_needs_rotate(root, row, action_id) -> dict
    Return a COPY of row with needs-rotate cleared. Refuses (raises) when
    AGI_BOX does not match the row host, or when action_id is absent from the
    action log (negative: no silent clear).

act_and_clear(root, row, kind, detail="", act_fn=None) -> dict
    If may_act: record action, optionally run act_fn(row), then clear.
    If not may_act: return the original row UNCHANGED (cross-box probe).
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Callable

import boxes


def actions_path(root: Path | None) -> Path:
    if root is None:
        raise ValueError("needs_rotate.actions_path: root is required")
    return Path(root) / ".agi" / "sessions" / "needs-rotate-actions.jsonl"


def may_act(root: Path | None, row: dict | None) -> bool:
    """Host-only gate: act only when AGI_BOX matches the row's box cell."""
    if root is None or not isinstance(row, dict):
        return False
    return boxes.row_is_local(Path(root), row)


def _append_action(root: Path, rec: dict) -> Path:
    path = actions_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")
    return path


def record_action(
    root: Path | None,
    post: str,
    kind: str,
    detail: str = "",
) -> str:
    """Append an action record; return action_id. Required before clear."""
    if root is None:
        raise ValueError("needs_rotate.record_action: root is required")
    if not post or not kind:
        raise ValueError("needs_rotate.record_action: post and kind required")
    action_id = uuid.uuid4().hex[:16]
    rec = {
        "action_id": action_id,
        "post": post,
        "kind": kind,
        "detail": detail or "",
        "ts": time.time(),
    }
    _append_action(Path(root), rec)
    return action_id


def action_recorded(root: Path | None, action_id: str) -> bool:
    """True when action_id appears in the local action log."""
    if not action_id:
        return False
    path = actions_path(root)
    if not path.is_file():
        return False
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(rec, dict) and rec.get("action_id") == action_id:
                return True
    except OSError:
        return False
    return False


def clear_needs_rotate(
    root: Path | None,
    row: dict,
    action_id: str,
) -> dict:
    """Clear needs-rotate on a row COPY after a recorded action on this box.

    Raises PermissionError on cross-box or missing action record — never
    silently clears.
    """
    if root is None or not isinstance(row, dict):
        raise ValueError("needs_rotate.clear_needs_rotate: root and row required")
    if not may_act(root, row):
        raise PermissionError(
            f"needs_rotate: AGI_BOX does not match row box="
            f"{row.get('box')!r} — cross-box clear refused"
        )
    if not action_recorded(root, action_id):
        raise PermissionError(
            f"needs_rotate: silent clear refused — action_id={action_id!r} "
            f"not in {actions_path(root)}"
        )
    out = dict(row)
    out["needs-rotate"] = False
    # also clear snake_case alias if present
    if "needs_rotate" in out:
        out["needs_rotate"] = False
    out["needs_rotate_cleared_by"] = action_id
    return out


def act_and_clear(
    root: Path | None,
    row: dict,
    kind: str,
    detail: str = "",
    act_fn: Callable[[dict], Any] | None = None,
) -> dict:
    """Host-only act + clear. Cross-box returns row unchanged (no mutate)."""
    if root is None or not isinstance(row, dict):
        raise ValueError("needs_rotate.act_and_clear: root and row required")
    if not may_act(root, row):
        # Cross-box probe: do not mutate.
        return row
    post = str(row.get("name") or row.get("post") or "").strip() or "?"
    action_id = record_action(root, post, kind, detail=detail)
    if act_fn is not None:
        act_fn(row)
    return clear_needs_rotate(root, row, action_id)


if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
