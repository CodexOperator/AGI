#!/usr/bin/env python3
"""spawn_refusal.py — named-row refusal + one reply cap (g7.31.3.3.4).

Owner design (goal:g7.31.3.3.4): a refusal writes the row by name AND sends
one reply to the requesting post via the send reply route; cap one reply per
failed request (no reply storms).

Public API
----------
memo_path(root) -> Path
    Local runtime memo of (request_id -> reply_sent).

stamp_row(root, row_name, request_id, reason) -> dict
    Write/update the named refusal stamp in the runtime file.

reply_already_sent(root, request_id) -> bool
send_one_reply(root, request_id, to_post, body, reply_fn) -> bool
    Invoke reply_fn exactly once per request_id. Second call returns False
    without invoking reply_fn (negative: no multi-reply storms).

refuse(root, row_name, request_id, reason, to_post, body, reply_fn) -> dict
    Stamp named row + one reply. Returns the stamp record.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Callable


def memo_path(root: Path | None) -> Path:
    if root is None:
        raise ValueError("spawn_refusal.memo_path: root is required")
    return Path(root) / ".agi" / "sessions" / "spawn-refusal-memo.json"


def stamps_path(root: Path | None) -> Path:
    if root is None:
        raise ValueError("spawn_refusal.stamps_path: root is required")
    return Path(root) / ".agi" / "sessions" / "spawn-refusal-stamps.json"


def _read_json(path: Path, default: dict) -> dict:
    if not path.is_file():
        return dict(default)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return dict(default)
    return data if isinstance(data, dict) else dict(default)


def _write_json(path: Path, data: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def stamp_row(
    root: Path | None,
    row_name: str,
    request_id: str,
    reason: str,
) -> dict:
    """Stamp the named row in the local refusal stamps file."""
    if root is None or not row_name or not request_id:
        raise ValueError("spawn_refusal.stamp_row: root, row_name, request_id required")
    path = stamps_path(root)
    data = _read_json(path, {"rows": {}})
    rows = data.setdefault("rows", {})
    if not isinstance(rows, dict):
        rows = {}
        data["rows"] = rows
    rec = {
        "row": row_name,
        "request_id": request_id,
        "reason": reason or "",
        "ts": time.time(),
        "status": "refused",
    }
    rows[row_name] = rec
    _write_json(path, data)
    return rec


def reply_already_sent(root: Path | None, request_id: str) -> bool:
    if not request_id:
        return False
    memo = _read_json(memo_path(root), {"replies": {}})
    replies = memo.get("replies") or {}
    return bool(isinstance(replies, dict) and request_id in replies)


def send_one_reply(
    root: Path | None,
    request_id: str,
    to_post: str,
    body: str,
    reply_fn: Callable[[str, str], Any],
) -> bool:
    """Deliver exactly one reply per request_id via reply_fn(to_post, body).

    Returns True when this call delivered the reply; False when the cap
    already consumed the slot for this request_id (reply_fn NOT called).
    """
    if root is None or not request_id or not to_post:
        raise ValueError("spawn_refusal.send_one_reply: root, request_id, to_post required")
    if reply_fn is None:
        raise ValueError("spawn_refusal.send_one_reply: reply_fn required")
    path = memo_path(root)
    memo = _read_json(path, {"replies": {}})
    replies = memo.setdefault("replies", {})
    if not isinstance(replies, dict):
        replies = {}
        memo["replies"] = replies
    if request_id in replies:
        return False
    reply_fn(to_post, body)
    replies[request_id] = {
        "to": to_post,
        "ts": time.time(),
        "body_len": len(body or ""),
    }
    _write_json(path, memo)
    return True


def refuse(
    root: Path | None,
    row_name: str,
    request_id: str,
    reason: str,
    to_post: str,
    body: str,
    reply_fn: Callable[[str, str], Any],
) -> dict:
    """Stamp named row + send at most one reply for this request_id."""
    stamp = stamp_row(root, row_name, request_id, reason)
    sent = send_one_reply(root, request_id, to_post, body, reply_fn)
    stamp = dict(stamp)
    stamp["reply_sent"] = sent
    return stamp


if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
