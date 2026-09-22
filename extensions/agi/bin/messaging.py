"""messaging.py — magic-pane messaging seam (goal:g7.32.2).

Same harness: native pane typing. Different harness: nudge (intent) then
send.py (transport). Unknown harness refuses by name, never defaults.
"""
from __future__ import annotations

class UnknownHarness(ValueError):
    """An empty/None harness has no route; never silently default."""

class CrossHarnessOnNative(RuntimeError):
    """Cross-harness offered to the native pane path."""

class SameHarnessOnCross(RuntimeError):
    """Same-harness offered to the nudge->send path."""

def _identity(harness):
    """Whitespace-only strings are unknown; non-strings pass through."""
    return harness.strip() if isinstance(harness, str) else harness

def route(sender_harness, recipient_harness):
    s = _identity(sender_harness)
    r = _identity(recipient_harness)
    if not s or not r:
        raise UnknownHarness(
            f"unknown harness: sender={sender_harness!r} recipient={recipient_harness!r}")
    return "native" if s == r else "nudge_send"

def native_send(pane, *, sender_harness, recipient_harness, to, text):
    if route(sender_harness, recipient_harness) != "native":
        raise CrossHarnessOnNative(
            f"{sender_harness!r}->{recipient_harness!r} is cross-harness; use cross_harness_send")
    pane.type(to, text)
    return {"route": "native", "steps": [("pane.type", to, text)]}

def cross_harness_send(send_py, nudge, *, sender_harness, recipient_harness, to, text):
    if route(sender_harness, recipient_harness) != "nudge_send":
        raise SameHarnessOnCross(
            f"{sender_harness!r}->{recipient_harness!r} is same-harness; use native_send")
    nudge.write(to, text)
    send_py.send(to, text)
    return {"route": "nudge_send",
            "steps": [("nudge.write", to, text), ("send.send", to, text)]}