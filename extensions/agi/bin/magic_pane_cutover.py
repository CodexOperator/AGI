#!/usr/bin/env python3
"""magic_pane_cutover.py — legacy-route cutover (goal:g7.16.1.7.3.4).

Wire inject+poll as THE delivery path; retire/bypass the four parent-measured
legacy routes (session_start_hook_paste · user_prompt_submit_meter ·
send_py_nudge · cc_send_message).

Owner (goal:g7.16.1.7.3 falsifier 4): after cutover, zero engine events are
delivered by a send-keys nudge, a hook's pasted text, or a second messaging
route; the census route table shows exactly one active route per event kind
(``tool_call_turn``).

This leaf is the CODE PATH gate + SoT cutover table. Live ``~/.claude/settings.json``
hook uninstall and live tmux attach stay deferred (owner: defer live attach
unless required). Messaging adapter (``adapters.magic_pane`` / g7.32.2*) stays
untouched. Pane owns no transport.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import magic_pane_inject as inj
import magic_pane_poll as poll

ACTIVE_ROUTE = "tool_call_turn"
LEGACY_POLICY = "bypassed"  # named for census; never used for delivery

# Parent-measured routes (goal:g7.16.1.7.3.1 fixture parent_measured_legacy_routes).
LEGACY_ROUTES = frozenset(
    {
        "session_start_hook_paste",
        "user_prompt_submit_meter",
        "send_py_nudge",
        "cc_send_message",
    }
)


class MagicPaneCutoverError(ValueError):
    """Cutover refused: legacy route, bad kind, or off-path delivery."""


def load_cutover(path: Path | None = None) -> dict[str, Any]:
    """Load v2 event-route SoT and require a cutover block."""
    data = inj.load_event_routes(path)
    cut = data.get("cutover")
    if not isinstance(cut, dict):
        raise MagicPaneCutoverError("fixture missing cutover block (g7.16.1.7.3.4)")
    if cut.get("active_route") != ACTIVE_ROUTE:
        raise MagicPaneCutoverError(
            f"cutover.active_route must be {ACTIVE_ROUTE!r}, got {cut.get('active_route')!r}"
        )
    if cut.get("legacy_policy") != LEGACY_POLICY:
        raise MagicPaneCutoverError(
            f"cutover.legacy_policy must be {LEGACY_POLICY!r}, got {cut.get('legacy_policy')!r}"
        )
    return data


def is_legacy(route: str) -> bool:
    return route in LEGACY_ROUTES


def assert_not_legacy(route: str) -> None:
    """Refuse any delivery attempt that names a legacy route."""
    if is_legacy(route):
        raise MagicPaneCutoverError(
            f"legacy route bypassed: {route!r} → use {ACTIVE_ROUTE!r} "
            f"(inject+poll; goal:g7.16.1.7.3.4)"
        )
    if route != ACTIVE_ROUTE:
        raise MagicPaneCutoverError(
            f"unknown/non-active route {route!r}; only {ACTIVE_ROUTE!r} is live after cutover"
        )


def legacy_status(route: str, *, data: dict[str, Any] | None = None) -> dict[str, str]:
    """Census row for one legacy route name."""
    data = data if data is not None else load_cutover()
    table = (data.get("cutover") or {}).get("legacy_routes") or {}
    row = table.get(route)
    if not isinstance(row, dict):
        if route in LEGACY_ROUTES:
            return {
                "route": route,
                "status": LEGACY_POLICY,
                "replaced_by": ACTIVE_ROUTE,
            }
        raise MagicPaneCutoverError(f"not a legacy route: {route!r}")
    status = str(row.get("status") or LEGACY_POLICY)
    replaced = str(row.get("replaced_by") or ACTIVE_ROUTE)
    if status != LEGACY_POLICY or replaced != ACTIVE_ROUTE:
        raise MagicPaneCutoverError(
            f"legacy row malformed for {route!r}: status={status!r} replaced_by={replaced!r}"
        )
    return {"route": route, "status": status, "replaced_by": replaced}


def route_table(*, data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Census-facing table: exactly one active route per event kind.

    Each row: ``{event_kind, channel, kind_tag, active_route, legacy_bypassed}``.
    ``active_route`` is always ``tool_call_turn``; legacy names appear only
    under ``legacy_bypassed`` (never as a second active route).
    """
    data = data if data is not None else load_cutover()
    rows: list[dict[str, Any]] = []
    for r in data.get("routes") or []:
        kind = r["event_kind"]
        legacy = list(r.get("legacy_routes") or [])
        for name in legacy:
            if name not in LEGACY_ROUTES:
                raise MagicPaneCutoverError(
                    f"route row {kind!r} names unknown legacy {name!r}"
                )
        rows.append(
            {
                "event_kind": kind,
                "channel": r["channel"],
                "kind_tag": r["kind_tag"],
                "active_route": ACTIVE_ROUTE,
                "legacy_bypassed": sorted(legacy),
            }
        )
    # uniqueness — one active route column, one row per kind
    kinds = [row["event_kind"] for row in rows]
    if len(kinds) != len(set(kinds)):
        raise MagicPaneCutoverError(f"duplicate event_kind in cutover table: {kinds}")
    for row in rows:
        if row["active_route"] != ACTIVE_ROUTE:
            raise MagicPaneCutoverError(f"non-active row: {row}")
    return rows


def deliver(
    root: Path,
    post_id: str,
    event_kind: str,
    body: str,
    *,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> Path:
    """THE cutover delivery path: inject envelope → local poll enqueue.

    Refuses if callers try to name a legacy route as the target. Returns the
    queued file path (local refs only — pane owns no transport).
    """
    data = routes if routes is not None else load_cutover(path)
    # Gate: active route only
    assert_not_legacy(ACTIVE_ROUTE)  # sanity: ACTIVE is not legacy
    row = inj.row_for_kind(data, event_kind)
    if row.get("target_route") != ACTIVE_ROUTE:
        raise MagicPaneCutoverError(
            f"event_kind {event_kind!r} target_route is not {ACTIVE_ROUTE!r}"
        )
    # Any attempt to "deliver via" a legacy name is refused up-front.
    for legacy in row.get("legacy_routes") or []:
        # naming them as the *active* path is the bug; listing as bypassed is fine
        if legacy == ACTIVE_ROUTE:
            raise MagicPaneCutoverError("legacy_routes must not contain active route")
    env = inj.build_envelope(event_kind, body, routes=data, path=path)
    if env["target_route"] != ACTIVE_ROUTE:
        raise MagicPaneCutoverError("envelope target_route drifted off cutover")
    return poll.enqueue(root, post_id, env)


def refuse_legacy_delivery(route: str, *args: Any, **kwargs: Any) -> None:
    """Explicit bypass stub for the four legacy entrypoints.

    Call sites that still name a legacy route invoke this instead of pasting /
    nudging / SendMessage. Always raises — cutover is the only path.
    """
    assert_not_legacy(route)


def free_lane_probe() -> dict[str, str]:
    """ONE-pi free lane (no second pi template) — same SoT as inject/poll."""
    return inj.free_lane_spec()
