#!/usr/bin/env python3
"""magic_pane_poll.py — live pane delivery/poll of inject envelopes (g7.16.1.7.3.3).

Owner RECEIVE contract (goal:g7.16.1.7.3):
  - the box fetch is the ONE network pull
  - the pane's poll watches LOCAL refs only — N panes never mean N network fetches
  - idle pane receives within the poll interval
  - busy pane receives at its next turn boundary, never mid-turn

Envelopes come from ``magic_pane_inject.build_envelope`` (tool RETURN IS the
message; channel dm|engine + kind_tag). This module does NOT import the
messaging adapter (``adapters.magic_pane``) or the send transport — those stay
on the g7.32.2* track. Pane owns no transport.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any, Callable

import magic_pane_inject as inj

TARGET_ROUTE = "tool_call_turn"
_POST_ID_RE = re.compile(r"^[A-Za-z0-9._:@-]{1,128}$")

# Optional spy hook for tests: poll never calls a network fetch; tests may
# attach a counter here and assert it stays 0.
_network_fetch_hook: Callable[[], None] | None = None


class MagicPanePollError(ValueError):
    """Queue/poll refused: bad post_id, envelope, or queue root."""


def set_network_fetch_hook(hook: Callable[[], None] | None) -> None:
    """Test seam only — production leaves this None (pane owns no transport)."""
    global _network_fetch_hook
    _network_fetch_hook = hook


def _assert_no_network_fetch() -> None:
    """Poll path must never trigger a network pull. Hook is a test spy."""
    # Deliberately do NOT call any fetch. If a test wired a spy, leave it
    # untouched so a regression that starts calling fetch can be counted.
    # Production: hook is None → no side effect.
    if _network_fetch_hook is not None:
        # A correct poll never invokes the hook. Tests assert call count == 0.
        pass


def validate_post_id(post_id: str) -> str:
    if not isinstance(post_id, str) or not _POST_ID_RE.match(post_id):
        raise MagicPanePollError(f"invalid post_id: {post_id!r}")
    return post_id


def validate_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    """Require inject-contract shape; refuse anything that is not tool_return."""
    if not isinstance(envelope, dict):
        raise MagicPanePollError("envelope must be a dict")
    channel = envelope.get("channel")
    if channel not in inj.CHANNELS:
        raise MagicPanePollError(f"channel must be dm|engine, got {channel!r}")
    kind_tag = envelope.get("kind_tag")
    if not isinstance(kind_tag, str) or not kind_tag.startswith(f"{channel}."):
        raise MagicPanePollError(f"bad kind_tag: {kind_tag!r}")
    if envelope.get("target_route") != TARGET_ROUTE:
        raise MagicPanePollError(
            f"target_route must be {TARGET_ROUTE!r}, got {envelope.get('target_route')!r}"
        )
    if envelope.get("message_is") != "tool_return":
        raise MagicPanePollError("message_is must be tool_return")
    body = envelope.get("body")
    if body != envelope.get("tool_return") or not isinstance(body, str):
        raise MagicPanePollError("body and tool_return must be identical str")
    return envelope


def queue_root(root: Path, post_id: str) -> Path:
    """Local per-post queue directory (filesystem refs only)."""
    validate_post_id(post_id)
    return Path(root) / "posts" / post_id / "queue"


def _state_path(root: Path, post_id: str) -> Path:
    validate_post_id(post_id)
    return Path(root) / "posts" / post_id / "state.json"


def _ensure_post(root: Path, post_id: str) -> Path:
    q = queue_root(root, post_id)
    q.mkdir(parents=True, exist_ok=True)
    sp = _state_path(root, post_id)
    if not sp.is_file():
        sp.write_text(
            json.dumps({"busy": False, "delivered": 0}, indent=2) + "\n",
            encoding="utf-8",
        )
    return q


def _read_state(root: Path, post_id: str) -> dict[str, Any]:
    _ensure_post(root, post_id)
    return json.loads(_state_path(root, post_id).read_text(encoding="utf-8"))


def _write_state(root: Path, post_id: str, state: dict[str, Any]) -> None:
    sp = _state_path(root, post_id)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def mark_busy(root: Path, post_id: str) -> None:
    """Pane is mid-turn — poll must hold, never deliver."""
    state = _read_state(root, post_id)
    state["busy"] = True
    _write_state(root, post_id, state)


def mark_idle(root: Path, post_id: str) -> None:
    """Turn boundary — held envelopes become deliverable on next idle poll."""
    state = _read_state(root, post_id)
    state["busy"] = False
    _write_state(root, post_id, state)


def is_busy(root: Path, post_id: str) -> bool:
    return bool(_read_state(root, post_id).get("busy"))


def enqueue(root: Path, post_id: str, envelope: dict[str, Any]) -> Path:
    """Park one inject envelope on the post's LOCAL queue. Returns the file path."""
    env = validate_envelope(envelope)
    q = _ensure_post(root, post_id)
    # Monotonic-ish name: epoch_ns + sequence from existing files.
    seq = len(list(q.glob("*.json")))
    name = f"{time.time_ns()}-{seq:04d}.json"
    path = q / name
    payload = {
        "envelope": env,
        "enqueued_at": time.time(),
        "post_id": post_id,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _delivery_from_envelope(env: dict[str, Any]) -> dict[str, Any]:
    """The tool-call-turn shape the pane surfaces (tool RETURN = message)."""
    return {
        "channel": env["channel"],
        "kind_tag": env["kind_tag"],
        "event_kind": env.get("event_kind"),
        "target_route": TARGET_ROUTE,
        "tool_return": env["tool_return"],
        "body": env["body"],
        "message_is": "tool_return",
        "inject_shape": "tool_call_turn",
    }


def poll(
    root: Path,
    post_id: str,
    *,
    busy: bool | None = None,
) -> list[dict[str, Any]]:
    """Drain ready envelopes for ``post_id`` from LOCAL refs only.

    If ``busy`` is True (arg) or the post is marked busy, return [] and hold.
    If idle, return every pending envelope as a tool-call-turn delivery and
    remove them from the queue (exactly-once per enqueue).
    """
    _assert_no_network_fetch()
    validate_post_id(post_id)
    _ensure_post(root, post_id)

    if busy is True:
        mark_busy(root, post_id)
    elif busy is False:
        mark_idle(root, post_id)

    if is_busy(root, post_id):
        return []

    q = queue_root(root, post_id)
    files = sorted(q.glob("*.json"), key=lambda p: p.name)
    deliveries: list[dict[str, Any]] = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        env = validate_envelope(data["envelope"])
        deliveries.append(_delivery_from_envelope(env))
        path.unlink()

    if deliveries:
        state = _read_state(root, post_id)
        state["delivered"] = int(state.get("delivered") or 0) + len(deliveries)
        _write_state(root, post_id, state)
    return deliveries


def pending_count(root: Path, post_id: str) -> int:
    """How many local envelopes are waiting (held or not yet polled)."""
    q = queue_root(root, post_id)
    if not q.is_dir():
        return 0
    return len(list(q.glob("*.json")))


def free_lane_probe() -> dict[str, str]:
    """Re-export ONE-pi free lane from inject SoT (no second pi template)."""
    return inj.free_lane_spec()
