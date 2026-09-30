#!/usr/bin/env python3
"""magic_pane_inject.py — uniform tool-call-turn envelope (goal:g7.16.1.7.3.2).

Owner: inject ALL info via a uniform tool-call turn; the tool RETURN is the
actual message; always tagged dm|engine (+ subtags). Built on the v2
event-route SoT (goal:g7.16.1.7.3.1). Render/dispatch only through
`pi_adapter` + `extensions/agi/templates/harness/pi.toml` on the ONE-pi
**free** row — never a second pi template and never a hand-built argv.

CC-compat: pi extension events `session_start` / `before_agent_start` /
`tool_result` mirror CC hooks SessionStart / UserPromptSubmit / PostToolUse
(not npm cc-mirror variants). This module documents that map; it does NOT
import the messaging adapter or the send transport module.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CHANNELS = frozenset({"dm", "engine"})
TARGET_ROUTE = "tool_call_turn"
DEFAULT_FIXTURE = (
    Path(__file__).resolve().parent.parent
    / "tests" / "fixtures" / "magic_pane_event_routes.json"
)

# Pi extension events → CC hooks they mirror (prove inject on free-pi first).
# Deliberately not npm `cc-mirror*` packages — native pi ext events only.
CC_COMPAT_MIRROR: dict[str, dict[str, str]] = {
    "session_start": {
        "pi_event": "session_start",
        "cc_hook": "SessionStart",
        "legacy_route": "session_start_hook_paste",
        "role": "session bootstrap / first_turn_docs · rotation_prompt entry",
    },
    "before_agent_start": {
        "pi_event": "before_agent_start",
        "cc_hook": "UserPromptSubmit",
        "legacy_route": "user_prompt_submit_meter",
        "role": "pre-turn meter / memory_alarm · write_commit_result nudge",
    },
    "tool_result": {
        "pi_event": "tool_result",
        "cc_hook": "PostToolUse",
        "legacy_route": "cc_send_message",
        "role": "tool RETURN carries the message body (inject contract)",
    },
}


class MagicPaneInjectError(ValueError):
    """Envelope refused: bad channel, kind_tag, or route."""


def load_event_routes(path: Path | None = None) -> dict[str, Any]:
    """Load the v2 event-route SoT fixture."""
    p = path or DEFAULT_FIXTURE
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("schema") != "magic-pane-event-routes/v2":
        raise MagicPaneInjectError(
            f"expected schema magic-pane-event-routes/v2, got {data.get('schema')!r}"
        )
    return data


def row_for_kind(data: dict[str, Any], event_kind: str) -> dict[str, Any]:
    """Return the unique route row for `event_kind`."""
    matches = [r for r in data.get("routes") or [] if r.get("event_kind") == event_kind]
    if not matches:
        raise MagicPaneInjectError(f"unknown event_kind: {event_kind!r}")
    if len(matches) > 1:
        raise MagicPaneInjectError(f"duplicate event_kind rows: {event_kind!r}")
    return matches[0]


def build_envelope(
    event_kind: str,
    body: str,
    *,
    routes: dict[str, Any] | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    """Build a tool-call-turn envelope from a v2 event-route row.

    Returns ``{channel, kind_tag, body, event_kind, target_route, tool_return}``
    where ``body`` (== ``tool_return``) is what the tool RETURN carries — the
    message itself. No parallel chat-turn paste of the same body.
    """
    data = routes if routes is not None else load_event_routes(path)
    row = row_for_kind(data, event_kind)
    channel = row.get("channel")
    kind_tag = row.get("kind_tag")
    target = row.get("target_route")
    if channel not in CHANNELS:
        raise MagicPaneInjectError(f"channel must be dm|engine, got {channel!r}")
    if not isinstance(kind_tag, str) or not kind_tag.startswith(f"{channel}."):
        raise MagicPaneInjectError(
            f"kind_tag must be '{{channel}}.{{event_kind}}', got {kind_tag!r}"
        )
    if target != TARGET_ROUTE:
        raise MagicPaneInjectError(
            f"target_route must be {TARGET_ROUTE!r}, got {target!r}"
        )
    if not isinstance(body, str):
        raise MagicPaneInjectError(f"body must be str, got {type(body).__name__}")
    return {
        "channel": channel,
        "kind_tag": kind_tag,
        "body": body,
        "event_kind": event_kind,
        "target_route": TARGET_ROUTE,
        # tool RETURN bytes ARE the message (owner contract)
        "tool_return": body,
        "inject_shape": "tool_call_turn",
        "message_is": "tool_return",
    }


def tool_return_payload(envelope: dict[str, Any]) -> str:
    """The sole tool-return payload — the message body, nothing else."""
    if envelope.get("message_is") != "tool_return":
        raise MagicPaneInjectError("envelope.message_is must be tool_return")
    body = envelope.get("body")
    if body != envelope.get("tool_return"):
        raise MagicPaneInjectError("body and tool_return must be identical")
    if not isinstance(body, str):
        raise MagicPaneInjectError("tool_return must be str")
    return body


def free_lane_spec(data: dict[str, Any] | None = None) -> dict[str, str]:
    """ONE-pi free build lane from the SoT (harness/row/adapter/template)."""
    data = data if data is not None else load_event_routes()
    lane = data["build_lane"]
    return {
        "harness": str(lane["harness"]),
        "row": str(lane["row"]),
        "adapter": str(lane["adapter"]),
        "template": str(lane["template"]),
        "harness_name": f"{lane['harness']}:{lane['row']}",  # pi:free
        "alias": "pi-free",
    }


def cc_compat_probe() -> dict[str, Any]:
    """Document (+ lightly probe) pi↔CC event mirror for the inject contract.

    Does not load pi runtime extensions in-test (free-pi may not). Returns the
    mirror table and whether each named pi event appears in the installed
    pi-coding-agent types (best-effort path probe).
    """
    installed: dict[str, bool] = {}
    candidates = [
        Path.home() / ".npm-global/lib/node_modules/@mariozechner/pi-coding-agent"
        / "dist/core/extensions/types.d.ts",
        Path("/home/belam/.npm-global/lib/node_modules/@mariozechner/pi-coding-agent"
             "/dist/core/extensions/types.d.ts"),
    ]
    text = ""
    for c in candidates:
        if c.is_file():
            text = c.read_text(encoding="utf-8", errors="replace")
            break
    for key, row in CC_COMPAT_MIRROR.items():
        ev = row["pi_event"]
        installed[ev] = (f'type: "{ev}"' in text) or (f'"{ev}"' in text and "on(event" in text) if text else False
        # also accept on(event: "…") form
        if text and f'event: "{ev}"' in text:
            installed[ev] = True
        if text and f'on(event: "{ev}"' in text:
            installed[ev] = True
    return {
        "mirror": dict(CC_COMPAT_MIRROR),
        "pi_events_in_types": installed,
        "note": (
            "CC-compat via native pi extension events mirroring CC hooks; "
            "not npm cc-mirror variants. Envelope deliverable as tool_result "
            "body (message_is=tool_return) after session_start/before_agent_start."
        ),
    }
