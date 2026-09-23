#!/usr/bin/env python3
"""messaging.py — magic-pane messaging (goal:g7.32.2).

Composes, never defines: the pane method (g7.32.3) and send.py (g7.32.4).
Same harness = NATIVE; cross-harness = NUDGE artifact -> send. A missing
seam raises MessagingError -- it never falls through to the other path.
"""
from __future__ import annotations

import enum
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

class MessagingError(RuntimeError):
    """Raised when the chosen route's seam is missing -- never a fallthrough."""

class Routing(enum.Enum):
    NATIVE = "native"
    NUDGE = "nudge"

@dataclass
class Delivery:
    route: str
    steps: list[str] = field(default_factory=list)
    nudge: Mapping[str, Any] | None = None
    sent: Any = None

def plan(sender, recipient, sender_harness, recipient_harness) -> Routing:
    """Pure, no I/O: equal harnesses are native; anything else is a nudge."""
    return (Routing.NATIVE if sender_harness == recipient_harness
            else Routing.NUDGE)

def build_nudge(sender, recipient, body, reason="") -> dict:
    """The nudge artifact records pane INTENT (from/to/body/reason/ts); a
    request for transport, not a dm."""
    return {"pane_intent": True, "from": sender, "to": recipient,
            "body": body, "reason": reason, "ts": time.time()}

def default_send_runner(nudge: Mapping[str, Any]) -> Any:
    """Invoke the real send.py CLI; path relative to this file."""
    argv = [sys.executable, str(Path(__file__).resolve().parent / "send.py"),
            "send", str(nudge["to"]), str(nudge["body"])]
    return subprocess.run(argv, capture_output=True, text=True, check=True)

def deliver(sender, recipient, body, *, sender_harness, recipient_harness,
            pane_send: Callable[[str, str], Any] | None = None,
            send_runner: Callable[[Mapping[str, Any]], Any] | None = None,
            nudge_sink: Callable[[Mapping[str, Any]], Any] | None = None
            ) -> Delivery:
    """NATIVE calls pane_send only; NUDGE emits the artifact then calls
    send_runner. The other transport is never touched. Fail closed."""
    route = plan(sender, recipient, sender_harness, recipient_harness)
    if route is Routing.NATIVE:
        if pane_send is None:
            raise MessagingError("NATIVE route needs pane_send (g7.32.3)")
        out = Delivery(route=route.value)
        out.sent = pane_send(recipient, body)
        out.steps.append("native")
        return out
    if send_runner is None:
        raise MessagingError("NUDGE route needs send_runner (g7.32.4)")
    out = Delivery(route=route.value)
    out.nudge = build_nudge(sender, recipient, body)
    if nudge_sink is not None:
        nudge_sink(out.nudge)
    out.steps.append("nudge")
    out.sent = send_runner(out.nudge)
    out.steps.append("send")
    return out
